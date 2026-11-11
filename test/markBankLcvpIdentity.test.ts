import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/lcvp/common';
import authored from '../scripts/markbank/authored/lcvp.json';
import original from '../scripts/markbank/authoring/lcvp/original-concept-identities.json';

describe('LCVP original learning identities', () => {
  it('retains every original card and concept identity in authored and emitted records', () => {
    expect(Object.keys(original.conceptIds)).toHaveLength(314);
    const source = new Map(authored.map(card => [card.id, card.conceptId]));
    const emitted = new Map(CARDS.map(card => [card.id, card.conceptId]));
    for (const [id, concept] of Object.entries(original.conceptIds)) {
      expect(source.get(id), id).toBe(concept);
      expect(emitted.get(id), id).toBe(concept);
    }
  });
});
