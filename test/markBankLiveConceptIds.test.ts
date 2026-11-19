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
import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import overrides from '../scripts/markbank/live-concept-ids.json';
import { CARD_ID_ALIASES } from '../components/MarkBank/cardAliases';
import { loadCards, levelsFor } from '../components/MarkBank/deck';
// Large review JSON is read at run time, not imported, so the test typecheck stays within its heap.
const pins = JSON.parse(readFileSync(`${__dirname}/./fixtures/markBankLiveConceptIds.json`, 'utf8'));

const SUBJECTS = ['maths', 'physics', 'home-economics', 'japanese', 'russian', 'lcvp'];
const live = pins as Record<string, string>;
const copiedBack = overrides as Record<string, string>;

/** Every card the app serves in the six subjects, at every level it builds. */
const served = async () => {
  const decks = await Promise.all(SUBJECTS.flatMap(subject =>
    levelsFor(subject).map(level => loadCards(subject, level))));
  return new Map(decks.flat().map(card => [card.id, card.conceptId]));
};

describe('live cards keep their conceptId through the reviewed decks', () => {
  it('pins every live card that is still a card', async () => {
    const conceptById = await served();
    expect(Object.keys(live)).toHaveLength(3_249);
    const moved = Object.entries(live)
      .filter(([id, conceptId]) => conceptById.get(id) !== conceptId)
      .map(([id, conceptId]) => `${id}: live ${conceptId}, now ${conceptById.get(id) ?? '(no card)'}`);
    expect(moved).toEqual([]);
  }, 60_000);

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
