import React from 'react';
import { ArrowRight } from 'lucide-react';
import { Button } from '../approved-ui-runtime';
import { SESSION_EXTENSION_MINUTES, STUDY_SESSION_POINTS } from '../../studySessionData';
import StudyCompletionLayout from './StudyCompletionLayout';

interface Props {
  subject: string;
  elapsedSeconds: number;
  extendedMinutes: number;
  extensionBonus: number;
  sessionPoints: number;
  onKeepGoing: (minutes: number) => void;
  onFinish: () => void;
}

export default function StudyTimeUp({ subject, elapsedSeconds, extendedMinutes, extensionBonus, sessionPoints, onKeepGoing, onFinish }: Props) {
  return <StudyCompletionLayout kind="timeup" title={extendedMinutes > 0 ? 'You kept going.' : 'Time’s up.'}
    description="Keep going for a little longer, or save the work you’ve done."
    subject={subject} seconds={elapsedSeconds} points={sessionPoints}>
    <div className="sc-finish-action" data-study-arrive>
      <Button className="sc-primary" onClick={onFinish}>Finish and log <ArrowRight size={18} aria-hidden="true" /></Button>
      {extensionBonus > 0 && <p className="sc-note">Includes +{extensionBonus} JP for finishing your extra time.</p>}
    </div>
    <section className="sc-extend" aria-labelledby="sc-keep-going" data-study-arrive>
      <h2 id="sc-keep-going">Need a little longer?</h2>
      <p className="sc-note">Add time to this session.</p>
      <div className="sc-extensions">
        {SESSION_EXTENSION_MINUTES.map(minutes => <Button key={minutes} variant="outline" className="sc-secondary" onClick={() => onKeepGoing(minutes)} aria-label={`Keep going for ${minutes} more minutes`}>+{minutes} min</Button>)}
      </div>
      <p className="sc-note">Extra minutes count towards your JP. Finish them and earn +{STUDY_SESSION_POINTS.EXTENSION_COMPLETED} JP.</p>
    </section>
  </StudyCompletionLayout>;
}
