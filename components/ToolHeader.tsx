/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * ToolHeader — shared editorial-Anthropic header used by every Innovation
 * Zone tool entry point and the Training Hub. Replaces the legacy "flat
 * coloured banner with circle blobs in the corners" pattern.
 *
 * Recipe:
 *   - Cream ground (#FDF8F0), no border, no shadow
 *   - 108px square colour tile on the left, white-ink illustration inside
 *   - Eyebrow + serif title + sans subtitle on the right
 *
 * The icon component receives the theme colour so it can use the tile fill
 * as "negative space" inside white shapes (Syllabus X-Ray, Spaced
 * Repetition Timetable, Comeback Engine, Points Passport).
 *
 * Phase 2 / icon upgrade path: the API also accepts an `iconImage` URL so
 * higher-fidelity hand-drawn raster illustrations (Midjourney / DALL-E /
 * GPT-Image) can be swapped in behind a feature flag without touching the
 * consumers.
 *
 * Phase 2 surfaces still using the legacy banner-blob pattern (track and
 * migrate in a future round): atmospheric surfaces (Countdown, North Star,
 * My Progress, Today's Focus) and any other section headers across the app
 * that haven't been brought into this system yet.
 */

import React from 'react';

interface ToolHeaderProps {
  /** Saturated palette colour for the tile fill. */
  themeColor: string;
  /** Small uppercase label, e.g. "Understand · Career discovery". Sentence case in source. */
  eyebrow: string;
  /** Tool name. */
  title: string;
  /** One-line description. */
  subtitle: string;
  /** Inline SVG icon component. Receives themeColor via parent. */
  icon?: React.ReactNode;
  /** Alternative to `icon` — a raster image source for higher-fidelity illustrations. */
  iconImage?: string;
  /** Painted-blob illustration rendered without the saturated tile (e.g.
   *  ToolIconBlob). When supplied, takes precedence over `icon`/`iconImage`
   *  and skips the tile chrome entirely. */
  iconBlob?: React.ReactNode;
  /** Optional className on the wrapper for layout overrides. */
  className?: string;
}

export const ToolHeader: React.FC<ToolHeaderProps> = ({
  themeColor,
  eyebrow,
  title,
  subtitle,
  icon,
  iconImage,
  iconBlob,
  className,
}) => {
  return (
    <div
      className={`flex items-start gap-7 ${className ?? ''}`}
    >
      {/* Tile (or blob — blob mode skips the saturated background) */}
      {iconBlob ? (
        <div
          className="shrink-0 flex items-center justify-center"
          style={{ width: 108, height: 108 }}
        >
          {iconBlob}
        </div>
      ) : (
        <div
          className="shrink-0 flex items-center justify-center overflow-hidden"
          style={{
            width: 108,
            height: 108,
            borderRadius: 18,
            background: themeColor,
          }}
        >
          {iconImage ? (
            <img
              src={iconImage}
              alt=""
              style={{ width: '64%', height: '64%', objectFit: 'contain' }}
            />
          ) : icon ? (
            <div style={{ width: '64%', height: '64%' }}>{icon}</div>
          ) : null}
        </div>
      )}

      {/* Text */}
      <div className="flex-1 min-w-0">
        <p
          style={{
            fontFamily: "'DM Sans', system-ui, sans-serif",
            fontSize: 11,
            fontWeight: 500,
            letterSpacing: '0.18em',
            textTransform: 'uppercase',
            color: 'rgba(0,0,0,0.5)',
            margin: 0,
          }}
        >
          {eyebrow}
        </p>
        <h1
          className="font-serif"
          style={{
            fontSize: 38,
            fontWeight: 500,
            letterSpacing: '-1.2px',
            lineHeight: 1.0,
            color: '#1a1a1a',
            margin: 0,
            marginTop: 14,
          }}
        >
          {title}
        </h1>
        <p
          style={{
            fontFamily: "'DM Sans', system-ui, sans-serif",
            fontSize: 15,
            fontWeight: 400,
            color: 'rgba(0,0,0,0.62)',
            lineHeight: 1.5,
            maxWidth: 460,
            margin: 0,
            marginTop: 14,
          }}
        >
          {subtitle}
        </p>
      </div>
    </div>
  );
};

export default ToolHeader;
