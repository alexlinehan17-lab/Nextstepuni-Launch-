/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * School-staff cohort tags (feature E8) — DEIS / At-risk / Priority working
 * annotations used to filter the practice RAG grid.
 *
 * SECURITY (review 2026-07-16, M-8): these are welfare-sensitive labels about
 * minors and were previously kept in plaintext browser localStorage — readable
 * on a shared staff machine, never cleared on logout, and outside the DSAR
 * cascade. They now live in Firestore at cohortTags/{school}, gated by the
 * rules to school staff of that school (isSchoolStaff() + same school), and are
 * removed by the GDPR erasure cascade (functions/src/dataRights.ts).
 *
 * The public read API stays synchronous (getTags) so callers don't have to
 * thread promises through render: it reads an in-memory cache that
 * loadCohortTags() hydrates from Firestore once per school. Writes (toggleTag)
 * are async — they update the cache and persist to Firestore.
 */

import { doc, getDoc, setDoc } from 'firebase/firestore';
import { db } from '../../firebase';
import { saveInBackground } from '../../utils/firestoreWrite';

export const COHORT_TAGS = ['DEIS', 'At-risk', 'Priority'] as const;
export type CohortTag = (typeof COHORT_TAGS)[number];

type TagMap = Record<string, string[]>;

// In-memory cache per school, hydrated by loadCohortTags().
const cache = new Map<string, TagMap>();

const legacyKeyFor = (school: string) => `gc:cohortTags:${school}`;

/**
 * Load a school's tag map from Firestore into the cache. Call once when the
 * dashboard mounts. One-time migration: if Firestore is empty but legacy
 * localStorage data exists (pre-M-8), migrate it up and clear the local copy.
 */
export async function loadCohortTags(school: string): Promise<TagMap> {
  try {
    const snap = await getDoc(doc(db, 'cohortTags', school));
    let map: TagMap = snap.exists() ? ((snap.data()?.tags as TagMap) ?? {}) : {};

    if (!snap.exists() || Object.keys(map).length === 0) {
      // Best-effort migration of any legacy local data.
      try {
        const raw = localStorage.getItem(legacyKeyFor(school));
        if (raw) {
          const legacy = JSON.parse(raw) as TagMap;
          if (legacy && Object.keys(legacy).length > 0) {
            map = legacy;
            // Fire, don't await — this runs inside the dashboard's initial
            // load, and an unsettled write would stall the whole tag load.
            saveInBackground(setDoc(doc(db, 'cohortTags', school), { tags: map }),
              'cohortTags.migrateLegacy', undefined, { silent: true });
          }
          localStorage.removeItem(legacyKeyFor(school));
        }
      } catch { /* ignore migration failures */ }
    }

    cache.set(school, map);
    return map;
  } catch (err) {
    console.error('[cohortTags] failed to load:', err);
    cache.set(school, cache.get(school) ?? {});
    return cache.get(school)!;
  }
}

export function getTags(school: string, uid: string): string[] {
  return cache.get(school)?.[uid] ?? [];
}

/**
 * Toggle a tag on a student; returns the fresh list synchronously (optimistic
 * cache update) and persists to Firestore in the background. The persist is
 * fire-and-forget so the UI updates instantly and never blocks on the network.
 */
export function toggleTag(school: string, uid: string, tag: CohortTag): string[] {
  const map = { ...(cache.get(school) ?? {}) };
  const cur = new Set(map[uid] ?? []);
  if (cur.has(tag)) cur.delete(tag);
  else cur.add(tag);
  const next = [...cur];
  if (next.length === 0) delete map[uid];
  else map[uid] = next;
  cache.set(school, map);
  // Full-doc write (not merge): the doc holds only `tags`, and merge would not
  // persist removals (a merge never deletes map keys absent from the payload).
  // Wrapped so neither a synchronous doc() throw nor an async write rejection
  // can disturb the optimistic cache update / return value.
  try {
    setDoc(doc(db, 'cohortTags', school), { tags: map }).catch(err => console.error('[cohortTags] failed to save:', err));
  } catch (err) {
    console.error('[cohortTags] persist skipped:', err);
  }
  return map[uid] ?? [];
}

/** Test-only: reset the in-memory cache between test cases. */
export function _resetCohortCacheForTests(): void {
  cache.clear();
}
