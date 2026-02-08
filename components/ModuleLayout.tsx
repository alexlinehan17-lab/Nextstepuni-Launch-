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
  finishButtonText = 'Finish Protocol',
  children,
}) => {
  const [activeSection, setActiveSection] = useState(progress.unlockedSection);
  const unlockedSection = progress.unlockedSection;

  useEffect(() => {
    setActiveSection(progress.unlockedSection);
  }, [progress.unlockedSection]);

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
    <div className="min-h-screen bg-[#FBFBF9] text-stone-900 font-sans flex flex-col md:flex-row overflow-x-hidden">
      <aside className="w-full md:w-80 bg-[#FAF9F7] border-r border-stone-200/60 sticky top-0 md:h-screen z-40 p-8 flex flex-col">
        <div className="flex items-center gap-4 mb-12">
          <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={onBack} className="p-2 rounded-full transition-all border border-stone-200/50 shadow-sm bg-white">
            <ArrowLeft size={16} className="text-stone-700" />
          </motion.button>
          <div>
            <p className={`text-[9px] font-semibold ${theme.sidebarModuleText} uppercase tracking-[0.4em] mb-0.5 underline`}>Module {moduleNumber}</p>
            <h1 className="font-serif font-semibold text-lg tracking-tight text-stone-900">{moduleTitle}</h1>
          </div>
        </div>

        <div className="flex-grow overflow-y-auto no-scrollbar pr-2">
          <div className="space-y-4 relative">
            <div className="absolute left-[21px] top-[34px] bottom-[34px] w-0.5 bg-stone-100 -z-0" />
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
                <button key={section.id} disabled={!isUnlocked} onClick={() => handleJumpToSection(idx)} className={`relative z-10 w-full flex items-center gap-4 p-3 rounded-xl transition-all duration-500 text-left group ${isActive ? `${theme.sidebarActiveBg} shadow-sm translate-x-2` : ''} ${!isUnlocked ? 'opacity-40 grayscale cursor-not-allowed' : 'hover:bg-stone-50'}`}>
                  <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border-2 transition-all duration-500 ${isCompleted ? `${theme.sidebarCompletedBg} ${theme.sidebarCompletedBorder} text-white shadow-lg` : isActive ? `bg-white ${theme.sidebarActiveBorder} ${theme.sidebarActiveText} shadow-xl rotate-12` : 'bg-white border-stone-200 text-stone-300'}`}>
                    {isCompleted ? <CheckCircle2 size={18} /> : isActive ? <section.icon size={18} /> : <Lock size={16} />}
                  </div>
                  <div className="flex-grow">
                    <p className={`text-[8px] font-semibold uppercase tracking-widest ${isActive ? theme.sidebarActiveEyebrow : 'text-stone-400'}`}>{section.eyebrow.split('// ')[1]}</p>
                    <h4 className={`text-xs font-bold leading-tight ${isActive ? 'text-stone-900' : 'text-stone-500'}`}>{section.title}</h4>
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        <div className="mt-8 border-t border-stone-100 pt-8 flex flex-col items-center">
          <ActivityRing progress={progressPercentage} color={theme.activityRingColor} />
          <p className="text-[11px] font-semibold text-stone-900 uppercase tracking-widest text-center">Progress</p>
        </div>
      </aside>

      <main className="flex-grow flex flex-col items-center py-10 md:py-24 px-6 md:px-16 overflow-y-auto h-screen relative">
        <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:32px_32px] opacity-20 pointer-events-none" />
        <div className="w-full max-w-4xl relative z-10">
          <AnimatePresence mode="wait">
            <motion.div key={activeSection} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}>
              {children(activeSection)}
              <footer className="mt-24 flex items-center justify-between pt-12 border-t border-stone-200/60 px-4">
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handlePrev} disabled={activeSection === 0} className={`flex items-center gap-4 bg-stone-100 text-stone-800 px-8 py-4 rounded-xl font-semibold text-[10px] uppercase tracking-widest transition-all shadow-sm ${activeSection === 0 ? 'opacity-0 pointer-events-none' : ''}`}>
                  <ArrowLeft size={16} /> Prev
                </motion.button>
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handleCompleteSection} className={`group relative flex items-center gap-4 bg-stone-900 text-white px-12 py-6 rounded-2xl font-semibold text-[12px] uppercase tracking-widest ${theme.footerHoverBg} transition-all shadow-[0_20px_50px_rgba(0,0,0,0.2)] overflow-hidden`}>
                  <span className="relative z-10">{activeSection === sections.length - 1 ? finishButtonText : 'Deploy Next Phase'}</span>
                  <ArrowRight size={18} className="relative z-10 group-hover:translate-x-2 transition-transform" />
                </motion.button>
              </footer>
            </motion.div>
          </AnimatePresence>
        </div>
      </main>
    </div>
  );
};
