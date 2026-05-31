/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Exam Reps — one real Leaving Cert question at a time, marked the examiner's
 * way. The ENTIRE tool is one card progressing through four in-place beats:
 *   intro → attempt → mark → done
 * There is deliberately NO router, NO tabs, NO library — the predecessor died
 * of exactly that fragmentation. One screen, one action, the next step always
 * the single orange button. Spacing/interleaving is handled invisibly; the
 * student never chooses or schedules anything.
 *
 * Evidence spine: generative retrieval (write from a blank box) + immediate
 * item-level feedback (self-mark against the real scheme) + calibration
 * (commit a confidence before you see the truth). See the build plan.
 */
import React, { useState, useEffect, useMemo, useRef } from 'react';
import { Check, ArrowRight } from 'lucide-react';
import { COLORS } from '../../design/tokens';
import PrimaryActionButton from '../ui/PrimaryActionButton';
import { useExamReps } from '../../hooks/useExamReps';
import { REP_CARDS } from '../../examRepsData';
import { type RepCard, type Confidence, ribbonId } from '../../types/examReps';

type Beat = 'intro' | 'attempt' | 'mark' | 'done';

const CONFIDENCE_OPTIONS: { id: Confidence; label: string }[] = [
  { id: 'unsure', label: 'Unsure' },
  { id: 'maybe', label: 'Maybe' },
  { id: 'confident', label: 'Confident' },
];

// ─── Soft marks-to-minutes arc (never a red countdown) ───────────────────────
const TimerArc: React.FC<{ progress: number; label: string }> = ({ progress, label }) => {
  const r = 15;
  const circ = 2 * Math.PI * r;
  const clamped = Math.max(0, Math.min(1, progress));
  return (
    <div className="flex items-center gap-2">
      <svg width="38" height="38" viewBox="0 0 38 38" aria-hidden="true">
        <circle cx="19" cy="19" r={r} fill="none" stroke="#E7E5E2" strokeWidth="4" />
        <circle
          cx="19" cy="19" r={r} fill="none" stroke={COLORS.accent} strokeWidth="4" strokeLinecap="round"
          strokeDasharray={circ} strokeDashoffset={circ * (1 - clamped)} transform="rotate(-90 19 19)"
          style={{ transition: 'stroke-dashoffset 0.9s linear' }}
        />
      </svg>
      <span className="text-xs text-[#7a7068] dark:text-zinc-400">{label}</span>
    </div>
  );
};

// Render the question. In the attempt beat the command word is a tappable
// highlight that pops a tooltip with what the word is actually asking for.
function renderQuestion(card: RepCard, tappable: boolean, tipOpen: boolean, onToggle: () => void): React.ReactNode {
  const text = card.questionText;
  const word = card.commandWord?.word;
  if (!word) return <span className="whitespace-pre-line">{text}</span>;
  const idx = text.toLowerCase().indexOf(word.toLowerCase());
  if (idx < 0) return <span className="whitespace-pre-line">{text}</span>;
  const before = text.slice(0, idx);
  const match = text.slice(idx, idx + word.length);
  const after = text.slice(idx + word.length);
  return (
    <span className="whitespace-pre-line">
      {before}
      {tappable ? (
        <span style={{ position: 'relative', display: 'inline-block' }}>
          <button
            type="button"
            onClick={onToggle}
            aria-expanded={tipOpen}
            className="font-semibold rounded px-0.5 transition-colors"
            style={{ backgroundColor: COLORS.accentTint, color: COLORS.accentDarkText, boxShadow: `inset 0 -2px 0 ${COLORS.accent}` }}
          >
            {match}
          </button>
          {tipOpen && (
            <span
              role="tooltip"
              className="absolute z-30 left-0 top-full mt-1.5 w-64 max-w-[80vw] rounded-xl border-2 p-3 block"
              style={{ borderColor: COLORS.border, backgroundColor: '#FAFBF6', boxShadow: `4px 4px 0 0 ${COLORS.border}` }}
            >
              <span className="block text-xs font-normal leading-relaxed normal-case" style={{ color: '#1A1A1A' }}>
                {card.commandWord!.reminder}
              </span>
            </span>
          )}
        </span>
      ) : (
        <span className="font-semibold">{match}</span>
      )}
      {after}
    </span>
  );
}

const ExamReps: React.FC<{ uid?: string }> = ({ uid }) => {
  const { state, recordRep } = useExamReps(uid);

  const [cardIndex, setCardIndex] = useState(0);
  const [beat, setBeat] = useState<Beat>('intro');
  const [confidence, setConfidence] = useState<Confidence | null>(null);
  const [answer, setAnswer] = useState('');
  const [tipOpen, setTipOpen] = useState(false);
  const [ribbonHad, setRibbonHad] = useState<Record<string, boolean>>({});
  const [elapsed, setElapsed] = useState(0);
  const [finished, setFinished] = useState(false);
  const recordedRef = useRef(false);

  const card = REP_CARDS[cardIndex];

  // soft timer — only runs during the attempt
  useEffect(() => {
    if (beat !== 'attempt') return;
    const t = setInterval(() => setElapsed(e => e + 1), 1000);
    return () => clearInterval(t);
  }, [beat]);

  const derived = useMemo(() => {
    if (!card) return null;
    const totalMarks = card.ribbons.reduce((s, r) => (r.kind !== 'gate' ? s + r.marks : s), 0);
    const captured = card.ribbons.reduce((s, r, i) => (r.kind !== 'gate' && ribbonHad[ribbonId(r, i)] ? s + r.marks : s), 0);
    const onTable = card.ribbons.reduce((s, r, i) => (r.kind !== 'gate' && ribbonHad[ribbonId(r, i)] === false ? s + r.marks : s), 0);
    const allMarked = card.ribbons.every((r, i) => ribbonId(r, i) in ribbonHad);
    const missedCount = card.ribbons.filter((r, i) => ribbonHad[ribbonId(r, i)] === false).length;
    const gateMissed = card.ribbons.some((r, i) => r.kind === 'gate' && ribbonHad[ribbonId(r, i)] === false);
    return { totalMarks, captured, onTable, allMarked, missedCount, gateMissed };
  }, [card, ribbonHad]);

  if (!card || !derived) {
    return (
      <div className="w-full max-w-xl mx-auto py-16 text-center text-[#7a7068]">
        No reps available yet — more are being added.
      </div>
    );
  }

  const resetRep = () => {
    setConfidence(null); setAnswer(''); setTipOpen(false);
    setRibbonHad({}); setElapsed(0); setFinished(false);
    recordedRef.current = false; setBeat('intro');
  };

  const pickNext = (): number => {
    if (REP_CARDS.length <= 1) return cardIndex;
    const curr = REP_CARDS[cardIndex];
    const others = REP_CARDS.map((c, i) => ({ c, i })).filter(x => x.i !== cardIndex);
    const diffSubject = others.filter(x => x.c.subject !== curr.subject);
    return (diffSubject.length ? diffSubject : others)[0].i;
  };

  const goDone = () => {
    if (!recordedRef.current) {
      recordRep({ cardId: card.id, capturedMarks: derived.captured, missedRibbons: derived.missedCount });
      recordedRef.current = true;
    }
    setBeat('done');
  };

  const timerProgress = elapsed / (card.minutes * 60);
  const atCap = timerProgress >= 1;
  const bankedAllTime = state.banked; // includes this rep once recorded

  const cardShell = 'w-full max-w-xl mx-auto rounded-2xl border-2 border-[#1A1A1A] dark:border-zinc-700 bg-white dark:bg-zinc-900 shadow-[4px_4px_0_0_#1A1A1A] dark:shadow-[4px_4px_0_0_#3f3f46] p-6 md:p-7';

  // ── INTRO ──────────────────────────────────────────────────────────────
  if (beat === 'intro') {
    return (
      <div className={cardShell}>
        <div className="flex items-center justify-between mb-4">
          <span className="text-[10px] font-bold uppercase tracking-[0.15em] px-2.5 py-1 rounded-full" style={{ backgroundColor: '#F0EEEB', color: '#7a7068' }}>
            {card.subjectLabel} · {card.questionRef}
          </span>
          <span className="text-[11px] font-semibold text-[#7a7068] dark:text-zinc-400">
            {card.marks} marks · ~{card.minutes} min
          </span>
        </div>

        <p className="font-serif text-xl md:text-2xl leading-relaxed text-[#1A1A1A] dark:text-white mb-6">
          {renderQuestion(card, false, false, () => {})}
        </p>

        <p className="text-[11px] font-bold uppercase tracking-[0.15em] text-zinc-400 mb-2">Before you start — how sure are you?</p>
        <div className="flex gap-2 mb-6">
          {CONFIDENCE_OPTIONS.map(opt => {
            const on = confidence === opt.id;
            return (
              <button
                key={opt.id}
                type="button"
                onClick={() => setConfidence(opt.id)}
                className="flex-1 rounded-xl border-2 py-2.5 text-sm font-semibold transition-colors"
                style={{ borderColor: on ? COLORS.accent : COLORS.border, backgroundColor: on ? COLORS.accentTint : '#FFFFFF', color: '#1A1A1A' }}
              >
                {opt.label}
              </button>
            );
          })}
        </div>

        <PrimaryActionButton
          label="Start the rep"
          onClick={() => { setElapsed(0); setBeat('attempt'); }}
          disabled={!confidence}
          className="w-full"
        />
      </div>
    );
  }

  // ── ATTEMPT ────────────────────────────────────────────────────────────
  if (beat === 'attempt') {
    return (
      <div className={cardShell}>
        <div className="flex items-center justify-between mb-3">
          <span className="text-[10px] font-bold uppercase tracking-[0.15em] text-zinc-400">{card.subjectLabel} · {card.questionRef}</span>
          <TimerArc progress={timerProgress} label={atCap ? 'that’s your exam budget — finish if you need' : `~${card.minutes} min budget`} />
        </div>

        {card.commandWord && !tipOpen && (
          <p className="text-[11px] text-zinc-400 mb-1.5">Tap the highlighted word to see what it’s asking for.</p>
        )}

        <div className="font-serif text-lg leading-relaxed text-[#1A1A1A] dark:text-white mb-4">
          {renderQuestion(card, !!card.commandWord, tipOpen, () => setTipOpen(v => !v))}
        </div>

        {card.answerKind === 'paper' ? (
          <div className="rounded-xl border-2 border-dashed p-5 mb-5 text-center" style={{ borderColor: '#d0cdc8', backgroundColor: '#F9F9F7' }}>
            <p className="text-sm font-semibold text-[#1A1A1A] dark:text-zinc-200">Grab a piece of paper for this one.</p>
            <p className="text-xs text-[#7a7068] dark:text-zinc-400 mt-1">
              Sketch it out as you would in the exam, then tap <span className="font-semibold">Mark it</span> when you’re ready.
            </p>
          </div>
        ) : (
          <textarea
            value={answer}
            onChange={e => setAnswer(e.target.value)}
            placeholder={card.answerKind === 'steps' ? 'Show your steps — exactly what you’d write…' : 'Write what you’d actually write in the exam…'}
            rows={8}
            className="w-full rounded-xl border-2 p-3 text-sm leading-relaxed text-[#1A1A1A] dark:text-white bg-white dark:bg-zinc-800 focus:outline-none resize-y mb-5"
            style={{ borderColor: COLORS.border }}
          />
        )}

        <PrimaryActionButton label="Mark it" onClick={() => setBeat('mark')} className="w-full" />
      </div>
    );
  }

  // ── MARK ───────────────────────────────────────────────────────────────
  if (beat === 'mark') {
    return (
      <div className={cardShell}>
        {card.answerKind === 'paper' ? (
          <p className="text-xs text-[#7a7068] dark:text-zinc-400 mb-5">You did this one on paper — now mark it against the scheme.</p>
        ) : (
          <>
            <p className="text-[10px] font-bold uppercase tracking-[0.15em] text-zinc-400 mb-2">Your answer</p>
            <div className="rounded-xl p-3 mb-5 text-sm leading-relaxed whitespace-pre-wrap max-h-32 overflow-y-auto" style={{ backgroundColor: '#F9F9F7', color: '#5a544e' }}>
              {answer.trim() || <span className="italic text-zinc-400">(left blank)</span>}
            </div>
          </>
        )}

        <p className="text-[10px] font-bold uppercase tracking-[0.15em] text-zinc-400 mb-1">Mark it like the examiner</p>
        <p className="text-xs text-[#7a7068] dark:text-zinc-400 mb-3">For each point the scheme rewards, did your answer have it?</p>

        <div className="space-y-2 mb-5">
          {card.ribbons.map((r, i) => {
            const id = ribbonId(r, i);
            const had = ribbonHad[id];
            const isGate = r.kind === 'gate';
            return (
              <div
                key={id}
                className="rounded-xl border-2 p-3 transition-colors"
                style={{
                  borderColor: had === true ? COLORS.success : had === false ? '#d0cdc8' : COLORS.border,
                  backgroundColor: had === true ? COLORS.successTint : had === false ? '#F9F9F7' : '#FFFFFF',
                }}
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="min-w-0">
                    <p className="text-sm font-semibold text-[#1A1A1A]">{r.label}</p>
                    <p className="text-[11px] font-bold mt-0.5" style={{ color: isGate ? COLORS.accentDarkText : '#7a7068' }}>
                      {isGate ? 'Essential — or the whole answer scores 0' : `worth ${r.marks} marks`}
                    </p>
                  </div>
                  <div className="flex gap-1.5 shrink-0">
                    <button
                      type="button"
                      onClick={() => setRibbonHad(p => ({ ...p, [id]: true }))}
                      className="px-2.5 py-1.5 rounded-lg text-[11px] font-bold transition-colors flex items-center gap-1"
                      style={had === true ? { backgroundColor: COLORS.success, color: '#FFFFFF' } : { backgroundColor: '#F0EEEB', color: '#7a7068' }}
                    >
                      {had === true && <Check size={11} />} I had this
                    </button>
                    <button
                      type="button"
                      onClick={() => setRibbonHad(p => ({ ...p, [id]: false }))}
                      className="px-2.5 py-1.5 rounded-lg text-[11px] font-bold transition-colors"
                      style={had === false ? { backgroundColor: '#1A1A1A', color: '#FFFFFF' } : { backgroundColor: '#F0EEEB', color: '#7a7068' }}
                    >
                      I didn’t
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* running marks-on-the-table */}
        <div className="rounded-xl px-4 py-3 mb-5 flex items-center justify-between" style={{ backgroundColor: derived.onTable > 0 || derived.gateMissed ? COLORS.accentTint : COLORS.successTint }}>
          <div>
            <p className="text-[10px] font-bold uppercase tracking-[0.15em]" style={{ color: derived.onTable > 0 || derived.gateMissed ? COLORS.accentDarkText : COLORS.successDarkText }}>
              Marks on the table
            </p>
            <p className="text-[11px]" style={{ color: derived.onTable > 0 || derived.gateMissed ? COLORS.accentDarkText : COLORS.successDarkText }}>
              {derived.gateMissed ? 'the essential point would zero this answer' : derived.onTable > 0 ? 'left for the taking' : 'nothing left behind — nice'}
            </p>
          </div>
          <span className="font-serif text-3xl font-bold" style={{ color: derived.onTable > 0 || derived.gateMissed ? COLORS.accent : COLORS.success }}>
            {derived.gateMissed ? card.marks : derived.onTable}
          </span>
        </div>

        <PrimaryActionButton label="See what you missed" onClick={goDone} disabled={!derived.allMarked} className="w-full" />
        {!derived.allMarked && <p className="text-[11px] text-center text-zinc-400 mt-2">Mark every point above to continue.</p>}
      </div>
    );
  }

  // ── DONE ───────────────────────────────────────────────────────────────
  const calibration =
    confidence === 'confident' && derived.captured < derived.totalMarks * 0.6 ? 'Worth a revisit — you felt surer than the marks landed.'
    : confidence === 'unsure' && derived.captured >= derived.totalMarks * 0.6 ? 'Better than you thought — trust that more.'
    : 'Good calibration.';

  return (
    <div className={cardShell}>
      <p className="text-[10px] font-bold uppercase tracking-[0.15em] text-zinc-400 mb-2">The one lesson</p>
      <div className="pl-3 py-1 mb-3" style={{ borderLeft: `3px solid ${COLORS.accent}` }}>
        <p className="text-sm leading-relaxed text-[#1A1A1A] dark:text-zinc-200">{card.lesson.text}</p>
      </div>
      <span className="inline-block text-[10px] font-semibold px-2 py-1 rounded-md mb-5" style={{ backgroundColor: COLORS.successTint, color: COLORS.successDarkText }}>
        {card.lesson.source}
      </span>

      <div className="rounded-xl p-4 mb-5" style={{ backgroundColor: '#F9F9F7' }}>
        <p className="text-sm text-[#1A1A1A] dark:text-zinc-200">
          You said <span className="font-bold">{confidence}</span> — you captured{' '}
          <span className="font-bold" style={{ color: COLORS.success }}>{derived.captured}</span> of {derived.totalMarks} marks.
        </p>
        <p className="text-xs text-[#7a7068] dark:text-zinc-400 mt-1">{calibration}</p>
      </div>

      <div className="flex items-center justify-between mb-5">
        <span className="text-xs text-[#7a7068] dark:text-zinc-400">Marks banked all-time</span>
        <span className="font-serif text-2xl font-bold" style={{ color: COLORS.success }}>{bankedAllTime}</span>
      </div>

      {finished ? (
        <div className="text-center py-2">
          <p className="text-sm font-semibold text-[#1A1A1A] dark:text-white">Nice work — come back anytime.</p>
          <button type="button" onClick={resetRep} className="text-xs font-semibold underline mt-2" style={{ color: COLORS.accentDarkText }}>Start another</button>
        </div>
      ) : (
        <>
          <PrimaryActionButton label="Next question" icon={ArrowRight} onClick={() => { setCardIndex(pickNext()); resetRep(); }} className="w-full" />
          <button type="button" onClick={() => setFinished(true)} className="w-full text-center text-xs font-semibold text-zinc-400 hover:text-[#1A1A1A] transition-colors mt-3">
            I’m done for now
          </button>
        </>
      )}
    </div>
  );
};

export default ExamReps;
