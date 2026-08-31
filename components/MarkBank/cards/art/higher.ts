/** @license SPDX-License-Identifier: Apache-2.0 */
import type { SecRubricCard } from '../../../../types/markBank';
import { generatedCardsForLevel } from './factory';

/** Every separately marked Higher-Level Art task and finite printed route, 2021–2025. */
export const CARDS: SecRubricCard[] = generatedCardsForLevel('higher');
