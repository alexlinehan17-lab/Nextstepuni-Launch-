/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guards the guardian weekly email builder (feature E10): it reports effort, is
 * personalised, and crucially carries NO grade/mark/percentage language.
 */
import { describe, it, expect } from 'vitest';
import { buildGuardianEmail } from '../data/guardianSummary';

describe('Guardian weekly email', () => {
  it('personalises and reports effort', () => {
    const { subject, text } = buildGuardianEmail({ studentName: 'Aoife', weekMinutes: 120, cardsReviewed: 34, currentStreak: 5, focusTopic: 'Calculus' });
    expect(subject).toContain('Aoife');
    expect(text).toContain('120 focused minutes');
    expect(text).toContain('34 practice questions');
    expect(text).toContain('5-day practice streak');
    expect(text).toContain('Calculus');
  });

  it('never mentions grades, marks or percentages', () => {
    const { subject, text } = buildGuardianEmail({ studentName: 'Aoife', weekMinutes: 120, cardsReviewed: 34, currentStreak: 5, focusTopic: 'Calculus' });
    const blob = `${subject} ${text}`.toLowerCase();
    for (const banned of ['grade', 'mark', '%', 'percent', 'h1', 'a1', 'points', 'score']) {
      expect(blob).not.toContain(banned);
    }
  });

  it('degrades gracefully with no name and a quiet week', () => {
    const { subject, text } = buildGuardianEmail({ weekMinutes: 0, cardsReviewed: 0, currentStreak: 0 });
    expect(subject).toContain('your student');
    expect(text).toContain('logged some revision');
    expect(text).not.toContain('undefined');
  });
});
