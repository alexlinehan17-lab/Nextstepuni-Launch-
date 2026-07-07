/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guards the Syllabus X-Ray personal ROI overlay (feature F6): the ≥3-self-mark
 * evidence gate, the subtopic-tag → strand join, the room-to-gain arithmetic
 * and ordering, the honest null when nothing joins, and — against the real
 * committed data — that Paper Trail topic tags actually resolve onto X-Ray
 * strands (the join the UI depends on) with per-uid isolation.
 */
import { describe, it, expect, beforeEach } from 'vitest';
import { roiFromMarks, computeSubjectRoi, MIN_SUBJECT_MARKS } from '../components/syllabusRoi';
import { setMark, attemptNs, type StoredMark } from '../components/PaperTrail/attemptStore';
import { SYLLABUS_DATA, type SubjectSyllabus, type SyllabusTopic } from '../components/syllabusData';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';

const NOW = 1_700_000_000_000;

const topic = (id: string, name: string, markWeight: number, subtopicIds: string[]): SyllabusTopic => ({
  id,
  name,
  section: 'Paper 1',
  markWeight,
  examFrequency: 8,
  difficulty: 3,
  studyHours: 10,
  tip: '',
  subtopics: subtopicIds.map((sid, i) => ({ id: sid, name: `${name} ${i}` })),
});

const SYL: SubjectSyllabus = {
  subject: 'Testology',
  subjectId: 'testology',
  totalMarks: 400,
  papers: [{ name: 'Paper 1', marks: 400, duration: '2h 30m' }],
  keyAdvice: '',
  topics: [
    topic('testology-0', 'Alpha', 25, ['testology-0-0', 'testology-0-1']), // carries 100 of 400
    topic('testology-1', 'Beta', 10, ['testology-1-0']),                   // carries 40 of 400
  ],
};

const mark = (n: string, score: number, max: number, subjectId = 'testology'): StoredMark => ({
  uid: 'u1', subjectId, year: 2023, level: 'higher', lang: 'ev', fileid: 'f', n, score, max, ts: NOW,
});

// Stub tag resolver: question n → curriculum subtopic id.
const TAGS: Record<string, string> = {
  '1': 'testology-0-0',
  '2': 'testology-0-1',
  '3': 'testology-1-0',
  '9': 'not-an-xray-strand-0', // tagged, but outside the X-Ray taxonomy
};
const resolve = (m: StoredMark) => TAGS[m.n];

describe('Syllabus X-Ray — personal ROI (pure core)', () => {
  it('returns null below the evidence gate', () => {
    const marks = [mark('1', 5, 10), mark('2', 7, 10)];
    expect(marks.length).toBeLessThan(MIN_SUBJECT_MARKS);
    expect(roiFromMarks(SYL, marks, resolve)).toBeNull();
  });

  it('joins marks onto strands, computes room to gain, and drops fully-accurate strands', () => {
    const roi = roiFromMarks(SYL, [
      mark('1', 5, 10),  // Alpha 50%
      mark('2', 7, 10),  // Alpha 70% → strand accuracy 60%
      mark('3', 10, 10), // Beta 100% → no room, dropped
    ], resolve)!;
    expect(roi).not.toBeNull();
    expect(roi.subjectId).toBe('testology');
    expect(roi.totalSelfMarks).toBe(3);
    expect(roi.entries).toHaveLength(1);
    expect(roi.entries[0]).toMatchObject({
      topicId: 'testology-0',
      topicName: 'Alpha',
      historicalMarks: 100, // 25% of 400
      accuracy: 60,
      sampleSize: 2,
      roomToGain: 40, // 100 × (1 − 0.60)
    });
  });

  it('ranks by room to gain, not raw historical weight', () => {
    const roi = roiFromMarks(SYL, [
      mark('1', 8, 10), // Alpha 80% → room 20 on 100 marks
      mark('2', 8, 10),
      mark('3', 1, 4),  // Beta 25% → room 30 on 40 marks
    ], resolve)!;
    expect(roi.entries.map(e => e.topicId)).toEqual(['testology-1', 'testology-0']);
    expect(roi.entries[0].roomToGain).toBe(30);
    expect(roi.entries[1].roomToGain).toBe(20);
  });

  it('shows nothing when no mark joins onto an X-Ray strand', () => {
    // Enough marks, but tags are missing or outside the X-Ray taxonomy.
    const marks = [mark('9', 2, 10), mark('9', 3, 10), mark('none', 4, 10)];
    expect(roiFromMarks(SYL, marks, resolve)).toBeNull();
  });

  it('ignores marks from other subjects', () => {
    const marks = [
      mark('1', 5, 10),
      mark('2', 5, 10),
      mark('3', 5, 10, 'other-subject'), // gate needs 3 IN this subject
    ];
    expect(roiFromMarks(SYL, marks, resolve)).toBeNull();
  });
});

describe('Syllabus X-Ray — personal ROI (real data + seeded localStorage)', () => {
  beforeEach(() => localStorage.clear());

  /** A real (syllabus, tagged paper) pair whose primary tags resolve onto
   *  X-Ray strands — the join the whole feature depends on. */
  function findJoinablePaper() {
    for (const syllabus of SYLLABUS_DATA) {
      const strandSubtopics = new Set(syllabus.topics.flatMap(t => t.subtopics.map(s => s.id)));
      for (const p of PAPER_TOPIC_TAGS) {
        if (p.subjectId !== syllabus.subjectId) continue;
        const seen = new Set<string>();
        const joinable = p.q.filter(q => {
          if (!strandSubtopics.has(q.primary) || seen.has(q.n)) return false;
          seen.add(q.n);
          return true;
        });
        if (joinable.length >= MIN_SUBJECT_MARKS) return { syllabus, paper: p, joinable };
      }
    }
    return null;
  }

  it('committed topic tags actually join onto X-Ray strands', () => {
    expect(findJoinablePaper()).not.toBeNull();
  });

  it('computes ROI from self-marks seeded in localStorage, per uid', () => {
    const found = findJoinablePaper()!;
    const { syllabus, paper, joinable } = found;
    const ns = attemptNs('u1', paper.subjectId, paper.year, paper.level, paper.lang, paper.fileid);
    for (const q of joinable.slice(0, 3)) {
      setMark(ns, q.n, { score: 5, max: 10, ts: NOW }); // 50% each
    }

    const roi = computeSubjectRoi('u1', syllabus)!;
    expect(roi).not.toBeNull();
    expect(roi.subjectId).toBe(syllabus.subjectId);
    expect(roi.totalSelfMarks).toBe(3);
    expect(roi.entries.length).toBeGreaterThan(0);
    expect(roi.entries.reduce((n, e) => n + e.sampleSize, 0)).toBe(3);
    for (const e of roi.entries) {
      expect(e.accuracy).toBe(50);
      expect(e.roomToGain).toBe(Math.round(e.historicalMarks * 0.5));
      // Every ranked strand is a real X-Ray topic for the subject.
      expect(syllabus.topics.some(t => t.id === e.topicId)).toBe(true);
    }
    // Descending room to gain.
    for (let i = 1; i < roi.entries.length; i++) {
      expect(roi.entries[i - 1].roomToGain).toBeGreaterThanOrEqual(roi.entries[i].roomToGain);
    }

    // Another student's view stays empty — marks are per uid.
    expect(computeSubjectRoi('u2', syllabus)).toBeNull();
  });
});
