/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The chosen mark on a stepped claim row (Politics, Geography and PE bands) stands apart
 * from the marks not chosen: it alone is pressed and carries the tick.
 */

import { describe, expect, test } from 'vitest';
import { render, screen, within } from '@testing-library/react';

import { ClaimRow } from '@/components/MarkBank/ClaimRows';

describe('the chosen mark on a stepped row stands apart from its neighbours', () => {
  test('only the chosen step carries the tick, and it is the pressed one', () => {
    render(<ClaimRow text="Very good" steps={[7, 8]} claimed value={8} onToggle={() => undefined} onStep={() => undefined} />);
    const group = screen.getByRole('group', { name: 'Marks for Very good' });
    const chosen = within(group).getByRole('button', { name: 'Clear 8 marks for Very good' });
    const other = within(group).getByRole('button', { name: 'Claim 7 marks for Very good' });
    expect(chosen).toHaveAttribute('aria-pressed', 'true');
    expect(chosen.querySelector('svg')).not.toBeNull();
    expect(other.querySelector('svg')).toBeNull();
  });
});

