/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, BookOpen } from 'lucide-react';
import { type Reference } from '../data/references/types';

// ─── Citation UX for accredited modules ─────────────────────────────────────
//
//   <Cite n={1} />               — a small superscript marker on a sourced claim.
//   <ReferencesModal … />        — the module-wide references list, opened from a
//                                  button in ModuleLayout (desktop: by the progress
//                                  wheel; mobile: top of the Sections drawer).
//
// The full per-claim verification record lives in
// compliance/evidence/<module>.md (the dossier reviewed for accreditation).

/** Inline superscript citation marker. Deliberately faint — present if wanted,
 *  invisible to the flow if not. The number maps to the References modal list. */
export const Cite: React.FC<{ n: number }> = ({ n }) => (
  <sup className="text-[10px] font-semibold text-zinc-400 dark:text-zinc-500 ml-px select-none">{n}</sup>
);

/** Module-wide references modal. Lists every verified source behind the module,
 *  numbered to match the inline <Cite/> markers. */
export const ReferencesModal: React.FC<{
  open: boolean;
  onClose: () => void;
  references: Reference[];
}> = ({ open, onClose, references }) => (
  <AnimatePresence>
    {open && (
      <>
        <motion.div
          key="refs-backdrop"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={onClose}
          className="fixed inset-0 z-[120] bg-black/40"
        />
        <motion.div
          key="refs-panel"
          initial={{ opacity: 0, y: 16, scale: 0.98 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: 16, scale: 0.98 }}
          transition={{ type: 'spring', damping: 26, stiffness: 320 }}
          role="dialog"
          aria-modal="true"
          aria-label="References"
          className="fixed left-1/2 top-1/2 z-[121] w-[calc(100%-2rem)] max-w-lg -translate-x-1/2 -translate-y-1/2 rounded-2xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 shadow-2xl max-h-[80vh] overflow-y-auto"
        >
          <div className="sticky top-0 flex items-center justify-between gap-3 px-5 py-4 bg-white/95 dark:bg-zinc-900/95 backdrop-blur-sm border-b border-zinc-100 dark:border-zinc-800">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-lg flex items-center justify-center" style={{ backgroundColor: 'rgba(var(--accent),0.1)' }}>
                <BookOpen size={16} style={{ color: 'var(--accent-hex)' }} />
              </div>
              <div>
                <h2 className="text-sm font-semibold text-zinc-900 dark:text-white leading-tight">References</h2>
                <p className="text-[11px] text-zinc-400 dark:text-zinc-500">Verified sources behind this module</p>
              </div>
            </div>
            <button onClick={onClose} className="p-1.5 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800" aria-label="Close references">
              <X size={16} className="text-zinc-400" />
            </button>
          </div>
          <ol className="px-5 py-4 space-y-3">
            {references.map((r, i) => (
              <li key={r.id} className="flex gap-3 text-[13px] leading-relaxed text-zinc-600 dark:text-zinc-300">
                <span className="shrink-0 w-5 text-right font-semibold text-zinc-400 dark:text-zinc-500">{i + 1}.</span>
                <span>
                  {r.authors} ({r.year}). {r.title}. <span className="italic">{r.source}</span>.{' '}
                  {r.doi ? (
                    <a
                      href={`https://doi.org/${r.doi}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="underline decoration-dotted underline-offset-2 hover:text-[var(--accent-hex)] transition-colors break-all"
                    >
                      doi:{r.doi}
                    </a>
                  ) : r.url ? (
                    <a
                      href={r.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="underline decoration-dotted underline-offset-2 hover:text-[var(--accent-hex)] transition-colors break-all"
                    >
                      {r.url.replace(/^https?:\/\/(www\.)?/, '').replace(/\/$/, '')}
                    </a>
                  ) : null}
                </span>
              </li>
            ))}
          </ol>
        </motion.div>
      </>
    )}
  </AnimatePresence>
);
