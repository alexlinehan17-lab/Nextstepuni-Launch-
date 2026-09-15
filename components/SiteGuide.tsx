/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Site Guide — a swipeable tour of the site's core pages, opened from the
 * home help menu (or the ? key). One card per page: a real
 * screenshot, what the page is, up to three things you do
 * there, and a "Take me there" deep link. Arrows + ←/→ on desktop, swipe on
 * touch, with persistent Next/Back controls. Every versioned image in /assets/guide/ is captured
 * from the running app. A missing asset shows a plain notice, never simulated
 * product UI.
 */

import React, { useCallback, useEffect, useRef, useState } from 'react';
import { ArrowRight, ChevronLeft, ChevronRight, Maximize2, X } from 'lucide-react';
import { useReducedMotion } from 'framer-motion';
import { MotionDiv } from './Motion';
import { useModal } from '../hooks/useModal';
import { useMobileAppDesign } from '../hooks/useMobileAppDesign';
import './site-guide.css';

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
    title: 'A little room for what’s next.',
    what: 'Your home brings the next chapter, your week’s study and your island together. Pick something small and keep going.',
    bullets: [
      'Start a study session or continue your unfinished module.',
      'Open Learning Paths, My Island and Launchpad from the illustrated cards.',
      'Find progress, year plans and account tools in your navigation.',
    ],
  },
  {
    id: 'modules',
    chip: 'Learn',
    title: 'Five worlds. Your own pace.',
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
    title: 'Make some time.',
    what: 'Choose a subject, how you’ll work and how long you have. Then settle into a study room that feels like yours.',
    bullets: [
      'Use After hours for a quiet, dark room, or turn on “I want my timer to have more colour!”.',
      'In Paper Horizon, the landscape opens out when you pause and settles back when you resume.',
      'Completed sessions build your history, streak and Journey Points.',
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
    what: 'Your exam archive, organised around your subjects. Find a past paper and its marking scheme together.',
    bullets: [
      'Choose your subject, level and exam year.',
      'Open a paper or its matching marking scheme from the same card.',
      'Save papers to return to them, or open Topic Atlas to practise by topic.',
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
    title: 'An island of your own.',
    what: 'Your effort becomes a world you can see: studying and completing modules earns Journey Points that build an island of your own.',
    bullets: [
      'Choose a tile from the tray and place it beside one you’ve already built.',
      'Each new tile reveals a little more of the Blue-pencil atlas.',
      'Use Find a sticker to follow a trail towards your next mythic discovery.',
    ],
    go: { label: 'Visit My Island', action: 'journey' },
  },
];

const CAPTURE_RELEASE = '2026-09-15';

/** Real captures stay readable in the card and can expand to the full image. */
const CardImage: React.FC<{ card: GuideCard; mobile: boolean }> = ({ card, mobile }) => {
  const [failed, setFailed] = useState(false);
  const [expanded, setExpanded] = useState(false);
  if (failed) return <p className="guide-capture-missing">Screen capture unavailable. You can still open this page below.</p>;
  return <figure className={`guide-capture ${mobile ? 'guide-capture-mobile' : ''} ${expanded ? 'guide-capture-expanded' : ''}`}>
    <button type="button" onClick={() => setExpanded(value => !value)} aria-expanded={expanded} aria-label={`${expanded ? 'Collapse' : 'Expand'} ${card.title} screenshot`} className="guide-capture-button">
      <img src={`/assets/guide/${CAPTURE_RELEASE}/${mobile ? 'mobile' : 'desktop'}/${card.id}.webp`} alt={`${card.title} — screenshot from the app`} data-guide-capture="real-app" onError={() => setFailed(true)} />
    </button>
    <figcaption><span>{mobile ? 'On your phone' : 'Inside the app'}</span><span><Maximize2 size={13} aria-hidden="true" />{expanded ? 'Tap to return' : 'Tap to expand'}</span></figcaption>
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
  return <div className="site-guide">
    <div className="guide-backdrop" onClick={onClose} aria-hidden="true" />
    <div ref={dialog} role="dialog" aria-modal="true" aria-label="Site guide" className="guide-dialog">
      <header className="guide-header">
        <span>A guide to your app</span>
        <button onClick={onClose} aria-label="Close the guide" className="guide-close"><X size={22} aria-hidden="true" /></button>
      </header>
      <div ref={body} className="guide-body" onTouchStart={event => { touch.current = { x: event.touches[0].clientX, y: event.touches[0].clientY }; }} onTouchEnd={event => {
        if (!touch.current) return;
        const dx = event.changedTouches[0].clientX - touch.current.x;
        const dy = event.changedTouches[0].clientY - touch.current.y;
        touch.current = null;
        if (Math.abs(dx) > 60 && Math.abs(dx) > Math.abs(dy) * 1.5) goTo(idx + (dx < 0 ? 1 : -1));
      }}>
        <MotionDiv key={card.id} className="guide-page" initial={{ opacity: reduced ? 1 : 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.15 }}>
          <div className="guide-page-heading">
            <p>{String(idx + 1).padStart(2, '0')} / {card.chip}</p>
            <h2>{card.title}</h2>
          </div>
          <CardImage key={`${card.id}-${mobile}`} card={card} mobile={mobile} />
          <div className="guide-copy">
            <p>{card.what}</p>
            <ol>{card.bullets.map((bullet, index) => <li key={bullet}><span aria-hidden="true">{String(index + 1).padStart(2, '0')}</span><span>{bullet}</span></li>)}</ol>
            {card.go && <button onClick={() => { onClose(); onGo(card.go!.action); }} className="guide-open-page">{card.go.label}<ArrowRight size={18} aria-hidden="true" /></button>}
          </div>
        </MotionDiv>
      </div>
      <footer className="guide-footer">
        <button onClick={() => goTo(idx - 1)} disabled={idx === 0} className="guide-previous" aria-label="Previous page"><ChevronLeft size={18} aria-hidden="true" />Back</button>
        <p role="status">{idx + 1} <span>of {CARDS.length}</span></p>
        {idx === CARDS.length - 1 ? <button onClick={onClose} className="guide-next">Done<ArrowRight size={18} aria-hidden="true" /></button> : <button onClick={() => goTo(idx + 1)} className="guide-next" aria-label="Next page">Next<ChevronRight size={18} aria-hidden="true" /></button>}
      </footer>
    </div>
  </div>;
};
export default SiteGuide;
