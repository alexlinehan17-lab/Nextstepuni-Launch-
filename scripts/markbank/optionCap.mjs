/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * How many options one best-of menu may show. Mirrors optionCapFor in
 * types/markBank.ts, which the build cannot import because it is TypeScript.
 * test/markBankDeck.test.ts asserts the two agree.
 */
export const MAX_OPTION_ROWS = 8;
export const MAX_LONG_OPTION_ROWS = 14;

/** Business Section 3 (Higher) and Section 2 (Ordinary); Sections B and C in
 *  the sciences. Keyed on the section, because a long question's individual
 *  parts are small while the menu the examiner prints for them is not. */
const LONG_SECTIONS = new Set(['2', '3', 'B', 'C']);

export const optionCapFor = (section) =>
  LONG_SECTIONS.has(section) ? MAX_LONG_OPTION_ROWS : MAX_OPTION_ROWS;
