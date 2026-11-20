/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * A card whose paper prices only the SECTION its question sits in, never the
 * question (types/markBank.ts `unpricedSection`, CARD-STANDARD 10i;
 * coordinator ruling, 20 Nov 2026). Portuguese 2015 Higher prints "Parte I
 * (30 pontos)" and no price on any Part I question; 2017 Higher the same on
 * Q2-Q6. Such a card lifts the scheme's answer rows with no marks, has no
 * total of its own, and shows the section's printed total with a fixed line.
 * It is studied as a self-check and never scored, as a no-scheme card is not.
 *
 * The fixture is a SHIPPED Portuguese card (2018 Higher Q2, priced "(5
 * pontos)") turned into the unpriced shape, so every other field is real.
 */
import { describe, expect, it, vi } from 'vitest';
import { readFileSync } from 'node:fs';
import { fireEvent, render, screen, within } from '@testing-library/react';
import { CARDS as PT_HIGHER } from '../components/MarkBank/cards/portuguese/higher';
import SessionScreen, { claimableTotal, marksClaimed } from '../components/MarkBank/SessionScreen';
import { isQuizCard } from '../components/study/quiz/studyQuizPlan';
import { waysInSourceFromMarkBank } from '../components/WaysIn/sources';
import {
  isPointCard, isUnpricedSectionCard, NO_SCHEME_PUBLISHED, tariffReconciles, UNPRICED_SECTION_LINE,
  unpricedSectionChip, unpricedSectionLine, type SecPointCard,
} from '../types/markBank';

vi.mock('../components/PaperTrail/vaultDocs', () => ({ vaultPdf: vi.fn(() => new Promise(() => {})) }));

const shipped = PT_HIGHER.find(card => card.id === 'por-2018-hl-i-2');
if (!shipped || !isPointCard(shipped)) throw new Error('the shipped base card is missing');
const priced: SecPointCard = shipped;
const section = { label: 'Parte I', totalMarks: 30 };
const unpriced: SecPointCard = {
  ...priced,
  tariffModel: { kind: 'questionTotal' },
  totalMarks: 0,
  rows: priced.rows.map(row => ({ ...row, marks: null })),
  unpricedSection: section,
};
const LINE = 'The paper gives 30 marks for Parte I as a whole, not for each question.';

describe('the gate accepts an unpriced card only with the field present', () => {
  it('accepts the unpriced shape, and the priced card it came from is unchanged', () => {
    expect(isUnpricedSectionCard(unpriced)).toBe(true);
    expect(tariffReconciles(unpriced)).toBe(true);
    expect(isUnpricedSectionCard(priced)).toBe(false);
    expect(tariffReconciles(priced)).toBe(true);
  });

  it('refuses a card with no total of its own unless it names the section', () => {
    const { unpricedSection: _field, ...withoutField } = unpriced;
    expect(tariffReconciles(withoutField)).toBe(false);
  });

  it('refuses every other shape carrying the field', () => {
    const bad: SecPointCard[] = [
      { ...unpriced, totalMarks: 30 },
      { ...unpriced, tariffModel: { kind: 'fixed' } },
      { ...unpriced, rows: priced.rows },
      { ...unpriced, rows: [] },
      { ...unpriced, noScheme: true },
      { ...unpriced, unpricedSection: { label: '', totalMarks: 30 } },
      { ...unpriced, unpricedSection: { label: ' Parte I', totalMarks: 30 } },
      { ...unpriced, unpricedSection: { label: 'Parte I', totalMarks: 0 } },
      { ...unpriced, unpricedSection: { label: 'Parte I', totalMarks: 7.5 } },
      { ...unpriced, rows: [{ ...unpriced.rows[0], verbatim: LINE }] },
      { ...unpriced, rows: [{ ...unpriced.rows[0], verbatim: NO_SCHEME_PUBLISHED }] },
      { ...unpriced, rows: [{ ...unpriced.rows[0], kind: 'criterion' }] },
    ];
    for (const card of bad) expect(tariffReconciles(card), JSON.stringify(card.unpricedSection)).toBe(false);
  });

  it('is mirrored word for word in build-deck.mjs', () => {
    const deck = readFileSync('scripts/markbank/build-deck.mjs', 'utf8');
    expect(deck).toContain(`const UNPRICED_SECTION_LINE = '${UNPRICED_SECTION_LINE}';`);
    expect(deck).toContain('function unpricedSectionFault(c)');
  });
});

describe('such a card never yields a numeric score or quiz mark', () => {
  it('is never a quick-quiz question, and claims nothing', () => {
    expect(isQuizCard(priced)).toBe(true);
    expect(isQuizCard(unpriced)).toBe(false);
    expect(claimableTotal(unpriced)).toBe(0);
    expect(marksClaimed(unpriced, { [unpriced.rows[0].id]: 'yes' })).toBe(0);
  });

  it('passes no printed total to Ways In', () => {
    expect(waysInSourceFromMarkBank(priced, 'Portuguese').answerShape).toEqual({ totalMarks: 5 });
    expect(waysInSourceFromMarkBank(unpriced, 'Portuguese').answerShape).toEqual({});
  });

  it('suggests no grade even with its answer ticked, and records no marks either way', () => {
    const onGrade = vi.fn();
    render(<SessionScreen cards={[unpriced]} subjectLabel="Portuguese" onGrade={onGrade} onFinish={vi.fn()} onExit={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    const row = screen.getAllByRole('button', { pressed: false })
      .find(button => button.textContent?.includes(unpriced.rows[0].verbatim.slice(0, 30)));
    expect(row).toBeDefined();
    fireEvent.click(row!);
    expect(row).toHaveAttribute('aria-pressed', 'true');
    expect(screen.getByText(/Nothing on this card can be scored, so there is no suggestion/)).toBeInTheDocument();
    expect(document.querySelector('[data-suggested]')).toBeNull();
    fireEvent.click(screen.getByRole('button', { name: 'Got it' }));
    expect(onGrade).toHaveBeenCalledWith(expect.objectContaining({ cardId: unpriced.id, marksClaimed: 0, marksAvailable: 0 }));
  });
});

describe('the fixed line renders with the lifted label and total', () => {
  it('fills the line and the chip from the card\'s field', () => {
    expect(unpricedSectionLine(section)).toBe(LINE);
    expect(unpricedSectionChip(section)).toBe('Parte I: 30m in all');
    expect(unpricedSectionLine({ label: 'Section A', totalMarks: 40 }))
      .toBe('The paper gives 40 marks for Section A as a whole, not for each question.');
  });

  it('shows the section\'s printed total in place of the card\'s marks, and the line after the reveal', () => {
    render(<SessionScreen cards={[unpriced]} subjectLabel="Portuguese" onGrade={vi.fn()} onFinish={vi.fn()} onExit={vi.fn()} />);
    expect(screen.getByText('Parte I: 30m in all')).toBeInTheDocument();
    expect(screen.queryByText('0m')).not.toBeInTheDocument();
    expect(screen.queryByTestId('mark-bank-unpriced-section')).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    const panel = screen.getByTestId('mark-bank-unpriced-section');
    expect(within(panel).getByText(LINE)).toBeInTheDocument();
    expect(within(panel).getByText(/cannot be scored here/)).toBeInTheDocument();
    expect(screen.queryByText(/Assess your complete answer against the 0-mark total/)).not.toBeInTheDocument();
    // The scheme's own answer is still shown, word for word.
    expect(screen.getByText(unpriced.rows[0].verbatim)).toBeInTheDocument();
  });
});
