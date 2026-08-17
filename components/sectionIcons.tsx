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
      x="0"
      y="0"
      width="100"
      height="100"
      preserveAspectRatio="xMidYMid meet"
    />
  </svg>
);

// ── Launchpad — dusty pink blob, hand-drawn rocket ──────────────────────

export const InnovationZoneIcon: React.FC = () => (
  <svg viewBox="0 0 100 100" width="100%" height="100%">
    <path
      d="M 12 28 Q 8 48 18 66 Q 30 84 52 82 Q 78 80 84 60 Q 88 38 74 22 Q 56 10 36 16 Q 18 22 12 28 Z"
      fill="#D9A9C2"
      opacity="0.75"
    />
    <image
      href="/assets/section-icons/launchpad.png"
      x="6"
      y="-6"
      width="88"
      height="112"
      preserveAspectRatio="xMidYMid meet"
    />
  </svg>
);

// ── Ways In — lilac blob, several routes into one exact page ───────────

export const WaysInIcon: React.FC = () => (
  <svg viewBox="0 0 100 100" width="100%" height="100%">
    <path
      d="M 11 27 Q 5 49 15 70 Q 28 88 52 84 Q 79 81 87 59 Q 91 36 76 20 Q 57 9 34 15 Q 17 20 11 27 Z"
      fill="#D7B7CB"
      opacity="0.78"
    />
    <image
      href="/assets/tools/ways-in.svg"
      x="3"
      y="3"
      width="94"
      height="94"
      preserveAspectRatio="xMidYMid meet"
    />
  </svg>
);

// ── My Progress — warm amber blob, hand-drawn summit mountain ──────────

export const MyProgressIcon: React.FC = () => (
  <svg viewBox="0 0 100 100" width="100%" height="100%">
    <path
      d="M 14 26 Q 8 46 14 66 Q 26 86 50 84 Q 76 82 82 64 Q 88 40 78 26 Q 62 12 38 16 Q 20 20 14 26 Z"
      fill="#D4B978"
      opacity="0.75"
    />
    <image
      href="/assets/section-icons/my-progress-mountain.png"
      x="-8"
      y="-8"
      width="116"
      height="116"
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

// ── My Journey — sea-glass blob, buildable island + destination flag ───

export const MyJourneyIcon: React.FC = () => (
  <svg viewBox="0 0 100 100" width="100%" height="100%">
    <path
      d="M 12 30 Q 9 49 17 68 Q 27 85 50 86 Q 72 84 84 66 Q 89 45 79 27 Q 62 13 40 16 Q 21 18 12 30 Z"
      fill="#8FC8C0"
      opacity="0.75"
    />
    <image
      href="/assets/section-icons/my-journey.png"
      x="-12"
      y="-12"
      width="124"
      height="124"
      preserveAspectRatio="xMidYMid meet"
    />
  </svg>
);
