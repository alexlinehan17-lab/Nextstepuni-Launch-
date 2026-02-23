/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React from 'react';

type MoodType = 'calm' | 'balanced' | 'energized' | 'stressed';

interface MoodFaceIconProps {
  mood: MoodType | string;
  size?: number;
  className?: string;
}

export const MoodFaceIcon: React.FC<MoodFaceIconProps> = ({ mood, size = 24, className = '' }) => {
  return (
    <svg
      viewBox="0 0 24 24"
      width={size}
      height={size}
      fill="none"
      className={className}
      stroke="currentColor"
      strokeWidth={1.5}
      strokeLinecap="round"
    >
      {/* Outer circle */}
      <circle cx="12" cy="12" r="10" />

      {mood === 'calm' && (
        <>
          {/* Closed eyes — small downward arcs */}
          <path d="M7.5 10.5c0.5 0.8 1.5 0.8 2 0" />
          <path d="M14.5 10.5c0.5 0.8 1.5 0.8 2 0" />
          {/* Gentle smile */}
          <path d="M8.5 14.5c1 1.5 5 1.5 7 0" />
        </>
      )}

      {mood === 'balanced' && (
        <>
          {/* Dot eyes */}
          <circle cx="9" cy="10.5" r="1" fill="currentColor" stroke="none" />
          <circle cx="15" cy="10.5" r="1" fill="currentColor" stroke="none" />
          {/* Straight mouth */}
          <path d="M9 15h6" />
        </>
      )}

      {mood === 'energized' && (
        <>
          {/* Dot eyes */}
          <circle cx="9" cy="10.5" r="1" fill="currentColor" stroke="none" />
          <circle cx="15" cy="10.5" r="1" fill="currentColor" stroke="none" />
          {/* Wide smile */}
          <path d="M7.5 13.5c1.2 2.5 6.8 2.5 9 0" />
        </>
      )}

      {mood === 'stressed' && (
        <>
          {/* Dot eyes */}
          <circle cx="9" cy="11" r="1" fill="currentColor" stroke="none" />
          <circle cx="15" cy="11" r="1" fill="currentColor" stroke="none" />
          {/* Angled brow lines */}
          <path d="M7 8.5l3 1" />
          <path d="M17 8.5l-3 1" />
          {/* Frown */}
          <path d="M8.5 16c1-1.5 5-1.5 7 0" />
        </>
      )}
    </svg>
  );
};

export const MOOD_KEYS: MoodType[] = ['calm', 'balanced', 'energized', 'stressed'];

export const MOOD_LABELS: Record<MoodType, string> = {
  calm: 'Calm',
  balanced: 'Balanced',
  energized: 'Energized',
  stressed: 'Stressed',
};
