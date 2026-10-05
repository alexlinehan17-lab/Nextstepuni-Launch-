import React from 'react';
import { createRoot } from 'react-dom/client';
import { KnowledgeTree } from '../../components/KnowledgeTree.desktop';
import IllustrationTheme from '../../components/IllustrationTheme';
import NextStepUniSidebar from '../../components/navigation/NextStepUniSidebar';
import { NavigationProvider } from '../../contexts/NavigationContext';
import type { CourseData } from '../../components/Library';
import '../../index.css';

// Review data only: render the actual Home and its container without signing in.
const noop = () => {};
localStorage.setItem('nsu-coachmarks:home-monitor-review', '1');
const course: CourseData = {
  id: 'review-controllables', category: 'architecture-mindset',
  title: 'Controlling the Controllables', subtitle: 'The Attribution Retraining Guide',
  description: '', sectionsCount: 5, tags: [], gradient: '', accentColor: '', pillBgColor: '',
};
const settings = { language: 'en' as const, avatar: '', darkMode: true, cardStyle: 'default' as const, defaultWorkMinutes: 25, showDashboard: false };
createRoot(document.getElementById('root')!).render(<><IllustrationTheme /><NavigationProvider><NextStepUniSidebar
  user={{ uid: 'home-monitor-review', name: 'Demo Student', avatar: 'Charlie', curriculumLevel: 'senior' }}
  settings={settings} updateSetting={noop} onLogout={noop} onOpenSettings={noop}
  onOpenPassport={noop} onOpenSiteGuide={noop} onOpenFeedback={noop}
  onUnreadCountChange={noop} completedCount={25} totalCount={53} unreadCount={0}
><KnowledgeTree
  uid="home-monitor-review" userName="Demo Student" allCourses={[course]}
  userProgress={{ [course.id]: { unlockedSection: 3 } }}
  categoryTitles={{ 'architecture-mindset': 'The Architecture of your Mindset', 'science-growth': '', 'learning-cheat-codes': '', 'exam-zone': '', 'subject-specific-science': '' }}
  settings={settings}
  updateSetting={noop} completedCount={25} totalCount={53} pointsBalance={5765}
  onSelectCategory={noop} onSelectModule={noop} onGoToModules={noop} onGoToStudy={noop}
  onGoToInnovationZone={noop} onGoToDashboard={noop} onGoToLearningPaths={noop} onGoToJourney={noop}
  onLogout={noop} onOpenSettings={noop} onOpenPassport={noop}
/></NextStepUniSidebar></NavigationProvider></>);
