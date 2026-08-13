/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import React from 'react';
import { describe, expect, test, vi } from 'vitest';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';

import CollegeCompass from '@/components/CollegeCompass';

const cycleItemStatus = vi.fn();

vi.mock('@/hooks/useCollegeCompass', () => ({
  useCollegeCompass: () => ({
    state: { checklist: {}, updatedAt: '' },
    isLoaded: true,
    cycleItemStatus,
    setHearIndicators: vi.fn(),
    setDareCategory: vi.fn(),
    setTargetInstitutions: vi.fn(),
    toggleDismissStop: vi.fn(),
  }),
}));

vi.mock('@/components/ModuleShared', () => ({
  ToolJumpCard: () => <div>Related tool</div>,
}));

vi.mock('@/components/collegeCompass/HearMeter', () => ({ default: () => <div>HEAR check</div> }));
vi.mock('@/components/collegeCompass/DareGate', () => ({ default: () => <div>DARE check</div> }));
vi.mock('@/components/collegeCompass/MoneySorter', () => ({ default: () => <div>Money sorter</div> }));
vi.mock('@/components/collegeCompass/OpenDoor', () => ({ default: () => <div>Open door</div> }));
vi.mock('@/components/collegeCompass/DocumentChecklist', () => ({ default: () => <div>Document checklist</div> }));

describe('College Compass horizontal timeline', () => {
  test('shows all six milestones but only one focused workspace', () => {
    render(<CollegeCompass yearGroup="5th" />);

    const tabs = screen.getAllByRole('tab');
    expect(tabs).toHaveLength(6);
    expect(tabs[0]).toHaveAttribute('aria-selected', 'true');
    expect(screen.getAllByRole('tabpanel')).toHaveLength(1);
    expect(screen.getByRole('tabpanel')).toHaveAccessibleName('Doors Open');

    fireEvent.click(screen.getByRole('tab', { name: /The Access Window/ }));
    expect(screen.getByRole('tabpanel')).toHaveAccessibleName('The Access Window');
    expect(screen.queryByRole('heading', { name: 'Doors Open' })).not.toBeInTheDocument();
    expect(screen.getByText('HEAR check')).toBeInTheDocument();
  });

  test('supports arrow, Home and End keys with roving focus', async () => {
    render(<CollegeCompass yearGroup="5th" />);

    const doors = screen.getByRole('tab', { name: /Doors Open/ });
    doors.focus();
    fireEvent.keyDown(doors, { key: 'ArrowRight' });
    const lockIn = screen.getByRole('tab', { name: /Lock-In Day/ });
    await waitFor(() => expect(lockIn).toHaveFocus());
    expect(lockIn).toHaveAttribute('aria-selected', 'true');

    fireEvent.keyDown(lockIn, { key: 'End' });
    const results = screen.getByRole('tab', { name: /Results & Offers/ });
    await waitFor(() => expect(results).toHaveFocus());
    expect(screen.getByRole('tabpanel')).toHaveAccessibleName('Results & Offers');

    fireEvent.keyDown(results, { key: 'Home' });
    await waitFor(() => expect(screen.getByRole('tab', { name: /Doors Open/ })).toHaveFocus());
  });

  test('preserves the three-state checklist interaction', () => {
    cycleItemStatus.mockClear();
    render(<CollegeCompass yearGroup="5th" />);

    fireEvent.click(screen.getByRole('button', { name: /Create my CAO account at cao.ie/ }));
    expect(cycleItemStatus).toHaveBeenCalledWith('doors-open:create-account');
  });
});
