/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * ResetPasswordPage — landing page for the Firebase password-reset email link.
 *
 * Configured via Firebase Console → Authentication → Templates → Password
 * reset → Action URL. Should point to https://<domain>/reset-password.
 * Firebase appends `?mode=resetPassword&oobCode=…&apiKey=…&lang=en` to
 * the URL.
 *
 * Flow:
 *   1. Parse oobCode from URL
 *   2. Verify code via verifyPasswordResetCode → returns email
 *   3. Show new-password form
 *   4. confirmPasswordReset, briefly authenticate with the new credential,
 *      and advance the server-side Firestore session cutoff
 *   5. Sign out and return to sign-in
 */

import React, { useEffect, useState } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionButton, MotionDiv } from './Motion';
import { Eye, EyeOff, Check, AlertTriangle } from 'lucide-react';
import app, { auth } from '../firebase';
import { verifyPasswordResetCode, confirmPasswordReset, signInWithEmailAndPassword, signOut } from 'firebase/auth';
import { getFunctions, httpsCallable } from 'firebase/functions';
import { COLORS } from '../design/tokens';
import { MAX_PASSWORD_LENGTH, MIN_PASSWORD_LENGTH, passwordLengthError } from '../utils/passwordPolicy';
import { clearLocalSessionData } from '../utils/sessionPrivacy';

const SPRING_FAST = { type: 'spring' as const, stiffness: 500, damping: 28 };
const SPRING_GENTLE = { type: 'spring' as const, stiffness: 340, damping: 30 };
const SPRING_POP = { type: 'spring' as const, stiffness: 420, damping: 18 };

const errorAnim = {
  initial: { opacity: 0, y: -6, scale: 0.96 },
  animate: { opacity: 1, y: 0, scale: 1 },
  exit: { opacity: 0, y: -4, scale: 0.96 },
  transition: SPRING_FAST,
};

const btnHover = { scale: 1.02, y: -1 };
const btnTap = { scale: 0.97, y: 1 };

type Stage = 'verifying' | 'ready' | 'invalid' | 'submitting' | 'done';

const ResetPasswordPage: React.FC = () => {
  const params = new URLSearchParams(window.location.search);
  const oobCode = params.get('oobCode');

  const [stage, setStage] = useState<Stage>('verifying');
  const [email, setEmail] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [securityNotice, setSecurityNotice] = useState('');

  useEffect(() => {
    if (!oobCode) {
      setStage('invalid');
      setError('This reset link is missing required information.');
      return;
    }
    (async () => {
      try {
        const verifiedEmail = await verifyPasswordResetCode(auth, oobCode);
        setEmail(verifiedEmail);
        setStage('ready');
      } catch (err: any) {
        console.error('Password reset code verification failed:', err);
        setStage('invalid');
        if (err.code === 'auth/expired-action-code') {
          setError('This reset link has expired. Request a new one from the sign-in page.');
        } else if (err.code === 'auth/invalid-action-code') {
          setError('This reset link is invalid or has already been used. Request a new one from the sign-in page.');
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
      } else if (err.code === 'auth/expired-action-code') {
        setError('This reset link has expired.');
        setStage('invalid');
      } else {
        setError('Could not reset your password. Try again.');
      }
    }
  };

  const inputClass = "w-full py-3.5 px-4 rounded-xl text-sm font-sans text-zinc-800 placeholder-zinc-400 outline-none transition-all bg-white border-2 border-zinc-200 focus:border-[#F26B1F]";
  const primaryBtn = "w-full py-3.5 rounded-xl text-[15px] font-semibold transition-all border-2 disabled:opacity-50 disabled:cursor-not-allowed";
  const primaryBtnStyle = { backgroundColor: '#FFFFFF', color: '#1A1A1A', borderColor: 'rgba(26,26,26,0.55)' };

  // Replace rather than append so a used reset token is not left in the
  // browser's Back history on a shared device.
  const goToSignIn = () => { window.location.replace('/'); };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4 md:p-8 theme-compat" style={{ backgroundColor: 'var(--surface-canvas)' }}>
      <MotionDiv
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={SPRING_GENTLE}
        className="w-full max-w-md bg-white rounded-2xl overflow-hidden p-8 md:p-10"
        style={{ boxShadow: '0 2px 8px rgba(0,0,0,0.06), 0 12px 40px rgba(0,0,0,0.04)', border: '1.5px solid rgba(0,0,0,0.25)' }}
      >
        <p className="text-[10px] font-bold uppercase tracking-[0.2em] mb-4" style={{ color: '#9e9186' }}>NEXTSTEPUNI</p>

        {stage === 'verifying' && (
          <div className="py-6 text-center">
            <svg className="animate-spin mx-auto mb-4" width="32" height="32" viewBox="0 0 36 36" fill="none">
              <circle cx="18" cy="18" r="15" stroke="#e0dbd4" strokeWidth="3" />
              <path d="M18 3a15 15 0 0 1 15 15" stroke={COLORS.accent} strokeWidth="3" strokeLinecap="round" />
            </svg>
            <p className="text-sm" style={{ color: '#7a7068' }}>Verifying your reset link…</p>
          </div>
        )}

        {stage === 'invalid' && (
          <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={SPRING_GENTLE}>
            <MotionDiv
              initial={{ scale: 0, rotate: -8 }}
              animate={{ scale: 1, rotate: 0 }}
              transition={SPRING_POP}
              className="w-12 h-12 mb-4 rounded-full flex items-center justify-center"
              style={{ backgroundColor: '#fef2f2' }}
            >
              <AlertTriangle size={24} style={{ color: '#A8746E' }} />
            </MotionDiv>
            <h2 className="text-2xl font-semibold tracking-tight mb-2" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>This link doesn&apos;t work</h2>
            <p className="text-sm mb-6" style={{ color: '#7a7068' }}>{error}</p>
            <MotionButton
              onClick={goToSignIn}
              whileHover={btnHover}
              whileTap={btnTap}
              transition={SPRING_FAST}
              className={primaryBtn}
              style={primaryBtnStyle}
            >
              Back to sign in
            </MotionButton>
          </MotionDiv>
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
              style={{ backgroundColor: COLORS.successTint }}
            >
              <Check size={24} style={{ color: COLORS.success }} />
            </MotionDiv>
            <MotionDiv initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} transition={SPRING_GENTLE}>
              <h2 className="text-2xl font-semibold tracking-tight mb-1" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>Password updated</h2>
              <p className="text-sm mb-6" style={{ color: '#7a7068' }}>You can now sign in with your new password.</p>
              {securityNotice && <p role="alert" className="text-sm mb-6 text-red-600">{securityNotice}</p>}
            </MotionDiv>
            <MotionDiv initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} transition={SPRING_GENTLE}>
              <MotionButton
                onClick={goToSignIn}
                whileHover={btnHover}
                whileTap={btnTap}
                transition={SPRING_FAST}
                className={primaryBtn}
                style={primaryBtnStyle}
              >
                Sign in
              </MotionButton>
            </MotionDiv>
          </MotionDiv>
        )}
      </MotionDiv>
    </div>
  );
};

export default ResetPasswordPage;
