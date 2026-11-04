/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { Award,Banknote,BookOpen,Briefcase,Car,Compass,DoorOpen,Flame,GraduationCap,HandHeart,Heart,Home,MicOff,PartyPopper,Plane,Puzzle,Rocket,Signpost,Sparkles,Star,TrendingUp,UserPlus,Users,Wallet,Wrench } from 'lucide-react';
import React from 'react';
import { CATEGORY_COLORS,NORTH_STAR_CATEGORIES,VISION_CARDS } from '../northStarData';
import { type NorthStar } from '../types';
import { MotionDiv } from './Motion';

const ICON_MAP: Record<string, React.ComponentType<{ size?: number; className?: string }>> = {
  Wallet, Heart, Wrench, GraduationCap, Flame, DoorOpen,
  Banknote, Car, Home, Users, Briefcase, Rocket, Award, UserPlus,
  TrendingUp, MicOff, Signpost, Plane, PartyPopper, HandHeart,
  // Junior cycle additions (Phase 5)
  Sparkles, Compass, Star, Puzzle, BookOpen,
};

interface NorthStarCalloutProps {
  northStar: NorthStar;
  variant: 'full' | 'compact' | 'nudge';
  message?: string;
}

const NorthStarCallout: React.FC<NorthStarCalloutProps> = ({ northStar, variant, message }) => {
  const category = NORTH_STAR_CATEGORIES.find(c => c.id === northStar.category);
  const colors = CATEGORY_COLORS[northStar.category];
  const CategoryIcon = category ? ICON_MAP[category.icon] : Star;

  if (variant === 'nudge') {
    const truncated = northStar.statement.length > 60
      ? northStar.statement.slice(0, 60) + '...'
      : northStar.statement;
    return (
      <p className="text-xs italic text-[var(--module-muted)] dark:text-[var(--module-muted)] mt-2 mb-1">
        <Star size={10} className="inline -mt-0.5 mr-1 text-[var(--accent-hex)]" />
        Remember: {truncated}
      </p>
    );
  }

  if (variant === 'compact') {
    return (
      <MotionDiv
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
        className={`my-8 rounded-xl border ${colors.border} ${colors.bg} p-5`}
      >
        <div className="flex items-start gap-3">
          <div className={`w-9 h-9 rounded-lg ${colors.iconBg} flex items-center justify-center shrink-0`}>
            {CategoryIcon && <CategoryIcon size={18} className={colors.text} />}
          </div>
          <div>
            <p className="text-[10px] font-bold uppercase tracking-widest text-[var(--accent-hex)] mb-1">Your North Star</p>
            <p className={`text-sm font-semibold ${colors.text} mb-1`}>{message || category?.label}</p>
            <p className="text-xs text-[var(--module-muted)] dark:text-[var(--module-muted)] italic leading-relaxed">
              "{northStar.statement.length > 120 ? northStar.statement.slice(0, 120) + '...' : northStar.statement}"
            </p>
          </div>
        </div>
      </MotionDiv>
    );
  }

  // Full variant
  const boardCards = VISION_CARDS.filter(c => northStar.visionBoard.includes(c.id));

  return (
    <MotionDiv
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
      className={`mb-8 rounded-2xl border ${colors.border} ${colors.bg} p-6`}
    >
      <div className="flex items-center gap-3 mb-4">
        <div className={`w-10 h-10 rounded-xl ${colors.iconBg} flex items-center justify-center`}>
          {CategoryIcon && <CategoryIcon size={20} className={colors.text} />}
        </div>
        <div>
          <p className="text-[10px] font-bold uppercase tracking-widest text-[var(--accent-hex)]">Your North Star</p>
          <p className={`text-base font-bold ${colors.text}`}>{category?.label}</p>
        </div>
      </div>
      <p className="text-sm text-[var(--module-ink)] dark:text-[var(--module-muted)] italic leading-relaxed mb-4">
        "{northStar.statement}"
      </p>
      {boardCards.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {boardCards.map(card => {
            const Icon = ICON_MAP[card.icon];
            return (
              <span key={card.id} className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full ${colors.selectedBg} ${colors.selectedBorder} border text-[10px] font-semibold ${colors.text}`}>
                {Icon && <Icon size={12} />}
                {card.label}
              </span>
            );
          })}
        </div>
      )}
    </MotionDiv>
  );
};

export default NorthStarCallout;
