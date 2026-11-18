/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Live progress identities survive Codex's reviewed decks (release 2026-11-18).
 *
 * Maths, Physics, Home Economics, Japanese, Russian and Link Modules shipped
 * October decks; Codex's reviewed decks replace them. Alex's decision (option
 * A, 18 Nov 2026): every live card id keeps resolving and keeps the conceptId
 * it had when it went live, while its rows and marks take the reviewed version.
 * The fixture is every live card in those six subjects that is still a card,
 * with its live conceptId, measured on main 4690b0487. 130 of them would have
 * changed; scripts/markbank/live-concept-ids.json copies those back at build
 * time (scripts/markbank/liveConceptIds.mjs). Never refresh this fixture to
 * make a change pass: a live conceptId only moves on Alex's say-so.
 */
import { describe, expect, it } from 'vitest';
import pins from './fixtures/markBankLiveConceptIds.json';
import overrides from '../scripts/markbank/live-concept-ids.json';
import { CARD_ID_ALIASES } from '../components/MarkBank/cardAliases';
import { CARDS as MATHS_HIGHER } from '../components/MarkBank/cards/maths/higher';
import { CARDS as MATHS_ORDINARY } from '../components/MarkBank/cards/maths/ordinary';
import { CARDS as MATHS_FOUNDATION } from '../components/MarkBank/cards/maths/foundation';
import { CARDS as PHYSICS_HIGHER } from '../components/MarkBank/cards/physics/higher';
import { CARDS as PHYSICS_ORDINARY } from '../components/MarkBank/cards/physics/ordinary';
import { CARDS as HOME_EC_HIGHER } from '../components/MarkBank/cards/home-economics/higher';
import { CARDS as HOME_EC_ORDINARY } from '../components/MarkBank/cards/home-economics/ordinary';
import { CARDS as JAPANESE_HIGHER } from '../components/MarkBank/cards/japanese/higher';
import { CARDS as JAPANESE_ORDINARY } from '../components/MarkBank/cards/japanese/ordinary';
import { CARDS as RUSSIAN_HIGHER } from '../components/MarkBank/cards/russian/higher';
import { CARDS as RUSSIAN_ORDINARY } from '../components/MarkBank/cards/russian/ordinary';
import { CARDS as LCVP_COMMON } from '../components/MarkBank/cards/lcvp/common';

const decks = [MATHS_HIGHER, MATHS_ORDINARY, MATHS_FOUNDATION, PHYSICS_HIGHER, PHYSICS_ORDINARY,
  HOME_EC_HIGHER, HOME_EC_ORDINARY, JAPANESE_HIGHER, JAPANESE_ORDINARY, RUSSIAN_HIGHER, RUSSIAN_ORDINARY, LCVP_COMMON];
const conceptById = new Map(decks.flat().map(card => [card.id, card.conceptId]));
const live = pins as Record<string, string>;
const copiedBack = overrides as Record<string, string>;

describe('live cards keep their conceptId through the reviewed decks', () => {
  it('pins every live card that is still a card', () => {
    expect(Object.keys(live)).toHaveLength(3_249);
    const moved = Object.entries(live)
      .filter(([id, conceptId]) => conceptById.get(id) !== conceptId)
      .map(([id, conceptId]) => `${id}: live ${conceptId}, now ${conceptById.get(id) ?? '(no card)'}`);
    expect(moved).toEqual([]);
  });

  it('copies back exactly the 130 live values a review had changed', () => {
    expect(Object.keys(copiedBack)).toHaveLength(130);
    for (const [id, conceptId] of Object.entries(copiedBack)) {
      expect(live[id], id).toBe(conceptId);
    }
  });

  it('never pins an id that is now an alias', () => {
    expect(Object.keys(live).filter(id => Object.hasOwn(CARD_ID_ALIASES, id))).toEqual([]);
  });
});
