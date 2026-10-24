/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Dev-only review page (24 Oct 2026): the current screen on the left, the same
 * screen rebuilt on Kobra on the right, for the highest-impact items in the
 * adoption audit. Open /kobra-review.html on the dev server. The "Now" pane
 * is the real component in an iframe (/kobra-review-before.html) or the live
 * app; the "With Kobra" pane is a live rebuild in kobra-review/sections/.
 * Never part of the production build (vite.config.ts lists its inputs).
 */
import React, { Component, Suspense, lazy, useState, type ComponentType, type ReactNode } from 'react';
import { createRoot } from 'react-dom/client';
import KobraScope, { Tabs, TabsList, TabsTrigger, Toasts } from './components/approved-ui-runtime';
import './index.css';
import './kobra-review.css';

const SECTIONS = [
  {
    id: 'post-session', n: '01', title: 'After a study session',
    change: 'Every session leaves the Kobra setup for a taupe Tailwind flow with offset shadows, a rotated receipt and an underline-only mode toggle. The rebuild keeps every word and puts the three steps on paper cards: Checkbox rows for strategies, Tabs for the debrief mode, a RadioGroup for confidence, Kobra Buttons throughout.',
    before: '/kobra-review-before.html?screen=post-session', beforeNote: 'Click through the three steps.',
    file: 'PostSessionAfter',
  },
  {
    id: 'home', n: '02', title: 'Home',
    change: 'The hero sits outside the Kobra scope with a hard-coded #ff7915 button, card drop shadows and ghost links that only underline on hover. The rebuild is a primary Kobra Button, hairline cards, quiet bars and outline buttons that read as clickable before hover.',
    before: '/?view=tree', beforeNote: 'The live app, signed in.',
    file: 'HomeHeroAfter',
  },
  {
    id: 'mark-bank', n: '03', title: 'Mark Bank library',
    change: 'A Kobra shell around a hand-rolled level control, a fake Input, a fake checkbox, a private --mb-* palette and 19 !important. The rebuild uses Select, Tabs, Input, Checkbox and ToggleGroup, ink markers for the index, and has real loading and error states.',
    before: '/?view=innovation-zone&tool=mark-bank', beforeNote: 'The live app.',
    file: 'MarkBankLibraryAfter',
  },
  {
    id: 'viewer', n: '04', title: 'Paper viewer chrome',
    change: 'The viewer opens on every paper: a grey canvas, ink buttons with offset shadows, a hand-built Tools menu, three hand-rolled toasts and eight dialogs. The rebuild is the toolbar on Kobra: Tabs, outline Buttons, a DropdownMenu with a Switch per tool, Progress for the page position and the runtime toast.',
    before: '/?view=innovation-zone&tool=paper-trail', beforeNote: 'The live app; open any paper to see the current viewer.',
    file: 'ViewerChromeAfter',
  },
  {
    id: 'settings', n: '05', title: 'Settings',
    change: 'A cream Tailwind modal with seven offset shadows and border-only appearance cards, duplicating Your setup; dark mode is set in four places with three different controls. The rebuild is the same sections on a paper panel with Tabs, Switch rows and a RadioGroup, and it can open as a Kobra Dialog.',
    before: '/kobra-review-before.html?screen=settings', beforeNote: 'The current modal, mounted on its own.',
    file: 'SettingsAfter',
  },
  {
    id: 'sign-in', n: '06', title: 'Sign up and sign in',
    change: 'Every student meets this first. Today it uses Kobra for one consent checkbox: a white-chip-on-grey account switch, border-only role choice, a three-layer card shadow, a fourth font. The rebuild is a paper card with Tabs, Inputs, outline provider Buttons, a segmented join code, a Checkbox and a RadioGroup.',
    before: '/kobra-review-before.html?screen=login', beforeNote: 'The current page, mounted on its own.',
    file: 'SignInAfter',
  },
] as const;

// The rebuilds are written one by one; a glob tolerates the ones not there yet,
// where a direct import would fail Vite's import analysis for the whole page.
// One lazy component per section, created once: creating them in render would
// remount every rebuild on each theme change.
const MODULES = import.meta.glob('./kobra-review/sections/*After.tsx') as Record<string, () => Promise<{ default: ComponentType }>>;
const AFTER = SECTIONS.map(section => {
  const loader = MODULES[`./kobra-review/sections/${section.file}.tsx`];
  return loader ? lazy(loader) : null;
});

class Pending extends Component<{ children: ReactNode }, { failed: boolean }> {
  state = { failed: false };
  static getDerivedStateFromError() { return { failed: true }; }
  render() {
    return this.state.failed
      ? <p className="kr-pending">This rebuild is still being written. Reload in a minute.</p>
      : this.props.children;
  }
}

function Review() {
  const [dark, setDark] = useState(document.documentElement.classList.contains('dark'));
  const setTheme = (value: string) => {
    const next = value === 'dark';
    setDark(next);
    document.documentElement.classList.toggle('dark', next);
  };
  const theme = dark ? '&theme=dark' : '';
  return (
    <KobraScope className="kr-page">
      <div className="kr-shell">
        <header className="kr-topbar">
          <h1>Kobra review <em>— before and after</em></h1>
          <nav className="kr-nav" aria-label="Sections">
            {SECTIONS.map(section => <a key={section.id} href={`#${section.id}`}>{section.n} {section.title}</a>)}
          </nav>
          <Tabs value={dark ? 'dark' : 'light'} onValueChange={setTheme}>
            <TabsList aria-label="Theme">
              <TabsTrigger value="light">Light</TabsTrigger>
              <TabsTrigger value="dark">Dark</TabsTrigger>
            </TabsList>
          </Tabs>
        </header>
        <main className="kr-main">
          <div className="kr-hero">
            <p className="kr-kicker">Kobra adoption · review</p>
            <h2 className="kr-title">The same screens, <em>on Kobra.</em></h2>
            <p className="kr-lede">Left is what students see today. Right is the same screen rebuilt on the Kobra runtime and the house visual language, with the same words. Everything on the right is live: click, tick and type.</p>
          </div>
          {SECTIONS.map((section, index) => {
            const After = AFTER[index];
            const src = section.before.startsWith('/kobra-review-before') ? `${section.before}${theme}` : section.before;
            return (
              <section key={section.id} id={section.id} className="kr-block">
                <div className="kr-block-head"><span className="kr-n">{section.n}</span><h2>{section.title}</h2></div>
                <p className="kr-change">{section.change}</p>
                <div className="kr-pair">
                  <div className="kr-pane">
                    <p className="kr-pane-label"><span className="kr-dot" /><b>Now</b> {section.beforeNote} <span className="kr-open"><a href={src} target="_blank" rel="noreferrer">Open</a></span></p>
                    <div className="kr-frame"><iframe title={`${section.title} today`} src={src} loading="lazy" /></div>
                  </div>
                  <div className="kr-pane">
                    <p className="kr-pane-label after"><span className="kr-dot" /><b>With Kobra</b> live rebuild</p>
                    <div className="kr-frame after">
                      {After
                        ? <Pending><Suspense fallback={<p className="kr-pending">Loading…</p>}><After /></Suspense></Pending>
                        : <p className="kr-pending">This rebuild is still being written. Reload in a minute.</p>}
                    </div>
                  </div>
                </div>
              </section>
            );
          })}
        </main>
        <Toasts />
      </div>
    </KobraScope>
  );
}

const root = document.getElementById('root');
if (root) createRoot(root).render(<Review />);
