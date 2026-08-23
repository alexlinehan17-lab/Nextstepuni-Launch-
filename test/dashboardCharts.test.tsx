/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { render, screen, within } from '@testing-library/react';
import { afterEach, describe, expect, test, vi } from 'vitest';
import { ActivityChart, MockTrajectoryChart, RankedBarChart, SessionMixChart } from '@/components/dashboard/DashboardCharts';
import type { UnifiedMockResult } from '@/types';

function mock(id: string, date: string, totalPoints: number): UnifiedMockResult {
  return {
    id,
    label: `Mock ${id}`,
    date,
    entries: [],
    totalPoints,
    timestamp: new Date(`${date}T12:00:00`).getTime(),
  };
}

describe('dashboard charts', () => {
  afterEach(() => vi.restoreAllMocks());

  test('renders one month label for multiple mock results in the same month', () => {
    render(
      <MockTrajectoryChart
        mocks={[
          mock('july', '2026-07-12', 410),
          mock('august-1', '2026-08-03', 430),
          mock('august-2', '2026-08-14', 455),
          mock('august-3', '2026-08-21', 480),
        ]}
      />,
    );

    const chart = screen.getByRole('img', { name: 'Mock exam total points trajectory' });
    expect(within(chart).getAllByText('Aug 26')).toHaveLength(1);
    expect(within(chart).getByText('Jul 26')).toBeInTheDocument();
    expect(within(chart).getAllByRole('button')).toHaveLength(4);
  });

  test('keeps only the first and last unique month labels on narrow charts', () => {
    vi.spyOn(HTMLElement.prototype, 'getBoundingClientRect').mockReturnValue({
      x: 0,
      y: 0,
      width: 360,
      height: 238,
      top: 0,
      right: 360,
      bottom: 238,
      left: 0,
      toJSON: () => ({}),
    });

    render(
      <MockTrajectoryChart
        mocks={[
          mock('may', '2026-05-12', 380),
          mock('june', '2026-06-12', 410),
          mock('july', '2026-07-12', 440),
          mock('august-1', '2026-08-03', 460),
          mock('august-2', '2026-08-21', 480),
        ]}
      />,
    );

    const chart = screen.getByRole('img', { name: 'Mock exam total points trajectory' });
    expect(within(chart).getByText('May 26')).toBeInTheDocument();
    expect(within(chart).getByText('Aug 26')).toBeInTheDocument();
    expect(within(chart).queryByText('Jun 26')).not.toBeInTheDocument();
    expect(within(chart).queryByText('Jul 26')).not.toBeInTheDocument();
    expect(within(chart).getAllByRole('button')).toHaveLength(5);
  });

  test('uses singular activity units when the value is one', () => {
    render(
      <ActivityChart
        metric="sessions"
        buckets={[{
          key: '2026-08-23',
          label: '23 Aug',
          accessibleLabel: '23 August 2026',
          start: new Date('2026-08-23T00:00:00').getTime(),
          end: new Date('2026-08-24T00:00:00').getTime(),
          sessions: 1,
          minutes: 1,
        }]}
      />,
    );

    expect(screen.getByRole('button', { name: '23 August 2026: 1 session' })).toBeInTheDocument();
    expect(screen.getByText('1 session in this period.')).toBeInTheDocument();
  });

  test('uses singular units in ranked and session-mix charts', () => {
    const { rerender } = render(
      <RankedBarChart
        values={[{ id: 'retrieval', label: 'Retrieval practice', value: 1 }]}
        unit="uses"
        emptyTitle="Empty"
        emptyDetail="Nothing yet"
      />,
    );
    expect(screen.getByText('1 use')).toBeInTheDocument();

    rerender(<SessionMixChart values={[{ id: 'practice', label: 'Practice', value: 1 }]} />);
    expect(screen.getByText('1 session')).toBeInTheDocument();
    expect(screen.getByLabelText('Practice: 1 session')).toBeInTheDocument();
  });
});
