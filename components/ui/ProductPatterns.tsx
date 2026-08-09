/**
 * Approved product-level patterns shared by focused learning tools.
 *
 * These deliberately contain structure, not feature semantics: callers supply
 * the words and values, while the component keeps borders, spacing, hierarchy
 * and responsive behaviour consistent across Study, Mark Bank and future tools.
 */

import React from 'react';

const SANS = "'DM Sans', system-ui, sans-serif";
const MONO = "'Roboto Mono', ui-monospace, monospace";

export interface ResultStat {
  label: string;
  value: React.ReactNode;
  icon?: React.ReactNode;
  tone?: 'default' | 'success' | 'accent';
}

const statColour = (tone: ResultStat['tone']) => {
  if (tone === 'success') return '#1F5F3E';
  if (tone === 'accent') return '#A43F08';
  return 'var(--ink-primary)';
};

export const ResultStatGrid: React.FC<{ items: ResultStat[]; className?: string }> = ({ items, className = '' }) => (
  <div
    className={className}
    style={{
      display: 'grid', gridTemplateColumns: `repeat(${items.length}, minmax(0, 1fr))`,
      overflow: 'hidden', border: '1.5px solid var(--outline-soft)', borderRadius: 16,
      background: 'var(--surface-paper)',
    }}
  >
    {items.map((item, index) => (
      <div
        key={item.label}
        style={{
          minWidth: 0, padding: '16px 14px', textAlign: 'center',
          borderLeft: index ? '1px solid var(--outline-soft)' : 'none',
        }}
      >
        {item.icon && <span style={{ display: 'flex', justifyContent: 'center', marginBottom: 6, color: 'var(--ink-muted)' }}>{item.icon}</span>}
        <strong style={{
          display: 'block', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
          font: `700 15px/1.2 ${MONO}`, color: statColour(item.tone), fontVariantNumeric: 'tabular-nums',
        }}>
          {item.value}
        </strong>
        <span style={{
          display: 'block', marginTop: 5, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
          font: `700 9px/1.4 ${SANS}`, letterSpacing: '.1em', textTransform: 'uppercase', color: 'var(--ink-muted)',
        }}>
          {item.label}
        </span>
      </div>
    ))}
  </div>
);

type NoticeTone = 'neutral' | 'success' | 'warning';

export const StatusNotice: React.FC<{
  title: string;
  children: React.ReactNode;
  tone?: NoticeTone;
  action?: { label: string; onClick: () => void };
  className?: string;
}> = ({ title, children, tone = 'neutral', action, className = '' }) => {
  const palette = tone === 'success'
    ? { background: '#E8F2EC', border: '#BFD8C8', title: '#1F5F3E' }
    : tone === 'warning'
      ? { background: '#FFF8F2', border: '#383838', title: '#1A1A1A' }
      : { background: 'var(--surface-paper)', border: 'var(--outline-soft)', title: 'var(--ink-primary)' };

  return (
    <div className={className} style={{ padding: '13px 14px', border: `1px solid ${palette.border}`, borderRadius: 12, background: palette.background }}>
      <p style={{ margin: 0, font: `650 12px/1.45 ${SANS}`, color: palette.title }}>{title}</p>
      <div style={{ marginTop: 2, font: `400 11.5px/1.5 ${SANS}`, color: 'var(--ink-secondary)' }}>{children}</div>
      {action && (
        <button
          type="button"
          onClick={action.onClick}
          style={{ marginTop: 10, padding: '8px 11px', borderRadius: 9, border: '1.5px solid var(--outline-strong)', background: 'var(--surface-paper)', color: 'var(--ink-primary)', font: `650 11.5px/1 ${SANS}`, cursor: 'pointer' }}
        >
          {action.label}
        </button>
      )}
    </div>
  );
};

export const OutlinedSurface: React.FC<React.HTMLAttributes<HTMLDivElement> & { strong?: boolean }> = ({ strong = false, style, ...props }) => (
  <div
    {...props}
    style={{
      background: 'var(--surface-paper)', border: strong ? '1.5px solid var(--outline-strong)' : '1px solid var(--outline-soft)',
      borderRadius: 16, boxShadow: '0 12px 28px rgba(38,32,27,.045)', color: 'var(--ink-primary)',
      ...style,
    }}
  />
);
