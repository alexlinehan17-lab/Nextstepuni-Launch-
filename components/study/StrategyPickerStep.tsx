/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from '../Motion';
import { STRATEGY_REGISTRY } from '../../utils/strategyRegistry';
import { getSubjectColor } from '../../utils/subjectColors';

// ── Strategy categories ─────────────────────────────────────

const CATEGORIES: { label: string; ids: string[] }[] = [
  {
    label: 'Recall and retention',
    ids: [
      'mastering-active-recall-protocol',
      'mastering-spaced-repetition-protocol',
      'mastering-interleaving-protocol',
      'elaborative-interrogation-protocol',
    ],
  },
  {
    label: 'Mindset and focus',
    ids: [
      'agency-protocol',
      'growth-mindset-protocol',
      'digital-distraction-protocol',
      'learning-radar-protocol',
    ],
  },
  {
    label: 'Exam prep',
    ids: ['exam-hall-strategies-protocol'],
  },
];

const strategyMap = Object.fromEntries(STRATEGY_REGISTRY.map(s => [s.moduleId, s]));

// ── Component ───────────────────────────────────────────────

interface StrategyPickerStepProps {
  learnedStrategyIds: string[];
  autoTrackedIds: string[];
  onContinue: (selectedIds: string[]) => void;
  onSkip?: () => void;
  subject?: string;
  durationSeconds?: number;
  pointsEarned?: number;
}

const StrategyPickerStep: React.FC<StrategyPickerStepProps> = ({
  _learnedStrategyIds,
  autoTrackedIds,
  onContinue,
  onSkip,
  subject,
  durationSeconds = 0,
  pointsEarned = 0,
}) => {
  const autoSet = new Set(autoTrackedIds);
  const [selected, setSelected] = useState<Set<string>>(new Set(autoTrackedIds));

  const toggle = (moduleId: string) => {
    if (autoSet.has(moduleId)) return;
    setSelected(prev => {
      const next = new Set(prev);
      if (next.has(moduleId)) next.delete(moduleId);
      else next.add(moduleId);
      return next;
    });
  };

  const count = selected.size;
  const durationMin = Math.round(durationSeconds / 60);
  const subjectColors = subject ? getSubjectColor(subject) : null;

  return (
    <div className="min-h-screen bg-zinc-50 dark:bg-zinc-950 flex flex-col items-center justify-center px-4 py-10">
      <MotionDiv
        initial={{ scale: 0.95, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
        className="w-full"
        style={{ maxWidth: 420 }}
      >
        {/* ── Header ── */}
        <div className="text-center mb-6">
          {/* Subject pill */}
          {subject && subjectColors && (
            <div className="inline-flex items-center gap-2 rounded-full px-3.5 py-1.5 mb-4" style={{ backgroundColor: '#E1F5EE' }}>
              <div className={`w-2 h-2 rounded-full ${subjectColors.dot}`} />
              <span className="text-xs font-medium" style={{ color: '#085041' }}>{subject}</span>
            </div>
          )}
          <h2 className="font-serif text-[22px] font-medium text-zinc-800 dark:text-white">Nice session</h2>
          <p className="text-sm text-zinc-400 dark:text-zinc-500 mt-1">Which strategies did you use?</p>
        </div>

        {/* ── Session stats ── */}
        <div className="flex items-center justify-center gap-8 pb-5 mb-7 border-b border-zinc-200 dark:border-zinc-800">
          <div className="text-center">
            <p className="text-xl font-medium font-apercu text-zinc-800 dark:text-white">{durationMin}m</p>
            <p className="text-xs text-zinc-400 dark:text-zinc-500">duration</p>
          </div>
          <div className="text-center">
            <p className="text-xl font-medium font-apercu text-zinc-800 dark:text-white">{autoTrackedIds.length}</p>
            <p className="text-xs text-zinc-400 dark:text-zinc-500">strategies tracked</p>
          </div>
          <div className="text-center">
            <p className="text-xl font-medium font-apercu text-zinc-800 dark:text-white">+{pointsEarned}</p>
            <p className="text-xs text-zinc-400 dark:text-zinc-500">journey points earned</p>
          </div>
        </div>

        {/* ── Strategy chips by category ── */}
        {CATEGORIES.map(cat => (
          <div key={cat.label} className="mb-5">
            <p className="text-[11px] uppercase font-medium text-zinc-400 dark:text-zinc-500 mb-2.5" style={{ letterSpacing: '0.06em' }}>
              {cat.label}
            </p>
            <div className="flex flex-wrap gap-2">
              {cat.ids.map(id => {
                const strategy = strategyMap[id];
                if (!strategy) return null;
                const isSelected = selected.has(id);
                const isAuto = autoSet.has(id);

                return (
                  <button
                    key={id}
                    onClick={() => toggle(id)}
                    disabled={isAuto}
                    className={`inline-flex items-center gap-2 rounded-xl transition-all duration-200 ${
                      isSelected
                        ? 'border-[1.5px] border-[#2A7D6F]'
                        : 'border-[1.5px] border-zinc-200 dark:border-zinc-700 hover:border-zinc-300 dark:hover:border-zinc-600'
                    } ${isAuto ? 'cursor-default' : 'cursor-pointer'}`}
                    style={{
                      padding: '10px 16px',
                      backgroundColor: isSelected ? '#E1F5EE' : 'transparent',
                      color: isSelected ? '#085041' : undefined,
                    }}
                  >
                    {/* Checkbox */}
                    <div
                      className={`flex items-center justify-center shrink-0 ${
                        isSelected ? '' : 'border-[1.5px] border-zinc-300 dark:border-zinc-600'
                      }`}
                      style={{
                        width: 18,
                        height: 18,
                        borderRadius: 5,
                        backgroundColor: isSelected ? '#2A7D6F' : 'transparent',
                        borderColor: isSelected ? '#2A7D6F' : undefined,
                        border: isSelected ? '1.5px solid #2A7D6F' : undefined,
                      }}
                    >
                      {isSelected && (
                        <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                          <path d="M2.5 6L5 8.5L9.5 3.5" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                        </svg>
                      )}
                    </div>
                    <span className={`text-sm ${isSelected ? '' : 'text-zinc-500 dark:text-zinc-400'}`}>
                      {strategy.strategyName}
                    </span>
                  </button>
                );
              })}
            </div>
          </div>
        ))}

        {/* ── CTA button ── */}
        <button
          onClick={() => onContinue([...selected])}
          disabled={count === 0}
          className={`w-full rounded-xl text-[15px] font-medium transition-all duration-200 active:scale-[0.98] mt-2 ${
            count > 0
              ? 'text-white hover:opacity-90'
              : 'bg-zinc-200 dark:bg-zinc-800 text-zinc-400 dark:text-zinc-600 cursor-not-allowed'
          }`}
          style={{
            padding: 14,
            backgroundColor: count > 0 ? '#2A7D6F' : undefined,
          }}
        >
          {count > 0
            ? `Continue with ${count} ${count === 1 ? 'strategy' : 'strategies'}`
            : 'Select strategies to continue'}
        </button>

        {/* ── Points hint ── */}
        <AnimatePresence>
          {count > 0 && (
            <MotionDiv
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.3 }}
              className="text-center mt-3"
            >
              <p className="text-xs font-medium" style={{ color: '#2A7D6F' }}>+5 bonus journey points for reflecting</p>
            </MotionDiv>
          )}
        </AnimatePresence>

        {/* ── Skip link ── */}
        <div className="text-center mt-3">
          <button
            onClick={() => onSkip ? onSkip() : onContinue([])}
            className="text-[13px] text-zinc-400 dark:text-zinc-500 hover:text-zinc-500 dark:hover:text-zinc-400 transition-colors"
          >
            Skip this step
          </button>
        </div>
      </MotionDiv>
    </div>
  );
};

export default StrategyPickerStep;
