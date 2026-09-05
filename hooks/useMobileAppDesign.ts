import { useSyncExternalStore } from 'react';
import { Capacitor } from '@capacitor/core';

/** This rollout is device-scoped, not a desktop redesign at a smaller width.
 * iPads using desktop-class Safari still identify through Mac + multi-touch.
 * Only the local development review iframe can explicitly preview a device.
 */
export function isMobileAppDesign(): boolean {
  if (typeof window === 'undefined') return false;
  if ((import.meta as ImportMeta & { env?: { DEV?: boolean } }).env?.DEV) {
    try {
      const preview = window.frameElement?.getAttribute('data-app-preview');
      if (preview === 'desktop') return false;
      if (preview === 'mobile') return true;
    } catch { /* Cross-origin frames cannot opt in. */ }
  }
  if (Capacitor.isNativePlatform()) return true;
  if (/Android|iPhone|iPad|iPod/i.test(navigator.userAgent)) return true;
  return /Mac/i.test(navigator.platform) && navigator.maxTouchPoints > 1;
}

const subscribe = (update: () => void) => {
  window.addEventListener('resize', update);
  return () => window.removeEventListener('resize', update);
};

export function useMobileAppDesign() {
  return useSyncExternalStore(subscribe, isMobileAppDesign, () => false);
}
