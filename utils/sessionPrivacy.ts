/** Clear account-linked browser state when a person leaves a shared device. */
export async function clearLocalSessionData(): Promise<void> {
  try { window.localStorage.clear(); } catch { /* Storage may be unavailable. */ }
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
