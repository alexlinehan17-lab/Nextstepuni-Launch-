/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * SubjectTilePicker — the shared subject-picker surface used by Catch-Up Lane,
 * Command-Word Reflex (and next, Paper Trail).
 *
 * Purely presentational: the caller filters subjects to the student's cycle /
 * level, sorts them, and renders display-ready labels + sublabels (counts,
 * progress). This component owns only the My Subjects / All Subjects segmented
 * toggle and white subject controls. Scope state remains in the caller.
 * Shared controls keep readable names/counts and an explicit scope selection.
 */

import React from 'react';
import { ArrowUpRight } from 'lucide-react';

export interface SubjectTileItem {
  /** Stable subject id, passed back through onPick. */
  id: string;
  /** Display-ready label (cycle parenthetical already stripped by the caller). */
  label: string;
  /** Optional second line — counts / progress, already formatted by the caller. */
  sublabel?: string;
}

export interface SubjectTilePickerProps {
  /** Already filtered (cycle/level) and sorted by the caller. */
  subjects: SubjectTileItem[];
  /**
   * Subject ids (⊆ subjects) that are in the student's own profile. One or
   * more enables the My Subjects / All Subjects toggle; empty/absent hides it
   * and shows every tile.
   */
  mineIds?: string[];
  /** Picker scope — state is lifted into the calling tool. */
  scope: 'mine' | 'all';
  onScopeChange: (scope: 'mine' | 'all') => void;
  /** Tile tap → open that subject in the tool. */
  onPick: (id: string) => void;
  /** Optional small-caps heading above the toggle; omit to render your own. */
  headingLabel?: string;
}

const SubjectTilePicker: React.FC<SubjectTilePickerProps> = ({
  subjects, mineIds, scope, onScopeChange, onPick, headingLabel,
}) => {
  const mineSet = new Set(mineIds ?? []);
  const hasMine = mineSet.size > 0;
  const list = hasMine && scope === 'mine' ? subjects.filter(s => mineSet.has(s.id)) : subjects;
  return (
    <>
      {headingLabel && (
        <h2 className="text-xs font-bold uppercase tracking-widest mb-3 text-zinc-600 dark:text-zinc-400">
          {headingLabel}
        </h2>
      )}
      {hasMine && (
        <div className="grid grid-cols-2 border-b border-zinc-300 dark:border-zinc-700 mb-5">
          {(['mine', 'all'] as const).map(sc => (
            <button
              key={sc}
              onClick={() => onScopeChange(sc)}
              aria-pressed={scope === sc}
              className={`min-h-12 border-b-[3px] px-3 py-3 text-sm transition-colors ${scope === sc ? 'border-[#F26B1F] text-zinc-900 dark:text-white font-bold' : 'border-transparent text-zinc-600 dark:text-zinc-400'}`}
            >
              {sc === 'mine' ? 'My Subjects' : 'All Subjects'}
            </button>
          ))}
        </div>
      )}
      <div className="grid grid-cols-1 min-[360px]:grid-cols-2 gap-3">
        {list.map(s => (
          <button
            key={s.id}
            onClick={() => onPick(s.id)}
            aria-label={`${s.label}${s.sublabel ? `, ${s.sublabel}` : ''}`}
            className="group flex min-h-[112px] min-w-0 flex-col items-start justify-between gap-4 rounded-xl border border-zinc-300 bg-white p-4 text-left text-zinc-900 transition-colors hover:border-[#B54D14] active:border-[#B54D14] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#B54D14] dark:border-zinc-600 dark:bg-zinc-900 dark:text-white"
          >
            <span className="text-base font-bold leading-snug [overflow-wrap:anywhere]">{s.label}</span>
            <span className="flex w-full items-end justify-between gap-2">{s.sublabel && <span className="text-sm leading-snug text-zinc-600 dark:text-zinc-300">{s.sublabel}</span>}<ArrowUpRight size={18} aria-hidden="true" className="ml-auto shrink-0 text-[#B54D14] dark:text-orange-400" /></span>
          </button>
        ))}
      </div>
    </>
  );
};

export default SubjectTilePicker;
