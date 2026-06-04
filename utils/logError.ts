/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Shared error reporting for the data layer.
 *
 * Before this, dozens of Firestore reads/writes swallowed their errors with
 * `.catch(() => {})` — so a failed save looked identical to a successful one,
 * and a failed read produced a blank screen with no signal. (Audit 2026-06-04,
 * M7–M15.) These two helpers replace the silent swallows:
 *
 *   • logError(context, err)        — always console.errors with a stable,
 *     greppable `[context]` prefix. Use for READ failures and best-effort
 *     fire-and-forget writes where a null/empty fallback is acceptable but the
 *     failure should still be visible in the console / remote logs.
 *
 *   • reportSaveError(context, err) — logs AND signals the UI to surface a
 *     "couldn't save" toast, so the student knows their change may not have
 *     persisted. Use for user-initiated WRITES (setDoc/updateDoc/etc.).
 *
 * The toast is delivered via a window CustomEvent so the data layer (hooks,
 * contexts, plain async functions) can trigger it without holding the React
 * Toast context. `ToastProvider` listens for SAVE_ERROR_EVENT and shows the
 * toast (see components/Toast.tsx).
 */

/** Window event name the ToastProvider listens for to surface a save-failure toast. */
export const SAVE_ERROR_EVENT = 'app:save-error';

export interface SaveErrorDetail {
  /** Short "Area.action" label, e.g. "useExamReps.saveCard". */
  context: string;
  /** Optional override for the toast copy. */
  message?: string;
}

/**
 * Log an error with a stable, greppable prefix. Never throws. Safe to call
 * from anywhere (no React/DOM dependency beyond `console`).
 */
export function logError(context: string, err: unknown): void {
  console.error(`[${context}]`, err);
}

/**
 * Report a user-initiated WRITE failure: log it, and ask the UI to show a
 * "couldn't save" toast. Pass `message` to override the default copy.
 */
export function reportSaveError(context: string, err: unknown, message?: string): void {
  logError(context, err);
  if (typeof window !== 'undefined' && typeof window.dispatchEvent === 'function') {
    window.dispatchEvent(
      new CustomEvent<SaveErrorDetail>(SAVE_ERROR_EVENT, { detail: { context, message } }),
    );
  }
}
