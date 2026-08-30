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

import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import SessionScreen, { type SessionCardResult } from './SessionScreen';
import {
  NEW_CARD, dueAt, grade as gradeCard, intervalWords,
  isDue, retentionFor, retrievability,
} from './scheduler';
import {
  MARK_BANK_SESSION_SIZE,
  nextSessionActionLabel,
  resolveSessionQueue,
  topicSessionSummary,
} from './sessionPlanning';
import { SUBJECTS, builtDecks, cardsForTopic, deckSize, loadCards, strandsFor, topicMarks, type Level } from './deck';
import {
  commitReview, ensureDeck, fetchDeck, mergeDecks, readChoice, readLocal,
  writeChoice, writeLocal, type DeckState,
} from './store';
import type { SecCard } from '../../types/markBank';
import ChoiceControl from '../ui/ChoiceControl';
import PrimaryActionButton from '../ui/PrimaryActionButton';
import { ResultStatGrid, StatusNotice } from '../ui/ProductPatterns';
import { getSubjectHex } from '../../utils/subjectColors';

const INK = 'var(--mb-ink)';
const INK_2 = 'var(--mb-ink-2)';
const MUTED = 'var(--mb-muted)';
const LABEL = 'var(--mb-label)';
const MUTED_BORDER = 'var(--mb-border)';
const SUCCESS = 'var(--mb-success)';
const SUCCESS_TINT = 'var(--mb-success-tint)';
const SUCCESS_TEXT = 'var(--mb-success-text)';

const SERIF = "'Source Serif 4', Georgia, serif";
const SANS = "'DM Sans', system-ui, sans-serif";
const MONO = "'Roboto Mono', ui-monospace, monospace";

/** Accent means "this is the action / do this now". Never "correct". */
const ACCENT = '#F26B1F';
const HAIRLINE = 'var(--mb-hairline)';

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
  studentSubjects?: Array<{ subjectName: string; level?: string }>;
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
 * A compact group of mutually exclusive choices using the platform selection
 * language. Mark Bank keeps its editorial typography and dense information,
 * while its controls now belong to the same product as Study and onboarding.
 *
 * An option with no cards behind it stays selectable and says so, rather than
 * being hidden or disabled: a student looking for Chemistry needs to see that it
 * exists and is being written, not to wonder whether the tool has it at all.
 */
const Segment: React.FC<{
  options: { value: string; label: string; empty?: boolean; markerColor?: string; shortLabel?: string }[];
  value: string;
  onChange: (value: string) => void;
  /**
   * Let the options run onto more than one row.
   *
   * A single-row stadium works only while every label is short. "Agricultural
   * Science" is 20 characters and needs about 160px of the 280px rail on its
   * own, so the four-subject control could not fit one row at any sensible size:
   * the label broke mid-phrase onto two lines at line-height 1, and the row
   * overflowed the rounded border it was supposed to sit inside. Wrapping is
   * opt-in rather than automatic so the two-option level toggle keeps its pill.
   */
  wrap?: boolean;
}> = ({ options, value, onChange, wrap = false }) => (
  <div style={{
    display: wrap ? 'flex' : 'inline-flex',
    flexWrap: wrap ? 'wrap' : 'nowrap',
    gap: 6,
    maxWidth: '100%',
    padding: 0,
  }}>
    {options.map(o => {
      const on = o.value === value;
      return (
        <ChoiceControl
          key={o.value}
          onClick={() => onChange(o.value)}
          label={o.label}
          selected={on}
          compact
          className={wrap ? 'flex-auto' : ''}
          markerColor={o.markerColor}
          trailing={(
            <>
              {o.shortLabel && (
                <span
                  aria-hidden
                  style={{
                    display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
                    minWidth: 22, height: 22, padding: '0 6px', borderRadius: 7,
                    background: on ? 'rgba(253,248,240,.18)' : 'var(--mb-raised)',
                    color: on ? '#FDF8F0' : MUTED,
                    font: `700 9px/1 ${MONO}`, letterSpacing: '.04em',
                  }}
                >
                  {o.shortLabel}
                </span>
              )}
              {o.empty && (
                <span
                  aria-hidden
                  title="No cards yet"
                  style={{ width: 5, height: 5, borderRadius: '50%', background: MUTED_BORDER }}
                />
              )}
            </>
          )}
        />
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

const normaliseSubjectName = (name: string) => name.toLowerCase().replace(/&/g, 'and').replace(/[^a-z0-9]/g, '');
const MARK_BANK_SUBJECT_ALIASES: Record<string, string> = {
  maths: 'mathematics',
  mathematic: 'mathematics',
  agscience: 'agriculturalscience',
  homeec: 'homeeconomics',
  construction: 'constructionstudies',
};

export function profileDeckChoice(studentSubjects?: MarkBankProps['studentSubjects']): { subjectId: string; level: Level } | null {
  for (const profileSubject of studentSubjects ?? []) {
    const raw = normaliseSubjectName(profileSubject.subjectName);
    const wanted = MARK_BANK_SUBJECT_ALIASES[raw] ?? raw;
    const subject = SUBJECTS.find(candidate => normaliseSubjectName(candidate.title) === wanted);
    if (!subject) continue;
    const level: Level = profileSubject.level?.toLowerCase().startsWith('ordinary') ? 'ordinary' : 'higher';
    if (deckSize(subject.id, level) > 0) return { subjectId: subject.id, level };
  }
  return null;
}

const MarkBank: React.FC<MarkBankProps> = ({ uid, studentSubjects, now = () => Date.now() }) => {
  /* Read synchronously on mount. A Chemistry Ordinary student must never watch
     the tool open on Biology Higher and correct it — that is two clicks every
     session, forever. */
  const saved = useMemo(() => readChoice(uid), [uid]);
  const profileDefault = useMemo(() => profileDeckChoice(studentSubjects), [studentSubjects]);
  const savedIsValid = Boolean(
    saved
    && SUBJECTS.some(subject => subject.id === saved.subjectId)
    && deckSize(saved.subjectId, saved.level) > 0,
  );
  const initialChoice = savedIsValid && saved ? saved : profileDefault ?? { subjectId: SUBJECTS[0].id, level: 'higher' as Level };
  const [subjectId, setSubjectId] = useState<string>(initialChoice.subjectId);
  const [level, setLevel] = useState<Level>(initialChoice.level);
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
  const [online, setOnline] = useState(() => typeof navigator === 'undefined' ? true : navigator.onLine);

  useEffect(() => {
    const goOnline = () => setOnline(true);
    const goOffline = () => setOnline(false);
    window.addEventListener('online', goOnline);
    window.addEventListener('offline', goOffline);
    return () => {
      window.removeEventListener('online', goOnline);
      window.removeEventListener('offline', goOffline);
    };
  }, []);

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
  const [cardsError, setCardsError] = useState(false);
  const [cardsAttempt, setCardsAttempt] = useState(0);
  const [launchingTopicId, setLaunchingTopicId] = useState<string | null>(null);
  const launchTimerRef = useRef<number | null>(null);
  useEffect(() => {
    let cancelled = false;
    setCardsLoading(true);
    setCardsError(false);
    loadCards(subjectId, level).then(loaded => {
      if (cancelled) return;
      setCards(loaded);
      setCardsLoading(false);
    }).catch(() => {
      if (cancelled) return;
      setCards([]);
      setCardsError(true);
      setCardsLoading(false);
    });
    return () => { cancelled = true; };
  }, [subjectId, level, cardsAttempt]);

  useEffect(() => () => {
    if (launchTimerRef.current !== null) window.clearTimeout(launchTimerRef.current);
  }, []);

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

  const startSession = (topicId?: string, preparedQueue?: SecCard[]) => {
    if (launchingTopicId !== null) return;
    const pool = topicId ? cards.filter(c => c.topicId === topicId) : cards;
    if (!pool.length) return;
    const queue = preparedQueue
      ?? resolveSessionQueue(pool, memories, now(), deck.examTs);
    if (!queue.length) return;
    // Give the selected row and board time to hand off visually before the
    // fixed question workspace takes over. This is deliberately brief: it is
    // navigation continuity, not a loading interstitial.
    setLaunchingTopicId(topicId ?? '__all__');
    launchTimerRef.current = window.setTimeout(() => {
      setScreen({ name: 'session', cards: queue, topicId });
      setLaunchingTopicId(null);
      launchTimerRef.current = null;
    }, 180);
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
    const reviewPool = screen.topicId ? cardsForTopic(screen.topicId, cards) : cards;
    const reviewPoolLabel = screen.topicId
      ? strandsFor(subjectId)
        .flatMap(strand => strand.topics)
        .find(topic => topic.id === screen.topicId)?.title ?? 'this topic'
      : subject.title;
    return (
      <SessionScreen
        cards={screen.cards}
        subjectLabel={subject.title}
        reviewPoolTotal={reviewPool.length}
        reviewPoolLabel={reviewPoolLabel}
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
    const nextPool = screen.topicId ? cardsForTopic(screen.topicId, cards) : cards;
    const nextQueue = resolveSessionQueue(nextPool, memories, now(), deck.examTs);
    const nextAction = nextSessionActionLabel(
      nextQueue.length,
      Boolean(screen.topicId),
      subject.title,
    );

    return (
      <div className="mark-bank-theme" style={{ minHeight: '100dvh', fontFamily: SANS, padding: '56px 16px 72px', background: 'var(--mb-canvas)' }}>
        <div style={{ maxWidth: 620, margin: '0 auto', textAlign: 'center' }}>
          <div style={{
            width: 76, height: 76, margin: '0 auto 20px', borderRadius: 24,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            background: left === 0 ? SUCCESS_TINT : '#FFF0E6',
            color: left === 0 ? SUCCESS : ACCENT,
          }}>
            <svg width="38" height="38" viewBox="0 0 40 40" fill="none" aria-hidden="true">
              {left === 0 ? (
                <path d="M10 20.5l6.5 6.5L30.5 13" stroke="currentColor" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round" />
              ) : (
                <>
                  <path d="M11 11.5h18v21H11z" stroke="currentColor" strokeWidth="2.5" strokeLinejoin="round" />
                  <path d="M15 8h10v7H15zM16 21h8M16 26h5" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
                </>
              )}
            </svg>
          </div>
          <Eyebrow>Session complete</Eyebrow>
          <h2 style={{ font: `700 32px/1.15 ${SERIF}`, color: INK, margin: '7px 0 8px' }}>
            {left === 0 ? 'Every mark banked.' : 'Good work. Keep building.'}
          </h2>
          <p style={{ font: `400 14px/1.5 ${SANS}`, color: MUTED, margin: '0 0 28px' }}>
            {distinct} {distinct === 1 ? 'question' : 'questions'} reviewed · {subject.title} · {level === 'higher' ? 'Higher level' : 'Ordinary level'}
          </p>

          <ResultStatGrid items={[
            { label: 'Marks banked', value: claimed, tone: 'success' },
            { label: 'Available', value: available },
            { label: 'To revisit', value: Math.max(0, left) },
          ]} />

          <div style={{ marginTop: 14, background: 'var(--mb-paper)', border: `1px solid ${HAIRLINE}`, borderRadius: 16, padding: '17px 19px', textAlign: 'left' }}>
            {left > 0 && worstCard && (
              <>
                <Eyebrow>Best next review</Eyebrow>
                <p style={{ font: `600 14px/1.5 ${SANS}`, color: INK, margin: '7px 0 2px' }}>
                  {worstCard.questionRef} · {worstGap} {worstGap === 1 ? 'mark' : 'marks'} to recover
                </p>
                <p style={{ font: `400 13px/1.5 ${SANS}`, color: MUTED, margin: 0 }}>{worstCard.questionText}</p>
              </>
            )}
            {left === 0 && (
              <p style={{ font: `500 14px/1.55 ${SANS}`, color: SUCCESS_TEXT, margin: 0 }}>
                Nothing left behind. The scheduler will bring these marks back before they fade.
              </p>
            )}
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 10, marginTop: 22, textAlign: 'left' }}>
            <PrimaryActionButton label="Back to Mark Bank" onClick={() => setScreen({ name: 'board' })} className="w-full" />
            {nextQueue.length > 0 && (
              <button
                type="button"
                onClick={() => startSession(screen.topicId, nextQueue)}
                style={{
                  padding: '13px 20px', borderRadius: 12, cursor: 'pointer',
                  background: 'var(--mb-paper)', color: INK_2, border: `1px solid ${MUTED_BORDER}`,
                  font: `600 14px/1 ${SANS}`,
                }}
              >
                {nextAction}
              </button>
            )}
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
  const coveredTopics = strands.flatMap(strand => strand.topics).filter(topic => cardsForTopic(topic.id, cards).length > 0).length;
  const totalTopics = strands.reduce((sum, strand) => sum + strand.topics.length, 0);
  // English is reconciled against every selectable response in all twenty
  // 2021–2025 papers. Empty taxonomy rows there mean "not examined in this
  // corpus", not "unfinished". Showing dozens of disabled poets and roll-up
  // categories made a complete subject look half-built and buried the useful
  // choices on mobile.
  const completePaperCorpus = subjectId === 'english' || subjectId === 'irish';
  const visibleStrands = completePaperCorpus
    ? strands
      .map(strand => ({
        ...strand,
        topics: strand.topics.filter(topic => cardsForTopic(topic.id, cards).length > 0),
      }))
      .filter(strand => strand.topics.length > 0)
    : strands;
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
    <div
      className={`mark-bank-theme ${launchingTopicId !== null ? 'mb-board-exit' : ''}`}
      aria-busy={launchingTopicId !== null}
      style={{ fontFamily: SANS, padding: '28px 0 72px', color: INK }}
    >
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
          <div style={{ marginBottom: 5 }}><Eyebrow>Mark Bank · exam practice</Eyebrow></div>
          <h2 style={{ font: `700 24px/1.15 ${SERIF}`, color: INK, margin: '0 0 3px' }}>
            {subject.title}
          </h2>
          <Eyebrow>{level === 'higher' ? 'Higher level' : 'Ordinary level'} · {subject.spec}</Eyebrow>

          {/* alignItems, or the pills stretch: a flex column stretches its
              children by default, which overrides the Segment's own inline-flex
              and leaves the options huddled at the left end of a 664px pill. */}
          <div style={{
            display: 'flex', flexDirection: 'column', alignItems: 'flex-start',
            gap: 14, margin: '18px 0 0', width: '100%',
          }}>
            <div style={{ width: '100%' }}>
              <div style={{ marginBottom: 6 }}><Eyebrow>Subject</Eyebrow></div>
              <Segment
                wrap
                options={SUBJECTS.map(s => ({
                  value: s.id,
                  label: s.title,
                  empty: deckSize(s.id, level) === 0,
                  markerColor: getSubjectHex(s.title),
                }))}
                value={subjectId}
                onChange={chooseSubject}
              />
            </div>
            <div style={{ width: '100%' }}>
              <div style={{ marginBottom: 6 }}><Eyebrow>Paper level</Eyebrow></div>
              <Segment
                options={(['higher', 'ordinary'] as Level[]).map(l => ({
                  value: l, label: l === 'higher' ? 'Higher' : 'Ordinary',
                  shortLabel: l === 'higher' ? 'HL' : 'OL',
                  empty: deckSize(subjectId, l) === 0,
                }))}
                value={level}
                onChange={v => chooseLevel(v as Level)}
              />
            </div>
          </div>

          {!online && (
            <StatusNotice title="Working offline" className="mt-[18px]">
              Reviews stay on this device and will sync when you reconnect.
            </StatusNotice>
          )}

          {cardsError ? (
            <StatusNotice
              title="Couldn’t load questions"
              tone="warning"
              className="mt-[18px]"
              action={{ label: 'Try again', onClick: () => setCardsAttempt(n => n + 1) }}
            >
              Your saved progress is safe. Check your connection and try loading this paper again.
            </StatusNotice>
          ) : levelUnbuilt ? (
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

              {dueCount > 0 ? (
                <PrimaryActionButton
                  autoFocus
                  label={`Start today's ${Math.min(dueCount, MARK_BANK_SESSION_SIZE)}`}
                  onClick={() => startSession()}
                  className={`w-full ${wide ? '' : 'max-w-80'} mt-3.5`}
                />
              ) : (
                <button
                  type="button"
                  autoFocus
                  onClick={() => startSession()}
                  className={`min-h-12 rounded-xl border border-[#E5E1DB] bg-white px-5 py-3 text-sm font-semibold text-[var(--text-body)] transition-colors hover:border-[rgba(var(--accent),0.35)] hover:bg-[#FDF8F0] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[rgba(var(--accent),0.38)] focus-visible:ring-offset-2 dark:border-zinc-700 dark:bg-zinc-900 ${wide ? 'w-full' : 'w-full max-w-80'} mt-3.5`}
                >
                  Start a practice session
                </button>
              )}

              {cards.length > 0 && (
                <p style={{ margin: '20px 0 0', font: `400 11.5px/1.5 ${SANS}`, color: LABEL }}>
                  {cards.length} questions from the {examYears} Leaving Certificate papers,
                  each marked against the real State Examinations Commission scheme.
                  {completePaperCorpus
                    ? <> Every selectable response is included across {coveredTopics} examined syllabus topics.</>
                    : <> Coverage currently spans {coveredTopics} of {totalTopics} syllabus topics.</>}
                </p>
              )}
            </>
          )}
        </div>

        {/* ---- the list: one card, aligned columns, hairlines not boxes ---- */}
        {!cardsError && !levelUnbuilt && (
          <div style={{
            width: wide ? LIST : '100%', flex: '0 0 auto', maxWidth: '100%',
            background: 'var(--mb-paper)', border: `1px solid ${MUTED_BORDER}`, borderRadius: 16, overflow: 'hidden',
            boxShadow: '0 12px 34px rgba(38, 32, 27, .055)',
          }}>
            {cardsLoading ? (
              <div aria-label="Loading questions" style={{ padding: '18px' }}>
                <Eyebrow>Loading paper</Eyebrow>
                {[0, 1, 2, 3, 4].map(i => (
                  <div key={i} style={{ height: 54, display: 'flex', alignItems: 'center', gap: 14, borderTop: i ? `1px solid ${HAIRLINE}` : 'none' }}>
                    <span style={{ width: 34, height: 22, borderRadius: 7, background: 'var(--mb-raised)' }} />
                    <span style={{ width: `${52 + i * 6}%`, maxWidth: 310, height: 10, borderRadius: 999, background: 'var(--mb-raised)' }} />
                  </div>
                ))}
              </div>
            ) : visibleStrands.map((strand, si) => (
              <section key={strand.id} id={`strand-${strand.id}`}>
                <div style={{
                  height: 44, display: 'flex', alignItems: 'center', gap: 9,
                  padding: '0 18px', background: 'var(--mb-soft)',
                  borderTop: si === 0 ? 'none' : `1px solid ${MUTED_BORDER}`,
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
                    const nextTopicCount = built && due === 0 && tMet === 0
                      ? resolveSessionQueue(topicCards, memories, now(), deck.examTs).length
                      : 0;
                    const sessionSummary = topicSessionSummary(topicCards.length, nextTopicCount);

                    return (
                      <li key={topic.id} style={{ borderTop: ti === 0 ? 'none' : `1px solid ${HAIRLINE}` }}>
                        <button
                          type="button"
                          disabled={!built}
                          onClick={() => startSession(topic.id)}
                          onMouseEnter={e => { if (built) e.currentTarget.style.background = 'var(--mb-raised)'; }}
                          onMouseLeave={e => { e.currentTarget.style.background = launchingTopicId === topic.id ? 'var(--mb-raised)' : 'transparent'; }}
                          style={{
                            width: '100%', height: 56, display: 'flex', alignItems: 'center', gap: wide ? 16 : 12,
                            padding: wide ? '0 18px' : '0 14px', textAlign: 'left',
                            background: launchingTopicId === topic.id ? 'var(--mb-raised)' : 'transparent', border: 'none',
                            cursor: built ? 'pointer' : 'default',
                            transform: launchingTopicId === topic.id ? 'translateX(4px)' : 'translateX(0)',
                            transition: 'background 140ms ease, transform 180ms cubic-bezier(.16, 1, .3, 1)',
                          }}
                        >
                          <span style={{
                            width: 34, height: 24, flex: '0 0 auto',
                            display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
                            borderRadius: 7, background: 'var(--mb-raised)',
                            fontFamily: SANS, fontSize: 11, fontWeight: 700,
                            lineHeight: 'normal', letterSpacing: '.025em', color: MUTED,
                          }}>
                            {topic.code.replace(/^U(?=\d)/i, 'U.')}
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
                          {wide && (
                            <span style={{ width: 120, flex: '0 0 auto' }}>
                              {built && tMet > 0 && <MarkBar secure={tSecure} met={tMet} total={total} />}
                            </span>
                          )}

                          <span style={{
                            width: wide ? 96 : 80, flex: '0 0 auto', textAlign: 'right',
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
                                  : (
                                    <>
                                      <span style={{ display: 'block' }}>{sessionSummary.primary}</span>
                                      {sessionSummary.secondary && (
                                        <span style={{ display: 'block', color: LABEL, fontSize: 10 }}>
                                          {sessionSummary.secondary}
                                        </span>
                                      )}
                                    </>
                                  )}
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
