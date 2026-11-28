/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Area 3, My Progress in the agreed look (c-progress.html, r5-b2.html
 * "r5-my-progress"): the five parts from one menu that says which of five,
 * Week / Month / Year as words, the figures in a line showing the same numbers
 * as before, no leave control on a place, and the shared parts extended for it
 * (the numbered menu with its count at the end; choices as words). The numbers
 * themselves come from dashboardAnalytics, which this area did not touch.
 */
import React, { useState } from 'react';
import { act, cleanup, fireEvent, render, screen, within } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, test, vi } from 'vitest';
import DashboardView from '@/components/DashboardView';
import { ProgressMilestones } from '@/components/dashboard/progress/ProgressMilestones';
import { Menu } from '@/components/ui/Menu';
import { SelectionWords } from '@/components/ui/Choice';
import { List, Row } from '@/components/ui/List';
import { createDemoStudentLoadedData } from '@/data/devStudent';
import { ALL_COURSES } from '@/courseData';
import { ATHLETE_RANKS, type GamificationState } from '@/gamificationConfig';
import { averageConfidence, collectConfidenceObservations, confidenceInRange, filterSessions } from '@/components/dashboard/dashboardAnalytics';

const device = vi.hoisted(() => ({ phone: true }));
vi.mock('@/hooks/useMobileAppDesign', () => ({ useMobileAppDesign: () => device.phone, isMobileAppDesign: () => device.phone }));
vi.mock('@/components/MountainLandscape', () => ({ default: () => <div>Programme mountains</div> }));

const NOW = new Date(2026, 8, 20, 12);
beforeEach(() => { device.phone = true; vi.useFakeTimers({ toFake: ['Date'] }); vi.setSystemTime(NOW); });
afterEach(() => { cleanup(); vi.useRealTimers(); });

const settle = () => act(async () => { await new Promise(resolve => setTimeout(resolve, 30)); });
const demo = () => createDemoStudentLoadedData(new Date());
function show(extra: Partial<React.ComponentProps<typeof DashboardView>> = {}) {
  const data = demo();
  const props: React.ComponentProps<typeof DashboardView> = {
    userProgress: data.userProgress, allCourses: ALL_COURSES, categoryTitles: {} as never,
    streak: { currentStreak: 18, longestStreak: 42, lastActiveDate: '2026-09-20' }, recommendation: null,
    onSelectModule: vi.fn(), onBack: vi.fn(), pointsEarned: 6240, pointsAvailable: 5065, studentProfile: data.studentProfile,
    studySessions: data.rawProgressDoc.studySessions, studyDebriefs: data.rawProgressDoc.studyDebriefs,
    studyReflections: data.rawProgressDoc.reflections, topicMastery: data.rawProgressDoc.topicMasteryV2,
    mockResults: data.rawProgressDoc.unifiedMockResults, ...extra,
  };
  return { ...render(<DashboardView {...props} />), data };
}
const partButton = () => screen.getByRole('button', { name: /Progress section/ });
const figure = (name: string) => {
  const term = screen.getAllByText(name, { selector: 'dt' })[0];
  return term.nextElementSibling?.querySelector('.mp-fig-value')?.textContent;
};

describe('My Progress, the frame', () => {
  test('a place: no leave control, the small label and the name', () => {
    show();
    expect(screen.queryByRole('button', { name: /^Back/ })).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Back to home' })).not.toBeInTheDocument();
    expect(screen.getByText('Your record')).toBeInTheDocument();
    expect(screen.getByRole('heading', { level: 1, name: 'My Progress' })).toBeInTheDocument();
  });

  test('the part menu switches part and says which of five, with a tick on the part you are on', async () => {
    show();
    expect(partButton()).toHaveTextContent(/Overview\s*·?\s*1 of 5/);
    fireEvent.click(partButton());
    const menu = await screen.findByRole('menu');
    const items = within(menu).getAllByRole('menuitemradio');
    expect(items.map(item => item.textContent)).toEqual(['01Overview', '02Study', '03Confidence', '04Practice', '05Milestones']);
    expect(within(menu).getByRole('menuitemradio', { name: 'Overview' })).toHaveAttribute('aria-checked', 'true');
    fireEvent.click(within(menu).getByRole('menuitemradio', { name: 'Practice' }));
    await settle();
    expect(partButton()).toHaveTextContent(/Practice\s*·?\s*4 of 5/);
    expect(screen.getByRole('heading', { name: 'Topic readiness' })).toBeInTheDocument();
    // The foot of a part names the next one.
    fireEvent.click(screen.getByRole('button', { name: /Next · 5 of 5\s*Milestones/ }));
    expect(partButton()).toHaveTextContent(/Milestones\s*·?\s*5 of 5/);
  });

  test('Week, Month and Year are words that switch the period, the chosen one checked', () => {
    show();
    const words = screen.getByRole('radiogroup', { name: 'Dashboard time range' });
    expect(within(words).getAllByRole('radio').map(word => word.textContent)).toEqual(['Week', 'Month', 'Year']);
    expect(within(words).getByRole('radio', { name: 'Week' })).toHaveAttribute('aria-checked', 'true');
    expect(screen.getByText(/· Focus time$/).textContent).toMatch(/^\d+ \w+ – \d+ \w+ · Focus time$/);
    fireEvent.click(within(words).getByRole('radio', { name: 'Month' }));
    expect(within(words).getByRole('radio', { name: 'Month' })).toHaveAttribute('aria-checked', 'true');
    expect(screen.getByText(/· Focus time$/)).toHaveTextContent('September · Focus time');
    fireEvent.keyDown(within(words).getByRole('radio', { name: 'Month' }), { key: 'ArrowRight' });
    expect(within(words).getByRole('radio', { name: 'Year' })).toHaveAttribute('aria-checked', 'true');
    expect(screen.getByText(/· Focus time$/)).toHaveTextContent('2026 · Focus time');
  });
});

describe('My Progress, the numbers', () => {
  test('the figures in a line are the same numbers as before for the same data', () => {
    const { data } = show();
    const sessions = data.rawProgressDoc.studySessions;
    const week = filterSessions(sessions, 'week');
    const confidence = averageConfidence(confidenceInRange(collectConfidenceObservations(sessions, data.rawProgressDoc.studyDebriefs, data.rawProgressDoc.reflections), 'week'));
    expect(figure('Sessions')).toBe(String(week.length));
    expect(figure('Confidence')).toBe(confidence === null ? '–' : confidence.toFixed(1));
    expect(figure('Study streak')).toBe('18');
    const minutes = Math.round(week.reduce((sum, item) => sum + Math.max(0, item.actualSeconds), 0) / 60);
    expect(document.querySelector('.pr-focus-total')).toHaveAccessibleName(minutes >= 60 ? `${Math.floor(minutes / 60)}h${minutes % 60 ? ` ${minutes % 60}m` : ''}` : `${minutes}m`);
    // Journey points: earned and spendable stay two different values.
    expect(screen.getByText('6,240')).toBeInTheDocument();
    expect(screen.getByText('5,065 available to spend')).toBeInTheDocument();
  });

  test('a student with no check-ins is told so, not shown a made-up figure', () => {
    show({ studySessions: [], studyDebriefs: [], studyReflections: [], mockResults: [] });
    expect(figure('Confidence')).toBe('–');
    expect(screen.getAllByText(/Awaiting your first check-in/).length).toBeGreaterThan(0);
    expect(screen.getByRole('heading', { name: 'Start with one focused session.' })).toBeInTheDocument();
  });

  test('Milestones: the rank bar is a charcoal line with its orange mark, and the four figures sit in a line', () => {
    const state: GamificationState = {
      totalPointsEarned: 6240, currentStreak: 18, longestStreak: 42, modulesCompleted: 3, sectionsCompleted: 40, categoriesCompleted: 0,
      totalReflections: 3, totalTimetableSessions: 5, northStarCategory: null, currentRank: ATHLETE_RANKS[2], nextRank: ATHLETE_RANKS[3],
      rankProgress: 70, unlockedAchievements: [], achievementTimestamps: {}, weeklyGoalProgress: {}, weekStartDate: '',
      personalBests: { bestDayReflections: 2, bestDayPoints: 112, bestDaySections: 8, bestWeekPoints: 486, bestWeekSessions: 11 },
      journeyMilestones: 0, streakShields: 0,
    };
    render(<ProgressMilestones state={state} streak={{ currentStreak: 18, longestStreak: 42, lastActiveDate: '' }} sessions={[]} strategyMastery={{}} curriculumLevel="senior" pointsAvailable={5065} />);
    const bar = screen.getByRole('progressbar', { name: 'Rank progress' });
    expect(bar).toHaveClass('mp-rankbar');
    expect(bar).toHaveAttribute('aria-valuenow', '70');
    expect((bar.firstElementChild as HTMLElement).style.width).toBe('70%');
    expect(screen.getByRole('heading', { name: 'The work adds up.' })).toBeInTheDocument();
    expect(screen.getAllByText(/^(Day streak|Sessions|Focused time|Badges)$/, { selector: 'dt' })).toHaveLength(4);
    expect(screen.getByText('Longest streak: 42 days.')).toBeInTheDocument();
  });
});

describe('shared parts extended for My Progress', () => {
  const PARTS = [
    { value: 'overview', label: 'Overview' }, { value: 'study', label: 'Study' }, { value: 'confidence', label: 'Confidence' },
    { value: 'practice', label: 'Practice' }, { value: 'milestones', label: 'Milestones' },
  ];
  test('Menu: a full-width button carries its count at the end in the mono; numbered options keep their names', async () => {
    function Harness() {
      const [part, setPart] = useState('overview');
      return <Menu label="Progress section" count numbered block value={part} onChange={setPart} options={PARTS} />;
    }
    render(<Harness />);
    const button = screen.getByRole('button', { name: /Progress section/ });
    expect(button.querySelector('.ui-menu-btn-count--end')).toHaveTextContent('1 of 5');
    expect(button).toHaveAccessibleName(/Progress section:\s*Overview\s*·\s*1 of 5/);
    fireEvent.click(button);
    const item = await screen.findByRole('menuitemradio', { name: 'Study' });
    expect(item.querySelector('.ui-menu-num')).toHaveTextContent('02');
    fireEvent.click(item);
    await settle();
    expect(screen.getByRole('button', { name: /Progress section/ }).querySelector('.ui-menu-btn-count--end')).toHaveTextContent('2 of 5');
  });

  test('Menu: a detail readout at the end of a full-width button (a method\'s entries)', () => {
    render(<Menu label="Choose a method" block value="recall" onChange={() => {}} detail="2 entries" options={[{ value: 'recall', label: 'Active Recall' }]} />);
    expect(screen.getByRole('button', { name: /Choose a method/ }).querySelector('.ui-menu-btn-count--end')).toHaveTextContent('2 entries');
  });

  test('SelectionWords: a radio group of words; arrow keys move and choose', () => {
    function Harness() {
      const [period, setPeriod] = useState('week');
      return <SelectionWords label="Period" value={period} onChange={setPeriod} options={[{ value: 'week', label: 'Week' }, { value: 'month', label: 'Month' }, { value: 'year', label: 'Year' }]} />;
    }
    render(<Harness />);
    const week = screen.getByRole('radio', { name: 'Week' });
    expect(week).toHaveAttribute('aria-checked', 'true');
    expect(week).toHaveAttribute('tabindex', '0');
    expect(screen.getByRole('radio', { name: 'Month' })).toHaveAttribute('tabindex', '-1');
    fireEvent.keyDown(week, { key: 'End' });
    expect(screen.getByRole('radio', { name: 'Year' })).toHaveAttribute('aria-checked', 'true');
    expect(screen.getByRole('radio', { name: 'Year' })).toHaveFocus();
  });

  test('Row: a row that moves forward ends in an arrow; a row that opens in place says so and turns its chevron', () => {
    function Harness() {
      const [open, setOpen] = useState(false);
      return <List><Row over="Next · 2 of 5" title="Study" forward onPress={() => {}} /><Row title="Full one" value="350 points" expanded={open} onPress={() => setOpen(!open)} /></List>;
    }
    const { container } = render(<Harness />);
    expect(container.querySelector('[data-arrow], .lucide-arrow-right')).not.toBeNull();
    const row = screen.getByRole('button', { name: /Full one/ });
    expect(row).toHaveAttribute('aria-expanded', 'false');
    fireEvent.click(row);
    expect(row).toHaveAttribute('aria-expanded', 'true');
    expect(row.querySelector('.ui-row-chev--down')).toHaveAttribute('data-open', 'true');
  });
});
