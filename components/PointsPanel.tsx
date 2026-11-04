/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import React, { useId } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv, useReducedMotion } from './Motion';
import JourneyPointsGuide from './JourneyPointsGuide';

interface PointsPanelProps {
  open: boolean;
  onHide: () => void;
}

/** Launchpad reference, sharing the study primer's rates and typography. */
const PointsPanel: React.FC<PointsPanelProps> = ({ open, onHide }) => {
  const titleId = useId();
  const reduceMotion = useReducedMotion();
  return (
    <AnimatePresence initial={false}>
      {open && (
        <MotionDiv
          initial={{ height: 0, opacity: 0, marginBottom: 0 }}
          animate={{ height: 'auto', opacity: 1, marginBottom: 32 }}
          exit={{ height: 0, opacity: 0, marginBottom: 0 }}
          transition={{ duration: reduceMotion ? 0 : 0.24 }}
          className="jp-reference-reveal"
        >
          <section className="jp-guide jp-reference" aria-label="How points work">
            <JourneyPointsGuide titleId={titleId} onClose={onHide} closeLabel="Hide points panel" />
          </section>
        </MotionDiv>
      )}
    </AnimatePresence>
  );
};

export default PointsPanel;
