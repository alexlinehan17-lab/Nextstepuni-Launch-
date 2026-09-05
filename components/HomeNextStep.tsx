import React from 'react';
import { ArrowRight, ChevronRight } from 'lucide-react';
import { type StudyBlock } from './subjectData';
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
}

export default function HomeNextStep({ blocks, completions, hasProfile, ready = true, error = false, gamification, onStudy, onPlannedStudy, onPlan, onProgress }: Props) {
  const goal = gamification ? generateWeeklyGoals(gamification.currentRank.id, getWeekNumber()).find(item => item.metric === 'sessions') : undefined;
  const current = gamification?.weeklyGoalProgress.sessions ?? 0;
  const remaining = goal ? Math.max(0, goal.target - current) : 0;
  const done = blocks.filter((_block, index) => completions.includes(`block-${index}`)).length;
  const nextIndex = blocks.findIndex((_block, index) => !completions.includes(`block-${index}`));
  return <>
    <section className="home-today" data-coach="study" aria-labelledby="home-today-title">
      <div className="home-section-heading"><h2 id="home-today-title">Today’s plan</h2>{onPlan && <button type="button" onClick={onPlan}>Your plan <ArrowRight size={14} aria-hidden="true" /></button>}</div>
      {!ready ? <p role="status" className="home-supporting">Getting your plan ready…</p> : error ? <div className="home-empty-plan"><p role="status">Your plan couldn’t load.</p><span>Try opening your plan, or start a session without it.</span>{onPlan && <button type="button" className="home-text-action" onClick={onPlan}>Open your plan <ArrowRight size={15} aria-hidden="true" /></button>}{onStudy && <button type="button" className="home-text-action" onClick={onStudy}>Start a session <ArrowRight size={15} aria-hidden="true" /></button>}</div> : blocks.length ? <>
        {blocks.slice(0, 4).map((block, index) => {
          const complete = completions.includes(`block-${index}`);
          const type = block.sessionType === 'new-learning' ? 'New learning' : block.sessionType === 'practice' ? 'Practice' : 'Revision';
          return <button type="button" className="home-plan-row" key={`${block.subjectName}-${index}`} onClick={() => onPlannedStudy ? onPlannedStudy(block, index) : onStudy?.()} disabled={!onStudy && !onPlannedStudy} aria-label={`${complete ? 'Review' : 'Study'} ${block.subjectName}: ${type}, ${block.durationMinutes} minutes`}>
            <span className="home-subject-code" aria-hidden="true">{block.subjectName.replace(/[^A-Za-z]/g, '').slice(0, 2).toUpperCase()}</span>
            <span className="home-plan-copy"><strong>{block.subjectName}</strong><span>{type} · {block.durationMinutes} min{complete ? ' · Done' : index === nextIndex ? ' · Up next' : ''}</span></span><ChevronRight size={18} aria-hidden="true" />
          </button>;
        })}
        {blocks.length > 4 && onPlan && <button type="button" className="home-text-action" onClick={onPlan}>See all {blocks.length} sessions</button>}
        {done === blocks.length && <p className="home-supporting">Your planned sessions are done. Leave some room to rest.</p>}
      </> : <div className="home-empty-plan"><p>{hasProfile ? 'Room to breathe today.' : 'Make a little room for learning.'}</p><span>{hasProfile ? 'Nothing scheduled. Take the day off, or start a session when you’re ready.' : 'Add your subjects to build a plan that fits your week.'}</span>{(hasProfile ? onStudy : onPlan) && <button type="button" className="home-text-action" onClick={hasProfile ? onStudy : onPlan}>{hasProfile ? 'Start a session' : 'Set up your plan'} <ArrowRight size={15} aria-hidden="true" /></button>}</div>}
    </section>
    {goal && <section className="home-week" aria-label="Weekly study goal"><div className="home-section-heading"><span className="home-eyebrow">This week</span><button type="button" onClick={onProgress}>Progress <ArrowRight size={14} aria-hidden="true" /></button></div><h2>{remaining === 0 ? 'Your weekly goal, reached.' : `${remaining === 1 ? 'One more session' : `${remaining} more sessions`} to reach your goal.`}</h2><p className="home-supporting">{current} of {goal.target} sessions completed</p><div className="home-week-bars" role="progressbar" aria-label="Weekly study sessions" aria-valuemin={0} aria-valuemax={goal.target} aria-valuenow={Math.min(current, goal.target)}>{Array.from({ length: goal.target }, (_, index) => <span key={index} data-complete={index < current} />)}</div></section>}
  </>;
}
