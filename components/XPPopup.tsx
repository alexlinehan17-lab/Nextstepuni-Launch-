/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';

interface XPPopupProps {
  points: number;
  isVisible: boolean;
  onComplete: () => void;
}

const XPPopup: React.FC<XPPopupProps> = ({ points, isVisible, onComplete }) => {
  if (!isVisible || points <= 0) return null;

  return (
    <AnimatePresence>
      {isVisible && (
        <MotionDiv
          key="xp-popup"
          initial={{ opacity: 0, y: 0, scale: 0.8 }}
          animate={{ opacity: 1, y: -20, scale: 1 }}
          exit={{ opacity: 0, y: -50 }}
          transition={{ duration: 0.6 }}
          onAnimationComplete={onComplete}
          className="fixed z-[250] pointer-events-none"
          style={{
            top: '45%',
            left: '50%',
            transform: 'translateX(-50%)',
          }}
        >
          <div
            className="flex items-center gap-2 px-5 py-2.5 rounded-full"
            style={{
              backgroundColor: 'rgba(42,125,111,0.95)',
              boxShadow: '0 4px 20px rgba(42,125,111,0.3)',
            }}
          >
            <span className="text-white text-lg font-bold">+{points}</span>
            <span className="text-white/80 text-sm font-medium">pts</span>
          </div>
        </MotionDiv>
      )}
    </AnimatePresence>
  );
};

export default XPPopup;
