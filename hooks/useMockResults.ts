/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect, useCallback } from 'react';
import { doc, setDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { useProgress } from '../contexts/ProgressContext';
import { type UnifiedMockResult } from '../types';

export function useMockResults(uid: string | undefined) {
  const { rawProgressDoc, progressLoaded } = useProgress();
  const [mocks, setMocks] = useState<UnifiedMockResult[]>([]);
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    if (!progressLoaded) return;
    if (!uid) { setIsLoaded(true); return; }

    const data = rawProgressDoc;

    if (data?.mockResults) {
      setMocks(data.mockResults);
    } else {
      // Migrate from old formats
      const migrated: UnifiedMockResult[] = [];

      // Migrate from PointsPassport
      if (data?.pointsPassport?.mockResults) {
        for (const m of data.pointsPassport.mockResults) {
          migrated.push({
            id: m.id || `pp-${Date.now()}-${Math.random().toString(36).slice(2,6)}`,
            label: m.label || 'Mock Exam',
            date: m.date || new Date().toISOString().split('T')[0],
            entries: m.grades || [],
            totalPoints: m.totalPoints || 0,
            timestamp: m.timestamp || Date.now(),
          });
        }
      }

      // Migrate from WarRoom (if not already covered)
      if (data?.warRoom?.mockResults) {
        const existingIds = new Set(migrated.map(m => m.id));
        for (const m of data.warRoom.mockResults) {
          if (!existingIds.has(m.id)) {
            migrated.push({
              id: m.id || `wr-${Date.now()}-${Math.random().toString(36).slice(2,6)}`,
              label: m.label || 'Mock Exam',
              date: m.date || new Date().toISOString().split('T')[0],
              entries: m.grades || [],
              totalPoints: m.totalPoints || 0,
              timestamp: m.timestamp || Date.now(),
            });
          }
        }
      }

      if (migrated.length > 0) {
        migrated.sort((a, b) => b.timestamp - a.timestamp);
        setMocks(migrated);
        setDoc(doc(db, 'progress', uid), { mockResults: migrated }, { merge: true }).catch(() => {});
      }
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
    let next: UnifiedMockResult[];
    setMocks(prev => { next = [newMock, ...prev]; return next; });
    setDoc(doc(db, 'progress', uid), { mockResults: next! }, { merge: true }).catch(() => {});
  }, [uid]);

  const removeMockResult = useCallback((id: string) => {
    if (!uid) return;
    let next: UnifiedMockResult[];
    setMocks(prev => { next = prev.filter(m => m.id !== id); return next; });
    setDoc(doc(db, 'progress', uid), { mockResults: next! }, { merge: true }).catch(() => {});
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
