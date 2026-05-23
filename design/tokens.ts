/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Design tokens — single source of truth for colour hex strings used in
 * places Tailwind classes can't reach: inline `style={{}}` props, SVG
 * `fill=` / `stroke=` attributes, Framer Motion values, and any other
 * runtime-dynamic hex literal.
 *
 * For Tailwind-class consumers see `tailwind.config.ts` (`accent`,
 * `accentDark`, `accentTint`, `success`, etc.).
 *
 * For CSS-variable consumers (e.g., `bg-[var(--accent-hex)]`) see the
 * `:root` block in `index.html`.
 *
 * All three layers must stay in sync. When changing a colour, update all
 * three — and update CLAUDE.md's design system section.
 *
 * Pivot history:
 *  - teal #2A7D6F → orange #F26B1F
 *  - introduced `success` (green) as a distinct semantic — orange does
 *    NOT carry "good/correct/complete" semantics.
 */

export const COLORS = {
  accent: '#F26B1F',
  accentDark: '#B54D14',
  accentTint: '#FDEEDF',
  accentDarkText: '#8C3A0E',
  success: '#3A8D5F',
  successTint: '#E8F2EC',
  successDarkText: '#1F5F3E',
  cream: '#FDF8F0',
  creamSubtle: '#F9F9F7',
  border: '#1A1A1A',
} as const;

export type ColorToken = keyof typeof COLORS;
