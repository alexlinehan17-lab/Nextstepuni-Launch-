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
import { MotionDiv, useReducedMotion } from '../Motion';
import SessionScreen, { ENVIRONMENT, type SessionCardResult } from './SessionScreen';
import {
  NEW_CARD, dueAt, grade as gradeCard, intervalWords,
  isDue, planSession, retentionFor, retrievability,
} from './scheduler';
import {
  IS_SAMPLE_DECK, SAMPLE_CARDS, STRANDS, cardsForTopic, topicMarks,
} from './deck';
import {
  commitReview, fetchDeck, mergeDecks, readLocal, writeLocal,
  type DeckState,
} from './store';
import type { SecCard } from '../../types/markBank';

const EASE = [0.16, 1, 0.3, 1] as number[];
const SESSION_SIZE = 12;

const INK = '#1a1a1a';
const INK_2 = '#3a3530';
const MUTED = '#7a7068';
const LABEL = '#9e9186';
const MUTED_BORDER = '#d0cdc8';
const PLATE = '#F0FAF8';
const SUCCESS = '#3A8D5F';
const SUCCESS_TINT = '#E8F2EC';
const SUCCESS_TEXT = '#1F5F3E';
const PAGE = '#f0f0f0';

const SERIF = "'Source Serif 4', Georgia, serif";
const SANS = "'DM Sans', system-ui, sans-serif";
const MONO = "'Roboto Mono', ui-monospace, monospace";

type Level = 'higher' | 'ordinary';
type Screen =
  | { name: 'bank' }
  | { name: 'topics' }
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
  const reduced = useReducedMotion() ?? false;
  const [level, setLevel] = useState<Level>('higher');
  const deckId = `biology-${level}`;
  const [deck, setDeck] = useState<DeckState>(() => readLocal(uid, deckId));
  const [screen, setScreen] = useState<Screen>({ name: 'bank' });
  const [loaded, setLoaded] = useState(false);

  // Seed FRESH from Firestore on mount — never from the app-start progress
  // snapshot, which is what makes other tools lose state saved this session.
  useEffect(() => {
    let cancelled = false;
    setLoaded(false);
    const local = readLocal(uid, deckId);
    setDeck(local);
    fetchDeck(uid, deckId).then(remote => {
      if (cancelled) return;
      const merged = mergeDecks(local, remote);
      writeLocal(uid, deckId, merged);
      setDeck(merged);
      setLoaded(true);
    });
    return () => { cancelled = true; };
  }, [uid, deckId]);

  const cards = useMemo(() => SAMPLE_CARDS.filter(c => c.level === level), [level]);
  const memories = deck.cards;
  const retention = retentionFor(now(), deck.examTs);

  const dueIds = useMemo(
    () => cards.filter(c => {
      const m = memories[c.id];
      return m && m.last ? isDue(c.id, m, now(), retention) : false;
    }).map(c => c.id),
    [cards, memories, retention, now],
  );
  const unmet = cards.filter(c => !memories[c.id]?.last);

  /** Marks on cards the scheduler still predicts the student would recall. */
  const marksSecure = useCallback((subset: SecCard[]) =>
    subset.reduce((n, c) => {
      const m = memories[c.id];
      if (!m?.last) return n;
      return retrievability(m, now()) >= 0.9 ? n + c.totalMarks : n;
    }, 0), [memories, now]);

  const marksMet = useCallback((subset: SecCard[]) =>
    subset.reduce((n, c) => (memories[c.id]?.last ? n + c.totalMarks : n), 0), [memories]);

  const totalMarks = cards.reduce((n, c) => n + c.totalMarks, 0);

  const startSession = (topicId?: string) => {
    const pool = topicId ? cards.filter(c => c.topicId === topicId) : cards;
    const plan = planSession(pool.map(c => c.id), memories, now(), { size: SESSION_SIZE, examTs: deck.examTs });
    const queue = plan.queue.map(id => pool.find(c => c.id === id)).filter(Boolean) as SecCard[];
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
        memories={memories}
        subjectLabel="Biology"
        onGrade={handleGrade}
        onExit={() => setScreen({ name: 'topics' })}
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
      <div style={{ minHeight: '100dvh', background: PAGE, fontFamily: SANS, padding: '28px 16px 60px' }}>
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
              onClick={() => { setScreen({ name: 'bank' }); }}
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

  /* ------------------------------------------------------------- topics ---- */

  if (screen.name === 'topics') {
    return (
      <div style={{ minHeight: '100dvh', background: PAGE, fontFamily: SANS }}>
        <div style={{ background: ENVIRONMENT, padding: '20px 16px 24px', borderRadius: '0 0 26px 26px' }}>
          <div style={{ maxWidth: 560, margin: '0 auto' }}>
            <button
              type="button" onClick={() => setScreen({ name: 'bank' })}
              style={{ background: 'none', border: 'none', padding: 0, color: 'rgba(255,255,255,.75)', font: `600 12.5px/1 ${SANS}`, cursor: 'pointer' }}
            >
              ‹ The Bank
            </button>
            <h2 style={{ font: `700 26px/1.15 ${SERIF}`, color: '#fff', margin: '12px 0 4px' }}>Biology</h2>
            <span style={{ font: `700 9.5px/1.5 ${SANS}`, letterSpacing: '.13em', textTransform: 'uppercase', color: 'rgba(255,255,255,.6)' }}>
              {level === 'higher' ? 'Higher level' : 'Ordinary level'} · redeveloped specification
            </span>
          </div>
        </div>

        <div style={{ maxWidth: 560, margin: '0 auto', padding: '20px 16px 60px' }}>
          {STRANDS.map(strand => (
            <section key={strand.id} style={{ marginBottom: 26 }}>
              <div style={{ marginBottom: 10 }}>
                <Eyebrow>{strand.label}</Eyebrow>
                <h3 style={{ font: `600 16px/1.25 ${SERIF}`, color: INK, margin: '3px 0 0' }}>{strand.title}</h3>
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                {strand.topics.map(topic => {
                  const topicCards = cardsForTopic(topic.id, cards);
                  const total = topicMarks(topic.id, cards);
                  const built = topicCards.length > 0;
                  const due = topicCards.filter(c => {
                    const m = memories[c.id];
                    return m?.last ? isDue(c.id, m, now(), retention) : false;
                  }).length;
                  const secure = marksSecure(topicCards);
                  const met = marksMet(topicCards);

                  return (
                    <button
                      key={topic.id}
                      type="button"
                      disabled={!built}
                      onClick={() => startSession(topic.id)}
                      style={{
                        textAlign: 'left', width: '100%', cursor: built ? 'pointer' : 'default',
                        background: '#fff', borderRadius: 14, padding: '13px 15px',
                        border: `2px solid ${built ? INK : MUTED_BORDER}`,
                        opacity: built ? 1 : 0.7,
                      }}
                    >
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', gap: 10 }}>
                        <span style={{ font: `600 14.5px/1.3 ${SANS}`, color: built ? INK : MUTED }}>
                          <span style={{ font: `700 11px/1 ${MONO}`, color: LABEL, marginRight: 7 }}>{topic.code}</span>
                          {topic.title}
                        </span>
                        {due > 0 && (
                          <span style={{
                            font: `700 10.5px/1.7 ${MONO}`, background: SUCCESS_TINT, color: SUCCESS_TEXT,
                            borderRadius: 6, padding: '0 7px', whiteSpace: 'nowrap',
                          }}>{due} due</span>
                        )}
                      </div>

                      {built ? (
                        <>
                          <p style={{ margin: '8px 0 6px', font: `400 12px/1.4 ${SANS}`, color: MUTED }}>
                            {met === 0
                              ? `${topicCards.length} ${topicCards.length === 1 ? 'card' : 'cards'} · none met yet`
                              : `${secure} of ${total} marks secure`}
                          </p>
                          <MarkBar secure={secure} met={met} total={total} />
                        </>
                      ) : (
                        <p style={{ margin: '7px 0 0', font: `400 12px/1.4 ${SANS}`, color: LABEL }}>
                          Not built yet — this topic is coming.
                        </p>
                      )}
                    </button>
                  );
                })}
              </div>
            </section>
          ))}
        </div>
      </div>
    );
  }

  /* --------------------------------------------------------------- bank ---- */

  const secure = marksSecure(cards);
  const met = marksMet(cards);
  const dueCount = dueIds.length;
  const nothingMet = met === 0;
  const nextReturn = cards
    .map(c => (memories[c.id]?.last ? dueAt(c.id, memories[c.id], retention) : Infinity))
    .filter(ts => ts > now() && Number.isFinite(ts))
    .sort((a, b) => a - b)[0];

  return (
    <div style={{ minHeight: '100dvh', background: PAGE, fontFamily: SANS }}>
      <MotionDiv
        initial={reduced ? false : { opacity: 0, y: -8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.35, ease: EASE }}
        style={{ background: ENVIRONMENT, padding: '30px 16px 34px', borderRadius: '0 0 28px 28px' }}
      >
        <div style={{ maxWidth: 560, margin: '0 auto' }}>
          {nothingMet ? (
            <>
              <h2 style={{ font: `700 27px/1.18 ${SERIF}`, color: '#fff', margin: '0 0 10px' }}>
                Nothing in the bank yet.
              </h2>
              <p style={{ font: `400 14.5px/1.55 ${SANS}`, color: 'rgba(255,255,255,.8)', margin: '0 0 20px', maxWidth: '34ch' }}>
                Pick a topic and you&rsquo;ll get real Leaving Cert Biology questions — the exact wording
                from the paper — marked point by point against the real scheme.
              </p>
            </>
          ) : dueCount > 0 ? (
            <>
              <h2 style={{ font: `700 27px/1.18 ${SERIF}`, color: '#fff', margin: '0 0 8px' }}>
                {dueCount} {dueCount === 1 ? 'question is' : 'questions are'} ready for you.
              </h2>
              <p style={{ font: `400 14px/1.5 ${SANS}`, color: 'rgba(255,255,255,.75)', margin: '0 0 20px' }}>
                About {Math.max(2, Math.round(dueCount * 1.2))} minutes.
              </p>
            </>
          ) : (
            <>
              <h2 style={{ font: `700 27px/1.18 ${SERIF}`, color: '#fff', margin: '0 0 10px' }}>
                Nothing due today.
              </h2>
              <p style={{ font: `400 14.5px/1.55 ${SANS}`, color: 'rgba(255,255,255,.8)', margin: '0 0 20px', maxWidth: '36ch' }}>
                That&rsquo;s not you slacking — it&rsquo;s the schedule doing its job. Everything you&rsquo;ve
                met is still fresh enough that showing it now would waste your time.
                {nextReturn && Number.isFinite(nextReturn) && (
                  <> Next one back {new Date(nextReturn).toLocaleDateString('en-IE', { weekday: 'long' })}.</>
                )}
              </p>
            </>
          )}

          <div style={{ display: 'flex', gap: 9, flexWrap: 'wrap' }}>
            <button
              type="button"
              onClick={() => (dueCount > 0 ? startSession() : setScreen({ name: 'topics' }))}
              style={{
                padding: '13px 24px', borderRadius: 100, border: 'none', cursor: 'pointer',
                background: '#F26B1F', color: '#fff', font: `600 15px/1 ${SANS}`,
                borderBottom: '3px solid #B54D14', boxShadow: '0 4px 0 #B54D14',
              }}
            >
              {dueCount > 0 ? "Start today's mix" : nothingMet ? 'Choose a topic' : 'Pick a topic anyway'}
            </button>
            {dueCount > 0 && (
              <button
                type="button"
                onClick={() => setScreen({ name: 'topics' })}
                style={{
                  padding: '13px 20px', borderRadius: 100, cursor: 'pointer',
                  background: 'transparent', color: '#fff',
                  border: '2px solid rgba(255,255,255,.35)', font: `600 14px/1 ${SANS}`,
                }}
              >
                Pick a topic
              </button>
            )}
          </div>
        </div>
      </MotionDiv>

      <div style={{ maxWidth: 560, margin: '0 auto', padding: '20px 16px 60px' }}>
        {/* Level segment. Switching never wipes state — both decks survive. */}
        <div style={{ display: 'inline-flex', background: '#fff', border: `2px solid ${INK}`, borderRadius: 100, padding: 3, marginBottom: 18 }}>
          {(['higher', 'ordinary'] as Level[]).map(l => (
            <button
              key={l} type="button" onClick={() => setLevel(l)}
              style={{
                padding: '7px 16px', borderRadius: 100, border: 'none', cursor: 'pointer',
                background: level === l ? INK : 'transparent',
                color: level === l ? '#fff' : MUTED, font: `600 12.5px/1 ${SANS}`,
              }}
            >
              {l === 'higher' ? 'Higher' : 'Ordinary'}
            </button>
          ))}
        </div>

        <button
          type="button"
          onClick={() => setScreen({ name: 'topics' })}
          style={{
            width: '100%', textAlign: 'left', cursor: 'pointer',
            background: '#fff', border: `2px solid ${INK}`, borderRadius: 16, padding: '17px 19px',
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', gap: 10 }}>
            <span style={{ font: `600 17px/1.2 ${SERIF}`, color: INK }}>Biology</span>
            <span style={{ font: `700 11px/1 ${MONO}`, color: MUTED, fontVariantNumeric: 'tabular-nums' }}>
              {secure} / {totalMarks} marks
            </span>
          </div>
          <p style={{ margin: '9px 0 8px', font: `400 12.5px/1.45 ${SANS}`, color: MUTED }}>
            {nothingMet
              ? `${cards.length} sample ${cards.length === 1 ? 'card' : 'cards'} across ${new Set(cards.map(c => c.topicId)).size} topics`
              : `${secure} of ${totalMarks} marks secure · ${unmet.length} not met yet`}
          </p>
          <MarkBar secure={secure} met={met} total={totalMarks} />
        </button>

        {IS_SAMPLE_DECK && (
          <div style={{ marginTop: 16, padding: '13px 15px', background: PLATE, borderRadius: 12 }}>
            <Eyebrow>Sample deck</Eyebrow>
            <p style={{ margin: '6px 0 0', font: `400 12.5px/1.5 ${SANS}`, color: INK_2 }}>
              These {SAMPLE_CARDS.length} cards exist so the tool can be walked through before authoring
              begins. Their marking points are quoted from real SEC schemes; the diagram is a labelled
              placeholder. Topics are the twelve units of the redeveloped specification, first examined
              June 2027.
            </p>
          </div>
        )}

        {!loaded && uid && (
          <p style={{ marginTop: 14, font: `400 11.5px/1.4 ${SANS}`, color: LABEL }}>
            Syncing your deck…
          </p>
        )}
      </div>
    </div>
  );
};

export default MarkBank;
