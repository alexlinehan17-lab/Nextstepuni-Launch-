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

export type YearGroup = '5th' | '6th';

export interface StudentSubjectProfile {
  subjects: StudentSubject[];
  examStartDate: string; // ISO date string, e.g. "2026-06-03"
  restDays: string[];    // e.g. ["Saturday", "Sunday"] — days with no study
  defaultBlockDuration?: number; // minutes per study block (default 45)
  yearGroup?: YearGroup; // "5th" or "6th" year — used for event filtering
  createdAt: string;
  updatedAt: string;
}

export interface StudyBlock {
  subjectName: string;
  sessionType: 'new-learning' | 'practice' | 'revision';
  durationMinutes: number;
  suggestedTopics?: string[];
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
  let points = grade.startsWith('H')
    ? (HIGHER_POINTS[grade] ?? 0)
    : (ORDINARY_POINTS[grade] ?? 0);
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

// ─── Grade Bargains Calculator ──────────────────────────────────────────────

export interface Bargain {
  subjectName: string;
  fromGrade: Grade;
  toGrade: Grade;
  pointsGain: number;
  isMathsBonus: boolean;
  effortHint: string;
}

export function computeBargains(profile: StudentSubjectProfile): Bargain[] {
  const bargains: Bargain[] = [];

  for (const sub of profile.subjects) {
    const isMaths = LC_SUBJECTS.find(lc => lc.name === sub.subjectName)?.isMaths ?? false;
    const grades = sub.level === 'higher' ? HIGHER_GRADES : ORDINARY_GRADES;
    const currentIdx = grades.indexOf(sub.currentGrade);
    if (currentIdx <= 0) continue;

    const nextGrade = grades[currentIdx - 1];
    const currentPoints = getPointsForGrade(sub.currentGrade, isMaths);
    const nextPoints = getPointsForGrade(nextGrade, isMaths);
    const gain = nextPoints - currentPoints;

    // Check if maths bonus kicks in
    const mathsBonusKicksIn = isMaths && sub.level === 'higher'
      && getPointsForGrade(sub.currentGrade, false) < 46
      && getPointsForGrade(nextGrade, false) >= 46;

    // Effort hint based on grade gap
    let effortHint = '4-6 focused study sessions';
    if (sub.currentGrade.endsWith('1') || sub.currentGrade.endsWith('2')) {
      effortHint = '6-10 focused study sessions';
    } else if (sub.currentGrade.endsWith('7') || sub.currentGrade.endsWith('8')) {
      effortHint = '2-4 focused study sessions';
    }

    if (gain > 0) {
      bargains.push({
        subjectName: sub.subjectName,
        fromGrade: sub.currentGrade,
        toGrade: nextGrade,
        pointsGain: gain,
        isMathsBonus: mathsBonusKicksIn,
        effortHint,
      });
    }
  }

  bargains.sort((a, b) => b.pointsGain - a.pointsGain);
  return bargains;
}

// ─── Timetable Completion Tracking ──────────────────────────────────────────

/** Completions keyed by ISO date "YYYY-MM-DD" → array of block IDs */
export type TimetableCompletions = Record<string, string[]>;

export interface TimetableStreak {
  currentStreak: number;
  lastActiveDate: string; // "YYYY-MM-DD" or ""
  longestStreak: number;
}

/** Returns a stable block ID: "SubjectName|sessionType|blockIndex" */
export function getBlockId(block: StudyBlock, blockIndex: number): string {
  return `${block.subjectName}|${block.sessionType}|${blockIndex}`;
}

/** Returns "YYYY-MM-DD" for a Date */
export function toDateKey(date: Date): string {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, '0');
  const d = String(date.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}
