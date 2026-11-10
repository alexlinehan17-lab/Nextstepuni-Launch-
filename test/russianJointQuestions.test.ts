import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { reviewedRussianJointTask, verifyRussianJointAnchors } from '../scripts/markbank/russianJointTasks.mjs';
const read = (path: string) => JSON.parse(readFileSync(path,'utf8'));
const cards = read('components/MarkBank/cards/russian/reviewed.json');
const sources = read('scripts/markbank/authoring/russian-reviewed-sources.json');
const card = cards.find((c: {id:string}) => c.id === 'ru-2011-hl-c2');
const source = sources.find((c: {id:string}) => c.id === card?.id);
const map = read('scripts/paper-trail/answers/2011/LC099ALP000EV.pdf.json');

describe('reviewed Russian shared-question coverage and Atlas identities', () => {
  it('resolves each original summary question to one joint card with complete source context', () => {
    const questions = reviewedRussianJointTask(source,card);
    expect(questions.map((q: {n:string}) => q.n)).toEqual(['c2-1','c2-2','c2-3','c2-4']);
    expect(() => verifyRussianJointAnchors(source,card,map)).not.toThrow();
    const anchors = map.q.filter((q: {markBankCardId?:string}) => q.markBankCardId === card.id);
    expect(anchors).toHaveLength(4);
    expect(anchors.map((q: {pP:number}) => q.pP)).toEqual([6,7,8,9]);
    const tags = read('scripts/paper-trail/topic-tags/tags/russian.json').find((p: {year:number;fileid:string;level:string}) => p.year === 2011 && p.level === 'higher' && p.fileid === 'LC099ALP000EV.pdf');
    for (const question of questions) expect(tags.q.filter((q: {n:string}) => q.n === question.n)).toHaveLength(1);
    for (const directory of ['paper-answers','paper-anchors']) expect(read(`public/${directory}/2011/LC099ALP000EV.pdf.json`)).toEqual(map);
  });
  it.each(['coveredQuestionRefs','atlasQuestions','questionPages','paperPages','schemePages'])('rejects omitted source evidence: %s', key => {
    const changed = structuredClone(source); delete changed[key];
    expect(() => reviewedRussianJointTask(changed,card)).toThrow();
  });
  it('rejects unknown, duplicate, mismatched and incomplete original questions', () => {
    for (const change of [
      (s: typeof source) => {s.coveredQuestionRefs[1] = s.coveredQuestionRefs[0];},
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
    expect(() => reviewedRussianJointTask(source,{...card,questionText:card.questionText.split('Section 4')[0]})).toThrow();
  });
  it('rejects missing or duplicate anchors, wrong card targets and lost passage pages', () => {
    for (const change of [
      (m: typeof map) => {m.q = m.q.filter((q:{n:string}) => q.n !== 'c2-4');},
      (m: typeof map) => {m.q.push(structuredClone(m.q.find((q:{n:string}) => q.n === 'c2-1')));},
      (m: typeof map) => {m.q.find((q:{n:string}) => q.n === 'c2-2').markBankCardId = 'ru-2011-hl-c1-1-i';},
      (m: typeof map) => {m.q.find((q:{n:string}) => q.n === 'c2-3').paperRegion.pop();},
      (m: typeof map) => {m.q.find((q:{n:string}) => q.n === 'c2-4').region[0].p = 10;},
    ]) {
      const changed = structuredClone(map); change(changed);
      expect(() => verifyRussianJointAnchors(source,card,changed)).toThrow();
    }
  });
  it('preserves every original 2011 reading anchor identity and coordinate', () => {
    const originals = read('test/fixtures/russian2011OriginalAnchors.json');
    expect(originals).toHaveLength(8);
    for (const old of originals) expect(map.q.find((q: {n:string}) => q.n === old.n)).toEqual(old);
  });
  it('leaves ordinary source records without joint metadata on their existing path', () => {
    const original = sources.find((s: {id:string}) => s.id === 'ru-2012-hl-gr');
    expect(reviewedRussianJointTask(original,cards.find((c: {id:string}) => c.id === original.id))).toBeNull();
  });
});
