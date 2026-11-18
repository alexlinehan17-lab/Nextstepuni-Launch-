import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/home-economics/higher';
import { tariffReconciles } from '../types/markBank';
import runtime from '../data/examTopics/home-economics-s-and-s-question-runtime.json';
import crosswalk from '../data/examTopics/home-economics-s-and-s-curriculum-crosswalk.json';
import anchors from '../scripts/paper-trail/answers/2025/LC098ALP014EV.pdf.json';
import bcAnchors from '../scripts/paper-trail/answers/2025/LC098ALP039EV.pdf.json';
import review from '../scripts/markbank/authoring/home-economics/2025-hl-main-review.json';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
import { CARD_ID_ALIASES } from '../components/MarkBank/cardAliases';
const get = (id: string) => {
  const c = CARDS.find(c => c.id === `he-2025-hl-${id}`);
  if (!c || c.kind !== 'question') throw new Error(id);
  return c;
};
const sitting = CARDS.filter(c => c.id.startsWith('he-2025-hl-sa-'));
const b2 = CARDS.filter(c => c.id.startsWith('he-2025-hl-sb-q2'));
const all = CARDS.filter(c => c.id.startsWith('he-2025-hl-'));
describe('2025 Higher Home Economics main-sitting source review', () => {
  it('covers the independently reviewed whole sitting and every alternative at its printed tariff', () => {
    expect(all.map(c => c.id).sort()).toEqual(review.tasks.map(t => t.id).sort());
    expect(all).toHaveLength(61);
    expect(all.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(749);
    for (const c of all) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
      for (const v of c.answerVariants ?? []) expect(tariffReconciles({ ...c, rows: v.rows }), `${c.id}/${v.id}`).toBe(true);
    }
  });
  it('keeps the three fatty-acid headings and appliance study whole, with progress aliases', () => {
    const acids = get('sb-q1b');
    expect(acids.totalMarks).toBe(18);
    expect(acids.rows.map(r => r.marks)).toEqual([4, 2, 4, 2, 4, 2]);
    expect(acids.rows.filter(r => r.marks === 2).map(r => r.permittedMarks)).toEqual(Array(3).fill([0, 2]));
    expect(acids.taskGroups?.map(g => g.marks)).toEqual([6, 6, 6]);
    const appliance = get('sb-q4b-principle');
    expect(appliance.totalMarks).toBe(22);
    expect(appliance.rows.map(r => r.marks)).toEqual([1, 3, 3, 3, 6, 6]);
    for (const [old, target] of [['sb-q1b-mono', 'sb-q1b'], ['sb-q1b-poly', 'sb-q1b'], ['sb-q4b-features', 'sb-q4b-principle']]) {
      expect(CARDS.some(c => c.id === `he-2025-hl-${old}`)).toBe(false);
      expect(CARD_ID_ALIASES[`he-2025-hl-${old}`]).toBe(`he-2025-hl-${target}`);
    }
  });
  it('retains the complete chart, both outfits and the full source-specific bacteria table', () => {
    const chart = get('sb-q1a');
    for (const percentage of ['23%', '21%', '16%', '14%', '9%', '7%', '5%', '3%']) expect(chart.questionFigure?.alt).toContain(percentage);
    expect(get('sc-q2ai').questionFigure?.src).toBe(get('sc-q2aii').questionFigure?.src);
    expect(get('sc-q2ai').rows.map(r => r.marks)).toEqual([5, 5, 5]);
    expect(get('sc-q2ai').rows[0].contextNote).toContain('does not assign five marks to each heading');
    const bacteria = get('sb-q3a');
    expect(bacteria.figure?.solution).toBe(true);
    expect(bacteria.answerVariants?.map(v => v.label)).toEqual(['Salmonella', 'Listeria', 'E. coli', 'Clostridium botulinum', 'Staphylococcus aureus', 'Another valid bacterium']);
    for (const v of bacteria.answerVariants ?? []) expect(v.rows.map(r => r.marks)).toEqual([2, 2, 4, 6, 4]);
  });
  it('splits independent ventilation and meat prompts without losing their original identities', () => {
    expect([get('sc-q1aiii').totalMarks, get('sc-q1aiii-effects').totalMarks]).toEqual([9, 9]);
    expect([get('sc-q4aii').totalMarks, get('sc-q4aii-methods').totalMarks]).toEqual([6, 12]);
    expect(get('sc-q2bi').rows.map(r => r.marks)).toEqual([6, 9]);
    for (const test of ['abrasion resistance', 'insulating properties', 'stretch and elasticity', 'crease resistance', 'washability', 'colourfast', 'absorbency', 'pilling and snagging', 'tearing resistance', 'resistance to water', 'flame resistance']) expect(get('sc-q2bi').rows[1].contextNote).toContain(test);
    expect(get('sc-q3aiii').rows[0].permittedMarks).toEqual([0, 3]);
    expect(get('sc-q4cii').rows.map(r => r.marks)).toEqual([6, 3, 6]);
  });
  it('keeps all fifteen independently reviewed tasks and every answer-route tariff', () => {
    expect(sitting.map(c => c.id).sort()).toEqual(review.tasks.filter(t => t.section === 'A').map(t => t.id).sort());
    expect(sitting).toHaveLength(15);
    expect(sitting.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(84);
    for (const c of sitting) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
      for (const v of c.answerVariants ?? []) expect(tariffReconciles({ ...c, rows: v.rows }), `${c.id}/${v.id}`).toBe(true);
    }
  });
  it('preserves the independent sodium-source prompt and complete table questions', () => {
    expect(get('sa-q3').totalMarks).toBe(4);
    expect(get('sa-q3-sources').totalMarks).toBe(2);
    expect(get('sa-q3-sources').rows[0].parts?.map(p => p.permittedMarks)).toEqual([[0, 1], [0, 1]]);
    expect(get('sa-q2').questionText).toContain('Organ: Pancreas');
    expect(get('sa-q2').rows.map(r => r.permittedMarks)).toEqual(Array(3).fill([0, 1, 2]));
    for (const name of ['Night blindness', 'Rickets', 'Beri-beri']) expect(get('sa-q4').questionText).toContain(name);
    expect(get('sa-q4').rows[1].contextNote).toContain('Vitamin D');
  });
  it('keeps dependent heat-transfer and assurance answers whole with complete source models', () => {
    const heat = get('sa-q8');
    expect(heat.answerVariants?.map(v => v.label)).toEqual(['Conduction', 'Convection', 'Radiation']);
    for (const v of heat.answerVariants ?? []) expect(v.rows.map(r => r.marks)).toEqual([2, 3, 1]);
    expect(heat.answerVariants?.[0].rows[1].contextNote).toContain('from molecule to molecule');
    expect(heat.answerVariants?.[1].rows[1].contextNote).toContain('cold air or liquid falls');
    expect(heat.answerVariants?.[2].rows[1].contextNote).toContain('to the object (food) in front of it');
    expect(heat.answerVariants?.[2].rows[2].contextNote).toContain('grilling; barbequing');
    const assurance = get('sa-q10');
    expect(assurance.answerVariants).toHaveLength(6);
    for (const v of assurance.answerVariants ?? []) expect(v.rows.map(r => r.permittedMarks)).toEqual([[0, 2, 3], [0, 2, 3]]);
    expect(assurance.answerVariants?.[4].label).toBe('Convertible term assurance');
  });
  it('retains paired responses and asymmetric tariffs without a long selectable option list', () => {
    expect(get('sa-q9').taskGroups?.map(g => g.marks)).toEqual([3, 3]);
    expect(get('sa-q9').rows.map(r => r.permittedMarks)).toEqual([[0, 1, 2], [0, 1], [0, 1, 2], [0, 1]]);
    for (const name of ['humectants', 'anti-caking', 'emulsifiers', 'setting agents', 'stabilisers', 'anti-spattering', 'anti-foaming', 'bulking', 'firming', 'packaging gas']) expect(get('sa-q9').rows[0].contextNote).toContain(name);
    expect(get('sa-q11').taskGroups?.map(g => g.marks)).toEqual([3, 3]);
    expect(get('sa-q11').rows.map(r => r.permittedMarks)).toEqual([[0, 2], [0, 1], [0, 2], [0, 1]]);
    expect(get('sa-q14').rows[0].parts?.map(p => p.permittedMarks)).toEqual([[0, 2, 3], [0, 2, 3]]);
    expect(get('sa-q6').rows.map(r => r.marks)).toEqual([3, 3]);
  });
  it('retains fourteen complete original Atlas paper/scheme anchors', () => {
    expect(anchors.q.map(q => q.n)).toEqual(Array.from({ length: 14 }, (_, i) => String(i + 1)));
    expect(anchors.q.find(q => q.n === '8')!.region.map(r => r.p)).toEqual([8]);
  });
  it('corrects B2 lettering while preserving the existing cheese and calcium identities', () => {
    expect(b2).toHaveLength(4);
    expect(b2.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(50);
    expect(b2.map(c => c.id).sort()).toEqual(review.tasks.filter(t => t.section === 'B2').map(t => t.id).sort());
    for (const c of b2) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
    }
    expect(get('sb-q2a').totalMarks).toBe(6);
    expect(get('sb-q2a-risk').totalMarks).toBe(12);
    expect(get('sb-q2a-risk').questionText).toContain('osteoporosis');
    expect(get('sb-q2a-calcium').questionRef).toBe('2025 HL Section B Q2(b)');
    expect(get('sb-q2b').questionRef).toBe('2025 HL Section B Q2(c)');
    expect(get('sb-q2b').conceptId).toBe('production-of-cheese');
    expect(CARDS.some(c => c.id === 'he-2025-hl-sb-q2b-calcium')).toBe(false);
  });
  it('retains the complete cheese process, calcium factors and exact partial credit', () => {
    const cheese = get('sb-q2b');
    expect(cheese.rows.map(r => r.marks)).toEqual([12, 2, 3]);
    expect(cheese.rows[0].parts?.map(p => p.permittedMarks)).toEqual(Array(6).fill([0, 1, 2]));
    for (const text of ['protective rind', '3-12 months', 'cheese is graded', 'weighed into portions']) expect(cheese.rows[0].contextNote).toContain(text);
    const calcium = get('sb-q2a-calcium');
    expect(calcium.rows[0].parts?.map(p => p.permittedMarks)).toEqual(Array(5).fill([0, 1, 2, 3]));
    expect(calcium.rows[0].contextNote).toContain('Assist Vitamin D');
    expect(calcium.rows[0].contextNote).toContain('Inhibit tannins');
    expect(calcium.rows[0].contextNote).toContain('phosphoric acid');
    expect(bcAnchors.q.find(q => q.n === '2')!.region.map(r => r.p)).toEqual([14]);
    expect(bcAnchors.q.map(q => q.n)).toEqual(['1', '2', '3', '4', '5', '6', '7', '8', '9']);
    expect(bcAnchors.q.find(q => q.n === '9')!.region.map(r => r.p)).toEqual([27, 28, 29, 30]);
  });
  it('maps each reviewed card to its own Atlas question and canonical topic', () => {
    for (const c of all) {
      const m = c.questionRef.match(/Section ([ABC]) (?:E\d )?Q(\d+)/)!;
      const file = m[1] === 'A' ? 'LC098ALP014EV.pdf' : 'LC098ALP039EV.pdf';
      const n = String(Number(m[2]) + (m[1] === 'C' ? 5 : 0));
      const row = runtime.questionMappings.find(q => q[0] === 'h' && q[1] === 'e' && q[2] === 2025 && q[4] === file && q[5] === n)!;
      expect(row, c.id).toBeDefined();
      expect((row[6] as number[]).map(i => runtime.topicIds[i]).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
      const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'home-economics-s-and-s' && p.year === 2025 && p.level === 'higher' && p.lang === 'ev' && p.fileid === file)!;
      expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === n)!).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
    }
  });
});
