/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Render smoke for Answer Architect: the subject picker lists real subjects, and
 * drilling into one shows answer-skeleton cards with the structure line, the SEC
 * source, and the ordered beats behind a toggle. Guards the projection UI against
 * render regressions.
 */
import { describe, test, expect } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import AnswerArchitect from '@/components/AnswerArchitect/AnswerArchitect';
import { architectSubjects, skeletonsForSubject } from '@/data/answerArchitect';

describe('Answer Architect', () => {
  test('every listed subject has at least one skeleton', () => {
    const subs = architectSubjects();
    expect(subs.length).toBeGreaterThan(0);
    for (const s of subs) expect(skeletonsForSubject(s.id).length).toBeGreaterThan(0);
  });

  test('renders the picker, then a subject’s skeletons with source + beats toggle', () => {
    render(<AnswerArchitect studentSubjects={['Business']} />);
    // Level 0 — the tool heading and the picker.
    expect(screen.getByRole('heading', { name: /Answer Architect/i })).toBeInTheDocument();
    // Drill into Business (a subject we know has skeletons).
    fireEvent.click(screen.getByRole('button', { name: /^Business/ }));
    // Level 1 — skeleton cards with SEC attribution and a "Build the answer" toggle.
    expect(screen.getAllByText(/State Examinations Commission/i).length).toBeGreaterThan(0);
    const toggle = screen.getAllByRole('button', { name: /Build the answer/i })[0];
    expect(toggle).toHaveAttribute('aria-expanded', 'false');
    fireEvent.click(toggle);
    // The beats are revealed — the toggle flips to "Hide the skeleton".
    expect(screen.getAllByRole('button', { name: /Hide the skeleton/i }).length).toBeGreaterThan(0);
  });
});
