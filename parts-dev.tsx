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
import { ChartNoAxesColumn, ChevronLeft, Compass, Ellipsis, House, Map, Search, SlidersHorizontal, Timer } from 'lucide-react';
import IllustrationTheme from './components/IllustrationTheme';
import { Arrow, Button, Glyph, IconButton, TextButton } from './components/ui/Button';
import { ChoiceGroup, SelectionBar, SelectionMark, SelectionWords, Switch } from './components/ui/Choice';
import { Menu, MenuAction, MenuLabel, MenuPanel, MenuRadioRows, MenuSegment, MenuSwitch } from './components/ui/Menu';
// The subject button's own look (Mark Bank), shown as the menu's button on the sheet.
import './components/MarkBank/mark-bank-library.css';
import { Confirm, Sheet } from './components/ui/Sheet';
import { MessageHost, showMessage } from './components/ui/Message';
import { PinnedFooter, TabBar, TopBar } from './components/ui/Bars';
import { Field, SearchField } from './components/ui/Field';
import { CheckRow, List, PaperSheet, PressBox, Row } from './components/ui/List';
import { EmptyState, ErrorState, LoadingShape } from './components/ui/States';
import { ChoiceTile } from './components/ui/Choice';
import { AreaField } from './components/ui/Field';
import { AnswerGroup, AnswerLine, ExercisePart, ExerciseSheet, RevealCard } from './components/learning/Exercise';

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
  const [period, setPeriod] = useState('week');
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
      <Spec label="Moving between the parts of a screen" caption="A menu button with a count, never a bar. Full width, the count stands at the end in the mono and the parts are numbered.">
        <Line><Menu label="Progress section" count value={section} onChange={setSection} options={SECTIONS} /></Line>
        <Menu label="Progress section" count numbered block value={section} onChange={setSection} options={SECTIONS} />
      </Spec>
      <Spec label="Choices as words" caption="Week, Month and Year; the Fieldbook's pages. The current word is ink with a short ink line under it; no tray.">
        <SelectionWords label="Period" value={period} onChange={setPeriod} options={[{ value: 'week', label: 'Week' }, { value: 'month', label: 'Month' }, { value: 'year', label: 'Year' }]} />
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
      <Spec label="A row that opens a menu" caption="face: the button shows its own words instead of the value (Find a starting point on Modules, on a laptop). Choosing still applies at once.">
        <Menu label="Find a starting point" block value="none" onChange={() => {}} face={<span className="ui-row-body"><span className="ui-row-title">Find a starting point</span><span className="ui-row-meta">Start from what you need help with</span></span>}
          options={[{ value: 'remember', label: 'I forget what I study' }, { value: 'start', label: 'I keep putting it off' }]} />
      </Spec>
      <Spec label="A menu of a screen's tools" caption="MenuPanel (the paper viewer's Tools on a laptop): the phone's Tools sheet as a menu under its button. A switch turns a thing on and the menu stays open; a row with a chevron opens it; up-right leaves the app.">
        <Line><span data-demo="menu-panel"><MenuPanelDemo /></span></Line>
      </Spec>
      <Spec label="A box that opens a menu of choices" caption="MenuPanel with the screen's own box as its button (Mark Bank's subject and level on a laptop): a selection bar (MenuSegment) and rows with a character (MenuRadioRows), the current one ticked. Choosing applies at once.">
        <Line><span data-demo="menu-choices"><MenuChoicesDemo /></span></Line>
      </Spec>
    </Section>
  );
}

function MenuChoicesDemo() {
  const [level, setLevel] = useState<'higher' | 'ordinary'>('higher');
  const [subject, setSubject] = useState('biology');
  const names: Record<string, string> = { accounting: 'Accounting', biology: 'Biology', chemistry: 'Chemistry' };
  return (
    <MenuPanel label="Change subject or level" buttonLabel={`Change subject or level: ${names[subject]}`} align="start" buttonClassName="mb-subject" className="mb-subject-menu"
      face={<><span className="mb-subject-art" aria-hidden="true"><img src={CREW.accounting} alt="" /></span><span className="mb-subject-copy"><span className="t-name-sm">{names[subject]}</span><span className="t-meta">{level === 'higher' ? 'Higher' : 'Ordinary'} level</span></span></>}>
      <MenuLabel>Paper level</MenuLabel>
      <MenuSegment label="Paper level" value={level} onChange={value => setLevel(value === 'ordinary' ? 'ordinary' : 'higher')} options={[{ value: 'higher', label: 'Higher' }, { value: 'ordinary', label: 'Ordinary' }]} />
      <MenuLabel>Your subjects</MenuLabel>
      <MenuRadioRows label="Your subjects" value={subject} onChange={setSubject}
        options={Object.entries(names).map(([value, label]) => ({ value, label, art: <img src={CREW.accounting} alt="" /> }))} />
    </MenuPanel>
  );
}

function MenuPanelDemo() {
  const [self, setSelf] = useState(true);
  const [words, setWords] = useState(true);
  return (
    <MenuPanel label="Tools" buttonLabel="Study tools for this paper" head="Tools" status={`${[self, words].filter(Boolean).length} on`}
      face={<><SlidersHorizontal className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" />Tools</>}>
      <MenuSwitch title="Save this paper" meta="Keeps it in Saved papers" checked={false} onChange={() => {}} />
      <MenuAction title="Download the paper" meta="Opens in your browser · PDF · 1.3 MB" href="#download" />
      <MenuLabel>Switch on</MenuLabel>
      <MenuSwitch title="Self-mark" meta="Score yourself against the scheme" checked={self} onChange={setSelf} />
      <MenuSwitch title="Command words" meta="Decode what each question demands" checked={words} onChange={setWords} />
      <MenuLabel>Start</MenuLabel>
      <MenuAction title="Triage" meta="Rate each question before you start" onPress={() => {}} />
    </MenuPanel>
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
          <Button onClick={() => setOpen('bare')}>Bare sheet (the quick tour)</Button>
          <Button onClick={() => setOpen('plain')}>Plain sheet (Finish for now)</Button>
          <Button onClick={() => setOpen('card')}>Sheet with its own headline (a tile's card)</Button>
          <Button onClick={() => setOpen('notes')}>Sheet with its title at the left and a status (a module's Notes)</Button>
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
      <Sheet open={open === 'bare'} bare title="Quick tour" onClose={close}
        footer={<div className="ui-pair"><Button size="lg" onClick={close}>Skip</Button><Button kind="main" size="lg" block arrow="forward" onClick={close}>Next</Button></div>}>
        <p className="t-label text-ink-muted">Quick tour · 1 of 3</p>
        <h3 className="t-heading text-ink-primary">Your lessons live here</h3>
        <p className="t-sub">A bare sheet carries its own words and its own way out: no handle, no header. On a laptop the same words sit in a popover (.ui-pop) beside what they point at.</p>
      </Sheet>
      <Sheet open={open === 'plain'} plain title="Finish for now?" onClose={close}
        footer={<><Button kind="main" size="lg" block arrow="forward" onClick={close}>End and keep 17 min</Button><Button size="lg" block onClick={close}>Keep studying</Button><TextButton tone="danger" onClick={close}>Discard without saving</TextButton></>}>
        <p className="t-sub">A plain sheet: the handle and the title at the left, no Close; its own choices are the way out.</p>
      </Sheet>
      <Sheet open={open === 'card'} hideTitle title="The branch library" onClose={close}
        footer={<Button kind="main" size="lg" block arrow="forward" onClick={close}>Build another · 180 JP</Button>}>
        <p className="t-label text-ink-muted">Part of your world</p>
        <h3 className="t-title text-ink-primary">The branch library</h3>
        <p className="t-sub">hideTitle: the body opens with its own headline, so the head shows only Close; the title stays the sheet's name for screen readers.</p>
      </Sheet>
      <Sheet open={open === 'notes'} titleAlign="start" titleSize="small" status="Saved" title="Notes" onClose={close}>
        <p className="t-sub">titleAlign start: the title sits at the left beside Close. status: a quiet word at the right of the head that says how things stand; notes save as you type, so there is no Done.</p>
      </Sheet>
      <Confirm open={open === 'confirm'} sentence="Delete your account?"
        detail="Everything you have studied, planned and saved is erased and cannot be brought back."
        keepLabel="Keep my account" onKeep={close} dangerLabel="Delete account" onDanger={close} />
    </Section>
  );
}

function CheckRowDemo() {
  const [done, setDone] = useState(false);
  return <CheckRow checked={done} onChange={setDone} mark={<SelectionMark on={done} shape="square" />}>2024 Paper 1, Question 6</CheckRow>;
}

function BarsSection() {
  const [need, setNeed] = useState(true);
  const [island, setIsland] = useState('island');
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
      <Spec label="A place that has become a task" caption="Study set-up once something is chosen: Cancel clears the choices and gives the place (and the tab bar, via useFrameTask) back.">
        <div className="border border-dashed border-outline-soft"><TopBar leave={{ kind: 'cancel', onPress: () => {} }} placeLabel="The Study Room" /></div>
      </Spec>
      <Spec label="A place's bar on a laptop, with a control in the middle" caption="The island: one quiet action at the left end (lead), the selection bar midway between the bar's ends (center), the points at the right. Balanced neighbours make it read as centred.">
        <div className="border border-dashed border-outline-soft"><TopBar lead={<TextButton tone="quiet">How it works</TextButton>}
          center={<SelectionBar label="Journey sections" value={island} onChange={setIsland} options={[{ value: 'island', label: 'Island' }, { value: 'build', label: 'Build' }, { value: 'fieldbook', label: 'Fieldbook' }, { value: 'year', label: 'Your year' }]} />}
          action={<Button size="sm"><span className="ui-readout">5,065 JP</span></Button>} /></div>
      </Spec>
      <Spec label="A row you tick" caption="CheckRow: the whole row is the checkbox, with the screen's own mark (Time's up: the session's dotted ring).">
        <CheckRowDemo />
      </Spec>
      <Spec label="An over-screen with its own controls, on a phone" caption="below: a second row inside the bar, under the name (the paper viewer: Paper or Scheme beside its Answers switch).">
        <div className="border border-dashed border-outline-soft"><TopBar ruled leave={{ kind: 'close', onPress: () => {}, label: 'Close viewer' }} over="2025 · Higher · Exam Paper" title="Physics"
          action={<IconButton label="Study tools for this paper" icon={<Glyph icon={SlidersHorizontal} />} />}
          below={<><SelectionBar label="Paper or marking scheme" size="md" className="flex-1" value="paper" onChange={() => {}} options={[{ value: 'paper', label: 'Paper' }, { value: 'scheme', label: 'Scheme' }]} /><label className="ui-switch-row"><span>Answers</span><Switch checked onChange={() => {}} label="Answers" /></label></>} /></div>
      </Spec>
      <Spec label="The same over-screen on a laptop" caption="A title and a centre control together: the name at the left beside Close, the control centred between two equal zones, the actions at the right.">
        <div className="border border-dashed border-outline-soft"><TopBar ruled leave={{ kind: 'close', onPress: () => {}, label: 'Close viewer' }} over="2025 · Higher · Exam Paper" title="Physics"
          center={<SelectionBar label="Paper or marking scheme" size="md" value="paper" onChange={() => {}} options={[{ value: 'paper', label: 'Paper' }, { value: 'scheme', label: 'Scheme' }]} />}
          action={<IconButton label="Study tools for this paper" icon={<Glyph icon={SlidersHorizontal} />} />} /></div>
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
          <PinnedFooter ruled lead={<>Next: <span className="text-ink-primary">Your New OS</span></>} note="Your answers stay as you go back">
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
  const [rowOpen, setRowOpen] = useState(false);
  return (
    <Section id="part-fields" title="Field, rows, the sheet, the box">
      <Spec label="A field">
        <Field label="First name" placeholder="Aoife" autoComplete="given-name" enterKeyHint="next" help="This is the name we greet you with." />
        <Field label="Email" defaultValue="aoife@glenrua.ie" type="email" inputMode="email" autoComplete="email" data-force="focus" />
        <Field label="School code" defaultValue="GLEN20" autoCapitalize="characters" error="That code is not one we know. Check it with your teacher and type it again." />
      </Spec>
      <Spec label="Search"><SearchField label="Search topics" placeholder="Search topics" /></Spec>
      <Spec label="Rows" caption="At least 56 tall, kept apart by a hairline. A row that opens something ends in a chevron; one that shows something ends in its value; a row with a switch has no chevron. The art may be a drawn element (a subject's character), and a row may carry its own accessible name.">
        <List>
          <Row art={CREW.accounting} title="Accounting" meta={<>Practice · 45 min · <span className="text-accent-text">Up next</span></>} onPress={() => {}} />
          <Row title="Sessions this week" value="6 / 8" />
          <Row external href="#download" title="Download the paper" meta="Opens in your browser · PDF · 1.3 MB" />
          <Row title="Offer me questions when I finish" trailing={<Switch checked={on} onChange={setOn} label="Offer me questions when I finish" />} />
          <Row art={<img src={CREW.irish} alt="" />} title="Irish" meta="Practice · 45 min" label="Study Irish: Practice, 45 minutes" onPress={() => {}} />
        </List>
      </Spec>
      <Spec label="Rows with a number, a bar and a count" caption="A topic in a list (Mark Bank): its number in the readout at the left, a 3px ink bar under the name for the share tried, the count at the right. Chosen in place, with its detail beside the list on a laptop: an ink outline and no chevron.">
        <List>
          <Row lead="2.1" title="Enzymes" progress={41 / 151} value="41 / 151" onPress={() => {}} />
          <Row lead="02" title="Structures and Processes of Life" progress={104 / 2023} meta="19 topics · 104 of 2,023 tried" onPress={() => {}} />
          <Row lead="2.2" title="Photosynthesis" progress={24 / 138} value="24 / 138" selected onPress={() => {}} />
          <Row lead="2.2" title="Respiration" progress={9 / 129} value="9 / 129" selected={false} onPress={() => {}} />
        </List>
      </Spec>
      <Spec label="Rows that move forward or open in place" caption="The next part of a screen ends in an arrow (it moves forward). A row that opens under itself ends in a chevron-down that turns up while it is open.">
        <List>
          <Row over="Next · 2 of 5" title="Study" forward onPress={() => {}} />
          <Row title="Latest practice mock" meta="24 Nov · one sitting recorded so far" value="506 points" expanded={rowOpen} onPress={() => setRowOpen(open => !open)} />
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
        <PressBox expanded={false} onPress={() => {}}><span className="t-row block">9 modules finished</span><span className="t-meta">expanded: it opens a list in place under itself (a world's finished modules)</span></PressBox>
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

/** Area 5b: the pieces an exercise in a module is made of (boards c-read-flow, c-read-choices, c-read-write). */
const REASONS = [
  { text: "I didn't use the right study method.", control: true },
  { text: "I'm just naturally bad at this subject.", control: false },
  { text: 'The test was unfairly hard.', control: false },
  { text: "I didn't put in enough focused effort.", control: true },
];
function ExerciseSection() {
  const [choice, setChoice] = useState<Record<string, boolean>>({ [REASONS[0].text]: true, [REASONS[2].text]: true });
  const [pair, setPair] = useState<number | null>(1);
  const [turned, setTurned] = useState<number[]>([1]);
  const [text, setText] = useState("I'm not a maths person yet.");
  const flip = (i: number) => setTurned(t => (t.includes(i) ? t.filter(x => x !== i) : [...t, i]));
  return (
    <Section id="part-exercise" title="An exercise in a module">
      <Spec label="The sheet, answers you choose" caption="The page's one lifted sheet. A chosen answer has an ink outline and its tick draws; under it, the module's own words on an ink line, with a green tick where the answer is right. The count is read from the answers. Arrow keys move within the group.">
        <ExerciseSheet title="Control Panel" sub="Scenario: You fail a test. Which of these reasons are actually within your control?">
          <AnswerGroup kind="several" count>
            {REASONS.map(r => (
              <ChoiceTile key={r.text} kind="several" chosen={!!choice[r.text]} label={r.text}
                note={choice[r.text] ? (r.control ? '(CONTROLLABLE)' : '(UNCONTROLLABLE)') : undefined} noteTone={r.control ? 'ok' : 'plain'}
                onClick={() => setChoice(c => ({ ...c, [r.text]: !c[r.text] }))} />
            ))}
          </AnswerGroup>
          <ExercisePart label="Pick one" title="When I fail at something...">
            <AnswerGroup kind="one" columns={2}>
              {["A) I feel like I'm a failure.", 'B) I feel like I need to try a new strategy.'].map((t, i) => (
                <ChoiceTile key={t} tile chosen={pair === i} label={t} onClick={() => setPair(i)} />
              ))}
            </AnswerGroup>
          </ExercisePart>
        </ExerciseSheet>
      </Spec>
      <Spec label="An answer you write" caption="The field takes the quiet ink edge while it is in use. The line under it is ink, with a green tick.">
        <ExerciseSheet label="Growth Mindset Activity" title={'The "Yet" Reframe Challenge'} sub={'Upgrade this fixed thought into a growth mindset statement using the power of "yet".'}>
          <AreaField label="Your Reframe" value={text} onChange={e => setText(e.target.value)} placeholder="Rewrite this using the word 'yet'..." data-force="focus" />
          {text.toLowerCase().includes('yet') ? <AnswerLine><b>Reframe complete.</b> You've opened up the possibility of future growth.</AnswerLine> : null}
        </ExerciseSheet>
      </Spec>
      <Spec label="A card you press to turn it over" caption="A white box with a line. Turned, the old words are struck through above the new ones, in ink, with a green tick: no orange or green panel.">
        <div className="flex flex-col gap-2">
          {[["I failed the test because I am stupid.", 'I failed the test because my study strategy for this topic was ineffective.'], ["I'm just naturally bad at Maths.", "I haven't found an effective way to learn Maths yet."]].map(([a, b], i) => (
            <RevealCard key={a} revealed={turned.includes(i)} onPress={() => flip(i)} before={`"${a}"`} after={`"${b}"`} hint="Tap to reframe" done="Reframed" />
          ))}
        </div>
      </Spec>
      <Spec label="Lines that answer" caption="Ink words. The tick beside them is the only green; a note has no tick.">
        <AnswerLine>You just turned a verdict into data.</AnswerLine>
        <AnswerLine tone="note">Result: You're leaning towards Growth, with some Fixed-Mindset code still running.</AnswerLine>
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
      <ExerciseSection />
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
