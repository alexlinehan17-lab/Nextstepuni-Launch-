/** Real Mark Bank practice, after the study session has been safely saved. */
import React, { useCallback, useEffect, useRef, useState, type ReactNode } from 'react';
import { Check, Maximize2, Minimize2 } from 'lucide-react';
import KobraScope, { Dialog, DialogContent, DialogDescription, DialogTitle, useSoundMuted } from '../../approved-ui-runtime';
import { TopBar } from '../../ui/Bars';
import { Button, Glyph } from '../../ui/Button';
import { OverScreen } from '../../ui/OverScreen';
import SessionScreen, { type SessionCardResult, type SessionResponse } from '../../MarkBank/SessionScreen';
import { ensureDeck, commitReview, memoryFor, readLocal } from '../../MarkBank/store';
import { grade as gradeCard, retentionFor } from '../../MarkBank/scheduler';
import { useDeckSound } from '../../immersiveDeck/useDeckSound';
import StudySoundToggle from '../StudySoundToggle';
import { formatStudyTime } from '../../../utils/studyTime';
import type { StudyTopicSelection } from '../../../types/studyTopics';
import type { StudentSubject } from '../../subjectData';
import { loadQuiz, quizCardTopic, type LoadedQuiz, type QuizResult } from './studyQuizPlan';
import { recordStudyQuizResults } from '../../../services/studyQuizEvidence';
import type { SecCard } from '../../../types/markBank';
import './study-quiz.css';

interface Props {
  uid: string;
  subject: string;
  seconds?: number;
  topicSelection?: StudyTopicSelection;
  profileSubjects?: StudentSubject[];
  examDate?: string | null;
  initialQuiz?: LoadedQuiz;
  onDone: (results: QuizResult[]) => void;
  onSkip: () => void;
  now?: () => number;
}

/** A phone (under 768px): the review is a full screen of its own, as the practice card is. */
const usePhone = () => {
  const query = '(max-width: 767px)';
  const [phone, setPhone] = useState(() => typeof window !== 'undefined' && Boolean(window.matchMedia?.(query).matches));
  useEffect(() => {
    const media = window.matchMedia?.(query);
    if (!media) return undefined;
    const update = () => setPhone(media.matches);
    media.addEventListener?.('change', update);
    return () => media.removeEventListener?.('change', update);
  }, []);
  return phone;
};

export default function StudySessionQuiz({ uid, subject, seconds = 0, topicSelection, profileSubjects, examDate, initialQuiz, onDone, onSkip, now = Date.now }: Props) {
  const [quiz, setQuiz] = useState<LoadedQuiz | null | undefined>(initialQuiz);
  const [failed, setFailed] = useState(false);
  const [attempt, setAttempt] = useState(0);
  const [finished, setFinished] = useState(false);
  const [revisit, setRevisit] = useState(false);
  const [expanded, setExpanded] = useState(false);
  const [results, setResults] = useState<QuizResult[]>([]);
  const committed = useRef(new Set<string>());
  const quizEvidence = useRef<{ card: SecCard; result: SessionCardResult }[]>([]);
  const quizSessionId = useRef<string | null>(null);
  const responses = useRef<Record<string, SessionResponse>>({});
  const phone = usePhone();
  const { play, setEnabled } = useDeckSound();
  const muted = useSoundMuted();
  useEffect(() => { setEnabled(!muted); }, [muted, setEnabled]);

  // Capture the saved session once. Typing, marking, muting or parent renders
  // must never reload the queue or change the student's selected topics.
  const input = useRef({ uid, subjectName: subject, topicSelection, profileSubjects, examDate, now: now() });
  useEffect(() => {
    if (initialQuiz) return;
    let live = true;
    setFailed(false);
    loadQuiz(input.current)
      .then(loaded => { if (live) setQuiz(loaded); })
      .catch(() => { if (live) setFailed(true); });
    return () => { live = false; };
  }, [attempt, initialQuiz]);
  useEffect(() => { if (quiz === null) onDone([]); }, [quiz, onDone]);

  const commit = useCallback((result: SessionCardResult) => {
    if (!quiz || committed.current.has(result.cardId)) return;
    const card = quiz.cards.find(item => item.id === result.cardId);
    if (!card) return;
    const t = now();
    ensureDeck(uid, quiz.deck.deckId, t);
    const local = readLocal(uid, quiz.deck.deckId);
    const after = gradeCard(memoryFor(local, card.id), result.grade, t, retentionFor(t, local.examTs));
    commitReview(uid, quiz.deck.deckId, card.id, after, t);
    committed.current.add(card.id);
    quizSessionId.current ??= crypto.randomUUID();
    quizEvidence.current.push({ card, result });
    recordStudyQuizResults(uid, input.current.topicSelection, quizEvidence.current, quizSessionId.current, t);
    setResults(previous => [...previous, { ...result, questionRef: card.questionRef }]);
  }, [quiz, uid, now]);

  const complete = () => { play('save'); setFinished(true); setRevisit(false); };
  const leave = () => { play('skip'); onDone(results); };
  const banner = <div className="sq-session-banner">
    <span><Check size={14} aria-hidden="true" /> Study session complete{seconds > 0 && <small> · {formatStudyTime(seconds)}</small>}</span>
    <StudySoundToggle muted={muted} />
  </div>;

  if (quiz && !finished) return <SessionScreen
    key={revisit ? 'revisit' : 'attempt'}
    paperLayout cards={quiz.cards} subjectLabel={subject}
    reviewPoolTotal={quiz.poolTotal} reviewPoolLabel={quiz.topicLabel ?? subject}
    onGrade={commit} onFinish={complete} onExit={revisit ? complete : leave}
    studyReview={{ banner, topicTitle: card => quizCardTopic(card, topicSelection), onCue: play,
      onResponse: (id, response) => { responses.current[id] = response; },
      responses: revisit ? responses.current : undefined, revisit }}
  />;

  const claimed = results.reduce((sum, result) => sum + result.marksClaimed, 0);
  const available = results.reduce((sum, result) => sum + result.marksAvailable, 0);
  const topics = new Set(quiz?.cards.map(card => quizCardTopic(card, topicSelection)));
  const heading = finished ? 'That’s your review.' : failed ? 'Your session is saved.' : 'Finding your questions…';
  const lede = finished ? `${results.length} ${results.length === 1 ? 'question' : 'questions'} reviewed · ${topics.size} ${topics.size === 1 ? 'topic' : 'topics'} from your session` : 'Mark Bank questions from the topics you studied.';
  // On a phone a full screen of its own (the shared OverScreen), as the practice card before it;
  // on a laptop today's dialog, drawn with the shared parts. One way out at the top left, Close;
  // on a laptop Expand gives it the whole window and Contract brings it back.
  const frame = (content: ReactNode) => phone
    ? <OverScreen label={`Session review: ${subject}`} onEscape={() => onDone(results)} className="sq-review sq-review--over">{content}</OverScreen>
    : <KobraScope><Dialog open={quiz !== null} onOpenChange={open => { if (!open) onDone(results); }}>
      <DialogContent className="mb-live-session-dialog sq-dialog sq-review" data-expanded={expanded} showCloseButton={false}>{content}</DialogContent>
    </Dialog></KobraScope>;
  return frame(<>
      <TopBar tool ruled className="sq-review-bar" leave={{ kind: 'close', onPress: leave, label: 'Close review' }} over="Session review" title={subject}
        action={phone ? undefined : <Button size="sm" aria-label={expanded ? 'Contract to compact view' : 'Expand to full screen'} aria-pressed={expanded}
          onClick={() => setExpanded(value => !value)}><Glyph icon={expanded ? Minimize2 : Maximize2} size={16} />{expanded ? 'Contract' : 'Expand'}</Button>} />
      {banner}
      <div className="sq-summary-body">
        <header className="sq-review-head">
          <p className="t-label sq-review-kicker">{subject} / Session review</p>
          {phone ? <h1 className="sq-review-title">{heading}</h1> : <DialogTitle className="sq-review-title">{heading}</DialogTitle>}
          {phone ? <p className="sq-review-lede">{lede}</p> : <DialogDescription className="sq-review-lede">{lede}</DialogDescription>}
        </header>
        {failed ? <><h2>Questions couldn’t load this time.</h2><p>Your study time and points are already saved.</p><Button onClick={() => setAttempt(value => value + 1)}>Try again</Button></> : !finished ? <p role="status">Loading questions for this session…</p> : <>
          <h2>A useful check on what you studied.</h2>
          <p>These are your self-assessed marks. Questions you skipped are left out of the total.</p>
          <ul className="sq-results" aria-label="Question by question">{quiz?.cards.map(card => {
            const result = results.find(item => item.cardId === card.id);
            return <li key={card.id} data-grade={!result ? 'skipped' : result.marksClaimed === result.marksAvailable ? 'got' : 'shaky'}>
              <span className="sq-result-dot" aria-hidden="true" />
              <div><strong>{quizCardTopic(card, topicSelection)}</strong><small>{card.questionRef} · {!result ? 'Skipped' : result.marksClaimed === result.marksAvailable ? 'Reviewed' : 'Worth another look'}</small></div>
              <span className="ui-readout">{result ? `${result.marksClaimed} / ${result.marksAvailable}` : '—'}</span>
            </li>;
          })}</ul>
          {results.length > 0 ? <p className="sq-summary-total"><strong>{claimed} / {available}</strong><span>self-assessed marks</span></p> : <p>No marks recorded. Your study session still counts.</p>}
        </>}
      </div>
      <footer className="sq-summary-footer"><span>Your study session is saved.</span><div>
        {finished && <Button size="lg" onClick={() => { play('swipe'); setRevisit(true); setFinished(false); }}>Review questions</Button>}
        <Button kind="main" size="lg" className="sq-primary" onClick={() => finished ? onDone(results) : onSkip()}>Done</Button>
      </div></footer>
    </>);
}
