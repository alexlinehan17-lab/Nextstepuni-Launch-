/**
 * Sample data shared by the planner's "Now" mount (kobra-review/before/PlannerBefore.tsx)
 * and its Kobra rebuild (PlannerAfter.tsx), so both panes show the same week.
 *
 * A sample Leaving Cert student, no account and no network. The week is the real
 * planner algorithm (components/timetableAlgorithm.ts, run exactly as
 * SpacedRepetitionTimetable.tsx runs it) on the grades below, so it moves with
 * the week arrows, rest days and block length just as the live planner does.
 */
import {
  allocateSessions,
  computeSubjectPrioritiesForCurriculum,
  computeWeeklyStudyTarget,
  computeWeeksUntilExam,
  generateWeeklyTimetable,
} from '../../components/timetableAlgorithm';
import { DAYS_OF_WEEK, getBlockId, toDateKey, type StudentSubject } from '../../components/subjectData';

export const DEMO_UID = 'kobra-review-demo';
export const DEMO_EXAM_DATE = '2027-06-02';
export const DEMO_REST_DAYS = ['Saturday'];
export const DEMO_DURATION = 45;
export const DEMO_SUBJECTS: StudentSubject[] = [
  { subjectName: 'English', level: 'higher', currentGrade: 'H4', targetGrade: 'H3' },
  { subjectName: 'Irish', level: 'higher', currentGrade: 'H5', targetGrade: 'H4' },
  { subjectName: 'Mathematics', level: 'higher', currentGrade: 'H5', targetGrade: 'H4' },
  { subjectName: 'Biology', level: 'higher', currentGrade: 'H3', targetGrade: 'H2' },
  { subjectName: 'Chemistry', level: 'higher', currentGrade: 'H4', targetGrade: 'H3' },
  { subjectName: 'Geography', level: 'higher', currentGrade: 'H3', targetGrade: 'H2' },
  { subjectName: 'French', level: 'higher', currentGrade: 'H5', targetGrade: 'H4' },
];
export const DEMO_SUBJECT_NAMES = DEMO_SUBJECTS.map(subject => subject.subjectName);

/** SpacedRepetitionTimetable.getWeekStartDate, copied so the harness does not pull in the auth contexts. */
export function weekStartFor(weekOffset: number): Date {
  const now = new Date(); const day = now.getDay();
  const monday = new Date(now); monday.setDate(now.getDate() + (day === 0 ? -6 : 1 - day) + weekOffset * 7); monday.setHours(0, 0, 0, 0);
  return monday;
}

export function demoPlan(weekOffset: number, restDays: string[], duration: number) {
  const weeksUntilExam = computeWeeksUntilExam(DEMO_EXAM_DATE);
  const effective = Math.max(0, weeksUntilExam - weekOffset);
  const priorities = computeSubjectPrioritiesForCurriculum(DEMO_SUBJECTS, undefined, 'senior', DEMO_EXAM_DATE);
  const weeklyTarget = computeWeeklyStudyTarget(effective);
  const allocations = allocateSessions(priorities, effective, [], duration);
  const timetable = generateWeeklyTimetable(allocations, weeksUntilExam, weekOffset, restDays, duration, [], undefined);
  const totalSessions = timetable.reduce((sum, day) => sum + day.blocks.length, 0);
  const totalMinutes = timetable.reduce((sum, day) => sum + day.blocks.reduce((minutes, block) => minutes + block.durationMinutes, 0), 0);
  return { priorities, allocations, timetable, weeklyTarget, weekStart: weekStartFor(weekOffset), totalSessions, totalMinutes };
}

/** Monday's blocks this week start as studied, so the done mark shows on first load. */
export function demoCompletions(): Record<string, string[]> {
  const { timetable, weekStart } = demoPlan(0, DEMO_REST_DAYS, DEMO_DURATION);
  const monday = timetable[DAYS_OF_WEEK.indexOf('Monday')];
  return { [toDateKey(weekStart)]: monday.blocks.map((block, index) => getBlockId(block, index)) };
}

/** The senior "Behind your plan" paragraphs, lifted from SpacedRepetitionTimetable.tsx:140. */
export const EXPLAIN_SPREAD = 'Work is spread across your available days, with repeat sessions spaced apart and room for rest.';
export const EXPLAIN_SENIOR = 'Subjects with the strongest combination of grade gap, achievable marks and topics to revisit receive more time; every subject still receives maintenance time.';
export const EXPLAIN_DETAIL = 'See the allocation in detail';

/**
 * The Catch-Up Lane subject picker for a Leaving Cert student (CatchUpLane/index.tsx:170):
 * subjectsWithContent() in catchUpLaneData.ts, display names, and the card count at
 * each level (common + that level). Counted from the data file on 27 Oct 2026 rather
 * than imported, because the data file is 2 MB.
 */
const CATCH_UP: Array<[id: string, label: string, higher: number, ordinary: number]> = [
  ['biology', 'Biology', 15, 11], ['english', 'English', 11, 10], ['mathematics', 'Mathematics', 11, 15],
  ['geography', 'Geography', 16, 12], ['home-economics', 'Home Economics', 12, 14], ['irish', 'Irish', 12, 10],
  ['business', 'Business', 10, 10], ['french', 'French', 10, 6], ['chemistry', 'Chemistry', 10, 10],
  ['physics', 'Physics', 14, 14], ['history', 'History', 13, 12], ['economics', 'Economics', 15, 10],
  ['agricultural-science', 'Agricultural Science', 13, 11], ['accounting', 'Accounting', 15, 10], ['spanish', 'Spanish', 16, 11],
  ['construction-studies', 'Construction Studies', 23, 11], ['art', 'Art', 16, 12], ['german', 'German', 15, 10],
  ['applied-mathematics', 'Applied Mathematics', 21, 14], ['politics-and-society', 'Politics & Society', 15, 10],
];
export type CatchUpLevel = 'higher' | 'ordinary';
export interface PickerOption { value: string; label: string; detail?: string }
export const catchUpOptions = (level: CatchUpLevel): PickerOption[] =>
  CATCH_UP.map(([value, label, higher, ordinary]) => ({ value, label, detail: `${level === 'higher' ? higher : ordinary} topics` }));
/** The Catch-Up level select (CatchUpLane/index.tsx:175). */
export const CATCH_UP_LEVELS: Array<{ value: CatchUpLevel; label: string }> = [
  { value: 'higher', label: 'Higher level' }, { value: 'ordinary', label: 'Ordinary level' },
];
