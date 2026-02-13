/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, MouseEvent } from 'react';
import { createPortal } from 'react-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { X, ArrowRight, User as UserIcon, Key, Eye, EyeOff, Shield, User as StudentIcon, ArrowLeft, ChevronDown } from 'lucide-react';
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
  buttonLabel?: string;
  buttonClassName?: string;
  showChevron?: boolean;
  initialStep?: 'initial' | 'login' | 'create';
}

// 4 male-leaning, 4 female-leaning seeds for notionists-neutral
export const AVATAR_SEEDS = [
  'James', 'Marcus', 'Ravi', 'Tomek',
  'Aoife', 'Priya', 'Zara', 'Mei',
];

/** Build a DiceBear avatar URL from a seed. */
export function getAvatarUrl(seed: string): string {
  return `https://api.dicebear.com/9.x/notionists-neutral/svg?seed=${seed}&backgroundColor=b6e3f4,c0aede,d1d4f9,ffd5dc,ffdfbf`;
}

export const Auth: React.FC<AuthProps> = ({ onLoginSuccess, buttonLabel, buttonClassName, showChevron, initialStep }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownTimeout = React.useRef<ReturnType<typeof setTimeout> | null>(null);
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
  
  const openModal = (toStep: 'initial' | 'login' | 'create', loginAs?: 'choice' | 'student' | 'admin') => {
    setIsOpen(true);
    setStep(toStep);
    setLoginView(loginAs ?? 'choice');
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
    setDropdownOpen(false);
  };

  const handleOpen = () => openModal(initialStep ?? 'initial');

  const handleDropdownEnter = () => {
    if (dropdownTimeout.current) clearTimeout(dropdownTimeout.current);
    setDropdownOpen(true);
  };
  const handleDropdownLeave = () => {
    dropdownTimeout.current = setTimeout(() => setDropdownOpen(false), 150);
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

  const inputClass = "w-full bg-zinc-50 dark:bg-white/[0.05] border border-zinc-200/50 dark:border-white/[0.1] rounded-xl py-3 px-4 text-zinc-900 dark:text-white/90 text-sm font-sans placeholder:text-zinc-400 dark:placeholder:text-white/30 focus:outline-none focus:border-[#CC785C]/60 focus:ring-1 focus:ring-[#CC785C]/30 transition-colors";
  const inputWithIconClass = "w-full bg-zinc-50 dark:bg-white/[0.05] border border-zinc-200/50 dark:border-white/[0.1] rounded-xl py-3 pl-10 pr-4 text-zinc-900 dark:text-white/90 text-sm font-sans placeholder:text-zinc-400 dark:placeholder:text-white/30 focus:outline-none focus:border-[#CC785C]/60 focus:ring-1 focus:ring-[#CC785C]/30 transition-colors";
  const inputWithBothClass = "w-full bg-zinc-50 dark:bg-white/[0.05] border border-zinc-200/50 dark:border-white/[0.1] rounded-xl py-3 pl-10 pr-10 text-zinc-900 dark:text-white/90 text-sm font-sans placeholder:text-zinc-400 dark:placeholder:text-white/30 focus:outline-none focus:border-[#CC785C]/60 focus:ring-1 focus:ring-[#CC785C]/30 transition-colors";

  const renderLoginForm = (isAdmin: boolean) => (
     <MotionDiv
      key={isAdmin ? "admin-login" : "student-login"}
      variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={1}
      transition={{ duration: 0.3, ease: 'easeInOut' }}
      className="flex flex-col flex-grow justify-center"
    >
      <h2 className="font-sans text-2xl font-semibold text-zinc-900 dark:text-white/95 mb-1 tracking-tight">{isAdmin ? 'Admin login' : 'Welcome back'}</h2>
      <p className="text-zinc-500 dark:text-white/40 text-sm mb-8">{isAdmin ? 'Enter the admin password to continue.' : 'Sign in to pick up where you left off.'}</p>
      <form onSubmit={handleLogin} className="flex flex-col gap-3">
        {!isAdmin && <div className="relative">
          <UserIcon size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-zinc-400 dark:text-white/25" />
          <input type="text" value={loginName} onChange={(e) => setLoginName(e.target.value)} placeholder="Choose a username" className={inputWithIconClass} autoFocus/>
        </div>}
         <div className="relative">
          <Key size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-zinc-400 dark:text-white/25" />
          <input type={showLoginPassword ? "text" : "password"} value={loginPassword} onChange={(e) => setLoginPassword(e.target.value)} placeholder="Password" className={inputWithBothClass} autoFocus={isAdmin}/>
           <button type="button" onClick={() => setShowLoginPassword(!showLoginPassword)} className="absolute right-3.5 top-1/2 -translate-y-1/2 text-zinc-400 dark:text-white/25 hover:text-zinc-600 dark:hover:text-white/50 transition-colors" aria-label={showLoginPassword ? "Hide password" : "Show password"}>
              {showLoginPassword ? <EyeOff size={16} /> : <Eye size={16} />}
           </button>
        </div>
        <AnimatePresence>{error && (<MotionP initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="text-xs text-red-400/90 font-medium">{error}</MotionP>)}</AnimatePresence>
        <button type="submit" className="w-full bg-[#CC785C] text-white font-medium py-3 rounded-xl hover:bg-[#B56A50] transition-colors text-sm mt-1">Continue</button>
        <button type="button" onClick={() => setLoginView('choice')} className="flex items-center justify-center gap-1.5 text-sm text-zinc-400 dark:text-white/35 hover:text-zinc-600 dark:hover:text-white/60 w-full py-2 rounded-lg transition-colors mt-1">
          <ArrowLeft size={14} /> Back
        </button>
      </form>
    </MotionDiv>
  );

  return (
    <>
      {showChevron ? (
        <div className="relative" onMouseEnter={handleDropdownEnter} onMouseLeave={handleDropdownLeave}>
          <button onClick={handleOpen} className={buttonClassName ?? "px-5 py-2 text-sm font-medium bg-zinc-900/5 dark:bg-white/[0.08] text-zinc-700 dark:text-white/80 rounded-full hover:bg-zinc-900/10 dark:hover:bg-white/[0.12] hover:text-zinc-900 dark:hover:text-white transition-all border border-zinc-200/50 dark:border-white/[0.06]"}>
            <span className="flex items-center gap-0">
              <span className="pr-3.5">{buttonLabel ?? "Log in"}</span>
              <span className="border-l border-white/20 pl-3">
                <ChevronDown size={16} className={`transition-transform duration-300 ${dropdownOpen ? 'rotate-180' : ''}`} />
              </span>
            </span>
          </button>
          <AnimatePresence>
            {dropdownOpen && (
              <MotionDiv
                initial={{ opacity: 0, y: -4, scale: 0.96 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: -4, scale: 0.96 }}
                transition={{ duration: 0.15, ease: [0.16, 1, 0.3, 1] }}
                className="absolute top-full right-0 mt-2 w-52 bg-white dark:bg-zinc-900 border border-zinc-200/60 dark:border-white/[0.08] rounded-xl shadow-lg shadow-black/[0.08] dark:shadow-black/40 overflow-hidden py-1"
              >
                <button onClick={() => openModal('login', 'student')} className="w-full text-left px-4 py-2.5 text-sm text-zinc-700 dark:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-white/[0.06] transition-colors font-medium">Student login</button>
                <button onClick={() => openModal('create')} className="w-full text-left px-4 py-2.5 text-sm text-zinc-700 dark:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-white/[0.06] transition-colors font-medium">Create account</button>
                <div className="border-t border-zinc-100 dark:border-white/[0.06] my-1" />
                <button onClick={() => openModal('login', 'admin')} className="w-full text-left px-4 py-2.5 text-sm text-zinc-400 dark:text-zinc-500 hover:bg-zinc-100 dark:hover:bg-white/[0.06] transition-colors">Admin login</button>
              </MotionDiv>
            )}
          </AnimatePresence>
        </div>
      ) : (
        <button onClick={handleOpen} className={buttonClassName ?? "px-5 py-2 text-sm font-medium bg-zinc-900/5 dark:bg-white/[0.08] text-zinc-700 dark:text-white/80 rounded-full hover:bg-zinc-900/10 dark:hover:bg-white/[0.12] hover:text-zinc-900 dark:hover:text-white transition-all border border-zinc-200/50 dark:border-white/[0.06]"}>
          {buttonLabel ?? "Log in"}
        </button>
      )}

      {createPortal(<AnimatePresence>
        {isOpen && (
          <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="fixed inset-0 bg-black/60 flex items-center justify-center z-[200] p-4" onClick={handleClose}>
            <MotionDiv initial={{ scale: 0.96, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} exit={{ scale: 0.96, opacity: 0 }} transition={{ duration: 0.2, ease: [0.16, 1, 0.3, 1] }} className="relative bg-white dark:bg-zinc-900 border border-zinc-200/50 dark:border-white/[0.08] rounded-2xl w-full max-w-sm shadow-[0_24px_64px_rgba(0,0,0,0.12)] dark:shadow-[0_24px_64px_rgba(0,0,0,0.5)] overflow-hidden" onClick={(e: MouseEvent<HTMLDivElement>) => e.stopPropagation()}>
              <button onClick={handleClose} className="absolute top-5 right-5 text-zinc-400 dark:text-white/25 hover:text-zinc-600 dark:hover:text-white/50 transition-colors z-10"><X size={18} /></button>

              <div className="p-8 min-h-[22rem] flex flex-col">
                <AnimatePresence mode="wait">
                  {step === 'initial' && (
                    <MotionDiv key="initial" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={1} transition={{ duration: 0.3, ease: 'easeInOut' }} className="flex flex-col flex-grow justify-center">
                      <h2 className="font-sans text-2xl font-semibold text-zinc-900 dark:text-white/95 mb-2 text-center tracking-tight">Welcome</h2>
                      <p className="text-zinc-500 dark:text-white/40 text-sm text-center mb-8">Get started with NextStepUni</p>
                      <div className="space-y-3">
                         <button onClick={() => { setStep('login'); setLoginView('choice'); setError(''); }} className="w-full text-left p-4 rounded-xl bg-zinc-50 dark:bg-white/[0.04] hover:bg-zinc-100 dark:hover:bg-white/[0.07] transition-all border border-zinc-200/50 dark:border-white/[0.08] hover:border-zinc-300 dark:hover:border-white/[0.15] group">
                           <p className="font-medium text-zinc-900 dark:text-white/90 text-sm">I have an account</p>
                           <p className="text-xs text-zinc-500 dark:text-white/35 mt-0.5">Log in with your username.</p>
                         </button>
                         <button onClick={() => setStep('create')} className="w-full text-left p-4 rounded-xl bg-zinc-50 dark:bg-white/[0.04] hover:bg-zinc-100 dark:hover:bg-white/[0.07] transition-all border border-zinc-200/50 dark:border-white/[0.08] hover:border-zinc-300 dark:hover:border-white/[0.15] group">
                           <p className="font-medium text-zinc-900 dark:text-white/90 text-sm">Create a new account</p>
                           <p className="text-xs text-zinc-500 dark:text-white/35 mt-0.5">Get started and save your progress.</p>
                         </button>
                      </div>
                    </MotionDiv>
                  )}

                  {step === 'login' && (
                    loginView === 'choice' ? (
                      <MotionDiv key="login-choice" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={-1} transition={{ duration: 0.3, ease: 'easeInOut' }} className="flex flex-col flex-grow justify-center">
                        <h2 className="font-sans text-2xl font-semibold text-zinc-900 dark:text-white/95 mb-2 text-center tracking-tight">Log in as</h2>
                        <p className="text-zinc-500 dark:text-white/40 text-sm text-center mb-8">Choose your account type</p>
                        <div className="space-y-3">
                           <button onClick={() => setLoginView('student')} className="w-full flex items-center gap-4 p-4 rounded-xl bg-zinc-50 dark:bg-white/[0.04] hover:bg-zinc-100 dark:hover:bg-white/[0.07] transition-all border border-zinc-200/50 dark:border-white/[0.08] hover:border-zinc-300 dark:hover:border-white/[0.15]">
                             <div className="w-10 h-10 rounded-xl bg-[#CC785C]/10 flex items-center justify-center flex-shrink-0"><StudentIcon size={20} className="text-[#CC785C]"/></div>
                             <div className="text-left"><p className="font-medium text-zinc-900 dark:text-white/90 text-sm">Student</p><p className="text-xs text-zinc-500 dark:text-white/35 mt-0.5">Access your modules and progress.</p></div>
                           </button>
                           <button onClick={() => setLoginView('admin')} className="w-full flex items-center gap-4 p-4 rounded-xl bg-zinc-50 dark:bg-white/[0.04] hover:bg-zinc-100 dark:hover:bg-white/[0.07] transition-all border border-zinc-200/50 dark:border-white/[0.08] hover:border-zinc-300 dark:hover:border-white/[0.15]">
                             <div className="w-10 h-10 rounded-xl bg-zinc-100 dark:bg-white/[0.06] flex items-center justify-center flex-shrink-0"><Shield size={20} className="text-zinc-400 dark:text-white/40"/></div>
                             <div className="text-left"><p className="font-medium text-zinc-900 dark:text-white/90 text-sm">Admin</p><p className="text-xs text-zinc-500 dark:text-white/35 mt-0.5">View student dashboard.</p></div>
                           </button>
                        </div>
                        <button type="button" onClick={() => setStep('initial')} className="flex items-center justify-center gap-1.5 text-sm text-zinc-400 dark:text-white/35 hover:text-zinc-600 dark:hover:text-white/60 mt-8 w-full py-2 rounded-lg transition-colors">
                          <ArrowLeft size={14} /> Back
                        </button>
                      </MotionDiv>
                    ) : loginView === 'student' ? renderLoginForm(false) : renderLoginForm(true)
                  )}

                  {step === 'create' && (
                    <MotionDiv key="create" variants={stepVariants} initial="hidden" animate="visible" exit="exit" custom={-1} transition={{ duration: 0.3, ease: 'easeInOut' }} className="flex flex-col flex-grow">
                      <h2 className="font-sans text-2xl font-semibold text-zinc-900 dark:text-white/95 mb-1 tracking-tight">Create account</h2>
                      <p className="text-zinc-500 dark:text-white/40 text-sm mb-6">Set up your profile to get started.</p>
                      <form onSubmit={handleCreate} className="flex flex-col flex-grow gap-3">
                        <div className="relative">
                          <UserIcon size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-zinc-400 dark:text-white/25" />
                          <input type="text" value={createName} onChange={(e) => { setCreateName(e.target.value); setError(''); }} placeholder="Choose a username" className={inputWithIconClass} autoFocus/>
                        </div>
                        <div className="relative">
                          <Key size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-zinc-400 dark:text-white/25" />
                          <input type={showCreatePassword ? "text" : "password"} value={createPassword} onChange={(e) => { setCreatePassword(e.target.value); setError(''); }} placeholder="Password" className={inputWithBothClass} />
                          <button type="button" onClick={() => setShowCreatePassword(!showCreatePassword)} className="absolute right-3.5 top-1/2 -translate-y-1/2 text-zinc-400 dark:text-white/25 hover:text-zinc-600 dark:hover:text-white/50 transition-colors" aria-label={showCreatePassword ? "Hide password" : "Show password"}>{showCreatePassword ? <EyeOff size={16} /> : <Eye size={16} />}</button>
                        </div>
                        <div className="relative">
                          <Key size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-zinc-400 dark:text-white/25" />
                          <input type={showConfirmPassword ? "text" : "password"} value={confirmPassword} onChange={(e) => { setConfirmPassword(e.target.value); setError(''); }} placeholder="Confirm password" className={inputWithBothClass} />
                          <button type="button" onClick={() => setShowConfirmPassword(!showConfirmPassword)} className="absolute right-3.5 top-1/2 -translate-y-1/2 text-zinc-400 dark:text-white/25 hover:text-zinc-600 dark:hover:text-white/50 transition-colors" aria-label={showConfirmPassword ? "Hide password" : "Show password"}>{showConfirmPassword ? <EyeOff size={16} /> : <Eye size={16} />}</button>
                        </div>
                        <p className="text-xs text-zinc-500 dark:text-white/35 mt-3 font-medium uppercase tracking-widest">Choose your avatar</p>
                        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
                          {AVATAR_SEEDS.map((seed) => (<MotionButton key={seed} type="button" onClick={() => setSelectedAvatar(seed)} className={`rounded-xl aspect-square p-1.5 transition-all ${selectedAvatar === seed ? 'ring-2 ring-[#CC785C] bg-[#CC785C]/10' : 'bg-zinc-50 dark:bg-white/[0.04] ring-1 ring-zinc-200 dark:ring-white/[0.06] hover:ring-zinc-300 dark:hover:ring-white/[0.15]'}`} whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}><img src={getAvatarUrl(seed)} alt="Avatar" className="w-full h-full rounded-lg"/></MotionButton>))}
                        </div>
                        <AnimatePresence>{error && (<MotionP initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="text-xs text-red-400/90 font-medium mt-1">{error}</MotionP>)}</AnimatePresence>
                        <button type="submit" disabled={!isProfileComplete} className="w-full bg-[#CC785C] text-white font-medium py-3 mt-auto rounded-xl hover:bg-[#B56A50] transition-colors text-sm disabled:bg-zinc-100 dark:disabled:bg-white/[0.06] disabled:text-zinc-400 dark:disabled:text-white/20 disabled:cursor-not-allowed">Create account</button>
                        <button type="button" onClick={() => setStep('initial')} className="flex items-center justify-center gap-1.5 text-sm text-zinc-400 dark:text-white/35 hover:text-zinc-600 dark:hover:text-white/60 mt-1 w-full py-2 rounded-lg transition-colors">
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
      </AnimatePresence>, document.body)}
    </>
  );
};
