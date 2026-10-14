/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Mark Bank — the printed part labels of a merged question.
 *
 * The session screen hangs a question's part labels — (i), (ii), (a) — in a
 * gutter, the way the paper sets them. A label is only one of those if it
 * continues the paper's own sequence. The same bracket shapes turn up in the
 * wording of a part: an element symbol, "boron (B)", or a reference back,
 * "use the values you wrote down in (ii)" and "your answer at part (b) above".
 * Splitting at those cut a part in two and hung a stray label in the gutter
 * (Chemistry 2026 OL Q5(a)). Printed labels run in order, so a bracket that
 * breaks the order belongs to the sentence it sits in.
 */

/* Never glued to a letter. "(x)" IS a part label -- Physics 2022 OL Q3 runs
 * to (x) -- but in "h(x) = 2 sin(2x)" it is a function's argument, and
 * splitting there put "(x)" in the part gutter and left the question
 * reading "the tangent line to h". A printed label always follows a space
 * or opens the text. */
const PART = /\s*(?<![A-Za-z0-9])(\((?:[ivx]+|[a-h])\))\s+/gi;

export interface QuestionPart {
  label: string;
  body: string;
  children: QuestionPart[];
}

const isRomanPart = (label: string) => /^\([ivx]+\)$/i.test(label);

const ROMAN_DIGITS: Record<string, number> = { i: 1, v: 5, x: 10 };

/** The value of a roman label, or NaN for a run like "(vx)" that is not one. */
const romanValue = (label: string): number => {
  const digits = label.slice(1, -1).toLowerCase();
  let total = 0;
  for (let i = 0; i < digits.length; i++) {
    const value = ROMAN_DIGITS[digits[i]];
    const next = ROMAN_DIGITS[digits[i + 1]] ?? 0;
    total += value < next ? -value : value;
  }
  const canonical = ['', 'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xi', 'xii', 'xiii', 'xiv', 'xv'];
  return canonical[total] === digits ? total : NaN;
};

const letterIndex = (label: string) => label.toLowerCase().charCodeAt(1) - 97;
const caseOf = (label: string) => (label === label.toLowerCase() ? 'lower' : 'upper');

/** Where the label itself starts: each match also carries the space before it. */
const labelStart = (match: RegExpMatchArray) =>
  (match.index ?? 0) + match[0].length - match[0].trimStart().length;

/**
 * Keep the matches that are printed labels.
 *
 * A label that simply continues the sequence, (ii) after (i) or (b) after (a),
 * is always one. A label that jumps ahead, because the card leaves a part out,
 * or that starts the numerals again under a new letter, is one only where a
 * new sub-question can begin: after a full stop, question mark, exclamation
 * or colon, on a new line, straight after another label, or after a marks note
 * such as "(8 marc)". A label that goes back is a reference to an earlier part
 * ("your answer at part (b) above"). Letters keep the case the question opened
 * with, lower case unless it opened on a capital, so "(B)" in "boron (B)" is
 * never a part.
 */
const printedLabels = (text: string, matches: RegExpMatchArray[]): RegExpMatchArray[] => {
  const kept: RegExpMatchArray[] = [];
  const first = matches[0][1];
  const romanCase = isRomanPart(first) ? caseOf(first) : 'lower';
  const letterCase = isRomanPart(first) ? 'lower' : caseOf(first);
  let lastRoman: number | null = null;
  let lastLetter: number | null = null;
  let lastChild: number | null = null;
  let lastTop: number | null = null;
  let letterSinceRoman = false;
  for (const [index, match] of matches.entries()) {
    const label = match[1];
    const before = text.slice(0, labelStart(match));
    const previous = kept[kept.length - 1];
    const atBoundary = /\n[^\S\n]*$/.test(before)
      || /[.?!:][”’"')\]]*\s*$/.test(before)
      || /\([^()]*\d[^()]*\)\s*$/.test(before)
      || (previous !== undefined && (previous.index ?? 0) + previous[0].length === match.index);
    if (isRomanPart(label)) {
      const value = romanValue(label);
      if (index > 0) {
        if (caseOf(label) !== romanCase) continue;
        const next = value === (lastRoman ?? 0) + 1;
        const ahead = value > (lastRoman ?? 0);
        const restart = letterSinceRoman && value <= (lastRoman ?? 0);
        if (!next && !((ahead || restart) && atBoundary)) continue;
      }
      lastRoman = value;
      lastChild = null;
      letterSinceRoman = false;
    } else {
      const value = letterIndex(label);
      if (index > 0) {
        if (caseOf(label) !== letterCase) continue;
        const nextChild = lastRoman !== null && value === (lastChild ?? -1) + 1;
        const nextTop = value === (lastTop ?? -1) + 1;
        const ahead = value > (lastLetter ?? -1);
        if (!nextChild && !nextTop && !(ahead && atBoundary)) continue;
        if (nextChild) lastChild = value;
        else {
          // A new top-level letter: its numerals start again at (i).
          lastTop = value;
          lastChild = null;
          lastRoman = null;
        }
      } else {
        lastTop = value;
      }
      lastLetter = value;
      letterSinceRoman = true;
    }
    kept.push(match);
  }
  return kept;
};

/** Parse the paper's one- and two-level part grammar.
 *
 * A flat label/body pairing cannot represent `(i) (a) … (b) …`: the empty
 * body between `(i)` and `(a)` shifts every later token into the wrong column.
 * SEC questions use roman numerals for the parent and letters for its children,
 * so retain that hierarchy and let both levels keep a real prose column.
 * Returns null when the text does not open with a label.
 */
export const questionParts = (text: string): QuestionPart[] | null => {
  const found = [...text.matchAll(new RegExp(PART.source, PART.flags))];
  if (!found.length || (found[0].index ?? 0) !== 0) return null;
  const matches = printedLabels(text, found);
  const tokens = matches.map((match, index) => ({
    label: match[1],
    body: text.slice(
      (match.index ?? 0) + match[0].length,
      matches[index + 1]?.index ?? text.length,
    ).trim(),
    children: [] as QuestionPart[],
  }));
  const parts: QuestionPart[] = [];
  let parent: QuestionPart | null = null;
  for (const token of tokens) {
    if (isRomanPart(token.label)) {
      parts.push(token);
      parent = token;
    } else if (parent) {
      parent.children.push(token);
    } else {
      parts.push(token);
    }
  }
  return parts;
};
