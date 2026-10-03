import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import test from 'node:test';
const require = createRequire(import.meta.url);
const braces = require('braces');

test('nested brace/parenthesis input is rejected before recursive stack exhaustion', () => {
  for (const pattern of ['{'.repeat(4000) + 'a,b' + '}'.repeat(4000), '('.repeat(4000) + 'a' + ')'.repeat(4000)]) {
    for (const action of [braces, braces.expand, braces.stringify]) {
      assert.throws(() => action(pattern), /exceeds max depth/);
      assert.throws(() => action(pattern, { maxDepth: 1_000_000 }), /exceeds max depth/);
    }
  }
});

test('direct AST entry points also reject excessive nesting', () => {
  for (const action of [braces.compile, braces.expand, braces.stringify]) {
    let ast = { type: 'text', value: 'a' };
    for (let i = 0; i < 101; i++) ast = { type: 'brace', nodes: [ast] };
    assert.throws(() => action({ type: 'root', nodes: [ast] }), /exceeds max depth/);
  }
});

test('ordinary build-tool glob patterns preserve expansion and compilation', () => {
  assert.deepEqual(braces.expand('src/{components,hooks}/**/*.{ts,tsx}'), [
    'src/components/**/*.ts', 'src/components/**/*.tsx', 'src/hooks/**/*.ts', 'src/hooks/**/*.tsx',
  ]);
  assert.deepEqual(braces.expand('file{1..3}.js'), ['file1.js', 'file2.js', 'file3.js']);
  assert.deepEqual(braces('a/{b,c}/d'), ['a/(b|c)/d']);
});
