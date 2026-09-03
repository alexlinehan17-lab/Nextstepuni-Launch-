/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from '../Motion';
import { STRATEGY_REGISTRY } from '../../utils/strategyRegistry';
import { getSubjectColor } from '../../utils/subjectColors';
import ChoiceControl from '../ui/ChoiceControl';
import PrimaryActionButton from '../ui/PrimaryActionButton';
import { ResultStatGrid } from '../ui/ProductPatterns';

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
  learnedStrategyIds: _learnedStrategyIds,
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
    <div className="min-h-screen bg-white dark:bg-zinc-950 flex flex-col items-center justify-center px-4 py-10">
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
            <div className="inline-flex items-center gap-2 rounded-xl px-3.5 py-2 mb-4 bg-white border border-[#D0CDC8]">
              <div className={`w-2 h-2 rounded-full ${subjectColors.dot}`} />
              <span className="text-xs font-semibold text-[#3A3530]">{subject}</span>
            </div>
          )}
          <p className="text-[10px] font-bold uppercase tracking-[0.14em] text-[#9E9186] mb-1.5">Before your results</p>
          <h2 className="font-serif text-[28px] font-bold text-[#1A1A1A] dark:text-white">What helped you focus?</h2>
          <p className="text-sm text-[#7A7068] mt-1">Select the strategies you used.</p>
        </div>

        {/* ── Session stats ── */}
        <ResultStatGrid className="mb-7" items={[
          { label: 'Duration', value: `${durationMin}m` },
          { label: 'Tracked', value: autoTrackedIds.length },
          { label: 'JP earned', value: `+${pointsEarned}`, tone: 'accent' },
        ]} />

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
                  <ChoiceControl
                    key={id}
                    onClick={() => toggle(id)}
                    disabled={isAuto}
                    label={strategy.strategyName}
                    selected={isSelected}
                    compact
                    trailing={isAuto ? <span className="text-[9px] font-bold uppercase tracking-wider opacity-70">Tracked</span> : undefined}
                  />
                );
              })}
            </div>
          </div>
        ))}

        {/* ── CTA button ── */}
        <PrimaryActionButton
          onClick={() => onContinue([...selected])}
          disabled={count === 0}
          className="w-full mt-2"
          label={count > 0
            ? `Continue with ${count} ${count === 1 ? 'strategy' : 'strategies'}`
            : 'Select strategies to continue'}
        />

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
              <p className="text-xs font-medium" style={{ color: '#F26B1F' }}>+5 bonus JP for reflecting</p>
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
