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
  LEGAL_URL_RE,
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
/**
 * Render a copy line, turning bare source URLs into real links.
 *
 * The Terms name the official government sources the app draws on (SEC, CAO,
 * SUSI, HEA...) and Google Play's Misleading Claims policy asks for those to be
 * accessible links rather than plain text. split() on a capturing group keeps
 * the URLs in the output array, so the odd indices are the matches.
 */
function withLinks(line: string): React.ReactNode[] {
  LEGAL_URL_RE.lastIndex = 0;
  return line.split(LEGAL_URL_RE).map((part, i) =>
    i % 2 === 1 ? (
      <a
        key={i}
        href={part}
        target="_blank"
        rel="noopener noreferrer"
        className="font-medium text-[#F26B1F] underline underline-offset-2 break-all"
      >
        {part}
      </a>
    ) : (
      part
    ),
  );
}

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
        className="fixed inset-0 z-[300] flex items-end justify-center bg-[#1A1A1A]/55 p-0 sm:items-center sm:p-6"
        onClick={onClose}
      >
        <MotionDiv
          key="legal-card"
          initial={{ opacity: 0, y: 28, scale: 0.985 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: 18, scale: 0.99 }}
          transition={{ type: 'spring', stiffness: 280, damping: 28, mass: 0.85 }}
          className="flex max-h-[94dvh] w-full flex-col overflow-hidden rounded-t-[24px] border-[1.5px] border-[#383838] bg-[#FAFBF6] shadow-[5px_5px_0_0_#383838] sm:max-h-[88dvh] sm:max-w-4xl sm:rounded-[24px] dark:border-zinc-600 dark:bg-zinc-900"
          onClick={(e: React.MouseEvent) => e.stopPropagation()}
        >
          {/* Header */}
          <div className="flex shrink-0 items-center gap-4 border-b border-[#DDD8D2] px-5 py-4 sm:px-8 sm:py-5 dark:border-zinc-700">
            <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl border-[1.5px] border-[#383838] bg-[#FFF0E7] shadow-[2px_2px_0_0_#383838] dark:border-zinc-600 dark:bg-orange-950/30">
              <Icon size={22} strokeWidth={1.8} style={{ color: '#F26B1F' }} />
            </div>
            <div className="flex-1 min-w-0">
              <p className="mb-0.5 text-[10px] font-bold uppercase tracking-[0.2em] text-[#9B9188]">Legal document</p>
              <h2 className="font-serif text-xl font-semibold text-[#1A1A1A] sm:text-2xl dark:text-white">{title}</h2>
              <p className="mt-0.5 text-[11px] text-[#8A8178] sm:text-xs">Version {PRIVACY_POLICY_VERSION} · Updated {LEGAL_LAST_UPDATED}</p>
            </div>
            <button onClick={onClose} aria-label="Close" className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg border-[1.5px] border-[#383838] bg-[#FAFBF6] text-[#383838] transition-transform hover:-translate-y-0.5 active:translate-y-0 dark:border-zinc-600 dark:bg-zinc-900 dark:text-zinc-200">
              <X size={19} />
            </button>
          </div>

          {/* Draft banner */}
          <div className="shrink-0 border-b border-[#DDD8D2] bg-[#FFF8E5] px-5 py-3 sm:px-8 dark:border-zinc-700 dark:bg-amber-950/20">
            <div className="flex items-start gap-2.5">
              <AlertTriangle size={15} className="mt-0.5 shrink-0 text-[#C45A16] dark:text-amber-400" />
              <p className="text-xs leading-relaxed text-[#8F4617] dark:text-amber-200">
                <span className="font-bold">Draft under legal review.</span> The wording may change before final publication.
              </p>
            </div>
          </div>

          <div className="overflow-y-auto">
            <div className="mx-auto grid max-w-4xl sm:grid-cols-[150px_minmax(0,1fr)]">
              <aside className="hidden border-r border-[#DDD8D2] px-6 py-7 sm:block dark:border-zinc-700">
                <p className="text-[10px] font-bold uppercase tracking-[0.18em] text-[#9B9188]">Contents</p>
                <ol className="mt-4 space-y-3">
                  {sections.map((section, index) => (
                    <li key={section.heading} className="flex gap-2 text-[11px] leading-snug text-[#78716C] dark:text-zinc-400">
                      <span className="font-mono text-[#F26B1F]">{String(index + 1).padStart(2, '0')}</span>
                      <span>{section.heading}</span>
                    </li>
                  ))}
                </ol>
              </aside>

              <main className="px-5 py-6 sm:px-8 sm:py-8">
                <div className="space-y-8">
                  {sections.map((section, sectionIndex) => (
                    <section key={section.heading} className="grid grid-cols-[30px_minmax(0,1fr)] gap-3 border-b border-[#E4E0DA] pb-8 last:border-0 last:pb-0 sm:grid-cols-[38px_minmax(0,1fr)]">
                      <span className="pt-1 font-mono text-[10px] font-bold text-[#F26B1F]">{String(sectionIndex + 1).padStart(2, '0')}</span>
                      <div>
                        <h3 className="mb-3 font-serif text-lg font-semibold text-[#1A1A1A] dark:text-white">{section.heading}</h3>
                        <div className="space-y-3">
                          {section.body.map((line, index) =>
                            line.startsWith('• ') ? (
                              <div key={index} className="grid grid-cols-[8px_minmax(0,1fr)] gap-2.5 text-[13px] leading-6 text-[#5F5A55] sm:text-sm dark:text-zinc-300">
                                <span className="mt-[9px] h-1.5 w-1.5 rounded-full bg-[#F26B1F]" aria-hidden />
                                <p>{withLinks(line.slice(2))}</p>
                              </div>
                            ) : (
                              <p key={index} className="text-[13px] leading-6 text-[#5F5A55] sm:text-sm dark:text-zinc-300">{withLinks(line)}</p>
                            )
                          )}
                        </div>
                      </div>
                    </section>
                  ))}
                </div>
              </main>
            </div>
          </div>
        </MotionDiv>
      </MotionDiv>
    </AnimatePresence>,
    document.body
  );
};

export default LegalModal;
