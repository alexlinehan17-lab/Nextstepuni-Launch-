/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — earlier-syllabus wording (data/paperTrail/syllabusChanges.ts).
 */

import { describe, expect, it } from 'vitest';
import {
  PAPER_TRAIL_SYLLABUS_HISTORY,
  earlierSyllabusNote,
  syllabusBoundary,
  syllabusGridNote,
  syllabusTag,
} from '../data/paperTrail/syllabusChanges';
import { PAPER_TRAIL_INDEX, PAPER_TRAIL_SUBJECTS } from '../paperTrailData';

describe('Paper Trail syllabus history', () => {
  it('only names indexed subjects, with ascending change years', () => {
    const ids = new Set(PAPER_TRAIL_SUBJECTS.map(s => s.id));
    for (const [id, history] of Object.entries(PAPER_TRAIL_SYLLABUS_HISTORY)) {
      expect(ids.has(id), id).toBe(true);
      expect([...history.changes].sort((a, b) => a - b), id).toEqual(history.changes);
    }
  });

  it('reads a past change as past and a future specification as announced', () => {
    expect(earlierSyllabusNote('economics', 'Economics', 2015, 2026))
      .toBe('Earlier syllabus. The current Economics syllabus was first examined in 2021.');
    expect(earlierSyllabusNote('economics', 'Economics', 2021, 2026)).toBeNull();
    expect(earlierSyllabusNote('biology', 'Biology', 2026, 2026))
      .toBe('Earlier syllabus. A new Biology specification is first examined in 2027.');
    expect(earlierSyllabusNote('biology', 'Biology', 1999, 2026))
      .toBe('Earlier syllabus. The Biology syllabus changed for the 2004 exams, and a new specification is first examined in 2027.');
    expect(earlierSyllabusNote('classical-studies', 'Classical Studies', 2005, 2026))
      .toBe('Earlier syllabus. The Classical Studies syllabus changed for the 2011 exams and again in 2023.');
    // Once the 2027 papers are archived the same table reads as history.
    expect(earlierSyllabusNote('biology', 'Biology', 2026, 2027))
      .toBe('Earlier syllabus. The current Biology syllabus was first examined in 2027.');
  });

  it('explains Project Maths and a retired subject in their own words', () => {
    expect(earlierSyllabusNote('mathematics', 'Mathematics', 2009, 2026)).toMatch(/before Project Maths/);
    expect(earlierSyllabusNote('mathematics', 'Mathematics', 2010, 2026)).toBeNull();
    expect(syllabusTag('technical-drawing')).toBe('No longer examined');
    expect(syllabusGridNote('technical-drawing', 'Technical Drawing', 2008)).toMatch(/Design and Communication Graphics/);
  });

  it('tags grid years only before a change the archive straddles', () => {
    expect(syllabusBoundary('biology', 2026)).toBe(2004);
    expect(syllabusBoundary('latin', 2026)).toBeNull();
    expect(syllabusGridNote('latin', 'Latin', 2026))
      .toBe('A new Latin specification is first examined in 2027, so every paper here was set on an earlier syllabus.');
    expect(syllabusGridNote('english', 'English', 2026))
      .toBe('Years marked “Earlier syllabus” were set before the 2001 syllabus change.');
    expect(syllabusGridNote('construction-studies', 'Construction Studies', 2026)).toBeNull();
  });

  it('flags archived years on both sides of a past change', () => {
    // Biology: papers from before the 2004 change sit beside current-syllabus
    // years, and every one of them predates the 2027 specification.
    const years = (PAPER_TRAIL_INDEX.biology ?? []).filter(e => e.papers.some(p => !p.sitting)).map(e => e.year);
    const latest = Math.max(...years);
    expect(years.some(y => y < 2004)).toBe(true);
    expect(syllabusBoundary('biology', latest)).toBe(2004);
    for (const y of years) expect(earlierSyllabusNote('biology', 'Biology', y, latest), String(y)).not.toBeNull();
  });
});

describe('Topic Atlas stays on the reviewed June papers', () => {
  it('never surfaces a pre-2010, deferred or sample paper as a topic question', async () => {
    const { taggedSubjects, questionsForTopics } = await import('../components/PaperTrail/topics');
    const archiveOnly = new Set<string>();
    for (const [subjectId, entries] of Object.entries(PAPER_TRAIL_INDEX)) {
      for (const e of entries) {
        if (e.sitting || e.year < 2010) for (const p of e.papers) archiveOnly.add(`${subjectId}|${e.year}|${p.doc.f}`);
      }
    }
    let checked = 0;
    for (const subjectId of taggedSubjects()) {
      for (const q of questionsForTopics(subjectId, null)) {
        checked++;
        expect(q.year, `${subjectId} ${q.fileid}`).toBeGreaterThanOrEqual(2010);
        expect(archiveOnly.has(`${subjectId}|${q.year}|${q.fileid}`), `${subjectId} ${q.year} ${q.fileid}`).toBe(false);
      }
    }
    expect(checked).toBeGreaterThan(1000);
  });
});
