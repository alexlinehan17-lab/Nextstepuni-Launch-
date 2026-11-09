import React, { useState } from 'react';
import { describe, expect, it } from 'vitest';
import { fireEvent, render, screen, within } from '@testing-library/react';
import { tariffReconciles, type LanguagePointsRubric, type LanguageWritingCriterion, type SecRubricCard, type SecQuestionCard } from '../types/markBank';
import { languageMarks, type LanguageScores } from '../components/MarkBank/languageScoring';
import LanguageRubricPanel from '../components/MarkBank/LanguageRubricPanel';

const rule = { otherLanguageMultiplier: 0.5 as const, sourceText: 'Where answers are in the language other than specified, award half marks.', schemePages: [3] };
// Japanese 2026 OL Q5, original scheme pp11–12: any five responses,
// independently C5/E5. The printed bands begin at1, not an invented0 band.
const criterion = (question: number, kind: 'content' | 'expression'): LanguageWritingCriterion => ({
  id: `q${question}-${kind}`, label: `Question ${question} ${kind}`, maxMarks: 5,
  permittedMarks: [0, 1, 2, 3, 4, 5], guidance: [], bands: [
    { label: '1', marks: [1], guidance: [kind === 'content' ? 'Very short answer to questions' : 'Vocabulary very inadequate'] },
    { label: '2–3', marks: [2, 3], guidance: [kind === 'content' ? 'Partial answer to question' : 'Vocabulary use quite good'] },
    { label: '4–5', marks: [4, 5], guidance: [kind === 'content' ? 'Full answer to questions' : 'Vocabulary use good'] },
  ],
});
const rubric: LanguagePointsRubric = { system: 'language-points', count: 5, taskRequirements: ['Answer any five.'], markingGuideNote: '',
  groups: Array.from({ length: 8 }, (_, index) => ({ id: `q${index + 1}`, label: `Response ${index + 1}`, rows: [],
    criteria: [criterion(index + 1, 'content'), criterion(index + 1, 'expression')] })) };
const card = { kind: 'rubric', rubric, totalMarks: 50, answerLanguageRule: rule } as SecRubricCard & { rubric: LanguagePointsRubric };

describe('selected language writing responses and source-defined half credit', () => {
  it.each(['English', 'Japanese'] as const)('shows a source condition limited to %s without broadening it', penalizedLanguage => {
    const scoped = { ...card, answerLanguageRule: { ...rule, penalizedLanguage } };
    expect(tariffReconciles(scoped)).toBe(true);
    const calls: string[] = [];
    render(<LanguageRubricPanel card={scoped} scores={{ 'language:group:q1': 1 }} onScore={id => calls.push(id)} />);
    const response = screen.getByRole('checkbox', { name: `Response 1 answered in ${penalizedLanguage}` });
    fireEvent.click(response);
    expect(calls).toEqual(['language:other-language:group:q1']);
    expect(screen.getByText(`All answers are in ${penalizedLanguage} · half credit`)).toBeInTheDocument();
    expect(screen.queryByRole('checkbox', { name: /answered in another language/ })).not.toBeInTheDocument();
  });

  it('prices five independently placed responses and never counts an unselected or sixth response', () => {
    expect(tariffReconciles(card)).toBe(true);
    const scores: LanguageScores = {};
    for (let q = 1; q <= 8; q++) {
      scores[`language:q${q}-content`] = 5;
      scores[`language:q${q}-expression`] = 5;
    }
    expect(languageMarks(card, scores)).toBe(0);
    scores['language:group:q8'] = 1;
    scores['language:q8-content'] = 3;
    expect(languageMarks(card, scores)).toBe(8);
    for (let q = 1; q <= 6; q++) scores[`language:group:q${q}`] = 1;
    expect(languageMarks(card, scores)).toBe(50);
    for (let q = 2; q <= 4; q++) scores[`language:group:q${q}`] = 0;
    expect(languageMarks(card, scores)).toBe(38);
  });

  it('rejects duplicate criterion IDs and any missing positive source band', () => {
    const duplicate = structuredClone(card);
    duplicate.rubric.groups[1].criteria![0].id = 'q1-content';
    expect(tariffReconciles(duplicate)).toBe(false);
    const missing = structuredClone(card);
    missing.rubric.groups[0].criteria![0].bands!.pop();
    expect(tariffReconciles(missing)).toBe(false);
  });

  it('rejects grouped controls that have no response-scoped length or flag input', () => {
    for (const condition of [{ length: 'characters' as const, below: 20 }, { flag: 'wrong-task', prompt: 'Wrong task' }]) {
      const unsupported = structuredClone(card);
      unsupported.rubric.groups[0].criteria![1].limits = [{ id: 'limited', maxMarks: 3, when: { any: [condition] }, guidance: [] }];
      expect(tariffReconciles(unsupported)).toBe(false);
    }
  });

  it('refuses language rules on scoring systems that do not apply them', () => {
    const point = { kind: 'question', totalMarks: 1, tariffModel: { kind: 'fixed' },
      rows: [{ id: 'a', kind: 'point', verbatim: 'Accepted answer', marks: 1 }] } as SecQuestionCard;
    expect(tariffReconciles({ ...point, answerLanguageRule: rule })).toBe(true);
    const whole = { ...point, tariffModel: { kind: 'questionTotal', notation: '1 mark' },
      rows: [{ ...point.rows[0], marks: null }] } as SecQuestionCard;
    expect(tariffReconciles(whole)).toBe(true);
    expect(tariffReconciles({ ...whole, answerLanguageRule: rule })).toBe(false);
    const scale = { ...point, mathematicsScale: { code: '1A', marks: [0, 1], fullCreditMinusOne: false, schemePages: [1], generalNotesPages: [1] } } as SecQuestionCard;
    expect(tariffReconciles(scale)).toBe(true);
    expect(tariffReconciles({ ...scale, answerLanguageRule: rule })).toBe(false);
    const otherRubric = { kind: 'rubric', totalMarks: 1, rubric: { system: 'politics', schemeFileid: 'fixture', schemePages: [1],
      criteria: [{ id: 'content', label: 'Content', maxMarks: 1, permittedMarks: [0, 1] }] } } as SecRubricCard;
    expect(tariffReconciles(otherRubric)).toBe(true);
    expect(tariffReconciles({ ...otherRubric, answerLanguageRule: rule })).toBe(false);
  });

  it('keeps a selected response content cap independent from the other responses', () => {
    const capped = structuredClone(card);
    capped.rubric.groups[0].criteria![1].limits = [{ id: 'limited', maxMarks: 3,
      when: { any: [{ criterionIds: ['q1-content'], atMost: 2 }] }, guidance: [] }];
    expect(tariffReconciles(capped)).toBe(true);
    const scores: LanguageScores = { 'language:group:q1': 1, 'language:q1-content': 2, 'language:q1-expression': 5,
      'language:other-language:group:q1': 1, 'language:group:q2': 1, 'language:q2-content': 5, 'language:q2-expression': 5 };
    expect(languageMarks(capped, scores)).toBe(12.5);
    expect(languageMarks(capped, { ...scores, 'language:q1-content': 3 })).toBe(14);
  });

  it('keeps mixed-language responses separate and retains fractional earned credit', () => {
    const scores: LanguageScores = { 'language:group:q1': 1, 'language:q1-content': 5, 'language:q1-expression': 4,
      'language:other-language:group:q1': 1, 'language:group:q2': 1, 'language:q2-content': 5, 'language:q2-expression': 5 };
    expect(languageMarks(card, scores)).toBe(14.5);
    expect(languageMarks({ ...card, answerLanguageRule: undefined }, scores)).toBe(19);
    expect(languageMarks(card, { ...scores, 'language:group:q1': 0 })).toBe(10);
  });

  it('applies a source-defined zero-credit rule only to the flagged response', () => {
    const zeroRule = { otherLanguageMultiplier: 0 as const, sourceText: 'Answers in a language other than that required are not awarded marks.', schemePages: [3] };
    const zeroCard = { ...card, answerLanguageRule: zeroRule };
    const scores: LanguageScores = { 'language:group:q1': 1, 'language:q1-content': 5, 'language:q1-expression': 4,
      'language:other-language:group:q1': 1, 'language:group:q2': 1, 'language:q2-content': 5, 'language:q2-expression': 5 };
    expect(tariffReconciles(zeroCard)).toBe(true);
    expect(languageMarks(zeroCard, scores)).toBe(10);
    render(<LanguageRubricPanel card={zeroCard} scores={scores} onScore={() => {}} />);
    expect(screen.getAllByText('This answer uses a language other than specified · no credit')).toHaveLength(8);
    expect(screen.queryByText(/half credit/)).not.toBeInTheDocument();
  });

  it('adjusts a wholly wrong-language response once, including discretionary marks', () => {
    // Synthetic summary fixture: a correct detail and a separate discretionary
    // criterion. A mixed response can retain discretion; an explicitly wholly
    // wrong-language response obeys the whole-answer rule.
    const grouped: LanguagePointsRubric = { ...rubric, count: 1,
      groups: [{ id: 'detail', label: 'Detail', rows: [{ id: 'answer', text: 'Fixture detail', marks: 2 }] }],
      criteria: [{ id: 'discretion', label: 'Discretionary credit', maxMarks: 2, permittedMarks: [0, 1, 2], guidance: [] }],
    };
    const summary = { ...card, rubric: grouped, totalMarks: 4 };
    const scores: LanguageScores = { 'language:group:detail': 1, 'language:row:detail:answer': 1,
      'language:other-language:row:detail:answer': 1, 'language:discretion': 2 };
    expect(languageMarks(summary, scores)).toBe(3);
    expect(languageMarks(summary, { ...scores, 'language:other-language:response': 1 })).toBe(2);
    const zeroRule = { ...summary, answerLanguageRule: { ...rule, otherLanguageMultiplier: 0 as const } };
    expect(languageMarks(zeroRule, scores)).toBe(2);
    expect(languageMarks(zeroRule, { ...scores, 'language:other-language:response': 1 })).toBe(0);
    expect(languageMarks({ ...summary, answerLanguageRule: undefined }, { ...scores, 'language:other-language:response': 1 })).toBe(4);
  });

  it('halves only the marked answer row, including named one-mark partial credit', () => {
    const grouped: LanguagePointsRubric = { ...rubric, count: 1, groups: [{ id: 'kanji', label: 'Kanji', rows: [
      { id: 'reading', text: 'Reading', marks: 1 }, { id: 'meaning', text: 'Meaning', marks: 2, steps: [0, 1, 2] },
    ] }] };
    const pointCard = { ...card, rubric: grouped, totalMarks: 3 };
    const scores: LanguageScores = { 'language:group:kanji': 1, 'language:row:kanji:reading': 1, 'language:row:kanji:meaning': 1,
      'language:other-language:row:kanji:meaning': 1 };
    expect(languageMarks(pointCard, scores)).toBe(1.5);
    expect(languageMarks(pointCard, { ...scores, 'language:other-language:row:kanji:reading': 1 })).toBe(1);
    expect(languageMarks(pointCard, { ...scores, 'language:row:kanji:meaning': 2 })).toBe(2);
    expect(languageMarks(pointCard, { ...scores, 'language:group:kanji': 0 })).toBe(0);
  });

  it('applies half credit after the source expression cap for a whole written response', () => {
    const writingCard: SecRubricCard = { ...card, totalMarks: 10, rubric: { system: 'language-writing', taskRequirements: [], markingGuideNote: '',
      criteria: [criterion(1, 'content'), { ...criterion(1, 'expression'), limits: [{ id: 'source-cap', maxMarks: 3,
        when: { any: [{ criterionIds: ['q1-content'], atMost: 2 }] }, guidance: [] }] }] } };
    const scores: LanguageScores = { 'language:q1-content': 2, 'language:q1-expression': 5, 'language:other-language:response': 1 };
    expect(languageMarks(writingCard, scores)).toBe(2.5);
    expect(languageMarks(writingCard, { ...scores, 'language:other-language:response': 0 })).toBe(5);
    expect(tariffReconciles({ ...writingCard, answerLanguageRule: { ...rule, schemePages: [] } })).toBe(false);
  });

  it('keeps response placement disabled until selected and exposes explicit half-credit controls', () => {
    function Harness() {
      const [scores, setScores] = useState<LanguageScores>({});
      return <LanguageRubricPanel card={card} scores={scores} onScore={(id, value) => setScores(old => ({ ...old, [id]: value }))} />;
    }
    render(<Harness />);
    const content = screen.getByRole('group', { name: 'Question 1 content mark' });
    expect(within(content).getByRole('button', { name: 'Set Question 1 content to 5 marks' })).toBeDisabled();
    fireEvent.click(screen.getByRole('button', { name: 'Response 1' }));
    fireEvent.click(within(content).getByRole('button', { name: 'Set Question 1 content to 5 marks' }));
    fireEvent.click(screen.getByRole('button', { name: 'Set Question 1 expression to 4 marks' }));
    fireEvent.click(screen.getByRole('checkbox', { name: 'Response 1 answered in another language' }));
    expect(screen.getByText('4.5 / 50')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('checkbox', { name: 'All answers answered in another language' }));
    expect(screen.getByText('4.5 / 50')).toBeInTheDocument();
    expect(screen.getByRole('checkbox', { name: 'Response 1 answered in another language' })).toBeDisabled();
    fireEvent.click(screen.getByRole('checkbox', { name: 'All answers answered in another language' }));
    expect(screen.getByRole('checkbox', { name: 'Response 1 answered in another language' })).toBeEnabled();
    for (let q = 2; q <= 5; q++) fireEvent.click(screen.getByRole('button', { name: `Response ${q}` }));
    expect(screen.getByRole('button', { name: 'Response 6' })).toBeDisabled();
    expect(screen.getByText(rule.sourceText)).toBeInTheDocument();
  });
});
