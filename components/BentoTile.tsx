/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Mercury-aesthetic tile used in the Modules page and on the home
 * navigation tiles (Innovation Zone, My Progress, Learning Paths).
 *
 * White card surface; the category accent is rendered as a small detail
 * (icon container, activity ring, hover border) rather than as the whole
 * card background.
 */

import React from 'react';
import { ArrowRight } from 'lucide-react';
import { MotionDiv } from './Motion';

interface BentoTileProps {
  icon: any;
  title: string;
  subtitle: string;
  description?: string;
  onClick: () => void;
  accentHex: string;
  progress?: number;
  hideProgress?: boolean;
  className?: string;
  delay?: number;
  /** Small uppercase data chip in the top-right (e.g. "8 TOOLS", "12/56 DONE"). */
  stat?: string;
}

interface ActivityRingProps {
  progress: number;
  color: string;
  size?: number;
  strokeWidth?: number;
}

const ActivityRing: React.FC<ActivityRingProps> = ({ progress, color, size = 40, strokeWidth = 3 }) => {
  const radius = (size - strokeWidth) / 2;
  const circumference = radius * 2 * Math.PI;
  const isComplete = progress >= 100;
  const isZero = progress <= 0;
  const offset = circumference - (Math.min(100, Math.max(0, progress)) / 100) * circumference;

  return (
    <div className="relative shrink-0" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="-rotate-90">
        <circle cx={size / 2} cy={size / 2} r={radius} stroke="#EDEBE8" strokeOpacity={0.6} strokeWidth={strokeWidth} fill="transparent" />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={color}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          fill="transparent"
          strokeDasharray={`${circumference} ${circumference}`}
          strokeDashoffset={offset}
          className="transition-all duration-700"
        />
      </svg>
      <div className="absolute inset-0 flex items-center justify-center">
        {isComplete ? (
          <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
            <path d="M3.5 8.5L6.5 11.5L12.5 4.5" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        ) : isZero ? (
          <span className="text-[9px] font-semibold tracking-wide" style={{ color }}>Start</span>
        ) : (
          <span className="text-[12px] font-bold" style={{ color }}>{Math.round(progress)}</span>
        )}
      </div>
    </div>
  );
};

export const BentoTile: React.FC<BentoTileProps> = ({
  icon: Icon,
  title,
  subtitle,
  description,
  onClick,
  accentHex,
  progress = 0,
  hideProgress = false,
  className = '',
  delay = 0,
  stat,
}) => {
  return (
    <MotionDiv
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay, ease: [0.16, 1, 0.3, 1] }}
      onClick={onClick}
      className={`group relative bg-white dark:bg-zinc-900 border border-[#EDEBE8] dark:border-zinc-800 hover:border-[#1A1A1A]/15 dark:hover:border-zinc-700 rounded-2xl cursor-pointer transition-all duration-300 hover:shadow-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#1A1A1A]/15 focus-visible:ring-offset-2 ${className}`}
      style={{ boxShadow: '0 1px 3px rgba(28,25,23,0.04)' }}
    >
      <div className="p-5 md:p-7 h-full flex flex-col justify-between">
        <div>
          <div className="flex items-start justify-between mb-5">
            <div
              className="w-11 h-11 rounded-xl flex items-center justify-center transition-transform duration-300 group-hover:scale-105"
              style={{ color: accentHex, backgroundColor: accentHex + '14' }}
            >
              <Icon size={22} strokeWidth={1.75} />
            </div>
            {stat ? (
              <span className="text-[10px] font-semibold uppercase tracking-[0.15em] mt-2 px-2 py-1 rounded-md" style={{ color: accentHex, backgroundColor: accentHex + '10' }}>
                {stat}
              </span>
            ) : (
              <div className="opacity-0 group-hover:opacity-100 transition-all duration-300 group-hover:translate-x-0.5 text-zinc-400 dark:text-zinc-500 mt-2">
                <ArrowRight size={16} />
              </div>
            )}
          </div>

          <p className="text-[10px] font-semibold uppercase tracking-[0.18em] mb-2 text-[#A8A29E] dark:text-zinc-500">
            {subtitle}
          </p>
          <h3 className="font-serif text-lg md:text-xl leading-tight font-semibold tracking-tight text-[#1A1A1A] dark:text-white">
            {title}
          </h3>
          {description && (
            <p className="mt-2 text-[12px] leading-relaxed line-clamp-2 text-[#78716C] dark:text-zinc-400">
              {description}
            </p>
          )}
        </div>

        {!hideProgress && (
          <div className="mt-5 flex items-center justify-between gap-4 pt-4 border-t border-[#EDEBE8] dark:border-zinc-800">
            <span className="text-[10px] font-semibold uppercase tracking-widest text-[#A8A29E] dark:text-zinc-500">Progress</span>
            <ActivityRing progress={progress} color={accentHex} />
          </div>
        )}
      </div>
    </MotionDiv>
  );
};
