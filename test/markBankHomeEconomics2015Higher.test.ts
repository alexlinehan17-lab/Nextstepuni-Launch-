import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/home-economics/higher';
import { tariffReconciles } from '../types/markBank';
import runtime from '../data/examTopics/home-economics-s-and-s-question-runtime.json';
import crosswalk from '../data/examTopics/home-economics-s-and-s-curriculum-crosswalk.json';
import anchors from '../scripts/paper-trail/answers/2015/LC098ALP000EV.pdf.json';
import review from '../scripts/markbank/authoring/home-economics/2015-hl-main-review.json';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
const all = CARDS.filter(c => c.id.startsWith('he-2015-hl-'));
const get = (id: string) => {
  const c = all.find(c => c.id === `he-2015-hl-${id}`);
  if (!c || c.kind !== 'question') throw new Error(id);
  return c;
};
describe('2015 Higher Home Economics: independently swept original sources', () => {
  it('retains all 48 priced tasks and the 627 offered marks', () => {
    expect(all).toHaveLength(48);
    expect(all.map(c => c.id).sort()).toEqual(review.tasks.map(c => c.id).sort());
    expect(['sa', 'sb', 'sc'].map(s => all.filter(c => c.id.includes(`-${s}-`)).length)).toEqual([12, 17, 19]);
    expect(all.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(627);
    for (const c of all) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
      for (const v of c.answerVariants ?? []) expect(tariffReconciles({ ...c, rows: v.rows }), `${c.id}/${v.id}`).toBe(true);
    }
  });
  it('keeps whole-six A tariffs, complete companion asks and printed choice pools', () => {
    for (let n = 1; n <= 12; n++) {
      const c = get(`sa-q${n}`);
      expect(c.tariffModel?.kind).toBe('questionTotal');
      expect(c.rows.every(r => r.marks === null && !r.permittedMarks && !r.parts)).toBe(true);
      expect(c.rows[0].contextNote).toContain('no per-answer allocation');
    }
    expect(get('sa-q2').rows).toHaveLength(3);
    expect(get('sa-q2').figure?.alt).toContain('example/food-source associations');
    expect(get('sa-q7').rows).toHaveLength(6);
    expect(get('sa-q7').rows[0].contextNote).toContain('any TWO classes');
    expect(get('sa-q8').rows).toHaveLength(3);
    expect(get('sa-q8').rows[0].contextNote).toContain('ANY TWO');
    expect(get('sa-q9').questionText).toContain('List the three components');
    expect(get('sa-q11').rows[0].contextNote).toContain('retained as printed');
    expect(get('sa-q6').topicId).toBe('home-economics-0-2');
  });
  it('retains all ten complete original question and model figures', () => {
    expect(Object.keys(review.figures)).toHaveLength(10);
    expect(new Set(all.flatMap(c => c.kind === 'question' && c.questionFigure ? [c.questionFigure.src] : [])).size).toBe(5);
    expect(new Set(all.flatMap(c => c.kind === 'question' && c.figure ? [c.figure.src] : [])).size).toBe(5);
    expect(get('sb-q1a').questionFigure?.alt).toContain('all nine food/drink categories');
    expect(get('sb-q4b').figure?.alt).toContain('underlined compulsory Housing, Food and Savings');
    expect(get('sb-q4c').figure?.alt).toContain('six-model');
    expect(get('sc-q1aii').figure?.alt).toContain('matching example/use pairs');
  });
  it('keeps shared tariffs coherent, independent romans priced and complete egg choices', () => {
    expect(get('sb-q1a').rows.map(r => r.marks)).toEqual([8, 8, 8]);
    expect(get('sb-q1a').rows[2].contextNote).toContain('no fixed three-per-heading quota');
    expect(get('sb-q1a').rows[1].contextNote).toContain('Biscuits, cakes and pastries');
    expect([get('sb-q1ci').totalMarks, get('sb-q1cii').totalMarks]).toEqual([6, 12]);
    expect(get('sb-q2a').totalMarks).toBe(40);
    expect(get('sb-q2a').taskGroups?.map(g => g.marks)).toEqual([24, 8, 8]);
    expect(get('sb-q2a').rows[3].group?.options).toEqual(['Coagulation', 'Aeration', 'Emulsification']);
    expect([get('sb-q5ai').totalMarks, get('sb-q5aii').totalMarks]).toEqual([5, 16]);
    for (const part of ['ai', 'aii', 'b', 'c']) expect(get(`sb-q5${part}`).topicId).toBe('home-economics-2-1');
  });
  it('preserves matching mould methods, required budget areas and historical savings profiles', () => {
    const mould = get('sb-q3b');
    expect(mould.answerVariants).toHaveLength(5);
    expect(mould.rows.map(r => r.marks)).toEqual([4, 6, 12]);
    expect(mould.answerVariants?.find(v => v.label === 'Mucor')?.rows[2].contextNote).toContain('Sexual reproduction:');
    expect(mould.answerVariants?.find(v => v.label === 'Penicillium')?.rows[2].contextNote).not.toContain('Sexual reproduction:');
    expect(mould.answerVariants?.find(v => v.label === 'Penicillium')?.rows[1].contextNote).toContain('20°C');
    expect(get('sb-q4b').rows.map(r => r.id)).toEqual(['housing', 'food', 'savings', 'other']);
    expect(get('sb-q4b').rows.map(r => r.marks)).toEqual([3, 3, 3, 9]);
    expect(get('sb-q4b').questionText).toContain('€650');
    const savings = get('sb-q4c');
    expect(savings.answerVariants).toHaveLength(7);
    expect(savings.rows.map(r => r.marks)).toEqual([2, 3, 3, 3, 3]);
    for (const v of savings.answerVariants?.slice(0, 6) ?? []) expect(v.rows[2].contextNote).toContain('Historical 2015');
  });
  it('keeps compulsory elective points, missing source models and complete continuation profiles', () => {
    expect(get('sc-q1aii').rows.map(r => r.marks)).toEqual([8, 2, 8, 2]);
    expect(get('sc-q1ci').rows.map(r => r.id)).toEqual(['service-pipe', 'stopcock', 'other']);
    expect(get('sc-q1ci').rows.map(r => r.marks)).toEqual([3, 3, 9]);
    expect(get('sc-q2ai').rows.map(r => r.marks)).toEqual([5, 4]);
    expect(get('sc-q2ai').rows[0].contextNote).toContain('without a model drawing');
    expect(get('sc-q2aii').rows.map(r => r.marks)).toEqual([4, 2, 2, 2, 2, 4]);
    expect(get('sc-q2aii').rows[2].contextNote).toContain('no reason models');
    expect(get('sc-q2aii').rows[3].contextNote).toContain('Required underlined stage');
    expect(get('sc-q2b').answerVariants).toHaveLength(5);
    expect(get('sc-q2b').answerVariants?.find(v => v.label === 'Silk')?.rows[1].contextNote).toContain('mulberry leaves');
    expect(get('sc-q3ai').rows.map(r => r.marks)).toEqual([4, 4, 12]);
    expect(get('sc-q3aiii').rows[0].group?.options).toHaveLength(6);
    expect(get('sc-q3aiii').topicId).toBe('home-economics-3-9');
    expect(get('sc-q3cii').taskGroups?.map(g => g.marks)).toEqual([6, 6]);
  });
  it('preserves twenty original Atlas identities and maps every canonical topic', () => {
    expect(anchors.q.map(q => q.n)).toEqual(Array.from({ length: 20 }, (_, i) => String(i + 1)));
    expect(anchors.q.find(q => q.n === '13')!.region.map(r => r.p)).toEqual([8, 9, 10]);
    expect(anchors.q.find(q => q.n === '18')!.region.map(r => r.p)).toEqual([16, 17, 18]);
    expect(anchors.q.find(q => q.n === '19')!.region.map(r => r.p)).toEqual([19, 20]);
    expect(anchors.q.find(q => q.n === '20')!.region.map(r => r.p)).toEqual([21, 22, 23]);
    for (const q of anchors.q) expect(q.pY[1]).toBeGreaterThan(q.pY[0]);
    const file = 'LC098ALP000EV.pdf';
    const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'home-economics-s-and-s' && p.year === 2015 && p.level === 'higher' && p.lang === 'ev' && p.fileid === file)!;
    for (const c of all) {
      const m = c.questionRef.match(/Section ([ABC]) (?:E\d )?Q(\d+)/)!;
      const n = String(Number(m[2]) + (m[1] === 'A' ? 0 : m[1] === 'B' ? 12 : 17));
      const row = runtime.questionMappings.find(q => q[0] === 'h' && q[1] === 'e' && q[2] === 2015 && q[4] === file && q[5] === n)!;
      expect(row, c.id).toBeDefined();
      expect((row[6] as number[]).map(i => runtime.topicIds[i]).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
      expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === n)!).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
    }
  });
});
