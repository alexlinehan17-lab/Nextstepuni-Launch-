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
import React, { useRef, useState } from 'react';
import { getFunctions, httpsCallable } from 'firebase/functions';
import { Check, Copy, Eye, EyeOff, KeyRound, LoaderCircle, Shuffle, X } from 'lucide-react';
import app, { auth } from '../firebase';
import { SCHOOLS } from '../schoolData';
import { reauthMethodFor, reauthenticateCurrentUser } from '../utils/reauthenticate';
import { Button, IconButton } from './ui/Button';
import { Field } from './ui/Field';

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
  const currentRef = useRef<HTMLInputElement>(null);
  const chosenRef = useRef<HTMLInputElement>(null);

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

  const needsCurrent = reauthMethodFor(auth.currentUser) === 'password' && !currentPassword;
  const glyph = (Icon: typeof KeyRound, spin = false) => (
    <Icon className={`ui-icon${spin ? ' adm-spin' : ''}`} width={16} height={16} strokeWidth={2} aria-hidden="true" />
  );

  return (
    <section aria-label="School logins" className="adm-access">
      <header className="gc8-head adm-head">
        <p className="gc8-label">School access</p>
        <h1 className="gc8-name">School logins</h1>
        <p className="gc8-sub">
          Each school has two shared logins: the guidance counsellor&apos;s and the staff room&apos;s.
          Both sign in with the school name and a password. There is no email inbox behind them, so
          the usual reset link cannot work. Setting a password here takes effect immediately and shows
          it once; send it to the school and their onboarding is done.
        </p>
      </header>

      {error && <p role="alert" className="adm-alert">{error}</p>}

      {pendingAdoption && (
        <div role="alert" className="adm-notice">
          <p className="gc8-label">This login already has an account</p>
          <p className="adm-notice-text adm-ink">{pendingAdoption.message}</p>
          <p className="adm-notice-text">
            If you do not recognise it, someone else may have registered this address. Check it in the
            Firebase console before continuing — adopting it grants that account access to every student
            record in the school.
          </p>
          <div className="adm-btnrow">
            <Button
              onClick={() => {
                const { loginKey, password } = pendingAdoption;
                setPendingAdoption(null);
                void reset(loginKey, password, true);
              }}
            >
              I recognise it — adopt
            </Button>
            <Button kind="main" onClick={() => setPendingAdoption(null)}>Stop</Button>
          </div>
        </div>
      )}

      {result && (
        <div role="status" className="adm-notice">
          <p className="gc8-label">
            {result.generated ? 'New password for' : 'Password set for'} {result.email}
          </p>
          <div className="adm-secretrow">
            <code className="gc8-code-value adm-secret">{result.password}</code>
            <Button className="gc8-ib" onClick={() => void copy()}>
              {copied ? glyph(Check) : glyph(Copy)}{copied ? 'Copied' : 'Copy'}
            </Button>
          </div>
          <p className="gc8-meta">
            {result.generated
              ? 'Shown once and never stored — copy it now. '
              : 'Set as typed, and not stored anywhere. '}
            The old password stopped working the moment this appeared, so anyone signed in at that
            school will need this to get back in.
          </p>
        </div>
      )}

      <ul className="adm-logins">
        {SCHOOLS.flatMap(school => (['gc', 'staff'] as const).map(kind => ({ school, kind, key: `${kind}:${school.id}` }))).map(({ school, kind, key }) => (
          <li key={key} className="adm-login">
            <p className="adm-lwho">
              <span className="gc8-person">{school.name}</span>
              <span className="gc8-meta">{kind === 'gc' ? 'Guidance counsellor' : 'Staff room'}</span>
            </p>
            <p className="gc8-readout adm-addr">{kind}-{school.id}@nextstep.app</p>
            <Button
              className="gc8-ib"
              onClick={() => { if (busySchool !== null) return; if (openSchool === key) closeRow(); else { closeRow(); setOpenSchool(key); } }}
              aria-disabled={busySchool !== null || undefined}
              aria-expanded={openSchool === key}
            >
              {busySchool === key
                ? glyph(LoaderCircle, true)
                : openSchool === key ? glyph(X) : glyph(KeyRound)}
              {busySchool === key
                ? 'Resetting…'
                : openSchool === key ? 'Cancel' : 'Set password'}
            </Button>

            {openSchool === key && (
              <div className="adm-setpw">
                {reauthMethodFor(auth.currentUser) === 'password' && (
                  <Field
                    ref={currentRef}
                    id={`current-pw-${key}`}
                    type="password"
                    label="Your current administrator password"
                    value={currentPassword}
                    onChange={event => setCurrentPassword(event.target.value)}
                    autoComplete="current-password"
                  />
                )}
                <div className="adm-pwfield">
                  <Field
                    ref={chosenRef}
                    id={`pw-${key}`}
                    className="adm-mono"
                    type={showChosen ? 'text' : 'password'}
                    label="Choose a password"
                    value={chosen}
                    onChange={event => setChosen(event.target.value)}
                    autoComplete="new-password"
                    placeholder={`At least ${MIN_SUPPLIED_PASSWORD_LENGTH} characters`}
                  />
                  <IconButton
                    className="adm-eye"
                    label={showChosen ? 'Hide password' : 'Show password'}
                    onClick={() => setShowChosen(v => !v)}
                    icon={showChosen
                      ? <EyeOff className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" />
                      : <Eye className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" />}
                  />
                </div>
                <div className="adm-btnrow">
                  <Button
                    // While the "already has an account" notice asks you to choose, its Stop is the one charcoal button.
                    kind={pendingAdoption ? 'second' : 'main'}
                    missing={needsCurrent
                      ? { sentence: 'Re-enter your password to continue.', goTo: currentRef }
                      : chosen.length < MIN_SUPPLIED_PASSWORD_LENGTH
                        ? { sentence: `Choose a password of at least ${MIN_SUPPLIED_PASSWORD_LENGTH} characters.`, goTo: chosenRef }
                        : undefined}
                    onClick={() => { if (busySchool === null) void reset(key, chosen); }}
                  >
                    Set password
                  </Button>
                  <Button
                    className="gc8-ib"
                    aria-disabled={needsCurrent || busySchool !== null || undefined}
                    onClick={() => {
                      // The sentence over Set password already says what is missing; this goes there too.
                      if (needsCurrent) { currentRef.current?.focus(); return; }
                      if (busySchool === null) void reset(key);
                    }}
                  >
                    {glyph(Shuffle)}Generate one
                  </Button>
                </div>
                <p className="gc8-meta">
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
