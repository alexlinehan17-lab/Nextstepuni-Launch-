/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { createPortal } from 'react-dom';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from '../Motion';
import { X, Download, Trash2, ShieldAlert, Loader2, Check } from 'lucide-react';
import { signOut } from 'firebase/auth';
import { getFunctions, httpsCallable } from 'firebase/functions';
import app, { auth } from '../../firebase';
import { useModal } from '../../hooks/useModal';
import { logError } from '../../utils/logError';
import { reauthMethodFor, reauthenticateCurrentUser } from '../../utils/reauthenticate';
import { clearLocalSessionData } from '../../utils/sessionPrivacy';

// Self-service GDPR Article 15 (export) + Article 17 (erasure) — audit item 15.
// Backed by the exportMyData / requestAccountDeletion Cloud Functions.

type Phase =
  | 'menu'
  | 'downloading'
  | 'downloaded'
  | 'delete-confirm'
  | 'delete-reauth'
  | 'delete-type'
  | 'deleting'
  | 'deleted';

interface DataRightsModalProps {
  open: boolean;
  onClose: () => void;
  /** Called after the account is fully deleted (parent should reset app state). */
  onAccountDeleted: () => void;
}

export const DataRightsModal: React.FC<DataRightsModalProps> = ({ open, onClose, onAccountDeleted }) => {
  const [phase, setPhase] = useState<Phase>('menu');
  const [password, setPassword] = useState('');
  const [typed, setTyped] = useState('');
  const [error, setError] = useState('');
  const [reauthBusy, setReauthBusy] = useState(false);
  // How this user proves who they are. An Apple or Google account has no
  // password, so asking for one is a dead end rather than a security step.
  const reauthMethod = reauthMethodFor(auth.currentUser);
  // Don't allow Esc / backdrop to dismiss mid-deletion.
  useModal(open, () => { if (phase !== 'deleting' && phase !== 'deleted') reset(); });

  const reset = () => {
    setPhase('menu'); setPassword(''); setTyped(''); setError('');
    onClose();
  };

  const handleDownload = async () => {
    setError(''); setPhase('downloading');
    try {
      const fns = getFunctions(app);
      const exportFn = httpsCallable<{ uid?: string }, unknown>(fns, 'exportMyData');
      const res = await exportFn({});
      const blob = new Blob([JSON.stringify(res.data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `nextstepuni-my-data-${auth.currentUser?.uid ?? 'export'}.json`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
      setPhase('downloaded');
    } catch (err) {
      console.error('Data export failed:', err);
      setError('Could not prepare your export. Please try again, or contact nextstepuniinfo@gmail.com.');
      setPhase('menu');
    }
  };

  const handleReauth = async () => {
    setError('');
    const user = auth.currentUser;
    if (!user) { setError('Could not verify your account. Please sign out and back in.'); return; }
    setReauthBusy(true);
    try {
      await reauthenticateCurrentUser(user, password);
      setPassword('');
      setPhase('delete-type');
    } catch (err) {
      console.error('Re-authentication failed:', err);
      // Say what actually went wrong. Telling an Apple user their password is
      // wrong when they have never had one is how this stayed hidden.
      setError(
        reauthMethod === 'password'
          ? 'Incorrect password. Please try again.'
          : reauthMethod === 'apple'
            ? 'Apple could not confirm it was you. Please try again.'
            : reauthMethod === 'google'
              ? 'Google could not confirm it was you. Please try again.'
              : 'We could not verify your account. Please contact nextstepuniinfo@gmail.com.',
      );
    } finally {
      setReauthBusy(false);
    }
  };

  const handleDelete = async () => {
    setError(''); setPhase('deleting');
    try {
      const fns = getFunctions(app);
      const deleteFn = httpsCallable<{ uid?: string }, { success: boolean }>(fns, 'requestAccountDeletion');
      await deleteFn({});
      await signOut(auth).catch((e) => logError('DataRightsModal.signOut', e));
      await clearLocalSessionData();
      setPhase('deleted');
    } catch (err) {
      console.error('Account deletion failed:', err);
      setError('Could not delete your account. Please try again, or contact nextstepuniinfo@gmail.com.');
      setPhase('delete-type');
    }
  };

  if (!open) return null;

  const panel = (body: React.ReactNode) => (
    <MotionDiv
      key="card"
      initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: 20 }}
      className="bg-white dark:bg-zinc-900 w-full sm:max-w-md rounded-t-2xl sm:rounded-2xl border border-zinc-200 dark:border-zinc-800 shadow-2xl overflow-hidden"
      onClick={(e: React.MouseEvent) => e.stopPropagation()}
    >
      {body}
    </MotionDiv>
  );

  const header = (title: string, closable = true) => (
    <div className="flex items-center justify-between px-5 py-4 border-b border-zinc-100 dark:border-zinc-800">
      <h2 className="text-base font-semibold text-zinc-900 dark:text-white" style={{ fontFamily: "'Source Serif 4', serif" }}>{title}</h2>
      {closable && (
        <button onClick={reset} aria-label="Close" className="p-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-white/[0.06]">
          <X size={18} className="text-zinc-500" />
        </button>
      )}
    </div>
  );

  const errLine = error ? <p className="text-sm text-red-500 font-medium mt-3">{error}</p> : null;

  let body: React.ReactNode;
  switch (phase) {
    case 'menu':
    case 'downloading':
    case 'downloaded':
      body = (
        <>
          {header('Your data')}
          <div className="p-5 space-y-3">
            <button
              onClick={handleDownload}
              disabled={phase === 'downloading'}
              className="w-full flex items-center gap-3 p-3.5 rounded-xl border-2 border-zinc-200 dark:border-zinc-700 hover:bg-zinc-50 dark:hover:bg-white/[0.04] transition-colors disabled:opacity-50 text-left"
            >
              {phase === 'downloading' ? <Loader2 size={18} className="text-zinc-500 animate-spin shrink-0" /> : phase === 'downloaded' ? <Check size={18} className="text-success shrink-0" /> : <Download size={18} className="text-zinc-500 shrink-0" />}
              <div>
                <p className="text-sm font-semibold text-zinc-800 dark:text-zinc-100">Download my data</p>
                <p className="text-[12px] text-zinc-500">{phase === 'downloading' ? 'Preparing your export…' : phase === 'downloaded' ? 'Saved. Check your downloads.' : 'A machine-readable copy of everything we hold about you.'}</p>
              </div>
            </button>
            <button
              onClick={() => { setError(''); setPhase('delete-confirm'); }}
              className="w-full flex items-center gap-3 p-3.5 rounded-xl border-2 border-rose-200 dark:border-rose-900/40 hover:bg-rose-50 dark:hover:bg-rose-900/10 transition-colors text-left"
            >
              <Trash2 size={18} className="text-rose-500 shrink-0" />
              <div>
                <p className="text-sm font-semibold text-rose-600 dark:text-rose-400">Delete my account</p>
                <p className="text-[12px] text-zinc-500">Permanently erase your account and all your data.</p>
              </div>
            </button>
            {errLine}
          </div>
        </>
      );
      break;

    case 'delete-confirm':
      body = (
        <>
          {header('Delete your account?')}
          <div className="p-5">
            <div className="flex items-start gap-2.5 mb-4">
              <ShieldAlert size={18} className="text-rose-500 mt-0.5 shrink-0" />
              <p className="text-sm text-zinc-600 dark:text-zinc-300 leading-relaxed">
                This permanently deletes your account and <strong>all</strong> your data — your progress, reflections, points and messages. This cannot be undone. If you only want a copy, choose “Download my data” first.
              </p>
            </div>
            <div className="flex gap-2">
              <button onClick={reset} className="flex-1 py-3 rounded-xl border-2 border-zinc-200 dark:border-zinc-700 text-sm font-medium text-zinc-600 dark:text-zinc-300">Cancel</button>
              <button onClick={() => { setError(''); setPhase('delete-reauth'); }} className="flex-1 py-3 rounded-xl text-sm font-semibold text-white" style={{ backgroundColor: '#e11d48' }}>Continue</button>
            </div>
          </div>
        </>
      );
      break;

    case 'delete-reauth':
      body = (
        <>
          {header('Confirm it’s you')}
          <div className="p-5">
            <p className="text-sm text-zinc-600 dark:text-zinc-300 mb-3">
              {reauthMethod === 'password'
                ? 'Please re-enter your password to continue.'
                : reauthMethod === 'apple'
                  ? 'Confirm with Apple to continue. You’ll be asked to sign in again.'
                  : reauthMethod === 'google'
                    ? 'Confirm with Google to continue. You’ll be asked to sign in again.'
                    : 'We can’t verify this account automatically. Please contact nextstepuniinfo@gmail.com and we’ll delete it for you.'}
            </p>
            {reauthMethod === 'password' && (
              <input
                type="password" value={password} autoFocus
                onChange={e => { setPassword(e.target.value); setError(''); }}
                onKeyDown={e => { if (e.key === 'Enter' && password) handleReauth(); }}
                placeholder="Your password"
                className="w-full py-3 px-4 rounded-xl text-sm bg-white dark:bg-zinc-800 border-2 border-zinc-200 dark:border-zinc-700 focus:border-rose-400 outline-none text-zinc-800 dark:text-zinc-100"
              />
            )}
            {errLine}
            <div className="flex gap-2 mt-4">
              <button onClick={reset} className="flex-1 py-3 rounded-xl border-2 border-zinc-200 dark:border-zinc-700 text-sm font-medium text-zinc-600 dark:text-zinc-300">Cancel</button>
              <button
                onClick={handleReauth}
                disabled={reauthBusy || reauthMethod === 'unsupported' || (reauthMethod === 'password' && !password)}
                className="flex-1 py-3 rounded-xl text-sm font-semibold text-white disabled:opacity-50 flex items-center justify-center gap-2"
                style={{ backgroundColor: '#e11d48' }}
              >
                {reauthBusy
                  ? <><Loader2 size={16} className="animate-spin" /> Confirming…</>
                  : reauthMethod === 'apple' ? 'Confirm with Apple'
                    : reauthMethod === 'google' ? 'Confirm with Google'
                      : 'Continue'}
              </button>
            </div>
          </div>
        </>
      );
      break;

    case 'delete-type':
    case 'deleting':
      body = (
        <>
          {header('Final step', phase !== 'deleting')}
          <div className="p-5">
            <p className="text-sm text-zinc-600 dark:text-zinc-300 mb-3">Type <strong>DELETE</strong> to permanently delete your account.</p>
            <input
              type="text" value={typed} autoFocus disabled={phase === 'deleting'}
              onChange={e => { setTyped(e.target.value); setError(''); }}
              placeholder="DELETE"
              className="w-full py-3 px-4 rounded-xl text-sm bg-white dark:bg-zinc-800 border-2 border-zinc-200 dark:border-zinc-700 focus:border-rose-400 outline-none text-zinc-800 dark:text-zinc-100 tracking-widest"
            />
            {errLine}
            <div className="flex gap-2 mt-4">
              <button onClick={reset} disabled={phase === 'deleting'} className="flex-1 py-3 rounded-xl border-2 border-zinc-200 dark:border-zinc-700 text-sm font-medium text-zinc-600 dark:text-zinc-300 disabled:opacity-50">Cancel</button>
              <button
                onClick={handleDelete}
                disabled={typed !== 'DELETE' || phase === 'deleting'}
                className="flex-1 py-3 rounded-xl text-sm font-semibold text-white disabled:opacity-50 flex items-center justify-center gap-2"
                style={{ backgroundColor: '#e11d48' }}
              >
                {phase === 'deleting' ? <><Loader2 size={16} className="animate-spin" /> Deleting…</> : 'Delete my account'}
              </button>
            </div>
          </div>
        </>
      );
      break;

    case 'deleted':
      body = (
        <>
          {header('Account deleted', false)}
          <div className="p-5 text-center">
            <div className="w-12 h-12 rounded-full bg-successTint dark:bg-success/15 flex items-center justify-center mx-auto mb-3">
              <Check size={24} className="text-success" />
            </div>
            <p className="text-sm text-zinc-600 dark:text-zinc-300 mb-5">Your account and all your data have been permanently deleted. Take care.</p>
            <button onClick={() => { setPhase('menu'); onAccountDeleted(); }} className="w-full py-3 rounded-xl text-sm font-semibold text-white" style={{ backgroundColor: '#1a1a1a' }}>Done</button>
          </div>
        </>
      );
      break;
  }

  return createPortal(
    <AnimatePresence>
      <MotionDiv
        key="backdrop"
        initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
        className="fixed inset-0 z-[320] flex items-end sm:items-center justify-center bg-black/50 backdrop-blur-sm p-0 sm:p-4"
        onClick={() => { if (phase !== 'deleting' && phase !== 'deleted') reset(); }}
      >
        {panel(body)}
      </MotionDiv>
    </AnimatePresence>,
    document.body
  );
};

export default DataRightsModal;
