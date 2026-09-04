/** @license SPDX-License-Identifier: Apache-2.0 */

/**
 * Explicit bridge from the comparison site's URL identity to NextStepUni's
 * durable subject identities. Similar display names are not safe joins: Paper
 * Trail deliberately uses `home-economics-s-and-s`, `link-modules`, and
 * `physics-and-chemistry`, while future replacement subjects may not have an
 * SEC paper corpus yet.
 */

export type ReferenceSubjectStatus = 'current' | 'transition' | 'future-no-sec-paper';

export interface ReferenceSubjectMapping {
  paperTrailSubjectId?: string;
  curriculumSubjectId?: string;
  status: ReferenceSubjectStatus;
}

export const STUDYCLIX_SUBJECT_MAP: Record<string, ReferenceSubjectMapping> = {
  accounting: { paperTrailSubjectId: 'accounting', curriculumSubjectId: 'accounting', status: 'transition' },
  art: { paperTrailSubjectId: 'art', curriculumSubjectId: 'art', status: 'current' },
  chemistry: { paperTrailSubjectId: 'chemistry', curriculumSubjectId: 'chemistry', status: 'transition' },
  'computer-science': { paperTrailSubjectId: 'computer-science', curriculumSubjectId: 'computer-science', status: 'transition' },
  'drama-film-and-theatre-studies': { status: 'future-no-sec-paper' },
  english: { paperTrailSubjectId: 'english', curriculumSubjectId: 'english', status: 'transition' },
  german: { paperTrailSubjectId: 'german', curriculumSubjectId: 'german', status: 'current' },
  irish: { paperTrailSubjectId: 'irish', curriculumSubjectId: 'irish', status: 'current' },
  'lcvp-link-modules': { paperTrailSubjectId: 'link-modules', curriculumSubjectId: 'lcvp-link-modules', status: 'transition' },
  music: { paperTrailSubjectId: 'music', curriculumSubjectId: 'music', status: 'transition' },
  physics: { paperTrailSubjectId: 'physics', curriculumSubjectId: 'physics', status: 'transition' },
  spanish: { paperTrailSubjectId: 'spanish', curriculumSubjectId: 'spanish', status: 'current' },
  'agricultural-science': { paperTrailSubjectId: 'agricultural-science', curriculumSubjectId: 'agricultural-science', status: 'transition' },
  biology: { paperTrailSubjectId: 'biology', curriculumSubjectId: 'biology', status: 'transition' },
  'classical-studies': { paperTrailSubjectId: 'classical-studies', curriculumSubjectId: 'classical-studies', status: 'current' },
  'construction-studies': { paperTrailSubjectId: 'construction-studies', curriculumSubjectId: 'construction-studies', status: 'transition' },
  economics: { paperTrailSubjectId: 'economics', curriculumSubjectId: 'economics', status: 'current' },
  french: { paperTrailSubjectId: 'french', curriculumSubjectId: 'french', status: 'current' },
  history: { paperTrailSubjectId: 'history', curriculumSubjectId: 'history', status: 'transition' },
  italian: { paperTrailSubjectId: 'italian', curriculumSubjectId: 'italian', status: 'current' },
  'life-community-and-work-formerly-lcvp': { curriculumSubjectId: 'lcvp-link-modules', status: 'future-no-sec-paper' },
  'phys-chem': { paperTrailSubjectId: 'physics-and-chemistry', curriculumSubjectId: 'physics-and-chemistry', status: 'transition' },
  'politics-and-society': { paperTrailSubjectId: 'politics-and-society', curriculumSubjectId: 'politics-and-society', status: 'current' },
  technology: { paperTrailSubjectId: 'technology', curriculumSubjectId: 'technology', status: 'current' },
  'applied-maths': { paperTrailSubjectId: 'applied-mathematics', curriculumSubjectId: 'applied-mathematics', status: 'current' },
  business: { paperTrailSubjectId: 'business', curriculumSubjectId: 'business', status: 'transition' },
  'climate-action-and-sustainability': { status: 'future-no-sec-paper' },
  'design-communication-graphics': { paperTrailSubjectId: 'design-and-communication-graphics', curriculumSubjectId: 'design-and-communication-graphics', status: 'transition' },
  engineering: { paperTrailSubjectId: 'engineering', curriculumSubjectId: 'engineering', status: 'transition' },
  geography: { paperTrailSubjectId: 'geography', curriculumSubjectId: 'geography', status: 'transition' },
  'home-economics': { paperTrailSubjectId: 'home-economics-s-and-s', curriculumSubjectId: 'home-economics', status: 'transition' },
  japanese: { paperTrailSubjectId: 'japanese', curriculumSubjectId: 'japanese', status: 'current' },
  mathematics: { paperTrailSubjectId: 'mathematics', curriculumSubjectId: 'mathematics', status: 'transition' },
  'physical-education': { paperTrailSubjectId: 'physical-education', curriculumSubjectId: 'physical-education', status: 'transition' },
  'religious-education': { paperTrailSubjectId: 'religious-education', curriculumSubjectId: 'religious-education', status: 'current' },
};

