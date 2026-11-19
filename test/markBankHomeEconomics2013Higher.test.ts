import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/home-economics/higher';
import { tariffReconciles } from '../types/markBank';
import runtime from '../data/examTopics/home-economics-s-and-s-question-runtime.json';
import crosswalk from '../data/examTopics/home-economics-s-and-s-curriculum-crosswalk.json';
import anchors from '../scripts/paper-trail/answers/2013/LC098ALP000EV.pdf.json';
import review from '../scripts/markbank/authoring/home-economics/2013-hl-main-review.json';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
const all = CARDS.filter(c => c.id.startsWith('he-2013-hl-'));
const get = (id: string) => {
  const c = all.find(c => c.id === `he-2013-hl-${id}`);
  if (!c || c.kind !== 'question') throw new Error(id);
  return c;
};
describe('2013 Higher Home Economics: independently swept original sources', () => {
  it('retains all 49 priced tasks and 627 offered marks', () => {
    expect(all).toHaveLength(49);
    expect(all.map(c => c.id).sort()).toEqual(review.tasks.map(c => c.id).sort());
    expect(['sa', 'sb', 'sc'].map(s => all.filter(c => c.id.includes(`-${s}-`)).length)).toEqual([12, 18, 19]);
    expect(all.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(627);
    for (const c of all) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
      for (const v of c.answerVariants ?? []) expect(tariffReconciles({ ...c, rows: v.rows }), `${c.id}/${v.id}`).toBe(true);
    }
  });
  it('preserves whole-six Section A tariffs, full table answers and choose-two scope', () => {
    for (let n = 1; n <= 12; n++) {
      const c = get(`sa-q${n}`);
      expect(c.tariffModel?.kind).toBe('questionTotal');
      expect(c.rows.every(r => r.marks === null && !r.permittedMarks && !r.parts)).toBe(true);
      expect(c.rows[0].contextNote).toContain('no per-answer allocation');
    }
    expect(get('sa-q1').rows[1].verbatim).toContain('blood proteins, nucleoproteins');
    expect(get('sa-q1').rows[2].verbatim).toContain('Provides essential amino acids');
    expect(get('sa-q3').rows[4].verbatim).toContain('B1/Thiamine');
    expect(get('sa-q4').rows[3].contextNote).toContain('without pairing them');
    expect(get('sa-q5').rows[1].verbatim).toContain('Benecol, Flora Pro-Active');
    expect(get('sa-q6').rows[1].contextNote).toContain('Possible effect on the body');
    expect(get('sa-q11').rows).toHaveLength(3);
    expect(get('sa-q11').rows[0].contextNote).toContain('ANY TWO');
    expect(get('sa-q12').rows[0].verbatim).toContain('Irregular: food');
  });
  it('retains complete original question tables and the printed shelf discrepancy', () => {
    expect(Object.keys(review.figures)).toHaveLength(5);
    expect(new Set(all.flatMap(c => c.kind === 'question' && c.questionFigure ? [c.questionFigure.src] : [])).size).toBe(5);
    for (const n of [1, 3, 4, 6]) expect(get(`sa-q${n}`).questionFigure?.includesPrompt).toBe(true);
    const c = get('sb-q1a');
    for (const value of ['SLAN', '40/26', '56/65', '22/20', '36/39', '14/14']) expect(c.questionFigure?.alt).toContain(value);
    expect(c.questionText).toContain('each shelf');
    expect(c.rows[0].marks).toBe(24);
    expect(c.rows[0].contextNote).toContain('FOUR shelf references');
    expect(c.rows[0].contextNote).toContain('Top shelf');
  });
  it('keeps independent sensory asks, chosen profiles and complete source gaps', () => {
    expect([get('sb-q2bi').totalMarks, get('sb-q2bii').totalMarks]).toEqual([8, 18]);
    expect(get('sb-q2bii').taskGroups?.map(g => g.marks)).toEqual([6, 6, 6]);
    expect(get('sb-q2a').rows.map(r => r.marks)).toEqual([4, 4, 4]);
    expect(get('sb-q3b').rows.map(r => r.marks)).toEqual([2, 6, 2, 4, 6]);
    for (const row of get('sb-q3b').rows) expect(row.contextNote).toContain('NO named bacterium or model answers');
    expect(get('sb-q4b').rows.map(r => r.marks)).toEqual([6, 6, 6]);
    for (const row of get('sb-q4b').rows) expect(row.contextNote).toContain('SCHOOL GRADUATION COMMITTEE');
    expect(get('sb-q5b').rows.map(r => r.marks)).toEqual([6, 6, 6, 6]);
    expect(get('sb-q5c').taskGroups?.map(g => g.marks)).toEqual([7, 7]);
    expect(get('sb-q5c').rows[0].group?.options).toHaveLength(7);
  });
  it('preserves required flooring pairs and dependent customisation/fabric guidance', () => {
    expect(get('sc-q1aii').rows.map(r => r.marks)).toEqual([6, 6, 6]);
    expect(get('sc-q1aii').rows[2].contextNote).toContain('Elderly people');
    expect(get('sc-q1bi').answerVariants?.map(v => v.label)).toEqual(['CFL/fluorescents lights', 'LED', 'Another energy-efficient lighting type']);
    expect(get('sc-q1cii').taskGroups?.map(g => g.marks)).toEqual([9, 9]);
    expect(get('sc-q1cii').rows[4].group?.options).toEqual(['carpet', 'rugs', 'carpet tiles']);
    expect(get('sc-q2aii').rows.map(r => r.marks)).toEqual([3, 4]);
    expect(get('sc-q2aii').rows[1].contextNote).toContain('No model diagram');
    expect(get('sc-q2aiii').stem).toContain('customising denim jeans');
    expect(get('sc-q2aiii').rows.every(r => r.contextNote?.includes('no model evaluation'))).toBe(true);
    expect(get('sc-q2b').answerVariants).toHaveLength(6);
    expect(get('sc-q2b').rows.map(r => r.marks)).toEqual([2, 6, 4, 3]);
    expect(get('sc-q2b').answerVariants?.find(v => v.label === 'Acetate')?.rows[3].contextNote).toContain('black, hard bead');
  });
  it('retains flexible extra quotas and the visually printed statutory tariff', () => {
    expect(get('sc-q3aii').rows.map(r => r.marks)).toEqual([5, 5, 5, 10]);
    expect(get('sc-q3bi').rows.map(r => r.marks)).toEqual([5, 5, 10]);
    expect(get('sc-q3bii').rows.map(r => r.marks)).toEqual([5, 5]);
    expect(get('sc-q3bii').rows[0].contextNote).toContain('awards 5 marks for the name');
    expect(get('sc-q3bii').rows[1].contextNote).toContain('5 marks for one matching detail');
    expect(get('sc-q3c').rows.map(r => r.marks)).toEqual([9, 9, 6, 6]);
    expect(get('sc-q3c').rows[3].contextNote).toContain('special needs');
  });
  it('preserves twenty original Atlas identities and maps every canonical topic', () => {
    expect(anchors.q.map(q => q.n)).toEqual(Array.from({ length: 20 }, (_, i) => String(i + 1)));
    expect(anchors.q.find(q => q.n === '13')!.region.map(r => r.p)).toEqual([8, 9]);
    expect(anchors.q.find(q => q.n === '18')!.region.map(r => r.p)).toEqual([14, 15, 16]);
    expect(anchors.q.find(q => q.n === '19')!.region.map(r => r.p)).toEqual([17, 18]);
    expect(anchors.q.find(q => q.n === '20')!.region.map(r => r.p)).toEqual([19, 20, 21]);
    for (const q of anchors.q) expect(q.pY[1]).toBeGreaterThan(q.pY[0]);
    const file = 'LC098ALP000EV.pdf';
    const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'home-economics-s-and-s' && p.year === 2013 && p.level === 'higher' && p.lang === 'ev' && p.fileid === file)!;
    for (const c of all) {
      const m = c.questionRef.match(/Section ([ABC]) (?:E\d )?Q(\d+)/)!;
      const n = String(Number(m[2]) + (m[1] === 'A' ? 0 : m[1] === 'B' ? 12 : 17));
      const row = runtime.questionMappings.find(q => q[0] === 'h' && q[1] === 'e' && q[2] === 2013 && q[4] === file && q[5] === n)!;
      expect(row, c.id).toBeDefined();
      expect((row[6] as number[]).map(i => runtime.topicIds[i]).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
      expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === n)!).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
    }
  });
});
