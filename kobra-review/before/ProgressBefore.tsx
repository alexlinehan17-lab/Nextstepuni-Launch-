/**
 * Dev-only "Now" pane for the Kobra review (27 Oct 2026): the REAL My Progress
 * screen (components/DashboardView.tsx) on a sample fortnight, with no account
 * and no network. The sample data lives in kobra-review/sections/progress-sample.ts
 * so the Kobra rebuild beside it shows the same numbers.
 *
 * DashboardView picks its phone design by DEVICE, not width (useMobileAppDesign),
 * so in this desktop iframe it draws the desktop design: the ink-grid section
 * tabs and the page's own theme switch. The phone design, with the section
 * listbox, is the same component in a frame marked data-app-preview="mobile":
 *   ?screen=progress&device=mobile
 * ?screen=progress&tab=milestones opens on Milestones.
 * TopicHistoryPanel only renders with a signed-in uid, so it is absent here.
 */
import { useMemo, useState } from 'react';
import DashboardView from '../../components/DashboardView';
import { ALL_COURSES, categoryTitles } from '../../courseData';
import type { DashboardSection } from '../../contexts/NavigationContext';
import {
  SAMPLE_LABEL, SAMPLE_POINTS, sampleGamification, sampleProfile, sampleQuest, sampleRecommendation, sampleSessions,
  sampleStrategyMastery, sampleStreak, sampleTopicMastery, sampleUserProgress, sampleWeeklyChallenge,
} from '../sections/progress-sample';

const params = new URLSearchParams(window.location.search);
const TABS: DashboardSection[] = ['overview', 'study', 'confidence', 'practice', 'milestones'];
const START_TAB = (TABS as string[]).includes(params.get('tab') ?? '') ? params.get('tab') as DashboardSection : 'overview';

function MobileFrame() {
  // The hook reads the attribute off window.frameElement, so the same page is
  // loaded again inside a frame that asks for the phone design.
  const next = new URLSearchParams(window.location.search);
  next.set('device', 'inner');
  return (
    <iframe title="My Progress, phone design" data-app-preview="mobile" src={`${window.location.pathname}?${next.toString()}`}
      style={{ display: 'block', width: '100%', height: '100vh', border: 0 }} />
  );
}

export default function ProgressBefore() {
  const sessions = useMemo(() => sampleSessions(), []);
  const profile = useMemo(sampleProfile, []);
  const progress = useMemo(sampleUserProgress, []);
  const recommendation = useMemo(sampleRecommendation, []);
  const quest = useMemo(sampleQuest, []);
  const gamification = useMemo(sampleGamification, []);
  const challenge = useMemo(sampleWeeklyChallenge, []);
  const mastery = useMemo(sampleStrategyMastery, []);
  const topics = useMemo(sampleTopicMastery, []);
  const streak = useMemo(() => sampleStreak(), []);
  const [tab, setTab] = useState<DashboardSection>(START_TAB);
  const [dark, setDark] = useState(() => document.documentElement.classList.contains('dark'));

  if (params.get('device') === 'mobile') return <MobileFrame />;

  const noop = () => {};
  return (
    <>
      <p style={{
        margin: 0, padding: '8px 16px', borderBottom: '1px solid var(--outline-soft)',
        font: '500 12px/1.5 DM Sans, sans-serif', color: 'var(--ink-muted)', background: 'var(--surface-canvas)',
      }}>{SAMPLE_LABEL}</p>
      <DashboardView
        userProgress={progress} allCourses={ALL_COURSES} categoryTitles={categoryTitles}
        streak={streak} recommendation={recommendation} onSelectModule={noop} onBack={noop}
        pointsEarned={SAMPLE_POINTS.earned} pointsAvailable={SAMPLE_POINTS.available}
        studentProfile={profile} studySessions={sessions} topicMastery={topics}
        questState={quest} onClaimQuestReward={noop} onStartStudy={noop}
        gamificationState={gamification} strategyMastery={mastery} weeklyChallenge={challenge}
        activeTab={tab} onTabChange={setTab}
        darkMode={dark}
        onToggleTheme={() => { const next = !dark; document.documentElement.classList.toggle('dark', next); setDark(next); }}
        onEditGrades={noop} onAddMockResult={noop}
        onStudyTopic={noop} onPracticeTopic={noop}
      />
    </>
  );
}
