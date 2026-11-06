import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/home-economics/higher';
import { tariffReconciles } from '../types/markBank';
import runtime from '../data/examTopics/home-economics-s-and-s-question-runtime.json';
import crosswalk from '../data/examTopics/home-economics-s-and-s-curriculum-crosswalk.json';
import anchors from '../scripts/paper-trail/answers/2026/LC098ALP014EV.pdf.json';
import bcAnchors from '../scripts/paper-trail/answers/2026/LC098ALP039EV.pdf.json';
import review from '../scripts/markbank/authoring/home-economics/2026-hl-main-review.json';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
const get = (id: string) => {
  const c = CARDS.find(c => c.id === `he-2026-hl-${id}`);
  if (!c || c.kind !== 'question') throw new Error(id);
  return c;
};
const all = CARDS.filter(c => c.id.startsWith('he-2026-hl-'));
describe('2026 Higher Home Economics independently reviewed main sitting', () => {
  it('covers every reviewed task and answer route at its published tariff', () => {
    expect(all.map(c => c.id).sort()).toEqual(review.tasks.map(t => t.id).sort());
    expect(all).toHaveLength(60);
    expect(all.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(749);
    expect(['sa', 'sb', 'sc'].map(s => all.filter(c => c.id.includes(`-${s}-`)).length)).toEqual([15, 18, 27]);
    for (const c of all) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
      for (const v of c.answerVariants ?? []) expect(tariffReconciles({ ...c, rows: v.rows }), `${c.id}/${v.id}`).toBe(true);
    }
  });
  it('exposes binary answers as claimable options and retains all required table cells', () => {
    expect(get('sa-q1').rows.map(r => r.marks)).toEqual([1, 1, 1, 1, 1, 1]);
    expect(get('sa-q1').taskGroups?.map(g => g.marks)).toEqual([2, 2, 2]);
    expect(get('sa-q1').questionFigure?.alt).toContain('all six cells retained');
    expect(get('sa-q5').rows.map(r => r.permittedMarks)).toEqual(Array(3).fill([0, 1, 2]));
    expect(get('sa-q5').questionFigure?.src).toContain('uht-table');
    expect([get('sa-q6').totalMarks, get('sa-q6-factors').totalMarks]).toEqual([2, 4]);
    expect(get('sa-q6-factors').rows[0].group?.options).toHaveLength(15);
    expect(get('sa-q6-factors').rows[0].group?.claimMax).toBe(2);
    expect(get('sb-q1c').rows[0].group?.options).toHaveLength(9);
    expect(get('sb-q1c').rows[0].group?.claimMax).toBe(7);
    expect(get('sb-q1c').rows[0].group?.perOption).toBe(2);
  });
  it('keeps the complete source comparison, paired examples and compulsory response quotas', () => {
    for (const datum of ['523/122', '17/12', '37/2.9', '7.6/1.3', '24/10', '16/8', '60/190', '13/3.5', '0.8/0.2']) expect(get('sb-q1a').questionFigure?.alt).toContain(datum);
    expect(get('sb-q1b').taskGroups?.map(g => g.marks)).toEqual([4, 4]);
    expect(get('sb-q1e').rows.map(r => r.marks)).toEqual([5, 5, 10]);
    expect(get('sb-q2b').rows.map(r => r.marks)).toEqual([3, 3, 6]);
    expect(get('sb-q5a').rows.map(r => r.marks)).toEqual([8, 8, 4]);
    expect(get('sc-q3aii').rows.map(r => r.marks)).toEqual([5, 5, 10]);
    expect(get('sc-q3ci').rows.map(r => r.marks)).toEqual([5, 5, 5, 5]);
    expect(get('sb-q3b').taskGroups?.map(g => g.marks)).toEqual([9, 9]);
    expect(get('sb-q3b').rows.map(r => r.permittedMarks)).toEqual([[0, 2, 3], undefined, undefined, [0, 2, 3], undefined, undefined]);
    expect(get('sb-q3b').rows[1].verbatim).toContain('Aspartame');
  });
  it('retains lower-page continuations and separately priced will tasks', () => {
    expect(get('sb-q3c').rows[0].contextNote).toContain('ease of use');
    expect(get('sb-q5b').rows[1].contextNote).toContain('role reversal as adult children become older');
    expect([get('sb-q5c').totalMarks, get('sb-q5c-procedure').totalMarks]).toEqual([6, 8]);
    expect(get('sb-q5c').rows[0].parts?.map(p => p.permittedMarks)).toEqual([[0, 2, 3], [0, 2, 3]]);
    expect(get('sb-q5c-procedure').rows[0].parts?.map(p => p.permittedMarks)).toEqual(Array(4).fill([0, 1, 2]));
    expect(bcAnchors.q.find(q => q.n === '5')!.region.map(r => r.p)).toEqual([15, 16]);
    expect(bcAnchors.q.find(q => q.n === '9')!.region.map(r => r.p)).toEqual([26, 27, 28]);
    expect(bcAnchors.q.find(q => q.n === '9')!.region.find(r => r.p === 27)!.r[3]).toBeGreaterThan(0.89);
  });
  it('keeps open profiles whole and preserves source grading without invented sketch criteria', () => {
    for (const [id, count, marks] of [['sc-q1ci', 6, [3, 5, 5, 5]], ['sc-q2b', 5, [3, 4, 4, 4]], ['sc-q3aiii', 5, [4, 6]], ['sc-q3cii', 3, [4, 6]], ['sc-q4bi', 5, [3, 3, 12]], ['sc-q4cii', 3, [3, 9]]] as const) {
      expect(get(id).answerVariants).toHaveLength(count);
      for (const v of get(id).answerVariants ?? []) expect(v.rows.map(r => r.marks)).toEqual(marks);
    }
    expect(get('sc-q2aii').rows[0].permittedMarks).toEqual([0, 1, 3, 5]);
    expect(get('sc-q2aiii').stem).toContain(get('sc-q2aii').questionText);
    expect(get('sc-q2ci').rows[0].permittedMarks).toEqual([0, 2, 4, 6]);
    expect(get('sc-q4aii').rows.map(r => r.marks)).toEqual([14, 2, 2]);
    expect(get('sc-q4aii').rows[0].parts?.map(p => p.permittedMarks)).toEqual(Array(7).fill([0, 1, 2]));
  });
  it('maps all tasks to their own original paper/scheme group and canonical topics', () => {
    expect(anchors.q).toHaveLength(14);
    expect(bcAnchors.q.map(q => q.n)).toEqual(['1', '2', '3', '4', '5', '6', '7', '8', '9']);
    for (const c of all) {
      const m = c.questionRef.match(/Section ([ABC]) (?:E\d )?Q(\d+)/)!;
      const file = m[1] === 'A' ? 'LC098ALP014EV.pdf' : 'LC098ALP039EV.pdf';
      const n = String(Number(m[2]) + (m[1] === 'C' ? 5 : 0));
      const row = runtime.questionMappings.find(q => q[0] === 'h' && q[1] === 'e' && q[2] === 2026 && q[4] === file && q[5] === n)!;
      expect(row, c.id).toBeDefined();
      expect((row[6] as number[]).map(i => runtime.topicIds[i]).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
      const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'home-economics-s-and-s' && p.year === 2026 && p.level === 'higher' && p.lang === 'ev' && p.fileid === file)!;
      expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === n)!).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
    }
  });
});
