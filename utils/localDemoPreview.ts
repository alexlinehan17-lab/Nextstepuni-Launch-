import { Capacitor } from '@capacitor/core';

/** Only the explicit localhost development preview opens sample data automatically. */
export function isLocalDemoPreview(): boolean {
  if (!import.meta.env.DEV || typeof window === 'undefined' || Capacitor.isNativePlatform()) return false;
  if (!/^(localhost|127\.0\.0\.1|\[::1\])$/.test(window.location.hostname)) return false;
  try {
    return window.frameElement?.getAttribute('data-demo-account') === 'true';
  } catch {
    return false;
  }
}
