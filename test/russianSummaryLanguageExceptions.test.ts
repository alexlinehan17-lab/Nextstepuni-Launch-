import { describe, expect, it } from 'vitest';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import { languageFlagId, languageGroupId, languageMarks, languageOtherLanguageId, languageRowId, languageScoreId, type LanguageScores } from '../components/MarkBank/languageScoring';
import { tariffReconciles, type LanguagePointsRubric, type SecRubricCard } from '../types/markBank';

type PointsCard = SecRubricCard & { rubric: LanguagePointsRubric };
const pages = new Map([[2010,7],[2013,6],[2014,6],[2015,7],[2016,6],[2017,6],[2022,7],[2023,7],[2024,8],[2025,7],[2026,7]]);
const ids = [...pages.keys()].flatMap(year => (year === 2010 ? [1,2,3,4,5] : [1,2,3,4]).map(number => `ru-${year}-hl-c2-${number}`));
const get = (id: string): PointsCard => {
  const card = REVIEWED_CARDS.find(card => card.id === id);
  if (!card || card.kind !== 'rubric' || card.rubric.system !== 'language-points') throw new Error(id);
  return { ...card, rubric: card.rubric };
};
const placement = (card: PointsCard): LanguageScores => {
  const group = card.rubric.groups[0];
  const scores: LanguageScores = { [languageGroupId(group.id)]: 1, [languageScoreId('summary-skills')]: 2 };
  const row = group.rows[0];
  if (row) scores[languageRowId(group.id,row.id)] = row.steps?.at(-1) ?? 1;
  for (const criterion of group.criteria ?? []) scores[languageScoreId(criterion.id)] = criterion.maxMarks;
  return scores;
};

describe('source-reviewed Russian manual summary language exceptions', () => {
  it('publishes only the forty prior and five 2010 source-reviewed summary exceptions', () => {
    const actual = REVIEWED_CARDS.filter(card => card.answerLanguageRule?.manualCriterionExceptions).map(card => card.id);
    expect(actual.sort()).toEqual([...ids].sort());
    expect(REVIEWED_CARDS.find(card => card.id === 'ru-2011-hl-c2')?.answerLanguageRule).toBeUndefined();
  });

  it.each(ids)('preserves stored content flags, manual discretion and source caps: %s', id => {
    const card = get(id), rule = card.answerLanguageRule!;
    expect(tariffReconciles(card)).toBe(true);
    expect(rule.otherLanguageMultiplier).toBe(0);
    expect(rule.manualCriterionExceptions).toMatchObject({ criterionIds: ['summary-skills'], schemePages: [pages.get(card.year!)] });
    expect(rule.manualCriterionExceptions!.sourceText).toContain('Discretionary marks');
    const normal = placement(card), normalMarks = languageMarks(card,normal);
    expect(normalMarks).toBeGreaterThan(2);
    const saved = JSON.parse(JSON.stringify({ ...normal, [languageOtherLanguageId('response')]: 1 })) as LanguageScores;
    const before = structuredClone(saved);
    expect(languageMarks(card,saved)).toBe(2);
    expect(languageMarks(card,{ ...saved, [languageOtherLanguageId('response')]: 0 })).toBe(normalMarks);
    expect(languageMarks(card,{ [languageOtherLanguageId('response')]: 1 })).toBe(0);
    expect(languageMarks(card,{ ...saved, [languageScoreId('summary-skills')]: 0 })).toBe(0);
    const criterion = card.rubric.criteria!.find(criterion => criterion.id === 'summary-skills')!;
    for (const limit of criterion.limits ?? []) {
      const flag = limit.when.any.find(condition => 'flag' in condition);
      if (!flag || !('flag' in flag)) throw new Error(`Missing explicit source condition ${id}/${limit.id}`);
      expect(languageMarks(card,{ ...saved, [languageFlagId(flag.flag)]: 1 })).toBe(limit.maxMarks);
    }
    const group = card.rubric.groups[0], row = group.rows[0];
    const local = languageOtherLanguageId(row ? `row:${group.id}:${row.id}` : `group:${group.id}`);
    const mixed = { ...saved, [local]: 1, [languageOtherLanguageId('response')]: 0 };
    expect(languageMarks(card,mixed)).toBe(2);
    expect(saved).toEqual(before);
  });

  it('does not add a manual exception to unrelated language-mandated reading or writing', () => {
    for (const suffix of ['c1-1-i','se','gw']) {
      const card = REVIEWED_CARDS.find(card => card.id === `ru-2025-hl-${suffix}`);
      expect(card?.answerLanguageRule).toBeDefined();
      expect(card?.answerLanguageRule?.manualCriterionExceptions).toBeUndefined();
    }
  });
});
