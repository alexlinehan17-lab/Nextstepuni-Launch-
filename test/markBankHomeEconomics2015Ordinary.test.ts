import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/home-economics/ordinary';
import { tariffReconciles } from '../types/markBank';
import runtime from '../data/examTopics/home-economics-s-and-s-question-runtime.json';
import crosswalk from '../data/examTopics/home-economics-s-and-s-curriculum-crosswalk.json';
import anchors from '../scripts/paper-trail/answers/2015/LC098GLP000EV.pdf.json';
import review from '../scripts/markbank/authoring/home-economics/2015-ol-main-review.json';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
const all = CARDS.filter(c => c.id.startsWith('he-2015-ol-'));
const get = (id: string) => {
  const c = all.find(c => c.id === `he-2015-ol-${id}`);
  if (!c || c.kind !== 'question') throw new Error(id);
  return c;
};
describe('2015 Ordinary Home Economics: independently swept original sources', () => {
  it('retains all 51 priced tasks and 627 offered marks', () => {
    expect(all).toHaveLength(51);
    expect(all.map(c => c.id).sort()).toEqual(review.tasks.map(c => c.id).sort());
    expect(['sa', 'sb', 'sc'].map(s => all.filter(c => c.id.includes(`-${s}-`)).length)).toEqual([12, 19, 20]);
    expect(all.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(627);
    for (const c of all) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
      for (const v of c.answerVariants ?? []) expect(tariffReconciles({ ...c, rows: v.rows }), `${c.id}/${v.id}`).toBe(true);
    }
  });
  it('preserves whole-six tariffs, complete companions and closed A choices', () => {
    for (let n = 1; n <= 12; n++) {
      const c = get(`sa-q${n}`);
      expect(c.tariffModel?.kind).toBe('questionTotal');
      expect(c.rows.every(r => r.marks === null && !r.permittedMarks && !r.parts)).toBe(true);
      expect(c.rows[0].contextNote).toContain('no per-answer allocation');
    }
    expect(get('sa-q1').rows.map(r => r.verbatim)).toEqual(['Calcium causes weak bones and teeth. — False', 'Calcium is required for blood clotting. — True', 'Calcium is necessary for normal muscle contraction. — True']);
    expect(get('sa-q2').rows.map(r => r.verbatim)).toEqual(['coagulate', 'maillard reaction', 'opaque']);
    expect(get('sa-q7').rows.map(r => r.verbatim)).toEqual(['Hard cheese — Parmesan', 'Soft cheese — mozzarella', 'Processed cheese — cheese slices']);
    expect(get('sa-q3').topicId).toBe('home-economics-0-10');
    expect(get('sb-q2c').topicId).toBe('home-economics-0-1');
    expect(get('sa-q4').rows).toHaveLength(4);
    expect(get('sa-q8').questionText).toContain('Name two materials');
    expect(get('sa-q10').rows[2].contextNote).toContain('ONE of the TWO credit types');
    expect(get('sa-q11').questionText).toContain('Name one shopper loyalty scheme');
    expect(get('sa-q12').rows[2].contextNote).toContain('historical 2015');
    expect(get('sa-q9').questionText).toContain('[blank] of a fabric');
  });
  it('keeps all six original figures and every table/plan input', () => {
    expect(Object.keys(review.figures)).toHaveLength(6);
    expect(new Set(all.flatMap(c => c.kind === 'question' && c.questionFigure ? [c.questionFigure.src] : [])).size).toBe(6);
    expect(get('sb-q1b').questionFigure?.alt).toContain('Beef, Chicken, Liver and Pork');
    expect(get('sc-q1ai-evaluation').questionFigure?.alt).toContain('all four bedrooms');
    expect(get('sc-q1ai-modifications').questionFigure?.src).toBe(get('sc-q1ai-evaluation').questionFigure?.src);
    expect(get('sc-q3ai').questionFigure?.alt).toContain('1,500/1,777/1,064/3,299');
  });
  it('keeps shared fish tariffs coherent and separately allocated asks priced', () => {
    expect([get('sb-q1ci').totalMarks, get('sb-q1cii').totalMarks]).toEqual([24, 4]);
    expect(get('sb-q1ci').rows.map(r => r.marks)).toEqual([12, 8, 4]);
    expect([get('sb-q2ai').totalMarks, get('sb-q2aii').totalMarks]).toEqual([10, 10]);
    expect(get('sb-q3a').rows.map(r => r.marks)).toEqual([6, 6, 12]);
    expect(get('sb-q3a').rows[2].contextNote).toContain('without a fabricated 12/12 split');
    expect([get('sb-q3b-methods').totalMarks, get('sb-q3b-explanation').totalMarks]).toEqual([12, 8]);
    expect(get('sb-q3b-methods').rows[0].group?.options).toHaveLength(11);
    expect(get('sb-q3b-explanation').answerVariants).toHaveLength(10);
    expect(get('sb-q3b-explanation').answerVariants?.find(v => v.label === 'Poaching')?.rows[0].contextNote).toContain('85°C');
    expect(get('sb-q3b-explanation').rows[0].contextNote).toContain('ONE of the THREE methods');
    expect(get('sb-q1d').rows.map(r => r.marks)).toEqual([5, 5, 10]);
    expect(get('sb-q2b').rows.map(r => r.marks)).toEqual([6, 6, 6]);
  });
  it('preserves linked appliance/payment/family choices without extra name prices', () => {
    expect(get('sb-q4a').rows.map(r => r.marks)).toEqual([4, 4, 9, 9]);
    expect(get('sb-q4a').rows[0].group?.options).toHaveLength(6);
    expect(get('sb-q4a').rows[1].contextNote).toContain('food processor');
    expect(get('sb-q4b').answerVariants).toHaveLength(6);
    expect(get('sb-q4b').rows.map(r => r.marks)).toEqual([6, 6]);
    expect(get('sb-q5a').rows.map(r => r.marks)).toEqual([7, 7, 7, 7]);
    expect(get('sc-q1aii').rows[0].contextNote).toContain('no name/description subprice');
    expect(get('sc-q3ci').rows[0].contextNote).toContain('no invented name/description split');
  });
  it('retains elective splits, same-choice context, flexible quotas and visible model gaps', () => {
    expect([get('sc-q1ai-evaluation').totalMarks, get('sc-q1ai-modifications').totalMarks]).toEqual([15, 10]);
    expect(get('sc-q1bii').taskGroups?.map(g => g.marks)).toEqual([9, 9]);
    expect(get('sc-q1bii').rows[1].contextNote).toContain('no item-specific description models');
    expect(get('sc-q1cii').questionText).toContain('overflow pipe');
    expect(get('sc-q2ai').rows.map(r => r.marks)).toEqual([6, 4]);
    expect(get('sc-q2ai').rows[0].contextNote).toContain('without a worked drawing');
    expect(get('sc-q2aii').stem).toContain('Sketch and describe');
    expect(get('sc-q2b').answerVariants).toHaveLength(3);
    expect(get('sc-q2b').rows.map(r => r.marks)).toEqual([3, 3, 3, 3, 3]);
    expect(get('sc-q2b').answerVariants?.find(v => v.label === 'Polyester')?.rows[2].contextNote).toContain('drip dries quickly');
    expect(get('sc-q3aiii').rows[0].group?.options).toHaveLength(8);
    expect(get('sc-q3aiii').rows[1].contextNote).toContain('anger management programmes');
    expect(get('sc-q3bi').rows.map(r => r.marks)).toEqual([5, 5, 5, 5]);
    expect(get('sc-q3cii').rows[0].group?.options).toHaveLength(6);
    expect(get('sc-q3cii').rows[1].contextNote).toContain('named without model details');
  });
  it('preserves twenty original Atlas identities and maps every canonical topic', () => {
    expect(anchors.q.map(q => q.n)).toEqual(Array.from({ length: 20 }, (_, i) => String(i + 1)));
    expect(anchors.q.find(q => q.n === '13')!.region.map(r => r.p)).toEqual([7, 8]);
    expect(anchors.q.find(q => q.n === '18')!.region.map(r => r.p)).toEqual([13, 14]);
    expect(anchors.q.find(q => q.n === '19')!.region.map(r => r.p)).toEqual([15, 16]);
    expect(anchors.q.find(q => q.n === '20')!.region.map(r => r.p)).toEqual([17, 18, 19]);
    for (const q of anchors.q) expect(q.pY[1]).toBeGreaterThan(q.pY[0]);
    const file = 'LC098GLP000EV.pdf';
    const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'home-economics-s-and-s' && p.year === 2015 && p.level === 'ordinary' && p.lang === 'ev' && p.fileid === file)!;
    for (const c of all) {
      const m = c.questionRef.match(/Section ([ABC]) (?:E\d )?Q(\d+)/)!;
      const n = String(Number(m[2]) + (m[1] === 'A' ? 0 : m[1] === 'B' ? 12 : 17));
      const row = runtime.questionMappings.find(q => q[0] === 'o' && q[1] === 'e' && q[2] === 2015 && q[4] === file && q[5] === n)!;
      expect(row, c.id).toBeDefined();
      expect((row[6] as number[]).map(i => runtime.topicIds[i]).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
      expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === n)!).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
    }
  });
});
