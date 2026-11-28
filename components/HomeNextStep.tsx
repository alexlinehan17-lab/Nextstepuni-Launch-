import React from 'react';
import SubjectAvatar from './SubjectAvatar';
import { TextButton, Button } from './ui/Button';
import { List, Row } from './ui/List';
import { EmptyState } from './ui/States';
import { getAvatarUrl } from '../utils/authUtils';
import { getBlockId, type StudyBlock } from './subjectData';
import { generateWeeklyGoals, getWeekNumber, type GamificationState } from '../gamificationConfig';
import './home-next-step.css';

interface Props {
  blocks: StudyBlock[];
  completions: string[];
  hasProfile: boolean;
  ready?: boolean;
  error?: boolean;
  gamification?: GamificationState | null;
  onStudy?: () => void;
  onPlannedStudy?: (block: StudyBlock, index: number) => void;
  onPlan?: () => void;
  onProgress: () => void;
  /** Which part to draw: today's plan (straight under Start on a phone), the
   *  weekly goal (under the week), or both, one after the other. */
  part?: 'today' | 'goal' | 'both';
}

export default function HomeNextStep({ blocks, completions, hasProfile, ready = true, error = false, gamification, onStudy, onPlannedStudy, onPlan, onProgress, part = 'both' }: Props) {
  const goal = gamification ? generateWeeklyGoals(gamification.currentRank.id, getWeekNumber()).find(item => item.metric === 'sessions') : undefined;
  const current = gamification?.weeklyGoalProgress.sessions ?? 0;
  const remaining = goal ? Math.max(0, goal.target - current) : 0;
  const done = blocks.filter((block, index) => (completions.includes(getBlockId(block, index)) || ('status' in block && block.status === 'completed'))).length;
  const nextIndex = blocks.findIndex((block, index) => !(completions.includes(getBlockId(block, index)) || ('status' in block && block.status === 'completed')));
  const today = <section className="home-today" data-coach="study" aria-labelledby="home-today-title">
    <div className="home-section-heading"><h2 id="home-today-title" className="t-heading">Today’s plan</h2>{onPlan && <TextButton arrow="forward" onClick={onPlan}>Your plan</TextButton>}</div>
    {!ready ? <p role="status" className="home-supporting">Getting your plan ready…</p> : error ? <div className="home-empty-plan"><p role="status">Your plan couldn’t load.</p><span>Try opening your plan, or start a session without it.</span>{onPlan && <TextButton arrow="forward" onClick={onPlan}>Open your plan</TextButton>}{onStudy && <TextButton arrow="forward" onClick={onStudy}>Start a session</TextButton>}</div> : blocks.length ? <>
      <List className="home-plan-list">
        {blocks.slice(0, 4).map((block, index) => {
          const complete = (completions.includes(getBlockId(block, index)) || ('status' in block && block.status === 'completed'));
          const type = block.sessionType === 'new-learning' ? 'New learning' : block.sessionType === 'practice' ? 'Practice' : 'Revision';
          return <Row key={`${block.subjectName}-${index}`} className="home-plan-row"
            art={<SubjectAvatar subject={block.subjectName} bare />}
            title={block.subjectName}
            meta={<>{type} · {block.durationMinutes} min{complete ? ' · Done' : index === nextIndex ? <> · <span className="home-up-next">Up next</span></> : ''}</>}
            label={`${complete ? 'Review' : 'Study'} ${block.subjectName}: ${type}, ${block.durationMinutes} minutes`}
            onPress={() => (onPlannedStudy ? onPlannedStudy(block, index) : onStudy?.())} />;
        })}
      </List>
      {blocks.length > 4 && onPlan && <TextButton arrow="forward" onClick={onPlan}>See all {blocks.length} sessions</TextButton>}
      {done === blocks.length && <p className="home-supporting">Your planned sessions are done. Leave some room to rest.</p>}
    </> : <EmptyState className="home-empty" art={getAvatarUrl(hasProfile ? 'star-crew:snoozer' : 'star-crew:maker')} artSize={96}
      title={hasProfile ? 'Room to breathe today.' : 'Make a little room for learning.'}
      line={hasProfile ? 'Nothing scheduled. Take the day off, or start a session when you’re ready.' : 'Add your subjects to build a plan that fits your week.'}
      action={(hasProfile ? onStudy : onPlan) ? <Button onClick={hasProfile ? onStudy : onPlan} arrow="forward">{hasProfile ? 'Start a session' : 'Set up your plan'}</Button> : undefined} />}
  </section>;
  const week = goal ? <section className="home-week" aria-label="Weekly study goal">
    <p className="t-label home-eyebrow">This week’s goal</p>
    <h3 className="t-row">{remaining === 0 ? 'Your weekly goal, reached.' : `${remaining === 1 ? 'One more session' : `${remaining} more sessions`} to reach your goal.`}</h3>
    <div className="home-week-bars" role="progressbar" aria-label="Weekly study sessions" aria-valuemin={0} aria-valuemax={goal.target} aria-valuenow={Math.min(current, goal.target)}>{Array.from({ length: goal.target }, (_, index) => <span key={index} data-complete={index < current} />)}</div>
    <p className="t-meta">{current} of {goal.target} sessions completed</p>
    {part === 'both' && <TextButton arrow="forward" onClick={onProgress}>Progress</TextButton>}
  </section> : null;
  if (part === 'today') return today;
  if (part === 'goal') return week;
  return <>{today}{week}</>;
}
