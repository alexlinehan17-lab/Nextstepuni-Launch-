import { StrictMode, useCallback, useState } from 'react';
import { act, renderHook, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { useSettings } from '../hooks/useSettings';
import { DEMO_STUDENT_UID } from '../data/devStudent';

const mocks = vi.hoisted(() => ({ getDoc: vi.fn(), setDoc: vi.fn() }));
vi.mock('firebase/firestore', () => ({
  doc: (_db: unknown, collection: string, uid: string) => `${collection}/${uid}`,
  getDoc: mocks.getDoc,
  setDoc: mocks.setDoc,
}));
const savedSettings = (data: Record<string, unknown> = {}) => ({ exists: () => true, data: () => data });
function deferred<T>() {
  let resolve!: (value: T) => void;
  const promise = new Promise<T>(done => { resolve = done; });
  return { promise, resolve };
}

beforeEach(() => {
  localStorage.clear();
  mocks.getDoc.mockReset().mockResolvedValue({ exists: () => false });
  mocks.setDoc.mockReset().mockResolvedValue(undefined);
});

describe('Star Crew identity after signup', () => {
  it('uses the signup character instead of the previous account’s cached avatar', async () => {
    localStorage.setItem('nextstep-settings', JSON.stringify({ avatar: 'Maya Angelou', language: 'en' }));
    const view = renderHook(() => useSettings('new-student', 'star-crew:maker'));
    expect(view.result.current.settings.avatar).toBe('star-crew:maker');
    await waitFor(() => expect(view.result.current.isLoaded).toBe(true));
    expect(view.result.current.settings.avatar).toBe('star-crew:maker');
  });

  it('replaces an auth fallback when the chosen signup character arrives', async () => {
    const pending = deferred<ReturnType<typeof savedSettings>>();
    mocks.getDoc.mockReturnValue(pending.promise);
    const view = renderHook(({ avatar }) => useSettings('student', avatar), { initialProps: { avatar: 'Charlie' } });
    view.rerender({ avatar: 'star-crew:reader' });
    await act(async () => pending.resolve(savedSettings({ avatar: 'Charlie', darkMode: true })));
    expect(view.result.current.settings).toMatchObject({ avatar: 'star-crew:reader', darkMode: true });
  });

  it('keeps the saved profile character on reload even if settings contain an old avatar', async () => {
    localStorage.setItem('nextstep-settings:student', JSON.stringify({ avatar: 'James' }));
    mocks.getDoc.mockResolvedValue(savedSettings({ avatar: 'James', defaultWorkMinutes: 45 }));
    const view = renderHook(() => useSettings('student', 'star-crew:skater'));
    await waitFor(() => expect(view.result.current.isLoaded).toBe(true));
    expect(view.result.current.settings).toMatchObject({ avatar: 'star-crew:skater', defaultWorkMinutes: 45 });
    act(() => view.result.current.updateSetting('darkMode', true));
    expect(mocks.setDoc).toHaveBeenCalledWith('settings/student', expect.objectContaining({ avatar: 'star-crew:skater' }), { merge: true });
    expect(mocks.setDoc).not.toHaveBeenCalledWith('users/student', expect.anything(), expect.anything());
  });

  it('updates the live profile immediately and keeps a new choice when an older read finishes', async () => {
    const pending = deferred<ReturnType<typeof savedSettings>>();
    mocks.getDoc.mockReturnValue(pending.promise);
    const view = renderHook(() => {
      const [profileAvatar, setProfileAvatar] = useState('star-crew:beanie');
      const onAvatarChange = useCallback((avatar: string) => setProfileAvatar(avatar), []);
      return { profileAvatar, ...useSettings('student', profileAvatar, onAvatarChange) };
    }, { wrapper: StrictMode });
    act(() => view.result.current.updateSetting('avatar', 'star-crew:musician'));
    expect(view.result.current.profileAvatar).toBe('star-crew:musician');
    await act(async () => pending.resolve(savedSettings({ avatar: 'star-crew:beanie' })));
    expect(view.result.current.settings.avatar).toBe('star-crew:musician');
    expect(mocks.setDoc.mock.calls.filter(([path]) => path === 'users/student')).toEqual([
      ['users/student', { avatar: 'star-crew:musician' }, { merge: true }],
    ]);
  });

  it('does not let the previous account’s delayed settings overwrite the next student', async () => {
    const first = deferred<ReturnType<typeof savedSettings>>();
    const second = deferred<ReturnType<typeof savedSettings>>();
    mocks.getDoc.mockImplementation((path: string) => path === 'settings/first' ? first.promise : second.promise);
    const view = renderHook(({ uid, avatar }) => useSettings(uid, avatar), {
      initialProps: { uid: 'first', avatar: 'star-crew:maker' },
    });
    act(() => view.result.current.updateSetting('avatar', 'star-crew:hugger'));
    view.rerender({ uid: 'second', avatar: 'star-crew:snoozer' });
    expect(view.result.current.settings.avatar).toBe('star-crew:snoozer');
    await act(async () => first.resolve(savedSettings({ avatar: 'James' })));
    await act(async () => second.resolve(savedSettings({ avatar: 'Charlie' })));
    expect(view.result.current.settings.avatar).toBe('star-crew:snoozer');
    expect(JSON.parse(localStorage.getItem('nextstep-settings:first')!).avatar).toBe('star-crew:hugger');
    expect(JSON.parse(localStorage.getItem('nextstep-settings:second')!).avatar).toBe('star-crew:snoozer');
  });

  it('does not display an account avatar after sign-out', () => {
    const view = renderHook(({ uid, avatar }: { uid?: string; avatar?: string }) => useSettings(uid, avatar), {
      initialProps: { uid: 'student', avatar: 'star-crew:maker' },
    });
    view.rerender({ uid: undefined, avatar: undefined });
    expect(view.result.current.settings.avatar).toBe('');
  });

  it('keeps demo character choices local and reloadable', () => {
    const patchProfile = vi.fn();
    const first = renderHook(() => useSettings(DEMO_STUDENT_UID, 'Maya Angelou', patchProfile));
    act(() => first.result.current.updateSetting('avatar', 'star-crew:maker'));
    expect(patchProfile).toHaveBeenCalledWith('star-crew:maker');
    first.unmount();
    const second = renderHook(() => useSettings(DEMO_STUDENT_UID, 'Maya Angelou'));
    expect(second.result.current.settings.avatar).toBe('star-crew:maker');
    expect(mocks.getDoc).not.toHaveBeenCalled();
    expect(mocks.setDoc).not.toHaveBeenCalled();
  });
});
