import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/home-economics/ordinary';
import { tariffReconciles } from '../types/markBank';
import runtime from '../data/examTopics/home-economics-s-and-s-question-runtime.json';
import crosswalk from '../data/examTopics/home-economics-s-and-s-curriculum-crosswalk.json';
import anchors from '../scripts/paper-trail/answers/2013/LC098GLP000EV.pdf.json';
import review from '../scripts/markbank/authoring/home-economics/2013-ol-main-review.json';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
const all = CARDS.filter(c => c.id.startsWith('he-2013-ol-'));
const get = (id: string) => {
  const c = all.find(c => c.id === `he-2013-ol-${id}`);
  if (!c || c.kind !== 'question') throw new Error(id);
  return c;
};
describe('2013 Ordinary Home Economics: independent original-source review', () => {
  it('retains 52 priced tasks and 627 offered marks', () => {
    expect(all).toHaveLength(52);
    expect(all.map(c => c.id).sort()).toEqual(review.tasks.map(c => c.id).sort());
    expect(['sa', 'sb', 'sc'].map(s => all.filter(c => c.id.includes(`-${s}-`)).length)).toEqual([12, 20, 20]);
    expect(all.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(627);
    for (const c of all) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
      for (const v of c.answerVariants ?? []) expect(tariffReconciles({ ...c, rows: v.rows }), `${c.id}/${v.id}`).toBe(true);
    }
  });
  it('preserves whole-six tariffs, companion asks, word pools and complete answers', () => {
    for (let n = 1; n <= 12; n++) {
      const c = get(`sa-q${n}`);
      expect(c.tariffModel?.kind).toBe('questionTotal');
      expect(c.rows.every(r => r.marks === null && !r.permittedMarks && !r.parts)).toBe(true);
      expect(c.rows[0].contextNote).toContain('no per-answer allocation');
    }
    expect(get('sa-q2').questionText.match(/\[blank\]/g)).toHaveLength(3);
    expect(get('sa-q2').rows.map(r => r.verbatim)).toEqual(['rhodopsin', 'night blindness', 'hypervitaminosis']);
    expect(get('sa-q2').rows[2].contextNote).toContain('hypervitiminosis');
    expect(get('sa-q5').questionText).toContain('heat treatments');
    expect(get('sa-q5').rows.map(r => r.verbatim).join(' ')).toContain('evaporated, condensed');
    expect(get('sa-q7').rows[0].contextNote).toContain('ANY TWO');
    expect(get('sa-q7').questionText).toContain('one use');
    expect(get('sa-q10').questionText).toContain('two advantages');
    expect(get('sa-q12').questionText).toContain('encourage consumer spending');
    expect(get('sa-q4').topicId).toBe('home-economics-0-3');
  });
  it('retains eight complete original figure groups and their input pools', () => {
    expect(Object.keys(review.figures)).toHaveLength(8);
    expect(new Set(all.flatMap(c => c.kind === 'question' && c.questionFigure ? [c.questionFigure.src] : [])).size).toBe(8);
    for (const n of [1, 3, 4, 6, 8, 11]) expect(get(`sa-q${n}`).questionFigure?.includesPrompt).toBe(true);
    expect(get('sa-q1').questionFigure?.alt).toContain('avocado, sardines, cheese');
    expect(get('sa-q8').rows.map(r => r.verbatim)).toEqual(['Hand wash only', 'Do not tumble dry']);
    expect(get('sb-q1a').questionFigure?.alt).toContain('Food Safety Authority, 2012');
    for (const value of ['roof25%', 'windows15%', 'walls35%', 'doors10%', 'floors15%']) expect(get('sc-q1ai').questionFigure?.alt).toContain(value);
    expect(get('sa-q11').rows[0].contextNote).toContain('shared source lists');
  });
  it('keeps coherent protein profiles and separately priced planning and conflict asks', () => {
    expect(get('sb-q1b').rows.map(r => r.marks)).toEqual([4, 8, 12, 8]);
    expect(get('sb-q1c').taskGroups?.map(g => g.marks)).toEqual([6, 6]);
    expect([get('sb-q2b-guidelines').totalMarks, get('sb-q2b-menu').totalMarks]).toEqual([12, 18]);
    expect(get('sb-q2b-menu').rows.map(r => r.marks)).toEqual([6, 6, 6]);
    expect(get('sb-q2b-menu').rows[0].contextNote).toContain('Mixed berries smoothie');
    expect(get('sb-q2b-menu').rows[1].contextNote).toContain('Cereal bar');
    expect([get('sb-q5c-definition').totalMarks, get('sb-q5c-ways').totalMarks]).toEqual([5, 10]);
    expect(get('sb-q5c-ways').stem).toContain('generation conflict');
    expect(get('sb-q5bi').questionText).toMatch(/^Comment on:/);
    expect(get('sb-q5bi').questionText).not.toMatch(/ and$/);
    expect(get('sb-q5bi').topicId).toBe('home-economics-2-3');
  });
  it('preserves original scenario, fridge profile and explicit missing models', () => {
    expect(get('sb-q4a').stem).toContain('Jane bought Peter a jacket');
    expect(get('sb-q4c').rows[0].contextNote).toContain('does not print a model explanation for every right');
    expect(get('sb-q3b').rows.map(r => r.marks)).toEqual([2, 9, 9, 4]);
    expect(get('sb-q3b').rows[1].contextNote).toContain('1°C');
    expect(get('sc-q2ai').rows.map(r => r.marks)).toEqual([3, 6]);
    expect(get('sc-q2ai').rows[0].contextNote).toContain('NO model drawing');
    expect(get('sc-q2aii').stem).toContain('Sketch and describe an outfit');
    expect(get('sc-q2b').answerVariants).toHaveLength(5);
    expect(get('sc-q2b').rows.map(r => r.marks)).toEqual([5, 5, 5]);
    expect(get('sc-q2b').rows[2].contextNote).toContain('Lacemaking');
  });
  it('retains linked choices and required headings within flexible total quotas', () => {
    expect(get('sc-q1ai').rows.map(r => r.marks)).toEqual([8, 4]);
    expect(Boolean(get('sc-q1ai').rows[0].openList)).toBe(false);
    expect(get('sc-q1ai').rows[1].contextNote).toContain('ONE reason');
    expect(get('sc-q1aii').taskGroups?.map(g => g.marks)).toEqual([8, 8]);
    expect(get('sc-q1bi').taskGroups?.map(g => g.marks)).toEqual([6, 6, 6]);
    expect(get('sc-q1bii').rows.map(r => r.marks)).toEqual([4, 4, 4]);
    expect(get('sc-q3aiii').answerVariants).toHaveLength(3);
    expect(get('sc-q3aiii').rows.map(r => r.marks)).toEqual([10]);
    expect(get('sc-q3aiii').rows[0].contextNote).toContain('no separate name allocation');
    expect(get('sc-q3bi').rows.map(r => r.marks)).toEqual([6, 6, 6]);
    expect(get('sc-q3bi').rows[2].contextNote).toContain('no two-per-group quota');
    expect(get('sc-q3cii').rows.map(r => r.marks)).toEqual([5, 5, 5]);
    expect(get('sc-q3cii').rows[2].contextNote).toContain('not two per side');
    expect(get('sc-q3cii').topicId).toBe('home-economics-3-11');
  });
  it('preserves twenty original physical IDs and every canonical Atlas link', () => {
    expect(anchors.q.map(q => q.n)).toEqual(Array.from({ length: 20 }, (_, i) => String(i + 1)));
    expect(anchors.q.find(q => q.n === '13')!.region.map(r => r.p)).toEqual([8, 9]);
    expect(anchors.q.find(q => q.n === '18')!.region.map(r => r.p)).toEqual([14, 15, 16]);
    expect(anchors.q.find(q => q.n === '19')!.region.map(r => r.p)).toEqual([17, 18]);
    expect(anchors.q.find(q => q.n === '20')!.region.map(r => r.p)).toEqual([19, 20]);
    for (const q of anchors.q) expect(q.pY[1]).toBeGreaterThan(q.pY[0]);
    const file = 'LC098GLP000EV.pdf';
    const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'home-economics-s-and-s' && p.year === 2013 && p.level === 'ordinary' && p.lang === 'ev' && p.fileid === file)!;
    for (const c of all) {
      const m = c.questionRef.match(/Section ([ABC]) (?:E\d )?Q(\d+)/)!;
      const n = String(Number(m[2]) + (m[1] === 'A' ? 0 : m[1] === 'B' ? 12 : 17));
      const row = runtime.questionMappings.find(q => q[0] === 'o' && q[1] === 'e' && q[2] === 2013 && q[4] === file && q[5] === n)!;
      expect(row, c.id).toBeDefined();
      expect((row[6] as number[]).map(i => runtime.topicIds[i]).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
      expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === n)!).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
    }
  });
});
