/**
 * A compact, touch-friendly tab rail for narrow screens.
 *
 * The active option is kept in view, labels never wrap, and the soft edge
 * fade makes horizontal overflow feel intentional rather than clipped.
 *
 * Pill variant: the white ink-edged pill is one shared element that glides
 * from the old tab to the new one (Motion layoutId, scoped per bar by a
 * LayoutGroup), and a faint ink ghost follows the pointer — and keyboard
 * focus — across the tabs before a choice is made. Reduced motion collapses
 * both to an instant switch. Roles, arrow keys and the focus ring (drawn on
 * the button, outside the pill) are unchanged.
 */
import React, { useEffect, useId, useRef, useState } from 'react';
import { LayoutGroup, motion } from 'framer-motion';
import { useReducedMotion } from '../Motion';
import { useMobileAppDesign } from '../../hooks/useMobileAppDesign';

// React 19 + Framer Motion type incompatibility — the same cast components/Motion.tsx uses.
const MotionSpan = motion.span as any;
const MotionDiv = motion.div as any;

export interface HorizontalTabOption<T extends string> {
  value: T;
  label: string;
}

interface HorizontalTabsProps<T extends string> {
  value: T;
  options: ReadonlyArray<HorizontalTabOption<T>>;
  onChange: (value: T) => void;
  label: string;
  variant?: 'underline' | 'pill';
  /** Pill only: 'md' is the section-tab size (44px), 'sm' the in-card toggle size (36px). */
  size?: 'sm' | 'md';
  className?: string;
  /** Pill only: the tabs share the rail's width evenly (each grows equally) while they fit; when they don't, the rail scrolls as usual. */
  fill?: boolean;
}

export default function HorizontalTabs<T extends string>({
  value,
  options,
  onChange,
  label,
  variant = 'underline',
  size = 'md',
  className = '',
 fill = false }: HorizontalTabsProps<T>) {
  const railRef = useRef<HTMLDivElement | null>(null);
  const activeRef = useRef<HTMLButtonElement | null>(null);
  const mobileAppDesign = useMobileAppDesign();
  const reducedMotion = useReducedMotion();
  const mountedRef = useRef(false);
  // The tab the pointer or keyboard focus is resting on: where the ghost sits.
  const [ghost, setGhost] = useState<T | null>(null);
  const barId = useId();

  useEffect(() => {
    const rail = railRef.current;
    const active = activeRef.current;
    if (!rail || !active) return;
    const left = active.offsetLeft - ((rail.clientWidth - active.offsetWidth) / 2);
    const targetLeft = Math.max(0, left);
    if (typeof rail.scrollTo === 'function') {
      rail.scrollTo({ left: targetLeft, behavior: mobileAppDesign && (reducedMotion || !mountedRef.current) ? 'auto' : 'smooth' });
    } else {
      rail.scrollLeft = targetLeft;
    }
    mountedRef.current = true;
  }, [value, mobileAppDesign, reducedMotion]);

  const pill = variant === 'pill';
  const glide = reducedMotion ? { duration: 0 } : { type: 'spring', bounce: 0.15, duration: 0.45 };

  return (
    <div className={`relative min-w-0 ${className}`}>
      <MotionDiv
        ref={railRef}
        layoutScroll
        role="tablist"
        aria-label={label}
        onPointerLeave={pill ? () => setGhost(null) : undefined}
        className={`overflow-x-auto overscroll-x-contain [scrollbar-width:none] [&::-webkit-scrollbar]:hidden ${pill ? 'rounded-xl border border-[var(--outline-soft)] bg-[var(--surface-soft)] p-1' : 'border-b border-[var(--outline-soft)]'}`}
      >
        <LayoutGroup id={barId}>
        <div className={`flex min-w-max ${pill ? 'gap-1' : 'gap-5 sm:gap-7'} ${pill && fill ? 'w-full' : ''}`}>
          {options.map(option => {
            const active = option.value === value;
            return (
              <button
                key={option.value}
                ref={active ? activeRef : undefined}
                type="button"
                role="tab"
                aria-selected={active}
                tabIndex={mobileAppDesign ? active ? 0 : -1 : undefined}
                onKeyDown={mobileAppDesign ? event => {
                  const index = options.findIndex(item => item.value === option.value);
                  const nextIndex = event.key === 'ArrowRight' ? (index + 1) % options.length : event.key === 'ArrowLeft' ? (index - 1 + options.length) % options.length : event.key === 'Home' ? 0 : event.key === 'End' ? options.length - 1 : -1;
                  if (nextIndex < 0) return;
                  event.preventDefault();
                  railRef.current?.querySelectorAll<HTMLButtonElement>('[role="tab"]')[nextIndex]?.focus({ preventScroll: true });
                  onChange(options[nextIndex].value);
                } : undefined}
                onClick={() => onChange(option.value)}
                onPointerEnter={pill ? () => setGhost(option.value) : undefined}
                onFocus={pill ? () => setGhost(option.value) : undefined}
                onBlur={pill ? () => setGhost(current => (current === option.value ? null : current)) : undefined}
                className={pill
                  ? `${size === 'sm' ? 'min-h-9 px-3 text-[13px]' : 'min-h-11 px-4 text-sm'} relative shrink-0 whitespace-nowrap rounded-lg border border-transparent font-semibold transition-colors ${fill ? 'flex-1 text-center' : ''} ${active ? 'text-[var(--ink-primary)]' : 'text-[var(--ink-muted)] hover:text-[var(--ink-secondary)]'}`
                  : `relative min-h-11 ${mobileAppDesign ? 'min-w-11' : ''} shrink-0 whitespace-nowrap pt-0.5 text-xs font-semibold transition-colors ${active ? 'text-[var(--ink-primary)]' : 'text-[var(--ink-muted)] hover:text-[var(--ink-secondary)]'}`
                }
              >
                {pill && ghost === option.value && (
                  <MotionSpan
                    aria-hidden="true"
                    layoutId="ghost"
                    transition={glide}
                    className="pointer-events-none absolute -inset-px rounded-lg"
                    style={{ background: 'color-mix(in srgb, var(--ink-primary) 6%, transparent)' }}
                  />
                )}
                {pill && active && (
                  <MotionSpan
                    aria-hidden="true"
                    layoutId="pill"
                    transition={glide}
                    className="pointer-events-none absolute -inset-px rounded-lg border border-[var(--outline-strong)] bg-[var(--surface-paper)] shadow-sm"
                  />
                )}
                <span className="relative">{option.label}</span>
                {!pill && active && (
                  <span aria-hidden="true" className="absolute inset-x-0 -bottom-px h-0.5 bg-[var(--accent-hex)]" />
                )}
              </button>
            );
          })}
        </div>
        </LayoutGroup>
      </MotionDiv>
      <div aria-hidden="true" className={`pointer-events-none absolute inset-y-px right-0 w-7 bg-gradient-to-l to-transparent sm:hidden ${pill ? 'rounded-r-xl from-[var(--surface-soft)]' : 'from-[var(--surface-canvas)]'}`} />
    </div>
  );
}
