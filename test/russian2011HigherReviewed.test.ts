import { describe, expect, it } from 'vitest';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import { languageMarks, languageScoreId, languageFlagId, languageGroupId, languageRowId, languageOtherLanguageId } from '../components/MarkBank/languageScoring';
import { isRubricCard, tariffReconciles } from '../types/markBank';
const sitting = REVIEWED_CARDS.filter(c => c.year === 2011 && c.level === 'higher');
const get = (suffix: string) => {
  const c = sitting.find(c => c.id === `ru-2011-hl-${suffix}`);
  if (!c || !isRubricCard(c)) throw new Error(suffix);
  return c;
};
const points = (suffix: string) => {
  const c = get(suffix);
  if (c.rubric.system !== 'language-points') throw new Error(suffix);
  return { ...c, rubric: c.rubric };
};
const row = (group: string, id = 'full') => ({ [languageGroupId(group)]: 1, [languageRowId(group, id)]: 1 });
const summary = (section: number, content: number, discretion: number) => ({
  [languageGroupId(`section-${section}`)]: 1,
  [languageScoreId(`section-${section}-content`)]: content,
  [languageScoreId(`section-${section}-discretion`)]: discretion,
});
const summaryCard = (section: number) => points(section === 1 ? 'c2' : `c2-${section}`);

describe('Russian 2011 Higher reviewed original allocations', () => {
  it('gives all 39 printed asks their own card with the approved practice maxima', () => {
    expect(sitting).toHaveLength(39);
    expect(sitting.filter(c => !tariffReconciles(c)).map(c => c.id)).toEqual([]);
    // Practice maxima differ from the printed 300 because four 12-mark
    // summary cards retain the source's conflicting 45-mark section total.
    expect(sitting.reduce((sum,c) => sum+c.totalMarks,0)).toBe(303);
    expect(sitting.filter(c => c.audioMaterial)).toHaveLength(20);
    expect(sitting.filter(c => c.audioMaterial).reduce((sum,c) => sum+c.totalMarks,0)).toBe(80);
    expect(sitting.filter(c => c.section === 'C2')).toHaveLength(4);
  });
  it('keeps each complete summary prompt, its own passage and the original identity on Section 1', () => {
    for (const section of [1,2,3,4]) {
      const c = summaryCard(section);
      expect(c.questionRef).toBe(`2011 HL Section C2 Q${section}`);
      expect(c.questionText.match(/Give five details\./g)).toHaveLength(1);
      expect(c.questionText).toContain('Write a summary in English');
      expect(c.sourceMaterial?.pages).toEqual([section+5]);
      expect(c.rubric.groups[0].criteria?.map(k => k.maxMarks)).toEqual([10,2]);
      expect(c.totalMarks).toBe(12);
      expect(c.rubric.markingGuideNote).toContain('scheme’s printed 45');
      expect(c.rubric.markingGuideNote).toContain('paper prints 40');
      expect(c.rubric.markingGuideNote).toContain('maxima add to 48');
    }
    expect(summaryCard(1).conceptId).toBe('summary-english-content-section-instructed-section');
  });
  it('records the printed 10 content plus one or two discretionary marks on every separate card', () => {
    for (const section of [1,2,3,4]) {
      const c = summaryCard(section);
      expect(languageMarks(c,summary(section,10,1))).toBe(11);
      expect(languageMarks(c,summary(section,10,2))).toBe(12);
      expect(languageMarks(c,{})).toBe(0);
      const scores = summary(section,10,2);
      const flagged = {...scores,[languageFlagId('incomplete-summary-response')]:1};
      expect(languageMarks(c,flagged)).toBe(10);
      expect(languageMarks(c,{...flagged,[languageFlagId('incomplete-summary-response')]:0})).toBe(12);
    }
  });
  it('keeps the language exception manual beside both original rules on every card', () => {
    for (const section of [1,2,3,4]) {
      const c = summaryCard(section);
      expect(c.answerLanguageRule).toBeUndefined();
      for (const criterion of c.rubric.groups[0].criteria ?? []) {
        const guide = criterion.guidance.join(' ');
        expect(guide).toContain('award NO marks');
        expect(guide).toContain('Discretionary marks may be awarded');
        expect(guide).toMatch(/Russian-\s*language words/);
      }
      const scores = summary(section,0,2);
      expect(languageMarks(c,scores)).toBe(2);
      expect(languageMarks(c,{...scores,[languageOtherLanguageId('response')]:1})).toBe(2);
    }
    expect(sitting.filter(c => c.answerLanguageRule)).toHaveLength(12);
    expect(sitting.filter(c => c.audioMaterial).every(c => !c.answerLanguageRule)).toBe(true);
  });
  it('keeps each nested content condition with the part it belongs to', () => {
    const second = summaryCard(2).rubric.groups[0].criteria![0].guidance.join(' ');
    const third = summaryCard(3).rubric.groups[0].criteria![0].guidance.join(' ');
    expect(second).toContain('all four categories are required');
    expect(second).toContain('maximum of two marks');
    expect(third).toMatch(/any two/i);
    expect(third).toMatch(/maximum of 4/i);
    expect(summaryCard(1).rubric.groups[0].criteria![0].guidance.join(' ')).not.toContain('all four categories are required');
    expect(summaryCard(3).rubric.markingGuideNote).toContain('do not count or classify individual details');
  });
  it('keeps the four-mark complete meeting statement exclusive from the two-person route', () => {
    const c = points('c1-1-i');
    expect(languageMarks(c,row('both-walking'))).toBe(4);
    const separate = {[languageGroupId('one-each')]:1,[languageScoreId('misha')]:2,[languageScoreId('lena')]:2};
    expect(languageMarks(c,separate)).toBe(4);
    expect(languageMarks(c,{...separate,...row('both-walking')})).toBe(0);
  });
  it('prevents a fantasy detail already credited in the previous question from scoring twice', () => {
    const c = points('c1-2-ii'), group = c.rubric.groups.find(g => g.criteria?.some(k => k.id === 'fantasy-credit'))!;
    const scores = {[languageGroupId(group.id)]:1,[languageScoreId('fantasy-credit')]:2};
    expect(languageMarks(c,scores)).toBe(2);
    expect(languageMarks(c,{...scores,[languageFlagId('fantasy-already-credited')]:1})).toBe(0);
  });
  it('retains exact infinitives, matching partials and all fifteen grammar answers', () => {
    expect(points('la1').rubric.groups.map(g => g.rows[0].text)).toEqual(['пойти','видеть','жить','забыть','нравиться','дружить']);
    const matching = points('sd');
    expect(matching.rubric.groups[0].rows.map(r => [r.text,r.marks])).toEqual([['6',2],['5',1],['8',1]]);
    expect(languageMarks(matching,{...row('answer-1','full'),...row('answer-1','partial-1')})).toBe(2);
    const grammar = points('gr');
    expect(grammar.rubric.groups).toHaveLength(15);
    expect(grammar.rubric.groups[6].rows[0].text).toBe('вуза/ВУЗа');
    expect(grammar.rubric.groups.every(g => g.rows.every(r => r.marks === 2 && !r.steps))).toBe(true);
  });
  it('retains all original writing alternatives and the literal Lower A overlap', () => {
    const essay = get('se'), guided = get('gw');
    expect(essay.questionText).toContain('7.');
    if (guided.rubric.system !== 'language-writing') throw new Error('guided writing');
    const lower = guided.rubric.criteria.find(k => k.id === 'expression')!.limits!.find(k => k.id === 'lower-a')!;
    expect(lower).toMatchObject({minMarks:7,maxMarks:12});
    expect(lower.bands).toBeUndefined();
    expect(lower.guidance.join(' ')).toMatch(/9\s*-\s*11/);
  });
  it('keeps the three birth facts under the printed two-detail quota without a new date/place split', () => {
    const c = points('l4-1-i');
    expect(c.rubric.groups).toHaveLength(3); expect(c.rubric.count).toBe(2);
    expect(languageMarks(c,{...row('answer-1'),...row('answer-2')})).toBe(4);
    expect(languageMarks(c,{...row('answer-1'),...row('answer-2'),...row('answer-3')})).toBe(4);
    expect(c.rubric.markingGuideNote).toContain('does not impose an additional one-date/one-place quota');
  });
});
