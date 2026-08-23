/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useEffect, useState, useCallback } from 'react';
import { getFunctions, httpsCallable } from 'firebase/functions';
import { Check, Copy, KeyRound, RefreshCw, ShieldCheck, UserMinus, Users } from 'lucide-react';
import app, { auth } from '../../firebase';
import { getSchoolName } from '../../schoolData';
import { reauthMethodFor, reauthenticateCurrentUser } from '../../utils/reauthenticate';

interface StaffMember { uid: string; name: string; email: string }
type SensitiveAction =
  | { kind: 'staff-code' }
  | { kind: 'student-code' }
  | { kind: 'revoke'; member: StaffMember };

export const StaffAccessPanel: React.FC<{ school: string }> = ({ school }) => {
  const [staffConfigured, setStaffConfigured] = useState(false);
  const [studentConfigured, setStudentConfigured] = useState(false);
  const [staffCode, setStaffCode] = useState<string | null>(null);
  const [studentCode, setStudentCode] = useState<string | null>(null);
  const [members, setMembers] = useState<StaffMember[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [copied, setCopied] = useState<'staff' | 'student' | null>(null);
  const [error, setError] = useState('');
  const [pendingAction, setPendingAction] = useState<SensitiveAction | null>(null);
  const [password, setPassword] = useState('');
  const closeSensitiveAction = useCallback(() => {
    setPassword('');
    setPendingAction(null);
  }, []);

  const load = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const functions = getFunctions(app);
      const statusFn = httpsCallable<unknown, { staffConfigured: boolean; studentConfigured: boolean }>(
        functions,
        'getSchoolAccessStatus',
      );
      const listFn = httpsCallable<unknown, { members: StaffMember[] }>(functions, 'listStaffAccess');
      const [status, roster] = await Promise.all([statusFn({}), listFn({})]);
      setStaffConfigured(status.data.staffConfigured);
      setStudentConfigured(status.data.studentConfigured);
      setMembers(roster.data.members);
    } catch (err) {
      console.error('[StaffAccess] failed to load access status:', err);
      setError('Could not load access settings. Try again.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { void load(); }, [load]);

  const performSensitiveAction = useCallback(async () => {
    if (!pendingAction || !auth.currentUser) return;
    setSaving(true);
    setError('');
    try {
      await reauthenticateCurrentUser(auth.currentUser, password);
      const functions = getFunctions(app);
      if (pendingAction.kind === 'staff-code') {
        const rotate = httpsCallable<unknown, { code: string }>(functions, 'rotateStaffAccessCode');
        const result = await rotate({});
        setStaffCode(result.data.code);
        setStaffConfigured(true);
      } else if (pendingAction.kind === 'student-code') {
        const rotate = httpsCallable<unknown, { code: string }>(functions, 'rotateStudentJoinCode');
        const result = await rotate({});
        setStudentCode(result.data.code);
        setStudentConfigured(true);
      } else {
        const revoke = httpsCallable<{ uid: string }, { success: boolean }>(functions, 'revokeStaffAccess');
        await revoke({ uid: pendingAction.member.uid });
        setMembers(current => current.filter(member => member.uid !== pendingAction.member.uid));
      }
      closeSensitiveAction();
    } catch (err) {
      console.error('[StaffAccess] security action failed:', err);
      setError('Your sign-in could not be verified, or the change was not saved. Please try again.');
    } finally {
      setSaving(false);
    }
  }, [closeSensitiveAction, password, pendingAction]);

  const copy = useCallback(async (kind: 'staff' | 'student', code: string | null) => {
    if (!code) return;
    try {
      await navigator.clipboard.writeText(code);
      setCopied(kind);
      setTimeout(() => setCopied(null), 1800);
    } catch { /* The code remains visible for manual copy. */ }
  }, []);

  const accessCard = (
    kind: 'staff' | 'student',
    label: string,
    description: string,
    configured: boolean,
    code: string | null,
  ) => (
    <section className="rounded-2xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 p-6">
      <p className="text-[11px] font-semibold uppercase tracking-widest text-zinc-400">{label}</p>
      <p className="text-sm text-zinc-500 dark:text-zinc-400 mt-2">{description}</p>
      {code ? (
        <div className="mt-4 flex items-center gap-3 flex-wrap">
          <code className="text-xl font-bold tracking-[0.16em] text-zinc-900 dark:text-white select-all">{code}</code>
          <button
            type="button"
            onClick={() => void copy(kind, code)}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium border border-zinc-200 dark:border-zinc-700 text-zinc-600 dark:text-zinc-300"
          >
            {copied === kind ? <><Check size={13} className="text-green-600" /> Copied</> : <><Copy size={13} /> Copy</>}
          </button>
          <p className="w-full text-xs text-amber-700 dark:text-amber-300">Copy this now. For security, it will not be shown again.</p>
        </div>
      ) : (
        <p className="text-sm text-zinc-500 dark:text-zinc-400 mt-4">
          {configured ? 'A code is active. Generate a new one if it needs to be shared again.' : 'No code is active yet.'}
        </p>
      )}
      <button
        type="button"
        onClick={() => { setError(''); setPendingAction({ kind: kind === 'staff' ? 'staff-code' : 'student-code' }); }}
        disabled={saving}
        className="mt-4 inline-flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium bg-zinc-900 dark:bg-white text-white dark:text-zinc-900 disabled:opacity-50"
      >
        <RefreshCw size={14} /> {configured ? 'Rotate code' : 'Generate code'}
      </button>
    </section>
  );

  return (
    <div className="p-6 max-w-3xl mx-auto w-full">
      <div className="flex items-center gap-2.5 mb-1">
        <KeyRound size={20} className="text-zinc-500 dark:text-zinc-400" />
        <h2 className="text-xl font-semibold tracking-tight text-zinc-900 dark:text-white">School access</h2>
      </div>
      <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-6">
        Manage join codes and the staff roster for {getSchoolName(school)}.
      </p>

      {loading ? <p className="text-sm text-zinc-400">Loading…</p> : (
        <div className="space-y-5">
          <div className="grid gap-5 md:grid-cols-2">
            {accessCard('student', 'Student join code', 'Students use this during registration. It remains active until you rotate it.', studentConfigured, studentCode)}
            {accessCard('staff', 'Staff invitation code', 'Give this to one verified teacher. It is consumed as soon as they redeem it.', staffConfigured, staffCode)}
          </div>

          <section className="rounded-2xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 p-6">
            <div className="flex items-center gap-2 mb-1">
              <Users size={17} className="text-zinc-500" />
              <h3 className="font-semibold text-zinc-900 dark:text-white">Active staff</h3>
            </div>
            <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-4">Remove access immediately when someone leaves or no longer needs student data.</p>
            {members.length === 0 ? <p className="text-sm text-zinc-400">No teachers have redeemed the current or earlier codes.</p> : (
              <ul className="divide-y divide-zinc-100 dark:divide-zinc-800">
                {members.map(member => (
                  <li key={member.uid} className="py-3 flex items-center justify-between gap-3">
                    <div className="min-w-0">
                      <p className="text-sm font-medium text-zinc-900 dark:text-white truncate">{member.name}</p>
                      <p className="text-xs text-zinc-500 truncate">{member.email}</p>
                    </div>
                    <button
                      type="button"
                      onClick={() => { setError(''); setPendingAction({ kind: 'revoke', member }); }}
                      className="inline-flex items-center gap-1.5 px-3 py-2 rounded-lg text-xs font-medium border border-red-200 text-red-700 dark:border-red-900 dark:text-red-300"
                    >
                      <UserMinus size={14} /> Revoke
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </section>
        </div>
      )}

      {error && <p role="alert" className="text-sm text-red-500 mt-4">{error}</p>}
      <p className="text-xs text-zinc-400 mt-4 leading-relaxed flex items-start gap-1.5">
        <ShieldCheck size={13} className="mt-0.5 shrink-0" /> Codes are stored as one-way hashes and shown only when generated. Staff invitations work once; rotate the student code to stop future joins, and use the roster to revoke existing access.
      </p>

      {pendingAction && (
        <div className="fixed inset-0 z-[240] flex items-center justify-center bg-black/55 p-4" onClick={() => !saving && closeSensitiveAction()}>
          <div role="dialog" aria-modal="true" aria-labelledby="verify-access-title" className="w-full max-w-sm rounded-2xl border border-zinc-700 bg-zinc-950 p-6 shadow-2xl" onClick={event => event.stopPropagation()}>
            <h3 id="verify-access-title" className="text-lg font-semibold text-white">Verify this security change</h3>
            <p className="text-sm text-zinc-400 mt-2">
              {pendingAction.kind === 'revoke' ? `Re-enter your password to revoke ${pendingAction.member.name}.` : 'Re-enter your password before rotating an access code.'}
            </p>
            {reauthMethodFor(auth.currentUser) === 'password' && (
              <input
                type="password"
                value={password}
                onChange={event => setPassword(event.target.value)}
                autoFocus
                autoComplete="current-password"
                className="mt-4 w-full rounded-xl border border-zinc-700 bg-zinc-900 px-4 py-3 text-sm text-white outline-none focus:border-orange-500"
                placeholder="Current password"
              />
            )}
            <div className="mt-5 flex gap-3">
              <button type="button" disabled={saving} onClick={closeSensitiveAction} className="flex-1 rounded-xl border border-zinc-700 px-4 py-2.5 text-sm text-zinc-300 disabled:opacity-50">Cancel</button>
              <button
                type="button"
                disabled={saving || (reauthMethodFor(auth.currentUser) === 'password' && !password)}
                onClick={() => void performSensitiveAction()}
                className="flex-1 rounded-xl bg-orange-600 px-4 py-2.5 text-sm font-semibold text-white disabled:opacity-50"
              >
                {saving ? 'Verifying…' : 'Verify and continue'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
