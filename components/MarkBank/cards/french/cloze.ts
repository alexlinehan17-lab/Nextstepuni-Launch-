import type { FrenchRubric, SecRubricCard } from '../../../../types/markBank';
import authored from './cloze.json';
import { withFrenchAnswers } from './answers';

export const FRENCH_CLOZE_CARDS = (authored as (SecRubricCard & { rubric: FrenchRubric })[]).map(withFrenchAnswers);
export const clozeCardsForLevel = (level: 'higher' | 'ordinary'): SecRubricCard[] =>
  FRENCH_CLOZE_CARDS.filter(card => card.level === level);
