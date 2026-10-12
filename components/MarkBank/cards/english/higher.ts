/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * English Mark Bank — Higher Level.
 *
 * English marking is not converted into exact-answer rows. Short answers use
 * the published combined grade grid; longer answers use discrete PCLM with the
 * year's own cap rule. SEC indicative material is carried only as explicitly
 * non-exhaustive possible directions and can never be claimed as marks.
 */

import type { SecRubricCard } from '../../../../types/markBank';
import { generatedCardsForLevel, publishedCards, type PublishedEnglishManifest } from './factory';
import publishedJson from './published-higher.json';

const PUBLISHED = publishedJson as unknown as PublishedEnglishManifest;

/**
 * Legacy 2021–2025 cards from authored.json, followed by every card from papers
 * whose own independent review gate passed (published-higher.json).
 *
 * 2025 Paper 1 and Paper 2 are bridged (scripts/markbank/authored/
 * english-legacy-bridge.json): their reviewed published cards replace the
 * legacy ones. 37 legacy ids are kept by the published card itself; the five
 * legacy cards that bundled separately marked parts or both sides of a motion
 * (Paper 1 Composing 2, Paper 2 Comparative A/B/C Q1 and Unseen Q1) are
 * progress aliases in cardAliases.ts. The six 2025 Paper 1 cards that showed
 * indicative material keep it, now lifted verbatim from the scheme page.
 */
export const CARDS: SecRubricCard[] = [
  ...generatedCardsForLevel('higher', PUBLISHED.legacyAdditionalSources, PUBLISHED.bridgedLegacyIds),
  ...publishedCards(PUBLISHED),
].sort((left, right) =>
  right.year - left.year
  || left.section.localeCompare(right.section)
  || left.questionRef.localeCompare(right.questionRef, undefined, { numeric: true }));
