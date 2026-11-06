import { describe, expect, it } from 'vitest';
import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { tariffReconciles, type LanguageWritingRubric, type LanguagePointsRubric, type SecRubricCard } from '../types/markBank';
import LanguageRubricPanel from '../components/MarkBank/LanguageRubricPanel';
import { languageWritingMarks, languagePointsMarks, languageCriterionValue, languageCriterionLimits, type LanguageScores } from '../components/MarkBank/languageScoring';

const steps = (max: number) => Array.from({ length: max + 1 }, (_, i) => i);
// SEC Japanese 2026 HL, scheme pp16–19: Q4 C20/E20; lower E15 at
// C≤10 OR fewer than150 characters. Q5 uses C30/E30, lower E20 at C≤15
// OR fewer than200 characters. These boundaries are independent of the
// paper's requested minimum200/320 characters.
const writing = (question: 4 | 5): LanguageWritingRubric => {
  const max = question === 4 ? 20 : 30;
  return {
    system: 'language-writing', taskRequirements: [], markingGuideNote: '',
    criteria: [
      { id: 'content', label: 'Content marks', maxMarks: max, permittedMarks: steps(max), guidance: [] },
      { id: 'expression', label: 'Expression marks', maxMarks: max, permittedMarks: steps(max), guidance: [],
        limits: [{ id: 'lower-e', maxMarks: question === 4 ? 15 : 20,
          when: { any: [{ criterionIds: ['content'], atMost: question === 4 ? 10 : 15 }, { length: 'characters', below: question === 4 ? 150 : 200 }] }, guidance: [] }] },
    ],
  };
};

describe('source-defined language writing limits', () => {
  it.each([[4, 10, 150, 15], [5, 15, 200, 20]] as const)('keeps Q%s content and character conditions independent', (q, threshold, length, lower) => {
    const rubric = writing(q);
    const max = q === 4 ? 20 : 30;
    const score = (content: number, characters: number) => ({ 'language:content': content, 'language:expression': max, 'language:length:characters': characters });
    expect(languageWritingMarks(rubric, score(threshold, length))).toBe(threshold + lower);
    expect(languageWritingMarks(rubric, score(threshold + 1, length - 1))).toBe(threshold + 1 + lower);
    expect(languageWritingMarks(rubric, score(threshold + 1, length))).toBe(threshold + 1 + max);
    expect(languageWritingMarks(rubric, score(threshold - 1, length - 1))).toBe(threshold - 1 + lower);
    expect(languageWritingMarks(rubric, { 'language:content': max, 'language:expression': max })).toBe(max + lower);
  });

  it('does not infer partial-credit marks outside printed steps', () => {
    const rubric = writing(4);
    rubric.criteria[0].permittedMarks = [0, 10, 20];
    expect(languageCriterionValue(rubric, 'content', { 'language:content': 11 })).toBe(0);
  });

  it('rejects invalid source tariffs and circular conditions before publishing', () => {
    const rubric = writing(4);
    const card = { kind: 'rubric', rubric, totalMarks: 40 } as SecRubricCard;
    expect(tariffReconciles(card)).toBe(true);
    expect(tariffReconciles({ ...card, totalMarks: 41 })).toBe(false);
    rubric.criteria[0].limits = [{ id: 'circular', maxMarks: 10, when: { any: [{ criterionIds: ['expression'], atMost: 10 }] }, guidance: [] }];
    expect(tariffReconciles(card)).toBe(false);
  });

  it('supports the Russian pre-title-deduction threshold, zero-content rule and explicit content cap', () => {
    const rubric: LanguageWritingRubric = {
      system: 'language-writing', taskRequirements: [], markingGuideNote: '', criteria: [
        { id: 'content', label: 'Content', maxMarks: 10, permittedMarks: steps(10), guidance: [], limits: [{ id: 'one-item', maxMarks: 8, when: { any: [{ flag: 'one-item', prompt: 'Only one item discussed' }] }, guidance: [] }] },
        { id: 'title', label: 'Title deduction', kind: 'deduction', deductFrom: 'content', maxMarks: 1, permittedMarks: [0, 1], guidance: [] },
        { id: 'expression', label: 'Expression', maxMarks: 20, permittedMarks: steps(20), guidance: [], limits: [
          { id: 'lower', maxMarks: 14, when: { any: [{ criterionIds: ['content'], atMost: 5, ignoreDeductions: true }, { length: 'words', below: 25 }] }, guidance: [] },
          { id: 'zero', maxMarks: 0, when: { any: [{ criterionIds: ['content'], atMost: 0 }] }, guidance: [] },
        ] },
        { id: 'soft-sign', label: 'Soft sign deduction', kind: 'deduction', deductFrom: 'expression', maxMarks: 2, permittedMarks: [0, 1, 2], guidance: [] },
      ],
    };
    const scores: LanguageScores = { 'language:content': 6, 'language:title': 1, 'language:expression': 20, 'language:length:words': 25 };
    expect(languageWritingMarks(rubric, scores)).toBe(25); // raw C6 becomes5; E remains20
    expect(languageWritingMarks(rubric, { ...scores, 'language:content': 5 })).toBe(18);
    expect(languageWritingMarks(rubric, { ...scores, 'language:length:words': 24 })).toBe(19);
    expect(languageWritingMarks(rubric, { ...scores, 'language:content': 0 })).toBe(0);
    expect(languageWritingMarks(rubric, { ...scores, 'language:soft-sign': 2 })).toBe(23);
    expect(languageCriterionValue(rubric, 'content', { ...scores, 'language:content': 10, 'language:flag:one-item': 1 })).toBe(7);
  });

  it('places a stale score on the active lower scale without altering other criteria', () => {
    const rubric = writing(4);
    const scores: LanguageScores = { 'language:content': 20, 'language:expression': 20, 'language:length:characters': 149 };
    expect(languageCriterionLimits(rubric, rubric.criteria[1], scores)[0].maxMarks).toBe(15);
    const card = { rubric, totalMarks: 40 } as SecRubricCard & { rubric: LanguageWritingRubric };
    const html = renderToStaticMarkup(React.createElement(LanguageRubricPanel, { card, scores, onScore: () => {} }));
    expect(html).toContain('35 / 40');
    expect(html).toContain('Up to 15 marks');
    expect(html).toContain('Response length (');
  });
});

describe('grouped language answer selection', () => {
  // Japanese 2026 HL Q3B, scheme p14: any FIVE kanji, separately priced
  // correct reading1 + meaning1. Six complete groups are offered once.
  const kanji: LanguagePointsRubric = { system: 'language-points', taskRequirements: [], markingGuideNote: '', count: 5,
    groups: Array.from({ length: 6 }, (_, i) => ({ id: String(i), label: `Item ${i + 1}`, rows: [{ id: 'reading', text: 'Reading', marks: 1 }, { id: 'meaning', text: 'Meaning', marks: 1 }] })) };

  it('awards partial components but never a sixth answer slot', () => {
    const scores: LanguageScores = {};
    for (let i = 0; i < 6; i++) {
      scores[`language:group:${i}`] = 1;
      scores[`language:row:${i}:reading`] = 1;
      scores[`language:row:${i}:meaning`] = i === 2 ? 0 : 1;
    }
    expect(languagePointsMarks(kanji, scores)).toBe(9);
    expect(languagePointsMarks(kanji, { ...scores, 'language:group:0': 0 })).toBe(9);
    expect(languagePointsMarks(kanji, { 'language:row:0:reading': 1 })).toBe(0);
    expect(tariffReconciles({ kind: 'rubric', rubric: kanji, totalMarks: 10 } as SecRubricCard)).toBe(true);
    expect(tariffReconciles({ kind: 'rubric', rubric: kanji, totalMarks: 12 } as SecRubricCard)).toBe(false);
  });

  it('keeps named full and partial listening wordings mutually exclusive', () => {
    const rubric: LanguagePointsRubric = { ...kanji, count: 2, groups: [0, 1, 2].map(i => ({ id: String(i), label: `Answer ${i}`, answerCount: 1, rows: [{ id: 'full', text: 'Full wording', marks: 2 }, { id: 'partial', text: 'Named partial wording', marks: 1 }] })) };
    const scores: LanguageScores = { 'language:group:0': 1, 'language:group:1': 1, 'language:group:2': 1, 'language:row:0:full': 1, 'language:row:0:partial': 1, 'language:row:1:partial': 1, 'language:row:2:full': 1 };
    expect(languagePointsMarks(rubric, scores)).toBe(3);
  });

  it('assesses discretionary marks separately and applies their printed restriction', () => {
    const rubric: LanguagePointsRubric = { ...kanji, count: 4, criteria: [{ id: 'discretionary', label: 'Discretionary marks', maxMarks: 2, permittedMarks: [0, 1, 2], guidance: [], limits: [{ id: 'missing-subsection', maxMarks: 1, when: { any: [{ flag: 'missing-subsection', prompt: 'Not all subsections answered' }] }, guidance: [] }] }] };
    const scores: LanguageScores = { 'language:group:0': 1, 'language:row:0:reading': 1, 'language:row:0:meaning': 1 };
    expect(languagePointsMarks(rubric, scores)).toBe(2);
    expect(languagePointsMarks(rubric, { ...scores, 'language:discretionary': 2 })).toBe(4);
    expect(languagePointsMarks(rubric, { ...scores, 'language:discretionary': 2, 'language:flag:missing-subsection': 1 })).toBe(3);
  });

  it('disables additional groups while keeping each selected component visible', () => {
    const card = { rubric: { ...kanji, count: 1 }, totalMarks: 2 } as SecRubricCard & { rubric: LanguagePointsRubric };
    const html = renderToStaticMarkup(React.createElement(LanguageRubricPanel, { card, scores: { 'language:group:0': 1, 'language:row:0:reading': 1 }, onScore: () => {} }));
    expect(html).toContain('aria-pressed="true"');
    expect(html).toContain('disabled=""');
    expect(html).toContain('1 / 2');
  });
});
