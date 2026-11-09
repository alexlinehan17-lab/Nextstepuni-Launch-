import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/home-economics/ordinary';
import { tariffReconciles } from '../types/markBank';
import runtime from '../data/examTopics/home-economics-s-and-s-question-runtime.json';
import crosswalk from '../data/examTopics/home-economics-s-and-s-curriculum-crosswalk.json';
import anchors from '../scripts/paper-trail/answers/2014/LC098GLP000EV.pdf.json';
import review from '../scripts/markbank/authoring/home-economics/2014-ol-main-review.json';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
const all = CARDS.filter(c => c.id.startsWith('he-2014-ol-'));
const get = (id: string) => {
  const c = all.find(c => c.id === `he-2014-ol-${id}`);
  if (!c || c.kind !== 'question') throw new Error(id);
  return c;
};
describe('2014 Ordinary Home Economics: independently swept original sources', () => {
  it('retains all 51 priced tasks and 627 offered marks', () => {
    expect(all).toHaveLength(51);
    expect(all.map(c => c.id).sort()).toEqual(review.tasks.map(c => c.id).sort());
    expect(['sa', 'sb', 'sc'].map(s => all.filter(c => c.id.includes(`-${s}-`)).length)).toEqual([12, 18, 21]);
    expect(all.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(627);
    for (const c of all) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
      for (const v of c.answerVariants ?? []) expect(tariffReconciles({ ...c, rows: v.rows }), `${c.id}/${v.id}`).toBe(true);
    }
  });
  it('keeps whole-six tariffs, complete companions and unrestricted source pools', () => {
    for (let n = 1; n <= 12; n++) {
      const c = get(`sa-q${n}`);
      expect(c.tariffModel?.kind).toBe('questionTotal');
      expect(c.rows.every(r => r.marks === null && !r.permittedMarks && !r.parts)).toBe(true);
      expect(c.rows[0].contextNote).toContain('no per-answer allocation');
    }
    expect(get('sa-q5').questionText).toContain('List two effects of cooking on cheese.');
    expect(get('sa-q11').questionText).toContain('Explain why natural fibres');
    expect(get('sa-q6').questionText.match(/\[blank\]/g)).toHaveLength(3);
    expect(get('sa-q3').rows[2].contextNote).toContain('ANY TWO');
    expect(get('sa-q7').rows[0].contextNote).toContain('ANY THREE');
    expect(get('sa-q8').topicId).toBe('home-economics-0-11');
    expect(get('sa-q9').topicId).toBe('home-economics-1-3');
  });
  it('keeps eight original inputs, all table data and complete electricity captions', () => {
    expect(Object.keys(review.figures)).toHaveLength(8);
    expect(new Set(all.flatMap(c => c.kind === 'question' && c.questionFigure ? [c.questionFigure.src] : [])).size).toBe(8);
    for (const n of [1, 2, 4, 5, 9, 11]) expect(get(`sa-q${n}`).questionFigure?.includesPrompt).toBe(true);
    expect(get('sb-q1a').questionFigure?.alt).toContain('20.0g/6.8g/0.4g');
    expect(get('sb-q1a').stem).toContain('FSAI website');
    expect(get('sc-q1ai').questionFigure?.alt).toContain('Miniature Circuit Breakers');
    expect(get('sa-q9').questionFigure?.alt).toContain('wave guide/turntable/magnetron');
  });
  it('preserves carbohydrate and milk headings, source anomaly and all paired soup choices', () => {
    expect(get('sb-q1a').answerVariants).toHaveLength(3);
    expect(get('sb-q1b').rows.map(r => r.marks)).toEqual([9, 9, 8, 4]);
    expect(get('sb-q1b').rows[0].contextNote).toContain('not all six labels');
    expect(get('sb-q1b').rows[3].contextNote).toContain('denatures egg protein');
    expect(get('sb-q1d').rows.map(r => r.marks)).toEqual([5, 5, 5, 5]);
    expect(get('sb-q2a').rows.map(r => r.marks)).toEqual([5, 5, 10]);
    expect(get('sb-q2c').rows.map(r => r.marks)).toEqual([6, 6, 6]);
    expect(get('sb-q3a').taskGroups?.map(g => g.marks)).toEqual([7, 7]);
    expect(get('sb-q3a').rows[0].group?.options).toHaveLength(3);
    expect(get('sb-q3bii').rows.map(r => r.marks)).toEqual([4, 4, 4]);
    expect(get('sb-q3bii').rows[2].contextNote).toContain('Both sides required within THREE');
  });
  it('keeps independent soup/pollution tariffs and original dependent naming context', () => {
    expect([get('sb-q3bi').totalMarks, get('sb-q3bii').totalMarks]).toEqual([12, 12]);
    expect([get('sb-q4bi').totalMarks, get('sb-q4bii').totalMarks]).toEqual([10, 10]);
    expect(get('sb-q4bi').rows[0].group?.options).toHaveLength(5);
    expect(get('sb-q4bii').stem).toContain('Name two different types');
    expect(get('sb-q4bii').rows.map(r => r.marks)).toEqual([5, 5]);
    for (const row of get('sb-q4bii').rows) expect(row.contextNote).toContain('Each effect must match its own type');
    expect(get('sb-q4c').rows[0].group?.options).toHaveLength(8);
    expect(get('sb-q5b').rows[0].contextNote).toContain('historical 2014');
  });
  it('retains source gaps, linked outfits and flexible required elective headings', () => {
    expect(get('sc-q1ai').rows.map(r => r.marks)).toEqual([6, 6, 6]);
    expect(get('sc-q1aii').rows[1].contextNote).toContain('as printed');
    expect(get('sc-q2ai').rows.map(r => r.marks)).toEqual([6, 6]);
    expect(get('sc-q2ai').rows[0].contextNote).toContain('no model drawing');
    expect(get('sc-q2aii').rows[0].group?.options).toHaveLength(6);
    expect(get('sc-q2aii').rows[1].contextNote).toContain('unpaired');
    expect(get('sc-q2aiii').rows[0].group?.options).toHaveLength(4);
    expect(get('sc-q2bii').rows[0].contextNote).toContain('without model descriptions');
    expect(get('sc-q2cii').taskGroups?.map(g => g.marks)).toEqual([5, 5]);
    expect(get('sc-q2cii').rows[0].group?.options).toHaveLength(8);
    expect(get('sc-q3aii').rows.map(r => r.marks)).toEqual([5, 5, 5, 5]);
    expect(get('sc-q3bi').rows.map(r => r.marks)).toEqual([5, 5, 10]);
    expect(get('sc-q3cii').rows[1].contextNote).toContain('Focus Ireland');
  });
  it('preserves twenty original Atlas identities, continuation pages and every canonical topic', () => {
    expect(anchors.q.map(q => q.n)).toEqual(Array.from({ length: 20 }, (_, i) => String(i + 1)));
    expect(anchors.q.find(q => q.n === '13')!.region.map(r => r.p)).toEqual([8, 9]);
    expect(anchors.q.find(q => q.n === '16')!.region.map(r => r.p)).toEqual([12, 13]);
    expect(anchors.q.find(q => q.n === '18')!.region.map(r => r.p)).toEqual([15, 16, 17]);
    expect(anchors.q.find(q => q.n === '19')!.region.map(r => r.p)).toEqual([18, 19]);
    expect(anchors.q.find(q => q.n === '20')!.region.map(r => r.p)).toEqual([20, 21, 22]);
    for (const q of anchors.q) expect(q.pY[1]).toBeGreaterThan(q.pY[0]);
    const file = 'LC098GLP000EV.pdf';
    const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'home-economics-s-and-s' && p.year === 2014 && p.level === 'ordinary' && p.lang === 'ev' && p.fileid === file)!;
    for (const c of all) {
      const m = c.questionRef.match(/Section ([ABC]) (?:E\d )?Q(\d+)/)!;
      const n = String(Number(m[2]) + (m[1] === 'A' ? 0 : m[1] === 'B' ? 12 : 17));
      const row = runtime.questionMappings.find(q => q[0] === 'o' && q[1] === 'e' && q[2] === 2014 && q[4] === file && q[5] === n)!;
      expect(row, c.id).toBeDefined();
      expect((row[6] as number[]).map(i => runtime.topicIds[i]).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
      expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === n)!).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
    }
  });
});
