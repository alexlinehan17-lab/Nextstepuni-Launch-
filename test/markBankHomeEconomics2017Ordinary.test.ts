import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/home-economics/ordinary';
import { groupMarks, tariffReconciles } from '../types/markBank';
import runtime from '../data/examTopics/home-economics-s-and-s-question-runtime.json';
import crosswalk from '../data/examTopics/home-economics-s-and-s-curriculum-crosswalk.json';
import anchors from '../scripts/paper-trail/answers/2017/LC098GLP000EV.pdf.json';
import review from '../scripts/markbank/authoring/home-economics/2017-ol-main-review.json';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
const all = CARDS.filter(c => c.id.startsWith('he-2017-ol-'));
const get = (id: string) => {
  const c = all.find(c => c.id === `he-2017-ol-${id}`);
  if (!c || c.kind !== 'question') throw new Error(id);
  return c;
};
describe('2017 Ordinary Home Economics: independently reviewed original sources', () => {
  it('retains all 52 priced tasks and 627 offered marks', () => {
    expect(all).toHaveLength(52);
    expect(all.map(c => c.id).sort()).toEqual(review.tasks.map(c => c.id).sort());
    expect(['sa', 'sb', 'sc'].map(s => all.filter(c => c.id.includes(`-${s}-`)).length)).toEqual([12, 19, 21]);
    expect(all.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(627);
    expect(review.sourceCensusReconciliation.expectedOriginalSectionLeaves).toEqual({ A: 12, B: 20, C: 20 });
    for (const c of all) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
      for (const v of c.answerVariants ?? []) expect(tariffReconciles({ ...c, rows: v.rows }), `${c.id}/${v.id}`).toBe(true);
    }
  });
  it('keeps all whole-six companion asks and complete unrestricted source pools', () => {
    for (let n = 1; n <= 12; n++) {
      const c = get(`sa-q${n}`);
      expect(c.tariffModel?.kind).toBe('questionTotal');
      expect(c.rows.every(r => r.marks === null && !r.permittedMarks && !r.parts)).toBe(true);
      expect(c.rows[0].contextNote).toContain('no per-answer allocation');
    }
    expect(get('sa-q1').rows.map(r => r.verbatim?.split(' — ')[1])).toEqual(['True', 'False', 'True']);
    expect(get('sa-q3').rows.map(r => r.verbatim)).toEqual(['Eggs — High Biological Value', 'Peas — Low Biological Value', 'Fish — High Biological Value']);
    expect(get('sa-q4').rows).toHaveLength(4);
    expect(get('sa-q4').questionText).toContain('Name two good dietary sources of calcium');
    expect(get('sa-q5').rows[0].contextNote).toContain('ANY THREE');
    expect(get('sa-q6').topicId).toBe('home-economics-0-3');
    expect(get('sa-q8').topicId).toBe('home-economics-0-11');
    expect(get('sa-q6').rows).toHaveLength(3);
    expect(get('sa-q6').rows[0].verbatim).toContain('tomatoes; mushrooms');
    expect(get('sa-q6').rows[0].contextNote).toContain('no one-per-column restriction');
    expect(get('sa-q7').rows.map(r => r.verbatim)).toEqual(['endosperm', 'staple', 'bran']);
    expect(get('sa-q8').rows.map(r => r.verbatim?.split(' — ')[1])).toEqual(['True', 'False', 'True']);
    expect(get('sa-q9').rows[0].contextNote).toContain('no requirement to select a guarantee');
    expect(get('sa-q10').rows).toHaveLength(4);
    expect(get('sa-q10').questionText).toContain('Name two fabrics');
    expect(get('sa-q11').rows[0].verbatim).toContain('A-G scale');
    expect(get('sa-q12').rows).toHaveLength(3);
  });
  it('retains all eleven full original question images', () => {
    expect(Object.keys(review.figures)).toHaveLength(11);
    expect(new Set(all.flatMap(c => c.kind === 'question' && c.questionFigure ? [c.questionFigure.src] : [])).size).toBe(11);
    expect(all.every(c => c.kind !== 'question' || !c.figure)).toBe(true);
    expect(get('sa-q7').questionFigure?.alt).toContain('word bank');
    expect(get('sa-q11').questionFigure?.alt).toContain('325 kWh');
    expect(get('sb-q1ai').questionFigure?.alt).toContain('full legend');
    expect(get('sb-q2ai').questionFigure?.alt).toContain('every food and drink');
    expect(get('sb-q2ai').stem).not.toContain('Bowl of porridge');
    expect(get('sc-q1ai').questionFigure?.alt).toContain('three original housing');
    expect(get('sc-q2ai').questionFigure?.alt).toContain('Both original Debs outfits');
  });
  it('preserves age quotas, distinct roman tariffs and the shared meat account', () => {
    expect(get('sb-q1ai').rows.map(r => r.marks)).toEqual([3, 4, 4, 4]);
    expect(get('sb-q1ai').rows.slice(1).map(r => r.contextNote)).toEqual(expect.arrayContaining([expect.stringContaining('15–34'), expect.stringContaining('35–54'), expect.stringContaining('55+')]));
    expect(get('sb-q1b').rows.map(r => r.marks)).toEqual([16, 8, 4]);
    expect(get('sb-q1d').rows.map(r => r.marks)).toEqual([5, 5, 10]);
    expect(get('sb-q2ai').totalMarks).toBe(8);
    expect(get('sb-q2aii').totalMarks).toBe(12);
    expect(get('sb-q2b').rows.map(r => r.marks)).toEqual([3, 6, 6]);
    expect(get('sb-q2b').topicId).toBe('home-economics-0-10');
    expect(get('sb-q2c').topicId).toBe('home-economics-0-10');
    expect(get('sb-q3a').rows.map(r => r.marks)).toEqual([5, 5, 10]);
    expect(get('sb-q3a').rows[2].contextNote).toContain('no separate 10/10 allocation');
    expect(all.some(c => c.id === 'he-2017-ol-sb-q3ai')).toBe(false);
    expect(get('sb-q3bi').totalMarks).toBe(8);
    expect(get('sb-q3bii').totalMarks).toBe(8);
    expect(get('sb-q3c').rows.map(r => r.marks)).toEqual([8, 6]);
    expect(get('sb-q4b').rows.map(r => r.marks)).toEqual([2, 12, 6]);
    expect(get('sb-q4b').rows[0].group?.options).toHaveLength(6);
    expect(get('sb-q5a').rows.map(r => r.marks)).toEqual([6, 6, 6]);
    expect(get('sb-q5c').rows.map(r => r.marks)).toEqual([5, 12]);
  });
  it('keeps required housing and textile profiles with matching source models', () => {
    const insulation = get('sc-q1aii');
    expect(insulation.taskGroups?.map(g => g.marks)).toEqual([5, 5, 5]);
    expect(insulation.rows.map(r => r.marks)).toEqual([2, 3, 2, 3, 2, 3]);
    expect(insulation.rows.filter(r => r.group).map(r => r.group?.options.length)).toEqual([4, 2, 2]);
    expect(insulation.rows[5].contextNote).toContain('low emissivity');
    expect(get('sc-q1bii').rows.map(r => r.marks)).toEqual([8, 4, 3]);
    expect(get('sc-q1bii').rows[2].contextNote).toContain('SAME furnishing 2');
    expect(get('sc-q1cii').rows[0].group?.options).toHaveLength(7);
    expect(get('sc-q1ci').topicId).toBe('home-economics-3-5');
    expect(get('sc-q2ai').rows.map(r => r.marks)).toEqual([6, 6, 6]);
    expect(get('sc-q2ai').rows[2].contextNote).toContain('pearls contrast');
    expect(get('sc-q2aii').answerVariants).toHaveLength(2);
    expect(get('sc-q2bi').taskGroups?.map(g => g.marks)).toEqual([4, 4]);
    expect(get('sc-q2bii').answerVariants).toHaveLength(2);
    expect(get('sc-q2bii').rows[1].contextNote).toContain('burning feathers or hair');
    expect(get('sc-q2ci').answerVariants).toHaveLength(7);
    expect(get('sc-q2ci').answerVariants?.find(v => v.label === 'Helen Cody')?.rows[1].contextNote).toContain('evening wear');
  });
  it('keeps both poverty asks, complete linked alternatives and unequal preschool names', () => {
    expect(get('sc-q3ai-definition').totalMarks).toBe(6);
    expect(get('sc-q3ai-types').totalMarks).toBe(12);
    expect(get('sc-q3ai-definition').questionText).toBe('Define poverty.');
    expect(get('sc-q3ai-types').rows.map(r => r.marks)).toEqual([6, 6]);
    expect(get('sc-q3ai-types').questionRef).toContain('Q3(a)(i)');
    expect(get('sc-q3aii').rows[0].group?.options).toHaveLength(10);
    expect(get('sc-q3aii').rows.map(r => r.marks)).toEqual([9, 3, 3, 3]);
    expect(get('sc-q3aiii').answerVariants).toHaveLength(6);
    expect(get('sc-q3aiii').answerVariants?.find(v => v.label === 'Lions Club')?.rows[1].contextNote).toContain('without detail models');
    expect(get('sc-q3bii').rows.map(r => r.marks)).toEqual([5, 5, 5]);
    expect(get('sc-q3bii').rows[0].contextNote).toContain('scheme misprints it (iii)');
    const preschool = get('sc-q3ci');
    expect(preschool.rows.map(r => r.marks)).toEqual([7, 4, 4]);
    expect(preschool.rows[0].group?.options).toHaveLength(6);
    expect(preschool.rows[0].group?.perOptionSteps).toEqual([4, 3]);
    expect([1, 2].map(claimMax => groupMarks({ ...preschool.rows[0].group!, claimMax }))).toEqual([4, 7]);
    expect(preschool.rows[1].parts).toHaveLength(2);
    expect(preschool.rows[2].contextNote).toContain('SAME option 2');
    expect(preschool.rows[2].contextNote).toContain('nurseries have names only');
  });
  it('preserves all twenty original Atlas identities and every canonical topic', () => {
    expect(anchors.q.map(q => q.n)).toEqual(Array.from({ length: 20 }, (_, i) => String(i + 1)));
    expect(anchors.q.find(q => q.n === '13')!.region.map(r => r.p)).toEqual([8, 9]);
    expect(anchors.q.find(q => q.n === '18')!.region.map(r => r.p)).toEqual([14, 15]);
    expect(anchors.q.find(q => q.n === '19')!.region.map(r => r.p)).toEqual([16, 17]);
    expect(anchors.q.find(q => q.n === '20')!.region.map(r => r.p)).toEqual([18, 19, 20]);
    for (const q of anchors.q) expect(q.pY[1]).toBeGreaterThan(q.pY[0]);
    const file = 'LC098GLP000EV.pdf';
    const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'home-economics-s-and-s' && p.year === 2017 && p.level === 'ordinary' && p.lang === 'ev' && p.fileid === file)!;
    for (const c of all) {
      const m = c.questionRef.match(/Section ([ABC]) (?:E\d )?Q(\d+)/)!;
      const n = String(Number(m[2]) + (m[1] === 'A' ? 0 : m[1] === 'B' ? 12 : 17));
      const row = runtime.questionMappings.find(q => q[0] === 'o' && q[1] === 'e' && q[2] === 2017 && q[4] === file && q[5] === n)!;
      expect(row, c.id).toBeDefined();
      expect((row[6] as number[]).map(i => runtime.topicIds[i]).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
      expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === n)!).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
    }
  });
});
