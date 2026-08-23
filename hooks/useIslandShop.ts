/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect, useCallback, useMemo } from 'react';
import { doc, setDoc, updateDoc, increment, arrayUnion } from 'firebase/firestore';
import { db } from '../firebase';
import { useProgress } from '../contexts/ProgressContext';
import { useFreshProgress } from './useFreshProgress';
import { type NorthStar, type IslandState, type IslandPlacement, type ShopItem, type NorthStarCategory, type IslandInventoryItem } from '../types';
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
import {
  createPlacementId,
  getPlacementRules,
  ISLAND_SCHEMA_VERSION,
  migrateIslandState,
} from '../services/islandStateMigration';
import { canPlaceAt } from '../components/journey/build/islandBuildModel';
import { getJourneyV2BasePrice } from '../journeyEconomyConfig';
import { awaitWriteOrTimeout } from '../utils/firestoreWrite';
import { DEMO_STUDENT_UID } from '../data/devStudent';

function isBuilding(model: string): boolean {
  return model.startsWith('building-') || model.startsWith('unit-') || model === 'bridge.glb';
}

function findAnyIslandItem(itemId: string): ShopItem | undefined {
  return [...SHOP_CATALOG, ...EXCLUSIVE_ITEMS].find(item => item.id === itemId)
    ?? Object.values(MILESTONE_REWARDS)
      .flatMap(rewards => rewards ?? [])
      .map(reward => reward.item)
      .find(item => item.id === itemId);
}

// JC NorthStar categories (added Phase 5) don't yet have dedicated
// STARTER_PACKS entries — the island shop content was built for the 6
// senior categories and a JC-specific design pass is still pending.
// Map each JC category to its closest senior equivalent so onboarding
// doesn't crash for JC students. The category field on the saved island
// state preserves the user's actual JC choice — only the starter
// placements come from the senior equivalent.
const JC_TO_SENIOR_PACK_ALIAS: Partial<Record<NorthStarCategory, NorthStarCategory>> = {
  'family-people':     'family-community',
  'prove-myself-jc':   'prove-myself',
  'curiosity-craft':   'career-craft',
  'future-doors':      'options-freedom',
};

export function createStarterState(category: NorthStarCategory): IslandState {
  // Look up the pack via alias for JC categories; senior categories
  // resolve directly. Fall back to 'independence' as an absolute last
  // resort so a missing pack never crashes onboarding again.
  const aliasedCategory = JC_TO_SENIOR_PACK_ALIAS[category] ?? category;
  const pack = STARTER_PACKS[aliasedCategory] ?? STARTER_PACKS['independence'];
  const now = new Date().toISOString();
  return {
    schemaVersion: ISLAND_SCHEMA_VERSION,
    category, // keep the original JC category — used by island UI for theming
    placements: pack.placements.map(p => ({
      ...p,
      placementId: createPlacementId(),
      layer: getPlacementRules({
        id: p.itemId,
        name: p.itemId,
        description: '',
        model: p.model,
        category: p.type === 'decoration'
          ? 'nature'
          : p.model.startsWith('path-') || p.model === 'bridge.glb'
            ? 'path'
            : (isBuilding(p.model) ? 'building' : 'terrain'),
        type: p.type,
        price: 0,
      }).layer,
      purchasedAt: now,
    })),
    totalSpent: 0,
    purchaseHistory: [],
    lastPurchaseTimestamp: '',
    claimedRewards: [],
    inventory: [],
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
  const {
    reloadProgress,
    rawProgressDoc: sharedProgressDoc,
    progressLoaded: sharedProgressLoaded,
    updateDemoProgress,
  } = useProgress();
  const isDemo = uid === DEMO_STUDENT_UID;
  const { doc: freshProgressDoc, loaded: freshProgressLoaded } = useFreshProgress(isDemo ? undefined : uid);
  const rawProgressDoc = isDemo ? sharedProgressDoc : freshProgressDoc;
  const progressLoaded = isDemo ? sharedProgressLoaded : freshProgressLoaded;
  const [islandState, setIslandState] = useState<IslandState | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const commitIslandState = useCallback((nextState: IslandState, pointsSpent = 0) => {
    setIslandState(nextState);
    if (!isDemo) return;
    updateDemoProgress(current => ({
      ...current,
      islandState: nextState,
      ...(pointsSpent > 0 ? {
        pointsData: {
          ...current.pointsData,
          totalSpent: (current.pointsData?.totalSpent ?? 0) + pointsSpent,
        },
      } : {}),
    }));
  }, [isDemo, updateDemoProgress]);

  // Load island state from context
  useEffect(() => {
    if (!progressLoaded) return;

    if (!uid || !northStar?.category) {
      setIslandState(null);
      setIsLoading(false);
      return;
    }

    // The localhost Demo Account is deliberately in-memory and has no
    // Firestore document. Treat a missing fresh document as an empty one so
    // Journey can initialise its starter island instead of crashing while
    // reading `islandState` from null.
    const data = rawProgressDoc;
    const stored = data?.islandState as IslandState | undefined;
    if (stored && stored.category === northStar.category && Array.isArray(stored.placements)) {
      const migrated = migrateIslandState(stored);
      setIslandState(migrated.state);
      if (migrated.changed) {
        if (isDemo) {
          updateDemoProgress(current => ({ ...current, islandState: migrated.state }));
        } else {
          setDoc(doc(db, 'progress', uid), { islandState: migrated.state }, { merge: true }).catch(console.error);
        }
      }
    } else {
      // No state or North Star changed — initialize with starter pack
      const starter = createStarterState(northStar.category);
      commitIslandState(starter);
      if (!isDemo) {
        setDoc(doc(db, 'progress', uid), { islandState: starter }, { merge: true }).catch(console.error);
      }
    }
    setIsLoading(false);
  }, [uid, northStar?.category, progressLoaded, rawProgressDoc, isDemo, commitIslandState, updateDemoProgress]);

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
        originalPrice: getJourneyV2BasePrice(item),
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
    const placementBase = {
      placementId: createPlacementId(),
      layer: getPlacementRules(item).layer,
    };
    if (item.type === 'hex') {
      if (isBuilding(item.model)) {
        const pos = findBuildingPlacement(state.placements);
        if (!pos) return null;
        return { ...placementBase, itemId: item.id, model: item.model, type: 'hex', q: pos.q, r: pos.r, purchasedAt: now };
      } else {
        const occupied = new Set<string>();
        for (const p of state.placements) {
          if (p.type === 'hex') occupied.add(`${p.q},${p.r}`);
        }
        const pos = findBestLandPlacement(occupied);
        return { ...placementBase, itemId: item.id, model: item.model, type: 'hex', q: pos.q, r: pos.r, purchasedAt: now };
      }
    } else {
      const pos = findDecorationPlacement(state.placements);
      if (!pos) return null;
      return {
        ...placementBase, itemId: item.id, model: item.model, type: 'decoration',
        q: pos.q, r: pos.r, scale: item.defaultScale ?? 0.5,
        offsetX: pos.offsetX, offsetZ: pos.offsetZ, purchasedAt: now,
      };
    }
  }, []);

  const createPlacementAt = useCallback((item: ShopItem, q: number, r: number, rotation: number = 0): IslandPlacement => ({
    placementId: createPlacementId(),
    itemId: item.id,
    model: item.model,
    type: item.type,
    layer: getPlacementRules(item).layer,
    q,
    r,
    rotation,
    ...(item.type === 'decoration' ? { scale: item.defaultScale ?? 0.5 } : {}),
    purchasedAt: new Date().toISOString(),
  }), []);

  const purchaseItemAt = useCallback(async (
    item: EnrichedShopItem | ShopItem,
    balance: number,
    q: number,
    r: number,
    rotation: number = 0,
  ): Promise<boolean> => {
    if (!uid || !islandState || !canPlaceAt(islandState, item, q, r)) return false;
    const price = 'effectivePrice' in item ? item.effectivePrice : item.price;
    if (balance < price) return false;
    const placement = createPlacementAt(item, q, r, rotation);
    const timestamp = new Date().toISOString();
    const newState: IslandState = {
      ...islandState,
      placements: [...islandState.placements, placement],
      totalSpent: islandState.totalSpent + price,
      purchaseHistory: [...islandState.purchaseHistory, item.id],
      lastPurchaseTimestamp: timestamp,
    };
    commitIslandState(newState, price);
    if (isDemo) return true;
    try {
      const outcome = await awaitWriteOrTimeout(updateDoc(doc(db, 'progress', uid), {
        'islandState.placements': arrayUnion(placement),
        'islandState.totalSpent': increment(price),
        'islandState.purchaseHistory': arrayUnion(item.id),
        'islandState.lastPurchaseTimestamp': timestamp,
        'pointsData.totalSpent': increment(price),
      }), 'useIslandShop.purchaseItemAt');
      if (outcome === 'failed') throw new Error('Purchase placement rejected');
      reloadProgress();
      return true;
    } catch (error) {
      setIslandState(islandState);
      console.error('Failed to confirm island placement:', error);
      return false;
    }
  }, [uid, islandState, createPlacementAt, reloadProgress, commitIslandState, isDemo]);

  const updatePlacement = useCallback(async (
    placementId: string,
    updates: Pick<IslandPlacement, 'q' | 'r' | 'rotation'>,
  ): Promise<boolean> => {
    if (!uid || !islandState) return false;
    const index = islandState.placements.findIndex(p => p.placementId === placementId);
    if (index < 0) return false;
    const currentPlacement = islandState.placements[index];
    const item = findAnyIslandItem(currentPlacement.itemId);
    const stateWithoutCurrent = {
      ...islandState,
      placements: islandState.placements.filter((_, placementIndex) => placementIndex !== index),
    };
    if (!item || !canPlaceAt(stateWithoutCurrent, item, updates.q, updates.r)) return false;
    const nextPlacements = islandState.placements.map((placement, placementIndex) =>
      placementIndex === index ? { ...placement, ...updates } : placement
    );
    const previous = islandState;
    const next = { ...islandState, placements: nextPlacements };
    commitIslandState(next);
    if (isDemo) return true;
    try {
      const outcome = await awaitWriteOrTimeout(
        updateDoc(doc(db, 'progress', uid), { 'islandState.placements': nextPlacements }),
        'useIslandShop.updatePlacement',
      );
      if (outcome === 'failed') throw new Error('Placement update rejected');
      return true;
    } catch (error) {
      setIslandState(previous);
      console.error('Failed to update island placement:', error);
      return false;
    }
  }, [uid, islandState, commitIslandState, isDemo]);

  const storePlacement = useCallback(async (placementId: string): Promise<boolean> => {
    if (!uid || !islandState) return false;
    const placement = islandState.placements.find(p => p.placementId === placementId);
    if (!placement || placement.isStarter) return false;
    const inventoryItem: IslandInventoryItem = {
      inventoryId: createPlacementId().replace('pl_', 'inv_'),
      itemId: placement.itemId,
      source: 'stored',
      acquiredAt: new Date().toISOString(),
    };
    const placements = islandState.placements.filter(p => p.placementId !== placementId);
    const inventory = [...(islandState.inventory ?? []), inventoryItem];
    const previous = islandState;
    commitIslandState({ ...islandState, placements, inventory });
    if (isDemo) return true;
    try {
      const outcome = await awaitWriteOrTimeout(updateDoc(doc(db, 'progress', uid), {
        'islandState.placements': placements,
        'islandState.inventory': inventory,
      }), 'useIslandShop.storePlacement');
      if (outcome === 'failed') throw new Error('Store placement rejected');
      return true;
    } catch (error) {
      setIslandState(previous);
      console.error('Failed to store island placement:', error);
      return false;
    }
  }, [uid, islandState, commitIslandState, isDemo]);

  const placeInventoryItem = useCallback(async (
    inventoryId: string,
    q: number,
    r: number,
    rotation: number = 0,
  ): Promise<boolean> => {
    if (!uid || !islandState) return false;
    const inventoryEntry = (islandState.inventory ?? []).find(entry => entry.inventoryId === inventoryId);
    if (!inventoryEntry) return false;
    const item = findAnyIslandItem(inventoryEntry.itemId);
    if (!item || !canPlaceAt(islandState, item, q, r)) return false;
    const placement = createPlacementAt(item, q, r, rotation);
    const inventory = (islandState.inventory ?? []).filter(entry => entry.inventoryId !== inventoryId);
    const placements = [...islandState.placements, placement];
    const previous = islandState;
    commitIslandState({ ...islandState, placements, inventory });
    if (isDemo) return true;
    try {
      const outcome = await awaitWriteOrTimeout(updateDoc(doc(db, 'progress', uid), {
        'islandState.placements': placements,
        'islandState.inventory': inventory,
      }), 'useIslandShop.placeInventoryItem');
      if (outcome === 'failed') throw new Error('Inventory placement rejected');
      return true;
    } catch (error) {
      setIslandState(previous);
      console.error('Failed to place inventory item:', error);
      return false;
    }
  }, [uid, islandState, createPlacementAt, commitIslandState, isDemo]);

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
    commitIslandState(newState, price);
    if (isDemo) return true;

    // Atomic deltas (audit item 18): append only the new placement / history /
    // spend rather than overwriting the whole islandState, removing the
    // read-modify-write race with a concurrent purchase or rank-up grant.
    const progressDocRef = doc(db, 'progress', uid);
    updateDoc(progressDocRef, {
      'islandState.placements': arrayUnion(placement),
      'islandState.totalSpent': increment(price),
      'islandState.purchaseHistory': arrayUnion(item.id),
      'islandState.lastPurchaseTimestamp': newState.lastPurchaseTimestamp,
      'pointsData.totalSpent': increment(price),
    })
      .then(() => reloadProgress())
      .catch(err => {
        console.error('Failed to save island purchase:', err);
      });

    return true;
  }, [uid, islandState, placeItem, reloadProgress, commitIslandState, isDemo]);

  // Claim a milestone reward
  const claimReward = useCallback(async (reward: MilestoneReward): Promise<boolean> => {
    if (!uid || !islandState) return false;
    if ((islandState.claimedRewards ?? []).includes(reward.id)) return false;

    const inventoryItem: IslandInventoryItem = {
      inventoryId: createPlacementId().replace('pl_', 'inv_'),
      itemId: reward.item.id,
      source: 'milestone',
      acquiredAt: new Date().toISOString(),
    };

    const newState: IslandState = {
      ...islandState,
      inventory: [...(islandState.inventory ?? []), inventoryItem],
      claimedRewards: [...(islandState.claimedRewards ?? []), reward.id],
      lastPurchaseTimestamp: new Date().toISOString(),
    };
    commitIslandState(newState);
    if (isDemo) return true;

    const progressDocRef = doc(db, 'progress', uid);
    try {
      const outcome = await awaitWriteOrTimeout(updateDoc(progressDocRef, {
        'islandState.inventory': arrayUnion(inventoryItem),
        'islandState.claimedRewards': arrayUnion(reward.id),
        'islandState.lastPurchaseTimestamp': newState.lastPurchaseTimestamp,
      }), 'useIslandShop.claimReward');
      if (outcome === 'failed') throw new Error('Reward claim rejected');
      return true;
    } catch (error) {
      setIslandState(islandState);
      console.error('Failed to claim island reward:', error);
      return false;
    }
  }, [uid, islandState, commitIslandState, isDemo]);

  // Place a gifted item on the island (no cost)
  const placeGiftItem = useCallback(async (itemId: string): Promise<boolean> => {
    if (!uid || !islandState) return false;
    const item = SHOP_CATALOG.find(i => i.id === itemId);
    if (!item) return false;

    const inventoryItem: IslandInventoryItem = {
      inventoryId: createPlacementId().replace('pl_', 'inv_'),
      itemId: item.id,
      source: 'gift',
      acquiredAt: new Date().toISOString(),
    };

    const newState: IslandState = {
      ...islandState,
      inventory: [...(islandState.inventory ?? []), inventoryItem],
      purchaseHistory: [...islandState.purchaseHistory, item.id],
    };
    commitIslandState(newState);
    if (isDemo) return true;

    const progressDocRef = doc(db, 'progress', uid);
    try {
      const outcome = await awaitWriteOrTimeout(updateDoc(progressDocRef, {
        'islandState.inventory': arrayUnion(inventoryItem),
        'islandState.purchaseHistory': arrayUnion(item.id),
      }), 'useIslandShop.placeGiftItem');
      if (outcome === 'failed') throw new Error('Gift inventory update rejected');
      return true;
    } catch (error) {
      setIslandState(islandState);
      console.error('Failed to add gifted island item:', error);
      return false;
    }
  }, [uid, islandState, commitIslandState, isDemo]);

  return {
    islandState,
    isLoading,
    availableItems,
    waterColor,
    stats,
    purchaseItem,
    purchaseItemAt,
    updatePlacement,
    storePlacement,
    placeInventoryItem,
    placeGiftItem,
    hasItem,
    milestoneRewards,
    claimReward,
  };
}
