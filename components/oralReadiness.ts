/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Readiness-delta helpers for the Oral Exam Trainer (feature F8): a light
 * spaced re-record schedule (mirroring the CODEX_INTERVALS ladder in
 * ExaminersChair/store.ts), a neutral words-per-minute pace estimate, and the
 * tiny on-device stores that back them. The pure schedule/WPM functions are
 * exported for unit testing (test/oralReadiness.test.ts).
 *
 * Privacy is absolute here: recording audio lives ONLY on the device — at most
 * the previous + latest take per oral part in this browser's IndexedDB, with
 * timestamps in localStorage. Nothing is ever uploaded, shared, or written to
 * Firestore.
 */

export const DAY_MS = 86_400_000;

/** Days until a part resurfaces for a re-record, indexed by takes made so far
 * (1st take → 1 day, then 3, 8, 21 — a lighter cut of the codex ladder). */
export const RERECORD_INTERVALS = [1, 3, 8, 21];

/** Metadata for one kept take. Audio blob itself lives in IndexedDB. */
export interface TakeMeta {
  /** When the take was recorded (ms epoch). */
  at: number;
  /** Recording length (ms). */
  durationMs: number;
}

/** How many takes we keep per part: the previous one and the latest. */
export const MAX_TAKES_PER_PART = 2;

/** Days before a part is due again, given how many takes it has. */
export const intervalDaysFor = (takeCount: number): number =>
  RERECORD_INTERVALS[Math.min(Math.max(takeCount, 1), RERECORD_INTERVALS.length) - 1];

/** A part is due for a re-record when its newest recording is older than its
 * interval. A never-recorded part is not "due" — there is nothing to re-record. */
export const isDueForRerecord = (
  lastRecordedAt: number | undefined,
  takeCount: number,
  now: number
): boolean =>
  takeCount > 0 &&
  lastRecordedAt !== undefined &&
  now - lastRecordedAt >= intervalDaysFor(takeCount) * DAY_MS;

/** Whole days between two timestamps (rounded, never negative). */
export const daysBetween = (earlier: number, later: number): number =>
  Math.max(0, Math.round((later - earlier) / DAY_MS));

/** "today" / "yesterday" / "N days ago" — calm label for take ages. */
export const daysAgoLabel = (recordedAt: number, now: number): string => {
  const d = daysBetween(recordedAt, now);
  return d === 0 ? 'today' : d === 1 ? 'yesterday' : `${d} days ago`;
};

// ── pace (words per minute) ──

/** Words in a script/prompt — whitespace-separated tokens. */
export const wordCount = (text: string): number => {
  const trimmed = text.trim();
  return trimmed ? trimmed.split(/\s+/).length : 0;
};

/** Minimum recording length before a WPM estimate is meaningful. */
export const MIN_PACE_DURATION_MS = 3_000;

/** Estimated words per minute, or null when there's nothing sound to estimate
 * from (no script words, or a clip too short to divide by). */
export const estimateWpm = (words: number, durationMs: number): number | null =>
  words > 0 && durationMs >= MIN_PACE_DURATION_MS
    ? Math.round(words / (durationMs / 60_000))
    : null;

/** Comfortable spoken range. Outside it we only *note* the pace in muted text
 * — never a judgment colour. */
export const PACE_COMFORT = { min: 100, max: 160 };

/** Neutral pace note: 'quick', 'unhurried', or null when comfortably in range. */
export const paceNote = (wpm: number): 'quick' | 'unhurried' | null =>
  wpm > PACE_COMFORT.max ? 'quick' : wpm < PACE_COMFORT.min ? 'unhurried' : null;

// ── take metadata store (localStorage, timestamps only — no audio) ──

const tKey = (uid?: string) => `oral:takes:${uid || 'anon'}`;

export const loadTakeMeta = (uid?: string): Record<string, TakeMeta[]> => {
  try {
    const raw = localStorage.getItem(tKey(uid));
    return raw ? JSON.parse(raw) : {};
  } catch {
    return {};
  }
};

export const saveTakeMeta = (uid: string | undefined, meta: Record<string, TakeMeta[]>) => {
  try {
    localStorage.setItem(tKey(uid), JSON.stringify(meta));
  } catch {
    /* ignore */
  }
};

/** Append a take to a part's history, keeping only the previous + latest (pure). */
export const appendTake = (
  meta: Record<string, TakeMeta[]>,
  partId: string,
  take: TakeMeta
): Record<string, TakeMeta[]> => ({
  ...meta,
  [partId]: [...(meta[partId] ?? []), take].slice(-MAX_TAKES_PER_PART),
});

// ── take audio store (IndexedDB, on-device only) ──
// Value per key is Blob[] (oldest → newest, max 2), keyed `${uid}:${partId}`.
// Every operation is best-effort: if IndexedDB is unavailable the trainer
// degrades to the old in-memory-only behaviour.

const DB_NAME = 'oral-trainer-takes';
const DB_STORE = 'takes';

const openTakeDb = (): Promise<IDBDatabase> =>
  new Promise((resolve, reject) => {
    if (typeof indexedDB === 'undefined') {
      reject(new Error('IndexedDB unavailable'));
      return;
    }
    const req = indexedDB.open(DB_NAME, 1);
    req.onupgradeneeded = () => {
      if (!req.result.objectStoreNames.contains(DB_STORE)) req.result.createObjectStore(DB_STORE);
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error ?? new Error('IndexedDB open failed'));
  });

/** Load a part's kept takes (oldest → newest). Empty array on any failure. */
export const loadTakeBlobs = async (uid: string | undefined, partId: string): Promise<Blob[]> => {
  try {
    const db = await openTakeDb();
    return await new Promise<Blob[]>(resolve => {
      const tx = db.transaction(DB_STORE, 'readonly');
      const req = tx.objectStore(DB_STORE).get(`${uid || 'anon'}:${partId}`);
      req.onsuccess = () => resolve(Array.isArray(req.result) ? (req.result as Blob[]) : []);
      req.onerror = () => resolve([]);
      tx.oncomplete = () => db.close();
    });
  } catch {
    return [];
  }
};

/** Persist a part's takes on-device, pruning to the previous + latest. */
export const saveTakeBlobs = async (
  uid: string | undefined,
  partId: string,
  blobs: Blob[]
): Promise<void> => {
  try {
    const db = await openTakeDb();
    await new Promise<void>(resolve => {
      const tx = db.transaction(DB_STORE, 'readwrite');
      tx.objectStore(DB_STORE).put(blobs.slice(-MAX_TAKES_PER_PART), `${uid || 'anon'}:${partId}`);
      tx.oncomplete = () => {
        db.close();
        resolve();
      };
      tx.onerror = () => {
        db.close();
        resolve();
      };
    });
  } catch {
    /* keep in-memory only — same behaviour as before this feature */
  }
};
