import React from 'react';
import type * as CapacitorModule from '@capacitor/core';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';
import { isMobileAppDesign } from '../hooks/useMobileAppDesign';
import LoginPage from '../components/LoginPage';
import Onboarding from '../components/Onboarding';
import { recordVisit } from '../components/lastVisited';

const native = vi.hoisted(() => ({ enabled: false }));
vi.mock('@capacitor/core', async importOriginal => ({
  ...(await importOriginal<typeof CapacitorModule>()),
  Capacitor: { isNativePlatform: () => native.enabled, getPlatform: () => 'web' },
}));
vi.mock('../utils/funnel', () => ({ trackFunnel: vi.fn() }));
vi.mock('firebase/functions', () => ({ getFunctions: () => ({}), httpsCallable: () => vi.fn().mockRejectedValue(new Error('not signed in')) }));

function device(ua: string, platform: string, touches = 0) {
  vi.spyOn(navigator, 'userAgent', 'get').mockReturnValue(ua);
  vi.spyOn(navigator, 'platform', 'get').mockReturnValue(platform);
  Object.defineProperty(navigator, 'maxTouchPoints', { configurable: true, value: touches });
}
beforeEach(() => {
  native.enabled = false;
  localStorage.clear();
  sessionStorage.clear();
  device('Mozilla/5.0 Macintosh Chrome', 'MacIntel');
});
afterEach(() => { vi.restoreAllMocks(); });

describe('mobile/tablet-only design boundary', () => {
  it.each([320, 768, 1024, 1440])('does not opt a desktop browser in at %i pixels', width => {
    vi.spyOn(window, 'innerWidth', 'get').mockReturnValue(width);
    expect(isMobileAppDesign()).toBe(false);
  });
  it('includes iPad desktop-mode Safari in landscape', () => {
    device('Mozilla/5.0 Macintosh Safari', 'MacIntel', 5);
    vi.spyOn(window, 'innerWidth', 'get').mockReturnValue(1366);
    expect(isMobileAppDesign()).toBe(true);
  });
  it.each(['iPhone', 'iPad', 'Android'])('includes %s browsers', agent => {
    device(agent, '');
    expect(isMobileAppDesign()).toBe(true);
  });
  it('does not treat a Windows touchscreen laptop as an iPad', () => {
    device('Mozilla/5.0 Windows Chrome', 'Win32', 10);
    expect(isMobileAppDesign()).toBe(false);
  });
  it('includes native WebViews regardless of window width', () => {
    native.enabled = true;
    expect(isMobileAppDesign()).toBe(true);
  });
  it('keeps the original desktop welcome and sign-in form', async () => {
    const { container } = render(<LoginPage handleLoginSuccess={vi.fn()} />);
    const login = screen.getAllByRole('button', { name: 'Log in' }).at(-1)!;
    expect(login).toBeInTheDocument();
    expect(container.querySelector('.account-entry')).toBeNull();
    expect(screen.queryByRole('textbox', { name: 'Email' })).toBeNull();
    fireEvent.click(login);
    expect(await screen.findByRole('heading', { name: 'Welcome back', level: 2 })).toBeInTheDocument();
    expect(screen.getByLabelText('Email')).toHaveAttribute('autocomplete', 'email');
    expect(screen.getByRole('button', { name: 'Forgot?' })).toBeInTheDocument();
  });
  it('does not mount or write the new onboarding on desktop', () => {
    const { container } = render(<Onboarding userId="desktop-scope" userName="Alex" onComplete={vi.fn()} onSkip={vi.fn()} />);
    expect(container.querySelector('.setup-flow')).toBeNull();
    expect(localStorage.getItem('nextstepuni:onboarding-draft:v2:desktop-scope:fresh')).toBeNull();
  });
  it('mounts the new onboarding for tablets', () => {
    device('Mozilla/5.0 Macintosh Safari', 'MacIntel', 5);
    const { container } = render(<Onboarding userId="tablet-scope" userName="Alex" onComplete={vi.fn()} onSkip={vi.fn()} />);
    expect(container.querySelector('.setup-flow')).not.toBeNull();
    expect(localStorage.getItem('nextstepuni:onboarding-draft:v2:tablet-scope:fresh')).not.toBeNull();
  });
  it('does not add the mobile recents history on desktop', () => {
    recordVisit('desktop-scope', { kind: 'tool', id: 'planner', label: 'Planner' });
    expect(localStorage.getItem('nsu-recent-tools:desktop-scope')).toBeNull();
  });
});
