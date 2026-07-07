/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — end-of-session receipt.
 *
 * When a marking session completes, the summary offers a compact receipt:
 * date, session, scripts marked, agreement, calibration band, streak. The
 * layout composition is a pure, unit-tested function (composeReceipt); the
 * canvas renderer below draws that composed model with the design tokens and
 * downloads it as a PNG — no libraries, no student name or uid anywhere on
 * the image (anonymous by construction: the model never receives one).
 */

import { calibrationBand, pct } from './store';

// ── design tokens (mirrors index.tsx / the visual design system) ──

const INK = '#1a1a1a';
const ACCENT = '#F26B1F';
const SUCCESS = '#3A8D5F';
const MUTED = '#7a7068';
const LABEL = '#9e9186';
const RULE = '#d0cdc8';

const SERIF = '"Source Serif 4", serif';
const SANS = '"DM Sans", sans-serif';

// ── pure layout composition ──

export interface ReceiptStats {
  sessionTitle: string;
  subjectLabel: string;
  levelLabel: string;
  scriptsMarked: number;
  /** 0..1 mean agreement with the examiner across the session. */
  agreement: number;
  /** Current daily-mark streak (0 = no streak row). */
  streak: number;
  /** Practice runs (borderline drill / daily mark) are labelled as such. */
  kind?: 'session' | 'borderline-drill' | 'daily-mark';
}

export interface ReceiptRow {
  label: string;
  value: string;
  /** Semantic colour for the value: agreement ≥75% earns the success token. */
  tone: 'ink' | 'accent' | 'success';
}

export interface ReceiptModel {
  /** Uppercase eyebrow, e.g. "THE EXAMINER'S CHAIR · MARKING RECEIPT". */
  header: string;
  /** Session title (serif headline). */
  title: string;
  /** Context line: subject · level · date. */
  context: string;
  rows: ReceiptRow[];
  footnote: string;
}

const MONTHS = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December',
];

/** Deterministic UTC date label, e.g. "7 July 2026" (no locale drift). */
export function receiptDateLabel(now: number): string {
  const d = new Date(now);
  return `${d.getUTCDate()} ${MONTHS[d.getUTCMonth()]} ${d.getUTCFullYear()}`;
}

/** Download filename, e.g. "examiners-chair-receipt-2026-07-07.png". */
export function receiptFilename(now: number): string {
  const d = new Date(now);
  const mm = String(d.getUTCMonth() + 1).padStart(2, '0');
  const dd = String(d.getUTCDate()).padStart(2, '0');
  return `examiners-chair-receipt-${d.getUTCFullYear()}-${mm}-${dd}.png`;
}

const KIND_LABEL: Record<NonNullable<ReceiptStats['kind']>, string> = {
  'session': 'Marking receipt',
  'borderline-drill': 'Borderline drill',
  'daily-mark': 'The Daily Mark',
};

/** Compose the receipt (pure). Everything on the image comes from here —
 * the stats carry no name or uid, so neither can the receipt. */
export function composeReceipt(stats: ReceiptStats, now: number): ReceiptModel {
  const kind = KIND_LABEL[stats.kind ?? 'session'];
  const agreementTone: ReceiptRow['tone'] = stats.agreement >= 0.75 ? 'success' : 'accent';
  const rows: ReceiptRow[] = [
    {
      label: 'Scripts marked',
      value: `${stats.scriptsMarked}`,
      tone: 'ink',
    },
    {
      label: 'Agreement with the examiner',
      value: pct(stats.agreement),
      tone: agreementTone,
    },
    {
      label: 'Calibration',
      value: calibrationBand(stats.agreement),
      tone: agreementTone,
    },
  ];
  if (stats.streak > 0) {
    rows.push({
      label: 'Daily Mark streak',
      value: `${stats.streak} ${stats.streak === 1 ? 'day' : 'days'}`,
      tone: 'ink',
    });
  }
  return {
    header: `The Examiner’s Chair · ${kind}`.toUpperCase(),
    title: stats.sessionTitle,
    context: `${stats.subjectLabel} · ${stats.levelLabel} · ${receiptDateLabel(now)}`,
    rows,
    footnote: 'Practice scripts marked against the SEC’s published marking rules.',
  };
}

// ── canvas renderer (thin, untested — the model above is the tested part) ──

const W = 560;
const PAD = 36;
const SCALE = 2;

const toneHex = (tone: ReceiptRow['tone']): string =>
  tone === 'success' ? SUCCESS : tone === 'accent' ? ACCENT : INK;

function roundedRect(ctx: CanvasRenderingContext2D, x: number, y: number, w: number, h: number, r: number): void {
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.arcTo(x + w, y, x + w, y + h, r);
  ctx.arcTo(x + w, y + h, x, y + h, r);
  ctx.arcTo(x, y + h, x, y, r);
  ctx.arcTo(x, y, x + w, y, r);
  ctx.closePath();
}

/** Draw the composed receipt onto a canvas (returns the canvas for download). */
export function drawReceipt(model: ReceiptModel): HTMLCanvasElement {
  const rowH = 34;
  const h = 178 + model.rows.length * rowH + 58;
  const canvas = document.createElement('canvas');
  canvas.width = W * SCALE;
  canvas.height = h * SCALE;
  const ctx = canvas.getContext('2d');
  if (!ctx) return canvas;
  ctx.scale(SCALE, SCALE);

  // page ground + the white card with the signature 2px ink border
  ctx.fillStyle = '#f0f0f0';
  ctx.fillRect(0, 0, W, h);
  roundedRect(ctx, 8, 8, W - 16, h - 16, 16);
  ctx.fillStyle = '#ffffff';
  ctx.fill();
  ctx.lineWidth = 2;
  ctx.strokeStyle = INK;
  ctx.stroke();

  ctx.textBaseline = 'alphabetic';

  // eyebrow
  ctx.font = `700 11px ${SANS}`;
  ctx.fillStyle = LABEL;
  const tracked = ctx as CanvasRenderingContext2D & { letterSpacing?: string };
  if ('letterSpacing' in tracked) tracked.letterSpacing = '1.5px';
  ctx.fillText(model.header, PAD, 56);
  if ('letterSpacing' in tracked) tracked.letterSpacing = '0px';

  // serif title
  ctx.font = `600 20px ${SERIF}`;
  ctx.fillStyle = INK;
  ctx.fillText(model.title, PAD, 88);

  // context line
  ctx.font = `400 13px ${SANS}`;
  ctx.fillStyle = MUTED;
  ctx.fillText(model.context, PAD, 112);

  // rule
  ctx.strokeStyle = RULE;
  ctx.lineWidth = 1;
  ctx.setLineDash([2, 3]);
  ctx.beginPath();
  ctx.moveTo(PAD, 134);
  ctx.lineTo(W - PAD, 134);
  ctx.stroke();
  ctx.setLineDash([]);

  // rows: sans label left, serif value right
  let y = 168;
  for (const row of model.rows) {
    ctx.font = `400 13.5px ${SANS}`;
    ctx.fillStyle = MUTED;
    ctx.textAlign = 'left';
    ctx.fillText(row.label, PAD, y);
    ctx.font = `700 17px ${SERIF}`;
    ctx.fillStyle = toneHex(row.tone);
    ctx.textAlign = 'right';
    ctx.fillText(row.value, W - PAD, y + 1);
    ctx.textAlign = 'left';
    y += rowH;
  }

  // footnote
  ctx.font = `italic 400 11px ${SANS}`;
  ctx.fillStyle = LABEL;
  ctx.fillText(model.footnote, PAD, h - 34);

  return canvas;
}

/** Render + download the receipt PNG. Waits for the web fonts so the serif
 * headings actually render in Source Serif 4. Best-effort — failures are
 * silent (the on-screen card is the source of truth). */
export async function downloadReceiptPng(model: ReceiptModel, now: number): Promise<void> {
  try {
    const fonts = (document as Document & { fonts?: FontFaceSet }).fonts;
    if (fonts) {
      await Promise.all([
        fonts.load(`600 20px ${SERIF}`),
        fonts.load(`700 17px ${SERIF}`),
        fonts.load(`400 13px ${SANS}`),
        fonts.load(`700 11px ${SANS}`),
      ]).catch(() => {});
    }
    const canvas = drawReceipt(model);
    const blob = await new Promise<Blob | null>(resolve => canvas.toBlob(resolve, 'image/png'));
    if (!blob) return;
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = receiptFilename(now);
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 5000);
  } catch {
    /* best-effort */
  }
}
