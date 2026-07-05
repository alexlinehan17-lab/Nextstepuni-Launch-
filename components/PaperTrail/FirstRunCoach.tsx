/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — first-run coach (onboarding). A single, dismissible strip that
 * explains the study loop to a brand-new student in three honest steps. Shown
 * only when there is zero activity (no self-marks, no review deck, no streak, no
 * recents) and not yet dismissed — so it never clutters a returning student's
 * home. Describes real features only; no promises.
 */

import React, { useState } from 'react';
import { X } from 'lucide-react';

const INK = '#1a1a1a';
const ACCENT = '#F26B1F';

const DISMISS_KEY = (uid?: string) => `pt:coachDismissed:${uid || 'anon'}`;

const isDismissed = (uid?: string): boolean => {
  try {
    return localStorage.getItem(DISMISS_KEY(uid)) === '1';
  } catch {
    return false;
  }
};

const STEPS = [
  'Open any paper beside its official marking scheme.',
  'Mark yourself against it — tag where you lost the marks.',
  'We surface your weak topics, schedule spaced review, and count down to your exam.',
];

interface Props {
  uid?: string;
  /** True once the student has practised anything — hides the coach for good. */
  hasActivity: boolean;
}

const FirstRunCoach: React.FC<Props> = ({ uid, hasActivity }) => {
  const [dismissed, setDismissed] = useState(() => isDismissed(uid));
  if (hasActivity || dismissed) return null;

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
      <p className="text-[10.5px] font-bold uppercase tracking-[0.12em] mb-0.5" style={{ color: '#9e9186' }}>New here?</p>
      <p className="text-[15px] font-semibold mb-3" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>How Paper Trail builds your revision</p>
      <ol className="space-y-2">
        {STEPS.map((s, i) => (
          <li key={i} className="flex items-start gap-2.5">
            <span className="shrink-0 mt-0.5 w-5 h-5 rounded-full flex items-center justify-center text-[11px] font-bold text-white" style={{ backgroundColor: ACCENT, fontFamily: "'Source Serif 4', serif" }}>{i + 1}</span>
            <span className="text-[13px] leading-snug" style={{ color: '#5a5550' }}>{s}</span>
          </li>
        ))}
      </ol>
    </div>
  );
};

export default FirstRunCoach;
