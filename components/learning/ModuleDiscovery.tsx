/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Finding a module from the Modules page (area 5 of the design build): search
 * every module and section, a starting point by what you need, and your
 * notebook. Each is a piece the Modules page lays out its own way: on a phone
 * search sits behind the bar's search button and the starting points rise in
 * a sheet (board c-modules-pick); on a laptop search is a field in the bar and
 * the starting points open a menu (board r5-modules, ROUND5-RESULTS "c1").
 * Behaviour is today's: the same results, routes, saved ideas and links.
 */
import { useState } from 'react';
import type { CourseData } from '../Library';
import type { UserProgress } from '../../types';
import { useAuth } from '../../contexts/AuthContext';
import { useSettingsContext } from '../../contexts/SettingsContext';
import { useModuleResponses } from '../../hooks/useModuleResponses';
import { moduleAvailability } from '../../utils/courseVisibility';
import { directResumeCourse, MODULE_ENTRY_ROUTES, moduleOutcome, moduleReadingTime, searchModuleSections } from '../../utils/moduleDiscovery';
import { LEARNING_NOTEBOOK_NAMESPACE, notebookEntry } from '../../utils/learningNotebook';
import { requestModuleSection } from './data';
import { IconButton, TextButton, Glyph } from '../ui/Button';
import { List, Row } from '../ui/List';
import { Sheet } from '../ui/Sheet';
import { X } from 'lucide-react';
import './module-discovery.css';

export function ModuleOutcome({ course }: { course: CourseData }) {
  const settings = useSettingsContext();
  return <div className="module-outcome"><p>{moduleOutcome(course)}</p><small>{moduleReadingTime(course, settings?.settings.essentialsMode)} · Activities are optional and take extra time.</small></div>;
}

/** What the Modules page needs to find a module: the student's available modules, the one to pick up, and the routes. */
export function useModuleDiscovery(courses: CourseData[], progress: UserProgress) {
  const { user } = useAuth();
  const available = courses.filter(course => moduleAvailability(course, user?.curriculumLevel, null) === 'available');
  const resume = directResumeCourse(available, progress);
  const routes = MODULE_ENTRY_ROUTES.map(route => ({
    ...route,
    courses: route.moduleIds.map(id => available.find(course => course.id === id)).filter((course): course is CourseData => !!course),
  })).filter(route => route.courses.length);
  return { available, resume, routes };
}
export type DiscoveryRoute = ReturnType<typeof useModuleDiscovery>['routes'][number];

/** Open a section directly, in the reading mode it was saved in. */
function useOpenSection(onOpen: (id: string) => void) {
  const settings = useSettingsContext();
  return (id: string, index: number, essentials = false) => {
    settings?.updateSetting('essentialsMode', essentials);
    requestModuleSection(id, index);
    onOpen(id);
  };
}

/** Search results for every module and section: today's results, in rows. */
export function ModuleSearchResults({ courses, query, onOpen }: { courses: CourseData[]; query: string; onOpen: (id: string) => void }) {
  const openSection = useOpenSection(onOpen);
  if (!query.trim()) return null;
  const results = searchModuleSections(courses, query);
  return (
    <div className="module-search-results">
      <p role="status" className="t-meta">{results.length} matching {results.length === 1 ? 'module' : 'modules'}{!results.length ? '. Try a different phrase or browse below.' : ''}</p>
      {results.map(({ course, sections }) => (
        <article key={course.id} className="module-search-hit">
          <List>
            <Row title={course.title} meta={moduleOutcome(course)} onPress={() => onOpen(course.id)} />
          </List>
          {!!sections.length && <ul className="module-search-sections">{sections.map(section => (
            <li key={section.index}><TextButton arrow="forward" onClick={() => openSection(course.id, section.index)}>Open full section: {section.title}</TextButton></li>
          ))}</ul>}
        </article>
      ))}
    </div>
  );
}

/** A starting point's three lessons, as rows. */
export function RouteLessons({ route, onOpen }: { route: DiscoveryRoute; onOpen: (id: string) => void }) {
  const settings = useSettingsContext();
  return (
    <List className="module-route-rows">
      {route.courses.map(course => (
        <Row key={course.id} title={course.title} meta={`${moduleOutcome(course)} · ${moduleReadingTime(course, settings?.settings.essentialsMode)}`} onPress={() => onOpen(course.id)} />
      ))}
    </List>
  );
}

/** The starting points on a phone: a sheet of the six needs, each opening its three lessons in place. */
export function StartingPointsSheet({ open, onClose, routes, onOpen }: { open: boolean; onClose: () => void; routes: DiscoveryRoute[]; onOpen: (id: string) => void }) {
  const [openRoute, setOpenRoute] = useState<string | null>(null);
  return (
    <Sheet open={open} onClose={onClose} title="Find a starting point" titleSize="small" className="module-start-sheet">
      <p className="t-sub module-start-lede">What would help? Each one leads to three short lessons.</p>
      <List>
        {routes.map(route => {
          const expanded = openRoute === route.id;
          return (
            <li key={route.id} className="ui-row-item module-start-need">
              <ul className="module-start-need-list">
                <Row title={route.title} meta={route.description} expanded={expanded} onPress={() => setOpenRoute(expanded ? null : route.id)} />
              </ul>
              {expanded ? (
                <List className="module-start-lessons">
                  {route.courses.map(course => <Row key={course.id} title={course.title} onPress={() => { onClose(); onOpen(course.id); }} />)}
                </List>
              ) : null}
            </li>
          );
        })}
      </List>
    </Sheet>
  );
}

/** A chosen starting point's lessons on the page (the laptop's menu applies at once and shows them here). */
export function ChosenRoute({ route, onClear, onOpen }: { route: DiscoveryRoute; onClear: () => void; onOpen: (id: string) => void }) {
  return (
    <section className="module-route-lessons" aria-label={route.title}>
      <div className="module-route-head">
        <h2 className="t-heading">{route.title}</h2>
        <IconButton label="Clear starting point" icon={<Glyph icon={X} size={20} />} onClick={onClear} />
      </div>
      <RouteLessons route={route} onOpen={onOpen} />
    </section>
  );
}

/** Your notebook: private notes and the ideas you chose to keep, each a way back to its lesson. */
export function NotebookResults({ courses, query = '', onOpen }: { courses: CourseData[]; query?: string; onOpen: (id: string) => void }) {
  const notebook = useModuleResponses(LEARNING_NOTEBOOK_NAMESPACE);
  const openSection = useOpenSection(onOpen);
  const q = query.trim().toLowerCase();
  const saved = courses.flatMap(course => {
    const entry = notebookEntry(notebook.responses[course.id], course.title);
    return entry.takeaways.map(takeaway => ({ course, takeaway }))
      .filter(item => !q || `${item.course.title} ${item.takeaway.sectionTitle} ${item.takeaway.text}`.toLowerCase().includes(q));
  });
  const notes = courses.map(course => ({ course, entry: notebookEntry(notebook.responses[course.id], course.title) }))
    .filter(({ entry }) => entry.notes && (!q || `${entry.title} ${entry.notes}`.toLowerCase().includes(q)));
  return (
    <div className="module-notebook-results">
      <p className="t-sub">Private notes and ideas you chose to keep.</p>
      {!notebook.isLoaded ? <p role="status" className="t-meta">Loading your notebook…</p>
        : !saved.length && !notes.length ? <p className="t-body">Save an idea or write a note from the Notes button in any lesson.</p>
        : <div className="module-notebook-list">
          {saved.map(({ course, takeaway }) => (
            <article key={takeaway.id} className="module-notebook-item">
              <p className="t-meta">{course.title} · {takeaway.sectionTitle}</p>
              <p className="t-body">{takeaway.text}</p>
              <TextButton arrow="forward" onClick={() => openSection(course.id, takeaway.sectionIndex, takeaway.mode === 'essentials')}>Return to this section</TextButton>
            </article>
          ))}
          {notes.map(({ course, entry }) => (
            <article key={course.id} className="module-notebook-item">
              <h3 className="t-row">{course.title}</h3>
              <p className="t-body module-notebook-text">{entry.notes}</p>
              <TextButton arrow="forward" onClick={() => onOpen(course.id)}>Open lesson</TextButton>
            </article>
          ))}
        </div>}
    </div>
  );
}

/** The notebook as a sheet over Modules (phone and laptop). */
export function NotebookSheet({ open, onClose, courses, onOpen }: { open: boolean; onClose: () => void; courses: CourseData[]; onOpen: (id: string) => void }) {
  return (
    <Sheet open={open} onClose={onClose} title="Your notebook" titleSize="small" className="module-notebook-sheet">
      <NotebookResults courses={courses} onOpen={id => { onClose(); onOpen(id); }} />
    </Sheet>
  );
}
