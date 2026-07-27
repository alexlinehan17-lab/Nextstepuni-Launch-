/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * How to write to Firestore in this app — and why you must not `await` it.
 *
 * ─── THE RULE ──────────────────────────────────────────────────────────────
 *
 *   NEVER gate UI on a Firestore write promise.
 *
 * `firebase.ts` initialises Firestore with `persistentLocalCache`. Under the
 * SDK's write semantics, the promise returned by setDoc / updateDoc / addDoc /
 * deleteDoc / batch.commit() resolves only when the write is acknowledged by
 * the SERVER. The write reaches the local cache immediately and is flushed on
 * reconnect — but while the client is offline the promise NEITHER RESOLVES NOR
 * REJECTS. It stays pending indefinitely.
 *
 * So this shape is a silent, permanent hang:
 *
 *     await setDoc(ref, data, { merge: true });
 *     setSaving(false);        // never runs offline — button stuck on "Saving…"
 *     onClose();               // never runs offline — modal never closes
 *     nav.navigateToTree();    // never runs offline — student stranded
 *
 * A try/catch does not help: nothing is thrown. Neither does `finally`.
 *
 * This is not theoretical for this product. The users are secondary-school
 * students on school wifi and patchy mobile data, and the app also ships as a
 * native iOS app via Capacitor. Worse, a captive portal or a dead uplink keeps
 * `navigator.onLine === true`, so the offline banner does not fire either — the
 * app looks online and simply stops responding.
 *
 * ─── WHAT TO DO INSTEAD ────────────────────────────────────────────────────
 *
 * Update local state FIRST, fire the write, and undo only on a real rejection:
 *
 *     const previous = value;
 *     setValue(next);                                     // instant, offline-safe
 *     saveInBackground(
 *       setDoc(ref, data, { merge: true }),
 *       'Thing.save',
 *       () => setValue(previous),                         // real rejection only
 *     );
 *
 * A rejection here means a genuine failure — security-rules denial, malformed
 * data, quota — never "the user is offline". That distinction is the whole
 * point: offline is the normal case and must not look like an error, while a
 * rules denial must not hide behind "check your connection".
 *
 * If a flow genuinely cannot continue until the data is durable, use
 * `awaitWriteOrTimeout` so the UI still moves on after a bounded wait.
 */

import { reportSaveError, logError } from './logError';

/**
 * Fire a Firestore write without gating the UI on it.
 *
 * @param write    the promise returned by setDoc/updateDoc/addDoc/deleteDoc/commit
 * @param context  stable "Area.action" label for logs, e.g. 'App.saveNorthStar'
 * @param rollback optional undo, run ONLY if the write is genuinely rejected
 * @param opts.silent  log without raising a toast (best-effort/background writes)
 */
export function saveInBackground(
  write: Promise<unknown>,
  context: string,
  rollback?: () => void,
  opts: { silent?: boolean } = {},
): void {
  write.catch((err: unknown) => {
    if (opts.silent) logError(context, err);
    else reportSaveError(context, err);
    try {
      rollback?.();
    } catch (rollbackErr) {
      logError(`${context}.rollback`, rollbackErr);
    }
  });
}

/** Outcome of a bounded wait on a write. */
export type WriteOutcome = 'acked' | 'pending' | 'failed';

/**
 * Await a write, but never longer than `timeoutMs`.
 *
 * For the rare flow that must not continue until the data is durable — and
 * even then, the caller must handle `'pending'` by carrying on rather than
 * blocking, because offline that is the permanent answer.
 *
 * `'pending'` does NOT mean the write was lost: it is queued in the local cache
 * and will flush on reconnect. It only means we stopped waiting.
 */
export async function awaitWriteOrTimeout(
  write: Promise<unknown>,
  context: string,
  timeoutMs: number = 4000,
): Promise<WriteOutcome> {
  let timer: ReturnType<typeof setTimeout> | undefined;
  const timeout = new Promise<WriteOutcome>(resolve => {
    timer = setTimeout(() => resolve('pending'), timeoutMs);
  });
  const acked = write.then<WriteOutcome, WriteOutcome>(
    () => 'acked',
    (err: unknown) => {
      logError(context, err);
      return 'failed';
    },
  );
  try {
    return await Promise.race([acked, timeout]);
  } finally {
    if (timer !== undefined) clearTimeout(timer);
  }
}
