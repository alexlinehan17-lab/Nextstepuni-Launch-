import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/home-economics/higher';
import { CARD_ID_ALIASES } from '../components/MarkBank/cardAliases';
import { tariffReconciles } from '../types/markBank';
import runtime from '../data/examTopics/home-economics-s-and-s-question-runtime.json';
import crosswalk from '../data/examTopics/home-economics-s-and-s-curriculum-crosswalk.json';
import anchors from '../scripts/paper-trail/answers/2022/LC098ALP039EV.pdf.json';
import review from '../scripts/markbank/authoring/home-economics/2022-hl-main-review.json';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';

const get = (id: string) => {
  const c = CARDS.find(c => c.id === `he-2022-hl-${id}`);
  if (!c || c.kind !== 'question') throw new Error(id);
  return c;
};
const sitting = CARDS.filter(c => c.year === 2022 && !c.id.includes('deferred'));

describe('2022 Higher Home Economics full source review', () => {
  it('retains every reviewed response and the tariff of each open route', () => {
    expect(sitting).toHaveLength(62);
    expect(sitting.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(749);
    expect(sitting.map(c => c.id).sort()).toEqual(review.tasks.map(c => c.id).sort());
    for (const [section, count, marks] of [['A', 17, 84], ['B', 17, 280], ['C', 28, 385]] as const) {
      const cards = sitting.filter(c => c.questionRef.includes(`Section ${section} `));
      expect(cards).toHaveLength(count);
      expect(cards.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(marks);
    }
    for (const c of sitting) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
      for (const v of c.answerVariants ?? []) expect(tariffReconciles({ ...c, rows: v.rows }), `${c.id}/${v.id}`).toBe(true);
    }
  });
  it('splits only the separately practicable prompts while preserving their marks', () => {
    for (const [id, extra, a, b] of [['sa-q1', 'absorption', 4, 2], ['sa-q3', 'example', 4, 2], ['sa-q6', 'advantage', 4, 2], ['sb-q5c', 'procedure', 4, 10]] as const) {
      expect(get(id).totalMarks).toBe(a);
      expect(get(`${id}-${extra}`).totalMarks).toBe(b);
      expect(get(id).questionRef).not.toBe(get(`${id}-${extra}`).questionRef);
    }
    expect(get('sa-q1').rows[0].parts?.map(p => p.permittedMarks)).toEqual([[0, 1, 2], [0, 1, 2]]);
    expect(get('sa-q3').rows[0].parts?.map(p => p.permittedMarks)).toEqual([[0, 2], [0, 2]]);
    expect(get('sa-q2').questionText).toContain('Pancreatic juice');
    expect(get('sa-q2').questionText).not.toContain('Amylase');
    expect(get('sa-q2').rows.map(r => r.verbatim)).toEqual(['Amylase', 'Starch', 'Maltose']);
    expect(get('sa-q14').questionFigure?.src).toContain('2022-hl-sa-q14-symbols.png');
  });
  it('restores the missing mould name and characteristics on the original identity', () => {
    const c = get('sb-q3b-conditions');
    expect(c.totalMarks).toBe(23);
    expect(c.questionText).toContain('characteristics/description');
    expect(c.answerVariants?.map(v => v.label)).toEqual(['Mucor', 'Rhizopus', 'Penicillium', 'Aspergillus', 'Another valid mould']);
    for (const v of c.answerVariants ?? []) {
      expect(v.rows.map(r => r.marks)).toEqual([2, 9, 12]);
      expect(v.rows[1].parts?.map(p => p.permittedMarks)).toEqual(Array(3).fill([0, 3]));
      expect(v.rows[2].parts?.map(p => p.permittedMarks)).toEqual(Array(4).fill([0, 1, 2, 3]));
    }
    expect(c.answerVariants?.[3].rows[1].contextNote).toContain('black or green mould');
  });
  it('keeps every food-manufacture route and exact required nutrition criteria', () => {
    expect(get('sb-q1a').questionFigure?.src).toContain('2022-hl-sb-q1a-chart.png');
    expect(get('sb-q1a').questionFigure?.alt).toContain('advertising 25; other 3');
    expect(get('sb-q1c').rows.map(r => r.marks)).toEqual([8, 6, 6]);
    expect(get('sb-q2a').rows.map(r => r.marks)).toEqual([2, 4, 2, 4, 2, 4]);
    expect(get('sb-q2b').answerVariants?.map(v => v.label)).toContain('Miso');
    expect(get('sb-q2b').answerVariants).toHaveLength(8);
    expect(get('sb-q2c').rows[0].contextNote).toContain('smallest possible effective quantity');
    expect(get('sb-q5c').topicId).toBe('home-economics-2-1');
  });
  it('consolidates the full floor-covering profile without losing old progress', () => {
    const c = get('sc-q1aii');
    expect(c.totalMarks).toBe(20);
    expect(CARD_ID_ALIASES['he-2022-hl-sc-q1aii-properties']).toBe(c.id);
    expect(sitting.some(c => c.id.endsWith('q1aii-properties'))).toBe(false);
    expect(c.answerVariants).toHaveLength(10);
    for (const v of c.answerVariants ?? []) expect(v.rows.map(r => r.marks)).toEqual([2, 12, 6]);
    const wood = c.answerVariants?.find(v => v.label === 'Wood')!;
    expect(wood.rows[0].contextNote).toContain('oak, beech maple');
    expect(wood.rows[2].contextNote).toContain('marked and scratched easily');
    expect(c.answerVariants?.find(v => v.label === 'Cork')?.rows[2].contextNote).toContain('porous so will stain if not sealed');
    expect(c.answerVariants?.find(v => v.label === 'Carpet')?.rows[0].contextNote).toContain('Woven/ hessian backed');
    expect(c.answerVariants?.find(v => v.label === 'Carpet')?.rows[2].contextNote).toContain('Good insulator');
  });
  it('preserves complete elective profiles, open pairs and source clarifications', () => {
    expect(get('sc-q2ai').questionFigure?.src).toContain('2022-hl-sc-q2ai-outfits.png');
    expect(get('sc-q2bii').rows.map(r => r.marks)).toEqual([3, 6]);
    expect(get('sc-q3aii').rows.map(r => r.marks)).toEqual([4, 4, 4, 8]);
    expect(get('sc-q3aiv').rows[0].contextNote).toContain('Local Enterprise Offices');
    expect(get('sc-q3bii').rows.map(r => r.marks)).toEqual([1, 2, 2, 4, 1, 2, 2, 4]);
    expect(get('sc-q3bii').taskGroups?.map(g => g.marks)).toEqual([9, 9]);
    expect(get('sc-q3cii').rows.map(r => r.marks)).toEqual([3, 4, 3, 4]);
    expect(get('sc-q4aii').answerVariants).toHaveLength(6);
    expect(get('sc-q4aii').answerVariants?.[1].rows[1].contextNote).toContain('validated pressure-canning process');
    expect(get('sc-q4ci').rows.map(r => r.marks)).toEqual([2, 6, 6, 4]);
    expect(get('sc-q4ci').rows[2].contextNote).toContain('electrical resistance converts electrical energy');
  });
  it('retains all scheme continuation pages under distinct B/C question IDs', () => {
    expect(anchors.q.map(q => q.n)).toEqual(['1', '2', '3', '4', '5', '6', '7', '8', '9']);
    for (const [n, pages] of [['1', [11, 12]], ['2', [13, 14]], ['6', [18, 19, 20, 21]], ['8', [24, 25, 26, 27]], ['9', [28, 29, 30]]] as const) {
      expect(anchors.q.find(q => q.n === n)?.region.map(r => r.p)).toEqual(pages);
    }
  });
  it('maps every card to its own Atlas question and canonical topic', () => {
    for (const c of sitting) {
      const m = c.questionRef.match(/Section ([ABC]) (?:E\d )?Q(\d+)/)!;
      const file = m[1] === 'A' ? 'LC098ALP014EV.pdf' : 'LC098ALP039EV.pdf';
      const n = String(Number(m[2]) + (m[1] === 'C' ? 5 : 0));
      const row = runtime.questionMappings.find(q => q[0] === 'h' && q[1] === 'e' && q[2] === 2022 && q[4] === file && q[5] === n)!;
      expect(row, c.id).toBeDefined();
      expect((row[6] as number[]).map(i => runtime.topicIds[i]).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
      const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'home-economics-s-and-s' && p.year === 2022 && p.level === 'higher' && p.lang === 'ev' && p.fileid === file)!;
      expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === n)!).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
    }
  });
});
