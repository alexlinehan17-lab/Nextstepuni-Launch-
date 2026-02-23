/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect } from 'react';
import { createPortal } from 'react-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Check, Lock } from 'lucide-react';
import { AVATAR_SEEDS, getAvatarUrl } from './Auth';
import { EXTRA_AVATAR_SEEDS } from './RewardShopModal';
import { UserSettings } from '../types';
import { ACCENT_THEME_LIST, CARD_STYLES } from '../themeData';

const MotionDiv = motion.div as any;

interface SettingsModalProps {
  isOpen: boolean;
  onClose: () => void;
  settings: UserSettings;
  updateSetting: <K extends keyof UserSettings>(key: K, value: UserSettings[K]) => void;
  unlockedAvatarSeeds?: string[];
  unlockedThemes?: string[];
  unlockedCardStyles?: string[];
}

const SettingsModal: React.FC<SettingsModalProps> = ({ isOpen, onClose, settings, updateSetting, unlockedAvatarSeeds = [], unlockedThemes = [], unlockedCardStyles = [] }) => {
  const [showSaved, setShowSaved] = useState(false);

  const flash = () => {
    setShowSaved(true);
    setTimeout(() => setShowSaved(false), 1200);
  };

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
            className="relative bg-white dark:bg-zinc-900 border border-zinc-200/50 dark:border-white/[0.08] rounded-2xl w-full max-w-md shadow-[0_24px_64px_rgba(0,0,0,0.12)] dark:shadow-[0_24px_64px_rgba(0,0,0,0.5)] overflow-hidden max-h-[90vh] overflow-y-auto"
            onClick={(e: React.MouseEvent) => e.stopPropagation()}
          >
            {/* Header */}
            <div className="flex items-center justify-between p-6 pb-0">
              <h2 className="font-sans text-xl font-semibold text-zinc-900 dark:text-white tracking-tight">
                Settings
              </h2>
              <div className="flex items-center gap-3">
                <AnimatePresence>
                  {showSaved && (
                    <MotionDiv
                      initial={{ opacity: 0, x: 10 }}
                      animate={{ opacity: 1, x: 0 }}
                      exit={{ opacity: 0, x: 10 }}
                      className="flex items-center gap-1 text-emerald-500 text-xs font-medium"
                    >
                      <Check size={14} />
                      Saved!
                    </MotionDiv>
                  )}
                </AnimatePresence>
                <button
                  onClick={onClose}
                  className="text-zinc-400 dark:text-white/25 hover:text-zinc-600 dark:hover:text-white/50 transition-colors"
                >
                  <X size={18} />
                </button>
              </div>
            </div>

            <div className="p-6 space-y-8">
              {/* Avatar */}
              <section>
                <h3 className="text-xs font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-3">
                  Avatar
                </h3>
                <div className="grid grid-cols-4 gap-2.5">
                  {AVATAR_SEEDS.map(seed => (
                    <button
                      key={seed}
                      onClick={() => {
                        updateSetting('avatar', seed);
                        flash();
                      }}
                      className={`rounded-xl aspect-square p-1.5 transition-all ${
                        settings.avatar === seed
                          ? 'ring-2 ring-[var(--accent-hex)] bg-[rgba(var(--accent),0.1)]'
                          : 'bg-zinc-50 dark:bg-white/[0.04] ring-1 ring-zinc-200 dark:ring-white/[0.06] hover:ring-zinc-300 dark:hover:ring-white/[0.15]'
                      }`}
                    >
                      <img src={getAvatarUrl(seed)} alt={seed} className="w-full h-full rounded-lg" />
                    </button>
                  ))}
                  {EXTRA_AVATAR_SEEDS.map(seed => {
                    const isUnlocked = unlockedAvatarSeeds.includes(seed);
                    return (
                      <div key={seed} className="relative" title={isUnlocked ? seed : 'Unlock in Reward Shop'}>
                        <button
                          onClick={() => {
                            if (isUnlocked) {
                              updateSetting('avatar', seed);
                              flash();
                            }
                          }}
                          disabled={!isUnlocked}
                          className={`w-full rounded-xl aspect-square p-1.5 transition-all ${
                            isUnlocked
                              ? settings.avatar === seed
                                ? 'ring-2 ring-[var(--accent-hex)] bg-[rgba(var(--accent),0.1)]'
                                : 'bg-zinc-50 dark:bg-white/[0.04] ring-1 ring-zinc-200 dark:ring-white/[0.06] hover:ring-zinc-300 dark:hover:ring-white/[0.15]'
                              : 'bg-zinc-50 dark:bg-white/[0.04] ring-1 ring-zinc-200 dark:ring-white/[0.06] cursor-not-allowed'
                          }`}
                        >
                          <img
                            src={getAvatarUrl(seed)}
                            alt={seed}
                            className={`w-full h-full rounded-lg ${!isUnlocked ? 'grayscale opacity-30' : ''}`}
                          />
                        </button>
                        {!isUnlocked && (
                          <div className="absolute bottom-0.5 right-0.5 w-4 h-4 rounded-full bg-zinc-400 dark:bg-zinc-600 flex items-center justify-center">
                            <Lock size={8} className="text-white" />
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              </section>

              {/* Default Timer Duration */}
              <section>
                <h3 className="text-xs font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-3">
                  Default Timer Duration
                </h3>
                <div className="flex gap-2">
                  {[25, 50].map(mins => (
                    <button
                      key={mins}
                      onClick={() => {
                        updateSetting('defaultWorkMinutes', mins);
                        flash();
                      }}
                      className={`px-5 py-2.5 rounded-xl text-sm font-medium transition-all ${
                        settings.defaultWorkMinutes === mins
                          ? 'bg-[rgba(var(--accent),0.1)] text-[var(--accent-hex)] ring-2 ring-[var(--accent-hex)]'
                          : 'bg-zinc-50 dark:bg-white/[0.04] text-zinc-700 dark:text-zinc-300 ring-1 ring-zinc-200 dark:ring-white/[0.06] hover:ring-zinc-300 dark:hover:ring-white/[0.15]'
                      }`}
                    >
                      {`${mins} minutes`}
                    </button>
                  ))}
                </div>
              </section>

              {/* Accent Theme */}
              <section>
                <h3 className="text-xs font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-3">
                  Accent Theme
                </h3>
                <div className="grid grid-cols-4 gap-2.5">
                  {ACCENT_THEME_LIST.map(theme => {
                    const isUnlocked = theme.price === 0 || unlockedThemes.includes(theme.id);
                    const isActive = isUnlocked && settings.accentTheme === theme.id;
                    return (
                      <button
                        key={theme.id}
                        onClick={() => {
                          if (isUnlocked) {
                            updateSetting('accentTheme', theme.id);
                            flash();
                          }
                        }}
                        disabled={!isUnlocked}
                        title={isUnlocked ? theme.name : 'Unlock in Reward Shop'}
                        className={`flex flex-col items-center gap-1.5 p-2 rounded-xl transition-all ${
                          isActive
                            ? 'ring-2 ring-[var(--accent-hex)] bg-[rgba(var(--accent),0.1)]'
                            : isUnlocked
                              ? 'bg-zinc-50 dark:bg-white/[0.04] ring-1 ring-zinc-200 dark:ring-white/[0.06] hover:ring-zinc-300 dark:hover:ring-white/[0.15]'
                              : 'bg-zinc-50 dark:bg-white/[0.04] ring-1 ring-zinc-200 dark:ring-white/[0.06] opacity-50 cursor-not-allowed'
                        }`}
                      >
                        <div className="relative">
                          <div
                            className="w-7 h-7 rounded-full border-2 border-white dark:border-zinc-800 shadow-sm"
                            style={{ backgroundColor: theme.hex }}
                          />
                          {!isUnlocked && (
                            <div className="absolute -bottom-0.5 -right-0.5 w-3.5 h-3.5 rounded-full bg-zinc-400 dark:bg-zinc-600 flex items-center justify-center">
                              <Lock size={7} className="text-white" />
                            </div>
                          )}
                        </div>
                        <p className="text-[9px] font-bold text-zinc-500 dark:text-zinc-400 text-center leading-tight">{theme.name}</p>
                      </button>
                    );
                  })}
                </div>
              </section>

              {/* Card Style */}
              <section>
                <h3 className="text-xs font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-3">
                  Card Style
                </h3>
                <div className="grid grid-cols-3 gap-2">
                  {CARD_STYLES.map(style => {
                    const isUnlocked = style.price === 0 || unlockedCardStyles.includes(style.id);
                    const isActive = isUnlocked && settings.cardStyle === style.id;
                    return (
                      <button
                        key={style.id}
                        onClick={() => {
                          if (isUnlocked) {
                            updateSetting('cardStyle', style.id);
                            flash();
                          }
                        }}
                        disabled={!isUnlocked}
                        title={isUnlocked ? style.name : 'Unlock in Reward Shop'}
                        className={`relative flex flex-col items-center gap-1.5 p-2.5 rounded-xl transition-all ${
                          isActive
                            ? 'ring-2 ring-[var(--accent-hex)] bg-[rgba(var(--accent),0.1)]'
                            : isUnlocked
                              ? 'bg-zinc-50 dark:bg-white/[0.04] ring-1 ring-zinc-200 dark:ring-white/[0.06] hover:ring-zinc-300 dark:hover:ring-white/[0.15]'
                              : 'bg-zinc-50 dark:bg-white/[0.04] ring-1 ring-zinc-200 dark:ring-white/[0.06] opacity-50 cursor-not-allowed'
                        }`}
                      >
                        <p className="text-[10px] font-bold text-zinc-700 dark:text-zinc-200">{style.name}</p>
                        <p className="text-[9px] text-zinc-400 dark:text-zinc-500 text-center">{style.description}</p>
                        {!isUnlocked && (
                          <div className="absolute top-1 right-1 w-3.5 h-3.5 rounded-full bg-zinc-400 dark:bg-zinc-600 flex items-center justify-center">
                            <Lock size={7} className="text-white" />
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

export default SettingsModal;
