/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * Which modules a given student can actually see.
 *
 * This was inlined in App.tsx's `studentCourses` useMemo, which made it the
 * student app's private knowledge — so the GC dashboard scored every student
 * against the full 83-module catalogue while the student's own counter used
 * their (much shorter) visible list. A 7-subject senior who had completed
 * everything they could open read as ~73% to their guidance counsellor.
 *
 * Extracted verbatim (including the documented senior filter quirk) so both
 * sides divide by the same denominator. Any behaviour change here changes the
 * student app — keep it mechanical.
 */

import { type CourseData } from '../components/Library';
import { SUBJECT_TO_MODULE } from '../courseData';
import { type StudentSubjectProfile } from '../components/subjectData';
import { type CurriculumLevel } from './authUtils';

export function filterCoursesForStudent(
  allCourses: CourseData[],
  curriculumLevel: CurriculumLevel | undefined,
  studentProfile: StudentSubjectProfile | null | undefined,
): CourseData[] {
  const level = curriculumLevel ?? 'senior';

  // Curriculum gating (Phase 4): a module is visible if it's tagged for
  // the user's level or for 'both'. Pre-Phase-1 modules without a tag are
  // assumed senior (every existing module was seeded 'senior' in Phase 1).
  const passesCurriculum = (c: CourseData) => {
    const tag = c.curriculum ?? 'senior';
    return tag === 'both' || tag === level;
  };

  const relevantModuleIds = studentProfile
    ? new Set(studentProfile.subjects.map(s => SUBJECT_TO_MODULE[s.subjectName]).filter(Boolean))
    : null;

  return allCourses.filter(c => {
    if (!passesCurriculum(c)) return false;

    if (c.category === 'subject-specific-science') {
      // Per-subject Decode (subject-*-protocol): only show for picked
      // subjects (existing senior behaviour, applied to both levels).
      if (c.id.startsWith('subject-')) {
        return !relevantModuleIds || relevantModuleIds.has(c.id);
      }
      // General strategy modules (mastering-*-protocol, applied-sciences,
      // digital-distraction, etc.): for JC users with a coming-soon tag,
      // surface them as "JC version coming" tiles regardless of picked
      // subjects. Senior behaviour unchanged (pre-existing filter quirk:
      // these are invisible to senior unless they're in SUBJECT_TO_MODULE
      // — separate cleanup, not Phase 4 scope).
      if (level === 'junior' && c.jcStatus === 'coming-soon') return true;
      return !relevantModuleIds || relevantModuleIds.has(c.id);
    }

    return true;
  });
}
