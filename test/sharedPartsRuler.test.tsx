/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The ruler of short choices (area 7a, Points Passport's What if?): a radio group, the chosen one
 * marked, arrow keys move and choose, a dot under the marked one.
 */
import React, { useState } from 'react';
import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, expect, test } from 'vitest';
import { ChoiceRuler } from '@/components/ui/Choice';

afterEach(cleanup);
const GRADES = ['H1', 'H2', 'H3', 'H4'];
function Harness() {
  const [value, setValue] = useState<string>('H3');
  return <ChoiceRuler label="Geography grade" value={value} onChange={setValue} options={GRADES.map(g => ({ value: g, label: g, name: `Geography ${g}`, marked: g === 'H4' }))} />;
}

test('a ruler is a radio group: the chosen one is checked, a press or an arrow key chooses', () => {
  render(<Harness />);
  const group = screen.getByRole('radiogroup', { name: 'Geography grade' });
  expect(screen.getByRole('radio', { name: 'Geography H3' })).toHaveAttribute('aria-checked', 'true');
  fireEvent.click(screen.getByRole('radio', { name: 'Geography H1' }));
  expect(screen.getByRole('radio', { name: 'Geography H1' })).toHaveAttribute('aria-checked', 'true');
  fireEvent.keyDown(screen.getByRole('radio', { name: 'Geography H1' }), { key: 'ArrowRight' });
  expect(screen.getByRole('radio', { name: 'Geography H2' })).toHaveAttribute('aria-checked', 'true');
  expect(group.querySelectorAll('.ui-ruler-dot')).toHaveLength(1);
});

test('a tall sheet can fit its tilt (fitTilt): the back sheets stay close to the face; off by default', async () => {
  const { PaperSheet } = await import('@/components/ui/List');
  const observers: (() => void)[] = [];
  const original = globalThis.ResizeObserver;
  globalThis.ResizeObserver = class { cb: () => void; constructor(cb: () => void) { this.cb = cb; observers.push(cb); } observe() {} disconnect() {} } as unknown as typeof ResizeObserver;
  const height = Object.getOwnPropertyDescriptor(HTMLElement.prototype, 'offsetHeight');
  Object.defineProperty(HTMLElement.prototype, 'offsetHeight', { configurable: true, get: () => 1400 });
  try {
    const { container } = render(<><PaperSheet label="Tall" fitTilt><p>Stage</p></PaperSheet><PaperSheet label="Plain"><p>Points</p></PaperSheet></>);
    const [tall, plain] = [...container.querySelectorAll('section')] as HTMLElement[];
    // 5px reach on a 1400px sheet: asin(5 / 700) = 0.41 degrees.
    expect(tall.style.getPropertyValue('--paper-tilt')).toBe('0.41deg');
    expect(plain.style.getPropertyValue('--paper-tilt')).toBe('');
  } finally {
    globalThis.ResizeObserver = original;
    if (height) Object.defineProperty(HTMLElement.prototype, 'offsetHeight', height);
  }
});
