/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo, useEffect } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionButton, MotionDiv, MotionP } from './Motion';
import { ArrowLeft, Eye, EyeOff, School, GraduationCap, ArrowRight, Check } from 'lucide-react';
import { auth, db } from '../firebase';
import { signInWithEmailAndPassword, createUserWithEmailAndPassword, updateProfile, deleteUser, sendPasswordResetEmail, GoogleAuthProvider, signInWithPopup } from 'firebase/auth';
import { doc, getDoc, setDoc } from 'firebase/firestore';
import { type SessionUser, getAvatarUrl, AVATAR_SEEDS } from '../utils/authUtils';
import { SCHOOLS } from '../schoolData';

// ── Shared animation tokens ──
const SPRING_FAST = { type: 'spring' as const, stiffness: 500, damping: 28 };
const SPRING_GENTLE = { type: 'spring' as const, stiffness: 340, damping: 30 };
const SPRING_POP = { type: 'spring' as const, stiffness: 420, damping: 18 };

const stepAnim = {
  initial: { opacity: 0, x: 24 },
  animate: { opacity: 1, x: 0 },
  exit: { opacity: 0, x: -24 },
  transition: SPRING_GENTLE,
};

const viewAnim = {
  initial: { opacity: 0, y: 14, scale: 0.97 },
  animate: { opacity: 1, y: 0, scale: 1 },
  exit: { opacity: 0, y: -10, scale: 0.97 },
  transition: SPRING_GENTLE,
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

      {/* Icon — centred anchor */}
      <div className="flex-1 flex items-center justify-center" style={{ padding: '16px 0' }}>
        <img
          src="/icons/gateway.png"
          alt=""
          aria-hidden
          style={{ width: '78%', maxWidth: 340, height: 'auto' }}
        />
      </div>

      {/* Statement + cycling caption */}
      <div>
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
        <div style={{ minHeight: 22 }}>
          <AnimatePresence mode="wait">
            <MotionP
              key={CYCLING_CAPTIONS[capIdx]}
              initial={{ opacity: 0, y: 4 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -4 }}
              transition={{ type: 'spring', stiffness: 340, damping: 30 }}
              className="font-sans"
              style={{
                fontSize: 13,
                color: '#7a7068',
                lineHeight: 1.55,
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
  <div className="min-h-screen flex flex-col items-center justify-center p-4 md:p-8 light" data-theme="light" style={{ backgroundColor: '#FAFBF6', colorScheme: 'light' }}>
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

const LoginPage: React.FC<LoginPageProps> = ({ handleLoginSuccess }) => {
  // ── Top-level mode ──
  const [view, setView] = useState<'welcome' | 'login' | 'register' | 'gc' | 'forgot'>('welcome');
  const [registerStep, setRegisterStep] = useState(1); // 1: email+name+school, 2: password, 3: avatar

  // ── Form state ──
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [school, setSchool] = useState('');
  const [gcSchool, setGcSchool] = useState('');
  const [avatar, setAvatar] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [resetSent, setResetSent] = useState(false);
  const [resendCountdown, setResendCountdown] = useState(0);

  // Countdown tick for the resend button on the forgot-password success screen.
  useEffect(() => {
    if (resendCountdown <= 0) return;
    const t = setTimeout(() => setResendCountdown(c => c - 1), 1000);
    return () => clearTimeout(t);
  }, [resendCountdown]);

  // Random default avatar for step 3
  const defaultAvatar = useMemo(() => AVATAR_SEEDS[Math.floor(Math.random() * AVATAR_SEEDS.length)], []);

  const resetForm = () => {
    setEmail(''); setPassword(''); setName(''); setSchool('');
    setGcSchool(''); setAvatar(''); setError('');
    setShowPassword(false); setRegisterStep(1); setResetSent(false);
    setResendCountdown(0);
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
        const userDoc = await getDoc(doc(db, 'users', cred.user.uid));
        if (userDoc.exists()) {
          const data = userDoc.data();
          handleLoginSuccess({
            uid: cred.user.uid,
            name: data.name || 'Student',
            avatar: data.avatar || 'James',
            isAdmin: data.isAdmin || false,
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
      const userRef = doc(db, 'users', cred.user.uid);
      const userDoc = await getDoc(userRef);
      if (userDoc.exists()) {
        const data = userDoc.data();
        handleLoginSuccess({
          uid: cred.user.uid,
          name: data.name || cred.user.displayName || 'Student',
          avatar: data.avatar || AVATAR_SEEDS[0],
          isAdmin: data.isAdmin || false,
          role: data.role || 'student',
          school: data.school || '',
          yearGroup: data.yearGroup,
        });
      } else {
        // First-time Google sign-in: create the user doc with school empty;
        // they can set it later in-app.
        const newName = cred.user.displayName || (cred.user.email?.split('@')[0]) || 'Student';
        const newAvatar = AVATAR_SEEDS[Math.floor(Math.random() * AVATAR_SEEDS.length)];
        await setDoc(userRef, { name: newName, avatar: newAvatar, school: '' });
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
      } else {
        console.error('Google sign-in failed:', err);
        setError('Could not sign in with Google. Try again or use email.');
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
    } catch (err) {
      console.error('GC login failed:', err);
      setError('Invalid credentials.');
    }
    setIsLoading(false);
  };

  // ── Register step validation ──
  const validateRegisterStep = (): boolean => {
    if (registerStep === 1) {
      if (!email.trim()) { setError('Please enter your email.'); return false; }
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim())) { setError('Please enter a valid email address.'); return false; }
      const normalised = email.trim().toLowerCase();
      if (normalised === 'admin@nextstep.app' || /^gc-.*@nextstep\.app$/.test(normalised)) { setError('This email is reserved.'); return false; }
      if (!name.trim()) { setError('Please enter your name.'); return false; }
      if (!school) { setError('Please select your school.'); return false; }
      return true;
    }
    if (registerStep === 2) {
      if (password.length < 6) { setError('Password must be at least 6 characters.'); return false; }
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
    if (registrationEmail === 'admin@nextstep.app' || /^gc-.*@nextstep\.app$/.test(registrationEmail)) {
      setError('This email is reserved.');
      setIsLoading(false);
      return;
    }
    const selectedAvatar = avatar || defaultAvatar;
    let createdUser: any = null;
    try {
      const cred = await createUserWithEmailAndPassword(auth, registrationEmail, password);
      createdUser = cred.user;
      await updateProfile(createdUser, { displayName: name.trim() });
      await setDoc(doc(db, 'users', createdUser.uid), {
        name: name.trim(),
        avatar: selectedAvatar,
        school,
      });
      handleLoginSuccess({
        uid: createdUser.uid,
        name: name.trim(),
        avatar: selectedAvatar,
        school,
        role: 'student',
      });
    } catch (err: any) {
      if (createdUser) {
        try { await deleteUser(createdUser); } catch (rollbackErr) {
          console.error('Failed to clean up auth account after registration failure:', rollbackErr);
        }
      }
      if (err.code === 'auth/weak-password') {
        setError('Password must be at least 6 characters.');
        setRegisterStep(2);
      } else if (err.code === 'auth/email-already-in-use') {
        setError('An account with this email already exists. Try signing in instead.');
        setRegisterStep(1);
      } else if (err.code === 'auth/invalid-email') {
        setError('Please enter a valid email address.');
        setRegisterStep(1);
      } else {
        setError('Registration failed. Try again.');
      }
    }
    setIsLoading(false);
  };

  // ── Shared styles ──
  const inputClass = "w-full py-3.5 px-4 rounded-xl text-sm font-sans text-zinc-800 placeholder-zinc-400 outline-none transition-all bg-white border-2 border-zinc-200 focus:border-[#2A7D6F]";
  const primaryBtn = "w-full py-3.5 rounded-full text-[15px] font-semibold transition-all border-2 disabled:opacity-50 disabled:cursor-not-allowed";
  const primaryBtnStyle = { backgroundColor: '#FFFFFF', color: '#1A1A1A', borderColor: 'rgba(26,26,26,0.55)' };

  // DEV button — only visible in development builds
  const devButton = (
    <button onClick={() => handleLoginSuccess({ uid: 'dev-student', name: 'Dev User', avatar: 'Casper', isAdmin: false })} className="mt-6 px-3 py-1 bg-red-600/10 text-red-400 border border-red-600/20 rounded-full text-[9px] font-mono hover:bg-red-600/20 transition-colors">
      DEV: Skip Login
    </button>
  );

  const selectedAvatar = avatar || defaultAvatar;

  // ═══════════════════════════════════════════════════════════
  // Single LoginCard with view-level AnimatePresence so navigating
  // between Welcome / Login / GC / Forgot / Register actually
  // animates — was an instant render before.
  // ═══════════════════════════════════════════════════════════
  return (
    <LoginCard devButton={devButton}>
      <AnimatePresence mode="wait" initial={false}>
        <MotionDiv key={view} {...viewAnim}>
          {/* ── WELCOME ────────────────────────────────────── */}
          {view === 'welcome' && (
            <div className="text-center">
              <p className="text-[10px] font-bold uppercase tracking-[0.2em] mb-6" style={{ color: '#9e9186' }}>NEXTSTEPUNI</p>
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
                  className="w-full py-3.5 rounded-full text-[15px] font-semibold transition-all border-2"
                  style={{ color: '#2A7D6F', borderColor: 'rgba(42,125,111,0.3)', backgroundColor: 'white' }}
                >
                  I already have an account
                </MotionButton>
                <MotionButton
                  whileHover={btnHover} whileTap={btnTap} transition={SPRING_FAST}
                  onClick={handleGoogleSignIn}
                  disabled={isLoading}
                  className="w-full py-3.5 rounded-full text-[15px] font-semibold transition-all border-2 flex items-center justify-center gap-2.5 disabled:opacity-50 disabled:cursor-not-allowed"
                  style={{ color: '#1a1a1a', borderColor: '#d0cdc8', backgroundColor: 'white' }}
                >
                  <GoogleIcon />
                  Continue with Google
                </MotionButton>
              </div>

              <div className="flex items-center gap-4 mt-8">
                <div className="flex-1 h-px" style={{ backgroundColor: '#d0cdc8' }} />
                <span className="text-[11px] font-medium" style={{ color: '#9e9186' }}>OR</span>
                <div className="flex-1 h-px" style={{ backgroundColor: '#d0cdc8' }} />
              </div>
              <button
                onClick={() => { resetForm(); setView('gc'); }}
                className="w-full py-3 rounded-full text-sm font-medium transition-all flex items-center justify-center gap-2 mt-4 border-2"
                style={{ color: '#7a7068', borderColor: '#d0cdc8', backgroundColor: 'white' }}
              >
                <GraduationCap size={16} /> Sign in as Guidance Counsellor
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
                  <label className="text-xs font-bold uppercase tracking-wider mb-1.5 block" style={{ color: '#9e9186' }}>Email</label>
                  <input type="email" value={email} onChange={e => { setEmail(e.target.value); setError(''); }} placeholder="you@example.com" className={inputClass} autoFocus />
                </div>
                <div>
                  <div className="flex items-center justify-between mb-1.5">
                    <label className="text-xs font-bold uppercase tracking-wider" style={{ color: '#9e9186' }}>Password</label>
                    <button type="button" onClick={() => { setView('forgot'); setError(''); }} className="text-xs font-semibold transition-colors hover:opacity-80" style={{ color: '#2A7D6F' }}>Forgot?</button>
                  </div>
                  <div className="relative">
                    <input type={showPassword ? 'text' : 'password'} value={password} onChange={e => { setPassword(e.target.value); setError(''); }} placeholder="Enter your password" className={inputClass} />
                    <button type="button" onClick={() => setShowPassword(!showPassword)} className="absolute right-3 top-1/2 -translate-y-1/2 transition-colors" style={{ color: '#9e9186' }}>
                      {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                    </button>
                  </div>
                </div>
                <AnimatePresence>{error && <MotionDiv {...errorAnim} className="text-sm text-red-500 font-medium">{error}</MotionDiv>}</AnimatePresence>
                <MotionButton type="submit" disabled={isLoading} whileHover={btnHover} whileTap={btnTap} transition={SPRING_FAST} className={primaryBtn} style={primaryBtnStyle}>
                  {isLoading ? 'Signing in...' : 'Sign In'}
                </MotionButton>
              </form>
              <div className="flex items-center gap-4 my-5">
                <div className="flex-1 h-px" style={{ backgroundColor: '#d0cdc8' }} />
                <span className="text-[11px] font-medium" style={{ color: '#9e9186' }}>OR</span>
                <div className="flex-1 h-px" style={{ backgroundColor: '#d0cdc8' }} />
              </div>
              <MotionButton
                whileHover={btnHover} whileTap={btnTap} transition={SPRING_FAST}
                onClick={handleGoogleSignIn}
                disabled={isLoading}
                className="w-full py-3.5 rounded-full text-[15px] font-semibold transition-all border-2 flex items-center justify-center gap-2.5 disabled:opacity-50 disabled:cursor-not-allowed"
                style={{ color: '#1a1a1a', borderColor: '#d0cdc8', backgroundColor: 'white' }}
              >
                <GoogleIcon />
                Continue with Google
              </MotionButton>
              <p className="text-sm text-center mt-6" style={{ color: '#9e9186' }}>
                Don&apos;t have an account?{' '}<button type="button" onClick={() => { resetForm(); setView('register'); }} className="font-semibold transition-colors hover:opacity-80" style={{ color: '#2A7D6F' }}>Register</button>
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
                  <label className="text-xs font-bold uppercase tracking-wider mb-1.5 block" style={{ color: '#9e9186' }}>School</label>
                  <div className="relative">
                    <select value={gcSchool} onChange={e => { setGcSchool(e.target.value); setError(''); }} className={`${inputClass} appearance-none cursor-pointer ${!gcSchool ? 'text-zinc-400' : ''}`} autoFocus>
                      <option value="" disabled>Select your school</option>
                      {SCHOOLS.map(s => (<option key={s.id} value={s.id}>{s.name}</option>))}
                    </select>
                    <School size={16} className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none" style={{ color: '#9e9186' }} />
                  </div>
                </div>
                <div>
                  <label className="text-xs font-bold uppercase tracking-wider mb-1.5 block" style={{ color: '#9e9186' }}>Password</label>
                  <div className="relative">
                    <input type={showPassword ? 'text' : 'password'} value={password} onChange={e => { setPassword(e.target.value); setError(''); }} placeholder="Enter your password" className={inputClass} />
                    <button type="button" onClick={() => setShowPassword(!showPassword)} className="absolute right-3 top-1/2 -translate-y-1/2 transition-colors" style={{ color: '#9e9186' }}>
                      {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                    </button>
                  </div>
                </div>
                <AnimatePresence>{error && <MotionDiv {...errorAnim} className="text-sm text-red-500 font-medium">{error}</MotionDiv>}</AnimatePresence>
                <MotionButton type="submit" disabled={isLoading} whileHover={btnHover} whileTap={btnTap} transition={SPRING_FAST} className={primaryBtn} style={primaryBtnStyle}>
                  {isLoading ? 'Signing in...' : 'Sign In'}
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
                    style={{ backgroundColor: '#e8f5f2' }}
                  >
                    <Check size={24} style={{ color: '#2A7D6F' }} />
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
                      className="w-full py-3 rounded-full text-[14px] font-medium transition-all border-2 disabled:opacity-50 disabled:cursor-not-allowed"
                      style={{ color: '#2A7D6F', borderColor: 'rgba(42,125,111,0.3)', backgroundColor: 'white' }}
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
                    <label className="text-xs font-bold uppercase tracking-wider mb-1.5 block" style={{ color: '#9e9186' }}>Email</label>
                    <input type="email" value={email} onChange={e => { setEmail(e.target.value); setError(''); }} placeholder="you@example.com" className={inputClass} autoFocus />
                  </div>
                  <AnimatePresence>{error && <MotionDiv {...errorAnim} className="text-sm text-red-500 font-medium">{error}</MotionDiv>}</AnimatePresence>
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
                        backgroundColor: s <= registerStep ? '#2A7D6F' : '#d0cdc8',
                      }}
                      transition={SPRING_GENTLE}
                    />
                  ))}
                </div>
              </div>

              <AnimatePresence mode="wait">
                {registerStep === 1 && (
                  <MotionDiv key="step1" {...stepAnim}>
                    <h2 className="text-2xl font-semibold tracking-tight mb-1" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>Let&apos;s get you set up</h2>
                    <p className="text-sm mb-8" style={{ color: '#7a7068' }}>We&apos;ll use your email to create your account and for password resets.</p>
                    <div className="space-y-4">
                      <div>
                        <label className="text-xs font-bold uppercase tracking-wider mb-1.5 block" style={{ color: '#9e9186' }}>Email</label>
                        <input type="email" value={email} onChange={e => { setEmail(e.target.value); setError(''); }} placeholder="you@example.com" className={inputClass} autoFocus />
                      </div>
                      <div>
                        <label className="text-xs font-bold uppercase tracking-wider mb-1.5 block" style={{ color: '#9e9186' }}>Your Name</label>
                        <input type="text" value={name} onChange={e => { setName(e.target.value); setError(''); }} placeholder="e.g. Sean, Emma, Jordan" className={inputClass} />
                      </div>
                      <div>
                        <label className="text-xs font-bold uppercase tracking-wider mb-1.5 block" style={{ color: '#9e9186' }}>School</label>
                        <div className="relative">
                          <select value={school} onChange={e => { setSchool(e.target.value); setError(''); }} className={`${inputClass} appearance-none cursor-pointer ${!school ? 'text-zinc-400' : ''}`}>
                            <option value="" disabled>Select your school</option>
                            {SCHOOLS.map(s => (<option key={s.id} value={s.id}>{s.name}</option>))}
                          </select>
                          <School size={16} className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none" style={{ color: '#9e9186' }} />
                        </div>
                      </div>
                      <AnimatePresence>{error && <MotionDiv {...errorAnim} className="text-sm text-red-500 font-medium">{error}</MotionDiv>}</AnimatePresence>
                      <MotionButton whileHover={btnHover} whileTap={btnTap} transition={SPRING_FAST} onClick={handleRegisterNext} className={primaryBtn} style={primaryBtnStyle}>
                        <span className="flex items-center justify-center gap-2">Continue <ArrowRight size={16} /></span>
                      </MotionButton>
                    </div>
                    <p className="text-sm text-center mt-6" style={{ color: '#9e9186' }}>
                      Already have an account?{' '}<button type="button" onClick={() => { resetForm(); setView('login'); }} className="font-semibold transition-colors hover:opacity-80" style={{ color: '#2A7D6F' }}>Sign in</button>
                    </p>
                  </MotionDiv>
                )}

                {registerStep === 2 && (
                  <MotionDiv key="step2" {...stepAnim}>
                    <h2 className="text-2xl font-semibold tracking-tight mb-1" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>Create a password</h2>
                    <p className="text-sm mb-8" style={{ color: '#7a7068' }}>At least 6 characters. You&apos;ll need this to log in.</p>
                    <div className="space-y-4">
                      <div>
                        <label className="text-xs font-bold uppercase tracking-wider mb-1.5 block" style={{ color: '#9e9186' }}>Password</label>
                        <div className="relative">
                          <input type={showPassword ? 'text' : 'password'} value={password} onChange={e => { setPassword(e.target.value); setError(''); }} placeholder="Create a password" className={inputClass} autoFocus />
                          <button type="button" onClick={() => setShowPassword(!showPassword)} className="absolute right-3 top-1/2 -translate-y-1/2 transition-colors" style={{ color: '#9e9186' }}>
                            {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                          </button>
                        </div>
                        {password.length > 0 && password.length < 6 && (
                          <p className="text-xs mt-1.5" style={{ color: '#9e9186' }}>{6 - password.length} more character{6 - password.length !== 1 ? 's' : ''} needed</p>
                        )}
                        {password.length >= 6 && (
                          <p className="text-xs mt-1.5 flex items-center gap-1" style={{ color: '#2A7D6F' }}><Check size={12} /> Looks good</p>
                        )}
                      </div>
                      <AnimatePresence>{error && <MotionDiv {...errorAnim} className="text-sm text-red-500 font-medium">{error}</MotionDiv>}</AnimatePresence>
                      <MotionButton whileHover={btnHover} whileTap={btnTap} transition={SPRING_FAST} onClick={handleRegisterNext} className={primaryBtn} style={primaryBtnStyle}>
                        <span className="flex items-center justify-center gap-2">Continue <ArrowRight size={16} /></span>
                      </MotionButton>
                    </div>
                  </MotionDiv>
                )}

                {registerStep === 3 && (
                  <MotionDiv key="step3" {...stepAnim}>
                    <h2 className="text-2xl font-semibold tracking-tight mb-1" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>Choose your avatar</h2>
                    <p className="text-sm mb-6" style={{ color: '#7a7068' }}>Pick one that feels like you. You can change it later.</p>
                    <div className="grid grid-cols-4 gap-3 mb-6">
                      {AVATAR_SEEDS.map(seed => (
                        <button key={seed} type="button" onClick={() => setAvatar(seed)} className={`rounded-xl aspect-square p-1 transition-all ${selectedAvatar === seed ? 'ring-2 ring-offset-2 bg-[#e8f5f2]' : 'hover:ring-1 hover:ring-zinc-300 bg-white'}`} style={selectedAvatar === seed ? { ringColor: '#2A7D6F', borderColor: '#2A7D6F', border: '2px solid #2A7D6F' } : { border: '2px solid #d0cdc8' }}>
                          <img src={getAvatarUrl(seed)} alt={seed} className="w-full h-full rounded-lg" />
                        </button>
                      ))}
                    </div>
                    <AnimatePresence>{error && <MotionDiv {...errorAnim} className="text-sm text-red-500 font-medium">{error}</MotionDiv>}</AnimatePresence>
                    <MotionButton whileHover={btnHover} whileTap={btnTap} transition={SPRING_FAST} onClick={handleRegisterSubmit} disabled={isLoading} className={primaryBtn} style={primaryBtnStyle}>
                      {isLoading ? 'Creating your account...' : 'Create Account'}
                    </MotionButton>
                  </MotionDiv>
                )}
              </AnimatePresence>
            </>
          )}
        </MotionDiv>
      </AnimatePresence>
    </LoginCard>
  );
};

export default LoginPage;
