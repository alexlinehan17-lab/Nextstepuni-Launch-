/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Set or reset the two shared logins each school gets.
 *
 * Both are per-school accounts at derived addresses — gc-{schoolId} for the
 * guidance counsellor, staff-{schoolId} for the staff room — whose mailboxes
 * do not exist, so the Firebase console's emailed reset link goes nowhere and
 * it offers no way to set a password directly. This calls
 * adminResetGcPassword, which does the work server-side and can only ever
 * target one of those two address shapes. Send each password to the school:
 * one for the counsellor, one for the staff room, and that is a school's
 * whole staff onboarding.
 *
 * The new password is shown ONCE and never stored — copy it before closing.
 */
import React, { useState } from 'react';
import { getFunctions, httpsCallable } from 'firebase/functions';
import { Check, Copy, Eye, EyeOff, KeyRound, LoaderCircle, Shuffle, TriangleAlert, X } from 'lucide-react';
import app, { auth } from '../firebase';
import { SCHOOLS } from '../schoolData';
import { reauthMethodFor, reauthenticateCurrentUser } from '../utils/reauthenticate';

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
const MIN_SUPPLIED_PASSWORD_LENGTH = 12;

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
  const [currentPassword, setCurrentPassword] = useState('');
  const [pendingAdoption, setPendingAdoption] = useState<
    { loginKey: string; password?: string; message: string } | null
  >(null);
  const [result, setResult] = useState<ResetResult | null>(null);
  const [error, setError] = useState('');
  const [copied, setCopied] = useState(false);

  const closeRow = () => {
    setOpenSchool(null);
    setChosen('');
    setShowChosen(false);
    setCurrentPassword('');
  };

  /**
   * `password` omitted → the server generates one.
   *
   * `adopt` is only ever set after the server has told us an unrecognised
   * account already holds this login, and the administrator has confirmed they
   * recognise it. It is never sent speculatively — the whole point is that
   * adoption is a deliberate act, not a side effect of clicking Reset.
   */
  const reset = async (loginKey: string, password?: string, adopt?: boolean) => {
    const [kind, schoolId] = loginKey.split(':') as ['gc' | 'staff', string];
    const email = `${kind}-${schoolId}@nextstep.app`;
    setBusySchool(loginKey);
    setError('');
    setResult(null);
    setPendingAdoption(null);
    setCopied(false);
    try {
      if (!auth.currentUser) throw new Error('No administrator is signed in.');
      await reauthenticateCurrentUser(auth.currentUser, currentPassword);
      const fn = httpsCallable<
        { email: string; password?: string; adoptExisting?: boolean },
        ResetResult & { success: true }
      >(getFunctions(app), 'adminResetGcPassword');
      const payload: { email: string; password?: string; adoptExisting?: boolean } = { email };
      if (password !== undefined) payload.password = password;
      if (adopt) payload.adoptExisting = true;
      const response = await fn(payload);
      // Trust what came back, not what we asked for.
      //
      // Hosting and functions deploy as separate CI jobs, so for a few minutes
      // after a release the client can be newer than the callable. An older
      // callable ignores `password` and returns no `generated` field — read
      // naively that reported "set as typed" for a password the server had
      // actually generated, which is exactly the kind of thing that ends with
      // someone handing a school a password that does not work.
      //
      // So decide from the response itself: it was set as typed only if we
      // asked for one AND got that same one back.
      const returned = response.data.password;
      const setAsTyped = password !== undefined && returned === password;
      setResult({ email: response.data.email, password: returned, generated: !setAsTyped });
      if (password !== undefined && !setAsTyped) {
        setError('The server generated a password instead of using the one you typed — it is still '
          + 'deploying an update. Use the password shown, or try again in a few minutes.');
      }
      closeRow();
      setCurrentPassword('');
    } catch (err) {
      const code = typeof err === 'object' && err && 'code' in err ? String((err as { code?: unknown }).code) : '';
      const message = typeof err === 'object' && err && 'message' in err ? String((err as { message?: unknown }).message) : '';
      if (code.endsWith('not-found')) {
        setError(`No account exists for ${email} yet. Create it in the Firebase console first.`);
      } else if (code.endsWith('permission-denied')) {
        setError('Only the administrator account can reset a school login.');
      } else if (code.endsWith('failed-precondition')) {
        // The login is already held by an account the platform did not create.
        // Surface it rather than adopting silently — this is the escalation the
        // 2026-08-17 review found, so the administrator has to make the call.
        setPendingAdoption({ loginKey, password, message });
      } else if (code.endsWith('invalid-argument')) {
        setError(message || `Choose a password of at least ${MIN_SUPPLIED_PASSWORD_LENGTH} characters.`);
      } else {
        console.error('School login reset failed:', err);
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
    <section aria-label="School logins">
      <div className="mb-5">
        <h2 className="font-serif text-xl font-semibold text-[#1A1A1A]">School logins</h2>
        <p className="mt-1 max-w-2xl text-sm leading-relaxed text-[#7A7068]">
          Each school has two shared logins: the guidance counsellor&apos;s and the staff room&apos;s.
          Both sign in with the school name and a password — there is no email inbox behind them, so
          the usual reset link cannot work. Setting a password here takes effect immediately and shows
          it once; send it to the school and their onboarding is done.
        </p>
      </div>

      {error && (
        <p role="alert" className="mb-4 flex items-start gap-2 rounded-r-[10px] border-l-[3px] border-[#F26B1F] bg-[#FDEEDF] px-4 py-3 text-sm italic text-[#8C3A0E]">
          <TriangleAlert size={16} className="mt-0.5 shrink-0" />
          {error}
        </p>
      )}

      {pendingAdoption && (
        <div role="alert" className="mb-5 rounded-r-[10px] border-l-[3px] border-[#F26B1F] bg-[#FDEEDF] p-5">
          <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-[#8C3A0E]">
            This login already has an account
          </p>
          <p className="mt-2 text-sm leading-relaxed text-[#8C3A0E]">{pendingAdoption.message}</p>
          <p className="mt-2 text-sm leading-relaxed text-[#8C3A0E]">
            If you do not recognise it, someone else may have registered this address. Check it in the
            Firebase console before continuing — adopting it grants that account access to every student
            record in the school.
          </p>
          <div className="mt-4 flex flex-wrap gap-2">
            <button
              type="button"
              onClick={() => {
                const { loginKey, password } = pendingAdoption;
                setPendingAdoption(null);
                void reset(loginKey, password, true);
              }}
              className="rounded-full border-2 border-[#1A1A1A] bg-white px-4 py-2 text-xs font-bold text-[#1A1A1A]"
            >
              I recognise it — adopt
            </button>
            <button
              type="button"
              onClick={() => setPendingAdoption(null)}
              className="rounded-full border-2 border-[#1A1A1A] bg-[#1A1A1A] px-4 py-2 text-xs font-bold text-white"
            >
              Stop
            </button>
          </div>
        </div>
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
        {SCHOOLS.flatMap(school => (['gc', 'staff'] as const).map(kind => ({ school, kind, key: `${kind}:${school.id}` }))).map(({ school, kind, key }) => (
          <li
            key={key}
            className="flex flex-wrap items-center justify-between gap-3 rounded-xl border-2 border-[#1A1A1A] bg-white p-4"
          >
            <div className="min-w-0">
              <p className="text-sm font-semibold text-[#1A1A1A]">
                {school.name}
                <span className="ml-2 text-xs font-medium text-[#7A7068]">{kind === 'gc' ? 'Guidance counsellor' : 'Staff room'}</span>
              </p>
              <p className="truncate font-mono text-xs text-[#7A7068]">{kind}-{school.id}@nextstep.app</p>
            </div>
            <button
              type="button"
              onClick={() => (openSchool === key ? closeRow() : (closeRow(), setOpenSchool(key)))}
              disabled={busySchool !== null}
              aria-expanded={openSchool === key}
              className="flex shrink-0 items-center gap-1.5 rounded-full border-2 border-[#1A1A1A] bg-white px-4 py-2 text-xs font-bold text-[#1A1A1A] disabled:opacity-40"
            >
              {busySchool === key
                ? <LoaderCircle size={14} className="animate-spin" />
                : openSchool === key ? <X size={14} /> : <KeyRound size={14} />}
              {busySchool === key
                ? 'Resetting…'
                : openSchool === key ? 'Cancel' : 'Set password'}
            </button>

            {openSchool === key && (
              <div className="w-full border-t border-[#DDD8D2] pt-4">
                {reauthMethodFor(auth.currentUser) === 'password' && (
                  <div className="mb-4">
                    <label htmlFor={`current-pw-${key}`} className="block text-[11px] font-bold uppercase tracking-[0.16em] text-[#9E9186]">
                      Your current administrator password
                    </label>
                    <input
                      id={`current-pw-${key}`}
                      type="password"
                      value={currentPassword}
                      onChange={event => setCurrentPassword(event.target.value)}
                      autoComplete="current-password"
                      className="mt-2 w-full rounded-xl border-2 border-[#1A1A1A] bg-white px-4 py-2.5 text-sm text-[#1A1A1A] outline-none focus:ring-4 focus:ring-[#F26B1F]/15"
                    />
                  </div>
                )}
                <label htmlFor={`pw-${key}`} className="block text-[11px] font-bold uppercase tracking-[0.16em] text-[#9E9186]">
                  Choose a password
                </label>
                <div className="mt-2 flex flex-wrap items-center gap-2">
                  <div className="relative min-w-0 flex-1">
                    <input
                      id={`pw-${key}`}
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
                    onClick={() => void reset(key, chosen)}
                    disabled={chosen.length < MIN_SUPPLIED_PASSWORD_LENGTH || busySchool !== null || (reauthMethodFor(auth.currentUser) === 'password' && !currentPassword)}
                    className="shrink-0 rounded-full border-2 border-[#1A1A1A] bg-[#1A1A1A] px-4 py-2.5 text-xs font-bold text-white disabled:opacity-40"
                  >
                    Set password
                  </button>
                  <button
                    type="button"
                    onClick={() => void reset(key)}
                    disabled={busySchool !== null || (reauthMethodFor(auth.currentUser) === 'password' && !currentPassword)}
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
