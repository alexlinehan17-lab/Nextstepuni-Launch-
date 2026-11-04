import React from 'react';
import { cleanup, renderHook } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import type * as FirebaseAuth from 'firebase/auth';
import { AuthProvider, useAuth } from '../contexts/AuthContext';
import { isLocalDemoPreview } from '../utils/localDemoPreview';
import { DEMO_STUDENT_UID } from '../data/devStudent';

const mocks = vi.hoisted(() => ({
  native: vi.fn(() => false),
  subscribe: vi.fn(() => vi.fn()),
}));
vi.mock('@capacitor/core', () => ({ Capacitor: { isNativePlatform: mocks.native } }));
vi.mock('firebase/auth', async importOriginal => ({
  ...await importOriginal<typeof FirebaseAuth>(),
  onAuthStateChanged: mocks.subscribe,
}));

const wrapper = ({ children }: { children: React.ReactNode }) => (
  <React.StrictMode><AuthProvider>{children}</AuthProvider></React.StrictMode>
);

beforeEach(() => {
  vi.stubEnv('DEV', true);
  mocks.native.mockReturnValue(false);
  mocks.subscribe.mockClear();
  window.localStorage.clear();
  window.sessionStorage.clear();
});
afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
  vi.unstubAllEnvs();
  vi.unstubAllGlobals();
});

function previewFrame() {
  const frame = document.createElement('iframe');
  frame.setAttribute('data-demo-account', 'true');
  vi.spyOn(window, 'frameElement', 'get').mockReturnValue(frame);
}

describe('local mobile review account', () => {
  it('opens a complete sample account on fresh mounts without subscribing to real authentication', () => {
    previewFrame();
    for (let visit = 0; visit < 2; visit++) {
      const view = renderHook(() => useAuth(), { wrapper });
      expect(view.result.current).toMatchObject({
        user: { uid: DEMO_STUDENT_UID, role: 'student' },
        userResolved: true, authResolved: true, isLoadingAuth: false,
        loadedDataUid: DEMO_STUDENT_UID, loadedDataStatus: 'loaded', needsOnboarding: false,
      });
      expect(view.result.current.loadedData.studentProfile?.subjects).toHaveLength(7);
      view.unmount();
    }
    expect(mocks.subscribe).not.toHaveBeenCalled();
    expect(window.sessionStorage.length).toBe(0);
  });

  it('still opens when browser storage is unavailable', () => {
    previewFrame();
    vi.spyOn(Storage.prototype, 'getItem').mockImplementation(() => { throw new Error('Storage blocked'); });
    const { result } = renderHook(() => useAuth(), { wrapper });
    expect(result.current.user?.uid).toBe(DEMO_STUDENT_UID);
    expect(result.current.loadedData.studentProfile?.subjects).toHaveLength(7);
    expect(mocks.subscribe).not.toHaveBeenCalled();
  });

  it('keeps normal sign-in outside the review iframe', () => {
    const { result } = renderHook(() => useAuth(), { wrapper });
    expect(mocks.subscribe).toHaveBeenCalled();
    expect(result.current.user).toBeNull();
  });

  it('keeps normal sign-in in a production build even if the iframe opts in', () => {
    previewFrame();
    vi.stubEnv('DEV', false);
    const { result } = renderHook(() => useAuth(), { wrapper });
    expect(mocks.subscribe).toHaveBeenCalled();
    expect(result.current.user).toBeNull();
  });

  it('rejects native apps, remote hosts and inaccessible parent frames', () => {
    previewFrame();
    mocks.native.mockReturnValue(true);
    expect(isLocalDemoPreview()).toBe(false);
    mocks.native.mockReturnValue(false);
    const frame = window.frameElement;
    vi.stubGlobal('window', { location: { hostname: 'nextstepuni.com' }, frameElement: frame });
    expect(isLocalDemoPreview()).toBe(false);
    vi.unstubAllGlobals();
    vi.spyOn(window, 'frameElement', 'get').mockImplementation(() => { throw new Error('Cross-origin frame'); });
    expect(isLocalDemoPreview()).toBe(false);
  });
});
