/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { describe, expect, test } from 'vitest';
import type { UnifiedMockResult } from '@/types';
import type { ActivityBucket, ConfidenceObservation } from '@/components/dashboard/dashboardAnalytics';
import {
  buildActivityInsights,
  buildConfidenceInsights,
  buildMockInsights,
} from '@/components/dashboard/dashboardInsightAnalytics';

function confidenceSeries(subject: string, scores: number[]): ConfidenceObservation[] {
  return scores.map((score, index) => ({
    id: `${subject}-${index}`,
    subject,
    timestamp: new Date(2026, 7, 1 + index, 12).getTime(),
    dateKey: `2026-08-${String(1 + index).padStart(2, '0')}`,
    score,
    label: ['lost', 'shaky', 'okay', 'good', 'confident'][score - 1] as ConfidenceObservation['label'],
  }));
}

function activityBucket(day: number, sessions: number, minutes = sessions * 25): ActivityBucket {
  const start = new Date(2026, 7, day);
  const end = new Date(2026, 7, day + 1);
  return {
    key: `2026-08-${String(day).padStart(2, '0')}`,
    label: String(day),
    accessibleLabel: `${day} August 2026`,
    start: start.getTime(),
    end: end.getTime(),
    sessions,
    minutes,
  };
}

function mock(
  id: string,
  date: string,
  totalPoints: number,
  biology: string,
  irish: string,
): UnifiedMockResult {
  return {
    id,
    label: `Mock ${id}`,
    date,
    totalPoints,
    timestamp: new Date(`${date}T12:00:00`).getTime(),
    entries: [
      { subjectName: 'Biology', grade: biology, level: biology.startsWith('O') ? 'ordinary' : 'higher' },
      { subjectName: 'Irish', grade: irish, level: irish.startsWith('O') ? 'ordinary' : 'higher' },
    ],
    resultKind: 'full',
  };
}

describe('dashboard insight analytics', () => {
  test('classifies each confidence subject without turning one debrief into a trend', () => {
    const insights = buildConfidenceInsights([
      ...confidenceSeries('Mathematics', [2, 3, 4, 5]),
      ...confidenceSeries('English', [5, 4, 3]),
      ...confidenceSeries('Irish', [3, 3, 3]),
      ...confidenceSeries('Geography', [2, 4, 2, 4]),
      ...confidenceSeries('Accounting', [4]),
    ], ['Mathematics', 'English', 'Irish', 'Geography', 'Accounting', 'Biology']);
    const trends = Object.fromEntries(insights.map(insight => [insight.title, insight.trend]));

    expect(trends).toEqual({
      Mathematics: 'upward',
      Geography: 'varied',
      English: 'downward',
      Irish: 'steady',
      Accounting: 'building',
      Biology: 'building',
    });
    expect(insights.find(insight => insight.title === 'Accounting')?.evidence).toContain('1 debrief');
    expect(insights.find(insight => insight.title === 'Biology')?.evidence).toContain('No confidence debriefs');
  });

  test('compares equal completed activity windows and ignores the unfinished day', () => {
    const buckets = [
      activityBucket(1, 0),
      activityBucket(2, 1),
      activityBucket(3, 1),
      activityBucket(4, 1),
      activityBucket(5, 3),
      activityBucket(6, 3),
      activityBucket(7, 3),
      activityBucket(8, 50),
    ];

    const [insight] = buildActivityInsights(buckets, 'sessions', 'All subjects', new Date(2026, 7, 8, 12));
    expect(insight.trend).toBe('upward');
    expect(insight.evidence).toContain('9 sessions across the latest 3 completed days');
    expect(insight.evidence).toContain('3 sessions in the preceding 3');
    expect(insight.evidence).not.toContain('50');
  });

  test('reads both total-point direction and subject-grade movement from mock results', () => {
    const insights = buildMockInsights([
      mock('one', '2026-01-10', 350, 'H5', 'H3'),
      mock('two', '2026-03-10', 380, 'H4', 'H4'),
      mock('three', '2026-05-10', 410, 'H3', 'H4'),
    ]);

    expect(insights[0]).toMatchObject({ title: 'Total points', trend: 'upward' });
    expect(insights[0].evidence).toContain('earlier average 350 points, recent average 410 (+60)');
    expect(insights[1]).toMatchObject({ title: 'Subject movement', trend: 'varied' });
    expect(insights[1].evidence).toContain('Biology H5 → H3');
    expect(insights[1].evidence).toContain('Irish H3 → H4');
  });

  test('labels a wide oscillating mock series as varied and empty history as building', () => {
    const varied = buildMockInsights([
      mock('one', '2026-01-10', 400, 'H4', 'H3'),
      mock('two', '2026-02-10', 450, 'H3', 'H3'),
      mock('three', '2026-03-10', 390, 'H4', 'H4'),
      mock('four', '2026-04-10', 440, 'H3', 'H3'),
    ]);

    expect(varied[0].trend).toBe('varied');
    expect(buildMockInsights([])[0].trend).toBe('building');
  });

  test('keeps single-subject results out of full-mock totals and uses them in a subject filter', () => {
    const mixed: UnifiedMockResult[] = [
      mock('full-one', '2026-01-10', 400, 'H5', 'H3'),
      {
        id: 'biology-paper',
        label: 'Biology paper',
        date: '2026-02-10',
        totalPoints: 77,
        timestamp: new Date('2026-02-10T12:00:00').getTime(),
        entries: [{ subjectName: 'Biology', grade: 'H3', level: 'higher' }],
        resultKind: 'single',
      },
      mock('full-two', '2026-03-10', 420, 'H2', 'H3'),
    ];

    const totals = buildMockInsights(mixed);
    expect(totals[0]).toMatchObject({ title: 'Total points', trend: 'upward' });
    expect(totals[0].evidence).toContain('2 full mock sittings');
    expect(totals[0].evidence).not.toContain('77');

    const biology = buildMockInsights(mixed, 'Biology');
    expect(biology).toHaveLength(1);
    expect(biology[0]).toMatchObject({ title: 'Biology results', trend: 'upward' });
    expect(biology[0].evidence).toContain('3 results');
    expect(biology[0].evidence).toContain('Latest grade H2');
  });

  test('uses the same early-versus-recent comparison for mock labels and evidence', () => {
    const insights = buildMockInsights([
      mock('one', '2026-01-10', 450, 'H4', 'H3'),
      mock('two', '2026-02-10', 300, 'H4', 'H3'),
      mock('three', '2026-03-10', 500, 'H3', 'H3'),
      mock('four', '2026-04-10', 440, 'H3', 'H3'),
    ]);

    expect(insights[0].trend).toBe('upward');
    expect(insights[0].evidence).toContain('earlier average 375 points, recent average 470 (+95)');
    expect(insights[0].evidence).not.toContain('-10');
  });

  test('excludes future-dated mock evidence defensively', () => {
    const insights = buildMockInsights([
      mock('past', '2026-08-20', 400, 'H4', 'H3'),
      mock('future', '2026-08-23', 600, 'H1', 'H1'),
    ], 'all', '2026-08-22');

    expect(insights[0]).toMatchObject({ trend: 'building' });
    expect(insights[0].evidence).toBe('One full mock sitting recorded at 400 points.');
  });

  test('uses grade movement rather than CAO points for Ordinary-level direction', () => {
    const upward = buildMockInsights([
      mock('one', '2026-01-10', 300, 'O8', 'H3'),
      mock('two', '2026-03-10', 300, 'O7', 'H3'),
    ], 'Biology');
    const downward = buildMockInsights([
      mock('one', '2026-01-10', 300, 'O7', 'H3'),
      mock('two', '2026-03-10', 300, 'O8', 'H3'),
    ], 'Biology');

    expect(upward[0]).toMatchObject({ trend: 'upward' });
    expect(upward[0].evidence).toContain('1 grade step higher');
    expect(upward[0].evidence).toContain('CAO subject points remain at 0');
    expect(downward[0]).toMatchObject({ trend: 'downward' });
    expect(downward[0].evidence).toContain('1 grade step lower');
  });

  test('shows level changes as a new baseline instead of comparing unlike grade scales', () => {
    const [insight] = buildMockInsights([
      mock('one', '2026-01-10', 300, 'H6', 'H3'),
      mock('two', '2026-03-10', 300, 'O2', 'H3'),
    ], 'Biology');

    expect(insight).toMatchObject({ trend: 'building' });
    expect(insight.evidence).toContain('level changed from Higher to Ordinary');
    expect(insight.evidence).toContain('new ordinary-level baseline');
  });

  test('starts a fresh trend from the latest level-change baseline', () => {
    const [insight] = buildMockInsights([
      mock('one', '2026-01-10', 300, 'H3', 'H3'),
      mock('two', '2026-02-10', 300, 'O4', 'H3'),
      mock('three', '2026-03-10', 300, 'O3', 'H3'),
      mock('four', '2026-04-10', 300, 'O2', 'H3'),
    ], 'Biology');

    expect(insight).toMatchObject({ trend: 'upward' });
    expect(insight.evidence).toContain('3 ordinary-level results since the latest level change');
    expect(insight.evidence).toContain('Latest grade O2');
  });

  test('waits for another result after repeated level switches', () => {
    const [insight] = buildMockInsights([
      mock('one', '2026-01-10', 300, 'H3', 'H3'),
      mock('two', '2026-02-10', 300, 'O4', 'H3'),
      mock('three', '2026-03-10', 300, 'H2', 'H3'),
    ], 'Biology');

    expect(insight).toMatchObject({ trend: 'building' });
    expect(insight.evidence).toContain('level changed 2 times');
    expect(insight.evidence).toContain('Latest grade H2 is the new higher-level baseline');
    expect(insight.evidence).not.toContain('Higher to Higher');
  });

  test('recognises an Ordinary-level grade lift in all-subject mock movement', () => {
    const insights = buildMockInsights([
      mock('one', '2026-01-10', 300, 'O8', 'H3'),
      mock('two', '2026-03-10', 300, 'O7', 'H3'),
    ]);

    expect(insights[1]).toMatchObject({ title: 'Subject movement', trend: 'upward' });
    expect(insights[1].evidence).toContain('Biology O8 → O7');
    expect(insights[1].evidence).toContain('no CAO-point change');
  });
});
