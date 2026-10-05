import { useEffect, useId, useState } from 'react';
import { ArrowRight, BookOpen, ChevronDown, Search, X } from 'lucide-react';
import type { CourseData } from '../Library';
import type { UserProgress } from '../../types';
import { useAuth } from '../../contexts/AuthContext';
import { useSettingsContext } from '../../contexts/SettingsContext';
import { useModuleResponses } from '../../hooks/useModuleResponses';
import KobraScope, { Button, Input, Popover, PopoverContent, PopoverTrigger, Tabs, TabsList, TabsTrigger } from '../approved-ui-runtime';
import { moduleAvailability } from '../../utils/courseVisibility';
import { directResumeCourse, MODULE_ENTRY_ROUTES, moduleOutcome, moduleReadingTime, searchModuleSections } from '../../utils/moduleDiscovery';
import { LEARNING_NOTEBOOK_NAMESPACE, notebookEntry } from '../../utils/learningNotebook';
import { requestModuleSection } from './data';
import './module-discovery.css';

export function ModuleOutcome({ course }: { course: CourseData }) {
  const settings = useSettingsContext();
  return <div className="module-outcome"><p>{moduleOutcome(course)}</p><small>{moduleReadingTime(course, settings?.settings.essentialsMode)} · Activities are optional and take extra time.</small></div>;
}

type DiscoveryDirection = 'toolbar' | 'rail' | 'list';
function entryRoutesPreview() {
  try { return import.meta.env.DEV && window.frameElement?.getAttribute('data-module-routes-preview') === 'true'; }
  catch { return false; }
}
function initialDirection(): DiscoveryDirection {
  try {
    const direction = window.frameElement?.getAttribute('data-module-discovery-direction');
    if (direction === 'rail' || direction === 'list') return direction;
  } catch { /* Normal app surface uses the compact toolbar. */ }
  return 'list';
}
const ROUTE_LABELS: Record<string, { short: string; label: string }> = {
  remember: { short: 'Remember', label: 'Remember what I study' },
  start: { short: 'Get started', label: 'Get started with study' },
  understand: { short: 'Understand', label: 'Understand a difficult topic' },
  exam: { short: 'Exam prep', label: 'Prepare for an exam' },
  worry: { short: 'Pressure', label: 'Handle exam pressure' },
  direction: { short: 'Direction', label: 'Find something to aim for' },
};

export function ModuleDiscovery({ courses, progress, onOpen }: { courses: CourseData[]; progress: UserProgress; onOpen: (id: string) => void }) {
  const { user } = useAuth();
  const settings = useSettingsContext();
  const [query, setQuery] = useState('');
  const [routeId, setRouteId] = useState<string | null>(null);
  const [showNotebook, setShowNotebook] = useState(false);
  const [pickerOpen, setPickerOpen] = useState(false);
  const [indexOpen, setIndexOpen] = useState(false);
  const indexId = useId();
  const [direction, setDirection] = useState<DiscoveryDirection>(initialDirection);
  const preview = entryRoutesPreview();
  const notebook = useModuleResponses(LEARNING_NOTEBOOK_NAMESPACE);
  const available = courses.filter(course => moduleAvailability(course, user?.curriculumLevel, null) === 'available');
  const resume = directResumeCourse(available, progress);
  const results = searchModuleSections(available, query);
  const routes = MODULE_ENTRY_ROUTES.map(route => ({
    ...route,
    courses: route.moduleIds.map(id => available.find(course => course.id === id)).filter((course): course is CourseData => !!course),
  })).filter(route => route.courses.length);
  const selectedRoute = routes.find(route => route.id === routeId);

  // The comparison controls live outside the product iframe, exclusively in
  // the local review page. They never become another product settings panel.
  useEffect(() => {
    if (!preview) return;
    const review = (event: Event) => {
      const detail = (event as CustomEvent<{ direction?: string; theme?: string }>).detail;
      if (detail?.direction === 'toolbar' || detail?.direction === 'rail' || detail?.direction === 'list') {
        setDirection(detail.direction);
        setRouteId(null);
        setPickerOpen(false);
        setIndexOpen(false);
      }
      if (detail?.theme === 'dark' || detail?.theme === 'light') settings?.updateSetting('darkMode', detail.theme === 'dark');
    };
    window.addEventListener('nextstepuni:module-design-review', review);
    return () => window.removeEventListener('nextstepuni:module-design-review', review);
  }, [preview, settings]);

  const openSection = (id: string, index: number, essentials = false) => {
    settings?.updateSetting('essentialsMode', essentials);
    requestModuleSection(id, index);
    onOpen(id);
  };
  const chooseRoute = (id: string) => {
    setRouteId(routeId === id ? null : id);
    setPickerOpen(false);
    setIndexOpen(false);
    setShowNotebook(false);
  };
  const saved = available.flatMap(course => {
    const entry = notebookEntry(notebook.responses[course.id], course.title);
    return entry.takeaways.map(takeaway => ({ course, takeaway }))
      .filter(item => !query.trim() || `${item.course.title} ${item.takeaway.sectionTitle} ${item.takeaway.text}`.toLowerCase().includes(query.trim().toLowerCase()));
  });
  const notes = available.map(course => ({ course, entry: notebookEntry(notebook.responses[course.id], course.title) }))
    .filter(({ entry }) => entry.notes && (!query.trim() || `${entry.title} ${entry.notes}`.toLowerCase().includes(query.trim().toLowerCase())));
  const resumeProgress = resume ? progress[resume.id] : undefined;
  const resumeIndex = resumeProgress?.reading?.lastSectionIndex ?? resumeProgress?.unlockedSection ?? 0;

  return <KobraScope className="module-discovery">
    <section aria-label="Find your next module" data-discovery-direction={direction}>
      {resume && <div className="module-resume">
        <span className="module-resume-label">Continue</span>
        <Button variant="ghost" className="module-resume-link" aria-label={`Resume lesson: ${resume.title}`} onClick={() => {
          if (resumeProgress?.reading) settings?.updateSetting('essentialsMode', resumeProgress.reading.lastMode === 'essentials');
          onOpen(resume.id);
        }}><span>{resume.title}</span><ArrowRight aria-hidden="true" /></Button>
        <span className="module-resume-location">Section {resumeIndex + 1}{resumeProgress?.reading?.lastMode === 'essentials' ? ' · Essentials' : ''}</span>
      </div>}

      <div className="module-discovery-toolbar">
        <div className="module-discovery-search">
          <Search aria-hidden="true" />
          <Input type="search" aria-label="Search all your modules and sections" value={query} onChange={event => setQuery(event.target.value)} placeholder="Search modules and sections" />
        </div>
        <div className="module-discovery-actions">
          {preview && direction === 'toolbar' && <Popover open={pickerOpen} onOpenChange={setPickerOpen}>
            <PopoverTrigger render={<Button variant="ghost" className="module-route-trigger" />}>
              {selectedRoute ? ROUTE_LABELS[selectedRoute.id].short : 'Find a starting point'}<ChevronDown aria-hidden="true" />
            </PopoverTrigger>
            <PopoverContent className="module-route-picker" align="end" sideOffset={8} aria-label="Choose a starting point">
              <p className="module-route-picker-label">What would help?</p>
              <div className="module-route-picker-options">{routes.map(route => <Button variant="ghost" key={route.id} aria-pressed={route.id === routeId} onClick={() => chooseRoute(route.id)}>
                <span>{ROUTE_LABELS[route.id].label}</span><small>{route.courses.length} lessons</small>
              </Button>)}</div>
            </PopoverContent>
          </Popover>}
          {preview && direction === 'list' && <Button variant="ghost" className="module-route-trigger" aria-expanded={indexOpen} aria-controls={indexId} onClick={() => setIndexOpen(value => !value)}>
            {selectedRoute ? ROUTE_LABELS[selectedRoute.id].short : 'Find a starting point'}<ChevronDown aria-hidden="true" className={indexOpen ? 'module-index-chevron-open' : ''} />
          </Button>}
          <Button variant="ghost" aria-pressed={showNotebook} onClick={() => setShowNotebook(value => !value)}><BookOpen aria-hidden="true" />Notebook</Button>
        </div>
      </div>

      {preview && direction === 'rail' && <Tabs value={routeId ?? 'all'} onValueChange={value => { setRouteId(value === 'all' ? null : String(value)); setShowNotebook(false); }} className="module-topic-rail">
        <TabsList variant="line" aria-label="Choose a starting point">
          <TabsTrigger value="all">All modules</TabsTrigger>
          {routes.map(route => <TabsTrigger key={route.id} value={route.id}>{ROUTE_LABELS[route.id].short}</TabsTrigger>)}
        </TabsList>
      </Tabs>}

      {preview && direction === 'list' && indexOpen && <div className="module-route-index" id={indexId}>
        <p>Choose a focus</p>
        <div>{routes.map(route => <Button variant="ghost" key={route.id} aria-pressed={route.id === routeId} onClick={() => chooseRoute(route.id)}>
          <span>{ROUTE_LABELS[route.id].label}</span><ArrowRight aria-hidden="true" />
        </Button>)}</div>
      </div>}

      {selectedRoute && !query.trim() && !showNotebook && <div className="module-route-lessons">
        <div className="module-route-results-heading"><h2>{ROUTE_LABELS[selectedRoute.id].label}</h2><Button variant="ghost" size="icon" aria-label="Clear starting point" onClick={() => setRouteId(null)}><X aria-hidden="true" /></Button></div>
        <ol>{selectedRoute.courses.map(course => <li key={course.id}>
          <Button variant="ghost" className="module-lesson-row" onClick={() => onOpen(course.id)}>
            <span><strong>{course.title}</strong><span>{moduleOutcome(course)}</span></span>
            <small>{moduleReadingTime(course, settings?.settings.essentialsMode)}</small><ArrowRight aria-hidden="true" />
          </Button>
        </li>)}</ol>
      </div>}

      {query.trim() && <div className="module-search-results">
        <p role="status">{results.length} matching {results.length === 1 ? 'module' : 'modules'}{!results.length ? '. Try a different phrase or browse below.' : ''}</p>
        {results.map(({ course, sections }) => <article key={course.id}>
          <Button variant="ghost" className="module-search-title" onClick={() => onOpen(course.id)}>{course.title}<ArrowRight aria-hidden="true" /></Button>
          <ModuleOutcome course={course} />
          {!!sections.length && <ul>{sections.map(section => <li key={section.index}><Button variant="link" onClick={() => openSection(course.id, section.index)}>Open full section: {section.title}</Button></li>)}</ul>}
        </article>)}
      </div>}

      {showNotebook && <div className="module-notebook-results">
        <h2>Your notebook</h2><p>Private notes and ideas you chose to keep. Use the search above to find them.</p>
        {!notebook.isLoaded ? <p role="status">Loading your notebook…</p> : !saved.length && !notes.length ? <p>Save an idea or write a note from the Notes button in any lesson.</p> : <>
          {saved.map(({ course, takeaway }) => <article key={takeaway.id}><p className="module-discovery-kicker">{course.title} · {takeaway.sectionTitle}</p><p>{takeaway.text}</p><Button variant="link" onClick={() => openSection(course.id, takeaway.sectionIndex, takeaway.mode === 'essentials')}>Return to this section <ArrowRight aria-hidden="true" /></Button></article>)}
          {notes.map(({ course, entry }) => <article key={course.id}><h3>{course.title}</h3><p className="module-notebook-text">{entry.notes}</p><Button variant="link" onClick={() => onOpen(course.id)}>Open lesson <ArrowRight aria-hidden="true" /></Button></article>)}
        </>}
      </div>}
    </section>
  </KobraScope>;
}
