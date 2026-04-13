/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useCallback, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronLeft, ChevronRight, CheckCircle2, ChevronDown } from 'lucide-react';
import { type CourseData } from './Library';
import { MODULE_SECTIONS, type SectionInfo } from '../moduleSections';
import { SUBJECT_MODULE_CONTENT } from '../subjectModuleData';

/* ═══════════════════════════════════════════════════════
   Aurora gradient palettes per category
   ═══════════════════════════════════════════════════════ */
const CATEGORY_AURORA: Record<string, { base: string; layers: string[] }> = {
  'architecture-mindset': {
    base: '#E8E3F0',
    layers: [
      'radial-gradient(ellipse 140% 70% at 50% 50%, rgba(140,120,210,0.45) 0%, transparent 65%)',
      'radial-gradient(ellipse 100% 50% at 35% 40%, rgba(155,135,225,0.3) 0%, transparent 60%)',
      'radial-gradient(ellipse 120% 55% at 50% 95%, rgba(180,140,210,0.35) 0%, transparent 50%)',
      'radial-gradient(ellipse 60% 65% at 0% 60%, rgba(120,145,225,0.35) 0%, transparent 60%)',
      'radial-gradient(ellipse 55% 40% at 80% 20%, rgba(200,170,230,0.25) 0%, transparent 50%)',
    ],
  },
  'science-growth': {
    base: '#F0EBE0',
    layers: [
      'radial-gradient(ellipse 140% 70% at 50% 50%, rgba(210,170,100,0.4) 0%, transparent 65%)',
      'radial-gradient(ellipse 100% 50% at 35% 40%, rgba(225,190,120,0.3) 0%, transparent 60%)',
      'radial-gradient(ellipse 120% 55% at 50% 95%, rgba(240,160,100,0.35) 0%, transparent 50%)',
      'radial-gradient(ellipse 60% 65% at 100% 60%, rgba(200,155,90,0.3) 0%, transparent 60%)',
      'radial-gradient(ellipse 55% 40% at 20% 80%, rgba(230,180,110,0.25) 0%, transparent 50%)',
    ],
  },
  'learning-cheat-codes': {
    base: '#E3EDE8',
    layers: [
      'radial-gradient(ellipse 140% 70% at 50% 50%, rgba(80,170,150,0.4) 0%, transparent 65%)',
      'radial-gradient(ellipse 100% 50% at 35% 40%, rgba(100,190,170,0.3) 0%, transparent 60%)',
      'radial-gradient(ellipse 120% 55% at 50% 95%, rgba(60,155,135,0.35) 0%, transparent 50%)',
      'radial-gradient(ellipse 60% 65% at 0% 60%, rgba(90,180,160,0.3) 0%, transparent 60%)',
      'radial-gradient(ellipse 55% 40% at 80% 20%, rgba(120,200,180,0.2) 0%, transparent 50%)',
    ],
  },
  'subject-specific-science': {
    base: '#E8E8EC',
    layers: [
      'radial-gradient(ellipse 140% 70% at 50% 50%, rgba(140,145,165,0.35) 0%, transparent 65%)',
      'radial-gradient(ellipse 100% 50% at 35% 40%, rgba(160,155,180,0.3) 0%, transparent 60%)',
      'radial-gradient(ellipse 120% 55% at 50% 95%, rgba(130,140,170,0.3) 0%, transparent 50%)',
      'radial-gradient(ellipse 60% 65% at 100% 60%, rgba(150,150,175,0.25) 0%, transparent 60%)',
      'radial-gradient(ellipse 55% 40% at 20% 80%, rgba(170,165,190,0.2) 0%, transparent 50%)',
    ],
  },
  'exam-zone': {
    base: '#F0E5E5',
    layers: [
      'radial-gradient(ellipse 140% 70% at 50% 50%, rgba(210,120,130,0.4) 0%, transparent 65%)',
      'radial-gradient(ellipse 100% 50% at 35% 40%, rgba(225,140,150,0.3) 0%, transparent 60%)',
      'radial-gradient(ellipse 120% 55% at 50% 95%, rgba(200,110,140,0.35) 0%, transparent 50%)',
      'radial-gradient(ellipse 60% 65% at 0% 60%, rgba(190,130,160,0.3) 0%, transparent 60%)',
      'radial-gradient(ellipse 55% 40% at 80% 20%, rgba(230,150,140,0.2) 0%, transparent 50%)',
    ],
  },
};

const getAurora = (category: string) =>
  CATEGORY_AURORA[category] || CATEGORY_AURORA['learning-cheat-codes'];

/* Get section titles for any module — covers both standard and subject modules */
function getSectionsForModule(moduleId: string, sectionsCount: number): SectionInfo[] {
  // Check standard modules first
  if (MODULE_SECTIONS[moduleId]) return MODULE_SECTIONS[moduleId];

  // Check subject modules — strip 'subject-' prefix and '-protocol' suffix to get subjectId
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

  // Fallback to generic
  return Array.from({ length: sectionsCount }, (_, i) => ({
    title: `Section ${i + 1}`,
    eyebrow: '',
  }));
}

/* ═══════════════════════════════════════════════════════
   ModuleShowcase — single-card carousel
   ═══════════════════════════════════════════════════════ */

interface ModuleShowcaseProps {
  courses: CourseData[];
  categoryTitle: string;
  categoryId: string;
  userProgress: Record<string, { unlockedSection: number }>;
  onSelectCourse: (courseId: string) => void;
}

export default function ModuleShowcase({
  courses,
  categoryTitle,
  categoryId,
  userProgress,
  onSelectCourse,
}: ModuleShowcaseProps) {
  const [currentIndex, setCurrentIndex] = useState(() => {
    // Start on the first non-completed module
    const firstIncomplete = courses.findIndex(c => {
      const p = userProgress[c.id];
      return !p || p.unlockedSection < c.sectionsCount;
    });
    return firstIncomplete === -1 ? 0 : firstIncomplete;
  });
  const [direction, setDirection] = useState(0);
  const [sectionsExpanded, setSectionsExpanded] = useState(false);

  const course = courses[currentIndex];
  const progress = userProgress[course.id];
  const isCompleted = progress && progress.unlockedSection >= course.sectionsCount;
  const isInProgress = progress && progress.unlockedSection > 0 && !isCompleted;
  const aurora = getAurora(categoryId);

  const goTo = useCallback((idx: number) => {
    if (idx < 0 || idx >= courses.length || idx === currentIndex) return;
    setDirection(idx > currentIndex ? 1 : -1);
    setCurrentIndex(idx);
    setSectionsExpanded(false);
  }, [currentIndex, courses.length]);

  const goNext = useCallback(() => goTo(currentIndex + 1), [goTo, currentIndex]);
  const goPrev = useCallback(() => goTo(currentIndex - 1), [goTo, currentIndex]);

  // Swipe / drag navigation
  const handleDragEnd = useCallback((_: any, info: { offset: { x: number } }) => {
    const swipeThreshold = 50;
    if (info.offset.x < -swipeThreshold) {
      goNext();
    } else if (info.offset.x > swipeThreshold) {
      goPrev();
    }
  }, [goNext, goPrev]);

  // Keyboard navigation
  useEffect(() => {
    const handleKey = (e: KeyboardEvent) => {
      if (e.key === 'ArrowRight') goNext();
      if (e.key === 'ArrowLeft') goPrev();
    };
    window.addEventListener('keydown', handleKey);
    return () => window.removeEventListener('keydown', handleKey);
  }, [goNext, goPrev]);

  const ctaLabel = isCompleted ? 'Review module' : isInProgress ? 'Continue module' : 'Start module';
  const progressLabel = isCompleted
    ? 'Completed'
    : isInProgress
    ? `In progress: ${progress.unlockedSection} of ${course.sectionsCount} sections`
    : 'Not started';
  const estimatedMinutes = course.sectionsCount * 8;

  // The entire card is one rigid object — it flicks as a unit
  const cardVariants = {
    enter: (dir: number) => ({
      x: dir > 0 ? '110%' : '-110%',
      rotateZ: 0,
      opacity: 1,
    }),
    center: {
      x: 0,
      rotateZ: 0,
      opacity: 1,
    },
    exit: (dir: number) => ({
      x: dir > 0 ? '-110%' : '110%',
      rotateZ: dir > 0 ? -4 : 4,
      opacity: 0.7,
    }),
  };

  return (
    <div className="w-full max-w-5xl mx-auto px-4">
      {/* Outer container — stays fixed, holds arrows + peeks + dots */}
      <div className="relative">

        {/* Card stack container — peek cards are absolute behind primary */}
        <div className="relative">

          {/* Second peek card — furthest back, most inset, most offset */}
          {courses.length > 2 && (
            <div
              className="absolute rounded-3xl pointer-events-none"
              style={{
                top: 24,
                left: 32,
                right: 32,
                height: '100%',
                backgroundColor: '#E8E0D0',
                border: '1px solid rgba(0,0,0,0.04)',
                zIndex: 1,
              }}
            />
          )}

          {/* First peek card — middle layer */}
          {courses.length > 1 && (
            <div
              className="absolute rounded-3xl pointer-events-none"
              style={{
                top: 12,
                left: 16,
                right: 16,
                height: '100%',
                backgroundColor: '#F0E8D8',
                border: '1px solid rgba(0,0,0,0.05)',
                zIndex: 2,
              }}
            />
          )}

          {/* Primary card area — frontmost, natural flow gives container its height */}
          <motion.div
            className="relative"
            style={{ zIndex: 3, overflow: 'hidden', touchAction: 'pan-y' }}
            drag="x"
            dragConstraints={{ left: 0, right: 0 }}
            dragElastic={0.2}
            onDragEnd={handleDragEnd}
          >
          <AnimatePresence mode="popLayout" custom={direction} initial={false}>
            <motion.div
              key={course.id}
              custom={direction}
              variants={cardVariants}
              initial="enter"
              animate="center"
              exit="exit"
              transition={{ duration: 0.45, ease: [0.22, 1, 0.36, 1] }}
              className="rounded-3xl overflow-hidden"
              style={{ backgroundColor: '#FAF7F2', border: '1px solid rgba(0,0,0,0.06)' }}
            >
              {/* The entire card — graphic + content — is ONE unit inside this motion.div */}
              <div className="flex flex-col md:flex-row min-h-[320px] md:min-h-[480px]">
                {/* Left — Aurora graphic */}
                <div className="relative w-full md:w-[40%] min-h-[200px] md:min-h-0 overflow-hidden">
                  <div className="absolute inset-0" style={{ backgroundColor: aurora.base }} />
                  {aurora.layers.map((layer, i) => (
                    <div key={i} className="absolute inset-0" style={{ background: layer }} />
                  ))}
                  <div className="absolute inset-0" style={{ opacity: 0.03, backgroundImage: 'url("data:image/svg+xml,%3Csvg viewBox=\'0 0 256 256\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cfilter id=\'noise\'%3E%3CfeTurbulence type=\'fractalNoise\' baseFrequency=\'0.65\' numOctaves=\'3\' stitchTiles=\'stitch\'/%3E%3C/filter%3E%3Crect width=\'100%25\' height=\'100%25\' filter=\'url(%23noise)\'/%3E%3C/svg%3E")' }} />
                </div>

                {/* Right — Content (NO independent animation — moves with card) */}
                <div className="flex-1 p-8 md:p-10 lg:p-12 flex flex-col">
                  <div className="flex-1 flex flex-col">
                  {/* Eyebrow */}
                  <p
                    className="text-[11px] font-semibold uppercase tracking-wider mb-4"
                    style={{ color: '#2A7D6F', letterSpacing: '0.12em' }}
                  >
                    {categoryTitle}
                  </p>

                  {/* Title */}
                  <h2
                    className="font-serif font-semibold leading-tight mb-4"
                    style={{ fontSize: 'clamp(28px, 4vw, 48px)', color: '#1a1a1a', letterSpacing: '-0.02em' }}
                  >
                    {course.title}
                  </h2>

                  {/* Subtitle */}
                  {course.subtitle && (
                    <p className="text-base mb-2" style={{ color: '#5a5550', lineHeight: 1.5 }}>
                      {course.subtitle}
                    </p>
                  )}

                  {/* Description */}
                  <p className="text-sm mb-6" style={{ color: '#7a7068', lineHeight: 1.6 }}>
                    {course.description}
                  </p>

                  {/* Action row */}
                  <div className="flex items-center gap-4 mb-8">
                    <button
                      onClick={() => onSelectCourse(course.id)}
                      className="text-white font-semibold transition-all"
                      style={{
                        backgroundColor: '#2A7D6F',
                        borderRadius: 100,
                        padding: '14px 32px',
                        fontSize: 15,
                      }}
                    >
                      {ctaLabel}
                    </button>

                    <button
                      onClick={() => setSectionsExpanded(!sectionsExpanded)}
                      className="flex items-center gap-1.5 transition-colors"
                      style={{ fontSize: 14, fontWeight: 500, color: '#2A7D6F' }}
                    >
                      What&rsquo;s in this module
                      <motion.span animate={{ rotate: sectionsExpanded ? 180 : 0 }} transition={{ duration: 0.2 }}>
                        <ChevronDown size={16} />
                      </motion.span>
                    </button>
                  </div>

                  {/* Expandable sections list */}
                  <AnimatePresence>
                    {sectionsExpanded && (
                      <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: 'auto', opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        transition={{ duration: 0.3, ease: [0.25, 1, 0.5, 1] }}
                        className="overflow-hidden mb-6"
                      >
                        <p className="text-xs font-semibold uppercase tracking-wider mb-3" style={{ color: '#9e9186', letterSpacing: '0.1em' }}>
                          {course.sectionsCount} sections in this module
                        </p>
                        <div className="space-y-2">
                          {getSectionsForModule(course.id, course.sectionsCount).map((section, i) => {
                            const sectionDone = progress && progress.unlockedSection > i;
                            return (
                              <div
                                key={i}
                                className="flex items-start gap-3 py-2"
                                style={{ borderTop: i === 0 ? 'none' : '1px solid rgba(0,0,0,0.04)' }}
                              >
                                <span
                                  className="shrink-0 mt-0.5 flex items-center justify-center"
                                  style={{
                                    width: 22,
                                    height: 22,
                                    borderRadius: '50%',
                                    backgroundColor: sectionDone ? '#2A7D6F' : '#e0dbd4',
                                    color: sectionDone ? '#fff' : '#9e9186',
                                    fontSize: 11,
                                    fontWeight: 700,
                                  }}
                                >
                                  {sectionDone ? <CheckCircle2 size={12} /> : i + 1}
                                </span>
                                <div>
                                  <p className="text-sm font-medium" style={{ color: sectionDone ? '#1a6358' : '#1a1a1a' }}>
                                    {section.title}
                                  </p>
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

                  {/* Divider */}
                  <div className="mt-auto" style={{ height: 1, backgroundColor: 'rgba(0,0,0,0.06)' }} />

                  {/* Metadata row */}
                  <div className="flex flex-wrap items-center gap-6 pt-5">
                    <div>
                      <p className="text-[10px] font-semibold uppercase tracking-wider" style={{ color: '#9e9186', letterSpacing: '0.1em' }}>Estimated time</p>
                      <p className="text-sm font-medium mt-0.5" style={{ color: '#1a1a1a' }}>{estimatedMinutes} minutes</p>
                    </div>
                    <div>
                      <p className="text-[10px] font-semibold uppercase tracking-wider" style={{ color: '#9e9186', letterSpacing: '0.1em' }}>Progress</p>
                      <p className="text-sm font-medium mt-0.5" style={{ color: isCompleted ? '#2A7D6F' : '#1a1a1a' }}>{progressLabel}</p>
                    </div>
                    {course.tags.length > 0 && (
                      <div>
                        <p className="text-[10px] font-semibold uppercase tracking-wider" style={{ color: '#9e9186', letterSpacing: '0.1em' }}>Topics</p>
                        <p className="text-sm font-medium mt-0.5" style={{ color: '#7a7068' }}>{course.tags.join(', ')}</p>
                      </div>
                    )}
                  </div>
                  </div>{/* end flex-col inner */}
                </div>{/* end right column */}
              </div>{/* end flex row */}
            </motion.div>{/* end animated card */}
          </AnimatePresence>
        </motion.div>{/* end overflow container (primary card) */}

        </div>{/* end card stack container */}

        {/* Navigation arrows — OUTSIDE the card stack, on the outer container */}
        {currentIndex > 0 && (
          <button
            onClick={goPrev}
            className="absolute left-[-20px] top-1/2 -translate-y-1/2 w-10 h-10 rounded-full flex items-center justify-center transition-all hover:scale-105"
            style={{ backgroundColor: 'rgba(255,255,255,0.9)', border: '1px solid rgba(0,0,0,0.08)', zIndex: 10 }}
          >
            <ChevronLeft size={20} style={{ color: '#2A7D6F' }} />
          </button>
        )}
        {currentIndex < courses.length - 1 && (
          <button
            onClick={goNext}
            className="absolute right-[-20px] top-1/2 -translate-y-1/2 w-10 h-10 rounded-full flex items-center justify-center transition-all hover:scale-105"
            style={{ backgroundColor: 'rgba(255,255,255,0.9)', border: '1px solid rgba(0,0,0,0.08)', zIndex: 10 }}
          >
            <ChevronRight size={20} style={{ color: '#2A7D6F' }} />
          </button>
        )}
      </div>{/* end outer relative container */}

      {/* Progress chips */}
      <div className="flex items-center justify-center gap-2 flex-nowrap" style={{ marginTop: 48 }}>
        {courses.map((c, i) => {
          const p = userProgress[c.id];
          const done = p && p.unlockedSection >= c.sectionsCount;
          const isCurrent = i === currentIndex;
          const rawProgress = p ? p.unlockedSection / c.sectionsCount : 0;
          const isInProgress = rawProgress > 0 && rawProgress < 1;

          // Clamp minimum visible fill to 10% so even 1/20 sections is visible
          const visibleFillPct = isInProgress ? Math.max(10, Math.round(rawProgress * 100)) : 0;
          // Text colour: cream if fill >= 50% or completed, black if fill < 50%, grey if no progress
          const textLight = done || (isInProgress && visibleFillPct >= 50);

          const chipSize = isCurrent ? 44 : 38;
          const chipRadius = isCurrent ? 9 : 8;
          const chipFontSize = isCurrent ? 14 : 13;
          const chipFontWeight = isCurrent ? 600 : 500;

          return (
            <motion.button
              key={c.id}
              onClick={() => goTo(i)}
              layout
              transition={{ duration: 0.25, ease: [0.25, 1, 0.5, 1] }}
              className="relative overflow-hidden shrink-0 flex items-center justify-center"
              style={{
                width: chipSize,
                height: chipSize,
                borderRadius: chipRadius,
                backgroundColor: done ? '#2A7D6F' : '#EBE0C5',
                border: isCurrent ? '2px solid #2A7D6F' : 'none',
                cursor: 'pointer',
              }}
              whileHover={!isCurrent ? { scale: 1.05 } : {}}
              aria-label={`Go to module ${i + 1}: ${c.title}`}
            >
              {/* Vertical fill — rendered on ALL chips with partial progress */}
              {isInProgress && (
                <motion.div
                  className="absolute left-0 right-0 bottom-0"
                  style={{ backgroundColor: '#2A7D6F' }}
                  animate={{ height: `${visibleFillPct}%` }}
                  transition={{ duration: 0.4, ease: [0.25, 1, 0.5, 1] }}
                />
              )}
              {/* Number */}
              <span
                className="relative"
                style={{
                  fontSize: chipFontSize,
                  fontWeight: chipFontWeight,
                  color: textLight ? '#FDF8F0' : isInProgress ? '#1A1A1A' : done ? '#FDF8F0' : '#8A8A8A',
                  zIndex: 1,
                }}
              >
                {i + 1}
              </span>
            </motion.button>
          );
        })}
      </div>

      {/* Module counter */}
      <p className="text-center mt-4 text-xs" style={{ color: '#9e9186' }}>
        Module {currentIndex + 1} of {courses.length}
      </p>
    </div>
  );
}
