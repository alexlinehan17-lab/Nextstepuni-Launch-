/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeEach, describe, expect, test, vi } from 'vitest';

import FeedbackModal, { feedbackSubmissionErrorMessage } from '@/components/FeedbackModal';

const { callableMock } = vi.hoisted(() => ({
  callableMock: vi.fn(),
}));

vi.mock('firebase/functions', () => ({
  getFunctions: vi.fn(() => ({})),
  httpsCallable: vi.fn(() => callableMock),
}));

describe('anonymous feedback modal', () => {
  beforeEach(() => {
    callableMock.mockReset();
    callableMock.mockResolvedValue({ data: { success: true } });
  });

  test('replaces the QR flow with a problem-first in-app form', () => {
    render(<FeedbackModal open onClose={vi.fn()} />);

    expect(screen.getByRole('heading', { name: 'What should we fix?' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Something is broken/ })).toHaveAttribute('aria-pressed', 'true');
    expect(screen.getByRole('button', { name: 'Send anonymously' })).toBeDisabled();
    expect(screen.queryByAltText(/QR code/i)).not.toBeInTheDocument();
  });

  test('keeps the textarea focused while the student types', async () => {
    const user = userEvent.setup();
    render(<FeedbackModal open onClose={vi.fn()} />);

    const textarea = screen.getByLabelText('Tell us what happened');
    await user.click(textarea);
    await user.keyboard('Every letter should stay in this box.');

    expect(textarea).toHaveValue('Every letter should stay in this box.');
    expect(textarea).toHaveFocus();
  });

  test('submits product context without account identity', async () => {
    render(
      <FeedbackModal
        open
        onClose={vi.fn()}
        context={{ surface: 'module', moduleId: 'growth-mindset', moduleTitle: 'Growth Mindset' }}
      />,
    );

    fireEvent.click(screen.getByRole('button', { name: /Feature idea/ }));
    fireEvent.change(screen.getByLabelText('Tell us what happened'), {
      target: { value: 'Please add a way to bookmark a module section.' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Send anonymously' }));

    await waitFor(() => expect(callableMock).toHaveBeenCalledTimes(1));
    const payload = callableMock.mock.calls[0][0] as Record<string, unknown>;
    expect(payload).toMatchObject({
      category: 'idea',
      message: 'Please add a way to bookmark a module section.',
      context: { surface: 'module', moduleId: 'growth-mindset', moduleTitle: 'Growth Mindset' },
    });
    expect(payload).not.toHaveProperty('uid');
    expect(payload).not.toHaveProperty('name');
    expect(payload).not.toHaveProperty('email');
    expect(payload).not.toHaveProperty('school');
    expect(await screen.findByText('Sent without account details.')).toBeInTheDocument();
  });

  test('explains the daily limit instead of blaming the connection', () => {
    expect(feedbackSubmissionErrorMessage({ code: 'functions/resource-exhausted' }))
      .toBe('You have sent several messages today. Please try again tomorrow.');
  });
});
