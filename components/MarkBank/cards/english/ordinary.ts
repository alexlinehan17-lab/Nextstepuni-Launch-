/** @license SPDX-License-Identifier: Apache-2.0 */
import type { SecRubricCard } from '../../../../types/markBank';

/**
 * The Ordinary Level census is in place, but no OL card is published until its
 * distinct P&C / L&M rubric has been rendered and verified. An empty honest
 * deck is preferable to silently applying the Higher Level grid.
 */
export const CARDS: SecRubricCard[] = [];

