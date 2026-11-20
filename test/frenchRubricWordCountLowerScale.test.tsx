/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * A lower scale switched on by the word count alone (FrenchLowerScale with
 * contentCriteria [] and no contentAtMost): the Portuguese 2025-2026 schemes
 * print "If the answer is too short (less than 140 words), mark questions 3
 * and 4 out of 20 marks (lower scale)", one statement that lowers Content
 * and Communication and Language together. One switch per card
 * (frenchShortSwitchId); German and Italian score as before, through the
 * app's own scoring code.
 */

import { describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';
import FrenchRubricPanel from '../components/MarkBank/FrenchRubricPanel';
import {
  frenchCriterionMark,
  frenchMarks,
  frenchScoreId,
  frenchShortId,
  frenchShortSwitchId,
  lowerScaleActive,
  type FrenchScores,
} from '../components/MarkBank/frenchRubric';
import { CARDS as GERMAN_HIGHER } from '../components/MarkBank/cards/german/higher';
import { CARDS as GERMAN_ORDINARY } from '../components/MarkBank/cards/german/ordinary';
import { CARDS as ITALIAN_HIGHER } from '../components/MarkBank/cards/italian/higher';
import { CARDS as ITALIAN_ORDINARY } from '../components/MarkBank/cards/italian/ordinary';
import type { FrenchCriterion, FrenchLowerScale, SecCard, SecRubricCard } from '../types/markBank';

const gridCards = (cards: SecCard[]) => cards.filter((card): card is SecRubricCard =>
  card.kind === 'rubric' && (card as SecRubricCard).rubric.system === 'french');
const criteriaOf = (card: SecRubricCard): FrenchCriterion[] =>
  (card.rubric.system === 'french' ? card.rubric.criteria : []);

/** Every lowered criterion of a deck, with its card. */
const lowered = (cards: SecCard[]) => gridCards(cards).flatMap(card =>
  criteriaOf(card).filter(k => k.lowerScale).map(criterion => ({ card, criterion })));

/** Scores placing each content criterion the scale counts at the given marks. */
function placeContent(criteria: FrenchCriterion[], lower: FrenchLowerScale, at: 'zero' | 'max'): FrenchScores {
  const scores: FrenchScores = {};
  for (const id of lower.contentCriteria) {
    const named = criteria.find(k => k.id === id)!;
    scores[frenchScoreId(id)] = at === 'zero' ? 0 : named.maxMarks;
  }
  return scores;
}

describe('German, as before', () => {
  const german = lowered([...GERMAN_HIGHER, ...GERMAN_ORDINARY]);
  const both = german.filter(({ criterion }) => criterion.lowerScale!.wordsUnder !== undefined);
  const contentOnly = german.filter(({ criterion }) => criterion.lowerScale!.wordsUnder === undefined);

  it('has its 68 both-trigger and 34 content-only lower scales, at most one word count per card', () => {
    expect(both).toHaveLength(68);
    expect(contentOnly).toHaveLength(34);
    for (const card of gridCards([...GERMAN_HIGHER, ...GERMAN_ORDINARY])) {
      expect(criteriaOf(card).filter(k => k.lowerScale?.wordsUnder !== undefined).length).toBeLessThanOrEqual(1);
    }
  });

  it('keeps every German and Italian lowered criterion its own switch', () => {
    const all = [...german, ...lowered([...ITALIAN_HIGHER, ...ITALIAN_ORDINARY])];
    expect(all.length).toBeGreaterThan(102);
    for (const { card, criterion } of all) {
      expect(frenchShortSwitchId(criteriaOf(card), criterion)).toBe(frenchShortId(criterion.id));
    }
  });

  it('content-only: lowered by its content, never by a short flag', () => {
    const { card, criterion } = contentOnly[0];
    const criteria = criteriaOf(card);
    const lower = criterion.lowerScale!;
    expect(lowerScaleActive(criteria, criterion, placeContent(criteria, lower, 'zero'))).toBe(true);
    const high = placeContent(criteria, lower, 'max');
    expect(lowerScaleActive(criteria, criterion, high)).toBe(false);
    expect(lowerScaleActive(criteria, criterion, { ...high, [frenchShortId(criterion.id)]: 1 })).toBe(false);
  });

  it('both-trigger: lowered by its content, and separately by the short flag', () => {
    const { card, criterion } = both[0];
    const criteria = criteriaOf(card);
    const lower = criterion.lowerScale!;
    const high = placeContent(criteria, lower, 'max');
    expect(lowerScaleActive(criteria, criterion, placeContent(criteria, lower, 'zero'))).toBe(true);
    expect(lowerScaleActive(criteria, criterion, high)).toBe(false);
    expect(lowerScaleActive(criteria, criterion, { ...high, [frenchShortId(criterion.id)]: 1 })).toBe(true);
    // Lowered, a placement above the lower maximum earns nothing; within it, itself.
    const short = { ...high, [frenchShortId(criterion.id)]: 1 };
    expect(frenchCriterionMark(criteria, criterion, { ...short, [frenchScoreId(criterion.id)]: criterion.maxMarks })).toBe(0);
    expect(frenchCriterionMark(criteria, criterion, { ...short, [frenchScoreId(criterion.id)]: lower.maxMarks })).toBe(lower.maxMarks);
  });
});

describe('Italian (#382), as before', () => {
  it('caps language when the content it names is at its threshold or less', () => {
    const [{ card, criterion }] = lowered([...ITALIAN_HIGHER, ...ITALIAN_ORDINARY])
      .filter(({ criterion: k }) => k.lowerScale!.contentCriteria.length === 1 && k.lowerScale!.maxMarks > 0);
    const criteria = criteriaOf(card);
    const lower = criterion.lowerScale!;
    const [contentId] = lower.contentCriteria;
    const at = (content: number): FrenchScores => ({ [frenchScoreId(contentId)]: content });
    expect(lowerScaleActive(criteria, criterion, at(lower.contentAtMost!))).toBe(true);
    expect(lowerScaleActive(criteria, criterion, at(lower.contentAtMost! + 1))).toBe(false);
    expect(frenchCriterionMark(criteria, criterion, { ...at(lower.contentAtMost!), [frenchScoreId(criterion.id)]: lower.maxMarks + 1 })).toBe(0);
  });
});

describe('a lower scale switched on by the word count alone (Portuguese 2025-2026)', () => {
  const rule = 'If the answer is too short (less than 140 words), mark questions 3 and 4 out of 20 marks (lower scale).';
  const range = (lo: number, hi: number) => Array.from({ length: hi - lo + 1 }, (_v, i) => lo + i);
  const lower = (): FrenchLowerScale => ({
    label: 'Lower', maxMarks: 10, permittedMarks: range(0, 10),
    bands: [{ label: 'TOP', marks: range(8, 10), guidance: [] }, { label: 'MIDDLE', marks: range(4, 7), guidance: [] },
      { label: 'BOTTOM', marks: range(0, 3), guidance: [] }],
    contentCriteria: [], wordsUnder: 140, rule,
  });
  const criterion = (id: string, label: string): FrenchCriterion => ({
    id, label, maxMarks: 15, permittedMarks: range(0, 15), guidance: [],
    bands: [{ label: 'TOP', marks: range(11, 15), guidance: [] }, { label: 'MIDDLE', marks: range(6, 10), guidance: [] },
      { label: 'BOTTOM', marks: range(0, 5), guidance: [] }],
    lowerScale: lower(),
  });
  const criteria = [criterion('content-communication', 'Content and Communication'), criterion('language', 'Language')];
  const card = {
    id: 'por-test-hl-b-3-a', kind: 'rubric', subjectId: 'portuguese', level: 'higher', year: 2025, section: 'B',
    topicId: 'portuguese-2-4', conceptId: 'test', questionRef: '2025 HL Section B Q3(a)', questionText: 'Test task',
    totalMarks: 30, schemePages: [9],
    rubric: { system: 'french', taskRequirements: [], criteria, markingGuideNote: '', practiceNotes: [] },
  } as unknown as SecRubricCard;
  const placed = (a: number, b: number, extra: FrenchScores = {}): FrenchScores => ({
    [frenchScoreId('content-communication')]: a, [frenchScoreId('language')]: b, ...extra,
  });
  const SWITCH = frenchShortId('content-communication');

  it('is off by default, even with every mark at 0', () => {
    for (const k of criteria) {
      expect(lowerScaleActive(criteria, k, {})).toBe(false);
      expect(lowerScaleActive(criteria, k, placed(0, 0))).toBe(false);
    }
    expect(frenchMarks(card, placed(12, 13))).toBe(25);
  });

  it('is switched on only by the one switch, and lowers both criteria together', () => {
    for (const k of criteria) expect(frenchShortSwitchId(criteria, k)).toBe(SWITCH);
    for (const k of criteria) expect(lowerScaleActive(criteria, k, { [SWITCH]: 1 })).toBe(true);
    expect(frenchMarks(card, placed(12, 13, { [SWITCH]: 1 }))).toBe(0);
    expect(frenchMarks(card, placed(9, 10, { [SWITCH]: 1 }))).toBe(19);
    // The second criterion's own short id is not a switch.
    for (const k of criteria) expect(lowerScaleActive(criteria, k, { [frenchShortId('language')]: 1 })).toBe(false);
  });

  it('shows one switch, under the first criterion, and both criteria read it', () => {
    const onScore = vi.fn();
    const { rerender } = render(<FrenchRubricPanel card={card} scores={{}} onScore={onScore} />);
    const buttons = screen.getAllByRole('button', { name: /my answer is under 140 words/i });
    expect(buttons).toHaveLength(1);
    fireEvent.click(buttons[0]);
    expect(onScore).toHaveBeenCalledWith(SWITCH, 1);
    expect(screen.getAllByText('Full scale applies')).toHaveLength(2);
    // The printed rule shows once per card, under the switch.
    expect(screen.getAllByText(rule)).toHaveLength(1);
    expect(screen.getAllByText(/you have not said your answer is under 140 words/)).toHaveLength(2);
    rerender(<FrenchRubricPanel card={card} scores={{ [SWITCH]: 1 }} onScore={onScore} />);
    expect(screen.getAllByText('Lower scale applies')).toHaveLength(2);
    expect(screen.getByText(/your answer is under 140 words \(set under Content and Communication\)/)).toBeInTheDocument();
  });
});
