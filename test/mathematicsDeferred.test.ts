import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/maths/ordinary';
import { browseTopicIdsForQuestion, questionsForTopics, topicsForPaper } from '../components/PaperTrail/topics';
import { examTopicIdsForQuestion } from '../data/examTopics/registry';
import { isAnswerMap, preferredAnswersUrl } from '../components/PaperTrail/vaultResolve';
import { paperRegionFor, schemeRegionFor } from '../components/PaperTrail/paperRegion';
import type { PaperAnswerMap } from '../types/paperTrail';
import review from '../scripts/markbank/mathematics/reviews/2025-ordinary-p1-deferred.json';

const prefix = 'maths-2025-ol-p1-deferred-q';
const cards = CARDS.filter(c => c.id.startsWith(prefix));

describe('2025 Ordinary deferred Paper 1', () => {
  it('retains every reviewed scale and every printed question, including unattempted exam choices', () => {
    expect(cards).toHaveLength(41);
    expect(cards.map(c => c.id).sort()).toEqual(review.cards.map(c => c.id).sort());
    expect(cards.reduce((total,c) => total+c.totalMarks,0)).toBe(380);
    for (const [q,marks] of Object.entries(review.printedQuestionMarks)) {
      expect(cards.filter(c => c.questionRef.match(/Q(\d+)/)?.[1] === q)
        .reduce((total,c) => total+c.totalMarks,0),q).toBe(marks);
    }
    const grouped = cards.find(c => c.id === prefix+'9-b-i-ii')!;
    expect(grouped.totalMarks).toBe(10);
    expect(grouped.questionText).toContain('366·43');
    expect(grouped.questionText).toContain('5·31');
    expect(grouped.stem).toContain('2000 m');
    expect(cards.some(c => c.id === prefix+'9-b-ii')).toBe(false);
  });

  it('uses the task-specific credit award when the general table disagrees', () => {
    const c = cards.find(c => c.id === prefix+'1-c')!;
    expect(c.mathematicsScale).toMatchObject({code:'10D',marks:[0,3,5,7,10]});
    expect(c.mathematicsScale?.markingNote).toContain('differs from the general');
    expect(cards.find(c => c.id === prefix+'2-c')!.mathematicsScale)
      .toMatchObject({code:'10D',marks:[0,3,5,8,10]});
  });

  it('binds distinct deferred sources and inspected typeset images, keeping answers behind the reveal', () => {
    for (const c of cards) {
      expect(c.paperFileid,c.id).toBe('LC003GLP100EV-deferred');
      expect(c.mathematicsScale?.schemeFileid,c.id).toBe(review.schemeFileid);
      expect(c.sourceMaterial?.sourceFileid,c.id).toBe(review.paperFileid);
      expect(c.questionFigure?.solution,c.id).not.toBe(true);
      expect('figure' in c && c.figure?.solution,c.id).toBe(true);
      const figures=[c.questionFigure,'figure' in c ? c.figure : undefined];
      for(const f of figures) {
        expect(f,c.id).toBeTruthy();
        expect(createHash('md5').update(readFileSync('public'+f!.src)).digest('hex'),c.id).toBe(f!.srcHash);
      }
    }
  });

  it('exposes every card in the actual Topic Atlas feed under its reviewed topics', () => {
    const paper=topicsForPaper('mathematics',2025,'ordinary','ev',review.paperFileid);
    expect(paper).toBeDefined();
    const feeds=new Map<string,ReturnType<typeof questionsForTopics>>();
    for (const task of review.cards) {
      const n=task.printedParts[0].match(/^Q(\d+)/)![1];
      const q=paper!.q.find(q => q.n === n);
      expect(q,task.id).toBeDefined();
      expect(browseTopicIdsForQuestion(paper!,q!),task.id).toEqual(expect.arrayContaining(task.examTopicIds));
      expect(examTopicIdsForQuestion('mathematics','ordinary',2025,'deferred',n,'p1','ev',review.paperFileid),task.id)
        .toEqual(expect.arrayContaining(task.examTopicIds));
      for (const topic of task.examTopicIds) {
        if(!feeds.has(topic)) feeds.set(topic,questionsForTopics('mathematics',[topic]));
        expect(feeds.get(topic),task.id).toContainEqual({subjectId:'mathematics',year:2025,level:'ordinary',lang:'ev',paperKey:'p1',fileid:review.paperFileid,n});
      }
    }
  });

  it('keeps June and deferred questions separate in the topic feed', () => {
    const all=questionsForTopics('mathematics',null).filter(q=>q.year===2025&&q.level==='ordinary'&&q.paperKey==='p1'&&q.n==='1');
    expect(new Set(all.map(q=>q.fileid))).toEqual(new Set(['LC003GLP100EV.pdf','LC003GLP100EV-deferred.pdf']));
  });

  it('ships usable deferred question and solution anchors without depending on a Storage upload', () => {
    const url=preferredAnswersUrl('mathematics',2025,review.paperFileid,'https://storage/map.json');
    expect(url).toBe(`/paper-answers/2025/${review.paperFileid}.json`);
    const hosted=readFileSync('public'+url,'utf8');
    expect(hosted).toBe(readFileSync(`scripts/paper-trail/answers/2025/${review.paperFileid}.json`,'utf8'));
    const map: PaperAnswerMap=JSON.parse(hosted);
    expect(isAnswerMap(map)).toBe(true);
    expect(map.schemeFileid).toBe(review.schemeFileid);
    expect(map.q.map(q=>q.n)).toEqual(Object.keys(review.printedQuestionMarks));
    for(const task of review.cards) {
      const n=task.printedParts[0].match(/^Q(\d+)/)![1];
      const q=map.q.find(q=>q.n===n)!;
      expect(paperRegionFor(map.q,n)?.map(r=>r.p),task.id).toEqual(expect.arrayContaining(task.sourcePages));
      expect(schemeRegionFor(q).map(r=>r.p),task.id).toEqual(expect.arrayContaining(task.schemePages));
    }
  });
});
