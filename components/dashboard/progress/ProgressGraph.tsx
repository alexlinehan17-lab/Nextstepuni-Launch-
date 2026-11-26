/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Time over a period on My Progress (components.md, "Data"; c-progress.js,
 * "the graph"): a smooth line with a flat fill, the steady band, today's value
 * as the one orange mark, read by touch and slide along the graph itself
 * ("This is the best way forward yep", 25 Nov 2026; "never bars again" for
 * time over a period). It draws the buckets it is given; it works nothing out.
 */
import { useEffect, useId, useRef, useState, type KeyboardEvent, type PointerEvent as ReactPointerEvent } from 'react';
import type { ActivityBucket } from '../dashboardAnalytics';

export type GraphMetric = 'minutes' | 'sessions';

/** "2h 58m", "45m", "0m". */
export function formatMinutes(minutes: number): string {
  const hours = Math.floor(minutes / 60);
  const rest = minutes % 60;
  return hours ? `${hours}h${rest ? ` ${rest}m` : ''}` : `${rest}m`;
}

const plural = (count: number, word: string) => `${count} ${word}${count === 1 ? '' : 's'}`;

/** A curve that never dips below its points (monotone), so an empty day reads as zero. */
function smooth(points: Array<[number, number]>): string {
  const n = points.length;
  if (n < 2) return '';
  const slope: number[] = [];
  const tangent: number[] = [];
  for (let i = 0; i < n - 1; i += 1) slope[i] = (points[i + 1][1] - points[i][1]) / (points[i + 1][0] - points[i][0]);
  tangent[0] = slope[0];
  tangent[n - 1] = slope[n - 2];
  for (let i = 1; i < n - 1; i += 1) tangent[i] = slope[i - 1] * slope[i] <= 0 ? 0 : 2 / (1 / slope[i - 1] + 1 / slope[i]);
  let d = `M${points[0][0].toFixed(1)} ${points[0][1].toFixed(1)}`;
  for (let i = 0; i < n - 1; i += 1) {
    const h = (points[i + 1][0] - points[i][0]) / 3;
    d += ` C${(points[i][0] + h).toFixed(1)} ${(points[i][1] + tangent[i] * h).toFixed(1)} ${(points[i + 1][0] - h).toFixed(1)} ${(points[i + 1][1] - tangent[i + 1] * h).toFixed(1)} ${points[i + 1][0].toFixed(1)} ${points[i + 1][1].toFixed(1)}`;
  }
  return d;
}

/** The tick under each slot: day names for a week, every seventh day for a month, initials for a year. */
function tickFor(bucket: ActivityBucket, index: number, count: number): string | null {
  if (count === 12) return bucket.label.charAt(0);
  if (count <= 7) return bucket.label;
  return index % 7 === 0 ? bucket.label : null;
}

export function ProgressGraph({ buckets, metric, height = 168, average = false, className = '' }: {
  buckets: ActivityBucket[];
  metric: GraphMetric;
  /** A dashed line at the period's average over the days or months so far (not a target). */
  average?: boolean;
  /** 168 on a phone; taller on a laptop. */
  height?: number;
  className?: string;
}) {
  const box = useRef<HTMLDivElement>(null);
  const [width, setWidth] = useState(342);
  const [pick, setPick] = useState<number | null>(null);
  const noteId = useId();
  useEffect(() => {
    const node = box.current;
    if (!node) return undefined;
    const measure = () => { const next = Math.round(node.getBoundingClientRect().width); if (next > 0) setWidth(next); };
    measure();
    const observer = typeof ResizeObserver !== 'undefined' ? new ResizeObserver(measure) : null;
    observer?.observe(node);
    return () => observer?.disconnect();
  }, []);
  // A new period or measure starts unread.
  useEffect(() => { setPick(null); }, [buckets, metric]);

  const now = Date.now();
  const elapsed = Math.max(1, buckets.filter(bucket => bucket.start <= now).length);
  const series = buckets.slice(0, elapsed).map(bucket => bucket[metric]);
  const last = series.length - 1;
  const max = Math.max(0, ...series);
  const steps = metric === 'sessions' ? [1, 2, 5, 10, 20, 50, 100] : [60, 120, 180, 360, 720, 1440, 2880];
  const step = steps.find(candidate => Math.ceil(max / candidate) <= 4) ?? steps[steps.length - 1];
  const top = Math.max(step * 2, Math.ceil(max / step) * step);
  const L = 36; const R = width - 14; const T = 14; const B = height - 34;
  const slots = Math.max(2, buckets.length);
  const x = (i: number) => L + (R - L) * i / (slots - 1);
  const y = (v: number) => B - (B - T) * v / top;
  const read = (v: number) => (metric === 'sessions' ? plural(v, 'session') : formatMinutes(v));

  const grid: number[] = [];
  for (let v = 0; v <= top; v += step) grid.push(v);
  const on = series.filter(v => v > 0);
  const mean = on.length >= 3 ? on.reduce((sum, v) => sum + v, 0) / on.length : null;
  const points = series.map((v, i): [number, number] => [x(i), y(v)]);
  const path = smooth(points);
  const meanSoFar = series.reduce((sum, v) => sum + v, 0) / series.length;
  const picked = pick !== null && pick !== last && pick <= last ? pick : null;
  const [tx, ty] = points[last] ?? [L, B];
  const anchor = tx > R - 46 ? 'end' : tx < L + 30 ? 'start' : 'middle';
  const total = series.reduce((sum, v) => sum + v, 0);

  const slotAt = (clientX: number) => {
    const rect = box.current?.getBoundingClientRect();
    if (!rect || !rect.width) return null;
    const at = (clientX - rect.left) * (width / rect.width);
    return Math.max(0, Math.min(last, Math.round((at - L) / (R - L) * (slots - 1))));
  };
  const onPointer = (event: ReactPointerEvent<SVGSVGElement>) => {
    if (event.type === 'pointerdown') { try { event.currentTarget.setPointerCapture(event.pointerId); } catch { /* the slide still follows */ } }
    else if (!event.buttons && event.pointerType === 'mouse') return;
    const slot = slotAt(event.clientX);
    if (slot !== null) setPick(slot);
  };
  const onKey = (event: KeyboardEvent<HTMLDivElement>) => {
    const move = event.key === 'ArrowRight' ? 1 : event.key === 'ArrowLeft' ? -1 : 0;
    if (!move) return;
    event.preventDefault();
    setPick(current => Math.max(0, Math.min(last, (current ?? last) + move)));
  };
  const said = (v: number) => (metric === 'sessions' ? plural(v, 'session') : v ? `${plural(v, 'minute')} of focused study` : 'No study recorded');
  const reading = pick !== null && buckets[pick] ? `${buckets[pick].accessibleLabel}: ${said(series[pick] ?? 0)}` : '';

  return (
    <div ref={box} className={`mp-graph ${className}`.trim()} tabIndex={0} onKeyDown={onKey}
      aria-label={`${metric === 'sessions' ? 'Sessions' : 'Focus time'} over the period: ${read(total)} in total. Use the arrow keys to read each ${slots === 12 ? 'month' : 'day'}.`}
      aria-describedby={noteId}>
      <svg className="mp-graph-svg" width={width} height={height} viewBox={`0 0 ${width} ${height}`} role="img" aria-hidden="true"
        onPointerDown={onPointer} onPointerMove={onPointer}>
        {grid.map(v => (
          <g key={v}>
            <line className="mp-graph-grid" x1={L} x2={R} y1={y(v)} y2={y(v)} />
            <text className="mp-graph-axis" x={L - 8} y={y(v) + 4} textAnchor="end">{metric === 'sessions' ? String(v) : v ? `${v / 60}h` : '0'}</text>
          </g>
        ))}
        {mean !== null ? (
          <>
            <rect className="mp-graph-band" x={L} width={R - L} y={y(Math.min(top, mean * 1.35))} height={y(mean * 0.65) - y(Math.min(top, mean * 1.35))} />
            <text className="mp-graph-steady" x={L + 2} y={y(Math.min(top, mean * 1.35)) - 5}>STEADY</text>
          </>
        ) : null}
        {path ? (
          <>
            <path className="mp-graph-fill" d={`${path} L${points[last][0].toFixed(1)} ${B} L${points[0][0].toFixed(1)} ${B} Z`} />
            <path className="mp-graph-line" d={path} />
          </>
        ) : null}
        {average ? (
          <>
            <line className="mp-graph-average" x1={L} x2={R} y1={y(meanSoFar)} y2={y(meanSoFar)} />
            <text className="mp-graph-axis" x={R} y={y(meanSoFar) - 6} textAnchor="end">{`Average ${metric === 'sessions' ? meanSoFar.toFixed(1) : formatMinutes(Math.round(meanSoFar))}`}</text>
          </>
        ) : null}
        {picked !== null ? <line className="mp-graph-pick" x1={x(picked)} x2={x(picked)} y1={T + 6} y2={B} /> : null}
        {buckets.map((bucket, i) => {
          const tick = tickFor(bucket, i, buckets.length);
          return tick === null ? null : (
            <text key={bucket.key} className={`mp-graph-axis${i === picked ? ' mp-graph-axis--on' : i === last ? ' mp-graph-axis--now' : ''}`} x={x(i)} y={B + 23} textAnchor="middle">{tick}</text>
          );
        })}
        <circle className="mp-graph-now" cx={tx} cy={ty} r={5} />
        <text className="mp-graph-value" x={anchor === 'end' ? tx + 4 : anchor === 'start' ? tx - 4 : tx} y={Math.max(T - 2, ty - 12)} textAnchor={anchor}>{read(series[last] ?? 0)}</text>
        {picked !== null ? (
          <>
            <circle className="mp-graph-pickdot" cx={x(picked)} cy={y(series[picked])} r={4.5} />
            <text className="mp-graph-reading" x={x(picked) + (x(picked) < L + 70 ? 9 : -9)} y={Math.min(B - 6, y(series[picked]) + 4)}
              textAnchor={x(picked) < L + 70 ? 'start' : 'end'}>{read(series[picked])}</text>
          </>
        ) : null}
      </svg>
      <p id={noteId} className="t-meta mp-graph-note">
        {`Touch the graph and slide to read a ${slots === 12 ? 'month' : 'day'}.${mean !== null ? ' The green band is your steady range.' : ''}`}
      </p>
      <p className="sr-only" role="status">{reading}</p>
    </div>
  );
}
