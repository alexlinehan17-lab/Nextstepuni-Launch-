import { markBankCurriculumMenu, cardsForMenuTopic } from './curriculumMenu';
import { consumeInitialPracticeLink } from './markBankDeepLink';
import { loadAtlasModel } from '../PaperTrail/atlasModel';
import { resolveSubjectId } from '../../curriculumRegistry';
import { COLORS } from '../../design/tokens';
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
import MarkBankLibrary, { type LibraryPage } from './MarkBankLibrary';
import ListeningStudio from '../ListeningStudio';
import { LISTENING_SUBJECT_IDS } from '../ListeningStudio/model';
import StartingPointCheck from './StartingPointCheck';
import { useSubjectAccess } from '../launchpad/SubjectAccess';
import SessionScreen, { type SessionCardResult } from './SessionScreen';
import {
  NEW_CARD, grade as gradeCard, intervalWords, retentionFor,
} from './scheduler';
import {
  listeningExerciseKey,
  nextSessionActionLabel,
  resolveSessionQueue,
  sessionExerciseCount,
} from './sessionPlanning';
import { SUBJECTS,  deckSize, levelsFor, loadCards,  type Level } from './deck';
import {
  commitReview, ensureDeck, fetchDeck, mergeDecks, readChoice, readLocal,
  writeChoice, writeLocal, type DeckState,
} from './store';
import { MARK_BANK_LEVEL_LABELS, isConfidenceReviewCard, isUnpricedSectionCard, type SecCard } from '../../types/markBank';

import PrimaryActionButton from '../ui/PrimaryActionButton';
import { ResultStatGrid } from '../ui/ProductPatterns';
import { trackProgrammeEvent } from '../../utils/programmeAnalytics';
import { DEMO_STUDENT_UID } from '../../data/devStudent';

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

/** Accent means "this is the action / do this now". Never "correct". */
const ACCENT = COLORS.accent;
const HAIRLINE = 'var(--mb-hairline)';

type Screen =
  | { name: 'board' }
  | { name: 'starting-point' }
  | { name: 'session'; cards: SecCard[]; topicId?: string }
  | { name: 'close'; results: SessionCardResult[]; topicId?: string };

export interface MarkBankProps {
  uid?: string;
  examDate?: string | null;
  studentSubjects?: Array<{ subjectName: string; level?: string }>;
  /**
   * Listening Studio. Every card with a recording is sat there, not in a
   * review: the Studio is this same tool on its own front page, so the cards,
   * the student's memory of them and the recorder are the ones a review uses.
   */
  studio?: boolean;
  /** Opens Listening Studio from Mark Bank's board. */
  onOpenListeningStudio?: () => void;
  /** Leaves Listening Studio for the Launchpad (the Studio fills the screen). */
  onLeaveStudio?: () => void;
  /** Injected for tests. */
  now?: () => number;
}

const isListeningSubject = (subjectId: string) => (LISTENING_SUBJECT_IDS as readonly string[]).includes(subjectId);

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
    const canonical = resolveSubjectId(profileSubject.subjectName);
    const wanted = MARK_BANK_SUBJECT_ALIASES[raw] ?? raw;
    const subject = SUBJECTS.find(candidate => canonical ? resolveSubjectId(candidate.id) === canonical : normaliseSubjectName(candidate.title) === wanted);
    if (!subject) continue;
    // A common-level subject has no Higher/Ordinary to read off the profile,
    // and a profile that says "Higher" for one is saying nothing about it.
    // A Foundation student practises the Foundation deck where one is built
    // (Irish), and Ordinary everywhere else.
    const levels = levelsFor(subject.id);
    const stated = profileSubject.level?.toLowerCase() ?? '';
    const level: Level = levels.length === 1 ? levels[0]
      : stated.startsWith('foundation') ? (levels.includes('foundation') ? 'foundation' : 'ordinary')
      : stated.startsWith('ordinary') ? 'ordinary' : 'higher';
    if (deckSize(subject.id, level) > 0) return { subjectId: subject.id, level };
  }
  return null;
}

const MarkBank: React.FC<MarkBankProps> = ({ uid, studentSubjects, examDate, studio = false, onOpenListeningStudio, onLeaveStudio, now = () => Date.now() }) => {
  const canSelectSubject = useSubjectAccess();
  /* Read synchronously on mount. A Chemistry Ordinary student must never watch
     the tool open on Biology Higher and correct it — that is two clicks every
     session, forever. */
  const saved = useMemo(() => readChoice(uid), [uid]);
  const profileDefault = useMemo(() => {
    const selectable = studentSubjects?.filter(s => canSelectSubject(s.subjectName));
    if (!studio) return profileDeckChoice(selectable);
    // The Studio opens on the first of the student's subjects that has listenings.
    for (const profileSubject of selectable ?? []) {
      const choice = profileDeckChoice([profileSubject]);
      if (choice && isListeningSubject(choice.subjectId)) return choice;
    }
    return null;
  }, [studentSubjects, canSelectSubject, studio]);
  const savedIsValid = Boolean(
    saved
    && SUBJECTS.some(subject => subject.id === saved.subjectId && canSelectSubject(subject.title))
    && deckSize(saved.subjectId, saved.level) > 0
    && (!studio || isListeningSubject(saved.subjectId)),
  );
  // A Topic Atlas question's "Practise these parts" link opens its own deck (markBankDeepLink).
  const [practiceLink] = useState(() => {
    const link = consumeInitialPracticeLink();
    const subject = link && SUBJECTS.find(s => s.id === link.subjectId);
    const linkLevel = link && levelsFor(link.subjectId).find(l => l === link.level);
    // The deck choice is rebuilt from the deck's own subject and level values, never copied from the URL.
    return link && subject && linkLevel && canSelectSubject(subject.title) && deckSize(subject.id, linkLevel) > 0
      ? { subjectId: subject.id, level: linkLevel, ids: link.ids } : null;
  });
  const linkedChoice = practiceLink ? { subjectId: practiceLink.subjectId, level: practiceLink.level } : null;
  const studioSubjects = useMemo(
    () => SUBJECTS.filter(s => isListeningSubject(s.id) && canSelectSubject(s.title) && levelsFor(s.id).some(l => deckSize(s.id, l) > 0)),
    [canSelectSubject],
  );
  // The student's own subjects that have listenings: the Studio's tabs.
  const myStudioSubjectIds = useMemo(() => {
    const ids = new Set<string>();
    for (const profileSubject of studentSubjects ?? []) {
      const choice = canSelectSubject(profileSubject.subjectName) ? profileDeckChoice([profileSubject]) : null;
      if (choice && isListeningSubject(choice.subjectId)) ids.add(choice.subjectId);
    }
    return [...ids];
  }, [studentSubjects, canSelectSubject]);
  const firstStudioSubject = studioSubjects[0];
  const fallbackChoice = studio && firstStudioSubject
    ? { subjectId: firstStudioSubject.id, level: levelsFor(firstStudioSubject.id).find(l => deckSize(firstStudioSubject.id, l) > 0) ?? ('higher' as Level) }
    : { subjectId: (SUBJECTS.find(s => canSelectSubject(s.title)) ?? SUBJECTS[0]).id, level: 'higher' as Level };
  const initialChoice = (studio ? null : linkedChoice) ?? (savedIsValid && saved ? saved : profileDefault) ?? fallbackChoice;
  const [subjectId, setSubjectId] = useState<string>(initialChoice.subjectId);
  const [level, setLevel] = useState<Level>(initialChoice.level);
  const chooseSubject = useCallback((id: string) => {
    const chosen = SUBJECTS.find(s => s.id === id);
    if (!chosen || !canSelectSubject(chosen.title)) return;
    setSubjectId(id);
    // A subject examined at one level has no Higher deck to carry the current
    // choice into; without this, picking LCVP opened an empty Higher deck.
    const levels = levelsFor(id);
    const next = levels.includes(level) ? level : levels[0];
    setLevel(next);
    writeChoice(uid, { subjectId: id, level: next });
  }, [uid, level, canSelectSubject]);
  const chooseLevel = useCallback((l: Level) => {
    setLevel(l);
    writeChoice(uid, { subjectId, level: l });
  }, [uid, subjectId]);
  const subject = SUBJECTS.find(s => s.id === subjectId) ?? SUBJECTS[0];
  // One deck per subject AND level, so a student's Biology work is untouched by
  // anything they do in Chemistry, and dropping a level never disturbs either.
  const deckId = `${subjectId}-${level}`;
  const [deck, setDeck] = useState<DeckState>(() => readLocal(uid, deckId));
  const [screen, setScreen] = useState<Screen>({ name: 'board' });
  // The library's page (a strand, a topic), held here so a practice run returns
  // the student to where they started it; a new subject or level opens on its home.
  const [libraryPlace, setLibraryPlace] = useState<{ deckId: string; pages: LibraryPage[] }>({ deckId, pages: [{ at: 'home' }] });
  const libraryPages = libraryPlace.deckId === deckId ? libraryPlace.pages : undefined;
  const setLibraryPages = useCallback((pages: LibraryPage[]) => setLibraryPlace({ deckId, pages }), [deckId]);
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
    // The subject's filing under the Topic Atlas headings arrives with its cards (atlasModel.ts).
    Promise.all([loadCards(subjectId, level), loadAtlasModel(subjectId)]).then(([loaded]) => {
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

  const practiceLinkUsed = useRef(false);
  useEffect(() => {
    if (!practiceLink || practiceLinkUsed.current || cardsLoading || subjectId !== practiceLink.subjectId || level !== practiceLink.level) return;
    practiceLinkUsed.current = true;
    const byId = new Map(cards.map(card => [card.id, card]));
    const queue = practiceLink.ids.map(id => byId.get(id)).filter((card): card is SecCard => Boolean(card));
    if (queue.length) setScreen({ name: 'session', cards: queue });
  }, [practiceLink, cards, cardsLoading, subjectId, level]);

  const memories = deck.cards;
  const retention = retentionFor(now(), deck.examTs);
  /* Cards with a recording are sat in Listening Studio, so they are not in
     the board's counts or in any review queue. They are still this deck's
     cards: the Studio records them through handleGrade below. */
  const reviewCards = useMemo(() => cards.filter(card => !card.audioMaterial), [cards]);
  const listeningCount = cards.length - reviewCards.length;

  const cohortMenu = useMemo(() => markBankCurriculumMenu(subjectId, level, examDate, reviewCards), [subjectId, level, examDate, reviewCards]);
  const topicCardsFor = (id: string, pool: SecCard[]) => cardsForMenuTopic(id, pool, cohortMenu);

  const startSession = (topicId?: string, preparedQueue?: SecCard[]) => {
    if (launchingTopicId !== null) return;
    const pool = topicId ? topicCardsFor(topicId, reviewCards) : reviewCards;
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
    const card = cards.find(candidate => candidate.id === r.cardId);
    // A confidence review has no mark total, and a section-total card (CARD-STANDARD 10i)
    // has no marks of its own, so neither is an assessed zero: they record no accuracy at all.
    if (uid && uid !== DEMO_STUDENT_UID && card && !isConfidenceReviewCard(card) && !isUnpricedSectionCard(card)) {
      const ratio = r.marksAvailable > 0 ? r.marksClaimed / r.marksAvailable : 0;
      const accuracyBand = ratio >= 1 ? 'full' : ratio >= 0.7 ? 'strong' : ratio > 0 ? 'partial' : 'none';
      trackProgrammeEvent('practice_attempt_completed', {
        source: 'practice',
        subjectId: card.subjectId,
        topicId: card.topicId,
        accuracyBand,
      });
    }
    return intervalWords(r.cardId, after, t, retention);
  }, [cards, memories, uid, deckId, retention, now]);

  /* ------------------------------------------------------------ session ---- */

  if (screen.name === 'starting-point') return <StartingPointCheck
    subjectLabel={subject.title} level={level} spec={cohortMenu.spec} cards={reviewCards}
    memories={memories} now={now} examTs={deck.examTs} onGrade={handleGrade}
    onClose={() => setScreen({ name: 'board' })}
    onPractice={(topicId, card) => startSession(topicId, [card])}
  />;

  if (screen.name === 'session') {
    const reviewPool = screen.topicId ? topicCardsFor(screen.topicId, reviewCards) : reviewCards;
    const reviewPoolLabel = screen.topicId
      ? cohortMenu.strands
        .flatMap(strand => strand.topics)
        .find(topic => topic.id === screen.topicId)?.title ?? 'this topic'
      : subject.title;
    return (
      <SessionScreen
        paperLayout
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
    // Confidence reviews and section-total cards (CARD-STANDARD 10i) were never scored,
    // so they stay out of the totals: a section-total card must never read as "0 available".
    const scored = screen.results.filter(result => {
      const resultCard = cards.find(card => card.id === result.cardId);
      return !resultCard || (!isConfidenceReviewCard(resultCard) && !isUnpricedSectionCard(resultCard));
    });
    const unscoredCount = screen.results.length - scored.length;
    const reviewOnly = scored.length === 0;
    const claimed = scored.reduce((n, r) => n + r.marksClaimed, 0);
    const available = scored.reduce((n, r) => n + r.marksAvailable, 0);
    const left = available - claimed;
    const worst = [...scored].sort(
      (a, b) => (b.marksAvailable - b.marksClaimed) - (a.marksAvailable - a.marksClaimed),
    )[0];
    const worstCard = worst && cards.find(c => c.id === worst.cardId);
    const worstGap = worst ? worst.marksAvailable - worst.marksClaimed : 0;
    const distinct = new Set(screen.results.map(result => {
      const resultCard = cards.find(card => card.id === result.cardId);
      return resultCard ? listeningExerciseKey(resultCard) ?? resultCard.id : result.cardId;
    })).size;
    const nextPool = screen.topicId ? topicCardsFor(screen.topicId, reviewCards) : reviewCards;
    const nextQueue = resolveSessionQueue(nextPool, memories, now(), deck.examTs);
    const nextAction = nextSessionActionLabel(
      sessionExerciseCount(nextQueue),
      Boolean(screen.topicId),
      subject.title,
    );

    return (
      <div className="mark-bank-theme" style={{ minHeight: '100dvh', fontFamily: SANS, padding: '56px 16px 72px', background: 'var(--mb-canvas)' }}>
        <div style={{ maxWidth: 620, margin: '0 auto', textAlign: 'center' }}>
          <div style={{
            width: 76, height: 76, margin: '0 auto 20px', borderRadius: 24,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            background: reviewOnly ? 'var(--mb-raised)' : left === 0 ? SUCCESS_TINT : '#FFF0E6',
            color: reviewOnly ? INK_2 : left === 0 ? SUCCESS : ACCENT,
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
            {reviewOnly ? 'Your review is complete.' : left === 0 ? 'Every mark banked.' : 'Good work. Keep building.'}
          </h2>
          <p style={{ font: `400 14px/1.5 ${SANS}`, color: MUTED, margin: '0 0 28px' }}>
            {distinct} {distinct === 1 ? 'question' : 'questions'} reviewed · {subject.title} · {MARK_BANK_LEVEL_LABELS[level]} level
          </p>

          {!reviewOnly && <ResultStatGrid items={[
            { label: 'Marks banked', value: claimed, tone: 'success' },
            { label: 'Available', value: available },
            { label: 'To revisit', value: Math.max(0, left) },
          ]} />}
          {unscoredCount > 0 && <p style={{ font: `400 14px/1.5 ${SANS}`, color: MUTED }}>
            {unscoredCount} {unscoredCount === 1 ? 'answer review had' : 'answer reviews had'} no calculated marks
            {reviewOnly ? '.' : unscoredCount === 1 ? ' and is excluded from these totals.' : ' and are excluded from these totals.'}
          </p>}

          {!reviewOnly && <div style={{ marginTop: 14, background: 'var(--mb-paper)', border: `1px solid ${HAIRLINE}`, borderRadius: 16, padding: '17px 19px', textAlign: 'left' }}>
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
          </div>}

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

  if (studio) return <ListeningStudio
    uid={uid} subjectId={subjectId} subjectLabel={subject.title} level={level}
    subjects={studioSubjects.map(s => ({ id: s.id, title: s.title }))} mySubjectIds={myStudioSubjectIds}
    chooseSubject={chooseSubject} chooseLevel={chooseLevel}
    cards={cards} memories={memories} loading={cardsLoading} error={cardsError}
    onRetry={() => setCardsAttempt(value => value + 1)} onGrade={handleGrade} onLeave={onLeaveStudio}
  />;

  return <MarkBankLibrary key={deckId} examDate={examDate} subjectId={subjectId} level={level} cards={reviewCards} state={deck} now={now}
    listeningCount={listeningCount} onOpenListeningStudio={onOpenListeningStudio}
    pages={libraryPages} onPagesChange={setLibraryPages}
    chooseSubject={chooseSubject} chooseLevel={chooseLevel} canSelectSubject={canSelectSubject}
    onStartingPoint={() => setScreen({ name: 'starting-point' })}
    onStart={startSession} busy={launchingTopicId!==null} ready={loaded&&!cardsLoading&&!cardsError}
    loading={cardsLoading} error={cardsError} onRetry={()=>setCardsAttempt(value=>value+1)} online={online}/>;
};
export default MarkBank;
