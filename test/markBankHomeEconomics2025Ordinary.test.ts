import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/home-economics/ordinary';
import { tariffReconciles } from '../types/markBank';
import review from '../scripts/markbank/authoring/home-economics/2025-ol-main-review.json';
import local from '../data/examTopics/home-economics-s-and-s-local-crosswalk.json';
import runtime from '../data/examTopics/home-economics-s-and-s-question-runtime.json';
import crosswalk from '../data/examTopics/home-economics-s-and-s-curriculum-crosswalk.json';
import anchors from '../scripts/paper-trail/answers/2025/LC098GLP014EV.pdf.json';
import bcAnchors from '../scripts/paper-trail/answers/2025/LC098GLP039EV.pdf.json';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
const all = CARDS.filter(c => c.id.startsWith('he-2025-ol-'));
const get = (suffix: string) => {
  const c = all.find(c => c.id === `he-2025-ol-${suffix}`);
  if (!c || c.kind !== 'question') throw new Error(suffix);
  return c;
};
describe('2025 Ordinary Home Economics independent source review', () => {
  it('covers all reviewed tasks and reconciles every chosen answer route', () => {
    expect(all.map(c => c.id).sort()).toEqual(review.tasks.map(t => t.id).sort());
    expect(all).toHaveLength(60);
    expect(all.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(749);
    for (const [section, count, marks] of [['A', 16, 84], ['B', 16, 280], ['C', 28, 385]] as const) {
      const cards = all.filter(c => c.section === section);
      expect(cards).toHaveLength(count);
      expect(cards.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(marks);
    }
    for (const c of all) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
      for (const v of c.answerVariants ?? []) expect(tariffReconciles({ ...c, rows: v.rows }), `${c.id}/${v.id}`).toBe(true);
    }
  });
  it('retains independent short tasks, exact partial marks and visible closed answers', () => {
    expect([get('sa-q2').totalMarks, get('sa-q2-source').totalMarks]).toEqual([4, 2]);
    expect([get('sa-q10').totalMarks, get('sa-q10-benefit').totalMarks]).toEqual([4, 2]);
    expect(get('sa-q2-source').rows[0].permittedMarks).toEqual([0, 2]);
    expect(get('sa-q4').rows.map(r => r.verbatim)).toEqual(['movement of food — dietary fibre', 'Glucose releases heat — energy', 'Excess carbohydrate — liver']);
    expect(get('sa-q7').rows.map(r => r.verbatim)).toEqual(['Pasta carbonara — parmesan cheese', 'Lemon cheesecake — cream cheese', 'Cheese sandwich — cheddar cheese slices']);
    expect(get('sa-q7').rows.map(r => r.permittedMarks)).toEqual(Array(3).fill([0, 1, 2]));
    expect(get('sa-q13').rows[0].contextNote).toContain('threat of digital scams');
    expect(get('sa-q14').rows.map(r => r.permittedMarks)).toEqual([[0, 2, 3], [0, 2, 3]]);
    expect(get('sa-q14').questionFigure?.alt).toContain('iron with two dots');
  });
  it('uses the explicit 15-plus-3 menu allocation and all three source meal models', () => {
    const menu = get('sb-q2b');
    expect(menu.taskGroups?.map(g => g.marks)).toEqual([5, 5, 5, 3]);
    expect(menu.rows.map(r => r.marks)).toEqual([4, 1, 4, 1, 4, 1, 3]);
    expect(menu.rows.filter(r => r.id.startsWith('beverage')).map(r => r.permittedMarks)).toEqual([[0, 1], [0, 1], [0, 1]]);
    expect(menu.rows.at(-1)?.permittedMarks).toEqual([0, 3]);
    expect(menu.rows[0].contextNote).toContain('Scrambled eggs on toast');
    expect(menu.rows[2].contextNote).toContain('Quiche Lorraine and green salad');
    expect(menu.rows[4].contextNote).toContain('Pasta carbonara');
    expect(get('sb-q2a').rows.map(r => r.marks)).toEqual([5, 5, 10]);
  });
  it('restores dependent reasons and details on their stable identities', () => {
    expect(get('sc-q2aii').rows.map(r => r.marks)).toEqual([3, 4]);
    expect(get('sc-q2aii').rows.map(r => r.permittedMarks)).toEqual([[0, 3], [0, 2, 4]]);
    for (const id of ['sc-q3aii-name', 'sc-q3bii-name']) {
      expect(get(id).totalMarks).toBe(15);
      expect(get(id).rows.map(r => r.marks)).toEqual([5, 10]);
      expect(get(id).rows[1].parts?.map(p => p.permittedMarks)).toEqual([[0, 3, 5], [0, 3, 5]]);
    }
    expect(get('sc-q4bii-name-reasons').rows.map(r => r.marks)).toEqual([3, 6, 6]);
    expect([get('sc-q1cii').totalMarks, get('sc-q1cii-examples').totalMarks]).toEqual([5, 10]);
    expect(get('sc-q1cii-examples').questionText).toContain('interior design of a room');
  });
  it('keeps required headings and complete choice models without combination cards', () => {
    expect(get('sc-q3ai').rows.map(r => r.marks)).toEqual([5, 5, 5, 5]);
    expect(get('sc-q3aiii').rows.map(r => r.marks)).toEqual([5, 5, 5]);
    expect(get('sc-q4aii').rows.map(r => r.marks)).toEqual([6, 6, 6]);
    expect(get('sc-q2bii').answerVariants?.map(v => v.label)).toEqual(['waterproofing', 'anti-static', 'stain resistant', 'crease resistant', 'mercerising', 'flame retardant', 'Another valid finish']);
    expect(get('sb-q3b').answerVariants).toHaveLength(7);
    expect(get('sb-q1a').answerVariants?.map(v => v.rows.map(r => r.marks))).toEqual([[4, 20], [4, 20]]);
    expect(get('sb-q1a').questionFigure?.alt).toContain('4.3/5.6 g');
  });
  it('retains complete original context and identifies printed scientific errors', () => {
    expect(get('sc-q2ai').questionFigure?.src).toBe(get('sc-q2aii').questionFigure?.src);
    expect(get('sc-q2ai').questionFigure?.alt).toContain('All three');
    expect(get('sc-q1ai').questionFigure?.src).toBe(get('sc-q1aiii').questionFigure?.src);
    expect(get('sc-q4ai').questionFigure?.alt).toContain('Both original');
    expect(get('sc-q1bii').rows[0].contextNote).toContain('does not inherently contain an RCD');
    expect(get('sc-q1bii').rows[2].contextNote).toContain('unit of ENERGY');
    expect(get('sa-q10').rows[0].contextNote).toContain('energy carrier');
    expect(get('sc-q4cii').questionText).toContain('other family members');
  });
  it('maps all sixty cards to complete original paper and scheme groups', () => {
    expect(anchors.q).toHaveLength(14);
    expect(bcAnchors.q).toHaveLength(9);
    expect(bcAnchors.q.slice(5).map(q => q.region.map(r => r.p))).toEqual([[16, 17], [18, 19], [20, 21], [22, 23]]);
    expect(bcAnchors.q[5].endY).toBeGreaterThan(0.89);
    const mapped = local.reviewedEnglish2025Ordinary.markBankMappings;
    expect(mapped.map(m => m.id).sort()).toEqual(all.map(c => c.id).sort());
    for (const m of mapped) {
      const route = runtime.questionMappings.find(r => r[0] === 'o' && r[1] === 'e' && r[2] === 2025 && r[4] === m.fileid && r[5] === m.n);
      expect(route, m.id).toBeTruthy();
      const topicIds = (route![6] as number[]).map(i => runtime.topicIds[i]);
      for (const id of m.atlasTopicIds) expect(topicIds, m.id).toContain(id);
      const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'home-economics-s-and-s' && p.year === 2025 && p.level === 'ordinary' && p.lang === 'ev' && p.fileid === m.fileid)!;
      expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === m.n)!).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(m.topicId)), m.id).toBe(true);
    }
  });
});
