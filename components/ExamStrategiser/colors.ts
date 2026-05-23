/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * ExamStrategiser-local colour aliases sourced from the central design tokens.
 *
 * Single source of truth for the ExamStrategiser subtree. Modules used to
 * declare their own `const TEAL = '#2A7D6F'`, `const TEAL_DARK = '#1F5F54'`,
 * `const CREAM = '#F0FAF8'` per file (~18 redeclarations). Those have all
 * been replaced with imports from this file.
 *
 * Naming preserves the existing call sites where possible:
 *   - `ACCENT` (was `TEAL`)            — brand accent
 *   - `ACCENT_DARK` (was `TEAL_DARK`)  — button depth + shadow
 *   - `ACCENT_TINT` (was `CREAM` where it meant the teal-tinted callout bg) — soft fill
 *   - `CREAM` (the actual global cream `#FDF8F0`)
 *   - `SUCCESS` / `SUCCESS_*`          — for "correct/match/level passed" states
 */

import { COLORS } from '../../design/tokens';

export const ACCENT = COLORS.accent;
export const ACCENT_DARK = COLORS.accentDark;
export const ACCENT_TINT = COLORS.accentTint;
export const ACCENT_DARK_TEXT = COLORS.accentDarkText;
export const SUCCESS = COLORS.success;
export const SUCCESS_TINT = COLORS.successTint;
export const SUCCESS_DARK_TEXT = COLORS.successDarkText;
export const CREAM = COLORS.cream;
export const CREAM_SUBTLE = COLORS.creamSubtle;
export const BORDER = COLORS.border;
