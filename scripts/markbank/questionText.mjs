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

/**
 * A question set in Japanese, which the character floor cannot measure.
 *
 * Every threshold above is calibrated on the Latin alphabet, and Japanese does
 * not spend characters the same way: 勉強 is a whole ask in two characters,
 * ゆうじさんは、どんな人ですか。is a complete question in fourteen, and the
 * eight-character floor written to catch table fragments refused eighty-seven
 * correct kanji and grammar cards. So a question written in kana or kanji is
 * measured on its own terms — it asks something if it ends the way a Japanese
 * question ends, and a short printed item is carried by its part's printed
 * instruction exactly as a short English one is carried by a stem.
 */
const CJK = /[\u3040-\u30ff\u3400-\u9fff\uff66-\uff9f]/;
/** ですか。／ますか。／か。 — how every Japanese ask in these papers ends. */
const ASKS_JA = /[かカ]\s*[。｡]\s*$/;
/** A printed Japanese item this short is a fragment whatever carries it. */
const FLOOR_JA = 1;

export function questionStandsAlone(card) {
  const t = String(card?.questionText ?? '').trim();
  // `figureKey` on an authored card, `figure` on a built one.
  const carried = String(card?.stem ?? '').trim().length >= STEM_MIN
    || Boolean(card?.figureKey ?? card?.figure);
  if (CJK.test(t)) {
    return t.length >= FLOOR_JA && (t.length >= 6 || ASKS_JA.test(t) || carried);
  }
  if (t.length < FLOOR) return false;
  if (t.length >= SELF_SUFFICIENT) return true;
  if (ASKS.test(t)) return true;
  return carried;
}
