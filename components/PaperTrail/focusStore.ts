/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — focus sessions (feature E7). A focus timer that grows a calm
 * visual artifact tied to real study time; completed sessions are kept as a
 * "grove" the student builds over time. This is Self-Determination-Theory
 * motivation (competence, autonomy) rather than points chasing — effort made
 * visible. Persisted per uid; `now` injected by the caller.
 */

import { dayKey } from './streakStore';

export interface FocusRecord {
  /** Epoch ms the session completed. */
  ts: number;
  /** Length of the completed session, minutes. */
  minutes: number;
  /** Deterministic seed for the artifact's shape. */
  seed: number;
}

const PREFIX = 'pt:focus:';
const blobKey = (uid?: string) => PREFIX + (uid || 'anon');

const read = (uid?: string): FocusRecord[] => {
  try {
    const raw = localStorage.getItem(blobKey(uid));
    return raw ? (JSON.parse(raw) as FocusRecord[]) : [];
  } catch {
    return [];
  }
};
const write = (uid: string | undefined, list: FocusRecord[]) => {
  try {
    localStorage.setItem(blobKey(uid), JSON.stringify(list));
  } catch {
    /* quota / private mode — degrade silently */
  }
};

/** The grove — completed sessions, newest first. */
export function loadGrove(uid?: string): FocusRecord[] {
  return read(uid).slice().sort((a, b) => b.ts - a.ts);
}

export function addSession(uid: string | undefined, minutes: number, seed: number, now: number): void {
  const list = read(uid);
  list.push({ ts: now, minutes, seed });
  write(uid, list);
}

export interface FocusStats {
  todayMinutes: number;
  sessions: number;
  totalMinutes: number;
}

export function focusStats(uid: string | undefined, now: number): FocusStats {
  const list = read(uid);
  const today = dayKey(now);
  return {
    todayMinutes: list.filter(r => dayKey(r.ts) === today).reduce((s, r) => s + r.minutes, 0),
    sessions: list.length,
    totalMinutes: list.reduce((s, r) => s + r.minutes, 0),
  };
}
