/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo, useEffect, useRef } from 'react';
import { AnimatePresence, useReducedMotion } from 'framer-motion';
import { MotionButton, MotionDiv } from './Motion';
import { ArrowLeft, Eye, EyeOff, GraduationCap, ArrowRight, Check, LockKeyhole, UserRound, BarChart3, ExternalLink, X } from 'lucide-react';
import { Capacitor } from '@capacitor/core';
import { authorizeWithApple } from '../utils/appleAuth';
import app, { auth, db } from '../firebase';
import { shouldReapAccount } from '../utils/registrationRollback';
import { type LoginSuccessOptions } from '../contexts/AuthContext';
import { signInWithEmailAndPassword, createUserWithEmailAndPassword, updateProfile, deleteUser, sendPasswordResetEmail, sendEmailVerification, signOut, GoogleAuthProvider, signInWithPopup, signInWithCredential } from 'firebase/auth';
import { doc, getDoc, setDoc } from 'firebase/firestore';
import { getFunctions, httpsCallable } from 'firebase/functions';
import { type SessionUser, AVATAR_SEEDS } from '../utils/authUtils';
import { awaitWriteOrTimeout, saveInBackground } from '../utils/firestoreWrite';
import { logError } from '../utils/logError';
import { trackFunnel } from '../utils/funnel';
import { trackProgrammeEvent } from '../utils/programmeAnalytics';
import { isReservedEmail, isVerifiedAdminSession } from '../utils/adminIdentity';
import {
  beginRegistrationProvisioning,
  endRegistrationProvisioning,
  stashRegistrationError,
  takeRegistrationError,
} from '../utils/registrationProvisioning';
import { getRegistrationErrorCode, registrationErrorField, registrationErrorMessage } from '../utils/registrationErrors';
import { SCHOOLS } from '../schoolData';
import { createDemoStudentSession } from '../data/devStudent';
import { MAX_PASSWORD_LENGTH, MIN_PASSWORD_LENGTH, passwordLengthError } from '../utils/passwordPolicy';
import { LegalModal, type LegalDoc, PRIVACY_POLICY_VERSION, CONSENT_BASIS } from './legal/LegalModal';
import { DEFAULT_PERSONAL_STAR_CREW_ID } from '../data/personalStarCrew';
import { pickLoadingCrew } from '../utils/loadingCrew';
import { useModal } from '../hooks/useModal';
import { useMobileAppDesign } from '../hooks/useMobileAppDesign';
import AccountCard from './AccountCard';
import AccountSchoolPicker from './AccountSchoolPicker';
import SchoolCrest from './SchoolCrest';
import AccountCrewPicker from './AccountCrewPicker';
import { Checkbox } from './account-ui-runtime';

/**
 * Did this visit start at the landing page? Read once, at module load, because
 * the router tidies the query string away before this page renders; the
 * referrer covers a reload of the sign-in page. It only changes the landing
 * link's wording: "Back to" rather than "See".
 */
const FROM_LANDING = (() => {
  try {
    return new URLSearchParams(window.location.search).get('from') === 'landing' || /\/landing(-dev\.html)?([?#]|$)/.test(document.referrer);
  } catch {
    return false;
  }
})();

// Google Sign-In uses signInWithPopup, which has no real popup to open inside
// Capacitor's webview on EITHER platform. Web only, until a native Google plugin
// is wired up — on Android that also means registering the release signing
// SHA-1 with Firebase, which is why v1 of the Android app ships without it.
const SHOW_GOOGLE_SIGN_IN = !Capacitor.isNativePlatform();

// Sign in with Apple runs through this app's own native plugin
// (ios/App/App/SignInWithApplePlugin.swift, built on Apple's system
// AuthenticationServices — no third-party SDK), which exists on iOS and nowhere
// else.
//
// This used to read `Capacitor.isNativePlatform()`. That is equally true on
// Android, where there is no implementation behind the bridge — so the Android
// build would have shown an Apple button that could only fail when tapped. It
// was written when iOS was the only native target and "native" and "iOS" were
// accidentally synonymous. Gate on the platform, not on nativeness.
const SHOW_APPLE_SIGN_IN = Capacitor.getPlatform() === 'ios';

// Apple Sign-In + Firebase replay protection: send Apple a SHA-256 hash of a
// random nonce, then hand Firebase the *raw* nonce so it can verify the hash in
// the returned identity token.

// Slide-and-fade for view/step transitions. Direction-aware:
// `custom={1}` slides forward (new view enters from right),
// `custom={-1}` slides back (new view enters from left). Pure
// tween easing keeps it crisp — no spring wobble.
const SLIDE_DISTANCE = 20;
const SLIDE_EASE = [0.32, 0.72, 0, 1] as const;
const slideTransition = { duration: 0.34, ease: SLIDE_EASE };
const slideVariants = {
  enter: (dir: number) => ({ x: dir * SLIDE_DISTANCE, opacity: 0 }),
  center: { x: 0, opacity: 1 },
  exit: (dir: number) => ({ x: dir * -SLIDE_DISTANCE, opacity: 0 }),
};

// Depth ordering for the auth views — used to compute swipe direction.
// Welcome is root (0); login/register/gc are one level in (1); forgot
// sits behind login (2). Going deeper slides forward, going shallower
// slides back.
const VIEW_DEPTH: Record<string, number> = {
  welcome: 0,
  login: 1,
  register: 1,
  gc: 1,
  forgot: 2,
};

const btnHover = { scale: 1.02, y: -1 };
const btnTap = { scale: 0.97, y: 1 };

// ── Google G logo, official 4-colour ──
const GoogleIcon: React.FC<{ size?: number }> = ({ size = 18 }) => (
  <svg width={size} height={size} viewBox="0 0 18 18" xmlns="http://www.w3.org/2000/svg" aria-hidden>
    <path d="M17.64 9.2c0-.637-.057-1.251-.164-1.84H9v3.481h4.844c-.209 1.125-.843 2.078-1.796 2.717v2.258h2.908c1.702-1.567 2.684-3.874 2.684-6.615z" fill="#4285F4" />
    <path d="M9 18c2.43 0 4.467-.806 5.956-2.18l-2.908-2.259c-.806.54-1.837.86-3.048.86-2.344 0-4.328-1.584-5.036-3.711H.957v2.332C2.438 15.983 5.482 18 9 18z" fill="#34A853" />
    <path d="M3.964 10.71c-.18-.54-.282-1.117-.282-1.71 0-.593.102-1.17.282-1.71V4.958H.957C.347 6.173 0 7.548 0 9c0 1.452.348 2.827.957 4.042l3.007-2.332z" fill="#FBBC05" />
    <path d="M9 3.58c1.321 0 2.508.454 3.44 1.345l2.582-2.58C13.463.891 11.426 0 9 0 5.482 0 2.438 2.017.957 4.958L3.964 7.29C4.672 5.163 6.656 3.58 9 3.58z" fill="#EA4335" />
  </svg>
);

// ── Apple logo glyph (white, for the black "Continue with Apple" button) ──
const AppleIcon: React.FC<{ size?: number }> = ({ size = 18 }) => (
  <svg width={size} height={size} viewBox="0 0 17 21" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden>
    <path d="M14.07 11.17c-.02-2.18 1.78-3.23 1.86-3.28-1.01-1.48-2.59-1.69-3.15-1.71-1.34-.14-2.61.79-3.29.79-.68 0-1.72-.77-2.83-.75-1.46.02-2.8.85-3.55 2.16-1.51 2.62-.39 6.5 1.09 8.62.72 1.04 1.58 2.21 2.71 2.17 1.09-.04 1.5-.7 2.82-.7 1.31 0 1.69.7 2.83.68 1.17-.02 1.91-1.06 2.62-2.1.83-1.21 1.17-2.38 1.19-2.44-.03-.01-2.28-.88-2.3-3.47zM11.9 4.56c.6-.73 1.01-1.74.9-2.75-.87.04-1.92.58-2.54 1.3-.55.64-1.04 1.67-.91 2.66.97.08 1.96-.49 2.55-1.21z" fill="#FFFFFF" />
  </svg>
);

interface LoginPageProps {
  handleLoginSuccess: (u: SessionUser, options?: LoginSuccessOptions) => void;
}

/**
 * Write a user doc during sign-up without the possibility of an infinite stall.
 *
 * These writes run immediately after a successful Auth call, so the client is
 * essentially always online here — but a connection can drop in the gap, and a
 * Firestore write promise settles only on SERVER acknowledgement, so a plain
 * await could hang the registration screen forever with no error.
 *
 * A bounded wait keeps the existing contract: a genuine rejection still throws
 * (so handleRegisterSubmit's deleteUser rollback still fires), while a write
 * that is merely queued resolves normally — it will flush on reconnect.
 */
async function writeUserDoc(
  write: Promise<void>,
  context: string,
  onLateRejection?: (err: unknown) => void,
): Promise<void> {
  // Capture the ORIGINAL error. awaitWriteOrTimeout collapses a rejection to
  // the string 'failed', and throwing a bare Error in its place strips
  // `err.code` — which silently re-broke LoginPage's 'permission-denied'
  // branch, the very branch added so a rules denial stops masquerading as an
  // auth failure.
  let captured: unknown;
  const watched = write.catch((err: unknown) => { captured = err; throw err; });
  // Swallow the late rejection so an 8s timeout can't leave an unhandled
  // rejection, and give the caller a chance to clean up (e.g. delete a
  // half-created account) if the answer arrives after we stopped waiting.
  watched.catch((err: unknown) => { onLateRejection?.(err); });
  const outcome = await awaitWriteOrTimeout(watched, context, 8000);
  if (outcome === 'failed') throw captured ?? new Error(`${context}: write rejected`);
}

const LoginPage: React.FC<LoginPageProps> = ({ handleLoginSuccess }) => {
  const mobileAppDesign = useMobileAppDesign();
  const reducedMotion = useReducedMotion();
  const viewTransition = reducedMotion ? { duration: 0 } : slideTransition;
  // ── Top-level mode ──
  const [view, setView] = useState<'welcome' | 'login' | 'register' | 'gc' | 'forgot'>(() => mobileAppDesign ? 'login' : 'welcome');

  // Boot the join-code function while the student is still typing.
  //
  // claimStudentSchool is the only callable on the signup path and it scales to
  // zero: measured 3.02s cold against 0.165s warm, and every bit of that sits
  // behind the "Setting up your account" screen, because registration cannot
  // call it any earlier — it needs an account that does not exist yet. What it
  // CAN do is start the container early. This ping is rejected by the very
  // first line of the function (`if (!request.auth) throw unauthenticated`),
  // before it reads Firestore, touches the brute-force counter or opens a
  // transaction, so it has no side effect whatsoever; the rejection is the
  // expected outcome and the boot is the point. Filling in name, email,
  // password, school and join code takes far longer than the ~3s boot, so by
  // submit time the container is warm.
  //
  // This is the cheap half of the cold-start fix. The other half is
  // minInstances on the function, which removes the cold start for everyone
  // (including the first GC of the morning) but bills continuously — an
  // owner's call, not one to make in a patch.
  const prewarmedRef = useRef(false);
  useEffect(() => {
    if (view !== 'register' || prewarmedRef.current) return;
    prewarmedRef.current = true;
    httpsCallable(getFunctions(app), 'claimStudentSchool')({}).catch(() => {});
  }, [view]);
  const [registerStep, setRegisterStep] = useState(1); // 1: details, 2: school, 3: password, 4: character + consent

  // ── Form state ──
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [school, setSchool] = useState('');
  const [joinCode, setJoinCode] = useState('');
  const [gcSchool, setGcSchool] = useState('');
  // One school door, two shared logins: the counsellor's and the staff room's.
  const [schoolRole, setSchoolRole] = useState<'gc' | 'staff'>('gc');
  const [avatar, setAvatar] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  // A failed registration deletes the account it just created, which signs the
  // student out and can unmount THIS component -- so setError below lands on a
  // dead instance and the replacement renders blank. That silent bounce is the
  // symptom students actually reported. The reason is handed over as a code and
  // the copy resolved here, so no rendered string is ever persisted.
  const [error, setError] = useState(() => {
    const code = takeRegistrationError();
    return code ? registrationErrorMessage(code) : '';
  });
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});
  const rejectField = (id: string, message: string) => {
    setError('');
    setFieldErrors({ [id]: message });
    requestAnimationFrame(() => document.getElementById(id)?.focus());
    return false;
  };
  const fieldValidation = (id: string) => ({
    'aria-invalid': Boolean(fieldErrors[id]),
    'aria-describedby': fieldErrors[id] ? `${id}-error` : undefined,
  });
  const fieldMessage = (id: string) => fieldErrors[id] && <small id={`${id}-error`} className="auth-live-field-error" role="alert">{fieldErrors[id]}</small>;
  const [isLoading, setIsLoading] = useState(false);
  const [resetSent, setResetSent] = useState(false);
  const [resendCountdown, setResendCountdown] = useState(0);
  // B4 (audit 2026-06-01): student must accept the Privacy Notice + Terms
  // before an account is created; `legalDoc` controls the reachable policy modal.
  const [agreedToTerms, setAgreedToTerms] = useState(false);
  const [legalDoc, setLegalDoc] = useState<LegalDoc | null>(null);
  const [entryHelp, setEntryHelp] = useState<'code' | 'reset' | null>(null);
  const entryHelpRef = useRef<HTMLDivElement>(null);
  useModal(Boolean(entryHelp), () => setEntryHelp(null), entryHelpRef);
  const authViewRef = useRef<HTMLDivElement>(null);
  const characterHeadingRef = useRef<HTMLHeadingElement>(null);

  // Direction tracking for view transitions. Computed synchronously on
  // each render so AnimatePresence sees the correct direction the moment
  // the new key arrives — useEffect-based tracking would lag by one frame.
  const prevViewRef = useRef(view);
  const viewDirection = useMemo(() => {
    const next = VIEW_DEPTH[view] ?? 0;
    const prev = VIEW_DEPTH[prevViewRef.current] ?? 0;
    return next >= prev ? 1 : -1;
  }, [view]);
  useEffect(() => { prevViewRef.current = view; }, [view]);

  const prevStepRef = useRef(registerStep);
  const stepDirection = useMemo(
    () => (registerStep >= prevStepRef.current ? 1 : -1),
    [registerStep],
  );
  useEffect(() => { prevStepRef.current = registerStep; }, [registerStep]);

  // Auth states are separate screens on mobile. Do not carry the keyboard's
  // previous document offset into the next screen or hide its back control.
  useEffect(() => {
    if (window.matchMedia('(min-width: 768px)').matches) return;
    const resetAuthScroll = () => {
      const scrollRoot = document.scrollingElement ?? document.documentElement;
      scrollRoot.scrollTop = 0;
      scrollRoot.scrollLeft = 0;
      document.body.scrollTop = 0;
    };
    resetAuthScroll();
    // AnimatePresence swaps screens over 340ms. Reset once more after that
    // layout settles so browser scroll anchoring cannot preserve a field from
    // the previous screen instead of the new screen's header.
    const settledReset = window.setTimeout(() => {
      resetAuthScroll();
      // Keep the form and its controls in view after changing steps.
      const scrollTarget = view === 'register' ? authViewRef.current?.closest('.auth-live-card') : authViewRef.current;
      if (typeof scrollTarget?.scrollIntoView === 'function') {
        scrollTarget.scrollIntoView({ block: 'start', inline: 'nearest', behavior: 'auto' });
      }
    }, 460);
    return () => window.clearTimeout(settledReset);
  }, [view, registerStep]);

  // Countdown tick for the resend button on the forgot-password success screen.
  useEffect(() => {
    if (resendCountdown <= 0) return;
    const t = setTimeout(() => setResendCountdown(c => c - 1), 1000);
    return () => clearTimeout(t);
  }, [resendCountdown]);

  // Fallback for existing accounts without a saved avatar.
  const defaultAvatar = useMemo(() => pickLoadingCrew().id, []);

  // ── Login handler ──
  const handleLogin = async () => {
    if (isLoading) return;
    if (!email.trim()) { rejectField('login-email', 'Enter your email or username.'); return; }
    if (!password.trim()) { rejectField('login-password', 'Enter your password.'); return; }
    setIsLoading(true); setError(''); setFieldErrors({});
    const input = email.trim().toLowerCase();
    // Try as-is first (real email), then fall back to legacy @nextstep.app format
    const attempts = input.includes('@') ? [input] : [input, `${input}@nextstep.app`];
    let success = false;
    for (const emailToTry of attempts) {
      try {
        const cred = await signInWithEmailAndPassword(auth, emailToTry, password);
        const token = await cred.user.getIdTokenResult();
        const userDoc = await getDoc(doc(db, 'users', cred.user.uid));
        if (userDoc.exists()) {
          const data = userDoc.data();
          handleLoginSuccess({
            uid: cred.user.uid,
            name: data.name || 'Student',
            avatar: data.avatar || 'James',
            // Admin is the verified auth identity, not a doc field — matches
            // AuthContext and firestore.rules' server-side admin check.
            // (Security review 2026-07-16, LOW — single source of truth.)
            isAdmin: isVerifiedAdminSession(cred.user, token.claims),
            role: data.role || 'student',
            school: data.school || '',
            yearGroup: data.yearGroup,
          });
        }
        success = true;
        break;
      } catch (err) {
        console.error('Login attempt failed:', err);
      }
    }
    if (!success) setError('Invalid email or password.');
    setIsLoading(false);
  };

  // ── Google sign-in handler ──
  const handleGoogleSignIn = async () => {
    if (isLoading) return;
    setIsLoading(true); setError(''); setFieldErrors({});
    try {
      const provider = new GoogleAuthProvider();
      const cred = await signInWithPopup(auth, provider);
      const token = await cred.user.getIdTokenResult();
      const userRef = doc(db, 'users', cred.user.uid);
      const userDoc = await getDoc(userRef);
      if (userDoc.exists()) {
        const data = userDoc.data();
        handleLoginSuccess({
          uid: cred.user.uid,
          name: data.name || cred.user.displayName || 'Student',
          avatar: data.avatar || AVATAR_SEEDS[0],
          // Admin is the verified auth identity, not a doc field. (Security
          // review 2026-07-16, LOW — single source of truth.)
          isAdmin: isVerifiedAdminSession(cred.user, token.claims),
          role: data.role || 'student',
          school: data.school || '',
          yearGroup: data.yearGroup,
        });
      } else {
        // First-time Google sign-in: create the user doc WITHOUT a school —
        // `school` is set only by the claimStudentSchool Cloud Function once a
        // valid join code is presented (security review H-2). The client is
        // forbidden from writing `school` by the /users create rule.
        const newName = cred.user.displayName || (cred.user.email?.split('@')[0]) || 'Student';
        const newAvatar = avatar || defaultAvatar;
        await writeUserDoc(setDoc(userRef, { name: newName, avatar: newAvatar, createdAt: new Date().toISOString() }), 'LoginPage.googleCreateUserDoc');
        handleLoginSuccess({
          uid: cred.user.uid,
          name: newName,
          avatar: newAvatar,
          school: '',
          role: 'student',
        }, { requiresOnboarding: true });
      }
    } catch (err: any) {
      if (err.code === 'auth/popup-closed-by-user' || err.code === 'auth/cancelled-popup-request') {
        // Silent — user dismissed the popup
      } else if (err.code === 'auth/operation-not-allowed') {
        setError('Google sign-in is not enabled. Contact support.');
      } else if (err?.code === 'permission-denied') {
        // A Firestore rules rejection is NOT an auth failure — say so, or the
        // real cause stays invisible behind a generic sign-in error.
        console.error('Google sign-in: user doc write rejected by rules:', err);
        setError('Signed in, but your profile could not be created. Please contact your school.');
      } else {
        console.error('Google sign-in failed:', err);
        setError('Could not sign in with Google. Try again or use email.');
      }
    }
    setIsLoading(false);
  };

  // ── Sign in with Apple handler (native iOS only) ──
  const handleAppleSignIn = async () => {
    if (isLoading) return;
    setIsLoading(true); setError(''); setFieldErrors({});
    try {
      // Native Apple sign-in via AuthenticationServices (no third-party SDK).
      // The nonce pairing lives in utils/appleAuth so the deletion flow's
      // re-authentication uses the identical exchange.
      const { credential, result } = await authorizeWithApple();
      const cred = await signInWithCredential(auth, credential);
      const token = await cred.user.getIdTokenResult();

      // Apple returns the user's name ONLY on the first authorization.
      const appleName = [result.givenName, result.familyName]
        .filter(Boolean).join(' ').trim();

      const userRef = doc(db, 'users', cred.user.uid);
      const userDoc = await getDoc(userRef);
      if (userDoc.exists()) {
        const data = userDoc.data();
        handleLoginSuccess({
          uid: cred.user.uid,
          name: data.name || appleName || cred.user.displayName || 'Student',
          avatar: data.avatar || AVATAR_SEEDS[0],
          isAdmin: isVerifiedAdminSession(cred.user, token.claims),
          role: data.role || 'student',
          school: data.school || '',
          yearGroup: data.yearGroup,
        });
      } else {
        // First-time Apple sign-in: create the user doc (school empty, set later
        // in-app). Record the policy version under which the account was created,
        // matching the email-registration flow. NOTE: the explicit in-app
        // Privacy/Terms acceptance checkbox is not shown on the social path
        // (same as Google); parental consent is captured at school enrolment
        // (basis = school-enrolment). See compliance/DPIA.md.
        const newName = appleName || cred.user.displayName || 'Student';
        const newAvatar = avatar || defaultAvatar;
        await writeUserDoc(setDoc(userRef, {
          name: newName,
          avatar: newAvatar,
          // NO `school` field. The /users create rule rejects the doc if the
          // key is present AT ALL, whatever its value — so `school: ''` made
          // this create fail permission-denied every time, and the catch below
          // reported it as "Could not sign in with Apple" on a sign-in that had
          // actually succeeded. The in-memory session passes school: '' itself.
          createdAt: new Date().toISOString(),
          consent: {
            policyVersion: PRIVACY_POLICY_VERSION,
            acceptedAt: new Date().toISOString(),
            basis: CONSENT_BASIS,
          },
        }), 'LoginPage.appleCreateUserDoc');
        handleLoginSuccess(
          { uid: cred.user.uid, name: newName, avatar: newAvatar, school: '', role: 'student' },
          { requiresOnboarding: true },
        );
      }
    } catch (err: any) {
      // The plugin rejects with code 'USER_CANCELLED' when the user dismisses the sheet.
      if (err?.code === 'USER_CANCELLED' || /cancel/i.test(err?.message || '')) {
        // Silent — user dismissed the Apple sheet
      } else if (err?.code === 'permission-denied') {
        console.error('Apple sign-in: user doc write rejected by rules:', err);
        setError('Signed in, but your profile could not be created. Please contact your school.');
      } else {
        console.error('Apple sign-in failed:', err);
        setError('Could not sign in with Apple. Try again or use email.');
      }
    }
    setIsLoading(false);
  };

  // ── Forgot password handler ──
  const handleForgotPassword = async () => {
    if (isLoading || resendCountdown > 0) return;
    if (!email.trim()) { rejectField('reset-email', 'Enter your email address.'); return; }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim())) {
      rejectField('reset-email', 'Check the email address, for example you@example.com.');
      return;
    }
    setIsLoading(true); setError(''); setFieldErrors({});
    try {
      await sendPasswordResetEmail(auth, email.trim().toLowerCase());
      setResetSent(true);
      setResendCountdown(30);
    } catch (err) {
      console.error('Failed to send password reset email:', err);
      setError('Could not send reset email. Check your email address.');
    }
    setIsLoading(false);
  };

  // ── School login handler (guidance counsellor or staff room) ──
  const handleGCLogin = async () => {
    if (isLoading) return;
    if (!gcSchool || !password.trim()) { setError('Please select your school and enter your password.'); return; }
    setIsLoading(true); setError(''); setFieldErrors({});
    try {
      await signInWithEmailAndPassword(auth, `${schoolRole}-${gcSchool}@nextstep.app`, password);
    } catch (err: any) {
      // Surface a more specific message so we know whether the GC account is
      // missing entirely vs. wrong password vs. network issue.
      // Use a single generic message for all credential errors. GC emails are
      // deterministic (gc-{schoolId}@nextstep.app) and the school list is
      // public, so a "no account for this school" vs "wrong password" split
      // would let anyone enumerate which schools have a provisioned GC account
      // to target. (Security review 2026-07-16, MEDIUM — account enumeration.)
      console.error('School login failed:', err.code, err.message);
      if (err.code === 'auth/network-request-failed') {
        setError('Network error. Check your connection and try again.');
      } else {
        setError('Sign-in failed. Check your school and password, or contact support.');
      }
    }
    setIsLoading(false);
  };

  // ── Register step validation ──
  const validateRegisterStep = (): boolean => {
    if (registerStep === 1) {
      if (!name.trim()) { return rejectField('register-name', 'Enter your name.'); }
      if (!email.trim()) { return rejectField('register-email', 'Enter your email address.'); }
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim())) { return rejectField('register-email', 'Check the email address, for example you@example.com.'); }
      const normalised = email.trim().toLowerCase();
      if (isReservedEmail(normalised)) { return rejectField('register-email', 'Use a different email address.'); }
      return true;
    }
    if (registerStep === 2) {
      if (!school) { return rejectField('register-school', 'Choose your school.'); }
      if (!joinCode.trim()) { return rejectField('register-join-code', 'Enter the join code from your school.'); }
      return true;
    }
    if (registerStep === 3) {
      const passwordError = passwordLengthError(password);
      if (passwordError) { return rejectField('register-password', passwordError); }
      return true;
    }
    return true;
  };

  const handleRegisterNext = () => {
    setError(''); setFieldErrors({});
    if (!validateRegisterStep()) return;
    if (registerStep === 3) setAvatar(current => current || DEFAULT_PERSONAL_STAR_CREW_ID);
    if (registerStep < 4) setRegisterStep(s => s + 1);
  };

  // ── Register submit (step 4) ──
  const handleRegisterSubmit = async () => {
    if (isLoading) return;
    if (!avatar) { setError('Choose your Star Crew character to continue.'); return; }
    setIsLoading(true); setError(''); setFieldErrors({});
    const registrationEmail = email.trim().toLowerCase();
    if (isReservedEmail(registrationEmail)) {
      setError('This email is reserved.');
      setIsLoading(false);
      return;
    }
    if (!agreedToTerms) {
      setError('Please confirm you have read the Privacy Notice and Terms of Use to continue.');
      setIsLoading(false);
      return;
    }
    const selectedAvatar = avatar || defaultAvatar;
    let createdUser: any = null;
    // Did we get as far as the /users write? Everything before it (join code,
    // ID token) leaves an account that never became usable and SHOULD be
    // reaped. The write itself does not -- see the catch.
    let userDocStarted = false;
    try {
      // Hold the router BEFORE the account exists. createUserWithEmailAndPassword
      // signs the student in immediately, and AuthContext's no-user-doc fallback
      // then routes them into Onboarding ~1s later -- while the rollback below can
      // still delete the account underneath them. See utils/registrationProvisioning.
      beginRegistrationProvisioning(Date.now(), selectedAvatar);
      // Warm the onboarding chunk while the account is being provisioned. Every
      // student who gets past this line lands in Onboarding, and AppRouter
      // lazy-loads it — so without this the 44KB fetch starts only once the
      // setup screen finally clears, adding itself to the end of the wait
      // instead of overlapping it. Same module specifier as AppRouter's lazy()
      // import, so this populates the very module the router then asks for.
      // Fire-and-forget: a failed prefetch just means the normal lazy load runs.
      void import('./Onboarding').catch(() => {});
      const cred = await createUserWithEmailAndPassword(auth, registrationEmail, password);
      createdUser = cred.user;
      // Send a verification email (fire-and-forget) so the address is provable.
      // Non-blocking: registration still proceeds (security review 2026-07-16,
      // L-5). Deliverability failures must not block sign-up.
      sendEmailVerification(createdUser).catch(err => console.error('Failed to send verification email:', err));
      // Verify the school join code SERVER-SIDE and bind the student to the
      // school (security review H-2). `school` is set by the function, not the
      // client — the /users rules forbid a client-supplied school. A wrong code
      // throws here and the account is rolled back below.
      const joinFn = httpsCallable<{ school: string; code: string }, { success: boolean }>(getFunctions(app), 'claimStudentSchool');
      // Concurrent, not sequential. Neither reads the other's result, so
      // awaiting them in series bought nothing but a round trip the student
      // spends staring at a setup screen.
      //
      // Both are still awaited, because the account-rollback below keys off
      // whether we got this far. Note what awaiting does NOT buy: it does not
      // order updateProfile against AuthContext's displayName fallback.
      // onAuthStateChanged does not re-fire for a profile update — it notifies
      // only when the uid changes — so AuthContext samples displayName exactly
      // once per sign-in, whenever its own read settles, and nothing here can
      // move that. The fallback race is pre-existing and unchanged either way.
      await Promise.all([
        updateProfile(createdUser, { displayName: name.trim() }),
        joinFn({ school, code: joinCode.trim() }),
      ]);
      // No getIdToken(true) here, deliberately. It was copied from the old
      // teacher-claim path, where the claim callable DID set role/school custom
      // claims and the token genuinely had to refresh. claimStudentSchool sets
      // no claim at all — syncAuthorizationClaims mirrors role and school into a
      // token only for 'gc' and 'staff', and explicitly deletes both for a
      // student, because student tenancy is resolved from the live user document
      // instead. So the refreshed token was byte-for-byte equivalent in every
      // claim the app reads: a full round trip to securetoken.googleapis.com
      // that could not change any decision, on the critical path of every
      // signup. If a student claim is ever introduced, this has to come back.
      const userDocPayload = {
        name: name.trim(),
        avatar: selectedAvatar,
        // Signup date on the user doc, not just on subjectProfile — a student
        // who skips onboarding never gets a subjectProfile, and without any
        // createdAt the GC's status classifier pinned them at "New" forever.
        createdAt: new Date().toISOString(),
        // B4 (audit 2026-06-01): record acceptance of the transparency notice +
        // terms. The Art 8 parental consent itself is captured at school
        // enrolment (basis = school-enrolment); see compliance/DPIA.md.
        consent: {
          policyVersion: PRIVACY_POLICY_VERSION,
          acceptedAt: new Date().toISOString(),
          basis: CONSENT_BASIS,
        },
      };
      // Late rejection: the /users write was still in flight when we stopped
      // waiting, and the answer — a rejection — arrives seconds later.
      //
      // This handler used to call deleteUser(). By the time it runs the student
      // is signed in and part-way through onboarding, so deleting the account
      // signed them out mid-flow and destroyed the account they had just made:
      // they landed back on the login screen with no way back in, and no error
      // that explained it. The cure was far worse than the orphaned user doc it
      // was written to prevent, and because it is a timing race it hit only
      // some students, which is what made it so hard to see (2026-08-17).
      //
      // Retry instead. setDoc(merge) is idempotent, so a transient failure —
      // by far the likeliest cause here — self-heals. If the retry also fails
      // the student keeps their session and their place; AuthContext's
      // no-user-doc fallback carries them, and the write flushes from the
      // Firestore cache on reconnect. NEVER destroy a live session from a
      // background callback.
      const retryUserDoc = (err: unknown) => {
        logError('LoginPage.registerUserDoc.lateRejection', err);
        saveInBackground(
          setDoc(doc(db, 'users', createdUser!.uid), userDocPayload, { merge: true }),
          'LoginPage.registerUserDocRetry',
          undefined,
          { silent: true },
        );
      };
      userDocStarted = true;
      // Publish the new-account destination BEFORE releasing the router hold.
      // Auth and progress hydrate independently, so releasing first creates a
      // render where the router sees a signed-in user but does not yet know
      // they need onboarding. That single render used the returning-user copy
      // ("Loading your workspace") between this setup screen and onboarding.
      handleLoginSuccess({
        uid: createdUser.uid,
        name: name.trim(),
        avatar: selectedAvatar,
        school,
        role: 'student',
      }, { requiresOnboarding: true });

      // The rollback is disarmed the instant userDocStarted flips —
      // shouldReapAccount returns false from here on — so the router hold has
      // nothing left to protect against and can come down after the onboarding
      // intent above is already available.
      // writeUserDoc waits on a SERVER acknowledgement (up to 8s on a poor
      // connection), and making a student stare at a setup screen for that is
      // pointless when the account is already safe. The finally below still
      // clears the marker; this is just the earliest correct moment.
      endRegistrationProvisioning();
      await writeUserDoc(
        setDoc(doc(db, 'users', createdUser.uid), userDocPayload, { merge: true }),
        'LoginPage.registerUserDoc',
        retryUserDoc,
      );
      trackFunnel('register_succeeded');
      trackProgrammeEvent('account_registered', { source: 'registration' });
    } catch (err: any) {
      // A failed /users write must NEVER cost the student their account.
      //
      // The auth account is valid at this point; only the doc write failed. The
      // student is already signed in -- AuthContext follows onAuthStateChanged,
      // not handleLoginSuccess -- so deleting here signs them out mid-flow and
      // destroys the account they just made, with no error that explains it.
      //
      // The late-rejection path was fixed this way on 2026-08-17. This is the
      // same race landing INSIDE the 8s window instead of after it, and it was
      // still deleting. Retry the write and carry on: setDoc(merge) is
      // idempotent, and AuthContext's no-user-doc fallback covers the student
      // until it lands.
      if (createdUser && !shouldReapAccount({ hasAccount: true, userDocStarted })) {
        // No retry call here: writeUserDoc registers onLateRejection on the
        // write itself, so it has already fired for THIS rejection. Retrying
        // again would just issue a duplicate setDoc.
        trackFunnel('register_succeeded');
        trackProgrammeEvent('account_registered', { source: 'registration' });
        // Onboarding intent was published synchronously before the hold came
        // down, so this recovery path can keep that same visual handoff.
        setIsLoading(false);
        return;
      }
      // Everything before the write leaves an orphaned auth account (a wrong
      // join code is the common one). Reaping it is right: it lets the student
      // retry with the same email instead of hitting email-already-in-use.
      if (shouldReapAccount({ hasAccount: !!createdUser, userDocStarted })) {
        try { await deleteUser(createdUser); } catch (rollbackErr) {
          console.error('Failed to clean up auth account after registration failure:', rollbackErr);
          // deleteUser failing is CORRELATED with the failure that triggered the
          // reap -- a dropped connection causes both. Recovery from the router
          // hold depends on an auth-state change, and a swallowed rejection
          // produces none, which would leave the student on a spinner with no
          // way out. Sign out instead: same escape the retired staff flow used.
          await signOut(auth).catch(() => {});
        }
      }
      // If the account was reaped, this component is already unmounted and
      // setError paints nothing -- so pass only the reason code to the next
      // instance. The rendered copy and any credentials stay out of storage.
      const code = getRegistrationErrorCode(err);
      const message = registrationErrorMessage(code);
      const field = registrationErrorField(code);
      stashRegistrationError(code);
      if (field) {
        setRegisterStep(field.step);
        setFieldErrors({ [field.id]: message });
        setError('');
      } else {
        setError(message);
      }
    } finally {
      // Always release the hold: on success, on a handled failure, and on the
      // early return in the catch. A marker left set would sit a later student
      // on a spinner until it self-expires.
      endRegistrationProvisioning();
    }
    setIsLoading(false);
  };

  // Localhost Demo Account — a deterministic in-memory student story for
  // viewing dashboards and progress features. It has no Firebase auth token
  // and never writes sample data to Firestore. Capacitor's native iOS webview
  // also serves from `localhost`, so the DEV and non-native checks are both
  // required to keep this affordance out of native and production builds.
  const isLocalHost = typeof window !== 'undefined'
    && /^(localhost|127\.0\.0\.1|\[::1\])$/.test(window.location.hostname);
  const isDevBuild = (import.meta as ImportMeta & { env: { DEV: boolean } }).env.DEV;
  const showDemoButton = isDevBuild && !Capacitor.isNativePlatform() && isLocalHost;
  const demoButton = showDemoButton ? (
    <MotionButton
      type="button"
      onClick={() => handleLoginSuccess(createDemoStudentSession())}
      whileHover={btnHover}
      whileTap={btnTap}
      aria-label="Open Demo Account with sample progress"
      className="mt-5 inline-flex min-h-11 items-center justify-center gap-2 rounded-xl border border-[#1A1A1A] bg-[#1A1A1A] px-5 text-xs font-bold tracking-[0.01em] text-white shadow-sm transition-colors hover:bg-[#33302d]"
    >
      <BarChart3 size={15} aria-hidden="true" />
      Demo Account
      <ArrowRight size={14} aria-hidden="true" />
    </MotionButton>
  ) : null;

  // The landing page (/landing) ships with the app, so the sign-in card always
  // offers it on the web; there is no landing page inside the native apps.
  // Arrived from its "Open the app": the link reads as the way back.
  const fromLanding = FROM_LANDING;
  const landingButton = !Capacitor.isNativePlatform() ? (
    <a
      href="/landing"
      className="mt-5 inline-flex min-h-11 items-center justify-center gap-2 rounded-xl border border-[#1A1A1A] bg-white px-5 text-xs font-bold tracking-[0.01em] text-[#1A1A1A] shadow-sm transition-colors hover:bg-[#F4F4F5]"
    >
      {fromLanding ? <ArrowLeft size={15} aria-hidden="true" /> : <ExternalLink size={15} aria-hidden="true" />}
      {fromLanding ? 'Back to the landing page' : 'See the landing page'}
    </a>
  ) : null;
  const devButtons = landingButton || demoButton ? (
    <div className="flex flex-wrap items-center justify-center gap-3">
      {landingButton}
      {demoButton}
    </div>
  ) : null;

  const navigate = (next: typeof view) => {
    if (isLoading) return;
    if (view === 'gc' || next === 'gc') setPassword('');
    setShowPassword(false);
    setError(''); setFieldErrors({});
    setView(next);
  };
  const registrationBack = () => {
    setError(''); setFieldErrors({});
    if (registerStep > 1) setRegisterStep((step) => step - 1);
    else navigate('welcome');
  };
  const selectedSchool = SCHOOLS.find((item) => item.id === school);
  const schoolName = selectedSchool?.name || '';
  const errorMessage = error && (
    <p className="auth-live-error" role="alert" aria-live="assertive">
      {error}
    </p>
  );
  const providers = (
    <>
      {(SHOW_GOOGLE_SIGN_IN || SHOW_APPLE_SIGN_IN) && (
        <div className="auth-live-divider">or</div>
      )}
      {SHOW_GOOGLE_SIGN_IN && (
        <button
          type="button"
          onClick={handleGoogleSignIn}
          disabled={isLoading}
          className="auth-live-secondary auth-live-provider"
        >
          <GoogleIcon />
          Continue with Google
        </button>
      )}
      {SHOW_APPLE_SIGN_IN && (
        <button
          type="button"
          onClick={handleAppleSignIn}
          disabled={isLoading}
          className="auth-live-secondary auth-live-provider auth-live-apple"
        >
          <AppleIcon />
          Continue with Apple
        </button>
      )}
    </>
  );
  const passwordField = (id: string, creating = false) => (
    <div className="auth-live-field">
      <label htmlFor={id}>Password</label>
      <div className="auth-live-password">
        <input
          id={id}
          {...fieldValidation(id)}
          type={showPassword ? 'text' : 'password'}
          value={password}
          onChange={(event) => {
            setPassword(event.target.value);
            setError(''); setFieldErrors({});
          }}
          placeholder={creating ? 'Create a password' : 'Your password'}
          autoComplete={creating ? 'new-password' : 'current-password'}
          autoCapitalize="off"
          autoCorrect="off"
          spellCheck={false}
          minLength={creating ? MIN_PASSWORD_LENGTH : undefined}
          maxLength={creating ? MAX_PASSWORD_LENGTH : undefined}
          aria-describedby={[creating && 'account-password-rule', fieldErrors[id] && `${id}-error`].filter(Boolean).join(' ') || undefined}
        />
        <button
          type="button"
          onClick={() => setShowPassword((value) => !value)}
          aria-label={showPassword ? 'Hide password' : 'Show password'}
          aria-pressed={showPassword}
        >
          {showPassword ? (
            <EyeOff size={17} aria-hidden="true" />
          ) : (
            <Eye size={17} aria-hidden="true" />
          )}
        </button>
      </div>
      {fieldMessage(id)}
      {creating && (
        <small
          id="account-password-rule"
          className="auth-live-password-rule"
          data-valid={password.length >= MIN_PASSWORD_LENGTH}
        >
          {password.length >= MIN_PASSWORD_LENGTH && (
            <Check size={13} aria-hidden="true" />
          )}
          At least {MIN_PASSWORD_LENGTH} characters. Try a memorable phrase.
        </small>
      )}
    </div>
  );
  const emailField = (id: string, signingIn = false) => (
    <div className="auth-live-field">
      <label htmlFor={id}>Email</label>
      <input
        id={id}
        {...fieldValidation(id)}
        type={signingIn ? 'text' : 'email'}
        inputMode="email"
        autoComplete={signingIn ? 'username' : 'email'}
        autoCapitalize="off"
        autoCorrect="off"
        spellCheck={false}
        value={email}
        placeholder="you@example.com"
        onChange={(event) => {
          setEmail(event.target.value);
          setError(''); setFieldErrors({});
        }}
      />
      {fieldMessage(id)}
    </div>
  );
  const focusHeading = (definition: string) => {
    if (definition === 'center') {
      const invalidField = document.getElementById(Object.keys(fieldErrors)[0] || '');
      (invalidField || characterHeadingRef.current)?.focus({ preventScroll: true });
    }
  };
  const stepTitles = [
    'Let’s start with you.',
    'Find your people.',
    'Keep it yours.',
    'Meet your study self.',
  ];
  const stepDescriptions = [
    'Your name, your email. Then we’ll make it yours.',
    'Connect your account to your school.',
    'A password that’s just for you.',
    'Pick the character that feels like you.',
  ];
  const stepLabels = [
    'Your details',
    'Your school',
    'Your password',
    'Your Star Crew',
  ];
  const StepIcon =
    registerStep === 2
      ? GraduationCap
      : registerStep === 3
        ? LockKeyhole
        : UserRound;

  return (
    <AccountCard
      devButton={devButtons}
      view={view}
      registerStep={registerStep}
      avatar={avatar}
      name={name}
      school={schoolName}
      busy={isLoading}
      onAvatarChange={setAvatar}
      onWelcome={() => navigate('welcome')}
      onSchoolAccess={() => navigate(view === 'gc' ? 'login' : 'gc')}
    >
      {(view === 'register' || view === 'login') && (
        <div className="auth-live-switch" aria-label="Account options">
          <button
            type="button"
            aria-pressed={view === 'register'}
            disabled={isLoading}
            onClick={() => navigate('register')}
          >
            Create account
          </button>
          <button
            type="button"
            aria-pressed={view === 'login'}
            disabled={isLoading}
            onClick={() => navigate('login')}
          >
            Log in
          </button>
        </div>
      )}
      <AnimatePresence
        mode="wait"
        initial={false}
        custom={view === 'register' ? stepDirection : viewDirection}
      >
        <MotionDiv
          ref={authViewRef}
          key={view === 'register' ? `register-${registerStep}` : view}
          custom={view === 'register' ? stepDirection : viewDirection}
          variants={slideVariants}
          initial="enter"
          animate="center"
          exit="exit"
          transition={viewTransition}
          onAnimationComplete={focusHeading}
          aria-busy={isLoading}
        >
          {view === 'welcome' && (
            <>
              <div className="auth-live-heading">
                <h1 ref={characterHeadingRef} tabIndex={-1}>
                  Your next step.
                </h1>
                <p>A place for your subjects, your plans and what’s next.</p>
              </div>
              <div className="auth-live-welcome-actions">
                <button
                  type="button"
                  className="auth-live-primary"
                  disabled={isLoading}
                  onClick={() => navigate('register')}
                >
                  Create an account
                  <ArrowRight size={20} aria-hidden="true" />
                </button>
                <button
                  type="button"
                  className="auth-live-secondary"
                  disabled={isLoading}
                  onClick={() => navigate('login')}
                >
                  Log in
                  <ArrowRight size={18} aria-hidden="true" />
                </button>
              </div>
              {providers}
              {errorMessage}
            </>
          )}
          {view === 'register' && (
            <>
              <div className="auth-live-context">
                <span>
                  <StepIcon size={17} aria-hidden="true" />
                </span>
                <span>{stepLabels[registerStep - 1]}</span>
              </div>
              <div className="auth-live-heading">
                <h1 ref={characterHeadingRef} tabIndex={-1}>
                  {stepTitles[registerStep - 1]}
                </h1>
                <p>{stepDescriptions[registerStep - 1]}</p>
              </div>
              {registerStep > 1 && <div className="auth-live-carry">
                {selectedSchool ? <SchoolCrest school={selectedSchool.id} /> :
                  <span className="auth-live-carry-initial" aria-hidden="true">{name.trim().slice(0, 1).toUpperCase()}</span>}
                <span>{name}{registerStep > 2 && schoolName && <small>{schoolName}</small>}</span>
                <Check size={16} aria-hidden="true" />
              </div>}
              <form
                noValidate
                onSubmit={(event) => {
                  event.preventDefault();
                  if (isLoading) return;
                  if (registerStep < 4) handleRegisterNext();
                  else void handleRegisterSubmit();
                }}
              >
                <fieldset
                  className="auth-live-fields"
                  disabled={isLoading}
                  aria-label={stepLabels[registerStep - 1]}
                >
                  {registerStep === 1 && (
                    <>
                      <div className="auth-live-field">
                        <label htmlFor="register-name">Your Name</label>
                        <input
                          id="register-name"
                          {...fieldValidation('register-name')}
                          value={name}
                          onChange={(event) => {
                            setName(event.target.value);
                            setError(''); setFieldErrors({});
                          }}
                          placeholder="First and last name"
                          autoComplete="name"
                        />
                        {fieldMessage('register-name')}
                        {/* Name remains free-form for all naming conventions. */}
                      </div>
                      {emailField('register-email')}
                    </>
                  )}
                  {registerStep === 2 && (
                    <>
                      <div className="auth-live-field">
                        <label htmlFor="register-school">School</label>
                        <AccountSchoolPicker id="register-school" {...fieldValidation('register-school')} value={school} disabled={isLoading} onChange={value => {
                          setSchool(value); setJoinCode(''); setError(''); setFieldErrors({});
                        }} />
                        {fieldMessage('register-school')}
                      </div>
                      <div className="auth-live-field">
                        <label htmlFor="register-join-code">
                          School join code
                        </label>
                        <input
                          id="register-join-code"
                          {...fieldValidation('register-join-code')}
                          value={joinCode}
                          onChange={(event) => {
                            setJoinCode(event.target.value);
                            setError(''); setFieldErrors({});
                          }}
                          placeholder="From your school"
                          autoComplete="off"
                          autoCapitalize="off"
                          autoCorrect="off"
                          spellCheck={false}
                        />
                        {fieldMessage('register-join-code')}
                        <button
                          type="button"
                          className="auth-live-link"
                          onClick={() => setEntryHelp('code')}
                        >
                          Where do I find my join code?
                        </button>
                      </div>
                    </>
                  )}
                  {registerStep === 3 &&
                    passwordField('register-password', true)}
                  {registerStep === 4 && (
                    <div>
                      <AccountCrewPicker value={avatar} disabled={isLoading} onChange={value => { setAvatar(value); setError(''); setFieldErrors({}); }} />
                      <div className="auth-live-consent">
                        <div>
                          <span className="nsu-kobra account-consent-control">
                            <Checkbox id="register-consent" data-account-sound="tap" className="account-consent-box" checked={agreedToTerms} disabled={isLoading}
                              onCheckedChange={checked => { setAgreedToTerms(checked); setError(''); setFieldErrors({}); }}
                              aria-label="I have read the Privacy Notice and agree to the Terms of Use" />
                          </span>
                          <span>
                            I have read the{' '}
                            <button
                              type="button"
                              onClick={() => setLegalDoc('privacy')}
                            >
                              Privacy Notice
                            </button>{' '}
                            and agree to the{' '}
                            <button
                              type="button"
                              onClick={() => setLegalDoc('terms')}
                            >
                              Terms of Use
                            </button>
                            .
                          </span>
                        </div>
                        <p>
                          Your school provides NextStepUni with your parent or
                          guardian’s permission as part of enrolment. The
                          Privacy Notice explains how your information is used.
                        </p>
                      </div>
                    </div>
                  )}
                </fieldset>
                {errorMessage}
                <div className="auth-live-actions">
                  <button
                    type="button"
                    className="auth-live-quiet"
                    disabled={isLoading}
                    data-account-sound="skip"
                    onClick={registrationBack}
                  >
                    <ArrowLeft size={17} aria-hidden="true" />
                    Back
                  </button>
                  <button
                    type="submit"
                    className="auth-live-primary"
                    disabled={
                      isLoading ||
                      (registerStep === 4 && (!avatar || !agreedToTerms))
                    }
                  >
                    {isLoading
                      ? 'Creating your account…'
                      : registerStep === 4
                        ? 'Create my account'
                        : 'Continue'}
                    <ArrowRight size={19} aria-hidden="true" />
                  </button>
                </div>
                {registerStep < 4 && (
                  <p className="auth-live-key-hint" aria-hidden="true">
                    ↵ Press Enter to continue
                  </p>
                )}
              </form>
            </>
          )}
          {view === 'login' && (
            <>
              <div className="auth-live-heading">
                <h1 ref={characterHeadingRef} tabIndex={-1}>
                  Good to see you.
                </h1>
                <p>Your space is right where you left it.</p>
              </div>
              <form
                noValidate
                onSubmit={(event) => {
                  event.preventDefault();
                  void handleLogin();
                }}
              >
                <fieldset className="auth-live-fields" disabled={isLoading}>
                  {emailField('login-email', true)}
                  {passwordField('login-password')}
                  <button
                    type="button"
                    className="auth-live-link auth-live-forgot"
                    onClick={() => {
                      navigate('forgot');
                      setResetSent(false);
                    }}
                  >
                    Forgot password?
                  </button>
                </fieldset>
                {errorMessage}
                <div className="auth-live-actions">
                  <button
                    type="button"
                    className="auth-live-quiet"
                    disabled={isLoading}
                    data-account-sound="skip"
                    onClick={() => navigate('welcome')}
                  >
                    <ArrowLeft size={17} aria-hidden="true" />
                    Back
                  </button>
                  <button
                    type="submit"
                    className="auth-live-primary"
                    disabled={isLoading}
                  >
                    {isLoading ? 'Signing in…' : 'Sign in'}
                    <ArrowRight size={19} aria-hidden="true" />
                  </button>
                </div>
              </form>
              {providers}
            </>
          )}
          {view === 'forgot' && (
            <>
              <div className="auth-live-heading">
                <h1 ref={characterHeadingRef} tabIndex={-1}>
                  {resetSent ? 'Check your inbox.' : 'Let’s get you back in.'}
                </h1>
                <p>
                  {resetSent
                    ? `We sent a reset link to ${email.trim()}.`
                    : 'Enter your email and we’ll send you a reset link.'}
                </p>
              </div>
              {resetSent ? (
                <>
                  <p role="status" className="auth-live-sr">
                    Password reset email sent.
                  </p>
                  <div className="auth-live-welcome-actions">
                    <button
                      type="button"
                      className="auth-live-secondary"
                      disabled={isLoading}
                      onClick={() => {
                        setResetSent(false);
                        setResendCountdown(0);
                        setError(''); setFieldErrors({});
                      }}
                    >
                      Change email address
                    </button>
                    <button
                      type="button"
                      className="auth-live-link"
                      disabled={isLoading}
                      onClick={() => setEntryHelp('reset')}
                    >
                      Still waiting?
                    </button>
                  </div>
                  {errorMessage}
                  <div className="auth-live-actions">
                    <button
                      type="button"
                      className="auth-live-quiet"
                      disabled={isLoading}
                      data-account-sound="skip"
                      onClick={() => navigate('login')}
                    >
                      <ArrowLeft size={17} aria-hidden="true" />
                      Back
                    </button>
                    <button
                      type="button"
                      className="auth-live-primary"
                      disabled={isLoading || resendCountdown > 0}
                      onClick={handleForgotPassword}
                    >
                      {isLoading
                        ? 'Sending…'
                        : resendCountdown > 0
                          ? `Resend in ${resendCountdown}s`
                          : 'Resend email'}
                    </button>
                  </div>
                </>
              ) : (
                <form
                  noValidate
                  onSubmit={(event) => {
                    event.preventDefault();
                    void handleForgotPassword();
                  }}
                >
                  <fieldset className="auth-live-fields" disabled={isLoading}>
                    {emailField('reset-email')}
                  </fieldset>
                  {errorMessage}
                  <div className="auth-live-actions">
                    <button
                      type="button"
                      className="auth-live-quiet"
                      disabled={isLoading}
                      data-account-sound="skip"
                      onClick={() => navigate('login')}
                    >
                      <ArrowLeft size={17} aria-hidden="true" />
                      Back
                    </button>
                    <button
                      type="submit"
                      className="auth-live-primary"
                      disabled={isLoading || resendCountdown > 0}
                    >
                      {isLoading
                        ? 'Sending…'
                        : resendCountdown > 0
                          ? `Resend in ${resendCountdown}s`
                          : 'Send Reset Link'}
                      <ArrowRight size={19} aria-hidden="true" />
                    </button>
                  </div>
                </form>
              )}
            </>
          )}
          {view === 'gc' && (
            <>
              <div className="auth-live-context">
                <span>
                  <GraduationCap size={17} aria-hidden="true" />
                </span>
                <span>School access</span>
              </div>
              <div className="auth-live-heading">
                <h1 ref={characterHeadingRef} tabIndex={-1}>
                  Hello, school team.
                </h1>
                <p>Sign in to your school’s shared workspace.</p>
              </div>
              <form
                noValidate
                onSubmit={(event) => {
                  event.preventDefault();
                  void handleGCLogin();
                }}
              >
                <fieldset className="auth-live-fields" disabled={isLoading}>
                  <div
                    className="auth-live-role"
                    role="group"
                    aria-label="School role"
                  >
                    <label htmlFor="school-role-gc">
                      <input
                        id="school-role-gc"
                        type="radio"
                        name="school-role"
                        value="gc"
                        checked={schoolRole === 'gc'}
                        onChange={() => {
                          setSchoolRole('gc');
                          setError(''); setFieldErrors({});
                          setPassword('');
                        }}
                      />
                      Guidance counsellor
                    </label>
                    <label htmlFor="school-role-staff">
                      <input
                        id="school-role-staff"
                        type="radio"
                        name="school-role"
                        value="staff"
                        checked={schoolRole === 'staff'}
                        onChange={() => {
                          setSchoolRole('staff');
                          setError(''); setFieldErrors({});
                          setPassword('');
                        }}
                      />
                      Staff room
                    </label>
                  </div>
                  <div className="auth-live-field">
                    <label htmlFor="gc-school">School</label>
                    <AccountSchoolPicker id="gc-school" value={gcSchool} disabled={isLoading} onChange={value => { setGcSchool(value); setError(''); setFieldErrors({}); }} />
                  </div>
                  {passwordField('gc-password')}
                </fieldset>
                {errorMessage}
                <div className="auth-live-actions">
                  <button
                    type="button"
                    className="auth-live-quiet"
                    disabled={isLoading}
                    data-account-sound="skip"
                    onClick={() => navigate('welcome')}
                  >
                    <ArrowLeft size={17} aria-hidden="true" />
                    Back
                  </button>
                  <button
                    type="submit"
                    className="auth-live-primary"
                    disabled={isLoading}
                  >
                    {isLoading ? 'Signing in…' : 'Sign in'}
                    <ArrowRight size={19} aria-hidden="true" />
                  </button>
                </div>
              </form>
            </>
          )}
        </MotionDiv>
      </AnimatePresence>
      <LegalModal doc={legalDoc} onClose={() => setLegalDoc(null)} />
      {entryHelp && (
        <div className="auth-live-overlay">
          <div
            ref={entryHelpRef}
            className="auth-live-dialog"
            role="dialog"
            aria-modal="true"
            aria-labelledby="entry-help-title"
          >
            <button
              type="button"
              className="auth-live-dialog-close"
              aria-label="Close help"
              onClick={() => setEntryHelp(null)}
            >
              <X size={19} aria-hidden="true" />
            </button>
            <h2 id="entry-help-title">
              {entryHelp === 'code'
                ? 'Let’s find your code.'
                : 'Still waiting?'}
            </h2>
            {entryHelp === 'code' ? (
              <>
                <p>
                  Ask the teacher or guidance counsellor who introduced
                  NextStepUni. They can confirm your school’s join code.
                </p>
                <p>
                  Check your school’s welcome message, too. Your entered details
                  will stay here while you check.
                </p>
              </>
            ) : (
              <>
                <p>
                  Check your spam or junk folder, then confirm the email address
                  you used for your account.
                </p>
                <p>
                  If you signed in with Apple or Google, go back and use the
                  same sign-in option.
                </p>
                <button
                  type="button"
                  className="auth-live-link"
                  onClick={() => {
                    setEntryHelp(null);
                    setResetSent(false);
                    setResendCountdown(0);
                    setError(''); setFieldErrors({});
                  }}
                >
                  Check email address
                </button>
              </>
            )}
            <button
              type="button"
              className="auth-live-primary"
              onClick={() => setEntryHelp(null)}
            >
              {entryHelp === 'code'
                ? 'Back to your details'
                : 'Back to password recovery'}
            </button>
          </div>
        </div>
      )}
    </AccountCard>
  );
};

export default LoginPage;
