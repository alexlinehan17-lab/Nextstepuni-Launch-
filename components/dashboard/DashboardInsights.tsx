/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { ChevronDown } from 'lucide-react';
import type { DashboardInsightItem, DashboardTrend } from './dashboardInsightAnalytics';

const TREND_LABEL: Record<DashboardTrend, string> = {
  upward: 'Trending upward',
  downward: 'Trending downward',
  steady: 'Steady',
  varied: 'Varied',
  building: 'Building a trend',
};

const TREND_STYLE: Record<DashboardTrend, { dot: string; text: string }> = {
  upward: { dot: 'bg-success', text: 'text-[var(--success-tint-ink)]' },
  downward: { dot: 'bg-[var(--danger-tint-ink)]', text: 'text-[var(--danger-tint-ink)]' },
  steady: { dot: 'bg-[var(--ink-muted)]', text: 'text-[var(--ink-secondary)]' },
  varied: { dot: 'bg-[var(--warning-text)]', text: 'text-[var(--ink-secondary)]' },
  building: { dot: 'bg-[var(--accent-hex)]', text: 'text-[var(--ink-secondary)]' },
};

export const InsightsToggle: React.FC<{
  controls: string;
  expanded: boolean;
  onToggle: () => void;
  chartLabel: string;
}> = ({ controls, expanded, onToggle, chartLabel }) => (
  <button
    type="button"
    aria-controls={controls}
    aria-expanded={expanded}
    aria-label={`${expanded ? 'Hide' : 'Show'} ${chartLabel} insights`}
    onClick={onToggle}
    className="inline-flex min-h-10 items-center gap-2 rounded-xl border border-[var(--outline-soft)] bg-[var(--surface-paper)] px-3 text-xs font-semibold text-[var(--ink-secondary)] transition-colors hover:border-[var(--outline-strong)] hover:text-[var(--ink-primary)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--focus-ring)]"
  >
    Insights
    <ChevronDown
      size={14}
      aria-hidden="true"
      className={`transition-transform duration-200 ${expanded ? 'rotate-180' : ''}`}
    />
  </button>
);

const DashboardInsights: React.FC<{
  id: string;
  items: DashboardInsightItem[];
  context: string;
  note?: string;
}> = ({ id, items, context, note }) => (
  <section id={id} aria-label="Chart insights" className="mb-5 border-b border-[var(--outline-soft)] pb-5">
    <div className="flex flex-wrap items-baseline justify-between gap-x-4 gap-y-1">
      <h3 className="font-serif text-lg font-semibold text-[var(--ink-primary)]">What the pattern suggests</h3>
      <p className="text-[10px] font-bold uppercase tracking-[0.14em] text-[var(--ink-muted)]">{context}</p>
    </div>

    <div className="mt-3 divide-y divide-[var(--outline-soft)] border-y border-[var(--outline-soft)]">
      {items.map(item => {
        const style = TREND_STYLE[item.trend];
        return (
          <article key={item.id} className="grid gap-2 py-4 sm:grid-cols-[minmax(140px,0.55fr)_minmax(0,1.45fr)] sm:gap-6">
            <div>
              <h4 className="text-sm font-semibold text-[var(--ink-primary)]">{item.title}</h4>
              <p className={`mt-1 inline-flex items-center gap-1.5 text-[10px] font-bold uppercase tracking-[0.12em] ${style.text}`}>
                <span className={`h-1.5 w-1.5 rounded-full ${style.dot}`} aria-hidden="true" />
                {TREND_LABEL[item.trend]}
              </p>
            </div>
            <div>
              <p className="text-xs leading-relaxed text-[var(--ink-secondary)]">{item.evidence}</p>
              <p className="mt-1.5 text-xs leading-relaxed text-[var(--ink-primary)]">
                <span className="font-semibold">Next move:</span> {item.guidance}
              </p>
            </div>
          </article>
        );
      })}
    </div>

    {note && <p className="mt-3 text-[10px] leading-relaxed text-[var(--ink-muted)]">{note}</p>}
  </section>
);

export default DashboardInsights;
