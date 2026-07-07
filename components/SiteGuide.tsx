/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Site Guide — a swipeable tour of the site's core pages, opened from the
 * "?" in the home sidebar (or the ? key). One sleek card per page: a real
 * screenshot in a framed mock, what the page is, up to three things you do
 * there, and a "Take me there" deep link. Arrows + ←/→ on desktop, swipe on
 * touch, dots throughout. Images live in /assets/guide/<id>.jpg and degrade
 * gracefully to a monogram tile if one is missing.
 */

import React, { useCallback, useEffect, useRef, useState } from 'react';
import { ArrowRight, ChevronLeft, ChevronRight, X } from 'lucide-react';
import { AnimatePresence, useReducedMotion } from 'framer-motion';
import { MotionDiv } from './Motion';

export type GuideAction =
  | 'modules'
  | 'launchpad'
  | 'tool:paper-trail'
  | 'tool:examiners-chair'
  | 'tool:points-passport'
  | 'dashboard'
  | 'study';

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
    what: 'Everything starts here: your subjects, your streak, and the two doors — Modules for learning, the Launchpad for exam tools.',
    bullets: [
      'The progress rings show how far you are in each module category.',
      'Your daily quest and streak live at the top.',
      'The sidebar gets you anywhere in two taps.',
    ],
  },
  {
    id: 'modules',
    chip: 'Learn',
    title: 'Modules & the Library',
    what: 'Interactive lessons that teach you how to learn — memory, focus, exam craft — unlocking section by section as you work through them.',
    bullets: [
      'Pick a category, then a module from its library grid.',
      'Each section unlocks the next — no skimming, real reps.',
      'Every claim inside is backed by cited research.',
    ],
    go: { label: 'Browse the modules', action: 'modules' },
  },
  {
    id: 'launchpad',
    chip: 'Exam tools',
    title: 'The Launchpad',
    what: 'The tool shelf: everything built for the exams themselves — past papers, marking practice, points planning, orals, and more.',
    bullets: [
      'Filter by Understand, Plan or Track.',
      'Tools remember your subjects once your profile is set.',
      'The two flagships: Paper Trail and The Examiner’s Chair.',
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
    id: 'examiners-chair',
    chip: 'Exam tools · Marking',
    title: 'The Examiner’s Chair',
    what: 'Sit on the other side of the desk: mark sample scripts against the real SEC rules and learn to see your own answers the way the examiner will.',
    bullets: [
      'Every marking rule is cited to a real SEC scheme.',
      'The Daily Mark keeps your marking eye calibrated — one script a day.',
      'With a class code, compare calls with your class, anonymously.',
    ],
    go: { label: 'Take the chair', action: 'tool:examiners-chair' },
  },
  {
    id: 'progress',
    chip: 'Track',
    title: 'Your progress & the Coach',
    what: 'Everything you practise turns into numbers you can act on — accuracy by subject, weakest topics, and why your marks die.',
    bullets: [
      'The Coach composes your next 20 minutes from every tool’s signals.',
      'The autopsy splits lost marks into knowledge, technique, slips and time — each with a fix.',
      'Export a report to show a teacher or parent.',
    ],
    go: { label: 'See your dashboard', action: 'dashboard' },
  },
  {
    id: 'future',
    chip: 'Plan',
    title: 'Points Passport & your future',
    what: 'The CAO side of the house: track mock results, run safe/target/stretch scenarios, and explore the courses and careers that fit you.',
    bullets: [
      'Points Passport shows your trend and the cheapest grade jumps.',
      'Future Finder matches your interests to real CAO courses.',
      'College Compass keeps every deadline in order.',
    ],
    go: { label: 'Open Points Passport', action: 'tool:points-passport' },
  },
  {
    id: 'study',
    chip: 'Daily habit',
    title: 'Study Session & Focus',
    what: 'Where the daily work happens: structured study sessions that count toward your streak, and a calm focus timer that grows a grove.',
    bullets: [
      'Sessions log automatically into your insights and streak.',
      'Focus sessions plant a tree for every block you finish.',
      'With a class code, see how many classmates are at their desks too.',
    ],
    go: { label: 'Start a session', action: 'study' },
  },
  {
    id: 'help',
    chip: 'Classroom & help',
    title: 'Class codes — and this guide',
    what: 'A class code (any phrase your class agrees on) links the classroom features — always anonymous, only counts, never names.',
    bullets: [
      'Students send blind spots; teachers see what the class mis-marks.',
      'The Daily Mark duel compares you with the class median.',
      'This guide lives behind the ? in the sidebar — come back anytime.',
    ],
  },
];

const INK = '#1a1a1a';
const ACCENT = '#F26B1F';

/** Screenshot with a graceful monogram fallback when the asset is missing. */
const CardImage: React.FC<{ card: GuideCard }> = ({ card }) => {
  const [failed, setFailed] = useState(false);
  if (failed) {
    return (
      <div
        className="w-full aspect-[16/10] rounded-xl border-2 flex items-center justify-center"
        style={{ borderColor: INK, backgroundColor: '#FDEEDF' }}
        aria-hidden
      >
        <span className="text-[64px] font-bold" style={{ fontFamily: "'Source Serif 4', serif", color: ACCENT }}>
          {card.title.replace(/^The /, '').charAt(0)}
        </span>
      </div>
    );
  }
  return (
    <img
      src={`/assets/guide/${card.id}.jpg`}
      alt={`${card.title} — screenshot`}
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
      else if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [open, idx, goTo, onClose]);

  if (!open) return null;
  const card = CARDS[idx];

  return (
    <div
      className="fixed inset-0 z-[130] flex items-center justify-center px-4"
      role="dialog"
      aria-modal="true"
      aria-label="Site guide"
    >
      <div className="absolute inset-0 bg-black/50" onClick={onClose} />

      {/* Desktop arrows — outside the card */}
      <button
        onClick={() => goTo(idx - 1)}
        disabled={idx === 0}
        aria-label="Previous page"
        className="hidden sm:flex absolute left-6 lg:left-[calc(50%-350px)] items-center justify-center w-12 h-12 rounded-full border-2 bg-white transition-transform active:translate-y-0.5 disabled:opacity-30 z-10"
        style={{ borderColor: INK, boxShadow: '0 3px 0 rgba(0,0,0,0.35)' }}
      >
        <ChevronLeft size={22} color={ACCENT} strokeWidth={2.5} />
      </button>
      <button
        onClick={() => goTo(idx + 1)}
        disabled={idx === CARDS.length - 1}
        aria-label="Next page"
        className="hidden sm:flex absolute right-6 lg:right-[calc(50%-350px)] items-center justify-center w-12 h-12 rounded-full border-2 bg-white transition-transform active:translate-y-0.5 disabled:opacity-30 z-10"
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
            initial={reduced ? { opacity: 0 } : { opacity: 0, x: 32 * dirRef.current }}
            animate={{ opacity: 1, x: 0 }}
            exit={reduced ? { opacity: 0 } : { opacity: 0, x: -32 * dirRef.current }}
            transition={{ duration: 0.22, ease: [0.16, 1, 0.3, 1] }}
            className="rounded-2xl border-2 bg-white px-5 pt-5 pb-4 max-h-[88vh] overflow-y-auto"
            style={{ borderColor: INK, boxShadow: '0 6px 0 rgba(0,0,0,0.4)' }}
          >
            <div className="flex items-start justify-between gap-2 mb-3">
              <span
                className="text-[10px] font-bold uppercase tracking-[0.08em] rounded-full px-3 py-1"
                style={{ backgroundColor: '#FDEEDF', color: '#8C3A0E', border: '1px solid rgba(242,107,31,0.2)' }}
              >
                {card.chip}
              </span>
              <button onClick={onClose} aria-label="Close the guide" className="p-1 -mt-1 -mr-1" style={{ color: '#9e9186' }}>
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
                className="w-full rounded-full py-2.5 text-[14px] font-semibold text-white transition-transform active:translate-y-0.5 mb-3"
                style={{ backgroundColor: ACCENT, boxShadow: '0 3px 0 #B54D14' }}
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
