/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Accreditation — the evidence library behind the Learning Lab.
 *
 * A master–detail explorer: every module, what it is, why it helps, and the
 * verified sources behind it. Copy lives in data/accreditationCatalog.ts
 * (dossier-grounded, fact-checked); references are the same ordered lists the
 * in-module <Cite/> markers number against, so this page can never drift from
 * what students see inside a module.
 */

import React, { useEffect, useMemo, useRef, useState } from 'react';
import { motion } from 'framer-motion';
import { ArrowLeft, ArrowRight, BookOpen, Check, ChevronRight, Search, ShieldCheck } from 'lucide-react';
import { ACCREDITED_MODULES, type AccreditedModuleEntry } from '../data/accreditationCatalog';
import { type Reference } from '../data/references/types';
import { ALL_COURSES, categoryTitles } from '../courseData';
import { type CategoryType } from './KnowledgeTree';

interface AccreditationPageProps {
  onBack: () => void;
}

const SERIF = "'Source Serif 4', serif";
const SANS = "'DM Sans', sans-serif";

const INK = '#1a1a1a';
const HAIRLINE = '#EDEBE8';
const PAGE = '#f0f0f0';
const BODY = '#5a5550';
const MUTED = '#7a7068';
const LABEL = '#9e9186';
const FAINT = '#b0a898';
const ACCENT = '#F26B1F';
const ACCENT_TINT = '#FDEEDF';
const ACCENT_DARK_TEXT = '#8C3A0E';
const SUCCESS = '#3A8D5F';
const SUCCESS_TINT = '#E8F2EC';
const SUCCESS_DARK_TEXT = '#1F5F3E';

const CATEGORY_ORDER: CategoryType[] = [
  'architecture-mindset',
  'science-growth',
  'learning-cheat-codes',
  'exam-zone',
  'subject-specific-science',
];

const MicroLabel: React.FC<{ children: React.ReactNode; color?: string; className?: string }> = ({
  children,
  color = LABEL,
  className = '',
}) => (
  <p className={`text-[10px] font-bold uppercase tracking-[0.14em] ${className}`} style={{ color, fontFamily: SANS }}>
    {children}
  </p>
);

/** One reference row inside the detail pane — numbered to match the module's inline markers. */
const RefRow: React.FC<{ r: Reference; n: number }> = ({ r, n }) => {
  const official = r.kind === 'official';
  const link = r.doi
    ? { href: `https://doi.org/${r.doi}`, label: `doi:${r.doi}` }
    : r.url
    ? { href: r.url, label: r.url.replace(/^https?:\/\/(www\.)?/, '').replace(/\/$/, '') }
    : null;
  return (
    <div className="flex gap-3 py-3.5" style={{ borderTop: `1px solid ${HAIRLINE}` }}>
      <span
        className="shrink-0 w-6 h-6 rounded-full flex items-center justify-center text-[11px] font-bold mt-0.5"
        style={{ backgroundColor: ACCENT_TINT, color: ACCENT_DARK_TEXT, fontFamily: SANS }}
      >
        {n}
      </span>
      <div className="min-w-0">
        <p className="text-[13.5px] leading-relaxed" style={{ color: BODY, fontFamily: SANS }}>
          {r.authors} ({r.year}). {r.title}. <span className="italic">{r.source}</span>.
        </p>
        <div className="flex flex-wrap items-center gap-x-2.5 gap-y-1 mt-1.5">
          <span
            className="inline-flex items-center px-2 py-0.5 rounded-full text-[9.5px] font-bold uppercase tracking-[0.08em]"
            style={
              official
                ? { backgroundColor: ACCENT_TINT, color: ACCENT_DARK_TEXT }
                : { backgroundColor: SUCCESS_TINT, color: SUCCESS_DARK_TEXT }
            }
          >
            {official ? 'Official source' : 'Peer-reviewed'}
          </span>
          {link && (
            <a
              href={link.href}
              target="_blank"
              rel="noopener noreferrer"
              className="text-[11.5px] underline decoration-dotted underline-offset-2 break-all transition-colors hover:text-[#F26B1F]"
              style={{ color: MUTED, fontFamily: SANS }}
            >
              {link.label}
            </a>
          )}
        </div>
      </div>
    </div>
  );
};

const AccreditationPage: React.FC<AccreditationPageProps> = ({ onBack }) => {
  const entryById = useMemo(() => {
    const m = new Map<string, AccreditedModuleEntry>();
    ACCREDITED_MODULES.forEach(e => m.set(e.id, e));
    return m;
  }, []);

  // Category-ordered index: accredited modules rich, remaining courses shown
  // honestly as "in review" — never a dead link, never a fake reference list.
  const groups = useMemo(
    () =>
      CATEGORY_ORDER.map(cat => {
        const courses = ALL_COURSES.filter(c => c.category === cat);
        return {
          cat,
          accredited: courses.filter(c => entryById.has(c.id)),
          inReview: courses.filter(c => !entryById.has(c.id)),
        };
      }).filter(g => g.accredited.length + g.inReview.length > 0),
    [entryById]
  );

  // Flat navigation order across every accredited module (for prev/next + arrows).
  const navOrder = useMemo(
    () => groups.flatMap(g => g.accredited.map(c => c.id)),
    [groups]
  );

  const sourceCount = useMemo(() => {
    const ids = new Set<string>();
    ACCREDITED_MODULES.forEach(e => e.references.forEach(r => ids.add(r.id)));
    return ids.size;
  }, []);

  const [selectedId, setSelectedId] = useState<string>(navOrder[0]);
  const [query, setQuery] = useState('');
  // Mobile drill-in: list → detail.
  const [mobileDetail, setMobileDetail] = useState(false);
  const detailRef = useRef<HTMLDivElement>(null);
  const activeItemRef = useRef<HTMLButtonElement>(null);

  // Keep the active index row visible when navigating via prev/next or arrows.
  useEffect(() => {
    activeItemRef.current?.scrollIntoView({ block: 'nearest' });
  }, [selectedId]);

  const selected = entryById.get(selectedId);
  const selectedCourse = useMemo(() => ALL_COURSES.find(c => c.id === selectedId), [selectedId]);
  const navIndex = navOrder.indexOf(selectedId);

  const goTo = (id: string) => {
    setSelectedId(id);
    setMobileDetail(true);
    detailRef.current?.scrollTo({ top: 0 });
  };
  const step = (dir: 1 | -1) => {
    const next = navOrder[navIndex + dir];
    if (next) goTo(next);
  };

  // ←/→ move through modules (desktop affordance; ignored while typing).
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if ((e.target as HTMLElement)?.tagName === 'INPUT') return;
      if (e.key === 'ArrowRight') step(1);
      if (e.key === 'ArrowLeft') step(-1);
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  });

  const q = query.trim().toLowerCase();
  const matches = (title: string) => !q || title.toLowerCase().includes(q);

  return (
    <div className="min-h-screen" style={{ backgroundColor: PAGE }}>
      {/* ── Masthead ── */}
      <header
        className="sticky top-0 z-30 px-4 md:px-10 bg-[#f0f0f0]/92 backdrop-blur-sm border-b"
        style={{ borderColor: HAIRLINE, paddingTop: 'calc(14px + var(--sat, 0px))', paddingBottom: '14px' }}
      >
        <div className="max-w-6xl mx-auto flex items-center gap-4">
          <button
            onClick={() => (mobileDetail ? setMobileDetail(false) : onBack())}
            className="p-2.5 rounded-xl transition-colors hover:bg-white shrink-0 md:hidden"
            style={{ border: '1px solid rgba(0,0,0,0.08)', backgroundColor: 'white' }}
            aria-label="Back"
          >
            <ArrowLeft size={18} style={{ color: INK }} />
          </button>
          <button
            onClick={onBack}
            className="p-2.5 rounded-xl transition-colors hover:bg-white shrink-0 hidden md:block"
            style={{ border: '1px solid rgba(0,0,0,0.08)', backgroundColor: 'white' }}
            aria-label="Back"
          >
            <ArrowLeft size={18} style={{ color: INK }} />
          </button>
          <div className="min-w-0">
            <h1 className="text-lg md:text-xl font-semibold leading-tight" style={{ fontFamily: SERIF, color: INK }}>
              References
            </h1>
            <p className="text-[12px] leading-tight mt-0.5 hidden sm:block" style={{ color: MUTED, fontFamily: SANS }}>
              Every module, the evidence behind it, and why it earns its place.
            </p>
          </div>
        </div>
      </header>

      <div className="max-w-6xl mx-auto md:px-10 md:py-8 md:grid md:grid-cols-[300px_1fr] md:gap-8 md:items-start">
        {/* ── Index (left pane / mobile list) ── */}
        <aside
          className={`${mobileDetail ? 'hidden' : 'block'} md:block px-4 py-5 md:p-0 md:sticky md:top-[86px] md:max-h-[calc(100vh-110px)] md:overflow-y-auto md:pr-1`}
        >
          <p className="text-[14px] leading-relaxed mb-4 md:hidden" style={{ color: BODY, fontFamily: SANS }}>
            Every module, the evidence behind it, and why it earns its place. Nothing here states what its sources
            can't support.
          </p>
          {/* Stat strip — lives in the index column so it never fights the app's floating HUD. */}
          <div className="rounded-2xl bg-white px-4 py-3.5 mb-4 flex items-center gap-5" style={{ border: `1px solid ${HAIRLINE}` }}>
            {[
              { v: String(ACCREDITED_MODULES.length), l: 'Modules' },
              { v: String(sourceCount), l: 'Sources' },
            ].map(s => (
              <div key={s.l}>
                <p className="text-[22px] font-semibold leading-none" style={{ fontFamily: SERIF, color: INK }}>{s.v}</p>
                <MicroLabel className="mt-1">{s.l}</MicroLabel>
              </div>
            ))}
            <div className="ml-auto flex items-center gap-1.5">
              <ShieldCheck size={15} style={{ color: SUCCESS }} />
              <p className="text-[11px] font-semibold leading-tight" style={{ color: SUCCESS_DARK_TEXT, fontFamily: SANS }}>
                Every source<br />checkable
              </p>
            </div>
          </div>
          <div
            className="flex items-center gap-2 px-3 py-2.5 rounded-xl mb-5 bg-white"
            style={{ border: `1px solid ${HAIRLINE}` }}
          >
            <Search size={15} style={{ color: FAINT }} />
            <input
              value={query}
              onChange={e => setQuery(e.target.value)}
              placeholder="Find a module"
              className="w-full bg-transparent outline-none text-[13.5px]"
              style={{ color: INK, fontFamily: SANS }}
            />
          </div>

          {groups.map(g => {
            const acc = g.accredited.filter(c => matches(c.title));
            const rev = g.inReview.filter(c => matches(c.title));
            if (acc.length + rev.length === 0) return null;
            return (
              <div key={g.cat} className="mb-6">
                <MicroLabel className="mb-2 px-1">{categoryTitles[g.cat]}</MicroLabel>
                <div className="rounded-2xl overflow-hidden bg-white" style={{ border: `1px solid ${HAIRLINE}` }}>
                  {acc.map((c, i) => {
                    const active = c.id === selectedId;
                    return (
                      <button
                        key={c.id}
                        ref={active ? activeItemRef : undefined}
                        onClick={() => goTo(c.id)}
                        className="w-full flex items-center gap-2.5 px-4 py-3 text-left transition-colors"
                        style={{
                          borderTop: i === 0 ? 'none' : `1px solid ${HAIRLINE}`,
                          backgroundColor: active ? ACCENT_TINT : 'white',
                        }}
                      >
                        <span className="min-w-0 flex-1">
                          <span
                            className="block text-[13.5px] font-semibold leading-snug truncate"
                            style={{ fontFamily: SERIF, color: active ? ACCENT_DARK_TEXT : INK }}
                          >
                            {c.title}
                          </span>
                          <span className="block text-[11px] mt-0.5" style={{ color: active ? ACCENT_DARK_TEXT : LABEL, fontFamily: SANS }}>
                            {entryById.get(c.id)?.references.length} sources
                          </span>
                        </span>
                        <ChevronRight size={15} className="shrink-0" style={{ color: active ? ACCENT : FAINT }} />
                      </button>
                    );
                  })}
                  {rev.map((c, i) => (
                    <div
                      key={c.id}
                      className="w-full flex items-center gap-2.5 px-4 py-3"
                      style={{ borderTop: acc.length + i === 0 ? 'none' : `1px solid ${HAIRLINE}` }}
                    >
                      <span className="min-w-0 flex-1">
                        <span className="block text-[13.5px] leading-snug truncate" style={{ fontFamily: SERIF, color: FAINT }}>
                          {c.title}
                        </span>
                        <span className="block text-[11px] mt-0.5" style={{ color: FAINT, fontFamily: SANS }}>
                          Evidence review in progress
                        </span>
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </aside>

        {/* ── Detail (right pane / mobile drill-in) ── */}
        <main ref={detailRef} className={`${mobileDetail ? 'block' : 'hidden'} md:block px-4 pb-10 md:p-0`}>
          {selected && selectedCourse && (
              <motion.div
                key={selected.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.22, ease: 'easeOut' }}
              >
                <div className="rounded-2xl bg-white px-5 md:px-8 py-6 md:py-8" style={{ border: `1px solid ${HAIRLINE}` }}>
                  <MicroLabel color={ACCENT}>{categoryTitles[selectedCourse.category as CategoryType]}</MicroLabel>
                  <h2 className="text-[24px] md:text-[28px] font-semibold leading-tight mt-1.5" style={{ fontFamily: SERIF, color: INK }}>
                    {selectedCourse.title}
                  </h2>
                  <p className="text-[13.5px] mt-1" style={{ color: MUTED, fontFamily: SANS }}>
                    {selectedCourse.subtitle}
                  </p>

                  <div className="grid md:grid-cols-2 gap-5 md:gap-8 mt-6">
                    <div>
                      <MicroLabel className="mb-2">What it is</MicroLabel>
                      <p className="text-[14.5px] leading-relaxed" style={{ color: BODY, fontFamily: SANS }}>
                        {selected.what}
                      </p>
                    </div>
                    <div>
                      <MicroLabel color={SUCCESS_DARK_TEXT} className="mb-2">Why it helps</MicroLabel>
                      <p className="text-[14.5px] leading-relaxed" style={{ color: BODY, fontFamily: SANS }}>
                        {selected.why}
                      </p>
                    </div>
                  </div>
                </div>

                <div className="rounded-2xl bg-white px-5 md:px-8 py-5 md:py-6 mt-4" style={{ border: `1px solid ${HAIRLINE}` }}>
                  <div className="flex items-center gap-2.5 mb-1">
                    <div className="w-8 h-8 rounded-lg flex items-center justify-center" style={{ backgroundColor: ACCENT_TINT }}>
                      <BookOpen size={15} style={{ color: ACCENT }} />
                    </div>
                    <div>
                      <p className="text-[14px] font-semibold leading-tight" style={{ fontFamily: SERIF, color: INK }}>
                        References
                      </p>
                      <p className="text-[11px]" style={{ color: LABEL, fontFamily: SANS }}>
                        Numbered exactly as the citations inside the module
                      </p>
                    </div>
                    <span
                      className="ml-auto inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[10.5px] font-bold"
                      style={{ backgroundColor: SUCCESS_TINT, color: SUCCESS_DARK_TEXT, fontFamily: SANS }}
                    >
                      <Check size={11} strokeWidth={3} /> {selected.references.length} verified
                    </span>
                  </div>
                  <div className="mt-3">
                    {selected.references.map((r, i) => (
                      <RefRow key={r.id} r={r} n={i + 1} />
                    ))}
                  </div>
                </div>

                {/* Prev / next */}
                <div className="flex items-stretch gap-3 mt-4">
                  {([-1, 1] as const).map(dir => {
                    const target = navOrder[navIndex + dir];
                    const course = target ? ALL_COURSES.find(c => c.id === target) : undefined;
                    return (
                      <button
                        key={dir}
                        disabled={!target}
                        onClick={() => step(dir)}
                        className={`flex-1 rounded-2xl bg-white px-4 py-3.5 transition-colors ${target ? 'hover:bg-[#FDEEDF]' : 'opacity-40 cursor-default'} ${dir === 1 ? 'text-right' : 'text-left'}`}
                        style={{ border: `1px solid ${HAIRLINE}` }}
                      >
                        <span className={`flex items-center gap-2 ${dir === 1 ? 'justify-end' : ''}`}>
                          {dir === -1 && <ArrowLeft size={14} style={{ color: MUTED }} />}
                          <span className="min-w-0">
                            <MicroLabel>{dir === -1 ? 'Previous' : 'Next'}</MicroLabel>
                            <span className="block text-[13px] font-semibold truncate mt-0.5" style={{ fontFamily: SERIF, color: INK }}>
                              {course?.title ?? '—'}
                            </span>
                          </span>
                          {dir === 1 && <ArrowRight size={14} style={{ color: MUTED }} />}
                        </span>
                      </button>
                    );
                  })}
                </div>

                <p className="text-[11.5px] mt-5 px-1" style={{ color: LABEL, fontFamily: SANS }}>
                  Peer-reviewed entries link to their DOI record; official entries link to the issuing body. The full
                  change-by-change audit trail lives on the Cut Content page.
                </p>
              </motion.div>
          )}
        </main>
      </div>
    </div>
  );
};

export default AccreditationPage;
