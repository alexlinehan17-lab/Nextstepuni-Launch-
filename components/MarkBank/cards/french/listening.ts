import type { CardAudioMaterial, FrenchRubric, SecRubricCard } from '../../../../types/markBank';
import authored from './listening.json';
import { withFrenchAnswers } from './answers';

export const FRENCH_LISTENING_CARDS = (authored as (SecRubricCard & { rubric: FrenchRubric; audioMaterial: CardAudioMaterial })[]).map(withFrenchAnswers);
export const listeningCardsForLevel = (level: 'higher' | 'ordinary'): SecRubricCard[] =>
  FRENCH_LISTENING_CARDS.filter(card => card.level === level);
