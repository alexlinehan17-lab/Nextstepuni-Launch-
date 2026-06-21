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
import {
  type LegalDoc,
  type Section,
  PRIVACY_NOTICE,
  TERMS_OF_USE,
  PRIVACY_POLICY_VERSION,
  LEGAL_LAST_UPDATED,
} from './legalContent';

// The legal copy + version constants now live in ./legalContent (a
// framework-free single source shared with the build-time generator that emits
// the public /privacy.html + /terms.html pages). Re-exported here so existing
// importers (LoginPage, SettingsModal) keep their import path unchanged.
export {
  PRIVACY_POLICY_VERSION,
  LEGAL_LAST_UPDATED,
  SUPPORT_EMAIL,
  CONSENT_BASIS,
} from './legalContent';
export type { LegalDoc } from './legalContent';

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
