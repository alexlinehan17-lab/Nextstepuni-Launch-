/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Last-visited store — powers the home page "Pick up where you left off"
 * card. One record per account (localStorage), overwritten on every module
 * or tool open. Deliberately tiny: the card only ever shows the single most
 * recent place, so we never keep history here (Paper Trail keeps its own
 * richer recents list).
 */

export interface LastVisit {
  kind: 'module' | 'tool';
  /** moduleId (moduleRegistry) or toolId (InnovationZone). */
  id: string;
  /** Display title, e.g. "Mastering Active Recall" or "Paper Trail". */
  label: string;
  /** Optional detail line, e.g. "Section 3 of 7" or "Biology · 2023 · Higher". */
  sub?: string;
  at: number;
}

const KEY = 'nsu-lastvisit:';

export const recordVisit = (uid: string | undefined, v: Omit<LastVisit, 'at'>): void => {
  try {
    localStorage.setItem(KEY + (uid || 'anon'), JSON.stringify({ ...v, at: Date.now() }));
  } catch { /* private mode */ }
};

export const getLastVisit = (uid: string | undefined): LastVisit | null => {
  try {
    const raw = localStorage.getItem(KEY + (uid || 'anon'));
    if (!raw) return null;
    const v = JSON.parse(raw) as LastVisit;
    if (!v || typeof v.id !== 'string' || typeof v.label !== 'string' || (v.kind !== 'module' && v.kind !== 'tool')) return null;
    return v;
  } catch {
    return null;
  }
};
