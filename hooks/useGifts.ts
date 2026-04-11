/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import { collection, query, where, orderBy, limit, getDocs, writeBatch, doc, serverTimestamp, Timestamp, increment } from 'firebase/firestore';
import { db } from '../firebase';
import { ShopItem } from '../types';
import { SHOP_CATALOG } from '../islandShopData';

/** Max price for giftable items */
const GIFT_MAX_PRICE = 50;

/** Items eligible to be gifted: decorations ≤50pts, not exclusive */
export const GIFTABLE_ITEMS: ShopItem[] = SHOP_CATALOG.filter(
  i => i.type === 'decoration' && i.price <= GIFT_MAX_PRICE && !i.exclusiveTo
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
      } catch {
        console.error('[useGifts] Failed to load gifts:');
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
    } catch {
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
        fromName,
        toUid,
        school,
        itemId: item.id,
        status: 'pending',
        createdAt: serverTimestamp(),
      });

      // Deduct points from sender
      const progressRef = doc(db, 'progress', uid);
      batch.update(progressRef, {
        'pointsData.totalSpent': increment(item.price),
      });

      await batch.commit();
      return true;
    } catch {
      console.error('[useGifts] Failed to send gift:');
      return false;
    }
  }, [uid]);

  // Mark a gift as placed
  const markGiftPlaced = useCallback(async (giftId: string): Promise<void> => {
    try {
      const batch = writeBatch(db);
      batch.update(doc(db, 'gifts', giftId), { status: 'placed' });
      await batch.commit();
      if (isMountedRef.current) setPendingGifts(prev => prev.filter(g => g.id !== giftId));
    } catch (err) {
      console.error('[useGifts] Failed to mark gift placed:', err);
    }
  }, []);

  return { pendingGifts, isLoading, canSendGiftToday, sendGift, markGiftPlaced, GIFTABLE_ITEMS };
}
