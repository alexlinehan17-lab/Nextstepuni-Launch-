/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * ResetPasswordPage — the `mode=resetPassword` branch of AuthActionPage, which
 * owns the Firebase action URL (see utils/authActionLink.ts).
 *
 * Flow:
 *   1. Parse oobCode from URL
 *   2. checkActionCode → must be a PASSWORD_RESET code; returns the email
 *   3. Show new-password form
 *   4. confirmPasswordReset, briefly authenticate with the new credential,
 *      and advance the server-side Firestore session cutoff
 *   5. Sign out and return to sign-in
 */

import React, { useEffect, useState } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionButton, MotionDiv } from './Motion';
import { Eye, EyeOff, Check } from 'lucide-react';
import app, { auth } from '../firebase';
import { ActionCodeOperation, checkActionCode, confirmPasswordReset, sendPasswordResetEmail, signInWithEmailAndPassword, signOut } from 'firebase/auth';
import { getFunctions, httpsCallable } from 'firebase/functions';
import { COLORS } from '../design/tokens';
import { MAX_PASSWORD_LENGTH, MIN_PASSWORD_LENGTH, passwordLengthError } from '../utils/passwordPolicy';
import { clearLocalSessionData } from '../utils/sessionPrivacy';
import {
  AuthActionCard,
  AuthActionProblem,
  AuthActionProgress,
  AuthActionSuccess,
  SPRING_FAST,
  SPRING_GENTLE,
  btnHover,
  btnTap,
  primaryBtn,
  primaryBtnStyle,
} from './AuthActionCard';

const errorAnim = {
  initial: { opacity: 0, y: -6, scale: 0.96 },
  animate: { opacity: 1, y: 0, scale: 1 },
  exit: { opacity: 0, y: -4, scale: 0.96 },
  transition: SPRING_FAST,
};

type Stage = 'verifying' | 'ready' | 'invalid' | 'submitting' | 'done';

const inputClass = "w-full py-3.5 px-4 rounded-xl text-sm font-sans text-zinc-800 placeholder-zinc-400 outline-none transition-all bg-white border-2 border-zinc-200 focus:border-[#F26B1F]";

/**
 * Each new reset request cancels the previous link, so a student who tapped
 * Resend and then opened the first email landed here with a dead link
 * (reproduced 2026-10-15). Let them send a fresh one without going back.
 */
const ResendResetLink: React.FC = () => {
  const [email, setEmail] = useState('');
  const [state, setState] = useState<'idle' | 'sending' | 'sent' | 'error'>('idle');
  const send = async () => {
    const value = email.trim().toLowerCase();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value) || value.endsWith('@nextstep.app')) {
      setState('error');
      return;
    }
    setState('sending');
    try {
      await sendPasswordResetEmail(auth, value);
      setState('sent');
    } catch {
      setState('error');
    }
  };
  if (state === 'sent') {
    return (
      <p role="status" className="text-sm mb-6 font-medium" style={{ color: '#1a1a1a' }}>
        Sent. Open the newest email from NextStepUni. It can take a few minutes to arrive, so check junk too.
      </p>
    );
  }
  return (
    <form onSubmit={e => { e.preventDefault(); void send(); }} className="mb-4 space-y-3" noValidate>
      <label htmlFor="resend-reset-email" className="text-xs font-bold uppercase tracking-wider block" style={{ color: '#9e9186' }}>Send a new link</label>
      <input
        id="resend-reset-email"
        type="email"
        inputMode="email"
        autoComplete="email"
        value={email}
        onChange={e => { setEmail(e.target.value); if (state === 'error') setState('idle'); }}
        placeholder="The email you sign in with"
        className={inputClass}
        aria-invalid={state === 'error'}
        aria-describedby={state === 'error' ? 'resend-reset-error' : undefined}
      />
      {state === 'error' && (
        <p id="resend-reset-error" className="text-sm text-red-500 font-medium">
          Check the email address and try again.
        </p>
      )}
      <button
        type="submit"
        disabled={state === 'sending' || !email.trim()}
        className="w-full py-3 rounded-xl text-sm font-semibold border-2 border-[#1A1A1A] bg-white text-[#1A1A1A] disabled:opacity-40"
      >
        {state === 'sending' ? 'Sending…' : 'Send me a new link'}
      </button>
    </form>
  );
};

const ResetPasswordPage: React.FC = () => {
  const params = new URLSearchParams(window.location.search);
  const oobCode = params.get('oobCode');

  const [stage, setStage] = useState<Stage>('verifying');
  const [email, setEmail] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [securityNotice, setSecurityNotice] = useState('');
  // A replaced, used or expired code: the student can send a fresh link here.
  const [canResend, setCanResend] = useState(false);

  useEffect(() => {
    if (!oobCode) {
      setStage('invalid');
      setError('This reset link is missing required information.');
      return;
    }
    (async () => {
      try {
        // verifyPasswordResetCode accepts ANY live action code (it returns the
        // email for a verify-email code too), which showed students a
        // "Set a new password" form for a link that could never reset it.
        const info = await checkActionCode(auth, oobCode);
        if (info.operation !== ActionCodeOperation.PASSWORD_RESET || !info.data.email) {
          setStage('invalid');
          setError('This isn\u2019t a password reset link. To reset your password, use Forgot password on the sign-in page.');
          return;
        }
        setEmail(info.data.email);
        setStage('ready');
      } catch (err: any) {
        console.error('Password reset code verification failed:', err);
        setStage('invalid');
        if (err.code === 'auth/expired-action-code') {
          setCanResend(true);
          setError('This reset link has expired. Links last an hour, so send yourself a new one.');
        } else if (err.code === 'auth/invalid-action-code') {
          setCanResend(true);
          setError('A newer reset email replaced this link, or it has already been used. Open the newest email from NextStepUni, or send yourself a new link.');
        } else {
          setError('Could not verify this reset link. Try requesting a new one.');
        }
      }
    })();
  }, [oobCode]);

  const handleSubmit = async () => {
    const validationError = passwordLengthError(newPassword);
    if (validationError) {
      setError(validationError);
      return;
    }
    if (!oobCode) return;
    setStage('submitting');
    setError('');
    setSecurityNotice('');
    let passwordWasUpdated = false;
    try {
      await confirmPasswordReset(auth, oobCode, newPassword);
      passwordWasUpdated = true;
      // Obtain a new-session token without ever sending the password to our
      // backend. The callable records a Firestore auth_time cutoff so stolen
      // pre-reset ID tokens stop working immediately, then revokes refresh
      // tokens; this page signs the temporary session back out.
      await signInWithEmailAndPassword(auth, email, newPassword);
      const finalize = httpsCallable<unknown, { success: boolean }>(
        getFunctions(app),
        'finalizeSelfServicePasswordReset',
      );
      try {
        await finalize({});
      } finally {
        await signOut(auth).catch(() => {});
        await clearLocalSessionData();
      }
      setNewPassword('');
      setStage('done');
    } catch (err: any) {
      console.error('Password reset failed:', err);
      if (passwordWasUpdated) {
        await signOut(auth).catch(() => {});
        await clearLocalSessionData();
        setNewPassword('');
        setSecurityNotice('Your password changed, but we could not confirm that every older session was closed. Contact support before using a shared device.');
        setStage('done');
        return;
      }
      setStage('ready');
      if (err.code === 'auth/weak-password') {
        setError('Password is too weak. Try a longer one.');
      } else if (err.code === 'auth/expired-action-code' || err.code === 'auth/invalid-action-code') {
        setError(err.code === 'auth/expired-action-code'
          ? 'This reset link has expired. Links last an hour, so send yourself a new one.'
          : 'A newer reset email replaced this link, or it has already been used. Open the newest email from NextStepUni, or send yourself a new link.');
        setCanResend(true);
        setStage('invalid');
      } else {
        setError('Could not reset your password. Try again.');
      }
    }
  };

  return (
    <AuthActionCard>
      {stage === 'verifying' && <AuthActionProgress label="Verifying your reset link…" />}

      {stage === 'invalid' && (
        <AuthActionProblem title={'This link doesn\u2019t work'} message={error}>
          {canResend && <ResendResetLink />}
        </AuthActionProblem>
      )}

      {(stage === 'ready' || stage === 'submitting') && (
        <MotionDiv initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={SPRING_GENTLE}>
          <h2 className="text-2xl font-semibold tracking-tight mb-1" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>Set a new password</h2>
          <p className="text-sm mb-8" style={{ color: '#7a7068' }}>For <span className="font-medium" style={{ color: '#1a1a1a' }}>{email}</span></p>
          <form onSubmit={e => { e.preventDefault(); handleSubmit(); }} className="space-y-4">
            <div>
              <label className="text-xs font-bold uppercase tracking-wider mb-1.5 block" style={{ color: '#9e9186' }}>New password</label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={newPassword}
                  onChange={e => { setNewPassword(e.target.value); setError(''); }}
                  placeholder={`At least ${MIN_PASSWORD_LENGTH} characters`}
                  minLength={MIN_PASSWORD_LENGTH}
                  maxLength={MAX_PASSWORD_LENGTH}
                  className={inputClass}
                  autoFocus
                />
                <button type="button" onClick={() => setShowPassword(!showPassword)} aria-label={showPassword ? 'Hide password' : 'Show password'} aria-pressed={showPassword} className="absolute right-3 top-1/2 -translate-y-1/2 transition-colors" style={{ color: '#9e9186' }}>
                  {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
              {newPassword.length > 0 && newPassword.length < MIN_PASSWORD_LENGTH && (
                <p className="text-xs mt-1.5" style={{ color: '#9e9186' }}>{MIN_PASSWORD_LENGTH - newPassword.length} more character{MIN_PASSWORD_LENGTH - newPassword.length !== 1 ? 's' : ''} needed</p>
              )}
              {newPassword.length >= MIN_PASSWORD_LENGTH && newPassword.length <= MAX_PASSWORD_LENGTH && (
                <p className="text-xs mt-1.5 flex items-center gap-1" style={{ color: COLORS.success }}><Check size={12} /> Looks good</p>
              )}
            </div>
            <AnimatePresence>
              {error && <MotionDiv {...errorAnim} className="text-sm text-red-500 font-medium">{error}</MotionDiv>}
            </AnimatePresence>
            <MotionButton
              type="submit"
              disabled={stage === 'submitting' || passwordLengthError(newPassword) !== null}
              whileHover={btnHover}
              whileTap={btnTap}
              transition={SPRING_FAST}
              className={primaryBtn}
              style={primaryBtnStyle}
            >
              {stage === 'submitting' ? 'Saving…' : 'Set password'}
            </MotionButton>
          </form>
        </MotionDiv>
      )}

      {stage === 'done' && (
        <AuthActionSuccess
          title="Password updated"
          message="You can now sign in with your new password."
          notice={securityNotice || undefined}
        />
      )}
    </AuthActionCard>
  );
};

export default ResetPasswordPage;
