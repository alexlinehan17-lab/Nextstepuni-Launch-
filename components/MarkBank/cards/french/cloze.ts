import type { FrenchRubric, SecRubricCard } from '../../../../types/markBank';
import authored from './cloze.json';

export const FRENCH_CLOZE_CARDS = authored as (SecRubricCard & { rubric: FrenchRubric })[];
export const clozeCardsForLevel = (level: 'higher' | 'ordinary'): SecRubricCard[] =>
  FRENCH_CLOZE_CARDS.filter(card => card.level === level);
