/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — live PDF text-layer extraction for the on-paper study tools
 * (time-budget chips, command-word decoder). Universal + data-light: every
 * overlay is derived from pdf.js's own `getTextContent()` at read time, so it
 * works on any paper in the corpus with no per-paper sidecar.
 *
 * The extractor reconstructs lines from the raw text items (pdf.js emits them
 * in reading-ish order but not grouped), then locates two things per page:
 *  - marks tokens — "(20 marks)" / "20 marks" — the anchor for time budgeting;
 *  - command words — "Explain", "Discuss", "Evaluate"… — but ONLY when they are
 *    the first word of a question line, which kills the "state of matter" /
 *    "United States" mid-sentence false positives that would otherwise litter
 *    the page. Precision beats recall here: a wrong highlight reads as a bug.
 *
 * All positions are returned as fractions of page width/height in [0,1], so the
 * caller can place overlays on top of the virtualised, zoom-scaled canvases
 * without knowing the render scale (mirrors the answer-map anchor convention).
 */

import type { PDFPageProxy } from 'pdfjs-dist';
import { COMMAND_WORDS } from '../../data/knowledge/commandWords';
import type { CommandWordEntry } from '../../types/knowledge';

// ─── shapes ─────────────────────────────────────────────────

export interface OverlayBox {
  /** Fractional top-left of the run, in [0,1] of page width/height. */
  pX: number;
  pY: number;
  /** Fractional width/height of the run. */
  pW: number;
  pH: number;
}

export interface MarkToken extends OverlayBox {
  /** Mark value, e.g. 20 for "(20 marks)". */
  value: number;
}

export interface CommandToken extends OverlayBox {
  /** The surface word actually matched (e.g. "Assess"). */
  matched: string;
  entry: CommandWordEntry;
}

export interface PageTokens {
  marks: MarkToken[];
  commands: CommandToken[];
}

export interface DocTokens {
  byPage: Map<number, PageTokens>;
  /** Sum of every marks token across the paper — the data-light "total marks"
   *  estimate used for the generic (no official timing) pace fallback. Inflated
   *  by "answer any 2 of 4" choice sections, so treat as an upper bound. */
  totalMarks: number;
}

// ─── regexes + command index ────────────────────────────────

const escapeRe = (s: string) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

// Marks: parenthesised "(20 marks)" or bare "20 marks". Requires the word
// "mark(s)" so plain numbers / years / list markers don't match.
const MARKS_RE = /\((\d{1,3})\s*marks?\)|\b(\d{1,3})\s*marks?\b/gi;

// Surface → canonical entry, longest surfaces first so "To what extent" wins
// over any shorter accidental substring.
const COMMAND_BY_SURFACE = new Map<string, CommandWordEntry>();
for (const e of COMMAND_WORDS) {
  COMMAND_BY_SURFACE.set(e.word.toLowerCase(), e);
  for (const a of e.aliases ?? []) COMMAND_BY_SURFACE.set(a.toLowerCase(), e);
}
const COMMAND_SURFACES = [...COMMAND_BY_SURFACE.keys()].sort((a, b) => b.length - a.length);
const COMMAND_RE = new RegExp(`\\b(${COMMAND_SURFACES.map(escapeRe).join('|')})\\b`, 'gi');

// A leading question enumerator: "(a)", "(iii)", "3.", "12)", nested. Consumed
// so a command word sitting right after the label still counts as "first word".
const ENUMERATOR_RE = /^\s*(?:\((?:[ivxlcdm]+|[a-z]|\d{1,2})\)\s*|(?:\d{1,2}|[a-z])[.)]\s*)*/i;

// ─── geometry helpers ───────────────────────────────────────

/** Apply a pdf.js 6-element affine [a,b,c,d,e,f] to a point. */
function apply(m: number[], x: number, y: number): [number, number] {
  return [m[0] * x + m[2] * y + m[4], m[1] * x + m[3] * y + m[5]];
}

interface Span {
  str: string;
  x: number; // device left (px, top-based space)
  y: number; // device baseline top (px from page top)
  w: number; // advance width (px)
  h: number; // glyph height (px)
}

interface Segment {
  span: Span;
  start: number; // char offset of this span in the reconstructed line
  end: number;
}

// ─── per-page extraction ────────────────────────────────────

export async function extractPageTokens(page: PDFPageProxy): Promise<PageTokens> {
  const vp = page.getViewport({ scale: 1 });
  const W = vp.width || 1;
  const H = vp.height || 1;

  let content;
  try {
    content = await page.getTextContent();
  } catch {
    return { marks: [], commands: [] };
  }

  const spans: Span[] = [];
  for (const raw of content.items as unknown[]) {
    const it = raw as { str?: string; width?: number; height?: number; transform?: number[] };
    if (!it.str || !it.transform) continue;
    const t = it.transform;
    const [dx, dy] = apply(vp.transform, t[4], t[5]);
    const h = Math.hypot(t[1], t[3]) || it.height || 10;
    spans.push({ str: it.str, x: dx, y: dy, w: it.width || 0, h });
  }
  if (spans.length === 0) return { marks: [], commands: [] };

  // Group into visual lines by baseline proximity, then order left→right.
  spans.sort((a, b) => a.y - b.y || a.x - b.x);
  const lines: Span[][] = [];
  let current: Span[] = [];
  let lineY = spans[0].y;
  for (const s of spans) {
    const tol = Math.max(3, s.h * 0.6);
    if (current.length === 0 || Math.abs(s.y - lineY) <= tol) {
      current.push(s);
      lineY = (lineY * (current.length - 1) + s.y) / current.length;
    } else {
      lines.push(current);
      current = [s];
      lineY = s.y;
    }
  }
  if (current.length) lines.push(current);

  const marks: MarkToken[] = [];
  const commands: CommandToken[] = [];

  for (const line of lines) {
    line.sort((a, b) => a.x - b.x);
    // Reconstruct the line text with a char→span map, inserting a space where
    // there's a real horizontal gap between adjacent spans.
    let text = '';
    const segs: Segment[] = [];
    let prevRight: number | null = null;
    for (const span of line) {
      if (prevRight !== null) {
        const gap = span.x - prevRight;
        const endsSpaced = text.endsWith(' ') || span.str.startsWith(' ');
        if (!endsSpaced && gap > span.h * 0.28) text += ' ';
      }
      const start = text.length;
      text += span.str;
      segs.push({ span, start, end: text.length });
      prevRight = span.x + span.w;
    }
    if (!text.trim()) continue;

    const boxFor = (mStart: number, mEnd: number): OverlayBox | null => {
      const startSeg = segs.find(s => mStart >= s.start && mStart < s.end) ?? segs[0];
      const endSeg = segs.find(s => mEnd - 1 >= s.start && mEnd - 1 < s.end) ?? segs[segs.length - 1];
      if (!startSeg || !endSeg) return null;
      const perChar = (s: Segment) => (s.span.str.length ? s.span.w / s.span.str.length : 0);
      const x0 = startSeg.span.x + (mStart - startSeg.start) * perChar(startSeg);
      const x1 = endSeg.span.x + (mEnd - endSeg.start) * perChar(endSeg);
      const y = startSeg.span.y;
      const h = startSeg.span.h;
      return {
        pX: Math.min(x0, x1) / W,
        pY: Math.max(0, (y - h)) / H,
        pW: Math.max(2, Math.abs(x1 - x0)) / W,
        pH: (h * 1.35) / H,
      };
    };

    // Marks — any occurrence on the line.
    MARKS_RE.lastIndex = 0;
    let m: RegExpExecArray | null;
    while ((m = MARKS_RE.exec(text)) !== null) {
      const value = Number(m[1] ?? m[2]);
      if (!Number.isFinite(value) || value <= 0 || value > 800) continue;
      const box = boxFor(m.index, m.index + m[0].length);
      if (box) marks.push({ ...box, value });
    }

    // Command words — ONLY as the first word of a question line. The SEC
    // boilerplate line "State Examinations Commission" would otherwise trip
    // "State"; skip any line carrying that mark.
    if (/examinations?\s+commission/i.test(text)) continue;
    const bodyStart = (ENUMERATOR_RE.exec(text)?.[0].length) ?? 0;
    COMMAND_RE.lastIndex = 0;
    let c: RegExpExecArray | null;
    while ((c = COMMAND_RE.exec(text)) !== null) {
      if (c.index !== bodyStart) continue; // not the leading command → skip
      const surface = c[0].toLowerCase();
      const entry = COMMAND_BY_SURFACE.get(surface);
      if (!entry) continue;
      const box = boxFor(c.index, c.index + c[0].length);
      if (box) commands.push({ ...box, matched: c[0], entry });
    }
  }

  return { marks, commands };
}

// ─── whole-document scan ────────────────────────────────────

/** Scan every page once. Cheap relative to rendering (no rasterisation), and
 *  the caller memoises the result so it runs a single time per open paper. */
export async function scanDocument(
  pdf: { numPages: number; getPage: (n: number) => Promise<PDFPageProxy> },
): Promise<DocTokens> {
  const byPage = new Map<number, PageTokens>();
  let totalMarks = 0;
  for (let n = 1; n <= pdf.numPages; n++) {
    let page: PDFPageProxy | null = null;
    try {
      page = await pdf.getPage(n);
      const tokens = await extractPageTokens(page);
      byPage.set(n, tokens);
      // Denominator for the generic (no-official-timing) pace: sum only
      // question-level marks. Exclude the cover page (carries the grand total)
      // and section/grand totals (≥ 100 marks) so a question's share isn't
      // diluted by totals that re-count marks already summed below them.
      if (n > 1) for (const mk of tokens.marks) if (mk.value < 100) totalMarks += mk.value;
    } catch {
      byPage.set(n, { marks: [], commands: [] });
    } finally {
      page?.cleanup();
    }
  }
  return { byPage, totalMarks };
}
