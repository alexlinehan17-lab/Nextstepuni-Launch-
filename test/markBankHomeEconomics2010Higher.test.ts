import { describe, expect, it } from 'vitest';
import { execFileSync } from 'node:child_process';
import { CARDS } from '../components/MarkBank/cards/home-economics/higher';
import { tariffReconciles } from '../types/markBank';
import runtime from '../data/examTopics/home-economics-s-and-s-question-runtime.json';
import crosswalk from '../data/examTopics/home-economics-s-and-s-curriculum-crosswalk.json';
import anchors from '../scripts/paper-trail/answers/2010/LC098ALP000EV.pdf.json';
import review from '../scripts/markbank/authoring/home-economics/2010-hl-main-review.json';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
const all = CARDS.filter(c => c.id.startsWith('he-2010-hl-'));
const get = (id: string) => {
  const c = all.find(c => c.id === `he-2010-hl-${id}`);
  if (!c || c.kind !== 'question') throw new Error(id);
  return c;
};
describe('2010 Higher Home Economics: independently reviewed combined booklet', () => {
  it('retains every printed task and all alternatives at the source total', () => {
    expect(all).toHaveLength(50);
    expect(all.map(c => c.id).sort()).toEqual(review.tasks.map(c => c.id).sort());
    expect(['sa', 'sb', 'sc'].map(s => all.filter(c => c.id.includes(`-${s}-`)).length)).toEqual([12, 18, 20]);
    expect(all.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(627);
    for (const c of all) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
      for (const v of c.answerVariants ?? []) expect(tariffReconciles({ ...c, rows: v.rows }), `${c.id}/${v.id}`).toBe(true);
    }
  });
  it('reconciles the independent PDF census across older merged blocks', () => {
    const observed = JSON.parse(execFileSync('python3', ['-c', `
import json,sys
sys.path.insert(0,'scripts/markbank/authoring')
import paper_census as c
p,t,s=c.census_sections('home-economics',2010,'hl')
print(json.dumps({'keys':sorted(c.key_label(k,'home-economics') for k in c.leaves_of(p)),'flags':c.continuity_flags(p,t,'home-economics')}))
`], { encoding: 'utf8' }));
    const expected = [
      ...Array.from({ length: 12 }, (_, i) => i + 1).filter(n => n !== 5).map(n => `Section A Q${n}`),
      'Section A Q5(i)', 'Section A Q5(ii)',
      'Section B Q1(a)(i)', 'Section B Q1(a)(ii)',
      ...['b', 'c', 'd'].map(l => `Section B Q1(${l})`),
      ...[2, 3, 4, 5].flatMap(n => ['a', 'b', 'c'].map(l => `Section B Q${n}(${l})`)),
      ...[1, 3].flatMap(n => ['a', 'b', 'c'].flatMap(l => (l === 'a' ? ['i', 'ii', 'iii'] : ['i', 'ii']).map(r => `Section C Q${n}(${l})(${r})`))),
      ...['i', 'ii', 'iii'].map(r => `Section C Q2(a)(${r})`),
      'Section C Q2(b)', 'Section C Q2(c)(i)', 'Section C Q2(c)(ii)',
    ];
    expect(observed.keys).toEqual(expected.sort());
    expect(observed.flags).toEqual([]);
  });
  it('does not invent per-answer marks in the six-mark short questions', () => {
    for (let n = 1; n <= 12; n++) {
      const c = get(`sa-q${n}`);
      expect(c.totalMarks).toBe(6);
      expect(c.tariffModel?.kind).toBe('questionTotal');
      expect(c.rows.every(r => r.marks === null && !r.permittedMarks && !r.parts)).toBe(true);
    }
    expect(get('sa-q2').rows).toHaveLength(10);
    expect(get('sa-q2').questionText).toContain('three properties');
    expect(get('sa-q6').questionText).toContain('one difference');
    expect(get('sa-q7').rows).toHaveLength(3);
  });
  it('keeps every original graph sector and all five source crops', () => {
    expect(Object.keys(review.figures)).toHaveLength(5);
    expect(new Set(all.flatMap(c => c.kind === 'question' && c.questionFigure ? [c.questionFigure.src] : [])).size).toBe(5);
    for (const v of ['29%', '21%', '18%', '15%', '4%', '9%']) expect(get('sb-q1ai').questionFigure?.alt).toContain(v);
    expect(get('sb-q1ai').rows[0].group?.options).toHaveLength(7);
    expect(get('sa-q12').questionFigure?.alt).toContain('both printed captions');
  });
  it('preserves fish category quotas and whole comparative cooking/preservation tasks', () => {
    expect(get('sb-q2a').answerVariants?.map(v => v.rows.map(r => r.group?.claimMax))).toEqual([[3, 2], [2, 3]]);
    expect(get('sb-q2b').taskGroups?.map(g => g.marks)).toEqual([10, 10]);
    expect(get('sb-q2b').rows.map(r => r.marks)).toEqual([2, 6, 2, 2, 6, 2]);
    expect(get('sb-q3a').rows.map(r => r.marks)).toEqual([2, 6, 6, 6, 6]);
    expect(get('sb-q3a').rows[1].group?.options).toHaveLength(9);
    expect(get('sb-q3a').rows[2].contextNote).toContain('Freeze-drying');
    expect(get('sb-q3a').rows[2].contextNote).toContain('Irradiation');
    expect(get('sb-q3a').rows[2].contextNote).toContain('Pasteurisation');
    expect(get('sb-q3b').rows.map(r => r.marks)).toEqual([4, 6, 6]);
  });
  it('keeps paired family points and the separately priced will tasks', () => {
    const row = get('sb-q5a').rows[0];
    expect([row.group?.claimMax, row.group?.perOption]).toEqual([4, 6]);
    expect(row.group?.options).toHaveLength(5);
    expect(row.group?.options.every(v => v.includes(' — '))).toBe(true);
    expect([get('sb-q5c-importance').totalMarks, get('sb-q5c-procedure').totalMarks]).toEqual([4, 10]);
    expect(get('sb-q5c-procedure').questionText).toBe('outline the procedure involved.');
    expect(get('sb-q5c-procedure').stem).toContain('parents to make a will');
  });
  it('retains chosen-response dependencies and only published full-point steps', () => {
    expect(get('sc-q1aii').rows[0].parts).toHaveLength(5);
    expect(get('sc-q3ai').rows[0].parts).toHaveLength(5);
    expect(get('sc-q1cii').answerVariants).toHaveLength(8);
    expect(get('sc-q2aii').rows.map(r => r.permittedMarks)).toEqual([[0, 5], [0, 4]]);
    expect(get('sc-q2aiii').stem).toContain('Sketch and describe an outfit');
    expect(get('sc-q2b').rows.map(r => r.marks)).toEqual([6, 4, 3, 2]);
    expect(get('sc-q3aiii').rows[1].contextNote).toContain('no model facts');
  });
  it('preserves the twenty physical IDs and maps every task to its canonical Atlas topics', () => {
    expect(anchors.q.map(q => q.n)).toEqual(Array.from({ length: 20 }, (_, i) => String(i + 1)));
    expect(anchors.q.find(q => q.n === '13')!.region.map(r => r.p)).toEqual([7, 8]);
    expect(anchors.q.find(q => q.n === '18')!.region.map(r => r.p)).toEqual([13, 14, 15]);
    expect(anchors.q.find(q => q.n === '20')!.region.map(r => r.p)).toEqual([18, 19]);
    const file = 'LC098ALP000EV.pdf';
    const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'home-economics-s-and-s' && p.year === 2010 && p.level === 'higher' && p.lang === 'ev' && p.fileid === file)!;
    for (const c of all) {
      const m = c.questionRef.match(/Section ([ABC]) (?:E\d )?Q(\d+)/)!;
      const n = String(Number(m[2]) + (m[1] === 'A' ? 0 : m[1] === 'B' ? 12 : 17));
      const row = runtime.questionMappings.find(q => q[0] === 'h' && q[1] === 'e' && q[2] === 2010 && q[4] === file && q[5] === n)!;
      expect(row, c.id).toBeDefined();
      expect((row[6] as number[]).map(i => runtime.topicIds[i]).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
      expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === n)!).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
    }
  });
});
