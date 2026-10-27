/**
 * The ⌘K palette, rebuilt on Kobra (review section 06).
 *
 * The same entries as components/CommandPalette.tsx (its pages list, its
 * exported TOOL_TITLES and every module a student without a subject profile
 * can open), handed to the runtime CommandMenu: pages and tools show when the
 * box is empty, modules only once you type (CommandMenu's `hidden`), and the
 * PAGE / TOOL / MODULE chips become the menu's group headings. The
 * nsu:command-palette event becomes openCommandMenu(), so one palette answers
 * ⌘K everywhere, modules included.
 *
 * The runtime menu is a fixed full-screen layer. Here it is held inside the
 * pane: the stage is a containing block (transform), and while this in-pane
 * menu is open the review page keeps scrolling (the menu's body scroll lock is
 * released by one scoped rule in command-palette.css). It opens by itself the
 * first time the pane is in view and closes when it scrolls away; the Button
 * reopens it, as does ⌘K. Choosing an entry only says what would open.
 */
import { useEffect, useMemo, useRef, type ReactNode } from 'react';
import { Search } from 'lucide-react';
import { Button, CommandMenu, Kbd, openCommandMenu, toast } from '../../components/approved-ui-runtime';
import { TOOL_TITLES } from '../../components/CommandPalette';
import { ALL_COURSES } from '../../courseData';
import { filterCoursesForStudent } from '../../utils/courseVisibility';
import './command-palette.css';

type Kind = 'Page' | 'Tool' | 'Module';
interface Entry { kind: Kind; id: string; title: string; detail?: string }

/** CommandPalette.tsx's pages, in its order, with its details. */
const PAGES: Entry[] = [
  { kind: 'Page', id: 'home', title: 'Home' },
  { kind: 'Page', id: 'modules', title: 'Modules', detail: 'The Programme' },
  { kind: 'Page', id: 'launchpad', title: 'Launchpad', detail: 'All exam tools' },
  { kind: 'Page', id: 'dashboard', title: 'My Progress' },
  { kind: 'Page', id: 'learning-paths', title: 'Learning Paths' },
  { kind: 'Page', id: 'my-journey', title: 'My Journey' },
  { kind: 'Page', id: 'study-session', title: 'Study Session' },
  { kind: 'Page', id: 'insights', title: 'Insights' },
  { kind: 'Page', id: 'accreditation', title: 'References' },
  { kind: 'Page', id: 'year-plans', title: 'Year Plans' },
];

export default function CommandPaletteAfter() {
  const stageRef = useRef<HTMLDivElement>(null);

  const actions = useMemo(() => {
    const tools: Entry[] = Object.entries(TOOL_TITLES).map(([id, title]) => ({ kind: 'Tool', id, title, detail: 'Launchpad' }));
    const modules: Entry[] = filterCoursesForStudent(ALL_COURSES, undefined, null)
      .map(course => ({ kind: 'Module', id: course.id, title: course.title, detail: course.subtitle }));
    return [...PAGES, ...tools, ...modules].map(entry => ({
      id: `${entry.kind.toLowerCase()}:${entry.id}`,
      label: entry.title,
      group: entry.kind,
      hint: entry.detail,
      hidden: entry.kind === 'Module',
      action: () => { toast({ message: `${entry.title} would open here.` }); },
    }));
  }, []);

  // Open in the pane the first time it is in view; close when it scrolls away
  // (its focus trap would otherwise hold Tab on the rest of the review page).
  useEffect(() => {
    const stage = stageRef.current;
    if (!stage) return;
    const isOpen = () => Boolean(stage.querySelector('.command-overlay'));
    let dismissed = false;
    let closingForScroll = false;
    const watch = new MutationObserver(() => {
      if (isOpen()) return;
      if (!closingForScroll) dismissed = true;
      closingForScroll = false;
    });
    watch.observe(stage, { childList: true, subtree: true });
    const view = new IntersectionObserver(([entry]) => {
      if (!entry) return;
      if (entry.intersectionRatio >= 0.6 && !dismissed && !isOpen()) openCommandMenu();
      else if (entry.intersectionRatio < 0.2 && isOpen()) {
        closingForScroll = true;
        window.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
      }
    }, { threshold: [0, 0.2, 0.6] });
    view.observe(stage);
    return () => { watch.disconnect(); view.disconnect(); };
  }, []);

  const hint: ReactNode = <><b>↑↓</b> to choose · <b>Enter</b> to go · <b>⌘K</b> anytime</>;

  return (
    <section className="kr-section kr-cp" aria-label="Command palette on Kobra">
      <div className="kr-cp-stage" ref={stageRef}>
        <div className="kr-cp-rest">
          <Button variant="outline" className="nsu-ink-outline kr-cp-trigger" onClick={() => openCommandMenu()}>
            <Search aria-hidden="true" />
            <span className="kr-cp-trigger-label">Jump to any module, tool or page</span>
            <Kbd className="kr-cp-kbd">⌘ K</Kbd>
          </Button>
          <p className="kr-cp-hint">{hint}</p>
        </div>
        <CommandMenu placeholder="Jump to a module, tool or page…" actions={actions} />
      </div>
    </section>
  );
}
