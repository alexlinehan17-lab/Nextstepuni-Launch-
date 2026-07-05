/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — first-run coach (onboarding). A dismissible card that walks a new
 * student through the study loop as a LIVE checklist: each step ticks itself off
 * as the student actually does it (opens a paper → marks themselves → starts a
 * spaced-review deck). The heading warms up once they're underway, and the whole
 * card retires the moment all three are done — so it never clutters a returning
 * student's home. Describes real actions only; no promises.
 */

import React, { useState } from 'react';
import { X, Check } from 'lucide-react';

const INK = '#1a1a1a';
const ACCENT = '#F26B1F';
const SUCCESS = '#3A8D5F';

const DISMISS_KEY = (uid?: string) => `pt:coachDismissed:${uid || 'anon'}`;

const isDismissed = (uid?: string): boolean => {
  try {
    return localStorage.getItem(DISMISS_KEY(uid)) === '1';
  } catch {
    return false;
  }
};

export interface CoachStep {
  label: string;
  done: boolean;
}

interface Props {
  uid?: string;
  steps: CoachStep[];
}

const FirstRunCoach: React.FC<Props> = ({ uid, steps }) => {
  const [dismissed, setDismissed] = useState(() => isDismissed(uid));
  const doneCount = steps.filter(s => s.done).length;
  // Retire once the loop is running (all steps done) or the student dismisses it.
  if (dismissed || doneCount === steps.length) return null;

  const firstPending = steps.findIndex(s => !s.done);
  const started = doneCount > 0;

  const dismiss = () => {
    try {
      localStorage.setItem(DISMISS_KEY(uid), '1');
    } catch {
      /* private mode — degrade silently */
    }
    setDismissed(true);
  };

  return (
    <div className="relative w-full rounded-2xl border-2 border-[#1a1a1a] dark:border-zinc-700 bg-white dark:bg-zinc-900 px-4 py-3.5 mb-5">
      <button
        onClick={dismiss}
        aria-label="Dismiss"
        className="absolute top-2.5 right-2.5 w-7 h-7 rounded-lg flex items-center justify-center transition-colors hover:bg-zinc-100 dark:hover:bg-zinc-800"
        style={{ color: '#9e9186' }}
      >
        <X size={15} />
      </button>
      <div className="flex items-center gap-2 mb-0.5">
        <p className="text-[10.5px] font-bold uppercase tracking-[0.12em]" style={{ color: '#9e9186' }}>{started ? 'Getting started' : 'New here?'}</p>
        <span className="text-[10.5px] font-bold tabular-nums" style={{ color: ACCENT }}>{doneCount}/{steps.length}</span>
      </div>
      <p className="text-[15px] font-semibold mb-3" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>
        {started ? 'Your revision is taking shape' : 'How Paper Trail builds your revision'}
      </p>
      <ol className="space-y-2">
        {steps.map((s, i) => {
          const isNext = i === firstPending;
          return (
            <li key={i} className="flex items-start gap-2.5">
              <span
                className="shrink-0 mt-0.5 w-5 h-5 rounded-full flex items-center justify-center text-[11px] font-bold"
                style={
                  s.done
                    ? { backgroundColor: SUCCESS, color: '#fff', fontFamily: "'Source Serif 4', serif" }
                    : isNext
                      ? { backgroundColor: ACCENT, color: '#fff', fontFamily: "'Source Serif 4', serif" }
                      : { backgroundColor: '#e0dbd4', color: '#9e9186', fontFamily: "'Source Serif 4', serif" }
                }
              >
                {s.done ? <Check size={12} /> : i + 1}
              </span>
              <span
                className="text-[13px] leading-snug"
                style={{ color: s.done ? '#9e9186' : isNext ? '#3a3530' : '#7a7068', textDecoration: s.done ? 'line-through' : 'none', fontWeight: isNext ? 600 : 400 }}
              >
                {s.label}
              </span>
            </li>
          );
        })}
      </ol>
    </div>
  );
};

export default FirstRunCoach;
