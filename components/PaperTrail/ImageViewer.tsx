/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — image-supplement lightbox.
 *
 * The SEC ships a small family of exam documents as images rather than PDFs
 * (the Geography aerial photograph and Ordnance Survey map sheets, and their
 * JC / LCA cousins). Forcing them through the pdf.js viewer would fail, so
 * they get a dedicated lightbox: the sheet is mounted like a photographic
 * print on the viewer's zinc ground, fit to width at rest, with the same zoom
 * ladder as the document viewer and free two-axis panning via natural scroll.
 */

import React, { useCallback, useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { Minus, Plus, SlidersHorizontal } from 'lucide-react';
import { Button, IconButton } from '../ui/Button';
import { TopBar } from '../ui/Bars';
import { List, Row } from '../ui/List';
import { MenuAction, MenuPanel } from '../ui/Menu';
import { Sheet } from '../ui/Sheet';
import './viewer-chrome.css';

const ZOOM_STEPS = [0.75, 1, 1.25, 1.5, 2, 2.5];

const ImageViewer: React.FC<{
  title: string;
  subtitle?: string;
  /** The bar's name and the small line over it; default the title and subtitle. */
  barName?: string;
  barOver?: string;
  url: string;
  onClose: () => void;
}> = ({ title, subtitle, barName, barOver, url, onClose }) => {
  const [zoom, setZoom] = useState(1);
  const [state, setState] = useState<'loading' | 'ready' | 'error'>('loading');
  const [retryTick, setRetryTick] = useState(0);
  const headerRef = useRef<HTMLDivElement | null>(null);
  const scrollRef = useRef<HTMLDivElement | null>(null);
  const onCloseRef = useRef(onClose);
  onCloseRef.current = onClose;
  // The same bar as the paper viewer: Close, the name and Tools; zoom and the
  // original move into Tools on a phone, zoom stays in the bar on a laptop.
  const [toolsOpen, setToolsOpen] = useState(false);
  const toolsOpenRef = useRef(false);
  toolsOpenRef.current = toolsOpen;
  const [isWide, setIsWide] = useState(() => typeof window !== 'undefined' && window.matchMedia('(min-width: 768px)').matches);
  useEffect(() => {
    const mq = window.matchMedia('(min-width: 768px)');
    const on = () => setIsWide(mq.matches);
    mq.addEventListener('change', on);
    return () => mq.removeEventListener('change', on);
  }, []);

  useEffect(() => {
    headerRef.current?.focus();
  }, []);

  const zoomBy = useCallback((dir: number) => {
    setZoom(z => {
      const i = ZOOM_STEPS.indexOf(z);
      return ZOOM_STEPS[Math.min(ZOOM_STEPS.length - 1, Math.max(0, i + dir))];
    });
  }, []);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') { if (toolsOpenRef.current) setToolsOpen(false); else onCloseRef.current(); }
      else if (e.key === '+' || e.key === '=') zoomBy(1);
      else if (e.key === '-') zoomBy(-1);
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [zoomBy]);

  // Double-tap / double-click: jump between rest and a close look, centred on
  // nothing fancier than the scroll position the reader already chose.
  const onDoubleClick = () => setZoom(z => (z === 1 ? 2 : 1));

  const zoomControl = (
    <span className="pv-zoom" role="group" aria-label="Zoom">
      <IconButton label="Zoom out" aria-disabled={zoom === ZOOM_STEPS[0] || undefined} onClick={() => zoomBy(-1)}
        icon={<Minus className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" focusable="false" />} />
      <span className="ui-readout pv-zoom-value">{Math.round(zoom * 100)}%</span>
      <IconButton label="Zoom in" aria-disabled={zoom === ZOOM_STEPS[ZOOM_STEPS.length - 1] || undefined} onClick={() => zoomBy(1)}
        icon={<Plus className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" focusable="false" />} />
    </span>
  );
  const download = { title: 'Download the image', meta: 'Opens in your browser · Image', href: url };
  const tools = isWide ? (
    <div className="pv-actions">
      <span />
      {zoomControl}
      <MenuPanel label="Tools" buttonLabel="Tools for this image" className="pv-tools-btn" open={toolsOpen} onOpenChange={setToolsOpen} head="Tools"
        face={<><SlidersHorizontal className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" focusable="false" />Tools</>}>
        <MenuAction title={download.title} meta={download.meta} href={download.href} />
      </MenuPanel>
    </div>
  ) : (
    <IconButton label="Tools for this image" onClick={() => setToolsOpen(true)}
      icon={<SlidersHorizontal className="ui-icon" width={24} height={24} strokeWidth={1.75} aria-hidden="true" focusable="false" />} />
  );

  return createPortal(
    <div
      className="pv-root fixed inset-0 z-[100] flex flex-col"
      role="dialog"
      aria-modal="true"
      aria-label={`${title} — image viewer`}
    >
      {/* The paper viewer's bar: Close, the paper's name and Tools. */}
      <div ref={headerRef} tabIndex={-1} className="pv-top">
        <TopBar ruled className="pv-bar" leave={{ kind: 'close', onPress: () => onCloseRef.current(), label: 'Close viewer' }}
          over={barOver ?? subtitle} title={barName ?? title} action={tools} />
      </div>
      <Sheet open={toolsOpen && !isWide} onClose={() => setToolsOpen(false)} title="Tools" titleAlign="start">
        <div className="pv-tools">
          <List label="This image">
            <Row title="Zoom" trailing={zoomControl} />
            <Row external href={download.href} title={download.title} meta={download.meta} />
          </List>
        </div>
      </Sheet>

      {/* Sheet */}
      <div ref={scrollRef} className="flex-1 overflow-auto overscroll-contain">
        <div className="min-h-full flex items-start justify-center p-4 sm:p-6">
          {state === 'error' ? (
            <div className="self-center text-center max-w-sm px-6 py-10">
              <p className="pv-state-title">
                The image didn’t load
              </p>
              <p className="mt-1 t-sub">
                Check your connection, then try again — or open the original in
                your browser.
              </p>
              <div className="mt-4 pv-state-actions">
                <Button kind="main" onClick={() => { setState('loading'); setRetryTick(t => t + 1); }}>Try again</Button>
                <a href={url} target="_blank" rel="noopener noreferrer" className="ui-part ui-btn"><span>Open in browser</span></a>
              </div>
            </div>
          ) : (
            <div
              className="transition-[width] duration-150 ease-out"
              style={{ width: `${zoom * 100}%`, maxWidth: zoom === 1 ? 900 : undefined }}
            >
              {state === 'loading' && (
                <div
                  aria-hidden
                  className="w-full aspect-[4/3] rounded-xl bg-zinc-200 dark:bg-zinc-800/70 animate-pulse"
                />
              )}
              <img
                key={retryTick}
                src={url}
                alt={subtitle ? `${title} — ${subtitle}` : title}
                onLoad={() => setState('ready')}
                onError={() => setState('error')}
                onDoubleClick={onDoubleClick}
                draggable={false}
                className={`w-full h-auto rounded-xl shadow-lg ring-1 ring-black/10 dark:ring-white/10 bg-white select-none ${
                  state === 'ready' ? '' : 'hidden'
                }`}
              />
            </div>
          )}
        </div>
        <p className="pv-copyright">
          Examination material © State Examinations Commission
        </p>
      </div>
    </div>,
    document.body,
  );
};

export default ImageViewer;
