/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { lockBodyScroll } from '../utils/bodyScrollLock';
import { useEffect, useRef, type RefObject } from 'react';

interface ModalOptions {
  closeDisabled?: boolean;
  initialFocus?: 'first' | 'dialog';
}
const activeModals: symbol[] = [];

/** True while a dialog or sheet that takes Escape for itself is open (area 8a: an over-screen
 *  under it leaves the key to it, as OverScreen's contract says). */
export function hasOpenModal(): boolean {
  return activeModals.length > 0;
}
/** Whether the student's last act was a key press. A dialog or sheet that opens by itself (the island
 *  welcome on a first visit) or from a tap still takes focus, but quietly: the ring is for the
 *  keyboard, so it shows again on the next key press (area 9; SWEEP, the ring on a sheet's Close). */
let keyboardLast = false;
const QUIET = 'data-quiet-focus';
if (typeof window !== 'undefined') {
  window.addEventListener('pointerdown', () => { keyboardLast = false; }, true);
  window.addEventListener('keydown', () => {
    keyboardLast = true;
    document.querySelectorAll(`[${QUIET}]`).forEach(el => el.removeAttribute(QUIET));
  }, true);
}
function placeFocus(target: HTMLElement) {
  if (!keyboardLast) {
    target.setAttribute(QUIET, '');
    target.addEventListener('blur', () => target.removeAttribute(QUIET), { once: true });
  }
  target.focus();
}
const focusableSelector = 'button:not([disabled]), a[href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';

/** One focus owner, scroll lock and dismissal contract for every modal. */
export function useModal(isOpen: boolean, onClose: () => void, dialogRef?: RefObject<HTMLElement | null>, options: ModalOptions = {}) {
  const latest = useRef({ onClose, ...options });
  latest.current = { onClose, ...options };
  useEffect(() => {
    if (!isOpen) return;
    const token = Symbol('modal');
    const previousFocus = document.activeElement instanceof HTMLElement ? document.activeElement : null;
    const releaseScroll = lockBodyScroll();
    activeModals.push(token);
    const isTop = () => activeModals.at(-1) === token;
    const getDialog = () => dialogRef?.current ?? Array.from(document.querySelectorAll<HTMLElement>('[role="dialog"][aria-modal="true"]')).at(-1);
    const controls = (dialog: HTMLElement) => Array.from(dialog.querySelectorAll<HTMLElement>(focusableSelector)).filter(el => {
      const style = getComputedStyle(el);
      return !el.closest('[hidden], [inert], [aria-hidden="true"]') && style.display !== 'none' && style.visibility !== 'hidden';
    });
    let focusFrame = 0;
    const portalFrame = requestAnimationFrame(() => {
      focusFrame = requestAnimationFrame(() => {
        if (!isTop()) return;
        const dialog = getDialog();
        if (dialog?.contains(document.activeElement)) return;
        if (dialog) placeFocus(latest.current.initialFocus === 'dialog' ? dialog : controls(dialog)[0] ?? dialog);
      });
    });
    const handleKeyDown = (event: KeyboardEvent) => {
      if (!isTop() || event.defaultPrevented) return;
      if (event.key === 'Escape') {
        event.preventDefault();
        event.stopPropagation();
        if (!latest.current.closeDisabled) latest.current.onClose();
        return;
      }
      if (event.key !== 'Tab') return;
      const dialog = getDialog();
      if (!dialog) return;
      const focusable = controls(dialog);
      if (!focusable.length) { event.preventDefault(); dialog.focus(); return; }
      const first = focusable[0], last = focusable[focusable.length - 1];
      const active = document.activeElement;
      if (active === dialog || !dialog.contains(active)) {
        event.preventDefault(); (event.shiftKey ? last : first).focus();
      } else if (event.shiftKey && active === first) {
        event.preventDefault(); last.focus();
      } else if (!event.shiftKey && active === last) {
        event.preventDefault(); first.focus();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => {
      const wasTop = isTop();
      activeModals.splice(activeModals.indexOf(token), 1);
      window.removeEventListener('keydown', handleKeyDown);
      cancelAnimationFrame(portalFrame);
      cancelAnimationFrame(focusFrame);
      releaseScroll();
      if (wasTop && previousFocus?.isConnected) previousFocus.focus();
    };
  }, [dialogRef, isOpen]);
}
