/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — local persistence for the attempt tools (Tier 2 triage + Tier 3
 * self-marking). Stored in localStorage (per device, works offline) keyed by a
 * paper namespace `ns` = `uid|subjectId|year|level|lang|fileid`.
 *
 * The self-mark scores also feed a cross-paper, topic-aware weakness map, so
 * `allMarks()` parses every stored paper back to its identity + question.
 */

export type TriageRating = 'g' | 'a' | 'r';
export type GapKind = 'content' | 'process' | 'careless' | 'timing';

export interface SelfMark {
  /** Marks the student awarded themselves. */
  score: number;
  /** Marks available for the question (from the marks token / scheme). */
  max: number;
  /** What kind of gap the loss was — drives the reflection. */
  gap?: GapKind;
  /** Epoch ms — set by the caller (Date.now is unavailable in some contexts). */
  ts: number;
}

interface PaperAttempt {
  triage?: Record<string, TriageRating>;
  marks?: Record<string, SelfMark>;
}

const PREFIX = 'pt:attempt:';
const key = (ns: string) => PREFIX + ns;

const read = (ns: string): PaperAttempt => {
  try {
    const raw = localStorage.getItem(key(ns));
    return raw ? (JSON.parse(raw) as PaperAttempt) : {};
  } catch {
    return {};
  }
};
const write = (ns: string, v: PaperAttempt) => {
  try {
    localStorage.setItem(key(ns), JSON.stringify(v));
  } catch {
    /* quota / private mode — silently degrade */
  }
};

export const loadAttempt = (ns: string): PaperAttempt => read(ns);

export function setTriage(ns: string, n: string, rating: TriageRating | null): PaperAttempt {
  const v = read(ns);
  v.triage ||= {};
  if (rating) v.triage[n] = rating;
  else delete v.triage[n];
  write(ns, v);
  return v;
}

export function setMark(ns: string, n: string, mark: SelfMark | null): PaperAttempt {
  const v = read(ns);
  v.marks ||= {};
  if (mark) v.marks[n] = mark;
  else delete v.marks[n];
  write(ns, v);
  return v;
}

/** Build a paper namespace. uid keeps it per-student on shared devices. */
export const attemptNs = (
  uid: string | undefined,
  subjectId: string,
  year: number,
  level: string,
  lang: string,
  fileid: string,
) => `${uid || 'anon'}|${subjectId}|${year}|${level}|${lang}|${fileid}`;

export interface StoredMark extends SelfMark {
  uid: string;
  subjectId: string;
  year: number;
  level: string;
  lang: string;
  fileid: string;
  n: string;
}

/** Every self-mark across every paper — for the weakness map. Filtered to the
 *  current uid when one is given. */
export function allMarks(uid?: string): StoredMark[] {
  const out: StoredMark[] = [];
  let n: number;
  try {
    n = localStorage.length;
  } catch {
    return out;
  }
  for (let i = 0; i < n; i++) {
    const k = localStorage.key(i);
    if (!k || !k.startsWith(PREFIX)) continue;
    const ns = k.slice(PREFIX.length);
    const [u, subjectId, year, level, lang, fileid] = ns.split('|');
    if (uid && u !== uid) continue;
    if (!subjectId || !fileid) continue;
    let v: PaperAttempt;
    try {
      v = JSON.parse(localStorage.getItem(k) || '{}');
    } catch {
      continue;
    }
    for (const [q, m] of Object.entries(v.marks ?? {})) {
      out.push({ ...m, uid: u, subjectId, year: Number(year), level, lang, fileid, n: q });
    }
  }
  return out;
}
