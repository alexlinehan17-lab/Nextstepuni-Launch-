import { existsSync, readFileSync } from 'node:fs';
import { expect, test } from 'vitest';

test('the published control runtime carries scoped styles and every local font', () => {
  const runtime = readFileSync('components/approved-ui-runtime.js', 'utf8');
  expect(runtime).toContain('import "./approved-ui-runtime.css"');
  expect(runtime).toContain('import "./approved-ui-theme.css"');
  expect(runtime).not.toContain('/Users/');
  expect(runtime).not.toContain('@/components/kobra/');
  for (const file of ['components/approved-ui-runtime.css', 'components/approved-ui-theme.css']) {
    const css = readFileSync(file, 'utf8');
    for (const match of css.matchAll(/url\(["']?(\/[^"')]+)["']?\)/g)) {
      expect(existsSync(`public${match[1]}`), `Missing style asset: ${match[1]}`).toBe(true);
    }
  }
});
