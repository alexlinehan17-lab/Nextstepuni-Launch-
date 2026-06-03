/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * SwipeDeck — the reusable Tinder-style swipe stack shared by the immersive
 * card decks. Generic over the item type; the consumer supplies a `renderFace`
 * for the card face. Drag-fling right = "save"/advance, left = "skip"/advance;
 * a small movement is treated as a tap (open). Three layered cards give the
 * stacked-deck illusion. White SAVE/SKIP stamps fade in as you drag.
 */

import React, { useRef } from 'react';
import { motion, useMotionValue, useTransform, animate } from 'framer-motion';

/** A single draggable top card. */
export const SwipeCard: React.FC<{
  onDismiss: (dir: 'left' | 'right') => void;
  onTap?: () => void;
  children: React.ReactNode;
}> = ({ onDismiss, onTap, children }) => {
  const x = useMotionValue(0);
  const rotate = useTransform(x, [-220, 220], [-12, 12]);
  const saveOp = useTransform(x, [30, 120], [0, 1]);
  const skipOp = useTransform(x, [-120, -30], [1, 0]);
  const dragged = useRef(false);

  return (
    <motion.div
      className="absolute inset-0 cursor-grab active:cursor-grabbing"
      style={{ x, rotate, zIndex: 30 }}
      drag="x"
      dragConstraints={{ left: 0, right: 0 }}
      dragElastic={0.7}
      onDragStart={() => { dragged.current = false; }}
      onDrag={(_e, info) => { if (Math.abs(info.offset.x) > 6) dragged.current = true; }}
      onDragEnd={(_e, info) => {
        if (info.offset.x > 110 || info.velocity.x > 600) animate(x, 780, { duration: 0.3, onComplete: () => onDismiss('right') });
        else if (info.offset.x < -110 || info.velocity.x < -600) animate(x, -780, { duration: 0.3, onComplete: () => onDismiss('left') });
        else animate(x, 0, { type: 'spring', stiffness: 320, damping: 30 });
        window.setTimeout(() => { dragged.current = false; }, 40);
      }}
      onClick={() => { if (!dragged.current) onTap?.(); }}
    >
      <motion.div
        className="absolute top-7 left-6 z-20 px-3 py-1 rounded-lg border-2 text-[15px] font-extrabold tracking-wide"
        style={{ opacity: saveOp, color: '#fff', borderColor: '#fff', transform: 'rotate(-12deg)' }}
      >
        SAVE
      </motion.div>
      <motion.div
        className="absolute top-7 right-6 z-20 px-3 py-1 rounded-lg border-2 text-[15px] font-extrabold tracking-wide"
        style={{ opacity: skipOp, color: 'rgba(255,255,255,0.9)', borderColor: 'rgba(255,255,255,0.9)', transform: 'rotate(12deg)' }}
      >
        SKIP
      </motion.div>
      {children}
    </motion.div>
  );
};

interface DeckStackProps<T extends { id: string }> {
  items: T[];
  index: number;
  onAdvance: (item: T, dir: 'left' | 'right') => void;
  onOpen: (item: T) => void;
  renderFace: (item: T) => React.ReactNode;
  /** Deck box size. */
  width?: number;
  height?: number;
}

/** The layered 3-card stack; only the top card is draggable. */
export function DeckStack<T extends { id: string }>({ items, index, onAdvance, onOpen, renderFace, width = 340, height = 460 }: DeckStackProps<T>) {
  return (
    <div className="relative mx-auto" style={{ maxWidth: width, height }}>
      {[2, 1, 0].map((off) => {
        const item = items[index + off];
        if (!item) return null;
        if (off === 0) {
          return (
            <SwipeCard key={item.id} onDismiss={(dir) => onAdvance(item, dir)} onTap={() => onOpen(item)}>
              {renderFace(item)}
            </SwipeCard>
          );
        }
        return (
          <div
            key={item.id}
            className="absolute inset-0"
            style={{ transform: `translateY(${off * 12}px) scale(${1 - off * 0.05})`, zIndex: 10 - off }}
          >
            {renderFace(item)}
          </div>
        );
      })}
    </div>
  );
}
