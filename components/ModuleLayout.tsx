/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useRef, useMemo } from 'react';
import { motion, AnimatePresence, useReducedMotion } from 'framer-motion';
import { ArrowLeft, ArrowRight, Search, Palette, Sun, Moon, PanelLeft, ArrowUpRight } from 'lucide-react';
import { type ModuleProgress, type SectionDefinition, type ModuleTheme } from '../types';
import { ReferencesModal, ModuleReferencesProvider } from './ModuleReferences';
import { type Reference } from '../data/references/types';
import { useSettingsContext } from '../contexts/SettingsContext';
import { useModulePosition } from '../contexts/ModulePositionContext';
import { COLORS } from '../design/tokens';
import ModuleCompleteScreen from './ModuleCompleteScreen';
import { useNavigation } from '../contexts/NavigationContext';
import KobraScope from './approved-ui-runtime';
import BackButton from './ui/BackButton';
import { Button } from './approved-ui-runtime';
import { Toasts, toast } from './approved-ui-runtime';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from './approved-ui-runtime';
import { CommandMenu, openCommandMenu } from './approved-ui-runtime';
import { BrandBook } from './learning/BrandBook';
import { CompletionMark } from './learning/CompletionMark';
import { ReadingProgress } from './learning/ReadingProgress';
import { ReaderNotes } from './learning/ReaderNotes';
import { Eyebrow } from './learning/shared';
import { requestedModuleSection, clearModuleSectionRequest } from './learning/data';
import { readSectionIds, readingCheckpoint, resumeSection } from '../utils/moduleReadingProgress';
import { useModuleResponses } from '../hooks/useModuleResponses';
import { ResponseSaveStatus } from './learning/ResponseSaveStatus';
import './learning/module-reader-preview.css';
import './learning/sidebar-directions.css';
import './learning/reader.css';
import './learning/module-activities-dark.css';
import './learning/module-discovery.css';

const CONFETTI_COLORS = ['#CC785C', '#f59e0b', '#3b82f6', '#10b981', '#8b5cf6', '#ef4444', '#ec4899'];
const CONFETTI_COUNT = 60;

const ConfettiOverlay: React.FC<{ onDone: () => void }> = ({ onDone }) => {
  const pieces = useMemo(() => Array.from({ length: CONFETTI_COUNT }, (_, i) => ({
    id: i, x: Math.random() * 100, delay: Math.random() * 0.6,
    duration: 1.8 + Math.random() * 1.2, color: CONFETTI_COLORS[i % CONFETTI_COLORS.length],
    rotation: Math.random() * 360, size: 6 + Math.random() * 6, drift: (Math.random() - 0.5) * 40,
  })), []);

  useEffect(() => {
    const timer = setTimeout(onDone, 2800);
    return () => clearTimeout(timer);
  }, [onDone]);

  return <div className="fixed inset-0 z-[200] pointer-events-none overflow-hidden">
    {pieces.map(p => <motion.div key={p.id} initial={{ y: -20, x: `${p.x}vw`, opacity: 1, rotate: 0 }} animate={{ y: '110vh', x: `${p.x + p.drift}vw`, opacity: [1, 1, 0], rotate: p.rotation + 360 }} transition={{ duration: p.duration, delay: p.delay, ease: 'easeIn' }} style={{ position: 'absolute', width: p.size, height: p.size * 0.6, backgroundColor: p.color, borderRadius: 2 }} />)}
  </div>;
};

interface ModuleLayoutProps {
  moduleNumber: string;
  moduleTitle: string;
  moduleSubtitle?: string;
  moduleDescription?: string;
  theme: ModuleTheme;
  sections: SectionDefinition[];
  onBack: () => void;
  progress: ModuleProgress;
  onProgressUpdate: (p: ModuleProgress) => void;
  finishButtonText?: string;
  /** When essentials mode uses fewer sections, set this to the full section count
   *  so completion is reported correctly against courseData.sectionsCount */
  fullSectionsCount?: number;
  /** Existing module sources feed inline Kobra citation bubbles and the
   *  Sources & further reading list in Contents. */
  references?: Reference[];
  children: (activeSection: number) => React.ReactNode;
  // Celebration screen props (optional)
  categoryColor?: string;
  modulesCompleted?: number;
  totalModules?: number;
  northStarStatement?: string;
}

export const ModuleLayout: React.FC<ModuleLayoutProps> = ({
  moduleNumber,
  moduleTitle,
  moduleSubtitle,
  moduleDescription,
  theme: _theme,
  sections,
  onBack,
  progress,
  onProgressUpdate,
  finishButtonText = 'Complete Section',
  fullSectionsCount,
  references,
  children,
  categoryColor,
  modulesCompleted,
  totalModules,
  northStarStatement,
}) => {
  const navigation = useNavigation();
  const settingsCtx = useSettingsContext();
  const reducedMotion = useReducedMotion();
  const moduleId = navigation.state?.currentModuleId ?? moduleTitle;
  const moduleResponses = useModuleResponses(moduleId);
  const readingMode = settingsCtx?.settings.essentialsMode ? 'essentials' : 'full';
  const requestedSection = useRef(requestedModuleSection(moduleId));
  const previousMode = useRef(readingMode);
  const focusRequested = useRef(false);
  const modulePosition = useModulePosition();
  const displayedModuleNumber = modulePosition?.displayNumber ?? moduleNumber;
  const [activeSection, setActiveSection] = useState(
    Math.max(0, Math.min(requestedSection.current ?? resumeSection(progress, sections, readingMode), sections.length - 1))
  );
  const [desktopSidebarOpen, setDesktopSidebarOpen] = useState(true);
  const [mobileSectionsOpen, setMobileSectionsOpen] = useState(false);
  const [referencesOpen, setReferencesOpen] = useState(false);
  const [notesOpen, setNotesOpen] = useState(false);
  const [showConfetti, setShowConfetti] = useState(false);
  const [showCelebration, setShowCelebration] = useState(false);
  const [pickerOpen, setPickerOpen] = useState(false);
  const isCompletingRef = useRef(false);
  const mainRef = useRef<HTMLElement>(null);
  const readIds = readSectionIds(progress, sections, readingMode);

  useEffect(() => {
    if (previousMode.current !== readingMode) {
      setActiveSection(resumeSection(progress, sections, readingMode));
      previousMode.current = readingMode;
    }
    clearModuleSectionRequest(moduleId);
  }, [moduleId, progress, sections, readingMode]);

  // Scroll to top whenever the active section changes
  useEffect(() => {
    window.scrollTo({ top: 0 });
    if (mainRef.current) {
      mainRef.current.scrollTop = 0;
    }
    if (!focusRequested.current) return;
    const timer = setTimeout(() => {
      mainRef.current?.querySelector<HTMLElement>('.mr-lesson-heading h1')?.focus({ preventScroll: true });
      focusRequested.current = false;
    }, reducedMotion ? 0 : 300);
    return () => clearTimeout(timer);
  }, [activeSection, reducedMotion]);

  const handleCompleteSection = () => {
    if (isCompletingRef.current) return;
    isCompletingRef.current = true;
    const isLastSection = activeSection === sections.length - 1;
    const isNewCompletion = !readIds.has(sections[activeSection].id);
    let checkpoint = readingCheckpoint(progress, sections, readingMode, activeSection, true, fullSectionsCount);
    const allRead = readSectionIds(checkpoint, sections, readingMode).size === sections.length;
    const nextIndex = isLastSection
      ? sections.findIndex(section => !readSectionIds(checkpoint, sections, readingMode).has(section.id))
      : activeSection + 1;
    if (nextIndex >= 0 && !allRead) checkpoint = readingCheckpoint(checkpoint, sections, readingMode, nextIndex, false, fullSectionsCount);
    onProgressUpdate(checkpoint);
    if (isNewCompletion) {
      if (!allRead) toast({ message: 'Reading checkpoint saved.', state: 'success' });
    }
    if (allRead && isNewCompletion) {
      setShowConfetti(!reducedMotion);
      setShowCelebration(true);
    } else if (nextIndex >= 0) {
      focusRequested.current = true;
      setActiveSection(nextIndex);
    } else {
      onBack();
    }
    setTimeout(() => { isCompletingRef.current = false; }, 500);
  };

  const handleConfettiDone = () => setShowConfetti(false);

  const handleCelebrationContinue = () => {
    setShowCelebration(false);
    onBack();
  };

  const handleJumpToSection = (index: number) => {
    if (index >= 0 && index < sections.length) {
      focusRequested.current = true;
      setActiveSection(index);
      setMobileSectionsOpen(false);
      onProgressUpdate(readingCheckpoint(progress, sections, readingMode, index, false, fullSectionsCount));
    }
  };

  const handlePrev = () => {
    if (activeSection > 0) {
      handleJumpToSection(activeSection - 1);
    }
  };

  const completedSections = readIds.size;

  // Reading comfort — ReadingSection (ModuleShared) consumes these variables.
  const readingScale = settingsCtx?.settings.readingScale ?? 1;
  const readingRelaxed = settingsCtx?.settings.readingSpacing === 'relaxed';
  const READING_SCALES = [0.9, 1, 1.1, 1.2, 1.4, 1.6, 1.8, 2];
  const stepReadingScale = (dir: 1 | -1) => {
    const idx = READING_SCALES.indexOf(readingScale);
    const next = READING_SCALES[Math.min(READING_SCALES.length - 1, Math.max(0, (idx === -1 ? 1 : idx) + dir))];
    settingsCtx?.updateSetting('readingScale', next);
  };

  const readingControls = settingsCtx && (
    <div>
      <p className="text-[9px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-1.5">Reading Comfort</p>
      <div className="flex items-center gap-2">
        <button
          onClick={() => stepReadingScale(-1)}
          disabled={readingScale <= READING_SCALES[0]}
          aria-label="Smaller text"
          className="w-8 h-8 rounded-lg border border-zinc-200 dark:border-zinc-700 text-xs font-bold text-zinc-600 dark:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-800 disabled:opacity-30"
        >
          A−
        </button>
        <span className="text-xs font-semibold tabular-nums text-zinc-500 dark:text-zinc-400 min-w-[44px] text-center">
          {Math.round(readingScale * 100)}%
        </span>
        <button
          onClick={() => stepReadingScale(1)}
          disabled={readingScale >= READING_SCALES[READING_SCALES.length - 1]}
          aria-label="Larger text"
          className="w-8 h-8 rounded-lg border border-zinc-200 dark:border-zinc-700 text-sm font-bold text-zinc-600 dark:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-800 disabled:opacity-30"
        >
          A+
        </button>
        <button
          onClick={() => settingsCtx.updateSetting('readingSpacing', readingRelaxed ? 'normal' : 'relaxed')}
          className={`flex-1 min-h-[32px] px-1.5 py-1 leading-tight rounded-lg border text-[11px] font-semibold transition-colors ${readingRelaxed ? 'border-[var(--accent-hex)] text-[var(--accent-hex)] bg-[rgba(var(--accent),0.08)]' : 'border-zinc-200 dark:border-zinc-700 text-zinc-600 dark:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-800'}`}
        >
          {readingRelaxed ? 'Relaxed spacing ✓' : 'Relaxed spacing'}
        </button>
      </div>
    </div>
  );

  const contents = (
    <div className="mr-contents-inner" data-sidebar="notebook">
      <div className="mr-notebook-label"><BrandBook size={39} /><div><Eyebrow>{moduleSubtitle || `Module ${displayedModuleNumber}`}</Eyebrow><span>Your learning notebook</span></div></div>
      <h2>{moduleTitle}</h2>
      <ReadingProgress done={completedSections} total={sections.length} />
      <nav className="mr-progress-list" aria-label="Module sections"><ol>
        {sections.map((section, index) => <li key={section.id}><button type="button" aria-label={`${section.title}. ${activeSection === index ? 'You’re here' : readIds.has(section.id) ? 'Read · Revisit anytime' : 'Open section'}`} aria-current={activeSection === index ? 'step' : undefined} onClick={() => handleJumpToSection(index)}>
          <CompletionMark number={index + 1} complete={readIds.has(section.id)} current={activeSection === index} />
          <span><strong>{section.title}</strong><small>{activeSection === index ? 'You’re here' : readIds.has(section.id) ? 'Read · Revisit anytime' : 'Open section'}</small></span>
        </button></li>)}
      </ol></nav>
      <div className="mr-contents-foot"><Button variant="ghost" onClick={() => { setMobileSectionsOpen(false); openCommandMenu(); }}><Search />Find a section<kbd>⌘ K</kbd></Button>
        {!!references?.length && <button className="mr-source-link" onClick={() => { setMobileSectionsOpen(false); setReferencesOpen(true); }}>Sources &amp; further reading<ArrowUpRight /></button>}
      </div>
    </div>
  );
  return (
    <KobraScope className="nsu-learning nsu-module-reader theme-compat">
      <div className="mr-main" data-sidebar="notebook" data-contents={desktopSidebarOpen} style={{ ['--reading-scale' as string]: String(readingScale), ['--reading-lh' as string]: readingRelaxed ? '2.15' : '1.85' }}>
        <header className="mr-topbar">
          <div className="mr-breadcrumb"><BackButton onClick={onBack} label="Back to modules" /><span>Module {displayedModuleNumber}</span><span>{moduleTitle}</span></div>
          <div className="mr-tools">
            <Button className="mr-desktop-contents" variant="outline" onClick={() => setDesktopSidebarOpen(value => !value)} aria-expanded={desktopSidebarOpen} aria-controls="module-sidebar-content" aria-label={desktopSidebarOpen ? 'Collapse module navigation' : 'Expand module navigation'}><PanelLeft />Contents</Button>
            <Button className="mr-mobile-contents" variant="outline" onClick={() => setMobileSectionsOpen(true)} aria-label="Open module sections"><PanelLeft />Contents</Button>
            <Button variant="ghost" onClick={() => setNotesOpen(true)}><BrandBook size={23} />Notes</Button>
            {settingsCtx && <Button variant="ghost" size="icon" aria-label="Reading comfort" onClick={() => setPickerOpen(true)}><Palette /></Button>}
          </div>
        </header>
        <div className="mr-layout">
          <aside className="mr-contents" aria-label="Module navigation" id="module-sidebar-content" inert={!desktopSidebarOpen} aria-hidden={!desktopSidebarOpen}>{contents}</aside>
          <main className="mr-reading-area" ref={mainRef}>
            <div className="mr-running-head"><span>{moduleDescription || moduleSubtitle}</span><span>Section {String(activeSection + 1).padStart(2, '0')} / {String(sections.length).padStart(2, '0')}</span></div>
            <article className="mr-paper">
              <ModuleReferencesProvider value={references ?? []}>
                <AnimatePresence mode="wait" initial={false}><motion.div key={sections[activeSection]?.id ?? activeSection} initial={{ opacity: 0, y: reducedMotion ? 0 : 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} transition={{ duration: reducedMotion ? 0 : .22 }} className="mr-page-content">
                  {moduleResponses.isLoaded ? children(activeSection) : <p role="status">Loading your saved drafts…</p>}
                  <ResponseSaveStatus status={moduleResponses.saveStatus} onRetry={moduleResponses.retrySave} />
                  <div className="mr-page-signoff"><span>A little further than before.</span><span>{String(activeSection + 1).padStart(2, '0')}</span></div>
                </motion.div></AnimatePresence>
              </ModuleReferencesProvider>
              <footer className="mr-page-footer">
                <Button variant="ghost" onClick={handlePrev} disabled={activeSection === 0}><ArrowLeft />Previous</Button>
                <div><small>This records reading, not practice. Activities are optional.</small><span>{sections[activeSection + 1]?.title ?? 'Your last page. Yours to revisit.'}</span></div>
                <Button variant="outline" className="nsu-ink-outline" onClick={handleCompleteSection} aria-label={activeSection === sections.length - 1 ? finishButtonText : 'Continue to the next section'}>{activeSection === sections.length - 1 ? finishButtonText : 'Continue'}<ArrowRight /></Button>
              </footer>
            </article>
          </main>
        </div>
      </div>
      <Dialog open={mobileSectionsOpen} onOpenChange={setMobileSectionsOpen}><DialogContent className="mr-contents-dialog"><DialogHeader><DialogTitle>Contents</DialogTitle><DialogDescription>{moduleTitle}</DialogDescription></DialogHeader>{contents}</DialogContent></Dialog>
      <Dialog open={pickerOpen} onOpenChange={setPickerOpen}><DialogContent><DialogHeader><DialogTitle>Make yourself comfortable</DialogTitle><DialogDescription>Choose how you like to read.</DialogDescription></DialogHeader>{readingControls}{settingsCtx && <Button variant="outline" onClick={() => settingsCtx.updateSetting('darkMode', !settingsCtx.settings.darkMode)}>{settingsCtx.settings.darkMode ? <Sun /> : <Moon />}{settingsCtx.settings.darkMode ? 'Light mode' : 'Dark mode'}</Button>}</DialogContent></Dialog>
      <Toasts position="bottom-center" />
      {notesOpen && <ReaderNotes moduleId={moduleId} title={moduleTitle} sectionTitle={sections[activeSection]?.title ?? moduleTitle} sectionIndex={activeSection} open={notesOpen} onClose={() => setNotesOpen(false)} />}
      <CommandMenu placeholder="Find a section…" actions={sections.map((section, index) => ({ id: section.id, label: section.title, hint: readIds.has(section.id) ? 'Read · Revisit anytime' : 'Open section', keywords: [section.eyebrow], icon: <CompletionMark number={index + 1} complete={readIds.has(section.id)} current={index === activeSection} />, action: () => handleJumpToSection(index) }))} />
      {!!references?.length && <ReferencesModal open={referencesOpen} onClose={() => setReferencesOpen(false)} references={references} />}
      {showConfetti && <ConfettiOverlay onDone={handleConfettiDone} />}
      <ModuleCompleteScreen isOpen={showCelebration} moduleTitle={moduleTitle} moduleSubtitle={moduleSubtitle} categoryColor={categoryColor || COLORS.accent} modulesCompleted={modulesCompleted} totalModules={totalModules} sectionsCount={sections.length} northStarStatement={northStarStatement} onContinue={handleCelebrationContinue} onPractice={() => { setShowCelebration(false); navigation.navigateToStudySession(); }} onReview={() => { setShowCelebration(false); setActiveSection(0); }} />
    </KobraScope>
  );
};
