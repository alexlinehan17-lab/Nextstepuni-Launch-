import type { FrenchRubric, SecRubricCard } from '../../../../types/markBank';
import authored from './reading.json';

export const FRENCH_READING_CARDS = authored as (SecRubricCard & { rubric: FrenchRubric })[];
export const readingCardsForLevel = (level: 'higher' | 'ordinary'): SecRubricCard[] =>
  FRENCH_READING_CARDS.filter(card => card.level === level);
