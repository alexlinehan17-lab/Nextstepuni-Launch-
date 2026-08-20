/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * ModuleShowcase — module detail / picker for a single world.
 *
 * Layout: cream hero card on cream page background, with a horizontal
 * carousel of mini-cards below for the other modules in this world.
 * Clicking a carousel card promotes it to the hero position with a
 * Framer Motion `layoutId` morph (same pattern as ModulesView's
 * hero/satellite swap on the Library page).
 *
 * The hero is wrapped in <AnimatePresence mode="popLayout"> with a
 * `key` tied to the active module id, so when the module changes:
 *   - The exiting hero stays mounted long enough for Framer to morph
 *     it back to its carousel slot
 *   - The entering hero animates in concurrently (popLayout) rather
 *     than waiting for the exit to finish
 *
 * Active-in-carousel: the currently-active module is rendered in the
 * carousel as a muted, non-interactive card with NO layoutId, so it
 * doesn't conflict with the hero's layoutId of the same module id.
 * (Two simultaneously-mounted elements with the same layoutId breaks
 * Framer's tracking and produces hard cuts instead of morphs.)
 */
import React, { useState, useCallback, useEffect, useRef } from 'react';
import { motion, AnimatePresence, LayoutGroup } from 'framer-motion';
import { CheckCircle2, ChevronDown, ArrowRight, ChevronLeft, ChevronRight } from 'lucide-react';
import { Capacitor } from '@capacitor/core';
import { type CourseData } from './Library';
import { MODULE_SECTIONS, type SectionInfo } from '../moduleSections';
import { SUBJECT_MODULE_CONTENT } from '../subjectModuleData';
import { WorldIconBlob, type WorldId } from './WorldIconBlob';
import { WORLD_TONES, useWorldTones, type WorldTones } from './worldPalette';

// ── World theming ──────────────────────────────────────────────────────
interface WorldTheme extends WorldTones {
  worldKey: WorldId;
  number: string;
  worldName: string;
}

const WORLD_THEMES: Record<string, WorldTheme> = {
  'architecture-mindset': {
    worldKey: 'mind',   number: '01', worldName: 'The Architecture',
    ...WORLD_TONES['architecture-mindset'],
  },
  'science-growth': {
    worldKey: 'growth', number: '02', worldName: 'The Garden',
    ...WORLD_TONES['science-growth'],
  },
  'learning-cheat-codes': {
    worldKey: 'learn',  number: '03', worldName: 'The Cheat Codes',
    ...WORLD_TONES['learning-cheat-codes'],
  },
  'subject-specific-science': {
    worldKey: 'decode', number: '04', worldName: 'The Decoder',
    ...WORLD_TONES['subject-specific-science'],
  },
  'exam-zone': {
    worldKey: 'exam',   number: '05', worldName: 'The Arena',
    ...WORLD_TONES['exam-zone'],
  },
};

const FALLBACK_THEME: WorldTheme = WORLD_THEMES['architecture-mindset'];

const CARD_WIDTH = 280; // px — matches w-[280px] used on carousel cards
const IS_NATIVE_IOS = Capacitor.getPlatform() === 'ios';

// ── Section helpers ────────────────────────────────────────────────────
function getSectionsForModule(moduleId: string, sectionsCount: number): SectionInfo[] {
  if (MODULE_SECTIONS[moduleId]) return MODULE_SECTIONS[moduleId];
  const subjectMatch = moduleId.match(/^subject-(.+)-protocol$/);
  if (subjectMatch) {
    const subjectId = subjectMatch[1];
    const content = SUBJECT_MODULE_CONTENT[subjectId];
    if (content?.sections) {
      return content.sections.map((s: { title: string; eyebrow: string }) => ({
        title: s.title,
        eyebrow: s.eyebrow,
      }));
    }
  }
  return Array.from({ length: sectionsCount }, (_, i) => ({
    title: `Section ${i + 1}`,
    eyebrow: '',
  }));
}

// ── Component ──────────────────────────────────────────────────────────
interface ModuleShowcaseProps {
  courses: CourseData[];
  categoryTitle: string;
  categoryId: string;
  userProgress: Record<string, { unlockedSection: number }>;
  onSelectCourse: (courseId: string) => void;
}

export default function ModuleShowcase({
  courses,
  categoryId,
  userProgress,
  onSelectCourse,
}: ModuleShowcaseProps) {
  const rawTheme = WORLD_THEMES[categoryId] ?? FALLBACK_THEME;
  const tones = useWorldTones();
  // Same object, with the ink and mid resolved for the active theme.
  // Only `deep` is swapped wholesale: it is text everywhere it appears. `mid`
  // also fills buttons and bars, so it stays raw and the eyebrow asks for
  // midText at its own use site.
  const theme = { ...rawTheme, deep: tones.ink(rawTheme) };

  // Synchronous initialiser — hero mounts with the right module on the
  // first render, no useEffect tick.
  const [currentIndex, setCurrentIndex] = useState(() => {
    if (courses.length === 0) return 0;
    const firstIncomplete = courses.findIndex(c => {
      const p = userProgress[c.id];
      return !p || p.unlockedSection < c.sectionsCount;
    });
    return firstIncomplete === -1 ? 0 : firstIncomplete;
  });
  const [sectionsExpanded, setSectionsExpanded] = useState(false);

  // Defensive: if courses is empty or currentIndex out of bounds, bail
  // before destructuring to avoid the "blank hero" rendering bug.
  if (courses.length === 0) return null;
  const safeIndex = Math.min(Math.max(currentIndex, 0), courses.length - 1);
  const course = courses[safeIndex];

  const progress = userProgress[course.id];
  const isCompleted = !!progress && progress.unlockedSection >= course.sectionsCount;
  const isInProgress = !!progress && progress.unlockedSection > 0 && !isCompleted;

  const sections = getSectionsForModule(course.id, course.sectionsCount);
  const startStep = isInProgress
    ? Math.min((progress?.unlockedSection ?? 0) + 1, course.sectionsCount)
    : 1;
  const startSection = sections[startStep - 1];
  const startSectionTitle = startSection?.title ?? `Section ${startStep}`;
  // Section eyebrow strings tend to be in the form "Section 1 // Sub-headline".
  // Strip the prefix to get just the sub-headline part.
  const sectionSubhed = startSection?.eyebrow?.includes(' // ')
    ? startSection.eyebrow.split(' // ').slice(1).join(' // ')
    : '';

  const ctaLabel = isCompleted ? 'Review module' : isInProgress ? 'Continue module' : 'Begin module';

  const goTo = useCallback((idx: number) => {
    if (idx < 0 || idx >= courses.length || idx === safeIndex) return;
    setCurrentIndex(idx);
    setSectionsExpanded(false);
  }, [safeIndex, courses.length]);

  // Keyboard nav
  useEffect(() => {
    const handleKey = (e: KeyboardEvent) => {
      if (e.key === 'ArrowRight') goTo(safeIndex + 1);
      if (e.key === 'ArrowLeft') goTo(safeIndex - 1);
    };
    window.addEventListener('keydown', handleKey);
    return () => window.removeEventListener('keydown', handleKey);
  }, [goTo, safeIndex]);

  // ── Carousel scroll affordance ──────────────────────────────────────
  const scrollRef = useRef<HTMLDivElement>(null);
  const [canScrollLeft, setCanScrollLeft] = useState(false);
  const [canScrollRight, setCanScrollRight] = useState(false);

  useEffect(() => {
    const el = scrollRef.current;
    if (!el) return;
    const update = () => {
      setCanScrollLeft(el.scrollLeft > 8);
      setCanScrollRight(el.scrollLeft + el.clientWidth < el.scrollWidth - 8);
    };
    update();
    el.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
    return () => {
      el.removeEventListener('scroll', update);
      window.removeEventListener('resize', update);
    };
  }, [courses.length]);

  const scrollByCard = (dir: 1 | -1) => {
    scrollRef.current?.scrollBy({ left: dir * (CARD_WIDTH + 12), behavior: 'smooth' });
  };

  if (IS_NATIVE_IOS) {
    return (
      <div className="w-full max-w-xl px-1 theme-compat">
        <div className="mb-5">
          <div className="flex items-center gap-3">
            <div className="flex h-14 w-14 shrink-0 items-center justify-center overflow-hidden rounded-2xl" style={{ background: `${theme.blob}38` }}>
              <WorldIconBlob world={theme.worldKey} size={76} compact />
            </div>
            <div className="min-w-0">
              <p className="font-mono text-[10px] font-bold uppercase tracking-[0.2em]" style={{ color: tones.midText(rawTheme) }}>
                {theme.number} · {theme.worldName}
              </p>
              <h2 className="mt-1 font-serif text-[27px] font-medium leading-none tracking-tight text-[#1A1A1A] dark:text-white">
                Choose a module
              </h2>
            </div>
          </div>
          <p className="mt-3 text-[13px] leading-relaxed text-zinc-600 dark:text-zinc-300">
            Tap any module to open it. Your next section is saved automatically.
          </p>
        </div>

        <div className="space-y-3">
          {courses.map((item, index) => {
            const itemProgress = userProgress[item.id];
            const completedSections = Math.min(itemProgress?.unlockedSection ?? 0, item.sectionsCount);
            const itemCompleted = completedSections >= item.sectionsCount;
            const itemInProgress = completedSections > 0 && !itemCompleted;
            const percent = item.sectionsCount > 0
              ? Math.round((completedSections / item.sectionsCount) * 100)
              : 0;
            const status = itemCompleted
              ? 'Complete'
              : itemInProgress
                ? `Continue · ${percent}%`
                : `${item.sectionsCount} sections`;

            return (
              <button
                key={item.id}
                type="button"
                onClick={() => onSelectCourse(item.id)}
                className="group w-full rounded-[20px] border bg-white p-4 text-left shadow-[0_2px_10px_rgba(0,0,0,0.04)] transition-transform active:scale-[0.985] dark:bg-zinc-900"
                style={{ borderColor: itemInProgress || itemCompleted ? `${theme.mid}88` : `${theme.blob}77` }}
              >
                <div className="flex items-start gap-3">
                  <span
                    className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full font-mono text-[11px] font-bold"
                    style={{ background: itemCompleted ? theme.mid : `${theme.blob}45`, color: itemCompleted ? '#fff' : theme.deep }}
                  >
                    {itemCompleted ? <CheckCircle2 size={18} /> : String(index + 1).padStart(2, '0')}
                  </span>

                  <div className="min-w-0 flex-1">
                    <div className="flex items-start justify-between gap-3">
                      <h3 className="font-serif text-[20px] font-medium leading-[1.08] tracking-tight text-[#1A1A1A] dark:text-white">
                        {item.title}
                      </h3>
                      <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full" style={{ background: `${theme.blob}38`, color: theme.deep }}>
                        <ChevronRight size={17} />
                      </span>
                    </div>
                    <p className="mt-2 line-clamp-2 text-[12px] leading-relaxed text-zinc-600 dark:text-zinc-400">
                      {item.description}
                    </p>

                    <div className="mt-3 flex items-center gap-2.5">
                      <span className="h-1.5 flex-1 overflow-hidden rounded-full" style={{ background: `${theme.deep}1F` }}>
                        <span className="block h-full rounded-full" style={{ width: `${percent}%`, background: theme.mid }} />
                      </span>
                      <span className="shrink-0 font-mono text-[9px] font-bold uppercase tracking-[0.12em]" style={{ color: theme.deep }}>
                        {status}
                      </span>
                    </div>
                  </div>
                </div>
              </button>
            );
          })}
        </div>
      </div>
    );
  }

  return (
    <div className="w-full max-w-5xl mx-auto px-4 flex flex-col gap-5 md:gap-6 theme-compat">
      <LayoutGroup>
        {/* ── Hero card ───────────────────────────────────────────
            Wrapped in AnimatePresence with key=course.id so each
            module mount/unmount is tracked. mode="popLayout" lets
            the exiting hero animate concurrently with the entering
            one (otherwise the hero slot is blank during the gap). */}
        <div className="relative">
          <AnimatePresence mode="popLayout" initial={false}>
            <motion.div
              key={course.id}
              layoutId={`module-card-${course.id}`}
              layout
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ type: 'spring', stiffness: 240, damping: 32, opacity: { duration: 0.18 } }}
              className="rounded-[24px] md:rounded-[28px] overflow-hidden"
              style={{
                background: '#FFFFFF',
                border: `1px solid ${theme.blob}66`,
                boxShadow: '0 4px 18px rgba(0,0,0,0.05), 0 1px 4px rgba(0,0,0,0.04)',
              }}
            >
              <div className="p-6 md:p-9 lg:p-10">
                {/* ── Eyebrow row — full width, above both columns ── */}
                <div className="flex items-center gap-5 mb-6 md:mb-8">
                  <WorldIconBlob world={theme.worldKey} size={140} />
                  <div className="flex items-center gap-3 min-w-0">
                    <span className="font-mono text-[11px] font-bold tracking-[0.25em]" style={{ color: theme.deep }}>
                      {theme.number}
                    </span>
                    <span className="h-px w-8 shrink-0" style={{ background: `${theme.deep}40` }} />
                    <span className="font-mono text-[10px] uppercase tracking-[0.22em]" style={{ color: `${theme.deep}AA` }}>
                      {theme.worldName}
                    </span>
                  </div>
                </div>

                {/* ── Two-column body ────────────────────────────── */}
                <div className="grid grid-cols-1 md:grid-cols-12 gap-6 md:gap-10">
                  {/* Left column — what this is */}
                  <div className="md:col-span-7 flex flex-col">
                    <h1
                      className="font-serif font-medium tracking-[-0.03em] leading-[1.0] text-[#1A1A1A]"
                      style={{ fontSize: 'clamp(36px, 4.5vw, 56px)' }}
                    >
                      {course.title}
                    </h1>

                    {course.subtitle && (
                      <p className="font-serif italic text-[18px] md:text-[22px] mt-4" style={{ color: tones.midText(rawTheme) }}>
                        {course.subtitle}
                      </p>
                    )}

                    <p className="text-[14px] md:text-[15px] leading-relaxed mt-5" style={{ color: 'rgba(0,0,0,0.62)' }}>
                      {course.description}
                    </p>
                  </div>

                  {/* Right column — how to start */}
                  <div className="md:col-span-5 md:pl-8 md:border-l flex flex-col" style={{ borderColor: `${theme.mid}4D` }}>
                    <p className="font-mono text-[11px] font-medium uppercase tracking-[0.22em]" style={{ color: tones.midText(rawTheme) }}>
                      {isInProgress ? 'Continue here' : 'Start here'}
                    </p>

                    <h3 className="font-serif font-medium leading-snug tracking-tight text-[#1A1A1A] mt-3" style={{ fontSize: 'clamp(20px, 2vw, 24px)' }}>
                      {startSectionTitle}
                    </h3>

                    {sectionSubhed && (
                      <p className="font-serif italic text-[14px] mt-1.5" style={{ color: 'rgba(0,0,0,0.6)' }}>
                        {sectionSubhed}
                      </p>
                    )}

                    {/* Begins with panel — muted secondary chip */}
                    <div className="mt-5 px-3 py-2 rounded-lg" style={{ background: '#F1F0ED', border: '1px solid #d0cdc8' }}>
                      <p className="font-mono text-[10px] font-bold uppercase tracking-[0.22em]" style={{ color: `${theme.deep}AA` }}>
                        {isInProgress
                          ? `Up next · Section ${startStep} of ${course.sectionsCount}`
                          : `Begins with · Section 1 of ${course.sectionsCount}`}
                      </p>
                    </div>

                    {/* Buttons */}
                    <div className="mt-6 flex flex-col items-start gap-3">
                      <button
                        onClick={() => onSelectCourse(course.id)}
                        className="group inline-flex items-center gap-2.5 px-6 py-3.5 rounded-full text-white text-[14px] font-semibold transition-all duration-300 hover:gap-3.5"
                        style={{
                          background: theme.mid,
                          boxShadow: `0 6px 16px ${theme.mid}55`,
                        }}
                      >
                        {ctaLabel}
                        <ArrowRight size={16} />
                      </button>
                      <button
                        onClick={() => setSectionsExpanded(!sectionsExpanded)}
                        className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-[12px] font-semibold transition-colors duration-200"
                        style={{ color: tones.midText(rawTheme), border: `1px solid ${theme.mid}55` }}
                      >
                        What&rsquo;s in this module
                        <motion.span animate={{ rotate: sectionsExpanded ? 180 : 0 }} transition={{ duration: 0.2 }}>
                          <ChevronDown size={12} />
                        </motion.span>
                      </button>
                    </div>
                  </div>
                </div>

                {/* Expandable sections — full width below body */}
                <AnimatePresence>
                  {sectionsExpanded && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: 'auto', opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={{ duration: 0.3, ease: [0.25, 1, 0.5, 1] }}
                      className="overflow-hidden mt-6"
                    >
                      <div className="space-y-1">
                        {sections.map((section, i) => {
                          const sectionDone = !!progress && progress.unlockedSection > i;
                          return (
                            <div
                              key={i}
                              className="flex items-start gap-3 py-2"
                              style={{ borderTop: i === 0 ? 'none' : '1px solid rgba(0,0,0,0.04)' }}
                            >
                              <span
                                className="shrink-0 mt-0.5 flex items-center justify-center"
                                style={{
                                  width: 22, height: 22, borderRadius: '50%',
                                  backgroundColor: sectionDone ? theme.mid : '#e0dbd4',
                                  color: sectionDone ? '#fff' : '#9e9186',
                                  fontSize: 11, fontWeight: 700,
                                }}
                              >
                                {sectionDone ? <CheckCircle2 size={12} /> : i + 1}
                              </span>
                              <div>
                                <p className="text-sm font-medium text-[#1A1A1A]">{section.title}</p>
                                {section.eyebrow && (
                                  <p className="text-xs mt-0.5" style={{ color: '#9e9186' }}>
                                    {section.eyebrow.split(' // ')[1] || section.eyebrow}
                                  </p>
                                )}
                              </div>
                            </div>
                          );
                        })}
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>

                {/* ── Metadata footer — full width below both columns ── */}
                <div className="mt-7 pt-5 flex flex-wrap items-baseline gap-x-8 gap-y-3" style={{ borderTop: '1px solid rgba(0,0,0,0.06)' }}>
                  <div className="flex items-baseline gap-2">
                    <span className="font-mono text-[10px] font-bold uppercase tracking-[0.18em]" style={{ color: `${theme.deep}99` }}>Progress</span>
                    <span className="text-[13px] font-medium" style={{ color: isCompleted ? tones.midText(rawTheme) : 'var(--ink-primary)' }}>
                      {isCompleted ? 'Completed' : isInProgress ? `${progress?.unlockedSection} of ${course.sectionsCount} sections` : 'Not started'}
                    </span>
                  </div>
                  {course.tags.length > 0 && (
                    <div className="flex items-baseline gap-2 min-w-0">
                      <span className="font-mono text-[10px] font-bold uppercase tracking-[0.18em]" style={{ color: `${theme.deep}99` }}>Topics</span>
                      <span className="text-[13px] font-medium text-[#1A1A1A] truncate">{course.tags.slice(0, 3).join(', ')}</span>
                    </div>
                  )}
                </div>
              </div>
            </motion.div>
          </AnimatePresence>
        </div>

        {/* ── Carousel ─────────────────────────────────────────── */}
        {courses.length > 1 && (
          <div>
            <p className="font-mono text-[10px] font-bold uppercase tracking-[0.22em] mb-3" style={{ color: tones.midText(rawTheme) }}>
              More in {theme.worldName}
            </p>

            <div className="relative">
              {/* Scroll container — scrollbar hidden, arrow buttons drive nav */}
              <div
                ref={scrollRef}
                className="flex gap-3 overflow-x-auto pb-1 -mx-4 px-4 snap-x scroll-px-4 [&::-webkit-scrollbar]:hidden"
                style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
              >
                {courses.map((c, originalIdx) => {
                  const isActive = originalIdx === safeIndex;
                  const cProgress = userProgress[c.id];
                  const cCompleted = !!cProgress && cProgress.unlockedSection >= c.sectionsCount;
                  const cPct = cProgress ? Math.round((cProgress.unlockedSection / c.sectionsCount) * 100) : 0;
                  const cNumber = String(originalIdx + 1).padStart(2, '0');

                  // Active card: muted, non-interactive, NO layoutId — never
                  // share a layoutId with the hero or Framer drops the morph.
                  if (isActive) {
                    return (
                      <div
                        key={c.id}
                        aria-current="true"
                        className="shrink-0 w-[260px] md:w-[280px] rounded-2xl overflow-hidden snap-start cursor-default"
                        style={{
                          background: '#FFFFFF',
                          border: `1px dashed ${theme.mid}55`,
                          boxShadow: 'inset 0 1px 3px rgba(0,0,0,0.04)',
                          opacity: 0.5,
                        }}
                      >
                        <div className="flex flex-col h-full p-5 min-h-[220px]">
                          <div className="flex justify-center -mt-4 -mb-2">
                            <WorldIconBlob world={theme.worldKey} size={120} compact />
                          </div>
                          <span className="font-mono text-[11px] font-medium tracking-[0.2em]" style={{ color: tones.midText(rawTheme) }}>
                            {cNumber}
                          </span>
                          <h4 className="font-serif text-[20px] md:text-[22px] font-medium tracking-tight leading-[1.05] text-[#1A1A1A] mt-1">
                            {c.title}
                          </h4>
                          <p className="font-mono text-[10px] font-bold uppercase tracking-[0.18em] mt-auto pt-3" style={{ color: tones.midText(rawTheme) }}>
                            Currently viewing
                          </p>
                        </div>
                      </div>
                    );
                  }

                  return (
                    <motion.button
                      key={c.id}
                      layoutId={`module-card-${c.id}`}
                      layout
                      transition={{ type: 'spring', stiffness: 240, damping: 32 }}
                      onClick={() => goTo(originalIdx)}
                      whileHover={{ y: -2 }}
                      className="shrink-0 w-[260px] md:w-[280px] text-left rounded-2xl overflow-hidden snap-start transition-shadow hover:shadow-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2"
                      style={{
                        background: '#FFFFFF',
                        border: `1px solid ${theme.blob}66`,
                        boxShadow: '0 2px 8px rgba(0,0,0,0.04)',
                      }}
                    >
                      <div className="flex flex-col h-full p-5 min-h-[220px]">
                        <div className="flex justify-center -mt-4 -mb-2">
                          <WorldIconBlob world={theme.worldKey} size={120} compact />
                        </div>
                        <span className="font-mono text-[11px] font-medium tracking-[0.2em]" style={{ color: tones.midText(rawTheme) }}>
                          {cNumber}
                        </span>
                        <h4 className="font-serif text-[20px] md:text-[22px] font-medium tracking-tight leading-[1.05] text-[#1A1A1A] mt-1">
                          {c.title}
                        </h4>
                        <p className="text-[12px] leading-snug mt-2" style={{ color: 'rgba(0,0,0,0.55)' }}>
                          {c.description}
                        </p>
                        <div className="mt-auto pt-3 flex items-center gap-2">
                          {cCompleted ? (
                            <span className="inline-flex items-center justify-center w-4 h-4 rounded-full" style={{ background: theme.mid, color: 'white' }}>
                              <CheckCircle2 size={10} />
                            </span>
                          ) : (
                            <span className="h-1 rounded-full overflow-hidden flex-1" style={{ background: `${theme.deep}1F` }}>
                              <span className="block h-full rounded-full" style={{ width: `${cPct}%`, background: theme.mid }} />
                            </span>
                          )}
                          <span className="text-[10px] font-mono font-bold tabular-nums" style={{ color: theme.deep }}>
                            {cCompleted ? 'Done' : `${cPct}%`}
                          </span>
                        </div>
                      </div>
                    </motion.button>
                  );
                })}
              </div>

              {/* Scroll arrows — fade in/out based on scroll position */}
              <AnimatePresence>
                {canScrollLeft && (
                  <motion.button
                    key="left"
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.8 }}
                    transition={{ duration: 0.18 }}
                    onClick={() => scrollByCard(-1)}
                    aria-label="Scroll modules left"
                    className="absolute left-0 top-1/2 -translate-y-1/2 z-10 w-10 h-10 rounded-full flex items-center justify-center"
                    style={{
                      background: '#FFFFFF',
                      border: `1px solid ${theme.blob}66`,
                      boxShadow: '0 4px 12px rgba(0,0,0,0.08)',
                      color: tones.midText(rawTheme),
                    }}
                  >
                    <ChevronLeft size={18} />
                  </motion.button>
                )}
                {canScrollRight && (
                  <motion.button
                    key="right"
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.8 }}
                    transition={{ duration: 0.18 }}
                    onClick={() => scrollByCard(1)}
                    aria-label="Scroll modules right"
                    className="absolute right-0 top-1/2 -translate-y-1/2 z-10 w-10 h-10 rounded-full flex items-center justify-center"
                    style={{
                      background: '#FFFFFF',
                      border: `1px solid ${theme.blob}66`,
                      boxShadow: '0 4px 12px rgba(0,0,0,0.08)',
                      color: tones.midText(rawTheme),
                    }}
                  >
                    <ChevronRight size={18} />
                  </motion.button>
                )}
              </AnimatePresence>
            </div>

            <p className="text-center mt-3 font-mono text-[10px] font-bold uppercase tracking-[0.22em]" style={{ color: `${theme.deep}99` }}>
              Module {safeIndex + 1} of {courses.length}
            </p>
          </div>
        )}
      </LayoutGroup>
    </div>
  );
}
