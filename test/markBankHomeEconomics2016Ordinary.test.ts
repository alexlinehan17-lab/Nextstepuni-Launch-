import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/home-economics/ordinary';
import { tariffReconciles } from '../types/markBank';
import runtime from '../data/examTopics/home-economics-s-and-s-question-runtime.json';
import crosswalk from '../data/examTopics/home-economics-s-and-s-curriculum-crosswalk.json';
import anchors from '../scripts/paper-trail/answers/2016/LC098GLP000EV.pdf.json';
import review from '../scripts/markbank/authoring/home-economics/2016-ol-main-review.json';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
const all = CARDS.filter(c => c.id.startsWith('he-2016-ol-'));
const get = (id: string) => {
  const c = all.find(c => c.id === `he-2016-ol-${id}`);
  if (!c || c.kind !== 'question') throw new Error(id);
  return c;
};
describe('2016 Ordinary Home Economics: independently swept original sources', () => {
  it('retains all 48 priced tasks and 627 offered marks', () => {
    expect(all).toHaveLength(48);
    expect(all.map(c => c.id).sort()).toEqual(review.tasks.map(c => c.id).sort());
    expect(['sa', 'sb', 'sc'].map(s => all.filter(c => c.id.includes(`-${s}-`)).length)).toEqual([12, 16, 20]);
    expect(all.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(627);
    for (const c of all) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
      for (const v of c.answerVariants ?? []) expect(tariffReconciles({ ...c, rows: v.rows }), `${c.id}/${v.id}`).toBe(true);
    }
  });
  it('preserves whole-six tariffs, all companion asks and complete A choices', () => {
    for (let n = 1; n <= 12; n++) {
      const c = get(`sa-q${n}`);
      expect(c.tariffModel?.kind).toBe('questionTotal');
      expect(c.rows.every(r => r.marks === null && !r.permittedMarks && !r.parts)).toBe(true);
      expect(c.rows[0].contextNote).toContain('no per-answer allocation');
    }
    expect(get('sa-q1').rows.every(r => r.verbatim.endsWith('— True'))).toBe(true);
    expect(get('sa-q3').rows).toHaveLength(4);
    expect(get('sa-q3').questionText).toContain('Name two good dietary sources');
    expect(get('sa-q5').rows[2].contextNote).toContain('ONE lifestyle change');
    expect(get('sa-q6').rows.map(r => r.verbatim)).toEqual(['lactic acid', 'rennin', 'curds']);
    expect(get('sa-q7').rows.map(r => r.verbatim.split(' — ')[1])).toEqual(['True', 'False', 'True']);
    expect(get('sa-q8').rows).toHaveLength(3);
    expect(get('sa-q8').rows[0].contextNote).toContain('ANY TWO examples for EACH');
    expect(get('sa-q9').rows[1].contextNote).toContain('no compulsory USC choice');
    expect(get('sa-q10').rows.map(r => r.verbatim)).toEqual(['hand wash only', 'do not bleach']);
    expect(get('sa-q11').rows.map(r => r.verbatim)).toEqual(['Kettle — Element', 'Food processor — Motor', 'Toaster — Element']);
    expect(get('sa-q12').questionText).toContain('Explain the benefit');
  });
  it('retains all eleven original crops and each dependent picture', () => {
    expect(Object.keys(review.figures)).toHaveLength(11);
    expect(new Set(all.flatMap(c => c.kind === 'question' && c.questionFigure ? [c.questionFigure.src] : [])).size).toBe(10);
    expect(new Set(all.flatMap(c => c.kind === 'question' && c.figure ? [c.figure.src] : [])).size).toBe(1);
    expect(get('sa-q6').questionFigure?.alt).toContain('every blank');
    expect(get('sb-q1a').questionFigure?.alt).toContain('all ingredients');
    expect(get('sb-q2b').figure?.alt).toContain('Egg Mayonnaise');
    for (const id of ['sc-q1ai', 'sc-q1aii', 'sc-q1aiii']) expect(get(id).questionFigure?.alt).toContain('original kitchen layout');
    for (const id of ['sc-q2ai', 'sc-q2aii']) expect(get(id).questionFigure?.alt).toContain('male and female');
  });
  it('keeps both meal models, complete lipid headings and shared roman tariffs', () => {
    expect(get('sb-q1a').answerVariants?.map(v => v.label)).toEqual(['Fisherman’s pie', 'Chicken curry with rice']);
    expect(get('sb-q1a').rows.map(r => r.marks)).toEqual([2, 18]);
    expect(get('sb-q1a').rows[1].contextNote).toContain('retained as printed');
    expect(get('sb-q1b').rows.map(r => r.marks)).toEqual([8, 8, 12]);
    expect(get('sb-q2b').rows.map(r => r.marks)).toEqual([6, 6, 6]);
    expect(get('sb-q2b').rows[2].contextNote).toContain('Egg Mayonnaise');
    expect(get('sb-q2c').rows.map(r => r.marks)).toEqual([4, 4, 4]);
    expect(get('sb-q3a').rows.map(r => r.marks)).toEqual([5, 5, 10]);
    expect(get('sb-q3a').questionText).toContain('(ii)');
    expect(get('sb-q3b').rows.map(r => r.marks)).toEqual([5, 5, 10]);
    expect(get('sb-q3b').questionText).toContain('effects of heat');
    expect(get('sb-q5b').rows[0].parts).toHaveLength(4);
    expect(get('sb-q5b').rows[0].contextNote).toContain('no separate quota');
  });
  it('preserves the coherent budget, savings model gaps and all historical marriage options', () => {
    expect(get('sb-q4b').stem).toContain('€220');
    expect(get('sb-q4b').stem).toContain('cycles to college');
    expect(get('sb-q4b').rows[0].contextNote).toContain('rent 25%');
    expect(get('sb-q4b').rows[0].parts).toHaveLength(5);
    expect(get('sb-q4c').answerVariants).toHaveLength(5);
    expect(get('sb-q4c').answerVariants?.find(v => v.label === 'Building society')?.rows[1].contextNote).toContain('no reason model');
    expect(get('sb-q5c').answerVariants).toHaveLength(8);
    expect(get('sb-q5c').rows.map(r => r.marks)).toEqual([5, 10]);
    expect(get('sb-q5c').answerVariants?.find(v => v.label === 'Divorce')?.rows[1].contextNote).toContain('four out of the previous five years');
    expect(get('sb-q5c').answerVariants?.find(v => v.label === 'Church nullity')?.rows[1].contextNote).toContain('no legal standing');
    for (const c of all.filter(c => c.id.includes('-sb-q5'))) expect(c.topicId).toBe('home-economics-2-1');
  });
  it('keeps required accommodation pairs, complete fabric choices and the leisure continuation', () => {
    expect(get('sc-q1ai').rows.map(r => r.marks)).toEqual([5, 5, 5, 5]);
    expect(get('sc-q1bii').answerVariants).toHaveLength(5);
    expect(get('sc-q1bii').rows.map(r => r.marks)).toEqual([4, 6]);
    expect(get('sc-q1cii').taskGroups?.map(g => g.marks)).toEqual([6, 6, 6]);
    expect(get('sc-q1cii').rows.map(r => r.marks)).toEqual([3, 3, 3, 3, 3, 3]);
    expect(get('sc-q1cii').rows[3].contextNote).toContain('panic button');
    expect(get('sc-q2ai').rows.map(r => r.marks)).toEqual([6, 6, 6]);
    expect(get('sc-q2aii').answerVariants).toHaveLength(9);
    expect(get('sc-q2aii').answerVariants?.find(v => v.label === 'polyester cotton')?.rows[1].contextNote).toContain('low static level');
    expect(get('sc-q2bi').answerVariants).toHaveLength(5);
    expect(get('sc-q2bi').rows.map(r => r.marks)).toEqual([6, 3]);
    expect(get('sc-q2bi').answerVariants?.find(v => v.label === 'silk')?.rows[0].contextNote).toContain('mulberry tree');
    expect(get('sc-q2bi').rows[1].contextNote).toContain('bonding:');
    expect(get('sc-q3aii').rows.map(r => r.marks)).toEqual([5, 5, 10]);
    expect(get('sc-q3aiii').rows[0].contextNote).toContain('€6.06');
    expect(get('sc-q3bii').rows[0].group?.options).toHaveLength(9);
    expect(get('sc-q3bii').rows[1].contextNote).toContain('not complete two-point worked accounts');
    expect(get('sc-q3cii').rows.map(r => r.marks)).toEqual([6, 6, 6, 6]);
    expect(get('sc-q3cii').rows[1].contextNote).toContain('career breaks');
    expect(get('sc-q3cii').rows[3].contextNote).toContain('walking');
  });
  it('preserves twenty original Atlas identities and maps every canonical topic', () => {
    expect(anchors.q.map(q => q.n)).toEqual(Array.from({ length: 20 }, (_, i) => String(i + 1)));
    expect(anchors.q.find(q => q.n === '13')!.region.map(r => r.p)).toEqual([8, 9]);
    expect(anchors.q.find(q => q.n === '18')!.region.map(r => r.p)).toEqual([15, 16, 17]);
    expect(anchors.q.find(q => q.n === '19')!.region.map(r => r.p)).toEqual([18, 19]);
    expect(anchors.q.find(q => q.n === '20')!.region.map(r => r.p)).toEqual([20, 21, 22]);
    for (const q of anchors.q) expect(q.pY[1]).toBeGreaterThan(q.pY[0]);
    const file = 'LC098GLP000EV.pdf';
    const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'home-economics-s-and-s' && p.year === 2016 && p.level === 'ordinary' && p.lang === 'ev' && p.fileid === file)!;
    for (const c of all) {
      const m = c.questionRef.match(/Section ([ABC]) (?:E\d )?Q(\d+)/)!;
      const n = String(Number(m[2]) + (m[1] === 'A' ? 0 : m[1] === 'B' ? 12 : 17));
      const row = runtime.questionMappings.find(q => q[0] === 'o' && q[1] === 'e' && q[2] === 2016 && q[4] === file && q[5] === n)!;
      expect(row, c.id).toBeDefined();
      expect((row[6] as number[]).map(i => runtime.topicIds[i]).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
      expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === n)!).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
    }
  });
});
