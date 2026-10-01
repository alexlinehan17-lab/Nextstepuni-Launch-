/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useEffect, useRef, type RefObject } from 'react';

interface ModalOptions {
  closeDisabled?: boolean;
  initialFocus?: 'first' | 'dialog';
}
const activeModals: symbol[] = [];
let savedOverflow = '';
const focusableSelector = 'button:not([disabled]), a[href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';

/** One focus owner, scroll lock and dismissal contract for every modal. */
export function useModal(isOpen: boolean, onClose: () => void, dialogRef?: RefObject<HTMLElement | null>, options: ModalOptions = {}) {
  const latest = useRef({ onClose, ...options });
  latest.current = { onClose, ...options };
  useEffect(() => {
    if (!isOpen) return;
    const token = Symbol('modal');
    const previousFocus = document.activeElement instanceof HTMLElement ? document.activeElement : null;
    if (activeModals.length === 0) {
      savedOverflow = document.body.style.overflow;
      document.body.style.overflow = 'hidden';
    }
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
        if (dialog) (latest.current.initialFocus === 'dialog' ? dialog : controls(dialog)[0] ?? dialog).focus();
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
      if (activeModals.length === 0) document.body.style.overflow = savedOverflow;
      if (wasTop && previousFocus?.isConnected) previousFocus.focus();
    };
  }, [dialogRef, isOpen]);
}
