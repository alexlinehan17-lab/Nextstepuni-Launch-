/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect, useCallback, useMemo } from 'react';
import { doc, setDoc, increment } from 'firebase/firestore';
import { db } from '../firebase';
import { useProgress } from '../contexts/ProgressContext';
import { type NorthStar, type IslandState, type IslandPlacement, type ShopItem, type NorthStarCategory } from '../types';
import {
  SHOP_CATALOG, EXCLUSIVE_ITEMS, STARTER_PACKS,
  MILESTONE_REWARDS, type MilestoneReward,
  getEffectivePrice, getUnlockRequirement,
} from '../islandShopData';
import {
  findBestLandPlacement,
  findBuildingPlacement,
  findDecorationPlacement,
} from '../components/journey/hex/hexGeometry';

function isBuilding(model: string): boolean {
  return model.startsWith('building-') || model.startsWith('unit-') || model === 'bridge.glb';
}

export function createStarterState(category: NorthStarCategory): IslandState {
  const pack = STARTER_PACKS[category];
  const now = new Date().toISOString();
  return {
    category,
    placements: pack.placements.map(p => ({ ...p, purchasedAt: now })),
    totalSpent: 0,
    purchaseHistory: [],
    lastPurchaseTimestamp: '',
    claimedRewards: [],
  };
}

export interface EnrichedShopItem extends ShopItem {
  effectivePrice: number;
  isLocked: boolean;
  unlockAt: number | null;
  hasDiscount: boolean;
  originalPrice: number;
}

export interface MilestoneRewardStatus {
  reward: MilestoneReward;
  status: 'locked' | 'claimable' | 'claimed';
}

export function useIslandShop(uid?: string, northStar?: NorthStar | null, completedCount: number = 0) {
  const { rawProgressDoc, progressLoaded } = useProgress();
  const [islandState, setIslandState] = useState<IslandState | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Load island state from context
  useEffect(() => {
    if (!progressLoaded) return;

    if (!uid || !northStar?.category) {
      setIslandState(null);
      setIsLoading(false);
      return;
    }

    const data = rawProgressDoc;
    const stored = data.islandState as IslandState | undefined;
    if (stored && stored.category === northStar.category && stored.purchaseHistory?.length > 0) {
      setIslandState(stored);
    } else {
      // No state or North Star changed — initialize with starter pack
      const starter = createStarterState(northStar.category);
      setIslandState(starter);
      setDoc(doc(db, 'progress', uid), { islandState: starter }, { merge: true }).catch(console.error);
    }
    setIsLoading(false);
  }, [uid, northStar?.category, progressLoaded, rawProgressDoc]);

  // Water color from starter pack
  const waterColor = useMemo(() => {
    if (!northStar?.category) return '#3B9EBF';
    return STARTER_PACKS[northStar.category]?.waterColor ?? '#3B9EBF';
  }, [northStar?.category]);

  const category = northStar?.category ?? null;

  // Available items: full catalog + exclusive, enriched with lock/discount info
  const availableItems: EnrichedShopItem[] = useMemo(() => {
    const raw = !category
      ? SHOP_CATALOG
      : [...SHOP_CATALOG, ...EXCLUSIVE_ITEMS.filter(i => i.exclusiveTo === category)];

    return raw.map(item => {
      const unlockAt = getUnlockRequirement(item, category);
      const isLocked = unlockAt !== null && completedCount < unlockAt;
      const effectivePrice = getEffectivePrice(item, category);
      return {
        ...item,
        effectivePrice,
        isLocked,
        unlockAt,
        hasDiscount: effectivePrice < item.price,
        originalPrice: item.price,
      };
    });
  }, [category, completedCount]);

  // Milestone rewards
  const milestoneRewards: MilestoneRewardStatus[] = useMemo(() => {
    if (!category) return [];
    const rewards = MILESTONE_REWARDS[category] ?? [];
    const claimed = new Set(islandState?.claimedRewards ?? []);
    return rewards.map(reward => {
      let status: 'locked' | 'claimable' | 'claimed';
      if (claimed.has(reward.id)) {
        status = 'claimed';
      } else if (completedCount >= reward.modulesRequired) {
        status = 'claimable';
      } else {
        status = 'locked';
      }
      return { reward, status };
    });
  }, [category, completedCount, islandState?.claimedRewards]);

  // Stats
  const stats = useMemo(() => {
    if (!islandState) return { tileCount: 0, decoCount: 0, totalSpent: 0 };
    const tileCount = islandState.placements.filter(p => p.type === 'hex' && !p.isStarter).length;
    const decoCount = islandState.placements.filter(p => p.type === 'decoration' && !p.isStarter).length;
    return { tileCount, decoCount, totalSpent: islandState.totalSpent };
  }, [islandState]);

  // Check if user already has a specific item
  const hasItem = useCallback((itemId: string): boolean => {
    if (!islandState) return false;
    return islandState.purchaseHistory.includes(itemId);
  }, [islandState]);

  // Place an item on the island (shared by purchase and reward claiming)
  const placeItem = useCallback((item: ShopItem, state: IslandState): IslandPlacement | null => {
    const now = new Date().toISOString();
    if (item.type === 'hex') {
      if (isBuilding(item.model)) {
        const pos = findBuildingPlacement(state.placements);
        if (!pos) return null;
        return { itemId: item.id, model: item.model, type: 'hex', q: pos.q, r: pos.r, purchasedAt: now };
      } else {
        const occupied = new Set<string>();
        for (const p of state.placements) {
          if (p.type === 'hex') occupied.add(`${p.q},${p.r}`);
        }
        const pos = findBestLandPlacement(occupied);
        return { itemId: item.id, model: item.model, type: 'hex', q: pos.q, r: pos.r, purchasedAt: now };
      }
    } else {
      const pos = findDecorationPlacement(state.placements);
      if (!pos) return null;
      return {
        itemId: item.id, model: item.model, type: 'decoration',
        q: pos.q, r: pos.r, scale: item.defaultScale ?? 0.5,
        offsetX: pos.offsetX, offsetZ: pos.offsetZ, purchasedAt: now,
      };
    }
  }, []);

  // Purchase an item
  const purchaseItem = useCallback(async (item: EnrichedShopItem | ShopItem, balance: number): Promise<boolean> => {
    if (!uid || !islandState) return false;
    const price = 'effectivePrice' in item ? (item as EnrichedShopItem).effectivePrice : item.price;
    if (balance < price) return false;

    const placement = placeItem(item, islandState);
    if (!placement) return false;

    const newState: IslandState = {
      ...islandState,
      placements: [...islandState.placements, placement],
      totalSpent: islandState.totalSpent + price,
      purchaseHistory: [...islandState.purchaseHistory, item.id],
      lastPurchaseTimestamp: new Date().toISOString(),
    };
    setIslandState(newState);

    const progressDocRef = doc(db, 'progress', uid);
    setDoc(progressDocRef, {
      islandState: newState,
      pointsData: { totalSpent: increment(price) },
    }, { merge: true }).catch(err => {
      console.error('Failed to save island purchase:', err);
    });

    return true;
  }, [uid, islandState, placeItem]);

  // Claim a milestone reward
  const claimReward = useCallback(async (reward: MilestoneReward): Promise<boolean> => {
    if (!uid || !islandState) return false;
    if ((islandState.claimedRewards ?? []).includes(reward.id)) return false;

    const placement = placeItem(reward.item, islandState);
    if (!placement) return false;

    const newState: IslandState = {
      ...islandState,
      placements: [...islandState.placements, placement],
      claimedRewards: [...(islandState.claimedRewards ?? []), reward.id],
      lastPurchaseTimestamp: new Date().toISOString(),
    };
    setIslandState(newState);

    const progressDocRef = doc(db, 'progress', uid);
    setDoc(progressDocRef, { islandState: newState }, { merge: true }).catch(console.error);

    return true;
  }, [uid, islandState, placeItem]);

  // Place a gifted item on the island (no cost)
  const placeGiftItem = useCallback(async (itemId: string): Promise<boolean> => {
    if (!uid || !islandState) return false;
    const item = SHOP_CATALOG.find(i => i.id === itemId);
    if (!item) return false;

    const placement = placeItem(item, islandState);
    if (!placement) return false;

    const newState: IslandState = {
      ...islandState,
      placements: [...islandState.placements, placement],
      purchaseHistory: [...islandState.purchaseHistory, item.id],
    };
    setIslandState(newState);

    const progressDocRef = doc(db, 'progress', uid);
    setDoc(progressDocRef, { islandState: newState }, { merge: true }).catch(console.error);

    return true;
  }, [uid, islandState, placeItem]);

  return {
    islandState,
    isLoading,
    availableItems,
    waterColor,
    stats,
    purchaseItem,
    placeGiftItem,
    hasItem,
    milestoneRewards,
    claimReward,
  };
}
