/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Colour worlds — the "colour as environment" palette for the immersive card
 * decks (How They Did It, Career Paths). Each world is a bold, saturated,
 * full-bleed background that white text sits on, in the Headspace register —
 * deliberately a different visual language from the white-card educational
 * modules. No gradients, no coloured left borders; the colour IS the surface.
 *
 * These tones avoid the banned primary hues (amber/yellow, purple, lime, and
 * fire-engine red) while staying bold. Used as inline `style` values, never as
 * Tailwind classes (CDN constraint).
 */

export interface ColorWorld {
  /** Main saturated surface colour. */
  bg: string;
  /** A darker shade of the same hue — chunky press shadows, footers. */
  deep: string;
  /** A lighter shade — decorative glow blob behind the glyph. */
  glow: string;
  /** Primary text on the surface (white). */
  onBg: string;
  /** Secondary / muted text on the surface. */
  onSoft: string;
  /** Translucent white chip / inset surface on the colour. */
  chip: string;
}

const ON = '#FFFFFF';
const SOFT = 'rgba(255,255,255,0.74)';
const CHIP = 'rgba(255,255,255,0.15)';
const w = (bg: string, deep: string, glow: string): ColorWorld => ({ bg, deep, glow, onBg: ON, onSoft: SOFT, chip: CHIP });

/** Named, reusable colour worlds. Bold + saturated, white-text-safe. */
export const WORLDS = {
  teal: w('#0E7C6B', '#0A5B4E', '#33A491'),
  ocean: w('#2A4D8F', '#1E396C', '#5179B8'),
  denim: w('#2E6E8E', '#21516A', '#5197B4'),
  indigo: w('#34407F', '#26305F', '#5C68A6'),
  terracotta: w('#C0532E', '#97401F', '#DB7B51'),
  rust: w('#A8472A', '#80341E', '#C76A47'),
  claret: w('#A23355', '#7C2541', '#C45878'),
  rose: w('#B23A5B', '#8A2C46', '#CE6080'),
  pine: w('#1F6B4A', '#154E36', '#3F8E68'),
  forest: w('#2C5E3F', '#1F472E', '#4C815F'),
  slate: w('#3B4A6B', '#2B3650', '#5E6E92'),
  cocoa: w('#6E4A36', '#523629', '#8C6A54'),
} as const;

export type WorldName = keyof typeof WORLDS;

/** Resolve a world by name with a safe fallback. */
export const world = (name: WorldName): ColorWorld => WORLDS[name] ?? WORLDS.teal;
