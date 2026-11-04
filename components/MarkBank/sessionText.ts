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

