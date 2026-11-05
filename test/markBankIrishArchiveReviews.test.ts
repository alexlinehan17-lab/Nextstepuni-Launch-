/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Irish archive review, batch 2 (2026-11-04): every paper reviewed down to the printed question, one commit per
 * paper. Each row pins the paper's printed asks as the builder lifted them and checks the cards a student gets:
 * legacy ids kept, every printed question its own criterion at its own tariff with claimable rows, the paper's
 * own words only (no line of ours in the question, the guidance or the task check), full marks reachable, and the
 * paper joined to the archive inventory and its Topic Atlas answer map.
 */
import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import inventory from '../scripts/markbank/authored/irish-archive-inventory.json';
import higher2022P1 from '../scripts/markbank/authored/irish-higher-2022-p1-component-review.json';
import higher2021P1 from '../scripts/markbank/authored/irish-higher-2021-p1-component-review.json';
import ordinary2021P1 from '../scripts/markbank/authored/irish-ordinary-2021-p1-component-review.json';
import higher2020P1 from '../components/MarkBank/cards/irish/higher-2020-p1-authored.json';
import higher2020P2 from '../components/MarkBank/cards/irish/higher-2020-p2-authored.json';
import ordinary2020P1 from '../components/MarkBank/cards/irish/ordinary-2020-p1-authored.json';
import ordinary2020P2 from '../components/MarkBank/cards/irish/ordinary-2020-p2-authored.json';
import higher2019P1 from '../components/MarkBank/cards/irish/higher-2019-p1-authored.json';
import higher2019P2 from '../components/MarkBank/cards/irish/higher-2019-p2-authored.json';
import ordinary2019P1 from '../components/MarkBank/cards/irish/ordinary-2019-p1-authored.json';
import ordinary2019P2 from '../components/MarkBank/cards/irish/ordinary-2019-p2-authored.json';
import higher2018P1 from '../components/MarkBank/cards/irish/higher-2018-p1-authored.json';
import higher2018P2 from '../components/MarkBank/cards/irish/higher-2018-p2-authored.json';
import ordinary2018P1 from '../components/MarkBank/cards/irish/ordinary-2018-p1-authored.json';
import ordinary2018P2 from '../components/MarkBank/cards/irish/ordinary-2018-p2-authored.json';
import higher2017P1 from '../components/MarkBank/cards/irish/higher-2017-p1-authored.json';
import higher2017P2 from '../components/MarkBank/cards/irish/higher-2017-p2-authored.json';
import ordinary2017P1 from '../components/MarkBank/cards/irish/ordinary-2017-p1-authored.json';
import ordinary2017P2 from '../components/MarkBank/cards/irish/ordinary-2017-p2-authored.json';
import higher2016P1 from '../components/MarkBank/cards/irish/higher-2016-p1-authored.json';
import higher2016P2 from '../components/MarkBank/cards/irish/higher-2016-p2-authored.json';
import ordinary2016P1 from '../components/MarkBank/cards/irish/ordinary-2016-p1-authored.json';
import ordinary2016P2 from '../components/MarkBank/cards/irish/ordinary-2016-p2-authored.json';
import higher2015P1 from '../components/MarkBank/cards/irish/higher-2015-p1-authored.json';
import higher2015P2 from '../components/MarkBank/cards/irish/higher-2015-p2-authored.json';
import ordinary2015P1 from '../components/MarkBank/cards/irish/ordinary-2015-p1-authored.json';
import ordinary2015P2 from '../components/MarkBank/cards/irish/ordinary-2015-p2-authored.json';
import higher2014P1 from '../components/MarkBank/cards/irish/higher-2014-p1-authored.json';
import higher2014P2 from '../components/MarkBank/cards/irish/higher-2014-p2-authored.json';
import ordinary2014P1 from '../components/MarkBank/cards/irish/ordinary-2014-p1-authored.json';
import ordinary2014P2 from '../components/MarkBank/cards/irish/ordinary-2014-p2-authored.json';
import ordinary2022P1 from '../scripts/markbank/authored/irish-ordinary-2022-p1-component-review.json';
import ordinary2022P2 from '../components/MarkBank/cards/irish/ordinary-2022-p2-authored.json';
import higher2022P2 from '../components/MarkBank/cards/irish/higher-2022-p2-authored.json';
import higher2021P2 from '../components/MarkBank/cards/irish/higher-2021-p2-authored.json';
import ordinary2021P2 from '../components/MarkBank/cards/irish/ordinary-2021-p2-authored.json';
import higher2013P1 from '../components/MarkBank/cards/irish/higher-2013-p1-authored.json';
import higher2013P2 from '../components/MarkBank/cards/irish/higher-2013-p2-authored.json';
import ordinary2013P1 from '../components/MarkBank/cards/irish/ordinary-2013-p1-authored.json';
import ordinary2013P2 from '../components/MarkBank/cards/irish/ordinary-2013-p2-authored.json';
import higher2012P1 from '../components/MarkBank/cards/irish/higher-2012-p1-authored.json';
import higher2012P2 from '../components/MarkBank/cards/irish/higher-2012-p2-authored.json';
import ordinary2012P1 from '../components/MarkBank/cards/irish/ordinary-2012-p1-authored.json';
import { CARDS as HIGHER } from '../components/MarkBank/cards/irish/higher';
import { CARDS as ORDINARY } from '../components/MarkBank/cards/irish/ordinary';
import { irishMarks } from '../components/MarkBank/SessionScreen';
import { tariffReconciles, type SecRubricCard } from '../types/markBank';
import { irishFullScores } from './fixtures/irishScores';

const DECK = new Map([...HIGHER, ...ORDINARY].map(card => [card.id, card]));
const card = (id: string): SecRubricCard => {
  const found = DECK.get(id);
  if (!found) throw new Error(`no card ${id}`);
  return found;
};
const rubric = (c: SecRubricCard) => {
  if (c.rubric.system !== 'irish') throw new Error(`${c.id} is not an Irish rubric card`);
  return c.rubric;
};
const criteria = (c: SecRubricCard) => rubric(c).criteria;
// Lines builders used to add in Irish of their own (irish_lifted.py strips them and the lift audit gates them).
const OURS = /Don chárta seo|An rogha don chárta seo|Léigh an téacs ar leathanach \d|Aon fhreagra ceart don chuid seo|An léargas seo =|Éist leis an taifeadadh|Freagair gach mír atá priontáilte|Coinnigh ceangal cinnte|Timpeall 500–600 focal|[\ue000-\uf8ff]/;
const shown = (c: SecRubricCard) => [c.questionText, c.stem ?? '', ...rubric(c).taskRequirements,
  ...criteria(c).flatMap(criterion => criterion.guidance)].join('\n');
const answerMap = (year: number, fileid: string) =>
  JSON.parse(readFileSync(`public/paper-answers/${year}/${fileid}.json`, 'utf8')) as { q: Array<{ n: string }> };

const PAPER_ONE = [
  { review: higher2022P1, year: 2022, fileid: 'LC001ALP100IV.pdf', segments: 8, questions: 25, titles: 9, perTitle: 100 },
  { review: ordinary2022P1, year: 2022, fileid: 'LC001GLP000IV.pdf', segments: 6, questions: 20, titles: 9, perTitle: 50 },
  { review: higher2021P1, year: 2021, fileid: 'LC001ALP100IV.pdf', segments: 8, questions: 23, titles: 9, perTitle: 100 },
  { review: ordinary2021P1, year: 2021, fileid: 'LC001GLP100IV.pdf', segments: 6, questions: 20, titles: 9, perTitle: 50 },
  // New cards (2020 has no legacy cards): the same shape, carded from the reviewed paper and scheme.
  { review: higher2020P1.review, year: 2020, fileid: 'LC001ALP100IV.pdf', segments: 8, questions: 23, titles: 9, perTitle: 100 },
  { review: ordinary2020P1.review, year: 2020, fileid: 'LC001GLP100IV.pdf', segments: 6, questions: 20, titles: 9, perTitle: 50 },
  { review: higher2019P1.review, year: 2019, fileid: 'LC001ALP100IV.pdf', segments: 8, questions: 26, titles: 9, perTitle: 100 },
  { review: ordinary2019P1.review, year: 2019, fileid: 'LC001GLP100IV.pdf', segments: 6, questions: 20, titles: 9, perTitle: 50 },
  { review: higher2018P1.review, year: 2018, fileid: 'LC001ALP100IV.pdf', segments: 8, questions: 29, titles: 9, perTitle: 100 },
  { review: ordinary2018P1.review, year: 2018, fileid: 'LC001GLP100IV.pdf', segments: 6, questions: 20, titles: 9, perTitle: 50 },
  { review: higher2017P1.review, year: 2017, fileid: 'LC001ALP100IV.pdf', segments: 8, questions: 28, titles: 9, perTitle: 100 },
  { review: ordinary2017P1.review, year: 2017, fileid: 'LC001GLP100IV.pdf', segments: 6, questions: 20, titles: 9, perTitle: 50 },
  { review: higher2016P1.review, year: 2016, fileid: 'LC001ALP100IV.pdf', segments: 8, questions: 25, titles: 9, perTitle: 100 },
  { review: ordinary2016P1.review, year: 2016, fileid: 'LC001GLP100IV.pdf', segments: 6, questions: 19, titles: 9, perTitle: 50 },
  { review: higher2015P1.review, year: 2015, fileid: 'LC001ALP100IV.pdf', segments: 8, questions: 27, titles: 9, perTitle: 100 },
  { review: ordinary2015P1.review, year: 2015, fileid: 'LC001GLP100IV.pdf', segments: 6, questions: 20, titles: 9, perTitle: 50 },
  { review: higher2014P1.review, year: 2014, fileid: 'LC001ALP100IV.pdf', segments: 8, questions: 26, titles: 9, perTitle: 100 },
  { review: ordinary2014P1.review, year: 2014, fileid: 'LC001GLP100IV.pdf', segments: 6, questions: 20, titles: 9, perTitle: 50 },
  { review: higher2013P1.review, year: 2013, fileid: 'LC001ALP100IV.pdf', segments: 8, questions: 30, titles: 9, perTitle: 100 },
  { review: ordinary2013P1.review, year: 2013, fileid: 'LC001GLP100IV.pdf', segments: 6, questions: 20, titles: 9, perTitle: 50 },
  { review: higher2012P1.review, year: 2012, fileid: 'LC001ALP100IV.pdf', segments: 8, questions: 28, titles: 9, perTitle: 100 },
  { review: ordinary2012P1.review, year: 2012, fileid: 'LC001GLP100IV.pdf', segments: 6, questions: 20, titles: 9, perTitle: 50 },
];

describe('Irish archive review: Paper 1 (listening and composition)', () => {
  for (const paper of PAPER_ONE) {
    it(`${paper.year} ${paper.review.level} ${paper.fileid}: ${paper.questions} printed questions and ${paper.titles} titles, each carded`, () => {
      const { review } = paper;
      expect(review.listeningSegmentCardIds).toHaveLength(paper.segments);
      expect(review.compositionRouteCardIds).toHaveLength(paper.titles);
      expect(review.printedListeningQuestions).toBe(paper.questions);
      const segments = review.listeningSegmentCardIds.map(card);
      // One criterion per printed question, at the published tariff, every one cut into claimable rows.
      expect(segments.flatMap(criteria)).toHaveLength(paper.questions);
      expect(segments.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(review.examStructure.listening);
      for (const c of segments) {
        expect(tariffReconciles(c), c.id).toBe(true);
        for (const criterion of criteria(c)) expect(criterion.allocation, `${c.id} ${criterion.id}`).toBeDefined();
        expect(irishMarks(c, irishFullScores(c)), c.id).toBe(c.totalMarks);
        expect(rubric(c).markingGuideNote, c.id).toMatch(/Bainfear ó 0 go [36] ar chaighdeán na Gaeilge/);
      }
      for (const id of review.compositionRouteCardIds) {
        const c = card(id);
        expect(c.totalMarks, id).toBe(paper.perTitle);
        expect(irishMarks(c, irishFullScores(c)), id).toBe(paper.perTitle);
        expect(c.questionText.split('\n').at(-1), id).toMatch(/^\((?:[a-e]|i{1,3})\) |^[A-ZÁÉÍÓÚ]/);
      }
      for (const id of review.cardIds) expect(shown(card(id)), id).not.toMatch(OURS);
      const row = inventory.papers.find(p => p.key === `${paper.year}|${review.level}|${paper.fileid}`)!;
      expect(row.markBankCardIds.slice().sort()).toEqual([...review.cardIds].sort());
      expect(row).toMatchObject({ fullVisualReview: 'complete', bankAtlasTaskParity: 'complete', partAndSelectionReconciliation: 'complete' });
      const mapped = new Set(answerMap(paper.year, paper.fileid).q.map(q => q.n));
      for (const n of ['1', '2', '3', '4']) expect(mapped.has(n), n).toBe(true);
    });
  }
});

const PAPER_TWO = [
  { file: ordinary2022P2, fileid: 'LC001GLP200IV.pdf', legacy: 22, practice: 42, readingWhole: 10 },
  { file: higher2022P2, fileid: 'LC001ALP200IV.pdf', legacy: 27, practice: 42, readingWhole: 12 },
  { file: higher2021P2, fileid: 'LC001ALP200IV.pdf', legacy: 26, practice: 48, readingWhole: 12 },
  { file: ordinary2021P2, fileid: 'LC001GLP200IV.pdf', legacy: 22, practice: 35, readingWhole: 10 },
];
// The Higher files name their added cards readingPracticeCardIds, the Ordinary ones practiceCardIds.
const practiceIds = (review: { practiceCardIds?: string[]; readingPracticeCardIds?: string[] }) =>
  review.practiceCardIds ?? review.readingPracticeCardIds ?? [];

describe('Irish archive review: Paper 2 (reading and literature)', () => {
  for (const paper of PAPER_TWO) {
    const { review } = paper.file;
    it(`${review.year} ${review.level} ${paper.fileid}: ${paper.legacy} retained cards and ${paper.practice} practice parts`, () => {
      expect(review.legacyCardIds).toHaveLength(paper.legacy);
      expect(practiceIds(review)).toHaveLength(paper.practice);
      expect(review.readingWholeCardIds).toHaveLength(paper.readingWhole);
      expect(paper.file.cards.map(c => c.id).sort()).toEqual([...practiceIds(review)].sort());
      for (const id of [...review.legacyCardIds, ...practiceIds(review)]) {
        const c = card(id);
        expect(tariffReconciles(c), id).toBe(true);
        expect(irishMarks(c, irishFullScores(c)), id).toBe(c.totalMarks);
        expect(shown(c), id).not.toMatch(OURS);
        if (c.practiceFocus) expect(c.practiceFocus, id).toMatch(/^[A-Z][a-z]/);
      }
      // Each whole reading question marks every printed part as its own criterion, each with claimable rows.
      for (const id of review.readingWholeCardIds) {
        const parts = criteria(card(id));
        expect(parts.length, id).toBeGreaterThan(1);
        for (const criterion of parts) expect(criterion.allocation, `${id} ${criterion.id}`).toBeDefined();
      }
      const row = inventory.papers.find(p => p.key === `${review.year}|${review.level}|${paper.fileid}`)!;
      expect(row.markBankCardIds.slice().sort()).toEqual([...review.legacyCardIds, ...practiceIds(review)].sort());
      expect(row).toMatchObject({ fullVisualReview: 'complete', bankAtlasTaskParity: 'complete', partAndSelectionReconciliation: 'complete' });
    });
  }
});

// New Paper 2 cards (2020 has no legacy cards): every card is the file's own, carded from the reviewed paper and scheme.
const NEW_PAPER_TWO = [
  { file: higher2020P2, fileid: 'LC001ALP200IV.pdf', cards: 78, readingWhole: 12 },
  { file: ordinary2020P2, fileid: 'LC001GLP200IV.pdf', cards: 52, readingWhole: 10 },
  { file: higher2019P2, fileid: 'LC001ALP200IV.pdf', cards: 60, readingWhole: 12 },
  { file: ordinary2019P2, fileid: 'LC001GLP200IV.pdf', cards: 50, readingWhole: 10 },
  { file: higher2018P2, fileid: 'LC001ALP200IV.pdf', cards: 61, readingWhole: 12 },
  { file: ordinary2018P2, fileid: 'LC001GLP200IV.pdf', cards: 53, readingWhole: 10 },
  { file: higher2017P2, fileid: 'LC001ALP200IV.pdf', cards: 62, readingWhole: 12 },
  { file: ordinary2017P2, fileid: 'LC001GLP200IV.pdf', cards: 60, readingWhole: 10 },
  { file: higher2016P2, fileid: 'LC001ALP200IV.pdf', cards: 64, readingWhole: 12 },
  { file: ordinary2016P2, fileid: 'LC001GLP200IV.pdf', cards: 54, readingWhole: 10 },
  { file: higher2015P2, fileid: 'LC001ALP200IV.pdf', cards: 64, readingWhole: 12 },
  { file: ordinary2015P2, fileid: 'LC001GLP200IV.pdf', cards: 48, readingWhole: 10 },
  { file: higher2014P2, fileid: 'LC001ALP200IV.pdf', cards: 60, readingWhole: 12 },
  { file: ordinary2014P2, fileid: 'LC001GLP200IV.pdf', cards: 53, readingWhole: 10 },
  { file: higher2013P2, fileid: 'LC001ALP200IV.pdf', cards: 60, readingWhole: 12 },
  { file: ordinary2013P2, fileid: 'LC001GLP200IV.pdf', cards: 63, readingWhole: 10 },
  { file: higher2012P2, fileid: 'LC001ALP200IV.pdf', cards: 46, readingWhole: 12 },
];

describe('Irish archive review: new Paper 2 cards', () => {
  for (const paper of NEW_PAPER_TWO) {
    const { review } = paper.file;
    it(`${review.year} ${review.level} ${paper.fileid}: ${paper.cards} cards, every printed part its own criterion`, () => {
      expect(paper.file.cards).toHaveLength(paper.cards);
      expect(review.readingWholeCardIds).toHaveLength(paper.readingWhole);
      for (const { id } of paper.file.cards) {
        const c = card(id);
        expect(tariffReconciles(c), id).toBe(true);
        expect(irishMarks(c, irishFullScores(c)), id).toBe(c.totalMarks);
        expect(shown(c), id).not.toMatch(OURS);
        if (c.practiceFocus) expect(c.practiceFocus, id).toMatch(/^[A-Z][a-z]/);
        for (const criterion of criteria(c).filter(x => x.kind === 'award' && x.guidanceKind !== 'quality')) {
          expect(criterion.allocation, `${id} ${criterion.id}`).toBeDefined();
        }
      }
      const row = inventory.papers.find(p => p.key === `${review.year}|${review.level}|${paper.fileid}`)!;
      expect(row.markBankCardIds.slice().sort()).toEqual(paper.file.cards.map(c => c.id).sort());
      expect(row).toMatchObject({ fullVisualReview: 'complete', bankAtlasTaskParity: 'complete', partAndSelectionReconciliation: 'complete' });
    });
  }
});
