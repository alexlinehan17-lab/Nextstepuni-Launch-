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
 *
 * A one-pick menu reads "One of these — 2 marks": "Any 1 of these — 2 marks
 * each" (1,965 menus on main, Spanish 2010 HL Section L Q2(b) among them) said "each"
 * of a single answer. A menu of one option offers no choice at all ("All 1 of
 * these — 5 marks each", 172 menus), so it states just its marks.
 */
export function anyNHeading(group: NonNullable<MarkRow['group']>): string {
  const price = (marks: number) => `${marks} ${marksWord(marks)}`;
  if (group.options.length === 1) {
    const only = group.optionMarks?.[0] ?? group.perOptionSteps?.[0] ?? group.perOption;
    if (Number.isFinite(only)) return price(only);
  }
  const one = group.claimMax === 1;
  const choice = one ? 'One of these'
    : group.claimMax === group.options.length ? `All ${group.claimMax} of these` : `Any ${group.claimMax} of these`;
  // Options priced one by one (a full answer and the part of it the scheme
  // also credits): the menu pays the best one claimed, at its own marks.
  if (group.optionMarks) {
    return `${one ? 'One of these' : `Any ${group.claimMax} of these`} — each at its own marks`;
  }
  if (group.perOptionSteps) {
    const steps = group.perOptionSteps.slice(0, group.claimMax);
    return `${choice} — ${steps.length === 1 ? price(steps[0]) : `${steps.join(' then ')} marks`}`;
  }
  if (!Number.isFinite(group.perOption)) return choice;
  return one ? `${choice} — ${price(group.perOption)}` : `${choice} — ${price(group.perOption)} each`;
}

/**
 * The label a menu row carries of its own, shown above the menu's heading:
 * "For — any one" over one Economics menu and "Against — any one" over its
 * neighbour, which otherwise read as two identical "One of these" lists.
 *
 * Shown exactly as the card prints it, and only where it is a label: never
 * where the row's text is one of its options or the options run together
 * (the menu already shows those), and never the generic "The answers the
 * scheme accepts…" the language decks give their menus, or LCVP's "Any 3 of
 * the answers the scheme states", which only repeat the heading.
 */
const GENERIC_MENU_LABEL = /^(?:The answers the scheme accepts|Any \d+ of the answers the scheme states)\b/;

export function menuLabel(row: Pick<MarkRow, 'verbatim' | 'group'>): string | null {
  const label = row.verbatim.trim();
  const options = (row.group?.options ?? []).map(option => option.trim());
  if (!label || !options.length) return null;
  if (options.includes(label)) return null;
  if (label.startsWith(options[0].slice(0, 30))) return null;
  if (GENERIC_MENU_LABEL.test(label)) return null;
  return label;
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
