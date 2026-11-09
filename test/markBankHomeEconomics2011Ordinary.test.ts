import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/home-economics/ordinary';
import { tariffReconciles } from '../types/markBank';
import runtime from '../data/examTopics/home-economics-s-and-s-question-runtime.json';
import crosswalk from '../data/examTopics/home-economics-s-and-s-curriculum-crosswalk.json';
import anchors from '../scripts/paper-trail/answers/2011/LC098GLP000EV.pdf.json';
import review from '../scripts/markbank/authoring/home-economics/2011-ol-main-review.json';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
const all = CARDS.filter(c => c.id.startsWith('he-2011-ol-'));
const get = (id: string) => {
  const c = all.find(c => c.id === `he-2011-ol-${id}`);
  if (!c || c.kind !== 'question') throw new Error(id);
  return c;
};
describe('2011 Ordinary Home Economics: independently swept original sources', () => {
  it('retains all 52 priced tasks, choices and 627 offered marks', () => {
    expect(all).toHaveLength(52);
    expect(all.map(c => c.id).sort()).toEqual(review.tasks.map(c => c.id).sort());
    expect(['sa', 'sb', 'sc'].map(s => all.filter(c => c.id.includes(`-${s}-`)).length)).toEqual([13, 18, 21]);
    expect(all.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(627);
    for (const c of all) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
      for (const v of c.answerVariants ?? []) expect(tariffReconciles({ ...c, rows: v.rows }), `${c.id}/${v.id}`).toBe(true);
    }
  });
  it('keeps the ambiguous raising-agent allocation visible without assigning prices to foods', () => {
    const c = get('sa-q6');
    expect(c.rows.map(r => r.marks)).toEqual([5, 1]);
    expect(c.rows[0].permittedMarks).toEqual([0, 5]);
    expect(c.rows[0].contextNote).toContain('does not assign those prices to individual dishes');
    for (const word of ['Bread', 'Sponge cake', 'Muffins']) expect(c.rows[0].contextNote).toContain(word);
    expect(c.rows[1].contextNote).toContain('ONE');
    expect(get('sa-q11').totalMarks).toBe(2);
    expect(get('sa-q11-uses').totalMarks).toBe(4);
    expect(get('sa-q12').rows.map(r => r.marks)).toEqual([2, 1, 2, 1]);
  });
  it('keeps exact printed prose despite the original PDF strip-set text layer', () => {
    expect(get('sa-q7').questionText).toBe('How should raw meat and chicken be stored in the home in order to prevent cross contamination? Give two points.');
    expect(get('sa-q9').questionText).toContain('washing machines. Explain its benefit');
    expect(get('sb-q2b').questionText).toBe('Plan a menu (3 meals to include a packed lunch) for one day for a school-going child. Include fruit/vegetables in each meal.');
    expect(get('sb-q3a').questionText).toBe('Describe the nutritive value of eggs.');
    expect(get('sc-q1aii').questionText).toContain('elderly person with limited mobility (movement)');
    expect(get('sc-q1aiii').questionText).toContain('two advantages and two disadvantages');
    for (const c of all) if (c.kind === 'question') expect(c.questionText).not.toMatch(/raww|egg gs|egg.gs|Name ttwo|Commeent|Describbe/);
  });
  it('preserves all ten original input figures, full table cells and the unlabelled chart bars', () => {
    expect(Object.keys(review.figures)).toHaveLength(10);
    expect(new Set(all.flatMap(c => c.kind === 'question' && c.questionFigure ? [c.questionFigure.src] : [])).size).toBe(10);
    for (const value of ['18.3 g/20.2 g', '0.7 g/11.0 g', '0 g/0 g', '80 kcal/180 kcal']) expect(get('sb-q1a').questionFigure?.alt).toContain(value);
    expect(get('sb-q2a').questionFigure?.alt).toContain('None, One, Two, Three, Four, Five');
    expect(get('sb-q2a').questionFigure?.alt).toContain('no exact printed value labels');
    expect(get('sc-q3ai').questionFigure?.alt).toContain('4.2% (178,074 people)');
    expect(get('sc-q3ai').questionFigure?.alt).toContain('14.4% (610,538 people)');
    expect(get('sa-q6').questionFigure?.includesPrompt).toBe(true);
  });
  it('retains independently priced explanations and required paired responses', () => {
    expect([get('sb-q1c-essential').totalMarks, get('sb-q1c-omega3').totalMarks]).toEqual([7, 7]);
    expect(get('sb-q1b').rows.map(r => r.marks)).toEqual([8, 12, 8]);
    expect(get('sb-q1d').rows.map(r => r.marks)).toEqual([10, 10]);
    expect(get('sb-q2b').rows.map(r => r.verbatim)).toEqual(['Breakfast', 'Packed Lunch', 'Dinner']);
    expect(get('sb-q3b').taskGroups?.map(g => g.marks)).toEqual([6, 6, 6]);
    expect(get('sb-q4a').taskGroups?.map(g => g.marks)).toEqual([8, 8, 8]);
    expect(get('sb-q4b').stem).toContain('€100');
    expect(get('sb-q5aii').taskGroups?.map(g => g.label)).toEqual(['Marriage counselling', 'Legal separation', 'Divorce']);
    expect(get('sb-q5aii').stem).toContain('marriage counselling');
    expect([get('sb-q5bi').totalMarks, get('sb-q5bii').totalMarks]).toEqual([5, 12]);
  });
  it('preserves dependent profiles and source quotas without invented per-heading allocations', () => {
    expect(get('sc-q1ai').rows[0].contextNote).toContain('Four points TOTAL');
    expect(get('sc-q1bi').rows.map(r => r.marks)).toEqual([6, 4, 4]);
    expect(get('sc-q1bii').taskGroups?.map(g => g.marks)).toEqual([8, 8]);
    expect(get('sc-q1cii').rows.map(r => r.marks)).toEqual([4, 8, 6]);
    expect(get('sc-q2aii').stem).toContain('Design and sketch an outfit');
    expect(get('sc-q2aiii').stem).toContain('Design and sketch an outfit');
    expect(get('sc-q2ci').rows.map(r => r.verbatim)).toEqual(['available money', 'climate', 'cultural influences.']);
    expect(get('sc-q3aiii').rows.map(r => r.marks)).toEqual([8, 12]);
    expect(get('sc-q3aiii').rows[1].contextNote).toContain('THREE effects TOTAL');
    expect(get('sc-q3bi').rows[0].contextNote).toContain('no per-heading allocation');
  });
  it('preserves all twenty physical IDs and joins every task to canonical Atlas topics', () => {
    expect(anchors.q.map(q => q.n)).toEqual(Array.from({ length: 20 }, (_, i) => String(i + 1)));
    expect(anchors.schemeFileid).toBe('LC098GLP000EV.PDF');
    expect(anchors.q.find(q => q.n === '13')!.region.map(r => r.p)).toEqual([8, 9]);
    expect(anchors.q.find(q => q.n === '18')!.region.map(r => r.p)).toEqual([15, 16]);
    expect(anchors.q.find(q => q.n === '19')!.region.map(r => r.p)).toEqual([17, 18]);
    expect(anchors.q.find(q => q.n === '19')!.region[0].r[3]).toBeGreaterThan(0.89);
    expect(anchors.q.find(q => q.n === '20')!.region.map(r => r.p)).toEqual([19, 20]);
    const file = 'LC098GLP000EV.pdf';
    const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'home-economics-s-and-s' && p.year === 2011 && p.level === 'ordinary' && p.lang === 'ev' && p.fileid === file)!;
    for (const c of all) {
      const m = c.questionRef.match(/Section ([ABC]) (?:E\d )?Q(\d+)/)!;
      const n = String(Number(m[2]) + (m[1] === 'A' ? 0 : m[1] === 'B' ? 12 : 17));
      const row = runtime.questionMappings.find(q => q[0] === 'o' && q[1] === 'e' && q[2] === 2011 && q[4] === file && q[5] === n)!;
      expect(row, c.id).toBeDefined();
      expect((row[6] as number[]).map(i => runtime.topicIds[i]).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
      expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === n)!).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
    }
  });
});
