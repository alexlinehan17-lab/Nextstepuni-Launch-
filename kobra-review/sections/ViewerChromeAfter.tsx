/**
 * Paper Trail viewer chrome, rebuilt on Kobra for the before/after review.
 *
 * The labels, tool names and their one-line descriptions are the live
 * viewer's (components/PaperTrail/Viewer.tsx). What changed against the
 * before: the option-E ink buttons with offset shadows are Kobra Buttons
 * (outline, and the default face for Answers), the hand-built Tools menu is a
 * Kobra DropdownMenu whose toggle rows each carry a Kobra Switch, the range
 * scrubber is a serif page count over a Kobra Progress with outline page
 * buttons, and the floating status pill is a Kobra toast.
 *
 * Physics Higher is the sample paper because it has both an official exam
 * clock (180 minutes) and a Formulae & Tables booklet, so every tool row shows.
 * The page is a placeholder; no PDF is rendered.
 */

import { useEffect, useRef, useState, type CSSProperties } from 'react';
import {
  ArrowLeft,
  ArrowUpRight,
  BookOpen,
  BookOpenCheck,
  Bookmark,
  BookmarkCheck,
  ChevronLeft,
  ChevronRight,
  Download,
  Highlighter,
  ListChecks,
  PenLine,
  Play,
  Repeat2,
  SlidersHorizontal,
  TrendingUp,
  ZoomIn,
  ZoomOut,
  type LucideIcon,
} from 'lucide-react';
import KobraScope, {
  Button,
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  Progress,
  ProgressLabel,
  Switch,
  Tabs,
  TabsList,
  TabsTrigger,
  toast,
} from '../../components/approved-ui-runtime';
import './viewer-chrome.css';

type Side = 'paper' | 'scheme';
type ToolKey = 'answers' | 'selfMark' | 'loop' | 'decode' | 'exam' | 'topics';

interface Tool {
  title: string;
  sub: string;
  icon: LucideIcon;
  /** A toggle carries a Switch; without one the row opens something. */
  toggle?: ToolKey;
}

/** The live Tools menu, in its order. */
const TOOLS: Tool[] = [
  { title: 'Answers', sub: 'Marking scheme beside each question', icon: BookOpenCheck, toggle: 'answers' },
  { title: 'Triage', sub: 'Rate each question before you start', icon: ListChecks },
  { title: 'Self-mark', sub: 'Score yourself against the scheme', icon: PenLine, toggle: 'selfMark' },
  { title: 'The Full Loop', sub: 'Work the paper question by question — attempt, reveal, mark', icon: Repeat2, toggle: 'loop' },
  { title: 'Command words', sub: 'Decode what each question demands', icon: Highlighter, toggle: 'decode' },
  { title: 'Exam mode', sub: 'Clock set to 180 min', icon: Play, toggle: 'exam' },
  { title: 'Topics & frequency', sub: 'How often each topic comes up + drill it across years', icon: TrendingUp, toggle: 'topics' },
  { title: 'Formulae & Tables', sub: 'Jump to the booklet section', icon: BookOpen },
];
/** Tools that need the paper's answer map, which loads once. */
const NEEDS_ANSWER_MAP: ToolKey[] = ['answers', 'selfMark', 'loop', 'topics'];
const PAGES: Record<Side, number> = { paper: 12, scheme: 16 };
const ZOOM_STEPS = [0.75, 1, 1.25, 1.5] as const;
const STATUS_TOAST = 'kr-vc-question-tools';
const OFF: Record<ToolKey, boolean> = { answers: false, selfMark: false, loop: false, decode: false, exam: false, topics: false };

export default function ViewerChromeAfter() {
  const [side, setSide] = useState<Side>('paper');
  const [pages, setPages] = useState<Record<Side, number>>({ paper: 3, scheme: 5 });
  const [zoomIndex, setZoomIndex] = useState(1);
  const [on, setOn] = useState<Record<ToolKey, boolean>>(OFF);
  const [saved, setSaved] = useState(false);
  const answerMapLoaded = useRef(false);
  const loadTimer = useRef<number | undefined>(undefined);
  useEffect(() => () => window.clearTimeout(loadTimer.current), []);

  const total = PAGES[side];
  const page = pages[side];
  const zoom = ZOOM_STEPS[zoomIndex];
  // As live: the Full Loop is a mode, not a counted overlay.
  const activeCount = [on.answers, on.decode, on.exam, on.topics, on.selfMark].filter(Boolean).length;
  const sideLabel = side === 'paper' ? 'paper' : 'marking scheme';

  function loadAnswerMap() {
    if (answerMapLoaded.current) return;
    answerMapLoaded.current = true;
    toast({ id: STATUS_TOAST, message: 'Loading question tools…', state: 'pending' });
    window.clearTimeout(loadTimer.current);
    // The live pill simply goes once the map arrives; settle the same toast and let it leave.
    loadTimer.current = window.setTimeout(() => toast({ id: STATUS_TOAST, message: 'Loading question tools…', lifetime: 200 }), 900);
  }
  function toggle(tool: ToolKey) {
    const next = !on[tool];
    setOn(current => ({ ...current, [tool]: next }));
    if (next && NEEDS_ANSWER_MAP.includes(tool)) loadAnswerMap();
  }
  function turnPage(delta: number) {
    setPages(current => ({ ...current, [side]: Math.min(PAGES[side], Math.max(1, current[side] + delta)) }));
  }
  function save() {
    if (saved) {
      setSaved(false);
      toast({ message: 'Removed from Saved papers' });
      return;
    }
    setSaved(true);
    toast({ message: 'Saved to Paper Trail', action: { label: 'Undo', run: () => setSaved(false) } });
  }

  return (
    <section className="kr-section kr-vc" aria-label="Paper Trail viewer">
      <div className="kr-vc-viewer" role="group" aria-label="Physics · 2025 — document viewer">
        <header className="kr-vc-toolbar">
          <Button variant="outline" size="icon" className="nsu-ink-outline kr-vc-icon" aria-label="Close viewer" onClick={() => toast({ message: 'Closes the viewer' })}>
            <ArrowLeft aria-hidden="true" />
          </Button>
          <div className="kr-vc-heading">
            <p className="kr-vc-title">Physics · 2025</p>
            <p className="kr-vc-subtitle">Paper · Higher</p>
          </div>

          <div className="kr-vc-controls">
            <Tabs value={side} onValueChange={value => setSide(value as Side)}>
              <TabsList aria-label="Paper or marking scheme">
                <TabsTrigger value="paper">Paper</TabsTrigger>
                <TabsTrigger value="scheme">Scheme</TabsTrigger>
              </TabsList>
            </Tabs>

            {side === 'paper' && (
              <Button
                className="kr-vc-answers"
                aria-pressed={on.answers}
                aria-label="Show the marking scheme beside each question"
                onClick={() => toggle('answers')}
              >
                <span className="kr-vc-answers-mark" aria-hidden="true" />Answers
              </Button>
            )}

            {side === 'paper' && (
              <DropdownMenu>
                <DropdownMenuTrigger
                  render={<Button variant="outline" className="nsu-ink-outline kr-vc-tools" data-active={activeCount > 0 || undefined} aria-label={`Study tools for this paper${activeCount ? `, ${activeCount} on` : ''}`} />}
                >
                  <SlidersHorizontal aria-hidden="true" />Tools
                  {activeCount > 0 && <span className="kr-vc-count" aria-hidden="true">{activeCount}</span>}
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" sideOffset={8} className="kr-vc-menu">
                  <KobraScope className="kr-page">
                    <p className="kr-vc-menu-label">Study tools</p>
                    {TOOLS.map(tool => {
                      const Icon = tool.icon;
                      const key = tool.toggle;
                      return key ? (
                        <DropdownMenuItem
                          key={tool.title}
                          className="kr-vc-tool"
                          role="menuitemcheckbox"
                          aria-checked={on[key]}
                          closeOnClick={false}
                          onClick={() => toggle(key)}
                        >
                          <span className="kr-vc-tool-icon" data-on={on[key] || undefined} aria-hidden="true"><Icon /></span>
                          <span className="kr-vc-tool-copy"><strong>{tool.title}</strong><small>{tool.sub}</small></span>
                          <span className="kr-vc-tool-switch" aria-hidden="true"><Switch checked={on[key]} tabIndex={-1} /></span>
                        </DropdownMenuItem>
                      ) : (
                        <DropdownMenuItem key={tool.title} className="kr-vc-tool" onClick={() => toast({ message: `Opens ${tool.title}` })}>
                          <span className="kr-vc-tool-icon" aria-hidden="true"><Icon /></span>
                          <span className="kr-vc-tool-copy"><strong>{tool.title}</strong><small>{tool.sub}</small></span>
                          <ArrowUpRight className="kr-vc-tool-open" aria-hidden="true" />
                        </DropdownMenuItem>
                      );
                    })}
                  </KobraScope>
                </DropdownMenuContent>
              </DropdownMenu>
            )}

            <Button variant="outline" className="nsu-ink-outline kr-vc-save" aria-pressed={saved} onClick={save}>
              {saved ? <BookmarkCheck aria-hidden="true" /> : <Bookmark aria-hidden="true" />}
              {saved ? 'Saved to Paper Trail' : 'Save to Paper Trail'}
            </Button>
          </div>

          <Button
            variant="outline"
            size="icon"
            className="nsu-ink-outline kr-vc-icon"
            aria-label={`Open the ${side} in your browser or download it (2.1 MB)`}
            onClick={() => toast({ message: `Opens the ${sideLabel} in your browser` })}
          >
            <Download aria-hidden="true" />
          </Button>
        </header>

        <div className="kr-vc-canvas" style={{ '--kr-vc-zoom': String(zoom) } as CSSProperties}>
          <article className="kr-vc-page" aria-label={`${side === 'paper' ? 'Paper' : 'Marking scheme'}, page ${page} of ${total}`}>
            <header className="kr-vc-page-head">
              <span>{side === 'paper' ? 'Physics · Higher Level' : 'Marking scheme · Physics · Higher Level'}</span>
              <span>Page {page}</span>
            </header>
            <div className="kr-vc-question">
              <h3 className="kr-vc-question-title">Question 2 (a)</h3>
              {side === 'paper' && on.answers && (
                <Button variant="outline" className="nsu-ink-outline kr-vc-chip" aria-label="Open the marking scheme for Question 2 (a)" onClick={() => setSide('scheme')}>
                  Mark scheme<ArrowUpRight aria-hidden="true" />
                </Button>
              )}
            </div>
            <div className="kr-vc-lines" aria-hidden="true"><span /><span /><span /><span /><span /></div>
            <p className="kr-vc-placeholder">Placeholder page. The {sideLabel} renders here.</p>
          </article>
          <p className="kr-vc-copyright">© State Examinations Commission</p>
        </div>

        <footer className="kr-vc-pagebar">
          <div className="kr-vc-zoom">
            <Button variant="outline" size="icon" className="nsu-ink-outline kr-vc-icon" aria-label="Zoom out" disabled={zoomIndex === 0} onClick={() => setZoomIndex(index => Math.max(0, index - 1))}>
              <ZoomOut aria-hidden="true" />
            </Button>
            <Button variant="outline" size="icon" className="nsu-ink-outline kr-vc-icon" aria-label="Zoom in" disabled={zoomIndex === ZOOM_STEPS.length - 1} onClick={() => setZoomIndex(index => Math.min(ZOOM_STEPS.length - 1, index + 1))}>
              <ZoomIn aria-hidden="true" />
            </Button>
          </div>
          <div className="kr-vc-position">
            <Button variant="outline" size="icon" className="nsu-ink-outline kr-vc-icon" aria-label="Previous page" disabled={page === 1} onClick={() => turnPage(-1)}>
              <ChevronLeft aria-hidden="true" />
            </Button>
            <Progress
              className="kr-vc-progress"
              value={Math.round((page / total) * 100)}
              getAriaValueText={() => `Page ${page} of ${total}`}
            >
              <ProgressLabel className="kr-vc-page-count"><span className="kr-vc-sr">Page </span>{page} <span className="kr-vc-of">of</span> {total}</ProgressLabel>
            </Progress>
            <Button variant="outline" size="icon" className="nsu-ink-outline kr-vc-icon" aria-label="Next page" disabled={page === total} onClick={() => turnPage(1)}>
              <ChevronRight aria-hidden="true" />
            </Button>
          </div>
        </footer>
      </div>
    </section>
  );
}
