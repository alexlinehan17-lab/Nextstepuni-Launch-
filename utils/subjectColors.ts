/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Lightweight subject colour utilities extracted from studySessionData.ts.
 * Import this (not studySessionData) in eagerly-loaded components to avoid
 * pulling the 24KB STRATEGY_PROMPTS array into the index chunk.
 */

export const SUBJECT_COLORS: Record<string, { dot: string; bg: string; border: string; text: string }> = {
  'English':    { dot: 'bg-blue-500',    bg: 'bg-blue-50 dark:bg-blue-900/20',    border: 'border-blue-200 dark:border-blue-800/40',    text: 'text-blue-700 dark:text-blue-300' },
  'Irish':      { dot: 'bg-emerald-500', bg: 'bg-emerald-50 dark:bg-emerald-900/20', border: 'border-emerald-200 dark:border-emerald-800/40', text: 'text-emerald-700 dark:text-emerald-300' },
  'Mathematics':{ dot: 'bg-indigo-500',  bg: 'bg-indigo-50 dark:bg-indigo-900/20',  border: 'border-indigo-200 dark:border-indigo-800/40',  text: 'text-indigo-700 dark:text-indigo-300' },
  'French':     { dot: 'bg-rose-500',    bg: 'bg-rose-50 dark:bg-rose-900/20',    border: 'border-rose-200 dark:border-rose-800/40',    text: 'text-rose-700 dark:text-rose-300' },
  'German':     { dot: 'bg-amber-500',   bg: 'bg-amber-50 dark:bg-amber-900/20',   border: 'border-amber-200 dark:border-amber-800/40',   text: 'text-amber-700 dark:text-amber-300' },
  'Spanish':    { dot: 'bg-orange-500',  bg: 'bg-orange-50 dark:bg-orange-900/20',  border: 'border-orange-200 dark:border-orange-800/40',  text: 'text-orange-700 dark:text-orange-300' },
  'Italian':    { dot: 'bg-lime-500',    bg: 'bg-lime-50 dark:bg-lime-900/20',    border: 'border-lime-200 dark:border-lime-800/40',    text: 'text-lime-700 dark:text-lime-300' },
  'Japanese':   { dot: 'bg-pink-500',    bg: 'bg-pink-50 dark:bg-pink-900/20',    border: 'border-pink-200 dark:border-pink-800/40',    text: 'text-pink-700 dark:text-pink-300' },
  'Physics':    { dot: 'bg-cyan-500',    bg: 'bg-cyan-50 dark:bg-cyan-900/20',    border: 'border-cyan-200 dark:border-cyan-800/40',    text: 'text-cyan-700 dark:text-cyan-300' },
  'Chemistry':  { dot: 'bg-teal-500',    bg: 'bg-teal-50 dark:bg-teal-900/20',    border: 'border-teal-200 dark:border-teal-800/40',    text: 'text-teal-700 dark:text-teal-300' },
  'Biology':    { dot: 'bg-green-500',   bg: 'bg-green-50 dark:bg-green-900/20',   border: 'border-green-200 dark:border-green-800/40',   text: 'text-green-700 dark:text-green-300' },
  'Applied Mathematics': { dot: 'bg-violet-500', bg: 'bg-violet-50 dark:bg-violet-900/20', border: 'border-violet-200 dark:border-violet-800/40', text: 'text-violet-700 dark:text-violet-300' },
  'Agricultural Science': { dot: 'bg-lime-600', bg: 'bg-lime-50 dark:bg-lime-900/20', border: 'border-lime-200 dark:border-lime-800/40', text: 'text-lime-700 dark:text-lime-300' },
  'Computer Science':    { dot: 'bg-sky-500', bg: 'bg-sky-50 dark:bg-sky-900/20', border: 'border-sky-200 dark:border-sky-800/40', text: 'text-sky-700 dark:text-sky-300' },
  'Accounting':          { dot: 'bg-emerald-600', bg: 'bg-emerald-50 dark:bg-emerald-900/20', border: 'border-emerald-200 dark:border-emerald-800/40', text: 'text-emerald-700 dark:text-emerald-300' },
  'Business':            { dot: 'bg-blue-600', bg: 'bg-blue-50 dark:bg-blue-900/20', border: 'border-blue-200 dark:border-blue-800/40', text: 'text-blue-700 dark:text-blue-300' },
  'Economics':           { dot: 'bg-yellow-500', bg: 'bg-yellow-50 dark:bg-yellow-900/20', border: 'border-yellow-200 dark:border-yellow-800/40', text: 'text-yellow-700 dark:text-yellow-300' },
  'History':             { dot: 'bg-amber-600', bg: 'bg-amber-50 dark:bg-amber-900/20', border: 'border-amber-200 dark:border-amber-800/40', text: 'text-amber-700 dark:text-amber-300' },
  'Geography':           { dot: 'bg-teal-600', bg: 'bg-teal-50 dark:bg-teal-900/20', border: 'border-teal-200 dark:border-teal-800/40', text: 'text-teal-700 dark:text-teal-300' },
  'Politics & Society':  { dot: 'bg-purple-500', bg: 'bg-purple-50 dark:bg-purple-900/20', border: 'border-purple-200 dark:border-purple-800/40', text: 'text-purple-700 dark:text-purple-300' },
  'Religious Education': { dot: 'bg-fuchsia-500', bg: 'bg-fuchsia-50 dark:bg-fuchsia-900/20', border: 'border-fuchsia-200 dark:border-fuchsia-800/40', text: 'text-fuchsia-700 dark:text-fuchsia-300' },
  'Home Economics':      { dot: 'bg-orange-600', bg: 'bg-orange-50 dark:bg-orange-900/20', border: 'border-orange-200 dark:border-orange-800/40', text: 'text-orange-700 dark:text-orange-300' },
  'Music':               { dot: 'bg-pink-600', bg: 'bg-pink-50 dark:bg-pink-900/20', border: 'border-pink-200 dark:border-pink-800/40', text: 'text-pink-700 dark:text-pink-300' },
  'Art':                 { dot: 'bg-red-500', bg: 'bg-red-50 dark:bg-red-900/20', border: 'border-red-200 dark:border-red-800/40', text: 'text-red-700 dark:text-red-300' },
  'Construction Studies':{ dot: 'bg-stone-500', bg: 'bg-stone-50 dark:bg-stone-900/20', border: 'border-stone-200 dark:border-stone-800/40', text: 'text-stone-700 dark:text-stone-300' },
  'Engineering':         { dot: 'bg-zinc-500', bg: 'bg-zinc-50 dark:bg-zinc-900/20', border: 'border-zinc-200 dark:border-zinc-800/40', text: 'text-zinc-700 dark:text-zinc-300' },
  'Technology':          { dot: 'bg-slate-500', bg: 'bg-slate-50 dark:bg-slate-900/20', border: 'border-slate-200 dark:border-slate-800/40', text: 'text-slate-700 dark:text-slate-300' },
  'Design & Communication Graphics': { dot: 'bg-indigo-600', bg: 'bg-indigo-50 dark:bg-indigo-900/20', border: 'border-indigo-200 dark:border-indigo-800/40', text: 'text-indigo-700 dark:text-indigo-300' },
  'Physical Education':  { dot: 'bg-red-600', bg: 'bg-red-50 dark:bg-red-900/20', border: 'border-red-200 dark:border-red-800/40', text: 'text-red-700 dark:text-red-300' },
  // ─── Junior Cycle-only subject colour entries (Phase 1) ────────────────
  // Reuses the existing group-colour ranges; picks hues that aren't already
  // used by an LC subject so each card reads distinctly in mixed grids
  // (e.g., a school's GC dashboard listing both cohorts).
  'Science':                     { dot: 'bg-green-600',   bg: 'bg-green-50 dark:bg-green-900/20',     border: 'border-green-200 dark:border-green-800/40',     text: 'text-green-700 dark:text-green-300' },
  'CSPE':                        { dot: 'bg-purple-600',  bg: 'bg-purple-50 dark:bg-purple-900/20',   border: 'border-purple-200 dark:border-purple-800/40',   text: 'text-purple-700 dark:text-purple-300' },
  'SPHE':                        { dot: 'bg-fuchsia-400', bg: 'bg-fuchsia-50 dark:bg-fuchsia-900/20', border: 'border-fuchsia-200 dark:border-fuchsia-800/40', text: 'text-fuchsia-700 dark:text-fuchsia-300' },
  'Business Studies':            { dot: 'bg-amber-700',   bg: 'bg-amber-50 dark:bg-amber-900/20',     border: 'border-amber-200 dark:border-amber-800/40',     text: 'text-amber-700 dark:text-amber-300' },
  'Materials Technology (Wood)': { dot: 'bg-stone-600',   bg: 'bg-stone-50 dark:bg-stone-900/20',     border: 'border-stone-200 dark:border-stone-800/40',     text: 'text-stone-700 dark:text-stone-300' },
  'Metalwork':                   { dot: 'bg-zinc-600',    bg: 'bg-zinc-50 dark:bg-zinc-900/20',       border: 'border-zinc-200 dark:border-zinc-800/40',       text: 'text-zinc-700 dark:text-zinc-300' },
  'Graphics':                    { dot: 'bg-indigo-700',  bg: 'bg-indigo-50 dark:bg-indigo-900/20',   border: 'border-indigo-200 dark:border-indigo-800/40',   text: 'text-indigo-700 dark:text-indigo-300' },
  'Classical Studies':           { dot: 'bg-violet-600',  bg: 'bg-violet-50 dark:bg-violet-900/20',   border: 'border-violet-200 dark:border-violet-800/40',   text: 'text-violet-700 dark:text-violet-300' },
  'Latin':                       { dot: 'bg-slate-600',   bg: 'bg-slate-50 dark:bg-slate-900/20',     border: 'border-slate-200 dark:border-slate-800/40',     text: 'text-slate-700 dark:text-slate-300' },
};

const DEFAULT_COLOR = { dot: 'bg-zinc-500', bg: 'bg-zinc-50 dark:bg-zinc-800/40', border: 'border-zinc-200 dark:border-zinc-700/40', text: 'text-zinc-700 dark:text-zinc-300' };

export function getSubjectColor(name: string) {
  return SUBJECT_COLORS[name] || DEFAULT_COLOR;
}

/**
 * The subject palette: ten fills, all deep enough to carry WHITE text at
 * WCAG AA (every one clears 5:1), spaced around the wheel so any six or
 * seven a student takes read as different colours, and kept warm and inky
 * so they sit with the brand's paper, ink and orange. Rust is the brand's
 * own orange-text tone.
 */
export const SUBJECT_PALETTE = {
  cobalt: '#2F52A8',
  forest: '#2C7A4B',
  violet: '#5B47C2',
  teal: '#1E7A76',
  rust: '#B84A0C',
  brick: '#A8332E',
  ochre: '#8A6508',
  olive: '#5C6E1C',
  raspberry: '#A82A5C',
  plum: '#8A3B7A',
} as const;

export type SubjectPaletteName = keyof typeof SUBJECT_PALETTE;

/** The one text colour that goes on every palette fill. */
export const SUBJECT_FILL_INK = '#FFFFFF';

/**
 * Which of the ten each subject wears. The three everyone takes (English,
 * Irish, Mathematics) own cobalt, forest and violet outright; the seven
 * remaining fills are shared out so the usual combinations — the sciences
 * together, the business trio, a language with anything — stay distinct.
 */
const SUBJECT_FILL_NAME: Record<string, SubjectPaletteName> = {
  'English': 'cobalt',
  'Irish': 'forest',
  'Mathematics': 'violet',
  'Applied Mathematics': 'plum',
  'Applied Maths': 'plum',
  'Biology': 'teal',
  'Chemistry': 'rust',
  'Physics': 'brick',
  'Agricultural Science': 'olive',
  'Ag Science': 'olive',
  'French': 'raspberry',
  'German': 'ochre',
  'Spanish': 'plum',
  'Italian': 'olive',
  'Japanese': 'brick',
  'Economics': 'ochre',
  'Business': 'plum',
  'Accounting': 'brick',
  'Geography': 'olive',
  'History': 'raspberry',
  'Politics & Society': 'teal',
  'Religious Education': 'plum',
  'Classical Studies': 'rust',
  'Home Economics': 'rust',
  'Art': 'raspberry',
  'Music': 'ochre',
  'Physical Education': 'brick',
  'Computer Science': 'teal',
  'Construction Studies': 'olive',
  'Engineering': 'brick',
  'Technology': 'ochre',
  'Design & Communication Graphics': 'plum',
  'DCG': 'plum',
  // Junior Cycle
  'Science': 'teal',
  'CSPE': 'plum',
  'SPHE': 'raspberry',
  'Business Studies': 'ochre',
  'Materials Technology (Wood)': 'olive',
  'Metalwork': 'brick',
  'Graphics': 'rust',
  'Latin': 'plum',
};

/** A subject's fill from the ten-colour palette; unknown subjects get plum. */
export function getSubjectFill(name: string): string {
  return SUBJECT_PALETTE[SUBJECT_FILL_NAME[name] ?? 'plum'];
}

/** Kept for existing callers: the same ten-colour palette, by subject. */
export const SUBJECT_HEX_COLORS: Record<string, string> = Object.fromEntries(
  Object.entries(SUBJECT_FILL_NAME).map(([subject, fill]) => [subject, SUBJECT_PALETTE[fill]]),
);

export function getSubjectHex(name: string): string {
  return getSubjectFill(name);
}

const DISTINCT_PALETTE = Object.values(SUBJECT_PALETTE);

export function getDistinctSubjectHex(name: string, index: number): string {
  return SUBJECT_HEX_COLORS[name] || DISTINCT_PALETTE[index % DISTINCT_PALETTE.length];
}
