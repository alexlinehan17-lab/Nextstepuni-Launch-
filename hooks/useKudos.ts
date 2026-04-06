/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect, useCallback } from 'react';
import { collection, query, where, orderBy, limit, getDocs, addDoc, serverTimestamp, Timestamp } from 'firebase/firestore';
import { db } from '../firebase';
import { KUDOS_MESSAGES } from '../kudosData';

export interface ReceivedKudos {
  messageId: string;
  fromName: string;
  createdAt: Date;
}

export function useKudos(uid?: string) {
  const [kudosCount, setKudosCount] = useState(0);
  const [recentKudos, setRecentKudos] = useState<ReceivedKudos[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  // Load kudos received by this user
  useEffect(() => {
    if (!uid) return;
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
        console.error('[useKudos] Failed to load kudos:');
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    })();

    return () => { cancelled = true; };
  }, [uid]);

  // Check if we already sent kudos to this peer today
  const canSendKudosTo = useCallback(async (targetUid: string): Promise<boolean> => {
    if (!uid) return false;
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
    } catch {
      return true; // Allow on error
    }
  }, [uid]);

  // Send kudos
  const sendKudos = useCallback(async (
    toUid: string,
    school: string,
    messageId: string,
    fromName: string,
  ): Promise<boolean> => {
    if (!uid) return false;
    try {
      await addDoc(collection(db, 'kudos'), {
        fromUid: uid,
        fromName,
        toUid,
        school,
        messageId,
        createdAt: serverTimestamp(),
      });
      return true;
    } catch (err) {
      console.error('[useKudos] Failed to send kudos:');
      return false;
    }
  }, [uid]);

  // Get message text by ID
  const getMessageText = useCallback((messageId: string): string => {
    return KUDOS_MESSAGES.find(m => m.id === messageId)?.text ?? 'Kudos!';
  }, []);

  return { kudosCount, recentKudos, isLoading, canSendKudosTo, sendKudos, getMessageText };
}
