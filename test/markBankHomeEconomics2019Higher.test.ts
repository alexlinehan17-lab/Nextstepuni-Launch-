import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/home-economics/higher';
import { tariffReconciles } from '../types/markBank';
import runtime from '../data/examTopics/home-economics-s-and-s-question-runtime.json';
import crosswalk from '../data/examTopics/home-economics-s-and-s-curriculum-crosswalk.json';
import anchors from '../scripts/paper-trail/answers/2019/LC098ALP000EV.pdf.json';
import review from '../scripts/markbank/authoring/home-economics/2019-hl-main-review.json';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
const all = CARDS.filter(c => c.id.startsWith('he-2019-hl-'));
const get = (id: string) => {
  const c = all.find(c => c.id === `he-2019-hl-${id}`);
  if (!c || c.kind !== 'question') throw new Error(id);
  return c;
};
describe('2019 Higher Home Economics: independently swept original sources', () => {
  it('retains all 51 priced tasks and 627 offered marks', () => {
    expect(all).toHaveLength(51);
    expect(all.map(c => c.id).sort()).toEqual(review.tasks.map(c => c.id).sort());
    expect(['sa', 'sb', 'sc'].map(s => all.filter(c => c.id.includes(`-${s}-`)).length)).toEqual([12, 18, 21]);
    expect(all.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(627);
    for (const c of all) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
      for (const v of c.answerVariants ?? []) expect(tariffReconciles({ ...c, rows: v.rows }), `${c.id}/${v.id}`).toBe(true);
    }
  });
  it('retains the new explicit A ladders and all required paired answers', () => {
    for (let n = 1; n <= 12; n++) expect(get(`sa-q${n}`).tariffModel?.kind).toBe('fixed');
    expect(get('sa-q1').rows.map(r => r.permittedMarks)).toEqual([[0, 1, 2, 3], [0, 1, 2, 3]]);
    expect(get('sa-q5').rows.map(r => r.permittedMarks)).toEqual([[0, 2, 3], [0, 2, 3]]);
    expect(get('sa-q3').rows.map(r => r.verbatim)).toEqual(['Osteomalacia', 'Dry, flaky skin', 'Goitre']);
    expect(get('sa-q3').rows[0].contextNote).toContain('Calcium; phosphorous;');
    expect(get('sa-q7').rows[0].parts?.map(p => p.permittedMarks)).toEqual([[0, 2], [0, 2], [0, 2]]);
    expect(get('sa-q9').rows[0].contextNote).toContain('European Consumer Centre Ireland');
    expect(get('sa-q10').rows[1].contextNote).toContain('original scheme');
    expect(get('sa-q11').rows.map(r => r.marks)).toEqual([2, 1, 2, 1]);
    expect(get('sa-q11').rows[3].contextNote).toContain('nuclear energy');
    expect(get('sa-q12').rows[0].parts?.map(p => p.permittedMarks)).toEqual([[0, 2, 3], [0, 2, 3]]);
  });
  it('keeps both complete original inputs and source-clean prompts', () => {
    expect(Object.keys(review.figures)).toHaveLength(2);
    expect(new Set(all.flatMap(c => c.kind === 'question' && c.questionFigure ? [c.questionFigure.src] : [])).size).toBe(2);
    expect(get('sa-q3').questionFigure?.alt).toContain('Goitre');
    expect(get('sb-q1a').questionFigure?.alt).toContain('raw 5%');
    expect(get('sb-q1b').questionFigure?.alt).toContain('full Bord Bia attribution');
    for (const c of all) if (c.kind === 'question') expect(c.questionText + c.stem).not.toMatch(/previous|running|Leaving Certificate Examination/);
    expect(get('sb-q1a').stem).not.toContain('66%');
  });
  it('preserves snack pairing, category limits and all published quotas', () => {
    expect(get('sb-q1c').rows.map(r => r.marks)).toEqual([6, 12]);
    expect(get('sb-q1c').rows[1].contextNote).toContain('no fixed two-per-snack split');
    expect(get('sb-q1c').rows[1].parts).toHaveLength(4);
    expect(get('sb-q1d').rows.map(r => r.marks)).toEqual([6, 6, 6]);
    expect(get('sb-q1e').rows.map(r => r.marks)).toEqual([5, 5, 10]);
    expect(get('sb-q2a').rows[0].contextNote).toContain('MAXIMUM of TWO mineral references and TWO vitamin references');
    expect(get('sb-q2bi').totalMarks).toBe(8);
    expect(get('sb-q2bii').totalMarks).toBe(12);
    expect(get('sb-q2c').rows.map(r => r.marks)).toEqual([3, 3, 9]);
    expect(get('sb-q2c').rows[2].contextNote).toContain('protects HDL cholesterol');
    expect(get('sb-q5a').rows.map(r => r.marks)).toEqual([3, 3, 3, 3, 2]);
    expect(get('sb-q5c').rows.map(r => r.marks)).toEqual([8, 8, 8]);
  });
  it('preserves coherent bacteria models and holds the disputed one-mark case visibly', () => {
    const c = get('sb-q3b');
    expect(c.answerVariants?.map(v => v.label)).toEqual(['Salmonella', 'Listeria', 'E.coli', 'Clostridium botulinum', 'Staphylococcus Aureus', 'Clostridium Perfringens', 'Campylobacter', 'Another valid food-poisoning bacterium']);
    for (const v of c.answerVariants ?? []) {
      expect(v.rows.map(r => r.marks)).toEqual([2, 6, 2, 6, 4]);
      for (const id of ['conditions', 'source', 'foods']) {
        const row = v.rows.find(r => r.id === id)!;
        expect(row.contextNote).toContain('page 12 prints 2:1:0');
        expect(row.contextNote).toContain('page 13 table headers print 2:0');
        expect(row.contextNote).toContain('Leave a response that may merit the disputed 1 mark unassessed');
        for (const p of row.parts ?? [row]) expect(p.permittedMarks).toEqual([0, 2]);
      }
    }
    expect(c.answerVariants?.[1].rows[1].contextNote).toContain('psychrophilic 5 – 20°C');
    expect(c.answerVariants?.[3].rows[4].contextNote).toContain('oil infused with garlic');
    expect(c.answerVariants?.[6].rows[3].contextNote).toContain('accepted by name only');
  });
  it('keeps century constraints, paired wall finishes and exact design ladders', () => {
    expect(get('sc-q1ai').rows[0].contextNote).toContain('TWO centuries');
    expect(get('sc-q1ai').rows[0].contextNote).toContain('21st Century');
    expect(get('sc-q1aii').rows.map(r => r.marks)).toEqual([6, 6, 6]);
    expect(get('sc-q1bii').taskGroups?.map(g => g.marks)).toEqual([7, 7]);
    expect(get('sc-q1bii').rows.map(r => r.marks)).toEqual([1, 2, 4, 1, 2, 4]);
    for (const token of ['Water-based paint', 'Embossed wall paper', 'Flock', 'Mosaic', 'Stone']) expect(get('sc-q1bii').rows[0].contextNote).toContain(token);
    expect(get('sc-q1ci').rows.map(r => r.marks)).toEqual([6, 6]);
    expect(get('sc-q2aii').rows.map(r => r.permittedMarks)).toEqual([[0, 2, 4], [0, 2, 4, 6]]);
    expect(get('sc-q2aii').rows[1].contextNote).toContain('Accept description on labelled sketch');
    expect(get('sc-q2ci').rows[1].contextNote).toContain('no biographical/work models');
  });
  it('keeps all source continuations and evaluates both selected childcare options', () => {
    expect(get('sc-q3ai').rows.map(r => r.marks)).toEqual([4, 4, 4]);
    expect(get('sc-q3aii').rows.map(r => r.marks)).toEqual([8, 8]);
    expect(get('sc-q3aiv').rows[0].contextNote).toContain('Organisation of Working Time Act 1997');
    expect(get('sc-q3aiv').rows[0].contextNote).toContain('Zero-hour contracts');
    expect(get('sc-q3bii').taskGroups?.map(g => g.marks)).toEqual([9, 9]);
    expect(get('sc-q3bii').rows.map(r => r.marks)).toEqual([1, 8, 1, 8]);
    expect(get('sc-q3bii').rows[3].contextNote).toContain('SAME option 2');
    expect(get('sc-q3ci').rows[0].parts?.[0].permittedMarks).toEqual([0, 1, 3]);
    expect(get('sc-q3cii').rows[0].contextNote).toContain('no fixed policy/response quota');
    expect(get('sc-q3cii').rows[0].contextNote).toContain('SUSI');
  });
  it('preserves twenty original Atlas identities and maps every canonical topic', () => {
    expect(anchors.q.map(q => q.n)).toEqual(Array.from({ length: 20 }, (_, i) => String(i + 1)));
    expect(anchors.q.find(q => q.n === '6')!.region.map(r => r.p)).toEqual([5]);
    expect(anchors.q.find(q => q.n === '13')!.region.map(r => r.p)).toEqual([8, 9]);
    expect(anchors.q.find(q => q.n === '18')!.region.map(r => r.p)).toEqual([16, 17, 18]);
    expect(anchors.q.find(q => q.n === '19')!.region.map(r => r.p)).toEqual([19, 20]);
    expect(anchors.q.find(q => q.n === '20')!.region.map(r => r.p)).toEqual([21, 22]);
    for (const q of anchors.q) expect(q.pY[1]).toBeGreaterThan(q.pY[0]);
    const file = 'LC098ALP000EV.pdf';
    const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'home-economics-s-and-s' && p.year === 2019 && p.level === 'higher' && p.lang === 'ev' && p.fileid === file)!;
    for (const c of all) {
      const m = c.questionRef.match(/Section ([ABC]) (?:E\d )?Q(\d+)/)!;
      const n = String(Number(m[2]) + (m[1] === 'A' ? 0 : m[1] === 'B' ? 12 : 17));
      const row = runtime.questionMappings.find(q => q[0] === 'h' && q[1] === 'e' && q[2] === 2019 && q[4] === file && q[5] === n)!;
      expect(row, c.id).toBeDefined();
      expect((row[6] as number[]).map(i => runtime.topicIds[i]).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
      expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === n)!).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
    }
  });
});
