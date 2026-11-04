/** @license SPDX-License-Identifier: Apache-2.0 */
import type { BusinessRubric, SecRubricCard } from '../../../../types/markBank';
import { resolveCurriculumSpecification } from '../../../../curriculumRegistry';
import data from './rubric-authored.json';
import routePools from './route-pools.json';
import { expandBusinessRoutePools } from './routes.mjs';

interface AuthoredCard {
  id: string;
  year: number;
  level: 'higher' | 'ordinary';
  topicId: string;
  additionalTopicIds?: string[];
  conceptId: string;
  questionRef: string;
  questionText: string;
  section: '1' | '2' | '3';
  totalMarks: number;
  paperFileid: string;
  paperPages: number[];
  sourceTitle: string;
  sourceLabel?: string;
  rubric: BusinessRubric;
}

export function businessRubricCards(level: 'higher' | 'ordinary'): SecRubricCard[] {
  const authored = [...data.cards, ...expandBusinessRoutePools(routePools.pools)] as AuthoredCard[];
  return authored.filter(card => card.level === level).map(card => {
    const specification = resolveCurriculumSpecification('Business', card.year);
    if ([card.topicId, ...(card.additionalTopicIds ?? [])].some(id =>
      !specification?.groups.some(group => group.topics.some(topic => topic.id === id)))) {
      throw new Error(`Business card ${card.id} has no canonical topic for ${card.year}`);
    }
    return {
      id: card.id, subjectId: 'business', source: 'sec', kind: 'rubric',
      year: card.year, level: card.level, topicId: card.topicId, conceptId: card.conceptId,
      ...(card.additionalTopicIds?.length ? { additionalTopicIds: card.additionalTopicIds } : {}),
      section: card.section, questionRef: card.questionRef, questionText: card.questionText,
      totalMarks: card.totalMarks, paperFileid: card.paperFileid,
      sourceMaterial: {
        kind: 'source-text', label: card.sourceLabel ?? 'CASE STUDY', title: card.sourceTitle,
        pages: card.paperPages,
        attribution: `SEC Business ${card.year} examination paper — © State Examinations Commission.`,
        presentationNote: card.sourceLabel === 'QUESTION PAPER'
          ? 'Read the original question and return when you are ready to answer.'
          : 'Read the case study and return to the question when you are ready to answer.',
      },
      schemeCitation: `SEC Business ${card.year} ${level === 'higher' ? 'Higher' : 'Ordinary'} Level marking scheme, PDF pp. ${card.rubric.schemePages.join(', ')} — © State Examinations Commission.`,
      specVersion: specification.id,
      qa: {
        gates: ['paper-prompt', 'published-mark-boundaries',
          card.sourceLabel === 'QUESTION PAPER' ? 'question-paper-source' : 'case-study-source', 'scheme-page-review'],
        humanReviewedBy: 'agent-paper-and-scheme-review', humanReviewedAt: '2026-10-07',
      },
      rubric: card.rubric,
    };
  });
}
