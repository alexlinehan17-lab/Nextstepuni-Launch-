/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { createPortal } from 'react-dom';
import { AnimatePresence } from 'framer-motion';
import { MotionButton, MotionDiv } from './Motion';
import { X, Star, Coffee, CalendarOff, Lock, Check, ShoppingBag, ChevronRight, Layers } from 'lucide-react';
import { type CosmeticUnlocks, type EarnedRest, type UserSettings } from '../types';
import { getAvatarUrl } from '../utils/authUtils';
import { ACCENT_THEME_LIST, CARD_STYLES } from '../themeData';

// Extra avatar seeds beyond the base 8
export const EXTRA_AVATAR_SEEDS = ['Luna', 'Kai', 'Suki', 'Dara', 'Nico', 'Asha', 'Finn', 'Yuki'];

interface SkippableBlock {
  blockId: string;
  fullId: string;
  subjectName: string;
  sessionType: string;
}

interface RewardShopModalProps {
  isOpen: boolean;
  onClose: () => void;
  pointsBalance: number;
  cosmeticUnlocks: CosmeticUnlocks;
  earnedRest: EarnedRest;
  onSpend: (type: 'skip-session' | 'rest-day-pass' | 'unlock-avatar' | 'unlock-theme' | 'unlock-card-style', detail?: string) => void;
  skippableBlocks?: SkippableBlock[];
  settings?: UserSettings;
  updateSetting?: <K extends keyof UserSettings>(key: K, value: UserSettings[K]) => void;
}

const SESSION_TYPE_LABELS: Record<string, string> = {
  'new-learning': 'New Learning',
  'practice': 'Practice',
  'revision': 'Revision',
};

const RewardShopModal: React.FC<RewardShopModalProps> = ({
  isOpen, onClose, pointsBalance, cosmeticUnlocks, _earnedRest, onSpend, skippableBlocks = [], settings, updateSetting,
}) => {
  const [pickingSession, setPickingSession] = useState(false);
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
                  <div className="rounded-xl bg-zinc-50 dark:bg-white/[0.03] border border-zinc-200/50 dark:border-white/[0.06] overflow-hidden">
                    <div className="flex items-center justify-between p-3">
                      <div className="flex items-center gap-3">
                        <div className="w-9 h-9 rounded-lg bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center">
                          <Coffee size={18} className="text-blue-500 dark:text-blue-400" />
                        </div>
                        <div>
                          <p className="text-sm font-bold text-zinc-700 dark:text-zinc-200">Skip a Session</p>
                          <p className="text-[10px] text-zinc-400 dark:text-zinc-500">Skip one of today's sessions without breaking your streak</p>
                        </div>
                      </div>
                      {!pickingSession ? (
                        <MotionButton
                          onClick={() => setPickingSession(true)}
                          disabled={!canAfford(20) || skippableBlocks.length === 0}
                          whileHover={canAfford(20) && skippableBlocks.length > 0 ? { scale: 1.05 } : {}}
                          whileTap={canAfford(20) && skippableBlocks.length > 0 ? { scale: 0.95 } : {}}
                          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                            canAfford(20) && skippableBlocks.length > 0
                              ? 'bg-purple-600 text-white hover:bg-purple-700'
                              : 'bg-zinc-100 dark:bg-zinc-800 text-zinc-400 dark:text-zinc-500 cursor-not-allowed'
                          }`}
                        >
                          <Star size={10} />
                          20 pts
                        </MotionButton>
                      ) : (
                        <button
                          onClick={() => setPickingSession(false)}
                          className="text-[10px] font-medium text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-300 transition-colors"
                        >
                          Cancel
                        </button>
                      )}
                    </div>
                    <AnimatePresence>
                      {pickingSession && (
                        <MotionDiv
                          initial={{ height: 0, opacity: 0 }}
                          animate={{ height: 'auto', opacity: 1 }}
                          exit={{ height: 0, opacity: 0 }}
                          transition={{ duration: 0.2 }}
                          className="overflow-hidden"
                        >
                          <div className="px-3 pb-3 space-y-1.5">
                            <p className="text-[10px] font-semibold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">
                              Choose a session to skip
                            </p>
                            {skippableBlocks.length === 0 ? (
                              <p className="text-xs text-zinc-400 dark:text-zinc-500 py-2 text-center">
                                No sessions left to skip today
                              </p>
                            ) : (
                              skippableBlocks.map(block => (
                                <button
                                  key={block.fullId}
                                  onClick={() => {
                                    onSpend('skip-session', block.fullId);
                                    setPickingSession(false);
                                  }}
                                  className="w-full flex items-center justify-between p-2 rounded-lg bg-white dark:bg-white/[0.04] border border-zinc-200/50 dark:border-white/[0.06] hover:border-blue-300 dark:hover:border-blue-600 transition-all group"
                                >
                                  <div className="text-left">
                                    <p className="text-xs font-bold text-zinc-700 dark:text-zinc-200">{block.subjectName}</p>
                                    <p className="text-[10px] text-zinc-400 dark:text-zinc-500">
                                      {SESSION_TYPE_LABELS[block.sessionType] || block.sessionType}
                                    </p>
                                  </div>
                                  <ChevronRight size={14} className="text-zinc-300 dark:text-zinc-600 group-hover:text-blue-400 transition-colors" />
                                </button>
                              ))
                            )}
                          </div>
                        </MotionDiv>
                      )}
                    </AnimatePresence>
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

              {/* Accent Themes Section */}
              <section>
                <h3 className="text-xs font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-3">
                  Accent Themes — 40 pts each
                </h3>
                <div className="grid grid-cols-4 gap-2.5">
                  {ACCENT_THEME_LIST.map(theme => {
                    const isUnlocked = theme.price === 0 || (cosmeticUnlocks.themeColors || []).includes(theme.id);
                    const isActive = isUnlocked && settings?.accentTheme === theme.id;
                    const affordable = canAfford(theme.price);
                    return (
                      <button
                        key={theme.id}
                        onClick={() => {
                          if (isUnlocked && updateSetting) {
                            updateSetting('accentTheme', theme.id);
                          } else if (!isUnlocked && affordable) {
                            onSpend('unlock-theme', theme.id);
                            if (updateSetting) updateSetting('accentTheme', theme.id);
                          }
                        }}
                        disabled={!isUnlocked && !affordable}
                        className={`relative flex flex-col items-center gap-1.5 p-2.5 rounded-xl transition-all focus:outline-none focus-visible:outline-none ${
                          isActive
                            ? 'ring-2 ring-emerald-400 bg-emerald-50 dark:bg-emerald-900/20'
                            : isUnlocked
                              ? 'bg-zinc-50 dark:bg-white/[0.04] ring-1 ring-zinc-200 dark:ring-white/[0.06] hover:ring-zinc-300 dark:hover:ring-white/[0.15]'
                              : affordable
                                ? 'bg-zinc-50 dark:bg-white/[0.04] ring-1 ring-zinc-200 dark:ring-white/[0.06] hover:ring-purple-300 dark:hover:ring-purple-600 cursor-pointer'
                                : 'bg-zinc-50 dark:bg-white/[0.04] ring-1 ring-zinc-200 dark:ring-white/[0.06] opacity-50 cursor-not-allowed'
                        }`}
                      >
                        <div
                          className="w-8 h-8 rounded-full border-2 border-white dark:border-zinc-800 shadow-sm"
                          style={{ backgroundColor: theme.hex }}
                        />
                        <p className="text-[9px] font-bold text-zinc-500 dark:text-zinc-400 text-center leading-tight">{theme.name}</p>
                        {isActive && (
                          <div className="absolute top-1 right-1 w-4 h-4 rounded-full bg-emerald-500 flex items-center justify-center">
                            <Check size={8} className="text-white" />
                          </div>
                        )}
                        {!isUnlocked && (
                          <div className="absolute top-1 right-1">
                            {affordable ? (
                              <span className="text-[8px] font-bold text-purple-600 dark:text-purple-400 bg-purple-100 dark:bg-purple-900/40 px-1.5 py-0.5 rounded-full">40</span>
                            ) : (
                              <div className="w-4 h-4 rounded-full bg-zinc-400 dark:bg-zinc-600 flex items-center justify-center">
                                <Lock size={7} className="text-white" />
                              </div>
                            )}
                          </div>
                        )}
                      </button>
                    );
                  })}
                </div>
              </section>

              {/* Card Styles Section */}
              <section>
                <h3 className="text-xs font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-3">
                  Card Styles — 40 pts each
                </h3>
                <div className="grid grid-cols-2 gap-2.5">
                  {CARD_STYLES.map(style => {
                    const isUnlocked = style.price === 0 || (cosmeticUnlocks.cardStyles || []).includes(style.id);
                    const isActive = isUnlocked && settings?.cardStyle === style.id;
                    const affordable = canAfford(style.price);
                    return (
                      <button
                        key={style.id}
                        onClick={() => {
                          if (isUnlocked && updateSetting) {
                            updateSetting('cardStyle', style.id);
                          } else if (!isUnlocked && affordable) {
                            onSpend('unlock-card-style', style.id);
                            if (updateSetting) updateSetting('cardStyle', style.id);
                          }
                        }}
                        disabled={!isUnlocked && !affordable}
                        className={`relative flex flex-col items-center gap-2 p-3 rounded-xl transition-all focus:outline-none focus-visible:outline-none ${
                          isActive
                            ? 'ring-2 ring-emerald-400 bg-emerald-50 dark:bg-emerald-900/20'
                            : isUnlocked
                              ? 'bg-zinc-50 dark:bg-white/[0.04] ring-1 ring-zinc-200 dark:ring-white/[0.06] hover:ring-zinc-300 dark:hover:ring-white/[0.15]'
                              : affordable
                                ? 'bg-zinc-50 dark:bg-white/[0.04] ring-1 ring-zinc-200 dark:ring-white/[0.06] hover:ring-purple-300 dark:hover:ring-purple-600 cursor-pointer'
                                : 'bg-zinc-50 dark:bg-white/[0.04] ring-1 ring-zinc-200 dark:ring-white/[0.06] opacity-50 cursor-not-allowed'
                        }`}
                      >
                        <div className="w-full h-10 rounded-lg border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-800 flex items-center justify-center">
                          <Layers size={14} className="text-zinc-400 dark:text-zinc-500" />
                        </div>
                        <div className="text-center">
                          <p className="text-[10px] font-bold text-zinc-700 dark:text-zinc-200">{style.name}</p>
                          <p className="text-[9px] text-zinc-400 dark:text-zinc-500">{style.description}</p>
                        </div>
                        {isActive && (
                          <div className="absolute top-1 right-1 w-4 h-4 rounded-full bg-emerald-500 flex items-center justify-center">
                            <Check size={8} className="text-white" />
                          </div>
                        )}
                        {!isUnlocked && (
                          <div className="absolute top-1 right-1">
                            {affordable ? (
                              <span className="text-[8px] font-bold text-purple-600 dark:text-purple-400 bg-purple-100 dark:bg-purple-900/40 px-1.5 py-0.5 rounded-full">40</span>
                            ) : (
                              <div className="w-4 h-4 rounded-full bg-zinc-400 dark:bg-zinc-600 flex items-center justify-center">
                                <Lock size={7} className="text-white" />
                              </div>
                            )}
                          </div>
                        )}
                      </button>
                    );
                  })}
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
