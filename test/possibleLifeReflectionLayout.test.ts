import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, test } from 'vitest';

describe('Your Possible Life reflection field alignment', () => {
  test('reserves the same heading track and fixes every journal field to one height', () => {
    const component = readFileSync(resolve(process.cwd(), 'components/YourPossibleLife.tsx'), 'utf8');
    const css = readFileSync(resolve(process.cwd(), 'index.css'), 'utf8');

    expect(component).toContain('text-3xl mt-7 lg:min-h-[72px]');
    expect(css).toMatch(/textarea\.possible-life-journal-field\s*\{[^}]*height:\s*112px;[^}]*min-height:\s*112px;/s);
  });
});
