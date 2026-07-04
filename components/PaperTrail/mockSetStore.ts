/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — custom mock-set store (feature B1). A student assembles their own
 * practice set from real past questions (a subject, some topics, a length); we
 * build a shuffled selection and persist it so it survives opening each paper.
 * The selection is a pure, seeded function so it is deterministic and testable —
 * the component passes a clock-derived seed at build time.
 */

import { type TopicSibling } from './topics';

export interface MockItem {
  q: TopicSibling;
  done: boolean;
}

export interface MockSet {
  subjectId: string;
  /** Human label, e.g. "Business · Mixed" or "Maths · Calculus". */
  label: string;
  createdTs: number;
  /** Target working time in minutes (a guide, not enforced). */
  targetMin: number;
  items: MockItem[];
}

// ─── pure seeded selection ──────────────────────────────────

/** Small deterministic PRNG (mulberry32) so a given seed always shuffles the
 *  same way — keeps set-building testable without a live clock. */
function mulberry32(seed: number): () => number {
  let a = seed >>> 0;
  return () => {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/** Choose `count` questions from `pool` using a seeded Fisher–Yates shuffle.
 *  Clamps to the pool size; returns fewer if the pool is small. Pure. */
export function buildSet(pool: TopicSibling[], count: number, seed: number): TopicSibling[] {
  const arr = pool.slice();
  const rnd = mulberry32(seed);
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(rnd() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr.slice(0, Math.max(0, Math.min(count, arr.length)));
}

// ─── persistence (one current set per uid) ──────────────────

const PREFIX = 'pt:mockset:';
const blobKey = (uid?: string) => PREFIX + (uid || 'anon');

export function loadSet(uid?: string): MockSet | null {
  try {
    const raw = localStorage.getItem(blobKey(uid));
    return raw ? (JSON.parse(raw) as MockSet) : null;
  } catch {
    return null;
  }
}

export function saveSet(uid: string | undefined, set: MockSet): void {
  try {
    localStorage.setItem(blobKey(uid), JSON.stringify(set));
  } catch {
    /* quota / private mode — degrade silently */
  }
}

export function clearSet(uid?: string): void {
  try {
    localStorage.removeItem(blobKey(uid));
  } catch {
    /* ignore */
  }
}

export function toggleDone(uid: string | undefined, index: number): MockSet | null {
  const set = loadSet(uid);
  if (!set || !set.items[index]) return set;
  set.items[index] = { ...set.items[index], done: !set.items[index].done };
  saveSet(uid, set);
  return set;
}
