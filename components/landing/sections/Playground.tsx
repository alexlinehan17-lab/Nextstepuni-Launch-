/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The product playground — the ElevenLabs move. One white frame: product
 * tabs across the top, a live mini-version of that product in the middle,
 * mode tabs along the bottom, and the CTA inside the frame. Every demo runs
 * on real data from demoData.ts.
 */

import React, { useEffect, useRef, useState } from 'react';
import { useInView } from 'framer-motion';
import { AnimatePresence, MotionDiv, useReducedMotion } from '../../Motion';
import { COPY, type PlaygroundTabId } from '../copy';
import { Button, TextTabs } from '../primitives';
import { APP_URL, FONT, L } from '../theme';
import MarkBankDemo, { MARKBANK_SUBTABS } from '../demos/MarkBankDemo';
import AtlasDemo, { ATLAS_SUBTABS } from '../demos/AtlasDemo';
import PlannerDemo, { PLANNER_SUBTABS } from '../demos/PlannerDemo';
import LaunchpadDemo, { LAUNCHPAD_SUBTABS } from '../demos/LaunchpadDemo';

export interface DemoProps {
  /** Active mode tab id for this demo. */
  sub: string;
  /** False while another product tab is showing — pause timers. */
  active: boolean;
}

const SUBTABS: Record<PlaygroundTabId, { id: string; label: string }[]> = {
  markbank: MARKBANK_SUBTABS,
  atlas: ATLAS_SUBTABS,
  planner: PLANNER_SUBTABS,
  launchpad: LAUNCHPAD_SUBTABS,
};

const DEMOS: Record<PlaygroundTabId, React.FC<DemoProps>> = {
  markbank: MarkBankDemo,
  atlas: AtlasDemo,
  planner: PlannerDemo,
  launchpad: LaunchpadDemo,
};

const DEMO_EVENT = 'landing:demo';

interface DemoEventDetail {
  demo: PlaygroundTabId;
  mode?: string;
}

/**
 * Ask the playground to show a demo (and optionally one of its modes) and
 * scroll itself into view. Any section on the page can call this — the
 * playground listens for the event while mounted.
 */
export const openDemo = (demo: PlaygroundTabId, mode?: string) => {
  window.dispatchEvent(new CustomEvent<DemoEventDetail>(DEMO_EVENT, { detail: { demo, mode } }));
};

const Playground: React.FC = () => {
  const reduce = useReducedMotion();
  const [tab, setTab] = useState<PlaygroundTabId>(() => {
    const wanted = new URLSearchParams(window.location.search).get('demo');
    return wanted && wanted in DEMOS ? (wanted as PlaygroundTabId) : 'markbank';
  });
  const [subs, setSubs] = useState<Record<PlaygroundTabId, string>>(() => {
    const p = new URLSearchParams(window.location.search);
    const wanted = p.get('demo');
    const mode = p.get('mode');
    const base: Record<PlaygroundTabId, string> = {
      markbank: MARKBANK_SUBTABS[0].id,
      atlas: ATLAS_SUBTABS[0].id,
      planner: PLANNER_SUBTABS[0].id,
      launchpad: LAUNCHPAD_SUBTABS[0].id,
    };
    if (wanted && mode && wanted in SUBTABS && SUBTABS[wanted as PlaygroundTabId].some(s => s.id === mode)) base[wanted as PlaygroundTabId] = mode;
    return base;
  });
  const meta = COPY.playground.tabs.find(t => t.id === tab)!;
  const Demo = DEMOS[tab];
  // Scripted autoplay only runs while the stage is actually on screen, so the
  // demo has not already played itself out by the time a reader scrolls to it.
  const stageRef = useRef<HTMLDivElement>(null);
  const stageInView = useInView(stageRef, { amount: 0.35 });

  // Other sections (chapter "Try it" links, the CTA row) open a demo by event.
  useEffect(() => {
    const onDemo = (e: Event) => {
      const detail = (e as CustomEvent<DemoEventDetail>).detail;
      if (!detail || !(detail.demo in DEMOS)) return;
      const { demo, mode } = detail;
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
        {/* Product tabs */}
        <div className="flex items-center justify-between gap-4 px-3 sm:px-5" style={{ borderBottom: `1px solid ${L.hairline}` }}>
          <TextTabs
            ariaLabel="Product"
            items={COPY.playground.tabs.map(t => ({ id: t.id, label: t.label }))}
            active={tab}
            onChange={id => setTab(id as PlaygroundTabId)}
            className="landing-strip"
            size="md"
          />
          <div className="hidden sm:block shrink-0 py-2">
            <Button variant="secondary" href={APP_URL} size="md">{COPY.playground.cta}</Button>
          </div>
        </div>

        {/* Stage: one grid cell, so the entering and exiting demo share the
            same slot and the stage grows with whichever is taller. */}
        <div ref={stageRef} style={{ position: 'relative', display: 'grid', minHeight: 'clamp(400px, 40vw, 480px)', background: L.paper }}>
          <AnimatePresence mode="wait" initial={false}>
            <MotionDiv
              key={tab}
              initial={reduce ? false : { opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={reduce ? undefined : { opacity: 0, y: -6 }}
              transition={{ duration: 0.22, ease: 'easeOut' }}
              style={{ gridArea: '1 / 1', minHeight: 'inherit' }}
            >
              <div className="p-5 sm:px-8 sm:py-7">
                <Demo sub={subs[tab]} active={stageInView} />
              </div>
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
