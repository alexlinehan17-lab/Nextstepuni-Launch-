import './module-cards.css';
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * ModulesView: the five module worlds (area 5 of the design build; boards
 * c-modules-pick on a phone, r5-modules on a laptop).
 *
 * One card picks up where the student left off. Then the five worlds, each a
 * white box you press keeping its drawing, its colour, its number and its
 * progress: stacked on a phone, side by side on a laptop. Find a starting
 * point and the Notebook close the page. Search sits behind the bar's search
 * button on a phone and is a field in the bar on a laptop.
 *
 * Motion (motion.md; the board's five moves at real speed, which Alex chose:
 * "the real speed is much better than slow"): the doors rise into place one
 * after another the first time the page is seen, their marks fill once and
 * their counts run up with them; a door grows to fill the page while its
 * drawing and name travel to their places on the world's page; Back plays it
 * in reverse. Reduced motion turns each move into a plain fade.
 */

import React, { useEffect, useLayoutEffect, useRef, useState, type CSSProperties, type ReactNode } from 'react';
import { Search } from 'lucide-react';
import { type CourseData } from './Library';
import { type CategoryType } from './KnowledgeTree';
import type { UserProgress } from '../types';
import { useCompactLayout } from '../hooks/useCompactLayout';
import { useSettingsContext } from '../contexts/SettingsContext';
import { useScreenLeave } from './navigation/useScreenLeave';
import { TopBar } from './ui/Bars';
import { Button, IconButton, Glyph, Arrow } from './ui/Button';
import { List, Row, PaperSheet, PressBox } from './ui/List';
import { SearchField } from './ui/Field';
import { Menu } from './ui/Menu';
import { FramePortal } from './ui/Frame';
import { MODULE_WORLDS, Marks, Readout, WorldArt, isModuleDone, moduleResumePoint, worldOf, worldProgress, worldStyle, type ModuleWorld } from './moduleWorlds';
import { ChosenRoute, ModuleSearchResults, NotebookSheet, StartingPointsSheet, useModuleDiscovery } from './learning/ModuleDiscovery';
import { requestModuleResume, takeWorldReturn } from './learning/intents';

interface ModulesViewProps {
  onBack: () => void;
  onSelectCategory: (category: CategoryType) => void;
  onSelectModule: (moduleId: string) => void;
  allCourses: CourseData[];
  categoryTitles: Record<CategoryType, string>;
  userProgress: UserProgress;
  /** The world's own page, drawn into the door as it opens (and as Back closes it). Without it the
   *  door simply opens the world. */
  renderWorld?: (category: CategoryType) => ReactNode;
}

/* ── Motion: the board's timings (site/src/js/c-modules.js), real speed ─────── */
const EASE = 'cubic-bezier(.23,1,.32,1)';       // --ease-out: arriving, pressing
const EASE_SHEET = 'cubic-bezier(.32,.72,0,1)'; // --ease-sheet: the door opening, front-loaded
const T = { stagger: 30, arrive: 180, markGap: 24, mark: 160, open: 360, veil: 80, inGap: 30, inDur: 220, inDelay: 60,
  back: 300, out: 120, backFadeAt: 90, backFade: 150, fade: 200, fadeOut: 160 };
const reducedMotion = () => typeof window !== 'undefined' && !!window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
const canAnimate = (el: Element | null | undefined): el is HTMLElement => !!el && typeof (el as HTMLElement).animate === 'function';
/** The doors arrive the first time the page is seen in a visit to the app, not every time. */
let doorsHaveArrived = false;

interface Box { x: number; y: number; w: number; h: number }
const boxOf = (el: Element | Range, origin: Box): Box => {
  const r = el.getBoundingClientRect();
  return { x: r.left - origin.x, y: r.top - origin.y, w: r.width, h: r.height };
};
const textBox = (el: Element, origin: Box): Box => {
  const range = document.createRange(); range.selectNodeContents(el);
  return boxOf(range, origin);
};
const inset = (r: Box, area: Box, radius: number) =>
  `inset(${r.y}px ${area.w - r.x - r.w}px ${area.h - r.y - r.h}px ${r.x}px round ${radius}px)`;
/** The transform that lays a flyer's own box exactly over a measured box. */
const onto = (natural: Box, to: Box, byHeight: boolean) => {
  const s = byHeight ? to.h / natural.h : to.w / natural.w;
  return `translate(${to.x - natural.x * s}px,${to.y - natural.y * s}px) scale(${s})`;
};

/** The marks on each door fill from the left, once, and its count runs up with them. */
function drawProgress(door: HTMLElement, delay: number) {
  const count = door.querySelector<HTMLElement>('[data-count]');
  const n = Number(count?.dataset.count ?? 0);
  const fills = door.querySelectorAll<HTMLElement>('.mw-marks i > b');
  if (count) count.textContent = '0';
  fills.forEach((fill, j) => {
    const a = fill.animate([{ transform: 'scaleX(0)' }, { transform: 'scaleX(1)' }], { duration: T.mark, delay: delay + j * T.markGap, easing: EASE, fill: 'backwards' });
    if (count && j < n) a.onfinish = () => { count.textContent = String(j + 1); };
  });
  if (count && !fills.length) count.textContent = String(n);
  window.setTimeout(() => { if (count) count.textContent = String(n); }, delay + fills.length * T.markGap + T.mark + 40);
}

type Move = { kind: 'open' | 'back'; world: ModuleWorld } | null;

export const ModulesView: React.FC<ModulesViewProps> = ({ onBack, onSelectCategory, onSelectModule, allCourses, userProgress, renderWorld }) => {
  const phone = useCompactLayout();
  const dark = useSettingsContext()?.settings.darkMode ?? false;
  const leave = useScreenLeave(onBack, 'Back');
  const { available, resume, routes } = useModuleDiscovery(allCourses, userProgress);
  const [searching, setSearching] = useState(false);
  const [query, setQuery] = useState('');
  const [startOpen, setStartOpen] = useState(false);
  const [notebookOpen, setNotebookOpen] = useState(false);
  const [routeId, setRouteId] = useState<string>('none');
  const [move, setMove] = useState<Move>(() => {
    const back = takeWorldReturn();
    const world = worldOf(back);
    return world && renderWorld ? { kind: 'back', world } : null;
  });
  const [layerArea, setLayerArea] = useState<CSSProperties | null>(null);
  const rootRef = useRef<HTMLDivElement>(null);
  const layerRef = useRef<HTMLDivElement>(null);
  const searchRef = useRef<HTMLInputElement>(null);
  const busy = useRef(false);

  const worlds = MODULE_WORLDS.filter(world => allCourses.some(course => course.category === world.id));
  const doneAll = allCourses.filter(course => isModuleDone(course, userProgress)).length;
  const chosenRoute = routes.find(route => route.id === routeId);

  // ── Move 2 and 3: the doors arrive and their marks fill, once per visit ──
  useLayoutEffect(() => {
    const root = rootRef.current;
    if (!root || move?.kind === 'back' || doorsHaveArrived) return;
    doorsHaveArrived = true;
    const doors = [...root.querySelectorAll<HTMLElement>('.mw-door')];
    if (!doors.length || !canAnimate(doors[0])) return;
    if (reducedMotion()) {
      root.querySelector<HTMLElement>('.mw-doors')?.animate([{ opacity: 0 }, { opacity: 1 }], { duration: T.fade, easing: 'ease-out', fill: 'backwards' });
      return;
    }
    doors.forEach((door, i) => {
      door.animate([{ opacity: 0, transform: 'translateY(8px)' }, { opacity: 1, transform: 'none' }], { duration: T.arrive, delay: i * T.stagger, easing: EASE, fill: 'backwards' });
      drawProgress(door, i * T.stagger + T.arrive * 0.66);
    });
    // Runs once, on the first paint of the page.
  }, []);

  const doorFor = (id: string) => rootRef.current?.querySelector(`[data-world="${id}"]`)?.closest<HTMLElement>('.mw-door') ?? null;

  // The world's page is laid over the Modules page's own area (beside sidebar B on a laptop,
  // above the tab bar on a phone) while a door opens or closes, and nothing else.
  useLayoutEffect(() => {
    if (!move || layerArea) return;
    if (move.kind === 'back') doorFor(move.world.id)?.scrollIntoView?.({ block: 'center' });
    const r = rootRef.current?.getBoundingClientRect();
    const tabbar = phone ? document.querySelector('.ui-tabbar')?.getBoundingClientRect() : undefined;
    const bottom = tabbar && tabbar.height > 0 ? tabbar.top : window.innerHeight;
    setLayerArea({ left: r ? Math.max(0, r.left) : 0, top: 0, width: r ? r.width : window.innerWidth, height: bottom });
  }, [move, layerArea]);

  // ── Move 4 and 5: a door opens into its world; Back closes it into its door ──
  useLayoutEffect(() => {
    const layer = layerRef.current;
    const root = rootRef.current;
    if (!move || !layerArea || !layer || !root) return;
    const door = doorFor(move.world.id);
    const area: Box = { x: layer.getBoundingClientRect().left, y: layer.getBoundingClientRect().top, w: layer.offsetWidth, h: layer.offsetHeight };
    const finishOpen = () => onSelectCategory(move.world.id);
    const finishBack = () => { busy.current = false; door?.classList.remove('is-src'); setMove(null); setLayerArea(null); door?.focus({ preventScroll: true }); };
    if (!door || !canAnimate(layer)) { if (move.kind === 'open') finishOpen(); else finishBack(); return; }

    if (reducedMotion()) {
      const a = move.kind === 'open'
        ? layer.animate([{ opacity: 0 }, { opacity: 1 }], { duration: T.fade, easing: 'ease-out', fill: 'both' })
        : layer.animate([{ opacity: 1 }, { opacity: 0 }], { duration: T.fadeOut, easing: 'ease-out', fill: 'forwards' });
      a.onfinish = move.kind === 'open' ? finishOpen : finishBack;
      return;
    }

    const doorBox = boxOf(door, area);
    const full: Box = { x: 0, y: 0, w: area.w, h: area.h };
    const dArt = door.querySelector('[data-world-art]');
    const dName = door.querySelector('[data-world-name]');
    const wArt = layer.querySelector<HTMLElement>('[data-world-art]');
    const wName = layer.querySelector<HTMLElement>('[data-world-name]');
    const flyers: HTMLElement[] = [];
    const moves: Animation[] = [];
    const duration = move.kind === 'open' ? T.open : T.back;
    const opt: KeyframeAnimationOptions = { duration, easing: EASE_SHEET, fill: 'both' };
    // The shared pieces (the drawing, the name) fly above both pages.
    const fly = (from: Element, to: HTMLElement, byText: boolean) => {
      const copy = byText ? document.createElement('span') : (from.cloneNode(true) as HTMLElement);
      if (byText) { copy.className = 't-name mw-fly-name'; copy.textContent = from.textContent; }
      copy.classList.add('mw-fly');
      layer.appendChild(copy);
      const natural = byText ? textBox(copy, area) : boxOf(copy, area);
      const a = byText ? textBox(from, area) : boxOf(from, area);
      const b = byText ? textBox(to, area) : boxOf(to, area);
      const [start, end] = move.kind === 'open' ? [a, b] : [b, a];
      to.style.visibility = 'hidden';
      (from as HTMLElement).style.visibility = 'hidden';
      flyers.push(copy);
      moves.push(copy.animate([{ transform: onto(natural, start, byText) }, { transform: onto(natural, end, byText) }], opt));
    };
    if (dArt && wArt) fly(dArt, wArt, false);
    if (dName && wName) fly(dName, wName, true);
    const page = layer.querySelector<HTMLElement>('.mw-layer-page');
    const ins = [...layer.querySelectorAll<HTMLElement>('[data-in]')];
    if (page) {
      const from = { clipPath: inset(doorBox, area, 14) };
      const to = { clipPath: inset(full, area, 0) };
      moves.push(page.animate(move.kind === 'open' ? [from, to] : [to, from], opt));
    }
    if (move.kind === 'open') {
      // Inside the growing door the page turns solid at once, so it reads as the box growing, not a wash.
      page?.animate([{ opacity: 0 }, { opacity: 1 }], { duration: T.veil, easing: 'ease-out', fill: 'backwards' });
      ins.forEach(el => {
        const g = Number(el.dataset.in) || 0;
        el.animate([{ opacity: 0, transform: 'translateY(10px)' }, { opacity: 1, transform: 'none' }], { duration: T.inDur, delay: T.inDelay + g * T.inGap, easing: EASE, fill: 'backwards' });
      });
    } else {
      ins.forEach(el => el.animate([{ opacity: 1 }, { opacity: 0 }], { duration: T.out, easing: EASE, fill: 'forwards' }));
      // The page lets the door show through as it arrives, so the door is never a blank box.
      if (page) moves.push(page.animate([{ opacity: 1 }, { opacity: 0 }], { duration: T.backFade, delay: T.backFadeAt, easing: 'ease-out', fill: 'forwards' }));
    }
    let cancelled = false;
    Promise.all(moves.map(a => a.finished.catch(() => undefined))).then(() => {
      if (cancelled) return;
      if (move.kind === 'open') { finishOpen(); return; }
      flyers.forEach(f => f.remove());
      if (dArt) (dArt as HTMLElement).style.visibility = '';
      if (dName) (dName as HTMLElement).style.visibility = '';
      finishBack();
    });
    return () => { cancelled = true; };
    // One move per change of `move`, once the layer is laid out.
  }, [move, layerArea]);

  const openWorld = (world: ModuleWorld) => {
    if (busy.current) return;
    if (!renderWorld) { onSelectCategory(world.id); return; }
    busy.current = true;
    doorFor(world.id)?.classList.add('is-src'); // it stays pressed while it opens
    setMove({ kind: 'open', world });
  };
  const continueReading = (id: string) => { requestModuleResume(id); onSelectModule(id); };

  useEffect(() => { if (searching) searchRef.current?.focus(); }, [searching]);

  // ── The pieces ──
  const pick = resume ? (() => {
    const world = worldOf(resume.category);
    const at = moduleResumePoint(resume, userProgress);
    return (
      <PaperSheet className={`mw-pick${phone ? '' : ' mw-pick--wide'}`} label="Pick up where you left off">
        <div className="mw-pick-copy" style={world ? worldStyle(world, dark) : undefined}>
          <p className="t-label mw-pick-label">Pick up where you left off</p>
          <h2 className={phone ? 't-heading mw-pick-title' : 't-title mw-pick-title'}>{resume.title}</h2>
          <p className="t-meta mw-pick-meta">{world ? <b className="mw-w-ink">{world.name}</b> : null}{world ? ' · ' : ''}Section {at.step} of {at.steps} · {at.title}</p>
        </div>
        <div className="mw-pick-go">
          <Marks total={at.steps} on={at.read} className="mw-pick-marks" />
          <Button kind="main" size="lg" block arrow="forward" onClick={() => continueReading(resume.id)}>Continue reading</Button>
        </div>
      </PaperSheet>
    );
  })() : null;

  const doors = (
    <section className="mw-sec mw-worlds" aria-labelledby="mw-worlds-head">
      <div className="mw-sec-head"><h2 id="mw-worlds-head" className="t-heading">Five worlds</h2><Readout className="mw-ink3">{doneAll} of {allCourses.length} done</Readout></div>
      <div className={`mw-doors${phone ? '' : ' mw-doors--row'}`}>
        {worlds.map(world => {
          const p = worldProgress(world.id, allCourses, userProgress);
          return (
            <div key={world.id} className="mw-door-slot" style={worldStyle(world, dark) as CSSProperties}>
              <PressBox className={`mw-door${phone ? '' : ' mw-door--tall'}`} label={`Open ${world.name}: ${p.done} of ${p.total} done`} onPress={() => openWorld(world)}>
                <span className="mw-door-in" data-world={world.id}>
                  {phone ? <WorldArt world={world} size={80} /> : <span className="mw-door-top"><WorldArt world={world} size={104} /><Arrow meaning="opens" size={20} className="mw-chev" /></span>}
                  <span className="mw-door-copy">
                    <span className="t-label mw-w-ink mw-door-place">{world.number} · {world.place}</span>
                    <span className="t-name mw-door-name"><span data-world-name>{world.name}</span></span>
                    <span className="t-meta mw-door-blurb">{world.blurb}</span>
                    <span className="mw-prog">
                      <Marks total={p.total} on={p.done} part={p.part} />
                      <Readout><span data-count={p.done}>{p.done}</span> of {p.total}</Readout>
                    </span>
                  </span>
                  {phone ? <Arrow meaning="opens" size={20} className="mw-chev" /> : null}
                </span>
              </PressBox>
            </div>
          );
        })}
      </div>
    </section>
  );

  const startMenu = (
    <Menu label="Find a starting point" value={routeId} onChange={setRouteId} className="mw-start-menu" block
      face={<span className="mw-cell"><span className="t-row">Find a starting point</span><span className="t-meta">Start from what you need help with</span></span>}
      options={routes.map(route => ({ value: route.id, label: route.title }))} />
  );

  const ends = phone ? (
    <section className="mw-sec">
      <List boxed className="mw-ends">
        <Row title="Find a starting point" meta="Start from what you need help with" onPress={() => setStartOpen(true)} />
        <Row title="Notebook" meta="Private notes and ideas you chose to keep" onPress={() => setNotebookOpen(true)} />
      </List>
    </section>
  ) : (
    <section className="mw-sec">
      <div className="mw-ends mw-ends--two">
        {startMenu}
        <List boxed className="mw-ends-cell"><Row title="Notebook" meta="Private notes and ideas you chose to keep" onPress={() => setNotebookOpen(true)} /></List>
      </div>
      {chosenRoute ? <ChosenRoute route={chosenRoute} onClear={() => setRouteId('none')} onOpen={onSelectModule} /> : null}
    </section>
  );

  const searchField = (
    <SearchField ref={searchRef} className="module-discovery-search mw-search" label="Search all your modules and sections" placeholder="Search modules and sections"
      value={query} onChange={event => setQuery(event.target.value)} autoComplete="off" />
  );

  return (
    <div ref={rootRef} className={`product-shell modules-shell mw-page ${phone ? 'mw-page--phone' : 'mw-page--desk'}`}>
      {phone ? (
        <TopBar data-student-page-header leave={leave ?? undefined} over="The programme" title="Modules"
          action={<IconButton label="Search modules and sections" aria-expanded={searching}
            icon={<Glyph icon={Search} />} onClick={() => { setSearching(value => !value); if (searching) setQuery(''); }} />} />
      ) : null}
      <div className="mw-col">
        {phone ? null : (
          <TopBar data-student-page-header tool ruled leave={leave ?? undefined} over="The programme" title="Modules" action={searchField} className="mw-deskbar" />
        )}
        {phone && searching ? <section className="mw-sec mw-search-sec">{searchField}</section> : null}
        {query.trim() ? <section className="mw-sec mw-results"><ModuleSearchResults courses={available} query={query} onOpen={onSelectModule} /></section> : null}
        {pick ? <section className="mw-sec mw-top">{pick}</section> : null}
        {doors}
        {ends}
      </div>
      {phone ? <StartingPointsSheet open={startOpen} onClose={() => setStartOpen(false)} routes={routes} onOpen={onSelectModule} /> : null}
      <NotebookSheet open={notebookOpen} onClose={() => setNotebookOpen(false)} courses={available} onOpen={onSelectModule} />
      {move && renderWorld ? (
        <FramePortal>
          <div ref={layerRef} className="mw-layer frame-takeover" style={layerArea ?? { visibility: 'hidden' }} aria-hidden="true" inert>
            {layerArea ? <div className="mw-layer-page">{renderWorld(move.world.id)}</div> : null}
          </div>
        </FramePortal>
      ) : null}
    </div>
  );
};

export default ModulesView;
