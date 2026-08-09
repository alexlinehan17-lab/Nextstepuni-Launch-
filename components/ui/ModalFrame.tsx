import React, { useEffect } from 'react';
import { createPortal } from 'react-dom';
import { AnimatePresence, motion } from 'framer-motion';
import { X } from 'lucide-react';

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
}

const widths = { sm: 'max-w-md', md: 'max-w-xl', lg: 'max-w-3xl', xl: 'max-w-5xl' };

/** Paper-and-outline modal shell with shared accessibility and motion. */
const ModalFrame: React.FC<ModalFrameProps> = ({ open, onClose, title, eyebrow, description, children, footer, width = 'md', labelledBy = 'modal-title' }) => {
  useEffect(() => {
    if (!open) return;
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    const onKey = (event: KeyboardEvent) => { if (event.key === 'Escape') onClose(); };
    window.addEventListener('keydown', onKey);
    return () => {
      document.body.style.overflow = previousOverflow;
      window.removeEventListener('keydown', onKey);
    };
  }, [open, onClose]);

  return createPortal(
    <AnimatePresence>
      {open && (
        <motion.div
          className="fixed inset-0 z-[200] flex items-end justify-center bg-[#1A1A1A]/55 p-0 sm:items-center sm:p-4"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.18 }}
          onMouseDown={event => { if (event.target === event.currentTarget) onClose(); }}
        >
          <motion.section
            role="dialog"
            aria-modal="true"
            aria-labelledby={labelledBy}
            initial={{ opacity: 0, y: 24, scale: 0.985 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 16, scale: 0.99 }}
            transition={{ type: 'spring', stiffness: 280, damping: 28, mass: 0.85 }}
            className={`flex max-h-[92dvh] w-full flex-col overflow-hidden rounded-t-[24px] border-[1.5px] border-[#383838] bg-[#FAFBF6] shadow-[5px_5px_0_0_#383838] sm:rounded-[24px] dark:border-zinc-600 dark:bg-zinc-900 ${widths[width]}`}
          >
            <div className="flex items-start justify-between gap-4 border-b border-[#DDD8D2] px-5 py-4 sm:px-6 sm:py-5 dark:border-zinc-700">
              <div>
                {eyebrow && <p className="mb-1 text-[10px] font-bold uppercase tracking-[0.18em] text-[#8D857E] dark:text-zinc-500">{eyebrow}</p>}
                <h2 id={labelledBy} className="font-serif text-2xl font-semibold leading-tight text-[#1A1A1A] dark:text-white">{title}</h2>
                {description && <p className="mt-1 text-sm leading-relaxed text-[#706A64] dark:text-zinc-400">{description}</p>}
              </div>
              <button type="button" onClick={onClose} aria-label="Close" className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl border border-[#CFC9C2] bg-white text-[#59534D] transition-colors hover:border-[#383838] hover:text-[#1A1A1A] dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-300">
                <X size={18} />
              </button>
            </div>
            <div className="min-h-0 flex-1 overflow-y-auto px-5 py-5 sm:px-6">{children}</div>
            {footer && <div className="border-t border-[#DDD8D2] bg-white/60 px-5 py-4 sm:px-6 dark:border-zinc-700 dark:bg-zinc-950/30">{footer}</div>}
          </motion.section>
        </motion.div>
      )}
    </AnimatePresence>,
    document.body,
  );
};

export default ModalFrame;
