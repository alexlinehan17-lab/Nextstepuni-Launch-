/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Static guards over two Firestore write mistakes that fail SILENTLY, which is
 * why both survived in production for months:
 *
 *  1. A dotted key inside a `setDoc` payload. `setDoc` treats the whole string
 *     as ONE field-name segment, so `{'pointsData.totalEarned': increment(5)}`
 *     creates a root field literally named "pointsData.totalEarned" and the
 *     real total never moves. (Dotted paths are `updateDoc`-only syntax.) Every
 *     point a student earned by ticking a timetable block was lost this way.
 *
 *  2. `undefined` in a payload. The SDK throws unless
 *     `ignoreUndefinedProperties` is set — which this project deliberately does
 *     NOT set, because doing so would silently drop fields everywhere else. A
 *     JC or LCA student's subject edit emitted `currentGrade: undefined` and so
 *     threw before writing anything, surfacing as "check your connection".
 *
 * These are cheap source scans, not runtime tests — the point is that they fail
 * the moment someone reintroduces the pattern anywhere in the app.
 */
import { describe, it, expect } from 'vitest';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join, resolve } from 'node:path';

const ROOT = resolve(__dirname, '..');
const SCAN_DIRS = ['components', 'hooks', 'contexts', 'utils'];

function sourceFiles(dir: string): string[] {
  const out: string[] = [];
  const walk = (d: string) => {
    for (const entry of readdirSync(d)) {
      if (entry === 'node_modules' || entry.startsWith('.')) continue;
      const full = join(d, entry);
      if (statSync(full).isDirectory()) walk(full);
      else if (/\.tsx?$/.test(entry)) out.push(full);
    }
  };
  walk(join(ROOT, dir));
  return out;
}

const FILES = SCAN_DIRS.flatMap(sourceFiles).concat([join(ROOT, 'App.tsx')]);

describe('no dotted field paths inside setDoc payloads', () => {
  it('finds none anywhere in the app source', () => {
    // Matches an object-literal key containing a dot, quoted either way:
    //   'a.b': …   or   "a.b": …
    const DOTTED_KEY = /(['"])([A-Za-z_$][\w$]*(?:\.[A-Za-z_$][\w$]*)+)\1\s*:/g;
    const offenders: string[] = [];

    for (const file of FILES) {
      const src = readFileSync(file, 'utf8');
      if (!src.includes('setDoc(')) continue;

      // Scan the ARGUMENT LIST of each setDoc(...) call — bounded by balanced
      // parentheses, not a fixed window. A fixed window swept up neighbouring
      // updateDoc calls, where dotted paths are the correct syntax.
      let idx = src.indexOf('setDoc(');
      while (idx !== -1) {
        const open = idx + 'setDoc('.length;
        let depth = 1;
        let end = open;
        while (end < src.length && depth > 0) {
          const ch = src[end];
          if (ch === '(') depth++;
          else if (ch === ')') depth--;
          end++;
        }
        const region = src.slice(open, end);
        for (const m of region.matchAll(DOTTED_KEY)) {
          // Ignore file paths and anything that isn't plausibly a field name.
          if (/\.(ts|tsx|js|json|css|png|svg)$/.test(m[2])) continue;
          offenders.push(`${file.replace(ROOT + '/', '')}: '${m[2]}'`);
        }
        idx = src.indexOf('setDoc(', idx + 1);
      }
    }

    expect(offenders, `Dotted keys in a setDoc payload create a literal root field with that name.\nUse a nested object instead: { pointsData: { totalEarned: increment(5) } }\nOffenders:\n${offenders.join('\n')}`).toEqual([]);
  });
});

describe('subject-profile payloads never contain undefined', () => {
  // Mirrors the branch ChangeSubjectsModal / SubjectOnboarding now use. If
  // someone reverts to unconditional `currentGrade: config.currentGrade`, the
  // JC and LCA cases below start producing undefined and this fails.
  const buildSubjects = (
    names: string[],
    opts: { isJunior?: boolean; isLca?: boolean; configs?: Record<string, any> } = {},
  ) => names.map(name => {
    if (opts.isJunior) return { subjectName: name, level: 'common', currentBand: 'Merit', targetBand: 'Higher Merit' };
    if (opts.isLca) return { subjectName: name, level: 'common' };
    const config = opts.configs?.[name] || { level: 'higher', currentGrade: 'H4', targetGrade: 'H2' };
    return {
      subjectName: name,
      level: config.level,
      ...(config.currentGrade ? { currentGrade: config.currentGrade } : {}),
      ...(config.targetGrade ? { targetGrade: config.targetGrade } : {}),
    };
  });

  const hasUndefined = (v: unknown): boolean => {
    if (v === undefined) return true;
    if (Array.isArray(v)) return v.some(hasUndefined);
    if (v && typeof v === 'object') return Object.values(v).some(hasUndefined);
    return false;
  };

  it('Junior Cycle subjects carry bands and no undefined grade', () => {
    const subjects = buildSubjects(['Science', 'Business Studies'], { isJunior: true });
    expect(hasUndefined(subjects)).toBe(false);
    expect(subjects[0]).not.toHaveProperty('currentGrade');
    expect(subjects[0]).toHaveProperty('currentBand');
  });

  it('LCA subjects carry level only and no undefined grade', () => {
    const subjects = buildSubjects(['Hair And Beauty'], { isLca: true });
    expect(hasUndefined(subjects)).toBe(false);
    expect(subjects[0]).not.toHaveProperty('currentGrade');
  });

  it('Leaving Cert subjects keep their grades', () => {
    const subjects = buildSubjects(['Mathematics'], {});
    expect(hasUndefined(subjects)).toBe(false);
    expect(subjects[0]).toMatchObject({ currentGrade: 'H4', targetGrade: 'H2' });
  });

  it('a partially-configured LC subject omits the missing field rather than writing undefined', () => {
    const subjects = buildSubjects(['Art'], { configs: { Art: { level: 'ordinary', currentGrade: 'O3' } } });
    expect(hasUndefined(subjects)).toBe(false);
    expect(subjects[0]).not.toHaveProperty('targetGrade');
  });
});
