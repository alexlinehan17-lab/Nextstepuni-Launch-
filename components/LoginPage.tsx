/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MotionButton, MotionDiv } from './Motion';
import { ArrowLeft, Eye, EyeOff, School, GraduationCap } from 'lucide-react';
import { auth, db } from '../firebase';
import { signInWithEmailAndPassword, createUserWithEmailAndPassword, updateProfile, deleteUser } from 'firebase/auth';
import { doc, getDoc, setDoc } from 'firebase/firestore';
import { type SessionUser, getAvatarUrl, AVATAR_SEEDS } from './Auth';
import { SCHOOLS } from '../schoolData';

interface LoginPageProps {
  handleLoginSuccess: (u: SessionUser) => void;
}

const LoginPage: React.FC<LoginPageProps> = ({ handleLoginSuccess }) => {
  const [authMode, setAuthMode] = useState<'login' | 'register'>('login');
  const [loginType, setLoginType] = useState<'student' | 'gc' | null>(null);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [name, setName] = useState('');
  const [school, setSchool] = useState('');
  const [gcSchool, setGcSchool] = useState('');
  const [avatar, setAvatar] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPw, setShowConfirmPw] = useState(false);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [, setResetSent] = useState(false);

  const handleLogin = async () => {
    setIsLoading(true);
    setError('');
    try {
      const emailToUse = email.includes('@') ? email : `${email}@nextstep.app`;
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
      setError('Invalid email or password');
    }
    setIsLoading(false);
  };

  const handleGCLogin = async () => {
    if (!gcSchool || !password.trim()) {
      setError('Please select your school and enter your password.');
      return;
    }
    setIsLoading(true);
    setError('');
    try {
      const gcEmail = `gc-${gcSchool}@nextstep.app`;
      await signInWithEmailAndPassword(auth, gcEmail, password);
    } catch {
      setError('Invalid credentials.');
    }
    setIsLoading(false);
  };

  const handleRegister = async () => {
    if (password !== confirmPassword) { setError('Passwords don\'t match'); return; }
    if (!name.trim()) { setError('Please enter your name'); return; }
    if (!school) { setError('Please select your school'); return; }
    if (!avatar) { setError('Please choose an avatar'); return; }
    setIsLoading(true);
    setError('');
    let createdUser: any = null;
    try {
      const emailToUse = `${name.toLowerCase().replace(/\s+/g, '')}@nextstep.app`;
      const cred = await createUserWithEmailAndPassword(auth, emailToUse, password);
      createdUser = cred.user;
      // Set displayName on Firebase Auth so it survives refresh even if
      // the Firestore user doc hasn't synced yet.
      await updateProfile(createdUser, { displayName: name.trim() });
      // Note: Firestore security rules forbid 'role' and 'createdAt' in user doc
      // creates — only name, avatar, and school are allowed.
      await setDoc(doc(db, 'users', createdUser.uid), {
        name: name.trim(),
        avatar,
        school,
      });
      handleLoginSuccess({
        uid: createdUser.uid,
        name: name.trim(),
        avatar,
        school,
        role: 'student',
      });
    } catch (err: any) {
      // Roll back auth account if it was created but Firestore write failed
      if (createdUser) {
        try { await deleteUser(createdUser); } catch (rollbackErr) {
          console.error('Failed to clean up auth account after registration failure:', rollbackErr);
        }
      }
      if (err.code === 'auth/weak-password') {
        setError('Password must be at least 6 characters.');
      } else if (err.code === 'auth/email-already-in-use') {
        setError('This name is already taken. Try a different one.');
      } else {
        setError('Registration failed. Try again.');
      }
    }
    setIsLoading(false);
  };


  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (authMode === 'register') {
      handleRegister();
    } else if (loginType === 'gc') {
      handleGCLogin();
    } else {
      handleLogin();
    }
  };

  const resetForm = () => {
    setEmail('');
    setPassword('');
    setConfirmPassword('');
    setName('');
    setSchool('');
    setGcSchool('');
    setAvatar('');
    setError('');
    setResetSent(false);
    setShowPassword(false);
    setShowConfirmPw(false);
  };

  const inputClass = "w-full py-3 px-4 rounded-xl text-sm text-zinc-800 dark:text-white placeholder-zinc-400 outline-none transition-all bg-[#FAF7F4] dark:bg-zinc-900 border border-[#e4e4e7] dark:border-zinc-700";

  // ── Cursor glow state for left panel ──
  const [cursorPos, setCursorPos] = useState<{ x: number; y: number } | null>(null);

  const handlePanelMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    setCursorPos({ x: e.clientX - rect.left, y: e.clientY - rect.top });
  };

  // ── Left Panel: Aurora gradient ──
  const gradientPanel = (
    <div
      className="hidden md:block w-1/2 relative overflow-hidden"
      style={{ borderRadius: '16px 0 0 16px' }}
      onMouseMove={handlePanelMouseMove}
      onMouseLeave={() => setCursorPos(null)}
    >
      {/* Aurora mesh gradient — stronger than onboarding for contained panel */}
      <div className="absolute inset-0" style={{ backgroundColor: '#EAE5DE' }} />
      <div className="absolute inset-0" style={{ background: 'linear-gradient(180deg, #FDF8F0 0%, transparent 15%)' }} />
      <div className="absolute inset-0" style={{ background: 'radial-gradient(ellipse 140% 70% at 50% 50%, rgba(140,120,210,0.5) 0%, transparent 65%)' }} />
      <div className="absolute inset-0" style={{ background: 'radial-gradient(ellipse 100% 50% at 35% 40%, rgba(155,135,225,0.35) 0%, transparent 60%)' }} />
      <div className="absolute inset-0" style={{ background: 'radial-gradient(ellipse 120% 55% at 50% 95%, rgba(225,110,160,0.65) 0%, transparent 50%)' }} />
      <div className="absolute inset-0" style={{ background: 'radial-gradient(ellipse 90% 45% at 50% 75%, rgba(215,130,175,0.4) 0%, transparent 55%)' }} />
      <div className="absolute inset-0" style={{ background: 'radial-gradient(ellipse 60% 65% at 0% 60%, rgba(120,145,225,0.4) 0%, transparent 60%)' }} />
      <div className="absolute inset-0" style={{ background: 'radial-gradient(ellipse 60% 65% at 100% 60%, rgba(120,145,225,0.35) 0%, transparent 60%)' }} />
      <div className="absolute inset-0" style={{ background: 'radial-gradient(ellipse 55% 40% at 65% 88%, rgba(240,150,120,0.4) 0%, transparent 50%)' }} />

      {/* Cursor glow — follows mouse */}
      <motion.div
        className="absolute pointer-events-none"
        animate={{
          x: (cursorPos?.x ?? 0) - 200,
          y: (cursorPos?.y ?? 0) - 200,
          opacity: cursorPos ? 0.5 : 0,
        }}
        transition={{ type: 'spring', damping: 25, stiffness: 200, mass: 0.5 }}
        style={{
          width: 400,
          height: 400,
          borderRadius: '50%',
          background: 'radial-gradient(circle, rgba(255,255,255,0.35) 0%, rgba(255,255,255,0.15) 40%, transparent 70%)',
          filter: 'blur(20px)',
          zIndex: 10,
        }}
      />

    </div>
  );

  // ── GC Login View ──
  if (loginType === 'gc') {
    return (
      <div className="min-h-screen flex items-center justify-center p-4 md:p-8 bg-[#FAFAF7] dark:bg-zinc-950">
        <MotionDiv
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
          className="w-full max-w-5xl bg-white dark:bg-zinc-900 rounded-2xl overflow-hidden flex"
          style={{ minHeight: 540, boxShadow: '0 4px 40px rgba(0,0,0,0.06)' }}
        >
          {gradientPanel}
          <div className="w-full md:w-1/2 flex flex-col justify-center px-8 md:px-14 py-16">
            <div className="w-full max-w-[380px] mx-auto">
              <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5 }}>
                <p className="text-zinc-400 text-[10px] font-semibold tracking-[0.2em] mb-8">NEXTSTEPUNI</p>
              </MotionDiv>
              <AnimatePresence mode="wait">
                <MotionDiv key="gc-form" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.3 }}>
                  <button type="button" onClick={() => { setLoginType(null); resetForm(); }} className="flex items-center gap-1.5 text-sm text-zinc-400 hover:text-zinc-600 mb-6 transition-colors">
                    <ArrowLeft size={14} /> Back
                  </button>
                  <h2 className="text-3xl font-semibold text-zinc-900 tracking-tight mb-1">Guidance Counsellor</h2>
                  <p className="text-sm text-zinc-400 mb-8">Select your school and enter your password.</p>
                  <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                      <label className="text-sm text-zinc-600 font-medium mb-1.5 block">School</label>
                      <select value={gcSchool} onChange={e => { setGcSchool(e.target.value); setError(''); }} className={`${inputClass} appearance-none cursor-pointer ${!gcSchool ? 'text-zinc-400' : ''}`} autoFocus>
                        <option value="" disabled>Select your school</option>
                        {SCHOOLS.map(s => (<option key={s.id} value={s.id}>{s.name}</option>))}
                      </select>
                    </div>
                    <div>
                      <label className="text-sm text-zinc-600 font-medium mb-1.5 block">Password</label>
                      <div className="relative">
                        <input type={showPassword ? 'text' : 'password'} value={password} onChange={e => { setPassword(e.target.value); setError(''); }} placeholder="Enter your password" className={inputClass} />
                        <button type="button" onClick={() => setShowPassword(!showPassword)} className="absolute right-3 top-1/2 -translate-y-1/2 text-zinc-400 hover:text-zinc-600 transition-colors">
                          {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                        </button>
                      </div>
                    </div>
                    <AnimatePresence>{error && <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="text-sm text-red-500 font-medium">{error}</MotionDiv>}</AnimatePresence>
                    <MotionButton type="submit" disabled={isLoading} whileHover={{ scale: 1.01 }} whileTap={{ scale: 0.99 }} className="w-full py-3 rounded-xl text-white text-sm font-semibold transition-all disabled:opacity-60 disabled:cursor-not-allowed" style={{ backgroundColor: '#2A7D6F' }}>
                      {isLoading ? 'Signing in...' : 'Sign In'}
                    </MotionButton>
                  </form>
                  <button onClick={() => handleLoginSuccess({ uid: 'dev-student', name: 'Dev User', avatar: 'Casper', isAdmin: false })} className="mt-10 mx-auto block px-3 py-1 bg-red-600/10 text-red-400 border border-red-600/20 rounded-full text-[9px] font-mono hover:bg-red-600/20 transition-colors">
                    DEV: Skip Login
                  </button>
                </MotionDiv>
              </AnimatePresence>
            </div>
          </div>
        </MotionDiv>
      </div>
    );
  }

  // ── Main Login / Register View ──
  return (
    <div className="min-h-screen flex items-center justify-center p-4 md:p-8 bg-[#FAFAF7] dark:bg-zinc-950">
      <MotionDiv
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: 'easeOut' }}
        className="w-full max-w-5xl bg-white dark:bg-zinc-900 rounded-2xl overflow-hidden flex"
        style={{ minHeight: 540, boxShadow: '0 2px 8px rgba(0,0,0,0.06), 0 12px 40px rgba(0,0,0,0.04)', border: '1.5px solid rgba(0,0,0,0.25)' }}
      >
        {gradientPanel}
        <div className="w-full md:w-1/2 flex flex-col justify-center px-8 md:px-14 py-16">
          <div className="w-full max-w-[380px] mx-auto">
            <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5 }}>
              <p className="text-zinc-400 text-[10px] font-semibold tracking-[0.2em] mb-8">NEXTSTEPUNI</p>
            </MotionDiv>
            <AnimatePresence mode="wait">
              {authMode === 'login' ? (
                <MotionDiv key="login-form" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.3 }}>
                  <h2 className="text-3xl font-semibold text-zinc-900 tracking-tight mb-8">Welcome back</h2>
                  <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                      <label className="text-sm text-zinc-600 font-medium mb-1.5 block">Username</label>
                      <input type="text" value={email} onChange={e => { setEmail(e.target.value); setError(''); setResetSent(false); }} placeholder="Enter your username" className={inputClass} autoFocus />
                    </div>
                    <div>
                      <div className="mb-1.5"><label className="text-sm text-zinc-600 font-medium">Password</label></div>
                      <div className="relative">
                        <input type={showPassword ? 'text' : 'password'} value={password} onChange={e => { setPassword(e.target.value); setError(''); }} placeholder="Enter your password" className={inputClass} />
                        <button type="button" onClick={() => setShowPassword(!showPassword)} className="absolute right-3 top-1/2 -translate-y-1/2 text-zinc-400 hover:text-zinc-600 transition-colors">
                          {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                        </button>
                      </div>
                    </div>
                    <AnimatePresence>{error && <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="text-sm text-red-500 font-medium">{error}</MotionDiv>}</AnimatePresence>
                    <MotionButton type="submit" disabled={isLoading} whileHover={{ scale: 1.01 }} whileTap={{ scale: 0.99 }} className="w-full py-3 rounded-xl text-white text-sm font-semibold transition-all disabled:opacity-60 disabled:cursor-not-allowed" style={{ backgroundColor: '#2A7D6F' }}>
                      {isLoading ? 'Signing in...' : 'Sign In'}
                    </MotionButton>
                  </form>
                  <p className="text-sm text-zinc-400 text-center mt-6">Don&apos;t have an account?{' '}<button type="button" onClick={() => { setAuthMode('register'); resetForm(); }} className="text-sm font-semibold transition-colors hover:opacity-80" style={{ color: '#2A7D6F' }}>Register</button></p>
                  <div className="flex items-center gap-4 mt-6"><div className="flex-1 h-px bg-zinc-200" /><span className="text-xs text-zinc-400">OR</span><div className="flex-1 h-px bg-zinc-200" /></div>
                  <MotionButton type="button" onClick={() => { setLoginType('gc'); resetForm(); }} whileHover={{ scale: 1.01, backgroundColor: '#fafaf7' }} whileTap={{ scale: 0.99 }} className="w-full py-3 rounded-xl text-sm font-medium text-zinc-600 dark:text-zinc-300 transition-all flex items-center justify-center gap-2 mt-4 bg-white dark:bg-zinc-800 border border-[#e4e4e7] dark:border-zinc-700">
                    <GraduationCap size={16} /> Sign in as Guidance Counsellor
                  </MotionButton>
                </MotionDiv>
              ) : (
                <MotionDiv key="register-form" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.3 }}>
                  <h2 className="text-3xl font-semibold text-zinc-900 tracking-tight mb-8">Create your account</h2>
                  <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                      <label className="text-sm text-zinc-600 font-medium mb-1.5 block">Name</label>
                      <input type="text" value={name} onChange={e => { setName(e.target.value); setError(''); }} placeholder="Choose a username" className={inputClass} autoFocus />
                    </div>
                    <div>
                      <label className="text-sm text-zinc-600 font-medium mb-1.5 block">School</label>
                      <div className="relative">
                        <select value={school} onChange={e => { setSchool(e.target.value); setError(''); }} className={`${inputClass} appearance-none cursor-pointer ${!school ? 'text-zinc-400' : ''}`}>
                          <option value="" disabled>Select your school</option>
                          {SCHOOLS.map(s => (<option key={s.id} value={s.id}>{s.name}</option>))}
                        </select>
                        <School size={16} className="absolute right-3 top-1/2 -translate-y-1/2 text-zinc-400 pointer-events-none" />
                      </div>
                    </div>
                    <div>
                      <label className="text-sm text-zinc-600 font-medium mb-1.5 block">Choose your avatar</label>
                      <div className="grid grid-cols-4 gap-2">
                        {AVATAR_SEEDS.map(seed => (
                          <button key={seed} type="button" onClick={() => setAvatar(seed)} className={`rounded-xl aspect-square p-1 transition-all ${avatar === seed ? 'ring-2 ring-offset-1 ring-[#2A7D6F] bg-[#FAF7F4] dark:bg-zinc-900' : 'ring-1 ring-zinc-200 hover:ring-zinc-400 bg-white dark:bg-zinc-800'}`}>
                            <img src={getAvatarUrl(seed)} alt={seed} className="w-full h-full rounded-lg" />
                          </button>
                        ))}
                      </div>
                    </div>
                    <div>
                      <label className="text-sm text-zinc-600 font-medium mb-1.5 block">Password</label>
                      <div className="relative">
                        <input type={showPassword ? 'text' : 'password'} value={password} onChange={e => { setPassword(e.target.value); setError(''); }} placeholder="Create a password" className={inputClass} />
                        <button type="button" onClick={() => setShowPassword(!showPassword)} className="absolute right-3 top-1/2 -translate-y-1/2 text-zinc-400 hover:text-zinc-600 transition-colors">
                          {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                        </button>
                      </div>
                    </div>
                    <div>
                      <label className="text-sm text-zinc-600 font-medium mb-1.5 block">Confirm Password</label>
                      <div className="relative">
                        <input type={showConfirmPw ? 'text' : 'password'} value={confirmPassword} onChange={e => { setConfirmPassword(e.target.value); setError(''); }} placeholder="Confirm your password" className={inputClass} />
                        <button type="button" onClick={() => setShowConfirmPw(!showConfirmPw)} className="absolute right-3 top-1/2 -translate-y-1/2 text-zinc-400 hover:text-zinc-600 transition-colors">
                          {showConfirmPw ? <EyeOff size={16} /> : <Eye size={16} />}
                        </button>
                      </div>
                    </div>
                    <AnimatePresence>{error && <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="text-sm text-red-500 font-medium">{error}</MotionDiv>}</AnimatePresence>
                    <MotionButton type="submit" disabled={isLoading} whileHover={{ scale: 1.01 }} whileTap={{ scale: 0.99 }} className="w-full py-3 rounded-xl text-white text-sm font-semibold transition-all disabled:opacity-60 disabled:cursor-not-allowed" style={{ backgroundColor: '#2A7D6F' }}>
                      {isLoading ? 'Creating account...' : 'Create Account'}
                    </MotionButton>
                  </form>
                  <p className="text-sm text-zinc-400 text-center mt-6">Already have an account?{' '}<button type="button" onClick={() => { setAuthMode('login'); resetForm(); }} className="text-sm font-semibold transition-colors hover:opacity-80" style={{ color: '#2A7D6F' }}>Sign in</button></p>
                </MotionDiv>
              )}
            </AnimatePresence>
            <button onClick={() => handleLoginSuccess({ uid: 'dev-student', name: 'Dev User', avatar: 'Casper', isAdmin: false })} className="mt-10 mx-auto block px-3 py-1 bg-red-600/10 text-red-400 border border-red-600/20 rounded-full text-[9px] font-mono hover:bg-red-600/20 transition-colors">
              DEV: Skip Login
            </button>
          </div>
        </div>
      </MotionDiv>
    </div>
  );
};

export default LoginPage;
