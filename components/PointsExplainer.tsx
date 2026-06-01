/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * PointsExplainer — primer modal shown on first study-mode entry, walking
 * the student through how they earn and spend XP.
 *
 * Visual register matches the rest of the app post-2026-05 aesthetic pass:
 * cream surface + chunky-shadow card grammar + painted-blob icons + the
 * canonical accent CTA. No dark gradient hero, no flat pill buttons.
 */

import React from 'react';
import { createPortal } from 'react-dom';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { useModal } from '../hooks/useModal';
import { BookOpen, Timer, Trophy, Gem, MapPin, SkipForward, CalendarOff, X, ArrowRight, Sparkles, type LucideIcon } from 'lucide-react';
import { COLORS } from '../design/tokens';

interface PointsExplainerProps {
  isOpen: boolean;
  onDismiss: () => void;
}

// Soft painted-blob recipe — same as AchievementGallery / Training Hub
// North Star card. Slight asymmetry so it feels hand-drawn.
const BLOB_PATH = 'M 38 4 Q 12 6 6 28 Q 2 50 22 56 Q 50 62 60 36 Q 64 12 48 4 Q 42 2 38 4 Z';

interface EarnItem {
  icon: LucideIcon;
  label: string;
  value: string;
  unit: string;
  highlight?: boolean;
}

const EARN_ITEMS: EarnItem[] = [
  { icon: Timer, label: 'Study session', value: '15', unit: 'pts / 10 min', highlight: true },
  { icon: BookOpen, label: 'Module section', value: '10', unit: 'pts each' },
  { icon: Trophy, label: 'Complete a module', value: '+30', unit: 'bonus' },
  { icon: Gem, label: 'Quests & challenges', value: '25–200', unit: 'pts' },
];

interface SpendItem {
  icon: LucideIcon;
  label: string;
  cost: string;
  desc: string;
}

const SPEND_ITEMS: SpendItem[] = [
  { icon: MapPin, label: 'Island shop', cost: 'Varies', desc: 'Build your island' },
  { icon: SkipForward, label: 'Skip a block', cost: '20 pts', desc: 'Skip one study session' },
  { icon: CalendarOff, label: 'Rest day pass', cost: '60 pts', desc: 'Day off, streak safe' },
];

// Tiny painted-blob + ink-icon. blob fill = accent-tint var so it reads
// soft on the cream surface; ink is the saturated accent.
const BlobIcon: React.FC<{ Icon: LucideIcon; size?: number; iconSize?: number }> = ({
  Icon, size = 44, iconSize = 18,
}) => (
  <div className="relative shrink-0" style={{ width: size, height: size }}>
    <svg viewBox="0 0 64 64" className="absolute inset-0 w-full h-full" aria-hidden="true">
      <path d={BLOB_PATH} fill="var(--accent-tint-hex)" opacity="0.9" />
    </svg>
    <div className="absolute inset-0 flex items-center justify-center">
      <Icon size={iconSize} style={{ color: COLORS.accent }} strokeWidth={2} />
    </div>
  </div>
);

const PointsExplainer: React.FC<PointsExplainerProps> = ({ isOpen, onDismiss }) => {
  useModal(isOpen, onDismiss);

  return createPortal(
    <AnimatePresence>
      {isOpen && (
        <MotionDiv
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.2 }}
          className="fixed inset-0 z-[300] flex items-center justify-center bg-black/55 backdrop-blur-sm p-4"
          onClick={onDismiss}
        >
          <MotionDiv
            initial={{ opacity: 0, scale: 0.96, y: 12 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.96, y: 12 }}
            transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] as number[] }}
            className="w-full max-w-md bg-[#FAFBF6] dark:bg-zinc-900 rounded-2xl border-2 border-[#1A1A1A] dark:border-zinc-700 shadow-[6px_6px_0_0_#1A1A1A] dark:shadow-[6px_6px_0_0_#3f3f46] max-h-[90vh] flex flex-col overflow-hidden"
            onClick={(e: React.MouseEvent) => e.stopPropagation()}
          >
            {/* Header — fixed, painted-blob illustration on the left */}
            <div className="flex items-start gap-4 p-6 pb-5 shrink-0">
              <BlobIcon Icon={Sparkles} size={56} iconSize={26} />
              <div className="flex-1 min-w-0">
                <p style={{ fontFamily: "'DM Sans', sans-serif", fontSize: '10px', fontWeight: 700, letterSpacing: '0.18em', color: 'var(--text-label)', textTransform: 'uppercase', margin: 0 }}>
                  Your Points
                </p>
                <h2 style={{ fontFamily: "'Source Serif 4', serif", fontSize: '24px', fontWeight: 600, color: 'var(--text-primary)', lineHeight: 1.1, margin: '6px 0 4px 0' }}>
                  Study more, earn more
                </h2>
                <p style={{ fontFamily: "'DM Sans', sans-serif", fontSize: '13px', color: 'var(--text-muted)', margin: 0, lineHeight: 1.4 }}>
                  Every session builds your island.
                </p>
              </div>
              <button
                onClick={onDismiss}
                className="w-8 h-8 rounded-lg flex items-center justify-center hover:bg-black/5 dark:hover:bg-white/10 transition-colors shrink-0"
                aria-label="Close"
              >
                <X size={18} className="text-zinc-500" />
              </button>
            </div>

            {/* Body — scrolls when content exceeds the viewport-capped modal. */}
            <div className="px-6 overflow-y-auto flex-1 min-h-0">

              {/* Earn grid — 2x2 chunky-shadow cards. The Study Session card
                  is highlighted with accent-tint bg + accent border, same
                  as the canonical selection state. */}
              <p style={{ fontFamily: "'DM Sans', sans-serif", fontSize: '10px', fontWeight: 700, letterSpacing: '0.18em', color: 'var(--text-label)', textTransform: 'uppercase', margin: '0 0 10px 0' }}>
                Earn
              </p>
              <div className="grid grid-cols-2 gap-3 mb-5">
                {EARN_ITEMS.map((item) => {
                  const Icon = item.icon;
                  return (
                    <div
                      key={item.label}
                      className={`rounded-xl p-3 border-2 ${
                        item.highlight
                          ? 'bg-[#FDEEDF] dark:bg-[rgba(242,107,31,0.14)] border-[#F26B1F] shadow-[3px_3px_0_0_#1A1A1A] dark:shadow-[3px_3px_0_0_#3f3f46]'
                          : 'bg-white dark:bg-zinc-800 border-[#1A1A1A] dark:border-zinc-600 shadow-[3px_3px_0_0_#1A1A1A] dark:shadow-[3px_3px_0_0_#3f3f46]'
                      }`}
                    >
                      <div className="flex items-center gap-1.5 mb-2">
                        <Icon size={14} style={{ color: item.highlight ? COLORS.accent : 'var(--text-muted)' }} strokeWidth={2.25} />
                        <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: '11px', fontWeight: 600, color: 'var(--text-muted)' }}>
                          {item.label}
                        </span>
                      </div>
                      <div className="flex items-baseline gap-1">
                        <span style={{ fontFamily: "'Source Serif 4', serif", fontSize: '22px', fontWeight: 700, color: item.highlight ? COLORS.accent : 'var(--text-primary)', lineHeight: 1 }}>
                          {item.value}
                        </span>
                        <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: '11px', color: 'var(--text-label)' }}>
                          {item.unit}
                        </span>
                      </div>
                    </div>
                  );
                })}
              </div>

              {/* Spend rows — chunky-shadow row + painted-blob icon */}
              <p style={{ fontFamily: "'DM Sans', sans-serif", fontSize: '10px', fontWeight: 700, letterSpacing: '0.18em', color: 'var(--text-label)', textTransform: 'uppercase', margin: '0 0 10px 0' }}>
                Spend
              </p>
              <div className="flex flex-col gap-2 pb-6">
                {SPEND_ITEMS.map((item) => (
                  <div
                    key={item.label}
                    className="flex items-center gap-3 p-3 rounded-xl bg-white dark:bg-zinc-800 border-2 border-[#1A1A1A] dark:border-zinc-600 shadow-[2px_2px_0_0_#1A1A1A] dark:shadow-[2px_2px_0_0_#3f3f46]"
                  >
                    <BlobIcon Icon={item.icon} size={40} iconSize={16} />
                    <div className="flex-1 min-w-0">
                      <p style={{ fontFamily: "'DM Sans', sans-serif", fontSize: '13px', fontWeight: 700, color: 'var(--text-primary)', margin: 0, lineHeight: 1.2 }}>
                        {item.label}
                      </p>
                      <p style={{ fontFamily: "'DM Sans', sans-serif", fontSize: '11px', color: 'var(--text-muted)', margin: '2px 0 0 0', lineHeight: 1.3 }}>
                        {item.desc}
                      </p>
                    </div>
                    <span style={{ fontFamily: "'Source Serif 4', serif", fontSize: '13px', fontWeight: 700, color: COLORS.accent, flexShrink: 0 }}>
                      {item.cost}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Footer CTA — canonical chunky-shadow accent button, fixed
                below the scrolling body so it never disappears off-screen. */}
            <div className="px-6 pb-6 pt-2 shrink-0 border-t border-black/[0.04] dark:border-white/[0.06]">
              <button
                onClick={onDismiss}
                className="w-full flex items-center justify-center gap-2 px-5 py-3 rounded-2xl border-2 border-[#1A1A1A] bg-[#F26B1F] text-[#FDF8F0] font-sans font-bold text-sm shadow-[4px_4px_0_0_#1A1A1A] dark:shadow-[4px_4px_0_0_#3f3f46] hover:shadow-[6px_6px_0_0_#1A1A1A] dark:hover:shadow-[6px_6px_0_0_#3f3f46] hover:-translate-y-0.5 active:translate-x-1 active:translate-y-1 active:shadow-[0px_0px_0_0_#1A1A1A] dark:active:shadow-[0px_0px_0_0_#3f3f46] transition-all duration-150"
              >
                Let's go
                <ArrowRight size={14} />
              </button>
            </div>
          </MotionDiv>
        </MotionDiv>
      )}
    </AnimatePresence>,
    document.body
  );
};

export default PointsExplainer;
