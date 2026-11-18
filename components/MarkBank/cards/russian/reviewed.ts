import rawCards from './reviewed.json';
import { resolveCurriculumSpecification, specificationContainsId } from '../../../../curriculumRegistry';
import type { SecCard } from '../../../../types/markBank';

export const REVIEWED_CARDS: SecCard[] = rawCards.map(raw => {
  const specification = resolveCurriculumSpecification('russian', raw.year);
  if (!specification || !specificationContainsId(specification, raw.topicId)) {
    throw new Error(`Russian card ${raw.id} has no canonical curriculum topic`);
  }
  // JSON widens discriminants and coordinate tuples. The source builder and
  // reviewed/deck regressions validate the complete data before publication.
  return { ...raw, specVersion: specification.id } as unknown as SecCard;
});

/** Preserve every shipped identity; corrections require explicit review. */
export function withReviewedCards(originals: SecCard[], level: 'higher' | 'ordinary'): SecCard[] {
  const reviewed = REVIEWED_CARDS.filter(card => card.level === level);
  const byId = new Map(reviewed.map(card => [card.id, card]));
  const originalIds = new Set(originals.map(card => card.id));
  if (byId.size !== reviewed.length) throw new Error('Duplicate reviewed Russian identity');
  for (const card of reviewed) {
    if (originalIds.has(card.id) && !card.qa.gates.includes('reviewed-card-correction')) {
      throw new Error(`Unreviewed Russian replacement ${card.id}`);
    }
  }
  return [...originals.map(card => byId.get(card.id) ?? card), ...reviewed.filter(card => !originalIds.has(card.id))];
}
