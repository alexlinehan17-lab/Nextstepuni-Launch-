import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/irish/higher';
import authored from '../components/MarkBank/cards/irish/authored.json';
import review from '../scripts/markbank/authored/irish-literature-2024-review.json';
import papers from '../scripts/markbank/authored/irish-paper-reviews.json';
import inventory from '../scripts/markbank/authored/irish-archive-inventory.json';
import { curriculumNodeIdsForExamTopic, examTopicIdsForQuestion } from '../data/examTopics/registry';
import { tariffReconciles, type IrishRubric } from '../types/markBank';

const card = (key: string) => CARDS.find(c => c.id==='irish-2024-hl-p2-'+key)!;
const rubric = (key: string): IrishRubric => {
  const r=card(key).rubric;
  if(r.system!=='irish') throw new Error('Wrong system');
  return r;
};

describe('2024 Higher prescribed poetry and additional literature source review', () => {
  it('retains the two complete prescribed poems with the actual shared language allocation', () => {
    for(const option of ['a','b']) {
      const key='poetry-3a-'+option;
      expect(card(key).totalMarks).toBe(30);
      expect(rubric(key).criteria.map(c=>c.maxMarks)).toEqual([13,5,7,5]);
      expect(card(key).sourceMaterial?.pages).toEqual([option==='a'?9:10]);
      expect(card(key).questionText).toMatch(/\(i\).*\(ii\).*\(iii\)/);
      expect(tariffReconciles(card(key))).toBe(true);
    }
    const geibheann=rubric('poetry-3a-a').criteria;
    expect(geibheann[0].guidance.join(' ')).toContain('as 10 marc');
    expect(geibheann[2].guidance.join(' ')).toContain('bronn 0 ar an mír ar fad');
    expect(geibheann[2].guidance.join(' ')).toContain('Trí phointe eolais');
    const earrach=rubric('poetry-3a-b').criteria[2].guidance.join(' ');
    expect(earrach).toContain('1 mharc + 1 mharc');
    expect(earrach).toContain('gan dul thar 3 mharc as 5 mharc');
    expect(earrach).toContain('Níos mó ná dhá aidiacht');
    expect(earrach).toContain('Samplaí d’aidiachtaí');
    expect(review.selectionDecisions.find(d=>d.quote.includes('Roghnaigh dhá cheann'))?.reason)
      .toContain('not an enumerated menu of task prompts');
    expect(card('poetry-3a-b').questionText).not.toContain('shéimh');
  });

  it('covers all six printed additional-literature options and their complete scheme conditions', () => {
    for(const option of ['a','b','c','d','e','f']) {
      const key='literature-4-'+option;
      expect(card(key).totalMarks).toBe(40);
      expect(tariffReconciles(card(key))).toBe(true);
      expect(rubric(key).criteria.map(c=>c.maxMarks)).toEqual(option==='f'?[19,7,9,5]:[35,5]);
      if(option!=='f') expect(rubric(key).criteria[0].guidance.join(' ')).toContain('as 25 marc');
    }
    expect(rubric('literature-4-a').criteria[0].guidance.join(' ')).toContain('Na mná sa teach lóistín');
    expect(rubric('literature-4-b').criteria[0].guidance.join(' ')).toContain('na comórtais pheile');
    expect(rubric('literature-4-e').criteria[0].guidance.join(' ')).toContain('a chosaint ar na coirpigh');
    expect(rubric('literature-4-f').criteria[2].guidance.join(' ')).toContain('an pointe eolais is fearr');
    expect(card('literature-4-f').sourceMaterial?.pages).toEqual([13]);
  });

  it('maps every reviewed response to its exact paper/scheme pages and canonical topic', () => {
    const answerMap=JSON.parse(readFileSync('public/paper-answers/2024/LC001ALP200IV.pdf.json','utf8'));
    const expected: Array<[string,string,number[],number[]]> = [
      ['poetry-3a-a','F-3A-a',[9],[33,34,35]],
      ['poetry-3a-b','F-3A-b',[10],[35,36,37]],
      ['literature-4-a','X-4A',[12],[41,42,43]],
      ['literature-4-b','X-4B',[12],[41,43,44]],
      ['literature-4-c','X-4C',[12],[41,44,45]],
      ['literature-4-d','X-4D',[12],[41,45,46]],
      ['literature-4-e','X-4E',[12],[41,46,47]],
      ['literature-4-f','X-4F',[12,13],[47,48,49,50]],
    ];
    expect(review.cardIds.slice().sort()).toEqual(expected.map(([key])=>card(key).id).sort());
    for(const [key,n,pages,schemePages] of expected) {
      const q=answerMap.q.find((q:{n:string})=>q.n===n);
      expect(q.paperRegion.map((r:{p:number})=>r.p)).toEqual(pages);
      expect(q.region.map((r:{p:number})=>r.p)).toEqual(schemePages);
      const topics=examTopicIdsForQuestion('irish','higher',2024,'main',n,'p2','iv','LC001ALP200IV.pdf');
      expect(topics.flatMap(curriculumNodeIdsForExamTopic)).toContain(card(key).topicId);
      if(key.startsWith('poetry')) {
        expect(topics).toContain('irish-higher-prescribed-poetry-archive');
        expect(topics).not.toContain('irish-higher-studied-poetry-filiocht-roghnach');
      }
      if(n==='X-4F') expect(topics).toContain('irish-higher-danta-breise');
    }
  });

  it('reconciles every existing and added 2024 Higher Paper 2 card without deleting a whole question', () => {
    const all=authored.cards.filter(c=>c.year===2024 && c.level==='higher' && c.paper===2);
    expect(all).toHaveLength(72);
    expect(all.every(c=>'reviewedAt' in c && 'atlasQuestionId' in c && 'schemePages' in c)).toBe(true);
    expect(new Set(all.map(c=>'atlasQuestionId' in c ? c.atlasQuestionId : '')).size).toBe(72);
    expect(all.filter(c=>/-reading-[ab]-q[1-6]$/.test(c.id))).toHaveLength(12);
    expect(all.filter(c=>c.id.includes('-prose-'))).toHaveLength(6);
    expect(all.filter(c=>c.id.includes('-poetry-'))).toHaveLength(4);
    expect(all.filter(c=>c.id.includes('-literature-'))).toHaveLength(6);
    const paper=papers.find(p=>p.year===2024 && p.level==='higher')!;
    expect(paper.cardIds.slice().sort()).toEqual(all.map(c=>c.id).sort());
    expect(paper.atomicPracticeCardIds).toHaveLength(55);
    expect(paper.reviewedPaperPages).toEqual(Array.from({length:16},(_,i)=>i+1));
    expect(paper.openIssues).toEqual([]);
    expect(paper.examStructure.reading.marks + paper.examStructure.prose.marksPerRoute
      + paper.examStructure.poetry.marksPerRoute + paper.examStructure.additionalLiterature.marksPerRoute).toBe(200);
    const row=inventory.papers.find(p=>p.key==='2024|higher|LC001ALP200IV.pdf')!;
    expect(row.fullVisualReview).toBe('complete');
    expect(row.bankAtlasTaskParity).toBe('complete');
    expect(inventory.summary.papersPendingFullReview).toBe(68);
  });
});
