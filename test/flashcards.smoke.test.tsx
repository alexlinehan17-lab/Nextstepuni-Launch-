/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Smoke test for student flashcards (feature E6): author a card, see it listed,
 * review it (flip → rate), and reach the done state. Exercises the real
 * localStorage + FSRS store end-to-end (jsdom).
 */
import { describe, test, expect, beforeEach, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import Flashcards from '@/components/PaperTrail/Flashcards';
import { createCard, dueCards, gradeCard, loadCards } from '@/components/PaperTrail/flashcardStore';

const NOW = 1_700_000_000_000;
const noop = vi.fn();

describe('Paper Trail — flashcard store', () => {
  beforeEach(() => localStorage.clear());

  test('create → due now; grade reschedules out of due', () => {
    createCard('u1', 'Q?', 'A', undefined, NOW);
    expect(loadCards('u1')).toHaveLength(1);
    expect(dueCards('u1', NOW)).toHaveLength(1);
    const id = loadCards('u1')[0].id;
    gradeCard('u1', id, 'good', NOW);
    expect(dueCards('u1', NOW)).toHaveLength(0); // scheduled into the future
  });

  test('ignores blank front/back', () => {
    createCard('u1', '  ', 'A', undefined, NOW);
    expect(loadCards('u1')).toHaveLength(0);
  });
});

describe('Paper Trail — flashcards UI', () => {
  beforeEach(() => localStorage.clear());

  test('author a card, then review it front → answer → rate', () => {
    render(<Flashcards uid="u1" now={NOW} onBack={noop} />);
    fireEvent.click(screen.getByRole('button', { name: /New card/i }));
    fireEvent.change(screen.getByPlaceholderText(/Le Chatelier/i), { target: { value: 'What is Ohm’s law?' } });
    fireEvent.change(screen.getByPlaceholderText(/your own words/i), { target: { value: 'V = IR' } });
    fireEvent.click(screen.getByRole('button', { name: /Save card/i }));

    // Back on the list, the card is shown.
    expect(screen.getByText(/What is Ohm’s law\?/)).toBeInTheDocument();

    // Review the one due card.
    fireEvent.click(screen.getByRole('button', { name: /Review 1 due/i }));
    fireEvent.click(screen.getByRole('button', { name: /Show answer/i }));
    expect(screen.getByText('V = IR')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /^Good/ }));
    expect(screen.getByText(/All done/i)).toBeInTheDocument();
  });
});
