/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Mark Bank — source-material reader.
 *
 * Some cards are not answerable from their prompt alone. This reader opens the
 * exact printed source pages or companion illustration sheets from Paper
 * Trail's SEC corpus before the marking-scheme reveal. Pages stay as PDF
 * renders rather than retyped HTML so layout, imagery, emphasis and examination
 * context cannot drift.
 */

import React, {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
} from 'react';
import { createPortal } from 'react-dom';
import type { PDFDocumentProxy } from 'pdfjs-dist';
import type { CardSourceMaterial } from '../../types/markBank';
import CropView from '../PaperTrail/CropView';
import { paperStoragePath, paperUrl } from '../PaperTrail/storage';
import { vaultPdf } from '../PaperTrail/vaultDocs';

interface SourceMaterialReaderProps {
  source: CardSourceMaterial;
  subjectId: string;
  year: number;
  paperFileid: string;
}

const withPdfExtension = (fileid: string) =>
  fileid.toLowerCase().endsWith('.pdf') ? fileid : `${fileid}.pdf`;

const clamp = (value: number, max: number) => Math.max(0, Math.min(max, value));

const PageStackIcon = () => (
  <svg width="25" height="25" viewBox="0 0 25 25" fill="none" aria-hidden="true">
    <rect x="6.25" y="3.25" width="13.5" height="17.5" rx="2.25" stroke="currentColor" strokeWidth="1.5" />
    <path d="M3.75 7.25v11.1a2.9 2.9 0 0 0 2.9 2.9H16" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
    <path d="M9.25 8h7.5M9.25 11.25h7.5M9.25 14.5h5" stroke="currentColor" strokeWidth="1.35" strokeLinecap="round" />
  </svg>
);

const ArrowIcon: React.FC<{ direction: 'left' | 'right' }> = ({ direction }) => (
  <svg width="17" height="17" viewBox="0 0 20 20" fill="none" aria-hidden="true">
    <path
      d={direction === 'left' ? 'M12.5 4.5 7 10l5.5 5.5' : 'M7.5 4.5 13 10l-5.5 5.5'}
      stroke="currentColor" strokeWidth="1.9" strokeLinecap="round" strokeLinejoin="round"
    />
  </svg>
);

const CloseIcon = () => (
  <svg width="18" height="18" viewBox="0 0 20 20" fill="none" aria-hidden="true">
    <path d="m5 5 10 10M15 5 5 15" stroke="currentColor" strokeWidth="1.9" strokeLinecap="round" />
  </svg>
);

const SourceMaterialReader: React.FC<SourceMaterialReaderProps> = ({
  source, subjectId, year, paperFileid,
}) => {
  const isIllustration = source.kind === 'source-illustration';
  const materialLabel = isIllustration ? 'illustration sheet' : 'source text';
  const [open, setOpen] = useState(false);
  const [pdf, setPdf] = useState<PDFDocumentProxy | null>(null);
  const [failed, setFailed] = useState(false);
  const [pageIndex, setPageIndex] = useState(0);
  const [zoom, setZoom] = useState(1);
  const triggerRef = useRef<HTMLButtonElement | null>(null);
  const closeRef = useRef<HTMLButtonElement | null>(null);
  const trackRef = useRef<HTMLDivElement | null>(null);
  const scrollFrame = useRef<number | null>(null);
  const swipeStart = useRef<{ x: number; y: number; pointerId: number } | null>(null);

  const url = useMemo(() => paperUrl(paperStoragePath(
    'lc', subjectId, year, 'paper', withPdfExtension(paperFileid),
  )), [paperFileid, subjectId, year]);
  const regions = useMemo(
    () => source.pages.map(page => [{ p: page }]),
    [source.pages],
  );
  const pageAriaLabel = useCallback(
    (page: number) => `${source.label}, printed examination page ${page}, shown as an image — © State Examinations Commission`,
    [source.label],
  );

  const close = useCallback(() => {
    setOpen(false);
    requestAnimationFrame(() => triggerRef.current?.focus());
  }, []);

  const show = useCallback(() => {
    setPageIndex(0);
    setZoom(1);
    setOpen(true);
  }, []);

  useEffect(() => {
    if (!open) return;
    let cancelled = false;
    setFailed(false);
    setPdf(null);
    vaultPdf(url)
      .then(document => { if (!cancelled) setPdf(document); })
      .catch(() => { if (!cancelled) setFailed(true); });
    return () => { cancelled = true; };
  }, [open, url]);

  useEffect(() => {
    if (!open) return;
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    requestAnimationFrame(() => closeRef.current?.focus());
    return () => {
      document.body.style.overflow = previousOverflow;
      if (scrollFrame.current !== null) cancelAnimationFrame(scrollFrame.current);
    };
  }, [open]);

  const goTo = useCallback((next: number) => {
    const index = clamp(next, source.pages.length - 1);
    setPageIndex(index);
    const slide = trackRef.current?.children[index] as HTMLElement | undefined;
    if (slide && typeof slide.scrollIntoView === 'function') {
      slide.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'start' });
    }
  }, [source.pages.length]);

  const trackScrolled = useCallback(() => {
    if (scrollFrame.current !== null) cancelAnimationFrame(scrollFrame.current);
    scrollFrame.current = requestAnimationFrame(() => {
      const track = trackRef.current;
      if (!track || track.clientWidth === 0) return;
      setPageIndex(clamp(Math.round(track.scrollLeft / track.clientWidth), source.pages.length - 1));
    });
  }, [source.pages.length]);

  const swipeStarted = useCallback((event: React.PointerEvent<HTMLDivElement>) => {
    if (zoom !== 1 || event.isPrimary === false) return;
    swipeStart.current = { x: event.clientX, y: event.clientY, pointerId: event.pointerId };
    try { event.currentTarget.setPointerCapture?.(event.pointerId); } catch { /* capture is an enhancement */ }
  }, [zoom]);

  const completeSwipe = useCallback((x: number, y: number, pointerId: number) => {
    const start = swipeStart.current;
    if (!start || start.pointerId !== pointerId || zoom !== 1) return;
    swipeStart.current = null;
    const dx = x - start.x;
    const dy = y - start.y;
    // Direction-aware so an ordinary vertical read never turns a page. The
    // distance is deliberately physical rather than a fraction of viewport:
    // 54px still feels intentional on a 390px phone but is not laborious on a
    // desktop trackpad or tablet.
    if (Math.abs(dx) < 54 || Math.abs(dx) < Math.abs(dy) * 1.15) return;
    goTo(pageIndex + (dx < 0 ? 1 : -1));
  }, [goTo, pageIndex, zoom]);

  const swipeFinished = useCallback((event: React.PointerEvent<HTMLDivElement>) => {
    completeSwipe(event.clientX, event.clientY, event.pointerId);
  }, [completeSwipe]);

  // CDP/device emulators may expose drag as mouse events without the matching
  // PointerEvent sequence. Real touch uses the pointer path above; this fallback
  // also makes a desktop click-and-drag feel like the same physical reader.
  const mouseSwipeStarted = useCallback((event: React.MouseEvent<HTMLDivElement>) => {
    if (zoom !== 1 || event.button !== 0) return;
    swipeStart.current = { x: event.clientX, y: event.clientY, pointerId: -1 };
  }, [zoom]);

  const mouseSwipeFinished = useCallback((event: React.MouseEvent<HTMLDivElement>) => {
    if (swipeStart.current?.pointerId !== -1) return;
    completeSwipe(event.clientX, event.clientY, -1);
  }, [completeSwipe]);

  // Keep an explicit touch path as well as Pointer Events. It matters inside
  // older WKWebView shells, where touch events are present but pointer capture
  // has historically been inconsistent during nested overflow scrolling.
  const touchSwipeStarted = useCallback((event: React.TouchEvent<HTMLDivElement>) => {
    if (zoom !== 1 || event.touches.length !== 1) return;
    const touch = event.touches[0];
    swipeStart.current = { x: touch.clientX, y: touch.clientY, pointerId: -2 };
  }, [zoom]);

  const touchSwipeFinished = useCallback((event: React.TouchEvent<HTMLDivElement>) => {
    const touch = event.changedTouches[0];
    if (!touch || swipeStart.current?.pointerId !== -2) return;
    completeSwipe(touch.clientX, touch.clientY, -2);
  }, [completeSwipe]);

  const trapDialogKeys = useCallback((event: React.KeyboardEvent<HTMLDivElement>) => {
    if (event.key === 'Escape') {
      event.preventDefault();
      event.stopPropagation();
      close();
      return;
    }
    if (event.key !== 'Tab') return;
    const controls = Array.from(event.currentTarget.querySelectorAll<HTMLElement>(
      'button:not([disabled]), a[href], [tabindex]:not([tabindex="-1"])',
    )).filter(control => !control.hasAttribute('hidden'));
    if (!controls.length) return;
    const first = controls[0];
    const last = controls[controls.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    } else if (!controls.includes(document.activeElement as HTMLElement)) {
      event.preventDefault();
      first.focus();
    }
  }, [close]);

  const modal = open && typeof document !== 'undefined' ? createPortal(
    <div className="mark-bank-theme mb-source-reader-overlay">
      <div
        className="mb-source-reader-dialog"
        role="dialog"
        aria-modal="true"
        aria-labelledby="mb-source-reader-title"
        onKeyDown={trapDialogKeys}
      >
        <header className="mb-source-reader-header">
          <div className="mb-source-reader-heading">
            <span>{source.label} · {materialLabel}</span>
            <h2 id="mb-source-reader-title">{source.title}</h2>
          </div>
          <div className="mb-source-reader-tools" aria-label="Page display controls">
            <button
              type="button"
              onClick={() => setZoom(value => Math.max(1, Number((value - 0.25).toFixed(2))))}
              disabled={zoom <= 1}
              aria-label="Zoom out"
              title="Zoom out"
            >
              <span aria-hidden="true">−</span>
            </button>
            <span aria-live="polite">{Math.round(zoom * 100)}%</span>
            <button
              type="button"
              onClick={() => setZoom(value => Math.min(2, Number((value + 0.25).toFixed(2))))}
              disabled={zoom >= 2}
              aria-label="Zoom in"
              title="Zoom in"
            >
              <span aria-hidden="true">+</span>
            </button>
          </div>
          <button ref={closeRef} type="button" className="mb-source-reader-close" onClick={close} aria-label={`Close ${materialLabel}`}>
            <CloseIcon />
          </button>
        </header>

        <div
          ref={trackRef}
          className="mb-source-reader-track"
          onScroll={trackScrolled}
          onPointerDown={swipeStarted}
          onPointerUp={swipeFinished}
          onPointerCancel={() => { swipeStart.current = null; }}
          onMouseDown={mouseSwipeStarted}
          onMouseUp={mouseSwipeFinished}
          onTouchStart={touchSwipeStarted}
          onTouchEnd={touchSwipeFinished}
          style={{ touchAction: zoom === 1 ? 'pan-y' : 'auto' }}
          aria-label={`${source.label} pages`}
        >
          {source.pages.map((page, index) => (
            <section
              key={page}
              className="mb-source-reader-slide"
              aria-label={`Source page ${index + 1} of ${source.pages.length}`}
            >
              <div className="mb-source-reader-page-meta">
                <span>Printed page {page}</span>
                <span>{index + 1} / {source.pages.length}</span>
              </div>
              <div className="mb-source-reader-page-pan">
                <div
                  className="mb-source-reader-paper"
                  style={{ width: `${zoom * 100}%` }}
                >
                  {pdf ? (
                    <CropView
                      key={`${page}-${zoom}`}
                      pdf={pdf}
                      region={regions[index]}
                      ariaLabel={pageAriaLabel}
                      failText="This printed page could not be rendered. Open the original paper below."
                    />
                  ) : failed ? (
                    <div className="mb-source-reader-failed">
                      <strong>That page did not load.</strong>
                      <span>You can retry or open the original examination document.</span>
                      <button type="button" onClick={() => { setFailed(false); setPdf(null); vaultPdf(url).then(setPdf).catch(() => setFailed(true)); }}>
                        Try again
                      </button>
                    </div>
                  ) : (
                    <div className="mb-source-reader-loading" aria-label="Loading source page">
                      <span />
                      <span />
                      <span />
                      <span />
                    </div>
                  )}
                </div>
              </div>
            </section>
          ))}
        </div>

        <footer className="mb-source-reader-footer">
          <div className="mb-source-reader-provenance">
            <strong>{source.attribution}</strong>
            <span>{source.presentationNote}</span>
            <a href={`${url}#page=${source.pages[pageIndex]}`} target="_blank" rel="noreferrer">
              Open the original {isIllustration ? 'illustration sheet' : 'paper'}
            </a>
          </div>
          <div className="mb-source-reader-navigation">
            <button
              type="button" onClick={() => goTo(pageIndex - 1)} disabled={pageIndex === 0}
              aria-label="Previous source page"
            >
              <ArrowIcon direction="left" />
            </button>
            <div className="mb-source-reader-dots" aria-label={`Page ${pageIndex + 1} of ${source.pages.length}`}>
              {source.pages.map((page, index) => (
                <button
                  key={page}
                  type="button"
                  onClick={() => goTo(index)}
                  aria-label={`Go to source page ${index + 1}`}
                  aria-current={index === pageIndex ? 'page' : undefined}
                />
              ))}
            </div>
            <button
              type="button" onClick={() => goTo(pageIndex + 1)} disabled={pageIndex === source.pages.length - 1}
              aria-label="Next source page"
            >
              <ArrowIcon direction="right" />
            </button>
          </div>
        </footer>
      </div>
    </div>,
    document.body,
  ) : null;

  return (
    <>
      <button type="button" ref={triggerRef} className="mb-source-material-trigger" onClick={show}>
        <span className="mb-source-material-icon"><PageStackIcon /></span>
        <span className="mb-source-material-copy">
          <span>Read {source.label}</span>
          <strong>{source.title}</strong>
          <small>
            {source.pages.length} printed {source.pages.length === 1 ? 'page' : 'pages'} · {isIllustration ? 'official examination imagery' : 'exact examination text'}
          </small>
        </span>
        <span className="mb-source-material-open" aria-hidden="true">
          <ArrowIcon direction="right" />
        </span>
      </button>
      {modal}
    </>
  );
};

export default SourceMaterialReader;
