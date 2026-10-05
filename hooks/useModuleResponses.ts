/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useEffect, useCallback, useMemo, useSyncExternalStore } from 'react';
import { auth } from '../firebase';
import { useAuth } from '../contexts/AuthContext';
import { changeModuleResponse, flushModuleResponses, loadModuleResponses, moduleResponseEntry, subscribeModuleResponses } from '../services/moduleResponseStore';

export function useModuleResponses(moduleId: string) {
  const { user } = useAuth();
  const uid = user?.uid ?? auth.currentUser?.uid ?? null;
  const namespace = RESPONSE_NAMESPACES[moduleId] ?? moduleId;
  const entry = useMemo(() => moduleResponseEntry(uid, namespace), [uid, namespace]);
  const subscribe = useCallback((listener: () => void) => subscribeModuleResponses(entry, listener), [entry]);
  const snapshot = useSyncExternalStore(subscribe, () => entry.snapshot);

  useEffect(() => {
    void loadModuleResponses(entry);
    const flush = () => { void flushModuleResponses(entry); };
    window.addEventListener('pagehide', flush);
    window.addEventListener('online', flush);
    return () => { window.removeEventListener('pagehide', flush); window.removeEventListener('online', flush); flush(); };
  }, [entry]);
  const saveResponse = useCallback((key: string, value: any) => changeModuleResponse(entry, key, value), [entry]);
  return { responses: snapshot.values, saveResponse, isLoaded: snapshot.loaded, saveStatus: snapshot.status, retrySave: async () => { await loadModuleResponses(entry, true); await flushModuleResponses(entry); } };
}

// Preserve response namespaces used by historical accounts. Curriculum and
// navigation continue to use their existing canonical module IDs.
const RESPONSE_NAMESPACES: Record<string, string> = {
  'agency-architecture-protocol': 'controlling-the-controllables',
  'best-possible-self-protocol': 'best-possible-self',
  'affirming-values-protocol': 'affirming-values',
  'linking-study-future-goals-protocol': 'linking-study-future-goals',
  'points-optimization-protocol': 'the-625-blueprint',
};
