import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/home-economics/ordinary';
import { tariffReconciles } from '../types/markBank';
import runtime from '../data/examTopics/home-economics-s-and-s-question-runtime.json';
import crosswalk from '../data/examTopics/home-economics-s-and-s-curriculum-crosswalk.json';
import anchors from '../scripts/paper-trail/answers/2012/LC098GLP000EV.pdf.json';
import review from '../scripts/markbank/authoring/home-economics/2012-ol-main-review.json';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
const all = CARDS.filter(c => c.id.startsWith('he-2012-ol-'));
const get = (id: string) => {
  const c = all.find(c => c.id === `he-2012-ol-${id}`);
  if (!c || c.kind !== 'question') throw new Error(id);
  return c;
};
describe('2012 Ordinary Home Economics: independently swept original sources', () => {
  it('retains all 53 priced tasks and 627 offered marks', () => {
    expect(all).toHaveLength(53);
    expect(all.map(c => c.id).sort()).toEqual(review.tasks.map(c => c.id).sort());
    expect(['sa', 'sb', 'sc'].map(s => all.filter(c => c.id.includes(`-${s}-`)).length)).toEqual([12, 20, 21]);
    expect(all.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(627);
    for (const c of all) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
      for (const v of c.answerVariants ?? []) expect(tariffReconciles({ ...c, rows: v.rows }), `${c.id}/${v.id}`).toBe(true);
    }
  });
  it('retains Section A whole tariffs, companion asks and complete source answer pools', () => {
    for (let n = 1; n <= 12; n++) {
      const c = get(`sa-q${n}`);
      expect(c.tariffModel?.kind).toBe('questionTotal');
      expect(c.rows.every(r => r.marks === null && !r.permittedMarks && !r.parts)).toBe(true);
      expect(c.rows[0].contextNote).toContain('no per-answer allocation');
    }
    expect(get('sa-q3').rows[0].verbatim).toContain('transports nutrients, oxygen');
    expect(get('sa-q4').questionText).toContain('List two sources of haem-iron');
    expect(get('sa-q6').rows).toHaveLength(6);
    expect(get('sa-q6').rows[5].verbatim).toContain('bananas, kiwis, rhubarb');
    expect(get('sa-q8').questionText).toContain('Name two major Irish food exports');
    expect(get('sa-q10').rows.map(r => r.verbatim)).toEqual(['Durable', 'Colourfast', 'Windproof', 'Absorbent']);
    expect(get('sa-q10').rows[0].contextNote).toContain('Choose THREE');
    expect(get('sa-q11').rows[0].contextNote).toContain('includes nuclear in the renewable cell');
    expect(get('sa-q11').questionText).toContain('State two different methods');
    expect(get('sa-q12').questionText).toContain('Name one statutory body');
  });
  it('preserves nine complete original question figures and their printed inputs', () => {
    expect(Object.keys(review.figures)).toHaveLength(9);
    expect(new Set(all.flatMap(c => c.kind === 'question' && c.questionFigure ? [c.questionFigure.src] : [])).size).toBe(9);
    expect(get('sa-q2').questionFigure?.alt).toContain('insoluble, gelatinisation, hygroscopic');
    expect(get('sa-q10').questionFigure?.alt).toContain('Irritant, Windproof, Flammable');
    for (const value of ['41%', '36%', '9%', '7%', '2%', '5%']) expect(get('sb-q1a').questionFigure?.alt).toContain(value);
    expect(get('sc-q1ai').questionFigure?.alt).toContain('fluoridation');
    expect(get('sc-q1ai').questionFigure?.alt).toContain('high storage reservoir');
    expect(get('sc-q2ai').questionFigure?.alt).toContain('trousers, skirt and shoes');
  });
  it('preserves all four independently priced companion pairs', () => {
    for (const [left, right, marks] of [
      ['sb-q2a-sources', 'sb-q2a-reasons', [12, 8]],
      ['sb-q2c-definition', 'sb-q2c-consumption', [5, 10]],
      ['sb-q4c-reasons', 'sb-q4c-schemes', [12, 6]],
      ['sc-q1bii-difference', 'sc-q1bii-procedure', [8, 16]],
    ] as const) expect([get(left).totalMarks, get(right).totalMarks]).toEqual(marks);
    expect(get('sb-q2c-consumption').questionText).toContain('fortified food products');
    expect(get('sc-q1bii-difference').rows.map(r => r.marks)).toEqual([4, 4]);
    expect(get('sc-q1bii-procedure').rows[0].contextNote).toContain('An Bórd Pleanála');
  });
  it('keeps chart and heading quotas, flexible third method and complete menu guidance', () => {
    expect(get('sb-q1a').rows.map(r => r.marks)).toEqual([4, 4, 4, 4, 4, 4]);
    expect(get('sb-q1b').rows.map(r => r.marks)).toEqual([8, 8, 4, 4]);
    expect(get('sb-q1c').rows.map(r => r.marks)).toEqual([4, 4, 4]);
    expect(get('sb-q1c').rows[2].contextNote).toContain('EITHER heading');
    expect(get('sb-q1d').rows).toHaveLength(5);
    expect(get('sb-q1d').rows[4].contextNote).toContain('home produce');
    expect(get('sb-q3b').rows.map(r => r.marks)).toEqual([6, 6, 6]);
    expect(get('sb-q3b').rows[1].contextNote).toContain('Cheese Salad Filled Brown Roll');
    expect(get('sb-q5aii').stem).toContain('four functions of the modern family');
  });
  it('keeps elective profiles, required headings and linked education programmes', () => {
    expect(get('sc-q1ai').rows[0].parts).toHaveLength(4);
    expect(get('sc-q1ai').rows[0].marks).toBe(20);
    expect(get('sc-q1ai').rows[0].contextNote).toContain('Fluoridation');
    expect(get('sc-q1ai').rows[0].contextNote).toContain('Softening');
    expect(get('sc-q1ai').rows[0].contextNote).toContain('requires an explanation');
    expect(get('sc-q1aii').rows.map(r => r.marks)).toEqual([5, 5, 5, 5]);
    expect(get('sc-q2ai').rows.map(r => r.marks)).toEqual([4, 4, 4]);
    expect(get('sc-q2aii').answerVariants).toHaveLength(3);
    expect(get('sc-q2aiii').answerVariants).toHaveLength(6);
    expect(get('sc-q2aiii').rows.map(r => r.marks)).toEqual([3, 4]);
    expect(get('sc-q2aiii').answerVariants?.find(v => v.label === 'embroidery')?.rows[1].contextNote).toContain('supplies no model description');
    expect(get('sc-q2bi').topicId).toBe('home-economics-3-8');
    expect(get('sc-q3ai').rows.map(r => r.marks)).toEqual([10, 10, 10, 10]);
    expect(get('sc-q3aii').rows.map(r => r.marks)).toEqual([4, 6]);
    expect(get('sc-q3ci').taskGroups?.map(g => g.marks)).toEqual([9, 9]);
    expect(get('sc-q3ci').rows[1].contextNote).toContain('without model details');
    expect(get('sc-q3cii').rows.map(r => r.marks)).toEqual([6, 6]);
    expect(get('sc-q3cii').stem).toContain('Name and give details of two education programmes');
    expect(get('sc-q3cii').topicId).toBe('home-economics-3-10');
  });
  it('preserves all twenty physical IDs, continuation pages and canonical Atlas mappings', () => {
    expect(anchors.q.map(q => q.n)).toEqual(Array.from({ length: 20 }, (_, i) => String(i + 1)));
    expect(anchors.schemeFileid).toBe('LC098GLP000EV.pdf');
    expect(anchors.q.find(q => q.n === '13')!.region.map(r => r.p)).toEqual([7, 8, 9]);
    expect(anchors.q.find(q => q.n === '14')!.region.map(r => r.p)).toEqual([9]);
    expect(anchors.q.find(q => q.n === '18')!.region.map(r => r.p)).toEqual([13, 14]);
    expect(anchors.q.find(q => q.n === '19')!.region.map(r => r.p)).toEqual([15, 16]);
    expect(anchors.q.find(q => q.n === '20')!.region.map(r => r.p)).toEqual([17, 18]);
    const file = 'LC098GLP000EV.pdf';
    const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'home-economics-s-and-s' && p.year === 2012 && p.level === 'ordinary' && p.lang === 'ev' && p.fileid === file)!;
    for (const c of all) {
      const m = c.questionRef.match(/Section ([ABC]) (?:E\d )?Q(\d+)/)!;
      const n = String(Number(m[2]) + (m[1] === 'A' ? 0 : m[1] === 'B' ? 12 : 17));
      const row = runtime.questionMappings.find(q => q[0] === 'o' && q[1] === 'e' && q[2] === 2012 && q[4] === file && q[5] === n)!;
      expect(row, c.id).toBeDefined();
      expect((row[6] as number[]).map(i => runtime.topicIds[i]).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
      expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === n)!).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
    }
  });
});
