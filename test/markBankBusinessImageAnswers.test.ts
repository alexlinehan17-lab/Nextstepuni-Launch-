import { describe, expect, it } from 'vitest';
import { CARDS as higher } from '../components/MarkBank/cards/business/higher';
import { CARDS as ordinary } from '../components/MarkBank/cards/business/ordinary';
import source from '../components/MarkBank/cards/business/rubric-authored.json';
import reviewed from '../components/MarkBank/cards/business/image-answers.json';
import exceptions from '../scripts/markbank/authored/business-expected-review.json';
import { businessMarks, businessScoreId, type BusinessScores } from '../components/MarkBank/businessRubric';

describe('reviewed Business image answers', () => {
  it('opens all six answers first, preserving every support page and published scoring allocation', () => {
    expect(Object.keys(reviewed.cards).sort()).toEqual(exceptions.map(item => item.id).sort());
    for (const [id, image] of Object.entries(reviewed.cards)) {
      const card = [...higher, ...ordinary].find(card => card.id === id)!;
      const original = source.cards.find(card => card.id === id)!;
      if (card.kind !== 'rubric' || card.rubric.system !== 'business') throw new Error(id);
      expect(card.rubric.schemePages[0], id).toBe(image.page);
      expect([...card.rubric.schemePages].sort(), id).toEqual([...original.rubric.schemePages].sort());
      expect(card.rubric.schemeRegions?.[0], id).toEqual({ p: image.page, r: image.region });
      expect(card.rubric.responses, id).toEqual(original.rubric.responses);
      expect(card.totalMarks, id).toBe(original.totalMarks);
      expect(image.sourceSha256, id).toMatch(/^[0-9a-f]{64}$/);
      const [left, top, right, bottom] = image.region;
      expect(left >= 0 && top >= 0 && right <= 1 && bottom <= 1 && left < right && top < bottom, id).toBe(true);
      const scores: BusinessScores = {};
      for (const response of card.rubric.responses) for (const allocation of response.allocations) {
        scores[businessScoreId(response.id, allocation.id)] = Math.max(...allocation.permittedMarks);
      }
      expect(businessMarks(card, scores), id).toBe(card.totalMarks);
    }
  });

  it('leaves all other Business reader regions and page order unchanged', () => {
    const ids = new Set(Object.keys(reviewed.cards));
    for (const original of source.cards.filter(card => !ids.has(card.id))) {
      const card = [...higher, ...ordinary].find(card => card.id === original.id)!;
      if (card.kind !== 'rubric' || card.rubric.system !== 'business') throw new Error(card.id);
      expect(card.rubric.schemePages, card.id).toEqual(original.rubric.schemePages);
      expect(card.rubric.schemeRegions, card.id).toBeUndefined();
    }
  });
});
