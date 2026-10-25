/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Dev-only. Mounts a CURRENT screen on its own so the Kobra review page
 * (/kobra-review.html) can show it in an iframe beside the Kobra version.
 * Open /kobra-review-before.html?screen=post-session|home|mark-bank|viewer|settings|login
 * (&theme=dark). Every screen is the real component on demo data, so nothing
 * here needs a signed-in account (the live app behind the review page showed
 * the sign-in wall instead of the screen, 25 Oct).
 * Never part of the production build (vite.config.ts lists its inputs).
 */
import React, { useEffect, useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { ToastProvider } from './components/Toast';
import StrategyPickerStep from './components/study/StrategyPickerStep';
import StudySessionFinish from './components/study/StudySessionFinish';
import StudySessionSaved from './components/study/StudySessionSaved';
import StudentHomeContent from './components/StudentHomeContent';
import MarkBankLibrary from './components/MarkBank/MarkBankLibrary';
import { levelsFor, loadCards, type Level } from './components/MarkBank/deck';
import Viewer, { type ViewerDoc } from './components/PaperTrail/Viewer';
import { paperStoragePath, paperUrl } from './components/PaperTrail/storage';
import SettingsModal from './components/SettingsModal';
import LoginPage from './components/LoginPage';
import { ALL_COURSES, categoryTitles } from './courseData';
import { toDateKey } from './components/subjectData';
import type { DeckState } from './components/MarkBank/store';
import type { SecCard } from './types/markBank';
import type { StudySessionRecord } from './studySessionData';
import type { UserSettings } from './types';
import './index.css';
// The live study room loads this before the finish screen; the receipt's
// "Topic time" block is styled here.
import './components/study/study-kobra.css';

const params = new URLSearchParams(window.location.search);
if (params.get('theme') === 'dark') document.documentElement.classList.add('dark');
const screen = params.get('screen') ?? 'post-session';

const STRATEGIES = [
  'mastering-active-recall-protocol', 'mastering-spaced-repetition-protocol', 'mastering-interleaving-protocol',
  'elaborative-interrogation-protocol', 'agency-protocol', 'growth-mindset-protocol', 'digital-distraction-protocol',
  'learning-radar-protocol', 'exam-hall-strategies-protocol',
];

function PostSession() {
  const [step, setStep] = useState<'pick' | 'finish' | 'saved'>('pick');
  const [mode, setMode] = useState<'quick' | 'full'>('quick');
  if (step === 'pick') {
    return (
      <StrategyPickerStep learnedStrategyIds={STRATEGIES} autoTrackedIds={STRATEGIES.slice(0, 2)}
        subject="Chemistry" durationSeconds={2700} pointsEarned={40}
        onContinue={() => setStep('finish')} onSkip={() => setStep('finish')} />
    );
  }
  if (step === 'finish') {
    return (
      <StudySessionFinish subject="Chemistry" elapsedSeconds={2700} plannedSeconds={2700} practice="Past paper questions"
        character="star-crew:maker" strategies={['Active recall', 'Spaced repetition']} basePoints={40} isSaving={false}
        mode={mode} onModeChange={setMode}
        onSave={async () => { setStep('saved'); }} onSkip={async () => { setStep('saved'); }} />
    );
  }
  return (
    <StudySessionSaved subject="Chemistry" seconds={2700} points={45} character="star-crew:maker"
      onIsland={() => setStep('pick')} onStudyAgain={() => setStep('pick')} />
  );
}

// ── Home: the same demo week and module as the Kobra rebuild (HomeHeroAfter) ──
const WEEK = [
  { minutes: 75, sessions: 2 }, { minutes: 48, sessions: 1 }, { minutes: 102, sessions: 2 },
  { minutes: 64, sessions: 2 }, { minutes: 125, sessions: 2 }, { minutes: 0, sessions: 0 }, { minutes: 0, sessions: 0 },
];
const HOME_MODULE = 'agency-architecture-protocol'; // Controlling the Controllables, 3 of 5 read
const SUBJECTS_ROTA = ['Chemistry', 'English', 'Mathematics', 'Geography'];

function demoSessions(): StudySessionRecord[] {
  const now = new Date();
  const monday = new Date(now.getFullYear(), now.getMonth(), now.getDate() - ((now.getDay() + 6) % 7));
  const records: StudySessionRecord[] = [];
  WEEK.forEach((day, offset) => {
    const date = new Date(monday);
    date.setDate(monday.getDate() + offset);
    const share = Math.floor(day.minutes / day.sessions);
    for (let n = 0; n < day.sessions; n += 1) {
      // The first session takes the remainder, so the week adds up to the rebuild's total.
      const minutes = n === 0 ? day.minutes - share * (day.sessions - 1) : share;
      const startedAt = new Date(date.getFullYear(), date.getMonth(), date.getDate(), 16 + n * 2).getTime();
      records.push({
        id: `demo-${offset}-${n}`, date: toDateKey(date), subject: SUBJECTS_ROTA[(offset + n) % SUBJECTS_ROTA.length],
        sessionType: n === 0 ? 'practice' : 'revision', plannedMinutes: minutes, actualSeconds: minutes * 60,
        startedAt, completedAt: startedAt + minutes * 60000, pointsEarned: 40, hadReflection: n === 0,
      });
    }
  });
  return records;
}

function Home() {
  const sessions = useMemo(demoSessions, []);
  // Every module before the demo one is complete, so Home picks it up at 3 of 5.
  const progress = useMemo(() => {
    const result: Record<string, { unlockedSection: number }> = {};
    for (const course of ALL_COURSES) {
      if (course.id === HOME_MODULE) { result[course.id] = { unlockedSection: 3 }; break; }
      result[course.id] = { unlockedSection: course.sectionsCount };
    }
    return result;
  }, []);
  const noop = () => {};
  return (
    <StudentHomeContent userName="Demo" userAvatarSeed="star-crew:maker" allCourses={ALL_COURSES} categoryTitles={categoryTitles}
      userProgress={progress} studySessions={sessions} pointsBalance={1240}
      onSelectModule={noop} onGoToStudy={noop} onGoToModules={noop} onGoToDashboard={noop} onGoToLearningPaths={noop}
      onGoToJourney={noop} onGoToInnovationZone={noop} />
  );
}

// ── Mark Bank library: the real library on the Politics and Society deck ──
const MARK_BANK_SUBJECT = 'politics-and-society';
const EMPTY_DECK: DeckState = { v: 1, cards: {}, updatedAt: 0 };

function MarkBank() {
  const [subjectId, setSubjectId] = useState(MARK_BANK_SUBJECT);
  const [level, setLevel] = useState<Level>(() => levelsFor(MARK_BANK_SUBJECT)[0]);
  const [cards, setCards] = useState<SecCard[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [attempt, setAttempt] = useState(0);
  useEffect(() => {
    let cancelled = false;
    setLoading(true); setError(false);
    loadCards(subjectId, level)
      .then(loaded => { if (!cancelled) { setCards(loaded); setLoading(false); } })
      .catch(() => { if (!cancelled) { setCards([]); setError(true); setLoading(false); } });
    return () => { cancelled = true; };
  }, [subjectId, level, attempt]);
  return (
    <MarkBankLibrary key={`${subjectId}-${level}`} subjectId={subjectId} level={level} cards={cards} state={EMPTY_DECK} now={Date.now}
      chooseSubject={id => { setSubjectId(id); setLevel(levelsFor(id)[0]); }} chooseLevel={setLevel} canSelectSubject={() => true}
      onStart={() => {}} busy={false} ready={!loading && !error} loading={loading} error={error}
      onRetry={() => setAttempt(value => value + 1)} online />
  );
}

// ── Paper viewer: the real viewer on Physics 2025 Higher (world-readable corpus) ──
function PaperViewer() {
  const [docs, setDocs] = useState<{ paper: ViewerDoc; scheme?: ViewerDoc } | null>(null);
  useEffect(() => {
    let cancelled = false;
    // The index is 1.2 MB, so it loads only for this screen.
    void import('./paperTrailData').then(({ PAPER_TRAIL_INDEX }) => {
      if (cancelled) return;
      const entry = PAPER_TRAIL_INDEX.physics?.find(item => item.year === 2025 && item.level === 'higher' && item.lang === 'ev' && !item.sitting);
      const item = entry?.papers[0];
      if (!item) return;
      const url = (kind: 'paper' | 'scheme', fileid: string) => paperUrl(paperStoragePath('lc', 'physics', 2025, kind, fileid));
      const label = item.label.replace(/\s*\([A-Z]{2}\)\s*$/, '').trim();
      setDocs({
        paper: { url: url('paper', item.doc.f), label, bytes: item.doc.b },
        scheme: item.scheme ? { url: url('scheme', item.scheme.f), label: 'Marking scheme', bytes: item.scheme.b } : undefined,
      });
    });
    return () => { cancelled = true; };
  }, []);
  if (!docs) return <p style={{ padding: 24, fontFamily: 'DM Sans, sans-serif' }}>Opening the paper…</p>;
  return <Viewer title="Physics · 2025" subtitle={`${docs.paper.label} · Higher`} paper={docs.paper} scheme={docs.scheme} onClose={() => {}} />;
}

function Settings() {
  const [settings, setSettings] = useState<UserSettings>({
    language: 'en', avatar: 'star-crew:maker', darkMode: params.get('theme') === 'dark', cardStyle: 'classic' as UserSettings['cardStyle'],
    defaultWorkMinutes: 25, showDashboard: true, essentialsMode: false, studyQuiz: true,
  });
  return (
    <SettingsModal isOpen onClose={() => {}} settings={settings}
      updateSetting={(key, value) => setSettings(current => ({ ...current, [key]: value }))}
      userName="Demo Student" userSchool="Marino College" hasStudyProfile hasNorthStar
      onStartProfileSetup={() => {}} onChangeSubjects={() => {}} onResetNorthStar={() => {}} onAdvanceYear={() => {}} onLogout={() => {}} />
  );
}

function Before() {
  if (screen === 'home') return <Home />;
  if (screen === 'mark-bank') return <MarkBank />;
  if (screen === 'viewer') return <PaperViewer />;
  if (screen === 'settings') return <Settings />;
  if (screen === 'login') return <LoginPage handleLoginSuccess={() => {}} />;
  return <PostSession />;
}

// The app shell paints the canvas behind every screen; here the harness does.
const root = document.getElementById('root');
if (root) {
  createRoot(root).render(
    <ToastProvider>
      <div style={{ minHeight: '100vh', background: 'var(--surface-canvas)', color: 'var(--ink-primary)' }}><Before /></div>
    </ToastProvider>,
  );
}
