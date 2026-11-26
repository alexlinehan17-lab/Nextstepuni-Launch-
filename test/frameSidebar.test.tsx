/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Area 0, the frame: the laptop sidebar is "sidebar B" (agreed 25 Nov 2026).
 * The five places, then Workspace: exactly ten rows. The place you are on is
 * shaded (aria-current), with no bar at its edge. Every destination that left
 * the list is still reachable: Year Plans, Study Passport, Your setup,
 * Insights, My Direction and Account (Settings) from the menu under the
 * student's name, References under Help, Learning paths from its card on Home,
 * War Room and Future Finder from the Launchpad.
 */
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import React from 'react';
import { act, cleanup, fireEvent, render, screen, within } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import NextStepUniSidebar from '../components/navigation/NextStepUniSidebar';
import { SIDEBAR_PLACES, SIDEBAR_WORKSPACE, sidebarItemFor } from '@/utils/places';

const nav = vi.hoisted(() => ({
  state: { viewState: 'tree', activeTool: null as string | null },
  navigateToTree: vi.fn(), navigateToModules: vi.fn(), navigateToStudySession: vi.fn(), navigateToDashboard: vi.fn(),
  navigateToJourney: vi.fn(), navigateToInnovationZone: vi.fn(), navigateToYearPlans: vi.fn(), navigateToYourSetup: vi.fn(),
  navigateToInsights: vi.fn(), navigateToAccreditation: vi.fn(), navigateToLearningPaths: vi.fn(),
}));
vi.mock('@capacitor/core', () => ({ Capacitor: { isNativePlatform: () => false } }));
vi.mock('../components/NotificationBell', () => ({ default: () => null }));
vi.mock('../components/ShortcutsOverlay', () => ({ openShortcutsOverlay: vi.fn() }));
vi.mock('../contexts/NavigationContext', () => ({ useNavigation: () => nav }));

const props: React.ComponentProps<typeof NextStepUniSidebar> = {
  user: { uid: 'sidebar-b-test', name: 'Sample Student', avatar: '' },
  settings: { language: 'en', avatar: '', darkMode: false, cardStyle: 'default', defaultWorkMinutes: 25, showDashboard: false },
  updateSetting: vi.fn(), onLogout: vi.fn(), onOpenSettings: vi.fn(), onOpenPassport: vi.fn(),
  onOpenSiteGuide: vi.fn(), onOpenFeedback: vi.fn(), onOpenDirection: vi.fn(), onUnreadCountChange: vi.fn(),
  completedCount: 27, totalCount: 58, unreadCount: 0,
  children: <p>Page</p>,
};

beforeEach(() => {
  nav.state = { viewState: 'tree', activeTool: null };
  vi.spyOn(window, 'innerWidth', 'get').mockReturnValue(1280);
  vi.spyOn(window, 'matchMedia').mockImplementation(query => ({
    matches: false, media: query, onchange: null, addEventListener: vi.fn(), removeEventListener: vi.fn(),
    addListener: vi.fn(), removeListener: vi.fn(), dispatchEvent: () => false,
  } as unknown as MediaQueryList));
});
afterEach(() => { cleanup(); vi.restoreAllMocks(); vi.useRealTimers(); });

const ROWS = ['Home', 'Modules', 'Study session', 'My Progress', 'My Island', 'Launchpad', 'Mark Bank', 'Planner', 'Topic Atlas', 'Paper Trail'];

describe('sidebar B', () => {
  it('lists exactly the ten places, in two groups, in the agreed order', () => {
    render(<NextStepUniSidebar {...props} />);
    const list = screen.getByRole('navigation', { name: 'Main navigation' });
    expect(within(list).getAllByRole('button').map(button => button.getAttribute('aria-label'))).toEqual(ROWS);
    expect(within(list).getByText('Workspace')).toBeInTheDocument();
    expect(SIDEBAR_PLACES.length + SIDEBAR_WORKSPACE.length).toBe(10);
    for (const gone of ['Your setup', 'Learning paths', 'War Room', 'Future Finder', 'Study Passport', 'Year Plans', 'References']) {
      expect(within(list).queryByRole('button', { name: gone })).toBeNull();
    }
  });

  it.each([
    ['tree', null, 'Home'], ['modules', null, 'Modules'], ['category', null, 'Modules'], ['study-session', null, 'Study session'],
    ['dashboard', null, 'My Progress'], ['insights', null, null], ['learning-paths', null, 'Home'], ['my-direction', null, null], ['my-journey', null, 'My Island'],
    ['innovation-zone', null, 'Launchpad'], ['innovation-zone', 'war-room', 'Launchpad'], ['innovation-zone', 'future-finder-revamped', 'Launchpad'],
    ['innovation-zone', 'mark-bank', 'Mark Bank'], ['innovation-zone', 'planner', 'Planner'], ['innovation-zone', 'topic-atlas', 'Topic Atlas'],
    ['innovation-zone', 'paper-trail', 'Paper Trail'], ['settings', null, null], ['year-plans', null, null], ['your-setup', null, null],
  ])('on %s (tool %s) shades %s', (viewState, activeTool, row) => {
    nav.state = { viewState, activeTool };
    render(<NextStepUniSidebar {...props} />);
    const list = screen.getByRole('navigation', { name: 'Main navigation' });
    const current = within(list).getAllByRole('button').filter(button => button.getAttribute('aria-current') === 'page');
    expect(current.map(button => button.getAttribute('aria-label'))).toEqual(row ? [row] : []);
    expect(sidebarItemFor({ viewState, activeTool }) === null).toBe(row === null);
  });

  it('opens each place it lists', () => {
    render(<NextStepUniSidebar {...props} />);
    fireEvent.click(screen.getByRole('button', { name: 'My Island' }));
    expect(nav.navigateToJourney).toHaveBeenCalled();
    fireEvent.click(screen.getByRole('button', { name: 'Paper Trail' }));
    expect(nav.navigateToInnovationZone).toHaveBeenCalledWith('paper-trail');
  });

  it('keeps every destination that left the list in the menu under the name', async () => {
    vi.useFakeTimers({ toFake: ['setTimeout'] });
    render(<NextStepUniSidebar {...props} />);
    const trigger = screen.getByRole('button', { name: 'Open account menu' });
    const open = () => act(() => { fireEvent.click(trigger); });
    const choose = (name: RegExp) => { open(); act(() => { fireEvent.click(screen.getByRole('menuitem', { name })); vi.runAllTimers(); }); };
    open();
    const menu = screen.getByRole('menu');
    for (const name of [/Year Plans/, /Study Passport\s*27 \/ 58/, /Your setup/, /Insights/, /My Direction/, /Account/, /Keyboard shortcuts/, /Language/, /Theme/, /Help/, /Log out/]) {
      expect(within(menu).getByRole('menuitem', { name })).toBeInTheDocument();
    }
    act(() => { fireEvent.keyDown(menu, { key: 'Escape' }); });
    choose(/Year Plans/); expect(nav.navigateToYearPlans).toHaveBeenCalled();
    choose(/Study Passport/); expect(props.onOpenPassport).toHaveBeenCalled();
    choose(/Your setup/); expect(nav.navigateToYourSetup).toHaveBeenCalled();
    choose(/Insights/); expect(nav.navigateToInsights).toHaveBeenCalled();
    choose(/My Direction/); expect(props.onOpenDirection).toHaveBeenCalled();
    choose(/^Account$/); expect(props.onOpenSettings).toHaveBeenCalled();
    choose(/Log out/); expect(props.onLogout).toHaveBeenCalled();
  });

  it('is drawn as agreed: white, the 1.5px ink rule, a shaded current row and no bar at its edge', () => {
    const css = readFileSync(join(process.cwd(), 'components/navigation/sidebar.css'), 'utf8');
    expect(css).toMatch(/\[data-slot=sidebar-container\] \{[^}]*border-right:1\.5px solid var\(--outline-strong\)/);
    expect(css).toMatch(/\.nsu-nav-button\[data-active\] \{ background:var\(--surface-soft\) !important; color:var\(--ink-primary\)/);
    expect(css).not.toContain('nsu-nav-active-line');
    const source = readFileSync(join(process.cwd(), 'components/navigation/NextStepUniSidebar.tsx'), 'utf8');
    expect(source).not.toContain('active-line');
  });
});

describe('the leaving destinations are reachable elsewhere', () => {
  it('Learning paths opens from its card on laptop Home; War Room and Future Finder are Launchpad tools; References is under Help', () => {
    const home = readFileSync(join(process.cwd(), 'components/StudentHomeContent.tsx'), 'utf8');
    expect(home).toMatch(/title: 'Learning Paths'[^}]*go: onGoToLearningPaths/);
    const launchpad = readFileSync(join(process.cwd(), 'components/InnovationZone.tsx'), 'utf8');
    expect(launchpad).toMatch(/id: 'war-room'/);
    expect(launchpad).toMatch(/id: 'future-finder-revamped'/);
    const sidebar = readFileSync(join(process.cwd(), 'components/navigation/NextStepUniSidebar.tsx'), 'utf8');
    expect(sidebar).toMatch(/onClick=\{nav\.navigateToAccreditation\}>References</);
  });
});
