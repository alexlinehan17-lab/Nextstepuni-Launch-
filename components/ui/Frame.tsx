/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The React half of the frame (the CSS half, with the rules, is ./frame.css).
 *
 * Layout primitives, by class name:
 *   frame-bar            a top bar: pads itself by the top inset; 44px hit areas
 *   frame-page           a page with no bar: pads its top by the inset
 *   frame-foot           anything ending at the bottom of the glass
 *   frame-takeover       full screen, edge to edge
 *   frame-safe-box       inside a takeover: the box controls are pinned in
 *   frame-dialog         dialog backdrop; frame-dialog-card for its card;
 *                        frame-dialog-native for a showModal() <dialog>;
 *                        frame-dialog-head for its header (44px hit areas)
 *   frame-sheet-backdrop / frame-sheet   bottom sheet below 640px, dialog above
 *   frame-float (+ -top -bottom -left -right)   toasts, mini timer, banners
 *   frame-hit            a 44 x 44 hit area on any one control
 * Variables: --safe-top/-right/-bottom/-left, --safe-h, --tabbar-h,
 * --edge-top, --edge-bottom, and the stacking order --z-sticky ... --z-system.
 */

import { useEffect, type ReactNode } from 'react';
import { createPortal } from 'react-dom';

/** Every overlay renders at the end of <body>, so no host's stacking context
 *  can trap it under a bar or the tab bar. */
export function FramePortal({ children }: { children: ReactNode }) {
  if (typeof document === 'undefined') return null;
  return createPortal(children, document.body);
}

export interface SafeArea { top: number; right: number; bottom: number; left: number }
let safeAreaCache: SafeArea | null = null;
let safeAreaListening = false;

/** The safe-area insets in CSS pixels, for code that places something itself
 *  (a caption, a popover). Measured once, again after a resize or rotation. */
export function readSafeArea(): SafeArea {
  if (typeof document === 'undefined' || !document.body) return { top: 0, right: 0, bottom: 0, left: 0 };
  if (safeAreaCache) return safeAreaCache;
  const probe = document.createElement('div');
  probe.style.cssText = 'position:fixed;top:0;left:0;width:0;height:0;visibility:hidden;pointer-events:none;'
    + 'padding:var(--safe-top) var(--safe-right) var(--safe-bottom) var(--safe-left)';
  document.body.appendChild(probe);
  const style = getComputedStyle(probe);
  safeAreaCache = {
    top: parseFloat(style.paddingTop) || 0,
    right: parseFloat(style.paddingRight) || 0,
    bottom: parseFloat(style.paddingBottom) || 0,
    left: parseFloat(style.paddingLeft) || 0,
  };
  probe.remove();
  if (!safeAreaListening) {
    safeAreaListening = true;
    window.addEventListener('resize', () => { safeAreaCache = null; });
  }
  return safeAreaCache;
}

let tabBarHolders = 0;

/** Called by the phone tab bar while it is mounted: the frame then knows the
 *  bar's height (--tabbar-h, 50px below 768px) and --edge-bottom clears it. */
export function useFrameTabBar() {
  useEffect(() => {
    const root = document.documentElement;
    tabBarHolders += 1;
    root.setAttribute('data-tabbar', '');
    return () => {
      tabBarHolders = Math.max(0, tabBarHolders - 1);
      if (tabBarHolders === 0) root.removeAttribute('data-tabbar');
    };
  }, []);
}
