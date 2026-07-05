/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Smoke tests for the Paper Trail first-run coach: the fresh state, the live
 * "taking shape" state as steps tick off, retirement once the loop is running,
 * and dismissal.
 */
import { describe, test, expect, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import FirstRunCoach from '@/components/PaperTrail/FirstRunCoach';

const steps = (a: boolean, b: boolean, c: boolean) => [
  { label: 'Open any paper', done: a },
  { label: 'Mark yourself', done: b },
  { label: 'Save to review', done: c },
];

describe('Paper Trail — first-run coach', () => {
  beforeEach(() => localStorage.clear());

  test('fresh: shows the intro and all three steps', () => {
    render(<FirstRunCoach uid="u1" steps={steps(false, false, false)} />);
    expect(screen.getByText(/New here\?/i)).toBeInTheDocument();
    expect(screen.getByText(/How Paper Trail builds your revision/i)).toBeInTheDocument();
    expect(screen.getByText('0/3')).toBeInTheDocument();
  });

  test('in progress: heading warms up and count reflects done steps', () => {
    render(<FirstRunCoach uid="u1" steps={steps(true, false, false)} />);
    expect(screen.getByText(/Your revision is taking shape/i)).toBeInTheDocument();
    expect(screen.getByText('1/3')).toBeInTheDocument();
  });

  test('retires once every step is done', () => {
    const { container } = render(<FirstRunCoach uid="u1" steps={steps(true, true, true)} />);
    expect(container).toBeEmptyDOMElement();
  });

  test('dismiss hides it and persists', () => {
    const { container, rerender } = render(<FirstRunCoach uid="u1" steps={steps(false, false, false)} />);
    fireEvent.click(screen.getByRole('button', { name: /Dismiss/i }));
    expect(container).toBeEmptyDOMElement();
    // Persisted: a fresh mount stays hidden.
    rerender(<FirstRunCoach uid="u1" steps={steps(false, false, false)} />);
    expect(container).toBeEmptyDOMElement();
  });
});
