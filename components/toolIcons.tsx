/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Tool icons — one inline SVG per tool, used inside <ToolHeader>.
 * Each component fills its container; the parent tile handles sizing.
 *
 * Where an icon needs theme-coloured "negative space" inside a white
 * shape, the component takes a `themeColor` prop. Defaults match the
 * palette so they remain valid if rendered standalone.
 *
 * White-on-white visibility rule (used in SyllabusXRayIcon): when a
 * white-stroked element overlaps a white shape, draw it three times —
 * outer black 0.7px → white stroke at the original radius → inner black
 * 0.7px — so the white element reads against either ground.
 */

import React from 'react';

interface IconProps {
  /** Used by icons that have theme-coloured details inside a white shape. */
  themeColor?: string;
}

// ── 1. Training Hub — bar-chart with peak ───────────────────────────────

export const TrainingHubIcon: React.FC<IconProps> = () => (
  <svg viewBox="0 0 100 100" width="100%" height="100%">
    <path
      d="M 10 65 L 24 65 L 28 52 L 33 65 L 44 65 L 49 38 L 55 65 L 64 65 L 69 22 L 75 65 L 90 65"
      fill="none"
      stroke="white"
      strokeWidth="3.2"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
    <circle cx="69" cy="22" r="4" fill="white" />
  </svg>
);

// ── 2. War Room — target with arrow ─────────────────────────────────────

export const WarRoomIcon: React.FC<IconProps> = () => (
  <svg viewBox="0 0 100 100" width="100%" height="100%">
    <circle cx="55" cy="52" r="32" fill="none" stroke="white" strokeWidth="3" />
    <circle cx="56" cy="51" r="21" fill="none" stroke="white" strokeWidth="3" />
    <circle cx="55" cy="52" r="9" fill="white" />
    <path d="M 11 22 Q 30 35 55 52" fill="none" stroke="white" strokeWidth="3" strokeLinecap="round" />
    <path d="M 6 19 L 11 22 L 8 28" fill="none" stroke="white" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
    <path d="M 11 22 L 4 15 M 11 22 L 3 24" stroke="white" strokeWidth="2.5" strokeLinecap="round" />
  </svg>
);

// ── 3. Academic Journey Simulator — branching node ──────────────────────

export const AcademicJourneyIcon: React.FC<IconProps> = () => (
  <svg viewBox="0 0 100 100" width="100%" height="100%">
    <circle cx="50" cy="85" r="4.5" fill="white" />
    <path d="M 50 82 L 50 56" stroke="white" strokeWidth="3" strokeLinecap="round" />
    <path d="M 50 56 Q 35 50 22 30" fill="none" stroke="white" strokeWidth="3" strokeLinecap="round" />
    <path d="M 50 56 L 50 24" stroke="white" strokeWidth="3" strokeLinecap="round" />
    <path d="M 50 56 Q 65 50 78 30" fill="none" stroke="white" strokeWidth="3" strokeLinecap="round" />
    <circle cx="22" cy="28" r="5" fill="none" stroke="white" strokeWidth="3" />
    <circle cx="50" cy="22" r="5" fill="white" />
    <circle cx="78" cy="28" r="5" fill="none" stroke="white" strokeWidth="3" />
  </svg>
);

// ── 4. CAO Points Simulator — three-row slider grid ─────────────────────

export const CAOPointsIcon: React.FC<IconProps> = () => (
  <svg viewBox="0 0 100 100" width="100%" height="100%">
    <line x1="18" y1="32" x2="82" y2="32" stroke="white" strokeWidth="2.5" strokeLinecap="round" opacity="0.4" />
    <line x1="18" y1="50" x2="82" y2="50" stroke="white" strokeWidth="2.5" strokeLinecap="round" opacity="0.4" />
    <line x1="18" y1="68" x2="82" y2="68" stroke="white" strokeWidth="2.5" strokeLinecap="round" opacity="0.4" />
    <circle cx="68" cy="32" r="7" fill="white" />
    <circle cx="38" cy="50" r="7" fill="white" />
    <circle cx="74" cy="68" r="7" fill="white" />
  </svg>
);

// ── 5. Future Finder — graph + sun (compass) ────────────────────────────

export const FutureFinderIcon: React.FC<IconProps> = () => (
  <svg viewBox="0 0 100 100" width="100%" height="100%">
    <line x1="20" y1="62" x2="38" y2="42" stroke="white" strokeWidth="2" strokeLinecap="round" opacity="0.55" />
    <line x1="38" y1="42" x2="56" y2="52" stroke="white" strokeWidth="2" strokeLinecap="round" opacity="0.55" />
    <line x1="38" y1="42" x2="62" y2="68" stroke="white" strokeWidth="2" strokeLinecap="round" opacity="0.55" />
    <line x1="56" y1="52" x2="74" y2="26" stroke="white" strokeWidth="2" strokeLinecap="round" opacity="0.55" />
    <circle cx="20" cy="62" r="3.5" fill="white" />
    <circle cx="38" cy="42" r="3.5" fill="white" />
    <circle cx="56" cy="52" r="3.5" fill="white" />
    <circle cx="62" cy="68" r="3.5" fill="white" />
    <circle cx="74" cy="26" r="7" fill="white" />
    <line x1="74" y1="12" x2="74" y2="16" stroke="white" strokeWidth="2" strokeLinecap="round" />
    <line x1="60" y1="26" x2="64" y2="26" stroke="white" strokeWidth="2" strokeLinecap="round" />
    <line x1="84" y1="26" x2="88" y2="26" stroke="white" strokeWidth="2" strokeLinecap="round" />
    <line x1="74" y1="36" x2="74" y2="40" stroke="white" strokeWidth="2" strokeLinecap="round" />
  </svg>
);

// ── 6. Syllabus X-Ray — document under magnifier ────────────────────────
// Magnifier uses the triple-circle white-on-white visibility technique.

export const SyllabusXRayIcon: React.FC<IconProps> = ({ themeColor = '#2C4B6E' }) => (
  <svg viewBox="0 0 100 100" width="100%" height="100%">
    <rect x="18" y="20" width="46" height="58" rx="3" fill="white" />
    <line x1="24" y1="32" x2="54" y2="32" stroke={themeColor} strokeWidth="2" strokeLinecap="round" />
    <line x1="24" y1="40" x2="48" y2="40" stroke={themeColor} strokeWidth="2" strokeLinecap="round" />
    <line x1="24" y1="48" x2="56" y2="48" stroke={themeColor} strokeWidth="2" strokeLinecap="round" />
    <line x1="24" y1="56" x2="46" y2="56" stroke={themeColor} strokeWidth="2" strokeLinecap="round" />
    <circle cx="48" cy="32" r="5" fill="none" stroke={themeColor} strokeWidth="2.5" />
    <circle cx="42" cy="48" r="5" fill="none" stroke={themeColor} strokeWidth="2.5" />
    <circle cx="72" cy="64" r="16" fill="none" stroke="#1a1a1a" strokeWidth="0.7" />
    <circle cx="72" cy="64" r="14" fill="none" stroke="white" strokeWidth="2.5" />
    <circle cx="72" cy="64" r="12" fill="none" stroke="#1a1a1a" strokeWidth="0.7" />
    <line x1="82" y1="74" x2="92" y2="84" stroke="white" strokeWidth="3" strokeLinecap="round" />
  </svg>
);

// ── 7. Spaced Repetition Timetable — three connected forgetting curves ──

export const SpacedRepetitionIcon: React.FC<IconProps> = () => (
  <svg viewBox="0 0 100 100" width="100%" height="100%">
    <path d="M 14 76 Q 16 60 22 58 L 26 60 Q 28 64 32 70" fill="none" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
    <path d="M 32 70 Q 36 42 46 40 L 50 42 Q 54 46 56 54" fill="none" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
    <path d="M 56 54 Q 64 26 78 22 L 86 22" fill="none" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
    <circle cx="22" cy="58" r="3.8" fill="white" />
    <circle cx="46" cy="40" r="3.8" fill="white" />
    <circle cx="78" cy="22" r="3.8" fill="white" />
    <line x1="14" y1="80" x2="86" y2="80" stroke="white" strokeWidth="1" strokeLinecap="round" opacity="0.35" />
  </svg>
);

// ── 8. Comeback Engine — rocket with theme-coloured porthole ────────────

export const ComebackEngineIcon: React.FC<IconProps> = ({ themeColor = '#E08938' }) => (
  <svg viewBox="0 0 100 100" width="100%" height="100%">
    <path
      d="M 50 14 L 60 38 L 60 60 Q 60 64 56 64 L 44 64 Q 40 64 40 60 L 40 38 Z"
      fill="white"
      stroke="white"
      strokeWidth="1.5"
      strokeLinejoin="round"
    />
    <circle cx="50" cy="40" r="4" fill={themeColor} />
    <path d="M 40 56 L 28 72 L 40 66 Z" fill="white" stroke="white" strokeWidth="1" strokeLinejoin="round" />
    <path d="M 60 56 L 72 72 L 60 66 Z" fill="white" stroke="white" strokeWidth="1" strokeLinejoin="round" />
    <path d="M 44 64 L 42 76" stroke="white" strokeWidth="2.5" strokeLinecap="round" />
    <path d="M 50 64 L 50 80" stroke="white" strokeWidth="2.5" strokeLinecap="round" />
    <path d="M 56 64 L 58 76" stroke="white" strokeWidth="2.5" strokeLinecap="round" />
  </svg>
);

// ── 9. Points Passport — open book with chart ───────────────────────────

export const PointsPassportIcon: React.FC<IconProps> = ({ themeColor = '#B8A079' }) => (
  <svg viewBox="0 0 100 100" width="100%" height="100%">
    <path
      d="M 12 28 L 50 22 L 88 28 L 88 76 L 50 70 L 12 76 Z"
      fill="white"
      stroke="#1a1a1a"
      strokeWidth="1"
      strokeLinejoin="round"
    />
    <line x1="50" y1="22" x2="50" y2="70" stroke="#1a1a1a" strokeWidth="1" opacity="0.45" />
    <line x1="20" y1="40" x2="42" y2="40" stroke={themeColor} strokeWidth="2" strokeLinecap="round" />
    <line x1="20" y1="48" x2="38" y2="48" stroke={themeColor} strokeWidth="2" strokeLinecap="round" />
    <line x1="20" y1="56" x2="42" y2="56" stroke={themeColor} strokeWidth="2" strokeLinecap="round" />
    <path d="M 56 60 L 64 54 L 70 56 L 76 42 L 82 48" fill="none" stroke={themeColor} strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" />
    <circle cx="76" cy="42" r="3" fill={themeColor} />
  </svg>
);
