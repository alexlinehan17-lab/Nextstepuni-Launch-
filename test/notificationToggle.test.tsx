/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import React from 'react';
import { describe, expect, test, vi } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';

vi.mock('@/components/gc/gcNotifications', () => ({
  getNotifications: vi.fn().mockResolvedValue([]),
  markNotificationRead: vi.fn().mockResolvedValue(undefined),
  markAllRead: vi.fn().mockResolvedValue(undefined),
}));

import NotificationBell from '@/components/NotificationBell';
import { toggleNotificationPanel } from '@/utils/notificationPanel';

const NotificationFixture: React.FC = () => (
  <>
    <button data-notification-toggle onClick={toggleNotificationPanel}>Sidebar notifications</button>
    <NotificationBell uid="student-1" />
  </>
);

describe('notification panel toggles', () => {
  test('the sidebar control opens and then closes the existing panel', () => {
    render(<NotificationFixture />);
    const sidebarButton = screen.getByRole('button', { name: 'Sidebar notifications' });
    const bell = screen.getByRole('button', { name: 'Open notifications' });

    fireEvent.mouseDown(sidebarButton);
    fireEvent.click(sidebarButton);
    expect(bell).toHaveAttribute('aria-expanded', 'true');
    expect(bell).toHaveAccessibleName('Close notifications');

    // Reproduce the browser's mousedown → click sequence. The mousedown must
    // not dismiss the panel before the click performs the one intended toggle.
    fireEvent.mouseDown(sidebarButton);
    fireEvent.click(sidebarButton);
    expect(bell).toHaveAttribute('aria-expanded', 'false');
    expect(bell).toHaveAccessibleName('Open notifications');
  });

  test('the bell itself still alternates between open and closed', () => {
    render(<NotificationFixture />);
    const bell = screen.getByRole('button', { name: 'Open notifications' });

    fireEvent.click(bell);
    expect(bell).toHaveAttribute('aria-expanded', 'true');
    fireEvent.click(bell);
    expect(bell).toHaveAttribute('aria-expanded', 'false');
  });
});
