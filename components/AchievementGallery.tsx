import React, { useState } from 'react';
import type { AchievementCategory, AchievementDefinition } from '../gamificationConfig';
import { getAchievementById, getAchievementsForCurriculum } from '../achievementData';
import type { CurriculumLevel } from '../utils/authUtils';
import CrewIllustration from './CrewIllustration';
import './achievement-stamps.css';

const CHARACTERS: Record<AchievementCategory, string> = {
  modules: 'reader', timetable: 'maker', streaks: 'skater', reflection: 'hugger',
  'north-star': 'stargazer', mastery: 'beanie', journey: 'musician',
};
const MILESTONE_CHARACTERS: Record<string, string> = {
  'first-step': 'beanie', 'getting-started': 'reader', 'first-module': 'maker',
  'getting-serious': 'stargazer',
};
const CATEGORIES: { id: AchievementCategory | 'all'; label: string }[] = [
  { id: 'all', label: 'All' }, { id: 'modules', label: 'Learning' },
  { id: 'timetable', label: 'Study' }, { id: 'streaks', label: 'Showing up' },
  { id: 'reflection', label: 'Reflection' }, { id: 'north-star', label: 'North Star' },
  { id: 'mastery', label: 'Mastery' }, { id: 'journey', label: 'Journey' },
];

/** Keep every earned milestone; surface just two next steps per category. */
export function curateAchievements(achievements: AchievementDefinition[], unlocked: Set<string>, showAll: boolean) {
  const upcoming: Partial<Record<AchievementCategory, number>> = {};
  return achievements.filter(achievement => {
    if (unlocked.has(achievement.id)) return true;
    if (achievement.isHidden) return false;
    upcoming[achievement.category] = (upcoming[achievement.category] ?? 0) + 1;
    return showAll || upcoming[achievement.category]! <= 2;
  }).sort((a, b) => Number(unlocked.has(b.id)) - Number(unlocked.has(a.id)));
}

export const AchievementBadge: React.FC<{ achievementId: string; size?: number; locked?: boolean }> = ({ achievementId, size = 44, locked = false }) => {
  const achievement = getAchievementById(achievementId);
  if (!achievement) return null;
  return <div className={`crew-stamp${locked ? ' is-upcoming' : ''}`} style={{ width: size, height: size }} aria-hidden="true"><CrewIllustration character={`star-crew:${MILESTONE_CHARACTERS[achievement.id] ?? CHARACTERS[achievement.category]}`} /></div>;
};

interface Props {
  unlockedAchievements: string[]; achievementTimestamps: Record<string, number>;
  curriculumLevel?: CurriculumLevel; showHeader?: boolean;
}
export default function AchievementGallery({ unlockedAchievements, achievementTimestamps, curriculumLevel = 'senior', showHeader = true }: Props) {
  const [category, setCategory] = useState<AchievementCategory | 'all'>('all');
  const [showAll, setShowAll] = useState(false);
  const unlocked = new Set(unlockedAchievements);
  const available = getAchievementsForCurriculum(curriculumLevel);
  const collected = available.filter(achievement => unlocked.has(achievement.id)).length;
  const curated = curateAchievements(available, unlocked, showAll);
  const displayed = curated.filter(achievement => category === 'all' || achievement.category === category);
  return <section className="crew-achievements" aria-label="Achievement collection">
    {showHeader && <div className="crew-achievement-heading"><div><span className="crew-eyebrow">Small steps, collected.</span><h3>Your stamp collection.</h3></div><span>{collected} collected</span></div>}
    <div className="crew-achievement-toolbar"><p>{collected ? 'A little proof of the work you put in.' : 'Every collection starts with a first step.'}</p><button type="button" className="crew-link" aria-pressed={showAll} onClick={() => setShowAll(value => !value)}>{showAll ? 'Show the essentials' : 'Explore all milestones'}</button></div>
    <div className="crew-achievement-tabs" role="group" aria-label="Achievement categories">{CATEGORIES.map(item => <button type="button" key={item.id} aria-pressed={category === item.id} onClick={() => setCategory(item.id)}>{item.label}</button>)}</div>
    <div className="crew-stamp-grid">{displayed.map(achievement => {
      const earned = unlocked.has(achievement.id);
      const timestamp = achievementTimestamps[achievement.id];
      return <article className={`crew-stamp-card${earned ? ' is-collected' : ''}`} key={achievement.id}>
        <span className="crew-stamp-status">{earned ? 'Collected' : 'A step ahead'}</span>
        <AchievementBadge achievementId={achievement.id} size={118} locked={!earned} />
        <h4>{achievement.title}</h4><p>{achievement.description}</p>
        <span className="crew-stamp-date">{earned ? timestamp ? new Date(timestamp).toLocaleDateString('en-IE', { day: 'numeric', month: 'short', year: 'numeric' }) : 'Part of your story' : 'Yours to work towards'}</span>
      </article>;
    })}</div>
    {!showAll && <p className="crew-achievement-caption">Your collected stamps, plus two upcoming milestones in each category. Explore all milestones whenever you’re curious.</p>}
  </section>;
}
