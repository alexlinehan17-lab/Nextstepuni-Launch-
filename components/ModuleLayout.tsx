/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowLeft, ArrowRight, CheckCircle2, Lock } from 'lucide-react';
import { ModuleProgress, SectionDefinition, ModuleTheme } from '../types';
import { ActivityRing } from './ModuleShared';

interface ModuleLayoutProps {
  moduleNumber: string;
  moduleTitle: string;
  theme: ModuleTheme;
  sections: SectionDefinition[];
  onBack: () => void;
  progress: ModuleProgress;
  onProgressUpdate: (p: ModuleProgress) => void;
  finishButtonText?: string;
  children: (activeSection: number) => React.ReactNode;
}

export const ModuleLayout: React.FC<ModuleLayoutProps> = ({
  moduleNumber,
  moduleTitle,
  theme,
  sections,
  onBack,
  progress,
  onProgressUpdate,
  finishButtonText = 'Complete Section',
  children,
}) => {
  const [activeSection, setActiveSection] = useState(
    progress.unlockedSection >= sections.length ? 0 : progress.unlockedSection
  );
  const unlockedSection = progress.unlockedSection;

  useEffect(() => {
    setActiveSection(progress.unlockedSection >= sections.length ? 0 : progress.unlockedSection);
  }, [progress.unlockedSection, sections.length]);

  const handleCompleteSection = () => {
    if (activeSection === unlockedSection && unlockedSection < sections.length) {
      onProgressUpdate({ unlockedSection: unlockedSection + 1 });
    }
    if (activeSection < sections.length - 1) {
      setActiveSection(activeSection + 1);
    } else {
      onBack();
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleJumpToSection = (index: number) => {
    if (index <= unlockedSection) {
      setActiveSection(index);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  const handlePrev = () => {
    if (activeSection > 0) {
      setActiveSection(activeSection - 1);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  const progressPercentage = sections.length > 0 ? (unlockedSection / sections.length) * 100 : 0;

  return (
    <div className="min-h-screen bg-zinc-50 dark:bg-zinc-950 text-zinc-900 dark:text-white font-sans flex flex-col md:flex-row overflow-x-hidden transition-colors duration-500">
      <aside className="w-full md:w-80 bg-white dark:bg-zinc-900 border-r border-zinc-200 dark:border-zinc-800 sticky top-0 md:h-screen z-40 p-8 flex flex-col">
        <div className="flex items-center gap-4 mb-12">
          <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={onBack} className="p-2 rounded-lg transition-colors border border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-800 hover:bg-zinc-100 dark:hover:bg-zinc-700">
            <ArrowLeft size={16} className="text-zinc-700 dark:text-zinc-300" />
          </motion.button>
          <div>
            <p className={`text-[9px] font-semibold ${theme.sidebarModuleText} uppercase tracking-[0.2em] mb-0.5 underline`}>Unit {moduleNumber}</p>
            <h1 className="font-serif font-semibold text-lg tracking-tight text-zinc-900 dark:text-white">{moduleTitle}</h1>
          </div>
        </div>

        <div className="flex-grow overflow-y-auto no-scrollbar pr-2">
          <div className="space-y-4 relative">
            <div className="absolute left-[21px] top-[34px] bottom-[34px] w-0.5 bg-zinc-100 dark:bg-white/10 -z-0" />
            <div className="absolute left-[21px] top-[34px] bottom-[34px] w-0.5">
              <motion.div
                className={`w-full ${theme.sidebarProgressBg} ${theme.sidebarProgressShadow}`}
                style={{ height: `${progressPercentage}%` }}
              />
            </div>
            {sections.map((section, idx) => {
              const isUnlocked = idx <= unlockedSection;
              const isActive = idx === activeSection;
              const isCompleted = idx < unlockedSection;
              return (
                <button key={section.id} disabled={!isUnlocked} onClick={() => handleJumpToSection(idx)} className={`relative z-10 w-full flex items-center gap-4 p-3 rounded-xl transition-all duration-500 text-left group ${isActive ? `${theme.sidebarActiveBg} shadow-sm translate-x-2` : ''} ${!isUnlocked ? 'opacity-40 grayscale cursor-not-allowed' : 'hover:bg-zinc-50 dark:hover:bg-white/5'}`}>
                  <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border-2 transition-all duration-500 ${isCompleted ? `${theme.sidebarCompletedBg} ${theme.sidebarCompletedBorder} text-white shadow-lg` : isActive ? `bg-white dark:bg-zinc-800 ${theme.sidebarActiveBorder} ${theme.sidebarActiveText} shadow-xl rotate-12` : 'bg-white dark:bg-zinc-800 border-zinc-200 dark:border-zinc-700 text-zinc-300 dark:text-zinc-600'}`}>
                    {isCompleted ? <CheckCircle2 size={18} /> : isActive ? <section.icon size={18} /> : <Lock size={16} />}
                  </div>
                  <div className="flex-grow">
                    <p className={`text-[8px] font-semibold uppercase tracking-widest ${isActive ? theme.sidebarActiveEyebrow : 'text-zinc-400 dark:text-zinc-500'}`}>{section.eyebrow.split('// ')[1]}</p>
                    <h4 className={`text-xs font-bold leading-tight ${isActive ? 'text-zinc-900 dark:text-white' : 'text-zinc-500 dark:text-zinc-400'}`}>{section.title}</h4>
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        <div className="mt-8 border-t border-zinc-100 dark:border-zinc-800 pt-8 flex flex-col items-center">
          <ActivityRing progress={progressPercentage} color={theme.activityRingColor} />
          <p className="text-[11px] font-semibold text-zinc-900 dark:text-white uppercase tracking-widest text-center">Progress</p>
        </div>
      </aside>

      <main className="flex-grow flex flex-col items-center py-10 md:py-24 px-6 md:px-16 overflow-y-auto h-screen">
        <div className="w-full max-w-4xl">
          <AnimatePresence mode="wait">
            <motion.div key={activeSection} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}>
              {children(activeSection)}
              <footer className="mt-24 flex items-center justify-between pt-12 border-t border-zinc-200 dark:border-zinc-800 px-4">
                <motion.button whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }} onClick={handlePrev} disabled={activeSection === 0} className={`flex items-center gap-3 bg-zinc-100 dark:bg-zinc-800 text-zinc-700 dark:text-white px-6 py-3.5 rounded-lg font-semibold text-[11px] uppercase tracking-widest transition-all ${activeSection === 0 ? 'opacity-0 pointer-events-none' : ''}`}>
                  <ArrowLeft size={16} /> Prev
                </motion.button>
                <motion.button whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }} onClick={handleCompleteSection} className={`group flex items-center gap-3 bg-zinc-900 dark:bg-white text-white dark:text-zinc-900 px-10 py-4 rounded-lg font-semibold text-[11px] uppercase tracking-widest ${theme.footerHoverBg} transition-all`}>
                  <span>{activeSection === sections.length - 1 ? finishButtonText : 'Continue'}</span>
                  <ArrowRight size={16} className="group-hover:translate-x-1 transition-transform" />
                </motion.button>
              </footer>
            </motion.div>
          </AnimatePresence>
        </div>
      </main>
    </div>
  );
};
