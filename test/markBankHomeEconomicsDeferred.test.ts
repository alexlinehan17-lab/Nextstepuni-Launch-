import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/home-economics/higher';
import { tariffReconciles } from '../types/markBank';
import { reviewedHomeEconomicsSource, homeEconomicsSourceMap } from '../scripts/markbank/homeEconomicsSources.mjs';
import { resolveIndexedPaperFileid } from '../scripts/markbank/paperIndex.mjs';
import review from '../scripts/markbank/authoring/home-economics/2023-hl-deferred-review.json';
import review2022 from '../scripts/markbank/authoring/home-economics/2022-hl-deferred-review.json';
import anchors2022 from '../scripts/paper-trail/answers/2022/LC098ALP014EV-deferred.pdf.json';
import anchors from '../scripts/paper-trail/answers/2023/LC098ALP014EV-deferred.pdf.json';
import bcAnchors from '../scripts/paper-trail/answers/2023/LC098ALP039EV-deferred.pdf.json';
import runtime from '../data/examTopics/home-economics-s-and-s-question-runtime.json';
import crosswalk from '../data/examTopics/home-economics-s-and-s-curriculum-crosswalk.json';
import { preferredAnswersUrl } from '../components/PaperTrail/vaultResolve';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';

const cards = CARDS.filter(c => c.id.startsWith('he-2023-hl-deferred-sa-'));
const get = (suffix: string) => {
  const c = cards.find(c => c.id === `he-2023-hl-deferred-sa-${suffix}`);
  if (!c || c.kind !== 'question') throw new Error(suffix);
  return c;
};

describe('Home Economics 2022 deferred Section A', () => {
  const cards2022 = CARDS.filter(c => c.id.startsWith('he-2022-hl-deferred-sa-'));
  const card = (suffix: string) => {
    const c = cards2022.find(c => c.id === `he-2022-hl-deferred-sa-${suffix}`);
    if (!c || c.kind !== 'question') throw new Error(suffix);
    return c;
  };
  it('keeps five independently marked second prompts and all required table entries', () => {
    expect(cards2022).toHaveLength(19);
    expect(cards2022.reduce((n, c) => n + c.totalMarks, 0)).toBe(84);
    expect(cards2022.map(c => c.id).sort()).toEqual(review2022.tasks.map(t => t.id).sort());
    for (const [q, suffix, marks] of [[1, 'mycoprotein', [4, 2]], [3, 'factors', [4, 2]], [6, 'meal-factors', [4, 2]], [8, 'effects', [2, 4]], [10, 'components', [3, 3]]] as const) {
      expect([card(`q${q}`).totalMarks, card(`q${q}-${suffix}`).totalMarks]).toEqual(marks);
      expect(card(`q${q}`).questionRef).not.toBe(card(`q${q}-${suffix}`).questionRef);
    }
    expect(card('q4').rows.map(r => r.verbatim)).toEqual(['Anaemia', 'Rickets', 'Beriberi']);
    expect(card('q7').questionText).toContain('Classification → Example:');
    expect(card('q7').rows.map(r => r.verbatim)).toEqual(['Thick soups', 'Thin/Clear soups', 'Cold soups']);
    expect(card('q12').rows.map(r => r.marks)).toEqual([2, 4]);
    expect(card('q12').rows[1].parts?.map(p => p.permittedMarks)).toEqual([[0, 2], [0, 2]]);
  });
  it('retains source ladders and complete guidance with explicit factual clarifications', () => {
    expect(card('q1').rows[0].parts?.map(p => p.permittedMarks)).toEqual([[0, 2], [0, 2]]);
    expect(card('q1-mycoprotein').rows[0].permittedMarks).toEqual([0, 1, 2]);
    expect(card('q3').rows[0].permittedMarks).toEqual([0, 1, 2, 3, 4]);
    expect(card('q3-factors').rows[0].contextNote).toContain('pregnancy/lactation');
    expect(card('q5').rows[0].contextNote).toContain('not another name for ferrous/ferric');
    expect(card('q6').rows[0].contextNote).toContain('impaired insulin action');
    expect(card('q6-meal-factors').questionText).toContain('planning meals for a person');
    expect(card('q8-effects').rows[0].contextNote).toContain('rancidity');
    expect(card('q10-components').rows[0].parts?.map(p => p.permittedMarks)).toEqual(Array(3).fill([0, 1]));
    expect(card('q13').rows[0].contextNote).toContain('2022 examination, not current benefits advice');
    expect(card('q14').rows[0].contextNote).toContain('income maximisation');
  });
  it('uses the 2022 deferred archive and maps all nineteen tasks to fourteen Atlas questions', () => {
    const file = 'LC098ALP014EV-deferred.pdf';
    const tags = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'home-economics-s-and-s' && p.year === 2022 && p.fileid === file)!;
    expect(anchors2022.q).toHaveLength(14);
    expect(preferredAnswersUrl('home-economics-s-and-s', 2022, file, 'stale')).toBe(`/paper-answers/2022/${file}.json`);
    for (const c of cards2022) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
      expect(c.paperFileid).toBe('LC098ALP014EV-deferred');
      const source = reviewedHomeEconomicsSource(c.id);
      expect(resolveIndexedPaperFileid('home-economics', 2022, 'higher', source)).toBe('LC098ALP014EV-deferred');
      const n = c.questionRef.match(/Q(\d+)/)![1];
      const mapping = runtime.questionMappings.find(r => r[0] === 'h' && r[1] === 'e' && r[2] === 2022 && r[4] === file && r[5] === n)!;
      expect(mapping?.[7]).toBe('deferred');
      const expected = Object.entries(crosswalk).filter(([k, nodes]) => k.includes('-higher-') && nodes.includes(c.topicId)).map(([k]) => k);
      expect(browseTopicIdsForQuestion(tags, tags.q.find(q => q.n === n)!)).toEqual(expect.arrayContaining(expected));
    }
    const wrongYear = structuredClone(review2022); wrongYear.year = 2023;
    expect(() => homeEconomicsSourceMap(wrongYear)).toThrow(/archive identity/);
    expect(() => reviewedHomeEconomicsSource('he-2022-hl-deferred-sb-q1a')).toThrow(/lacks reviewed sources/);
  });
});

describe('Home Economics deferred source boundaries', () => {
  it('keeps all 58 reviewed tasks with exact section totals and every canonical Atlas topic', () => {
    const sitting = CARDS.filter(c => c.id.startsWith('he-2023-hl-deferred-'));
    expect(sitting).toHaveLength(58);
    expect(sitting.reduce((n, c) => n + c.totalMarks, 0)).toBe(749);
    expect(sitting.map(c => c.id).sort()).toEqual(review.tasks.map(t => t.id).sort());
    const c = sitting.filter(c => c.id.includes('-sc-'));
    expect(c).toHaveLength(26);
    expect(c.reduce((n, c) => n + c.totalMarks, 0)).toBe(385);
    const file = 'LC098ALP039EV-deferred.pdf';
    const tags = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'home-economics-s-and-s' && p.year === 2023 && p.fileid === file)!;
    expect(bcAnchors.q.slice(5).map(q => q.region.map(r => r.p))).toEqual([[18, 19, 20, 21], [22, 23, 24], [25, 26, 27], [28, 29, 30]]);
    for (const card of c) {
      if (card.kind !== 'question') throw new Error(card.id);
      expect(tariffReconciles(card), card.id).toBe(true);
      for (const v of card.answerVariants ?? []) expect(tariffReconciles({ ...card, rows: v.rows }), `${card.id}/${v.id}`).toBe(true);
      expect(card.paperFileid).toBe('LC098ALP039EV-deferred');
      const n = String(Number(card.questionRef.match(/Q(\d+)/)![1]) + 5);
      const expected = Object.entries(crosswalk).filter(([k, nodes]) => k.includes('-higher-') && nodes.includes(card.topicId)).map(([k]) => k);
      const mapping = runtime.questionMappings.find(r => r[0] === 'h' && r[1] === 'e' && r[2] === 2023 && r[4] === file && r[5] === n)!;
      expect(mapping?.[7]).toBe('deferred');
      expect(browseTopicIdsForQuestion(tags, tags.q.find(q => q.n === n)!)).toEqual(expect.arrayContaining(expected));
    }
  });
  const getC = (part: string) => {
    const c = CARDS.find(c => c.id === `he-2023-hl-deferred-sc-q${part}`);
    if (!c || c.kind !== 'question') throw new Error(part);
    return c;
  };
  it('retains exact housing/design/electricity scoring and labels the MCB error', () => {
    expect(getC('1ai').questionText).toContain('nineteenth century');
    expect(getC('1ai').rows[0].contextNote).toContain('small living space and outdoor areas');
    expect(getC('1aiii').rows[0].parts?.map(p => p.permittedMarks)).toEqual(Array(3).fill([0, 3, 5]));
    expect(getC('1bi').rows.map(r => r.permittedMarks)).toEqual(Array(3).fill([0, 2, 4]));
    expect(getC('1bii').rows.map(r => r.parts?.map(p => p.permittedMarks))).toEqual(Array(3).fill(Array(3).fill([0, 2])));
    expect(getC('1bii').rows[0].contextNote).toContain('Rhythm:');
    expect(getC('1ci').rows[1].contextNote).toContain('An RCBO combines overcurrent and residual-current protection');
    expect(getC('1cii').rows.map(r => r.parts?.map(p => p.permittedMarks))).toEqual(Array(3).fill([[0, 3], [0, 3]]));
    expect(getC('1cii').rows[0].contextNote).toContain('no model reduction descriptions');
  });
  it('carries the graduation image and sketch into evaluation, retaining one open fabric profile', () => {
    expect(getC('2ai').questionFigure?.alt).toContain('Original graduation-ball photograph');
    expect(getC('2aii').questionFigure).toEqual(getC('2ai').questionFigure);
    expect(getC('2ai').rows.map(r => r.permittedMarks)).toEqual([[0, 1, 2, 3, 4], [0, 2, 4, 6]]);
    expect(getC('2aii').stem).toContain(getC('2ai').questionText);
    expect(getC('2aii').rows.map(r => r.permittedMarks)).toEqual(Array(3).fill([0, 3, 5]));
    expect(getC('2b').answerVariants?.map(v => v.label)).toEqual(['Cotton', 'Linen', 'Wool', 'Silk', 'Another valid natural fabric']);
    for (const variant of getC('2b').answerVariants ?? []) expect(variant.rows.map(r => r.marks)).toEqual([6, 4, 5]);
    expect(getC('2b').answerVariants?.[3].rows[2].contextNote).toContain('burns as black beads');
    expect(getC('2ci').rows[0].parts?.map(p => p.permittedMarks)).toEqual(Array(3).fill([0, 2, 3]));
  });
  it('preserves the full social-studies continuations and corrects core source errors', () => {
    expect(getC('3aiii').rows[0].contextNote).toContain('Social contact:');
    expect(getC('3bii').rows.map(r => r.permittedMarks)).toEqual([[0, 1, 2], [0, 2, 4, 6, 8]]);
    expect(getC('3bii').rows[1].contextNote).toContain('Night classes-');
    expect(getC('3bii').rows[1].contextNote).toContain('not current eligibility or funding advice');
    expect(getC('3ci').questionText).toContain('Analyse the key requirements');
    expect(getC('3cii').rows[1].contextNote).toContain('not a complete model evaluation');
    expect(getC('4ai').rows[0].parts?.map(p => p.permittedMarks)).toEqual(Array(5).fill([0, 1, 2, 3, 4]));
    expect(getC('4aii').rows.map(r => r.marks)).toEqual([12, 4, 4]);
    expect(getC('4aii').rows[0].contextNote).toContain('heading says “9 points”');
    expect(getC('4bi').rows.map(r => r.parts?.map(p => p.permittedMarks))).toEqual(Array(2).fill([[0, 3], [0, 1, 2], [0, 1, 2]]));
    expect(getC('4bi').rows[0].contextNote).toContain('Discount Electrical Stores');
    expect(getC('4bii').rows[0].contextNote).toContain('Outputs / Evaluation:');
    expect(getC('4ci').questionText).toContain('Describe three different');
    expect(getC('4cii').rows[0].contextNote).toContain('marriage creates no entitlement to sex');
    expect(getC('4cii').rows[0].contextNote).toContain('Family Home Protection Act 1976');
  });
  it('keeps all 17 Section B tasks and the full choice profiles at their published tariffs', () => {
    const b = CARDS.filter(c => c.id.startsWith('he-2023-hl-deferred-sb-'));
    expect(b).toHaveLength(17);
    expect(b.reduce((n, c) => n + c.totalMarks, 0)).toBe(280);
    const getB = (part: string) => {
      const c = b.find(c => c.id.endsWith(`q${part}`));
      if (!c || c.kind !== 'question') throw new Error(part);
      return c;
    };
    expect(getB('2a').rows.map(r => r.marks)).toEqual([8, 6, 8]);
    expect(getB('2a').rows[0].contextNote).toContain('ESPGHAN, 2024');
    expect(getB('2a').rows[0].contextNote).toContain('gluten in a baby’s diet before 6 months');
    expect(getB('2a').rows[2].contextNote).toContain('most people with coeliac disease tolerate avenin');
    expect(getB('2b').rows.map(r => r.permittedMarks)).toEqual(Array(4).fill([0, 2, 4]));
    expect(getB('2c').rows.map(r => r.parts?.map(p => p.permittedMarks))).toEqual(Array(2).fill([[0, 2, 4], [0, 2]]));
    expect(getB('2c').rows[0].contextNote).toContain('Cesar salad');
    expect(getB('3a').answerVariants).toHaveLength(4);
    expect(getB('3a').answerVariants?.[0].rows[1].contextNote).toContain('1.5 cm head space');
    expect(getB('3a').answerVariants?.[0].rows[2].contextNote).not.toContain('usually fruit');
    expect(getB('3a').answerVariants?.[1].rows[2].contextNote).toContain('usually fruit');
    expect(getB('3a').answerVariants?.[1].rows[2].contextNote).toContain('vacuum on cooling');
    expect(getB('3b').answerVariants).toHaveLength(5);
    expect(getB('3b').answerVariants?.[3].rows[2].contextNote).toContain('biodegradable');
    expect(getB('4b').rows.map(r => r.marks)).toEqual([6, 12, 6]);
    expect(getB('4c').answerVariants).toHaveLength(6);
    expect(getB('4c').answerVariants?.[0].rows[0].permittedMarks).toEqual([0, 1, 2]);
    expect(getB('5a').rows.map(r => r.permittedMarks)).toEqual(Array(4).fill([0, 3, 5]));
    expect(getB('5b').rows.map(r => r.marks)).toEqual([5, 5, 10]);
    expect(getB('5c').questionRef).toContain('Q5(c)');
    expect(getB('5c').rows[0].contextNote).toContain('scheme accidentally repeats (b)');
    const file = 'LC098ALP039EV-deferred.pdf';
    const tags = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'home-economics-s-and-s' && p.year === 2023 && p.fileid === file)!;
    for (const c of b) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
      for (const v of c.answerVariants ?? []) expect(tariffReconciles({ ...c, rows: v.rows }), `${c.id}/${v.id}`).toBe(true);
      const n = c.questionRef.match(/Q(\d+)/)![1];
      const expected = Object.entries(crosswalk).filter(([k, nodes]) => k.includes('-higher-') && nodes.includes(c.topicId)).map(([k]) => k);
      expect(browseTopicIdsForQuestion(tags, tags.q.find(q => q.n === n)!)).toEqual(expect.arrayContaining(expected));
    }
  });
  it('retains the B1 chart, three carbohydrate headings, paired classes and reserved environmental points', () => {
    const b1 = CARDS.filter(c => /^he-2023-hl-deferred-sb-q1[a-e]$/.test(c.id));
    expect(b1).toHaveLength(5);
    expect(b1.reduce((n, c) => n + c.totalMarks, 0)).toBe(80);
    const b = (part: string) => {
      const c = b1.find(c => c.id.endsWith(`q1${part}`));
      if (!c || c.kind !== 'question') throw new Error(part);
      return c;
    };
    expect(b('a').questionFigure?.alt).toContain('Potatoes: 14%, 21%, 26%, 33%, 38%, 43%');
    expect(b('a').questionFigure?.includesPrompt).toBe(false);
    expect(b('a').stem).toContain('evening meal');
    expect(b('a').rows.map(r => r.permittedMarks)).toEqual(Array(3).fill([0, 1, 2, 3, 4, 5, 6]));
    expect(b('a').rows[2].contextNote).toContain('rice puddings, risottos, curries');
    expect(b('b').rows.map(r => r.parts?.map(p => p.permittedMarks))).toEqual(Array(3).fill([[0, 2], [0, 2]]));
    expect(b('c').rows.map(r => r.parts?.map(p => p.permittedMarks))).toEqual(Array(3).fill([[0, 2, 3], [0, 2, 3]]));
    expect(b('d').rows[0].contextNote).toContain('no model descriptions');
    expect(b('e').rows.map(r => r.marks)).toEqual([4, 4, 12]);
    expect(b('e').rows[0].contextNote).toContain('consider food miles');
    expect(b('e').rows[1].contextNote).toContain('At least one point');
    expect(bcAnchors.q.map(q => q.n)).toEqual(['1', '2', '3', '4', '5', '6', '7', '8', '9']);
    expect(bcAnchors.q[0].region.map(r => r.p)).toEqual([8, 9]);
    const file = 'LC098ALP039EV-deferred.pdf';
    const tags = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'home-economics-s-and-s' && p.year === 2023 && p.fileid === file)!;
    for (const c of b1) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
      expect(c.paperFileid).toBe('LC098ALP039EV-deferred');
      const expected = Object.entries(crosswalk).filter(([k, nodes]) => k.includes('-higher-') && nodes.includes(c.topicId)).map(([k]) => k);
      expect(browseTopicIdsForQuestion(tags, tags.q[0])).toEqual(expect.arrayContaining(expected));
    }
    expect(preferredAnswersUrl('home-economics-s-and-s', 2023, file, 'stale')).toBe(`/paper-answers/2023/${file}.json`);
  });
  it('separates the two gel tasks while preserving every other required or open response', () => {
    expect(cards).toHaveLength(15);
    expect(cards.reduce((n, c) => n + c.totalMarks, 0)).toBe(84);
    expect(get('q1').totalMarks).toBe(4);
    expect(get('q1-example').totalMarks).toBe(2);
    expect(get('q1-example').stem).toBe('In relation to proteins.');
    for (const c of cards) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
      expect(c.paperFileid).toBe('LC098ALP014EV-deferred');
      expect(c.schemeCitation).toContain('deferred examination');
    }
  });
  it('retains given table context, all six export sectors and exact partial-credit ladders', () => {
    expect(get('q2').questionText).toContain('Secretion: Pancreatic juice');
    expect(get('q2').rows.map(r => r.permittedMarks)).toEqual(Array(3).fill([0, 1, 2]));
    expect(get('q3').rows.map(r => r.permittedMarks)).toEqual(Array(3).fill([0, 2]));
    expect(get('q6').rows).toHaveLength(3);
    expect(get('q6').rows[0].contextNote?.split('\n\n')).toHaveLength(7);
    expect(get('q6').rows[0].contextNote).toContain('Horticulture: Mushrooms; potatoes; vegetables; fruit.');
    expect(get('q6').rows[0].contextNote).toContain('Prepared consumer foods: Cooked meat; pizza; sauces; bakery; confectionary.');
    expect(get('q8').rows.map(r => r.permittedMarks)).toEqual([[0, 2, 4], [0, 2]]);
    expect(get('q8').rows[0].contextNote).toContain('market value and/or a longer shelf life');
    expect(get('q10').rows[0].contextNote).toContain('access to funds');
    expect(get('q11').rows.map(r => r.permittedMarks)).toEqual(Array(2).fill([0, 2, 3]));
    expect(get('q12').rows[0].contextNote).toContain('“Current” refers to this 2023 examination');
    expect(get('q14').rows.map(r => r.verbatim)).toEqual(['Cause', 'Effect', 'Reduction measure']);
  });
  it('fails closed on a June archive, swapped component, changed bytes or undeclared task', () => {
    for (const kind of ['a', 'bc', 'scheme'] as const) {
      const bad = structuredClone(review);
      bad.sources[kind].path = bad.sources[kind].path.replace('deferredexams', 'exampapers').replace('deferredmarkingschemes', 'markingschemes');
      expect(() => homeEconomicsSourceMap(bad)).toThrow(/archive identity/);
    }
    const bad = structuredClone(review); bad.sources.a.fileid = bad.sources.bc.fileid;
    expect(() => homeEconomicsSourceMap(bad)).toThrow(/archive identity/);
    expect(() => homeEconomicsSourceMap(review, () => Buffer.from('wrong document'))).toThrow(/bytes differ/);
    expect(() => reviewedHomeEconomicsSource('he-2023-hl-deferred-sa-q99')).toThrow(/lacks reviewed sources/);
    expect(reviewedHomeEconomicsSource('he-2023-hl-sa-q1')).toBeUndefined();
    expect(resolveIndexedPaperFileid('home-economics', 2023, 'higher', reviewedHomeEconomicsSource(get('q1').id))).toBe('LC098ALP014EV-deferred');
    expect(() => resolveIndexedPaperFileid('home-economics', 2023, 'ordinary', reviewedHomeEconomicsSource(get('q1').id))).toThrow(/No unique indexed/);
  });
  it('maps every new task to its own deferred Atlas question and every canonical topic', () => {
    const file = 'LC098ALP014EV-deferred.pdf';
    const tags = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'home-economics-s-and-s' && p.year === 2023 && p.fileid === file)!;
    expect(tags).toBeDefined();
    expect(anchors.q).toHaveLength(14);
    expect(anchors.schemeFileid).toBe('LC098ALP000EV-deferred.pdf');
    expect(preferredAnswersUrl('home-economics-s-and-s', 2023, file, 'stale')).toBe(`/paper-answers/2023/${file}.json`);
    for (const c of cards) {
      const n = c.questionRef.match(/Q(\d+)/)![1];
      const row = runtime.questionMappings.find(r => r[0] === 'h' && r[1] === 'e' && r[2] === 2023 && r[4] === file && r[5] === n)!;
      expect(row, c.id).toBeDefined();
      const topics = (row[6] as number[]).map(i => runtime.topicIds[i]);
      const expected = Object.entries(crosswalk).filter(([k, nodes]) => k.includes('-higher-') && nodes.includes(c.topicId)).map(([k]) => k);
      expect(topics).toEqual(expect.arrayContaining(expected));
      const question = tags.q.find(q => q.n === n)!;
      expect(browseTopicIdsForQuestion(tags, question)).toEqual(expect.arrayContaining(expected));
    }
  });
});
