import React, { useEffect, useId, useRef } from 'react';
import { createPortal } from 'react-dom';
import { AnimatePresence, motion, useReducedMotion } from 'framer-motion';
import { X } from 'lucide-react';
import { useModal } from '../../hooks/useModal';

interface ModalFrameProps {
  open: boolean;
  onClose: () => void;
  title: string;
  eyebrow?: string;
  description?: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
  width?: 'sm' | 'md' | 'lg' | 'xl';
  labelledBy?: string;
  variant?: 'standard' | 'listening-room';
  closeDisabled?: boolean;
}

const widths = { sm: 'max-w-md', md: 'max-w-xl', lg: 'max-w-3xl', xl: 'max-w-5xl' };

/** Paper-and-outline modal shell with shared accessibility and motion. */
const ModalFrame: React.FC<ModalFrameProps> = ({ open, onClose, title, eyebrow, description, children, footer, width = 'md', labelledBy, variant = 'standard', closeDisabled = false }) => {
  const dialogRef = useRef<HTMLElement>(null);
  const overlayRef = useRef<HTMLDivElement>(null);
  const titleId = useId();
  const labelId = labelledBy ?? titleId;
  const requestClose = () => { if (!closeDisabled) onClose(); };
  useModal(open, requestClose, dialogRef, { closeDisabled, initialFocus: 'dialog' });
  const reduceMotion = useReducedMotion();
  const isListeningRoom = variant === 'listening-room';

  // iOS keeps the layout viewport behind the keyboard. Fit the feedback sheet
  // to the visible area so its header and scrollable form remain reachable.
  useEffect(() => {
    const viewport = window.visualViewport;
    if (!open || !isListeningRoom || !viewport) return;
    let previousHeight = viewport.height;
    let focusFrame = 0;
    const updateViewport = () => {
      // Preserve browser pinch zoom rather than resizing the dialog around it.
      if (viewport.scale !== 1) return;
      overlayRef.current?.style.setProperty('--feedback-viewport-height', `${viewport.height}px`);
      overlayRef.current?.style.setProperty('--feedback-viewport-top', `${viewport.offsetTop}px`);
      if (viewport.height < previousHeight) {
        cancelAnimationFrame(focusFrame);
        focusFrame = requestAnimationFrame(() => {
          const field = document.activeElement;
          const scroll = dialogRef.current?.querySelector<HTMLElement>('.feedback-scroll');
          if (!(field instanceof HTMLElement) || !field.matches('input, textarea') || !scroll?.contains(field)) return;
          const bounds = scroll.getBoundingClientRect();
          const input = field.getBoundingClientRect();
          if (input.bottom > bounds.bottom) scroll.scrollTop += input.bottom - bounds.bottom + 12;
          else if (input.top < bounds.top) scroll.scrollTop += input.top - bounds.top - 12;
        });
      }
      previousHeight = viewport.height;
    };
    updateViewport();
    viewport.addEventListener('resize', updateViewport);
    viewport.addEventListener('scroll', updateViewport);
    return () => {
      cancelAnimationFrame(focusFrame);
      viewport.removeEventListener('resize', updateViewport);
      viewport.removeEventListener('scroll', updateViewport);
    };
  }, [open, isListeningRoom]);

  return createPortal(
    <AnimatePresence>
      {open && (
        <motion.div
          ref={overlayRef}
          data-lenis-prevent
          /* Modals render outside .product-shell, so the dark compat layer never
             reached their hard-coded light surfaces -- white panels kept
             dark-mode ink. `theme-compat` opts every ModalFrame consumer in. */
          className={`${isListeningRoom ? 'feedback-overlay' : 'theme-compat'} fixed inset-0 z-[200] flex items-end justify-center bg-[#1A1A1A]/55 p-0 sm:items-center sm:p-4`}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.18 }}
          onMouseDown={event => { if (event.target === event.currentTarget) requestClose(); }}
        >
          <motion.section
            ref={dialogRef}
            role="dialog"
            aria-modal="true"
            aria-labelledby={labelId}
            tabIndex={-1}
            initial={{ opacity: 0, y: reduceMotion ? 0 : 24, scale: reduceMotion ? 1 : 0.985 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: reduceMotion ? 0 : 16, scale: reduceMotion ? 1 : 0.99 }}
            transition={reduceMotion ? { duration: 0 } : { type: 'spring', stiffness: 280, damping: 28, mass: 0.85 }}
            className={isListeningRoom ? 'feedback-listening-room' : `flex max-h-[92dvh] w-full flex-col overflow-hidden rounded-t-[24px] border-[1.5px] border-[#383838] bg-white dark:bg-zinc-900 shadow-[5px_5px_0_0_#383838] sm:rounded-[24px] dark:border-zinc-600 dark:bg-zinc-900 ${widths[width]}`}
          >
            {isListeningRoom ? (
              <header className="feedback-brand-header">
                <span className="feedback-wordmark">nextstepuni</span>
                <span className="feedback-brand-note">A better app, together.</span>
                <h2 id={labelId} className="sr-only">{title}</h2>
                <button type="button" onClick={requestClose} disabled={closeDisabled} aria-label="Close" className="feedback-close">
                  <X size={19} aria-hidden="true" />
                </button>
              </header>
            ) : <div className="flex shrink-0 items-start justify-between gap-4 border-b border-[var(--outline-soft)] px-5 py-4 sm:px-6 sm:py-5 dark:border-zinc-700">
              <div>
                {eyebrow && <p className="mb-1 text-[10px] font-bold uppercase tracking-[0.18em] text-[#8D857E] dark:text-zinc-500">{eyebrow}</p>}
                <h2 id={labelId} className="font-serif text-2xl font-semibold leading-tight text-[#1A1A1A] dark:text-white">{title}</h2>
                {description && <p className="mt-1 text-sm leading-relaxed text-[#706A64] dark:text-zinc-400">{description}</p>}
              </div>
              <button type="button" onClick={requestClose} disabled={closeDisabled} aria-label="Close" className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl border border-[var(--outline-soft)] bg-white text-[#59534D] transition-colors hover:border-[#383838] hover:text-[#1A1A1A] dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-300">
                <X size={18} />
              </button>
            </div>}
            <div data-lenis-prevent className={isListeningRoom ? 'feedback-scroll' : 'min-h-0 flex-1 overflow-y-auto overscroll-contain px-5 py-5 sm:px-6'}>{children}</div>
            {footer && <div className="border-t border-[var(--outline-soft)] bg-white/60 px-5 py-4 sm:px-6 dark:border-zinc-700 dark:bg-zinc-950/30">{footer}</div>}
          </motion.section>
        </motion.div>
      )}
    </AnimatePresence>,
    document.body,
  );
};

export default ModalFrame;
