/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from '../Motion';

export interface IsometricSpriteProps {
  src: string;
  /** Horizontal position in world px (from left edge) */
  x: number;
  /** Vertical position in world px (from bottom edge). Higher = further back. */
  y: number;
  /** Display width in px */
  width?: number;
  /** Manual z-index override */
  zIndex?: number;
  /** Controls visibility with spring animation */
  visible?: boolean;
  /** Animation stagger delay (seconds) */
  delay?: number;
  /** Tooltip on hover */
  label?: string;
  /** Flip horizontally */
  flip?: boolean;
  opacity?: number;
  onClick?: () => void;
}

const IsometricSprite: React.FC<IsometricSpriteProps> = ({
  src, x, y, width = 80, zIndex, visible = true,
  delay = 0, label, flip = false, opacity = 1, onClick,
}) => {
  const [hovered, setHovered] = useState(false);
  const autoZ = zIndex ?? Math.round(1000 - y);

  return (
    <AnimatePresence>
      {visible && (
        <MotionDiv
          initial={{ opacity: 0, scale: 0 }}
          animate={{ opacity, scale: 1 }}
          exit={{ opacity: 0, scale: 0 }}
          transition={{ type: 'spring', stiffness: 260, damping: 22, delay }}
          style={{
            position: 'absolute',
            left: x,
            bottom: y,
            width,
            zIndex: autoZ,
            transformOrigin: 'bottom center',
            cursor: onClick ? 'pointer' : 'default',
            filter: hovered
              ? 'brightness(1.15) drop-shadow(0 2px 8px rgba(0,0,0,0.3))'
              : 'none',
            pointerEvents: 'auto',
          }}
          onMouseEnter={() => setHovered(true)}
          onMouseLeave={() => setHovered(false)}
          onClick={onClick}
        >
          <img
            src={src}
            alt={label || ''}
            style={{
              width: '100%',
              height: 'auto',
              display: 'block',
              pointerEvents: 'none',
              transform: flip ? 'scaleX(-1)' : undefined,
            }}
            draggable={false}
          />
          {label && hovered && (
            <div style={{
              position: 'absolute', bottom: '100%', left: '50%',
              transform: 'translateX(-50%)', padding: '4px 10px',
              borderRadius: 6, background: 'rgba(0,0,0,0.85)',
              color: 'white', fontSize: 11, fontWeight: 600,
              whiteSpace: 'nowrap', marginBottom: 4,
              pointerEvents: 'none', zIndex: 9000,
            }}>
              {label}
            </div>
          )}
        </MotionDiv>
      )}
    </AnimatePresence>
  );
};

/** Isometric diamond-shaped ground plane */
export const IsoGround: React.FC<{
  /** Top color of gradient */
  color1?: string;
  /** Bottom color of gradient */
  color2?: string;
  /** 0-100% from left */
  left?: string;
  /** 0-100% width */
  width?: string;
  /** 0-100% from bottom */
  bottom?: string;
  /** 0-100% height */
  height?: string;
}> = ({
  color1 = '#7DB86A',
  color2 = '#5A9A48',
  left = '10%',
  width = '80%',
  bottom = '5%',
  height = '55%',
}) => (
  <div style={{
    position: 'absolute', left, bottom, width, height, zIndex: 1, pointerEvents: 'none',
  }}>
    {/* Shadow under ground */}
    <div style={{
      position: 'absolute', inset: '-2%',
      background: 'rgba(0,0,0,0.12)',
      clipPath: 'polygon(50% 20%, 97% 42%, 50% 64%, 3% 42%)',
      filter: 'blur(16px)',
    }} />
    {/* Ground diamond */}
    <div style={{
      position: 'absolute', inset: 0,
      background: `linear-gradient(160deg, ${color1} 0%, ${color2} 100%)`,
      clipPath: 'polygon(50% 18%, 97% 42%, 50% 66%, 3% 42%)',
    }} />
    {/* Subtle edge highlight */}
    <div style={{
      position: 'absolute', inset: 0,
      background: 'linear-gradient(160deg, rgba(255,255,255,0.12) 0%, transparent 50%)',
      clipPath: 'polygon(50% 18%, 97% 42%, 50% 66%, 3% 42%)',
    }} />
  </div>
);

/** Golden celebration overlay */
export const GoldenOverlay: React.FC<{ active: boolean }> = ({ active }) => (
  <AnimatePresence>
    {active && (
      <MotionDiv
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        transition={{ duration: 1.5 }}
        style={{
          position: 'absolute', inset: 0,
          background: 'radial-gradient(ellipse at center, rgba(255,200,50,0.3) 0%, rgba(255,160,20,0.12) 50%, transparent 80%)',
          pointerEvents: 'none', zIndex: 9990,
        }}
      />
    )}
  </AnimatePresence>
);

export default IsometricSprite;
