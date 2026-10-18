/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * A student on Ordinary level can aim for a Higher grade ("allow students who
 * are current grade in ordinary to set a target of higher level", 17 Oct 2026).
 */
import React from 'react';
import { describe, expect, test, vi } from 'vitest';
import { fireEvent, render, screen, within } from '@testing-library/react';
import { SubjectGradeCards } from '../components/shared/SubjectProfileCards';
import type { GradeConfig } from '../components/shared/SubjectProfileCards';

const render1 = (config: GradeConfig, onUpdate = vi.fn()) => {
  render(<SubjectGradeCards selected={new Set(['English'])} configs={{ English: config }} onUpdate={onUpdate} />);
  return { onUpdate, targets: screen.getByRole('group', { name: 'English target grade' }) };
};

describe('target grades on the change-subjects cards', () => {
  test('an Ordinary student can pick a Higher target', () => {
    const { onUpdate, targets } = render1({ level: 'ordinary', currentGrade: 'O2', targetGrade: 'O1' });
    const buttons = within(targets).getAllByRole('button').map(button => button.textContent);
    expect(buttons.slice(0, 3)).toEqual(['H1', 'H2', 'H3']);
    expect(buttons).toContain('O1');

    fireEvent.click(within(targets).getByRole('button', { name: 'H3' }));
    expect(onUpdate).toHaveBeenCalledWith('English', 'targetGrade', 'H3');
  });

  test('targets worse than the current grade stay disabled', () => {
    const { targets } = render1({ level: 'ordinary', currentGrade: 'O2', targetGrade: 'O1' });
    expect(within(targets).getByRole('button', { name: 'H7' })).toBeDisabled();
    expect(within(targets).getByRole('button', { name: 'O3' })).toBeDisabled();
    expect(within(targets).getByRole('button', { name: 'H6' })).toBeEnabled();
    expect(within(targets).getByRole('button', { name: 'O1' })).toBeEnabled();
  });

  test('a Higher student sees Higher targets only', () => {
    const { targets } = render1({ level: 'higher', currentGrade: 'H4', targetGrade: 'H2' });
    expect(within(targets).getAllByRole('button')).toHaveLength(8);
  });

  test('moving from Ordinary to Higher shows the points gain', () => {
    render1({ level: 'ordinary', currentGrade: 'O2', targetGrade: 'H3' });
    expect(screen.getByText('+31 pts')).toBeInTheDocument();
  });
});
