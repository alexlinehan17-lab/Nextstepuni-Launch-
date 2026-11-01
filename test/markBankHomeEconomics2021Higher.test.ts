import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/home-economics/higher';
import { tariffReconciles } from '../types/markBank';
import runtime from '../data/examTopics/home-economics-s-and-s-question-runtime.json';
import crosswalk from '../data/examTopics/home-economics-s-and-s-curriculum-crosswalk.json';
import anchors from '../scripts/paper-trail/answers/2021/LC098ALP039EV.pdf.json';
import review from '../scripts/markbank/authoring/home-economics/2021-hl-main-review.json';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
const get = (id: string) => {
  const c = CARDS.find(c => c.id === `he-2021-hl-${id}`);
  if (!c || c.kind !== 'question') throw new Error(id);
  return c;
};
const sitting = CARDS.filter(c => c.year === 2021 && !c.id.includes('deferred'));
describe('2021 Higher Home Economics full source review', () => {
  it('covers the independent paper review with every tariff and open route intact', () => {
    expect(sitting).toHaveLength(62);
    expect(sitting.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(749);
    expect(sitting.map(c => c.id).sort()).toEqual(review.tasks.map(c => c.id).sort());
    for (const [section, count, marks] of [['A', 16, 84], ['B', 18, 280], ['C', 28, 385]] as const) {
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
  it('splits independent prompts and retains separately graded paired answers', () => {
    for (const [id, suffix, first, second] of [['sa-q4', 'factors', 4, 2], ['sa-q8', 'advantages', 2, 4], ['sb-q5a', 'universality', 5, 5], ['sc-q1cii', 'strategies', 4, 8]] as const) {
      expect(get(id).totalMarks).toBe(first);
      expect(get(`${id}-${suffix}`).totalMarks).toBe(second);
      expect(get(id).questionRef).not.toBe(get(`${id}-${suffix}`).questionRef);
    }
    expect(get('sa-q1').rows.map(r => r.permittedMarks)).toEqual([[0, 2], [0, 1], [0, 2], [0, 1]]);
    for (const id of ['sa-q5', 'sa-q11']) {
      expect(get(id).taskGroups?.map(g => g.marks)).toEqual([2, 2, 2]);
      expect(get(id).rows.map(r => r.permittedMarks)).toEqual(Array(6).fill([0, 1]));
    }
    expect(get('sa-q6').rows[0].parts?.map(p => p.permittedMarks)).toEqual([[0, 2, 3], [0, 2, 3]]);
    expect(get('sa-q6').rows[0].contextNote).toContain('easy to control portion sizes');
    expect(get('sa-q9').rows[1].contextNote).toContain('Dextrinisation');
    expect(get('sa-q11').rows[0].contextNote).toContain('Charity shops');
  });
  it('restores eggs and the whole four-stage HACCP task, including the continued preparation row', () => {
    expect(get('sb-q2a').totalMarks).toBe(20);
    expect(get('sb-q2a').rows[0].parts).toHaveLength(5);
    const c = get('sb-q3b');
    expect(c.totalMarks).toBe(24);
    expect(c.taskGroups?.map(g => g.marks)).toEqual([6, 6, 6, 6]);
    expect(c.rows.map(r => r.marks)).toEqual(Array(4).fill([1, 2, 3]).flat());
    const table = c.rows[0].contextNote!;
    for (const stage of ['Purchase', 'Transportation', 'Storage', 'Preparation', 'Cooking', 'Serving', 'Reheating / hot holding']) expect(table).toContain(`${stage} — hazards:`);
    expect(table).toContain('before and after handling food');
    expect(table).toContain('Ensure that containers used for storage are absolutely clean');
    expect(table).toContain('Hold cooked food for a maximum of 90 minutes');
    expect(table).toContain('not a general requirement to exceed 100°C');
  });
  it('enforces the printed heading quotas and unequal marking steps', () => {
    expect(get('sb-q1a').rows.map(r => r.marks)).toEqual([10, 10]);
    expect(get('sb-q1a').rows[0].parts?.[0].permittedMarks).toEqual([0, 1, 3, 5]);
    expect(get('sb-q1c').rows.map(r => r.marks)).toEqual([2, 2, 2, 6, 6]);
    expect(get('sb-q1e').rows.map(r => r.marks)).toEqual([8, 8, 4]);
    expect(get('sb-q3a').rows.map(r => r.marks)).toEqual([8, 8]);
    expect(get('sb-q3c').rows.map(r => r.permittedMarks)).toEqual([[0, 2, 3, 5], [0, 2, 3, 5]]);
    expect(get('sb-q4b').rows.map(r => r.marks)).toEqual([6, 6, 6]);
    expect(get('sb-q5b').rows.map(r => r.marks)).toEqual([6, 6, 6, 6]);
    expect(get('sc-q1ai').rows.map(r => r.marks)).toEqual([4, 4, 8]);
    expect(get('sc-q3aiii').rows.map(r => r.marks)).toEqual([4, 4, 4]);
    expect(get('sc-q4bi').rows.map(r => r.marks)).toEqual([8, 12]);
    expect(get('sc-q4cii').rows.map(r => r.marks)).toEqual([6, 6, 6]);
  });
  it('retains both original figures, complete profile routes and source corrections', () => {
    expect(get('sb-q1a').questionFigure?.alt).toContain('Health and Wellbeing 42%; Responsible Living 27%');
    expect(get('sc-q2ai').questionFigure?.alt).toContain('four athleisure outfits');
    expect(get('sc-q2b').answerVariants?.map(v => v.label)).toEqual(['Cotton', 'Linen', 'Wool', 'Silk', 'Another natural-fibre fabric']);
    for (const v of get('sc-q2b').answerVariants ?? []) expect(v.rows.map(r => r.marks)).toEqual([3, 6, 3, 3]);
    expect(get('sc-q2b').answerVariants?.[0].rows[2].contextNote).toContain('weakened by sun');
    expect(get('sc-q2b').answerVariants?.[3].rows[3].contextNote).toContain('cushion covers');
    expect(get('sc-q4aii').answerVariants).toHaveLength(7);
    expect(get('sc-q4aii').answerVariants?.find(v => v.label === 'UHT')?.rows[1].contextNote).toContain('at least 135°C');
    for (const v of get('sc-q4aii').answerVariants ?? []) expect(v.rows.map(r => r.marks)).toEqual([2, 8, 4, 4]);
    expect(get('sc-q4aii').rows[3].contextNote).toContain('storage instructions');
    expect(get('sb-q1d').rows[0].contextNote).toContain('does not turn it into haem iron');
    expect(get('sc-q4ci').rows[0].contextNote).toContain('desk research uses secondary/existing data');
  });
  it('retains every scheme continuation under distinct B/C question IDs', () => {
    expect(anchors.q.map(q => q.n)).toEqual(['1', '2', '3', '4', '5', '6', '7', '8', '9']);
    for (const [n, pages] of [['1', [10, 11, 12]], ['3', [14, 15]], ['6', [18, 19, 20]], ['7', [21, 22]], ['8', [23, 24, 25]], ['9', [26, 27, 28]]] as const) {
      expect(anchors.q.find(q => q.n === n)?.region.map(r => r.p)).toEqual(pages);
    }
  });
  it('maps every card to its own Atlas question and canonical topic', () => {
    for (const c of sitting) {
      const m = c.questionRef.match(/Section ([ABC]) (?:E\d )?Q(\d+)/)!;
      const file = m[1] === 'A' ? 'LC098ALP014EV.pdf' : 'LC098ALP039EV.pdf';
      const n = String(Number(m[2]) + (m[1] === 'C' ? 5 : 0));
      const row = runtime.questionMappings.find(q => q[0] === 'h' && q[1] === 'e' && q[2] === 2021 && q[4] === file && q[5] === n)!;
      expect(row, c.id).toBeDefined();
      expect((row[6] as number[]).map(i => runtime.topicIds[i]).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
      const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'home-economics-s-and-s' && p.year === 2021 && p.level === 'higher' && p.lang === 'ev' && p.fileid === file)!;
      expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === n)!).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
    }
  });
});
