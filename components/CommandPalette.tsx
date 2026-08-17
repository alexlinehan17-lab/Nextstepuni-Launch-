/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Command palette — ⌘K / Ctrl+K anywhere in the app (also openable via
 * openCommandPalette() from any button). One fuzzy-search box over every
 * module, every Launchpad tool, and the core pages, so "I know it exists
 * but where is it" costs one keystroke instead of three taps.
 *
 * Navigation goes through NavigationContext, so the palette works from any
 * view. Rendering is a light modal in the module design register (white
 * card, 2px ink border, accent highlights) — deliberately light-only, like
 * the Site Guide, since it floats over a dimmed backdrop.
 */

import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Search, ArrowRight } from 'lucide-react';
import { useNavigation } from '../contexts/NavigationContext';
import { type CourseData } from './Library';

/** Launchpad tools, mirrored from InnovationZone's internal list.
 *  Keep titles in sync when a tool is added or renamed there. */
export const TOOL_TITLES: Record<string, string> = {
  'journey': 'Academic Journey Simulator',
  'cao-simulator': 'Points Passport · Grade Planner',
  'planner': 'Spaced Repetition Timetable',
  'war-room': 'War Room · Subject Coverage',
  'comeback': 'Comeback Engine',
  'future-finder-revamped': 'Future Finder',
  'points-passport': 'Points Passport',
  'college-compass': 'College Compass',
  'mark-bank': 'Mark Bank',
  'paper-trail': 'Paper Trail',
  'oral-trainer': 'Irish Oral Trainer',
  'examiners-chair': "The Examiner's Chair",
  'command-word-reflex': 'Command-Word Reflex',
  'how-they-did-it': 'How They Did It',
  'your-possible-life': 'Your Possible Life',
};

type EntryKind = 'page' | 'tool' | 'module';

interface PaletteEntry {
  kind: EntryKind;
  id: string;
  title: string;
  detail?: string;
  go: () => void;
}

/** Programmatic open — lets any button (e.g. a sidebar item) summon the palette. */
export const openCommandPalette = (): void => {
  window.dispatchEvent(new CustomEvent('nsu:command-palette'));
};

/** Cheap fuzzy score: exact substring beats word-prefix beats subsequence. */
export const fuzzyScore = (query: string, text: string): number => {
  const q = query.trim().toLowerCase();
  const t = text.toLowerCase();
  if (!q) return 0;
  const idx = t.indexOf(q);
  if (idx === 0) return 100;
  if (idx > 0) return t[idx - 1] === ' ' ? 80 : 60;
  // word-initials ("cps" → CAO Points Simulator)
  const initials = t.split(/[^a-z0-9]+/).filter(Boolean).map(w => w[0]).join('');
  if (initials.includes(q)) return 50;
  // subsequence fallback
  let ti = 0;
  for (const ch of q) {
    ti = t.indexOf(ch, ti);
    if (ti === -1) return 0;
    ti++;
  }
  return 20;
};

const KIND_CHIP: Record<EntryKind, { label: string; bg: string; color: string }> = {
  page:   { label: 'PAGE',   bg: '#f0efec', color: '#7a7068' },
  tool:   { label: 'TOOL',   bg: '#FDEEDF', color: '#8C3A0E' },
  module: { label: 'MODULE', bg: '#E8F2EC', color: '#1F5F3E' },
};

interface Props {
  courses: CourseData[];
}

const CommandPalette: React.FC<Props> = ({ courses }) => {
  const nav = useNavigation();
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [active, setActive] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);
  const listRef = useRef<HTMLDivElement>(null);

  // ⌘K / Ctrl+K toggles; the custom event opens.
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && (e.key === 'k' || e.key === 'K')) {
        e.preventDefault();
        setOpen(v => !v);
      }
    };
    const onOpen = () => setOpen(true);
    window.addEventListener('keydown', onKey);
    window.addEventListener('nsu:command-palette', onOpen);
    return () => {
      window.removeEventListener('keydown', onKey);
      window.removeEventListener('nsu:command-palette', onOpen);
    };
  }, []);

  useEffect(() => {
    if (open) {
      setQuery('');
      setActive(0);
      // Focus after the mount paints.
      const t = setTimeout(() => inputRef.current?.focus(), 30);
      return () => clearTimeout(t);
    }
  }, [open]);

  const close = useCallback(() => setOpen(false), []);

  const entries = useMemo<PaletteEntry[]>(() => {
    const pages: PaletteEntry[] = [
      { kind: 'page', id: 'home', title: 'Home', go: () => nav.navigateToTree() },
      { kind: 'page', id: 'modules', title: 'Modules', detail: 'The Programme', go: () => nav.navigateToModules() },
      { kind: 'page', id: 'launchpad', title: 'Launchpad', detail: 'All exam tools', go: () => nav.navigateToInnovationZone() },
      { kind: 'page', id: 'dashboard', title: 'My Progress', go: () => nav.navigateToDashboard() },
      { kind: 'page', id: 'learning-paths', title: 'Learning Paths', go: () => nav.navigateToLearningPaths() },
      { kind: 'page', id: 'my-journey', title: 'My Journey', go: () => nav.navigateToJourney() },
      { kind: 'page', id: 'training-hub', title: 'Training Hub', go: () => nav.navigateToGamificationHub() },
      { kind: 'page', id: 'study-session', title: 'Study Session', go: () => nav.navigateToStudySession() },
      { kind: 'page', id: 'insights', title: 'Insights', go: () => nav.navigateToInsights() },
      { kind: 'page', id: 'accreditation', title: 'References', go: () => nav.navigateToAccreditation() },
      { kind: 'page', id: 'year-plans', title: 'Year Plans', go: () => nav.navigateToYearPlans() },
    ];
    const tools: PaletteEntry[] = Object.entries(TOOL_TITLES).map(([id, title]) => ({
      kind: 'tool' as const,
      id,
      title,
      detail: 'Launchpad',
      go: () => nav.navigateToInnovationZone(id),
    }));
    const modules: PaletteEntry[] = courses.map(c => ({
      kind: 'module' as const,
      id: c.id,
      title: c.title,
      detail: c.subtitle,
      go: () => nav.navigateToModule(c.id),
    }));
    return [...pages, ...tools, ...modules];
  }, [nav, courses]);

  const results = useMemo(() => {
    const q = query.trim();
    if (!q) {
      // Default view: pages + tools — the "where can I go" menu.
      return entries.filter(e => e.kind !== 'module').slice(0, 12);
    }
    return entries
      .map(e => ({ e, s: fuzzyScore(q, e.title) }))
      .filter(r => r.s > 0)
      .sort((a, b) => b.s - a.s)
      .slice(0, 12)
      .map(r => r.e);
  }, [entries, query]);

  useEffect(() => { setActive(0); }, [query]);

  const pick = useCallback((entry: PaletteEntry) => {
    close();
    entry.go();
  }, [close]);

  const onInputKey = (e: React.KeyboardEvent) => {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setActive(v => Math.min(v + 1, results.length - 1));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setActive(v => Math.max(v - 1, 0));
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (results[active]) pick(results[active]);
    } else if (e.key === 'Escape') {
      close();
    }
  };

  // Keep the active row in view while arrowing.
  useEffect(() => {
    const el = listRef.current?.children[active] as HTMLElement | undefined;
    el?.scrollIntoView({ block: 'nearest' });
  }, [active]);

  if (!open) return null;

  return (
    <div
      className="fixed inset-0 z-[130] flex items-start justify-center px-4"
      style={{ paddingTop: 'min(18vh, 160px)' }}
      role="dialog"
      aria-modal="true"
      aria-label="Jump to"
      onMouseDown={e => { if (e.target === e.currentTarget) close(); }}
    >
      <div className="absolute inset-0 bg-black/45" onMouseDown={close} />
      <div
        className="relative w-full max-w-[560px] rounded-2xl bg-white overflow-hidden"
        style={{ border: '2px solid #1a1a1a', boxShadow: '0 4px 0 rgba(0,0,0,0.4)' }}
      >
        <div className="flex items-center gap-3 px-4 py-3" style={{ borderBottom: '2px solid #f0efec' }}>
          <Search size={16} style={{ color: '#F26B1F' }} />
          <input
            ref={inputRef}
            value={query}
            onChange={e => setQuery(e.target.value)}
            onKeyDown={onInputKey}
            placeholder="Jump to a module, tool or page…"
            className="flex-1 outline-none bg-transparent text-[15px]"
            style={{ color: '#1a1a1a' }}
            aria-label="Search"
          />
          <kbd
            className="hidden sm:block text-[10px] font-bold px-1.5 py-0.5 rounded"
            style={{ backgroundColor: '#f0efec', color: '#9e9186' }}
          >
            ESC
          </kbd>
        </div>

        <div ref={listRef} className="max-h-[46vh] overflow-y-auto py-1.5">
          {results.length === 0 && (
            <p className="px-4 py-6 text-[13px] text-center" style={{ color: '#9e9186' }}>
              Nothing matches &ldquo;{query}&rdquo; — try a shorter word.
            </p>
          )}
          {results.map((r, i) => {
            const chip = KIND_CHIP[r.kind];
            const isActive = i === active;
            return (
              <button
                key={`${r.kind}:${r.id}`}
                onClick={() => pick(r)}
                onMouseMove={() => setActive(i)}
                className="w-full flex items-center gap-3 px-4 py-2.5 text-left"
                style={isActive ? { backgroundColor: '#FDEEDF' } : undefined}
              >
                <span
                  className="text-[9px] font-bold tracking-[0.08em] px-1.5 py-0.5 rounded shrink-0"
                  style={{ backgroundColor: chip.bg, color: chip.color, minWidth: 52, textAlign: 'center' }}
                >
                  {chip.label}
                </span>
                <span className="flex-1 min-w-0">
                  <span className="block text-[14px] font-semibold truncate" style={{ color: '#1a1a1a' }}>{r.title}</span>
                  {r.detail && (
                    <span className="block text-[11.5px] truncate" style={{ color: '#9e9186' }}>{r.detail}</span>
                  )}
                </span>
                {isActive && <ArrowRight size={14} style={{ color: '#F26B1F' }} className="shrink-0" />}
              </button>
            );
          })}
        </div>

        <div className="flex items-center gap-3 px-4 py-2" style={{ borderTop: '2px solid #f0efec' }}>
          <span className="text-[10.5px]" style={{ color: '#9e9186' }}>
            <b>↑↓</b> to choose · <b>Enter</b> to go · <b>⌘K</b> anytime
          </span>
        </div>
      </div>
    </div>
  );
};

export default CommandPalette;
