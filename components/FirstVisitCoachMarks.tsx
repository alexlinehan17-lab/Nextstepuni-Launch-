/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * First-visit coach marks — three short spotlight steps on the home page:
 * the module tree, the Launchpad, then the account menu, ending with the offer
 * to take the full Site Guide. Skippable at every step, shows exactly once
 * per account (localStorage). Targets are found by [data-coach="..."]; if a
 * target isn't visible (e.g. the collapsed mobile sidebar), the step renders
 * as a centred card instead of a spotlight — nothing ever breaks.
 *
 * The look (r5-home, agreed 26 Nov 2026): the page is dimmed and the part the
 * step is about stays lit, ringed in ink. On a phone the words come up in a
 * sheet from the bottom, with Skip and a charcoal Next the same size; on a
 * laptop they sit in a card beside what they point at.
 */

import React, { useCallback, useEffect, useState } from 'react';
import { useMobileAppDesign } from '../hooks/useMobileAppDesign';
import { useReducedMotion } from './Motion';
import { readSafeArea } from './ui/Frame';
import { Button } from './ui/Button';
import { Sheet } from './ui/Sheet';
import './first-visit-coach-marks.css';

const STEPS: { target: string; title: string; body: string }[] = [
  {
    target: 'modules',
    title: 'Your lessons live here',
    body: 'Interactive modules that teach you how to learn — memory, focus, exam craft. Browse any section; your reading and activity drafts save as you go.',
  },
  {
    target: 'launchpad',
    title: 'Your exam tools live here',
    body: 'The Launchpad: past papers beside their marking schemes, marking practice, CAO planning and more.',
  },
  {
    target: 'help',
    title: 'Help is always here',
    body: 'Open your account menu, then Help, for the full app guide. It walks through every core page with screenshots. You can also press ? from Home.',
  },
];

const KEY = 'nsu-coachmarks:';

export const coachMarksSeen = (uid?: string): boolean => {
  try {
    return localStorage.getItem(KEY + (uid || 'anon')) === '1';
  } catch {
    return true;
  }
};
const markSeen = (uid?: string) => {
  try {
    localStorage.setItem(KEY + (uid || 'anon'), '1');
  } catch { /* private mode */ }
};

/** Room kept round what the tour points at: the lit area on a phone, and the
 *  gap between the ring and the card on a laptop. */
const PHONE_PAD = 10;
const DESK_GAP = 18;
/** The phone bar (44) under the status bar: a lit target stays below it. */
const BAR_H = 44;

/** The element that scrolls the page the target is on. */
function scrollerOf(el: HTMLElement): HTMLElement {
  for (let node = el.parentElement; node; node = node.parentElement) {
    const overflow = getComputedStyle(node).overflowY;
    if (/(auto|scroll)/.test(overflow) && node.scrollHeight > node.clientHeight + 1) return node;
  }
  return (document.scrollingElement as HTMLElement | null) ?? document.documentElement;
}

interface Props {
  uid?: string;
  onFinish: () => void;
  /** "Take the full tour" on the last step. */
  onOpenGuide: () => void;
}

const FirstVisitCoachMarks: React.FC<Props> = ({ uid, onFinish, onOpenGuide }) => {
  const mobileAppDesign = useMobileAppDesign();
  const reducedMotion = useReducedMotion();
  const [step, setStep] = useState(0);
  const [rect, setRect] = useState<DOMRect | null>(null);
  const [card, setCard] = useState<HTMLDivElement | null>(null);

  const finish = useCallback(() => {
    markSeen(uid);
    onFinish();
  }, [uid, onFinish]);

  // Measure the current step's target; re-measure on resize/scroll.
  // A target can mount a beat late (home cards still hydrating right after
  // login), so if it isn't in the DOM yet, retry briefly. If it never appears,
  // skip the step rather than show a caption that points at nothing.
  useEffect(() => {
    let cancelled = false;
    let timer: ReturnType<typeof setTimeout> | undefined;
    let tries = 0;
    let resizeObserver: ResizeObserver | undefined;
    const MAX_TRIES = 30; // Allow lazy dashboard content and fonts to settle.

    // A target is ready only once it is both mounted and visible. The home
    // dashboard can restore below the fold after onboarding, so treating mere
    // DOM existence as success left the tour running without a spotlight. On a
    // phone it must also sit clear of the sheet the words come up in.
    const measure = (): boolean => {
      const targets = document.querySelectorAll<HTMLElement>(`[data-coach="${STEPS[step].target}"]`);
      // On a phone, prefer a target on the page to one in the tab bar: the
      // tour's sheet covers the bottom of the screen.
      const shown = [...targets].filter(target => {
        const bounds = target.getBoundingClientRect();
        return bounds.width > 4 && bounds.height > 4;
      });
      const el = mobileAppDesign ? shown.find(target => !target.closest('nav')) ?? shown[0] : targets[0];
      if (!el) { setRect(null); return false; }
      const r = el.getBoundingClientRect();
      const sized = r.width > 4 && r.height > 4;
      const sheet = mobileAppDesign ? document.querySelector<HTMLElement>('.coach-sheet')?.getBoundingClientRect().height ?? 0 : 0;
      const top = mobileAppDesign ? readSafeArea().top + BAR_H + PHONE_PAD : 0;
      const bottom = window.innerHeight - sheet - (mobileAppDesign ? PHONE_PAD : 0);
      const fixed = el.closest('nav, aside, .ui-bar') !== null;
      const visible = sized && (fixed ? r.bottom > 0 && r.top < window.innerHeight : r.top >= top - 1 && r.bottom <= bottom + 1) && r.bottom > 0 && r.top < window.innerHeight;
      if (!visible) {
        setRect(null);
        if (sized && !fixed) {
          if (mobileAppDesign) {
            // Bring it into the room between the bar and the sheet, centred.
            const room = Math.max(0, bottom - top);
            const scroller = scrollerOf(el);
            scroller.scrollTop += r.top - (top + Math.max(0, (room - r.height) / 2));
          } else {
            el.scrollIntoView({ block: 'center', inline: 'nearest', behavior: tries === 0 && !reducedMotion ? 'smooth' : 'auto' });
          }
        }
        return false;
      }
      setRect(r);
      resizeObserver?.disconnect();
      resizeObserver = new ResizeObserver(measure);
      resizeObserver.observe(el);
      return true;
    };

    if (!measure()) {
      const retry = () => {
        if (cancelled) return;
        tries += 1;
        if (measure()) return;
        if (tries >= MAX_TRIES) {
          // Target genuinely absent — advance past this step (or end the tour
          // if it was the last), so we never highlight nothing.
          if (step < STEPS.length - 1) setStep(v => v + 1);
          else { markSeen(uid); onFinish(); }
          return;
        }
        timer = setTimeout(retry, 120);
      };
      timer = setTimeout(retry, 120);
    }

    const mutationObserver = new MutationObserver(measure);
    mutationObserver.observe(document.body, { childList: true, subtree: true });

    window.addEventListener('resize', measure);
    window.addEventListener('scroll', measure, true);
    return () => {
      cancelled = true;
      if (timer) clearTimeout(timer);
      resizeObserver?.disconnect();
      mutationObserver.disconnect();
      window.removeEventListener('resize', measure);
      window.removeEventListener('scroll', measure, true);
    };
  }, [step, uid, onFinish, mobileAppDesign, reducedMotion]);

  const s = mobileAppDesign && step === 2 ? { ...STEPS[step], title: 'Help is always here', body: 'Find help, settings and the full app guide from your profile or the sidebar.' } : STEPS[step];
  const last = step === STEPS.length - 1;
  const next = () => (last ? finish() : setStep(v => v + 1));
  const guide = () => { markSeen(uid); onOpenGuide(); };

  const words = (
    <div className="coach-words">
      <p className="t-label coach-count">Quick tour · {step + 1} of {STEPS.length}</p>
      <h3 className="t-heading">{s.title}</h3>
      <p className="t-sub">{s.body}</p>
    </div>
  );
  const actions = (size: 'lg' | 'md') => (
    <>
      {last && <Button block size={size} onClick={guide}>Take the full tour</Button>}
      <div className="ui-pair">
        <Button size={size} onClick={finish}>Skip</Button>
        <Button kind="main" size={size} block arrow="forward" onClick={next}>{last ? 'Done' : 'Next'}</Button>
      </div>
    </>
  );

  // The lit area: what the step is about, a little room round it on a phone,
  // and the ink ring just outside that.
  const pad = mobileAppDesign ? PHONE_PAD : 0;
  const spot = rect ? (
    <div className={`coach-spot${mobileAppDesign ? ' coach-spot--phone' : ''}`} style={{ top: rect.top - pad, left: rect.left - pad, width: rect.width + pad * 2, height: rect.height + pad * 2 }} />
  ) : <div className="coach-dim" />;

  if (mobileAppDesign) {
    return (
      <>
        <div className="theme-compat coach-layer frame-takeover z-[125]" aria-hidden="true">{spot}</div>
        <Sheet open bare dim={false} title="Quick tour" onClose={finish} className="coach-sheet" footer={actions('lg')}>
          {words}
        </Sheet>
      </>
    );
  }

  // On a laptop the card sits beside what it points at: to the right of a
  // sidebar row, otherwise under it (or over it, when there is no room below).
  const cardH = card?.offsetHeight ?? 260;
  const cardW = card?.offsetWidth ?? 360;
  const safe = readSafeArea();
  let position: React.CSSProperties = { top: '50%', left: '50%', transform: 'translate(-50%, -50%)' };
  if (rect) {
    const beside = rect.right + DESK_GAP + cardW < window.innerWidth && rect.left < window.innerWidth / 3;
    if (beside) {
      position = { left: rect.right + DESK_GAP, top: Math.min(Math.max(16 + safe.top, rect.top - 21), window.innerHeight - cardH - 16 - safe.bottom) };
    } else {
      const below = rect.bottom + DESK_GAP;
      position = {
        top: below + cardH < window.innerHeight - safe.bottom - 16 ? below : Math.max(16 + safe.top, rect.top - DESK_GAP - cardH),
        left: Math.min(Math.max(16, rect.left), Math.max(16, window.innerWidth - cardW - 16)),
      };
    }
  }

  return (
    <div className="theme-compat coach-layer frame-takeover z-[125]" role="dialog" aria-modal="true" aria-label="Quick tour">
      {spot}
      <div ref={setCard} className="ui-part ui-pop coach-card" style={position}>
        {words}
        <div className="coach-actions">{actions('md')}</div>
      </div>
    </div>
  );
};

export default FirstVisitCoachMarks;
