/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo, useRef, useEffect } from 'react';
import { createPortal } from 'react-dom';
import { AnimatePresence } from 'framer-motion';
import { MotionButton, MotionDiv } from './Motion';
import { X, BookOpen, Target, RotateCcw } from 'lucide-react';
import { useModal } from '../hooks/useModal';

// ─── Reflection Quality Scoring ─────────────────────────────────────────────

export interface ReflectionQuality {
  lengthScore: number;
  specificityScore: number;
  growthScore: number;
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

  const confidenceLevels: Record<string, ReflectionQuality> = {
    'lost': { lengthScore: 0.3, specificityScore: 0.3, growthScore: 0.5, tier: 'basic' },
    'shaky': { lengthScore: 0.4, specificityScore: 0.4, growthScore: 0.5, tier: 'basic' },
    'okay': { lengthScore: 0.5, specificityScore: 0.5, growthScore: 0.5, tier: 'thoughtful' },
    'good': { lengthScore: 0.7, specificityScore: 0.7, growthScore: 0.7, tier: 'thoughtful' },
    'confident': { lengthScore: 1, specificityScore: 1, growthScore: 1, tier: 'deep' },
  };
  if (confidenceLevels[trimmed]) return confidenceLevels[trimmed];

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

// ── Points for each mode ──
export const QUICK_DEBRIEF_POINTS = 50;
export const FULL_REFLECTION_POINTS = 150;

// ─── Rotating Prompts ───────────────────────────────────────────────────────

const REFLECTION_PROMPTS = [
  'What was the hardest part of this session?',
  'What would you do differently next time?',
  'What clicked for you today?',
  'What strategy worked well?',
  'What surprised you about this topic?',
  'What connection did you make to something you already knew?',
  'What question do you still have?',
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
  mode: 'quick' | 'full';
  onSubmit: (reflectionText: string, quality: ReflectionQuality) => void;
  onCancel: () => void;
}

const CONFIDENCE_OPTIONS = [
  { value: 'lost', label: 'Lost', desc: "I don't understand this at all", color: '#DC2626' },
  { value: 'shaky', label: 'Shaky', desc: 'I get the basics but would struggle in an exam', color: '#E67E22' },
  { value: 'okay', label: 'Okay', desc: 'I could answer some questions on this', color: '#FDCB6E' },
  { value: 'good', label: 'Good', desc: 'I feel solid — could explain it to someone', color: '#2A7D6F' },
  { value: 'confident', label: 'Confident', desc: 'I could ace an exam question on this right now', color: '#276749' },
] as const;

const SESSION_TYPE_LABELS: Record<string, { label: string; icon: React.ElementType }> = {
  'new-learning': { label: 'New Learning', icon: BookOpen },
  'practice': { label: 'Practice', icon: Target },
  'revision': { label: 'Revision', icon: RotateCcw },
};

const ReflectionModal: React.FC<ReflectionModalProps> = ({
  isOpen, subjectName, sessionType, mode, onSubmit, onCancel,
}) => {
  useModal(isOpen, onCancel);
  const [confidence, setConfidence] = useState('');
  const [freeText, setFreeText] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const submitTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const prompt = useMemo(() => getRotatingPrompt(), []);

  const bonusPts = mode === 'quick' ? QUICK_DEBRIEF_POINTS : FULL_REFLECTION_POINTS;
  const isQuick = mode === 'quick';

  // Quick mode: valid when confidence is selected
  // Full mode: valid when confidence is selected AND freeText has 15+ chars
  const isValid = isQuick
    ? CONFIDENCE_OPTIONS.some(o => o.value === confidence)
    : CONFIDENCE_OPTIONS.some(o => o.value === confidence) && freeText.trim().length >= 15;

  useEffect(() => {
    return () => { if (submitTimerRef.current) clearTimeout(submitTimerRef.current); };
  }, []);

  // Reset state when modal opens
  useEffect(() => {
    if (isOpen) {
      setConfidence('');
      setFreeText('');
      setSubmitted(false);
    }
  }, [isOpen]);

  const handleSubmit = () => {
    if (!isValid) return;
    const text = isQuick ? confidence : `${confidence}|${freeText.trim()}`;
    const quality = scoreReflection(isQuick ? confidence : freeText);
    setSubmitted(true);

    submitTimerRef.current = setTimeout(() => {
      onSubmit(text, quality);
      setConfidence('');
      setFreeText('');
      setSubmitted(false);
    }, 800);
  };

  const typeConfig = SESSION_TYPE_LABELS[sessionType] || SESSION_TYPE_LABELS['new-learning'];
  const TypeIcon = typeConfig.icon;

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
            className="relative bg-white dark:bg-zinc-900 border border-zinc-200/50 dark:border-white/[0.08] rounded-2xl w-full max-w-md shadow-[0_24px_64px_rgba(0,0,0,0.12)] dark:shadow-[0_24px_64px_rgba(0,0,0,0.5)] overflow-hidden max-h-[90vh] overflow-y-auto"
            onClick={(e: React.MouseEvent) => e.stopPropagation()}
          >
            {/* Header */}
            <div className="flex items-center justify-between p-6 pb-0">
              <div>
                <h2 className="font-sans text-xl font-semibold text-zinc-900 dark:text-white tracking-tight">
                  {isQuick ? 'Quick Debrief' : 'Write a Reflection'}
                </h2>
                <p className="text-xs text-zinc-400 dark:text-zinc-500 mt-0.5">
                  +{bonusPts} bonus pts
                </p>
              </div>
              <button
                onClick={onCancel}
                aria-label="Close"
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

              {/* Confidence level selector */}
              <div>
                <p className="text-xs font-semibold uppercase tracking-widest mb-3 text-[#A8A29E] dark:text-zinc-500">
                  How confident do you feel now?
                </p>
                <div className="flex flex-col gap-2">
                  {CONFIDENCE_OPTIONS.map(option => {
                    const isSelected = confidence === option.value;
                    return (
                      <button
                        key={option.value}
                        onClick={() => setConfidence(option.value)}
                        className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-left transition-all ${isSelected ? '' : 'bg-[#FEFDFB] dark:bg-zinc-800 border border-[#EDEBE8] dark:border-zinc-700'}`}
                        style={isSelected ? {
                          backgroundColor: `${option.color}12`,
                          border: `2px solid ${option.color}`,
                        } : undefined}
                      >
                        <div className="w-3 h-3 rounded-full shrink-0" style={{ backgroundColor: option.color }} />
                        <div className="flex-1 min-w-0">
                          <p className={`text-sm font-semibold ${isSelected ? '' : 'text-[#1C1917] dark:text-white'}`} style={isSelected ? { color: option.color } : undefined}>{option.label}</p>
                          <p className={`text-[11px] ${isSelected ? '' : 'text-[#A8A29E] dark:text-zinc-500'}`} style={isSelected ? { color: option.color } : undefined}>{option.desc}</p>
                        </div>
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Free-text reflection (full mode only) */}
              {!isQuick && (
                <div>
                  <p className="text-xs font-semibold uppercase tracking-widest mb-2 text-[#A8A29E] dark:text-zinc-500">
                    {prompt}
                  </p>
                  <textarea
                    value={freeText}
                    onChange={(e) => setFreeText(e.target.value)}
                    placeholder="What worked, what didn't, what you'd change next time..."
                    className="w-full bg-zinc-50 dark:bg-zinc-800/50 border border-zinc-200 dark:border-zinc-700 rounded-xl p-3.5 text-sm text-zinc-800 dark:text-white placeholder:text-zinc-400 resize-none h-28 focus:outline-none focus:border-[rgba(42,125,111,0.5)] transition-colors"
                  />
                  <p className="text-[10px] text-zinc-400 text-right mt-1">
                    {freeText.trim().length < 15 ? `${15 - freeText.trim().length} more chars needed` : `${freeText.trim().length} chars`}
                  </p>
                </div>
              )}

              {/* Submit */}
              <MotionButton
                onClick={handleSubmit}
                disabled={!isValid || submitted}
                whileHover={isValid && !submitted ? { scale: 1.02 } : {}}
                whileTap={isValid && !submitted ? { scale: 0.98 } : {}}
                className={`w-full py-3 rounded-xl text-sm font-bold transition-all ${
                  isValid && !submitted
                    ? 'text-white'
                    : 'bg-zinc-100 dark:bg-white/[0.06] text-zinc-400 dark:text-white/20 cursor-not-allowed'
                }`}
                style={isValid && !submitted ? { backgroundColor: '#2A7D6F' } : undefined}
              >
                {submitted ? 'Saving...' : `Complete & Earn +${bonusPts} pts`}
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
