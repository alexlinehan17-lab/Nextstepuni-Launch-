/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { render, renderHook, screen } from '@testing-library/react';
import { beforeEach, describe, expect, test, vi } from 'vitest';
import NotificationBell from '@/components/NotificationBell';
import { DEMO_STUDENT_UID } from '@/data/devStudent';
import { useGifts } from '@/hooks/useGifts';
import { useKudos } from '@/hooks/useKudos';

const mocks = vi.hoisted(() => ({
  getDocs: vi.fn(),
  addDoc: vi.fn(),
  writeBatch: vi.fn(),
  getNotifications: vi.fn(),
  markNotificationRead: vi.fn(),
  markAllRead: vi.fn(),
}));

vi.mock('firebase/firestore', () => ({
  collection: vi.fn(),
  query: vi.fn(),
  where: vi.fn(),
  orderBy: vi.fn(),
  limit: vi.fn(),
  getDocs: mocks.getDocs,
  addDoc: mocks.addDoc,
  serverTimestamp: vi.fn(),
  Timestamp: { fromDate: vi.fn() },
  writeBatch: mocks.writeBatch,
  doc: vi.fn(),
  increment: vi.fn(),
}));

vi.mock('@/components/gc/gcNotifications', () => ({
  getNotifications: mocks.getNotifications,
  markNotificationRead: mocks.markNotificationRead,
  markAllRead: mocks.markAllRead,
  STAFF_ORIGINATED: new Set(),
}));

describe('Demo Account offline isolation', () => {
  beforeEach(() => {
    Object.values(mocks).forEach(mock => mock.mockReset());
  });

  test('does not query Firestore-backed social features', () => {
    const kudos = renderHook(() => useKudos(DEMO_STUDENT_UID));
    const gifts = renderHook(() => useGifts(DEMO_STUDENT_UID));

    expect(kudos.result.current.kudosCount).toBe(0);
    expect(gifts.result.current.pendingGifts).toEqual([]);
    expect(mocks.getDocs).not.toHaveBeenCalled();
    expect(mocks.writeBatch).not.toHaveBeenCalled();
  });

  test('keeps the notification bell usable without polling Firestore', () => {
    render(<NotificationBell uid={DEMO_STUDENT_UID} />);

    expect(screen.getByRole('button', { name: 'Open notifications' })).toBeInTheDocument();
    expect(mocks.getNotifications).not.toHaveBeenCalled();
  });
});
