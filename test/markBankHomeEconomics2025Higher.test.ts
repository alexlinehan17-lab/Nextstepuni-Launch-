import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/home-economics/higher';
import { tariffReconciles } from '../types/markBank';
import runtime from '../data/examTopics/home-economics-s-and-s-question-runtime.json';
import crosswalk from '../data/examTopics/home-economics-s-and-s-curriculum-crosswalk.json';
import anchors from '../scripts/paper-trail/answers/2025/LC098ALP014EV.pdf.json';
import review from '../scripts/markbank/authoring/home-economics/2025-hl-main-review.json';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
const get = (id: string) => {
  const c = CARDS.find(c => c.id === `he-2025-hl-${id}`);
  if (!c || c.kind !== 'question') throw new Error(id);
  return c;
};
const sitting = CARDS.filter(c => c.id.startsWith('he-2025-hl-sa-'));
describe('2025 Higher Home Economics Section A source review', () => {
  it('keeps all fifteen independently reviewed tasks and every answer-route tariff', () => {
    expect(sitting.map(c => c.id).sort()).toEqual(review.tasks.filter(t => t.section === 'A').map(t => t.id).sort());
    expect(sitting).toHaveLength(15);
    expect(sitting.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(84);
    for (const c of sitting) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
      for (const v of c.answerVariants ?? []) expect(tariffReconciles({ ...c, rows: v.rows }), `${c.id}/${v.id}`).toBe(true);
    }
  });
  it('preserves the independent sodium-source prompt and complete table questions', () => {
    expect(get('sa-q3').totalMarks).toBe(4);
    expect(get('sa-q3-sources').totalMarks).toBe(2);
    expect(get('sa-q3-sources').rows[0].parts?.map(p => p.permittedMarks)).toEqual([[0, 1], [0, 1]]);
    expect(get('sa-q2').questionText).toContain('Organ: Pancreas');
    expect(get('sa-q2').rows.map(r => r.permittedMarks)).toEqual(Array(3).fill([0, 1, 2]));
    for (const name of ['Night blindness', 'Rickets', 'Beri-beri']) expect(get('sa-q4').questionText).toContain(name);
    expect(get('sa-q4').rows[1].contextNote).toContain('Vitamin D');
  });
  it('keeps dependent heat-transfer and assurance answers whole with complete source models', () => {
    const heat = get('sa-q8');
    expect(heat.answerVariants?.map(v => v.label)).toEqual(['Conduction', 'Convection', 'Radiation']);
    for (const v of heat.answerVariants ?? []) expect(v.rows.map(r => r.marks)).toEqual([2, 3, 1]);
    expect(heat.answerVariants?.[0].rows[1].contextNote).toContain('from molecule to molecule');
    expect(heat.answerVariants?.[1].rows[1].contextNote).toContain('cold air or liquid falls');
    expect(heat.answerVariants?.[2].rows[1].contextNote).toContain('to the object (food) in front of it');
    expect(heat.answerVariants?.[2].rows[2].contextNote).toContain('grilling; barbequing');
    const assurance = get('sa-q10');
    expect(assurance.answerVariants).toHaveLength(6);
    for (const v of assurance.answerVariants ?? []) expect(v.rows.map(r => r.permittedMarks)).toEqual([[0, 2, 3], [0, 2, 3]]);
    expect(assurance.answerVariants?.[4].label).toBe('Convertible term assurance');
  });
  it('retains paired responses and asymmetric tariffs without a long selectable option list', () => {
    expect(get('sa-q9').taskGroups?.map(g => g.marks)).toEqual([3, 3]);
    expect(get('sa-q9').rows.map(r => r.permittedMarks)).toEqual([[0, 1, 2], [0, 1], [0, 1, 2], [0, 1]]);
    for (const name of ['humectants', 'anti-caking', 'emulsifiers', 'setting agents', 'stabilisers', 'anti-spattering', 'anti-foaming', 'bulking', 'firming', 'packaging gas']) expect(get('sa-q9').rows[0].contextNote).toContain(name);
    expect(get('sa-q11').taskGroups?.map(g => g.marks)).toEqual([3, 3]);
    expect(get('sa-q11').rows.map(r => r.permittedMarks)).toEqual([[0, 2], [0, 1], [0, 2], [0, 1]]);
    expect(get('sa-q14').rows[0].parts?.map(p => p.permittedMarks)).toEqual([[0, 2, 3], [0, 2, 3]]);
    expect(get('sa-q6').rows.map(r => r.marks)).toEqual([3, 3]);
  });
  it('retains fourteen complete original Atlas paper/scheme anchors', () => {
    expect(anchors.q.map(q => q.n)).toEqual(Array.from({ length: 14 }, (_, i) => String(i + 1)));
    expect(anchors.q.find(q => q.n === '8')!.region.map(r => r.p)).toEqual([8]);
  });
  it('maps each card to its own Atlas question and canonical topic', () => {
    for (const c of sitting) {
      const m = c.questionRef.match(/Section ([ABC]) (?:E\d )?Q(\d+)/)!;
      const file = m[1] === 'A' ? 'LC098ALP014EV.pdf' : 'LC098ALP039EV.pdf';
      const n = String(Number(m[2]) + (m[1] === 'C' ? 5 : 0));
      const row = runtime.questionMappings.find(q => q[0] === 'h' && q[1] === 'e' && q[2] === 2025 && q[4] === file && q[5] === n)!;
      expect(row, c.id).toBeDefined();
      expect((row[6] as number[]).map(i => runtime.topicIds[i]).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
      const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'home-economics-s-and-s' && p.year === 2025 && p.level === 'higher' && p.lang === 'ev' && p.fileid === file)!;
      expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === n)!).some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
    }
  });
});
