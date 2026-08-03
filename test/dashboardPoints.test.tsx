/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Progress page's "Journey points / earned to date" stat.
 *
 * It was wired to `pointsData.balance` — earned MINUS spent — so it fell every
 * time a student bought something, and once spending overtook current earnings
 * it rendered "−23 earned to date": the page told a student they had earned a
 * negative number of points for having used the shop.
 *
 * These tests pin the distinction the caption makes. Lifetime earnings only
 * ever increment, so the stat can never go backwards; the spendable balance is
 * a different number shown elsewhere.
 */
import { describe, test, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

vi.mock('@/components/MountainLandscape', () => ({
  default: () => <div data-testid="mountains" />,
}));

import DashboardView from '@/components/DashboardView';

const COURSES = [
  { id: 'm1', category: 'architecture-mindset', title: 'One', subtitle: '', description: '', sectionsCount: 2, tags: [] },
] as never;

const renderDashboard = (pointsEarned: number) =>
  render(
    <DashboardView
      userProgress={{ m1: { unlockedSection: 2 } }}
      allCourses={COURSES}
      categoryTitles={{} as never}
      streak={{ currentStreak: 0 } as never}
      recommendation={null}
      onSelectModule={vi.fn()}
      onBack={vi.fn()}
      pointsEarned={pointsEarned}
    />,
  );

/** The stat value sits in the same cell as its "earned to date" caption. */
const earnedStat = () => {
  const caption = screen.getByText('earned to date');
  const cell = caption.parentElement;
  if (!cell) throw new Error('stat cell not found');
  return cell.querySelector('p:nth-of-type(2)')?.textContent ?? '';
};

describe('Progress page — journey points', () => {
  test('shows lifetime points earned', () => {
    renderDashboard(485);
    expect(earnedStat()).toBe('485');
  });

  test('a student who has spent more than they currently hold still sees what they earned', () => {
    // The reported case: balance was −23, lifetime earnings were not.
    renderDashboard(120);
    expect(earnedStat()).toBe('120');
    expect(screen.queryByText('-23')).not.toBeInTheDocument();
    expect(screen.queryByText(/^-\d/)).not.toBeInTheDocument();
  });

  test('a brand-new student sees zero, not a negative', () => {
    renderDashboard(0);
    expect(earnedStat()).toBe('0');
  });

  /**
   * The defect was in the WIRING, not in this component — the router handed it
   * `pointsData.balance`. Rendering DashboardView with an explicit prop cannot
   * catch that, and neither can the compiler: balance and totalEarned are both
   * `number`, so `pointsEarned={pointsData.balance}` still typechecks. This
   * reads the call site itself, which is the only place the mistake can recur.
   */
  test('the router feeds the stat lifetime earnings, not the spendable balance', () => {
    const router = readFileSync(
      resolve(__dirname, '../components/AppRouter.tsx'),
      'utf8',
    );
    const call = /<DashboardView[\s\S]*?\/>/.exec(router)?.[0];
    expect(call, 'DashboardView call site not found in AppRouter').toBeTruthy();
    expect(call).toContain('pointsEarned={pointsData.totalEarned}');
    expect(call).not.toContain('pointsData.balance');
  });
});
