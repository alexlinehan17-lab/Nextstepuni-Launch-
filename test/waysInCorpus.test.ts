/**
 * Ways In corpus guard — every built SEC card must survive the support handoff
 * without its exact question changing or any marking-scheme fields crossing the
 * boundary. Command coverage is monitored across the real corpus so a future
 * authoring wave cannot silently turn the interpreter into an empty scaffold.
 */
import { describe, expect, test } from 'vitest';

import { CARDS as agHigher } from '@/components/MarkBank/cards/agricultural-science/higher';
import { CARDS as agOrdinary } from '@/components/MarkBank/cards/agricultural-science/ordinary';
import { CARDS as biologyHigher } from '@/components/MarkBank/cards/biology/higher';
import { CARDS as biologyOrdinary } from '@/components/MarkBank/cards/biology/ordinary';
import { CARDS as businessHigher } from '@/components/MarkBank/cards/business/higher';
import { CARDS as businessOrdinary } from '@/components/MarkBank/cards/business/ordinary';
import { CARDS as chemistryHigher } from '@/components/MarkBank/cards/chemistry/higher';
import { CARDS as chemistryOrdinary } from '@/components/MarkBank/cards/chemistry/ordinary';
import { CARDS as homeEconomicsHigher } from '@/components/MarkBank/cards/home-economics/higher';
import { CARDS as homeEconomicsOrdinary } from '@/components/MarkBank/cards/home-economics/ordinary';
import { CARDS as physicsHigher } from '@/components/MarkBank/cards/physics/higher';
import { CARDS as physicsOrdinary } from '@/components/MarkBank/cards/physics/ordinary';
import { buildQuestionModel } from '@/components/WaysIn/questionModel';
import { waysInSourceFromMarkBank } from '@/components/WaysIn/sources';

const cards = [
  ...agHigher, ...agOrdinary,
  ...biologyHigher, ...biologyOrdinary,
  ...businessHigher, ...businessOrdinary,
  ...chemistryHigher, ...chemistryOrdinary,
  ...homeEconomicsHigher, ...homeEconomicsOrdinary,
  ...physicsHigher, ...physicsOrdinary,
];

describe('Ways In across the Mark Bank corpus', () => {
  test('preserves every exact question and carries no scheme payload', () => {
    expect(cards.length).toBeGreaterThan(100);
    for (const card of cards) {
      const source = waysInSourceFromMarkBank(card, card.subjectId);
      const model = buildQuestionModel(source);
      expect(model.exactText, card.id).toBe(card.questionText.trim());
      expect(model.expectedPoints, card.id).toBeGreaterThanOrEqual(1);
      expect(model.expectedPoints, card.id).toBeLessThanOrEqual(8);

      const payload = source as unknown as Record<string, unknown>;
      expect(payload, card.id).not.toHaveProperty('rows');
      expect(payload, card.id).not.toHaveProperty('schemeCitation');
      expect(payload, card.id).not.toHaveProperty('tariffModel');
      expect(payload, card.id).not.toHaveProperty('schemeRegion');
    }
  });

  test('recognises the command in at least nine out of ten real questions', () => {
    const missing = cards.filter(card => {
      const source = waysInSourceFromMarkBank(card, card.subjectId);
      return buildQuestionModel(source).command === null;
    });
    const coverage = (cards.length - missing.length) / cards.length;
    expect(
      coverage,
      missing.slice(0, 30).map(card => `${card.id}: ${card.questionText}`).join('\n'),
    ).toBeGreaterThanOrEqual(0.9);
  });
});
