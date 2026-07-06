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
  codexDue,
  completeSession,
  gridDecisionKey,
  gridScriptMisses,
  isBorderlineScript,
  loadChair,
  markCodexOnCards,
  mergeMisses,
  overallCalibration,
  pct,
  reviewCodex,
  saveChair,
  scaleScriptMisses,
  scoreGridScript,
  scoreScaleScript,
  topMisses,
  type ChairState,
  type MissDelta,
  type ScriptScore,
} from './store';
import { createCard } from '../PaperTrail/flashcardStore';

const INK = '#1a1a1a';
const ACCENT = '#F26B1F';
const SUCCESS = '#3A8D5F';
const MUTED = '#7a7068';
const LABEL = '#9e9186';
const BORDER = '#d8d4ce';
/** The examiner's pen — the one colour reserved for the examiner's own marks
 * and annotations, never for app UI. (Drawn from the script margin rule.) */
const PEN = '#C4443C';
const PEN_SOFT = 'rgba(196,68,60,0.10)';
const PAPER = '#FDFCF8';

const SERIF = "'Source Serif 4', serif";
const MONO = "'DM Mono', ui-monospace, 'SF Mono', Menlo, Consolas, monospace";

const FLASHCARD_SUBJECT: Record<string, string> = { business: 'business', maths: 'mathematics' };
const LEVEL_ORDER: ChairLevel[] = ['higher', 'ordinary', 'foundation', 'common'];

type Stage = 'intro' | 'mark' | 'reveal' | 'summary' | 'own-write' | 'own-mark' | 'own-result';

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
      background: `repeating-linear-gradient(to bottom, transparent 0px, transparent 27px, rgba(90,85,80,0.07) 27px, rgba(90,85,80,0.07) 28px), ${PAPER}`,
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

// ── the calibration gauge: how close your eye is to the examiner's ──

const Gauge: React.FC<{ value: number; size?: number; caption?: string }> = ({ value, size = 116, caption }) => {
  const v = Math.max(0, Math.min(1, value));
  const w = size;
  const h = size * 0.66;
  const cx = w / 2;
  const cy = h - 6;
  const r = w / 2 - 8;
  const arc = Math.PI * r; // length of the semicircle
  const col = agreementColor(v);
  return (
    <div className="text-center" style={{ width: w }}>
      <svg viewBox={`0 0 ${w} ${h + 4}`} width={w} height={h + 4} role="img" aria-label={`Calibration ${pct(v)}`}>
        <path d={`M8 ${cy} A${r} ${r} 0 0 1 ${w - 8} ${cy}`} fill="none" stroke="#e5e0d9" strokeWidth={9} strokeLinecap="round" />
        <path
          d={`M8 ${cy} A${r} ${r} 0 0 1 ${w - 8} ${cy}`}
          fill="none"
          stroke={col}
          strokeWidth={9}
          strokeLinecap="round"
          strokeDasharray={arc}
          strokeDashoffset={arc * (1 - v)}
        />
        {/* the examiner's line at the top of the dial */}
        <line x1={cx} y1={cy - r + 1} x2={cx} y2={cy - r - 7} stroke={PEN} strokeWidth={2.5} strokeLinecap="round" />
      </svg>
      <p className="font-bold leading-none" style={{ fontFamily: SERIF, color: col, fontSize: size * 0.28, marginTop: -size * 0.06 }}>
        {pct(v)}
      </p>
      {caption && (
        <p style={{ fontFamily: MONO, fontSize: 9.5, letterSpacing: '0.08em', textTransform: 'uppercase', color: LABEL, marginTop: 2 }}>
          {caption}
        </p>
      )}
    </div>
  );
};

/** The examiner's total, circled in red pen like a stamp on the script. */
const MarkStamp: React.FC<{ marks: number; max: number }> = ({ marks, max }) => (
  <div
    className="shrink-0 flex flex-col items-center justify-center rounded-full"
    style={{ width: 56, height: 56, border: `2.5px solid ${PEN}`, color: PEN, transform: 'rotate(-8deg)', fontFamily: SERIF }}
    aria-label={`Examiner awards ${marks} of ${max}`}
  >
    <b className="leading-none" style={{ fontSize: 18 }}>
      {marks}<span style={{ fontSize: 11 }}>/{max}</span>
    </b>
    <span style={{ fontSize: 8, fontFamily: MONO, letterSpacing: '0.05em', textTransform: 'uppercase', marginTop: 1 }}>marked</span>
  </div>
);

/** A red-pen margin symbol: tick when the examiner awarded, cross when not. */
const PenMark: React.FC<{ awarded: boolean }> = ({ awarded }) => (
  <span aria-hidden="true" style={{ color: PEN, fontFamily: SERIF, fontWeight: 700, fontSize: 17, lineHeight: 1 }}>
    {awarded ? '✓' : '✗'}
  </span>
);

/** The "How this is marked" card, set in the marking scheme's own typographic
 * language — monospaced allocations, the real notation, a page clip on top. */
const SchemeExtract: React.FC<{ session: MarkingSession }> = ({ session }) => {
  const rows: { left: string; alloc: string }[] =
    session.mode === 'grid'
      ? session.grid.perPoint.map(c => ({ left: c.label, alloc: `[ ${c.marks} ]` }))
      : session.scale.levels.map(l => ({ left: l.label, alloc: `${l.annotation} · ${l.marks}` }));
  const notes = session.mode === 'grid' ? [session.grid.ruleNote] : session.scale.notes;
  const shorthand = session.mode === 'grid' ? session.grid.shorthand : `Scale ${session.scale.name}`;
  const cite = session.mode === 'grid' ? session.grid.cite.label : session.scale.cite.label;
  return (
    <div className="rounded-xl overflow-hidden mb-4" style={{ border: `2px solid ${INK}`, background: '#fff' }}>
      {/* the page clip */}
      <div className="flex items-center px-3.5" style={{ height: 26, borderBottom: `1.5px dashed ${BORDER}` }}>
        <span style={{ width: 26, height: 8, borderRadius: 3, background: PEN_SOFT, border: `1px solid rgba(196,68,60,0.35)` }} />
        <span className="ml-auto" style={{ fontFamily: MONO, fontSize: 10, letterSpacing: '0.08em', textTransform: 'uppercase', color: LABEL }}>
          Marking scheme
        </span>
      </div>
      <div className="px-4 pt-3 pb-1" style={{ overflowX: 'auto' }}>
        <p style={{ fontFamily: MONO, fontSize: 11.5, color: '#8C3A0E', marginBottom: 8 }}>{shorthand}</p>
        {rows.map((r, i) => (
          <div
            key={i}
            className="flex justify-between gap-4 py-1"
            style={{ fontFamily: MONO, fontSize: 12.5, color: INK, borderBottom: `1px dotted ${BORDER}`, whiteSpace: 'nowrap' }}
          >
            <span>{r.left}</span>
            <span style={{ color: PEN, fontWeight: 600 }}>{r.alloc}</span>
          </div>
        ))}
      </div>
      <div className="px-4 pt-2.5 pb-3.5">
        {notes.map((n, i) => (
          <p key={i} className="leading-relaxed" style={{ fontSize: 12.5, color: '#5a5550', marginBottom: 3 }}>
            {n}
          </p>
        ))}
        <p className="mt-1.5 italic" style={{ fontFamily: MONO, fontSize: 10.5, color: LABEL }}>
          {cite}
        </p>
      </div>
    </div>
  );
};

// ═══════════════════════════════ main component ═══════════════════════════════

const ExaminersChair: React.FC<Props> = ({ uid }) => {
  const [state, setState] = useState<ChairState>(() => loadChair(uid));
  const [view, setView] = useState<'home' | 'subject' | 'codex' | 'session' | 'mismatch'>('home');
  const [subjectId, setSubjectId] = useState<string | null>(null);
  const [level, setLevel] = useState<ChairLevel>('higher');
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [stage, setStage] = useState<Stage>('intro');
  const [scriptIdx, setScriptIdx] = useState(0);
  const [decisions, setDecisions] = useState<Record<string, boolean>>({});
  const [chosenLevel, setChosenLevel] = useState<string | null>(null);
  const [scores, setScores] = useState<ScriptScore[]>([]);
  const [sessionMisses, setSessionMisses] = useState<MissDelta[]>([]);
  const [ownText, setOwnText] = useState('');
  const [reason, setReason] = useState('');
  const [borderlineOnly, setBorderlineOnly] = useState(false);
  const [codexAdded, setCodexAdded] = useState(false);
  const [recallOpen, setRecallOpen] = useState<string | null>(null);

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
    setSessionMisses([]);
    setOwnText('');
    setReason('');
    setBorderlineOnly(false);
    setCodexAdded(false);
    setView('session');
  };

  /** Jump straight into a session from anywhere, setting its subject context so
   * the in-session back button returns to the right subject screen. */
  const drillSession = (id: string) => {
    const sess = allSessions().find(s => s.id === id);
    if (!sess) return;
    const subj = CHAIR_SUBJECTS.find(c => c.id === sess.subject);
    if (subj) {
      setSubjectId(subj.id);
      setLevel(levelsOf(subj).includes(sess.level) ? sess.level : levelsOf(subj)[0] ?? 'higher');
    }
    openSession(id);
  };

  // ───────────────────────────── session flow ─────────────────────────────

  if (view === 'session' && session) {
    const allScriptsU = session.scripts as (GridSession['scripts'][number] | ScaleSession['scripts'][number])[];
    const borderlineCount = allScriptsU.filter(s => isBorderlineScript(session, s)).length;
    const scripts = (borderlineOnly ? allScriptsU.filter(s => isBorderlineScript(session, s)) : session.scripts) as typeof session.scripts;
    const script = scripts[Math.min(scriptIdx, scripts.length - 1)];

    const commitScript = () => {
      const score =
        session.mode === 'grid'
          ? scoreGridScript(session, script as GridSession['scripts'][number], decisions)
          : scoreScaleScript(session, script as ScaleSession['scripts'][number], chosenLevel);
      const deltas =
        session.mode === 'grid'
          ? gridScriptMisses(session, script as GridSession['scripts'][number], decisions)
          : scaleScriptMisses(session, script as ScaleSession['scripts'][number], chosenLevel);
      setScores(prev => [...prev, score]);
      setSessionMisses(prev => [...prev, ...deltas]);
      setStage('reveal');
    };

    const nextScript = () => {
      if (scriptIdx + 1 < scripts.length) {
        setScriptIdx(i => i + 1);
        setDecisions({});
        setChosenLevel(null);
        setReason('');
        setStage('mark');
      } else {
        const now = Date.now();
        // A borderline drill is practice — record the blind spots it surfaces,
        // but don't overwrite the full session's result or auto-earn the codex.
        const base = borderlineOnly ? state : completeSession(state, session, scores, now);
        persist(mergeMisses(base, sessionMisses, now));
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
          {(stage === 'mark' || stage === 'reveal') && (
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

            <Small className="mb-1.5">How this is marked</Small>
            <SchemeExtract session={session} />

            <button
              onClick={() => { setBorderlineOnly(false); setScriptIdx(0); setStage('mark'); }}
              className="w-full rounded-full py-3 text-[15px] font-semibold text-white transition-transform active:translate-y-0.5"
              style={{ backgroundColor: ACCENT, borderBottom: '3px solid #B54D14', boxShadow: '0 4px 0 #B54D14' }}
            >
              Start marking · {session.scripts.length} scripts
            </button>
            {borderlineCount > 0 && borderlineCount < session.scripts.length && (
              <button
                onClick={() => { setBorderlineOnly(true); setScriptIdx(0); setDecisions({}); setChosenLevel(null); setStage('mark'); }}
                className="w-full mt-2.5 rounded-full py-2.5 text-[13.5px] font-semibold transition-transform active:translate-y-0.5 inline-flex items-center justify-center gap-1.5"
                style={{ backgroundColor: '#fff', color: PEN, border: `2px solid rgba(196,68,60,0.4)` }}
              >
                Borderline drill · {borderlineCount} hard {borderlineCount === 1 ? 'call' : 'calls'} only
              </button>
            )}
            <button
              onClick={() => { setDecisions({}); setChosenLevel(null); setStage('own-write'); }}
              className="w-full mt-2.5 rounded-full py-2.5 text-[13.5px] font-semibold transition-transform active:translate-y-0.5"
              style={{ backgroundColor: '#fff', color: ACCENT, border: '2px solid rgba(242,107,31,0.35)' }}
            >
              Or mark your own answer to this question
            </button>
          </>
        )}

        {/* ── mark your own work: write → self-mark → honest estimate ── */}
        {stage === 'own-write' && (
          <>
            <div className="rounded-2xl border bg-white dark:bg-zinc-900 dark:border-zinc-700 px-5 py-4 mb-3" style={{ borderColor: BORDER, padding: '18px 20px' }}>
              <Small className="mb-2">Your question</Small>
              <p className="text-[15px] leading-relaxed" style={{ fontFamily: SERIF, color: INK }}>{session.question}</p>
            </div>
            <Small className="mb-1.5">Write (or paste) your own answer</Small>
            <textarea
              value={ownText}
              onChange={e => setOwnText(e.target.value)}
              rows={7}
              placeholder="Answer as you would in the exam — then you'll mark it against the real scheme, the way the examiner would."
              className="w-full rounded-xl border px-3.5 py-3 text-[14px] leading-relaxed resize-y"
              style={{ borderColor: BORDER, background: PAPER, color: '#2a2620', fontFamily: SERIF }}
            />
            <p className="text-[11px] mt-2 mb-3" style={{ color: LABEL }}>
              Nothing here is sent anywhere or auto-graded — you’ll mark it yourself against the scheme, honestly, with the examiner’s rules in front of you.
            </p>
            <button
              onClick={() => setStage('own-mark')}
              disabled={ownText.trim().length === 0}
              className="w-full rounded-full py-3 text-[15px] font-semibold text-white transition-transform active:translate-y-0.5 disabled:opacity-40"
              style={{ backgroundColor: ACCENT, borderBottom: '3px solid #B54D14', boxShadow: '0 4px 0 #B54D14' }}
            >
              Mark it against the scheme
            </button>
          </>
        )}

        {stage === 'own-mark' && (
          <>
            <Small className="mb-1.5">Your answer</Small>
            <ScriptPaper>
              {ownText.split('\n').filter(Boolean).map((line, i) => (
                <p key={i} className="text-[14.5px] italic" style={{ fontFamily: SERIF, color: '#2a2620', lineHeight: '28px' }}>{line}</p>
              ))}
            </ScriptPaper>

            <Small className="mt-4 mb-2">Now mark it honestly — the rule is in front of you</Small>
            {session.mode === 'grid' ? (
              <div className="space-y-2.5">
                {session.grid.perPoint.map(c => {
                  const k = gridDecisionKey('own', c.id);
                  const awarded = !!decisions[k];
                  const blind = (state.misses[`${session.subject}::${c.label}`]?.over ?? 0) >
                                (state.misses[`${session.subject}::${c.label}`]?.under ?? 0);
                  return (
                    <div key={c.id} className="rounded-xl border px-3.5 py-3" style={{ borderColor: awarded ? ACCENT : BORDER, background: awarded ? '#FDEEDF' : '#fff' }}>
                      <div className="flex items-center justify-between gap-3">
                        <p className="text-[14px] font-semibold" style={{ fontFamily: SERIF, color: INK }}>{c.label} · {c.marks}m</p>
                        <button
                          onClick={() => setDecisions(d => ({ ...d, [k]: !d[k] }))}
                          className="text-[12px] font-semibold px-3 py-1.5 rounded-full border transition-transform active:translate-y-0.5"
                          style={awarded ? { backgroundColor: ACCENT, color: '#fff', borderColor: ACCENT } : { backgroundColor: '#fff', color: MUTED, borderColor: BORDER }}
                        >
                          {awarded ? '✓ Earned' : 'Not earned'}
                        </button>
                      </div>
                      {blind && (
                        <p className="text-[11.5px] mt-1.5 italic" style={{ color: PEN }}>
                          You tend to award this generously — be strict: did your answer really earn it?
                        </p>
                      )}
                    </div>
                  );
                })}
                <p className="text-[12px] leading-relaxed mt-1 italic" style={{ color: '#8C3A0E' }}>{session.grid.ruleNote}</p>
              </div>
            ) : (
              <div className="space-y-2">
                {(() => {
                  const blind = (state.misses[`${session.subject}::scale-placement`]?.over ?? 0) >
                                (state.misses[`${session.subject}::scale-placement`]?.under ?? 0);
                  return (
                    <>
                      <div className="flex flex-wrap gap-1.5">
                        {session.scale.levels.map(l => (
                          <button
                            key={l.id}
                            onClick={() => setChosenLevel(l.id)}
                            className="text-[12px] font-semibold px-2.5 py-1.5 rounded-full border transition-transform active:translate-y-0.5"
                            style={chosenLevel === l.id ? { backgroundColor: ACCENT, color: '#fff', borderColor: ACCENT } : { backgroundColor: '#fff', color: MUTED, borderColor: BORDER }}
                          >
                            {l.label} · {l.marks}m
                          </button>
                        ))}
                      </div>
                      <ul className="mt-2 space-y-1">
                        {session.scale.notes.map((n, i) => (
                          <li key={i} className="text-[12.5px] italic leading-relaxed" style={{ color: '#8C3A0E' }}>{n}</li>
                        ))}
                      </ul>
                      {blind && (
                        <p className="text-[11.5px] italic" style={{ color: PEN }}>
                          You tend to place scripts too high — be honest about which band yours truly meets.
                        </p>
                      )}
                    </>
                  );
                })()}
              </div>
            )}

            <button
              onClick={() => setStage('own-result')}
              disabled={session.mode === 'scale' && chosenLevel === null}
              className="w-full mt-4 rounded-full py-3 text-[15px] font-semibold text-white transition-transform active:translate-y-0.5 disabled:opacity-40"
              style={{ backgroundColor: ACCENT, borderBottom: '3px solid #B54D14', boxShadow: '0 4px 0 #B54D14' }}
            >
              See my honest estimate
            </button>
          </>
        )}

        {stage === 'own-result' && (() => {
          const selfMarks = session.mode === 'grid'
            ? session.grid.perPoint.reduce((sum, c) => sum + (decisions[gridDecisionKey('own', c.id)] ? c.marks : 0), 0)
            : (session.scale.levels.find(l => l.id === chosenLevel)?.marks ?? 0);
          const maxMarks = session.mode === 'grid'
            ? session.grid.perPoint.reduce((s, c) => s + c.marks, 0)
            : session.scale.levels[session.scale.levels.length - 1]?.marks ?? 0;
          return (
            <>
              <div className="rounded-2xl border bg-white dark:bg-zinc-900 dark:border-zinc-700 px-5 py-5 mb-3 text-center" style={{ borderColor: BORDER }}>
                <Small className="mb-2">Your honest self-estimate</Small>
                <p className="text-[40px] font-bold leading-none" style={{ fontFamily: SERIF, color: ACCENT }}>
                  {selfMarks}<span className="text-[20px]" style={{ color: MUTED }}>/{maxMarks}</span>
                </p>
                <p className="text-[12px] mt-2" style={{ color: MUTED }}>
                  marked against the scheme — the examiner isn’t here, so this is only as honest as you were.
                </p>
              </div>
              <div className="rounded-xl px-4 py-3.5 mb-4" style={{ backgroundColor: '#FDEEDF', borderLeft: `3px solid ${ACCENT}` }}>
                <Small className="mb-1">Hold yourself to this</Small>
                <p className="text-[14px] font-semibold" style={{ fontFamily: SERIF, color: INK }}>{session.takeaway.rule}</p>
                <p className="text-[12.5px] italic leading-relaxed mt-1" style={{ color: '#8C3A0E' }}>{session.takeaway.detail}</p>
                <CiteLine label={session.takeaway.cite.label} />
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => { setDecisions({}); setChosenLevel(null); setStage('own-write'); }}
                  className="flex-1 rounded-full py-2.5 text-[13.5px] font-semibold transition-transform active:translate-y-0.5"
                  style={{ backgroundColor: '#fff', color: MUTED, border: `2px solid ${BORDER}` }}
                >
                  Redo
                </button>
                <button
                  onClick={() => setStage('intro')}
                  className="flex-1 rounded-full py-2.5 text-[13.5px] font-semibold text-white transition-transform active:translate-y-0.5"
                  style={{ backgroundColor: ACCENT, borderBottom: '3px solid #B54D14', boxShadow: '0 3px 0 #B54D14' }}
                >
                  Mark the sample scripts
                </button>
              </div>
            </>
          );
        })()}

        {/* ── mark / reveal ── */}
        {(stage === 'mark' || stage === 'reveal') && (
          <>
            <div className="flex items-center justify-between gap-3 mb-3">
              <p className="text-[13px]" style={{ color: MUTED }}>
                <span className="font-semibold" style={{ color: INK }}>{script.label}</span>
                <span> — {script.persona}</span>
              </p>
              {stage === 'reveal' && currentScore && (
                <div className="flex items-center gap-2.5 shrink-0">
                  <div className="text-right">
                    <p className="text-[11.5px] font-bold leading-tight" style={{ color: agreementColor(currentScore.agreement) }}>
                      {pct(currentScore.agreement)} match
                    </p>
                    <p className="text-[10px] leading-tight" style={{ color: MUTED }}>
                      you {currentScore.studentMarks}m
                    </p>
                  </div>
                  <MarkStamp marks={currentScore.examinerMarks} max={currentScore.maxMarks} />
                </div>
              )}
            </div>

            {stage === 'reveal' && reason.trim() && (
              <div className="rounded-xl px-3.5 py-2.5 mb-3" style={{ backgroundColor: '#fff', border: `2px solid ${BORDER}` }}>
                <Small className="mb-1">Your reasoning</Small>
                <p className="text-[13px] italic" style={{ color: '#3a3530', fontFamily: SERIF }}>“{reason.trim()}”</p>
                <p className="text-[11px] mt-1.5" style={{ color: LABEL }}>Now read the examiner’s note below — did you see it the same way?</p>
              </div>
            )}

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
                            className="inline-flex items-center gap-1.5 text-[12px] px-2 py-1 rounded-md"
                            style={{ backgroundColor: PEN_SOFT, border: '1px solid rgba(196,68,60,0.28)' }}
                          >
                            <PenMark awarded={keyAwarded} />
                            <span className="font-semibold" style={{ color: INK }}>{c.label}</span>
                            <span style={{ fontFamily: MONO, fontSize: 11, color: PEN }}>{keyAwarded ? `${attempt.key[c.id]}m` : '0m'}</span>
                            {match ? (
                              <Check size={12} color={SUCCESS} aria-label="you agreed" />
                            ) : (
                              <span className="font-semibold" style={{ color: ACCENT, fontSize: 10.5 }}>
                                you said {awarded ? 'award' : 'no'}
                              </span>
                            )}
                          </span>
                        );
                      })}
                    </div>
                    {stage === 'reveal' && (
                      <p className="text-[12.5px] leading-relaxed mt-2 italic" style={{ color: PEN, borderLeft: `2px solid ${PEN}`, paddingLeft: 10 }}>
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
                    const matched = isKey && isChoice;
                    return (
                      <span
                        key={l.id}
                        className="inline-flex items-center gap-1.5 text-[12px] font-semibold px-2.5 py-1.5 rounded-md border"
                        style={
                          isKey
                            ? { backgroundColor: PEN_SOFT, borderColor: 'rgba(196,68,60,0.45)', color: INK }
                            : isChoice
                              ? { backgroundColor: '#FDEEDF', borderColor: ACCENT, color: '#8C3A0E' }
                              : { backgroundColor: '#fff', borderColor: BORDER, color: '#b0a898' }
                        }
                      >
                        {isKey && <PenMark awarded />}
                        {isKey && <span style={{ fontFamily: MONO, fontSize: 11, color: PEN }}>{l.annotation}</span>}
                        {l.label} · {l.marks}m
                        {isKey && (matched
                          ? <Check size={12} color={SUCCESS} aria-label="you agreed" />
                          : <span style={{ color: ACCENT, fontSize: 10.5 }}>examiner's call</span>)}
                        {isChoice && !isKey && <span style={{ fontSize: 10.5 }}>your call</span>}
                      </span>
                    );
                  })}
                </div>
                {stage === 'reveal' && (
                  <p className="text-[12.5px] leading-relaxed mt-2 italic" style={{ color: PEN, borderLeft: `2px solid ${PEN}`, paddingLeft: 10 }}>
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

            {stage === 'mark' && (
              <div className="mb-3">
                <input
                  value={reason}
                  onChange={e => setReason(e.target.value)}
                  placeholder="In a line — why did you mark it that way? (optional)"
                  className="w-full rounded-xl border px-3.5 py-2.5 text-[13px]"
                  style={{ borderColor: BORDER, background: '#fff', color: INK }}
                />
                <p className="text-[10.5px] mt-1" style={{ color: LABEL }}>
                  Commit to a reason before you see the key — then check it against the examiner’s.
                </p>
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
                  <Small className="mb-1">How close was your eye to the examiner's?</Small>
                  <div className="flex justify-center my-1">
                    <Gauge value={agreement} size={136} />
                  </div>
                  <p className="text-[13px] font-semibold" style={{ color: agreementColor(agreement) }}>
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
              <Small className="mb-1">{borderlineOnly ? 'The rule behind these calls' : 'Added to your codex'}</Small>
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
    const now = Date.now();
    const earned = allSessions().filter(s => state.codex.includes(s.takeaway.id));
    const dueIds = new Set(codexDue(state, state.codex, now));
    const dueRules = earned.filter(s => dueIds.has(s.takeaway.id));
    const earnedByRule = new Map(earned.map(s => [s.takeaway.id, s]));
    // per-subject completion, only subjects the student has started earning in
    const bySubject = CHAIR_SUBJECTS
      .map(c => ({ subject: c, earned: c.sessions.filter(s => earnedByRule.has(s.takeaway.id)), total: c.sessions.length }))
      .filter(g => g.earned.length > 0);

    const rate = (id: string, got: boolean) => {
      persist(reviewCodex(state, id, got, Date.now()));
      setRecallOpen(null);
    };

    return (
      <div className="w-full max-w-xl mx-auto pb-12">
        <button onClick={() => setView('home')} className="flex items-center gap-1.5 text-[13px] font-medium mb-4" style={{ color: MUTED }}>
          <ArrowLeft size={15} /> Subjects
        </button>
        <h2 className="text-[22px] font-semibold mb-1" style={{ fontFamily: SERIF, color: INK }}>
          Your Marker’s Codex
        </h2>
        <p className="text-[13px] mb-5" style={{ color: MUTED }}>
          The rules you’ve earned, each cited to the SEC document it comes from — {state.codex.length} of {allSessions().length}.
        </p>

        {earned.length === 0 ? (
          <p className="text-[13.5px] italic" style={{ color: LABEL }}>
            Nothing here yet — finish a marking session to earn your first rule.
          </p>
        ) : (
          <>
            {/* spaced recall of the rules */}
            {dueRules.length > 0 && (
              <div className="mb-6">
                <Small className="mb-2">Recall due · {dueRules.length}</Small>
                <div className="space-y-2.5">
                  {dueRules.map(s => {
                    const open = recallOpen === s.takeaway.id;
                    return (
                      <div key={s.takeaway.id} className="rounded-xl border px-4 py-3.5" style={{ borderColor: ACCENT, background: '#FDEEDF' }}>
                        <Small className="mb-1">{CHAIR_SUBJECTS.find(c => c.id === s.subject)?.label ?? s.subject} · {s.cue}</Small>
                        <p className="text-[14.5px] font-semibold" style={{ fontFamily: SERIF, color: INK }}>{s.title}</p>
                        {!open ? (
                          <button
                            onClick={() => setRecallOpen(s.takeaway.id)}
                            className="mt-2 text-[12.5px] font-semibold inline-flex items-center gap-1.5"
                            style={{ color: '#8C3A0E' }}
                          >
                            Recall the rule, then reveal <ChevronRight size={14} />
                          </button>
                        ) : (
                          <>
                            <p className="text-[14px] font-semibold mt-2" style={{ fontFamily: SERIF, color: INK }}>{s.takeaway.rule}</p>
                            <p className="text-[12.5px] italic leading-relaxed mt-1" style={{ color: '#8C3A0E' }}>{s.takeaway.detail}</p>
                            <div className="flex gap-2 mt-3">
                              <button onClick={() => rate(s.takeaway.id, false)} className="flex-1 rounded-full py-2 text-[12.5px] font-semibold" style={{ backgroundColor: '#fff', color: MUTED, border: `2px solid ${BORDER}` }}>Fuzzy</button>
                              <button onClick={() => rate(s.takeaway.id, true)} className="flex-1 rounded-full py-2 text-[12.5px] font-semibold text-white" style={{ backgroundColor: SUCCESS }}>Got it</button>
                            </div>
                          </>
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* per-subject completion + the rules */}
            <div className="space-y-5">
              {bySubject.map(g => (
                <div key={g.subject.id}>
                  <div className="flex items-center justify-between gap-3 mb-2">
                    <p className="text-[15px] font-semibold" style={{ fontFamily: SERIF, color: INK }}>{g.subject.label}</p>
                    <span className="text-[11.5px] font-semibold" style={{ color: g.earned.length === g.total ? SUCCESS : MUTED }}>
                      {g.earned.length}/{g.total} earned
                    </span>
                  </div>
                  <div className="h-1.5 rounded-full mb-2.5" style={{ backgroundColor: '#eceae6' }}>
                    <div className="h-1.5 rounded-full" style={{ width: `${Math.round((g.earned.length / g.total) * 100)}%`, backgroundColor: g.earned.length === g.total ? SUCCESS : ACCENT }} />
                  </div>
                  <div className="space-y-2">
                    {g.earned.map(s => (
                      <div key={s.takeaway.id} className="rounded-xl border bg-white dark:bg-zinc-900 dark:border-zinc-700 px-4 py-3" style={{ borderColor: BORDER }}>
                        <p className="text-[14px] font-semibold" style={{ fontFamily: SERIF, color: INK }}>{s.takeaway.rule}</p>
                        <p className="text-[12px] leading-relaxed mt-0.5" style={{ color: '#5a5550' }}>{s.takeaway.detail}</p>
                        <CiteLine label={s.takeaway.cite.label} />
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </>
        )}
      </div>
    );
  }

  // ───────────────────────────── mismatch map ─────────────────────────────

  if (view === 'mismatch') {
    const misses = topMisses(state, 12);
    return (
      <div className="w-full max-w-xl mx-auto pb-12">
        <button onClick={() => setView('home')} className="flex items-center gap-1.5 text-[13px] font-medium mb-4" style={{ color: MUTED }}>
          <ArrowLeft size={15} /> Subjects
        </button>
        <h2 className="text-[22px] font-semibold mb-1" style={{ fontFamily: SERIF, color: INK }}>
          Where your eye differs
        </h2>
        <p className="text-[13px] mb-5" style={{ color: MUTED }}>
          The marking calls you make differently from the examiner, most frequent first. Fix the habit, not the question.
        </p>
        {misses.length === 0 ? (
          <p className="text-[13.5px] italic" style={{ color: LABEL }}>
            Nothing to show yet — mark a few scripts and any pattern in how your eye differs from the examiner’s will surface here.
          </p>
        ) : (
          <div className="space-y-2.5">
            {misses.map(m => {
              const total = m.over + m.under;
              const generous = m.over >= m.under;
              const scale = m.key.endsWith('::scale-placement');
              const subjLabel = CHAIR_SUBJECTS.find(c => c.id === m.subject)?.label ?? m.subject;
              const headline = scale
                ? generous
                  ? `You place ${subjLabel} scripts too high on the scale`
                  : `You place ${subjLabel} scripts too low on the scale`
                : generous
                  ? `You award the “${m.label}” mark when the examiner doesn’t`
                  : `You withhold the “${m.label}” mark when the examiner gives it`;
              const drills = m.sessions
                .map(id => allSessions().find(s => s.id === id))
                .filter((s): s is MarkingSession => !!s)
                .slice(0, 3);
              return (
                <div key={m.key} className="rounded-xl border bg-white dark:bg-zinc-900 dark:border-zinc-700 px-4 py-3.5" style={{ borderColor: BORDER }}>
                  <div className="flex items-center justify-between gap-2 mb-1.5">
                    <Small>{subjLabel}</Small>
                    <span className="text-[10.5px] font-bold px-2 py-0.5 rounded-full" style={{ color: PEN, backgroundColor: PEN_SOFT }}>
                      {generous ? 'too generous' : 'too harsh'} · {total}×
                    </span>
                  </div>
                  <p className="text-[14.5px] font-semibold leading-snug" style={{ fontFamily: SERIF, color: INK }}>
                    {headline}
                  </p>
                  {m.over > 0 && m.under > 0 && (
                    <p className="text-[11.5px] mt-1" style={{ color: MUTED }}>
                      {m.over}× too generous · {m.under}× too harsh
                    </p>
                  )}
                  {drills.length > 0 && (
                    <div className="flex flex-wrap gap-1.5 mt-2.5">
                      {drills.map(s => (
                        <button
                          key={s.id}
                          onClick={() => drillSession(s.id)}
                          className="text-[11.5px] font-semibold px-2.5 py-1 rounded-full border transition-transform active:translate-y-0.5"
                          style={{ borderColor: ACCENT, color: '#8C3A0E', backgroundColor: '#FDEEDF' }}
                        >
                          Re-mark: {s.title}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              );
            })}
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
  const codexDueCount = codexDue(state, state.codex, Date.now()).length;

  return (
    <div className="w-full max-w-xl mx-auto pb-12">
      <p className="text-[14px] leading-relaxed mb-4" style={{ color: '#5a5550' }}>
        Mark sample answers against the SEC’s own rules. The closer your marking gets to the examiner’s, the better
        you’ll judge your own work when it counts.
      </p>

      <div className="rounded-xl border bg-white dark:bg-zinc-900 dark:border-zinc-700 px-4 py-3 mb-5 flex items-center justify-between gap-3" style={{ borderColor: BORDER }}>
        <div className="min-w-0 flex items-center gap-3">
          {calibration !== null && <Gauge value={calibration} size={72} caption="your eye" />}
          <div className="min-w-0">
            <Small className="mb-0.5">Calibration</Small>
            {calibration === null ? (
              <p className="text-[13px]" style={{ color: MUTED }}>
                Mark your first scripts to find your baseline.
              </p>
            ) : (
              <p className="text-[14px] font-semibold" style={{ color: agreementColor(calibration) }}>
                {calibrationBand(calibration)}
              </p>
            )}
          </div>
        </div>
        <button
          onClick={() => setView('codex')}
          className="shrink-0 inline-flex items-center gap-1.5 text-[12px] font-semibold rounded-full border px-3 py-1.5"
          style={codexDueCount > 0 ? { borderColor: ACCENT, color: '#8C3A0E', backgroundColor: '#FDEEDF' } : { borderColor: BORDER, color: MUTED, backgroundColor: '#fff' }}
        >
          <BookMarked size={13} /> Codex · {state.codex.length}{codexDueCount > 0 ? ` · ${codexDueCount} due` : ''}
        </button>
      </div>

      {(() => {
        const misses = topMisses(state, 1);
        if (misses.length === 0) return null;
        const m = misses[0];
        const generous = m.over >= m.under;
        const scale = m.key.endsWith('::scale-placement');
        const subjLabel = CHAIR_SUBJECTS.find(c => c.id === m.subject)?.label ?? m.subject;
        const phrase = scale
          ? `you place ${subjLabel} scripts too ${generous ? 'high' : 'low'} on the scale`
          : `you ${generous ? 'award' : 'withhold'} the “${m.label}” mark ${generous ? 'when the examiner doesn’t' : 'when the examiner does'}`;
        return (
          <button
            onClick={() => setView('mismatch')}
            className="w-full text-left rounded-xl px-4 py-3 mb-5 transition-transform active:translate-y-0.5"
            style={{ backgroundColor: PEN_SOFT, border: `1px solid rgba(196,68,60,0.3)` }}
          >
            <div className="flex items-center justify-between gap-3">
              <div className="min-w-0">
                <p className="text-[10.5px] font-bold uppercase tracking-[0.1em] mb-0.5" style={{ color: PEN }}>Your biggest blind spot</p>
                <p className="text-[13px] leading-snug" style={{ color: INK }}>
                  Most often, <span className="font-semibold">{phrase}</span>.
                </p>
              </div>
              <span className="shrink-0 inline-flex items-center gap-1 text-[12px] font-semibold" style={{ color: PEN }}>
                See all <ChevronRight size={14} />
              </span>
            </div>
          </button>
        );
      })()}

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
