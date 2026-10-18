/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The onboarding "How do points work?" explainer shows only the levels a
 * student's subjects offer, marks their own grades, and never appears where
 * CAO points do not exist.
 */
import React from 'react';
import { describe, expect, test } from 'vitest';
import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import PointsGuide, { guideColumns } from '../components/onboarding/PointsGuide';
import type { SetupDraft } from '../components/onboarding/model';

const choice = (level: SetupDraft['configs'][string]['level'], current: string, target: string) => ({ level, current, target, reviewed: true }) as SetupDraft['configs'][string];
const open = (draft: Pick<SetupDraft, 'subjects' | 'configs'>) => {
  render(<PointsGuide draft={draft} />);
  fireEvent.click(screen.getByRole('button', { name: /How do points work/ }));
  return screen.getByRole('dialog');
};

describe('guideColumns', () => {
  test('shows every level before subjects are chosen', () => {
    expect(guideColumns([])).toEqual(['higher', 'ordinary', 'foundation']);
  });
  test('shows Foundation only when Maths or Irish is chosen', () => {
    expect(guideColumns(['Biology', 'French'])).toEqual(['higher', 'ordinary']);
    expect(guideColumns(['Biology', 'Mathematics'])).toEqual(['higher', 'ordinary', 'foundation']);
    expect(guideColumns(['Irish'])).toEqual(['higher', 'ordinary', 'foundation']);
  });
  test('a Higher-only subject on its own needs only the Higher column', () => {
    expect(guideColumns(['Romanian'])).toEqual(['higher']);
  });
});

describe('PointsGuide', () => {
  test('lists Higher and Ordinary points and marks the student’s own grades', () => {
    const dialog = open({ subjects: ['Japanese'], configs: { Japanese: choice('ordinary', 'O1', 'H1') } });
    expect(within(dialog).getByRole('cell', { name: 'H1: 100 points, your target' })).toBeInTheDocument();
    expect(within(dialog).getByRole('cell', { name: 'O1: 56 points, your current grade' })).toBeInTheDocument();
    expect(within(dialog).getByRole('cell', { name: 'H5: 56 points' })).toBeInTheDocument();
    expect(within(dialog).queryByRole('columnheader', { name: 'Foundation' })).not.toBeInTheDocument();
    expect(within(dialog).queryByText(/Higher Maths bonus/)).not.toBeInTheDocument();
  });

  test('adds Foundation, the Maths bonus and LCVP only where they apply', () => {
    const dialog = open({
      subjects: ['Mathematics', 'Irish', 'LCVP Link Modules'],
      configs: { Mathematics: choice('higher', 'H4', 'H2'), Irish: choice('foundation', 'F2', 'O3'), 'LCVP Link Modules': choice('common', 'Merit', 'Distinction') },
    });
    expect(within(dialog).getByRole('columnheader', { name: 'Foundation' })).toBeInTheDocument();
    expect(within(dialog).getByRole('cell', { name: 'F1: 20 points' })).toBeInTheDocument();
    expect(within(dialog).getByText(/25 extra points/)).toBeInTheDocument();
    expect(within(dialog).getByText(/66, 46 or 28 points/)).toBeInTheDocument();
  });

  test('closes with Escape', async () => {
    open({ subjects: [], configs: {} });
    fireEvent.keyDown(window, { key: 'Escape' });
    await waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument());
  });
});
