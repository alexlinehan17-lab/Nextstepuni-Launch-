import { beforeEach, describe, expect, it, vi } from 'vitest';

const state = vi.hoisted(() => ({
  native: false,
  docs: new Map<string, { items: unknown[]; [key: string]: unknown }>(),
  reads: [] as string[],
  failBrowserRead: false,
}));
vi.mock('../firebase', () => ({ db: {} }));
vi.mock('@capacitor/core', () => ({ Capacitor: { isNativePlatform: () => state.native } }));
vi.mock('../utils/firestoreWrite', () => ({ awaitWriteOrTimeout: (promise: Promise<unknown>) => promise }));
vi.mock('firebase/firestore', () => {
  const get = async (path: string) => {
    state.reads.push(path);
    if (state.failBrowserRead && path.startsWith('browserNotifications/')) throw Error('Unavailable');
    return { exists: () => state.docs.has(path), data: () => state.docs.get(path) };
  };
  return {
    doc: (_db: unknown, collection: string, uid: string) => `${collection}/${uid}`,
    getDoc: get,
    runTransaction: (_db: unknown, callback: (txn: unknown) => unknown) => callback({
      get,
      set: (path: string, data: { items: unknown[] }, options?: { merge: boolean }) => {
        state.docs.set(path, options?.merge ? { ...state.docs.get(path), ...data } : data);
      },
    }),
  };
});
import { getNotifications, markNotificationRead, markAllRead, addNotification } from '../components/gc/gcNotifications';

const campaign = { id: 'roundup', type: 'product-update' as const, title: 'Recent changes', body: 'Ten improvements', timestamp: 20, read: false };
const general = { ...campaign, id: 'general', timestamp: 10 };
beforeEach(() => {
  state.native = false;
  state.failBrowserRead = false;
  state.docs.clear();
  state.reads = [];
  state.docs.set('notifications/student', { items: [general] });
  state.docs.set('browserNotifications/student', { items: [campaign] });
});

describe('Staged browser and app announcements', () => {
  it('shows the browser campaign beside ordinary notifications before app release', async () => {
    expect((await getNotifications('student')).map(n => n.id)).toEqual(['roundup', 'general']);
  });
  it('does not read or display the browser campaign in the native app', async () => {
    state.native = true;
    expect((await getNotifications('student')).map(n => n.id)).toEqual(['general']);
    expect(state.reads).toEqual(['notifications/student']);
    await markAllRead('student');
    expect(state.docs.get('browserNotifications/student')?.items).toEqual([campaign]);
  });
  it('keeps a read browser campaign read and unique when its unread app copy is delivered', async () => {
    await markNotificationRead('student', 'roundup');
    state.docs.set('notifications/student', { items: [campaign, general] });
    expect((await getNotifications('student')).filter(n => n.id === 'roundup')).toEqual([{ ...campaign, read: true }]);
    await markAllRead('student');
    expect(state.docs.get('notifications/student')?.items).toEqual([campaign, { ...general, read: true }]);
    state.native = true;
    expect((await getNotifications('student'))[0]).toEqual(campaign);
    await markNotificationRead('student', 'roundup');
    expect((await getNotifications('student'))[0].read).toBe(true);
  });
  it('keeps a browser campaign when an older app replaces the shared inbox', async () => {
    await markNotificationRead('student', 'roundup');
    state.docs.set('notifications/student', { items: [{ ...general, read: true }] });
    expect((await getNotifications('student'))[0]).toEqual({ ...campaign, read: true });
  });
  it('marks a single ordinary notification without consuming the browser campaign', async () => {
    await markNotificationRead('student', 'general');
    expect((await getNotifications('student')).map(n => [n.id, n.read])).toEqual([['roundup', false], ['general', true]]);
  });
  it('preserves other document fields when generating ordinary notifications', async () => {
    state.docs.set('notifications/student', { items: [general], other: 'preserved' });
    await addNotification('student', { type: 'comeback', title: 'Welcome back', body: 'Ready to study?' });
    expect(state.docs.get('notifications/student')?.other).toBe('preserved');
    expect(state.docs.get('browserNotifications/student')?.items).toEqual([campaign]);
  });
  it('still reads ordinary notifications if the browser route is unavailable', async () => {
    state.failBrowserRead = true;
    const error = vi.spyOn(console, 'error').mockImplementation(() => {});
    expect(await getNotifications('student')).toEqual([general]);
    error.mockRestore();
  });
  it('isolates accounts and handles an empty inbox', async () => {
    expect(await getNotifications('someone-else')).toEqual([]);
    await markAllRead('someone-else');
    expect(state.docs.has('notifications/someone-else')).toBe(false);
  });
});
