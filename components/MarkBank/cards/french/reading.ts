import type { FrenchRubric, SecRubricCard } from '../../../../types/markBank';
import authored from './reading.json';
import { withFrenchAnswers } from './answers';

export const FRENCH_READING_CARDS = (authored as (SecRubricCard & { rubric: FrenchRubric })[]).map(withFrenchAnswers);
export const readingCardsForLevel = (level: 'higher' | 'ordinary'): SecRubricCard[] =>
  FRENCH_READING_CARDS.filter(card => card.level === level);
