/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * What a signed-out visitor gets to touch. Biology and Mathematics are open
 * across every surface in the playground — under "My subjects" and "All
 * subjects" alike; everything else shows with a lock and shakes when pressed. The sample profile feeds the tools that need a
 * student (timetable, grade planner, Future Finder) — a plausible sixth-year
 * with the seven subjects Alex named, not a real one.
 */

import type { StudentSubjectProfile } from '../../subjectData';
import { SUBJECTS as MARK_BANK_SUBJECTS } from '../../MarkBank/deck';

export const FREE_SUBJECTS: readonly string[] = ['Biology', 'Mathematics'];
export const isFree = (name: string): boolean => FREE_SUBJECTS.includes(name);

/** The subject grid a visitor sees (Mark Bank's fifteen), in Mark Bank's order. */
export const LANDING_SUBJECTS: readonly string[] = MARK_BANK_SUBJECTS.map(s => s.title);
export const LOCKED_SUBJECTS: readonly string[] = LANDING_SUBJECTS.filter(t => !isFree(t));

/** Paper Trail opens on Mathematics: 200 of its 222 papers carry answer maps. */
export const PAPER_TRAIL_OPEN_SUBJECT = 'Mathematics';

const STAMP = '2026-09-01T09:00:00.000Z';

export const DEMO_PROFILE: StudentSubjectProfile = {
  subjects: [
    { subjectName: 'English', level: 'higher', currentGrade: 'H4', targetGrade: 'H3' },
    { subjectName: 'Irish', level: 'ordinary', currentGrade: 'O2', targetGrade: 'O1' },
    { subjectName: 'Mathematics', level: 'higher', currentGrade: 'H5', targetGrade: 'H3' },
    { subjectName: 'Chemistry', level: 'higher', currentGrade: 'H4', targetGrade: 'H2' },
    { subjectName: 'Economics', level: 'higher', currentGrade: 'H3', targetGrade: 'H2' },
    { subjectName: 'Biology', level: 'higher', currentGrade: 'H4', targetGrade: 'H2' },
    { subjectName: 'French', level: 'higher', currentGrade: 'H4', targetGrade: 'H3' },
  ],
  examStartDate: '2027-06-02',
  restDays: ['Sunday'],
  defaultBlockDuration: 45,
  yearGroup: '6th',
  createdAt: STAMP,
  updatedAt: STAMP,
};

export const DEMO_SUBJECT_NAMES: readonly string[] = DEMO_PROFILE.subjects.map(s => s.subjectName);
/** The same seven as Paper Trail wants them: name + level. */
export const DEMO_LEVELS = DEMO_PROFILE.subjects.map(s => ({ name: s.subjectName, level: s.level as string }));
/** The same seven as the Topic Atlas keys them (its subject ids are the lowercase names). */
export const DEMO_ATLAS_SUBJECTS = DEMO_PROFILE.subjects.map(s => ({ id: s.subjectName.toLowerCase(), label: s.subjectName }));
