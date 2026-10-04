import React, { useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { DEMO_STUDENT_UID } from '../../data/devStudent';
import { type SessionUser, isSchoolStaff } from '../../utils/authUtils';
import { useModal } from '../../hooks/useModal';
import { hasCurrentLegalAcceptance } from '../../functions/src/legalAgreementPolicy';
import { recordLegalAcceptance, takeRegistrationAgreement, watchLegalAcceptance } from '../../services/legalAgreement';
import { SUPPORT_EMAIL, type LegalDoc } from './legalContent';
import { LegalModal } from './LegalModal';
import './legal-document.css';

/** Student/staff use waits for a current record. Company operators and demos
 * are not parties to the school-user Terms. Admin identity is verified by AuthContext. */
export function LegalAgreementGate({ user, ready, onLogout, children }: {
  user: SessionUser | null;
  ready: boolean;
  onLogout: () => Promise<void>;
  children: React.ReactNode;
}) {
  if (!user || !ready || user.isAdmin || user.uid === DEMO_STUDENT_UID) return <>{children}</>;
  return <AccountLegalReview key={user.uid} user={user} onLogout={onLogout}>{children}</AccountLegalReview>;
}

function AccountLegalReview({ user, onLogout, children }: {
  user: SessionUser;
  onLogout: () => Promise<void>;
  children: React.ReactNode;
}) {
  const student = !user.isAdmin && !isSchoolStaff(user.role);
  const [status, setStatus] = useState<'checking' | 'review' | 'accepted' | 'error'>('checking');
  const [retry, setRetry] = useState(0);
  const [agreed, setAgreed] = useState(false);
  const [ageConfirmed, setAgeConfirmed] = useState(false);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');
  const [doc, setDoc] = useState<LegalDoc | null>(null);
  const active = useRef(true);
  useEffect(() => { active.current = true; return () => { active.current = false; }; }, []);
  const dialogRef = useRef<HTMLElement>(null);
  useModal(status !== 'accepted' && !doc, () => {}, dialogRef, { closeDisabled: true, initialFocus: 'dialog' });

  useEffect(() => {
    let mounted = true;
    let autoSubmitted = false;
    setStatus('checking');
    const timeout = window.setTimeout(() => { if (mounted) setStatus('error'); }, 10000);
    const unsubscribe = watchLegalAcceptance(user.uid, value => {
      if (!mounted) return;
      window.clearTimeout(timeout);
      if (hasCurrentLegalAcceptance(value, student)) { takeRegistrationAgreement(user.uid); setStatus('accepted'); return; }
      if (!autoSubmitted && takeRegistrationAgreement(user.uid)) {
        autoSubmitted = true;
        setSaving(true);
        recordLegalAcceptance(true).then(() => {
          if (mounted) setStatus('accepted');
        }).catch(() => {
          if (mounted) { setStatus('review'); setMessage('We could not save your agreement. Please review and try again.'); }
        }).finally(() => { if (mounted) setSaving(false); });
      } else if (!autoSubmitted) setStatus('review');
    }, () => { if (mounted) { window.clearTimeout(timeout); setStatus('error'); } });
    return () => { mounted = false; window.clearTimeout(timeout); unsubscribe(); };
  }, [user.uid, student, retry]);

  const submit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!agreed || (student && !ageConfirmed) || saving) return;
    setSaving(true); setMessage('');
    try {
      await recordLegalAcceptance(student && ageConfirmed);
      if (active.current) setStatus('accepted');
    } catch {
      if (active.current) setMessage('Your agreement has not been saved. Check your connection and try again.');
    } finally { if (active.current) setSaving(false); }
  };
  if (status === 'accepted') return <>{children}</>;
  return createPortal(<>
    <div className="legal-agreement-screen" inert={!!doc} aria-hidden={doc ? true : undefined}>
      <section ref={dialogRef} tabIndex={-1}
        className="legal-document legal-dialog legal-agreement" role="dialog" aria-modal="true" aria-labelledby="legal-agreement-title" aria-describedby="legal-agreement-description">
        <p className="legal-wordmark">NextStep<span>Uni</span></p>
        <p className="legal-label">Your account · Updated documents</p>
        <h1 id="legal-agreement-title">Before you begin<span>.</span></h1>
        <p id="legal-agreement-description">Review how your information is handled and the rules for using your school workspace.</p>
        <nav className="legal-agreement-documents" aria-label="Review documents">
          <button type="button" onClick={() => setDoc('privacy')}>Read Privacy Notice <span aria-hidden="true">↗</span></button>
          <button type="button" onClick={() => setDoc('terms')}>Read Terms of Use <span aria-hidden="true">↗</span></button>
        </nav>
        {status === 'checking' ? <p role="status">{saving ? 'Saving your agreement…' : 'Checking your account…'}</p> : status === 'error' ? <>
          <p role="alert">We could not check your account. Your agreement has not been assumed.</p>
          <button className="legal-agreement-continue" onClick={() => setRetry(value => value + 1)}>Try again</button>
        </> : <form onSubmit={submit}>
          <label className="legal-agreement-check"><input type="checkbox" checked={agreed} disabled={saving} onChange={event => setAgreed(event.target.checked)} /><span>I have read the Privacy Notice and agree to the Terms of Use.</span></label>
          {student && <label className="legal-agreement-check"><input type="checkbox" checked={ageConfirmed} disabled={saving} onChange={event => setAgeConfirmed(event.target.checked)} /><span>I am aged 16 or over and eligible for my school’s programme.</span></label>}
          <p className="legal-agreement-note">This records your acknowledgement and agreement. It is not blanket consent to use your information.</p>
          {message && <p role="alert">{message}</p>}
          <button className="legal-agreement-continue" disabled={!agreed || (student && !ageConfirmed) || saving}>{saving ? 'Saving…' : 'Agree & continue'} <span aria-hidden="true">↗</span></button>
        </form>}
        <div className="legal-agreement-exit"><button type="button" onClick={() => { void onLogout(); }}>Sign out</button><a href={`mailto:${SUPPORT_EMAIL}`}>Need help?</a></div>
        <p className="legal-agreement-note">Prefer not to agree? You can <a href={`mailto:${SUPPORT_EMAIL}?subject=Account%20data%20request`}>request a data copy or account deletion</a> by email.</p>
      </section>
    </div>
    <LegalModal doc={doc} onClose={() => setDoc(null)} onDocumentChange={setDoc} />
  </>, document.body);
}
