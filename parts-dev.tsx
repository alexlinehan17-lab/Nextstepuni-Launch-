/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The parts sheet: every shared part (components/ui/) in every state, at phone
 * width, light and dark. For developers and for pictures; never part of the
 * production build (vite.config.ts lists its HTML inputs explicitly, and this
 * page is not one), so a student cannot reach it.
 *
 *   npx vite, then open /parts-dev.html
 *   ?theme=dark                    dark mode (the capture harness sets it too)
 *   ?open=sheet|save|confirm|toast  open one of the things that come up over the screen
 *   ?scene=tabbar                  a phone screen with the tab bar and a toast above it
 *   ?scene=menu-top                a menu button at the very top that prefers to open upwards
 *   ?scene=menu-low                a menu button low on the screen, above the tab bar
 *
 * Controls marked data-force="active" / "focus" are put in that state by the
 * picture script (Chrome's forced pseudo-states), so the pressed and focused
 * looks can be photographed.
 */
import React, { useRef, useState, type ReactNode } from 'react';
import { createRoot } from 'react-dom/client';
// The app loads its global stylesheet first and the parts after it; so does this page.
import './index.css';
import { ChartNoAxesColumn, ChevronLeft, Compass, Ellipsis, House, Map, Search, Timer } from 'lucide-react';
import IllustrationTheme from './components/IllustrationTheme';
import { Arrow, Button, Glyph, IconButton, TextButton } from './components/ui/Button';
import { ChoiceGroup, SelectionBar, Switch } from './components/ui/Choice';
import { Menu } from './components/ui/Menu';
import { Confirm, Sheet } from './components/ui/Sheet';
import { MessageHost, showMessage } from './components/ui/Message';
import { PinnedFooter, TabBar, TopBar } from './components/ui/Bars';
import { Field, SearchField } from './components/ui/Field';
import { List, PaperSheet, PressBox, Row } from './components/ui/List';
import { EmptyState, ErrorState, LoadingShape } from './components/ui/States';

const params = new URLSearchParams(window.location.search);
if (params.get('theme') === 'dark') document.documentElement.classList.add('dark');
const OPEN = params.get('open');
const SCENE = params.get('scene');

const CREW = {
  accounting: '/assets/star-crew/subjects/accounting.png',
  biology: '/assets/star-crew/subjects/biology.png',
  irish: '/assets/star-crew/subjects/irish-v3.png',
  mathematics: '/assets/star-crew/subjects/mathematics.png',
  snoozer: '/assets/star-crew/personal/11-snoozer.png',
};
const FUTURE_FINDER = '/assets/tools/future-finder-revamped.png';
const PLACES = [
  { id: 'home', label: 'Home', icon: House },
  { id: 'progress', label: 'Progress', icon: ChartNoAxesColumn },
  { id: 'study', label: 'Study', icon: Timer },
  { id: 'journey', label: 'Journey', icon: Map },
  { id: 'launch', label: 'Launch', icon: Compass },
];
const SUBJECTS = [
  { value: 'all', label: 'All subjects' },
  { value: 'accounting', label: 'Accounting' },
  { value: 'biology', label: 'Biology' },
  { value: 'irish', label: 'Irish' },
  { value: 'mathematics', label: 'Mathematics' },
];
const SECTIONS = [
  { value: 'overview', label: 'Overview' }, { value: 'study', label: 'Study' }, { value: 'confidence', label: 'Confidence' },
  { value: 'practice', label: 'Practice' }, { value: 'milestones', label: 'Milestones' },
];

function Section({ id, title, children }: { id: string; title: string; children: ReactNode }) {
  return (
    <section id={id} className="flex flex-col gap-4 border-t border-hairline px-6 pt-5 pb-8">
      <h2 className="t-heading text-ink-primary">{title}</h2>
      {children}
    </section>
  );
}

function Spec({ label, caption, children }: { label: string; caption?: ReactNode; children: ReactNode }) {
  return (
    <div className="flex flex-col gap-3" data-spec={label}>
      <p className="t-label text-ink-muted">{label}</p>
      {children}
      {caption ? <p className="t-meta">{caption}</p> : null}
    </div>
  );
}

function Line({ children }: { children: ReactNode }) {
  return <div className="flex flex-wrap items-center gap-3">{children}</div>;
}

function ButtonsSection() {
  const subjectRef = useRef<HTMLDivElement>(null);
  const timeRef = useRef<HTMLDivElement>(null);
  const [subject, setSubject] = useState<string | null>(null);
  const [minutes, setMinutes] = useState<string | null>(null);
  const missing = !subject
    ? { sentence: minutes ? 'Choose a subject to continue.' : 'Choose a subject and how long to study.', goTo: subjectRef }
    : !minutes ? { sentence: 'Choose how long to study.', goTo: timeRef } : undefined;
  return (
    <Section id="part-buttons" title="Buttons">
      <Spec label="Three kinds, and the icon button" caption="Main: charcoal, label left, arrow right. Second: white with a line. Text: no box. Icon: a bare glyph in a 44 x 44 target.">
        <Button kind="main" size="lg" block arrow="forward">Start session</Button>
        <Line><Button>Add a mock result</Button></Line>
        <Line>
          <TextButton arrow="forward">Your plan</TextButton>
          <TextButton tone="quiet">Skip</TextButton>
          <TextButton tone="danger">Delete account</TextButton>
        </Line>
        <Line>
          <IconButton label="Back" icon={<Glyph icon={ChevronLeft} />} />
          <IconButton label="Search" icon={<Glyph icon={Search} />} />
          <IconButton label="More" icon={<Glyph icon={Ellipsis} />} />
        </Line>
      </Spec>
      <Spec label="Three heights" caption="52 for the one main action of a task screen; 44 for everything else; 36 in toolbars and rows, still 44 to the finger.">
        <Line>
          <Button kind="main" size="lg">Continue</Button>
          <Button>Add</Button>
          <Button size="sm">Filter</Button>
        </Line>
      </Spec>
      <Spec label="Rank by style, not size" caption="Side by side, the same size. The one that matters is charcoal.">
        <div className="grid grid-cols-2 gap-3">
          <Button block>Browse topics</Button>
          <Button kind="main" block>Practise</Button>
        </div>
      </Spec>
      <Spec label="Pressed" caption="Every button gives on pointer-down: a fill step and scale .98.">
        <Line>
          <Button kind="main" data-force="active">Continue</Button>
          <Button data-force="active">Add</Button>
          <IconButton label="Back" data-force="active" icon={<Glyph icon={ChevronLeft} />} />
        </Line>
      </Spec>
      <Spec label="A main button never goes dead" caption="Until both choices are made, the sentence above the button says what is missing and the button names the next step. Pressing either takes you to the missing choice.">
        <div ref={subjectRef}>
          <ChoiceGroup legend="Subject" value={subject} onChange={setSubject}
            options={[{ value: 'Biology', label: 'Biology', art: CREW.biology }, { value: 'Mathematics', label: 'Mathematics', art: CREW.mathematics }]} />
        </div>
        <div ref={timeRef} className="flex flex-col gap-2">
          <p className="ui-choices-legend">Minutes</p>
          <SelectionBar label="Minutes" size="md" value={minutes ?? ''} onChange={setMinutes}
            options={[{ value: '15', label: '15' }, { value: '25', label: '25' }, { value: '45', label: '45' }, { value: '60', label: '60' }]} />
        </div>
        <div className="border-t border-hairline pt-3" data-demo="needs">
          <Button kind="main" size="lg" block arrow="forward" missing={missing}>
            {!subject ? 'Choose your subject' : !minutes ? 'Choose how long' : `Start ${subject}`}
          </Button>
        </div>
        <Line><TextButton tone="quiet" onClick={() => { setSubject(null); setMinutes(null); }}>Start again</TextButton></Line>
      </Spec>
      <Spec label="Not available yet" caption="Truly locked: a well, a quiet label, and a line saying why and when it opens. Never just faded.">
        <Button size="lg" block unavailable="Opens when you finish Your interests. 8 questions to go.">Start What matters</Button>
      </Spec>
      <Spec label="The four arrows">
        <List><Row title="Unit 2 · The cell" meta="9 topics · 231 questions" onPress={() => {}} /></List>
        <Line><TextButton arrow="forward">Your plan</TextButton><span className="t-meta">Arrow right: forward, or another place</span></Line>
        <Line><Menu label="Subject" value="all" options={SUBJECTS} onChange={() => {}} /><span className="t-meta">Chevron down: opens a menu</span></Line>
        <Line><TextButton arrow="leaves">Send feedback</TextButton><span className="t-meta">Up and right: leaves the app</span></Line>
        <Line><span className="text-ink-primary"><Arrow meaning="opens" size={20} /></span><span className="text-ink-primary"><Arrow meaning="forward" size={20} /></span><span className="text-ink-primary"><Arrow meaning="menu" size={20} /></span><span className="text-ink-primary"><Arrow meaning="leaves" size={20} /></span></Line>
      </Spec>
    </Section>
  );
}

function ChoosingSection() {
  const [answer, setAnswer] = useState<string | null>('like');
  const [subjects, setSubjects] = useState<string[]>(['biology', 'irish']);
  const [offer, setOffer] = useState(true);
  const [colour, setColour] = useState(false);
  const [show, setShow] = useState('paper');
  const [goal, setGoal] = useState('10');
  const [section, setSection] = useState('overview');
  return (
    <Section id="part-choosing" title="Choosing">
      <Spec label="One answer" caption="An outlined tile; chosen, it keeps its white face and gains an ink outline. Its round mark fills ink and the tick draws.">
        <ChoiceGroup legend="How much would you enjoy doing this?" value={answer} onChange={setAnswer}
          options={[{ value: 'love', label: "I'd love it" }, { value: 'like', label: "I'd like it" }, { value: 'unsure', label: 'Not sure' }]} />
      </Spec>
      <Spec label="Several, with a count" caption="The same tile with a square mark. Add becomes Added.">
        <ChoiceGroup kind="several" tiles legend="Your subjects" value={subjects} onChange={setSubjects}
          options={[
            { value: 'biology', label: 'Biology', meta: 'Add', metaChosen: 'Added' },
            { value: 'english', label: 'English', meta: 'Add', metaChosen: 'Added' },
            { value: 'irish', label: 'Irish', meta: 'Add', metaChosen: 'Added' },
            { value: 'physics', label: 'Physics', meta: 'Add', metaChosen: 'Added' },
          ]} />
      </Spec>
      <Spec label="A switch" caption="For a setting that takes effect at once. Ink when it is on.">
        <List>
          <Row title="Offer me questions when I finish" meta="Real exam questions on what you studied" trailing={<Switch checked={offer} onChange={setOffer} label="Offer me questions when I finish" />} />
          <Row title="Give my timer more colour" meta="After hours · a quiet dark study room" trailing={<Switch checked={colour} onChange={setColour} label="Give my timer more colour" />} />
        </List>
      </Spec>
      <Spec label="The selection bar" caption="Two to four one-word choices. The white pill with an ink edge slides; what is under it changes at once.">
        <SelectionBar label="Show" size="md" value={show} onChange={setShow} options={[{ value: 'paper', label: 'Paper' }, { value: 'scheme', label: 'Scheme' }]} />
        <p className="t-meta">Showing the exam {show === 'paper' ? 'paper' : 'marking scheme'}</p>
        <SelectionBar label="Sessions this week" value={goal} onChange={setGoal}
          options={[{ value: '6', label: '6' }, { value: '8', label: '8' }, { value: '10', label: '10' }, { value: '12', label: '12' }]} />
      </Spec>
      <Spec label="Moving between the parts of a screen" caption="A menu button with a count, never a bar.">
        <Line><Menu label="Progress section" count value={section} onChange={setSection} options={SECTIONS} /></Line>
      </Spec>
    </Section>
  );
}

function MenuSection() {
  const [subject, setSubject] = useState('all');
  return (
    <Section id="part-menu" title="Menu button and menu">
      <Spec label="A menu button and its menu" caption="The button shows the current value and a chevron. The current option has a tick. Choosing applies at once and closes the menu. It opens inside the safe box.">
        <Line><span data-demo="menu"><Menu label="Subject" value={subject} onChange={setSubject} options={SUBJECTS} /></span><span className="t-meta" data-demo="menu-value">Now: {SUBJECTS.find(s => s.value === subject)?.label}</span></Line>
        <Menu label="Subject" block value={subject} onChange={setSubject} options={SUBJECTS} />
      </Spec>
    </Section>
  );
}

function OverSection() {
  const [open, setOpen] = useState<string | null>(OPEN);
  const [subject, setSubject] = useState<string | null>('mathematics');
  const [goal, setGoal] = useState('10');
  const close = () => setOpen(null);
  React.useEffect(() => { if (OPEN === 'toast') showMessage('Saved to your plan', { action: { label: 'Undo', onPress: () => {} }, duration: 600000 }); }, []);
  return (
    <Section id="part-over" title="Sheets, confirms and toasts">
      <Spec label="Open one" caption="A sheet rises from the bottom on a phone and is a centred dialog from 640px. Close top-left; Cancel and Save when there are changes. The confirm is the one centred pop-up on a phone.">
        <Line>
          <Button onClick={() => setOpen('sheet')}>Bottom sheet</Button>
          <Button onClick={() => setOpen('save')}>Sheet with Save</Button>
          <Button onClick={() => setOpen('who')}>Sheet about someone</Button>
        </Line>
        <Line>
          <Button onClick={() => setOpen('confirm')}>Confirm</Button>
          <Button onClick={() => showMessage('Saved to your plan', { action: { label: 'Undo', onPress: () => {} } })}>Toast</Button>
        </Line>
      </Spec>
      <Sheet open={open === 'sheet'} onClose={close} title="What are you studying?"
        footer={<Button kind="main" size="lg" block arrow="forward" onClick={close}>Choose {SUBJECTS.find(s => s.value === subject)?.label ?? 'a subject'}</Button>}>
        <ChoiceGroup legend={<span className="sr-only">Subject</span>} value={subject} onChange={setSubject}
          options={[
            { value: 'accounting', label: 'Accounting', art: CREW.accounting },
            { value: 'biology', label: 'Biology', art: CREW.biology },
            { value: 'irish', label: 'Irish', art: CREW.irish },
            { value: 'mathematics', label: 'Mathematics', art: CREW.mathematics },
          ]} />
      </Sheet>
      <Sheet open={open === 'who'} onClose={close} title="Demo Student" meta="Student" art={<img src={CREW.accounting} alt="" />}>
        <List><Row icon={<Glyph icon={ChartNoAxesColumn} size={20} />} title="My Progress" onPress={close} /></List>
      </Sheet>
      <Sheet open={open === 'save'} onClose={close} title="This week's goal" titleSize="small" save={{ label: 'Save', onPress: close }}>
        <h3 className="t-title text-ink-primary">How many sessions this week?</h3>
        <SelectionBar label="Sessions this week" size="md" value={goal} onChange={setGoal}
          options={[{ value: '6', label: '6' }, { value: '8', label: '8' }, { value: '10', label: '10' }, { value: '12', label: '12' }]} />
        <p className="t-meta">You have done 6 so far. Your goal was 8.</p>
      </Sheet>
      <Confirm open={open === 'confirm'} sentence="Delete your account?"
        detail="Everything you have studied, planned and saved is erased and cannot be brought back."
        keepLabel="Keep my account" onKeep={close} dangerLabel="Delete account" onDanger={close} />
    </Section>
  );
}

function BarsSection() {
  const [need, setNeed] = useState(true);
  const answerRef = useRef<HTMLDivElement>(null);
  return (
    <Section id="part-bars" title="Bars">
      <Spec label="A place" caption="No leave control: the tab bar is how you move. Its small capitals label sits at the left.">
        <div className="border border-dashed border-outline-soft"><TopBar placeLabel="Tuesday, 24 November" /></div>
      </Spec>
      <Spec label="A page" caption="Back, a chevron, top left; one action at the right.">
        <div className="border border-dashed border-outline-soft"><TopBar leave={{ kind: 'back', onPress: () => {} }} title="Biology" action={<IconButton label="Search" icon={<Glyph icon={Search} />} />} /></div>
      </Spec>
      <Spec label="A Launchpad tool" caption="Its family as a small line over its name; its own drawing at the right, once.">
        <div className="border border-dashed border-outline-soft"><TopBar tool leave={{ kind: 'back', onPress: () => {} }} over="Start with you" title="Future Finder" art={FUTURE_FINDER} /></div>
      </Spec>
      <Spec label="Something over the top" caption="Close, an X, top left. A hairline once content scrolls under it.">
        <div className="border border-dashed border-outline-soft"><TopBar ruled leave={{ kind: 'close', onPress: () => {} }} title="Practice" /></div>
      </Spec>
      <Spec label="The tab bar" caption="Five places. The current one is ink with a 2px ink marker above it. It steps aside while the keyboard is up; a tab can carry a tour stop (coach).">
        <div className="border border-dashed border-outline-soft"><TabBar items={PLACES} current="launch" onSelect={() => {}} /></div>
      </Spec>
      <Spec label="The pinned footer" caption="The one main action of a task screen, the sentence naming what is missing directly above it.">
        <div ref={answerRef}><ChoiceGroup legend="Fixing something that has stopped working" value={need ? null : 'like'} onChange={() => setNeed(false)}
          options={[{ value: 'love', label: "I'd love it" }, { value: 'like', label: "I'd like it" }]} /></div>
        <div className="border border-dashed border-outline-soft">
          <PinnedFooter ruled note="Your answers stay as you go back">
            <Button kind="main" size="lg" block arrow="forward" missing={need ? { sentence: 'Choose an answer to go on.', goTo: answerRef } : undefined} onClick={() => setNeed(true)}>
              {need ? 'Choose an answer' : 'Continue'}
            </Button>
          </PinnedFooter>
        </div>
      </Spec>
    </Section>
  );
}

function FieldsSection() {
  const [on, setOn] = useState(true);
  return (
    <Section id="part-fields" title="Field, rows, the sheet, the box">
      <Spec label="A field">
        <Field label="First name" placeholder="Aoife" autoComplete="given-name" enterKeyHint="next" help="This is the name we greet you with." />
        <Field label="Email" defaultValue="aoife@glenrua.ie" type="email" inputMode="email" autoComplete="email" data-force="focus" />
        <Field label="School code" defaultValue="GLEN20" autoCapitalize="characters" error="That code is not one we know. Check it with your teacher and type it again." />
      </Spec>
      <Spec label="Search"><SearchField label="Search topics" placeholder="Search topics" /></Spec>
      <Spec label="Rows" caption="At least 56 tall, kept apart by a hairline. A row that opens something ends in a chevron; one that shows something ends in its value; a row with a switch has no chevron.">
        <List>
          <Row art={CREW.accounting} title="Accounting" meta={<>Practice · 45 min · <span className="text-accent-text">Up next</span></>} onPress={() => {}} />
          <Row title="Sessions this week" value="6 / 8" />
          <Row title="Offer me questions when I finish" trailing={<Switch checked={on} onChange={setOn} label="Offer me questions when I finish" />} />
        </List>
      </Spec>
      <Spec label="Rows with an icon" caption="The account sheet's rows: a bare 20px glyph in ink-2 at the left. A destructive row is red words with no arrow.">
        <List>
          <Row icon={<Glyph icon={ChartNoAxesColumn} size={20} />} title="My Progress" onPress={() => {}} />
          <Row icon={<Glyph icon={Timer} size={20} />} title="Log out" tone="danger" onPress={() => {}} />
        </List>
      </Spec>
      <Spec label="A group of rows that is one control" caption="Boxed only when the group as a whole is a control: a line, like every box you press.">
        <List boxed>
          <Row art={CREW.mathematics} over="Subject" title="Mathematics" onPress={() => {}} />
          <Row over="How you'll work" title="Practice" onPress={() => {}} />
        </List>
      </Spec>
      <Spec label="A box you press (level 1)" caption="A line only (the owner's choice, 26 Nov 2026); the lift token stays, set to nothing.">
        <div className="grid grid-cols-2 gap-3">
          <PressBox onPress={() => {}}><span className="t-row block">Exam paper</span><span className="t-meta">PDF · 2.4 MB</span></PressBox>
          <PressBox onPress={() => {}}><span className="t-row block">Marking scheme</span><span className="t-meta">PDF · 519 KB</span></PressBox>
        </div>
      </Spec>
      <Spec label="The raised sheet (level 2)" caption="At most one per screen, for the thing the screen is about.">
        <div className="px-1 pt-2 pb-1">
          <PaperSheet label="Making time">
            <p className="t-label text-ink-muted">Making time</p>
            <p className="t-number text-ink-primary mt-3">2<span className="t-sub">h</span> 58<span className="t-sub">m</span></p>
            <p className="t-meta mt-4">4 sessions of focused study</p>
          </PaperSheet>
        </div>
      </Spec>
    </Section>
  );
}

function StatesSection() {
  const [failed, setFailed] = useState(true);
  return (
    <Section id="part-states" title="Empty, loading, error">
      <Spec label="Empty" caption="One character, 96 or smaller. One plain line. One action. No background of its own.">
        <EmptyState art={CREW.snoozer} title="There's room to rest." line="Your next blocks will appear here."
          action={<Button kind="main" arrow="forward">Plan your week</Button>} />
      </Spec>
      <Spec label="Loading" caption="Nothing for 300ms, then grey shapes where the content will be. No spinner, nothing that pulses.">
        <LoadingShape rows={3} label="Loading your plan" immediate />
      </Spec>
      <Spec label="Error" caption="A plain sentence where it happened, with the way out as a button.">
        {failed
          ? <ErrorState sentence="We couldn't save your setup. Your answers are still here." onRetry={() => setFailed(false)} />
          : <p className="t-body text-ink-primary">Saved.</p>}
      </Spec>
    </Section>
  );
}

function PartsSheet() {
  return (
    <main className="ui-part min-h-[100dvh] bg-surface-canvas text-ink-primary">
      <header className="px-6 pb-6 frame-page" style={{ '--frame-pad-top': 'var(--space-8)' } as React.CSSProperties}>
        <p className="t-label text-ink-muted">For developers · not in the app</p>
        <h1 className="t-title mt-2">The shared parts</h1>
        <p className="t-sub mt-2">One of each, in every state. components/ui/</p>
      </header>
      <ButtonsSection />
      <ChoosingSection />
      <MenuSection />
      <OverSection />
      <BarsSection />
      <FieldsSection />
      <StatesSection />
      <MessageHost />
    </main>
  );
}

/** A phone screen with the tab bar and a toast showing above it. */
function TabBarScene() {
  React.useEffect(() => { showMessage('Saved to your plan', { action: { label: 'Undo', onPress: () => {} }, duration: 600000 }); }, []);
  return (
    <div className="ui-part flex h-[100dvh] flex-col bg-surface-canvas text-ink-primary">
      <TopBar placeLabel="Tuesday, 24 November" />
      <div className="flex flex-1 flex-col gap-3 overflow-y-auto px-6">
        <h1 className="t-display">Good afternoon, Aoife.</h1>
        <List>
          <Row art={CREW.accounting} title="Accounting" meta="Practice · 45 min" onPress={() => {}} />
          <Row art={CREW.irish} title="Irish" meta="Practice · 45 min" onPress={() => {}} />
        </List>
      </div>
      <TabBar items={PLACES} current="home" onSelect={() => {}} />
      <MessageHost />
    </div>
  );
}

/** A menu button at the very top that prefers to open upwards (it must not go
 *  under the island), or low on the screen above the tab bar. */
function MenuScene({ where }: { where: 'top' | 'low' }) {
  const [subject, setSubject] = useState('all');
  const many = [...SUBJECTS, { value: 'chemistry', label: 'Chemistry' }, { value: 'english', label: 'English' }];
  return (
    <div className="ui-part flex h-[100dvh] flex-col bg-surface-canvas text-ink-primary">
      {where === 'top'
        ? <TopBar leave={{ kind: 'back', onPress: () => {} }} title="Mark Bank" action={<span data-demo="menu"><Menu label="Subject" side="top" value={subject} onChange={setSubject} options={many} /></span>} />
        : <TopBar leave={{ kind: 'back', onPress: () => {} }} title="Mark Bank" />}
      <div className="flex flex-1 flex-col justify-end gap-3 px-6 pb-4">
        {where === 'low' ? <span data-demo="menu"><Menu label="Subject" block value={subject} onChange={setSubject} options={many} /></span> : null}
      </div>
      <TabBar items={PLACES} current="launch" onSelect={() => {}} />
    </div>
  );
}

const root = document.getElementById('root');
if (root) {
  createRoot(root).render(
    <>
      <IllustrationTheme />
      {SCENE === 'tabbar' ? <TabBarScene /> : SCENE === 'menu-top' ? <MenuScene where="top" /> : SCENE === 'menu-low' ? <MenuScene where="low" /> : <PartsSheet />}
    </>,
  );
}
