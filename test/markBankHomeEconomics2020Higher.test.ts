import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/home-economics/higher';
import { tariffReconciles } from '../types/markBank';
import runtime from '../data/examTopics/home-economics-s-and-s-question-runtime.json';
import crosswalk from '../data/examTopics/home-economics-s-and-s-curriculum-crosswalk.json';
import anchorsA from '../scripts/paper-trail/answers/2020/LC098ALP014EV.pdf.json';
import anchorsBC from '../scripts/paper-trail/answers/2020/LC098ALP039EV.pdf.json';
import review from '../scripts/markbank/authoring/home-economics/2020-hl-main-review.json';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
const all = CARDS.filter(c => c.id.startsWith('he-2020-hl-'));
const get = (id: string) => {
  const c = all.find(c => c.id === `he-2020-hl-${id}`);
  if (!c || c.kind !== 'question') throw new Error(id);
  return c;
};
describe('2020 Higher Home Economics: independently swept split booklets', () => {
  it('covers 53 printed leaves with 49 whole tasks and 627 offered marks', () => {
    expect(review.expectedSourceLeaves).toBe(53);
    expect(review.expectedSectionSourceLeaves).toEqual({ A: 16, B: 16, C: 21 });
    expect(all).toHaveLength(49);
    expect(all.map(c => c.id).sort()).toEqual(review.tasks.map(c => c.id).sort());
    expect(['sa', 'sb', 'sc'].map(s => all.filter(c => c.id.includes(`-${s}-`)).length)).toEqual([12, 16, 21]);
    expect(all.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(627);
    for (const c of all) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
      for (const v of c.answerVariants ?? []) expect(tariffReconciles({ ...c, rows: v.rows }), `${c.id}/${v.id}`).toBe(true);
    }
  });
  it('keeps all required short-answer terms, paired cells and source alternatives', () => {
    expect(get('sa-q1').rows.map(r => r.marks)).toEqual([1, 1, 1, 1, 1, 1]);
    expect(get('sa-q1').rows[0].verbatim).toContain('C6H12O6');
    expect(get('sa-q1').rows[5].group?.options).toContain('glycogen');
    expect(get('sa-q2').rows.map(r => r.permittedMarks)).toEqual([[0, 2, 3], [0, 2, 3]]);
    expect(get('sa-q2').rows[0].contextNote).toContain('ONE required reference');
    expect(get('sa-q4').rows[0].contextNote).toContain('Vitamin K, Vitamin C, Vitamin D');
    expect(get('sa-q8').rows.map(r => r.marks)).toEqual([2, 1, 2, 1]);
    for (const n of [6, 10, 11, 12]) {
      expect(get(`sa-q${n}`).rows).toHaveLength(2);
      expect(get(`sa-q${n}`).rows.map(r => r.permittedMarks)).toEqual([[0, 2, 3], [0, 2, 3]]);
    }
    expect(get('sa-q11').rows[1].contextNote).toContain('Tracker rate');
    expect(get('sa-q9').rows[0].contextNote).not.toContain('www.repak');
    expect(get('sa-q9').rows[1].contextNote).toContain('most widely recycled plastic');
  });
  it('preserves five complete original inputs and the full portion-choice task', () => {
    expect(Object.keys(review.figures)).toHaveLength(5);
    expect(new Set(all.flatMap(c => c.kind === 'question' && c.questionFigure ? [c.questionFigure.src] : [])).size).toBe(5);
    expect(get('sa-q9').questionFigure?.alt).toContain('repak.ie and clearpak.com');
    expect(get('sb-q1a').questionFigure?.alt).toContain('all ten situations and three percentage columns');
    expect(get('sb-q1a').rows[0].parts).toHaveLength(5);
    expect(get('sb-q1a').rows[0].parts?.[0].permittedMarks).toEqual([0, 1, 2, 3, 4]);
    expect(get('sb-q1a').rows[0].contextNote).toContain('Not difficult:');
    for (const c of all) if (c.kind === 'question') expect(c.questionText + c.stem).not.toMatch(/Leaving Certificate Examination|Section A and answerbook/);
  });
  it('keeps all protein headings and exact portion, food-safety and family quotas', () => {
    expect(get('sb-q1b').rows.map(r => r.marks)).toEqual([8, 8, 8]);
    expect(get('sb-q1c').rows.map(r => r.marks)).toEqual([8, 8]);
    expect(get('sb-q1c').rows[1].contextNote).toContain('culinary application');
    expect(get('sb-q1d').rows.map(r => r.marks)).toEqual([5, 5, 5, 5]);
    expect(get('sb-q1d').rows[3].contextNote).toContain('additional distinct');
    expect(get('sb-q3a').rows.map(r => r.marks)).toEqual([3, 3, 6]);
    expect(get('sb-q4b').rows.map(r => r.marks)).toEqual([4, 4, 4]);
    expect(get('sb-q5a').rows.map(r => r.marks)).toEqual([8, 8, 4]);
    expect(get('sb-q5b').rows.map(r => r.permittedMarks)).toEqual([[0, 2, 4, 6], [0, 2, 4, 6], [0, 2, 4, 6]]);
  });
  it('retains coherent cereal and two-method choices with every original table profile', () => {
    expect(get('sb-q2b').answerVariants?.map(v => v.label)).toEqual(['Flour', 'Pasta', 'Another valid cereal product']);
    for (const v of get('sb-q2b').answerVariants ?? []) expect(v.rows.map(r => r.marks)).toEqual([12, 3, 3]);
    const c = get('sb-q3b');
    expect(c.taskGroups?.map(g => g.marks)).toEqual([13, 13]);
    expect(c.rows.map(r => r.marks)).toEqual([4, 6, 3, 4, 6, 3]);
    expect(c.rows[1].parts?.[0].permittedMarks).toEqual([0, 1, 2, 3]);
    for (const label of ['Freezing:', 'Heat treatments:', 'Chemical preservation:', 'Dehydration:', 'Salting:', 'Brining']) expect(c.rows[0].contextNote).toContain(label);
    expect(c.rows[0].contextNote).toContain('Incorrect concentration of vinegar');
    expect(c.rows[5].contextNote).toContain('SAME selected method 2');
    expect(c.answerVariants).toBeUndefined();
  });
  it('keeps named-only legislation, all appliance choices and complete heating continuation', () => {
    expect(get('sb-q3c').answerVariants).toHaveLength(8);
    expect(get('sb-q3c').answerVariants?.[4].rows[1].contextNote).toContain('Health Acts');
    expect(get('sb-q3c').answerVariants?.[6].rows[1].contextNote).toContain('name only');
    expect(get('sb-q4a').rows.map(r => r.marks)).toEqual([2, 6, 6, 8, 4]);
    expect(get('sb-q4a').rows[0].contextNote).toContain('dishwasher');
    expect(get('sb-q4a').rows[3].contextNote).toContain('Food processor:');
    expect(get('sc-q1bii').answerVariants).toHaveLength(5);
    expect(get('sc-q1bii').answerVariants?.[3].rows[1].contextNote).toContain('Incremental Purchase Scheme');
    expect(get('sc-q1cii').rows.map(r => r.marks)).toEqual([1, 1, 9, 3]);
    expect(get('sc-q1cii').rows[2].contextNote).toContain('Ground source heat pump:');
    expect(get('sc-q1cii').rows[2].contextNote).toContain('compression increases the temperature');
    expect(get('sc-q1cii').rows[3].contextNote).toContain('must relate to fuel used');
  });
  it('carries companion outfit context, required education headings and two leisure profiles', () => {
    expect(get('sc-q2ai').rows.map(r => r.permittedMarks)).toEqual([[0, 1, 2, 3, 4], [0, 2, 4, 6]]);
    expect(get('sc-q2aii').stem).toContain('Sketch and describe a daywear outfit suitable for a college student');
    expect(get('sc-q2bi').rows[0].group?.options).toHaveLength(10);
    expect(get('sc-q3aii').rows.map(r => r.marks)).toEqual([5, 5, 5, 5]);
    expect(get('sc-q3biii').answerVariants).toHaveLength(5);
    expect(get('sc-q3biii').answerVariants?.[3].rows[1].contextNote).toContain('name only');
    expect(get('sc-q3ci').rows.map(r => r.marks)).toEqual([6, 6]);
    expect(get('sc-q3cii').taskGroups?.map(g => g.marks)).toEqual([9, 9]);
    expect(get('sc-q3cii').rows.map(r => r.marks)).toEqual([3, 3, 3, 3, 3, 3]);
    expect(get('sc-q3cii').rows[0].contextNote).toContain('horse riding');
    expect(get('sc-q3biii').stem).toContain('126,900');
  });
  it('preserves seventeen original Atlas identities and restores all three missing electives', () => {
    expect(get('sa-q5').topicId).toBe('home-economics-0-11');
    expect(get('sc-q1bi').topicId).toBe('home-economics-3-3');
    expect(get('sc-q1bii').topicId).toBe('home-economics-3-3');
    expect(anchorsA.q.map(q => q.n)).toEqual(Array.from({ length: 12 }, (_, i) => String(i + 1)));
    expect(anchorsBC.q.map(q => q.n)).toEqual(Array.from({ length: 8 }, (_, i) => String(i + 1)));
    expect(anchorsBC.q.find(q => q.n === '3')!.region.map(r => r.p)).toEqual([13, 14, 15]);
    expect(anchorsBC.q.find(q => q.n === '6')!.region.map(r => r.p)).toEqual([19, 20, 21, 22]);
    expect(anchorsBC.q.find(q => q.n === '7')!.region.map(r => r.p)).toEqual([23, 24]);
    expect(anchorsBC.q.find(q => q.n === '8')!.region.map(r => r.p)).toEqual([25, 26, 27]);
    for (const c of all) {
      const m = c.questionRef.match(/Section ([ABC]) (?:E\d )?Q(\d+)/)!;
      const file = m[1] === 'A' ? 'LC098ALP014EV.pdf' : 'LC098ALP039EV.pdf';
      const n = String(Number(m[2]) + (m[1] === 'C' ? 5 : 0));
      const row = runtime.questionMappings.find(q => q[0] === 'h' && q[1] === 'e' && q[2] === 2020 && q[4] === file && q[5] === n)!;
      expect(row, c.id).toBeDefined();
      expect((row[6] as number[]).map(i => runtime.topicIds[i]).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
      const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'home-economics-s-and-s' && p.year === 2020 && p.level === 'higher' && p.lang === 'ev' && p.fileid === file)!;
      expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === n)!).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
    }
  });
});
