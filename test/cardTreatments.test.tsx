/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The two card treatments prototyped for review pack 1 (PLAN-2026-11-18
 * Phase 2c), tested on the SHIPPED cards, not fixtures:
 *
 *  - a paper the SEC published no marking scheme for (Ancient Greek 2022
 *    Ordinary): the question is shown with its printed marks and the fixed
 *    line, nothing is claimable, no grade is suggested, and the result carries
 *    no marks either way;
 *  - an unseen translation marked unit by unit (Latin 2023 Higher Q2): every
 *    unit is the scheme's own cut of the passage, a unit takes full, partial
 *    (a whole mark below full) or no marks, and no grade is suggested until
 *    every unit is marked.
 */
import { describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen, within } from '@testing-library/react';
import { CARDS as AGREEK_ORDINARY } from '../components/MarkBank/cards/ancient-greek/ordinary';
import { CARDS as LATIN_HIGHER } from '../components/MarkBank/cards/latin/higher';
import SessionScreen, { rubricMarks } from '../components/MarkBank/SessionScreen';
import TranslationPanel from '../components/MarkBank/TranslationPanel';
import {
  partialSteps, translationMarks, translationPlacementComplete, translationUnitId, translationUnitMark,
} from '../components/MarkBank/translationScoring';
import {
  isNoSchemeCard, isPointCard, isRubricCard, NO_SCHEME_PUBLISHED, tariffReconciles, TRANSLATION_NO_MODEL,
  type SecRubricCard, type TranslationRubric,
} from '../types/markBank';
import { isQuizCard } from '../components/study/quiz/studyQuizPlan';

vi.mock('../components/PaperTrail/vaultDocs', () => ({ vaultPdf: vi.fn(() => new Promise(() => {})) }));

const noScheme = AGREEK_ORDINARY.filter(isNoSchemeCard);
type TranslationCard = SecRubricCard & { rubric: TranslationRubric };
const translations = LATIN_HIGHER
  .filter((card): card is TranslationCard => isRubricCard(card) && card.rubric.system === 'translation');
const virgil = translations.find(card => card.id === 'lat-2023-hl-a-q2-i')!;

describe('Ancient Greek 2022 Ordinary: no marking scheme was published', () => {
  it('cards every one of the paper\'s 21 asks, and only that sitting', () => {
    expect(noScheme).toHaveLength(21);
    expect(new Set(noScheme.map(card => `${card.year} ${card.level}`))).toEqual(new Set(['2022 ordinary']));
    expect(noScheme.every(tariffReconciles)).toBe(true);
    expect(noScheme.map(card => card.totalMarks).reduce((a, b) => a + b, 0)).toBe(4 * 105 + 60 + 8 * 10 + 8 * 30);
  });

  it('is never offered as a quick quiz question', () => {
    expect(noScheme.filter(isQuizCard)).toEqual([]);
  });

  it('reveals the fixed line and the paper\'s marks, with nothing to claim and no suggestion', () => {
    const card = noScheme.find(c => c.id === 'agr-2022-ol-q3-vii')!;
    const onGrade = vi.fn();
    render(<SessionScreen cards={[card]} subjectLabel="Ancient Greek" onGrade={onGrade} onFinish={vi.fn()} onExit={vi.fn()} />);
    expect(screen.queryByText(NO_SCHEME_PUBLISHED)).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    const panel = screen.getByTestId('mark-bank-no-scheme');
    expect(within(panel).getByText(NO_SCHEME_PUBLISHED)).toBeInTheDocument();
    expect(within(panel).getByText(/cannot be scored here/)).toBeInTheDocument();
    expect(within(panel).getByText(/worth 30 marks/)).toBeInTheDocument();
    expect(screen.queryByText('Select the points you actually got.')).not.toBeInTheDocument();
    expect(screen.queryByText('Check your complete response.')).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /Select all/ })).not.toBeInTheDocument();
    expect(screen.getByText(/Nothing on this card can be scored, so there is no suggestion/)).toBeInTheDocument();
    expect(document.querySelector('[data-suggested]')).toBeNull();
    fireEvent.click(screen.getByRole('button', { name: 'Got it' }));
    expect(onGrade).toHaveBeenCalledWith(expect.objectContaining({ cardId: card.id, marksClaimed: 0, marksAvailable: 0 }));
  });
});

describe('Latin 2023 Higher Q2: an unseen translation marked unit by unit', () => {
  it('cards the four passages of the sitting, each the scheme\'s own units making 65', () => {
    expect(translations.map(card => card.questionRef).sort()).toEqual([
      '2023 HL Section A Q2(i)', '2023 HL Section A Q2(ii)', '2023 HL Section B Q2(i)', '2023 HL Section B Q2(ii)',
    ]);
    for (const card of translations) {
      expect(card.totalMarks).toBe(65);
      expect(card.rubric.units.reduce((n, u) => n + u.marks, 0)).toBe(65);
      expect(tariffReconciles(card)).toBe(true);
    }
    expect(virgil.rubric.units.map(u => u.marks)).toEqual([4, 4, 6, 6, 7, 6, 9, 7, 6, 4, 6]);
    expect(virgil.rubric.units[0].text).toBe('hastam alii galeamque ferunt;');
  });

  it('scores full, partial and none, and rejects a value a unit cannot take', () => {
    const [u1, u2, u3] = virgil.rubric.units;
    expect(partialSteps(u3)).toEqual([1, 2, 3, 4, 5]);
    const scores = { [translationUnitId(u1)]: 4, [translationUnitId(u2)]: 2, [translationUnitId(u3)]: 0 };
    expect(translationMarks(virgil, scores)).toBe(6);
    expect(rubricMarks(virgil, scores)).toBe(6);
    expect(translationUnitMark(u1, { [translationUnitId(u1)]: 5 })).toBeNull();
    expect(translationUnitMark(u1, { [translationUnitId(u1)]: 1.5 })).toBeNull();
    expect(translationUnitMark(u1, { [translationUnitId(u1)]: -1 })).toBeNull();
    expect(translationPlacementComplete(virgil.rubric, scores)).toBe(false);
    const all = Object.fromEntries(virgil.rubric.units.map(u => [translationUnitId(u), u.marks]));
    expect(translationPlacementComplete(virgil.rubric, all)).toBe(true);
    expect(translationMarks(virgil, all)).toBe(65);
  });

  it('shows the scheme\'s rule and every unit, and Partial opens the whole marks below full', () => {
    const onScore = vi.fn();
    render(<TranslationPanel card={virgil} scores={{}} onScore={onScore} />);
    expect(screen.getByText(TRANSLATION_NO_MODEL)).toBeInTheDocument();
    expect(screen.getByText(/^Partial marks are awarded based on demonstrating sufficient understanding/)).toBeInTheDocument();
    expect(screen.getByText('hastam alii galeamque ferunt;')).toBeInTheDocument();
    expect(screen.getByText('0 of 11 units marked')).toBeInTheDocument();
    const unit3 = screen.getByRole('group', { name: 'Marks for unit 3' });
    fireEvent.click(within(unit3).getByRole('button', { name: 'Partial marks for unit 3' }));
    const steps = screen.getByRole('group', { name: 'Partial marks for unit 3' });
    expect(within(steps).getAllByRole('button').map(b => b.textContent)).toEqual(['1m', '2m', '3m', '4m', '5m']);
    fireEvent.click(within(steps).getByRole('button', { name: 'Claim 3 marks for unit 3' }));
    expect(onScore).toHaveBeenLastCalledWith('translation:u3', 3);
    fireEvent.click(within(screen.getByRole('group', { name: 'Marks for unit 1' })).getByRole('button', { name: /Claim full marks, 4, for unit 1/ }));
    expect(onScore).toHaveBeenLastCalledWith('translation:u1', 4);
  });

  it('suggests no grade in a session until every unit is marked', () => {
    render(<SessionScreen cards={[virgil]} subjectLabel="Latin" onGrade={vi.fn()} onFinish={vi.fn()} onExit={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    expect(screen.getByText(/No unit-by-unit placement selected yet/)).toBeInTheDocument();
    fireEvent.click(within(screen.getByRole('group', { name: 'Marks for unit 1' })).getByRole('button', { name: /full marks/ }));
    expect(screen.getByText(/Your unit-by-unit marking is not finished/)).toBeInTheDocument();
    expect(document.querySelector('[data-suggested]')).toBeNull();
    for (let i = 2; i <= virgil.rubric.units.length; i++) {
      fireEvent.click(within(screen.getByRole('group', { name: `Marks for unit ${i}` })).getByRole('button', { name: /full marks/ }));
    }
    expect(screen.getByText(/Your unit-by-unit placement is 65 of 65 marks/)).toBeInTheDocument();
    expect(document.querySelector('[data-suggested]')).not.toBeNull();
  });

  it('leaves every other card in both decks a card of the kind it was', () => {
    expect(AGREEK_ORDINARY.filter(c => isPointCard(c) && !c.noScheme).every(c => !isNoSchemeCard(c))).toBe(true);
    expect(LATIN_HIGHER.filter(c => isRubricCard(c)).every(c => c.year === 2023 && c.questionRef.includes('Q2('))).toBe(true);
  });
});
