/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useMemo, useState } from 'react';
import { ArrowLeft, Printer, ArrowRight, FileText } from 'lucide-react';
import { CUT_CONTENT, type CutContentEntry, type CutAction } from '../data/cutContent';

interface CutContentPageProps {
  onBack: () => void;
}

const SERIF = "'Source Serif 4', serif";

// ── Palette (Mercury / data-dense register) ──────────────────────────────────
const INK = 'var(--ink-primary)';
const HAIRLINE = 'var(--hairline)';
const PAGE = 'var(--page-canvas)';
const PANEL = 'var(--surface-soft)';
const MUTED = 'var(--page-muted)';
const LABEL = 'var(--page-label)';
const FAINT = 'var(--ink-faint)';
const ACCENT = '#F26B1F';
const ACCENT_TINT = 'var(--accent-tint)';
const ACCENT_DARK_TEXT = 'var(--accent-tint-ink)';
const SUCCESS_TINT = 'var(--success-tint)';
const SUCCESS_DARK_TEXT = 'var(--success-tint-ink)';

type FilterKey = 'all' | CutAction | 'awaiting';

// Token-compliant only: reframed = success (kept, softened); corrected = accent
// (attention — a fix was needed); removed = neutral (absence). No blue/purple.
const ACTION_META: Record<CutAction, { label: string; tint: string; text: string; border: string }> = {
  reframed: { label: 'Reframed', tint: SUCCESS_TINT, text: SUCCESS_DARK_TEXT, border: 'rgba(58,141,95,0.3)' },
  corrected: { label: 'Corrected', tint: ACCENT_TINT, text: ACCENT_DARK_TEXT, border: 'rgba(242,107,31,0.25)' },
  removed: { label: 'Removed', tint: 'var(--neutral-tint)', text: MUTED, border: '#d0cdc8' },
};

const MicroLabel: React.FC<{ children: React.ReactNode; color?: string; className?: string }> = ({
  children,
  color = LABEL,
  className = '',
}) => (
  <p
    className={`text-[10px] font-bold uppercase tracking-[0.14em] ${className}`}
    style={{ color, fontFamily: "'DM Sans', sans-serif" }}
  >
    {children}
  </p>
);

const ActionPill: React.FC<{ action: CutAction }> = ({ action }) => {
  const m = ACTION_META[action];
  return (
    <span
      className="inline-flex items-center px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-[0.08em]"
      style={{ backgroundColor: m.tint, color: m.text, border: `1px solid ${m.border}`, fontFamily: "'DM Sans', sans-serif" }}
    >
      {m.label}
    </span>
  );
};

// ── Executive-summary statistic ──────────────────────────────────────────────
const Stat: React.FC<{ value: number | string; label: string; accent?: boolean }> = ({ value, label, accent }) => (
  <div className="flex flex-col gap-1">
    <span
      className="text-4xl md:text-5xl font-semibold leading-none"
      style={{ fontFamily: SERIF, color: accent ? ACCENT : INK }}
    >
      {value}
    </span>
    <MicroLabel>{label}</MicroLabel>
  </div>
);

// ── A single change, as a before → after diff ────────────────────────────────
const DiffEntry: React.FC<{ entry: CutContentEntry }> = ({ entry }) => {
  const hasReplacement = Boolean(entry.reframedTo);
  const afterLabel = entry.action === 'corrected' ? 'Corrected to' : 'Now reads';

  return (
    <div className="py-5" style={{ breakInside: 'avoid' }}>
      {/* Meta row */}
      <div className="flex items-center justify-between gap-3 mb-3">
        <div className="flex items-center gap-2.5 min-w-0">
          <ActionPill action={entry.action} />
          <span className="text-[12px] truncate" style={{ color: MUTED, fontFamily: "'DM Sans', sans-serif" }}>
            {entry.section}
          </span>
        </div>
        <span className="text-[11px] shrink-0" style={{ color: FAINT, fontFamily: "'DM Sans', sans-serif" }}>
          {entry.date}
        </span>
      </div>

      {/* Diff */}
      <div className="flex flex-col md:flex-row md:items-stretch gap-2.5 md:gap-3">
        {/* Original */}
        <div
          className="flex-1 rounded-xl p-3.5"
          style={{ backgroundColor: PANEL, border: `1px solid ${HAIRLINE}` }}
        >
          <MicroLabel className="mb-1.5">Original</MicroLabel>
          <p
            className="text-[13px] leading-relaxed"
            style={{
              color: MUTED,
              fontFamily: "'DM Sans', sans-serif",
              textDecoration: hasReplacement ? 'none' : 'line-through',
            }}
          >
            {entry.original}
          </p>
        </div>

        {/* Connector */}
        <div className="flex md:flex-col items-center justify-center shrink-0" aria-hidden>
          <ArrowRight size={16} style={{ color: FAINT }} className="rotate-90 md:rotate-0" />
        </div>

        {/* Replacement (or removed note) */}
        {hasReplacement ? (
          <div className="flex-1 rounded-xl p-3.5" style={{ backgroundColor: 'white', border: `1px solid ${HAIRLINE}` }}>
            <MicroLabel className="mb-1.5" color={ACTION_META[entry.action].text}>
              {afterLabel}
            </MicroLabel>
            <p className="text-[13px] leading-relaxed" style={{ color: INK, fontFamily: "'DM Sans', sans-serif" }}>
              {entry.reframedTo}
            </p>
          </div>
        ) : (
          <div
            className="flex-1 rounded-xl p-3.5 flex items-center"
            style={{ backgroundColor: 'white', border: `1px dashed ${HAIRLINE}` }}
          >
            <p className="text-[12px] italic" style={{ color: FAINT, fontFamily: "'DM Sans', sans-serif" }}>
              Removed — no replacement.
            </p>
          </div>
        )}
      </div>

      {/* Reason */}
      <div className="flex items-baseline gap-2.5 mt-3">
        <MicroLabel className="shrink-0 translate-y-px">Why</MicroLabel>
        <p className="text-[12.5px] leading-relaxed" style={{ color: MUTED, fontFamily: "'DM Sans', sans-serif" }}>
          {entry.reason}
        </p>
      </div>

      {/* Awaiting source — restorable once the paper is supplied */}
      {entry.awaitingSource && (
        <div
          className="mt-3 rounded-lg px-3.5 py-2.5"
          style={{ backgroundColor: ACCENT_TINT, borderLeft: `3px solid ${ACCENT}` }}
        >
          <MicroLabel color={ACCENT_DARK_TEXT} className="mb-1">
            Restorable once sourced
          </MicroLabel>
          {entry.neededSource && (
            <p className="text-[12px] leading-relaxed" style={{ color: ACCENT_DARK_TEXT, fontFamily: "'DM Sans', sans-serif" }}>
              {entry.neededSource}
            </p>
          )}
        </div>
      )}
    </div>
  );
};

const CutContentPage: React.FC<CutContentPageProps> = ({ onBack }) => {
  const [filter, setFilter] = useState<FilterKey>('all');

  // ── Derived stats (all from the data — nothing hardcoded) ──────────────────
  const stats = useMemo(() => {
    const reframed = CUT_CONTENT.filter(e => e.action === 'reframed').length;
    const corrected = CUT_CONTENT.filter(e => e.action === 'corrected').length;
    const removed = CUT_CONTENT.filter(e => e.action === 'removed').length;
    const awaiting = CUT_CONTENT.filter(e => e.awaitingSource).length;
    const modules = new Set(CUT_CONTENT.map(e => e.module)).size;
    return { total: CUT_CONTENT.length, reframed, corrected, removed, awaiting, modules };
  }, []);

  // ── Filter chips (only show buckets that exist) ────────────────────────────
  const chips = useMemo(() => {
    const list: { key: FilterKey; label: string; count: number }[] = [
      { key: 'all', label: 'All', count: stats.total },
      { key: 'reframed', label: 'Reframed', count: stats.reframed },
      { key: 'corrected', label: 'Corrected', count: stats.corrected },
      { key: 'removed', label: 'Removed', count: stats.removed },
      { key: 'awaiting', label: 'Awaiting source', count: stats.awaiting },
    ];
    return list.filter(c => c.key === 'all' || c.count > 0);
  }, [stats]);

  const matches = (e: CutContentEntry): boolean => {
    if (filter === 'all') return true;
    if (filter === 'awaiting') return Boolean(e.awaitingSource);
    return e.action === filter;
  };

  // ── Group by module, preserving first-appearance order ─────────────────────
  const groups = useMemo(() => {
    const map = new Map<string, CutContentEntry[]>();
    for (const e of CUT_CONTENT) {
      const arr = map.get(e.module) ?? [];
      arr.push(e);
      map.set(e.module, arr);
    }
    return Array.from(map.entries()).map(([module, entries]) => ({ module, entries }));
  }, []);

  return (
    <div className="min-h-screen print:bg-white theme-compat" style={{ backgroundColor: PAGE }}>
      {/* Masthead */}
      <header
        className="sticky top-0 z-30 px-4 md:px-10 backdrop-blur-sm border-b print:static print:bg-white print:backdrop-blur-none"
        style={{ backgroundColor: 'color-mix(in srgb, var(--page-canvas) 90%, transparent)', borderColor: HAIRLINE, paddingTop: 'calc(16px + var(--sat, 0px))', paddingBottom: '16px' }}
      >
        <div className="max-w-4xl mx-auto flex items-center justify-between gap-4">
          <div className="flex items-center gap-4 min-w-0">
            <button
              onClick={onBack}
              className="p-2.5 rounded-xl transition-colors hover:bg-white print:hidden shrink-0"
              style={{ border: '1px solid rgba(0,0,0,0.08)', backgroundColor: 'white' }}
              aria-label="Back"
            >
              <ArrowLeft size={18} style={{ color: INK }} />
            </button>
            <div className="min-w-0">
              <MicroLabel color={ACCENT}>Pre-accreditation review</MicroLabel>
              <h1
                className="text-lg md:text-xl font-semibold leading-tight mt-0.5"
                style={{ fontFamily: SERIF, color: INK }}
              >
                Content Verification Log
              </h1>
            </div>
          </div>
          <button
            onClick={() => window.print()}
            className="inline-flex items-center gap-2 px-3.5 py-2 rounded-xl text-[13px] font-semibold transition-colors hover:bg-white print:hidden shrink-0"
            style={{ border: '1px solid rgba(0,0,0,0.1)', backgroundColor: 'white', color: MUTED, fontFamily: "'DM Sans', sans-serif" }}
          >
            <Printer size={15} />
            <span className="hidden sm:inline">Export / Print</span>
          </button>
        </div>
      </header>

      <div className="max-w-4xl mx-auto px-4 md:px-10 py-6 md:py-9">
        {/* Executive summary */}
        <section
          className="rounded-2xl px-5 md:px-8 py-6 md:py-7 mb-5"
          style={{ backgroundColor: 'white', border: `1px solid ${HAIRLINE}`, breakInside: 'avoid' }}
        >
          <div className="grid grid-cols-2 md:grid-cols-4 gap-y-6 gap-x-4 md:gap-x-8">
            <Stat value={stats.total} label="Changes logged" />
            <Stat value={stats.modules} label="Modules reviewed" />
            <Stat value={stats.reframed} label="Reframed" />
            <Stat value={stats.corrected} label="Corrected" />
          </div>
          {(stats.awaiting > 0 || stats.removed > 0) && (
            <div className="mt-6 pt-5 flex flex-wrap items-center gap-x-2 gap-y-1" style={{ borderTop: `1px solid ${HAIRLINE}` }}>
              <span className="text-[13px]" style={{ color: MUTED, fontFamily: "'DM Sans', sans-serif" }}>
                {stats.removed > 0 && <><strong style={{ color: INK }}>{stats.removed}</strong> removed outright · </>}
                <strong style={{ color: ACCENT }}>{stats.awaiting}</strong> reframed only because a primary source is
                paywalled — restorable verbatim once the paper is supplied.
              </span>
            </div>
          )}
        </section>

        {/* Methodology */}
        <section
          className="rounded-2xl px-5 md:px-8 py-6 mb-7"
          style={{ backgroundColor: PANEL, border: `1px solid ${HAIRLINE}`, breakInside: 'avoid' }}
        >
          <h2 className="text-[15px] font-semibold mb-2.5" style={{ fontFamily: SERIF, color: INK }}>
            How this log was produced
          </h2>
          <p className="text-[13.5px] leading-relaxed" style={{ color: '#5a5550', fontFamily: "'DM Sans', sans-serif" }}>
            Every claim in these modules is held to one rule: we only state or advise something that a real, locatable
            source genuinely supports — peer-reviewed literature for the learning-science content, and official State
            Examinations Commission / CAO documents for the exam content. Any claim that could not be verified was
            reframed to non-prescriptive language or removed outright. <strong style={{ color: INK }}>A citation was
            never invented to keep a claim.</strong> Every such change is recorded below.
          </p>
          {/* Legend */}
          <div className="mt-4 flex flex-wrap gap-x-5 gap-y-2">
            {[
              { a: 'reframed' as CutAction, d: 'softened to what the evidence supports' },
              { a: 'corrected' as CutAction, d: 'a factual error fixed against an authoritative source' },
              { a: 'removed' as CutAction, d: 'cut with no replacement' },
            ].map(({ a, d }) => (
              <div key={a} className="flex items-center gap-2">
                <ActionPill action={a} />
                <span className="text-[11.5px]" style={{ color: LABEL, fontFamily: "'DM Sans', sans-serif" }}>
                  {d}
                </span>
              </div>
            ))}
          </div>
        </section>

        {/* Filter chips */}
        {CUT_CONTENT.length > 0 && (
          <div className="flex flex-wrap gap-2 mb-6 print:hidden">
            {chips.map(chip => {
              const active = filter === chip.key;
              return (
                <button
                  key={chip.key}
                  onClick={() => setFilter(chip.key)}
                  className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full text-[12.5px] font-semibold transition-colors"
                  style={{
                    fontFamily: "'DM Sans', sans-serif",
                    backgroundColor: active ? ACCENT : 'white',
                    color: active ? 'white' : MUTED,
                    border: `1px solid ${active ? ACCENT : HAIRLINE}`,
                  }}
                >
                  {chip.label}
                  <span
                    className="text-[10.5px] font-bold px-1.5 rounded-full"
                    style={{
                      backgroundColor: active ? 'rgba(255,255,255,0.22)' : '#f0eeec',
                      color: active ? 'white' : FAINT,
                    }}
                  >
                    {chip.count}
                  </span>
                </button>
              );
            })}
          </div>
        )}

        {/* Entries grouped by module */}
        {CUT_CONTENT.length === 0 ? (
          <div
            className="rounded-2xl p-10 text-center"
            style={{ backgroundColor: 'white', border: `1px dashed ${HAIRLINE}` }}
          >
            <div className="w-12 h-12 mx-auto mb-3 rounded-full flex items-center justify-center" style={{ backgroundColor: PAGE }}>
              <FileText size={22} style={{ color: FAINT }} />
            </div>
            <p className="text-sm font-medium" style={{ color: MUTED }}>Nothing cut yet</p>
            <p className="text-xs mt-1" style={{ color: LABEL }}>
              As the module review proceeds, removed and reframed content will be logged here.
            </p>
          </div>
        ) : (
          <div className="space-y-7">
            {groups.map(group => {
              const visibleEntries = group.entries.filter(matches);
              // Hidden on screen when the filter excludes the whole group, but
              // always rendered for print so the exported document is complete.
              const groupHidden = visibleEntries.length === 0;
              return (
                <section
                  key={group.module}
                  className={groupHidden ? 'hidden print:block' : ''}
                  style={{ breakInside: 'avoid' }}
                >
                  {/* Module header */}
                  <div className="flex items-baseline justify-between gap-3 pb-2.5 mb-1" style={{ borderBottom: `1px solid ${HAIRLINE}` }}>
                    <h3 className="text-[15px] font-semibold" style={{ fontFamily: SERIF, color: INK }}>
                      {group.module}
                    </h3>
                    <span className="text-[11px] shrink-0" style={{ color: FAINT, fontFamily: "'DM Sans', sans-serif" }}>
                      {group.entries.length} {group.entries.length === 1 ? 'change' : 'changes'}
                    </span>
                  </div>

                  {/* Entries (hidden-but-printed when filtered out individually) */}
                  <div className="divide-y" style={{ borderColor: HAIRLINE }}>
                    {group.entries.map(entry => (
                      <div key={entry.id} className={matches(entry) ? '' : 'hidden print:block'}>
                        <DiffEntry entry={entry} />
                      </div>
                    ))}
                  </div>
                </section>
              );
            })}
          </div>
        )}

        {/* Print footer */}
        <div className="hidden print:block mt-8 pt-4 text-[10px]" style={{ borderTop: `1px solid ${HAIRLINE}`, color: LABEL, fontFamily: "'DM Sans', sans-serif" }}>
          Nextstepuni — Content Verification Log · Pre-accreditation review (DCU / Brian MacCraith)
        </div>
      </div>
    </div>
  );
};

export default CutContentPage;
