/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * One of each: buttons, pop-ups and dropdowns come from the shared parts.
 *
 * The design audit of 24 Nov 2026 counted 41 kinds of button (1,225 hand-styled
 * `<button>`s against about 300 on a shared component), 17 pop-up
 * implementations and 9 kinds of dropdown, each made again by hand on a
 * screen. Stage 2 built one of each in components/ui/ (Button.tsx, Choice.tsx,
 * Menu.tsx, Sheet.tsx, Message.tsx, Bars.tsx, Field.tsx, List.tsx, States.tsx).
 * This guard fails when a NEW hand-made one appears in screen code:
 *
 *   button     `<button`  `<motion.button` / `MotionButton`  `role="button"`
 *   pop-up     `role="dialog"` / `role="alertdialog"`  `<dialog`  `createPortal(`
 *   dropdown   `<select`  `role="listbox"` / `role="menu"`  `aria-haspopup`
 *
 * components/ui/ is the parts' own home and is not scanned. Today's places are
 * a ratchet: test/fixtures/sharedPartsBaseline.json records how many each file
 * has, and a file may only go down as screens move onto the parts. To record a
 * file going down, run
 *
 *   SHARED_PARTS_UPDATE=1 npx vitest run test/sharedParts.guard.test.ts
 *
 * which lowers the baseline and never raises it.
 */
import { existsSync, readFileSync, readdirSync, statSync, writeFileSync } from 'node:fs';
import { join, relative, sep } from 'node:path';
import { describe, expect, it } from 'vitest';

const ROOT = process.cwd();
const BASELINE_FILE = join(ROOT, 'test/fixtures/sharedPartsBaseline.json');

const SCAN_DIRS = ['components', 'hooks', 'contexts', 'utils', 'services', 'design'];
/** The parts' own home, the separate landing document, and build output. */
const SKIP_DIRS = new Set(['node_modules', 'dist', 'capture-harness', 'landing']);
const SKIP_PATHS = ['components/ui/'];
const SOURCE = /\.tsx?$/;

type Rule = 'button' | 'pop-up' | 'dropdown';
type Counts = Partial<Record<Rule, number>>;

const INSTEAD: Record<Rule, string> = {
  button: 'Button, TextButton or IconButton from components/ui/Button (a choice: ChoiceGroup, ChoiceTile, Switch or SelectionBar from components/ui/Choice; a row that opens something: Row from components/ui/List; a box you press: PressBox)',
  'pop-up': 'Sheet or Confirm from components/ui/Sheet (a message: showMessage from components/ui/Message)',
  dropdown: 'Menu from components/ui/Menu (more than about seven options, or options that need explaining: a Sheet of ChoiceTiles)',
};

const PATTERNS: Record<Rule, RegExp[]> = {
  button: [/<button\b/g, /<motion\.button\b/g, /<MotionButton\b/g, /\brole\s*=\s*\{?\s*["'`]button["'`]/g],
  'pop-up': [/\brole\s*=\s*\{?\s*["'`](?:alert)?dialog["'`]/g, /<dialog\b/g, /\bcreatePortal\s*\(/g],
  dropdown: [/<select\b/g, /\brole\s*=\s*\{?\s*["'`](?:listbox|menu)["'`]/g, /\baria-haspopup\b/g],
};

function stripComments(source: string): string {
  return source.replace(/\/\*[\s\S]*?\*\//g, ' ').replace(/(^|[^:\\'"`])\/\/[^\n]*/g, '$1');
}

export function countHandMade(source: string): Counts {
  const text = stripComments(source);
  const counts: Counts = {};
  for (const [rule, patterns] of Object.entries(PATTERNS) as [Rule, RegExp[]][]) {
    const n = patterns.reduce((sum, pattern) => sum + (text.match(pattern) ?? []).length, 0);
    if (n) counts[rule] = n;
  }
  return counts;
}

function walk(dir: string, files: string[]) {
  for (const name of readdirSync(dir)) {
    if (SKIP_DIRS.has(name) || name.startsWith('.')) continue;
    const path = join(dir, name);
    if (statSync(path).isDirectory()) walk(path, files);
    else if (SOURCE.test(name) && !/\.d\.ts$|\.test\.tsx?$/.test(name)) files.push(path);
  }
}

function scan(): Record<string, Counts> {
  const files: string[] = [];
  for (const dir of SCAN_DIRS) walk(join(ROOT, dir), files);
  for (const name of readdirSync(ROOT)) {
    if (SOURCE.test(name) && !/\.config\.ts$|\.d\.ts$|^landing-/.test(name)) files.push(join(ROOT, name));
  }
  const result: Record<string, Counts> = {};
  for (const file of files) {
    const path = relative(ROOT, file).split(sep).join('/');
    if (SKIP_PATHS.some(prefix => path.startsWith(prefix))) continue;
    const counts = countHandMade(readFileSync(file, 'utf8'));
    if (Object.keys(counts).length) result[path] = counts;
  }
  return result;
}

function sortCounts(files: Record<string, Counts>): Record<string, Counts> {
  return Object.fromEntries(Object.keys(files).sort().map(path => [path,
    Object.fromEntries(Object.entries(files[path]).sort(([a], [b]) => a.localeCompare(b)))]));
}

describe('one of each: buttons, pop-ups and dropdowns come from the shared parts', () => {
  it('finds each kind of hand-made control it is meant to catch, and nothing in comments', () => {
    expect(countHandMade('<button type="button" className="px-3">Go</button>')).toEqual({ button: 1 });
    expect(countHandMade('<MotionButton whileTap={{ scale: 0.98 }} /><motion.button /><div role="button" tabIndex={0} />')).toEqual({ button: 3 });
    expect(countHandMade('<div role="dialog" aria-modal="true">{createPortal(x, document.body)}</div><dialog open />')).toEqual({ 'pop-up': 3 });
    expect(countHandMade('<div role="alertdialog" />')).toEqual({ 'pop-up': 1 });
    expect(countHandMade('<select value={v}><option /></select><button aria-haspopup="listbox" /><ul role="listbox" /><div role="menu" />'))
      .toEqual({ dropdown: 4, button: 1 });
    expect(countHandMade('<Button kind="main">Go</Button><Sheet open /><Menu label="x" />')).toEqual({});
    expect(countHandMade('/* a <button> in a comment */ // <select> here too\nconst x = 1;')).toEqual({});
  });

  it('has a baseline to hold the line against', () => {
    expect(existsSync(BASELINE_FILE) || process.env.SHARED_PARTS_UPDATE === '1', 'test/fixtures/sharedPartsBaseline.json is missing').toBe(true);
  });

  it('lets no file hand-make more buttons, pop-ups or dropdowns than it did when the shared parts arrived', () => {
    const current = scan();
    const baseline: Record<string, Counts> = existsSync(BASELINE_FILE)
      ? (JSON.parse(readFileSync(BASELINE_FILE, 'utf8')) as { files: Record<string, Counts> }).files
      : current; // first run only, with SHARED_PARTS_UPDATE=1
    const grew: string[] = [];
    for (const [path, counts] of Object.entries(current)) {
      for (const [rule, n] of Object.entries(counts) as [Rule, number][]) {
        const allowed = baseline[path]?.[rule] ?? 0;
        if (n > allowed) grew.push(`  ${path}: ${n} hand-made ${rule}${n === 1 ? '' : 's'} (allowed ${allowed}). Use ${INSTEAD[rule]}.`);
      }
    }
    if (process.env.SHARED_PARTS_UPDATE === '1' && !grew.length) {
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
        about: 'Ratchet for test/sharedParts.guard.test.ts: how many hand-made buttons, pop-ups and dropdowns each file has outside the shared parts (components/ui/). Counts may only go down.',
        files: sortCounts(lowered),
      }, null, 1)}\n`);
    }
    expect(grew, [
      'Buttons, pop-ups and dropdowns come from the shared parts in components/ui/ (one of each:',
      'the design audit of 24 Nov 2026 found 41 kinds of button, 17 pop-ups and 9 dropdowns, each made by hand).',
      'New hand-made controls:',
      ...grew,
    ].join('\n')).toEqual([]);
  });
});
