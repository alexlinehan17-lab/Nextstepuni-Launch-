import React, { useEffect, useId, useRef } from 'react';
import { createPortal } from 'react-dom';
import { AnimatePresence } from 'framer-motion';
import { X } from 'lucide-react';
import { MotionDiv } from '../Motion';
import { useModal } from '../../hooks/useModal';
import './signature-card.css';

interface SignatureCardProps {
  open: boolean;
  onClose: () => void;
  title: string;
  eyebrow?: string;
  description?: React.ReactNode;
  progress?: { current: number; total: number };
  wide?: boolean;
  children: React.ReactNode;
  footer: React.ReactNode;
}

export default function SignatureCard({ open, onClose, title, eyebrow, description, progress, wide, children, footer }: SignatureCardProps) {
  const ref = useRef<HTMLDivElement>(null);
  const bodyRef = useRef<HTMLDivElement>(null);
  const id = useId();
  useModal(open, onClose, ref, { initialFocus: 'dialog' });
  useEffect(() => {
    if (!open) return;
    // A new step can disable or remove the previously focused action.
    // Announce its heading and start the scrollable content at the top.
    ref.current?.focus();
    if (bodyRef.current) bodyRef.current.scrollTop = 0;
  }, [open, title]);
  return createPortal(<AnimatePresence>{open && <MotionDiv className="theme-compat signature-card-overlay" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} onClick={onClose}>
    <MotionDiv ref={ref} className={`signature-card${wide ? ' signature-card--wide' : ''}`} role="dialog" aria-modal="true" aria-labelledby={`${id}-title`} aria-describedby={description ? `${id}-description` : undefined} tabIndex={-1}
      initial={{ opacity: 0, scale: .98 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, scale: .98 }} transition={{ duration: .18 }} onClick={(event: React.MouseEvent) => event.stopPropagation()}>
      <header className="sc-header">
        <div>{eyebrow && <p className="sc-eyebrow">{eyebrow}</p>}<h2 id={`${id}-title`}>{title}</h2>{description && <p id={`${id}-description`} className="sc-description">{description}</p>}
          {progress && <div className="sc-progress" role="progressbar" aria-label="Setup progress" aria-valuemin={1} aria-valuemax={progress.total} aria-valuenow={progress.current} aria-valuetext={`Step ${progress.current} of ${progress.total}`}>
            {Array.from({ length: progress.total }, (_, index) => <span key={index} data-complete={index < progress.current} />)}
          </div>}
        </div>
        <button type="button" className="sc-close" onClick={onClose} aria-label="Close"><X size={18} aria-hidden="true" /></button>
      </header>
      <div ref={bodyRef} className="sc-body">{children}</div>
      <footer className="sc-footer">{footer}</footer>
    </MotionDiv>
  </MotionDiv>}</AnimatePresence>, document.body);
}
