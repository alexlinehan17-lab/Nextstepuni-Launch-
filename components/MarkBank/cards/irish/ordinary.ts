/** @license SPDX-License-Identifier: Apache-2.0 */
import type { SecRubricCard } from '../../../../types/markBank';
import { generatedCardsForLevel } from './factory';

/** Every selectable Ordinary-Level response across the 2021–2025 Irish papers. */
export const CARDS: SecRubricCard[] = generatedCardsForLevel('ordinary');
