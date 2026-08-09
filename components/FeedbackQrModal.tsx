/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Feedback QR modal — surfaces a printable QR code so students can scan
 * it with their phone and submit feedback. Triggered from the home-page
 * sidebar.
 */

import React from 'react';
import ModalFrame from './ui/ModalFrame';

const INK = '#1a1a1a';

interface Props {
  open: boolean;
  onClose: () => void;
}

const FeedbackQrModal: React.FC<Props> = ({ open, onClose }) => {
  return (
    <ModalFrame open={open} onClose={onClose} title="Scan to tell us what’s working" eyebrow="Share your feedback" width="sm">
            <p className="mb-5 text-sm leading-relaxed text-[#5A5550]">
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
    </ModalFrame>
  );
};

export default FeedbackQrModal;
