import React from 'react';
import { act, cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import NextStepUniSidebar from '../components/navigation/NextStepUniSidebar';

const platform = vi.hoisted(() => ({ native: false }));
const navigateToInnovationZone = vi.hoisted(() => vi.fn());
vi.mock('@capacitor/core', () => ({ Capacitor: { isNativePlatform: () => platform.native } }));
vi.mock('../components/NotificationBell', () => ({ default: () => null }));
vi.mock('../components/ShortcutsOverlay', () => ({ openShortcutsOverlay: vi.fn() }));
vi.mock('../contexts/NavigationContext', () => ({ useNavigation: () => ({
  state: { viewState: 'tree' }, navigateToInnovationZone,
  navigateToTree: vi.fn(), navigateToModules: vi.fn(), navigateToStudySession: vi.fn(),
  navigateToYourSetup: vi.fn(), navigateToLearningPaths: vi.fn(), navigateToDashboard: vi.fn(),
  navigateToJourney: vi.fn(), navigateToYearPlans: vi.fn(), navigateToAccreditation: vi.fn(),
}) }));

const props: React.ComponentProps<typeof NextStepUniSidebar> = {
  user: { uid: 'tablet-navigation-test', name: 'Sample Student', avatar: '' },
  settings: { language: 'en', avatar: '', darkMode: false, cardStyle: 'default', defaultWorkMinutes: 25, showDashboard: false },
  updateSetting: vi.fn(), onLogout: vi.fn(), onOpenSettings: vi.fn(), onOpenPassport: vi.fn(),
  onOpenSiteGuide: vi.fn(), onOpenFeedback: vi.fn(), onUnreadCountChange: vi.fn(),
  completedCount: 0, totalCount: 10, unreadCount: 0,
  children: <input aria-label="Unfinished work" defaultValue="Keep my answer" />,
};
let width = 1024;
const mediaListeners = new Set<() => void>();
function resize(next: number) {
  act(() => {
    width = next;
    window.dispatchEvent(new Event('resize'));
    mediaListeners.forEach(listener => listener());
  });
}

beforeEach(() => {
  width = 1024;
  platform.native = false;
  localStorage.clear();
  document.cookie = 'sidebar_state=; max-age=0; path=/';
  navigateToInnovationZone.mockClear();
  vi.spyOn(window, 'innerWidth', 'get').mockImplementation(() => width);
  vi.spyOn(navigator, 'userAgent', 'get').mockReturnValue('Mozilla/5.0 Macintosh Safari');
  vi.spyOn(navigator, 'platform', 'get').mockReturnValue('MacIntel');
  Object.defineProperty(navigator, 'maxTouchPoints', { configurable: true, value: 5 });
  vi.spyOn(window, 'matchMedia').mockImplementation(query => ({
    get matches() { return query.includes('max-width: 767px') && width < 768; },
    media: query, onchange: null,
    addEventListener: (_event: string, listener: () => void) => { mediaListeners.add(listener); },
    removeEventListener: (_event: string, listener: () => void) => { mediaListeners.delete(listener); },
    addListener: vi.fn(), removeListener: vi.fn(), dispatchEvent: () => false,
  } as unknown as MediaQueryList));
});
afterEach(() => { cleanup(); mediaListeners.clear(); vi.restoreAllMocks(); });

describe('persistent tablet navigation', () => {
  it.each([768, 820, 1024, 1366])('shows labelled navigation in iPad Safari at %ipx', viewport => {
    width = viewport;
    render(<NextStepUniSidebar {...props} />);
    expect(screen.getByRole('navigation', { name: 'Main navigation' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Collapse sidebar' })).toHaveAttribute('aria-expanded', 'true');
    fireEvent.click(screen.getByRole('button', { name: 'Mark Bank' }));
    expect(navigateToInnovationZone).toHaveBeenCalledWith('mark-bank');
  });
  it('shows the same sidebar in the native iPad app', () => {
    platform.native = true;
    render(<NextStepUniSidebar {...props} />);
    expect(screen.getByRole('navigation', { name: 'Main navigation' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Open account menu' })).toBeInTheDocument();
  });
  it('keeps the rail available after collapse and restores its labels', () => {
    render(<NextStepUniSidebar {...props} />);
    fireEvent.click(screen.getByRole('button', { name: 'Collapse sidebar' }));
    expect(screen.getByRole('navigation', { name: 'Main navigation' })).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Expand sidebar' }));
    expect(screen.getByRole('button', { name: 'Collapse sidebar' })).toHaveAttribute('aria-expanded', 'true');
    expect(screen.getByRole('textbox', { name: 'Unfinished work' })).toHaveValue('Keep my answer');
  });
  it('switches at the bottom bar breakpoint when iPad Split View is resized', () => {
    render(<NextStepUniSidebar {...props} />);
    resize(767);
    expect(screen.queryByRole('navigation', { name: 'Main navigation' })).toBeNull();
    expect(screen.getByRole('textbox', { name: 'Unfinished work' })).toBeInTheDocument();
    resize(768);
    expect(screen.getByRole('navigation', { name: 'Main navigation' })).toBeInTheDocument();
  });
  it.each([390, 540, 767])('leaves narrow %ipx windows to the bottom navigation', viewport => {
    width = viewport;
    platform.native = true;
    render(<NextStepUniSidebar {...props} />);
    expect(screen.queryByRole('navigation', { name: 'Main navigation' })).toBeNull();
  });
});
