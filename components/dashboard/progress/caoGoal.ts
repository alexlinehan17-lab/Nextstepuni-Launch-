/**
 * "I would like to see the points bars where I'm currently at and what my
 * goal points are" (student feedback, 12 Oct 2026).
 *
 * Both numbers come from what the student has already told us — never a
 * second grade form (Alex, 5 Oct review: the CAO calculator gives way to the
 * current and target grades collected in onboarding).
 *   - Goal: the target grades chosen in onboarding / Change subjects.
 *   - Now: per subject, the most recent evidence — a recorded mock result if
 *     it is newer than the student's last grade update, otherwise the current
 *     grade they gave us.
 * Points use the app's one table (getPointsForGrade, incl. the Higher Maths
 * bonus), best six subjects.
 */
import { LC_SUBJECTS, getPointsForGrade, type Grade, type StudentSubjectProfile } from '../../subjectData';
import type { UnifiedMockResult } from '../../../types';
import { isLcaYear, type CurriculumLevel } from '../../../utils/authUtils';

/** Six H1s with the Maths bonus. */
export const CAO_MAX_POINTS = 625;

const isGrade = (value: unknown): value is Grade => typeof value === 'string' && /^[HO][1-8]$/.test(value);
const isMaths = (subjectName: string) => !!LC_SUBJECTS.find(subject => subject.name === subjectName)?.isMaths;

function bestSix(grades: { subjectName: string; grade: Grade }[]): number {
  return grades
    .map(item => getPointsForGrade(item.grade, isMaths(item.subjectName)))
    .sort((a, b) => b - a)
    .slice(0, 6)
    .reduce((sum, points) => sum + points, 0);
}

export interface CaoCurrentEvidence {
  /** Subjects whose "now" grade is a mock result newer than the profile. */
  fromMocks: number;
  /** Subjects whose "now" grade is the current grade from onboarding/settings. */
  fromProfile: number;
  /** Label of the newest mock used, e.g. "Christmas mocks". */
  latestMockLabel?: string;
}

export type CaoGoalStanding =
  | { status: 'hidden' }
  | { status: 'no-goal' }
  | { status: 'no-current'; goal: number }
  | { status: 'ready'; current: number; goal: number; gap: number; evidence: CaoCurrentEvidence };

export function caoGoalStanding(
  profile: StudentSubjectProfile | null | undefined,
  mockResults: UnifiedMockResult[] = [],
  curriculumLevel: CurriculumLevel = 'senior',
): CaoGoalStanding {
  // Junior Cycle and LCA have no CAO points; say nothing rather than print 0.
  if (!profile || curriculumLevel === 'junior' || isLcaYear(profile.yearGroup)) return { status: 'hidden' };
  const subjects = profile.subjects.filter(subject => subject.level === 'higher' || subject.level === 'ordinary');
  if (!subjects.length) return { status: 'hidden' };

  const goals = subjects.filter(subject => isGrade(subject.targetGrade))
    .map(subject => ({ subjectName: subject.subjectName, grade: subject.targetGrade as Grade }));
  if (!goals.length) return { status: 'no-goal' };
  const goal = bestSix(goals);

  const profileUpdated = Date.parse(profile.updatedAt) || 0;
  const mocksNewestFirst = [...mockResults].sort((a, b) => b.timestamp - a.timestamp);
  let fromMocks = 0, fromProfile = 0, latestMockLabel: string | undefined, latestMockTime = 0;
  const now: { subjectName: string; grade: Grade }[] = [];
  for (const subject of subjects) {
    const mock = mocksNewestFirst.find(result => result.timestamp > profileUpdated
      && result.entries.some(entry => entry.subjectName === subject.subjectName && isGrade(entry.grade)));
    const mockGrade = mock?.entries.find(entry => entry.subjectName === subject.subjectName)?.grade;
    if (mock && isGrade(mockGrade)) {
      now.push({ subjectName: subject.subjectName, grade: mockGrade });
      fromMocks += 1;
      if (mock.timestamp > latestMockTime) { latestMockTime = mock.timestamp; latestMockLabel = mock.label; }
    } else if (isGrade(subject.currentGrade)) {
      now.push({ subjectName: subject.subjectName, grade: subject.currentGrade });
      fromProfile += 1;
    }
  }
  if (!now.length) return { status: 'no-current', goal };
  const current = bestSix(now);
  return { status: 'ready', current, goal, gap: goal - current, evidence: { fromMocks, fromProfile, latestMockLabel } };
}

/** The gap in words; never colour alone. */
export function caoGapLabel(gap: number): string {
  if (gap === 0) return 'Right on your goal';
  const points = Math.abs(gap);
  return gap > 0 ? `${points} point${points === 1 ? '' : 's'} to go` : `${points} point${points === 1 ? '' : 's'} above your goal`;
}

export function caoEvidenceLabel({ fromMocks, fromProfile, latestMockLabel }: CaoCurrentEvidence): string {
  if (fromMocks && !fromProfile) return `From your latest results${latestMockLabel ? ` (${latestMockLabel})` : ''}.`;
  if (fromMocks) return `From your latest results${latestMockLabel ? ` (${latestMockLabel})` : ''} for ${fromMocks} subject${fromMocks === 1 ? '' : 's'}, and your current grades for the rest.`;
  return 'From the current grades you gave us.';
}
