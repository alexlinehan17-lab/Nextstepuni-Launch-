/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * What a student told us in onboarding, read back from the saved profile and
 * North Star ("i wish there was a view for all the stuff I did on
 * onboarding", workshop feedback 12 Oct 2026). Pure, so the page stays a view.
 */

import { DAYS_OF_WEEK, LC_SUBJECTS, getPointsForGrade, type Grade, type StudentSubjectProfile, type YearGroup } from '../subjectData';
import { NORTH_STAR_CATEGORIES, VISION_CARDS, VISION_CARD_ART } from '../../northStarData';
import { isLcaYear, yearGroupLabel, yearGroupToCurriculumLevel } from '../../utils/authUtils';
import { getSubjectFill } from '../../utils/subjectColors';
import type { NorthStar } from '../../types';

export interface SetupSubjectRow {
  name: string;
  level: string;
  current: string | null;
  target: string | null;
  fill: string;
}

export interface SetupSummary {
  year: { label: string; cycle: string } | null;
  exam: { iso: string; label: string; daysAway: number } | null;
  subjects: SetupSubjectRow[];
  /** Leaving Cert only: best six, with the maths bonus, as onboarding counts them. */
  points: { current: number; target: number; counted: number } | null;
  week: { day: string; short: string; study: boolean }[];
  studyDays: number;
  blockMinutes: number | null;
  northStar: { title: string; statement: string; vision: { id: string; label: string; art: string | null }[] } | null;
}

const LEVEL_LABEL = { higher: 'Higher', ordinary: 'Ordinary', common: 'Common' } as const;

export function setupYearLabel(year: YearGroup | undefined): string {
  if (year === 'LCA1') return 'LCA Year 1';
  if (year === 'LCA2') return 'LCA Year 2';
  return yearGroupLabel(year);
}

function cycleLabel(year: YearGroup): string {
  if (year === 'graduated') return 'Finished school';
  if (isLcaYear(year)) return 'Leaving Cert Applied';
  return yearGroupToCurriculumLevel(year) === 'junior' ? 'Junior Cycle' : 'Leaving Cert';
}

const bestSix = (grades: (Grade | undefined)[], maths: boolean[]) =>
  Math.min(625, grades
    .map((grade, index) => getPointsForGrade(grade, maths[index]))
    .sort((a, b) => b - a)
    .slice(0, 6)
    .reduce((sum, points) => sum + points, 0));

export function summariseSetup(
  profile: StudentSubjectProfile | null,
  northStar: NorthStar | null,
  yearGroup?: YearGroup,
  today = new Date(),
): SetupSummary {
  const year = yearGroup ?? profile?.yearGroup;
  const subjects: SetupSubjectRow[] = (profile?.subjects ?? []).map(subject => ({
    name: subject.subjectName,
    level: LEVEL_LABEL[subject.level] ?? subject.level,
    current: subject.currentGrade ?? subject.currentBand ?? null,
    target: subject.targetGrade ?? subject.targetBand ?? null,
    fill: getSubjectFill(subject.subjectName),
  }));

  const leavingCert = year && !isLcaYear(year) && year !== 'graduated' && yearGroupToCurriculumLevel(year) === 'senior';
  const graded = (profile?.subjects ?? []).filter(s => s.currentGrade && s.targetGrade);
  const maths = graded.map(s => !!LC_SUBJECTS.find(lc => lc.name === s.subjectName)?.isMaths);
  const points = leavingCert && graded.length
    ? { current: bestSix(graded.map(s => s.currentGrade), maths), target: bestSix(graded.map(s => s.targetGrade), maths), counted: graded.length }
    : null;

  let exam: SetupSummary['exam'] = null;
  if (profile?.examStartDate) {
    const date = new Date(`${profile.examStartDate}T00:00:00`);
    if (!Number.isNaN(date.getTime())) {
      const start = new Date(today.getFullYear(), today.getMonth(), today.getDate());
      exam = {
        iso: profile.examStartDate,
        label: date.toLocaleDateString('en-IE', { day: 'numeric', month: 'long', year: 'numeric' }),
        daysAway: Math.ceil((date.getTime() - start.getTime()) / 86_400_000),
      };
    }
  }

  const rest = new Set(profile?.restDays ?? []);
  const week = DAYS_OF_WEEK.map(day => ({ day, short: day.slice(0, 3), study: !rest.has(day) }));

  let summaryNorthStar: SetupSummary['northStar'] = null;
  if (northStar) {
    const category = NORTH_STAR_CATEGORIES.find(c => c.id === northStar.category);
    summaryNorthStar = {
      title: category?.label ?? 'Your North Star',
      statement: northStar.statement || category?.description || '',
      vision: (northStar.visionBoard ?? []).flatMap(id => {
        const card = VISION_CARDS.find(c => c.id === id);
        return card ? [{ id, label: card.label, art: VISION_CARD_ART[id] ?? null }] : [];
      }),
    };
  }

  return {
    year: year ? { label: setupYearLabel(year), cycle: cycleLabel(year) } : null,
    exam,
    subjects,
    points,
    week,
    studyDays: week.filter(d => d.study).length,
    blockMinutes: profile?.defaultBlockDuration ?? null,
    northStar: summaryNorthStar,
  };
}
