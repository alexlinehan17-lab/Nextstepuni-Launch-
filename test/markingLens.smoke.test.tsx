/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Render smoke for the Marking Lens panel inside a VaultQuestionCard. `fetch`
 * is stubbed to reject, so the card degrades to its fallback row — proving the
 * lens's key design property: it teaches even when no crop can render. Uses a
 * REAL golden entry (Business 2024 HL Q4, which carries a pitfall), so the
 * assertions track the shipped content.
 */
import { describe, test, expect, beforeEach, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import VaultQuestionCard from '@/components/PaperTrail/VaultQuestionCard';
import { lensFor } from '@/data/markingLens';

const SIBLING = {
  subjectId: 'business',
  year: 2024,
  level: 'higher' as const,
  lang: 'ev' as const,
  fileid: 'LC033ALP041EV.pdf',
  paperKey: 'p2',
  n: '4',
};

beforeEach(() => {
  vi.stubGlobal('fetch', vi.fn(() => Promise.reject(new Error('no network in jsdom'))));
});

describe('Marking Lens panel', () => {
  test('the golden entry this test renders still exists', () => {
    expect(lensFor(SIBLING)).not.toBeNull();
  });

  test('opens from the card and shows ladder, total, pitfall and cite', async () => {
    render(
      <VaultQuestionCard sibling={SIBLING} saved={false} onToggleReview={vi.fn()} onOpenInPaper={vi.fn()} />,
    );
    const toggle = await screen.findByRole('button', { name: /How the marks are given/i });
    fireEvent.click(toggle);
    expect(toggle).toHaveAttribute('aria-expanded', 'true');
    // Ladder row from the scheme (Q4(C) — Evaluate the CCPC).
    expect(screen.getByText(/Evaluate the role of the CCPC/i)).toBeInTheDocument();
    expect(screen.getByText(/4 @ 4m \(2\+2\) \+ EV 2 \+ EV 2/)).toBeInTheDocument();
    // Total chip.
    expect(screen.getByText(/60 marks/)).toBeInTheDocument();
    // Cited pitfall.
    expect(screen.getByText(/Where marks are lost/i)).toBeInTheDocument();
    expect(screen.getByText(/Chief Examiner's Report 2015 \(Business HL\), p\.17/)).toBeInTheDocument();
    // Scheme cite + SEC attribution.
    expect(screen.getByText(/SEC Marking Scheme 2024, Business Higher Level, Q4/)).toBeInTheDocument();
    // And it closes again.
    fireEvent.click(toggle);
    expect(toggle).toHaveAttribute('aria-expanded', 'false');
    expect(screen.queryByText(/60 marks/)).not.toBeInTheDocument();
  });

  test('a question with no lens shows no lens toggle', () => {
    render(
      <VaultQuestionCard
        sibling={{ ...SIBLING, n: '999' }}
        saved={false}
        onToggleReview={vi.fn()}
        onOpenInPaper={vi.fn()}
      />,
    );
    expect(screen.queryByText(/How the marks are given/i)).not.toBeInTheDocument();
  });
});
