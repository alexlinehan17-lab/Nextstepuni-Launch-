/** @license SPDX-License-Identifier: Apache-2.0 */
import type { SecRubricCard } from '../../../../types/markBank';
import { tariffReconciles } from '../../../../types/markBank';
import { resolveCurriculumSpecification } from '../../../../curriculumRegistry';
import authored from './authored.json';
import { withPoliticsAnswers } from './answers';
import { withSchemeCorrections } from './corrections';

export const generatedCardsForLevel = (level: 'higher' | 'ordinary'): SecRubricCard[] =>
  (authored.cards as SecRubricCard[]).filter(card => card.level === level).map(card => {
    const specification = resolveCurriculumSpecification(card.subjectId, card.year);
    if (!specification || specification.id !== card.specVersion ||
        !specification.groups.some(group => group.topics.some(topic => topic.id === card.topicId))) {
      throw new Error(`Politics card ${card.id} has no topic in its examination-year curriculum`);
    }
    if (card.rubric.system !== 'politics' || !tariffReconciles(card)) {
      throw new Error(`Politics card ${card.id} has an invalid published tariff`);
    }
    // The scheme block, its lost price lines restored (corrections.ts), as ladders and rows where they reconcile
    // (cards/politics-and-society/answers.ts).
    return withPoliticsAnswers(withSchemeCorrections(card as SecRubricCard & { rubric: Extract<SecRubricCard['rubric'], { system: 'politics' }> }));
  });
