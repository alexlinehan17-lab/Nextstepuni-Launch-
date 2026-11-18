import React, { useRef, useState } from "react";
import type { InkStroke } from "./answerDeskStore";
export type InkTool = "pen" | "highlight" | "erase" | "move";
export interface AnswerInkProps {
  strokes: InkStroke[];
  base?: InkStroke[];
  tool: InkTool;
  enabled: boolean;
  correction?: boolean;
  onChange: (strokes: InkStroke[]) => void;
}
export default function AnswerInk({
  strokes,
  base = [],
  tool,
  enabled,
  correction,
  onChange,
  aspect = 1.414,
}: AnswerInkProps & { aspect?: number }) {
  const active = useRef<InkStroke | null>(null);
  const [line, setLine] = useState<InkStroke | null>(null);
  const point = (e: React.PointerEvent<SVGSVGElement>): [number, number] => {
    const r = e.currentTarget.getBoundingClientRect();
    return [
      Math.max(
        0,
        Math.min(
          1,
          Math.round(((e.clientX - r.left) / r.width) * 10000) / 10000,
        ),
      ),
      Math.max(
        0,
        Math.min(
          1,
          Math.round(((e.clientY - r.top) / r.height) * 10000) / 10000,
        ),
      ),
    ];
  };
  const erase = (p: [number, number]) => {
    const kept = strokes.filter(
      (s) =>
        !s.points.some(
          (a) => Math.hypot(a[0] - p[0], (a[1] - p[1]) * aspect) < 0.018,
        ),
    );
    // Empty-space movement must not fill undo history with identical copies.
    if (kept.length !== strokes.length) onChange(kept);
  };
  const down = (e: React.PointerEvent<SVGSVGElement>) => {
    if (!enabled || tool === "move" || e.button !== 0) return;
    e.currentTarget.setPointerCapture(e.pointerId);
    const p = point(e);
    if (tool === "erase") {
      erase(p);
      return;
    }
    const s: InkStroke = {
      points: [p, p],
      kind: tool,
      colour:
        tool === "highlight" ? "#dfb14d" : correction ? "#ad4e23" : "#162d4d",
    };
    active.current = s;
    setLine(s);
  };
  const move = (e: React.PointerEvent<SVGSVGElement>) => {
    if (!enabled || !e.currentTarget.hasPointerCapture(e.pointerId)) return;
    const p = point(e);
    if (tool === "erase") {
      erase(p);
      return;
    }
    const s = active.current;
    if (!s) return;
    const last = s.points.at(-1)!;
    if (Math.hypot(last[0] - p[0], last[1] - p[1]) < 0.001) return;
    const next = { ...s, points: [...s.points, p] };
    active.current = next;
    setLine(next);
  };
  const end = () => {
    if (active.current) onChange([...strokes, active.current]);
    active.current = null;
    setLine(null);
  };
  const paths = (list: InkStroke[], prefix: string) =>
    list.map((s, i) => (
      <polyline
        key={`${prefix}${i}`}
        points={s.points
          .map(([x, y]) => `${x * 1000},${y * 1000 * aspect}`)
          .join(" ")}
        fill="none"
        stroke={s.colour}
        strokeWidth={s.kind === "highlight" ? 20 : 3}
        opacity={s.kind === "highlight" ? 0.25 : 1}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    ));
  return (
    <svg
      className="ad-ink"
      aria-label="Handwritten working on this page"
      role="img"
      aria-hidden={
        !enabled && !strokes.length && !base.length ? true : undefined
      }
      viewBox={`0 0 1000 ${1000 * aspect}`}
      style={{
        pointerEvents: enabled && tool !== "move" ? "auto" : "none",
        touchAction: enabled && tool !== "move" ? "none" : "auto",
        cursor: tool === "erase" ? "cell" : "crosshair",
      }}
      onPointerDown={down}
      onPointerMove={move}
      onPointerUp={end}
      onPointerCancel={end}
    >
      {paths(base, "base")}
      {paths(strokes, "work")}
      {line && paths([line], "active")}
    </svg>
  );
}
