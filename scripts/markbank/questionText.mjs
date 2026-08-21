/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Mark Bank — whether a card's question can be answered from the card alone.
 *
 * The first Mark Bank shipped cards whose "question" was a table fragment, so
 * both the build and test/markBankDeck.test.ts refuse them. Both did it by
 * length alone, and length is the wrong test: "What is cancer?" is fifteen
 * characters and needs nothing else, while "Set up control?" is the same length
 * and is a row stub from the scheme's own table. Four correct Biology, Chemistry
 * and Physics questions were dropped for being short.
 *
 * What actually decides it is whether the text ASKS something, or the card sets
 * it up — a stem, or a figure the question points into ("Name gas X.", where the
 * card carries the leaf section with X printed on it). Short and neither is
 * still a fragment.
 *
 * One implementation, imported by the build and by the deck test, for the same
 * reason schemeText.mjs and contentFree.mjs exist: the two had separate copies
 * of the length rule, so loosening one alone wrote cards the other rejected.
 */

/** The words a question opens with when it is asking something. */
const ASKS = /^(what|why|how|when|where|which|who|name|state|give|list|define|explain|describe|identify|suggest|outline|calculate|draw|compare|distinguish|account|match|complete|write|find|show)\b/i;

/** Below this, nothing can carry it. */
const FLOOR = 8;
/** At or above this, the question carries itself. */
const SELF_SUFFICIENT = 16;
/** A stem shorter than this is a label, not a setup. */
const STEM_MIN = 20;

export function questionStandsAlone(card) {
  const t = String(card?.questionText ?? '').trim();
  if (t.length < FLOOR) return false;
  if (t.length >= SELF_SUFFICIENT) return true;
  if (ASKS.test(t)) return true;
  // `figureKey` on an authored card, `figure` on a built one.
  return String(card?.stem ?? '').trim().length >= STEM_MIN
    || Boolean(card?.figureKey ?? card?.figure);
}
