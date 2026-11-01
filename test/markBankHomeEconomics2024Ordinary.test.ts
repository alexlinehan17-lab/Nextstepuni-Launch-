import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/home-economics/ordinary';
import { CARD_ID_ALIASES } from '../components/MarkBank/cardAliases';
import { tariffReconciles } from '../types/markBank';
import runtime from '../data/examTopics/home-economics-s-and-s-question-runtime.json';
import crosswalk from '../data/examTopics/home-economics-s-and-s-curriculum-crosswalk.json';
import anchors from '../scripts/paper-trail/answers/2024/LC098GLP039EV.pdf.json';
import review from '../scripts/markbank/authoring/home-economics/2024-ol-main-review.json';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
const get = (id: string) => {
  const c = CARDS.find(c => c.id === `he-2024-ol-${id}`);
  if (!c || c.kind !== 'question') throw new Error(id);
  return c;
};
const sitting = CARDS.filter(c => c.year === 2024 && !c.id.includes('deferred'));
describe('2024 Ordinary Home Economics full source review', () => {
  it('retains every independently reviewed boundary and reconciles each answer route', () => {
    expect(sitting.map(c => c.id).sort()).toEqual(review.tasks.map(t => t.id).sort());
    expect(sitting).toHaveLength(58);
    expect(sitting.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(749);
    for (const [section, count, marks] of [['A', 16, 84], ['B', 16, 280], ['C', 26, 385]] as const) {
      const cards = sitting.filter(c => c.questionRef.includes(`Section ${section} `));
      expect(cards).toHaveLength(count);
      expect(cards.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(marks);
    }
    for (const c of sitting) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
      for (const v of c.answerVariants ?? []) expect(tariffReconciles({ ...c, rows: v.rows }), `${c.id}/${v.id}`).toBe(true);
    }
  });
  it('splits independent short prompts and keeps complete statement and matching tables', () => {
    expect(get('sa-q2').totalMarks).toBe(4);
    expect(get('sa-q2-source').totalMarks).toBe(2);
    expect(get('sa-q2-source').rows[0].permittedMarks).toEqual([0, 2]);
    expect(get('sa-q4').totalMarks).toBe(4);
    expect(get('sa-q4-methods').rows[0].parts?.map(p => p.permittedMarks)).toEqual([[0, 1], [0, 1]]);
    expect(get('sa-q1').questionText).toContain('Eggs are a low biological value food');
    expect(get('sa-q3').questionText).toContain('Energy input equals energy output');
    expect(get('sa-q9').questionText).toContain('Heat travels through the molecules');
    expect(get('sa-q7').taskGroups?.map(g => g.marks)).toEqual([3, 3]);
    expect(get('sa-q13').rows[0].parts?.map(p => p.permittedMarks)).toEqual([[0, 2, 3], [0, 2, 3]]);
  });
  it('preserves the food-choice pool and the exact required-heading quotas', () => {
    expect(get('sb-q1a').rows[0].parts).toHaveLength(5);
    for (const text of ['Emotions', 'Cooking skills', 'Time', 'Money', 'Likes and dislikes', 'Food availability', 'Work patterns']) expect(get('sb-q1a').rows[0].contextNote).toContain(text);
    expect(get('sb-q1a').questionFigure?.alt).toContain('seven factors');
    expect(get('sb-q1d').rows.map(r => r.marks)).toEqual([5, 5, 10]);
    expect(get('sb-q1d').rows[0].permittedMarks).toEqual([0, 3, 4, 5]);
    expect(get('sb-q2a').rows.map(r => r.marks)).toEqual([5, 5, 10]);
    expect(get('sb-q2a').rows[0].permittedMarks).toEqual([0, 2, 3, 4, 5]);
    expect(get('sb-q3b').taskGroups?.map(g => g.marks)).toEqual([5, 5, 5]);
    expect(get('sb-q5b').rows.map(r => r.marks)).toEqual([5, 5, 5]);
  });
  it('keeps the entire vegetarian day menu with different food and beverage partial credit', () => {
    const c = get('sb-q2b');
    expect(c.taskGroups?.map(g => [g.label, g.marks])).toEqual([['Breakfast', 6], ['Lunch', 6], ['Dinner', 6]]);
    expect(c.rows.map(r => r.marks)).toEqual([4, 2, 4, 2, 4, 2]);
    for (let i = 0; i < 6; i += 2) {
      expect(c.rows[i].parts?.map(p => p.permittedMarks)).toEqual([[0, 1, 2], [0, 1, 2]]);
      expect(c.rows[i + 1].permittedMarks).toEqual([0, 2]);
    }
    expect(c.rows[0].contextNote).toContain('Porridge with milk');
    expect(c.rows[2].contextNote).toContain('Strawberry yoghurt');
    expect(c.rows[4].contextNote).toContain('Vegetarian Lasagne');
  });
  it('keeps both sportswear images and the asymmetric design-principle tariff', () => {
    const a = get('sc-q2ai'), b = get('sc-q2aii');
    expect(a.questionFigure?.alt).toContain('Both original sportswear outfits');
    expect(b.questionFigure).toEqual(a.questionFigure);
    expect(a.rows.map(r => r.marks)).toEqual([6, 6, 6]);
    expect(b.rows.map(r => r.permittedMarks)).toEqual([[0, 2, 4], [0, 2, 3]]);
    expect(b.rows[0].contextNote).toContain('contrasting zip');
  });
  it('keeps open fibre and milk profiles whole with all models and existing progress aliases', () => {
    const fibre = get('sc-q2b-linen');
    expect(fibre.answerVariants?.map(v => v.label)).toEqual(['Linen', 'Cotton', 'Wool', 'Silk', 'Another natural fibre']);
    for (const v of fibre.answerVariants ?? []) expect(v.rows.map(r => r.marks)).toEqual([5, 5, 5]);
    for (const name of ['cotton', 'wool', 'silk']) expect(CARD_ID_ALIASES[`he-2024-ol-sc-q2b-${name}`]).toBe(fibre.id);
    const milk = get('sc-q4aii-pasteurisation');
    expect(milk.answerVariants).toHaveLength(6);
    for (const v of milk.answerVariants ?? []) expect(v.rows.map(r => r.marks)).toEqual([2, 12, 4]);
    expect(milk.answerVariants?.[2].rows[1].contextNote).toContain('at least 135°C');
    expect(milk.answerVariants?.[5].rows[0].contextNote).toContain('Spray Drying and Roller Drying');
    expect(get('sc-q4ai').questionText).toContain('(i) the nutritive value and (ii) the dietetic value');
    expect(get('sc-q4ai').rows.map(r => r.marks)).toEqual([5, 5, 10]);
  });
  it('retains the parenting and dairy guidance that continues onto the next scheme page', () => {
    expect(get('sc-q3ci').rows[1].contextNote).toContain('increased need for childcare');
    expect(get('sc-q3ci').rows[2].contextNote).toContain('shorter working week/day');
    for (const name of ['Milk', 'Cheese', 'Yoghurt', 'Cream']) expect(get('sc-q4aiii').rows[0].contextNote).toContain(name);
    expect(get('sc-q1aiii').rows[2].contextNote).toContain('hot press tank');
  });
  it('keeps complete Atlas crops, including bottom-page marks and all scheme continuations', () => {
    expect(anchors.q.map(q => q.n)).toEqual(['1', '2', '3', '4', '5', '6', '7', '8', '9']);
    for (const [n, pages] of [['1', [10, 11]], ['2', [12]], ['3', [13]], ['4', [14]], ['5', [15]], ['6', [16, 17, 18]], ['7', [19, 20]], ['8', [21, 22, 23]], ['9', [24, 25]]] as const) expect(anchors.q.find(q => q.n === n)?.region.map(r => r.p)).toEqual(pages);
    expect(anchors.q.find(q => q.n === '7')!.endY * 841.92).toBeGreaterThan(751);
    expect(anchors.q.find(q => q.n === '8')!.endY * 841.92).toBeGreaterThan(747);
  });
  it('maps each card to its own Atlas question and canonical topic', () => {
    for (const c of sitting) {
      const m = c.questionRef.match(/Section ([ABC]) (?:E\d )?Q(\d+)/)!;
      const file = m[1] === 'A' ? 'LC098GLP014EV.pdf' : 'LC098GLP039EV.pdf';
      const n = String(Number(m[2]) + (m[1] === 'C' ? 5 : 0));
      const row = runtime.questionMappings.find(q => q[0] === 'o' && q[1] === 'e' && q[2] === 2024 && q[4] === file && q[5] === n)!;
      expect(row, c.id).toBeDefined();
      expect((row[6] as number[]).map(i => runtime.topicIds[i]).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
      const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'home-economics-s-and-s' && p.year === 2024 && p.level === 'ordinary' && p.lang === 'ev' && p.fileid === file)!;
      expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === n)!).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
    }
  });
});
