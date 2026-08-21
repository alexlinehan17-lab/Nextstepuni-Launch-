/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Mark Bank — how a marking point is compared against its marking scheme.
 *
 * The build drops any card whose rows it cannot find in the scheme, and a test
 * re-checks the shipped deck the same way. Those two had their own copies of
 * this logic and drifted: the build learned to ignore the extractor's ⟨marks⟩
 * cells and page markers, the test did not, and four correct Chemistry and
 * Physics cards were reported as untraceable by the very check that had just
 * accepted them. One implementation, imported by both — the same reason
 * paperIndex.mjs exists.
 */

/** A line that is nothing but a mark. */
const MARKS_ONLY = /^\s*\d+\s*(\(\s*\d+\s*\))?\s*$/;

/**
 * A line that is nothing but a part label — "(iii)", "(B)", "(a)".
 *
 * These live in a narrow left-hand column of the scheme table and land on their
 * own row, which puts them INSIDE the marking point printed beside them:
 *
 *     Increased sales/reach a wider audience:      ⟨14m⟩
 *     (iii)
 *     When a business chooses to distribute their product via retailers, the
 *
 * A card quoting that point whole — heading and sentence, which is what the
 * (4+3) pays for — then fails provenance because of a label that is not part of
 * the answer at all. Same reasoning as MARKS_ONLY: it carries no marking content.
 */
const LABEL_ONLY = /^\s*\(?\s*([ivx]{1,4}|[a-z]|\d{1,2})\s*\)\s*$/i;

/**
 * The same left-hand label, but sharing a line with the answer beside it.
 *
 * LABEL_ONLY catches the label that lands on its own row. It does not catch the
 * one whose y-band happens to line up with a WRAPPED line of the answer, which
 * the converter then emits as a single line:
 *
 *     The gearing ratio improved from 0.6:1 in 2020
 *     (iii) to 0.25:1in 2021.
 *
 * In the printed scheme (Business 2022 HL p.52) that "(iii)" sits at x≈96 in the
 * narrow Question column while the answer text starts at x≈127 — it is not a
 * word of the SEC's answer. Left in, it splits the one sentence the examiner
 * underlined, the literal answer to "improved or disimproved?", so no card can
 * quote it. Physics 2025 HL loses C = q/V the same way: the fraction sets over
 * two lines and "(i)" lands between numerator and denominator.
 */
const LEADING_LABEL = /^\s*\(\s*(?:[ivx]{1,4}|[a-z]|\d{1,2})\s*\)\s+(?=\S)/i;

/**
 * A marks cell that extract-scheme.py lifted out of the prose, e.g. ⟨2@5m(3+2)⟩.
 * It has to come out before normalising, or its digits fuse onto the words either
 * side of it and the sentence stops matching — the corruption the bracketing was
 * added to undo.
 */
const MARKS_CELL = /⟨[^⟩]*⟩/g;

/**
 * The extractor's own page markers.
 *
 * A marking point does not stop at a page break — the SEC prints "Less Risk /
 * Proven Business Model:" at the foot of one page and the sentence developing it
 * at the head of the next. Leave "## Page 14" in the comparison text and those
 * halves are no longer adjacent, so a card quoting the whole point is rejected
 * for quoting it whole. This is our annotation, not the SEC's words.
 */
const PAGE_MARKER = /^##\s*Page\s*\d+\s*$/gm;

/**
 * Digits that are drawn differently but ARE digits.
 *
 * SEC PDFs extract formulae as plain ASCII — "H2SO4", not "H₂SO₄" — while an
 * author writing the answer out is liable to typeset it properly. And the SEC's
 * own equation editor sets answers in Mathematical Bold: "𝟎. 𝟓: 𝟏", every
 * character of which normalise() would otherwise strip as non-alphanumeric,
 * reducing a correct answer to the empty string. Folding maps a character to the
 * digit it already means; it does not loosen what counts as a match.
 */
const SUP = { '⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4', '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9' };
export const foldDigits = (t) => t
  .replace(/[₀-₉]/g, (c) => String(c.charCodeAt(0) - 0x2080))
  .replace(/[⁰¹²³⁴-⁹]/g, (c) => SUP[c] ?? c)
  // Mathematical Alphanumeric Symbols, the whole block. The SEC typesets
  // formulae in it -- "Kc = [𝐍𝐇𝟑]𝟐" is bold capital N, bold capital H, bold
  // three, bold two -- and the LETTERS were being stripped as punctuation while
  // the digits folded, so "[NH3]²" could never match "[𝐍𝐇𝟑]𝟐". NFKD maps each
  // back to the character it already is. Same principle as the digit folding
  // above, and it does not loosen what counts as a match: 𝐇 IS H.
  .replace(/[\u{1D400}-\u{1D7FF}]/gu, (c) => c.normalize('NFKD'));

/** Case, spacing and punctuation removed; every character of an answer must
 *  still appear, in order. */
export const normalise = (t) =>
  foldDigits(t).toLowerCase().replace(/[‐-―]/g, '-').replace(/[^a-z0-9]+/g, '');

/**
 * A whole scheme file reduced to the text a marking point is searched in.
 *
 * Two forms of it, not one, joined by a character normalise() can never produce
 * so that nothing matches across the seam. Deleting the inline labels outright
 * would be simpler and wrong: some marking points ARE printed behind one, and
 * quote it — "(i) PAYE which Gemma has to pay: 17,325" is the answer in Business
 * 2025 HL, and sixteen other shipped rows read the same way. Searching both
 * forms keeps every one of those matching while letting a point quoted across an
 * intruding label match too. Nothing is added to either form, so no wording the
 * SEC did not print can pass — the guard only stops rejecting the SEC's own.
 */
export const comparableScheme = (raw) => {
  const lines = raw.replace(MARKS_CELL, ' ').replace(PAGE_MARKER, ' ')
    .split('\n').filter((l) => !MARKS_ONLY.test(l) && !LABEL_ONLY.test(l));
  return `${normalise(lines.join(' '))}|${normalise(lines.map((l) => l.replace(LEADING_LABEL, '')).join(' '))}`;
};
