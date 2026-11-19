import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/home-economics/higher';
import { tariffReconciles } from '../types/markBank';
import runtime from '../data/examTopics/home-economics-s-and-s-question-runtime.json';
import crosswalk from '../data/examTopics/home-economics-s-and-s-curriculum-crosswalk.json';
import anchors from '../scripts/paper-trail/answers/2018/LC098ALP000EV.pdf.json';
import review from '../scripts/markbank/authoring/home-economics/2018-hl-main-review.json';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
const all = CARDS.filter(c => c.id.startsWith('he-2018-hl-'));
const get = (id: string) => {
  const c = all.find(c => c.id === `he-2018-hl-${id}`);
  if (!c || c.kind !== 'question') throw new Error(id);
  return c;
};
describe('2018 Higher Home Economics: independently swept original sources', () => {
  it('retains all 49 priced tasks and 627 offered marks', () => {
    expect(all).toHaveLength(49);
    expect(all.map(c => c.id).sort()).toEqual(review.tasks.map(c => c.id).sort());
    expect(['sa', 'sb', 'sc'].map(s => all.filter(c => c.id.includes(`-${s}-`)).length)).toEqual([12, 17, 20]);
    expect(all.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(627);
    for (const c of all) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
      for (const v of c.answerVariants ?? []) expect(tariffReconciles({ ...c, rows: v.rows }), `${c.id}/${v.id}`).toBe(true);
    }
  });
  it('keeps all whole-six asks, coherent enzyme choices and the complete textile pool', () => {
    for (let n = 1; n <= 12; n++) {
      const c = get(`sa-q${n}`);
      expect(c.tariffModel?.kind).toBe('questionTotal');
      expect(c.rows.every(r => r.marks === null && !r.permittedMarks && !r.parts)).toBe(true);
      expect(c.rows[0].contextNote).toContain('no per-answer allocation');
    }
    expect(get('sa-q1').rows.map(r => r.verbatim)).toEqual(['Pancreas — Amylase — Starch — Maltose', 'Maltase — Maltose — Glucose', 'Sucrase — Sucrose — Glucose / Fructose', 'Lactase — Lactose — Glucose / Fructose']);
    expect(get('sa-q1').rows[3].contextNote).toContain('original scheme prints');
    expect(get('sa-q5').questionText).toContain('Name two products');
    expect(get('sa-q8').rows.map(r => r.verbatim)).toEqual(['Psychrophiles — -5°C to 20°C', 'Mesophiles — 20°C to 45°C', 'Thermophiles — 45°C to 75°C']);
    expect(get('sa-q9').rows).toHaveLength(9);
    expect(get('sa-q9').rows[7].contextNote).toContain('shrink resistant');
    expect(get('sa-q9').rows[8].verbatim).toBe('Proban; Provatex; etc.');
    expect(get('sa-q11').questionText).toContain('Name two saving schemes');
    expect(get('sa-q12').rows[1].verbatim).toContain('€13,000');
  });
  it('keeps all seven complete original question figures', () => {
    expect(Object.keys(review.figures)).toHaveLength(7);
    expect(new Set(all.flatMap(c => c.kind === 'question' && c.questionFigure ? [c.questionFigure.src] : [])).size).toBe(7);
    expect(get('sa-q5').questionFigure?.alt).toContain('two labelled products');
    expect(get('sa-q9').questionFigure?.alt).toContain('fire-retardant finish');
    expect(get('sb-q1a').questionFigure?.alt).toContain('all ingredients');
    expect(get('sc-q2ai').questionFigure?.alt).toContain('four outfits');
    expect(get('sb-q1a').stem).not.toContain('387');
  });
  it('preserves complete lipid/vegetarian choices and BOTH required additive accounts', () => {
    expect(get('sb-q1b').rows.map(r => r.marks)).toEqual([3, 6]);
    expect(get('sb-q1b').rows[0].group?.options).toEqual(['Carbon(C)', 'Hydrogen(H)', 'Oxygen(O)']);
    expect(get('sb-q1c').rows.map(r => r.marks)).toEqual([6, 6, 6]);
    expect(get('sb-q1c').rows[2].contextNote).toContain('arachidonic acid');
    expect(get('sb-q2a').rows.map(r => r.marks)).toEqual([9, 12, 9]);
    expect(get('sb-q2b').rows[0].group?.options).toHaveLength(8);
    expect(get('sb-q2b').rows[1].contextNote).toContain('fermented soya milk');
    expect(get('sb-q2c').answerVariants).toHaveLength(3);
    expect(get('sb-q2c').rows.map(r => r.marks)).toEqual([2, 10]);
    expect(get('sb-q3a').rows.map(r => r.marks)).toEqual([4, 16]);
    expect(get('sb-q3b').taskGroups?.map(g => g.marks)).toEqual([10, 10]);
    expect(get('sb-q3b').rows.map(r => r.marks)).toEqual([2, 2, 2, 4, 2, 2, 2, 4]);
    expect(get('sb-q3b').rows[0].contextNote).toContain('Flavour Enhancers E600-699');
    expect(get('sb-q3b').rows[0].contextNote).toContain('Monosodium Glutamate E621');
    expect(get('sb-q3b').rows[4].contextNote).toContain('BHT (E321)');
    expect(get('sb-q3b').rows[7].contextNote).toContain('reduces food waste');
  });
  it('keeps exact refrigeration, conflict and paired flooring tariffs', () => {
    expect(get('sb-q4b').rows.map(r => r.marks)).toEqual([12, 6, 4]);
    expect(get('sb-q4b').rows[0].contextNote).toContain('returns to the compressor');
    expect(get('sb-q5b').rows.map(r => r.marks)).toEqual([12, 12]);
    expect(get('sb-q5c').rows[0].contextNote).toContain('Attachment of Earnings Order');
    expect(get('sc-q1aii').rows.map(r => r.marks)).toEqual([9, 9]);
    expect(get('sc-q1aiii').rows[0].contextNote).toContain('No separate importance/regulation quota');
    expect(get('sc-q1bii').rows.map(r => r.marks)).toEqual([4, 2, 4, 2, 4, 2]);
    expect(get('sc-q1bii').taskGroups?.map(g => g.marks)).toEqual([6, 6, 6]);
    for (const text of ['Stone carpeting', 'Marble/travertine', 'Block Parquet', 'Tufted', 'linoleum']) expect(get('sc-q1bii').rows[0].contextNote).toContain(text);
    expect(get('sc-q1ci').rows[0].contextNote).toContain('sustainability of EACH');
    expect(get('sc-q1ci').rows[0].contextNote).toContain('ANY THREE sources');
    expect(get('sc-q1ci').rows[0].contextNote).toContain('no required mix of energy-source types or internal mark split');
    expect(get('sc-q1cii').rows[0].contextNote).toContain('No fixed climate/acid-rain/smog quota');
  });
  it('keeps original unsplit fibre tariffs, paired programme profiles and leisure quotas', () => {
    expect(get('sc-q2bi').rows[0].contextNote).toContain('does not allocate separate marks');
    expect(get('sc-q2bii').rows[0].contextNote).toContain('No separate example allocation');
    expect(get('sc-q2cii').answerVariants).toHaveLength(3);
    expect(get('sc-q2cii').rows.map(r => r.marks)).toEqual([2, 4]);
    expect(get('sc-q2cii').answerVariants?.find(v => v.label === 'shortening')?.rows[1].contextNote).toContain('pin fold in position');
    expect(get('sc-q3ai').rows.map(r => r.marks)).toEqual([4, 4, 4, 4, 4]);
    expect(get('sc-q3ai').rows[0].group?.options).toHaveLength(7);
    expect(get('sc-q3ai').rows[2].contextNote).toContain('work (60%)');
    expect(get('sc-q3ai').rows[2].contextNote).toContain('PLC courses are accepted by name only');
    expect(get('sc-q3ai').rows[4].contextNote).toContain('SAME programme 2');
    expect(get('sc-q3ai').rows[4].parts).toBeUndefined();
    expect(get('sc-q3ai').rows[4].permittedMarks).toEqual([0, 4]);
    expect(get('sc-q3cii').rows.map(r => r.marks)).toEqual([5, 5, 5]);
    expect(get('sc-q3cii').rows[2].contextNote).toContain('ADDITIONAL');
  });
  it('preserves twenty original Atlas identities and maps every canonical topic', () => {
    expect(anchors.q.map(q => q.n)).toEqual(Array.from({ length: 20 }, (_, i) => String(i + 1)));
    expect(anchors.q.find(q => q.n === '6')!.region.map(r => r.p)).toEqual([5]);
    expect(anchors.q.find(q => q.n === '13')!.region.map(r => r.p)).toEqual([8, 9, 10]);
    expect(anchors.q.find(q => q.n === '18')!.region.map(r => r.p)).toEqual([17, 18, 19, 20]);
    expect(anchors.q.find(q => q.n === '19')!.region.map(r => r.p)).toEqual([21, 22]);
    expect(anchors.q.find(q => q.n === '20')!.region.map(r => r.p)).toEqual([23, 24, 25]);
    for (const q of anchors.q) expect(q.pY[1]).toBeGreaterThan(q.pY[0]);
    const file = 'LC098ALP000EV.pdf';
    const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'home-economics-s-and-s' && p.year === 2018 && p.level === 'higher' && p.lang === 'ev' && p.fileid === file)!;
    for (const c of all) {
      const m = c.questionRef.match(/Section ([ABC]) (?:E\d )?Q(\d+)/)!;
      const n = String(Number(m[2]) + (m[1] === 'A' ? 0 : m[1] === 'B' ? 12 : 17));
      const row = runtime.questionMappings.find(q => q[0] === 'h' && q[1] === 'e' && q[2] === 2018 && q[4] === file && q[5] === n)!;
      expect(row, c.id).toBeDefined();
      expect((row[6] as number[]).map(i => runtime.topicIds[i]).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
      expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === n)!).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
    }
  });
});
