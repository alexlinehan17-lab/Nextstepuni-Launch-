import { useState, type CSSProperties } from 'react';
import type { DashboardSection } from '../../../contexts/NavigationContext';
import type { RankedValue, MasterySummary } from '../dashboardAnalytics';
import { Eyebrow } from './shared';

export function ProgressSections({ value, onChange, options }: {
  value: DashboardSection;
  onChange: (value: DashboardSection) => void;
  options: { id: DashboardSection; label: string }[];
}) {
  return <nav className="pr-paper-tabs" aria-label="Progress sections"><div role="tablist" aria-label="Dashboard sections">{options.map((item, index) => <button
    type="button" key={item.id} role="tab" aria-selected={value === item.id} tabIndex={value === item.id ? 0 : -1}
    onClick={() => onChange(item.id)} onKeyDown={event => {
      const next = event.key === 'ArrowRight' ? (index + 1) % options.length : event.key === 'ArrowLeft' ? (index + options.length - 1) % options.length : event.key === 'Home' ? 0 : event.key === 'End' ? options.length - 1 : -1;
      if (next < 0) return;
      event.preventDefault(); onChange(options[next].id);
      (event.currentTarget.parentElement?.children[next] as HTMLButtonElement)?.focus();
    }}><span aria-hidden="true">{String(index + 1).padStart(2, '0')}</span>{item.label}</button>)}</div></nav>;
}

const mixDetails: Record<string, { colour: string; note: string }> = {
  'new-learning': { colour: '#eb692a', note: 'Getting started with unfamiliar material.' },
  practice: { colour: '#397f7c', note: 'Putting what you know to work.' },
  revision: { colour: '#b27d2d', note: 'Returning to material you have studied.' },
};
export function ProgressBreakdown({ kind, values = [], summary, period, className = '' }: {
  kind: 'mix' | 'readiness'; values?: RankedValue[]; summary?: MasterySummary; period?: string; className?: string;
}) {
  const [selected, setSelected] = useState<string | null>(null);
  const data = kind === 'mix' ? values.map(item => ({ ...item, ...mixDetails[item.id] })) : [
    { id: 'not-started', label: 'Not started', value: summary?.notStarted ?? 0, colour: '#999da4', note: 'Topics with no recorded readiness yet.' },
    { id: 'shaky', label: 'Shaky', value: summary?.shaky ?? 0, colour: '#b27d2d', note: 'Topics that would benefit from another look.' },
    { id: 'solid', label: 'Solid', value: summary?.solid ?? 0, colour: '#397f7c', note: 'Topics you currently feel secure with.' },
  ];
  const total = data.reduce((sum, item) => sum + item.value, 0);
  const unit = kind === 'mix' ? 'sessions' : 'topics';
  return <article className={`pr-paper pr-breakdown ${className}`}>
    <header><Eyebrow>{kind === 'mix' ? 'Session design' : 'Current picture'}</Eyebrow><div className="pr-breakdown-title"><h2>{kind === 'mix' ? 'Learning mix' : 'Topic readiness'}</h2><span><strong>{total}</strong> {unit}</span></div><p>{kind === 'mix' ? 'How you spent your study sessions.' : 'How your topics feel right now.'}</p></header>
    <div className="pr-breakdown-body"><div className="pr-breakdown-items" role="group" aria-label={kind === 'mix' ? 'Session types' : 'Readiness levels'}>{data.map(item => <button type="button" key={item.id} aria-pressed={selected === item.id} onClick={() => setSelected(item.id)} style={{ '--item-colour': item.colour } as CSSProperties}>
      <span className="pr-breakdown-label"><i aria-hidden="true" />{item.label}</span><strong>{total ? Math.round(item.value / total * 100) : 0}<small>%</small></strong><span className="pr-breakdown-count">{item.value} {unit}</span><span className="pr-breakdown-track" aria-hidden="true"><i style={{ width: `${total ? item.value / total * 100 : 0}%` }} /></span>
    </button>)}</div><p className="pr-breakdown-reading" role="status">{!total ? `No ${unit} recorded yet.` : data.find(item => item.id === selected)?.note ?? 'Select a category to read more.'}</p></div>
    <footer>{kind === 'mix' ? `Recorded sessions${period ? ` · ${period}` : ' in the selected period'}.` : 'Current snapshot · subject filter applies; date range does not.'}</footer>
  </article>;
}
