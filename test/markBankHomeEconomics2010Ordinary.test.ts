import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/home-economics/ordinary';
import { tariffReconciles } from '../types/markBank';
import runtime from '../data/examTopics/home-economics-s-and-s-question-runtime.json';
import crosswalk from '../data/examTopics/home-economics-s-and-s-curriculum-crosswalk.json';
import anchors from '../scripts/paper-trail/answers/2010/LC098GLP000EV.pdf.json';
import review from '../scripts/markbank/authoring/home-economics/2010-ol-main-review.json';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
const all = CARDS.filter(c => c.id.startsWith('he-2010-ol-'));
const get = (id: string) => {
  const c = all.find(c => c.id === `he-2010-ol-${id}`);
  if (!c || c.kind !== 'question') throw new Error(id);
  return c;
};
describe('2010 Ordinary Home Economics: independently swept original sources', () => {
  it('covers all50 practice tasks and preserves627 offered source marks', () => {
    expect(all).toHaveLength(50);
    expect(all.map(c => c.id).sort()).toEqual(review.tasks.map(t => t.id).sort());
    expect(all.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(627);
    expect(['sa', 'sb', 'sc'].map(s => all.filter(c => c.id.includes(`-${s}-`)).length)).toEqual([16, 16, 18]);
    for (const c of all) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
      expect(c.rows.every(r => r.marks !== null), c.id).toBe(true);
    }
  });
  it('preserves the four independently priced short-question companion asks', () => {
    expect(['sa-q1', 'sa-q1-sources', 'sa-q6', 'sa-q6-careers', 'sa-q9', 'sa-q9-symbol', 'sa-q10', 'sa-q10-assurance'].map(id => get(id).totalMarks)).toEqual([4, 2, 2, 4, 3, 3, 4, 2]);
    expect(get('sa-q6').rows[0].group?.options).toHaveLength(10);
    expect(get('sa-q6-careers').rows[0].group?.options).toHaveLength(13);
    expect(get('sa-q4').rows.map(r => r.verbatim.split(' — ')[1])).toEqual(['True', 'True', 'False']);
    expect(get('sa-q8').rows.map(r => r.verbatim.split(' — ')[1])).toEqual(['turmeric', 'herbs and spices', 'vitamin E']);
    expect(get('sa-q3').rows[0].group?.claimMax).toBe(2);
    expect(get('sa-q3').rows[0].openList).not.toBe(true);
    expect(get('sa-q12').rows[0].group?.options).toHaveLength(3);
    expect(get('sa-q12').rows[0].openList).not.toBe(true);
    expect(get('sa-q7').taskGroups?.map(g => g.marks)).toEqual([2, 2, 2]);
  });
  it('retains eight complete original input figures and all milk data', () => {
    expect(Object.keys(review.figures)).toHaveLength(8);
    expect(new Set(all.flatMap(c => c.kind === 'question' && c.questionFigure ? [c.questionFigure.src] : [])).size).toBe(8);
    for (const value of ['66 / 46', '3.3 / 3.5', '4.6 / 4.7', '3.9 / 1.7', '2.5 / 1.1', '118 / 120', '0.03 / 0.02', '30 / 19', '8 / 9', '2 / 2']) expect(get('sb-q1a').questionFigure?.alt).toContain(value);
    expect(get('sa-q2').questionFigure?.includesPrompt).toBe(true);
    expect(get('sc-q1ai').questionFigure?.alt).toContain('Blueprint Home Plans');
    expect(get('sc-q2ai').questionFigure?.alt).toContain('Complete photograph');
  });
  it('keeps the four-mark food pair whole and all dependent method guidance visible', () => {
    const c = get('sb-q3b');
    expect(c.rows.map(r => r.marks)).toEqual([4, 4, 12, 4]);
    expect(c.rows[1].permittedMarks).toEqual([0, 4]);
    expect(c.rows[1].parts).toBeUndefined();
    expect(c.rows[1].contextNote).toContain('TWO suitable foods');
    expect(c.rows[2].parts?.map(p => p.permittedMarks)).toEqual([[0, 4], [0, 4], [0, 4]]);
    expect(c.rows[2].contextNote).toContain('jam making:');
    expect(c.rows[2].contextNote).toContain('skim, pot, cover, label and store.');
    expect(get('sb-q2c').taskGroups?.map(g => g.marks)).toEqual([8, 8]);
    expect(get('sb-q5a').rows.map(r => r.marks)).toEqual([5, 5, 5]);
    expect(get('sb-q5a').rows[2].contextNote).toContain('physical OR psychological');
  });
  it('retains low-printed prompts and models, and makes source omissions explicit', () => {
    expect(get('sc-q1cii').questionText).toContain('State two properties of each.');
    expect(get('sc-q1cii').rows[1].contextNote).toContain('marmoleum – wide variety of colours, patterns, easy-care, quiet, etc.');
    expect(get('sc-q1cii').taskGroups?.map(g => g.marks)).toEqual([9, 9]);
    expect(get('sc-q2ai').rows[0].contextNote).toContain('fashion-influences answer bullet is blank');
    expect(get('sc-q2aii').rows.map(r => r.marks)).toEqual([3, 4]);
    expect(get('sc-q2c').rows.map(r => r.marks)).toEqual([3, 3, 3, 3, 3]);
    expect(get('sc-q2c').rows[0].contextNote).toContain('scheme additionally requires the fabric name');
  });
  it('preserves explicit required-heading minima and the choose-three pool', () => {
    expect(get('sc-q3ai').rows.map(r => r.marks)).toEqual([5, 5, 5, 5]);
    expect(get('sc-q3aii').rows.map(r => r.marks)).toEqual([8, 8]);
    expect(get('sc-q3bi').rows.map(r => r.marks)).toEqual([3, 3, 3, 9]);
    expect(get('sc-q3c').rows[0].parts).toHaveLength(5);
    expect(get('sc-q3c').rows[0].contextNote).toContain('Choose THREE of the four');
    expect(get('sc-q3c').rows[0].contextNote).toContain('pension entitlements');
    expect(get('sc-q3c').rows[0].contextNote).toContain('career breaks / job sharing');
  });
  it('preserves all20 original Atlas IDs and maps every emitted task to canonical topics', () => {
    expect(anchors.q.map(q => q.n)).toEqual(Array.from({ length: 20 }, (_, i) => String(i + 1)));
    expect(anchors.q.find(q => q.n === '13')!.region.map(r => r.p)).toEqual([8, 9]);
    expect(anchors.q.find(q => q.n === '18')!.region.map(r => r.p)).toEqual([14, 15]);
    expect(anchors.q.find(q => q.n === '18')!.pY[1]).toBeGreaterThan(0.936);
    expect(anchors.q.find(q => q.n === '20')!.region.map(r => r.p)).toEqual([18, 19, 20]);
    const file = 'LC098GLP000EV.pdf';
    const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'home-economics-s-and-s' && p.year === 2010 && p.level === 'ordinary' && p.lang === 'ev' && p.fileid === file)!;
    for (const c of all) {
      const m = c.questionRef.match(/Section ([ABC]) (?:E\d )?Q(\d+)/)!;
      const n = String(Number(m[2]) + (m[1] === 'A' ? 0 : m[1] === 'B' ? 12 : 17));
      const row = runtime.questionMappings.find(q => q[0] === 'o' && q[1] === 'e' && q[2] === 2010 && q[4] === file && q[5] === n)!;
      expect(row, c.id).toBeDefined();
      expect((row[6] as number[]).map(i => runtime.topicIds[i]).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
      expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === n)!).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
    }
  });
});
