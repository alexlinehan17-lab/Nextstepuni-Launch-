/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

// ─── Types ──────────────────────────────────────────────────────────────────

export type Grade =
  | 'H1' | 'H2' | 'H3' | 'H4' | 'H5' | 'H6' | 'H7' | 'H8'
  | 'O1' | 'O2' | 'O3' | 'O4' | 'O5' | 'O6' | 'O7' | 'O8'
  | LcvpGrade;

/** LCVP Link Modules is one common-level exam graded Distinction / Merit /
 *  Pass, and CAO counts it among the best six (66 / 46 / 28 points). It is the
 *  only established Leaving Cert subject on this scale, so 'common' level in
 *  the LC programme means these grades. */
export type LcvpGrade = 'Distinction' | 'Merit' | 'Pass';

// LC subjects use 'higher' | 'ordinary'. Junior Cycle subjects without an
// H/O choice (all JC subjects except English / Irish / Mathematics) carry
// level 'common'. Treat this as a runtime flag — LC code that branches on
// level === 'higher' / 'ordinary' continues to work because no LC subject
// ever has level === 'common'.
export type Level = 'higher' | 'ordinary' | 'common';

// LC entries set currentGrade / targetGrade. JC entries set currentBand /
// targetBand. Discriminate at the call site via the profile-level
// curriculumLevel (or check which pair of fields is populated). Don't try
// to map between the two — they represent different grading scales.
export interface StudentSubject {
  subjectName: string;
  level: Level;
  // LC only:
  currentGrade?: Grade;
  targetGrade?: Grade;
  // JC only:
  currentBand?: JCBand;
  targetBand?: JCBand;
}

// Junior Cycle expansion (Phase 1): YearGroup widened to cover JC years
// (1st/2nd/3rd) and Transition Year (4th) alongside the existing senior
// years. TY is mapped to senior content for now per the audit decision —
// revisit post-launch.
//
// Phase 8: 'graduated' added as a forward-only soft state — set when a
// 6th-year user explicitly marks themselves as having finished their
// Leaving Cert via Settings → School Year. Graduated users retain full
// app access; the value just drives a different label in Settings and a
// muted treatment on the GC dashboard.
export type YearGroup = '1st' | '2nd' | '3rd' | 'TY' | '5th' | '6th' | 'LCA1' | 'LCA2' | 'graduated';

import type { CurriculumLevel } from '../utils/authUtils';

export interface StudentSubjectProfile {
  subjects: StudentSubject[];
  examStartDate: string | null; // ISO date string, e.g. "2026-06-03". null for 1st/2nd-year JC who have no imminent exam.
  restDays: string[];    // e.g. ["Saturday", "Sunday"] — days with no study
  defaultBlockDuration?: number; // minutes per study block (default 45)
  yearGroup?: YearGroup;
  curriculumLevel?: CurriculumLevel; // mirrored from users/{uid}.curriculumLevel for code that only has profile in scope
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
  /** Levels the SEC examines. Omitted means Higher and Ordinary. The
   *  non-curricular EU languages and Ukrainian are Higher only; LCVP Link
   *  Modules is a single common-level paper. */
  levels?: Level[];
}


/** Leaving Cert Applied courses. Names match the Paper Trail archive display
 *  names (paperTrailData cycle 'lca') so a student's chosen subjects link
 *  straight to their papers. All LCA courses are assessed at common level —
 *  credits (Distinction / Merit / Pass), not H/O grades. */
export const LCA_SUBJECTS: LCSubject[] = [
  // Languages & communication
  { name: 'English and Communications', group: 'languages' },
  { name: 'Gaeilge Chumarsáideach', group: 'languages' },
  { name: 'French', group: 'languages' },
  { name: 'German', group: 'languages' },
  { name: 'Spanish', group: 'languages' },
  { name: 'Italian', group: 'languages' },
  { name: 'Sign Language', group: 'languages' },
  // STEM
  { name: 'Mathematical Applications', group: 'stem', isMaths: true },
  { name: 'Information & Communication Tech.', group: 'stem' },
  // Business / vocational
  { name: 'Office Admin And Customer', group: 'business' },
  { name: 'Hotel / Catering & Tourism', group: 'business' },
  // Humanities
  { name: 'Social Education', group: 'humanities' },
  // Practical / vocational specialisms
  { name: 'Engineering', group: 'practical' },
  { name: 'Graphics And Construction Studies', group: 'practical' },
  { name: 'Agriculture / Horticulture', group: 'practical' },
  { name: 'Childcare / Community Care', group: 'practical' },
  { name: 'Hair And Beauty', group: 'practical' },
  { name: 'Active Leisure Studies', group: 'practical' },
  { name: 'Technology', group: 'practical' },
  // Creative
  { name: 'Crafts & Design', group: 'creative' },
];

const HIGHER_ONLY: Level[] = ['higher'];

/** Established Leaving Cert subjects a student can sit. Names match the Paper
 *  Trail archive display names or their aliases (paperTrailData cycle 'lc') and
 *  resolve through curriculumRegistry's resolveSubjectId, so a chosen subject
 *  links to its papers, Mark Bank deck and Topic Atlas
 *  (test/subjectCatalogueLinks.test.ts holds every entry to that). */
export const LC_SUBJECTS: LCSubject[] = [
  // Languages
  { name: 'English', group: 'languages' },
  { name: 'Irish', group: 'languages' },
  { name: 'French', group: 'languages' },
  { name: 'German', group: 'languages' },
  { name: 'Spanish', group: 'languages' },
  { name: 'Italian', group: 'languages' },
  { name: 'Japanese', group: 'languages' },
  { name: 'Mandarin Chinese', group: 'languages' },
  { name: 'Russian', group: 'languages' },
  { name: 'Arabic', group: 'languages' },
  { name: 'Lithuanian', group: 'languages' },
  { name: 'Polish', group: 'languages' },
  { name: 'Portuguese', group: 'languages' },
  { name: 'Latin', group: 'languages' },
  { name: 'Ancient Greek', group: 'languages' },
  { name: 'Hebrew Studies', group: 'languages' },
  // Non-curricular EU languages and Ukrainian: examined at Higher level only,
  // for students with a home or community connection to the language.
  { name: 'Bulgarian', group: 'languages', levels: HIGHER_ONLY },
  { name: 'Croatian', group: 'languages', levels: HIGHER_ONLY },
  { name: 'Czech', group: 'languages', levels: HIGHER_ONLY },
  { name: 'Danish', group: 'languages', levels: HIGHER_ONLY },
  { name: 'Dutch', group: 'languages', levels: HIGHER_ONLY },
  { name: 'Estonian', group: 'languages', levels: HIGHER_ONLY },
  { name: 'Finnish', group: 'languages', levels: HIGHER_ONLY },
  { name: 'Hungarian', group: 'languages', levels: HIGHER_ONLY },
  { name: 'Latvian', group: 'languages', levels: HIGHER_ONLY },
  { name: 'Maltese', group: 'languages', levels: HIGHER_ONLY },
  { name: 'Modern Greek', group: 'languages', levels: HIGHER_ONLY },
  { name: 'Romanian', group: 'languages', levels: HIGHER_ONLY },
  { name: 'Slovakian', group: 'languages', levels: HIGHER_ONLY },
  { name: 'Slovenian', group: 'languages', levels: HIGHER_ONLY },
  { name: 'Swedish', group: 'languages', levels: HIGHER_ONLY },
  { name: 'Ukrainian', group: 'languages', levels: HIGHER_ONLY },
  // STEM
  { name: 'Mathematics', group: 'stem', isMaths: true },
  { name: 'Applied Maths', group: 'stem' },
  { name: 'Physics', group: 'stem' },
  { name: 'Chemistry', group: 'stem' },
  { name: 'Physics & Chemistry', group: 'stem' },
  { name: 'Biology', group: 'stem' },
  { name: 'Computer Science', group: 'stem' },
  { name: 'Ag Science', group: 'stem' },
  // Business
  { name: 'Accounting', group: 'business' },
  { name: 'Business', group: 'business' },
  { name: 'Economics', group: 'business' },
  { name: 'LCVP Link Modules', group: 'business', levels: ['common'] },
  // Humanities
  { name: 'History', group: 'humanities' },
  { name: 'Geography', group: 'humanities' },
  { name: 'Politics & Society', group: 'humanities' },
  { name: 'Religious Education', group: 'humanities' },
  { name: 'Classical Studies', group: 'humanities' },
  { name: 'Climate Action and Sustainable Development', group: 'humanities' },
  // Practical
  { name: 'Home Economics', group: 'practical' },
  { name: 'Construction Studies', group: 'practical' },
  { name: 'Engineering', group: 'practical' },
  { name: 'DCG', group: 'practical' },
  { name: 'Technology', group: 'practical' },
  { name: 'Physical Education', group: 'practical' },
  // Creative
  { name: 'Art', group: 'creative' },
  { name: 'Music', group: 'creative' },
  { name: 'Drama, Film and Theatre Studies', group: 'creative' },
];

const DEFAULT_LC_LEVELS: Level[] = ['higher', 'ordinary'];

/** The levels a Leaving Cert subject is examined at, in display order. */
export function lcSubjectLevels(name: string): Level[] {
  return LC_SUBJECTS.find(subject => subject.name === name)?.levels ?? DEFAULT_LC_LEVELS;
}

export const LEVEL_LABELS: Record<Level, string> = { higher: 'Higher', ordinary: 'Ordinary', common: 'Common' };

/** One line for a subject whose level is fixed, or null when the student chooses. */
export function fixedLevelNote(name: string): string | null {
  const levels = lcSubjectLevels(name);
  if (levels.length !== 1) return null;
  return levels[0] === 'common'
    ? `${name} is one common-level exam, graded Distinction, Merit or Pass.`
    : `${name} is examined at Higher level only.`;
}

export const SUBJECT_GROUP_LABELS: Record<LCSubject['group'], string> = {
  languages: 'Languages',
  stem: 'STEM',
  business: 'Business',
  humanities: 'Humanities',
  practical: 'Practical',
  creative: 'Creative',
};

// ─── Junior Cycle Subjects (Phase 1) ───────────────────────────────────────
//
// Parallel to LC_SUBJECTS for use during onboarding when curriculumLevel
// === 'junior'. Subjects are grouped into the same 6 group buckets as LC
// so the existing GROUP_DOT_HEX + group labels work unchanged.
//
// JC has Higher/Ordinary level only for English, Irish, and Mathematics
// since the 2017–2022 NCCA reforms. All other JC subjects are at Common
// Level — `jcHasLevelChoice: false`.
//
// Subjects that exist in both LC and JC under different names are kept as
// separate entries in LC_SUBJECTS / JC_SUBJECTS (e.g., LC "Business" vs
// JC "Business Studies"; LC "Construction Studies" vs JC "Materials
// Technology (Wood)"; LC "DCG" vs JC "Graphics"). We never need to map
// across — the student picks from one list based on their curriculum.

export interface JCSubject {
  name: string;
  group: LCSubject['group'];
  isMaths?: boolean;
  jcHasLevelChoice?: boolean; // true only for English / Irish / Mathematics
}

export const JC_SUBJECTS: JCSubject[] = [
  // Languages
  { name: 'English', group: 'languages', jcHasLevelChoice: true },
  { name: 'Irish', group: 'languages', jcHasLevelChoice: true },
  { name: 'French', group: 'languages' },
  { name: 'German', group: 'languages' },
  { name: 'Spanish', group: 'languages' },
  { name: 'Italian', group: 'languages' },
  // STEM
  { name: 'Mathematics', group: 'stem', isMaths: true, jcHasLevelChoice: true },
  { name: 'Science', group: 'stem' }, // single integrated subject at JC (not split into Biology/Chemistry/Physics)
  // Business
  { name: 'Business Studies', group: 'business' },
  // Humanities
  { name: 'History', group: 'humanities' },
  { name: 'Geography', group: 'humanities' },
  { name: 'CSPE', group: 'humanities' },        // Civic, Social and Political Education
  { name: 'SPHE', group: 'humanities' },        // Social, Personal and Health Education
  { name: 'Religious Education', group: 'humanities' },
  { name: 'Classical Studies', group: 'humanities' },
  { name: 'Latin', group: 'humanities' },
  // Practical
  { name: 'Home Economics', group: 'practical' },
  { name: 'Materials Technology (Wood)', group: 'practical' },
  { name: 'Metalwork', group: 'practical' },
  { name: 'Graphics', group: 'practical' },
  { name: 'Technology', group: 'practical' },
  { name: 'Physical Education', group: 'practical' },
  // Creative
  { name: 'Art', group: 'creative' },
  { name: 'Music', group: 'creative' },
];

// ─── Junior Cycle grading scale ────────────────────────────────────────────
//
// NCCA descriptor bands. No CAO-points equivalent — points logic
// (getPointsForGrade, HIGHER_POINTS, ORDINARY_POINTS) stays senior-only.
// JC bands are rendered as labels with optional percentage ranges; the UI
// for picking these lands in Phase 4.

export type JCBand =
  | 'Distinction'
  | 'Higher Merit'
  | 'Merit'
  | 'Achieved'
  | 'Partially Achieved'
  | 'Not Graded';

export const JC_BANDS: JCBand[] = [
  'Distinction',
  'Higher Merit',
  'Merit',
  'Achieved',
  'Partially Achieved',
  'Not Graded',
];

export const JC_BAND_RANGES: Record<JCBand, [number, number]> = {
  'Distinction': [90, 100],
  'Higher Merit': [75, 89],
  'Merit': [55, 74],
  'Achieved': [40, 54],
  'Partially Achieved': [20, 39],
  'Not Graded': [0, 19],
};

export function getStudentGradingScale(level: CurriculumLevel): 'lc-points' | 'jc-bands' {
  return level === 'junior' ? 'jc-bands' : 'lc-points';
}

export const HIGHER_GRADES: Grade[] = ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8'];
export const ORDINARY_GRADES: Grade[] = ['O1', 'O2', 'O3', 'O4', 'O5', 'O6', 'O7', 'O8'];

export const HIGHER_POINTS: Record<string, number> = {
  H1: 100, H2: 88, H3: 77, H4: 66, H5: 56, H6: 46, H7: 37, H8: 0,
};

export const ORDINARY_POINTS: Record<string, number> = {
  O1: 56, O2: 46, O3: 37, O4: 28, O5: 20, O6: 12, O7: 0, O8: 0,
};

export const LCVP_GRADES: Grade[] = ['Distinction', 'Merit', 'Pass'];

export const LCVP_POINTS: Record<string, number> = {
  Distinction: 66, Merit: 46, Pass: 28,
};

export type GradeScale = 'higher' | 'ordinary' | 'lcvp';

/** Which scale a grade belongs to, read from the grade itself. */
export function gradeScale(grade: Grade | undefined | null): GradeScale | null {
  if (!grade || typeof grade !== 'string') return null;
  if (Object.prototype.hasOwnProperty.call(LCVP_POINTS, grade)) return 'lcvp';
  if (grade.startsWith('H')) return 'higher';
  if (grade.startsWith('O')) return 'ordinary';
  return null;
}

/** Every grade on the same scale as `grade`, best first. */
export function gradeLadder(grade: Grade | undefined | null): Grade[] {
  const scale = gradeScale(grade);
  return scale === 'lcvp' ? LCVP_GRADES : scale === 'higher' ? HIGHER_GRADES : ORDINARY_GRADES;
}

/** A sensible starting pair (current, target) on a level's scale. */
export function defaultGradesForLevel(level: Level): { currentGrade: Grade; targetGrade: Grade } {
  const grades = getGradesForLevel(level);
  return level === 'common'
    ? { currentGrade: 'Merit', targetGrade: 'Distinction' }
    : { currentGrade: grades[3], targetGrade: grades[1] };
}

/** A new LC subject's starting level and grades, respecting fixed levels. */
export function defaultSubjectConfig(name: string): { level: Level; currentGrade: Grade; targetGrade: Grade } {
  const level = lcSubjectLevels(name)[0];
  return { level, ...defaultGradesForLevel(level) };
}

export const DAYS_OF_WEEK = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'] as const;

// ─── Helpers ────────────────────────────────────────────────────────────────

/**
 * Returns CAO points for a given grade, including the +25 Maths bonus for Higher Level H6+.
 */
export function getPointsForGrade(grade: Grade | undefined | null, isMaths: boolean = false): number {
  // JC subjects don't carry currentGrade/targetGrade (they use bands), so
  // call sites that iterate a mixed cohort may pass undefined. Guard here
  // rather than at every caller. Returns 0 cleanly — calculateCAOPoints +
  // getStudentCurrentCAO end up giving JC students a CAO total of 0, which
  // is the correct semantic (no LC points to compute).
  if (!grade || typeof grade !== 'string') return 0;
  if (gradeScale(grade) === 'lcvp') return LCVP_POINTS[grade];
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
  if (level === 'common') return LCVP_GRADES;
  return level === 'higher' ? HIGHER_GRADES : ORDINARY_GRADES;
}

/**
 * Returns the grade index within its scale (0 = best, 7 = worst).
 * JC subjects don't carry an LC grade — return a sentinel mid-band so
 * downstream comparators don't crash. Same defensive pattern as
 * getPointsForGrade.
 */
export function getGradeIndex(grade: Grade | undefined): number {
  if (!grade) return ORDINARY_GRADES.length; // off-scale → lowest priority
  return gradeLadder(grade).indexOf(grade);
}

/**
 * Check if target grade is at same level or better than current.
 */
export function isValidTarget(current: Grade, target: Grade): boolean {
  // Must be on the same scale
  if (gradeScale(current) !== gradeScale(target)) return false;
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
    const grades = gradeLadder(sub.currentGrade);
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
