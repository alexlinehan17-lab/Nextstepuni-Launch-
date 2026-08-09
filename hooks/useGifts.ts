/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import { collection, query, where, orderBy, limit, getDocs, writeBatch, doc, serverTimestamp, Timestamp, increment } from 'firebase/firestore';
import { db } from '../firebase';
import { saveInBackground, awaitWriteOrTimeout } from '../utils/firestoreWrite';
import { type ShopItem } from '../types';
import { SHOP_CATALOG } from '../islandShopData';
import { getJourneyV2BasePrice } from '../journeyEconomyConfig';
import { firstName } from '../utils/firstName';

/** Max price for giftable items */
const GIFT_MAX_PRICE = 50;

/** Items eligible to be gifted: decorations ≤50pts, not exclusive */
export const GIFTABLE_ITEMS: ShopItem[] = SHOP_CATALOG.filter(
  i => i.type === 'decoration' && getJourneyV2BasePrice(i) <= GIFT_MAX_PRICE && !i.exclusiveTo
);

export interface PendingGift {
  id: string;
  fromName: string;
  itemId: string;
  itemName: string;
  createdAt: Date;
}

export function useGifts(uid?: string) {
  const [pendingGifts, setPendingGifts] = useState<PendingGift[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const isMountedRef = useRef(true);
  useEffect(() => () => { isMountedRef.current = false; }, []);

  // Load pending gifts for this user
  useEffect(() => {
    if (!uid) return;
    let cancelled = false;

    (async () => {
      setIsLoading(true);
      try {
        const q = query(
          collection(db, 'gifts'),
          where('toUid', '==', uid),
          where('status', '==', 'pending'),
          orderBy('createdAt', 'desc'),
          limit(10),
        );
        const snap = await getDocs(q);
        if (cancelled) return;

        setPendingGifts(snap.docs.map(d => {
          const data = d.data();
          const item = SHOP_CATALOG.find(i => i.id === data.itemId);
          return {
            id: d.id,
            fromName: data.fromName || 'Someone',
            itemId: data.itemId,
            itemName: item?.name ?? 'Gift',
            createdAt: (data.createdAt as Timestamp)?.toDate?.() ?? new Date(),
          };
        }));
      } catch (err) {
        console.error('[useGifts] Failed to load gifts:', err);
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    })();

    return () => { cancelled = true; };
  }, [uid]);

  // Check if sender has already sent a gift today
  const canSendGiftToday = useCallback(async (): Promise<boolean> => {
    if (!uid) return false;
    try {
      const startOfDay = new Date();
      startOfDay.setHours(0, 0, 0, 0);

      const q = query(
        collection(db, 'gifts'),
        where('fromUid', '==', uid),
        where('createdAt', '>=', Timestamp.fromDate(startOfDay)),
        limit(1),
      );
      const snap = await getDocs(q);
      return snap.empty;
    } catch (err) {
      console.error('[useGifts] Failed to check gift eligibility:', err);
      return true;
    }
  }, [uid]);

  // Send a gift to a peer (atomic: create gift doc + deduct points)
  const sendGift = useCallback(async (
    toUid: string,
    school: string,
    item: ShopItem,
    fromName: string,
  ): Promise<boolean> => {
    if (!uid) return false;
    try {
      const batch = writeBatch(db);

      const giftRef = doc(collection(db, 'gifts'));
      batch.set(giftRef, {
        fromUid: uid,
        // Peers see first name only (data minimisation, 2026-07-18).
        fromName: firstName(fromName),
        toUid,
        school,
        itemId: item.id,
        status: 'pending',
        createdAt: serverTimestamp(),
      });

      // Deduct points from sender
      const progressRef = doc(db, 'progress', uid);
      batch.update(progressRef, {
        'pointsData.totalSpent': increment(getJourneyV2BasePrice(item)),
      });

      // Bounded wait — see useKudos.sendKudos. A queued batch still reaches the
      // recipient on reconnect, so only an outright rejection is a failure.
      const outcome = await awaitWriteOrTimeout(batch.commit(), 'useGifts.sendGift');
      return outcome !== 'failed';
    } catch (err) {
      console.error('[useGifts] Failed to send gift:', err);
      return false;
    }
  }, [uid]);

  // Mark a gift as placed
  const markGiftPlaced = useCallback(async (giftId: string): Promise<void> => {
    const batch = writeBatch(db);
    batch.update(doc(db, 'gifts', giftId), { status: 'placed' });
    // Remove from the pending list immediately; batch.commit() has the same
    // server-ack semantics as any other write, so awaiting it meant the gift
    // stayed stuck in "pending" offline and the student could place it twice.
    const removed = giftId;
    if (isMountedRef.current) setPendingGifts(prev => prev.filter(g => g.id !== removed));
    saveInBackground(
      batch.commit(),
      'useGifts.markGiftPlaced',
      undefined,
      { silent: true },
    );
  }, []);

  return { pendingGifts, isLoading, canSendGiftToday, sendGift, markGiftPlaced, GIFTABLE_ITEMS };
}
