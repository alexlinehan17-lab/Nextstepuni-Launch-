/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect, useCallback } from 'react';
import { collection, query, where, orderBy, limit, getDocs, Timestamp } from 'firebase/firestore';
import { getFunctions, httpsCallable } from 'firebase/functions';
import app, { db } from '../firebase';
import { KUDOS_MESSAGES } from '../kudosData';
import { DEMO_STUDENT_UID } from '../data/devStudent';

export interface ReceivedKudos {
  messageId: string;
  fromName: string;
  createdAt: Date;
}

export function useKudos(uid?: string) {
  const isDemo = uid === DEMO_STUDENT_UID;
  const [kudosCount, setKudosCount] = useState(0);
  const [recentKudos, setRecentKudos] = useState<ReceivedKudos[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  // Load kudos received by this user
  useEffect(() => {
    if (!uid || isDemo) {
      setKudosCount(0);
      setRecentKudos([]);
      setIsLoading(false);
      return;
    }
    let cancelled = false;

    (async () => {
      setIsLoading(true);
      try {
        const q = query(
          collection(db, 'kudos'),
          where('toUid', '==', uid),
          orderBy('createdAt', 'desc'),
          limit(50),
        );
        const snap = await getDocs(q);
        if (cancelled) return;

        setKudosCount(snap.size);
        setRecentKudos(snap.docs.slice(0, 5).map(d => {
          const data = d.data();
          return {
            messageId: data.messageId,
            fromName: data.fromName || 'Someone',
            createdAt: (data.createdAt as Timestamp)?.toDate?.() ?? new Date(),
          };
        }));
      } catch (err) {
        console.error('[useKudos] Failed to load kudos:', err);
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    })();

    return () => { cancelled = true; };
  }, [uid, isDemo]);

  // Check if we already sent kudos to this peer today
  const canSendKudosTo = useCallback(async (targetUid: string): Promise<boolean> => {
    if (!uid || isDemo) return false;
    try {
      const startOfDay = new Date();
      startOfDay.setHours(0, 0, 0, 0);

      const q = query(
        collection(db, 'kudos'),
        where('fromUid', '==', uid),
        where('toUid', '==', targetUid),
        where('createdAt', '>=', Timestamp.fromDate(startOfDay)),
        limit(1),
      );
      const snap = await getDocs(q);
      return snap.empty;
    } catch (err) {
      console.error('[useKudos] Failed to check kudos eligibility:', err);
      return false;
    }
  }, [uid, isDemo]);

  // Send kudos
  const sendKudos = useCallback(async (
    toUid: string,
    _school: string,
    messageId: string,
    _fromName: string,
  ): Promise<boolean> => {
    if (!uid || isDemo) return false;
    try {
      const send = httpsCallable<{ toUid: string; messageId: string }, { success: boolean }>(
        getFunctions(app),
        'sendKudos',
      );
      await send({ toUid, messageId });
      return true;
    } catch (err) {
      console.error('[useKudos] Failed to send kudos:', err);
      return false;
    }
  }, [uid, isDemo]);

  // Get message text by ID
  const getMessageText = useCallback((messageId: string): string => {
    return KUDOS_MESSAGES.find(m => m.id === messageId)?.text ?? 'Kudos!';
  }, []);

  return { kudosCount, recentKudos, isLoading, canSendKudosTo, sendKudos, getMessageText };
}
