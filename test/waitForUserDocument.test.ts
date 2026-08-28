/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * waitForUserDocument gates the whole post-signup screen: AuthContext only
 * publishes loadedDataUid once it resolves, and AppRouter will not render
 * onboarding until that happens. So how it waits is a user-visible latency
 * decision, not an implementation detail.
 *
 * The version this replaced polled three times, 250ms apart. Registration
 * writes users/{uid} after the join-code callable and a token refresh, so on a
 * signup the write landed AFTER the last attempt was spent: every registration
 * paid the full ~1.1s budget and still returned null. These tests pin the two
 * properties that stops it coming back — an existing document costs exactly one
 * read, and a document that appears mid-wait resolves when it appears rather
 * than on a poll boundary.
 */
import { describe, it, expect, vi, beforeEach } from 'vitest';

type Snap = { exists: () => boolean; data: () => unknown };
type Listener = (snap: Snap) => void;

const missing: Snap = { exists: () => false, data: () => undefined };
const present = (data: unknown): Snap => ({ exists: () => true, data: () => data });

let getDocCalls = 0;
let getDocResult: Snap = missing;
let listeners: Listener[] = [];
let unsubscribes = 0;

vi.mock('firebase/firestore', () => ({
  doc: (_db: unknown, ...path: string[]) => ({ path: path.join('/') }),
  getDoc: async () => { getDocCalls++; return getDocResult; },
  setDoc: async () => undefined,
  onSnapshot: (_ref: unknown, next: Listener) => {
    listeners.push(next);
    return () => { unsubscribes++; };
  },
}));
vi.mock('../firebase', () => ({ db: {} }));

const { waitForUserDocument } = await import('../services/userRepository');

/** Let the initial getDoc settle so the listener is attached. Microtasks only —
 *  the deadline tests run on fake timers, so this must not await a timer. */
async function untilListening(): Promise<void> {
  for (let i = 0; i < 20 && listeners.length === 0; i++) await Promise.resolve();
  if (listeners.length === 0) throw new Error('listener was never attached');
}

beforeEach(() => {
  getDocCalls = 0;
  getDocResult = missing;
  listeners = [];
  unsubscribes = 0;
});

describe('waitForUserDocument', () => {
  it('costs one read and no listener when the document already exists', async () => {
    getDocResult = present({ name: 'Aoife' });

    await expect(waitForUserDocument('uid')).resolves.toEqual({ name: 'Aoife' });

    // The ordinary sign-in path is the common case and must not have got slower.
    expect(getDocCalls).toBe(1);
    expect(listeners).toHaveLength(0);
  });

  it('resolves with the real document the moment a later write lands', async () => {
    const pending = waitForUserDocument('uid');
    await untilListening();
    expect(listeners).toHaveLength(1);

    // The registration write arrives after the first read missed. Under the old
    // poll this instant fell between attempts and, if late enough, after the
    // last one — returning null for an account that plainly had a document.
    listeners[0](present({ name: 'Aoife', avatar: 'Milo' }));

    await expect(pending).resolves.toEqual({ name: 'Aoife', avatar: 'Milo' });
    expect(unsubscribes).toBe(1);
  });

  it('ignores a snapshot that says the document is still absent', async () => {
    vi.useFakeTimers();
    try {
      const pending = waitForUserDocument('uid', { timeoutMs: 500 });
      await untilListening();

      listeners[0](missing);          // still not written
      listeners[0](missing);          // still not written

      vi.advanceTimersByTime(500);
      await expect(pending).resolves.toBeNull();
    } finally {
      vi.useRealTimers();
    }
  });

  it('gives up after the deadline so a document-less account still gets a session', async () => {
    vi.useFakeTimers();
    try {
      const pending = waitForUserDocument('uid', { timeoutMs: 1200 });
      await untilListening();

      vi.advanceTimersByTime(1199);
      let settled = false;
      void pending.then(() => { settled = true; });
      await Promise.resolve();
      expect(settled).toBe(false);

      vi.advanceTimersByTime(1);
      await expect(pending).resolves.toBeNull();
      expect(unsubscribes).toBe(1);
    } finally {
      vi.useRealTimers();
    }
  });

  it('does not resolve twice when the document arrives as the deadline fires', async () => {
    vi.useFakeTimers();
    try {
      const pending = waitForUserDocument('uid', { timeoutMs: 100 });
      await untilListening();

      vi.advanceTimersByTime(100);
      listeners[0](present({ name: 'Late' }));   // must be ignored, already settled

      await expect(pending).resolves.toBeNull();
      expect(unsubscribes).toBe(1);
    } finally {
      vi.useRealTimers();
    }
  });
});
