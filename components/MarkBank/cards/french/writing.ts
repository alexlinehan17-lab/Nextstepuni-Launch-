import type { FrenchRubric, SecRubricCard } from '../../../../types/markBank';
import authored from './writing.json';

export type FrenchWritingCard = SecRubricCard & { rubric: FrenchRubric };
export const FRENCH_WRITING_CARDS = authored as FrenchWritingCard[];
export const writingCardsForLevel = (level: 'higher' | 'ordinary'): SecRubricCard[] =>
  FRENCH_WRITING_CARDS.filter(card => card.level === level);
