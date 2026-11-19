import { describe, expect, it } from 'vitest';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import { CARDS } from '../components/MarkBank/cards/russian/ordinary';
import { languageMarks, languageScoreId, languageFlagId, languageGroupId, languageRowId } from '../components/MarkBank/languageScoring';
import { isRubricCard, tariffReconciles } from '../types/markBank';

const reviewed = REVIEWED_CARDS.filter(card => card.year === 2026 && card.level === 'ordinary');
const get = (suffix: string) => {
  const card = reviewed.find(card => card.id === `ru-2026-ol-${suffix}`);
  if (!card) throw new Error(suffix);
  return card;
};

describe('Russian 2026 Ordinary original-source tasks', () => {
  it('covers all 56 independently counted tasks and all 320 marks', () => {
    expect(reviewed).toHaveLength(56);
    expect(CARDS.length).toBeGreaterThanOrEqual(172);
    expect(reviewed.every(tariffReconciles)).toBe(true);
    const written = reviewed.filter(card => !card.audioMaterial);
    const listening = reviewed.filter(card => card.audioMaterial);
    expect(written).toHaveLength(31);
    expect(listening).toHaveLength(25);
    expect(written.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(220);
    expect(listening.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(100);
    expect(listening.every(card => card.paperFileid === 'LC099GLPA00BV')).toBe(true);
  });

  it('keeps all four required event headings in one task', () => {
    const card = get('ir2-1');
    if (card.kind !== 'question') throw new Error('Missing event table');
    expect(card.rows.map(row => row.contextNote?.split('\n')[0])).toEqual(['Day of the week', 'Date', 'Year', 'Time']);
    expect(card.rows.map(row => row.marks)).toEqual([1, 1, 1, 1]);
  });

  it('retains the two complete discourse routes under one question', () => {
    const card = get('sd');
    if (card.kind !== 'question') throw new Error('Missing dialogue');
    expect(card.answerVariants).toHaveLength(2);
    for (const route of card.answerVariants ?? []) {
      expect(route.rows).toHaveLength(5);
      expect(route.rows.reduce((sum, row) => sum + (row.marks ?? 0), 0)).toBe(20);
    }
    expect(card.sourceMaterial?.pages).toEqual([10, 11]);
    expect(card.questionText).toContain('Group A');
    expect(card.questionText).toContain('Group B');
    expect(card.questionText).toContain('suitable word');
  });

  it('marks three chosen cursive phrases with the actual 0/1/2 grid', () => {
    const card = get('la2');
    if (!isRubricCard(card) || card.rubric.system !== 'language-writing') throw new Error('Missing handwriting grid');
    expect(card.rubric.criteria).toHaveLength(3);
    expect(card.rubric.criteria.every(criterion => criterion.permittedMarks.join() === '0,1,2')).toBe(true);
    expect(card.questionText).toContain('музыкальная школа');
    expect(card.questionText).toContain('классическая музыка');
    expect(languageMarks(card, { [languageScoreId('phrase-1')]: 2, [languageScoreId('phrase-2')]: 1 })).toBe(3);
  });

  it('uses the printed writing prices and lower-expression triggers', () => {
    const card = get('ew');
    if (!isRubricCard(card) || card.rubric.system !== 'language-writing') throw new Error('Missing writing grid');
    expect(card.rubric.criteria[0].permittedMarks).toEqual([0, 2, 4, 6, 8, 10, 12]);
    const marks = { [languageScoreId('content')]: 12, [languageScoreId('expression')]: 12, [languageScoreId('coherence')]: 6 };
    expect(languageMarks(card, marks)).toBe(30);
    expect(languageMarks(card, { ...marks, [languageScoreId('content')]: 6 })).toBe(21);
    expect(languageMarks(card, { ...marks, [languageFlagId('fewer-six-sentences')]: 1 })).toBe(27);
    const culture = get('sa');
    if (!isRubricCard(culture) || culture.rubric.system !== 'language-writing') throw new Error('Missing cultural writing');
    expect(culture.rubric.criteria[0].permittedMarks).toEqual([0, 4, 8, 12, 16, 20, 24]);
    expect(culture.rubric.criteria[1].permittedMarks).toEqual([0, 2, 4, 6]);
  });

  it('retains the 3-mark listening price with its named 1-mark partial', () => {
    const card = get('l1-2-ii');
    if (!isRubricCard(card) || card.rubric.system !== 'language-points') throw new Error('Missing listening grid');
    const scores = { [languageGroupId('answer-2')]: 1, [languageRowId('answer-2', 'partial-1')]: 1 };
    expect(languageMarks(card, scores)).toBe(1);
    expect(languageMarks(card, { ...scores, [languageRowId('answer-2', 'full')]: 1 })).toBe(3);
    const family = get('l2-1-i');
    if (!isRubricCard(family) || family.rubric.system !== 'language-points') throw new Error('Missing family answers');
    expect(family.rubric.groups[0].rows[0].text).toBe('Russian was always part of his family culture');
    expect(family.rubric.groups[4].rows[0].text).toBe('They mostly use only basic Russian words');
    expect(get('l4-3-ii').questionRef).toBe('2026 OL Section L4 Q3(ii)');
  });
});
