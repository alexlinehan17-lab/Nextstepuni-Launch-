/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo, useRef, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MotionDiv } from '../Motion';
import { ChevronDown, ChevronRight, Star, Lock, Gift, Check, X } from 'lucide-react';
import { ShopItemCategory } from '../../types';
import { isUniqueItem, MilestoneReward } from '../../islandShopData';
import { EnrichedShopItem, MilestoneRewardStatus } from '../../hooks/useIslandShop';

interface IslandShopDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  items: EnrichedShopItem[];
  pointsBalance: number;
  onBuy: (item: EnrichedShopItem) => void;
  hasItem: (itemId: string) => boolean;
  milestoneRewards: MilestoneRewardStatus[];
  onClaimReward: (reward: MilestoneReward) => void;
}

type TabKey = 'rewards' | ShopItemCategory | 'exclusive';

const CATEGORY_LABELS: { key: TabKey; label: string }[] = [
  { key: 'rewards', label: 'Rewards' },
  { key: 'terrain', label: 'Terrain' },
  { key: 'building', label: 'Buildings' },
  { key: 'path', label: 'Paths' },
  { key: 'nature', label: 'Nature' },
  { key: 'furniture', label: 'Furniture' },
  { key: 'vehicle', label: 'Vehicles' },
  { key: 'atmosphere', label: 'Atmosphere' },
  { key: 'exclusive', label: 'Exclusive' },
];

const IslandShopDrawer: React.FC<IslandShopDrawerProps> = ({
  isOpen, onClose, items, pointsBalance, onBuy, hasItem,
  milestoneRewards, onClaimReward,
}) => {
  const [activeCategory, setActiveCategory] = useState<TabKey>('rewards');
  const scrollRef = useRef<HTMLDivElement>(null);

  const exclusiveItems = useMemo(() => items.filter(i => i.exclusiveTo), [items]);
  const hasExclusive = exclusiveItems.length > 0;

  const filteredItems = useMemo(() => {
    if (activeCategory === 'rewards') return [];
    if (activeCategory === 'exclusive') return exclusiveItems;
    return items.filter(i => i.category === activeCategory && !i.exclusiveTo);
  }, [items, activeCategory, exclusiveItems]);

  const visibleCategories = useMemo(() => {
    if (hasExclusive) return CATEGORY_LABELS;
    return CATEGORY_LABELS.filter(c => c.key !== 'exclusive');
  }, [hasExclusive]);

  const claimableCount = useMemo(() =>
    milestoneRewards.filter(r => r.status === 'claimable').length
  , [milestoneRewards]);

  const handleBuy = useCallback((item: EnrichedShopItem) => {
    onBuy(item);
  }, [onBuy]);

  const isDesktop = typeof window !== 'undefined' && window.matchMedia('(min-width: 768px)').matches;

  /* ── Shared content ── */
  const shopContent = (
    <>
      {/* Category tabs */}
      <div className="px-4 pb-3 md:pb-3">
        <div
          className="shop-tabs-scroll flex md:flex-wrap gap-2 overflow-x-auto"
          style={{ scrollbarWidth: 'none' }}
        >
          {visibleCategories.map(cat => (
            <button
              key={cat.key}
              onClick={() => setActiveCategory(cat.key)}
              style={{ flexShrink: 0, whiteSpace: 'nowrap' }}
              className={`px-3 py-1.5 rounded-full text-xs font-semibold transition-colors relative ${
                activeCategory === cat.key
                  ? 'bg-[var(--accent-hex)] text-white'
                  : 'bg-zinc-200 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 hover:bg-zinc-300 dark:hover:bg-zinc-700'
              }`}
            >
              {cat.label}
              {cat.key === 'rewards' && claimableCount > 0 && (
                <span className="absolute -top-1 -right-1 w-4 h-4 rounded-full bg-amber-500 text-white text-[9px] font-bold flex items-center justify-center">
                  {claimableCount}
                </span>
              )}
            </button>
          ))}
        </div>
      </div>

      {/* Content area */}
      <div
        ref={scrollRef}
        className="overflow-y-auto px-4 pb-4 flex-1"
        style={{ scrollbarWidth: 'none' }}
      >
        {activeCategory === 'rewards' ? (
          /* ── Rewards tab ── */
          <div className="flex flex-col gap-2">
            {milestoneRewards.map(({ reward, status }) => (
              <div
                key={reward.id}
                className={`flex items-center gap-3 p-3 rounded-xl border transition-all ${
                  status === 'claimable'
                    ? 'border-amber-400 dark:border-amber-500 bg-amber-50/50 dark:bg-amber-950/20 animate-pulse-subtle'
                    : status === 'claimed'
                    ? 'border-emerald-300 dark:border-emerald-800 bg-emerald-50/30 dark:bg-emerald-950/10'
                    : 'border-zinc-200 dark:border-zinc-800 bg-zinc-50/50 dark:bg-zinc-900/50 opacity-60'
                }`}
              >
                {/* Icon */}
                <div className={`w-10 h-10 rounded-xl flex items-center justify-center shrink-0 ${
                  status === 'claimable'
                    ? 'bg-amber-100 dark:bg-amber-900/40 text-amber-600 dark:text-amber-400'
                    : status === 'claimed'
                    ? 'bg-emerald-100 dark:bg-emerald-900/40 text-emerald-600 dark:text-emerald-400'
                    : 'bg-zinc-200 dark:bg-zinc-800 text-zinc-400 dark:text-zinc-600'
                }`}>
                  {status === 'claimed' ? <Check size={18} /> : status === 'claimable' ? <Gift size={18} /> : <Lock size={14} />}
                </div>

                {/* Info */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-1.5">
                    <span className="text-xs font-semibold text-zinc-800 dark:text-zinc-200 truncate">{reward.label}</span>
                    <span className="text-[10px] text-zinc-400 dark:text-zinc-500">·</span>
                    <span className="text-[10px] text-zinc-500 dark:text-zinc-400 truncate">{reward.item.name}</span>
                  </div>
                  <p className="text-[10px] text-zinc-400 dark:text-zinc-500 mt-0.5">
                    {status === 'locked' ? `Complete ${reward.modulesRequired} modules` : status === 'claimed' ? 'Claimed' : `${reward.modulesRequired} modules reached!`}
                  </p>
                </div>

                {/* Action */}
                {status === 'claimable' && (
                  <button
                    onClick={() => onClaimReward(reward)}
                    className="shrink-0 px-3 py-1.5 rounded-lg text-[10px] font-bold bg-amber-500 text-white hover:bg-amber-600 transition-colors"
                  >
                    Claim!
                  </button>
                )}
                {status === 'claimed' && (
                  <span className="shrink-0 text-[10px] font-semibold text-emerald-500">
                    <Check size={14} />
                  </span>
                )}
              </div>
            ))}
            {milestoneRewards.length === 0 && (
              <p className="text-center text-xs text-zinc-400 dark:text-zinc-500 py-8">
                Set your North Star to unlock rewards
              </p>
            )}
          </div>
        ) : (
          /* ── Shop items grid ── */
          <div className="grid grid-cols-2 gap-2">
            {filteredItems.map(item => {
              const owned = isUniqueItem(item) && hasItem(item.id);
              const canAfford = !item.isLocked && pointsBalance >= item.effectivePrice;

              return (
                <div
                  key={item.id}
                  className={`bg-white/90 dark:bg-zinc-900/90 backdrop-blur rounded-xl border p-3 flex flex-col justify-between ${
                    item.isLocked
                      ? 'border-zinc-300 dark:border-zinc-700 opacity-60'
                      : 'border-zinc-200 dark:border-zinc-800'
                  }`}
                >
                  <div>
                    <div className="flex items-center justify-between mb-1">
                      <h4 className="text-xs font-semibold text-zinc-800 dark:text-zinc-200 leading-tight">
                        {item.name}
                      </h4>
                      <div className="flex items-center gap-1 shrink-0">
                        {item.hasDiscount && (
                          <Star size={10} className="text-[var(--accent-hex)]" fill="currentColor" />
                        )}
                        {item.exclusiveTo && (
                          <Star size={12} className="text-amber-500" fill="currentColor" />
                        )}
                        {item.isLocked && (
                          <Lock size={12} className="text-zinc-400" />
                        )}
                      </div>
                    </div>
                    <p className="text-[10px] text-zinc-500 dark:text-zinc-400 leading-snug line-clamp-2">
                      {item.isLocked
                        ? `Unlock at ${item.unlockAt} modules`
                        : item.description}
                    </p>
                  </div>

                  <div className="mt-2">
                    {owned ? (
                      <span className="block text-center text-[10px] font-semibold text-emerald-500 py-1">
                        Owned
                      </span>
                    ) : item.isLocked ? (
                      <span className="block text-center text-[10px] font-semibold text-zinc-400 py-1">
                        <Lock size={10} className="inline mr-1" />
                        Locked
                      </span>
                    ) : (
                      <button
                        onClick={() => handleBuy(item)}
                        disabled={!canAfford}
                        className={`w-full px-2 py-1.5 rounded-lg text-[10px] font-semibold transition-colors ${
                          canAfford
                            ? 'bg-[var(--accent-hex)] text-white hover:opacity-90'
                            : 'bg-zinc-200 dark:bg-zinc-700 text-zinc-400 dark:text-zinc-500 cursor-not-allowed'
                        }`}
                      >
                        {item.hasDiscount && (
                          <span className="line-through opacity-60 mr-1">{item.originalPrice}</span>
                        )}
                        {item.effectivePrice} pts
                      </button>
                    )}
                  </div>
                </div>
              );
            })}

            {filteredItems.length === 0 && (
              <p className="col-span-2 text-center text-xs text-zinc-400 dark:text-zinc-500 py-8">
                No items in this category
              </p>
            )}
          </div>
        )}
      </div>

      <style>{`
        @keyframes pulse-subtle {
          0%, 100% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.3); }
          50% { box-shadow: 0 0 0 4px rgba(245, 158, 11, 0.1); }
        }
        .animate-pulse-subtle { animation: pulse-subtle 2s ease-in-out infinite; }
        .shop-tabs-scroll::-webkit-scrollbar { display: none; }
      `}</style>
    </>
  );

  return (
    <AnimatePresence>
      {isOpen && (
        <MotionDiv
          key="shop-drawer"
          initial={isDesktop ? { x: '100%' } : { y: '100%' }}
          animate={isDesktop ? { x: 0 } : { y: 0 }}
          exit={isDesktop ? { x: '100%' } : { y: '100%' }}
          transition={{ type: 'spring', damping: 30, stiffness: 300 }}
          className={`z-[86] bg-white dark:bg-zinc-900 shadow-2xl flex flex-col ${
            isDesktop
              ? 'absolute top-0 right-0 bottom-0 w-[380px] rounded-l-2xl border-l border-zinc-200 dark:border-zinc-800'
              : 'absolute bottom-0 left-0 right-0 rounded-t-2xl border-t border-zinc-200 dark:border-zinc-800'
          }`}
          style={isDesktop ? undefined : { maxHeight: '50vh' }}
        >
          {/* Mobile: drag handle */}
          {!isDesktop && (
            <div className="flex justify-center pt-2 pb-1 cursor-pointer" onClick={onClose}>
              <div className="w-10 h-1 rounded-full bg-zinc-300 dark:bg-zinc-700" />
            </div>
          )}

          {/* Header */}
          <div className="flex items-center justify-between px-4 pb-2 pt-2">
            <h3 className="text-sm font-semibold text-zinc-900 dark:text-white">Island Shop</h3>
            <div className="flex items-center gap-2">
              <span className="text-sm font-bold text-[var(--accent-hex)]">{pointsBalance} pts</span>
              <button onClick={onClose} className="p-1 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800">
                {isDesktop ? (
                  <ChevronRight size={16} className="text-zinc-400" />
                ) : (
                  <ChevronDown size={16} className="text-zinc-400" />
                )}
              </button>
            </div>
          </div>

          {shopContent}
        </MotionDiv>
      )}
    </AnimatePresence>
  );
};

export default IslandShopDrawer;
