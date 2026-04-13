/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useRef, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowLeft, ArrowRight, CheckCircle2, Lock, List, X, Palette, Sun, Moon } from 'lucide-react';
import { type ModuleProgress, type SectionDefinition, type ModuleTheme, type AccentThemeId, type CardStyleId } from '../types';
import { ActivityRing } from './ModuleShared';
import { useSettingsContext } from '../contexts/SettingsContext';
import { ACCENT_THEME_LIST, CARD_STYLES } from '../themeData';
import ModuleCompleteScreen from './ModuleCompleteScreen';

/* ── Confetti celebration overlay ── */
const CONFETTI_COLORS = ['#CC785C', '#f59e0b', '#3b82f6', '#10b981', '#8b5cf6', '#ef4444', '#ec4899'];
const CONFETTI_COUNT = 60;

const ConfettiOverlay: React.FC<{ onDone: () => void }> = ({ onDone }) => {
  const pieces = useMemo(() => Array.from({ length: CONFETTI_COUNT }, (_, i) => ({
    id: i,
    x: Math.random() * 100,
    delay: Math.random() * 0.6,
    duration: 1.8 + Math.random() * 1.2,
    color: CONFETTI_COLORS[i % CONFETTI_COLORS.length],
    rotation: Math.random() * 360,
    size: 6 + Math.random() * 6,
    drift: (Math.random() - 0.5) * 40,
  })), []);

  useEffect(() => {
    const timer = setTimeout(onDone, 2800);
    return () => clearTimeout(timer);
  }, [onDone]);

  return (
    <div className="fixed inset-0 z-[200] pointer-events-none overflow-hidden">
      {pieces.map(p => (
        <motion.div
          key={p.id}
          initial={{ y: -20, x: `${p.x}vw`, opacity: 1, rotate: 0 }}
          animate={{ y: '110vh', x: `${p.x + p.drift}vw`, opacity: [1, 1, 0], rotate: p.rotation + 360 }}
          transition={{ duration: p.duration, delay: p.delay, ease: 'easeIn' }}
          style={{
            position: 'absolute',
            width: p.size,
            height: p.size * 0.6,
            backgroundColor: p.color,
            borderRadius: 2,
          }}
        />
      ))}
    </div>
  );
};

interface ModuleLayoutProps {
  moduleNumber: string;
  moduleTitle: string;
  moduleSubtitle?: string;
  moduleDescription?: string;
  theme: ModuleTheme;
  sections: SectionDefinition[];
  onBack: () => void;
  progress: ModuleProgress;
  onProgressUpdate: (p: ModuleProgress) => void;
  finishButtonText?: string;
  /** When essentials mode uses fewer sections, set this to the full section count
   *  so completion is reported correctly against courseData.sectionsCount */
  fullSectionsCount?: number;
  children: (activeSection: number) => React.ReactNode;
  // Celebration screen props (optional)
  categoryColor?: string;
  modulesCompleted?: number;
  totalModules?: number;
  northStarStatement?: string;
}

export const ModuleLayout: React.FC<ModuleLayoutProps> = ({
  moduleNumber,
  moduleTitle,
  moduleSubtitle,
  moduleDescription,
  theme,
  sections,
  onBack,
  progress,
  onProgressUpdate,
  finishButtonText = 'Complete Section',
  fullSectionsCount,
  children,
  categoryColor,
  modulesCompleted,
  totalModules,
  northStarStatement,
}) => {
  const settingsCtx = useSettingsContext();
  const [activeSection, setActiveSection] = useState(
    progress.unlockedSection >= sections.length ? sections.length - 1 : progress.unlockedSection
  );
  const [mobileSectionsOpen, setMobileSectionsOpen] = useState(false);
  const [showConfetti, setShowConfetti] = useState(false);
  const [showCelebration, setShowCelebration] = useState(false);
  const [pickerOpen, setPickerOpen] = useState(false);
  const pickerRef = useRef<HTMLDivElement>(null);
  const isCompletingRef = useRef(false);
  const mainRef = useRef<HTMLElement>(null);
  const pendingBackRef = useRef(false);
  const unlockedSection = progress.unlockedSection;

  // Close picker on outside click
  useEffect(() => {
    if (!pickerOpen) return;
    const handleClick = (e: MouseEvent) => {
      if (pickerRef.current && !pickerRef.current.contains(e.target as Node)) setPickerOpen(false);
    };
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, [pickerOpen]);

  useEffect(() => {
    setActiveSection(progress.unlockedSection >= sections.length ? sections.length - 1 : progress.unlockedSection);
  }, [progress.unlockedSection, sections.length]);

  // Scroll to top whenever the active section changes
  useEffect(() => {
    window.scrollTo({ top: 0 });
    if (mainRef.current) {
      mainRef.current.scrollTop = 0;
    }
  }, [activeSection]);

  const handleCompleteSection = () => {
    if (isCompletingRef.current) return;
    isCompletingRef.current = true;
    const isLastSection = activeSection === sections.length - 1;
    const isNewCompletion = activeSection === unlockedSection && unlockedSection < sections.length;
    if (isNewCompletion) {
      // When essentials mode uses fewer sections, report the full section count
      // on the last section so courseData.sectionsCount considers it complete
      const reportedUnlocked = (isLastSection && fullSectionsCount && fullSectionsCount > sections.length)
        ? fullSectionsCount
        : unlockedSection + 1;
      onProgressUpdate({ unlockedSection: reportedUnlocked });
    }
    if (!isLastSection) {
      setActiveSection(activeSection + 1);
    } else if (isNewCompletion) {
      // First-time module completion — show confetti + celebration screen
      setShowConfetti(true);
      setShowCelebration(true);
    } else {
      onBack();
    }
    setTimeout(() => { isCompletingRef.current = false; }, 500);
  };

  const handleConfettiDone = () => {
    setShowConfetti(false);
    // If no celebration screen (no categoryColor prop), fall back to old behaviour
    if (!showCelebration && pendingBackRef.current) {
      pendingBackRef.current = false;
      onBack();
    }
  };

  const handleCelebrationContinue = () => {
    setShowCelebration(false);
    onBack();
  };

  const handleJumpToSection = (index: number) => {
    if (index <= unlockedSection) {
      setActiveSection(index);
      setMobileSectionsOpen(false);
    }
  };

  const handlePrev = () => {
    if (activeSection > 0) {
      setActiveSection(activeSection - 1);
    }
  };

  const progressPercentage = sections.length > 0 ? (unlockedSection / sections.length) * 100 : 0;

  return (
    <div className="min-h-screen bg-[#F8F8F8] dark:bg-zinc-950 text-zinc-900 dark:text-white font-sans flex flex-col md:flex-row overflow-x-hidden transition-colors duration-500">

      {/* ── Desktop Sidebar (unchanged) ── */}
      <aside className="hidden md:flex w-80 bg-white dark:bg-zinc-900 border-r border-zinc-200 dark:border-zinc-800 sticky top-0 h-screen z-40 p-8 flex-col">
        <div className="flex items-center gap-4 mb-12">
          <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={onBack} className="p-2 rounded-lg transition-colors border border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-800 hover:bg-zinc-100 dark:hover:bg-zinc-700">
            <ArrowLeft size={16} className="text-zinc-700 dark:text-zinc-300" />
          </motion.button>
          <div>
            <p className={`text-[9px] font-semibold ${theme.sidebarModuleText} uppercase tracking-[0.2em] mb-0.5 underline`} style={{ color: 'var(--accent-hex)' }}>Unit {moduleNumber}</p>
            <h1 className="font-serif font-semibold text-lg tracking-tight text-zinc-900 dark:text-white">{moduleTitle}</h1>
          </div>
        </div>

        {(moduleSubtitle || moduleDescription) && (
          <div className="mb-8 -mt-4">
            {moduleSubtitle && <p className={`text-[11px] font-bold ${theme.sidebarActiveEyebrow} uppercase tracking-widest mb-1.5`} style={{ color: 'var(--accent-hex)' }}>{moduleSubtitle}</p>}
            {moduleDescription && <p className="text-[11px] leading-relaxed text-zinc-400 dark:text-zinc-500">{moduleDescription}</p>}
          </div>
        )}

        <div className="flex-grow overflow-y-auto no-scrollbar pr-2">
          <div className="space-y-4 relative">
            <div className="absolute left-[21px] top-[34px] bottom-[34px] w-0.5 bg-zinc-100 dark:bg-white/10 -z-0" />
            <div className="absolute left-[21px] top-[34px] bottom-[34px] w-0.5">
              <motion.div
                className={`w-full ${theme.sidebarProgressBg} ${theme.sidebarProgressShadow}`}
                style={{ height: `${progressPercentage}%`, backgroundColor: 'var(--accent-hex)', boxShadow: '0 0 10px rgba(var(--accent),0.5)' }}
              />
            </div>
            {sections.map((section, idx) => {
              const isUnlocked = idx <= unlockedSection;
              const isActive = idx === activeSection;
              const isCompleted = idx < unlockedSection;
              return (
                <button key={section.id} disabled={!isUnlocked} onClick={() => handleJumpToSection(idx)} className={`relative z-10 w-full flex items-center gap-4 p-3 rounded-xl transition-all duration-500 text-left group ${isActive ? `${theme.sidebarActiveBg} shadow-sm translate-x-2` : ''} ${!isUnlocked ? 'opacity-40 grayscale cursor-not-allowed' : 'hover:bg-zinc-50 dark:hover:bg-white/5'}`} style={isActive ? { backgroundColor: 'rgba(var(--accent),0.08)' } : undefined}>
                  <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border-2 transition-all duration-500 ${isCompleted ? `${theme.sidebarCompletedBg} ${theme.sidebarCompletedBorder} text-white shadow-lg` : isActive ? `bg-white dark:bg-zinc-800 ${theme.sidebarActiveBorder} ${theme.sidebarActiveText} shadow-xl rotate-12` : 'bg-white dark:bg-zinc-800 border-zinc-200 dark:border-zinc-700 text-zinc-300 dark:text-zinc-600'}`} style={isCompleted ? { backgroundColor: 'var(--accent-hex)', borderColor: 'var(--accent-hex)' } : isActive ? { borderColor: 'var(--accent-hex)', color: 'var(--accent-hex)' } : undefined}>
                    {isCompleted ? <CheckCircle2 size={18} /> : isActive ? <section.icon size={18} /> : <Lock size={16} />}
                  </div>
                  <div className="flex-grow">
                    <p className={`text-[8px] font-semibold uppercase tracking-widest ${isActive ? theme.sidebarActiveEyebrow : 'text-zinc-400 dark:text-zinc-500'}`} style={isActive ? { color: 'var(--accent-hex)' } : undefined}>{section.eyebrow.split('// ')[1]}</p>
                    <h4 className={`text-xs font-bold leading-tight ${isActive ? 'text-zinc-900 dark:text-white' : 'text-zinc-500 dark:text-zinc-400'}`}>{section.title}</h4>
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        <div className="mt-8 border-t border-zinc-100 dark:border-zinc-800 pt-8 flex flex-col items-center">
          <ActivityRing progress={progressPercentage} color={'var(--accent-hex)'} />
          <p className="text-[11px] font-semibold text-zinc-900 dark:text-white uppercase tracking-widest text-center">Progress</p>
        </div>

        {/* Floating theme/card picker */}
        {settingsCtx && (
          <div className="relative mt-4" ref={pickerRef}>
            <button onClick={() => setPickerOpen(!pickerOpen)} className="w-full flex items-center justify-center gap-2 p-2.5 rounded-xl border border-zinc-200 dark:border-zinc-800 hover:bg-zinc-50 dark:hover:bg-zinc-800 transition-colors text-zinc-500 dark:text-zinc-400">
              <Palette size={14} />
              <span className="text-[10px] font-semibold uppercase tracking-widest">Theme</span>
            </button>
            <AnimatePresence>
              {pickerOpen && (
                <motion.div
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 8 }}
                  className="absolute bottom-full left-0 right-0 mb-2 bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-xl shadow-xl p-4 z-50"
                >
                  {/* Dark mode toggle */}
                  <button onClick={() => settingsCtx.updateSetting('darkMode', !settingsCtx.settings.darkMode)} className="w-full flex items-center justify-between p-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-white/5 mb-2">
                    <span className="text-xs font-medium text-zinc-700 dark:text-zinc-300">{settingsCtx.settings.darkMode ? 'Light Mode' : 'Dark Mode'}</span>
                    {settingsCtx.settings.darkMode ? <Sun size={14} className="text-amber-400" /> : <Moon size={14} className="text-zinc-600" />}
                  </button>
                  {/* Accent colors */}
                  <p className="text-[9px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-1.5">Accent</p>
                  <div className="flex flex-wrap gap-1.5 mb-3">
                    {ACCENT_THEME_LIST.filter(t => t.price === 0 || settingsCtx.unlockedThemes.includes(t.id)).map(t => (
                      <button key={t.id} onClick={() => settingsCtx.updateSetting('accentTheme', t.id as AccentThemeId)} title={t.name} className={`p-1 rounded-lg transition-all ${settingsCtx.settings.accentTheme === t.id ? 'ring-2 ring-[var(--accent-hex)] bg-[rgba(var(--accent),0.1)]' : 'hover:bg-zinc-100 dark:hover:bg-zinc-800'}`}>
                        <div className="w-5 h-5 rounded-full border border-white dark:border-zinc-700 shadow-sm" style={{ backgroundColor: t.hex }} />
                      </button>
                    ))}
                  </div>
                  {/* Card styles */}
                  <p className="text-[9px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-1.5">Card Style</p>
                  <div className="space-y-1">
                    {CARD_STYLES.filter(s => s.price === 0 || settingsCtx.unlockedCardStyles.includes(s.id)).map(s => (
                      <button key={s.id} onClick={() => settingsCtx.updateSetting('cardStyle', s.id as CardStyleId)} className={`w-full text-left px-2 py-1.5 rounded-lg text-xs transition-all ${settingsCtx.settings.cardStyle === s.id ? 'bg-[rgba(var(--accent),0.1)] text-[var(--accent-hex)] font-semibold' : 'text-zinc-600 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-800'}`}>
                        {s.name}
                      </button>
                    ))}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        )}
      </aside>

      {/* ── Mobile Top Bar ── */}
      <div className="md:hidden fixed top-0 left-0 right-0 h-14 z-40 bg-white/80 dark:bg-zinc-900/80 backdrop-blur-xl border-b border-zinc-200/50 dark:border-white/[0.06] flex items-center gap-3 px-3" style={{ paddingTop: 'var(--sat, 0px)' }}>
        <button onClick={onBack} className="p-2 rounded-xl border border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-800 shrink-0 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[rgba(var(--accent),0.5)]">
          <ArrowLeft size={16} className="text-zinc-700 dark:text-zinc-300" />
        </button>
        <div className="flex-1 min-w-0">
          <p className={`text-[9px] font-semibold ${theme.sidebarModuleText} uppercase tracking-[0.15em] leading-none`} style={{ color: 'var(--accent-hex)' }}>Unit {moduleNumber}</p>
          <h1 className="text-sm font-semibold text-zinc-900 dark:text-white truncate">{moduleTitle}</h1>
        </div>
        <button onClick={() => setMobileSectionsOpen(true)} className="p-2 rounded-xl border border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-800 shrink-0 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[rgba(var(--accent),0.5)]">
          <List size={16} className="text-zinc-700 dark:text-zinc-300" />
        </button>
      </div>

      {/* ── Mobile Sections Drawer ── */}
      <AnimatePresence>
        {mobileSectionsOpen && (
          <>
            <motion.div
              key="sections-backdrop"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setMobileSectionsOpen(false)}
              className="md:hidden fixed inset-0 z-[50] bg-black/40"
            />
            <motion.div
              key="sections-sheet"
              initial={{ y: '100%' }}
              animate={{ y: 0 }}
              exit={{ y: '100%' }}
              transition={{ type: 'spring', damping: 28, stiffness: 300 }}
              className="md:hidden fixed bottom-0 left-0 right-0 z-[51] bg-white dark:bg-zinc-900 rounded-t-2xl border-t border-zinc-200 dark:border-zinc-800 max-h-[75vh] overflow-y-auto"
              style={{ paddingBottom: 'var(--sab, 0px)' }}
            >
              {/* Drag handle */}
              <div className="flex justify-center pt-3 pb-1">
                <div className="w-10 h-1 rounded-full bg-zinc-300 dark:bg-zinc-700" />
              </div>
              <div className="flex items-center justify-between px-5 pb-3">
                <div className="flex items-center gap-3">
                  <ActivityRing progress={progressPercentage} size={32} strokeWidth={3} color={'var(--accent-hex)'} />
                  <p className="text-sm font-semibold text-zinc-900 dark:text-white">Sections</p>
                </div>
                <button onClick={() => setMobileSectionsOpen(false)} className="p-1.5 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800">
                  <X size={16} className="text-zinc-400" />
                </button>
              </div>
              <div className="px-4 pb-6 space-y-1">
                {sections.map((section, idx) => {
                  const isUnlocked = idx <= unlockedSection;
                  const isActive = idx === activeSection;
                  const isCompleted = idx < unlockedSection;
                  return (
                    <button
                      key={section.id}
                      disabled={!isUnlocked}
                      onClick={() => handleJumpToSection(idx)}
                      className={`w-full flex items-center gap-3 p-3 rounded-xl text-left transition-colors ${isActive ? 'bg-zinc-100 dark:bg-zinc-800' : ''} ${!isUnlocked ? 'opacity-30 cursor-not-allowed' : 'hover:bg-zinc-50 dark:hover:bg-zinc-800/50'}`}
                    >
                      <div className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 border transition-colors ${isCompleted ? `${theme.sidebarCompletedBg} ${theme.sidebarCompletedBorder} text-white` : isActive ? `bg-white dark:bg-zinc-700 ${theme.sidebarActiveBorder} ${theme.sidebarActiveText}` : 'bg-zinc-100 dark:bg-zinc-800 border-zinc-200 dark:border-zinc-700 text-zinc-400'}`} style={isCompleted ? { backgroundColor: 'var(--accent-hex)', borderColor: 'var(--accent-hex)' } : isActive ? { borderColor: 'var(--accent-hex)', color: 'var(--accent-hex)' } : undefined}>
                        {isCompleted ? <CheckCircle2 size={14} /> : isActive ? <section.icon size={14} /> : <Lock size={12} />}
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className={`text-[8px] font-semibold uppercase tracking-widest ${isActive ? theme.sidebarActiveEyebrow : 'text-zinc-400 dark:text-zinc-500'}`} style={isActive ? { color: 'var(--accent-hex)' } : undefined}>{section.eyebrow.split('// ')[1]}</p>
                        <h4 className={`text-xs font-bold leading-tight truncate ${isActive ? 'text-zinc-900 dark:text-white' : 'text-zinc-500 dark:text-zinc-400'}`}>{section.title}</h4>
                      </div>
                    </button>
                  );
                })}
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>

      {/* ── Main Content ── */}
      <main ref={mainRef} className="flex-grow flex flex-col items-center pt-20 md:pt-24 px-6 md:px-16 pb-24 md:pb-0 md:overflow-y-auto md:h-screen bg-[#F8F8F8] dark:bg-zinc-950">
        <div className="w-full max-w-3xl">
          <AnimatePresence mode="wait">
            <motion.div
              key={activeSection}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.4, ease: [0.25, 1, 0.5, 1] }}
            >
              {children(activeSection)}
              <footer className="mt-16 flex items-center justify-between pt-8 pb-6">
                <button onClick={handlePrev} disabled={activeSection === 0} className={`flex items-center gap-3 bg-[#FEFDFB] dark:bg-zinc-800 text-zinc-600 dark:text-white px-6 py-3.5 rounded-xl font-semibold text-[11px] uppercase tracking-widest transition-all hover:scale-[1.02] active:scale-[0.98] border border-[#EDEBE8] dark:border-zinc-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[rgba(var(--accent),0.5)] focus-visible:ring-offset-2 ${activeSection === 0 ? 'invisible' : ''}`}>
                  <ArrowLeft size={16} /> Prev
                </button>
                <button onClick={handleCompleteSection} className="flex items-center gap-3 bg-[#FEFDFB] dark:bg-zinc-800 text-zinc-600 dark:text-white px-6 py-3.5 rounded-xl font-semibold text-[11px] uppercase tracking-widest transition-all hover:scale-[1.02] active:scale-[0.98] border border-[#EDEBE8] dark:border-zinc-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[rgba(var(--accent),0.5)] focus-visible:ring-offset-2">
                  {activeSection === sections.length - 1 ? finishButtonText : 'Continue'} <ArrowRight size={16} />
                </button>
              </footer>
            </motion.div>
          </AnimatePresence>
        </div>
      </main>

      {showConfetti && <ConfettiOverlay onDone={handleConfettiDone} />}

      {/* Module completion celebration screen */}
      <ModuleCompleteScreen
        isOpen={showCelebration}
        moduleTitle={moduleTitle}
        moduleSubtitle={moduleSubtitle}
        categoryColor={categoryColor || '#2A7D6F'}
        modulesCompleted={modulesCompleted}
        totalModules={totalModules}
        sectionsCount={sections.length}
        northStarStatement={northStarStatement}
        onContinue={handleCelebrationContinue}
      />
    </div>
  );
};
