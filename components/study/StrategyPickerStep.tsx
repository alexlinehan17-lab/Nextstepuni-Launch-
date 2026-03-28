/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Check, Circle, Lock, Brain, Repeat, Shuffle, HelpCircle, Compass, Sprout, Shield, Radar, ClipboardCheck } from 'lucide-react';
import { STRATEGY_REGISTRY } from '../../studySessionData';

const MotionDiv = motion.div as any;

const STRATEGY_ICONS: Record<string, React.ElementType> = {
  'mastering-active-recall-protocol': Brain,
  'mastering-spaced-repetition-protocol': Repeat,
  'mastering-interleaving-protocol': Shuffle,
  'elaborative-interrogation-protocol': HelpCircle,
  'agency-protocol': Compass,
  'growth-mindset-protocol': Sprout,
  'digital-distraction-protocol': Shield,
  'learning-radar-protocol': Radar,
  'exam-hall-strategies-protocol': ClipboardCheck,
};

interface StrategyPickerStepProps {
  learnedStrategyIds: string[];
  autoTrackedIds: string[];
  onContinue: (selectedIds: string[]) => void;
}

const StrategyPickerStep: React.FC<StrategyPickerStepProps> = ({
  learnedStrategyIds,
  autoTrackedIds,
  onContinue,
}) => {
  const autoSet = new Set(autoTrackedIds);
  const learnedSet = new Set(learnedStrategyIds);
  const [selected, setSelected] = useState<Set<string>>(new Set(autoTrackedIds));

  // Show ALL strategies — learned ones first, then unlearned
  const strategies = [
    ...STRATEGY_REGISTRY.filter(s => learnedSet.has(s.moduleId)),
    ...STRATEGY_REGISTRY.filter(s => !learnedSet.has(s.moduleId)),
  ];

  const toggle = (moduleId: string) => {
    if (autoSet.has(moduleId)) return;
    setSelected(prev => {
      const next = new Set(prev);
      if (next.has(moduleId)) {
        next.delete(moduleId);
      } else {
        next.add(moduleId);
      }
      return next;
    });
  };

  return (
    <div className="min-h-screen bg-zinc-50 dark:bg-zinc-950 flex flex-col items-center justify-center px-4">
      <MotionDiv
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
        className="w-full max-w-sm space-y-6"
      >
        {/* Header */}
        <div className="text-center">
          <h2 className="text-2xl font-bold text-zinc-800 dark:text-white">Which strategies did you use?</h2>
          <p className="text-sm text-zinc-400 dark:text-zinc-500 mt-2">
            Select all that apply. Auto-tracked strategies are locked in.
          </p>
        </div>

        {/* Strategy list */}
        <div className="space-y-2">
          {strategies.map(strategy => {
            const Icon = STRATEGY_ICONS[strategy.moduleId] || Brain;
            const isAuto = autoSet.has(strategy.moduleId);
            const isSelected = selected.has(strategy.moduleId);
            const isLearned = learnedSet.has(strategy.moduleId);

            return (
              <button
                key={strategy.moduleId}
                onClick={() => toggle(strategy.moduleId)}
                disabled={isAuto}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-left transition-all ${
                  isSelected
                    ? 'bg-[rgba(var(--accent),0.08)] ring-1 ring-inset ring-[rgba(var(--accent),0.2)]'
                    : 'bg-white dark:bg-zinc-900 hover:bg-zinc-100 dark:hover:bg-zinc-800/60'
                } ${isAuto ? 'cursor-default' : ''}`}
              >
                <Icon size={16} className={isSelected ? 'text-[var(--accent-hex)]' : 'text-zinc-400'} />
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <span className={`text-[13px] font-medium ${isSelected ? 'text-zinc-800 dark:text-white' : 'text-zinc-500 dark:text-zinc-400'}`}>
                      {strategy.strategyName}
                    </span>
                    {isLearned && (
                      <span className="text-[9px] font-semibold px-1.5 py-0.5 rounded-full bg-emerald-50 dark:bg-emerald-900/20 text-emerald-500">
                        Learned
                      </span>
                    )}
                  </div>
                  <span className="text-[11px] text-zinc-400 dark:text-zinc-500 block truncate">
                    {strategy.description}
                  </span>
                </div>
                {isAuto ? (
                  <Lock size={14} className="text-teal-500 shrink-0" />
                ) : isSelected ? (
                  <Check size={16} className="text-[var(--accent-hex)] shrink-0" />
                ) : (
                  <Circle size={16} className="text-zinc-300 dark:text-zinc-600 shrink-0" />
                )}
              </button>
            );
          })}
        </div>

        {/* Continue button */}
        <button
          onClick={() => onContinue([...selected])}
          className="w-full py-3.5 rounded-xl text-sm font-bold bg-[var(--accent-hex)] text-white shadow-lg shadow-[rgba(var(--accent),0.25)] hover:shadow-[rgba(var(--accent),0.4)] active:scale-[0.98] transition-all"
        >
          Continue
        </button>
      </MotionDiv>
    </div>
  );
};

export default StrategyPickerStep;
