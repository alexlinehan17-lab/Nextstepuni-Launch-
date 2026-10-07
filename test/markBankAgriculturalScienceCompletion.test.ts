import { describe, expect, it } from 'vitest';
import { CARDS as higher } from '../components/MarkBank/cards/agricultural-science/higher';
import { CARDS as ordinary } from '../components/MarkBank/cards/agricultural-science/ordinary';
import review from '../scripts/markbank/authored/agricultural-science-reviewed-tasks.json';
import { isPointCard, tariffReconciles } from '../types/markBank';
import { marksClaimed } from '../components/MarkBank/SessionScreen';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import atlas from '../data/examTopics/agricultural-science-question-runtime.json';
import { examTopicIdsForQuestion } from '../data/examTopics/registry';
import { siblingsFor } from '../components/PaperTrail/topics';
import { preferredAnswersUrl } from '../components/PaperTrail/vaultResolve';
import { paperRegionFor } from '../components/PaperTrail/paperRegion';
import type { PaperAnswerMap } from '../types/paperTrail';
import { findCanonicalTopic, resolveCurriculumSpecification } from '../curriculumRegistry';
import { cardsForTopic } from '../components/MarkBank/deck';

const cards = [...higher, ...ordinary];
const get = (id: string) => {
  const card = cards.find(c => c.id === id);
  if (!card || !isPointCard(card)) throw new Error(`Missing reviewed point card ${id}`);
  return card;
};

describe('Agricultural Science reviewed additions (full audit still in progress)', () => {
  it('expands every three-of-four udder-labelling route at the published three-mark tariff', () => {
    const routes = cards.filter(c => c.id.startsWith('agsci-2023-hl-q18ai-route-'));
    expect(routes.map(c => c.id.split('-').at(-1)).sort()).toEqual(['abc', 'abd', 'acd', 'bcd']);
    for (const card of routes) {
      expect(card.totalMarks).toBe(3);
      expect(card.sourceMaterial?.pages).toEqual([37]);
      expect(card.questionText).toBe('Label any three parts of the structure of the udder.');
      expect(tariffReconciles(card)).toBe(true);
    }
    expect(get('agsci-2023-hl-q18ai-route-abc').rows[1].verbatim).toBe('Median suspensory ligament');
  });

  it('keeps the separate ram reason pools and their complete 3+1 marking menus', () => {
    const e = get('agsci-2022-ol-q2bii-route-e');
    const f = get('agsci-2022-ol-q2bii-route-f');
    expect(e.rows[0].group?.options).toHaveLength(8);
    expect(f.rows[0].group?.options).toHaveLength(5);
    expect(f.rows[0].group?.options).not.toContain('easy lambing');
    for (const card of [e, f]) {
      expect(card.totalMarks).toBe(4);
      expect(card.rows[0].group?.perOptionSteps).toEqual([3, 1]);
      expect(card.sourceMaterial?.pages).toEqual([5]);
      expect(tariffReconciles(card)).toBe(true);
      expect(marksClaimed(card, {}, { reasons: [0] })).toBe(3);
      expect(marksClaimed(card, {}, { reasons: [0, 1] })).toBe(4);
    }
  });

  it('retains partial credit for the two correct warning symbols', () => {
    const card = get('agsci-2025-ol-q8b');
    expect(card.rows[0].group?.options).toEqual(['2', '3']);
    expect(card.rows[0].group?.perOptionSteps).toEqual([3, 2]);
    expect(card.sourceMaterial?.pages).toEqual([9]);
    expect(tariffReconciles(card)).toBe(true);
    expect(marksClaimed(card, {}, { 'warning-signs': [0] })).toBe(3);
    expect(marksClaimed(card, {}, { 'warning-signs': [1] })).toBe(3);
    expect(marksClaimed(card, {}, { 'warning-signs': [0, 1] })).toBe(5);
  });

  it('retains the field photograph and the actual four-mark sketch criterion', () => {
    const card = get('agsci-2022-ol-q13bi');
    expect(card.topicId).toBe('agsci-2-3');
    expect(card.sourceMaterial?.pages).toEqual([22]);
    expect(card.rows).toEqual([{ id: 'sampling-pattern', kind: 'criterion', verbatim: 'W shape on photograph', marks: 4 }]);
  });

  it('ships every reviewed route with a source page and a reconciled tariff', () => {
    for (const task of review.tasks) {
      for (const id of task.cardIds) {
        const card = get(id);
        expect(card.totalMarks).toBe(task.marksPerRoute);
        expect(card.sourceMaterial?.pages).toContain(task.paperPage);
        expect(tariffReconciles(card)).toBe(true);
      }
    }
  });

  it('preserves both 2010 Q3 options and all 62 independently reviewed legacy tasks', () => {
    const legacy = cards.filter(card => card.year === 2010);
    expect(legacy).toHaveLength(62);
    expect(legacy.filter(card => card.questionRef.includes('Q3 Option One'))).toHaveLength(6);
    expect(legacy.filter(card => card.questionRef.includes('Q3 Option Two'))).toHaveLength(7);
    const diseaseRoutes = legacy.filter(card => card.id.startsWith('agsci-2010-hl-q3o2b-route-'));
    expect(diseaseRoutes.map(card => card.id).sort()).toEqual([
      'agsci-2010-hl-q3o2b-route-grass-tetany', 'agsci-2010-hl-q3o2b-route-hoose',
    ]);
    expect(diseaseRoutes.map(card => card.totalMarks)).toEqual([12, 12]);
    for (const card of legacy) {
      const specification = resolveCurriculumSpecification(card.subjectId, card.year)!;
      expect(card.specificationId).toBe(specification.id);
      expect(card.specVersion).toBe(specification.id);
      expect(card.specificationId).toBe('agricultural-science:legacy-current');
      expect(card.curriculumNodeIds?.length).toBeGreaterThan(0);
      for (const id of card.curriculumNodeIds!) expect(findCanonicalTopic(specification, id)).toBeDefined();
    }
  });

  it('expands both 2010 three-of-four tasks with their complete wording and tariffs', () => {
    const combinations = ['i-ii-iii', 'i-ii-iv', 'i-iii-iv', 'ii-iii-iv'];
    for (const [question, marks, rowCount] of [['q7a', 12, 3], ['q8c', 24, 6]] as const) {
      const routes = cards.filter(card => card.id.startsWith(`agsci-2010-hl-${question}-route-`));
      expect(routes.map(card => card.id.split('-route-')[1])).toEqual(combinations);
      expect(new Set(routes.map(card => card.questionText)).size).toBe(1);
      for (const candidate of routes) {
        const card = get(candidate.id);
        expect(card.totalMarks).toBe(marks);
        expect(card.rows).toHaveLength(rowCount);
        const claims = Object.fromEntries(card.rows.map(row => [row.id, [0, 1]]));
        expect(marksClaimed(card, {}, claims)).toBe(marks);
      }
    }
  });

  it('awards 2010 first-correct marks independently of the named instrument', () => {
    const card = get('agsci-2010-hl-q1e');
    for (const first of [0, 1, 2]) expect(marksClaimed(card, {}, { 'r-1': [first] })).toBe(6);
    expect(marksClaimed(card, {}, { 'r-1': [1, 2] })).toBe(8);
    expect(marksClaimed(card, {}, { 'r-1': [0, 1, 2] })).toBe(10);
  });

  it('keeps the minimum ewe/ram and fasting/hanging coverage in every marking allocation', () => {
    for (const [id, allocations] of [['agsci-2010-hl-q8a', 3], ['agsci-2010-hl-q9a', 2]] as const) {
      const card = get(id);
      expect(card.answerVariants).toHaveLength(allocations);
      for (const variant of card.answerVariants!) {
        expect(variant.rows).toHaveLength(2);
        expect(variant.rows.every(row => row.group!.claimMax >= 1)).toBe(true);
        const effective = { ...card, rows: variant.rows };
        expect(tariffReconciles(effective)).toBe(true);
        const claims = Object.fromEntries(variant.rows.map(row => [row.id, Array.from({ length: row.group!.claimMax }, (_, i) => i)]));
        expect(marksClaimed(effective, {}, claims)).toBe(card.totalMarks);
        expect(marksClaimed(effective, {}, { 'r-1': claims['r-1'] })).toBeLessThan(card.totalMarks);
      }
    }
  });

  it('requires the compulsory nitrogen-fixation point for full marks without inventing a zero-score gate', () => {
    const card = get('agsci-2010-hl-q6cii');
    expect(marksClaimed(card, { 'r-1': 'yes' }, {})).toBe(3);
    expect(marksClaimed(card, {}, { 'r-2': [0] })).toBe(3);
    expect(marksClaimed(card, { 'r-1': 'yes' }, { 'r-2': [0] })).toBe(6);
  });

  it('keeps mixed comparisons discoverable under each assessed current topic without duplicating cards', () => {
    const card = get('agsci-2010-hl-q8c-route-i-ii-iv');
    for (const topic of ['agsci-4-3-1', 'agsci-3-3-2', 'agsci-4-3-3']) {
      expect(cardsForTopic(topic, cards).filter(candidate => candidate.id === card.id)).toHaveLength(1);
      expect(findCanonicalTopic(resolveCurriculumSpecification('agricultural-science', 2026)!, topic)).toBeDefined();
    }
  });

  it('keeps complete legacy method menus and official drawing solutions', () => {
    expect(get('agsci-2010-hl-q4a').answerVariants).toHaveLength(3);
    expect(get('agsci-2010-hl-q4d').answerVariants).toHaveLength(2);
    expect(get('agsci-2010-hl-q5aii').rows[0].group?.options).toHaveLength(17);
    for (const id of ['agsci-2010-hl-q1b', 'agsci-2010-hl-q7bii']) {
      const card = get(id);
      expect(card.figure?.solution).toBe(true);
      expect(card.figure?.alt).toBeTruthy();
      expect(readFileSync(resolve(__dirname, `../public${card.figure!.src}`)).length).toBeGreaterThan(1000);
    }
  });

  it('makes each reviewed Mark Bank task directly browsable in Atlas under its reviewed topic', () => {
    expect(atlas.markBankCards).toHaveLength(70);
    for (const join of atlas.markBankCards) {
      const card = get(join.cardId);
      const task = review.tasks.find(task => task.cardIds.includes(join.cardId))!;
      const ids = examTopicIdsForQuestion('agricultural-science', card.level, card.year, 'main', join.n, 'single', 'ev', join.fileid);
      expect(ids).toEqual(task.examTopicIds);
      for (const topic of ids) {
        expect(siblingsFor('agricultural-science', topic).some(sibling =>
          sibling.year === join.year && sibling.fileid === join.fileid && sibling.n === join.n)).toBe(true);
      }
      const path = `/paper-answers/${join.year}/${join.fileid}.json`;
      expect(preferredAnswersUrl('agricultural-science', join.year, join.fileid, 'stale-storage')).toBe(path);
      const map = JSON.parse(readFileSync(resolve(__dirname, `../public${path}`), 'utf8'));
      const anchor = map.q.find((q: { n: string }) => q.n === join.n);
      expect(anchor.paperRegion[0].p).toBe(task.paperPage);
      expect(anchor.region[0].p).toBe(task.schemePage);
      if ('paperRegions' in task) expect(anchor.paperRegion).toEqual(task.paperRegions);
      if ('schemeRegions' in task) expect(anchor.region).toEqual(task.schemeRegions);
      expect(anchor.mode).toBe('crop');
      expect(anchor.parentN).toBe(card.questionRef.match(/Q(\d+)/)?.[1]);
    }
  });

  it('does not shorten whole-question crops when independently selectable parts are appended', () => {
    for (const join of atlas.markBankCards) {
      const map = JSON.parse(readFileSync(resolve(__dirname, `../public/paper-answers/${join.year}/${join.fileid}.json`), 'utf8')) as PaperAnswerMap;
      const old = map.q.filter(question => !question.parentN);
      for (const question of old) {
        expect(paperRegionFor(map.q, question.n), `${join.year} ${join.fileid} Q${question.n}`).toEqual(paperRegionFor(old, question.n));
      }
    }
  });
});
