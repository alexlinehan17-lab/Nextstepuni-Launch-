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
/**
 * Ligature glyphs an SEC font encodes with no sensible Unicode mapping.
 *
 * The same map markbank_text.py folds on extraction, applied at comparison time
 * as well, because two scheme files converted before that fold existed still
 * carry the raw glyphs: Physics 2025 HL prints "paƩern" for "pattern" sixteen
 * times, and the card quoting "electric field pattern" could not be traced.
 * Folding here rather than rewriting the converted schemes keeps the extraction
 * output exactly as the extractor produced it, and a claim can never contain
 * one of these, so folding both sides changes nothing else.
 */
const LIGATURES = { 'Ɵ': 'ti', 'Ŧ': 'ti', 'Ʃ': 'tt', 'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl', 'ﬃ': 'ffi', 'ﬄ': 'ffl', 'ﬅ': 'st', 'ﬆ': 'st' };

const SUP = { '⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4', '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9' };
export const foldDigits = (t) => t
  .replace(/[ƟŦƩﬀﬁﬂﬃﬄﬅﬆ]/g, (c) => LIGATURES[c] ?? c)
  .replace(/[₀-₉]/g, (c) => String(c.charCodeAt(0) - 0x2080))
  .replace(/[⁰¹²³⁴-⁹]/g, (c) => SUP[c] ?? c)
  // Mathematical Alphanumeric Symbols, the whole block. The SEC typesets
  // formulae in it -- "Kc = [𝐍𝐇𝟑]𝟐" is bold capital N, bold capital H, bold
  // three, bold two -- and the LETTERS were being stripped as punctuation while
  // the digits folded, so "[NH3]²" could never match "[𝐍𝐇𝟑]𝟐". NFKD maps each
  // back to the character it already is. Same principle as the digit folding
  // above, and it does not loosen what counts as a match: 𝐇 IS H.
  .replace(/[\u{1D400}-\u{1D7FF}]/gu, (c) => c.normalize('NFKD'));

/**
 * The digits of a stacked fraction, as the SEC's equation font encodes them.
 *
 * Its ToUnicode map sends the ten digits into the Oriya letter block, so
 * 22.50/187.5 extracts as "ଶଶ.ହ଴ / ଵ଼଻.ହ" — each digit is exactly U+0B34 plus
 * its value. Eleven Chemistry calculations whose working was correct were
 * dropped over it.
 *
 * NOT folded in foldDigits, which runs on both sides. Tried that first and it
 * COST a card: Chemistry 2022 HL Q7(b)(ii) matched precisely because normalise()
 * threw the Oriya characters away as punctuation, and turning them into digits
 * put digits back in the middle of the phrase it quotes. An added form cannot do
 * that. No claim contains an Oriya letter, so folding one side is enough.
 */
const ORIYA_DIGIT = /[\u0B34-\u0B3D]/g;
const foldOriya = (t) => t.replace(ORIYA_DIGIT, (c) => String(c.charCodeAt(0) - 0x0B34));

/**
 * The degree sign as SEC PDFs actually print it.
 *
 * "17 °C to 32 °C" comes out of the scheme as "17oC to 32oC" — the degree mark
 * is set as a superscript letter o, and the extractor faithfully reports a
 * letter. An author who types the temperature properly then cannot match the
 * scheme that priced it, which is what dropped the Biology 2022 OL alcohol
 * preparation and the 2021 HL enzyme denaturation.
 *
 * Folded into a third form of the scheme rather than into normalise(). Doing it
 * symmetrically would also eat a real leading "o" — "2 oxygen atoms" would
 * reduce to "2xygen", and a card quoting "oxygen atoms" would stop matching.
 * Adding a form can only add matches.
 */
const DEGREE_O = /(\d)oc/g;

/** Case, spacing and punctuation removed; every character of an answer must
 *  still appear, in order. */
export const normalise = (t) =>
  foldDigits(t).toLowerCase().replace(/[‐-―]/g, '-').replace(/[^a-z0-9]+/g, '');

/**
 * A whole scheme file reduced to the text a marking point is searched in.
 *
 * Several forms of it, not one, joined by a character normalise() can never
 * produce so that nothing matches across the seam: the scheme as printed, the
 * scheme with inline part labels removed, the scheme with the degree sign read
 * as a degree sign, and the scheme with a stacked fraction's digits read as
 * digits.
 *
 * Deleting the inline labels outright would be simpler and wrong: some marking
 * points ARE printed behind one, and quote it — "(i) PAYE which Gemma has to
 * pay: 17,325" is the answer in Business 2025 HL, and sixteen other shipped rows
 * read the same way. Searching every form keeps all of those matching while
 * letting a point quoted across an intruding label match too. Nothing is added
 * to any form, so no wording the SEC did not print can pass — the guard only
 * stops rejecting the SEC's own.
 */
/**
 * The double t an SEC font prints once.
 *
 * The 2024 Ordinary Chemistry scheme embeds a font whose "tt" ligature maps to a
 * single t, so it reads "pipete", "atraction", "leters", "writen". Unlike the
 * ligature glyphs above there is nothing in the text to say which t should be
 * two, so it cannot be repaired — only compared around, by collapsing tt on BOTH
 * sides. Restricted to tt because tt is what the evidence shows; collapsing every
 * doubled letter would loosen matching far past the defect.
 */
const collapseTT = (t) => t.replace(/tt/g, 't');

/** The last form comparableScheme() emits: the whole scheme with tt collapsed. */
const collapsedCache = new Map();

/**
 * Does this marking point appear in this scheme?
 *
 * Imported by the build and by test/markBankDeck.test.ts so the shipped deck is
 * re-checked by the rule that admitted it.
 */
export const claimMatches = (scheme, claim) => {
  const c = normalise(claim);
  if (scheme.includes(c)) return true;
  let collapsed = collapsedCache.get(scheme);
  if (collapsed === undefined) {
    collapsed = collapseTT(scheme);
    collapsedCache.set(scheme, collapsed);
  }
  return collapsed.includes(collapseTT(c));
};

export const comparableScheme = (raw) => {
  const lines = raw.replace(MARKS_CELL, ' ').replace(PAGE_MARKER, ' ')
    .split('\n').filter((l) => !MARKS_ONLY.test(l) && !LABEL_ONLY.test(l));
  const joined = lines.join(' ');
  const whole = normalise(joined);
  return [
    whole,
    normalise(lines.map((l) => l.replace(LEADING_LABEL, '')).join(' ')),
    whole.replace(DEGREE_O, '$1c'),
    normalise(foldOriya(joined)),
  ].join('|');
};
