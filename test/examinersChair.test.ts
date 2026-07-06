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
  loadChair,
  markCodexOnCards,
  overallCalibration,
  saveChair,
  scoreGridScript,
  scoreScaleScript,
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
