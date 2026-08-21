/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useRef } from 'react';
import { createPortal } from 'react-dom';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { X, Check, Lock, Sun, Moon, RefreshCw, LogOut, ChevronRight, Compass, GraduationCap, ArrowRight, ShieldCheck, FileText, Trash2 } from 'lucide-react';
import { useModal } from '../hooks/useModal';
import { LegalModal, type LegalDoc } from './legal/LegalModal';
import { DataRightsModal } from './account/DataRightsModal';
import { AVATAR_SEEDS, getAvatarUrl, nextYearAction, yearGroupLabel, yearGroupToCurriculumLevel } from '../utils/authUtils';
import { type YearGroup } from './subjectData';

const EXTRA_AVATAR_SEEDS = ['Luna', 'Kai', 'Suki', 'Dara', 'Nico', 'Asha', 'Finn', 'Yuki'];
const AVATAR_PRICE_JP = 120;
import { type UserSettings } from '../types';

interface SettingsModalProps {
  isOpen: boolean;
  onClose: () => void;
  settings: UserSettings;
  updateSetting: <K extends keyof UserSettings>(key: K, value: UserSettings[K]) => void;
  unlockedAvatarSeeds?: string[];
  pointsBalance?: number;
  onPurchaseAvatar?: (seed: string, price: number) => Promise<boolean>;
  unlockedThemes?: string[];
  unlockedCardStyles?: string[];
  userName?: string;
  userSchool?: string;
  /** Phase 8: current year group, used by the School Year section to
   *  render the "I'm now in X" forward-progression button. */
  userYearGroup?: YearGroup;
  onChangeSubjects?: () => void;
  onResetNorthStar?: () => void;
  /** Phase 8: opens the year transition flow (quiet bump confirm /
   *  TY-vs-5th picker / graduation confirm depending on current year). */
  onAdvanceYear?: () => void;
  onLogout?: () => void;
}

const SettingsModal: React.FC<SettingsModalProps> = ({
  isOpen, onClose, settings, updateSetting,
  unlockedAvatarSeeds = [], unlockedThemes: _unlockedThemes = [], unlockedCardStyles: _unlockedCardStyles = [],
  pointsBalance = 0, onPurchaseAvatar,
  userName, userSchool, userYearGroup, onChangeSubjects, onResetNorthStar, onAdvanceYear, onLogout,
}) => {
  useModal(isOpen, onClose);
  // Junior Cycle always runs in Essentials Mode (simpler, shorter modules) — the
  // toggle is shown as locked-on rather than editable. See useEssentialsMode.
  const isJunior = userYearGroup ? yearGroupToCurriculumLevel(userYearGroup) === 'junior' : false;
  const [showSaved, setShowSaved] = useState(false);
  const [legalDoc, setLegalDoc] = useState<LegalDoc | null>(null);
  const [dataRightsOpen, setDataRightsOpen] = useState(false);
  const [purchasingAvatar, setPurchasingAvatar] = useState<string | null>(null);
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
    <>
    <AnimatePresence>
      {isOpen && (
        <MotionDiv
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="theme-compat fixed inset-0 bg-[#1A1A1A]/55 flex items-end sm:items-center justify-center z-[200] p-0 sm:p-4"
          onClick={onClose}
        >
          <MotionDiv
            initial={{ scale: 0.96, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.96, opacity: 0 }}
            transition={{ duration: 0.2, ease: [0.16, 1, 0.3, 1] }}
            className="relative bg-[#FAFBF6] dark:bg-zinc-900 border-[1.5px] border-[#383838] dark:border-zinc-600 rounded-t-[24px] sm:rounded-[24px] w-full max-w-md shadow-[5px_5px_0_0_#383838] overflow-hidden max-h-[92dvh] overflow-y-auto"
            onClick={(e: React.MouseEvent) => e.stopPropagation()}
          >
            {/* Header */}
            <div className="flex items-center justify-between p-6 pb-4 border-b border-[#DDD8D2] dark:border-zinc-700">
              <h2 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white tracking-tight">
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
                  aria-label="Close"
                  className="flex h-9 w-9 items-center justify-center rounded-xl border border-[#CFC9C2] bg-white text-[#6F6861] transition-colors hover:border-[#383838] hover:text-[#1A1A1A] dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-300"
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
                <div className="mb-3 flex items-center justify-between">
                  <h3 className="text-xs font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">
                    Avatar
                  </h3>
                  <span className="font-mono text-[10px] font-bold text-[#B94712] dark:text-[#FF9A64]">
                    {pointsBalance} JP available
                  </span>
                </div>
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
                    const canAfford = pointsBalance >= AVATAR_PRICE_JP;
                    const isPurchasing = purchasingAvatar === seed;
                    return (
                      <div key={seed} className="group relative" title={isUnlocked ? seed : `${AVATAR_PRICE_JP} JP`}>
                        <button
                          onClick={async () => {
                            if (isUnlocked) {
                              updateSetting('avatar', seed);
                              flash();
                              return;
                            }
                            if (!onPurchaseAvatar || isPurchasing) return;
                            setPurchasingAvatar(seed);
                            try {
                              const purchased = await onPurchaseAvatar(seed, AVATAR_PRICE_JP);
                              if (purchased) {
                                updateSetting('avatar', seed);
                                flash();
                              }
                            } finally {
                              setPurchasingAvatar(null);
                            }
                          }}
                          aria-label={isUnlocked ? `Select ${seed} avatar` : `Unlock ${seed} avatar for ${AVATAR_PRICE_JP} JP`}
                          disabled={isPurchasing}
                          className={`w-full rounded-xl aspect-square p-1.5 transition-all ${
                            isUnlocked
                              ? settings.avatar === seed
                                ? 'ring-2 ring-[var(--accent-hex)] bg-[rgba(var(--accent),0.1)]'
                                : 'bg-zinc-50 dark:bg-white/[0.04] ring-1 ring-zinc-200 dark:ring-white/[0.06] hover:ring-zinc-300 dark:hover:ring-white/[0.15]'
                              : 'bg-zinc-50 dark:bg-white/[0.04] ring-1 ring-zinc-200 dark:ring-white/[0.06] hover:ring-[#383838] focus-visible:ring-[#383838]'
                          }`}
                        >
                          <img
                            src={getAvatarUrl(seed)}
                            alt={seed}
                            className={`w-full h-full rounded-lg transition-all ${!isUnlocked ? 'grayscale opacity-35 group-hover:opacity-20 group-focus-within:opacity-20' : ''}`}
                          />
                          {!isUnlocked && (
                            <span className="absolute inset-1.5 flex flex-col items-center justify-center rounded-lg bg-[#20201F]/90 text-white opacity-0 transition-opacity group-hover:opacity-100 group-focus-within:opacity-100">
                              <span className="font-mono text-[11px] font-bold text-[#FF8A4C]">
                                {isPurchasing ? 'BUYING…' : `${AVATAR_PRICE_JP} JP`}
                              </span>
                              <span className="mt-0.5 text-[9px] font-semibold">
                                {canAfford ? 'Unlock' : `Need ${AVATAR_PRICE_JP - pointsBalance} more`}
                              </span>
                            </span>
                          )}
                        </button>
                        {!isUnlocked && (
                          <div className="pointer-events-none absolute bottom-0.5 right-0.5 flex h-5 w-5 items-center justify-center rounded-full border border-white bg-[#383838] transition-opacity group-hover:opacity-0 group-focus-within:opacity-0">
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
                      <p className="text-sm font-medium text-zinc-700 dark:text-zinc-200">{settings.darkMode ? 'Light Mode (Beta)' : 'Dark Mode (Beta)'}</p>
                    </div>
                    <div className={`relative w-10 h-6 rounded-full transition-colors ${
                      settings.darkMode ? 'bg-[var(--accent-hex)]' : 'bg-zinc-300 dark:bg-zinc-600'
                    }`}>
                      <div className={`absolute top-0.5 w-5 h-5 rounded-full bg-white shadow-sm transition-transform ${
                        settings.darkMode ? 'translate-x-[18px]' : 'translate-x-0.5'
                      }`} />
                    </div>
                  </button>

                  {/* Essentials mode toggle. Junior Cycle is always on (locked);
                      senior students can toggle it. */}
                  <button
                    onClick={() => {
                      if (isJunior) return;
                      updateSetting('essentialsMode', !settings.essentialsMode);
                      flash();
                    }}
                    disabled={isJunior}
                    className={`w-full flex items-center justify-between p-3 rounded-xl bg-zinc-50 dark:bg-white/[0.04] ring-1 ring-zinc-200 dark:ring-white/[0.06] transition-all ${isJunior ? 'cursor-default' : 'hover:ring-zinc-300 dark:hover:ring-white/[0.15]'}`}
                  >
                    <div className="flex-1 text-left">
                      <p className="text-sm font-medium text-zinc-700 dark:text-zinc-200">Essentials Mode</p>
                      <p className="text-[10px] text-zinc-400 dark:text-zinc-500 mt-0.5">
                        {isJunior ? 'Always on for Junior Cycle — shorter modules with simpler language' : 'Shorter modules with simpler language'}
                      </p>
                    </div>
                    <div className={`relative w-10 h-6 rounded-full transition-colors ${
                      (isJunior || settings.essentialsMode) ? 'bg-[var(--accent-hex)]' : 'bg-zinc-300 dark:bg-zinc-600'
                    }`}>
                      <div className={`absolute top-0.5 w-5 h-5 rounded-full bg-white shadow-sm transition-transform ${
                        (isJunior || settings.essentialsMode) ? 'translate-x-[18px]' : 'translate-x-0.5'
                      }`} />
                    </div>
                  </button>

                </div>
              </section>

              {/* School Year (Phase 8) — forward-progression action.
                  Renders for any logged-in student. If userYearGroup is
                  unknown (legacy account, pre-Phase-8), we still surface
                  the section with an empty-state CTA so the flow is
                  discoverable instead of silently hidden. */}
              {onAdvanceYear && (() => {
                const action = userYearGroup ? nextYearAction(userYearGroup) : null;
                const isGraduated = userYearGroup === 'graduated';
                return (
                  <section>
                    <h3 className="text-xs font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-3">
                      School Year
                    </h3>
                    <div className="rounded-2xl p-4 bg-zinc-50 dark:bg-white/[0.04] border border-zinc-200/60 dark:border-white/[0.06]">
                      <div className="flex items-center gap-3 mb-3">
                        <GraduationCap size={18} className="text-zinc-400" />
                        <p className="text-sm font-medium text-zinc-700 dark:text-zinc-200">
                          {!userYearGroup
                            ? "We don't have your school year on file."
                            : isGraduated
                              ? "You've completed your Leaving Cert."
                              : `You're in ${yearGroupLabel(userYearGroup)}.`}
                        </p>
                      </div>
                      {!action || action.kind === 'terminal' ? (
                        <p className="text-xs text-zinc-500 dark:text-zinc-400 italic">
                          {action?.label ?? 'Set your school year so we can tune content to where you are.'}
                        </p>
                      ) : (
                        <button
                          onClick={() => { onClose(); onAdvanceYear(); }}
                          className="w-full flex items-center justify-center gap-2 px-4 py-3 rounded-2xl border-2 border-[#1A1A1A] bg-[#F26B1F] text-[#FDF8F0] font-sans font-bold text-sm transition-all duration-150 -translate-x-0 -translate-y-0 hover:-translate-y-0.5 active:translate-x-1 active:translate-y-1 shadow-[4px_4px_0_0_#1A1A1A] hover:shadow-[6px_6px_0_0_#1A1A1A] active:shadow-[0px_0px_0_0_#1A1A1A]"
                        >
                          {action.label}
                          <ArrowRight size={14} />
                        </button>
                      )}
                    </div>
                  </section>
                );
              })()}

              {/* Actions */}
              {/* Legal — Privacy Notice + Terms (audit 2026-06-01, B4) */}
              <section>
                <h3 className="text-xs font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-3">
                  Legal
                </h3>
                {/* Non-affiliation disclaimer, shown without opening a document.
                    Google Play's Misleading Claims policy requires any app
                    carrying government information to state plainly that it does
                    not represent the government entity, and to be easy to see —
                    the full source list lives in Terms of Use. */}
                <p className="text-xs text-zinc-500 dark:text-zinc-400 mb-3 leading-relaxed">
                  NextStepUni is an independent study app. It is not affiliated with or
                  endorsed by the State Examinations Commission, the Department of Education,
                  the CAO, SUSI, or any other government body. See{' '}
                  <button
                    onClick={() => setLegalDoc('terms')}
                    className="underline font-medium text-zinc-600 dark:text-zinc-300"
                  >
                    Terms of Use
                  </button>{' '}
                  for the official sources we draw on.
                </p>
                <div className="space-y-1">
                  <button
                    onClick={() => setLegalDoc('privacy')}
                    className="w-full flex items-center justify-between p-3 rounded-xl hover:bg-zinc-50 dark:hover:bg-white/[0.04] transition-colors"
                  >
                    <div className="flex items-center gap-3">
                      <ShieldCheck size={16} className="text-zinc-400" />
                      <p className="text-sm font-medium text-zinc-700 dark:text-zinc-200">Privacy Notice</p>
                    </div>
                    <ChevronRight size={14} className="text-zinc-300 dark:text-zinc-600" />
                  </button>
                  <button
                    onClick={() => setLegalDoc('terms')}
                    className="w-full flex items-center justify-between p-3 rounded-xl hover:bg-zinc-50 dark:hover:bg-white/[0.04] transition-colors"
                  >
                    <div className="flex items-center gap-3">
                      <FileText size={16} className="text-zinc-400" />
                      <p className="text-sm font-medium text-zinc-700 dark:text-zinc-200">Terms of Use</p>
                    </div>
                    <ChevronRight size={14} className="text-zinc-300 dark:text-zinc-600" />
                  </button>
                </div>
              </section>

              {/* Account — its own section on purpose.
                  App Review rejected 1.0 (1) under Guideline 5.1.1(v) saying the
                  app had no way to delete an account. It did: this button, then
                  "Delete my account". But it was labelled "Download or delete my
                  data", sat third in the LEGAL list under Privacy Notice and
                  Terms, and wore a database icon — so it read as a GDPR export
                  control and a reviewer scanning for the words "Delete Account"
                  went straight past it. The feature was never the problem; the
                  wording was. Keep "Delete Account" in this label. */}
              <section>
                <h3 className="text-xs font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-3">
                  Account
                </h3>
                <div className="space-y-1">
                  <button
                    onClick={() => setDataRightsOpen(true)}
                    className="w-full flex items-center justify-between p-3 rounded-xl hover:bg-zinc-50 dark:hover:bg-white/[0.04] transition-colors"
                  >
                    <div className="flex items-center gap-3">
                      <Trash2 size={16} className="text-rose-500" />
                      <div className="text-left">
                        <p className="text-sm font-medium text-zinc-700 dark:text-zinc-200">Delete Account</p>
                        <p className="text-[12px] text-zinc-500">Permanently erase your account, or download your data first.</p>
                      </div>
                    </div>
                    <ChevronRight size={14} className="text-zinc-300 dark:text-zinc-600" />
                  </button>
                </div>
              </section>

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
    </AnimatePresence>
    <LegalModal doc={legalDoc} onClose={() => setLegalDoc(null)} />
    <DataRightsModal
      open={dataRightsOpen}
      onClose={() => setDataRightsOpen(false)}
      onAccountDeleted={() => { setDataRightsOpen(false); onClose(); onLogout?.(); }}
    />
    </>,
    document.body
  );
};

export default SettingsModal;
