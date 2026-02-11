/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { createPortal } from 'react-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Star, Coffee, CalendarOff, Lock, Check, ShoppingBag, Palette } from 'lucide-react';
import { type CosmeticUnlocks, type EarnedRest } from '../types';
import { getAvatarUrl } from './Auth';

const MotionDiv = motion.div as any;
const MotionButton = motion.button as any;

// Extra avatar seeds beyond the base 8
export const EXTRA_AVATAR_SEEDS = ['Luna', 'Kai', 'Suki', 'Dara', 'Nico', 'Asha', 'Finn', 'Yuki'];

interface RewardShopModalProps {
  isOpen: boolean;
  onClose: () => void;
  pointsBalance: number;
  cosmeticUnlocks: CosmeticUnlocks;
  earnedRest: EarnedRest;
  onSpend: (type: 'skip-session' | 'rest-day-pass' | 'unlock-avatar' | 'unlock-theme', detail?: string) => void;
}

const RewardShopModal: React.FC<RewardShopModalProps> = ({
  isOpen, onClose, pointsBalance, cosmeticUnlocks, earnedRest, onSpend,
}) => {
  const canAfford = (cost: number) => pointsBalance >= cost;

  return createPortal(
    <AnimatePresence>
      {isOpen && (
        <MotionDiv
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black/60 flex items-center justify-center z-[200] p-4"
          onClick={onClose}
        >
          <MotionDiv
            initial={{ scale: 0.96, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.96, opacity: 0 }}
            transition={{ duration: 0.2, ease: [0.16, 1, 0.3, 1] }}
            className="relative bg-white dark:bg-zinc-900 border border-zinc-200/50 dark:border-white/[0.08] rounded-2xl w-full max-w-lg shadow-[0_24px_64px_rgba(0,0,0,0.12)] dark:shadow-[0_24px_64px_rgba(0,0,0,0.5)] overflow-hidden max-h-[85vh] flex flex-col"
            onClick={(e: React.MouseEvent) => e.stopPropagation()}
          >
            {/* Header */}
            <div className="flex items-center justify-between p-6 pb-4 flex-shrink-0">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-purple-100 dark:bg-purple-900/40 flex items-center justify-center">
                  <ShoppingBag size={20} className="text-purple-600 dark:text-purple-400" />
                </div>
                <div>
                  <h2 className="font-sans text-xl font-semibold text-zinc-900 dark:text-white tracking-tight">
                    Reward Shop
                  </h2>
                  <div className="flex items-center gap-1.5 mt-0.5">
                    <Star size={12} className="text-yellow-500" />
                    <span className="text-xs font-bold text-yellow-600 dark:text-yellow-400">{pointsBalance} pts available</span>
                  </div>
                </div>
              </div>
              <button
                onClick={onClose}
                className="text-zinc-400 dark:text-white/25 hover:text-zinc-600 dark:hover:text-white/50 transition-colors"
              >
                <X size={18} />
              </button>
            </div>

            {/* Content */}
            <div className="flex-1 overflow-y-auto px-6 pb-6 space-y-6">
              {/* Earned Rest Section */}
              <section>
                <h3 className="text-xs font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-3">
                  Earned Rest
                </h3>
                <div className="space-y-2">
                  {/* Skip a Session */}
                  <div className="flex items-center justify-between p-3 rounded-xl bg-zinc-50 dark:bg-white/[0.03] border border-zinc-200/50 dark:border-white/[0.06]">
                    <div className="flex items-center gap-3">
                      <div className="w-9 h-9 rounded-lg bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center">
                        <Coffee size={18} className="text-blue-500 dark:text-blue-400" />
                      </div>
                      <div>
                        <p className="text-sm font-bold text-zinc-700 dark:text-zinc-200">Skip a Session</p>
                        <p className="text-[10px] text-zinc-400 dark:text-zinc-500">Skip one session without breaking your streak</p>
                      </div>
                    </div>
                    <MotionButton
                      onClick={() => onSpend('skip-session', 'pending')}
                      disabled={!canAfford(20)}
                      whileHover={canAfford(20) ? { scale: 1.05 } : {}}
                      whileTap={canAfford(20) ? { scale: 0.95 } : {}}
                      className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                        canAfford(20)
                          ? 'bg-purple-600 text-white hover:bg-purple-700'
                          : 'bg-zinc-100 dark:bg-zinc-800 text-zinc-400 dark:text-zinc-500 cursor-not-allowed'
                      }`}
                    >
                      <Star size={10} />
                      20 pts
                    </MotionButton>
                  </div>

                  {/* Rest Day Pass */}
                  <div className="flex items-center justify-between p-3 rounded-xl bg-zinc-50 dark:bg-white/[0.03] border border-zinc-200/50 dark:border-white/[0.06]">
                    <div className="flex items-center gap-3">
                      <div className="w-9 h-9 rounded-lg bg-rose-100 dark:bg-rose-900/30 flex items-center justify-center">
                        <CalendarOff size={18} className="text-rose-500 dark:text-rose-400" />
                      </div>
                      <div>
                        <p className="text-sm font-bold text-zinc-700 dark:text-zinc-200">Rest Day Pass</p>
                        <p className="text-[10px] text-zinc-400 dark:text-zinc-500">Turn today into a rest day, streak protected</p>
                      </div>
                    </div>
                    <MotionButton
                      onClick={() => onSpend('rest-day-pass')}
                      disabled={!canAfford(60)}
                      whileHover={canAfford(60) ? { scale: 1.05 } : {}}
                      whileTap={canAfford(60) ? { scale: 0.95 } : {}}
                      className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                        canAfford(60)
                          ? 'bg-purple-600 text-white hover:bg-purple-700'
                          : 'bg-zinc-100 dark:bg-zinc-800 text-zinc-400 dark:text-zinc-500 cursor-not-allowed'
                      }`}
                    >
                      <Star size={10} />
                      60 pts
                    </MotionButton>
                  </div>
                </div>
              </section>

              {/* Avatar Unlocks Section */}
              <section>
                <h3 className="text-xs font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-3">
                  Avatar Unlocks — 50 pts each
                </h3>
                <div className="grid grid-cols-4 gap-2.5">
                  {EXTRA_AVATAR_SEEDS.map(seed => {
                    const isUnlocked = cosmeticUnlocks.avatarSeeds.includes(seed);
                    return (
                      <div key={seed} className="relative">
                        <button
                          onClick={() => !isUnlocked && canAfford(50) && onSpend('unlock-avatar', seed)}
                          disabled={isUnlocked || !canAfford(50)}
                          className={`w-full rounded-xl aspect-square p-1.5 transition-all ${
                            isUnlocked
                              ? 'ring-2 ring-emerald-400 bg-emerald-50 dark:bg-emerald-900/20'
                              : canAfford(50)
                                ? 'bg-zinc-50 dark:bg-white/[0.04] ring-1 ring-zinc-200 dark:ring-white/[0.06] hover:ring-purple-300 dark:hover:ring-purple-600 cursor-pointer'
                                : 'bg-zinc-50 dark:bg-white/[0.04] ring-1 ring-zinc-200 dark:ring-white/[0.06] opacity-50 cursor-not-allowed'
                          }`}
                        >
                          <img
                            src={getAvatarUrl(seed)}
                            alt={seed}
                            className={`w-full h-full rounded-lg ${!isUnlocked ? 'grayscale opacity-40' : ''}`}
                          />
                        </button>
                        {/* Lock/Check overlay */}
                        <div className="absolute bottom-1 right-1">
                          {isUnlocked ? (
                            <div className="w-5 h-5 rounded-full bg-emerald-500 flex items-center justify-center">
                              <Check size={10} className="text-white" />
                            </div>
                          ) : (
                            <div className="w-5 h-5 rounded-full bg-zinc-400 dark:bg-zinc-600 flex items-center justify-center">
                              <Lock size={9} className="text-white" />
                            </div>
                          )}
                        </div>
                        <p className="text-[9px] font-bold text-center text-zinc-500 dark:text-zinc-400 mt-1">{seed}</p>
                      </div>
                    );
                  })}
                </div>
              </section>

              {/* Theme Colors Section (placeholder) */}
              <section>
                <h3 className="text-xs font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-3">
                  Theme Colors — 40 pts each
                </h3>
                <div className="p-4 rounded-xl bg-zinc-50 dark:bg-white/[0.03] border border-zinc-200/50 dark:border-white/[0.06] text-center">
                  <Palette size={24} className="text-zinc-300 dark:text-zinc-600 mx-auto mb-2" />
                  <p className="text-xs font-semibold text-zinc-400 dark:text-zinc-500">Coming Soon</p>
                  <p className="text-[10px] text-zinc-400 dark:text-zinc-500 mt-0.5">Custom accent themes will be available in a future update.</p>
                </div>
              </section>
            </div>
          </MotionDiv>
        </MotionDiv>
      )}
    </AnimatePresence>,
    document.body
  );
};

export default RewardShopModal;
