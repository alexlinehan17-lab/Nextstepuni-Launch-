/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * StageProgress — top-of-screen stage indicator + forward/back arrows for the
 * Exam Strategiser player.
 */

import React from 'react';
import { type ExamStrategiserStage } from '../../types/examStrategiser';

const TEAL = '#2A7D6F';

interface StageProgressProps {
  stages: ExamStrategiserStage[];
  current: ExamStrategiserStage;
  onBack: () => void;
  onForward: () => void;
  canGoBack: boolean;
  canGoForward: boolean;
  forwardLabel?: string;
}

const STAGE_LABELS: Record<ExamStrategiserStage, string> = {
  raw: 'Question',
  predict: 'Predict',
  annotation: 'Examiner notes',
  insights: 'Insights',
  'mark-scheme': 'Mark scheme',
};

const StageProgress: React.FC<StageProgressProps> = ({
  stages, current, onBack, onForward, canGoBack, canGoForward, forwardLabel,
}) => {
  const currentIdx = stages.indexOf(current);

  return (
    <div className="flex items-center justify-between gap-4 mb-6">
      <button
        type="button"
        onClick={onBack}
        disabled={!canGoBack}
        aria-label="Previous stage"
        className="flex items-center justify-center w-9 h-9 rounded-full transition-colors"
        style={{
          backgroundColor: canGoBack ? '#FFFFFF' : '#F5F4F1',
          border: '1px solid #EDEBE8',
          color: canGoBack ? '#1A1A1A' : '#C4C0BC',
          cursor: canGoBack ? 'pointer' : 'not-allowed',
        }}
      >
        <svg width="14" height="14" viewBox="0 0 16 16" fill="none" aria-hidden>
          <path d="M10 3L5 8L10 13" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </button>

      <div className="flex items-center gap-3 flex-1 justify-center">
        {stages.map((s, idx) => {
          const isCurrent = idx === currentIdx;
          const isPast = idx < currentIdx;
          return (
            <div key={s} className="flex items-center gap-3">
              <div className="flex flex-col items-center" style={{ minWidth: 0 }}>
                <span
                  style={{
                    width: isCurrent ? 28 : 8,
                    height: 8,
                    borderRadius: 999,
                    backgroundColor: isCurrent ? TEAL : isPast ? `${TEAL}66` : '#E5E3DF',
                    transition: 'all 200ms ease',
                  }}
                />
                <span
                  className="font-sans hidden sm:block"
                  style={{
                    fontSize: 10,
                    fontWeight: isCurrent ? 700 : 500,
                    letterSpacing: 0.4,
                    textTransform: 'uppercase',
                    color: isCurrent ? '#1A1A1A' : '#A8A29E',
                    marginTop: 6,
                    whiteSpace: 'nowrap',
                  }}
                >
                  {STAGE_LABELS[s]}
                </span>
              </div>
              {idx < stages.length - 1 && (
                <span style={{ width: 18, height: 1, backgroundColor: '#E5E3DF' }} />
              )}
            </div>
          );
        })}
      </div>

      <button
        type="button"
        onClick={onForward}
        disabled={!canGoForward}
        aria-label="Next stage"
        className="flex items-center justify-center gap-2 h-9 rounded-full transition-colors"
        style={{
          backgroundColor: canGoForward ? TEAL : '#F5F4F1',
          color: canGoForward ? '#FFFFFF' : '#C4C0BC',
          padding: forwardLabel ? '0 14px' : '0',
          width: forwardLabel ? 'auto' : 36,
          fontSize: 13,
          fontWeight: 600,
          cursor: canGoForward ? 'pointer' : 'not-allowed',
          border: 'none',
        }}
      >
        {forwardLabel && <span className="hidden sm:inline">{forwardLabel}</span>}
        <svg width="14" height="14" viewBox="0 0 16 16" fill="none" aria-hidden>
          <path d="M6 3L11 8L6 13" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </button>
    </div>
  );
};

export default StageProgress;
