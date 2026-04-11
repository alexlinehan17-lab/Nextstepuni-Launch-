/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useRef } from 'react';
import { createPortal } from 'react-dom';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { X, Check, Lock, Sun, Moon, RefreshCw, LogOut, ChevronRight, Compass } from 'lucide-react';
import { AVATAR_SEEDS, getAvatarUrl } from './Auth';
import { EXTRA_AVATAR_SEEDS } from './RewardShopModal';
import { type UserSettings } from '../types';

interface SettingsModalProps {
  isOpen: boolean;
  onClose: () => void;
  settings: UserSettings;
  updateSetting: <K extends keyof UserSettings>(key: K, value: UserSettings[K]) => void;
  unlockedAvatarSeeds?: string[];
  unlockedThemes?: string[];
  unlockedCardStyles?: string[];
  userName?: string;
  userSchool?: string;
  onChangeSubjects?: () => void;
  onResetNorthStar?: () => void;
  onLogout?: () => void;
}

const SettingsModal: React.FC<SettingsModalProps> = ({
  isOpen, onClose, settings, updateSetting,
  unlockedAvatarSeeds = [], _unlockedThemes = [], _unlockedCardStyles = [],
  userName, userSchool, onChangeSubjects, onResetNorthStar, onLogout,
}) => {
  const [showSaved, setShowSaved] = useState(false);
  const flashTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    return () => {
      if (flashTimerRef.current) clearTimeout(flashTimerRef.current);
    };
  }, []);

  const flash = () => {
    setShowSaved(true);
    flashTimerRef.current = setTimeout(() => setShowSaved(false), 1200);
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

            <div className="p-6 space-y-6">
              {/* Account */}
              {(userName || userSchool) && (
                <section>
                  <h3 className="text-xs font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-3">
                    Account
                  </h3>
                  <div className="p-3 rounded-xl bg-zinc-50 dark:bg-white/[0.04] ring-1 ring-zinc-200 dark:ring-white/[0.06]">
                    {userName && <p className="text-sm font-medium text-zinc-700 dark:text-zinc-200">{userName}</p>}
                    {userSchool && <p className="text-[11px] text-zinc-400 dark:text-zinc-500 mt-0.5">{userSchool}</p>}
                  </div>
                </section>
              )}

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

              {/* Preferences */}
              <section>
                <h3 className="text-xs font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-3">
                  Preferences
                </h3>
                <div className="space-y-2">
                  {/* Dark Mode */}
                  <button
                    onClick={() => {
                      updateSetting('darkMode', !settings.darkMode);
                      flash();
                    }}
                    className="w-full flex items-center justify-between p-3 rounded-xl bg-zinc-50 dark:bg-white/[0.04] ring-1 ring-zinc-200 dark:ring-white/[0.06] hover:ring-zinc-300 dark:hover:ring-white/[0.15] transition-all"
                  >
                    <div className="flex items-center gap-3">
                      {settings.darkMode ? <Sun size={16} className="text-amber-400" /> : <Moon size={16} className="text-zinc-500" />}
                      <p className="text-sm font-medium text-zinc-700 dark:text-zinc-200">{settings.darkMode ? 'Light Mode' : 'Dark Mode'}</p>
                    </div>
                    <div className={`relative w-10 h-6 rounded-full transition-colors ${
                      settings.darkMode ? 'bg-[var(--accent-hex)]' : 'bg-zinc-300 dark:bg-zinc-600'
                    }`}>
                      <div className={`absolute top-0.5 w-5 h-5 rounded-full bg-white shadow-sm transition-transform ${
                        settings.darkMode ? 'translate-x-[18px]' : 'translate-x-0.5'
                      }`} />
                    </div>
                  </button>

                  {/* Dashboard toggle */}
                  <button
                    onClick={() => {
                      updateSetting('showDashboard', settings.showDashboard === false ? true : false);
                      flash();
                    }}
                    className="w-full flex items-center justify-between p-3 rounded-xl bg-zinc-50 dark:bg-white/[0.04] ring-1 ring-zinc-200 dark:ring-white/[0.06] hover:ring-zinc-300 dark:hover:ring-white/[0.15] transition-all"
                  >
                    <div className="flex-1 text-left">
                      <p className="text-sm font-medium text-zinc-700 dark:text-zinc-200">Show home dashboard</p>
                      <p className="text-[10px] text-zinc-400 dark:text-zinc-500 mt-0.5">Today's plan and progress above modules</p>
                    </div>
                    <div className={`relative w-10 h-6 rounded-full transition-colors ${
                      settings.showDashboard !== false ? 'bg-[var(--accent-hex)]' : 'bg-zinc-300 dark:bg-zinc-600'
                    }`}>
                      <div className={`absolute top-0.5 w-5 h-5 rounded-full bg-white shadow-sm transition-transform ${
                        settings.showDashboard !== false ? 'translate-x-[18px]' : 'translate-x-0.5'
                      }`} />
                    </div>
                  </button>

                  {/* Flares toggle */}
                  <button
                    onClick={() => {
                      updateSetting('flaresToggle', settings.flaresToggle === false ? true : false);
                      flash();
                    }}
                    className="w-full flex items-center justify-between p-3 rounded-xl bg-zinc-50 dark:bg-white/[0.04] ring-1 ring-zinc-200 dark:ring-white/[0.06] hover:ring-zinc-300 dark:hover:ring-white/[0.15] transition-all"
                  >
                    <div className="flex-1 text-left">
                      <p className="text-sm font-medium text-zinc-700 dark:text-zinc-200">SOS Flares</p>
                      <p className="text-[10px] text-zinc-400 dark:text-zinc-500 mt-0.5">See when classmates need help</p>
                    </div>
                    <div className={`relative w-10 h-6 rounded-full transition-colors ${
                      settings.flaresToggle !== false ? 'bg-[var(--accent-hex)]' : 'bg-zinc-300 dark:bg-zinc-600'
                    }`}>
                      <div className={`absolute top-0.5 w-5 h-5 rounded-full bg-white shadow-sm transition-transform ${
                        settings.flaresToggle !== false ? 'translate-x-[18px]' : 'translate-x-0.5'
                      }`} />
                    </div>
                  </button>
                </div>
              </section>

              {/* Actions */}
              <section>
                <h3 className="text-xs font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-3">
                  Actions
                </h3>
                <div className="space-y-1">
                  {onChangeSubjects && (
                    <button
                      onClick={() => { onClose(); onChangeSubjects(); }}
                      className="w-full flex items-center justify-between p-3 rounded-xl hover:bg-zinc-50 dark:hover:bg-white/[0.04] transition-colors"
                    >
                      <div className="flex items-center gap-3">
                        <RefreshCw size={16} className="text-zinc-400" />
                        <p className="text-sm font-medium text-zinc-700 dark:text-zinc-200">Change Subjects</p>
                      </div>
                      <ChevronRight size={14} className="text-zinc-300 dark:text-zinc-600" />
                    </button>
                  )}
                  {onResetNorthStar && (
                    <button
                      onClick={() => { onClose(); onResetNorthStar(); }}
                      className="w-full flex items-center justify-between p-3 rounded-xl hover:bg-zinc-50 dark:hover:bg-white/[0.04] transition-colors"
                    >
                      <div className="flex items-center gap-3">
                        <Compass size={16} className="text-zinc-400" />
                        <p className="text-sm font-medium text-zinc-700 dark:text-zinc-200">Edit North Star</p>
                      </div>
                      <ChevronRight size={14} className="text-zinc-300 dark:text-zinc-600" />
                    </button>
                  )}
                  {onLogout && (
                    <button
                      onClick={() => { onClose(); onLogout(); }}
                      className="w-full flex items-center p-3 rounded-xl hover:bg-zinc-50 dark:hover:bg-white/[0.04] transition-colors"
                    >
                      <div className="flex items-center gap-3">
                        <LogOut size={16} className="text-rose-500" />
                        <p className="text-sm font-medium text-rose-500">Sign Out</p>
                      </div>
                    </button>
                  )}
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
