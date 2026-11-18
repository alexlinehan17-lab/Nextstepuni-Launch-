/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Religious Education band-grid cards (scripts/markbank/authoring/re_lane.py):
 * every RE answer as the SEC marks it, on its printed band grid. The sittings
 * rebuilt into this shape have left the point-card deck, so each printed ask
 * is one card. A card whose grid does not reconcile to its printed total is
 * refused here rather than shipped.
 */
import type { SecRubricCard } from '../../../../types/markBank';
import { tariffReconciles } from '../../../../types/markBank';
import authored from './rubric-authored.json';

export const rubricCardsForLevel = (level: 'higher' | 'ordinary'): SecRubricCard[] =>
  (authored.cards as unknown as SecRubricCard[]).filter(card => card.level === level).map(card => {
    if (card.kind !== 'rubric' || card.rubric.system !== 'religious-education' || !tariffReconciles(card)) {
      throw new Error(`Religious Education card ${card.id} has an invalid band grid`);
    }
    return card;
  });
