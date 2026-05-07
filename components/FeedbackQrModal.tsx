/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Feedback QR modal — surfaces a printable QR code so students can scan
 * it with their phone and submit feedback. Triggered from the home-page
 * sidebar.
 */

import React, { useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X } from 'lucide-react';

const TEAL = '#2A7D6F';
const INK = '#1a1a1a';

interface Props {
  open: boolean;
  onClose: () => void;
}

const FeedbackQrModal: React.FC<Props> = ({ open, onClose }) => {
  // Close on Escape
  useEffect(() => {
    if (!open) return;
    const handler = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [open, onClose]);

  return (
    <AnimatePresence>
      {open && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.2 }}
          onClick={onClose}
          aria-modal
          role="dialog"
          aria-label="Share feedback — QR code"
          style={{
            position: 'fixed',
            inset: 0,
            backgroundColor: 'rgba(20, 18, 16, 0.65)',
            backdropFilter: 'blur(4px)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1000,
            padding: 24,
          }}
        >
          <motion.div
            initial={{ opacity: 0, scale: 0.94, y: 8 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.96, y: 6 }}
            transition={{ duration: 0.25, ease: 'easeOut' }}
            onClick={(e) => e.stopPropagation()}
            className="rounded-2xl"
            style={{
              backgroundColor: '#FFFFFF',
              border: `2px solid ${INK}`,
              padding: '28px 30px',
              maxWidth: 440,
              width: '100%',
              position: 'relative',
              boxShadow: '0 24px 48px rgba(20, 18, 16, 0.25)',
            }}
          >
            <button
              type="button"
              onClick={onClose}
              aria-label="Close"
              style={{
                position: 'absolute',
                top: 14,
                right: 14,
                width: 32,
                height: 32,
                borderRadius: 999,
                border: 'none',
                backgroundColor: 'transparent',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: '#5a5550',
              }}
            >
              <X size={18} strokeWidth={1.8} />
            </button>

            <p
              className="font-sans"
              style={{
                fontSize: 10,
                fontWeight: 700,
                textTransform: 'uppercase',
                letterSpacing: 0.6,
                color: TEAL,
                marginBottom: 6,
              }}
            >
              Share your feedback
            </p>
            <h2
              className="font-serif"
              style={{
                fontSize: 22,
                fontWeight: 600,
                color: INK,
                lineHeight: 1.25,
                marginBottom: 6,
              }}
            >
              Scan to tell us what&rsquo;s working.
            </h2>
            <p
              className="font-sans"
              style={{
                fontSize: 13,
                color: '#5a5550',
                lineHeight: 1.55,
                marginBottom: 18,
              }}
            >
              Point your phone camera at the code. Two minutes is enough — what helped, what didn&rsquo;t, what&rsquo;s missing.
            </p>

            <div
              className="rounded-xl"
              style={{
                backgroundColor: '#FFFFFF',
                border: `1.5px solid ${INK}`,
                padding: 18,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              <img
                src="/feedback-qr.png"
                alt="Feedback QR code"
                style={{
                  display: 'block',
                  width: '100%',
                  maxWidth: 320,
                  height: 'auto',
                  imageRendering: 'pixelated',
                }}
              />
            </div>

            <p
              className="font-sans"
              style={{
                fontSize: 11.5,
                color: '#9e9186',
                marginTop: 12,
                textAlign: 'center',
              }}
            >
              Hold the phone steady — the code links to a short form, no login required.
            </p>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default FeedbackQrModal;
