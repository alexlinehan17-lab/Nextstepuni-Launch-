/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Examiner's Chair — calibration core + content integrity tests.
 */

import { beforeEach, describe, expect, it } from 'vitest';
import {
  calibrationBand,
  completeSession,
  gridDecisionKey,
  borderlineScripts,
  codexDue,
  gridScriptMisses,
  isBorderlineScript,
  loadChair,
  reviewCodex,
  markCodexOnCards,
  mergeMisses,
  overallCalibration,
  saveChair,
  scaleScriptMisses,
  scoreGridScript,
  scoreScaleScript,
  topMisses,
  type ChairState,
} from '../components/ExaminersChair/store';
import { CHAIR_SUBJECTS, allSessions, findSession } from '../data/examinersChair';
import { type GridSession, type ScaleSession } from '../data/examinersChair';

const gridSession = (): GridSession => allSessions().find(s => s.mode === 'grid') as GridSession;
const scaleSession = (): ScaleSession => allSessions().find(s => s.mode === 'scale') as ScaleSession;

describe('scoreGridScript', () => {
  it('gives full agreement and matching marks when decisions mirror the key', () => {
    const session = gridSession();
    const script = session.scripts[0];
    const decisions: Record<string, boolean> = {};
    for (const attempt of script.attempts) {
      for (const c of session.grid.perPoint) {
        decisions[gridDecisionKey(attempt.id, c.id)] = (attempt.key[c.id] ?? 0) > 0;
      }
    }
    const score = scoreGridScript(session, script, decisions);
    expect(score.agreement).toBe(1);
    expect(score.studentMarks).toBe(score.examinerMarks);
  });

  it('gives zero agreement when every decision is inverted', () => {
    const session = gridSession();
    const script = session.scripts[0];
    const decisions: Record<string, boolean> = {};
    for (const attempt of script.attempts) {
      for (const c of session.grid.perPoint) {
        decisions[gridDecisionKey(attempt.id, c.id)] = !((attempt.key[c.id] ?? 0) > 0);
      }
    }
    const score = scoreGridScript(session, script, decisions);
    expect(score.agreement).toBe(0);
  });

  it('treats missing decisions as "not awarded"', () => {
    const session = gridSession();
    const script = session.scripts[0];
    const score = scoreGridScript(session, script, {});
    expect(score.studentMarks).toBe(0);
    // Agreement equals the share of criteria the key also left at zero.
    let zeros = 0;
    let total = 0;
    for (const attempt of script.attempts) {
      for (const c of session.grid.perPoint) {
        total += 1;
        if ((attempt.key[c.id] ?? 0) === 0) zeros += 1;
      }
    }
    expect(score.agreement).toBeCloseTo(zeros / total, 10);
  });
});

describe('scoreScaleScript', () => {
  it('scores exact level match as full agreement', () => {
    const session = scaleSession();
    const script = session.scripts[0];
    const score = scoreScaleScript(session, script, script.keyLevelId);
    expect(score.agreement).toBe(1);
    expect(score.studentMarks).toBe(score.examinerMarks);
  });

  it('scores an adjacent level as half agreement', () => {
    const session = scaleSession();
    const script = session.scripts[0];
    const keyIdx = session.scale.levels.findIndex(l => l.id === script.keyLevelId);
    const neighbour = session.scale.levels[keyIdx + 1] ?? session.scale.levels[keyIdx - 1];
    const score = scoreScaleScript(session, script, neighbour.id);
    expect(score.agreement).toBe(0.5);
  });

  it('scores a far-off level as zero agreement', () => {
    const session = scaleSession();
    // find a script whose key has a level ≥2 rungs away available
    for (const script of session.scripts) {
      const keyIdx = session.scale.levels.findIndex(l => l.id === script.keyLevelId);
      const far = session.scale.levels.find((_, i) => Math.abs(i - keyIdx) >= 2);
      if (far) {
        expect(scoreScaleScript(session, script, far.id).agreement).toBe(0);
        return;
      }
    }
    throw new Error('no scale session with a far-off level');
  });

  it('scores no choice as zero', () => {
    const session = scaleSession();
    const score = scoreScaleScript(session, session.scripts[0], null);
    expect(score.agreement).toBe(0);
    expect(score.studentMarks).toBe(0);
  });
});

describe('session results + calibration', () => {
  beforeEach(() => localStorage.clear());

  const fakeScores = (agreement: number) => [
    { scriptId: 'x', agreement, studentMarks: 1, examinerMarks: 2, maxMarks: 5 },
  ];

  it('records a result, earns the codex rule once, and counts retakes', () => {
    const session = gridSession();
    let state: ChairState = loadChair('u1');
    state = completeSession(state, session, fakeScores(0.8), 1000);
    expect(state.results[session.id].agreement).toBe(0.8);
    expect(state.results[session.id].attempts).toBe(1);
    expect(state.codex).toEqual([session.takeaway.id]);
    state = completeSession(state, session, fakeScores(1), 2000);
    expect(state.results[session.id].attempts).toBe(2);
    expect(state.codex).toEqual([session.takeaway.id]); // not duplicated
  });

  it('round-trips through localStorage', () => {
    const session = gridSession();
    let state = loadChair('u2');
    state = completeSession(state, session, fakeScores(0.5), 1000);
    saveChair('u2', state);
    const back = loadChair('u2');
    expect(back.results[session.id].agreement).toBe(0.5);
    expect(loadChair('other').results[session.id]).toBeUndefined();
  });

  it('overallCalibration averages across sessions and is null when empty', () => {
    expect(overallCalibration(loadChair('u3'))).toBeNull();
    const [a, b] = [gridSession(), scaleSession()];
    let state = loadChair('u3');
    state = completeSession(state, a, fakeScores(1), 1);
    state = completeSession(state, b, fakeScores(0.5), 2);
    expect(overallCalibration(state)).toBeCloseTo(0.75, 10);
  });

  it('markCodexOnCards is idempotent', () => {
    let state = loadChair('u4');
    state = markCodexOnCards(state, 'r1');
    state = markCodexOnCards(state, 'r1');
    expect(state.codexOnCards).toEqual(['r1']);
  });

  it('calibrationBand maps thresholds', () => {
    expect(calibrationBand(0.95)).toBe('Examiner-sharp');
    expect(calibrationBand(0.8)).toBe('Well calibrated');
    expect(calibrationBand(0.6)).toBe('Getting there');
    expect(calibrationBand(0.2)).toBe('Marking optimist');
  });
});

describe('mismatch tracking', () => {
  const miniGrid: GridSession = {
    mode: 'grid', id: 't-g', subject: 'business', level: 'higher', title: 'Mini', cue: 'x',
    question: 'q', questionNote: 'n',
    grid: {
      perPoint: [{ id: 'name', label: 'Name', marks: 2 }, { id: 'link', label: 'Link', marks: 1 }],
      shorthand: '', ruleNote: '', cite: { label: 'c' },
    },
    scripts: [{ id: 's1', label: 'A', persona: 'p', attempts: [{ id: 'a1', text: 't', key: { name: 2, link: 0 }, keyNote: 'k' }] }],
    takeaway: { id: 'tk', rule: 'r', detail: 'd', cite: { label: 'c' } },
  };
  const miniScale: ScaleSession = {
    mode: 'scale', id: 't-s', subject: 'maths', level: 'higher', title: 'Mini scale', cue: 'x',
    question: 'q', questionNote: 'n',
    scale: {
      name: 'S', levels: [
        { id: 'lo', label: 'Low', annotation: 'L', marks: 0 },
        { id: 'mid', label: 'Mid', annotation: 'M', marks: 3 },
        { id: 'hi', label: 'High', annotation: 'H', marks: 6 },
      ], notes: [], cite: { label: 'c' },
    },
    scripts: [{ id: 's1', label: 'A', persona: 'p', work: ['w'], keyLevelId: 'mid', keyNote: 'k' }],
    takeaway: { id: 'tk2', rule: 'r', detail: 'd', cite: { label: 'c' } },
  };

  it('flags an over-credit when the student awards a criterion the examiner withheld', () => {
    const decisions = { [gridDecisionKey('a1', 'name')]: true, [gridDecisionKey('a1', 'link')]: true };
    const deltas = gridScriptMisses(miniGrid, miniGrid.scripts[0], decisions);
    expect(deltas).toEqual([{ key: 'business::Link', subject: 'business', label: 'Link', over: 1, under: 0, sessionId: 't-g' }]);
  });

  it('flags an under-credit when the student withholds a criterion the examiner gave', () => {
    const decisions = { [gridDecisionKey('a1', 'name')]: false, [gridDecisionKey('a1', 'link')]: false };
    const deltas = gridScriptMisses(miniGrid, miniGrid.scripts[0], decisions);
    expect(deltas).toEqual([{ key: 'business::Name', subject: 'business', label: 'Name', over: 0, under: 1, sessionId: 't-g' }]);
  });

  it('returns no deltas when the student marks exactly like the examiner', () => {
    const decisions = { [gridDecisionKey('a1', 'name')]: true, [gridDecisionKey('a1', 'link')]: false };
    expect(gridScriptMisses(miniGrid, miniGrid.scripts[0], decisions)).toEqual([]);
  });

  it('flags scale generosity direction (too high = over)', () => {
    expect(scaleScriptMisses(miniScale, miniScale.scripts[0], 'hi')[0]).toMatchObject({ over: 1, under: 0 });
    expect(scaleScriptMisses(miniScale, miniScale.scripts[0], 'lo')[0]).toMatchObject({ over: 0, under: 1 });
    expect(scaleScriptMisses(miniScale, miniScale.scripts[0], 'mid')).toEqual([]);
  });

  it('merges and ranks blind spots by frequency', () => {
    let state = loadChair('m1');
    const over = { key: 'business::Link', subject: 'business', label: 'Link', over: 1, under: 0, sessionId: 't-g' };
    state = mergeMisses(state, [over], 100);
    state = mergeMisses(state, [over], 200);
    state = mergeMisses(state, [{ key: 'maths::scale-placement', subject: 'maths', label: 'scale', over: 1, under: 0, sessionId: 't-s' }], 300);
    expect(state.misses['business::Link'].over).toBe(2);
    expect(state.misses['business::Link'].sessions).toEqual(['t-g']); // deduped
    const top = topMisses(state);
    expect(top[0].key).toBe('business::Link'); // most frequent first
    expect(top).toHaveLength(2);
  });

  it('schedules codex recall: got-it climbs, fuzzy resets and comes back soon', () => {
    let state = loadChair('cx');
    const T = 1_000_000;
    // never-reviewed earned rule is due now
    expect(codexDue(state, ['r'], T)).toEqual(['r']);
    state = reviewCodex(state, 'r', true, T);
    expect(state.codexReview['r'].streak).toBe(1);
    expect(state.codexReview['r'].due).toBe(T + 1 * 86_400_000); // 1 day
    expect(codexDue(state, ['r'], T)).toEqual([]); // no longer due now
    state = reviewCodex(state, 'r', true, state.codexReview['r'].due);
    expect(state.codexReview['r'].streak).toBe(2); // climbs
    const fuzzy = reviewCodex(state, 'r', false, T + 999);
    expect(fuzzy.codexReview['r'].streak).toBe(0); // reset
    expect(fuzzy.codexReview['r'].due - (T + 999)).toBeLessThan(86_400_000); // back within a day
  });

  it('detects borderline scripts (split grid / middle scale rung)', () => {
    // grid: key splits criteria (name earned, link withheld) → borderline
    expect(isBorderlineScript(miniGrid, miniGrid.scripts[0])).toBe(true);
    // scale: middle rung → borderline; top/bottom → not
    expect(isBorderlineScript(miniScale, miniScale.scripts[0])).toBe(true);
    const topScript = { ...miniScale.scripts[0], keyLevelId: 'hi' };
    const botScript = { ...miniScale.scripts[0], keyLevelId: 'lo' };
    expect(isBorderlineScript(miniScale, topScript)).toBe(false);
    expect(isBorderlineScript(miniScale, botScript)).toBe(false);
    expect(borderlineScripts(miniGrid)).toHaveLength(1);
  });
});

// ─────────────────── content integrity (hand-authored data) ───────────────────

describe('Examiner\'s Chair content integrity', () => {
  it('has unique session and takeaway ids', () => {
    const ids = allSessions().map(s => s.id);
    expect(new Set(ids).size).toBe(ids.length);
    const rules = allSessions().map(s => s.takeaway.id);
    expect(new Set(rules).size).toBe(rules.length);
  });

  it('findSession resolves every session', () => {
    for (const s of allSessions()) expect(findSession(s.id)?.id).toBe(s.id);
  });

  it('every cite label is non-empty (verify-don\'t-guess)', () => {
    for (const subject of CHAIR_SUBJECTS) {
      expect(subject.sources.length).toBeGreaterThan(0);
      for (const s of subject.sessions) {
        expect(s.questionNote.length).toBeGreaterThan(10);
        expect(s.takeaway.cite.label.length).toBeGreaterThan(5);
        if (s.mode === 'grid') expect(s.grid.cite.label.length).toBeGreaterThan(5);
        else expect(s.scale.cite.label.length).toBeGreaterThan(5);
      }
    }
  });

  it('grid keys award 0 or the full criterion marks, over known criteria only', () => {
    for (const s of allSessions()) {
      if (s.mode !== 'grid') continue;
      const byId = new Map(s.grid.perPoint.map(c => [c.id, c.marks]));
      for (const script of s.scripts) {
        for (const attempt of script.attempts) {
          for (const [cid, awarded] of Object.entries(attempt.key)) {
            const full = byId.get(cid);
            expect(full, `${s.id}/${script.id}/${attempt.id}: unknown criterion ${cid}`).toBeDefined();
            expect([0, full], `${s.id}/${script.id}/${attempt.id}:${cid}`).toContain(awarded);
          }
          // every criterion must have an explicit decision in the key
          for (const c of s.grid.perPoint) {
            expect(attempt.key[c.id], `${s.id}/${script.id}/${attempt.id}: missing key for ${c.id}`).toBeDefined();
          }
          expect(attempt.keyNote.length).toBeGreaterThan(10);
        }
      }
    }
  });

  it('scale sessions have strictly increasing mark ladders and resolvable keys', () => {
    for (const s of allSessions()) {
      if (s.mode !== 'scale') continue;
      const marks = s.scale.levels.map(l => l.marks);
      for (let i = 1; i < marks.length; i++) {
        expect(marks[i], `${s.id}: ladder must increase`).toBeGreaterThan(marks[i - 1]);
      }
      const ids = new Set(s.scale.levels.map(l => l.id));
      expect(ids.size).toBe(s.scale.levels.length);
      for (const script of s.scripts) {
        expect(ids.has(script.keyLevelId), `${s.id}/${script.id}: key level ${script.keyLevelId}`).toBe(true);
        expect(script.work.length).toBeGreaterThan(0);
        expect(script.keyNote.length).toBeGreaterThan(10);
      }
    }
  });

  it('every embodied insight carries a citation', () => {
    for (const s of allSessions()) {
      const scripts = s.mode === 'grid' ? s.scripts : s.scripts;
      for (const script of scripts) {
        if (script.embodies) {
          expect(script.embodies.cite.label.length).toBeGreaterThan(5);
          expect(script.embodies.behaviour.length).toBeGreaterThan(10);
        }
      }
    }
  });
});
