/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * FluencyTrap — a mistake-first micro-interactive for the Comeback Engine.
 *
 * Leads with the WRONG move: the student rates how confident they FEEL they could
 * explain a topic, then actually tries to recall it cold — and sees the gap
 * between felt confidence and real recall. That gap is the "fluency trap":
 * re-reading builds the feeling of knowing without the recall to back it up
 * (Dunlosky 2013; Roediger & Karpicke 2006). The fix is the kind of recall the
 * week's missions prescribe.
 *
 * DEIS framing: this lowers effort, not raises the bar — it reframes "I studied
 * for hours and it didn't work" as a fixable technique problem, not a verdict.
 * Design: white 2px #1a1a1a card; the confidence bar is neutral ink, the recall
 * bar earns success green only when recall is high; the animation encodes the
 * gap (the lesson), never decorates. No orange-as-good.
 */

import React, { useState } from 'react';
import { MotionDiv } from '../Motion';
import { Brain, RotateCcw } from 'lucide-react';
import { COLORS } from '../../design/tokens';
import { LOW_UTILITY_STRATEGIES } from '../../comebackMissionData';

const INK = '#1a1a1a';
const MAX_BAR = 104; // px

type Phase = 'rate' | 'recall' | 'reveal';

const FluencyTrap: React.FC = () => {
  const [phase, setPhase] = useState<Phase>('rate');
  const [confidence, setConfidence] = useState(0); // 0 = unset, then 1–5
  const [recalled, setRecalled] = useState(-1);     // -1 = unset, then 0–3

  const reset = () => { setPhase('rate'); setConfidence(0); setRecalled(-1); };

  const confidencePct = confidence / 5;          // 0–1
  const recallPct = recalled >= 0 ? recalled / 3 : 0;
  const recallEarned = recalled >= 2;            // 2–3 of 3 = real recall
  const gap = confidencePct - recallPct;

  return (
    <div className="rounded-2xl border-2 p-5" style={{ borderColor: INK, backgroundColor: '#FFFFFF' }}>
      <div className="flex items-center gap-2 mb-1">
        <Brain size={16} style={{ color: COLORS.accent }} />
        <p className="text-[10px] font-bold uppercase tracking-[0.15em] text-zinc-400">The fluency trap · 20 seconds</p>
      </div>

      {phase === 'rate' && (
        <>
          <h3 className="text-base font-bold mb-1" style={{ color: INK, fontFamily: "'Source Serif 4', serif" }}>
            Pick a topic you’d say you know.
          </h3>
          <p className="text-[13px] leading-relaxed text-[#5a544e] mb-4">
            With the book closed, how confident are you that you could explain it right now?
          </p>
          <div className="flex gap-2">
            {[1, 2, 3, 4, 5].map(n => (
              <button
                key={n}
                onClick={() => { setConfidence(n); setPhase('recall'); }}
                className="flex-1 py-2.5 rounded-lg text-sm font-bold transition-colors bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-300 hover:bg-zinc-200 dark:hover:bg-zinc-700"
              >
                {n}
              </button>
            ))}
          </div>
          <div className="flex justify-between mt-1">
            <span className="text-[9px] text-zinc-400">Not at all</span>
            <span className="text-[9px] text-zinc-400">Totally</span>
          </div>
        </>
      )}

      {phase === 'recall' && (
        <>
          <h3 className="text-base font-bold mb-1" style={{ color: INK, fontFamily: "'Source Serif 4', serif" }}>
            Now actually do it.
          </h3>
          <p className="text-[13px] leading-relaxed text-[#5a544e] mb-4">
            Close everything and write the 3 key points from memory. No peeking. How many did you really get?
          </p>
          <div className="flex gap-2">
            {[0, 1, 2, 3].map(n => (
              <button
                key={n}
                onClick={() => { setRecalled(n); setPhase('reveal'); }}
                className="flex-1 py-2.5 rounded-lg text-sm font-bold transition-colors bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-300 hover:bg-zinc-200 dark:hover:bg-zinc-700"
              >
                {n}
              </button>
            ))}
          </div>
          <div className="flex justify-between mt-1">
            <span className="text-[9px] text-zinc-400">None</span>
            <span className="text-[9px] text-zinc-400">All three</span>
          </div>
        </>
      )}

      {phase === 'reveal' && (
        <>
          <h3 className="text-base font-bold mb-3" style={{ color: INK, fontFamily: "'Source Serif 4', serif" }}>
            {gap > 0.2 ? 'That gap is the trap.' : 'Nicely calibrated — keep testing.'}
          </h3>

          {/* Two bars: felt confidence (neutral ink) vs actual recall (success when earned) */}
          <div className="flex items-end justify-center gap-8 mb-4" style={{ height: MAX_BAR + 24 }}>
            <div className="flex flex-col items-center justify-end" style={{ height: MAX_BAR }}>
              <MotionDiv
                initial={{ height: 0 }}
                animate={{ height: Math.max(6, confidencePct * MAX_BAR) }}
                transition={{ duration: 0.6 }}
                className="w-14 rounded-t-lg"
                style={{ backgroundColor: '#9A9590' }}
              />
            </div>
            <div className="flex flex-col items-center justify-end" style={{ height: MAX_BAR }}>
              <MotionDiv
                initial={{ height: 0 }}
                animate={{ height: Math.max(6, recallPct * MAX_BAR) }}
                transition={{ duration: 0.6, delay: 0.5 }}
                className="w-14 rounded-t-lg"
                style={{ backgroundColor: recallEarned ? COLORS.success : '#C9B8AE' }}
              />
            </div>
          </div>
          <div className="flex items-start justify-center gap-8 -mt-3 mb-4">
            <p className="w-14 text-center text-[10px] font-bold leading-tight" style={{ color: '#7a7068' }}>Felt you knew it</p>
            <p className="w-14 text-center text-[10px] font-bold leading-tight" style={{ color: recallEarned ? COLORS.successDarkText : '#7a7068' }}>Actually recalled</p>
          </div>

          <div className="rounded-xl px-4 py-3 mb-3" style={{ backgroundColor: COLORS.accentTint }}>
            <p className="text-[12.5px] leading-relaxed italic" style={{ color: COLORS.accentDarkText }}>
              {gap > 0.2
                ? `${LOW_UTILITY_STRATEGIES.note} That’s not a “you’re not academic” problem — it’s a fixable technique one.`
                : 'Your sense of what you know is matching what you can recall — that’s what testing yourself builds.'}
            </p>
          </div>
          <p className="text-[11px] leading-relaxed text-[#5a544e] mb-4">
            The fix is below: this week’s missions are recall, spacing and mixed practice — the moves that actually move the needle.
            <span className="block text-[10px] text-zinc-400 mt-1">{LOW_UTILITY_STRATEGIES.source}</span>
          </p>

          <button
            onClick={reset}
            className="inline-flex items-center gap-1.5 text-[12px] font-semibold text-zinc-500 hover:text-zinc-700 dark:hover:text-zinc-300 transition-colors"
          >
            <RotateCcw size={13} /> Try another topic
          </button>
        </>
      )}
    </div>
  );
};

export default FluencyTrap;
