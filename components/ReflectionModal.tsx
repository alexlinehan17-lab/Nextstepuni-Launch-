/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo, useRef, useEffect } from 'react';
import { createPortal } from 'react-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Star, BookOpen, Target, RotateCcw, Sparkles } from 'lucide-react';

const MotionDiv = motion.div as any;
const MotionButton = motion.button as any;

// ─── Reflection Quality Scoring ─────────────────────────────────────────────

export interface ReflectionQuality {
  lengthScore: number;       // 0-1
  specificityScore: number;  // 0-1
  growthScore: number;       // 0-1
  tier: 'basic' | 'thoughtful' | 'deep';
}

const SPECIFICITY_KEYWORDS = [
  'equation', 'formula', 'chapter', 'topic', 'concept', 'example', 'question',
  'problem', 'exercise', 'strategy', 'technique', 'method', 'approach',
  'paragraph', 'essay', 'experiment', 'theorem', 'proof', 'diagram',
  'flashcard', 'notes', 'summary', 'practice', 'revision', 'exam',
  'maths', 'english', 'irish', 'biology', 'chemistry', 'physics',
  'geography', 'history', 'business', 'economics', 'accounting',
];

const GROWTH_KEYWORDS = [
  'next time', 'improve', 'realized', 'understood', 'learned', 'discovered',
  'struggled', 'difficult', 'easier', 'better', 'progress', 'goal',
  'differently', 'strategy', 'changed', 'tried', 'worked', 'clicked',
  'breakthrough', 'mistake', 'corrected', 'figured out',
];

export function scoreReflection(text: string): ReflectionQuality {
  const trimmed = text.trim().toLowerCase();

  // Handle confidence level selections (from the 5-option picker)
  const confidenceLevels: Record<string, ReflectionQuality> = {
    'lost': { lengthScore: 0.3, specificityScore: 0.3, growthScore: 0.5, tier: 'basic' },
    'shaky': { lengthScore: 0.4, specificityScore: 0.4, growthScore: 0.5, tier: 'basic' },
    'okay': { lengthScore: 0.5, specificityScore: 0.5, growthScore: 0.5, tier: 'thoughtful' },
    'good': { lengthScore: 0.7, specificityScore: 0.7, growthScore: 0.7, tier: 'thoughtful' },
    'confident': { lengthScore: 1, specificityScore: 1, growthScore: 1, tier: 'deep' },
  };
  if (confidenceLevels[trimmed]) return confidenceLevels[trimmed];

  // Fallback: score free-text reflections (used by other parts of the app)
  const len = trimmed.length;
  const lengthScore = len < 15 ? 0 : len < 50 ? 0.3 + ((len - 15) / 35) * 0.4 : Math.min(1, 0.7 + ((len - 50) / 50) * 0.3);
  const specificMatches = SPECIFICITY_KEYWORDS.filter(kw => trimmed.includes(kw));
  const specificityScore = Math.min(1, specificMatches.length * 0.25);
  const growthMatches = GROWTH_KEYWORDS.filter(kw => trimmed.includes(kw));
  const growthScore = Math.min(1, growthMatches.length * 0.3);
  const total = (lengthScore * 0.3) + (specificityScore * 0.35) + (growthScore * 0.35);
  const tier: ReflectionQuality['tier'] = total >= 0.6 ? 'deep' : total >= 0.35 ? 'thoughtful' : 'basic';
  return { lengthScore, specificityScore, growthScore, tier };
}

export const REFLECTION_TIER_POINTS: Record<ReflectionQuality['tier'], number> = {
  basic: 10,
  thoughtful: 15,
  deep: 20,
};

const TIER_LABELS: Record<ReflectionQuality['tier'], { label: string; color: string }> = {
  basic: { label: '', color: '' },
  thoughtful: { label: 'Thoughtful reflection!', color: 'text-blue-500' },
  deep: { label: 'Deep reflection!', color: 'text-purple-500' },
};

// ─── Rotating Prompts ───────────────────────────────────────────────────────

const REFLECTION_PROMPTS = [
  'What was the hardest part of this session?',
  'What would you do differently next time?',
  'What clicked for you today?',
  'What strategy worked well?',
  'What surprised you about this topic?',
  'What connection did you make to something you already knew?',
  'What question do you still have?',
  'How confident do you feel about this material now?',
];

function getRotatingPrompt(): string {
  const dayOfYear = Math.floor((Date.now() - new Date(new Date().getFullYear(), 0, 0).getTime()) / 86400000);
  return REFLECTION_PROMPTS[dayOfYear % REFLECTION_PROMPTS.length];
}

// ─── Component ──────────────────────────────────────────────────────────────

interface ReflectionModalProps {
  isOpen: boolean;
  subjectName: string;
  sessionType: 'new-learning' | 'practice' | 'revision';
  basePoints: number;
  streakMultiplier: number;
  onSubmit: (reflectionText: string, quality: ReflectionQuality) => void;
  onCancel: () => void;
}

const SESSION_TYPE_LABELS: Record<string, { label: string; icon: React.ElementType }> = {
  'new-learning': { label: 'New Learning', icon: BookOpen },
  'practice': { label: 'Practice', icon: Target },
  'revision': { label: 'Revision', icon: RotateCcw },
};

const MIN_CHARS = 15;

const ReflectionModal: React.FC<ReflectionModalProps> = ({
  isOpen, subjectName, sessionType, basePoints, streakMultiplier, onSubmit, onCancel,
}) => {
  const [text, setText] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [submittedQuality, setSubmittedQuality] = useState<ReflectionQuality | null>(null);
  const submitTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    return () => {
      if (submitTimerRef.current) clearTimeout(submitTimerRef.current);
    };
  }, []);

  const totalPoints = Math.round(basePoints * streakMultiplier);
  const typeConfig = SESSION_TYPE_LABELS[sessionType] || SESSION_TYPE_LABELS['new-learning'];
  const TypeIcon = typeConfig.icon;
  const isValid = ['lost', 'shaky', 'okay', 'good', 'confident'].includes(text);
  const prompt = useMemo(() => getRotatingPrompt(), []);

  const handleSubmit = () => {
    if (!isValid) return;
    const quality = scoreReflection(text);
    setSubmittedQuality(quality);
    setSubmitted(true);

    // Brief pause to show quality tier feedback, then submit
    submitTimerRef.current = setTimeout(() => {
      onSubmit(text.trim(), quality);
      setText('');
      setSubmitted(false);
      setSubmittedQuality(null);
    }, 1500);
  };

  return createPortal(
    <AnimatePresence>
      {isOpen && (
        <MotionDiv
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black/60 flex items-center justify-center z-[200] p-4"
          onClick={onCancel}
        >
          <MotionDiv
            initial={{ scale: 0.96, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.96, opacity: 0 }}
            transition={{ duration: 0.2, ease: [0.16, 1, 0.3, 1] }}
            className="relative bg-white dark:bg-zinc-900 border border-zinc-200/50 dark:border-white/[0.08] rounded-2xl w-full max-w-md shadow-[0_24px_64px_rgba(0,0,0,0.12)] dark:shadow-[0_24px_64px_rgba(0,0,0,0.5)] overflow-hidden"
            onClick={(e: React.MouseEvent) => e.stopPropagation()}
          >
            {/* Quality tier feedback overlay */}
            <AnimatePresence>
              {submitted && submittedQuality && submittedQuality.tier !== 'basic' && (
                <MotionDiv
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.9 }}
                  className="absolute inset-0 z-10 bg-white/95 dark:bg-zinc-900/95 flex flex-col items-center justify-center"
                >
                  <Sparkles size={32} className={TIER_LABELS[submittedQuality.tier].color} />
                  <p className={`text-lg font-bold mt-3 ${TIER_LABELS[submittedQuality.tier].color}`}>
                    {TIER_LABELS[submittedQuality.tier].label}
                  </p>
                </MotionDiv>
              )}
            </AnimatePresence>

            {/* Header */}
            <div className="flex items-center justify-between p-6 pb-0">
              <h2 className="font-sans text-xl font-semibold text-zinc-900 dark:text-white tracking-tight">
                Quick Reflection
              </h2>
              <button
                onClick={onCancel}
                className="text-zinc-400 dark:text-white/25 hover:text-zinc-600 dark:hover:text-white/50 transition-colors"
              >
                <X size={18} />
              </button>
            </div>

            <div className="p-6 space-y-5">
              {/* Subject + Session info */}
              <div className="flex items-center gap-3 p-3 rounded-xl bg-zinc-50 dark:bg-white/[0.04] border border-zinc-200/50 dark:border-white/[0.08]">
                <div className="w-10 h-10 rounded-lg bg-purple-100 dark:bg-purple-900/40 flex items-center justify-center flex-shrink-0">
                  <TypeIcon size={20} className="text-purple-600 dark:text-purple-400" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-bold text-zinc-800 dark:text-zinc-200 truncate">{subjectName}</p>
                  <p className="text-[10px] text-zinc-400 dark:text-zinc-500 font-medium">{typeConfig.label} session</p>
                </div>
              </div>

              {/* Points preview */}
              <div className="flex items-center justify-center gap-3 p-3 rounded-xl bg-amber-50 dark:bg-amber-900/15 border border-amber-200 dark:border-amber-700/30">
                <Star size={16} className="text-amber-500" />
                <span className="text-sm font-bold text-amber-700 dark:text-amber-300">
                  +{totalPoints} pts
                </span>
                {streakMultiplier > 1 && (
                  <span className="text-[10px] text-amber-500 dark:text-amber-400 font-semibold">
                    ({basePoints} x {streakMultiplier} streak)
                  </span>
                )}
              </div>

              {/* Confidence level selector */}
              <div>
                <p className="text-xs font-semibold uppercase tracking-widest mb-3" style={{ color: '#A8A29E' }}>
                  How confident do you feel about this material now?
                </p>
                <div className="flex flex-col gap-2">
                  {([
                    { value: 'lost', label: 'Lost', desc: 'I don\'t understand this at all', color: '#DC2626' },
                    { value: 'shaky', label: 'Shaky', desc: 'I get the basics but would struggle in an exam', color: '#E67E22' },
                    { value: 'okay', label: 'Okay', desc: 'I could answer some questions on this', color: '#FDCB6E' },
                    { value: 'good', label: 'Good', desc: 'I feel solid — could explain it to someone', color: '#2A7D6F' },
                    { value: 'confident', label: 'Confident', desc: 'I could ace an exam question on this right now', color: '#276749' },
                  ] as const).map(option => {
                    const isSelected = text === option.value;
                    return (
                      <button
                        key={option.value}
                        onClick={() => setText(option.value)}
                        className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-left transition-all"
                        style={{
                          backgroundColor: isSelected ? `${option.color}12` : '#FEFDFB',
                          border: isSelected ? `2px solid ${option.color}` : '1px solid #EDEBE8',
                        }}
                      >
                        <div className="w-3 h-3 rounded-full shrink-0" style={{ backgroundColor: option.color }} />
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-semibold" style={{ color: isSelected ? option.color : '#1C1917' }}>{option.label}</p>
                          <p className="text-[11px]" style={{ color: isSelected ? option.color : '#A8A29E' }}>{option.desc}</p>
                        </div>
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Submit */}
              <MotionButton
                onClick={handleSubmit}
                disabled={!isValid || submitted}
                whileHover={isValid && !submitted ? { scale: 1.02 } : {}}
                whileTap={isValid && !submitted ? { scale: 0.98 } : {}}
                className={`w-full py-3 rounded-xl text-sm font-bold transition-all ${
                  isValid && !submitted
                    ? 'bg-purple-600 text-white hover:bg-purple-700 shadow-lg shadow-purple-500/20'
                    : 'bg-zinc-100 dark:bg-white/[0.06] text-zinc-400 dark:text-white/20 cursor-not-allowed'
                }`}
              >
                {submitted ? 'Submitting...' : `Complete & Earn ${totalPoints} pts`}
              </MotionButton>
            </div>
          </MotionDiv>
        </MotionDiv>
      )}
    </AnimatePresence>,
    document.body
  );
};

export default ReflectionModal;
