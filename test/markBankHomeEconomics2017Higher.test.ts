import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/home-economics/higher';
import { groupMarks, tariffReconciles } from '../types/markBank';
import runtime from '../data/examTopics/home-economics-s-and-s-question-runtime.json';
import crosswalk from '../data/examTopics/home-economics-s-and-s-curriculum-crosswalk.json';
import anchors from '../scripts/paper-trail/answers/2017/LC098ALP000EV.pdf.json';
import review from '../scripts/markbank/authoring/home-economics/2017-hl-main-review.json';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
const all = CARDS.filter(c => c.id.startsWith('he-2017-hl-'));
const get = (id: string) => {
  const c = all.find(c => c.id === `he-2017-hl-${id}`);
  if (!c || c.kind !== 'question') throw new Error(id);
  return c;
};
describe('2017 Higher Home Economics: independently swept original sources', () => {
  it('retains all 48 priced tasks and 627 offered marks', () => {
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
  it('keeps all whole-six companion asks, complete bacteria profiles and source-only alternatives', () => {
    for (let n = 1; n <= 12; n++) {
      const c = get(`sa-q${n}`);
      expect(c.tariffModel?.kind).toBe('questionTotal');
      expect(c.rows.every(r => r.marks === null && !r.permittedMarks && !r.parts)).toBe(true);
      expect(c.rows[0].contextNote).toContain('no per-answer allocation');
    }
    expect(get('sa-q1').rows[0].verbatim).toContain('tryptophan');
    expect(get('sa-q1').rows[1].verbatim).toContain('tyrosine');
    expect(get('sa-q2').questionText).toContain('Give two culinary examples');
    expect(get('sa-q6').rows.map(r => r.verbatim)).toEqual(['Salmonella', 'Listeria', 'E-coli', 'Clostridium botulinum', 'Staphylococcus aureus', 'Clostridium Welchii; Campylobacter; etc.']);
    expect(get('sa-q6').rows[3].contextNote).toContain('fish and pig intestines');
    expect(get('sa-q6').rows[5].contextNote).toContain('No model has been invented');
    expect(get('sa-q7').rows[0].contextNote).toContain('original chemical equation');
    expect(get('sa-q8').rows.map(r => r.verbatim)).toEqual(['Temperature — 132°C', 'Time — 1 to 3 seconds', 'Effect — Change in flavour; loss of vitamins B and C; all bacteria destroyed so milk keeps unopened for several months without refrigeration; etc.']);
    expect(get('sa-q9').questionText).toContain('Give two examples');
    expect(get('sa-q11').rows[0].contextNote).toContain('ANY THREE');
    expect(get('sa-q12').rows[1].verbatim).toContain('recommended retail price');
  });
  it('retains all nine original crops with complete tables and source equations', () => {
    expect(Object.keys(review.figures)).toHaveLength(9);
    expect(new Set(all.flatMap(c => c.kind === 'question' && c.questionFigure ? [c.questionFigure.src] : [])).size).toBe(7);
    expect(new Set(all.flatMap(c => c.kind === 'question' && c.figure ? [c.figure.src] : [])).size).toBe(2);
    expect(get('sa-q6').questionFigure?.alt).toContain('both blank rows');
    expect(get('sa-q7').figure?.alt).toContain('reaction arrow');
    expect(get('sb-q1a').questionFigure?.alt).toContain('full legend');
    expect(get('sb-q1b').figure?.alt).toContain('subscripts');
    expect(get('sc-q1ai').questionFigure?.alt).toContain('Bedroom 2');
    expect(get('sc-q1ai').stem).toContain('John (11 years) and Emily (4 years)');
    expect(get('sc-q3ai').questionFigure?.alt).toContain('all six percentages');
    expect(get('sc-q3ai').stem).not.toContain('15.1%');
  });
  it('preserves carbohydrate pairs, descending effect marks and production quotas', () => {
    expect(get('sb-q1b').taskGroups?.map(g => g.marks)).toEqual([5, 5, 5]);
    expect(get('sb-q1b').rows.map(r => r.marks)).toEqual([1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1]);
    expect(get('sb-q1b').rows[2].group?.options).toEqual(['Glucose', 'Fructose', 'Galactose']);
    expect(get('sb-q1c').rows[0].contextNote).toContain('Hydrolysis and Inversion');
    const group = get('sb-q1d').rows[0].group!;
    expect(group.options).toHaveLength(6);
    expect(group.perOptionSteps).toEqual([4, 3, 3]);
    expect([1, 2, 3].map(claimMax => groupMarks({ ...group, claimMax }))).toEqual([4, 7, 10]);
    expect(get('sb-q1e').rows.map(r => r.marks)).toEqual([4, 4, 12]);
    expect(get('sb-q2a').rows.map(r => r.marks)).toEqual([8, 8, 4]);
    expect(get('sb-q2b').rows.map(r => r.marks)).toEqual([14, 2, 2]);
    expect(get('sb-q2b').rows[0].contextNote).toContain('cheddaring');
    expect(get('sb-q3a').rows.map(r => r.marks)).toEqual([4, 4, 4, 4]);
  });
  it('keeps every sensory-test and mortgage model, historical constraints and all marriage headings', () => {
    expect(get('sb-q3c').answerVariants).toHaveLength(5);
    expect(get('sb-q3c').rows.map(r => r.marks)).toEqual([3, 3, 12]);
    expect(get('sb-q3c').answerVariants?.find(v => v.label === 'Duo-trio Test')?.rows[2].contextNote).toContain('starting with the reference sample');
    expect(get('sb-q4a').rows.map(r => r.marks)).toEqual([6, 6, 6]);
    expect(get('sb-q4b').rows[0].contextNote).toContain('€220,000');
    expect(get('sb-q4c').answerVariants).toHaveLength(8);
    expect(get('sb-q4c').rows.map(r => r.marks)).toEqual([4, 12]);
    expect(get('sb-q4c').answerVariants?.find(v => v.label === 'Tracker')?.rows[1].contextNote).toContain('without description models');
    expect(get('sb-q5c').rows.map(r => r.marks)).toEqual([6, 6, 6]);
    expect(get('sb-q5c').rows[2].contextNote).toContain('Judicial Separation and Family Law Reform Act 1989');
    for (const c of all.filter(c => c.id.includes('-sb-q5'))) expect(c.topicId).toBe('home-economics-2-1');
  });
  it('keeps linked elective profiles, both childcare detail sets and the unequal names tariff', () => {
    expect(get('sc-q1ai').rows).toHaveLength(1);
    expect(get('sc-q1ai').rows[0].contextNote).toContain('no separate evaluation/modification allocation');
    expect(get('sc-q1aii').rows[0].contextNote).toContain('related improvement strategy for EACH');
    expect(get('sc-q1cii').taskGroups?.map(g => g.marks)).toEqual([9, 9]);
    expect(get('sc-q1cii').rows.map(r => r.marks)).toEqual([3, 6, 3, 6]);
    expect(get('sc-q1cii').answerVariants).toHaveLength(3);
    expect(get('sc-q1cii').answerVariants?.find(v => v.label === 'Cooker hood')?.rows[3].contextNote).toContain('ductless');
    expect(get('sc-q2ai').rows.map(r => r.marks)).toEqual([5, 5, 5]);
    expect(get('sc-q2aii').rows.map(r => r.marks)).toEqual([5, 5]);
    expect(get('sc-q2b').answerVariants).toHaveLength(3);
    expect(get('sc-q2b').rows.map(r => r.marks)).toEqual([9, 3, 3]);
    expect(get('sc-q2b').answerVariants?.find(v => v.label === 'polyester cotton')?.rows[0].contextNote).toContain('spinneret');
    expect(get('sc-q2cii').rows[0].group?.options).toHaveLength(9);
    expect(get('sc-q2cii').rows[1].contextNote).toContain('names only');
    expect(get('sc-q3aii').rows.map(r => r.marks)).toEqual([4, 4, 4, 8]);
    expect(get('sc-q3aii').rows[2].contextNote).toContain('increase in taxes');
    expect(get('sc-q3aiii').rows[0].group?.options).toHaveLength(12);
    expect(get('sc-q3aiii').rows[1].contextNote).toContain('not complete two-point worked accounts');
    const childcare = get('sc-q3bii');
    expect(childcare.rows.map(r => r.marks)).toEqual([3, 6, 6]);
    expect(childcare.rows[0].group?.options).toHaveLength(6);
    expect(childcare.rows[0].group?.perOptionSteps).toEqual([2, 1]);
    expect([1, 2].map(claimMax => groupMarks({ ...childcare.rows[0].group!, claimMax }))).toEqual([2, 3]);
    expect(childcare.rows[1].parts).toHaveLength(3);
    expect(childcare.rows[2].contextNote).toContain('SAME option 2');
    expect(childcare.rows[2].contextNote).toContain('Montessori have names only');
  });
  it('preserves twenty original Atlas identities and maps every canonical topic', () => {
    expect(anchors.q.map(q => q.n)).toEqual(Array.from({ length: 20 }, (_, i) => String(i + 1)));
    expect(anchors.q.find(q => q.n === '6')!.region.map(r => r.p)).toEqual([5, 6]);
    expect(anchors.q.find(q => q.n === '13')!.region.map(r => r.p)).toEqual([8, 9, 10]);
    expect(anchors.q.find(q => q.n === '18')!.region.map(r => r.p)).toEqual([18, 19, 20]);
    expect(anchors.q.find(q => q.n === '19')!.region.map(r => r.p)).toEqual([21, 22]);
    expect(anchors.q.find(q => q.n === '20')!.region.map(r => r.p)).toEqual([23, 24, 25]);
    for (const q of anchors.q) expect(q.pY[1]).toBeGreaterThan(q.pY[0]);
    const file = 'LC098ALP000EV.pdf';
    const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'home-economics-s-and-s' && p.year === 2017 && p.level === 'higher' && p.lang === 'ev' && p.fileid === file)!;
    for (const c of all) {
      const m = c.questionRef.match(/Section ([ABC]) (?:E\d )?Q(\d+)/)!;
      const n = String(Number(m[2]) + (m[1] === 'A' ? 0 : m[1] === 'B' ? 12 : 17));
      const row = runtime.questionMappings.find(q => q[0] === 'h' && q[1] === 'e' && q[2] === 2017 && q[4] === file && q[5] === n)!;
      expect(row, c.id).toBeDefined();
      expect((row[6] as number[]).map(i => runtime.topicIds[i]).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
      expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === n)!).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
    }
  });
});
