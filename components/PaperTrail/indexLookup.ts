/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — resolve one indexed document by its full identity.
 *
 * A year/level/language can hold more than one entry: the June sitting and,
 * from 2022, the SEC's deferred sitting (a separate entry, listed after June).
 * Taking the first entry for a year and then looking for the fileid would miss
 * every deferred paper, so a stored or linked document is resolved across all
 * of that year's entries.
 */

import { PAPER_TRAIL_INDEX } from '../../paperTrailData';
import type { PaperEntry, PaperItem, PaperLang, PaperLevel } from '../../types/paperTrail';

export function findIndexedItem(
  subjectId: string,
  year: number,
  level: PaperLevel | string | null,
  lang: PaperLang | string | null,
  fileid: string | null,
): { entry: PaperEntry; item: PaperItem } | null {
  for (const entry of PAPER_TRAIL_INDEX[subjectId] ?? []) {
    if (entry.year !== year || entry.level !== level || entry.lang !== lang) continue;
    const item = entry.papers.find(p => p.doc.f === fileid);
    if (item) return { entry, item };
  }
  return null;
}

const yearViews = new Map<string, PaperEntry>();

/**
 * One list for a year/level/language: the June papers followed by the deferred
 * sitting's (whose items carry `sitting`). Memoised so the archive view keeps
 * a stable object across renders (open previews compare entries by identity).
 */
export function yearEntryView(subjectId: string, entries: PaperEntry[]): PaperEntry | undefined {
  if (entries.length <= 1) return entries[0];
  const [first] = entries;
  const key = `${subjectId}|${first.year}|${first.level}|${first.lang}`;
  const cached = yearViews.get(key);
  if (cached) return cached;
  const june = entries.find(e => !e.sitting) ?? first;
  const view: PaperEntry = {
    ...june,
    papers: [...june.papers, ...entries.filter(e => e !== june).flatMap(e => e.papers)],
  };
  yearViews.set(key, view);
  return view;
}

/** First year of the window the Mark Bank, Topic Atlas and answer-map reviews
 *  cover. Earlier papers (1995-2009) are archive-only: several predate a
 *  syllabus change and none has a reviewed answer map. */
export const REVIEWED_ARCHIVE_FROM = 2010;

/** A subject's June-sitting entries inside the reviewed window — what corpus
 *  inventories reconcile against. Deferred-sitting and sample entries, and
 *  pre-2010 years, are listed in Paper Trail but not part of those reviews. */
export const reviewedArchiveEntries = (subjectId: string): PaperEntry[] =>
  (PAPER_TRAIL_INDEX[subjectId] ?? []).filter(e => !e.sitting && e.year >= REVIEWED_ARCHIVE_FROM);
