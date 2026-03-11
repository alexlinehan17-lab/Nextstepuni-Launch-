/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Brain, CheckCircle, ArrowRight, TrendingUp, BookOpen, Target, RotateCcw,
  Lightbulb, Sparkles, BarChart3,
} from 'lucide-react';

const MotionDiv = motion.div as any;

// ─── Types ───────────────────────────────────────────────────────────────────

export interface DebriefEntry {
  id: string;
  date: string;
  subject: string;
  sessionType: 'new-learning' | 'practice' | 'revision';
  durationMinutes: number;
  hardestTopic: string;
  strategy: string;
  confidenceBefore: number;   // 1-5
  confidenceAfter: number;    // 1-5
  whatWorked: string;         // short free text
}

// ─── Constants ───────────────────────────────────────────────────────────────

export const STRATEGY_OPTIONS = [
  { id: 'past-papers', label: 'Past papers / practice questions', icon: Target },
  { id: 'active-recall', label: 'Active recall / self-testing', icon: Brain },
  { id: 're-reading', label: 'Re-reading notes', icon: BookOpen },
  { id: 'summarising', label: 'Summarising / mind maps', icon: Lightbulb },
  { id: 'teaching', label: 'Teaching / explaining it', icon: Sparkles },
  { id: 'videos', label: 'Videos / online resources', icon: BarChart3 },
  { id: 'flashcards', label: 'Flashcards', icon: RotateCcw },
  { id: 'other', label: 'Other', icon: CheckCircle },
];

const CONFIDENCE_LABELS = ['Very Low', 'Low', 'Medium', 'High', 'Very High'];

// ─── StudyDebrief Modal ──────────────────────────────────────────────────────

interface StudyDebriefProps {
  isOpen: boolean;
  subject: string;
  sessionType: 'new-learning' | 'practice' | 'revision';
  durationMinutes: number;
  onSubmit: (entry: Omit<DebriefEntry, 'id' | 'date'>) => void;
  onSkip: () => void;
}

const StudyDebrief: React.FC<StudyDebriefProps> = ({
  isOpen, subject, sessionType, durationMinutes, onSubmit, onSkip,
}) => {
  const [step, setStep] = useState(0);
  const [hardestTopic, setHardestTopic] = useState('');
  const [strategy, setStrategy] = useState('');
  const [confidenceBefore, setConfidenceBefore] = useState(3);
  const [confidenceAfter, setConfidenceAfter] = useState(3);
  const [whatWorked, setWhatWorked] = useState('');

  const handleSubmit = () => {
    onSubmit({
      subject,
      sessionType,
      durationMinutes,
      hardestTopic: hardestTopic.trim() || 'Not specified',
      strategy: strategy || 'other',
      confidenceBefore,
      confidenceAfter,
      whatWorked: whatWorked.trim(),
    });
    // Reset for next use
    setStep(0);
    setHardestTopic('');
    setStrategy('');
    setConfidenceBefore(3);
    setConfidenceAfter(3);
    setWhatWorked('');
  };

  if (!isOpen) return null;

  const steps = [
    // Step 0: What was hardest?
    <MotionDiv key="step-0" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} className="space-y-4">
      <div>
        <p className="text-sm font-bold text-zinc-800 dark:text-zinc-200">What felt hardest today?</p>
        <p className="text-xs text-zinc-400 dark:text-zinc-500 mt-1">Name a specific topic, concept, or question type.</p>
      </div>
      <input
        type="text"
        value={hardestTopic}
        onChange={(e) => setHardestTopic(e.target.value)}
        placeholder={`e.g. "Organic chemistry reactions" or "Integration by parts"`}
        className="w-full px-4 py-3 rounded-xl bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-sm text-zinc-800 dark:text-zinc-200 placeholder:text-zinc-400 outline-none focus:ring-2 focus:ring-teal-500/30"
        autoFocus
      />
    </MotionDiv>,

    // Step 1: What strategy did you use?
    <MotionDiv key="step-1" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} className="space-y-4">
      <div>
        <p className="text-sm font-bold text-zinc-800 dark:text-zinc-200">What strategy did you mainly use?</p>
        <p className="text-xs text-zinc-400 dark:text-zinc-500 mt-1">Pick the one that best describes your session.</p>
      </div>
      <div className="grid grid-cols-2 gap-2">
        {STRATEGY_OPTIONS.map(opt => {
          const Icon = opt.icon;
          return (
            <button
              key={opt.id}
              onClick={() => setStrategy(opt.id)}
              className={`flex items-center gap-2 px-3 py-2.5 rounded-xl text-xs font-medium transition-all text-left ${
                strategy === opt.id
                  ? 'bg-teal-500 text-white shadow-sm'
                  : 'bg-zinc-50 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-700'
              }`}
            >
              <Icon size={14} />
              {opt.label}
            </button>
          );
        })}
      </div>
    </MotionDiv>,

    // Step 2: Confidence before & after
    <MotionDiv key="step-2" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} className="space-y-5">
      <div>
        <p className="text-sm font-bold text-zinc-800 dark:text-zinc-200">Confidence check</p>
        <p className="text-xs text-zinc-400 dark:text-zinc-500 mt-1">How confident did you feel before vs after this session?</p>
      </div>

      <div className="space-y-4">
        <div>
          <p className="text-[11px] font-semibold text-zinc-500 dark:text-zinc-400 mb-2">Before the session</p>
          <div className="flex gap-2">
            {[1, 2, 3, 4, 5].map(n => (
              <button
                key={n}
                onClick={() => setConfidenceBefore(n)}
                className={`flex-1 py-2.5 rounded-lg text-xs font-bold transition-all ${
                  confidenceBefore === n
                    ? 'bg-zinc-700 dark:bg-zinc-300 text-white dark:text-zinc-900'
                    : 'bg-zinc-100 dark:bg-zinc-800 text-zinc-500 dark:text-zinc-400 hover:bg-zinc-200 dark:hover:bg-zinc-700'
                }`}
              >
                {n}
              </button>
            ))}
          </div>
          <div className="flex justify-between mt-1">
            <span className="text-[9px] text-zinc-400">Very Low</span>
            <span className="text-[9px] text-zinc-400">Very High</span>
          </div>
        </div>

        <div>
          <p className="text-[11px] font-semibold text-zinc-500 dark:text-zinc-400 mb-2">After the session</p>
          <div className="flex gap-2">
            {[1, 2, 3, 4, 5].map(n => (
              <button
                key={n}
                onClick={() => setConfidenceAfter(n)}
                className={`flex-1 py-2.5 rounded-lg text-xs font-bold transition-all ${
                  confidenceAfter === n
                    ? 'bg-teal-500 text-white'
                    : 'bg-zinc-100 dark:bg-zinc-800 text-zinc-500 dark:text-zinc-400 hover:bg-zinc-200 dark:hover:bg-zinc-700'
                }`}
              >
                {n}
              </button>
            ))}
          </div>
          <div className="flex justify-between mt-1">
            <span className="text-[9px] text-zinc-400">Very Low</span>
            <span className="text-[9px] text-zinc-400">Very High</span>
          </div>
        </div>

        {confidenceAfter > confidenceBefore && (
          <p className="text-xs text-emerald-600 dark:text-emerald-400 font-medium">
            +{confidenceAfter - confidenceBefore} confidence — that session worked.
          </p>
        )}
        {confidenceAfter < confidenceBefore && (
          <p className="text-xs text-amber-600 dark:text-amber-400 font-medium">
            Confidence dropped — that's okay. It means you found what you don't know yet. That's progress.
          </p>
        )}
      </div>
    </MotionDiv>,

    // Step 3: What worked? (optional short note)
    <MotionDiv key="step-3" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} className="space-y-4">
      <div>
        <p className="text-sm font-bold text-zinc-800 dark:text-zinc-200">Anything you want to remember?</p>
        <p className="text-xs text-zinc-400 dark:text-zinc-500 mt-1">Optional. A quick note about what clicked or what to revisit.</p>
      </div>
      <textarea
        value={whatWorked}
        onChange={(e) => setWhatWorked(e.target.value)}
        placeholder="e.g. 'The worked examples in ch. 5 really helped' or 'Need to revisit trigonometric identities'"
        rows={3}
        className="w-full px-4 py-3 rounded-xl bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-sm text-zinc-800 dark:text-zinc-200 placeholder:text-zinc-400 outline-none focus:ring-2 focus:ring-teal-500/30 resize-none"
      />
    </MotionDiv>,
  ];

  const isLastStep = step === steps.length - 1;

  return (
    <div className="fixed inset-0 z-[200] flex items-center justify-center bg-black/50 backdrop-blur-sm px-4">
      <MotionDiv
        initial={{ scale: 0.95, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        className="bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-2xl shadow-2xl w-full max-w-md overflow-hidden"
      >
        {/* Header */}
        <div className="px-5 pt-5 pb-3">
          <div className="flex items-center gap-2 mb-3">
            <Brain size={18} className="text-teal-500" />
            <span className="text-sm font-bold text-zinc-800 dark:text-zinc-200">Quick Debrief</span>
            <span className="text-[10px] text-zinc-400 dark:text-zinc-500 ml-auto">{step + 1} / {steps.length}</span>
          </div>
          {/* Step progress */}
          <div className="flex gap-1">
            {steps.map((_, i) => (
              <div key={i} className={`flex-1 h-1 rounded-full transition-all ${i <= step ? 'bg-teal-500' : 'bg-zinc-200 dark:bg-zinc-700'}`} />
            ))}
          </div>
        </div>

        {/* Content */}
        <div className="px-5 py-4 min-h-[200px]">
          <AnimatePresence mode="wait">
            {steps[step]}
          </AnimatePresence>
        </div>

        {/* Actions */}
        <div className="px-5 pb-5 flex items-center gap-3">
          {step > 0 && (
            <button
              onClick={() => setStep(step - 1)}
              className="px-4 py-2.5 rounded-xl text-sm font-medium text-zinc-500 hover:text-zinc-700 dark:hover:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-800/50 transition-all"
            >
              Back
            </button>
          )}
          <button
            onClick={onSkip}
            className="text-sm text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-300 transition-colors"
          >
            Skip
          </button>
          <div className="flex-1" />
          <button
            onClick={isLastStep ? handleSubmit : () => setStep(step + 1)}
            disabled={step === 1 && !strategy}
            className="px-5 py-2.5 rounded-xl text-sm font-bold text-white bg-teal-500 hover:bg-teal-600 shadow-sm transition-all disabled:opacity-40 disabled:cursor-not-allowed flex items-center gap-1.5"
          >
            {isLastStep ? 'Save Debrief' : 'Next'}
            <ArrowRight size={14} />
          </button>
        </div>
      </MotionDiv>
    </div>
  );
};

export default StudyDebrief;
