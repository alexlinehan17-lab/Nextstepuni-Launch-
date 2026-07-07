/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — local recents + pinned papers (quality-of-life wave).
 *
 * localStorage, per uid, so the rails work offline and never depend on a
 * Firestore round-trip. Entries carry only the paper's identity (the composite
 * recentKey pieces) + a display label; the live PaperItem is re-resolved from
 * PAPER_TRAIL_INDEX at open time, so stored data can never go stale against a
 * re-generated index.
 *
 * Pure functions over storage — unit-tested in test/ptRecentsStore.test.ts.
 */

import { type PaperLang, type PaperLevel } from '../../types/paperTrail';

/** Identity + display info for one opened/pinned paper. */
export interface PaperRef {
  /** Composite recentKey: `${subjectId}|${year}|${level}|${lang}|${fileid}`. */
  key: string;
  subjectId: string;
  year: number;
  level: PaperLevel;
  lang: PaperLang;
  fileid: string;
  /** Human label, e.g. "Paper One". */
  label: string;
  /** Which side was open when recorded (recents only; pins default 'paper'). */
  kind: 'paper' | 'scheme';
  /** Epoch ms — last opened (recents) / pinned (pins). */
  at: number;
}

const RECENTS_PREFIX = 'nsu-pt-recents:';
const PINS_PREFIX = 'nsu-pt-pins:';

export const MAX_RECENTS = 6;
export const MAX_PINS = 12;

const storageKey = (prefix: string, uid?: string) => prefix + (uid || 'anon');

const readList = (prefix: string, uid?: string): PaperRef[] => {
  try {
    const raw = localStorage.getItem(storageKey(prefix, uid));
    if (!raw) return [];
    const list = JSON.parse(raw) as PaperRef[];
    if (!Array.isArray(list)) return [];
    return list.filter(
      r =>
        r &&
        typeof r.key === 'string' &&
        typeof r.subjectId === 'string' &&
        typeof r.fileid === 'string' &&
        typeof r.label === 'string' &&
        Number.isFinite(r.year),
    );
  } catch {
    return [];
  }
};

const writeList = (prefix: string, uid: string | undefined, list: PaperRef[]) => {
  try {
    localStorage.setItem(storageKey(prefix, uid), JSON.stringify(list));
  } catch {
    /* quota / private mode — degrade silently */
  }
};

/** Recents, newest first (≤ MAX_RECENTS). */
export const listRecentOpens = (uid?: string): PaperRef[] => readList(RECENTS_PREFIX, uid);

/** Record that a paper was actually opened in the viewer. Dedupes by key,
 *  newest first, capped. */
export function recordRecentOpen(
  uid: string | undefined,
  entry: Omit<PaperRef, 'at'>,
  now: number,
): PaperRef[] {
  const next = [
    { ...entry, at: now },
    ...readList(RECENTS_PREFIX, uid).filter(r => r.key !== entry.key),
  ].slice(0, MAX_RECENTS);
  writeList(RECENTS_PREFIX, uid, next);
  return next;
}

/** Pinned papers, most recently pinned first (≤ MAX_PINS). */
export const listPins = (uid?: string): PaperRef[] => readList(PINS_PREFIX, uid);

export const isPinned = (uid: string | undefined, key: string): boolean =>
  readList(PINS_PREFIX, uid).some(r => r.key === key);

/** Toggle a paper's pin. Returns the NEW pinned state (true = now pinned). */
export function togglePin(
  uid: string | undefined,
  entry: Omit<PaperRef, 'at'>,
  now: number,
): boolean {
  const pins = readList(PINS_PREFIX, uid);
  if (pins.some(r => r.key === entry.key)) {
    writeList(PINS_PREFIX, uid, pins.filter(r => r.key !== entry.key));
    return false;
  }
  writeList(PINS_PREFIX, uid, [{ ...entry, at: now }, ...pins].slice(0, MAX_PINS));
  return true;
}
