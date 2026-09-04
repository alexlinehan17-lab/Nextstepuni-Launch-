/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — synthesise a PAPER-side crop region for one question from the
 * answer-map anchors. The sidecars carry only a start anchor per question
 * (page pP + vertical band pY on that page); a question's full extent —
 * including its diagrams, tables and source material — runs from its own
 * anchor to the NEXT question's anchor. That derivation is what lets the
 * Topic Vault show the real question as printed without any new extraction.
 *
 * Honesty rule: when the anchors don't support a confident region (missing
 * question, non-monotonic anchors, implausibly long span), return null and
 * let the caller fall back to "open in the full paper" — never guess a crop.
 */

import { type PaperAnswerQuestion, type PaperAnswerSeg } from '../../types/paperTrail';

/** Small upward pad so the question's own header line isn't shaved off. */
const TOP_PAD = 0.008;
/** A question spanning more than this many pages is almost certainly a bad
 *  derivation (missing next anchor / section restart) — refuse it. */
const MAX_PAGES = 3;
/** A trailing sliver shorter than this fraction of a page adds nothing. */
const MIN_TAIL = 0.03;

/** Sort anchors into printed order (page, then vertical position). */
const inPrintOrder = (qs: PaperAnswerQuestion[]): PaperAnswerQuestion[] =>
  [...qs].sort((a, b) => a.pP - b.pP || a.pY[0] - b.pY[0]);

/**
 * Paper-side region for question `n`: from its anchor down to the next
 * question's anchor (spanning whole pages in between), or to its own band end
 * when it is the last anchored question. Returns null when no confident
 * region can be derived.
 */
export function paperRegionFor(
  qs: PaperAnswerQuestion[],
  n: string,
  maxPages = MAX_PAGES,
): PaperAnswerSeg[] | null {
  if (!qs.length) return null;
  const ordered = inPrintOrder(qs);
  const i = ordered.findIndex(q => q.n === n);
  if (i === -1) return null;
  const q = ordered[i];
  if (!q.pP || q.pP < 1 || !Array.isArray(q.pY)) return null;

  // A COLLAPSED anchor is not an anchor. lang_reading.py resolved a question's
  // paper position by searching the page for an anchor string, and on a miss it
  // substituted 0 — the top of the page — which reads downstream as a confident
  // "this question starts here". The tell is arithmetic: this question sits at
  // the very top of a page that also carries a LOWER-numbered question, which in
  // print order cannot happen. Cropping it hands the student a sliver of the
  // previous question's tail (2014 Italian Q5 shows Q1's last line), so refuse,
  // and let the caller fall back to opening the full paper.
  if (q.pY[0] === 0 && ordered.some(o => o.pP === q.pP && Number(o.n) < Number(q.n))) {
    return null;
  }

  const y0 = Math.max(0, Math.min(1, q.pY[0]) - TOP_PAD);

  // Explicit crop-END (section-restart "island" papers): the question's crop
  // must stop at (endP, endY), independent of the next anchor, so a reading
  // section's last question doesn't bleed into the following passage/section.
  // Fully additive — questions without endP/endY fall through to the unchanged
  // next-anchor derivation below.
  if (typeof q.endP === 'number' && typeof q.endY === 'number') {
    const endY = Math.min(1, Math.max(0, q.endY));
    // End must lie strictly after the start (monotonic), else no confident crop.
    if (q.endP < q.pP || (q.endP === q.pP && endY <= q.pY[0] + 0.005)) return null;
    if (q.endP - q.pP > maxPages) return null;
    if (q.endP === q.pP) return [{ p: q.pP, r: [0, y0, 1, endY] }];
    const segs: PaperAnswerSeg[] = [{ p: q.pP, r: [0, y0, 1, 1] }];
    for (let p = q.pP + 1; p < q.endP; p++) segs.push({ p, r: [0, 0, 1, 1] });
    if (endY > MIN_TAIL) segs.push({ p: q.endP, r: [0, 0, 1, endY] });
    return segs;
  }

  const next = ordered[i + 1];

  // Last anchored question — trust its own band; if the band is degenerate,
  // run to the bottom of the page (the composition/essay tail is rarely
  // anchored, so this stays within the question's own page).
  if (!next) {
    const y1 = q.pY[1] > y0 + 0.01 ? Math.min(1, q.pY[1]) : 1;
    return [{ p: q.pP, r: [0, y0, 1, y1] }];
  }

  // Non-monotonic anchors (same spot or going backwards) — no confident crop.
  if (next.pP < q.pP || (next.pP === q.pP && next.pY[0] <= q.pY[0] + 0.005)) return null;

  const span = next.pP - q.pP;
  if (span > maxPages) return null;

  if (span === 0) {
    return [{ p: q.pP, r: [0, y0, 1, Math.min(1, next.pY[0]) ] }];
  }

  const segs: PaperAnswerSeg[] = [{ p: q.pP, r: [0, y0, 1, 1] }];
  for (let p = q.pP + 1; p < next.pP; p++) segs.push({ p, r: [0, 0, 1, 1] });
  const tail = Math.min(1, next.pY[0]);
  if (tail > MIN_TAIL) segs.push({ p: next.pP, r: [0, 0, 1, tail] });
  return segs;
}
