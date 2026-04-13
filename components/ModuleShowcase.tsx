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
   Category gradients — matching KnowledgeTree tile colours
   ═══════════════════════════════════════════════════════ */
const CATEGORY_GRADIENTS: Record<string, { from: string; to: string }> = {
  'architecture-mindset': { from: '#4f8ef7', to: '#2563eb' },
  'science-growth': { from: '#f7b84e', to: '#e8860c' },
  'learning-cheat-codes': { from: '#2dd4bf', to: '#0d9488' },
  'subject-specific-science': { from: '#f472b6', to: '#db2777' },
  'exam-zone': { from: '#f87171', to: '#dc2626' },
  'the-shield': { from: '#6366f1', to: '#4338ca' },
  'the-launchpad': { from: '#34d399', to: '#059669' },
};

const getGradient = (category: string) =>
  CATEGORY_GRADIENTS[category] || { from: '#2dd4bf', to: '#0d9488' };

/* Get section titles for any module */
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
  const gradient = getGradient(categoryId);

  const goTo = useCallback((idx: number) => {
    if (idx < 0 || idx >= courses.length || idx === currentIndex) return;
    setDirection(idx > currentIndex ? 1 : -1);
    setCurrentIndex(idx);
    setSectionsExpanded(false);
  }, [currentIndex, courses.length]);

  const goNext = useCallback(() => goTo(currentIndex + 1), [goTo, currentIndex]);
  const goPrev = useCallback(() => goTo(currentIndex - 1), [goTo, currentIndex]);

  const handleDragEnd = useCallback((_: any, info: { offset: { x: number } }) => {
    if (info.offset.x < -50) goNext();
    else if (info.offset.x > 50) goPrev();
  }, [goNext, goPrev]);

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

  const cardVariants = {
    enter: (dir: number) => ({ x: dir > 0 ? '110%' : '-110%', opacity: 1 }),
    center: { x: 0, opacity: 1 },
    exit: (dir: number) => ({ x: dir > 0 ? '-110%' : '110%', rotateZ: dir > 0 ? -4 : 4, opacity: 0.7 }),
  };

  return (
    <div className="w-full max-w-6xl mx-auto px-4">
      <div className="relative">

        {/* Peek cards */}
        <div className="relative">
          {courses.length > 2 && (
            <div
              className="absolute rounded-3xl pointer-events-none"
              style={{ top: 24, left: 32, right: 32, height: '100%', backgroundColor: gradient.to, opacity: 0.3, zIndex: 1 }}
            />
          )}
          {courses.length > 1 && (
            <div
              className="absolute rounded-3xl pointer-events-none"
              style={{ top: 12, left: 16, right: 16, height: '100%', backgroundColor: gradient.to, opacity: 0.5, zIndex: 2 }}
            />
          )}

          {/* Primary card */}
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
              style={{ boxShadow: '0 20px 60px rgba(0,0,0,0.12), 0 0 0 1px rgba(0,0,0,0.04)' }}
            >
              <div className="flex flex-col md:flex-row min-h-[340px] md:min-h-[520px]">
                {/* Left — Bold gradient panel */}
                <div
                  className="relative w-full md:w-[40%] min-h-[180px] md:min-h-0 overflow-hidden flex flex-col items-center justify-center"
                  style={{ background: `linear-gradient(135deg, ${gradient.from} 0%, ${gradient.to} 100%)` }}
                >
                  {/* Decorative circles */}
                  <div className="absolute -top-10 -right-10 w-40 h-40 rounded-full" style={{ backgroundColor: 'rgba(255,255,255,0.1)' }} />
                  <div className="absolute bottom-6 -left-8 w-28 h-28 rounded-full" style={{ backgroundColor: 'rgba(255,255,255,0.08)' }} />
                  <div className="absolute top-1/3 right-1/4 w-14 h-14 rounded-full" style={{ backgroundColor: 'rgba(255,255,255,0.06)' }} />

                  {/* Category + module info */}
                  <div className="relative z-10 text-center px-6 md:px-8">
                    <p style={{ fontFamily: "'DM Sans', sans-serif", fontSize: '11px', fontWeight: 700, letterSpacing: '0.15em', color: 'rgba(255,255,255,0.6)', textTransform: 'uppercase', marginBottom: '12px' }}>
                      {categoryTitle}
                    </p>
                    <h3 style={{ fontFamily: "'Source Serif 4', serif", fontSize: '24px', fontWeight: 700, color: '#fff', lineHeight: 1.3 }}>
                      {course.title}
                    </h3>
                    <div className="flex items-center justify-center gap-2 mt-4">
                      <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: '13px', fontWeight: 600, color: 'rgba(255,255,255,0.8)' }}>
                        {currentIndex + 1} / {courses.length}
                      </span>
                    </div>
                  </div>

                  {/* Progress badge */}
                  {(isCompleted || isInProgress) && (
                    <div
                      className="absolute bottom-4 left-1/2 -translate-x-1/2 flex items-center gap-1.5 px-3 py-1.5 rounded-full"
                      style={{ backgroundColor: 'rgba(255,255,255,0.2)', backdropFilter: 'blur(8px)' }}
                    >
                      {isCompleted && <CheckCircle2 size={12} color="#fff" />}
                      <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: '11px', fontWeight: 600, color: '#fff' }}>
                        {isCompleted ? 'Complete' : `${progress.unlockedSection}/${course.sectionsCount}`}
                      </span>
                    </div>
                  )}
                </div>

                {/* Right — Content */}
                <div className="flex-1 p-6 md:p-10 lg:p-12 flex flex-col bg-white dark:bg-zinc-900">
                  <div className="flex-1 flex flex-col">
                    <p
                      className="text-[11px] font-semibold uppercase tracking-wider mb-3"
                      style={{ color: gradient.from, letterSpacing: '0.12em' }}
                    >
                      {categoryTitle}
                    </p>

                    <h2
                      className="font-serif font-semibold leading-tight mb-3 text-zinc-900 dark:text-white"
                      style={{ fontSize: 'clamp(24px, 3.5vw, 42px)', letterSpacing: '-0.02em' }}
                    >
                      {course.title}
                    </h2>

                    {course.subtitle && (
                      <p className="text-base mb-2 text-zinc-600 dark:text-zinc-400" style={{ lineHeight: 1.5 }}>
                        {course.subtitle}
                      </p>
                    )}

                    <p className="text-sm mb-6 text-zinc-500 dark:text-zinc-500" style={{ lineHeight: 1.6 }}>
                      {course.description}
                    </p>

                    {/* Actions */}
                    <div className="flex flex-col gap-3 mb-6">
                      <button
                        onClick={() => onSelectCourse(course.id)}
                        className="w-full text-white font-semibold transition-all active:translate-y-[2px]"
                        style={{
                          background: `linear-gradient(135deg, ${gradient.from}, ${gradient.to})`,
                          borderRadius: 100,
                          padding: '15px 32px',
                          fontSize: 16,
                          boxShadow: `0 4px 0 ${gradient.to}`,
                          borderBottom: `3px solid ${gradient.to}`,
                        }}
                      >
                        {ctaLabel}
                      </button>

                      <button
                        onClick={() => setSectionsExpanded(!sectionsExpanded)}
                        className="w-full flex items-center justify-center gap-1.5 py-3 rounded-full transition-colors"
                        style={{ fontSize: 14, fontWeight: 500, color: gradient.from, backgroundColor: `${gradient.from}10`, border: `1.5px solid ${gradient.from}25` }}
                      >
                        What&rsquo;s in this module
                        <motion.span animate={{ rotate: sectionsExpanded ? 180 : 0 }} transition={{ duration: 0.2 }}>
                          <ChevronDown size={16} />
                        </motion.span>
                      </button>
                    </div>

                    {/* Expandable sections */}
                    <AnimatePresence>
                      {sectionsExpanded && (
                        <motion.div
                          initial={{ height: 0, opacity: 0 }}
                          animate={{ height: 'auto', opacity: 1 }}
                          exit={{ height: 0, opacity: 0 }}
                          transition={{ duration: 0.3, ease: [0.25, 1, 0.5, 1] }}
                          className="overflow-hidden mb-6"
                        >
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
                                      width: 22, height: 22, borderRadius: '50%',
                                      backgroundColor: sectionDone ? gradient.from : '#e0dbd4',
                                      color: sectionDone ? '#fff' : '#9e9186',
                                      fontSize: 11, fontWeight: 700,
                                    }}
                                  >
                                    {sectionDone ? <CheckCircle2 size={12} /> : i + 1}
                                  </span>
                                  <div>
                                    <p className="text-sm font-medium text-zinc-900 dark:text-white">
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

                    {/* Metadata */}
                    <div className="mt-auto pt-5" style={{ borderTop: '1px solid rgba(0,0,0,0.06)' }}>
                      <div className="flex flex-wrap items-center gap-6">
                        <div>
                          <p className="text-[10px] font-semibold uppercase tracking-wider text-zinc-400" style={{ letterSpacing: '0.1em' }}>Time</p>
                          <p className="text-sm font-medium mt-0.5 text-zinc-900 dark:text-white">{estimatedMinutes} min</p>
                        </div>
                        <div>
                          <p className="text-[10px] font-semibold uppercase tracking-wider text-zinc-400" style={{ letterSpacing: '0.1em' }}>Progress</p>
                          <p className="text-sm font-medium mt-0.5" style={{ color: isCompleted ? gradient.from : undefined }}>{progressLabel}</p>
                        </div>
                        {course.tags.length > 0 && (
                          <div>
                            <p className="text-[10px] font-semibold uppercase tracking-wider text-zinc-400" style={{ letterSpacing: '0.1em' }}>Topics</p>
                            <p className="text-sm font-medium mt-0.5 text-zinc-500">{course.tags.join(', ')}</p>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          </AnimatePresence>
        </motion.div>

        </div>

        {/* Navigation arrows */}
        {currentIndex > 0 && (
          <button
            onClick={goPrev}
            className="absolute left-[-24px] top-1/2 -translate-y-1/2 w-12 h-12 rounded-full flex items-center justify-center transition-all hover:scale-110 shadow-lg"
            style={{ backgroundColor: '#fff', border: '1px solid rgba(0,0,0,0.08)', zIndex: 10 }}
          >
            <ChevronLeft size={22} style={{ color: gradient.from }} />
          </button>
        )}
        {currentIndex < courses.length - 1 && (
          <button
            onClick={goNext}
            className="absolute right-[-24px] top-1/2 -translate-y-1/2 w-12 h-12 rounded-full flex items-center justify-center transition-all hover:scale-110 shadow-lg"
            style={{ backgroundColor: '#fff', border: '1px solid rgba(0,0,0,0.08)', zIndex: 10 }}
          >
            <ChevronRight size={22} style={{ color: gradient.from }} />
          </button>
        )}
      </div>

      {/* Progress chips */}
      <div className="flex items-center justify-center gap-2 flex-nowrap" style={{ marginTop: 48 }}>
        {courses.map((c, i) => {
          const p = userProgress[c.id];
          const done = p && p.unlockedSection >= c.sectionsCount;
          const isCurrent = i === currentIndex;
          const rawProgress = p ? p.unlockedSection / c.sectionsCount : 0;
          const chipInProgress = rawProgress > 0 && rawProgress < 1;
          const visibleFillPct = chipInProgress ? Math.max(10, Math.round(rawProgress * 100)) : 0;
          const textLight = done || (chipInProgress && visibleFillPct >= 50);

          const chipSize = isCurrent ? 50 : 42;

          return (
            <motion.button
              key={c.id}
              onClick={() => goTo(i)}
              layout
              transition={{ duration: 0.25, ease: [0.25, 1, 0.5, 1] }}
              className="relative overflow-hidden shrink-0 flex items-center justify-center rounded-xl"
              style={{
                width: chipSize,
                height: chipSize,
                backgroundColor: done ? gradient.from : isCurrent ? `${gradient.from}15` : '#f0ede8',
                border: isCurrent ? `2px solid ${gradient.from}` : 'none',
                cursor: 'pointer',
              }}
              whileHover={!isCurrent ? { scale: 1.05 } : {}}
              aria-label={`Go to module ${i + 1}: ${c.title}`}
            >
              {chipInProgress && (
                <motion.div
                  className="absolute left-0 right-0 bottom-0"
                  style={{ backgroundColor: gradient.from }}
                  animate={{ height: `${visibleFillPct}%` }}
                  transition={{ duration: 0.4, ease: [0.25, 1, 0.5, 1] }}
                />
              )}
              <span
                className="relative"
                style={{
                  fontSize: isCurrent ? 16 : 14,
                  fontWeight: isCurrent ? 700 : 500,
                  color: textLight ? '#fff' : done ? '#fff' : isCurrent ? gradient.from : '#8a8a8a',
                  zIndex: 1,
                }}
              >
                {i + 1}
              </span>
            </motion.button>
          );
        })}
      </div>

      <p className="text-center mt-4 text-xs" style={{ color: '#9e9186' }}>
        Module {currentIndex + 1} of {courses.length}
      </p>
    </div>
  );
}
