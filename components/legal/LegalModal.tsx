/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { createPortal } from 'react-dom';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from '../Motion';
import { X, ShieldCheck, FileText, AlertTriangle } from 'lucide-react';
import { useModal } from '../../hooks/useModal';

// ── Version control ─────────────────────────────────────────
// Bump PRIVACY_POLICY_VERSION whenever the substance of the notice changes.
// Registration records the version a student accepted (users/{uid}.consent),
// so a future re-consent prompt can detect an out-of-date acceptance.
export const PRIVACY_POLICY_VERSION = '2026-06-01';
export const LEGAL_LAST_UPDATED = '1 June 2026';
export const SUPPORT_EMAIL = 'nextstepuniinfo@gmail.com';

// The lawful-basis model wired into the app (confirmed 2026-06-01):
// school is Controller (GDPR Art 6(1)(e) public task, in loco parentis) with
// parental consent captured at school enrolment (Art 8). See compliance/DPIA.md.
export const CONSENT_BASIS = 'school-enrolment';

export type LegalDoc = 'privacy' | 'terms';

interface Section { heading: string; body: string[] }

// NOTE: This content is a DRAFT authored from the project's own compliance
// documents (DPIA.md, RETENTION_POLICY.md, DSAR_SPEC.md, DPA_SCHEDULES.md) and
// verified against the code. It is pending review by legal counsel before the
// product ships. Lines beginning with "• " render as bullet points.

const PRIVACY_NOTICE: Section[] = [
  {
    heading: 'About this notice',
    body: [
      'This notice explains, in plain language, what personal information NextStepUni collects when you use the Learning Lab, why we use it, and the choices and rights you have.',
      `It applies to students using NextStepUni. Last updated ${LEGAL_LAST_UPDATED} (version ${PRIVACY_POLICY_VERSION}).`,
    ],
  },
  {
    heading: 'Who looks after your information',
    body: [
      'Your school is the data controller — it decides how your information is used to run this study programme and acts on behalf of you and your parents/guardians.',
      'NextStepUni Ltd is the data processor — we build and run the app and handle your information on your school’s instructions.',
      'PwC Ireland sponsors the programme but is not a controller or processor and never receives any student information.',
      `You can contact NextStepUni about your information at ${SUPPORT_EMAIL}.`,
    ],
  },
  {
    heading: 'What we collect',
    body: [
      '• Account details: your name, your email address, a password (stored only in a scrambled “hashed” form by Google Firebase), and the avatar you choose.',
      '• Your school and year group (for example, 5th or 6th Year).',
      '• Your study setup: the subjects and levels you take, your target grades, your exam start date, your rest days, and your “North Star” goal for after school.',
      '• Your activity: how far you’ve got in each module, your study sessions, points and achievements, mock exam results, and your topic confidence/mastery.',
      '• Your reflections: short notes you write after a study session, and free-text answers to module exercises.',
      '• Peer features: the kudos and gifts you send to classmates at your school.',
      '• Settings: your display preferences, such as dark mode, language and theme.',
    ],
  },
  {
    heading: 'What we do NOT collect',
    body: [
      '• We do not ask for your date of birth or age.',
      '• We do not collect your location beyond the name of your school.',
      '• No biometric data, no advertising identifiers, and no advertising or tracking cookies.',
      '• We do not use any analytics or tracking service.',
      '• We do not send anything you type to any artificial-intelligence service.',
    ],
  },
  {
    heading: 'Why we use your information',
    body: [
      'To run the study programme and show you the right content for your subjects and year; to track your progress, points and streaks; to let your school’s guidance counsellor support you; and to keep your account secure.',
    ],
  },
  {
    heading: 'Our legal basis',
    body: [
      'We rely on a public-interest task (GDPR Article 6(1)(e)): your school delivers a state-curriculum educational service and acts in place of a parent during the school day. Permission from your parent or guardian is obtained when you are enrolled in the programme at your school (Article 8).',
      'If sensitive information ever happens to appear in something you write, we rely on the “substantial public interest (education)” condition (Article 9(2)(g) GDPR and section 41 of the Data Protection Act 2018).',
      'These legal bases are being confirmed with participating schools and our legal advisers.',
    ],
  },
  {
    heading: 'Who can see your information',
    body: [
      '• You can see all of your own information.',
      '• Your school’s guidance counsellor can see your progress and can write private notes to support you.',
      '• Other students at your school can see a limited public version of your island (your name, avatar, school, chosen goal category, and your island decorations and score), plus any kudos you choose to send. Your study sessions, reflections, grades, points and purchases are never shown to other students.',
      '• NextStepUni staff do not routinely read your information by hand — only occasionally to fix a technical problem.',
    ],
  },
  {
    heading: 'Who we share it with',
    body: [
      'Your information is stored using Google Firebase (for login, the database, and server functions). Firebase is our main service provider.',
      'Your profile picture is generated by an avatar service called DiceBear. We only send it the preset avatar name you picked (such as “Maya Angelou”) — never your real name, email, or anything that identifies you.',
      'We do not sell your information and we do not share it for advertising.',
      'Your information is stored in the European Economic Area (London region). Some processing may take place on Google servers outside the EEA, under Google’s data-protection terms.',
    ],
  },
  {
    heading: 'How long we keep it',
    body: [
      'We keep your information while you are in the programme, plus a period afterwards. Our intended policy is to keep it for 12 months after your Leaving Certificate, and then erase the details that identify you. This retention period is being finalised.',
    ],
  },
  {
    heading: 'Your rights',
    body: [
      'You can ask to see a copy of your information, correct it, delete it, or restrict or object to how it is used.',
      `To do any of these, email us at ${SUPPORT_EMAIL} or ask your guidance counsellor. We will respond within one month. These requests are currently handled by our team by hand.`,
      'If you are unhappy with how your information is handled, you can complain to the Irish Data Protection Commission at dataprotection.ie.',
    ],
  },
  {
    heading: 'Changes & contact',
    body: [
      'We may update this notice. When we do, we will change the version date at the top.',
      `Questions about your privacy: ${SUPPORT_EMAIL}.`,
    ],
  },
];

const TERMS_OF_USE: Section[] = [
  {
    heading: 'About these terms',
    body: [
      'These terms are the agreement between you and NextStepUni Ltd for using the Learning Lab. By creating an account and using NextStepUni, you agree to them.',
      `Last updated ${LEGAL_LAST_UPDATED} (version ${PRIVACY_POLICY_VERSION}).`,
    ],
  },
  {
    heading: 'Who can use NextStepUni',
    body: [
      'NextStepUni is for students taking part in the programme through a participating school. You will normally have been set up through your school with your parent or guardian’s permission.',
    ],
  },
  {
    heading: 'Your account',
    body: [
      '• Keep your password private and don’t share your account with anyone.',
      '• Give accurate information when you sign up.',
      '• Use one account that belongs to you.',
      '• You’re responsible for what happens on your account.',
    ],
  },
  {
    heading: 'Being a good classmate',
    body: [
      'The peer features (kudos and gifts) are for supporting other students at your school. Be kind and respectful.',
      'No bullying, harassment, or inappropriate content. Your peer activity can be seen by your guidance counsellor.',
      'Misusing these features can lead to them — or your account — being suspended.',
    ],
  },
  {
    heading: 'Our content',
    body: [
      'The learning content in NextStepUni is for your own personal study. Please don’t copy, sell or share it outside the app.',
    ],
  },
  {
    heading: 'Availability',
    body: [
      'NextStepUni is provided “as is” while we keep improving it. It is in active development, so we can’t promise it will always be available or completely error-free.',
    ],
  },
  {
    heading: 'Suspension',
    body: [
      'Your school or NextStepUni may suspend or remove access if these terms are broken, or where needed to protect students.',
    ],
  },
  {
    heading: 'Changes, law & contact',
    body: [
      'We may update these terms; we’ll change the version date at the top when we do. These terms are governed by the laws of Ireland.',
      `Questions: ${SUPPORT_EMAIL}.`,
    ],
  },
];

const DOC_META: Record<LegalDoc, { title: string; Icon: typeof ShieldCheck; sections: Section[] }> = {
  privacy: { title: 'Privacy Notice', Icon: ShieldCheck, sections: PRIVACY_NOTICE },
  terms: { title: 'Terms of Use', Icon: FileText, sections: TERMS_OF_USE },
};

interface LegalModalProps {
  /** Which document to show, or null to render nothing. */
  doc: LegalDoc | null;
  onClose: () => void;
}

/**
 * Full-screen, scrollable overlay rendering the Privacy Notice or Terms of Use.
 * Reachable from registration (LoginPage) and from Settings.
 */
export const LegalModal: React.FC<LegalModalProps> = ({ doc, onClose }) => {
  useModal(!!doc, onClose);
  if (!doc) return null;
  const { title, Icon, sections } = DOC_META[doc];

  return createPortal(
    <AnimatePresence>
      <MotionDiv
        key="legal-backdrop"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 z-[300] flex items-end sm:items-center justify-center bg-black/50 backdrop-blur-sm p-0 sm:p-4"
        onClick={onClose}
      >
        <MotionDiv
          key="legal-card"
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: 24 }}
          className="bg-white dark:bg-zinc-900 w-full sm:max-w-2xl max-h-[92vh] sm:max-h-[85vh] rounded-t-2xl sm:rounded-2xl border border-zinc-200 dark:border-zinc-800 shadow-2xl flex flex-col overflow-hidden"
          onClick={(e: React.MouseEvent) => e.stopPropagation()}
        >
          {/* Header */}
          <div className="flex items-center gap-3 px-5 py-4 border-b border-zinc-100 dark:border-zinc-800 shrink-0">
            <div className="w-9 h-9 rounded-xl flex items-center justify-center" style={{ backgroundColor: 'rgba(242,107,31,0.1)' }}>
              <Icon size={18} style={{ color: '#F26B1F' }} />
            </div>
            <div className="flex-1 min-w-0">
              <h2 className="text-base font-semibold text-zinc-900 dark:text-white" style={{ fontFamily: "'Source Serif 4', serif" }}>{title}</h2>
              <p className="text-[11px] text-zinc-400">Version {PRIVACY_POLICY_VERSION} · Updated {LEGAL_LAST_UPDATED}</p>
            </div>
            <button onClick={onClose} aria-label="Close" className="p-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-white/[0.06] transition-colors">
              <X size={18} className="text-zinc-500" />
            </button>
          </div>

          {/* Draft banner */}
          <div className="flex items-start gap-2 px-5 py-2.5 bg-amber-50 dark:bg-amber-900/15 border-b border-amber-100 dark:border-amber-900/30 shrink-0">
            <AlertTriangle size={14} className="text-amber-600 dark:text-amber-400 mt-0.5 shrink-0" />
            <p className="text-[11px] leading-snug text-amber-700 dark:text-amber-300">
              Draft — under review by our legal advisers. The wording may change before final publication.
            </p>
          </div>

          {/* Body */}
          <div className="overflow-y-auto px-5 py-4 space-y-5">
            {sections.map((s) => (
              <section key={s.heading}>
                <h3 className="text-sm font-semibold text-zinc-900 dark:text-white mb-1.5" style={{ fontFamily: "'Source Serif 4', serif" }}>{s.heading}</h3>
                <div className="space-y-1.5">
                  {s.body.map((line, i) =>
                    line.startsWith('• ') ? (
                      <p key={i} className="text-[13px] leading-relaxed text-zinc-600 dark:text-zinc-300 pl-4 -indent-4">{line}</p>
                    ) : (
                      <p key={i} className="text-[13px] leading-relaxed text-zinc-600 dark:text-zinc-300">{line}</p>
                    )
                  )}
                </div>
              </section>
            ))}
          </div>
        </MotionDiv>
      </MotionDiv>
    </AnimatePresence>,
    document.body
  );
};

export default LegalModal;
