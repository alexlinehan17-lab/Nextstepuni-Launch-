/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guidance-Counsellor cohort tags (feature E8). A counsellor's private working
 * annotations — DEIS / At-risk / Priority — used to filter the practice RAG
 * grid to the students they most need to watch. Stored locally per school+GC
 * (these are the counsellor's own labels, not student-visible data), so no
 * change to Firestore or its security rules is required.
 */

export const COHORT_TAGS = ['DEIS', 'At-risk', 'Priority'] as const;
export type CohortTag = (typeof COHORT_TAGS)[number];

const keyFor = (school: string) => `gc:cohortTags:${school}`;

type TagMap = Record<string, string[]>;

const read = (school: string): TagMap => {
  try {
    const raw = localStorage.getItem(keyFor(school));
    return raw ? (JSON.parse(raw) as TagMap) : {};
  } catch {
    return {};
  }
};
const write = (school: string, map: TagMap) => {
  try {
    localStorage.setItem(keyFor(school), JSON.stringify(map));
  } catch {
    /* private mode — degrade silently */
  }
};

export function getTags(school: string, uid: string): string[] {
  return read(school)[uid] ?? [];
}

/** Toggle a tag on a student; returns the fresh tag list for that student. */
export function toggleTag(school: string, uid: string, tag: CohortTag): string[] {
  const map = read(school);
  const cur = new Set(map[uid] ?? []);
  if (cur.has(tag)) cur.delete(tag);
  else cur.add(tag);
  map[uid] = [...cur];
  if (map[uid].length === 0) delete map[uid];
  write(school, map);
  return map[uid] ?? [];
}
