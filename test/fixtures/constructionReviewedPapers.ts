/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import fs from 'node:fs';

/**
 * Construction Studies theory papers reviewed on the shared engine (scripts/markbank/authoring/construction_paper.py).
 * construction_paper.integrate() appends one entry per paper to constructionReviewedPapers.json.
 */
export interface ConstructionReviewedPaper {
  year: number;
  level: 'higher' | 'ordinary';
  validator: string;
  result: Record<string, number | boolean>;
  priorCount: number;
  addedIds: string[];
  correctedIds: string[];
  withdrawnIds: string[];
  keptChoiceIds: string[];
  choiceCardIds: string[];
}

const PATH = 'test/fixtures/constructionReviewedPapers.json';
export const CONSTRUCTION_REVIEWED_PAPERS: ConstructionReviewedPaper[] = fs.existsSync(PATH) ? JSON.parse(fs.readFileSync(PATH, 'utf8')) : [];
export const CONSTRUCTION_REVIEWED_HIGHER_ADDED_IDS = CONSTRUCTION_REVIEWED_PAPERS.filter(p => p.level === 'higher').flatMap(p => p.addedIds);
export const CONSTRUCTION_REVIEWED_ORDINARY_ADDED_IDS = CONSTRUCTION_REVIEWED_PAPERS.filter(p => p.level === 'ordinary').flatMap(p => p.addedIds);
