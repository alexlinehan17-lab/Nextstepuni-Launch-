/** @license SPDX-License-Identifier: Apache-2.0 */
import type { SecRubricCard } from '../../../../types/markBank';
import { generatedCardsForLevel } from './factory';

/** Authored Higher-Level tasks; full archive and internal-route review is ongoing. */
export const CARDS: SecRubricCard[] = generatedCardsForLevel('higher');
