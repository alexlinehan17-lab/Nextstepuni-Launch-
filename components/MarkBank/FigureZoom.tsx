/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Mark Bank — a figure that opens full screen.
 *
 * A question figure or a scheme's worked solution is a crop of the printed
 * page, capped to the card's column. On a 390 px phone a wide crop sets its
 * text at 7.5-10 px (the Economics data tables are the worst of it), which
 * nobody can read. The crop stays exactly as it was in the card, with a
 * visible "Enlarge" control beside its attribution; tapping either the crop
 * or the control opens it full screen, where it can be zoomed and moved:
 * pinch on a touch screen, ctrl-scroll or a trackpad pinch on a desktop, the
 * − and + buttons, or the keyboard (+, −, 0 to fit, arrows to move, Esc to
 * close). Focus returns to the control on close.
 *
 * The pattern follows the source-material reader: a portal over the session,
 * a counted body-scroll lock, zoom as a width rather than a CSS transform (so
 * the stage scrolls natively and nothing is re-rasterised), and Escape caught
 * before the session dialog can see it.
 */

import React, { useCallback, useEffect, useLayoutEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { lockBodyScroll } from '../../utils/bodyScrollLock';
import './figure-zoom.css';

const ZOOM_STEP = 1.5;
/** How far a fitted figure may be scaled up to fit the screen before zooming. */
const FIT_MAX = 2;
/** The canvas padding around the figure; matches .mb-figzoom-canvas in figure-zoom.css. */
const CANVAS_PAD = 16;

const clamp = (value: number, lo: number, hi: number) => Math.min(hi, Math.max(lo, value));

/** A magnifier, not the corner arrows the session's own "Expand" carries. */
const EnlargeIcon = () => (
  <svg width="15" height="15" viewBox="0 0 20 20" fill="none" aria-hidden="true">
    <circle cx="8.5" cy="8.5" r="5.25" stroke="currentColor" strokeWidth="1.8" />
    <path d="M12.5 12.5 16.5 16.5M8.5 6.25v4.5M6.25 8.5h4.5" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
  </svg>
);

const CloseIcon = () => (
  <svg width="18" height="18" viewBox="0 0 20 20" fill="none" aria-hidden="true">
    <path d="m5 5 10 10M15 5 5 15" stroke="currentColor" strokeWidth="1.9" strokeLinecap="round" />
  </svg>
);

/** The figure point (u, v as fractions) to keep under the stage point (x, y). */
interface Anchor { u: number; v: number; x: number; y: number }

const FigureViewer: React.FC<{
  src: string;
  alt: string;
  kicker: string;
  caption: string;
  onClose: () => void;
}> = ({ src, alt, kicker, caption, onClose }) => {
  const [natural, setNatural] = useState<{ w: number; h: number } | null>(null);
  const [fit, setFit] = useState<{ w: number; h: number } | null>(null);
  const [zoom, setZoom] = useState(1);
  const [failed, setFailed] = useState(false);
  const stageRef = useRef<HTMLDivElement | null>(null);
  const imgRef = useRef<HTMLImageElement | null>(null);
  const closeRef = useRef<HTMLButtonElement | null>(null);
  const dialogRef = useRef<HTMLDivElement | null>(null);
  const anchor = useRef<Anchor | null>(null);
  const pinch = useRef<{ d: number; zoom: number } | null>(null);
  const drag = useRef<{ x: number; y: number; left: number; top: number } | null>(null);
  const onCloseRef = useRef(onClose);
  onCloseRef.current = onClose;
  const zoomRef = useRef(zoom);
  zoomRef.current = zoom;

  const maxZoom = natural && fit ? clamp((natural.w * 3) / fit.w, 2, 6) : 4;

  /** The size at which the whole figure fits the stage: zoom 1. */
  const measure = useCallback(() => {
    const stage = stageRef.current;
    if (!stage || !natural) return;
    const pad = CANVAS_PAD * 2;
    const scale = Math.min((stage.clientWidth - pad) / natural.w, (stage.clientHeight - pad) / natural.h, FIT_MAX);
    setFit({ w: Math.max(1, Math.round(natural.w * scale)), h: Math.max(1, Math.round(natural.h * scale)) });
  }, [natural]);

  useLayoutEffect(() => { measure(); }, [measure]);
  useEffect(() => {
    window.addEventListener('resize', measure);
    return () => window.removeEventListener('resize', measure);
  }, [measure]);

  /** Zoom to `next`, keeping the figure point under (x, y) where it is; the stage centre by default. */
  const zoomTo = useCallback((next: number, at?: { x: number; y: number }) => {
    const stage = stageRef.current;
    const img = imgRef.current;
    if (stage && img) {
      const box = img.getBoundingClientRect();
      const frame = stage.getBoundingClientRect();
      const x = at?.x ?? frame.left + frame.width / 2;
      const y = at?.y ?? frame.top + frame.height / 2;
      anchor.current = {
        u: box.width ? clamp((x - box.left) / box.width, 0, 1) : 0.5,
        v: box.height ? clamp((y - box.top) / box.height, 0, 1) : 0.5,
        x: x - frame.left, y: y - frame.top,
      };
    }
    setZoom(clamp(next, 1, maxZoom));
  }, [maxZoom]);
  // The listeners below are attached once; they always reach the latest zoomTo.
  const zoomToRef = useRef(zoomTo);
  zoomToRef.current = zoomTo;

  // After a zoom has laid out, scroll so the anchored point is back under the pointer.
  useLayoutEffect(() => {
    const stage = stageRef.current;
    const img = imgRef.current;
    const a = anchor.current;
    anchor.current = null;
    if (!stage || !img || !a) return;
    if (!fit) return;
    // Computed from the sizes this render set rather than measured, so a
    // stray width transition can never leave the view at the old scroll.
    const width = fit.w * zoom;
    const height = fit.h * zoom;
    const left = Math.max(CANVAS_PAD, (stage.clientWidth - width) / 2);
    const top = Math.max(CANVAS_PAD, (stage.clientHeight - height) / 2);
    stage.scrollLeft = left + a.u * width - a.x;
    stage.scrollTop = top + a.v * height - a.y;
  }, [zoom, fit]);

  // Keys are caught on the window in the capture phase, before the session's
  // own dialog can treat Escape as "leave the review".
  useEffect(() => {
    const release = lockBodyScroll();
    const onKey = (event: KeyboardEvent) => {
      const stage = stageRef.current;
      const zoomTo = zoomToRef.current;
      if (event.key === 'Escape') onCloseRef.current();
      else if (event.key === '+' || event.key === '=') zoomTo(zoomRef.current * ZOOM_STEP);
      else if (event.key === '-' || event.key === '_') zoomTo(zoomRef.current / ZOOM_STEP);
      else if (event.key === '0') zoomTo(1);
      else if (stage && event.key.startsWith('Arrow')) {
        const step = event.shiftKey ? 240 : 60;
        stage.scrollBy({
          left: event.key === 'ArrowLeft' ? -step : event.key === 'ArrowRight' ? step : 0,
          top: event.key === 'ArrowUp' ? -step : event.key === 'ArrowDown' ? step : 0,
        });
      } else if (event.key === 'Tab' && dialogRef.current) {
        const controls = Array.from(dialogRef.current.querySelectorAll<HTMLElement>('button:not([disabled]), [tabindex="0"]'));
        if (!controls.length) return;
        const first = controls[0];
        const last = controls[controls.length - 1];
        const inside = controls.includes(document.activeElement as HTMLElement);
        if (event.shiftKey && (document.activeElement === first || !inside)) { last.focus(); }
        else if (!event.shiftKey && (document.activeElement === last || !inside)) { first.focus(); }
        else return;
      } else return;
      event.preventDefault();
      event.stopPropagation();
    };
    window.addEventListener('keydown', onKey, true);
    requestAnimationFrame(() => closeRef.current?.focus());
    return () => {
      window.removeEventListener('keydown', onKey, true);
      release();
    };
  }, []);

  // Pinch and ctrl-wheel need listeners that may cancel the browser's own page zoom.
  useEffect(() => {
    const stage = stageRef.current;
    if (!stage) return;
    const distance = (t: TouchList) => Math.hypot(t[0].clientX - t[1].clientX, t[0].clientY - t[1].clientY);
    const onTouchStart = (event: TouchEvent) => {
      if (event.touches.length === 2) pinch.current = { d: distance(event.touches), zoom: zoomRef.current };
    };
    const onTouchMove = (event: TouchEvent) => {
      if (event.touches.length !== 2 || !pinch.current) return;
      event.preventDefault();
      const t = event.touches;
      zoomToRef.current(pinch.current.zoom * (distance(t) / pinch.current.d), {
        x: (t[0].clientX + t[1].clientX) / 2, y: (t[0].clientY + t[1].clientY) / 2,
      });
    };
    const onTouchEnd = (event: TouchEvent) => { if (event.touches.length < 2) pinch.current = null; };
    const onWheel = (event: WheelEvent) => {
      if (!event.ctrlKey) return;
      event.preventDefault();
      zoomToRef.current(zoomRef.current * Math.exp(-event.deltaY * 0.01), { x: event.clientX, y: event.clientY });
    };
    // Safari's own pinch gesture would zoom the page under the viewer.
    const stopGesture = (event: Event) => event.preventDefault();
    stage.addEventListener('touchstart', onTouchStart, { passive: true });
    stage.addEventListener('touchmove', onTouchMove, { passive: false });
    stage.addEventListener('touchend', onTouchEnd, { passive: true });
    stage.addEventListener('touchcancel', onTouchEnd, { passive: true });
    stage.addEventListener('wheel', onWheel, { passive: false });
    stage.addEventListener('gesturestart', stopGesture);
    stage.addEventListener('gesturechange', stopGesture);
    return () => {
      stage.removeEventListener('touchstart', onTouchStart);
      stage.removeEventListener('touchmove', onTouchMove);
      stage.removeEventListener('touchend', onTouchEnd);
      stage.removeEventListener('touchcancel', onTouchEnd);
      stage.removeEventListener('wheel', onWheel);
      stage.removeEventListener('gesturestart', stopGesture);
      stage.removeEventListener('gesturechange', stopGesture);
    };
  }, []);

  // Drag to move with a mouse; touch moves the stage natively.
  const startDrag = (event: React.MouseEvent) => {
    const stage = stageRef.current;
    if (event.button !== 0 || !stage) return;
    drag.current = { x: event.clientX, y: event.clientY, left: stage.scrollLeft, top: stage.scrollTop };
    const move = (e: MouseEvent) => {
      if (!drag.current) return;
      stage.scrollLeft = drag.current.left - (e.clientX - drag.current.x);
      stage.scrollTop = drag.current.top - (e.clientY - drag.current.y);
    };
    const up = () => {
      drag.current = null;
      window.removeEventListener('mousemove', move);
      window.removeEventListener('mouseup', up);
    };
    window.addEventListener('mousemove', move);
    window.addEventListener('mouseup', up);
  };

  const size = fit ? { width: Math.round(fit.w * zoom), height: Math.round(fit.h * zoom) } : undefined;

  return createPortal(
    <div className="mark-bank-theme mb-figzoom-overlay">
      <div ref={dialogRef} className="mb-figzoom-dialog" role="dialog" aria-modal="true" aria-label={`${kicker}, enlarged`}>
        <header className="mb-figzoom-header">
          <div className="mb-figzoom-heading">
            <span>{kicker}</span>
            <p>{caption}</p>
          </div>
          <div className="mb-figzoom-tools" role="group" aria-label="Zoom">
            <button type="button" onClick={() => zoomTo(zoom / ZOOM_STEP)} disabled={zoom <= 1} aria-label="Zoom out" title="Zoom out (−)">
              <span aria-hidden="true">−</span>
            </button>
            <button type="button" className="mb-figzoom-level" onClick={() => zoomTo(1)} disabled={zoom === 1}
              aria-label={`Zoomed to ${Math.round(zoom * 100)}%. Fit to screen`} title="Fit to screen (0)">
              {Math.round(zoom * 100)}%
            </button>
            <button type="button" onClick={() => zoomTo(zoom * ZOOM_STEP)} disabled={zoom >= maxZoom} aria-label="Zoom in" title="Zoom in (+)">
              <span aria-hidden="true">+</span>
            </button>
          </div>
          <button ref={closeRef} type="button" className="mb-figzoom-close" onClick={() => onCloseRef.current()} aria-label="Close enlarged figure" title="Close (Esc)">
            <CloseIcon />
          </button>
        </header>
        <div
          ref={stageRef}
          className="mb-figzoom-stage"
          data-zoomed={zoom > 1}
          tabIndex={0}
          aria-label={`${alt}. Use the arrow keys to move around the figure.`}
          onMouseDown={startDrag}
          onDoubleClick={event => zoomTo(zoom > 1 ? 1 : Math.min(2.5, maxZoom), { x: event.clientX, y: event.clientY })}
        >
          <div className="mb-figzoom-canvas">
            {failed ? (
              <p className="mb-figzoom-failed">This figure did not load. Close the viewer and try again.</p>
            ) : (
              <img
                ref={imgRef}
                src={src}
                alt={alt}
                draggable={false}
                onLoad={event => setNatural({ w: event.currentTarget.naturalWidth, h: event.currentTarget.naturalHeight })}
                onError={() => setFailed(true)}
                style={size ?? { visibility: 'hidden' }}
              />
            )}
          </div>
        </div>
        <footer className="mb-figzoom-footer">
          <span className="mb-figzoom-hint-touch">Pinch to zoom; drag to move around.</span>
          <span className="mb-figzoom-hint-pointer">Scroll or drag to move · + and − zoom · 0 fits · Esc closes</span>
        </footer>
      </div>
    </div>,
    document.body,
  );
};

/**
 * The figure in the card, unchanged, with a visibly clickable "Enlarge"
 * control in its caption row. Renders the figure's img and its figcaption, so
 * it sits directly inside the caller's <figure>.
 */
const FigureZoom: React.FC<{
  src: string;
  alt: string;
  /** The img's own style in the card, kept exactly as it was. */
  imgStyle: React.CSSProperties;
  /** Wraps the img in the card (the solution crop is centred in a div). */
  imgWrapStyle?: React.CSSProperties;
  /** What the viewer's heading calls the figure: "Printed question", "Marking scheme". */
  kicker: string;
  /** The figure's attribution, shown in the card and in the viewer. */
  caption: string;
  captionStyle: React.CSSProperties;
}> = ({ src, alt, imgStyle, imgWrapStyle, kicker, caption, captionStyle }) => {
  const [open, setOpen] = useState(false);
  const triggerRef = useRef<HTMLButtonElement | null>(null);
  const close = useCallback(() => {
    setOpen(false);
    requestAnimationFrame(() => triggerRef.current?.focus());
  }, []);
  const img = (
    <img src={src} alt={alt} style={{ ...imgStyle, cursor: 'zoom-in' }} onClick={() => setOpen(true)} />
  );
  return (
    <>
      {imgWrapStyle ? <div style={imgWrapStyle}>{img}</div> : img}
      <figcaption className="mb-figzoom-bar" style={captionStyle}>
        <span>{caption}</span>
        <button ref={triggerRef} type="button" className="mb-figzoom-open" onClick={() => setOpen(true)} aria-label={`Enlarge: ${kicker}`}>
          <EnlargeIcon />Enlarge
        </button>
      </figcaption>
      {open && <FigureViewer src={src} alt={alt} kicker={kicker} caption={caption} onClose={close} />}
    </>
  );
};

export default FigureZoom;
