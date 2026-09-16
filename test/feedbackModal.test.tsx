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

  test('opens the listening room with an idea selected and submission disabled', () => {
    render(<FeedbackModal open onClose={vi.fn()} />);

    expect(screen.getByRole('heading', { name: 'What would make it better?' })).toBeInTheDocument();
    expect(screen.getByRole('radio', { name: 'I have an idea' })).toBeChecked();
    expect(screen.getByRole('button', { name: 'Send anonymously' })).toBeDisabled();
    expect(screen.queryByAltText(/QR code/i)).not.toBeInTheDocument();
  });

  test('keeps the textarea focused while the student types', async () => {
    const user = userEvent.setup();
    render(<FeedbackModal open onClose={vi.fn()} />);

    const textarea = screen.getByLabelText('Your words. We’re listening.');
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

    fireEvent.click(screen.getByRole('radio', { name: 'I have an idea' }));
    fireEvent.change(screen.getByLabelText('Your words. We’re listening.'), {
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

  test('can leave out the app context and keeps the message when a send fails', async () => {
    callableMock.mockRejectedValueOnce({ code: 'functions/unavailable' });
    render(<FeedbackModal open onClose={vi.fn()} context={{ surface: 'home' }} />);
    fireEvent.click(screen.getByRole('radio', { name: 'Something isn’t working' }));
    const textarea = screen.getByLabelText('Your words. We’re listening.');
    expect(textarea).toHaveAttribute('placeholder', 'What were you trying to do? What happened instead?');
    fireEvent.change(textarea, { target: { value: 'The next card button stopped responding.' } });
    fireEvent.click(screen.getByRole('checkbox', { name: /Include the page/ }));
    fireEvent.click(screen.getByRole('button', { name: 'Send anonymously' }));
    expect(await screen.findByRole('alert')).toHaveTextContent('That did not send.');
    expect(textarea).toHaveValue('The next card button stopped responding.');
    expect(screen.getByRole('button', { name: 'Send anonymously' })).toBeEnabled();
    expect(callableMock).toHaveBeenCalledWith(expect.objectContaining({ category: 'broken', context: null }));
    fireEvent.click(screen.getByRole('button', { name: 'Send anonymously' }));
    expect(await screen.findByText('Sent without account details.')).toBeInTheDocument();
  });

  test('prevents a second submission or dismissal while sending', async () => {
    let finishSend!: (value: unknown) => void;
    callableMock.mockImplementationOnce(() => new Promise(resolve => { finishSend = resolve; }));
    const onClose = vi.fn();
    render(<FeedbackModal open onClose={onClose} />);
    fireEvent.change(screen.getByLabelText('Your words. We’re listening.'), { target: { value: 'A useful suggestion about studying.' } });
    fireEvent.click(screen.getByRole('button', { name: 'Send anonymously' }));
    expect(screen.getByRole('button', { name: 'Sending…' })).toBeDisabled();
    expect(screen.getByRole('button', { name: 'Close' })).toBeDisabled();
    fireEvent.keyDown(window, { key: 'Escape' });
    expect(onClose).not.toHaveBeenCalled();
    expect(callableMock).toHaveBeenCalledTimes(1);
    finishSend({ data: { success: true } });
    const thanks = await screen.findByRole('status');
    await waitFor(() => expect(thanks).toHaveFocus());
    fireEvent.click(screen.getByRole('button', { name: 'Back to my study' }));
    expect(onClose).toHaveBeenCalledOnce();
  });

  test('explains the daily limit instead of blaming the connection', () => {
    expect(feedbackSubmissionErrorMessage({ code: 'functions/resource-exhausted' }))
      .toBe('You have sent several messages today. Please try again tomorrow.');
  });
});
