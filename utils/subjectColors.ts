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
};

const DEFAULT_COLOR = { dot: 'bg-zinc-500', bg: 'bg-zinc-50 dark:bg-zinc-800/40', border: 'border-zinc-200 dark:border-zinc-700/40', text: 'text-zinc-700 dark:text-zinc-300' };

export function getSubjectColor(name: string) {
  return SUBJECT_COLORS[name] || DEFAULT_COLOR;
}

export const SUBJECT_HEX_COLORS: Record<string, string> = {
  'English': '#0984E3',
  'Irish': '#00B894',
  'Mathematics': '#2D3436',
  'French': '#E84393',
  'German': '#FDCB6E',
  'Spanish': '#E17055',
  'Italian': '#00CEC9',
  'Japanese': '#A29BFE',
  'Physics': '#74B9FF',
  'Chemistry': '#55EFC4',
  'Biology': '#00B894',
  'Applied Mathematics': '#6C5CE7',
  'Applied Maths': '#6C5CE7',
  'Agricultural Science': '#BADC58',
  'Computer Science': '#74B9FF',
  'Accounting': '#FDCB6E',
  'Business': '#0984E3',
  'Economics': '#E67E22',
  'History': '#D63031',
  'Geography': '#00B894',
  'Politics & Society': '#E84393',
  'Religious Education': '#A29BFE',
  'Home Economics': '#E17055',
  'Music': '#FD79A8',
  'Art': '#FF7675',
  'Construction Studies': '#636E72',
  'Engineering': '#636E72',
  'Technology': '#636E72',
  'Design & Communication Graphics': '#6C5CE7',
  'Physical Education': '#D63031',
};

export function getSubjectHex(name: string): string {
  return SUBJECT_HEX_COLORS[name] || '#a855f7';
}

const DISTINCT_PALETTE = [
  '#0984E3', '#E84393', '#E67E22', '#6C5CE7', '#00B894',
  '#D63031', '#FDCB6E', '#A29BFE', '#00CEC9', '#2D3436',
];

export function getDistinctSubjectHex(name: string, index: number): string {
  return SUBJECT_HEX_COLORS[name] || DISTINCT_PALETTE[index % DISTINCT_PALETTE.length];
}
