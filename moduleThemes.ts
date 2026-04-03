/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { ModuleTheme } from './types';

// ─── Theme colour definitions ───────────────────────────────────────────────
// Each colour defines a Tailwind colour name and its hex for arbitrary values.

interface ThemeColor {
  name: string;       // Tailwind colour name (e.g. 'amber', 'blue')
  hex500: string;     // Hex for the 500 shade (used in shadows and activityRing)
}

const THEME_COLORS: Record<string, ThemeColor> = {
  amber:   { name: 'amber',   hex500: '#f59e0b' },
  blue:    { name: 'blue',    hex500: '#3b82f6' },
  rose:    { name: 'rose',    hex500: '#e11d48' },
  emerald: { name: 'emerald', hex500: '#10b981' },
  orange:  { name: 'orange',  hex500: '#f97316' },
  teal:    { name: 'teal',    hex500: '#14b8a6' },
  cyan:    { name: 'cyan',    hex500: '#06b6d4' },
  slate:   { name: 'slate',   hex500: '#64748b' },
  sky:     { name: 'sky',     hex500: '#0ea5e9' },
  red:     { name: 'red',     hex500: '#ef4444' },
  purple:  { name: 'purple',  hex500: '#a855f7' },
  fuchsia: { name: 'fuchsia', hex500: '#d946ef' },
  indigo:  { name: 'indigo',  hex500: '#4f46e5' },
  violet:  { name: 'violet',  hex500: '#8b5cf6' },
  pink:    { name: 'pink',    hex500: '#ec4899' },
  lime:    { name: 'lime',    hex500: '#65a30d' },
  yellow:  { name: 'yellow',  hex500: '#ca8a04' },
  gray:    { name: 'gray',    hex500: '#4b5563' },
};

// ─── Factory function ───────────────────────────────────────────────────────
// Now that Tailwind runs at build time, we can construct class strings dynamically.

function createTheme(c: ThemeColor): ModuleTheme {
  const n = c.name;
  // Convert hex to RGB for shadow
  const hex = c.hex500;
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);

  return {
    // Highlight
    highlightBg: `bg-${n}-100/40`,
    highlightText: `text-${n}-900`,
    highlightDecor: `decoration-${n}-400/40`,
    highlightHover: `hover:bg-${n}-200/60`,
    tooltipAccent: `text-${n}-400`,

    // ReadingSection
    readingIconColor: `text-${n}-400`,
    readingEyebrowBg: `bg-${n}-50`,
    readingEyebrowText: `text-${n}-600`,

    // MicroCommitment
    microBg: `bg-${n}-50/50`,
    microBorder: `border-${n}-200`,
    microIconBg: `bg-${n}-500`,
    microIconShadow: `shadow-${n}-500/20`,
    microTitle: `text-${n}-800`,

    // Sidebar
    sidebarModuleText: `text-${n}-500`,
    sidebarProgressBg: `bg-${n}-500`,
    sidebarProgressShadow: `shadow-[0_0_10px_rgba(${r},${g},${b},0.5)]`,
    sidebarActiveBg: `bg-${n}-50`,
    sidebarCompletedBg: `bg-${n}-600`,
    sidebarCompletedBorder: `border-${n}-600`,
    sidebarActiveBorder: `border-${n}-500`,
    sidebarActiveText: `text-${n}-600`,
    sidebarActiveEyebrow: `text-${n}-500`,

    // Footer
    footerHoverBg: `hover:bg-${n}-600`,

    // ActivityRing
    activityRingColor: hex,
  };
}

// ─── Export all themes ──────────────────────────────────────────────────────

export const amberTheme   = createTheme(THEME_COLORS.amber);
export const blueTheme    = createTheme(THEME_COLORS.blue);
export const roseTheme    = createTheme(THEME_COLORS.rose);
export const emeraldTheme = createTheme(THEME_COLORS.emerald);
export const orangeTheme  = createTheme(THEME_COLORS.orange);
export const tealTheme    = createTheme(THEME_COLORS.teal);
export const cyanTheme    = createTheme(THEME_COLORS.cyan);
export const slateTheme   = createTheme(THEME_COLORS.slate);
export const skyTheme     = createTheme(THEME_COLORS.sky);
export const redTheme     = createTheme(THEME_COLORS.red);
export const purpleTheme  = createTheme(THEME_COLORS.purple);
export const fuchsiaTheme = createTheme(THEME_COLORS.fuchsia);
export const indigoTheme  = createTheme(THEME_COLORS.indigo);
export const violetTheme  = createTheme(THEME_COLORS.violet);
export const pinkTheme    = createTheme(THEME_COLORS.pink);
export const limeTheme    = createTheme(THEME_COLORS.lime);
export const yellowTheme  = createTheme(THEME_COLORS.yellow);
export const grayTheme    = createTheme(THEME_COLORS.gray);
