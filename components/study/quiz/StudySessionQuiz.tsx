/** Real Mark Bank practice, after the study session has been safely saved. */
import React, { useCallback, useEffect, useRef, useState } from 'react';
import { Check, Maximize2, Minimize2, X } from 'lucide-react';
import KobraScope, { Button, Dialog, DialogContent, DialogDescription, DialogTitle, useSoundMuted } from '../../approved-ui-runtime';
import SessionScreen, { type SessionCardResult, type SessionResponse } from '../../MarkBank/SessionScreen';
import { ensureDeck, commitReview, memoryFor, readLocal } from '../../MarkBank/store';
import { grade as gradeCard, retentionFor } from '../../MarkBank/scheduler';
import { useDeckSound } from '../../immersiveDeck/useDeckSound';
import StudySoundToggle from '../StudySoundToggle';
import { formatStudyTime } from '../../../utils/studyTime';
import type { StudyTopicSelection } from '../../../types/studyTopics';
import type { StudentSubject } from '../../subjectData';
import { loadQuiz, quizCardTopic, type LoadedQuiz, type QuizResult } from './studyQuizPlan';
import './study-quiz.css';

interface Props {
  uid: string;
  subject: string;
  seconds?: number;
  topicSelection?: StudyTopicSelection;
  profileSubjects?: StudentSubject[];
  examDate?: string | null;
  onDone: (results: QuizResult[]) => void;
  onSkip: () => void;
  now?: () => number;
}

export default function StudySessionQuiz({ uid, subject, seconds = 0, topicSelection, profileSubjects, examDate, onDone, onSkip, now = Date.now }: Props) {
  const [quiz, setQuiz] = useState<LoadedQuiz | null>();
  const [failed, setFailed] = useState(false);
  const [attempt, setAttempt] = useState(0);
  const [finished, setFinished] = useState(false);
  const [revisit, setRevisit] = useState(false);
  const [expanded, setExpanded] = useState(false);
  const [results, setResults] = useState<QuizResult[]>([]);
  const committed = useRef(new Set<string>());
  const responses = useRef<Record<string, SessionResponse>>({});
  const { play, setEnabled } = useDeckSound();
  const muted = useSoundMuted();
  useEffect(() => { setEnabled(!muted); }, [muted, setEnabled]);

  // Capture the saved session once. Typing, marking, muting or parent renders
  // must never reload the queue or change the student's selected topics.
  const input = useRef({ uid, subjectName: subject, topicSelection, profileSubjects, examDate, now: now() });
  useEffect(() => {
    let live = true;
    setFailed(false);
    loadQuiz(input.current)
      .then(loaded => { if (live) setQuiz(loaded); })
      .catch(() => { if (live) setFailed(true); });
    return () => { live = false; };
  }, [attempt]);
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
  return <KobraScope><Dialog open={quiz !== null} onOpenChange={open => { if (!open) onDone(results); }}>
    <DialogContent className="mb-live-session-dialog sq-dialog" data-expanded={expanded} showCloseButton={false}>
      {banner}
      <header className="mb-paper-session-heading">
        <div><p className="mb-kicker">{subject} / Session review</p>
          <DialogTitle>{finished ? 'That’s your review.' : failed ? 'Your session is saved.' : 'Finding your questions…'}</DialogTitle>
          <DialogDescription>{finished ? `${results.length} ${results.length === 1 ? 'question' : 'questions'} reviewed · ${topics.size} ${topics.size === 1 ? 'topic' : 'topics'} from your session` : 'Mark Bank questions from the topics you studied.'}</DialogDescription>
        </div>
        <div><Button variant="outline" aria-label={expanded ? 'Contract to compact view' : 'Expand to full screen'} aria-pressed={expanded} onClick={() => setExpanded(value => !value)}>{expanded ? <Minimize2 size={16} /> : <Maximize2 size={16} />}<span>{expanded ? 'Contract' : 'Expand'}</span></Button>
          <Button variant="outline" size="icon" aria-label="Close review" onClick={leave}><X size={18} /></Button></div>
      </header>
      <div className="sq-summary-body">
        {failed ? <><h2>Questions couldn’t load this time.</h2><p>Your study time and points are already saved.</p><Button variant="outline" onClick={() => setAttempt(value => value + 1)}>Try again</Button></> : !finished ? <p role="status">Loading questions for this session…</p> : <>
          <h2>A useful check on what you studied.</h2>
          <p>These are your self-assessed marks. Questions you skipped are left out of the total.</p>
          <ul className="sq-results" aria-label="Question by question">{quiz?.cards.map(card => {
            const result = results.find(item => item.cardId === card.id);
            return <li key={card.id} data-grade={!result ? 'skipped' : result.marksClaimed === result.marksAvailable ? 'got' : 'shaky'}>
              <span className="sq-result-dot" aria-hidden="true" />
              <div><strong>{quizCardTopic(card, topicSelection)}</strong><small>{card.questionRef} · {!result ? 'Skipped' : result.marksClaimed === result.marksAvailable ? 'Reviewed' : 'Worth another look'}</small></div>
              <span>{result ? `${result.marksClaimed} / ${result.marksAvailable}` : '—'}</span>
            </li>;
          })}</ul>
          {results.length > 0 ? <p className="sq-summary-total"><strong>{claimed} / {available}</strong><span>self-assessed marks</span></p> : <p>No marks recorded. Your study session still counts.</p>}
        </>}
      </div>
      <footer className="sq-summary-footer"><span>Your study session is saved.</span><div>
        {finished && <Button variant="outline" onClick={() => { play('swipe'); setRevisit(true); setFinished(false); }}>Review questions</Button>}
        <Button className="sq-primary" onClick={() => finished ? onDone(results) : onSkip()}>Done <Check size={16} aria-hidden="true" /></Button>
      </div></footer>
    </DialogContent>
  </Dialog></KobraScope>;
}
