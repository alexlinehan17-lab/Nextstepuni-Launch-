/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * A screen that comes up over where you were (navigation.md, "Three kinds of
 * screen": an over-screen; components.md, "Full-screen task"): a practice run,
 * a viewer. It fills the window on a phone, its bar (a TopBar with Close)
 * owning the top inset and its footer the bottom one; the tab bar steps aside
 * while it is up. On a laptop it may sit beside sidebar B (`left`), leaving the
 * sidebar in reach, and then it is not modal.
 *
 *   <OverScreen label="Practice: Photosynthesis" onEscape={askBeforeLeaving} left={sidebarEdge} modal={phone}>
 *     <TopBar leave={{ kind: 'close', onPress: askBeforeLeaving }} over="Mark Bank" title="Biology" />
 *     ...the task...
 *   </OverScreen>
 *
 * The house contract, as the dialog it replaces kept it: the page behind is
 * still, focus moves in (to the leave control) and goes back to what opened it,
 * and Escape calls onEscape. A layer opened inside it that takes Escape for
 * itself (a figure enlarged, a source page) stops the key before it arrives.
 */
import React, { useEffect, useRef, type CSSProperties, type ReactNode } from 'react';
import { FramePortal, useFrameTask } from './Frame';
import { lockBodyScroll } from '../../utils/bodyScrollLock';
import { hasOpenModal } from '../../hooks/useModal';
import './parts.css';

export interface OverScreenProps {
  /** Its accessible name. */
  label: string;
  /** Escape, unless something inside took it first. */
  onEscape: () => void;
  /** It covers the whole window (a phone, or a laptop task expanded): aria-modal. Default true. */
  modal?: boolean;
  /** Where it starts from the left, in px: sidebar B's edge on a laptop. Default 0. */
  left?: number;
  className?: string;
  children: ReactNode;
  /** Extra data attributes (a screen's own state, for its stylesheet and its tests). */
  [data: `data-${string}`]: string | boolean | undefined;
}

export const OverScreen = React.forwardRef<HTMLDivElement, OverScreenProps>(function OverScreen(
  { label, onEscape, modal = true, left = 0, className = '', children, ...data },
  ref,
) {
  const own = useRef<HTMLDivElement | null>(null);
  const escape = useRef(onEscape);
  escape.current = onEscape;
  useFrameTask(true);
  useEffect(() => {
    const previous = document.activeElement instanceof HTMLElement ? document.activeElement : null;
    const release = lockBodyScroll();
    const frame = requestAnimationFrame(() => {
      const root = own.current;
      if (!root || root.contains(document.activeElement)) return;
      (root.querySelector<HTMLElement>('.ui-bar-slot .ui-icon-btn, .ui-bar-slot .ui-link') ?? root).focus();
    });
    const onKey = (event: KeyboardEvent) => {
      // A sheet or dialog opened over it takes the key first (its listener is registered later, so
      // without this the screen under it would close instead; area 8a).
      if (event.key !== 'Escape' || event.defaultPrevented || hasOpenModal()) return;
      event.preventDefault();
      escape.current();
    };
    window.addEventListener('keydown', onKey);
    return () => {
      cancelAnimationFrame(frame);
      window.removeEventListener('keydown', onKey);
      release();
      if (previous?.isConnected) previous.focus();
    };
  }, []);
  return (
    <FramePortal>
      <div
        {...data}
        ref={element => {
          own.current = element;
          if (typeof ref === 'function') ref(element);
          else if (ref) ref.current = element;
        }}
        role="dialog"
        aria-modal={modal || undefined}
        aria-label={label}
        tabIndex={-1}
        className={`ui-part ui-over frame-takeover ${className}`.trim()}
        style={{ left } as CSSProperties}
      >
        {children}
      </div>
    </FramePortal>
  );
});
