
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Sun, Moon, LogOut, Settings, Flame, ChevronRight, Trophy, Award, BarChart3, Star, X, BookOpen, CalendarRange, HelpCircle, MessageSquare } from 'lucide-react';
import { type SessionUser, getAvatarUrl, handleAvatarError } from '../utils/authUtils';
import { type UserSettings } from '../types';
import { type StreakData } from '../hooks/useStreak';
import { type FocusRecommendation } from '../hooks/useTodaysFocus';
import { useModal } from '../hooks/useModal';
import NotificationBell from './NotificationBell';

const streakLabel = (count: number): string => `${count} ${count === 1 ? 'day' : 'days'} streak`;

interface UserProfileProps {
  user: SessionUser;
  onLogout: () => void;
  settings: UserSettings;
  updateSetting: <K extends keyof UserSettings>(key: K, value: UserSettings[K]) => void;
  onOpenSettings: () => void;
  avatarOverride: string;
  streak: StreakData;
  recommendation: FocusRecommendation | null;
  onSelectModule: (moduleId: string) => void;
  onOpenPassport: () => void;
  onGoToDashboard: () => void;
  completedCount: number;
  totalCount: number;
  onOpenNorthStar: () => void;
  hasNorthStar: boolean;
  unlockedThemes: string[];
}

export const UserProfile: React.FC<UserProfileProps> = ({ user, onLogout, settings, updateSetting, onOpenSettings, avatarOverride, streak, recommendation, onSelectModule, onOpenPassport, onGoToDashboard, completedCount, totalCount, onOpenNorthStar, hasNorthStar, unlockedThemes: _unlockedThemes }) => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const displayAvatar = avatarOverride || user.avatar;

  useEffect(() => {
    if (!isOpen) return;
    const handleClickOutside = (e: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [isOpen]);

  return (
    <div className="relative" ref={dropdownRef}>
      <button onClick={() => setIsOpen(!isOpen)} className="flex items-center gap-2 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[rgba(var(--accent),0.5)] rounded-full">
        <img src={getAvatarUrl(displayAvatar)} alt="User Avatar" className="w-12 h-12 rounded-full bg-zinc-200" onError={(e) => handleAvatarError(e, displayAvatar)} />
      </button>
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: -10, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -10, scale: 0.95 }}
            className="absolute top-full right-0 mt-2 w-72 bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-xl shadow-lg p-4 max-h-[80vh] overflow-y-auto"
          >
            {/* User info */}
            <div className="flex items-center gap-3 border-b border-zinc-200/50 dark:border-white/10 pb-3 mb-3">
              <img src={getAvatarUrl(displayAvatar)} alt="User Avatar" className="w-12 h-12 rounded-full bg-zinc-200" onError={(e) => handleAvatarError(e, displayAvatar)} />
              <div>
                <p className="font-bold text-zinc-800 dark:text-white">{user.name}</p>
                <p className="text-xs text-zinc-500">{user.isAdmin ? 'Admin' : 'Student'}</p>
              </div>
            </div>

            {/* Study Streak */}
            <div className="flex items-center gap-3 p-2 mb-1">
              <div className="w-8 h-8 rounded-lg bg-orange-50 dark:bg-orange-500/10 flex items-center justify-center">
                <Flame size={16} className="text-orange-500" />
              </div>
              <div className="flex-1">
                <p className="text-sm font-semibold text-zinc-800 dark:text-white">
                  {streakLabel(streak.currentStreak)}
                </p>
                {streak.longestStreak > 1 && (
                  <p className="text-[10px] text-zinc-400 dark:text-zinc-500">
                    Longest: {streak.longestStreak} days
                  </p>
                )}
              </div>
            </div>

            {/* Today's Focus */}
            <div className="border-t border-zinc-200/50 dark:border-white/10 pt-3 mt-2 mb-2">
              <p className="text-[10px] font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 px-2 mb-2">Today's Focus</p>
              {recommendation && recommendation.reason !== 'all-complete' ? (
                <button
                  onClick={() => { setIsOpen(false); onSelectModule(recommendation.moduleId); }}
                  className="w-full flex items-center justify-between p-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-white/5 group"
                >
                  <p className="text-sm font-medium text-zinc-700 dark:text-zinc-300 text-left line-clamp-1 pr-2">{recommendation.title}</p>
                  <ChevronRight size={14} className="text-zinc-400 dark:text-zinc-500 shrink-0 group-hover:translate-x-0.5 transition-transform" />
                </button>
              ) : (
                <div className="flex items-center gap-2 p-2">
                  <Trophy size={14} className="text-amber-500" />
                  <p className="text-sm font-medium text-amber-600 dark:text-amber-400">All modules complete!</p>
                </div>
              )}
            </div>

            {/* My Progress + Study Passport */}
            <div className="border-t border-zinc-200/50 dark:border-white/10 pt-2 mt-2 mb-2">
              <button
                onClick={() => { setIsOpen(false); onGoToDashboard(); }}
                className="w-full flex items-center gap-3 p-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-white/5"
              >
                <div className="w-8 h-8 rounded-lg bg-[rgba(var(--accent),0.1)] flex items-center justify-center">
                  <BarChart3 size={16} className="text-[var(--accent-hex)]" />
                </div>
                <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300 flex-1 text-left">My Progress</span>
              </button>
              <button
                onClick={() => { setIsOpen(false); onOpenPassport(); }}
                className="w-full flex items-center gap-3 p-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-white/5"
              >
                <div className="w-8 h-8 rounded-lg bg-[rgba(var(--accent),0.1)] dark:bg-[rgba(var(--accent),0.1)] flex items-center justify-center">
                  <Award size={16} className="text-[var(--accent-hex)]" />
                </div>
                <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300 flex-1 text-left">Study Passport</span>
                <span className="text-xs font-bold text-zinc-400 dark:text-zinc-500">{completedCount}/{totalCount}</span>
              </button>
            </div>

            {/* North Star + Theme, Settings, Log Out */}
            <div className="border-t border-zinc-200/50 dark:border-white/10 pt-2 mt-2">
              {hasNorthStar && (
                <button
                  onClick={() => { setIsOpen(false); onOpenNorthStar(); }}
                  className="w-full flex items-center gap-3 p-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-white/5"
                >
                  <div className="w-8 h-8 rounded-lg bg-amber-50 dark:bg-amber-500/10 flex items-center justify-center">
                    <Star size={16} className="text-amber-500" />
                  </div>
                  <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300 flex-1 text-left">My North Star</span>
                </button>
              )}
              <button role="switch" aria-checked={settings.darkMode} onClick={() => updateSetting('darkMode', !settings.darkMode)} className="w-full flex items-center justify-between p-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-white/5">
                  <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300">{settings.darkMode ? 'Light Mode (Beta)' : 'Dark Mode (Beta)'}</span>
                   <AnimatePresence mode="wait">
                      {settings.darkMode ? (
                        <motion.div key="sun" initial={{ rotate: -90, opacity: 0 }} animate={{ rotate: 0, opacity: 1 }} exit={{ rotate: 90, opacity: 0 }} transition={{ duration: 0.2 }}>
                          <Sun size={16} className="text-amber-400" />
                        </motion.div>
                      ) : (
                        <motion.div key="moon" initial={{ rotate: -90, opacity: 0 }} animate={{ rotate: 0, opacity: 1 }} exit={{ rotate: 90, opacity: 0 }} transition={{ duration: 0.2 }}>
                          <Moon size={16} className="text-zinc-600" />
                        </motion.div>
                      )}
                  </AnimatePresence>
              </button>
              <button onClick={() => { setIsOpen(false); onOpenSettings(); }} className="w-full flex items-center gap-2 p-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-white/5 mt-1">
                <Settings size={16} className="text-zinc-500" />
                <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300">Settings</span>
              </button>
              <button onClick={onLogout} className="w-full flex items-center gap-2 p-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-white/5 mt-1">
                <LogOut size={16} className="text-rose-500" />
                <span className="text-sm font-medium text-rose-500">Log Out</span>
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

interface MobileProfileSheetProps {
  isOpen: boolean;
  onClose: () => void;
  user: SessionUser;
  onLogout: () => void;
  settings: UserSettings;
  updateSetting: <K extends keyof UserSettings>(key: K, value: UserSettings[K]) => void;
  onOpenSettings: () => void;
  avatarOverride: string;
  streak: StreakData;
  recommendation: FocusRecommendation | null;
  onSelectModule: (moduleId: string) => void;
  onOpenPassport: () => void;
  onGoToDashboard: () => void;
  onGoToInsights: () => void;
  onGoToReferences: () => void;
  onGoToYearPlans: () => void;
  onOpenSiteGuide: () => void;
  onOpenFeedback: () => void;
  completedCount: number;
  totalCount: number;
  onOpenNorthStar: () => void;
  hasNorthStar: boolean;
  unlockedThemes: string[];
}

export const MobileProfileSheet: React.FC<MobileProfileSheetProps> = ({ isOpen, onClose, user, onLogout, settings, updateSetting, onOpenSettings, avatarOverride, streak, recommendation, onSelectModule, onOpenPassport, onGoToDashboard, onGoToInsights: _onGoToInsights, onGoToReferences, onGoToYearPlans, onOpenSiteGuide, onOpenFeedback, completedCount, totalCount, onOpenNorthStar, hasNorthStar, unlockedThemes: _unlockedThemes }) => {
  const displayAvatar = avatarOverride || user.avatar;
  const sheetRef = useRef<HTMLDivElement>(null);
  useModal(isOpen, onClose, sheetRef);
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            key="profile-backdrop"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 z-[95] bg-black/40 md:hidden"
          />
          {/* Sheet */}
          <motion.div
            ref={sheetRef}
            key="profile-sheet"
            initial={{ y: '100%' }}
            animate={{ y: 0 }}
            exit={{ y: '100%' }}
            transition={{ type: 'spring', damping: 28, stiffness: 300 }}
            role="dialog"
            aria-modal="true"
            aria-labelledby="mobile-profile-title"
            tabIndex={-1}
            className="fixed bottom-0 left-0 right-0 z-[96] md:hidden bg-white dark:bg-zinc-900 rounded-t-2xl border-t border-zinc-200 dark:border-zinc-800 max-h-[85vh] overflow-y-auto"
            style={{ paddingBottom: 'var(--sab, 0px)' }}
          >
            {/* Drag handle */}
            <div className="flex justify-center pt-3 pb-2">
              <div className="w-10 h-1 rounded-full bg-zinc-300 dark:bg-zinc-700" />
            </div>

            <div className="px-5 pb-6">
              {/* User info */}
              <div className="sticky top-0 z-10 -mx-5 mb-4 flex items-center justify-between border-b border-zinc-100 bg-white/95 px-5 py-3 backdrop-blur-xl dark:border-zinc-800 dark:bg-zinc-900/95">
                <div className="flex items-center gap-3">
                  <img src={getAvatarUrl(displayAvatar)} alt="Avatar" className="w-12 h-12 rounded-full bg-zinc-200" onError={(e) => handleAvatarError(e, displayAvatar)} />
                  <div>
                    <h2 id="mobile-profile-title" className="font-bold text-zinc-800 dark:text-white">{user.name}</h2>
                    <p className="text-xs text-zinc-500">Student</p>
                  </div>
                </div>
                <button onClick={onClose} aria-label="Close profile" className="flex h-11 w-11 items-center justify-center rounded-xl hover:bg-zinc-100 dark:hover:bg-zinc-800">
                  <X size={18} className="text-zinc-400" />
                </button>
              </div>

              {/* Streak */}
              <div className="flex items-center gap-3 p-3 rounded-xl bg-zinc-50 dark:bg-zinc-800/50 mb-3">
                <div className="w-8 h-8 rounded-lg bg-orange-50 dark:bg-orange-500/10 flex items-center justify-center">
                  <Flame size={16} className="text-orange-500" />
                </div>
                <div className="flex-1">
                  <p className="text-sm font-semibold text-zinc-800 dark:text-white">{streakLabel(streak.currentStreak)}</p>
                  {streak.longestStreak > 1 && (
                    <p className="text-[10px] text-zinc-400 dark:text-zinc-500">Longest: {streak.longestStreak} days</p>
                  )}
                </div>
              </div>

              {/* Today's Focus */}
              <div className="mb-3">
                <p className="text-[10px] font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 px-1 mb-2">Today's Focus</p>
                {recommendation && recommendation.reason !== 'all-complete' ? (
                  <button
                    onClick={() => { onClose(); onSelectModule(recommendation.moduleId); }}
                    className="w-full flex items-center justify-between p-3 rounded-xl bg-zinc-50 dark:bg-zinc-800/50 group"
                  >
                    <p className="text-sm font-medium text-zinc-700 dark:text-zinc-300 text-left line-clamp-1 pr-2">{recommendation.title}</p>
                    <ChevronRight size={14} className="text-zinc-400 dark:text-zinc-500 shrink-0" />
                  </button>
                ) : (
                  <div className="flex items-center gap-2 p-3 rounded-xl bg-zinc-50 dark:bg-zinc-800/50">
                    <Trophy size={14} className="text-amber-500" />
                    <p className="text-sm font-medium text-amber-600 dark:text-amber-400">All modules complete!</p>
                  </div>
                )}
              </div>

              {/* Grouped actions keep the sheet scannable as the app grows. */}
              <div className="space-y-5">
                <section aria-labelledby="profile-learning-heading">
                  <p id="profile-learning-heading" className="mb-1 px-1 text-[10px] font-semibold uppercase tracking-[0.16em] text-zinc-400 dark:text-zinc-500">Learning</p>
                  <div className="divide-y divide-zinc-100 rounded-2xl border border-zinc-200 dark:divide-zinc-800 dark:border-zinc-700">
                    <button onClick={() => { onClose(); onGoToDashboard(); }} className="flex min-h-14 w-full items-center gap-3 px-3 text-left hover:bg-zinc-50 dark:hover:bg-zinc-800/50">
                      <div className="flex h-8 w-8 items-center justify-center rounded-lg border border-zinc-200 dark:border-zinc-700"><BarChart3 size={16} className="text-[var(--accent-hex)]" /></div>
                      <span className="flex-1 text-sm font-medium text-zinc-700 dark:text-zinc-300">My Progress</span>
                    </button>
                    <button onClick={() => { onClose(); onOpenPassport(); }} className="flex min-h-14 w-full items-center gap-3 px-3 text-left hover:bg-zinc-50 dark:hover:bg-zinc-800/50">
                      <div className="flex h-8 w-8 items-center justify-center rounded-lg border border-zinc-200 dark:border-zinc-700"><Award size={16} className="text-[var(--accent-hex)]" /></div>
                      <span className="flex-1 text-sm font-medium text-zinc-700 dark:text-zinc-300">Study Passport</span>
                      <span className="text-xs font-bold text-zinc-400 dark:text-zinc-500">{completedCount}/{totalCount}</span>
                    </button>
                    <button onClick={() => { onClose(); onGoToYearPlans(); }} className="flex min-h-14 w-full items-center gap-3 px-3 text-left hover:bg-zinc-50 dark:hover:bg-zinc-800/50">
                      <div className="flex h-8 w-8 items-center justify-center rounded-lg border border-zinc-200 dark:border-zinc-700"><CalendarRange size={16} className="text-zinc-500" /></div>
                      <span className="flex-1 text-sm font-medium text-zinc-700 dark:text-zinc-300">Year Plans</span>
                    </button>
                  </div>
                </section>

                <section aria-labelledby="profile-direction-heading">
                  <p id="profile-direction-heading" className="mb-1 px-1 text-[10px] font-semibold uppercase tracking-[0.16em] text-zinc-400 dark:text-zinc-500">Direction</p>
                  <div className="divide-y divide-zinc-100 rounded-2xl border border-zinc-200 dark:divide-zinc-800 dark:border-zinc-700">
                    {hasNorthStar && (
                      <button onClick={() => { onClose(); onOpenNorthStar(); }} className="flex min-h-14 w-full items-center gap-3 px-3 text-left hover:bg-zinc-50 dark:hover:bg-zinc-800/50">
                        <div className="flex h-8 w-8 items-center justify-center rounded-lg border border-zinc-200 dark:border-zinc-700"><Star size={16} className="text-amber-500" /></div>
                        <span className="flex-1 text-sm font-medium text-zinc-700 dark:text-zinc-300">My North Star</span>
                      </button>
                    )}
                    <button onClick={() => { onClose(); onGoToReferences(); }} className="flex min-h-14 w-full items-center gap-3 px-3 text-left hover:bg-zinc-50 dark:hover:bg-zinc-800/50">
                      <div className="flex h-8 w-8 items-center justify-center rounded-lg border border-zinc-200 dark:border-zinc-700"><BookOpen size={16} className="text-zinc-500" /></div>
                      <span className="flex-1 text-sm font-medium text-zinc-700 dark:text-zinc-300">References</span>
                    </button>
                  </div>
                </section>

                <section aria-labelledby="profile-support-heading">
                  <p id="profile-support-heading" className="mb-1 px-1 text-[10px] font-semibold uppercase tracking-[0.16em] text-zinc-400 dark:text-zinc-500">Support</p>
                  <div className="divide-y divide-zinc-100 rounded-2xl border border-zinc-200 dark:divide-zinc-800 dark:border-zinc-700">
                    <NotificationBell uid={user.uid} variant="menu" />
                    <button onClick={() => { onClose(); onOpenSiteGuide(); }} className="flex min-h-14 w-full items-center gap-3 px-3 text-left hover:bg-zinc-50 dark:hover:bg-zinc-800/50">
                      <div className="flex h-8 w-8 items-center justify-center rounded-lg border border-zinc-200 dark:border-zinc-700"><HelpCircle size={16} className="text-[#F26B1F]" /></div>
                      <span className="flex-1 text-sm font-medium text-zinc-700 dark:text-zinc-300">How the app works</span>
                    </button>
                    <button onClick={() => { onClose(); onOpenFeedback(); }} className="flex min-h-14 w-full items-center gap-3 px-3 text-left hover:bg-zinc-50 dark:hover:bg-zinc-800/50">
                      <div className="flex h-8 w-8 items-center justify-center rounded-lg border border-zinc-200 dark:border-zinc-700"><MessageSquare size={16} className="text-zinc-500" /></div>
                      <span className="flex-1 text-sm font-medium text-zinc-700 dark:text-zinc-300">Help us improve</span>
                    </button>
                  </div>
                </section>

                <section aria-labelledby="profile-account-heading">
                  <p id="profile-account-heading" className="mb-1 px-1 text-[10px] font-semibold uppercase tracking-[0.16em] text-zinc-400 dark:text-zinc-500">Account</p>
                  <div className="divide-y divide-zinc-100 rounded-2xl border border-zinc-200 dark:divide-zinc-800 dark:border-zinc-700">
                    <button role="switch" aria-checked={settings.darkMode} onClick={() => updateSetting('darkMode', !settings.darkMode)} className="flex min-h-14 w-full items-center gap-3 px-3 text-left hover:bg-zinc-50 dark:hover:bg-zinc-800/50">
                      <div className="flex h-8 w-8 items-center justify-center rounded-lg border border-zinc-200 dark:border-zinc-700">{settings.darkMode ? <Sun size={16} className="text-amber-400" /> : <Moon size={16} className="text-zinc-600 dark:text-zinc-300" />}</div>
                      <span className="flex-1 text-sm font-medium text-zinc-700 dark:text-zinc-300">{settings.darkMode ? 'Light Mode (Beta)' : 'Dark Mode (Beta)'}</span>
                    </button>
                    <button onClick={() => { onClose(); onOpenSettings(); }} className="flex min-h-14 w-full items-center gap-3 px-3 text-left hover:bg-zinc-50 dark:hover:bg-zinc-800/50">
                      <div className="flex h-8 w-8 items-center justify-center rounded-lg border border-zinc-200 dark:border-zinc-700"><Settings size={16} className="text-zinc-500" /></div>
                      <span className="flex-1 text-sm font-medium text-zinc-700 dark:text-zinc-300">Settings</span>
                    </button>
                    <button onClick={() => { onClose(); onLogout(); }} className="flex min-h-14 w-full items-center gap-3 px-3 text-left hover:bg-zinc-50 dark:hover:bg-zinc-800/50">
                      <div className="flex h-8 w-8 items-center justify-center rounded-lg border border-rose-200 dark:border-rose-900"><LogOut size={16} className="text-rose-500" /></div>
                      <span className="flex-1 text-sm font-medium text-rose-500">Log Out</span>
                    </button>
                  </div>
                </section>
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
};
