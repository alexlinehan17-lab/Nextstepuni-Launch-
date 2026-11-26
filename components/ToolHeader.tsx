/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * ToolHeader — shared editorial-Anthropic header used by every Innovation
 * Zone tool entry point and the Training Hub. Replaces the legacy "flat
 * coloured banner with circle blobs in the corners" pattern.
 *
 * Recipe:
 *   - Cream ground (#FAFBF6), no border, no shadow
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
import { TopBar } from './ui/Bars';
import { useScreenLeave } from './navigation/useScreenLeave';

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

/** Drawn as the agreed tool bar (navigation.md, "Top bar"): the family as a
 *  small line over the tool's name, the tool's own drawing at the right end
 *  on a phone and none on a laptop, the one line under it. No tile, no serif.
 *  `themeColor` and `icon` are kept for old callers and no longer painted. */
export const ToolHeader: React.FC<ToolHeaderProps> = ({
  eyebrow,
  title,
  subtitle,
  iconImage,
  iconBlob,
  className,
}) => {
  const leave = useScreenLeave(undefined, 'Back');
  return (
    <div className={`tool-header ${className ?? ''}`}>
      <TopBar tool ruled leave={leave} over={eyebrow} title={title} art={iconImage ?? iconBlob} />
      {subtitle ? <p className="ui-part ui-bar-sub">{subtitle}</p> : null}
    </div>
  );
};

export default ToolHeader;
