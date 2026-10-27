/** @license SPDX-License-Identifier: Apache-2.0 */
import { describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { CARDS } from '../components/MarkBank/cards/accounting/higher';
import { CARDS as ORDINARY } from '../components/MarkBank/cards/accounting/ordinary';
import authored from '../components/MarkBank/cards/accounting/authored.json';
import reviewed2025 from '../scripts/markbank/accounting/reviewed/2025-higher.json';
import SessionScreen, { rubricMarks } from '../components/MarkBank/SessionScreen';
import { accountingMark } from '../components/MarkBank/AccountingAssessment';
import { accountingCardsForLevel } from '../components/MarkBank/cards/accounting/factory';
import { deckSize, loadCards } from '../components/MarkBank/deck';
import { questionsForTopics } from '../components/PaperTrail/topics';
import { examTopicIdsForQuestion } from '../data/examTopics/registry';
import { paperRegionFor, schemeRegionFor } from '../components/PaperTrail/paperRegion';
import { resolveSibling, hostedAnswersUrl } from '../components/PaperTrail/vaultResolve';
import { tariffReconciles } from '../types/markBank';
import type { PaperAnswerMap } from '../types/paperTrail';
import { vaultPdf } from '../components/PaperTrail/vaultDocs';
import { rotatedCropRect } from '../components/PaperTrail/CropView';
import { reviewedArchiveEntries } from '../components/PaperTrail/indexLookup';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
import inventory from '../scripts/markbank/accounting/inventory.json';
import progress from '../scripts/markbank/accounting/progress.json';
import reconciliation from '../scripts/markbank/accounting/reconciliation.json';

vi.mock('../components/PaperTrail/vaultDocs', () => ({ vaultPdf: vi.fn(() => new Promise(() => {})) }));

const current = CARDS.filter(card => card.year === 2025);
const json = (path: string) => JSON.parse(readFileSync(resolve(__dirname, '..', path), 'utf8'));
const map = json('public/paper-answers/2025/LC032ALP000EV.pdf.json') as PaperAnswerMap;
const original = json('scripts/paper-trail/answers/2025/LC032ALP000EV.pdf.json') as PaperAnswerMap;

describe('Accounting corpus reconciliation', () => {
  it('covers the actual Paper Trail index without unreviewed or orphan editions', () => {
    // The reviewed window: June sittings 2010-2026 (pre-2010 and deferred
    // papers are archive-only).
    const indexed = reviewedArchiveEntries('accounting').flatMap(entry => entry.papers.map(paper => `${entry.year}/${paper.doc.f}`));
    expect(new Set(inventory.papers.map(paper => `${paper.year}/${paper.fileid}`))).toEqual(new Set(indexed));
    expect(progress.editions.filter(edition => edition.status === 'pending')).toEqual([]);
    expect(reconciliation.sourceReconciliationPassed).toBe(true);
    expect(reconciliation.openIssues).toEqual([]);
    expect(reconciliation.logicalTasks).toBe(authored.cards.length);
  });

  it('preserves every old Atlas question and exposes only reviewed additions', () => {
    const atlas = questionsForTopics('accounting', null);
    const identity = (year: number, level: string, n: string) => `${year}|${level}|${n}`;
    const old = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'accounting')
      .flatMap(paper => paper.q.map(q => identity(paper.year, paper.level, q.n)));
    // Existing Atlas supplementation also draws parents from the audited
    // answer sidecars; the frozen canonical tag file is only one input.
    const originalParents = inventory.papers.flatMap(paper => {
      const path = `scripts/paper-trail/answers/${paper.year}/${paper.fileid}.json`;
      return existsSync(resolve(__dirname, '..', path))
        ? (json(path) as PaperAnswerMap).q.map(q => identity(paper.year, paper.level, q.n)) : [];
    });
    const expected = new Set([...old, ...originalParents, ...authored.cards.map(card => identity(card.year, card.level, card.taskKey))]);
    expect(new Set(atlas.map(q => identity(q.year, q.level, q.n)))).toEqual(expected);
    expect(atlas).toHaveLength(expected.size);
    for (const topic of new Set(authored.cards.flatMap(card => card.examTopicIds))) {
      const visible = new Set(questionsForTopics('accounting', [topic]).map(q => identity(q.year, q.level, q.n)));
      for (const card of authored.cards.filter(card => card.examTopicIds.includes(topic))) {
        expect(visible.has(identity(card.year, card.level, card.taskKey)), `${card.id} in ${topic}`).toBe(true);
      }
    }
  });

  it('keeps missing Irish schemes explicit and the translated concept choice as one task', () => {
    for (const level of ['higher', 'ordinary']) {
      const review = json(`scripts/markbank/accounting/correspondence/2020-${level}-irish.json`);
      expect(review.visualSchemePages).toEqual([]);
      expect(existsSync(resolve(__dirname, `../paper-trail-corpus/markingschemes/2020/${review.fileid}`))).toBe(false);
      expect(review.schemeFallback.fileid).toBe(review.fileid.replace('IV.pdf', 'EV.pdf'));
      expect(review.schemeFallback.visualSchemePages.length).toBeGreaterThan(0);
      expect(review.schemeFallback.reason).toBeTruthy();
    }
    const review = json('scripts/markbank/accounting/correspondence/2022-higher-irish.json');
    expect(review.selectionReview.filter((d: { classification: string }) => d.classification === 'closed-pool')
      .every((d: { englishTaskKey: string }) => d.englishTaskKey === '6(c)')).toBe(true);
    expect(review.taskCorrespondence.filter((t: { englishTaskKey: string }) => t.englishTaskKey.startsWith('6(c)')).map((t: { englishTaskKey: string }) => t.englishTaskKey)).toEqual(['6(c)']);
  });

  it('retains the translated pagination corrections found in the visual sweep', () => {
    const pages = (year: number, level: string, key: string) => json(`scripts/markbank/accounting/correspondence/${year}-${level}-irish.json`)
      .taskCorrespondence.find((t: { englishTaskKey: string }) => t.englishTaskKey === key)
      .schemeRegions.map((r: { p: number }) => r.p);
    expect(pages(2023, 'ordinary', '9(a)')).toEqual([21]);
    expect(pages(2025, 'ordinary', '5(b)(i)')).toEqual([13]);
    expect(pages(2025, 'higher', '7')).toEqual([24]);
    expect(pages(2026, 'higher', '2(b)')).toEqual([12, 13]);
    expect(pages(2026, 'higher', '8(e)(ii)')).toEqual([32]);
    expect(pages(2026, 'higher', '9(a)')).toEqual([33]);
  });
});

describe('reviewed 2025 Higher Accounting tasks (not a full-corpus completion claim)', () => {
  it('loads the registered deck and retains every reviewed task', async () => {
    expect(current).toHaveLength(41);
    expect(new Set(current.map(card => card.id)).size).toBe(41);
    expect(await loadCards('accounting', 'higher')).toEqual(CARDS);
    expect(deckSize('accounting', 'higher')).toBe(CARDS.length);
    expect(current.every(tariffReconciles)).toBe(true);
    expect(current.every(card => card.specVersion === 'accounting:outgoing')).toBe(true);
    expect(current.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(880);
  });

  it('keeps both Q1 routes and publishes only real subpart allocations', () => {
    for (const route of ['A', 'B']) {
      expect(current.filter(card => card.questionRef.includes(`Q1${route}`)).map(card => card.totalMarks)).toEqual([75, 45]);
    }
    expect(current.filter(card => card.questionRef.includes('Q5(a)')).map(card => card.totalMarks)).toEqual([12, 10, 8, 10, 10]);
    expect(current.filter(card => card.questionRef.includes('Q2(c)')).map(card => card.totalMarks)).toEqual([8]);
    expect(current.filter(card => card.questionRef.includes('Q9(d)')).map(card => card.totalMarks)).toEqual([11, 9]);
    expect(reviewed2025.tasks.every(task => task.boundaryReason.length > 0)).toBe(true);
  });

  it('makes every task reachable in Atlas under exactly its reviewed topic', () => {
    const atlas = questionsForTopics('accounting', null);
    for (const task of authored.cards) {
      const sibling = atlas.find(q => q.year === task.year && q.level === task.level && q.n === task.taskKey);
      expect(sibling, task.id).toBeDefined();
      expect(examTopicIdsForQuestion('accounting', task.level as 'higher' | 'ordinary', task.year, 'main',
        task.taskKey, 'single', 'ev', task.paperFileid)).toEqual(task.examTopicIds);
      const resolved = resolveSibling(sibling!);
      expect(resolved?.answersUrl).toBe(hostedAnswersUrl(task.year, task.paperFileid));
      const answerMap = json(`public/paper-answers/${task.year}/${task.paperFileid}.json`) as PaperAnswerMap;
      const q = answerMap.q.find(question => question.n === task.taskKey)!;
      expect(paperRegionFor(answerMap.q, q.n, answerMap.maxCropPages)?.map(region => region.p)).toEqual(task.paperPages);
      expect(schemeRegionFor(q)).toEqual(task.schemeRegions);
    }
  });

  it('preserves all legacy identities and fixes the rotated tabular-statement answer', () => {
    for (const old of original.q) {
      const updated = map.q.find(q => q.n === old.n)!;
      for (const field of ['n', 'pP', 'pY', 'region', 'mode', 'conf'] as const) expect(updated[field]).toEqual(old[field]);
    }
    expect(schemeRegionFor(map.q.find(q => q.n === '6')!).map(region => region.p)).toEqual([21, 22, 23, 24]);
    expect(schemeRegionFor(map.q.find(q => q.n === '7')!)[0]).toEqual({ p: 25, r: [0, 0, 1, 1] });
    expect(paperRegionFor(map.q, '1', map.maxCropPages)?.map(region => region.p)).toEqual([2, 3, 4, 5]);
  });

  it('retains trial balances, workings and the exact marking conventions', () => {
    for (const card of current) {
      expect(card.sourceMaterial?.kind).toBe('source-table');
      if (card.rubric.system !== 'accounting') throw new Error('Wrong assessment');
      expect(card.rubric.solution.kind).toBe('marking-scheme');
      expect(card.rubric.solution.pages).toContain(31);
      expect(card.rubric.solution.regions?.every(region => region.r[3] > region.r[1])).toBe(true);
    }
    expect(current[0].sourceMaterial?.pages).toEqual([2, 3]);
    expect(current[0].rubric.system === 'accounting' && current[0].rubric.solution.pages).toEqual([3, 5, 31]);
  });
});

describe('Accounting source reader and self-assessment', () => {
  it('turns sideways tables upright without changing which source area is shown', () => {
    const rect: [number, number, number, number] = [0, 0.25, 0.5, 1];
    expect(rotatedCropRect(rect, 90)).toEqual([0, 0, 0.75, 0.5]);
    expect(rotatedCropRect(rect, 180)).toEqual([0.5, 0, 1, 0.75]);
    expect(rotatedCropRect(rect, 270)).toEqual([0.25, 0.5, 1, 1]);
    expect(rotatedCropRect(rect, undefined)).toEqual(rect);
    const tabular = authored.cards.find(card => card.id === 'acc-2023-hl-q4')!;
    expect(tabular.schemeRegions[0]).toEqual({ p: 13, r: [0, 0, 1, 1], rotate: 90 });
    expect(tabular.schemeRegions.at(-1)).toEqual({ p: 33, r: [0, 0, 1, 1] });
  });

  it('bounds partial-credit scores, including restored invalid state', () => {
    expect(accountingMark(75, 74.5)).toBe(74.5);
    expect(accountingMark(75, 100)).toBe(75);
    expect(accountingMark(75, -2)).toBe(0);
    expect(accountingMark(75, Number.NaN)).toBe(0);
    expect(rubricMarks(current[0], { 'accounting:allocation': 74.5 })).toBe(74.5);
  });

  it('opens only the paper before reveal and keeps solutions behind reveal', async () => {
    vi.mocked(vaultPdf).mockClear();
    render(<SessionScreen cards={[current[0]]} subjectLabel="Accounting" onGrade={vi.fn()} onFinish={vi.fn()} onExit={vi.fn()} />);
    expect(screen.queryByRole('button', { name: /Open worked solution/ })).not.toBeInTheDocument();
    const dataButton = screen.getByRole('button', { name: /Open accounting data/ });
    fireEvent.click(dataButton);
    const dialog = screen.getByRole('dialog');
    expect(within(dialog).getByRole('button', { name: 'Next source page' })).toBeEnabled();
    expect(vi.mocked(vaultPdf).mock.calls.at(-1)?.[0]).toContain('%2Fpaper%2F');
    fireEvent.keyDown(dialog, { key: 'Escape' });
    await waitFor(() => expect(dataButton).toHaveFocus());
    fireEvent.click(screen.getByRole('button', { name: /Reveal/ }));
    const solutionButton = await screen.findByRole('button', { name: /Open worked solution/ });
    fireEvent.click(solutionButton);
    expect(vi.mocked(vaultPdf).mock.calls.at(-1)?.[0]).toContain('%2Fscheme%2F');
    fireEvent.click(screen.getByRole('button', { name: 'Close worked solution' }));
    // The task's scheme lines are rows the student claims (cards/accounting/rows.json); the stepper is gone.
    const rows = (current[0].rubric as Extract<typeof current[0]['rubric'], { system: 'accounting' }>).rows!;
    expect(screen.queryByRole('spinbutton', { name: 'Your marks out of 75' })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: `${rows[1].text} · ${rows[1].marks}m` }));
    expect(screen.getByText(`${rows[1].marks} of 75 marks claimed`, { exact: false })).toBeInTheDocument();
  });

  it('keeps the half-mark stepper on a task whose rows are in the residue', async () => {
    const card = [...accountingCardsForLevel('higher'), ...accountingCardsForLevel('ordinary')].find(candidate => candidate.rubric.system === 'accounting' && !candidate.rubric.rows?.length)!;
    render(<SessionScreen cards={[card]} subjectLabel="Accounting" onGrade={vi.fn()} onFinish={vi.fn()} onExit={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: /Reveal/ }));
    const score = await screen.findByRole('spinbutton', { name: `Your marks out of ${card.totalMarks}` });
    fireEvent.change(score, { target: { value: '4.5' } });
    expect(score).toHaveValue(4.5);
    fireEvent.click(screen.getByRole('button', { name: 'Add half a mark' }));
    expect(score).toHaveValue(5);
  });
});

describe('Accounting paper-specific allocations', () => {
  it('distinguishes correction tasks from suspense accounts in the canonical curriculum', () => {
    const errors = authored.cards.filter(card => ['accounting-2-3', 'accounting-2-4'].includes(card.topicId));
    expect(errors.length).toBeGreaterThan(0);
    for (const card of errors) {
      expect(card.topicId, card.id).toBe(card.title.toLowerCase().includes('suspense')
        ? 'accounting-2-3' : 'accounting-2-4');
    }
  });

  it.each([
    [2010, 'higher', 43], [2010, 'ordinary', 37],
    [2011, 'higher', 37], [2011, 'ordinary', 39],
    [2012, 'higher', 48], [2012, 'ordinary', 41],
    [2013, 'higher', 44], [2013, 'ordinary', 34],
    [2014, 'higher', 48], [2014, 'ordinary', 38],
    [2015, 'higher', 42], [2015, 'ordinary', 36],
    [2016, 'higher', 37], [2016, 'ordinary', 33],
    [2017, 'higher', 39], [2017, 'ordinary', 41],
    [2018, 'higher', 46], [2018, 'ordinary', 33],
    [2019, 'higher', 42], [2019, 'ordinary', 42],
    [2020, 'higher', 42], [2020, 'ordinary', 34],
    [2021, 'higher', 46], [2021, 'ordinary', 41],
    [2022, 'higher', 40], [2022, 'ordinary', 38],
    [2023, 'higher', 36], [2023, 'ordinary', 40],
    [2024, 'higher', 47], [2024, 'ordinary', 38],
    [2025, 'higher', 41], [2025, 'ordinary', 40],
    [2026, 'higher', 43], [2026, 'ordinary', 39],
  ] as const)('retains every reviewed task in %s %s', (year, level, count) => {
    const cards = [...CARDS, ...ORDINARY].filter(card => card.year === year && card.level === level);
    expect(cards).toHaveLength(count);
    expect(cards.every(tariffReconciles)).toBe(true);
    // A printed choice is one card, so every paper sums to its published total.
    expect(cards.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(year < 2021 ? 760 : 880);
    const byQuestion = cards.reduce<Record<string, number>>((totals, card) => {
      const n = card.questionRef.match(/Q(\d+)/)![1];
      totals[n] = (totals[n] ?? 0) + card.totalMarks;
      return totals;
    }, {});
    expect(byQuestion).toEqual({ 1: year < 2021 ? 120 : 240, 2: 60, 3: 60, 4: 60, 5: 100, 6: 100, 7: 100, 8: 80, 9: 80 });
  });

  it('retains the repeated 2010 acid-test requirement within its only published allocation', () => {
    const cards = authored.cards.filter(card => card.year === 2010 && card.level === 'ordinary');
    const liquidity = cards.find(card => card.taskKey === '5(a)(v)-and-5(c)')!;
    expect(liquidity.totalMarks).toBe(10);
    expect(liquidity.questionText).toContain('The Acid Test ratio.');
    expect(liquidity.questionText).toContain('Calculate these ratios for 2009.');
    expect(liquidity.questionText).toContain('Comment on the liquidity');
    expect(cards.filter(card => /^5\(a\)\([iv]+\)$/.test(card.taskKey)).map(card => card.totalMarks)).toEqual([10, 10, 10, 10]);
    expect(cards.find(card => card.taskKey === '2')!.schemeRegions[0]).toEqual({ p: 6, r: [0, 0, 1, 1], rotate: 270 });
  });

  it('uses the 2010 cash-flow allocations and keeps the 2011 graph with its explanation', () => {
    const cash = authored.cards.filter(card => card.year === 2010 && card.level === 'higher' && card.taskKey.startsWith('2(a)'));
    expect(cash.map(card => card.totalMarks)).toEqual([18, 26, 4]);
    const graph = authored.cards.find(card => card.id === 'acc-2011-hl-q8(f)(ii)')!;
    expect(graph.totalMarks).toBe(5);
    expect(graph.questionText).toContain('Explain what is meant by a step fixed cost.');
    expect(graph.questionText).toContain('Roughly sketch a graph');
    expect(graph.paperPages).toEqual([9]);
    expect(graph.schemeRegions[0].p).toBe(19);
  });

  it('keeps the 2022 Higher choose-two concept task as one ten-mark card', () => {
    // A printed choice is one card (AGENTS.md, 2026-10-12): the printed question,
    // the scheme's single 10-mark allocation, and all four concepts it explains.
    const family = authored.cards.filter(card => card.year === 2022 && card.level === 'higher' && card.taskKey.startsWith('6(c)'));
    expect(family.map(card => card.id)).toEqual(['acc-2022-hl-q6(c)']);
    const [card] = family;
    expect(card.totalMarks).toBe(10);
    expect(card.questionText).toBe('There are four fundamental accounting concepts applied in the preparation of accounts.\nExplain two fundamental accounting concepts, with reference to how they apply to the accounts of McSharry.');
    expect(card.taskFocus).toBeNull();
    expect(card.title).toBe('Fundamental accounting concepts');
    for (const concept of ['Going Concern', 'Accruals (matching)', 'Consistency', 'Prudence']) expect(card.allocationNote).toContain(concept);
    expect(card.paperPages).toEqual([12, 13]);
    expect(card.schemeRegions.map(region => region.p)).toEqual([27, 40]);
    expect(card.topicId).toBe('accounting-0-5');
  });

  it('never publishes a printed choice as route siblings', () => {
    // A printed task key appears once per paper edition, and no task key or
    // focus carries a route suffix in place of the printed question.
    const keys = authored.cards.map(card => `${card.year}|${card.level}|${card.taskKey}`);
    expect(keys.filter((key, index) => keys.indexOf(key) !== index)).toEqual([]);
    const reviewed = ['higher', 'ordinary'].flatMap(level => Array.from({ length: 17 }, (_, i) => 2010 + i)
      .map(year => json(`scripts/markbank/accounting/reviewed/${year}-${level}.json`)));
    const choices = reviewed.flatMap(review => review.tasks
      .filter((task: { printedChoice?: unknown }) => task.printedChoice)
      .map((task: { key: string }) => ({ review, key: task.key })));
    expect(reviewed.some(review => review.tasks.some((task: { selectionPool?: unknown }) => task.selectionPool))).toBe(false);
    expect(choices.map(({ review, key }) => `${review.year} ${review.level} ${key}`)).toEqual(['2022 higher 6(c)']);
    for (const { review, key } of choices) {
      const cards = authored.cards.filter(card => card.year === review.year && card.level === review.level &&
        (card.taskKey === key || card.taskKey.startsWith(`${key}-`)));
      expect(cards.map(card => card.taskKey)).toEqual([key]);
    }
  });

  it('keeps shared theory tariffs and continuous journals intact', () => {
    const allocations = (year: number, level: string, prefix: string) => authored.cards
      .filter(card => card.year === year && card.level === level && card.taskKey.startsWith(prefix))
      .map(card => card.totalMarks);
    expect(allocations(2012, 'higher', '2(')).toEqual([40, 14, 6]);
    expect(allocations(2012, 'higher', '3(')).toEqual([13, 18, 3, 4, 12, 2, 6, 2]);
    expect(allocations(2012, 'higher', '4(')).toEqual([20, 11, 9, 12, 5, 3]);
    expect(allocations(2012, 'higher', '5(')).toEqual([12, 8, 8, 12, 10, 35, 5, 10]);
    expect(allocations(2012, 'higher', '7(')).toEqual([18, 17, 48, 5, 12]);
    expect(allocations(2012, 'higher', '8(')).toEqual([29, 8, 4, 4, 5, 8, 16, 6]);
    expect(allocations(2012, 'higher', '9(')).toEqual([62, 13, 5]);
    expect(allocations(2012, 'ordinary', '4(')).toEqual([15, 9, 30, 6]);
    expect(allocations(2012, 'ordinary', '6(')).toEqual([10, 10, 10, 30, 40]);
    expect(allocations(2012, 'ordinary', '8(')).toEqual([12, 10, 10, 10, 15, 15, 8]);
    expect(allocations(2012, 'ordinary', '9(')).toEqual([16, 16, 16, 16, 10, 6]);
    expect(allocations(2013, 'higher', '4(')).toEqual([25, 25, 3, 7]);
    expect(allocations(2013, 'higher', '6(')).toEqual([40, 26, 19, 4, 4, 7]);
    expect(allocations(2013, 'higher', '8(')).toEqual([16, 14, 2, 2, 2, 30, 2, 2, 2, 6, 2]);
    expect(allocations(2013, 'higher', '9(')).toEqual([11, 13, 37, 15, 4]);
    expect(allocations(2013, 'ordinary', '1(')).toEqual([40, 40, 40]);
    expect(allocations(2013, 'ordinary', '8(')).toEqual([17, 15, 16, 16, 10, 6]);
    expect(allocations(2013, 'ordinary', '9(')).toEqual([75, 5]);
    expect(allocations(2014, 'higher', '2(')).toEqual([18, 28, 5, 6, 3]);
    expect(allocations(2014, 'higher', '3(')).toEqual([36, 15, 3, 6]);
    expect(allocations(2014, 'higher', '5(a)')).toEqual([12, 8, 10, 12, 8]);
    expect(allocations(2014, 'higher', '8(')).toEqual([10, 6, 8, 10, 12, 12, 7, 6, 6, 3]);
    expect(allocations(2014, 'higher', '9(')).toEqual([16, 20, 23, 13, 6, 2]);
    expect(allocations(2014, 'ordinary', '5(a)')).toEqual([10, 10, 4, 8, 8]);
    expect(allocations(2014, 'ordinary', '7(')).toEqual([30, 65, 5]);
    expect(allocations(2014, 'ordinary', '8(')).toEqual([14, 14, 12, 14, 12, 10, 4]);
    expect(allocations(2014, 'ordinary', '9(')).toEqual([58, 18, 4]);
    expect(allocations(2015, 'higher', '2(')).toEqual([6, 32, 14, 4, 4]);
    expect(allocations(2015, 'higher', '4(')).toEqual([20, 11, 9, 10, 5, 5]);
    expect(allocations(2015, 'higher', '5(a)')).toEqual([12, 10, 12, 8, 8]);
    expect(allocations(2015, 'higher', '6(')).toEqual([18, 20, 46, 4, 8, 4]);
    expect(allocations(2015, 'higher', '7(c)')).toEqual([4, 4]);
    expect(allocations(2015, 'higher', '8(')).toEqual([20, 14, 4, 8, 8, 20, 6]);
    expect(allocations(2015, 'higher', '9(')).toEqual([58, 14, 4, 4]);
    expect(allocations(2015, 'ordinary', '5(a)')).toEqual([40]);
    expect(allocations(2015, 'ordinary', '6(')).toEqual([30, 65, 5]);
    expect(allocations(2015, 'ordinary', '7(')).toEqual([10, 10, 10, 30, 40]);
    expect(allocations(2015, 'ordinary', '8(')).toEqual([10, 10, 10, 10, 24, 10, 6]);
    expect(allocations(2015, 'ordinary', '9(')).toEqual([16, 18, 16, 16, 10, 4]);
    expect(allocations(2016, 'higher', '2(')).toEqual([22, 30, 8]);
    expect(allocations(2016, 'higher', '5(a)')).toEqual([12, 10, 10, 9, 9]);
    expect(allocations(2016, 'higher', '7(a)')).toEqual([40, 26, 22]);
    expect(allocations(2016, 'higher', '8(')).toEqual([26, 8, 6, 6, 24, 10]);
    expect(allocations(2016, 'higher', '9(')).toEqual([11, 13, 34, 13, 9]);
    expect(allocations(2016, 'ordinary', '3(')).toEqual([35, 25]);
    expect(allocations(2016, 'ordinary', '5(a)')).toEqual([10, 10, 10, 10]);
    expect(allocations(2016, 'ordinary', '7(')).toEqual([27, 13, 25, 35]);
    expect(allocations(2016, 'ordinary', '8(')).toEqual([12, 12, 10, 10, 15, 17, 4]);
    expect(allocations(2016, 'ordinary', '9(')).toEqual([74, 6]);
    expect(allocations(2017, 'higher', '2(')).toEqual([18, 29, 5, 8]);
    expect(allocations(2017, 'higher', '3(')).toEqual([48, 4, 8]);
    expect(allocations(2017, 'higher', '4(')).toEqual([50, 10]);
    expect(allocations(2017, 'higher', '5(a)')).toEqual([12, 12, 10, 8, 8]);
    expect(allocations(2017, 'higher', '8(')).toEqual([8, 13, 5, 14, 14, 9, 9, 2, 6]);
    expect(allocations(2017, 'higher', '9(')).toEqual([12, 18, 23, 12, 9, 6]);
    expect(allocations(2017, 'ordinary', '1(')).toEqual([40, 40, 40]);
    expect(allocations(2017, 'ordinary', '4(')).toEqual([35, 25]);
    expect(allocations(2017, 'ordinary', '5(a)')).toEqual([12, 8, 12, 8]);
    expect(allocations(2017, 'ordinary', '6(')).toEqual([30, 60, 10]);
    expect(allocations(2017, 'ordinary', '8(')).toEqual([15, 15, 16, 16, 10, 8]);
    expect(allocations(2017, 'ordinary', '9(')).toEqual([20, 16, 16, 10, 10, 8]);
    expect(allocations(2018, 'higher', '1(a)')).toEqual([75]);
    expect(allocations(2018, 'higher', '5(a)')).toEqual([12, 10, 10, 9, 9]);
    expect(allocations(2018, 'higher', '6(a)')).toEqual([40, 26, 24]);
    expect(allocations(2018, 'higher', '8(a)')).toEqual([34, 15, 1]);
    expect(allocations(2018, 'higher', '8(b)')).toEqual([1, 1, 1, 1, 1, 1, 2, 16, 6]);
    expect(allocations(2018, 'higher', '9(')).toEqual([14, 14, 15, 15, 15, 2, 5]);
    expect(allocations(2018, 'ordinary', '6(')).toEqual([30, 65, 5]);
    expect(allocations(2018, 'ordinary', '8(')).toEqual([14, 14, 14, 6, 11, 15, 6]);
    expect(allocations(2018, 'ordinary', '9(')).toEqual([61, 14, 5]);
    expect(allocations(2019, 'higher', '3(a)')).toEqual([12, 10, 1, 16, 7, 2, 4]);
    expect(allocations(2019, 'higher', '5(c)')).toEqual([10]);
    expect(allocations(2019, 'higher', '7(a)')).toEqual([18, 17, 48, 5]);
    expect(allocations(2019, 'higher', '8(')).toEqual([26, 8, 6, 6, 22, 12]);
    expect(allocations(2019, 'higher', '9(')).toEqual([12, 18, 23, 12, 9, 6]);
    expect(allocations(2019, 'ordinary', '5(a)')).toEqual([10, 12, 10, 8]);
    expect(allocations(2019, 'ordinary', '5(d)')).toEqual([10]);
    expect(allocations(2019, 'ordinary', '8(')).toEqual([10, 10, 10, 10, 20, 10, 10]);
    expect(allocations(2020, 'higher', '2(a)')).toEqual([35, 16]);
    expect(allocations(2020, 'higher', '4(b)')).toEqual([20]);
    expect(allocations(2020, 'higher', '8(a)')).toEqual([8, 13, 5, 14, 14, 4]);
    expect(allocations(2020, 'higher', '8(b)')).toEqual([14, 8]);
    expect(allocations(2020, 'higher', '9(')).toEqual([11, 13, 35, 15, 6]);
    expect(allocations(2020, 'ordinary', '6(')).toEqual([30, 65, 5]);
    expect(allocations(2020, 'ordinary', '7(b)')).toEqual([20]);
    expect(allocations(2020, 'ordinary', '8(')).toEqual([10, 10, 10, 10, 15, 20, 5]);
    expect(allocations(2021, 'higher', '1B(a)')).toEqual([40, 35]);
    expect(allocations(2021, 'higher', '3(d)')).toEqual([8]);
    expect(allocations(2021, 'higher', '5(a)')).toEqual([12, 10, 10, 10, 8]);
    expect(allocations(2021, 'higher', '7(a)')).toEqual([18, 17, 46, 7]);
    expect(allocations(2021, 'higher', '8(b)')).toEqual([2, 2, 2, 28]);
    expect(allocations(2021, 'higher', '8(c)')).toEqual([2, 2, 2, 10]);
    expect(allocations(2021, 'higher', '9(')).toEqual([14, 14, 16, 12, 12, 2, 10]);
    expect(allocations(2021, 'ordinary', '8(')).toEqual([15, 15, 16, 16, 10, 8]);
    expect(allocations(2021, 'ordinary', '9(')).toEqual([14, 16, 16, 16, 10, 8]);
    expect(allocations(2022, 'higher', '2(a)')).toEqual([13, 34, 5]);
    expect(allocations(2022, 'higher', '3(a)')).toEqual([40]);
    expect(allocations(2022, 'higher', '4(a)')).toEqual([48, 4]);
    expect(allocations(2022, 'higher', '8(')).toEqual([33, 8, 3, 3, 23, 10]);
    expect(allocations(2022, 'higher', '9(d)')).toEqual([11, 9]);
    expect(allocations(2022, 'ordinary', '5(a)')).toEqual([12, 12, 8, 8]);
    expect(allocations(2022, 'ordinary', '5(d)')).toEqual([10]);
    expect(allocations(2022, 'ordinary', '9(')).toEqual([60, 16, 4]);
    expect(allocations(2026, 'higher', '2(a)')).toEqual([15, 5, 32]);
    expect(allocations(2026, 'higher', '6(a)')).toEqual([40, 26, 24]);
    expect(allocations(2026, 'higher', '7(a)')).toEqual([50]);
    expect(allocations(2026, 'higher', '8(e)')).toEqual([11, 3, 4]);
    expect(allocations(2026, 'ordinary', '5(d)')).toEqual([10]);
    expect(allocations(2026, 'ordinary', '8(f)')).toEqual([15]);
    expect(allocations(2025, 'ordinary', '1B')).toEqual([40, 40, 40]);
    expect(allocations(2025, 'ordinary', '5(c)')).toEqual([10]);
    expect(allocations(2024, 'higher', '2(a)')).toEqual([35, 17]);
    expect(allocations(2024, 'higher', '3(b)')).toEqual([20]);
    expect(allocations(2024, 'higher', '6(a)')).toEqual([20, 19, 46, 5]);
    expect(allocations(2024, 'higher', '7(b)')).toEqual([8, 2]);
    expect(allocations(2024, 'higher', '8(a)(iv)')).toEqual([5, 4]);
    expect(allocations(2024, 'higher', '8(b)')).toEqual([13, 13, 6]);
    expect(allocations(2024, 'ordinary', '2(b)')).toEqual([20, 20]);
    expect(allocations(2024, 'ordinary', '5(d)')).toEqual([10]);
    expect(allocations(2024, 'ordinary', '7(b)')).toEqual([20]);
    expect(allocations(2024, 'ordinary', '9(')).toEqual([75, 5]);
    expect(allocations(2023, 'higher', '6(a)')).toEqual([40, 26, 24]);
    expect(allocations(2023, 'higher', '8(a)')).toEqual([8, 16, 4, 14, 14]);
    expect(allocations(2023, 'higher', '8(b)')).toEqual([18, 6]);
    expect(allocations(2023, 'higher', '9(')).toEqual([58, 16, 6]);
    expect(allocations(2023, 'ordinary', '3(')).toEqual([15, 20, 15, 10]);
    expect(allocations(2023, 'ordinary', '5(c)')).toEqual([10]);
    expect(allocations(2023, 'ordinary', '7(a)')).toEqual([20, 20]);
    expect(allocations(2023, 'ordinary', '8(a)')).toEqual([22, 22]);
    expect(allocations(2023, 'ordinary', '9(')).toEqual([22, 16, 16, 12, 10, 4]);
  });

  it('registers the ordinary deck and preserves old answer-map fields in every reviewed paper', async () => {
    expect(await loadCards('accounting', 'ordinary')).toEqual(ORDINARY);
    expect(deckSize('accounting', 'ordinary')).toBe(ORDINARY.length);
    const papers = new Set(authored.cards.map(card => `${card.year}/${card.paperFileid}.json`));
    for (const path of papers) {
      const before = json(`scripts/paper-trail/answers/${path}`) as PaperAnswerMap;
      const after = json(`public/paper-answers/${path}`) as PaperAnswerMap;
      for (const old of before.q) {
        const updated = after.q.find(q => q.n === old.n)!;
        for (const field of ['n', 'pP', 'pY', 'region', 'mode', 'conf'] as const) expect(updated[field]).toEqual(old[field]);
      }
    }
  });
});
