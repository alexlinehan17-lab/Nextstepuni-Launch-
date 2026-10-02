/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
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
 }> = ({ id, items, context, note }) => {
  const [selected, setSelected] = useState<string | null | undefined>(undefined);
  const openId = selected === null ? null : items.some(item => item.id === selected) ? selected : items[0]?.id;
  return <section id={id} aria-label="Chart insights" className="pr-insight-index">
    <header><p>{context}</p><h3>What the pattern suggests</h3></header>
    <div>{items.map(item => {
      const open = openId === item.id;
      const style = TREND_STYLE[item.trend];
      return <article key={item.id}>
        <h4 aria-label={item.title}><button type="button" aria-expanded={open} aria-controls={`${id}-${item.id}`} onClick={() => setSelected(open ? null : item.id)}>
          <span><strong>{item.title}</strong><span className={`pr-insight-trend ${style.text}`}><i className={style.dot} aria-hidden="true" />{TREND_LABEL[item.trend]}</span></span><ChevronDown size={17} aria-hidden="true" />
        </button></h4>
        {open && <div id={`${id}-${item.id}`} className="pr-insight-reading"><p>{item.evidence}</p><div><strong>Try next</strong><p>{item.guidance}</p></div></div>}
      </article>;
    })}</div>
    {note && <footer>{note}</footer>}
  </section>;
};

export default DashboardInsights;
