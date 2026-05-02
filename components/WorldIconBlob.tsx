/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * WorldIconBlob — paint blob + ink illustration for the five worlds.
 *
 * Used in ModulesView (the Library page):
 *   - Hero card: size=96
 *   - Satellite cards: size=72
 *
 * Each world has its own blob colour and a hand-illustrated PNG icon.
 * The blob is a hand-drawn-feeling rounded organic shape sized to fully
 * sit behind the icon (no cream peeking through the icon's bounding box).
 * The PNG is absolute-centred on top.
 *
 * The PNGs live at /public/assets/worlds/{file}.png and are loaded
 * via <img> rather than inlined as SVG — the artwork is the source
 * of truth and shouldn't be re-rendered as vector.
 */

import React from 'react';

export type WorldId = 'mind' | 'growth' | 'learn' | 'decode' | 'exam';

interface WorldConfig {
  /** Soft blob fill colour. */
  blob: string;
  iconPath: string;
  /** Decorative blob path — covers ~95% of the 0–100 viewBox so the
   *  icon's bounding box never extends past the blob into cream. Each
   *  world's path is slightly different so they don't read as identical. */
  blobPath: string;
  /** Per-world scale multiplier to normalise visible illustration size.
   *  PNGs have different aspect ratios + internal transparent padding,
   *  so objectFit: contain leaves them looking unequal. Eyeballed to
   *  match. */
  iconScale: number;
  /** Optional smaller scale for satellite tiles (size <= 130). Some
   *  illustrations (e.g. the pillar) fill most of their PNG canvas and
   *  read too dominant when the wrapper shrinks; this keeps the hero
   *  size prominent while shrinking it in tile/focus contexts. */
  tileIconScale?: number;
  /** Per-world blob scale. Default 1.0 leaves the small atmospheric
   *  wash; >1 grows the blob to back illustrations that fill most of
   *  their PNG canvas (e.g. the pillar). */
  blobScale?: number;
  /** Optional smaller blob scale for compact contexts. Lets the blob
   *  shrink alongside the icon in tile/focus rows so the proportions
   *  stay consistent with the hero rendering. */
  tileBlobScale?: number;
}

const WORLDS: Record<WorldId, WorldConfig> = {
  mind: {
    blob: '#B8C9E5',
    iconPath: '/assets/worlds/mind-pillar.png',
    blobPath: 'M 6 24 Q -2 52 8 78 Q 24 98 52 94 Q 86 90 94 62 Q 100 30 84 10 Q 60 -4 32 4 Q 12 12 6 24 Z',
    iconScale: 1.0,
    tileIconScale: 0.45,
    blobScale: 2.1,
    tileBlobScale: 1.4,
  },
  growth: {
    blob: '#F5C9A8',
    iconPath: '/assets/worlds/growth-branch.png',
    blobPath: 'M 4 28 Q 0 56 12 82 Q 28 100 56 96 Q 90 92 96 60 Q 100 28 82 8 Q 56 -6 30 6 Q 10 16 4 28 Z',
    iconScale: 1.0,
    tileIconScale: 0.45,
    blobScale: 2.1,
    tileBlobScale: 1.4,
  },
  learn: {
    blob: '#B8DDC8',
    iconPath: '/assets/worlds/learn-book.png',
    blobPath: 'M 8 22 Q 0 48 6 76 Q 20 96 50 96 Q 84 96 94 70 Q 100 40 84 14 Q 64 -2 36 4 Q 14 12 8 22 Z',
    iconScale: 1.0,
    tileIconScale: 0.45,
    blobScale: 2.1,
    tileBlobScale: 1.4,
  },
  decode: {
    blob: '#F0BFCE',
    iconPath: '/assets/worlds/decode-checklist.png',
    blobPath: 'M 6 22 Q -2 50 10 78 Q 26 98 56 94 Q 90 88 96 56 Q 100 24 80 6 Q 56 -6 28 6 Q 10 14 6 22 Z',
    iconScale: 1.0,
    tileIconScale: 0.45,
    blobScale: 2.1,
    tileBlobScale: 1.4,
  },
  exam: {
    blob: '#F5BFB0',
    iconPath: '/assets/worlds/exam-head.png',
    blobPath: 'M 4 26 Q 2 56 12 82 Q 26 98 52 96 Q 88 94 96 64 Q 100 34 84 10 Q 60 -4 30 6 Q 10 18 4 26 Z',
    iconScale: 1.0,
    tileIconScale: 0.45,
    blobScale: 2.1,
    tileBlobScale: 1.4,
  },
};

interface WorldIconBlobProps {
  world: WorldId;
  /** Pixel size of the entire wrapper (square). 96 for hero, 72 for satellite. */
  size?: number;
  /** Compact contexts (satellite tiles, focus rows) where canvas-filling
   *  illustrations like the pillar/sapling read too large. Defaults false
   *  (full hero scale). */
  compact?: boolean;
  className?: string;
}

export const WorldIconBlob: React.FC<WorldIconBlobProps> = ({
  world,
  size = 96,
  compact = false,
  className,
}) => {
  const config = WORLDS[world];
  const effectiveIconScale =
    compact && config.tileIconScale !== undefined
      ? config.tileIconScale
      : config.iconScale;
  const effectiveBlobScale = compact
    ? config.tileBlobScale ?? config.blobScale ?? 1
    : config.blobScale ?? 1;
  return (
    <div
      className={`relative shrink-0 ${className ?? ''}`}
      style={{ width: size, height: size, overflow: 'visible' }}
    >
      {/*
        Blob is a small atmospheric wash (~42% of wrapper), centred. The
        icon scales aggressively past the wrapper bounds so the visible
        artwork (which has internal transparent padding inside the PNG)
        ends up substantially larger than the wrapper itself.
      */}
      <svg
        className="absolute pointer-events-none"
        viewBox="0 0 100 100"
        aria-hidden="true"
        preserveAspectRatio="xMidYMid meet"
        style={{
          width: `${42 * effectiveBlobScale}%`,
          height: `${42 * effectiveBlobScale}%`,
          left: '50%',
          top: '50%',
          transform: 'translate(-50%, -50%)',
          zIndex: 0,
        }}
      >
        <path d={config.blobPath} fill={config.blob} opacity="0.85" />
      </svg>
      <img
        src={config.iconPath}
        alt=""
        style={{
          position: 'absolute',
          left: '50%',
          top: '50%',
          transform: `translate(-50%, -50%) scale(${effectiveIconScale})`,
          width: '150%',
          height: '150%',
          objectFit: 'contain',
          zIndex: 1,
        }}
        draggable={false}
      />
    </div>
  );
};

export default WorldIconBlob;
