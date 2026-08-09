/**
 * Shared product states: deliberately quiet enough for utility screens, but
 * built from the same paper, charcoal and orange language as the rest of the app.
 */
import React from 'react';
import { AlertTriangle, Inbox, RefreshCw, type LucideIcon } from 'lucide-react';

interface StatePanelProps {
  title: string;
  description: string;
  icon?: LucideIcon;
  actionLabel?: string;
  onAction?: () => void;
  tone?: 'neutral' | 'error';
  compact?: boolean;
  className?: string;
}

export const StatePanel: React.FC<StatePanelProps> = ({
  title,
  description,
  icon: Icon,
  actionLabel,
  onAction,
  tone = 'neutral',
  compact = false,
  className = '',
}) => {
  const StateIcon = Icon ?? (tone === 'error' ? AlertTriangle : Inbox);
  return (
    <section
      role={tone === 'error' ? 'alert' : 'status'}
      className={`rounded-2xl border-[1.5px] border-[var(--outline-strong)] bg-[var(--surface-paper)] text-center shadow-[4px_4px_0_0_var(--outline-strong)] ${compact ? 'px-5 py-6' : 'px-6 py-10 sm:px-10'} ${className}`}
    >
      <div className={`mx-auto flex items-center justify-center rounded-xl border-[1.5px] border-[var(--outline-strong)] ${tone === 'error' ? 'bg-[#FFF0E7] dark:bg-[#3A2118] text-[#C54B18] dark:text-[#FF9A68]' : 'bg-[var(--surface-raised)] text-[#F26B1F]'} ${compact ? 'h-10 w-10' : 'h-12 w-12'}`}>
        <StateIcon size={compact ? 19 : 22} strokeWidth={1.8} />
      </div>
      <h3 className={`font-serif font-semibold text-[var(--ink-primary)] ${compact ? 'mt-3 text-lg' : 'mt-4 text-xl'}`}>{title}</h3>
      <p className="mx-auto mt-1.5 max-w-md text-sm leading-6 text-[var(--ink-secondary)]">{description}</p>
      {actionLabel && onAction && (
        <button
          type="button"
          onClick={onAction}
          className="mt-5 inline-flex min-h-11 items-center justify-center gap-2 rounded-xl border-2 border-[#1A1A1A] bg-[#F26B1F] px-5 py-2.5 text-sm font-bold text-white shadow-[3px_3px_0_0_#1A1A1A] transition-transform hover:-translate-y-0.5 active:translate-x-0.5 active:translate-y-0.5 active:shadow-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#F26B1F] focus-visible:ring-offset-2"
        >
          {tone === 'error' && <RefreshCw size={15} />}
          {actionLabel}
        </button>
      )}
    </section>
  );
};

export const LoadingState: React.FC<{ label?: string; rows?: number; className?: string }> = ({
  label = 'Getting things ready',
  rows = 3,
  className = '',
}) => (
  <div role="status" aria-live="polite" className={`mx-auto w-full max-w-2xl px-4 py-10 ${className}`}>
    <span className="sr-only">{label}</span>
    <div className="rounded-2xl border-[1.5px] border-[var(--outline-strong)] bg-[var(--surface-paper)] p-5 shadow-[4px_4px_0_0_var(--outline-strong)]">
      <div className="mb-5 flex items-center gap-3">
        <span className="system-shimmer h-10 w-10 rounded-xl" />
        <div className="flex-1 space-y-2">
          <span className="system-shimmer block h-3 w-32 rounded" />
          <span className="system-shimmer block h-2.5 w-48 max-w-full rounded" />
        </div>
      </div>
      <div className="space-y-3">
        {Array.from({ length: rows }, (_, index) => (
          <div key={index} className="flex items-center gap-3 rounded-xl border border-[var(--outline-soft)] bg-[var(--surface-raised)] p-3">
            <span className="system-shimmer h-8 w-8 shrink-0 rounded-lg" />
            <span className="system-shimmer h-3 rounded" style={{ width: `${72 - index * 9}%` }} />
          </div>
        ))}
      </div>
    </div>
  </div>
);
