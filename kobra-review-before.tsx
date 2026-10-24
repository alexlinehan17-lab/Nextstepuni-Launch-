/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Dev-only. Mounts a CURRENT screen on its own so the Kobra review page
 * (/kobra-review.html) can show it in an iframe beside the Kobra version.
 * Open /kobra-review-before.html?screen=post-session|settings|login (&theme=dark).
 * Never part of the production build (vite.config.ts lists its inputs).
 */
import React, { useState } from 'react';
import { createRoot } from 'react-dom/client';
import { ToastProvider } from './components/Toast';
import StrategyPickerStep from './components/study/StrategyPickerStep';
import StudySessionFinish from './components/study/StudySessionFinish';
import StudySessionSaved from './components/study/StudySessionSaved';
import SettingsModal from './components/SettingsModal';
import LoginPage from './components/LoginPage';
import type { UserSettings } from './types';
import './index.css';

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
  if (screen === 'settings') return <Settings />;
  if (screen === 'login') return <LoginPage handleLoginSuccess={() => {}} />;
  return <PostSession />;
}

const root = document.getElementById('root');
if (root) createRoot(root).render(<ToastProvider><Before /></ToastProvider>);
