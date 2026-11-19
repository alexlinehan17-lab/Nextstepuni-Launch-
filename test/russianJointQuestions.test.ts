import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { reviewedRussianJointTask, verifyRussianJointAnchors } from '../scripts/markbank/russianJointTasks.mjs';
const read = (path: string) => JSON.parse(readFileSync(path,'utf8'));
const cards = read('components/MarkBank/cards/russian/reviewed.json');
const sources = read('scripts/markbank/authoring/russian-reviewed-sources.json');
const card = cards.find((c: {id:string}) => c.id === 'ru-2011-hl-c2');
const source = sources.find((c: {id:string}) => c.id === card?.id);
const map = read('scripts/paper-trail/answers/2011/LC099ALP000EV.pdf.json');

describe('reviewed Russian summary split and preserved Atlas identities', () => {
  it('keeps the old card identity bound only to the first original question', () => {
    const questions = reviewedRussianJointTask(source,card);
    expect(questions.map((q: {n:string}) => q.n)).toEqual(['c2-1']);
    expect(() => verifyRussianJointAnchors(source,card,map)).not.toThrow();
    const anchors = map.q.filter((q: {markBankCardId?:string}) => q.markBankCardId === card.id);
    expect(anchors).toHaveLength(1);
    expect(anchors[0].pP).toBe(6);
    expect(source.coveredQuestionRefs).toEqual(['2011 HL Section C2 Q1']);
  });
  it('resolves all four original asks separately without duplicating an Atlas row or card', () => {
    const tags = read('scripts/paper-trail/topic-tags/tags/russian.json').find((p: {year:number;fileid:string;level:string}) => p.year === 2011 && p.level === 'higher' && p.fileid === 'LC099ALP000EV.pdf');
    const targets = new Set();
    for (const section of [1,2,3,4]) {
      const id = section === 1 ? 'ru-2011-hl-c2' : `ru-2011-hl-c2-${section}`;
      const matches = map.q.filter((q: {n:string}) => q.n === `c2-${section}`);
      expect(matches).toHaveLength(1);
      const anchor = matches[0];
      expect(anchor.markBankCardId).toBe(section === 1 ? id : undefined);
      expect(anchor.paperRegion.map((p: {p:number})=>p.p)).toEqual([section+5]);
      const task = sources.find((s: {id:string})=>s.id===id);
      const own = cards.find((c: {id:string})=>c.id===id);
      expect(own.questionRef).toBe(`2011 HL Section C2 Q${section}`);
      expect(task.questionPages).toEqual([section+5]);
      expect(tags.q.find((q: {n:string})=>q.n===`c2-${section}`).primary).toBe(own.topicId);
      if (section > 1) expect(reviewedRussianJointTask(task,own)).toBeNull();
      targets.add(id);
    }
    expect(targets.size).toBe(4);
    expect(map.q.filter((q: {n:string})=>q.n==='c2')).toHaveLength(0);
    for (const directory of ['paper-answers','paper-anchors']) expect(read(`public/${directory}/2011/LC099ALP000EV.pdf.json`)).toEqual(map);
  });
  it.each(['coveredQuestionRefs','atlasQuestions','questionPages','paperPages','schemePages'])('rejects omitted identity evidence: %s', key => {
    const changed = structuredClone(source); delete changed[key];
    expect(() => reviewedRussianJointTask(changed,card)).toThrow();
  });
  it('rejects unknown, duplicate, mismatched and incomplete first-question bindings', () => {
    for (const change of [
      (s: typeof source) => {s.coveredQuestionRefs.push(s.coveredQuestionRefs[0]);},
      (s: typeof source) => {s.coveredQuestionRefs[0] = '2011 HL Section C2 Q5';},
      (s: typeof source) => {s.year = 2012;},
      (s: typeof source) => {s.level = 'ordinary';},
      (s: typeof source) => {s.atlasQuestions[0].n = 'c2-new';},
      (s: typeof source) => {s.atlasQuestions[0].questionText = '';},
      (s: typeof source) => {s.atlasQuestions[0].questionPages = [7];},
      (s: typeof source) => {s.atlasQuestions[0].schemePages = [10];},
      (s: typeof source) => {s.atlasQuestions.pop();},
    ]) {
      const changed = structuredClone(source); change(changed);
      expect(() => reviewedRussianJointTask(changed,card)).toThrow();
    }
    expect(() => reviewedRussianJointTask({...source,id:'ru-2011-hl-invented'},card)).toThrow();
    expect(() => reviewedRussianJointTask(source,{...card,section:'C1'})).toThrow();
    expect(() => reviewedRussianJointTask(source,{...card,questionText:''})).toThrow();
  });
  it('rejects lost or duplicate first anchors, wrong targets and lost passage pages', () => {
    for (const change of [
      (m: typeof map) => {m.q = m.q.filter((q:{n:string}) => q.n !== 'c2-1');},
      (m: typeof map) => {m.q.push(structuredClone(m.q.find((q:{n:string}) => q.n === 'c2-1')));},
      (m: typeof map) => {m.q.find((q:{n:string}) => q.n === 'c2-1').markBankCardId = 'ru-2011-hl-c1-1-i';},
      (m: typeof map) => {m.q.find((q:{n:string}) => q.n === 'c2-1').paperRegion.pop();},
      (m: typeof map) => {m.q.find((q:{n:string}) => q.n === 'c2-1').region[0].p = 10;},
    ]) {
      const changed = structuredClone(map); change(changed);
      expect(() => verifyRussianJointAnchors(source,card,changed)).toThrow();
    }
  });
  it('preserves every original reading anchor identity and coordinate', () => {
    const originals = read('test/fixtures/russian2011OriginalAnchors.json');
    expect(originals).toHaveLength(8);
    for (const old of originals) expect(map.q.find((q: {n:string}) => q.n === old.n)).toEqual(old);
  });
});
