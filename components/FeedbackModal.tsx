/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Anonymous, in-app product feedback. Account identity is used transiently by
 * the callable function for authentication and rate limiting, but is never
 * written to the feedback record shown in the admin inbox.
 */

import React, { useEffect, useRef, useState } from 'react';
import { LoaderCircle } from 'lucide-react';
import { getFunctions, httpsCallable } from 'firebase/functions';
import app from '../firebase';
import {
  FEEDBACK_CATEGORIES,
  getFeedbackPlatform,
  type FeedbackCategory,
} from '../utils/anonymousFeedback';
import ModalFrame from './ui/ModalFrame';
import './feedback-listening-room.css';

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
const LISTENER_IMAGE = '/assets/star-crew/companions/listener-transparent.png';
const CATEGORY_ORDER = ['idea' as const, ...FEEDBACK_CATEGORIES.filter(category => category !== 'idea')];
const CATEGORY_COPY: Record<FeedbackCategory, { label: string; prompt: string }> = {
  idea: { label: 'I have an idea', prompt: 'What would you like to see? How would it help you?' },
  broken: { label: 'Something isn’t working', prompt: 'What were you trying to do? What happened instead?' },
  confusing: { label: 'Something’s confusing', prompt: 'Where did you get stuck? What would make it clearer?' },
  other: { label: 'Something else', prompt: 'The good bits, the little frustrations — we’re listening.' },
};

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
  const [category, setCategory] = useState<FeedbackCategory>('idea');
  const [message, setMessage] = useState('');
  const [includeContext, setIncludeContext] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSent, setIsSent] = useState(false);
  const [error, setError] = useState('');
  const successRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (isSent) successRef.current?.focus();
  }, [isSent]);

  useEffect(() => {
    if (!open) return;
    setCategory('idea');
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
      title="Help us improve"
      width="xl"
      labelledBy="anonymous-feedback-title"
      variant="listening-room"
      closeDisabled={isSubmitting}
    >
      {isSent ? (
        <div className="feedback-thanks" ref={successRef} tabIndex={-1} role="status">
          <p className="feedback-eyebrow">A little better, together.</p>
          <img src={LISTENER_IMAGE} alt="The Listener sitting on an orange star" width={220} height={220} />
          <h3>Thanks for<br />having your say.</h3>
          <p>Ideas, frustrations and small fixes — they all help us decide what to improve next.</p>
          <p className="feedback-sent-note">Sent without account details.</p>
          <button type="button" onClick={onClose} className="feedback-primary">
            Back to my study <span aria-hidden="true">↗</span>
          </button>
        </div>
      ) : (
        <div className="feedback-split">
          <aside className="feedback-welcome">
            <p className="feedback-eyebrow">Help us improve</p>
            <h3>A little thought.<br />A better<br />next step.</h3>
            <p className="feedback-lead">Tell us what helps, what gets in the way, or what you wish was here.</p>
            <img src={LISTENER_IMAGE} alt="The Listener, a Star Crew companion with a hand cupped beside its head" width={270} height={270} />
            <p className="feedback-companion-caption">A little better, together.</p>
          </aside>
          <form className="feedback-form" onSubmit={submit} aria-busy={isSubmitting}>
            <h3>What would make it better?</h3>
            <p className="feedback-form-intro">A good idea can start with one small thing.</p>
            <fieldset className="feedback-categories" disabled={isSubmitting}>
              <legend>What’s on your mind?</legend>
              <div className="feedback-category-grid">
                {CATEGORY_ORDER.map(option => (
                  <label className="feedback-category" key={option}>
                    <input
                      type="radio"
                      name="feedback-category"
                      value={option}
                      checked={category === option}
                      onChange={() => setCategory(option)}
                    />
                    <span>
                      {CATEGORY_COPY[option].label}
                      <i aria-hidden="true">{category === option ? '●' : '+'}</i>
                    </span>
                  </label>
                ))}
              </div>
            </fieldset>
            <label className="feedback-message-label" htmlFor="anonymous-feedback-message">Your words. We’re listening.</label>
            <textarea
              id="anonymous-feedback-message"
              value={message}
              onChange={event => setMessage(event.target.value)}
              minLength={MIN_MESSAGE_LENGTH}
              maxLength={MAX_MESSAGE_LENGTH}
              rows={4}
              required
              disabled={isSubmitting}
              placeholder={CATEGORY_COPY[category].prompt}
              aria-describedby={`feedback-message-hint${error ? ' feedback-error' : ''}`}
            />
            <div className="feedback-message-meta">
              <p id="feedback-message-hint">A sentence or two. At least {MIN_MESSAGE_LENGTH} characters.</p>
              <p>{message.length.toLocaleString()} / 2,000</p>
            </div>
            <label className="feedback-context">
              <input type="checkbox" checked={includeContext} disabled={isSubmitting} onChange={event => setIncludeContext(event.target.checked)} />
              <span>Include the page I’m on<small>Helps us understand where this happened.</small></span>
            </label>
            <p className="feedback-privacy">
              Your name, email, school and account ID aren’t attached. Your words are shared as written, so leave personal details out.
            </p>
            {error && <p id="feedback-error" className="feedback-error" role="alert">{error}</p>}
            <button type="submit" disabled={message.trim().length < MIN_MESSAGE_LENGTH || isSubmitting} className="feedback-primary">
              <span>{isSubmitting ? 'Sending…' : 'Send anonymously'}</span>
              {isSubmitting ? <LoaderCircle size={19} className="animate-spin" aria-hidden="true" /> : <span aria-hidden="true">↗</span>}
            </button>
          </form>
        </div>
      )}
    </ModalFrame>
  );
};

export default FeedbackModal;
