import React from 'react';
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { CARDS as HIGHER } from '../components/MarkBank/cards/applied-maths/higher';
import { CARDS as ORDINARY } from '../components/MarkBank/cards/applied-maths/ordinary';
import { REVIEWED_CARDS, withReviewedCards } from '../components/MarkBank/cards/applied-maths/reviewed';
import { appliedMathematicsMarks } from '../components/MarkBank/AppliedMathematicsRubricPanel';
import SessionScreen from '../components/MarkBank/SessionScreen';
import { tariffReconciles, type AppliedMathematicsRubric, type SecRubricCard } from '../types/markBank';
import { resolveCurriculumSpecification, specificationContainsId } from '../curriculumRegistry';
import { examTopicIdsForQuestion } from '../data/examTopics/registry';
import { topicsForPaper } from '../components/PaperTrail/topics';
import { preferredAnswersUrl, isAnswerMap } from '../components/PaperTrail/vaultResolve';
import { vaultPdf } from '../components/PaperTrail/vaultDocs';
import review from '../scripts/markbank/authoring/reviewed/applied-maths/2026.json';
import archiveReview from '../scripts/markbank/authoring/reviewed/applied-maths/2010.json';
import review2011 from '../scripts/markbank/authoring/reviewed/applied-maths/2011.json';
import review2012 from '../scripts/markbank/authoring/reviewed/applied-maths/2012.json';
import review2013 from '../scripts/markbank/authoring/reviewed/applied-maths/2013.json';
import review2014 from '../scripts/markbank/authoring/reviewed/applied-maths/2014.json';
import review2015 from '../scripts/markbank/authoring/reviewed/applied-maths/2015.json';
import review2016 from '../scripts/markbank/authoring/reviewed/applied-maths/2016.json';
import review2017 from '../scripts/markbank/authoring/reviewed/applied-maths/2017.json';
import review2018 from '../scripts/markbank/authoring/reviewed/applied-maths/2018.json';
import review2020 from '../scripts/markbank/authoring/reviewed/applied-maths/2020.json';
import review2019 from '../scripts/markbank/authoring/reviewed/applied-maths/2019.json';
import review2021 from '../scripts/markbank/authoring/reviewed/applied-maths/2021.json';
import review2022 from '../scripts/markbank/authoring/reviewed/applied-maths/2022.json';
import review2023 from '../scripts/markbank/authoring/reviewed/applied-maths/2023.json';
import review2024 from '../scripts/markbank/authoring/reviewed/applied-maths/2024.json';
import review2025 from '../scripts/markbank/authoring/reviewed/applied-maths/2025.json';

vi.mock('../components/PaperTrail/vaultDocs', () => ({ vaultPdf: vi.fn(async () => ({})) }));
const crop = vi.hoisted(() => vi.fn());
vi.mock('../components/PaperTrail/CropView', () => ({ default: (props: unknown) => {
  crop(props);
  return <div>Rendered original PDF</div>;
} }));

type AppliedCard = SecRubricCard & { rubric: AppliedMathematicsRubric };
const card = (id: string) => REVIEWED_CARDS.find(item => item.id === id)! as AppliedCard;
const idHash = (cards: Array<{ id: string }>) => createHash('sha256')
  .update(cards.map(item => item.id).sort().join('\n')).digest('hex');

describe('Applied Mathematics independently reviewed 2026 tasks', () => {
  it('keeps every previously shipped card ID, independently of the new baseline', () => {
    for (const [level, deck, hash] of [
      ['higher', HIGHER, '0eb618ccbbc6c6b312acbbe23e5f6e15906dc8e6395657ff8ce3fd0837026714'],
      ['ordinary', ORDINARY, '5457fa7f47995a3c74f439a7033728404ef1a719bb30cd4b404954c96174da33'],
    ] as const) {
      const source = readFileSync(`components/MarkBank/cards/applied-maths/${level}.ts`, 'utf8');
      const originalIds = [...source.matchAll(/^ {4}id: "([^"]+)"/gm)].map(match => match[1]);
      expect(idHash(originalIds.map(id => ({ id })))).toBe(hash);
      expect(idHash(deck.filter(item => originalIds.includes(item.id)))).toBe(hash);
      expect(new Set(deck.map(item => item.id)).size).toBe(deck.length);
    }
  });

  it('pins the reviewed task boundaries and every printed question tariff', () => {
    const expected = { higher: [5, 5, 5, 4, 5, 2, 4, 5, 5, 5], ordinary: [5, 6, 8, 6, 5, 6, 6, 7, 7, 2] };
    for (const level of ['higher', 'ordinary'] as const) {
      const cards = REVIEWED_CARDS.filter(item => item.level === level && item.year === 2026);
      expect(cards).toHaveLength(level === 'higher' ? 45 : 58);
      for (let q = 1; q <= 10; q++) {
        const tasks = cards.filter(item => item.questionRef.match(/Q(\d+)/)?.[1] === String(q));
        expect(tasks, `${level} Q${q}`).toHaveLength(expected[level][q - 1]);
        expect(tasks.reduce((sum, item) => sum + item.totalMarks, 0)).toBe(50);
      }
      expect(new Set(cards.map(item => item.id)).size).toBe(cards.length);
    }
    expect(['4kg', '6kg', '10kg'].map(suffix => card(`am-2026-ol-3-i-${suffix}`).totalMarks)).toEqual([5, 5, 5]);
    expect(card('am-2026-ol-3-iii-pulley-string').practiceFocus).toContain('6 kg and 10 kg');
    expect(card('am-2026-ol-3-iii-table-string').practiceFocus).toContain('4 kg and 6 kg');
    expect(card('am-2026-ol-8-i-m1').totalMarks).toBe(5);
    expect(card('am-2026-ol-8-i-m2').totalMarks).toBe(5);
  });

  it('retains powers, subscripts and published level-specific scales', () => {
    expect(card('am-2026-hl-1-b-ii').questionText).toContain('(13/2)3ⁿ − n − 3/2');
    expect(card('am-2026-hl-9-a-i').questionText).toContain('(t³/3)');
    expect(card('am-2026-ol-8-i-m1').questionText).toContain('M₁ and M₂');
    expect(card('am-2026-hl-1-a-i').rubric.allocations[0].credit).toEqual([0, 5, 10, 15]);
    expect(card('am-2026-ol-2-i').rubric.allocations[0].credit).toEqual([0, 6, 9, 12, 15]);
    expect(card('am-2026-ol-10-a').rubric.allocations[0].credit).toEqual([0, 9, 18, 24, 32, 35]);
  });

  it('joins every task to a canonical topic and the actual Atlas question', () => {
    for (const paper of review.papers) {
      for (const task of paper.tasks) {
        const level = paper.level as 'higher' | 'ordinary';
        const specification = resolveCurriculumSpecification('applied-mathematics', 2026)!;
        expect(specificationContainsId(specification, task.topicId), task.ref).toBe(true);
        const fileid = `LC020${level === 'higher' ? 'A' : 'G'}LP000EV.pdf`;
        const n = task.ref.match(/^Q(\d+)/)![1];
        const topics = examTopicIdsForQuestion('applied-mathematics', level, 2026, 'main', n, 'single', 'ev', fileid);
        expect(topics, `${level} ${task.ref}`).toEqual(expect.arrayContaining(task.examTopicIds));
        expect(topicsForPaper('applied-mathematics', 2026, level, 'ev', fileid)!.q.some(q => q.n === n)).toBe(true);
      }
    }
    // Vectors and projectiles share a curriculum node, but not these tasks.
    expect(examTopicIdsForQuestion('applied-mathematics', 'ordinary', 2026, 'main', '7', 'single', 'ev', 'LC020GLP000EV.pdf'))
      .toEqual(['applied-mathematics-ordinary-vectors']);
  });

  it('ships usable question and scheme crops while preserving the live Higher map identity', () => {
    for (const code of ['A', 'G']) {
      const fileid = `LC020${code}LP000EV.pdf`;
      const url = preferredAnswersUrl('applied-mathematics', 2026, fileid, 'unused-storage-url');
      expect(url).toBe(`/paper-answers/2026/${fileid}.json`);
      const map = JSON.parse(readFileSync(`public${url}`, 'utf8'));
      expect(isAnswerMap(map)).toBe(true);
      expect(map.q).toHaveLength(10);
      expect(map.q.every((q: { paperRegion: unknown[]; region: unknown[] }) => q.paperRegion.length && q.region.length)).toBe(true);
      if (code === 'A') {
        const original = JSON.parse(readFileSync(`scripts/paper-trail/answers/2026/${fileid}.json`, 'utf8'));
        for (const q of original.q) expect(map.q.find((item: { n: string }) => item.n === q.n)).toMatchObject(q);
      }
    }
    for (const item of REVIEWED_CARDS) expect(tariffReconciles(item), item.id).toBe(true);
  });
});

describe('Applied Mathematics independently reviewed 2010 Higher tasks', () => {
  it('covers the complete printed paper at the reviewed mark boundaries', () => {
    const cards = REVIEWED_CARDS.filter(item => item.year === 2010 && item.level === 'higher');
    expect(cards).toHaveLength(35);
    for (let q = 1; q <= 10; q++) {
      const tasks = cards.filter(item => item.questionRef.match(/Q(\d+)/)?.[1] === String(q));
      expect(tasks).toHaveLength([3, 3, 3, 4, 4, 4, 4, 3, 4, 3][q - 1]);
      expect(tasks.reduce((sum, item) => sum + item.totalMarks, 0)).toBe(50);
    }
    expect(card('am-2010-hl-9-a-principle').totalMarks).toBe(5);
    expect(card('am-2010-hl-9-a-density').totalMarks).toBe(20);
    expect(card('am-2010-hl-4-b-i').totalMarks).toBe(5);
    expect(card('am-2010-hl-4-b-ii').rubric.allocations.map(item => Math.max(...item.credit))).toEqual([5, 5, 5, 15]);
    expect(card('am-2010-hl-5-a-i').totalMarks).toBe(15);
    expect(card('am-2010-hl-5-a-ii').totalMarks).toBe(10);
    expect(card('am-2010-hl-7-b-ii').totalMarks).toBe(15);
    expect(card('am-2010-hl-1-a-i').rubric.allocations[0].credit).toEqual([0, 2, 5]);
  });

  it('keeps archived mechanics under their real curriculum and Atlas topics', () => {
    const specification = resolveCurriculumSpecification('applied-mathematics', 2010)!;
    for (const task of archiveReview.papers[0].tasks) {
      expect(specificationContainsId(specification, task.topicId)).toBe(true);
      const n = task.ref.match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('applied-mathematics', 'higher', 2010, 'main', n, 'single', 'ev', 'LC020ALP000EV.pdf'))
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
    expect(examTopicIdsForQuestion('applied-mathematics', 'higher', 2010, 'main', '9', 'single', 'ev', 'LC020ALP000EV.pdf'))
      .toEqual(['applied-mathematics-higher-hydrostatics']);
  });
});

describe('Applied Mathematics independently reviewed 2010 Ordinary tasks', () => {
  it('retains unnumbered asks, separately priced paired asks and the actual gravity constant', () => {
    const cards = REVIEWED_CARDS.filter(item => item.year === 2010 && item.level === 'ordinary');
    expect(cards).toHaveLength(42);
    for (let q = 1; q <= 9; q++) {
      const tasks = cards.filter(item => item.questionRef.match(/Q(\d+)/)?.[1] === String(q));
      expect(tasks).toHaveLength([4, 6, 5, 5, 3, 4, 6, 5, 4][q - 1]);
      expect(tasks.reduce((sum, item) => sum + item.totalMarks, 0)).toBe(50);
    }
    expect(card('am-2010-ol-9-a-principle').totalMarks).toBe(10);
    expect(card('am-2010-ol-2-iii-magnitude').totalMarks).toBe(5);
    expect(card('am-2010-ol-2-iii-direction').totalMarks).toBe(5);
    expect(card('am-2010-ol-7-ii-horizontal').practiceFocus).toBe('Horizontal force equation');
    expect(card('am-2010-ol-7-ii-vertical').practiceFocus).toBe('Vertical force equation');
    expect(card('am-2010-ol-4-b-i').totalMarks).toBe(10);
    expect(card('am-2010-ol-8-a-i').totalMarks).toBe(5);
    expect(card('am-2010-ol-8-a-ii').totalMarks).toBe(15);
    expect(card('am-2010-ol-3-i').stem).toContain('10 m s⁻²');
    expect(card('am-2010-ol-3-i').rubric.allocations[0].credit).toEqual([0, 3, 10]);
    const paper = archiveReview.papers.find(item => item.level === 'ordinary')!;
    for (const task of paper.tasks) {
      const n = task.ref.match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('applied-mathematics', 'ordinary', 2010, 'main', n, 'single', 'ev', 'LC020GLP000EV.pdf'))
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
});

describe('Applied Mathematics independently reviewed 2011 tasks', () => {
  it('preserves separate parameter, pendulum and ship-distance asks at published boundaries', () => {
    const expected = { higher: [4, 3, 4, 2, 4, 5, 3, 4, 2, 3], ordinary: [4, 6, 5, 5, 3, 4, 2, 4, 2] };
    for (const level of ['higher', 'ordinary'] as const) {
      const cards = REVIEWED_CARDS.filter(item => item.year === 2011 && item.level === level);
      expect(cards).toHaveLength(level === 'higher' ? 34 : 35);
      for (let q = 1; q <= expected[level].length; q++) {
        const tasks = cards.filter(item => item.questionRef.match(/Q(\d+)/)?.[1] === String(q));
        expect(tasks).toHaveLength(expected[level][q - 1]);
        expect(tasks.reduce((sum, item) => sum + item.totalMarks, 0)).toBe(50);
      }
      const fileid = `LC020${level === 'higher' ? 'A' : 'G'}LP000EV.pdf`;
      const url = preferredAnswersUrl('applied-mathematics', 2011, fileid, 'unused');
      expect(url).toBe(`/paper-answers/2011/${fileid}.json`);
      expect(isAnswerMap(JSON.parse(readFileSync(`public${url}`, 'utf8')))).toBe(true);
      for (const task of review2011.papers.find(p => p.level === level)!.tasks) {
        expect(specificationContainsId(resolveCurriculumSpecification('applied-mathematics', 2011)!, task.topicId)).toBe(true);
        expect(examTopicIdsForQuestion('applied-mathematics', level, 2011, 'main', task.ref.match(/^Q(\d+)/)![1], 'single', 'ev', fileid))
          .toEqual(expect.arrayContaining(task.examTopicIds));
      }
    }
    expect(['omega', 'epsilon', 'amplitude'].map(s => card(`am-2011-hl-6-a-ii-${s}`).totalMarks)).toEqual([5, 5, 5]);
    expect(['period', 'length'].map(s => card(`am-2011-hl-8-b-ii-${s}`).totalMarks)).toEqual([10, 5]);
    expect(['a', 'b'].map(s => card(`am-2011-ol-2-v-${s}`).totalMarks)).toEqual([5, 5]);
    expect(card('am-2011-hl-4-b').totalMarks).toBe(30);
    expect(card('am-2011-ol-4-a-i').totalMarks).toBe(10);
    expect(card('am-2011-ol-5-i').totalMarks).toBe(30);
    expect(card('am-2011-hl-8-b-ii-period').rubric.solution.regions![0][1]).toBeLessThan(.54);
    expect(card('am-2011-hl-6-b').rubric.solution.regions![0][1]).toBeLessThan(.24);
  });
});

describe('Applied Mathematics independently reviewed 2012 tasks', () => {
  it('covers the reviewed tasks without splitting joint credits or omitting unnumbered asks', () => {
    const expected = { higher: [3, 4, 4, 4, 2, 4, 2, 3, 3, 4], ordinary: [4, 4, 6, 5, 3, 4, 6, 5, 4] };
    for (const level of ['higher', 'ordinary'] as const) {
      const cards = REVIEWED_CARDS.filter(item => item.year === 2012 && item.level === level);
      expect(cards).toHaveLength(level === 'higher' ? 33 : 41);
      for (let q = 1; q <= expected[level].length; q++) {
        const tasks = cards.filter(item => item.questionRef.match(/Q(\d+)/)?.[1] === String(q));
        expect(tasks).toHaveLength(expected[level][q - 1]);
        expect(tasks.reduce((sum, item) => sum + item.totalMarks, 0)).toBe(50);
      }
      const fileid = `LC020${level === 'higher' ? 'A' : 'G'}LP000EV.pdf`;
      const url = preferredAnswersUrl('applied-mathematics', 2012, fileid, 'unused');
      expect(url).toBe(`/paper-answers/2012/${fileid}.json`);
      expect(isAnswerMap(JSON.parse(readFileSync(`public${url}`, 'utf8')))).toBe(true);
      for (const task of review2012.papers.find(p => p.level === level)!.tasks) {
        expect(specificationContainsId(resolveCurriculumSpecification('applied-mathematics', 2012)!, task.topicId)).toBe(true);
        expect(examTopicIdsForQuestion('applied-mathematics', level, 2012, 'main', task.ref.match(/^Q(\d+)/)![1], 'single', 'ev', fileid))
          .toEqual(expect.arrayContaining(task.examTopicIds));
      }
    }
    expect(['speed', 'direction'].map(s => card(`am-2012-ol-3-b-ii-${s}`).totalMarks)).toEqual([5, 5]);
    expect(['horizontal', 'vertical'].map(s => card(`am-2012-ol-7-ii-${s}`).totalMarks)).toEqual([5, 5]);
    expect(card('am-2012-ol-9-a-principle').totalMarks).toBe(5);
    expect(card('am-2012-hl-2-b-i').totalMarks).toBe(10);
    expect(card('am-2012-ol-5-i').rubric.allocations.map(a => Math.max(...a.credit))).toEqual([10, 10, 5]);
    expect(card('am-2012-hl-8-b-i').totalMarks).toBe(25);
    expect(card('am-2012-hl-10-b-ii').questionText).toContain('(10/99)ln100');
    expect(card('am-2012-hl-4-a-i').sourceMaterial!.regions![0][1]).toBeLessThan(.4274);
  });
});

describe('Applied Mathematics independently reviewed 2025 tasks', () => {
  it('restores all printed tasks, source contexts and question tariffs', () => {
    const expected = { higher: [7, 6, 5, 6, 6, 4, 5, 6, 3, 4], ordinary: [5, 5, 5, 6, 5, 5, 6, 8, 5, 5] };
    for (const level of ['higher', 'ordinary'] as const) {
      const cards = REVIEWED_CARDS.filter(item => item.year === 2025 && item.level === level);
      expect(cards).toHaveLength(level === 'higher' ? 52 : 55);
      for (let q = 1; q <= 10; q++) {
        const tasks = cards.filter(item => item.questionRef.match(/Q(\d+)/)?.[1] === String(q));
        expect(tasks).toHaveLength(expected[level][q - 1]);
        expect(tasks.reduce((sum, item) => sum + item.totalMarks, 0)).toBe(50);
      }
      const fileid = `LC020${level === 'higher' ? 'A' : 'G'}LP000EV.pdf`;
      const url = preferredAnswersUrl('applied-mathematics', 2025, fileid, 'unused');
      expect(url).toBe(`/paper-answers/2025/${fileid}.json`);
      const map = JSON.parse(readFileSync(`public${url}`, 'utf8'));
      expect(isAnswerMap(map)).toBe(true);
      const original = JSON.parse(readFileSync(`scripts/paper-trail/answers/2025/${fileid}.json`, 'utf8'));
      for (const q of original.q) expect(map.q.find((item: { n: string }) => item.n === q.n)).toMatchObject(q);
      for (const task of review2025.papers.find(p => p.level === level)!.tasks) {
        expect(specificationContainsId(resolveCurriculumSpecification('applied-mathematics', 2025)!, task.topicId)).toBe(true);
        expect(examTopicIdsForQuestion('applied-mathematics', level, 2025, 'main', task.ref.match(/^Q(\d+)/)![1], 'single', 'ev', fileid))
          .toEqual(expect.arrayContaining(task.examTopicIds));
      }
    }
    expect(card('am-2025-hl-2').questionRef).toBe('2025 HL Q2(i)');
    expect(['2', '2-ii', '2-iii', '2-iv', '2-v', '2-vi'].map(s => card(`am-2025-hl-${s}`).totalMarks))
      .toEqual([5, 10, 5, 15, 5, 10]);
    expect(card('am-2025-hl-2-vi').sourceMaterial?.pages).toEqual([6, 7, 9]);
    expect(card('am-2025-hl-4-vi').sourceMaterial?.pages).toEqual([14, 15, 16, 17]);
    expect(card('am-2025-ol-3-v').sourceMaterial?.pages).toEqual([10, 12, 13]);
    expect(['x', 'y'].map(s => card(`am-2025-hl-5-a-i-${s}`).totalMarks)).toEqual([5, 5]);
    expect(['5-a-ii', '5-a-ii-y'].map(s => card(`am-2025-hl-${s}`).totalMarks)).toEqual([10, 5]);
    expect(['table', 'incline'].map(s => card(`am-2025-ol-1-b-i-${s}`).totalMarks)).toEqual([5, 5]);
    expect(['8-a-i', '8-a-i-direction'].map(s => card(`am-2025-ol-${s}`).totalMarks)).toEqual([5, 5]);
  });

  it('uses the actual 2025 marking scales and retains separately priced outputs', () => {
    expect(card('am-2025-hl-1-a-ii').rubric.allocations[0].credit).toEqual([0, 4, 7, 10]);
    expect(card('am-2025-hl-7-a-i').rubric.allocations[0].credit).toEqual([0, 6, 12, 15]);
    expect(card('am-2025-ol-4-vi').rubric.allocations[0].credit).toEqual([0, 6, 12, 15]);
    expect(card('am-2025-hl-6-a-i').rubric.allocations[0].credit).toEqual([0, 8, 14, 17, 20]);
    expect(card('am-2025-ol-2-a-ii').rubric.allocations.map(a => a.credit)).toEqual([[0, 5], [0, 5], [0, 5], [0, 5]]);
    expect(card('am-2025-ol-9-b-ii').rubric.allocations[0].credit).toEqual([0, 10]);
    const entries = card('am-2025-ol-9-b-i');
    expect(entries.rubric.allocations[0].credit).toEqual(Array.from({ length: 11 }, (_, i) => i));
    expect(appliedMathematicsMarks(entries, { [`applied:${entries.rubric.allocations[0].id}:credit`]: 7 })).toBe(7);
    expect(card('am-2025-hl-5-a-ii-y').rubric.allocations[0].guidance).toContain('last published 5-mark placement');
    expect(card('am-2025-ol-5-a-ii').rubric.allocations[1].guidance).toContain('2.8 m s⁻¹');
    expect(card('am-2025-hl-5-b').rubric.allocations[1].guidance).toContain('cannot be chosen independently');
  });

  it('retains every shipped identity with an explicit source correction', () => {
    for (const paper of review2025.papers) {
      const deck = paper.level === 'higher' ? HIGHER : ORDINARY;
      expect(paper.cardCorrections).toHaveLength(paper.level === 'higher' ? 40 : 49);
      for (const correction of paper.cardCorrections) {
        expect(deck.filter(item => item.id === correction.cardId)).toHaveLength(1);
        expect(card(correction.cardId).qa?.gates).toContain('reviewed-card-correction');
      }
    }
  });
});

describe('Applied Mathematics independently reviewed 2024 tasks', () => {
  it('pins mark boundaries, sources and Atlas joins for both complete papers', () => {
    const expected = { higher: [4, 6, 3, 6, 4, 6, 6, 3, 5, 5], ordinary: [6, 7, 9, 6, 4, 4, 6, 7, 6, 6] };
    for (const level of ['higher', 'ordinary'] as const) {
      const cards = REVIEWED_CARDS.filter(item => item.year === 2024 && item.level === level);
      expect(cards).toHaveLength(level === 'higher' ? 48 : 61);
      for (let q = 1; q <= expected[level].length; q++) {
        const tasks = cards.filter(item => item.questionRef.match(/Q(\d+)/)?.[1] === String(q));
        expect(tasks).toHaveLength(expected[level][q - 1]);
        expect(tasks.reduce((sum, item) => sum + item.totalMarks, 0)).toBe(50);
      }
      const fileid = `LC020${level === 'higher' ? 'A' : 'G'}LP000EV.pdf`;
      const url = preferredAnswersUrl('applied-mathematics', 2024, fileid, 'unused');
      expect(url).toBe(`/paper-answers/2024/${fileid}.json`);
      const map = JSON.parse(readFileSync(`public${url}`, 'utf8'));
      expect(isAnswerMap(map)).toBe(true);
      const original = JSON.parse(readFileSync(`scripts/paper-trail/answers/2024/${fileid}.json`, 'utf8'));
      for (const q of original.q) expect(map.q.find((item: { n: string }) => item.n === q.n)).toMatchObject(q);
      for (const task of review2024.papers.find(p => p.level === level)!.tasks) {
        expect(specificationContainsId(resolveCurriculumSpecification('applied-mathematics', 2024)!, task.topicId)).toBe(true);
        expect(examTopicIdsForQuestion('applied-mathematics', level, 2024, 'main', task.ref.match(/^Q(\d+)/)![1], 'single', 'ev', fileid))
          .toEqual(expect.arrayContaining(task.examTopicIds));
      }
    }
    expect(['w1', 'pulley', 'w2'].map(s => card(`am-2024-hl-2-b-i-${s}`).totalMarks)).toEqual([5, 5, 5]);
    expect(['5-a-ii', '5-a-ii-meaning'].map(s => card(`am-2024-ol-${s}`).totalMarks)).toEqual([5, 5]);
    expect(['table', 'hanging'].map(s => card(`am-2024-ol-8-b-i-${s}`).totalMarks)).toEqual([5, 5]);
    expect(card('am-2024-hl-3-b-i').rubric.allocations.map(a => Math.max(...a.credit))).toEqual([5, 5, 5]);
    expect(card('am-2024-hl-5-a-i').rubric.allocations.map(a => Math.max(...a.credit))).toEqual([5, 5, 5]);
    expect(card('am-2024-ol-7-v').totalMarks).toBe(5);
    expect(card('am-2024-ol-8-a-iii').rubric.allocations.map(a => Math.max(...a.credit))).toEqual([5, 5]);
    expect(card('am-2024-hl-8-a-i').rubric.allocations[0].credit).toEqual([0, 8, 16, 24, 27, 30]);
    expect(card('am-2024-ol-5-b').rubric.allocations[0].credit).toEqual([0, 10, 18, 21, 25]);
    expect(card('am-2024-hl-1-b-i').rubric.allocations[0].credit).toEqual([0, 3, 6, 9, 12, 15]);
    expect(card('am-2024-hl-1-b-i').rubric.allocations[0].guidance).toContain('correct algorithm name with no other work');
    for (const id of ['am-2024-ol-9-i', 'am-2024-ol-6-a-i']) {
      expect(card(id).rubric.allocations[0].credit).toEqual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);
      expect(card(id).rubric.allocations[0].guidance).toContain('do not deduct the same error again');
      expect(appliedMathematicsMarks(card(id), { 'applied:allocation-1:credit': 9 })).toBe(9);
    }
    expect(card('am-2024-hl-8-b').topicId).toBe('applied-mathematics-2-8');
    expect(card('am-2024-ol-6-a-iii').topicId).toBe('applied-mathematics-0-4');
    expect(examTopicIdsForQuestion('applied-mathematics', 'higher', 2024, 'main', '8', 'single', 'ev', 'LC020ALP000EV.pdf'))
      .toEqual(expect.arrayContaining(['applied-mathematics-higher-dimensional-analysis', 'applied-mathematics-higher-optimal-critical-paths']));
  });

  it('applies only explicitly recorded legacy corrections and retains each shipped identity once', () => {
    for (const paper of review2024.papers) {
      const deck = paper.level === 'higher' ? HIGHER : ORDINARY;
      const source = readFileSync(`components/MarkBank/cards/applied-maths/${paper.level}.ts`, 'utf8');
      const blocks = [...source.matchAll(/ {2}\{\n {4}\.\.\.base,[\s\S]*? {2}\} as SecCard,/g)].map(match => match[0]);
      expect(paper.cardCorrections).toHaveLength(paper.level === 'higher' ? 37 : 47);
      for (const correction of paper.cardCorrections) {
        const block = blocks.find(value => value.match(/^ {4}id: "([^"]+)"/m)?.[1] === correction.cardId)!;
        expect(createHash('sha256').update(block).digest('hex')).toBe(correction.originalBlockSha256);
        const matches = deck.filter(item => item.id === correction.cardId);
        expect(matches).toHaveLength(1);
        expect(matches[0]).toBe(card(correction.cardId));
        expect(matches[0].qa?.gates).toContain('reviewed-card-correction');
      }
    }
    expect(() => withReviewedCards([card('am-2010-ol-3-i')], 'ordinary')).toThrow('unaudited correction');
  });

  it('retains supporting source pages and distinguishes study corrections from the published scheme', () => {
    expect(card('am-2024-hl-4-vi').sourceMaterial?.pages).toEqual([14, 15, 16, 17]);
    expect(card('am-2024-hl-8-a-i').sourceMaterial?.pages).toEqual([30, 31]);
    expect(card('am-2024-ol-9-i').sourceMaterial?.pages).toEqual([30, 31]);
    expect(card('am-2024-ol-9-vi').sourceMaterial?.pages).toEqual([30, 32, 33]);
    expect(card('am-2024-ol-5-a-ii-meaning').practiceFocus).toBe('Explain the entries of N²');
    expect(card('am-2024-ol-5-a-ii-meaning').rubric.allocations[0].guidance).toContain('second 5-mark placement');
    expect(card('am-2024-hl-6-a-iii').rubric.allocations[0].guidance).toContain('13662');
    expect(card('am-2024-hl-6-a-iii').rubric.allocations[0].guidance).toContain('not an SEC erratum');
    expect(card('am-2024-ol-3-a-iv').rubric.allocations[0].guidance).toContain('165(1.1ⁿ − 1) = 240');
    expect(card('am-2024-hl-5-a-i').rubric.allocations[2].guidance).toContain('|u(1 − 9e)/5|');
  });
});

describe('Applied Mathematics independently reviewed 2023 tasks', () => {
  it('pins mark boundaries, sources and Atlas joins for both complete papers', () => {
    const expected = { higher: [5, 3, 5, 6, 4, 5, 5, 6, 5, 7], ordinary: [6, 7, 9, 4, 5, 7, 5, 5, 7, 6] };
    for (const level of ['higher', 'ordinary'] as const) {
      const cards = REVIEWED_CARDS.filter(item => item.year === 2023 && item.level === level);
      expect(cards).toHaveLength(level === 'higher' ? 51 : 61);
      for (let q = 1; q <= expected[level].length; q++) {
        const tasks = cards.filter(item => item.questionRef.match(/Q(\d+)/)?.[1] === String(q));
        expect(tasks).toHaveLength(expected[level][q - 1]);
        expect(tasks.reduce((sum, item) => sum + item.totalMarks, 0)).toBe(50);
      }
      const fileid = `LC020${level === 'higher' ? 'A' : 'G'}LP000EV.pdf`;
      const url = preferredAnswersUrl('applied-mathematics', 2023, fileid, 'unused');
      expect(url).toBe(`/paper-answers/2023/${fileid}.json`);
      const map = JSON.parse(readFileSync(`public${url}`, 'utf8'));
      expect(isAnswerMap(map)).toBe(true);
      const original = JSON.parse(readFileSync(`scripts/paper-trail/answers/2023/${fileid}.json`, 'utf8'));
      for (const q of original.q) expect(map.q.find((item: { n: string }) => item.n === q.n)).toMatchObject(q);
      for (const task of review2023.papers.find(p => p.level === level)!.tasks) {
        expect(specificationContainsId(resolveCurriculumSpecification('applied-mathematics', 2023)!, task.topicId)).toBe(true);
        expect(examTopicIdsForQuestion('applied-mathematics', level, 2023, 'main', task.ref.match(/^Q(\d+)/)![1], 'single', 'ev', fileid))
          .toEqual(expect.arrayContaining(task.examTopicIds));
      }
    }
    expect(['2-b', '2-b-q'].map(s => card(`am-2023-hl-${s}`).totalMarks)).toEqual([25, 5]);
    expect(['8-iii', '8-iii-q'].map(s => card(`am-2023-hl-${s}`).totalMarks)).toEqual([5, 5]);
    expect(['7-i', '7-i-s2'].map(s => card(`am-2023-ol-${s}`).totalMarks)).toEqual([15, 5]);
    expect(card('am-2023-ol-3-vii').rubric.allocations.map(a => Math.max(...a.credit))).toEqual([5, 5]);
    expect(card('am-2023-hl-7-b-i').rubric.allocations.map(a => Math.max(...a.credit))).toEqual([5, 5, 5, 5]);
    expect(card('am-2023-hl-1-a-i').rubric.allocations[0].credit).toEqual([0, 4, 7, 10]);
    expect(card('am-2023-ol-10-i').rubric.allocations[0].credit).toEqual([0, 8, 14, 17, 20]);
    expect(card('am-2023-hl-7-a-i').rubric.allocations[0].credit).toEqual([0, 3, 6, 9, 12, 15]);
    expect(card('am-2023-hl-7-a-i').rubric.allocations[0].guidance).toContain('correct algorithm name with no other work');
    for (const id of ['am-2023-hl-9-i', 'am-2023-ol-4-a-i']) {
      expect(card(id).rubric.allocations[0].credit).toEqual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);
      expect(card(id).rubric.allocations[0].guidance).toContain('do not deduct the same error again');
      expect(appliedMathematicsMarks(card(id), { 'applied:allocation-1:credit': 9 })).toBe(9);
    }
    expect(card('am-2023-hl-3-iii').topicId).toBe('applied-mathematics-2-8');
    expect(examTopicIdsForQuestion('applied-mathematics', 'higher', 2023, 'main', '3', 'single', 'ev', 'LC020ALP000EV.pdf'))
      .toContain('applied-mathematics-higher-dimensional-analysis');
  });

  it('applies only explicitly recorded legacy corrections and retains each shipped identity once', () => {
    for (const paper of review2023.papers) {
      const deck = paper.level === 'higher' ? HIGHER : ORDINARY;
      const source = readFileSync(`components/MarkBank/cards/applied-maths/${paper.level}.ts`, 'utf8');
      const blocks = [...source.matchAll(/ {2}\{\n {4}\.\.\.base,[\s\S]*? {2}\} as SecCard,/g)].map(match => match[0]);
      expect(paper.cardCorrections).toHaveLength(paper.level === 'higher' ? 37 : 43);
      for (const correction of paper.cardCorrections) {
        const block = blocks.find(value => value.match(/^ {4}id: "([^"]+)"/m)?.[1] === correction.cardId)!;
        expect(createHash('sha256').update(block).digest('hex')).toBe(correction.originalBlockSha256);
        const matches = deck.filter(item => item.id === correction.cardId);
        expect(matches).toHaveLength(1);
        expect(matches[0]).toBe(card(correction.cardId));
        expect(matches[0].qa?.gates).toContain('reviewed-card-correction');
      }
    }
    expect(() => withReviewedCards([card('am-2010-ol-3-i')], 'ordinary')).toThrow('unaudited correction');
  });

  it('retains the network, table and supporting context across question pages', () => {
    expect(card('am-2023-hl-9-i').sourceMaterial?.pages).toEqual([34, 35]);
    expect(card('am-2023-hl-9-iv').sourceMaterial?.pages).toEqual([34, 35, 37]);
    expect(card('am-2023-hl-8-v').sourceMaterial?.pages).toEqual([30, 31, 32, 33]);
    expect(card('am-2023-ol-6-v-cyclist').sourceMaterial?.pages).toEqual([22, 23, 24]);
    expect(card('am-2023-ol-3-iv').practiceFocus).toBe('Angle α');
    expect(card('am-2023-hl-3-iv').rubric.allocations[2].guidance).toContain('complete revolutions: 8');
  });
});

describe('Applied Mathematics independently reviewed 2022 tasks', () => {
  it('pins mark boundaries, sources and Atlas joins for both complete papers', () => {
    const expected = { higher: [6, 5, 3, 4, 5, 6, 3, 3, 3, 6], ordinary: [6, 8, 6, 6, 5, 5, 6, 9, 5] };
    for (const level of ['higher', 'ordinary'] as const) {
      const cards = REVIEWED_CARDS.filter(item => item.year === 2022 && item.level === level);
      expect(cards).toHaveLength(level === 'higher' ? 44 : 56);
      for (let q = 1; q <= expected[level].length; q++) {
        const tasks = cards.filter(item => item.questionRef.match(/Q(\d+)/)?.[1] === String(q));
        expect(tasks).toHaveLength(expected[level][q - 1]);
        expect(tasks.reduce((sum, item) => sum + item.totalMarks, 0)).toBe(50);
      }
      const fileid = `LC020${level === 'higher' ? 'A' : 'G'}LP000EV.pdf`;
      const url = preferredAnswersUrl('applied-mathematics', 2022, fileid, 'unused');
      expect(url).toBe(`/paper-answers/2022/${fileid}.json`);
      const map = JSON.parse(readFileSync(`public${url}`, 'utf8'));
      expect(isAnswerMap(map)).toBe(true);
      const original = JSON.parse(readFileSync(`scripts/paper-trail/answers/2022/${fileid}.json`, 'utf8'));
      for (const q of original.q) expect(map.q.find((item: { n: string }) => item.n === q.n)).toMatchObject(q);
      for (const task of review2022.papers.find(p => p.level === level)!.tasks) {
        expect(specificationContainsId(resolveCurriculumSpecification('applied-mathematics', 2022)!, task.topicId)).toBe(true);
        expect(examTopicIdsForQuestion('applied-mathematics', level, 2022, 'main', task.ref.match(/^Q(\d+)/)![1], 'single', 'ev', fileid))
          .toEqual(expect.arrayContaining(task.examTopicIds));
      }
    }
    expect(['1-b-i', '1-b-i-distance'].map(s => card(`am-2022-hl-${s}`).totalMarks)).toEqual([5, 5]);
    expect(['5-a-i', '5-a-i-b'].map(s => card(`am-2022-hl-${s}`).totalMarks)).toEqual([15, 5]);
    expect(card('am-2022-hl-3-a-ii').totalMarks).toBe(5);
    expect(card('am-2022-ol-5-i').rubric.allocations.map(a => Math.max(...a.credit))).toEqual([5, 5, 10]);
    expect(card('am-2022-ol-4-a-ii').rubric.allocations.map(a => a.credit)).toEqual([[0, 2, 15]]);
    expect(card('am-2022-ol-1-i').rubric.allocations[0].credit).toEqual([0, 2, 10]);
    expect(['7-a-ii', '7-a-ii-left'].map(s => card(`am-2022-ol-${s}`).totalMarks)).toEqual([10, 5]);
    expect(card('am-2022-hl-5-b').sourceMaterial?.regions![0][3]).toBeGreaterThan(.457);
    expect(card('am-2022-hl-6-b').sourceMaterial?.regions![0][3]).toBeGreaterThan(.88);
    expect(card('am-2022-ol-4-a-i').sourceMaterial?.regions![0][1]).toBeLessThan(.336);
  });

  it('applies only explicitly recorded legacy corrections and retains each shipped identity once', () => {
    for (const paper of review2022.papers) {
      const deck = paper.level === 'higher' ? HIGHER : ORDINARY;
      const source = readFileSync(`components/MarkBank/cards/applied-maths/${paper.level}.ts`, 'utf8');
      const blocks = [...source.matchAll(/ {2}\{\n {4}\.\.\.base,[\s\S]*? {2}\} as SecCard,/g)].map(match => match[0]);
      expect(paper.cardCorrections).toHaveLength(paper.level === 'higher' ? 31 : 33);
      for (const correction of paper.cardCorrections) {
        const block = blocks.find(value => value.match(/^ {4}id: "([^"]+)"/m)?.[1] === correction.cardId)!;
        expect(createHash('sha256').update(block).digest('hex')).toBe(correction.originalBlockSha256);
        const matches = deck.filter(item => item.id === correction.cardId);
        expect(matches).toHaveLength(1);
        expect(matches[0]).toBe(card(correction.cardId));
        expect(matches[0].qa?.gates).toContain('reviewed-card-correction');
      }
    }
    expect(() => withReviewedCards([card('am-2010-ol-3-i')], 'ordinary')).toThrow('unaudited correction');
  });

  it('retains both question pages and the full cliff diagram for every Q3 task', () => {
    const tasks = REVIEWED_CARDS.filter(item => item.id.startsWith('am-2022-ol-3-'));
    expect(tasks).toHaveLength(6);
    for (const item of tasks) {
      expect(item.sourceMaterial?.pages).toEqual([2, 3]);
      expect(item.sourceMaterial?.regions).toHaveLength(2);
      expect(item.sourceMaterial?.regions![1][1]).toBeLessThan(.095);
      expect(item.sourceMaterial?.regions![1][3]).toBeGreaterThan(.285);
      expect(item.sourceMaterial?.regions![1][3]).toBeLessThan(.336);
    }
  });
});

describe('Applied Mathematics independently reviewed 2021 tasks', () => {
  it('pins mark boundaries, sources and Atlas joins for both complete papers', () => {
    const expected = { higher: [4, 3, 5, 8, 5, 4, 5, 4, 4, 4], ordinary: [6, 7, 6, 6, 5, 4, 8, 6, 6] };
    for (const level of ['higher', 'ordinary'] as const) {
      const cards = REVIEWED_CARDS.filter(item => item.year === 2021 && item.level === level);
      expect(cards).toHaveLength(level === 'higher' ? 46 : 54);
      for (let q = 1; q <= expected[level].length; q++) {
        const tasks = cards.filter(item => item.questionRef.match(/Q(\d+)/)?.[1] === String(q));
        expect(tasks).toHaveLength(expected[level][q - 1]);
        expect(tasks.reduce((sum, item) => sum + item.totalMarks, 0)).toBe(50);
      }
      const fileid = `LC020${level === 'higher' ? 'A' : 'G'}LP000EV.pdf`;
      const url = preferredAnswersUrl('applied-mathematics', 2021, fileid, 'unused');
      expect(url).toBe(`/paper-answers/2021/${fileid}.json`);
      const map = JSON.parse(readFileSync(`public${url}`, 'utf8'));
      expect(isAnswerMap(map)).toBe(true);
      const original = JSON.parse(readFileSync(`scripts/paper-trail/answers/2021/${fileid}.json`, 'utf8'));
      for (const q of original.q) expect(map.q.find((item: { n: string }) => item.n === q.n)).toMatchObject(q);
      for (const task of review2021.papers.find(p => p.level === level)!.tasks) {
        expect(specificationContainsId(resolveCurriculumSpecification('applied-mathematics', 2021)!, task.topicId)).toBe(true);
        expect(examTopicIdsForQuestion('applied-mathematics', level, 2021, 'main', task.ref.match(/^Q(\d+)/)![1], 'single', 'ev', fileid))
          .toEqual(expect.arrayContaining(task.examTopicIds));
      }
    }
    expect(['3-a', '3-a-i-maximum', '3-a-ii-distance'].map(s => card(`am-2021-hl-${s}`).totalMarks)).toEqual([15, 5, 5]);
    expect(['wedge', 'particle'].map(s => card(`am-2021-hl-4-b-i-${s}`).totalMarks)).toEqual([5, 5]);
    expect(card('am-2021-hl-8-b-ii').rubric.allocations.map(a => Math.max(...a.credit))).toEqual([5, 5, 5]);
    expect(card('am-2021-ol-5-a-i').rubric.allocations.map(a => Math.max(...a.credit))).toEqual([5, 5, 10]);
    expect(card('am-2021-ol-6-b-i').totalMarks).toBe(10);
    expect(card('am-2021-ol-7-b-v').totalMarks).toBe(5);
    expect(card('am-2021-hl-3-b-i').rubric.solution.regions![0][1]).toBeLessThan(.281);
    expect(card('am-2021-hl-9-b-i').rubric.solution.regions![0][1]).toBeLessThan(.30);
  });

  it('applies only explicitly recorded legacy corrections and retains each shipped identity once', () => {
    for (const paper of review2021.papers) {
      const deck = paper.level === 'higher' ? HIGHER : ORDINARY;
      const source = readFileSync(`components/MarkBank/cards/applied-maths/${paper.level}.ts`, 'utf8');
      const blocks = [...source.matchAll(/ {2}\{\n {4}\.\.\.base,[\s\S]*? {2}\} as SecCard,/g)].map(match => match[0]);
      expect(paper.cardCorrections).toHaveLength(paper.level === 'higher' ? 30 : 36);
      for (const correction of paper.cardCorrections) {
        const block = blocks.find(value => value.match(/^ {4}id: "([^"]+)"/m)?.[1] === correction.cardId)!;
        expect(createHash('sha256').update(block).digest('hex')).toBe(correction.originalBlockSha256);
        const matches = deck.filter(item => item.id === correction.cardId);
        expect(matches).toHaveLength(1);
        expect(matches[0]).toBe(card(correction.cardId));
        expect(matches[0].qa?.gates).toContain('reviewed-card-correction');
      }
    }
    expect(() => withReviewedCards([card('am-2010-ol-3-i')], 'ordinary')).toThrow('unaudited correction');
  });

  it('labels the corrected angular velocity as a study aid while retaining the official solution', () => {
    const item = card('am-2021-ol-8-b-ii');
    expect(item.questionText).toBe('Find the angular velocity of the object.');
    expect(item.stem).toContain('Study aid:');
    const guidance = item.rubric.allocations[2].guidance;
    expect(guidance).toContain('Study aid correction, not an SEC erratum');
    expect(guidance).toContain('√2.5 ≈ 1.58 rad s⁻¹');
    expect(item.rubric.solution.pages).toEqual([15]);
    expect(item.rubric.solution.sourceFileid).toBe('LC020GLP000EV.pdf');
  });
});

describe('Applied Mathematics independently reviewed 2020 Higher tasks', () => {
  it('retains separately marked speeds and forces, original diagrams and canonical topic joins', () => {
    const expected = [3, 3, 4, 4, 4, 4, 4, 3, 3, 4];
    const cards = REVIEWED_CARDS.filter(item => item.year === 2020);
    expect(cards).toHaveLength(36);
    expect(cards.every(item => item.level === 'higher')).toBe(true);
    for (let q = 1; q <= 10; q++) {
      const tasks = cards.filter(item => item.questionRef.match(/Q(\d+)/)?.[1] === String(q));
      expect(tasks).toHaveLength(expected[q - 1]);
      expect(tasks.reduce((sum, item) => sum + item.totalMarks, 0)).toBe(50);
    }
    const fileid = 'LC020ALP000EV.pdf';
    const url = preferredAnswersUrl('applied-mathematics', 2020, fileid, 'unused');
    expect(url).toBe(`/paper-answers/2020/${fileid}.json`);
    const map = JSON.parse(readFileSync(`public${url}`, 'utf8'));
    expect(isAnswerMap(map)).toBe(true);
    const original = JSON.parse(readFileSync(`scripts/paper-trail/answers/2020/${fileid}.json`, 'utf8'));
    for (const q of original.q) expect(map.q.find((item: { n: string }) => item.n === q.n)).toMatchObject(q);
    for (const task of review2020.papers[0].tasks) {
      expect(specificationContainsId(resolveCurriculumSpecification('applied-mathematics', 2020)!, task.topicId)).toBe(true);
      expect(examTopicIdsForQuestion('applied-mathematics', 'higher', 2020, 'main', task.ref.match(/^Q(\d+)/)![1], 'single', 'ev', fileid))
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
    expect(['a', 'b'].map(s => card(`am-2020-hl-5-a-i-${s}`).totalMarks)).toEqual([15, 5]);
    expect(['horizontal', 'vertical'].map(s => card(`am-2020-hl-7-b-${s}`).totalMarks)).toEqual([5, 20]);
    expect(card('am-2020-hl-2-a-ii').totalMarks).toBe(10);
    expect(card('am-2020-hl-4-b-i').totalMarks).toBe(5);
    expect(card('am-2020-hl-5-a-i-a').rubric.allocations[0].guidance).toContain('shared collision equations');
    expect(card('am-2020-hl-5-a-i-b').rubric.allocations[0].guidance).toContain('second of the two final');
    expect(card('am-2020-hl-6-b-ii').topicId).toBe('applied-mathematics-2-2');
    expect(card('am-2020-hl-4-a-ii').topicId).toBe('applied-mathematics-2-0');
    expect(card('am-2020-hl-5-a-i-a').rubric.solution.regions![0][1]).toBeLessThan(.26);
    expect(card('am-2020-hl-9-a').rubric.solution.regions![0][1]).toBeLessThan(.22);
    expect(card('am-2020-hl-4-b-ii').sourceMaterial!.regions![0][3]).toBeGreaterThan(.892);
  });
});

describe('Applied Mathematics independently reviewed 2019 tasks', () => {
  it('retains independently marked outputs, complete source crops and topic joins', () => {
    const expected = { higher: [6, 3, 5, 6, 4, 5, 5, 4, 2, 6], ordinary: [5, 6, 5, 6, 5, 4, 4, 6, 3] };
    for (const level of ['higher', 'ordinary'] as const) {
      const cards = REVIEWED_CARDS.filter(item => item.year === 2019 && item.level === level);
      expect(cards).toHaveLength(level === 'higher' ? 46 : 44);
      for (let q = 1; q <= expected[level].length; q++) {
        const tasks = cards.filter(item => item.questionRef.match(/Q(\d+)/)?.[1] === String(q));
        expect(tasks).toHaveLength(expected[level][q - 1]);
        expect(tasks.reduce((sum, item) => sum + item.totalMarks, 0)).toBe(50);
      }
      const fileid = `LC020${level === 'higher' ? 'A' : 'G'}LP000EV.pdf`;
      const url = preferredAnswersUrl('applied-mathematics', 2019, fileid, 'unused');
      expect(url).toBe(`/paper-answers/2019/${fileid}.json`);
      expect(isAnswerMap(JSON.parse(readFileSync(`public${url}`, 'utf8')))).toBe(true);
      for (const task of review2019.papers.find(p => p.level === level)!.tasks) {
        expect(specificationContainsId(resolveCurriculumSpecification('applied-mathematics', 2019)!, task.topicId)).toBe(true);
        expect(examTopicIdsForQuestion('applied-mathematics', level, 2019, 'main', task.ref.match(/^Q(\d+)/)![1], 'single', 'ev', fileid))
          .toEqual(expect.arrayContaining(task.examTopicIds));
      }
    }
    expect(['wedge', 'particle'].map(s => card(`am-2019-hl-4-b-i-${s}`).totalMarks)).toEqual([5, 5]);
    expect(['p', 'q'].map(s => card(`am-2019-hl-4-b-ii-${s}`).totalMarks)).toEqual([5, 10]);
    expect(['magnitude', 'direction'].map(s => card(`am-2019-hl-7-a-${s}`).totalMarks)).toEqual([20, 5]);
    expect(['horizontal', 'vertical'].map(s => card(`am-2019-hl-7-b-ii-${s}`).totalMarks)).toEqual([5, 5]);
    expect(['ab', 'c'].map(s => card(`am-2019-hl-10-a-i-${s}`).totalMarks)).toEqual([15, 5]);
    expect(['c', 'd'].map(s => card(`am-2019-ol-7-a-i-${s}`).totalMarks)).toEqual([10, 10]);
    expect(['i', 'ii'].map(s => card(`am-2019-ol-9-a-${s}`).totalMarks)).toEqual([20, 5]);
    expect(card('am-2019-hl-2-a').totalMarks).toBe(25);
    expect(card('am-2019-hl-5-b-i').totalMarks).toBe(20);
    expect(card('am-2019-ol-4-a-i').totalMarks).toBe(10);
    expect(card('am-2019-ol-3-iii').rubric.solution.pages).toEqual([6, 7]);
    expect(card('am-2019-ol-3-iii').rubric.solution.regions).toHaveLength(2);
    expect(card('am-2019-hl-7-b-i').rubric.allocations[0].guidance).toContain('remaining three');
    expect(card('am-2019-hl-10-a-i-ab').rubric.allocations[0].guidance).toContain('separately practised');
    expect(card('am-2019-hl-4-a-i').sourceMaterial!.regions![0][1]).toBeLessThan(.528);
    expect(card('am-2019-ol-3-v').sourceMaterial!.regions![0][3]).toBeGreaterThan(.454);
    expect(card('am-2019-ol-5-b-ii').sourceMaterial!.regions![0][3]).toBeGreaterThan(.551);
  });
});

describe('Applied Mathematics independently reviewed 2018 tasks', () => {
  it('retains independently marked outputs, complete source crops and topic joins', () => {
    const expected = { higher: [3, 4, 6, 5, 5, 4, 2, 4, 2, 3], ordinary: [5, 4, 5, 5, 5, 4, 6, 8, 4] };
    for (const level of ['higher', 'ordinary'] as const) {
      const cards = REVIEWED_CARDS.filter(item => item.year === 2018 && item.level === level);
      expect(cards).toHaveLength(level === 'higher' ? 38 : 46);
      for (let q = 1; q <= expected[level].length; q++) {
        const tasks = cards.filter(item => item.questionRef.match(/Q(\d+)/)?.[1] === String(q));
        expect(tasks).toHaveLength(expected[level][q - 1]);
        expect(tasks.reduce((sum, item) => sum + item.totalMarks, 0)).toBe(50);
      }
      const fileid = `LC020${level === 'higher' ? 'A' : 'G'}LP000EV.pdf`;
      const url = preferredAnswersUrl('applied-mathematics', 2018, fileid, 'unused');
      expect(url).toBe(`/paper-answers/2018/${fileid}.json`);
      expect(isAnswerMap(JSON.parse(readFileSync(`public${url}`, 'utf8')))).toBe(true);
      for (const task of review2018.papers.find(p => p.level === level)!.tasks) {
        expect(specificationContainsId(resolveCurriculumSpecification('applied-mathematics', 2018)!, task.topicId)).toBe(true);
        expect(examTopicIdsForQuestion('applied-mathematics', level, 2018, 'main', task.ref.match(/^Q(\d+)/)![1], 'single', 'ev', fileid))
          .toEqual(expect.arrayContaining(task.examTopicIds));
      }
    }
    expect(['times', 'ratio'].map(s => card(`am-2018-hl-3-b-i-${s}`).totalMarks)).toEqual([10, 5]);
    expect(['range', 'angle'].map(s => card(`am-2018-hl-3-b-ii-${s}`).totalMarks)).toEqual([5, 5]);
    expect(['x', 'y'].map(s => card(`am-2018-ol-6-b-${s}`).totalMarks)).toEqual([25, 5]);
    expect(['horizontal', 'vertical'].map(s => card(`am-2018-ol-7-ii-${s}`).totalMarks)).toEqual([5, 5]);
    expect(card('am-2018-hl-4-b-i').totalMarks).toBe(5);
    expect(card('am-2018-ol-4-b-i').totalMarks).toBe(10);
    expect(card('am-2018-hl-5-a-i').totalMarks).toBe(15);
    expect(card('am-2018-hl-5-b-i').totalMarks).toBe(20);
    expect(card('am-2018-ol-1-iii').rubric.allocations[0].credit).toEqual([0, 15]);
    expect(card('am-2018-ol-1-iii').rubric.allocations[0].guidance).toContain('no separate attempt tariff');
    expect(appliedMathematicsMarks(card('am-2018-ol-1-iii'), {
      'applied:allocation-1:credit': 15, 'applied:allocation-1:errors': 1,
    })).toBe(12);
    expect(card('am-2018-ol-9-a-i').rubric.allocations[0].guidance).toContain('weight of fluid');
    expect(card('am-2018-hl-4-b-iii').sourceMaterial!.regions![0][3]).toBeGreaterThan(.925);
    expect(card('am-2018-hl-6-b-ii').sourceMaterial!.regions![0][3]).toBeGreaterThan(.91);
    expect(card('am-2018-ol-4-a-i').sourceMaterial!.regions![0][1]).toBeLessThan(.46);
    expect(card('am-2018-ol-4-b-iii').sourceMaterial!.regions![0][3]).toBeGreaterThan(.885);
    expect(card('am-2018-ol-6-b-x').rubric.solution.regions![0][1]).toBeLessThan(.4);
  });
});

describe('Applied Mathematics independently reviewed 2017 tasks', () => {
  it('retains independently marked outputs, complete source crops and topic joins', () => {
    const expected = { higher: [4, 4, 5, 7, 4, 4, 3, 4, 3, 5], ordinary: [6, 5, 5, 6, 5, 4, 5, 8, 2] };
    for (const level of ['higher', 'ordinary'] as const) {
      const cards = REVIEWED_CARDS.filter(item => item.year === 2017 && item.level === level);
      expect(cards).toHaveLength(level === 'higher' ? 43 : 46);
      for (let q = 1; q <= expected[level].length; q++) {
        const tasks = cards.filter(item => item.questionRef.match(/Q(\d+)/)?.[1] === String(q));
        expect(tasks).toHaveLength(expected[level][q - 1]);
        expect(tasks.reduce((sum, item) => sum + item.totalMarks, 0)).toBe(50);
      }
      const fileid = `LC020${level === 'higher' ? 'A' : 'G'}LP000EV.pdf`;
      const url = preferredAnswersUrl('applied-mathematics', 2017, fileid, 'unused');
      expect(url).toBe(`/paper-answers/2017/${fileid}.json`);
      expect(isAnswerMap(JSON.parse(readFileSync(`public${url}`, 'utf8')))).toBe(true);
      for (const task of review2017.papers.find(p => p.level === level)!.tasks) {
        expect(specificationContainsId(resolveCurriculumSpecification('applied-mathematics', 2017)!, task.topicId)).toBe(true);
        expect(examTopicIdsForQuestion('applied-mathematics', level, 2017, 'main', task.ref.match(/^Q(\d+)/)![1], 'single', 'ev', fileid))
          .toEqual(expect.arrayContaining(task.examTopicIds));
      }
    }
    expect(['i', 'ii'].map(s => card(`am-2017-hl-5-a-${s}`).totalMarks)).toEqual([10, 10]);
    expect(['i', 'ii', 'iii'].map(s => card(`am-2017-hl-8-b-${s}`).totalMarks)).toEqual([20, 5, 5]);
    expect(['i', 'ii'].map(s => card(`am-2017-hl-9-b-${s}`).totalMarks)).toEqual([20, 10]);
    expect(['min', 'max'].map(s => card(`am-2017-hl-6-b-ii-${s}`).totalMarks)).toEqual([5, 5]);
    expect(['q', 'p'].map(s => card(`am-2017-hl-7-a-${s}`).totalMarks)).toEqual([20, 5]);
    expect(['time', 'distance'].map(s => card(`am-2017-hl-10-a-ii-${s}`).totalMarks)).toEqual([5, 5]);
    expect(['x', 'y'].map(s => card(`am-2017-ol-6-b-${s}`).totalMarks)).toEqual([25, 5]);
    expect(card('am-2017-ol-4-a-i').totalMarks).toBe(5);
    expect(card('am-2017-ol-7-b-iii').totalMarks).toBe(10);
    expect(card('am-2017-hl-8-b-ii').topicId).toBe('applied-mathematics-2-10');
    for (const suffix of ['horizontal', 'inclined']) {
      const flight = card(`am-2017-hl-3-a-ii-${suffix}`);
      expect(flight.totalMarks).toBe(5);
      expect(flight.questionText).toContain('reach P');
      expect(flight.stem).toContain('time to reach the ground');
      expect(flight.rubric.allocations[0].guidance).toContain('last 5 marks');
      expect(flight.rubric.solution.regions![0][3]).toBeGreaterThan(.81);
    }
    expect(card('am-2017-hl-6-a').sourceMaterial!.regions![0][1]).toBeLessThan(.467);
    expect(card('am-2017-ol-5-b-ii').sourceMaterial!.regions![0][3]).toBeGreaterThan(.59);
    expect(card('am-2017-hl-9-a').rubric.solution.regions![0][1]).toBeLessThan(.4);
    expect(card('am-2017-ol-8-b-ii').rubric.solution.regions![0][1]).toBeLessThan(.49);
  });
});

describe('Applied Mathematics independently reviewed 2016 tasks', () => {
  it('retains independently marked outputs, complete source crops and topic joins', () => {
    const expected = { higher: [4, 4, 4, 4, 5, 5, 4, 4, 2, 4], ordinary: [6, 6, 4, 6, 5, 4, 6, 6, 4] };
    for (const level of ['higher', 'ordinary'] as const) {
      const cards = REVIEWED_CARDS.filter(item => item.year === 2016 && item.level === level);
      expect(cards).toHaveLength(level === 'higher' ? 40 : 47);
      for (let q = 1; q <= expected[level].length; q++) {
        const tasks = cards.filter(item => item.questionRef.match(/Q(\d+)/)?.[1] === String(q));
        expect(tasks).toHaveLength(expected[level][q - 1]);
        expect(tasks.reduce((sum, item) => sum + item.totalMarks, 0)).toBe(50);
      }
      const fileid = `LC020${level === 'higher' ? 'A' : 'G'}LP000EV.pdf`;
      const url = preferredAnswersUrl('applied-mathematics', 2016, fileid, 'unused');
      expect(url).toBe(`/paper-answers/2016/${fileid}.json`);
      expect(isAnswerMap(JSON.parse(readFileSync(`public${url}`, 'utf8')))).toBe(true);
      for (const task of review2016.papers.find(p => p.level === level)!.tasks) {
        expect(specificationContainsId(resolveCurriculumSpecification('applied-mathematics', 2016)!, task.topicId)).toBe(true);
        expect(examTopicIdsForQuestion('applied-mathematics', level, 2016, 'main', task.ref.match(/^Q(\d+)/)![1], 'single', 'ev', fileid))
          .toEqual(expect.arrayContaining(task.examTopicIds));
      }
    }
    expect(['b', 'difference'].map(s => card(`am-2016-ol-2-iv-${s}`).totalMarks)).toEqual([5, 5]);
    expect(['horizontal', 'vertical'].map(s => card(`am-2016-ol-7-ii-${s}`).totalMarks)).toEqual([5, 5]);
    expect(['i', 'ii'].map(s => card(`am-2016-ol-6-a-${s}`).totalMarks)).toEqual([15, 5]);
    expect(['x', 'y'].map(s => card(`am-2016-ol-6-b-${s}`).totalMarks)).toEqual([25, 5]);
    expect(card('am-2016-hl-2-a-ii').totalMarks).toBe(5);
    expect(card('am-2016-hl-4-a-i').totalMarks).toBe(15);
    expect(card('am-2016-ol-4-b-i').totalMarks).toBe(10);
    for (const suffix of ['i', 'ii']) {
      const beam = card(`am-2016-hl-7-a-${suffix}`);
      expect(beam.stem).toContain('surface should be rough');
      expect(beam.rubric.allocations[0].guidance).toContain('either assumption');
      expect(beam.rubric.solution.regions![0][1]).toBeLessThan(.30);
      expect(beam.rubric.solution.regions![0][3]).toBeGreaterThan(.9);
    }
    expect(card('am-2016-hl-4-a-i').sourceMaterial!.regions![0][1]).toBeLessThan(.469);
    expect(card('am-2016-hl-4-b-ii').sourceMaterial!.regions![0][3]).toBeGreaterThan(.944);
    expect(card('am-2016-ol-4-a-i').sourceMaterial!.regions![0][1]).toBeLessThan(.405);
    expect(card('am-2016-hl-6-a-ii').rubric.solution.regions![0][3]).toBeGreaterThan(.85);
  });
});

describe('Applied Mathematics independently reviewed 2015 tasks', () => {
  it('retains independently marked outputs, complete source crops and topic joins', () => {
    const expected = { higher: [3, 4, 4, 5, 3, 4, 6, 4, 3, 7], ordinary: [5, 5, 5, 5, 5, 4, 3, 5, 2] };
    for (const level of ['higher', 'ordinary'] as const) {
      const cards = REVIEWED_CARDS.filter(item => item.year === 2015 && item.level === level);
      expect(cards).toHaveLength(level === 'higher' ? 43 : 39);
      for (let q = 1; q <= expected[level].length; q++) {
        const tasks = cards.filter(item => item.questionRef.match(/Q(\d+)/)?.[1] === String(q));
        expect(tasks).toHaveLength(expected[level][q - 1]);
        expect(tasks.reduce((sum, item) => sum + item.totalMarks, 0)).toBe(50);
      }
      const fileid = `LC020${level === 'higher' ? 'A' : 'G'}LP000EV.pdf`;
      const url = preferredAnswersUrl('applied-mathematics', 2015, fileid, 'unused');
      expect(url).toBe(`/paper-answers/2015/${fileid}.json`);
      expect(isAnswerMap(JSON.parse(readFileSync(`public${url}`, 'utf8')))).toBe(true);
      for (const task of review2015.papers.find(p => p.level === level)!.tasks) {
        expect(specificationContainsId(resolveCurriculumSpecification('applied-mathematics', 2015)!, task.topicId)).toBe(true);
        expect(examTopicIdsForQuestion('applied-mathematics', level, 2015, 'main', task.ref.match(/^Q(\d+)/)![1], 'single', 'ev', fileid))
          .toEqual(expect.arrayContaining(task.examTopicIds));
      }
    }
    expect(['shm', 'period'].map(s => card(`am-2015-hl-6-a-ii-${s}`).totalMarks)).toEqual([10, 5]);
    expect(['sketch', 'shade'].map(s => card(`am-2015-hl-10-a-iii-${s}`).totalMarks)).toEqual([5, 5]);
    expect(['i', 'ii'].map(s => card(`am-2015-hl-5-a-${s}`).totalMarks)).toEqual([15, 15]);
    expect(['x', 'y'].map(s => card(`am-2015-ol-6-b-${s}`).totalMarks)).toEqual([25, 5]);
    expect(card('am-2015-hl-2-a-i').totalMarks).toBe(15);
    expect(card('am-2015-hl-3-a-ii').totalMarks).toBe(5);
    expect(card('am-2015-hl-4-a-i').sourceMaterial!.pages).toEqual([3]);
    expect(card('am-2015-hl-4-b-i').sourceMaterial!.pages).toEqual([4]);
    expect(card('am-2015-hl-4-a-iii').topicId).toBe('applied-mathematics-2-4');
    expect(card('am-2015-ol-9-b').sourceMaterial!.regions![0][3]).toBeGreaterThan(.878);
    const map = JSON.parse(readFileSync('public/paper-answers/2015/LC020ALP000EV.pdf.json', 'utf8'));
    expect(map.q.find((q: { n: string }) => q.n === '4').paperRegion.map((r: { p: number }) => r.p)).toEqual([3, 4]);
  });
});

describe('Applied Mathematics independently reviewed 2014 tasks', () => {
  it('retains independently marked outputs, complete source crops and topic joins', () => {
    const expected = { higher: [4, 5, 3, 5, 4, 4, 8, 3, 4, 5], ordinary: [5, 5, 5, 5, 4, 4, 6, 6, 4] };
    for (const level of ['higher', 'ordinary'] as const) {
      const cards = REVIEWED_CARDS.filter(item => item.year === 2014 && item.level === level);
      expect(cards).toHaveLength(level === 'higher' ? 45 : 44);
      for (let q = 1; q <= expected[level].length; q++) {
        const tasks = cards.filter(item => item.questionRef.match(/Q(\d+)/)?.[1] === String(q));
        expect(tasks).toHaveLength(expected[level][q - 1]);
        expect(tasks.reduce((sum, item) => sum + item.totalMarks, 0)).toBe(50);
      }
      const fileid = `LC020${level === 'higher' ? 'A' : 'G'}LP000EV.pdf`;
      const url = preferredAnswersUrl('applied-mathematics', 2014, fileid, 'unused');
      expect(url).toBe(`/paper-answers/2014/${fileid}.json`);
      expect(isAnswerMap(JSON.parse(readFileSync(`public${url}`, 'utf8')))).toBe(true);
      for (const task of review2014.papers.find(p => p.level === level)!.tasks) {
        expect(specificationContainsId(resolveCurriculumSpecification('applied-mathematics', 2014)!, task.topicId)).toBe(true);
        expect(examTopicIdsForQuestion('applied-mathematics', level, 2014, 'main', task.ref.match(/^Q(\d+)/)![1], 'single', 'ev', fileid))
          .toEqual(expect.arrayContaining(task.examTopicIds));
      }
    }
    expect(['particle', 'wedge'].map(s => card(`am-2014-hl-4-b-i-${s}`).totalMarks)).toEqual([5, 5]);
    expect(['rod', 'hemisphere'].map(s => card(`am-2014-hl-7-b-i-${s}`).totalMarks)).toEqual([5, 5]);
    expect(card('am-2014-ol-4-b-i').totalMarks).toBe(10);
    expect(card('am-2014-hl-4-b-ii').totalMarks).toBe(20);
    expect(card('am-2014-hl-9-a').totalMarks).toBe(20);
    expect(card('am-2014-ol-9-a-principle').totalMarks).toBe(5);
    expect(card('am-2014-hl-5-a-i').sourceMaterial!.regions![0][1]).toBeLessThan(.077);
    expect(card('am-2014-hl-7-b-i-rod').rubric.solution.regions![0][1]).toBeLessThan(.07);
    expect(card('am-2014-ol-8-b-i').rubric.solution.regions![0][1]).toBeLessThan(.33);
  });
});

describe('Applied Mathematics independently reviewed 2013 tasks', () => {
  it('retains independently marked outputs, complete source crops and topic joins', () => {
    const expected = { higher: [4, 3, 3, 3, 5, 4, 4, 3, 3, 5], ordinary: [5, 6, 5, 5, 3, 4, 5, 6, 2] };
    for (const level of ['higher', 'ordinary'] as const) {
      const cards = REVIEWED_CARDS.filter(item => item.year === 2013 && item.level === level);
      expect(cards).toHaveLength(level === 'higher' ? 37 : 41);
      for (let q = 1; q <= expected[level].length; q++) {
        const tasks = cards.filter(item => item.questionRef.match(/Q(\d+)/)?.[1] === String(q));
        expect(tasks).toHaveLength(expected[level][q - 1]);
        expect(tasks.reduce((sum, item) => sum + item.totalMarks, 0)).toBe(50);
      }
      const fileid = `LC020${level === 'higher' ? 'A' : 'G'}LP000EV.pdf`;
      const url = preferredAnswersUrl('applied-mathematics', 2013, fileid, 'unused');
      expect(url).toBe(`/paper-answers/2013/${fileid}.json`);
      expect(isAnswerMap(JSON.parse(readFileSync(`public${url}`, 'utf8')))).toBe(true);
      for (const task of review2013.papers.find(p => p.level === level)!.tasks) {
        expect(specificationContainsId(resolveCurriculumSpecification('applied-mathematics', 2013)!, task.topicId)).toBe(true);
        expect(examTopicIdsForQuestion('applied-mathematics', level, 2013, 'main', task.ref.match(/^Q(\d+)/)![1], 'single', 'ev', fileid))
          .toEqual(expect.arrayContaining(task.examTopicIds));
      }
    }
    expect(['velocity', 'distance'].map(s => card(`am-2013-hl-10-b-i-${s}`).totalMarks)).toEqual([5, 10]);
    expect(['v1', 'v2'].map(s => card(`am-2013-hl-9-a-${s}`).totalMarks)).toEqual([20, 5]);
    expect(['c', 'a'].map(s => card(`am-2013-hl-7-b-i-${s}`).totalMarks)).toEqual([10, 10]);
    expect(card('am-2013-hl-7-b-i-a').questionRef).toBe('2013 HL Q7(b)(i) — Reaction at A');
    expect(card('am-2013-hl-10-c').questionRef).toBe('2013 HL Q10(c)');
    expect(card('am-2013-hl-6-a-i').topicId).toBe('applied-mathematics-2-11');
    expect(card('am-2013-hl-6-a-ii').topicId).toBe('applied-mathematics-2-13');
    expect(card('am-2013-hl-9-a-v2').rubric.solution.regions![0][1]).toBeLessThan(.64);
    expect(card('am-2013-ol-5-i').sourceMaterial!.regions![0][1]).toBeLessThan(.657);
    expect(card('am-2013-ol-1-v').rubric.solution.regions![0][3]).toBeGreaterThan(.90);
  });

  it('keeps separately priced lamina coordinates while scoring common preparation once', () => {
    for (const year of [2010, 2011, 2012, 2013]) {
      const x = card(`am-${year}-ol-6-b${year === 2013 ? '-x' : ''}`);
      const y = card(`am-${year}-ol-6-b-y`);
      expect(x.practiceFocus).toContain('Horizontal coordinate');
      expect(y.practiceFocus).toBe('Vertical coordinate');
      expect(x.totalMarks).toBe(year < 2012 ? 15 : 25);
      expect(y.totalMarks).toBe(5);
      expect(x.questionText).toBe(y.questionText);
      expect(x.sourceMaterial).toMatchObject({ pages: y.sourceMaterial!.pages, regions: y.sourceMaterial!.regions });
    }
  });
});

describe('Applied Mathematics marking and source reader', () => {
  it('passes both continued solution crops to the reader in source order', async () => {
    const c = card('am-2019-ol-3-iii');
    render(<SessionScreen cards={[c]} subjectLabel="Applied Mathematics" onGrade={vi.fn()} onFinish={vi.fn()} onExit={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    fireEvent.click(screen.getByRole('button', { name: /Read.*worked solution/i }));
    for (const [index, p] of c.rubric.solution.pages.entries()) {
      await waitFor(() => expect(crop).toHaveBeenCalledWith(expect.objectContaining({
        region: [{ p, r: c.rubric.solution.regions![index] }],
      })));
    }
    fireEvent.click(screen.getByRole('button', { name: 'Next source page' }));
    expect(screen.getByRole('link', { name: 'Open the original marking scheme' }).getAttribute('href')).toMatch(/#page=7$/);
    expect(screen.getByRole('button', { name: 'Go to source page 2' }).getAttribute('aria-current')).toBe('page');
  });

  it('allows only published credit, deducts locally, and prevents negative marks', () => {
    const c = card('am-2026-hl-2-iv');
    expect(appliedMathematicsMarks(c, { 'applied:allocation-1:credit': 5, 'applied:allocation-1:errors': 2,
      'applied:allocation-2:credit': 5, 'applied:allocation-2:slips': 1 })).toBe(4);
    expect(appliedMathematicsMarks(c, { 'applied:allocation-1:credit': 100 })).toBe(0);
    expect(appliedMathematicsMarks(c, { 'applied:allocation-1:credit': NaN })).toBe(0);
    expect(appliedMathematicsMarks(c, { 'applied:allocation-1:credit': 5, 'applied:allocation-1:errors': -3 })).toBe(5);
    expect(appliedMathematicsMarks(card('am-2026-ol-2-i'), { 'applied:allocation-1:credit': 12 })).toBe(12);
    expect(appliedMathematicsMarks(card('am-2026-ol-2-i'), { 'applied:allocation-1:credit': 10 })).toBe(0);
  });

  it('rejects malformed scheme pages or crop geometry', () => {
    const c = card('am-2026-hl-1-a-i');
    for (const solution of [
      { ...c.rubric.solution, pages: [0] },
      { ...c.rubric.solution, regions: [[0, 0.8, 1, 0.2]] },
      { ...c.rubric.solution, regions: [[0, 0, 1, Infinity]] },
    ]) expect(tariffReconciles({ ...c, rubric: { ...c.rubric, solution } } as AppliedCard)).toBe(false);
  });

  it('opens the paper before reveal and the cropped scheme only after reveal', async () => {
    const c = card('am-2026-ol-3-i-4kg');
    render(<SessionScreen cards={[c]} subjectLabel="Applied Mathematics" onGrade={vi.fn()} onFinish={vi.fn()} onExit={vi.fn()} />);
    expect(screen.getByText('Practise: 4 kg mass')).toBeTruthy();
    expect(screen.queryByRole('button', { name: /Read.*worked solution/i })).toBeNull();
    const question = screen.getByRole('button', { name: /Read.*question and context/i });
    fireEvent.click(question);
    await waitFor(() => expect(vaultPdf).toHaveBeenCalledWith(expect.stringContaining('applied-mathematics%2F2026%2Fpaper%2FLC020GLP000EV.pdf')));
    fireEvent.keyDown(screen.getByRole('dialog'), { key: 'Escape' });
    await waitFor(() => expect(document.activeElement).toBe(question));
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    fireEvent.click(screen.getByRole('button', { name: /Read.*worked solution/i }));
    await waitFor(() => expect(vaultPdf).toHaveBeenCalledWith(expect.stringContaining('applied-mathematics%2F2026%2Fscheme%2FLC020GLP000EV.pdf')));
    await waitFor(() => expect(crop).toHaveBeenCalledWith(expect.objectContaining({
      region: [{ p: c.rubric.solution.pages[0], r: c.rubric.solution.regions![0] }],
    })));
    fireEvent.click(screen.getByRole('button', { name: 'Close worked solution' }));
    fireEvent.click(screen.getByRole('button', { name: 'Set Published step 1 to 5 marks' }));
    expect(screen.getByText('Your mark: 5 / 5')).toBeTruthy();
  });
});
