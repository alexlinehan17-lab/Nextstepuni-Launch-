import React, { lazy, Suspense, useEffect, useState } from 'react';
import type { StudentSubject } from '../subjectData';
import type { StudyTopicSelection } from '../../types/studyTopics';
import type { LoadedQuiz } from './quiz/studyQuizPlan';
import StudySessionSaved from './StudySessionSaved';
import StudyQuizInvitation from './StudyQuizInvitation';

const StudySessionQuiz = lazy(() => import('./quiz/StudySessionQuiz'));

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
  const [quiz, setQuiz] = useState<LoadedQuiz | null>();
  const [choice, setChoice] = useState<'offered' | 'accepted' | 'finished'>('offered');
  useEffect(() => {
    if (!quizEnabled) return;
    let current = true;
    void import('./quiz/studyQuizPlan')
      .then(({ loadQuiz }) => loadQuiz({ uid, subjectName: subject, topicSelection, profileSubjects, examDate, now: Date.now() }))
      .then(value => { if (current) setQuiz(value); })
      .catch(() => { if (current) setQuiz(null); });
    return () => { current = false; };
  }, [quizEnabled, uid, subject, topicSelection, profileSubjects, examDate]);
  const finish = () => setChoice('finished');
  // The receipt/debrief has already been saved. Keep the final screen out of
  // this step so it only appears after declining, leaving or finishing questions.
  if (!quizEnabled || choice === 'finished' || quiz === null) {
    return <StudySessionSaved subject={subject} seconds={seconds} points={points} character={character} onIsland={onIsland} onStudyAgain={onStudyAgain} />;
  }
  return <>
    <div className="sq-completion-stage" aria-hidden={quiz ? true : undefined}>{!quiz && <p role="status">Your session is saved. Checking for topic questions…</p>}</div>
    {choice === 'offered' && quiz && <StudyQuizInvitation subject={subject} topicLabel={quiz.topicLabel} questionCount={quiz.cards.length}
      hasStudiedTopics={Boolean(topicSelection?.topicIds.length)} character={character} onOpen={onInvitationOpen} onAccept={() => setChoice('accepted')} onDecline={finish} />}
    {choice === 'accepted' && quiz && <Suspense fallback={<p className="sc-loading" role="status">Opening your questions…</p>}>
      <StudySessionQuiz uid={uid} subject={subject} seconds={seconds} topicSelection={topicSelection} profileSubjects={profileSubjects} examDate={examDate} initialQuiz={quiz} onDone={finish} onSkip={finish} />
    </Suspense>}
  </>;
}
