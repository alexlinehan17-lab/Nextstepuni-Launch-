import React, { useEffect, useState } from 'react';
import type { StudentSubject } from '../subjectData';
import type { StudyTopicSelection } from '../../types/studyTopics';
import type { LoadedQuiz } from './quiz/studyQuizPlan';
import type StudySessionQuiz from './quiz/StudySessionQuiz';
import StudySessionSaved from './StudySessionSaved';
import StudyQuizInvitation from './StudyQuizInvitation';

type PreparedQuiz = { quiz: LoadedQuiz; Screen: typeof StudySessionQuiz };

interface Props {
  uid: string;
  subject: string;
  seconds: number;
  points: number;
  character?: string;
  topicSelection?: StudyTopicSelection;
  profileSubjects?: StudentSubject[];
  examDate?: string | null;
  quizEnabled: boolean;
  onIsland?: () => void;
  onStudyAgain: () => void;
  onInvitationOpen?: () => void;
}

/** The session is already saved. Opening questions always requires a new choice. */
export default function StudySessionCompletion({ uid, subject, seconds, points, character, topicSelection, profileSubjects, examDate, quizEnabled, onIsland, onStudyAgain, onInvitationOpen }: Props) {
  const [prepared, setPrepared] = useState<PreparedQuiz | null>();
  const [choice, setChoice] = useState<'offered' | 'accepted' | 'finished'>('offered');
  const finished = choice === 'finished';
  useEffect(() => {
    if (!quizEnabled || finished) return;
    let current = true;
    const settle = (value: PreparedQuiz | null) => {
      if (!current) return;
      current = false;
      window.clearTimeout(timeout);
      setPrepared(value);
    };
    // A slow connection must never hold the saved session hostage. Late loads
    // cannot reopen the invitation after the student continues or times out.
    const timeout = window.setTimeout(() => settle(null), 8000);
    // Prepare the interface as well as its cards before offering questions:
    // accepting the invitation then mounts the quiz in the same render.
    void Promise.all([
      import('./quiz/studyQuizPlan').then(({ loadQuiz }) => loadQuiz({ uid, subjectName: subject, topicSelection, profileSubjects, examDate, now: Date.now() })),
      import('./quiz/StudySessionQuiz'),
    ]).then(([quiz, { default: Screen }]) => settle(quiz ? { quiz, Screen } : null))
      .catch(() => settle(null));
    return () => { current = false; window.clearTimeout(timeout); };
  }, [quizEnabled, finished, uid, subject, topicSelection, profileSubjects, examDate]);
  const finish = () => setChoice('finished');
  // The receipt/debrief has already been saved. Keep the final screen out of
  // this step so it only appears after declining, leaving or finishing questions.
  if (!quizEnabled || finished || prepared === null) {
    return <StudySessionSaved subject={subject} seconds={seconds} points={points} character={character} onIsland={onIsland} onStudyAgain={onStudyAgain} />;
  }
  const quiz = prepared?.quiz;
  const QuizScreen = prepared?.Screen;
  return <>
    <div className="sq-completion-stage" aria-hidden={quiz ? true : undefined}>{!quiz && <div className="sq-completion-wait">
      <p role="status">Your session is saved. Checking for topic questions…</p>
      <button type="button" onClick={finish}>Continue without questions</button>
    </div>}</div>
    {choice === 'offered' && quiz && <StudyQuizInvitation subject={subject} topicLabel={quiz.topicLabel} questionCount={quiz.cards.length}
      hasStudiedTopics={Boolean(topicSelection?.topicIds.length)} character={character} onOpen={onInvitationOpen} onAccept={() => setChoice('accepted')} onDecline={finish} />}
    {choice === 'accepted' && quiz && QuizScreen && <QuizScreen uid={uid} subject={subject} seconds={seconds} topicSelection={topicSelection} profileSubjects={profileSubjects} examDate={examDate} initialQuiz={quiz} onDone={finish} onSkip={finish} />}
  </>;
}
