import { expect, test } from 'vitest';
import { cn } from '../components/approved-ui-runtime';
import { readFileSync } from 'node:fs';
import postcss from 'postcss';
import selectorParser from 'postcss-selector-parser';

test('native utility classes cannot move or restyle the surrounding app', () => {
  expect(cn('flex flex-col -translate-x-1/2', 'custom-card')).toBe('nsuk-flex nsuk-flex-col nsuk--translate-x-1/2 custom-card');
  expect(cn(cn('flex flex-col'), 'flex-row')).toBe('nsuk-flex nsuk-flex-row');
  const css = postcss.parse(readFileSync('components/approved-ui-runtime.css','utf8'));
  const leaked: string[] = [];
  css.walkRules(rule => { selectorParser(root => root.walkClasses(node => {
    if (['flex','flex-col','-translate-x-1/2','-translate-y-1/2','hidden'].includes(node.value)) leaked.push(node.value);
  })).processSync(rule.selector); });
  expect(leaked).toEqual([]);
});
