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
 * `overlay` covers the viewport. The provisioning hold needs that: rendering a
 * bare inline spinner there left the app header and points pill visible behind
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
    <div className="nsu-loader-in w-full max-w-xs">
      <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-[var(--ink-muted)]">{kicker}</p>
      <p className="mt-3 font-serif text-[22px] font-semibold leading-snug text-[var(--ink-primary)]">{label}</p>
      {/* Decorative: the copy above already announces the state to assistive
          tech, and a second live description of a spinner is noise. */}
      <div className="nsu-loader-rail mx-auto mt-6" aria-hidden="true">
        <span className="nsu-loader-sweep nsu-loader-sweep--echo" />
        <span className="nsu-loader-sweep nsu-loader-sweep--lead" />
      </div>
    </div>
  </div>
);
