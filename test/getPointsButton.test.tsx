import React from 'react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { act, cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import GetPointsButton from '../components/GetPointsButton';
import { DEMO_STUDENT_UID } from '../data/devStudent';
import type { ProgressDocument } from '../services/progressRepository';

const state = vi.hoisted(() => ({
  uid: 'student-a',
  loaded: true,
  credit: vi.fn(),
  toast: vi.fn(),
  reload: vi.fn(),
  doc: { pointsData: { totalEarned: 250, totalSpent: 75 } } as ProgressDocument,
}));
vi.mock('../services/progressRepository', () => ({ creditDrawerPoints: state.credit, DRAWER_POINTS_CREDIT: 100 }));
vi.mock('../components/Toast', () => ({ useToast: () => ({ showToast: state.toast }) }));
vi.mock('../utils/logError', () => ({ logError: vi.fn(), reportSaveError: vi.fn() }));
vi.mock('../contexts/ProgressContext', () => ({
  useOptionalProgress: () => ({
    progressLoaded: state.loaded,
    progressDataUid: state.uid,
    reloadProgress: state.reload,
    updateDemoProgress: (update: (doc: ProgressDocument) => ProgressDocument) => { state.doc = update(state.doc); },
  }),
}));

beforeEach(() => {
  vi.clearAllMocks();
  state.uid = 'student-a';
  state.loaded = true;
  state.credit.mockResolvedValue(undefined);
  state.doc = { pointsData: { totalEarned: 250, totalSpent: 75 } };
});
afterEach(() => { cleanup(); vi.useRealTimers(); });

describe('GET POINTS drawer action', () => {
  it('credits the current account once while saving, then allows another credit', async () => {
    let finish!: () => void;
    state.credit.mockReturnValueOnce(new Promise<void>(resolve => { finish = resolve; }));
    render(<GetPointsButton uid="student-a" expanded />);
    const button = screen.getByRole('button', { name: 'GET POINTS' });
    fireEvent.click(button);
    fireEvent.click(button);
    expect(button).toBeDisabled();
    expect(state.credit).toHaveBeenCalledTimes(1);
    expect(state.credit).toHaveBeenCalledWith('student-a');
    await act(async () => finish());
    expect(button).toBeEnabled();
    expect(state.reload).toHaveBeenCalledTimes(1);
    expect(state.toast).toHaveBeenCalledWith('100 JP added to your bank.', 'success');
    fireEvent.click(button);
    await waitFor(() => expect(state.credit).toHaveBeenCalledTimes(2));
  });

  it('reports a rejected write and leaves the action available to retry', async () => {
    state.credit.mockRejectedValueOnce(new Error('permission-denied'));
    render(<GetPointsButton uid="student-a" expanded />);
    fireEvent.click(screen.getByRole('button', { name: 'GET POINTS' }));
    await waitFor(() => expect(state.toast).toHaveBeenCalledWith('Could not add JP. Please try again.', 'error'));
    expect(screen.getByRole('button', { name: 'GET POINTS' })).toBeEnabled();
    expect(state.toast).not.toHaveBeenCalledWith('100 JP added to your bank.', 'success');
  });

  it('unblocks a queued offline write and reports any later rejection', async () => {
    vi.useFakeTimers();
    let reject!: (error: Error) => void;
    state.credit.mockReturnValueOnce(new Promise<void>((_, fail) => { reject = fail; }));
    render(<GetPointsButton uid="student-a" expanded />);
    fireEvent.click(screen.getByRole('button', { name: 'GET POINTS' }));
    await act(async () => { await vi.advanceTimersByTimeAsync(4000); });
    expect(screen.getByRole('button', { name: 'GET POINTS' })).toBeEnabled();
    expect(state.toast).toHaveBeenCalledWith('100 JP queued. They’ll sync when you’re online.', 'info');
    await act(async () => reject(new Error('permission-denied')));
    expect(state.toast).toHaveBeenCalledWith('Could not add JP. Please try again.', 'error');
  });

  it('adds 100 per click in the demo without overwriting spending or writing remotely', () => {
    state.uid = DEMO_STUDENT_UID;
    render(<GetPointsButton uid={DEMO_STUDENT_UID} expanded={false} />);
    const button = screen.getByRole('button', { name: 'GET POINTS' });
    fireEvent.click(button);
    fireEvent.click(button);
    expect(state.doc.pointsData).toEqual({ totalEarned: 450, totalSpent: 75 });
    expect(state.credit).not.toHaveBeenCalled();
  });

  it('does not expose a credit action for unloaded or mismatched account data', () => {
    const { rerender } = render(<GetPointsButton uid="student-b" expanded />);
    expect(screen.queryByRole('button')).not.toBeInTheDocument();
    state.loaded = false;
    rerender(<GetPointsButton uid="student-a" expanded />);
    expect(screen.queryByRole('button')).not.toBeInTheDocument();
  });
});
