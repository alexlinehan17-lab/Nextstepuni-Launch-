import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/home-economics/higher';
import { tariffReconciles } from '../types/markBank';
import runtime from '../data/examTopics/home-economics-s-and-s-question-runtime.json';
import crosswalk from '../data/examTopics/home-economics-s-and-s-curriculum-crosswalk.json';
import anchors from '../scripts/paper-trail/answers/2011/LC098ALP000EV.pdf.json';
import review from '../scripts/markbank/authoring/home-economics/2011-hl-main-review.json';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
const all = CARDS.filter(c => c.id.startsWith('he-2011-hl-'));
const get = (id: string) => {
  const c = all.find(c => c.id === `he-2011-hl-${id}`);
  if (!c || c.kind !== 'question') throw new Error(id);
  return c;
};
describe('2011 Higher Home Economics: independently swept original sources', () => {
  it('retains all 48 priced tasks, choices and 627 offered marks', () => {
    expect(all).toHaveLength(48);
    expect(all.map(c => c.id).sort()).toEqual(review.tasks.map(c => c.id).sort());
    expect(['sa', 'sb', 'sc'].map(s => all.filter(c => c.id.includes(`-${s}-`)).length)).toEqual([12, 17, 19]);
    expect(all.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(627);
    for (const c of all) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
      for (const v of c.answerVariants ?? []) expect(tariffReconciles({ ...c, rows: v.rows }), `${c.id}/${v.id}`).toBe(true);
    }
  });
  it('uses whole-question tariffs for A with visible complete guidance', () => {
    for (let n = 1; n <= 12; n++) {
      const c = get(`sa-q${n}`);
      expect(c.tariffModel?.kind).toBe('questionTotal');
      expect(c.rows.every(r => r.marks === null && !r.permittedMarks && !r.parts)).toBe(true);
      expect(c.rows[0].contextNote).toContain('no per-answer allocation');
    }
    expect(get('sa-q1').rows).toHaveLength(9);
    expect(get('sa-q6').rows[0].contextNote).toContain('Vitamins A, C, E BHA BHT');
    expect(get('sa-q6').rows[1].contextNote).toContain('prevents oxidative rancidity');
    expect(get('sa-q9').questionText).toContain('Give an example');
    expect(get('sa-q10').questionText).toContain('State two conditions');
    expect(get('sa-q12').rows.map(r => r.verbatim)).toEqual(['Goods comply with European standards of safety.', 'Appliance has double insulation.']);
  });
  it('retains five complete original figures and all chart products', () => {
    expect(Object.keys(review.figures)).toHaveLength(5);
    expect(new Set(all.flatMap(c => c.kind === 'question' && c.questionFigure ? [c.questionFigure.src] : [])).size).toBe(5);
    for (const value of ['39%', '26%', '18%', '17%']) expect(get('sb-q1a').questionFigure?.alt).toContain(value);
    expect(get('sb-q1a').rows.map(r => r.marks)).toEqual([2, 3, 2, 3, 2, 3, 2, 3]);
    expect(get('sb-q1a').taskGroups?.map(g => [g.label, g.marks])).toEqual([['Milk', 5], ['Yogurts', 5], ['Cheese', 5], ['Cream and fats', 5]]);
    expect(get('sa-q12').questionFigure?.alt).toContain('double-square');
  });
  it('preserves complete profiles and source-specific milk process routes', () => {
    expect(get('sb-q1b').rows.map(r => r.marks)).toEqual([8, 8, 12]);
    expect(get('sb-q1b').rows[2].group?.options).toHaveLength(5);
    expect(get('sb-q1b').rows[2].group?.options[0]).toMatch(/^Denaturation/);
    const milk = get('sb-q1c');
    expect(milk.answerVariants).toHaveLength(7);
    expect(milk.rows.map(r => r.marks)).toEqual([2, 6, 4]);
    expect(milk.answerVariants?.find(v => v.id === 'uht')?.rows[1].contextNote).toContain('132ºC');
    expect(milk.answerVariants?.find(v => v.id === 'dried')?.rows[2].contextNote).toContain('Some amino acids destroyed.');
    expect(get('sb-q2a').rows.map(r => r.marks)).toEqual([12, 6, 12]);
    expect(get('sb-q2b').rows.map(r => r.marks)).toEqual([3, 3, 3, 3]);
    expect(get('sb-q3b').rows.map(r => r.marks)).toEqual([2, 10, 4, 4]);
  });
  it('retains independent family asks and required social factors', () => {
    expect([get('sb-q5a-definition').totalMarks, get('sb-q5a-universality').totalMarks]).toEqual([5, 5]);
    expect(get('sb-q5a-universality').questionText).toContain('universality');
    expect(get('sb-q5a-universality').stem).toContain('Define the term family');
    expect(get('sb-q4b').rows.map(r => r.verbatim.split(' –')[0])).toEqual(['Age', 'Gender', 'Social class', 'Cultural factors']);
    expect(get('sb-q5c').topicId).toBe('home-economics-2-3');
  });
  it('keeps source omissions explicit and preserves the bottom of taller scheme pages', () => {
    expect(get('sc-q2ai').rows.map(r => r.permittedMarks)).toEqual([[0, 4], [0, 6]]);
    expect(get('sc-q2aii').rows.map(r => r.marks)).toEqual([9, 6]);
    expect(get('sc-q2aii').stem).toContain('Sketch and describe');
    expect(get('sc-q2b').rows.map(r => r.marks)).toEqual([6, 4, 5]);
    expect(get('sc-q2b').rows.every(r => r.contextNote?.includes('supplies no model answer'))).toBe(true);
    expect(get('sc-q2cii').rows[2].verbatim).toContain('no expense spared');
    expect(get('sc-q3cii').rows[0].group?.options?.join(' ')).toContain('every 4.5 hrs');
    const energy = get('sc-q1bi');
    expect(energy.answerVariants).toHaveLength(6);
    expect(energy.rows.map(r => r.marks)).toEqual([3, 8, 4]);
    expect(energy.rows[1].contextNote).toContain('visibly clipped');
    expect(energy.answerVariants?.find(v => v.id === 'source-4')?.rows[1].contextNote).toContain('CO2 than');
    expect(energy.answerVariants?.find(v => v.id === 'source-5')?.rows[2].contextNote).toContain('danger of depletion');
  });
  it('preserves all twenty physical IDs and joins every task to canonical Atlas topics', () => {
    expect(anchors.q.map(q => q.n)).toEqual(Array.from({ length: 20 }, (_, i) => String(i + 1)));
    expect(anchors.schemeFileid).toBe('LC098ALP000EV.PDF');
    expect(anchors.q.find(q => q.n === '13')!.region.map(r => r.p)).toEqual([7, 8, 9]);
    expect(anchors.q.find(q => q.n === '18')!.region.map(r => r.p)).toEqual([14, 15, 16]);
    expect(anchors.q.find(q => q.n === '19')!.region.map(r => r.p)).toEqual([17]);
    expect(anchors.q.find(q => q.n === '19')!.region[0].r[3]).toBeGreaterThan(0.89);
    expect(anchors.q.find(q => q.n === '20')!.region.map(r => r.p)).toEqual([18, 19]);
    const file = 'LC098ALP000EV.pdf';
    const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'home-economics-s-and-s' && p.year === 2011 && p.level === 'higher' && p.lang === 'ev' && p.fileid === file)!;
    for (const c of all) {
      const m = c.questionRef.match(/Section ([ABC]) (?:E\d )?Q(\d+)/)!;
      const n = String(Number(m[2]) + (m[1] === 'A' ? 0 : m[1] === 'B' ? 12 : 17));
      const row = runtime.questionMappings.find(q => q[0] === 'h' && q[1] === 'e' && q[2] === 2011 && q[4] === file && q[5] === n)!;
      expect(row, c.id).toBeDefined();
      expect((row[6] as number[]).map(i => runtime.topicIds[i]).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
      expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === n)!).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
    }
  });
});
