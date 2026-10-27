/**
 * "Now" pane for review section 05: the legal modal and the consent gate.
 *
 * The modal is the REAL components/legal/LegalModal.tsx, mounted open on the
 * Privacy Notice with its Privacy / Terms switcher (its own portal, backdrop,
 * blur, shadow and LegalDiatype type). Close it (X, Escape or the backdrop)
 * to see the gate underneath; the gate's "Read …" buttons open it again.
 *
 * The gate is NOT the real LegalAgreementGate, because it cannot reach its
 * review state without an account: its inner AccountLegalReview is not
 * exported, and it only leaves "checking" when a Firestore SERVER snapshot of
 * the signed-in user's users/{uid} doc arrives (services/legalAgreement.ts,
 * watchLegalAcceptance ignores cached snapshots). With no account it shows the
 * spinner for ten seconds and then its error screen. So the gate below is a
 * verbatim copy of AccountLegalReview's review-state markup (the createPortal
 * block in components/legal/LegalAgreementGate.tsx) for a student, with the
 * same class names on the real legal-document.css and the real LegalModal.
 * Its checkboxes are local state; Agree & continue records nothing.
 */
import React, { useState } from 'react';
import { createPortal } from 'react-dom';
import { LegalModal } from '../../components/legal/LegalModal';
import { SUPPORT_EMAIL, type LegalDoc } from '../../components/legal/legalContent';
import '../../components/legal/legal-document.css';

export default function LegalBefore() {
  const [doc, setDoc] = useState<LegalDoc | null>('privacy');
  const [agreed, setAgreed] = useState(false);
  const [ageConfirmed, setAgeConfirmed] = useState(false);
  const student = true;
  const saving = false;

  // Copy of LegalAgreementGate.tsx (status === 'review'), unchanged markup.
  const gate = createPortal(
    <div className="legal-agreement-screen" inert={!!doc} aria-hidden={doc ? true : undefined}>
      <section tabIndex={-1}
        className="legal-document legal-dialog legal-agreement" role="dialog" aria-modal="true" aria-labelledby="legal-agreement-title" aria-describedby="legal-agreement-description">
        <p className="legal-wordmark">nextstepuni</p>
        <p className="legal-label">Your account · Updated documents</p>
        <h1 id="legal-agreement-title">Before you begin<span>.</span></h1>
        <p id="legal-agreement-description">Review how your information is handled and the rules for using your school workspace.</p>
        <nav className="legal-agreement-documents" aria-label="Review documents">
          <button type="button" onClick={() => setDoc('privacy')}>Read Privacy Notice <span aria-hidden="true">↗</span></button>
          <button type="button" onClick={() => setDoc('terms')}>Read Terms of Use <span aria-hidden="true">↗</span></button>
        </nav>
        <form onSubmit={event => event.preventDefault()}>
          <label className="legal-agreement-check"><input type="checkbox" checked={agreed} disabled={saving} onChange={event => setAgreed(event.target.checked)} /><span>I have read the Privacy Notice and agree to the Terms of Use.</span></label>
          {student && <label className="legal-agreement-check"><input type="checkbox" checked={ageConfirmed} disabled={saving} onChange={event => setAgeConfirmed(event.target.checked)} /><span>I am aged 16 or over and eligible for my school’s programme.</span></label>}
          <p className="legal-agreement-note">This records your acknowledgement and agreement. It is not blanket consent to use your information.</p>
          <button className="legal-agreement-continue" disabled={!agreed || (student && !ageConfirmed) || saving}>{saving ? 'Saving…' : 'Agree & continue'} <span aria-hidden="true">↗</span></button>
        </form>
        <div className="legal-agreement-exit"><button type="button">Sign out</button><a href={`mailto:${SUPPORT_EMAIL}`}>Need help?</a></div>
        <p className="legal-agreement-note">Prefer not to agree? You can <a href={`mailto:${SUPPORT_EMAIL}?subject=Account%20data%20request`}>request a data copy or account deletion</a> by email.</p>
      </section>
    </div>,
    document.body,
  );

  return (
    <>
      {gate}
      <LegalModal doc={doc} onClose={() => setDoc(null)} onDocumentChange={setDoc} />
    </>
  );
}
