/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * Dark mode is delivered two ways in this codebase:
 *
 *  1. semantic tokens in index.css, redefined under `.dark`, and
 *  2. a compatibility layer that rewrites the pre-token primitives
 *     (`bg-white`, `text-zinc-900`, inline `background: #fff`) onto those
 *     tokens for any screen carrying `.product-shell` or `.theme-compat`.
 *
 * Both have a failure mode that is invisible until someone opens the app in the
 * dark: a token defined for light and forgotten under `.dark` silently keeps its
 * light value, and a screen that never opts into the compat layer keeps white
 * cards while its text flips to near-white. That is exactly how the login
 * heading ended up at 1.1:1 against a white card.
 */
import { describe, it, expect } from 'vitest';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

const ROOT = resolve(__dirname, '..');
const css = readFileSync(resolve(ROOT, 'index.css'), 'utf8');

function tokensIn(selector: string): Map<string, string> {
  const re = new RegExp(String.raw`(?:^|\})\s*${selector}\s*\{([\s\S]*?)\n\}`, 'm');
  const body = css.match(re)?.[1] ?? '';
  const out = new Map<string, string>();
  for (const m of body.matchAll(/(--[a-z0-9-]+)\s*:\s*([^;]+);/g)) out.set(m[1], m[2].trim());
  return out;
}

const light = tokensIn(':root');
const dark = tokensIn(String.raw`\.dark`);

describe('dark mode tokens', () => {
  it('parses both blocks', () => {
    expect(light.size).toBeGreaterThan(20);
    expect(dark.size).toBeGreaterThan(20);
  });

  it('redefines every themed token under .dark', () => {
    // Tokens that are deliberately theme-independent live here. Anything else
    // missing from .dark keeps its light value in dark mode, which is a bug.
    const themeIndependent = new Set([
      '--result-stat-count',
      // Ink sitting ON the accent stays dark in both themes. The accent is a
      // mid-orange either way, and dark ink clears AA on it where white does
      // not (white on #F26B1F is only 3.04:1).
      '--ink-on-accent',
    ]);
    const missing = [...light.keys()]
      .filter(k => !dark.has(k) && !themeIndependent.has(k));
    expect(missing, `defined for light but not for dark: ${missing.join(', ')}`).toEqual([]);
  });

  it('actually changes value in dark rather than repeating the light one', () => {
    const identical = [...dark.entries()]
      .filter(([k, v]) => light.has(k) && light.get(k)!.toLowerCase() === v.toLowerCase())
      // A few are intentionally shared: the brand accent and the CTA ink stay put.
      .filter(([k]) => !['--cta-invert-ink'].includes(k))
      .map(([k]) => k);
    expect(identical, `same value in both themes: ${identical.join(', ')}`).toEqual([]);
  });

  /**
   * Light mode was explicitly out of scope for the dark-mode work. These are the
   * values the editorial pages and the login CTA used before it, pinned so a
   * later token tidy-up cannot quietly restyle light mode.
   */
  it('keeps the pre-existing light values byte-identical', () => {
    const pinned: Record<string, string> = {
      '--page-canvas': '#f0f0f0',
      '--page-body': '#5a5550',
      '--page-muted': '#7a7068',
      '--page-label': '#9e9186',
      '--ink-faint': '#B0A898',
      '--hairline': '#EDEBE8',
      '--accent-tint': '#FDEEDF',
      '--accent-tint-ink': '#8C3A0E',
      '--success-tint': '#E8F2EC',
      '--success-tint-ink': '#1F5F3E',
      '--cta-invert-bg': '#FFFFFF',
      '--cta-invert-ink': '#1A1A1A',
    };
    for (const [name, value] of Object.entries(pinned)) {
      expect(light.get(name)?.toLowerCase(), `${name} drifted in light mode`).toBe(value.toLowerCase());
    }
  });
});

describe('dark mode compatibility layer', () => {
  it('applies to .theme-compat as well as .product-shell', () => {
    const shellOnly = css
      .split('\n')
      .filter(l => l.trimStart().startsWith('.dark .product-shell'));
    expect(shellOnly, 'these dark rules never reach .theme-compat screens').toEqual([]);
    expect(css).toContain('.dark :is(.product-shell, .theme-compat)');
  });

  it('leaves the field grammar scoped to .product-shell only', () => {
    // These rules are NOT dark-scoped. Extending them to .theme-compat would
    // restyle inputs on those screens in light mode too.
    expect(css).toMatch(/^\.product-shell :where\(input/m);
    expect(css).not.toMatch(/^\.theme-compat :where\(input/m);
  });
});

describe('screens opt into a dark treatment', () => {
  // Every screen here rendered white cards under near-white text before the fix.
  const needsCompat = [
    'components/LoginPage.tsx',
    'components/ResetPasswordPage.tsx',
    'components/AccreditationPage.tsx',
    'components/CutContentPage.tsx',
    'components/WipTools.tsx',
    'components/YearPlansView.tsx',
  ];
  for (const file of needsCompat) {
    it(`${file} carries theme-compat`, () => {
      expect(readFileSync(resolve(ROOT, file), 'utf8')).toContain('theme-compat');
    });
  }

  it('no screen opts out of the theme with a hard-coded light override', () => {
    // LoginPage and ResetPasswordPage used `data-theme="light"` + colorScheme,
    // which set the surface but not the text, leaving near-white type on white.
    for (const file of needsCompat) {
      const src = readFileSync(resolve(ROOT, file), 'utf8');
      expect(src, `${file} still forces light`).not.toContain('data-theme="light"');
      expect(src, `${file} still forces light`).not.toContain("colorScheme: 'light'");
    }
  });
});
