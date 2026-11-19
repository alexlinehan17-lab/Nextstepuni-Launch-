import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/home-economics/higher';
import { tariffReconciles } from '../types/markBank';
import runtime from '../data/examTopics/home-economics-s-and-s-question-runtime.json';
import crosswalk from '../data/examTopics/home-economics-s-and-s-curriculum-crosswalk.json';
import anchors from '../scripts/paper-trail/answers/2016/LC098ALP000EV.pdf.json';
import review from '../scripts/markbank/authoring/home-economics/2016-hl-main-review.json';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
const all = CARDS.filter(c => c.id.startsWith('he-2016-hl-'));
const get = (id: string) => {
  const c = all.find(c => c.id === `he-2016-hl-${id}`);
  if (!c || c.kind !== 'question') throw new Error(id);
  return c;
};
describe('2016 Higher Home Economics: independently swept original sources', () => {
  it('retains all 53 priced tasks and the 627 offered marks', () => {
    expect(all).toHaveLength(53);
    expect(all.map(c => c.id).sort()).toEqual(review.tasks.map(c => c.id).sort());
    expect(['sa', 'sb', 'sc'].map(s => all.filter(c => c.id.includes(`-${s}-`)).length)).toEqual([12, 17, 24]);
    expect(all.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(627);
    for (const c of all) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
      for (const v of c.answerVariants ?? []) expect(tariffReconciles({ ...c, rows: v.rows }), `${c.id}/${v.id}`).toBe(true);
    }
  });
  it('keeps whole-six A tariffs, all choice categories and complete companion questions', () => {
    for (let n = 1; n <= 12; n++) {
      const c = get(`sa-q${n}`);
      expect(c.tariffModel?.kind).toBe('questionTotal');
      expect(c.rows.every(r => r.marks === null && !r.permittedMarks && !r.parts)).toBe(true);
      expect(c.rows[0].contextNote).toContain('no per-answer allocation');
    }
    expect(get('sa-q3').rows).toHaveLength(3);
    expect(get('sa-q4').rows.some(r => r.verbatim.includes('brain, spinal cord and skeleton'))).toBe(true);
    expect(get('sa-q6').rows).toHaveLength(3);
    expect(get('sa-q6').rows[0].contextNote).toContain('ANY TWO of the THREE');
    expect(get('sa-q7').rows.map(r => r.verbatim)).toEqual(['A = vacuole', 'B = nucleus', 'C = granular cytoplasm/food vacuole/food reserve']);
    expect(get('sa-q8').rows).toHaveLength(4);
    expect(get('sa-q8').rows[2].contextNote).toContain('retained as printed');
    expect(get('sa-q9').rows.some(r => r.contextNote?.includes('no model description for Focus groups'))).toBe(true);
    expect(get('sa-q11').questionText).toContain('What information does the following label');
  });
  it('retains five complete original figures and every food contribution', () => {
    expect(Object.keys(review.figures)).toHaveLength(5);
    expect(new Set(all.flatMap(c => c.kind === 'question' && c.questionFigure ? [c.questionFigure.src] : [])).size).toBe(4);
    expect(new Set(all.flatMap(c => c.kind === 'question' && c.figure ? [c.figure.src] : [])).size).toBe(1);
    expect(get('sa-q7').questionFigure?.alt).toContain('original image attribution');
    expect(get('sb-q1a').questionFigure?.alt).toContain('both 18–64 and ≥65');
    expect(get('sb-q1a').rows[0].contextNote).toContain('FOUR foods');
    for (const name of ['Bread and rolls', 'Vegetables and vegetable dishes', 'Potatoes and potato products', 'Fruit and fruit juices', 'Breakfast cereals', 'Others']) expect(get('sb-q1a').rows[0].contextNote).toContain(name);
    expect(get('sb-q1a').rows[0].contextNote).toContain('Potato products');
    expect(get('sb-q1a').rows[0].parts).toHaveLength(4);
    expect(get('sb-q1d').figure?.alt).toContain('five-model');
  });
  it('retains coherent disease, vitamin and freezing profiles, and flexible required quotas', () => {
    const disease = get('sb-q1d');
    expect(disease.answerVariants).toHaveLength(9);
    expect(disease.rows.map(r => r.marks)).toEqual([1, 4, 4]);
    expect(disease.answerVariants?.find(v => v.label === 'Crohn’s disease')?.rows[1].contextNote).toContain('no accounts or symptom models');
    expect(get('sb-q1e').rows.map(r => r.marks)).toEqual([4, 4, 12]);
    expect(get('sb-q2a').rows.map(r => r.marks)).toEqual([8, 8, 4]);
    expect(get('sb-q2c').answerVariants?.map(v => v.label)).toEqual(['D3 – cholecalciferol', 'D2 – ergocalciferol']);
    expect(get('sb-q2c').rows.map(r => r.marks)).toEqual([1, 2, 6, 6]);
    expect(get('sb-q2c').answerVariants?.[1].rows[1].contextNote).toContain('fungi and yeast');
    const freezing = get('sb-q3b');
    expect(freezing.answerVariants).toHaveLength(5);
    expect(freezing.rows.map(r => r.marks)).toEqual([2, 9, 6, 3]);
    expect(freezing.answerVariants?.[3].rows[1].contextNote).toContain('perforated conveyor belt');
    expect(freezing.answerVariants?.[0].rows[3].contextNote).toContain('quick freezing:');
    expect(freezing.answerVariants?.[0].rows[3].contextNote).toContain('slow freezing:');
    expect(get('sb-q3c').rows.map(r => r.marks)).toEqual([6, 6, 6]);
    expect(get('sb-q4a').rows[0].contextNote).toContain('No separate quota');
    expect(get('sb-q4c').answerVariants).toHaveLength(6);
    expect(get('sb-q4c').answerVariants?.some(v => v.label === 'Small Claims Procedure')).toBe(true);
    expect(get('sb-q5b').rows.map(r => r.marks)).toEqual([6, 6, 6]);
  });
  it('preserves asymmetric planning tariffs and separately priced lighting tasks', () => {
    expect(get('sc-q1ai').rows.map(r => r.marks)).toEqual([8, 8, 8]);
    const planning = get('sc-q1aii');
    expect(planning.rows.map(r => r.marks)).toEqual([12, 2]);
    expect(planning.rows[0].parts?.every(p => JSON.stringify(p.permittedMarks) === '[0,4]')).toBe(true);
    expect(planning.rows[1].permittedMarks).toEqual([0, 2]);
    expect(get('sc-q1bii').answerVariants).toHaveLength(4);
    expect(get('sc-q1bii').rows.map(r => r.marks)).toEqual([3, 9, 6]);
    expect(get('sc-q1bii').answerVariants?.find(v => v.label === 'Solar heating')?.rows[1].contextNote).toContain('solar collectors');
    expect([get('sc-q1ci-principles').totalMarks, get('sc-q1ci-profile').totalMarks]).toEqual([9, 5]);
    expect(get('sc-q1ci-principles').questionText).not.toContain('name and describe');
    expect(get('sc-q1ci-profile').questionText).toContain('name and describe one type');
    expect(get('sc-q1ci-profile').answerVariants).toHaveLength(6);
    expect(get('sc-q1ci-principles').questionRef).not.toBe(get('sc-q1ci-profile').questionRef);
    expect(get('sc-q1cii').rows.map(r => r.marks)).toEqual([4, 4, 8]);
  });
  it('keeps dependent outfit context, all names and visible missing-model guidance', () => {
    expect(get('sc-q2aii').rows.map(r => r.marks)).toEqual([5, 4]);
    expect(get('sc-q2aii').rows[0].contextNote).toContain('without a worked sketch');
    expect(get('sc-q2aiii').stem).toContain('Sketch and design an outfit');
    expect(get('sc-q2bi').rows.map(r => r.marks)).toEqual([4, 1, 1]);
    expect(get('sc-q2bi').rows[1].group?.options).toEqual(['rayon', 'viscose', 'acetate', 'tri-acetate']);
    expect([get('sc-q2bii-colour').totalMarks, get('sc-q2bii-design').totalMarks]).toEqual([5, 4]);
    expect(get('sc-q2bii-colour').rows[0].contextNote).toContain('no worked descriptions');
    expect(get('sc-q2bii-design').rows[0].contextNote).toContain('appliqué');
    expect(get('sc-q2bii-colour').questionRef).not.toBe(get('sc-q2bii-design').questionRef);
    expect(get('sc-q2ci').rows[0].group?.options).toHaveLength(15);
    expect(get('sc-q2ci').rows[1].contextNote).toContain('no model account');
    expect(get('sc-q3aiv').rows[0].group?.options).toEqual(['Society of St Vincent de Paul', 'Focus Ireland', 'Simon Community']);
    expect(get('sc-q3aiv').rows[1].contextNote).toContain('no detailed model account');
    expect(get('sc-q3bi').rows.map(r => r.marks)).toEqual([6, 6, 6]);
    expect(get('sc-q3bii').answerVariants).toHaveLength(3);
    expect(get('sc-q3bii').answerVariants?.[1].rows[1].contextNote).toContain('September, January, April');
    expect(get('sc-q3cii').rows.map(r => r.marks)).toEqual([5, 5, 5]);
    expect(get('sc-q3cii').rows[2].contextNote).toContain('no fixed two-per-heading quota');
  });
  it('preserves twenty original Atlas identities and maps every canonical topic', () => {
    expect(anchors.q.map(q => q.n)).toEqual(Array.from({ length: 20 }, (_, i) => String(i + 1)));
    expect(anchors.q.find(q => q.n === '13')!.region.map(r => r.p)).toEqual([9, 10, 11, 12]);
    expect(anchors.q.find(q => q.n === '18')!.region.map(r => r.p)).toEqual([18, 19, 20]);
    expect(anchors.q.find(q => q.n === '19')!.region.map(r => r.p)).toEqual([21, 22]);
    expect(anchors.q.find(q => q.n === '20')!.region.map(r => r.p)).toEqual([23, 24, 25]);
    for (const q of anchors.q) expect(q.pY[1]).toBeGreaterThan(q.pY[0]);
    const file = 'LC098ALP000EV.pdf';
    const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'home-economics-s-and-s' && p.year === 2016 && p.level === 'higher' && p.lang === 'ev' && p.fileid === file)!;
    for (const c of all) {
      const m = c.questionRef.match(/Section ([ABC]) (?:E\d )?Q(\d+)/)!;
      const n = String(Number(m[2]) + (m[1] === 'A' ? 0 : m[1] === 'B' ? 12 : 17));
      const row = runtime.questionMappings.find(q => q[0] === 'h' && q[1] === 'e' && q[2] === 2016 && q[4] === file && q[5] === n)!;
      expect(row, c.id).toBeDefined();
      expect((row[6] as number[]).map(i => runtime.topicIds[i]).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
      expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === n)!).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
    }
  });
});
