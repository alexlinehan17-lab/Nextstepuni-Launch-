import type { LanguageWritingRubric, LanguageWritingCriterion, LanguageLimitCondition, LanguagePointsRubric, SecRubricCard, SecCardBase } from '../../types/markBank';

export type LanguageScoreId = `language:${string}`;
export type LanguageScores = Partial<Record<LanguageScoreId, number>>;
/** Derived from the current valid selections, never restored or entered. */
export interface LanguageScoringContext { selectedGroupMarks: number }
export const languageScoreId = (id: string): LanguageScoreId => `language:${id}`;
export const languageLengthId = (unit: 'words' | 'characters'): LanguageScoreId => `language:length:${unit}`;
export const languageFlagId = (id: string): LanguageScoreId => `language:flag:${id}`;
export const languageGroupId = (id: string): LanguageScoreId => `language:group:${id}`;
export const languageRowId = (group: string, row: string): LanguageScoreId => `language:row:${group}:${row}`;
export const languageOtherLanguageId = (target: string): LanguageScoreId => `language:other-language:${target}`;
export const languageCreditMultiplier = (rule: SecCardBase['answerLanguageRule'], scores: LanguageScores, target: string) =>
  rule && scores[languageOtherLanguageId(target)] === 1 ? rule.otherLanguageMultiplier : 1;
export const languageCreditAriaLabel = (rule: NonNullable<SecCardBase['answerLanguageRule']>, label: string) =>
  `${label} answered in ${rule.penalizedLanguage ?? 'another language'}`;
export const languageCreditCondition = (rule: NonNullable<SecCardBase['answerLanguageRule']>, plural = false) =>
  rule.penalizedLanguage
    ? `${plural ? 'All answers are' : 'This answer is'} in ${rule.penalizedLanguage}`
    : `${plural ? 'All answers use' : 'This answer uses'} a language other than specified`;

const selectedMark = (criterion: LanguageWritingCriterion, scores: LanguageScores) => {
  const mark = scores[languageScoreId(criterion.id)] ?? 0;
  return criterion.permittedMarks.includes(mark) ? mark : 0;
};

export function languageConditionApplies(rubric: LanguageWritingRubric, condition: LanguageLimitCondition, scores: LanguageScores, visited: string[] = [], context?: LanguageScoringContext): boolean {
  if ('flag' in condition) return scores[languageFlagId(condition.flag)] === 1;
  if ('length' in condition) {
    const length = scores[languageLengthId(condition.length)];
    // Until a length is supplied use the lower scale: an omitted answer is
    // never implicit permission to award above a published short-answer cap.
    return length === undefined || !Number.isFinite(length) || length < condition.below;
  }
  const selectedGroupMarks = condition.includeSelectedGroupMarks ? context?.selectedGroupMarks ?? 0 : 0;
  return condition.criterionIds.reduce((sum, id) => sum + languageCriterionValue(rubric, id, scores, !!condition.ignoreDeductions, visited, context), selectedGroupMarks) <= condition.atMost;
}

export function languageCriterionLimits(rubric: LanguageWritingRubric, criterion: LanguageWritingCriterion, scores: LanguageScores, visited: string[] = [], context?: LanguageScoringContext) {
  return (criterion.limits ?? []).filter(limit => limit.when.any.some(condition => languageConditionApplies(rubric, condition, scores, visited, context)));
}

/** One active source scale shared by the displayed controls and scorer.
 * Retain raw saved choices so clearing a condition restores the placement.
 * A lower bound restricts positive choices; it never grants minimum credit. */
export function languageCriterionPlacement(rubric: LanguageWritingRubric, criterion: LanguageWritingCriterion, scores: LanguageScores, visited: string[] = [], context?: LanguageScoringContext) {
  if (criterion.automaticAward) {
    const marks = criterion.automaticAward.marks;
    return { limits: [], permitted: [marks], selected: marks, minimum: marks, cap: marks, needsRangeReview: false };
  }
  const limits = languageCriterionLimits(rubric, criterion, scores, visited, context);
  const ceiling = Math.min(criterion.maxMarks, ...limits.map(limit => limit.maxMarks));
  const minimum = Math.max(0, ...limits.map(limit => limit.minMarks ?? 0));
  const permitted = criterion.permittedMarks.filter(mark => mark === 0 || (mark >= minimum && mark <= ceiling));
  const stored = selectedMark(criterion, scores);
  const capped = Math.min(stored, ceiling);
  const selected = permitted.includes(capped) ? capped : 0;
  return { limits, permitted, selected, minimum, cap: Math.max(0, ...permitted),
    needsRangeReview: minimum > 0 && stored > 0 && !permitted.includes(stored) };
}

export function languageCriterionValue(rubric: LanguageWritingRubric, id: string, scores: LanguageScores, ignoreDeductions = false, visited: string[] = [], context?: LanguageScoringContext): number {
  const criterion = rubric.criteria.find(item => item.id === id);
  if (!criterion || visited.includes(id)) return 0;
  const path = [...visited, id];
  const { selected: raw } = languageCriterionPlacement(rubric, criterion, scores, path, context);
  if (ignoreDeductions || criterion.kind === 'deduction') return raw;
  const deducted = rubric.criteria.filter(item => item.kind === 'deduction' && item.deductFrom === id)
    .reduce((sum, item) => sum + languageCriterionValue(rubric, item.id, scores, true, path, context), 0);
  return Math.max(0, raw - deducted);
}

export function languageWritingMarks(rubric: LanguageWritingRubric, scores: LanguageScores, context?: LanguageScoringContext): number {
  return rubric.criteria.filter(item => item.kind !== 'deduction')
    .reduce((sum, item) => sum + languageCriterionValue(rubric, item.id, scores, false, [], context), 0);
}

/** Inconsistent restored selections must be resolved by the student. Do not
 * silently pick a preferred alternative or award both ways of saying it. */
export function languageAlternativeConflicts(rubric: LanguagePointsRubric, scores: LanguageScores): Set<string> {
  const counts = new Map<string, number>();
  for (const group of rubric.groups) if (group.alternativeSet && scores[languageGroupId(group.id)] === 1) {
    counts.set(group.alternativeSet, (counts.get(group.alternativeSet) ?? 0) + 1);
  }
  return new Set([...counts].filter(([, count]) => count > 1).map(([id]) => id));
}

/** Apply only conditions the student explicitly marked as present in the
 * actual response. Selected answer labels do not infer its wording. */
export function languageAllocationMaximum(rubric: LanguagePointsRubric, scores: LanguageScores): number {
  const cap = rubric.allocationCap;
  return Math.min(cap?.maxMarks ?? Infinity, ...(cap?.limits ?? [])
    .filter(limit => scores[languageFlagId(limit.when.flag)] === 1).map(limit => limit.maxMarks));
}

/** Only a valid, explicitly selected reduced category funds an increased one.
 * Invalid restored combinations retain normal credit and require reassessment;
 * never silently choose which of several increased categories gets priority. */
export function languageCategoryCompensation(rubric: LanguagePointsRubric, scores: LanguageScores) {
  const rule = rubric.allocationCap?.categoryCompensation;
  if (!rule) return undefined;
  const values = new Map(rubric.groups.filter(group => scores[languageGroupId(group.id)] === 1).slice(0, rubric.count).map(group => {
    const row = group.rows[0];
    const raw = row ? scores[languageRowId(group.id, row.id)] ?? 0 : 0;
    return [group.id, row?.steps?.includes(raw) ? raw : 0] as const;
  }));
  const reducedCount = [...values.values()].filter(mark => mark === rule.reducedMarks).length;
  const increasedCount = [...values.values()].filter(mark => mark > rule.normalMarks).length;
  return { ...rule, values, reducedCount, increasedCount, needsReview: increasedCount > reducedCount };
}

export function languagePointsAllocation(rubric: LanguagePointsRubric, scores: LanguageScores, rule?: SecCardBase['answerLanguageRule']): number {
  // The response flag supersedes individual adjustments without compounding
  // them. Source-defined exceptions can retain named manual criteria; neither
  // those exceptions nor clearing the flag changes the stored placements.
  const responseMultiplier = languageCreditMultiplier(rule, scores, 'response');
  const individualRule = responseMultiplier === 1 ? rule : undefined;
  // Selection is explicit even if every component of an option earned zero.
  // Defensive slicing also prevents stale or tampered state exceeding quota.
  const conflicts = languageAlternativeConflicts(rubric, scores);
  const selectedGroups = rubric.groups.filter(group => scores[languageGroupId(group.id)] === 1
    && (!group.alternativeSet || !conflicts.has(group.alternativeSet))).slice(0, rubric.count);
  const compensation = languageCategoryCompensation(rubric, scores);
  const rowMarks = selectedGroups.flatMap(group => group.rows.map(row => {
      const selected = scores[languageRowId(group.id, row.id)] ?? 0;
      const earned = row.steps ? row.steps.includes(selected) ? selected : 0 : selected === 1 ? row.marks : 0;
      const placed = compensation?.needsReview ? Math.min(earned, compensation.normalMarks) : earned;
      return placed * languageCreditMultiplier(individualRule, scores, `row:${group.id}:${row.id}`);
    }).sort((a, b) => b - a).slice(0, group.answerCount ?? group.rows.length));
  const rowAllocation = rowMarks.sort((a, b) => b - a).slice(0, rubric.allocationCap?.answerCount ?? rowMarks.length)
    .reduce((sum, mark) => sum + mark, 0);
  const groupCriteria = selectedGroups.reduce((sum, group) => sum + (group.criteria
    ? languageWritingMarks({ ...rubric, system: 'language-writing', criteria: group.criteria }, scores)
      * languageCreditMultiplier(individualRule, scores, `group:${group.id}`) : 0), 0);
  return Math.min(rowAllocation + groupCriteria, languageAllocationMaximum(rubric, scores));
}

export function languagePointsMarks(rubric: LanguagePointsRubric, scores: LanguageScores, rule?: SecCardBase['answerLanguageRule']): number {
  const responseMultiplier = languageCreditMultiplier(rule, scores, 'response');
  const allocation = languagePointsAllocation(rubric, scores, rule);
  const context = { selectedGroupMarks: allocation };
  const manualRubric: LanguageWritingRubric = { ...rubric, system: 'language-writing', criteria: rubric.criteria ?? [] };
  const exceptions = rule?.manualCriterionExceptions?.criterionIds ?? [];
  if (!exceptions.length) return (allocation + languageWritingMarks(manualRubric, scores, context)) * responseMultiplier;
  const manualMarks = manualRubric.criteria.filter(criterion => criterion.kind !== 'deduction')
    .reduce((sum, criterion) => sum + languageCriterionValue(manualRubric, criterion.id, scores, false, [], context)
      * (exceptions.includes(criterion.id) ? 1 : responseMultiplier), 0);
  return allocation * responseMultiplier + manualMarks;
}

export function languageMarks(card: SecRubricCard, scores: LanguageScores): number {
  const rubric = card.rubric;
  const marks = rubric.system === 'language-writing' ? languageWritingMarks(rubric, scores) * languageCreditMultiplier(card.answerLanguageRule, scores, 'response')
    : rubric.system === 'language-points' ? languagePointsMarks(rubric, scores, card.answerLanguageRule) : 0;
  return Math.max(0, Math.min(card.totalMarks, marks));
}
