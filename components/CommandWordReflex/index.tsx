/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Command-Word Reflex — read the question like an examiner.
 *
 * Pick a subject → see a real exam question → tap the command word (the cue
 * that says what to DO) → learn what it demands and the examiner-flagged trap.
 * Trains the decode-the-question skill on authentic questions.
 *
 * Aesthetics: Innovation-Zone tool vocabulary (chunky cardShell +
 * PrimaryActionButton); scholarly indigo identity with an amber "highlighter"
 * for the spotted cue word. Cool tints, no warm cream, no coloured left borders.
 */

import React, { useMemo, useState } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from '../Motion';
import { ArrowLeft, ArrowRight, Check, AlertTriangle, BookOpenCheck } from 'lucide-react';
import { COLORS } from '../../design/tokens';
import PrimaryActionButton from '../ui/PrimaryActionButton';
import { useCommandWordReflex } from '../../hooks/useCommandWordReflex';
import { COMMAND_WORD_QUESTIONS, commandSubjects, questionsForSubject } from '../../commandWordData';
import { type CommandWordQuestion } from '../../types/commandWord';
import SubjectTilePicker from '../shared/SubjectTilePicker';
import { baseName, displayName } from '../shared/subjectNames';
import { figureUrl } from '../../utils/figureUrl';

const INDIGO = '#6366F1';
const INDIGO_DARK_TEXT = '#3730A3';
const INDIGO_TINT = '#EEF0FF';
const HL_BG = '#FDE68A';        // amber-200 highlighter
const HL_TEXT = '#92400E';      // amber-800
const AMBER_TINT = '#FFFBEB';   // amber-50 (a tint, not warm cream)
const AMBER_ICON = '#D97706';   // amber-600

const cardShell =
  'w-full max-w-xl mx-auto rounded-2xl border-2 border-[#1A1A1A] dark:border-zinc-700 bg-white dark:bg-zinc-900 shadow-[4px_4px_0_0_#1A1A1A] dark:shadow-[4px_4px_0_0_#3f3f46] p-6 md:p-7';

const norm = (s: string) => s.replace(/[^a-zA-Z]/g, '').toLowerCase();

const fade = { initial: { opacity: 0, y: 10 }, animate: { opacity: 1, y: 0 }, exit: { opacity: 0, y: -8 }, transition: { duration: 0.22 } };

const CommandWordReflex: React.FC<{ uid?: string; studentSubjects?: string[]; studentCycle?: 'junior-cycle' | 'leaving-cert' }> = ({ uid, studentSubjects, studentCycle }) => {
  const { state, isLoaded, recordResult } = useCommandWordReflex(uid);

  const [view, setView] = useState<'home' | 'play'>('home');
  const [subjectId, setSubjectId] = useState<string | null>(null);
  const [qIndex, setQIndex] = useState(0);
  const [phase, setPhase] = useState<'spot' | 'reveal'>('spot');
  const [wrong, setWrong] = useState<Set<number>>(new Set());
  const [usedReveal, setUsedReveal] = useState(false);
  // Higher / Ordinary filter — a command-word question comes from a specific
  // level's paper; 'common' (if any) shows at both.
  const [levelFilter, setLevelFilter] = useState<'higher' | 'ordinary'>('higher');
  const atLevel = (q: CommandWordQuestion) => q.level === 'common' || q.level === levelFilter;
  // Subject-picker scope: just the student's chosen subjects, or every subject in their cycle.
  const [scope, setScope] = useState<'mine' | 'all'>('mine');

  // Subjects with at least one question at the selected level (count = visible),
  // filtered to the student's own cycle — JC students see only Junior Cycle
  // subjects, LC students only Leaving Cert. (No studentCycle → show all.)
  const subjects = useMemo(() => commandSubjects()
    .filter(s => !studentCycle || s.cycle === studentCycle)
    .map(s => ({ ...s, count: questionsForSubject(s.subjectId).filter(q => q.level === 'common' || q.level === levelFilter).length }))
    .filter(s => s.count > 0), [levelFilter, studentCycle]);
  const studentSet = useMemo(() => new Set((studentSubjects ?? []).map(baseName)), [studentSubjects]);
  const comingSoon = useMemo(
    () => (studentSubjects ?? []).filter(name => !subjects.some(s => baseName(s.subjectLabel) === baseName(name))),
    [studentSubjects, subjects],
  );

  const queue = subjectId ? questionsForSubject(subjectId).filter(atLevel) : [];
  const q: CommandWordQuestion | undefined = queue[qIndex];

  const tokens = useMemo(() => (q ? q.stem.split(/(\s+)/) : []), [q]);

  // Token indices that make up the command word — supports MULTI-WORD cues
  // ("Account for", "To what extent", "Show that", "Distinguish between"), which
  // a single-token match could never catch. Marks every matching run, so any
  // word of the cue is tappable and single-word cues keep working unchanged.
  const cmdIndices = useMemo(() => {
    const set = new Set<number>();
    if (!q) return set;
    const cmdWords = q.commandWord.toLowerCase().split(/\s+/).map(w => w.replace(/[^a-z]/g, '')).filter(Boolean);
    if (cmdWords.length === 0) return set;
    const wordPos = tokens.map((t, i) => (/^\s+$/.test(t) ? -1 : i)).filter(i => i >= 0);
    for (let p = 0; p + cmdWords.length <= wordPos.length; p++) {
      let ok = true;
      for (let k = 0; k < cmdWords.length; k++) {
        if (norm(tokens[wordPos[p + k]]) !== cmdWords[k]) { ok = false; break; }
      }
      if (ok) for (let k = 0; k < cmdWords.length; k++) set.add(wordPos[p + k]);
    }
    return set;
  }, [q, tokens]);

  const startSubject = (sid: string) => { setSubjectId(sid); setQIndex(0); resetQuestion(); setView('play'); };
  const resetQuestion = () => { setPhase('spot'); setWrong(new Set()); setUsedReveal(false); };

  const solve = (firstTry: boolean) => {
    if (!q) return;
    setPhase('reveal');
    recordResult(q.id, q.commandWord, firstTry);
  };

  const onTapToken = (i: number) => {
    if (!q || phase === 'reveal') return;
    if (cmdIndices.has(i)) {
      solve(wrong.size === 0 && !usedReveal);
    } else {
      setWrong(prev => new Set(prev).add(i));
    }
  };

  const reveal = () => { setUsedReveal(true); solve(false); };
  const next = () => {
    if (qIndex + 1 < queue.length) { setQIndex(qIndex + 1); resetQuestion(); }
    else setView('home');
  };

  if (!isLoaded) {
    return <div className="w-full max-w-xl mx-auto py-16 text-center text-sm text-zinc-400">Loading…</div>;
  }

  // ───────── HOME ─────────
  if (view === 'home') {
    const totalQs = COMMAND_WORD_QUESTIONS.length;
    // Picker inputs: cycle/level-filtered subjects sorted by display label, with
    // the question count in the sublabel; mineIds drives the My/All toggle.
    const sortedSubjects = subjects
      .slice()
      .sort((a, b) => displayName(a.subjectLabel).localeCompare(displayName(b.subjectLabel)));
    const pickerSubjects = sortedSubjects.map(s => ({
      id: s.subjectId,
      label: displayName(s.subjectLabel),
      sublabel: `${s.count} real ${s.count === 1 ? 'question' : 'questions'}`,
    }));
    const mineIds = sortedSubjects.filter(s => studentSet.has(baseName(s.subjectLabel))).map(s => s.subjectId);
    return (
      <div className="w-full max-w-xl mx-auto pb-12">
        <p className="text-[15px] leading-relaxed mb-5" style={{ color: '#5a5550', fontFamily: "'DM Sans', sans-serif" }}>
          Half of exam technique is reading the question right. Pick a subject, find the command word in real questions,
          and learn exactly what each one is telling you to do — and the trap that loses marks.
        </p>

        {/* Higher / Ordinary level filter */}
        <div className="flex items-center gap-2.5 mb-5">
          <span className="text-[11px] font-bold uppercase tracking-[0.12em]" style={{ color: '#9e9186' }}>Your level</span>
          <div className="flex items-center gap-1 p-1 rounded-xl bg-zinc-100 dark:bg-zinc-800/50">
            {(['higher', 'ordinary'] as const).map(lv => (
              <button
                key={lv}
                onClick={() => setLevelFilter(lv)}
                className={`px-4 py-1.5 rounded-lg text-[13px] transition-all ${levelFilter === lv ? 'bg-white dark:bg-zinc-800 text-zinc-900 dark:text-white font-semibold shadow-sm' : 'text-zinc-500 dark:text-zinc-400'}`}
              >
                {lv === 'higher' ? 'Higher' : 'Ordinary'}
              </button>
            ))}
          </div>
        </div>

        {state.wordsMet.length > 0 && (
          <div className="rounded-2xl p-5 mb-6" style={{ backgroundColor: INDIGO_TINT }}>
            <div className="flex items-baseline justify-between mb-2">
              <span className="text-[11px] font-bold uppercase tracking-[0.14em]" style={{ color: INDIGO_DARK_TEXT }}>Your reflex</span>
              <span className="text-[11px] font-semibold" style={{ color: INDIGO_DARK_TEXT }}>{state.firstTryIds.length}/{state.seenIds.length} spotted first try</span>
            </div>
            <p className="text-2xl font-semibold" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>
              {state.wordsMet.length} command {state.wordsMet.length === 1 ? 'word' : 'words'} met
            </p>
            <div className="h-2.5 rounded-full overflow-hidden mt-3" style={{ backgroundColor: '#ffffff' }}>
              <div className="h-full rounded-full transition-all" style={{ width: `${Math.round((state.seenIds.length / totalQs) * 100)}%`, backgroundColor: INDIGO }} />
            </div>
          </div>
        )}

        {/* My / All toggle (only when the student has subjects with content in
            this cycle) + subject tiles in the exact year-selection card style. */}
        <SubjectTilePicker
          headingLabel="Pick a subject"
          subjects={pickerSubjects}
          mineIds={mineIds}
          scope={scope}
          onScopeChange={setScope}
          onPick={startSubject}
        />
        {comingSoon.length > 0 && (
          <p className="text-[12px] leading-relaxed mt-5" style={{ color: '#9e9186' }}>More of your subjects are coming — we’re adding them subject by subject.</p>
        )}
      </div>
    );
  }

  // ───────── PLAY ─────────
  if (view === 'play' && q) {
    return (
      <div className="w-full">
        <button onClick={() => setView('home')} className="flex items-center gap-1.5 text-[13px] font-medium text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200 mb-4 max-w-xl mx-auto w-full">
          <ArrowLeft size={15} /> {q.subjectLabel}
        </button>

        <AnimatePresence mode="wait">
          <MotionDiv key={`${q.id}-${phase}`} {...fade} className={cardShell}>
            <div className="flex items-center justify-between mb-4">
              <span className="text-[11px] font-bold uppercase tracking-[0.14em]" style={{ color: INDIGO_DARK_TEXT }}>{q.questionRef}</span>
              <span className="text-[11px] font-medium text-zinc-400">{qIndex + 1} / {queue.length}</span>
            </div>

            {/* Figure for figure-attached questions — the real SEC graph/diagram
                the cue depends on, shown above the tappable stem, with attribution. */}
            {q.figure && (
              <figure className="mb-4 rounded-xl border-2 border-[#1A1A1A] dark:border-zinc-700 overflow-hidden bg-white">
                <img src={figureUrl(q.figure.src)} alt={q.figure.alt} loading="lazy" className="w-full h-auto block" />
                <figcaption className="text-[10px] px-3 py-1.5" style={{ color: INDIGO_DARK_TEXT, backgroundColor: INDIGO_TINT }}>{q.figure.source}</figcaption>
              </figure>
            )}

            {phase === 'spot' && (
              <p className="text-[12px] font-semibold mb-3" style={{ color: INDIGO_DARK_TEXT }}>
                Tap the command word — the cue telling you what to actually <span className="italic">do</span>.
              </p>
            )}

            {/* The question stem as tappable tokens */}
            <p className="text-[18px] leading-[1.7] mb-5" style={{ color: '#1a1a1a', fontFamily: "'Source Serif 4', serif" }}>
              {tokens.map((tok, i) => {
                if (/^\s+$/.test(tok)) return <span key={i}>{tok}</span>;
                const isCmd = cmdIndices.has(i);
                const isWrong = wrong.has(i);
                if (phase === 'reveal' && isCmd) {
                  return <span key={i} className="rounded px-1 py-0.5 font-semibold" style={{ backgroundColor: HL_BG, color: HL_TEXT }}>{tok}</span>;
                }
                return (
                  <button
                    key={i}
                    onClick={() => onTapToken(i)}
                    disabled={phase === 'reveal'}
                    className="rounded transition-colors"
                    style={isWrong
                      ? { textDecoration: 'line-through', color: '#b0a898', cursor: phase === 'reveal' ? 'default' : 'pointer' }
                      : { color: 'inherit', cursor: phase === 'reveal' ? 'default' : 'pointer' }}
                    onMouseEnter={(e) => { if (phase === 'spot') e.currentTarget.style.backgroundColor = INDIGO_TINT; }}
                    onMouseLeave={(e) => { e.currentTarget.style.backgroundColor = 'transparent'; }}
                  >{tok}</button>
                );
              })}
            </p>

            {phase === 'spot' && (
              <>
                {wrong.size > 0 && (
                  <p className="text-[12px] mb-3" style={{ color: '#9e9186' }}>That’s a topic word — look for the <span className="font-semibold">action</span> word (the verb telling you what to produce).</p>
                )}
                <div className="flex justify-end">
                  <button onClick={reveal} className="text-[13px] font-medium text-zinc-400 hover:text-zinc-700 underline">Reveal it</button>
                </div>
              </>
            )}

            {phase === 'reveal' && (
              <>
                <div className="flex items-center gap-1.5 mb-3">
                  <Check size={16} strokeWidth={3} style={{ color: COLORS.success }} />
                  <span className="text-[12px] font-semibold" style={{ color: COLORS.successDarkText }}>
                    {usedReveal ? `The command word is “${q.commandWord}”` : wrong.size === 0 ? 'Spotted it first try' : `Got it — it’s “${q.commandWord}”`}
                  </span>
                </div>

                {/* What it demands */}
                <div className="rounded-xl p-4 mb-3" style={{ backgroundColor: INDIGO_TINT }}>
                  <p className="text-[11px] font-bold uppercase tracking-[0.12em] mb-1.5" style={{ color: INDIGO_DARK_TEXT }}>What “{q.commandWord}” is asking you to do</p>
                  <p className="text-[14px] leading-relaxed" style={{ color: '#2a2622' }}>{q.demand}</p>
                </div>

                {/* The trap */}
                <div className="rounded-xl p-4 mb-3" style={{ backgroundColor: AMBER_TINT }}>
                  <div className="flex items-center gap-2 mb-1.5">
                    <AlertTriangle size={15} style={{ color: AMBER_ICON }} />
                    <p className="text-[11px] font-bold uppercase tracking-[0.12em]" style={{ color: '#92400E' }}>The trap</p>
                  </div>
                  <p className="text-[14px] leading-relaxed mb-2" style={{ color: '#3a3530' }}>{q.trap}</p>
                  <p className="text-[11px]" style={{ color: '#9e9186' }}>{q.source} · ~{q.marks} marks at stake</p>
                </div>

                <div className="flex justify-end">
                  <PrimaryActionButton label={qIndex + 1 < queue.length ? 'Next question' : 'Finish'} icon={qIndex + 1 < queue.length ? ArrowRight : BookOpenCheck} onClick={next} />
                </div>
              </>
            )}
          </MotionDiv>
        </AnimatePresence>
      </div>
    );
  }

  return null;
};

export default CommandWordReflex;
