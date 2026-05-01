/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * SectionCard — Mercury-styled tile for the home dashboard's top-level
 * entry points (Modules, Innovation Zone, My Progress, Learning Paths).
 *
 * Recipe:
 *   - White card, 1px #EDEBE8 border, soft 1/3 shadow at rest
 *   - Painted-blob + ink-illustration tile on the left (each section
 *     supplies its own dedicated icon component)
 *   - Eyebrow / serif title / sans subtitle on the right
 *   - Right-side arrow that fades + slides in on hover ("click me")
 *   - Hover lifts the card 2px, deepens the shadow, darkens the border,
 *     and nudges the icon
 *
 * Sister component to <ToolHeader>. Different surface, different role:
 *   - <SectionCard>: dashboard navigation, soft blob + ink illustration
 *   - <ToolHeader>: tool entry within IZ, saturated tile + white SVG
 */

import React from 'react';

interface SectionCardProps {
  eyebrow: string;
  title: string;
  subtitle: string;
  /** Inline SVG component containing both the blob fill and the ink illustration. */
  icon: React.ReactNode;
  onClick?: () => void;
  className?: string;
}

const ArrowSVG: React.FC = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <path d="M5 12h14M12 5l7 7-7 7" />
  </svg>
);

export const SectionCard: React.FC<SectionCardProps> = ({
  eyebrow,
  title,
  subtitle,
  icon,
  onClick,
  className,
}) => {
  const interactive = !!onClick;
  const Wrapper: React.ElementType = interactive ? 'button' : 'div';

  return (
    <Wrapper
      onClick={onClick}
      className={`group relative flex items-center gap-5 text-left w-full bg-white dark:bg-zinc-900 border border-[#EDEBE8] dark:border-zinc-800 rounded-2xl transition-all duration-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#1A1A1A]/15 focus-visible:ring-offset-2 ${interactive ? 'cursor-pointer hover:border-[#1A1A1A]/15 dark:hover:border-zinc-700 hover:-translate-y-0.5' : ''} ${className ?? ''}`}
      style={{
        padding: '22px',
        boxShadow: '0 1px 3px rgba(28,25,23,0.04)',
        ...(interactive ? {} : {}),
      }}
      onMouseEnter={interactive ? (e) => {
        (e.currentTarget as HTMLElement).style.boxShadow = '0 8px 24px rgba(28,25,23,0.08), 0 1px 3px rgba(28,25,23,0.04)';
      } : undefined}
      onMouseLeave={interactive ? (e) => {
        (e.currentTarget as HTMLElement).style.boxShadow = '0 1px 3px rgba(28,25,23,0.04)';
      } : undefined}
    >
      {/* Tile — painted blob + ink illustration. Slight scale on hover. */}
      <div
        className="shrink-0 overflow-hidden transition-transform duration-300 group-hover:scale-[1.04]"
        style={{ width: 88, height: 88, borderRadius: 14 }}
      >
        {icon}
      </div>

      {/* Text */}
      <div className="flex-1 min-w-0">
        <p
          style={{
            fontFamily: "'DM Sans', system-ui, sans-serif",
            fontSize: 10,
            fontWeight: 500,
            letterSpacing: '1.5px',
            textTransform: 'uppercase',
            color: 'rgba(0,0,0,0.5)',
            margin: 0,
          }}
        >
          {eyebrow}
        </p>
        <h3
          className="font-serif"
          style={{
            fontSize: 22,
            fontWeight: 500,
            letterSpacing: '-0.4px',
            lineHeight: 1.1,
            color: '#1a1a1a',
            margin: 0,
            marginTop: 6,
          }}
        >
          {title}
        </h3>
        <p
          style={{
            fontFamily: "'DM Sans', system-ui, sans-serif",
            fontSize: 13,
            fontWeight: 400,
            color: 'rgba(0,0,0,0.6)',
            lineHeight: 1.5,
            margin: 0,
            marginTop: 6,
          }}
        >
          {subtitle}
        </p>
      </div>

      {/* Arrow — fades + slides in on hover. The "click me" affordance. */}
      {interactive && (
        <div
          className="shrink-0 self-center pl-2 text-zinc-400 dark:text-zinc-500 transition-all duration-300 opacity-50 group-hover:opacity-100 group-hover:translate-x-1 group-hover:text-zinc-800 dark:group-hover:text-zinc-200"
          aria-hidden="true"
        >
          <ArrowSVG />
        </div>
      )}
    </Wrapper>
  );
};

export default SectionCard;
