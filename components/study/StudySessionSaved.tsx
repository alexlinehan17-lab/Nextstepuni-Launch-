import React from 'react';
import { Button } from '../ui/Button';
import StudyCompletionLayout from './StudyCompletionLayout';

interface Props {
  subject: string;
  seconds: number;
  points: number;
  character?: string;
  onIsland?: () => void;
  onStudyAgain: () => void;
}

export default function StudySessionSaved({ subject, seconds, points, character, onIsland, onStudyAgain }: Props) {
  return <StudyCompletionLayout kind="saved" title="Session saved."
    description="Your study time is on the record. Your Journey Points are ready to spend."
    subject={subject} seconds={seconds} points={points} character={character}>
    <div className="sc-saved-actions">
      {onIsland && <Button kind="main" size="lg" block arrow="forward" className="sc-main" onClick={onIsland}>Spend them on your island</Button>}
      <Button size="lg" block className="sc-second" onClick={onStudyAgain}>Back to the study room</Button>
    </div>
  </StudyCompletionLayout>;
}
