/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * ToolIconBlob — paint blob + ink illustration for the eight Innovation
 * Zone tools, modelled on WorldIconBlob.
 *
 * Each tool has a soft-pastel painted blob behind a hand-drawn PNG. The
 * blobs are slightly different organic shapes so the eight tiles don't
 * read as identical. The PNGs live at /public/assets/tools/{id}.png and
 * are loaded via <img>; the artwork is the source of truth.
 *
 * Sizes used in the app:
 *   - IZ bento card icon area: size=72
 *   - IZ active-tool ToolHeader: size=108
 */
import React from 'react';
import { type LucideIcon, Mic } from 'lucide-react';

export type ToolIconKey =
  | 'journey'
  | 'cao-simulator'
  | 'planner'
  | 'war-room'
  | 'comeback'
  | 'future-finder'
  | 'syllabus-xray'
  | 'points-passport'
  | 'exam-reps'
  | 'college-compass'
  | 'catch-up-lane'
  | 'command-word-reflex'
  | 'how-they-did-it'
  | 'career-paths'
  | 'future-finder-revamped'
  | 'your-possible-life'
  | 'oral-trainer'
  | 'paper-trail';

interface ToolIconConfig {
  blob: string;
  blobPath: string;
  /** Hand-drawn PNG art (preferred). Omit when using an inline lucide icon instead. */
  iconPath?: string;
  iconScale: number;
  /** Inline lucide icon — used when no PNG art exists yet (e.g. catch-up-lane). */
  icon?: LucideIcon;
  iconColor?: string;
}

const TOOLS: Record<ToolIconKey, ToolIconConfig> = {
  'journey': {
    blob: '#C9C2DD',
    iconPath: '/assets/tools/journey.png',
    blobPath: 'M 6 24 Q -2 52 8 78 Q 24 98 52 94 Q 86 90 94 62 Q 100 30 84 10 Q 60 -4 32 4 Q 12 12 6 24 Z',
    iconScale: 1.0,
  },
  'cao-simulator': {
    blob: '#BCCCE3',
    iconPath: '/assets/tools/cao-simulator.png',
    blobPath: 'M 4 28 Q 0 56 12 82 Q 28 100 56 96 Q 90 92 96 60 Q 100 28 82 8 Q 56 -6 30 6 Q 10 16 4 28 Z',
    iconScale: 1.0,
  },
  'planner': {
    blob: '#C5DBC0',
    iconPath: '/assets/tools/planner.png',
    blobPath: 'M 8 22 Q 0 48 6 76 Q 20 96 50 96 Q 84 96 94 70 Q 100 40 84 14 Q 64 -2 36 4 Q 14 12 8 22 Z',
    iconScale: 1.0,
  },
  'war-room': {
    blob: '#F1B7AB',
    iconPath: '/assets/tools/war-room.png',
    blobPath: 'M 6 22 Q -2 50 10 78 Q 26 98 56 94 Q 90 88 96 56 Q 100 24 80 6 Q 56 -6 28 6 Q 10 14 6 22 Z',
    iconScale: 1.0,
  },
  'comeback': {
    blob: '#F5C7A0',
    iconPath: '/assets/tools/comeback.png',
    blobPath: 'M 4 26 Q 2 56 12 82 Q 26 98 52 96 Q 88 94 96 64 Q 100 34 84 10 Q 60 -4 30 6 Q 10 18 4 26 Z',
    iconScale: 1.0,
  },
  'future-finder': {
    blob: '#ECBBCC',
    iconPath: '/assets/tools/future-finder.png',
    blobPath: 'M 8 26 Q 0 50 8 78 Q 22 96 54 96 Q 88 94 96 64 Q 100 32 80 10 Q 56 -2 28 8 Q 12 16 8 26 Z',
    iconScale: 1.0,
  },
  'syllabus-xray': {
    blob: '#B8C5D8',
    iconPath: '/assets/tools/syllabus-xray.png',
    blobPath: 'M 6 26 Q 2 54 14 80 Q 30 98 56 94 Q 88 92 94 60 Q 100 30 82 10 Q 56 -4 30 8 Q 12 18 6 26 Z',
    iconScale: 1.0,
  },
  'points-passport': {
    blob: '#DDC9A4',
    iconPath: '/assets/tools/points-passport.png',
    blobPath: 'M 8 28 Q 4 54 12 82 Q 28 100 56 94 Q 88 90 96 60 Q 100 30 84 12 Q 60 -4 32 6 Q 14 14 8 28 Z',
    iconScale: 1.0,
  },
  'exam-reps': {
    blob: '#B5D4CC',
    iconPath: '/assets/tools/exam-reps.png',
    blobPath: 'M 6 24 Q 2 52 12 80 Q 28 98 56 94 Q 90 90 96 58 Q 100 26 82 8 Q 58 -4 30 6 Q 12 14 6 24 Z',
    iconScale: 1.0,
  },
  'college-compass': {
    blob: '#A8D5C9',
    iconPath: '/assets/tools/college-compass.png',
    blobPath: 'M 6 26 Q 0 52 10 80 Q 26 98 54 94 Q 88 90 96 60 Q 100 28 82 8 Q 56 -4 30 8 Q 12 16 6 26 Z',
    iconScale: 1.0,
  },
  'paper-trail': {
    blob: '#C7D8E8',
    iconPath: '/assets/tools/paper-trail.png',
    blobPath: 'M 5 26 Q -1 54 9 80 Q 25 99 53 95 Q 87 91 95 61 Q 101 29 83 9 Q 57 -5 31 5 Q 11 14 5 26 Z',
    iconScale: 1.25,
  },
  'catch-up-lane': {
    blob: '#AEDDE2',
    iconPath: '/assets/tools/catch-up-lane.png',
    blobPath: 'M 6 24 Q 0 52 10 80 Q 26 98 54 94 Q 88 90 96 60 Q 100 28 82 8 Q 56 -4 30 6 Q 12 14 6 24 Z',
    iconScale: 1.0,
  },
  'command-word-reflex': {
    blob: '#C7C9F5',
    iconPath: '/assets/tools/command-word-reflex.png',
    blobPath: 'M 8 26 Q 0 52 8 78 Q 22 96 54 96 Q 88 94 96 64 Q 100 32 80 10 Q 56 -2 28 8 Q 12 16 8 26 Z',
    iconScale: 1.0,
  },
  'how-they-did-it': {
    blob: '#A8D0CE',
    iconPath: '/assets/tools/how-they-did-it.png',
    blobPath: 'M 6 24 Q 0 52 10 80 Q 26 98 54 94 Q 88 90 96 60 Q 100 28 82 8 Q 56 -4 30 6 Q 12 14 6 24 Z',
    iconScale: 1.0,
  },
  'career-paths': {
    blob: '#A8D0CE',
    iconPath: '/assets/tools/career-paths.png',
    blobPath: 'M 8 26 Q 0 50 8 78 Q 22 96 54 96 Q 88 94 96 64 Q 100 32 80 10 Q 56 -2 28 8 Q 12 16 8 26 Z',
    iconScale: 1.0,
  },
  'future-finder-revamped': {
    blob: '#ECBBCC',
    iconPath: '/assets/tools/future-finder-revamped.png',
    blobPath: 'M 8 26 Q 0 50 8 78 Q 22 96 54 96 Q 88 94 96 64 Q 100 32 80 10 Q 56 -2 28 8 Q 12 16 8 26 Z',
    iconScale: 1.0,
  },
  'your-possible-life': {
    blob: '#BCD3E0',
    iconPath: '/assets/tools/your-possible-life.png',
    blobPath: 'M 6 24 Q -2 52 8 78 Q 24 98 52 94 Q 86 90 94 62 Q 100 30 84 10 Q 60 -4 32 4 Q 12 12 6 24 Z',
    iconScale: 1.0,
  },
  'oral-trainer': {
    blob: '#BFDCC4',
    blobPath: 'M 6 24 Q 0 52 10 80 Q 26 98 54 94 Q 88 90 96 60 Q 100 28 82 8 Q 56 -4 30 6 Q 12 14 6 24 Z',
    icon: Mic,
    iconColor: '#3A6B47',
    iconScale: 1.0,
  },
};

interface ToolIconBlobProps {
  toolId: ToolIconKey;
  /** Pixel size of the entire wrapper (square). 72 for grid card, 108 for ToolHeader. */
  size?: number;
  className?: string;
}

export const ToolIconBlob: React.FC<ToolIconBlobProps> = ({
  toolId,
  size = 72,
  className,
}) => {
  const cfg = TOOLS[toolId];
  if (!cfg) return null;
  return (
    <div
      className={`relative shrink-0 ${className ?? ''}`}
      style={{ width: size, height: size, overflow: 'visible' }}
    >
      {/* Painted blob — sized to read as a soft ground behind the icon. */}
      <svg
        className="absolute pointer-events-none"
        viewBox="0 0 100 100"
        aria-hidden="true"
        preserveAspectRatio="xMidYMid meet"
        style={{
          width: '90%',
          height: '90%',
          left: '50%',
          top: '50%',
          transform: 'translate(-50%, -50%)',
          zIndex: 0,
        }}
      >
        <path d={cfg.blobPath} fill={cfg.blob} opacity="0.85" />
      </svg>
      {cfg.icon ? (
        <cfg.icon
          size={size * 0.42}
          strokeWidth={2}
          color={cfg.iconColor ?? '#1a1a1a'}
          style={{ position: 'absolute', left: '50%', top: '50%', transform: 'translate(-50%, -50%)', zIndex: 1 }}
          aria-hidden="true"
        />
      ) : (
        <img
          src={cfg.iconPath}
          alt=""
          style={{
            position: 'absolute',
            left: '50%',
            top: '50%',
            transform: `translate(-50%, -50%) scale(${cfg.iconScale})`,
            width: '94%',
            height: '94%',
            objectFit: 'contain',
            zIndex: 1,
          }}
          draggable={false}
        />
      )}
    </div>
  );
};

export default ToolIconBlob;
