/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { createPortal } from 'react-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { TrendingUp, Target, Zap, Award, Crown, Mountain, Footprints } from 'lucide-react';
import { type AthleteRank } from '../gamificationConfig';

const MotionDiv = motion.div as any;
const MotionButton = motion.button as any;

const RANK_ICONS: Record<string, React.ElementType> = {
  Footprints,
  TrendingUp,
  Target,
  Zap,
  Award,
  Crown,
  Mountain,
};

const RANK_DESCRIPTIONS: Record<string, string> = {
  newcomer: 'Welcome to your study journey.',
  beginner: 'You\'re building momentum. Keep it up.',
  consistent: 'Consistency is your superpower.',
  dedicated: 'Your dedication is paying off.',
  driven: 'Nothing can stop you now.',
  elite: 'You\'re in the top tier.',
  master: 'True mastery takes commitment. You\'ve earned it.',
  legend: 'Legendary status achieved. Inspiring.',
};

interface RankUpModalProps {
  isOpen: boolean;
  newRank: AthleteRank | null;
  onClose: () => void;
}

const RankUpModal: React.FC<RankUpModalProps> = ({ isOpen, newRank, onClose }) => {
  if (!newRank) return null;

  const RankIcon = RANK_ICONS[newRank.icon] || Footprints;

  return createPortal(
    <AnimatePresence>
      {isOpen && (
        <MotionDiv
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.3 }}
          className="fixed inset-0 z-[250] bg-zinc-950/80 flex items-center justify-center p-4"
          onClick={onClose}
        >
          <MotionDiv
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.8, opacity: 0 }}
            transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
            className="relative w-full max-w-sm text-center"
            onClick={(e: React.MouseEvent) => e.stopPropagation()}
          >
            {/* Rank icon — large, centered */}
            <MotionDiv
              initial={{ scale: 0, rotate: -180 }}
              animate={{ scale: 1, rotate: 0 }}
              transition={{ duration: 0.8, delay: 0.2, ease: [0.16, 1, 0.3, 1] }}
              className="mx-auto mb-6 w-24 h-24 rounded-full flex items-center justify-center"
              style={{ backgroundColor: `${newRank.colorHex}20`, boxShadow: `0 0 60px ${newRank.colorHex}30` }}
            >
              <RankIcon size={48} style={{ color: newRank.colorHex }} />
            </MotionDiv>

            {/* Eyebrow */}
            <MotionDiv
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
            >
              <p className="font-mono text-[10px] font-bold uppercase tracking-[0.3em] text-white/50 mb-2">
                Rank Up
              </p>
            </MotionDiv>

            {/* Rank title */}
            <MotionDiv
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
            >
              <h2
                className="font-serif text-4xl sm:text-5xl font-semibold mb-4"
                style={{ color: newRank.colorHex }}
              >
                {newRank.title}
              </h2>
            </MotionDiv>

            {/* Description */}
            <MotionDiv
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6 }}
            >
              <p className="text-white/60 text-base leading-relaxed mb-8 max-w-xs mx-auto">
                {RANK_DESCRIPTIONS[newRank.id] || 'Keep pushing forward.'}
              </p>
            </MotionDiv>

            {/* CTA */}
            <MotionDiv
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.7 }}
            >
              <MotionButton
                onClick={onClose}
                whileHover={{ scale: 1.03 }}
                whileTap={{ scale: 0.97 }}
                className="px-8 py-3 rounded-full text-sm font-bold text-white transition-colors"
                style={{ backgroundColor: newRank.colorHex }}
              >
                Let's go
              </MotionButton>
            </MotionDiv>
          </MotionDiv>
        </MotionDiv>
      )}
    </AnimatePresence>,
    document.body
  );
};

export default RankUpModal;
