import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/home-economics/higher';
import { tariffReconciles } from '../types/markBank';
import runtime from '../data/examTopics/home-economics-s-and-s-question-runtime.json';
import crosswalk from '../data/examTopics/home-economics-s-and-s-curriculum-crosswalk.json';
import anchors from '../scripts/paper-trail/answers/2012/LC098ALP000EV.pdf.json';
import review from '../scripts/markbank/authoring/home-economics/2012-hl-main-review.json';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
const all = CARDS.filter(c => c.id.startsWith('he-2012-hl-'));
const get = (id: string) => {
  const c = all.find(c => c.id === `he-2012-hl-${id}`);
  if (!c || c.kind !== 'question') throw new Error(id);
  return c;
};
describe('2012 Higher Home Economics: independently swept original sources', () => {
  it('retains all 51 priced tasks, choices and 627 offered marks', () => {
    expect(all).toHaveLength(51);
    expect(all.map(c => c.id).sort()).toEqual(review.tasks.map(c => c.id).sort());
    expect(['sa', 'sb', 'sc'].map(s => all.filter(c => c.id.includes(`-${s}-`)).length)).toEqual([12, 17, 22]);
    expect(all.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(627);
    for (const c of all) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
      for (const v of c.answerVariants ?? []) expect(tariffReconciles({ ...c, rows: v.rows }), `${c.id}/${v.id}`).toBe(true);
    }
  });
  it('keeps all Section A source answers under whole-question six-mark tariffs', () => {
    for (let n = 1; n <= 12; n++) {
      const c = get(`sa-q${n}`);
      expect(c.tariffModel?.kind).toBe('questionTotal');
      expect(c.rows.every(r => r.marks === null && !r.permittedMarks && !r.parts)).toBe(true);
      expect(c.rows[0].contextNote).toContain('no per-answer allocation');
    }
    expect(get('sa-q3').topicId).toBe('home-economics-0-11');
    expect(get('sa-q4').topicId).toBe('home-economics-0-9');
    expect(get('sa-q7').topicId).toBe('home-economics-0-11');
    expect(get('sa-q1').questionText).toContain('List two good dietary sources');
    expect(get('sa-q12').questionText).toContain('Name two household appliances');
    expect(get('sa-q5').rows[0].contextNote).toContain('TVP');
    expect(get('sa-q6').rows[0].contextNote).toContain('Microwave cooking');
    expect(get('sa-q8').rows.map(r => r.verbatim)).toEqual(['A. sporangium', 'B. hypha /sporangiophore', 'C. mycelium']);
  });
  it('retains five complete question inputs and the original carbohydrate answer diagrams', () => {
    expect(Object.keys(review.figures)).toHaveLength(6);
    expect(new Set(all.flatMap(c => c.kind === 'question' && c.questionFigure ? [c.questionFigure.src] : [])).size).toBe(5);
    expect(get('sb-q1b').figure?.alt).toContain('disaccharide formation equation');
    expect(get('sb-q1b').questionFigure).toBeUndefined();
    for (const value of ['5–13', '14–18', '19–50', '51+', '3–5/3–4', '5–7/5–6']) expect(get('sb-q1a').questionFigure?.alt).toContain(value);
    expect(get('sc-q3ai').questionFigure?.alt).toContain('13.7%');
    expect(get('sc-q3ai').rows[0].contextNote).toContain('scheme repeats 13.6%');
    expect(get('sc-q3ai').rows[0].contextNote).toContain('14.4%');
    expect(get('sc-q3ai').rows[0].contextNote).toContain('14.2%');
  });
  it('preserves food-group quotas and the full carbohydrate account', () => {
    expect(get('sb-q1a').rows.map(r => r.marks)).toEqual([2, 4, 2, 4, 2, 4, 2, 4]);
    expect(get('sb-q1a').taskGroups?.map(g => g.marks)).toEqual([6, 6, 6, 6]);
    expect(get('sb-q1a').rows[0].contextNote).toContain('Two references to EACH');
    expect(get('sb-q1b').rows.map(r => r.marks)).toEqual([8, 8, 8]);
    expect(get('sb-q1b').rows[0].permittedMarks).toEqual([0, 8]);
    expect(get('sb-q1b').rows[1].contextNote).toContain('glucose + galactose = lactose');
    expect(get('sb-q2b').rows[0].contextNote).toContain('EITHER fruit OR vegetables');
    expect(get('sb-q2c').rows.map(r => r.marks)).toEqual([6, 6, 6]);
    expect(get('sb-q3a').rows.map(r => r.marks)).toEqual([8, 8, 8]);
  });
  it('keeps chosen profiles complete and independently prices the family asks', () => {
    expect(get('sb-q3b').answerVariants).toHaveLength(4);
    expect(get('sb-q3b').answerVariants?.find(v => v.id === 'source-2')?.rows[1].contextNote).toContain('vacuum on cooling');
    expect(get('sb-q4b').answerVariants).toHaveLength(7);
    expect(get('sb-q4b').answerVariants?.find(v => v.id === 'source-6')?.rows[1].contextNote).toContain('does not facilitate a fixed rate');
    expect(get('sb-q4c').answerVariants).toHaveLength(7);
    expect(get('sb-q4c').answerVariants?.find(v => v.id === 'source-6')?.rows[1].contextNote).toContain('at least 5 apartments');
    expect([get('sb-q5b-child').totalMarks, get('sb-q5b-parent').totalMarks]).toEqual([12, 12]);
    expect(get('sb-q5b-parent').questionText).toContain('a parent has special needs');
  });
  it('preserves elective quotas, independent techniques and explicit missing model guidance', () => {
    expect(get('sc-q1aii').rows.map(r => r.marks)).toEqual([4, 4, 12, 4]);
    expect(get('sc-q1bii').answerVariants).toHaveLength(4);
    expect(get('sc-q1bii').answerVariants?.find(v => v.id === 'source-3')?.rows[1].contextNote).toContain('carbon exhaust filter');
    expect(get('sc-q1ci').rows.map(r => r.marks)).toEqual([3, 3, 3, 9]);
    expect(get('sc-q1ci').rows[3].contextNote).toContain('no per-heading quota');
    expect(get('sc-q1cii').taskGroups?.map(g => g.marks)).toEqual([6, 6]);
    expect(get('sc-q2aii').rows.map(r => r.marks)).toEqual([6, 4]);
    for (const key of ['construction', 'colour', 'design']) {
      const c = get(`sc-q2c-${key}`);
      expect(c.totalMarks).toBe(5);
      expect(c.rows[0].contextNote).toContain('supplies no model descriptions');
    }
    expect(get('sc-q3aii').rows.map(r => r.marks)).toEqual([5, 5, 5, 5]);
    expect(get('sc-q3aii').rows[2].contextNote).toContain('cheaper imported goods');
    expect([get('sc-q3bi-definition').totalMarks, get('sc-q3bi-value').totalMarks]).toEqual([6, 12]);
    expect(get('sc-q3cii').taskGroups?.map(g => g.marks)).toEqual([9, 9]);
    expect(get('sc-q3cii').rows[1].contextNote).toContain('provides no model evaluations');
  });
  it('preserves all twenty physical IDs and joins every task to canonical Atlas topics', () => {
    expect(anchors.q.map(q => q.n)).toEqual(Array.from({ length: 20 }, (_, i) => String(i + 1)));
    expect(anchors.schemeFileid).toBe('LC098ALP000EV.pdf');
    expect(anchors.q.find(q => q.n === '13')!.region.map(r => r.p)).toEqual([7, 8]);
    expect(anchors.q.find(q => q.n === '18')!.region.map(r => r.p)).toEqual([14, 15, 16]);
    expect(anchors.q.find(q => q.n === '19')!.region.map(r => r.p)).toEqual([17]);
    expect(anchors.q.find(q => q.n === '19')!.region[0].r[3]).toBeGreaterThan(0.89);
    expect(anchors.q.find(q => q.n === '20')!.region.map(r => r.p)).toEqual([18, 19]);
    const file = 'LC098ALP000EV.pdf';
    const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'home-economics-s-and-s' && p.year === 2012 && p.level === 'higher' && p.lang === 'ev' && p.fileid === file)!;
    for (const c of all) {
      const m = c.questionRef.match(/Section ([ABC]) (?:E\d )?Q(\d+)/)!;
      const n = String(Number(m[2]) + (m[1] === 'A' ? 0 : m[1] === 'B' ? 12 : 17));
      const row = runtime.questionMappings.find(q => q[0] === 'h' && q[1] === 'e' && q[2] === 2012 && q[4] === file && q[5] === n)!;
      expect(row, c.id).toBeDefined();
      expect((row[6] as number[]).map(i => runtime.topicIds[i]).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
      expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === n)!).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
    }
  });
});
