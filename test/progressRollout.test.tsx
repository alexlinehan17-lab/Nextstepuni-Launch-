import React from 'react';
import type * as Recharts from 'recharts';
import type * as Motion from 'motion/react';
import { describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen, within } from '@testing-library/react';
import { buildMethodJournal, confidenceChartData, selectSubjects, subjectColour } from '../components/dashboard/progress/progressData';
import { ProgressConfidence, ProgressSubjects } from '../components/dashboard/progress/ProgressCharts';
import { MethodJournal } from '../components/dashboard/progress/MethodJournal';
import { ProgressSummary } from '../components/dashboard/progress/ProgressSummary';
import KobraScope from '../components/approved-ui-runtime';
import type { StudySessionRecord } from '../utils/strategyRegistry';
import type { DebriefEntry } from '../components/StudyDebrief';
import type { ConfidenceObservation } from '../components/dashboard/dashboardAnalytics';
import { buildActivityBuckets } from '../components/dashboard/dashboardAnalytics';

// Give the chart a deterministic size in jsdom while retaining real Recharts lines/dots.
vi.mock('recharts', async importOriginal => {
  const actual = await importOriginal<typeof Recharts>();
  return { ...actual, ResponsiveContainer: ({ children }: { children: React.ReactElement }) => React.cloneElement(children as React.ReactElement<{ width: number; height: number }>, { width: 720, height: 320 }) };
});
vi.mock('motion/react', async importOriginal => {
  const actual = await importOriginal<typeof Motion>();
  return { ...actual, useReducedMotion: () => true };
});
const now = new Date(2026, 8, 27, 12);
const session = (id: string, subject: string, date: string, strategiesShown: string[]): StudySessionRecord => ({
  id, subject, date, strategiesShown, sessionType: 'practice', plannedMinutes: 25, actualSeconds: 1500,
  startedAt: new Date(`${date}T12:00:00`).getTime(), completedAt: new Date(`${date}T12:25:00`).getTime(), pointsEarned: 10, hadReflection: false,
});
const debrief = (id: string, subject: string, date: string, strategy: string): DebriefEntry => ({
  id, subject, date, strategy, sessionType: 'practice', durationMinutes: 20, hardestTopic: '', confidenceBefore: 2, confidenceAfter: 4, whatWorked: '',
});
const subjects = ['Geography', 'Irish', 'Mathematics', 'Applied Maths', 'Accounting', 'Politics & Society', 'English'];
const observations: ConfidenceObservation[] = subjects.flatMap((subject, index) => [
  { id: `${index}-first`, subject, timestamp: new Date(2026, 8, 1 + index, 12).getTime(), dateKey: `2026-09-0${index + 1}`, score: 3, label: 'okay' as const },
  { id: `${index}-last`, subject, timestamp: new Date(2026, 8, 21 + index, 12).getTime(), dateKey: `2026-09-${21 + index}`, score: 4, label: 'good' as const },
]);
const bounds = { start: new Date(2026, 8, 1), end: new Date(2026, 9, 1), label: 'September 2026' };

describe('approved Progress rollout', () => {
  it('filters several subjects without changing source records; clearing restores historical subjects', () => {
    const records = [session('1', 'Irish', '2026-09-22', []), session('2', 'Geography', '2026-09-23', []), session('3', 'Old subject', '2026-09-24', [])];
    expect(selectSubjects(records, ['Irish', 'Geography'])).toEqual(records.slice(0, 2));
    expect(selectSubjects(records, [])).toBe(records);
    expect(records).toHaveLength(3);
  });

  it('keeps prompt exposure and legacy self-reported use distinct, scoped to the selected period', () => {
    const sessions = [session('1', 'Irish', '2026-09-22', ['mastering-active-recall-protocol', 'mastering-active-recall-protocol']), session('2', 'Geography', '2026-09-01', ['mastering-interleaving-protocol'])];
    const debriefs = [debrief('1', 'Irish', '2026-09-23', 'active-recall'), debrief('2', 'Irish', '2026-09-24', 'flashcards'), debrief('3', 'Irish', '2025-09-24', 'videos')];
    const methods = buildMethodJournal(sessions, debriefs, 'week', now);
    const recall = methods.find(method => method.id === 'mastering-active-recall-protocol')!;
    expect(recall.entries).toHaveLength(2);
    expect(recall.entries.map(entry => entry.evidence).sort()).toEqual(['prompt', 'reported']);
    expect(methods.map(method => method.name)).toEqual(['Active Recall', 'Flashcards']);
    expect(buildMethodJournal(sessions, debriefs, 'month', now).map(method => method.name)).toContain('Interleaving');
  });

  it('keeps sparse recorded check-ins without inventing values between them', () => {
    const data = confidenceChartData(observations, subjects);
    expect(data).toHaveLength(14);
    expect(data[0].s0).toBe(3);
    expect(data[0].s1).toBeUndefined();
    expect(Object.values(data[data.length - 1])).toContain(4);
    expect(new Set(subjects.map(subject => subjectColour(subject, subjects))).size).toBe(7);
    expect(observations[0].score).toBe(3);
  });

  it('renders every subject with continuous coloured lines and filled markers in both views', () => {
    const { container } = render(<KobraScope sound={false}><ProgressConfidence observations={observations} bounds={bounds} subjects={subjects} universe={subjects} insights={null} /></KobraScope>);
    const assertLines = () => {
      const lines = Array.from(container.querySelectorAll('.recharts-line-curve'));
      expect(lines).toHaveLength(7);
      expect(new Set(lines.map(line => line.getAttribute('stroke'))).size).toBe(7);
      lines.forEach(line => {
        expect(line).not.toHaveAttribute('stroke-dasharray');
        expect(line.getAttribute('d')?.match(/M/g)).toHaveLength(1);
      });
      const dots = Array.from(container.querySelectorAll('.recharts-line-dot'));
      expect(dots).toHaveLength(14);
      dots.forEach(dot => {
        expect(dot.getAttribute('fill')).not.toBe('#fff');
        expect(dot.getAttribute('fill')).toBe(dot.getAttribute('stroke'));
        expect(dot).toHaveAttribute('stroke-width', '0');
      });
    };
    assertLines();
    fireEvent.click(screen.getByRole('tab', { name: 'By subject' }));
    expect(container.querySelectorAll('.pr-confidence-grid > article')).toHaveLength(7);
    assertLines();
    fireEvent.click(within(screen.getByRole('group', { name: 'Subjects to compare' })).getByRole('checkbox', { name: 'Irish' }));
    expect(container.querySelectorAll('.recharts-line-curve')).toHaveLength(6);
  });

  it('keeps every subject in the Star Crew chart, including an eighth historical subject', () => {
    const values = [...subjects, 'Biology'].map((label, index) => ({ id: label, label, value: index * 10 + 10 }));
    const { container } = render(<KobraScope sound={false}><ProgressSubjects values={values} period="September" /></KobraScope>);
    expect(container.querySelectorAll('.pr-crew-bar')).toHaveLength(8);
    expect(container.querySelectorAll('.pr-crew-bar .pr-subject-art')).toHaveLength(8);
    fireEvent.click(screen.getByRole('tab', { name: 'A–Z' }));
    expect(container.querySelector('.pr-bar-column')?.textContent).toContain('Accounting');
    expect(screen.getByRole('img', { name: /Biology: 80 minutes/ })).toBeInTheDocument();
  });

  it('falls back to a valid method when filters remove the currently open one', () => {
    const methods = buildMethodJournal([session('1', 'Irish', '2026-09-22', ['mastering-active-recall-protocol'])], [debrief('1', 'Geography', '2026-09-23', 'flashcards')], 'week', now);
    const { rerender } = render(<KobraScope sound={false}><MethodJournal methods={methods} period="This week" /></KobraScope>);
    fireEvent.click(screen.getByRole('button', { name: /Flashcards/ }));
    rerender(<KobraScope sound={false}><MethodJournal methods={methods.filter(method => method.name === 'Active Recall')} period="This week" /></KobraScope>);
    expect(screen.getByRole('button', { name: /Active Recall/ })).toHaveAttribute('aria-pressed', 'true');
    rerender(<KobraScope sound={false}><MethodJournal methods={[]} period="This week" /></KobraScope>);
    expect(screen.getByText('No techniques tracked yet')).toBeInTheDocument();
  });

  it('shows lifetime earnings and spendable balance as different values', () => {
    render(<KobraScope sound={false}><ProgressSummary period="September" minutes={0} sessions={0} activeDays={0} confidence={null} streak={0} pointsEarned={6240} pointsAvailable={5065} buckets={[]} /></KobraScope>);
    expect(screen.getByText('6,240')).toBeInTheDocument();
    expect(screen.getByText('5,065 available to spend')).toBeInTheDocument();
    expect(screen.getByText('Awaiting your first check-in')).toBeInTheDocument();
  });

  it('reads the selected focus column from filtered records and changes period without retaining stale details', () => {
    const records = [session('1', 'Irish', '2026-09-22', []), session('2', 'Mathematics', '2026-09-22', [])];
    const summary = (range: 'week' | 'month' | 'year', subject = 'all') => <KobraScope sound={false}>
      <ProgressSummary period={range} minutes={subject === 'all' ? 50 : 25} sessions={records.length} activeDays={1} confidence={null} streak={0} pointsEarned={0} buckets={buildActivityBuckets(records, range, subject, now)} />
    </KobraScope>;
    const { rerender } = render(summary('week'));
    const columns = () => within(screen.getByRole('group', { name: 'Focus time in the selected period' }));
    expect(columns().getAllByRole('button')).toHaveLength(7);
    const tuesday = columns().getByRole('button', { name: 'Tuesday, 22 September: 50 minutes' });
    fireEvent.click(tuesday);
    expect(tuesday).toHaveAttribute('aria-pressed', 'true');
    expect(screen.getByRole('status')).toHaveTextContent('50 minutes of focused study');

    rerender(summary('week', 'Irish'));
    expect(screen.getByRole('status')).toHaveTextContent('25 minutes of focused study');
    fireEvent.focus(columns().getByRole('button', { name: 'Wednesday, 23 September: 0 minutes' }));
    expect(screen.getByRole('status')).toHaveTextContent('Wednesday, 23 September · No study recorded');

    rerender(summary('year'));
    expect(columns().getAllByRole('button')).toHaveLength(12);
    expect(columns().getByRole('button', { name: 'September 2026: 50 minutes' })).toHaveAttribute('aria-pressed', 'true');
    expect(screen.getByRole('status')).toHaveTextContent('September 2026 · 50 minutes of focused study');
    rerender(summary('month'));
    expect(columns().getAllByRole('button')).toHaveLength(30);
    expect(screen.getByRole('status')).toHaveTextContent('Wednesday, 23 September · No study recorded');
    fireEvent.click(columns().getByRole('button', { name: 'Tuesday, 22 September: 50 minutes' }));
    expect(screen.getByRole('status')).toHaveTextContent('Tuesday, 22 September · 50 minutes of focused study');
  });
});
