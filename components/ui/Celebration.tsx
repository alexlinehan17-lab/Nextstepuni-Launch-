import React from 'react';
import { createPortal } from 'react-dom';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from '../Motion';

export type CelebrationScale = 'small' | 'medium' | 'milestone';

interface CelebrationFrameProps {
  isOpen: boolean;
  scale?: CelebrationScale;
  children: React.ReactNode;
  ariaLabel: string;
  onDismiss?: () => void;
}

export const CelebrationFrame: React.FC<CelebrationFrameProps> = ({
  isOpen,
  scale = 'milestone',
  children,
  ariaLabel,
  onDismiss,
}) => createPortal(
  <AnimatePresence>
    {isOpen && (
      <MotionDiv
        className="fixed inset-0 z-[300] flex items-end justify-center bg-[#1A1A1A]/55 p-0 sm:items-center sm:p-6"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        onClick={onDismiss}
      >
        <MotionDiv
          role="dialog"
          aria-modal="true"
          aria-label={ariaLabel}
          onClick={(event: React.MouseEvent) => event.stopPropagation()}
          initial={{ opacity: 0, y: 28, scale: 0.985 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: 18, scale: 0.99 }}
          transition={{ type: 'spring', stiffness: 260, damping: 27, mass: 0.9 }}
          className={`relative w-full overflow-hidden rounded-t-[26px] border-[1.5px] border-[#383838] bg-white shadow-[6px_6px_0_0_#383838] dark:border-zinc-600 dark:bg-zinc-900 sm:rounded-[26px] ${
            scale === 'small' ? 'max-w-sm p-6' : scale === 'medium' ? 'max-w-lg p-7 sm:p-9' : 'max-w-2xl p-7 sm:p-10'
          }`}
        >
          <div className="pointer-events-none absolute inset-x-0 top-0 h-1.5 bg-[#F26B1F]" />
          {children}
        </MotionDiv>
      </MotionDiv>
    )}
  </AnimatePresence>,
  document.body,
);

export const MilestoneBadge: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <span className="inline-flex items-center gap-1.5 rounded-lg border-[1.5px] border-[#383838] bg-[#FFF0E7] px-3 py-1.5 text-[10px] font-bold uppercase tracking-[0.16em] text-[#A53E0C] shadow-[2px_2px_0_0_#383838]">
    {children}
  </span>
);

export const CelebrationStat: React.FC<{ label: string; value: React.ReactNode }> = ({ label, value }) => (
  <div className="min-w-0 rounded-xl border border-[#D8D3CD] bg-white px-4 py-3 text-left">
    <p className="truncate text-[10px] font-bold uppercase tracking-[0.14em] text-[#9B9188]">{label}</p>
    <p className="mt-1 truncate font-serif text-xl font-semibold text-[#1A1A1A]">{value}</p>
  </div>
);

