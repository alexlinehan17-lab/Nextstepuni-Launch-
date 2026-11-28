
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/
import Avatar from './Avatar';

import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Sun, Moon, LogOut, Settings, Flame, ChevronRight, Trophy, Award, BarChart3, Star, BookOpen, CalendarRange, HelpCircle, MessageSquare, SlidersHorizontal, ChartNoAxesColumn, Stamp, Bell } from 'lucide-react';
import { type SessionUser } from '../utils/authUtils';
import { type UserSettings } from '../types';
import { type StreakData } from '../hooks/useStreak';
import { type FocusRecommendation } from '../hooks/useTodaysFocus';
import NotificationBell from './NotificationBell';
import { Sheet } from './ui/Sheet';
import { List, Row } from './ui/List';
import { Switch } from './ui/Choice';
import './account-sheet.css';

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
      <button onClick={() => setIsOpen(!isOpen)} aria-label="Open profile and settings" aria-expanded={isOpen} className="flex items-center gap-2 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[rgba(var(--accent),0.5)] rounded-full">
        <Avatar seed={displayAvatar} alt="User Avatar" className="w-11 h-11 rounded-full bg-zinc-200" />
      </button>
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: -10, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -10, scale: 0.95 }}
            className="absolute top-full right-0 mt-2 w-72 bg-white dark:bg-surface-paper border border-zinc-200 dark:border-hairline rounded-xl shadow-lg p-4 max-h-[80vh] overflow-y-auto"
          >
            {/* User info */}
            <div className="flex items-center gap-3 border-b border-zinc-200/50 dark:border-white/10 pb-3 mb-3">
              <Avatar seed={displayAvatar} alt="User Avatar" className="w-12 h-12 rounded-full bg-zinc-200" />
              <div>
                <p className="font-bold text-zinc-800 dark:text-white">{user.name}</p>
                <p className="text-xs text-zinc-500">{user.isAdmin ? 'Admin' : 'Student'}</p>
              </div>
            </div>

            {/* Study Streak */}
            <div className="flex items-center gap-3 p-2 mb-1">
              <div className="w-8 h-8 rounded-lg bg-orange-50 dark:bg-accent/10 flex items-center justify-center">
                <Flame size={16} className="text-accent" />
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
  /** Everything the student set up in onboarding, with its editors. */
  onGoToYourSetup?: () => void;
  onOpenSiteGuide: () => void;
  onOpenFeedback: () => void;
  onUnreadCountChange?: (count: number) => void;
  completedCount: number;
  totalCount: number;
  onOpenNorthStar: () => void;
  hasNorthStar: boolean;
  unlockedThemes: string[];
}

export const MobileProfileSheet: React.FC<MobileProfileSheetProps> = ({ isOpen, onClose, user, onLogout, settings, updateSetting, onOpenSettings, avatarOverride, streak, recommendation, onSelectModule, onOpenPassport, onGoToDashboard, onGoToInsights: _onGoToInsights, onGoToReferences, onGoToYearPlans, onGoToYourSetup, onOpenSiteGuide, onOpenFeedback, onUnreadCountChange, completedCount, totalCount, onOpenNorthStar, hasNorthStar, unlockedThemes: _unlockedThemes }) => {
  // The account sheet, on a phone (agreed 26 Nov 2026, r5-account-settings):
  // one bottom sheet with Close at the top left, then the student's character
  // and name; the streak on the sheet with no grey box; every row with a bare
  // ink icon and the arrow that says it opens a page. Same rows, groups and
  // order as before. The shared Sheet owns the safe areas, Escape, the scrim
  // and the swipe down.
  const displayAvatar = avatarOverride || user.avatar;
  const go = (action: () => void) => () => { onClose(); action(); };
  const glyph = (Icon: typeof Flame) => <Icon width={20} height={20} strokeWidth={1.75} aria-hidden="true" focusable="false" />;
  return (
    <Sheet
      open={isOpen}
      onClose={onClose}
      closeLabel="Close profile"
      className="acct-sheet"
      title={<span id="mobile-profile-title">{user.name}</span>}
      meta="Student"
      art={<Avatar seed={displayAvatar} alt="" className="acct-avatar crew-illustration" />}
    >
      <div className="acct-streak">
        {glyph(Flame)}
        <span className="acct-streak-copy">
          <span className="acct-streak-title">{streakLabel(streak.currentStreak)}</span>
          {streak.longestStreak > 1 && <span className="acct-streak-meta">Longest: {streak.longestStreak} days</span>}
        </span>
      </div>

      <p className="acct-label">Today's focus</p>
      <List>
        {recommendation && recommendation.reason !== 'all-complete'
          ? <Row title={recommendation.title} onPress={go(() => onSelectModule(recommendation.moduleId))} />
          : <Row icon={glyph(Trophy)} title="All modules complete!" />}
      </List>

      <p className="acct-label">Learning</p>
      <List>
        <Row icon={glyph(ChartNoAxesColumn)} title="My Progress" onPress={go(onGoToDashboard)} />
        <Row icon={glyph(Stamp)} title="Study Passport" meta={`${completedCount} / ${totalCount}`} onPress={go(onOpenPassport)} />
        <Row icon={glyph(CalendarRange)} title="Year Plans" onPress={go(onGoToYearPlans)} />
      </List>

      <p className="acct-label">Direction</p>
      <List>
        {onGoToYourSetup && <Row icon={glyph(SlidersHorizontal)} title="Your setup" onPress={go(onGoToYourSetup)} />}
        {hasNorthStar && <Row icon={glyph(Star)} title="My North Star" onPress={go(onOpenNorthStar)} />}
        <Row icon={glyph(BookOpen)} title="References" onPress={go(onGoToReferences)} />
      </List>

      <p className="acct-label">Support</p>
      <List>
        <li className="ui-row-item acct-bell">
          <NotificationBell uid={user.uid} variant="menu" onUnreadCountChange={onUnreadCountChange}
            menuIcon={glyph(Bell)} menuTrailing={<ChevronRight className="ui-icon ui-row-chev" width={20} height={20} strokeWidth={1.75} aria-hidden="true" />} />
        </li>
        <Row icon={glyph(HelpCircle)} title="How the app works" onPress={go(onOpenSiteGuide)} />
        <Row icon={glyph(MessageSquare)} title="Give feedback" onPress={go(onOpenFeedback)} />
      </List>

      <p className="acct-label">Account</p>
      <List>
        <Row icon={glyph(Moon)} title="Dark mode (Beta)"
          trailing={<Switch checked={settings.darkMode} onChange={on => updateSetting('darkMode', on)} label="Dark mode (Beta)" />} />
        <Row icon={glyph(Settings)} title="Settings" onPress={go(onOpenSettings)} />
        <Row icon={glyph(LogOut)} title="Log out" tone="danger" onPress={go(onLogout)} />
      </List>
    </Sheet>
  );
};
