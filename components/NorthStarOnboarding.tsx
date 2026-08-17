/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { ArrowRight, ArrowLeft, Check, Wallet, Heart, Wrench, GraduationCap, Flame, DoorOpen, Banknote, Car, Home, Users, Briefcase, Rocket, Award, UserPlus, TrendingUp, MicOff, Signpost, Plane, PartyPopper, HandHeart, Sparkles, Compass, Star, Puzzle, BookOpen } from 'lucide-react';
import { type NorthStarCategory, type NorthStar } from '../types';
import { type CurriculumLevel } from '../utils/authUtils';
import { CATEGORY_COLORS, VISION_CARD_ART, getActiveCategories, getVisionCardsForLevel } from '../northStarData';
import { CategoryIconBlob, NORTH_STAR_CATEGORY_BLOBS as CATEGORY_BLOBS } from './NorthStarCategoryIcon';

const ICON_MAP: Record<string, React.ComponentType<{ size?: number; className?: string }>> = {
  Wallet, Heart, Wrench, GraduationCap, Flame, DoorOpen,
  Banknote, Car, Home, Users, Briefcase, Rocket, Award, UserPlus,
  TrendingUp, MicOff, Signpost, Plane, PartyPopper, HandHeart,
  // Junior cycle additions (Phase 5)
  Sparkles, Compass, Star, Puzzle, BookOpen,
};

interface NorthStarOnboardingProps {
  onComplete: (northStar: NorthStar) => void;
  initialData?: NorthStar | null;
  /** Curriculum level controls which themes + vision cards are shown.
   *  Senior sees the 6 senior themes + 18 senior cards; junior sees the
   *  4 JC themes + 12 JC cards. Defaults to 'senior' for back-compat. */
  curriculumLevel?: CurriculumLevel;
}

const NorthStarOnboarding: React.FC<NorthStarOnboardingProps> = ({ onComplete, initialData, curriculumLevel = 'senior' }) => {
  // Selection-only by design: students choose a direction and supporting
  // images here. Existing student-authored wording is preserved, but generic
  // category copy is explicitly marked as system-authored downstream.
  const [subStep, setSubStep] = useState<1 | 2>(1);
  const [direction, setDirection] = useState(1);
  const [selectedCategory, setSelectedCategory] = useState<NorthStarCategory | null>(initialData?.category ?? null);
  const [statement] = useState(initialData?.statement ?? '');
  const [selectedCards, setSelectedCards] = useState<Set<string>>(new Set(initialData?.visionBoard ?? []));

  const activeCategories = useMemo(() => getActiveCategories(curriculumLevel), [curriculumLevel]);
  const activeVisionCards = useMemo(() => getVisionCardsForLevel(curriculumLevel), [curriculumLevel]);

  const sortedVisionCards = useMemo(() => {
    if (!selectedCategory) return activeVisionCards;
    return [...activeVisionCards].sort((a, b) => {
      const aMatch = a.category === selectedCategory ? 0 : 1;
      const bMatch = b.category === selectedCategory ? 0 : 1;
      return aMatch - bMatch;
    });
  }, [selectedCategory, activeVisionCards]);

  // Vision board bounds — JC has fewer cards per theme (3 vs 6) so the
  // minimum and maximum scale down. Picking 2-of-3 in your chosen JC theme
  // feels appropriate; picking 3-of-6 in a senior theme is the existing
  // mental model.
  const minCards = curriculumLevel === 'junior' ? 2 : 3;
  const maxCards = curriculumLevel === 'junior' ? 3 : 5;

  const toggleCard = (cardId: string) => {
    setSelectedCards(prev => {
      const next = new Set(prev);
      if (next.has(cardId)) {
        next.delete(cardId);
      } else if (next.size < maxCards) {
        next.add(cardId);
      }
      return next;
    });
  };

  const handleComplete = () => {
    if (!selectedCategory) return;
    const now = new Date().toISOString();
    // Category copy seeds the direction without asking for personal free text.
    const catDescription = activeCategories.find(c => c.id === selectedCategory)?.description ?? '';
    const finalStatement = statement.trim() || catDescription;
    onComplete({
      category: selectedCategory,
      statement: finalStatement,
      visionBoard: Array.from(selectedCards),
      createdAt: initialData?.createdAt ?? now,
      updatedAt: now,
      authoredByStudent: initialData?.authoredByStudent ?? Boolean(statement.trim()),
      reviewedAt: now,
    });
  };

  const canProceedSub = () => {
    if (subStep === 1) return selectedCategory !== null;
    if (subStep === 2) return selectedCards.size >= minCards;
    return false;
  };

  const goNextSub = () => {
    if (subStep === 2) {
      handleComplete();
      return;
    }
    setDirection(1);
    setSubStep(s => Math.min(2, s + 1) as 1 | 2);
  };

  const goBackSub = () => {
    setDirection(-1);
    setSubStep(s => Math.max(1, s - 1) as 1 | 2);
  };

  const stepVariants = {
    hidden: (dir: number) => ({ opacity: 0, x: dir > 0 ? 40 : -40 }),
    visible: { opacity: 1, x: 0 },
    exit: (dir: number) => ({ opacity: 0, x: dir > 0 ? -40 : 40 }),
  };

  return (
    <div className="space-y-6">
      <AnimatePresence mode="wait" custom={direction}>

        {/* Sub-step 1: Pick a category */}
        {subStep === 1 && (
          <MotionDiv key="ns-sub1" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={direction} transition={{ duration: 0.3, ease: 'easeInOut' }}>
            <h2 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white mb-1">What's driving you?</h2>
            <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-8">
              {curriculumLevel === 'junior'
                ? 'Everyone has a reason for putting in the work. What’s yours?'
                : 'Everyone has a reason for doing the Leaving Cert. Pick the one that feels most like yours.'}
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {activeCategories.map((cat) => {
                const colors = CATEGORY_COLORS[cat.id];
                const isSelected = selectedCategory === cat.id;
                const Icon = ICON_MAP[cat.icon];
                const blobCfg = CATEGORY_BLOBS[cat.id];
                // Every card gets the full chunky-shadow + black border
                // grammar so the unselected ones don't read as "undesigned"
                // next to the selected. Selection is communicated by the
                // accent-tint background + accent border swap only — same
                // pattern as YearTransitionFlow's TY-vs-5th picker.
                return (
                  <button
                    key={cat.id}
                    onClick={() => setSelectedCategory(cat.id)}
                    className={`flex items-center gap-3.5 p-4 rounded-2xl border-2 text-left text-[#1A1A1A] dark:text-zinc-100 shadow-[4px_4px_0_0_#1A1A1A] dark:shadow-[4px_4px_0_0_#3f3f46] hover:-translate-y-0.5 hover:shadow-[6px_6px_0_0_#1A1A1A] dark:hover:shadow-[6px_6px_0_0_#3f3f46] active:translate-x-1 active:translate-y-1 active:shadow-[0px_0px_0_0_#1A1A1A] dark:active:shadow-[0px_0px_0_0_#3f3f46] transition-all duration-150 ${
                      isSelected
                        ? 'bg-[#FDEEDF] dark:bg-[rgba(242,107,31,0.14)] border-[#F26B1F]'
                        : 'bg-white dark:bg-zinc-900 border-[#1A1A1A] dark:border-zinc-600'
                    }`}
                  >
                    {blobCfg ? (
                      <CategoryIconBlob config={blobCfg} size={64} />
                    ) : (
                      <div className={`w-14 h-14 rounded-xl flex items-center justify-center shrink-0 ${isSelected ? colors.iconBg : 'bg-zinc-100 dark:bg-zinc-800'}`}>
                        {Icon && <Icon size={22} className={isSelected ? colors.text : 'text-zinc-400 dark:text-zinc-500'} />}
                      </div>
                    )}
                    <div>
                      <p className="text-sm font-bold">{cat.label}</p>
                      <p className={`text-xs mt-0.5 ${isSelected ? 'text-[#8C3A0E] dark:text-zinc-300' : 'text-zinc-500 dark:text-zinc-400'}`}>{cat.description}</p>
                    </div>
                    {isSelected && (
                      <div className="ml-auto shrink-0 w-6 h-6 rounded-full flex items-center justify-center bg-[#F26B1F]">
                        <Check size={12} className="text-white" strokeWidth={3} />
                      </div>
                    )}
                  </button>
                );
              })}
            </div>
          </MotionDiv>
        )}

        {/* Sub-step 2: Vision board */}
        {subStep === 2 && (
          <MotionDiv key="ns-sub2" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={direction} transition={{ duration: 0.3, ease: 'easeInOut' }}>
            <h2 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white mb-1">Build Your Vision Board</h2>
            <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-6">
              Pick <span className="font-semibold text-[var(--accent-hex)]">{minCards}-{maxCards} things</span> that represent what you're working towards. <span className="font-semibold text-[var(--accent-hex)]">{selectedCards.size} selected</span>
            </p>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-2.5">
              {sortedVisionCards.map((card) => {
                const isSelected = selectedCards.has(card.id);
                const colors = CATEGORY_COLORS[card.category];
                const Icon = ICON_MAP[card.icon];
                const isDisabled = !isSelected && selectedCards.size >= maxCards;
                const visionIcon = VISION_CARD_ART[card.id];
                const categoryBlob = CATEGORY_BLOBS[card.category];
                // Same selection language as the category picker above —
                // accent-tint + accent border + offset shadow, scaled
                // smaller (3px shadow) for the tighter tile grid.
                return (
                  <button
                    key={card.id}
                    onClick={() => toggleCard(card.id)}
                    disabled={isDisabled}
                    className={`flex flex-col items-center gap-2 p-3.5 rounded-xl border-2 transition-all duration-150 text-[#1A1A1A] dark:text-zinc-100 ${
                      isSelected
                        ? 'bg-[#FDEEDF] dark:bg-[rgba(242,107,31,0.14)] border-[#F26B1F] shadow-[3px_3px_0_0_#1A1A1A] dark:shadow-[3px_3px_0_0_#3f3f46]'
                        : isDisabled
                        ? 'bg-zinc-50 dark:bg-zinc-800/50 border-zinc-200 dark:border-zinc-700 text-zinc-300 dark:text-zinc-600 cursor-not-allowed'
                        : 'bg-white dark:bg-zinc-900 border-[#EDEBE8] dark:border-zinc-700 hover:-translate-y-0.5 hover:shadow-[2px_2px_0_0_#1A1A1A] dark:hover:shadow-[2px_2px_0_0_#3f3f46]'
                    }`}
                  >
                    {visionIcon && categoryBlob ? (
                      <CategoryIconBlob
                        config={{ iconPath: visionIcon, blob: categoryBlob.blob, blobPath: categoryBlob.blobPath }}
                        size={56}
                      />
                    ) : (
                      <div className={`w-9 h-9 rounded-lg flex items-center justify-center ${isSelected ? colors.iconBg : 'bg-zinc-100 dark:bg-zinc-800'}`}>
                        {Icon && <Icon size={18} className={isSelected ? colors.text : 'text-zinc-400 dark:text-zinc-500'} />}
                      </div>
                    )}
                    <span className="text-[11px] font-semibold text-center leading-tight">{card.label}</span>
                    {isSelected && (
                      <div className="w-5 h-5 rounded-full flex items-center justify-center bg-[#F26B1F]">
                        <Check size={10} className="text-white" strokeWidth={3} />
                      </div>
                    )}
                  </button>
                );
              })}
            </div>
          </MotionDiv>
        )}
      </AnimatePresence>

      {/* Internal navigation */}
      <div className="flex items-center justify-between pt-4">
        {subStep > 1 ? (
          <button onClick={goBackSub} className="flex items-center gap-1.5 text-sm font-medium text-zinc-400 dark:text-zinc-500 hover:text-zinc-600 dark:hover:text-zinc-300 transition-colors">
            <ArrowLeft size={14} /> Back
          </button>
        ) : <div />}
        <button
          onClick={goNextSub}
          disabled={!canProceedSub()}
          className="flex items-center gap-2 px-6 py-2.5 bg-[var(--accent-hex)] text-white font-semibold text-sm rounded-full hover:bg-[var(--accent-dark-hex)] transition-colors disabled:opacity-40 disabled:cursor-not-allowed shadow-lg shadow-[rgba(var(--accent),0.2)]"
        >
          {subStep === 2 ? (
            <><Check size={14} /> Save My North Star</>
          ) : (
            <>Continue <ArrowRight size={14} /></>
          )}
        </button>
      </div>
    </div>
  );
};

export default NorthStarOnboarding;
