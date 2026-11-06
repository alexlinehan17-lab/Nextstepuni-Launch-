import type { LanguageWritingRubric, LanguageWritingCriterion, LanguageLimitCondition, LanguagePointsRubric, SecRubricCard } from '../../types/markBank';

export type LanguageScoreId = `language:${string}`;
export type LanguageScores = Partial<Record<LanguageScoreId, number>>;
export const languageScoreId = (id: string): LanguageScoreId => `language:${id}`;
export const languageLengthId = (unit: 'words' | 'characters'): LanguageScoreId => `language:length:${unit}`;
export const languageFlagId = (id: string): LanguageScoreId => `language:flag:${id}`;
export const languageGroupId = (id: string): LanguageScoreId => `language:group:${id}`;
export const languageRowId = (group: string, row: string): LanguageScoreId => `language:row:${group}:${row}`;

const selectedMark = (criterion: LanguageWritingCriterion, scores: LanguageScores) => {
  const mark = scores[languageScoreId(criterion.id)] ?? 0;
  return criterion.permittedMarks.includes(mark) ? mark : 0;
};

export function languageConditionApplies(rubric: LanguageWritingRubric, condition: LanguageLimitCondition, scores: LanguageScores, visited: string[] = []): boolean {
  if ('flag' in condition) return scores[languageFlagId(condition.flag)] === 1;
  if ('length' in condition) {
    const length = scores[languageLengthId(condition.length)];
    // Until a length is supplied use the lower scale: an omitted answer is
    // never implicit permission to award above a published short-answer cap.
    return length === undefined || !Number.isFinite(length) || length < condition.below;
  }
  return condition.criterionIds.reduce((sum, id) => sum + languageCriterionValue(rubric, id, scores, !!condition.ignoreDeductions, visited), 0) <= condition.atMost;
}

export function languageCriterionLimits(rubric: LanguageWritingRubric, criterion: LanguageWritingCriterion, scores: LanguageScores, visited: string[] = []) {
  return (criterion.limits ?? []).filter(limit => limit.when.any.some(condition => languageConditionApplies(rubric, condition, scores, visited)));
}

export function languageCriterionValue(rubric: LanguageWritingRubric, id: string, scores: LanguageScores, ignoreDeductions = false, visited: string[] = []): number {
  const criterion = rubric.criteria.find(item => item.id === id);
  if (!criterion || visited.includes(id)) return 0;
  const path = [...visited, id];
  const limits = languageCriterionLimits(rubric, criterion, scores, path);
  const cap = Math.min(criterion.maxMarks, ...limits.map(limit => limit.maxMarks));
  const raw = Math.min(selectedMark(criterion, scores), cap);
  if (ignoreDeductions || criterion.kind === 'deduction') return raw;
  const deducted = rubric.criteria.filter(item => item.kind === 'deduction' && item.deductFrom === id)
    .reduce((sum, item) => sum + languageCriterionValue(rubric, item.id, scores, true, path), 0);
  return Math.max(0, raw - deducted);
}

export function languageWritingMarks(rubric: LanguageWritingRubric, scores: LanguageScores): number {
  return rubric.criteria.filter(item => item.kind !== 'deduction')
    .reduce((sum, item) => sum + languageCriterionValue(rubric, item.id, scores), 0);
}

export function languagePointsMarks(rubric: LanguagePointsRubric, scores: LanguageScores): number {
  // Selection is explicit even if every component of an option earned zero.
  // Defensive slicing also prevents stale or tampered state exceeding quota.
  const allocation = rubric.groups.filter(group => scores[languageGroupId(group.id)] === 1).slice(0, rubric.count)
    .reduce((total, group) => total + group.rows.map(row => {
      const selected = scores[languageRowId(group.id, row.id)] ?? 0;
      return row.steps ? row.steps.includes(selected) ? selected : 0 : selected === 1 ? row.marks : 0;
    }).sort((a, b) => b - a).slice(0, group.answerCount ?? group.rows.length).reduce((sum, mark) => sum + mark, 0), 0);
  return allocation + (rubric.criteria ? languageWritingMarks({ ...rubric, system: 'language-writing', criteria: rubric.criteria }, scores) : 0);
}

export function languageMarks(card: SecRubricCard, scores: LanguageScores): number {
  const rubric = card.rubric;
  const marks = rubric.system === 'language-writing' ? languageWritingMarks(rubric, scores)
    : rubric.system === 'language-points' ? languagePointsMarks(rubric, scores) : 0;
  return Math.max(0, Math.min(card.totalMarks, marks));
}
