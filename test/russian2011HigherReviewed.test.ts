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
const summary = (content: number, discretion: number) => ({
  [languageGroupId('complete-response')]: 1,
  ...Object.fromEntries([1,2,3,4].flatMap(n => [[languageScoreId(`section-${n}-content`), content], [languageScoreId(`section-${n}-discretion`), discretion]])),
});

describe('Russian 2011 Higher reviewed original allocations', () => {
  it('preserves 39 original asks as 35 independent tasks and one joint four-summary task', () => {
    expect(sitting).toHaveLength(36);
    expect(sitting.filter(c => !tariffReconciles(c)).map(c => c.id)).toEqual([]);
    expect(sitting.reduce((sum,c) => sum+c.totalMarks,0)).toBe(300);
    expect(sitting.filter(c => c.audioMaterial)).toHaveLength(20);
    expect(sitting.filter(c => c.audioMaterial).reduce((sum,c) => sum+c.totalMarks,0)).toBe(80);
    expect(sitting.filter(c => c.section === 'C2')).toHaveLength(1);
  });
  it('retains four complete summary prompts and passage pages under the collective 45', () => {
    const c = points('c2');
    expect(c.questionText.match(/Give five details\./g)).toHaveLength(4);
    expect(c.sourceMaterial?.pages).toEqual([6,7,8,9]);
    expect(c.rubric.groups).toHaveLength(1);
    expect(c.rubric.groups[0].criteria?.map(k => k.maxMarks)).toEqual([10,2,10,2,10,2,10,2]);
    expect(c.rubric.markingGuideNote).toContain('paper gives 40');
    expect(c.rubric.markingGuideNote).toContain('without assigning a fixed 11/12 split');
  });
  it('caps the whole response at 45 without assigning unequal section totals', () => {
    const c = points('c2');
    expect(languageMarks(c,summary(10,1))).toBe(44);
    expect(languageMarks(c,summary(10,2))).toBe(45);
    const scores = summary(0,0);
    scores[languageScoreId('section-3-content')] = 10;
    scores[languageScoreId('section-3-discretion')] = 2;
    expect(languageMarks(c,scores)).toBe(12);
    expect(languageMarks(c,{})).toBe(0);
  });
  it('withholds all four discretionary awards for the explicit incomplete-response condition and restores choices', () => {
    const c = points('c2'), scores = summary(10,2);
    const flagged = {...scores,[languageFlagId('incomplete-summary-response')]:1};
    expect(languageMarks(c,flagged)).toBe(40);
    expect(languageMarks(c,{...flagged,[languageFlagId('incomplete-summary-response')]:0})).toBe(45);
    expect(scores[languageScoreId('section-4-discretion')]).toBe(2);
  });
  it('keeps the language exception manual while preserving both original rules beside every criterion', () => {
    const c = points('c2');
    expect(c.answerLanguageRule).toBeUndefined();
    for (const criterion of c.rubric.groups[0].criteria ?? []) {
      const guide = criterion.guidance.join(' ');
      expect(guide).toContain('award NO marks');
      expect(guide).toContain('Discretionary marks may be awarded');
      expect(guide).toMatch(/Russian-\s*language words/);
    }
    const scores = summary(0,0); scores[languageScoreId('section-1-discretion')] = 2;
    expect(languageMarks(c,scores)).toBe(2);
    expect(languageMarks(c,{...scores,[languageOtherLanguageId('response')]:1})).toBe(2);
    expect(sitting.filter(c => c.answerLanguageRule)).toHaveLength(12);
    expect(sitting.filter(c => c.audioMaterial).every(c => !c.answerLanguageRule)).toBe(true);
  });
  it('keeps every nested summary condition within explicitly manual content assessment', () => {
    const c = points('c2'), criteria = c.rubric.groups[0].criteria!;
    const second = criteria.find(k => k.id === 'section-2-content')!.guidance.join(' ');
    const third = criteria.find(k => k.id === 'section-3-content')!.guidance.join(' ');
    expect(second).toContain('all four categories are required');
    expect(second).toContain('maximum of two marks');
    expect(third).toMatch(/any two/i);
    expect(third).toMatch(/maximum of 4/i);
    expect(c.rubric.markingGuideNote).toContain('do not count or classify individual details');
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
