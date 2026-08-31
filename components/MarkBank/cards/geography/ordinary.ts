/** @license SPDX-License-Identifier: Apache-2.0 */
import type { SecRubricCard } from '../../../../types/markBank';
import { generatedCardsForLevel } from './factory';

/** Every answerable Ordinary-Level Geography task and finite route, 2021–2026. */
export const CARDS: SecRubricCard[] = generatedCardsForLevel('ordinary');
