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

import React, { useEffect, useState, useCallback, useRef } from 'react';
import { getFunctions, httpsCallable } from 'firebase/functions';
import { Check, Copy, Lock, RefreshCw } from 'lucide-react';
import app, { auth } from '../../firebase';
import { getSchoolName } from '../../schoolData';
import { reauthMethodFor, reauthenticateCurrentUser } from '../../utils/reauthenticate';
import { Button } from '../ui/Button';
import { Field } from '../ui/Field';
import { PaperSheet } from '../ui/List';
import { Sheet } from '../ui/Sheet';
import { LoadingShape } from '../ui/States';
import { useWide } from './gcView';

export const StaffAccessPanel: React.FC<{ school: string }> = ({ school }) => {
  const [studentConfigured, setStudentConfigured] = useState(false);
  const [studentCode, setStudentCode] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [copied, setCopied] = useState(false);
  const [error, setError] = useState('');
  const [confirming, setConfirming] = useState(false);
  const [password, setPassword] = useState('');
  const wide = useWide();
  const passwordRef = useRef<HTMLInputElement>(null);

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

  const needsPassword = reauthMethodFor(auth.currentUser) === 'password';
  return (
    <div className="gc8-narrow">
      <section className="gc8-head" aria-labelledby="gc8-access">
        <h1 id="gc8-access" className={wide ? 'gc8-title' : 'gc8-name'}>School access</h1>
        <p className="gc8-sub">
          The student join code for {getSchoolName(school)}. Teachers do not need a code: they sign in
          with the staff-room password your school was given.
        </p>
      </section>

      {loading ? <LoadingShape rows={2} label="Loading…" /> : (
        <PaperSheet label="Student join code">
          <div className="gc8-code">
            <p className="gc8-label">Student join code</p>
            <p className="gc8-sub">Students use this during registration. It remains active until you rotate it.</p>
            {studentCode ? (
              <>
                <div className="gc8-row-x">
                  <code className="gc8-code-value">{studentCode}</code>
                  <Button size="sm" className="gc8-ib" onClick={() => void copy()}>
                    {copied
                      ? <><Check className="ui-icon gc8-up" width={16} height={16} strokeWidth={2} aria-hidden="true" />Copied</>
                      : <><Copy className="ui-icon" width={16} height={16} strokeWidth={2} aria-hidden="true" />Copy</>}
                  </Button>
                </div>
                <p className="gc8-sub gc8-strong">Copy this now. For security, it will not be shown again.</p>
              </>
            ) : (
              <p className="gc8-strong">
                {studentConfigured ? 'A code is active. Generate a new one if it needs to be shared again.' : 'No code is active yet.'}
              </p>
            )}
            <Button className="gc8-ib" onClick={() => { if (saving) return; setError(''); setConfirming(true); }} aria-disabled={saving || undefined}>
              <RefreshCw className="ui-icon" width={16} height={16} strokeWidth={2} aria-hidden="true" /> {studentConfigured ? 'Rotate code' : 'Generate code'}
            </Button>
          </div>
        </PaperSheet>
      )}

      {error && <p role="alert" className="gc8-strong">{error}</p>}
      <p className="gc8-note">
        <Lock className="ui-icon" width={14} height={14} strokeWidth={2} aria-hidden="true" /> The code is stored as a one-way hash and shown only when generated. Rotate it to stop future joins.
      </p>

      <Sheet
        open={confirming}
        title="Verify this security change"
        onClose={() => { if (!saving) closeConfirm(); }}
        footer={
          <Button
            kind="main"
            size="lg"
            block
            missing={needsPassword && !password ? { sentence: 'Re-enter your password before rotating the join code.', goTo: passwordRef } : undefined}
            onClick={() => { if (!saving) void rotate(); }}
          >
            {saving ? 'Working…' : 'Confirm'}
          </Button>
        }
      >
        <div className="gc8-sheet-body">
          {/* Today's line; while the password is missing the button's own line says it, so it shows once. */}
          {!(needsPassword && !password) && <p className="gc8-sub">Re-enter your password before rotating the join code.</p>}
          {error && <p className="gc8-strong">{error}</p>}
          {needsPassword && (
            <Field
              ref={passwordRef}
              type="password"
              label="Your password"
              placeholder="Your password"
              value={password}
              onChange={event => setPassword(event.target.value)}
              autoComplete="current-password"
            />
          )}
        </div>
      </Sheet>
    </div>
  );
};

export default StaffAccessPanel;
