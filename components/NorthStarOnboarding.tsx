/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo, useRef } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { Wallet, Heart, Wrench, GraduationCap, Flame, DoorOpen, Banknote, Car, Home, Users, Briefcase, Rocket, Award, UserPlus, TrendingUp, MicOff, Signpost, Plane, PartyPopper, HandHeart, Sparkles, Compass, Star, Puzzle, BookOpen } from 'lucide-react';
import { type NorthStarCategory, type NorthStar } from '../types';
import { type CurriculumLevel } from '../utils/authUtils';
import { CATEGORY_COLORS, VISION_CARD_ART, getActiveCategories, getVisionCardsForLevel } from '../northStarData';
import { Button, TextButton } from './ui/Button';
import { SelectionMark } from './ui/Choice';
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
  const choicesRef = useRef<HTMLDivElement>(null);

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

  // The system's look (area 9): the shared choice tiles (white, a 1px line; chosen, an ink outline and
  // a drawn tick: round for the one reason, a rounded square for the several cards), the type scale,
  // and the charcoal button that says what is still needed. Each card keeps its own drawing.
  const stillNeeded = subStep === 1
    ? (selectedCategory === null ? 'Pick the one that feels most like yours.' : null)
    : (selectedCards.size < minCards ? `Pick ${minCards}-${maxCards} things that represent what you're working towards.` : null);

  return (
    <div className="space-y-6">
      <AnimatePresence mode="wait" custom={direction}>

        {/* Sub-step 1: Pick a category */}
        {subStep === 1 && (
          <MotionDiv key="ns-sub1" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={direction} transition={{ duration: 0.24, ease: [0.2, 0, 0, 1] }}>
            <h2 className="t-heading text-[var(--ink-primary)] mb-1">What's driving you?</h2>
            <p className="t-sub mb-6">
              {curriculumLevel === 'junior'
                ? 'Everyone has a reason for putting in the work. What’s yours?'
                : 'Everyone has a reason for doing the Leaving Cert. Pick the one that feels most like yours.'}
            </p>
            <div ref={choicesRef} tabIndex={-1} className="grid grid-cols-1 sm:grid-cols-2 gap-2" role="radiogroup" aria-label="What's driving you?">
              {activeCategories.map((cat) => {
                const colors = CATEGORY_COLORS[cat.id];
                const isSelected = selectedCategory === cat.id;
                const Icon = ICON_MAP[cat.icon];
                const blobCfg = CATEGORY_BLOBS[cat.id];
                return (
                  <button
                    key={cat.id}
                    type="button"
                    role="radio"
                    aria-checked={isSelected}
                    onClick={() => setSelectedCategory(cat.id)}
                    className="ui-part ui-choice text-left"
                  >
                    {blobCfg ? (
                      <CategoryIconBlob config={blobCfg} size={48} />
                    ) : (
                      <span className="w-12 h-12 flex items-center justify-center shrink-0">
                        {Icon && <Icon size={22} className={colors.text} />}
                      </span>
                    )}
                    <span className="ui-choice-body">
                      <span className="ui-choice-label">{cat.label}</span>
                      {' '}<span className="ui-choice-meta">{cat.description}</span>
                    </span>
                    <SelectionMark on={isSelected} />
                  </button>
                );
              })}
            </div>
          </MotionDiv>
        )}

        {/* Sub-step 2: Vision board */}
        {subStep === 2 && (
          <MotionDiv key="ns-sub2" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={direction} transition={{ duration: 0.24, ease: [0.2, 0, 0, 1] }}>
            <h2 className="t-heading text-[var(--ink-primary)] mb-1">Build Your Vision Board</h2>
            <p className="t-sub mb-6">
              Pick <span className="text-[var(--ink-primary)]">{minCards}-{maxCards} things</span> that represent what you're working towards. <span className="text-[var(--ink-primary)]">{selectedCards.size} selected</span>
            </p>
            <div ref={choicesRef} tabIndex={-1} className="grid grid-cols-2 sm:grid-cols-3 gap-2" role="group" aria-label="Build Your Vision Board">
              {sortedVisionCards.map((card) => {
                const isSelected = selectedCards.has(card.id);
                const colors = CATEGORY_COLORS[card.category];
                const Icon = ICON_MAP[card.icon];
                const isDisabled = !isSelected && selectedCards.size >= maxCards;
                const visionIcon = VISION_CARD_ART[card.id];
                const categoryBlob = CATEGORY_BLOBS[card.category];
                return (
                  <button
                    key={card.id}
                    type="button"
                    role="checkbox"
                    aria-checked={isSelected}
                    onClick={() => toggleCard(card.id)}
                    disabled={isDisabled}
                    className="ui-part ui-choice ui-choice--tile disabled:opacity-60"
                  >
                    {visionIcon && categoryBlob ? (
                      <CategoryIconBlob
                        config={{ iconPath: visionIcon, blob: categoryBlob.blob, blobPath: categoryBlob.blobPath }}
                        size={48}
                      />
                    ) : (
                      <span className="w-9 h-9 flex items-center justify-center">
                        {Icon && <Icon size={18} className={colors.text} />}
                      </span>
                    )}
                    <span className="ui-choice-body">
                      <span className="ui-choice-label">{card.label}</span>
                    </span>
                    <SelectionMark on={isSelected} shape="square" />
                  </button>
                );
              })}
            </div>
          </MotionDiv>
        )}
      </AnimatePresence>

      {/* Internal navigation */}
      <div className="flex items-end justify-between gap-4 pt-2">
        {subStep > 1 ? (
          <TextButton tone="quiet" onClick={goBackSub}>Back</TextButton>
        ) : <span />}
        <Button
          kind="main"
          arrow={subStep === 2 ? undefined : 'forward'}
          missing={stillNeeded ? { sentence: stillNeeded, goTo: choicesRef } : undefined}
          onClick={goNextSub}
        >
          {subStep === 2 ? 'Save My North Star' : 'Continue'}
        </Button>
      </div>
    </div>
  );
};

export default NorthStarOnboarding;
