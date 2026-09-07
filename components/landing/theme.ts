/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Landing-page theme. The marketing site uses the brand sheet Alex supplied
 * on 2026-09-07 — Paper, Charcoal, Orange, Orange text — and nothing else.
 * These are deliberately NOT imported from design/tokens.ts: the app's
 * success/tint semantics do not apply to a marketing page, and the page must
 * stay white-canvas even if the app's tokens drift.
 */

export const L = {
  paper: '#FFFFFF',
  ink: '#1A1A1A',
  orange: '#F26B1F',
  /** Orange darkened to pass as TEXT on white (7:1-ish). Never use raw orange for words. */
  orangeText: '#B84A0C',
  /** The only tint on the page: orange at 10% on white, for hover fills and the active playground tab. */
  orangeTint: '#FDEEDF',
  /** Body copy that is not the headline. */
  muted: '#5F5A55',
  /** Eyebrows, captions, footnotes. */
  faint: '#766A5F',
  /** Structural rules between rows. Ink at low alpha so it reads as pencil, not border. */
  hairline: 'rgba(26, 26, 26, 0.14)',
  /** Card and frame edges — the "white + edge" look. */
  edge: '#1A1A1A',
} as const;

export const FONT = {
  serif: "'Source Serif 4', Georgia, 'Times New Roman', serif",
  sans: "'DM Sans', system-ui, -apple-system, sans-serif",
  mono: "'Apercu Mono Pro', 'Roboto Mono', ui-monospace, monospace",
} as const;

/** Section spacing rhythm: 128 desktop / 72 mobile, as measured off the references. */
export const SPACE = { section: 'py-[72px] md:py-[128px]', sectionTight: 'py-[56px] md:py-[96px]' } as const;

/** Where the primary CTA sends people. The app's sign-in lives at the root. */
export const APP_URL = '/?from=landing';
/** There is no dedicated sign-in route: every path renders the login page when signed out. */
export const APP_SIGNIN_URL = '/?from=landing';
