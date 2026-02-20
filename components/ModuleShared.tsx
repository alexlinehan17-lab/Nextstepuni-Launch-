/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Zap, Quote } from 'lucide-react';
import { ModuleTheme } from '../types';

interface HighlightProps {
  children?: React.ReactNode;
  description: string;
  theme: ModuleTheme;
}

export const Highlight = ({ children, description, theme }: HighlightProps) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <span className="relative inline-block mx-0.5">
      <button
        onClick={(e) => {
          e.stopPropagation();
          setIsOpen(!isOpen);
        }}
        className={`relative inline-flex items-center px-2 py-0.5 font-bold ${theme.highlightBg} dark:bg-white/10 ${theme.highlightText} dark:text-white rounded-md cursor-help ${theme.highlightHover} transition-all duration-300 ${theme.highlightDecor} underline decoration-2 underline-offset-4`}
      >
        <span className="not-italic">{children}</span>
      </button>
      <AnimatePresence>
        {isOpen && (
          <>
            <div className="fixed inset-0 z-[60]" onClick={() => setIsOpen(false)} />
            <motion.div
              initial={{ opacity: 0, scale: 0.9, y: 10, x: "-50%" }}
              animate={{ opacity: 1, scale: 1, y: 0, x: "-50%" }}
              exit={{ opacity: 0, scale: 0.9, y: 10, x: "-50%" }}
              className="absolute z-[70] bottom-full left-1/2 mb-6 w-72 max-w-[calc(100vw-2rem)] p-6 bg-zinc-900/95 text-white text-xs rounded-2xl shadow-2xl pointer-events-auto leading-relaxed border border-white/10 backdrop-blur-xl whitespace-normal text-left"
              style={{ transformOrigin: 'bottom center' }}
            >
              <div className="absolute bottom-0 left-1/2 -translate-x-1/2 translate-y-full w-0 h-0 border-l-[10px] border-l-transparent border-r-[10px] border-r-transparent border-t-[10px] border-t-zinc-900/95"></div>
              <p className={`font-sans font-bold ${theme.tooltipAccent} mb-2 uppercase tracking-wider text-[9px]`}>Key Insight</p>
              <p className="text-zinc-200 font-medium">{description}</p>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </span>
  );
};

interface ReadingSectionProps {
  title: string;
  eyebrow: string;
  icon: any;
  children?: React.ReactNode;
  theme: ModuleTheme;
}

export const ReadingSection = ({ title, eyebrow, icon: Icon, children, theme }: ReadingSectionProps) => (
  <article className="animate-fade-in">
    <header className="mb-12 text-left relative">
      <div className="absolute -left-16 top-0 hidden xl:block">
        <div className={`w-12 h-12 rounded-2xl bg-zinc-900 flex items-center justify-center ${theme.readingIconColor} shadow-xl border border-white/10`}>
          <Icon size={24} />
        </div>
      </div>
      <span className={`inline-flex items-center gap-2 px-3 py-1 ${theme.readingEyebrowBg} ${theme.readingEyebrowText} text-[10px] font-semibold tracking-wider uppercase rounded-full mb-4`}>
        {eyebrow}
      </span>
      <h2 className="font-serif text-3xl md:text-5xl leading-tight tracking-tight text-zinc-900 dark:text-white font-semibold">
        {title}
      </h2>
    </header>
    <div className="prose prose-stone dark:prose-invert prose-lg max-w-none space-y-8 text-zinc-600 dark:text-zinc-300 leading-relaxed font-serif overflow-visible">
      {children}
    </div>
  </article>
);

interface MicroCommitmentProps {
  children?: React.ReactNode;
  theme: ModuleTheme;
  northStarNudge?: string;
}

export const MicroCommitment = ({ children, theme, northStarNudge }: MicroCommitmentProps) => (
  <div className={`my-12 border-l-[3px] ${theme.microBorder} bg-white dark:bg-zinc-900 rounded-r-xl p-8`}>
    <div className="flex items-start gap-4">
      <div className={`w-9 h-9 rounded-lg ${theme.microIconBg} text-white flex items-center justify-center shrink-0`}>
        <Zap size={16} />
      </div>
      <div>
        <p className={`text-[10px] font-semibold uppercase tracking-[0.15em] ${theme.microTitle} dark:text-zinc-300 mb-2`}>Quick Challenge</p>
        <div className="text-zinc-600 dark:text-zinc-400 text-sm leading-relaxed">
          {children}
        </div>
        {northStarNudge && (
          <p className="text-xs italic text-zinc-400 dark:text-zinc-500 mt-3">
            <Zap size={10} className="inline -mt-0.5 mr-1 text-[#CC785C]" />
            Remember: {northStarNudge}
          </p>
        )}
      </div>
    </div>
  </div>
);

interface PersonalStoryProps {
  children: React.ReactNode;
  name: string;
  role?: string;
}

export const PersonalStory = ({ children, name, role }: PersonalStoryProps) => (
  <div className="my-10 rounded-2xl bg-stone-50 dark:bg-stone-900/40 border border-stone-200/60 dark:border-stone-800/60 border-l-[3px] border-l-stone-400 dark:border-l-stone-600 p-8">
    <div className="flex items-center gap-3 mb-4">
      <div className="w-8 h-8 rounded-lg bg-stone-200 dark:bg-stone-800 flex items-center justify-center text-stone-500 dark:text-stone-400 shrink-0">
        <Quote size={14} />
      </div>
      <div className="flex items-center gap-2">
        <span className="text-sm font-bold text-stone-700 dark:text-stone-300">{name}</span>
        {role && (
          <span className="text-[10px] font-semibold uppercase tracking-wider text-stone-400 dark:text-stone-500">{role}</span>
        )}
      </div>
    </div>
    <div className="text-stone-600 dark:text-stone-400 text-sm leading-relaxed italic font-serif">
      {children}
    </div>
  </div>
);

interface ActivityRingProps {
  progress: number;
  color?: string;
  size?: number;
  strokeWidth?: number;
}

export const ActivityRing = ({ progress, color = "#f59e0b", size, strokeWidth }: ActivityRingProps) => {
  const sw = strokeWidth ?? 10;
  const r = size ? (size / 2) - (sw / 2) : 35;
  const vb = size ?? 96;
  const cx = vb / 2;
  const circumference = 2 * Math.PI * r;
  const offset = circumference - (progress / 100) * circumference;
  const px = size ? `${size}px` : '96px';

  return (
    <div className={`relative flex items-center justify-center ${size ? '' : 'w-24 h-24'} mx-auto mb-4`} style={size ? { width: px, height: px } : undefined}>
      <svg className="w-full h-full -rotate-90 overflow-visible" viewBox={`0 0 ${vb} ${vb}`}>
        <circle cx={cx} cy={cx} r={r} stroke={color} strokeWidth={sw} fill="transparent" className="opacity-10" />
        <motion.circle cx={cx} cy={cx} r={r} stroke={color} strokeWidth={sw} fill="transparent" strokeDasharray={circumference} initial={{ strokeDashoffset: circumference }} animate={{ strokeDashoffset: offset }} transition={{ duration: 1.5, ease: "easeOut" }} strokeLinecap="round" style={{ filter: `drop-shadow(0 0 8px ${color}55)` }} />
      </svg>
    </div>
  );
};
