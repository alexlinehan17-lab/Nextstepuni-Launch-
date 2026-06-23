/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { type Reference } from '../data/references/types';

// ─── Citation UX for accredited modules ─────────────────────────────────────
//
// Two primitives, designed to be unobtrusive for students but complete for
// review:
//   <Cite n={1} />            — a small superscript marker on a sourced claim.
//   <SectionSources refs={…}/> — a quiet "The evidence" list at the foot of a
//                                section, numbered to match the markers.
//
// The full per-claim verification record lives in
// compliance/evidence/<module>.md (the dossier reviewed for accreditation).

/** Inline superscript citation marker. Deliberately faint — present if wanted,
 *  invisible to the flow if not. The number maps to the section's SectionSources. */
export const Cite: React.FC<{ n: number }> = ({ n }) => (
  <sup className="text-[10px] font-semibold text-zinc-400 dark:text-zinc-500 ml-px select-none">{n}</sup>
);

/** Foot-of-section reference list. Renders nothing if there are no references. */
export const SectionSources: React.FC<{ refs: Reference[] }> = ({ refs }) => {
  if (!refs || refs.length === 0) return null;
  return (
    <div className="mt-10 pt-5 border-t border-zinc-200/70 dark:border-zinc-700/50">
      <p className="text-[10px] font-bold uppercase tracking-[0.14em] text-zinc-400 dark:text-zinc-500 mb-3">
        The evidence
      </p>
      <ol className="space-y-1.5">
        {refs.map((r, i) => (
          <li key={r.id} className="flex gap-2 text-[11px] leading-relaxed text-zinc-500 dark:text-zinc-400">
            <span className="shrink-0 font-semibold text-zinc-400 dark:text-zinc-500">{i + 1}.</span>
            <span>
              {r.authors} ({r.year}). {r.title}. <span className="italic">{r.source}</span>.{' '}
              <a
                href={`https://doi.org/${r.doi}`}
                target="_blank"
                rel="noopener noreferrer"
                className="underline decoration-dotted underline-offset-2 hover:text-[#F26B1F] transition-colors"
              >
                doi:{r.doi}
              </a>
            </span>
          </li>
        ))}
      </ol>
    </div>
  );
};
