/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Mark Bank — the review session. The flagship screen.
 *
 * A real SEC question in the examiner's wording, then the actual marking scheme
 * revealed as the discrete points the examiner awards marks for, which the
 * student ticks off against what they wrote. The ticks suggest a grade; the
 * student always decides.
 *
 * Three interaction decisions are load-bearing and deliberate:
 *
 *  - **The reveal is not a flip.** The scheme unrolls *beneath* the question and
 *    the question stays on screen. A flip hides the prompt at the exact moment
 *    the student judges themselves against the answer, which is the foresight
 *    bias that inflates self-assessment — we would be building the overconfidence
 *    problem into the interaction.
 *
 *  - **Rows default to not-claimed.** Overconfidence then requires an action
 *    rather than an omission. This matters because the lowest-attaining students
 *    are the most overconfident self-assessors, and they are who this is for.
 *
 *  - **The suggested grade is a suggestion, not a verdict.** All three buttons
 *    stay live and the suggestion is expressed physically — the button sits
 *    proud — never chromatically, because orange must never come to mean
 *    "correct".
 *
 * Colour containment: the environment colour appears only OUTSIDE cards and the
 * state colours only INSIDE them, so a deep green background can never be
 * compared against the success green that means "you had this mark". They never
 * share a surface. `test/markBankSession.test.tsx` asserts it.
 */

import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { AnimatePresence, MotionDiv, MotionSpan, useReducedMotion } from '../Motion';
import { rowId, type LabelKey, type MarkRow, type SecCard } from '../../types/markBank';
import type { MarkBankGrade } from './scheduler';

const EASE = [0.16, 1, 0.3, 1] as number[];

/** Deep forest green. Far darker than the success token so the two can never be
 *  mistaken for each other even if a future layout breaks containment. */
export const ENVIRONMENT = '#123B2B';

const INK = '#1a1a1a';
const INK_2 = '#3a3530';
const MUTED = '#7a7068';
const LABEL = '#9e9186';
const HAIRLINE = '#ece9e4';
const MUTED_BORDER = '#d0cdc8';
const PLATE = '#F0FAF8';
const SUCCESS = '#3A8D5F';
const SUCCESS_TINT = '#E8F2EC';
const SUCCESS_TEXT = '#1F5F3E';
const RISK_TINT = '#FDEEDF';
const RISK_TEXT = '#8C3A0E';

const SERIF = "'Source Serif 4', Georgia, serif";
const SANS = "'DM Sans', system-ui, sans-serif";
const MONO = "'Roboto Mono', ui-monospace, monospace";

/** How the student answered one row. */
type RowClaim = 'no' | 'yes' | 'synonym';

export interface SessionCardResult {
  cardId: string;
  grade: MarkBankGrade;
  marksClaimed: number;
  marksAvailable: number;
}

export interface SessionScreenProps {
  /** Resolved queue for this sitting. Snapshotted by the caller so it cannot
   *  shrink underneath the student mid-session. */
  cards: SecCard[];
  subjectLabel: string;
  /**
   * Called on every graded card. Grades commit per card, never batched, so
   * leaving mid-session is always safe.
   *
   * The caller owns the scheduler, so it may return the words for when this card
   * comes back ("in about 5 days") and the screen will whisper exactly that
   * rather than a generic reassurance.
   */
  onGrade: (result: SessionCardResult) => string | void;
  onExit: () => void;
  onFinish: (results: SessionCardResult[]) => void;
  environmentColor?: string;
}

/* ------------------------------------------------------------- mark logic ---- */

/** Marks a row is worth when claimed. `anyN` groups count their claimable max. */
export function rowMarks(row: MarkRow): number {
  if (row.kind === 'anyN' && row.group) return row.group.claimMax * row.group.perOption;
  return row.marks ?? 0;
}

/** Total marks a student can claim on this card. Falls back to the printed
 *  tariff when the scheme leaves per-row values undefined. */
export function claimableTotal(card: SecCard): number {
  if (card.tariffModel.kind === 'orderedSplit') return card.totalMarks;
  if (card.tariffModel.kind === 'bestNofParts') {
    return card.tariffModel.answer * card.tariffModel.perPart;
  }
  return card.rows.reduce((n, r) => n + rowMarks(r), 0);
}

/** Only a `fixed` tariff may show per-row mark chips: for the other conventions
 *  a per-row number would be arithmetically wrong, so we show none. */
export const showsRowMarks = (card: SecCard) => card.tariffModel.kind === 'fixed';

export function marksClaimed(card: SecCard, claims: Record<string, RowClaim>): number {
  if (!showsRowMarks(card)) return 0;
  return card.rows.reduce((n, r, i) => (claims[rowId(r, i)] !== 'no' ? n + rowMarks(r) : n), 0);
}

/**
 * The SEC's asterisk marks a row where only the exact scientific term scores, and
 * where adding a wrong answer alongside it cancels THAT row's mark. It does not
 * zero the rest of the question — each asterisked item stands or falls alone.
 */
export const needsExactTerm = (row: MarkRow) => row.kind === 'gate' || !!row.exactTermRequired;

/**
 * Which grade the ticks point at. It follows the marks and nothing else — a
 * student who claimed every mark is told it looks like Got it.
 *
 * There is no first-encounter override here. One used to force Shaky on a card's
 * first showing, on the theory that a single self-graded pass should not buy a
 * long interval; but FSRS already guarantees that through its learning steps, so
 * the override bought nothing and produced the absurdity of "you claimed 12 of 12
 * marks — that looks like Shaky".
 */
export function suggestGrade(
  card: SecCard,
  claims: Record<string, RowClaim>,
): MarkBankGrade {
  const total = claimableTotal(card);
  const got = marksClaimed(card, claims);
  if (!showsRowMarks(card)) {
    const claimedRows = card.rows.filter((r, i) => claims[rowId(r, i)] !== 'no').length;
    if (claimedRows === 0) return 'missed';
    return claimedRows === card.rows.length ? 'got' : 'shaky';
  }
  if (got <= 0) return 'missed';
  return got >= total ? 'got' : 'shaky';
}

/* ------------------------------------------------------------- small bits ---- */

/** A number that counts to its new value. Marks count DOWN — the mistake-first
 *  reading is what a student should feel: marks leaving the table. */
const Tally: React.FC<{ value: number; reduced: boolean }> = ({ value, reduced }) => {
  const [shown, setShown] = useState(value);
  const raf = useRef<number | undefined>(undefined);
  const shownRef = useRef(value);
  shownRef.current = shown;

  useEffect(() => {
    if (reduced) { setShown(value); return; }
    const from = shownRef.current;
    if (from === value) return;

    // The clock must come from the frame itself. Seeding `start` from
    // performance.now() assumes it shares an epoch with the timestamp rAF hands
    // back; where it does not, elapsed goes negative, the eased term inverts and
    // the number overshoots — a 9-mark card rendered "11 marks left behind".
    let start: number | undefined;
    const tick = (t: number) => {
      if (start === undefined) start = t;
      const p = Math.min(1, Math.max(0, (t - start) / 260));
      setShown(Math.round(from + (value - from) * (1 - Math.pow(1 - p, 3))));
      if (p < 1) raf.current = requestAnimationFrame(tick);
      else setShown(value);
    };
    raf.current = requestAnimationFrame(tick);
    return () => { if (raf.current) cancelAnimationFrame(raf.current); };
  }, [value, reduced]);
  return <span style={{ fontVariantNumeric: 'tabular-nums' }}>{shown}</span>;
};

const ProgressRail: React.FC<{ total: number; done: number }> = ({ total, done }) => (
  <div style={{ display: 'flex', gap: 3, flex: 1 }} aria-hidden="true">
    {Array.from({ length: total }, (_, i) => (
      <div
        key={i}
        style={{
          height: 3, flex: 1, borderRadius: 2,
          background: i < done ? '#FFFFFF' : 'rgba(255,255,255,0.26)',
          transition: 'background 240ms',
        }}
      />
    ))}
  </div>
);

/* ---------------------------------------------------------------- the row ---- */

const MarkRowView: React.FC<{
  row: MarkRow;
  id: string;
  index: number;
  claim: RowClaim;
  showMarks: boolean;
  blocked: boolean;
  reduced: boolean;
  onClaim: (id: string, next: RowClaim) => void;
}> = ({ row, id, index, claim, showMarks, blocked, reduced, onClaim }) => {
  const claimed = claim !== 'no';
  const marks = rowMarks(row);
  const isGate = row.kind === 'gate';
  const canSynonym = !row.exactTermRequired && (row.openList || row.kind === 'alt');

  return (
    <MotionDiv
      initial={reduced ? false : { opacity: 0, x: -8 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.24, ease: EASE, delay: reduced ? 0 : index * 0.055 }}
      style={{ marginBottom: 8 }}
    >
      <button
        type="button"
        onClick={() => !blocked && onClaim(id, claimed ? 'no' : 'yes')}
        disabled={blocked}
        aria-pressed={claimed}
        style={{
          width: '100%', textAlign: 'left', display: 'grid',
          gridTemplateColumns: '20px 1fr auto', gap: 10, alignItems: 'start',
          padding: '11px 12px', borderRadius: 12,
          border: `1.5px solid ${claimed ? SUCCESS : MUTED_BORDER}`,
          background: claimed ? SUCCESS_TINT : '#FFFFFF',
          cursor: blocked ? 'not-allowed' : 'pointer',
          opacity: blocked ? 0.5 : 1,
          font: `500 13.5px/1.42 ${SANS}`, color: INK_2,
          transition: reduced ? 'none' : 'background 160ms, border-color 160ms',
        }}
      >
        <MotionSpan
          animate={reduced ? {} : { scale: claimed ? 1 : 0.85 }}
          transition={{ type: 'spring', stiffness: 420, damping: 26 }}
          style={{
            width: 18, height: 18, borderRadius: '50%', marginTop: 1,
            background: claimed ? SUCCESS : 'transparent',
            border: claimed ? 'none' : `1.5px solid ${MUTED_BORDER}`,
            display: 'inline-flex', alignItems: 'center', justifyContent: 'center', flex: 'none',
          }}
        >
          {/* Drawn, not typed: a U+2713 text tick renders with emoji presentation
              on some platforms, and this app bans emoji as UI furniture. */}
          {claimed && (
            <svg width="11" height="11" viewBox="0 0 12 12" fill="none" aria-hidden="true">
              <path d="M2.5 6.2l2.4 2.4L9.5 3.9" stroke="#FFFFFF" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          )}
        </MotionSpan>

        <span>
          <span style={{ color: claimed ? SUCCESS_TEXT : INK_2 }}>
            {row.verbatim}
            {/* The scheme's own alternatives, shown in full: a student who wrote
                "heterotrophic" earned the mark and must be able to see that. */}
            {row.accepts?.length ? (
              <span style={{ color: MUTED }}>
                {' or '}{row.accepts.join(' or ')}
              </span>
            ) : null}
          </span>
          {row.exactTermRequired && (
            <span style={{
              display: 'inline-block', marginLeft: 6, padding: '0 6px', borderRadius: 4,
              background: RISK_TINT, color: RISK_TEXT,
              font: `600 9px/1.6 ${SANS}`, letterSpacing: '.06em', textTransform: 'uppercase',
              verticalAlign: 1,
            }}>
              needs the exact term
            </span>
          )}
          {row.contextNote && (
            <span style={{ display: 'block', marginTop: 3, font: `400 12px/1.4 ${SANS}`, color: MUTED }}>
              {row.contextNote}
            </span>
          )}
          {row.kind === 'anyN' && row.group && (
            <span style={{ display: 'block', marginTop: 5, font: `400 11.5px/1.4 ${SANS}`, color: MUTED }}>
              Any {row.group.claimMax} of: {row.group.options.join(' · ')}
            </span>
          )}
        </span>

        {showMarks && !isGate && (
          <span style={{
            font: `700 10.5px/1.7 ${MONO}`, borderRadius: 6, padding: '0 6px', whiteSpace: 'nowrap',
            fontVariantNumeric: 'tabular-nums',
            background: claimed ? SUCCESS_TINT : RISK_TINT,
            color: claimed ? SUCCESS_TEXT : RISK_TEXT,
          }}>
            {claimed ? `${marks}m` : `−${marks}m`}
          </span>
        )}
      </button>

      {canSynonym && !claimed && (
        <button
          type="button"
          onClick={() => onClaim(id, 'synonym')}
          style={{
            marginTop: 4, marginLeft: 42, background: 'none', border: 'none', padding: 0,
            font: `600 11.5px/1.5 ${SANS}`, color: SUCCESS_TEXT,
            borderBottom: `1px solid ${SUCCESS}`, cursor: 'pointer',
          }}
        >
          I had something like this
        </button>
      )}
      {claim === 'synonym' && (
        <span style={{ display: 'block', marginTop: 4, marginLeft: 42, font: `400 11.5px/1.5 ${SANS}`, color: MUTED }}>
          The examiner accepts synonyms here.
        </span>
      )}
    </MotionDiv>
  );
};

/* ------------------------------------------------------------ label key ----- */

const LabelKeyPanel: React.FC<{ keys: LabelKey[] }> = ({ keys }) => (
  <div style={{ marginTop: 12, padding: '11px 13px', borderRadius: 10, background: PLATE }}>
    <span style={{
      display: 'block', marginBottom: 6, font: `700 9px/1.6 ${SANS}`,
      letterSpacing: '.11em', textTransform: 'uppercase', color: LABEL,
    }}>
      What every label means
    </span>
    <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
      {keys.map(k => (
        <span
          key={k.letter}
          style={{
            font: `500 12px/1.5 ${SANS}`, background: '#FFFFFF', borderRadius: 6,
            padding: '3px 9px', color: k.askedInThisQuestion ? INK_2 : MUTED,
          }}
        >
          <strong style={{ fontFamily: MONO, fontSize: 11.5 }}>{k.letter}</strong> — {k.meaning}
          {!k.askedInThisQuestion && (
            <span style={{ marginLeft: 5, font: `400 10px/1 ${SANS}`, color: LABEL }}>not asked</span>
          )}
        </span>
      ))}
    </div>
  </div>
);

/* ------------------------------------------------------------ the screen ---- */

const GRADE_COPY: Record<MarkBankGrade, string> = {
  missed: 'Missed it',
  shaky: 'Shaky',
  got: 'Got it',
};

const SessionScreen: React.FC<SessionScreenProps> = ({
  cards, subjectLabel, onGrade, onExit, onFinish,
  environmentColor = ENVIRONMENT,
}) => {
  const reduced = useReducedMotion() ?? false;
  const [queue, setQueue] = useState(() => cards.map(c => c.id));
  const [position, setPosition] = useState(0);
  const [revealed, setRevealed] = useState(false);
  const [claims, setClaims] = useState<Record<string, RowClaim>>({});
  const [results, setResults] = useState<SessionCardResult[]>([]);
  const [whisper, setWhisper] = useState<string | null>(null);
  const byId = useMemo(() => new Map(cards.map(c => [c.id, c])), [cards]);

  const card = byId.get(queue[position]);
  const distinctDone = new Set(results.map(r => r.cardId)).size;

  const claimOf = useCallback((id: string): RowClaim => claims[id] ?? 'no', [claims]);
  const rowClaims = useMemo(() => {
    if (!card) return {};
    const out: Record<string, RowClaim> = {};
    card.rows.forEach((r, i) => { out[rowId(r, i)] = claimOf(rowId(r, i)); });
    return out;
  }, [card, claimOf]);

  const total = card ? claimableTotal(card) : 0;
  const got = card ? marksClaimed(card, rowClaims) : 0;
  const left = Math.max(0, total - got);
  const suggested = card ? suggestGrade(card, rowClaims) : 'shaky';

  const setClaim = useCallback((id: string, next: RowClaim) => {
    setClaims(prev => ({ ...prev, [id]: next }));
  }, []);

  const claimAll = useCallback(() => {
    if (!card) return;
    const all: Record<string, RowClaim> = {};
    card.rows.forEach((r, i) => { all[rowId(r, i)] = 'yes'; });
    setClaims(prev => ({ ...prev, ...all }));
  }, [card]);

  const commit = useCallback((grade: MarkBankGrade) => {
    if (!card) return;
    const result: SessionCardResult = {
      cardId: card.id, grade, marksClaimed: got, marksAvailable: total,
    };
    const words = onGrade(result);
    const nextResults = [...results, result];
    setResults(nextResults);

    // Never "correct" or "failed" — only when it comes back, and always warmly.
    //
    // A first encounter graded well still returns within the hour: that is the
    // learning step doing its job, consolidating before the card is spaced out.
    // Said plainly it would read as a punishment for getting it right, so a
    // same-day return after a positive grade is framed as what it is.
    const soon = !!words && /today/.test(words);
    setWhisper(
      words
        ? grade === 'missed'
          ? `No bother. It's back ${words}.`
          : soon
            ? `Good — one more look ${words}, then it starts spacing out.`
            : `Nice. This one's back ${words}.`
        : grade === 'got' ? "Nice. You won't see this one for a while."
        : grade === 'shaky' ? 'Good — that one comes back soon.'
        : "No bother. It'll come back before you finish today.",
    );

    // "Missed it" re-serves the card at the end of the sitting, so the number of
    // presentations exceeds twelve while the number of distinct cards does not.
    const nextQueue = grade === 'missed' ? [...queue, card.id] : queue;
    const seen = new Set(nextResults.map(r => r.cardId));
    const finished = nextQueue.slice(position + 1).every(id => seen.has(id) && grade !== 'missed');

    setQueue(nextQueue);
    setClaims({});
    setRevealed(false);

    if (position + 1 >= nextQueue.length || finished) onFinish(nextResults);
    else setPosition(position + 1);
  }, [card, got, total, onGrade, results, queue, position, onFinish]);

  useEffect(() => {
    if (!whisper) return;
    const t = setTimeout(() => setWhisper(null), reduced ? 400 : 1100);
    return () => clearTimeout(t);
  }, [whisper, reduced]);

  if (!card) return null;

  const levelLabel = card.level === 'higher' ? 'HIGHER LEVEL' : 'ORDINARY LEVEL';
  const figure = 'figure' in card ? card.figure : undefined;
  const labelKey = card.kind === 'diagram' ? card.labelKey : undefined;

  return (
    <div style={{
      minHeight: '100dvh', background: environmentColor,
      paddingBottom: 'calc(150px + var(--sab, 0px))',
      fontFamily: SANS,
      // Full-bleed: the tool renders inside a max-width app shell, so without
      // this the environment reads as a green column with page background either
      // side rather than as the environment it is meant to be.
      width: '100vw', marginLeft: 'calc(50% - 50vw)', marginRight: 'calc(50% - 50vw)',
      // Centre the card on tall desktop viewports instead of stranding it at the
      // top above a large empty field.
      display: 'flex', flexDirection: 'column',
    }}>
      {/* Top rail — leaving is always safe, grades commit per card. */}
      <div style={{
        position: 'sticky', top: 0, zIndex: 3, display: 'flex', alignItems: 'center', gap: 12,
        padding: '14px 16px', background: environmentColor,
      }}>
        <button
          type="button" onClick={onExit} aria-label="Leave this session"
          style={{ background: 'none', border: 'none', padding: 4, cursor: 'pointer', color: '#FFFFFF', lineHeight: 0 }}
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path d="M15 18l-6-6 6-6" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </button>
        <ProgressRail total={cards.length} done={distinctDone} />
        <span style={{
          font: `700 11px/1 ${MONO}`, color: 'rgba(255,255,255,0.82)',
          fontVariantNumeric: 'tabular-nums', whiteSpace: 'nowrap',
        }}>
          {Math.min(distinctDone + 1, cards.length)} of {cards.length}
        </span>
      </div>

      {/* The card. White, always — the environment colour never enters it. */}
      <div style={{ maxWidth: 560, width: '100%', margin: '0 auto', padding: '4px 12px 0', flex: '0 0 auto' }}>
        <div style={{ background: '#FFFFFF', borderRadius: 20, overflow: 'hidden' }}>
          <div style={{ padding: '16px 18px 0' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', gap: 10 }}>
              <span style={{
                font: `700 9.5px/1.5 ${SANS}`, letterSpacing: '.11em',
                textTransform: 'uppercase', color: LABEL,
              }}>
                {subjectLabel} · {levelLabel} · {card.year} · {card.questionRef.replace(/^\d{4}\s+(HL|OL)\s+/, '')}
              </span>
              <span style={{
                font: `700 11.5px/1 ${MONO}`, background: PLATE, color: INK,
                borderRadius: 6, padding: '4px 7px', fontVariantNumeric: 'tabular-nums', whiteSpace: 'nowrap',
              }}>
                {card.totalMarks}m
              </span>
            </div>

            {card.stem && (
              <p style={{ margin: '10px 0 0', font: `400 14px/1.55 ${SANS}`, color: MUTED }}>{card.stem}</p>
            )}

            <p style={{ margin: '9px 0 0', font: `500 19px/1.45 ${SERIF}`, color: INK }}>
              {card.questionText}
            </p>

            {figure && (
              <figure style={{ margin: '13px 0 0' }}>
                <div style={{ background: PLATE, borderRadius: 12, padding: 10, textAlign: 'center' }}>
                  <img
                    src={figure.src} alt={figure.alt}
                    style={{ maxWidth: '100%', maxHeight: 260, objectFit: 'contain', display: 'inline-block' }}
                  />
                </div>
                <figcaption style={{ marginTop: 6, font: `400 10.5px/1.4 ${SANS}`, color: LABEL }}>
                  {figure.attribution}
                </figcaption>
              </figure>
            )}
          </div>

          {!revealed && (
            <div style={{ padding: '16px 18px 18px' }}>
              <p style={{ margin: '0 0 11px', font: `italic 400 13px/1.5 ${SANS}`, color: MUTED }}>
                Answer it in your head, or write it out. Then reveal the scheme.
              </p>
              <button
                type="button"
                onClick={() => setRevealed(true)}
                style={{
                  width: '100%', padding: '13px 18px', borderRadius: 14,
                  background: INK, color: '#FFFFFF', border: 'none',
                  font: `650 14.5px/1 ${SANS}`, cursor: 'pointer',
                }}
              >
                Reveal the marking scheme
              </button>
            </div>
          )}

          <AnimatePresence>
            {revealed && (
              <MotionDiv
                key="scheme"
                initial={reduced ? { opacity: 0 } : { height: 0, opacity: 0, y: 8 }}
                animate={reduced ? { opacity: 1 } : { height: 'auto', opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
                transition={{ duration: reduced ? 0.12 : 0.32, ease: EASE }}
                style={{ overflow: 'hidden' }}
              >
                <div style={{ padding: '4px 18px 18px', borderTop: `1px solid ${HAIRLINE}`, marginTop: 14 }}>
                  <div style={{
                    display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                    padding: '12px 0 9px',
                  }}>
                    <span style={{
                      font: `700 9.5px/1.5 ${SANS}`, letterSpacing: '.12em',
                      textTransform: 'uppercase', color: LABEL,
                    }}>
                      The scheme
                    </span>
                    <button
                      type="button" onClick={claimAll}
                      style={{
                        background: 'none', border: 'none', padding: 0, cursor: 'pointer',
                        font: `600 11.5px/1.5 ${SANS}`, color: SUCCESS_TEXT,
                        borderBottom: `1px solid ${SUCCESS}`,
                      }}
                    >
                      I had them all
                    </button>
                  </div>

                  {card.rows.map((row, i) => {
                    const id = rowId(row, i);
                    return (
                      <MarkRowView
                        key={id}
                        row={row} id={id} index={i}
                        claim={claimOf(id)}
                        showMarks={showsRowMarks(card)}
                        blocked={!!row.dependsOn && claimOf(row.dependsOn) === 'no'}
                        reduced={reduced}
                        onClaim={setClaim}
                      />
                    );
                  })}

                  {card.tariffModel.kind === 'orderedSplit' && (
                    <p style={{ margin: '2px 0 0', font: `400 12px/1.45 ${SANS}`, color: MUTED }}>
                      The examiner marks the first correct answers higher than the rest
                      ({card.tariffModel.notation}) — so what these are worth depends on how many you got.
                    </p>
                  )}
                  {card.tariffModel.kind === 'bestNofParts' && (
                    <p style={{ margin: '2px 0 0', font: `400 12px/1.45 ${SANS}`, color: MUTED }}>
                      Answer any {card.tariffModel.answer} of these {card.tariffModel.ofParts} —
                      {' '}{card.tariffModel.perPart} marks each.
                    </p>
                  )}

                  {labelKey && <LabelKeyPanel keys={labelKey} />}

                  <p style={{ margin: '14px 0 0', font: `400 10px/1.45 ${SANS}`, color: LABEL }}>
                    {card.schemeCitation}
                  </p>
                </div>
              </MotionDiv>
            )}
          </AnimatePresence>
        </div>
      </div>

      {/* The interval whisper lives OUTSIDE the grade bar on purpose. Grading
          advances the card and closes the scheme, so anything rendered inside
          the bar unmounts at exactly the moment it has something to say — the
          message would only ever be seen by a student who tapped through fast
          enough to keep the bar alive. The schedule speaks on its own surface. */}
      <AnimatePresence>
        {whisper && (
          <MotionDiv
            key="whisper"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            transition={{ duration: reduced ? 0.12 : 0.22, ease: EASE }}
            style={{
              position: 'fixed', left: 0, right: 0, bottom: 0, zIndex: 5,
              background: '#FFFFFF', borderTop: `1px solid ${HAIRLINE}`,
              padding: `14px 16px calc(14px + var(--sab, 0px))`,
            }}
          >
            <p style={{
              maxWidth: 560, margin: '0 auto',
              font: `500 13.5px/1.45 ${SANS}`, color: SUCCESS_TEXT,
            }}>
              {whisper}
            </p>
          </MotionDiv>
        )}
      </AnimatePresence>

      {/* Grade bar. Solid white, never translucent — blurred glass over a
          saturated colour goes muddy and reads as generated UI. */}
      {revealed && !whisper && (
        <div style={{
          position: 'fixed', left: 0, right: 0, bottom: 0, zIndex: 4,
          background: '#FFFFFF', borderTop: `1px solid ${HAIRLINE}`,
          padding: `12px 16px calc(12px + var(--sab, 0px))`,
        }}>
          <div style={{ maxWidth: 560, margin: '0 auto' }}>
            {showsRowMarks(card) && (
              <div style={{
                marginBottom: 10, padding: '8px 11px', borderRadius: 10,
                background: left === 0 ? SUCCESS_TINT : RISK_TINT,
                color: left === 0 ? SUCCESS_TEXT : RISK_TEXT,
                font: `700 9.5px/1.5 ${SANS}`, letterSpacing: '.11em', textTransform: 'uppercase',
              }}>
                {left === 0 ? (
                  <>All {total} marks. Nothing left behind.</>
                ) : (
                  <>
                    Marks left behind · <span style={{ font: `700 14px/1 ${MONO}`, letterSpacing: 0 }}>
                      <Tally value={left} reduced={reduced} />
                    </span>
                  </>
                )}
              </div>
            )}

            <AnimatePresence mode="wait">
              {(
                <MotionDiv key="grades" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.18 }}>
                  <p style={{ margin: '0 0 9px', font: `400 12px/1.45 ${SANS}`, color: INK_2 }}>
                    {showsRowMarks(card)
                      ? <>You claimed {got} of {total} marks — that looks like {GRADE_COPY[suggested]}.</>
                      : <>That looks like {GRADE_COPY[suggested]}.</>}
                    <br />
                    <em style={{ color: MUTED }}>You decide. Tap any of the three.</em>
                  </p>
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 8 }}>
                    {(['missed', 'shaky', 'got'] as MarkBankGrade[]).map(g => {
                      const isSuggested = g === suggested;
                      return (
                        <button
                          key={g}
                          type="button"
                          onClick={() => commit(g)}
                          data-suggested={isSuggested || undefined}
                          style={{
                            padding: '12px 4px', borderRadius: 14, cursor: 'pointer',
                            background: '#FFFFFF', color: INK,
                            border: `1.5px solid ${INK}`,
                            // The suggestion is physical, never chromatic: orange
                            // must not come to mean "correct".
                            boxShadow: isSuggested ? `0 4px 0 0 ${INK}` : 'none',
                            transform: isSuggested ? 'translateY(-2px)' : 'none',
                            font: `650 13.5px/1.2 ${SANS}`,
                          }}
                        >
                          {GRADE_COPY[g]}
                        </button>
                      );
                    })}
                  </div>
                </MotionDiv>
              )}
            </AnimatePresence>
          </div>
        </div>
      )}
    </div>
  );
};

export default SessionScreen;
