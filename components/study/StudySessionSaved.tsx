import React from 'react';
import { ArrowUpRight } from 'lucide-react';
import { Button } from '../approved-ui-runtime';
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
      {onIsland && <Button className="sc-primary" onClick={onIsland}>Spend them on your island <ArrowUpRight size={18} aria-hidden="true" /></Button>}
      <Button variant="outline" className="sc-secondary" onClick={onStudyAgain}>Back to the study room</Button>
    </div>
  </StudyCompletionLayout>;
}
