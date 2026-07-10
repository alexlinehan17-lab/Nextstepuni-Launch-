/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Render smoke for Definition Drill: the picker lists real subjects; drilling
 * into one shows a prompt with a Reveal button, then the mark-earning wording,
 * the SEC source, and the "I knew it" / "Review again" self-rate buttons.
 */
import { describe, test, expect } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import DefinitionDrill from '@/components/DefinitionDrill/DefinitionDrill';
import { drillSubjects, definitionsForSubject } from '@/data/definitionDrill';

describe('Definition Drill', () => {
  test('every listed subject has at least one definition', () => {
    const subs = drillSubjects();
    expect(subs.length).toBeGreaterThan(0);
    for (const s of subs) expect(definitionsForSubject(s.id).length).toBeGreaterThan(0);
  });

  test('renders the picker, then a subject’s drill with reveal + self-rate', () => {
    render(<DefinitionDrill studentSubjects={['Physics']} />);
    // Level 0 — the tool heading and the picker.
    expect(screen.getByRole('heading', { name: /Definition Drill/i })).toBeInTheDocument();
    // Drill into Physics (a subject we know has definitions).
    fireEvent.click(screen.getByRole('button', { name: /^Physics/ }));
    // Level 1 — a prompt with a Reveal button.
    const reveal = screen.getByRole('button', { name: /Reveal the marking wording/i });
    expect(reveal).toBeInTheDocument();
    fireEvent.click(reveal);
    // The mark-earning wording, its SEC source, and the self-rate buttons appear.
    expect(screen.getAllByText(/State Examinations Commission/i).length).toBeGreaterThan(0);
    expect(screen.getByRole('button', { name: /I knew it/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Review again/i })).toBeInTheDocument();
  });
});
