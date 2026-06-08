/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * College Compass — "The Open Door" (embedded at the Money Stops trail stop).
 *
 * Mistake-first affordability reframe: the student first sees the "closed door"
 * sticker price they fear, taps to open it, and watches each cost fall away —
 * each one labelled with what removes it (Free Fees, SUSI, HEAR) — to reveal the
 * real, supported, much smaller cost, plus the lower-points HEAR door.
 *
 * Grounded in Destin & Oyserman (an open, affordable-looking path raises
 * low-income students' effort) + Snyder hope theory (show multiple routes).
 * Every euro figure is an ESTIMATE, source-stamped and verify-gated. NO student
 * income is collected — the SUSI bands are public info only. DEIS framing: the
 * win is "the door is open", never "you scored highly".
 */

import React, { useState } from 'react';
import { MotionDiv } from '../Motion';
import { ArrowRight, Check, DoorOpen, ExternalLink, Sparkles } from 'lucide-react';
import { COLORS } from '../../design/tokens';
import {
  OPEN_DOOR_LINES, OPEN_DOOR_HEAR, OPEN_DOOR_SUSI_BANDS, OPEN_DOOR_COPY, COMPASS_LAST_VERIFIED,
} from '../../collegeCompassData';

const TEAL = '#2A7D6F';
const TEAL_TINT = '#F0FAF8';

const chunkyCta =
  'w-full inline-flex items-center justify-center gap-2 px-5 py-3 rounded-2xl border-2 border-[#1A1A1A] font-sans font-bold text-sm text-white shadow-[3px_3px_0_0_#1A1A1A] hover:-translate-y-0.5 active:translate-y-0.5 active:shadow-[0px_0px_0_0_#1A1A1A] transition-all duration-150';

const Source: React.FC<{ label: string; url: string }> = ({ label, url }) => (
  <a href={url} target="_blank" rel="noreferrer" className="inline-flex items-center gap-1 text-[10px] font-semibold mt-1 underline" style={{ color: TEAL }}>
    {label} <ExternalLink size={9} />
  </a>
);

const OpenDoor: React.FC = () => {
  const [revealed, setRevealed] = useState(false);

  return (
    <div className="rounded-2xl border-2 border-[#1A1A1A] dark:border-zinc-700 bg-white dark:bg-zinc-900 shadow-[4px_4px_0_0_#1A1A1A] dark:shadow-[4px_4px_0_0_#3f3f46] p-5">
      <div className="flex items-center gap-2 mb-1">
        <DoorOpen size={18} style={{ color: TEAL }} />
        <p className="text-[10px] font-bold uppercase tracking-[0.15em] text-zinc-400 dark:text-zinc-500">The real cost of college</p>
      </div>

      {!revealed ? (
        // ── CLOSED DOOR — the feared wall (mistake-first) ──
        <>
          <h4 className="font-serif text-lg font-bold text-[#1A1A1A] dark:text-white mb-1">{OPEN_DOOR_COPY.closedHeading}</h4>
          <p className="text-xs leading-relaxed text-[#7a7068] dark:text-zinc-400 mb-3">{OPEN_DOOR_COPY.closedSub}</p>
          <div className="rounded-xl p-4 mb-4" style={{ backgroundColor: '#F1F3F2' }}>
            {OPEN_DOOR_LINES.map((l, i) => (
              <div key={l.id} className={`flex items-baseline justify-between gap-3 ${i > 0 ? 'mt-2 pt-2 border-t border-black/[0.06]' : ''}`}>
                <span className="text-[13px] font-semibold text-[#1A1A1A] dark:text-zinc-200">{l.label}</span>
                <span className="text-[13px] text-[#7a7068] dark:text-zinc-400 text-right">{l.sticker}</span>
              </div>
            ))}
          </div>
          <button type="button" onClick={() => setRevealed(true)} className={chunkyCta} style={{ backgroundColor: COLORS.accent }}>
            {OPEN_DOOR_COPY.revealCta} <ArrowRight size={16} />
          </button>
        </>
      ) : (
        // ── OPEN DOOR — the reveal, each cost falling away with what removes it ──
        <>
          <h4 className="font-serif text-lg font-bold text-[#1A1A1A] dark:text-white mb-1">{OPEN_DOOR_COPY.openHeading}</h4>
          <p className="text-xs leading-relaxed text-[#7a7068] dark:text-zinc-400 mb-3">{OPEN_DOOR_COPY.openSub}</p>

          <div className="space-y-2 mb-4">
            {OPEN_DOOR_LINES.map((l, i) => (
              <MotionDiv
                key={l.id}
                initial={{ opacity: 0, y: -6 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.2, duration: 0.3 }}
                className="rounded-xl p-3"
                style={{ backgroundColor: COLORS.successTint }}
              >
                <div className="flex items-baseline justify-between gap-3">
                  <span className="text-[13px] font-semibold text-[#1A1A1A]">{l.label}</span>
                  <span className="text-[13px] text-right">
                    <span className="line-through text-[#b0a89e] mr-1.5">{l.sticker}</span>
                    <span className="font-bold" style={{ color: COLORS.successDarkText }}>{l.open}</span>
                  </span>
                </div>
                <div className="flex items-center gap-1.5 mt-1">
                  <Check size={12} style={{ color: COLORS.success }} />
                  <span className="text-[10px] font-bold uppercase tracking-wide" style={{ color: COLORS.successDarkText }}>{l.removedBy}</span>
                </div>
                <p className="text-[11.5px] leading-snug mt-1 text-[#5a544e]">{l.detail}</p>
                <Source label={l.source.label} url={l.source.url} />
              </MotionDiv>
            ))}
          </div>

          {/* The second, lower door — HEAR (full border, never a left-border) */}
          <MotionDiv
            initial={{ opacity: 0, y: -6 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: OPEN_DOOR_LINES.length * 0.2, duration: 0.3 }}
            className="rounded-xl p-3 mb-4"
            style={{ backgroundColor: TEAL_TINT, border: `2px solid ${TEAL}` }}
          >
            <div className="flex items-center gap-1.5 mb-0.5">
              <Sparkles size={13} style={{ color: TEAL }} />
              <span className="text-[11px] font-bold" style={{ color: TEAL }}>{OPEN_DOOR_HEAR.label}</span>
            </div>
            <p className="text-[11.5px] leading-snug text-[#3a4a45]">{OPEN_DOOR_HEAR.detail}</p>
            <Source label={OPEN_DOOR_HEAR.source.label} url={OPEN_DOOR_HEAR.source.url} />
          </MotionDiv>

          {/* SUSI bands — public info, NO income input */}
          <p className="text-[11px] font-bold uppercase tracking-[0.12em] mb-1.5" style={{ color: TEAL }}>{OPEN_DOOR_COPY.bandsHeading}</p>
          <ul className="space-y-1 mb-1.5">
            {OPEN_DOOR_SUSI_BANDS.map((b, i) => (
              <li key={i} className="text-[12px] leading-snug text-[#3a3530] dark:text-zinc-300 flex gap-1.5">
                <span style={{ color: TEAL }}>•</span><span>{b}</span>
              </li>
            ))}
          </ul>
          <p className="text-[11px] italic text-[#7a7068] dark:text-zinc-400 mb-4">{OPEN_DOOR_COPY.bandsNote}</p>

          {/* The one concrete next step (EEF: never end in a daydream) */}
          <a href={OPEN_DOOR_COPY.step.url} target="_blank" rel="noreferrer" className={chunkyCta} style={{ backgroundColor: COLORS.accent }}>
            {OPEN_DOOR_COPY.step.label} <ExternalLink size={15} />
          </a>

          <p className="text-[10px] leading-snug text-zinc-400 mt-3">{OPEN_DOOR_COPY.disclaimer} Last reviewed {COMPASS_LAST_VERIFIED}.</p>
        </>
      )}
    </div>
  );
};

export default OpenDoor;
