/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Colour worlds — each card/field owns a saturated identity colour. As of the
 * 2026-06-03 "hybrid" redesign the decks are light cards (white surface, bold
 * #1a1a1a border, chunky shadow) with the colour used as a HEADER BAND + accents
 * — not full-bleed dark backgrounds — so they sit in the same family as the rest
 * of the app instead of sticking out. Each world therefore carries:
 *   bg    — the identity colour for the header band / icon circle (white-text-safe)
 *   deep  — a darker shade: coloured ink for text on white, chunky shadow
 *   glow  — a lighter shade: decorative blob behind the header glyph
 *   tint  — a very light wash: chip / panel / icon-circle backgrounds on white
 *   onBg/onSoft/chip — white text + translucent chip ON the colour header
 *
 * Tones were lifted brighter/cleaner from the old muddy palette. They still avoid
 * the banned primary hues (amber/yellow/lime/violet, fire-engine red). Inline
 * `style` values only — never Tailwind classes.
 */

export interface ColorWorld {
  /** Identity colour — header band, icon circle, active pills (white-text-safe). */
  bg: string;
  /** Darker shade — coloured ink on white, chunky press shadow. */
  deep: string;
  /** Lighter shade — decorative glow blob behind the glyph. */
  glow: string;
  /** Very light wash — chip / panel / icon-circle backgrounds on a white body. */
  tint: string;
  /** Primary text on the colour band (white). */
  onBg: string;
  /** Secondary / muted text on the colour band. */
  onSoft: string;
  /** Translucent white chip / inset on the colour band. */
  chip: string;
}

const ON = '#FFFFFF';
const SOFT = 'rgba(255,255,255,0.82)';
const CHIP = 'rgba(255,255,255,0.18)';
const w = (bg: string, deep: string, glow: string, tint: string): ColorWorld =>
  ({ bg, deep, glow, tint, onBg: ON, onSoft: SOFT, chip: CHIP });

/** Named, reusable colour worlds. Bright + clean, white-text-safe on `bg`. */
/**
 * `bg` carries white label text, so every world is held at >=4.6:1 against
 * white. Seven of the twelve were originally between 3.16 and 4.13 -- they have
 * been deepened rather than switching those bands to dark ink, which would have
 * split the decks between two ink treatments. `deep` moved with them to keep
 * the chunky shadow separated from the band it sits under (~1.55:1).
 */
export const WORLDS = {
  teal:       w('#118471', '#0A6353', '#5BC9B6', '#E2F5F1'),
  ocean:      w('#3A6FD0', '#284F9A', '#7CA0E4', '#E7EEFB'),
  denim:      w('#277DA1', '#1B5D7B', '#6FBEDC', '#E4F2F8'),
  indigo:     w('#5061C9', '#38449B', '#8E9BE6', '#E9ECFB'),
  terracotta: w('#C35224', '#904020', '#EE9A76', '#FCEDE4'),
  rust:       w('#BB5735', '#903F22', '#E08C68', '#FBEAE2'),
  claret:     w('#C04668', '#8E2F48', '#DC7B96', '#FAE7ED'),
  rose:       w('#CD4260', '#95374D', '#E98AA0', '#FCE8EC'),
  pine:       w('#23845C', '#166343', '#5FC698', '#E3F5EC'),
  forest:     w('#358355', '#266240', '#6FBF90', '#E6F4EB'),
  slate:      w('#5566A8', '#3C4878', '#8995C4', '#ECEEF6'),
  cocoa:      w('#9A6B4E', '#6E4A34', '#BC9176', '#F3EBE4'),
} as const;

export type WorldName = keyof typeof WORLDS;

/**
 * Ink for coloured text/glyphs sitting directly on `--deck-paper`.
 *
 * `deep` is tuned for WHITE paper (5.5-8.8:1) and collapses on the dark deck
 * paper #242321 (1.79-2.87:1 across all twelve worlds) -- that is what made the
 * avatar initials unreadable in dark mode. `glow` is the readable tone there
 * (5.35-7.83:1). Chips on `tint` keep using `deep`: the tint wash stays light
 * in both themes, so its ink must stay dark.
 */
export const paperInk = (w: ColorWorld, dark: boolean): string => (dark ? w.glow : w.deep);

/** Resolve a world by name with a safe fallback. */
export const world = (name: WorldName): ColorWorld => WORLDS[name] ?? WORLDS.teal;
