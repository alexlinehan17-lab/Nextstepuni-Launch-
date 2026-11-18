/** Optional iOS Screen Time shielding. Tokens and choices never cross this bridge. */
import { Capacitor, registerPlugin } from '@capacitor/core';
import type { StudyTimerSnapshot } from './studyTimerAlerts';

export interface StudyFocusStatus {
  available: boolean;
  authorized: boolean;
  enabled: boolean;
  active: boolean;
  selectionCount: number;
}
export interface StudyFocusSnapshot extends StudyFocusStatus { busy: boolean; error: string | null }
interface FocusPlugin {
  sync(options: { owner: string | null; deadline: number | null }): Promise<StudyFocusStatus>;
  configure(options: { owner: string }): Promise<StudyFocusStatus>;
  setEnabled(options: { owner: string; enabled: boolean }): Promise<StudyFocusStatus>;
}
const native = registerPlugin<FocusPlugin>('StudyFocus');
const EMPTY: StudyFocusSnapshot = { available: false, authorized: false, enabled: false, active: false, selectionCount: 0, busy: false, error: null };
let snapshot = EMPTY;
let owner: string | null = null;
let deadline: number | null = null;
let revision = 0;
let ownerEpoch = 0;
let queue: Promise<void> = Promise.resolve();
const listeners = new Set<() => void>();
export const getStudyFocusSnapshot = () => snapshot;
export const subscribeStudyFocus = (listener: () => void) => { listeners.add(listener); return () => { listeners.delete(listener); }; };
const publish = (next: StudyFocusSnapshot) => { snapshot = next; listeners.forEach(listener => listener()); };
const supported = () => Capacitor.getPlatform() === 'ios' && Capacitor.isPluginAvailable?.('StudyFocus');

/** The stopwatch's four-hour limit and countdown use the timer's own clock. */
export function studyFocusDeadline(session: Pick<StudyTimerSnapshot, 'phase' | 'openEnded' | 'startedAt' | 'totalDuration' | 'endsAt'>): number | null {
  if (session.phase !== 'active') return null;
  return session.openEnded ? session.startedAt + session.totalDuration * 1000 : session.endsAt;
}

function syncCurrent(): Promise<void> {
  const requestedOwner = owner;
  const requestedDeadline = deadline;
  const requestedRevision = revision;
  const run = queue.then(async () => {
    // Coalesce stale ticks, account changes and pause/resume requests.
    if (requestedRevision !== revision || !supported()) return;
    try {
      const status = await native.sync({ owner: requestedOwner, deadline: requestedDeadline });
      if (requestedRevision === revision) publish({ ...snapshot, ...status, error: null });
    } catch {
      if (requestedRevision === revision) publish({ ...snapshot, active: false, error: 'Could not confirm app blocking. Pause the timer and try again.' });
    }
  });
  queue = run;
  return run;
}

export function syncStudyFocus(uid: string | undefined, nextDeadline: number | null): Promise<void> {
  const nextOwner = uid ?? null;
  if (nextOwner !== owner) { ownerEpoch++; publish(EMPTY); }
  owner = nextOwner;
  deadline = nextDeadline;
  revision++;
  if (!supported()) { publish(EMPTY); return Promise.resolve(); }
  return syncCurrent();
}

/** Prompt/picker calls deliberately do not occupy the sync queue: sign-out must release immediately. */
export async function configureStudyFocus(): Promise<void> {
  const requestedOwner = owner;
  const requestedEpoch = ownerEpoch;
  if (!requestedOwner || !supported() || snapshot.busy) return;
  publish({ ...snapshot, busy: true, error: null });
  try {
    await queue;
    if (requestedOwner !== owner || requestedEpoch !== ownerEpoch) return;
    const status = await native.configure({ owner: requestedOwner });
    if (requestedOwner === owner && requestedEpoch === ownerEpoch) {
      publish({ ...status, busy: false, error: null });
      await syncCurrent();
    }
  } catch {
    if (requestedOwner === owner && requestedEpoch === ownerEpoch) publish({ ...snapshot, busy: false, error: 'App blocking was not enabled. Allow Screen Time access and choose apps to try again.' });
  }
}

export async function setStudyFocusEnabled(enabled: boolean): Promise<void> {
  const requestedOwner = owner;
  const requestedEpoch = ownerEpoch;
  if (!requestedOwner || !supported() || snapshot.busy) return;
  if (enabled && (!snapshot.authorized || !snapshot.selectionCount)) return configureStudyFocus();
  publish({ ...snapshot, busy: true, error: null });
  let changed = false;
  const run = queue.then(async () => {
    if (requestedOwner !== owner || requestedEpoch !== ownerEpoch) return;
    try {
      const status = await native.setEnabled({ owner: requestedOwner, enabled });
      changed = true;
      if (requestedOwner === owner && requestedEpoch === ownerEpoch) publish({ ...status, busy: false, error: null });
    } catch {
      if (requestedOwner === owner && requestedEpoch === ownerEpoch) publish({ ...snapshot, busy: false, error: 'Could not change app blocking. Pause the timer and try again.' });
    }
  });
  queue = run;
  await run;
  if (changed && requestedOwner === owner && requestedEpoch === ownerEpoch) await syncCurrent();
}

if (typeof window !== 'undefined') {
  window.addEventListener('nextstepuni:session-cleared', () => { void syncStudyFocus(undefined, null); });
}
