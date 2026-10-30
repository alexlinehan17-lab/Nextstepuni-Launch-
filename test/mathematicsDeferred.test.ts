import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/maths/ordinary';
import { CARDS as HIGHER_CARDS } from '../components/MarkBank/cards/maths/higher';
import { browseTopicIdsForQuestion, questionsForTopics, topicsForPaper } from '../components/PaperTrail/topics';
import { examTopicIdsForQuestion } from '../data/examTopics/registry';
import { isAnswerMap, preferredAnswersUrl } from '../components/PaperTrail/vaultResolve';
import { paperRegionFor, schemeRegionFor } from '../components/PaperTrail/paperRegion';
import type { PaperAnswerMap } from '../types/paperTrail';
import review from '../scripts/markbank/mathematics/reviews/2025-ordinary-p1-deferred.json';
import reviewP2 from '../scripts/markbank/mathematics/reviews/2025-ordinary-p2-deferred.json';
import reviewHL1 from '../scripts/markbank/mathematics/reviews/2025-higher-p1-deferred.json';
import reviewHL2 from '../scripts/markbank/mathematics/reviews/2025-higher-p2-deferred.json';

const prefix = 'maths-2025-ol-p1-deferred-q';
const cards = CARDS.filter(c => c.id.startsWith(prefix));

describe('2025 Higher deferred Paper 2', () => {
  const prefix='maths-2025-hl-p2-deferred-q';
  const cards=HIGHER_CARDS.filter(c=>c.id.startsWith(prefix));
  it('retains all printed tasks at their own allocations, keeping shared marks together', () => {
    expect(cards).toHaveLength(43);
    expect(cards.map(c=>c.id).sort()).toEqual(reviewHL2.cards.map(c=>c.id).sort());
    expect(cards.reduce((s,c)=>s+c.totalMarks,0)).toBe(380);
    for(const [n,marks] of Object.entries(reviewHL2.printedQuestionMarks))
      expect(cards.filter(c=>c.questionRef.match(/Q(\d+)/)?.[1]===n).reduce((s,c)=>s+c.totalMarks,0),n).toBe(marks);
    for(const [id,marks] of [['2-a-i-ii',15],['3-a-i-ii',10],['3-b-i-ii',10],['4-a-b',10],['9-b-i-ii',10]] as const)
      expect(cards.find(c=>c.id===prefix+id)?.totalMarks,id).toBe(marks);
    expect(cards.some(c=>c.id===prefix+'4-b')).toBe(false);
    expect(cards.find(c=>c.id===prefix+'7-a')?.questionText).toContain('construction lines');
    expect(cards.find(c=>c.id===prefix+'10-c-iii')?.questionText).toContain('different committee');
  });

  it('uses Paper 2 awards and flags source errors without inventing official guidance', () => {
    expect(cards.find(c=>c.id===prefix+'1-a-i')?.mathematicsScale).toMatchObject({code:'10C',marks:[0,4,7,10]});
    expect(cards.find(c=>c.id===prefix+'2-a-i-ii')?.mathematicsScale).toMatchObject({code:'15D',marks:[0,4,7,11,15]});
    expect(cards.find(c=>c.id===prefix+'9-c-ii')?.mathematicsScale).toMatchObject({code:'5D',marks:[0,2,3,4,5]});
    for(const [id,note] of [['4-a-b','√3/2 − (−1/2)'],['10-a-i','74·75%'],['10-a-ii','P(Z ≤ z) = 0·5918']]) {
      const c=cards.find(c=>c.id===prefix+id)!;
      expect('figure' in c && c.figure?.sourceNote).toContain(note);
    }
    expect(cards.find(c=>c.id===prefix+'10-a-i')?.mathematicsScale?.markingNote).toContain('no substitute official criterion');
  });

  it('exposes every card through the exact deferred Atlas feed with complete source regions and verified images', () => {
    const paper=topicsForPaper('mathematics',2025,'higher','ev',reviewHL2.paperFileid)!;
    expect(paper).toBeDefined();
    const url=preferredAnswersUrl('mathematics',2025,reviewHL2.paperFileid,'https://storage/map.json');
    expect(url).toBe(`/paper-answers/2025/${reviewHL2.paperFileid}.json`);
    const hosted=readFileSync('public'+url,'utf8');
    expect(hosted).toBe(readFileSync(`scripts/paper-trail/answers/2025/${reviewHL2.paperFileid}.json`,'utf8'));
    const map:PaperAnswerMap=JSON.parse(hosted);
    expect(isAnswerMap(map)).toBe(true);
    expect(map.schemeFileid).toBe(reviewHL2.schemeFileid);
    const feeds=new Map<string,ReturnType<typeof questionsForTopics>>();
    for(const task of reviewHL2.cards) {
      const c=cards.find(c=>c.id===task.id)!;
      expect(c.paperFileid).toBe('LC003ALP200EV-deferred');
      expect(c.questionFigure?.solution).not.toBe(true);
      expect('figure' in c && c.figure?.solution).toBe(true);
      for(const f of [c.questionFigure,'figure' in c?c.figure:undefined]) {
        expect(f,task.id).toBeDefined();
        expect(createHash('md5').update(readFileSync('public'+f!.src)).digest('hex'),task.id).toBe(f!.srcHash);
      }
      const n=task.printedParts[0].match(/^Q(\d+)/)![1];
      const q=paper.q.find(q=>q.n===n)!;
      expect(browseTopicIdsForQuestion(paper,q),task.id).toEqual(expect.arrayContaining(task.examTopicIds));
      expect(paperRegionFor(map.q,n)?.map(r=>r.p),task.id).toEqual(expect.arrayContaining(task.sourcePages));
      expect(schemeRegionFor(map.q.find(q=>q.n===n)!).map(r=>r.p),task.id).toEqual(expect.arrayContaining(task.schemePages));
      for(const topic of task.examTopicIds) {
        if(!feeds.has(topic))feeds.set(topic,questionsForTopics('mathematics',[topic]));
        expect(feeds.get(topic),task.id).toContainEqual({subjectId:'mathematics',year:2025,level:'higher',lang:'ev',paperKey:'p2',fileid:reviewHL2.paperFileid,n});
      }
    }
  });
});

describe('2025 Higher deferred Paper 1', () => {
  const prefix='maths-2025-hl-p1-deferred-q';
  const cards=HIGHER_CARDS.filter(c=>c.id.startsWith(prefix));
  it('retains every printed part at its published allocation, including grouped parts and choices', () => {
    expect(cards).toHaveLength(40);
    expect(cards.map(c=>c.id).sort()).toEqual(reviewHL1.cards.map(c=>c.id).sort());
    expect(cards.reduce((s,c)=>s+c.totalMarks,0)).toBe(380);
    for(const [n,marks] of Object.entries(reviewHL1.printedQuestionMarks))
      expect(cards.filter(c=>c.questionRef.match(/Q(\d+)/)?.[1]===n).reduce((s,c)=>s+c.totalMarks,0),n).toBe(marks);
    expect(cards.find(c=>c.id===prefix+'6-c-i-ii')?.totalMarks).toBe(10);
    expect(cards.find(c=>c.id===prefix+'7-a-b')?.totalMarks).toBe(10);
    expect(cards.some(c=>c.id===prefix+'7-b')).toBe(false);
    for(const id of ['4-b','7-d']) {
      const pool=cards.filter(c=>c.id.startsWith(prefix+id));
      expect(pool).toHaveLength(1);
      expect(pool[0].questionText).toContain('Tick one box only');
      expect(pool[0].questionText).toContain('Justify your answer');
    }
  });

  it('retains the printed numeric bands and explains inconsistent source notation', () => {
    expect(cards.find(c=>c.id===prefix+'2-b-i')?.mathematicsScale)
      .toMatchObject({code:'5D',marks:[0,2,3,4,5]});
    expect(cards.find(c=>c.id===prefix+'10-a-iv')?.mathematicsScale)
      .toMatchObject({code:'10B',marks:[0,5,10]});
    const average=cards.find(c=>c.id===prefix+'10-a-iii')!;
    expect(average.mathematicsScale).toMatchObject({code:'10C',marks:[0,4,6,10]});
    expect(average.mathematicsScale?.markingNote).toContain('without assigning a separate mark');
    const graph=cards.find(c=>c.id===prefix+'10-a-i')!;
    expect('figure' in graph && graph.figure?.attribution).toContain('Worked example: NextStepUni');
    expect('figure' in graph && graph.figure?.alt).toContain('0 to 32 seconds');
    expect('figure' in graph && graph.figure?.sourceNote).toContain('clipped at its right edge');
    for(const [id,note] of [['7-a-b','two decimal places'],['9-b-ii','−1·35'],['4-b','local maximum']]) {
      const c=cards.find(c=>c.id===prefix+id)!;
      expect('figure' in c && c.figure?.sourceNote).toContain(note);
    }
  });

  it('exposes every card in Atlas with the exact deferred booklet, full images and hosted answer regions', () => {
    const paper=topicsForPaper('mathematics',2025,'higher','ev',reviewHL1.paperFileid)!;
    expect(paper).toBeDefined();
    const url=preferredAnswersUrl('mathematics',2025,reviewHL1.paperFileid,'https://storage/map.json');
    expect(url).toBe(`/paper-answers/2025/${reviewHL1.paperFileid}.json`);
    const hosted=readFileSync('public'+url,'utf8');
    expect(hosted).toBe(readFileSync(`scripts/paper-trail/answers/2025/${reviewHL1.paperFileid}.json`,'utf8'));
    const map:PaperAnswerMap=JSON.parse(hosted);
    expect(isAnswerMap(map)).toBe(true);
    expect(map.schemeFileid).toBe(reviewHL1.schemeFileid);
    const feeds=new Map<string,ReturnType<typeof questionsForTopics>>();
    for(const task of reviewHL1.cards) {
      const c=cards.find(c=>c.id===task.id)!;
      expect(c.paperFileid).toBe('LC003ALP100EV-deferred');
      expect(c.questionFigure?.solution).not.toBe(true);
      expect('figure' in c && c.figure?.solution).toBe(true);
      for(const f of [c.questionFigure,'figure' in c?c.figure:undefined]) {
        expect(f,task.id).toBeDefined();
        expect(createHash('md5').update(readFileSync('public'+f!.src)).digest('hex'),task.id).toBe(f!.srcHash);
      }
      const n=task.printedParts[0].match(/^Q(\d+)/)![1];
      const q=paper.q.find(q=>q.n===n)!;
      expect(browseTopicIdsForQuestion(paper,q),task.id).toEqual(expect.arrayContaining(task.examTopicIds));
      expect(paperRegionFor(map.q,n)?.map(r=>r.p),task.id).toEqual(expect.arrayContaining(task.sourcePages));
      expect(schemeRegionFor(map.q.find(q=>q.n===n)!).map(r=>r.p),task.id).toEqual(expect.arrayContaining(task.schemePages));
      for(const topic of task.examTopicIds) {
        if(!feeds.has(topic))feeds.set(topic,questionsForTopics('mathematics',[topic]));
        expect(feeds.get(topic),task.id).toContainEqual({subjectId:'mathematics',year:2025,level:'higher',lang:'ev',paperKey:'p1',fileid:reviewHL1.paperFileid,n});
      }
    }
  });
});

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

describe('2025 Ordinary deferred Paper 2', () => {
  const prefix='maths-2025-ol-p2-deferred-q';
  const cards=CARDS.filter(c=>c.id.startsWith(prefix));
  it('retains all 45 reviewed tasks, shared allocations, printed choices and 380 offered marks', () => {
    expect(cards.map(c=>c.id).sort()).toEqual(reviewP2.cards.map(c=>c.id).sort());
    expect(cards).toHaveLength(45);
    expect(cards.reduce((sum,c)=>sum+c.totalMarks,0)).toBe(380);
    for(const [n,marks] of Object.entries(reviewP2.printedQuestionMarks))
      expect(cards.filter(c=>c.questionRef.match(/Q(\d+)/)?.[1]===n).reduce((s,c)=>s+c.totalMarks,0),n).toBe(marks);
    expect(cards.find(c=>c.id===prefix+'4-a-i-ii-iii')?.totalMarks).toBe(15);
    expect(cards.find(c=>c.id===prefix+'5-a-i-ii')?.totalMarks).toBe(10);
    expect(cards.find(c=>c.id===prefix+'10-a-ii-iii')?.totalMarks).toBe(10);
    const choice=cards.filter(c=>c.id.startsWith(prefix+'3-d'));
    expect(choice).toHaveLength(1);
    for(const option of ['Option 1','Option 2','Option 3']) expect(choice[0].questionText).toContain(option);
  });

  it('keeps task-specific marks and makes omissions or contradictions in the scheme explicit', () => {
    for(const id of ['7-a-ii','7-b-i']) {
      const c=cards.find(c=>c.id===prefix+id)!;
      expect(c.mathematicsScale).toMatchObject({code:'10C',marks:[0,3,7,10]});
      expect(c.mathematicsScale?.markingNote).toContain('general Paper 2');
    }
    const tree=cards.find(c=>c.id===prefix+'10-b-i')!;
    expect('figure' in tree && tree.figure?.attribution).toContain('Worked example: NextStepUni');
    expect('figure' in tree && tree.figure?.alt).toContain('0.1625');
    expect('figure' in tree && tree.figure?.sourceNote).toContain('model tree blank');
    const rain=cards.find(c=>c.id===prefix+'10-b-iii')!;
    expect('figure' in rain && rain.figure?.sourceNote).toContain('0·0469');
    expect('figure' in rain && rain.figure?.sourceNote).toContain('0·0129');
    // Independent reference arithmetic: the paper conditions on rain already.
    expect((1/4)*(1/4)*(3/4)).toBe(3/64);
    expect((3/64).toFixed(4)).toBe('0.0469');
  });

  it('pairs every card with its inspected source images and a working Atlas question/answer link', () => {
    const paper=topicsForPaper('mathematics',2025,'ordinary','ev',reviewP2.paperFileid)!;
    expect(paper).toBeDefined();
    const url=preferredAnswersUrl('mathematics',2025,reviewP2.paperFileid,'https://storage/map.json');
    expect(url).toBe(`/paper-answers/2025/${reviewP2.paperFileid}.json`);
    const content=readFileSync('public'+url,'utf8');
    expect(content).toBe(readFileSync(`scripts/paper-trail/answers/2025/${reviewP2.paperFileid}.json`,'utf8'));
    const map: PaperAnswerMap=JSON.parse(content);
    expect(isAnswerMap(map)).toBe(true);
    expect(map.schemeFileid).toBe(reviewP2.schemeFileid);
    const feeds=new Map<string,ReturnType<typeof questionsForTopics>>();
    for(const task of reviewP2.cards) {
      const c=cards.find(c=>c.id===task.id)!;
      expect(c.paperFileid).toBe('LC003GLP200EV-deferred');
      expect(c.questionFigure?.solution).not.toBe(true);
      expect('figure' in c && c.figure?.solution).toBe(true);
      for(const f of [c.questionFigure,'figure' in c?c.figure:undefined]) {
        expect(f,task.id).toBeDefined();
        expect(createHash('md5').update(readFileSync('public'+f!.src)).digest('hex'),task.id).toBe(f!.srcHash);
      }
      const n=task.printedParts[0].match(/^Q(\d+)/)![1];
      const q=paper.q.find(q=>q.n===n)!;
      expect(browseTopicIdsForQuestion(paper,q),task.id).toEqual(expect.arrayContaining(task.examTopicIds));
      expect(paperRegionFor(map.q,n)?.map(r=>r.p),task.id).toEqual(expect.arrayContaining(task.sourcePages));
      expect(schemeRegionFor(map.q.find(q=>q.n===n)!).map(r=>r.p),task.id).toEqual(expect.arrayContaining(task.schemePages));
      for(const topic of task.examTopicIds) {
        if(!feeds.has(topic))feeds.set(topic,questionsForTopics('mathematics',[topic]));
        expect(feeds.get(topic),task.id).toContainEqual({subjectId:'mathematics',year:2025,level:'ordinary',lang:'ev',paperKey:'p2',fileid:reviewP2.paperFileid,n});
      }
    }
  });
});
