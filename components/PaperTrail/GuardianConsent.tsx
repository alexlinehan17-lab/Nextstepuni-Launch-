/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Weekly guardian-summary consent (feature E10). Lets a student add a parent/
 * guardian email and switch on an opt-in weekly effort summary — with a preview
 * of exactly what would be sent (effort, never grades). Consent is stored in the
 * student's own settings doc. Ship-gated: renders nothing until
 * GUARDIAN_EMAILS_LIVE is on (see compliance/guardian-summary-plan.md).
 */

import React, { useEffect, useState } from 'react';
import { Mail, Check } from 'lucide-react';
import {
  GUARDIAN_EMAILS_LIVE,
  buildGuardianEmail,
  loadGuardianConsent,
  saveGuardianConsent,
  type GuardianWeekSummary,
} from '../../data/guardianSummary';

const INK = '#1a1a1a';
const ACCENT = '#F26B1F';
const validEmail = (e: string) => /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(e);

const GuardianConsent: React.FC<{ uid?: string; preview: GuardianWeekSummary }> = ({ uid, preview }) => {
  const [email, setEmail] = useState('');
  const [optIn, setOptIn] = useState(false);
  const [saved, setSaved] = useState(false);
  const [showPreview, setShowPreview] = useState(false);

  useEffect(() => {
    if (!GUARDIAN_EMAILS_LIVE || !uid) return;
    loadGuardianConsent(uid).then(c => {
      if (c) {
        setEmail(c.email);
        setOptIn(c.optIn);
      }
    });
  }, [uid]);

  if (!GUARDIAN_EMAILS_LIVE) return null;

  const canSave = !optIn || validEmail(email);
  const save = () => {
    if (uid && canSave) {
      saveGuardianConsent(uid, { email: email.trim(), optIn });
      setSaved(true);
    }
  };
  const mail = buildGuardianEmail(preview);

  return (
    <div className="rounded-2xl border-2 border-[#1a1a1a] dark:border-zinc-700 bg-white dark:bg-zinc-900 px-4 py-4 mb-6">
      <p className="text-[14px] font-semibold mb-1 flex items-center gap-1.5" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>
        <Mail size={16} style={{ color: ACCENT }} /> Weekly update for a parent or guardian
      </p>
      <p className="text-[12.5px] leading-relaxed mb-3" style={{ color: '#7a7068' }}>
        Opt in to send one short weekly email about your <b>effort</b> — minutes revised, questions practised, your streak. Never any grades or marks.
      </p>
      <div className="flex flex-wrap items-center gap-2 mb-2">
        <input
          type="email"
          value={email}
          onChange={e => { setEmail(e.target.value); setSaved(false); }}
          placeholder="guardian@example.com"
          className="flex-1 min-w-[180px] px-3 py-2 rounded-lg border-2 border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-900 text-[13.5px] outline-none focus:border-[#1a1a1a]"
        />
        <label className="flex items-center gap-1.5 text-[12.5px] font-medium" style={{ color: INK }}>
          <input type="checkbox" checked={optIn} onChange={e => { setOptIn(e.target.checked); setSaved(false); }} /> Send weekly
        </label>
        <button onClick={save} disabled={!canSave} className="px-4 py-2 rounded-full text-[13px] font-semibold text-white disabled:opacity-40 transition-transform active:translate-y-0.5" style={{ backgroundColor: ACCENT, boxShadow: '0 3px 0 #B54D14' }}>
          {saved ? <span className="inline-flex items-center gap-1"><Check size={13} /> Saved</span> : 'Save'}
        </button>
      </div>
      <button onClick={() => setShowPreview(v => !v)} className="text-[12px] font-semibold" style={{ color: ACCENT }}>
        {showPreview ? 'Hide preview' : 'Preview the email'}
      </button>
      {showPreview && (
        <div className="mt-2 rounded-xl border border-zinc-200 dark:border-zinc-700 bg-zinc-50 dark:bg-zinc-800/40 px-3.5 py-3">
          <p className="text-[12px] font-bold mb-1" style={{ color: INK }}>Subject: {mail.subject}</p>
          <p className="text-[12.5px] leading-relaxed" style={{ color: '#5a5550' }}>{mail.text}</p>
        </div>
      )}
      <p className="text-[11px] mt-2" style={{ color: '#9e9186' }}>Your guardian can unsubscribe from any email. You can switch this off any time.</p>
    </div>
  );
};

export default GuardianConsent;
