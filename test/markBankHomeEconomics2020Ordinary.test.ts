import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/home-economics/ordinary';
import { tariffReconciles } from '../types/markBank';
import runtime from '../data/examTopics/home-economics-s-and-s-question-runtime.json';
import crosswalk from '../data/examTopics/home-economics-s-and-s-curriculum-crosswalk.json';
import anchorsA from '../scripts/paper-trail/answers/2020/LC098GLP014EV.pdf.json';
import anchorsBC from '../scripts/paper-trail/answers/2020/LC098GLP039EV.pdf.json';
import review from '../scripts/markbank/authoring/home-economics/2020-ol-main-review.json';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
const all = CARDS.filter(c => c.id.startsWith('he-2020-ol-'));
const get = (id: string) => {
  const c = all.find(c => c.id === `he-2020-ol-${id}`);
  if (!c || c.kind !== 'question') throw new Error(id);
  return c;
};
describe('2020 Ordinary Home Economics: independent 78-page original sweep', () => {
  it('reconciles 55 printed leaves to 56 priced tasks without flattening choices', () => {
    expect(review.expectedSourceLeaves).toBe(55);
    expect(review.expectedSectionSourceLeaves).toEqual({ A: 13, B: 20, C: 22 });
    expect(all).toHaveLength(56);
    expect(all.map(c => c.id).sort()).toEqual(review.tasks.map(c => c.id).sort());
    expect(['sa', 'sb', 'sc'].map(s => all.filter(c => c.id.includes(`-${s}-`)).length)).toEqual([15, 19, 22]);
    expect(all.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(627);
    for (const c of all) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(c.questionRef, c.id).toMatch(/^2020 OL Section /);
      expect(tariffReconciles(c), c.id).toBe(true);
      for (const v of c.answerVariants ?? []) expect(tariffReconciles({ ...c, rows: v.rows }), `${c.id}/${v.id}`).toBe(true);
    }
  });
  it('keeps original truth positions, named definitions and separately priced companions', () => {
    for (const [n, answers] of [[1, ['True', 'False', 'True']], [5, ['True', 'True', 'False']], [9, ['False', 'True', 'True']]] as const) {
      expect(get(`sa-q${n}`).rows.map(r => r.verbatim.split(' — ').at(-1))).toEqual(answers);
      expect(get(`sa-q${n}`).rows.map(r => r.marks)).toEqual([2, 2, 2]);
    }
    expect(get('sa-q2').rows.map(r => r.verbatim)).toEqual(['Smoke point', 'Flash point']);
    expect(get('sa-q2').rows.map(r => r.permittedMarks)).toEqual([[0, 2, 3], [0, 2, 3]]);
    expect(get('sa-q6-definition').totalMarks).toBe(2);
    expect(get('sa-q6-additives').totalMarks).toBe(4);
    expect(get('sa-q8-foods').totalMarks).toBe(4);
    expect(get('sa-q8-careers').totalMarks).toBe(2);
    expect(get('sa-q10-advantages').totalMarks).toBe(4);
    expect(get('sa-q10-payment').totalMarks).toBe(2);
    expect(get('sa-q4').rows.map(r => r.marks)).toEqual([2, 4]);
    expect(get('sa-q4').rows[1].contextNote).toContain('SAME TWO');
    expect(get('sa-q4').rows[0].contextNote).toContain('emulsifying');
  });
  it('retains ten complete original figures, both companion contexts and no footer leakage', () => {
    expect(Object.keys(review.figures)).toHaveLength(10);
    expect(new Set(all.flatMap(c => c.kind === 'question' && c.questionFigure ? [c.questionFigure.src] : [])).size).toBe(10);
    expect(get('sa-q3').questionFigure?.alt).toContain('all three blanks');
    expect(get('sa-q12').questionFigure?.alt).toContain('goodhousekeeping.com');
    expect(get('sb-q1ai').questionFigure?.alt).toContain('Thinking House / Bord Bia');
    expect(get('sc-q1ai').questionFigure?.src).toBe(get('sc-q1aii').questionFigure?.src);
    expect(get('sc-q2ai').questionFigure?.src).toBe(get('sc-q2aii').questionFigure?.src);
    expect(get('sc-q2ai').questionFigure?.alt).toContain('dunnesstores.com');
    for (const c of all) if (c.kind === 'question') expect(c.questionText + c.stem).not.toMatch(/Leaving Certificate Examination|Section A and answerbook/);
  });
  it('preserves the iron quotas, source menu columns and flexible fish roman pool', () => {
    expect(get('sb-q1ai').rows[0].parts).toHaveLength(4);
    expect(get('sb-q1ai').rows[0].parts?.[0].permittedMarks).toEqual([0, 2, 4, 6]);
    expect(get('sb-q1ai').rows[0].contextNote).toContain('Animal welfare:');
    expect(get('sb-q1b').rows.map(r => r.marks)).toEqual([8, 12, 4]);
    expect(get('sb-q1d').rows.map(r => r.marks)).toEqual([5, 5, 10]);
    expect(get('sb-q2ai').totalMarks).toBe(4);
    expect(get('sb-q2aii').totalMarks).toBe(12);
    const menu = get('sb-q2c');
    expect(menu.taskGroups?.map(g => g.marks)).toEqual([6, 6, 6]);
    expect(menu.rows.map(r => r.marks)).toEqual([4, 2, 4, 2, 4, 2]);
    expect(menu.rows[0].contextNote).toContain('Porridge with low fat milk');
    expect(menu.rows[0].contextNote).not.toContain('Carrot and Lentil');
    expect(menu.rows[2].contextNote).toContain('Carrot and Lentil soup');
    expect(menu.rows[4].contextNote).toContain('Vegetable stir fry');
    expect(get('sb-q3a').rows.map(r => r.marks)).toEqual([8, 8, 4]);
    expect(get('sb-q3a').rows[2].contextNote).toContain('additional distinct');
    expect(get('sb-q3b').rows.map(r => r.marks)).toEqual([8, 8]);
  });
  it('keeps matching packaging profiles, required appliance headings and exact marriage steps', () => {
    const c = get('sb-q3c');
    expect(c.taskGroups?.map(g => g.marks)).toEqual([7, 7]);
    expect(c.rows.map(r => r.marks)).toEqual([3, 4, 3, 4]);
    for (const label of ['Metal:', 'Glass:', 'Paper:', 'Plastic:', 'Polystyrene:']) expect(c.rows[0].contextNote).toContain(label);
    expect(c.rows[3].contextNote).toContain('SAME material 2');
    expect(get('sb-q4c').rows.map(r => r.marks)).toEqual([12, 4, 3, 3]);
    expect(get('sb-q4c').rows[2].contextNote).toContain('ONE required reference to care');
    expect(get('sb-q4c').rows[3].contextNote).toContain('ONE required reference to cleaning');
    expect(get('sb-q5ai').rows[0].permittedMarks).toEqual([0, 2, 3, 5]);
    expect(get('sb-q5c').rows[1].contextNote).toContain('Judicial Separation:');
    expect(get('sb-q5c').rows[1].contextNote).toContain('Family Law Act 2019');
  });
  it('preserves coherent elective choices, cross-page profiles and visible name-only gaps', () => {
    expect(get('sc-q1aiii').taskGroups?.map(g => g.marks)).toEqual([5, 5]);
    expect(get('sc-q1aiii').rows[0].contextNote).toContain('Builder:');
    expect(get('sc-q1aiii').rows[0].contextNote).toContain('Interior Designer');
    expect(get('sc-q1aiii').rows[1].contextNote).toContain('no description model is invented');
    expect(get('sc-q1bii').rows.map(r => r.marks)).toEqual([3, 6, 3, 6]);
    expect(get('sc-q1bii').rows[0].contextNote).toContain('electric motor rotates blades');
    expect(get('sc-q1cii').answerVariants).toHaveLength(8);
    expect(get('sc-q1cii').answerVariants?.[6].rows[1].contextNote).toContain('name only');
    expect(get('sc-q2ai').rows.map(r => r.marks)).toEqual([6, 6, 6]);
    expect(get('sc-q2aii').answerVariants).toHaveLength(8);
    expect(get('sc-q2bii').answerVariants).toHaveLength(6);
    expect(get('sc-q2bii').answerVariants?.[4].rows[1].contextNote).toContain('no detailed model');
    expect(get('sc-q2cii').rows[0].contextNote).toContain('no expanded detail model or fixed name/detail allocation');
  });
  it('keeps required social-study categories and complete continuation guidance', () => {
    expect(get('sc-q3ai').rows.map(r => r.permittedMarks)).toEqual([[0, 2, 3], [0, 2, 3]]);
    expect(get('sc-q3aiii').rows.map(r => r.marks)).toEqual([4, 4, 8]);
    expect(get('sc-q3aiv').rows.map(r => r.marks)).toEqual([2, 6]);
    expect(get('sc-q3aiv').rows[0].contextNote).toContain('Emotional support; social support');
    expect(get('sc-q3bii').rows.map(r => r.marks)).toEqual([3, 4, 3, 4]);
    expect(get('sc-q3bii').rows[0].contextNote).toContain('Early Start Programme');
    expect(get('sc-q3bii').rows[0].contextNote).toContain('School-age childcare');
    expect(get('sc-q3ci').rows.map(r => r.marks)).toEqual([6, 6, 6]);
    expect(get('sc-q3ci').rows[2].contextNote).toContain('Home School Community Liaison Scheme');
    expect(get('sc-q3cii').rows[0].parts).toHaveLength(3);
  });
  it('preserves seventeen original Atlas IDs and restores the three elective groups', () => {
    expect(get('sa-q11').topicId).toBe('home-economics-3-3');
    expect(get('sb-q3c').topicId).toBe('home-economics-0-11');
    expect(anchorsA.q.map(q => q.n)).toEqual(Array.from({ length: 12 }, (_, i) => String(i + 1)));
    expect(anchorsBC.q.map(q => q.n)).toEqual(Array.from({ length: 8 }, (_, i) => String(i + 1)));
    expect(anchorsBC.q.find(q => q.n === '1')!.region.map(r => r.p)).toEqual([8, 9]);
    expect(anchorsBC.q.find(q => q.n === '6')!.region.map(r => r.p)).toEqual([14, 15, 16]);
    expect(anchorsBC.q.find(q => q.n === '7')!.region.map(r => r.p)).toEqual([17, 18]);
    expect(anchorsBC.q.find(q => q.n === '8')!.region.map(r => r.p)).toEqual([19, 20, 21]);
    for (const c of all) {
      const m = c.questionRef.match(/Section ([ABC]) (?:E\d )?Q(\d+)/)!;
      const file = m[1] === 'A' ? 'LC098GLP014EV.pdf' : 'LC098GLP039EV.pdf';
      const n = String(Number(m[2]) + (m[1] === 'C' ? 5 : 0));
      const row = runtime.questionMappings.find(q => q[0] === 'o' && q[1] === 'e' && q[2] === 2020 && q[4] === file && q[5] === n)!;
      expect(row, c.id).toBeDefined();
      expect((row[6] as number[]).map(i => runtime.topicIds[i]).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
      const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'home-economics-s-and-s' && p.year === 2020 && p.level === 'ordinary' && p.lang === 'ev' && p.fileid === file)!;
      expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === n)!).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
    }
  });
});
