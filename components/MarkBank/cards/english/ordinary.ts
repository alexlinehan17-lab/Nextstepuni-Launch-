/** @license SPDX-License-Identifier: Apache-2.0 */
import type { SecRubricCard } from '../../../../types/markBank';
import { generatedCardsForLevel, publishedCards, type PublishedEnglishManifest } from './factory';
import publishedJson from './published-ordinary.json';

const PUBLISHED = publishedJson as unknown as PublishedEnglishManifest;

/**
 * All 440 legacy Ordinary Level response choices from the 2021–2025 papers,
 * followed by every card from papers whose own independent review gate passed
 * (published-ordinary.json). Legacy cards use the modern O1–O8 grid; reviewed
 * historical cards use the grid and cap rule their own year prints.
 */
export const CARDS: SecRubricCard[] = [
  ...generatedCardsForLevel('ordinary', PUBLISHED.legacyAdditionalSources, PUBLISHED.bridgedLegacyIds),
  ...publishedCards(PUBLISHED),
];
