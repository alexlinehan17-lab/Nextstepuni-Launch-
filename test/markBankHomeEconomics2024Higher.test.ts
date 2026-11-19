import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/home-economics/higher';
import { CARD_ID_ALIASES } from '../components/MarkBank/cardAliases';
import { tariffReconciles } from '../types/markBank';
import runtime from '../data/examTopics/home-economics-s-and-s-question-runtime.json';
import crosswalk from '../data/examTopics/home-economics-s-and-s-curriculum-crosswalk.json';
import anchors from '../scripts/paper-trail/answers/2024/LC098ALP039EV.pdf.json';
import review from '../scripts/markbank/authoring/home-economics/2024-hl-main-review.json';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
const get = (id: string) => {
  const c = CARDS.find(c => c.id === `he-2024-hl-${id}`);
  if (!c || c.kind !== 'question') throw new Error(id);
  return c;
};
const sitting = CARDS.filter(c => c.year === 2024 && !c.id.includes('deferred'));
describe('2024 Higher Home Economics full source review', () => {
  it('retains every independently reviewed boundary and reconciles each answer route', () => {
    expect(sitting.map(c => c.id).sort()).toEqual(review.tasks.map(t => t.id).sort());
    expect(sitting).toHaveLength(58);
    expect(sitting.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(749);
    for (const [section, count, marks] of [['A', 15, 84], ['B', 16, 280], ['C', 27, 385]] as const) {
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
  it('preserves independent vitamin and insulation prompts with their own tariffs', () => {
    expect(get('sa-q2').totalMarks).toBe(4);
    expect(get('sa-q2-sources').totalMarks).toBe(2);
    expect(get('sa-q2-sources').rows[0].parts?.map(p => p.permittedMarks)).toEqual([[0, 1], [0, 1]]);
    expect(get('sc-q1ci').totalMarks).toBe(6);
    expect(get('sc-q1ci-methods').totalMarks).toBe(12);
    expect(get('sc-q1ci-methods').rows[0].parts?.map(p => p.permittedMarks)).toEqual(Array(3).fill([0, 1, 2, 3, 4]));
    expect(get('sc-q1ci-methods').stem).toBe(get('sc-q1ci').stem);
    expect(get('sc-q1ci-methods').rows[0].contextNote).toContain('windows/doors');
  });
  it('keeps short-question tables and contaminant/source/effect pairings complete', () => {
    expect(get('sa-q3').questionText).toContain('Non-haem iron: description; food source');
    expect(get('sa-q3').rows.map(r => r.permittedMarks)).toEqual([[0, 2], [0, 1], [0, 2], [0, 1]]);
    expect(get('sa-q5').taskGroups?.map(g => g.marks)).toEqual([3, 3]);
    expect(get('sa-q7').rows).toHaveLength(6);
    expect(get('sa-q7').taskGroups?.map(g => g.marks)).toEqual([3, 3]);
    for (const text of ['pesticides', 'dioxins', 'Urea formaldehyde', 'foreign bodies']) expect(get('sa-q7').rows[0].contextNote).toContain(text);
    expect(get('sa-q10').rows.map(r => r.marks)).toEqual([2, 1, 2, 1]);
    expect(get('sa-q11').rows.map(r => r.permittedMarks)).toEqual([[0, 2, 3], [0, 2, 3]]);
  });
  it('restores missing long answers and enforces the published heading quotas', () => {
    expect(get('sb-q1d').rows.map(r => r.marks)).toEqual([5, 5, 10]);
    expect(get('sb-q1d').rows[0].contextNote).toContain('fruit canned in syrup');
    expect(get('sb-q1d').rows[1].contextNote).toContain('cooked sweet potatoes');
    expect(get('sb-q4b').taskGroups?.map(g => g.marks)).toEqual([9, 9]);
    expect(get('sb-q4b').rows.map(r => r.marks)).toEqual([3, 6, 3, 6]);
    expect(get('sb-q4b').rows[0].contextNote).toContain('hire purchase');
    expect(get('sb-q5a').rows.map(r => r.marks)).toEqual([5, 5, 10]);
    expect(get('sc-q1ai').questionText).toContain('family size and circumstances');
    expect(get('sc-q1ai').rows.map(r => r.marks)).toEqual([4, 4, 4, 8]);
    expect(get('sc-q3aii').rows[0].parts?.[0].permittedMarks).toEqual([0, 2, 3, 4, 5]);
    expect(get('sc-q4aii').rows.map(r => r.marks)).toEqual([2, 8, 5]);
    expect(get('sc-q4aii').rows[0].contextNote).toContain('explicitly requires hydrogenation');
    expect(get('sc-q4bii-study').totalMarks).toBe(18);
    expect(get('sc-q4bii-study').rows.map(r => r.marks)).toEqual([2, 6, 6, 4]);
  });
  it('keeps source figures and continued guidance within whole choice responses', () => {
    expect(get('sb-q1a').rows[0].parts).toHaveLength(4);
    expect(get('sb-q1a').questionFigure?.alt).toContain('impact on environment 11 / 0');
    expect(get('sb-q1b').figure?.solution).toBe(true);
    expect(get('sb-q1b').figure?.alt).toContain('H₂O');
    expect(get('sb-q1b').questionFigure).toBeUndefined();
    expect(get('sb-q1b').rows.map(r => r.marks)).toEqual([8, 8, 6]);
    expect(get('sb-q1c').taskGroups?.map(g => g.marks)).toEqual([6, 6, 6]);
    expect(get('sb-q1c').rows[0].contextNote).toContain('culinary application sponge cake');
    expect(get('sb-q1c').rows[0].contextNote).toContain('hydrolysis and inversion');
    expect(get('sc-q2ai').questionFigure?.alt).toContain('Both original summer outfits');
    expect(get('sc-q2cii').rows[0].contextNote).toContain('Riverdance costumes');
  });
  it('preserves the existing fabric progress aliases and every source model on one card', () => {
    const c = get('sc-q2b-wool');
    expect(c.answerVariants?.map(v => v.label)).toEqual(['Wool', 'Silk', 'Cotton', 'Linen', 'Another natural-fibre fabric']);
    for (const v of c.answerVariants ?? []) expect(v.rows.map(r => r.marks)).toEqual([2, 6, 3, 4]);
    for (const name of ['silk', 'cotton', 'linen']) {
      const id = `he-2024-hl-sc-q2b-${name}`;
      expect(CARDS.some(c => c.id === id)).toBe(false);
      expect(CARD_ID_ALIASES[id]).toBe(c.id);
    }
    expect(c.answerVariants?.[2].rows[1].contextNote).toContain('seed head');
    expect(c.answerVariants?.[3].rows[3].contextNote).toContain('grey ash');
  });
  it('keeps all scheme continuation pages separate from adjacent sections', () => {
    expect(anchors.q.map(q => q.n)).toEqual(['1', '2', '3', '4', '5', '6', '7', '8', '9']);
    for (const [n, pages] of [['1', [11, 12, 13]], ['2', [14]], ['3', [15]], ['4', [16]], ['5', [17]], ['6', [18, 19, 20]], ['7', [21, 22, 23]], ['8', [24, 25, 26]], ['9', [27, 28, 29]]] as const) expect(anchors.q.find(q => q.n === n)?.region.map(r => r.p)).toEqual(pages);
  });
  it('maps each card to its own Atlas question and canonical topic', () => {
    for (const c of sitting) {
      const m = c.questionRef.match(/Section ([ABC]) (?:E\d )?Q(\d+)/)!;
      const file = m[1] === 'A' ? 'LC098ALP014EV.pdf' : 'LC098ALP039EV.pdf';
      const n = String(Number(m[2]) + (m[1] === 'C' ? 5 : 0));
      const row = runtime.questionMappings.find(q => q[0] === 'h' && q[1] === 'e' && q[2] === 2024 && q[4] === file && q[5] === n)!;
      expect(row, c.id).toBeDefined();
      expect((row[6] as number[]).map(i => runtime.topicIds[i]).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
      const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'home-economics-s-and-s' && p.year === 2024 && p.level === 'higher' && p.lang === 'ev' && p.fileid === file)!;
      expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === n)!).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
    }
  });
});
