/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo, useEffect, useRef } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionButton, MotionDiv, MotionP } from './Motion';
import { ArrowLeft, Eye, EyeOff, School, GraduationCap, ArrowRight, Check, KeyRound, BarChart3 } from 'lucide-react';
import { Capacitor } from '@capacitor/core';
import { authorizeWithApple } from '../utils/appleAuth';
import app, { auth, db } from '../firebase';
import { shouldReapAccount } from '../utils/registrationRollback';
import { signInWithEmailAndPassword, createUserWithEmailAndPassword, updateProfile, deleteUser, sendPasswordResetEmail, sendEmailVerification, signOut, GoogleAuthProvider, signInWithPopup, signInWithCredential } from 'firebase/auth';
import { doc, getDoc, setDoc } from 'firebase/firestore';
import { getFunctions, httpsCallable } from 'firebase/functions';
import { type SessionUser, getAvatarUrl, AVATAR_SEEDS } from '../utils/authUtils';
import { awaitWriteOrTimeout, saveInBackground } from '../utils/firestoreWrite';
import { logError } from '../utils/logError';
import { trackFunnel } from '../utils/funnel';
import { isReservedEmail, isVerifiedAdminSession } from '../utils/adminIdentity';
import { beginStaffProvisioning, endStaffProvisioning } from '../utils/staffProvisioning';
import { SCHOOLS } from '../schoolData';
import { createDemoStudentSession } from '../data/devStudent';
import { MAX_PASSWORD_LENGTH, MIN_PASSWORD_LENGTH, passwordLengthError } from '../utils/passwordPolicy';
import { LegalModal, type LegalDoc, PRIVACY_POLICY_VERSION, CONSENT_BASIS } from './legal/LegalModal';

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

// ── Shared animation tokens ──
const SPRING_FAST = { type: 'spring' as const, stiffness: 500, damping: 28 };
const SPRING_GENTLE = { type: 'spring' as const, stiffness: 340, damping: 30 };
const SPRING_POP = { type: 'spring' as const, stiffness: 420, damping: 18 };

// Slide-and-fade for view/step transitions. Direction-aware:
// `custom={1}` slides forward (new view enters from right),
// `custom={-1}` slides back (new view enters from left). Pure
// tween easing keeps it crisp — no spring wobble.
const SLIDE_DISTANCE = 56;
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
  staff: 1,
  forgot: 2,
};

const errorAnim = {
  initial: { opacity: 0, y: -6, scale: 0.96 },
  animate: { opacity: 1, y: 0, scale: 1 },
  exit: { opacity: 0, y: -4, scale: 0.96 },
  transition: SPRING_FAST,
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

// ── Gateway panel ──────────────────────────────────────────
// Left half of the auth card. Premium product-entry composition:
// three structural zones (brand strip top / icon centred /
// statement + cycling caption bottom) on a pure white surface.
// The gateway artwork is the visual anchor.
const CYCLING_CAPTIONS = [
  'Personalised study, examiner-grounded.',
  'Built on marking schemes, not memorisation.',
  'Subject-tailored, strategy-led.',
  'Smarter than rote learning.',
  'Where examiner insight meets your routine.',
];

const GatewayPanel = () => {
  const [capIdx, setCapIdx] = useState(0);

  useEffect(() => {
    const id = setInterval(() => {
      setCapIdx(i => (i + 1) % CYCLING_CAPTIONS.length);
    }, 4500);
    return () => clearInterval(id);
  }, []);

  return (
    <div
      className="hidden md:flex md:flex-col w-1/2 relative overflow-hidden"
      style={{
        backgroundColor: '#FFFFFF',
        borderRadius: '16px 0 0 16px',
        padding: '36px 44px',
      }}
    >
      {/* Brand strip */}
      <div className="flex items-center gap-3">
        <p
          className="font-sans"
          style={{
            fontSize: 10,
            fontWeight: 700,
            textTransform: 'uppercase',
            letterSpacing: '0.22em',
            color: '#5a5550',
          }}
        >
          Nextstepuni
        </p>
        <div style={{ flex: 1, height: 1, backgroundColor: 'rgba(26,26,26,0.12)' }} />
      </div>

      {/* Icon emblem + statement — grouped as one centred unit */}
      <div className="flex-1 flex flex-col items-center justify-center text-center">
        <div
          style={{
            position: 'relative',
            marginBottom: 28,
            display: 'inline-flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <img
            src="/icons/gateway.png"
            alt=""
            aria-hidden
            style={{
              width: '100%',
              maxWidth: 300,
              height: 'auto',
              display: 'block',
            }}
          />
        </div>

        <h2
          className="font-serif"
          style={{
            fontSize: 24,
            fontWeight: 600,
            color: '#1a1a1a',
            lineHeight: 1.2,
            letterSpacing: '-0.01em',
            marginBottom: 8,
          }}
        >
          Built around how you learn.
        </h2>
        <div style={{ minHeight: 26 }}>
          <AnimatePresence mode="wait">
            <MotionP
              key={CYCLING_CAPTIONS[capIdx]}
              initial={{ opacity: 0, y: 4 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -4 }}
              transition={{ type: 'spring', stiffness: 340, damping: 30 }}
              className="font-sans"
              style={{
                fontSize: 15,
                color: '#4a4540',
                lineHeight: 1.5,
              }}
            >
              {CYCLING_CAPTIONS[capIdx]}
            </MotionP>
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
};

// ── Card wrapper — split panel on desktop, full-width on mobile ──
const LoginCard: React.FC<{ children: React.ReactNode; devButton?: React.ReactNode }> = ({ children, devButton }) => (
  <div className="min-h-screen flex flex-col items-center justify-center p-4 md:p-8 theme-compat" style={{ backgroundColor: 'var(--surface-canvas)' }}>
    <MotionDiv
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: 'easeOut' }}
      className="w-full max-w-5xl bg-white rounded-2xl overflow-hidden flex"
      style={{ minHeight: 540, boxShadow: '0 2px 8px rgba(0,0,0,0.06), 0 12px 40px rgba(0,0,0,0.04)', border: '1.5px solid rgba(0,0,0,0.25)' }}
    >
      <GatewayPanel />
      <div className="w-full md:w-1/2 flex flex-col justify-center px-8 md:px-14 py-12">
        <div className="w-full max-w-[380px] mx-auto">
          {children}
        </div>
      </div>
    </MotionDiv>
    {devButton}
  </div>
);

interface LoginPageProps {
  handleLoginSuccess: (u: SessionUser) => void;
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
  // ── Top-level mode ──
  const [view, setView] = useState<'welcome' | 'login' | 'register' | 'gc' | 'staff' | 'forgot'>('welcome');
  const [registerStep, setRegisterStep] = useState(1); // 1: email+name+school, 2: password, 3: avatar

  // ── Form state ──
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [school, setSchool] = useState('');
  const [joinCode, setJoinCode] = useState('');
  const [gcSchool, setGcSchool] = useState('');
  const [staffCode, setStaffCode] = useState('');
  const [avatar, setAvatar] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [resetSent, setResetSent] = useState(false);
  const [resendCountdown, setResendCountdown] = useState(0);
  // B4 (audit 2026-06-01): student must accept the Privacy Notice + Terms
  // before an account is created; `legalDoc` controls the reachable policy modal.
  const [agreedToTerms, setAgreedToTerms] = useState(false);
  const [legalDoc, setLegalDoc] = useState<LegalDoc | null>(null);

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

  // Countdown tick for the resend button on the forgot-password success screen.
  useEffect(() => {
    if (resendCountdown <= 0) return;
    const t = setTimeout(() => setResendCountdown(c => c - 1), 1000);
    return () => clearTimeout(t);
  }, [resendCountdown]);

  // Random default avatar for step 3
  const defaultAvatar = useMemo(() => AVATAR_SEEDS[Math.floor(Math.random() * AVATAR_SEEDS.length)], []);

  const resetForm = () => {
    setEmail(''); setPassword(''); setName(''); setSchool(''); setJoinCode('');
    setGcSchool(''); setStaffCode(''); setAvatar(''); setError('');
    setShowPassword(false); setRegisterStep(1); setResetSent(false);
    setResendCountdown(0); setAgreedToTerms(false);
  };

  // ── Login handler ──
  const handleLogin = async () => {
    if (!email.trim() || !password.trim()) { setError('Please enter your email and password.'); return; }
    setIsLoading(true); setError('');
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
    setIsLoading(true); setError('');
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
        const newAvatar = AVATAR_SEEDS[Math.floor(Math.random() * AVATAR_SEEDS.length)];
        await writeUserDoc(setDoc(userRef, { name: newName, avatar: newAvatar, createdAt: new Date().toISOString() }), 'LoginPage.googleCreateUserDoc');
        handleLoginSuccess({
          uid: cred.user.uid,
          name: newName,
          avatar: newAvatar,
          school: '',
          role: 'student',
        });
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
    setIsLoading(true); setError('');
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
        const newAvatar = AVATAR_SEEDS[Math.floor(Math.random() * AVATAR_SEEDS.length)];
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
        handleLoginSuccess({ uid: cred.user.uid, name: newName, avatar: newAvatar, school: '', role: 'student' });
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
    if (!email.trim()) { setError('Please enter your email address.'); return; }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim())) {
      setError('Please enter a valid email address.');
      return;
    }
    setIsLoading(true); setError('');
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

  // ── GC Login handler ──
  const handleGCLogin = async () => {
    if (!gcSchool || !password.trim()) { setError('Please select your school and enter your password.'); return; }
    setIsLoading(true); setError('');
    try {
      await signInWithEmailAndPassword(auth, `gc-${gcSchool}@nextstep.app`, password);
    } catch (err: any) {
      // Surface a more specific message so we know whether the GC account is
      // missing entirely vs. wrong password vs. network issue.
      // Use a single generic message for all credential errors. GC emails are
      // deterministic (gc-{schoolId}@nextstep.app) and the school list is
      // public, so a "no account for this school" vs "wrong password" split
      // would let anyone enumerate which schools have a provisioned GC account
      // to target. (Security review 2026-07-16, MEDIUM — account enumeration.)
      console.error('GC login failed:', err.code, err.message);
      if (err.code === 'auth/network-request-failed') {
        setError('Network error. Check your connection and try again.');
      } else {
        setError('Sign-in failed. Check your school and password, or contact support.');
      }
    }
    setIsLoading(false);
  };

  // ── Staff access handler ──
  // A teacher redeems their school's staff code to gain dashboard access.
  // Signs in an existing account or creates one, then calls the
  // claimStaffAccess Cloud Function, which verifies the code SERVER-SIDE and
  // sets role:'staff' (clients can't self-assign role). See
  // compliance/STAFF_DASHBOARD_PLAN.md.
  const handleStaffAccess = async () => {
    if (!school) { setError('Please select your school.'); return; }
    if (!name.trim()) { setError('Please enter your name.'); return; }
    const normalisedEmail = email.trim().toLowerCase();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(normalisedEmail)) { setError('Please enter a valid email address.'); return; }
    const staffPasswordError = passwordLengthError(password);
    if (staffPasswordError) { setError(staffPasswordError); return; }
    if (!staffCode.trim()) { setError('Please enter your staff access code.'); return; }
    if (isReservedEmail(normalisedEmail)) { setError('This email is reserved.'); return; }
    setIsLoading(true); setError('');
    // Creating the account below signs the teacher in immediately, but they are
    // not known to be staff until claimStaffAccess returns. Hold the app on its
    // loading state for that window so AppRouter cannot mistake them for a
    // student and drop them into student onboarding. See utils/staffProvisioning.
    beginStaffProvisioning();
    try {
      // Sign in if the teacher already has an account; otherwise create one.
      let uid: string;
      try {
        const cred = await signInWithEmailAndPassword(auth, normalisedEmail, password);
        uid = cred.user.uid;
      } catch {
        const cred = await createUserWithEmailAndPassword(auth, normalisedEmail, password);
        uid = cred.user.uid;
        await updateProfile(cred.user, { displayName: name.trim() });
      }
      // Staff access exposes school-wide student records, so the callable
      // requires a verified mailbox. A brand-new Firebase account cannot be
      // verified in the same request: send the link, leave the invitation
      // unconsumed, and end this unprivileged session so AppRouter cannot drop
      // the teacher into student onboarding while they check their email.
      const staffUser = auth.currentUser;
      if (!staffUser) throw new Error('The staff sign-in did not complete.');
      if (staffUser.emailVerified !== true) {
        try {
          await sendEmailVerification(staffUser);
        } finally {
          await signOut(auth).catch(() => {});
        }
        endStaffProvisioning();
        setError('Check your email and verify this address, then return here with the same details and staff code.');
        setIsLoading(false);
        return;
      }
      // Ensure a minimal user doc exists. `role` AND `school` are set
      // server-side by claimStaffAccess (clients can't write either), so the
      // client write carries neither.
      const selectedAvatar = AVATAR_SEEDS[Math.floor(Math.random() * AVATAR_SEEDS.length)];
      await writeUserDoc(setDoc(doc(db, 'users', uid), { name: name.trim(), avatar: selectedAvatar }, { merge: true }), 'LoginPage.staffAccessUserDoc');
      // Redeem the code — server verifies + grants role:'staff' and sets school.
      const claimFn = httpsCallable<{ school: string; code: string }, { success: boolean }>(getFunctions(app), 'claimStaffAccess');
      await claimFn({ school, code: staffCode.trim() });
      await auth.currentUser?.getIdToken(true);
      // Reload so AuthContext re-reads role:'staff' and routes to the Staff
      // Dashboard. The marker is cleared by AppRouter once the staff role is
      // visible, so it survives this reload.
      window.location.reload();
    } catch (err: any) {
      // Provisioning failed, so release the hold — otherwise a teacher who
      // mistyped their code would sit on a spinner instead of seeing why.
      endStaffProvisioning();
      const msg = String(err?.message || '');
      const code = String(err?.code || '');
      if (/staff code is not correct/i.test(msg)) {
        setError('That staff code is not correct. Check with your school.');
      } else if (/No staff access is set up/i.test(msg)) {
        setError("Your school hasn't set up staff access yet. Ask your guidance counsellor to generate a code.");
      } else if (/wrong-password|invalid-credential|invalid-login/.test(code)) {
        setError('That email already has an account, but the password is wrong.');
      } else if (/email-already-in-use/.test(code)) {
        setError('That email already has an account. Enter its password to continue.');
      } else {
        console.error('Staff access failed:', err);
        setError('Could not verify staff access. Try again.');
      }
      setIsLoading(false);
    }
  };

  // ── Register step validation ──
  const validateRegisterStep = (): boolean => {
    if (registerStep === 1) {
      if (!email.trim()) { setError('Please enter your email.'); return false; }
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim())) { setError('Please enter a valid email address.'); return false; }
      const normalised = email.trim().toLowerCase();
      if (isReservedEmail(normalised)) { setError('This email is reserved.'); return false; }
      if (!name.trim()) { setError('Please enter your name.'); return false; }
      if (!school) { setError('Please select your school.'); return false; }
      if (!joinCode.trim()) { setError('Please enter your school join code.'); return false; }
      return true;
    }
    if (registerStep === 2) {
      const passwordError = passwordLengthError(password);
      if (passwordError) { setError(passwordError); return false; }
      return true;
    }
    return true;
  };

  const handleRegisterNext = () => {
    setError('');
    if (!validateRegisterStep()) return;
    if (registerStep < 3) setRegisterStep(s => s + 1);
  };

  // ── Register submit (step 3) ──
  const handleRegisterSubmit = async () => {
    setIsLoading(true); setError('');
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
      const cred = await createUserWithEmailAndPassword(auth, registrationEmail, password);
      createdUser = cred.user;
      await updateProfile(createdUser, { displayName: name.trim() });
      // Send a verification email (fire-and-forget) so the address is provable.
      // Non-blocking: registration still proceeds (security review 2026-07-16,
      // L-5). Deliverability failures must not block sign-up.
      sendEmailVerification(createdUser).catch(err => console.error('Failed to send verification email:', err));
      // Verify the school join code SERVER-SIDE and bind the student to the
      // school (security review H-2). `school` is set by the function, not the
      // client — the /users rules forbid a client-supplied school. A wrong code
      // throws here and the account is rolled back below.
      const joinFn = httpsCallable<{ school: string; code: string }, { success: boolean }>(getFunctions(app), 'claimStudentSchool');
      await joinFn({ school, code: joinCode.trim() });
      await createdUser.getIdToken(true);
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
      await writeUserDoc(
        setDoc(doc(db, 'users', createdUser.uid), userDocPayload, { merge: true }),
        'LoginPage.registerUserDoc',
        retryUserDoc,
      );
      trackFunnel('register_succeeded');
      handleLoginSuccess({
        uid: createdUser.uid,
        name: name.trim(),
        avatar: selectedAvatar,
        school,
        role: 'student',
      });
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
        handleLoginSuccess({
          uid: createdUser.uid,
          name: name.trim(),
          avatar: selectedAvatar,
          school,
          role: 'student',
        });
        setIsLoading(false);
        return;
      }
      // Everything before the write leaves an orphaned auth account (a wrong
      // join code is the common one). Reaping it is right: it lets the student
      // retry with the same email instead of hitting email-already-in-use.
      if (shouldReapAccount({ hasAccount: !!createdUser, userDocStarted })) {
        try { await deleteUser(createdUser); } catch (rollbackErr) {
          console.error('Failed to clean up auth account after registration failure:', rollbackErr);
        }
      }
      const msg = String(err?.message || '');
      if (err.code === 'auth/weak-password') {
        setError(`Password must be at least ${MIN_PASSWORD_LENGTH} characters.`);
        setRegisterStep(2);
      } else if (err.code === 'auth/email-already-in-use') {
        setError('An account with this email already exists. Try signing in instead.');
        setRegisterStep(1);
      } else if (err.code === 'auth/invalid-email') {
        setError('Please enter a valid email address.');
        setRegisterStep(1);
      } else if (/join code is not correct/i.test(msg)) {
        setError('That school join code is not correct. Check the code from your school.');
        setRegisterStep(1);
      } else if (/Too many attempts/i.test(msg)) {
        setError('Too many attempts. Please wait a few minutes and try again.');
        setRegisterStep(1);
      } else {
        setError('Registration failed. Try again.');
      }
    }
    setIsLoading(false);
  };

  // ── Shared styles ──
  const inputClass = "w-full py-3.5 px-4 rounded-xl text-sm font-sans text-zinc-800 placeholder-zinc-400 outline-none transition-all bg-white border-2 border-zinc-200 focus:border-[#F26B1F]";
  // Password inputs need extra right padding so the show/hide eye toggle and
  // iOS's own AutoFill / Strong-Password key icon don't visually collide
  // inside the field.
  const passwordInputClass = `${inputClass} pr-12`;
  const primaryBtn = "w-full py-3.5 rounded-xl text-[15px] font-semibold transition-all border-2 disabled:opacity-50 disabled:cursor-not-allowed";
  const primaryBtnStyle = { backgroundColor: 'var(--cta-invert-bg)', color: 'var(--cta-invert-ink)', borderColor: 'var(--cta-invert-border)' };

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

  const selectedAvatar = avatar || defaultAvatar;

  // ═══════════════════════════════════════════════════════════
  // Single LoginCard with view-level AnimatePresence so navigating
  // between Welcome / Login / GC / Forgot / Register actually
  // animates — was an instant render before.
  // ═══════════════════════════════════════════════════════════
  return (
    <LoginCard devButton={demoButton}>
      <AnimatePresence mode="wait" initial={false} custom={viewDirection}>
        <MotionDiv
          key={view}
          custom={viewDirection}
          variants={slideVariants}
          initial="enter"
          animate="center"
          exit="exit"
          transition={slideTransition}
        >
          {/* ── WELCOME ────────────────────────────────────── */}
          {view === 'welcome' && (
            <div className="text-center">
              <p className="text-[10px] font-bold uppercase tracking-[0.2em] mb-6" style={{ color: '#9e9186' }}>LOG-IN</p>
              <h1 className="text-3xl md:text-4xl font-semibold tracking-tight mb-3" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>
                Your study,<br />your way.
              </h1>
              <p className="text-sm mb-10" style={{ fontFamily: "'DM Sans', sans-serif", color: '#7a7068' }}>
                Science-backed study strategies personalised to your subjects, your goals, and your exam.
              </p>

              <div className="space-y-3">
                <MotionButton
                  whileHover={btnHover} whileTap={btnTap} transition={SPRING_FAST}
                  onClick={() => { resetForm(); setView('register'); }}
                  className={primaryBtn}
                  style={primaryBtnStyle}
                >
                  Get Started
                </MotionButton>
                <MotionButton
                  whileHover={btnHover} whileTap={btnTap} transition={SPRING_FAST}
                  onClick={() => { resetForm(); setView('login'); }}
                  className="w-full py-3.5 rounded-xl text-[15px] font-semibold transition-all border-2"
                  style={{ color: '#F26B1F', borderColor: 'rgba(242,107,31,0.3)', backgroundColor: 'white' }}
                >
                  I already have an account
                </MotionButton>
                {SHOW_GOOGLE_SIGN_IN && (
                  <MotionButton
                    whileHover={btnHover} whileTap={btnTap} transition={SPRING_FAST}
                    onClick={handleGoogleSignIn}
                    disabled={isLoading}
                    className="w-full py-3.5 rounded-xl text-[15px] font-semibold transition-all border-2 flex items-center justify-center gap-2.5 disabled:opacity-50 disabled:cursor-not-allowed"
                    style={{ color: '#1a1a1a', borderColor: '#d0cdc8', backgroundColor: 'white' }}
                  >
                    <GoogleIcon />
                    Continue with Google
                  </MotionButton>
                )}
                {SHOW_APPLE_SIGN_IN && (
                  <MotionButton
                    whileHover={btnHover} whileTap={btnTap} transition={SPRING_FAST}
                    onClick={handleAppleSignIn}
                    disabled={isLoading}
                    className="w-full py-3.5 rounded-xl text-[15px] font-semibold transition-all flex items-center justify-center gap-2.5 disabled:opacity-50 disabled:cursor-not-allowed"
                    style={{ color: '#FFFFFF', backgroundColor: '#000000' }}
                  >
                    <AppleIcon />
                    Continue with Apple
                  </MotionButton>
                )}
              </div>

              <div className="flex items-center gap-4 mt-8">
                <div className="flex-1 h-px" style={{ backgroundColor: '#d0cdc8' }} />
                <span className="text-[11px] font-medium" style={{ color: '#9e9186' }}>OR</span>
                <div className="flex-1 h-px" style={{ backgroundColor: '#d0cdc8' }} />
              </div>
              <button
                onClick={() => { resetForm(); setView('gc'); }}
                className="w-full py-3 rounded-xl text-sm font-medium transition-all flex items-center justify-center gap-2 mt-4 border-2"
                style={{ color: '#7a7068', borderColor: '#d0cdc8', backgroundColor: 'white' }}
              >
                <GraduationCap size={16} /> Sign in as Guidance Counsellor
              </button>
              <button
                onClick={() => { resetForm(); setView('staff'); }}
                className="w-full py-3 rounded-xl text-sm font-medium transition-all flex items-center justify-center gap-2 mt-3 border-2"
                style={{ color: '#7a7068', borderColor: '#d0cdc8', backgroundColor: 'white' }}
              >
                <KeyRound size={16} /> Teacher / staff access
              </button>
            </div>
          )}

          {/* ── LOGIN ──────────────────────────────────────── */}
          {view === 'login' && (
            <>
              <button type="button" onClick={() => setView('welcome')} className="flex items-center gap-1.5 text-sm font-medium mb-6 transition-colors" style={{ color: '#9e9186' }}>
                <ArrowLeft size={14} /> Back
              </button>
              <h2 className="text-2xl font-semibold tracking-tight mb-1" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>Welcome back</h2>
              <p className="text-sm mb-8" style={{ color: '#7a7068' }}>Sign in with your email and password.</p>
              <form onSubmit={e => { e.preventDefault(); handleLogin(); }} className="space-y-4">
                <div>
                  <label htmlFor="login-email" className="text-xs font-bold uppercase tracking-wider mb-1.5 block" style={{ color: '#9e9186' }}>Email</label>
                  <input id="login-email" type="email" value={email} onChange={e => { setEmail(e.target.value); setError(''); }} placeholder="you@example.com" className={inputClass} autoFocus autoComplete="email" autoCapitalize="off" autoCorrect="off" inputMode="email" spellCheck={false} />
                </div>
                <div>
                  <div className="flex items-center justify-between mb-1.5">
                    <label htmlFor="login-password" className="text-xs font-bold uppercase tracking-wider" style={{ color: '#9e9186' }}>Password</label>
                    <button type="button" onClick={() => { setView('forgot'); setError(''); }} className="text-xs font-semibold transition-colors hover:opacity-80" style={{ color: '#F26B1F' }}>Forgot?</button>
                  </div>
                  <div className="relative">
                    <input id="login-password" type={showPassword ? 'text' : 'password'} value={password} onChange={e => { setPassword(e.target.value); setError(''); }} placeholder="Enter your password" className={passwordInputClass} autoComplete="current-password" autoCapitalize="off" autoCorrect="off" spellCheck={false} />
                    <button type="button" onClick={() => setShowPassword(!showPassword)} aria-label={showPassword ? 'Hide password' : 'Show password'} aria-pressed={showPassword} className="absolute right-3 top-1/2 -translate-y-1/2 transition-colors" style={{ color: '#9e9186' }}>
                      {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                    </button>
                  </div>
                </div>
                <AnimatePresence>{error && <MotionDiv {...errorAnim} role="alert" aria-live="assertive" className="text-sm text-red-500 font-medium">{error}</MotionDiv>}</AnimatePresence>
                <MotionButton type="submit" disabled={isLoading} whileHover={btnHover} whileTap={btnTap} transition={SPRING_FAST} className={primaryBtn} style={primaryBtnStyle}>
                  {isLoading ? 'Signing in...' : 'Sign In'}
                </MotionButton>
              </form>
              {SHOW_GOOGLE_SIGN_IN && (
                <>
                  <div className="flex items-center gap-4 my-5">
                    <div className="flex-1 h-px" style={{ backgroundColor: '#d0cdc8' }} />
                    <span className="text-[11px] font-medium" style={{ color: '#9e9186' }}>OR</span>
                    <div className="flex-1 h-px" style={{ backgroundColor: '#d0cdc8' }} />
                  </div>
                  <MotionButton
                    whileHover={btnHover} whileTap={btnTap} transition={SPRING_FAST}
                    onClick={handleGoogleSignIn}
                    disabled={isLoading}
                    className="w-full py-3.5 rounded-xl text-[15px] font-semibold transition-all border-2 flex items-center justify-center gap-2.5 disabled:opacity-50 disabled:cursor-not-allowed"
                    style={{ color: '#1a1a1a', borderColor: '#d0cdc8', backgroundColor: 'white' }}
                  >
                    <GoogleIcon />
                    Continue with Google
                  </MotionButton>
                </>
              )}
              {SHOW_APPLE_SIGN_IN && (
                <>
                  <div className="flex items-center gap-4 my-5">
                    <div className="flex-1 h-px" style={{ backgroundColor: '#d0cdc8' }} />
                    <span className="text-[11px] font-medium" style={{ color: '#9e9186' }}>OR</span>
                    <div className="flex-1 h-px" style={{ backgroundColor: '#d0cdc8' }} />
                  </div>
                  <MotionButton
                    whileHover={btnHover} whileTap={btnTap} transition={SPRING_FAST}
                    onClick={handleAppleSignIn}
                    disabled={isLoading}
                    className="w-full py-3.5 rounded-xl text-[15px] font-semibold transition-all flex items-center justify-center gap-2.5 disabled:opacity-50 disabled:cursor-not-allowed"
                    style={{ color: '#FFFFFF', backgroundColor: '#000000' }}
                  >
                    <AppleIcon />
                    Continue with Apple
                  </MotionButton>
                </>
              )}
              <p className="text-sm text-center mt-6" style={{ color: '#9e9186' }}>
                Don&apos;t have an account?{' '}<button type="button" onClick={() => { resetForm(); setView('register'); }} className="font-semibold transition-colors hover:opacity-80" style={{ color: '#F26B1F' }}>Register</button>
              </p>
            </>
          )}

          {/* ── GC LOGIN ───────────────────────────────────── */}
          {view === 'gc' && (
            <>
              <button type="button" onClick={() => setView('welcome')} className="flex items-center gap-1.5 text-sm font-medium mb-6 transition-colors" style={{ color: '#9e9186' }}>
                <ArrowLeft size={14} /> Back
              </button>
              <h2 className="text-2xl font-semibold tracking-tight mb-1" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>Guidance Counsellor</h2>
              <p className="text-sm mb-8" style={{ color: '#7a7068' }}>Select your school and enter your password.</p>
              <form onSubmit={e => { e.preventDefault(); handleGCLogin(); }} className="space-y-4">
                <div>
                  <label htmlFor="gc-school" className="text-xs font-bold uppercase tracking-wider mb-1.5 block" style={{ color: '#9e9186' }}>School</label>
                  <div className="relative">
                    <select id="gc-school" value={gcSchool} onChange={e => { setGcSchool(e.target.value); setError(''); }} className={`${inputClass} appearance-none cursor-pointer ${!gcSchool ? 'text-zinc-400' : ''}`} autoFocus>
                      <option value="" disabled>Select your school</option>
                      {SCHOOLS.map(s => (<option key={s.id} value={s.id}>{s.name}</option>))}
                    </select>
                    <School size={16} className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none" style={{ color: '#9e9186' }} />
                  </div>
                </div>
                <div>
                  <label htmlFor="gc-password" className="text-xs font-bold uppercase tracking-wider mb-1.5 block" style={{ color: '#9e9186' }}>Password</label>
                  <div className="relative">
                    <input id="gc-password" type={showPassword ? 'text' : 'password'} value={password} onChange={e => { setPassword(e.target.value); setError(''); }} placeholder="Enter your password" className={passwordInputClass} autoComplete="current-password" autoCapitalize="off" autoCorrect="off" spellCheck={false} />
                    <button type="button" onClick={() => setShowPassword(!showPassword)} aria-label={showPassword ? 'Hide password' : 'Show password'} aria-pressed={showPassword} className="absolute right-3 top-1/2 -translate-y-1/2 transition-colors" style={{ color: '#9e9186' }}>
                      {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                    </button>
                  </div>
                </div>
                <AnimatePresence>{error && <MotionDiv {...errorAnim} role="alert" aria-live="assertive" className="text-sm text-red-500 font-medium">{error}</MotionDiv>}</AnimatePresence>
                <MotionButton type="submit" disabled={isLoading} whileHover={btnHover} whileTap={btnTap} transition={SPRING_FAST} className={primaryBtn} style={primaryBtnStyle}>
                  {isLoading ? 'Signing in...' : 'Sign In'}
                </MotionButton>
              </form>
            </>
          )}

          {/* ── STAFF / TEACHER ACCESS ──────────────────────── */}
          {view === 'staff' && (
            <>
              <button type="button" onClick={() => setView('welcome')} className="flex items-center gap-1.5 text-sm font-medium mb-6 transition-colors" style={{ color: '#9e9186' }}>
                <ArrowLeft size={14} /> Back
              </button>
              <h2 className="text-2xl font-semibold tracking-tight mb-1" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>Teacher / staff access</h2>
              <p className="text-sm mb-6" style={{ color: '#7a7068' }}>Enter your details and the staff access code from your school. New to NextStepUni? This creates your staff account. Already have an account? Use the same email and password.</p>
              <form onSubmit={e => { e.preventDefault(); handleStaffAccess(); }} className="space-y-4">
                <div>
                  <label htmlFor="staff-name" className="text-xs font-bold uppercase tracking-wider mb-1.5 block" style={{ color: '#9e9186' }}>Your name</label>
                  <input id="staff-name" type="text" value={name} onChange={e => { setName(e.target.value); setError(''); }} placeholder="Jane Murphy" className={inputClass} autoFocus autoComplete="name" />
                </div>
                <div>
                  <label htmlFor="staff-school" className="text-xs font-bold uppercase tracking-wider mb-1.5 block" style={{ color: '#9e9186' }}>School</label>
                  <div className="relative">
                    <select id="staff-school" value={school} onChange={e => { setSchool(e.target.value); setError(''); }} className={`${inputClass} appearance-none cursor-pointer ${!school ? 'text-zinc-400' : ''}`}>
                      <option value="" disabled>Select your school</option>
                      {SCHOOLS.map(s => (<option key={s.id} value={s.id}>{s.name}</option>))}
                    </select>
                    <School size={16} className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none" style={{ color: '#9e9186' }} />
                  </div>
                </div>
                <div>
                  <label htmlFor="staff-email" className="text-xs font-bold uppercase tracking-wider mb-1.5 block" style={{ color: '#9e9186' }}>Email</label>
                  <input id="staff-email" type="email" value={email} onChange={e => { setEmail(e.target.value); setError(''); }} placeholder="you@school.ie" className={inputClass} autoComplete="email" autoCapitalize="off" autoCorrect="off" inputMode="email" spellCheck={false} />
                </div>
                <div>
                  <label htmlFor="staff-password" className="text-xs font-bold uppercase tracking-wider mb-1.5 block" style={{ color: '#9e9186' }}>Password</label>
                  <div className="relative">
                    <input id="staff-password" type={showPassword ? 'text' : 'password'} value={password} onChange={e => { setPassword(e.target.value); setError(''); }} placeholder={`At least ${MIN_PASSWORD_LENGTH} characters`} minLength={MIN_PASSWORD_LENGTH} maxLength={MAX_PASSWORD_LENGTH} className={passwordInputClass} autoComplete="current-password" autoCapitalize="off" autoCorrect="off" spellCheck={false} />
                    <button type="button" onClick={() => setShowPassword(!showPassword)} aria-label={showPassword ? 'Hide password' : 'Show password'} aria-pressed={showPassword} className="absolute right-3 top-1/2 -translate-y-1/2 transition-colors" style={{ color: '#9e9186' }}>
                      {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                    </button>
                  </div>
                </div>
                <div>
                  <label htmlFor="staff-code" className="text-xs font-bold uppercase tracking-wider mb-1.5 block" style={{ color: '#9e9186' }}>Staff access code</label>
                  <div className="relative">
                    <input id="staff-code" type="text" value={staffCode} onChange={e => { setStaffCode(e.target.value); setError(''); }} placeholder="Code from your school" className={`${inputClass} pr-10`} autoCapitalize="characters" autoCorrect="off" spellCheck={false} />
                    <KeyRound size={16} className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none" style={{ color: '#9e9186' }} />
                  </div>
                </div>
                <AnimatePresence>{error && <MotionDiv {...errorAnim} role="alert" aria-live="assertive" className="text-sm text-red-500 font-medium">{error}</MotionDiv>}</AnimatePresence>
                <MotionButton type="submit" disabled={isLoading} whileHover={btnHover} whileTap={btnTap} transition={SPRING_FAST} className={primaryBtn} style={primaryBtnStyle}>
                  {isLoading ? 'Verifying...' : 'Get staff access'}
                </MotionButton>
              </form>
            </>
          )}

          {/* ── FORGOT PASSWORD ─────────────────────────────── */}
          {view === 'forgot' && (
            <>
              <button type="button" onClick={() => { setView('login'); setError(''); setResetSent(false); }} className="flex items-center gap-1.5 text-sm font-medium mb-6 transition-colors" style={{ color: '#9e9186' }}>
                <ArrowLeft size={14} /> Back to sign in
              </button>
              <h2 className="text-2xl font-semibold tracking-tight mb-1" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>Reset your password</h2>
              <p className="text-sm mb-8" style={{ color: '#7a7068' }}>Enter your email and we&apos;ll send you a link to reset your password.</p>
              {resetSent ? (
                <MotionDiv
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ ...SPRING_GENTLE, staggerChildren: 0.08, delayChildren: 0.05 }}
                  className="text-center py-2"
                >
                  <MotionDiv
                    initial={{ scale: 0, rotate: -8 }}
                    animate={{ scale: 1, rotate: 0 }}
                    transition={SPRING_POP}
                    className="w-12 h-12 mx-auto mb-4 rounded-full flex items-center justify-center"
                    style={{ backgroundColor: '#FDEEDF' }}
                  >
                    <Check size={24} style={{ color: '#F26B1F' }} />
                  </MotionDiv>
                  <MotionDiv initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} transition={SPRING_GENTLE}>
                    <p className="text-sm font-medium mb-1" style={{ color: '#1a1a1a' }}>Check your inbox</p>
                    <p className="text-sm mb-2" style={{ color: '#7a7068' }}>We&apos;ve sent a password reset link to <span className="font-medium" style={{ color: '#1a1a1a' }}>{email}</span></p>
                    <p className="text-xs mb-6" style={{ color: '#9e9186' }}>Can&apos;t find it? Check your spam folder.</p>
                  </MotionDiv>

                  <MotionDiv initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} transition={SPRING_GENTLE} className="space-y-2.5">
                    <MotionButton
                      onClick={() => { resetForm(); setView('login'); }}
                      whileHover={btnHover}
                      whileTap={btnTap}
                      transition={SPRING_FAST}
                      className={primaryBtn}
                      style={primaryBtnStyle}
                    >
                      Back to sign in
                    </MotionButton>
                    <MotionButton
                      onClick={handleForgotPassword}
                      disabled={resendCountdown > 0 || isLoading}
                      whileHover={resendCountdown > 0 ? {} : btnHover}
                      whileTap={resendCountdown > 0 ? {} : btnTap}
                      transition={SPRING_FAST}
                      className="w-full py-3 rounded-xl text-[14px] font-medium transition-all border-2 disabled:opacity-50 disabled:cursor-not-allowed"
                      style={{ color: '#F26B1F', borderColor: 'rgba(242,107,31,0.3)', backgroundColor: 'white' }}
                    >
                      {resendCountdown > 0
                        ? `Resend in ${resendCountdown}s`
                        : isLoading
                        ? 'Sending…'
                        : 'Resend email'}
                    </MotionButton>
                  </MotionDiv>
                </MotionDiv>
              ) : (
                <form onSubmit={e => { e.preventDefault(); handleForgotPassword(); }} className="space-y-4">
                  <div>
                    <label htmlFor="reset-email" className="text-xs font-bold uppercase tracking-wider mb-1.5 block" style={{ color: '#9e9186' }}>Email</label>
                    <input id="reset-email" type="email" value={email} onChange={e => { setEmail(e.target.value); setError(''); }} placeholder="you@example.com" className={inputClass} autoFocus autoComplete="email" autoCapitalize="off" autoCorrect="off" inputMode="email" spellCheck={false} />
                  </div>
                <AnimatePresence>{error && <MotionDiv {...errorAnim} role="alert" aria-live="assertive" className="text-sm text-red-500 font-medium">{error}</MotionDiv>}</AnimatePresence>
                  <MotionButton type="submit" disabled={isLoading} whileHover={btnHover} whileTap={btnTap} transition={SPRING_FAST} className={primaryBtn} style={primaryBtnStyle}>
                    {isLoading ? 'Sending...' : 'Send Reset Link'}
                  </MotionButton>
                </form>
              )}
            </>
          )}

          {/* ── REGISTER (multi-step) ───────────────────────── */}
          {view === 'register' && (
            <>
              <div className="flex items-center justify-between mb-6">
                <button type="button" onClick={() => {
                  if (registerStep > 1) { setRegisterStep(s => s - 1); setError(''); }
                  else setView('welcome');
                }} className="flex items-center gap-1.5 text-sm font-medium transition-colors" style={{ color: '#9e9186' }}>
                  <ArrowLeft size={14} /> Back
                </button>
                <div className="flex items-center gap-1.5">
                  {[1, 2, 3].map(s => (
                    <MotionDiv
                      key={s}
                      className="h-1.5 rounded-full"
                      animate={{
                        width: s === registerStep ? 24 : 8,
                        backgroundColor: s <= registerStep ? '#F26B1F' : '#d0cdc8',
                      }}
                      transition={SPRING_GENTLE}
                    />
                  ))}
                </div>
              </div>

              <AnimatePresence mode="wait" initial={false} custom={stepDirection}>
                {registerStep === 1 && (
                  <MotionDiv key="step1" custom={stepDirection} variants={slideVariants} initial="enter" animate="center" exit="exit" transition={slideTransition}>
                    <h2 className="text-2xl font-semibold tracking-tight mb-1" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>Let&apos;s get you set up</h2>
                    <p className="text-sm mb-8" style={{ color: '#7a7068' }}>We&apos;ll use your email to create your account and for password resets.</p>
                    <form onSubmit={e => { e.preventDefault(); handleRegisterNext(); }} className="space-y-4">
                      <div>
                        <label htmlFor="register-email" className="text-xs font-bold uppercase tracking-wider mb-1.5 block" style={{ color: '#9e9186' }}>Email</label>
                        <input id="register-email" type="email" value={email} onChange={e => { setEmail(e.target.value); setError(''); }} placeholder="you@example.com" className={inputClass} autoFocus autoComplete="email" autoCapitalize="off" autoCorrect="off" inputMode="email" spellCheck={false} />
                      </div>
                      <div>
                        <label htmlFor="register-name" className="text-xs font-bold uppercase tracking-wider mb-1.5 block" style={{ color: '#9e9186' }}>Your Name</label>
                        <input id="register-name" type="text" value={name} onChange={e => { setName(e.target.value); setError(''); }} placeholder="e.g. Sean, Emma, Jordan" className={inputClass} autoComplete="given-name" autoCapitalize="words" autoCorrect="off" spellCheck={false} />
                      </div>
                      <div>
                        <label htmlFor="register-school" className="text-xs font-bold uppercase tracking-wider mb-1.5 block" style={{ color: '#9e9186' }}>School</label>
                        <div className="relative">
                          <select id="register-school" value={school} onChange={e => { setSchool(e.target.value); setError(''); }} className={`${inputClass} appearance-none cursor-pointer ${!school ? 'text-zinc-400' : ''}`}>
                            <option value="" disabled>Select your school</option>
                            {SCHOOLS.map(s => (<option key={s.id} value={s.id}>{s.name}</option>))}
                          </select>
                          <School size={16} className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none" style={{ color: '#9e9186' }} />
                        </div>
                      </div>
                      <div>
                        <label htmlFor="register-join-code" className="text-xs font-bold uppercase tracking-wider mb-1.5 block" style={{ color: '#9e9186' }}>School join code</label>
                        <div className="relative">
                          <input id="register-join-code" type="text" value={joinCode} onChange={e => { setJoinCode(e.target.value); setError(''); }} placeholder="From your school" className={`${inputClass} pr-10`} autoComplete="off" autoCapitalize="off" autoCorrect="off" spellCheck={false} />
                          <KeyRound size={16} className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none" style={{ color: '#9e9186' }} />
                        </div>
                        <p className="text-xs mt-1.5" style={{ color: '#9e9186' }}>Your school gives you this code. It confirms you belong to your school.</p>
                      </div>
                      <AnimatePresence>{error && <MotionDiv {...errorAnim} role="alert" aria-live="assertive" className="text-sm text-red-500 font-medium">{error}</MotionDiv>}</AnimatePresence>
                      <MotionButton type="submit" whileHover={btnHover} whileTap={btnTap} transition={SPRING_FAST} className={primaryBtn} style={primaryBtnStyle}>
                        <span className="flex items-center justify-center gap-2">Continue <ArrowRight size={16} /></span>
                      </MotionButton>
                    </form>
                    <p className="text-sm text-center mt-6" style={{ color: '#9e9186' }}>
                      Already have an account?{' '}<button type="button" onClick={() => { resetForm(); setView('login'); }} className="font-semibold transition-colors hover:opacity-80" style={{ color: '#F26B1F' }}>Sign in</button>
                    </p>
                  </MotionDiv>
                )}

                {registerStep === 2 && (
                  <MotionDiv key="step2" custom={stepDirection} variants={slideVariants} initial="enter" animate="center" exit="exit" transition={slideTransition}>
                    <h2 className="text-2xl font-semibold tracking-tight mb-1" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>Create a password</h2>
                    <p className="text-sm mb-8" style={{ color: '#7a7068' }}>Use at least {MIN_PASSWORD_LENGTH} characters. A short phrase is easier to remember and harder to guess.</p>
                    <form onSubmit={e => { e.preventDefault(); handleRegisterNext(); }} className="space-y-4">
                      <div>
                        <label htmlFor="register-password" className="text-xs font-bold uppercase tracking-wider mb-1.5 block" style={{ color: '#9e9186' }}>Password</label>
                        <div className="relative">
                          <input id="register-password" type={showPassword ? 'text' : 'password'} value={password} onChange={e => { setPassword(e.target.value); setError(''); }} placeholder="Create a password" minLength={MIN_PASSWORD_LENGTH} maxLength={MAX_PASSWORD_LENGTH} className={passwordInputClass} autoFocus autoComplete="new-password" autoCapitalize="off" autoCorrect="off" spellCheck={false} />
                          <button type="button" onClick={() => setShowPassword(!showPassword)} aria-label={showPassword ? 'Hide password' : 'Show password'} aria-pressed={showPassword} className="absolute right-3 top-1/2 -translate-y-1/2 transition-colors" style={{ color: '#9e9186' }}>
                            {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                          </button>
                        </div>
                        {password.length > 0 && password.length < MIN_PASSWORD_LENGTH && (
                          <p className="text-xs mt-1.5" style={{ color: '#9e9186' }}>{MIN_PASSWORD_LENGTH - password.length} more character{MIN_PASSWORD_LENGTH - password.length !== 1 ? 's' : ''} needed</p>
                        )}
                        {password.length >= MIN_PASSWORD_LENGTH && password.length <= MAX_PASSWORD_LENGTH && (
                          <p className="text-xs mt-1.5 flex items-center gap-1" style={{ color: '#F26B1F' }}><Check size={12} /> Looks good</p>
                        )}
                      </div>
                      <AnimatePresence>{error && <MotionDiv {...errorAnim} role="alert" aria-live="assertive" className="text-sm text-red-500 font-medium">{error}</MotionDiv>}</AnimatePresence>
                      <MotionButton type="submit" whileHover={btnHover} whileTap={btnTap} transition={SPRING_FAST} className={primaryBtn} style={primaryBtnStyle}>
                        <span className="flex items-center justify-center gap-2">Continue <ArrowRight size={16} /></span>
                      </MotionButton>
                    </form>
                  </MotionDiv>
                )}

                {registerStep === 3 && (
                  <MotionDiv key="step3" custom={stepDirection} variants={slideVariants} initial="enter" animate="center" exit="exit" transition={slideTransition}>
                    <h2 className="text-2xl font-semibold tracking-tight mb-1" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>Choose your avatar</h2>
                    <p className="text-sm mb-6" style={{ color: '#7a7068' }}>Pick one that feels like you. You can change it later.</p>
                    <div className="grid grid-cols-4 gap-3 mb-6">
                      {AVATAR_SEEDS.map(seed => (
                        <button key={seed} type="button" onClick={() => setAvatar(seed)} className={`rounded-xl aspect-square p-1 transition-all ${selectedAvatar === seed ? 'ring-2 ring-offset-2 bg-[#FDEEDF]' : 'hover:ring-1 hover:ring-zinc-300 bg-white'}`} style={selectedAvatar === seed ? { borderColor: '#F26B1F', border: '2px solid #F26B1F' } : { border: '2px solid #d0cdc8' }}>
                          <img src={getAvatarUrl(seed)} alt={seed} className="w-full h-full rounded-lg" />
                        </button>
                      ))}
                    </div>
                    {/* B4 (audit 2026-06-01): privacy/terms acceptance gate */}
                    <div className="mb-4 rounded-xl border-2 p-3.5" style={{ borderColor: '#e5e2dd' }}>
                      <div className="flex items-start gap-2.5">
                        <button
                          type="button"
                          role="checkbox"
                          aria-checked={agreedToTerms}
                          aria-label="I have read the Privacy Notice and agree to the Terms of Use"
                          onClick={() => { setAgreedToTerms(v => !v); setError(''); }}
                          className="mt-0.5 w-5 h-5 rounded-md border-2 flex items-center justify-center shrink-0 transition-colors"
                          style={agreedToTerms ? { backgroundColor: '#F26B1F', borderColor: '#F26B1F' } : { borderColor: '#d0cdc8' }}
                        >
                          {agreedToTerms && <Check size={13} className="text-white" strokeWidth={3} />}
                        </button>
                        <span className="text-[13px] leading-snug" style={{ color: '#5a5550' }}>
                          I have read the{' '}
                          <button type="button" onClick={() => setLegalDoc('privacy')} className="font-semibold underline" style={{ color: '#F26B1F' }}>Privacy Notice</button>
                          {' '}and agree to the{' '}
                          <button type="button" onClick={() => setLegalDoc('terms')} className="font-semibold underline" style={{ color: '#F26B1F' }}>Terms of Use</button>.
                        </span>
                      </div>
                      <p className="text-[11px] leading-snug mt-2" style={{ color: '#9e9186', paddingLeft: '30px' }}>
                        Your school provides NextStepUni with your parent or guardian’s permission as part of enrolment. The Privacy Notice explains how your information is used.
                      </p>
                    </div>
                    <AnimatePresence>{error && <MotionDiv {...errorAnim} role="alert" aria-live="assertive" className="text-sm text-red-500 font-medium">{error}</MotionDiv>}</AnimatePresence>
                    <MotionButton whileHover={btnHover} whileTap={btnTap} transition={SPRING_FAST} onClick={handleRegisterSubmit} disabled={isLoading || !agreedToTerms} className={primaryBtn} style={primaryBtnStyle}>
                      {isLoading ? 'Creating your account...' : 'Create Account'}
                    </MotionButton>
                  </MotionDiv>
                )}
              </AnimatePresence>
            </>
          )}
        </MotionDiv>
      </AnimatePresence>
      <LegalModal doc={legalDoc} onClose={() => setLegalDoc(null)} />
    </LoginCard>
  );
};

export default LoginPage;
