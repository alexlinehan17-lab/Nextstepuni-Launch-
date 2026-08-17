/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Reset a guidance-counsellor login.
 *
 * GC logins are shared per-school accounts at derived addresses
 * (gc-{schoolId}@nextstep.app) whose mailboxes do not exist, so the Firebase
 * console's emailed reset link goes nowhere and it offers no way to set a
 * password directly. This calls adminResetGcPassword, which does the work
 * server-side and can only ever target a gc-* address.
 *
 * The new password is shown ONCE and never stored — copy it before closing.
 */
import React, { useState } from 'react';
import { getFunctions, httpsCallable } from 'firebase/functions';
import { Check, Copy, KeyRound, LoaderCircle, TriangleAlert } from 'lucide-react';
import app from '../firebase';
import { SCHOOLS } from '../schoolData';

interface ResetResult {
  email: string;
  password: string;
}

const AdminGcAccessPanel: React.FC = () => {
  const [busySchool, setBusySchool] = useState<string | null>(null);
  const [result, setResult] = useState<ResetResult | null>(null);
  const [error, setError] = useState('');
  const [copied, setCopied] = useState(false);

  const reset = async (schoolId: string) => {
    const email = `gc-${schoolId}@nextstep.app`;
    setBusySchool(schoolId);
    setError('');
    setResult(null);
    setCopied(false);
    try {
      const fn = httpsCallable<{ email: string }, ResetResult & { success: true }>(
        getFunctions(app),
        'adminResetGcPassword',
      );
      const response = await fn({ email });
      setResult({ email: response.data.email, password: response.data.password });
    } catch (err) {
      const code = typeof err === 'object' && err && 'code' in err ? String((err as { code?: unknown }).code) : '';
      const message = typeof err === 'object' && err && 'message' in err ? String((err as { message?: unknown }).message) : '';
      if (code.endsWith('not-found')) {
        setError(`No counsellor account exists for ${email} yet. Create it in the Firebase console first.`);
      } else if (code.endsWith('permission-denied')) {
        setError('Only the administrator account can reset a counsellor login.');
      } else {
        console.error('GC password reset failed:', err);
        setError(message || 'Could not reset that login. Try again.');
      }
    } finally {
      setBusySchool(null);
    }
  };

  const copy = async () => {
    if (!result) return;
    try {
      await navigator.clipboard.writeText(result.password);
      setCopied(true);
    } catch {
      setError('Could not copy — select the password and copy it manually.');
    }
  };

  return (
    <section aria-label="Guidance counsellor logins">
      <div className="mb-5">
        <h2 className="font-serif text-xl font-semibold text-[#1A1A1A]">Counsellor logins</h2>
        <p className="mt-1 max-w-2xl text-sm leading-relaxed text-[#7A7068]">
          These accounts sign in with the school name and a password — there is no email inbox behind
          them, so the usual reset link cannot work. Resetting here sets a new password immediately and
          shows it once.
        </p>
      </div>

      {error && (
        <p role="alert" className="mb-4 flex items-start gap-2 rounded-r-[10px] border-l-[3px] border-[#F26B1F] bg-[#FDEEDF] px-4 py-3 text-sm italic text-[#8C3A0E]">
          <TriangleAlert size={16} className="mt-0.5 shrink-0" />
          {error}
        </p>
      )}

      {result && (
        <div role="status" className="mb-5 rounded-r-[10px] border-l-[3px] border-[#3A8D5F] bg-[#E8F2EC] p-5">
          <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-[#1F5F3E]">
            New password for {result.email}
          </p>
          <div className="mt-2 flex flex-wrap items-center gap-3">
            <code className="select-all rounded-lg border-2 border-[#1A1A1A] bg-white px-4 py-2 font-mono text-lg tracking-wider text-[#1A1A1A]">
              {result.password}
            </code>
            <button
              type="button"
              onClick={() => void copy()}
              className="flex items-center gap-1.5 rounded-full border-2 border-[#1A1A1A] bg-white px-4 py-2 text-xs font-bold text-[#1A1A1A]"
            >
              {copied ? <Check size={14} /> : <Copy size={14} />}
              {copied ? 'Copied' : 'Copy'}
            </button>
          </div>
          <p className="mt-3 text-xs leading-relaxed text-[#1F5F3E]">
            Shown once and never stored — copy it now. The old password stopped working the moment this
            appeared, so anyone signed in at that school will need this to get back in.
          </p>
        </div>
      )}

      <ul className="space-y-2">
        {SCHOOLS.map(school => (
          <li
            key={school.id}
            className="flex flex-wrap items-center justify-between gap-3 rounded-xl border-2 border-[#1A1A1A] bg-white p-4"
          >
            <div className="min-w-0">
              <p className="text-sm font-semibold text-[#1A1A1A]">{school.name}</p>
              <p className="truncate font-mono text-xs text-[#7A7068]">gc-{school.id}@nextstep.app</p>
            </div>
            <button
              type="button"
              onClick={() => void reset(school.id)}
              disabled={busySchool !== null}
              className="flex shrink-0 items-center gap-1.5 rounded-full border-2 border-[#1A1A1A] bg-white px-4 py-2 text-xs font-bold text-[#1A1A1A] disabled:opacity-40"
            >
              {busySchool === school.id
                ? <LoaderCircle size={14} className="animate-spin" />
                : <KeyRound size={14} />}
              {busySchool === school.id ? 'Resetting…' : 'Reset password'}
            </button>
          </li>
        ))}
      </ul>
    </section>
  );
};

export default AdminGcAccessPanel;
