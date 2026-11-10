/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

// ─── Types ──────────────────────────────────────────────────────────────────

export type Grade =
  | 'H1' | 'H2' | 'H3' | 'H4' | 'H5' | 'H6' | 'H7' | 'H8'
  | 'O1' | 'O2' | 'O3' | 'O4' | 'O5' | 'O6' | 'O7' | 'O8'
  | 'F1' | 'F2' | 'F3' | 'F4' | 'F5' | 'F6' | 'F7' | 'F8'
  | LcvpGrade;

/** LCVP Link Modules is one common-level exam graded Distinction / Merit /
 *  Pass, and CAO counts it among the best six (66 / 46 / 28 points). It is the
 *  only established Leaving Cert subject on this scale, so 'common' level in
 *  the LC programme means these grades. */
export type LcvpGrade = 'Distinction' | 'Merit' | 'Pass';

// LC subjects use 'higher' | 'ordinary', plus 'foundation' for Mathematics and
// Irish (the only LC subjects the SEC examines at Foundation level) and
// 'common' for LCVP Link Modules. Junior Cycle subjects without an
// H/O choice (all JC subjects except English / Irish / Mathematics) carry
// level 'common'. Treat this as a runtime flag — LC code that branches on
// level === 'higher' / 'ordinary' must keep common-level LCVP and non-exam
// courses separate; only LCVP awards Distinction / Merit / Pass exam grades.
export type Level = 'higher' | 'ordinary' | 'foundation' | 'common';

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
  /** Persisted identity; legacy blocks retain the old fallback. */
  id?: string;
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
   *  non-curricular EU languages and Ukrainian are Higher only; Mathematics
   *  and Irish add Foundation; LCVP Link Modules is a single common-level paper. */
  levels?: Level[];
  /** Other names students search by, including the name the subject takes
   *  for a later exam cohort (e.g. Construction Technology from 2028). */
  aliases?: string[];
  /** Current official label; `name` remains compatible with saved profiles. */
  label?: string;
  /** No SEC written paper. These courses do not use exam grade targets. */
  noWrittenExam?: boolean;
  /** An externally assessed project can still award national exam grades (JC Visual Art). */
  examGrades?: boolean;
  /** LCA Social Education: final exam ended for the cohort entering in 2025. */
  lastWrittenExamYear?: number;
  /** Explicit route for separately certified LCE subjects selected by LCA students. */
  establishedSubject?: string;
  /** JC paper identity, including current names for legacy saved choices. */
  paperSubjectId?: string;
  shortCourseLevel?: 1 | 2 | 3;
}


/** Leaving Cert Applied courses (LCA Programme Statement, Dec 2024). Courses
 *  with an SEC final exam use the Paper Trail archive display names
 *  (paperTrailData cycle 'lca') so a student's chosen subjects link straight to
 *  their papers. Courses assessed only by key assignments are marked
 *  `noWrittenExam`. LCA students may also take Leaving Cert Mathematics at any
 *  level and separately certified LCE modern foreign languages. LCA courses are assessed at common level: credits
 *  (Distinction / Merit / Pass), not H/O grades. */
export const LCA_SUBJECTS: LCSubject[] = [
  // Languages & communication
  { name: 'English and Communications', group: 'languages', aliases: ['English and Communication'] },
  { name: 'Gaeilge Chumarsáideach', group: 'languages', aliases: ['Gaeilge', 'Irish'] },
  { name: 'French', group: 'languages' },
  { name: 'German', group: 'languages' },
  { name: 'Spanish', group: 'languages' },
  { name: 'Italian', group: 'languages' },
  { name: 'Sign Language', group: 'languages' },
  // STEM
  { name: 'Mathematical Applications', group: 'stem', isMaths: true },
  { name: 'Leaving Cert Maths', group: 'stem', establishedSubject: 'Mathematics', levels: ['higher', 'ordinary', 'foundation'], aliases: ['Mathematics', 'Ordinary Maths', 'Maths'] },
  { name: 'Information & Communication Tech.', group: 'stem', aliases: ['ICT', 'Information and Communication Technology', 'Information and Communications Technology', 'Information and Communications Technology (Voc. Specialism)'] },
  { name: 'Introduction to ICT', group: 'stem', noWrittenExam: true, aliases: ['Introduction to Information and Communication Technology', 'Introduction to Information and Communications Technology'] },
  { name: 'Science', group: 'stem', noWrittenExam: true },
  // Business / vocational
  { name: 'Vocational Preparation & Guidance', group: 'business', noWrittenExam: true, aliases: ['VPG', 'Vocational Preparation and Guidance', 'Vocational Studies', 'Vocational Studies and Preparation'] },
  { name: 'Office Admin And Customer', group: 'business', aliases: ['Office Administration and Customer Care'] },
  { name: 'Hotel / Catering & Tourism', group: 'business', aliases: ['Hotel, Catering and Tourism', 'Hotel Catering and Tourism'] },
  // Humanities
  { name: 'Social Education', group: 'humanities', lastWrittenExamYear: 2026 },
  { name: 'SPHE', group: 'humanities', noWrittenExam: true, aliases: ['Social Personal and Health Education'] },
  { name: 'Religious Education', group: 'humanities', noWrittenExam: true },
  // Practical / vocational specialisms
  { name: 'Engineering', group: 'practical' },
  { name: 'Graphics And Construction Studies', group: 'practical', aliases: ['Wood Technology', 'Woodwork', 'Woodcraft'] },
  { name: 'Agriculture / Horticulture', group: 'practical', aliases: ['Agriculture/ Horticulture', 'Agriculture/Horticulture'] },
  { name: 'Childcare / Community Care', group: 'practical', aliases: ['Childcare/Community Care'] },
  { name: 'Hair And Beauty', group: 'practical' },
  { name: 'Active Leisure Studies', group: 'practical' },
  { name: 'Leisure and Recreation', group: 'practical', noWrittenExam: true },
  { name: 'Technology', group: 'practical' },
  // Creative
  { name: 'Crafts & Design', group: 'creative', aliases: ['Craft and Design'] },
  // Keep the old umbrella choice for saved profiles, alongside its official courses.
  { name: 'Arts Education', group: 'creative', noWrittenExam: true },
  { name: 'Dance', group: 'creative', noWrittenExam: true },
  { name: 'Drama', group: 'creative', noWrittenExam: true },
  { name: 'Music', group: 'creative', noWrittenExam: true },
  { name: 'Visual Art', group: 'creative', noWrittenExam: true, aliases: ['Visual Arts', 'Art'] },
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
  { name: 'Irish', group: 'languages', levels: ['higher', 'ordinary', 'foundation'], aliases: ['Gaeilge'] },
  { name: 'French', group: 'languages' },
  { name: 'German', group: 'languages' },
  { name: 'Spanish', group: 'languages' },
  { name: 'Italian', group: 'languages' },
  { name: 'Japanese', group: 'languages' },
  { name: 'Mandarin Chinese', group: 'languages', aliases: ['Chinese'] },
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
  { name: 'Mathematics', group: 'stem', isMaths: true, levels: ['higher', 'ordinary', 'foundation'], aliases: ['Maths'] },
  { name: 'Applied Maths', group: 'stem', aliases: ['Applied Mathematics'] },
  { name: 'Physics', group: 'stem' },
  { name: 'Chemistry', group: 'stem' },
  { name: 'Physics & Chemistry', group: 'stem', aliases: ['Physics and Chemistry', 'Chemical and Physical Science'] },
  { name: 'Biology', group: 'stem' },
  { name: 'Computer Science', group: 'stem' },
  { name: 'Ag Science', group: 'stem', aliases: ['Agricultural Science'] },
  // Business
  { name: 'Accounting', group: 'business' },
  { name: 'Business', group: 'business' },
  { name: 'Economics', group: 'business' },
  { name: 'LCVP Link Modules', group: 'business', levels: ['common'], aliases: ['LCVP', 'Link Modules', 'Life, Community and Work'] },
  // Humanities
  { name: 'History', group: 'humanities' },
  { name: 'Geography', group: 'humanities' },
  { name: 'Politics & Society', group: 'humanities', aliases: ['Politics and Society'] },
  { name: 'Religious Education', group: 'humanities' },
  { name: 'Classical Studies', group: 'humanities' },
  { name: 'Climate Action and Sustainable Development', group: 'humanities', aliases: ['CASD'] },
  // Practical
  { name: 'Home Economics', group: 'practical', aliases: ['Home Ec'] },
  { name: 'Construction Studies', group: 'practical', aliases: ['Construction Technology'] },
  { name: 'Engineering', group: 'practical' },
  { name: 'DCG', group: 'practical', aliases: ['Design and Communication Graphics', 'Applied Graphics and Design'] },
  { name: 'Technology', group: 'practical' },
  { name: 'Physical Education', group: 'practical', aliases: ['PE', 'LCPE'] },
  // Creative
  { name: 'Art', group: 'creative' },
  { name: 'Music', group: 'creative' },
  { name: 'Drama, Film and Theatre Studies', group: 'creative', aliases: ['DFTS'] },
  { name: 'SPHE', group: 'humanities', levels: ['common'], noWrittenExam: true, aliases: ['Social Personal and Health Education'] },
  { name: 'Religious Education (non-exam)', group: 'humanities', levels: ['common'], noWrittenExam: true, aliases: ['Religious Education Non-examination Framework', 'Non-exam RE'] },
  { name: 'Physical Education (non-exam)', group: 'practical', levels: ['common'], noWrittenExam: true, aliases: ['Physical Education Framework', 'PE Framework', 'Non-exam PE'] },
];

// NCCA LCA addendum, September 2022: an LCE modern foreign language can be
// taken in addition to the LCA language. Separate names preserve both courses
// and their different assessments, including Higher-only non-curricular languages.
// These choices record a student's course; school/SEC eligibility still applies.
LCA_SUBJECTS.push(...LC_SUBJECTS.filter(subject => subject.group === 'languages'
  && !['English', 'Irish', 'Latin', 'Ancient Greek', 'Hebrew Studies'].includes(subject.name))
  .map(subject => ({ ...subject, name: `Leaving Cert ${subject.name}`,
    establishedSubject: subject.name, levels: subject.levels ?? ['higher', 'ordinary'],
    aliases: [`LCE ${subject.name}`, ...(subject.aliases ?? []).map(alias => `Leaving Cert ${alias}`)] } as LCSubject)));


const DEFAULT_LC_LEVELS: Level[] = ['higher', 'ordinary'];

/** The levels a Leaving Cert subject is examined at, in display order. */
export function lcSubjectLevels(name: string): Level[] {
  return LC_SUBJECTS.find(subject => subject.name === name)?.levels ?? LCA_SUBJECTS.find(subject => subject.name === name)?.levels ?? DEFAULT_LC_LEVELS;
}

/** LCA courses use common level; separately examined LCE subjects keep their own levels. */
export function lcaSubjectLevels(name: string): Level[] {
  return LCA_SUBJECTS.find(subject => subject.name === name)?.levels ?? ['common'];
}

export const LEVEL_LABELS: Record<Level, string> = { higher: 'Higher', ordinary: 'Ordinary', foundation: 'Foundation', common: 'Common' };

/** Whether a subject matches what a student typed, by name or by another name. */
export function subjectMatchesQuery(subject: LCSubject, query: string): boolean {
  const q = query.trim().toLocaleLowerCase();
  if (!q) return true;
  return [subject.name, subject.label ?? subject.name, ...(subject.aliases ?? [])].some(name => name.toLocaleLowerCase().includes(q));
}

/** One line for a subject whose level is fixed, or null when the student chooses. */
export function fixedLevelNote(name: string): string | null {
  if (LC_SUBJECTS.find(subject => subject.name === name)?.noWrittenExam) return 'Non-exam course';
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

export interface JCSubject extends LCSubject {
  jcHasLevelChoice?: boolean; // true only for English / Irish / Mathematics
}

export const JC_SUBJECTS: JCSubject[] = [
  { name: 'English', group: 'languages', jcHasLevelChoice: true, paperSubjectId: 'jc-english' },
  { name: 'Irish', group: 'languages', jcHasLevelChoice: true, aliases: ['Gaeilge', 'Gaeilge T2', 'Irish T2'], paperSubjectId: 'jc-irish' },
  { name: 'Irish T1', group: 'languages', jcHasLevelChoice: true, aliases: ['Gaeilge T1', 'Irish first language'], paperSubjectId: 'jc-irish-t1' },
  { name: 'French', group: 'languages', paperSubjectId: 'jc-french' },
  { name: 'German', group: 'languages', paperSubjectId: 'jc-german' },
  { name: 'Spanish', group: 'languages', paperSubjectId: 'jc-spanish' },
  { name: 'Italian', group: 'languages', paperSubjectId: 'jc-italian' },
  { name: 'Mathematics', group: 'stem', isMaths: true, jcHasLevelChoice: true, aliases: ['Maths'], paperSubjectId: 'jc-mathematics' },
  { name: 'Science', group: 'stem', paperSubjectId: 'jc-science' },
  { name: 'Business Studies', group: 'business', paperSubjectId: 'jc-business-studies' },
  { name: 'History', group: 'humanities', paperSubjectId: 'jc-history' },
  { name: 'Geography', group: 'humanities', paperSubjectId: 'jc-geography' },
  { name: 'Religious Education', group: 'humanities', aliases: ['RE', 'Religion'], paperSubjectId: 'jc-religious-education' },
  { name: 'Jewish Studies', group: 'humanities', paperSubjectId: 'jc-jewish-studies' },
  { name: 'Classical Studies', label: 'Classics', group: 'humanities', aliases: ['Classics'], paperSubjectId: 'jc-classics' },
  // Latin is a route within Classics; retain the old saved choice and route it correctly.
  { name: 'Latin', label: 'Classics (Latin)', group: 'humanities', aliases: ['Classics Latin'], paperSubjectId: 'jc-classics' },
  { name: 'Home Economics', group: 'practical', aliases: ['Home Ec'], paperSubjectId: 'jc-home-economics' },
  { name: 'Materials Technology (Wood)', label: 'Wood Technology', group: 'practical', aliases: ['Wood Technology', 'Woodwork'], paperSubjectId: 'jc-wood-technology' },
  { name: 'Metalwork', label: 'Engineering', group: 'practical', aliases: ['Engineering'], paperSubjectId: 'jc-engineering' },
  { name: 'Graphics', group: 'practical', paperSubjectId: 'jc-graphics' },
  { name: 'Technology', label: 'Applied Technology', group: 'practical', aliases: ['Applied Technology'], paperSubjectId: 'jc-applied-technology' },
  { name: 'Art', label: 'Visual Art', group: 'creative', aliases: ['Visual Art'], noWrittenExam: true, examGrades: true },
  { name: 'Music', group: 'creative', paperSubjectId: 'jc-music' },
  // Every NCCA-published short course. Assessment is not the written-exam band scale.
  { name: 'CSPE', group: 'humanities', noWrittenExam: true, shortCourseLevel: 3, aliases: ['Civic Social and Political Education'] },
  { name: 'SPHE', group: 'humanities', noWrittenExam: true, shortCourseLevel: 3, aliases: ['Social Personal and Health Education'] },
  { name: 'Physical Education', group: 'practical', noWrittenExam: true, shortCourseLevel: 3, aliases: ['PE'] },
  { name: 'Artistic Performance', group: 'creative', noWrittenExam: true, shortCourseLevel: 3 },
  { name: 'Chinese Language and Culture', group: 'languages', noWrittenExam: true, shortCourseLevel: 3 },
  { name: 'Coding', group: 'stem', noWrittenExam: true, shortCourseLevel: 3 },
  { name: 'Digital Media Literacy', group: 'stem', noWrittenExam: true, shortCourseLevel: 3 },
  { name: 'Philosophy', group: 'humanities', noWrittenExam: true, shortCourseLevel: 3 },
  { name: 'A Personal Project: Caring for Animals (Level 2)', group: 'practical', noWrittenExam: true, shortCourseLevel: 2 },
  { name: 'CSI: Exploring Forensic Science (Level 2)', group: 'stem', noWrittenExam: true, shortCourseLevel: 2 },
  { name: 'Enterprise in Animation (Level 2)', group: 'creative', noWrittenExam: true, shortCourseLevel: 2 },
  { name: 'History (Level 2)', group: 'humanities', noWrittenExam: true, shortCourseLevel: 2 },
  { name: 'Around the world in eighty days (Level 1)', group: 'humanities', noWrittenExam: true, shortCourseLevel: 1 },
  { name: 'Food glorious food (Level 1)', group: 'practical', noWrittenExam: true, shortCourseLevel: 1 },
  { name: 'Keeping well, looking good, feeling great (Level 1)', group: 'practical', noWrittenExam: true, shortCourseLevel: 1 },
];

export type SubjectProgramme = 'jc' | 'lca' | 'lc';
export const subjectProgramme = (year?: YearGroup | null, curriculumLevel?: CurriculumLevel): SubjectProgramme =>
  year === 'LCA1' || year === 'LCA2' ? 'lca'
    : year === '1st' || year === '2nd' || year === '3rd' || (!year && curriculumLevel === 'junior') ? 'jc' : 'lc';
export const catalogueForProgramme = (programme: SubjectProgramme): LCSubject[] =>
  programme === 'jc' ? JC_SUBJECTS : programme === 'lca' ? LCA_SUBJECTS : LC_SUBJECTS;
export const catalogueSubject = (programme: SubjectProgramme, name: string) => {
  const key = name.toLocaleLowerCase();
  const catalogue = catalogueForProgramme(programme);
  return catalogue.find(subject => subject.name.toLocaleLowerCase() === key)
    ?? catalogue.find(subject => [subject.label, ...(subject.aliases ?? [])].some(alias => alias?.toLocaleLowerCase() === key));
};
export const subjectHasWrittenExam = (subject: LCSubject, examYear?: number): boolean =>
  !subject.noWrittenExam && !(examYear && subject.lastWrittenExamYear && examYear > subject.lastWrittenExamYear);
export function subjectLevels(programme: SubjectProgramme, name: string): Level[] {
  if (programme === 'jc') return JC_SUBJECTS.find(subject => subject.name === name)?.jcHasLevelChoice ? ['higher', 'ordinary'] : ['common'];
  return programme === 'lca' ? lcaSubjectLevels(name) : lcSubjectLevels(name);
}
export function subjectUsesExamGrades(programme: SubjectProgramme, name: string): boolean {
  const subject = catalogueSubject(programme, name);
  if (subject?.noWrittenExam && !subject.examGrades) return false;
  return programme !== 'lca' || Boolean(subject?.establishedSubject);
}
export function subjectAssessmentNote(programme: SubjectProgramme, name: string): string {
  const subject = catalogueSubject(programme, name);
  if (programme === 'lca' && !subject?.establishedSubject) return 'Common level · LCA credits';
  if (subject?.shortCourseLevel) return `Level ${subject.shortCourseLevel} short course · No written exam`;
  if (subject?.noWrittenExam) return 'Non-exam course';
  return '';
}

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
  // Department of Education, revised bands from the 2025 examinations.
  'Distinction': [85, 100],
  'Higher Merit': [70, 84],
  'Merit': [55, 69],
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

export const FOUNDATION_GRADES: Grade[] = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8'];

/** CAO's grid: F1 20, F2 12 for Foundation Mathematics and Irish. Not every
 *  college counts them, but CAO publishes them, so the totals include them. */
export const FOUNDATION_POINTS: Record<string, number> = {
  F1: 20, F2: 12, F3: 0, F4: 0, F5: 0, F6: 0, F7: 0, F8: 0,
};

export const LCVP_GRADES: Grade[] = ['Distinction', 'Merit', 'Pass'];

export const LCVP_POINTS: Record<string, number> = {
  Distinction: 66, Merit: 46, Pass: 28,
};

export type GradeScale = 'higher' | 'ordinary' | 'foundation' | 'lcvp';

/** Which scale a grade belongs to, read from the grade itself. */
export function gradeScale(grade: Grade | undefined | null): GradeScale | null {
  if (!grade || typeof grade !== 'string') return null;
  if (Object.prototype.hasOwnProperty.call(LCVP_POINTS, grade)) return 'lcvp';
  if (grade.startsWith('H')) return 'higher';
  if (grade.startsWith('O')) return 'ordinary';
  if (Object.prototype.hasOwnProperty.call(FOUNDATION_POINTS, grade)) return 'foundation';
  return null;
}

/** Every grade on the same scale as `grade`, best first. */
export function gradeLadder(grade: Grade | undefined | null): Grade[] {
  const scale = gradeScale(grade);
  return scale === 'lcvp' ? LCVP_GRADES : scale === 'higher' ? HIGHER_GRADES : scale === 'foundation' ? FOUNDATION_GRADES : ORDINARY_GRADES;
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
  if (gradeScale(grade) === 'foundation') return FOUNDATION_POINTS[grade];
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
  if (level === 'foundation') return FOUNDATION_GRADES;
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

const SCALE_BONUS: Record<GradeScale, number> = { higher: 3, ordinary: 2, foundation: 1, lcvp: 0 };

/**
 * One number to compare any two Leaving Cert grades, bigger is better: CAO
 * points first, then the level (H6 and O2 are both 46 points but H6 is the
 * stronger result), then position on the grade's own scale (so H8, O7 and O8,
 * all 0 points, still order within a scale).
 */
export function gradeRank(grade: Grade | undefined | null): number {
  const scale = gradeScale(grade);
  if (!grade || !scale) return -1;
  return getPointsForGrade(grade) * 100 + SCALE_BONUS[scale] * 10 + (8 - getGradeIndex(grade));
}

/** The levels a student can aim for from `level`: their own and every level above it. */
export function targetLevelsFor(level: Level): Level[] {
  if (level === 'common') return ['common'];
  if (level === 'foundation') return ['higher', 'ordinary', 'foundation'];
  if (level === 'ordinary') return ['higher', 'ordinary'];
  return ['higher'];
}

/**
 * Grades a student may set as a target: those of their own level and every
 * level above, best first. An Ordinary student can aim for Higher, a
 * Foundation student for Ordinary or Higher. Every subject offered at a level is
 * also offered at the levels above it, so the level alone decides this.
 */
export function targetGradesFor(level: Level): Grade[] {
  return targetLevelsFor(level).flatMap(getGradesForLevel);
}

/**
 * How far a target is from the current grade, for effort estimates. On one
 * scale it is the number of grade steps; across levels it is the difference in
 * CAO points steps plus one for the jump in level (moving up a level is harder
 * than the same points on the level you are on).
 */
export function gradeSteps(current: Grade | undefined, target: Grade | undefined): number {
  const from = gradeScale(current);
  const to = gradeScale(target);
  if (!current || !target || !from || !to) return 0;
  if (from === to) return Math.max(0, getGradeIndex(current) - getGradeIndex(target));
  const ladder = [100, 88, 77, 66, 56, 46, 37, 28, 20, 12, 0];
  const position = (grade: Grade) => ladder.indexOf(getPointsForGrade(grade));
  const jump = SCALE_BONUS[to] > SCALE_BONUS[from] ? 1 : 0;
  return Math.max(0, position(current) - position(target)) + jump;
}

/**
 * A target is valid when it is no worse than the current grade, on the same
 * scale or a higher one (Ordinary current, Higher target).
 */
export function isValidTarget(current: Grade, target: Grade): boolean {
  const from = gradeScale(current);
  const to = gradeScale(target);
  if (!from || !to) return false;
  if (from === 'lcvp' || to === 'lcvp') return from === to && getGradeIndex(target) <= getGradeIndex(current);
  return gradeRank(target) >= gradeRank(current);
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
  return block.id ?? `${block.subjectName}|${block.sessionType}|${blockIndex}`;
}

/** Returns "YYYY-MM-DD" for a Date */
export function toDateKey(date: Date): string {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, '0');
  const d = String(date.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}
