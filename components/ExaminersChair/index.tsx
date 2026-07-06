/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair (Launchpad tool) — students sit on the other side of the
 * desk. Each session: an exam-style question, the REAL SEC marking rules that
 * govern it (cited), and authored sample "scripts" to mark against those rules.
 * After each script the examiner's key is revealed decision-by-decision, and a
 * running calibration score tracks how closely the student's marking matches
 * the examiner's. Completed sessions earn a transferable "Marker's Codex" rule,
 * which can be pushed into the Paper Trail review deck as a flashcard.
 *
 * Content: data/examinersChair/* (authored, every rule cited to SEC documents —
 * see compliance/evidence/examiners-chair.md). Scoring: ./store.ts (tested).
 */

import React, { useMemo, useState } from 'react';
import { ArrowLeft, BookMarked, Check, ChevronRight, Scale, Stamp, X } from 'lucide-react';
import {
  CHAIR_SUBJECTS,
  allSessions,
  type GridSession,
  type MarkingSession,
  type ScaleSession,
} from '../../data/examinersChair';
import {
  calibrationBand,
  completeSession,
  gridDecisionKey,
  loadChair,
  markCodexOnCards,
  overallCalibration,
  pct,
  saveChair,
  scoreGridScript,
  scoreScaleScript,
  type ChairState,
  type ScriptScore,
} from './store';
import { createCard } from '../PaperTrail/flashcardStore';

const INK = '#1a1a1a';
const ACCENT = '#F26B1F';
const SUCCESS = '#3A8D5F';
const MUTED = '#7a7068';
const LABEL = '#9e9186';
const BORDER_MUTED = '#d0cdc8';

const SERIF = "'Source Serif 4', serif";

const FLASHCARD_SUBJECT: Record<string, string> = { business: 'business', maths: 'mathematics' };

type Stage = 'intro' | 'mark' | 'reveal' | 'summary';

interface Props {
  uid?: string;
}

// ── small shared bits ──

const SectionLabel: React.FC<{ children: React.ReactNode; className?: string }> = ({ children, className }) => (
  <p className={`text-[10.5px] font-bold uppercase tracking-[0.12em] ${className ?? ''}`} style={{ color: LABEL }}>
    {children}
  </p>
);

const CiteLine: React.FC<{ label: string }> = ({ label }) => (
  <p className="text-[11px] mt-2 italic" style={{ color: LABEL }}>
    Source: {label}
  </p>
);

/** The exam-script card: authored candidate work, styled as a script. */
const ScriptPaper: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div
    className="rounded-xl border-2 px-4 py-3.5"
    style={{ borderColor: BORDER_MUTED, backgroundColor: '#FCFBF8' }}
  >
    {children}
  </div>
);

const agreementColor = (a: number) => (a >= 0.75 ? SUCCESS : a >= 0.5 ? ACCENT : '#9e9186');

// ═══════════════════════════════ main component ═══════════════════════════════

const ExaminersChair: React.FC<Props> = ({ uid }) => {
  const [state, setState] = useState<ChairState>(() => loadChair(uid));
  const [view, setView] = useState<'home' | 'codex' | 'session'>('home');
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [stage, setStage] = useState<Stage>('intro');
  const [scriptIdx, setScriptIdx] = useState(0);
  // grid decisions for the CURRENT script only, keyed attemptId:criterionId
  const [decisions, setDecisions] = useState<Record<string, boolean>>({});
  // scale choice for the current script
  const [chosenLevel, setChosenLevel] = useState<string | null>(null);
  // accumulated scores for the session in progress
  const [scores, setScores] = useState<ScriptScore[]>([]);
  const [codexAdded, setCodexAdded] = useState(false);

  const session: MarkingSession | undefined = useMemo(
    () => (sessionId ? allSessions().find(s => s.id === sessionId) : undefined),
    [sessionId],
  );

  const persist = (next: ChairState) => {
    setState(next);
    saveChair(uid, next);
  };

  const openSession = (id: string) => {
    setSessionId(id);
    setStage('intro');
    setScriptIdx(0);
    setDecisions({});
    setChosenLevel(null);
    setScores([]);
    setCodexAdded(false);
    setView('session');
  };

  const exitSession = () => {
    setView('home');
    setSessionId(null);
  };

  // ───────────────────────────── session flow ─────────────────────────────

  if (view === 'session' && session) {
    const scripts = session.scripts;
    const script = scripts[Math.min(scriptIdx, scripts.length - 1)];

    const commitScript = () => {
      const score =
        session.mode === 'grid'
          ? scoreGridScript(session, script as GridSession['scripts'][number], decisions)
          : scoreScaleScript(session, script as ScaleSession['scripts'][number], chosenLevel);
      setScores(prev => [...prev, score]);
      setStage('reveal');
    };

    const nextScript = () => {
      if (scriptIdx + 1 < scripts.length) {
        setScriptIdx(i => i + 1);
        setDecisions({});
        setChosenLevel(null);
        setStage('mark');
      } else {
        persist(completeSession(state, session, scores, Date.now()));
        setStage('summary');
      }
    };

    const currentScore = scores[scriptIdx];

    return (
      <div className="w-full max-w-xl mx-auto pb-12">
        <button onClick={exitSession} className="flex items-center gap-1.5 text-[13px] font-medium mb-4" style={{ color: MUTED }}>
          <ArrowLeft size={15} /> All sessions
        </button>
        <SectionLabel className="mb-1">
          {session.subject === 'business' ? 'Business' : 'Mathematics'} · cue: {session.cue}
        </SectionLabel>
        <h2 className="text-2xl font-semibold mb-4" style={{ fontFamily: SERIF, color: INK }}>
          {session.title}
        </h2>

        {/* ── intro: the question + the real rules ── */}
        {stage === 'intro' && (
          <>
            <div className="rounded-2xl border-2 border-[#1a1a1a] dark:border-zinc-700 bg-white dark:bg-zinc-900 shadow-[4px_4px_0_0_#1a1a1a] dark:shadow-[4px_4px_0_0_#3f3f46] px-5 py-5 mb-4">
              <SectionLabel className="mb-2">The question</SectionLabel>
              {'caseText' in session && session.caseText && (
                <p className="text-[13.5px] leading-relaxed mb-3 pb-3 border-b" style={{ color: '#3a3530', borderColor: BORDER_MUTED }}>
                  {session.caseText}
                </p>
              )}
              <p className="text-[15px] leading-relaxed font-medium" style={{ color: INK }}>
                {session.question}
              </p>
              <p className="text-[11.5px] mt-3 italic" style={{ color: LABEL }}>
                {session.questionNote}
              </p>
            </div>

            <div className="rounded-xl px-4 py-3.5 mb-4" style={{ backgroundColor: '#FDEEDF', borderLeft: `3px solid ${ACCENT}` }}>
              <SectionLabel className="mb-1.5">How the examiner marks this</SectionLabel>
              {session.mode === 'grid' ? (
                <>
                  <p className="text-[14px] font-semibold" style={{ fontFamily: SERIF, color: INK }}>
                    {session.grid.shorthand}
                  </p>
                  <div className="flex flex-wrap gap-1.5 my-2">
                    {session.grid.perPoint.map(c => (
                      <span key={c.id} className="text-[11px] font-semibold px-2 py-0.5 rounded-full bg-white" style={{ color: '#8C3A0E', border: '1px solid rgba(242,107,31,0.25)' }}>
                        {c.label} · {c.marks}m
                      </span>
                    ))}
                  </div>
                  <p className="text-[13px] italic leading-relaxed" style={{ color: '#8C3A0E' }}>{session.grid.ruleNote}</p>
                  <CiteLine label={session.grid.cite.label} />
                </>
              ) : (
                <>
                  <p className="text-[14px] font-semibold" style={{ fontFamily: SERIF, color: INK }}>
                    Scale {session.scale.name} — {session.scale.levels.map(l => l.marks).join(', ')}
                  </p>
                  <ul className="mt-2 space-y-1">
                    {session.scale.notes.map((n, i) => (
                      <li key={i} className="text-[13px] italic leading-relaxed" style={{ color: '#8C3A0E' }}>
                        {n}
                      </li>
                    ))}
                  </ul>
                  <CiteLine label={session.scale.cite.label} />
                </>
              )}
            </div>

            <button
              onClick={() => setStage('mark')}
              className="w-full rounded-full py-3 text-[15px] font-semibold text-white transition-transform active:translate-y-0.5"
              style={{ backgroundColor: ACCENT, borderBottom: '3px solid #B54D14', boxShadow: '0 4px 0 #B54D14' }}
            >
              Take the chair — mark {scripts.length} scripts
            </button>
          </>
        )}

        {/* ── mark / reveal ── */}
        {(stage === 'mark' || stage === 'reveal') && (
          <>
            <div className="flex items-center justify-between mb-2.5">
              <SectionLabel>
                Script {scriptIdx + 1} of {scripts.length} · {script.label}
              </SectionLabel>
              {stage === 'reveal' && currentScore && (
                <span className="text-[11.5px] font-bold" style={{ color: agreementColor(currentScore.agreement) }}>
                  {pct(currentScore.agreement)} agreement
                </span>
              )}
            </div>
            <p className="text-[12.5px] italic mb-3" style={{ color: MUTED }}>
              “{script.persona}”
            </p>

            {session.mode === 'grid' ? (
              <div className="space-y-3 mb-4">
                {(script as GridSession['scripts'][number]).attempts.map((attempt, ai) => (
                  <div key={attempt.id}>
                    <ScriptPaper>
                      {(script as GridSession['scripts'][number]).attempts.length > 1 && (
                        <SectionLabel className="mb-1">Point {ai + 1}</SectionLabel>
                      )}
                      <p className="text-[14px] leading-relaxed italic" style={{ fontFamily: SERIF, color: '#2a2620' }}>
                        {attempt.text}
                      </p>
                    </ScriptPaper>
                    <div className="flex flex-wrap gap-1.5 mt-2">
                      {session.grid.perPoint.map(c => {
                        const k = gridDecisionKey(attempt.id, c.id);
                        const awarded = !!decisions[k];
                        const keyAwarded = (attempt.key[c.id] ?? 0) > 0;
                        if (stage === 'mark') {
                          return (
                            <button
                              key={c.id}
                              onClick={() => setDecisions(d => ({ ...d, [k]: !d[k] }))}
                              className="text-[12px] font-semibold px-2.5 py-1.5 rounded-full border-2 transition-transform active:translate-y-0.5"
                              style={
                                awarded
                                  ? { backgroundColor: '#FDEEDF', borderColor: ACCENT, color: '#8C3A0E' }
                                  : { backgroundColor: '#fff', borderColor: BORDER_MUTED, color: MUTED }
                              }
                            >
                              {awarded ? '✓ ' : ''}
                              {c.label} · {c.marks}m
                            </button>
                          );
                        }
                        // reveal: agreement colouring
                        const match = awarded === keyAwarded;
                        return (
                          <span
                            key={c.id}
                            className="inline-flex items-center gap-1 text-[12px] font-semibold px-2.5 py-1.5 rounded-full border-2"
                            style={
                              match
                                ? { backgroundColor: '#E8F2EC', borderColor: SUCCESS, color: '#1F5F3E' }
                                : { backgroundColor: '#FDEEDF', borderColor: ACCENT, color: '#8C3A0E' }
                            }
                          >
                            {match ? <Check size={12} /> : <X size={12} />}
                            {c.label}: examiner {keyAwarded ? `${attempt.key[c.id]}m` : '0m'}
                          </span>
                        );
                      })}
                    </div>
                    {stage === 'reveal' && (
                      <p className="text-[12.5px] leading-relaxed mt-2 px-1" style={{ color: '#5a5550' }}>
                        {attempt.keyNote}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <div className="mb-4">
                <ScriptPaper>
                  <div className="space-y-1">
                    {(script as ScaleSession['scripts'][number]).work.map((line, i) => (
                      <p key={i} className="text-[14.5px] italic" style={{ fontFamily: SERIF, color: '#2a2620' }}>
                        {line}
                      </p>
                    ))}
                  </div>
                </ScriptPaper>
                <SectionLabel className="mt-3 mb-1.5">Where does this land on scale {session.scale.name}?</SectionLabel>
                <div className="flex flex-wrap gap-1.5">
                  {session.scale.levels.map(l => {
                    const isChoice = chosenLevel === l.id;
                    const isKey = (script as ScaleSession['scripts'][number]).keyLevelId === l.id;
                    if (stage === 'mark') {
                      return (
                        <button
                          key={l.id}
                          onClick={() => setChosenLevel(l.id)}
                          className="text-[12px] font-semibold px-2.5 py-1.5 rounded-full border-2 transition-transform active:translate-y-0.5"
                          style={
                            isChoice
                              ? { backgroundColor: '#FDEEDF', borderColor: ACCENT, color: '#8C3A0E' }
                              : { backgroundColor: '#fff', borderColor: BORDER_MUTED, color: MUTED }
                          }
                        >
                          {l.label} · {l.marks}m
                        </button>
                      );
                    }
                    return (
                      <span
                        key={l.id}
                        className="inline-flex items-center gap-1 text-[12px] font-semibold px-2.5 py-1.5 rounded-full border-2"
                        style={
                          isKey
                            ? { backgroundColor: '#E8F2EC', borderColor: SUCCESS, color: '#1F5F3E' }
                            : isChoice
                              ? { backgroundColor: '#FDEEDF', borderColor: ACCENT, color: '#8C3A0E' }
                              : { backgroundColor: '#fff', borderColor: BORDER_MUTED, color: '#b0a898' }
                        }
                      >
                        {isKey && <Check size={12} />}
                        {isChoice && !isKey && <X size={12} />}
                        {(isKey || isChoice) ? `${l.annotation} ` : ''}{l.label} · {l.marks}m
                      </span>
                    );
                  })}
                </div>
                {stage === 'reveal' && (
                  <p className="text-[12.5px] leading-relaxed mt-2 px-1" style={{ color: '#5a5550' }}>
                    {(script as ScaleSession['scripts'][number]).keyNote}
                  </p>
                )}
              </div>
            )}

            {stage === 'reveal' && script.embodies && (
              <div className="rounded-xl px-4 py-3 mb-4" style={{ backgroundColor: '#FDEEDF', borderLeft: `3px solid ${ACCENT}` }}>
                <SectionLabel className="mb-1">Documented pattern</SectionLabel>
                <p className="text-[13px] italic leading-relaxed" style={{ color: '#8C3A0E' }}>
                  {script.embodies.behaviour}
                </p>
                <CiteLine label={script.embodies.cite.label} />
              </div>
            )}

            {stage === 'mark' ? (
              <button
                onClick={commitScript}
                disabled={session.mode === 'scale' && chosenLevel === null}
                className="w-full rounded-full py-3 text-[15px] font-semibold text-white transition-transform active:translate-y-0.5 disabled:opacity-40"
                style={{ backgroundColor: ACCENT, borderBottom: '3px solid #B54D14', boxShadow: '0 4px 0 #B54D14' }}
              >
                Lock in your marks
              </button>
            ) : (
              <button
                onClick={nextScript}
                className="w-full inline-flex items-center justify-center gap-1.5 rounded-full py-3 text-[15px] font-semibold text-white transition-transform active:translate-y-0.5"
                style={{ backgroundColor: ACCENT, borderBottom: '3px solid #B54D14', boxShadow: '0 4px 0 #B54D14' }}
              >
                {scriptIdx + 1 < scripts.length ? (
                  <>
                    Next script <ChevronRight size={16} />
                  </>
                ) : (
                  'See your calibration'
                )}
              </button>
            )}
          </>
        )}

        {/* ── summary ── */}
        {stage === 'summary' && (
          <>
            {(() => {
              const agreement = scores.length ? scores.reduce((a, s) => a + s.agreement, 0) / scores.length : 0;
              return (
                <div className="rounded-2xl border-2 border-[#1a1a1a] dark:border-zinc-700 bg-white dark:bg-zinc-900 shadow-[4px_4px_0_0_#1a1a1a] dark:shadow-[4px_4px_0_0_#3f3f46] px-5 py-5 mb-4 text-center">
                  <SectionLabel className="mb-2">Your calibration this session</SectionLabel>
                  <p className="text-[44px] font-bold leading-none" style={{ fontFamily: SERIF, color: agreementColor(agreement) }}>
                    {pct(agreement)}
                  </p>
                  <p className="text-[13px] font-semibold mt-1.5" style={{ color: agreementColor(agreement) }}>
                    {calibrationBand(agreement)}
                  </p>
                  <div className="mt-3 space-y-1.5">
                    {scores.map((s, i) => (
                      <div key={s.scriptId} className="flex items-center gap-2">
                        <span className="text-[11px] w-14 text-left shrink-0" style={{ color: MUTED }}>
                          Script {String.fromCharCode(65 + i)}
                        </span>
                        <div className="flex-1 h-2 rounded-full" style={{ backgroundColor: '#e0dbd4' }}>
                          <div className="h-2 rounded-full" style={{ width: `${Math.round(s.agreement * 100)}%`, backgroundColor: agreementColor(s.agreement) }} />
                        </div>
                        <span className="text-[11px] w-20 text-right shrink-0" style={{ color: MUTED }}>
                          you {s.studentMarks}m · ex {s.examinerMarks}m
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              );
            })()}

            <div className="rounded-xl px-4 py-3.5 mb-4" style={{ backgroundColor: '#E8F2EC', borderLeft: `3px solid ${SUCCESS}` }}>
              <SectionLabel className="mb-1">Added to your Marker’s Codex</SectionLabel>
              <p className="text-[15px] font-semibold" style={{ fontFamily: SERIF, color: INK }}>
                {session.takeaway.rule}
              </p>
              <p className="text-[13px] italic leading-relaxed mt-1" style={{ color: '#1F5F3E' }}>
                {session.takeaway.detail}
              </p>
              <CiteLine label={session.takeaway.cite.label} />
              {!state.codexOnCards.includes(session.takeaway.id) && !codexAdded ? (
                <button
                  onClick={() => {
                    createCard(
                      uid,
                      `Marking rule (${session.subject === 'business' ? 'Business' : 'Maths'}): ${session.takeaway.rule}`,
                      session.takeaway.detail,
                      FLASHCARD_SUBJECT[session.subject],
                      Date.now(),
                    );
                    persist(markCodexOnCards(state, session.takeaway.id));
                    setCodexAdded(true);
                  }}
                  className="mt-2.5 text-[12.5px] font-semibold inline-flex items-center gap-1.5"
                  style={{ color: SUCCESS }}
                >
                  <BookMarked size={14} /> Add to my review deck
                </button>
              ) : (
                <p className="mt-2.5 text-[12px] inline-flex items-center gap-1.5 font-semibold" style={{ color: SUCCESS }}>
                  <Check size={13} /> In your review deck
                </p>
              )}
            </div>

            <button
              onClick={exitSession}
              className="w-full rounded-full py-3 text-[15px] font-semibold text-white transition-transform active:translate-y-0.5"
              style={{ backgroundColor: ACCENT, borderBottom: '3px solid #B54D14', boxShadow: '0 4px 0 #B54D14' }}
            >
              Back to the desk
            </button>
          </>
        )}
      </div>
    );
  }

  // ───────────────────────────── codex view ─────────────────────────────

  if (view === 'codex') {
    const earned = allSessions().filter(s => state.codex.includes(s.takeaway.id));
    return (
      <div className="w-full max-w-xl mx-auto pb-12">
        <button onClick={() => setView('home')} className="flex items-center gap-1.5 text-[13px] font-medium mb-4" style={{ color: MUTED }}>
          <ArrowLeft size={15} /> The desk
        </button>
        <h2 className="text-2xl font-semibold mb-1" style={{ fontFamily: SERIF, color: INK }}>
          Your Marker’s Codex
        </h2>
        <p className="text-[13px] mb-5" style={{ color: MUTED }}>
          Every rule you’ve earned by marking like the examiner. Each cites the SEC document it comes from.
        </p>
        {earned.length === 0 ? (
          <p className="text-[13.5px] italic" style={{ color: LABEL }}>
            Nothing here yet — complete a marking session to earn your first rule.
          </p>
        ) : (
          <div className="space-y-2.5">
            {earned.map(s => (
              <div key={s.takeaway.id} className="rounded-2xl border-2 border-[#1a1a1a] dark:border-zinc-700 bg-white dark:bg-zinc-900 px-4 py-3.5">
                <SectionLabel className="mb-1">{s.subject === 'business' ? 'Business' : 'Mathematics'}</SectionLabel>
                <p className="text-[15px] font-semibold" style={{ fontFamily: SERIF, color: INK }}>
                  {s.takeaway.rule}
                </p>
                <p className="text-[12.5px] leading-relaxed mt-1" style={{ color: '#5a5550' }}>
                  {s.takeaway.detail}
                </p>
                <CiteLine label={s.takeaway.cite.label} />
              </div>
            ))}
          </div>
        )}
      </div>
    );
  }

  // ───────────────────────────── home ─────────────────────────────

  const calibration = overallCalibration(state);
  const done = Object.keys(state.results).length;
  const total = allSessions().length;

  return (
    <div className="w-full max-w-xl mx-auto pb-12">
      <p className="text-[14px] leading-relaxed mb-4" style={{ color: '#5a5550' }}>
        The fastest way to stop losing marks is to learn how they’re awarded. Sit on the examiner’s side of the desk:
        mark sample answers against the real SEC marking rules, compare your decisions to the examiner’s, and build the
        judgement that tells you — mid-exam — exactly what your own answer is worth.
      </p>

      {/* calibration hero */}
      <div className="rounded-2xl border-2 border-[#1a1a1a] dark:border-zinc-700 bg-white dark:bg-zinc-900 shadow-[4px_4px_0_0_#1a1a1a] dark:shadow-[4px_4px_0_0_#3f3f46] px-5 py-4 mb-3 flex items-center justify-between gap-3">
        <div>
          <SectionLabel className="mb-1">Marking calibration</SectionLabel>
          {calibration === null ? (
            <p className="text-[13.5px] italic" style={{ color: MUTED }}>
              Mark your first scripts to find out how you judge.
            </p>
          ) : (
            <p className="text-[13px] font-semibold" style={{ color: agreementColor(calibration) }}>
              {calibrationBand(calibration)} · {done}/{total} sessions
            </p>
          )}
        </div>
        <div className="flex items-center gap-3 shrink-0">
          {calibration !== null && (
            <span className="text-[34px] font-bold leading-none" style={{ fontFamily: SERIF, color: agreementColor(calibration) }}>
              {pct(calibration)}
            </span>
          )}
          <button
            onClick={() => setView('codex')}
            className="inline-flex items-center gap-1.5 text-[12px] font-semibold rounded-full border-2 px-3 py-1.5"
            style={{ borderColor: BORDER_MUTED, color: MUTED, backgroundColor: '#fff' }}
          >
            <BookMarked size={13} /> Codex · {state.codex.length}
          </button>
        </div>
      </div>

      {CHAIR_SUBJECTS.map(subject => (
        <div key={subject.id} className="mt-5">
          <div className="flex items-center gap-2 mb-1">
            {subject.id === 'business' ? <Stamp size={15} color={LABEL} /> : <Scale size={15} color={LABEL} />}
            <h3 className="text-[16px] font-semibold" style={{ fontFamily: SERIF, color: INK }}>
              {subject.label}
            </h3>
          </div>
          <p className="text-[12px] mb-2.5" style={{ color: MUTED }}>
            {subject.tagline}
          </p>
          <div className="space-y-2">
            {subject.sessions.map(s => {
              const result = state.results[s.id];
              return (
                <button
                  key={s.id}
                  onClick={() => openSession(s.id)}
                  className="w-full text-left rounded-2xl border-2 border-[#1a1a1a] dark:border-zinc-700 bg-white dark:bg-zinc-900 shadow-[3px_3px_0_0_#1a1a1a] dark:shadow-[3px_3px_0_0_#3f3f46] px-4 py-3 transition-transform active:translate-y-0.5 hover:-translate-y-0.5"
                >
                  <div className="flex items-center justify-between gap-3">
                    <span className="min-w-0">
                      <span className="block text-[14.5px] font-semibold" style={{ fontFamily: SERIF, color: INK }}>
                        {s.title}
                      </span>
                      <span className="block text-[11.5px] mt-0.5" style={{ color: MUTED }}>
                        Cue: {s.cue} · {s.scripts.length} scripts to mark
                      </span>
                    </span>
                    {result ? (
                      <span
                        className="shrink-0 inline-flex items-center gap-1 text-[11px] font-bold px-2 py-0.5 rounded-full"
                        style={{ backgroundColor: '#E8F2EC', color: '#1F5F3E' }}
                      >
                        <Check size={11} /> {pct(result.agreement)}
                      </span>
                    ) : (
                      <ChevronRight size={16} color={BORDER_MUTED} className="shrink-0" />
                    )}
                  </div>
                </button>
              );
            })}
          </div>
        </div>
      ))}

      <p className="text-[11px] leading-relaxed mt-6" style={{ color: LABEL }}>
        Questions and scripts are written for these exercises — they aren’t real SEC questions or real candidates’ work.
        The marking grids, scales and credit rules are the real ones, cited on every session to the SEC marking schemes
        and Chief Examiner’s Reports they come from.
      </p>
    </div>
  );
};

export default ExaminersChair;
