/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The three states every screen that loads data owes the student
 * (components.md, "States"; the kit's .empty and the loading and error
 * specimens). None is left blank, and none is a dead end.
 *
 *   <EmptyState art="/assets/star-crew/personal/11-snoozer.png" title="There's room to rest."
 *     line="Your next blocks will appear here." action={<Button kind="main" arrow="forward" onClick={plan}>Plan your week</Button>} />
 *   <LoadingShape rows={3} label="Loading your plan" />        nothing for 300ms, then grey shapes where the rows will be
 *   <ErrorState sentence="We couldn't save your setup. Your answers are still here." onRetry={save} />
 *
 * The full-screen Star Crew loader (LoadingSpinner) stays for app launch and
 * route changes; this shape is for inside a screen whose layout is known.
 * Migration: CrewEmptyState, StatePanel / LoadingState and the per-screen
 * empty, loading and error sentences move onto these screen by screen.
 */
import { useEffect, useState, type ReactNode } from 'react';
import { Button } from './Button';
import ThemeArtwork from '../ThemeArtwork';
import './parts.css';

export interface EmptyStateProps {
  /** One Star Crew character, bare, no tile. */
  art?: string;
  /** Its size: 96 or smaller. */
  artSize?: 56 | 72 | 96;
  title: ReactNode;
  /** One plain line saying what will appear here. */
  line?: ReactNode;
  /** One action that makes it non-empty (usually a main Button). */
  action?: ReactNode;
  className?: string;
}

/** Laid on the page: it paints no background of its own. */
export function EmptyState({ art, artSize = 96, title, line, action, className = '' }: EmptyStateProps) {
  return (
    <div className={`ui-part ui-empty ${className}`.trim()}>
      {art ? <ThemeArtwork className="ui-empty-art" src={art} transparentBackground alt="" width={artSize} height={artSize} /> : null}
      <h3 className="ui-empty-title">{title}</h3>
      {line ? <p className="ui-empty-line">{line}</p> : null}
      {action ?? null}
    </div>
  );
}

/** Nothing for the first 300ms (motion.md, "Loading"). */
const QUIET_MS = 300;

export interface LoadingShapeProps {
  /** How many rows the content will have. */
  rows?: number;
  /** What is loading, for screen readers ("Loading your plan"). */
  label: string;
  /** Show the shape at once (for a picture of it). */
  immediate?: boolean;
  className?: string;
}

/** The loading shape: grey rows where the content will be. No spinner, nothing that pulses. */
export function LoadingShape({ rows = 3, label, immediate = false, className = '' }: LoadingShapeProps) {
  const [shown, setShown] = useState(immediate);
  useEffect(() => {
    if (immediate) return;
    const timer = window.setTimeout(() => setShown(true), QUIET_MS);
    return () => window.clearTimeout(timer);
  }, [immediate]);
  return (
    <div className={`ui-part ${className}`.trim()} role="status" aria-label={label} aria-busy="true">
      {shown ? (
        <div className="ui-skel" aria-hidden="true">
          {Array.from({ length: rows }, (_, index) => (
            <div key={index} className="ui-skel-row">
              <i className="ui-skel-bar" style={{ width: index % 2 ? '34%' : '46%' }} />
              <i className="ui-skel-bar ui-skel-bar--sub" style={{ width: index % 2 ? '58%' : '72%' }} />
            </div>
          ))}
        </div>
      ) : null}
    </div>
  );
}

export interface ErrorStateProps {
  /** An ink sentence: what happened, and (after a failed save) that the work is still there. */
  sentence: ReactNode;
  /** The way out. */
  onRetry?: () => void;
  retryLabel?: string;
  /** Or another way out (a Button), instead of Try again. */
  action?: ReactNode;
  className?: string;
}

/** Where it happened: no red box, no browser alert. */
export function ErrorState({ sentence, onRetry, retryLabel = 'Try again', action, className = '' }: ErrorStateProps) {
  return (
    <div className={`ui-part ui-error ${className}`.trim()} role="alert">
      <p className="ui-error-text">{sentence}</p>
      {action ?? (onRetry ? <Button onClick={onRetry}>{retryLabel}</Button> : null)}
    </div>
  );
}
