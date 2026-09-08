/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The real papers the Subjects section shows. Every image is a render of the
 * first page of an actual SEC Leaving Certificate paper from the Paper Trail
 * corpus (the same PDFs the app opens), nothing is drawn or retouched:
 *  - /assets/landing/papers/  six first pages at 800px for the paper stack
 *  - /assets/landing/peek/    every Subjects-table subject at 360px for the
 *                             hover peek, named by the SUBJECT_GROUPS id
 * Captions carry the subject, level and year printed on the cover.
 */

export interface StackPaper {
  id: string;
  subject: string;
  level: 'Higher Level' | 'Ordinary Level';
  year: number;
  /** Booklet, where the exam is split ("Paper 1", "Sections A and B"). */
  part?: string;
  src: string;
}

export const STACK_PAPERS: StackPaper[] = [
  { id: 'physics', subject: 'Physics', level: 'Higher Level', year: 2023, src: '/assets/landing/papers/physics-2023-higher.webp' },
  { id: 'english', subject: 'English', level: 'Higher Level', year: 2025, part: 'Paper 1', src: '/assets/landing/papers/english-2025-higher.webp' },
  { id: 'maths', subject: 'Mathematics', level: 'Higher Level', year: 2025, part: 'Paper 1', src: '/assets/landing/papers/mathematics-2025-higher.webp' },
  { id: 'construction-studies', subject: 'Construction Studies', level: 'Higher Level', year: 2023, part: 'Theory', src: '/assets/landing/papers/construction-studies-2023-higher.webp' },
  { id: 'irish', subject: 'Irish', level: 'Ordinary Level', year: 2022, part: 'Paper 1', src: '/assets/landing/papers/irish-2022-ordinary.webp' },
  { id: 'economics', subject: 'Economics', level: 'Higher Level', year: 2024, src: '/assets/landing/papers/economics-2024-higher.webp' },
];

/** Rendered pixel size of every stack page (A4 at 800px wide). */
export const STACK_PAGE = { width: 800, height: 1132 } as const;

export const stackCaption = (p: StackPaper): string => [p.subject, p.level, String(p.year), p.part].filter(Boolean).join(' · ');

/** Which Leaving Certificate sitting each peek plate is the first page of. */
const PEEK_PAPERS: Record<string, { year: number; level: 'Higher Level' | 'Ordinary Level' }> = {
  accounting: { year: 2020, level: 'Higher Level' },
  'agricultural-science': { year: 2024, level: 'Higher Level' },
  'applied-mathematics': { year: 2022, level: 'Higher Level' },
  art: { year: 2024, level: 'Higher Level' },
  biology: { year: 2025, level: 'Higher Level' },
  business: { year: 2023, level: 'Higher Level' },
  chemistry: { year: 2024, level: 'Higher Level' },
  'classical-studies': { year: 2024, level: 'Higher Level' },
  'computer-science': { year: 2024, level: 'Higher Level' },
  'construction-studies': { year: 2023, level: 'Higher Level' },
  'design-and-communication-graphics': { year: 2024, level: 'Higher Level' },
  economics: { year: 2024, level: 'Higher Level' },
  engineering: { year: 2024, level: 'Higher Level' },
  english: { year: 2025, level: 'Higher Level' },
  french: { year: 2024, level: 'Higher Level' },
  geography: { year: 2024, level: 'Higher Level' },
  german: { year: 2024, level: 'Higher Level' },
  history: { year: 2024, level: 'Higher Level' },
  'home-economics': { year: 2024, level: 'Higher Level' },
  irish: { year: 2022, level: 'Ordinary Level' },
  italian: { year: 2024, level: 'Higher Level' },
  maths: { year: 2025, level: 'Higher Level' },
  music: { year: 2024, level: 'Higher Level' },
  'physical-education': { year: 2024, level: 'Higher Level' },
  physics: { year: 2023, level: 'Higher Level' },
  'politics-and-society': { year: 2024, level: 'Higher Level' },
  'religious-education': { year: 2024, level: 'Higher Level' },
  spanish: { year: 2024, level: 'Higher Level' },
  technology: { year: 2024, level: 'Higher Level' },
};

/** Rendered pixel size of every peek plate (A4 at 360px wide). */
export const PEEK_PAGE = { width: 360, height: 509 } as const;

/** The peek plate for a Subjects-table subject, or null when no real page exists for it (then there is no peek at all). */
export const peekFor = (subjectId: string, label: string): { src: string; alt: string } | null => {
  const p = PEEK_PAPERS[subjectId];
  if (!p) return null;
  return { src: `/assets/landing/peek/${subjectId}.webp`, alt: `${label} ${p.year}, ${p.level}: first page of the Leaving Certificate paper` };
};
