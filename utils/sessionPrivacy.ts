// CERTLE is an anonymous browser game, independent of the signed-in account.
// Keep only its documented keys on an unauthenticated boot, never on logout,
// password reset or account deletion. Do not preserve arbitrary namespace keys.
const isPublicGameKey = (key: string): boolean =>
  ['nextstepuni.certle.v2', 'nextstepuni.certle.stats.v1', 'landing.today.v1'].includes(key)
  || /^nextstepuni\.certle\.draft:\d{4}-\d{2}-\d{2}:[a-z0-9_-]+$/i.test(key);

/** Clear account-linked browser state when a person leaves a shared device. */
export async function clearLocalSessionData(
  { preservePublicGames = false }: { preservePublicGames?: boolean } = {},
): Promise<void> {
  try {
    if (preservePublicGames) {
      const storage = window.localStorage;
      for (let i = storage.length - 1; i >= 0; i--) {
        const key = storage.key(i);
        if (key !== null && !isPublicGameKey(key)) storage.removeItem(key);
      }
    } else {
      window.localStorage.clear();
    }
  } catch { /* Storage may be unavailable. */ }
  try { window.sessionStorage.clear(); } catch { /* Storage may be unavailable. */ }

  // Oral practice audio is intentionally device-only and therefore must not
  // remain available to the next person using the same browser profile.
  if (typeof indexedDB !== 'undefined') {
    await new Promise<void>(resolve => {
      const request = indexedDB.deleteDatabase('oral-trainer-takes');
      request.onsuccess = () => resolve();
      request.onerror = () => resolve();
      request.onblocked = () => resolve();
    });
  }
}
