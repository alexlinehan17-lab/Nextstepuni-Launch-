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
import { Check, Copy, Eye, EyeOff, KeyRound, LoaderCircle, Shuffle, TriangleAlert, X } from 'lucide-react';
import app from '../firebase';
import { SCHOOLS } from '../schoolData';

/**
 * Mirrors MIN_SUPPLIED_PASSWORD_LENGTH in functions/src/gcPasswordPolicy.ts.
 *
 * Duplicated rather than imported: that module is server code, and importing it
 * here would break the client build the moment anyone adds a firebase-admin
 * dependency to it. test/gcPasswordPolicy.test.ts asserts the two agree.
 *
 * The server enforces this regardless — the check here only saves a round trip
 * and gives the typist an immediate error.
 */
const MIN_SUPPLIED_PASSWORD_LENGTH = 10;

interface ResetResult {
  email: string;
  password: string;
  generated: boolean;
}

const AdminGcAccessPanel: React.FC = () => {
  const [busySchool, setBusySchool] = useState<string | null>(null);
  const [openSchool, setOpenSchool] = useState<string | null>(null);
  const [chosen, setChosen] = useState('');
  const [showChosen, setShowChosen] = useState(false);
  const [result, setResult] = useState<ResetResult | null>(null);
  const [error, setError] = useState('');
  const [copied, setCopied] = useState(false);

  const closeRow = () => {
    setOpenSchool(null);
    setChosen('');
    setShowChosen(false);
  };

  /** `password` omitted → the server generates one. */
  const reset = async (schoolId: string, password?: string) => {
    const email = `gc-${schoolId}@nextstep.app`;
    setBusySchool(schoolId);
    setError('');
    setResult(null);
    setCopied(false);
    try {
      const fn = httpsCallable<{ email: string; password?: string }, ResetResult & { success: true }>(
        getFunctions(app),
        'adminResetGcPassword',
      );
      const response = await fn(password === undefined ? { email } : { email, password });
      setResult({
        email: response.data.email,
        password: response.data.password,
        generated: response.data.generated,
      });
      closeRow();
    } catch (err) {
      const code = typeof err === 'object' && err && 'code' in err ? String((err as { code?: unknown }).code) : '';
      const message = typeof err === 'object' && err && 'message' in err ? String((err as { message?: unknown }).message) : '';
      if (code.endsWith('not-found')) {
        setError(`No counsellor account exists for ${email} yet. Create it in the Firebase console first.`);
      } else if (code.endsWith('permission-denied')) {
        setError('Only the administrator account can reset a counsellor login.');
      } else if (code.endsWith('invalid-argument')) {
        setError(message || `Choose a password of at least ${MIN_SUPPLIED_PASSWORD_LENGTH} characters.`);
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
            {result.generated ? 'New password for' : 'Password set for'} {result.email}
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
            {result.generated
              ? 'Shown once and never stored — copy it now. '
              : 'Set as typed, and not stored anywhere. '}
            The old password stopped working the moment this appeared, so anyone signed in at that
            school will need this to get back in.
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
              onClick={() => (openSchool === school.id ? closeRow() : (closeRow(), setOpenSchool(school.id)))}
              disabled={busySchool !== null}
              aria-expanded={openSchool === school.id}
              className="flex shrink-0 items-center gap-1.5 rounded-full border-2 border-[#1A1A1A] bg-white px-4 py-2 text-xs font-bold text-[#1A1A1A] disabled:opacity-40"
            >
              {busySchool === school.id
                ? <LoaderCircle size={14} className="animate-spin" />
                : openSchool === school.id ? <X size={14} /> : <KeyRound size={14} />}
              {busySchool === school.id
                ? 'Resetting…'
                : openSchool === school.id ? 'Cancel' : 'Reset password'}
            </button>

            {openSchool === school.id && (
              <div className="w-full border-t border-[#DDD8D2] pt-4">
                <label htmlFor={`pw-${school.id}`} className="block text-[11px] font-bold uppercase tracking-[0.16em] text-[#9E9186]">
                  Choose a password
                </label>
                <div className="mt-2 flex flex-wrap items-center gap-2">
                  <div className="relative min-w-0 flex-1">
                    <input
                      id={`pw-${school.id}`}
                      type={showChosen ? 'text' : 'password'}
                      value={chosen}
                      onChange={event => setChosen(event.target.value)}
                      autoComplete="new-password"
                      placeholder={`At least ${MIN_SUPPLIED_PASSWORD_LENGTH} characters`}
                      className="w-full rounded-xl border-2 border-[#1A1A1A] bg-white px-4 py-2.5 pr-11 font-mono text-sm text-[#1A1A1A] outline-none placeholder:font-sans placeholder:text-[#9E9186] focus:ring-4 focus:ring-[#F26B1F]/15"
                    />
                    <button
                      type="button"
                      onClick={() => setShowChosen(v => !v)}
                      aria-label={showChosen ? 'Hide password' : 'Show password'}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-[#7A7068]"
                    >
                      {showChosen ? <EyeOff size={16} /> : <Eye size={16} />}
                    </button>
                  </div>
                  <button
                    type="button"
                    onClick={() => void reset(school.id, chosen)}
                    disabled={chosen.length < MIN_SUPPLIED_PASSWORD_LENGTH || busySchool !== null}
                    className="shrink-0 rounded-full border-2 border-[#1A1A1A] bg-[#1A1A1A] px-4 py-2.5 text-xs font-bold text-white disabled:opacity-40"
                  >
                    Set password
                  </button>
                  <button
                    type="button"
                    onClick={() => void reset(school.id)}
                    disabled={busySchool !== null}
                    className="flex shrink-0 items-center gap-1.5 rounded-full border-2 border-[#1A1A1A] bg-white px-4 py-2.5 text-xs font-bold text-[#1A1A1A] disabled:opacity-40"
                  >
                    <Shuffle size={14} />
                    Generate one
                  </button>
                </div>
                <p className="mt-2 text-xs leading-relaxed text-[#7A7068]">
                  Whichever you choose, the old password stops working immediately.
                </p>
              </div>
            )}
          </li>
        ))}
      </ul>
    </section>
  );
};

export default AdminGcAccessPanel;
