/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The onboarding "How do points work?" explainer (Kobra Dialog and Tabs) shows
 * only the levels a student's subjects offer, marks their own grades and the
 * tabs that hold them, and adds notes only where they apply.
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
  return screen.findByRole('dialog');
};
const line = (dialog: HTMLElement, code: string) => within(dialog).getByText(code).closest('li') as HTMLElement;

describe('guideColumns', () => {
  test('shows every level before subjects are chosen', () => {
    expect(guideColumns([])).toEqual(['higher', 'ordinary', 'foundation']);
  });
  test('shows Foundation only when Maths or Irish is chosen', () => {
    expect(guideColumns(['Biology', 'French'])).toEqual(['higher', 'ordinary']);
    expect(guideColumns(['Biology', 'Mathematics'])).toEqual(['higher', 'ordinary', 'foundation']);
    expect(guideColumns(['Irish'])).toEqual(['higher', 'ordinary', 'foundation']);
  });
  test('a Higher-only subject on its own needs only the Higher tab', () => {
    expect(guideColumns(['Romanian'])).toEqual(['higher']);
  });
});

describe('PointsGuide', () => {
  test('opens on the student’s own level and marks their current grade and target', async () => {
    const dialog = await open({ subjects: ['Japanese', 'Irish'], configs: { Japanese: choice('ordinary', 'O1', 'H1'), Irish: choice('ordinary', 'O2', 'O3') } });
    expect(within(dialog).getByRole('tab', { name: /Ordinary/ })).toHaveAttribute('aria-selected', 'true');
    expect(within(line(dialog, 'O1')).getByText('You now')).toBeInTheDocument();
    expect(within(line(dialog, 'O3')).getByText('Target')).toBeInTheDocument();
    expect(within(line(dialog, 'O4')).queryByText(/You now|Target/)).not.toBeInTheDocument();
  });

  test('flags the tab that holds a target on another level and shows it there', async () => {
    const dialog = await open({ subjects: ['Japanese'], configs: { Japanese: choice('ordinary', 'O1', 'H1') } });
    const higher = within(dialog).getByRole('tab', { name: /Higher/ });
    expect(within(higher).getByRole('img', { name: 'has your grades' })).toBeInTheDocument();
    fireEvent.click(higher);
    await waitFor(() => expect(within(line(dialog, 'H1')).getByText('Target')).toBeInTheDocument());
    expect(within(line(dialog, 'H1')).getByRole('progressbar', { name: 'H1, 100 points' })).toBeInTheDocument();
  });

  test('has no Foundation tab or Maths note unless they apply', async () => {
    const dialog = await open({ subjects: ['Japanese'], configs: { Japanese: choice('ordinary', 'O1', 'H1') } });
    expect(within(dialog).queryByRole('tab', { name: /Foundation/ })).not.toBeInTheDocument();
    expect(within(dialog).queryByText(/Higher Maths bonus/)).not.toBeInTheDocument();
    expect(within(dialog).queryByText(/LCVP Link Modules/)).not.toBeInTheDocument();
  });

  test('adds Foundation, the Maths bonus and LCVP where they apply', async () => {
    const dialog = await open({
      subjects: ['Mathematics', 'Irish', 'LCVP Link Modules'],
      configs: { Mathematics: choice('higher', 'H4', 'H2'), Irish: choice('foundation', 'F2', 'O3'), 'LCVP Link Modules': choice('common', 'Merit', 'Distinction') },
    });
    const foundation = within(dialog).getByRole('tab', { name: /Foundation/ });
    fireEvent.click(foundation);
    await waitFor(() => expect(within(line(dialog, 'F1')).getByRole('progressbar', { name: 'F1, 20 points' })).toBeInTheDocument());
    expect(within(dialog).getByText(/25 extra points/)).toBeInTheDocument();
    expect(within(dialog).getByText(/66, 46 or 28 points/)).toBeInTheDocument();
  });

  test('closes with Escape', async () => {
    await open({ subjects: [], configs: {} });
    fireEvent.keyDown(document.activeElement ?? document.body, { key: 'Escape' });
    await waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument());
  });
});
