/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The signup route crosses three independently-resolved states: registration,
 * AuthContext's Firestore read, and ProgressContext's mirrored snapshot. The
 * app used to replace the account-setup loader with App.tsx's default loader
 * in the middle, producing a one-second "Loading your workspace" interstitial.
 * These source contracts keep a single router-owned presentation through the
 * handoff while retaining the guard against stale student chrome.
 */
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';

const ROOT = resolve(__dirname, '..');
const readSource = (path: string) => readFileSync(resolve(ROOT, path), 'utf8');

describe('onboarding loading handoff', () => {
  it('keeps progress hydration inside AppRouter instead of replacing the router', () => {
    const app = readSource('App.tsx');

    expect(app).not.toContain("import { LoadingSpinner } from './components/LoadingSpinner'");
    expect(app).not.toMatch(/if \(user && !isProgressReadyForUser[\s\S]*?return <LoadingSpinner/);
    expect(app).toContain('const userProgressReady = user !== null');
    expect(app).toContain('<AppRouter {...routerProps} />');
    expect(app).toContain('user && userProgressReady && shouldShowStudentChrome(viewState)');
  });

  it('uses one account-setup presentation through hydration and lazy onboarding', () => {
    const router = readSource('components/AppRouter.tsx');

    expect(router).toContain('const ACCOUNT_SETUP_LOADING = (');
    expect(router).toContain('<LoadingSpinner overlay kicker="One moment" label="Setting up your account" />');
    expect(router).toContain('return needsOnboarding ? ACCOUNT_SETUP_LOADING : <LoadingSpinner />;');
    expect(router).toContain('<Suspense fallback={ACCOUNT_SETUP_LOADING}>');
  });

  it('publishes onboarding intent synchronously for every new-account success path', () => {
    const auth = readSource('contexts/AuthContext.tsx');
    const login = readSource('components/LoginPage.tsx');

    expect(auth).toContain('options?.requiresOnboarding');
    expect(auth).toContain('setLoadedData(previous => ({ ...previous, needsOnboarding: true }))');
    expect(login.match(/requiresOnboarding: true/g)).toHaveLength(3);

    const emailRegistration = login.indexOf('userDocStarted = true;');
    const onboardingIntent = login.indexOf('{ requiresOnboarding: true }', emailRegistration);
    const provisioningRelease = login.indexOf('endRegistrationProvisioning();', emailRegistration);

    expect(emailRegistration).toBeGreaterThan(-1);
    expect(onboardingIntent).toBeGreaterThan(emailRegistration);
    expect(provisioningRelease).toBeGreaterThan(onboardingIntent);
  });
});
