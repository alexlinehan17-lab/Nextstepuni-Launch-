/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Onboarding follows the phone's dark setting (r5-onboarding, agreed 26 Nov
 * 2026; until then it was always light): true when the device prefers dark,
 * or the app is already in dark mode. The orange pages stay orange either way.
 */
import { useEffect, useState } from 'react';

const QUERY = '(prefers-color-scheme: dark)';

function read(): boolean {
  if (typeof window === 'undefined') return false;
  const prefers = typeof window.matchMedia === 'function' && window.matchMedia(QUERY).matches;
  return prefers || document.documentElement.classList.contains('dark');
}

export function useFlowDark(): boolean {
  const [dark, setDark] = useState(read);
  useEffect(() => {
    if (typeof window === 'undefined') return undefined;
    const update = () => setDark(read());
    const media = typeof window.matchMedia === 'function' ? window.matchMedia(QUERY) : null;
    media?.addEventListener?.('change', update);
    const observer = new MutationObserver(update);
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });
    return () => {
      media?.removeEventListener?.('change', update);
      observer.disconnect();
    };
  }, []);
  return dark;
}
