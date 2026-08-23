/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Accreditation — the evidence library behind the Learning Lab.
 *
 * A master–detail explorer: every module, what it is, why it helps, and the
 * verified sources behind it. Copy lives in data/accreditationCatalog.ts;
 * references preserve the same order as each module's inline citations.
 */

import React, { useEffect, useMemo, useRef, useState } from 'react';
import { motion } from 'framer-motion';
import {
  ArrowLeft,
  ArrowRight,
  ArrowUpRight,
  BookOpen,
  Check,
  ChevronRight,
  Search,
  ShieldCheck,
} from 'lucide-react';
import { ACCREDITED_MODULES, type AccreditedModuleEntry } from '../data/accreditationCatalog';
import { type Reference } from '../data/references/types';
import { ALL_COURSES, categoryTitles } from '../courseData';
import { type CategoryType } from './KnowledgeTree';
import PageHeader from './ui/PageHeader';

interface AccreditationPageProps {
  onBack: () => void;
  /** Jump straight into the module being inspected. */
  onOpenModule?: (moduleId: string) => void;
}

type CategoryFilter = CategoryType | 'all';

const CATEGORY_ORDER: CategoryType[] = [
  'architecture-mindset',
  'science-growth',
  'learning-cheat-codes',
  'exam-zone',
  'subject-specific-science',
];

const CATEGORY_TAB_LABELS: Partial<Record<CategoryType, string>> = {
  'architecture-mindset': 'Mindset',
  'science-growth': 'Growth',
  'learning-cheat-codes': 'Learning',
  'exam-zone': 'Exam',
  'subject-specific-science': 'Subjects',
};

const MicroLabel: React.FC<{
  children: React.ReactNode;
  tone?: 'default' | 'accent' | 'success';
  className?: string;
}> = ({ children, tone = 'default', className = '' }) => {
  const toneClass = tone === 'accent'
    ? 'text-[var(--accent-text)]'
    : tone === 'success'
      ? 'text-[var(--success-tint-ink)]'
      : 'text-[var(--ink-muted)]';

  return (
    <p className={`text-[10px] font-bold uppercase tracking-[0.18em] ${toneClass} ${className}`}>
      {children}
    </p>
  );
};

const StatCell: React.FC<{
  eyebrow: string;
  value: string;
  meta: string;
  accent?: boolean;
}> = ({ eyebrow, value, meta, accent = false }) => (
  <div className="min-w-0">
    <MicroLabel>{eyebrow}</MicroLabel>
    <p className={`mt-2 font-serif text-[30px] font-semibold leading-none tracking-[-0.025em] ${accent ? 'text-[var(--accent-text)]' : 'text-[var(--ink-primary)]'}`}>
      {value}
    </p>
    <p className="mt-2 text-xs leading-relaxed text-[var(--ink-muted)]">{meta}</p>
  </div>
);

/** One reference row inside the detail pane — numbered to match inline markers. */
const RefRow: React.FC<{ reference: Reference; number: number }> = ({ reference, number }) => {
  const official = reference.kind === 'official';
  const href = reference.doi ? `https://doi.org/${reference.doi}` : reference.url;

  return (
    <div className="grid grid-cols-[32px_minmax(0,1fr)] gap-3 border-t border-[var(--outline-soft)] py-5 first:border-t-0">
      <span className="flex h-8 w-8 items-center justify-center rounded-full border border-[var(--outline-soft)] bg-[var(--surface-soft)] text-xs font-bold tabular-nums text-[var(--ink-secondary)]">
        {number}
      </span>
      <div className="min-w-0">
        <p className="text-sm leading-relaxed text-[var(--ink-secondary)]">
          {reference.authors} ({reference.year}). {reference.title}. <span className="italic">{reference.source}</span>.
        </p>
        <div className="mt-2 flex flex-wrap items-center gap-2.5">
          <span className="inline-flex items-center gap-1 rounded-full bg-[var(--success-tint)] px-2.5 py-1 text-[9px] font-bold uppercase tracking-[0.1em] text-[var(--success-tint-ink)]">
            <Check size={10} strokeWidth={3} aria-hidden="true" />
            {official ? 'Official source' : 'Peer-reviewed'}
          </span>
          {href && (
            <a
              href={href}
              target="_blank"
              rel="noopener noreferrer"
              aria-label={`Open ${official ? 'official source' : 'DOI record'} for ${reference.title}`}
              className="inline-flex items-center gap-1 text-xs font-semibold text-[var(--accent-text)] underline decoration-dotted underline-offset-4 transition-colors hover:text-[var(--ink-primary)]"
            >
              {official ? 'Source record' : 'DOI record'} <ArrowUpRight size={12} aria-hidden="true" />
            </a>
          )}
        </div>
      </div>
    </div>
  );
};

const AccreditationPage: React.FC<AccreditationPageProps> = ({ onBack, onOpenModule }) => {
  const entryById = useMemo(() => {
    const entries = new Map<string, AccreditedModuleEntry>();
    ACCREDITED_MODULES.forEach(entry => entries.set(entry.id, entry));
    return entries;
  }, []);

  // Category-ordered index: accredited modules are rich; remaining courses are
  // shown honestly as in review. The subject collection stays withheld until
  // every subject module has passed its evidence review.
  const groups = useMemo(
    () => CATEGORY_ORDER.map(category => {
      const courses = ALL_COURSES.filter(course => course.category === category);
      return {
        category,
        accredited: courses.filter(course => entryById.has(course.id)),
        inReview: courses.filter(course => !entryById.has(course.id)),
      };
    })
      .filter(group => group.accredited.length + group.inReview.length > 0)
      .filter(group => !(group.category === 'subject-specific-science' && group.inReview.length > 0)),
    [entryById],
  );

  const navOrder = useMemo(
    () => groups.flatMap(group => group.accredited.map(course => course.id)),
    [groups],
  );

  const sourceStats = useMemo(() => {
    const uniqueSources = new Map<string, Reference>();
    const visibleModuleIds = new Set(navOrder);
    ACCREDITED_MODULES.filter(entry => visibleModuleIds.has(entry.id)).forEach(entry => {
      entry.references.forEach(reference => uniqueSources.set(reference.id, reference));
    });
    const sources = [...uniqueSources.values()];
    return {
      total: sources.length,
      peerReviewed: sources.filter(reference => reference.kind !== 'official').length,
      official: sources.filter(reference => reference.kind === 'official').length,
    };
  }, [navOrder]);

  const [selectedId, setSelectedId] = useState<string>(navOrder[0]);
  const [activeCategory, setActiveCategory] = useState<CategoryFilter>('all');
  const [query, setQuery] = useState('');
  const [mobileDetail, setMobileDetail] = useState(false);
  const detailRef = useRef<HTMLDivElement>(null);
  const activeItemRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    activeItemRef.current?.scrollIntoView?.({ block: 'nearest' });
  }, [selectedId]);

  const selected = entryById.get(selectedId);
  const selectedCourse = useMemo(() => ALL_COURSES.find(course => course.id === selectedId), [selectedId]);
  const navIndex = navOrder.indexOf(selectedId);

  const goTo = (id: string) => {
    setSelectedId(id);
    setMobileDetail(true);
    detailRef.current?.scrollTo?.({ top: 0 });
  };

  const step = (direction: 1 | -1) => {
    const next = navOrder[navIndex + direction];
    if (!next) return;
    const nextCategory = ALL_COURSES.find(course => course.id === next)?.category as CategoryType | undefined;
    setQuery('');
    setActiveCategory(current => current === 'all' || !nextCategory ? current : nextCategory);
    goTo(next);
  };

  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      const target = event.target as HTMLElement | null;
      if (target?.closest('input, textarea, select, button, a, [contenteditable="true"]')) return;
      if (event.key === 'ArrowRight') step(1);
      if (event.key === 'ArrowLeft') step(-1);
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  });

  const normalizedQuery = query.trim().toLowerCase();
  const visibleGroups = useMemo(
    () => groups
      .filter(group => activeCategory === 'all' || group.category === activeCategory)
      .map(group => ({
        ...group,
        accredited: group.accredited.filter(course => !normalizedQuery || course.title.toLowerCase().includes(normalizedQuery)),
        inReview: group.inReview.filter(course => !normalizedQuery || course.title.toLowerCase().includes(normalizedQuery)),
      }))
      .filter(group => group.accredited.length + group.inReview.length > 0),
    [activeCategory, groups, normalizedQuery],
  );

  const visibleModuleCount = visibleGroups.reduce(
    (total, group) => total + group.accredited.length + group.inReview.length,
    0,
  );

  const visibleAccreditedIds = useMemo(
    () => visibleGroups.flatMap(group => group.accredited.map(course => course.id)),
    [visibleGroups],
  );
  const hasVisibleSelectedEvidence = visibleAccreditedIds.includes(selectedId);

  // Keep the master and detail panes truthful to each other. A search that
  // removes the active module should select the first matching result instead
  // of leaving stale evidence visible beside the filtered list.
  useEffect(() => {
    if (visibleAccreditedIds.length > 0 && !visibleAccreditedIds.includes(selectedId)) {
      setSelectedId(visibleAccreditedIds[0]);
      detailRef.current?.scrollTo?.({ top: 0 });
    }
  }, [visibleAccreditedIds, selectedId]);

  const categoryTabs: Array<{ id: CategoryFilter; label: string }> = [
    { id: 'all', label: 'All modules' },
    ...groups.map(group => ({
      id: group.category,
      label: CATEGORY_TAB_LABELS[group.category] ?? categoryTitles[group.category],
    })),
  ];

  const chooseCategory = (category: CategoryFilter) => {
    setActiveCategory(category);
    setQuery('');
    setMobileDetail(false);
    const nextId = category === 'all'
      ? navOrder[0]
      : groups.find(group => group.category === category)?.accredited[0]?.id;
    if (nextId) setSelectedId(nextId);
  };

  const handleCategoryKeyDown = (event: React.KeyboardEvent<HTMLButtonElement>, index: number) => {
    let nextIndex: number | undefined;
    if (event.key === 'ArrowRight') nextIndex = (index + 1) % categoryTabs.length;
    if (event.key === 'ArrowLeft') nextIndex = (index - 1 + categoryTabs.length) % categoryTabs.length;
    if (event.key === 'Home') nextIndex = 0;
    if (event.key === 'End') nextIndex = categoryTabs.length - 1;
    if (nextIndex === undefined) return;

    event.preventDefault();
    const nextCategory = categoryTabs[nextIndex].id;
    chooseCategory(nextCategory);
    document.getElementById(`evidence-tab-${nextCategory}`)?.focus();
  };

  const handlePageBack = () => {
    if (mobileDetail && window.innerWidth < 768) {
      setMobileDetail(false);
      return;
    }
    onBack();
  };

  return (
    <div className="product-shell theme-compat min-h-screen bg-[var(--surface-canvas)] text-[var(--ink-primary)] transition-colors duration-300">
      <div
        className="sticky inset-x-0 top-0 z-40 border-b border-[var(--outline-soft)] bg-[color:var(--surface-canvas)]/95 px-4 pb-4 backdrop-blur-xl md:px-10"
        style={{ paddingTop: 'calc(16px + var(--sat, 0px))' }}
      >
        <div className="mx-auto max-w-7xl">
          <PageHeader onBack={handlePageBack} eyebrow="Evidence library" title="References" backLabel="Go back" compact />
        </div>
      </div>

      <main className="mx-auto max-w-7xl px-4 pb-[calc(120px+var(--sab,0px))] pt-7 sm:px-6 md:px-10 md:pt-10">
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
        >
          <div className={`${mobileDetail ? 'hidden md:block' : 'block'}`}>
            <div className="flex flex-col gap-8 border-b border-[var(--outline-strong)] pb-7 lg:flex-row lg:items-end lg:justify-between">
              <div className="max-w-3xl">
                <div className="flex items-center gap-3">
                  <MicroLabel tone="accent">Verified foundations</MicroLabel>
                  <span className="h-px w-8 bg-[var(--outline-soft)]" aria-hidden="true" />
                  <p className="text-xs text-[var(--ink-muted)]">Research and official guidance</p>
                </div>
                <h1 className="mt-4 max-w-3xl font-serif text-[clamp(38px,6vw,68px)] font-semibold leading-[0.96] tracking-[-0.045em] text-[var(--ink-primary)]">
                  The evidence behind{' '}<br />every module.
                </h1>
                <p className="mt-4 max-w-2xl text-sm leading-relaxed text-[var(--ink-secondary)] sm:text-[15px]">
                  Explore what each module is designed to teach, why it helps, and the source record supporting it.
                </p>
              </div>

              <div className="max-w-sm border-t border-[var(--outline-strong)] pt-4 lg:mb-1 lg:w-80">
                <div className="flex items-center gap-2">
                  <ShieldCheck size={16} className="text-[var(--success-tint-ink)]" aria-hidden="true" />
                  <MicroLabel tone="success">Evidence standard</MicroLabel>
                </div>
                <p className="mt-2 text-xs leading-relaxed text-[var(--ink-muted)]">
                  Citation numbers match the modules. Every listed source opens to its DOI record or issuing body.
                </p>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-x-5 gap-y-6 border-b border-[var(--outline-soft)] py-6 sm:grid-cols-4">
              <StatCell eyebrow="Modules" value={String(navOrder.length)} meta="with reviewed evidence" accent />
              <StatCell eyebrow="Unique sources" value={String(sourceStats.total)} meta="across the library" />
              <StatCell eyebrow="Peer-reviewed" value={String(sourceStats.peerReviewed)} meta="research records" />
              <StatCell eyebrow="Official" value={String(sourceStats.official)} meta="institutional sources" />
            </div>

            <div className="mt-6 overflow-x-auto border-b border-[var(--outline-soft)]" role="tablist" aria-label="Evidence collections">
              <div className="flex min-w-max gap-7">
                {categoryTabs.map((tab, index) => (
                  <button
                    key={tab.id}
                    id={`evidence-tab-${tab.id}`}
                    type="button"
                    role="tab"
                    aria-selected={activeCategory === tab.id}
                    aria-controls="evidence-browser-panel"
                    tabIndex={activeCategory === tab.id ? 0 : -1}
                    onClick={() => chooseCategory(tab.id)}
                    onKeyDown={event => handleCategoryKeyDown(event, index)}
                    className={`relative pb-3 text-xs font-semibold transition-colors ${activeCategory === tab.id ? 'text-[var(--ink-primary)]' : 'text-[var(--ink-muted)] hover:text-[var(--ink-secondary)]'}`}
                  >
                    {tab.label}
                    {activeCategory === tab.id && <span className="absolute inset-x-0 -bottom-px h-0.5 bg-[var(--accent-hex)]" />}
                  </button>
                ))}
              </div>
            </div>
          </div>

          <div
            id="evidence-browser-panel"
            role="tabpanel"
            aria-labelledby={`evidence-tab-${activeCategory}`}
            className="mt-5 grid grid-cols-1 gap-4 md:grid-cols-12 md:items-start"
          >
            <aside className={`${mobileDetail ? 'hidden' : 'block'} md:sticky md:top-[94px] md:col-span-4 md:block`}>
              <section className="overflow-hidden rounded-[18px] border border-[var(--outline-soft)] bg-[var(--surface-paper)]">
                <div className="border-b border-[var(--outline-soft)] px-5 py-5 sm:px-6">
                  <MicroLabel>Module index</MicroLabel>
                  <div className="mt-1 flex items-end justify-between gap-4">
                    <h2 className="font-serif text-2xl font-semibold tracking-[-0.02em]">Find a module</h2>
                    <p className="shrink-0 text-xs font-semibold tabular-nums text-[var(--ink-muted)]">
                      {visibleModuleCount} shown
                    </p>
                  </div>
                  <label className="relative mt-4 block">
                    <Search size={15} className="pointer-events-none absolute left-3 top-1/2 z-10 -translate-y-1/2 text-[var(--ink-muted)]" aria-hidden="true" />
                    <span className="sr-only">Search modules</span>
                    <input
                      value={query}
                      onChange={event => setQuery(event.target.value)}
                      placeholder="Search modules"
                      className="w-full pl-9 pr-3 text-sm"
                    />
                  </label>
                </div>

                <div className="max-h-[62vh] overflow-y-auto px-3 py-3 md:max-h-[calc(100vh-245px)]">
                  {visibleGroups.length === 0 && (
                    <div className="px-3 py-10 text-center">
                      <p className="font-serif text-xl font-semibold">No modules found</p>
                      <p className="mt-2 text-xs leading-relaxed text-[var(--ink-muted)]">Try a different title or evidence collection.</p>
                      <button
                        type="button"
                        onClick={() => setQuery('')}
                        className="mt-4 text-xs font-bold text-[var(--accent-text)] underline underline-offset-4"
                      >
                        Clear search
                      </button>
                    </div>
                  )}

                  {visibleGroups.map(group => (
                    <div key={group.category} className="mb-5 last:mb-0">
                      <MicroLabel className="px-2 pb-2 pt-1">{categoryTitles[group.category]}</MicroLabel>
                      <div>
                        {group.accredited.map(course => {
                          const active = course.id === selectedId;
                          return (
                            <button
                              key={course.id}
                              ref={active ? activeItemRef : undefined}
                              type="button"
                              aria-current={active ? 'true' : undefined}
                              aria-label={`${course.title}, ${entryById.get(course.id)?.references.length} verified sources`}
                              onClick={() => goTo(course.id)}
                              className={`group flex w-full items-center gap-3 rounded-xl px-3 py-3 text-left transition-colors ${active ? 'bg-[var(--surface-soft)]' : 'hover:bg-[var(--surface-canvas)]'}`}
                            >
                              <span className={`h-1.5 w-1.5 shrink-0 rounded-full ${active ? 'bg-[var(--accent-hex)]' : 'bg-[var(--outline-soft)]'}`} aria-hidden="true" />
                              <span className="min-w-0 flex-1">
                                <span className={`block truncate font-serif text-[15px] font-semibold leading-snug ${active ? 'text-[var(--ink-primary)]' : 'text-[var(--ink-secondary)]'}`}>
                                  {course.title}
                                </span>
                                <span className="mt-0.5 block text-[11px] text-[var(--ink-muted)]">
                                  {entryById.get(course.id)?.references.length} verified sources
                                </span>
                              </span>
                              <ChevronRight size={15} className={`shrink-0 ${active ? 'text-[var(--accent-text)]' : 'text-[var(--ink-muted)] group-hover:text-[var(--ink-primary)]'}`} aria-hidden="true" />
                            </button>
                          );
                        })}

                        {group.inReview.map(course => (
                          <div key={course.id} className="flex items-center gap-3 px-3 py-3">
                            <span className="h-1.5 w-1.5 shrink-0 rounded-full bg-[var(--outline-soft)]" aria-hidden="true" />
                            <span className="min-w-0 flex-1">
                              <span className="block truncate font-serif text-[15px] leading-snug text-[var(--ink-muted)]">{course.title}</span>
                              <span className="mt-0.5 block text-[11px] text-[var(--ink-muted)]">Evidence review underway</span>
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </section>
            </aside>

            <section ref={detailRef} aria-label="Module evidence" className={`${mobileDetail ? 'block' : 'hidden'} md:col-span-8 md:block`}>
              {selected && selectedCourse && hasVisibleSelectedEvidence && (
                <motion.div
                  key={selected.id}
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.22, ease: 'easeOut' }}
                >
                  <article className="overflow-hidden rounded-[18px] border border-[var(--outline-soft)] bg-[var(--surface-paper)]">
                    <div className="flex flex-col gap-5 border-b border-[var(--outline-soft)] px-5 py-6 sm:px-7 sm:py-7 lg:flex-row lg:items-start lg:justify-between">
                      <div className="min-w-0 max-w-2xl">
                        <MicroLabel tone="accent">{categoryTitles[selectedCourse.category as CategoryType]}</MicroLabel>
                        <h2 className="mt-2 font-serif text-[clamp(30px,4vw,44px)] font-semibold leading-[1.02] tracking-[-0.035em] text-[var(--ink-primary)]">
                          {selectedCourse.title}
                        </h2>
                        <p className="mt-2 text-sm text-[var(--ink-muted)]">{selectedCourse.subtitle}</p>
                      </div>
                      {onOpenModule && (
                        <button
                          type="button"
                          onClick={() => onOpenModule(selected.id)}
                          className="inline-flex min-h-11 shrink-0 items-center justify-center gap-2 rounded-xl border border-[var(--outline-strong)] bg-[var(--surface-paper)] px-4 text-xs font-bold text-[var(--ink-primary)] transition-transform hover:-translate-y-0.5"
                          aria-label={`Open the ${selectedCourse.title} module`}
                        >
                          Open module <ArrowUpRight size={14} aria-hidden="true" />
                        </button>
                      )}
                    </div>

                    <div className="grid sm:grid-cols-2">
                      <section className="px-5 py-6 sm:border-r sm:border-[var(--outline-soft)] sm:px-7">
                        <MicroLabel>What it is</MicroLabel>
                        <p className="mt-3 text-sm leading-7 text-[var(--ink-secondary)]">{selected.what}</p>
                      </section>
                      <section className="border-t border-[var(--outline-soft)] px-5 py-6 sm:border-t-0 sm:px-7">
                        <MicroLabel tone="success">Why it helps</MicroLabel>
                        <p className="mt-3 text-sm leading-7 text-[var(--ink-secondary)]">{selected.why}</p>
                      </section>
                    </div>
                  </article>

                  <section className="mt-4 overflow-hidden rounded-[18px] border border-[var(--outline-soft)] bg-[var(--surface-paper)]">
                    <div className="flex flex-wrap items-start justify-between gap-4 border-b border-[var(--outline-soft)] px-5 py-5 sm:px-7">
                      <div className="min-w-0">
                        <MicroLabel>Source record</MicroLabel>
                        <div className="mt-1 flex items-center gap-2.5">
                          <BookOpen size={17} className="text-[var(--accent-text)]" aria-hidden="true" />
                          <h2 className="font-serif text-2xl font-semibold tracking-[-0.02em]">References</h2>
                        </div>
                        <p className="mt-1 text-xs leading-relaxed text-[var(--ink-muted)]">
                          Numbered exactly as the citations inside this module.
                        </p>
                      </div>
                      <span className="inline-flex min-h-8 items-center gap-1.5 rounded-full bg-[var(--success-tint)] px-3 text-[10px] font-bold uppercase tracking-[0.1em] text-[var(--success-tint-ink)]">
                        <Check size={11} strokeWidth={3} aria-hidden="true" /> {selected.references.length} verified
                      </span>
                    </div>

                    <div className="px-5 sm:px-7">
                      {selected.references.map((reference, index) => (
                        <RefRow key={reference.id} reference={reference} number={index + 1} />
                      ))}
                    </div>

                    <p className="border-t border-[var(--outline-soft)] px-5 py-4 text-[11px] leading-relaxed text-[var(--ink-muted)] sm:px-7">
                      Peer-reviewed entries open to their DOI record; official entries open to the issuing body.
                    </p>
                  </section>

                  <nav className="mt-4 grid grid-cols-2 gap-3" aria-label="Browse accredited modules">
                    {([-1, 1] as const).map(direction => {
                      const target = navOrder[navIndex + direction];
                      const course = target ? ALL_COURSES.find(item => item.id === target) : undefined;
                      return (
                        <button
                          key={direction}
                          type="button"
                          disabled={!target}
                          onClick={() => step(direction)}
                          className={`rounded-[18px] border border-[var(--outline-soft)] bg-[var(--surface-paper)] px-4 py-4 transition-colors ${target ? 'hover:border-[var(--outline-strong)]' : 'cursor-default opacity-40'} ${direction === 1 ? 'text-right' : 'text-left'}`}
                        >
                          <span className={`flex items-center gap-2 ${direction === 1 ? 'justify-end' : ''}`}>
                            {direction === -1 && <ArrowLeft size={15} className="shrink-0 text-[var(--ink-muted)]" aria-hidden="true" />}
                            <span className="min-w-0">
                              <MicroLabel>{direction === -1 ? 'Previous' : 'Next'}</MicroLabel>
                              <span className="mt-1 block truncate font-serif text-sm font-semibold text-[var(--ink-primary)]">
                                {course?.title ?? '—'}
                              </span>
                            </span>
                            {direction === 1 && <ArrowRight size={15} className="shrink-0 text-[var(--ink-muted)]" aria-hidden="true" />}
                          </span>
                        </button>
                      );
                    })}
                  </nav>
                </motion.div>
              )}
              {!hasVisibleSelectedEvidence && (
                <div className="rounded-[18px] border border-[var(--outline-soft)] bg-[var(--surface-paper)] px-6 py-12 text-center sm:px-10">
                  <MicroLabel>Evidence status</MicroLabel>
                  <h2 className="mt-3 font-serif text-3xl font-semibold tracking-[-0.025em] text-[var(--ink-primary)]">
                    {visibleModuleCount > 0 ? 'Review underway' : 'No evidence record found'}
                  </h2>
                  <p className="mx-auto mt-3 max-w-md text-sm leading-7 text-[var(--ink-muted)]">
                    {visibleModuleCount > 0
                      ? 'The matching module is listed in the index, but its source record is still being reviewed.'
                      : 'Try a different module title or evidence collection.'}
                  </p>
                </div>
              )}
            </section>
          </div>
        </motion.div>
      </main>
    </div>
  );
};

export default AccreditationPage;
