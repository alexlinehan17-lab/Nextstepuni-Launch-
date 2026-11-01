import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/home-economics/ordinary';
import { tariffReconciles } from '../types/markBank';
import runtime from '../data/examTopics/home-economics-s-and-s-question-runtime.json';
import crosswalk from '../data/examTopics/home-economics-s-and-s-curriculum-crosswalk.json';
import anchors from '../scripts/paper-trail/answers/2021/LC098GLP039EV.pdf.json';
import review from '../scripts/markbank/authoring/home-economics/2021-ol-main-review.json';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
const get = (id: string) => {
  const c = CARDS.find(c => c.id === `he-2021-ol-${id}`);
  if (!c || c.kind !== 'question') throw new Error(id);
  return c;
};
const sitting = CARDS.filter(c => c.year === 2021 && !c.id.includes('deferred'));
describe('2021 Ordinary Home Economics full source review', () => {
  it('covers the independent paper review with every tariff and open route intact', () => {
    expect(sitting).toHaveLength(61);
    expect(sitting.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(749);
    expect(sitting.map(c => c.id).sort()).toEqual(review.tasks.map(c => c.id).sort());
    for (const [section, count, marks] of [['A', 17, 84], ['B', 17, 280], ['C', 27, 385]] as const) {
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
  it('retains complete short prompts and separately priced tasks', () => {
    for (const [id, suffix, first, second] of [['sa-q3', 'methods', 2, 4], ['sa-q10', 'payment', 4, 2], ['sa-q11', 'disposal', 4, 2], ['sb-q3b', 'storage', 9, 9]] as const) {
      expect(get(id).totalMarks).toBe(first);
      expect(get(`${id}-${suffix}`).totalMarks).toBe(second);
      expect(get(id).questionRef).not.toBe(get(`${id}-${suffix}`).questionRef);
    }
    expect(get('sa-q2').questionText).toContain('calcium    osteoporosis    iron');
    expect(get('sa-q2').questionText?.match(/_{5,}/g)).toHaveLength(3);
    expect(get('sa-q7').questionText).toContain('Plain white flour (cream)');
    expect(get('sa-q8').questionText).toContain('A lacto-vegetarian does not eat dairy produce');
    expect(get('sa-q9').questionText).toContain('Preserves food by removing moisture');
    expect(get('sa-q13').questionText).toContain('Discretionary expenditure');
    expect(get('sa-q14').rows.map(r => r.permittedMarks)).toEqual([[0, 1, 2, 3], [0, 1, 2, 3]]);
  });
  it('restores the three missing B tasks with original choice, menu slots and heading quotas', () => {
    const yoghurt = get('sb-q1a');
    expect(yoghurt.answerVariants?.map(v => v.label)).toEqual(['Full fat natural yoghurt', 'Low fat natural yoghurt', 'Fat free natural yoghurt']);
    expect(yoghurt.questionFigure?.alt).toContain('sugars: 3.2 / 6.8 / 7.3 g');
    for (const v of yoghurt.answerVariants ?? []) {
      expect(v.rows.map(r => r.marks)).toEqual([4, 16]);
      expect(v.rows[1].parts).toHaveLength(4);
      expect(v.rows[1].parts?.[0].permittedMarks).toEqual([0, 2, 4]);
    }
    const menu = get('sb-q2b');
    expect(menu.rows.map(r => r.marks)).toEqual([6, 6, 6]);
    for (const r of menu.rows) expect(r.parts?.map(p => p.verbatim)).toEqual(['First course', 'Second course', 'Beverage']);
    expect(menu.rows[0].contextNote).toContain('Pancakes with blueberry sauce');
    expect(menu.rows[2].contextNote).toContain('Chicken and broccoli bake with mashed potato');
    expect(get('sb-q3a').rows.map(r => r.marks)).toEqual([8, 8, 4]);
    expect(get('sb-q2a').rows[0].contextNote).toContain('avoid raw/undercooked eggs');
    expect(get('sb-q1c').rows[1].contextNote).toContain('cell membranes');
  });
  it('keeps required headings and dependent pairs within their whole responses', () => {
    expect(get('sb-q1c').rows.map(r => r.marks)).toEqual([8, 8, 12]);
    expect(get('sb-q5a').rows.map(r => r.marks)).toEqual([6, 6, 6]);
    expect(get('sc-q1aii').rows.map(r => r.permittedMarks)).toEqual(Array(3).fill([[0, 2], [0, 3]]).flat());
    expect(get('sc-q1aii').taskGroups?.map(g => g.marks)).toEqual([5, 5, 5]);
    expect(get('sc-q1bi').rows.map(r => r.marks)).toEqual([4, 4, 4]);
    expect(get('sc-q2ai').rows.map(r => r.marks)).toEqual([6, 6, 6]);
    expect(get('sc-q2aii').rows.map(r => r.permittedMarks)).toEqual([[0, 3], [0, 2, 4]]);
    expect(get('sc-q3cii').rows.map(r => r.marks)).toEqual([4, 8]);
    expect(get('sc-q4ai').rows.map(r => r.marks)).toEqual([8, 8, 4]);
    expect(get('sc-q4aii').rows.map(r => r.marks)).toEqual([9, 9]);
    expect(get('sc-q4bii').rows.map(r => r.marks)).toEqual([5, 5, 5]);
  });
  it('retains original figures, all fabric routes and multi-page guidance', () => {
    expect(get('sa-q14').questionFigure?.alt).toContain('iron with two dots');
    for (const id of ['sc-q1ai', 'sc-q1aii', 'sc-q1aiii']) expect(get(id).questionFigure?.alt).toContain('roof 25%');
    for (const id of ['sc-q2ai', 'sc-q2aii']) expect(get(id).questionFigure?.alt).toContain('red lace dress');
    expect(get('sc-q2ai').rows[2].contextNote).toContain('single button detail');
    expect(get('sc-q2bi').answerVariants?.map(v => v.label)).toEqual(['Linen', 'Cotton', 'Wool', 'Silk', 'Another natural fabric']);
    for (const v of get('sc-q2bi').answerVariants ?? []) expect(v.rows.map(r => r.marks)).toEqual([3, 6]);
    expect(get('sc-q2bi').rows[0].contextNote).toContain('Lacemaking');
    expect(get('sc-q2cii').rows[0].contextNote).toContain('sponsorship deals');
    expect(get('sc-q3ci').rows[1].contextNote).toContain('problems paying rent');
    expect(get('sc-q3ci').rows[2].contextNote).toContain('black economy');
  });
  it('retains every scheme continuation under distinct B/C question IDs', () => {
    expect(anchors.q.map(q => q.n)).toEqual(['1', '2', '3', '4', '5', '6', '7', '8', '9']);
    for (const [n, pages] of [['1', [9, 10]], ['2', [11]], ['3', [12]], ['6', [15, 16, 17]], ['7', [18, 19, 20]], ['8', [21, 22, 23]], ['9', [24, 25]]] as const) {
      expect(anchors.q.find(q => q.n === n)?.region.map(r => r.p)).toEqual(pages);
    }
  });
  it('maps every card to its own Atlas question and canonical topic', () => {
    for (const c of sitting) {
      const m = c.questionRef.match(/Section ([ABC]) (?:E\d )?Q(\d+)/)!;
      const file = m[1] === 'A' ? 'LC098GLP014EV.pdf' : 'LC098GLP039EV.pdf';
      const n = String(Number(m[2]) + (m[1] === 'C' ? 5 : 0));
      const row = runtime.questionMappings.find(q => q[0] === 'o' && q[1] === 'e' && q[2] === 2021 && q[4] === file && q[5] === n)!;
      expect(row, c.id).toBeDefined();
      expect((row[6] as number[]).map(i => runtime.topicIds[i]).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
      const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'home-economics-s-and-s' && p.year === 2021 && p.level === 'ordinary' && p.lang === 'ev' && p.fileid === file)!;
      expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === n)!).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
    }
  });
});
