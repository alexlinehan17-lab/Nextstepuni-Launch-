import React from 'react';
import { cleanup, render, screen, fireEvent } from '@testing-library/react';
import { afterEach, expect, test } from 'vitest';
import ConfidenceRecord from '../components/dashboard/ConfidenceRecord';
import type { ConfidenceObservation } from '../components/dashboard/dashboardAnalytics';
afterEach(cleanup);
test('keeps every subject, including no-data subjects, and opens underlying reflections', () => {
  const subjects = ['Accounting', 'Applied Maths', 'English', 'Geography', 'Irish', 'Mathematics', 'Politics & Society'];
  const observations: ConfidenceObservation[] = subjects.slice(0, 6).map((subject, i) => ({ id: String(i), subject, score: 4, label: 'good', timestamp: new Date('2026-09-20T12:00:00').getTime(), dateKey: '2026-09-20' }));
  const { container } = render(<ConfidenceRecord subjects={subjects} observations={observations} />);
  expect(container.querySelectorAll('details')).toHaveLength(7);
  expect(screen.getByText('No reflections in this period')).toBeInTheDocument();
  fireEvent.click(screen.getByText('Irish'));
  const irish = screen.getByText('Irish').closest('details');
  expect(irish?.textContent).toContain('Good · 4/5');
  expect(irish?.textContent).toContain('20 Sept');
});
test('one reflection is not presented as a trend', () => {
  render(<ConfidenceRecord subjects={['Irish']} observations={[{ id: 'one', subject: 'Irish', score: 3, label: 'okay', timestamp: Date.now(), dateKey: '2026-09-20' }]} />);
  expect(screen.getByText(/one observation, not a trend/)).toBeInTheDocument();
});
