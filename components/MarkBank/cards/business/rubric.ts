/** @license SPDX-License-Identifier: Apache-2.0 */
import type { BusinessRubric, SecRubricCard } from '../../../../types/markBank';
import { resolveCurriculumSpecification } from '../../../../curriculumRegistry';
import data from './rubric-authored.json';
import routePools from './route-pools.json';
// The SEC's deferred sittings, carded as papers of their own (scripts/markbank/authoring/business/
// add-<year>-<level>-deferred.py): each card's id, reference and booklet name the sitting.
import deferred from './deferred-authored.json';
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
  const authored = [...data.cards, ...expandBusinessRoutePools(routePools.pools),
    ...deferred.cards, ...expandBusinessRoutePools(deferred.pools)] as AuthoredCard[];
  return authored.filter(card => card.level === level).map(card => {
    const specification = resolveCurriculumSpecification('Business', card.year);
    if ([card.topicId, ...(card.additionalTopicIds ?? [])].some(id =>
      !specification?.groups.some(group => group.topics.some(topic => topic.id === id)))) {
      throw new Error(`Business card ${card.id} has no canonical topic for ${card.year}`);
    }
    // A deferred card's booklet is "<SEC file id>-deferred", as Paper Trail files it; its citations say so.
    const sitting = card.paperFileid.endsWith('-deferred') ? ', deferred examination' : '';
    return {
      id: card.id, subjectId: 'business', source: 'sec', kind: 'rubric',
      year: card.year, level: card.level, topicId: card.topicId, conceptId: card.conceptId,
      ...(card.additionalTopicIds?.length ? { additionalTopicIds: card.additionalTopicIds } : {}),
      section: card.section, questionRef: card.questionRef, questionText: card.questionText,
      totalMarks: card.totalMarks, paperFileid: card.paperFileid,
      sourceMaterial: {
        kind: 'source-text', label: card.sourceLabel ?? 'CASE STUDY', title: card.sourceTitle,
        pages: card.paperPages,
        attribution: `SEC Business ${card.year} examination paper${sitting} — © State Examinations Commission.`,
        presentationNote: card.sourceLabel === 'QUESTION PAPER'
          ? 'Read the original question and return when you are ready to answer.'
          : 'Read the case study and return to the question when you are ready to answer.',
      },
      schemeCitation: `SEC Business ${card.year} ${level === 'higher' ? 'Higher' : 'Ordinary'} Level marking scheme, PDF pp. ${card.rubric.schemePages.join(', ')}${sitting} — © State Examinations Commission.`,
      specVersion: specification.id,
      qa: {
        gates: ['paper-prompt', 'published-mark-boundaries',
          card.sourceLabel === 'QUESTION PAPER' ? 'question-paper-source' : 'case-study-source', 'scheme-page-review'],
        humanReviewedBy: 'agent-paper-and-scheme-review', humanReviewedAt: sitting ? '2026-11-19' : '2026-10-07',
      },
      rubric: card.rubric,
    };
  });
}
