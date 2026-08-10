/**
 * Shared result language for reflective and strategic NextStepUni experiences.
 * The shell provides hierarchy and actions; feature components provide meaning.
 */

import React from 'react';
import { ArrowRight, RotateCcw } from 'lucide-react';
import { type ResultStat, OutlinedSurface, ResultStatGrid } from './ProductPatterns';

const SANS = "'DM Sans', system-ui, sans-serif";

export interface OutcomeAction {
  label: string;
  onClick: () => void;
}

export const OutcomeShell: React.FC<{
  eyebrow: string;
  title: string;
  summary: React.ReactNode;
  illustration?: React.ReactNode;
  metrics: ResultStat[];
  primaryAction?: OutcomeAction;
  secondaryAction?: OutcomeAction;
  children: React.ReactNode;
}> = ({ eyebrow, title, summary, illustration, metrics, primaryAction, secondaryAction, children }) => (
  <div className="outcome-shell space-y-7 pb-14 pt-2 sm:space-y-9 sm:pt-4">
    <OutlinedSurface strong className="overflow-hidden">
      <div className="grid gap-5 p-6 sm:p-8 md:grid-cols-[1fr_auto] md:items-start">
        <div className="min-w-0">
          <p className="text-[10px] font-bold uppercase tracking-[.2em] text-[var(--ink-muted)]" style={{ fontFamily: SANS }}>
            {eyebrow}
          </p>
          <h2 className="mt-3 max-w-3xl font-serif text-[36px] font-semibold leading-[1.02] tracking-[-.025em] text-[var(--ink-primary)] sm:text-[48px]">
            {title}
          </h2>
          <div className="mt-4 max-w-2xl font-serif text-[16px] leading-relaxed text-[var(--ink-secondary)] sm:text-[17px]">
            {summary}
          </div>
        </div>
        {illustration && <div className="hidden sm:block" aria-hidden="true">{illustration}</div>}
      </div>

      <div className="border-t border-[var(--outline-soft)] p-4 sm:p-6">
        <ResultStatGrid items={metrics} />
      </div>

      {(primaryAction || secondaryAction) && (
        <div className="flex flex-col gap-3 border-t border-[var(--outline-soft)] px-6 py-5 sm:flex-row sm:items-center">
          {primaryAction && (
            <button
              type="button"
              onClick={primaryAction.onClick}
              className="inline-flex min-h-12 items-center justify-center gap-2 rounded-xl border-[1.5px] border-[var(--outline-strong)] bg-[#F26B1F] px-5 text-sm font-semibold text-white shadow-[3px_3px_0_var(--outline-strong)] transition-transform hover:-translate-y-0.5"
            >
              {primaryAction.label}<ArrowRight size={16} aria-hidden="true" />
            </button>
          )}
          {secondaryAction && (
            <button
              type="button"
              onClick={secondaryAction.onClick}
              className="inline-flex min-h-12 items-center justify-center gap-2 rounded-xl border border-[var(--outline-soft)] bg-[var(--surface-paper)] px-5 text-sm font-semibold text-[var(--ink-primary)] transition-colors hover:bg-[var(--surface-soft)]"
            >
              <RotateCcw size={15} aria-hidden="true" />{secondaryAction.label}
            </button>
          )}
        </div>
      )}
    </OutlinedSurface>
    {children}
  </div>
);

export const OutcomeSection: React.FC<{
  eyebrow?: string;
  title: string;
  children: React.ReactNode;
  className?: string;
}> = ({ eyebrow, title, children, className = '' }) => (
  <section className={className}>
    {eyebrow && <p className="text-[10px] font-bold uppercase tracking-[.18em] text-[var(--ink-muted)]">{eyebrow}</p>}
    <h3 className="mt-1.5 font-serif text-[24px] font-semibold text-[var(--ink-primary)]">{title}</h3>
    <div className="mt-4">{children}</div>
  </section>
);

export const EvidenceDisclosure: React.FC<{
  summary: string;
  description?: string;
  children: React.ReactNode;
  defaultOpen?: boolean;
}> = ({ summary, description, children, defaultOpen = false }) => (
  <details className="outcome-disclosure border-b border-[var(--outline-soft)]" open={defaultOpen}>
    <summary className="cursor-pointer list-none py-5 focus-visible:outline-none">
      <span className="flex items-center justify-between gap-5">
        <span>
          <strong className="block font-serif text-[17px] font-semibold text-[var(--ink-primary)]">{summary}</strong>
          {description && <span className="mt-1 block text-xs leading-relaxed text-[var(--ink-muted)]">{description}</span>}
        </span>
        <span className="outcome-disclosure-mark text-xl text-[var(--ink-muted)]" aria-hidden="true">+</span>
      </span>
    </summary>
    <div className="pb-6">{children}</div>
  </details>
);
