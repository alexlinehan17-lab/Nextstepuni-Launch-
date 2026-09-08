/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * A deterministic marker for the landing page's "answer like an examiner"
 * pieces and Today's Question. No model, no network: an answer earns a
 * scheme point when it says what the scheme's line says.
 *
 * The scheme line is the truth (verbatim, from the marking scheme). A point
 * can carry explicit `accept` alternatives — each a list of tokens that must
 * all appear — for lines where the wording matters (a formula, a number with
 * its unit, a one-word answer). Without them, the point is earned when most
 * of the line's content words appear in the answer: every content token for a
 * short line, three of five for a long one. Tokens are lower-cased with light
 * stemming, so "cells" meets "cell" and "digested" meets "digest".
 */

export interface MarkPoint {
  id: string;
  /** The scheme's own words for this point. */
  verbatim: string;
  marks: number;
  /** Optional alternatives, each a list of tokens that must all be present. */
  accept?: string[][];
}

export interface PointHit { id: string; marks: number; matched: boolean }
export interface MarkResult { earned: number; total: number; hits: PointHit[] }

const STOP = new Set(('a an the and or of to in on at by for with from as is are was were be been being it its this that these those any ' +
  'each all both either neither not no nor so than then there their they them he she his her we our you your i my one two three ' +
  'into onto over under between through during after before above below up down out off again further once here where when why how ' +
  'which who whom what such only own same other some more most very can will just should would could may might must shall do does did ' +
  'has have had having e.g i.e etc via per also').split(/\s+/));

const stem = (w: string): string => {
  if (w.length <= 3) return w;
  if (/\d/.test(w)) return w;
  return w
    .replace(/(ies)$/, 'y')
    .replace(/(sses|shes|ches|xes)$/, (m) => m.slice(0, -2))
    .replace(/(ing|ed|ly)$/, '')
    .replace(/(s)$/, '');
};

/** Lower-case, strip punctuation that is not part of a formula, split, stem. */
export const tokens = (s: string): string[] =>
  s
    .toLowerCase()
    .replace(/[’'`]/g, '')
    .replace(/[−–—]/g, '-')
    .replace(/[^a-z0-9%°+\-=/().,\s]/g, ' ')
    .replace(/[(),]/g, ' ')
    .replace(/(?<=\D)[./](?=\D)/g, ' ')
    .split(/\s+/)
    .filter(Boolean)
    .map(stem);

/**
 * A scheme line's bracketed text is an elaboration or an alternative
 * ("Peristalsis (muscular contraction)"), so the words outside the brackets
 * are what the answer must carry; the bracketed words count only when the
 * line is nothing but brackets.
 */
const contentTokens = (s: string): string[] => {
  const outside = s.replace(/\([^)]*\)/g, ' ');
  const pick = (t: string) => Array.from(new Set(tokens(t).filter(w => !STOP.has(w) && w.length > 1)));
  const main = pick(outside);
  return main.length ? main : pick(s);
};

/** How many of a line's content tokens an answer must carry to earn it. */
export const needed = (n: number): number => (n <= 3 ? n : Math.ceil(n * 0.6));

export const pointMatched = (answerTokens: Set<string>, point: MarkPoint): boolean => {
  if (point.accept && point.accept.length) {
    return point.accept.some(alt => alt.length > 0 && alt.every(t => tokens(t).every(tt => answerTokens.has(tt))));
  }
  const content = contentTokens(point.verbatim);
  if (content.length === 0) return false;
  const found = content.filter(t => answerTokens.has(t)).length;
  return found >= needed(content.length);
};

export const markAnswer = (answer: string, points: MarkPoint[]): MarkResult => {
  const set = new Set(tokens(answer));
  const hits = points.map(p => ({ id: p.id, marks: p.marks, matched: set.size > 0 && pointMatched(set, p) }));
  return { earned: hits.reduce((n, h) => n + (h.matched ? h.marks : 0), 0), total: points.reduce((n, p) => n + p.marks, 0), hits };
};

/** Orange squares for the share card: one per point, in scheme order. */
export const squares = (result: MarkResult): string => result.hits.map(h => (h.matched ? '\u{1F7E7}' : '⬜')).join('');
