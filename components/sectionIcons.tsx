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

// ── Modules — sage blob, hand-drawn open door + terracotta mat ──────────

export const ModulesIcon: React.FC = () => (
  <svg viewBox="0 0 100 100" width="100%" height="100%">
    <path
      d="M 14 30 Q 8 50 16 70 Q 28 86 50 84 Q 76 82 82 64 Q 88 42 76 26 Q 60 14 38 18 Q 20 22 14 30 Z"
      fill="#A8C9A0"
      opacity="0.75"
    />
    <image
      href="/assets/section-icons/modules.png"
      x="10"
      y="10"
      width="80"
      height="80"
      preserveAspectRatio="xMidYMid meet"
    />
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

// ── My Progress — warm amber blob, hand-drawn mountain + winding trail ──

export const MyProgressIcon: React.FC = () => (
  <svg viewBox="0 0 100 100" width="100%" height="100%">
    <path
      d="M 14 26 Q 8 46 14 66 Q 26 86 50 84 Q 76 82 82 64 Q 88 40 78 26 Q 62 12 38 16 Q 20 20 14 26 Z"
      fill="#D4B978"
      opacity="0.75"
    />
    <image
      href="/assets/section-icons/my-progress.png"
      x="10"
      y="10"
      width="80"
      height="80"
      preserveAspectRatio="xMidYMid meet"
    />
  </svg>
);

// ── Learning Paths — soft blue blob, hand-drawn map illustration ─────────

export const LearningPathsIcon: React.FC = () => (
  <svg viewBox="0 0 100 100" width="100%" height="100%">
    <path
      d="M 14 28 Q 8 50 18 68 Q 30 86 52 82 Q 78 80 84 60 Q 88 36 74 22 Q 56 10 36 16 Q 18 22 14 28 Z"
      fill="#9DB7CC"
      opacity="0.75"
    />
    <image
      href="/assets/section-icons/learning-paths.png"
      x="10"
      y="10"
      width="80"
      height="80"
      preserveAspectRatio="xMidYMid meet"
    />
  </svg>
);
