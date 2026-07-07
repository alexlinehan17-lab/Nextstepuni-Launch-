/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — resolve a topic sibling (subject/year/level/lang/fileid) to
 * its Storage URLs via the committed index. Pure lookup, no fetching.
 */

import { PAPER_TRAIL_INDEX, PAPER_TRAIL_SUBJECTS } from '../../paperTrailData';
import { paperAnswersPath, paperStoragePath, paperUrl } from './storage';
import { type TopicSibling } from './topics';

export interface ResolvedSibling {
  paperUrl: string;
  /** Null when the index has no scheme for this paper. */
  schemeUrl: string | null;
  answersUrl: string;
  paperLabel: string;
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
        paperLabel: item.label,
      }
    : null;
  memo.set(key, out);
  return out;
}
