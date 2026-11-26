/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Area 0, the frame: the account sheet on a phone is one bottom sheet with
 * Close at the top left (the shared Sheet), and Settings is a page with Back
 * at the top left (agreed 26 Nov 2026, r5-account-settings). Both keep every
 * row, setting and account action they had.
 */
import React from 'react';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { act, cleanup, fireEvent, render, screen, within } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { MobileProfileSheet } from '@/components/UserProfileMenu';
import SettingsModal from '@/components/SettingsModal';
import type { UserSettings } from '@/types';

vi.mock('@/components/NotificationBell', () => ({
  default: ({ variant }: { variant?: string }) => <button type="button" data-variant={variant}>Notifications</button>,
}));

const settings: UserSettings = { language: 'en', avatar: 'star-crew:maker', darkMode: false, cardStyle: 'default', defaultWorkMinutes: 25, showDashboard: false };

afterEach(cleanup);
beforeEach(() => { window.scrollTo = vi.fn(); });

describe('the account sheet', () => {
  const handlers = () => ({
    onClose: vi.fn(), onLogout: vi.fn(), updateSetting: vi.fn(), onOpenSettings: vi.fn(), onSelectModule: vi.fn(),
    onOpenPassport: vi.fn(), onGoToDashboard: vi.fn(), onGoToInsights: vi.fn(), onGoToReferences: vi.fn(),
    onGoToYearPlans: vi.fn(), onGoToYourSetup: vi.fn(), onOpenSiteGuide: vi.fn(), onOpenFeedback: vi.fn(), onOpenNorthStar: vi.fn(),
  });
  const open = (h: ReturnType<typeof handlers>) => render(<MobileProfileSheet isOpen user={{ uid: 'u', name: 'Demo Student', avatar: '' } as never}
    settings={settings} avatarOverride="" streak={{ currentStreak: 18, longestStreak: 42, lastActiveDate: '' }}
    recommendation={{ moduleId: 'agency', title: 'Controlling the Controllables', reason: 'next' } as never}
    completedCount={27} totalCount={58} hasNorthStar unlockedThemes={[]} {...h} />);

  it('is one sheet with Close at the top left, the name and every row in today’s groups and order', () => {
    const h = handlers();
    open(h);
    const sheet = screen.getByRole('dialog', { name: 'Demo Student' });
    const head = sheet.querySelector('.ui-sheet-head');
    expect(head?.firstElementChild).toHaveAccessibleName('Close profile');
    expect(within(sheet).getByText('18 days streak')).toBeInTheDocument();
    expect(within(sheet).getByText('Longest: 42 days')).toBeInTheDocument();
    const labels = [...sheet.querySelectorAll('.acct-label')].map(label => label.textContent);
    expect(labels).toEqual(["Today's focus", 'Learning', 'Direction', 'Support', 'Account']);
    const rows = within(sheet).getAllByRole('button').map(button => button.textContent?.trim()).filter(Boolean);
    expect(rows).toEqual(['Controlling the Controllables', 'My Progress', 'Study Passport27 / 58', 'Year Plans', 'Your setup', 'My North Star',
      'References', 'Notifications', 'How the app works', 'Give feedback', 'Settings', 'Log out']);
    expect(within(sheet).getByRole('switch', { name: 'Dark mode (Beta)' })).toHaveAttribute('aria-checked', 'false');
  });

  it('keeps every action: each row closes the sheet and does what it did', () => {
    const cases: Array<[string, keyof ReturnType<typeof handlers>]> = [
      ['My Progress', 'onGoToDashboard'], ['Study Passport', 'onOpenPassport'], ['Year Plans', 'onGoToYearPlans'],
      ['Your setup', 'onGoToYourSetup'], ['My North Star', 'onOpenNorthStar'], ['References', 'onGoToReferences'],
      ['How the app works', 'onOpenSiteGuide'], ['Give feedback', 'onOpenFeedback'], ['Settings', 'onOpenSettings'], ['Log out', 'onLogout'],
    ];
    for (const [name, handler] of cases) {
      const h = handlers();
      const { unmount } = open(h);
      fireEvent.click(screen.getByRole('button', { name: new RegExp(`^${name}`) }));
      expect(h[handler]).toHaveBeenCalledTimes(1);
      expect(h.onClose).toHaveBeenCalled();
      unmount();
    }
    const h = handlers();
    open(h);
    fireEvent.click(screen.getByRole('button', { name: 'Controlling the Controllables' }));
    expect(h.onSelectModule).toHaveBeenCalledWith('agency');
    fireEvent.click(screen.getByRole('switch', { name: 'Dark mode (Beta)' }));
    expect(h.updateSetting).toHaveBeenCalledWith('darkMode', true);
    act(() => { fireEvent.click(screen.getByRole('button', { name: 'Close profile' })); });
    expect(h.onClose).toHaveBeenCalled();
  });

  it('draws no orange, no icon tiles and no grey streak box', () => {
    const css = readFileSync(join(process.cwd(), 'components/account-sheet.css'), 'utf8');
    expect(css).not.toMatch(/orange|accent|#[0-9a-f]{3,6}\b/i);
    const source = readFileSync(join(process.cwd(), 'components/UserProfileMenu.tsx'), 'utf8');
    const sheet = source.slice(source.indexOf('export const MobileProfileSheet'));
    expect(sheet).not.toMatch(/bg-orange|text-accent|rose-|rounded-lg border|bg-zinc-50/);
  });
});

describe('Settings, the page', () => {
  const actions = () => ({
    onClose: vi.fn(), updateSetting: vi.fn(), onStartProfileSetup: vi.fn(), onChangeSubjects: vi.fn(),
    onResetNorthStar: vi.fn(), onAdvanceYear: vi.fn(), onLogout: vi.fn(),
  });
  const page = (a: ReturnType<typeof actions>) => render(<SettingsModal isOpen settings={settings} userName="Demo Student" userYearGroup="6th"
    hasStudyProfile hasNorthStar {...a} />);

  it('is a page, not a floating card: Back at the top left and the name once', () => {
    const a = actions();
    page(a);
    expect(screen.queryByRole('dialog')).toBeNull();
    expect(screen.getByRole('heading', { level: 1, name: 'Settings' })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Close' })).toBeNull();
    fireEvent.click(screen.getByRole('button', { name: 'Back' }));
    expect(a.onClose).toHaveBeenCalledTimes(1);
  });

  it('keeps every setting and account action', () => {
    const a = actions();
    page(a);
    expect(screen.getAllByRole('button', { name: /^Select .* avatar$/ })).toHaveLength(8);
    expect(screen.getByRole('button', { name: 'Select The Maker avatar' })).toHaveAttribute('aria-pressed', 'true');
    expect(within(screen.getByRole('group', { name: 'Appearance' })).getAllByRole('button')).toHaveLength(2);
    expect(screen.getByRole('switch', { name: 'Use Essentials Mode' })).toBeInTheDocument();
    for (const name of ['Privacy notice', 'Terms of use', /Delete Account/, 'Change subjects', 'Edit North Star', 'Sign out']) {
      expect(screen.getByRole('button', { name })).toBeInTheDocument();
    }
    fireEvent.click(screen.getByRole('button', { name: 'Change subjects' }));
    expect(a.onChangeSubjects).toHaveBeenCalledTimes(1);
    fireEvent.click(screen.getByRole('button', { name: 'Edit North Star' }));
    expect(a.onResetNorthStar).toHaveBeenCalledTimes(1);
    fireEvent.click(screen.getByRole('button', { name: 'Sign out' }));
    expect(a.onLogout).toHaveBeenCalledTimes(1);
    // The page stays under the pop-ups these open; nothing leaves it first.
    expect(a.onClose).not.toHaveBeenCalled();
    fireEvent.click(screen.getByRole('button', { name: 'Select The Reader avatar' }));
    expect(a.updateSetting).toHaveBeenCalledWith('avatar', 'star-crew:reader');
  });

  it('chooses with the ink outline and the drawn tick, never orange', () => {
    const css = readFileSync(join(process.cwd(), 'components/settings-modal.css'), 'utf8');
    expect(css).toMatch(/\.st-crew-option\[aria-pressed=true\] \{ border-color: var\(--outline-strong\); box-shadow: inset 0 0 0 1px var\(--outline-strong\); \}/);
    expect(css).toMatch(/\[data-slot=switch\]\[data-on=true\] \{ border-color: var\(--action\); background: var\(--action\); \}/);
    expect(css).not.toMatch(/--nsu-orange\)|var\(--accent|nsu-serif/);
  });
});

describe('Settings is reached as a page from both doors', () => {
  it('the account sheet and the menu under the name both open the settings view', () => {
    const app = readFileSync(join(process.cwd(), 'App.tsx'), 'utf8');
    expect(app).toMatch(/const setSettingsOpen = useCallback\(\(open: boolean\) => \{ if \(open\) nav\.navigateToSettings\(\); \}, \[nav\]\);/);
    expect(app).not.toMatch(/<SettingsModal\s+isOpen=\{settingsOpen\}/);
    const router = readFileSync(join(process.cwd(), 'components/AppRouter.tsx'), 'utf8');
    expect(router).toMatch(/if \(viewState === 'settings'\) \{\s*return <>\{settingsPage \?\? null\}<\/>;/);
  });
});
