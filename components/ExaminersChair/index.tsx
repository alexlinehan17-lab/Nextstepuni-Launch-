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
 * Structure: home (subject grid) → subject (level tabs + numbered sessions) →
 * session (rules → mark each script → reveal → summary). Content:
 * data/examinersChair/* (authored, every rule cited to SEC documents — see
 * compliance/evidence/examiners-chair.md). Scoring: ./store.ts (tested).
 */

import React, { useMemo, useState } from 'react';
import { ArrowLeft, BookMarked, Check, ChevronRight } from 'lucide-react';
import {
  CHAIR_SUBJECTS,
  LEVEL_LABEL,
  allSessions,
  type ChairLevel,
  type ChairSubject,
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
const BORDER = '#d8d4ce';

const SERIF = "'Source Serif 4', serif";

const FLASHCARD_SUBJECT: Record<string, string> = { business: 'business', maths: 'mathematics' };
const LEVEL_ORDER: ChairLevel[] = ['higher', 'ordinary', 'foundation', 'common'];

type Stage = 'intro' | 'mark' | 'reveal' | 'summary';

interface Props {
  uid?: string;
}

// ── shared bits ──

const Small: React.FC<{ children: React.ReactNode; className?: string }> = ({ children, className }) => (
  <p className={`text-[10.5px] font-bold uppercase tracking-[0.1em] ${className ?? ''}`} style={{ color: LABEL }}>
    {children}
  </p>
);

const CiteLine: React.FC<{ label: string }> = ({ label }) => (
  <p className="text-[11px] mt-2 italic" style={{ color: LABEL }}>
    Source: {label}
  </p>
);

/** Candidate work, styled as a ruled exam script with a margin rule. */
const ScriptPaper: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div
    className="relative rounded-lg border overflow-hidden"
    style={{
      borderColor: BORDER,
      background: 'repeating-linear-gradient(to bottom, transparent 0px, transparent 27px, rgba(90,85,80,0.07) 27px, rgba(90,85,80,0.07) 28px), #FDFCF8',
    }}
  >
    <span className="absolute top-0 bottom-0" style={{ left: 26, width: 1, backgroundColor: 'rgba(196,74,60,0.22)' }} aria-hidden="true" />
    <div className="py-2.5 pr-4" style={{ paddingLeft: 38 }}>
      {children}
    </div>
  </div>
);

const agreementColor = (a: number) => (a >= 0.75 ? SUCCESS : a >= 0.5 ? ACCENT : '#9e9186');

const levelsOf = (subject: ChairSubject): ChairLevel[] => {
  // Prefer the subject's declared offered levels; fall back to whatever the
  // sessions carry (older data without offeredLevels).
  const declared: ChairLevel[] = (subject.offeredLevels ?? []).filter(l => l !== 'common');
  if (declared.length) return LEVEL_ORDER.filter(l => declared.includes(l));
  return LEVEL_ORDER.filter(l => subject.sessions.some(s => s.level === l));
};

const sessionsFor = (subject: ChairSubject, level: ChairLevel): MarkingSession[] =>
  subject.sessions.filter(s => s.level === level || s.level === 'common');

// ═══════════════════════════════ main component ═══════════════════════════════

const ExaminersChair: React.FC<Props> = ({ uid }) => {
  const [state, setState] = useState<ChairState>(() => loadChair(uid));
  const [view, setView] = useState<'home' | 'subject' | 'codex' | 'session'>('home');
  const [subjectId, setSubjectId] = useState<string | null>(null);
  const [level, setLevel] = useState<ChairLevel>('higher');
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [stage, setStage] = useState<Stage>('intro');
  const [scriptIdx, setScriptIdx] = useState(0);
  const [decisions, setDecisions] = useState<Record<string, boolean>>({});
  const [chosenLevel, setChosenLevel] = useState<string | null>(null);
  const [scores, setScores] = useState<ScriptScore[]>([]);
  const [codexAdded, setCodexAdded] = useState(false);

  const subject = useMemo(() => CHAIR_SUBJECTS.find(s => s.id === subjectId) ?? null, [subjectId]);
  const session: MarkingSession | undefined = useMemo(
    () => (sessionId ? allSessions().find(s => s.id === sessionId) : undefined),
    [sessionId],
  );

  const persist = (next: ChairState) => {
    setState(next);
    saveChair(uid, next);
  };

  const openSubject = (s: ChairSubject) => {
    setSubjectId(s.id);
    setLevel(levelsOf(s)[0] ?? 'higher');
    setView('subject');
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
        <button onClick={() => setView('subject')} className="flex items-center gap-1.5 text-[13px] font-medium mb-4" style={{ color: MUTED }}>
          <ArrowLeft size={15} /> Sessions
        </button>

        <div className="flex items-start justify-between gap-3 mb-4">
          <div>
            <Small className="mb-0.5">
              {subject?.label ?? session.subject} · {LEVEL_LABEL[session.level]} · {session.cue}
            </Small>
            <h2 className="text-[22px] font-semibold leading-snug" style={{ fontFamily: SERIF, color: INK }}>
              {session.title}
            </h2>
          </div>
          {stage !== 'intro' && stage !== 'summary' && (
            <div className="flex gap-1 mt-2 shrink-0" aria-label={`Script ${scriptIdx + 1} of ${scripts.length}`}>
              {scripts.map((_, i) => (
                <span
                  key={i}
                  className="h-1.5 rounded-full"
                  style={{
                    width: 16,
                    backgroundColor: i < scriptIdx ? SUCCESS : i === scriptIdx ? ACCENT : '#e0dbd4',
                  }}
                />
              ))}
            </div>
          )}
        </div>

        {/* ── intro: the question + the real rules ── */}
        {stage === 'intro' && (
          <>
            <div className="rounded-2xl border bg-white dark:bg-zinc-900 dark:border-zinc-700 px-5 py-4.5 mb-3" style={{ borderColor: BORDER, padding: '18px 20px' }}>
              <Small className="mb-2">The question</Small>
              {'caseText' in session && session.caseText && (
                <p className="text-[13.5px] leading-relaxed mb-3 pb-3 border-b" style={{ color: '#3a3530', borderColor: '#eceae6' }}>
                  {session.caseText}
                </p>
              )}
              <p className="text-[15px] leading-relaxed" style={{ fontFamily: SERIF, color: INK }}>
                {session.question}
              </p>
              <p className="text-[11px] mt-3" style={{ color: LABEL }}>
                {session.questionNote}
              </p>
            </div>

            <div className="rounded-xl px-4 py-3.5 mb-4" style={{ backgroundColor: '#FDEEDF', borderLeft: `3px solid ${ACCENT}` }}>
              <Small className="mb-1.5">How this is marked</Small>
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
              Start marking · {scripts.length} scripts
            </button>
          </>
        )}

        {/* ── mark / reveal ── */}
        {(stage === 'mark' || stage === 'reveal') && (
          <>
            <div className="flex items-center justify-between mb-2">
              <p className="text-[13px]" style={{ color: MUTED }}>
                <span className="font-semibold" style={{ color: INK }}>{script.label}</span>
                <span> — {script.persona}</span>
              </p>
              {stage === 'reveal' && currentScore && (
                <span className="text-[11.5px] font-bold shrink-0" style={{ color: agreementColor(currentScore.agreement) }}>
                  {pct(currentScore.agreement)} match
                </span>
              )}
            </div>

            {session.mode === 'grid' ? (
              <div className="space-y-3.5 mb-4">
                {(script as GridSession['scripts'][number]).attempts.map((attempt, ai) => (
                  <div key={attempt.id}>
                    <ScriptPaper>
                      {(script as GridSession['scripts'][number]).attempts.length > 1 && (
                        <Small className="mb-1">Point {ai + 1}</Small>
                      )}
                      <p className="text-[14px] italic" style={{ fontFamily: SERIF, color: '#2a2620', lineHeight: '28px' }}>
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
                              className="text-[12px] font-semibold px-2.5 py-1.5 rounded-full border transition-transform active:translate-y-0.5"
                              style={
                                awarded
                                  ? { backgroundColor: '#FDEEDF', borderColor: ACCENT, color: '#8C3A0E' }
                                  : { backgroundColor: '#fff', borderColor: BORDER, color: MUTED }
                              }
                            >
                              {awarded ? '✓ ' : ''}
                              {c.label} · {c.marks}m
                            </button>
                          );
                        }
                        const match = awarded === keyAwarded;
                        return (
                          <span
                            key={c.id}
                            className="inline-flex items-center gap-1 text-[12px] font-semibold px-2.5 py-1.5 rounded-full border"
                            style={
                              match
                                ? { backgroundColor: '#E8F2EC', borderColor: SUCCESS, color: '#1F5F3E' }
                                : { backgroundColor: '#FDEEDF', borderColor: ACCENT, color: '#8C3A0E' }
                            }
                          >
                            {match ? <Check size={12} /> : <span className="font-bold">·</span>}
                            {c.label}: {keyAwarded ? `${attempt.key[c.id]}m` : '0m'}
                          </span>
                        );
                      })}
                    </div>
                    {stage === 'reveal' && (
                      <p className="text-[12.5px] leading-relaxed mt-2 px-0.5" style={{ color: '#5a5550' }}>
                        {attempt.keyNote}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <div className="mb-4">
                <ScriptPaper>
                  {(script as ScaleSession['scripts'][number]).work.map((line, i) => (
                    <p key={i} className="text-[14.5px] italic" style={{ fontFamily: SERIF, color: '#2a2620', lineHeight: '28px' }}>
                      {line}
                    </p>
                  ))}
                </ScriptPaper>
                <Small className="mt-3 mb-1.5">Your call — scale {session.scale.name}</Small>
                <div className="flex flex-wrap gap-1.5">
                  {session.scale.levels.map(l => {
                    const isChoice = chosenLevel === l.id;
                    const isKey = (script as ScaleSession['scripts'][number]).keyLevelId === l.id;
                    if (stage === 'mark') {
                      return (
                        <button
                          key={l.id}
                          onClick={() => setChosenLevel(l.id)}
                          className="text-[12px] font-semibold px-2.5 py-1.5 rounded-full border transition-transform active:translate-y-0.5"
                          style={
                            isChoice
                              ? { backgroundColor: '#FDEEDF', borderColor: ACCENT, color: '#8C3A0E' }
                              : { backgroundColor: '#fff', borderColor: BORDER, color: MUTED }
                          }
                        >
                          {l.label} · {l.marks}m
                        </button>
                      );
                    }
                    return (
                      <span
                        key={l.id}
                        className="inline-flex items-center gap-1 text-[12px] font-semibold px-2.5 py-1.5 rounded-full border"
                        style={
                          isKey
                            ? { backgroundColor: '#E8F2EC', borderColor: SUCCESS, color: '#1F5F3E' }
                            : isChoice
                              ? { backgroundColor: '#FDEEDF', borderColor: ACCENT, color: '#8C3A0E' }
                              : { backgroundColor: '#fff', borderColor: BORDER, color: '#b0a898' }
                        }
                      >
                        {isKey && <Check size={12} />}
                        {(isKey || isChoice) ? `${l.annotation} ` : ''}
                        {l.label} · {l.marks}m
                      </span>
                    );
                  })}
                </div>
                {stage === 'reveal' && (
                  <p className="text-[12.5px] leading-relaxed mt-2 px-0.5" style={{ color: '#5a5550' }}>
                    {(script as ScaleSession['scripts'][number]).keyNote}
                  </p>
                )}
              </div>
            )}

            {stage === 'reveal' && script.embodies && (
              <div className="rounded-xl px-4 py-3 mb-4" style={{ backgroundColor: '#FDEEDF', borderLeft: `3px solid ${ACCENT}` }}>
                <Small className="mb-1">The examiners have seen this before</Small>
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
                Confirm marks
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
                  'Finish'
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
                <div className="rounded-2xl border bg-white dark:bg-zinc-900 dark:border-zinc-700 px-5 py-5 mb-3 text-center" style={{ borderColor: BORDER }}>
                  <Small className="mb-2">Calibration this session</Small>
                  <p className="text-[42px] font-bold leading-none" style={{ fontFamily: SERIF, color: agreementColor(agreement) }}>
                    {pct(agreement)}
                  </p>
                  <p className="text-[13px] font-semibold mt-1.5" style={{ color: agreementColor(agreement) }}>
                    {calibrationBand(agreement)}
                  </p>
                  <div className="mt-3.5 space-y-1.5">
                    {scores.map((s, i) => (
                      <div key={s.scriptId} className="flex items-center gap-2">
                        <span className="text-[11px] w-14 text-left shrink-0" style={{ color: MUTED }}>
                          Script {String.fromCharCode(65 + i)}
                        </span>
                        <div className="flex-1 h-1.5 rounded-full" style={{ backgroundColor: '#e8e4de' }}>
                          <div className="h-1.5 rounded-full" style={{ width: `${Math.round(s.agreement * 100)}%`, backgroundColor: agreementColor(s.agreement) }} />
                        </div>
                        <span className="text-[11px] w-24 text-right shrink-0" style={{ color: MUTED }}>
                          you {s.studentMarks}m · key {s.examinerMarks}m
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              );
            })()}

            <div className="rounded-xl px-4 py-3.5 mb-4" style={{ backgroundColor: '#E8F2EC', borderLeft: `3px solid ${SUCCESS}` }}>
              <Small className="mb-1">Added to your codex</Small>
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
                      `Marking rule (${subject?.label ?? session.subject}): ${session.takeaway.rule}`,
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
              onClick={() => setView('subject')}
              className="w-full rounded-full py-3 text-[15px] font-semibold text-white transition-transform active:translate-y-0.5"
              style={{ backgroundColor: ACCENT, borderBottom: '3px solid #B54D14', boxShadow: '0 4px 0 #B54D14' }}
            >
              Done
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
          <ArrowLeft size={15} /> Subjects
        </button>
        <h2 className="text-[22px] font-semibold mb-1" style={{ fontFamily: SERIF, color: INK }}>
          Your Marker’s Codex
        </h2>
        <p className="text-[13px] mb-5" style={{ color: MUTED }}>
          The rules you’ve earned, each cited to the SEC document it comes from.
        </p>
        {earned.length === 0 ? (
          <p className="text-[13.5px] italic" style={{ color: LABEL }}>
            Nothing here yet — finish a marking session to earn your first rule.
          </p>
        ) : (
          <div className="space-y-2.5">
            {earned.map(s => (
              <div key={s.takeaway.id} className="rounded-xl border bg-white dark:bg-zinc-900 dark:border-zinc-700 px-4 py-3.5" style={{ borderColor: BORDER }}>
                <Small className="mb-1">{CHAIR_SUBJECTS.find(c => c.id === s.subject)?.label ?? s.subject}</Small>
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

  // ───────────────────────────── subject view ─────────────────────────────

  if (view === 'subject' && subject) {
    const levels = levelsOf(subject);
    const activeLevel = levels.includes(level) ? level : levels[0];
    const sessions = sessionsFor(subject, activeLevel);
    return (
      <div className="w-full max-w-xl mx-auto pb-12">
        <button onClick={() => setView('home')} className="flex items-center gap-1.5 text-[13px] font-medium mb-4" style={{ color: MUTED }}>
          <ArrowLeft size={15} /> Subjects
        </button>
        <h2 className="text-[22px] font-semibold" style={{ fontFamily: SERIF, color: INK }}>
          {subject.label}
        </h2>
        <p className="text-[13px] mt-0.5 mb-4" style={{ color: MUTED }}>
          {subject.tagline}
        </p>

        {levels.length > 1 && (
          <div className="inline-flex rounded-full border p-0.5 mb-4" style={{ borderColor: BORDER, backgroundColor: '#fff' }}>
            {levels.map(l => (
              <button
                key={l}
                onClick={() => setLevel(l)}
                className="text-[12.5px] font-semibold px-3.5 py-1.5 rounded-full"
                style={activeLevel === l ? { backgroundColor: ACCENT, color: '#fff' } : { color: MUTED }}
              >
                {LEVEL_LABEL[l]}
              </button>
            ))}
          </div>
        )}
        {levels.length === 1 && (
          <Small className="mb-3">{levels[0] === 'common' ? 'Common level' : `${LEVEL_LABEL[levels[0]]} level`}</Small>
        )}

        {sessions.length === 0 && (
          <div className="rounded-xl border px-4 py-4 mt-1" style={{ borderColor: BORDER, backgroundColor: '#FCFBF8' }}>
            <p className="text-[13px] leading-relaxed" style={{ color: MUTED }}>
              {LEVEL_LABEL[activeLevel]}-specific sessions are being added. The marking
              principles in the {levels.filter(l => l !== activeLevel).map(l => LEVEL_LABEL[l]).join('/')} sessions —
              how points, diagrams and answers are marked — largely carry over; the mark
              allocations differ, and verified {LEVEL_LABEL[activeLevel]} examples are on the way.
            </p>
          </div>
        )}

        <div className="space-y-2 mt-1">
          {sessions.map((s, i) => {
            const result = state.results[s.id];
            return (
              <button
                key={s.id}
                onClick={() => openSession(s.id)}
                className="w-full text-left rounded-xl border bg-white dark:bg-zinc-900 dark:border-zinc-700 px-4 py-3 transition-transform active:translate-y-0.5 hover:-translate-y-0.5 flex items-center gap-3"
                style={{ borderColor: result ? '#cfe2d6' : BORDER }}
              >
                <span
                  className="shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-[13px] font-bold"
                  style={
                    result
                      ? { backgroundColor: SUCCESS, color: '#fff' }
                      : { backgroundColor: '#f2efeb', color: MUTED, fontFamily: SERIF }
                  }
                >
                  {result ? <Check size={15} /> : i + 1}
                </span>
                <span className="min-w-0 flex-1">
                  <span className="block text-[14.5px] font-semibold truncate" style={{ fontFamily: SERIF, color: INK }}>
                    {s.title}
                  </span>
                  <span className="block text-[11.5px] mt-0.5" style={{ color: MUTED }}>
                    {s.cue} · {s.scripts.length} scripts{result ? ` · ${pct(result.agreement)} match` : ''}
                  </span>
                </span>
                <ChevronRight size={16} color="#c9c4bd" className="shrink-0" />
              </button>
            );
          })}
        </div>

        {subject.coverageNote && (
          <p className="text-[11.5px] leading-relaxed mt-4 italic" style={{ color: LABEL }}>
            {subject.coverageNote}
          </p>
        )}
        <p className="text-[11px] leading-relaxed mt-4" style={{ color: LABEL }}>
          {subject.sources.map(s => s.label).join(' · ')}
        </p>
      </div>
    );
  }

  // ───────────────────────────── home ─────────────────────────────

  const calibration = overallCalibration(state);

  return (
    <div className="w-full max-w-xl mx-auto pb-12">
      <p className="text-[14px] leading-relaxed mb-4" style={{ color: '#5a5550' }}>
        Mark sample answers against the SEC’s own rules. The closer your marking gets to the examiner’s, the better
        you’ll judge your own work when it counts.
      </p>

      <div className="rounded-xl border bg-white dark:bg-zinc-900 dark:border-zinc-700 px-4 py-3 mb-5 flex items-center justify-between gap-3" style={{ borderColor: BORDER }}>
        <div className="min-w-0">
          <Small className="mb-0.5">Calibration</Small>
          {calibration === null ? (
            <p className="text-[13px]" style={{ color: MUTED }}>
              Mark your first scripts to find your baseline.
            </p>
          ) : (
            <p className="text-[14px] font-semibold" style={{ color: agreementColor(calibration) }}>
              {pct(calibration)} · {calibrationBand(calibration)}
            </p>
          )}
        </div>
        <button
          onClick={() => setView('codex')}
          className="shrink-0 inline-flex items-center gap-1.5 text-[12px] font-semibold rounded-full border px-3 py-1.5"
          style={{ borderColor: BORDER, color: MUTED, backgroundColor: '#fff' }}
        >
          <BookMarked size={13} /> Codex · {state.codex.length}
        </button>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
        {CHAIR_SUBJECTS.map(s => {
          const done = s.sessions.filter(x => state.results[x.id]).length;
          const levels = levelsOf(s);
          return (
            <button
              key={s.id}
              onClick={() => openSubject(s)}
              className="text-left rounded-2xl border bg-white dark:bg-zinc-900 dark:border-zinc-700 px-4 py-3.5 transition-transform active:translate-y-0.5 hover:-translate-y-0.5"
              style={{ borderColor: BORDER }}
            >
              <p className="text-[16px] font-semibold" style={{ fontFamily: SERIF, color: INK }}>
                {s.label}
              </p>
              <p className="text-[11.5px] mt-0.5 mb-2.5" style={{ color: MUTED }}>
                {levels.map(l => LEVEL_LABEL[l]).join(' · ')} · {s.sessions.length} sessions
              </p>
              <div className="flex items-center gap-2">
                <div className="flex-1 h-1.5 rounded-full" style={{ backgroundColor: '#eceae6' }}>
                  <div
                    className="h-1.5 rounded-full"
                    style={{
                      width: `${s.sessions.length ? Math.round((done / s.sessions.length) * 100) : 0}%`,
                      backgroundColor: done === s.sessions.length && done > 0 ? SUCCESS : ACCENT,
                    }}
                  />
                </div>
                <span className="text-[11px] font-semibold shrink-0" style={{ color: done > 0 ? INK : LABEL }}>
                  {done}/{s.sessions.length}
                </span>
              </div>
            </button>
          );
        })}
      </div>

      <p className="text-[11px] leading-relaxed mt-6" style={{ color: LABEL }}>
        Questions and scripts are written for these exercises — they aren’t real SEC questions or real candidates’ work.
        The marking grids, scales and credit rules are the real ones, cited on every session to the SEC marking schemes
        and Chief Examiner’s Reports they come from.
      </p>
    </div>
  );
};

export default ExaminersChair;
