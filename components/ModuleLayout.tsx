/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { AnimatePresence,motion,useReducedMotion } from 'framer-motion';
import { ArrowLeft,ArrowRight,ArrowUpRight,Clock,ListOrdered,Moon,Palette,PanelLeft,Search,Sun } from 'lucide-react';
import React,{ useEffect,useLayoutEffect,useRef,useState } from 'react';
import { useModulePosition } from '../contexts/ModulePositionContext';
import { useNavigation } from '../contexts/NavigationContext';
import { useSettingsContext } from '../contexts/SettingsContext';
import { type Reference } from '../data/references/types';
import { COLORS } from '../design/tokens';
import { useEssentialsMode } from '../hooks/useEssentialsMode';
import { useModuleResponses } from '../hooks/useModuleResponses';
import { type ModuleProgress,type ModuleTheme,type SectionDefinition } from '../types';
import { readSectionIds,readingCheckpoint,resumeSection } from '../utils/moduleReadingProgress';
import ModuleCompleteScreen from './ModuleCompleteScreen';
import { ModuleReferencesProvider,ReferencesModal } from './ModuleReferences';
import KobraScope,{ Button,CommandMenu,Dialog,DialogContent,DialogDescription,DialogHeader,DialogTitle,Toasts,openCommandMenu,toast } from './approved-ui-runtime';
import { BrandBook } from './learning/BrandBook';
import { CompletionMark } from './learning/CompletionMark';
import { ReaderNotes } from './learning/ReaderNotes';
import { ReadingProgress } from './learning/ReadingProgress';
import { ResponseSaveStatus } from './learning/ResponseSaveStatus';
import { clearModuleSectionRequest,requestedModuleSection } from './learning/data';
import './learning/module-activities-dark.css';
import './learning/module-brand-review.css';
import './learning/module-discovery.css';
import './learning/module-reader-preview.css';
import './learning/reader.css';
import { Eyebrow } from './learning/shared';
import './learning/sidebar-directions.css';
import BackButton from './ui/BackButton';
import { ALL_COURSES } from '../courseData';
import { useCompactLayout } from '../hooks/useCompactLayout';
import { moduleOutcome,moduleReadingTime } from '../utils/moduleDiscovery';
import { ModuleFinishContext,ReaderStepContext } from './learning/readerContext';
import { clearModuleResumeRequest,requestedModuleResume } from './learning/intents';
import './learning/module-reader.css';
import { MODULE_WORLDS,Readout,WorldArt,worldStyle } from './moduleWorlds';
import { PinnedFooter,TopBar } from './ui/Bars';
import { Button as UiButton,Glyph,IconButton } from './ui/Button';
import { Switch } from './ui/Choice';
import { useFrameTask } from './ui/Frame';
import { List,PaperSheet,Row } from './ui/List';
import { Sheet } from './ui/Sheet';

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
  const essentials = useEssentialsMode();
  const readingMode = essentials ? 'essentials' : 'full';
  const requestedSection = useRef(requestedModuleSection(moduleId));
  const previousMode = useRef(readingMode);
  const focusRequested = useRef(false);
  const modulePosition = useModulePosition();
  const displayedModuleNumber = modulePosition?.displayNumber ?? moduleNumber;
  const [activeSection, setActiveSection] = useState(
    Math.max(0, Math.min(requestedSection.current ?? resumeSection(progress, sections, readingMode), sections.length - 1))
  );
  // A phone opens a module on its title page, unless the student came to pick up where they left
  // off (a continue action, Home's continue card) or to a particular section (board c-read-flow).
  const phone = useCompactLayout();
  const resumeRequested = useRef(requestedModuleResume(moduleId));
  const [onCover, setOnCover] = useState(() => phone && requestedSection.current === undefined && !resumeRequested.current);
  const finish = React.useContext(ModuleFinishContext);
  const [desktopSidebarOpen, setDesktopSidebarOpen] = useState(true);
  const [mobileSectionsOpen, setMobileSectionsOpen] = useState(false);
  const [referencesOpen, setReferencesOpen] = useState(false);
  const [notesOpen, setNotesOpen] = useState(false);
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
    clearModuleResumeRequest(moduleId);
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
      setShowCelebration(true);
    } else if (nextIndex >= 0) {
      focusRequested.current = true;
      setActiveSection(nextIndex);
    } else {
      onBack();
    }
    setTimeout(() => { isCompletingRef.current = false; }, 500);
  };

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
          className="w-8 h-8 rounded-lg border border-zinc-200 dark:border-zinc-700 text-xs font-bold text-zinc-600 dark:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-surface-soft disabled:opacity-30"
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
          className="w-8 h-8 rounded-lg border border-zinc-200 dark:border-zinc-700 text-sm font-bold text-zinc-600 dark:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-surface-soft disabled:opacity-30"
        >
          A+
        </button>
        <button
          onClick={() => settingsCtx.updateSetting('readingSpacing', readingRelaxed ? 'normal' : 'relaxed')}
          className={`flex-1 min-h-[32px] px-1.5 py-1 leading-tight rounded-lg border text-[11px] font-semibold transition-colors ${readingRelaxed ? 'border-[var(--accent-hex)] text-[var(--accent-hex)] bg-[rgba(var(--accent),0.08)]' : 'border-zinc-200 dark:border-zinc-700 text-zinc-600 dark:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-surface-soft'}`}
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
  if (phone) return (
    <PhoneReader
      moduleId={moduleId} moduleTitle={moduleTitle} moduleSubtitle={moduleSubtitle} displayedModuleNumber={displayedModuleNumber}
      sections={sections} activeSection={activeSection} readIds={readIds} onCover={onCover} setOnCover={setOnCover}
      onBack={onBack} onJump={handleJumpToSection} onComplete={handleCompleteSection} finishButtonText={finishButtonText}
      references={references} readingScale={readingScale} readingRelaxed={readingRelaxed}
      mainRef={mainRef} reducedMotion={!!reducedMotion}
      contentsOpen={mobileSectionsOpen} setContentsOpen={setMobileSectionsOpen}
      notesOpen={notesOpen} setNotesOpen={setNotesOpen} comfortOpen={pickerOpen} setComfortOpen={setPickerOpen}
      referencesOpen={referencesOpen} setReferencesOpen={setReferencesOpen}
      comfort={settingsCtx ? <ReadingComfort scale={readingScale} relaxed={readingRelaxed} onStep={stepReadingScale}
        onRelaxed={value => settingsCtx.updateSetting('readingSpacing', value ? 'relaxed' : 'normal')}
        dark={settingsCtx.settings.darkMode} onDark={() => settingsCtx.updateSetting('darkMode', !settingsCtx.settings.darkMode)} /> : null}
      content={moduleResponses.isLoaded ? children(activeSection) : <p role="status">Loading your saved drafts…</p>}
      saveStatus={<ResponseSaveStatus status={moduleResponses.saveStatus} onRetry={moduleResponses.retrySave} />}
      commandMenu={<CommandMenu placeholder="Find a section…" actions={sections.map((section, index) => ({ id: section.id, label: section.title, hint: readIds.has(section.id) ? 'Read · Revisit anytime' : 'Open section', keywords: [section.eyebrow], icon: <CompletionMark number={index + 1} complete={readIds.has(section.id)} current={index === activeSection} />, action: () => handleJumpToSection(index) }))} />}
      complete={<ModuleCompleteScreen isOpen={showCelebration} moduleTitle={moduleTitle} moduleSubtitle={moduleSubtitle} categoryColor={categoryColor || COLORS.accent} modulesCompleted={modulesCompleted} totalModules={totalModules} sectionsCount={sections.length} sections={sections} finish={finish} northStarStatement={northStarStatement} onContinue={handleCelebrationContinue} onPractice={() => { setShowCelebration(false); navigation.navigateToStudySession(); }} onReview={() => { setShowCelebration(false); setOnCover(false); setActiveSection(0); }} />}
    />
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
      <ModuleCompleteScreen isOpen={showCelebration} moduleTitle={moduleTitle} moduleSubtitle={moduleSubtitle} categoryColor={categoryColor || COLORS.accent} modulesCompleted={modulesCompleted} totalModules={totalModules} sectionsCount={sections.length} northStarStatement={northStarStatement} onContinue={handleCelebrationContinue} onPractice={() => { setShowCelebration(false); navigation.navigateToStudySession(); }} onReview={() => { setShowCelebration(false); setActiveSection(0); }} />
    </KobraScope>
  );
};

/* ── Reading a module on a phone (area 5 of the design build; board c-read-flow) ───────────────────
   The page itself is the paper and each step is its own screen: one bar (Back, the steps, Contents,
   Notes), the step's number, headline and Thinker, its words on the white page, and one charcoal
   Continue at the foot that names the next step. Contents, Notes and the reading comfort rise from
   the bottom. A module opens on its title page; Continue reading picks up at the student's step. */

interface PhoneReaderProps {
  moduleId: string; moduleTitle: string; moduleSubtitle?: string; displayedModuleNumber: string;
  sections: SectionDefinition[]; activeSection: number; readIds: Set<string>;
  onCover: boolean; setOnCover: (value: boolean) => void;
  onBack: () => void; onJump: (index: number) => void; onComplete: () => void; finishButtonText: string;
  references?: Reference[]; readingScale: number; readingRelaxed: boolean;
  mainRef: React.RefObject<HTMLElement | null>; reducedMotion: boolean;
  contentsOpen: boolean; setContentsOpen: (open: boolean) => void;
  notesOpen: boolean; setNotesOpen: (open: boolean) => void;
  comfortOpen: boolean; setComfortOpen: (open: boolean) => void;
  referencesOpen: boolean; setReferencesOpen: (open: boolean) => void;
  comfort: React.ReactNode; content: React.ReactNode; saveStatus: React.ReactNode; commandMenu: React.ReactNode; complete: React.ReactNode;
}

const pad2 = (n: number) => String(n).padStart(2, '0');
/** A section's own name after its number ("04 // Retraining" is "Retraining"). */
const sectionName = (eyebrow?: string) => (eyebrow?.includes('//') ? eyebrow.split('//').slice(1).join('//').trim() : '');

/** The steps in the bar: read ones in ink, the one you are on filling as you scroll, the rest the track. */
function ReaderTrack({ sections, activeSection, readIds, live }: { sections: SectionDefinition[]; activeSection: number; readIds: Set<string>; live: boolean }) {
  const ref = useRef<HTMLSpanElement>(null);
  useEffect(() => {
    if (!live) return undefined;
    const update = () => {
      const max = document.documentElement.scrollHeight - window.innerHeight;
      ref.current?.style.setProperty('--p', `${Math.round(Math.min(1, Math.max(0, max > 0 ? window.scrollY / max : 1)) * 100)}%`);
    };
    update();
    window.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
    return () => { window.removeEventListener('scroll', update); window.removeEventListener('resize', update); };
  }, [live, activeSection]);
  return (
    <span ref={ref} className="rd-track" aria-hidden="true">
      {sections.map((section, index) => <i key={section.id} className={index === activeSection && live ? 'is-cur' : readIds.has(section.id) ? 'is-on' : undefined} />)}
    </span>
  );
}

/** Text size and spacing (today's reading comfort), on the system's controls. */
function ReadingComfort({ scale, relaxed, onStep, onRelaxed, dark, onDark }: { scale: number; relaxed: boolean; onStep: (dir: 1 | -1) => void; onRelaxed: (value: boolean) => void; dark: boolean; onDark: () => void }) {
  return (
    <div className="rd-comfort">
      <div className="rd-comfort-row">
        <span className="t-body">Text size</span>
        <span className="rd-comfort-size">
          <UiButton size="sm" aria-label="Smaller text" onClick={() => onStep(-1)}>A−</UiButton>
          <Readout className="rd-comfort-pct">{Math.round(scale * 100)}%</Readout>
          <UiButton size="sm" aria-label="Larger text" onClick={() => onStep(1)}>A+</UiButton>
        </span>
      </div>
      <div className="rd-comfort-row"><span className="t-body" id="rd-relaxed">Relaxed spacing</span><Switch checked={relaxed} onChange={onRelaxed} aria-labelledby="rd-relaxed" /></div>
      <UiButton block onClick={onDark}>{dark ? <Sun className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" /> : <Moon className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" />}{dark ? 'Light mode' : 'Dark mode'}</UiButton>
    </div>
  );
}

function stepMeta(index: number, read: boolean, current: string | null) {
  return <>Step {index + 1}{current ? <> · <span className="rd-live">{current}</span></> : read ? ' · Read' : ' · Not read yet'}</>;
}

function PhoneReader(props: PhoneReaderProps) {
  const { moduleId, moduleTitle, moduleSubtitle, displayedModuleNumber, sections, activeSection, readIds, onCover, setOnCover, onBack, onJump, onComplete, finishButtonText,
    references, readingScale, readingRelaxed, mainRef, reducedMotion, contentsOpen, setContentsOpen, notesOpen, setNotesOpen, comfortOpen, setComfortOpen,
    referencesOpen, setReferencesOpen, comfort, content, saveStatus, commandMenu, complete } = props;
  const settings = useSettingsContext();
  const dark = settings?.settings.darkMode ?? false;
  const course = ALL_COURSES.find(item => item.id === moduleId);
  const world = MODULE_WORLDS.find(item => item.id === course?.category);
  const worldLabel = `${world ? `${world.name} · ` : ''}Module ${displayedModuleNumber}`;
  const total = sections.length;
  const read = readIds.size;
  const last = activeSection === total - 1;
  const next = sections[activeSection + 1];
  useFrameTask(true);
  useLayoutEffect(() => { window.scrollTo({ top: 0 }); }, [onCover]);

  const bar = (
    <TopBar className="rd-bar" data-student-page-header leave={{ kind: 'back', onPress: onBack, label: 'Back to modules' }}
      center={<ReaderTrack sections={sections} activeSection={activeSection} readIds={readIds} live={!onCover} />}
      action={<span className="rd-tools">
        <IconButton label="Contents" icon={<Glyph icon={ListOrdered} />} onClick={() => setContentsOpen(true)} />
        <IconButton label="Notes" icon={<BrandBook size={26} />} onClick={() => setNotesOpen(true)} />
      </span>} />
  );

  const stepRows = (current: (index: number) => string | null, close?: () => void) => (
    <List className="rd-steps">
      {sections.map((section, index) => {
        const isRead = readIds.has(section.id);
        const now = current(index);
        return (
          <Row key={section.id} icon={<CompletionMark number={index + 1} complete={isRead} current={index === activeSection} />}
            title={section.title} meta={stepMeta(index, isRead, now)}
            label={`${section.title}. ${now ?? (isRead ? 'Read · Revisit anytime' : 'Open section')}`}
            onPress={() => { close?.(); onJump(index); setOnCover(false); }} />
        );
      })}
    </List>
  );

  const resumeAt = sections[activeSection];
  const page = onCover ? (
    <main className="rd-cover" ref={mainRef as React.RefObject<HTMLElement>}>
      <section className="rd-covertop">
        <PaperSheet className="rd-coversheet" label={moduleTitle}>
          <div className="rd-cover-in" style={world ? worldStyle(world, dark) : undefined}>
            {world ? <WorldArt world={world} size={88} className="rd-cover-art" /> : null}
            <p className="t-label mw-w-ink">{worldLabel}</p>
            <h1 className="t-display rd-cover-title" tabIndex={-1}>{moduleTitle}</h1>
            {moduleSubtitle ? <p className="t-sub">{moduleSubtitle}</p> : null}
            {course ? <>
              <hr className="mw-rule rd-cover-rule" />
              <p className="t-label rd-cover-label">What you’ll get</p>
              <p className="t-body">{moduleOutcome(course)}</p>
              <p className="t-meta rd-facts"><span><Clock className="ui-icon" width={15} height={15} strokeWidth={2} aria-hidden="true" />{moduleReadingTime(course, settings?.settings.essentialsMode).replace(/ reading$/, '')}</span><span>{total} steps</span></p>
            </> : null}
          </div>
        </PaperSheet>
      </section>
      <section className="rd-sec" aria-labelledby="rd-in-this">
        <div className="mw-sec-head"><h2 id="rd-in-this" className="t-heading">In this module</h2><Readout className="mw-ink3">{read} / {total} read</Readout></div>
        {stepRows(index => (index === activeSection && read < total ? 'Up next' : null))}
      </section>
    </main>
  ) : (
    <main className="rd-step" ref={mainRef as React.RefObject<HTMLElement>}>
      <ReaderStepContext.Provider value={{ index: activeSection, total, name: sectionName(sections[activeSection]?.eyebrow) }}>
        <ModuleReferencesProvider value={references ?? []}>
          <AnimatePresence mode="wait" initial={false}><motion.div key={sections[activeSection]?.id ?? activeSection} initial={{ opacity: 0, y: reducedMotion ? 0 : 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} transition={{ duration: reducedMotion ? 0 : .22 }} className="mr-page-content rd-page">
            {content}
            <div className="rd-save">{saveStatus}</div>
            <div className="mr-page-signoff rd-signoff"><span>A little further than before.</span><Readout className="mw-ink3">{pad2(activeSection + 1)}</Readout></div>
          </motion.div></AnimatePresence>
        </ModuleReferencesProvider>
      </ReaderStepContext.Provider>
    </main>
  );

  const foot = onCover ? (
    <PinnedFooter ruled lead={read > 0 && resumeAt ? `You stopped at step ${activeSection + 1}, ${resumeAt.title}.` : undefined}>
      <UiButton kind="main" size="lg" block arrow="forward" onClick={() => setOnCover(false)}>{read > 0 ? 'Continue reading' : 'Start reading'}</UiButton>
    </PinnedFooter>
  ) : (
    <PinnedFooter ruled lead={next ? <>Next: <span className="rd-next">{next.title}</span></> : 'Your last page. Yours to revisit.'}>
      <UiButton kind="main" size="lg" block arrow="forward" onClick={onComplete} aria-label={last ? finishButtonText : 'Continue to the next section'}>{last ? finishButtonText : 'Continue'}</UiButton>
    </PinnedFooter>
  );

  return (
    <KobraScope className="nsu-learning nsu-module-reader theme-compat rd-reader rd-reader--phone">
      <div className="rd-main" data-cover={onCover || undefined} style={{ ['--reading-scale' as string]: String(readingScale), ['--reading-lh' as string]: readingRelaxed ? '1.95' : '1.65' }}>
        {bar}
        {page}
        {foot}
      </div>
      <Sheet open={contentsOpen} onClose={() => setContentsOpen(false)} title="Contents" titleSize="small" titleAlign="start" className="rd-sheet rd-contents">
        <div className="rd-nb" style={world ? worldStyle(world, dark) : undefined}>
          <BrandBook size={40} />
          <div className="rd-nb-copy"><p className="t-label mw-w-ink">{worldLabel}</p><p className="t-heading rd-nb-title">{moduleTitle}</p></div>
        </div>
        <ReadingProgress done={read} total={total} />
        <nav className="mr-progress-list" aria-label="Module sections">{stepRows(index => (index === activeSection && !onCover ? 'You’re here' : null), () => setContentsOpen(false))}</nav>
        <List className="rd-more">
          {references?.length ? <Row title="Sources and further reading" meta={`${references.length} ${references.length === 1 ? 'source' : 'sources'}`} onPress={() => { setContentsOpen(false); setReferencesOpen(true); }} /> : null}
          {comfort ? <Row title="Text size and spacing" meta={`${Math.round(readingScale * 100)}% · ${readingRelaxed ? 'Relaxed' : 'Normal'} spacing`} onPress={() => { setContentsOpen(false); setComfortOpen(true); }} /> : null}
          <Row title="Find a section" onPress={() => { setContentsOpen(false); openCommandMenu(); }} />
        </List>
      </Sheet>
      {comfort ? <Sheet open={comfortOpen} onClose={() => setComfortOpen(false)} title="Text size and spacing" titleSize="small" titleAlign="start" className="rd-sheet">{comfort}</Sheet> : null}
      <Toasts position="bottom-center" />
      {notesOpen && <ReaderNotes moduleId={moduleId} title={moduleTitle} sectionTitle={sections[activeSection]?.title ?? moduleTitle} sectionIndex={activeSection} open={notesOpen} onClose={() => setNotesOpen(false)} />}
      {commandMenu}
      {!!references?.length && <ReferencesModal open={referencesOpen} onClose={() => setReferencesOpen(false)} references={references} />}
      {complete}
    </KobraScope>
  );
}
