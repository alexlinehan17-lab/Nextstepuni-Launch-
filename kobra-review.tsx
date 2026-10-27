/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Dev-only review page (27 Oct 2026): the Kobra adoption items still open in
 * wave 1 and wave 2, each shown as the current screen on the left ("Now", the
 * real component in an iframe via /kobra-review-before.html?screen=…) beside
 * the same screen rebuilt on the Kobra runtime on the right ("With Kobra", a
 * live rebuild in kobra-review/sections/). Alex reviews from this page.
 * Never part of the production build (vite.config.ts lists its inputs).
 */
import React, { Component, Suspense, lazy, useState, type ComponentType, type ReactNode } from 'react';
import { createRoot } from 'react-dom/client';
import KobraScope, { Tabs, TabsList, TabsTrigger, Toasts } from './components/approved-ui-runtime';
import './index.css';
import './kobra-review.css';

const SECTIONS = [
  {
    id: 'mark-bank-session', n: '01', wave: 'Wave 1', effort: 'M', title: 'Mark Bank session controls',
    change: 'Inside the flagship screen there are 305 inline style objects and 41 !important; every rail button is forced to outline, so Reveal stops reading as the primary action, and the six subject rubric panels pick marks six different ways. The rebuild keeps the paper and the words: Reveal is the one primary Button, the answer route is the pill Tabs, grade and mark pickers are one ToggleGroup, claim rows are Checkbox rows that stay mint when claimed, and the exit confirm is the runtime Dialog.',
    before: '/kobra-review-before.html?screen=mark-bank-session', beforeNote: 'A real card from the bank, with the answer revealed.',
    file: 'MarkBankSession',
  },
  {
    id: 'progress', n: '02', wave: 'Wave 1', effort: 'M', title: 'My Progress',
    change: 'The section tabs are an ink grid while the date range already uses the pill; the mobile listbox is a native select; the page has its own theme switch; bars and loaders are hand-drawn, and orange stands for "completed". The rebuild uses the pill Tabs for sections, Select on phones, Progress bars with outlined tracks, hairline Insights and Milestones panels, and mint or ink for done.',
    before: '/kobra-review-before.html?screen=progress', beforeNote: 'The current dashboard on a sample fortnight.',
    file: 'Progress',
  },
  {
    id: 'onboarding', n: '03', wave: 'Wave 2', effort: 'M', title: 'Onboarding, both flows',
    change: 'The phone and desktop flows share onboarding.css: native category selects, hand-drawn checkboxes for natives, segmented progress bars, alert dialogs and a hand-rolled grade slider, with border-only orange selection beside ink-fill selection. The rebuild keeps every step and word on Kobra: pill Tabs for categories, square Checkbox rows, runtime Progress, Dialog for the alerts, one strong selected treatment. Whether the full-orange welcome, north-star and schedule steps stay is an open decision for Alex.',
    before: '/kobra-review-before.html?screen=onboarding', beforeNote: 'The current flow, mounted on its own. Step through it.',
    file: 'Onboarding',
  },
  {
    id: 'topic-atlas', n: '04', wave: 'Wave 2', effort: 'M', title: 'Topic Atlas and the unscoped Paper Trail views',
    change: 'Only the Paper Trail home and subject pages sit inside the Kobra scope; saved, practice, Topic Atlas, Mock, Flashcards, Review and Progress render outside it, and in dark mode hex-coloured text on the zinc panels vanishes. The rebuild wraps the study surface in the scope: Select for the year, Input for search, the runtime toast for "Copied", a hairline marks lens, and placeholders while the index loads.',
    before: '/kobra-review-before.html?screen=topic-atlas', beforeNote: 'The current Revise by topic view on a real subject.',
    file: 'TopicAtlas',
  },
  {
    id: 'legal', n: '05', wave: 'Wave 2', effort: 'S', title: 'Legal modal and consent gate',
    change: 'Seen at every sign-up consent and every legal version bump: underline tabs for Privacy and Terms, a shell with a drop shadow and blur, an orange accent-color checkbox on the gate, a third font. The rebuild is the pill Tabs, the runtime Dialog, a square ink Checkbox and Kobra Buttons, in the house fonts.',
    before: '/kobra-review-before.html?screen=legal', beforeNote: 'The current modal and gate, mounted on their own.',
    file: 'Legal',
  },
  {
    id: 'command', n: '06', wave: 'Wave 2', effort: 'S', title: '⌘K command palette',
    change: 'The hand-built palette has a peach active row and a 4px drop shadow, and inside a module both it and the Kobra CommandMenu open on ⌘K. The rebuild ports the same entries to the runtime CommandMenu, so one palette opens everywhere.',
    before: '/kobra-review-before.html?screen=command', beforeNote: 'The current palette, open. Type to filter.',
    file: 'CommandPalette',
  },
  {
    id: 'planner', n: '07', wave: 'Wave 2', effort: 'S', title: 'Planner controls and the native-select sweep',
    change: 'The planner uses a hand-drawn day rail, cue-trigger buttons, a native select inside its Kobra Dialog and an orange done-circle. Around the app, seventeen native selects and the Launchpad subject picker still render the browser’s own control. The rebuild shows the day rail as the pill Tabs, cue triggers as a ToggleGroup, the native selects as Kobra Select, the subject picker as a Combobox, and a square ink check for done.',
    before: '/kobra-review-before.html?screen=planner', beforeNote: 'The current planner and three of the native selects.',
    file: 'Planner',
  },
  {
    id: 'email-link', n: '08', wave: 'Wave 2', effort: 'S', title: 'Email-link pages',
    change: 'Every new student lands here to verify their email, and every reset lands here too: hand-styled cards, inputs and buttons, "Looks good" in orange, a hard-coded 12 where the password length constant belongs. The rebuild is the same three pages on Card, Input and Button, with the states in ink and mint.',
    before: '/kobra-review-before.html?screen=email-link', beforeNote: 'Verify email, reset password and the forced change-password modal.',
    file: 'EmailLink',
  },
] as const;

const SHIPPED = [
  'Foundations: six more runtime primitives, one orange (#273)',
  'After a study session, as paper cards, with the study receipt untouched (#282)',
  'Mark Bank library on runtime controls and hairline rows (#283)',
  'Settings as one paper card in the runtime Dialog (#284)',
  'Paper Trail viewer chrome on runtime controls (#285)',
];
const DECLINED = ['Home (25 Oct: keep today’s Home)', 'Sign up and sign in (25 Oct: keep today’s LoginPage)'];
const DECISIONS = [
  'Kobra Tabs or ui/HorizontalTabs as the one selection bar (both draw the same pill today)',
  'Keep My Island’s cream paper and the Admin dashboard’s dark theme as deliberate exceptions',
  'Keep onboarding’s full-orange welcome, north-star and schedule steps',
  'The Modules hero sparkle and the pastel card circles',
  'How far to pull the immersive study room into study-kobra.css',
];

const MODULES = import.meta.glob('./kobra-review/sections/*After.tsx') as Record<string, () => Promise<{ default: ComponentType }>>;
const AFTER = SECTIONS.map(section => {
  const loader = MODULES[`./kobra-review/sections/${section.file}After.tsx`];
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
          <h1>Kobra review <em>— waves 1 and 2</em></h1>
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
            <p className="kr-kicker">Kobra adoption · what is left in waves 1 and 2</p>
            <h2 className="kr-title">Eight more screens, <em>on Kobra.</em></h2>
            <p className="kr-lede">The 24 October audit ranked every place the app still departs from the Kobra runtime and the house visual language into waves. Wave 0 (foundations) and four of the wave 1 screens are live. This page shows the eight items left in wave 1 (the daily path) and wave 2 (entry and reach): left is what students see today, right is the same screen rebuilt on Kobra with the same words. Everything on the right is live: click, tick and type. Nothing here is built into the app until you say so.</p>
            <div className="kr-ledger">
              <div>
                <p className="kr-ledger-head">Live since 25–27 October</p>
                <ul>{SHIPPED.map(item => <li key={item}>{item}</li>)}</ul>
              </div>
              <div>
                <p className="kr-ledger-head">Declined on 25 October, not on this page</p>
                <ul>{DECLINED.map(item => <li key={item}>{item}</li>)}</ul>
              </div>
              <div>
                <p className="kr-ledger-head">Open decisions the page cannot make for you</p>
                <ul>{DECISIONS.map(item => <li key={item}>{item}</li>)}</ul>
              </div>
            </div>
          </div>
          {SECTIONS.map((section, index) => {
            const After = AFTER[index];
            const src = `${section.before}${theme}`;
            return (
              <section key={section.id} id={section.id} className="kr-block">
                <div className="kr-block-head"><span className="kr-n">{section.n}</span><h2>{section.title}</h2><span className="kr-meta">{section.wave} · effort {section.effort}</span></div>
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
