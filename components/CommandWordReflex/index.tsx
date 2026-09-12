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

import ToolMasthead from '../launchpad/ToolMasthead';
import SubjectPicker from '../launchpad/SubjectPicker';
import React, { useMemo, useState } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from '../Motion';
import { ArrowLeft, ArrowRight, Check, BookOpenCheck } from 'lucide-react';
import { COLORS } from '../../design/tokens';
import PrimaryActionButton from '../ui/PrimaryActionButton';
import HorizontalTabs from '../ui/HorizontalTabs';
import { useCommandWordReflex } from '../../hooks/useCommandWordReflex';
import { commandSubjects, questionsForSubject } from '../../commandWordData';
import { type CommandWordQuestion } from '../../types/commandWord';

import { baseName, displayName } from '../shared/subjectNames';
import { figureUrl } from '../../utils/figureUrl';


const INDIGO_DARK_TEXT = 'var(--accent-text)';
const INDIGO_TINT = 'var(--surface-soft)';
const HL_BG = '#F26B1F';        // amber-200 highlighter
const HL_TEXT = '#1a1a1a';      // amber-800

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


  // Subjects with at least one question at the selected level (count = visible),
  // filtered to the student's own cycle — JC students see only Junior Cycle
  // subjects, LC students only Leaving Cert. (No studentCycle → show all.)
  const subjects = useMemo(() => commandSubjects()
    .filter(s => !studentCycle || s.cycle === studentCycle)
    .map(s => ({ ...s, count: questionsForSubject(s.subjectId).filter(q => q.level === 'common' || q.level === levelFilter).length }))
    .filter(s => s.count > 0), [levelFilter, studentCycle]);
  const studentSet = useMemo(() => new Set((studentSubjects ?? []).map(baseName)), [studentSubjects]);


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
    const selectedSubject = sortedSubjects.find(s => s.subjectId === subjectId) ?? sortedSubjects.find(s => mineIds.includes(s.subjectId)) ?? sortedSubjects[0];
    const previewQuestion = selectedSubject ? questionsForSubject(selectedSubject.subjectId).filter(atLevel)[0] : undefined;
    const preview = <div className="lp-reflex-example"><p className="lp-eyebrow">Try the idea · {previewQuestion?.subjectLabel}</p><p className="lp-reflex-stem">{previewQuestion?.stem}</p><p className="lp-body mt-4">Spot the command word. It tells you what the answer needs to do.</p></div>;
    return <div className="pb-12">
      <ToolMasthead tool="command-word-reflex" eyebrow="Read the question right" title="Command-Word Reflex." subtitle="Spot the word. Know what the examiner is asking." />
      <div className="lp-reflex-entry">
        {previewQuestion && <div className="lp-reflex-desktop">{preview}</div>}
        <section><h2 className="lp-title">Choose your subject</h2>
          <HorizontalTabs variant="pill" size="sm" label="Question level" value={levelFilter} onChange={next => setLevelFilter(next as typeof levelFilter)} options={[{value:'higher',label:'Higher'},{value:'ordinary',label:'Ordinary'}]} />
          <div className="lp-reflex-subjects">{(mineIds.length ? sortedSubjects.filter(s => mineIds.includes(s.subjectId)) : sortedSubjects.slice(0,6)).map(s => <button key={s.subjectId} aria-pressed={selectedSubject?.subjectId === s.subjectId} onClick={() => setSubjectId(s.subjectId)}><strong>{displayName(s.subjectLabel)}</strong><small>{s.count} questions</small></button>)}</div>
          <SubjectPicker label="All subjects" value={selectedSubject?.subjectId ?? ''} options={pickerSubjects.map(s => ({value:s.id,label:s.label,detail:s.sublabel}))} onChange={setSubjectId} />
          <button className="lp-button w-full mt-4" disabled={!selectedSubject} onClick={() => selectedSubject && startSubject(selectedSubject.subjectId)}>Start practising <ArrowRight size={17} /></button>
          {state.wordsMet.length > 0 && <p className="lp-body mt-4">{state.wordsMet.length} command words met · {state.firstTryIds.length}/{state.seenIds.length} spotted first try</p>}
          {previewQuestion && <details className="lp-reflex-mobile mt-6"><summary className="text-sm font-semibold">See an example</summary>{preview}</details>}
        </section>
      </div>
    </div>;
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

                {/* One editorial teaching surface. The old version used two
                    stacked pastel callouts and a stock warning icon, which made
                    grounded examiner guidance look like generic AI output. */}
                <section className="mb-4 overflow-hidden rounded-2xl border-[1.5px] border-[var(--outline-strong)] bg-[var(--surface-paper)] shadow-[3px_3px_0_0_var(--outline-strong)]">
                  <header className="px-5 py-4 border-b border-[var(--outline-soft)]">
                    <p className="font-mono text-[10px] font-bold uppercase tracking-[0.2em] text-[#F26B1F] mb-1">
                      Read it like an examiner
                    </p>
                    <h3 className="font-serif text-[22px] leading-tight font-semibold text-[var(--ink-primary)]">
                      “{q.commandWord}” is an instruction, not a label.
                    </h3>
                  </header>

                  <div className="grid md:grid-cols-2">
                    <div className="px-5 py-5 md:border-r border-[var(--outline-soft)]">
                      <div className="flex items-center gap-3 mb-3">
                        <span className="font-mono text-[11px] font-bold text-[#F26B1F]">01</span>
                        <span className="h-px w-8 bg-[#F26B1F]" aria-hidden="true" />
                        <p className="font-mono text-[10px] font-bold uppercase tracking-[0.18em] text-[var(--ink-muted)]">The move</p>
                      </div>
                      <p className="text-[14px] leading-relaxed text-[var(--ink-primary)]">{q.demand}</p>
                    </div>

                    <div className="px-5 py-5 border-t md:border-t-0 border-[var(--outline-soft)]">
                      <div className="flex items-center gap-3 mb-3">
                        <span className="font-mono text-[11px] font-bold text-[#F26B1F]">02</span>
                        <span className="h-px w-8 bg-[#F26B1F]" aria-hidden="true" />
                        <p className="font-mono text-[10px] font-bold uppercase tracking-[0.18em] text-[var(--ink-muted)]">Where marks go</p>
                      </div>
                      <p className="text-[14px] leading-relaxed text-[var(--ink-primary)]">{q.trap}</p>
                    </div>
                  </div>

                  <footer className="px-5 py-3 border-t border-[var(--outline-soft)] flex flex-wrap items-center justify-between gap-2">
                    <p className="text-[11px] leading-relaxed text-[var(--ink-muted)]">{q.source}</p>
                    <p className="font-mono text-[10px] font-bold uppercase tracking-[0.12em] text-[#F26B1F]">About {q.marks} marks in play</p>
                  </footer>
                </section>

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
