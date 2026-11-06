import rawCards from './reviewed.json';
import { resolveCurriculumSpecification, specificationContainsId } from '../../../../curriculumRegistry';
import { tariffReconciles, type SecCard } from '../../../../types/markBank';

export const REVIEWED_CARDS: SecCard[] = rawCards.map(raw => {
  const specification = resolveCurriculumSpecification(raw.subjectId, raw.year);
  if (!specification || !specificationContainsId(specification, raw.topicId)) {
    throw new Error(`Japanese task ${raw.id} has no canonical curriculum topic`);
  }
  const card = { ...raw, specVersion: specification.id } as SecCard;
  if (!tariffReconciles(card)) throw new Error(`Japanese task ${raw.id} has an invalid source tariff`);
  return card;
});

export function withReviewedCards(originals: SecCard[], level: 'higher' | 'ordinary'): SecCard[] {
  const reviewed = REVIEWED_CARDS.filter(card => card.level === level);
  const byId = new Map(reviewed.map(card => [card.id, card]));
  const originalIds = new Set(originals.map(card => card.id));
  return [
    ...originals.map(original => {
      const correction = byId.get(original.id);
      if (correction && !correction.qa?.gates?.includes('reviewed-card-correction')) {
        throw new Error(`Japanese card ${original.id} has an unaudited correction`);
      }
      return correction ?? original;
    }),
    ...reviewed.filter(card => !originalIds.has(card.id)),
  ];
}
