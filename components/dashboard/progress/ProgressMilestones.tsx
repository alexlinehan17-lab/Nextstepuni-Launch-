import { useEffect, useMemo, useRef, useState } from 'react';
import { ArrowRight, Check, ChevronDown, X } from 'lucide-react';
import { Button } from '../../approved-ui-runtime';
import { type GamificationState, generateWeeklyGoals, getWeekNumber } from '../../../gamificationConfig';
import type { StreakData } from '../../../hooks/useStreak';
import type { WeeklyChallengeState } from '../../../hooks/useWeeklyChallenge';
import type { StrategyMasteryMap, MasteryTier } from '../../../types';
import { STRATEGY_REGISTRY, type StudySessionRecord } from '../../../utils/strategyRegistry';
import type { CurriculumLevel } from '../../../utils/authUtils';
import { getAchievementsForCurriculum } from '../../../achievementData';
import AchievementGallery, { AchievementBadge } from '../../AchievementGallery';
import TermReviewCard from '../TermReviewCard';
import { Artwork, Eyebrow } from './shared';

const tiers: Record<MasteryTier, { label: string; level: number }> = {
  none: { label: 'Not started', level: 0 }, learned: { label: 'Read', level: 1 },
  practiced: { label: 'Practised', level: 2 }, applied: { label: 'Applied', level: 3 }, habitual: { label: 'Habitual', level: 4 },
};
const recordGroups = [
  { title: 'In a day', records: [{ key: 'bestDayPoints', label: 'Points earned' }, { key: 'bestDaySections', label: 'Sections completed' }] },
  { title: 'In a week', records: [{ key: 'bestWeekPoints', label: 'Points earned' }, { key: 'bestWeekSessions', label: 'Study sessions' }] },
] as const;

export function ProgressMilestones({ state, streak, sessions, strategyMastery, weeklyChallenge, pointsAvailable, pointsReload, curriculumLevel }: {
  state: GamificationState; streak: StreakData; sessions: StudySessionRecord[]; strategyMastery: StrategyMasteryMap;
  weeklyChallenge?: WeeklyChallengeState | null; pointsAvailable?: number; pointsReload?: () => void; curriculumLevel: CurriculumLevel;
}) {
  const [gallery, setGallery] = useState(false);
  const [badgeId, setBadgeId] = useState<string | null>(null);
  const [claiming, setClaiming] = useState(false);
  const [claimError, setClaimError] = useState(false);
  const dialog = useRef<HTMLDialogElement>(null);
  useEffect(() => { if (badgeId) dialog.current?.showModal(); else if (dialog.current?.open) dialog.current.close(); }, [badgeId]);
  const available = useMemo(() => getAchievementsForCurriculum(curriculumLevel), [curriculumLevel]);
  const earned = available.filter(item => state.unlockedAchievements.includes(item.id));
  const visible = available.filter(item => !item.isHidden || state.unlockedAchievements.includes(item.id));
  const recent = [...earned].sort((a, b) => (state.achievementTimestamps[b.id] ?? 0) - (state.achievementTimestamps[a.id] ?? 0) || state.unlockedAchievements.indexOf(b.id) - state.unlockedAchievements.indexOf(a.id)).slice(0, 3);
  const badge = available.find(item => item.id === badgeId);
  const methods = STRATEGY_REGISTRY.map(item => ({ ...item, record: strategyMastery[item.moduleId] })).filter(item => item.record && item.record.tier !== 'none').sort((a, b) => tiers[b.record.tier].level - tiers[a.record.tier].level);
  const weeklyGoals = generateWeeklyGoals(state.currentRank.id, getWeekNumber());
  const day = new Date().getDay();
  const resetDays = day === 0 ? 1 : 8 - day;
  const minutes = Math.round(sessions.reduce((total, session) => total + Math.max(0, session.actualSeconds || 0), 0) / 60);
  const duration = minutes >= 60 ? `${Math.floor(minutes / 60)}h${minutes % 60 ? ` ${minutes % 60}m` : ''}` : `${minutes}m`;
  const rankProgress = Math.max(0, Math.min(100, state.rankProgress));
  const dateLabel = (id: string) => state.achievementTimestamps[id] ? new Date(state.achievementTimestamps[id]).toLocaleDateString('en-IE', { day: 'numeric', month: 'short' }) : 'Part of your story';
  const claim = async () => {
    if (!weeklyChallenge || claiming) return;
    setClaiming(true); setClaimError(false);
    try { await weeklyChallenge.claimReward(); pointsReload?.(); } catch { setClaimError(true); } finally { setClaiming(false); }
  };
  return <div className="pm-milestones lg:col-span-12">
    <article className="pr-paper pm-hero" aria-label="Study Passport — all-time record">
      <div className="pm-intro"><Eyebrow>Your learning record / Milestones</Eyebrow><h2>The work<br /><em>adds up.</em></h2><p>A record of the time, habits and small steps you have made your own.</p></div>
      <div className="pm-rank"><Artwork src="/assets/star-crew/personal/07-maker.png" size={90} /><div><Eyebrow>Your rank</Eyebrow><h2>{state.currentRank.title}</h2><p>{state.nextRank ? <><strong>{Math.max(0, state.nextRank.minPoints - state.totalPointsEarned).toLocaleString()}</strong> points to {state.nextRank.title}</> : 'Highest rank reached.'}</p></div>
        <div className="pm-rank-line"><span>{state.currentRank.title}</span><strong>{rankProgress}%</strong><span>{state.nextRank?.title ?? 'Complete'}</span><div role="progressbar" aria-label="Rank progress" aria-valuenow={rankProgress} aria-valuemin={0} aria-valuemax={100}><i style={{ width: `${rankProgress}%` }} /></div></div>
        <p className="pm-rank-totals"><strong>{state.totalPointsEarned.toLocaleString()}</strong> XP earned {pointsAvailable !== undefined && <span>{pointsAvailable.toLocaleString()} JP available to spend</span>}</p>
      </div>
      <dl className="pm-all-time">{[[streak.currentStreak, 'Day streak'], [streak.longestStreak, 'Longest streak'], [sessions.length, 'Sessions'], [duration, 'Focused time'], [`${earned.length} / ${visible.length}`, 'Achievements']].map(([value, label]) => <div key={label}><dt>{label}</dt><dd>{typeof value === 'number' ? value.toLocaleString() : value}</dd></div>)}</dl>
    </article>
    <div className="pm-middle">
      <article className="pr-paper pm-targets"><header><Eyebrow>This week / Resets {resetDays === 1 ? 'tomorrow' : `in ${resetDays} days`}</Eyebrow><h2>Three useful targets.</h2></header><div className="pm-target-list">{weeklyGoals.map((goal, index) => {
        const current = Math.max(0, state.weeklyGoalProgress[goal.metric] ?? 0);
        const progress = Math.min(100, current / goal.target * 100);
        return <div className="pm-target-row" key={goal.id}><span className="pm-target-number">{current >= goal.target ? <Check size={19} aria-label="Complete" /> : String(index + 1).padStart(2, '0')}</span><div><h3>{goal.label}</h3><div className="pm-target-track" role="progressbar" aria-label={goal.label} aria-valuenow={Math.min(current, goal.target)} aria-valuemin={0} aria-valuemax={goal.target}><i style={{ width: `${progress}%` }} /></div></div><strong>{Math.min(current, goal.target)}<span> / {goal.target}</span></strong></div>;
      })}</div>
      {weeklyChallenge?.isLoaded && weeklyChallenge.challenge && <details className="pm-challenge"><summary><span><small>Weekly challenge</small><strong>{weeklyChallenge.challenge.title}</strong></span><span>{weeklyChallenge.isClaimed ? 'Claimed' : `${Math.min(weeklyChallenge.current, weeklyChallenge.challenge.target)} / ${weeklyChallenge.challenge.target}`}<ChevronDown size={18} /></span></summary><div><p>{weeklyChallenge.challenge.description}</p>{weeklyChallenge.isClaimed ? <p className="pm-claim-state"><Check size={16} />Reward claimed</p> : weeklyChallenge.isCompleted ? <Button variant="outline" className="nsu-ink-outline" disabled={claiming} onClick={claim}>{claiming ? 'Claiming…' : `Claim ${weeklyChallenge.challenge.rewardPoints} JP`}</Button> : <p>{weeklyChallenge.challenge.rewardPoints} JP when complete.</p>}{claimError && <p role="alert">The reward could not be claimed. Please try again.</p>}</div></details>}
      </article>
      <article className="pr-paper pm-achievements"><header><div><Eyebrow>Recognition</Eyebrow><h2>Marks of progress.</h2></div><span className="pm-count">{earned.length} earned</span></header>
        {recent.length ? <div className="pm-badge-shelf">{recent.map(item => <button type="button" key={item.id} onClick={() => setBadgeId(item.id)}><AchievementBadge achievementId={item.id} size={76} /><strong>{item.title}</strong><small>{dateLabel(item.id)}</small></button>)}</div> : <p className="pm-empty">Every collection starts with a first step. Your earned milestones will appear here.</p>}
        <Button variant="ghost" className="pm-gallery-toggle" aria-expanded={gallery} aria-controls="progress-achievement-gallery" onClick={() => setGallery(!gallery)}>{gallery ? 'Close gallery' : 'Open achievement gallery'}<ArrowRight size={17} /></Button>
      </article>
    </div>
    {gallery && <section id="progress-achievement-gallery" className="pr-paper pm-gallery" aria-label="Achievement gallery"><header><Eyebrow>Achievement gallery</Eyebrow><h2>The collection so far.</h2></header><AchievementGallery unlockedAchievements={state.unlockedAchievements} achievementTimestamps={state.achievementTimestamps} curriculumLevel={curriculumLevel} showHeader={false} /></section>}
    <article className="pr-paper pm-methods"><header><div><Eyebrow>Learning methods</Eyebrow><h2>From knowing to doing.</h2><p>Techniques you have brought into your learning.</p></div><span className="pm-count">{methods.length} method{methods.length === 1 ? '' : 's'}</span></header>
      {methods.length ? <><div className="pm-method-head" aria-hidden="true"><span>Technique</span><span>Use in study</span><span>Stage</span></div>{methods.map(item => <details key={item.moduleId}><summary><strong>{item.strategyName}</strong><span>{item.record.sessionCount} session{item.record.sessionCount === 1 ? '' : 's'}</span><span className="pm-method-stage">{[1, 2, 3, 4].map(level => <i key={level} data-filled={level <= tiers[item.record.tier].level} aria-hidden="true" />)}<small>{tiers[item.record.tier].label}</small><ChevronDown size={16} /></span></summary><p>{item.description}.{item.record.subjectsSeen.length > 0 && <> Used in {item.record.subjectsSeen.join(', ')}.</>}</p></details>)}</> : <p className="pm-empty">Complete a strategy module, then use that technique during a study session to begin tracking it here.</p>}
    </article>
    <article className="pr-paper pm-best"><header><Eyebrow>Personal records</Eyebrow><h2>Best efforts.</h2><p>A few days and weeks to remember. Every session has its place.</p></header><div className="pm-record-groups">{recordGroups.map(group => <section key={group.title}><h3>{group.title}</h3><dl>{group.records.map(record => <div key={record.key}><dt>{record.label}</dt><dd>{state.personalBests[record.key] > 0 ? state.personalBests[record.key].toLocaleString() : <span className="pm-no-record">Yet to record</span>}</dd></div>)}</dl></section>)}</div></article>
    <TermReviewCard sessions={sessions} streak={streak} />
    <dialog ref={dialog} className="pm-badge-dialog" aria-labelledby="pm-badge-title" onClose={() => setBadgeId(null)} onCancel={() => setBadgeId(null)} onKeyDown={event => { if (event.key === 'Escape') { event.stopPropagation(); setBadgeId(null); } }} onClick={event => { if (event.target === event.currentTarget) setBadgeId(null); }}>{badge && <div><button type="button" className="pm-dialog-close" aria-label="Close achievement" onClick={() => setBadgeId(null)}><X size={20} /></button><AchievementBadge achievementId={badge.id} size={110} /><Eyebrow>Achievement earned</Eyebrow><h2 id="pm-badge-title">{badge.title}</h2><p>{badge.description}</p><small>{dateLabel(badge.id)}</small></div>}</dialog>
  </div>;
}
