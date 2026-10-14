/** @license SPDX-License-Identifier: Apache-2.0 */
import { createHash } from 'node:crypto';
import { execFileSync, spawnSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { CARDS as HIGHER } from '../components/MarkBank/cards/business/higher';
import { CARDS as ORDINARY } from '../components/MarkBank/cards/business/ordinary';
import { cardsForTopic } from '../components/MarkBank/deck';
import authored from '../scripts/markbank/authored/business.json';
import supplement from '../components/MarkBank/cards/business/rubric-authored.json';
import routePools from '../components/MarkBank/cards/business/route-pools.json';
import selectionReviews from '../scripts/markbank/authored/business-selection-reviews.json';
import { expandBusinessRoutePools } from '../components/MarkBank/cards/business/routes.mjs';
import SessionScreen, { rubricMarks } from '../components/MarkBank/SessionScreen';
import { businessMarks, businessScoreId, type BusinessScores } from '../components/MarkBank/businessRubric';
import { isRubricCard, tariffReconciles } from '../types/markBank';
import { examQuestionPartReferencesForSubject, curriculumNodeIdsForExamTopic, examTopicIdsForQuestion } from '../data/examTopics/registry';
import { vaultPdf } from '../components/PaperTrail/vaultDocs';

vi.mock('../components/PaperTrail/vaultDocs', () => ({
  vaultPdf: vi.fn(() => new Promise(() => {})),
}));

const cards = [...HIGHER, ...ORDINARY];
// Direct SEC review files questions under the examined 1999 syllabus; provider
// joins to the redeveloped (2027) course remain attached beside them.
const outgoing = (ids: string[]) => ids.filter(id => !id.startsWith('business-2027-'));
const businessRubrics = HIGHER.filter(isRubricCard).filter(card => card.rubric.system === 'business');
const reviewed = businessRubrics.filter(card => card.section === '2');
const enterprise = reviewed.find(card => card.id === 'bus-2025-hl-s2-abq-a')!;
const hasPdfParser = (() => {
  try { execFileSync('python3', ['-c', 'import pymupdf'], { stdio: 'ignore' }); return true; }
  catch { return false; }
})();

describe('Business corpus completion in progress', () => {
  it.skipIf(!hasPdfParser)('blocks normal generation before deck writes while selection review is incomplete', () => {
    const path = 'components/MarkBank/cards/business/higher.ts';
    const before = readFileSync(path, 'utf8');
    const result = spawnSync('node', ['scripts/markbank/build-deck.mjs',
      'scripts/markbank/authored/business.json'], { encoding: 'utf8' });
    expect(result.status).not.toBe(0);
    expect(result.stderr).toContain('Business source review blocks generation');
    expect(result.stderr).toContain('unclassified Business selection directives');
    expect(readFileSync(path, 'utf8')).toBe(before);
  }, 30_000);

  it('expands the printed any-two-of-three pool to all three distinct 20-mark routes', () => {
    const routes = expandBusinessRoutePools(routePools.pools.filter(pool => pool.id === 'bus-2013-hl-s3-q1b'));
    expect(routes.map(route => route.selectedOptionIds)).toEqual([
      ['small-claims', 'labour-relations'], ['small-claims', 'employment-appeals'],
      ['labour-relations', 'employment-appeals'],
    ]);
    expect(routes.map(route => route.id)).toEqual([
      'bus-2013-hl-s3-q1b-small-claims-labour-relations',
      'bus-2013-hl-s3-q1b-small-claims-employment-appeals',
      'bus-2013-hl-s3-q1b-labour-relations-employment-appeals',
    ]);
    expect(new Set(routes.map(route => route.questionText)).size).toBe(3);
    for (const route of routes) {
      const card = businessRubrics.find(item => item.id === route.id)!;
      expect(card.totalMarks).toBe(20);
      expect(tariffReconciles(card)).toBe(true);
      expect(card.sourceMaterial?.label).toBe('QUESTION PAPER');
      expect(card.sourceMaterial?.pages).toEqual([6]);
      expect(card.questionText).toBe('Evaluate the following two legislative approaches to solving conflict:\n'
        + route.selectedOptionIds.map(id => routePools.pools[0].options.find(option => option.id === id)!.label).join('\n'));
      expect(card.rubric.system === 'business' && card.rubric.schemePages).toEqual([7, 21, 22]);
      expect(examTopicIdsForQuestion('business', 'higher', 2013, 'main', 'S3Q1', 'single')
        .flatMap(topic => curriculumNodeIdsForExamTopic(topic))).toContain(card.topicId);
    }
  });

  it('rejects an incomplete ordered tariff instead of producing partial routes', () => {
    const pool = routePools.pools.find(pool => pool.id === 'bus-2013-hl-s3-q1b')!;
    expect(() => expandBusinessRoutePools([{ ...pool, orderedResponses: [pool.options[0].response] }]))
      .toThrow('Invalid Business route pool');
  });

  it('pins every 2014 short-question boundary and keeps all required rows together', () => {
    const expected = {
      '1': [10], '2': [10], '3': [10], '4': [10], '5': [4, 6],
      '6': [10], '7': [4, 6], '8': [10], '9': [10], '10': [2, 3, 2, 3],
    };
    const cohort = businessRubrics.filter(card => card.year === 2014 && card.section === '1');
    expect(cohort).toHaveLength(15);
    expect(cohort.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(100);
    for (const [q, marks] of Object.entries(expected)) {
      expect(cohort.filter(card => card.questionRef.match(/ Q(\d+)/)?.[1] === q)
        .map(card => card.totalMarks)).toEqual(marks);
    }
    const match = cohort.find(card => card.id === 'bus-2014-hl-s1-q2')!;
    if (match.rubric.system !== 'business') throw new Error('Wrong rubric');
    expect(match.rubric.responses.map(response => response.allocations[0].maxMarks)).toEqual([2, 2, 2, 2, 2]);
    const abbreviations = cohort.find(card => card.id === 'bus-2014-hl-s1-q6')!;
    if (abbreviations.rubric.system !== 'business') throw new Error('Wrong rubric');
    expect(abbreviations.rubric.responses[0].allocations[0].permittedMarks).toEqual([0, 3, 6, 8, 9, 10]);
  });

  it.each([
    [1, [12, 13, 15, 20]], [2, [20, 20, 20]], [3, [4, 16, 20, 20]],
    [4, [20, 20, 20]], [5, [25, 4, 10, 6, 15]],
    [6, [5, 10, 10, 15, 4, 16]], [7, [25, 10, 10, 15]],
  ] as const)('retains the marked 2014 Section 3 Q%i tasks at 60 marks, each printed choice one card', (q, marks) => {
    const all = businessRubrics.filter(card => card.id.startsWith(`bus-2014-hl-s3-q${q}`));
    expect(all.map(card => card.totalMarks)).toEqual(marks);
    expect(all.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(60);
  });

  it.each([2014, 2015, 2016, 2017, 2018, 2019])('maps every reviewed %i task and each additional topic to the correct section identity', year => {
    for (const card of businessRubrics.filter(card => card.year === year && card.section !== '2')) {
      const q = card.questionRef.match(/ Q(\d+)/)![1];
      const n = card.section === '3' ? `S3Q${q}` : q;
      const nodes = examTopicIdsForQuestion('business', 'higher', year, 'main', n, 'single')
        .flatMap(curriculumNodeIdsForExamTopic);
      for (const topic of [card.topicId, ...(card.additionalTopicIds ?? [])]) {
        expect(nodes, card.id).toContain(topic);
        expect(cardsForTopic(topic, businessRubrics)).toContain(card);
      }
    }
  });

  it('keeps 2020 short and long numbering in the correct booklet and maps every assessed topic', () => {
    for (const card of businessRubrics.filter(card => card.year === 2020 && card.section !== '2')) {
      const q = card.questionRef.match(/ Q(\d+)/)![1];
      const paperKey = card.section === '1' ? 'p1' : 'p2';
      const nodes = examTopicIdsForQuestion('business', 'higher', 2020, 'main', q, paperKey)
        .flatMap(curriculumNodeIdsForExamTopic);
      for (const topic of [card.topicId, ...(card.additionalTopicIds ?? [])]) {
        expect(nodes, card.id).toContain(topic);
        expect(cardsForTopic(topic, businessRubrics)).toContain(card);
      }
      expect(card.paperFileid).toBe(card.section === '1' ? 'LC033ALP032EV' : 'LC033ALP041EV');
    }
    const nodes = (key: string) => outgoing(examTopicIdsForQuestion('business', 'higher', 2020, 'main', '1', key)
      .flatMap(curriculumNodeIdsForExamTopic));
    expect(nodes('p1')).toEqual(['business-4-17']);
    expect(nodes('p2')).toEqual(['business-0-12', 'business-0-13', 'business-0-14']);
  });

  it('preserves all 2020 short-question boundaries and the exceptional True/False answer', () => {
    const cohort = businessRubrics.filter(card => card.year === 2020 && card.section === '1');
    const expected = { '1': [10], '2': [10], '3': [4, 6], '4': [10], '5': [4, 3, 3],
      '6': [5, 5], '7': [10], '8': [10], '9': [6, 4], '10': [6, 4] };
    expect(cohort).toHaveLength(16);
    expect(cohort.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(100);
    for (const [q, marks] of Object.entries(expected)) {
      expect(cohort.filter(card => card.questionRef.match(/ Q(\d+)/)?.[1] === q)
        .map(card => card.totalMarks)).toEqual(marks);
    }
    for (const q of [1, 2, 4, 7]) {
      const card = cohort.find(card => card.id === `bus-2020-hl-s1-q${q}`)!;
      if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
      expect(card.rubric.responses[0].allocations[0].permittedMarks).toEqual([0, 3, 5, 7, 9, 10]);
    }
    const tf = cohort.find(card => card.id === 'bus-2020-hl-s1-q7')!;
    if (tf.rubric.system !== 'business') throw new Error('Wrong rubric');
    expect(tf.rubric.guidance.join(' ')).toContain('4 False or True');
    expect(tf.rubric.guidance.join(' ')).toContain('count that statement only once');
    const reason = cohort.find(card => card.id === 'bus-2020-hl-s1-q10ii')!;
    for (const value of ['€200,000', '€250,000', '€36,000', '€28,800']) expect(reason.questionText).toContain(value);
    expect(reason.sourceMaterial?.pages).toEqual([7]);
    expect(cohort.find(card => card.id === 'bus-2020-hl-s1-q5ii')!.questionText)
      .toContain('other than a Regulation');
  });

  it.each([
    [1, [7, 7, 6, 20, 20]], [2, [15, 5, 20, 20]], [3, [8, 8, 4, 25, 15]],
    [4, [20, 10, 10, 8, 12]], [5, [5, 15, 20, 20]],
    [6, [6, 14, 15, 5, 5, 15]], [7, [20, 5, 20, 15]],
  ] as const)('preserves 2020 Section 3 Q%i boundaries at 60 marks, the printed choice one card', (q, marks) => {
    const all = businessRubrics.filter(card => card.id.startsWith(`bus-2020-hl-s3-q${q}`));
    expect(all.map(card => card.totalMarks)).toEqual(marks);
    expect(all.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(60);
  });

  it('retains the 2020 infographic scale, eight calculation marks and evaluation requirements', () => {
    const calc = businessRubrics.find(card => card.id === 'bus-2020-hl-s3-q3a-ii')!;
    if (calc.rubric.system !== 'business') throw new Error('Wrong rubric');
    expect(calc.sourceMaterial?.pages).toEqual([4]);
    expect(calc.rubric.schemePages).toEqual([9, 41]);
    expect(calc.rubric.responses[0].allocations.map(a => a.maxMarks)).toEqual(Array(8).fill(1));
    expect(calc.rubric.responses[0].allocations.map(a => a.label)).toContain('Balance: −€5bn');
    expect(calc.rubric.responses[0].allocations.at(-1)!.label).toBe('Deficit');
    const debt = businessRubrics.find(card => card.id === 'bus-2020-hl-s3-q5c')!;
    if (debt.rubric.system !== 'business') throw new Error('Wrong rubric');
    expect(debt.rubric.responses.map(r => r.allocations.map(a => a.maxMarks)))
      .toEqual([[2, 2], [2, 2], [2, 2], [2, 2], [4]]);
    expect(debt.rubric.responses.at(-1)!.allocations[0].permittedMarks).toEqual([0, 2, 4]);
    expect(businessMarks(debt, { [businessScoreId('response-5', 'evaluate')]: 3 })).toBe(2);
    expect(debt.rubric.guidance.join(' ')).toContain('contradictory example');
    const mix = businessRubrics.find(card => card.id === 'bus-2020-hl-s3-q7b-ii')!;
    if (mix.rubric.system !== 'business') throw new Error('Wrong rubric');
    expect(mix.questionText).toMatch(/^Evaluate the Promotion and Place/);
    expect(mix.rubric.responses.map(r => r.label)).toEqual(['Promotion', 'Place']);
    expect(mix.rubric.responses.map(r => r.allocations.map(a => a.maxMarks))).toEqual([[4, 1, 4, 1], [4, 1, 4, 1]]);
    expect(businessRubrics.find(card => card.id === 'bus-2020-hl-s3-q6c-ii')!.questionText)
      .toContain('other than public liability');
  });

  it('preserves every 2019 short-question boundary and its graphical source', () => {
    const cohort = businessRubrics.filter(card => card.year === 2019 && card.section === '1');
    const expected = { '1': [10], '2': [10], '3': [10], '4': [10], '5': [4, 6],
      '6': [10], '7': [2, 4, 2, 2], '8': [10], '9': [10], '10': [4, 3, 3] };
    expect(cohort).toHaveLength(16);
    expect(cohort.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(100);
    for (const [q, marks] of Object.entries(expected)) {
      expect(cohort.filter(card => card.questionRef.match(/ Q(\d+)/)?.[1] === q)
        .map(card => card.totalMarks)).toEqual(marks);
    }
    for (const q of [1, 3, 4]) {
      const card = cohort.find(card => card.id === `bus-2019-hl-s1-q${q}`)!;
      if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
      expect(card.rubric.responses[0].allocations[0].permittedMarks).toEqual([0, 3, 5, 7, 9, 10]);
    }
    for (const card of cohort.filter(card => /-q7/.test(card.id))) {
      expect(card.sourceMaterial?.pages).toEqual([4]);
      expect(card.questionText).toContain('infographic');
    }
    const identification = cohort.find(card => card.id === 'bus-2019-hl-s1-q7iii')!;
    if (identification.rubric.system !== 'business') throw new Error('Wrong rubric');
    expect(identification.rubric.responses[0].allocations[0].label).toBe('Coffee or wine');
    const profit = cohort.find(card => card.id === 'bus-2019-hl-s1-q10ii')!;
    if (profit.rubric.system !== 'business') throw new Error('Wrong rubric');
    expect(profit.sourceMaterial?.pages).toEqual([5]);
    expect(profit.rubric.responses[0].allocations.map(a => a.label))
      .toEqual(['Total revenue: €270,000', 'Total costs: €240,000', 'Profit: €30,000']);
    expect(profit.rubric.guidance.join(' ')).toContain('€ thousands');
  });

  it.each([
    [1, [20, 15, 10, 15]], [2, [15, 10, 20, 15]], [3, [25, 15, 20]],
    [4, [10, 10, 20, 10, 10]], [5, [15, 3, 9, 7, 6, 20]],
    [6, [5, 15, 15, 10, 15]], [7, [18, 7, 5, 15, 15]],
  ] as const)('preserves every 2019 Section 3 Q%i mark boundary and its full 60 marks', (q, marks) => {
    const cohort = businessRubrics.filter(card => card.id.startsWith(`bus-2019-hl-s3-q${q}`));
    expect(cohort.map(card => card.totalMarks)).toEqual(marks);
    expect(cohort.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(60);
    expect(routePools.pools.some(pool => pool.template.year === 2019)).toBe(false);
  });

  it('counts each 2019 ratio formula once across both years and supplies independent analysis context', () => {
    for (const [suffix, marks, rowMarks, answers] of [
      ['current', 7, [1, 3, 3], ['2:1', '2.5:1']],
      ['acid', 9, [1, 4, 4], ['1.5:1', '0.8:1']],
    ] as const) {
      const card = businessRubrics.find(card => card.id === `bus-2019-hl-s3-q5b-ii-${suffix}`)!;
      expect(card.totalMarks).toBe(marks);
      expect(card.questionRef).toBe('2019 HL Section 3 Q5(B)(ii)');
      expect(card.questionText).toContain('both 2017 and 2018');
      expect(card.sourceMaterial?.pages).toEqual([11]);
      if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
      expect(card.rubric.schemePages).toEqual([11, 41]);
      expect(card.rubric.responses.map(r => r.allocations.length)).toEqual(rowMarks);
      expect(card.rubric.responses.flatMap(r => r.allocations).filter(a => a.id === 'formula')).toHaveLength(1);
      expect(card.rubric.responses.slice(1).map(r => r.allocations.at(-1)!.label)).toEqual(answers);
      expect(tariffReconciles(card)).toBe(true);
    }
    const analysis = businessRubrics.find(card => card.id === 'bus-2019-hl-s3-q5b-iii')!;
    for (const ratio of ['2:1', '2.5:1', '1.5:1', '0.8:1']) expect(analysis.questionText).toContain(ratio);
    expect(analysis.questionText).not.toContain('2:5:1');
  });

  it('retains the 2019 evaluation scales, required headings and excluded examples', () => {
    const find = (part: string) => {
      const card = businessRubrics.find(card => card.id === `bus-2019-hl-s3-${part}`)!;
      if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
      return card;
    };
    const claims = find('q1c');
    const eu = find('q3a');
    if (claims.rubric.system !== 'business' || eu.rubric.system !== 'business') throw new Error('Wrong rubric');
    expect(claims.rubric.responses.at(-1)!.allocations[0].permittedMarks).toEqual([0, 1, 3]);
    expect(eu.rubric.responses.map(r => r.allocations.map(a => a.maxMarks)))
      .toEqual([[3, 3, 3], [3, 3], [3, 3], [4]]);
    expect(eu.rubric.responses.at(-1)!.allocations[0].permittedMarks).toEqual([0, 2, 4]);
    expect(businessMarks(eu, { [businessScoreId('response-4', 'evaluate')]: 3 })).toBe(2);
    expect(find('q2a-ii').questionText).toContain('biodegradable cutlery and napkins');
    expect(find('q6b-ii').questionText).toContain('other than a strategic alliance');
    const stages = find('q6a-ii');
    if (stages.rubric.system !== 'business') throw new Error('Wrong rubric');
    expect(stages.rubric.responses.map(r => r.label)).toEqual(['Feasibility Study', 'Prototype Development', 'Test Marketing']);
    expect(stages.rubric.responses.map(r => r.allocations.map(a => a.maxMarks)))
      .toEqual([[3, 2], [3, 2], [3, 2]]);
  });

  it('preserves the 2018 short-task boundaries, graph source and cumulative row sequence', () => {
    const cohort = businessRubrics.filter(card => card.year === 2018 && card.section === '1');
    const expected = { '1': [10], '2': [10], '3': [10], '4': [10], '5': [2, 2, 6],
      '6': [10], '7': [4, 6], '8': [10], '9': [10], '10': [10] };
    expect(cohort).toHaveLength(13);
    expect(cohort.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(100);
    for (const [q, marks] of Object.entries(expected)) {
      expect(cohort.filter(card => card.questionRef.match(/ Q(\d+)/)?.[1] === q)
        .map(card => card.totalMarks)).toEqual(marks);
    }
    for (const q of [1, 3, 4, 9]) {
      const card = cohort.find(card => card.id === `bus-2018-hl-s1-q${q}`)!;
      if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
      expect(card.rubric.responses[0].allocations[0].permittedMarks).toEqual([0, 3, 5, 7, 9, 10]);
    }
    for (const suffix of ['i', 'ii']) {
      const card = cohort.find(card => card.id === `bus-2018-hl-s1-q5${suffix}`)!;
      expect(card.sourceMaterial?.pages).toEqual([3]);
      expect(card.questionText).toContain('bar chart');
    }
    const table = cohort.find(card => card.id === 'bus-2018-hl-s1-q6')!;
    if (table.rubric.system !== 'business') throw new Error('Wrong rubric');
    expect(table.rubric.responses.map(response => response.allocations[0].permittedMarks))
      .toEqual([[0, 2], [0, 2], [0, 2], [0, 2], [0, 2]]);
  });

  it.each([
    [1, [4, 21, 15, 20]], [2, [20, 25, 15]], [3, [20, 20, 20]],
    [4, [5, 20, 20, 5, 10]], [5, [20, 25, 15]],
    [6, [20, 20, 10, 7, 1, 2]], [7, [9, 10, 6, 10, 10, 15]],
  ] as const)('preserves every 2018 Section 3 Q%i boundary without generating scheme-only choices', (q, marks) => {
    const cohort = businessRubrics.filter(card => card.id.startsWith(`bus-2018-hl-s3-q${q}`));
    expect(cohort.map(card => card.totalMarks)).toEqual(marks);
    expect(cohort.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(60);
    expect(routePools.pools.some(pool => pool.template.year === 2018)).toBe(false);
  });

  it('counts the 2018 shared tax setup once and retains exact net-pay partial credit', () => {
    const taxes = ['i', 'ii', 'iii', 'iv'].map(suffix =>
      businessRubrics.find(card => card.id === `bus-2018-hl-s3-q6c-${suffix}`)!);
    expect(taxes.map(card => card.totalMarks)).toEqual([10, 7, 1, 2]);
    expect(taxes.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(20);
    for (const card of taxes) {
      expect(card.sourceMaterial?.pages).toEqual([11]);
      if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
      expect(card.rubric.schemePages).toEqual([12, 56]);
    }
    if (taxes[0].rubric.system !== 'business') throw new Error('Wrong rubric');
    expect(taxes[0].rubric.responses.map(response => response.allocations.map(a => a.maxMarks)))
      .toEqual([[2], [3, 1, 1, 1, 1, 1]]);
    expect(taxes[1].questionText).toContain('€60,000');
    expect(taxes[2].questionText).toContain('€60,000');
    expect(taxes[3].questionText).toContain('PAYE €13,720, USC €2,137.09 and PRSI €2,400');
    const net = taxes[3];
    if (net.rubric.system !== 'business') throw new Error('Wrong rubric');
    expect(net.rubric.responses[0].allocations[0].permittedMarks).toEqual([0, 1, 2]);
    expect(net.rubric.taskRequirements.join(' ')).toContain('€41,742.91');
    expect(businessMarks(net, { [businessScoreId('response-1', 'answer')]: 1 })).toBe(1);
    expect(businessMarks(net, { [businessScoreId('response-1', 'answer')]: 2 })).toBe(2);
    expect(net.rubric.guidance.join(' ')).toContain('only other accepted figure');
  });

  it('retains the 2018 lifecycle diagram marks and required extension-method distinction', () => {
    const diagram = businessRubrics.find(card => card.id === 'bus-2018-hl-s3-q7a-i-diagram')!;
    const stages = businessRubrics.find(card => card.id === 'bus-2018-hl-s3-q7a-i-stages')!;
    expect(diagram.questionRef).toBe('2018 HL Section 3 Q7(A)(i)');
    expect(stages.questionRef).toBe(diagram.questionRef);
    if (diagram.rubric.system !== 'business' || stages.rubric.system !== 'business') throw new Error('Wrong rubric');
    expect(diagram.sourceMaterial?.pages).toEqual([12]);
    expect(diagram.rubric.schemePages).toEqual([13, 57]);
    expect(diagram.rubric.responses[0].allocations.map(a => a.id)).toEqual([
      'introduction', 'growth', 'maturity', 'saturation', 'decline', 'title', 'sales', 'time', 'curve',
    ]);
    expect(diagram.rubric.responses[0].allocations.every(a => a.maxMarks === 1)).toBe(true);
    expect(stages.rubric.responses.map(r => r.allocations[0].maxMarks)).toEqual([2, 2, 2, 2, 2]);
    const extension = businessRubrics.find(card => card.id === 'bus-2018-hl-s3-q7a-ii')!;
    if (extension.rubric.system !== 'business') throw new Error('Wrong rubric');
    expect(extension.rubric.taskRequirements.join(' ')).toContain('two different elements');
  });

  it('keeps the 2018 whole letter and fixed heading tariffs with compulsory conditions', () => {
    const find = (part: string) => {
      const card = businessRubrics.find(card => card.id === `bus-2018-hl-s3-${part}`)!;
      if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
      return card.rubric;
    };
    const letter = find('q5b');
    expect(letter.responses.map(r => r.allocations.map(a => a.maxMarks)))
      .toEqual([[1, 1, 2, 2, 1, 1, 1], [2, 2], [2, 2], [2, 2], [2], [2]]);
    expect(letter.guidance.join(' ')).toContain('At least one of the three policies');
    expect(find('q4a-ii').responses.map(r => r.allocations.map(a => a.maxMarks)))
      .toEqual([[5, 2, 1], [5, 2, 1], [2, 2]]);
    expect(find('q6a').responses.map(r => r.allocations.map(a => a.maxMarks)))
      .toEqual([[5, 2], [5, 2], [4], [2]]);
    expect(find('q2b').guidance.join(' ')).toContain('Only one government point');
    expect(find('q2c').responses.at(-1)!.allocations[0].permittedMarks).toEqual([0, 3]);
    expect(find('q3a').responses.at(-1)!.allocations[0].permittedMarks).toEqual([0, 2]);
    expect(find('q7c').responses.at(-1)!.allocations[0].permittedMarks).toEqual([0, 2]);
  });

  it('retains the marked 2015 short tasks, cumulative row tariffs and independent calculation context', () => {
    const cohort = businessRubrics.filter(card => card.year === 2015 && card.section === '1');
    expect(cohort).toHaveLength(13);
    const expected = { '1': [10], '2': [4, 6], '3': [6, 4], '4': [10], '5': [10],
      '6': [10], '7': [6, 4], '8': [10], '9': [10], '10': [10] };
    for (const [q, marks] of Object.entries(expected)) {
      expect(cohort.filter(card => card.questionRef.match(/ Q(\d+)/)?.[1] === q)
        .map(card => card.totalMarks)).toEqual(marks);
    }
    expect(cohort.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(100);
    for (const q of [4, 8]) {
      const card = cohort.find(card => card.id === `bus-2015-hl-s1-q${q}`)!;
      if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
      expect(card.rubric.responses[0].allocations[0].permittedMarks).toEqual([0, 3, 6, 8, 9, 10]);
    }
    const trend = cohort.find(card => card.id === 'bus-2015-hl-s1-q3b')!;
    expect(trend.questionText).toContain('25% in 2013 and 20% in 2014');
    expect(trend.sourceMaterial?.pages).toEqual([2]);
  });

  it.each([
    [1, [20, 10, 10, 9, 11], null], [2, [20, 20, 20], null], [3, [20, 20, 20], null],
    [4, [12, 13, 15, 20], null], [5, [9, 16, 5, 15, 15], null],
    [6, [5, 5, 10, 15, 10, 7, 8], null], [7, [25, 6, 14, 5, 10], null],
  ] as const)('preserves the 2015 Section 3 Q%i boundaries and each complete 60-mark route', (q, marks, poolPart) => {
    const cohort = businessRubrics.filter(card => card.id.startsWith(`bus-2015-hl-s3-q${q}`));
    const routes = poolPart ? cohort.filter(card => card.id.startsWith(`bus-2015-hl-s3-q${q}${poolPart}-`)) : [];
    const base = cohort.filter(card => !routes.includes(card));
    expect(base.map(card => card.totalMarks)).toEqual(marks);
    const baseTotal = base.reduce((sum, card) => sum + card.totalMarks, 0);
    if (routes.length) for (const route of routes) expect(baseTotal + route.totalMarks).toBe(60);
    else expect(baseTotal).toBe(60);
  });

  it('keeps the 2015 cash-flow table, insurance exclusion and required marketing headings', () => {
    const find = (suffix: string) => businessRubrics.find(card => card.id === `bus-2015-hl-s3-${suffix}`)!;
    const cash = find('q6c-ii');
    expect(cash.sourceMaterial?.pages).toEqual([9]);
    if (cash.rubric.system !== 'business') throw new Error('Wrong rubric');
    expect(cash.rubric.responses.map(response => response.allocations.map(allocation => allocation.maxMarks)))
      .toEqual([[2], [2, 1], [2]]);
    expect(find('q6a-iii').questionText).toContain('other than utmost good faith');
    const mix = find('q7a');
    expect(mix.sourceMaterial?.pages).toEqual([10]);
    if (mix.rubric.system !== 'business') throw new Error('Wrong rubric');
    expect(mix.rubric.responses.map(response => response.allocations.map(allocation => allocation.maxMarks)))
      .toEqual([[3, 3, 3], [3, 2, 3], [3, 2, 3]]);
  });

  it('preserves all 2016 short boundaries and shared correct-answer sequences', () => {
    const cohort = businessRubrics.filter(card => card.year === 2016 && card.section === '1');
    expect(cohort).toHaveLength(13);
    const expected = { '1': [10], '2': [4, 6], '3': [10], '4': [10], '5': [6, 4],
      '6': [10], '7': [6, 4], '8': [10], '9': [10], '10': [10] };
    for (const [q, marks] of Object.entries(expected)) {
      expect(cohort.filter(card => card.questionRef.match(/ Q(\d+)/)?.[1] === q)
        .map(card => card.totalMarks)).toEqual(marks);
    }
    expect(cohort.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(100);
    for (const q of [1, 3, 4, 10]) {
      const card = cohort.find(card => card.id === `bus-2016-hl-s1-q${q}`)!;
      if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
      expect(card.rubric.responses[0].allocations[0].permittedMarks)
        .toEqual(q === 10 ? [0, 4, 7, 10] : [0, 3, 6, 8, 9, 10]);
    }
    expect(cohort.find(card => card.id === 'bus-2016-hl-s1-q5b')!.questionText).toContain('2:1');
    expect(cohort.find(card => card.id === 'bus-2016-hl-s1-q7a')!.sourceMaterial?.pages).toEqual([4]);
  });

  it.each([
    [1, [12, 8, 20, 20]], [2, [20, 20, 20]], [3, [20, 20, 20]], [4, [20, 20, 20]],
    [5, [20, 20, 5, 15]], [6, [15, 25, 15, 5]], [7, [15, 10, 15, 20]],
  ] as const)('preserves the 2016 Section 3 Q%i mark boundaries at 60, the printed choice one card', (q, marks) => {
    const cohort = businessRubrics.filter(card => card.id.startsWith(`bus-2016-hl-s3-q${q}`));
    expect(cohort.map(card => card.totalMarks)).toEqual(marks);
    expect(cohort.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(60);
  });

  it('keeps the 2016 chart tasks whole and limits calculation-only scoring to the published 12 and 5 marks', () => {
    const original = businessRubrics.find(card => card.id === 'bus-2016-hl-s3-q6b')!;
    const changed = businessRubrics.find(card => card.id === 'bus-2016-hl-s3-q6c-i')!;
    for (const card of [original, changed]) {
      expect(card.questionText).toContain('60,000');
      expect(card.questionText).toContain('€400,000');
      expect(card.sourceMaterial?.pages).toEqual([9]);
      expect(tariffReconciles(card)).toBe(true);
    }
    const calculationOnly = Object.fromEntries(['bep', 'mos', 'profit']
      .map(id => [businessScoreId('response-2', id), 4]));
    expect(businessMarks(original, calculationOnly)).toBe(12);
    expect(businessMarks(changed, { [businessScoreId('response-1', 'bep')]: 5 })).toBe(5);
    for (const card of [original, changed]) {
      if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
      const scores = Object.fromEntries(card.rubric.responses.flatMap(response => response.allocations
        .map(allocation => [businessScoreId(response.id, allocation.id), allocation.maxMarks])));
      expect(businessMarks(card, scores)).toBe(card === original ? 25 : 15);
    }
    if (original.rubric.system !== 'business' || changed.rubric.system !== 'business') throw new Error('Wrong rubric');
    expect(original.rubric.schemePages).toEqual([11, 41]);
    expect(changed.rubric.schemePages).toEqual([11, 41, 42]);
    expect(original.rubric.guidance.join(' ')).toContain('at most 12');
    expect(changed.rubric.guidance.join(' ')).toContain('at most 5');
  });

  it('preserves 2017 short-task boundaries and the changed 3/2/2/2/1 sequence', () => {
    const cohort = businessRubrics.filter(card => card.year === 2017 && card.section === '1');
    expect(cohort).toHaveLength(13);
    const expected = { '1': [10], '2': [10], '3': [10], '4': [10], '5': [10],
      '6': [10], '7': [6, 4], '8': [6, 4], '9': [6, 4], '10': [10] };
    for (const [q, marks] of Object.entries(expected)) {
      expect(cohort.filter(card => card.questionRef.match(/ Q(\d+)/)?.[1] === q)
        .map(card => card.totalMarks)).toEqual(marks);
    }
    expect(cohort.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(100);
    for (const q of [1, 2, 3, 4, 5]) {
      const card = cohort.find(card => card.id === `bus-2017-hl-s1-q${q}`)!;
      if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
      expect(card.rubric.responses[0].allocations[0].permittedMarks).toEqual([0, 3, 5, 7, 9, 10]);
      expect(businessMarks(card, { [businessScoreId('response-1', 'component-1')]: 6 })).toBe(5);
    }
    const diagram = cohort.find(card => card.id === 'bus-2017-hl-s1-q8a')!;
    expect(diagram.sourceMaterial?.pages).toEqual([4]);
    if (diagram.rubric.system !== 'business') throw new Error('Wrong rubric');
    expect(diagram.rubric.responses[0].allocations[0].permittedMarks).toEqual([0, 2, 4, 5, 6]);
    const margin = cohort.find(card => card.id === 'bus-2017-hl-s1-q8b')!;
    if (margin.rubric.system !== 'business') throw new Error('Wrong rubric');
    expect(margin.rubric.guidance.join(' ')).toContain('€450,000');
    expect(margin.rubric.guidance.join(' ')).toContain('unit of measurement is required');
  });

  it.each([
    [1, [5, 15, 20, 2, 18]], [2, [15, 5, 15, 8, 17]], [3, [13, 12, 15, 20]],
    [4, [20, 20, 20]], [5, [25, 15, 12, 8]], [6, [15, 4, 4, 6, 6, 14, 5, 6]],
    [7, [6, 14, 15, 5, 20]],
  ] as const)('preserves every 2017 Section 3 Q%i boundary without inventing routes from required headings', (q, marks) => {
    const cohort = businessRubrics.filter(card => card.id.startsWith(`bus-2017-hl-s3-q${q}`));
    expect(cohort.map(card => card.totalMarks)).toEqual(marks);
    expect(cohort.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(60);
    for (const card of cohort) expect(tariffReconciles(card), card.id).toBe(true);
    expect(routePools.pools.some(pool => pool.template.year === 2017)).toBe(false);
  });

  it('keeps 2017 compulsory report headings, consumer provision and product-development order', () => {
    const find = (suffix: string) => businessRubrics.find(card => card.id === `bus-2017-hl-s3-${suffix}`)!;
    const report = find('q4c');
    if (report.rubric.system !== 'business') throw new Error('Wrong rubric');
    expect(report.sourceMaterial?.pages).toEqual([8]);
    expect(report.rubric.schemePages).toEqual([10, 42]);
    expect(report.rubric.responses[0].allocations.map(item => item.id))
      .toEqual(['title', 'to', 'from', 'date', 'terms', 'findings']);
    expect(report.rubric.responses.map(response => response.allocations.reduce((sum, a) => sum + a.maxMarks, 0)))
      .toEqual([6, 5, 5, 4]);
    const consumer = find('q1c-ii');
    expect(consumer.questionText).toContain('Sale of Goods and Supply of Services Act 1980');
    if (consumer.rubric.system !== 'business') throw new Error('Wrong rubric');
    expect(consumer.rubric.responses[0].label).toBe('Merchantable quality — required');
    const stages = find('q5a');
    if (stages.rubric.system !== 'business') throw new Error('Wrong rubric');
    expect(stages.rubric.responses.map(response => response.label)).toEqual([
      'Idea generation', 'Product screening', 'Concept development', 'Feasibility study', 'Prototype development',
    ]);
    expect(stages.rubric.taskRequirements.join(' ')).toContain('correct order');
    expect(stages.rubric.schemePages).toEqual([11, 43, 44]);
  });

  it('retains each 2017 ratio calculation and supplies its results to the independent analysis task', () => {
    for (const [suffix, marks] of [['i', [1, 1, 1, 1]], ['ii', [1, 1, 1, 1]],
      ['iii', [1, 1, 1, 1, 1, 1]], ['iv', [1, 1, 1, 1, 2]]] as const) {
      const card = businessRubrics.find(card => card.id === `bus-2017-hl-s3-q6b-${suffix}`)!;
      expect(card.sourceMaterial?.pages).toEqual([9]);
      if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
      expect(card.rubric.schemePages).toEqual([12, 48]);
      expect(card.rubric.responses[0].allocations.map(allocation => allocation.maxMarks)).toEqual(marks);
      for (const allocation of card.rubric.responses[0].allocations) {
        expect(allocation.permittedMarks).toEqual([0, allocation.maxMarks]);
      }
    }
    const analysis = businessRubrics.find(card => card.id === 'bus-2017-hl-s3-q6c-i')!;
    for (const value of ['20.5%', '15.2%', '8%', '4%', '2:1', '1.25:1']) expect(analysis.questionText).toContain(value);
    expect(analysis.totalMarks).toBe(14);
    const pricing = businessRubrics.find(card => card.id === 'bus-2017-hl-s3-q7b-ii')!;
    if (pricing.rubric.system !== 'business') throw new Error('Wrong rubric');
    expect(pricing.rubric.responses[0].allocations.map(allocation => allocation.permittedMarks))
      .toEqual([[0, 2], [0, 1, 3]]);
    expect(businessMarks(pricing, { [businessScoreId('response-1', 'choice')]: 2,
      [businessScoreId('response-1', 'reason')]: 2 })).toBe(3);
  });

  it('retains context when the 2014 calculation and production tasks are practised separately', () => {
    const find = (suffix: string) => businessRubrics.find(card => card.id === `bus-2014-hl-${suffix}`)!;
    expect(find('s1-q7b').questionText).toContain('leadership style of your choice');
    expect(find('s3-q5b-iii').questionText).toContain('0.33 : 1');
    expect(find('s3-q6a-ii').questionText).toContain('job production');
    expect(find('s3-q6a-iii').questionText).toContain('from job production');
    expect(find('s3-q6a-ii').sourceMaterial?.pages).toEqual([9]);
    expect(find('s3-q5b-ii').sourceMaterial?.pages).toEqual([8]);
    expect(find('s3-q4c').sourceMaterial?.pages).toEqual([8]);
  });

  it('cross-lists combined tasks without duplicating their card identities or progress', () => {
    const route = businessRubrics.find(card => card.id === 'bus-2013-hl-s3-q1b-small-claims-labour-relations')!;
    expect(route.additionalTopicIds).toEqual(['business-0-14']);
    for (const topic of ['business-0-13', 'business-0-14']) {
      expect(cardsForTopic(topic, businessRubrics).filter(card => card.id === route.id)).toEqual([route]);
    }
    const mixed = businessRubrics.find(card => card.id === 'bus-2013-hl-s1-q4')!;
    for (const topic of ['business-3-16', 'business-4-15', 'business-5-14', 'business-3-19']) {
      expect(cardsForTopic(topic, businessRubrics).filter(card => card.id === mixed.id)).toEqual([mixed]);
    }
    expect(new Set(businessRubrics.map(card => card.id)).size).toBe(businessRubrics.length);
  });

  it.skipIf(!hasPdfParser)('recovers short questions after ruled answer lines without inventing roman tasks', () => {
    const rows = JSON.parse(execFileSync('python3', ['-c', `
import json,sys
sys.path.insert(0,'scripts/markbank/authoring')
import paper_census as census
parts,_,_=census.census_sections('business',2013,'hl')
print(json.dumps(sorted(census.key_label(key) for key in census.leaves_of(parts) if key[0]=='1')))
`], { encoding: 'utf8' }));
    expect(rows).toEqual(['Q1', 'Q10', 'Q2(a)', 'Q2(b)', 'Q3(a)', 'Q3(b)', 'Q4',
      'Q5', 'Q6', 'Q7', 'Q8', 'Q9'].map(q => `Section 1 ${q}`));
  });

  it.skipIf(!hasPdfParser)('does not let 2014 matching rows or the acronym table swallow later questions', () => {
    const result = JSON.parse(execFileSync('python3', ['-c', `
import json,sys
sys.path.insert(0,'scripts/markbank/authoring')
import paper_census as census
parts,texts,_=census.census_sections('business',2014,'hl')
print(json.dumps({'keys':sorted(census.key_label(key) for key in census.leaves_of(parts) if key[0]=='1'),
 'protectionism':texts[('1',3,None,None)],'interest':texts[('1',5,'a',None)]}))
`], { encoding: 'utf8' }));
    expect(result.keys).toEqual(['Q1', 'Q10(a)', 'Q10(b)', 'Q10(c)', 'Q10(d)', 'Q2',
      'Q3', 'Q4', 'Q5(a)', 'Q5(b)', 'Q6', 'Q7(a)', 'Q7(b)', 'Q8', 'Q9']
      .map(q => `Section 1 ${q}`));
    expect(result.protectionism).toContain('protectionism');
    expect(result.interest).toContain('interest rate');
  });

  it.skipIf(!hasPdfParser)('keeps 2016 true/false statements within Q3 and retains the following insurance and gearing asks', () => {
    const result = JSON.parse(execFileSync('python3', ['-c', `
import json,sys
sys.path.insert(0,'scripts/markbank/authoring')
import paper_census as census
parts,texts,_=census.census_sections('business',2016,'hl')
next_parts,_,_=census.census_sections('business',2026,'hl')
print(json.dumps({'keys':sorted(census.key_label(key) for key in census.leaves_of(parts) if key[0]=='1'),
 'statements':texts[('1',3,None,None)],'insurance':texts[('1',4,None,None)],
 'gearing':texts[('1',5,'a',None)],
 'nextQuestion':all(('1',6,None,roman) in next_parts for roman in ['i','ii'])}))
`], { encoding: 'utf8' }));
    expect(result.keys).toEqual(['Q1', 'Q10(a)', 'Q10(b)', 'Q10(c)', 'Q2(a)', 'Q2(b)', 'Q3', 'Q4', 'Q5(a)', 'Q5(b)',
      'Q6', 'Q7(a)', 'Q7(b)', 'Q8', 'Q9'].map(q => `Section 1 ${q}`));
    expect(result.statements).toContain('Inflation refers');
    expect(result.statements).toContain('A recession represents');
    expect(result.insurance).toContain('insurance terms');
    expect(result.gearing).toContain('Lalco');
    expect(result.nextQuestion).toBe(true);
  });

  it.skipIf(!hasPdfParser)('reads the last row of the 2010 Higher EU-institutions matching table as a row, keeping Q5(a)', () => {
    const result = JSON.parse(execFileSync('python3', ['-c', `
import json,sys
sys.path.insert(0,'scripts/markbank/authoring')
import paper_census as census
parts,texts,flags=census.census_sections('business',2010,'hl')
print(json.dumps({'q4':sorted(census.key_label(k) for k in census.leaves_of(parts) if k[0]=='1' and k[1] in (4,5)),
 'q5a':texts[('1',5,'a',None)]}))
`], { encoding: 'utf8' }));
    expect(result.q4).toEqual(['Section 1 Q4', 'Section 1 Q5(a)', 'Section 1 Q5(b)']);
    expect(result.q5a).toContain('Outline the purpose of a company’s ‘Articles of Association’.');
  });

  it.skipIf(!hasPdfParser)('reads the strip-cut 2011 Ordinary page 11 from its characters for the census and the selection scan', () => {
    const result = JSON.parse(execFileSync('python3', ['-c', `
import json,sys
sys.path.insert(0,'scripts/markbank/authoring')
import paper_census as census
from strip_pages import strip_cut,page_text
from business_selection import page_directives
parts,texts,_=census.census_sections('business',2011,'ol')
doc=census.PP.pymupdf.open('paper-trail-corpus/exampapers/2011/LC033GLP000EV.pdf')
print(json.dumps({'q8':sorted(census.key_label(k) for k in census.leaves_of(parts) if k[0]=='2' and k[1]==8),
 'ratio':texts[('2',8,'d','i')],'swot':texts[('2',7,'a',None)],
 'cut':[n+1 for n in range(len(doc)) if strip_cut(doc[n])],
 'directives':[d['matchedText'] for d in page_directives(2011,'LC033GLP000EV.pdf',11,page_text(doc[10]),'h')]}))
`], { encoding: 'utf8' }));
    expect(result.q8).toEqual(['Q8(a)', 'Q8(b)', 'Q8(c)(i)', 'Q8(c)(ii)', 'Q8(d)(i)', 'Q8(d)(ii)'].map(q => `Section 2 ${q}`));
    expect(result.ratio).toContain('Calculate the Working Capital Ratio for 2010 and 2009.');
    expect(result.swot).toBe('Explain the term ‘SWOT analysis’. (20)');
    expect(result.cut).toEqual([11]);
    expect(result.directives).toEqual(['two of', 'or', '11 of']);
  });

  it.skipIf(!hasPdfParser)('fails closed for unreviewed directives and stale English or Irish source decisions', () => {
    const output = JSON.parse(execFileSync('python3', ['-c', `
import json,sys
sys.path.insert(0,'scripts/markbank/authoring')
from business_selection import page_directives,apply_reviews,require_reviewed
items=page_directives(2013,'paper.pdf',6,'Choose any two. Roghnaigh dhá cheann. Freagair ceist amháin. A bar chart or a line graph. Barrachairt nó líneghraf.','source-hash')
failures=[]
for callback in [lambda:require_reviewed(items),
    lambda:apply_reviews(items,{'unknown':{}}),
    lambda:apply_reviews(items,{items[0]['id']:{'wording':items[0]['wording'],'paperSha256':'changed'}})]:
    try:callback();failures.append(False)
    except ValueError:failures.append(True)
reviews={item['id']:{'wording':item['wording'],'paperSha256':item['paperSha256'],
    'classification':'open-response','reason':'Test source decision'} for item in items}
apply_reviews(items,reviews)
require_reviewed(items)
print(json.dumps({'matches':[item['matchedText'] for item in items],'failures':failures}))
`], { encoding: 'utf8' }));
    expect(output).toEqual({ matches: ['Choose', 'any two', 'Roghnaigh', 'dhá cheann', 'Freagair', 'or', 'nó'],
      failures: [true, true, true] });
  });

  it.skipIf(!hasPdfParser)('retains printed parts after question numbers, quotations and separate source boxes', () => {
    const rows = JSON.parse(execFileSync('python3', ['-c', `
import json,sys,tempfile
from pathlib import Path
sys.path.insert(0,'scripts/markbank/authoring')
import paper_census as census
sources=[(2014,'000'),(2023,'032'),(2023,'041'),(2025,'032'),(2025,'041')]
expected={2014:[('2','ABQ','b',None)],2023:[('1',1,'a',None),('1',1,'b',None)],
    2025:[('3',2,'b',None),('3',3,'c',None),('3',4,'b',None),('3',7,'c',None)]}
with tempfile.TemporaryDirectory() as cache:
    for year,component in sources:
        Path(cache,f'{year}-hl-{component}-paper.pdf').symlink_to(
            Path(f'paper-trail-corpus/exampapers/{year}/LC033ALP{component}EV.pdf').resolve())
    census.PP.papers_dir=lambda subject:cache
    rows=[]
    for year,wanted in expected.items():
        parts,texts,_=census.census_sections('business',year,'hl')
        rows.append({'year':year,'missing':[list(key) for key in wanted if key not in parts],
            'empty':[list(key) for key in wanted if not texts.get(key,'').strip()]})
print(json.dumps(rows))
`], { encoding: 'utf8' }));
    expect(rows).toEqual([2014, 2023, 2025].map(year => ({ year, missing: [], empty: [] })));
  });

  it.skipIf(!hasPdfParser)('recognises the capitalised ABQ heading before the separate question page', () => {
    const rows = JSON.parse(execFileSync('python3', ['-c', `
import json,sys,tempfile
from pathlib import Path
sys.path.insert(0,'scripts/markbank/authoring')
import paper_census as census
results=[]
with tempfile.TemporaryDirectory() as cache:
    for year in [2018,2019]:
        source=Path(f'paper-trail-corpus/exampapers/{year}/LC033ALP000EV.pdf').resolve()
        Path(cache,f'{year}-hl-000-paper.pdf').symlink_to(source)
    census.PP.papers_dir=lambda subject: cache
    for year in [2018,2019]:
        parts,_,_=census.census_sections('business',year,'hl')
        leaves=census.leaves_of(parts)
        results.append({'year':year,'abq':sorted(census.key_label(k) for k in leaves if k[1]=='ABQ'),
            'misfiledNumberedQuestions':[list(k) for k in leaves if k[0]=='2' and isinstance(k[1],int)],
            'sectionThreeStarts':any(k[0]=='3' and k[1]==1 for k in leaves)})
print(json.dumps(results))
`], { encoding: 'utf8' }));
    expect(rows).toEqual([
      { year: 2018, abq: ['Section 2 ABQ(a)(i)', 'Section 2 ABQ(a)(ii)',
        'Section 2 ABQ(b)(i)', 'Section 2 ABQ(b)(ii)', 'Section 2 ABQ(c)'],
        misfiledNumberedQuestions: [], sectionThreeStarts: true },
      { year: 2019, abq: ['Section 2 ABQ(a)(i)', 'Section 2 ABQ(a)(ii)',
        'Section 2 ABQ(b)', 'Section 2 ABQ(c)'],
        misfiledNumberedQuestions: [], sectionThreeStarts: true },
    ]);
  });

  it('retains every pre-existing authored card ID', () => {
    const runtimeIds = new Set(cards.map(card => card.id));
    expect(runtimeIds.size).toBe(cards.length);
    expect(authored.filter(card => !runtimeIds.has(card.id)).map(card => card.id)).toEqual([]);
  });

  it('keeps 2013 short-question topics separate from repeated long-question numbers', () => {
    const nodes = (n: string) => outgoing(examTopicIdsForQuestion('business', 'higher', 2013, 'main', n, 'single')
      .flatMap(topic => curriculumNodeIdsForExamTopic(topic)));
    expect(nodes('1')).toEqual(['business-5-14']);
    expect(nodes('S3Q1')).toEqual(['business-0-12', 'business-0-13', 'business-0-14']);
    expect(nodes('3')).toEqual(['business-3-19']);
    expect(nodes('S3Q3')).toEqual(['business-6-13', 'business-6-14']);
    const expected = {
      '1': [10], '2': [4, 6], '3': [7, 3], '4': [10], '5': [10],
      '6': [10], '7': [10], '8': [10], '9': [10], '10': [10],
    };
    const short = businessRubrics.filter(card => card.year === 2013 && card.section === '1');
    expect(short).toHaveLength(12);
    expect(short.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(100);
    for (const [q, marks] of Object.entries(expected)) {
      const cohort = short.filter(card => card.questionRef.match(/ Q(\d+)/)?.[1] === q);
      expect(cohort.map(card => card.totalMarks)).toEqual(marks);
      for (const card of cohort) expect(nodes(q), card.id).toContain(card.topicId);
    }
    expect(short.find(card => card.id === 'bus-2013-hl-s1-q3b')?.questionText).toContain('0.5 : 1');
  });

  it('retains shared correct-answer tariffs for the five-row short exercises', () => {
    for (const q of [4, 8]) {
      const card = businessRubrics.find(item => item.id === `bus-2013-hl-s1-q${q}`)!;
      if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
      const allocation = card.rubric.responses[0].allocations[0];
      expect(card.rubric.responses).toHaveLength(1);
      expect(allocation.permittedMarks).toEqual([0, 3, 6, 8, 9, 10]);
      for (const marks of allocation.permittedMarks) {
        expect(businessMarks(card, { [businessScoreId('response-1', 'correct')]: marks })).toBe(marks);
      }
    }
    const inventory = JSON.parse(readFileSync('scripts/markbank/authored/business-corpus-inventory.json', 'utf8'));
    const paper = inventory.documents.find((document: { year: number; level: string; language: string }) =>
      document.year === 2013 && document.level === 'higher' && document.language === 'ev');
    expect(paper.selectionDirectives.every((directive: { reviewStatus: string }) =>
      directive.reviewStatus === 'reviewed')).toBe(true);
    expect(paper.taskBoundaryReview).toBe('complete-paper-and-scheme-review');
    expect(paper.paperTrailQuestionIds).toEqual([
      '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'ABQ',
      'S3Q1', 'S3Q2', 'S3Q3', 'S3Q4', 'S3Q5', 'S3Q6', 'S3Q7',
    ]);
    const irish = inventory.documents.find((document: { year: number; level: string; language: string }) =>
      document.year === 2013 && document.level === 'higher' && document.language === 'iv');
    expect(irish.taskBoundaryReview).toBe('not-yet-complete');
  });

  it('attaches the visually inspected case study to all existing Higher ABQ cards', () => {
    const originals = authored.filter(card => card.level === 'higher' && card.section === '2');
    expect(originals).toHaveLength(5);
    for (const original of originals) {
      const card = HIGHER.find(item => item.id === original.id)!;
      expect(card.sourceMaterial?.pages, card.id).toEqual([2]);
      expect(card.sourceMaterial?.kind, card.id).toBe('source-text');
      expect(card.paperFileid, card.id).toBe('LC033ALP041EV');
    }
  });

  it('preserves the five existing ABQ IDs and tariffs while correcting their rubric and topic', () => {
    const expected = {
      'bus-2021-hl-s2-abq-a': 'business-2-13',
      'bus-2021-hl-s2-abq-b-i': 'business-3-17',
      'bus-2022-hl-s2-abq-b': 'business-4-18',
      'bus-2024-hl-s2-abq-a': 'business-1-5',
      'bus-2024-hl-s2-abq-c': 'business-2-11',
    };
    for (const [id, topic] of Object.entries(expected)) {
      const card = reviewed.find(item => item.id === id)!;
      const original = authored.find(item => item.id === id)!;
      expect(card.topicId).toBe(topic);
      expect(card.totalMarks).toBe(original.totalMarks);
      expect(card.rubric.system).toBe('business');
      expect(supplement.cards.find(item => item.id === id)).toMatchObject({
        correction: { originalQuestionText: original.questionText, originalTotalMarks: original.totalMarks },
      });
    }
  });

  it.each([
    [2010, [['A(i)', 5], ['A(ii)', 15], ['B', 30], ['C', 30]]],
    [2011, [['A(i)', 6], ['A(ii)', 14], ['B', 30], ['C(i)', 6], ['C(ii)', 24]]],
    [2012, [['A', 20], ['B', 30], ['C', 30]]],
    [2013, [['A', 30], ['B', 20], ['C', 30]]],
    [2014, [['A', 20], ['B', 30], ['C', 30]]],
    [2015, [['A', 20], ['B(i)', 6], ['B(ii)', 24], ['C', 30]]],
    [2016, [['A', 30], ['B(i)', 24], ['B(ii)', 6], ['C(i)', 10], ['C(ii)', 10]]],
    [2017, [['A', 20], ['B', 30], ['C(i)', 10], ['C(ii)', 20]]],
    [2018, [['A(i)', 10], ['A(ii)', 10], ['B(i)', 6], ['B(ii)', 24], ['C', 30]]],
    [2019, [['A(i)', 6], ['A(ii)', 14], ['B', 30], ['C', 30]]],
    [2020, [['A', 20], ['B(i)', 24], ['B(ii)', 6], ['C', 30]]],
    [2021, [['A', 30], ['B(i)', 18], ['B(ii)', 12], ['C', 20]]],
    [2022, [['A', 30], ['B', 20], ['C(i)', 27], ['C(ii)', 3]]],
    [2023, [['A', 20], ['B', 30], ['C', 30]]],
    [2024, [['A', 20], ['B(i)', 6], ['B(ii)', 24], ['C', 30]]],
  ] as const)('pins the independently reviewed %i task boundaries', (year, boundaries) => {
    const cohort = reviewed.filter(card => card.year === year);
    expect(cohort.map(card => [card.questionRef.replace(`${year} HL Section 2 ABQ`, '')
      .replace(/^\(([A-C])\)/, '$1'), card.totalMarks])).toEqual(boundaries);
    expect(cohort.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(80);
  });

  it('pins the independently reviewed 2025 ABQ task boundaries to 20 + 28 + 2 + 30', () => {
    const cohort = reviewed.filter(card => card.year === 2025);
    expect(cohort.map(card => [card.questionRef, card.totalMarks])).toEqual([
      ['2025 HL Section 2 ABQ(A)', 20],
      ['2025 HL Section 2 ABQ(B)(i)', 28],
      ['2025 HL Section 2 ABQ(B)(ii)', 2],
      ['2025 HL Section 2 ABQ(C)', 30],
    ]);
    expect(cohort.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(80);
  });

  it('pins the independently reviewed 2026 ABQ task boundaries to 20 + 6 + 24 + 24 + 6', () => {
    const cohort = reviewed.filter(card => card.year === 2026);
    expect(cohort.map(card => [card.questionRef, card.totalMarks])).toEqual([
      ['2026 HL Section 2 ABQ(A)', 20],
      ['2026 HL Section 2 ABQ(B)(i)', 6],
      ['2026 HL Section 2 ABQ(B)(ii)', 24],
      ['2026 HL Section 2 ABQ(C)(i)', 24],
      ['2026 HL Section 2 ABQ(C)(ii)', 6],
    ]);
    expect(cohort.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(80);
    const rewards = cohort[0];
    if (rewards.rubric.system !== 'business') throw new Error('Wrong rubric');
    expect(rewards.rubric.responses.map(response =>
      response.allocations.map(allocation => allocation.maxMarks))).toEqual([[8, 2, 5], [2, 1, 2]]);
    expect(cohort[2].questionText).toContain('other pricing strategies');
    expect(cohort[2].rubric.system === 'business' && cohort[2].rubric.taskRequirements[0])
      .toContain('other than price discrimination');
  });

  it('binds every reviewed task to the inspected source hashes and reconciled tariff', () => {
    // Reviews cover both levels; an Ordinary review's cards live in the Ordinary deck.
    const bothLevels = cards.filter(isRubricCard).filter(card => card.rubric.system === 'business');
    expect(bothLevels.every(tariffReconciles)).toBe(true);
    for (const review of supplement.reviews) {
      expect(review.selectionAnalysis).toContain('open examples');
      for (const [kind, source] of Object.entries(review.sources)) {
        const bytes = readFileSync(`paper-trail-corpus/${kind}/${review.year}/${source.fileid}`);
        expect(createHash('sha256').update(bytes).digest('hex')).toBe(source.sha256);
      }
      const cohort = 'cardIds' in review
        ? bothLevels.filter(card => review.cardIds!.includes(card.id))
        : reviewed.filter(card => card.year === review.year);
      expect(cohort).toHaveLength(Object.keys(review.boundaries).length);
      for (const card of cohort) {
        expect(card.sourceMaterial?.pages).toEqual(review.paperPagesReviewed);
        if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
        expect(card.rubric.schemePages.every(page => review.schemePagesReviewed.includes(page))).toBe(true);
      }
    }
  });

  it('retains each 2013 Q1 route at 60 marks and the complete 60-mark Q2', () => {
    const questionOne = businessRubrics.filter(card => card.id.startsWith('bus-2013-hl-s3-q1')
      && !card.id.startsWith('bus-2013-hl-s3-q1b'));
    expect(questionOne.map(card => card.totalMarks)).toEqual([6, 14, 20]);
    for (const route of businessRubrics.filter(card => card.id.startsWith('bus-2013-hl-s3-q1b'))) {
      expect(questionOne.reduce((sum, card) => sum + card.totalMarks, route.totalMarks)).toBe(60);
    }
    const questionTwo = businessRubrics.filter(card => card.id.startsWith('bus-2013-hl-s3-q2'));
    expect(questionTwo.map(card => card.totalMarks)).toEqual([20, 20, 20]);
    for (const card of [...questionOne, ...questionTwo]) {
      expect(tariffReconciles(card)).toBe(true);
      const q = card.id.includes('-q1') ? 1 : 2;
      expect(examTopicIdsForQuestion('business', 'higher', 2013, 'main', `S3Q${q}`, 'single')
        .flatMap(topic => curriculumNodeIdsForExamTopic(topic))).toContain(card.topicId);
    }
    expect(questionOne[1].questionText).toContain('Data Protection Acts 1988 and 2003');
  });

  it.each([
    [3, [10, 6, 4, 20, 20], 7],
    [4, [6, 14, 20, 20], 8],
    [5, [20, 20, 10, 10], 8],
    [6, [20, 20, 20], 9],
    [7, [20, 6, 14, 20], 9],
  ] as const)('preserves every published boundary and source in 2013 Section 3 Q%i', (q, marks, page) => {
    const cohort = businessRubrics.filter(card => card.id.startsWith(`bus-2013-hl-s3-q${q}`));
    expect(cohort.map(card => card.totalMarks)).toEqual(marks);
    expect(cohort.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(60);
    const topics = examTopicIdsForQuestion('business', 'higher', 2013, 'main', `S3Q${q}`, 'single')
      .flatMap(topic => curriculumNodeIdsForExamTopic(topic));
    for (const card of cohort) {
      expect(tariffReconciles(card), card.id).toBe(true);
      expect(card.sourceMaterial?.pages, card.id).toEqual([page]);
      expect(topics, card.id).toContain(card.topicId);
    }
  });

  it('uses the historical tax table without adding the non-cash benefit to take-home pay', () => {
    const card = businessRubrics.find(item => item.id === 'bus-2013-hl-s3-q5a')!;
    if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
    const allocations = card.rubric.responses.flatMap(response => response.allocations);
    expect(allocations.filter(item => item.maxMarks === 1)).toHaveLength(14);
    expect(allocations.filter(item => item.maxMarks === 2)).toHaveLength(3);
    expect(allocations.filter(item => item.label.includes('(own figure)'))).toHaveLength(5);
    expect(allocations.every(item => item.permittedMarks.join(',') === `0,${item.maxMarks}`)).toBe(true);
    expect(card.rubric.guidance.join(' ')).toContain('€78,000 − €30,410.80 = €47,589.20');
    expect(allocations.at(-1)?.label).toContain('€3,965.77');
    expect(card.rubric.schemePages).toEqual([9, 32]);
  });

  it('keeps all four expansion headings together without inventing short/long-term mark splits', () => {
    const card = businessRubrics.find(item => item.id === 'bus-2013-hl-s3-q6c')!;
    if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
    expect(card.rubric.responses.map(response => response.label)).toEqual([
      'Organisation Structure', 'Product mix', 'Profitability', 'Employment',
    ]);
    expect(card.rubric.responses.map(response => response.allocations.map(item => item.maxMarks)))
      .toEqual([[4, 1], [4, 1], [4, 1], [4, 1]]);
    expect(card.rubric.guidance[0]).toContain('does not label');
  });

  it('keeps the 2012 shared medium-term allowance in one task without doubling its marks', () => {
    const finance = reviewed.find(card => card.id === 'bus-2012-hl-s2-abq-a')!;
    if (finance.rubric.system !== 'business') throw new Error('Wrong rubric');
    expect(finance.totalMarks).toBe(20);
    expect(finance.rubric.responses.map(response => response.allocations.reduce(
      (sum, allocation) => sum + allocation.maxMarks, 0))).toEqual([7, 6, 7]);
    expect(finance.rubric.taskRequirements.join(' ')).toContain('only once');
    expect(reviewed.some(card => /^bus-2012-hl-s2-abq-a-/.test(card.id))).toBe(false);
  });

  it('uses the published all-or-nothing decision marks', () => {
    for (const [year, suffix, marks] of [[2015, 'a', 2], [2016, 'a', 3], [2019, 'c', 3]] as const) {
      const card = reviewed.find(item => item.id === `bus-${year}-hl-s2-abq-${suffix}`)!;
      if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
      const decision = card.rubric.responses[0].allocations[0];
      expect(decision.permittedMarks).toEqual([0, marks]);
      expect(businessMarks(card, { [businessScoreId('response-1', 'decision')]: marks - 1 })).toBe(0);
      expect(businessMarks(card, { [businessScoreId('response-1', 'decision')]: marks })).toBe(marks);
    }
  });

  it('keeps the same parts under their canonical topics in Topic Atlas', () => {
    const references = examQuestionPartReferencesForSubject('business')
      .filter(reference => reference.year === 2025 && reference.level === 'higher'
        && reference.sitting === 'main' && reference.n === 'ABQ');
    for (const [suffix, part] of [['a', 'a'], ['b-i', 'b'], ['b-ii', 'b'], ['c', 'c']]) {
      const card = reviewed.find(item => item.id === `bus-2025-hl-s2-abq-${suffix}`)!;
      const topics = references.filter(reference => reference.subdivision?.endsWith(`Part (${part})`))
        .flatMap(reference => curriculumNodeIdsForExamTopic(reference.topicId));
      expect(topics, card.questionRef).toContain(card.topicId);
    }
  });

  it('files every reviewed case study under each assessed canonical topic in Topic Atlas', () => {
    for (const card of reviewed) {
      const topics = examTopicIdsForQuestion('business', 'higher', card.year, 'main', 'ABQ', card.year < 2020 ? 'single' : 'p2')
        .flatMap(topic => curriculumNodeIdsForExamTopic(topic));
      expect(topics, card.questionRef).toContain(card.topicId);
    }
    expect(examTopicIdsForQuestion('business', 'higher', 2024, 'main', 'ABQ', 'p2'))
      .toContain('business-higher-old-course-abq-units-1-2-3');
    expect(examTopicIdsForQuestion('business', 'higher', 2024, 'main', 'ABQ', 'p2'))
      .not.toContain('business-higher-old-course-abq-units-5-6-7');
  });
});

describe('Business 2026 Higher full paper', () => {
  const y2026 = businessRubrics.filter(card => card.year === 2026 && card.section !== '2');
  const qOf = (card: { questionRef: string }) => card.questionRef.match(/ Q(\d+)/)![1];
  const find = (id: string) => {
    const card = businessRubrics.find(item => item.id === id)!;
    if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
    return card as typeof card & { rubric: Extract<typeof card.rubric, { system: 'business' }> };
  };

  it('preserves every 2026 short-question boundary and the cumulative answer keys', () => {
    const cohort = y2026.filter(card => card.section === '1');
    const expected = { '1': [10], '2': [10], '3': [10], '4': [5, 5], '5': [10], '6': [6, 4], '7': [10],
      '8': [10], '9': [10], '10': [4, 3, 3], '11': [10], '12': [10] };
    expect(cohort).toHaveLength(16);
    expect(cohort.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(120);
    for (const [q, marks] of Object.entries(expected)) {
      expect(cohort.filter(card => qOf(card) === q).map(card => card.totalMarks)).toEqual(marks);
    }
    for (const [q, key] of [[2, 'Single European Market'], [5, '1. True 2. False 3. True 4. True 5. False'],
      [7, '(iv) Statutory'], [9, '1 C; 2 D; 3 E; 4 A; 5 F']] as const) {
      const card = find(`bus-2026-hl-s1-q${q}`);
      expect(card.rubric.responses[0].allocations[0].permittedMarks).toEqual([0, 3, 5, 7, 9, 10]);
      expect(card.rubric.guidance.join(' ')).toContain(key);
    }
    for (const part of ['i', 'ii', 'iii']) {
      const card = find(`bus-2026-hl-s1-q10${part}`);
      for (const value of ['50,000 units', '€ 20', '€ 300,000', '€ 10']) expect(card.questionText).toContain(value);
      expect(card.sourceMaterial?.pages).toEqual([7]);
      expect(card.rubric.responses[0].allocations.every(allocation => allocation.maxMarks === 1)).toBe(true);
    }
    expect(find('bus-2026-hl-s1-q11').rubric.responses.map(r => r.label)).toEqual(['Organic growth', 'Inorganic growth']);
  });

  it.each([
    [1, [15, 5, 20, 20]], [2, [20, 20, 6, 14]], [3, [5, 15, 6, 14, 20]], [4, [12, 8, 10, 10, 20]],
    [5, [6, 14, 20, 20]], [6, [20, 20, 20]], [7, [20, 4, 4, 5, 7, 20]], [8, [20, 6, 14, 20]],
  ] as const)('preserves 2026 Section 3 Q%i boundaries at 60 marks', (q, marks) => {
    const cohort = y2026.filter(card => card.section === '3' && qOf(card) === String(q));
    expect(cohort.map(card => card.totalMarks)).toEqual(marks);
    expect(cohort.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(60);
    for (const card of cohort) {
      expect(tariffReconciles(card)).toBe(true);
      expect(card.paperFileid).toBe('LC033ALP041EV');
    }
  });

  it('keeps required headings whole and the separately published evaluation allowances', () => {
    expect(find('bus-2026-hl-s3-q1b').rubric.responses.map(r => r.label)).toEqual([
      'Business and a competitor: co-operative', 'Business and a competitor: competitive',
      'Government and a business: co-operative', 'Government and a business: competitive']);
    expect(find('bus-2026-hl-s3-q4b-ii').rubric.responses.map(r => r.label)).toEqual(['Customers', 'Investors']);
    for (const id of ['bus-2026-hl-s3-q1c', 'bus-2026-hl-s3-q4c', 'bus-2026-hl-s3-q5c', 'bus-2026-hl-s3-q8b-ii']) {
      const evaluation = find(id).rubric.responses.at(-1)!;
      expect(evaluation.label, id).toBe('Evaluation');
      expect(evaluation.allocations[0].maxMarks, id).toBe(2);
    }
    const eu = find('bus-2026-hl-s3-q3c');
    expect(eu.rubric.responses[0].allocations[0].permittedMarks).toEqual([0, 2]);
    expect(eu.rubric.responses.slice(1).map(r => r.allocations.map(a => a.maxMarks))).toEqual([[3, 3], [3, 3], [3, 3]]);
    const plc = find('bus-2026-hl-s3-q7a');
    expect(plc.rubric.responses[0].allocations.reduce((sum, a) => sum + a.maxMarks, 0)).toBe(10);
    expect(plc.rubric.responses.slice(1).map(r => r.allocations[0].maxMarks)).toEqual([2, 2, 2, 2, 2]);
  });

  it('gives every ratio card the full Swift Ltd table and the analysis its industry averages', () => {
    for (const [part, marks] of [['i', 4], ['ii', 4], ['iii', 5], ['iv', 7]] as const) {
      const card = find(`bus-2026-hl-s3-q7b-${part}`);
      expect(card.totalMarks).toBe(marks);
      for (const value of ['€ 450,000', '€ 33,750', '€ 174,375', '€ 93,750', '€ 250,000', '€ 350,000', '€ 75,000']) {
        expect(card.questionText).toContain(value);
      }
    }
    expect(find('bus-2026-hl-s3-q7b-iv').rubric.responses[0].allocations.find(a => a.id === 'loan')!.maxMarks).toBe(2);
    const analysis = find('bus-2026-hl-s3-q7c');
    for (const value of ['Current ratio 2.1 : 1', 'Return on investment 8%', 'current ratio 1.86 : 1', 'return on investment 5%']) {
      expect(analysis.questionText).toContain(value);
    }
  });

  it('files both 2026 booklets under booklet-specific Topic Atlas identities', () => {
    for (const card of y2026) {
      const nodes = examTopicIdsForQuestion('business', 'higher', 2026, 'main', qOf(card), card.section === '1' ? 'p1' : 'p2')
        .flatMap(curriculumNodeIdsForExamTopic);
      for (const topic of [card.topicId, ...(card.additionalTopicIds ?? [])]) {
        expect(nodes, card.id).toContain(topic);
        expect(cardsForTopic(topic, businessRubrics)).toContain(card);
      }
    }
    const abq = examTopicIdsForQuestion('business', 'higher', 2026, 'main', 'ABQ', 'p2');
    expect(new Set(outgoing(abq.flatMap(curriculumNodeIdsForExamTopic))))
      .toEqual(new Set(['business-4-19', 'business-3-20', 'business-4-17', 'business-2-13']));
    // The redeveloped-course crosswalk is not part of this review and survives it.
    expect(abq).toContain('business-higher-new-course-24-the-target-market');
    expect(examTopicIdsForQuestion('business', 'higher', 2026, 'main', '1', 'p1'))
      .toContain('business-higher-new-course-25-operations-and-finance');
  });
});

describe('Business 2025 Higher full paper', () => {
  const y2025 = businessRubrics.filter(card => card.year === 2025 && card.section !== '2');
  const qOf = (card: { questionRef: string }) => card.questionRef.match(/ Q(\d+)/)![1];
  const legacyChart = ['c1', 'c2', 'ci', 'cii', 'ciii'].map(part => `bus-2025-hl-s3-q8${part}`);
  const find = (id: string) => {
    const card = businessRubrics.find(item => item.id === id)!;
    if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
    return card as typeof card & { rubric: Extract<typeof card.rubric, { system: 'business' }> };
  };

  it('keeps every 2025 legacy ID and total while recording its verified correction', () => {
    const legacy = authored.filter(card => card.year === 2025 && card.level === 'higher' && card.section !== '2');
    expect(legacy).toHaveLength(52);
    for (const original of legacy) {
      const card = find(original.id);
      expect(card.totalMarks, original.id).toBe(original.totalMarks);
      expect(card.questionRef, original.id).toBe(original.questionRef);
      expect(supplement.cards.find(item => item.id === original.id), original.id).toMatchObject({
        correction: { originalQuestionText: original.questionText, originalTotalMarks: original.totalMarks },
      });
    }
    expect(HIGHER.filter(card => card.year === 2025 && card.section !== '2').every(isRubricCard)).toBe(true);
    expect(y2025.map(card => card.id).filter(id => !legacy.some(item => item.id === id))).toEqual(['bus-2025-hl-s3-q8c']);
  });

  it('preserves every 2025 short-question boundary and the cumulative answer keys', () => {
    const cohort = y2025.filter(card => card.section === '1');
    const expected = { '1': [10], '2': [6, 4], '3': [10], '4': [10], '5': [10], '6': [10], '7': [5, 5],
      '8': [10], '9': [5, 5], '10': [10], '11': [6, 4], '12': [10] };
    expect(cohort.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(120);
    for (const [q, marks] of Object.entries(expected)) {
      expect(cohort.filter(card => qOf(card) === q).map(card => card.totalMarks)).toEqual(marks);
    }
    for (const [q, key] of [[1, '1 D; 2 E; 3 A; 4 C; 5 F'], [3, 'ICTU = Irish Congress of Trade Unions'], [4, '(v) Less']] as const) {
      const card = find(`bus-2025-hl-s1-q${q}`);
      expect(card.rubric.responses[0].allocations[0].permittedMarks).toEqual([0, 3, 5, 7, 9, 10]);
      expect(card.rubric.guidance.join(' ')).toContain(key);
    }
    expect(find('bus-2025-hl-s1-q7b').rubric.responses[0].allocations.map(a => a.maxMarks)).toEqual([1, 1, 1, 1, 1]);
    expect(find('bus-2025-hl-s1-q7b').questionText).toContain('Authorised Share Capital €900,000');
  });

  it.each([
    [1, [20, 20, 12, 8]], [2, [20, 20, 20]], [3, [14, 6, 20, 20]], [4, [20, 20, 6, 14]],
    [5, [20, 20, 10, 10]], [6, [20, 20, 10, 6, 2, 2]], [7, [20, 20, 20]], [8, [6, 14, 15, 25]],
  ] as const)('preserves 2025 Section 3 Q%i boundaries at 60 marks', (q, marks) => {
    const cohort = y2025.filter(card => card.section === '3' && qOf(card) === String(q) && !legacyChart.includes(card.id));
    expect(cohort.map(card => card.totalMarks)).toEqual(marks);
    expect(cohort.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(60);
    for (const card of cohort) expect(tariffReconciles(card)).toBe(true);
  });

  it('adds the complete break-even chart and labels the five legacy component cards', () => {
    const chart = find('bus-2025-hl-s3-q8c');
    expect(chart.rubric.responses.map(r => r.allocations.map(a => a.maxMarks))).toEqual([[2, 1, 1, 3, 3, 3], [4, 4, 4]]);
    expect(chart.rubric.taskRequirements.join(' ')).toContain('at most 12');
    expect(legacyChart.map(id => find(id).totalMarks)).toEqual([4, 9, 4, 4, 4]);
    for (const id of legacyChart.slice(0, 2)) expect(find(id).rubric.taskRequirements[0]).toContain('Practise the complete chart on the Q8(C) card');
    for (const id of legacyChart.slice(2)) expect(find(id).rubric.guidance[0]).toContain('Calculation route');
  });

  it('keeps required pairs whole and unequal splits unattached to named items', () => {
    expect(find('bus-2025-hl-s3-q2b').rubric.responses.map(r => r.label))
      .toEqual(['Benefit 1', 'Benefit 2', 'Challenge 1', 'Challenge 2']);
    expect(find('bus-2025-hl-s3-q7a').rubric.responses.map(r => r.label))
      .toEqual(['Advantage 1', 'Advantage 2', 'Disadvantage 1', 'Disadvantage 2']);
    expect(find('bus-2025-hl-s3-q4cii').rubric.responses.map(r => r.label)).toEqual(['Two suppliers', 'Two employees']);
    for (const id of ['bus-2025-hl-s3-q1a', 'bus-2025-hl-s3-q2a', 'bus-2025-hl-s3-q3c', 'bus-2025-hl-s3-q4a']) {
      expect(find(id).rubric.responses.map(r => r.allocations.map(a => a.maxMarks)), id).toEqual([[4, 1], [4, 1], [3, 2], [3, 2]]);
    }
    expect(find('bus-2025-hl-s3-q1cii').rubric.responses[0].allocations[0].permittedMarks).toEqual([0, 3, 6, 7, 8]);
    expect(find('bus-2025-hl-s3-q6ci').rubric.responses[0].allocations.reduce((sum, a) => sum + a.maxMarks, 0)).toBe(10);
    expect(find('bus-2025-hl-s3-q6civ').questionText).toContain('PAYE 17,325');
  });

  it('corrects the two employment-law topics and files both booklets in Topic Atlas', () => {
    expect(find('bus-2025-hl-s3-q1ci').topicId).toBe('business-0-14');
    expect(find('bus-2025-hl-s3-q4b').topicId).toBe('business-0-14');
    for (const card of y2025) {
      const nodes = examTopicIdsForQuestion('business', 'higher', 2025, 'main', qOf(card), card.section === '1' ? 'p1' : 'p2')
        .flatMap(curriculumNodeIdsForExamTopic);
      for (const topic of [card.topicId, ...(card.additionalTopicIds ?? [])]) {
        expect(nodes, card.id).toContain(topic);
        expect(cardsForTopic(topic, businessRubrics)).toContain(card);
      }
    }
  });
});

describe('Business 2024 Higher full paper', () => {
  const y2024 = businessRubrics.filter(card => card.year === 2024 && card.section !== '2');
  const qOf = (card: { questionRef: string }) => card.questionRef.match(/ Q(\d+)/)![1];
  const find = (id: string) => {
    const card = businessRubrics.find(item => item.id === id)!;
    if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
    return card as typeof card & { rubric: Extract<typeof card.rubric, { system: 'business' }> };
  };
  // Every 2024 Higher printed choice is marked alike under one topic, so each is one card.
  const pools = {} as Record<string, readonly (readonly string[])[]>;

  it('keeps every 2024 legacy ID and total, each printed choice one card', () => {
    const legacy = authored.filter(card => card.year === 2024 && card.level === 'higher' && card.section !== '2');
    expect(legacy).toHaveLength(57);
    for (const original of legacy) {
      const card = find(original.id);
      expect(card.totalMarks, original.id).toBe(original.totalMarks);
      expect(card.questionRef, original.id).toBe(original.questionRef);
    }
    const legacyIds = new Set(legacy.map(card => card.id));
    expect(y2024.map(card => card.id).filter(id => !legacyIds.has(id)).sort()).toEqual([
      'bus-2024-hl-s1-q9i',
    ]);
  });

  it('preserves every 2024 boundary at 10 marks per short question and 60 per long question', () => {
    const short = y2024.filter(card => card.section === '1');
    const expected = { '1': [10], '2': [10], '3': [4, 6], '4': [10], '5': [10], '6': [10], '7': [10],
      '8': [10], '9': [6, 4], '10': [10], '11': [10], '12': [4, 6] };
    for (const [q, marks] of Object.entries(expected)) {
      expect(short.filter(card => qOf(card) === q).map(card => card.totalMarks), q).toEqual(marks);
    }
    const routed = new Set(Object.keys(pools).flatMap(id => expandBusinessRoutePools(
      [routePools.pools.find(item => item.id === id)!]).map(route => route.id)));
    for (let q = 1; q <= 8; q++) {
      const base = y2024.filter(card => card.section === '3' && qOf(card) === String(q) && !routed.has(card.id));
      const pool = Object.keys(pools).find(id => id.includes(`-q${q}`));
      expect(base.reduce((sum, card) => sum + card.totalMarks, 0) + (pool ? find(pool).totalMarks : 0), String(q)).toBe(60);
    }
  });

  it('keeps the 2024 calculation sources and published mark steps', () => {
    const comp = find('bus-2024-hl-s1-q9i');
    for (const value of ['€300,000', '€250,000', '€60,000']) expect(comp.questionText).toContain(value);
    expect(comp.rubric.responses[0].allocations.map(a => a.maxMarks)).toEqual([1, 1, 2, 2]);
    const trade = find('bus-2024-hl-s3-q3aii');
    for (const value of ['€72bn', '€34bn', '€93bn', '€84bn']) expect(trade.questionText).toContain(value);
    expect(trade.rubric.responses.map(r => r.allocations.length)).toEqual([6, 8]);
    expect(find('bus-2024-hl-s3-q6aii').rubric.responses[0].allocations[0].permittedMarks).toEqual([0, 3, 5, 7]);
    expect(find('bus-2024-hl-s3-q6aiii').questionText).toContain('Closing Cash 26,000 (17,000) (28,000) (28,000)');
    expect(find('bus-2024-hl-s1-q12ii').rubric.responses[0].allocations[0].permittedMarks).toEqual([0, 2, 4, 5, 6]);
    expect(find('bus-2024-hl-s3-q4c').rubric.responses.at(-1)!.allocations.map(a => a.maxMarks)).toEqual([2, 2]);
  });

  it('files both 2024 booklets, every route and every corrected topic in Topic Atlas', () => {
    expect(find('bus-2024-hl-s1-q4').topicId).toBe('business-3-19');
    expect(find('bus-2024-hl-s1-q12ii').topicId).toBe('business-3-20');
    expect(find('bus-2024-hl-s3-q1ci').topicId).toBe('business-0-14');
    for (const card of y2024) {
      const nodes = examTopicIdsForQuestion('business', 'higher', 2024, 'main', qOf(card), card.section === '1' ? 'p1' : 'p2')
        .flatMap(curriculumNodeIdsForExamTopic);
      for (const topic of [card.topicId, ...(card.additionalTopicIds ?? [])]) {
        expect(nodes, card.id).toContain(topic);
        expect(cardsForTopic(topic, businessRubrics)).toContain(card);
      }
    }
  });
});

describe('Business 2023 Higher full paper', () => {
  const y2023 = businessRubrics.filter(card => card.year === 2023 && card.section !== '2');
  const qOf = (card: { questionRef: string }) => card.questionRef.match(/ Q(\d+)/)![1];
  const components = ['bus-2023-hl-s1-q5a', 'bus-2023-hl-s3-q8c1', 'bus-2023-hl-s3-q8c2', 'bus-2023-hl-s3-q8c3'];
  const find = (id: string) => {
    const card = businessRubrics.find(item => item.id === id)!;
    if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
    return card as typeof card & { rubric: Extract<typeof card.rubric, { system: 'business' }> };
  };

  it('keeps every 2023 legacy ID and total while recording its verified correction', () => {
    const legacy = authored.filter(card => card.year === 2023 && card.level === 'higher' && card.section !== '2');
    expect(legacy).toHaveLength(57);
    for (const original of legacy) {
      const card = find(original.id);
      expect(card.totalMarks, original.id).toBe(original.totalMarks);
      expect(supplement.cards.find(item => item.id === original.id), original.id).toMatchObject({
        correction: { originalQuestionText: original.questionText, originalTotalMarks: original.totalMarks },
      });
    }
    expect(y2023.map(card => card.id).filter(id => !legacy.some(item => item.id === id)).sort())
      .toEqual(['bus-2023-hl-s1-q5a-diagram', 'bus-2023-hl-s3-q8c']);
  });

  it('preserves every 2023 boundary at 10 marks per short question and 60 per long question', () => {
    for (let q = 1; q <= 12; q++) {
      const cohort = y2023.filter(card => card.section === '1' && qOf(card) === String(q) && !components.includes(card.id));
      expect(cohort.reduce((sum, card) => sum + card.totalMarks, 0), String(q)).toBe(10);
    }
    for (let q = 1; q <= 8; q++) {
      const cohort = y2023.filter(card => card.section === '3' && qOf(card) === String(q) && !components.includes(card.id));
      expect(cohort.reduce((sum, card) => sum + card.totalMarks, 0), String(q)).toBe(60);
      for (const card of cohort) expect(tariffReconciles(card)).toBe(true);
    }
  });

  it('keeps the 2023 calculation sources, keys and restricted mark steps', () => {
    const trade = find('bus-2023-hl-s1-q3b');
    for (const value of ['Visible Exports €70bn', 'Invisible Imports €40bn', 'Total Exports €100bn', 'Total Imports €90bn']) expect(trade.questionText).toContain(value);
    expect(trade.rubric.responses[0].allocations.map(a => a.maxMarks)).toEqual([2, 1, 1, 1, 1]);
    expect(find('bus-2023-hl-s1-q4').rubric.guidance.join(' ')).toContain('1 D; 2 E; 3 A; 4 C; 5 F');
    expect(find('bus-2023-hl-s1-q9').rubric.guidance.join(' ')).toContain('1 False; 2 True; 3 True; 4 False; 5 True');
    expect(find('bus-2023-hl-s3-q3b').rubric.responses.at(-1)!.allocations[0].permittedMarks).toEqual([0, 1, 3]);
    expect(find('bus-2023-hl-s3-q7bi').rubric.responses[0].allocations.reduce((sum, a) => sum + a.maxMarks, 0)).toBe(10);
    expect(find('bus-2023-hl-s3-q7biv').questionText).toContain('PAYE €32,355');
    expect(find('bus-2023-hl-s3-q5a').rubric.responses.map(r => r.label))
      .toEqual(['Physical needs', 'Safety needs', 'Social needs', 'Esteem needs', 'Self-actualisation']);
  });

  it('adds the complete diagram and chart cards and labels the legacy components', () => {
    expect(find('bus-2023-hl-s1-q5a-diagram').rubric.responses[0].allocations.map(a => a.maxMarks)).toEqual([2, 2, 2]);
    expect(find('bus-2023-hl-s1-q5a').rubric.taskRequirements[0]).toContain('Practise the complete diagram');
    const chart = find('bus-2023-hl-s3-q8c');
    expect(chart.rubric.responses.map(r => r.allocations.map(a => a.maxMarks))).toEqual([[1, 1, 1, 2, 4, 4], [4, 4, 4]]);
    expect(components.slice(1).map(id => find(id).totalMarks)).toEqual([12, 4, 20]);
    for (const id of components.slice(1)) expect(find(id).rubric.taskRequirements[0]).toContain('Q8(C) card');
    for (const id of ['bus-2023-hl-s3-q1ai', 'bus-2023-hl-s3-q1aii']) {
      expect(find(id).questionText).toContain('one example of a co-operative relationship and one example of a competitive relationship');
      expect(find(id).rubric.responses.map(r => r.allocations.reduce((sum, a) => sum + a.maxMarks, 0))).toEqual([2, 4, 4]);
    }
  });

  it('files both 2023 booklets in Topic Atlas', () => {
    for (const card of y2023) {
      const nodes = examTopicIdsForQuestion('business', 'higher', 2023, 'main', qOf(card), card.section === '1' ? 'p1' : 'p2')
        .flatMap(curriculumNodeIdsForExamTopic);
      for (const topic of [card.topicId, ...(card.additionalTopicIds ?? [])]) {
        expect(nodes, card.id).toContain(topic);
        expect(cardsForTopic(topic, businessRubrics)).toContain(card);
      }
    }
  });
});

describe('Business 2022 Higher full paper', () => {
  const y2022 = businessRubrics.filter(card => card.year === 2022 && card.section !== '2');
  const qOf = (card: { questionRef: string }) => card.questionRef.match(/ Q(\d+)/)![1];
  const find = (id: string) => {
    const card = businessRubrics.find(item => item.id === id)!;
    if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
    return card as typeof card & { rubric: Extract<typeof card.rubric, { system: 'business' }> };
  };
  // Every 2022 Higher printed choice is marked alike under one topic, so each is one card.
  const pools = {} as Record<string, readonly (readonly string[])[]>;

  it('keeps every 2022 legacy ID and total, each printed choice one card', () => {
    const legacy = authored.filter(card => card.year === 2022 && card.level === 'higher' && card.section !== '2');
    expect(legacy).toHaveLength(51);
    for (const original of legacy) {
      const card = find(original.id);
      expect(card.totalMarks, original.id).toBe(original.totalMarks);
      expect(card.questionRef, original.id).toBe(original.questionRef);
    }
    const legacyIds = new Set(legacy.map(card => card.id));
    expect(y2022.map(card => card.id).filter(id => !legacyIds.has(id))).toEqual([]);
  });

  it('preserves every 2022 boundary at 10 marks per short question and 60 per long question', () => {
    for (let q = 1; q <= 12; q++) {
      expect(y2022.filter(card => card.section === '1' && qOf(card) === String(q))
        .reduce((sum, card) => sum + card.totalMarks, 0), String(q)).toBe(10);
    }
    const routed = new Set(Object.keys(pools).flatMap(id => expandBusinessRoutePools(
      [routePools.pools.find(item => item.id === id)!]).map(route => route.id)));
    for (let q = 1; q <= 8; q++) {
      const base = y2022.filter(card => card.section === '3' && qOf(card) === String(q) && !routed.has(card.id));
      const pool = Object.keys(pools).find(id => id.includes(`-q${q}`));
      expect(base.reduce((sum, card) => sum + card.totalMarks, 0) + (pool ? 20 : 0), String(q)).toBe(60);
    }
  });

  it('keeps the 2022 data, answer keys and restricted mark steps', () => {
    expect(find('bus-2022-hl-s1-q1').rubric.guidance.join(' ')).toContain('1 E; 2 A; 3 D; 4 B; 5 F');
    expect(find('bus-2022-hl-s1-q7').rubric.guidance.join(' ')).toContain('1 False; 2 False; 3 False; 4 False; 5 True');
    expect(find('bus-2022-hl-s1-q9').rubric.responses[0].allocations.map(a => a.maxMarks)).toEqual([3, 3, 2, 2]);
    expect(find('bus-2022-hl-s1-q12').rubric.responses[1].allocations[0].permittedMarks).toEqual([0, 2, 4]);
    expect(find('bus-2022-hl-s1-q12').questionText).toContain('Kellie has a salary of €42,600.');
    expect(find('bus-2022-hl-s3-q1cii').rubric.responses[0].allocations[0].permittedMarks).toEqual([0, 3, 6, 8, 10, 12]);
    const ratio = find('bus-2022-hl-s3-q7aii');
    expect(ratio.questionText).toContain('Retained Earnings €140,000 €120,000');
    expect(ratio.rubric.responses.map(r => r.allocations.reduce((sum, a) => sum + a.maxMarks, 0))).toEqual([3, 6, 6]);
    expect(find('bus-2022-hl-s3-q5b').rubric.responses.map(r => r.label)).toEqual(['Stock control', 'Quality control']);
  });

  it('files both 2022 booklets, every route and every corrected topic in Topic Atlas', () => {
    expect(find('bus-2022-hl-s3-q1ci').topicId).toBe('business-0-14');
    expect(find('bus-2022-hl-s3-q3bi').topicId).toBe('business-5-13');
    for (const card of y2022) {
      const nodes = examTopicIdsForQuestion('business', 'higher', 2022, 'main', qOf(card), card.section === '1' ? 'p1' : 'p2')
        .flatMap(curriculumNodeIdsForExamTopic);
      for (const topic of [card.topicId, ...(card.additionalTopicIds ?? [])]) {
        expect(nodes, card.id).toContain(topic);
        expect(cardsForTopic(topic, businessRubrics)).toContain(card);
      }
    }
  });
});

describe('Business 2021 Higher full paper', () => {
  const y2021 = businessRubrics.filter(card => card.year === 2021 && card.section !== '2');
  const qOf = (card: { questionRef: string }) => card.questionRef.match(/ Q(\d+)/)![1];
  const indicators = ['bi', 'bii', 'biii'].map(part => `bus-2021-hl-s3-q7${part}`);
  const find = (id: string) => {
    const card = businessRubrics.find(item => item.id === id)!;
    if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
    return card as typeof card & { rubric: Extract<typeof card.rubric, { system: 'business' }> };
  };

  it('keeps every 2021 legacy ID and total, the EU-policy choice as one card', () => {
    const legacy = authored.filter(card => card.year === 2021 && card.level === 'higher' && card.section !== '2');
    expect(legacy).toHaveLength(50);
    for (const original of legacy) {
      const card = find(original.id);
      expect(card.totalMarks, original.id).toBe(original.totalMarks);
      expect(card.questionRef, original.id).toBe(original.questionRef);
    }
    const legacyIds = new Set(legacy.map(card => card.id));
    expect(y2021.map(card => card.id).filter(id => !legacyIds.has(id)).sort()).toEqual([
      'bus-2021-hl-s3-q6cii', 'bus-2021-hl-s3-q7b',
    ]);
  });

  it('preserves every 2021 boundary at 10 marks per short question and 60 per long question', () => {
    for (let q = 1; q <= 12; q++) {
      expect(y2021.filter(card => card.section === '1' && qOf(card) === String(q))
        .reduce((sum, card) => sum + card.totalMarks, 0), String(q)).toBe(10);
    }
    for (let q = 1; q <= 8; q++) {
      const base = y2021.filter(card => card.section === '3' && qOf(card) === String(q) && !indicators.includes(card.id));
      expect(base.reduce((sum, card) => sum + card.totalMarks, 0), String(q)).toBe(60);
    }
  });

  it('keeps the 2021 data, keys, new chart and reward cards', () => {
    expect(find('bus-2021-hl-s1-q1').rubric.guidance.join(' ')).toContain('1 D; 2 F; 3 A; 4 E; 5 B');
    expect(find('bus-2021-hl-s1-q5').rubric.responses[0].allocations.map(a => a.permittedMarks)).toEqual([[0, 3], [0, 3], [0, 2], [0, 2]]);
    expect(find('bus-2021-hl-s1-q8i').rubric.responses[0].allocations.map(a => a.maxMarks)).toEqual([1, 1, 1, 1, 1, 1]);
    expect(find('bus-2021-hl-s1-q8ii').questionText).toContain('12.5%');
    expect(find('bus-2021-hl-s3-q7b').rubric.responses.map(r => r.allocations.map(a => a.maxMarks))).toEqual([[1, 1, 1, 2, 4, 4], [4, 4, 4]]);
    for (const id of indicators) expect(find(id).rubric.taskRequirements[0]).toContain('Practise the complete 25-mark chart');
    expect(find('bus-2021-hl-s3-q6cii').totalMarks).toBe(7);
    expect(find('bus-2021-hl-s3-q6ci').rubric.responses.map(r => r.label)).toEqual(['Commission', 'Employee Share Purchase Plan', 'Flexitime']);
    expect(find('bus-2021-hl-s3-q2cii').rubric.responses.map(r => r.label)).toEqual(['Economic benefit', 'Social benefit']);
  });

  it('files both 2021 booklets, every route and every corrected topic in Topic Atlas', () => {
    expect(find('bus-2021-hl-s3-q1c').topicId).toBe('business-0-14');
    expect(find('bus-2021-hl-s3-q6ai').topicId).toBe('business-3-20');
    for (const card of y2021) {
      const nodes = examTopicIdsForQuestion('business', 'higher', 2021, 'main', qOf(card), card.section === '1' ? 'p1' : 'p2')
        .flatMap(curriculumNodeIdsForExamTopic);
      for (const topic of [card.topicId, ...(card.additionalTopicIds ?? [])]) {
        expect(nodes, card.id).toContain(topic);
        expect(cardsForTopic(topic, businessRubrics)).toContain(card);
      }
    }
  });
});

describe('Business 2010 Higher full paper outside the ABQ', () => {
  const higherRubrics = HIGHER.filter(isRubricCard).filter(card => card.rubric.system === 'business');
  const y2010 = higherRubrics.filter(card => card.year === 2010 && card.section !== '2');
  const qOf = (card: { questionRef: string }) => card.questionRef.match(/ Q(\d+)/)![1];
  const find = (id: string) => {
    const card = higherRubrics.find(item => item.id === id)!;
    if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
    return card as typeof card & { rubric: Extract<typeof card.rubric, { system: 'business' }> };
  };
  const maxes = (id: string) => find(id).rubric.responses.map(r => r.allocations.map(a => a.maxMarks));

  it('adds Sections 1 and 3 of the single-booklet 2010 Higher paper beside its ABQ, with no earlier card and no route', () => {
    expect(authored.filter(card => card.year === 2010 && card.level === 'higher')).toHaveLength(0);
    expect(y2010).toHaveLength(48);
    expect(higherRubrics.filter(card => card.year === 2010 && card.section === '2')).toHaveLength(4);
    expect(routePools.pools.some(pool => pool.template.year === 2010 && pool.template.level === 'higher')).toBe(false);
    for (const card of y2010) {
      expect(card.paperFileid, card.id).toBe('LC033ALP000EV');
      expect(tariffReconciles(card), card.id).toBe(true);
      expect(card.questionText, card.id).not.toContain('Outline two benefits to “Marie’s Pizzas”');
    }
  });

  it('preserves every Section 1 question at 10 marks and every Section 3 question at 60', () => {
    for (let q = 1; q <= 10; q++) expect(y2010.filter(card => card.section === '1' && qOf(card) === String(q)).reduce((sum, card) => sum + card.totalMarks, 0), String(q)).toBe(10);
    for (let q = 1; q <= 7; q++) expect(y2010.filter(card => card.section === '3' && qOf(card) === String(q)).reduce((sum, card) => sum + card.totalMarks, 0), String(q)).toBe(60);
    expect(find('bus-2010-hl-s1-q4').rubric.guidance.join(' ')).toContain('1 F; 2 A; 3 D; 4 C; 5 B');
    expect(['bus-2010-hl-s1-q6i', 'bus-2010-hl-s1-q6ii', 'bus-2010-hl-s1-q6iii'].map(id => find(id).totalMarks)).toEqual([4, 3, 3]);
    expect(maxes('bus-2010-hl-s1-q10a')).toEqual([[1, 1, 1, 1, 1, 1, 1]]);
  });

  it('keeps the published Section 3 splits, the one-card ombudsman part and the one-card policy choice', () => {
    expect(['b-i', 'b-ii', 'b-iii', 'b-iv'].map(s => find(`bus-2010-hl-s3-q5${s}`).totalMarks)).toEqual([5, 5, 5, 5]);
    expect(['c-i', 'c-ii', 'c-iii'].map(s => find(`bus-2010-hl-s3-q5${s}`).totalMarks)).toEqual([6, 8, 6]);
    expect(find('bus-2010-hl-s3-q5c-ii').questionText).toContain('Debt Equity Ratio | 0.4:1');
    expect(maxes('bus-2010-hl-s3-q1b')).toEqual([[4, 3], [4, 3], [3, 3]]);
    expect(maxes('bus-2010-hl-s3-q4a-ii')).toEqual([[2], [2, 1], [2, 1], [2, 1], [2, 1]]);
    const choice = find('bus-2010-hl-s3-q3c');
    for (const item of ['Competition Policy', 'Common Fisheries Policy (CFP)', 'Common Agricultural Policy (CAP)']) {
      expect(choice.questionText, item).toContain(item);
      expect(choice.rubric.guidance.filter(line => line.startsWith(`${item} (scheme PDF page `)), item).toHaveLength(1);
    }
  });

  it('files the 2010 Higher booklet in Topic Atlas with single-booklet identities', () => {
    for (const card of y2010) {
      const n = card.section === '1' ? qOf(card) : `S3Q${qOf(card)}`;
      const nodes = examTopicIdsForQuestion('business', 'higher', 2010, 'main', n, 'single').flatMap(curriculumNodeIdsForExamTopic);
      for (const topic of [card.topicId, ...(card.additionalTopicIds ?? [])]) {
        expect(nodes, card.id).toContain(topic);
        expect(cardsForTopic(topic, higherRubrics), card.id).toContain(card);
      }
    }
  });
});

describe('Business 2011 Higher full paper outside the ABQ', () => {
  const higherRubrics = HIGHER.filter(isRubricCard).filter(card => card.rubric.system === 'business');
  const y2011 = higherRubrics.filter(card => card.year === 2011 && card.section !== '2');
  const qOf = (card: { questionRef: string }) => card.questionRef.match(/ Q(\d+)/)![1];
  const find = (id: string) => {
    const card = higherRubrics.find(item => item.id === id)!;
    if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
    return card as typeof card & { rubric: Extract<typeof card.rubric, { system: 'business' }> };
  };
  const maxes = (id: string) => find(id).rubric.responses.map(r => r.allocations.map(a => a.maxMarks));

  it('adds Sections 1 and 3 of the single-booklet 2011 Higher paper beside its ABQ, with no earlier card and no route', () => {
    expect(authored.filter(card => card.year === 2011 && card.level === 'higher')).toHaveLength(0);
    expect(y2011).toHaveLength(45);
    expect(higherRubrics.filter(card => card.year === 2011 && card.section === '2')).toHaveLength(5);
    expect(routePools.pools.some(pool => pool.template.year === 2011 && pool.template.level === 'higher')).toBe(false);
    for (const card of y2011) {
      expect(card.paperFileid, card.id).toBe('LC033ALP000EV');
      expect(tariffReconciles(card), card.id).toBe(true);
    }
  });

  it('preserves every Section 1 question at 10 marks and every Section 3 question at 60', () => {
    for (let q = 1; q <= 10; q++) expect(y2011.filter(card => card.section === '1' && qOf(card) === String(q)).reduce((sum, card) => sum + card.totalMarks, 0), String(q)).toBe(10);
    for (let q = 1; q <= 7; q++) expect(y2011.filter(card => card.section === '3' && qOf(card) === String(q)).reduce((sum, card) => sum + card.totalMarks, 0), String(q)).toBe(60);
    expect(find('bus-2011-hl-s1-q8').rubric.guidance.join(' ')).toContain('1 True; 2 False; 3 True; 4 True; 5 False');
    expect(maxes('bus-2011-hl-s1-q2b')).toEqual([[1, 1, 1, 1, 1, 1]]);
    expect(find('bus-2011-hl-s1-q5b').rubric.responses.map(r => r.label)).toEqual(['Balance of Trade', 'Balance of Payments']);
    expect(maxes('bus-2011-hl-s1-q5b')).toEqual([[1, 1, 1], [1, 1, 1]]);
  });

  it('keeps the published Section 3 splits, the underlined taxes and the chart items', () => {
    for (const [id, total] of [['bus-2011-hl-s3-q1b-i', 20], ['bus-2011-hl-s3-q1b-ii', 10], ['bus-2011-hl-s3-q2c-i', 8], ['bus-2011-hl-s3-q2c-ii', 12],
      ['bus-2011-hl-s3-q4b-i', 10], ['bus-2011-hl-s3-q4b-ii', 10], ['bus-2011-hl-s3-q5b-i', 18], ['bus-2011-hl-s3-q5b-ii', 7], ['bus-2011-hl-s3-q5c-i', 8],
      ['bus-2011-hl-s3-q5c-ii', 12], ['bus-2011-hl-s3-q6a-i', 10], ['bus-2011-hl-s3-q6a-ii', 15], ['bus-2011-hl-s3-q7b-i', 10], ['bus-2011-hl-s3-q7b-ii', 15],
      ['bus-2011-hl-s3-q7c-i', 20], ['bus-2011-hl-s3-q7c-ii', 5]] as const) expect(find(id).totalMarks, id).toBe(total);
    expect(find('bus-2011-hl-s3-q5b-i').rubric.responses.map(r => r.label)).toEqual(['PAYE', 'VAT', 'Corporation Tax']);
    expect(maxes('bus-2011-hl-s3-q7c-i')).toEqual([[2, 2, 2, 3, 3, 3, 2, 2, 1]]);
    expect(maxes('bus-2011-hl-s3-q7b-i')).toEqual([[1, 1, 1, 1, 1, 1, 1, 1], [2]]);
    expect(find('bus-2011-hl-s3-q4c').rubric.responses.map(r => r.label)).toEqual(['Stock control', 'Quality control']);
  });

  it('files the 2011 Higher booklet in Topic Atlas with single-booklet identities', () => {
    for (const card of y2011) {
      const n = card.section === '1' ? qOf(card) : `S3Q${qOf(card)}`;
      const nodes = examTopicIdsForQuestion('business', 'higher', 2011, 'main', n, 'single').flatMap(curriculumNodeIdsForExamTopic);
      for (const topic of [card.topicId, ...(card.additionalTopicIds ?? [])]) {
        expect(nodes, card.id).toContain(topic);
        expect(cardsForTopic(topic, higherRubrics), card.id).toContain(card);
      }
    }
  });
});

describe('Business 2012 Higher full paper outside the ABQ', () => {
  const higherRubrics = HIGHER.filter(isRubricCard).filter(card => card.rubric.system === 'business');
  const y2012 = higherRubrics.filter(card => card.year === 2012 && card.section !== '2');
  const qOf = (card: { questionRef: string }) => card.questionRef.match(/ Q(\d+)/)![1];
  const find = (id: string) => {
    const card = higherRubrics.find(item => item.id === id)!;
    if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
    return card as typeof card & { rubric: Extract<typeof card.rubric, { system: 'business' }> };
  };
  const maxes = (id: string) => find(id).rubric.responses.map(r => r.allocations.map(a => a.maxMarks));

  it('adds Sections 1 and 3 of the single-booklet 2012 Higher paper beside its ABQ, with no earlier card and no route', () => {
    expect(authored.filter(card => card.year === 2012 && card.level === 'higher')).toHaveLength(0);
    expect(y2012).toHaveLength(37);
    expect(higherRubrics.filter(card => card.year === 2012 && card.section === '2').map(card => card.id))
      .toEqual(['bus-2012-hl-s2-abq-a', 'bus-2012-hl-s2-abq-b', 'bus-2012-hl-s2-abq-c']);
    expect(routePools.pools.some(pool => pool.template.year === 2012 && pool.template.level === 'higher')).toBe(false);
    for (const card of y2012) {
      expect(card.paperFileid, card.id).toBe('LC033ALP000EV');
      expect(card.rubric.schemeFileid, card.id).toBe('LC033ALP000EV');
      expect(tariffReconciles(card), card.id).toBe(true);
    }
  });

  it('preserves every Section 1 question at 10 marks and every Section 3 question at 60', () => {
    for (let q = 1; q <= 10; q++) expect(y2012.filter(card => card.section === '1' && qOf(card) === String(q)).reduce((sum, card) => sum + card.totalMarks, 0), String(q)).toBe(10);
    for (let q = 1; q <= 7; q++) expect(y2012.filter(card => card.section === '3' && qOf(card) === String(q)).reduce((sum, card) => sum + card.totalMarks, 0), String(q)).toBe(60);
    expect(find('bus-2012-hl-s1-q2').rubric.guidance.join(' ')).toContain('1 D; 2 A; 3 E; 4 C; 5 F');
    expect(find('bus-2012-hl-s1-q6').rubric.responses[0].allocations[0].permittedMarks).toEqual([0, 3, 6, 8, 9, 10]);
    expect(['bus-2012-hl-s1-q10i', 'bus-2012-hl-s1-q10ii', 'bus-2012-hl-s1-q10iii'].map(id => find(id).totalMarks)).toEqual([6, 2, 2]);
    expect(find('bus-2012-hl-s1-q10i').rubric.guidance.join(' ')).toContain('Units: 10,000');
  });

  it('keeps the published Section 3 splits, headings and calculation marks', () => {
    for (const [id, total] of [['bus-2012-hl-s3-q2c-i', 5], ['bus-2012-hl-s3-q2c-ii', 10], ['bus-2012-hl-s3-q5b-i', 20], ['bus-2012-hl-s3-q5b-ii', 20],
      ['bus-2012-hl-s3-q6c-i', 6], ['bus-2012-hl-s3-q6c-ii', 14]] as const) expect(find(id).totalMarks, id).toBe(total);
    expect(find('bus-2012-hl-s3-q2a').rubric.responses.map(r => r.label)).toEqual(['Formation', 'Liability', 'Finance', 'Control']);
    expect(maxes('bus-2012-hl-s3-q2a')).toEqual([[2, 3, 2], [2, 2, 2], [2, 2, 2], [2, 2, 2]]);
    expect(maxes('bus-2012-hl-s3-q5a')).toEqual([[1, 2, 1, 1, 1, 1, 1], [2, 2, 2, 2], [1, 1, 1, 1]]);
    const ratios = find('bus-2012-hl-s3-q5b-i');
    expect(maxes('bus-2012-hl-s3-q5b-i')).toEqual([[1, 5], [1, 3], [1, 4], [1, 4]]);
    for (const response of ratios.rubric.responses) expect(response.allocations[0].permittedMarks).toEqual([0, 1]);
    expect(ratios.questionText).toContain('Closing Stock | 80,000');
    expect(find('bus-2012-hl-s3-q6b').rubric.responses.map(r => r.label)).toEqual(['Idea Generation', 'Feasibility Study']);
  });

  it('files the 2012 Higher booklet in Topic Atlas with single-booklet identities', () => {
    for (const card of y2012) {
      const n = card.section === '1' ? qOf(card) : `S3Q${qOf(card)}`;
      const nodes = examTopicIdsForQuestion('business', 'higher', 2012, 'main', n, 'single').flatMap(curriculumNodeIdsForExamTopic);
      for (const topic of [card.topicId, ...(card.additionalTopicIds ?? [])]) {
        expect(nodes, card.id).toContain(topic);
        expect(cardsForTopic(topic, higherRubrics), card.id).toContain(card);
      }
    }
  });
});

describe('Business 2026 Ordinary full paper', () => {
  const ordinaryRubrics = ORDINARY.filter(isRubricCard).filter(card => card.rubric.system === 'business');
  const y2026 = ordinaryRubrics.filter(card => card.year === 2026);
  const qOf = (card: { questionRef: string }) => card.questionRef.match(/ Q(\d+)/)![1];
  const find = (id: string) => {
    const card = ordinaryRubrics.find(item => item.id === id)!;
    if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
    return card as typeof card & { rubric: Extract<typeof card.rubric, { system: 'business' }> };
  };
  // The 2026 Ordinary chart choice and Q8(B) are each one card.
  const pools = {} as Record<string, readonly (readonly string[])[]>;
  const routed = new Set(expandBusinessRoutePools(routePools.pools.filter(pool => pool.id in pools)).map(route => route.id));

  it('adds the 2026 Ordinary paper with no earlier card to preserve', () => {
    expect(authored.filter(card => card.year === 2026 && card.level === 'ordinary')).toHaveLength(0);
    expect(y2026.every(card => card.id.startsWith('bus-2026-ol-'))).toBe(true);
    expect(y2026.filter(card => !routed.has(card.id))).toHaveLength(74);
    for (const card of y2026) {
      expect(card.paperFileid, card.id).toBe(card.section === '1' ? 'LC033GLP032EV' : 'LC033GLP033EV');
      expect(card.rubric.schemeFileid, card.id).toBe('LC033GLP000EV');
      expect(tariffReconciles(card), card.id).toBe(true);
    }
  });

  it('preserves every Section 1 boundary at 10 marks and the published answer-count sequences', () => {
    const cohort = y2026.filter(card => card.section === '1');
    expect(cohort).toHaveLength(16);
    for (let q = 1; q <= 15; q++) {
      expect(cohort.filter(card => qOf(card) === String(q)).map(card => card.totalMarks), String(q))
        .toEqual(q === 13 ? [5, 5] : [10]);
    }
    for (const [q, steps, key] of [
      [2, [0, 3, 6, 8, 10], 'True; False; False; True'], [3, [0, 4, 7, 10], 'Price; Place; Promotion'],
      [5, [0, 3, 6, 8, 10], '(i) Invisible Export; (ii) Visible Export; (iii) Visible Import; (iv) Invisible Import'],
      [10, [0, 3, 6, 8, 10], 'PAYE Direct'], [12, [0, 3, 6, 8, 10], '(i) inflation; (ii) decrease'],
      [15, [0, 2, 4, 6, 8, 10], '1 E; 2 F; 3 D; 4 B; 5 C'],
    ] as const) {
      const card = find(`bus-2026-ol-s1-q${q}`);
      expect(card.rubric.responses[0].allocations[0].permittedMarks, String(q)).toEqual(steps);
      expect(card.rubric.guidance.join(' '), String(q)).toContain(key);
    }
    const acid = find('bus-2026-ol-s1-q14');
    for (const value of ['€110,000', '€42,000', '€136,000']) expect(acid.questionText).toContain(value);
    expect(acid.rubric.responses[0].allocations.map(a => a.maxMarks)).toEqual([3, 3, 4]);
    expect(find('bus-2026-ol-s1-q13i').questionText).toContain('Identify the stage above, labelled stage 5');
  });

  it.each([1, 2, 3, 4, 5, 6, 7, 8, 9])('preserves 2026 Ordinary Section 2 Q%i at 75 marks', q => {
    const base = y2026.filter(card => card.section === '2' && qOf(card) === String(q) && !routed.has(card.id));
    const pooled = 0;
    expect(base.reduce((sum, card) => sum + card.totalMarks, 0) + pooled).toBe(75);
  });

  it('keeps the unequal two-point tariff unattached and the published calculation steps', () => {
    for (const id of ['bus-2026-ol-s2-q1b', 'bus-2026-ol-s2-q4b', 'bus-2026-ol-s2-q9a']) {
      expect(find(id).rubric.responses.map(r => r.allocations.map(a => a.maxMarks)), id).toEqual([[7, 3], [4, 1]]);
    }
    const pay = find('bus-2026-ol-s2-q7c');
    expect(pay.rubric.responses[0].allocations.map(a => a.maxMarks)).toEqual([4, 2, 2, 3, 4]);
    expect(pay.rubric.guidance.join(' ')).toContain('€645 + €800 = €1,445');
    expect(find('bus-2026-ol-s2-q5a').rubric.responses[0].allocations[0].permittedMarks).toEqual([0, 6, 9, 11, 13, 15]);
    expect(find('bus-2026-ol-s2-q8c').rubric.responses[0].allocations[0].permittedMarks).toEqual([0, 10, 14, 15]);
    expect(find('bus-2026-ol-s2-q3ci').rubric.responses.map(r => r.allocations[0].maxMarks)).toEqual([7, 2]);
    expect(find('bus-2026-ol-s2-q6di').rubric.guidance.join(' ')).toContain('March');
    for (const value of ['10,000', '14,000', '(4,000)']) expect(find('bus-2026-ol-s2-q6di').questionText).toContain(value);
  });

  it('files both 2026 Ordinary booklets and every route in Topic Atlas', () => {
    for (const card of y2026) {
      const nodes = examTopicIdsForQuestion('business', 'ordinary', 2026, 'main', qOf(card), card.section === '1' ? 'p1' : 'p2')
        .flatMap(curriculumNodeIdsForExamTopic);
      for (const topic of [card.topicId, ...(card.additionalTopicIds ?? [])]) {
        expect(nodes, card.id).toContain(topic);
        expect(cardsForTopic(topic, ordinaryRubrics), card.id).toContain(card);
      }
    }
  });
});

describe('Business 2025 Ordinary full paper', () => {
  const ordinaryRubrics = ORDINARY.filter(isRubricCard).filter(card => card.rubric.system === 'business');
  const y2025 = ordinaryRubrics.filter(card => card.year === 2025);
  const qOf = (card: { questionRef: string }) => card.questionRef.match(/ Q(\d+)/)![1];
  const find = (id: string) => {
    const card = ordinaryRubrics.find(item => item.id === id)!;
    if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
    return card as typeof card & { rubric: Extract<typeof card.rubric, { system: 'business' }> };
  };
  // Every 2025 Ordinary printed choice is one card.
  const pools = {} as Record<string, readonly (readonly string[])[]>;
  const routed = new Set(expandBusinessRoutePools(routePools.pools.filter(pool => pool.id in pools)).map(route => route.id));

  it('keeps every 2025 Ordinary legacy ID and total, each printed choice one card', () => {
    const legacy = authored.filter(card => card.year === 2025 && card.level === 'ordinary');
    expect(legacy).toHaveLength(64);
    for (const original of legacy) {
      const card = find(original.id);
      expect(card.totalMarks, original.id).toBe(original.totalMarks);
      expect(card.questionRef, original.id).toBe(original.questionRef);
      // The generated deck strips correction records; they live in the reviewed source.
      const source = supplement.cards.find(item => item.id === original.id)
        ?? routePools.pools.map(pool => (pool as { legacyRoute?: { id: string } }).legacyRoute).find(route => route?.id === original.id);
      expect(source, original.id).toMatchObject({ correction: { originalQuestionText: original.questionText, originalTotalMarks: original.totalMarks } });
    }
    const legacyIds = new Set(legacy.map(card => card.id));
    expect(y2025.filter(card => !routed.has(card.id) && !legacyIds.has(card.id)).map(card => card.id).sort())
      .toEqual(['bus-2025-ol-s1-q9', 'bus-2025-ol-s2-q8e', 'bus-2025-ol-s2-q9e']);
    expect(y2025.filter(card => !legacyIds.has(card.id))).toHaveLength(3);
  });

  it('preserves every Section 1 boundary at 10 marks with the published keys and row marks', () => {
    const cohort = y2025.filter(card => card.section === '1');
    expect(cohort).toHaveLength(15);
    for (let q = 1; q <= 15; q++) expect(cohort.filter(card => qOf(card) === String(q)).map(card => card.totalMarks), String(q)).toEqual([10]);
    for (const [q, steps, key] of [
      [2, [0, 4, 7, 10], '2. Labour 3. Capital 4. Enterprise'], [3, [0, 3, 6, 8, 10], '(i) False; (ii) True; (iii) True; (iv) False'],
      [4, [0, 3, 6, 8, 10], 'A Break-Even Point (BEP)'], [6, [0, 4, 7, 10], '(i) Mass; (ii) Job; (iii) Batch'],
      [7, [0, 4, 7, 10], '(i) Sponsorship (ii) Sales Promotion (iii) Personal Selling'], [11, [0, 4, 7, 10], '(i) Contingency Plan'],
      [12, [0, 3, 6, 8, 10], '(i) Visa Card; (ii) short term; (iii) last; (iv) bad debt'], [14, [0, 3, 6, 8, 10], '(i) Visible; (ii) Invisible'],
      [15, [0, 2, 4, 6, 8, 10], '1 C; 2 F; 3 A; 4 B; 5 D'],
    ] as const) {
      const card = find(`bus-2025-ol-s1-q${q}`);
      expect(card.rubric.responses[0].allocations[0].permittedMarks, String(q)).toEqual(steps);
      expect(card.rubric.guidance.join(' '), String(q)).toContain(key);
    }
    const matrix = find('bus-2025-ol-s1-q9');
    expect(matrix.rubric.responses.map(r => r.allocations.map(a => a.maxMarks))).toEqual([[2, 2], [1, 1], [4]]);
    expect(matrix.rubric.responses[2].allocations[0].permittedMarks).toEqual([0, 2, 3, 4]);
    const cash = find('bus-2025-ol-s1-q10');
    expect(cash.rubric.responses.map(r => r.allocations.map(a => a.maxMarks))).toEqual([[3], [5], [2]]);
    expect(cash.rubric.responses[1].allocations[0].permittedMarks).toEqual([0, 3, 5]);
    for (const value of ['115,000', '267,000', '98,000']) expect(cash.questionText).toContain(value);
    expect(find('bus-2025-ol-s1-q5').topicId).toBe('business-3-20');
  });

  it.each([1, 2, 3, 4, 5, 6, 7, 8, 9])('preserves 2025 Ordinary Section 2 Q%i at 75 marks', q => {
    const base = y2025.filter(card => card.section === '2' && qOf(card) === String(q) && !routed.has(card.id));
    const pooled = 0;
    expect(base.reduce((sum, card) => sum + card.totalMarks, 0) + pooled).toBe(75);
  });

  it('keeps named splits, the net-salary steps and the new diagram card', () => {
    expect(find('bus-2025-ol-s2-q2a').rubric.responses.map(r => r.label)).toEqual(['Reward', 'Risk']);
    expect(find('bus-2025-ol-s2-q7a').rubric.responses.map(r => r.label)).toEqual(['Induction training', 'On-the-job training']);
    expect(find('bus-2025-ol-s2-q4b').rubric.responses.map(r => r.allocations.map(a => a.maxMarks))).toEqual([[7, 3], [4, 1]]);
    expect(find('bus-2025-ol-s2-q3cii').rubric.responses.map(r => r.allocations.map(a => a.maxMarks))).toEqual([[5, 2], [5, 2]]);
    expect(find('bus-2025-ol-s2-q3di').rubric.responses[0].allocations[0].permittedMarks).toEqual([0, 4, 6, 7]);
    expect(find('bus-2025-ol-s2-q8cii').rubric.responses[0].allocations[0].permittedMarks).toEqual([0, 6, 8]);
    const pay = find('bus-2025-ol-s2-q7e');
    expect(pay.rubric.responses[0].allocations.map(a => a.maxMarks)).toEqual([1, 2, 2, 2, 2, 2, 2, 2]);
    for (const value of ['€46,000', '€3,750', '4.1%', '3.0%']) expect(pay.questionText).toContain(value);
    expect(pay.rubric.guidance.join(' ')).toContain('36,484');
    const agm = find('bus-2025-ol-s2-q6c');
    expect(agm.rubric.responses.map(r => r.allocations.map(a => a.maxMarks))).toEqual([[1, 1, 1, 1], [10], [1]]);
    expect(agm.rubric.responses[1].allocations[0].permittedMarks).toEqual([0, 2, 4, 6, 8, 10]);
    const plc = find('bus-2025-ol-s2-q8e');
    expect(plc.totalMarks).toBe(15);
    expect(plc.rubric.responses[0].allocations.map(a => a.maxMarks)).toEqual([1, 1, 1, 2, 2, 2, 2, 2, 2]);
    expect(find('bus-2025-ol-s2-q9-d').questionText).toContain('public liability insurance');
  });

  it('files both 2025 Ordinary booklets and every route in Topic Atlas', () => {
    expect(find('bus-2025-ol-s2-q9-b').topicId).toBe('business-2-13');
    expect(find('bus-2025-ol-s2-q9-c').topicId).toBe('business-5-15');
    expect(find('bus-2025-ol-s2-q4d').topicId).toBe('business-0-14');
    for (const card of y2025) {
      const nodes = examTopicIdsForQuestion('business', 'ordinary', 2025, 'main', qOf(card), card.section === '1' ? 'p1' : 'p2')
        .flatMap(curriculumNodeIdsForExamTopic);
      for (const topic of [card.topicId, ...(card.additionalTopicIds ?? [])]) {
        expect(nodes, card.id).toContain(topic);
        expect(cardsForTopic(topic, ordinaryRubrics), card.id).toContain(card);
      }
    }
  });
});

describe('Business 2024 Ordinary full paper', () => {
  const ordinaryRubrics = ORDINARY.filter(isRubricCard).filter(card => card.rubric.system === 'business');
  const y2024 = ordinaryRubrics.filter(card => card.year === 2024);
  const qOf = (card: { questionRef: string }) => card.questionRef.match(/ Q(\d+)/)![1];
  const find = (id: string) => {
    const card = ordinaryRubrics.find(item => item.id === id)!;
    if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
    return card as typeof card & { rubric: Extract<typeof card.rubric, { system: 'business' }> };
  };
  // Every 2024 Ordinary printed choice is marked alike, so each is one card.
  const pools = {} as Record<string, readonly (readonly string[])[]>;
  const routed = new Set(expandBusinessRoutePools(routePools.pools.filter(pool => pool.id in pools)).map(route => route.id));

  it('keeps every 2024 Ordinary legacy ID and total, each printed choice one card', () => {
    const legacy = authored.filter(card => card.year === 2024 && card.level === 'ordinary');
    expect(legacy).toHaveLength(69);
    for (const original of legacy) {
      const card = find(original.id);
      expect(card.totalMarks, original.id).toBe(original.totalMarks);
      expect(card.questionRef, original.id).toBe(original.questionRef);
      const source = supplement.cards.find(item => item.id === original.id)
        ?? routePools.pools.map(pool => (pool as { legacyRoute?: { id: string } }).legacyRoute).find(route => route?.id === original.id);
      expect(source, original.id).toMatchObject({ correction: { originalQuestionText: original.questionText, originalTotalMarks: original.totalMarks } });
    }
    const legacyIds = new Set(legacy.map(card => card.id));
    expect(y2024.filter(card => !routed.has(card.id) && !legacyIds.has(card.id)).map(card => card.id)).toEqual(['bus-2024-ol-s2-q9-a-ii', 'bus-2024-ol-s2-q9e']);
    expect(y2024.filter(card => !legacyIds.has(card.id))).toHaveLength(2);
  });

  it('preserves every Section 1 boundary at 10 marks with the published keys and row marks', () => {
    const cohort = y2024.filter(card => card.section === '1');
    expect(cohort).toHaveLength(16);
    for (let q = 1; q <= 15; q++) {
      expect(cohort.filter(card => qOf(card) === String(q)).map(card => card.totalMarks), String(q)).toEqual(q === 6 ? [5, 5] : [10]);
    }
    for (const [q, steps, key] of [
      [3, [0, 3, 6, 8, 10], '(i) departments; (ii) matrix; (iii) wide; (iv) removing'], [4, [0, 3, 6, 8, 10], 'Subway Franchise'],
      [7, [0, 3, 6, 8, 10], 'False; True; True; True'], [9, [0, 4, 7, 10], 'IDA Ireland'], [10, [0, 4, 7, 10], '1. Strengths; 3. Opportunities; 4. Threats'],
      [13, [0, 4, 7, 10], '1. Forming; 2. Storming; 4. Performing'], [15, [0, 2, 4, 6, 8, 10], '1 E; 2 A; 3 F; 4 B; 5 D'],
    ] as const) {
      const card = find(`bus-2024-ol-s1-q${q}`);
      expect(card.rubric.responses[0].allocations[0].permittedMarks, String(q)).toEqual(steps);
      expect(card.rubric.guidance.join(' '), String(q)).toContain(key);
    }
    expect(find('bus-2024-ol-s1-q4').questionText).toContain('Coca Cola purchased over 51% of the shares of Costa Coffee');
    const pay = find('bus-2024-ol-s1-q8');
    expect(pay.rubric.responses[0].allocations.map(a => a.maxMarks)).toEqual([3, 3, 2, 2]);
    expect(pay.rubric.guidance.join(' ')).toContain('€31,290');
    expect(find('bus-2024-ol-s1-q1').rubric.responses.map(r => r.allocations[0].maxMarks)).toEqual([3, 4, 3]);
  });

  it.each([1, 2, 3, 4, 5, 6, 7, 8, 9])('preserves 2024 Ordinary Section 2 Q%i at 75 marks', q => {
    const base = y2024.filter(card => card.section === '2' && qOf(card) === String(q) && !routed.has(card.id));
    const pooled = 0;
    expect(base.reduce((sum, card) => sum + card.totalMarks, 0) + pooled).toBe(75);
  });

  it('keeps named splits, the balance-of-payments and channel steps, and the unattached sequences', () => {
    expect(find('bus-2024-ol-s2-q5a').rubric.responses.map(r => [r.label, r.allocations.map(a => a.maxMarks)])).toEqual([['Risk', [4, 4]], ['Reward', [4, 3]]]);
    expect(find('bus-2024-ol-s2-q5bi').rubric.responses.map(r => r.allocations[0].maxMarks)).toEqual([7, 3]);
    expect(find('bus-2024-ol-s2-q4a').rubric.responses.map(r => r.allocations.map(a => a.maxMarks))).toEqual([[5, 2], [5, 2], [5, 1]]);
    const bop = find('bus-2024-ol-s2-q3ai');
    expect(bop.rubric.responses[0].allocations.map(a => a.maxMarks)).toEqual([3, 3, 4]);
    expect(bop.rubric.responses[0].allocations[2].permittedMarks).toEqual([0, 2, 4]);
    for (const value of ['€89bn', '€33bn', '€83bn', '€85bn']) expect(bop.questionText).toContain(value);
    const channel = find('bus-2024-ol-s2-q8bii');
    expect(channel.rubric.responses[0].allocations.map(a => a.permittedMarks)).toEqual([[0, 3], [0, 3], [0, 2, 4]]);
    expect(find('bus-2024-ol-s2-q1a').rubric.responses[0].allocations[0].permittedMarks).toEqual([0, 2, 4, 6, 8, 10]);
    expect(find('bus-2024-ol-s2-q4d').rubric.responses[0].allocations[0].permittedMarks).toEqual([0, 3, 6, 8, 10]);
    expect(find('bus-2024-ol-s2-q6c').rubric.responses.map(r => r.allocations.map(a => a.label))).toEqual([['Explanation', 'Example'], ['Explanation', 'Example']]);
    expect(find('bus-2024-ol-s2-q8e').rubric.responses.map(r => r.allocations.map(a => a.maxMarks))).toEqual([[4, 4], [4, 3]]);
  });

  it('files both 2024 Ordinary booklets and every route in Topic Atlas', () => {
    expect(find('bus-2024-ol-s2-q4a').topicId).toBe('business-0-14');
    expect(find('bus-2024-ol-s2-q5d').topicId).toBe('business-3-20');
    for (const card of y2024) {
      const nodes = examTopicIdsForQuestion('business', 'ordinary', 2024, 'main', qOf(card), card.section === '1' ? 'p1' : 'p2')
        .flatMap(curriculumNodeIdsForExamTopic);
      for (const topic of [card.topicId, ...(card.additionalTopicIds ?? [])]) {
        expect(nodes, card.id).toContain(topic);
        expect(cardsForTopic(topic, ordinaryRubrics), card.id).toContain(card);
      }
    }
  });
});

describe('Business 2023 Ordinary full paper', () => {
  const ordinaryRubrics = ORDINARY.filter(isRubricCard).filter(card => card.rubric.system === 'business');
  const y2023 = ordinaryRubrics.filter(card => card.year === 2023);
  const qOf = (card: { questionRef: string }) => card.questionRef.match(/ Q(\d+)/)![1];
  const find = (id: string) => {
    const card = ordinaryRubrics.find(item => item.id === id)!;
    if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
    return card as typeof card & { rubric: Extract<typeof card.rubric, { system: 'business' }> };
  };
  // Every 2023 Ordinary printed choice is one card.
  const pools = {} as Record<string, readonly (readonly string[])[]>;
  const routed = new Set(expandBusinessRoutePools(routePools.pools.filter(pool => pool.id in pools)).map(route => route.id));

  it('keeps every 2023 Ordinary legacy ID and total, each printed choice one card', () => {
    const legacy = authored.filter(card => card.year === 2023 && card.level === 'ordinary');
    expect(legacy).toHaveLength(68);
    for (const original of legacy) {
      const card = find(original.id);
      expect(card.totalMarks, original.id).toBe(original.totalMarks);
      expect(card.questionRef, original.id).toBe(original.questionRef);
      const source = supplement.cards.find(item => item.id === original.id)
        ?? routePools.pools.map(pool => (pool as { legacyRoute?: { id: string } }).legacyRoute).find(route => route?.id === original.id);
      expect(source, original.id).toMatchObject({ correction: { originalQuestionText: original.questionText, originalTotalMarks: original.totalMarks } });
    }
    const legacyIds = new Set(legacy.map(card => card.id));
    expect(y2023.filter(card => !routed.has(card.id) && !legacyIds.has(card.id)).map(card => card.id).sort()).toEqual([
      'bus-2023-ol-s1-q11', 'bus-2023-ol-s1-q7', 'bus-2023-ol-s2-q3ai', 'bus-2023-ol-s2-q9-c-i', 'bus-2023-ol-s2-q9-c-ii', 'bus-2023-ol-s2-q9d']);
    expect(y2023.filter(card => !legacyIds.has(card.id))).toHaveLength(6);
  });

  it('preserves every Section 1 boundary at 10 marks with the published keys and row marks', () => {
    const cohort = y2023.filter(card => card.section === '1');
    expect(cohort).toHaveLength(18);
    const split: Record<number, number[]> = { 6: [6, 4], 14: [4, 3, 3] };
    for (let q = 1; q <= 15; q++) expect(cohort.filter(card => qOf(card) === String(q)).map(card => card.totalMarks), String(q)).toEqual(split[q] ?? [10]);
    for (const [q, steps, key] of [
      [2, [0, 3, 6, 8, 10], '(i) Controller; (ii) Facilitator; (iii) Facilitator; (iv) Controller'], [4, [0, 3, 6, 8, 10], '(i) True; (ii) False; (iii) False; (iv) True'],
      [8, [0, 3, 6, 8, 10], '(i) seven; (ii) cost of living; (iii) businesses; (iv) interest group'], [11, [0, 3, 6, 8, 10], 'live and work Social Charter'],
      [12, [0, 4, 7, 10], 'tourism Fáilte Ireland'], [15, [0, 2, 4, 6, 8, 10], '1 C; 2 D; 3 F; 4 A; 5 E'],
    ] as const) {
      const card = find(`bus-2023-ol-s1-q${q}`);
      expect(card.rubric.responses[0].allocations[0].permittedMarks, String(q)).toEqual(steps);
      expect(card.rubric.guidance.join(' '), String(q)).toContain(key);
    }
    const order = find('bus-2023-ol-s1-q7');
    expect(order.rubric.responses.map(r => r.allocations.map(a => a.maxMarks))).toEqual([[3], [5], [2]]);
    expect(order.rubric.responses[1].allocations[0].permittedMarks).toEqual([0, 3, 5]);
    expect(find('bus-2023-ol-s1-q10').rubric.responses[0].allocations.map(a => a.maxMarks)).toEqual([2, 2, 1, 3, 1, 1]);
    expect(find('bus-2023-ol-s1-q1').rubric.responses.map(r => r.allocations[0].maxMarks)).toEqual([3, 3, 4]);
  });

  it.each([1, 2, 3, 4, 5, 6, 7, 8, 9])('preserves 2023 Ordinary Section 2 Q%i at 75 marks', q => {
    const base = y2023.filter(card => card.section === '2' && qOf(card) === String(q) && !routed.has(card.id));
    const pooled = 0;
    expect(base.reduce((sum, card) => sum + card.totalMarks, 0) + pooled).toBe(75);
  });

  it('keeps required named items, the salary lines and the unattached sequences', () => {
    expect(find('bus-2023-ol-s2-q4e').rubric.responses.map(r => r.label)).toEqual(['Secret Ballot', 'Minimum Notice', 'Picketing']);
    expect(find('bus-2023-ol-s2-q6a').rubric.responses.map(r => r.label)).toEqual(['AGM', 'Minutes', 'AOB']);
    expect(find('bus-2023-ol-s2-q7d').rubric.responses.map(r => [r.label, r.allocations.map(a => a.maxMarks)])).toEqual([['Commission', [6, 2]], ['Benefit-in-kind', [5, 2]]]);
    const pay = find('bus-2023-ol-s2-q7a');
    expect(pay.rubric.responses[0].allocations.map(a => a.maxMarks)).toEqual([3, 3, 2, 3, 3, 2, 2, 2]);
    expect(pay.rubric.responses[0].allocations[1].permittedMarks).toEqual([0, 3]);
    expect(find('bus-2023-ol-s2-q9-b').rubric.responses.map(r => r.allocations.map(a => a.maxMarks))).toEqual([[3, 3, 2], [3, 2, 2]]);
    expect(find('bus-2023-ol-s2-q9-c-ii').rubric.responses.map(r => r.allocations.map(a => a.maxMarks))).toEqual([[4, 3], [4, 2]]);
    expect(find('bus-2023-ol-s2-q8c').rubric.responses[0].allocations[0].permittedMarks).toEqual([0, 8, 12, 15]);
    expect(find('bus-2023-ol-s2-q1c').rubric.responses[0].allocations[0].permittedMarks).toEqual([0, 3, 6, 9, 12, 15]);
    expect(find('bus-2023-ol-s2-q4aii').rubric.responses[0].allocations[0].permittedMarks).toEqual([0, 2, 4, 6, 8, 10]);
  });

  it('files both 2023 Ordinary booklets and every route in Topic Atlas', () => {
    expect(find('bus-2023-ol-s2-q1a').topicId).toBe('business-0-14');
    expect(find('bus-2023-ol-s2-q9-b').topicId).toBe('business-4-16');
    for (const card of y2023) {
      const nodes = examTopicIdsForQuestion('business', 'ordinary', 2023, 'main', qOf(card), card.section === '1' ? 'p1' : 'p2')
        .flatMap(curriculumNodeIdsForExamTopic);
      for (const topic of [card.topicId, ...(card.additionalTopicIds ?? [])]) {
        expect(nodes, card.id).toContain(topic);
        expect(cardsForTopic(topic, ordinaryRubrics), card.id).toContain(card);
      }
    }
  });
});

describe('Business 2022 Ordinary full paper', () => {
  const ordinaryRubrics = ORDINARY.filter(isRubricCard).filter(card => card.rubric.system === 'business');
  const y2022 = ordinaryRubrics.filter(card => card.year === 2022);
  const qOf = (card: { questionRef: string }) => card.questionRef.match(/ Q(\d+)/)![1];
  const find = (id: string) => {
    const card = ordinaryRubrics.find(item => item.id === id)!;
    if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
    return card as typeof card & { rubric: Extract<typeof card.rubric, { system: 'business' }> };
  };
  // Both 2022 Ordinary printed choices are marked alike, so each is one card.
  const pools = {} as Record<string, readonly (readonly string[])[]>;
  const routed = new Set(expandBusinessRoutePools(routePools.pools.filter(pool => pool.id in pools)).map(route => route.id));

  it('keeps every 2022 Ordinary legacy ID and total, each printed choice one card', () => {
    const legacy = authored.filter(card => card.year === 2022 && card.level === 'ordinary');
    expect(legacy).toHaveLength(65);
    for (const original of legacy) {
      const card = find(original.id);
      expect(card.totalMarks, original.id).toBe(original.totalMarks);
      expect(card.questionRef, original.id).toBe(original.questionRef);
      const source = supplement.cards.find(item => item.id === original.id)
        ?? routePools.pools.map(pool => (pool as { legacyRoute?: { id: string } }).legacyRoute).find(route => route?.id === original.id);
      expect(source, original.id).toMatchObject({ correction: { originalQuestionText: original.questionText, originalTotalMarks: original.totalMarks } });
    }
    const legacyIds = new Set(legacy.map(card => card.id));
    expect(y2022.filter(card => !routed.has(card.id) && !legacyIds.has(card.id)).map(card => card.id).sort()).toEqual([
      'bus-2022-ol-s2-q9-a', 'bus-2022-ol-s2-q9-c', 'bus-2022-ol-s2-q9-d-i', 'bus-2022-ol-s2-q9-d-ii']);
    expect(y2022.filter(card => !legacyIds.has(card.id))).toHaveLength(4);
  });

  it('preserves every Section 1 boundary at 15 marks with the published keys and row marks', () => {
    const cohort = y2022.filter(card => card.section === '1');
    expect(cohort).toHaveLength(15);
    for (let q = 1; q <= 15; q++) expect(cohort.filter(card => qOf(card) === String(q)).map(card => card.totalMarks), String(q)).toEqual([15]);
    for (const [q, steps, key] of [
      [3, [0, 4, 8, 12, 15], '1. Theory Y; 2. Theory X; 3. Theory X; 4. Theory Y'], [4, [0, 4, 8, 12, 15], 'cocoa beans Land'],
      [6, [0, 8, 15], 'European Parliament'], [7, [0, 4, 8, 12, 15], '(i) the government; (ii) two; (iii) equal; (iv) limited'],
      [8, [0, 8, 15], 'Tactical'], [11, [0, 5, 10, 15], 'import tax Tariff'], [12, [0, 4, 8, 12, 15], 'False; True; True; True'],
      [13, [0, 5, 10, 15], '1. Product; 2. Price; 4. Place'], [14, [0, 5, 10, 15], 'BATCH PRODUCTION'], [15, [0, 3, 6, 9, 12, 15], '1 D; 2 F; 3 A; 4 E; 5 C'],
    ] as const) {
      const card = find(`bus-2022-ol-s1-q${q}`);
      expect(card.rubric.responses[0].allocations[0].permittedMarks, String(q)).toEqual(steps);
      expect(card.rubric.guidance.join(' '), String(q)).toContain(key);
    }
    const chart = find('bus-2022-ol-s1-q5');
    expect(chart.rubric.responses.map(r => r.allocations.map(a => a.maxMarks))).toEqual([[4], [11]]);
    expect(chart.rubric.responses[1].allocations[0].permittedMarks).toEqual([0, 4, 8, 11]);
    expect(find('bus-2022-ol-s1-q9').rubric.responses.map(r => r.label)).toEqual(['Takeover', 'Merger']);
    expect(find('bus-2022-ol-s1-q10').rubric.responses[0].allocations.map(a => a.permittedMarks)).toEqual([[0, 4], [0, 2, 4, 6], [0, 5]]);
  });

  it.each([1, 2, 3, 4, 5, 6, 7, 8, 9])('preserves 2022 Ordinary Section 2 Q%i at 75 marks', q => {
    const base = y2022.filter(card => card.section === '2' && qOf(card) === String(q) && !routed.has(card.id));
    const pooled = 0;
    expect(base.reduce((sum, card) => sum + card.totalMarks, 0) + pooled).toBe(75);
  });

  it('keeps the calculation lines, the chart marks and the unattached sequences', () => {
    const bot = find('bus-2022-ol-s2-q3ci');
    expect(bot.rubric.responses[0].allocations.map(a => a.permittedMarks)).toEqual([[0, 2], [0, 2, 4, 6], [0, 1, 2]]);
    expect(find('bus-2022-ol-s2-q6d').rubric.responses[0].allocations.map(a => a.maxMarks)).toEqual([1, 2, 2, 2, 2, 2, 2, 2]);
    expect(find('bus-2022-ol-s2-q7ci').rubric.responses[0].allocations.map(a => a.permittedMarks)).toEqual([[0, 2], [0, 2], [0, 2], [0, 2], [0, 2]]);
    expect(find('bus-2022-ol-s2-q1ei').rubric.responses.map(r => r.allocations.map(a => a.maxMarks))).toEqual([[4, 2], [4, 2], [2, 1]]);
    expect(find('bus-2022-ol-s2-q5b').rubric.responses.map(r => r.label)).toEqual(['Risk 1', 'Risk 2', 'Reward 1', 'Reward 2']);
    expect(find('bus-2022-ol-s2-q6aii').rubric.guidance.join(' ')).toContain('two sources you chose in (i)');
    expect(find('bus-2022-ol-s2-q9-a').rubric.responses[0].allocations.map(a => a.maxMarks)).toEqual([1, 1, 1, 2, 2, 2, 2, 2, 2]);
  });

  it('files both 2022 Ordinary booklets and every route in Topic Atlas', () => {
    expect(find('bus-2022-ol-s2-q1d').topicId).toBe('business-0-14');
    expect(find('bus-2022-ol-s1-q14').topicId).toBe('business-4-15');
    for (const card of y2022) {
      const nodes = examTopicIdsForQuestion('business', 'ordinary', 2022, 'main', qOf(card), card.section === '1' ? 'p1' : 'p2')
        .flatMap(curriculumNodeIdsForExamTopic);
      for (const topic of [card.topicId, ...(card.additionalTopicIds ?? [])]) {
        expect(nodes, card.id).toContain(topic);
        expect(cardsForTopic(topic, ordinaryRubrics), card.id).toContain(card);
      }
    }
  });
});

describe('Business 2021 Ordinary full paper', () => {
  const ordinaryRubrics = ORDINARY.filter(isRubricCard).filter(card => card.rubric.system === 'business');
  const y2021 = ordinaryRubrics.filter(card => card.year === 2021);
  const qOf = (card: { questionRef: string }) => card.questionRef.match(/ Q(\d+)/)![1];
  const find = (id: string) => {
    const card = ordinaryRubrics.find(item => item.id === id)!;
    if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
    return card as typeof card & { rubric: Extract<typeof card.rubric, { system: 'business' }> };
  };

  it('keeps every 2021 Ordinary legacy ID and total, with three new cards and no route pool', () => {
    const legacy = authored.filter(card => card.year === 2021 && card.level === 'ordinary');
    expect(legacy).toHaveLength(68);
    for (const original of legacy) {
      const card = find(original.id);
      expect(card.totalMarks, original.id).toBe(original.totalMarks);
      expect(card.questionRef, original.id).toBe(original.questionRef);
      expect(supplement.cards.find(item => item.id === original.id), original.id)
        .toMatchObject({ correction: { originalQuestionText: original.questionText, originalTotalMarks: original.totalMarks } });
    }
    const legacyIds = new Set(legacy.map(card => card.id));
    expect(y2021.filter(card => !legacyIds.has(card.id)).map(card => card.id).sort()).toEqual([
      'bus-2021-ol-s1-q7', 'bus-2021-ol-s2-q9-c-i', 'bus-2021-ol-s2-q9-d']);
    expect(routePools.pools.some(pool => pool.template.year === 2021 && pool.template.level === 'ordinary')).toBe(false);
  });

  it.each([
    ['bus-2021-ol-s2-q6e', ['Utmost Good Faith', 'Indemnity', 'Insurable Interest'], [[4, 4], [4, 3]]],
    ['bus-2021-ol-s2-q8a', ['Idea Generation', 'Product Screening', 'Feasibility Study'], [[5, 3], [5, 2]]],
  ] as const)('keeps the printed choice %s as one card carrying every printed item', (id, items, marks) => {
    const card = find(id);
    expect(card.totalMarks).toBe(15);
    expect(tariffReconciles(card)).toBe(true);
    expect(card.rubric.responses.map(r => r.allocations.map(a => a.maxMarks))).toEqual(marks);
    expect(card.rubric.responses.map(r => r.label)).toEqual(
      id.endsWith('q6e') ? ['First principle you chose', 'Second principle you chose'] : ['First term you chose', 'Second term you chose']);
    for (const item of items) {
      expect(card.questionText, item).toContain(item);
      expect(card.rubric.guidance.filter(line => line.startsWith(item)), item).toHaveLength(1);
    }
    expect(ordinaryRubrics.filter(other => other.id.startsWith(`${id}-`))).toEqual([]);
    const reviews = Object.values(selectionReviews.reviews as Record<string, { classification: string; cardId?: string }>)
      .filter(review => review.cardId === id);
    expect(reviews.map(review => review.classification)).toEqual(['finite-choice']);
  });

  it('preserves every Section 1 boundary at 15 marks with the published keys and row marks', () => {
    const cohort = y2021.filter(card => card.section === '1');
    expect(cohort).toHaveLength(15);
    for (let q = 1; q <= 15; q++) expect(cohort.filter(card => qOf(card) === String(q)).map(card => card.totalMarks), String(q)).toEqual([15]);
    for (const [q, steps, key] of [
      [2, [0, 4, 8, 12, 15], '(i) TRUE; (ii) FALSE; (iii) TRUE; (iv) TRUE'], [3, [0, 8, 15], 'SEGMENTATION'],
      [4, [0, 5, 10, 15], 'Market Trends'], [5, [0, 4, 8, 12, 15], 'Set the standard 1'], [7, [0, 5, 10, 15], 'EU PARLIAMENT'],
      [12, [0, 3, 6, 9, 12, 15], '1 D; 2 B; 3 A; 4 F; 5 C'], [13, [0, 8, 15], 'LAND'], [14, [0, 4, 8, 12, 15], 'Apple Strength'],
      [15, [0, 4, 8, 12, 15], '(iv) Aided'],
    ] as const) {
      const card = find(`bus-2021-ol-s1-q${q}`);
      expect(card.rubric.responses[0].allocations[0].permittedMarks, String(q)).toEqual(steps);
      expect(card.rubric.guidance.join(' '), String(q)).toContain(key);
    }
    expect(find('bus-2021-ol-s1-q6').rubric.responses.map(r => r.allocations[0].permittedMarks)).toEqual([[0, 4, 8], [0, 4, 7]]);
    expect(find('bus-2021-ol-s1-q8').rubric.responses[0].allocations.map(a => a.maxMarks)).toEqual([4, 4, 4, 3]);
    expect(find('bus-2021-ol-s1-q11').rubric.responses.map(r => r.allocations.map(a => a.maxMarks))).toEqual([[3, 3, 2], [3, 2, 2]]);
  });

  it.each([1, 2, 3, 4, 5, 6, 7, 8, 9])('preserves 2021 Ordinary Section 2 Q%i at 75 marks', q => {
    const cohort = y2021.filter(card => card.section === '2' && qOf(card) === String(q));
    expect(cohort.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(75);
  });

  it('keeps the calculation lines, the diagram marks and the named-item marks', () => {
    expect(find('bus-2021-ol-s2-q3ai').rubric.responses[0].allocations.map(a => a.maxMarks)).toEqual([2, 5, 5, 4]);
    expect(find('bus-2021-ol-s2-q3ai').rubric.responses[0].allocations.map(a => a.permittedMarks)[3]).toEqual([0, 4]);
    expect(find('bus-2021-ol-s2-q6c').rubric.responses[0].allocations[0].permittedMarks).toEqual([0, 1, 2, 3, 4, 5, 6, 7, 8, 10]);
    expect(find('bus-2021-ol-s2-q8d').rubric.responses[0].allocations.map(a => a.maxMarks)).toEqual([2, 2, 2, 2, 2]);
    expect(find('bus-2021-ol-s2-q2c').rubric.responses.map(r => [r.label, r.allocations.map(a => a.maxMarks)])).toEqual([['Advantage', [4, 4]], ['Disadvantage', [4, 3]]]);
    expect(find('bus-2021-ol-s2-q8cii').rubric.responses.map(r => [r.label, r.allocations.map(a => a.maxMarks)])).toEqual([['Job production', [4, 3]], ['Batch production', [3, 3]]]);
    expect(find('bus-2021-ol-s2-q2dii').rubric.responses.map(r => r.allocations.map(a => a.maxMarks))).toEqual([[4, 4, 2], [4, 4, 2]]);
    expect(find('bus-2021-ol-s2-q9-b').rubric.responses.map(r => r.allocations.map(a => a.maxMarks))).toEqual([[4, 3], [4, 3], [4, 2]]);
    expect(find('bus-2021-ol-s2-q7bii').rubric.guidance.join(' ')).toContain('the month you chose in (i)');
  });

  it('files both 2021 Ordinary booklets and every corrected topic in Topic Atlas', () => {
    expect(find('bus-2021-ol-s1-q6').topicId).toBe('business-0-14');
    expect(find('bus-2021-ol-s2-q9-a').topicId).toBe('business-4-17');
    expect(find('bus-2021-ol-s2-q7e').topicId).toBe('business-4-15');
    for (const card of y2021) {
      const nodes = examTopicIdsForQuestion('business', 'ordinary', 2021, 'main', qOf(card), card.section === '1' ? 'p1' : 'p2')
        .flatMap(curriculumNodeIdsForExamTopic);
      for (const topic of [card.topicId, ...(card.additionalTopicIds ?? [])]) {
        expect(nodes, card.id).toContain(topic);
        expect(cardsForTopic(topic, ordinaryRubrics), card.id).toContain(card);
      }
    }
  });
});

describe('Business 2010 Ordinary full paper', () => {
  const ordinaryRubrics = ORDINARY.filter(isRubricCard).filter(card => card.rubric.system === 'business');
  const y2010 = ordinaryRubrics.filter(card => card.year === 2010);
  const qOf = (card: { questionRef: string }) => card.questionRef.match(/ Q(\d+)/)![1];
  const find = (id: string) => {
    const card = ordinaryRubrics.find(item => item.id === id)!;
    if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
    return card as typeof card & { rubric: Extract<typeof card.rubric, { system: 'business' }> };
  };
  const maxes = (id: string) => find(id).rubric.responses.map(r => r.allocations.map(a => a.maxMarks));

  it('adds the single-booklet 2010 Ordinary paper with no earlier card, no route and no printed choice', () => {
    expect(authored.filter(card => card.year === 2010 && card.level === 'ordinary')).toHaveLength(0);
    expect(y2010).toHaveLength(60);
    expect(routePools.pools.some(pool => pool.template.year === 2010 && pool.template.level === 'ordinary')).toBe(false);
    for (const card of y2010) {
      expect(card.paperFileid, card.id).toBe('LC033GLP000EV');
      expect(card.rubric.schemeFileid, card.id).toBe('LC033GLP000EV');
      expect(tariffReconciles(card), card.id).toBe(true);
      expect(card.rubric.guidance.some(line => / \(scheme PDF page \d+\): “/.test(line)), card.id).toBe(false);
    }
  });

  it('preserves every Section 1 boundary at 10 marks with the summary sequences and keys', () => {
    const cohort = y2010.filter(card => card.section === '1');
    expect(cohort).toHaveLength(15);
    for (let q = 1; q <= 15; q++) expect(cohort.filter(card => qOf(card) === String(q)).map(card => card.totalMarks), String(q)).toEqual([10]);
    for (const [q, stepList, key] of [
      [3, [0, 2, 4, 6, 8, 10], 'A coal mining company Primary'], [5, [0, 2, 4, 6, 8, 10], '1 C; 2 F; 3 E; 4 A; 5 B'],
      [8, [0, 2, 4, 6, 8, 10], '1 True; 2 True; 3 True; 4 False; 5 True'], [9, [0, 4, 7, 10], 'Membership of traveller community'],
    ] as const) {
      const card = find(`bus-2010-ol-s1-q${q}`);
      expect(card.rubric.responses[0].allocations[0].permittedMarks, String(q)).toEqual(stepList);
      expect(card.rubric.guidance.join(' '), String(q)).toContain(key);
    }
    expect(maxes('bus-2010-ol-s1-q1')).toEqual([[3], [3], [1, 1, 1, 1]]);
    expect(maxes('bus-2010-ol-s1-q7')).toEqual([[1, 1, 1, 1, 1, 1], [4]]);
    expect(maxes('bus-2010-ol-s1-q13')).toEqual([[2, 2, 2], [2], [2]]);
    expect(find('bus-2010-ol-s1-q2').rubric.responses.map(r => r.allocations[0].permittedMarks)).toEqual([[0, 1, 2, 3, 5], [0, 1, 2, 3, 5]]);
  });

  it.each([1, 2, 3, 4, 5, 6, 7, 8])('preserves 2010 Ordinary Section 2 Q%i at 75 marks', q => {
    const cohort = y2010.filter(card => card.section === '2' && qOf(card) === String(q));
    expect(cohort.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(75);
  });

  it('keeps the published sub-part splits, the notice and agenda, the life cycle and the one-sentence sole trader part', () => {
    for (const [id, total] of [
      ['bus-2010-ol-s2-q1ai', 10], ['bus-2010-ol-s2-q1aii', 20], ['bus-2010-ol-s2-q1aiii', 20], ['bus-2010-ol-s2-q1bi', 15], ['bus-2010-ol-s2-q1bii', 10],
      ['bus-2010-ol-s2-q2ci', 10], ['bus-2010-ol-s2-q2cii', 10], ['bus-2010-ol-s2-q3ai', 10], ['bus-2010-ol-s2-q3aii', 20], ['bus-2010-ol-s2-q3aiii', 20],
      ['bus-2010-ol-s2-q3bi', 15], ['bus-2010-ol-s2-q3bii', 10], ['bus-2010-ol-s2-q5bi', 10], ['bus-2010-ol-s2-q5bii', 10], ['bus-2010-ol-s2-q5di', 10],
      ['bus-2010-ol-s2-q5dii', 10], ['bus-2010-ol-s2-q6ai', 10], ['bus-2010-ol-s2-q6aii', 10], ['bus-2010-ol-s2-q7di', 10], ['bus-2010-ol-s2-q7dii', 5],
      ['bus-2010-ol-s2-q8a', 20], ['bus-2010-ol-s2-q8bi', 9], ['bus-2010-ol-s2-q8bii', 11],
    ] as const) expect(find(id).totalMarks, id).toBe(total);
    expect(find('bus-2010-ol-s2-q1ai').rubric.responses[0].allocations[0].permittedMarks).toEqual([0, 2, 4, 6, 8, 10]);
    expect(maxes('bus-2010-ol-s2-q1aii')).toEqual([[3, 2], [3, 2], [3, 2], [3, 2]]);
    expect(maxes('bus-2010-ol-s2-q5a')).toEqual([[2, 2, 2, 2, 2, 2, 2], [1], [2, 2, 2, 2, 2]]);
    expect(maxes('bus-2010-ol-s2-q7b')).toEqual([[2, 2, 2, 2, 2], [1, 1], [3]]);
    expect(maxes('bus-2010-ol-s2-q8a')).toEqual([[5], [5], [5], [5]]);
    expect(find('bus-2010-ol-s2-q8a').questionText).toContain('State (i) two advantages AND (ii) two disadvantages of a sole trader business.');
    expect(maxes('bus-2010-ol-s2-q8bii')).toEqual([[4], [4], [3]]);
  });

  it('files the 2010 Ordinary booklet in Topic Atlas with single-booklet identities', () => {
    for (const card of y2010) {
      const n = card.section === '1' ? qOf(card) : `S2Q${qOf(card)}`;
      const nodes = examTopicIdsForQuestion('business', 'ordinary', 2010, 'main', n, 'single').flatMap(curriculumNodeIdsForExamTopic);
      for (const topic of [card.topicId, ...(card.additionalTopicIds ?? [])]) {
        expect(nodes, card.id).toContain(topic);
        expect(cardsForTopic(topic, ordinaryRubrics), card.id).toContain(card);
      }
    }
  });
});

describe('Business 2011 Ordinary full paper', () => {
  const ordinaryRubrics = ORDINARY.filter(isRubricCard).filter(card => card.rubric.system === 'business');
  const y2011 = ordinaryRubrics.filter(card => card.year === 2011);
  const qOf = (card: { questionRef: string }) => card.questionRef.match(/ Q(\d+)/)![1];
  const find = (id: string) => {
    const card = ordinaryRubrics.find(item => item.id === id)!;
    if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
    return card as typeof card & { rubric: Extract<typeof card.rubric, { system: 'business' }> };
  };
  const maxes = (id: string) => find(id).rubric.responses.map(r => r.allocations.map(a => a.maxMarks));

  it('adds the single-booklet 2011 Ordinary paper with no earlier card and no route', () => {
    expect(authored.filter(card => card.year === 2011 && card.level === 'ordinary')).toHaveLength(0);
    expect(y2011).toHaveLength(61);
    expect(routePools.pools.some(pool => pool.template.year === 2011 && pool.template.level === 'ordinary')).toBe(false);
    for (const card of y2011) {
      expect(card.paperFileid, card.id).toBe('LC033GLP000EV');
      expect(card.rubric.schemeFileid, card.id).toBe('LC033GLP000EV');
      expect(tariffReconciles(card), card.id).toBe(true);
    }
  });

  it('preserves every Section 1 boundary at 10 marks with the summary sequences and keys', () => {
    const cohort = y2011.filter(card => card.section === '1');
    expect(cohort).toHaveLength(15);
    for (let q = 1; q <= 15; q++) expect(cohort.filter(card => qOf(card) === String(q)).map(card => card.totalMarks), String(q)).toEqual([10]);
    for (const [q, stepList, key] of [
      [3, [0, 3, 6, 8, 10], 'Payment of electricity bill Short term'], [7, [0, 2, 4, 6, 8, 10], '(i) True; (ii) False; (iii) True; (iv) False; (v) True'],
      [13, [0, 2, 4, 6, 8, 10], '1 D; 2 E; 3 A; 4 F; 5 C'], [15, [0, 5, 10], '(i) Increase; (ii) Increase'],
    ] as const) {
      const card = find(`bus-2011-ol-s1-q${q}`);
      expect(card.rubric.responses[0].allocations[0].permittedMarks, String(q)).toEqual(stepList);
      expect(card.rubric.guidance.join(' '), String(q)).toContain(key);
    }
    expect(maxes('bus-2011-ol-s1-q2')).toEqual([[3, 3], [2], [2]]);
    expect(maxes('bus-2011-ol-s1-q6')).toEqual([[2, 4, 4]]);
  });

  it.each([1, 2, 3, 4, 5, 6, 7, 8])('preserves 2011 Ordinary Section 2 Q%i at 75 marks', q => {
    const cohort = y2011.filter(card => card.section === '2' && qOf(card) === String(q));
    expect(cohort.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(75);
  });

  it('keeps the published sub-part splits, the even law steps and the SWOT words', () => {
    for (const [id, total] of [
      ['bus-2011-ol-s2-q1ai', 10], ['bus-2011-ol-s2-q1aii', 15], ['bus-2011-ol-s2-q1aiii', 25], ['bus-2011-ol-s2-q1bi', 15], ['bus-2011-ol-s2-q1bii', 10],
      ['bus-2011-ol-s2-q3di', 6], ['bus-2011-ol-s2-q3dii', 14], ['bus-2011-ol-s2-q5ci', 3], ['bus-2011-ol-s2-q5cii', 12], ['bus-2011-ol-s2-q5di', 10],
      ['bus-2011-ol-s2-q5dii', 10], ['bus-2011-ol-s2-q6bi', 10], ['bus-2011-ol-s2-q6bii', 10], ['bus-2011-ol-s2-q6di', 5], ['bus-2011-ol-s2-q6dii', 15],
      ['bus-2011-ol-s2-q6ei', 10], ['bus-2011-ol-s2-q6eii', 5], ['bus-2011-ol-s2-q7ci', 10], ['bus-2011-ol-s2-q7cii', 10], ['bus-2011-ol-s2-q7di', 15],
      ['bus-2011-ol-s2-q7dii', 10], ['bus-2011-ol-s2-q8ci', 10], ['bus-2011-ol-s2-q8cii', 10], ['bus-2011-ol-s2-q8di', 16], ['bus-2011-ol-s2-q8dii', 4],
    ] as const) expect(find(id).totalMarks, id).toBe(total);
    expect(find('bus-2011-ol-s2-q1ai').rubric.responses[0].allocations[0].permittedMarks).toEqual([0, 2, 4, 6, 8, 10]);
    expect(maxes('bus-2011-ol-s2-q1aiii')).toEqual([[5, 4], [4, 4], [4, 4]]);
    expect(maxes('bus-2011-ol-s2-q7a')).toEqual([[2, 3], [2, 3], [2, 3], [2, 3]]);
    for (const response of find('bus-2011-ol-s2-q7a').rubric.responses) expect(response.allocations[0].permittedMarks).toEqual([0, 2]);
    expect(maxes('bus-2011-ol-s2-q7di')).toEqual([[3, 1, 8, 3]]);
    expect(maxes('bus-2011-ol-s2-q8di')).toEqual([[4, 6, 6]]);
  });

  it('reads the strip-cut page 11 as printed and keeps each printed choice as one card', () => {
    expect(find('bus-2011-ol-s2-q8di').questionText).toContain('Current Liabilities | 500,000 | 400,000');
    expect(find('bus-2011-ol-s2-q8a').questionText).toContain('Brady’s Hotel is a family run business situated in a seaside town.');
    for (const [id, items, sequence] of [
      ['bus-2011-ol-s2-q4e', ['Form P60', 'Form P45', 'Form P21'], [[3, 2], [3, 2]]],
      ['bus-2011-ol-s2-q8cii', ['Physical Needs', 'Safety/Security Needs', 'Social Needs', 'Esteem Needs', 'Self-actualisation Needs'], [[3, 2], [3, 2]]],
    ] as const) {
      const choice = find(id);
      expect(maxes(id), id).toEqual(sequence);
      for (const item of items) expect(choice.rubric.guidance.filter(line => line.startsWith(`${item} (scheme PDF page `)), item).toHaveLength(1);
    }
    for (const item of ['Form P60', 'Form P45', 'Form P21']) expect(find('bus-2011-ol-s2-q4e').questionText).toContain(item);
  });

  it('files the 2011 Ordinary booklet in Topic Atlas with single-booklet identities', () => {
    for (const card of y2011) {
      const n = card.section === '1' ? qOf(card) : `S2Q${qOf(card)}`;
      const nodes = examTopicIdsForQuestion('business', 'ordinary', 2011, 'main', n, 'single').flatMap(curriculumNodeIdsForExamTopic);
      for (const topic of [card.topicId, ...(card.additionalTopicIds ?? [])]) {
        expect(nodes, card.id).toContain(topic);
        expect(cardsForTopic(topic, ordinaryRubrics), card.id).toContain(card);
      }
    }
  });
});

describe('Business 2012 Ordinary full paper', () => {
  const ordinaryRubrics = ORDINARY.filter(isRubricCard).filter(card => card.rubric.system === 'business');
  const y2012 = ordinaryRubrics.filter(card => card.year === 2012);
  const qOf = (card: { questionRef: string }) => card.questionRef.match(/ Q(\d+)/)![1];
  const find = (id: string) => {
    const card = ordinaryRubrics.find(item => item.id === id)!;
    if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
    return card as typeof card & { rubric: Extract<typeof card.rubric, { system: 'business' }> };
  };
  const maxes = (id: string) => find(id).rubric.responses.map(r => r.allocations.map(a => a.maxMarks));

  it('adds the single-booklet 2012 Ordinary paper with no earlier card and no route', () => {
    expect(authored.filter(card => card.year === 2012 && card.level === 'ordinary')).toHaveLength(0);
    expect(y2012).toHaveLength(61);
    expect(routePools.pools.some(pool => pool.template.year === 2012 && pool.template.level === 'ordinary')).toBe(false);
    for (const card of y2012) {
      expect(card.paperFileid, card.id).toBe('LC033GLP000EV');
      expect(card.rubric.schemeFileid, card.id).toBe('LC033GLP000EV');
      expect(tariffReconciles(card), card.id).toBe(true);
    }
  });

  it('preserves every Section 1 boundary at 10 marks with the summary sequences and keys', () => {
    const cohort = y2012.filter(card => card.section === '1');
    expect(cohort).toHaveLength(15);
    for (let q = 1; q <= 15; q++) expect(cohort.filter(card => qOf(card) === String(q)).map(card => card.totalMarks), String(q)).toEqual([10]);
    for (const [q, stepList, key] of [
      [6, [0, 5, 10], 'Land and Capital'], [8, [0, 2, 4, 6, 8, 10], 'TRUE; FALSE; FALSE; TRUE; TRUE'],
      [10, [0, 2, 4, 6, 8, 10], '1 F; 2 E; 3 A; 4 B; 5 C'], [15, [0, 4, 7, 10], 'Verbal Telephone'],
    ] as const) {
      const card = find(`bus-2012-ol-s1-q${q}`);
      expect(card.rubric.responses[0].allocations[0].permittedMarks, String(q)).toEqual(stepList);
      expect(card.rubric.guidance.join(' '), String(q)).toContain(key);
    }
    expect(maxes('bus-2012-ol-s1-q1')).toEqual([[4], [3], [3]]);
    expect(maxes('bus-2012-ol-s1-q3')).toEqual([[3], [3], [2], [2]]);
    expect(maxes('bus-2012-ol-s1-q12')).toEqual([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]);
    expect(find('bus-2012-ol-s1-q5').rubric.responses.map(r => r.allocations[0].permittedMarks)).toEqual([[0, 1, 2, 3, 5], [0, 1, 2, 3, 5]]);
  });

  it.each([1, 2, 3, 4, 5, 6, 7, 8])('preserves 2012 Ordinary Section 2 Q%i at 75 marks', q => {
    const cohort = y2012.filter(card => card.section === '2' && qOf(card) === String(q));
    expect(cohort.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(75);
  });

  it('keeps the published sub-part splits, the take-home pay groups and the notice and agenda', () => {
    for (const [id, total] of [
      ['bus-2012-ol-s2-q1di', 10], ['bus-2012-ol-s2-q1dii', 15], ['bus-2012-ol-s2-q3ai', 10], ['bus-2012-ol-s2-q3aii', 5],
      ['bus-2012-ol-s2-q3bi', 9], ['bus-2012-ol-s2-q3bii', 6], ['bus-2012-ol-s2-q5ci', 5], ['bus-2012-ol-s2-q5cii', 5],
      ['bus-2012-ol-s2-q7ci', 8], ['bus-2012-ol-s2-q7cii', 7], ['bus-2012-ol-s2-q7ei', 8], ['bus-2012-ol-s2-q7eii', 7],
      ['bus-2012-ol-s2-q8bi', 8], ['bus-2012-ol-s2-q8bii', 7],
    ] as const) expect(find(id).totalMarks, id).toBe(total);
    expect(maxes('bus-2012-ol-s2-q4b')).toEqual([[2, 2, 2, 2, 2, 2, 2], [1], [3, 3, 2, 2]]);
    const pay = find('bus-2012-ol-s2-q5d').rubric.responses[0].allocations;
    expect(pay.map(a => a.maxMarks)).toEqual([16, 4]);
    expect(pay[0].permittedMarks).toEqual([0, 4, 8, 12, 16]);
    expect(pay[1].permittedMarks).toEqual([0, 1, 2, 3, 4]);
    expect(find('bus-2012-ol-s2-q5d').rubric.guidance.join(' ')).toContain('Net Take Home Pay €26,960');
  });

  it('keeps each printed choice as one card with every item and the scheme wording for each', () => {
    for (const [id, items, sequence] of [
      ['bus-2012-ol-s2-q1b', ['Offer', 'Acceptance', 'Consideration', 'Consent to Contract'], [[9, 1], [9, 1], [4, 1]]],
      ['bus-2012-ol-s2-q5b', ['Insurable Interest', 'Indemnity', 'Utmost Good Faith'], [[3, 2, 3], [3, 2, 2]]],
      ['bus-2012-ol-s2-q5e', ['Term Loan', 'Leasing'], [[8], [7]]],
      ['bus-2012-ol-s2-q6a', ['Training and Development', 'Recruitment and Selection', 'Employer/Employee Relations'], [[5, 5], [5, 5]]],
    ] as const) {
      const choice = find(id);
      expect(maxes(id), id).toEqual(sequence);
      for (const item of items) {
        expect(choice.questionText, item).toContain(item);
        expect(choice.rubric.guidance.filter(line => line.startsWith(`${item} (scheme PDF page `)), item).toHaveLength(1);
      }
    }
  });

  it('files the 2012 Ordinary booklet in Topic Atlas with single-booklet identities', () => {
    for (const card of y2012) {
      const n = card.section === '1' ? qOf(card) : `S2Q${qOf(card)}`;
      const nodes = examTopicIdsForQuestion('business', 'ordinary', 2012, 'main', n, 'single').flatMap(curriculumNodeIdsForExamTopic);
      for (const topic of [card.topicId, ...(card.additionalTopicIds ?? [])]) {
        expect(nodes, card.id).toContain(topic);
        expect(cardsForTopic(topic, ordinaryRubrics), card.id).toContain(card);
      }
    }
  });
});

describe('Business 2013 Ordinary full paper', () => {
  const ordinaryRubrics = ORDINARY.filter(isRubricCard).filter(card => card.rubric.system === 'business');
  const y2013 = ordinaryRubrics.filter(card => card.year === 2013);
  const qOf = (card: { questionRef: string }) => card.questionRef.match(/ Q(\d+)/)![1];
  const find = (id: string) => {
    const card = ordinaryRubrics.find(item => item.id === id)!;
    if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
    return card as typeof card & { rubric: Extract<typeof card.rubric, { system: 'business' }> };
  };
  const maxes = (id: string) => find(id).rubric.responses.map(r => r.allocations.map(a => a.maxMarks));

  it('adds the single-booklet 2013 Ordinary paper with no earlier card and no route', () => {
    expect(authored.filter(card => card.year === 2013 && card.level === 'ordinary')).toHaveLength(0);
    expect(y2013).toHaveLength(55);
    expect(routePools.pools.some(pool => pool.template.year === 2013 && pool.template.level === 'ordinary')).toBe(false);
    for (const card of y2013) {
      expect(card.paperFileid, card.id).toBe('LC033GLP000EV');
      expect(card.rubric.schemeFileid, card.id).toBe('LC033GLP000EV');
      expect(tariffReconciles(card), card.id).toBe(true);
    }
  });

  it('preserves every Section 1 boundary at 10 marks with the summary sequences and keys', () => {
    const cohort = y2013.filter(card => card.section === '1');
    expect(cohort).toHaveLength(15);
    for (let q = 1; q <= 15; q++) expect(cohort.filter(card => qOf(card) === String(q)).map(card => card.totalMarks), String(q)).toEqual([10]);
    for (const [q, stepList, key] of [
      [2, [0, 4, 7, 10], '5. Self-Actualisation Needs 4. Esteem Needs 3. Social Needs'], [4, [0, 4, 7, 10], 'PRODUCT PRICE PLACE PROMOTION'],
      [7, [0, 3, 6, 8, 10], 'Justin Timberlake in Dublin Invisible Import'], [9, [0, 2, 4, 6, 8, 10], 'FIELD; DESK; DESK; FIELD; FIELD'],
      [12, [0, 4, 7, 10], 'QUALITY CONTROL'], [13, [0, 2, 4, 6, 8, 10], '1 D; 2 F; 3 E; 4 B; 5 C'], [14, [0, 2, 4, 6, 8, 10], 'TRUE; FALSE; FALSE; TRUE; TRUE'],
    ] as const) {
      const card = find(`bus-2013-ol-s1-q${q}`);
      expect(card.rubric.responses[0].allocations[0].permittedMarks, String(q)).toEqual(stepList);
      expect(card.rubric.guidance.join(' '), String(q)).toContain(key);
    }
    expect(maxes('bus-2013-ol-s1-q1')).toEqual([[3], [4], [3]]);
    expect(maxes('bus-2013-ol-s1-q6')).toEqual([[4], [6]]);
  });

  it.each([1, 2, 3, 4, 5, 6, 7, 8])('preserves 2013 Ordinary Section 2 Q%i at 75 marks', q => {
    const cohort = y2013.filter(card => card.section === '2' && qOf(card) === String(q));
    expect(cohort.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(75);
  });

  it('keeps the summary splits, the notice and agenda, the letter and the one-card stage choice', () => {
    expect(maxes('bus-2013-ol-s2-q1a')).toEqual([[7], [4], [4]]);
    expect(maxes('bus-2013-ol-s2-q3a')).toEqual([[2, 5, 2, 2, 2, 2]]);
    expect(find('bus-2013-ol-s2-q3a').rubric.responses[0].allocations[1].permittedMarks).toEqual([0, 1, 2, 3, 4, 5]);
    expect(maxes('bus-2013-ol-s2-q3e')).toEqual([[5], [5], [5, 5]]);
    expect(maxes('bus-2013-ol-s2-q4b')).toEqual([[3, 2], [3, 2], [3, 2], [3, 2]]);
    expect(maxes('bus-2013-ol-s2-q5c')).toEqual([[2, 2, 2, 2, 2], [1], [2, 2, 2, 2, 2], [2, 2]]);
    expect(maxes('bus-2013-ol-s2-q6e')).toEqual([[2], [5, 4], [5, 4]]);
    expect(maxes('bus-2013-ol-s2-q7c')).toEqual([[1, 1, 3, 2, 2, 2, 2, 2]]);
    expect(maxes('bus-2013-ol-s2-q8d')).toEqual([[2, 2, 2, 1, 1, 1, 1, 10]]);
    const choice = find('bus-2013-ol-s2-q8c');
    expect(maxes('bus-2013-ol-s2-q8c')).toEqual([[4, 4], [4, 3]]);
    for (const item of ['Idea Generation', 'Prototype Development', 'Test Marketing']) {
      expect(choice.questionText, item).toContain(item);
      expect(choice.rubric.guidance.filter(line => line.startsWith(`${item} (scheme PDF page `)), item).toHaveLength(1);
    }
  });

  it('files the 2013 Ordinary booklet in Topic Atlas with single-booklet identities', () => {
    for (const card of y2013) {
      const n = card.section === '1' ? qOf(card) : `S2Q${qOf(card)}`;
      const nodes = examTopicIdsForQuestion('business', 'ordinary', 2013, 'main', n, 'single').flatMap(curriculumNodeIdsForExamTopic);
      for (const topic of [card.topicId, ...(card.additionalTopicIds ?? [])]) {
        expect(nodes, card.id).toContain(topic);
        expect(cardsForTopic(topic, ordinaryRubrics), card.id).toContain(card);
      }
    }
  });
});

describe('Business 2014 Ordinary full paper', () => {
  const ordinaryRubrics = ORDINARY.filter(isRubricCard).filter(card => card.rubric.system === 'business');
  const y2014 = ordinaryRubrics.filter(card => card.year === 2014);
  const qOf = (card: { questionRef: string }) => card.questionRef.match(/ Q(\d+)/)![1];
  const find = (id: string) => {
    const card = ordinaryRubrics.find(item => item.id === id)!;
    if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
    return card as typeof card & { rubric: Extract<typeof card.rubric, { system: 'business' }> };
  };
  const maxes = (id: string) => find(id).rubric.responses.map(r => r.allocations.map(a => a.maxMarks));
  const steps = (id: string, r = 0) => find(id).rubric.responses[r].allocations[0].permittedMarks;

  it('adds the single-booklet 2014 Ordinary paper with no earlier card and no route', () => {
    expect(authored.filter(card => card.year === 2014 && card.level === 'ordinary')).toHaveLength(0);
    expect(y2014).toHaveLength(58);
    expect(routePools.pools.some(pool => pool.template.year === 2014 && pool.template.level === 'ordinary')).toBe(false);
    for (const card of y2014) {
      expect(card.paperFileid, card.id).toBe('LC033GLP000EV');
      expect(card.rubric.schemeFileid, card.id).toBe('LC033GLP000EV');
      expect(tariffReconciles(card), card.id).toBe(true);
    }
  });

  it('preserves every Section 1 boundary at 10 marks with the summary sequences and keys', () => {
    const cohort = y2014.filter(card => card.section === '1');
    expect(cohort).toHaveLength(15);
    for (let q = 1; q <= 15; q++) expect(cohort.filter(card => qOf(card) === String(q)).map(card => card.totalMarks), String(q)).toEqual([10]);
    for (const [q, stepList, key] of [
      [4, [0, 4, 7, 10], 'Growth, Maturity and Decline'], [5, [0, 4, 6, 8, 9, 10], '1 Chairperson; 2 Secretary'], [8, [0, 4, 6, 8, 9, 10], 'FALSE; TRUE; TRUE; TRUE; FALSE'],
      [10, [0, 4, 6, 8, 9, 10], '1 F; 2 D; 3 E; 4 C; 5 B'], [12, [0, 5, 10], 'European Central Bank'], [13, [0, 3, 6, 8, 10], 'fridge Not of merchantable quality'],
      [14, [0, 4, 7, 10], 'Membership of a trade union'],
    ] as const) {
      const card = find(`bus-2014-ol-s1-q${q}`);
      expect(card.rubric.responses[0].allocations[0].permittedMarks, String(q)).toEqual(stepList);
      expect(card.rubric.guidance.join(' '), String(q)).toContain(key);
    }
    expect(maxes('bus-2014-ol-s1-q1')).toEqual([[4], [3], [3]]);
    expect(maxes('bus-2014-ol-s1-q3')).toEqual([[2, 2], [3], [3]]);
    expect(maxes('bus-2014-ol-s1-q9')).toEqual([[2, 3, 3, 2]]);
  });

  it.each([1, 2, 3, 4, 5, 6, 7, 8])('preserves 2014 Ordinary Section 2 Q%i at 75 marks', q => {
    const cohort = y2014.filter(card => card.section === '2' && qOf(card) === String(q));
    expect(cohort.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(75);
  });

  it('keeps the published splits, the underlined terms, the graph, the memo and the take-home pay', () => {
    expect(maxes('bus-2014-ol-s2-q1d')).toEqual([[6, 2], [5, 2]]);
    expect(maxes('bus-2014-ol-s2-q1c')).toEqual([[10], [3], [2]]);
    expect([find('bus-2014-ol-s2-q2ai').totalMarks, find('bus-2014-ol-s2-q2aii').totalMarks]).toEqual([10, 5]);
    expect(maxes('bus-2014-ol-s2-q3a')).toEqual([[3, 1, 1, 2, 2, 2, 2, 2]]);
    expect(steps('bus-2014-ol-s2-q4d')).toEqual([0, 3, 6, 9, 12]);
    expect(maxes('bus-2014-ol-s2-q5d')).toEqual([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]);
    expect(find('bus-2014-ol-s2-q6b').rubric.responses.map(r => r.label)).toEqual(['Job Description', 'Person Specification', 'Bonuses', 'Benefits-in-kind']);
    expect(maxes('bus-2014-ol-s2-q6e')).toEqual([[2, 3, 3, 3, 3, 3, 3]]);
    expect(steps('bus-2014-ol-s2-q6e')).toEqual([0, 2]);
    expect([find('bus-2014-ol-s2-q8ai').totalMarks, find('bus-2014-ol-s2-q8aii').totalMarks]).toEqual([10, 10]);
  });

  it('files the 2014 Ordinary booklet in Topic Atlas with single-booklet identities', () => {
    for (const card of y2014) {
      const n = card.section === '1' ? qOf(card) : `S2Q${qOf(card)}`;
      const nodes = examTopicIdsForQuestion('business', 'ordinary', 2014, 'main', n, 'single').flatMap(curriculumNodeIdsForExamTopic);
      for (const topic of [card.topicId, ...(card.additionalTopicIds ?? [])]) {
        expect(nodes, card.id).toContain(topic);
        expect(cardsForTopic(topic, ordinaryRubrics), card.id).toContain(card);
      }
    }
  });
});

describe('Business 2015 Ordinary full paper', () => {
  const ordinaryRubrics = ORDINARY.filter(isRubricCard).filter(card => card.rubric.system === 'business');
  const y2015 = ordinaryRubrics.filter(card => card.year === 2015);
  const qOf = (card: { questionRef: string }) => card.questionRef.match(/ Q(\d+)/)![1];
  const find = (id: string) => {
    const card = ordinaryRubrics.find(item => item.id === id)!;
    if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
    return card as typeof card & { rubric: Extract<typeof card.rubric, { system: 'business' }> };
  };
  const maxes = (id: string) => find(id).rubric.responses.map(r => r.allocations.map(a => a.maxMarks));
  const steps = (id: string, r = 0) => find(id).rubric.responses[r].allocations[0].permittedMarks;

  it('adds the single-booklet 2015 Ordinary paper with no earlier card and no route', () => {
    expect(authored.filter(card => card.year === 2015 && card.level === 'ordinary')).toHaveLength(0);
    expect(y2015).toHaveLength(56);
    expect(routePools.pools.some(pool => pool.template.year === 2015 && pool.template.level === 'ordinary')).toBe(false);
    for (const card of y2015) {
      expect(card.paperFileid, card.id).toBe('LC033GLP000EV');
      expect(card.rubric.schemeFileid, card.id).toBe('LC033GLP000EV');
      expect(tariffReconciles(card), card.id).toBe(true);
    }
  });

  it('preserves every Section 1 boundary at 10 marks with the summary sequences and keys', () => {
    const cohort = y2015.filter(card => card.section === '1');
    expect(cohort).toHaveLength(15);
    for (let q = 1; q <= 15; q++) expect(cohort.filter(card => qOf(card) === String(q)).map(card => card.totalMarks), String(q)).toEqual([10]);
    for (const [q, stepList, key] of [
      [3, [0, 3, 6, 8, 10], 'Press Conference Public Relations'], [5, [0, 5, 10], 'European Court of Auditors'], [7, [0, 5, 10], 'of sound mind'],
      [9, [0, 2, 4, 6, 8, 10], 'TRUE; FALSE; FALSE; FALSE; TRUE'], [11, [0, 4, 7, 10], 'BEP where TR crosses TC'], [12, [0, 4, 7, 10], 'PRODUCT PRICE PROMOTION'],
      [13, [0, 2, 4, 6, 8, 10], '1 F; 2 D; 3 E; 4 A; 5 C'], [15, [0, 3, 6, 8, 10], 'CEO / MD'],
    ] as const) {
      const card = find(`bus-2015-ol-s1-q${q}`);
      expect(card.rubric.responses[0].allocations[0].permittedMarks, String(q)).toEqual(stepList);
      expect(card.rubric.guidance.join(' '), String(q)).toContain(key);
    }
    expect(maxes('bus-2015-ol-s1-q1')).toEqual([[3], [3], [4]]);
    expect(maxes('bus-2015-ol-s1-q6')).toEqual([[4, 2, 2, 2]]);
    expect(steps('bus-2015-ol-s1-q14')).toEqual([0, 10]);
  });

  it.each([1, 2, 3, 4, 5, 6, 7, 8])('preserves 2015 Ordinary Section 2 Q%i at 75 marks', q => {
    const cohort = y2015.filter(card => card.section === '2' && qOf(card) === String(q));
    expect(cohort.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(75);
  });

  it('keeps the published splits, the notice and agenda, the charts and the one-card principle choice', () => {
    expect(steps('bus-2015-ol-s2-q1a')).toEqual([0, 2, 4, 6, 8, 10]);
    expect([find('bus-2015-ol-s2-q1ei').totalMarks, find('bus-2015-ol-s2-q1eii').totalMarks]).toEqual([15, 5]);
    expect(steps('bus-2015-ol-s2-q2b')).toEqual([0, 2, 4, 6, 8]);
    expect(maxes('bus-2015-ol-s2-q2b')).toEqual([[8], [4, 3]]);
    expect(maxes('bus-2015-ol-s2-q4d')).toEqual([[2, 2, 2, 2, 2], [2, 2, 2, 2], [1, 1]]);
    expect(maxes('bus-2015-ol-s2-q5e')).toEqual([[6, 2], [5, 2]]);
    expect(maxes('bus-2015-ol-s2-q6b')).toEqual([[1, 2, 2, 2, 2, 2, 2, 2]]);
    expect(maxes('bus-2015-ol-s2-q7e')).toEqual([[4, 4], [3, 3, 1]]);
    expect(maxes('bus-2015-ol-s2-q8d')).toEqual([[4, 4], [4, 3]]);
    const choice = find('bus-2015-ol-s2-q5b');
    expect(maxes('bus-2015-ol-s2-q5b')).toEqual([[4, 3, 3], [4, 3, 3]]);
    for (const item of ['Indemnity', 'Insurable Interest', 'Utmost Good Faith']) {
      expect(choice.questionText, item).toContain(item);
      expect(choice.rubric.guidance.filter(line => line.startsWith(`${item} (scheme PDF page `)), item).toHaveLength(1);
    }
  });

  it('files the 2015 Ordinary booklet in Topic Atlas with single-booklet identities', () => {
    for (const card of y2015) {
      const n = card.section === '1' ? qOf(card) : `S2Q${qOf(card)}`;
      const nodes = examTopicIdsForQuestion('business', 'ordinary', 2015, 'main', n, 'single').flatMap(curriculumNodeIdsForExamTopic);
      for (const topic of [card.topicId, ...(card.additionalTopicIds ?? [])]) {
        expect(nodes, card.id).toContain(topic);
        expect(cardsForTopic(topic, ordinaryRubrics), card.id).toContain(card);
      }
    }
  });
});

describe('Business 2016 Ordinary full paper', () => {
  const ordinaryRubrics = ORDINARY.filter(isRubricCard).filter(card => card.rubric.system === 'business');
  const y2016 = ordinaryRubrics.filter(card => card.year === 2016);
  const qOf = (card: { questionRef: string }) => card.questionRef.match(/ Q(\d+)/)![1];
  const find = (id: string) => {
    const card = ordinaryRubrics.find(item => item.id === id)!;
    if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
    return card as typeof card & { rubric: Extract<typeof card.rubric, { system: 'business' }> };
  };
  const maxes = (id: string) => find(id).rubric.responses.map(r => r.allocations.map(a => a.maxMarks));
  const steps = (id: string) => find(id).rubric.responses[0].allocations[0].permittedMarks;

  it('adds the single-booklet 2016 Ordinary paper with no earlier card and no route', () => {
    expect(authored.filter(card => card.year === 2016 && card.level === 'ordinary')).toHaveLength(0);
    expect(y2016).toHaveLength(63);
    expect(routePools.pools.some(pool => pool.template.year === 2016 && pool.template.level === 'ordinary')).toBe(false);
    for (const card of y2016) {
      expect(card.paperFileid, card.id).toBe('LC033GLP000EV');
      expect(card.rubric.schemeFileid, card.id).toBe('LC033GLP000EV');
      expect(tariffReconciles(card), card.id).toBe(true);
      // The scheme's text layer drops E and reads J as ':' in some runs; no card quotes them.
      expect(JSON.stringify(card), card.id).not.toMatch(/\bxplain|:ob|Wz|h\^/);
    }
  });

  it('preserves every Section 1 boundary at 10 marks with the summary sequences and keys', () => {
    const cohort = y2016.filter(card => card.section === '1');
    expect(cohort).toHaveLength(15);
    for (let q = 1; q <= 15; q++) expect(cohort.filter(card => qOf(card) === String(q)).map(card => card.totalMarks), String(q)).toEqual([10]);
    for (const [q, stepList, key] of [
      [2, [0, 4, 7, 10], 'email, letter, memo'], [4, [0, 5, 10], 'Labour and Enterprise'], [6, [0, 4, 7, 10], '(i) Planning (ii) Organising (iii) Controlling'],
      [8, [0, 5, 10], 'Race or colour'], [10, [0, 2, 4, 6, 8, 10], 'TRUE; FALSE; TRUE; TRUE; TRUE'], [12, [0, 5, 10], 'Common Fisheries Policy'],
      [14, [0, 3, 6, 8, 10], 'Stage 5 Decline'], [15, [0, 2, 4, 6, 8, 10], '1 B; 2 D; 3 F; 4 C; 5 A'],
    ] as const) {
      const card = find(`bus-2016-ol-s1-q${q}`);
      expect(card.rubric.responses[0].allocations[0].permittedMarks, String(q)).toEqual(stepList);
      expect(card.rubric.guidance.join(' '), String(q)).toContain(key);
    }
    expect(maxes('bus-2016-ol-s1-q1')).toEqual([[4], [3], [3]]);
    expect(maxes('bus-2016-ol-s1-q3')).toEqual([[3, 3, 2, 2]]);
    expect(maxes('bus-2016-ol-s1-q5')).toEqual([[3, 2, 2, 3]]);
    expect(maxes('bus-2016-ol-s1-q13')).toEqual([[4, 4], [2]]);
    expect(steps('bus-2016-ol-s1-q11')).toEqual([0, 10]);
  });

  it.each([1, 2, 3, 4, 5, 6, 7, 8])('preserves 2016 Ordinary Section 2 Q%i at 75 marks', q => {
    const cohort = y2016.filter(card => card.section === '2' && qOf(card) === String(q));
    expect(cohort.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(75);
  });

  it('splits every printed sub-part at its published marks and keeps the calculation lines', () => {
    for (const [id, total] of [['q2ai', 12], ['q2aii', 3], ['q2bi', 12], ['q2bii', 3], ['q3ai', 12], ['q3aii', 3], ['q3bi', 6], ['q3bii', 14],
      ['q6bi', 10], ['q6bii', 10], ['q7di', 8], ['q7dii', 12], ['q8ai', 5], ['q8aii', 10], ['q8bi', 10], ['q8bii', 10]] as const) {
      expect(find(`bus-2016-ol-s2-${id}`).totalMarks, id).toBe(total);
    }
    expect(steps('bus-2016-ol-s2-q1a')).toEqual([0, 2, 4, 6, 8, 10]);
    expect(maxes('bus-2016-ol-s2-q3ai')).toEqual([[3, 3, 3, 3]]);
    expect(steps('bus-2016-ol-s2-q3ai')).toEqual([0, 3]);
    expect(maxes('bus-2016-ol-s2-q3c')).toEqual([[5, 3], [5, 2]]);
    expect(maxes('bus-2016-ol-s2-q5c')).toEqual([[8], [7]]);
    expect(maxes('bus-2016-ol-s2-q6a')).toEqual([[4, 3, 3], [4, 3, 3]]);
    expect(maxes('bus-2016-ol-s2-q6c')).toEqual([[3, 2], [3, 2]]);
  });

  it('files the 2016 Ordinary booklet in Topic Atlas with single-booklet identities', () => {
    for (const card of y2016) {
      const n = card.section === '1' ? qOf(card) : `S2Q${qOf(card)}`;
      const nodes = examTopicIdsForQuestion('business', 'ordinary', 2016, 'main', n, 'single').flatMap(curriculumNodeIdsForExamTopic);
      for (const topic of [card.topicId, ...(card.additionalTopicIds ?? [])]) {
        expect(nodes, card.id).toContain(topic);
        expect(cardsForTopic(topic, ordinaryRubrics), card.id).toContain(card);
      }
    }
  });
});

describe('Business 2017 Ordinary full paper', () => {
  const ordinaryRubrics = ORDINARY.filter(isRubricCard).filter(card => card.rubric.system === 'business');
  const y2017 = ordinaryRubrics.filter(card => card.year === 2017);
  const qOf = (card: { questionRef: string }) => card.questionRef.match(/ Q(\d+)/)![1];
  const find = (id: string) => {
    const card = ordinaryRubrics.find(item => item.id === id)!;
    if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
    return card as typeof card & { rubric: Extract<typeof card.rubric, { system: 'business' }> };
  };
  const maxes = (id: string) => find(id).rubric.responses.map(r => r.allocations.map(a => a.maxMarks));

  it('adds the single-booklet 2017 Ordinary paper with no earlier card and no route', () => {
    expect(authored.filter(card => card.year === 2017 && card.level === 'ordinary')).toHaveLength(0);
    expect(y2017).toHaveLength(68);
    expect(routePools.pools.some(pool => pool.template.year === 2017 && pool.template.level === 'ordinary')).toBe(false);
    for (const card of y2017) {
      expect(card.paperFileid, card.id).toBe('LC033GLP000EV');
      expect(card.rubric.schemeFileid, card.id).toBe('LC033GLP000EV');
      expect(tariffReconciles(card), card.id).toBe(true);
      expect(card.questionText, card.id).not.toContain('on the job training');
    }
  });

  it('preserves every Section 1 boundary at 10 marks with the summary sequences and keys', () => {
    const cohort = y2017.filter(card => card.section === '1');
    expect(cohort).toHaveLength(15);
    for (let q = 1; q <= 15; q++) expect(cohort.filter(card => qOf(card) === String(q)).map(card => card.totalMarks), String(q)).toEqual([10]);
    for (const [q, steps, key] of [
      [2, [0, 4, 7, 10], 'Consent to contract'], [4, [0, 4, 7, 10], 'Product, Promotion and Place'], [8, [0, 4, 7, 10], 'Membership of Travelling Community'],
      [10, [0, 4, 7, 9, 10], 'The Zip Yard Franchise'], [12, [0, 5, 10], 'European Court of Auditors'],
      [14, [0, 2, 4, 6, 8, 10], 'FALSE; TRUE; TRUE; FALSE; FALSE'], [15, [0, 2, 4, 6, 8, 10], '1 E; 2 F; 3 D; 4 B; 5 C'],
    ] as const) {
      const card = find(`bus-2017-ol-s1-q${q}`);
      expect(card.rubric.responses[0].allocations[0].permittedMarks, String(q)).toEqual(steps);
      expect(card.rubric.guidance.join(' '), String(q)).toContain(key);
    }
    expect(maxes('bus-2017-ol-s1-q1')).toEqual([[3], [3], [4]]);
    expect(maxes('bus-2017-ol-s1-q3')).toEqual([[3, 2], [3, 1, 1]]);
    expect(maxes('bus-2017-ol-s1-q6')).toEqual([[4, 1], [4, 1]]);
    expect(find('bus-2017-ol-s1-q11').rubric.responses[0].allocations[0].permittedMarks).toEqual([0, 10]);
  });

  it.each([1, 2, 3, 4, 5, 6, 7, 8])('preserves 2017 Ordinary Section 2 Q%i at 75 marks', q => {
    const cohort = y2017.filter(card => card.section === '2' && qOf(card) === String(q));
    expect(cohort.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(75);
  });

  it('keeps the published splits, the AGM notice and the diagram tariffs', () => {
    expect(find('bus-2017-ol-s2-q1b').rubric.responses[0].allocations[0].permittedMarks).toEqual([0, 2, 4, 6, 8, 10]);
    expect(maxes('bus-2017-ol-s2-q1c')).toEqual([[6, 2], [6, 2], [2, 2]]);
    expect(maxes('bus-2017-ol-s2-q4cii')).toEqual([[3, 2], [2, 1]]);
    expect(maxes('bus-2017-ol-s2-q4e')).toEqual([[2, 2, 2, 2], [2, 2, 2, 2, 2], [1, 1]]);
    expect(maxes('bus-2017-ol-s2-q5e')).toEqual([[3, 3], [3, 3], [2, 1]]);
    expect(maxes('bus-2017-ol-s2-q7bii')).toEqual([[1, 1, 1, 2, 2, 2, 2, 2, 2]]);
    expect(maxes('bus-2017-ol-s2-q7ci')).toEqual([[5, 5]]);
    expect(maxes('bus-2017-ol-s2-q7cii')).toEqual([[5, 5]]);
    expect(maxes('bus-2017-ol-s2-q7d')).toEqual([[3, 3, 2], [3, 2, 2]]);
    expect(find('bus-2017-ol-s2-q8d').rubric.responses[0].allocations[0].permittedMarks).toEqual([0, 2, 4, 6, 8, 10]);
  });

  it('keeps each printed choice marked alike as one card carrying every item', () => {
    for (const [id, slots, items] of [
      ['bus-2017-ol-s2-q1a', [[10, 5], [4, 1]], ['False or misleading advertising', 'False prices', 'False product descriptions']],
      ['bus-2017-ol-s2-q6a', [[8, 4], [3, 1], [3, 1]], ['Prototype Development', 'Feasibility Study', 'Test Marketing', 'Launch']],
    ] as const) {
      const choice = find(id);
      expect(maxes(id), id).toEqual(slots);
      for (const item of items) {
        expect(choice.questionText.toLowerCase(), `${id} ${item}`).toContain(item.toLowerCase());
        expect(choice.rubric.guidance.filter(line => line.startsWith(`${item} (scheme PDF page `)), `${id} ${item}`).toHaveLength(1);
      }
    }
  });

  it('files the 2017 Ordinary booklet in Topic Atlas with single-booklet identities', () => {
    for (const card of y2017) {
      const n = card.section === '1' ? qOf(card) : `S2Q${qOf(card)}`;
      const nodes = examTopicIdsForQuestion('business', 'ordinary', 2017, 'main', n, 'single').flatMap(curriculumNodeIdsForExamTopic);
      for (const topic of [card.topicId, ...(card.additionalTopicIds ?? [])]) {
        expect(nodes, card.id).toContain(topic);
        expect(cardsForTopic(topic, ordinaryRubrics), card.id).toContain(card);
      }
    }
  });
});

describe('Business 2018 Ordinary full paper', () => {
  const ordinaryRubrics = ORDINARY.filter(isRubricCard).filter(card => card.rubric.system === 'business');
  const y2018 = ordinaryRubrics.filter(card => card.year === 2018);
  const qOf = (card: { questionRef: string }) => card.questionRef.match(/ Q(\d+)/)![1];
  const find = (id: string) => {
    const card = ordinaryRubrics.find(item => item.id === id)!;
    if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
    return card as typeof card & { rubric: Extract<typeof card.rubric, { system: 'business' }> };
  };
  const maxes = (id: string) => find(id).rubric.responses.map(r => r.allocations.map(a => a.maxMarks));

  it('adds the single-booklet 2018 Ordinary paper with no earlier card and no route', () => {
    expect(authored.filter(card => card.year === 2018 && card.level === 'ordinary')).toHaveLength(0);
    expect(y2018).toHaveLength(64);
    expect(routePools.pools.some(pool => pool.template.year === 2018 && pool.template.level === 'ordinary')).toBe(false);
    for (const card of y2018) {
      expect(card.paperFileid, card.id).toBe('LC033GLP000EV');
      expect(card.rubric.schemeFileid, card.id).toBe('LC033GLP000EV');
      expect(tariffReconciles(card), card.id).toBe(true);
    }
  });

  it('preserves every Section 1 boundary at 10 marks with the summary sequences and keys', () => {
    const cohort = y2018.filter(card => card.section === '1');
    expect(cohort).toHaveLength(15);
    for (let q = 1; q <= 15; q++) expect(cohort.filter(card => qOf(card) === String(q)).map(card => card.totalMarks), String(q)).toEqual([10]);
    for (const [q, steps, key] of [
      [2, [0, 2, 4, 6, 8, 10], 'Sony Intrapreneur'], [5, [0, 4, 7, 10], '2. Weaknesses 3. Opportunities 4. Threats'],
      [7, [0, 3, 6, 8, 10], 'FALSE; TRUE; TRUE; FALSE'], [12, [0, 4, 7, 10], 'Land, Capital and Enterprise'],
      [13, [0, 4, 7, 10], 'Celebrity Endorsement'], [14, [0, 3, 6, 8, 10], 'vegan range in the next 6 months Tactical Plan'],
      [15, [0, 3, 6, 8, 9, 10], '1 E; 2 A; 3 F; 4 B; 5 D'],
    ] as const) {
      const card = find(`bus-2018-ol-s1-q${q}`);
      expect(card.rubric.responses[0].allocations[0].permittedMarks, String(q)).toEqual(steps);
      expect(card.rubric.guidance.join(' '), String(q)).toContain(key);
    }
    expect(maxes('bus-2018-ol-s1-q1')).toEqual([[4], [3], [3]]);
    expect(maxes('bus-2018-ol-s1-q4')).toEqual([[5, 5]]);
    expect(find('bus-2018-ol-s1-q4').rubric.guidance.join(' ')).toContain('The card follows the summary');
    expect(maxes('bus-2018-ol-s1-q6')).toEqual([[2, 1, 2, 1, 2, 2]]);
    expect(maxes('bus-2018-ol-s1-q9')).toEqual([[2, 1, 2, 1, 2, 1, 1]]);
    expect(maxes('bus-2018-ol-s1-q10')).toEqual([[4, 3, 3]]);
  });

  it.each([1, 2, 3, 4, 5, 6, 7, 8])('preserves 2018 Ordinary Section 2 Q%i at 75 marks', q => {
    const cohort = y2018.filter(card => card.section === '2' && qOf(card) === String(q));
    expect(cohort.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(75);
  });

  it('keeps the printed sub-part splits, the calculations and the channel templates', () => {
    expect(maxes('bus-2018-ol-s2-q1c')).toEqual([[3], [3, 3], [6]]);
    expect(find('bus-2018-ol-s2-q1c').rubric.guidance.join(' ')).toContain('the card follows it');
    expect(maxes('bus-2018-ol-s2-q2ai')).toEqual([[5]]);
    expect(maxes('bus-2018-ol-s2-q2aii')).toEqual([[2, 2, 2, 4]]);
    expect(maxes('bus-2018-ol-s2-q2c')).toEqual([[5, 2], [5, 2], [5, 1]]);
    expect(maxes('bus-2018-ol-s2-q3ai')).toEqual([[2, 2, 2, 4]]);
    expect(maxes('bus-2018-ol-s2-q3b')).toEqual([[3, 2, 3], [2, 2, 3]]);
    expect([find('bus-2018-ol-s2-q3ci').totalMarks, find('bus-2018-ol-s2-q3cii').totalMarks]).toEqual([8, 7]);
    expect(find('bus-2018-ol-s2-q4di').rubric.responses[0].allocations[0].permittedMarks).toEqual([0, 2, 4, 6, 8, 10]);
    expect(maxes('bus-2018-ol-s2-q6b').map(r => r.reduce((a, b) => a + b, 0))).toEqual([10, 10]);
    expect(maxes('bus-2018-ol-s2-q6c')).toEqual([[3, 4, 2], [3, 6, 2]]);
    expect(find('bus-2018-ol-s2-q7d').rubric.responses[0].allocations[0].permittedMarks).toEqual([0, 2, 4, 6, 8, 10]);
    expect(find('bus-2018-ol-s2-q7d').rubric.guidance.join(' ')).toContain('(4m + 2m +4m) or (5 @ 2m)');
    expect(maxes('bus-2018-ol-s2-q8bi').flat().reduce((a, b) => a + b, 0) + maxes('bus-2018-ol-s2-q8bii').flat().reduce((a, b) => a + b, 0)).toBe(20);
  });

  it('keeps each printed choice marked alike as one card carrying every item', () => {
    for (const [id, slots, items] of [
      ['bus-2018-ol-s2-q5a', 4, ['Premium', 'No claims bonus', 'Loadings', 'Insurance policy', 'Policy excess']],
      ['bus-2018-ol-s2-q5d', 3, ['Salary', 'Benefit in kind', 'Person specification', 'Training']],
      ['bus-2018-ol-s2-q8c', 3, ['Share Capital/Equity Capital', 'Bank Overdraft', 'Leasing', 'Medium Term Loan']],
    ] as const) {
      const choice = find(id);
      expect(maxes(id), id).toEqual(Array.from({ length: slots }, () => [3, 2]));
      for (const item of items) {
        expect(choice.questionText.toLowerCase(), `${id} ${item}`).toContain(item.toLowerCase());
        expect(choice.rubric.guidance.filter(line => line.startsWith(`${item} (scheme PDF page `)), `${id} ${item}`).toHaveLength(1);
      }
    }
  });

  it('files the 2018 Ordinary booklet in Topic Atlas with single-booklet identities', () => {
    for (const card of y2018) {
      const n = card.section === '1' ? qOf(card) : `S2Q${qOf(card)}`;
      const nodes = examTopicIdsForQuestion('business', 'ordinary', 2018, 'main', n, 'single').flatMap(curriculumNodeIdsForExamTopic);
      for (const topic of [card.topicId, ...(card.additionalTopicIds ?? [])]) {
        expect(nodes, card.id).toContain(topic);
        expect(cardsForTopic(topic, ordinaryRubrics), card.id).toContain(card);
      }
    }
  });
});

describe('Business 2019 Ordinary full paper', () => {
  const ordinaryRubrics = ORDINARY.filter(isRubricCard).filter(card => card.rubric.system === 'business');
  const y2019 = ordinaryRubrics.filter(card => card.year === 2019);
  const qOf = (card: { questionRef: string }) => card.questionRef.match(/ Q(\d+)/)![1];
  const find = (id: string) => {
    const card = ordinaryRubrics.find(item => item.id === id)!;
    if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
    return card as typeof card & { rubric: Extract<typeof card.rubric, { system: 'business' }> };
  };

  it('adds the single-booklet 2019 Ordinary paper with no earlier card and no route', () => {
    expect(authored.filter(card => card.year === 2019 && card.level === 'ordinary')).toHaveLength(0);
    expect(y2019).toHaveLength(72);
    expect(routePools.pools.some(pool => pool.template.year === 2019 && pool.template.level === 'ordinary')).toBe(false);
    for (const card of y2019) {
      expect(card.paperFileid, card.id).toBe('LC033GLP000EV');
      expect(card.rubric.schemeFileid, card.id).toBe('LC033GLP000EV');
      expect(tariffReconciles(card), card.id).toBe(true);
    }
  });

  it('preserves every Section 1 boundary at 10 marks with the summary sequences and keys', () => {
    const cohort = y2019.filter(card => card.section === '1');
    expect(cohort).toHaveLength(15);
    for (let q = 1; q <= 15; q++) expect(cohort.filter(card => qOf(card) === String(q)).map(card => card.totalMarks), String(q)).toEqual([10]);
    for (const [q, steps, key] of [
      [2, [0, 5, 10], 'Premium Pricing: Product B'], [6, [0, 4, 7, 9, 10], '(iv) do not'], [8, [0, 4, 7, 10], 'does not consult Autocratic'],
      [9, [0, 5, 10], 'Retailer Consumer'], [12, [0, 3, 6, 8, 10], 'A GM Self-Driving Car'], [13, [0, 3, 6, 8, 10], 'TRUE; FALSE; FALSE; TRUE'],
      [15, [0, 3, 6, 8, 9, 10], '1 D; 2 C; 3 A; 4 B; 5 F'],
    ] as const) {
      const card = find(`bus-2019-ol-s1-q${q}`);
      expect(card.rubric.responses[0].allocations[0].permittedMarks, String(q)).toEqual(steps);
      expect(card.rubric.guidance.join(' '), String(q)).toContain(key);
    }
    expect(find('bus-2019-ol-s1-q4').rubric.responses.map(r => r.allocations[0].maxMarks)).toEqual([6, 4]);
    expect(find('bus-2019-ol-s1-q4').rubric.guidance.join(' ')).toContain('The card follows the summary');
    expect(find('bus-2019-ol-s1-q5').rubric.responses[0].allocations.map(a => a.maxMarks)).toEqual([2, 1, 2, 1, 2, 1, 1]);
    expect(find('bus-2019-ol-s1-q11').rubric.responses[0].allocations.map(a => a.maxMarks)).toEqual([3, 4, 3]);
    expect(find('bus-2019-ol-s1-q14').rubric.responses.map(r => r.allocations.map(a => a.maxMarks))).toEqual([[2, 2], [2, 1], [2, 1]]);
  });

  it.each([1, 2, 3, 4, 5, 6, 7, 8])('preserves 2019 Ordinary Section 2 Q%i at 75 marks', q => {
    const cohort = y2019.filter(card => card.section === '2' && qOf(card) === String(q));
    expect(cohort.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(75);
  });

  it('keeps the calculations, the chart grid and the one-card sources-of-finance choice', () => {
    expect(find('bus-2019-ol-s2-q1ai').rubric.responses[0].allocations[0].permittedMarks).toEqual([0, 2, 4, 6, 8, 10]);
    expect(find('bus-2019-ol-s2-q2a').rubric.responses[0].allocations).toHaveLength(13);
    expect(find('bus-2019-ol-s2-q3di').rubric.responses[0].allocations.map(a => a.maxMarks)).toEqual([2, 2, 2, 4]);
    expect(find('bus-2019-ol-s2-q4e').rubric.responses[0].allocations.map(a => a.maxMarks)).toEqual([1, 1, 1, 3, 3, 3, 3]);
    expect(find('bus-2019-ol-s2-q5ei').rubric.responses[0].allocations.map(a => a.maxMarks)).toEqual([2, 3, 3, 2]);
    expect(find('bus-2019-ol-s2-q5eii').rubric.responses[0].allocations.map(a => a.maxMarks)).toEqual([3, 3, 4]);
    expect(find('bus-2019-ol-s2-q6bii').rubric.responses.map(r => r.label)).toEqual(['Primary research', 'Secondary research']);
    const choice = find('bus-2019-ol-s2-q7c');
    expect(choice.rubric.responses.map(r => r.allocations.map(a => a.maxMarks))).toEqual([[4, 4], [4, 4], [2, 2]]);
    for (const item of ['Bank overdraft', 'Trade credit', 'Hire-purchase', 'Grant', 'Long term loan']) {
      expect(choice.questionText.toLowerCase()).toContain(item.toLowerCase());
      expect(choice.rubric.guidance.filter(line => line.startsWith(`${item} (scheme PDF page `))).toHaveLength(1);
    }
  });

  it('files the 2019 Ordinary booklet in Topic Atlas with single-booklet identities', () => {
    for (const card of y2019) {
      const n = card.section === '1' ? qOf(card) : `S2Q${qOf(card)}`;
      const nodes = examTopicIdsForQuestion('business', 'ordinary', 2019, 'main', n, 'single').flatMap(curriculumNodeIdsForExamTopic);
      for (const topic of [card.topicId, ...(card.additionalTopicIds ?? [])]) {
        expect(nodes, card.id).toContain(topic);
        expect(cardsForTopic(topic, ordinaryRubrics), card.id).toContain(card);
      }
    }
  });
});

describe('Business 2020 Ordinary full paper', () => {
  const ordinaryRubrics = ORDINARY.filter(isRubricCard).filter(card => card.rubric.system === 'business');
  const y2020 = ordinaryRubrics.filter(card => card.year === 2020);
  const qOf = (card: { questionRef: string }) => card.questionRef.match(/ Q(\d+)/)![1];
  const find = (id: string) => {
    const card = ordinaryRubrics.find(item => item.id === id)!;
    if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
    return card as typeof card & { rubric: Extract<typeof card.rubric, { system: 'business' }> };
  };

  it('adds the 2020 Ordinary paper with no earlier card to preserve and no route', () => {
    expect(authored.filter(card => card.year === 2020 && card.level === 'ordinary')).toHaveLength(0);
    expect(y2020).toHaveLength(67);
    expect(routePools.pools.some(pool => pool.template.year === 2020 && pool.template.level === 'ordinary')).toBe(false);
    for (const card of y2020) {
      expect(card.paperFileid, card.id).toBe(card.section === '1' ? 'LC033GLP032EV' : 'LC033GLP033EV');
      expect(card.rubric.schemeFileid, card.id).toBe('LC033GLP000EV');
      expect(tariffReconciles(card), card.id).toBe(true);
    }
  });

  it('preserves every Section 1 boundary at 10 marks with the published keys and row marks', () => {
    const cohort = y2020.filter(card => card.section === '1');
    expect(cohort).toHaveLength(15);
    for (let q = 1; q <= 15; q++) expect(cohort.filter(card => qOf(card) === String(q)).map(card => card.totalMarks), String(q)).toEqual([10]);
    for (const [q, steps, key] of [
      [2, [0, 4, 7, 10], '(i) Batch (ii) Job (iii) Mass'], [4, [0, 4, 7, 10], 'drafts all laws European Commission'],
      [5, [0, 2, 4, 6, 8, 10], 'Field; Field; Desk; Field; Desk'], [6, [0, 3, 6, 8, 10], '(iv) more expensive'],
      [7, [0, 3, 6, 8, 10], 'Lidl Loss Leader'], [8, [0, 5, 10], 'A takeover ... a merger'], [10, [0, 4, 7, 10], 'NORMING'],
      [12, [0, 3, 6, 8, 10], 'True; True; False; True'], [13, [0, 4, 7, 10], 'Workplace Relations Commission (WRC)'],
      [14, [0, 3, 6, 8, 10], '3. Concept Development'], [15, [0, 2, 4, 6, 8, 10], '1 F; 2 C; 3 A; 4 B; 5 D'],
    ] as const) {
      const card = find(`bus-2020-ol-s1-q${q}`);
      expect(card.rubric.responses[0].allocations[0].permittedMarks, String(q)).toEqual(steps);
      expect(card.rubric.guidance.join(' '), String(q)).toContain(key);
    }
    expect(find('bus-2020-ol-s1-q1').rubric.responses.map(r => r.allocations[0].maxMarks)).toEqual([4, 3, 3]);
    expect(find('bus-2020-ol-s1-q11').rubric.responses[0].allocations.map(a => a.maxMarks)).toEqual([3, 3, 2, 2]);
    expect(find('bus-2020-ol-s1-q11').questionText).toContain('(40% of €24,700) 9,880');
  });

  it.each([1, 2, 3, 4, 5, 6, 7, 8])('preserves 2020 Ordinary Section 2 Q%i at 75 marks', q => {
    const cohort = y2020.filter(card => card.section === '2' && qOf(card) === String(q));
    expect(cohort.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(75);
  });

  it('keeps the calculations, the named items and the one-card principle choice', () => {
    expect(find('bus-2020-ol-s2-q1a').rubric.responses[0].allocations[0].permittedMarks).toEqual([0, 4, 7, 10]);
    expect(find('bus-2020-ol-s2-q1b').rubric.responses.map(r => r.allocations.map(a => a.maxMarks))).toEqual([[4, 4], [4, 3]]);
    expect(find('bus-2020-ol-s2-q2c').rubric.responses.map(r => r.label)).toEqual(['Land', 'Labour', 'Capital', 'Enterprise']);
    expect(find('bus-2020-ol-s2-q3bi').rubric.responses[0].allocations.map(a => a.maxMarks)).toEqual([1, 1, 1, 2]);
    expect(find('bus-2020-ol-s2-q3ci').rubric.responses[0].allocations.map(a => a.maxMarks)).toEqual([3, 2, 2, 3]);
    expect(find('bus-2020-ol-s2-q6di').rubric.responses.map(r => r.label)).toEqual(['Salary', 'Wage']);
    expect(find('bus-2020-ol-s2-q6dii').rubric.responses.map(r => r.allocations.map(a => a.maxMarks))).toEqual([[3, 3], [2, 2]]);
    expect(find('bus-2020-ol-s2-q7a').rubric.responses.map(r => r.allocations.map(a => a.maxMarks))).toEqual([[4, 3], [4, 3], [3, 3]]);
    const choice = find('bus-2020-ol-s2-q5aii');
    for (const item of ['Indemnity', 'Utmost Good Faith']) {
      expect(choice.questionText).toContain(item);
      expect(choice.rubric.guidance.filter(line => line.startsWith(`${item} (scheme PDF page `))).toHaveLength(1);
    }
    expect(choice.rubric.responses.map(r => r.label)).toEqual(['The principle you chose']);
  });

  it('files both 2020 Ordinary booklets in Topic Atlas', () => {
    for (const card of y2020) {
      const nodes = examTopicIdsForQuestion('business', 'ordinary', 2020, 'main', qOf(card), card.section === '1' ? 'p1' : 'p2')
        .flatMap(curriculumNodeIdsForExamTopic);
      for (const topic of [card.topicId, ...(card.additionalTopicIds ?? [])]) {
        expect(nodes, card.id).toContain(topic);
        expect(cardsForTopic(topic, ordinaryRubrics), card.id).toContain(card);
      }
    }
  });
});

describe('Business printed choices are one card each (choice is not a route)', () => {
  const all = [...HIGHER, ...ORDINARY].filter(isRubricCard).filter(card => card.rubric.system === 'business');
  const find = (id: string) => {
    const card = all.find(item => item.id === id)!;
    if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
    return card as typeof card & { rubric: Extract<typeof card.rubric, { system: 'business' }> };
  };
  const ordinal = ['First', 'Second', 'Third', 'Fourth'];

  it.each([
    ["bus-2014-hl-s3-q1c", ["Merchantable Quality", "Guarantees", "Signs limiting consumer rights", "Unsolicited Goods"], [[2, 2, 3], [4, 3], [4, 2]]],
    ["bus-2014-hl-s3-q3c", ["European Monetary Union (EMU)", "European Union Competition Policy", "European Social Charter"], [[4, 4, 2], [4, 4, 2]]],
    ["bus-2015-hl-s3-q5b-ii", ["Feasibility Study", "Test Marketing", "Product Screening", "Prototype Development"], [[2, 3], [2, 3], [2, 3]]],
    ["bus-2016-hl-s3-q2c", ["Investors", "Employees", "Suppliers", "Customers", "Government"], [[3, 3], [3, 3], [2, 2], [2, 2]]],
    ["bus-2020-hl-s3-q1b", ["Services", "Guarantees", "Signs limiting consumer rights", "Merchantable Quality"], [[4, 3], [4, 3], [3, 3]]],
    ["bus-2021-hl-s3-q3c", ["The Common Agricultural Policy", "The Competition Policy", "The European Union Social Charter"], [[2, 2, 2, 2, 2], [2, 2, 2, 2, 2]]],
    ["bus-2022-ol-s2-q4c", ["Offer and Acceptance (Agreement)", "Capacity to Contract", "Consideration", "Consent to Contract"], [[3, 2], [3, 2], [3, 2]]],
    ["bus-2022-ol-s2-q6ai", ["Medium Term Loan", "Hire Purchase", "Leasing"], [[4, 3], [4, 3]]],
    ["bus-2022-hl-s3-q6c", ["Corporation Tax", "PAYE", "Capital Gains Tax", "Local Property Tax (LPT)"], [[4, 3], [4, 3], [3, 3]]],
    ["bus-2022-hl-s3-q8c", ["Persuasive advertising", "Informative advertising", "Generic advertising", "Competitive advertising"], [[4, 3], [4, 3], [3, 3]]],
    ["bus-2023-ol-s2-q1e", ["Frustration", "Breach", "Agreement", "Performance"], [[4, 3], [4, 3], [4, 2]]],
    ["bus-2023-ol-s2-q9d", ["Feasibility Study", "Prototype Development", "Test Marketing"], [[4, 4], [4, 3]]],
    ["bus-2024-ol-s2-q3c", ["Quota", "Tariff", "Embargo", "Subsidies"], [[4, 3], [4, 3], [4, 2]]],
    ["bus-2024-ol-s2-q4c", ["False or misleading advertising", "False product descriptions", "False pricing"], [[7, 3], [4, 1]]],
    ["bus-2024-ol-s2-q4e", ["Consideration", "Capacity to Contract", "Consent to Contract", "Legality of Purpose"], [[4, 3], [4, 3], [4, 2]]],
    ["bus-2024-ol-s2-q6c", ["Utmost good faith", "Insurable interest", "Indemnity"], [[6, 4], [6, 4]]],
    ["bus-2024-ol-s2-q7b", ["Manpower Planning", "Training and Development", "Performance Appraisal"], [[7, 3], [4, 1]]],
    ["bus-2024-ol-s2-q9e", ["Grant", "Long-term Loan", "Share Capital"], [[4, 4], [4, 3]]],
    ["bus-2024-hl-s3-q7ci", ["Liquidity", "Profit and Loss Account", "Debtors", "Dividends"], [[2, 3], [2, 3], [2, 3]]],
    ["bus-2024-hl-s3-q8biii", ["Rolex watches", "Adare Manor Hotel and Golf Resort", "Prime Hydration drinks"], [[3, 3], [3, 2]]],
    ["bus-2025-ol-s2-q1a", ["Goods must be of merchantable quality", "Goods must be fit for purpose", "Goods must be as described", "Goods must conform to sample"], [[7, 3], [4, 1]]],
    ["bus-2025-ol-s2-q2d", ["Excise Duty", "VAT", "Carbon Tax"], [[7, 3], [4, 1]]],
    ["bus-2025-ol-s2-q9-d", ["Insurance premiums", "Motor insurance", "Public liability insurance", "Employer PRSI"], [[4, 1], [4, 1], [4, 1]]],
    ["bus-2025-ol-s2-q9e", ["Insurable interest", "Indemnity", "Utmost good faith"], [[7, 3], [4, 1]]],
    ["bus-2026-ol-s2-q8b", ["Feasibility Study", "Prototype Development", "Test Marketing"], [[7, 3], [4, 1]]],
    ["bus-2015-hl-s3-q4a-i", ["Bar chart", "Line graph"], [[1, 1, 1, 1, 1, 1, 2, 2, 2]]],
    ["bus-2022-hl-s3-q2a", ["A Private Company Limited by shares (LTD company)", "A Designated Activity Company (DAC)"], [[3, 3, 3, 3, 3, 3, 2]]],
    ["bus-2023-ol-s2-q6e", ["Assessors", "Actuaries"], [[5, 5]]],
    ["bus-2024-hl-s3-q3cii", ["Common Agricultural Policy", "EU Social Policy", "EU Competition Policy"], [[2, 3, 2, 3]]],
    ["bus-2025-ol-s2-q3e", ["European Parliament", "European Commission", "Council of the European Union"], [[10, 5]]],
    ["bus-2026-ol-s2-q3a", ["Bar Chart", "Line Graph"], [[1, 2, 2, 2, 2, 2, 2, 2]]],
  ] as const)('%s prints every item, marks each chosen slot and quotes the scheme for every item', (id, items, marks) => {
    const card = find(id);
    expect(tariffReconciles(card)).toBe(true);
    expect(card.totalMarks).toBe(marks.flat().reduce((sum, mark) => sum + mark, 0));
    expect(card.rubric.responses.map(r => r.allocations.map(a => a.maxMarks))).toEqual(marks);
    card.rubric.responses.forEach((response, i) => expect(response.label)
      .toMatch(new RegExp(`^${card.rubric.responses.length === 1 ? 'The' : ordinal[i]} .+ you chose$`)));
    expect(card.rubric.guidance[0]).toContain('The scheme marks every choice alike');
    for (const item of items) {
      expect(card.questionText.toLowerCase(), item).toContain(item.toLowerCase());
      expect(card.rubric.guidance.filter(line => line.startsWith(`${item} (scheme PDF page `)), item).toHaveLength(1);
    }
    expect(all.filter(other => other.id.startsWith(`${id}-`))).toEqual([]);
    expect(routePools.pools.some(pool => pool.id === id
      || (pool as { legacyRoute?: { id: string } }).legacyRoute?.id === id)).toBe(false);
    const reviews = Object.values(selectionReviews.reviews as Record<string, { classification: string; cardId?: string }>)
      .filter(review => review.cardId === id);
    expect(reviews.length).toBeGreaterThan(0);
    expect(reviews.every(review => review.classification === 'finite-choice')).toBe(true);
  });

  it('routes only the printed choice whose routes the scheme marks differently', () => {
    expect(routePools.pools.map(pool => [pool.id, pool.choose])).toEqual([['bus-2013-hl-s3-q1b', 2]]);
    // 2013 Q1(B): one approach is marked 2 + 2 + 2 + 2 + 2, the other two 4 + 4 + 2.
    const shapes = routePools.pools[0].options.map(option => option.response!.allocations.map(a => a.maxMarks));
    expect(shapes).toEqual([[2, 2, 2, 2, 2], [4, 4, 2], [4, 4, 2]]);
  });
});

describe('Business ABQ scoring and source reader', () => {
  it('awards the case link only when the same response contains relevant theory', () => {
    const link = businessScoreId('response-1', 'link');
    const theory = businessScoreId('response-1', 'explain');
    expect(businessMarks(enterprise, { [link]: 1 })).toBe(0);
    expect(businessMarks(enterprise, { [link]: 1, [theory]: 2 })).toBe(3);
    expect(businessMarks(enterprise, { [link]: 1,
      [businessScoreId('response-2', 'explain')]: 2 })).toBe(2);
  });

  it('respects component limits and uses the same scoring path as the session', () => {
    for (const card of businessRubrics) {
      if (card.rubric.system !== 'business') throw new Error('Wrong rubric');
      const scores: BusinessScores = {};
      for (const response of card.rubric.responses) {
        for (const allocation of response.allocations) {
          scores[businessScoreId(response.id, allocation.id)] = 999;
        }
      }
      expect(businessMarks(card, scores)).toBe(card.totalMarks);
      expect(rubricMarks(card, scores)).toBe(card.totalMarks);
    }
    expect(businessMarks(enterprise, { [businessScoreId('response-1', 'explain')]: NaN })).toBe(0);
    expect(businessMarks(enterprise, { [businessScoreId('response-1', 'explain')]: -2 })).toBe(0);
  });

  it('keeps the official answers behind reveal and opens the scheme storage path', async () => {
    render(<SessionScreen cards={[enterprise]} subjectLabel="Business"
      onGrade={vi.fn()} onFinish={vi.fn()} onExit={vi.fn()} />);
    expect(screen.getByRole('button', { name: /Read CASE STUDY/ })).toBeVisible();
    expect(screen.queryByRole('button', { name: /Read OFFICIAL MARKING SCHEME/ })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Reveal the marking scheme' }));
    const zero = screen.getByRole('button', { name: 'Set Skill or characteristic 1 Name to 0 marks' });
    expect(zero).toHaveAttribute('aria-pressed', 'false');
    fireEvent.click(zero);
    expect(zero).toHaveAttribute('aria-pressed', 'true');
    const source = await screen.findByRole('button', { name: /Read OFFICIAL MARKING SCHEME/ });
    fireEvent.click(source);
    await waitFor(() => expect(vaultPdf).toHaveBeenCalledWith(expect.stringContaining('%2Fscheme%2FLC033ALP000EV.pdf')));
    expect(screen.getByRole('dialog')).toBeVisible();
    fireEvent.click(screen.getByRole('button', { name: 'Close marking scheme' }));
    await waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument());
  });
});
