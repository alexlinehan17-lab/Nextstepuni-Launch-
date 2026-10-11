import type { CardAudioMaterial, FrenchRubric, SecRubricCard } from '../../../../types/markBank';
import authored from './listening.json';

export const FRENCH_LISTENING_CARDS = authored as (SecRubricCard & { rubric: FrenchRubric; audioMaterial: CardAudioMaterial })[];
export const listeningCardsForLevel = (level: 'higher' | 'ordinary'): SecRubricCard[] =>
  FRENCH_LISTENING_CARDS.filter(card => card.level === level);
