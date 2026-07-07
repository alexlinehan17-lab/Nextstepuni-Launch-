/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — Full Loop save-and-exit. When a student leaves mid-loop (exits
 * the paper, closes the tab, or the viewer unmounts) their place is persisted
 * so the next open of that same paper offers a one-tap resume.
 *
 * Keyed by the paper's attempt namespace (`uid|subjectId|year|level|lang|fileid`),
 * so it is per-account AND per-paper by construction. Per-question self-marks
 * already persist independently in attemptStore — this module only carries the
 * loop position + elapsed time.
 *
 * Unit-tested in test/ptLoopResume.test.ts.
 */

export interface LoopPlace {
  /** 0-based index of the question the student was on. */
  idx: number;
  /** Question count of the answer map when saved — guards a re-generated map. */
  total: number;
  /** Whole-loop elapsed seconds so far (resume restarts the clock from here). */
  elapsedSec: number;
  /** Questions self-marked so far (informational, shown on the resume card). */
  marked: number;
  /** Epoch ms saved. */
  savedAt: number;
}

const PREFIX = 'nsu-pt-loop:';

/** Saved places older than this are stale — a fortnight later, "question 4"
 *  means nothing; start fresh. */
export const LOOP_PLACE_MAX_AGE_MS = 14 * 24 * 60 * 60 * 1000;

const key = (ns: string) => PREFIX + ns;

export function saveLoopPlace(ns: string, place: Omit<LoopPlace, 'savedAt'>, now: number): void {
  try {
    localStorage.setItem(key(ns), JSON.stringify({ ...place, savedAt: now }));
  } catch {
    /* quota / private mode — degrade silently */
  }
}

export function loadLoopPlace(ns: string, now: number): LoopPlace | null {
  try {
    const raw = localStorage.getItem(key(ns));
    if (!raw) return null;
    const p = JSON.parse(raw) as LoopPlace;
    if (
      !p ||
      !Number.isInteger(p.idx) ||
      p.idx < 0 ||
      !Number.isInteger(p.total) ||
      p.total < 1 ||
      p.idx >= p.total ||
      !Number.isFinite(p.savedAt)
    )
      return null;
    if (now - p.savedAt > LOOP_PLACE_MAX_AGE_MS) {
      clearLoopPlace(ns);
      return null;
    }
    return {
      ...p,
      elapsedSec: Number.isFinite(p.elapsedSec) && p.elapsedSec > 0 ? p.elapsedSec : 0,
      marked: Number.isInteger(p.marked) && p.marked > 0 ? p.marked : 0,
    };
  } catch {
    return null;
  }
}

export function clearLoopPlace(ns: string): void {
  try {
    localStorage.removeItem(key(ns));
  } catch {
    /* ignore */
  }
}
