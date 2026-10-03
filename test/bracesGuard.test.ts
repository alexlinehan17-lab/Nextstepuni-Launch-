import { createRequire } from 'node:module';
import { describe, expect, it } from 'vitest';

const require = createRequire(import.meta.url);
const guarded = require('../vendor/braces-guarded');
const malicious = '{'.repeat(4000) + 'x' + '}'.repeat(4000);

describe('bounded build-tool brace expansion', () => {
  it.each(['parse', 'compile', 'expand', 'stringify'])('rejects deep patterns before %s can exhaust the stack', method => {
    expect(() => guarded[method](malicious)).toThrow(SyntaxError);
    expect(() => guarded[method](malicious)).toThrow(/nesting exceeds the safe limit/);
  });
  it('also bounds the main entry point and parenthesis blocks', () => {
    expect(() => guarded(malicious)).toThrow(SyntaxError);
    expect(() => guarded('('.repeat(4000) + 'x' + ')'.repeat(4000))).toThrow(SyntaxError);
    expect(() => guarded(malicious, { maxDepth: Infinity, maxLength: Infinity })).toThrow(SyntaxError);
  });
  it.each(['compile', 'expand', 'stringify'])('bounds direct and cyclic ASTs passed to %s', method => {
    const ast: { type: string; nodes: unknown[] } = { type: 'root', nodes: [] };
    let parent = ast;
    for (let index = 0; index < 100; index++) {
      const child = { type: 'brace', nodes: [] };
      parent.nodes.push(child); parent = child;
    }
    expect(() => guarded[method](ast)).toThrow(SyntaxError);
    const cycle: { type: string; nodes: unknown[] } = { type: 'root', nodes: [] };
    cycle.nodes.push(cycle);
    expect(() => guarded[method](cycle)).toThrow(SyntaxError);
  });
  it('retains normal glob, nested alternatives, ranges and escape behavior', () => {
    expect(guarded.expand('src/**/*.{ts,tsx}')).toEqual(['src/**/*.ts', 'src/**/*.tsx']);
    expect(guarded.expand('a/{b,{c,d}}/e')).toEqual(['a/b/e', 'a/c/e', 'a/d/e']);
    expect(guarded.expand('item-{01..03}')).toEqual(['item-01', 'item-02', 'item-03']);
    expect(guarded.compile('src/{a,b}')).toBe('src/(a|b)');
    expect(guarded.stringify(guarded.parse('a/{b,c}/d'))).toBe('a/{b,c}/d');
    expect(guarded.expand('literal\\{a,b\\}')).toEqual(['literal{a,b}']);
  });
  it('installs the protected implementation for every existing build-tool consumer', () => {
    for (const consumer of ['tailwindcss', 'chokidar', 'micromatch']) {
      const fromConsumer = createRequire(require.resolve(`${consumer}/package.json`));
      expect(fromConsumer('braces/package.json').name).toBe('@nextstepuni/braces-guarded');
      expect(() => fromConsumer('braces')(malicious)).toThrow(SyntaxError);
    }
  });
});
