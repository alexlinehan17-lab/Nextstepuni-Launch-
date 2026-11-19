import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/home-economics/ordinary';
import { groupMarks, tariffReconciles } from '../types/markBank';
import runtime from '../data/examTopics/home-economics-s-and-s-question-runtime.json';
import crosswalk from '../data/examTopics/home-economics-s-and-s-curriculum-crosswalk.json';
import anchors from '../scripts/paper-trail/answers/2018/LC098GLP000EV.pdf.json';
import review from '../scripts/markbank/authoring/home-economics/2018-ol-main-review.json';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
const all = CARDS.filter(c => c.id.startsWith('he-2018-ol-'));
const get = (id: string) => {
  const c = all.find(c => c.id === `he-2018-ol-${id}`);
  if (!c || c.kind !== 'question') throw new Error(id);
  return c;
};
describe('2018 Ordinary Home Economics: independently swept original sources', () => {
  it('retains all 53 priced tasks and 627 offered marks', () => {
    expect(all).toHaveLength(53);
    expect(all.map(c => c.id).sort()).toEqual(review.tasks.map(c => c.id).sort());
    expect(['sa', 'sb', 'sc'].map(s => all.filter(c => c.id.includes(`-${s}-`)).length)).toEqual([12, 20, 21]);
    expect(all.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(627);
    for (const c of all) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
      for (const v of c.answerVariants ?? []) expect(tariffReconciles({ ...c, rows: v.rows }), `${c.id}/${v.id}`).toBe(true);
    }
  });
  it('keeps every whole-six ask, tick column, cloze alternative and companion credit question', () => {
    for (let n = 1; n <= 12; n++) {
      const c = get(`sa-q${n}`);
      expect(c.tariffModel?.kind).toBe('questionTotal');
      expect(c.rows.every(r => r.marks === null && !r.permittedMarks && !r.parts)).toBe(true);
      expect(c.rows[0].contextNote).toContain('no per-answer allocation');
    }
    expect(get('sa-q1').rows.map(r => r.verbatim?.split(' — ')[1])).toEqual(['True', 'True', 'False']);
    expect(get('sa-q7').rows.map(r => r.verbatim?.split(' — ')[1])).toEqual(['True', 'False', 'True']);
    expect(get('sa-q2').rows.map(r => r.verbatim)).toEqual(['vitamin K', 'Vitamin B', 'folic acid']);
    expect(get('sa-q4').rows.map(r => r.verbatim)).toEqual(['Salmon — marine', 'Olive Oil — vegetable (plant)', 'Butter — animal']);
    expect(get('sa-q8').rows[1].verbatim).toContain('Enzymes/yeast');
    expect(get('sa-q8').rows[1].contextNote).toContain('Retain both alternatives');
    expect(get('sa-q10').questionText).toContain('Name two types of credit');
    expect(get('sa-q10').rows).toHaveLength(4);
    expect(get('sa-q11').rows.map(r => r.verbatim)).toEqual(['Hot Iron', 'Drip dry']);
    expect(get('sa-q12').rows[2].verbatim).toContain('smart refrigerators');
  });
  it('retains nine complete original inputs, all ingredients and all diagram labels', () => {
    expect(Object.keys(review.figures)).toHaveLength(9);
    expect(new Set(all.flatMap(c => c.kind === 'question' && c.questionFigure ? [c.questionFigure.src] : [])).size).toBe(9);
    expect(get('sa-q2').questionFigure?.alt).toContain('all three offered words');
    expect(get('sa-q8').questionFigure?.alt).toContain('all three blank statements');
    expect(get('sa-q11').questionFigure?.alt).toContain('hot iron and drip dry');
    expect(get('sb-q1ai').questionFigure?.alt).toContain('seven nutrition lines');
    expect(get('sc-q1ai').questionFigure?.alt).toContain('overflow pipe and stopcock');
    expect(get('sc-q2ai').questionFigure?.alt).toContain('three primary-school uniforms');
    expect(get('sb-q1ai').stem).not.toContain('121 kcal');
  });
  it('preserves paired accompaniment, protein continuation, shared osteoporosis tariff and whole meals', () => {
    expect(get('sb-q1aii').rows.map(r => r.marks)).toEqual([2, 3]);
    expect(get('sb-q1aii').rows[1].contextNote).toContain('SAME accompaniment');
    expect(get('sb-q1b').rows.map(r => r.marks)).toEqual([8, 12, 6]);
    expect(get('sb-q1b').rows[2].contextNote).toContain('blood plasma');
    expect(get('sb-q1d').rows.map(r => r.marks)).toEqual([10, 10]);
    expect(get('sb-q2a').rows.map(r => r.marks)).toEqual([8, 8, 4]);
    expect(get('sb-q2a').rows[2].contextNote).toContain('no10/10 split');
    expect(get('sb-q2b').rows.map(r => r.marks)).toEqual([6, 6, 6]);
    for (const r of get('sb-q2b').rows) expect(r.permittedMarks).toEqual([0, 6]);
    expect(get('sb-q2c').rows[0].contextNote).toContain('no fixed heading quota');
  });
  it('keeps matched cereal products, separately priced consumer asks and both conflict tasks', () => {
    expect(get('sb-q3a').rows.map(r => r.marks)).toEqual([8, 8, 4]);
    expect(get('sb-q3b').rows[0].group?.options).toHaveLength(6);
    expect(get('sb-q3b').rows[1].contextNote).toContain('SAME THREE selected cereals');
    expect(get('sb-q3b').rows[1].contextNote).toContain('cornflakes');
    expect(get('sb-q3ci').totalMarks).toBe(6);
    expect(get('sb-q3cii').totalMarks).toBe(12);
    expect(get('sb-q4bi').totalMarks).toBe(5);
    expect(get('sb-q4bii').totalMarks).toBe(15);
    expect(get('sb-q4c').rows[0].contextNote).toContain('€2,000');
    expect(get('sb-q5c-definition').totalMarks).toBe(5);
    expect(get('sb-q5c-ways').totalMarks).toBe(10);
    expect(get('sb-q5c-definition').questionText).toBe('Explain generation conflict.');
    expect(get('sb-q5c-ways').questionText).toBe('Outline two ways of dealing with generation conflict.');
    expect(get('sb-q5c-definition').questionRef).not.toBe(get('sb-q5c-ways').questionRef);
  });
  it('keeps all elective requirements, paired alternatives and descending crest marks', () => {
    expect(get('sc-q1ai').rows.map(r => r.marks)).toEqual([6, 6, 6]);
    expect(get('sc-q1aii').rows.map(r => r.marks)).toEqual([4, 4, 4, 4]);
    expect(get('sc-q1aii').rows.map(r => r.verbatim)).toEqual(['Screening', 'Chlorination', 'Fluoridation', 'Testing']);
    expect(get('sc-q1ci').rows[0].contextNote).toContain('ergonomics');
    expect(get('sc-q1cii').rows.map(r => r.marks)).toEqual([6, 9]);
    expect(get('sc-q1cii').rows[0].group?.options).toHaveLength(7);
    expect(get('sc-q1cii').rows[1].contextNote).toContain('bedside lockers are accepted names only');
    expect(get('sc-q2ai').rows.map(r => r.marks)).toEqual([6, 6, 6]);
    const crest = get('sc-q2aii').rows[0].group!;
    expect(crest.options).toHaveLength(7);
    expect(crest.perOptionSteps).toEqual([4, 3]);
    expect([1, 2].map(claimMax => groupMarks({ ...crest, claimMax }))).toEqual([4, 7]);
    expect(get('sc-q2bii').answerVariants).toHaveLength(7);
    expect(get('sc-q2bii').rows.map(r => r.marks)).toEqual([3, 3]);
    expect(get('sc-q3aii').rows.map(r => r.marks)).toEqual([8, 8, 8]);
    expect(get('sc-q3aiv').rows.map(r => r.marks)).toEqual([4, 8]);
    expect(get('sc-q3aiv').rows[0].group?.options).toHaveLength(8);
    expect(get('sc-q3aiv').rows[1].contextNote).toContain('Safe Pass are accepted names only');
    expect(get('sc-q3bii').rows[0].contextNote).toContain('No separate category quota');
  });
  it('preserves twenty original Atlas identities and maps every canonical topic', () => {
    expect(anchors.q.map(q => q.n)).toEqual(Array.from({ length: 20 }, (_, i) => String(i + 1)));
    expect(anchors.q.find(q => q.n === '6')!.region.map(r => r.p)).toEqual([5]);
    expect(anchors.q.find(q => q.n === '13')!.region.map(r => r.p)).toEqual([8, 9]);
    expect(anchors.q.find(q => q.n === '18')!.region.map(r => r.p)).toEqual([14, 15, 16]);
    expect(anchors.q.find(q => q.n === '19')!.region.map(r => r.p)).toEqual([17, 18]);
    expect(anchors.q.find(q => q.n === '20')!.region.map(r => r.p)).toEqual([19, 20]);
    for (const q of anchors.q) expect(q.pY[1]).toBeGreaterThan(q.pY[0]);
    const file = 'LC098GLP000EV.pdf';
    const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'home-economics-s-and-s' && p.year === 2018 && p.level === 'ordinary' && p.lang === 'ev' && p.fileid === file)!;
    for (const c of all) {
      const m = c.questionRef.match(/Section ([ABC]) (?:E\d )?Q(\d+)/)!;
      const n = String(Number(m[2]) + (m[1] === 'A' ? 0 : m[1] === 'B' ? 12 : 17));
      const row = runtime.questionMappings.find(q => q[0] === 'o' && q[1] === 'e' && q[2] === 2018 && q[4] === file && q[5] === n)!;
      expect(row, c.id).toBeDefined();
      expect((row[6] as number[]).map(i => runtime.topicIds[i]).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
      expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === n)!).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
    }
  });
});
