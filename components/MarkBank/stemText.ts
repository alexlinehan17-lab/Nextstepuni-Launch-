/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Mark Bank — the line breaks a question's stem keeps on screen.
 *
 * A stem can carry a printed choice list, "Choose one of the following:" and
 * then one bulleted item to a line. Laid out as plain prose, the items ran
 * together as "• Russborough House • Casino at Marino". Only a break that
 * starts a bulleted item is kept; every other break in a stem (a paragraph gap,
 * a line from a table, a wrap carried over from the PDF) runs on as a space,
 * exactly as the stem rendered before, so no prose turns ragged.
 */

const BULLET = /[•●▪◦‣]/;

/** The stem with each break before a bullet kept and every other break a space. */
export const stemWithListBreaks = (stem: string): string =>
  stem.replace(/[^\S\n]*\n\s*/g, (gap: string, offset: number) =>
    (BULLET.test(stem.charAt(offset + gap.length)) ? '\n' : ' '));
