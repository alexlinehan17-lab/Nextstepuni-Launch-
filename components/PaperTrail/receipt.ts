/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — end-of-loop receipt. A compact, shareable summary of one Full
 * Loop session: date, paper, questions worked, time, average self-mark, gaps
 * flagged. Anonymous by construction — no name, no uid, ever.
 *
 * composeReceipt() is a pure layout function (unit-tested in
 * test/ptReceipt.test.ts); drawReceipt() paints that layout onto a canvas with
 * the design tokens (Source Serif 4 headings, DM Sans body, accent #F26B1F,
 * success #3A8D5F, white card with a bold ink border) — no external libraries.
 */

import { type GapKind } from './attemptStore';

export interface LoopReceiptStats {
  /** ISO date of the session, e.g. "2026-07-07". */
  dateIso: string;
  /** e.g. "Biology · 2023". */
  paperTitle: string;
  /** e.g. "Paper One · Higher". */
  paperDetail?: string;
  questionsWorked: number;
  questionsTotal: number;
  /** Whole-loop time in seconds (0 = unknown). */
  totalSec: number;
  /** Average self-mark percentage, or null when nothing was marked. */
  avgPct: number | null;
  gaps: Partial<Record<GapKind, number>>;
}

export interface ReceiptLayout {
  header: string;
  date: string;
  title: string;
  detail?: string;
  /** The hero number, e.g. "72%" (or "—" when nothing was marked). */
  score: string;
  /** true → the hero renders in success green; false → accent orange. */
  scoreIsGood: boolean;
  rows: { label: string; value: string }[];
  footer: string;
}

const GAP_SHORT: Record<GapKind, string> = {
  content: 'content',
  process: 'method',
  careless: 'careless',
  timing: 'timing',
};

/** "2026-07-07" → "7 July 2026" (falls back to the raw string). */
export function prettyDate(dateIso: string): string {
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(dateIso);
  if (!m) return dateIso;
  const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  const month = months[Number(m[2]) - 1];
  return month ? `${Number(m[3])} ${month} ${m[1]}` : dateIso;
}

export function formatDuration(totalSec: number): string {
  if (!Number.isFinite(totalSec) || totalSec <= 0) return '—';
  const mins = Math.round(totalSec / 60);
  if (mins < 1) return 'under a minute';
  if (mins < 60) return `${mins} min`;
  const h = Math.floor(mins / 60);
  const m = mins % 60;
  return m ? `${h} h ${m} min` : `${h} h`;
}

export function formatGaps(gaps: Partial<Record<GapKind, number>>): string {
  const parts = (Object.entries(gaps) as [GapKind, number][])
    .filter(([, n]) => n > 0)
    .sort((a, b) => b[1] - a[1])
    .map(([g, n]) => `${n}× ${GAP_SHORT[g]}`);
  return parts.length ? parts.join(', ') : 'none flagged';
}

/** Pure layout: the exact text the receipt carries, with no student identity. */
export function composeReceipt(stats: LoopReceiptStats): ReceiptLayout {
  return {
    header: 'THE FULL LOOP · RECEIPT',
    date: prettyDate(stats.dateIso),
    title: stats.paperTitle,
    ...(stats.paperDetail ? { detail: stats.paperDetail } : {}),
    score: stats.avgPct == null ? '—' : `${stats.avgPct}%`,
    scoreIsGood: stats.avgPct != null && stats.avgPct >= 66,
    rows: [
      { label: 'Questions worked', value: `${stats.questionsWorked} of ${stats.questionsTotal}` },
      { label: 'Time', value: formatDuration(stats.totalSec) },
      { label: 'Average self-mark', value: stats.avgPct == null ? '—' : `${stats.avgPct}%` },
      { label: 'Gaps flagged', value: formatGaps(stats.gaps) },
    ],
    footer: 'Self-marked against the official SEC marking scheme · Paper Trail',
  };
}

// ─── canvas rendering (design tokens, hand-drawn) ───────────

const INK = '#1a1a1a';
const ACCENT = '#F26B1F';
const SUCCESS = '#3A8D5F';
const MUTED = '#7a7068';
const LABEL = '#9e9186';
const RULE = '#d0cdc8';

const W = 640;
const SCALE = 2; // retina-crisp PNG

/** Paint the composed layout onto a canvas. Exported for reuse/preview. */
export function drawReceipt(canvas: HTMLCanvasElement, layout: ReceiptLayout): boolean {
  const rowH = 34;
  const detailH = layout.detail ? 24 : 0;
  const height = 236 + detailH + layout.rows.length * rowH + 56;
  canvas.width = W * SCALE;
  canvas.height = height * SCALE;
  const ctx = canvas.getContext('2d');
  if (!ctx) return false;
  ctx.scale(SCALE, SCALE);

  // Card: white, bold ink border (the primary-card language).
  ctx.fillStyle = '#ffffff';
  ctx.fillRect(0, 0, W, height);
  ctx.strokeStyle = INK;
  ctx.lineWidth = 4;
  ctx.strokeRect(2, 2, W - 4, height - 4);

  const left = 36;
  const right = W - 36;
  let y = 52;

  // Header label + date.
  ctx.fillStyle = LABEL;
  ctx.font = '700 12px "DM Sans", sans-serif';
  ctx.textAlign = 'left';
  ctx.fillText(layout.header, left, y);
  ctx.textAlign = 'right';
  ctx.fillText(layout.date, right, y);
  y += 34;

  // Paper title (serif) + detail.
  ctx.textAlign = 'left';
  ctx.fillStyle = INK;
  ctx.font = '600 26px "Source Serif 4", serif';
  ctx.fillText(layout.title, left, y);
  y += 8;
  if (layout.detail) {
    y += 24;
    ctx.fillStyle = MUTED;
    ctx.font = '400 14px "DM Sans", sans-serif';
    ctx.fillText(layout.detail, left, y);
  }
  y += 30;

  // Hero score — success green only when it genuinely reads "good".
  ctx.fillStyle = layout.scoreIsGood ? SUCCESS : ACCENT;
  ctx.font = '700 56px "Source Serif 4", serif';
  ctx.fillText(layout.score, left, y + 44);
  y += 72;

  // Divider.
  ctx.strokeStyle = RULE;
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.moveTo(left, y);
  ctx.lineTo(right, y);
  ctx.stroke();
  y += 30;

  // Rows.
  for (const row of layout.rows) {
    ctx.fillStyle = MUTED;
    ctx.font = '400 14px "DM Sans", sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText(row.label, left, y);
    ctx.fillStyle = INK;
    ctx.font = '600 15px "DM Sans", sans-serif';
    ctx.textAlign = 'right';
    ctx.fillText(row.value, right, y);
    y += rowH;
  }

  // Footer.
  y += 6;
  ctx.fillStyle = LABEL;
  ctx.font = '400 11px "DM Sans", sans-serif';
  ctx.textAlign = 'left';
  ctx.fillText(layout.footer, left, y);
  return true;
}

/** Compose, draw and download the receipt PNG. Returns false when the canvas
 *  pipeline is unavailable (the caller shows a quiet failure line). */
export function downloadReceipt(stats: LoopReceiptStats): boolean {
  try {
    const layout = composeReceipt(stats);
    const canvas = document.createElement('canvas');
    if (!drawReceipt(canvas, layout)) return false;
    const trigger = (url: string, revoke: boolean) => {
      const a = document.createElement('a');
      a.href = url;
      a.download = `full-loop-receipt-${stats.dateIso}.png`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      if (revoke) setTimeout(() => URL.revokeObjectURL(url), 5000);
    };
    if (canvas.toBlob) {
      canvas.toBlob(blob => {
        if (blob) trigger(URL.createObjectURL(blob), true);
      }, 'image/png');
    } else {
      trigger(canvas.toDataURL('image/png'), false);
    }
    return true;
  } catch {
    return false;
  }
}
