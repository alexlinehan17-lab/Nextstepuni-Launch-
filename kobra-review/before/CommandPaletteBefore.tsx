/**
 * "Now" pane for review section 06: the REAL components/CommandPalette.tsx,
 * opened as ⌘K opens it (its own `nsu:command-palette` event, via the
 * component's exported openCommandPalette), with its real entries: the ten
 * pages, the fifteen Launchpad tools and every module a student without a
 * subject profile can open (filterCoursesForStudent, as App.tsx passes them).
 * Navigation is a no-op NavigationContext, so choosing an entry only closes
 * the palette; ⌘K (Ctrl+K) opens it again.
 */
import React, { useEffect, useMemo } from 'react';
import CommandPalette, { openCommandPalette } from '../../components/CommandPalette';
import NavigationContext from '../../contexts/NavigationContext';
import { ALL_COURSES } from '../../courseData';
import { filterCoursesForStudent } from '../../utils/courseVisibility';

type NavigationValue = NonNullable<React.ContextType<typeof NavigationContext>>;

/** Every navigateTo… is a no-op; the palette reads nothing else. */
const NOOP_NAVIGATION = new Proxy({}, { get: () => () => {} }) as NavigationValue;

export default function CommandPaletteBefore() {
  const courses = useMemo(() => filterCoursesForStudent(ALL_COURSES, undefined, null), []);
  // The palette registers its listener in an effect, so open it after mount.
  useEffect(() => {
    const timer = window.setTimeout(openCommandPalette, 50);
    return () => window.clearTimeout(timer);
  }, []);
  return (
    <NavigationContext.Provider value={NOOP_NAVIGATION}>
      <CommandPalette courses={courses} />
    </NavigationContext.Provider>
  );
}
