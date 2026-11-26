import React, { useEffect, useRef, useState } from 'react';
import { TextButton } from '../ui/Button';

/** Resizing is local to the drawer: dragging does not rerender the island tree.
 *  The drawer is headed by its line ("A little more of your world.") with Smaller beside it
 *  (r5-b2.html, "Build"); its grab line resizes it. */
export default function BuildDrawer({ open, children, title }: { open: boolean; children: React.ReactNode; title?: React.ReactNode }) {
  const root = useRef<HTMLDivElement>(null);
  const drag = useRef<{ pointer: number; y: number; height: number } | null>(null);
  const [narrow, setNarrow] = useState(() => window.matchMedia('(max-width:700px)').matches);
  const [available, setAvailable] = useState(window.innerHeight);
  const [size, setSize] = useState<number | null>(null);
  const minimum = narrow ? 260 : 176;
  // On a phone it opens tall enough to show the shelf and the place button (r5-b2.html, "Build": about 450).
  const preferred = narrow ? 450 : 310;
  // On a phone the island keeps about 120px above the drawer (the agreed board); on a laptop 180.
  const maximum = Math.max(minimum, Math.min(preferred + 100, available - (narrow ? 120 : 180)));
  const height = Math.max(minimum, Math.min(maximum, size ?? preferred));
  const compact = height < preferred - 40;

  useEffect(() => {
    const media = window.matchMedia('(max-width:700px)');
    const change = () => { setNarrow(media.matches); setSize(null); };
    media.addEventListener('change', change);
    const parent = root.current?.parentElement;
    const observer = new ResizeObserver(() => { if (parent) setAvailable(parent.clientHeight); });
    if (parent) { setAvailable(parent.clientHeight); observer.observe(parent); }
    return () => { media.removeEventListener('change', change); observer.disconnect(); };
  }, []);
  const resize = (next: number) => setSize(Math.max(minimum, Math.min(maximum, next)));

  return <div ref={root} className={`coast-build-tray resizable-build-tray${compact ? ' is-compact' : ''}`}
    style={{ '--build-drawer-height': `${height}px` } as React.CSSProperties}
    inert={!open} aria-hidden={!open}>
    <div className="build-drawer-toolbar">
      <div className="build-drawer-grip" role="slider" tabIndex={open ? 0 : -1}
        aria-label="Build drawer height" aria-orientation="vertical"
        aria-valuemin={minimum} aria-valuemax={maximum} aria-valuenow={Math.round(height)}
        aria-valuetext={`${compact ? 'Compact' : 'Expanded'}, ${Math.round(height)} pixels. Drag down to shrink, or use the arrow keys.`}
        onPointerDown={event => {
          if (event.button !== 0) return;
          drag.current = { pointer: event.pointerId, y: event.clientY, height };
          root.current?.classList.add('is-resizing');
          event.currentTarget.setPointerCapture(event.pointerId);
        }}
        onPointerMove={event => {
          const start = drag.current;
          if (start && start.pointer === event.pointerId) resize(start.height + start.y - event.clientY);
        }}
        onLostPointerCapture={() => { drag.current = null; root.current?.classList.remove('is-resizing'); }}
        onPointerUp={event => {
          if (event.currentTarget.hasPointerCapture(event.pointerId)) event.currentTarget.releasePointerCapture(event.pointerId);
        }}
        onPointerCancel={() => { drag.current = null; root.current?.classList.remove('is-resizing'); }}
        onKeyDown={event => {
          const next = event.key === 'ArrowDown' ? height - 24 : event.key === 'ArrowUp' ? height + 24
            : event.key === 'Home' ? minimum : event.key === 'End' ? maximum : null;
          if (next !== null) { event.preventDefault(); resize(next); }
        }}>
        <span className="build-drawer-grab-line" aria-hidden="true" /><span className="sr-only">Drag to resize</span>
      </div>
      <div className="build-drawer-head">
        {title ? <h2 className="t-heading build-drawer-title">{title}</h2> : <span />}
        <TextButton tone="quiet" className="build-drawer-toggle" aria-label={compact ? 'Expand build drawer' : 'Make build drawer smaller'}
          onClick={() => resize(compact ? preferred : minimum)}>
          {compact ? 'Expand' : 'Smaller'}
        </TextButton>
      </div>
    </div>
    {children}
  </div>;
}
