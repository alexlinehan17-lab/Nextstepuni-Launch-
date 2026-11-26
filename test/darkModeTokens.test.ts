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
import { resolve as resolve_ } from 'node:path';

const ROOT = resolve_(__dirname, '..');
const css = readFileSync(resolve_(ROOT, 'index.css'), 'utf8');
const html = readFileSync(resolve_(ROOT, 'index.html'), 'utf8');

function tokensIn(selector: string): Map<string, string> {
  const re = new RegExp(String.raw`(?:^|\})\s*${selector}\s*\{([\s\S]*?)\n\}`, 'm');
  const body = css.match(re)?.[1] ?? '';
  const out = new Map<string, string>();
  for (const m of body.matchAll(/(--[a-z0-9-]+)\s*:\s*([^;]+);/g)) out.set(m[1], m[2].trim());
  return out;
}

const light = tokensIn(':root');
const dark = tokensIn(String.raw`\.dark`);

/** A token whose light value is `var(--other)` is an alias: it follows the set in both themes. */
const isAlias = (name: string) => /^var\(--[a-z0-9-]+\)$/.test(light.get(name) ?? '');
/** Follow aliases to a literal, in the given theme. */
function resolve(name: string, theme: 'light' | 'dark'): string {
  let value = (theme === 'dark' ? dark.get(name) : undefined) ?? light.get(name) ?? '';
  for (let i = 0; i < 5; i += 1) {
    const ref = value.match(/^var\((--[a-z0-9-]+)\)$/);
    if (!ref) break;
    value = (theme === 'dark' ? dark.get(ref[1]) : undefined) ?? light.get(ref[1]) ?? '';
  }
  return value;
}

/**
 * The one set of values, exactly as the design system specifies it
 * (nextstepuni-design skill, references/tokens.md, decided 24-25 Nov 2026).
 * Pinned to the literal, light and dark, so a dark value cannot quietly drift
 * into a "slightly different black" again and no part of the set can go missing.
 */
const THE_SET: Record<string, [light: string, dark: string]> = {
  '--surface-canvas': ['#ffffff', '#181818'],
  '--surface-paper': ['#ffffff', '#242424'],
  '--surface-soft': ['#f5f5f5', '#101010'],
  '--surface-raised': ['#ffffff', '#2c2c2c'],
  '--ink-primary': ['#171717', '#f5f5f5'],
  '--ink-secondary': ['#575757', '#bbbbbb'],
  '--ink-muted': ['#6b6b6b', '#9a9a9a'],
  '--hairline': ['#e5e5e5', '#3a3a3a'],
  '--outline-soft': ['#d6d6d6', '#505050'],
  '--outline-strong': ['#383838', '#f5f5f5'],
  '--action': ['#191919', '#f5f5f5'],
  '--action-ink': ['#ffffff', '#181818'],
  '--nsu-orange': ['#eb692a', '#eb692a'],
  '--accent-text': ['#b84a0c', '#f58c4e'],
  '--success-hex': ['#3a8d5f', '#56ad7c'],
  '--success-tint': ['#e8f2ec', '#1d3327'],
  '--success-tint-ink': ['#1f5f3e', '#9fd9b6'],
  '--danger-tint': ['#fde4e4', '#3a2020'],
  '--danger-tint-ink': ['#8e2c2c', '#f0a9a9'],
  '--lift-ctl': ['0 1px 2px rgba(23, 23, 23, 0.06)', 'none'],
  '--lift': ['0 2px 3px rgba(0, 0, 0, 0.03), 0 13px 25px -9px rgba(0, 0, 0, 0.14)', 'none'],
  '--float': ['0 18px 40px -18px rgba(20, 20, 18, 0.34)', '0 18px 40px -18px rgba(0, 0, 0, 0.7)'],
};

describe('the one set of values', () => {
  for (const [token, [lightValue, darkValue]] of Object.entries(THE_SET)) {
    it(`${token} is ${lightValue} in light and ${darkValue} in dark`, () => {
      expect(resolve(token, 'light').toLowerCase(), `${token} (light)`).toBe(lightValue);
      expect(resolve(token, 'dark').toLowerCase(), `${token} (dark)`).toBe(darkValue);
    });
  }

  it('keeps focus in its own policy file, light and dark', () => {
    const focus = readFileSync(resolve_(ROOT, 'design/quiet-focus.css'), 'utf8');
    expect(focus).toMatch(/:root\s*\{\s*--nsu-focus-edge:\s*#383833;/);
    expect(focus).toMatch(/\.dark\s*\{\s*--nsu-focus-edge:\s*#e4e2db;/);
  });

  it('has no cream left in the set', () => {
    for (const name of ['--bg-card-soft', '--bg-card-cream']) {
      expect(light.has(name), `${name} is cream and was deleted`).toBe(false);
      expect(html, `${name} is cream and was deleted`).not.toContain(`${name}:`);
    }
  });

  it('defines the scales once, outside the colour blocks', () => {
    for (const step of ['--space-1: 4px', '--space-4: 16px', '--space-6: 24px', '--space-8: 32px', '--space-12: 48px',
      '--r-sm: 9px', '--r-ctl: 12px', '--r-box: 14px', '--r-card: 20px']) {
      expect(css, `${step} missing`).toContain(step);
    }
    for (const style of ['display', 'title', 'name', 'heading', 'row', 'body', 'sub', 'meta', 'label', 'readout', 'number']) {
      expect(css, `type style .t-${style} missing`).toMatch(new RegExp(String.raw`^\.t-${style} \{`, 'm'));
    }
  });
});

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
      // not (white on #eb692a is only 3.2:1).
      '--ink-on-accent',
      // A fill colour's ink on white: #F59E0B is 2.15:1 there. On a dark
      // ground the authored colour already passes.
      '--warning-text',
      // The one orange (Kobra's --nsu-orange, also Tailwind's accent) is the
      // same in both themes, as it is in approved-ui-theme.css, and so are its
      // triplet and the darker shades that edge an orange button.
      '--nsu-orange',
      '--nsu-orange-rgb',
      '--accent-dark',
      '--accent-dark-hex',
      '--accent-dark-text',
      '--accent-dark-text-hex',
      '--success-dark-text',
    ]);
    const missing = [...light.keys()]
      .filter(k => !dark.has(k) && !themeIndependent.has(k) && !isAlias(k));
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
   * The ink scale clears AA on every light surface. The darkest one in the set
   * is --surface-soft (#f5f5f5, a well or a disabled button), so it binds; the
   * page itself is white. Asserted by contrast rather than pinned, so the
   * palette can be re-tuned without rewriting the test.
   */
  const srgb = (hex: string) => [1, 3, 5].map(i => {
    const v = parseInt(hex.slice(i, i + 2), 16) / 255;
    return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
  });
  const lu = (hex: string) => { const [r, g, b] = srgb(hex); return 0.2126 * r + 0.7152 * g + 0.0722 * b; };
  const cr = (a: string, b: string) => {
    const [l1, l2] = [lu(a), lu(b)].sort((x, y) => y - x);
    return (l1 + 0.05) / (l2 + 0.05);
  };
  const INKS = ['--ink-primary', '--ink-secondary', '--ink-muted', '--ink-faint',
    '--page-body', '--page-muted', '--page-label', '--text-primary', '--text-body', '--text-muted', '--text-label'];

  it('clears AA on the darkest light surface', () => {
    const SOFT = resolve('--surface-soft', 'light');
    for (const token of [...INKS, '--accent-text', '--warning-text']) {
      const v = resolve(token, 'light');
      expect(v, `${token} missing`).toMatch(/^#[0-9a-f]{6}$/i);
      const r = cr(v, SOFT);
      expect(r, `${token} is ${r.toFixed(2)}:1 on --surface-soft ${SOFT}`).toBeGreaterThanOrEqual(4.5);
    }
  });

  it('clears AA in dark on every surface a word can sit on', () => {
    for (const surface of ['--surface-canvas', '--surface-paper', '--surface-raised', '--surface-soft']) {
      const ground = resolve(surface, 'dark');
      for (const token of [...INKS, '--accent-text']) {
        const r = cr(resolve(token, 'dark'), ground);
        expect(r, `${token} is ${r.toFixed(2)}:1 on dark ${surface}`).toBeGreaterThanOrEqual(4.5);
      }
    }
  });

  it('keeps the three ink steps distinguishable from each other', () => {
    // Raising every step to exactly 4.5 collapses them into a single tone.
    // Three steps is what the 4.5-7:1 band actually fits.
    const steps = ['--ink-primary', '--ink-secondary', '--ink-muted']
      .map(t => parseInt(resolve(t, 'light').slice(1, 3), 16));
    for (let i = 1; i < steps.length; i++) {
      expect(steps[i] - steps[i - 1], 'the ink steps have collapsed together').toBeGreaterThanOrEqual(8);
    }
  });

  it('every older name for a page, ink or line is an alias of the set', () => {
    for (const name of ['--page-canvas', '--page-body', '--page-muted', '--page-label', '--ink-faint',
      '--bg-page', '--bg-card', '--text-primary', '--text-body', '--text-muted', '--text-label',
      '--border-strong', '--border-soft', '--border-faint', '--accent-hex', '--mountain-paper', '--mountain-ink']) {
      expect(isAlias(name), `${name} should be var(--…) of the set, is ${light.get(name)}`).toBe(true);
      expect(dark.has(name), `${name} is an alias; a dark value would fork it`).toBe(false);
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
    // LoginPage's themed root is owned by its shared account card.
    'components/AccountCard.tsx',
    // Password reset and every other email-action screen share AuthActionCard.
    'components/AuthActionCard.tsx',
    'components/AccreditationPage.tsx',
    'components/CutContentPage.tsx',
    'components/WipTools.tsx',
    'components/YearPlansView.tsx',
  ];
  for (const file of needsCompat) {
    it(`${file} carries theme-compat`, () => {
      expect(readFileSync(resolve_(ROOT, file), 'utf8')).toContain('theme-compat');
    });
  }

  it('no screen opts out of the theme with a hard-coded light override', () => {
    // LoginPage and ResetPasswordPage used `data-theme="light"` + colorScheme,
    // which set the surface but not the text, leaving near-white type on white.
    for (const file of needsCompat) {
      const src = readFileSync(resolve_(ROOT, file), 'utf8');
      expect(src, `${file} still forces light`).not.toContain('data-theme="light"');
      expect(src, `${file} still forces light`).not.toContain("colorScheme: 'light'");
    }
  });
});


/**
 * index.html used to carry a SECOND token system (--bg-*, --text-*, --border-*)
 * with its own dark values, which is how --text-label once sat at 3.37:1. It
 * now lives in index.css as aliases of the set (asserted above); index.html
 * must not grow its own colour tokens again.
 */
describe('index.html carries no colour tokens', () => {
  it('defines no --bg-*, --text-*, --border-*, --accent* or --success* of its own', () => {
    const own = [...html.matchAll(/^\s*(--(?:bg|text|border|accent|success)[a-z0-9-]*)\s*:/gm)].map(m => m[1]);
    expect(own, `colour tokens in index.html: ${own.join(', ')}`).toEqual([]);
  });
});


/**
 * Ink on the brand accent.
 *
 * White on #F26B1F is 3.04:1 and cream 2.88:1 — both fail AA, and in BOTH
 * themes, so this is not a dark-mode concern. --ink-on-accent is the token for
 * it and is deliberately the one value shared across themes, because the accent
 * itself does not change.
 */
describe('ink on the accent', () => {
  const ACCENT = '#F26B1F';
  const srgb = (hex: string) => [1, 3, 5].map(i => {
    const v = parseInt(hex.slice(i, i + 2), 16) / 255;
    return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
  });
  const lum = (hex: string) => { const [r, g, b] = srgb(hex); return 0.2126 * r + 0.7152 * g + 0.0722 * b; };
  const ratio = (a: string, b: string) => {
    const [l1, l2] = [lum(a), lum(b)].sort((x, y) => y - x);
    return (l1 + 0.05) / (l2 + 0.05);
  };

  it('is defined and clears AA on the accent', () => {
    const ink = light.get('--ink-on-accent');
    expect(ink).toBeDefined();
    const r = ratio(ink!, ACCENT);
    expect(r, `--ink-on-accent is ${r.toFixed(2)}:1 on ${ACCENT}`).toBeGreaterThanOrEqual(4.5);
  });

  it('white would not have cleared it — the reason this rule exists', () => {
    expect(ratio('#FFFFFF', ACCENT)).toBeLessThan(4.5);
  });

  it('is applied to every way the accent surface is expressed', () => {
    // Miss one of these and a whole family of buttons keeps its white ink; the
    // bg-[var(--accent-hex)] form is how the study-session Start pill slipped
    // through the first attempt.
    for (const form of [
      'bg-[#F26B1F]',
      'bg-[var(--accent-hex)]',
      'bg-[var(--accent-dark-hex)]',
      'background-color: rgb(242, 107, 31)',
      'background: rgb(242, 107, 31)',
    ]) {
      expect(css, `accent surface form not covered: ${form}`).toContain(form);
    }
  });

  it('overrides inline ink, which a plain rule cannot', () => {
    const block = css.slice(css.indexOf('Ink on the accent'));
    expect(block).toContain('color: var(--ink-on-accent) !important;');
    // Anchored: a bare [style*="color: …"] also matches `background-color: …`,
    // which recoloured children of any element with a white BACKGROUND.
    expect(block).toContain('[style^="color: white"]');
    expect(block).toContain('[style*="; color: white"]');
  });

  it('never matches an inline colour with an unanchored substring', () => {
    // `[style*="color: X"]` matches `background-color: X` too. Every inline
    // colour matcher must anchor with ^= or a leading "; ".
    const withoutComments = css.replace(/\/\*[\s\S]*?\*\//g, '');
    const unanchored = [...withoutComments.matchAll(/\[style\*="color: [^"]*"\]/g)].map((m) => m[0]);
    expect(unanchored, `unanchored inline colour matchers: ${unanchored.join(', ')}`).toEqual([]);
  });
});
