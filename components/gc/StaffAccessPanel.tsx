/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The guidance counsellor's school-access panel.
 *
 * Since the per-teacher invitation flow was retired (2026-09-04), the only
 * code managed here is the STUDENT join code. Teachers now sign in with the
 * shared staff-room password the administrator provisions — there is nothing
 * for the counsellor to mint, and no roster to prune: revoking staff access
 * is rotating that password.
 */

import React, { useEffect, useState, useCallback } from 'react';
import { getFunctions, httpsCallable } from 'firebase/functions';
import { Check, Copy, KeyRound, RefreshCw, ShieldCheck } from 'lucide-react';
import app, { auth } from '../../firebase';
import { getSchoolName } from '../../schoolData';
import { reauthMethodFor, reauthenticateCurrentUser } from '../../utils/reauthenticate';

export const StaffAccessPanel: React.FC<{ school: string }> = ({ school }) => {
  const [studentConfigured, setStudentConfigured] = useState(false);
  const [studentCode, setStudentCode] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [copied, setCopied] = useState(false);
  const [error, setError] = useState('');
  const [confirming, setConfirming] = useState(false);
  const [password, setPassword] = useState('');

  const closeConfirm = useCallback(() => {
    setPassword('');
    setConfirming(false);
  }, []);

  const load = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const statusFn = httpsCallable<unknown, { studentConfigured: boolean }>(
        getFunctions(app),
        'getSchoolAccessStatus',
      );
      const status = await statusFn({});
      setStudentConfigured(status.data.studentConfigured);
    } catch (err) {
      console.error('[SchoolAccess] failed to load access status:', err);
      setError('Could not load access settings. Try again.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { void load(); }, [load]);

  const rotate = useCallback(async () => {
    if (!auth.currentUser) return;
    setSaving(true);
    setError('');
    try {
      await reauthenticateCurrentUser(auth.currentUser, password);
      const rotateFn = httpsCallable<unknown, { code: string }>(getFunctions(app), 'rotateStudentJoinCode');
      const result = await rotateFn({});
      setStudentCode(result.data.code);
      setStudentConfigured(true);
      closeConfirm();
    } catch (err) {
      console.error('[SchoolAccess] rotation failed:', err);
      setError('Your sign-in could not be verified, or the change was not saved. Please try again.');
    } finally {
      setSaving(false);
    }
  }, [closeConfirm, password]);

  const copy = useCallback(async () => {
    if (!studentCode) return;
    try {
      await navigator.clipboard.writeText(studentCode);
      setCopied(true);
      setTimeout(() => setCopied(false), 1800);
    } catch { /* The code remains visible for manual copy. */ }
  }, [studentCode]);

  return (
    <div className="p-6 max-w-3xl mx-auto w-full">
      <div className="flex items-center gap-2.5 mb-1">
        <KeyRound size={20} className="text-zinc-500 dark:text-zinc-400" />
        <h2 className="text-xl font-semibold tracking-tight text-zinc-900 dark:text-white">School access</h2>
      </div>
      <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-6">
        The student join code for {getSchoolName(school)}. Teachers do not need a code — they sign in
        with the staff-room password your school was given.
      </p>

      {loading ? <p className="text-sm text-zinc-400">Loading…</p> : (
        <section className="rounded-2xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 p-6">
          <p className="text-[11px] font-semibold uppercase tracking-widest text-zinc-400">Student join code</p>
          <p className="text-sm text-zinc-500 dark:text-zinc-400 mt-2">
            Students use this during registration. It remains active until you rotate it.
          </p>
          {studentCode ? (
            <div className="mt-4 flex items-center gap-3 flex-wrap">
              <code className="text-xl font-bold tracking-[0.16em] text-zinc-900 dark:text-white select-all">{studentCode}</code>
              <button
                type="button"
                onClick={() => void copy()}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium border border-zinc-200 dark:border-zinc-700 text-zinc-600 dark:text-zinc-300"
              >
                {copied ? <><Check size={13} className="text-green-600" /> Copied</> : <><Copy size={13} /> Copy</>}
              </button>
              <p className="w-full text-xs text-amber-700 dark:text-amber-300">Copy this now. For security, it will not be shown again.</p>
            </div>
          ) : (
            <p className="text-sm text-zinc-500 dark:text-zinc-400 mt-4">
              {studentConfigured ? 'A code is active. Generate a new one if it needs to be shared again.' : 'No code is active yet.'}
            </p>
          )}
          <button
            type="button"
            onClick={() => { setError(''); setConfirming(true); }}
            disabled={saving}
            className="mt-4 inline-flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium bg-zinc-900 dark:bg-white text-white dark:text-zinc-900 disabled:opacity-50"
          >
            <RefreshCw size={14} /> {studentConfigured ? 'Rotate code' : 'Generate code'}
          </button>
        </section>
      )}

      {error && <p role="alert" className="text-sm text-red-500 mt-4">{error}</p>}
      <p className="text-xs text-zinc-400 mt-4 leading-relaxed flex items-start gap-1.5">
        <ShieldCheck size={13} className="mt-0.5 shrink-0" /> The code is stored as a one-way hash and shown only when generated. Rotate it to stop future joins.
      </p>

      {confirming && (
        <div className="fixed inset-0 z-[240] flex items-center justify-center bg-black/55 p-4" onClick={() => !saving && closeConfirm()}>
          <div role="dialog" aria-modal="true" aria-labelledby="verify-access-title" className="w-full max-w-sm rounded-2xl border border-zinc-700 bg-zinc-950 p-6 shadow-2xl" onClick={event => event.stopPropagation()}>
            <h3 id="verify-access-title" className="text-lg font-semibold text-white">Verify this security change</h3>
            <p className="text-sm text-zinc-400 mt-2">Re-enter your password before rotating the join code.</p>
            {reauthMethodFor(auth.currentUser) === 'password' && (
              <input
                type="password"
                value={password}
                onChange={event => setPassword(event.target.value)}
                placeholder="Your password"
                autoComplete="current-password"
                className="mt-4 w-full rounded-xl border border-zinc-700 bg-zinc-900 px-4 py-2.5 text-sm text-white outline-none"
              />
            )}
            <div className="mt-5 flex justify-end gap-2">
              <button type="button" onClick={closeConfirm} disabled={saving} className="px-4 py-2 rounded-lg text-sm font-medium text-zinc-300">Cancel</button>
              <button
                type="button"
                onClick={() => void rotate()}
                disabled={saving || (reauthMethodFor(auth.currentUser) === 'password' && !password)}
                className="px-4 py-2 rounded-lg text-sm font-semibold bg-white text-zinc-900 disabled:opacity-50"
              >
                {saving ? 'Working…' : 'Confirm'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default StaffAccessPanel;
