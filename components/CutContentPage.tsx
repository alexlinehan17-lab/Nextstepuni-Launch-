/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useMemo, useState } from 'react';
import { ArrowRight, Printer } from 'lucide-react';
import { CUT_CONTENT, type CutContentEntry, type CutAction } from '../data/cutContent';
import PageHeader from './ui/PageHeader';
import { IconButton } from './ui/Button';
import { Menu } from './ui/Menu';

interface CutContentPageProps {
  onBack: () => void;
}

// The system's look (area 9): one typeface, ink on the page, small capitals labels, no tints or pills.
const INK = 'var(--ink-primary)';
const HAIRLINE = 'var(--hairline)';
const MUTED = 'var(--ink-secondary)';
const FAINT = 'var(--ink-muted)';

type FilterKey = 'all' | CutAction | 'awaiting';

const ACTION_META: Record<CutAction, { label: string }> = {
  reframed: { label: 'Reframed' },
  corrected: { label: 'Corrected' },
  removed: { label: 'Removed' },
};

const MicroLabel: React.FC<{ children: React.ReactNode; className?: string }> = ({ children, className = '' }) => (
  <p className={`t-label ${className}`} style={{ color: FAINT }}>{children}</p>
);

const ActionPill: React.FC<{ action: CutAction }> = ({ action }) => (
  <span className="t-label" style={{ color: INK }}>{ACTION_META[action].label}</span>
);

// ── Executive-summary figure: the number over its small label, centred in its column ────────
const Stat: React.FC<{ value: number | string; label: string }> = ({ value, label }) => (
  <div className="flex flex-col items-center gap-1 text-center">
    <span className="t-number" style={{ color: INK }}>{value}</span>
    <MicroLabel>{label}</MicroLabel>
  </div>
);

// ── A single change, as a before → after diff, on the page ───────────────────
const DiffEntry: React.FC<{ entry: CutContentEntry }> = ({ entry }) => {
  const hasReplacement = Boolean(entry.reframedTo);
  const afterLabel = entry.action === 'corrected' ? 'Corrected to' : 'Now reads';

  return (
    <div className="py-5" style={{ breakInside: 'avoid' }}>
      {/* Meta row */}
      <div className="flex items-center justify-between gap-3 mb-3">
        <div className="flex items-baseline gap-2.5 min-w-0">
          <ActionPill action={entry.action} />
          <span className="t-meta truncate" style={{ color: MUTED }}>{entry.section}</span>
        </div>
        <span className="t-readout shrink-0" style={{ color: FAINT }}>{entry.date}</span>
      </div>

      {/* Diff */}
      <div className="flex flex-col md:flex-row md:items-start gap-2.5 md:gap-4">
        {/* Original */}
        <div className="flex-1 min-w-0">
          <MicroLabel className="mb-1.5">Original</MicroLabel>
          <p className="t-sub" style={{ color: MUTED, textDecoration: hasReplacement ? 'none' : 'line-through' }}>
            {entry.original}
          </p>
        </div>

        {/* Connector */}
        <div className="flex md:flex-col items-center justify-center shrink-0 md:pt-5" aria-hidden>
          <ArrowRight size={16} style={{ color: FAINT }} className="rotate-90 md:rotate-0" />
        </div>

        {/* Replacement (or removed note) */}
        {hasReplacement ? (
          <div className="flex-1 min-w-0">
            <MicroLabel className="mb-1.5">{afterLabel}</MicroLabel>
            <p className="t-sub" style={{ color: INK }}>{entry.reframedTo}</p>
          </div>
        ) : (
          <div className="flex-1 min-w-0 flex items-center">
            <p className="t-meta">Removed — no replacement.</p>
          </div>
        )}
      </div>

      {/* Reason */}
      <div className="flex items-baseline gap-2.5 mt-3">
        <MicroLabel className="shrink-0 translate-y-px">Why</MicroLabel>
        <p className="t-meta" style={{ color: MUTED }}>{entry.reason}</p>
      </div>

      {/* Awaiting source — restorable once the paper is supplied: a notice on the page, no tint or rail */}
      {entry.awaitingSource && (
        <div className="mt-3 pt-2.5" style={{ borderTop: `1px solid ${HAIRLINE}` }}>
          <MicroLabel className="mb-1">Restorable once sourced</MicroLabel>
          {entry.neededSource && <p className="t-meta" style={{ color: INK }}>{entry.neededSource}</p>}
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
    <div className="min-h-screen print:bg-white bg-white dark:bg-surface-canvas">
      {/* Masthead: the shared page bar (Back at the top left, the small line over the name, one
          action at the right), sticky as before; printed with its words and without its buttons, as before (area 9). */}
      <div className="sticky top-0 z-30 bg-white dark:bg-surface-canvas print:static print:[&_button]:hidden">
        <div className="max-w-4xl mx-auto">
          <PageHeader
            onBack={onBack}
            backLabel="Back to home"
            eyebrow="Pre-accreditation review"
            title="Content Verification Log"
            actions={<IconButton label="Export / Print" onClick={() => window.print()} icon={<Printer className="ui-icon" width={24} height={24} strokeWidth={1.75} aria-hidden="true" focusable="false" />} />}
          />
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 md:px-10 py-6 md:py-9">
        {/* Executive summary: the figures in a line, centred, on the page */}
        <section className="pb-6 mb-6" style={{ borderBottom: `1px solid ${HAIRLINE}`, breakInside: 'avoid' }}>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-y-6 gap-x-4 md:gap-x-8">
            <Stat value={stats.total} label="Changes logged" />
            <Stat value={stats.modules} label="Modules reviewed" />
            <Stat value={stats.reframed} label="Reframed" />
            <Stat value={stats.corrected} label="Corrected" />
          </div>
          {(stats.awaiting > 0 || stats.removed > 0) && (
            <p className="t-sub mt-6 text-center">
              {stats.removed > 0 && <><span style={{ color: INK }}>{stats.removed}</span> removed outright · </>}
              <span style={{ color: INK }}>{stats.awaiting}</span> reframed only because a primary source is
              paywalled — restorable verbatim once the paper is supplied.
            </p>
          )}
        </section>

        {/* Methodology: on the page under the rule */}
        <section className="mb-7" style={{ breakInside: 'avoid' }}>
          <h2 className="t-row mb-2.5" style={{ color: INK }}>
            How this log was produced
          </h2>
          <p className="t-sub">
            Every claim in these modules is held to one rule: we only state or advise something that a real, locatable
            source genuinely supports — peer-reviewed literature for the learning-science content, and official State
            Examinations Commission / CAO documents for the exam content. Any claim that could not be verified was
            reframed to non-prescriptive language or removed outright. <strong style={{ color: INK }}>A citation was
            never invented to keep a claim.</strong> Every such change is recorded below.
          </p>
          {/* Legend */}
          <div className="mt-4 flex flex-col gap-2">
            {[
              { a: 'reframed' as CutAction, d: 'softened to what the evidence supports' },
              { a: 'corrected' as CutAction, d: 'a factual error fixed against an authoritative source' },
              { a: 'removed' as CutAction, d: 'cut with no replacement' },
            ].map(({ a, d }) => (
              <div key={a} className="flex items-baseline gap-2">
                <ActionPill action={a} />
                <span className="t-meta">{d}</span>
              </div>
            ))}
          </div>
        </section>

        {/* Filter: the shared menu (a choice applies at once); its options are today's chips */}
        {CUT_CONTENT.length > 0 && (
          <div className="mb-6 print:hidden">
            <Menu<FilterKey>
              label="Changes shown"
              options={chips.map(chip => ({ value: chip.key, label: `${chip.label} · ${chip.count}` }))}
              value={filter}
              onChange={setFilter}
            />
          </div>
        )}

        {/* Entries grouped by module */}
        {CUT_CONTENT.length === 0 ? (
          <div className="py-10 text-center">
            <p className="t-row" style={{ color: INK }}>Nothing cut yet</p>
            <p className="t-meta mt-1">
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
                    <h3 className="t-row" style={{ color: INK }}>
                      {group.module}
                    </h3>
                    <span className="t-meta shrink-0">
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
        <div className="t-meta hidden print:block mt-8 pt-4" style={{ borderTop: `1px solid ${HAIRLINE}` }}>
          Nextstepuni — Content Verification Log · Pre-accreditation review (DCU / Brian MacCraith)
        </div>
      </div>
    </div>
  );
};

export default CutContentPage;
