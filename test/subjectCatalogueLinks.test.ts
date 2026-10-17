/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Every subject a student can pick at onboarding must link to the rest of the
 * app: a curriculum entry (Topic Atlas, study topics), its Paper Trail papers
 * and, where the bank has cards, its Mark Bank deck. A name that resolves
 * nowhere silently gives the student an empty subject.
 */
import { describe, expect, it } from 'vitest';
import { LC_SUBJECTS, LCA_SUBJECTS, LCVP_GRADES, defaultSubjectConfig, fixedLevelNote, getGradeIndex, getGradesForLevel, getPointsForGrade, gradeLadder, isValidTarget, lcSubjectLevels, subjectMatchesQuery } from '../components/subjectData';
import { resolveSubjectId } from '../curriculumRegistry';
import { PAPER_TRAIL_INDEX, PAPER_TRAIL_SUBJECTS } from '../paperTrailData';
import { baseName } from '../components/shared/subjectNames';
import { profileDeckChoice } from '../components/MarkBank/MarkBank';
import { SUBJECTS as MARK_BANK_SUBJECTS, deckSize, levelsFor } from '../components/MarkBank/deck';
import { choicesFor, emptyChoice, levelOptions } from '../components/onboarding/model';
import { getSubjectStarCrew } from '../data/subjectStarCrew';

const paperTrailMatch = (name: string, cycle: 'lc' | 'lca') =>
  PAPER_TRAIL_SUBJECTS.find(subject => subject.cycle === cycle
    && [subject.name, ...(subject.aliases ?? [])].some(alias => baseName(alias) === baseName(name)));

// First examined in June 2027, so the SEC archive has no papers for them yet.
const NO_PAPERS_YET = new Set(['Climate Action and Sustainable Development', 'Drama, Film and Theatre Studies']);

// A Paper Trail subject with no sitting since 2022 is no longer a choice
// (Agricultural Economics, Technical Drawing, archive-only course names).
const STILL_EXAMINED_FROM = 2022;
const stillExamined = (id: string) =>
  (PAPER_TRAIL_INDEX[id] ?? []).some(entry => entry.year >= STILL_EXAMINED_FROM);

describe('Leaving Cert subject catalogue', () => {
  it('has no duplicate names', () => {
    const names = LC_SUBJECTS.map(subject => subject.name);
    expect(new Set(names).size).toBe(names.length);
  });

  it.each(LC_SUBJECTS.map(subject => subject.name))('%s resolves to a curriculum subject', name => {
    expect(resolveSubjectId(name)).toBeTruthy();
  });

  it.each(LC_SUBJECTS.map(subject => subject.name).filter(name => !NO_PAPERS_YET.has(name)))('%s links to its Paper Trail papers', name => {
    expect(paperTrailMatch(name, 'lc')).toBeTruthy();
  });

  it('offers every Paper Trail Leaving Cert subject that is still examined', () => {
    const offered = new Set(LC_SUBJECTS.map(subject => paperTrailMatch(subject.name, 'lc')?.id).filter(Boolean));
    // History (Early Modern) is a field of study within History, which
    // students pick as History.
    const folded = new Set(['history-early-modern']);
    const missing = PAPER_TRAIL_SUBJECTS
      .filter(subject => subject.cycle === 'lc' && stillExamined(subject.id) && !offered.has(subject.id) && !folded.has(subject.id))
      .map(subject => subject.name);
    expect(missing).toEqual([]);
  });

  it('opens Mark Bank on the student’s own subject for every subject with cards', () => {
    const unlinked = MARK_BANK_SUBJECTS
      .filter(deck => levelsFor(deck.id).some(level => deckSize(deck.id, level) > 0))
      .filter(deck => !LC_SUBJECTS.some(subject => profileDeckChoice([{ subjectName: subject.name, level: lcSubjectLevels(subject.name)[0] }])?.subjectId === deck.id))
      .map(deck => deck.title);
    expect(unlinked).toEqual([]);
  });

  it('keeps the requested languages, LCVP and PE selectable', () => {
    for (const name of ['LCVP Link Modules', 'Physical Education', 'Romanian', 'Portuguese', 'Polish', 'Ukrainian', 'Russian', 'Mandarin Chinese', 'Physics & Chemistry'])
      expect(LC_SUBJECTS.some(subject => subject.name === name)).toBe(true);
  });
});

describe('levels and the LCVP grade scale', () => {
  it('examines the non-curricular EU languages and Ukrainian at Higher only', () => {
    expect(lcSubjectLevels('Romanian')).toEqual(['higher']);
    expect(lcSubjectLevels('Ukrainian')).toEqual(['higher']);
    expect(lcSubjectLevels('Polish')).toEqual(['higher', 'ordinary']);
    expect(fixedLevelNote('Romanian')).toBe('Romanian is examined at Higher level only.');
    expect(fixedLevelNote('Biology')).toBeNull();
  });

  it('starts a fixed-level subject on its level in onboarding', () => {
    expect(emptyChoice('5th', 'Romanian').level).toBe('higher');
    expect(emptyChoice('5th', 'LCVP Link Modules').level).toBe('common');
    expect(emptyChoice('5th', 'Biology').level).toBeNull();
    expect(levelOptions('LCA1', 'Social Education')).toEqual(['common']);
  });

  it('grades LCVP Distinction, Merit or Pass with CAO points', () => {
    expect(choicesFor('6th', 'common')).toEqual(LCVP_GRADES);
    expect(choicesFor('LCA2', 'common')).toEqual([]);
    expect(getGradesForLevel('common')).toEqual(['Distinction', 'Merit', 'Pass']);
    expect(['Distinction', 'Merit', 'Pass'].map(grade => getPointsForGrade(grade as never))).toEqual([66, 46, 28]);
    expect(getGradeIndex('Merit')).toBe(1);
    expect(gradeLadder('Pass')).toEqual(LCVP_GRADES);
    expect(isValidTarget('Merit', 'Distinction')).toBe(true);
    expect(isValidTarget('Merit', 'H1')).toBe(false);
    expect(defaultSubjectConfig('LCVP Link Modules')).toEqual({ level: 'common', currentGrade: 'Merit', targetGrade: 'Distinction' });
    expect(defaultSubjectConfig('Romanian').level).toBe('higher');
  });

  it('leaves H and O grades unchanged', () => {
    expect(getPointsForGrade('H1')).toBe(100);
    expect(getPointsForGrade('H6', true)).toBe(71);
    expect(getPointsForGrade('O4')).toBe(28);
    expect(getGradeIndex('O3')).toBe(2);
    expect(getGradeIndex(undefined)).toBe(8);
  });
});

describe('Leaving Cert Applied catalogue', () => {
  // Courses with an SEC exam link to their LCA papers. Courses assessed only by
  // key assignments have none, and LCA students may sit Leaving Cert Maths.
  it.each(LCA_SUBJECTS.filter(subject => !subject.noWrittenExam && subject.name !== 'Leaving Cert Maths').map(subject => subject.name))('%s links to its Paper Trail papers', name => {
    expect(paperTrailMatch(name, 'lca')).toBeTruthy();
  });

  it('offers every LCA course the SEC examines', () => {
    const offered = new Set(LCA_SUBJECTS.map(subject => paperTrailMatch(subject.name, 'lca')?.id).filter(Boolean));
    expect(PAPER_TRAIL_SUBJECTS.filter(subject => subject.cycle === 'lca' && stillExamined(subject.id) && !offered.has(subject.id)).map(subject => subject.name)).toEqual([]);
  });

  it('offers the programme courses without an exam, and Leaving Cert Maths', () => {
    const names = LCA_SUBJECTS.map(subject => subject.name);
    for (const name of ['Vocational Preparation & Guidance', 'Introduction to ICT', 'Arts Education', 'Leisure and Recreation', 'Science', 'Religious Education', 'Leaving Cert Maths'])
      expect(names).toContain(name);
    expect(resolveSubjectId('Leaving Cert Maths')).toBe('mathematics');
  });
});

describe('artwork', () => {
  it('draws every subject in both pickers instead of falling back to initials', () => {
    expect([...LC_SUBJECTS, ...LCA_SUBJECTS].filter(subject => !getSubjectStarCrew(subject.name)).map(subject => subject.name)).toEqual([]);
  });
});

describe('Foundation level and other names', () => {
  it('offers Foundation for Mathematics and Irish only', () => {
    expect(lcSubjectLevels('Mathematics')).toEqual(['higher', 'ordinary', 'foundation']);
    expect(lcSubjectLevels('Irish')).toEqual(['higher', 'ordinary', 'foundation']);
    expect(LC_SUBJECTS.filter(subject => subject.levels?.includes('foundation')).map(subject => subject.name)).toEqual(['Irish', 'Mathematics']);
  });

  it('counts Foundation grades as CAO does', () => {
    expect(getGradesForLevel('foundation')[0]).toBe('F1');
    expect(['F1', 'F2', 'F3'].map(grade => getPointsForGrade(grade as never, true))).toEqual([20, 12, 0]);
    expect(isValidTarget('F3', 'F1')).toBe(true);
    expect(isValidTarget('F3', 'O6')).toBe(false);
    expect(choicesFor('6th', 'foundation')).toEqual(['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8']);
  });

  it('practises Foundation in the Ordinary Mark Bank deck', () => {
    expect(profileDeckChoice([{ subjectName: 'Mathematics', level: 'foundation' }])).toEqual({ subjectId: 'maths', level: 'ordinary' });
  });

  it('finds a subject by the name students search for', () => {
    const find = (query: string) => LC_SUBJECTS.filter(subject => subjectMatchesQuery(subject, query)).map(subject => subject.name);
    expect(find('construction technology')).toEqual(['Construction Studies']);
    expect(find('life, community')).toEqual(['LCVP Link Modules']);
    expect(find('lcpe')).toEqual(['Physical Education']);
    expect(find('chinese')).toEqual(['Mandarin Chinese']);
    expect(LCA_SUBJECTS.filter(subject => subjectMatchesQuery(subject, 'vpg')).map(subject => subject.name)).toEqual(['Vocational Preparation & Guidance']);
  });
});
