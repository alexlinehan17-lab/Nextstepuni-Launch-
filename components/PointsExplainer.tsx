/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { createPortal } from 'react-dom';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { useModal } from '../hooks/useModal';

interface PointsExplainerProps {
  isOpen: boolean;
  onDismiss: () => void;
}

const PointsExplainer: React.FC<PointsExplainerProps> = ({ isOpen, onDismiss }) => {
  useModal(isOpen, onDismiss);

  return createPortal(
    <AnimatePresence>
      {isOpen && (
        <MotionDiv
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.2 }}
          className="fixed inset-0 flex items-center justify-center z-[300] p-4"
          style={{ backgroundColor: 'rgba(0,0,0,0.4)' }}
          onClick={onDismiss}
        >
          <MotionDiv
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.25, ease: [0.16, 1, 0.3, 1] }}
            className="w-full max-w-sm"
            style={{
              background: '#ffffff',
              border: '2px solid #1a1a1a',
              borderRadius: '16px',
              padding: '24px',
            }}
            onClick={(e: React.MouseEvent) => e.stopPropagation()}
          >
            {/* Title */}
            <h2
              style={{
                fontFamily: "'Source Serif 4', serif",
                fontSize: '22px',
                fontWeight: 700,
                color: '#1a1a1a',
                margin: 0,
                marginBottom: '20px',
              }}
            >
              How Points Work
            </h2>

            {/* Earn section */}
            <div style={{ marginBottom: '18px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '10px' }}>
                <span
                  style={{
                    width: '8px',
                    height: '8px',
                    borderRadius: '50%',
                    backgroundColor: '#2A7D6F',
                    display: 'inline-block',
                    flexShrink: 0,
                  }}
                />
                <span
                  style={{
                    fontFamily: "'Source Serif 4', serif",
                    fontSize: '16px',
                    fontWeight: 600,
                    color: '#1a1a1a',
                  }}
                >
                  Earn
                </span>
              </div>
              <ul
                style={{
                  listStyle: 'none',
                  margin: 0,
                  padding: 0,
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '6px',
                  paddingLeft: '16px',
                }}
              >
                {[
                  'Study sessions: 15 pts per 10 min',
                  'Module sections: 10 pts each',
                  'Complete a module: +30 bonus',
                  'Daily quests: 25\u201345 pts',
                  'Weekly challenges: 100\u2013200 pts',
                ].map((item) => (
                  <li
                    key={item}
                    style={{
                      fontFamily: "'DM Sans', sans-serif",
                      fontSize: '14px',
                      fontWeight: 400,
                      color: '#3a3530',
                      lineHeight: '1.5',
                    }}
                  >
                    {item}
                  </li>
                ))}
              </ul>
            </div>

            {/* Spend section */}
            <div style={{ marginBottom: '18px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '10px' }}>
                <span
                  style={{
                    width: '8px',
                    height: '8px',
                    borderRadius: '50%',
                    backgroundColor: '#2A7D6F',
                    display: 'inline-block',
                    flexShrink: 0,
                  }}
                />
                <span
                  style={{
                    fontFamily: "'Source Serif 4', serif",
                    fontSize: '16px',
                    fontWeight: 600,
                    color: '#1a1a1a',
                  }}
                >
                  Spend
                </span>
              </div>
              <ul
                style={{
                  listStyle: 'none',
                  margin: 0,
                  padding: 0,
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '6px',
                  paddingLeft: '16px',
                }}
              >
                {[
                  'Island shop: build your island',
                  'Skip a study block: 20 pts',
                  'Rest day pass: 60 pts',
                ].map((item) => (
                  <li
                    key={item}
                    style={{
                      fontFamily: "'DM Sans', sans-serif",
                      fontSize: '14px',
                      fontWeight: 400,
                      color: '#3a3530',
                      lineHeight: '1.5',
                    }}
                  >
                    {item}
                  </li>
                ))}
              </ul>
            </div>

            {/* Tip callout */}
            <div
              style={{
                background: '#f0faf8',
                borderLeft: '3px solid #2A7D6F',
                borderRadius: '0 10px 10px 0',
                padding: '12px 16px',
                marginBottom: '22px',
              }}
            >
              <p
                style={{
                  fontFamily: "'Source Serif 4', serif",
                  fontSize: '14px',
                  fontWeight: 600,
                  color: '#1a1a1a',
                  margin: 0,
                  marginBottom: '4px',
                }}
              >
                Tip
              </p>
              <p
                style={{
                  fontFamily: "'DM Sans', sans-serif",
                  fontSize: '14px',
                  fontWeight: 400,
                  fontStyle: 'italic',
                  color: '#1a6358',
                  margin: 0,
                  lineHeight: '1.5',
                }}
              >
                The more you study, the more you earn. A 30-minute session earns 45 points — enough for a new island tile.
              </p>
            </div>

            {/* Got it button — Primary CTA pill */}
            <button
              onClick={onDismiss}
              style={{
                display: 'block',
                width: '100%',
                background: '#2A7D6F',
                color: '#ffffff',
                fontFamily: "'DM Sans', sans-serif",
                fontSize: '15px',
                fontWeight: 600,
                border: 'none',
                borderRadius: '100px',
                borderBottom: '3px solid #1a5a4e',
                boxShadow: '0 4px 0 #1a5a4e',
                padding: '13px 28px',
                cursor: 'pointer',
                transition: 'transform 0.1s, box-shadow 0.1s',
              }}
              onMouseDown={(e) => {
                const btn = e.currentTarget;
                btn.style.transform = 'translateY(3px)';
                btn.style.boxShadow = '0 1px 0 #1a5a4e';
              }}
              onMouseUp={(e) => {
                const btn = e.currentTarget;
                btn.style.transform = 'translateY(0)';
                btn.style.boxShadow = '0 4px 0 #1a5a4e';
              }}
              onMouseLeave={(e) => {
                const btn = e.currentTarget;
                btn.style.transform = 'translateY(0)';
                btn.style.boxShadow = '0 4px 0 #1a5a4e';
              }}
            >
              Got it
            </button>
          </MotionDiv>
        </MotionDiv>
      )}
    </AnimatePresence>,
    document.body
  );
};

export default PointsExplainer;
