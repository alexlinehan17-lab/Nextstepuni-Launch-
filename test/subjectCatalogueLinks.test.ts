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
import { LC_SUBJECTS, LCA_SUBJECTS, LCVP_GRADES, defaultSubjectConfig, fixedLevelNote, getGradeIndex, getGradesForLevel, getPointsForGrade, gradeLadder, isValidTarget, lcSubjectLevels } from '../components/subjectData';
import { resolveSubjectId } from '../curriculumRegistry';
import { PAPER_TRAIL_SUBJECTS } from '../paperTrailData';
import { baseName } from '../components/shared/subjectNames';
import { profileDeckChoice } from '../components/MarkBank/MarkBank';
import { SUBJECTS as MARK_BANK_SUBJECTS, deckSize, levelsFor } from '../components/MarkBank/deck';
import { choicesFor, emptyChoice, levelOptions } from '../components/onboarding/model';

const paperTrailMatch = (name: string, cycle: 'lc' | 'lca') =>
  PAPER_TRAIL_SUBJECTS.find(subject => subject.cycle === cycle
    && [subject.name, ...(subject.aliases ?? [])].some(alias => baseName(alias) === baseName(name)));

// First examined in June 2027, so the SEC archive has no papers for them yet.
const NO_PAPERS_YET = new Set(['Climate Action and Sustainable Development', 'Drama, Film and Theatre Studies']);

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
    // Agricultural Economics was last examined in 2019; History (Early Modern)
    // is a field of study within History, which students pick as History.
    const retiredOrFolded = new Set(['agricultural-economics', 'history-early-modern']);
    const missing = PAPER_TRAIL_SUBJECTS
      .filter(subject => subject.cycle === 'lc' && !offered.has(subject.id) && !retiredOrFolded.has(subject.id))
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
  it.each(LCA_SUBJECTS.map(subject => subject.name))('%s links to its Paper Trail papers', name => {
    expect(paperTrailMatch(name, 'lca')).toBeTruthy();
  });
});
