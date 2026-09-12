/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import React, { useEffect, useId, useRef } from 'react';
import { createPortal } from 'react-dom';
import { AnimatePresence } from 'framer-motion';
import { ArrowRight } from 'lucide-react';
import { MotionDiv, useReducedMotion } from './Motion';
import { useModal } from '../hooks/useModal';
import JourneyPointsGuide from './JourneyPointsGuide';

interface PointsExplainerProps {
  isOpen: boolean;
  onDismiss: () => void;
}

/** First-study primer: one paper surface, aligned rates and a clear way back. */
const PointsExplainer: React.FC<PointsExplainerProps> = ({ isOpen, onDismiss }) => {
  const dialogRef = useRef<HTMLDivElement>(null);
  const titleId = useId();
  const reduceMotion = useReducedMotion();
  useModal(isOpen, onDismiss, dialogRef);

  useEffect(() => {
    if (!isOpen) return;
    const previous = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => { document.body.style.overflow = previous; };
  }, [isOpen]);

  return createPortal(
    <AnimatePresence>
      {isOpen && (
        <MotionDiv
          className="jp-primer-backdrop"
          data-lenis-prevent
          initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
          transition={{ duration: reduceMotion ? 0 : 0.18 }}
          onMouseDown={(event: React.MouseEvent) => { if (event.target === event.currentTarget) onDismiss(); }}
        >
          <MotionDiv
            ref={dialogRef}
            className="jp-guide jp-primer"
            role="dialog"
            aria-modal="true"
            aria-labelledby={titleId}
            tabIndex={-1}
            initial={{ opacity: 0, y: reduceMotion ? 0 : 16 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: reduceMotion ? 0 : 8 }}
            transition={{ duration: reduceMotion ? 0 : 0.24 }}
          >
            <JourneyPointsGuide titleId={titleId} onClose={onDismiss} />
            <footer className="jp-primer-footer">
              <button type="button" className="jp-primer-action" onClick={onDismiss}>
                Got it <ArrowRight size={18} aria-hidden="true" />
              </button>
            </footer>
          </MotionDiv>
        </MotionDiv>
      )}
    </AnimatePresence>,
    document.body,
  );
};

export default PointsExplainer;
