

/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import type React from 'react';

/**
 * A quiet but visible Suspense state for slower devices and school networks.
 *
 * `label` exists because the default copy is a RETURNING-user message. A student
 * creating an account has no workspace yet, so "Loading your workspace" during
 * signup is both wrong and slightly alarming when it sits there for a few
 * seconds. Callers on the signup path pass their own wording.
 */
export const LoadingSpinner: React.FC<{ label?: string; kicker?: string }> = ({
  label = 'Loading your workspace',
  kicker = 'Opening',
}) => (
  <div
    role="status"
    aria-live="polite"
    className="theme-compat flex min-h-[45vh] w-full items-center justify-center bg-[var(--surface-canvas)] px-6 text-center"
  >
    <div className="w-full max-w-xs">
      <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-[var(--ink-muted)]">{kicker}</p>
      <p className="mt-3 font-serif text-2xl font-semibold text-[var(--ink-primary)]">{label}</p>
      <div className="mx-auto mt-5 h-px w-20 overflow-hidden bg-[var(--outline-soft)]" aria-hidden="true">
        <div className="h-full w-1/2 animate-pulse bg-[var(--accent-hex)]" />
      </div>
    </div>
  </div>
);
