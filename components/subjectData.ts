/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

// ─── Types ──────────────────────────────────────────────────────────────────

export type Grade =
  | 'H1' | 'H2' | 'H3' | 'H4' | 'H5' | 'H6' | 'H7' | 'H8'
  | 'O1' | 'O2' | 'O3' | 'O4' | 'O5' | 'O6' | 'O7' | 'O8';

export type Level = 'higher' | 'ordinary';

export interface StudentSubject {
  subjectName: string;
  level: Level;
  currentGrade: Grade;
  targetGrade: Grade;
}

export interface StudentSubjectProfile {
  subjects: StudentSubject[];
  examStartDate: string; // ISO date string, e.g. "2026-06-03"
  restDays: string[];    // e.g. ["Saturday", "Sunday"] — days with no study
  createdAt: string;
  updatedAt: string;
}

export interface StudyBlock {
  subjectName: string;
  sessionType: 'new-learning' | 'practice' | 'revision';
  durationMinutes: number;
}

export interface DaySchedule {
  day: string;
  blocks: StudyBlock[];
}

export type WeeklyTimetable = DaySchedule[];

// ─── Constants ──────────────────────────────────────────────────────────────

export interface LCSubject {
  name: string;
  group: 'languages' | 'stem' | 'business' | 'humanities' | 'practical' | 'creative';
  isMaths?: boolean;
}

export const LC_SUBJECTS: LCSubject[] = [
  // Languages
  { name: 'English', group: 'languages' },
  { name: 'Irish', group: 'languages' },
  { name: 'French', group: 'languages' },
  { name: 'German', group: 'languages' },
  { name: 'Spanish', group: 'languages' },
  { name: 'Italian', group: 'languages' },
  { name: 'Japanese', group: 'languages' },
  // STEM
  { name: 'Mathematics', group: 'stem', isMaths: true },
  { name: 'Applied Maths', group: 'stem' },
  { name: 'Physics', group: 'stem' },
  { name: 'Chemistry', group: 'stem' },
  { name: 'Biology', group: 'stem' },
  { name: 'Computer Science', group: 'stem' },
  { name: 'Ag Science', group: 'stem' },
  // Business
  { name: 'Accounting', group: 'business' },
  { name: 'Business', group: 'business' },
  { name: 'Economics', group: 'business' },
  // Humanities
  { name: 'History', group: 'humanities' },
  { name: 'Geography', group: 'humanities' },
  { name: 'Politics & Society', group: 'humanities' },
  { name: 'Religious Education', group: 'humanities' },
  { name: 'Classical Studies', group: 'humanities' },
  // Practical
  { name: 'Home Economics', group: 'practical' },
  { name: 'Construction Studies', group: 'practical' },
  { name: 'Engineering', group: 'practical' },
  { name: 'DCG', group: 'practical' },
  { name: 'Technology', group: 'practical' },
  // Creative
  { name: 'Art', group: 'creative' },
  { name: 'Music', group: 'creative' },
  { name: 'Design & Communication Graphics', group: 'creative' },
];

export const SUBJECT_GROUP_LABELS: Record<LCSubject['group'], string> = {
  languages: 'Languages',
  stem: 'STEM',
  business: 'Business',
  humanities: 'Humanities',
  practical: 'Practical',
  creative: 'Creative',
};

export const HIGHER_GRADES: Grade[] = ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8'];
export const ORDINARY_GRADES: Grade[] = ['O1', 'O2', 'O3', 'O4', 'O5', 'O6', 'O7', 'O8'];

export const HIGHER_POINTS: Record<string, number> = {
  H1: 100, H2: 88, H3: 77, H4: 66, H5: 56, H6: 46, H7: 37, H8: 0,
};

export const ORDINARY_POINTS: Record<string, number> = {
  O1: 56, O2: 46, O3: 37, O4: 28, O5: 20, O6: 12, O7: 0, O8: 0,
};

export const DAYS_OF_WEEK = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'] as const;

// ─── Helpers ────────────────────────────────────────────────────────────────

/**
 * Returns CAO points for a given grade, including the +25 Maths bonus for Higher Level H6+.
 */
export function getPointsForGrade(grade: Grade, isMaths: boolean = false): number {
  let points = 0;
  if (grade.startsWith('H')) {
    points = HIGHER_POINTS[grade] ?? 0;
  } else {
    points = ORDINARY_POINTS[grade] ?? 0;
  }
  // Maths HL bonus: +25 for H6 and above (H1-H6)
  if (isMaths && grade.startsWith('H') && HIGHER_POINTS[grade] >= 46) {
    points += 25;
  }
  return points;
}

/**
 * Returns the grade options for a given level.
 */
export function getGradesForLevel(level: Level): Grade[] {
  return level === 'higher' ? HIGHER_GRADES : ORDINARY_GRADES;
}

/**
 * Returns the grade index within its scale (0 = best, 7 = worst).
 */
export function getGradeIndex(grade: Grade): number {
  if (grade.startsWith('H')) {
    return HIGHER_GRADES.indexOf(grade);
  }
  return ORDINARY_GRADES.indexOf(grade);
}

/**
 * Check if target grade is at same level or better than current.
 */
export function isValidTarget(current: Grade, target: Grade): boolean {
  // Must be same level prefix
  if (current.charAt(0) !== target.charAt(0)) return false;
  return getGradeIndex(target) <= getGradeIndex(current);
}
