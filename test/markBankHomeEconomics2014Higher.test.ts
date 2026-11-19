import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/home-economics/higher';
import { tariffReconciles } from '../types/markBank';
import runtime from '../data/examTopics/home-economics-s-and-s-question-runtime.json';
import crosswalk from '../data/examTopics/home-economics-s-and-s-curriculum-crosswalk.json';
import anchors from '../scripts/paper-trail/answers/2014/LC098ALP000EV.pdf.json';
import review from '../scripts/markbank/authoring/home-economics/2014-hl-main-review.json';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
const all = CARDS.filter(c => c.id.startsWith('he-2014-hl-'));
const get = (id: string) => {
  const c = all.find(c => c.id === `he-2014-hl-${id}`);
  if (!c || c.kind !== 'question') throw new Error(id);
  return c;
};
describe('2014 Higher Home Economics: independently swept original sources', () => {
  it('retains all 49 priced tasks and 627 offered marks', () => {
    expect(all).toHaveLength(49);
    expect(all.map(c => c.id).sort()).toEqual(review.tasks.map(c => c.id).sort());
    expect(['sa', 'sb', 'sc'].map(s => all.filter(c => c.id.includes(`-${s}-`)).length)).toEqual([12, 18, 19]);
    expect(all.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(627);
    for (const c of all) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
      for (const v of c.answerVariants ?? []) expect(tariffReconciles({ ...c, rows: v.rows }), `${c.id}/${v.id}`).toBe(true);
    }
  });
  it('keeps whole-six A questions, all cheese choices and correct curriculum topics', () => {
    for (let n = 1; n <= 12; n++) {
      const c = get(`sa-q${n}`);
      expect(c.tariffModel?.kind).toBe('questionTotal');
      expect(c.rows.every(r => r.marks === null && !r.permittedMarks && !r.parts)).toBe(true);
      expect(c.rows[0].contextNote).toContain('no per-answer allocation');
    }
    expect(get('sa-q1').rows[1].contextNote).toContain('65% of jam');
    expect(get('sa-q6').rows).toHaveLength(5);
    expect(get('sa-q6').rows[0].contextNote).toContain('THREE');
    expect(get('sa-q4').rows[1].contextNote).toContain('ANY TWO');
    expect(get('sa-q5').topicId).toBe('home-economics-0-11');
    expect(get('sa-q7').topicId).toBe('home-economics-0-1');
    expect(get('sa-q10').topicId).toBe('home-economics-3-3');
  });
  it('retains complete original question inputs and both original answer figures', () => {
    expect(Object.keys(review.figures)).toHaveLength(7);
    expect(new Set(all.flatMap(c => c.kind === 'question' && c.questionFigure ? [c.questionFigure.src] : [])).size).toBe(5);
    for (const n of [2, 6, 8]) expect(get(`sa-q${n}`).questionFigure?.includesPrompt).toBe(true);
    expect(get('sb-q1a').questionFigure?.alt).toContain('every household description');
    expect(get('sc-q2ai').questionFigure?.alt).toContain('arms and shoes');
    expect(get('sb-q1d').figure?.alt).toContain('aligned food sources');
    expect(get('sc-q1aii').figure?.alt).toContain('non-renewable sources of energy were also accepted');
  });
  it('prices independent meat asks and complete protein, preservation and appliance profiles', () => {
    expect([get('sb-q2b-factors').totalMarks, get('sb-q2b-methods').totalMarks]).toEqual([9, 6]);
    expect(get('sb-q2b-factors').questionText).not.toContain('tenderising');
    expect(get('sb-q2b-methods').questionText).toContain('two methods of tenderising');
    expect(get('sb-q1d').rows.map(r => r.marks)).toEqual([12, 12, 8, 5, 5, 5]);
    expect(get('sb-q1d').rows[2].contextNote).toContain('Lysine ↑');
    expect(get('sb-q2c').rows.map(r => r.marks)).toEqual([2, 9, 4]);
    expect(get('sb-q2c').rows[0].group?.options).toHaveLength(6);
    expect(get('sb-q2c').rows[1].contextNote).toContain('Dehydration');
    expect(get('sb-q4b').rows.map(r => r.marks)).toEqual([8, 12, 6]);
    expect(get('sb-q3b').rows.map(r => r.marks)).toEqual([9, 9, 2]);
  });
  it('preserves linked HACCP, insulation and wall-finish quotas plus energy allowance', () => {
    expect(get('sb-q3a').rows.map(r => r.marks)).toEqual([4, 4, 16]);
    expect(get('sb-q3a').rows[0].contextNote).toContain('Corresponding control measures');
    expect(get('sb-q3a').rows[2].contextNote).toContain('Four ADDITIONAL');
    expect(get('sc-q1ai').taskGroups?.map(g => g.marks)).toEqual([8, 8, 8]);
    expect(get('sc-q1bii').taskGroups?.map(g => g.marks)).toEqual([7, 7]);
    const energy = get('sc-q1aii');
    expect(energy.answerVariants).toHaveLength(6);
    expect(energy.rows.map(r => r.marks)).toEqual([2, 3, 6, 3]);
    for (const variant of energy.answerVariants ?? []) for (const row of variant.rows) expect(row.contextNote).toContain('NON-RENEWABLE');
    expect(energy.answerVariants?.at(-1)?.label).toContain('non-renewable');
  });
  it('keeps complete design/education continuations, source gaps and family headings', () => {
    expect(get('sc-q2aii').rows[0].contextNote).toContain('Pattern -');
    expect(get('sc-q2bii').rows[0].contextNote).toContain('ONE finish');
    expect(get('sc-q2bii').rows[0].contextNote).toContain('no name mark');
    expect(get('sc-q2cii').rows[1].contextNote).toContain('no name/work pairing');
    expect(get('sc-q3aiii').rows.map(r => r.marks)).toEqual([4, 6]);
    expect(get('sc-q3aiii').rows[0].group?.options).toContain('DARE');
    expect(get('sc-q3aiii').rows[1].contextNote).toContain('receive on-going support in college');
    expect(get('sc-q3b').rows.map(r => r.marks)).toEqual([10, 10, 10]);
    expect([get('sb-q5bi').totalMarks, get('sb-q5bii').totalMarks]).toEqual([15, 10]);
    expect(get('sb-q5bii').rows[0].contextNote).toContain('2 different state interventions');
  });
  it('preserves twenty original Atlas identities and maps every canonical topic', () => {
    expect(anchors.q.map(q => q.n)).toEqual(Array.from({ length: 20 }, (_, i) => String(i + 1)));
    expect(anchors.q.find(q => q.n === '13')!.region.map(r => r.p)).toEqual([8, 9, 10]);
    expect(anchors.q.find(q => q.n === '18')!.region.map(r => r.p)).toEqual([19, 20, 21]);
    expect(anchors.q.find(q => q.n === '19')!.region.map(r => r.p)).toEqual([22, 23, 24]);
    expect(anchors.q.find(q => q.n === '20')!.region.map(r => r.p)).toEqual([25, 26, 27]);
    for (const q of anchors.q) expect(q.pY[1]).toBeGreaterThan(q.pY[0]);
    const file = 'LC098ALP000EV.pdf';
    const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'home-economics-s-and-s' && p.year === 2014 && p.level === 'higher' && p.lang === 'ev' && p.fileid === file)!;
    for (const c of all) {
      const m = c.questionRef.match(/Section ([ABC]) (?:E\d )?Q(\d+)/)!;
      const n = String(Number(m[2]) + (m[1] === 'A' ? 0 : m[1] === 'B' ? 12 : 17));
      const row = runtime.questionMappings.find(q => q[0] === 'h' && q[1] === 'e' && q[2] === 2014 && q[4] === file && q[5] === n)!;
      expect(row, c.id).toBeDefined();
      expect((row[6] as number[]).map(i => runtime.topicIds[i]).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
      expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === n)!).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
    }
  });
});
