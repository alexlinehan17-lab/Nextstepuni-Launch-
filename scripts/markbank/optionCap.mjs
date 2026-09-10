/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * How many options one best-of menu may show. Mirrors optionCapFor in
 * types/markBank.ts, which the build cannot import because it is TypeScript.
 * test/markBankDeck.test.ts asserts the two agree.
 */
export const MAX_OPTION_ROWS = 8;
// 2017 Construction Studies HL Q4(a) prints sixteen distinct acceptable
// functional requirements. The ceiling must cover the largest verified SEC
// menu; trimming it would make a correct answer impossible to self-mark.
export const MAX_LONG_OPTION_ROWS = 16;

/** Business Section 3 (Higher) and Section 2 (Ordinary); Sections B and C in
 *  the sciences. Keyed on the section, because a long question's individual
 *  parts are small while the menu the examiner prints for them is not. */
// German's reading comprehensions are long questions whose PARTS are small:
// the 2022 Higher TEXT I theme question prints twenty-six accepted points
// for ten marks and its 1(a) prints nine for six, so the section tokens the
// German deck cites — TEXT I, II and III — belong here too.
const LONG_SECTIONS = new Set(['2', '3', 'B', 'C', 'T1', 'T2', 'T3']);

export const optionCapFor = (section) =>
  LONG_SECTIONS.has(section) ? MAX_LONG_OPTION_ROWS : MAX_OPTION_ROWS;
