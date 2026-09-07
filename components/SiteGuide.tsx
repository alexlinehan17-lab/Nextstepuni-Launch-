/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Site Guide — a swipeable tour of the site's core pages, opened from the
 * home help menu (or the ? key). One card per page: a real
 * screenshot, what the page is, up to three things you do
 * there, and a "Take me there" deep link. Arrows + ←/→ on desktop, swipe on
 * touch, with persistent Next/Back controls. Every image in /assets/guide/<id>.jpg is captured
 * from the running app. A missing asset shows a plain notice, never simulated
 * product UI.
 */

import React, { useCallback, useEffect, useRef, useState } from 'react';
import { ArrowRight, ChevronLeft, ChevronRight, X } from 'lucide-react';
import { useReducedMotion } from 'framer-motion';
import { MotionDiv } from './Motion';
import { useModal } from '../hooks/useModal';
import { useMobileAppDesign } from '../hooks/useMobileAppDesign';

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
    what: 'Home brings your next lesson and today’s plan together. Continue where you left off, or move into study, tools and progress.',
    bullets: [
      'Pick up where you left off without finding the page again.',
      'Five clear destinations keep the full app easy to scan.',
      'The bottom bar takes you to Home, Progress, Study, Journey and Launch.',
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
      'Open the references in each module to read its sources.',
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
    what: 'Browse past papers and marking schemes in the Paper Trail reader, with question navigation and revision tools in the same view.',
    bullets: [
      'Open a paper, then use Answers to reach its marking scheme.',
      'Use Topics to find a question, then self-mark your attempt.',
      'Full Loop guides you through attempt, reveal, mark and next question.',
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

/** Current captures; mobile crops stay large enough to read. Tap to expand. */
const CardImage: React.FC<{ card: GuideCard; mobile: boolean }> = ({ card, mobile }) => {
  const [failed, setFailed] = useState(false);
  const [expanded, setExpanded] = useState(false);
  if (failed) return <p className="rounded-xl border border-zinc-300 p-6 text-sm dark:border-zinc-600">Screen capture unavailable. You can still open this page below.</p>;
  return <figure>
    <button type="button" onClick={() => setExpanded(value => !value)} aria-expanded={expanded} aria-label={`${expanded ? 'Collapse' : 'Expand'} ${card.title} screenshot`} className="block w-full overflow-hidden rounded-xl border border-zinc-300 bg-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#B54D14] dark:border-zinc-600">
      <img src={mobile ? `/assets/guide/mobile/${card.id}.webp` : `/assets/guide/${card.id}.jpg`} alt={`${card.title} — screenshot from the app`} data-guide-capture="real-app" className={`w-full object-cover object-top ${expanded ? 'h-auto' : mobile ? 'aspect-[393/300]' : 'aspect-[16/10]'}`} onError={() => setFailed(true)} />
    </button>
    <figcaption className="mt-2 text-xs text-zinc-500 dark:text-zinc-400">{expanded ? 'Tap the image to collapse' : 'Tap to see the full screen'}</figcaption>
  </figure>;
};

interface Props {
  open: boolean;
  onClose: () => void;
  /** Deep-link out of the guide (closes it first). */
  onGo: (action: GuideAction) => void;
}

const SiteGuide: React.FC<Props> = ({ open, onClose, onGo }) => {
  const dialog = useRef<HTMLDivElement>(null);
  const body = useRef<HTMLDivElement>(null);
  useModal(open, onClose, dialog);
  const mobile = useMobileAppDesign();
  const [idx, setIdx] = useState(0);
  const reduced = useReducedMotion();
  const touch = useRef<{ x: number; y: number } | null>(null);
  const goTo = useCallback((next: number) => setIdx(Math.max(0, Math.min(CARDS.length - 1, next))), []);
  useEffect(() => { if (open) setIdx(0); }, [open]);
  useEffect(() => { if (body.current) body.current.scrollTop = 0; }, [idx]);
  useEffect(() => {
    if (!open) return;
    const onKey = (event: KeyboardEvent) => {
      if (event.key === 'ArrowRight') { event.preventDefault(); goTo(idx + 1); }
      else if (event.key === 'ArrowLeft') { event.preventDefault(); goTo(idx - 1); }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [open, idx, goTo]);
  if (!open) return null;
  const card = CARDS[idx];
  return <div className="fixed inset-0 z-[200] flex items-end justify-center sm:items-center sm:p-4">
    <div className="absolute inset-0 bg-black/55" onClick={onClose} aria-hidden="true" />
    <div ref={dialog} role="dialog" aria-modal="true" aria-label="Site guide" className="relative flex max-h-[92dvh] w-full max-w-md flex-col overflow-hidden rounded-t-3xl border border-zinc-300 bg-white text-zinc-900 dark:border-zinc-700 dark:bg-zinc-900 dark:text-white sm:rounded-3xl" style={{ paddingBottom: 'env(safe-area-inset-bottom)' }}>
      <header className="flex shrink-0 items-center justify-between gap-3 border-b border-zinc-200 px-5 py-2 dark:border-zinc-700">
        <span className="text-xs font-bold uppercase tracking-widest text-[#B54D14] dark:text-orange-400">A guide to your app</span>
        <button onClick={onClose} aria-label="Close the guide" className="flex h-11 w-11 items-center justify-center rounded-lg"><X size={22} aria-hidden="true" /></button>
      </header>
      <div ref={body} className="min-h-0 overflow-y-auto overscroll-contain px-5 py-5" onTouchStart={event => { touch.current = { x: event.touches[0].clientX, y: event.touches[0].clientY }; }} onTouchEnd={event => {
        if (!touch.current) return;
        const dx = event.changedTouches[0].clientX - touch.current.x;
        const dy = event.changedTouches[0].clientY - touch.current.y;
        touch.current = null;
        if (Math.abs(dx) > 60 && Math.abs(dx) > Math.abs(dy) * 1.5) goTo(idx + (dx < 0 ? 1 : -1));
      }}>
        <MotionDiv key={card.id} initial={{ opacity: reduced ? 1 : 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.15 }}>
          <p className="mb-2 text-xs font-bold uppercase tracking-widest text-zinc-600 dark:text-zinc-400">{card.chip}</p>
          <h2 className="mb-4 font-serif text-3xl font-semibold leading-tight">{card.title}</h2>
          <CardImage key={`${card.id}-${mobile}`} card={card} mobile={mobile} />
          <p className="mb-5 mt-5 text-base leading-relaxed">{card.what}</p>
          <ul className="space-y-3">{card.bullets.map((bullet, index) => <li key={index} className="flex gap-3 text-[15px] leading-relaxed text-zinc-600 dark:text-zinc-300"><span className="font-bold text-[#B54D14] dark:text-orange-400" aria-hidden="true">{index + 1}.</span><span>{bullet}</span></li>)}</ul>
        </MotionDiv>
      </div>
      <footer className="shrink-0 border-t border-zinc-200 px-5 pb-3 pt-3 dark:border-zinc-700">
        {card.go && <button onClick={() => { onClose(); onGo(card.go!.action); }} className="mb-2 flex min-h-12 w-full items-center justify-between gap-3 rounded-xl bg-[#F26B1F] px-4 py-3 text-base font-bold text-[#1A1A1A]">{card.go.label}<ArrowRight size={20} aria-hidden="true" /></button>}
        <div className="flex items-center justify-between gap-2">
          <button onClick={() => goTo(idx - 1)} disabled={idx === 0} className="flex min-h-11 items-center gap-1 rounded-lg pr-2 text-sm font-semibold disabled:opacity-35" aria-label="Previous page"><ChevronLeft size={18} aria-hidden="true" />Back</button>
          <p role="status" className="text-sm tabular-nums text-zinc-600 dark:text-zinc-300">{idx + 1} of {CARDS.length}</p>
          {idx === CARDS.length - 1 ? <button onClick={onClose} className="min-h-11 rounded-lg px-3 text-sm font-bold">Done</button> : <button onClick={() => goTo(idx + 1)} className="flex min-h-11 items-center gap-1 rounded-lg pl-2 text-sm font-bold" aria-label="Next page">Next<ChevronRight size={18} aria-hidden="true" /></button>}
        </div>
      </footer>
    </div>
  </div>;
};
export default SiteGuide;
