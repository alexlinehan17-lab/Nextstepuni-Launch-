/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import { doc, setDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { reportSaveError } from '../utils/logError';
import { useFreshProgress } from './useFreshProgress';
import { type UnifiedMockResult } from '../types';
import { mockResultsStoragePatch, reconcileMockResults } from '../services/mockResultsRepository';

export function useMockResults(uid: string | undefined) {
  const { doc: rawProgressDoc, loaded: progressLoaded } = useFreshProgress(uid);
  const [mocks, setMocks] = useState<UnifiedMockResult[]>([]);
  const mocksRef = useRef<UnifiedMockResult[]>([]);
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    if (!progressLoaded) return;
    if (!uid) { mocksRef.current = []; setMocks([]); setIsLoaded(true); return; }

    const reconciled = reconcileMockResults(rawProgressDoc);
    mocksRef.current = reconciled;
    setMocks(reconciled);
    const canonical = rawProgressDoc?.unifiedMockResults ?? [];
    if (reconciled.length > 0 && JSON.stringify(canonical) !== JSON.stringify(reconciled)) {
      setDoc(doc(db, 'progress', uid), mockResultsStoragePatch(reconciled), { merge: true })
        .catch((e) => reportSaveError('useMockResults.migrate', e));
    }
    setIsLoaded(true);
  }, [uid, progressLoaded, rawProgressDoc]);

  const addMockResult = useCallback((mock: Omit<UnifiedMockResult, 'id' | 'timestamp'>) => {
    if (!uid) return;
    const newMock: UnifiedMockResult = {
      ...mock,
      id: Date.now().toString(36) + Math.random().toString(36).slice(2, 8),
      timestamp: Date.now(),
    };
    const next = [newMock, ...mocksRef.current];
    mocksRef.current = next;
    setMocks(next);
    setDoc(doc(db, 'progress', uid), mockResultsStoragePatch(next), { merge: true }).catch((e) => reportSaveError('useMockResults.save', e));
  }, [uid]);

  const removeMockResult = useCallback((id: string) => {
    if (!uid) return;
    const next = mocksRef.current.filter(m => m.id !== id);
    mocksRef.current = next;
    setMocks(next);
    setDoc(doc(db, 'progress', uid), mockResultsStoragePatch(next), { merge: true }).catch((e) => reportSaveError('useMockResults.save', e));
  }, [uid]);

  const getLatestBySubject = useCallback((subjectName: string) => {
    for (const mock of mocks) {
      const entry = mock.entries.find(e => e.subjectName === subjectName);
      if (entry) return { mock, entry };
    }
    return null;
  }, [mocks]);

  return { mocks, isLoaded, addMockResult, removeMockResult, getLatestBySubject };
}
