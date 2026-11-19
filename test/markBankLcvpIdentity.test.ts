import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/lcvp/common';
import original from '../scripts/markbank/authoring/lcvp/original-concept-identities.json';
// Large review JSON is read at run time, not imported, so the test typecheck stays within its heap.
const authored = JSON.parse(readFileSync(`${__dirname}/../scripts/markbank/authored/lcvp.json`, 'utf8'));

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
