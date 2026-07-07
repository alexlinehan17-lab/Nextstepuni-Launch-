/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — save-and-exit for marking sessions.
 *
 * If the bell rings mid-session (tab closed, back button, battery), the desk
 * shouldn't be lost. A single resume slot per uid holds everything needed to
 * put the desk back exactly where it was: which session, which script, every
 * marking decision so far, the running scores/blind-spots, and elapsed time.
 * Written on every decision, cleared on completion or an explicit "Start
 * over". localStorage per account, `now` injected — same persistence shape as
 * ./store.
 */

import { type MissDelta, type ScriptScore } from './store';

/** Structurally identical to cohortSync's DecisionDelta, declared locally so
 * this module (and its tests) never touch the Firestore layer. */
export interface ResumeDecisionDelta {
  sessionId: string;
  scriptId: string;
  choice: string;
}

export interface ChairResumeSnapshot {
  /** Schema version — bump on breaking shape changes; old slots are dropped. */
  v: 1;
  sessionId: string;
  /** Denormalised for the resume card, so it renders without a data lookup. */
  sessionTitle: string;
  stage: 'mark' | 'reveal';
  scriptIdx: number;
  /** How many scripts this run is marking (after any drill filter). */
  scriptCount: number;
  decisions: Record<string, boolean>;
  chosenLevel: string | null;
  scores: ScriptScore[];
  misses: MissDelta[];
  decisionDeltas: ResumeDecisionDelta[];
  reason: string;
  borderlineOnly: boolean;
  dailyMode: boolean;
  restrictScriptId: string | null;
  elapsedMs: number;
  savedAt: number;
}

/** A saved place older than this is stale — the moment has passed. */
export const RESUME_STALE_MS = 7 * 86_400_000;

const key = (uid?: string) => `chair-resume:${uid || 'anon'}`;

/** Is there anything on the desk worth saving? (No point offering to resume a
 * session where not a single call has been made yet.) */
export function hasResumableProgress(snap: {
  scores: ScriptScore[];
  decisions: Record<string, boolean>;
  chosenLevel: string | null;
}): boolean {
  return snap.scores.length > 0 || Object.keys(snap.decisions).length > 0 || snap.chosenLevel !== null;
}

/** Persist the in-flight session (quota / private mode degrade silently). */
export function saveResume(uid: string | undefined, snap: ChairResumeSnapshot): void {
  try {
    localStorage.setItem(key(uid), JSON.stringify(snap));
  } catch {
    /* quota / private mode — degrade silently */
  }
}

/** The saved place, or null when absent, malformed, stale, or empty-handed. */
export function loadResume(uid: string | undefined, now: number): ChairResumeSnapshot | null {
  try {
    const raw = localStorage.getItem(key(uid));
    if (!raw) return null;
    const p = JSON.parse(raw) as Partial<ChairResumeSnapshot>;
    if (
      p.v !== 1 ||
      typeof p.sessionId !== 'string' ||
      typeof p.sessionTitle !== 'string' ||
      (p.stage !== 'mark' && p.stage !== 'reveal') ||
      typeof p.scriptIdx !== 'number' ||
      typeof p.scriptCount !== 'number' ||
      typeof p.decisions !== 'object' || p.decisions === null ||
      !Array.isArray(p.scores) ||
      !Array.isArray(p.misses) ||
      !Array.isArray(p.decisionDeltas) ||
      typeof p.savedAt !== 'number'
    ) {
      return null;
    }
    if (now - p.savedAt > RESUME_STALE_MS) return null;
    return {
      v: 1,
      sessionId: p.sessionId,
      sessionTitle: p.sessionTitle,
      stage: p.stage,
      scriptIdx: p.scriptIdx,
      scriptCount: p.scriptCount,
      decisions: p.decisions as Record<string, boolean>,
      chosenLevel: typeof p.chosenLevel === 'string' ? p.chosenLevel : null,
      scores: p.scores as ScriptScore[],
      misses: p.misses as MissDelta[],
      decisionDeltas: p.decisionDeltas as ResumeDecisionDelta[],
      reason: typeof p.reason === 'string' ? p.reason : '',
      borderlineOnly: !!p.borderlineOnly,
      dailyMode: !!p.dailyMode,
      restrictScriptId: typeof p.restrictScriptId === 'string' ? p.restrictScriptId : null,
      elapsedMs: typeof p.elapsedMs === 'number' && p.elapsedMs >= 0 ? p.elapsedMs : 0,
      savedAt: p.savedAt,
    };
  } catch {
    return null;
  }
}

/** Drop the saved place (on completion or an explicit "Start over"). */
export function clearResume(uid?: string): void {
  try {
    localStorage.removeItem(key(uid));
  } catch {
    /* ignore */
  }
}

/** One quiet line for the resume card, e.g. "Script 2 of 4 · about 3 min in". */
export function describeResume(snap: ChairResumeSnapshot): string {
  const where = `Script ${Math.min(snap.scriptIdx, snap.scriptCount - 1) + 1} of ${snap.scriptCount}`;
  const mins = Math.round(snap.elapsedMs / 60_000);
  if (mins < 1) return `${where} · under a minute in`;
  return `${where} · about ${mins} min in`;
}
