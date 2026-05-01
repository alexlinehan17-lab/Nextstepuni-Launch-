/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Section icons — one inline SVG per home-dashboard section.
 *
 * Each icon contains two layers:
 *   1. A soft "paint blob" (Bézier curves) at 0.75 opacity in the
 *      section's signature colour. The blob fills ~80% of the viewBox
 *      so the cream behind shows at the corners — gives the watercolour
 *      quality.
 *   2. A black-ink illustration (real objects: books, lightbulb,
 *      mountain, compass) drawn with stroke="#1a1a1a" at varied weights.
 *
 * Each blob has a slightly different Bézier path so the four don't read
 * as the same shape recoloured.
 */

import React from 'react';

// ── Modules — sage blob, books on a shelf + book pulled forward ─────────

export const ModulesIcon: React.FC = () => (
  <svg viewBox="0 0 100 100" width="100%" height="100%">
    <path
      d="M 14 30 Q 8 50 16 70 Q 28 86 50 84 Q 76 82 82 64 Q 88 42 76 26 Q 60 14 38 18 Q 20 22 14 30 Z"
      fill="#A8C9A0"
      opacity="0.75"
    />
    <g transform="translate(8, 12)">
      <rect x="8" y="32" width="11" height="46" fill="white" stroke="#1a1a1a" strokeWidth="0.8" />
      <rect x="20" y="36" width="9" height="42" fill="#FDF8F0" stroke="#1a1a1a" strokeWidth="0.8" />
      <rect x="30" y="28" width="13" height="50" fill="white" stroke="#1a1a1a" strokeWidth="0.8" />
      <line x1="11" y1="42" x2="16" y2="42" stroke="#2A7D6F" strokeWidth="1.5" />
      <line x1="33" y1="38" x2="40" y2="38" stroke="#2A7D6F" strokeWidth="1.5" />
      <line x1="33" y1="44" x2="38" y2="44" stroke="#2A7D6F" strokeWidth="1" />
      <path d="M 50 50 L 78 46 L 78 80 L 50 84 Z" fill="white" stroke="#1a1a1a" strokeWidth="1" />
      <path d="M 50 50 L 50 84 L 47 82 L 47 50 Z" fill="#FDF8F0" stroke="#1a1a1a" strokeWidth="1" />
      <line x1="56" y1="58" x2="72" y2="56" stroke="#2A7D6F" strokeWidth="1.5" />
      <line x1="56" y1="64" x2="68" y2="62" stroke="#2A7D6F" strokeWidth="1.2" />
    </g>
  </svg>
);

// ── Innovation Zone — dusty pink blob, lightbulb with rays ──────────────

export const InnovationZoneIcon: React.FC = () => (
  <svg viewBox="0 0 100 100" width="100%" height="100%">
    <path
      d="M 12 28 Q 8 48 18 66 Q 30 84 52 82 Q 78 80 84 60 Q 88 38 74 22 Q 56 10 36 16 Q 18 22 12 28 Z"
      fill="#D9A9C2"
      opacity="0.75"
    />
    <g>
      <path
        d="M 50 18 Q 32 18 30 36 Q 28 48 38 56 L 38 64 Q 38 66 40 66 L 60 66 Q 62 66 62 64 L 62 56 Q 72 48 70 36 Q 68 18 50 18 Z"
        fill="white"
        stroke="#1a1a1a"
        strokeWidth="1.5"
        strokeLinejoin="round"
      />
      <path
        d="M 42 36 L 46 44 L 50 38 L 54 44 L 58 36"
        fill="none"
        stroke="#1a1a1a"
        strokeWidth="1.3"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <line x1="40" y1="70" x2="60" y2="70" stroke="#1a1a1a" strokeWidth="1.5" strokeLinecap="round" />
      <line x1="42" y1="74" x2="58" y2="74" stroke="#1a1a1a" strokeWidth="1.5" strokeLinecap="round" />
      <path
        d="M 44 78 Q 48 82 56 82 Q 56 82 56 78"
        fill="none"
        stroke="#1a1a1a"
        strokeWidth="1.5"
        strokeLinecap="round"
      />
      <line x1="50" y1="8" x2="50" y2="13" stroke="#1a1a1a" strokeWidth="1.5" strokeLinecap="round" />
      <line x1="22" y1="22" x2="26" y2="26" stroke="#1a1a1a" strokeWidth="1.5" strokeLinecap="round" />
      <line x1="78" y1="22" x2="74" y2="26" stroke="#1a1a1a" strokeWidth="1.5" strokeLinecap="round" />
      <line x1="14" y1="42" x2="20" y2="42" stroke="#1a1a1a" strokeWidth="1.5" strokeLinecap="round" />
      <line x1="80" y1="42" x2="86" y2="42" stroke="#1a1a1a" strokeWidth="1.5" strokeLinecap="round" />
    </g>
  </svg>
);

// ── My Progress — warm amber blob, mountain + flag + dotted trail ───────

export const MyProgressIcon: React.FC = () => (
  <svg viewBox="0 0 100 100" width="100%" height="100%">
    <path
      d="M 14 26 Q 8 46 14 66 Q 26 86 50 84 Q 76 82 82 64 Q 88 40 78 26 Q 62 12 38 16 Q 20 20 14 26 Z"
      fill="#D4B978"
      opacity="0.75"
    />
    <g>
      <path d="M 18 78 L 50 28 L 82 78 Z" fill="white" stroke="#1a1a1a" strokeWidth="1" />
      <path d="M 42 40 L 50 28 L 58 40 L 54 42 L 50 38 L 46 42 Z" fill="#FDF8F0" stroke="#1a1a1a" strokeWidth="0.8" />
      <path
        d="M 24 76 Q 30 70 34 64 Q 38 58 36 52 Q 34 44 42 38 Q 48 32 50 30"
        fill="none"
        stroke="#1a1a1a"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeDasharray="2 3"
      />
      <line x1="50" y1="28" x2="50" y2="14" stroke="#1a1a1a" strokeWidth="1.5" />
      <path d="M 50 14 L 60 17 L 50 20 Z" fill="#1a1a1a" />
      <circle cx="24" cy="76" r="3" fill="#1a1a1a" />
      <line x1="10" y1="80" x2="90" y2="80" stroke="#1a1a1a" strokeWidth="1" />
    </g>
  </svg>
);

// ── Learning Paths — soft blue blob, compass face-up ────────────────────

export const LearningPathsIcon: React.FC = () => (
  <svg viewBox="0 0 100 100" width="100%" height="100%">
    <path
      d="M 14 28 Q 8 50 18 68 Q 30 86 52 82 Q 78 80 84 60 Q 88 36 74 22 Q 56 10 36 16 Q 18 22 14 28 Z"
      fill="#9DB7CC"
      opacity="0.75"
    />
    <g transform="translate(50, 52)">
      <circle cx="0" cy="0" r="26" fill="white" stroke="#1a1a1a" strokeWidth="1" />
      <line x1="0" y1="-26" x2="0" y2="-22" stroke="#1a1a1a" strokeWidth="1.5" />
      <line x1="0" y1="22" x2="0" y2="26" stroke="#1a1a1a" strokeWidth="1" />
      <line x1="-26" y1="0" x2="-22" y2="0" stroke="#1a1a1a" strokeWidth="1" />
      <line x1="22" y1="0" x2="26" y2="0" stroke="#1a1a1a" strokeWidth="1" />
      <path d="M 0 0 L 14 -16 L 4 0 Z" fill="#5B7DB0" stroke="#1a1a1a" strokeWidth="0.8" strokeLinejoin="round" />
      <path d="M 0 0 L -8 9 L -3 0 Z" fill="white" stroke="#1a1a1a" strokeWidth="0.8" strokeLinejoin="round" />
      <circle cx="0" cy="0" r="2" fill="#1a1a1a" />
      <text x="0" y="-29" textAnchor="middle" fontFamily="Source Serif 4, serif" fontSize="8" fontWeight="600" fill="#1a1a1a">
        N
      </text>
    </g>
  </svg>
);
