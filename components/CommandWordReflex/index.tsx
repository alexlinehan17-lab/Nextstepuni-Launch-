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
 * Look (area 7b, boards c-tools2-command and r5-command-word-reflex): a real exam question
 * with its command word leads the opening; subjects carry their characters, bare; a round is
 * a task with Reveal it and Next question pinned; the found word fills charcoal and the
 * examiner's two-part answer opens on the same surface. The mechanics are unchanged.
 */

import SubjectPicker from '../launchpad/SubjectPicker';
import LockedButton from '../ui/LockedButton';
import React, { useMemo, useState } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from '../Motion';
import { Check, LockKeyhole } from 'lucide-react';
import { Button } from '../ui/Button';
import { SelectionBar } from '../ui/Choice';
import { PinnedFooter } from '../ui/Bars';
import { useFrameTask } from '../ui/Frame';
import SubjectAvatar from '../SubjectAvatar';
import { useBackStep } from '../../contexts/NavigationContext';
import './command-word-7.css';
import { useCommandWordReflex } from '../../hooks/useCommandWordReflex';
import { commandSubjects, questionsForSubject } from '../../commandWordData';
import { type CommandWordQuestion } from '../../types/commandWord';

import { useSubjectAccess } from '../launchpad/SubjectAccess';
import { baseName, displayName } from '../shared/subjectNames';
import { figureUrl } from '../../utils/figureUrl';


const norm = (s: string) => s.replace(/[^a-zA-Z]/g, '').toLowerCase();

const fade = { initial: { opacity: 0, y: 10 }, animate: { opacity: 1, y: 0 }, exit: { opacity: 0, y: -8 }, transition: { duration: 0.22 } };

const CommandWordReflex: React.FC<{ uid?: string; studentSubjects?: string[]; studentCycle?: 'junior-cycle' | 'leaving-cert' }> = ({ uid, studentSubjects, studentCycle }) => {
  const canSelectSubject = useSubjectAccess();
  const { state, isLoaded, recordResult } = useCommandWordReflex(uid);

  const [view, setView] = useState<'home' | 'play'>('home');
  const [subjectId, setSubjectId] = useState<string | null>(null);
  const [qIndex, setQIndex] = useState(0);
  const [phase, setPhase] = useState<'spot' | 'reveal'>('spot');
  const [wrong, setWrong] = useState<Set<number>>(new Set());
  const [usedReveal, setUsedReveal] = useState(false);
  // A round is a task on a phone: Reveal it and Next question are pinned and the tab bar steps aside;
  // the bar's one Back returns to the subjects (board c-tools2-command: one way back, in the bar).
  useFrameTask(view === 'play');
  useBackStep(view === 'play', () => setView('home'));
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

  const startSubject = (sid: string) => { const selected = subjects.find(s => s.subjectId === sid); if (!selected || !canSelectSubject(displayName(selected.subjectLabel))) return; setSubjectId(sid); setQIndex(0); resetQuestion(); setView('play'); };
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
    return <div className="cr7"><p className="t-sub cr7-loading">Loading…</p></div>;
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
    const accessibleSubjects = sortedSubjects.filter(s => canSelectSubject(displayName(s.subjectLabel)));
    const selectedSubject = accessibleSubjects.find(s => s.subjectId === subjectId) ?? accessibleSubjects.find(s => mineIds.includes(s.subjectId)) ?? accessibleSubjects[0];
    const previewQuestion = selectedSubject ? questionsForSubject(selectedSubject.subjectId).filter(atLevel)[0] : undefined;
    const shown = mineIds.length ? sortedSubjects.filter(s => mineIds.includes(s.subjectId)) : sortedSubjects.slice(0, 6);
    return <div className="cr7 cr7-home">
      {previewQuestion && <section className="cr7-idea" aria-label="Try the idea">
        <p className="t-label">Try the idea · {ideaLabel(previewQuestion)}</p>
        {/* The example question leads (board c-tools2-command): on a phone the sentence that holds the
            command word, on a laptop the whole question; the command word is marked in both. */}
        <h2 className="t-title cr7-example cr7-example--short">{markCommand(commandSentence(previewQuestion), previewQuestion.commandWord)}</h2>
        <h2 className="cr7-example cr7-example--full">{markCommand(previewQuestion.stem, previewQuestion.commandWord)}</h2>
        <p className="t-sub">Half of exam technique is reading the question right. Spot the command word, and the trap that loses marks.</p>
      </section>}
      <section className="cr7-pick" aria-label="Choose your subject">
        <div className="cr7-pick-head"><h3 className="t-heading">Choose your subject</h3><SubjectPicker link label="All subjects" value={selectedSubject?.subjectId ?? ''} options={pickerSubjects.map(s => ({value:s.id,label:s.label,detail:s.sublabel}))} onChange={setSubjectId} /></div>
        <SelectionBar label="Question level" size="md" value={levelFilter} onChange={next => setLevelFilter(next)} options={[{value:'higher',label:'Higher'},{value:'ordinary',label:'Ordinary'}]} />
        <div className="cr7-subjects">{shown.map(s => {
          const locked = !canSelectSubject(displayName(s.subjectLabel));
          return <LockedButton key={s.subjectId} className="ui-part ui-press cr7-subject" locked={locked} aria-pressed={selectedSubject?.subjectId === s.subjectId} onClick={() => setSubjectId(s.subjectId)}>
            <span className="cr7-subject-art" aria-hidden="true"><SubjectAvatar subject={displayName(s.subjectLabel)} bare /></span>
            <span className="cr7-subject-copy"><span className="cr7-subject-name">{displayName(s.subjectLabel)}</span><span className="t-meta">{locked ? <><LockKeyhole size={12} aria-hidden="true" /> Available in the app</> : `${s.count} questions`}</span></span>
          </LockedButton>;
        })}</div>
        <Button kind="main" size="lg" block arrow="forward" className="cr7-start" {...(selectedSubject ? {} : { 'aria-disabled': true as const })} onClick={() => selectedSubject && startSubject(selectedSubject.subjectId)}>Start practising</Button>
        {state.wordsMet.length > 0 && <p className="t-meta">{state.wordsMet.length} command words met · <span className="ui-readout">{state.firstTryIds.length} / {state.seenIds.length}</span> spotted first try</p>}
      </section>
    </div>;
  }

  // ───────── PLAY ─────────
  if (view === 'play' && q) {
    const last = qIndex + 1 >= queue.length;
    return (
      <div className="cr7 cr7-play" data-phase={phase}>
        <div className="cr7-play-head">
          <div className="cr7-ref"><span className="t-label">{q.subjectLabel} · {q.questionRef}</span><span className="ui-readout">{qIndex + 1} / {queue.length}</span></div>
          <div className="cr7-steps" aria-hidden="true">{queue.map((item, index) => <i key={item.id} data-state={index < qIndex ? 'done' : index === qIndex ? 'now' : undefined} />)}</div>
        </div>

        <AnimatePresence mode="wait">
          <MotionDiv key={`${q.id}-${phase}`} {...fade} className="cr7-card">
            {/* Figure for figure-attached questions — the real SEC graph/diagram
                the cue depends on, shown above the tappable stem, with attribution. */}
            {q.figure && (
              <figure className="cr7-figure">
                <img src={figureUrl(q.figure.src)} alt={q.figure.alt} loading="lazy" />
                <figcaption className="t-meta">{q.figure.source}</figcaption>
              </figure>
            )}

            {phase === 'spot' && (
              <p className="t-sub">Tap the command word: the cue telling you what to actually do.</p>
            )}

            {/* The question stem as tappable tokens */}
            <p className="cr7-stem">
              {tokens.map((tok, i) => {
                if (/^\s+$/.test(tok)) return <span key={i}>{tok}</span>;
                const isCmd = cmdIndices.has(i);
                const isWrong = wrong.has(i);
                if (phase === 'reveal' && isCmd) {
                  return <span key={i} className="cr7-hit">{tok}</span>;
                }
                return (
                  <button
                    key={i}
                    onClick={() => onTapToken(i)}
                    disabled={phase === 'reveal'}
                    className="cr7-word"
                    data-wrong={isWrong || undefined}
                  >{tok}</button>
                );
              })}
            </p>

            {phase === 'spot' && wrong.size > 0 && (
              <p className="t-sub">That’s a topic word. Look for the action word, the verb telling you what to produce.</p>
            )}

            {phase === 'reveal' && (
              <section className="cr7-reveal" aria-label="Read it like an examiner">
                <p className="cr7-got"><Check size={16} strokeWidth={2} aria-hidden="true" /><span>
                  {usedReveal ? `The command word is “${q.commandWord}”` : wrong.size === 0 ? 'Spotted it first try' : `Got it — it’s “${q.commandWord}”`}
                </span></p>
                <div className="cr7-examiner"><p className="t-label">Read it like an examiner</p><h3 className="t-heading">“{q.commandWord}” is an instruction, not a label.</h3></div>
                <div className="cr7-part"><div className="cr7-motif"><b className="ui-readout">01</b><i aria-hidden="true" /><span className="t-label">The move</span></div><p className="t-body">{q.demand}</p></div>
                <div className="cr7-part"><div className="cr7-motif"><b className="ui-readout">02</b><i aria-hidden="true" /><span className="t-label">Where marks go</span></div><p className="t-body">{q.trap}</p></div>
                <p className="t-meta">{q.source}</p>
                <p className="t-label cr7-marks">About {q.marks} marks in play</p>
              </section>
            )}
          </MotionDiv>
        </AnimatePresence>

        <div className="cr7-foot-wrap frame-float frame-float-bottom">
          <PinnedFooter className="cr7-foot">
            {phase === 'spot'
              ? <Button size="lg" block onClick={reveal}>Reveal it</Button>
              : <Button kind="main" size="lg" block arrow="forward" onClick={next}>{last ? 'Finish' : 'Next question'}</Button>}
          </PinnedFooter>
        </div>
      </div>
    );
  }

  return null;
};

/** The opening's label: "Accounting 2025, Higher" where the reference starts with a year and a level
 *  (board c-tools2-command), the subject alone otherwise. */
const ideaLabel = (q: CommandWordQuestion) => {
  const sat = /^(\d{4})\s+(HL|OL)\b/.exec(q.questionRef);
  return sat ? `${q.subjectLabel} ${sat[1]}, ${sat[2] === 'HL' ? 'Higher' : 'Ordinary'}` : q.subjectLabel;
};

/** The sentence of the stem that holds the command word ("Outline the benefits of maintaining a
 *  debtors control account."): the phone's headline. The whole stem when it cannot be found. */
const commandSentence = (q: CommandWordQuestion) => {
  const at = q.stem.toLowerCase().indexOf(q.commandWord.toLowerCase());
  if (at < 0) return q.stem;
  const before = q.stem.slice(0, at);
  const start = Math.max(before.lastIndexOf('. '), before.lastIndexOf('? '), before.lastIndexOf('! '), before.lastIndexOf(': '));
  const from = start < 0 ? 0 : start + 2;
  const rest = q.stem.slice(at);
  const stop = rest.search(/[.?!](\s|$)/);
  return q.stem.slice(from, stop < 0 ? undefined : at + stop + 1).trim();
};

/** The text with the command word marked (an ink underline), as the boards draw it. */
const markCommand = (text: string, commandWord: string) => {
  const at = text.toLowerCase().indexOf(commandWord.toLowerCase());
  if (at < 0) return text;
  return <>{text.slice(0, at)}<span className="cr7-cmd">{text.slice(at, at + commandWord.length)}</span>{text.slice(at + commandWord.length)}</>;
};

export default CommandWordReflex;
