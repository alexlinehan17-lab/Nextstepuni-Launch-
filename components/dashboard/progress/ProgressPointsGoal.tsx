import { Button } from '../../approved-ui-runtime';
import { Surface, Eyebrow } from './shared';
import { CAO_MAX_POINTS, caoEvidenceLabel, caoGapLabel, type CaoGoalStanding } from './caoGoal';

const position = (points: number) => `${Math.min(100, Math.max(0, points / CAO_MAX_POINTS * 100))}%`;

/** Where the student is against the CAO points they are aiming for. */
export function ProgressPointsGoal({ standing, onEditGrades, onAddMockResult }: {
  standing: CaoGoalStanding;
  onEditGrades?: () => void;
  onAddMockResult?: () => void;
}) {
  if (standing.status === 'hidden') return null;

  // Both actions keep a visible outline: buttons must look clickable before hover.
  const gradesButton = onEditGrades && <Button key="grades" variant="outline" className="nsu-ink-outline" onClick={onEditGrades}>
    {standing.status === 'no-goal' ? 'Set your target grades' : 'Update your grades'}
  </Button>;
  const mockButton = onAddMockResult && <Button key="mock" variant="outline" className="nsu-ink-outline" onClick={onAddMockResult}>Add a mock result</Button>;
  const actions = (primary: 'grades' | 'mock') => <div className="pr-goal-actions">
    {primary === 'grades' ? [gradesButton, mockButton] : [mockButton, gradesButton]}
  </div>;

  if (standing.status === 'no-goal') {
    return <Surface className="pr-goal pr-goal-empty" label="CAO points goal">
      <div><Eyebrow>CAO points</Eyebrow><h2>Set a goal to see the gap.</h2>
        <p>Choose a target grade for each subject and your goal points appear here, beside where you are now.</p></div>
      {actions('grades')}
    </Surface>;
  }

  if (standing.status === 'no-current') {
    return <Surface className="pr-goal pr-goal-empty" label="CAO points goal">
      <div><Eyebrow>CAO points</Eyebrow><h2>Your goal: <span className="pr-goal-number">{standing.goal}</span> points.</h2>
        <p>Add a mock result or your current grades to see how far you are from it.</p></div>
      {actions('mock')}
    </Surface>;
  }

  const { current, goal, gap, evidence } = standing;
  const reached = gap <= 0;
  const gapLabel = caoGapLabel(gap);
  return <Surface className="pr-goal" label="CAO points against your goal">
    <div className="pr-goal-figures">
      <Eyebrow>CAO points</Eyebrow>
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
      <p className="pr-goal-source">{caoEvidenceLabel(evidence)} Best six subjects, with the Higher Maths bonus.</p>
    </div>
    {actions('mock')}
  </Surface>;
}
