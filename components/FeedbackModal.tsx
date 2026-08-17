/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Anonymous, in-app product feedback. Account identity is used transiently by
 * the callable function for authentication and rate limiting, but is never
 * written to the feedback record shown in the admin inbox.
 */

import React, { useEffect, useState } from 'react';
import { Check, LoaderCircle } from 'lucide-react';
import { getFunctions, httpsCallable } from 'firebase/functions';
import app from '../firebase';
import {
  FEEDBACK_CATEGORIES,
  FEEDBACK_CATEGORY_LABELS,
  getFeedbackPlatform,
  type FeedbackCategory,
} from '../utils/anonymousFeedback';
import ModalFrame from './ui/ModalFrame';

interface Props {
  open: boolean;
  onClose: () => void;
  context?: {
    surface: string;
    moduleId?: string;
    moduleTitle?: string;
  };
}

interface SubmitFeedbackRequest {
  category: FeedbackCategory;
  message: string;
  context: Props['context'] | null;
  platform: 'web' | 'ios' | 'android';
  appVersion: string;
}

const MIN_MESSAGE_LENGTH = 10;
const MAX_MESSAGE_LENGTH = 2000;

export function feedbackSubmissionErrorMessage(error: unknown): string {
  const code = typeof error === 'object' && error && 'code' in error
    ? String((error as { code?: unknown }).code)
    : '';
  if (code.endsWith('resource-exhausted')) {
    return 'You have sent several messages today. Please try again tomorrow.';
  }
  if (code.endsWith('permission-denied')) {
    return 'Feedback is available to active student accounts.';
  }
  return 'That did not send. Check your connection and try again.';
}

const FeedbackModal: React.FC<Props> = ({ open, onClose, context = { surface: 'home' } }) => {
  const [category, setCategory] = useState<FeedbackCategory>('broken');
  const [message, setMessage] = useState('');
  const [includeContext, setIncludeContext] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSent, setIsSent] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!open) return;
    setCategory('broken');
    setMessage('');
    setIncludeContext(true);
    setIsSubmitting(false);
    setIsSent(false);
    setError('');
  }, [open]);

  const close = () => {
    if (!isSubmitting) onClose();
  };

  const submit = async (event: React.FormEvent) => {
    event.preventDefault();
    const trimmedMessage = message.trim();
    if (trimmedMessage.length < MIN_MESSAGE_LENGTH || isSubmitting) return;

    setIsSubmitting(true);
    setError('');
    try {
      const functions = getFunctions(app);
      const submitFeedback = httpsCallable<SubmitFeedbackRequest, { success: true }>(
        functions,
        'submitAnonymousFeedback',
      );
      await submitFeedback({
        category,
        message: trimmedMessage,
        context: includeContext ? context : null,
        platform: getFeedbackPlatform(navigator.userAgent),
        appVersion: '0.0.0',
      });
      setIsSent(true);
    } catch (submissionError) {
      console.error('Anonymous feedback submission failed:', submissionError);
      setError(feedbackSubmissionErrorMessage(submissionError));
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <ModalFrame
      open={open}
      onClose={close}
      title={isSent ? 'Thank you.' : 'What should we fix?'}
      eyebrow="Anonymous feedback"
      description={isSent ? undefined : 'Tell us what is not working, what feels confusing, or what NextStepUni is missing.'}
      width="md"
      labelledBy="anonymous-feedback-title"
    >
      {isSent ? (
        <div className="py-8 text-center" role="status">
          <div className="mx-auto mb-5 flex h-14 w-14 items-center justify-center rounded-full border-2 border-[#3A8D5F] text-[#3A8D5F]">
            <Check size={26} strokeWidth={2} />
          </div>
          <p className="font-serif text-xl font-semibold text-[#1A1A1A] dark:text-white">Sent without account details.</p>
          <p className="mx-auto mt-2 max-w-sm text-sm leading-relaxed text-[#706A64] dark:text-zinc-400">
            Thank you — this genuinely helps us decide what to improve next.
          </p>
          <button
            type="button"
            onClick={onClose}
            className="mt-7 rounded-full border-2 border-[#1A1A1A] bg-white px-6 py-2.5 text-sm font-bold text-[#1A1A1A] transition-transform hover:-translate-y-0.5"
          >
            Done
          </button>
        </div>
      ) : (
        <form onSubmit={submit}>
          <fieldset>
            <legend className="mb-3 text-[11px] font-bold uppercase tracking-[0.16em] text-[#9E9186]">
              What kind of feedback is this?
            </legend>
            <div className="grid grid-cols-1 gap-2 sm:grid-cols-2">
              {FEEDBACK_CATEGORIES.map(option => {
                const selected = category === option;
                return (
                  <button
                    key={option}
                    type="button"
                    aria-pressed={selected}
                    onClick={() => setCategory(option)}
                    className="flex min-h-12 items-center justify-between rounded-xl border-2 bg-white px-4 py-3 text-left text-sm font-semibold transition-colors"
                    style={{
                      borderColor: selected ? '#F26B1F' : '#1A1A1A',
                      color: selected ? '#9A3B0E' : '#3A3530',
                    }}
                  >
                    {FEEDBACK_CATEGORY_LABELS[option]}
                    <span
                      aria-hidden="true"
                      className="h-2.5 w-2.5 rounded-full border"
                      style={{
                        borderColor: selected ? '#F26B1F' : '#9E9186',
                        backgroundColor: selected ? '#F26B1F' : '#FFFFFF',
                      }}
                    />
                  </button>
                );
              })}
            </div>
          </fieldset>

          <label htmlFor="anonymous-feedback-message" className="mt-6 block text-[11px] font-bold uppercase tracking-[0.16em] text-[#9E9186]">
            Tell us what happened
          </label>
          <textarea
            id="anonymous-feedback-message"
            value={message}
            onChange={event => setMessage(event.target.value)}
            maxLength={MAX_MESSAGE_LENGTH}
            rows={7}
            required
            placeholder="What were you trying to do? What got in the way? What would make it better?"
            className="mt-2 w-full resize-y rounded-xl border-2 border-[#1A1A1A] bg-white px-4 py-3 text-sm leading-relaxed text-[#3A3530] outline-none transition-shadow placeholder:text-[#9E9186] focus:ring-4 focus:ring-[#F26B1F]/15"
          />
          <div className="mt-1.5 flex items-start justify-between gap-4 text-xs text-[#7A7068]">
            <p>At least {MIN_MESSAGE_LENGTH} characters.</p>
            <p aria-live="polite">{message.length}/{MAX_MESSAGE_LENGTH}</p>
          </div>

          <label className="mt-5 flex cursor-pointer items-start gap-3 border-t border-[#DDD8D2] pt-4 text-sm text-[#3A3530] dark:border-zinc-700 dark:text-zinc-300">
            <input
              type="checkbox"
              checked={includeContext}
              onChange={event => setIncludeContext(event.target.checked)}
              className="mt-0.5 h-4 w-4 accent-[#F26B1F]"
            />
            <span>
              <span className="font-semibold">Include where I was in the app</span>
              <span className="mt-0.5 block text-xs leading-relaxed text-[#7A7068] dark:text-zinc-500">
                This adds the page name so we can find the problem. It does not add your account details.
              </span>
            </span>
          </label>

          <p className="mt-5 border-t border-[#DDD8D2] pt-4 text-xs leading-relaxed text-[#706A64] dark:border-zinc-700 dark:text-zinc-400">
            We do not automatically attach your name, email, school or account ID. Your words are stored as written, so please do not include personal information in your message.
          </p>

          {error && <p className="mt-3 text-sm font-medium text-red-700" role="alert">{error}</p>}

          <div className="mt-6 flex items-center justify-end gap-3">
            <button
              type="button"
              onClick={close}
              disabled={isSubmitting}
              className="rounded-full px-4 py-2.5 text-sm font-semibold text-[#706A64] disabled:opacity-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={message.trim().length < MIN_MESSAGE_LENGTH || isSubmitting}
              className="flex min-w-44 items-center justify-center gap-2 rounded-full border-0 border-b-[3px] border-[#B54D14] bg-[#F26B1F] px-6 py-3 text-sm font-bold text-white shadow-[0_4px_0_#B54D14] transition-transform active:translate-y-[3px] active:shadow-none disabled:cursor-not-allowed disabled:opacity-45 disabled:active:translate-y-0 disabled:active:shadow-[0_4px_0_#B54D14]"
            >
              {isSubmitting && <LoaderCircle size={16} className="animate-spin" />}
              {isSubmitting ? 'Sending…' : 'Send anonymously'}
            </button>
          </div>
        </form>
      )}
    </ModalFrame>
  );
};

export default FeedbackModal;
