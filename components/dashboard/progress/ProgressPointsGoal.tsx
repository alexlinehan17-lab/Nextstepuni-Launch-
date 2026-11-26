import { Button, TextButton } from '../../ui/Button';
import { PaperSheet } from '../../ui/List';
import { CAO_MAX_POINTS, caoEvidenceLabel, caoGapLabel, type CaoGoalStanding } from './caoGoal';

const position = (points: number) => `${Math.min(100, Math.max(0, points / CAO_MAX_POINTS * 100))}%`;

/** Where the student is against the CAO points they are aiming for: the one
 *  raised sheet on My Progress, with today's orange bar and its goal mark
 *  (identity.md, "What must survive"). The second action is a text button. */
export function ProgressPointsGoal({ standing, onEditGrades, onAddMockResult }: {
  standing: CaoGoalStanding;
  onEditGrades?: () => void;
  onAddMockResult?: () => void;
}) {
  if (standing.status === 'hidden') return null;

  const gradesLabel = standing.status === 'no-goal' ? 'Set your target grades' : 'Update your grades';
  const actions = (primary: 'grades' | 'mock') => {
    const first = primary === 'grades' ? (onEditGrades ? { label: gradesLabel, press: onEditGrades } : null) : (onAddMockResult ? { label: 'Add a mock result', press: onAddMockResult } : null);
    const second = primary === 'grades' ? (onAddMockResult ? { label: 'Add a mock result', press: onAddMockResult } : null) : (onEditGrades ? { label: gradesLabel, press: onEditGrades } : null);
    if (!first && !second) return null;
    return <div className="pr-goal-actions">
      {first ? <Button block onClick={first.press}>{first.label}</Button> : null}
      {second ? first ? <TextButton onClick={second.press}>{second.label}</TextButton> : <Button block onClick={second.press}>{second.label}</Button> : null}
    </div>;
  };

  if (standing.status === 'no-goal') {
    return <PaperSheet className="pr-goal pr-goal-empty" label="CAO points goal">
      <div className="pr-goal-figures"><p className="t-label pr-goal-label">CAO points</p><h2 className="pr-goal-gap">Set a goal to see the gap.</h2>
        <p className="t-meta pr-goal-source">Choose a target grade for each subject and your goal points appear here, beside where you are now.</p></div>
      {actions('grades')}
    </PaperSheet>;
  }

  if (standing.status === 'no-current') {
    return <PaperSheet className="pr-goal pr-goal-empty" label="CAO points goal">
      <div className="pr-goal-figures"><p className="t-label pr-goal-label">CAO points</p><h2 className="pr-goal-gap">Your goal: <span className="pr-goal-number">{standing.goal}</span> points.</h2>
        <p className="t-meta pr-goal-source">Add a mock result or your current grades to see how far you are from it.</p></div>
      {actions('mock')}
    </PaperSheet>;
  }

  const { current, goal, gap, evidence } = standing;
  const reached = gap <= 0;
  const gapLabel = caoGapLabel(gap);
  return <PaperSheet className="pr-goal" label="CAO points against your goal">
    <div className="pr-goal-figures">
      <p className="t-label pr-goal-label">CAO points</p>
      <dl>
        <div><dt>Now</dt><dd className="pr-goal-number">{current}</dd></div>
        <div><dt>Goal</dt><dd className="pr-goal-number">{goal}</dd></div>
      </dl>
    </div>
    <div className="pr-goal-chart">
      <p className="pr-goal-gap" data-reached={reached}>{gapLabel}</p>
      <div className="pr-goal-bar" role="img"
        aria-label={`${current} points now, goal ${goal} points, out of ${CAO_MAX_POINTS}. ${gapLabel}.`}>
        <div className="pr-goal-track"><i data-reached={reached} style={{ width: position(current) }} /></div>
        <span className="pr-goal-marker" data-edge={goal / CAO_MAX_POINTS > 0.85} style={{ left: position(goal) }} aria-hidden="true"><b>Goal</b></span>
      </div>
      <div className="pr-goal-scale" aria-hidden="true"><span>0</span><span>{CAO_MAX_POINTS}</span></div>
      <p className="t-meta pr-goal-source">{caoEvidenceLabel(evidence)} Best six subjects, with the Higher Maths bonus.</p>
    </div>
    {actions('mock')}
  </PaperSheet>;
}
