/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — resolve a topic sibling (subject/year/level/lang/fileid) to
 * its Storage URLs via the committed index. Pure lookup, no fetching.
 */

import { type PaperAnswerMap } from '../../types/paperTrail';
import { PAPER_TRAIL_INDEX, PAPER_TRAIL_SUBJECTS } from '../../paperTrailData';
import { paperAnswersPath, paperStoragePath, paperUrl } from './storage';
import { type TopicSibling } from './topics';

export interface ResolvedSibling {
  paperUrl: string;
  /** Null when the index has no scheme for this paper. */
  schemeUrl: string | null;
  answersUrl: string;
  /** Hosted paper-side-only anchor sidecar (public/paper-anchors/, deployed
   *  with the app — no Storage object). Tried when `answersUrl` misses; same
   *  PaperAnswerMap schema with mode:'pagejump' throughout, so the card gets
   *  its paper crop while the answer toggle stays on the honest
   *  "Open beside its marking scheme" fallback. */
  anchorsUrl: string;
  paperLabel: string;
}

/** Hosting path for a paper's committed paper-anchors sidecar. Year + fileid
 *  is unique (fileids recur across years but encode exam/subject/level/
 *  component/lang), mirroring scripts/paper-trail/answers/<year>/<fileid>.json. */
export const hostedAnchorsUrl = (year: number, fileid: string) =>
  `/paper-anchors/${year}/${encodeURIComponent(fileid)}.json`;

/** Ordered answer-map candidates: the verified Storage sidecar first (it may
 *  carry scheme crops), then the hosted paper-only anchors. */
export const answerMapUrls = (r: ResolvedSibling): string[] => [r.answersUrl, r.anchorsUrl];

/**
 * Shape guard for a fetched answer map. Firebase Hosting rewrites every
 * unknown path to index.html with HTTP 200, so a missing hosted sidecar comes
 * back as HTML (JSON parse fails) — and any other valid-JSON-but-wrong-shape
 * response must also read as a miss, never reach the renderer.
 */
export function isAnswerMap(v: unknown): v is PaperAnswerMap {
  if (typeof v !== 'object' || v === null) return false;
  const m = v as Record<string, unknown>;
  if (typeof m.paperFileid !== 'string' || !Array.isArray(m.q) || m.q.length === 0) return false;
  return m.q.every((q: unknown) => {
    if (typeof q !== 'object' || q === null) return false;
    const x = q as Record<string, unknown>;
    return (
      typeof x.n === 'string' &&
      typeof x.pP === 'number' && x.pP >= 1 &&
      Array.isArray(x.pY) && x.pY.length === 2 && x.pY.every(y => typeof y === 'number') &&
      Array.isArray(x.region) &&
      (x.mode === 'crop' || x.mode === 'pagejump')
    );
  });
}

const cycleById = new Map(PAPER_TRAIL_SUBJECTS.map(s => [s.id, s.cycle]));

/** In-memory memo — the vault feed resolves the same tuple repeatedly. */
const memo = new Map<string, ResolvedSibling | null>();

export function resolveSibling(t: TopicSibling): ResolvedSibling | null {
  const key = `${t.subjectId}|${t.year}|${t.level}|${t.lang}|${t.fileid}`;
  if (memo.has(key)) return memo.get(key)!;
  const cycle = cycleById.get(t.subjectId);
  const entry = (PAPER_TRAIL_INDEX[t.subjectId] ?? []).find(
    e => e.year === t.year && e.level === t.level && e.lang === t.lang,
  );
  const item = entry?.papers.find(p => p.doc.f === t.fileid);
  const out: ResolvedSibling | null = cycle && item
    ? {
        paperUrl: paperUrl(paperStoragePath(cycle, t.subjectId, t.year, 'paper', item.doc.f)),
        schemeUrl: item.scheme
          ? paperUrl(paperStoragePath(cycle, t.subjectId, t.year, 'scheme', item.scheme.f))
          : null,
        answersUrl: paperUrl(paperAnswersPath(cycle, t.subjectId, t.year, item.doc.f)),
        anchorsUrl: hostedAnchorsUrl(t.year, item.doc.f),
        paperLabel: item.label,
      }
    : null;
  memo.set(key, out);
  return out;
}
