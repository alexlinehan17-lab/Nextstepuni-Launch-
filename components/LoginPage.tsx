/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionButton, MotionDiv } from './Motion';
import { ArrowLeft, Eye, EyeOff, School, GraduationCap, ArrowRight, Check } from 'lucide-react';
import { auth, db } from '../firebase';
import { signInWithEmailAndPassword, createUserWithEmailAndPassword, updateProfile, deleteUser } from 'firebase/auth';
import { doc, getDoc, setDoc } from 'firebase/firestore';
import { type SessionUser, getAvatarUrl, AVATAR_SEEDS } from './Auth';
import { SCHOOLS } from '../schoolData';

interface LoginPageProps {
  handleLoginSuccess: (u: SessionUser) => void;
}

const LoginPage: React.FC<LoginPageProps> = ({ handleLoginSuccess }) => {
  // ── Top-level mode ──
  const [view, setView] = useState<'welcome' | 'login' | 'register' | 'gc'>('welcome');
  const [registerStep, setRegisterStep] = useState(1); // 1: school+name, 2: password, 3: avatar

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

  // Random default avatar for step 3
  const defaultAvatar = useMemo(() => AVATAR_SEEDS[Math.floor(Math.random() * AVATAR_SEEDS.length)], []);

  const resetForm = () => {
    setEmail(''); setPassword(''); setName(''); setSchool('');
    setGcSchool(''); setAvatar(''); setError('');
    setShowPassword(false); setRegisterStep(1);
  };

  // ── Login handler ──
  // Login school state (separate from registration school)
  const [loginSchool, setLoginSchool] = useState('');

  const handleLogin = async () => {
    if (!email.trim() || !password.trim()) { setError('Please enter your username and password.'); return; }
    setIsLoading(true); setError('');
    try {
      // Try school-namespaced email first, fall back to legacy format
      const username = email.trim().toLowerCase().replace(/\s+/g, '');
      const emailToUse = email.includes('@') ? email
        : loginSchool ? `${username}-${loginSchool}@nextstep.app`
        : `${username}@nextstep.app`;
      const cred = await signInWithEmailAndPassword(auth, emailToUse, password);
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
    } catch {
      setError('Invalid username or password.');
    }
    setIsLoading(false);
  };

  // ── GC Login handler ──
  const handleGCLogin = async () => {
    if (!gcSchool || !password.trim()) { setError('Please select your school and enter your password.'); return; }
    setIsLoading(true); setError('');
    try {
      await signInWithEmailAndPassword(auth, `gc-${gcSchool}@nextstep.app`, password);
    } catch {
      setError('Invalid credentials.');
    }
    setIsLoading(false);
  };

  // ── Register step validation ──
  const validateRegisterStep = (): boolean => {
    if (registerStep === 1) {
      if (!name.trim()) { setError('Please enter your name.'); return false; }
      const username = name.trim().toLowerCase().replace(/\s+/g, '');
      if (!/^[a-z0-9_-]+$/.test(username)) { setError('Name can only contain letters, numbers, hyphens and underscores.'); return false; }
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
    const selectedAvatar = avatar || defaultAvatar;
    const username = name.trim().toLowerCase().replace(/\s+/g, '');
    let createdUser: any = null;
    try {
      const cred = await createUserWithEmailAndPassword(auth, `${username}-${school}@nextstep.app`, password);
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
        setError('This name is already taken at your school. Try a different one.');
        setRegisterStep(1);
      } else {
        setError('Registration failed. Try again.');
      }
    }
    setIsLoading(false);
  };

  // ── Shared styles ──
  const inputClass = "w-full py-3.5 px-4 rounded-xl text-sm font-sans text-zinc-800 dark:text-white placeholder-zinc-400 dark:placeholder-zinc-500 outline-none transition-all bg-white dark:bg-zinc-900 border-2 border-zinc-200 dark:border-zinc-700 focus:border-[#2A7D6F]";
  const primaryBtn = "w-full py-3.5 rounded-full text-white text-[15px] font-semibold transition-all disabled:opacity-50 disabled:cursor-not-allowed";
  const primaryBtnStyle = { backgroundColor: '#2A7D6F', borderBottom: '3px solid #1a5a4e', boxShadow: '0 4px 0 #1a5a4e' };

  // ── Aurora gradient left panel ──
  const gradientPanel = (
    <div className="hidden md:block w-1/2 relative overflow-hidden" style={{ borderRadius: '16px 0 0 16px' }}>
      <div className="absolute inset-0" style={{ backgroundColor: '#EAE5DE' }} />
      <div className="absolute inset-0" style={{ background: 'linear-gradient(180deg, #FDF8F0 0%, transparent 15%)' }} />
      <div className="absolute inset-0" style={{ background: 'radial-gradient(ellipse 140% 70% at 50% 50%, rgba(140,120,210,0.5) 0%, transparent 65%)' }} />
      <div className="absolute inset-0" style={{ background: 'radial-gradient(ellipse 100% 50% at 35% 40%, rgba(155,135,225,0.35) 0%, transparent 60%)' }} />
      <div className="absolute inset-0" style={{ background: 'radial-gradient(ellipse 120% 55% at 50% 95%, rgba(225,110,160,0.65) 0%, transparent 50%)' }} />
      <div className="absolute inset-0" style={{ background: 'radial-gradient(ellipse 90% 45% at 50% 75%, rgba(215,130,175,0.4) 0%, transparent 55%)' }} />
      <div className="absolute inset-0" style={{ background: 'radial-gradient(ellipse 60% 65% at 0% 60%, rgba(120,145,225,0.4) 0%, transparent 60%)' }} />
      <div className="absolute inset-0" style={{ background: 'radial-gradient(ellipse 60% 65% at 100% 60%, rgba(120,145,225,0.35) 0%, transparent 60%)' }} />
      <div className="absolute inset-0" style={{ background: 'radial-gradient(ellipse 55% 40% at 65% 88%, rgba(240,150,120,0.4) 0%, transparent 50%)' }} />
    </div>
  );

  // ── Card wrapper — split panel on desktop, full-width on mobile ──
  const Card: React.FC<{ children: React.ReactNode }> = ({ children }) => (
    <div className="min-h-screen flex flex-col items-center justify-center p-4 md:p-8" style={{ backgroundColor: '#FAFAF7' }}>
      <MotionDiv
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: 'easeOut' }}
        className="w-full max-w-5xl bg-white dark:bg-zinc-900 rounded-2xl overflow-hidden flex"
        style={{ minHeight: 540, boxShadow: '0 2px 8px rgba(0,0,0,0.06), 0 12px 40px rgba(0,0,0,0.04)', border: '1.5px solid rgba(0,0,0,0.25)' }}
      >
        {gradientPanel}
        <div className="w-full md:w-1/2 flex flex-col justify-center px-8 md:px-14 py-12">
          <div className="w-full max-w-[380px] mx-auto">
            {children}
          </div>
        </div>
      </MotionDiv>
      {/* DEV button */}
      <button onClick={() => handleLoginSuccess({ uid: 'dev-student', name: 'Dev User', avatar: 'Casper', isAdmin: false })} className="mt-6 px-3 py-1 bg-red-600/10 text-red-400 border border-red-600/20 rounded-full text-[9px] font-mono hover:bg-red-600/20 transition-colors">
        DEV: Skip Login
      </button>
    </div>
  );

  // ═══════════════════════════════════════════════════════════
  // WELCOME SCREEN — first thing users see
  // ═══════════════════════════════════════════════════════════
  if (view === 'welcome') {
    return (
      <Card>
        <div className="text-center">
          <p className="text-[10px] font-bold uppercase tracking-[0.2em] mb-6" style={{ color: '#9e9186' }}>NEXTSTEPUNI</p>
          <h1 className="text-3xl md:text-4xl font-semibold tracking-tight mb-3" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>
            Your Leaving Cert,<br />your way.
          </h1>
          <p className="text-sm mb-10" style={{ fontFamily: "'DM Sans', sans-serif", color: '#7a7068' }}>
            Science-backed study strategies personalised to your subjects, your goals, and your exam.
          </p>

          <div className="space-y-3">
            <MotionButton
              whileHover={{ scale: 1.01 }} whileTap={{ scale: 0.97 }}
              onClick={() => { resetForm(); setView('register'); }}
              className={primaryBtn}
              style={primaryBtnStyle}
            >
              Get Started
            </MotionButton>
            <MotionButton
              whileHover={{ scale: 1.01 }} whileTap={{ scale: 0.97 }}
              onClick={() => { resetForm(); setView('login'); }}
              className="w-full py-3.5 rounded-full text-[15px] font-semibold transition-all border-2"
              style={{ color: '#2A7D6F', borderColor: 'rgba(42,125,111,0.3)', backgroundColor: 'white' }}
            >
              I already have an account
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
      </Card>
    );
  }

  // ═══════════════════════════════════════════════════════════
  // LOGIN SCREEN
  // ═══════════════════════════════════════════════════════════
  if (view === 'login') {
    return (
      <Card>
        <button type="button" onClick={() => setView('welcome')} className="flex items-center gap-1.5 text-sm font-medium mb-6 transition-colors" style={{ color: '#9e9186' }}>
          <ArrowLeft size={14} /> Back
        </button>
        <h2 className="text-2xl font-semibold tracking-tight mb-1" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>Welcome back</h2>
        <p className="text-sm mb-8" style={{ color: '#7a7068' }}>Sign in with your username and password.</p>
        <form onSubmit={e => { e.preventDefault(); handleLogin(); }} className="space-y-4">
          <div>
            <label className="text-xs font-bold uppercase tracking-wider mb-1.5 block" style={{ color: '#9e9186' }}>School</label>
            <div className="relative">
              <select value={loginSchool} onChange={e => { setLoginSchool(e.target.value); setError(''); }} className={`${inputClass} appearance-none cursor-pointer ${!loginSchool ? 'text-zinc-400' : ''}`} autoFocus>
                <option value="" disabled>Select your school</option>
                {SCHOOLS.map(s => (<option key={s.id} value={s.id}>{s.name}</option>))}
              </select>
              <School size={16} className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none" style={{ color: '#9e9186' }} />
            </div>
          </div>
          <div>
            <label className="text-xs font-bold uppercase tracking-wider mb-1.5 block" style={{ color: '#9e9186' }}>Username</label>
            <input type="text" value={email} onChange={e => { setEmail(e.target.value); setError(''); }} placeholder="Enter your username" className={inputClass} />
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
          <AnimatePresence>{error && <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="text-sm text-red-500 font-medium">{error}</MotionDiv>}</AnimatePresence>
          <MotionButton type="submit" disabled={isLoading} whileHover={{ scale: 1.01 }} whileTap={{ scale: 0.97 }} className={primaryBtn} style={primaryBtnStyle}>
            {isLoading ? 'Signing in...' : 'Sign In'}
          </MotionButton>
        </form>
        <p className="text-sm text-center mt-6" style={{ color: '#7a7068' }}>
          Forgot your password?{' '}<span style={{ color: '#2A7D6F', fontWeight: 600 }}>Ask your guidance counsellor.</span>
        </p>
        <p className="text-sm text-center mt-3" style={{ color: '#9e9186' }}>
          Don&apos;t have an account?{' '}<button type="button" onClick={() => { resetForm(); setView('register'); }} className="font-semibold transition-colors hover:opacity-80" style={{ color: '#2A7D6F' }}>Register</button>
        </p>
      </Card>
    );
  }

  // ═══════════════════════════════════════════════════════════
  // GC LOGIN SCREEN
  // ═══════════════════════════════════════════════════════════
  if (view === 'gc') {
    return (
      <Card>
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
          <AnimatePresence>{error && <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="text-sm text-red-500 font-medium">{error}</MotionDiv>}</AnimatePresence>
          <MotionButton type="submit" disabled={isLoading} whileHover={{ scale: 1.01 }} whileTap={{ scale: 0.97 }} className={primaryBtn} style={primaryBtnStyle}>
            {isLoading ? 'Signing in...' : 'Sign In'}
          </MotionButton>
        </form>
      </Card>
    );
  }

  // ═══════════════════════════════════════════════════════════
  // REGISTER — Multi-step
  // ═══════════════════════════════════════════════════════════
  const selectedAvatar = avatar || defaultAvatar;

  return (
    <Card>
      {/* Back + progress */}
      <div className="flex items-center justify-between mb-6">
        <button type="button" onClick={() => {
          if (registerStep > 1) { setRegisterStep(s => s - 1); setError(''); }
          else setView('welcome');
        }} className="flex items-center gap-1.5 text-sm font-medium transition-colors" style={{ color: '#9e9186' }}>
          <ArrowLeft size={14} /> Back
        </button>
        <div className="flex items-center gap-1.5">
          {[1, 2, 3].map(s => (
            <div key={s} className="h-1.5 rounded-full transition-all" style={{
              width: s === registerStep ? 24 : 8,
              backgroundColor: s <= registerStep ? '#2A7D6F' : '#d0cdc8',
            }} />
          ))}
        </div>
      </div>

      <AnimatePresence mode="wait">
        {/* ── Step 1: School + Name ── */}
        {registerStep === 1 && (
          <MotionDiv key="step1" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.25 }}>
            <h2 className="text-2xl font-semibold tracking-tight mb-1" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>Let&apos;s get you set up</h2>
            <p className="text-sm mb-8" style={{ color: '#7a7068' }}>Pick your school and choose a name. This is how you&apos;ll log in.</p>
            <div className="space-y-4">
              <div>
                <label className="text-xs font-bold uppercase tracking-wider mb-1.5 block" style={{ color: '#9e9186' }}>School</label>
                <div className="relative">
                  <select value={school} onChange={e => { setSchool(e.target.value); setError(''); }} className={`${inputClass} appearance-none cursor-pointer ${!school ? 'text-zinc-400' : ''}`} autoFocus>
                    <option value="" disabled>Select your school</option>
                    {SCHOOLS.map(s => (<option key={s.id} value={s.id}>{s.name}</option>))}
                  </select>
                  <School size={16} className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none" style={{ color: '#9e9186' }} />
                </div>
              </div>
              <div>
                <label className="text-xs font-bold uppercase tracking-wider mb-1.5 block" style={{ color: '#9e9186' }}>Your Name</label>
                <input type="text" value={name} onChange={e => { setName(e.target.value); setError(''); }} placeholder="e.g. sean, emma_k, jmurphy" className={inputClass} />
                {name.trim() && (
                  <p className="text-xs mt-1.5" style={{ color: '#9e9186' }}>You&apos;ll log in as <span className="font-semibold" style={{ color: '#2A7D6F' }}>{name.trim().toLowerCase().replace(/\s+/g, '')}</span></p>
                )}
              </div>
              <AnimatePresence>{error && <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="text-sm text-red-500 font-medium">{error}</MotionDiv>}</AnimatePresence>
              <MotionButton whileHover={{ scale: 1.01 }} whileTap={{ scale: 0.97 }} onClick={handleRegisterNext} className={primaryBtn} style={primaryBtnStyle}>
                <span className="flex items-center justify-center gap-2">Continue <ArrowRight size={16} /></span>
              </MotionButton>
            </div>
            <p className="text-sm text-center mt-6" style={{ color: '#9e9186' }}>
              Already have an account?{' '}<button type="button" onClick={() => { resetForm(); setView('login'); }} className="font-semibold transition-colors hover:opacity-80" style={{ color: '#2A7D6F' }}>Sign in</button>
            </p>
          </MotionDiv>
        )}

        {/* ── Step 2: Password ── */}
        {registerStep === 2 && (
          <MotionDiv key="step2" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.25 }}>
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
              <AnimatePresence>{error && <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="text-sm text-red-500 font-medium">{error}</MotionDiv>}</AnimatePresence>
              <MotionButton whileHover={{ scale: 1.01 }} whileTap={{ scale: 0.97 }} onClick={handleRegisterNext} className={primaryBtn} style={primaryBtnStyle}>
                <span className="flex items-center justify-center gap-2">Continue <ArrowRight size={16} /></span>
              </MotionButton>
            </div>
          </MotionDiv>
        )}

        {/* ── Step 3: Avatar ── */}
        {registerStep === 3 && (
          <MotionDiv key="step3" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.25 }}>
            <h2 className="text-2xl font-semibold tracking-tight mb-1" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>Choose your avatar</h2>
            <p className="text-sm mb-6" style={{ color: '#7a7068' }}>Pick one that feels like you. You can change it later.</p>
            <div className="grid grid-cols-4 gap-3 mb-6">
              {AVATAR_SEEDS.map(seed => (
                <button key={seed} type="button" onClick={() => setAvatar(seed)} className={`rounded-xl aspect-square p-1 transition-all ${selectedAvatar === seed ? 'ring-2 ring-offset-2 bg-[#e8f5f2]' : 'hover:ring-1 hover:ring-zinc-300 bg-white dark:bg-zinc-800'}`} style={selectedAvatar === seed ? { ringColor: '#2A7D6F', borderColor: '#2A7D6F', border: '2px solid #2A7D6F' } : { border: '2px solid #d0cdc8' }}>
                  <img src={getAvatarUrl(seed)} alt={seed} className="w-full h-full rounded-lg" />
                </button>
              ))}
            </div>
            <AnimatePresence>{error && <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="text-sm text-red-500 font-medium">{error}</MotionDiv>}</AnimatePresence>
            <MotionButton whileHover={{ scale: 1.01 }} whileTap={{ scale: 0.97 }} onClick={handleRegisterSubmit} disabled={isLoading} className={primaryBtn} style={primaryBtnStyle}>
              {isLoading ? 'Creating your account...' : 'Create Account'}
            </MotionButton>
          </MotionDiv>
        )}
      </AnimatePresence>
    </Card>
  );
};

export default LoginPage;
