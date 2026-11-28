import { useMemo, useState } from 'react';
import { Check, ChevronDown } from 'lucide-react';
import { Button } from '../../ui/Button';
import { List, Row } from '../../ui/List';
import { Sheet } from '../../ui/Sheet';
import { type GamificationState, generateWeeklyGoals, getWeekNumber } from '../../../gamificationConfig';
import type { StreakData } from '../../../hooks/useStreak';
import type { WeeklyChallengeState } from '../../../hooks/useWeeklyChallenge';
import type { StrategyMasteryMap, MasteryTier } from '../../../types';
import { STRATEGY_REGISTRY, type StudySessionRecord } from '../../../utils/strategyRegistry';
import type { CurriculumLevel } from '../../../utils/authUtils';
import { getAchievementsForCurriculum } from '../../../achievementData';
import AchievementGallery, { AchievementBadge } from '../../AchievementGallery';
import TermReviewCard from '../TermReviewCard';
import { Artwork } from './shared';
import { Bar, Duration, Figures, Section } from './ProgressParts';

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
  const rankProgress = Math.max(0, Math.min(100, state.rankProgress));
  const dateLabel = (id: string) => state.achievementTimestamps[id] ? new Date(state.achievementTimestamps[id]).toLocaleDateString('en-IE', { day: 'numeric', month: 'short' }) : 'Part of your story';
  const claim = async () => {
    if (!weeklyChallenge || claiming) return;
    setClaiming(true); setClaimError(false);
    try { await weeklyChallenge.claimReward(); pointsReload?.(); } catch { setClaimError(true); } finally { setClaiming(false); }
  };
  const latest = recent[0];
  return <div className="pm-milestones mp-milestones">
    <Section ruled={false} className="mp-ms-top">
      <div className="mp-ms-intro">
        <div className="mp-sec-head"><p className="t-label mp-label">Your learning record</p><h2 className="t-title mp-title">The work adds up.</h2></div>
        <p className="t-sub mp-ms-sub">A record of the time, habits and small steps you have made your own.</p>
      </div>
      <div className="mp-rank" aria-label="Study Passport — all-time record">
        <div className="mp-rank-row">
          <Artwork src="/assets/star-crew/personal/07-maker.png" size={76} />
          <div className="mp-rank-text"><p className="t-label mp-label">Your rank</p><h3 className="t-heading mp-heading">{state.currentRank.title}</h3>
            <p className="t-meta">{state.nextRank ? `${Math.max(0, state.nextRank.minPoints - state.totalPointsEarned).toLocaleString()} points to ${state.nextRank.title}` : 'Highest rank reached.'}</p></div>
          <span className="mp-big mp-rank-pct">{rankProgress}<small>%</small></span>
        </div>
        <div className="mp-rankbar" role="progressbar" aria-label="Rank progress" aria-valuenow={rankProgress} aria-valuemin={0} aria-valuemax={100}
          aria-valuetext={`${rankProgress}% of the way from ${state.currentRank.title} to ${state.nextRank?.title ?? 'the top'}`}><i style={{ width: `${rankProgress}%` }} /></div>
        <p className="t-meta">{`${state.totalPointsEarned.toLocaleString()} XP earned`}{pointsAvailable !== undefined ? ` · ${pointsAvailable.toLocaleString()} JP available to spend` : ''}</p>
      </div>
      <Figures className="mp-figs--four" items={[
        { name: 'Day streak', value: streak.currentStreak.toLocaleString(), unit: 'days', description: `Your longest was ${streak.longestStreak.toLocaleString()} days.` },
        { name: 'Sessions', value: sessions.length.toLocaleString() },
        { name: 'Focused time', value: <Duration minutes={minutes} /> },
        { name: 'Badges', value: earned.length, unit: `/ ${visible.length}` },
      ]} />
      <p className="t-meta mp-ms-longest">{`Longest streak: ${streak.longestStreak.toLocaleString()} days.`}</p>
    </Section>
    <div className="mp-pair">
      <Section label={`This week · ${resetDays === 1 ? 'resets tomorrow' : `resets in ${resetDays} days`}`} title="Three useful targets." className="pm-targets">
        <div className="mp-bars">{weeklyGoals.map(goal => {
          const current = Math.max(0, state.weeklyGoalProgress[goal.metric] ?? 0);
          const done = current >= goal.target;
          return <div key={goal.id} role="progressbar" aria-label={goal.label} aria-valuenow={Math.min(current, goal.target)} aria-valuemin={0} aria-valuemax={goal.target}>
            <Bar title={goal.label} readout={`${Math.min(current, goal.target)} / ${goal.target}${done ? ' · done' : ''}`} share={Math.min(1, current / goal.target)} done={done} />
          </div>;
        })}</div>
        {weeklyChallenge?.isLoaded && weeklyChallenge.challenge && <details className="pm-challenge mp-disclosure"><summary className="ui-part"><span className="mp-disclosure-text"><span className="t-meta">Weekly challenge</span><span className="t-row">{weeklyChallenge.challenge.title}</span></span><span className="t-readout">{weeklyChallenge.isClaimed ? 'Claimed' : `${Math.min(weeklyChallenge.current, weeklyChallenge.challenge.target)} / ${weeklyChallenge.challenge.target}`}</span><ChevronDown className="ui-icon mp-chev" width={20} height={20} strokeWidth={1.75} aria-hidden="true" /></summary>
          <div className="mp-disclosure-body"><p className="t-sub">{weeklyChallenge.challenge.description}</p>{weeklyChallenge.isClaimed ? <p className="t-body pm-claim-state"><Check className="ui-icon" size={16} aria-hidden="true" />Reward claimed</p> : weeklyChallenge.isCompleted ? <Button onClick={claim} aria-busy={claiming || undefined}>{claiming ? 'Claiming…' : `Claim ${weeklyChallenge.challenge.rewardPoints} JP`}</Button> : <p className="t-meta">{weeklyChallenge.challenge.rewardPoints} JP when complete.</p>}{claimError && <p role="alert" className="t-body">The reward could not be claimed. Please try again.</p>}</div></details>}
      </Section>
      <Section label={`Recognition · ${earned.length} earned`} title="Marks of progress." className="pm-achievements">
        <List label="Achievements">
          <Row title="Achievement gallery" meta={latest ? `Latest: ${latest.title}, ${dateLabel(latest.id)}` : 'Every collection starts with a first step.'}
            label={gallery ? 'Close gallery' : 'Open achievement gallery'} onPress={() => setGallery(!gallery)} />
        </List>
        {recent.length ? <div className="pm-badge-shelf mp-badges">{recent.map(item => <button type="button" className="ui-part" key={item.id} onClick={() => setBadgeId(item.id)}><AchievementBadge achievementId={item.id} size={64} /><span className="t-meta mp-badge-name">{item.title}</span><span className="t-meta">{dateLabel(item.id)}</span></button>)}</div> : null}
      </Section>
    </div>
    {gallery && <section id="progress-achievement-gallery" className="mp-sec mp-sec--ruled pm-gallery" aria-label="Achievement gallery"><div className="mp-sec-headrow"><div className="mp-sec-head"><p className="t-label mp-label">Achievement gallery</p><h2 className="t-heading mp-heading">The collection so far.</h2></div></div><AchievementGallery unlockedAchievements={state.unlockedAchievements} achievementTimestamps={state.achievementTimestamps} curriculumLevel={curriculumLevel} showHeader={false} /></section>}
    <Section label={`Learning methods · ${methods.length} method${methods.length === 1 ? '' : 's'}`} title="From knowing to doing." className="pm-methods">
      <p className="t-sub">Techniques you have brought into your learning.</p>
      {methods.length ? <div className="mp-method-stages">{methods.map(item => <details key={item.moduleId} className="mp-disclosure"><summary className="ui-part"><span className="mp-disclosure-text"><span className="t-row">{item.strategyName}</span><span className="t-meta">{item.record.sessionCount} session{item.record.sessionCount === 1 ? '' : 's'} · {tiers[item.record.tier].label}</span></span><span className="mp-steps" aria-hidden="true">{[1, 2, 3, 4].map(level => <i key={level} data-on={level <= tiers[item.record.tier].level || undefined} />)}</span><ChevronDown className="ui-icon mp-chev" width={20} height={20} strokeWidth={1.75} aria-hidden="true" /></summary><div className="mp-disclosure-body"><p className="t-sub">{item.description}.{item.record.subjectsSeen.length > 0 && <> Used in {item.record.subjectsSeen.join(', ')}.</>}</p></div></details>)}</div>
        : <p className="t-meta">Complete a strategy module, then use that technique during a study session to begin tracking it here.</p>}
    </Section>
    <Section label="Personal records" title="Best efforts." className="pm-best">
      <p className="t-sub">A few days and weeks to remember. Every session has its place.</p>
      <div className="mp-pair mp-pair--tight">{recordGroups.map(group => <section key={group.title} aria-labelledby={`pm-best-${group.records[0].key}`}>
        <h3 id={`pm-best-${group.records[0].key}`} className="t-row">{group.title}</h3>
        <Figures className="mp-figs--two" items={group.records.map(record => ({ name: record.label, value: state.personalBests[record.key] > 0 ? state.personalBests[record.key].toLocaleString() : '–', description: state.personalBests[record.key] > 0 ? undefined : 'Yet to record' }))} />
      </section>)}</div>
    </Section>
    <TermReviewCard sessions={sessions} streak={streak} />
    <Sheet open={Boolean(badge)} onClose={() => setBadgeId(null)} title="Achievement earned" titleSize="small" closeLabel="Close achievement">
      {badge && <div className="mp-badge-sheet"><AchievementBadge achievementId={badge.id} size={110} /><h2 id="pm-badge-title" className="t-title">{badge.title}</h2><p className="t-sub">{badge.description}</p><p className="t-meta">{dateLabel(badge.id)}</p></div>}
    </Sheet>
  </div>;
}
