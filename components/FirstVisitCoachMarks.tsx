/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * First-visit coach marks — three short spotlight steps on the home page:
 * the module tree, the Launchpad, then the "?" button, ending with the offer
 * to take the full Site Guide. Skippable at every step, shows exactly once
 * per account (localStorage). Targets are found by [data-coach="..."]; if a
 * target isn't visible (e.g. the collapsed mobile sidebar), the step renders
 * as a centred card instead of a spotlight — nothing ever breaks.
 */

import React, { useCallback, useEffect, useState } from 'react';

const STEPS: { target: string; title: string; body: string }[] = [
  {
    target: 'modules',
    title: 'Your lessons live here',
    body: 'Interactive modules that teach you how to learn — memory, focus, exam craft. They unlock section by section.',
  },
  {
    target: 'launchpad',
    title: 'Your exam tools live here',
    body: 'The Launchpad: past papers beside their marking schemes, marking practice, CAO planning and more.',
  },
  {
    target: 'help',
    title: 'Lost? Press this anytime',
    body: 'The full guided tour of every core page lives behind the ? — with screenshots of exactly what each one does.',
  },
];

const KEY = 'nsu-coachmarks:';

export const coachMarksSeen = (uid?: string): boolean => {
  try {
    return localStorage.getItem(KEY + (uid || 'anon')) === '1';
  } catch {
    return true;
  }
};
const markSeen = (uid?: string) => {
  try {
    localStorage.setItem(KEY + (uid || 'anon'), '1');
  } catch { /* private mode */ }
};

const INK = '#1a1a1a';
const ACCENT = '#F26B1F';

interface Props {
  uid?: string;
  onFinish: () => void;
  /** "Take the full tour" on the last step. */
  onOpenGuide: () => void;
}

const FirstVisitCoachMarks: React.FC<Props> = ({ uid, onFinish, onOpenGuide }) => {
  const [step, setStep] = useState(0);
  const [rect, setRect] = useState<DOMRect | null>(null);

  const finish = useCallback(() => {
    markSeen(uid);
    onFinish();
  }, [uid, onFinish]);

  // Measure the current step's target; re-measure on resize/scroll.
  useEffect(() => {
    const measure = () => {
      const el = document.querySelector<HTMLElement>(`[data-coach="${STEPS[step].target}"]`);
      if (!el) { setRect(null); return; }
      const r = el.getBoundingClientRect();
      // A collapsed/offscreen target gets the centred-card fallback.
      setRect(r.width > 4 && r.height > 4 && r.bottom > 0 && r.top < window.innerHeight ? r : null);
    };
    measure();
    window.addEventListener('resize', measure);
    window.addEventListener('scroll', measure, true);
    return () => {
      window.removeEventListener('resize', measure);
      window.removeEventListener('scroll', measure, true);
    };
  }, [step]);

  const s = STEPS[step];
  const last = step === STEPS.length - 1;

  // Caption placement: under the target when there's room, else above it.
  const below = rect ? rect.bottom + 12 : 0;
  const captionTop = rect ? (below + 170 < window.innerHeight ? below : Math.max(12, rect.top - 182)) : 0;
  const captionLeft = rect ? Math.min(Math.max(12, rect.left), Math.max(12, window.innerWidth - 332)) : 0;

  return (
    <div className="fixed inset-0 z-[125]" role="dialog" aria-modal="true" aria-label="Quick tour">
      {rect ? (
        <div
          className="absolute rounded-xl pointer-events-none"
          style={{
            top: rect.top - 6,
            left: rect.left - 6,
            width: rect.width + 12,
            height: rect.height + 12,
            boxShadow: '0 0 0 9999px rgba(0,0,0,0.55)',
            border: `2px solid ${ACCENT}`,
          }}
        />
      ) : (
        <div className="absolute inset-0 bg-black/55" />
      )}

      <div
        className="absolute w-[320px] max-w-[calc(100vw-24px)] rounded-2xl border-2 bg-white px-4 py-3.5"
        style={
          rect
            ? { top: captionTop, left: captionLeft, borderColor: INK, boxShadow: '0 4px 0 rgba(0,0,0,0.4)' }
            : { top: '50%', left: '50%', transform: 'translate(-50%, -50%)', borderColor: INK, boxShadow: '0 4px 0 rgba(0,0,0,0.4)' }
        }
      >
        <p className="text-[10px] font-bold uppercase tracking-[0.12em] mb-1" style={{ color: '#9e9186' }}>
          Quick tour · {step + 1} of {STEPS.length}
        </p>
        <h3 className="text-[16px] font-semibold mb-1" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>
          {s.title}
        </h3>
        <p className="text-[12.5px] leading-relaxed mb-3" style={{ color: '#5a5550' }}>{s.body}</p>
        <div className="flex items-center justify-between gap-2">
          <button onClick={finish} className="text-[12px] font-medium" style={{ color: '#9e9186' }}>
            Skip
          </button>
          <div className="flex gap-2">
            {last && (
              <button
                onClick={() => { markSeen(uid); onOpenGuide(); }}
                className="rounded-full px-3.5 py-1.5 text-[12.5px] font-semibold border-2 transition-transform active:translate-y-0.5"
                style={{ borderColor: 'rgba(242,107,31,0.35)', color: ACCENT }}
              >
                Take the full tour
              </button>
            )}
            <button
              onClick={() => (last ? finish() : setStep(v => v + 1))}
              className="rounded-full px-4 py-1.5 text-[12.5px] font-semibold text-white transition-transform active:translate-y-0.5"
              style={{ backgroundColor: ACCENT, boxShadow: '0 2px 0 #B54D14' }}
            >
              {last ? 'Done' : 'Next →'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FirstVisitCoachMarks;
