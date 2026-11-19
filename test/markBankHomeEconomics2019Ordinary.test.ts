import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/home-economics/ordinary';
import { tariffReconciles } from '../types/markBank';
import runtime from '../data/examTopics/home-economics-s-and-s-question-runtime.json';
import crosswalk from '../data/examTopics/home-economics-s-and-s-curriculum-crosswalk.json';
import anchors from '../scripts/paper-trail/answers/2019/LC098GLP000EV.pdf.json';
import review from '../scripts/markbank/authoring/home-economics/2019-ol-main-review.json';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
const all = CARDS.filter(c => c.id.startsWith('he-2019-ol-'));
const get = (id: string) => {
  const c = all.find(c => c.id === `he-2019-ol-${id}`);
  if (!c || c.kind !== 'question') throw new Error(id);
  return c;
};
describe('2019 Ordinary Home Economics: independently swept original sources', () => {
  it('retains all 52 priced tasks and 627 offered marks', () => {
    expect(all).toHaveLength(52);
    expect(all.map(c => c.id).sort()).toEqual(review.tasks.map(c => c.id).sort());
    expect(['sa', 'sb', 'sc'].map(s => all.filter(c => c.id.includes(`-${s}-`)).length)).toEqual([12, 20, 20]);
    expect(all.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(627);
    for (const c of all) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
      for (const v of c.answerVariants ?? []) expect(tariffReconciles({ ...c, rows: v.rows }), `${c.id}/${v.id}`).toBe(true);
    }
  });
  it('keeps exact short-question answers, companion asks and new partial ladders', () => {
    for (let n = 1; n <= 12; n++) expect(get(`sa-q${n}`).tariffModel?.kind).toBe('fixed');
    expect(get('sa-q1').rows.map(r => r.verbatim.split(' — ').at(-1))).toEqual(['True', 'True', 'False']);
    expect(get('sa-q8').rows.map(r => r.verbatim.split(' — ').at(-1))).toEqual(['False', 'True', 'True']);
    expect(get('sa-q3').rows.map(r => r.marks)).toEqual([2, 4]);
    expect(get('sa-q3').rows[0].permittedMarks).toEqual([0, 1, 2]);
    expect(get('sa-q3').rows[1].contextNote).toContain('ANY TWO different dishes');
    expect(get('sa-q5').rows.map(r => r.verbatim)).toEqual(['Citrus fruit', 'Dried fruit', 'Stone fruit']);
    expect(get('sa-q5').rows[2].contextNote).toContain('avocado');
    expect(get('sa-q7').rows.map(r => r.marks)).toEqual([4, 2]);
    expect(get('sa-q7').rows[1].contextNote).toContain('SAME TWO');
    expect(get('sa-q10').rows.map(r => r.marks)).toEqual([4, 2]);
    expect(get('sa-q11').rows.map(r => r.permittedMarks)).toEqual([[0, 2, 3], [0, 2, 3]]);
    expect(get('sa-q12').rows.map(r => r.marks)).toEqual([3, 3]);
  });
  it('keeps all ten complete original inputs and the jacket companion image', () => {
    expect(Object.keys(review.figures)).toHaveLength(10);
    expect(new Set(all.flatMap(c => c.kind === 'question' && c.questionFigure ? [c.questionFigure.src] : [])).size).toBe(10);
    expect(get('sa-q2').questionFigure?.alt).toContain('rhodopsin, rickets, ascorbic acid');
    expect(get('sa-q9').questionFigure?.alt).toContain('shrink, static, proban');
    expect(get('sb-q1ai').questionFigure?.alt).toContain('rolls/buns/baps 26');
    expect(get('sb-q1aii').questionFigure?.alt).toContain('Bord Bia 2017');
    expect(get('sc-q1ai').questionFigure?.alt).toContain('cbaarchitecture.ie');
    expect(get('sc-q2aii').questionFigure?.src).toBe(get('sc-q2ai').questionFigure?.src);
    for (const c of all) if (c.kind === 'question') expect(c.questionText + c.stem).not.toMatch(/previous|running|Leaving Certificate Examination/);
    expect(get('sb-q1ai').stem).not.toContain('8080');
  });
  it('preserves matching bread accounts, full nutrient pools and three coherent menus', () => {
    expect(get('sb-q1ai').taskGroups?.map(g => g.marks)).toEqual([5, 5, 5, 5]);
    expect(get('sb-q1ai').rows.map(r => r.marks)).toEqual([2, 3, 2, 3, 2, 3, 2, 3]);
    expect(get('sb-q1ai').rows[1].contextNote).toContain('Rolls/Buns/Baps');
    expect(get('sb-q1aii').rows.map(r => r.permittedMarks)).toEqual([[0, 1, 2, 3], [0, 2]]);
    expect(get('sb-q1b').rows.map(r => r.marks)).toEqual([6, 12, 8]);
    expect(get('sb-q1b').rows[1].parts?.[0].permittedMarks).toEqual([0, 4]);
    expect(get('sb-q1d').rows.map(r => r.marks)).toEqual([5, 5, 5, 5]);
    expect(get('sb-q2b').taskGroups?.map(g => g.marks)).toEqual([6, 6, 6]);
    expect(get('sb-q2b').rows.map(r => r.marks)).toEqual([4, 2, 4, 2, 4, 2]);
    expect(get('sb-q2b').rows[0].contextNote).toContain('Poached eggs');
    expect(get('sb-q2b').rows[2].contextNote).toContain('Tuna and pasta salad');
    expect(get('sb-q2b').rows[4].contextNote).toContain('Chicken curry');
  });
  it('reconciles shared roman tariffs and preserves separately priced roman tasks', () => {
    expect(get('sb-q2c').rows.map(r => r.marks)).toEqual([4, 4, 4]);
    expect(get('sb-q2c').rows[2].contextNote).toContain('no 6/6 split');
    expect(get('sb-q3a').rows.map(r => r.marks)).toEqual([8, 8, 4]);
    expect(get('sb-q3a').rows[2].contextNote).toContain('no fixed 10/10 split');
    expect([get('sb-q3bi').totalMarks, get('sb-q3bii').totalMarks]).toEqual([9, 9]);
    expect([get('sb-q4bi').totalMarks, get('sb-q4bii').totalMarks]).toEqual([12, 8]);
    expect([get('sb-q5ai').totalMarks, get('sb-q5aii').totalMarks]).toEqual([16, 4]);
    expect(get('sb-q5aii').rows[0].permittedMarks).toEqual([0, 1, 2, 4]);
    expect(get('sb-q5aii').rows[0].contextNote).toContain('Emotional');
    expect(get('sb-q5c').rows[0].parts?.[0].permittedMarks).toEqual([0, 2, 5]);
    expect(get('sb-q5c').rows[0].contextNote).toContain('both sides');
  });
  it('keeps housing continuations, exact heating tariffs and matched lighting details', () => {
    expect(get('sc-q1aii').rows.map(r => r.marks)).toEqual([5, 5, 5, 5]);
    expect(get('sc-q1aiii').rows[0].parts?.[0].permittedMarks).toEqual([0, 3]);
    expect(get('sc-q1aiii').rows[0].contextNote).toContain('€65.00');
    expect(get('sc-q1bii').taskGroups?.map(g => g.marks)).toEqual([6, 6]);
    expect(get('sc-q1bii').rows[1].contextNote).toContain('without detailed model accounts');
    expect(get('sc-q1ci').rows.map(r => r.marks)).toEqual([3, 4, 4, 4]);
    expect(get('sc-q1ci').rows[2].permittedMarks).toEqual([0, 4]);
    expect(get('sc-q1ci').rows[3].contextNote).toContain('smart phone');
    expect(get('sc-q1cii').rows[0].contextNote).toContain('no fixed category quota');
    expect(get('sc-q2aii').rows.map(r => r.permittedMarks)).toEqual([[0, 1, 3], [0, 2, 4]]);
  });
  it('preserves all manufactured-fabric and voluntary-organisation profiles and source gaps', () => {
    const fabric = get('sc-q2b');
    expect(fabric.answerVariants?.map(v => v.label)).toEqual(['Viscose', 'Nylon', 'Acetate', 'tri-acetate', 'Polyester', 'Acrylic', 'Another valid manufactured fabric']);
    for (const v of fabric.answerVariants ?? []) expect(v.rows.map(r => r.marks)).toEqual([6, 3, 6]);
    expect(fabric.answerVariants?.[0].rows[0].contextNote).toContain('spinneret');
    expect(fabric.answerVariants?.[1].rows[1].contextNote).toContain('mildew resistant');
    expect(fabric.answerVariants?.[2].rows[0].contextNote).toContain('no production model');
    expect(fabric.rows[2].contextNote).toContain('no requirement to describe both');
    expect(get('sc-q2cii').rows[0].contextNote).toContain('ONE selected pattern-envelope');
    expect(get('sc-q3ai').rows[0].parts?.[0].permittedMarks).toEqual([0, 3]);
    expect(get('sc-q3bii').rows.map(r => r.marks)).toEqual([5, 5, 5]);
    expect(get('sc-q3cii').answerVariants).toHaveLength(6);
    expect(get('sc-q3cii').answerVariants?.[2].rows[1].contextNote).toContain('job opportunities');
    expect(get('sc-q3cii').answerVariants?.[4].rows[1].contextNote).toContain('accepted by name only');
  });
  it('preserves twenty original Atlas identities and maps every canonical topic', () => {
    expect(anchors.q.map(q => q.n)).toEqual(Array.from({ length: 20 }, (_, i) => String(i + 1)));
    expect(anchors.q.find(q => q.n === '6')!.region.map(r => r.p)).toEqual([5]);
    expect(anchors.q.find(q => q.n === '13')!.region.map(r => r.p)).toEqual([8, 9]);
    expect(anchors.q.find(q => q.n === '18')!.region.map(r => r.p)).toEqual([15, 16, 17]);
    expect(anchors.q.find(q => q.n === '19')!.region.map(r => r.p)).toEqual([18, 19]);
    expect(anchors.q.find(q => q.n === '20')!.region.map(r => r.p)).toEqual([20, 21]);
    for (const q of anchors.q) expect(q.pY[1]).toBeGreaterThan(q.pY[0]);
    const file = 'LC098GLP000EV.pdf';
    const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'home-economics-s-and-s' && p.year === 2019 && p.level === 'ordinary' && p.lang === 'ev' && p.fileid === file)!;
    for (const c of all) {
      const m = c.questionRef.match(/Section ([ABC]) (?:E\d )?Q(\d+)/)!;
      const n = String(Number(m[2]) + (m[1] === 'A' ? 0 : m[1] === 'B' ? 12 : 17));
      const row = runtime.questionMappings.find(q => q[0] === 'o' && q[1] === 'e' && q[2] === 2019 && q[4] === file && q[5] === n)!;
      expect(row, c.id).toBeDefined();
      expect((row[6] as number[]).map(i => runtime.topicIds[i]).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
      expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === n)!).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
    }
  });
});
