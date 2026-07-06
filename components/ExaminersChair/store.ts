/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — result store + calibration core.
 *
 * Pure scoring functions (unit-tested) with a thin localStorage persistence
 * layer, per uid, `now` injected by callers — same shape as the Paper Trail
 * stores.
 *
 * "Agreement" is the tool's core metric: how closely the student's marking
 * decisions match the examiner's key. Grid sessions compare per-criterion
 * decisions; scale sessions compare the chosen credit level (an adjacent level
 * counts half — being one rung off is a much smaller miss than calling a
 * no-credit script full marks).
 */

import {
  type GridScript,
  type GridSession,
  type MarkingSession,
  type ScaleScript,
  type ScaleSession,
} from '../../data/examinersChair';

// ── decision keys ──

/** Key for one grid decision: did this attempt earn this criterion? */
export const gridDecisionKey = (attemptId: string, criterionId: string) => `${attemptId}:${criterionId}`;

// ── pure scoring ──

export interface ScriptScore {
  scriptId: string;
  /** 0..1 — proportion of marking decisions that matched the examiner. */
  agreement: number;
  /** Total marks the student awarded the script. */
  studentMarks: number;
  /** Total marks the examiner's key awards the script. */
  examinerMarks: number;
  /** Maximum marks available for the script. */
  maxMarks: number;
}

/** Score a grid script against the student's per-criterion decisions. */
export function scoreGridScript(
  session: GridSession,
  script: GridScript,
  decisions: Record<string, boolean>,
): ScriptScore {
  let matched = 0;
  let total = 0;
  let studentMarks = 0;
  let examinerMarks = 0;
  let maxMarks = 0;
  for (const attempt of script.attempts) {
    for (const c of session.grid.perPoint) {
      total += 1;
      maxMarks += c.marks;
      const studentAwarded = !!decisions[gridDecisionKey(attempt.id, c.id)];
      const keyAwarded = (attempt.key[c.id] ?? 0) > 0;
      if (studentAwarded === keyAwarded) matched += 1;
      if (studentAwarded) studentMarks += c.marks;
      if (keyAwarded) examinerMarks += attempt.key[c.id];
    }
  }
  return {
    scriptId: script.id,
    agreement: total === 0 ? 0 : matched / total,
    studentMarks,
    examinerMarks,
    maxMarks,
  };
}

/** Score a scale script against the student's chosen credit level. */
export function scoreScaleScript(
  session: ScaleSession,
  script: ScaleScript,
  chosenLevelId: string | null,
): ScriptScore {
  const levels = session.scale.levels;
  const keyIdx = levels.findIndex(l => l.id === script.keyLevelId);
  const chosenIdx = chosenLevelId === null ? -1 : levels.findIndex(l => l.id === chosenLevelId);
  const maxMarks = levels[levels.length - 1]?.marks ?? 0;
  const examinerMarks = keyIdx >= 0 ? levels[keyIdx].marks : 0;
  const studentMarks = chosenIdx >= 0 ? levels[chosenIdx].marks : 0;
  let agreement = 0;
  if (chosenIdx >= 0 && keyIdx >= 0) {
    if (chosenIdx === keyIdx) agreement = 1;
    else if (Math.abs(chosenIdx - keyIdx) === 1) agreement = 0.5;
  }
  return { scriptId: script.id, agreement, studentMarks, examinerMarks, maxMarks };
}

// ── session results + persistence ──

export interface SessionResult {
  sessionId: string;
  /** 0..1 mean agreement across the session's scripts (latest attempt). */
  agreement: number;
  scripts: ScriptScore[];
  completedAt: number;
  /** How many times the session has been completed (retakes overwrite scores). */
  attempts: number;
}

export interface ChairState {
  results: Record<string, SessionResult>;
  /** Earned codex rule ids, in the order they were earned. */
  codex: string[];
  /** Codex rule ids already pushed to Paper Trail flashcards. */
  codexOnCards: string[];
}

const EMPTY: ChairState = { results: {}, codex: [], codexOnCards: [] };
const key = (uid?: string) => `chair:${uid || 'anon'}`;

export function loadChair(uid?: string): ChairState {
  try {
    const raw = localStorage.getItem(key(uid));
    if (!raw) return { ...EMPTY, results: {}, codex: [], codexOnCards: [] };
    const parsed = JSON.parse(raw) as Partial<ChairState>;
    return {
      results: parsed.results ?? {},
      codex: parsed.codex ?? [],
      codexOnCards: parsed.codexOnCards ?? [],
    };
  } catch {
    return { ...EMPTY, results: {}, codex: [], codexOnCards: [] };
  }
}

export function saveChair(uid: string | undefined, state: ChairState): void {
  try {
    localStorage.setItem(key(uid), JSON.stringify(state));
  } catch {
    /* quota / private mode — degrade silently */
  }
}

/** Record a completed session (pure — returns the next state). */
export function completeSession(
  state: ChairState,
  session: MarkingSession,
  scripts: ScriptScore[],
  now: number,
): ChairState {
  const agreement = scripts.length === 0 ? 0 : scripts.reduce((a, s) => a + s.agreement, 0) / scripts.length;
  const prev = state.results[session.id];
  const result: SessionResult = {
    sessionId: session.id,
    agreement,
    scripts,
    completedAt: now,
    attempts: (prev?.attempts ?? 0) + 1,
  };
  const codex = state.codex.includes(session.takeaway.id) ? state.codex : [...state.codex, session.takeaway.id];
  return { ...state, results: { ...state.results, [session.id]: result }, codex };
}

/** Mark a codex rule as pushed to flashcards (pure). */
export function markCodexOnCards(state: ChairState, ruleId: string): ChairState {
  if (state.codexOnCards.includes(ruleId)) return state;
  return { ...state, codexOnCards: [...state.codexOnCards, ruleId] };
}

/** Overall calibration, 0..1 — mean of latest agreement across completed sessions. */
export function overallCalibration(state: ChairState): number | null {
  const rs = Object.values(state.results);
  if (rs.length === 0) return null;
  return rs.reduce((a, r) => a + r.agreement, 0) / rs.length;
}

/** Display helper: 0..1 → whole-percent string. */
export const pct = (x: number) => `${Math.round(x * 100)}%`;

/** Calibration band label for the home screen. */
export function calibrationBand(agreement: number): string {
  if (agreement >= 0.9) return 'Examiner-sharp';
  if (agreement >= 0.75) return 'Well calibrated';
  if (agreement >= 0.55) return 'Getting there';
  return 'Marking optimist';
}
