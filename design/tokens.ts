/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Design tokens — the TypeScript mirror of the token home (the :root and
 * .dark blocks of index.css) for colour hex strings used in
 * places Tailwind classes can't reach: inline `style={{}}` props, SVG
 * `fill=` / `stroke=` attributes, Framer Motion values, and any other
 * runtime-dynamic hex literal.
 *
 * For Tailwind-class consumers see `tailwind.config.ts` (`accent`,
 * `accentDark`, `accentTint`, `success`, etc.).
 *
 * For CSS-variable consumers (e.g., `bg-[var(--accent-hex)]`) see the
 * `:root` block in `index.css`.
 *
 * All three layers must stay in sync. When changing a colour, update all
 * three — and update CLAUDE.md's design system section.
 *
 * Pivot history:
 *  - teal → the retired orange
 *  - introduced `success` (green) as a distinct semantic — orange does
 *    NOT carry "good/correct/complete" semantics.
 *  - the retired orange → #eb692a (Oct 2026): one orange, the Kobra theme's
 *    --nsu-orange, also on :root in index.css.
 */

export const COLORS = {
  accent: '#eb692a',
  accentDark: '#B54D14',
  accentTint: '#FDEEDF',
  accentDarkText: '#8C3A0E',
  success: '#3A8D5F',
  successTint: '#E8F2EC',
  successDarkText: '#1F5F3E',
  border: '#1A1A1A',
} as const;

export type ColorToken = keyof typeof COLORS;

/** The one orange at an alpha, for places a CSS variable cannot reach (SVG
 *  presentation attributes, canvas). In CSS write rgba(var(--nsu-orange-rgb), a). */
export const accentRgba = (alpha: number): string => `rgba(235, 105, 42, ${alpha})`;
