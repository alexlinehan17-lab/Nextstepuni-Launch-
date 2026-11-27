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
