/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Mark Bank — the session screen's own wording, kept out of the component so
 * each rule can be tested on its own.
 */

import type { MarkRow } from '../../types/markBank';

/** "1 mark", "3 marks": a heading that says "1 marks" reads as a typo on the scheme. */
export const marksWord = (n: number) => (n === 1 ? 'mark' : 'marks');

/**
 * The heading over a bounded "Any N" menu.
 *
 * A descending tariff is stated as it is paid ("6 then 4 marks"); a menu the
 * scheme prices only as a whole has no per-option value, so it states the
 * choice alone.
 */
export function anyNHeading(group: NonNullable<MarkRow['group']>): string {
  const choice = group.claimMax === group.options.length
    ? `All ${group.claimMax} of these` : `Any ${group.claimMax} of these`;
  if (group.perOptionSteps) {
    const steps = group.perOptionSteps.slice(0, group.claimMax);
    return `${choice} — ${steps.join(' then ')} ${steps.length === 1 ? marksWord(steps[0]) : 'marks'}`;
  }
  return Number.isFinite(group.perOption) ? `${choice} — ${group.perOption} ${marksWord(group.perOption)} each` : choice;
}

/** The most a "Not claimed yet" name runs to before it is cut at a word. */
export const UNCLAIMED_NAME_MAX = 64;

/** A spaced hyphen between two numbers is a minus or a range ("108 - 82", "18 - 24"), never a label break. */
const ARITHMETIC_DASH = /[\d)%°]\s-\s[\d(€£$−-]/;

/**
 * How the "Not claimed yet" band names one unclaimed row: the scheme's own
 * wording, minus a "Label — " prefix where the row carries one.
 *
 * The band used to keep only the text after the LAST spaced dash, which cut
 * working ("82 ÷ 2 = 41 • 108 - 82 = 26 …" became "82 = 26 • …") and dates
 * ("Ferdinand Porsche (1875 - 1951) was …" became "1951) was …"). A prefix is
 * stripped only where it is unambiguous: one em dash, or failing that one
 * spaced hyphen that is not arithmetic. Where what follows the label is a
 * letter, a verdict or a bare number it names nothing on its own, so the
 * label stays. Case is kept as printed.
 */
export function unclaimedName(verbatim: string, max = UNCLAIMED_NAME_MAX): string {
  const text = verbatim.replace(/\s+/g, ' ').trim().replace(/^[•·]\s*/, '');
  const emDashes = text.split(' — ');
  let tail: string | null = null;
  if (emDashes.length === 2) tail = emDashes[1];
  else if (emDashes.length === 1) {
    const hyphens = text.split(' - ');
    if (hyphens.length === 2 && !ARITHMETIC_DASH.test(text)) tail = hyphens[1];
  }
  const name = tail !== null && tail.trim().length > 6 && /[A-Za-zÀ-￿]{3}/.test(tail) ? tail.trim() : text;
  if (name.length <= max) return name;
  const cut = name.slice(0, max);
  const word = cut.lastIndexOf(' ');
  return `${(word > max * 0.6 ? cut.slice(0, word) : cut).replace(/[\s,;:·•—-]+$/, '')}…`;
}
