/**
 * Live progress identities kept on Codex's reviewed cards (release 2026-11-18).
 *
 * A conceptId is the identity a student's Higher/Ordinary progress hangs on, so
 * a card that is live keeps the conceptId it had when it went live (R12), even
 * where a later review chose a different one. live-concept-ids.json lists the
 * 130 live cards in Maths, Japanese, Russian, Physics and Home Economics whose
 * reviewed deck would otherwise carry a new conceptId; every generator that
 * emits those decks passes each card through withLiveConceptId before writing.
 * test/markBankLiveConceptIds.test.ts pins every live value.
 */
import { readFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
export const LIVE_CONCEPT_IDS = Object.freeze(JSON.parse(
  readFileSync(resolve(ROOT, 'scripts/markbank/live-concept-ids.json'), 'utf8')));

/** The card with its live conceptId restored; any other card unchanged. */
export function withLiveConceptId(card) {
  const live = Object.hasOwn(LIVE_CONCEPT_IDS, card.id) ? LIVE_CONCEPT_IDS[card.id] : undefined;
  return live === undefined || card.conceptId === live ? card : { ...card, conceptId: live };
}
