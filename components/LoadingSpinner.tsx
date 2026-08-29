/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import type React from 'react';

/**
 * The app's single loading state.
 *
 * There used to be two. This one, and a hand-rolled spinning circle inside
 * AppRouter's registration hold — which was the one a new student actually sat
 * and watched, and the only screen in the product that looked like a generic
 * app rather than this one. Both now render from here, so the loading moment
 * has a single visual language.
 *
 * `label` exists because the default copy is a RETURNING-user message. A
 * student creating an account has no workspace yet, so "Loading your workspace"
 * during signup is both wrong and slightly alarming when it sits there for a
 * few seconds. Callers on the signup path pass their own wording.
 *
 * The visual is a miniature dashboard assembling itself: Course, Calendar and
 * Progress settle into the same editorial grid the student is about to enter.
 * It is CSS-only so account creation and hydration cannot make the motion
 * stutter while the JavaScript thread is busy. The entrance is also delayed in
 * CSS, which means very short waits finish before any loading chrome flashes.
 *
 * `overlay` covers the viewport. The provisioning hold needs that: rendering a
 * bare inline loader there left the app header and points pill visible behind
 * it, and returning the login form put a sign-in screen inside a signed-in
 * shell, which read as having been logged out.
 */
export const LoadingSpinner: React.FC<{
  label?: string;
  kicker?: string;
  overlay?: boolean;
}> = ({ label = 'Loading your workspace', kicker = 'Opening', overlay = false }) => (
  <div
    role="status"
    aria-live="polite"
    className={[
      'theme-compat flex w-full items-center justify-center bg-[var(--surface-canvas)] px-6 text-center',
      overlay ? 'fixed inset-0 z-[200] h-full' : 'min-h-[45vh]',
    ].join(' ')}
  >
    <div className="nsu-loader-in w-full max-w-[430px]">
      {/* Decorative: the copy below already announces the state to assistive
          tech, and narrating every miniature dashboard card would be noise. */}
      <div className="nsu-dashboard-assembly" aria-hidden="true">
        <div className="nsu-assembly-aura" />
        <div className="nsu-assembly-board">
          <div className="nsu-assembly-masthead">
            <span className="nsu-assembly-mark" />
            <span className="nsu-assembly-wordmark" />
            <span className="nsu-assembly-control" />
            <span className="nsu-assembly-control nsu-assembly-control--quiet" />
          </div>

          <div className="nsu-assembly-grid">
            <div className="nsu-assembly-card nsu-assembly-course" data-loader-card="course">
              <div className="nsu-assembly-card-heading">
                <span className="nsu-assembly-card-dot" />
                <span>Course</span>
              </div>
              <div className="nsu-course-lines">
                <span className="nsu-course-line nsu-course-line--title" />
                <span className="nsu-course-line nsu-course-line--body" />
                <span className="nsu-course-line nsu-course-line--short" />
              </div>
              <div className="nsu-course-track">
                <span className="nsu-course-fill" />
              </div>
            </div>

            <div className="nsu-assembly-card nsu-assembly-calendar" data-loader-card="calendar">
              <div className="nsu-assembly-card-heading">
                <span className="nsu-assembly-card-dot nsu-assembly-card-dot--teal" />
                <span>Calendar</span>
              </div>
              <div className="nsu-calendar-week">
                {['M', 'T', 'W', 'T', 'F'].map((day, index) => (
                  <span key={`${day}-${index}`} className={index === 2 ? 'nsu-calendar-day nsu-calendar-day--active' : 'nsu-calendar-day'}>
                    <span>{day}</span>
                    <i />
                  </span>
                ))}
              </div>
            </div>

            <div className="nsu-assembly-card nsu-assembly-progress" data-loader-card="progress">
              <span className="nsu-progress-ring" />
              <span className="nsu-progress-copy">
                <span className="nsu-progress-label">Progress</span>
                <span className="nsu-progress-line" />
                <span className="nsu-progress-line nsu-progress-line--short" />
              </span>
            </div>
          </div>
        </div>
      </div>

      <div className="nsu-loader-copy">
        <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-[var(--ink-muted)]">{kicker}</p>
        <p className="mt-2.5 font-serif text-[22px] font-semibold leading-snug text-[var(--ink-primary)]">{label}</p>
      </div>
    </div>
  </div>
);
