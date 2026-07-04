/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guards the Paper Trail progress aggregator (feature C1): overall + per-subject
 * accuracy, distinct-paper counting, gap tallies and an honest empty state. Runs
 * against the real localStorage-backed stores (jsdom provides localStorage).
 */
import { describe, it, expect, beforeEach } from 'vitest';
import { setMark } from '../components/PaperTrail/attemptStore';
import { computeProgress } from '../components/PaperTrail/progressStats';

const NOW = 1_700_000_000_000;
const ns = (uid: string, subject: string, year: number, file: string) => `${uid}|${subject}|${year}|higher|ev|${file}`;

describe('Paper Trail — progress aggregator', () => {
  beforeEach(() => localStorage.clear());

  it('reports an honest empty state with no practice', () => {
    const p = computeProgress('u1', NOW);
    expect(p.totalMarks).toBe(0);
    expect(p.overallAvg).toBe(0);
    expect(p.papersPractised).toBe(0);
    expect(p.subjects).toEqual([]);
  });

  it('averages self-marks overall and per subject, and counts distinct papers', () => {
    setMark(ns('u1', 'business', 2022, 'a'), '1', { score: 10, max: 20, ts: NOW }); // 50%
    setMark(ns('u1', 'business', 2022, 'a'), '2', { score: 15, max: 20, ts: NOW }); // 75%  (same paper)
    setMark(ns('u1', 'mathematics', 2021, 'b'), '1', { score: 40, max: 40, ts: NOW }); // 100%

    const p = computeProgress('u1', NOW);
    expect(p.totalMarks).toBe(3);
    expect(p.papersPractised).toBe(2);
    expect(p.overallAvg).toBe(75); // (50+75+100)/3
    const biz = p.subjects.find(s => s.subjectId === 'business')!;
    expect(biz).toMatchObject({ n: 2, avg: 63 }); // round((50+75)/2)
    const maths = p.subjects.find(s => s.subjectId === 'mathematics')!;
    expect(maths).toMatchObject({ n: 1, avg: 100 });
  });

  it('tallies the reflection gaps', () => {
    setMark(ns('u1', 'business', 2022, 'a'), '1', { score: 5, max: 20, gap: 'careless', ts: NOW });
    setMark(ns('u1', 'business', 2022, 'a'), '2', { score: 5, max: 20, gap: 'careless', ts: NOW });
    setMark(ns('u1', 'business', 2022, 'a'), '3', { score: 5, max: 20, gap: 'timing', ts: NOW });
    const p = computeProgress('u1', NOW);
    expect(p.gaps.careless).toBe(2);
    expect(p.gaps.timing).toBe(1);
    expect(p.gaps.content).toBe(0);
  });

  it('scopes to the given uid', () => {
    setMark(ns('u1', 'business', 2022, 'a'), '1', { score: 10, max: 20, ts: NOW });
    setMark(ns('u2', 'business', 2022, 'a'), '1', { score: 20, max: 20, ts: NOW });
    expect(computeProgress('u1', NOW).totalMarks).toBe(1);
    expect(computeProgress('u2', NOW).totalMarks).toBe(1);
  });
});
