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
 * toggle and the cream year-selection-style tile grid. Scope state lives in
 * the calling tool (controlled via `scope` + `onScopeChange`), so each tool
 * keeps its own picker scope independently.
 *
 * The toggle and tile markup is the exact year-selection card vocabulary
 * (cream #FDF8F0, 2px ink border, hard 4px offset shadow, orange #F26B1F
 * hover/active) — copied verbatim; don't restyle here without restyling the
 * year picker too.
 */

import React from 'react';

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
        <h2 className="text-[13px] font-bold uppercase tracking-[0.14em] mb-3" style={{ color: '#9e9186' }}>
          {headingLabel}
        </h2>
      )}
      {hasMine && (
        <div className="flex items-center gap-1 p-1 rounded-xl bg-zinc-100 dark:bg-zinc-800/50 w-fit mb-4">
          {(['mine', 'all'] as const).map(sc => (
            <button
              key={sc}
              onClick={() => onScopeChange(sc)}
              className={`px-4 py-1.5 rounded-lg text-[13px] transition-all ${scope === sc ? 'bg-white dark:bg-zinc-800 text-zinc-900 dark:text-white font-semibold shadow-sm' : 'text-zinc-500 dark:text-zinc-400'}`}
            >
              {sc === 'mine' ? 'My Subjects' : 'All Subjects'}
            </button>
          ))}
        </div>
      )}
      <div className="grid grid-cols-2 gap-3">
        {list.map(s => (
          <button
            key={s.id}
            onClick={() => onPick(s.id)}
            aria-label={`${s.label}${s.sublabel ? `, ${s.sublabel}` : ''}`}
            className="group flex flex-col items-center justify-center text-center px-3 py-5 min-h-[92px] rounded-2xl border-2 border-[#1A1A1A] font-sans transition-all duration-150 hover:-translate-y-0.5 active:translate-x-1 active:translate-y-1 shadow-[4px_4px_0_0_#1A1A1A] hover:shadow-[6px_6px_0_0_#1A1A1A] active:shadow-[0px_0px_0_0_#1A1A1A] bg-[#FDF8F0] text-[#1A1A1A] hover:bg-[#F26B1F] hover:text-[#FDF8F0] active:bg-[#F26B1F] active:text-[#FDF8F0]"
          >
            <span className="text-[17px] font-bold leading-tight">{s.label}</span>
            {s.sublabel && <span className="text-[11px] font-medium mt-1 opacity-80">{s.sublabel}</span>}
          </button>
        ))}
      </div>
    </>
  );
};

export default SubjectTilePicker;
