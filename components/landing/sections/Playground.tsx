/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The product playground — the ElevenLabs move, done honestly: product tabs
 * across the top, the ACTUAL app surface in the middle (Mark Bank board,
 * Topic Atlas feed, Command-Word Reflex), mode tabs along the bottom. Nothing
 * here is a mock-up; every surface is the same component the app renders,
 * running signed out.
 */

import React, { useEffect, useRef, useState } from 'react';
import { useInView } from 'framer-motion';
import { AnimatePresence, MotionDiv, useReducedMotion } from '../../Motion';
import { COPY, type PlaygroundTabId } from '../copy';
import { Button, TextTabs } from '../primitives';
import { APP_URL, FONT, L } from '../theme';
import MarkBankGlass, { MARKBANK_SUBJECTS_LIVE } from '../glass/MarkBankGlass';
import AtlasGlass, { ATLAS_TOPICS_LIVE } from '../glass/AtlasGlass';
import ReflexGlass, { REFLEX_SUBJECTS_LIVE } from '../glass/ReflexGlass';

const SUBTABS: Record<PlaygroundTabId, { id: string; label: string }[]> = {
  markbank: MARKBANK_SUBJECTS_LIVE,
  atlas: ATLAS_TOPICS_LIVE,
  reflex: REFLEX_SUBJECTS_LIVE,
};

const GLASS: Record<PlaygroundTabId, React.FC<{ sub: string; active: boolean }>> = {
  markbank: MarkBankGlass,
  atlas: AtlasGlass,
  reflex: ReflexGlass,
};

const DEMO_EVENT = 'landing:demo';
interface DemoEventDetail { demo: PlaygroundTabId; mode?: string }

/** Ask the playground to open a product (and optionally a mode) and scroll to it. Used by chapter "Try it" links. */
export const openDemo = (demo: PlaygroundTabId, mode?: string) => {
  window.dispatchEvent(new CustomEvent<DemoEventDetail>(DEMO_EVENT, { detail: { demo, mode } }));
};

const isTab = (v: string | null): v is PlaygroundTabId => v === 'markbank' || v === 'atlas' || v === 'reflex';

const Playground: React.FC = () => {
  const reduce = useReducedMotion();
  const [tab, setTab] = useState<PlaygroundTabId>(() => {
    const wanted = new URLSearchParams(window.location.search).get('demo');
    return isTab(wanted) ? wanted : 'markbank';
  });
  const [subs, setSubs] = useState<Record<PlaygroundTabId, string>>(() => {
    const p = new URLSearchParams(window.location.search);
    const wanted = p.get('demo'); const mode = p.get('mode');
    const base: Record<PlaygroundTabId, string> = {
      markbank: MARKBANK_SUBJECTS_LIVE[0].id,
      atlas: ATLAS_TOPICS_LIVE[0].id,
      reflex: REFLEX_SUBJECTS_LIVE[0].id,
    };
    if (isTab(wanted) && mode && SUBTABS[wanted].some(s => s.id === mode)) base[wanted] = mode;
    return base;
  });
  const meta = COPY.playground.tabs.find(t => t.id === tab)!;
  const Glass = GLASS[tab];

  // Live surfaces only run (and only fetch) while the stage is on screen.
  const stageRef = useRef<HTMLDivElement>(null);
  const stageInView = useInView(stageRef, { amount: 0.25 });

  useEffect(() => {
    const onDemo = (e: Event) => {
      const { demo, mode } = (e as CustomEvent<DemoEventDetail>).detail;
      if (!isTab(demo)) return;
      setTab(demo);
      if (mode && SUBTABS[demo].some(s => s.id === mode)) setSubs(s => ({ ...s, [demo]: mode }));
      document.getElementById('playground')?.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
    };
    window.addEventListener(DEMO_EVENT, onDemo);
    return () => window.removeEventListener(DEMO_EVENT, onDemo);
  }, [reduce]);

  return (
    <div id="playground" style={{ scrollMarginTop: 90 }}>
      <div className="flex items-end justify-between gap-4 mb-4">
        <p className="m-0" style={{ fontFamily: FONT.sans, fontSize: 15, fontWeight: 600, color: L.ink, lineHeight: 1.4 }}>{COPY.playground.eyebrow}</p>
      </div>
      <div style={{ background: L.paper, border: `1.5px solid ${L.edge}`, borderRadius: 22, overflow: 'hidden' }}>
        {/* Product tabs + the live mark */}
        <div className="flex items-center justify-between gap-4 px-3 sm:px-5" style={{ borderBottom: `1px solid ${L.hairline}` }}>
          <TextTabs
            ariaLabel="Product"
            items={COPY.playground.tabs.map(t => ({ id: t.id, label: t.label }))}
            active={tab}
            onChange={id => setTab(id as PlaygroundTabId)}
            className="landing-strip"
            size="md"
          />
          <span className="hidden sm:inline-flex items-center gap-2 shrink-0" style={{ fontFamily: FONT.mono, fontSize: 11, letterSpacing: '0.14em', textTransform: 'uppercase', color: L.faint }}>
            <span aria-hidden="true" className="landing-live-dot" style={{ width: 7, height: 7, borderRadius: 999, background: L.orange, display: 'inline-block' }} />
            {COPY.playground.live}
          </span>
        </div>

        {/* The window into the app */}
        <div ref={stageRef} style={{ position: 'relative', background: L.paper }}>
          <AnimatePresence mode="wait" initial={false}>
            <MotionDiv
              key={tab}
              initial={reduce ? false : { opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={reduce ? undefined : { opacity: 0 }}
              transition={{ duration: 0.2, ease: 'easeOut' }}
            >
              <Glass sub={subs[tab]} active={stageInView} />
            </MotionDiv>
          </AnimatePresence>
        </div>

        {/* Mode tabs + hint */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 sm:gap-6 px-3 sm:px-5 pb-2 sm:pb-0" style={{ borderTop: `1px solid ${L.hairline}` }}>
          <TextTabs
            ariaLabel={`${meta.label} modes`}
            items={SUBTABS[tab]}
            active={subs[tab]}
            onChange={id => setSubs(s => ({ ...s, [tab]: id }))}
            size="sm"
            className="landing-strip"
          />
          <p className="m-0 sm:text-right" style={{ fontFamily: FONT.sans, fontSize: 13, color: L.faint, lineHeight: 1.4, padding: '6px 0' }}>{meta.hint}</p>
        </div>
      </div>
      <div className="sm:hidden mt-4">
        <Button href={APP_URL} size="lg" className="w-full">{COPY.playground.cta}</Button>
      </div>
    </div>
  );
};

export default Playground;
