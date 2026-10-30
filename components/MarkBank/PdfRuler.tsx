import React, { useEffect, useState } from 'react';
import type { PDFDocumentProxy } from 'pdfjs-dist';

type Point = { x: number; y: number };

/** PDF coordinates are physical points (1/72 inch), independent of screen zoom. */
export function printedCentimetres(a: Point, b: Point, width: number, height: number): number {
  return Math.hypot((b.x - a.x) * width, (b.y - a.y) * height) * 2.54 / 72;
}

const PdfRuler: React.FC<{
  pdf: PDFDocumentProxy;
  page: number;
  onMeasure: (centimetres: number | null) => void;
}> = ({ pdf, page, onMeasure }) => {
  const [size, setSize] = useState<{ width: number; height: number }>();
  const [points, setPoints] = useState<Point[]>([]);
  const [cursor, setCursor] = useState<Point>({ x: .5, y: .5 });
  useEffect(() => {
    let cancelled = false;
    pdf.getPage(page).then(p => {
      const viewport = p.getViewport({ scale: 1 });
      if (!cancelled) setSize({ width: viewport.width, height: viewport.height });
    }).catch(() => {});
    return () => { cancelled = true; };
  }, [pdf, page]);

  const place = (point: Point) => {
    const next = points.length === 1 ? [points[0], point] : [point];
    setPoints(next);
    setCursor(point);
    onMeasure(next.length === 2 && size
      ? printedCentimetres(next[0], next[1], size.width, size.height) : null);
  };
  if (!size) return null;
  const coordinates = (p: Point) => ({ x: p.x * size.width, y: p.y * size.height });
  const a = points[0] && coordinates(points[0]);
  const b = points[1] && coordinates(points[1]);
  const crosshair = coordinates(cursor);
  return (
    <button type="button" className="mb-pdf-ruler"
      aria-label="Printed-page ruler. Select two endpoints. Arrow keys move the crosshair; Enter selects an endpoint. Hold Shift for larger steps."
      onPointerDown={event => event.stopPropagation()}
      onClick={event => {
        event.stopPropagation();
        if (!event.detail) { place(cursor); return; }
        const rect = event.currentTarget.getBoundingClientRect();
        place({ x: (event.clientX - rect.left) / rect.width, y: (event.clientY - rect.top) / rect.height });
      }}
      onKeyDown={event => {
        const directions: Record<string, [number, number]> = {
          ArrowLeft: [-1, 0], ArrowRight: [1, 0], ArrowUp: [0, -1], ArrowDown: [0, 1],
        };
        const direction = directions[event.key];
        if (!direction) return;
        event.preventDefault();
        event.stopPropagation();
        const step = event.shiftKey ? 10 : 1;
        setCursor(old => ({
          x: Math.max(0, Math.min(1, old.x + direction[0] * step / size.width)),
          y: Math.max(0, Math.min(1, old.y + direction[1] * step / size.height)),
        }));
      }}>
      <svg viewBox={`0 0 ${size.width} ${size.height}`} preserveAspectRatio="none" aria-hidden="true">
        {a && b && <line x1={a.x} y1={a.y} x2={b.x} y2={b.y} stroke="#F26B1F" strokeWidth="2" />}
        {[a, b].filter((p): p is Point => Boolean(p)).map((p, index) => (
          <circle key={index} cx={p.x} cy={p.y} r="4" fill="#F26B1F" stroke="#1A1A1A" strokeWidth="1" />
        ))}
        <path d={`M${crosshair.x - 6},${crosshair.y}h12 M${crosshair.x},${crosshair.y - 6}v12`}
          fill="none" stroke="#A8430E" strokeWidth="1.5" />
      </svg>
    </button>
  );
};

export default PdfRuler;
