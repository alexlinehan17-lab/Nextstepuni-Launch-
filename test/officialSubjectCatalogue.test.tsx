import React from 'react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen, within } from '@testing-library/react';
import official from './fixtures/officialSubjectCatalogue20261110.json';
import {
  catalogueForProgramme, catalogueSubject, JC_SUBJECTS, JC_BAND_RANGES, LC_SUBJECTS, LCA_SUBJECTS,
  subjectLevels, subjectUsesExamGrades, subjectHasWrittenExam, subjectMatchesQuery,
  type StudentSubjectProfile, type SubjectProgramme, type YearGroup,
} from '../components/subjectData';
import { buildProfile, draftKey, emptyChoice, initialDraft, readDraft, requiresGradeSetup, subjectsFor, type SetupDraft } from '../components/onboarding/model';
import { PAPER_TRAIL_SUBJECTS } from '../paperTrailData';
import { paperTrailSubjectMatchesStudentName, paperTrailSubjectMatchesProfileCycle } from '../components/PaperTrail';
import { resolveSubjectId } from '../curriculumRegistry';
import { getSubjectStarCrew } from '../data/subjectStarCrew';
import ChangeSubjectsModal from '../components/ChangeSubjectsModal';
import SubjectOnboarding from '../components/SubjectOnboarding';
import Onboarding from '../components/Onboarding';
import StudySubjectPicker from '../components/study/StudySubjectPicker';

const device = vi.hoisted(() => ({ mobile: true }));
vi.mock('../hooks/useMobileAppDesign', () => ({ useMobileAppDesign: () => device.mobile }));
vi.mock('../utils/funnel', () => ({ trackFunnel: vi.fn() }));
beforeEach(() => { localStorage.clear(); sessionStorage.clear(); });

describe('independent official catalogue checklist, 10 November 2026', () => {
  it.each([
    ['jc', [...official.jc, ...official.jcShortCourses]],
    ['lc', [...official.lc, ...official.lcNonExam, ...official.nonCurricularLanguages]],
    ['lca', [...official.lca, ...[...official.modernForeignLanguages, ...official.nonCurricularLanguages].map(name => `Leaving Cert ${name}`)]],
  ] as [SubjectProgramme, string[]][])('offers every published %s choice, with searchable official names', (programme, expected) => {
    for (const name of expected) {
      const subject = catalogueSubject(programme, name);
      expect(subject, name).toBeDefined();
      expect(subjectMatchesQuery(subject!, name), name).toBe(true);
    }
    const names = catalogueForProgramme(programme).map(s => s.name);
    expect(new Set(names).size).toBe(names.length);
  });

  it('covers all current JC written-paper identities without confusing Irish T1 and T2', () => {
    for (const paper of PAPER_TRAIL_SUBJECTS.filter(s => s.cycle === 'jc')) {
      expect(JC_SUBJECTS.some(s => s.paperSubjectId === paper.id), paper.id).toBe(true);
    }
    for (const subject of JC_SUBJECTS.filter(s => !s.noWrittenExam)) {
      const matches = PAPER_TRAIL_SUBJECTS.filter(p => p.cycle === 'jc' && paperTrailSubjectMatchesStudentName(p, subject.name));
      expect(matches.map(p => p.id), subject.name).toEqual([subject.paperSubjectId]);
    }
  });

  it('keeps established languages separate from common-level LCA languages and their papers', () => {
    const names = ['French', 'Leaving Cert French', 'Leaving Cert Polish', 'Leaving Cert Ukrainian'];
    const papers = PAPER_TRAIL_SUBJECTS.filter(p => paperTrailSubjectMatchesProfileCycle(p, false, true, names)
      && names.some(name => paperTrailSubjectMatchesStudentName(p, name)));
    expect(papers.map(p => p.id).sort()).toEqual(['french', 'lca-french', 'polish', 'ukrainian']);
    for (const course of LCA_SUBJECTS.filter(s => s.establishedSubject)) {
      expect(resolveSubjectId(course.name), course.name).toBe(resolveSubjectId(course.establishedSubject!));
      expect(PAPER_TRAIL_SUBJECTS.filter(p => paperTrailSubjectMatchesStudentName(p, course.name)).map(p => p.id)).toEqual([resolveSubjectId(course.establishedSubject!)]);
    }
    expect(subjectLevels('lca', 'French')).toEqual(['common']);
    expect(subjectLevels('lca', 'Leaving Cert French')).toEqual(['higher', 'ordinary']);
    expect(subjectLevels('lca', 'Leaving Cert Ukrainian')).toEqual(['higher']);
  });

  it('does not assign written-exam grades or unrelated papers to short and non-exam courses', () => {
    for (const programme of ['jc', 'lc', 'lca'] as const) {
      for (const course of catalogueForProgramme(programme).filter(s => s.noWrittenExam)) {
        expect(subjectUsesExamGrades(programme, course.name), course.name).toBe(course.examGrades === true);
        expect(PAPER_TRAIL_SUBJECTS.filter(p => p.cycle === programme && paperTrailSubjectMatchesStudentName(p, course.name)), course.name).toEqual([]);
      }
    }
    expect(subjectUsesExamGrades('jc', 'Art')).toBe(true);
    expect(subjectHasWrittenExam(catalogueSubject('lca', 'Social Education')!, 2026)).toBe(true);
    expect(subjectHasWrittenExam(catalogueSubject('lca', 'Social Education')!, 2027)).toBe(false);
    const social = PAPER_TRAIL_SUBJECTS.find(s => s.id === 'lca-social-education')!;
    expect(paperTrailSubjectMatchesStudentName(social, 'Social Education', 2026)).toBe(true);
    expect(paperTrailSubjectMatchesStudentName(social, 'Social Education', 2027)).toBe(false);
  });

  it('uses existing approved artwork for every selectable course', () => {
    expect([...JC_SUBJECTS, ...LC_SUBJECTS, ...LCA_SUBJECTS].filter(s => !getSubjectStarCrew(s.name)).map(s => s.name)).toEqual([]);
  });

  it('uses the revised national JC grade boundaries without changing saved band labels', () => {
    expect(JC_BAND_RANGES.Distinction).toEqual([85, 100]);
    expect(JC_BAND_RANGES['Higher Merit']).toEqual([70, 84]);
    expect(JC_BAND_RANGES.Merit).toEqual([55, 69]);
  });
});

function readyDraft(year: YearGroup, names = subjectsFor(year).map(s => s.name)): SetupDraft {
  return { ...initialDraft(), year, step: 'subjects', subjects: names, date: '2030-06-05', dateEdited: true,
    category: 'college-learning', vision: ['campus'], rest: ['Sunday'],
    configs: Object.fromEntries(names.map(name => [name, {
      ...emptyChoice(year, name), level: subjectLevels(year === '3rd' ? 'jc' : year === 'LCA1' ? 'lca' : 'lc', name)[0],
      current: 'later', target: 'later', reviewed: true,
    }])) };
}

it.each(['3rd', 'LCA1', '5th'] as const)('retains every %s choice through draft reload and profile JSON persistence', year => {
  const value = readyDraft(year);
  localStorage.setItem(draftKey('catalogue', 'fresh'), JSON.stringify(value));
  const restored = readDraft('catalogue', 'fresh');
  const profile = JSON.parse(JSON.stringify(buildProfile(restored))) as StudentSubjectProfile;
  expect(profile.subjects.map(s => s.subjectName)).toEqual(value.subjects);
  for (const subject of profile.subjects) {
    expect(subject.level).toBe(value.configs[subject.subjectName].level);
    expect(subject.currentGrade).toBeUndefined();
    expect(subject.currentBand).toBeUndefined();
  }
});

const jcProfile = (): StudentSubjectProfile => ({
  yearGroup: '3rd', curriculumLevel: 'junior', examStartDate: '2030-06-05', restDays: ['Sunday'],
  createdAt: '2026-01-01', updatedAt: '2026-01-01', subjects: [
    { subjectName: 'Irish', level: 'ordinary', currentBand: 'Merit', targetBand: 'Higher Merit' },
    { subjectName: 'Technology', level: 'common', currentBand: 'Achieved', targetBand: 'Merit' },
  ],
});

describe('existing subject editor flows', () => {
  it('saves two French courses separately and starts a Higher-only LCE language at its only level', () => {
    const save = vi.fn();
    render(<ChangeSubjectsModal isOpen onClose={vi.fn()} onSave={save} currentProfile={{ ...jcProfile(), yearGroup: 'LCA1', curriculumLevel: 'senior', subjects: [] }} />);
    for (const name of ['French', 'Leaving Cert French', 'Leaving Cert Ukrainian']) fireEvent.click(screen.getByRole('button', { name }));
    fireEvent.click(screen.getByRole('button', { name: 'Continue' }));
    expect(screen.getByRole('button', { name: 'Save Changes' })).toBeDisabled();
    expect(screen.queryByRole('group', { name: 'French current grade' })).not.toBeInTheDocument();
    fireEvent.click(within(screen.getByRole('group', { name: 'Leaving Cert French level' })).getByRole('button', { name: 'Ordinary' }));
    fireEvent.click(within(screen.getByRole('group', { name: 'Leaving Cert French current grade' })).getByRole('button', { name: 'O3' }));
    fireEvent.click(within(screen.getByRole('group', { name: 'Leaving Cert French target grade' })).getByRole('button', { name: 'H3' }));
    fireEvent.click(within(screen.getByRole('group', { name: 'Leaving Cert Ukrainian current grade' })).getByRole('button', { name: 'H4' }));
    fireEvent.click(screen.getByRole('button', { name: 'Save Changes' }));
    expect(save.mock.calls[0][0].subjects).toEqual([
      { subjectName: 'French', level: 'common' },
      { subjectName: 'Leaving Cert French', level: 'ordinary', currentGrade: 'O3', targetGrade: 'H3' },
      { subjectName: 'Leaving Cert Ukrainian', level: 'higher', currentGrade: 'H4', targetGrade: 'H4' },
    ]);
  });

  it('offers JC choices, preserves legacy names and bands, and saves new courses through reopen', () => {
    const save = vi.fn();
    const view = render(<ChangeSubjectsModal isOpen onClose={vi.fn()} onSave={save} currentProfile={jcProfile()} />);
    expect(screen.queryByRole('button', { name: 'Biology' })).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Applied Technology' })).toHaveAttribute('aria-pressed', 'true');
    fireEvent.click(screen.getByRole('button', { name: 'Jewish Studies' }));
    fireEvent.click(screen.getByRole('button', { name: 'Coding' }));
    fireEvent.click(screen.getByRole('button', { name: 'Continue' }));
    expect(screen.queryByRole('group', { name: 'Coding current grade' })).not.toBeInTheDocument();
    expect(screen.queryByRole('group', { name: 'Coding current band' })).not.toBeInTheDocument();
    fireEvent.click(within(screen.getByRole('group', { name: 'Jewish Studies current band' })).getByRole('button', { name: 'Merit' }));
    fireEvent.click(within(screen.getByRole('group', { name: 'Irish level' })).getByRole('button', { name: 'Higher' }));
    fireEvent.click(screen.getByRole('button', { name: 'Save Changes' }));
    const saved = JSON.parse(JSON.stringify(save.mock.calls[0][0]));
    expect(saved.subjects).toEqual([
      { ...jcProfile().subjects[0], level: 'higher' }, jcProfile().subjects[1],
      { subjectName: 'Jewish Studies', level: 'common', currentBand: 'Merit' },
      { subjectName: 'Coding', level: 'common' },
    ]);
    view.unmount();
    render(<ChangeSubjectsModal isOpen onClose={vi.fn()} onSave={save} currentProfile={saved} />);
    expect(screen.getByRole('button', { name: 'Coding' })).toHaveAttribute('aria-pressed', 'true');
  });

  it('uses the JC catalogue in first-time Launchpad setup, with no LC points or invented short-course bands', () => {
    const save = vi.fn();
    render(<SubjectOnboarding user={{ uid: 'junior', yearGroup: '2nd' }} onComplete={save} onClose={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: 'Get Started' }));
    expect(screen.queryByRole('button', { name: 'Biology' })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Digital Media Literacy' }));
    for (let step = 2; step < 6; step++) fireEvent.click(screen.getByRole('button', { name: 'Continue' }));
    expect(screen.queryByText('Projected CAO points gain')).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Save & Continue' }));
    expect(save.mock.calls[0][0]).toMatchObject({ yearGroup: '2nd', curriculumLevel: 'junior', examStartDate: null,
      subjects: [{ subjectName: 'Digital Media Literacy', level: 'common' }] });
  });

  it('does not assign LCVP points to LC non-exam subjects', () => {
    const save = vi.fn();
    render(<ChangeSubjectsModal isOpen onClose={vi.fn()} onSave={save} currentProfile={{ ...jcProfile(), yearGroup: '5th', curriculumLevel: 'senior', subjects: [] }} />);
    fireEvent.click(screen.getByRole('button', { name: 'Physical Education (non-exam)' }));
    fireEvent.click(screen.getByRole('button', { name: 'SPHE' }));
    fireEvent.click(screen.getByRole('button', { name: 'Continue' }));
    expect(screen.queryByRole('button', { name: 'Distinction' })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Save Changes' }));
    expect(save.mock.calls[0][0].subjects).toEqual([{ subjectName: 'Physical Education (non-exam)', level: 'common' }, { subjectName: 'SPHE', level: 'common' }]);
  });
});

it.each([true, false])('skips exam grading for a short-course-only onboarding selection, mobile=%s', mobile => {
  device.mobile = mobile;
  const draft = readyDraft('3rd', ['Coding', 'Philosophy']);
  localStorage.setItem(draftKey('short-courses', 'fresh'), JSON.stringify(draft));
  render(<Onboarding userId="short-courses" userName="Alex" onComplete={vi.fn()} onSkip={vi.fn()} />);
  fireEvent.click(screen.getByRole('button', { name: 'Continue' }));
  expect(screen.getByRole('heading', { name: 'Make room for progress.' })).toBeInTheDocument();
  expect(draft.subjects.some(name => requiresGradeSetup(draft.year, name))).toBe(false);
});

it('makes new courses selectable in the unchanged Study Room picker', () => {
  const select = vi.fn();
  render(<StudySubjectPicker subjects={['Jewish Studies', 'Coding', 'Leaving Cert Polish']} selected="Coding" onSelect={select} />);
  fireEvent.click(screen.getByRole('button', { name: 'Study Leaving Cert Polish' }));
  expect(select).toHaveBeenCalledWith('Leaving Cert Polish');
});
