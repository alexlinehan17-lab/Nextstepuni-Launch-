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
import { splitForEmphasis } from './questionEmphasis';
import { createPortal } from 'react-dom';
import { AnimatePresence, MotionDiv, MotionSpan, useReducedMotion } from '../Motion';
import { rowId, type LabelKey, type MarkRow, type SecCard } from '../../types/markBank';
import type { MarkBankGrade } from './scheduler';
import { figureUrl } from '../../utils/figureUrl';

const EASE = [0.16, 1, 0.3, 1] as number[];

const INK = '#1a1a1a';
const INK_2 = '#3a3530';
const MUTED = '#7a7068';
const LABEL = '#9e9186';
const MUTED_BORDER = '#d0cdc8';
const PLATE = '#F0FAF8';
const SUCCESS = '#3A8D5F';
const SUCCESS_TINT = '#E8F2EC';
const SUCCESS_TEXT = '#1F5F3E';
/** Accent means "this is the action / you are here". Never "correct". */
const ACCENT = '#F26B1F';
/** The accent mixed ~55/45 with white: the offset sheets behind the question
    card. A quiet tint, not full accent — a solid #F26B1F band down two sides
    of a white card on this light page out-shouts the question text itself. */
const ACCENT_SHEET = '#F8AE84';

/** How far the frame layers sit off the card, and the stroke's weight. */
const FRAME_OFFSET = 8;
const STROKE = 2;
/** A flat accent bar. The registration frame is four of these rather than a
 *  bordered box: the design guard forbids coloured left borders in this file,
 *  and separate bars also let each arm terminate exactly where it should. */
const ACCENT_BAR: React.CSSProperties = {
  position: 'absolute', background: ACCENT, pointerEvents: 'none',
};

/**
 * Which frame the question card wears. 'stack' is two tinted sibling sheets on
 * opposite diagonals; 'registration' pairs the down-right tinted sheet with a
 * crisp full-accent stroke up-left, closer to the founder's reference. One
 * word to flip between them while the choice is being made.
 */
type Frame = 'stack' | 'registration';
const FRAME = 'registration' as Frame;
const PAPER = '#f0f0f0';
/** A rule, not a fill: enough to bound a figure without adding a surface. */
const HAIRLINE_2 = '#e0ddd8';
/** One work surface for the whole tool: 620 question + 32 gutter + 440 scheme. */
const SURFACE = 1092;
const QUESTION_W = 620;
const SCHEME_W = 440;
/**
 * The single-column width between the phone layout and the split.
 *
 * The whole design rests on ~60 characters per line, and an uncapped column
 * blows straight past it: at 1100px the question was setting 110 characters,
 * wider than the 80 WCAG caps at and wider than the SEC's own printed paper.
 * One column, same measure, at every width.
 */
const COLUMN = 664;

const SERIF = "'Source Serif 4', Georgia, serif";
const SANS = "'DM Sans', system-ui, sans-serif";
const MONO = "'Roboto Mono', ui-monospace, monospace";

/** How the student answered one row. */
type RowClaim = 'no' | 'yes' | 'synonym';

/** A row absent from the claims map has not been claimed. Defaulting the other
 *  way silently credits every row a caller forgot to mention. */
const isClaimed = (claims: Record<string, RowClaim>, id: string) => (claims[id] ?? 'no') !== 'no';

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
}

/* ------------------------------------------------------------- mark logic ---- */

/** Marks a row is worth when claimed. `anyN` groups count their claimable max. */
export function rowMarks(row: MarkRow): number {
  if (row.kind === 'anyN' && row.group) return row.group.claimMax * row.group.perOption;
  return row.marks ?? 0;
}

/**
 * Total marks a student can claim on this card. Falls back to the printed tariff
 * when the scheme leaves per-row values undefined.
 *
 * Mutually exclusive routes are counted ONCE. A question the scheme answers two
 * ways with a // offers both routes' rows, but a student may only take one, so
 * summing every row states a total nobody can reach — and then tells a student
 * who answered a full route perfectly that they left half the marks behind.
 */
export function claimableTotal(card: SecCard): number {
  if (card.tariffModel.kind === 'orderedSplit') return card.totalMarks;
  if (card.tariffModel.kind === 'bestNofParts') {
    return card.tariffModel.answer * card.tariffModel.perPart;
  }
  const byRoute = new Map<string, number>();
  let common = 0;
  for (const r of card.rows) {
    // A row outside every route is claimable whichever route is taken.
    if (!r.route) common += rowMarks(r);
    else byRoute.set(r.route, (byRoute.get(r.route) ?? 0) + rowMarks(r));
  }
  return common + Math.max(0, ...byRoute.values());
}

/** Only a `fixed` tariff may show per-row mark chips: for the other conventions
 *  a per-row number would be arithmetically wrong, so we show none. */
export const showsRowMarks = (card: SecCard) => card.tariffModel.kind === 'fixed';

/**
 * Which mutually exclusive answer route the student has committed to, if any.
 * The SEC's double solidus separates routes that may not be mixed.
 */
export function committedRoute(card: SecCard, claims: Record<string, RowClaim>): string | null {
  for (let i = 0; i < card.rows.length; i++) {
    const r = card.rows[i];
    if (r.route && isClaimed(claims, rowId(r, i))) return r.route;
  }
  return null;
}

export function marksClaimed(
  card: SecCard,
  claims: Record<string, RowClaim>,
  picks: Record<string, number[]> = {},
): number {
  if (!showsRowMarks(card)) return 0;
  const route = committedRoute(card, claims);
  return card.rows.reduce((n, r, i) => {
    const id = rowId(r, i);
    // Points from an abandoned route earn nothing: the scheme forbids taking a
    // partial answer from one side of a // together with one from the other.
    if (r.route && route && r.route !== route) return n;
    // A bounded "Any four 4(3)" group is scored by how many the student actually
    // had, not as one all-or-nothing block worth twelve marks.
    if (r.kind === 'anyN' && r.group) {
      const chosen = Math.min(picks[id]?.length ?? 0, r.group.claimMax);
      return n + chosen * r.group.perOption;
    }
    return isClaimed(claims, id) ? n + rowMarks(r) : n;
  }, 0);
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
  picks: Record<string, number[]> = {},
): MarkBankGrade {
  const total = claimableTotal(card);
  const got = marksClaimed(card, claims, picks);
  if (!showsRowMarks(card)) {
    const claimedRows = card.rows.filter((r, i) => isClaimed(claims, rowId(r, i))).length;
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

/**
 * Where you are in the session — three states, never two.
 *
 * Done / not-done alone reads as a score creeping up. Marking the CURRENT card
 * makes it read as position instead: this one, these behind me, those ahead. And
 * no segment is ever tinted by the GRADE it earned — that turns the rail into a
 * running scoreboard, which is the ego-involving feedback that cancels the value
 * of everything beside it.
 */
const ProgressRail: React.FC<{ total: number; done: number; current: number }> = ({ total, done, current }) => (
  <div style={{ display: 'flex', gap: 2, width: '100%' }} aria-hidden="true">
    {Array.from({ length: total }, (_, i) => (
      <div
        key={i}
        style={{
          height: 6, flex: 1,
          background: i < done ? INK : i === current ? ACCENT : '#d6d2cc',
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
  blockedReason?: string;
  reduced: boolean;
  picks: number[];
  onClaim: (id: string, next: RowClaim) => void;
  onPick: (id: string, optionIndex: number) => void;
  /** Options already claimed in a SIBLING menu on this card. */
  takenElsewhere?: ReadonlySet<string>;
}> = ({ row, id, index, claim, showMarks, blocked, blockedReason, reduced, picks, onClaim, onPick, takenElsewhere }) => {
  const claimed = claim !== 'no';
  const marks = rowMarks(row);
  const canSynonym = !row.exactTermRequired && (row.openList || row.kind === 'alt');

  // A bounded "Any four 4(3)" group. The scheme lets a student bank any four of
  // nine, so each option is claimed on its own: treating the whole group as one
  // tick makes a twelve-mark row all-or-nothing and gives a student who had two
  // of them no way to say so.
  if (row.kind === 'anyN' && row.group) {
    const g = row.group;
    const chosen = Math.min(picks.length, g.claimMax);
    const atCap = chosen >= g.claimMax;
    return (
      <MotionDiv
        /* The rows arrive one after another, and the stagger IS the message:
           these are discrete, countable things and you are going to work down
           them one at a time. They RISE rather than slide in from the side —
           a slide says "this was hidden from you". Capped at eight steps so a
           long list never drags. */
        initial={reduced ? false : { opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.14, ease: EASE, delay: reduced ? 0 : Math.min(index, 8) * 0.024 }}
        style={{
          marginBottom: 8, padding: '12px 13px', borderRadius: 12,
          border: `1.5px solid ${chosen ? SUCCESS : MUTED_BORDER}`,
          background: chosen ? SUCCESS_TINT : '#FFFFFF',
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', gap: 10, marginBottom: 9 }}>
          <span style={{ font: `600 12.5px/1.35 ${SANS}`, color: chosen ? SUCCESS_TEXT : INK_2 }}>
            Any {g.claimMax} of these — {g.perOption} marks each
          </span>
          {showMarks && (
            <span style={{
              font: `700 10.5px/1.7 ${MONO}`, borderRadius: 6, padding: '0 6px', whiteSpace: 'nowrap',
              fontVariantNumeric: 'tabular-nums',
              background: chosen ? SUCCESS_TINT : '#f2efea',
              color: chosen ? SUCCESS_TEXT : MUTED,
            }}>
              {chosen} of {g.claimMax}
            </span>
          )}
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 5 }}>
          {g.options.map((option, oi) => {
            const on = picks.includes(oi);
            // A question marked "7 + 7 + 6" for three answers is carried as one
            // menu per ANSWER POSITION, each listing everything the examiner
            // allows — the split follows the order you answered in, not which
            // item you picked. Nothing stopped the same item being ticked in
            // two of those menus, which banked one answer twice and told the
            // student they had scored marks the examiner never gave.
            const usedAlready = !on && takenElsewhere?.has(option);
            const disabled = !on && (atCap || Boolean(usedAlready));
            return (
              <button
                key={oi}
                type="button"
                onClick={() => onPick(id, oi)}
                disabled={disabled}
                aria-pressed={on}
                style={{
                  width: '100%', textAlign: 'left', display: 'grid',
                  gridTemplateColumns: '16px 1fr', gap: 8, alignItems: 'start',
                  padding: '7px 9px', borderRadius: 9,
                  border: `1px solid ${on ? SUCCESS : '#e4e0da'}`,
                  background: on ? '#FFFFFF' : 'transparent',
                  cursor: disabled ? 'not-allowed' : 'pointer',
                  opacity: disabled ? 0.45 : 1,
                  font: `500 12.5px/1.4 ${SANS}`, color: on ? SUCCESS_TEXT : INK_2,
                }}
              >
                <span style={{
                  width: 14, height: 14, borderRadius: 4, marginTop: 2, flex: 'none',
                  background: on ? SUCCESS : 'transparent',
                  border: on ? 'none' : `1.5px solid ${MUTED_BORDER}`,
                  display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
                }}>
                  {on && (
                    <svg width="9" height="9" viewBox="0 0 12 12" fill="none" aria-hidden="true">
                      <path d="M2.5 6.2l2.4 2.4L9.5 3.9" stroke="#FFFFFF" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                  )}
                </span>
                <span>
                  {option}
                  {usedAlready && (
                    <em style={{ display: 'block', marginTop: 2, font: `400 11px/1.4 ${SANS}`, color: MUTED, fontStyle: 'normal' }}>
                      Already claimed above — one answer earns marks once.
                    </em>
                  )}
                </span>
              </button>
            );
          })}
        </div>
        {/* This branch returns before the ordinary row body, so a contextNote on
            an anyN row used to reach nobody — and an author with scheme detail
            that would not fit an option put it here, believing it showed. Silent
            loss of marking content is worse than a crowded card. */}
        {row.contextNote && (
          <p style={{ margin: '8px 0 0', font: `400 11.5px/1.45 ${SANS}`, color: MUTED }}>
            {row.contextNote}
          </p>
        )}
        {atCap && (
          <p style={{ margin: '8px 0 0', font: `400 11.5px/1.4 ${SANS}`, color: MUTED }}>
            That&rsquo;s the {g.claimMax} the examiner marks — any more score nothing.
          </p>
        )}
      </MotionDiv>
    );
  }

  return (
    <MotionDiv
      /* The rows arrive one after another, and the stagger IS the message:
         these are discrete, countable things and you are going to work down
         them one at a time. They RISE rather than slide in from the side —
         a slide says "this was hidden from you". Capped at eight steps so a
         long list never drags. */
      initial={reduced ? false : { opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.14, ease: EASE, delay: reduced ? 0 : Math.min(index, 8) * 0.024 }}
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
            // A circle is a RADIO — one of many. Every marking point here is
            // claimed independently, so the control is a checkbox: rounded
            // square, not round.
            width: 18, height: 18, borderRadius: 5, marginTop: 1,
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
          {row.contextNote && (
            <span style={{ display: 'block', marginTop: 3, font: `400 12px/1.4 ${SANS}`, color: MUTED }}>
              {row.contextNote}
            </span>
          )}
        </span>

        {showMarks && (
          /* An unclaimed point is UNCLAIMED, not wrong. This chip used to open
             in the accent tint, and `claims` starts empty — so revealing a card
             greeted the student with a column of orange before they had touched
             anything. That is both an accusation and a misuse of the token:
             orange means "this is the action", never "you got this wrong". */
          <span style={{
            font: `700 10.5px/1.7 ${MONO}`, borderRadius: 6, padding: '0 6px', whiteSpace: 'nowrap',
            fontVariantNumeric: 'tabular-nums',
            background: claimed ? SUCCESS_TINT : '#f2efea',
            color: claimed ? SUCCESS_TEXT : MUTED,
          }}>
            {claimed ? `${marks}m` : `${marks}m`}
          </span>
        )}
      </button>

      {blocked && (
        <span style={{ display: 'block', marginTop: 4, marginLeft: 42, font: `400 11.5px/1.5 ${SANS}`, color: MUTED }}>
          {blockedReason ?? 'This mark only counts if the point above was right.'}
        </span>
      )}
      {canSynonym && !claimed && (
        <button
          type="button"
          onClick={() => onClaim(id, 'synonym')}
          style={{
            marginTop: 4, marginLeft: 42, background: 'none', border: 'none', padding: 0,
            font: `600 11.5px/1.5 ${SANS}`, color: INK_2,
            borderBottom: `1px solid ${MUTED_BORDER}`, cursor: 'pointer',
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

/**
 * What the letters on the diagram mean — for the ones this question does NOT ask
 * about.
 *
 * It used to print every letter, which on a labelling card meant the answer
 * appeared twice: "A — Oesophagus" as a marking point the student is asked to
 * self-mark, and then "A — Oesophagus" again in the panel directly beneath it.
 * The panel gave away the rows it sat under. It earns its place only where the
 * diagram carries letters the question leaves alone, and renders nothing when it
 * has nothing to add.
 */
const LabelKeyPanel: React.FC<{ keys: LabelKey[] }> = ({ keys }) => {
  const extra = keys.filter(k => !k.askedInThisQuestion);
  if (!extra.length) return null;
  return (
  <div style={{ marginTop: 12, padding: '11px 13px', borderRadius: 10, background: PLATE }}>
    <span style={{
      display: 'block', marginBottom: 6, font: `700 9px/1.6 ${SANS}`,
      letterSpacing: '.11em', textTransform: 'uppercase', color: LABEL,
    }}>
      Also on the diagram
    </span>
    <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
      {extra.map(k => (
        <span
          key={k.letter}
          style={{
            font: `500 12px/1.5 ${SANS}`, background: '#FFFFFF', borderRadius: 6,
            padding: '3px 9px', color: MUTED,
          }}
        >
          <strong style={{ fontFamily: MONO, fontSize: 11.5 }}>{k.letter}</strong> — {k.meaning}
        </span>
      ))}
    </div>
  </div>
  );
};


/**
 * The question, set the way the paper sets it.
 *
 * SEC papers hang their part labels — (i), (ii), (a) — in the left margin so the
 * prose of each part starts on a common line, and a student's eye can find "(ii)"
 * without reading. Run inline, as a single paragraph, the labels disappear into
 * the sentence and a two-part question reads as one long instruction.
 *
 * This splits on labels only where the paper actually printed them; a question
 * with no parts renders as one block, unchanged.
 */
const PART = /\s*(\((?:[ivx]+|[a-h])\))\s+/gi;

/**
 * Which emphasis the command clause carries.
 *
 * 'rule' is a weighted underline in the brand orange, sitting clear of the
 * descenders. 'marker' is a highlighter sweep that fills only the lower part of
 * the line.
 *
 * The rule is the default, and the deciding factor was the wrap. A fill has an
 * area, and the moment a clause runs onto a second line those two areas stack
 * into a block — the slab this whole file is written to avoid — so the marker
 * only ever looks right on clauses that happen to fit one line, and no clause
 * splitter can promise that at every viewport width. A rule has no area: two
 * lines of it read as two underlines, which is what an underline is supposed to
 * look like. It degrades instead of breaking.
 *
 * Orange, not yellow. The accent means "this is the instruction, this is what
 * you are being asked to do", which is exactly the job here — and it can never
 * be misread as "correct", because it is printed on the question, before the
 * student has seen a marking scheme or claimed a single mark.
 */
export type Emphasis = 'marker' | 'rule';
export const EMPHASIS: Emphasis = 'rule';

/** Warm yellow. Behind black serif it keeps contrast where orange muddies it. */
const MARKER = 'rgba(247, 201, 72, 0.55)';

const MARKER_STYLE: React.CSSProperties = {
  // An inset shadow rather than a gradient: 0.4em of ink laid along the bottom
  // of the line box, so the sweep sits under the x-height instead of boxing the
  // whole line. A gradient would do the same job, but this file is guarded
  // against gradients — a rule worth keeping, since the one place a gradient is
  // defensible is not worth the exception that lets the next one in.
  boxShadow: `inset 0 -0.4em 0 ${MARKER}`,
  // The 0.1em bleed past each end is what stops it reading as a rectangle, and
  // `clone` gives a wrapped clause a sweep per line rather than one long band.
  padding: '0 0.1em',
  boxDecorationBreak: 'clone',
  WebkitBoxDecorationBreak: 'clone',
};

const RULE_STYLE: React.CSSProperties = {
  // text-decoration, not a background gradient. A gradient on an inline box is
  // painted ONCE across all of its line fragments, so the earlier gradient rule
  // underlined a wrapped clause's first line and left the second bare. The
  // decoration is drawn per line by the text engine, at a position the font
  // itself declares — which is also why it stays right at any size.
  textDecorationLine: 'underline',
  textDecorationColor: ACCENT,
  // Heavy enough to read as drawn rather than as a hyperlink, light enough that
  // it never competes with the 20px serif above it.
  textDecorationThickness: '2.5px',
  // Below the descenders, and NOT skipping ink around them: a rule with notches
  // cut out of it for every g and y reads as an artefact. 0.28em is measured,
  // not guessed — at 0.18em the rule grazed the tails of Source Serif's g, p and
  // y, and by 0.32em it had come loose from the words it belongs to.
  textUnderlineOffset: '0.28em',
  textDecorationSkipInk: 'none',
};

/**
 * The command clause, emphasised. Everything around it — the method and the
 * scope — stays plain, which is what keeps the mark sleek on a question that
 * runs to two or three lines.
 */
const Clause: React.FC<{ text: string }> = ({ text }) => {
  const { before, marked, after } = splitForEmphasis(text);
  return (
    <>
      {before}
      <span style={EMPHASIS === 'rule' ? RULE_STYLE : MARKER_STYLE}>{marked}</span>
      {after}
    </>
  );
};

const QuestionText: React.FC<{ text: string }> = ({ text }) => {
  const pieces = text.split(PART).filter(s => s !== undefined && s !== '');
  // No label at the head means no hanging: one block, as before.
  if (pieces.length < 3 || !/^\([ivx]+\)$|^\([a-h]\)$/i.test(pieces[0])) {
    return (
      <p style={{ margin: '9px 0 0', font: `500 20px/1.5 ${SERIF}`, color: INK }}>
        <Clause text={text} />
      </p>
    );
  }
  const parts: { label: string; body: string }[] = [];
  for (let i = 0; i < pieces.length - 1; i += 2) {
    parts.push({ label: pieces[i], body: (pieces[i + 1] ?? '').trim() });
  }
  return (
    <div style={{ margin: '9px 0 0' }}>
      {parts.map(part => (
        <p
          key={part.label}
          style={{
            display: 'flex', gap: 12, margin: '0 0 8px',
            font: `500 20px/1.5 ${SERIF}`, color: INK,
          }}
        >
          <span style={{
            flex: '0 0 34px', font: `500 15px/1.95 ${MONO}`, color: MUTED,
          }}>
            {part.label}
          </span>
          <span><Clause text={part.body} /></span>
        </p>
      ))}
    </div>
  );
};

/* ------------------------------------------------------------ the screen ---- */

const GRADE_COPY: Record<MarkBankGrade, string> = {
  missed: 'Missed it',
  shaky: 'Shaky',
  got: 'Got it',
};

/**
 * The two-pane threshold.
 *
 * 620 question + 32 gutter + 440 scheme + margins does not fit honestly below
 * this, and the phone layout below it is correct and shipping — so there are
 * three layouts, not a fluid one: phone, single column with a sticky question,
 * and the split. Android puts multi-pane at 1200dp for the same arithmetic.
 */
const TWO_PANE = 1200;

const useTwoPane = () => {
  const [wide, setWide] = useState(
    () => typeof window !== 'undefined' && window.matchMedia(`(min-width: ${TWO_PANE}px)`).matches,
  );
  useEffect(() => {
    const mq = window.matchMedia(`(min-width: ${TWO_PANE}px)`);
    const onChange = (e: MediaQueryListEvent) => setWide(e.matches);
    mq.addEventListener('change', onChange);
    return () => mq.removeEventListener('change', onChange);
  }, []);
  return wide;
};

const SessionScreen: React.FC<SessionScreenProps> = ({
  cards, subjectLabel, onGrade, onExit, onFinish,
}) => {
  const reduced = useReducedMotion() ?? false;
  const wide = useTwoPane();
  const [queue, setQueue] = useState(() => cards.map(c => c.id));
  const [position, setPosition] = useState(0);
  const [revealed, setRevealed] = useState(false);
  const [claims, setClaims] = useState<Record<string, RowClaim>>({});
  const [picks, setPicks] = useState<Record<string, number[]>>({});
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
  const got = card ? marksClaimed(card, rowClaims, picks) : 0;
  const left = Math.max(0, total - got);

  /**
   * What the student has not ticked, named rather than counted.
   *
   * "You left 6 marks behind" makes the student the subject of a failure verb.
   * The same six marks listed as "cohesion · root pressure" is task-focused, and
   * doubles as the revision list for the card they are about to grade. Rows on a
   * route they did not take are excluded — those marks were never theirs to get.
   */
  const unclaimed = useMemo(() => {
    if (!card) return [];
    const route = committedRoute(card, rowClaims);
    return card.rows
      .filter((r, i) => {
        if (r.route && route && r.route !== route) return false;
        // An anyN group is partially claimable, so it is never simply "unclaimed".
        if (r.kind === 'anyN') return false;
        return (rowClaims[rowId(r, i)] ?? 'no') === 'no';
      })
      // The scheme's own wording, minus any "Label — " prefix the card carries.
      // Except on a matching or true/false card, where the scheme's whole answer
      // IS the prefix's tail — a letter or a verdict. "e · a · d" and
      // "false · false · false" name nothing; there the label is the content.
      .map(r => {
        const tail = r.verbatim.split(/\s[—-]\s/).pop() ?? r.verbatim;
        return (tail.trim().length <= 6 ? r.verbatim : tail).toLowerCase();
      });
  }, [card, rowClaims]);
  /* Three names fit the band; beyond that the count carries it. Naming all six
     would wrap the bar and push the grade buttons around. */
  const unclaimedNames = unclaimed.slice(0, 3);
  const unclaimedMore = unclaimed.length - unclaimedNames.length;
  const suggested = card ? suggestGrade(card, rowClaims, picks) : 'shaky';
  const routeTaken = card ? committedRoute(card, rowClaims) : null;

  const setClaim = useCallback((id: string, next: RowClaim) => {
    setClaims(prev => ({ ...prev, [id]: next }));
  }, []);

  /**
   * Options already claimed in some OTHER menu on this card, per row.
   *
   * Only meaningful where a card carries several menus over the SAME list — the
   * "7 + 7 + 6 across three answers" shape. One answer earns marks once, so an
   * item ticked in the first menu must not still be tickable in the second.
   */
  const takenByRow = useMemo(() => {
    const out: Record<string, Set<string>> = {};
    if (!card) return out;
    const menus = card.rows
      .map((r, i) => ({ r, id: rowId(r, i) }))
      .filter(({ r }) => r.kind === 'anyN' && r.group);
    for (const { id } of menus) out[id] = new Set<string>();
    for (const { r, id } of menus) {
      for (const oi of picks[id] ?? []) {
        const option = r.group!.options[oi];
        if (option === undefined) continue;
        for (const other of menus) if (other.id !== id) out[other.id].add(option);
      }
    }
    return out;
  }, [card, picks]);

  /** Toggle one option inside a bounded "Any N" group. */
  const togglePick = useCallback((id: string, optionIndex: number) => {
    setPicks(prev => {
      const current = prev[id] ?? [];
      const next = current.includes(optionIndex)
        ? current.filter(i => i !== optionIndex)
        : [...current, optionIndex];
      return { ...prev, [id]: next };
    });
  }, []);

  const claimAll = useCallback(() => {
    if (!card) return;
    const all: Record<string, RowClaim> = {};
    const allPicks: Record<string, number[]> = {};
    card.rows.forEach((r, i) => {
      const id = rowId(r, i);
      all[id] = 'yes';
      if (r.kind === 'anyN' && r.group) {
        allPicks[id] = Array.from({ length: r.group.claimMax }, (_, k) => k);
      }
    });
    setClaims(prev => ({ ...prev, ...all }));
    setPicks(prev => ({ ...prev, ...allPicks }));
  }, [card]);

  const commit = useCallback((grade: MarkBankGrade) => {
    if (!card) return;
    const result: SessionCardResult = {
      cardId: card.id, grade,
      marksClaimed: got,
      // Where the scheme leaves per-row values undefined we score no marks, so
      // we must not report a total either — otherwise the close screen reads
      // "0 of 20 marks" for a card the student may have answered perfectly.
      marksAvailable: showsRowMarks(card) ? total : 0,
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
    // presentations exceeds the session size while the number of DISTINCT cards
    // does not. The session simply ends when the queue runs out — an earlier
    // "finished" heuristic discarded the re-queued card unless it was last, which
    // silently broke the one mechanic that makes a missed card come back.
    const nextQueue = grade === 'missed' ? [...queue, card.id] : queue;

    setQueue(nextQueue);
    setClaims({});
    setPicks({});
    setRevealed(false);

    if (position + 1 >= nextQueue.length) onFinish(nextResults);
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

  const banked = results.reduce((n, r) => n + r.marksClaimed, 0);

  /* PORTALLED TO THE BODY, and that is load-bearing rather than tidiness. The
     tool renders inside `<main class="relative z-10">`, which opens a stacking
     context — so a z-index of 70 on a descendant is resolved INSIDE that context
     and still loses to the app header's z-60. The takeover appeared correctly in
     the DOM and rendered underneath the header. Portalling escapes the context. */
  return createPortal(
    /* A full-viewport takeover, not a page inside the tool shell. Review is one
       task with one action, and every mature reviewer treats it that way — Anki
       ships a fullscreen mode, RemNote drops its sidebar, Mochi dims the app.
       Sitting inside the shell means the app's own header competes with the exam
       question for the top of the screen, and loses the student ~150px of it. */
    /* NO entrance fade on this element. It is the whole screen, and an opacity
       animation here restarts on every re-render of the session — the tool was
       measured sitting at opacity 0.2 four seconds after opening. A decorative
       fade whose failure mode is an invisible tool is not worth having; the
       transitions that earn their place are inside, where a stall costs one card
       rather than everything. */
    <div style={{
      /* Above the app's own z-100 chrome overlay. During a review the points
         chip and notification bell are exactly what should step aside — and the
         points chip is doubly wrong here, since Mark Bank is deliberately exempt
         from the points system. */
      position: 'fixed', inset: 0, zIndex: 120,
      background: PAPER, fontFamily: SANS,
      overflowY: 'auto', overscrollBehavior: 'contain',
      paddingBottom: 'calc(112px + var(--sab, 0px))',
    }}>
      {/* Session bar. Full-bleed, so the work surface below reads as contained
          by a declared edge rather than adrift in a wide window. */}
      <div style={{
        position: 'sticky', top: 0, zIndex: 3,
        background: '#FFFFFF', borderBottom: `2px solid ${INK}`,
      }}>
        <div style={{
          maxWidth: wide ? SURFACE : COLUMN, margin: '0 auto', padding: '0 16px',
          height: 56, display: 'flex', alignItems: 'center', gap: 16,
        }}>
          <button
            type="button" onClick={onExit}
            style={{
              display: 'flex', alignItems: 'center', gap: 6,
              background: 'none', border: 'none', padding: '4px 2px', cursor: 'pointer',
              color: INK, font: `600 13px/1.5 ${SANS}`,
            }}
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <path d="M15 18l-6-6 6-6" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
            Leave
          </button>

          {/* One line where four stacked headings used to be. */}
          <span style={{
            // 1.5, not 1: a line box the same height as the type clips every
            // descender, and `overflow: hidden` — needed for the ellipsis —
            // turns that clip into a straight cut through the g's.
            font: `400 13px/1.5 ${SANS}`, color: MUTED,
            overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
            flexShrink: 0,
          }}>
            {subjectLabel} · {card.level === 'higher' ? 'Higher' : 'Ordinary'}
          </span>

          <span style={{ flex: 1 }} />

          <span style={{
            font: `700 12.5px/1.5 ${MONO}`, color: MUTED,
            fontVariantNumeric: 'tabular-nums', whiteSpace: 'nowrap',
          }}>
            Card {Math.min(distinctDone + 1, cards.length)} of {cards.length}
          </span>
          {banked > 0 && (
            <span style={{
              font: `700 12.5px/1.5 ${MONO}`, color: SUCCESS_TEXT,
              fontVariantNumeric: 'tabular-nums', whiteSpace: 'nowrap',
            }}>
              {banked} banked
            </span>
          )}
        </div>
        <ProgressRail total={cards.length} done={distinctDone} current={distinctDone} />
      </div>

      {/* The work surface. Two panes from the FIRST frame, never assembled at the
          moment of reveal — re-laying out exactly when the student starts reading
          evidence is the worst possible time to move anything. */}
      {/* Keyed, but NOT inside an AnimatePresence: `mode="wait"` holds the next
          question back until the old one has finished leaving, which adds a third
          of a second to every card in a twelve-card sitting. Re-keying alone
          re-runs `initial -> animate`, so the new card fades up immediately while
          the panes below ease to their new heights.

          Opacity ONLY. A y-offset leaves a transform on this element, and a
          transformed ancestor becomes the containing block for position:sticky —
          which would silently kill the sticky question pane inside it. */}
      <div
        key={card.id}
        className="mb-card-in"
        style={{
          maxWidth: wide ? SURFACE : COLUMN, margin: '0 auto', padding: '34px 16px 0',
          display: 'flex', alignItems: 'flex-start',
          gap: wide ? 32 : 0, flexDirection: wide ? 'row' : 'column',
        }}
      >
      <div style={{
        width: wide ? QUESTION_W : '100%',
        maxWidth: '100%',
        flex: '0 0 auto',
        // Stays put while the marking points scroll beneath it: the exact wording
        // is the evidence a student marks against, so it must never leave view.
        position: wide ? 'sticky' : 'static', top: 96,
      }}>
        {/* The question card is built like the top of a small stack of
            papers: the white sheet with its ink border, and behind it two
            flat accent sheets of the SAME SIZE, offset on opposite diagonals
            — one up-left, one down-right. Each shows only the L-shaped band
            the card leaves uncovered, so every visible edge either hugs the
            card or ends in a square cut where a real sheet's corner would
            be; nothing terminates in mid-air. Both layers are filled bands
            of identical weight and colour — siblings — because a hairline
            paired with a slab reads as two unrelated marks, not a stack.

            The colour is a flat white-mixed tint of the accent, not full
            #F26B1F: on this light page a full-strength band out-shouts the
            question text, which is the actual content. The geometry carries
            the depth; the tint keeps the frame subordinate. (A concentric
            ring at an even gap is not an alternative — it reads as a focus
            state.)

            Square corners are deliberate and load-bearing. Where an offset
            layer disappears behind the sheet, a straight edge cuts it cleanly —
            at a rounded corner the same stroke emerges mid-curve as a stub and
            reads as a fault. The rest of the screen keeps the system's 14–18px
            radii; this card alone is squared, because it is the one element
            that IS a printed exam paper. */}
        <div style={{ position: 'relative' }}>
          <div
            aria-hidden
            style={{
              position: 'absolute', inset: '8px -8px -8px 8px',
              background: ACCENT_SHEET, pointerEvents: 'none',
            }}
          />
          {FRAME === 'stack' ? (
            <div
              aria-hidden
              style={{
                position: 'absolute', inset: '-8px 8px 8px -8px',
                background: ACCENT_SHEET, pointerEvents: 'none',
              }}
            />
          ) : (
            /* 'registration': the up-left layer is a crisp full-accent stroke
               rather than a second tinted sheet — the founder's reference pairs
               a thin stroke with a mass.

               Four bars, not a bordered box, for two reasons. The design guard
               in test/markBankSession.test.tsx forbids coloured left borders in
               this file, and separate bars let each arm stop exactly where it
               should.

               The two long arms run the full width and height of the card, and
               each one TURNS onto the card at its far end — the top arm drops
               FRAME_OFFSET down onto the card's top edge, the left arm runs
               FRAME_OFFSET right onto its left edge. Without those turns the
               arms simply stopped in space and the frame read as a rectangle
               someone had failed to finish. With them the stroke closes onto
               the sheet, so it reads as a register mark tucked behind the
               paper rather than as an unfinished outline. */
            <>
              <div
                aria-hidden
                style={{
                  ...ACCENT_BAR,
                  top: -FRAME_OFFSET, left: -FRAME_OFFSET, right: 0, height: STROKE,
                }}
              />
              <div
                aria-hidden
                style={{
                  ...ACCENT_BAR,
                  top: -FRAME_OFFSET, right: 0, width: STROKE, height: FRAME_OFFSET,
                }}
              />
              <div
                aria-hidden
                style={{
                  ...ACCENT_BAR,
                  top: -FRAME_OFFSET, left: -FRAME_OFFSET, bottom: 0, width: STROKE,
                }}
              />
              <div
                aria-hidden
                style={{
                  ...ACCENT_BAR,
                  bottom: 0, left: -FRAME_OFFSET, width: FRAME_OFFSET, height: STROKE,
                }}
              />
            </>
          )}
        <MotionDiv
          layout={reduced ? false : true}
          transition={{ duration: 0.26, ease: EASE }}
          style={{
            position: 'relative',
            background: '#FFFFFF', overflow: 'hidden', border: `2px solid ${INK}`,
          }}
        >
          <div style={{ padding: '16px 18px 18px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', gap: 10 }}>
              <span style={{
                font: `700 9.5px/1.5 ${SANS}`, letterSpacing: '.11em',
                textTransform: 'uppercase', color: LABEL,
              }}>
                {subjectLabel} · {levelLabel} · {card.year} · {card.questionRef.replace(/^\d{4}\s+(HL|OL)\s+/, '')}
              </span>
              <span style={{
                font: `700 11.5px/1 ${MONO}`, background: INK, color: '#FFFFFF',
                borderRadius: 6, padding: '5px 8px', fontVariantNumeric: 'tabular-nums', whiteSpace: 'nowrap',
              }}>
                {card.totalMarks}m
              </span>
            </div>

            {card.stem && (
              <p style={{ margin: '10px 0 0', font: `400 14.5px/1.6 ${SANS}`, color: INK_2 }}>{card.stem}</p>
            )}

            <QuestionText text={card.questionText} />

            {figure && (
              /* The crop sits directly on the sheet — no third box competing
                 with the card's own border. A full-bleed hairline rule marks
                 where our typesetting ends and the SEC's print begins. */
              <figure style={{ margin: '16px -18px 0', padding: '14px 18px 0', borderTop: `1px solid ${HAIRLINE_2}` }}>
                <div style={{ textAlign: 'center' }}>
                  <img
                    src={figureUrl(figure.src)} alt={figure.alt}
                    style={{ maxWidth: '100%', maxHeight: 340, objectFit: 'contain', display: 'inline-block' }}
                  />
                </div>
                <figcaption style={{ marginTop: 8, font: `400 10.5px/1.4 ${SANS}`, color: LABEL }}>
                  {figure.attribution}
                </figcaption>
              </figure>
            )}
          </div>
        </MotionDiv>
        </div>
      </div>

      {/* The scheme pane. Present from the first frame so nothing moves on
          reveal — before it, it holds the tariff and the instruction; after, the
          marking points themselves. */}
      <div style={{
        width: wide ? SCHEME_W : '100%',
        maxWidth: '100%',
        flex: '0 0 auto',
        /* 14px of visible gap: the question card's accent plate reaches 8px
           below its sheet, so the margin allows for it in single-column mode. */
        marginTop: wide ? 0 : 22,
      }}>
        <MotionDiv
          /* The pane still grows from the prompt to the marking points within a
             single card; `layout` eases that instead of snapping to the new size. */
          layout={reduced ? false : true}
          transition={{ duration: 0.26, ease: EASE }}
          style={{ background: '#FFFFFF', borderRadius: 18, overflow: 'hidden', border: `2px solid ${INK}` }}
        >
          {!revealed && (
            <div style={{ padding: '16px 18px 18px' }}>
              <span style={{
                display: 'block', marginBottom: 9,
                font: `700 9.5px/1.5 ${SANS}`, letterSpacing: '.12em',
                textTransform: 'uppercase', color: LABEL,
              }}>
                The scheme
              </span>
              <p style={{ margin: '0 0 4px', font: `italic 400 13px/1.5 ${SANS}`, color: MUTED }}>
                Answer it in your head, or write it out. Then reveal the scheme and
                tick off what you had.
              </p>
            </div>
          )}

          <AnimatePresence>
            {revealed && (
              <MotionDiv
                key="scheme"
                initial={reduced ? { opacity: 0 } : { opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                transition={{ duration: reduced ? 0.12 : 0.18, ease: EASE }}
              >
                <div style={{ padding: '4px 18px 18px' }}>
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
                        font: `600 11.5px/1.5 ${SANS}`, color: INK_2,
                        borderBottom: `1px solid ${MUTED_BORDER}`,
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
                        blocked={
                          (!!row.dependsOn && claimOf(row.dependsOn) === 'no')
                          || (!!row.route && !!routeTaken && row.route !== routeTaken)
                        }
                        blockedReason={
                          !!row.route && !!routeTaken && row.route !== routeTaken
                            ? 'The examiner marks one route or the other — not a mix of both.'
                            : undefined
                        }
                        reduced={reduced}
                        picks={picks[id] ?? []}
                        takenElsewhere={takenByRow[id]}
                        onClaim={setClaim}
                        onPick={togglePick}
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
        </MotionDiv>
      </div>
      </div>

      {/* The interval whisper lives OUTSIDE the grade bar on purpose. Grading
          advances the card and closes the scheme, so anything rendered inside
          the bar unmounts at exactly the moment it has something to say — the
          message would only ever be seen by a student who tapped through fast
          enough to keep the bar alive. The schedule speaks on its own surface. */}
      {/* ONE bottom rail, not three fixed siblings competing for bottom: 0.
          The whisper STACKS above the action rather than replacing it — an
          earlier arrangement suppressed the reveal button for the 1.1s the
          whisper was on screen, so the next card briefly had no way in. */}
      <div style={{
        position: 'fixed', left: 0, right: 0, bottom: 0, zIndex: 2,
        background: '#FFFFFF', borderTop: `2px solid ${INK}`,
      }}>
        {/* A plain element with a CSS fade, for the same reason as the card: an
            animated HEIGHT that stalls leaves the sentence sliced in half by the
            rail's edge, which is exactly what it did. It appears when the
            schedule has something to say and disappears when the timer clears
            it — no exit animation to get stuck partway. */}
        {whisper && (
          <p
            key={whisper}
            className="mb-card-in"
            style={{
              maxWidth: wide ? SURFACE : COLUMN, margin: '0 auto', padding: '12px 16px 0',
              font: `500 13.5px/1.45 ${SANS}`, color: SUCCESS_TEXT,
            }}
          >
            {whisper}
          </p>
        )}

        {/* The action. Reveal and grade occupy the same band, so nothing shifts
            at the moment the student's attention moves to the marking points. */}
        {!revealed && (
          <div style={{ padding: `16px 16px calc(16px + var(--sab, 0px))` }}>
            <div style={{ maxWidth: wide ? SURFACE : COLUMN, margin: '0 auto' }}>
              <button
                type="button"
                autoFocus
                // Clear any lingering whisper so the schedule note for the card
                // just graded does not hang over the one now in front of them.
                onClick={() => { setWhisper(null); setRevealed(true); }}
                style={{
                  width: '100%', padding: '15px 18px', borderRadius: 100,
                  background: ACCENT, color: '#FFFFFF', border: 'none',
                  borderBottom: '3px solid #B54D14', boxShadow: '0 4px 0 #B54D14',
                  font: `650 15px/1 ${SANS}`, cursor: 'pointer',
                }}
              >
                Reveal the marking scheme
              </button>
            </div>
          </div>
        )}

      {/* Grade bar. Solid white, never translucent — blurred glass over a
          saturated colour goes muddy and reads as generated UI. */}
      {revealed && (
        <div style={{ padding: `12px 16px calc(12px + var(--sab, 0px))` }}>
          <div style={{ maxWidth: wide ? SURFACE : COLUMN, margin: '0 auto' }}>
            {showsRowMarks(card) && (
              /* Never "you left 6 marks behind". Same information, but the
                 student is not the subject of a failure verb — and naming the
                 points turns the tally into a revision list instead of a
                 verdict. An unclaimed point is neutral, so this band is too. */
              <div style={{
                marginBottom: 10, padding: '8px 11px', borderRadius: 10,
                background: left === 0 ? SUCCESS_TINT : '#f2efea',
                color: left === 0 ? SUCCESS_TEXT : INK_2,
                font: `500 12px/1.5 ${SANS}`,
              }}>
                {left === 0 ? (
                  <span style={{
                    font: `700 9.5px/1.5 ${SANS}`, letterSpacing: '.11em', textTransform: 'uppercase',
                  }}>
                    All {total} marks. Nothing left behind.
                  </span>
                ) : (
                  <>
                    <span style={{ color: MUTED }}>Not claimed yet · </span>
                    <span style={{ font: `700 13px/1 ${MONO}`, fontVariantNumeric: 'tabular-nums' }}>
                      <Tally value={left} reduced={reduced} />
                    </span>
                    <span style={{ color: MUTED }}>{left === 1 ? ' mark' : ' marks'}</span>
                    {unclaimedNames.length > 0 && (
                      <>
                        {' · '}
                        {unclaimedNames.join(' · ')}
                        {unclaimedMore > 0 && <span style={{ color: MUTED }}> and {unclaimedMore} more</span>}
                      </>
                    )}
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
                  {/* Capped and left-aligned under the copy that explains them.
                      Stretching three two-word labels across 1092px gives each a
                      360px hit area and makes the rail read as a toolbar. */}
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, minmax(0, 168px))', gap: 8 }}>
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
    </div>,
    document.body,
  );
};

export default SessionScreen;
