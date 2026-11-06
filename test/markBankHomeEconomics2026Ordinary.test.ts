import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/home-economics/ordinary';
import { tariffReconciles } from '../types/markBank';
import runtime from '../data/examTopics/home-economics-s-and-s-question-runtime.json';
import crosswalk from '../data/examTopics/home-economics-s-and-s-curriculum-crosswalk.json';
import anchors from '../scripts/paper-trail/answers/2026/LC098GLP014EV.pdf.json';
import bcAnchors from '../scripts/paper-trail/answers/2026/LC098GLP039EV.pdf.json';
import review from '../scripts/markbank/authoring/home-economics/2026-ol-main-review.json';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
const get = (id: string) => {
  const c = CARDS.find(c => c.id === `he-2026-ol-${id}`);
  if (!c || c.kind !== 'question') throw new Error(id);
  return c;
};
const all = CARDS.filter(c => c.id.startsWith('he-2026-ol-'));
describe('2026 Ordinary Home Economics independently reviewed main sitting', () => {
  it('covers the reviewed sitting and every alternative at its exact printed tariff', () => {
    expect(all.map(c => c.id).sort()).toEqual(review.tasks.map(t => t.id).sort());
    expect(all).toHaveLength(58);
    expect(all.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(749);
    expect(['sa', 'sb', 'sc'].map(s => all.filter(c => c.id.includes(`-${s}-`)).length)).toEqual([15, 17, 26]);
    for (const c of all) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
      for (const v of c.answerVariants ?? []) expect(tariffReconciles({ ...c, rows: v.rows }), `${c.id}/${v.id}`).toBe(true);
    }
  });
  it('keeps closed answers claimable and preserves the independent vitamin source prompt', () => {
    expect(get('sa-q1').rows.map(r => r.verbatim.split(' — ')[1])).toEqual(['True', 'True', 'False']);
    expect(get('sa-q5').rows.map(r => r.verbatim.split(' — ')[1])).toEqual(['True', 'False', 'False']);
    expect(get('sa-q6').rows.map(r => r.verbatim.split(' — ')[1])).toEqual(['Chutney making', 'Drying', 'Quick freezing']);
    expect([get('sa-q4').totalMarks, get('sa-q4-source').totalMarks]).toEqual([4, 2]);
    expect(get('sa-q4-source').rows[0].verbatim).toContain('fortified replacement milk products');
    expect(get('sa-q4-source').rows[0].permittedMarks).toEqual([0, 1, 2]);
    expect(get('sa-q11').rows[0].verbatim).toContain('sewage');
    expect(get('sa-q14').rows[1].verbatim).toContain('catches fire easily');
    expect(get('sa-q12').rows[0].contextNote).toContain('information on energy efficiency');
    expect(get('sa-q12').rows[0].contextNote).not.toContain('information14.');
    expect(anchors.q.map(q => q.n)).toEqual(Array.from({ length: 14 }, (_, i) => String(i + 1)));
  });
  it('retains all ten original figure groups with complete data and source context', () => {
    const figures = new Set(all.flatMap(c => c.kind === 'question' && c.questionFigure ? [c.questionFigure.src] : []));
    expect(figures.size).toBe(10);
    expect(Object.keys(review.figures)).toHaveLength(10);
    for (const value of ['117 kcal', '4.8 g', '9.0 g', '4.4 g', '6.0 g', '3.5 g', '0.0 g', '1.0 g', '0.3 g']) expect(get('sb-q1a').questionFigure?.alt).toContain(value);
    expect(get('sb-q1a').rows[0].contextNote).toContain('without inventing a corrected numeric value');
    for (const value of ['265 kWh', '208 L', '372 L', '41 dB']) expect(get('sa-q12').questionFigure?.alt).toContain(value);
    expect(get('sa-q12').questionFigure?.includesPrompt).toBe(true);
    expect(get('sc-q1ai').questionFigure?.src).toBe(get('sc-q1aii').questionFigure?.src);
    expect(get('sc-q1ai').questionFigure?.alt).toContain('all room labels retained');
    expect(get('sb-q3a').questionFigure?.alt).toContain('5–7 servings');
  });
  it('keeps paired responses and compulsory headings without inventing extra quotas', () => {
    expect(get('sb-q1b').rows.map(r => r.marks)).toEqual([4, 4]);
    expect(get('sb-q1b').rows[0].verbatim).toContain('green salad');
    expect(get('sb-q1c').rows.map(r => r.marks)).toEqual([12, 8, 4]);
    expect(get('sb-q2a').rows.map(r => r.marks)).toEqual([5, 5, 10]);
    expect(get('sb-q4a').rows.map(r => r.marks)).toEqual([6, 8, 6]);
    expect(get('sc-q1aii').taskGroups?.map(g => g.marks)).toEqual([10, 10]);
    expect(get('sc-q2ai').rows.map(r => r.marks)).toEqual([6, 6, 6]);
    expect(get('sc-q3ci').rows.map(r => r.marks)).toEqual([5, 5, 5]);
    expect(get('sc-q4bi').rows.map(r => r.marks)).toEqual([5, 5, 10]);
    expect(get('sc-q4ci').rows.map(r => r.marks)).toEqual([5, 5, 5]);
  });
  it('preserves the two different menu tariffs and complete original models', () => {
    expect(get('sb-q2b').taskGroups?.map(g => g.marks)).toEqual([6, 6, 6]);
    expect(get('sb-q2b').rows.map(r => r.marks)).toEqual([4, 2, 4, 2, 4, 2]);
    for (const r of get('sb-q2b').rows.filter(r => r.id.startsWith('beverage'))) expect(r.permittedMarks).toEqual([0, 2]);
    expect(get('sb-q2b').rows[2].contextNote).toContain('Quiche Lorraine');
    expect(get('sb-q2b').rows[4].contextNote).toContain('Lasagne and green salad');
    expect(get('sc-q4aii').taskGroups?.map(g => g.marks)).toEqual([6, 6, 8]);
    expect(get('sc-q4aii').rows.map(r => r.marks)).toEqual([4, 2, 4, 2, 2, 4, 2]);
    expect(get('sc-q4aii').rows[5].permittedMarks).toEqual([0, 2, 4]);
    expect(get('sc-q4aii').rows[4].contextNote).toContain('Chicken and broccoli bake with mashed potatoes');
  });
  it('retains the asymmetric crest and colour-method allocations with whole law profiles', () => {
    expect(get('sc-q2aii').rows.map(r => r.permittedMarks)).toEqual([[0, 2, 4], [0, 2, 3]]);
    expect(get('sc-q2aii').rows[0].contextNote).toContain('no developed application steps');
    expect(get('sc-q2b').rows.map(r => r.marks)).toEqual([6, 9]);
    expect(get('sc-q2b').rows[0].parts).toHaveLength(2);
    expect(get('sc-q2b').rows[1].parts).toHaveLength(3);
    expect(get('sc-q2b').rows[0].verbatim).toContain('Tie-dyeing');
    expect(get('sc-q3aiii').answerVariants).toHaveLength(6);
    for (const v of get('sc-q3aiii').answerVariants ?? []) expect(v.rows.map(r => r.marks)).toEqual([5, 10]);
  });
  it('maps every reviewed task to its source paper/scheme group and canonical topic', () => {
    expect(bcAnchors.q.map(q => q.n)).toEqual(['1', '2', '3', '4', '5', '6', '7', '8', '9']);
    expect(bcAnchors.q.find(q => q.n === '1')!.region.map(r => r.p)).toEqual([9, 10]);
    expect(bcAnchors.q.find(q => q.n === '9')!.region.map(r => r.p)).toEqual([21, 22]);
    for (const c of all) {
      const m = c.questionRef.match(/Section ([ABC]) (?:E\d )?Q(\d+)/)!;
      const file = m[1] === 'A' ? 'LC098GLP014EV.pdf' : 'LC098GLP039EV.pdf';
      const n = String(Number(m[2]) + (m[1] === 'C' ? 5 : 0));
      const row = runtime.questionMappings.find(q => q[0] === 'o' && q[1] === 'e' && q[2] === 2026 && q[4] === file && q[5] === n)!;
      expect(row, c.id).toBeDefined();
      expect((row[6] as number[]).map(i => runtime.topicIds[i]).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
      const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'home-economics-s-and-s' && p.year === 2026 && p.level === 'ordinary' && p.lang === 'ev' && p.fileid === file)!;
      expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === n)!).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
    }
  });
});
