/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { createPortal } from 'react-dom';
import { AnimatePresence } from 'framer-motion';
import { MotionButton, MotionDiv } from './Motion';

interface StreakCelebrationProps {
  streakCount: number;
  isOpen: boolean;
  onDismiss: () => void;
  weekDays: boolean[]; // 7 booleans for M-S, true = studied that day
}

const MILESTONE_MESSAGES: Record<number, string> = {
  3: "Three days in. You're building something.",
  7: "A full week. That's not luck \u2014 that's discipline.",
  14: "Two weeks strong. Most people quit by now.",
  21: "Three weeks. They say it takes 21 days to build a habit.",
  30: "A month. You're not the same student you were 30 days ago.",
  50: "Fifty days. This is who you are now.",
  100: "One hundred days. Extraordinary.",
};

const getMessage = (count: number): string => {
  return MILESTONE_MESSAGES[count] || `${count} days. Keep the momentum going.`;
};

const PARTICLE_COLORS = ['#2A7D6F', '#4CC9F0', '#6B8F71', '#F59E0B', '#E94560'];

const DAY_LABELS = ['M', 'T', 'W', 'T', 'F', 'S', 'S'];

const StreakCelebration: React.FC<StreakCelebrationProps> = ({ streakCount, isOpen, onDismiss, weekDays }) => {
  // Generate 24 particles that fly outward
  const particles = Array.from({ length: 24 }, (_, i) => {
    const angle = (i / 24) * Math.PI * 2;
    const distance = 150 + Math.random() * 100;
    const x = Math.cos(angle) * distance;
    const y = Math.sin(angle) * distance;
    const size = 4 + Math.random() * 8;
    const color = PARTICLE_COLORS[Math.floor(Math.random() * PARTICLE_COLORS.length)];
    const delay = Math.random() * 0.3;

    return (
      <MotionDiv
        key={i}
        className="absolute rounded-full"
        style={{ width: size, height: size, backgroundColor: color, left: '50%', top: '40%' }}
        initial={{ x: 0, y: 0, opacity: 1, scale: 0 }}
        animate={{ x, y, opacity: 0, scale: 1 }}
        transition={{ duration: 0.8, delay, ease: 'easeOut' }}
      />
    );
  });

  return createPortal(
    <AnimatePresence>
      {isOpen && (
        <MotionDiv
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.3 }}
          className="fixed inset-0 z-[300] flex flex-col items-center justify-center"
          onClick={onDismiss}
        >
          {/* Gradient background */}
          <div
            className="absolute inset-0"
            style={{ background: 'linear-gradient(180deg, rgba(42,125,111,0.08) 0%, rgba(42,125,111,0.15) 100%)', backdropFilter: 'blur(24px)', WebkitBackdropFilter: 'blur(24px)' }}
          />

          {/* Particle burst */}
          <div className="absolute inset-0 pointer-events-none overflow-hidden">
            {particles}
          </div>

          {/* Content */}
          <MotionDiv
            className="relative z-10 flex flex-col items-center"
            onClick={(e: React.MouseEvent) => e.stopPropagation()}
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.8, opacity: 0 }}
            transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
          >
            {/* Hero number */}
            <MotionDiv
              initial={{ scale: 0.5, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ duration: 0.6, delay: 0.2, ease: [0.16, 1, 0.3, 1] }}
              style={{ fontSize: 128, fontWeight: 800, color: '#2A7D6F', letterSpacing: '-0.05em', lineHeight: 1 }}
            >
              {streakCount}
            </MotionDiv>

            {/* Label */}
            <MotionDiv
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
            >
              <p style={{ fontSize: 24, fontWeight: 600, color: '#1a1a2e' }} className="dark:!text-white">
                day streak!
              </p>
            </MotionDiv>

            {/* Weekly dot tracker */}
            <MotionDiv
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              className="flex gap-3 mt-8"
            >
              {DAY_LABELS.map((day, i) => (
                <div key={i} className="flex flex-col items-center gap-1">
                  <div
                    className="w-8 h-8 rounded-full transition-colors"
                    style={{
                      backgroundColor: weekDays[i] ? '#2A7D6F' : undefined,
                    }}
                    {...(!weekDays[i] ? { className: 'w-8 h-8 rounded-full bg-zinc-200 dark:bg-zinc-700' } : { className: 'w-8 h-8 rounded-full', style: { backgroundColor: '#2A7D6F' } })}
                  />
                  <span className={`text-xs font-medium ${weekDays[i] ? 'text-[#2A7D6F]' : 'text-[#9A9590] dark:text-zinc-500'}`}>{day}</span>
                </div>
              ))}
            </MotionDiv>

            {/* Milestone message */}
            <MotionDiv
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6 }}
            >
              <p className="text-sm mt-6 max-w-xs text-center" style={{ color: '#6b7280' }}>
                {getMessage(streakCount)}
              </p>
            </MotionDiv>

            {/* Continue button */}
            <MotionDiv
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.7 }}
            >
              <MotionButton
                onClick={onDismiss}
                whileHover={{ scale: 1.03 }}
                whileTap={{ scale: 0.97 }}
                className="mt-8 px-8 py-3 rounded-full bg-zinc-900 dark:bg-white text-white dark:text-zinc-900 font-semibold text-sm"
              >
                Keep going
              </MotionButton>
            </MotionDiv>
          </MotionDiv>
        </MotionDiv>
      )}
    </AnimatePresence>,
    document.body
  );
};

export default StreakCelebration;
