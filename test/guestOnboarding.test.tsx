/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guest setup: onboarding without an account, from the landing page's "Set up
 * without an account" to the "Dive in" placeholder. The contract under test:
 *   - a signed-out visitor with ?setup=guest gets the SAME Onboarding, with
 *     no user behind it;
 *   - nothing on that path writes to Firestore or calls Auth (the app's own
 *     boot is outside this router and is not exercised here);
 *   - the final button reads "Dive in" and leads to the placeholder, which
 *     offers exactly two real actions;
 *   - a signed-in student is never shown the guest flow, whatever the URL;
 *   - a reload keeps the draft through the unauthenticated-boot storage clear.
 */
import React from 'react';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { configure, fireEvent, render, screen, waitFor } from '@testing-library/react';

/**
 * Testing Library waits one second by default, which is not enough when this
 * file is scheduled beside the Mark Bank suites: those load every built deck —
 * 15,600 cards and growing — and starve the workers for whole seconds at a
 * time. The failure then reads as "Onboarding never mounted" when Onboarding
 * mounted and the assertion arrived first. Reproduced on a tree with no Mark
 * Bank change in it at all, by running this file beside markBankDeck,
 * markBankCoverage, markBankCardPreservation and curriculumRegistry.
 */
configure({ asyncUtilTimeout: 15_000 });

// ─── Firebase: keep the real modules, spy on every write-shaped export ─────
const firestoreSpies = vi.hoisted(() => ({
  addDoc: vi.fn(() => Promise.resolve({ id: 'evt' })),
  setDoc: vi.fn(() => Promise.resolve()),
  updateDoc: vi.fn(() => Promise.resolve()),
  deleteDoc: vi.fn(() => Promise.resolve()),
  runTransaction: vi.fn(() => Promise.resolve()),
  writeBatch: vi.fn(),
  // The test stub for `db` is `{}`; the real collection() would throw on it
  // before addDoc is ever reached, which is not the property under test.
  collection: vi.fn((_db: unknown, path: string) => ({ path })),
}));
const authSpies = vi.hoisted(() => ({
  signInWithEmailAndPassword: vi.fn(),
  createUserWithEmailAndPassword: vi.fn(),
  signInWithPopup: vi.fn(),
  signOut: vi.fn(),
  updateProfile: vi.fn(),
}));
const functionsSpies = vi.hoisted(() => ({ httpsCallable: vi.fn(() => vi.fn()) }));

vi.mock('firebase/firestore', async importOriginal => ({ ...(await importOriginal<object>()), ...firestoreSpies }));
vi.mock('firebase/auth', async importOriginal => ({ ...(await importOriginal<object>()), ...authSpies }));
vi.mock('firebase/functions', async importOriginal => ({ ...(await importOriginal<object>()), ...functionsSpies }));

// ─── The router's surroundings ─────────────────────────────────────────────
const bootParams = vi.hoisted(() => new Map<string, string>());
vi.mock('@/utils/bootParams', () => ({ getBootParam: (name: string) => bootParams.get(name) ?? null }));

type TestUser = { uid: string; name: string; avatar: string; isAdmin: boolean; role?: string } | null;
const authState = vi.hoisted(() => ({
  user: null as TestUser,
  userResolved: true,
  needsOnboarding: false,
  handleLoginSuccess: vi.fn(),
  handleLogout: vi.fn(),
}));
vi.mock('@/contexts/AuthContext', () => ({ useAuth: () => authState }));

const navState = vi.hoisted(() => ({ viewState: 'tree', dashboardSection: 'overview', currentCategory: null, currentModuleId: null, cameFromJourney: false, activeTool: null }));
vi.mock('@/contexts/NavigationContext', () => ({
  useNavigation: () => new Proxy({ state: navState }, { get: (target, key) => (key in target ? target[key as keyof typeof target] : vi.fn()) }),
}));
vi.mock('@/contexts/ProgressContext', () => ({
  useProgress: () => ({ updateDemoProgress: vi.fn(), setTimetableCompletions: vi.fn(), progressLoaded: true, progressDataUid: authState.user?.uid ?? null }),
}));
vi.mock('@/utils/registrationProvisioning', () => ({
  isRegistrationProvisioning: () => false,
  registrationHoldRemainingMs: () => 0,
  subscribeToRegistrationProvisioning: () => () => {},
}));
vi.mock('@/hooks/useMobileAppDesign', () => ({ useMobileAppDesign: () => false }));

// Heavy, irrelevant neighbours of the branch under test.
vi.mock('@/components/KnowledgeTree', () => ({ KnowledgeTree: () => <div>KNOWLEDGE TREE</div> }));
vi.mock('@/components/Library', () => ({ Library: () => <div>LIBRARY</div> }));
vi.mock('@/components/LoginPage', () => ({ default: () => <div>LOGIN PAGE</div> }));
vi.mock('@/components/AppLaunch', () => ({ default: () => <div>APP LAUNCH</div> }));
vi.mock('@/moduleRegistry', () => ({ moduleComponents: {}, InnovationZone: () => <div>INNOVATION ZONE</div> }));

import AppRouter from '@/components/AppRouter';
import DiveIn from '@/components/DiveIn';
import { trackFunnel } from '@/utils/funnel';
import { endGuestSetup, guestStorage, readGuestPhase, readGuestSetupResult, restoreGuestSetupState, setGuestPhase } from '@/components/onboarding/guest';
import { APP_SETUP_URL } from '@/components/landing/theme';

const ROOT = resolve(__dirname, '..');
const readSource = (path: string) => readFileSync(resolve(ROOT, path), 'utf8');

const handleOnboardingComplete = vi.fn(() => Promise.resolve());
const handleOnboardingSkip = vi.fn();

function renderRouter() {
  const props = {
    studentProfile: null, userProgress: {}, northStar: null, timetableCompletions: {},
    studySessions: [], studyDebriefs: [], studyReflections: [], topicMasteryV2: {}, unifiedMockResults: [],
    pointsData: { balance: 0, totalEarned: 0, reload: vi.fn() }, streak: { current: 0, longest: 0 },
    settings: {}, updateSetting: vi.fn(),
    gamification: { state: {}, isLoaded: false, checkAndUnlockAchievements: vi.fn(), updateWeeklyGoalProgress: vi.fn(), reload: vi.fn() },
    currentToast: null, setCurrentToast: vi.fn(),
    studentCourses: [], completedCount: 0, smartRec: null, questState: null, claimQuestReward: vi.fn(), reloadQuest: vi.fn(),
    recommendation: null, strategyMastery: { masteryMap: {}, recompute: vi.fn() }, weeklyChallenge: {},
    dismissedGuides: {}, handleDismissGuide: vi.fn(),
    timetableBlockContext: null, setTimetableBlockContext: vi.fn(), handleStudyFromTimetable: vi.fn(),
    journeyResult: null, setJourneyResult: vi.fn(),
    handleOnboardingComplete, handleOnboardingSkip,
    handleProgressUpdate: vi.fn(),
    setSettingsOpen: vi.fn(), setPassportOpen: vi.fn(), setChangeSubjectsOpen: vi.fn(), setNorthStarEditOpen: vi.fn(),
    setUnlockedAvatarSeeds: vi.fn(), unlockedThemes: [], setUnlockedThemes: vi.fn(), setUnlockedCardStyles: vi.fn(),
    onOpenSiteGuide: vi.fn(), onOpenFeedback: vi.fn(), onOpenMobileProfile: vi.fn(), hasUnreadNotifications: false,
  };
  return render(<AppRouter {...(props as any)} />);
}

/** The desktop draft shape (Onboarding.desktop.tsx, version 1), parked on the review step. */
const GUEST_DESKTOP_DRAFT_KEY = 'nextstepuni:onboarding-draft:v1:guest:fresh';
const reviewDraft = () => ({
  version: 1, step: 9, selectedSubjects: ['English', 'Mathematics'],
  subjectConfigs: { English: { level: 'higher', currentGrade: 'H4', targetGrade: 'H2' }, Mathematics: { level: 'ordinary', currentGrade: 'O3', targetGrade: 'O1' } },
  subjectBands: {}, examDate: '2030-06-05', yearGroup: '6th', essentialsMode: false, northStarData: null, restDays: ['Sunday'],
});

const { collection: _collectionStub, ...firestoreWrites } = firestoreSpies;
const allWriteSpies = () => [...Object.values(firestoreWrites), ...Object.values(authSpies), functionsSpies.httpsCallable];

beforeEach(() => {
  localStorage.clear();
  sessionStorage.clear();
  endGuestSetup({ keepDraft: false });
  bootParams.clear();
  authState.user = null;
  authState.needsOnboarding = false;
  navState.viewState = 'tree';
  allWriteSpies().forEach(spy => spy.mockClear());
  handleOnboardingComplete.mockClear();
  handleOnboardingSkip.mockClear();
});

describe('guest onboarding (no account)', () => {
  it('a signed-out visitor without the flag still gets the login page', async () => {
    renderRouter();
    expect(await screen.findByText('LOGIN PAGE')).toBeInTheDocument();
  });

  it('mounts the same Onboarding for a signed-out visitor with ?setup=guest, with no user behind it', async () => {
    bootParams.set('setup', 'guest');
    renderRouter();
    expect(await screen.findByText('Hi there — welcome to NextStepUni.')).toBeInTheDocument();
    expect(screen.queryByText('LOGIN PAGE')).not.toBeInTheDocument();
    expect(readGuestPhase()).toBe('onboarding');

    // The first step works, and the draft lands in the guest namespace, not an account's localStorage.
    fireEvent.click(screen.getByRole('button', { name: /Get Started/ }));
    expect(await screen.findByText('What year are you in?')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /6th/ }));
    await waitFor(() => expect(JSON.parse(guestStorage.getItem(GUEST_DESKTOP_DRAFT_KEY) ?? '{}')).toMatchObject({ version: 1, step: 2, yearGroup: '6th' }));
    expect(localStorage.length).toBe(0);
    expect(sessionStorage.getItem(`nsu:guest-setup:${GUEST_DESKTOP_DRAFT_KEY}`)).not.toBeNull();

    expect(authState.handleLoginSuccess).not.toHaveBeenCalled();
    allWriteSpies().forEach(spy => expect(spy).not.toHaveBeenCalled());
  });

  it('ends with "Dive in", leads to the placeholder, and writes nothing to Firestore or Auth', async () => {
    bootParams.set('setup', 'guest');
    guestStorage.setItem(GUEST_DESKTOP_DRAFT_KEY, JSON.stringify(reviewDraft()));
    renderRouter();

    expect(await screen.findByText('You\'re ready.')).toBeInTheDocument();
    const dive = screen.getByRole('button', { name: /Dive in/ });
    expect(screen.queryByRole('button', { name: /Start Learning/i })).not.toBeInTheDocument();

    fireEvent.click(dive);
    expect(await screen.findByRole('heading', { level: 1, name: /You’re set up/ })).toBeInTheDocument();
    expect(screen.getByText(/September 2027/)).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /Create your account/ })).toHaveAttribute('href', '/?from=landing');
    expect(screen.getByRole('link', { name: /Back to the landing page/ })).toHaveAttribute('href', '/landing-dev.html');
    expect(readGuestPhase()).toBe('dive-in');

    // The app's own onboarding save was never asked for, and no SDK write happened.
    expect(handleOnboardingComplete).not.toHaveBeenCalled();
    allWriteSpies().forEach(spy => expect(spy).not.toHaveBeenCalled());

    // What the guest built is kept, verbatim, for a later adoption.
    const result = readGuestSetupResult();
    expect(result?.profile).toMatchObject({ yearGroup: '6th', curriculumLevel: 'senior', examStartDate: '2030-06-05', restDays: ['Sunday'] });
    expect((result?.profile as { subjects: unknown[] }).subjects).toHaveLength(2);
    expect(guestStorage.getItem(GUEST_DESKTOP_DRAFT_KEY)).not.toBeNull();

    // "Create your account" leaves the guest phase but keeps the answers.
    fireEvent.click(screen.getByRole('link', { name: /Create your account/ }));
    expect(readGuestPhase()).toBeNull();
    expect(readGuestSetupResult()).not.toBeNull();
    expect(guestStorage.getItem(GUEST_DESKTOP_DRAFT_KEY)).not.toBeNull();
  });

  it('a reload after the URL is tidied resumes from the phase marker, and the Dive-in page is where it was left', async () => {
    // No boot param this time: NavigationContext has rewritten the URL, only the marker remains.
    setGuestPhase('dive-in');
    renderRouter();
    expect(await screen.findByRole('heading', { level: 1, name: /You’re set up/ })).toBeInTheDocument();
  });

  it('"Skip for now" returns to the landing page and throws the guest answers away', async () => {
    bootParams.set('setup', 'guest');
    const assign = vi.fn();
    const original = window.location;
    Object.defineProperty(window, 'location', { configurable: true, value: { ...original, assign, search: '', pathname: '/' } });
    try {
      renderRouter();
      fireEvent.click(await screen.findByRole('button', { name: 'Skip for now' }));
      expect(assign).toHaveBeenCalledWith('/landing-dev.html');
      expect(readGuestPhase()).toBeNull();
      expect(guestStorage.getItem(GUEST_DESKTOP_DRAFT_KEY)).toBeNull();
      expect(handleOnboardingSkip).not.toHaveBeenCalled();
      allWriteSpies().forEach(spy => expect(spy).not.toHaveBeenCalled());
    } finally {
      Object.defineProperty(window, 'location', { configurable: true, value: original });
    }
  });

  it('a signed-in student with ?setup=guest is never shown the guest flow', async () => {
    bootParams.set('setup', 'guest');
    setGuestPhase('onboarding');
    authState.user = { uid: 'student-1', name: 'Aoife Byrne', avatar: 'Charlie', isAdmin: false };

    const home = renderRouter();
    expect(await screen.findByText('KNOWLEDGE TREE')).toBeInTheDocument();
    expect(screen.queryByText(/Hi there/)).not.toBeInTheDocument();
    expect(screen.queryByText(/Dive in/)).not.toBeInTheDocument();
    home.unmount();

    // ...and a signed-in student who does need onboarding gets THEIR onboarding, not the guest one.
    authState.needsOnboarding = true;
    renderRouter();
    expect(await screen.findByText('Hi Aoife — welcome to NextStepUni.')).toBeInTheDocument();
    expect(screen.queryByText(/Dive in/)).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /Get Started/ }));
    await waitFor(() => expect(localStorage.getItem('nextstepuni:onboarding-draft:v1:student-1:fresh')).not.toBeNull());
    expect(guestStorage.getItem('nextstepuni:onboarding-draft:v1:student-1:fresh')).toBeNull();
  });

  it('keeps the draft through the unauthenticated-boot storage clear, but not past a deliberate end', () => {
    setGuestPhase('onboarding');
    guestStorage.setItem('draft-key', '{"kept":true}');
    // AuthContext → clearLocalSessionData() on an unauthenticated boot.
    sessionStorage.clear();
    expect(sessionStorage.getItem('nsu:guest-setup:draft-key')).toBeNull();
    restoreGuestSetupState();
    expect(sessionStorage.getItem('nsu:guest-setup:draft-key')).toBe('{"kept":true}');
    expect(readGuestPhase()).toBe('onboarding');

    endGuestSetup({ keepDraft: false });
    sessionStorage.clear();
    restoreGuestSetupState();
    expect(sessionStorage.getItem('nsu:guest-setup:draft-key')).toBeNull();
    expect(readGuestPhase()).toBeNull();
  });

  it('the funnel records nothing for a guest, and resumes for everyone else', () => {
    setGuestPhase('onboarding');
    trackFunnel('onboarding_started');
    trackFunnel('onboarding_completed');
    expect(firestoreSpies.addDoc).not.toHaveBeenCalled();

    endGuestSetup({ keepDraft: false });
    trackFunnel('first_tool_opened');
    expect(firestoreSpies.addDoc).toHaveBeenCalledTimes(1);
  });
});

describe('the Dive-in placeholder', () => {
  it('states the launch window, offers exactly two actions, and shows no payment UI', () => {
    const onCreateAccount = vi.fn();
    const onBackToLanding = vi.fn();
    render(<DiveIn onCreateAccount={onCreateAccount} onBackToLanding={onBackToLanding} />);
    expect(screen.getByText(/Accounts and payment open at launch/)).toBeInTheDocument();
    expect(screen.getByText(/September 2027/)).toBeInTheDocument();

    const links = screen.getAllByRole('link');
    expect(links.map(a => a.getAttribute('href'))).toEqual(['/?from=landing', '/landing-dev.html']);
    expect(screen.queryAllByRole('button')).toHaveLength(0);
    expect(document.body.textContent).not.toMatch(/€|\$|per month|per year|price/i);

    fireEvent.click(links[0]);
    fireEvent.click(links[1]);
    expect(onCreateAccount).toHaveBeenCalledOnce();
    expect(onBackToLanding).toHaveBeenCalledOnce();
  });

  it('carries the open decision about payment order as a comment at the decision point', () => {
    expect(readSource('components/DiveIn.tsx')).toMatch(/DECISION PENDING[\s\S]*BEFORE payment[\s\S]*AFTER it/);
  });
});

describe('the landing page entry', () => {
  it('links "Set up without an account" from the How-it-works CTA row, keeping from=landing', () => {
    expect(APP_SETUP_URL).toBe('/?from=landing&setup=guest');
    const source = readSource('components/landing/sections/HowItWorks.tsx');
    expect(source).toContain('href={APP_SETUP_URL}');
    expect(source).toContain('{APP_SETUP_LABEL}');
    // The hero carries one action only (Alex, 2026-09-09).
    expect(readSource('components/landing/sections/Hero.tsx')).not.toContain('APP_SETUP_URL');
  });
});
