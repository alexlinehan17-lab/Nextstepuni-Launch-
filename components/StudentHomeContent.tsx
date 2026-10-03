import React from 'react';
import { ArrowRight, ArrowUpRight } from 'lucide-react';
import type { CourseData } from './Library';
import type { StudySessionRecord } from '../studySessionData';
import { ModulesIcon, InnovationZoneIcon, LearningPathsIcon, MyJourneyIcon } from './sectionIcons';
import { getLastVisit } from './lastVisited';
import Avatar from './Avatar';
import './student-screens.css';
import FieldNotes from './dashboard/FieldNotes';
import KobraScope from './approved-ui-runtime';
import { Button } from './approved-ui-runtime';
import { ReadingProgress } from './learning/ReadingProgress';
import './learning/learning.css';
import './learning/home-learning.css';

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

export default function StudentHomeContent({ uid, userName, userAvatarSeed, hasUnreadNotifications, onOpenMobileProfile, allCourses, userProgress, categoryTitles, studySessions = [], pointsBalance = 0, onSelectModule, onGoToStudy, onGoToModules, onGoToDashboard, onGoToLearningPaths, onGoToJourney, onGoToInnovationZone }: StudentHomeContentProps) {
  const now = new Date();
  const visit = getLastVisit(uid);
  const recent = visit && Date.now() - visit.at <= 21 * 86400000 ? visit : null;
  const available = allCourses.filter(course => (userProgress[course.id]?.unlockedSection || 0) < course.sectionsCount);
  const course = available.find(item => recent?.kind === 'module' && recent.id === item.id) || available[0];
  const done = course ? Math.max(0, Math.min(userProgress[course.id]?.unlockedSection || 0, course.sectionsCount)) : 0;
  const firstName = userName?.trim().split(/\s+/)[0];
  const greeting = now.getHours() < 12 ? 'Good morning' : now.getHours() < 18 ? 'Good afternoon' : 'Good evening';
  const destinations = [
    { title: 'Learning Paths', copy: 'A little structure for what’s next.', action: 'Find your path', icon: <LearningPathsIcon />, go: onGoToLearningPaths },
    { title: 'My Island', copy: `${pointsBalance.toLocaleString()} JP. Plenty of room to grow.`, action: 'Build your island', icon: <MyJourneyIcon />, go: onGoToJourney },
    { title: 'Launchpad', copy: 'Your tools for the work ahead.', action: 'Open your toolkit', icon: <InnovationZoneIcon />, go: onGoToInnovationZone, coach: 'launchpad' },
  ];
  return <main className="student-home">
    <div className="sh-date"><span className="student-eyebrow">{now.toLocaleDateString('en-IE', { weekday: 'long', day: 'numeric', month: 'long' })}</span>{onOpenMobileProfile && <button type="button" className="sh-profile" onClick={onOpenMobileProfile} aria-label="Open profile and settings"><Avatar seed={userAvatarSeed || userName || 'student'} className="h-10 w-10" />{hasUnreadNotifications && <i aria-label="Unread notifications" />}</button>}</div>
    <section className="sh-hero" aria-label="Welcome home">
      <div className="sh-greeting"><h1>{greeting}{firstName ? ',' : '.'}{firstName && <><br /><em>{firstName}.</em></>}</h1><p>Make a little room for what comes next.</p>{onGoToStudy && <button type="button" className="student-primary" data-coach="study" onClick={onGoToStudy}>Start a study session <ArrowUpRight size={21} /></button>}</div>
      <FieldNotes sessions={studySessions} onProgress={onGoToDashboard} />
    </section>
    <KobraScope className="sh-learning">
      <section className="sh-learning-card sh-continue" data-coach="modules" aria-labelledby="home-current-module">
        <div className="sh-continue-art"><ModulesIcon /></div>
        <p className="rs-eyebrow sh-continue-eyebrow">{course ? done > 0 ? 'Pick up where you left off' : 'A good place to begin' : 'Your next chapter'}</p>
        <div className="sh-continue-copy">
          {course ? <><p className="sh-continue-world">{categoryTitles[course.category]}</p><h2 id="home-current-module">{course.title}</h2><p className="sh-continue-subtitle">{course.subtitle}</p></> : <><h2 id="home-current-module">{allCourses.length ? 'Look how far you’ve come.' : 'A world of ideas.'}</h2><p className="sh-continue-subtitle">{allCourses.length ? 'You’ve completed your available modules. Revisit an idea and put it into practice.' : 'Explore the programme and find your next chapter.'}</p></>}
        </div>
        <div className="sh-continue-actions">
          {course && <><ReadingProgress done={done} total={course.sectionsCount} /><Button variant="outline" className="nsu-ink-outline" onClick={() => onSelectModule(course.id)}>{done ? 'Continue learning' : 'Begin this module'}<ArrowUpRight size={18} /></Button></>}
          <Button variant={course ? 'ghost' : 'outline'} className={course ? 'sh-worlds-action' : 'nsu-ink-outline sh-worlds-action'} onClick={onGoToModules}>Browse all five module worlds <ArrowRight size={18} /></Button>
        </div>
      </section>
      <div className="sh-destination-grid">{destinations.filter(item => item.go).map(item => <section className="sh-learning-card sh-destination-card" key={item.title} data-coach={item.coach}>
        <span className="sh-destination-art">{item.icon}</span>
        <div className="sh-destination-copy"><h2>{item.title}</h2><p>{item.copy}</p></div>
        <Button variant="ghost" className="sh-destination-action" onClick={item.go}>{item.action}<ArrowUpRight size={18} /></Button>
      </section>)}</div>
    </KobraScope>
  </main>;
}
