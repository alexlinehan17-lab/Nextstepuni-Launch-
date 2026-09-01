/** @license SPDX-License-Identifier: Apache-2.0 */
import type { SecRubricCard } from '../../../../types/markBank';
import { generatedCardsForLevel } from './factory';

/**
 * All 450 Ordinary Level response choices from the 2021–2025 papers.  Combined,
 * composite and discrete cards each use the Ordinary Level O1–O8 grid printed
 * by the SEC; no Higher-Level label or invented answer row crosses the boundary.
 */
export const CARDS: SecRubricCard[] = generatedCardsForLevel('ordinary');
