import React, { useEffect, useState, type ReactNode } from 'react';
import { ArrowRight, ArrowUpRight, ChevronRight } from 'lucide-react';
import type { CourseData } from './Library';
import type { StudySessionRecord } from '../studySessionData';
import { ModulesIcon, InnovationZoneIcon, LearningPathsIcon, MyJourneyIcon } from './sectionIcons';
import { getLastVisit } from './lastVisited';
import Avatar from './Avatar';
import './student-screens.css';
import FieldNotes from './dashboard/FieldNotes';
import KobraScope from './approved-ui-runtime';
import { Button as KobraButton } from './approved-ui-runtime';
import { ReadingProgress } from './learning/ReadingProgress';
import { TopBar } from './ui/Bars';
import { Button, IconButton, TextButton } from './ui/Button';
import { List, PressBox, Row } from './ui/List';
import './learning/learning.css';
import './learning/home-learning.css';
import './home-phone.css';

export interface StudentHomeContentProps {
  uid?: string;
  userName?: string;
  userAvatarSeed?: string;
  hasUnreadNotifications?: boolean;
  onOpenMobileProfile?: () => void;
  onOpenFeedback?: () => void;
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
  /** phone: the agreed phone Home (the frame's bar, Today's plan straight under
   *  Start, the week as the one sheet); desk: today's laptop layout. */
  layout?: 'phone' | 'desk';
  /** On a phone: today's plan, drawn straight under Start. */
  plan?: ReactNode;
  /** On a phone: the weekly goal, under the week. */
  goal?: ReactNode;
}

export default function StudentHomeContent({ uid, userName, userAvatarSeed, hasUnreadNotifications, onOpenMobileProfile, onOpenFeedback, allCourses, userProgress, categoryTitles, studySessions = [], pointsBalance = 0, onSelectModule, onGoToStudy, onGoToModules, onGoToDashboard, onGoToLearningPaths, onGoToJourney, onGoToInnovationZone, layout = 'desk', plan, goal }: StudentHomeContentProps) {
  const now = new Date();
  const visit = getLastVisit(uid);
  const recent = visit && Date.now() - visit.at <= 21 * 86400000 ? visit : null;
  const available = allCourses.filter(course => (userProgress[course.id]?.unlockedSection || 0) < course.sectionsCount);
  const course = available.find(item => recent?.kind === 'module' && recent.id === item.id) || available[0];
  const done = course ? Math.max(0, Math.min(userProgress[course.id]?.unlockedSection || 0, course.sectionsCount)) : 0;
  const firstName = userName?.trim().split(/\s+/)[0];
  const greeting = now.getHours() < 12 ? 'Good morning' : now.getHours() < 18 ? 'Good afternoon' : 'Good evening';
  const date = now.toLocaleDateString('en-IE', { weekday: 'long', day: 'numeric', month: 'long' });
  const destinations = [
    { title: 'Learning Paths', copy: 'A little structure for what’s next.', action: 'Find your path', icon: <LearningPathsIcon />, go: onGoToLearningPaths },
    { title: 'My Island', copy: `${pointsBalance.toLocaleString()} JP. Plenty of room to grow.`, action: 'Build your island', icon: <MyJourneyIcon />, go: onGoToJourney },
    { title: 'Launchpad', copy: 'Your tools for the work ahead.', action: 'Open your toolkit', icon: <InnovationZoneIcon />, go: onGoToInnovationZone, coach: 'launchpad' },
  ];
  const eyebrow = course ? done > 0 ? 'Pick up where you left off' : 'A good place to begin' : 'Your next chapter';
  // The bar gains its hairline once the page has scrolled under it (tokens.md, "Bars").
  const [scrolled, setScrolled] = useState(false);
  useEffect(() => {
    if (layout !== 'phone') return undefined;
    const update = () => setScrolled(window.scrollY > 4);
    update();
    window.addEventListener('scroll', update, { passive: true });
    return () => window.removeEventListener('scroll', update);
  }, [layout]);

  if (layout === 'phone') {
    const account = onOpenMobileProfile ? (
      <IconButton className="sh-me" data-coach="help" data-unread={hasUnreadNotifications || undefined} onClick={onOpenMobileProfile}
        label={hasUnreadNotifications ? 'Open account, new updates available' : 'Open profile and settings'}
        icon={<Avatar seed={userAvatarSeed || userName || 'student'} className="sh-me-art" />} />
    ) : undefined;
    const remaining = course ? course.sectionsCount - done : 0;
    return <main className="student-home sh-phone">
      <TopBar placeLabel={date} action={account} ruled={scrolled} />
      <section className="sh-open" aria-label="Welcome home">
        <h1 className="t-display">{greeting}{firstName ? `, ${firstName}.` : '.'}</h1>
        <p className="t-sub">Make a little room for what comes next.</p>
        {onGoToStudy && <Button kind="main" size="lg" block arrow="forward" data-coach="study" onClick={onGoToStudy}>Start a study session</Button>}
      </section>
      {plan ? <div className="sh-sec">{plan}</div> : null}
      <section className="sh-sec" aria-labelledby="home-week-title">
        <div className="home-section-heading"><h2 id="home-week-title" className="t-heading">Your week so far</h2><TextButton arrow="forward" onClick={onGoToDashboard}>Progress</TextButton></div>
        <FieldNotes layout="phone" sessions={studySessions} onProgress={onGoToDashboard} />
        {goal}
      </section>
      <section className="sh-sec sh-continue-phone" aria-labelledby="home-current-module">
        <div className="sh-continue-lit" data-coach="modules">
        <div className="home-section-heading"><h2 id="home-current-module" className="t-heading">{eyebrow}</h2></div>
        {course ? <PressBox className="sh-module" onPress={() => onSelectModule(course.id)} label={`${done ? 'Continue learning' : 'Begin this module'}: ${course.title}`}>
          <span className="sh-module-body">
            <span className="sh-module-names"><span className="t-meta">{categoryTitles[course.category]}</span><span className="t-row">{course.title}</span></span>
            <span className="sh-module-bar" aria-hidden="true"><i style={{ width: `${course.sectionsCount ? (done / course.sectionsCount) * 100 : 0}%` }} /></span>
            <span className="t-meta">{done} of {course.sectionsCount} read · {remaining === 0 ? 'All read' : `${remaining} to go`}</span>
          </span>
          <ChevronRight className="ui-icon sh-module-chev" width={20} height={20} strokeWidth={1.75} aria-hidden="true" />
        </PressBox> : <div className="sh-module-none"><p className="t-row">{allCourses.length ? 'Look how far you’ve come.' : 'A world of ideas.'}</p><p className="t-sub">{allCourses.length ? 'You’ve completed your available modules. Revisit an idea and put it into practice.' : 'Explore the programme and find your next chapter.'}</p></div>}
        </div>
        <TextButton arrow="forward" className="sh-worlds" onClick={onGoToModules}>Browse all five module worlds</TextButton>
      </section>
      <section className="sh-sec" aria-labelledby="home-go-to">
        <div className="home-section-heading"><h2 id="home-go-to" className="t-heading">Go to</h2></div>
        <List>
          {destinations.filter(item => item.go).map(item => <Row key={item.title} className="sh-go" coach={item.coach} title={item.title} meta={item.copy.replace(/\.$/, '')} onPress={item.go} label={`${item.title}: ${item.action}`} />)}
        </List>
      </section>
      {onOpenFeedback ? <div className="sh-feedback-line"><TextButton tone="quiet" onClick={onOpenFeedback}>Feedback</TextButton></div> : null}
    </main>;
  }

  return <main className="student-home">
    <div className="sh-date">
      <span className="student-eyebrow">{date}</span>
      <div className="sh-home-actions">
        {onOpenFeedback && <button type="button" className="sh-feedback" onClick={onOpenFeedback} aria-haspopup="dialog">Feedback <ArrowUpRight size={16} aria-hidden="true" /></button>}
        {onOpenMobileProfile && <button type="button" className="sh-profile" data-unread={hasUnreadNotifications || undefined} onClick={onOpenMobileProfile} aria-label={hasUnreadNotifications ? 'Open account, new updates available' : 'Open profile and settings'}>
          <Avatar seed={userAvatarSeed || userName || 'student'} className="sh-profile-avatar" />
          <span className="sh-profile-copy"><strong>Account</strong>{hasUnreadNotifications && <small>New updates</small>}</span>
        </button>}
      </div>
    </div>
    <section className="sh-hero" aria-label="Welcome home">
      <div className="sh-greeting"><h1>{greeting}{firstName ? ',' : '.'}{firstName && <><br /><em>{firstName}.</em></>}</h1><p>Make a little room for what comes next.</p>{onGoToStudy && <Button kind="main" size="lg" arrow="forward" className="sh-start" data-coach="study" onClick={onGoToStudy}>Start a study session</Button>}</div>
      <FieldNotes sessions={studySessions} onProgress={onGoToDashboard} />
    </section>
    <KobraScope className="sh-learning">
      <section className="sh-learning-card sh-continue" data-coach="modules" aria-labelledby="home-current-module">
        <div className="sh-continue-art"><ModulesIcon /></div>
        <p className="rs-eyebrow sh-continue-eyebrow">{eyebrow}</p>
        <div className="sh-continue-copy">
          {course ? <><p className="sh-continue-world">{categoryTitles[course.category]}</p><h2 id="home-current-module">{course.title}</h2><p className="sh-continue-subtitle">{course.subtitle}</p></> : <><h2 id="home-current-module">{allCourses.length ? 'Look how far you’ve come.' : 'A world of ideas.'}</h2><p className="sh-continue-subtitle">{allCourses.length ? 'You’ve completed your available modules. Revisit an idea and put it into practice.' : 'Explore the programme and find your next chapter.'}</p></>}
        </div>
        <div className="sh-continue-actions">
          {course && <><ReadingProgress done={done} total={course.sectionsCount} /><KobraButton variant="outline" className="nsu-ink-outline" onClick={() => onSelectModule(course.id)}>{done ? 'Continue learning' : 'Begin this module'}<ArrowUpRight size={18} /></KobraButton></>}
          <KobraButton variant={course ? 'ghost' : 'outline'} className={course ? 'sh-worlds-action' : 'nsu-ink-outline sh-worlds-action'} onClick={onGoToModules}>Browse all five module worlds <ArrowRight size={18} /></KobraButton>
        </div>
      </section>
      <div className="sh-destination-grid">{destinations.filter(item => item.go).map(item => <section className="sh-learning-card sh-destination-card" key={item.title} data-coach={item.coach}>
        <span className="sh-destination-art">{item.icon}</span>
        <div className="sh-destination-copy"><h2>{item.title}</h2><p>{item.copy}</p></div>
        <KobraButton variant="ghost" className="sh-destination-action" onClick={item.go}>{item.action}<ArrowUpRight size={18} /></KobraButton>
      </section>)}</div>
    </KobraScope>
  </main>;
}
