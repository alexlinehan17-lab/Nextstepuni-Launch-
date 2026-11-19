import React, { useState } from 'react';
import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import LanguageRubricPanel from '../components/MarkBank/LanguageRubricPanel';
import { languageMarks, languageGroupId, languageRowId, languageScoreId, languageOtherLanguageId, type LanguageScores } from '../components/MarkBank/languageScoring';
import { tariffReconciles, type LanguagePointsRubric, type SecRubricCard } from '../types/markBank';

type PointsCard = SecRubricCard & { rubric: LanguagePointsRubric };
const fixture = (id = 'ru-2026-hl-c2-1'): PointsCard => {
  const card = structuredClone(REVIEWED_CARDS.find(candidate => candidate.id === id));
  if (!card || card.kind !== 'rubric' || card.rubric.system !== 'language-points' || !card.answerLanguageRule) throw new Error(id);
  const guidance = card.rubric.taskRequirements.find(text => text.includes('unable to express what they understand in intelligible English'));
  if (!guidance) throw new Error('Missing original discretionary-language exception');
  const start = guidance.lastIndexOf('Discretionary marks', guidance.indexOf('unable to express'));
  const end = guidance.indexOf('If a candidate fails', start);
  if (start < 0 || end < 0) throw new Error('Missing original exception boundary');
  card.answerLanguageRule.manualCriterionExceptions = {
    criterionIds: ['summary-skills'], sourceText: guidance.slice(start, end).trim(),
    schemePages: [card.year === 2026 ? 7 : 6],
  };
  return card as PointsCard;
};

const fullPlacement = (card: PointsCard): LanguageScores => {
  const scores: LanguageScores = { 'language:summary-skills': 2 };
  for (const group of card.rubric.groups.slice(0, card.rubric.count)) {
    scores[languageGroupId(group.id)] = 1;
    for (const row of group.rows) scores[languageRowId(group.id, row.id)] = row.steps?.at(-1) ?? 1;
    for (const criterion of group.criteria ?? []) scores[languageScoreId(criterion.id)] = criterion.maxMarks;
  }
  return scores;
};

describe('published exceptions for manually assessed language criteria', () => {
  it.each(['ru-2026-hl-c2-1', 'ru-2013-hl-c2-2'])('retains saved content adjustments and only exempts the named manual criterion: %s', id => {
    const card = fixture(id);
    const saved = { ...fullPlacement(card), [languageOtherLanguageId('response')]: 1 };
    const before = structuredClone(saved);
    expect(tariffReconciles(card)).toBe(true);
    expect(languageMarks(card, saved)).toBe(2);
    expect(saved).toEqual(before);
    expect(languageMarks(card, { ...saved, [languageOtherLanguageId('response')]: 0 })).toBe(10);
    const legacy = structuredClone(card);
    delete legacy.answerLanguageRule!.manualCriterionExceptions;
    expect(languageMarks(legacy, saved)).toBe(0);
  });

  it('does not override incomplete or source-specific zero discretion caps, or grant an unplaced mark', () => {
    const card = fixture('ru-2016-hl-c2-4');
    const saved: LanguageScores = { ...fullPlacement(card), 'language:other-language:response': 1 };
    expect(languageMarks(card, { ...saved, 'language:flag:incomplete-response': 1 })).toBe(1);
    expect(languageMarks(card, { ...saved, 'language:flag:missed-return-delay': 1 })).toBe(0);
    expect(languageMarks(card, { ...saved, 'language:summary-skills': 0 })).toBe(0);
    expect(languageMarks(card, { ...saved, 'language:summary-skills': 99 })).toBe(0);
    expect(languageMarks(card, { 'language:other-language:response': 1 })).toBe(0);
  });

  it('retains individual adjustments when the whole-response flag is cleared', () => {
    const card = fixture();
    const group = card.rubric.groups[0];
    const individual = languageOtherLanguageId(`row:${group.id}:${group.rows[0].id}`);
    const saved: LanguageScores = { ...fullPlacement(card), [individual]: 1, 'language:other-language:response': 1 };
    expect(languageMarks(card, saved)).toBe(2);
    expect(languageMarks(card, { ...saved, 'language:other-language:response': 0 })).toBe(8);
    expect(saved[individual]).toBe(1);
  });

  it.each([
    { criterionIds: [] }, { criterionIds: ['summary-skills', 'summary-skills'] },
    { criterionIds: ['missing'] }, { criterionIds: [' '] }, { criterionIds: ['answer-1'] },
    { sourceText: ' ' }, { schemePages: [] }, { schemePages: [0] }, { schemePages: [1.5] },
  ])('rejects unbound exception metadata %j', change => {
    const card = fixture();
    Object.assign(card.answerLanguageRule!.manualCriterionExceptions!, change);
    expect(tariffReconciles(card)).toBe(false);
  });

  it('rejects group-only criteria and deductions as manual exceptions', () => {
    const card = fixture('ru-2013-hl-c2-2');
    const groupCriterion = card.rubric.groups.flatMap(group => group.criteria ?? [])[0];
    expect(groupCriterion).toBeDefined();
    card.answerLanguageRule!.manualCriterionExceptions!.criterionIds = [groupCriterion.id];
    expect(tariffReconciles(card)).toBe(false);
    card.answerLanguageRule!.manualCriterionExceptions!.criterionIds = ['summary-skills'];
    card.rubric.criteria![0].kind = 'deduction';
    expect(tariffReconciles(card)).toBe(false);
  });

  it('rejects response-level exceptions on a standalone writing rubric', () => {
    const card = fixture();
    const writing: SecRubricCard = { ...card, totalMarks: 2,
      rubric: { system: 'language-writing', criteria: card.rubric.criteria!,
        taskRequirements: card.rubric.taskRequirements, markingGuideNote: card.rubric.markingGuideNote } };
    expect(tariffReconciles(writing)).toBe(false);
    delete writing.answerLanguageRule!.manualCriterionExceptions;
    expect(tariffReconciles(writing)).toBe(true);
  });

  it('shows the source exception and restored language flag without restoring content credit', () => {
    const card = fixture();
    function Harness() {
      const [scores, setScores] = useState<LanguageScores>({ ...fullPlacement(card), 'language:other-language:response': 1 });
      return <LanguageRubricPanel card={card} scores={scores} onScore={(id, value) => setScores(old => ({ ...old, [id]: value }))} />;
    }
    render(<Harness />);
    const flag = screen.getByRole('checkbox', { name: 'All answers answered in another language' });
    expect(flag).toBeChecked();
    expect(screen.getByText('2 / 10')).toBeInTheDocument();
    expect(screen.getByText(/content: no credit/)).toBeInTheDocument();
    expect(screen.getByText('Assess Discretionary marks separately under the source guidance.')).toBeInTheDocument();
    expect(screen.getByText(card.answerLanguageRule!.manualCriterionExceptions!.sourceText)).toBeInTheDocument();
    fireEvent.click(flag);
    expect(screen.getByText('10 / 10')).toBeInTheDocument();
    fireEvent.click(flag);
    expect(screen.getByText('2 / 10')).toBeInTheDocument();
  });
});
