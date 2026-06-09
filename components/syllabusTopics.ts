/** @license SPDX-License-Identifier: Apache-2.0 */

/**
 * Leaving Cert syllabus topics per subject, for tracking which syllabus areas a
 * student has covered. DERIVED from the single source of truth (curriculum.ts):
 * each subject's "topics" are its curriculum STRANDS, the exact same nodes that
 * Syllabus X-Ray, Catch-Up Lane and Command-Word use — so coverage tracking can
 * never describe the syllabus differently from the other tools.
 */
import { CURRICULUM } from '../curriculum';

// subjectName -> list of strand names (the coarse "areas" a student tracks coverage against)
export const SYLLABUS_TOPICS: Record<string, string[]> = Object.fromEntries(
  CURRICULUM.map((s) => [s.name, s.strands.map((st) => st.name)]),
);

// Common abbreviations / colloquial names -> canonical curriculum subject name.
const SUBJECT_ALIASES: Record<string, string> = {
  maths: 'Mathematics', math: 'Mathematics', 'higher maths': 'Mathematics', 'hl maths': 'Mathematics',
  'applied maths': 'Applied Mathematics', 'applied math': 'Applied Mathematics',
  bio: 'Biology', chem: 'Chemistry', phys: 'Physics',
  gaeilge: 'Irish', gaelige: 'Irish', eng: 'English',
  geo: 'Geography', geog: 'Geography', hist: 'History',
  'business studies': 'Business', econ: 'Economics',
  'ag science': 'Agricultural Science', 'agricultural science': 'Agricultural Science',
  'home ec': 'Home Economics', dcg: 'Design and Communication Graphics',
  'comp sci': 'Computer Science', 'computer science': 'Computer Science',
  re: 'Religious Education', 'politics and society': 'Politics and Society',
};

/**
 * Returns the list of syllabus topics (curriculum strand names) for a subject.
 * Case-insensitive against the canonical curriculum names, then a small alias map.
 * Returns an empty array when no match is found.
 */
export function getSyllabusTopics(subjectName: string): string[] {
  if (!subjectName) return [];
  const trimmed = subjectName.trim();

  // 1. Exact (case-insensitive) match against canonical curriculum subject names
  const canonical = Object.keys(SYLLABUS_TOPICS).find(
    (key) => key.toLowerCase() === trimmed.toLowerCase(),
  );
  if (canonical) return SYLLABUS_TOPICS[canonical];

  // 2. Alias lookup
  const aliasTarget = SUBJECT_ALIASES[trimmed.toLowerCase()];
  if (aliasTarget && SYLLABUS_TOPICS[aliasTarget]) return SYLLABUS_TOPICS[aliasTarget];

  // 3. No match
  return [];
}
