/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, MouseEvent } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, ArrowRight, User as UserIcon, Key, Eye, EyeOff, Shield, User as StudentIcon, ArrowLeft } from 'lucide-react';
import { auth, db } from '../firebase';
import { createUserWithEmailAndPassword, signInWithEmailAndPassword } from 'firebase/auth';
import { doc, setDoc, getDoc } from 'firebase/firestore';

// FIX: Cast motion components to any to bypass broken type definitions
const MotionDiv = motion.div as any;
const MotionP = motion.p as any;
const MotionButton = motion.button as any;


// This represents the user session object passed to the main app.
export type SessionUser = {
  uid: string;
  name: string;
  avatar: string;
  isAdmin?: boolean;
};

interface AuthProps {
  onLoginSuccess: (user: SessionUser) => void;
}

const AVATAR_SEEDS = [
  'Casper', 'Midnight', 'Bandit', 'Leo', 'Misty', 'Felix'
];

export const Auth: React.FC<AuthProps> = ({ onLoginSuccess }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [step, setStep] = useState<'initial' | 'login' | 'create'>('initial');
  const [loginView, setLoginView] = useState<'choice' | 'student' | 'admin'>('choice');
  const [error, setError] = useState('');
  
  // Login state
  const [loginName, setLoginName] = useState('');
  const [loginPassword, setLoginPassword] = useState('');
  const [showLoginPassword, setShowLoginPassword] = useState(false);

  // Create state
  const [createName, setCreateName] = useState('');
  const [createPassword, setCreatePassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [selectedAvatar, setSelectedAvatar] = useState('');
  const [showCreatePassword, setShowCreatePassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  
  const handleOpen = () => {
    setIsOpen(true);
    setStep('initial');
    setLoginView('choice');
    setError('');
    setLoginName('');
    setLoginPassword('');
    setCreateName('');
    setCreatePassword('');
    setConfirmPassword('');
    setSelectedAvatar('');
    setShowLoginPassword(false);
    setShowCreatePassword(false);
    setShowConfirmPassword(false);
  };

  const handleClose = () => {
    setIsOpen(false);
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (loginView === 'admin') {
      try {
        await signInWithEmailAndPassword(auth, 'admin@nextstep.app', loginPassword);
        // onLoginSuccess will be triggered by onAuthStateChanged in App.tsx
        handleClose();
      } catch (error: any) {
        setError("Invalid admin credentials.");
      }
      return;
    }

    if (!loginName.trim() || !loginPassword.trim()) {
      setError("Please enter your username and password.");
      return;
    }
    
    try {
      // Firebase Auth uses email for login, so we'll create a fake email from the username.
      const email = `${loginName.trim().toLowerCase()}@nextstep.app`;
      await signInWithEmailAndPassword(auth, email, loginPassword);
      // onLoginSuccess will be triggered by onAuthStateChanged in App.tsx
      handleClose();
    } catch (error: any) {
      setError("Invalid username or password.");
    }
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    if (!createName.trim() || !selectedAvatar || !createPassword) {
      setError("Please fill out all fields.");
      return;
    }
    if (createPassword !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }
    
    try {
        const email = `${createName.trim().toLowerCase()}@nextstep.app`;
        const userCredential = await createUserWithEmailAndPassword(auth, email, createPassword);
        const user = userCredential.user;

        // Create a corresponding user profile document in Firestore
        await setDoc(doc(db, "users", user.uid), {
            name: createName.trim(),
            avatar: selectedAvatar,
            isAdmin: false,
        });

        // onLoginSuccess will be triggered by onAuthStateChanged in App.tsx
        handleClose();
    } catch (error: any) {
        if (error.code === 'auth/email-already-in-use') {
            setError("This username is already taken.");
        } else if (error.code === 'auth/weak-password') {
            setError("Password should be at least 6 characters.");
        } else {
            setError("Failed to create account. Please try again.");
        }
    }
  };

  const isProfileComplete = createName.trim() !== '' && selectedAvatar !== '' && createPassword !== '' && createPassword === confirmPassword;

  const stepVariants = {
    hidden: (direction: number) => ({ opacity: 0, x: direction > 0 ? 50 : -50 }),
    visible: { opacity: 1, x: 0 },
    exit: (direction: number) => ({ opacity: 0, x: direction > 0 ? -50 : 50 }),
  };

  const renderLoginForm = (isAdmin: boolean) => (
     <MotionDiv
      key={isAdmin ? "admin-login" : "student-login"}
      variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={1}
      transition={{ duration: 0.3, ease: 'easeInOut' }}
      className="flex flex-col flex-grow justify-center"
    >
      <h2 className="font-serif text-3xl font-bold text-white mb-2 italic">{isAdmin ? 'Admin Log In' : 'Student Log In'}</h2>
      <p className="text-stone-400 mb-6">Enter your credentials to continue.</p>
      <form onSubmit={handleLogin} className="flex flex-col gap-4">
        <div className="relative">
          <UserIcon size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-stone-500" />
          <input type="text" value={loginName} onChange={(e) => setLoginName(e.target.value)} placeholder={isAdmin ? 'Admin Username (hidden)' : 'Username'} className="w-full bg-stone-800/50 border border-stone-700 rounded-lg py-2 pl-9 pr-3 text-white focus:outline-none focus:ring-2 focus:ring-purple-500" autoFocus/>
        </div>
         <div className="relative">
          <Key size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-stone-500" />
          <input type={showLoginPassword ? "text" : "password"} value={loginPassword} onChange={(e) => setLoginPassword(e.target.value)} placeholder="Password" className="w-full bg-stone-800/50 border border-stone-700 rounded-lg py-2 pl-9 pr-10 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"/>
           <button type="button" onClick={() => setShowLoginPassword(!showLoginPassword)} className="absolute right-3 top-1/2 -translate-y-1/2 text-stone-500 hover:text-white" aria-label={showLoginPassword ? "Hide password" : "Show password"}>
              {showLoginPassword ? <EyeOff size={16} /> : <Eye size={16} />}
           </button>
        </div>
        <AnimatePresence>{error && (<MotionP initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="text-xs text-red-400">{error}</MotionP>)}</AnimatePresence>
        <button type="submit" className="w-full bg-purple-600 text-white font-bold py-2 rounded-lg hover:bg-purple-500 transition-colors flex items-center justify-center gap-2">Log In <ArrowRight size={16} /></button>
        <button type="button" onClick={() => setLoginView('choice')} className="flex items-center justify-center gap-2 text-xs text-center text-stone-400 hover:text-white hover:bg-white/10 w-full py-2 rounded-lg transition-colors">
          <ArrowLeft size={14} /> Back
        </button>
      </form>
    </MotionDiv>
  );

  return (
    <>
      <button onClick={handleOpen} className="px-4 py-2 text-sm font-bold bg-stone-800 text-white rounded-full hover:bg-stone-700 transition-colors dark:bg-white dark:text-black dark:hover:bg-stone-200">
        Log In
      </button>

      <AnimatePresence>
        {isOpen && (
          <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-[200] p-4" onClick={handleClose}>
            <MotionDiv initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} exit={{ scale: 0.9, opacity: 0 }} className="relative bg-stone-900/80 backdrop-blur-2xl border border-white/10 rounded-2xl w-full max-w-xs shadow-2xl dark:shadow-[0_25px_50px_-12px_rgba(0,0,0,0.5),0_0px_25px_rgba(168,85,247,0.1)] overflow-hidden" onClick={(e: MouseEvent<HTMLDivElement>) => e.stopPropagation()}>
              <button onClick={handleClose} className="absolute top-4 right-4 text-stone-500 hover:text-white transition-colors z-10"><X size={20} /></button>

              <div className="p-6 min-h-[22rem] flex flex-col">
                <AnimatePresence mode="wait">
                  {step === 'initial' && (
                    <MotionDiv key="initial" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={1} transition={{ duration: 0.3, ease: 'easeInOut' }} className="flex flex-col flex-grow justify-center">
                      <h2 className="font-serif text-3xl font-bold text-white mb-6 text-center italic">Welcome</h2>
                      <div className="space-y-3">
                         <button onClick={() => { setStep('login'); setLoginView('choice'); setError(''); }} className="w-full text-left p-4 rounded-xl bg-white/10 hover:bg-white/20 transition-all border border-transparent hover:border-purple-500/30"><p className="font-bold text-white">I have an account</p><p className="text-xs text-stone-400">Log in with your username.</p></button>
                         <button onClick={() => setStep('create')} className="w-full text-left p-4 rounded-xl bg-white/10 hover:bg-white/20 transition-all border border-transparent hover:border-purple-500/30"><p className="font-bold text-white">Create a new account</p><p className="text-xs text-stone-400">Get started and save your progress.</p></button>
                      </div>
                    </MotionDiv>
                  )}
                  
                  {step === 'login' && (
                    loginView === 'choice' ? (
                      <MotionDiv key="login-choice" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={-1} transition={{ duration: 0.3, ease: 'easeInOut' }} className="flex flex-col flex-grow justify-center">
                        <h2 className="font-serif text-3xl font-bold text-white mb-6 text-center italic">Log In As...</h2>
                        <div className="space-y-3">
                           <button onClick={() => setLoginView('student')} className="w-full flex items-center gap-4 p-4 rounded-xl bg-white/10 hover:bg-white/20 transition-all border border-transparent hover:border-purple-500/30"><StudentIcon size={24} className="text-purple-400 drop-shadow-[0_0_8px_rgba(192,132,252,0.4)]"/><div className="text-left"><p className="font-bold text-white">Student</p><p className="text-xs text-stone-400">Access your modules and progress.</p></div></button>
                           <button onClick={() => setLoginView('admin')} className="w-full flex items-center gap-4 p-4 rounded-xl bg-white/10 hover:bg-white/20 transition-all border border-transparent hover:border-purple-500/30"><Shield size={24} className="text-purple-400 drop-shadow-[0_0_8px_rgba(192,132,252,0.4)]"/><div className="text-left"><p className="font-bold text-white">Admin</p><p className="text-xs text-stone-400">View student dashboard.</p></div></button>
                        </div>
                        <button type="button" onClick={() => setStep('initial')} className="flex items-center justify-center gap-2 text-xs text-center text-stone-400 hover:text-white mt-8 hover:bg-white/10 w-full py-2 rounded-lg transition-colors">
                          <ArrowLeft size={14} /> Back
                        </button>
                      </MotionDiv>
                    ) : loginView === 'student' ? renderLoginForm(false) : renderLoginForm(true)
                  )}

                  {step === 'create' && (
                    <MotionDiv key="create" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={-1} transition={{ duration: 0.3, ease: 'easeInOut' }} className="flex flex-col flex-grow">
                      <h2 className="font-serif text-3xl font-bold text-white mb-2 italic">Create Account</h2>
                      <p className="text-stone-400 mb-6">Create your profile to enter the lab.</p>
                      <form onSubmit={handleCreate} className="flex flex-col flex-grow gap-3">
                        <div className="relative"><UserIcon size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-stone-500" /><input type="text" value={createName} onChange={(e) => { setCreateName(e.target.value); setError(''); }} placeholder="Enter your username" className="w-full bg-stone-800/50 border border-stone-700 rounded-lg py-2 pl-9 pr-3 text-white focus:outline-none focus:ring-2 focus:ring-purple-500" autoFocus/></div>
                        <div className="relative"><Key size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-stone-500" /><input type={showCreatePassword ? "text" : "password"} value={createPassword} onChange={(e) => { setCreatePassword(e.target.value); setError(''); }} placeholder="Password" className="w-full bg-stone-800/50 border border-stone-700 rounded-lg py-2 pl-9 pr-10 text-white focus:outline-none focus:ring-2 focus:ring-purple-500" /><button type="button" onClick={() => setShowCreatePassword(!showCreatePassword)} className="absolute right-3 top-1/2 -translate-y-1/2 text-stone-500 hover:text-white" aria-label={showCreatePassword ? "Hide password" : "Show password"}>{showCreatePassword ? <EyeOff size={16} /> : <Eye size={16} />}</button></div>
                        <div className="relative"><Key size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-stone-500" /><input type={showConfirmPassword ? "text" : "password"} value={confirmPassword} onChange={(e) => { setConfirmPassword(e.target.value); setError(''); }} placeholder="Confirm Password" className="w-full bg-stone-800/50 border border-stone-700 rounded-lg py-2 pl-9 pr-10 text-white focus:outline-none focus:ring-2 focus:ring-purple-500" /><button type="button" onClick={() => setShowConfirmPassword(!showConfirmPassword)} className="absolute right-3 top-1/2 -translate-y-1/2 text-stone-500 hover:text-white" aria-label={showConfirmPassword ? "Hide password" : "Show password"}>{showConfirmPassword ? <EyeOff size={16} /> : <Eye size={16} />}</button></div>
                        <p className="text-xs text-stone-400 mt-2 font-bold uppercase tracking-wider">Choose your avatar</p>
                        <div className="grid grid-cols-6 gap-2">
                          {AVATAR_SEEDS.map((seed) => (<MotionButton key={seed} type="button" onClick={() => setSelectedAvatar(seed)} className={`rounded-lg aspect-square p-1 bg-stone-800/50 transition-all ${selectedAvatar === seed ? 'ring-2 ring-purple-500' : 'ring-1 ring-transparent hover:ring-purple-500/50'}`} whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}><img src={`https://api.dicebear.com/7.x/adventurer/svg?seed=${seed}`} alt="Avatar" className="w-full h-full"/></MotionButton>))}
                        </div>
                        <AnimatePresence>{error && (<MotionP initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="text-xs text-red-400 mt-2">{error}</MotionP>)}</AnimatePresence>
                        <button type="submit" disabled={!isProfileComplete} className="w-full bg-purple-600 text-white font-bold py-2 mt-auto rounded-lg hover:bg-purple-500 transition-colors disabled:bg-stone-700 disabled:opacity-50 disabled:cursor-not-allowed">Enter Application</button>
                        <button type="button" onClick={() => setStep('initial')} className="flex items-center justify-center gap-2 text-xs text-center text-stone-400 hover:text-white mt-2 hover:bg-white/10 w-full py-2 rounded-lg transition-colors">
                          <ArrowLeft size={14} /> Back
                        </button>
                      </form>
                    </MotionDiv>
                  )}
                </AnimatePresence>
              </div>
            </MotionDiv>
          </MotionDiv>
        )}
      </AnimatePresence>
    </>
  );
};
