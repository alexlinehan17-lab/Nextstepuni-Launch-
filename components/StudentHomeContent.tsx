import React from 'react';
import { ArrowRight, ArrowUpRight } from 'lucide-react';
import type { CourseData } from './Library';
import type { StudySessionRecord } from '../studySessionData';
import { ModulesIcon, InnovationZoneIcon, LearningPathsIcon, MyJourneyIcon } from './sectionIcons';
import { getLastVisit } from './lastVisited';
import { toDateKey } from './subjectData';
import Avatar from './Avatar';
import './student-screens.css';

export interface StudentHomeContentProps {
  uid?: string;
  userName?: string;
  userAvatarSeed?: string;
  hasUnreadNotifications?: boolean;
  onOpenMobileProfile?: () => void;
  allCourses: CourseData[];
  userProgress: Record<string, { unlockedSection: number }>;
  categoryTitles: Record<string, string>;
  studySessions?: StudySessionRecord[];
  pointsBalance?: number;
  onSelectModule: (id: string) => void;
  onGoToStudy?: () => void;
  onGoToModules: () => void;
  onGoToDashboard: () => void;
  onGoToLearningPaths: () => void;
  onGoToDirection?: () => void;
  onGoToJourney: () => void;
  onGoToInnovationZone: () => void;
  onOpenTool?: (id: string) => void;
}

export default function StudentHomeContent({ uid, userName, userAvatarSeed, hasUnreadNotifications, onOpenMobileProfile, allCourses, userProgress, categoryTitles, studySessions = [], pointsBalance = 0, onSelectModule, onGoToStudy, onGoToModules, onGoToDashboard, onGoToLearningPaths, onGoToDirection, onGoToJourney, onGoToInnovationZone, onOpenTool }: StudentHomeContentProps) {
  const now = new Date();
  const monday = new Date(now.getFullYear(), now.getMonth(), now.getDate() - (now.getDay() + 6) % 7);
  const days = Array.from({ length: 7 }, (_, i) => { const day = new Date(monday); day.setDate(day.getDate() + i); return toDateKey(day); });
  const sessions = studySessions.filter(session => days.includes(session.date) && session.date <= toDateKey(now));
  const minutes = Math.floor(sessions.reduce((sum, session) => sum + Math.max(0, session.actualSeconds || 0), 0) / 60);
  const duration = minutes >= 60 ? `${Math.floor(minutes / 60)}h ${minutes % 60}m` : `${minutes} min`;
  const visit = getLastVisit(uid);
  const recent = visit && Date.now() - visit.at <= 21 * 86400000 ? visit : null;
  const available = allCourses.filter(course => (userProgress[course.id]?.unlockedSection || 0) < course.sectionsCount);
  const course = available.find(item => recent?.kind === 'module' && recent.id === item.id) || available[0];
  const done = course ? Math.max(0, Math.min(userProgress[course.id]?.unlockedSection || 0, course.sectionsCount)) : 0;
  const firstName = userName?.trim().split(/\s+/)[0];
  const greeting = now.getHours() < 12 ? 'Good morning' : now.getHours() < 18 ? 'Good afternoon' : 'Good evening';
  const destinations = [
    { title: 'Learning Paths', copy: 'A little structure for what’s next.', action: 'Find your path', icon: <LearningPathsIcon />, go: onGoToLearningPaths },
    { title: 'My Direction', copy: 'Make room for your possibilities.', action: 'Visit your North Star', icon: <span className="sh-compass"><img src="/assets/training/north-star-compass.png" alt="" /></span>, go: onGoToDirection },
    { title: 'My Island', copy: `${pointsBalance.toLocaleString()} JP. Plenty of room to grow.`, action: 'Build your island', icon: <MyJourneyIcon />, go: onGoToJourney },
    { title: 'Launchpad', copy: 'Your tools for the work ahead.', action: 'Open your toolkit', icon: <InnovationZoneIcon />, go: onGoToInnovationZone, coach: 'launchpad' },
  ];
  return <main className="student-home">
    <div className="sh-date"><span className="student-eyebrow">{now.toLocaleDateString('en-IE', { weekday: 'long', day: 'numeric', month: 'long' })}</span>{onOpenMobileProfile && <button type="button" className="sh-profile" onClick={onOpenMobileProfile} aria-label="Open profile and settings"><Avatar seed={userAvatarSeed || userName || 'student'} className="h-10 w-10" />{hasUnreadNotifications && <i aria-label="Unread notifications" />}</button>}</div>
    <section className="sh-hero" aria-label="Welcome home">
      <div className="sh-greeting"><h1>{greeting}{firstName ? ',' : '.'}{firstName && <><br /><em>{firstName}.</em></>}</h1><p>Make a little room for what comes next.</p>{onGoToStudy && <button type="button" className="student-primary" data-coach="study" onClick={onGoToStudy}>Start a study session <ArrowUpRight size={21} /></button>}{course && <button type="button" className="student-text-action" onClick={() => onSelectModule(course.id)}>Or continue your module <ArrowRight size={19} /></button>}</div>
      <img className="sh-character" src="/assets/landing/starguy-door.png" alt="" />
      <aside className="sh-week"><p className="student-eyebrow">Your week so far</p><strong>{sessions.length ? duration : 'A fresh start.'}</strong><p>{sessions.length ? `of focused study across ${sessions.length} session${sessions.length === 1 ? '' : 's'}` : 'Your record grows as you go.'}</p><div className="sh-week-days" aria-label="Study days this week">{days.map((day, index) => <span key={day} title={day}><i className={sessions.some(session => session.date === day) ? 'studied' : ''} aria-label={`${day}: ${sessions.some(session => session.date === day) ? 'studied' : 'no sessions'}`} /><small>{'MTWTFSS'[index]}</small></span>)}</div><button type="button" className="student-text-action" onClick={onGoToDashboard}>Your progress <ArrowUpRight size={19} /></button></aside>
    </section>
    <div className="sh-section-heading"><h2>Keep a good thing going.</h2><p>A chapter to finish. A world to explore.</p></div>
    <div className="sh-notebook">
      <section className="student-ink-card sh-next" data-coach="modules">
        <p className="student-eyebrow">{course ? done > 0 ? 'Pick up where you left off' : 'A good place to begin' : 'Your next chapter'}</p>
        <div className="sh-art sh-module-art"><ModulesIcon /></div>
        {course ? <><p className="student-eyebrow">{categoryTitles[course.category]}</p><h2>{course.title}</h2><p>{course.subtitle}</p><div className="sh-module-progress"><span>{done} of {course.sectionsCount} sections complete</span><div role="progressbar" aria-label="Module progress" aria-valuenow={done} aria-valuemin={0} aria-valuemax={course.sectionsCount}><i style={{ width: `${course.sectionsCount ? done / course.sectionsCount * 100 : 0}%` }} /></div></div><button type="button" className="student-primary" onClick={() => onSelectModule(course.id)}>{done ? 'Continue learning' : 'Begin this module'}<ArrowUpRight size={21} /></button></> : <><h2>{allCourses.length ? 'Look how far you’ve come.' : 'A world of ideas.'}</h2><p>{allCourses.length ? 'You’ve completed your available modules. Revisit an idea and put it into practice.' : 'Explore the programme and find your next chapter.'}</p><button type="button" className="student-primary" onClick={onGoToModules}>Explore modules <ArrowUpRight size={21} /></button></>}
        {recent?.kind === 'tool' && onOpenTool && <button type="button" className="student-text-action sh-return-tool" onClick={() => onOpenTool(recent.id)}>Return to {recent.label}<ArrowUpRight size={18} /></button>}
      </section>
      <div className="sh-destinations">{destinations.filter(item => item.go).map(item => <button type="button" className="student-ink-card sh-destination" key={item.title} onClick={item.go} data-coach={item.coach}><span className="sh-art">{item.icon}</span><h2>{item.title}</h2><p>{item.copy}</p><span className="sh-card-action">{item.action}<ArrowUpRight size={20} /></span></button>)}</div>
    </div>
    <button type="button" className="student-secondary sh-browse" onClick={onGoToModules}>Browse all five module worlds <ArrowRight size={21} /></button>
  </main>;
}
