/**
 * A compact, touch-friendly tab rail for narrow screens.
 *
 * The active option is kept in view, labels never wrap, and the soft edge
 * fade makes horizontal overflow feel intentional rather than clipped.
 */
import React, { useEffect, useRef } from 'react';
import { useReducedMotion } from '../Motion';
import { useMobileAppDesign } from '../../hooks/useMobileAppDesign';

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
  className?: string;
}

export default function HorizontalTabs<T extends string>({
  value,
  options,
  onChange,
  label,
  variant = 'underline',
  className = '',
}: HorizontalTabsProps<T>) {
  const railRef = useRef<HTMLDivElement | null>(null);
  const activeRef = useRef<HTMLButtonElement | null>(null);
  const mobileAppDesign = useMobileAppDesign();
  const reducedMotion = useReducedMotion();
  const mountedRef = useRef(false);

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

  return (
    <div className={`relative min-w-0 ${className}`}>
      <div
        ref={railRef}
        role="tablist"
        aria-label={label}
        className={`overflow-x-auto overscroll-x-contain [scrollbar-width:none] [&::-webkit-scrollbar]:hidden ${pill ? 'rounded-xl border border-[var(--outline-soft)] bg-[var(--surface-soft)] p-1' : 'border-b border-[var(--outline-soft)]'}`}
      >
        <div className={`flex min-w-max ${pill ? 'gap-1' : 'gap-5 sm:gap-7'}`}>
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
                className={pill
                  ? `min-h-11 shrink-0 whitespace-nowrap rounded-lg border px-4 text-sm font-semibold transition-colors ${active ? 'border-[var(--outline-strong)] bg-[var(--surface-paper)] text-[var(--ink-primary)] shadow-sm' : 'border-transparent text-[var(--ink-muted)] hover:text-[var(--ink-secondary)]'}`
                  : `relative min-h-11 ${mobileAppDesign ? 'min-w-11' : ''} shrink-0 whitespace-nowrap pt-0.5 text-xs font-semibold transition-colors ${active ? 'text-[var(--ink-primary)]' : 'text-[var(--ink-muted)] hover:text-[var(--ink-secondary)]'}`
                }
              >
                {option.label}
                {!pill && active && (
                  <span aria-hidden="true" className="absolute inset-x-0 -bottom-px h-0.5 bg-[var(--accent-hex)]" />
                )}
              </button>
            );
          })}
        </div>
      </div>
      <div aria-hidden="true" className={`pointer-events-none absolute inset-y-px right-0 w-7 bg-gradient-to-l to-transparent sm:hidden ${pill ? 'rounded-r-xl from-[var(--surface-soft)]' : 'from-[var(--surface-canvas)]'}`} />
    </div>
  );
}
