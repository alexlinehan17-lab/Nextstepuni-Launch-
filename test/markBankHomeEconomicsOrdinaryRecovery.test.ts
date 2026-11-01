import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/home-economics/ordinary';
import { tariffReconciles } from '../types/markBank';
import runtime from '../data/examTopics/home-economics-s-and-s-question-runtime.json';
import crosswalk from '../data/examTopics/home-economics-s-and-s-curriculum-crosswalk.json';
import anchors from '../scripts/paper-trail/answers/2023/LC098GLP039EV.pdf.json';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
import { preferredAnswersUrl } from '../components/PaperTrail/vaultResolve';
import { paperRegionFor, schemeRegionFor } from '../components/PaperTrail/paperRegion';
import type { PaperAnswerMap } from '../types/paperTrail';

const get = (id: string) => {
  const card = CARDS.find(c => c.id === id);
  if (!card || card.kind !== 'question') throw new Error(`Missing question: ${id}`);
  return card;
};

describe('2023 Ordinary Home Economics recovered tasks', () => {
  it('retains the full Section B protein, hygiene and appliance allocations', () => {
    const protein = get('he-2023-ol-sb-q1b');
    expect(protein.rows.map(r => r.marks)).toEqual([6, 12, 8]);
    expect(protein.rows[0].parts?.map(p => p.permittedMarks)).toEqual(Array(2).fill([0, 2, 3]));
    expect(protein.rows[1].parts?.map(p => p.permittedMarks)).toEqual(Array(3).fill([0, 2, 4]));
    expect(protein.rows[2].contextNote).toContain('manufacture of blood plasma');
    const hygiene = get('he-2023-ol-sb-q3a');
    expect(hygiene.rows.map(r => r.marks)).toEqual([4, 4, 8]);
    expect(hygiene.rows[0].verbatim).toBe('preparation');
    expect(hygiene.rows[1].verbatim).toBe('storage');
    expect(hygiene.rows[1].contextNote).toContain('-18°C');
    const fridge = get('he-2023-ol-sb-q3b');
    expect(fridge.rows.map(r => r.marks)).toEqual([2, 12, 12]);
    expect(fridge.rows[0].permittedMarks).toEqual([0, 1, 2]);
    expect(fridge.rows[2].contextNote).toContain('leave unplugged and open');
  });

  it('preserves the separate causes and solutions tariffs with the conflict context', () => {
    const causes = get('he-2023-ol-sb-q5b');
    const ways = get('he-2023-ol-sb-q5bii');
    expect(causes.questionRef).toBe('2023 OL Section B Q5(b)(i)');
    expect(ways.questionRef).toBe('2023 OL Section B Q5(b)(ii)');
    expect(causes.totalMarks).toBe(10);
    expect(ways.totalMarks).toBe(10);
    expect(ways.stem).toBe('Identify two causes of conflict between teenagers and adults.');
    for (const c of [causes, ways]) expect(c.rows[0].parts?.map(p => p.permittedMarks)).toEqual(Array(2).fill([0, 3, 5]));
    expect(causes.rows[0].contextNote).toContain('dishonesty; etc.');
    expect(ways.rows[0].contextNote).toContain('do not ignore conflict; etc.');
    const cards = CARDS.filter(c => c.questionRef.startsWith('2023 OL Section B '));
    expect(cards).toHaveLength(17);
    expect(cards.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(280);
    for (const c of cards) expect(tariffReconciles(c), c.id).toBe(true);
  });

  it('keeps all housing factors and distinguishes original source errors from factual guidance', () => {
    const housing = get('he-2023-ol-sb-q4a');
    expect(housing.rows.map(r => r.verbatim)).toEqual(['family needs', 'cost', 'location', 'trends in housing development']);
    expect(housing.rows.map(r => r.permittedMarks)).toEqual(Array(4).fill([0, 3, 5]));
    expect(housing.rows[3].contextNote).toContain('passive houses with high energy rating-BER rating');
    const pollution = get('he-2023-ol-sb-q4c');
    expect(pollution.rows[0].contextNote).toContain('appears to be an error');
    expect(pollution.rows[0].contextNote).toContain('Published 2023 scheme wording: use phosphate detergents;');
    expect(pollution.rows[0].contextNote).toContain('use a reusable water bottle; etc.');
    const will = get('he-2023-ol-sb-q5c');
    expect(will.rows[0].contextNote).toContain('is not a general rule');
    expect(will.rows[0].contextNote).toContain('Intestacy rules determine distribution among family members');
    expect(will.rows[0].contextNote).toContain('if a person dies without leaving a will a sizable portion of their estate will go to the state');
  });

  it('splits the independent iron-source task without changing its functions identity', () => {
    const functions = get('he-2023-ol-sa-q4');
    const source = get('he-2023-ol-sa-q4-source');
    expect(functions.totalMarks).toBe(4);
    expect(functions.questionText).toBe('State two functions of iron in the body.');
    expect(functions.rows[0].parts?.map(p => p.permittedMarks)).toEqual([[0, 1, 2], [0, 1, 2]]);
    expect(source.questionText).toBe('Name one dietary source of iron.');
    expect(source.totalMarks).toBe(2);
    expect(source.rows[0].permittedMarks).toEqual([0, 1, 2]);
    expect(source.rows[0].contextNote).toContain('green vegetables; fish; etc.');
    const row = runtime.questionMappings.find(q => q[0] === 'o' && q[1] === 'e' && q[2] === 2023
      && q[4] === 'LC098GLP014EV.pdf' && q[5] === '4')!;
    expect((row[6] as number[]).map(i => runtime.topicIds[i])
      .some(t => (crosswalk as Record<string, string[]>)[t]?.includes(source.topicId))).toBe(true);
  });

  it('exposes the published one-mark steps and complete short-answer guidance', () => {
    for (const n of [2, 7, 9, 12, 13]) {
      const c = get(`he-2023-ol-sa-q${n}`);
      expect(c.rows[0].parts?.map(p => p.permittedMarks)).toEqual(Array(3).fill([0, 1, 2]));
      expect(c.rows[0].contextNote).toMatch(/etc\.$/);
    }
    const microwave = get('he-2023-ol-sa-q13');
    expect(microwave.rows[0].contextNote).toContain('brand;');
    expect(microwave.rows[0].contextNote).toContain('after sales service;');
    const raising = get('he-2023-ol-sa-q8');
    expect(raising.questionText).toContain('Sponge cake\nBread\nLemon drizzle cake');
    expect(raising.rows.map(r => r.permittedMarks)).toEqual(Array(3).fill([0, 1, 2]));
    expect(raising.rows.every(r => r.contextNote?.includes('different agent for each product'))).toBe(true);
    const credit = get('he-2023-ol-sa-q11');
    expect(credit.rows.map(r => r.marks)).toEqual([2, 4]);
    expect(credit.rows[0].permittedMarks).toEqual([0, 1, 2]);
    expect(credit.rows[1].parts?.map(p => p.permittedMarks)).toEqual([[0, 1, 2], [0, 1, 2]]);
    const cards = CARDS.filter(c => c.questionRef.startsWith('2023 OL Section A '));
    expect(cards).toHaveLength(15);
    expect(cards.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(84);
    for (const c of cards) expect(tariffReconciles(c), c.id).toBe(true);
  });

  it('shows the original care symbols with separate published partial marks', () => {
    const c = get('he-2023-ol-sa-q14');
    expect(c.questionFigure?.src).toContain('2023-ol-sa-q14-symbols.png');
    expect(c.questionFigure?.alt).not.toMatch(/dry/i);
    expect(c.rows.map(r => r.verbatim)).toEqual(['drip dry', 'do not tumble dry']);
    expect(c.rows.map(r => r.permittedMarks)).toEqual([[0, 2, 3], [0, 2, 3]]);
    expect(c.totalMarks).toBe(6);
    expect(tariffReconciles(c)).toBe(true);
  });

  it('keeps all three bars in one choice card with the full original nutrition table', () => {
    const c = get('he-2023-ol-sb-q1a');
    expect(c.questionFigure?.src).toContain('2023-ol-sb-q1a-table.png');
    expect(c.questionFigure?.alt).toContain('per 100 g');
    expect(c.questionFigure?.alt).toContain('Salt: 0.95, 0.73, 0.59 g');
    expect(c.totalMarks).toBe(24);
    expect(c.answerVariants?.map(v => v.label)).toEqual(['Peanut & chocolate', 'Peanut & caramel', 'Crunchy peanut butter']);
    for (const v of c.answerVariants ?? []) {
      expect(v.rows.map(r => r.marks)).toEqual([4, 20]);
      expect(v.rows[1].parts?.map(p => p.permittedMarks)).toEqual(Array(4).fill([0, 2, 3, 4, 5]));
      expect(v.rows[1].contextNote).toMatch(/etc\.$/);
      expect(tariffReconciles({ ...c, rows: v.rows })).toBe(true);
    }
  });

  it('reserves both required meat headings and the low-income menu reason', () => {
    const meat = get('he-2023-ol-sb-q2a');
    expect(meat.rows.map(r => r.marks)).toEqual([5, 5, 10]);
    expect(meat.rows.map(r => r.verbatim)).toEqual(['nutritive', 'dietetic', 'plus 2 others']);
    expect(meat.rows[0].contextNote).toContain('protein');
    expect(meat.rows[1].contextNote).toContain('digest');
    const menu = get('he-2023-ol-sb-q2b');
    expect(menu.rows.map(r => r.marks)).toEqual([8, 4, 8]);
    expect(menu.rows[0].parts?.map(p => p.permittedMarks)).toEqual([[0, 2, 4], [0, 2, 4]]);
    expect(menu.rows[0].contextNote).toContain('not the only valid menu');
    expect(menu.rows[1].contextNote).toContain('low income');
    expect(menu.rows[2].contextNote).toMatch(/easy to digest; etc\.$/);
    expect(tariffReconciles(meat)).toBe(true);
    expect(tariffReconciles(menu)).toBe(true);
  });

  it('restores the full statutory-scheme response without inventing a printed model detail', () => {
    const c = get('he-2023-ol-sc-q3aiv');
    expect(c.totalMarks).toBe(8);
    expect(c.questionText).toMatch(/^Name and give details/);
    expect(c.rows.map(r => r.permittedMarks)).toEqual([[0, 2, 4], [0, 2, 4]]);
    expect(c.rows[0].contextNote).toContain('MABS; Abhaile; etc.');
    expect(c.rows[1].contextNote).toContain('prints no model detail answer');
    expect(tariffReconciles(c)).toBe(true);
    expect(CARDS.some(c => c.id === 'he-2023-ol-sc-q3aiv-details')).toBe(false);
  });

  it('opens every Ordinary elective at its own paper and scheme pages', () => {
    expect(anchors.q.map(q => q.n)).toEqual(['1', '2', '3', '4', '5', '6', '7', '8', '9']);
    const regions = [[16, 17], [18, 19], [20, 21, 22], [23, 24]];
    for (let i = 0; i < 4; i++) {
      const n = String(i + 6);
      const q = (anchors as PaperAnswerMap).q.find(q => q.n === n)!;
      expect(q.label).toBe(`Section C · Q${i + 1}`);
      expect(paperRegionFor((anchors as PaperAnswerMap).q, n)?.map(r => r.p)).toEqual([i + 5]);
      expect(schemeRegionFor(q).map(r => r.p)).toEqual(regions[i]);
    }
    expect(preferredAnswersUrl('home-economics-s-and-s', 2023, 'LC098GLP039EV.pdf', 'stale-storage-url'))
      .toBe('/paper-answers/2023/LC098GLP039EV.pdf.json');
  });

  it('places every reviewed B/C identity and new short question under its canonical Atlas topic', () => {
    const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'home-economics-s-and-s'
      && p.year === 2023 && p.level === 'ordinary' && p.lang === 'ev' && p.fileid === 'LC098GLP039EV.pdf')!;
    const cards = CARDS.filter(c => /^2023 OL Section [BC] /.test(c.questionRef));
    expect(cards).toHaveLength(45);
    for (const c of cards) {
      const m = c.questionRef.match(/Section ([BC]) (?:E\d )?Q(\d+)/)!;
      const n = String(Number(m[2]) + (m[1] === 'C' ? 5 : 0));
      const topics = browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === n)!);
      expect(topics.some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId)), c.id).toBe(true);
    }
    const c = get('he-2023-ol-sa-q14');
    const row = runtime.questionMappings.find(q => q[0] === 'o' && q[1] === 'e' && q[2] === 2023
      && q[4] === 'LC098GLP014EV.pdf' && q[5] === '14')!;
    expect((row[6] as number[]).map(i => runtime.topicIds[i])
      .some(t => (crosswalk as Record<string, string[]>)[t]?.includes(c.topicId))).toBe(true);
  });
});
