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
  type ChairSubjectId,
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

// ── mismatch tracking: where the student's eye differs from the examiner's ──

/** One accumulated marking blind spot — a place the student systematically
 * marks differently from the examiner. `over` = too generous (awarded credit
 * the examiner withheld); `under` = too harsh (withheld credit the examiner
 * gave). Aggregated per subject + criterion, so "you over-credit the Link
 * mark" surfaces across every session that uses it. */
export interface MissTally {
  key: string;
  subject: ChairSubjectId;
  label: string;
  over: number;
  under: number;
  /** Session ids where this blind spot showed up (deduped, capped) — the drills. */
  sessions: string[];
  last: number;
}

/** A per-script contribution to the tally, before it's merged into state. */
export interface MissDelta {
  key: string;
  subject: ChairSubjectId;
  label: string;
  over: number;
  under: number;
  sessionId: string;
}

/** Per-criterion divergences for one marked grid script. */
export function gridScriptMisses(
  session: GridSession,
  script: GridScript,
  decisions: Record<string, boolean>,
): MissDelta[] {
  const acc = new Map<string, { over: number; under: number }>();
  for (const attempt of script.attempts) {
    for (const c of session.grid.perPoint) {
      const student = !!decisions[gridDecisionKey(attempt.id, c.id)];
      const keyAwarded = (attempt.key[c.id] ?? 0) > 0;
      if (student === keyAwarded) continue;
      const e = acc.get(c.label) ?? { over: 0, under: 0 };
      if (student && !keyAwarded) e.over += 1;
      else e.under += 1;
      acc.set(c.label, e);
    }
  }
  return [...acc].map(([label, v]) => ({
    key: `${session.subject}::${label}`,
    subject: session.subject,
    label,
    over: v.over,
    under: v.under,
    sessionId: session.id,
  }));
}

/** Generosity divergence for one marked scale script (too high vs too low). */
export function scaleScriptMisses(
  session: ScaleSession,
  script: ScaleScript,
  chosenLevelId: string | null,
): MissDelta[] {
  const levels = session.scale.levels;
  const keyIdx = levels.findIndex(l => l.id === script.keyLevelId);
  const chosenIdx = chosenLevelId === null ? -1 : levels.findIndex(l => l.id === chosenLevelId);
  if (chosenIdx < 0 || keyIdx < 0 || chosenIdx === keyIdx) return [];
  return [{
    key: `${session.subject}::scale-placement`,
    subject: session.subject,
    label: 'where you place the whole script on the scale',
    over: chosenIdx > keyIdx ? 1 : 0,
    under: chosenIdx < keyIdx ? 1 : 0,
    sessionId: session.id,
  }];
}

/** Merge a session's worth of miss deltas into the persisted tally (pure). */
export function mergeMisses(state: ChairState, deltas: MissDelta[], now: number): ChairState {
  if (deltas.length === 0) return state;
  const misses = { ...state.misses };
  for (const d of deltas) {
    const cur = misses[d.key] ?? { key: d.key, subject: d.subject, label: d.label, over: 0, under: 0, sessions: [], last: 0 };
    misses[d.key] = {
      ...cur,
      over: cur.over + d.over,
      under: cur.under + d.under,
      sessions: cur.sessions.includes(d.sessionId) ? cur.sessions : [...cur.sessions, d.sessionId].slice(-12),
      last: now,
    };
  }
  return { ...state, misses };
}

/** The student's biggest blind spots, most-frequent first. */
export function topMisses(state: ChairState, n = 8): MissTally[] {
  return Object.values(state.misses)
    .filter(m => m.over + m.under > 0)
    .sort((a, b) => (b.over + b.under) - (a.over + a.under) || b.last - a.last)
    .slice(0, n);
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
  /** Accumulated marking blind spots, keyed by subject::criterion. */
  misses: Record<string, MissTally>;
}

const EMPTY: ChairState = { results: {}, codex: [], codexOnCards: [], misses: {} };
const key = (uid?: string) => `chair:${uid || 'anon'}`;

const fresh = (): ChairState => ({ ...EMPTY, results: {}, codex: [], codexOnCards: [], misses: {} });

export function loadChair(uid?: string): ChairState {
  try {
    const raw = localStorage.getItem(key(uid));
    if (!raw) return fresh();
    const parsed = JSON.parse(raw) as Partial<ChairState>;
    return {
      results: parsed.results ?? {},
      codex: parsed.codex ?? [],
      codexOnCards: parsed.codexOnCards ?? [],
      misses: parsed.misses ?? {},
    };
  } catch {
    return fresh();
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
