import { useEffect, useSyncExternalStore } from 'react';
import type { useStudySession } from './useStudySession';
import { getStudyFocusSnapshot, subscribeStudyFocus, studyFocusDeadline, syncStudyFocus } from '../services/studyFocus';

export const useStudyFocus = () => useSyncExternalStore(subscribeStudyFocus, getStudyFocusSnapshot, getStudyFocusSnapshot);

/** Lives in the account-scoped session engine, never in a timer screen. */
export function useStudyFocusSession(session: ReturnType<typeof useStudySession>, uid: string | undefined, identityReady = true) {
  const deadline = studyFocusDeadline(session);
  useEffect(() => {
    if (!identityReady) return;
    void syncStudyFocus(uid, deadline);
    const refresh = () => { if (document.visibilityState === 'visible') void syncStudyFocus(uid, deadline); };
    document.addEventListener('visibilitychange', refresh);
    return () => document.removeEventListener('visibilitychange', refresh);
  }, [uid, deadline, identityReady]);
  useEffect(() => () => { if (identityReady) void syncStudyFocus(undefined, null); }, [uid, identityReady]);
}
