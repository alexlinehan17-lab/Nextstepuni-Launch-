/**
 * A progress snapshot is safe to render only when it explicitly belongs to the
 * signed-in account. `progressLoaded` alone can still describe the logged-out
 * empty state during the first render of a new login.
 */
export function isProgressReadyForUser(
  uid: string,
  progressLoaded: boolean,
  progressDataUid: string | null,
): boolean {
  return progressLoaded && progressDataUid === uid;
}
