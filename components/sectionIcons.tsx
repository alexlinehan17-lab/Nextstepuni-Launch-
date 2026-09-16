/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Section artwork. The four home cards use the approved Star Crew
 * companions; the remaining tool illustrations retain their own artwork.
 */

import React from 'react';

// Decorative artwork: the surrounding card supplies the accessible name.
const CompanionArtwork: React.FC<{ character: string }> = ({ character }) => (
  <img
    src={`/assets/star-crew/companions/${character}.png`}
    alt=""
    aria-hidden="true"
    width="1254"
    height="1254"
    decoding="async"
    draggable={false}
    className="block h-full w-full object-contain"
  />
);

// ── Modules — The Thinker ────────────────────────────────────────────

export const ModulesIcon: React.FC = () => (
  <CompanionArtwork character="thinker" />
);

// ── Launchpad — The Card Dealer ──────────────────────────────────────

export const InnovationZoneIcon: React.FC = () => (
  <CompanionArtwork character="card-dealer" />
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

// ── Learning Paths — The Wayfinder ───────────────────────────────────

export const LearningPathsIcon: React.FC = () => (
  <CompanionArtwork character="wayfinder" />
);

// ── My Journey — The Islander ────────────────────────────────────────

export const MyJourneyIcon: React.FC = () => (
  <CompanionArtwork character="islander" />
);
