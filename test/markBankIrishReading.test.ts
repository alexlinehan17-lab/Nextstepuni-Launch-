import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/irish/higher';
import authored from '../components/MarkBank/cards/irish/authored.json';
import review from '../scripts/markbank/authored/irish-reading-review.json';
import { cardsForTopic } from '../components/MarkBank/deck';
import { irishMarks, irishScoreId } from '../components/MarkBank/SessionScreen';
import { curriculumNodeIdsForExamTopic, examTopicIdsForQuestion } from '../data/examTopics/registry';
import { paperRegionFor, schemeRegionFor } from '../components/PaperTrail/paperRegion';
import { tariffReconciles, type IrishRubric } from '../types/markBank';

const byId = new Map(CARDS.map(c => [c.id,c]));
const cardFor = (suffix: string) => byId.get('irish-2024-hl-p2-reading-'+suffix)!;
const rubric = (suffix: string): IrishRubric => {
  const r=cardFor(suffix).rubric;
  if(r.system!=='irish') throw new Error('Wrong rubric');
  return r;
};

describe('2024 Higher Irish reading: independently reviewed paper/scheme boundaries', () => {
  it('reconciles all published parts without counting overlapping whole questions twice', () => {
    const atomic: Array<[string,number]> = [];
    for (const passage of ['a','b']) {
      for (const n of [1,2,3,4,5]) {
        for (const [part,marks] of [['a',3],['bi',2],['bii',2]] as const) {
          const key=`${passage}-q${n}-${part}`;
          if (passage==='b' && ['1-bi','4-bi','4-bii','5-bii'].includes(`${n}-${part}`)) {
            atomic.push([key+'-1',1],[key+'-2',1]);
            expect(cardFor(key).totalMarks).toBe(2);
          } else atomic.push([key,marks]);
        }
      }
      atomic.push([`${passage}-q6-a`,3]);
      if (passage==='a') atomic.push(['a-q6-b',12]);
      else atomic.push(['b-q6-b-1',6],['b-q6-b-2',6]);
    }
    expect(atomic).toHaveLength(39);
    expect(review.atomicCardIds.slice().sort()).toEqual(atomic.map(([id]) => 'irish-2024-hl-p2-reading-'+id).sort());
    for(const [suffix,marks] of atomic) {
      expect(cardFor(suffix).totalMarks,suffix).toBe(marks);
      expect(tariffReconciles(cardFor(suffix)),suffix).toBe(true);
    }
    for(const passage of ['a','b']) {
      expect(atomic.filter(([id]) => id.startsWith(passage)).reduce((sum,[,marks]) => sum+marks,0)).toBe(50);
      const parents=[1,2,3,4,5,6].map(n => cardFor(`${passage}-q${n}`));
      expect(parents.map(c => c.totalMarks)).toEqual([7,7,7,7,7,15]);
      for(const n of [1,2,3,4,5]) expect(rubric(`${passage}-q${n}`).criteria.map(c => c.maxMarks)).toEqual([3,2,2]);
    }
    expect(review.addedCardIds).toHaveLength(44);
    expect(new Set(review.cardIds).size).toBe(56);
    expect(cardFor('b-q6-b').totalMarks).toBe(12);
    expect(review.scope).toContain('full-paper status is recorded separately');
  });

  it('keeps grammar as a paired 0/2/3 task under the canonical grammar topic', () => {
    for(const passage of ['a','b']) {
      const card=cardFor(`${passage}-q6-a`);
      expect(card.topicId).toBe('irish-3-3');
      expect(rubric(`${passage}-q6-a`).criteria).toHaveLength(1);
      const criterion=rubric(`${passage}-q6-a`).criteria[0];
      expect(criterion.permittedMarks).toEqual([0,2,3]);
      expect(criterion.guidance.join(' ')).toContain('ceart agus marc amháin ar an gceann eile');
      for(const marks of [0,2,3]) expect(irishMarks(card,{[irishScoreId(criterion.id)]:marks})).toBe(marks);
      expect(cardsForTopic('irish-3-3',CARDS)).toContain(cardFor(`${passage}-q6`));
      expect(cardsForTopic('irish-3-3',CARDS)).not.toContain(cardFor(`${passage}-q6-b`));
    }
    expect(cardFor('a-q6-a').questionText).toContain('Aimsir Fháistineach');
    expect(cardFor('a-q6-a').questionText).toContain('bhreischéim na haidiachta');
    expect(cardFor('b-q6-a').questionText).toContain('Mhodh Coinníollach');
    expect(cardFor('b-q6-a').questionText).toContain('Aimsir Láithreach');
    expect(rubric('a-q6').criteria.map(c => c.maxMarks)).toEqual([3,12]);
    expect(rubric('b-q6').criteria.map(c => c.maxMarks)).toEqual([3,6,6]);
  });

  it('retains shared opinion conditions and the independently marked insight conditions', () => {
    const opinion=rubric('a-q6-b');
    expect(opinion.criteria).toHaveLength(1);
    const guide=opinion.criteria[0].guidance.join(' ');
    expect(guide).toContain('Tuairim (T) = 2 mharc');
    expect(guide).toContain('5 mharc + 5 mharc');
    expect(guide).toContain('Gan tuairim luaite, ní féidir glacadh leis an bpointe eolais/na pointí eolais');
    expect(guide).not.toContain('LÉAMHTHUISCINT B');
    for(const suffix of ['b-q6-b-1','b-q6-b-2']) {
      expect(cardFor(suffix).questionText).toContain('Is leor 60 focal');
      expect(cardFor(suffix).questionText).not.toContain('30 focal');
      expect(cardFor(suffix).questionText).toContain('mínigh léargas amháin');
      const r=rubric(suffix);
      expect(r.criteria).toHaveLength(1);
      expect(r.criteria[0].maxMarks).toBe(6);
      expect(r.criteria[0].guidance.join(' ')).toContain('Gan léargas luaite/intuigthe, ní féidir glacadh leis an sampla');
      expect(cardFor(suffix).questionText).not.toContain('Léargais fhéideartha');
    }
    for(const key of ['1-bi','4-bi','4-bii','5-bii']) {
      for(const slot of [1,2]) {
        const card=cardFor(`b-q${key}-${slot}`);
        expect(card.totalMarks).toBe(1);
        expect(card.questionText).toContain('tabhair freagra amháin');
        expect(rubric(`b-q${key}-${slot}`).criteria[0].permittedMarks).toEqual([0,1]);
      }
    }
    expect(cardFor('b-q1-bi-1').questionText).not.toContain('Alexa');
    expect(rubric('a-q5-a').criteria[0].guidance.join(' ')).toContain('seirbhísí iompair farraige agus an gealltanas eile bainteach le seirbhísí iompair aeir');
  });

  it('joins every new part and retained question to its full passage, scheme and correct Atlas topic', () => {
    const map=JSON.parse(readFileSync('public/paper-answers/2024/LC001ALP200IV.pdf.json','utf8'));
    const ids=new Set(review.cardIds);
    const rows=authored.cards.filter(c => ids.has(c.id));
    expect(rows).toHaveLength(56);
    for(const raw of rows) {
      if(!('atlasQuestionId' in raw) || !('schemePages' in raw)) throw new Error('Missing source metadata');
      const card=byId.get(raw.id)!;
      const pages=card.id.includes('-reading-a-') ? [4,5] : [6,7];
      expect(card.sourceMaterial?.pages,card.id).toEqual(pages);
      const q=map.q.find((q:{n:string}) => q.n===raw.atlasQuestionId);
      expect(q,card.id).toBeDefined();
      expect(q.paperRegion.map((r:{p:number}) => r.p),card.id).toEqual(pages);
      expect((q.schemeRegion ?? q.region).map((r:{p:number}) => r.p),card.id).toEqual(raw.schemePages);
      expect(paperRegionFor(map.q,q.n,10),card.id).not.toBeNull();
      expect(schemeRegionFor(q).length,card.id).toBeGreaterThan(0);
      const topics=examTopicIdsForQuestion('irish','higher',2024,'main',q.n,'p2','iv','LC001ALP200IV.pdf');
      expect(topics.flatMap(curriculumNodeIdsForExamTopic),card.id).toContain(card.topicId);
      if(card.topicId==='irish-3-3') expect(topics).toEqual(['irish-higher-grammar']);
    }
    const guide=(suffix:string) => rows.find(c => c.id.endsWith(suffix))!;
    expect(guide('a-q6-b')).toMatchObject({schemePages:[21,22]});
    expect(guide('b-q4-bi')).toMatchObject({schemePages:[23,24]});
    expect(guide('b-q6-b')).toMatchObject({schemePages:[24,25]});
  });
});
