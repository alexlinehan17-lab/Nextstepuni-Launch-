import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/home-economics/ordinary';
import { tariffReconciles } from '../types/markBank';
import runtime from '../data/examTopics/home-economics-s-and-s-question-runtime.json';
import crosswalk from '../data/examTopics/home-economics-s-and-s-curriculum-crosswalk.json';
import anchors from '../scripts/paper-trail/answers/2022/LC098GLP039EV.pdf.json';
import review from '../scripts/markbank/authoring/home-economics/2022-ol-main-review.json';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';

const get = (id: string) => {
  const card = CARDS.find(c => c.id === `he-2022-ol-${id}`);
  if (!card || card.kind !== 'question') throw new Error(`Missing question: ${id}`);
  return card;
};
const sitting = CARDS.filter(c => c.year === 2022);

describe('2022 Ordinary Home Economics full source review', () => {
  it('retains all source-reviewed tasks, their marks and every alternative tariff', () => {
    expect(sitting).toHaveLength(60);
    expect(sitting.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(749);
    expect(sitting.map(c => c.id).sort()).toEqual(review.tasks.map(c => c.id).sort());
    for (const [section, count, marks] of [['A', 16, 84], ['B', 16, 280], ['C', 28, 385]] as const) {
      const cards = sitting.filter(c => c.questionRef.includes(`Section ${section} `));
      expect(cards).toHaveLength(count);
      expect(cards.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(marks);
    }
    for (const c of sitting) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
      for (const v of c.answerVariants ?? []) expect(tariffReconciles({ ...c, rows: v.rows }), `${c.id}/${v.id}`).toBe(true);
      expect(JSON.stringify(c)).not.toContain('Held - see heldReason');
    }
  });
  it('splits independent prompts without changing their combined marks', () => {
    for (const [old, added, a, b] of [['sa-q2', 'sa-q2-source', 4, 2], ['sa-q11', 'sa-q11-car', 4, 2], ['sc-q3ai', 'sc-q3ai-terms', 4, 12]] as const) {
      expect(get(old).totalMarks).toBe(a);
      expect(get(added).totalMarks).toBe(b);
      expect(get(old).questionRef).not.toBe(get(added).questionRef);
    }
    expect(get('sa-q2').rows[0].parts?.map(p => p.permittedMarks)).toEqual([[0, 2], [0, 2]]);
    expect(get('sa-q11-car').rows[0].contextNote).toContain('PCP (personal contract plans)');
    expect(get('sc-q3ai-terms').rows.map(r => r.marks)).toEqual([6, 6]);
    expect(get('sc-q3ai-terms').rows[0].contextNote).toContain('60% of median equivalised disposable income');
  });
  it('preserves unequal tariffs and all required short-answer headings', () => {
    expect(get('sa-q5').rows[0].parts?.map(p => p.permittedMarks)).toEqual([[0, 1, 2], [0, 1, 2], [0, 1], [0, 1]]);
    expect(get('sa-q5').questionText).toContain('Grilling: (i), (ii)');
    expect(get('sa-q5').rows[0].contextNote).toContain('bruschetta');
    expect(get('sa-q9').rows.map(r => r.verbatim)).toEqual(['Food storage', 'Personal hygiene', 'Reheating food']);
    expect(get('sa-q10').rows[2].contextNote).toContain('sorbitol; mannitol');
    expect(get('sa-q14').questionFigure?.src).toContain('2022-ol-sa-q14-symbols.png');
    expect(get('sa-q14').rows.map(r => r.permittedMarks)).toEqual([[0, 2, 3], [0, 2, 3]]);
  });
  it('keeps the milk choice together and uses the original table values', () => {
    const c = get('sb-q1a');
    expect(c.answerVariants?.map(v => v.id)).toEqual(['whole', 'fat-free']);
    expect(c.questionFigure?.src).toContain('2022-ol-sb-q1a-milk.png');
    for (const v of c.answerVariants ?? []) {
      expect(v.rows.map(r => r.marks)).toEqual([4, 16]);
      expect(v.rows[1].contextNote).toContain('more carbohydrate (5.0 g versus 4.7 g)');
    }
    expect(get('sb-q1b').rows[0].contextNote).toContain('accept butter; ice-cream; etc.');
    expect(get('sb-q1c').rows.map(r => r.marks)).toEqual([12, 12, 4]);
    expect(get('sb-q1d').rows.map(r => r.marks)).toEqual([5, 5, 10]);
  });
  it('retains each complete menu column and all three required meal elements', () => {
    const c = get('sb-q2b');
    expect(c.rows).toHaveLength(3);
    for (const r of c.rows) {
      expect(r.parts?.map(p => p.verbatim)).toEqual(['First course', 'Second course', 'Beverage']);
      expect(r.parts?.map(p => p.permittedMarks)).toEqual(Array(3).fill([0, 1, 2]));
    }
    expect(c.rows[0].contextNote).toContain('Wholegrain cereal with milk');
    expect(c.rows[1].contextNote).toContain('Brown roll with chicken and cheese');
    expect(c.rows[2].contextNote).toContain('Vegetable soup with brown bread; Spaghetti Bolognese with brown pasta');
    expect(get('sb-q2a').rows.map(r => r.marks)).toEqual([5, 5, 10]);
  });
  it('keeps open profiles on one card with their dependent guidance', () => {
    const preserve = get('sb-q3a');
    expect(preserve.answerVariants?.map(v => v.id)).toEqual(['jam', 'bottling', 'drying', 'freezing', 'another']);
    for (const v of preserve.answerVariants ?? []) expect(v.rows.map(r => r.marks)).toEqual([3, 9, 12]);
    expect(preserve.answerVariants?.find(v => v.id === 'bottling')?.rows[2].contextNote).toContain('validated pressure-canning process');
    expect(get('sb-q4a').rows[0].parts).toHaveLength(4);
    expect(get('sb-q4b').rows.map(r => r.marks)).toEqual([3, 12, 9]);
    expect(get('sb-q5b').rows.map(r => r.marks)).toEqual([5, 5, 10]);
    expect(get('sb-q5c').rows[0].contextNote).toContain('Location:');
    expect(get('sb-q5a').rows[0].contextNote).toContain('ongoing consent');
  });
  it('preserves the complete visual context and required elective criteria', () => {
    expect(get('sc-q1ai').questionFigure?.src).toContain('2022-ol-sc-q1-room.png');
    expect(get('sc-q1ai').rows[0].contextNote).toContain('lacking storage for toys');
    for (const id of ['sc-q2ai', 'sc-q2aii']) expect(get(id).questionFigure?.src).toContain('2022-ol-sc-q2-outfits.png');
    expect(get('sc-q2ai').rows.map(r => r.permittedMarks)).toEqual(Array(3).fill([0, 3, 6]));
    expect(get('sc-q2aii').rows.map(r => r.permittedMarks)).toEqual([[0, 2, 3], [0, 2, 4]]);
    expect(get('sc-q1ci').rows[0].contextNote).toContain('RCBO');
    const fabric = get('sc-q2bi');
    expect(fabric.answerVariants).toHaveLength(6);
    for (const v of fabric.answerVariants ?? []) expect(v.rows.map(r => r.marks)).toEqual([6, 2, 1]);
    expect(fabric.answerVariants?.find(v => v.id === 'acrylic')?.rows[1].contextNote).toContain('sensitive to heat; etc.');
  });
  it('includes all source routes and the last continuation page of the core question', () => {
    expect(get('sc-q3aiii').answerVariants).toHaveLength(4);
    expect(get('sc-q3aiii').answerVariants?.find(v => v.id === 'focus-ireland')?.rows[1].contextNote).toContain('emergency accommodation');
    expect(get('sc-q4aiii').answerVariants?.map(v => v.id)).toEqual(['freezing', 'canning', 'smoking', 'another']);
    expect(get('sc-q4ci').rows.map(r => r.marks)).toEqual([5, 5, 5]);
    expect(get('sc-q4cii').rows[0].contextNote).toContain('apps for budgeting');
    expect(anchors.q.find(q => q.n === '9')?.region.map(r => r.p)).toEqual([23, 24, 25]);
    expect(anchors.q.find(q => q.n === '1')?.region.map(r => r.p)).toEqual([11, 12]);
  });
  it('maps every card to its own A/B/C Atlas question and canonical topic', () => {
    for (const c of sitting) {
      const m = c.questionRef.match(/Section ([ABC]) (?:E\d )?Q(\d+)/)!;
      const file = m[1] === 'A' ? 'LC098GLP014EV.pdf' : 'LC098GLP039EV.pdf';
      const n = String(Number(m[2]) + (m[1] === 'C' ? 5 : 0));
      const row = runtime.questionMappings.find(q => q[0] === 'o' && q[1] === 'e' && q[2] === 2022 && q[4] === file && q[5] === n)!;
      expect(row, c.id).toBeDefined();
      expect((row[6] as number[]).map(i => runtime.topicIds[i]).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
      const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'home-economics-s-and-s' && p.year === 2022 && p.level === 'ordinary' && p.lang === 'ev' && p.fileid === file)!;
      expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === n)!).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
    }
  });
});
