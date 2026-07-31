/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Mark Bank — the tool.
 *
 * Screen flow: the Bank (home) → a topic board → a review session → the session
 * close. The session screen itself lives in SessionScreen.tsx; this is the shell
 * that gets a student to it and reports back afterwards.
 *
 * Progress is measured in MARKS, never a percentage and never a grade. Marks are
 * external and awarded by an examiner, so no progress statement here can be read
 * as a verdict on the student. "Marks secure" counts the marks on cards the
 * scheduler still predicts you would recall — so it moves as time passes and
 * degrades gently rather than snapping to zero.
 *
 * Deliberately absent: streaks, points, XP, badges, leaderboards, and any count
 * of what is "overdue". A student who lost a week to a chaotic fortnight should
 * open this and find it forgiving, not accusatory.
 */

import React, { useCallback, useEffect, useMemo, useState } from 'react';
import SessionScreen, { type SessionCardResult } from './SessionScreen';
import {
  NEW_CARD, dueAt, grade as gradeCard, intervalWords,
  isDue, planSession, retentionFor, retrievability,
} from './scheduler';
import { SUBJECTS, builtDecks, cardsForTopic, deckSize, loadCards, strandsFor, topicMarks, type Level } from './deck';
import {
  commitReview, ensureDeck, fetchDeck, mergeDecks, readChoice, readLocal,
  writeChoice, writeLocal, type DeckState,
} from './store';
import type { SecCard } from '../../types/markBank';

const SESSION_SIZE = 12;

const INK = '#1a1a1a';
const INK_2 = '#3a3530';
const MUTED = '#7a7068';
const LABEL = '#9e9186';
const MUTED_BORDER = '#d0cdc8';
const SUCCESS = '#3A8D5F';
const SUCCESS_TEXT = '#1F5F3E';

const SERIF = "'Source Serif 4', Georgia, serif";
const SANS = "'DM Sans', system-ui, sans-serif";
const MONO = "'Roboto Mono', ui-monospace, monospace";

/** Accent means "this is the action / do this now". Never "correct". */
const ACCENT = '#F26B1F';
const HAIRLINE = '#ece9e4';

/* One work surface for the whole tool, at every window width above the split.
   280 rail + 32 gutter + 780 list. It never grows: at 1920px the margins are
   414px and that is correct — filling a wide window with rails is the instinct
   that produced the layout this replaces. */
const SURFACE = 1092;
const RAIL = 280;
const GUTTER = 32;
const LIST = 780;
const TWO_PANE = 1200;
/** Single-column width between the phone layout and the rail-plus-list split. */
const COLUMN = 664;

type Screen =
  | { name: 'board' }
  | { name: 'session'; cards: SecCard[]; topicId?: string }
  | { name: 'close'; results: SessionCardResult[]; topicId?: string };

export interface MarkBankProps {
  uid?: string;
  /** Injected for tests. */
  now?: () => number;
}

/* ------------------------------------------------------------------ bits ---- */

const Eyebrow: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <span style={{
    font: `700 9.5px/1.5 ${SANS}`, letterSpacing: '.13em',
    textTransform: 'uppercase', color: LABEL,
  }}>{children}</span>
);

/**
 * A pill of mutually exclusive choices.
 *
 * An option with no cards behind it stays selectable and says so, rather than
 * being hidden or disabled: a student looking for Chemistry needs to see that it
 * exists and is being written, not to wonder whether the tool has it at all.
 */
const Segment: React.FC<{
  options: { value: string; label: string; empty?: boolean }[];
  value: string;
  onChange: (value: string) => void;
}> = ({ options, value, onChange }) => (
  <div style={{ display: 'inline-flex', background: '#fff', border: `2px solid ${INK}`, borderRadius: 100, padding: 3 }}>
    {options.map(o => {
      const on = o.value === value;
      return (
        <button
          key={o.value} type="button" onClick={() => onChange(o.value)}
          aria-pressed={on}
          style={{
            display: 'flex', alignItems: 'center', gap: 5,
            padding: '7px 16px', borderRadius: 100, border: 'none', cursor: 'pointer',
            background: on ? INK : 'transparent',
            color: on ? '#fff' : MUTED, font: `600 12.5px/1 ${SANS}`,
          }}
        >
          {o.label}
          {o.empty && (
            <span
              aria-hidden
              title="No cards yet"
              style={{
                width: 5, height: 5, borderRadius: '50%',
                background: on ? 'rgba(255,255,255,.55)' : MUTED_BORDER,
              }}
            />
          )}
        </button>
      );
    })}
  </div>
);

/** Rail-plus-list above this, single column below. Same threshold as the review
 *  screen's split, so the tool changes shape once rather than twice. */
const useWide = () => {
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

/** Three-zone bar: secure, met-but-fading, not yet met. Never a percentage. */
const MarkBar: React.FC<{ secure: number; met: number; total: number }> = ({ secure, met, total }) => {
  const pct = (n: number) => (total > 0 ? Math.min(100, (n / total) * 100) : 0);
  return (
    <div style={{ height: 6, borderRadius: 4, background: '#e4e1dc', overflow: 'hidden', display: 'flex' }}>
      <div style={{ width: `${pct(secure)}%`, background: SUCCESS }} />
      <div style={{ width: `${pct(Math.max(0, met - secure))}%`, background: SUCCESS, opacity: 0.35 }} />
    </div>
  );
};

/* ------------------------------------------------------------------ tool ---- */

const MarkBank: React.FC<MarkBankProps> = ({ uid, now = () => Date.now() }) => {
  /* Read synchronously on mount. A Chemistry Ordinary student must never watch
     the tool open on Biology Higher and correct it — that is two clicks every
     session, forever. */
  const saved = useMemo(() => readChoice(uid), [uid]);
  const [subjectId, setSubjectId] = useState<string>(saved?.subjectId ?? SUBJECTS[0].id);
  const [level, setLevel] = useState<Level>(saved?.level ?? 'higher');
  const chooseSubject = useCallback((id: string) => {
    setSubjectId(id);
    writeChoice(uid, { subjectId: id, level });
  }, [uid, level]);
  const chooseLevel = useCallback((l: Level) => {
    setLevel(l);
    writeChoice(uid, { subjectId, level: l });
  }, [uid, subjectId]);
  const wide = useWide();
  const subject = SUBJECTS.find(s => s.id === subjectId) ?? SUBJECTS[0];
  // One deck per subject AND level, so a student's Biology work is untouched by
  // anything they do in Chemistry, and dropping a level never disturbs either.
  const deckId = `${subjectId}-${level}`;
  const [deck, setDeck] = useState<DeckState>(() => readLocal(uid, deckId));
  const [screen, setScreen] = useState<Screen>({ name: 'board' });
  const [loaded, setLoaded] = useState(false);

  // Seed FRESH from Firestore on mount — never from the app-start progress
  // snapshot, which is what makes other tools lose state saved this session.
  useEffect(() => {
    let cancelled = false;
    setLoaded(false);
    setDeck(readLocal(uid, deckId));
    // The deck document must exist before any per-card updateDoc: updateDoc
    // fails on a missing document, and those writes are fired and never awaited,
    // so without this every single review was silently lost.
    ensureDeck(uid, deckId, Date.now());
    fetchDeck(uid, deckId).then(remote => {
      if (cancelled) return;
      // Re-read rather than closing over the snapshot taken before the fetch —
      // a grade made while the read was in flight would otherwise be overwritten.
      const merged = mergeDecks(readLocal(uid, deckId), remote);
      writeLocal(uid, deckId, merged);
      setDeck(merged);
      setLoaded(true);
    });
    return () => { cancelled = true; };
  }, [uid, deckId]);

  // Cards for the current level only, fetched on demand so a student never
  // downloads the level they are not sitting.
  const [cards, setCards] = useState<SecCard[]>([]);
  const [cardsLoading, setCardsLoading] = useState(true);
  useEffect(() => {
    let cancelled = false;
    setCardsLoading(true);
    loadCards(subjectId, level).then(loaded => {
      if (cancelled) return;
      setCards(loaded);
      setCardsLoading(false);
    });
    return () => { cancelled = true; };
  }, [subjectId, level]);

  const levelUnbuilt = !cardsLoading && cards.length === 0;
  const memories = deck.cards;
  const retention = retentionFor(now(), deck.examTs);

  const dueIds = useMemo(
    () => cards.filter(c => {
      const m = memories[c.id];
      return m && m.last ? isDue(c.id, m, now(), retention) : false;
    }).map(c => c.id),
    [cards, memories, retention, now],
  );

  /**
   * Marks on cards the scheduler predicts the student would still recall
   * TOMORROW, and only for cards that have graduated out of learning.
   *
   * Measuring at this instant is meaningless: retrievability at zero elapsed time
   * is exactly 1 whatever the stability, so a card graded "Missed it" counted its
   * full marks as secure the moment it was failed.
   */
  const marksSecure = useCallback((subset: SecCard[]) =>
    subset.reduce((n, c) => {
      const m = memories[c.id];
      if (!m?.last || m.state !== 2) return n;
      return retrievability(m, now() + 86_400_000) >= 0.9 ? n + c.totalMarks : n;
    }, 0), [memories, now]);

  const marksMet = useCallback((subset: SecCard[]) =>
    subset.reduce((n, c) => (memories[c.id]?.last ? n + c.totalMarks : n), 0), [memories]);
  const examYears = useMemo(() => {
    const years = [...new Set(cards.map(c => c.year))].sort();
    if (!years.length) return '';
    return years.length === 1 ? `${years[0]}` : `${years[0]}\u2013${years[years.length - 1]}`;
  }, [cards]);

  const startSession = (topicId?: string) => {
    const pool = topicId ? cards.filter(c => c.topicId === topicId) : cards;
    if (!pool.length) return;
    const plan = planSession(pool.map(c => c.id), memories, now(), { size: SESSION_SIZE, examTs: deck.examTs });
    let queue = plan.queue.map(id => pool.find(c => c.id === id)).filter(Boolean) as SecCard[];
    // Nothing due and nothing new does NOT mean "do nothing". A student who taps
    // a topic, or "Another twelve" at the end of a session, is asking to practise
    // — so serve the weakest cards they have already met rather than silently
    // ignoring the tap.
    if (!queue.length) {
      queue = [...pool]
        .sort((a, b) => retrievability(memories[a.id] ?? NEW_CARD, now()) - retrievability(memories[b.id] ?? NEW_CARD, now()))
        .slice(0, SESSION_SIZE);
    }
    if (!queue.length) return;
    setScreen({ name: 'session', cards: queue, topicId });
  };

  const handleGrade = useCallback((r: SessionCardResult): string => {
    const t = now();
    const before = memories[r.cardId] ?? NEW_CARD;
    const after = gradeCard(before, r.grade, t, retention);
    setDeck(commitReview(uid, deckId, r.cardId, after, t));
    return intervalWords(r.cardId, after, t, retention);
  }, [memories, uid, deckId, retention, now]);

  /* ------------------------------------------------------------ session ---- */

  if (screen.name === 'session') {
    return (
      <SessionScreen
        cards={screen.cards}
        subjectLabel={subject.title}
        onGrade={handleGrade}
        onExit={() => setScreen({ name: 'board' })}
        onFinish={results => setScreen({ name: 'close', results, topicId: screen.topicId })}
      />
    );
  }

  /* -------------------------------------------------------------- close ---- */

  if (screen.name === 'close') {
    const claimed = screen.results.reduce((n, r) => n + r.marksClaimed, 0);
    const available = screen.results.reduce((n, r) => n + r.marksAvailable, 0);
    const left = available - claimed;
    const worst = [...screen.results].sort(
      (a, b) => (b.marksAvailable - b.marksClaimed) - (a.marksAvailable - a.marksClaimed),
    )[0];
    const worstCard = worst && cards.find(c => c.id === worst.cardId);
    const worstGap = worst ? worst.marksAvailable - worst.marksClaimed : 0;
    const distinct = new Set(screen.results.map(r => r.cardId)).size;

    return (
      <div style={{ minHeight: '100dvh', fontFamily: SANS, padding: '28px 16px 60px' }}>
        <div style={{ maxWidth: 560, margin: '0 auto' }}>
          <h2 style={{ font: `700 26px/1.2 ${SERIF}`, color: INK, margin: '0 0 18px' }}>
            {distinct === 1 ? "That's the card." : `That's the ${distinct}.`}
          </h2>

          <div style={{ background: '#fff', border: `2px solid ${INK}`, borderRadius: 18, padding: '20px 22px' }}>
            <Eyebrow>What you banked</Eyebrow>
            <p style={{ font: `700 34px/1.1 ${SERIF}`, color: INK, margin: '8px 0 2px', fontVariantNumeric: 'tabular-nums' }}>
              {claimed} <span style={{ font: `400 18px/1 ${SANS}`, color: MUTED }}>of {available} marks</span>
            </p>
            {left > 0 && worstCard && (
              <p style={{ font: `400 14px/1.55 ${SANS}`, color: INK_2, margin: '12px 0 0' }}>
                {left} {left === 1 ? 'mark was' : 'marks were'} left on the table
                {worstGap > 0 && <> — {worstGap} of {left === worstGap ? 'them' : `them on one card`}.</>}
                <br />
                <strong style={{ color: INK }}>{worstCard.questionRef}</strong>{' '}
                <span style={{ color: MUTED }}>{worstCard.questionText}</span>
              </p>
            )}
            {left === 0 && (
              <p style={{ font: `400 14px/1.55 ${SANS}`, color: SUCCESS_TEXT, margin: '12px 0 0' }}>
                Nothing left behind. Every mark on the table.
              </p>
            )}
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 9, marginTop: 20 }}>
            <button
              type="button"
              onClick={() => { setScreen({ name: 'board' }); }}
              style={{
                padding: '13px 20px', borderRadius: 100, border: 'none', cursor: 'pointer',
                background: '#F26B1F', color: '#fff', font: `600 15px/1 ${SANS}`,
                borderBottom: '3px solid #B54D14', boxShadow: '0 4px 0 #B54D14',
              }}
            >
              Back to the Bank
            </button>
            <button
              type="button"
              onClick={() => startSession(screen.topicId)}
              style={{
                padding: '11px 20px', borderRadius: 20, cursor: 'pointer',
                background: '#fff', color: MUTED, border: `2px solid ${MUTED_BORDER}`,
                font: `600 14px/1 ${SANS}`,
              }}
            >
              Another {SESSION_SIZE}
            </button>
          </div>
        </div>
      </div>
    );
  }

  /* -------------------------------------------------------------- board ---- */

  /* The bank home and the topic board were two screens showing the same thing.
     Once the subject and level are remembered, the home screen's whole job is one
     readout and one button — that is a rail, not a screen. */
  const dueCount = dueIds.length;
  const strands = strandsFor(subjectId);
  const dueTopics = strands.flatMap(s => s.topics).filter(t => {
    const tc = cardsForTopic(t.id, cards);
    return tc.some(c => { const m = memories[c.id]; return m?.last ? isDue(c.id, m, now(), retention) : false; });
  }).length;
  const dueMarks = cards
    .filter(c => { const m = memories[c.id]; return m?.last ? isDue(c.id, m, now(), retention) : false; })
    .reduce((n, c) => n + c.totalMarks, 0);

  const nextReturn = cards
    .map(c => (memories[c.id]?.last ? dueAt(c.id, memories[c.id], retention) : Infinity))
    .filter(ts => ts > now() && Number.isFinite(ts))
    .sort((a, b) => a - b)[0];

  const elsewhere = builtDecks().filter(d => d.subjectId !== subjectId || d.level !== level);
  const builtElsewhere = elsewhere.length
    ? `${elsewhere.map(d => d.label).join(', ').replace(/, ([^,]*)$/, ' and $1')} ${elsewhere.length === 1 ? 'is' : 'are'} ready now`
    : null;

  return (
    <div style={{ fontFamily: SANS, padding: '28px 0 72px' }}>
      <div style={{
        maxWidth: wide ? SURFACE : COLUMN, margin: '0 auto', padding: '0 16px',
        display: 'flex', alignItems: 'flex-start', gap: wide ? GUTTER : 0,
        flexDirection: wide ? 'row' : 'column',
      }}>

        {/* ---- the rail: what you sit, what is waiting, and the way in ---- */}
        <div style={{
          width: wide ? RAIL : '100%', flex: '0 0 auto',
          position: wide ? 'sticky' : 'static', top: 24,
          marginBottom: wide ? 0 : 22,
        }}>
          <h2 style={{ font: `700 24px/1.15 ${SERIF}`, color: INK, margin: '0 0 3px' }}>
            {subject.title}
          </h2>
          <Eyebrow>{level === 'higher' ? 'Higher level' : 'Ordinary level'} · redeveloped specification</Eyebrow>

          {/* alignItems, or the pills stretch: a flex column stretches its
              children by default, which overrides the Segment's own inline-flex
              and leaves the options huddled at the left end of a 664px pill. */}
          <div style={{
            display: 'flex', flexDirection: 'column', alignItems: 'flex-start',
            gap: 8, margin: '16px 0 0',
          }}>
            <Segment
              options={SUBJECTS.map(s => ({ value: s.id, label: s.title, empty: deckSize(s.id, level) === 0 }))}
              value={subjectId}
              onChange={chooseSubject}
            />
            <Segment
              options={(['higher', 'ordinary'] as Level[]).map(l => ({
                value: l, label: l === 'higher' ? 'Higher' : 'Ordinary',
                empty: deckSize(subjectId, l) === 0,
              }))}
              value={level}
              onChange={v => chooseLevel(v as Level)}
            />
          </div>

          {levelUnbuilt ? (
            <p style={{ margin: '18px 0 0', font: `400 13.5px/1.55 ${SANS}`, color: MUTED }}>
              Cards are written one paper at a time, straight from the marking schemes.
              This one is still being written — {builtElsewhere ?? 'try another subject or level in the meantime'}.
            </p>
          ) : (
            <>
              {/* Never a backlog. Today's work, and nothing about what was missed. */}
              <p style={{
                margin: '18px 0 0', font: `700 13px/1.5 ${MONO}`, color: dueCount > 0 ? INK : MUTED,
                fontVariantNumeric: 'tabular-nums',
              }}>
                {dueCount > 0
                  ? `${dueMarks} marks due · ${dueTopics} ${dueTopics === 1 ? 'topic' : 'topics'}`
                  : 'Nothing due today'}
              </p>
              {dueCount === 0 && (
                <p style={{ margin: '6px 0 0', font: `400 13px/1.5 ${SANS}`, color: MUTED }}>
                  That&rsquo;s the schedule doing its job, not you slacking.
                  {nextReturn && Number.isFinite(nextReturn) && (
                    <> Next one back {new Date(nextReturn).toLocaleDateString('en-IE', { weekday: 'long' })}.</>
                  )}
                </p>
              )}

              <button
                type="button"
                autoFocus
                onClick={() => startSession()}
                style={{
                  width: '100%', maxWidth: wide ? '100%' : 320,
                  marginTop: 14, padding: '15px 20px', borderRadius: 100, cursor: 'pointer',
                  font: `650 15px/1 ${SANS}`,
                  ...(dueCount > 0
                    ? {
                      border: 'none', background: ACCENT, color: '#fff',
                      borderBottom: '3px solid #B54D14', boxShadow: '0 4px 0 #B54D14',
                    }
                    : {
                      border: `2px solid ${INK}`, background: '#fff', color: INK,
                    }),
                }}
              >
                {dueCount > 0 ? `Start today's ${Math.min(dueCount, SESSION_SIZE)}` : 'Practise anyway'}
              </button>

              {cards.length > 0 && (
                <p style={{ margin: '20px 0 0', font: `400 11.5px/1.5 ${SANS}`, color: LABEL }}>
                  {cards.length} questions from the {examYears} Leaving Certificate papers,
                  each marked against the real State Examinations Commission scheme.
                </p>
              )}
            </>
          )}
        </div>

        {/* ---- the list: one card, aligned columns, hairlines not boxes ---- */}
        {!levelUnbuilt && (
          <div style={{
            width: wide ? LIST : '100%', flex: '0 0 auto', maxWidth: '100%',
            background: '#fff', border: `2px solid ${INK}`, borderRadius: 16, overflow: 'hidden',
          }}>
            {strands.map((strand, si) => (
              <section key={strand.id} id={`strand-${strand.id}`}>
                <div style={{
                  height: 44, display: 'flex', alignItems: 'center', gap: 9,
                  padding: '0 18px', background: '#f4f2ee',
                  borderTop: si === 0 ? 'none' : `2px solid ${INK}`,
                  borderBottom: `1px solid ${HAIRLINE}`,
                }}>
                  <span style={{ font: `600 14px/1 ${SERIF}`, color: INK }}>{strand.title}</span>
                  <span style={{ font: `700 9.5px/1.5 ${SANS}`, letterSpacing: '.12em', textTransform: 'uppercase', color: LABEL }}>
                    {strand.label}
                  </span>
                </div>

                <ul style={{ listStyle: 'none', margin: 0, padding: 0 }}>
                  {strand.topics.map((topic, ti) => {
                    const topicCards = cardsForTopic(topic.id, cards);
                    const total = topicMarks(topic.id, cards);
                    const built = topicCards.length > 0;
                    const due = topicCards.filter(c => {
                      const m = memories[c.id];
                      return m?.last ? isDue(c.id, m, now(), retention) : false;
                    }).length;
                    const tSecure = marksSecure(topicCards);
                    const tMet = marksMet(topicCards);
                    const dueHere = topicCards
                      .filter(c => { const m = memories[c.id]; return m?.last ? isDue(c.id, m, now(), retention) : false; })
                      .reduce((n, c) => n + c.totalMarks, 0);

                    return (
                      <li key={topic.id} style={{ borderTop: ti === 0 ? 'none' : `1px solid ${HAIRLINE}` }}>
                        <button
                          type="button"
                          disabled={!built}
                          onClick={() => startSession(topic.id)}
                          style={{
                            width: '100%', height: 56, display: 'flex', alignItems: 'center', gap: 16,
                            padding: '0 18px', textAlign: 'left', background: 'none', border: 'none',
                            cursor: built ? 'pointer' : 'default',
                          }}
                        >
                          <span style={{
                            width: 30, flex: '0 0 auto',
                            font: `700 11px/1 ${MONO}`, color: LABEL,
                          }}>
                            {topic.code}
                          </span>
                          <span style={{
                            flex: 1, minWidth: 0,
                            font: `500 14.5px/1.3 ${SANS}`, color: built ? INK : LABEL,
                            overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
                          }}>
                            {topic.title}
                          </span>

                          {/* Every bar at the same x. Twenty bars scattered across
                              twenty cards cannot be compared, which is the one
                              thing a marks-based progress model exists to do. */}
                          <span style={{ width: 120, flex: '0 0 auto' }}>
                            {built && tMet > 0 && <MarkBar secure={tSecure} met={tMet} total={total} />}
                          </span>

                          <span style={{
                            width: 96, flex: '0 0 auto', textAlign: 'right',
                            font: `700 11px/1.5 ${MONO}`, fontVariantNumeric: 'tabular-nums',
                            // Orange is the ONE colour here, and it means "do this
                            // now". It used to be the success green, so the same
                            // green said "start here" and "you finished this".
                            color: !built ? LABEL : due > 0 ? ACCENT : MUTED,
                            whiteSpace: 'nowrap',
                          }}>
                            {!built
                              ? 'Being built'
                              : due > 0
                                ? `${dueHere} due`
                                : tMet > 0
                                  ? `${tSecure} of ${total}`
                                  /* Never a zero on a topic nobody has opened. A
                                     first look at a subject must not be a column
                                     of "0 of 104 marks secure". */
                                  : `${topicCards.length} cards`}
                          </span>
                        </button>
                      </li>
                    );
                  })}
                </ul>
              </section>
            ))}
          </div>
        )}
      </div>

      {!loaded && uid && (
        <p style={{ maxWidth: wide ? SURFACE : COLUMN, margin: '14px auto 0', padding: '0 16px', font: `400 11.5px/1.4 ${SANS}`, color: LABEL }}>
          Syncing your deck…
        </p>
      )}
    </div>
  );
};

export default MarkBank;
