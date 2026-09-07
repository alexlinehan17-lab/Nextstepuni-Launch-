/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The width a real app surface is laid out at before being scaled to fit.
 * The app's own breakpoints read window.matchMedia, so on a wide window we
 * lay the surface out at desktop width (and scale it down); on anything
 * narrower we let it lay out natively at the host's width, no scaling.
 */

import { useEffect, useState } from 'react';

export const DESKTOP_LOGICAL = 1200;

export const useLogicalWidth = (hostWidth: number): number => {
  const [wide, setWide] = useState(() => typeof window !== 'undefined' && window.matchMedia('(min-width: 1200px)').matches);
  useEffect(() => {
    const mq = window.matchMedia('(min-width: 1200px)');
    const sync = () => setWide(mq.matches);
    mq.addEventListener('change', sync);
    return () => mq.removeEventListener('change', sync);
  }, []);
  return wide ? DESKTOP_LOGICAL : Math.max(320, hostWidth);
};
