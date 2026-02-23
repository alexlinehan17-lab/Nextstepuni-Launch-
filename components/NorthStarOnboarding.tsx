/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowRight, ArrowLeft, Check, Wallet, Heart, Wrench, GraduationCap, Flame, DoorOpen, Banknote, Car, Home, Users, Briefcase, Rocket, Award, UserPlus, TrendingUp, MicOff, Signpost, Plane, PartyPopper, HandHeart } from 'lucide-react';
import { NorthStarCategory, NorthStar } from '../types';
import { NORTH_STAR_CATEGORIES, VISION_CARDS, CATEGORY_COLORS, CATEGORY_PROMPTS } from '../northStarData';

const MotionDiv = motion.div as any;

const ICON_MAP: Record<string, React.ComponentType<{ size?: number; className?: string }>> = {
  Wallet, Heart, Wrench, GraduationCap, Flame, DoorOpen,
  Banknote, Car, Home, Users, Briefcase, Rocket, Award, UserPlus,
  TrendingUp, MicOff, Signpost, Plane, PartyPopper, HandHeart,
};

interface NorthStarOnboardingProps {
  onComplete: (northStar: NorthStar) => void;
  initialData?: NorthStar | null;
}

const NorthStarOnboarding: React.FC<NorthStarOnboardingProps> = ({ onComplete, initialData }) => {
  const [subStep, setSubStep] = useState<1 | 2 | 3>(1);
  const [direction, setDirection] = useState(1);
  const [selectedCategory, setSelectedCategory] = useState<NorthStarCategory | null>(initialData?.category ?? null);
  const [statement, setStatement] = useState(initialData?.statement ?? '');
  const [selectedCards, setSelectedCards] = useState<Set<string>>(new Set(initialData?.visionBoard ?? []));

  const sortedVisionCards = useMemo(() => {
    if (!selectedCategory) return VISION_CARDS;
    return [...VISION_CARDS].sort((a, b) => {
      const aMatch = a.category === selectedCategory ? 0 : 1;
      const bMatch = b.category === selectedCategory ? 0 : 1;
      return aMatch - bMatch;
    });
  }, [selectedCategory]);

  const toggleCard = (cardId: string) => {
    setSelectedCards(prev => {
      const next = new Set(prev);
      if (next.has(cardId)) {
        next.delete(cardId);
      } else if (next.size < 5) {
        next.add(cardId);
      }
      return next;
    });
  };

  const handleComplete = () => {
    if (!selectedCategory) return;
    const now = new Date().toISOString();
    onComplete({
      category: selectedCategory,
      statement,
      visionBoard: Array.from(selectedCards),
      createdAt: initialData?.createdAt ?? now,
      updatedAt: now,
    });
  };

  const canProceedSub = () => {
    if (subStep === 1) return selectedCategory !== null;
    if (subStep === 2) return statement.trim().length > 0;
    if (subStep === 3) return selectedCards.size >= 3;
    return false;
  };

  const goNextSub = () => {
    if (subStep === 3) {
      handleComplete();
      return;
    }
    setDirection(1);
    setSubStep(s => Math.min(3, s + 1) as 1 | 2 | 3);
  };

  const goBackSub = () => {
    setDirection(-1);
    setSubStep(s => Math.max(1, s - 1) as 1 | 2 | 3);
  };

  const stepVariants = {
    hidden: (dir: number) => ({ opacity: 0, x: dir > 0 ? 40 : -40 }),
    visible: { opacity: 1, x: 0 },
    exit: (dir: number) => ({ opacity: 0, x: dir > 0 ? -40 : 40 }),
  };

  const categoryLabel = selectedCategory ? NORTH_STAR_CATEGORIES.find(c => c.id === selectedCategory)?.label : '';

  return (
    <div className="space-y-6">
      <AnimatePresence mode="wait" custom={direction}>

        {/* Sub-step 1: Pick a category */}
        {subStep === 1 && (
          <MotionDiv key="ns-sub1" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={direction} transition={{ duration: 0.3, ease: 'easeInOut' }}>
            <h2 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white mb-1">What's driving you?</h2>
            <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-8">
              Everyone has a reason for doing the Leaving Cert. Pick the one that feels most like yours.
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {NORTH_STAR_CATEGORIES.map((cat) => {
                const colors = CATEGORY_COLORS[cat.id];
                const isSelected = selectedCategory === cat.id;
                const Icon = ICON_MAP[cat.icon];
                return (
                  <button
                    key={cat.id}
                    onClick={() => setSelectedCategory(cat.id)}
                    className={`flex items-start gap-3.5 p-4 rounded-xl border-2 transition-all text-left ${
                      isSelected
                        ? `${colors.selectedBg} ${colors.selectedBorder} ${colors.text}`
                        : `bg-white/70 dark:bg-white/[0.03] border-zinc-200 dark:border-zinc-700 text-zinc-700 dark:text-zinc-300 hover:border-zinc-300 dark:hover:border-zinc-600`
                    }`}
                  >
                    <div className={`w-10 h-10 rounded-xl flex items-center justify-center shrink-0 ${isSelected ? colors.iconBg : 'bg-zinc-100 dark:bg-zinc-800'}`}>
                      {Icon && <Icon size={20} className={isSelected ? colors.text : 'text-zinc-400 dark:text-zinc-500'} />}
                    </div>
                    <div>
                      <p className="text-sm font-bold">{cat.label}</p>
                      <p className={`text-xs mt-0.5 ${isSelected ? colors.text : 'text-zinc-400 dark:text-zinc-500'}`}>{cat.description}</p>
                    </div>
                    {isSelected && (
                      <div className={`ml-auto shrink-0 w-6 h-6 rounded-full flex items-center justify-center ${colors.selectedBg} ${colors.selectedBorder} border`}>
                        <Check size={12} className={colors.text} />
                      </div>
                    )}
                  </button>
                );
              })}
            </div>
          </MotionDiv>
        )}

        {/* Sub-step 2: Personal statement */}
        {subStep === 2 && (
          <MotionDiv key="ns-sub2" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={direction} transition={{ duration: 0.3, ease: 'easeInOut' }}>
            <h2 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white mb-1">Tell us more</h2>
            <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-2">
              You picked <span className="font-semibold text-[var(--accent-hex)]">"{categoryLabel}"</span>
            </p>
            <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-6">
              {selectedCategory ? CATEGORY_PROMPTS[selectedCategory] : ''}
            </p>
            <textarea
              value={statement}
              onChange={(e) => setStatement(e.target.value)}
              placeholder="Write a sentence or two about what this means to you..."
              maxLength={300}
              rows={4}
              className="w-full p-4 rounded-xl border border-zinc-200 dark:border-zinc-700 bg-white/80 dark:bg-zinc-800 text-zinc-900 dark:text-white text-sm leading-relaxed resize-none focus:outline-none focus:ring-2 focus:ring-[rgba(var(--accent),0.4)] focus:border-[rgba(var(--accent),0.6)] transition-all placeholder:text-zinc-400 dark:placeholder:text-zinc-500"
            />
            <p className="text-right text-[10px] text-zinc-400 dark:text-zinc-500 mt-1">
              {statement.length}/300
            </p>
          </MotionDiv>
        )}

        {/* Sub-step 3: Vision board */}
        {subStep === 3 && (
          <MotionDiv key="ns-sub3" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={direction} transition={{ duration: 0.3, ease: 'easeInOut' }}>
            <h2 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white mb-1">Build Your Vision Board</h2>
            <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-6">
              Pick <span className="font-semibold text-[var(--accent-hex)]">3-5 things</span> that represent what you're working towards. <span className="font-semibold text-[var(--accent-hex)]">{selectedCards.size} selected</span>
            </p>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-2.5">
              {sortedVisionCards.map((card) => {
                const isSelected = selectedCards.has(card.id);
                const colors = CATEGORY_COLORS[card.category];
                const Icon = ICON_MAP[card.icon];
                const isDisabled = !isSelected && selectedCards.size >= 5;
                return (
                  <button
                    key={card.id}
                    onClick={() => toggleCard(card.id)}
                    disabled={isDisabled}
                    className={`flex flex-col items-center gap-2 p-3.5 rounded-xl border-2 transition-all ${
                      isSelected
                        ? `${colors.selectedBg} ${colors.selectedBorder} ${colors.text}`
                        : isDisabled
                        ? 'bg-zinc-100 dark:bg-zinc-800/50 border-zinc-200 dark:border-zinc-700 text-zinc-300 dark:text-zinc-600 cursor-not-allowed'
                        : 'bg-white/70 dark:bg-white/[0.03] border-zinc-200 dark:border-zinc-700 text-zinc-600 dark:text-zinc-400 hover:border-zinc-300 dark:hover:border-zinc-600'
                    }`}
                  >
                    <div className={`w-9 h-9 rounded-lg flex items-center justify-center ${isSelected ? colors.iconBg : 'bg-zinc-100 dark:bg-zinc-800'}`}>
                      {Icon && <Icon size={18} className={isSelected ? colors.text : 'text-zinc-400 dark:text-zinc-500'} />}
                    </div>
                    <span className="text-[11px] font-semibold text-center leading-tight">{card.label}</span>
                    {isSelected && (
                      <div className={`w-5 h-5 rounded-full flex items-center justify-center ${colors.selectedBg} ${colors.selectedBorder} border`}>
                        <Check size={10} className={colors.text} />
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
          {subStep === 3 ? (
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
