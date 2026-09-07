/**
 * Shared selection controls for compact product choices.
 *
 * The colour hierarchy is deliberate: orange communicates interaction and
 * selection; optional subject colours remain a small identity cue. These are
 * controls, not tags, so they use a softly squared shape and a full focus ring.
 */

import React from 'react';

interface ChoiceControlProps extends Omit<React.ButtonHTMLAttributes<HTMLButtonElement>, 'children'> {
  label: string;
  selected: boolean;
  icon?: React.ReactNode;
  markerClassName?: string;
  markerColor?: string;
  trailing?: React.ReactNode;
  compact?: boolean;
}

export const ChoiceControl: React.FC<ChoiceControlProps> = ({
  label,
  selected,
  icon,
  markerClassName,
  markerColor,
  trailing,
  compact = false,
  className = '',
  style,
  ...rest
}) => (
  <button
    type="button"
    aria-pressed={selected}
    className={`group inline-flex min-h-11 items-center justify-center gap-2 rounded-xl border-2 text-left font-medium transition-[background-color,border-color,color,box-shadow,transform] duration-150 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[rgba(var(--accent),0.38)] focus-visible:ring-offset-2 ${
      compact ? 'px-3 py-2 text-xs' : 'px-4 py-2.5 text-[13px]'
    } ${
      selected
        ? 'border-[#1A1A1A] bg-[#F26B1F] text-[#1A1A1A]'
        : 'border-[#E5E1DB] bg-white text-[var(--text-body)] hover:border-[#1A1A1A] hover:bg-white active:translate-y-px dark:border-zinc-700 dark:bg-zinc-900 dark:hover:bg-zinc-800'
    } ${className}`}
    style={style}
    {...rest}
  >
    {(markerClassName || markerColor) && (
      <span
        aria-hidden="true"
        className={`h-2 w-2 shrink-0 rounded-full ${markerClassName ?? ''}`}
        style={selected
          ? { backgroundColor: 'transparent', boxShadow: 'inset 0 0 0 1.5px #1A1A1A' }
          : markerColor ? { backgroundColor: markerColor } : undefined}
      />
    )}
    {icon && (
      <span
        aria-hidden="true"
        className={`shrink-0 ${selected ? 'text-[#1A1A1A]' : 'text-[var(--text-muted)]'}`}
      >
        {icon}
      </span>
    )}
    <span className="min-w-0 leading-snug">{label}</span>
    {trailing}
  </button>
);

export default ChoiceControl;
