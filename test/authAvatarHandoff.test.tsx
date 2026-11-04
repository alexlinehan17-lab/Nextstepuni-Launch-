import React from 'react';
import { act, renderHook } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { AuthProvider, useAuth } from '../contexts/AuthContext';

const mocks = vi.hoisted(() => ({
  listener: null as null | ((user: any) => Promise<void>),
  userDoc: vi.fn(),
  progressDoc: vi.fn(),
}));
vi.mock('firebase/auth', () => ({
  onAuthStateChanged: (_auth: unknown, listener: (user: any) => Promise<void>) => {
    mocks.listener = listener;
    return vi.fn();
  },
  signOut: vi.fn(),
}));
vi.mock('../services/userRepository', () => ({ waitForUserDocument: mocks.userDoc, mergeUserDocument: vi.fn().mockResolvedValue(undefined) }));
vi.mock('../services/progressRepository', () => ({ getProgressDocument: mocks.progressDoc, progressNeedsOnboarding: () => true }));
vi.mock('../components/gc/gcNotifications', () => ({ generateAutoNotifications: vi.fn().mockResolvedValue(undefined) }));
vi.mock('../utils/adminIdentity', () => ({ isVerifiedAdminSession: () => false }));
vi.mock('../utils/sessionPrivacy', () => ({ clearLocalSessionData: vi.fn().mockResolvedValue(undefined) }));
vi.mock('../utils/logError', () => ({ logError: vi.fn() }));

const firebaseUser = { uid: 'new-student', displayName: 'Aoife', getIdTokenResult: async () => ({ claims: {} }) };
const choice = { uid: 'new-student', name: 'Aoife Byrne', avatar: 'star-crew:maker', school: 'mountcarmel', role: 'student' as const };
const wrapper = ({ children }: { children: React.ReactNode }) => <AuthProvider>{children}</AuthProvider>;

beforeEach(() => {
  mocks.userDoc.mockReset();
  mocks.progressDoc.mockReset().mockResolvedValue(null);
});

describe('signup avatar handoff', () => {
  it.each([
    ['school-only registration stub', { school: 'mountcarmel', curriculumLevel: 'senior' }],
    ['stale legacy profile', { name: 'Student', avatar: 'Charlie', school: 'mountcarmel', curriculumLevel: 'senior' }],
    ['missing profile', null],
  ])('preserves the chosen name and character when a %s resolves late', async (_label, profile) => {
    let resolve!: (value: unknown) => void;
    mocks.userDoc.mockReturnValue(new Promise(done => { resolve = done; }));
    const view = renderHook(() => useAuth(), { wrapper });
    let loading!: Promise<void>;
    await act(async () => { loading = mocks.listener!(firebaseUser); });
    act(() => view.result.current.handleLoginSuccess(choice, { requiresOnboarding: true }));
    await act(async () => { resolve(profile); await loading; });
    expect(view.result.current.user).toMatchObject({ uid: choice.uid, name: choice.name, avatar: choice.avatar });
  });

  it('uses the stored profile avatar on a normal returning-user login', async () => {
    mocks.userDoc.mockResolvedValue({ name: 'Aoife', avatar: 'star-crew:reader', curriculumLevel: 'senior' });
    const view = renderHook(() => useAuth(), { wrapper });
    await act(async () => { await mocks.listener!(firebaseUser); });
    expect(view.result.current.user?.avatar).toBe('star-crew:reader');
  });

  it('preserves only cosmetic identity from the handoff, not privileged fields', async () => {
    let resolve!: (value: unknown) => void;
    mocks.userDoc.mockReturnValue(new Promise(done => { resolve = done; }));
    const view = renderHook(() => useAuth(), { wrapper });
    let loading!: Promise<void>;
    await act(async () => { loading = mocks.listener!(firebaseUser); });
    act(() => view.result.current.handleLoginSuccess({ ...choice, role: 'gc', school: 'pwc', isAdmin: true }));
    await act(async () => { resolve({ role: 'student', school: 'mountcarmel', curriculumLevel: 'senior' }); await loading; });
    expect(view.result.current.user).toMatchObject({ avatar: choice.avatar, role: 'student', school: 'mountcarmel', isAdmin: false });
  });
});
