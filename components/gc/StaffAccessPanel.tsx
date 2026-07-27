/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useEffect, useState, useCallback } from 'react';
import { doc, getDoc, setDoc } from 'firebase/firestore';
import { db } from '../../firebase';
import { awaitWriteOrTimeout } from '../../utils/firestoreWrite';
import { KeyRound, Copy, Check, RefreshCw, ShieldCheck } from 'lucide-react';
import { getSchoolName } from '../../schoolData';

/**
 * Staff Access panel — a guidance counsellor generates and shares the school's
 * staff code so teachers can gain dashboard access (see
 * compliance/STAFF_DASHBOARD_PLAN.md). The code lives in
 * gcSettings/{school}.staffCode: staff-writable, student-unreadable. Redemption
 * is verified server-side by the claimStaffAccess Cloud Function.
 */

// Unambiguous alphabet (no O/0/I/1/L) for a code that's easy to read aloud.
const CODE_ALPHABET = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789';

function generateCode(): string {
  const bytes = new Uint32Array(10);
  crypto.getRandomValues(bytes);
  let raw = '';
  for (let i = 0; i < bytes.length; i++) raw += CODE_ALPHABET[bytes[i] % CODE_ALPHABET.length];
  // Format as XXXXX-XXXXX for readability.
  return `${raw.slice(0, 5)}-${raw.slice(5)}`;
}

export const StaffAccessPanel: React.FC<{ school: string }> = ({ school }) => {
  const [code, setCode] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [copied, setCopied] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const snap = await getDoc(doc(db, 'gcSettings', school));
        if (!cancelled) setCode((snap.exists() ? (snap.data()?.staffCode as string | undefined) : undefined) ?? null);
      } catch (err) {
        console.error('[StaffAccess] failed to load code:', err);
        if (!cancelled) setError('Could not load the staff code.');
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => { cancelled = true; };
  }, [school]);

  const regenerate = useCallback(async () => {
    setSaving(true); setError(''); setCopied(false);
    const next = generateCode();
    // This is the ONE flow that must be durable before it is reported.
    //
    // The code is verified server-side by the claimStaffAccess function reading
    // gcSettings directly, so a locally-cached-but-unflushed code does not work
    // yet: the OLD code still grants staff access (the revocation silently
    // hasn't happened), and every teacher trying the NEW one gets a mismatch —
    // burning the 6-attempt/15-minute brute-force lockout on a code the server
    // has never seen. So: bounded wait, and only reveal on a real ack.
    const outcome = await awaitWriteOrTimeout(
      setDoc(doc(db, 'gcSettings', school), { staffCode: next }, { merge: true }),
      'StaffAccess.regenerateCode',
      8000,
    );
    setSaving(false);
    if (outcome === 'acked') {
      setCode(next);
    } else if (outcome === 'pending') {
      setError('Not saved yet — still syncing. The old code is still active; don\'t share the new one until this succeeds.');
    } else {
      setError('Could not save the new code. Try again.');
    }
  }, [school]);

  const copy = useCallback(async () => {
    if (!code) return;
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 1800);
    } catch { /* clipboard may be unavailable; the code is visible to copy manually */ }
  }, [code]);

  return (
    <div className="p-6 max-w-2xl mx-auto w-full">
      <div className="flex items-center gap-2.5 mb-1">
        <KeyRound size={20} className="text-zinc-500 dark:text-zinc-400" />
        <h2 className="text-xl font-semibold tracking-tight text-zinc-900 dark:text-white">Staff access</h2>
      </div>
      <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-6">
        Share this code with teachers at {getSchoolName(school)} so they can access the Staff Dashboard.
        Teachers choose <span className="font-medium">Teacher / staff access</span> on the sign-in screen and enter this code.
      </p>

      <div className="rounded-2xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 p-6">
        {loading ? (
          <p className="text-sm text-zinc-400">Loading…</p>
        ) : (
          <>
            <p className="text-[11px] font-semibold uppercase tracking-widest text-zinc-400 mb-2">Current staff code</p>
            {code ? (
              <div className="flex items-center gap-3 flex-wrap">
                <code className="text-2xl font-bold tracking-[0.2em] text-zinc-900 dark:text-white select-all">{code}</code>
                <button
                  onClick={copy}
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium border border-zinc-200 dark:border-zinc-700 text-zinc-600 dark:text-zinc-300 hover:bg-zinc-50 dark:hover:bg-zinc-800 transition-colors"
                >
                  {copied ? <><Check size={13} className="text-green-600" /> Copied</> : <><Copy size={13} /> Copy</>}
                </button>
              </div>
            ) : (
              <p className="text-sm text-zinc-500 dark:text-zinc-400">No code yet. Generate one to let teachers in.</p>
            )}

            <div className="mt-5 flex items-center gap-3 flex-wrap">
              <button
                onClick={regenerate}
                disabled={saving}
                className="inline-flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium bg-zinc-900 dark:bg-white text-white dark:text-zinc-900 hover:opacity-90 transition-opacity disabled:opacity-50"
              >
                <RefreshCw size={14} className={saving ? 'animate-spin' : ''} />
                {code ? 'Regenerate code' : 'Generate code'}
              </button>
              {code && (
                <span className="inline-flex items-center gap-1.5 text-xs text-zinc-400">
                  <ShieldCheck size={13} /> Regenerating immediately revokes the old code.
                </span>
              )}
            </div>
            {error && <p className="text-sm text-red-500 mt-3">{error}</p>}
          </>
        )}
      </div>

      <p className="text-xs text-zinc-400 mt-4 leading-relaxed">
        Teachers who redeem this code get the same view you have, for {getSchoolName(school)} only —
        including student progress and welfare notes. Only share it with staff. Regenerate it if it may
        have leaked; anyone who already has access keeps it, but the old code stops working for new sign-ups.
      </p>
    </div>
  );
};
