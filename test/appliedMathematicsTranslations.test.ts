import { describe, expect, it } from 'vitest';
import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/applied-maths/reviewed';
import { examTopicIdsForQuestion } from '../data/examTopics/registry';
import { topicsForPaper } from '../components/PaperTrail/topics';
import { isAnswerMap, preferredAnswersUrl, resolveSibling } from '../components/PaperTrail/vaultResolve';
import type { PaperAnswerMap, PaperLevel } from '../types/paperTrail';

type Translation = {
  year: number;
  papers: {
    level: PaperLevel;
    paperFileid: string;
    schemeFileid: string;
    practiceTaskCount: number;
    distinctAdditionalTasks: unknown[];
    questions: { n: string; canonicalTaskIds: string[]; taskTariffs: number[] }[];
  }[];
};
const directory = 'scripts/markbank/authoring/translated/applied-maths';
const reviews = readdirSync(directory).filter(name => name.endsWith('.json'))
  .map(name => JSON.parse(readFileSync(`${directory}/${name}`, 'utf8')) as Translation);

describe('reviewed Applied Mathematics Irish editions', () => {
  it('replaces all historical drawing exclusions with priced source-backed tasks', () => {
    expect(JSON.parse(readFileSync('scripts/markbank/authoring/exclusions/applied-maths.json', 'utf8'))).toEqual([]);
    const resolved = JSON.parse(readFileSync('scripts/markbank/authoring/exclusions/resolved/applied-maths.json', 'utf8')) as {
      originalExclusion: { ref: string }; cards: { id: string; questionRef: string; totalMarks: number; schemeCitation: string }[];
    }[];
    expect(resolved).toHaveLength(51);
    expect(new Set(resolved.map(entry => entry.originalExclusion.ref)).size).toBe(51);
    expect(resolved.flatMap(entry => entry.cards)).toHaveLength(60);
    for (const entry of resolved) {
      expect(entry.cards.length).toBeGreaterThan(0);
      for (const recorded of entry.cards) {
        const card = REVIEWED_CARDS.find(item => item.id === recorded.id)!;
        expect(card).toMatchObject(recorded);
        expect(recorded.totalMarks).toBeGreaterThan(0);
        expect(recorded.questionRef.startsWith(entry.originalExclusion.ref)).toBe(true);
        if (card.kind !== 'rubric') throw new Error(`${card.id} must retain source-backed marking`);
        if (card.rubric.system !== 'applied-mathematics') throw new Error(`${card.id} must use the Applied Mathematics rubric`);
        expect(card.rubric.solution.kind).toBe('source-scheme');
      }
    }
  });

  it.each(reviews.flatMap(review => review.papers.map(paper => ({ year: review.year, ...paper }))))(
    '$year $level preserves task correspondence and native Atlas source identity', paper => {
      const cards = REVIEWED_CARDS.filter(card => card.year === paper.year && card.level === paper.level);
      const linkedIds = paper.questions.flatMap(question => question.canonicalTaskIds);
      expect(linkedIds.length).toBe(new Set(linkedIds).size);
      expect(linkedIds.slice().sort()).toEqual(cards.map(card => card.id).sort());
      expect(cards).toHaveLength(paper.practiceTaskCount);
      expect(paper.distinctAdditionalTasks).toEqual([]);
      const url = preferredAnswersUrl('applied-mathematics', paper.year, paper.paperFileid, 'stale-storage');
      expect(url).toBe(`/paper-answers/${paper.year}/${paper.paperFileid}.json`);
      const map: PaperAnswerMap = JSON.parse(readFileSync(`public${url}`, 'utf8'));
      expect(isAnswerMap(map)).toBe(true);
      expect(map.paperFileid).toBe(paper.paperFileid);
      expect(map.schemeFileid).toBe(paper.schemeFileid);
      expect(map.q.map(question => question.n).sort()).toEqual(paper.questions.map(question => question.n).sort());
      const atlas = topicsForPaper('applied-mathematics', paper.year, paper.level, 'iv', paper.paperFileid)!;
      for (const question of paper.questions) {
        expect(atlas.q.some(item => item.n === question.n)).toBe(true);
        expect(question.canonicalTaskIds.map(id => cards.find(card => card.id === id)!.totalMarks))
          .toEqual(question.taskTariffs);
        const englishTopics = examTopicIdsForQuestion('applied-mathematics', paper.level, paper.year, 'main', question.n, 'single', 'ev', paper.paperFileid.replace('IV.pdf', 'EV.pdf'));
        expect(examTopicIdsForQuestion('applied-mathematics', paper.level, paper.year, 'main', question.n, 'single', 'iv', paper.paperFileid))
          .toEqual(englishTopics);
        expect(englishTopics.length).toBeGreaterThan(0);
        const mapped = map.q.find(item => item.n === question.n)!;
        expect(mapped.paperRegion!.length).toBeGreaterThan(0);
        expect((mapped.schemeRegion ?? mapped.region).length).toBeGreaterThan(0);
      }
      const originalPath = `scripts/paper-trail/answers/${paper.year}/${paper.paperFileid}.json`;
      if (existsSync(originalPath)) {
        const original: PaperAnswerMap = JSON.parse(readFileSync(originalPath, 'utf8'));
        for (const question of original.q) expect(map.q.find(item => item.n === question.n)).toMatchObject(question);
      }
    },
  );

  it('resolves the 2011 Ordinary Irish paper to its explicitly reviewed English scheme', () => {
    const resolved = resolveSibling({ subjectId: 'applied-mathematics', year: 2011, level: 'ordinary', lang: 'iv',
      fileid: 'LC020GLP000IV.pdf', n: '1', paperKey: 'single' });
    expect(decodeURIComponent(resolved!.paperUrl)).toContain('/paper/LC020GLP000IV.pdf');
    expect(decodeURIComponent(resolved!.schemeUrl!)).toContain('/scheme/LC020GLP000EV.pdf');
    expect(resolved!.answersUrl).toBe('/paper-answers/2011/LC020GLP000IV.pdf.json');
    const map: PaperAnswerMap = JSON.parse(readFileSync(`public${resolved!.answersUrl}`, 'utf8'));
    expect(map.schemeFileid).toBe('LC020GLP000EV.pdf');
    expect(map.q).toHaveLength(9);
  });

  it('retains the Irish 2012 Ordinary booklet pagination', () => {
    const map: PaperAnswerMap = JSON.parse(readFileSync('public/paper-answers/2012/LC020GLP000IV.pdf.json', 'utf8'));
    expect(map.q.find(question => question.n === '3')!.paperRegion!.map(region => region.p)).toEqual([3]);
    expect(map.q.find(question => question.n === '4')!.paperRegion!.map(region => region.p)).toEqual([4]);
    expect(map.q.find(question => question.n === '3')!.schemeRegion!.map(region => region.p)).toEqual([6, 7]);
  });
});
