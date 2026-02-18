/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

// Types for data-driven subject modules

export interface SubjectHighlight {
  term: string;
  description: string;
}

export interface SubjectSectionData {
  title: string;
  eyebrow: string;
  paragraphs: string[];
  highlights: SubjectHighlight[];
  bullets?: string[];
  commitmentText?: string;
}

export interface SubjectModuleContent {
  subjectId: string;
  subjectName: string;
  moduleNumber: string;
  moduleTitle: string;
  moduleSubtitle: string;
  moduleDescription: string;
  themeName: string;
  sections: SubjectSectionData[];
}

import { LANGUAGES_CONTENT } from './subjectContentLanguages';
import { STEM_CONTENT } from './subjectContentStem';
import { BUSINESS_CONTENT } from './subjectContentBusiness';
import { HUMANITIES_CONTENT } from './subjectContentHumanities';
import { PRACTICAL_CONTENT } from './subjectContentPractical';
import { CREATIVE_CONTENT } from './subjectContentCreative';

export const SUBJECT_MODULE_CONTENT: Record<string, SubjectModuleContent> = {
  ...LANGUAGES_CONTENT,
  ...STEM_CONTENT,
  ...BUSINESS_CONTENT,
  ...HUMANITIES_CONTENT,
  ...PRACTICAL_CONTENT,
  ...CREATIVE_CONTENT,
};
