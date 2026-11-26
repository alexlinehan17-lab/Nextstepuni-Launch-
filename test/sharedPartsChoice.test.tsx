/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Choosing (components/ui/Choice.tsx): the selection mark, the switch and the
 * selection bar. The tick draws (160ms, 60ms after the outline) and, when the
 * system asks for reduced motion, simply appears (motion.md, sections 3 and 5).
 *
 * jsdom does not apply stylesheets, so the motion is checked in the stylesheet
 * the parts load (components/ui/parts.css); the same rules are measured in
 * Chrome with reduced motion emulated on the parts sheet (stage 2A evidence).
 */
import { useState } from 'react';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, test } from 'vitest';
import { ChoiceGroup, SelectionBar, SelectionMark, Switch } from '@/components/ui/Choice';

afterEach(cleanup);

const css = readFileSync(join(process.cwd(), 'components/ui/parts.css'), 'utf8').replace(/\/\*[\s\S]*?\*\//g, '');
const reduced = (() => {
  const at = css.indexOf('@media (prefers-reduced-motion: reduce)');
  let depth = 0;
  for (let i = css.indexOf('{', at); i < css.length; i += 1) {
    if (css[i] === '{') depth += 1;
    if (css[i] === '}') { depth -= 1; if (depth === 0) return css.slice(at, i + 1); }
  }
  return '';
})();
/** The declarations of the first rule whose selector list contains `selector`, in `source`. */
function rule(source: string, selector: string): string {
  const escaped = selector.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const match = source.match(new RegExp(`(?:^|[}\\s,])${escaped}\\s*(?:,[^{]*)?\\{([^}]*)\\}`, 'm'));
  return match?.[1] ?? '';
}

describe('the tick that draws', () => {
  test('chosen: the ring fills and the tick draws, 160ms after a 60ms wait, on the ease-out curve', () => {
    expect(rule(css, '.ui-mark--on path')).toMatch(/stroke-dashoffset:\s*0/);
    expect(rule(css, '.ui-mark--on path')).toMatch(/transition:\s*stroke-dashoffset var\(--t-draw\) var\(--ease-out\) var\(--t-draw-wait\)/);
    expect(rule(css, '.ui-mark path')).toMatch(/stroke-dasharray:\s*22;\s*stroke-dashoffset:\s*22/);
    const tokens = readFileSync(join(process.cwd(), 'index.css'), 'utf8');
    expect(tokens).toMatch(/--t-draw:\s*160ms/);
    expect(tokens).toMatch(/--t-draw-wait:\s*60ms/);
  });

  test('under reduced motion the tick does not animate: it simply appears', () => {
    expect(reduced, 'parts.css has a reduced-motion block').not.toBe('');
    expect(rule(reduced, '.ui-mark--on path')).toMatch(/transition:\s*none/);
    // Nothing else travels or scales either; fades and colour stay.
    for (const selector of ['.ui-seg-pill', '.ui-switch-knob']) expect(rule(reduced, selector), selector).toMatch(/transition:\s*none/);
    expect(reduced).toMatch(/\.ui-choice:active[^{]*\{\s*transform:\s*none/);
  });

  test('deselecting reverses with no drawing: the off state has no tick transition', () => {
    expect(rule(css, '.ui-mark path')).toMatch(/transition:\s*none/);
  });

  test('the mark says its state, and its shape says pick-one or pick-several', () => {
    const { container, rerender } = render(<SelectionMark on={false} />);
    expect(container.querySelector('.ui-mark')).toHaveAttribute('data-mark', 'off');
    rerender(<SelectionMark on shape="square" />);
    expect(container.querySelector('.ui-mark')).toHaveClass('ui-mark--on', 'ui-mark--square');
  });
});

test('pick-one is a radio group: a tap chooses, arrow keys move and choose', () => {
  function One() {
    const [v, setV] = useState<string | null>(null);
    return <ChoiceGroup legend="How much would you enjoy doing this?" value={v} onChange={setV}
      options={[{ value: 'love', label: "I'd love it" }, { value: 'like', label: "I'd like it" }, { value: 'unsure', label: 'Not sure' }]} />;
  }
  render(<One />);
  expect(screen.getByRole('radiogroup', { name: 'How much would you enjoy doing this?' })).toBeInTheDocument();
  fireEvent.click(screen.getByRole('radio', { name: "I'd like it" }));
  expect(screen.getByRole('radio', { name: "I'd like it" })).toHaveAttribute('aria-checked', 'true');
  fireEvent.keyDown(screen.getByRole('radio', { name: "I'd like it" }), { key: 'ArrowDown' });
  expect(screen.getByRole('radio', { name: 'Not sure' })).toHaveAttribute('aria-checked', 'true');
  expect(document.activeElement).toBe(screen.getByRole('radio', { name: 'Not sure' }));
});

test('pick-several counts what is chosen and says the state in words', () => {
  function Several() {
    const [v, setV] = useState<string[]>(['bio']);
    return <ChoiceGroup kind="several" tiles legend="Your subjects" value={v} onChange={setV}
      options={[{ value: 'bio', label: 'Biology', meta: 'Add', metaChosen: 'Added' }, { value: 'eng', label: 'English', meta: 'Add', metaChosen: 'Added' }]} />;
  }
  render(<Several />);
  expect(screen.getByText('1 of 2 chosen')).toBeInTheDocument();
  fireEvent.click(screen.getByRole('checkbox', { name: /English/ }));
  expect(screen.getByText('2 of 2 chosen')).toBeInTheDocument();
  expect(screen.getByRole('checkbox', { name: /English/ })).toHaveTextContent('Added');
});

test('a switch applies at once and is ink when on (aria-checked)', () => {
  function S() { const [on, setOn] = useState(false); return <Switch checked={on} onChange={setOn} label="Offer me questions when I finish" />; }
  render(<S />);
  const sw = screen.getByRole('switch', { name: 'Offer me questions when I finish' });
  expect(sw).toHaveAttribute('aria-checked', 'false');
  fireEvent.click(sw);
  expect(sw).toHaveAttribute('aria-checked', 'true');
  expect(rule(css, ".ui-switch[aria-checked='true']")).toMatch(/background:\s*var\(--ink-primary\)/);
});

test('the selection bar: the pill sits on the current choice, and none shows before a choice', () => {
  function Bar({ start }: { start: string }) {
    const [v, setV] = useState(start);
    return <SelectionBar label="Show" value={v} onChange={setV} options={[{ value: 'paper', label: 'Paper' }, { value: 'scheme', label: 'Scheme' }]} />;
  }
  const { container, unmount } = render(<Bar start="" />);
  expect(container.querySelector('.ui-seg-pill')).toBeNull();
  fireEvent.click(screen.getByRole('radio', { name: 'Scheme' }));
  const bar = screen.getByRole('radiogroup', { name: 'Show' });
  expect(bar.style.getPropertyValue('--seg-i')).toBe('1');
  expect(container.querySelector('.ui-seg-pill')).not.toBeNull();
  unmount();
  // It slides on the move curve in 260ms; nothing bounces.
  expect(rule(css, '.ui-seg-pill')).toMatch(/transition:\s*transform var\(--t-move\) var\(--ease-move\)/);
});
