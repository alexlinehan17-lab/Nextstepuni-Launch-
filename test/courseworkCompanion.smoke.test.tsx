/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Render smoke for Coursework Companion: the picker lists real subjects;
 * drilling into one shows component cards with the SEC source and the printed
 * marking criteria behind a toggle.
 */
import { describe, test, expect } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import CourseworkCompanion from '@/components/CourseworkCompanion/CourseworkCompanion';
import { courseworkSubjects, componentsForSubject } from '@/data/courseworkCompanion';

describe('Coursework Companion', () => {
  test('every listed subject has at least one component', () => {
    const subs = courseworkSubjects();
    expect(subs.length).toBeGreaterThan(0);
    for (const s of subs) expect(componentsForSubject(s.id).length).toBeGreaterThan(0);
  });

  test('renders the picker, then a subject’s components with source + criteria toggle', () => {
    render(<CourseworkCompanion studentSubjects={['Geography']} />);
    // Level 0 — the tool heading and the picker.
    expect(screen.getByRole('heading', { name: /Coursework Companion/i })).toBeInTheDocument();
    // Drill into Geography (a subject we know has a component).
    fireEvent.click(screen.getByRole('button', { name: /^Geography/ }));
    // Level 1 — a component card with SEC attribution.
    expect(screen.getAllByText(/State Examinations Commission/i).length).toBeGreaterThan(0);
    // The criteria are behind a toggle.
    const toggle = screen.getAllByRole('button', { name: /How it’s marked/i })[0];
    expect(toggle).toHaveAttribute('aria-expanded', 'false');
    fireEvent.click(toggle);
    expect(screen.getByText(/Gathering of Data/i)).toBeInTheDocument();
    expect(screen.getAllByRole('button', { name: /Hide the marking criteria/i }).length).toBeGreaterThan(0);
  });
});
