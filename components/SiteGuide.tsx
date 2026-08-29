/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Site Guide — a swipeable tour of the site's core pages, opened from the
 * "?" in the home sidebar (or the ? key). One sleek card per page: a real
 * screenshot in a framed mock, what the page is, up to three things you do
 * there, and a "Take me there" deep link. Arrows + ←/→ on desktop, swipe on
 * touch, dots throughout. Every image in /assets/guide/<id>.jpg is captured
 * from the running app. A missing asset shows a plain notice, never simulated
 * product UI.
 */

import React, { useCallback, useEffect, useRef, useState } from 'react';
import { ArrowRight, ChevronLeft, ChevronRight, X } from 'lucide-react';
import { AnimatePresence, useReducedMotion } from 'framer-motion';
import { MotionDiv } from './Motion';
import { useModal } from '../hooks/useModal';

export type GuideAction =
  | 'modules'
  | 'learning-paths'
  | 'launchpad'
  | 'tool:paper-trail'
  | 'tool:mark-bank'
  | 'tool:points-passport'
  | 'dashboard'
  | 'study'
  | 'journey';

interface GuideCard {
  id: string;
  chip: string;
  title: string;
  what: string;
  bullets: string[];
  go?: { label: string; action: GuideAction };
}

const CARDS: GuideCard[] = [
  {
    id: 'home',
    chip: 'Start here',
    title: 'Home — your base camp',
    what: 'Your real home screen is the map: continue where you left off, or move straight into learning, tools, progress and your journey.',
    bullets: [
      'Pick up where you left off without finding the page again.',
      'Five clear destinations keep the full app easy to scan.',
      'The sidebar keeps Study, My Progress and Year Plans one tap away.',
    ],
  },
  {
    id: 'modules',
    chip: 'Learn',
    title: 'Modules & the Library',
    what: 'Five learning worlds cover mindset, growth, learning science, subject skills and exam performance — all at your own pace.',
    bullets: [
      'Continue the exact section you last reached.',
      'Move between the five worlds from one visual library.',
      'Every claim inside is backed by cited research.',
    ],
    go: { label: 'Browse the modules', action: 'modules' },
  },
  {
    id: 'learning-paths',
    chip: 'Guided learning',
    title: 'Learning Paths',
    what: 'Curated routes group the right modules into a clear sequence when you want direction instead of choosing lesson by lesson.',
    bullets: [
      'Start with foundations or choose a focused exam sprint.',
      'Continue from your next unfinished module in one tap.',
      'Each path shows its real progress and remaining modules.',
    ],
    go: { label: 'Explore Learning Paths', action: 'learning-paths' },
  },
  {
    id: 'study',
    chip: 'Daily habit',
    title: 'Study Session & Focus',
    what: 'Choose the subject, session type and length, then work inside a calm full-screen timer with a useful learning prompt.',
    bullets: [
      'The full-screen timer removes everything except the work.',
      'Strategy prompts turn techniques from the modules into action.',
      'Finished sessions feed your history, streak and Journey Points.',
    ],
    go: { label: 'Start a session', action: 'study' },
  },
  {
    id: 'launchpad',
    chip: 'Exam tools',
    title: 'The Launchpad',
    what: 'The complete tool shelf for understanding, practising, planning and tracking — including guidance when you are not sure where to begin.',
    bullets: [
      'Filter the shelf by Understand, Practice, Plan or Track.',
      'Get a recommendation from two quick questions.',
      'Your subjects and goals carry into the tools automatically.',
    ],
    go: { label: 'Open the Launchpad', action: 'launchpad' },
  },
  {
    id: 'paper-trail',
    chip: 'Exam tools · Papers',
    title: 'Paper Trail',
    what: 'Every SEC past paper beside its official marking scheme — with answers pinned to questions, time budgets, and a guided Full Loop mode.',
    bullets: [
      'Tap a question’s chip to see the scheme’s answer for exactly that question.',
      'Self-mark and tag where the marks died — it feeds your weakness map.',
      'The Full Loop walks a whole paper: attempt → reveal → mark → next.',
    ],
    go: { label: 'Open Paper Trail', action: 'tool:paper-trail' },
  },
  {
    id: 'mark-bank',
    chip: 'Exam tools · Practice',
    title: 'Mark Bank',
    what: 'Practise real exam questions one at a time, then mark each point against the official scheme and bring weak questions back at the right time.',
    bullets: [
      'Ways In can make dense wording easier to navigate without changing the question.',
      'Mark point by point instead of relying on a vague right-or-wrong result.',
      'Your confidence and result decide when the question returns.',
    ],
    go: { label: 'Open Mark Bank', action: 'tool:mark-bank' },
  },
  {
    id: 'progress',
    chip: 'Track',
    title: 'My Progress',
    what: 'Your study rhythm, confidence, practice evidence and programme milestones come together in one real learning record.',
    bullets: [
      'Switch between week, month and year views.',
      'Filter the dashboard to understand one subject at a time.',
      'Insights turn charts into clear next moves.',
    ],
    go: { label: 'See your dashboard', action: 'dashboard' },
  },
  {
    id: 'points-passport',
    chip: 'Plan',
    title: 'Points Passport',
    what: 'Turn your current and target grades into a practical points plan, with trends, scenarios and the most valuable next grade moves.',
    bullets: [
      'See your current points, target and remaining gap immediately.',
      'Track mocks and compare realistic grade scenarios.',
      'Best Moves highlights where another grade is worth the most.',
    ],
    go: { label: 'Open Points Passport', action: 'tool:points-passport' },
  },
  {
    id: 'journey',
    chip: 'Build your world',
    title: 'My Journey',
    what: 'Your effort becomes a world you can see: studying and completing modules earns Journey Points that build an island of your own.',
    bullets: [
      'Your island grows from the progress you make elsewhere in the app.',
      'Journey Points unlock additions in the build shop.',
      'Your north-star goal stays visible at the heart of the world.',
    ],
    go: { label: 'Visit My Journey', action: 'journey' },
  },
];

const INK = '#1a1a1a';
const ACCENT = '#F26B1F';

/** A real app capture. Missing assets fail to a plain notice, never simulated UI. */
const CardImage: React.FC<{ card: GuideCard }> = ({ card }) => {
  const [failed, setFailed] = useState(false);
  if (failed) {
    return (
      <div
        className="flex aspect-[16/10] w-full items-center justify-center rounded-xl border-2 bg-[#F3F0EB] px-6 text-center"
        style={{ borderColor: INK }}
        role="img"
        aria-label={`${card.title} screenshot unavailable`}
      >
        <span className="text-xs font-semibold text-[#6F6861]">Screen capture unavailable</span>
      </div>
    );
  }
  return (
    <img
      src={`/assets/guide/${card.id}.jpg`}
      alt={`${card.title} — real screenshot from the app`}
      data-guide-capture="real-app"
      className="w-full aspect-[16/10] object-cover object-top rounded-xl border-2"
      style={{ borderColor: INK }}
      onError={() => setFailed(true)}
      loading="eager"
    />
  );
};

interface Props {
  open: boolean;
  onClose: () => void;
  /** Deep-link out of the guide (closes it first). */
  onGo: (action: GuideAction) => void;
}

const SiteGuide: React.FC<Props> = ({ open, onClose, onGo }) => {
  useModal(open, onClose);
  const [idx, setIdx] = useState(0);
  const [visited, setVisited] = useState<Set<number>>(() => new Set([0]));
  const reduced = useReducedMotion();
  const touchX = useRef<number | null>(null);
  const dirRef = useRef(1);

  const goTo = useCallback((next: number) => {
    const clamped = Math.max(0, Math.min(CARDS.length - 1, next));
    dirRef.current = clamped >= next ? (clamped === next ? dirRef.current : -1) : 1;
    setIdx(prev => {
      dirRef.current = clamped > prev ? 1 : -1;
      return clamped;
    });
    setVisited(v => new Set(v).add(clamped));
  }, []);

  // Reset to the first card each time the guide opens.
  useEffect(() => {
    if (open) {
      setIdx(0);
      setVisited(new Set([0]));
    }
  }, [open]);

  // Keyboard: ← → navigate, Esc closes.
  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'ArrowRight') goTo(idx + 1);
      else if (e.key === 'ArrowLeft') goTo(idx - 1);
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [open, idx, goTo]);

  if (!open) return null;
  const card = CARDS[idx];

  return (
    <div
      className="fixed inset-0 z-[200] flex items-end justify-center p-0 sm:items-center sm:p-4"
      role="dialog"
      aria-modal="true"
      aria-label="Site guide"
    >
      <div className="absolute inset-0 bg-[#1A1A1A]/55" onClick={onClose} />

      {/* Desktop arrows — outside the card */}
      <button
        onClick={() => goTo(idx - 1)}
        disabled={idx === 0}
        aria-label="Previous page"
        className="hidden sm:flex absolute left-6 lg:left-[calc(50%-350px)] items-center justify-center w-12 h-12 rounded-xl border-2 bg-[#FAFBF6] transition-transform active:translate-y-0.5 disabled:opacity-30 z-10"
        style={{ borderColor: INK, boxShadow: '0 3px 0 rgba(0,0,0,0.35)' }}
      >
        <ChevronLeft size={22} color={ACCENT} strokeWidth={2.5} />
      </button>
      <button
        onClick={() => goTo(idx + 1)}
        disabled={idx === CARDS.length - 1}
        aria-label="Next page"
        className="hidden sm:flex absolute right-6 lg:right-[calc(50%-350px)] items-center justify-center w-12 h-12 rounded-xl border-2 bg-[#FAFBF6] transition-transform active:translate-y-0.5 disabled:opacity-30 z-10"
        style={{ borderColor: INK, boxShadow: '0 3px 0 rgba(0,0,0,0.35)' }}
      >
        <ChevronRight size={22} color={ACCENT} strokeWidth={2.5} />
      </button>

      {/* The card */}
      <div
        className="relative w-full max-w-md"
        onTouchStart={e => { touchX.current = e.touches[0].clientX; }}
        onTouchEnd={e => {
          if (touchX.current === null) return;
          const dx = e.changedTouches[0].clientX - touchX.current;
          touchX.current = null;
          if (dx < -48) goTo(idx + 1);
          else if (dx > 48) goTo(idx - 1);
        }}
      >
        <AnimatePresence mode="wait" initial={false}>
          <MotionDiv
            key={card.id}
            initial={reduced ? { opacity: 0 } : { opacity: 0, y: 18, scale: 0.985 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={reduced ? { opacity: 0 } : { opacity: 0, y: 12, scale: 0.99 }}
            transition={{ type: 'spring', stiffness: 280, damping: 28, mass: 0.85 }}
            className="rounded-t-[24px] sm:rounded-[24px] border-[1.5px] bg-[#FAFBF6] px-5 pt-5 pb-4 max-h-[92dvh] overflow-y-auto"
            style={{ borderColor: INK, boxShadow: '5px 5px 0 #383838' }}
          >
            <div className="flex items-start justify-between gap-2 mb-3">
              <span
                className="text-[10px] font-bold uppercase tracking-[0.08em] rounded-full px-3 py-1"
                style={{ backgroundColor: '#FDEEDF', color: '#8C3A0E', border: '1px solid rgba(242,107,31,0.2)' }}
              >
                {card.chip}
              </span>
              <button onClick={onClose} aria-label="Close the guide" className="flex h-9 w-9 items-center justify-center rounded-xl border border-[#CFC9C2] bg-white -mt-1 -mr-1" style={{ color: '#6F6861' }}>
                <X size={18} />
              </button>
            </div>

            <CardImage card={card} />

            <h2 className="text-[20px] font-semibold mt-3.5 mb-1 leading-snug" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>
              {card.title}
            </h2>
            <p className="text-[13.5px] leading-relaxed mb-3" style={{ color: '#3a3530' }}>{card.what}</p>

            <ul className="space-y-1.5 mb-4">
              {card.bullets.map((b, i) => (
                <li key={i} className="flex items-start gap-2.5 text-[12.5px] leading-relaxed" style={{ color: '#5a5550' }}>
                  <span
                    className="shrink-0 mt-0.5 w-4.5 h-4.5 min-w-[18px] h-[18px] rounded-full flex items-center justify-center text-[10px] font-bold text-white"
                    style={{ backgroundColor: ACCENT, fontFamily: "'Source Serif 4', serif" }}
                  >
                    {i + 1}
                  </span>
                  {b}
                </li>
              ))}
            </ul>

            {card.go && (
              <button
                onClick={() => { onClose(); onGo(card.go!.action); }}
                className="w-full rounded-xl border-2 border-[#1A1A1A] py-2.5 text-[14px] font-semibold text-white transition-all active:translate-x-1 active:translate-y-1 active:shadow-none mb-3"
                style={{ backgroundColor: ACCENT, boxShadow: '3px 3px 0 #1A1A1A' }}
              >
                {card.go.label} <ArrowRight size={14} className="inline -mt-0.5" />
              </button>
            )}

            {/* Dots + counter */}
            <div className="flex items-center justify-center gap-1.5">
              {CARDS.map((c, i) => (
                <button
                  key={c.id}
                  onClick={() => goTo(i)}
                  aria-label={`Go to card ${i + 1}: ${c.title}`}
                  className="rounded-full transition-all"
                  style={{
                    width: i === idx ? 18 : 7,
                    height: 7,
                    backgroundColor: i === idx ? ACCENT : visited.has(i) ? INK : '#d0cdc8',
                  }}
                />
              ))}
              <span className="ml-2 text-[11px] tabular-nums" style={{ color: '#9e9186' }}>
                {idx + 1} of {CARDS.length}
              </span>
            </div>
          </MotionDiv>
        </AnimatePresence>
      </div>
    </div>
  );
};

export default SiteGuide;
