/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The card every Firebase email-action screen sits in (password reset, email
 * confirmation, email recovery), plus its shared progress and outcome states.
 */

import React from 'react';
import { MotionButton, MotionDiv } from './Motion';
import { Check, AlertTriangle } from 'lucide-react';
import { COLORS } from '../design/tokens';

export const SPRING_FAST = { type: 'spring' as const, stiffness: 500, damping: 28 };
export const SPRING_GENTLE = { type: 'spring' as const, stiffness: 340, damping: 30 };
const SPRING_POP = { type: 'spring' as const, stiffness: 420, damping: 18 };

export const btnHover = { scale: 1.02, y: -1 };
export const btnTap = { scale: 0.97, y: 1 };

export const primaryBtn = "w-full py-3.5 rounded-xl text-[15px] font-semibold transition-all border-2 disabled:opacity-50 disabled:cursor-not-allowed";
export const primaryBtnStyle = { backgroundColor: '#FFFFFF', color: '#1A1A1A', borderColor: 'rgba(26,26,26,0.55)' };
export const headingStyle = { fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' };
export const bodyStyle = { color: '#7a7068' };

// Replace rather than append so a used one-time code is not left in the
// browser's Back history on a shared device.
export const goToSignIn = () => { window.location.replace('/'); };

export const AuthActionCard: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div className="min-h-screen flex flex-col items-center justify-center p-4 md:p-8 theme-compat" style={{ backgroundColor: 'var(--surface-canvas)' }}>
    <MotionDiv
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={SPRING_GENTLE}
      className="w-full max-w-md bg-white rounded-2xl overflow-hidden p-8 md:p-10"
      style={{ boxShadow: '0 2px 8px rgba(0,0,0,0.06), 0 12px 40px rgba(0,0,0,0.04)', border: '1.5px solid rgba(0,0,0,0.25)' }}
    >
      <p className="text-[10px] font-bold uppercase tracking-[0.2em] mb-4" style={{ color: '#9e9186' }}>NEXTSTEPUNI</p>
      {children}
    </MotionDiv>
  </div>
);

export const AuthActionProgress: React.FC<{ label: string }> = ({ label }) => (
  <div className="py-6 text-center" role="status">
    <svg className="animate-spin mx-auto mb-4" width="32" height="32" viewBox="0 0 36 36" fill="none" aria-hidden="true">
      <circle cx="18" cy="18" r="15" stroke="#e0dbd4" strokeWidth="3" />
      <path d="M18 3a15 15 0 0 1 15 15" stroke={COLORS.accent} strokeWidth="3" strokeLinecap="round" />
    </svg>
    <p className="text-sm" style={bodyStyle}>{label}</p>
  </div>
);

/** A link that could not be used: what happened, and the way back to sign in. */
/** A link that did not work. `children` (optional) sits between the message
 *  and the way back, e.g. a form to send a fresh link. */
export const AuthActionProblem: React.FC<{ title: string; message: string; children?: React.ReactNode }> = ({ title, message, children }) => (
  <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={SPRING_GENTLE}>
    <MotionDiv
      initial={{ scale: 0, rotate: -8 }}
      animate={{ scale: 1, rotate: 0 }}
      transition={SPRING_POP}
      className="w-12 h-12 mb-4 rounded-full flex items-center justify-center"
      style={{ backgroundColor: '#fef2f2' }}
    >
      <AlertTriangle size={24} style={{ color: '#A8746E' }} aria-hidden="true" />
    </MotionDiv>
    <h2 className="text-2xl font-semibold tracking-tight mb-2" style={headingStyle}>{title}</h2>
    <p className="text-sm mb-6" style={bodyStyle}>{message}</p>
    {children}
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
);

/** A link that worked. */
export const AuthActionSuccess: React.FC<{ title: string; message: string; notice?: string }> = ({ title, message, notice }) => (
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
      <Check size={24} style={{ color: COLORS.success }} aria-hidden="true" />
    </MotionDiv>
    <MotionDiv initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} transition={SPRING_GENTLE}>
      <h2 className="text-2xl font-semibold tracking-tight mb-1" style={headingStyle}>{title}</h2>
      <p className="text-sm mb-6" style={bodyStyle}>{message}</p>
      {notice && <p role="alert" className="text-sm mb-6 text-red-600">{notice}</p>}
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
);
