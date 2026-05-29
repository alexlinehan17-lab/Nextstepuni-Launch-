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
import { CATEGORY_COLORS, getActiveCategories, getVisionCardsForLevel } from '../northStarData';

const ICON_MAP: Record<string, React.ComponentType<{ size?: number; className?: string }>> = {
  Wallet, Heart, Wrench, GraduationCap, Flame, DoorOpen,
  Banknote, Car, Home, Users, Briefcase, Rocket, Award, UserPlus,
  TrendingUp, MicOff, Signpost, Plane, PartyPopper, HandHeart,
  // Junior cycle additions (Phase 5)
  Sparkles, Compass, Star, Puzzle, BookOpen,
};

// Custom hand-drawn illustrations for the "What's driving you?" category
// picker. Each category has a soft pastel painted blob behind the hand-drawn
// PNG, modelled on the Innovation Zone ToolIconBlob. The blob paths are
// slightly different per category so the six tiles don't read as identical.
interface CategoryBlobConfig {
  iconPath: string;
  blob: string;
  blobPath: string;
}

// Vision board icons (sub-step 3). Each PNG matches a VISION_CARDS id and
// is rendered behind the category-coloured blob from CATEGORY_BLOBS.
const VISION_ICON_IMG: Record<string, string> = {
  'first-paycheck': '/icons/north-star/vision/first-paycheck.png',
  'own-car': '/icons/north-star/vision/own-car.png',
  'own-place': '/icons/north-star/vision/own-place.png',
  'family-proud': '/icons/north-star/vision/family-proud.png',
  'role-model': '/icons/north-star/vision/role-model.png',
  'giving-back': '/icons/north-star/vision/giving-back.png',
  'dream-job': '/icons/north-star/vision/dream-job.png',
  'own-thing': '/icons/north-star/vision/own-thing.png',
  'skilled-trade': '/icons/north-star/vision/skilled-trade.png',
  'campus': '/icons/north-star/vision/campus.png',
  'scholarship': '/icons/north-star/vision/scholarship.png',
  'new-people': '/icons/north-star/vision/new-people.png',
  'results-day': '/icons/north-star/vision/results-day.png',
  'beating-odds': '/icons/north-star/vision/beating-odds.png',
  'silence-doubters': '/icons/north-star/vision/silence-doubters.png',
  'real-choices': '/icons/north-star/vision/real-choices.png',
  'see-world': '/icons/north-star/vision/see-world.png',
  'freedom-no': '/icons/north-star/vision/freedom-no.png',
  // ─── JC vision cards (Phase 5) ───────────────────────────────────────
  // 8 reuse senior PNGs where concepts map 1:1; 4 use bespoke JC art
  // (jc-really-good, jc-solve-hard, jc-subject-choice, jc-try-new) added
  // 2026-05-24.
  'jc-family-proud': '/icons/north-star/vision/family-proud.png',
  'jc-role-model': '/icons/north-star/vision/role-model.png',
  'jc-giving-back': '/icons/north-star/vision/giving-back.png',
  'jc-beating-odds': '/icons/north-star/vision/beating-odds.png',
  'jc-silence-doubters': '/icons/north-star/vision/silence-doubters.png',
  'jc-results-day': '/icons/north-star/vision/results-day.png',
  'jc-mastering-skill': '/icons/north-star/vision/skilled-trade.png',
  'jc-real-choices': '/icons/north-star/vision/real-choices.png',
  'jc-really-good': '/icons/north-star/vision/jc-really-good.png',
  'jc-solve-hard': '/icons/north-star/vision/jc-solve-hard.png',
  'jc-subject-choice': '/icons/north-star/vision/jc-subject-choice.png',
  'jc-try-new': '/icons/north-star/vision/jc-try-new.png',
};

const CATEGORY_BLOBS: Partial<Record<NorthStarCategory, CategoryBlobConfig>> = {
  'independence': {
    iconPath: '/icons/north-star/my-own-path.png',
    blob: '#DDC9A4',
    blobPath: 'M 6 24 Q -2 52 8 78 Q 24 98 52 94 Q 86 90 94 62 Q 100 30 84 10 Q 60 -4 32 4 Q 12 12 6 24 Z',
  },
  'family-community': {
    iconPath: '/icons/north-star/community.png',
    blob: '#ECBBCC',
    blobPath: 'M 4 28 Q 0 56 12 82 Q 28 100 56 96 Q 90 92 96 60 Q 100 28 82 8 Q 56 -6 30 6 Q 10 16 4 28 Z',
  },
  'career-craft': {
    iconPath: '/icons/north-star/career.png',
    blob: '#F5C7A0',
    blobPath: 'M 8 22 Q 0 48 6 76 Q 20 96 50 96 Q 84 96 94 70 Q 100 40 84 14 Q 64 -2 36 4 Q 14 12 8 22 Z',
  },
  'college-learning': {
    iconPath: '/icons/north-star/learning.png',
    blob: '#BCCCE3',
    blobPath: 'M 6 22 Q -2 50 10 78 Q 26 98 56 94 Q 90 88 96 56 Q 100 24 80 6 Q 56 -6 28 6 Q 10 14 6 22 Z',
  },
  'prove-myself': {
    iconPath: '/icons/north-star/prove-them-wrong.png',
    blob: '#F1B7AB',
    blobPath: 'M 4 26 Q 2 56 12 82 Q 26 98 52 96 Q 88 94 96 64 Q 100 34 84 10 Q 60 -4 30 6 Q 10 18 4 26 Z',
  },
  'options-freedom': {
    iconPath: '/icons/north-star/open-options.png',
    blob: '#B5D4CC',
    blobPath: 'M 8 26 Q 0 50 8 78 Q 22 96 54 96 Q 88 94 96 64 Q 100 32 80 10 Q 56 -2 28 8 Q 12 16 8 26 Z',
  },
  // ─── JC categories (Phase 5) ─────────────────────────────────────────
  // Reuse the senior category PNGs since the underlying themes map 1:1.
  // Distinct blob colours so the JC view still feels its own visually.
  'family-people': {
    iconPath: '/icons/north-star/community.png',
    blob: '#ECBBCC',
    blobPath: 'M 4 28 Q 0 56 12 82 Q 28 100 56 96 Q 90 92 96 60 Q 100 28 82 8 Q 56 -6 30 6 Q 10 16 4 28 Z',
  },
  'prove-myself-jc': {
    iconPath: '/icons/north-star/prove-them-wrong.png',
    blob: '#F1B7AB',
    blobPath: 'M 4 26 Q 2 56 12 82 Q 26 98 52 96 Q 88 94 96 64 Q 100 34 84 10 Q 60 -4 30 6 Q 10 18 4 26 Z',
  },
  'curiosity-craft': {
    iconPath: '/icons/north-star/career.png',
    blob: '#F5C7A0',
    blobPath: 'M 8 22 Q 0 48 6 76 Q 20 96 50 96 Q 84 96 94 70 Q 100 40 84 14 Q 64 -2 36 4 Q 14 12 8 22 Z',
  },
  'future-doors': {
    iconPath: '/icons/north-star/open-options.png',
    blob: '#B5D4CC',
    blobPath: 'M 8 26 Q 0 50 8 78 Q 22 96 54 96 Q 88 94 96 64 Q 100 32 80 10 Q 56 -2 28 8 Q 12 16 8 26 Z',
  },
};

// Renders an icon + organic painted blob behind it. The icon is sized
// slightly bigger than the blob so it spills past the edges — matches the
// Innovation Zone aesthetic.
const CategoryIconBlob: React.FC<{ config: CategoryBlobConfig; size: number }> = ({ config, size }) => (
  <div
    className="relative shrink-0"
    style={{ width: size, height: size, overflow: 'visible' }}
    aria-hidden
  >
    <svg
      className="absolute pointer-events-none"
      viewBox="0 0 100 100"
      preserveAspectRatio="xMidYMid meet"
      style={{
        width: '88%',
        height: '88%',
        left: '50%',
        top: '50%',
        transform: 'translate(-50%, -50%)',
        zIndex: 0,
      }}
    >
      <path d={config.blobPath} fill={config.blob} opacity="0.85" />
    </svg>
    <img
      src={config.iconPath}
      alt=""
      style={{
        position: 'absolute',
        left: '50%',
        top: '50%',
        transform: 'translate(-50%, -50%)',
        width: '105%',
        height: '105%',
        objectFit: 'contain',
        zIndex: 1,
      }}
      draggable={false}
    />
  </div>
);

interface NorthStarOnboardingProps {
  onComplete: (northStar: NorthStar) => void;
  initialData?: NorthStar | null;
  /** Curriculum level controls which themes + vision cards are shown.
   *  Senior sees the 6 senior themes + 18 senior cards; junior sees the
   *  4 JC themes + 12 JC cards. Defaults to 'senior' for back-compat. */
  curriculumLevel?: CurriculumLevel;
}

const NorthStarOnboarding: React.FC<NorthStarOnboardingProps> = ({ onComplete, initialData, curriculumLevel = 'senior' }) => {
  // Sub-step flow simplified to 2 steps (picker → vision board). The old
  // "Tell us more" textarea step was removed — the displayed
  // northStar.statement now defaults to the chosen category's own
  // first-person description (e.g. "I want to make my family proud…"),
  // which already reads as a personal "why" quote on the rank card and
  // surfaces like Knowledge Tree's North Star line. Existing accounts
  // with a typed statement keep theirs via initialData.
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
    // Fall back to the category's first-person description if the user
    // has no statement saved. Preserves existing typed statements from
    // pre-removal accounts.
    const catDescription = activeCategories.find(c => c.id === selectedCategory)?.description ?? '';
    const finalStatement = statement.trim() || catDescription;
    onComplete({
      category: selectedCategory,
      statement: finalStatement,
      visionBoard: Array.from(selectedCards),
      createdAt: initialData?.createdAt ?? now,
      updatedAt: now,
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
                // Selection language now matches the rest of the app:
                // accent-tint background + accent border + chunky offset
                // shadow. The painted blob carries category identity; the
                // background doesn't need to rainbow-shift per category.
                return (
                  <button
                    key={cat.id}
                    onClick={() => setSelectedCategory(cat.id)}
                    className={`flex items-center gap-3.5 p-4 rounded-xl border-2 transition-all duration-150 text-left text-[#1A1A1A] dark:text-zinc-100 ${
                      isSelected
                        ? 'bg-[#FDEEDF] dark:bg-[rgba(242,107,31,0.14)] border-[#F26B1F] shadow-[4px_4px_0_0_#1A1A1A] dark:shadow-[4px_4px_0_0_#3f3f46]'
                        : 'bg-white dark:bg-zinc-900 border-[#EDEBE8] dark:border-zinc-700 hover:-translate-y-0.5 hover:shadow-[2px_2px_0_0_#1A1A1A] dark:hover:shadow-[2px_2px_0_0_#3f3f46]'
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
                const visionIcon = VISION_ICON_IMG[card.id];
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
