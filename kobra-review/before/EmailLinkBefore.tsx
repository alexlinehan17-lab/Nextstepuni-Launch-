/**
 * "Now" pane for review section 08: the email-link pages, stacked.
 *
 * 1. Verify email: the REAL components/AuthActionPage.tsx on a sample
 *    `mode=verifyEmail` link, so it runs its own applyActionCode and lands on
 *    its own success state (AuthActionCard + AuthActionSuccess).
 * 2. Reset password: the REAL components/ResetPasswordPage.tsx on the same
 *    sample code, so its own checkActionCode passes and it shows the
 *    new-password form for a sample address.
 *    Both run the real Firebase Auth SDK; only the network is stubbed. The SDK
 *    reads window.fetch on every call, so the stub below answers the two
 *    identitytoolkit requests in this frame locally and nothing leaves the
 *    machine. Set password is answered with a server error (there is no
 *    account to change), so the page shows its own "Could not reset your
 *    password. Try again." line.
 * 3. Forced password change: a COPY of the ChangePasswordModal markup from
 *    components/AppRouter.tsx (lines 963-1023 on 27 Oct), because that
 *    component is not exported and AppRouter only renders it for a signed-in
 *    user whose progress has loaded. Same classes, inline styles and words;
 *    Set Password skips the changeOwnPassword callable.
 *
 * Both real pages autofocus their field, which would scroll this frame to the
 * middle; the harness holds the frame at the top for its first four seconds.
 */
import React, { useEffect, useState } from 'react';
import { Check, Eye, EyeOff } from 'lucide-react';
import AuthActionPage from '../../components/AuthActionPage';
import ResetPasswordPage from '../../components/ResetPasswordPage';

const SAMPLE_CODE = 'kobra-review-sample-code';
const SAMPLE_EMAIL = 'sample.student@example.com';

// The sample action link both real pages read from window.location.
const link = new URLSearchParams(window.location.search);
if (link.get('oobCode') !== SAMPLE_CODE) {
  link.set('mode', 'verifyEmail');
  link.set('oobCode', SAMPLE_CODE);
  window.history.replaceState(null, '', `${window.location.pathname}?${link.toString()}`);
}

// Local answers for Firebase Auth's REST calls in this frame only.
const realFetch = window.fetch.bind(window);
const json = (status: number, body: unknown) => new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json' } });
window.fetch = async (input: RequestInfo | URL, init?: RequestInit) => {
  const url = typeof input === 'string' ? input : input instanceof URL ? input.href : input.url;
  if (!url.includes('identitytoolkit.googleapis.com')) return realFetch(input, init);
  let body: Record<string, unknown> = {};
  try { body = JSON.parse(String(init?.body ?? '{}')); } catch { /* not JSON */ }
  if (url.includes('accounts:update') && body.oobCode === SAMPLE_CODE) return json(200, { email: SAMPLE_EMAIL });
  if (url.includes('accounts:resetPassword') && body.oobCode === SAMPLE_CODE && !body.newPassword) {
    return json(200, { email: SAMPLE_EMAIL, requestType: 'PASSWORD_RESET' });
  }
  return json(400, { error: { code: 400, message: 'INTERNAL_ERROR', errors: [] } });
};

/** Copy of ChangePasswordModal (components/AppRouter.tsx), markup unchanged. */
const ChangePasswordModalCopy: React.FC = () => {
  const [newPassword, setNewPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChangePassword = async () => {
    if (newPassword.length < 12) { setError('Password must be at least 12 characters.'); return; }
    if (newPassword.length > 128) { setError('Password must be no more than 128 characters.'); return; }
    setError('');
    // The real screen calls the changeOwnPassword callable and signs out.
  };

  const inputClass = "w-full py-3.5 px-4 rounded-xl text-sm font-sans text-zinc-800 dark:text-white placeholder-zinc-400 outline-none transition-all bg-white dark:bg-zinc-900 border-2 border-zinc-200 dark:border-zinc-700 focus:border-[#F26B1F]";

  return (
    <div className="min-h-screen flex items-center justify-center p-5 bg-white dark:bg-zinc-950">
      <div className="w-full max-w-md bg-white dark:bg-zinc-900 rounded-2xl p-8 md:p-10" style={{ border: '2px solid #1a1a1a' }}>
        <h2 className="text-2xl font-semibold tracking-tight mb-1" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>Set a new password</h2>
        <p className="text-sm mb-8" style={{ color: '#7a7068' }}>Your password was reset by your guidance counsellor. Please choose a new password to continue.</p>
        <div className="space-y-4">
          <div>
            <label className="text-xs font-bold uppercase tracking-wider mb-1.5 block" style={{ color: '#9e9186' }}>New Password</label>
            <div className="relative">
              <input type={showPassword ? 'text' : 'password'} value={newPassword} onChange={e => { setNewPassword(e.target.value); setError(''); }} placeholder="Choose a new password" className={inputClass} autoFocus />
              <button type="button" onClick={() => setShowPassword(!showPassword)} aria-label={showPassword ? 'Hide password' : 'Show password'} aria-pressed={showPassword} className="absolute right-3 top-1/2 -translate-y-1/2 transition-colors" style={{ color: '#9e9186' }}>
                {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
              </button>
            </div>
            {newPassword.length > 0 && newPassword.length < 12 && (
              <p className="text-xs mt-1.5" style={{ color: '#9e9186' }}>{12 - newPassword.length} more character{12 - newPassword.length !== 1 ? 's' : ''} needed</p>
            )}
            {newPassword.length >= 12 && newPassword.length <= 128 && (
              <p className="text-xs mt-1.5 flex items-center gap-1" style={{ color: '#F26B1F' }}><Check size={12} /> Looks good</p>
            )}
          </div>
          {error && <p className="text-sm text-red-500 font-medium">{error}</p>}
          <button
            onClick={handleChangePassword}
            disabled={isLoading || newPassword.length < 12 || newPassword.length > 128}
            className="w-full py-3.5 rounded-full text-white text-[15px] font-semibold transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            style={{ backgroundColor: '#F26B1F', borderBottom: '3px solid #B54D14', boxShadow: '0 4px 0 #B54D14' }}
          >
            {isLoading ? 'Saving...' : 'Set Password'}
          </button>
        </div>
      </div>
    </div>
  );
};

/** Harness label between the screens (not part of any screen). */
const Caption: React.FC<{ part: number; children: React.ReactNode }> = ({ part, children }) => (
  <p id={`kr-el-part-${part}`} style={{ margin: 0, padding: '10px 16px', font: '500 12px/1.4 "DM Sans", sans-serif', letterSpacing: '.08em', textTransform: 'uppercase', color: 'var(--ink-muted, #69605A)', borderTop: '1px dashed var(--outline-soft, #ddd)', borderBottom: '1px dashed var(--outline-soft, #ddd)' }}>
    {children}
  </p>
);

export default function EmailLinkBefore() {
  // Keep the frame at the top while the real pages autofocus their fields
  // (or at screen N with &part=N, for screenshots of the lower screens). In a
  // background iframe focus() scrolls without firing focus events, so hold the
  // position for the first few seconds until the reader scrolls or clicks.
  useEffect(() => {
    const part = new URLSearchParams(window.location.search).get('part');
    const hold = () => {
      const anchor = part ? document.getElementById(`kr-el-part-${part}`) : null;
      const y = anchor ? anchor.getBoundingClientRect().top + window.scrollY : 0;
      if (Math.abs(window.scrollY - y) > 1) window.scrollTo(0, y);
    };
    const interval = window.setInterval(hold, 100);
    const stop = () => window.clearInterval(interval);
    const timer = window.setTimeout(stop, 4000);
    const events = ['wheel', 'touchstart', 'pointerdown', 'keydown'] as const;
    events.forEach(name => window.addEventListener(name, stop, { once: true, passive: true }));
    hold();
    return () => { stop(); window.clearTimeout(timer); events.forEach(name => window.removeEventListener(name, stop)); };
  }, []);
  return (
    <>
      <Caption part={1}>1 · Verify email · AuthActionPage on a sample link</Caption>
      <AuthActionPage />
      <Caption part={2}>2 · Reset password · ResetPasswordPage for a sample address</Caption>
      <ResetPasswordPage />
      <Caption part={3}>3 · Forced password change · copy of AppRouter’s ChangePasswordModal</Caption>
      <ChangePasswordModalCopy />
    </>
  );
}
