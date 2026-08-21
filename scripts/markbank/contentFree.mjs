/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Mark Bank — whether a marking row states an ANSWER or only a criterion.
 *
 * SEC schemes mix two things on the same page. "Xylem (tracheid or vessel) or
 * phloem" is an answer a student can learn. "Named piece of apparatus used" is
 * an instruction to the examiner, and a flashcard whose back reads that teaches
 * nothing — the student already knows they had to name the apparatus; what they
 * cannot recall is which one.
 *
 * The build drops any card carrying such a row, and test/markBankDeck.test.ts
 * re-checks the shipped deck the same way. Those two had SEPARATE copies of this
 * and had already drifted: the build knew "matching result" and "description
 * how", the deck test did not, and the deck test knew "Three points, 2 marks
 * each" while the build did not — so a row of that shape would have been written
 * by a build that accepted it into a suite that rejected it. One implementation,
 * imported by both, for the same reason schemeText.mjs exists.
 *
 * `types/markBank.ts` keeps its own copy because it is app code and must not
 * import out of scripts/; test/markBankContentFree.test.ts asserts the two agree
 * so the drift cannot come back silently.
 */

/** A tariff written where a marking point should be — "2 items, 3 marks each". */
const TARIFF_AS_ANSWER = /^\d+\s*(items?|points?|answers?)?[,\s]*\d*\s*marks?\s*(each)?\.?$/;

/** The same, spelled out — "Three points, 2 marks each". */
const TARIFF_IN_WORDS = /^(two|three|four|five|six)\s+(items?|points?|answers?)\b.*\bmarks?\b/;

/**
 * Openings that mark examiner instruction rather than answer content.
 *
 * "correct position" is qualified: bare, it is a criterion, but "Correct
 * position of leaf (or leaf disc) on lid" names both the thing and where it
 * goes, which is exactly the recallable content of that experiment. The
 * distinction is "of" — the SEC writes the criterion bare and names the thing
 * when it wants it named.
 */
const CRITERION = new RegExp(
  '^(named piece of apparatus( used)?'
  + '|control named( and setup described)?'
  + '|safety precaution described'
  + '|correct (sketch|matching result)'
  + '|correct position(?! of )'
  + '|suitable (time|temperature|volume)'
  + '|left for a (suitable )?time'
  + '|any correct'
  + '|the description earns'
  + '|description how'
  + '|matching result)',
);

/** True when the row says what the examiner must see, not what the answer is. */
export function isContentFreeRow(verbatim) {
  const t = String(verbatim).trim().toLowerCase();
  if (!t) return true;
  return TARIFF_AS_ANSWER.test(t) || TARIFF_IN_WORDS.test(t) || CRITERION.test(t);
}
