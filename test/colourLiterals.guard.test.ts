/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * One set of values: every colour comes from the token home.
 *
 * The design audit of 24 Nov 2026 found 111 different oranges, 55 dark greys
 * used as surfaces and 14 page backgrounds, each one a decision made again by
 * hand in a component. The values now live in one place: the `:root` and
 * `.dark` blocks at the top of index.css (exposed to Tailwind in
 * tailwind.config.ts and to TypeScript in design/tokens.ts). This guard fails
 * when a NEW typed colour appears anywhere else:
 *
 *   a hex (`#eb692a`)   `rgb(` / `rgba(` with numbers   `hsl(` / `hsla(`
 *   a Tailwind arbitrary colour (`bg-[#…]`)   a raw `bg-zinc-9xx` / `bg-neutral-9xx` surface
 *
 * Thousands of these predate the token home, so it is a ratchet:
 * test/fixtures/colourLiteralsBaseline.json records how many each file had,
 * and a file may only go down. To record a file going down, run
 *
 *   COLOUR_LITERALS_UPDATE=1 npx vitest run test/colourLiterals.guard.test.ts
 *
 * which lowers the baseline and never raises it.
 */
import { existsSync, readFileSync, readdirSync, statSync, writeFileSync } from 'node:fs';
import { join, relative, sep } from 'node:path';
import { describe, expect, it } from 'vitest';

const ROOT = process.cwd();
const BASELINE_FILE = join(ROOT, 'test/fixtures/colourLiteralsBaseline.json');

/** Files that ARE the token home, or a named palette the system keeps on purpose. */
const HOME_FILES = new Set([
  'design/tokens.ts', // the TypeScript mirror of the CSS tokens (COLORS, accentRgba)
  'utils/subjectColors.ts', // the ten subject colours (tokens.md, "Orange, green, red")
]);
/** In these stylesheets only the leading token blocks are the home; the rest is counted. */
const HOME_BLOCKS: Record<string, RegExp> = {
  'index.css': /^(?::root|\.dark)\s*\{[\s\S]*?\n\}/gm,
  'design/quiet-focus.css': /^(?::root|\.dark)\s*\{[\s\S]*?\n\}/gm,
};
const SCAN_DIRS = ['components', 'hooks', 'contexts', 'utils', 'services', 'design'];
const SKIP_DIRS = new Set(['node_modules', 'dist', 'capture-harness', 'landing']);
const SOURCE = /\.(tsx?|css)$/;

type Rule = 'hex' | 'rgb(' | 'hsl(' | 'tailwind [#…]' | 'zinc/neutral-9xx surface';
type Counts = Partial<Record<Rule, number>>;

const INSTEAD: Record<Rule, string> = {
  hex: 'a token: var(--surface-canvas | --surface-paper | --surface-soft | --surface-raised), var(--ink-primary | --ink-secondary | --ink-muted), var(--hairline | --outline-soft | --outline-strong), var(--nsu-orange) or var(--accent-text); in TypeScript COLORS.accent from design/tokens',
  'rgb(': 'a token; for the orange with an alpha, rgba(var(--nsu-orange-rgb), 0.2) in CSS or accentRgba(0.2) from design/tokens',
  'hsl(': 'a token from the :root block of index.css',
  'tailwind [#…]': 'a Tailwind token class: bg-surface-paper, text-ink-muted, border-hairline, border-outline-soft, bg-accent, text-accent-text',
  'zinc/neutral-9xx surface': 'bg-surface-canvas (the page) or bg-surface-paper (a box): the token already changes with the theme, so no dark: class is needed',
};

/** Token values, for a "nearest token" hint in the failure message. */
const NEAREST: Record<string, string> = {
  '#ffffff': '--surface-canvas / --surface-paper', '#f5f5f5': '--surface-soft', '#181818': '--surface-canvas (dark)',
  '#242424': '--surface-paper (dark)', '#101010': '--surface-soft (dark)', '#2c2c2c': '--surface-raised (dark)',
  '#171717': '--ink-primary', '#575757': '--ink-secondary', '#6b6b6b': '--ink-muted', '#e5e5e5': '--hairline',
  '#d6d6d6': '--outline-soft', '#383838': '--outline-strong', '#eb692a': '--nsu-orange', '#b84a0c': '--accent-text',
  '#3a8d5f': '--success-hex', '#8e2c2c': '--danger-tint-ink',
};
function nearest(hex: string): string {
  const rgb = (h: string) => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16));
  const full = hex.length === 4 ? `#${[...hex.slice(1)].map(c => c + c).join('')}` : hex.slice(0, 7);
  if (!/^#[0-9a-f]{6}$/i.test(full)) return 'a token';
  const [r, g, b] = rgb(full.toLowerCase());
  let best = 'a token'; let bestD = Infinity;
  for (const [value, name] of Object.entries(NEAREST)) {
    const [R, G, B] = rgb(value);
    const d = (r - R) ** 2 + (g - G) ** 2 + (b - B) ** 2;
    if (d < bestD) { bestD = d; best = name; }
  }
  return bestD < 40 ** 2 ? `var(${best.split(' ')[0]})${best.includes('(dark)') ? ' (its dark value)' : ''}` : 'a token';
}

function stripComments(source: string, css: boolean): string {
  let out = source.replace(/\/\*[\s\S]*?\*\//g, ' ');
  if (!css) out = out.replace(/(^|[^:\\'"`])\/\/[^\n]*/g, '$1');
  return out;
}

const HEX = /(?<=[\s'"`:(,=[>{|_])#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})(?![0-9a-zA-Z_-])/g;
const TW_HEX = /-\[#[0-9a-fA-F]{3,8}\]/g;
const RGB = /\brgba?\(\s*\d/g;
const HSL = /\bhsla?\(\s*\d/g;
const ZINC = /(?<![\w-])(?:[a-z0-9-]+:)*!?bg-(?:zinc|neutral)-9\d\d(?![\w-])/g;
/** `href="#top"`, `id="#a"`, url fragments: not colours. */
const NOT_COLOUR = /(?:href|to|url|id|htmlFor|xlinkHref|aria-[a-z]+)\s*[=:(]\s*[{('"`]*\s*$/;

export function countColours(source: string, kind: 'css' | 'ts' | 'tsx'): { counts: Counts; samples: string[] } {
  const css = kind === 'css';
  const text = stripComments(source, css);
  const counts: Counts = {};
  const samples: string[] = [];
  const add = (rule: Rule, n: number) => { if (n) counts[rule] = (counts[rule] ?? 0) + n; };
  for (const line of text.split('\n')) {
    const tw = [...line.matchAll(TW_HEX)];
    add('tailwind [#…]', tw.length);
    for (const m of line.matchAll(HEX)) {
      const at = m.index ?? 0;
      if (tw.some(t => (t.index ?? 0) < at && at < (t.index ?? 0) + t[0].length)) { samples.push(m[0]); continue; }
      if (NOT_COLOUR.test(line.slice(0, at))) continue;
      add('hex', 1); samples.push(m[0]);
    }
    add('rgb(', (line.match(RGB) ?? []).length);
    add('hsl(', (line.match(HSL) ?? []).length);
    if (!css) add('zinc/neutral-9xx surface', (line.match(ZINC) ?? []).length);
  }
  return { counts, samples };
}

function walk(dir: string, files: string[]) {
  for (const name of readdirSync(dir)) {
    if (SKIP_DIRS.has(name) || name.startsWith('.')) continue;
    const path = join(dir, name);
    if (statSync(path).isDirectory()) walk(path, files);
    else if (SOURCE.test(name) && !/\.d\.ts$|-runtime\.css$|\.test\.tsx?$/.test(name)) files.push(path);
  }
}

function scan(): { counts: Record<string, Counts>; samples: Record<string, string[]> } {
  const files: string[] = [];
  for (const dir of SCAN_DIRS) walk(join(ROOT, dir), files);
  for (const name of readdirSync(ROOT)) {
    if (SOURCE.test(name) && !/\.config\.ts$|\.d\.ts$|^landing-/.test(name)) files.push(join(ROOT, name));
  }
  const counts: Record<string, Counts> = {};
  const samples: Record<string, string[]> = {};
  for (const file of files) {
    const path = relative(ROOT, file).split(sep).join('/');
    if (HOME_FILES.has(path)) continue;
    let source = readFileSync(file, 'utf8');
    if (HOME_BLOCKS[path]) source = source.replace(HOME_BLOCKS[path], block => block.replace(/[^\n]/g, ' '));
    const found = countColours(source, path.endsWith('.css') ? 'css' : path.endsWith('.tsx') ? 'tsx' : 'ts');
    if (Object.keys(found.counts).length) { counts[path] = found.counts; samples[path] = found.samples; }
  }
  return { counts, samples };
}

function readBaseline(current: Record<string, Counts>): Record<string, Counts> {
  if (!existsSync(BASELINE_FILE) && process.env.COLOUR_LITERALS_UPDATE === '1') return current;
  return (JSON.parse(readFileSync(BASELINE_FILE, 'utf8')) as { files: Record<string, Counts> }).files;
}

function sortCounts(files: Record<string, Counts>): Record<string, Counts> {
  return Object.fromEntries(Object.keys(files).sort().map(path => [path,
    Object.fromEntries(Object.entries(files[path]).sort(([a], [b]) => a.localeCompare(b)))]));
}

describe('one set of values: colours come from the token home', () => {
  it('finds each kind of typed colour it is meant to catch', () => {
    expect(countColours('<div className="bg-[#F26B1F] text-white dark:bg-zinc-900" style={{ color: \'#eb692a\' }} />', 'tsx').counts)
      .toEqual({ 'tailwind [#…]': 1, hex: 1, 'zinc/neutral-9xx surface': 1 });
    expect(countColours(".x { color: rgba(0, 0, 0, .4); background: hsl(20 80% 50%); border-color: #ddd }", 'css').counts)
      .toEqual({ 'rgb(': 1, 'hsl(': 1, hex: 1 });
    // Tokens, alpha on a token, fragments and prose are not typed colours.
    expect(countColours(".x { color: var(--ink-muted); box-shadow: 0 0 0 3px rgba(var(--nsu-orange-rgb), .2) }", 'css').counts).toEqual({});
    expect(countColours('<a href="#top" className="bg-surface-paper text-ink-muted">Back to #1 in the list</a>', 'tsx').counts).toEqual({});
    expect(countColours('/* was #F26B1F */ .x { color: var(--nsu-orange) }', 'css').counts).toEqual({});
  });

  it('keeps the home in one place', () => {
    const css = readFileSync(join(ROOT, 'index.css'), 'utf8');
    expect(css, 'index.css :root must hold the one orange').toMatch(/^:root\s*\{[\s\S]*?--nsu-orange:\s*#eb692a;/m);
    expect(css, 'index.css .dark must hold the dark canvas').toMatch(/^\.dark\s*\{[\s\S]*?--surface-canvas:\s*#181818;/m);
    for (const file of HOME_FILES) expect(statSync(join(ROOT, file)).isFile(), file).toBe(true);
  });

  it('lets no file type more colours than it did when the token home was made', () => {
    const { counts: current, samples } = scan();
    const baseline = readBaseline(current);
    const grew: string[] = [];
    for (const [path, counts] of Object.entries(current)) {
      for (const [rule, n] of Object.entries(counts) as [Rule, number][]) {
        const allowed = baseline[path]?.[rule] ?? 0;
        if (n > allowed) {
          const hints = rule === 'hex' || rule === 'tailwind [#…]'
            ? ` Seen: ${[...new Set(samples[path] ?? [])].slice(-4).map(h => `${h} → ${nearest(h)}`).join(', ')}.`
            : '';
          grew.push(`  ${path}: ${n} × ${rule} (allowed ${allowed}). Use ${INSTEAD[rule]}.${hints}`);
        }
      }
    }
    if (process.env.COLOUR_LITERALS_UPDATE === '1' && !grew.length) {
      const lowered: Record<string, Counts> = {};
      for (const [path, counts] of Object.entries(baseline)) {
        const now: Counts = {};
        for (const [rule, n] of Object.entries(counts) as [Rule, number][]) {
          const kept = Math.min(n, current[path]?.[rule] ?? 0);
          if (kept) now[rule] = kept;
        }
        if (Object.keys(now).length) lowered[path] = now;
      }
      writeFileSync(BASELINE_FILE, `${JSON.stringify({
        about: 'Ratchet for test/colourLiterals.guard.test.ts: how many typed colours each file has outside the token home (the :root and .dark blocks of index.css). Counts may only go down.',
        files: sortCounts(lowered),
      }, null, 1)}\n`);
    }
    expect(grew, [
      'Colours come from one place: the :root and .dark blocks at the top of index.css (Tailwind: tailwind.config.ts;',
      'TypeScript: COLORS in design/tokens.ts). The page is --surface-canvas, a box is --surface-paper, a well is',
      '--surface-soft, a menu or sheet is --surface-raised; text is --ink-primary / --ink-secondary / --ink-muted;',
      'lines are --hairline / --outline-soft / --outline-strong; the one orange is --nsu-orange (as text: --accent-text).',
      'New typed colours:',
      ...grew,
    ].join('\n')).toEqual([]);
  });
});
