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

  it('makes each reviewed Mark Bank task directly browsable in Atlas under its reviewed topic', () => {
    expect(atlas.markBankCards).toHaveLength(8);
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
