/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Smoke test for the Paper Trail daily-review session (feature A2): an empty deck
 * shows the invitation, a due card renders its question reference and rating row,
 * and grading it advances the session to the caught-up state. Exercises the real
 * localStorage-backed reviewStore end-to-end (jsdom provides localStorage).
 */
import { describe, test, expect, beforeEach, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import ReviewSession from '@/components/PaperTrail/ReviewSession';
import { addCard } from '@/components/PaperTrail/reviewStore';

const NOW = 1_700_000_000_000;
const noop = vi.fn();
const label = (id: string) => id.toUpperCase();

describe('Paper Trail — daily review session', () => {
  beforeEach(() => localStorage.clear());

  test('empty deck invites the student to build one', () => {
    render(<ReviewSession uid="u1" now={NOW} subjectLabel={label} onOpenQuestion={noop} onBack={noop} />);
    expect(screen.getByText(/Daily review/i)).toBeInTheDocument();
    expect(screen.getByText(/review deck is empty/i)).toBeInTheDocument();
  });

  test('a due card renders and grading it advances to caught-up', () => {
    addCard('u1', { subjectId: 'business', year: 2022, level: 'higher', lang: 'ev', fileid: 'f1', n: '3' }, undefined, NOW);
    render(<ReviewSession uid="u1" now={NOW} subjectLabel={label} onOpenQuestion={noop} onBack={noop} />);
    // Card front shows the real question reference.
    expect(screen.getByText(/Question 3/)).toBeInTheDocument();
    expect(screen.getByText('1 / 1')).toBeInTheDocument();
    // Grade it — the only due card leaves the due set, so we're caught up.
    fireEvent.click(screen.getByRole('button', { name: /^Good/ }));
    expect(screen.getByText(/Reviewed 1 card/i)).toBeInTheDocument();
  });

  test('grading "again" re-queues the card within the session', () => {
    addCard('u1', { subjectId: 'business', year: 2022, level: 'higher', lang: 'ev', fileid: 'f1', n: '5' }, undefined, NOW);
    render(<ReviewSession uid="u1" now={NOW} subjectLabel={label} onOpenQuestion={noop} onBack={noop} />);
    fireEvent.click(screen.getByRole('button', { name: /^Again/ }));
    // Still in-session on the re-queued card (2 of 2), not caught up.
    expect(screen.getByText('2 / 2')).toBeInTheDocument();
    expect(screen.getByText(/Question 5/)).toBeInTheDocument();
  });
});
