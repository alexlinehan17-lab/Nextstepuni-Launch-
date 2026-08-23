/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import { collection, query, where, orderBy, limit, getDocs, Timestamp } from 'firebase/firestore';
import { getFunctions, httpsCallable } from 'firebase/functions';
import app, { db } from '../firebase';
import { type ShopItem } from '../types';
import { SHOP_CATALOG } from '../islandShopData';
import { getJourneyV2BasePrice } from '../journeyEconomyConfig';
import { DEMO_STUDENT_UID } from '../data/devStudent';

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
  const isDemo = uid === DEMO_STUDENT_UID;
  const [pendingGifts, setPendingGifts] = useState<PendingGift[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const isMountedRef = useRef(true);
  useEffect(() => () => { isMountedRef.current = false; }, []);

  // Load pending gifts for this user
  useEffect(() => {
    if (!uid || isDemo) {
      setPendingGifts([]);
      setIsLoading(false);
      return;
    }
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
  }, [uid, isDemo]);

  // Check if sender has already sent a gift today
  const canSendGiftToday = useCallback(async (): Promise<boolean> => {
    if (!uid || isDemo) return false;
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
      return false;
    }
  }, [uid, isDemo]);

  // Send a gift to a peer (atomic: create gift doc + deduct points)
  const sendGift = useCallback(async (
    toUid: string,
    _school: string,
    item: ShopItem,
    _fromName: string,
  ): Promise<boolean> => {
    if (!uid || isDemo) return false;
    try {
      const send = httpsCallable<{ toUid: string; itemId: string }, { success: boolean }>(
        getFunctions(app),
        'sendGift',
      );
      await send({ toUid, itemId: item.id });
      return true;
    } catch (err) {
      console.error('[useGifts] Failed to send gift:', err);
      return false;
    }
  }, [uid, isDemo]);

  // Mark a gift as placed
  const markGiftPlaced = useCallback(async (giftId: string): Promise<void> => {
    if (isDemo) {
      if (isMountedRef.current) setPendingGifts(prev => prev.filter(g => g.id !== giftId));
      return;
    }
    const place = httpsCallable<{ giftId: string }, { success: boolean }>(
      getFunctions(app),
      'placeGift',
    );
    await place({ giftId });
    if (isMountedRef.current) setPendingGifts(prev => prev.filter(g => g.id !== giftId));
  }, [isDemo]);

  return { pendingGifts, isLoading, canSendGiftToday, sendGift, markGiftPlaced, GIFTABLE_ITEMS };
}
