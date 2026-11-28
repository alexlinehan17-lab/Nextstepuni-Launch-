/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The frame owns the edges of the glass (components/ui/frame.css).
 *
 * The design audit of 24 Nov 2026 found 29 live faults where a control sat
 * under the Dynamic Island or in the home indicator, all from one cause: every
 * screen positioned against the raw edge of the screen and had to remember the
 * inset itself. The fix is a small set of layout primitives with the inset
 * maths built in. This guard keeps it that way: it fails when a NEW
 *
 *   `fixed` (Tailwind) / `position: fixed`   `inset-0`   `100vh`   `h-screen`
 *   `env(safe-area-`   a raw `var(--sat|--sab|--sal|--sar)` read
 *
 * appears anywhere outside the primitives' own files. About a hundred files did
 * this before the frame existed, so it is a ratchet: test/fixtures/
 * frameEdgesBaseline.json records how many each file had, and a file may only
 * go down. To record a file going down, run
 *
 *   FRAME_EDGES_UPDATE=1 npx vitest run test/frameEdges.guard.test.ts
 *
 * which lowers the baseline and never raises it.
 */
import { existsSync, readFileSync, readdirSync, statSync, writeFileSync } from 'node:fs';
import { join, relative, sep } from 'node:path';
import { describe, expect, it } from 'vitest';

const ROOT = process.cwd();
const BASELINE_FILE = join(ROOT, 'test/fixtures/frameEdgesBaseline.json');

/** The primitives may touch the edge; nothing else may. */
const PRIMITIVE_FILES = new Set(['components/ui/frame.css', 'components/ui/Frame.tsx', 'index.html']);
const SCAN_DIRS = ['components', 'hooks', 'contexts', 'utils', 'services', 'design'];
const SKIP_DIRS = new Set(['node_modules', 'dist', 'capture-harness']);
const SOURCE = /\.(tsx?|css)$/;

type Rule = 'fixed' | 'inset-0' | '100vh' | 'h-screen' | 'env(safe-area-' | 'var(--sa*)';
type Counts = Partial<Record<Rule, number>>;

const INSTEAD: Record<Rule, string> = {
  fixed: 'frame-top (a pinned page bar), frame-takeover, frame-dialog, frame-sheet-backdrop or frame-float',
  'inset-0': 'frame-takeover / frame-dialog for a layer; frame-safe-box for controls pinned inside one',
  '100vh': '100dvh, or calc(var(--safe-h) - margin) for a card',
  'h-screen': 'h-[100dvh] or min-h-[100dvh]',
  'env(safe-area-': 'var(--safe-top) / --safe-bottom / --safe-left / --safe-right, or --edge-top / --edge-bottom',
  'var(--sa*)': 'var(--safe-top) / --safe-bottom / --safe-left / --safe-right, or --edge-top / --edge-bottom',
};

/** A token of a Tailwind class list ("md:fixed", "z-[200]", "-translate-x-1/2"). */
const CLASS_TOKEN = /^!?(?:[a-z0-9-]+:)*-?[a-z0-9][a-z0-9\-[\]/.%#(),_=&>*@+:]*$/;

/** True when the `fixed` at `at` sits inside a quoted class list on its line,
 *  not in prose ("a fixed date") or exam text. */
function inClassList(line: string, at: number, length: number): boolean {
  const before = line.slice(0, at);
  const open = Math.max(before.lastIndexOf('"'), before.lastIndexOf("'"), before.lastIndexOf('`'));
  if (open < 0) return false;
  const close = line.indexOf(before[open], at + length);
  if (close < 0) return false;
  const tokens = line.slice(open + 1, close).replace(/\$\{[^}]*\}/g, ' ').trim().split(/\s+/);
  return tokens.length > 1 && tokens.every(token => CLASS_TOKEN.test(token)) && tokens.some(token => /[-:[]/.test(token));
}

function stripComments(source: string, css: boolean): string {
  let out = source.replace(/\/\*[\s\S]*?\*\//g, ' ');
  if (!css) out = out.replace(/(^|[^:\\'"`])\/\/[^\n]*/g, '$1');
  return out;
}

function countEdges(source: string, kind: 'css' | 'ts' | 'tsx'): Counts {
  const css = kind === 'css';
  const text = stripComments(source, css);
  const counts: Counts = {};
  const add = (rule: Rule, n: number) => { if (n) counts[rule] = (counts[rule] ?? 0) + n; };
  add('100vh', (text.match(/\b100vh\b/g) ?? []).length);
  add('env(safe-area-', (text.match(/env\(\s*safe-area-/g) ?? []).length);
  add('var(--sa*)', (text.match(/var\(\s*--sa[tblr]\b/g) ?? []).length);
  add('fixed', (text.match(/position\s*:\s*['"`]?fixed\b/g) ?? []).length);
  if (!css) {
    add('inset-0', (text.match(/(?<![\w-])!?inset-0(?![\w.\-[])/g) ?? []).length);
    add('h-screen', (text.match(/(?<![\w-])(?:min-|max-)?h-screen(?![\w-])/g) ?? []).length);
    if (kind === 'tsx') {
      for (const line of text.split('\n')) {
        for (const match of line.matchAll(/(?<=^|[\s"'`{])(?:[a-z0-9]+:)*!?fixed(?=$|[\s"'`}])/g)) {
          if (inClassList(line, match.index ?? 0, match[0].length)) add('fixed', 1);
        }
      }
    }
  }
  return counts;
}

function walk(dir: string, files: string[]) {
  for (const name of readdirSync(dir)) {
    if (SKIP_DIRS.has(name) || name.startsWith('.')) continue;
    const path = join(dir, name);
    if (statSync(path).isDirectory()) walk(path, files);
    else if (SOURCE.test(name)) files.push(path);
  }
}

function scan(): Record<string, Counts> {
  const files: string[] = [];
  for (const dir of SCAN_DIRS) walk(join(ROOT, dir), files);
  for (const name of readdirSync(ROOT)) {
    if (SOURCE.test(name) && !/\.config\.ts$|\.d\.ts$/.test(name)) files.push(join(ROOT, name));
  }
  const result: Record<string, Counts> = {};
  for (const file of files) {
    const path = relative(ROOT, file).split(sep).join('/');
    if (PRIMITIVE_FILES.has(path)) continue;
    const counts = countEdges(readFileSync(file, 'utf8'), path.endsWith('.css') ? 'css' : path.endsWith('.tsx') ? 'tsx' : 'ts');
    if (Object.keys(counts).length) result[path] = counts;
  }
  return result;
}

function readBaseline(current: Record<string, Counts>): Record<string, Counts> {
  // First run only: the baseline is today's places, written once by hand-run update.
  if (!existsSync(BASELINE_FILE) && process.env.FRAME_EDGES_UPDATE === '1') return current;
  return (JSON.parse(readFileSync(BASELINE_FILE, 'utf8')) as { files: Record<string, Counts> }).files;
}

function sortCounts(files: Record<string, Counts>): Record<string, Counts> {
  return Object.fromEntries(Object.keys(files).sort().map(path => [path,
    Object.fromEntries(Object.entries(files[path]).sort(([a], [b]) => a.localeCompare(b)))]));
}

describe('the frame owns the edges', () => {
  it('finds each kind of edge-touching code it is meant to catch', () => {
    expect(countEdges('<div className="fixed inset-0 z-50 h-screen" />', 'tsx')).toEqual({ fixed: 1, 'inset-0': 1, 'h-screen': 1 });
    expect(countEdges('<p className="mt-2 text-sm">The date is fixed, on top of the page.</p>', 'tsx')).toEqual({});
    expect(countEdges("style={{ position: 'fixed', top: 'var(--sat, 0px)' }}", 'tsx')).toEqual({ fixed: 1, 'var(--sa*)': 1 });
    expect(countEdges('.x { position: fixed; padding-top: max(16px, env(safe-area-inset-top)); height: 100vh; }', 'css'))
      .toEqual({ fixed: 1, 'env(safe-area-': 1, '100vh': 1 });
    expect(countEdges('/* position: fixed; 100vh */ .x { top: 0 }', 'css')).toEqual({});
  });

  it('keeps the primitives in one place', () => {
    for (const file of PRIMITIVE_FILES) expect(statSync(join(ROOT, file)).isFile(), file).toBe(true);
    expect(readFileSync(join(ROOT, 'index.css'), 'utf8'), 'index.css must import the frame before Tailwind')
      .toMatch(/^@import "\.\/design\/quiet-focus\.css";\n@import "\.\/components\/ui\/frame\.css";/);
  });

  it('lets no file touch the edge of the screen more than it did before the frame', () => {
    const current = scan();
    const baseline = readBaseline(current);
    const grew: string[] = [];
    for (const [path, counts] of Object.entries(current)) {
      for (const [rule, n] of Object.entries(counts) as [Rule, number][]) {
        const allowed = baseline[path]?.[rule] ?? 0;
        if (n > allowed) grew.push(`  ${path}: ${n} × \`${rule}\` (allowed ${allowed}). Use ${INSTEAD[rule]}.`);
      }
    }
    if (process.env.FRAME_EDGES_UPDATE === '1' && !grew.length) {
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
        about: 'Ratchet for test/frameEdges.guard.test.ts: how often each file touches the edge of the screen outside the frame primitives (components/ui/frame.css). Counts may only go down.',
        files: sortCounts(lowered),
      }, null, 1)}\n`);
    }
    expect(grew, [
      'Nothing in a screen may touch the edge of the glass: the status bar, Dynamic Island and home',
      'indicator belong to the frame. Build the layer from the primitives in components/ui/frame.css',
      '(frame-bar, frame-page, frame-foot, frame-takeover + frame-safe-box, frame-dialog + frame-dialog-card,',
      'frame-sheet-backdrop + frame-sheet, frame-float) and its variables (--safe-*, --edge-*, --z-*).',
      'New edge-touching code:',
      ...grew,
    ].join('\n')).toEqual([]);
  });
});
