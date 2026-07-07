/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — handwriting-speed calibrator (feature F4). A ~2-minute
 * self-timed drill: the app shows a fixed 40-word passage, the student copies
 * it BY HAND on real paper while the app times them (typing speed is not
 * handwriting speed), and the resulting words-per-minute personalises the
 * time-budget guidance in the viewer and the mock builder.
 *
 * Rendered as a self-contained overlay so both Viewer and MockExamBuilder can
 * open it without touching PaperTrail/index.tsx. Local-only (wpmStore).
 */

import React, { useEffect, useRef, useState } from 'react';
import { PenLine, Play, RotateCcw, Square, X } from 'lucide-react';
import {
  CALIBRATION_PASSAGE,
  CALIBRATION_WORD_COUNT,
  STANDARD_WPM,
  computeWpm,
  paceScale,
  saveCalibration,
  type WpmCalibration,
} from './wpmStore';

const INK = '#1a1a1a';
const ACCENT = '#F26B1F';

interface Props {
  uid?: string;
  /** Fired once a calibration is measured and stored. */
  onSaved: (cal: WpmCalibration) => void;
  onClose: () => void;
}

type Phase = 'intro' | 'timing' | 'result' | 'tooQuick';

const WpmCalibrator: React.FC<Props> = ({ uid, onSaved, onClose }) => {
  const [phase, setPhase] = useState<Phase>('intro');
  const [cal, setCal] = useState<WpmCalibration | null>(null);
  const [, setTick] = useState(0);
  const startTs = useRef(0);
  const closeRef = useRef<HTMLButtonElement | null>(null);

  useEffect(() => {
    closeRef.current?.focus();
  }, []);

  // Live elapsed readout while the pen is moving.
  useEffect(() => {
    if (phase !== 'timing') return;
    const id = setInterval(() => setTick(t => t + 1), 500);
    return () => clearInterval(id);
  }, [phase]);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [onClose]);

  const begin = () => {
    startTs.current = Date.now();
    setPhase('timing');
  };

  const stop = () => {
    const seconds = Math.round((Date.now() - startTs.current) / 1000);
    const wpm = computeWpm(CALIBRATION_WORD_COUNT, seconds);
    if (wpm == null) {
      setPhase('tooQuick');
      return;
    }
    const next: WpmCalibration = { wpm, words: CALIBRATION_WORD_COUNT, seconds, ts: Date.now() };
    saveCalibration(uid, next);
    setCal(next);
    setPhase('result');
    onSaved(next);
  };

  const elapsedSec = phase === 'timing' ? Math.floor((Date.now() - startTs.current) / 1000) : 0;
  const fmt = (s: number) => `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`;

  return (
    <div className="fixed inset-0 z-[130] flex items-end sm:items-center justify-center">
      <div className="absolute inset-0 bg-black/40" onClick={onClose} aria-hidden />
      <div
        role="dialog"
        aria-modal="true"
        aria-label="Handwriting speed calibration"
        className="relative w-full sm:max-w-md max-h-[90vh] overflow-y-auto overscroll-contain bg-white rounded-t-2xl sm:rounded-2xl border-2 border-[#1a1a1a] p-5"
        style={{ paddingBottom: 'calc(20px + var(--sab, 0px))' }}
      >
        <div className="flex items-start gap-2 mb-1">
          <h2 className="flex-1 text-[19px] font-semibold" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>
            <PenLine size={16} className="inline -mt-0.5 mr-1.5" style={{ color: ACCENT }} />
            How fast do you write?
          </h2>
          <button ref={closeRef} onClick={onClose} aria-label="Close" className="p-1.5 -mr-1 -mt-1 rounded-lg" style={{ color: '#9e9186' }}>
            <X size={17} />
          </button>
        </div>

        {(phase === 'intro' || phase === 'timing' || phase === 'tooQuick') && (
          <>
            <p className="text-[13px] leading-relaxed mb-3" style={{ color: '#5a5550' }}>
              Grab a pen and paper. Copy the passage below <strong>by hand, at your normal exam pace</strong> — the app
              only does the timing. Takes about two minutes, and your time budgets get personalised to how you actually write.
            </p>

            <div className="rounded-xl border-2 border-[#1a1a1a] bg-white p-4 mb-2">
              <p className="text-[10px] font-bold uppercase tracking-[0.12em] mb-1.5" style={{ color: '#9e9186' }}>
                Copy this — {CALIBRATION_WORD_COUNT} words
              </p>
              <p className="text-[15px] leading-relaxed" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>
                {CALIBRATION_PASSAGE}
              </p>
            </div>

            {phase === 'tooQuick' && (
              <div className="rounded-r-xl px-4 py-3 mb-2" style={{ backgroundColor: '#FDEEDF', borderLeft: `3px solid ${ACCENT}` }}>
                <p className="text-[13px] italic" style={{ color: '#8C3A0E' }}>
                  That was too quick to be a real handwriting pass — nothing was saved. Write the whole passage out, then stop the timer.
                </p>
              </div>
            )}

            {phase === 'timing' ? (
              <div className="flex items-center gap-3 mt-3">
                <span
                  className="text-[32px] font-bold tabular-nums leading-none"
                  style={{ fontFamily: "'Source Serif 4', serif", color: ACCENT }}
                  role="timer"
                >
                  {fmt(elapsedSec)}
                </span>
                <button
                  onClick={stop}
                  className="flex-1 inline-flex items-center justify-center gap-1.5 py-3 rounded-full text-[14.5px] font-semibold text-white transition-transform active:translate-y-0.5"
                  style={{ backgroundColor: ACCENT, boxShadow: '0 3px 0 #B54D14' }}
                >
                  <Square size={14} /> I’ve finished writing
                </button>
              </div>
            ) : (
              <button
                onClick={begin}
                className="w-full mt-3 inline-flex items-center justify-center gap-1.5 py-3 rounded-full text-[14.5px] font-semibold text-white transition-transform active:translate-y-0.5"
                style={{ backgroundColor: ACCENT, boxShadow: '0 3px 0 #B54D14' }}
              >
                <Play size={14} /> Pen ready — start timing
              </button>
            )}
          </>
        )}

        {phase === 'result' && cal && (
          <>
            <div className="text-center py-3">
              <p className="text-[44px] font-bold leading-none" style={{ fontFamily: "'Source Serif 4', serif", color: ACCENT }}>
                {cal.wpm}
              </p>
              <p className="text-[11px] font-bold uppercase tracking-[0.12em] mt-1" style={{ color: '#9e9186' }}>
                words per minute
              </p>
            </div>
            <div className="rounded-r-xl px-4 py-3 mb-3" style={{ backgroundColor: '#E8F2EC', borderLeft: '3px solid #3A8D5F' }}>
              <p className="text-[13px] italic" style={{ color: '#1F5F3E' }}>
                Saved. Your time budgets are now scaled ×{paceScale(cal).toFixed(2)}
                {cal.wpm < STANDARD_WPM
                  ? ' — you write slower than the standard pace the budgets assume, so each question gets a little more writing time.'
                  : cal.wpm > STANDARD_WPM
                    ? ' — you write faster than the standard pace the budgets assume, so each question needs a little less writing time.'
                    : ' — right on the standard pace.'}
              </p>
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => setPhase('intro')}
                className="inline-flex items-center gap-1.5 rounded-full px-4 py-2 text-[13px] font-semibold border-2 transition-transform active:translate-y-0.5"
                style={{ borderColor: '#d0cdc8', color: '#7a7068' }}
              >
                <RotateCcw size={13} /> Redo
              </button>
              <button
                onClick={onClose}
                className="flex-1 py-2 rounded-full text-[13.5px] font-semibold text-white transition-transform active:translate-y-0.5"
                style={{ backgroundColor: ACCENT, boxShadow: '0 3px 0 #B54D14' }}
              >
                Done
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default WpmCalibrator;
