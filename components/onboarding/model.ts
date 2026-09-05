import { DAYS_OF_WEEK, JC_BANDS, JC_SUBJECTS, LC_SUBJECTS, LCA_SUBJECTS, getGradesForLevel, getPointsForGrade, type Grade, type JCBand, type Level, type StudentSubject, type StudentSubjectProfile, type YearGroup } from '../subjectData';
import { getActiveCategories, getVisionCardsForLevel } from '../../northStarData';
import { isLcaYear, yearGroupToCurriculumLevel } from '../../utils/authUtils';
import { getDefaultExamDate } from '../../utils/examDates';
import type { NorthStar, NorthStarCategory } from '../../types';

export type SetupStep = 'welcome' | 'year' | 'north' | 'vision' | 'subjects' | 'grades' | 'schedule' | 'summary';
export type GradeChoice = Grade | JCBand | '' | 'later';
export interface SubjectChoice { level: Level | null; current: GradeChoice; target: GradeChoice; reviewed: boolean }
export interface SetupDraft {
  version: 2;
  step: SetupStep;
  year: YearGroup | null;
  category: NorthStarCategory | null;
  vision: string[];
  subjects: string[];
  configs: Record<string, SubjectChoice>;
  rest: string[];
  date: string;
  dateConfirmed: boolean;
  gradeSubject: string | null;
}
export const draftKey = (uid: string, mode: string) => `nextstepuni:onboarding-draft:v2:${uid}:${mode}`;
export const legacyDraftKey = (uid: string, mode: string) => `nextstepuni:onboarding-draft:v1:${uid}:${mode}`;
export const cycleFor = (year: YearGroup | null) => year ? yearGroupToCurriculumLevel(year) : 'senior';
export const subjectsFor = (year: YearGroup | null) => cycleFor(year) === 'junior' ? JC_SUBJECTS : isLcaYear(year ?? undefined) ? LCA_SUBJECTS : LC_SUBJECTS;
export const needsDate = (year: YearGroup | null) => year !== '1st' && year !== '2nd';
export const daysUntil = (value: string, today = new Date()) => {
  const now = new Date(today.getFullYear(), today.getMonth(), today.getDate());
  return Math.ceil((new Date(`${value}T00:00:00`).getTime() - now.getTime()) / 86400000);
};
export function emptyChoice(year: YearGroup | null, name: string): SubjectChoice {
  const common = isLcaYear(year ?? undefined) || (cycleFor(year) === 'junior' && !JC_SUBJECTS.find(s => s.name === name)?.jcHasLevelChoice);
  return { level: common ? 'common' : null, current: '', target: '', reviewed: false };
}
export const choicesFor = (year: YearGroup | null, level: Level | null): readonly string[] => cycleFor(year) === 'junior' ? JC_BANDS : level && level !== 'common' ? getGradesForLevel(level) : [];
export function choiceReady(year: YearGroup | null, choice?: SubjectChoice): boolean {
  if (!choice?.level) return false;
  const values = choicesFor(year, choice.level);
  return [choice.current, choice.target].every(value => value === 'later' || values.includes(value));
}
export const hasGrades = (year: YearGroup | null, choice?: SubjectChoice) => Boolean(choice?.reviewed && choiceReady(year, choice) && choice.current !== 'later' && choice.target !== 'later');
export function pointsFor(draft: SetupDraft) {
  const known = draft.subjects.filter(name => hasGrades(draft.year, draft.configs[name]));
  if (cycleFor(draft.year) === 'junior' || isLcaYear(draft.year ?? undefined)) return { count: 0, current: 0, target: 0 };
  const sum = (field: 'current' | 'target') => Math.min(625, known.map(name => getPointsForGrade(draft.configs[name][field] as Grade, !!LC_SUBJECTS.find(s => s.name === name)?.isMaths)).sort((a, b) => b - a).slice(0, 6).reduce((a, b) => a + b, 0));
  return { count: known.length, current: sum('current'), target: sum('target') };
}
export function initialDraft(targetYear?: 'TY' | '5th'): SetupDraft {
  return { version: 2, step: targetYear ? 'subjects' : 'welcome', year: targetYear ?? null, category: null, vision: [], subjects: [], configs: {}, rest: [...DAYS_OF_WEEK], date: getDefaultExamDate(), dateConfirmed: false, gradeSubject: null };
}
/** Untrusted local storage is validated, including legacy drafts. Legacy auto-filled
 * grades are retained for review, never silently treated as confirmed answers. */
export function readDraft(uid: string, mode: string, targetYear?: 'TY' | '5th'): SetupDraft {
  const base = initialDraft(targetYear);
  try {
    const raw = localStorage.getItem(draftKey(uid, mode));
    const legacy = !raw && localStorage.getItem(legacyDraftKey(uid, mode));
    if (!raw && !legacy) return base;
    const saved = JSON.parse(raw || legacy || '{}');
    const years = ['1st', '2nd', '3rd', 'TY', '5th', '6th', 'LCA1', 'LCA2'];
    const year = targetYear ?? (years.includes(saved.year ?? saved.yearGroup) ? saved.year ?? saved.yearGroup : null);
    const allowed = subjectsFor(year).map(s => s.name);
    const subjects = [...new Set<string>((Array.isArray(saved.subjects ?? saved.selectedSubjects) ? saved.subjects ?? saved.selectedSubjects : []).filter((name: unknown) => typeof name === 'string' && allowed.includes(name)))];
    const configs: SetupDraft['configs'] = {};
    for (const name of subjects) {
      const next = emptyChoice(year, name);
      const config = raw ? saved.configs?.[name] : cycleFor(year) === 'junior' ? saved.subjectBands?.[name] : saved.subjectConfigs?.[name];
      if (config && typeof config === 'object') {
        if (next.level !== 'common' && ['higher', 'ordinary'].includes(config.level)) next.level = config.level;
        const values = choicesFor(year, next.level);
        const current = config.current ?? config.currentGrade ?? config.currentBand;
        const target = config.target ?? config.targetGrade ?? config.targetBand;
        if (values.includes(current) || current === 'later') next.current = current;
        if (values.includes(target) || target === 'later') next.target = target;
        next.reviewed = Boolean(raw && config.reviewed === true && choiceReady(year, next));
      }
      configs[name] = next;
    }
    const categories = getActiveCategories(cycleFor(year));
    const categoryValue = saved.category ?? saved.northStarData?.category;
    const category = categories.find(c => c.id === categoryValue)?.id ?? null;
    const visionValues = saved.vision ?? saved.northStarData?.visionBoard;
    const vision = Array.isArray(visionValues) ? getVisionCardsForLevel(cycleFor(year)).filter(c => visionValues.includes(c.id)).map(c => c.id).slice(0, cycleFor(year) === 'junior' ? 3 : 5) : [];
    const steps: SetupStep[] = ['welcome', 'year', 'north', 'vision', 'subjects', 'grades', 'schedule', 'summary'];
    const legacySteps: Record<number, SetupStep> = { 1: 'welcome', 2: 'year', 3: 'north', 4: 'north', 5: 'subjects', 6: 'grades', 7: 'schedule', 8: 'schedule', 9: 'summary', 10: 'summary' };
    let step = raw && steps.includes(saved.step) ? saved.step : legacySteps[saved.step] ?? base.step;
    if (!year && step !== 'welcome') step = 'year';
    if (targetYear && ['welcome', 'year'].includes(step)) step = 'subjects';
    if (step === 'grades' && (!subjects.length || isLcaYear(year))) step = 'subjects';
    return { ...base, year, step, category, vision, subjects, configs,
      rest: DAYS_OF_WEEK.filter(day => (saved.rest ?? saved.restDays ?? base.rest).includes?.(day)),
      date: typeof (saved.date ?? saved.examDate) === 'string' ? saved.date ?? saved.examDate : base.date,
      dateConfirmed: raw ? saved.dateConfirmed === true : false,
      gradeSubject: subjects.includes(saved.gradeSubject) ? saved.gradeSubject : subjects[0] ?? null };
  } catch { return base; }
}
export function buildProfile(draft: SetupDraft): StudentSubjectProfile {
  if (!draft.year) throw new Error('Choose your school year.');
  const junior = cycleFor(draft.year) === 'junior';
  const lca = isLcaYear(draft.year);
  const subjects: StudentSubject[] = draft.subjects.map(name => {
    const config = draft.configs[name];
    if (lca) return { subjectName: name, level: 'common' };
    if (!config?.reviewed || !choiceReady(draft.year, config) || !config.level) throw new Error(`Review the level and grades for ${name}.`);
    return { subjectName: name, level: config.level,
      ...(config.current !== 'later' ? junior ? { currentBand: config.current as JCBand } : { currentGrade: config.current as Grade } : {}),
      ...(config.target !== 'later' ? junior ? { targetBand: config.target as JCBand } : { targetGrade: config.target as Grade } : {}) };
  });
  const now = new Date().toISOString();
  return { subjects, yearGroup: draft.year, curriculumLevel: cycleFor(draft.year), examStartDate: needsDate(draft.year) ? draft.date : null, restDays: [...draft.rest], createdAt: now, updatedAt: now };
}
export function buildNorthStar(draft: SetupDraft): NorthStar {
  const category = getActiveCategories(cycleFor(draft.year)).find(c => c.id === draft.category);
  if (!category || !draft.vision.length) throw new Error('Choose your motivation and at least one vision.');
  const now = new Date().toISOString();
  return { category: category.id, statement: category.description, visionBoard: [...draft.vision], authoredByStudent: false, createdAt: now, updatedAt: now, reviewedAt: now };
}
