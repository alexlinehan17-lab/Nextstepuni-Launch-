import React, { useLayoutEffect, useRef } from 'react';
import { createPortal } from 'react-dom';
import { ArrowRight, X } from 'lucide-react';
import CrewIllustration from '../CrewIllustration';
import { useModal } from '../../hooks/useModal';
import { useReducedMotion } from '../Motion';
import './study-quiz-invitation.css';

interface Props {
  subject: string;
  topicLabel?: string;
  questionCount: number;
  hasStudiedTopics: boolean;
  character?: string;
  onAccept: () => void;
  onDecline: () => void;
  onOpen?: () => void;
}

/** A separate, optional step after the receipt is saved, before the final screen. */
export default function StudyQuizInvitation({ subject, topicLabel, questionCount, hasStudiedTopics, character, onAccept, onDecline, onOpen }: Props) {
  const dialogRef = useRef<HTMLDivElement>(null);
  const overlayRef = useRef<HTMLDivElement>(null);
  const announced = useRef(false);
  const reduced = useReducedMotion();
  useModal(true, onDecline, dialogRef, { initialFocus: 'dialog' });
  useLayoutEffect(() => {
    if (announced.current) return;
    announced.current = true;
    if (!document.hidden) onOpen?.();
  }, [onOpen]);
  useLayoutEffect(() => {
    const overlay = overlayRef.current, dialog = dialogRef.current;
    if (!overlay?.animate || !dialog?.animate) return;
    const quiet = reduced || document.hidden;
    const options = { duration: quiet ? 120 : 600, easing: 'cubic-bezier(.22,1,.36,1)', fill: 'both' as const };
    const animations = [
      overlay.animate([{ opacity: 0 }, { opacity: 1 }], { ...options, duration: quiet ? 120 : 320 }),
      dialog.animate(quiet ? [{ opacity: 0 }, { opacity: 1 }] : [
        { opacity: 0, transform: 'translateY(16px) scale(.985)' },
        { opacity: 1, transform: 'translateY(0) scale(1)' },
      ], options),
    ];
    let settled = false;
    const clean = () => { if (!settled) { settled = true; animations.forEach(animation => animation.cancel()); } };
    const timer = window.setTimeout(clean, options.duration + 200);
    void Promise.all(animations.map(animation => animation.finished.catch(() => {}))).then(() => { window.clearTimeout(timer); clean(); });
    return () => { window.clearTimeout(timer); clean(); };
  }, [reduced]);

  return createPortal(
    <div ref={overlayRef} className="sqi-overlay" data-lenis-prevent onClick={event => { if (event.target === event.currentTarget) onDecline(); }}>
      <div ref={dialogRef} className="sqi-dialog" role="dialog" aria-modal="true" tabIndex={-1}
        aria-labelledby="study-invitation-title" aria-describedby="study-invitation-description">
        <header className="sqi-header">
          <span className="sqi-brand">nextstepuni</span>
          <button type="button" className="sqi-close" aria-label="Not now, show my saved session" onClick={onDecline}><X size={18} aria-hidden="true" /></button>
        </header>
        <div className="sqi-body">
          <div className="sqi-story">
            <p className="sqi-eyebrow">One last thing, if you like</p>
            <h2 id="study-invitation-title">What stayed<br /> with you?</h2>
            <div className="sqi-art" aria-hidden="true"><CrewIllustration character={character} /></div>
          </div>
          <div className="sqi-choice">
            <p id="study-invitation-description" className="sqi-question">{hasStudiedTopics ? 'Would you like to try a few questions on the topics you studied?' : `Would you like to try a few ${subject} questions?`}</p>
            <div className="sqi-topic"><strong>{topicLabel || subject}</strong><span>{questionCount} {questionCount === 1 ? 'question' : 'questions'}</span></div>
            <p className="sqi-note">Answer first, then check your work against the official marking scheme.</p>
            <div className="sqi-actions">
              <button type="button" className="sqi-accept" onClick={onAccept}>Yes, test me <ArrowRight size={18} aria-hidden="true" /></button>
              <button type="button" className="sqi-decline" onClick={onDecline}>Not now</button>
            </div>
            <p className="sqi-reassurance">Your study time and Journey Points are already saved.</p>
          </div>
        </div>
      </div>
    </div>
  , document.body);
}
