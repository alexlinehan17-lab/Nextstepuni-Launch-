import { useEffect, useRef, useState, type ReactNode } from 'react';
import { AnimatePresence, motion } from 'motion/react';
import { ChevronDown, ChevronLeft, ChevronRight, Clock3, RotateCcw, SkipForward, SlidersHorizontal } from 'lucide-react';
import { Artwork } from '../learning/shared';
import { SessionTodos } from '../study/SessionTodos';
import { StudySubjectArtwork } from '../study/StudySubjectPicker';
import { DAYS_OF_WEEK as days, getBlockId, toDateKey, type StudyBlock, type WeeklyTimetable } from '../subjectData';
import type { SchoolEvent } from '../gc/GCKeyEvents';
import type { PlanCue, PlanCues } from '../../hooks/usePlanCues';
import { PLAN_TRIGGERS, PLAN_WHY, defaultThen } from '../../planIntentionData';
import { readPlannerTodos, savePlannerTodos } from './plannerTodos';
import { Button, Glyph, IconButton, TextButton } from '../ui/Button';
import { AnswerTick, ChoiceTile, SelectionBar } from '../ui/Choice';
import { PressBox } from '../ui/List';
import { Sheet } from '../ui/Sheet';
import { AreaField } from '../ui/Field';
import './planner.css';

/** A to-do of the next small step (the shape the Kobra PlanCard used: a label, done or not). */
export interface PlanStep { label: string; done?: boolean }
export interface PlannerEntry { block: StudyBlock; day: number; index: number; id: string; dateKey: string; key: string; }
export function plannerEntries(timetable: WeeklyTimetable, weekStart: Date): PlannerEntry[] {
  return timetable.flatMap((day, dayIndex) => day.blocks.map((block, index) => {
    const date = new Date(weekStart); date.setDate(date.getDate() + dayIndex);
    const dateKey = toDateKey(date); const id = getBlockId(block, index);
    return { block, day: dayIndex, index, id, dateKey, key: `${dateKey}|${id}` };
  }));
}
export function workloadLedger(timetable: WeeklyTimetable, subjects: string[]) {
  return subjects.map(subject => ({ subject, minutes: timetable.flatMap(day => day.blocks).filter(block => block.subjectName === subject).reduce((sum, block) => sum + block.durationMinutes, 0) }));
}
const method = { 'new-learning': 'New learning', practice: 'Practice', revision: 'Revision' };
const time = (minutes: number) => minutes < 60 ? `${minutes}m` : `${Math.floor(minutes / 60)}h${minutes % 60 ? ` ${minutes % 60}m` : ''}`;
const dateLabel = (date: Date) => date.toLocaleDateString('en-IE', { day: 'numeric', month: 'short' });
const defaultSteps = (block: StudyBlock): PlanStep[] => block.sessionType === 'practice' ? [
  { label: block.suggestedTopics?.[0] ? `Practise ${block.suggestedTopics[0]}` : 'Choose one question to work through' },
  { label: 'Have a go before checking the answer' }, { label: 'Note one thing to revisit' },
] : [{ label: block.suggestedTopics?.[0] ? `Work through ${block.suggestedTopics[0]}` : 'Choose a manageable piece of work' }, { label: 'Recall it in your own words' }, { label: 'Note what needs another look' }];
/** The to-dos shown before "Show N more" (as the plan card did). */
const VISIBLE_STEPS = 3;

/** The week beside its next small step from 768px (boards r5-planner, c-tools2-planner). Without
 *  matchMedia (a test, an old browser) the page is the wide one, as a laptop browser would be. */
function useBeside() {
  const query = '(min-width: 768px)';
  const [beside, setBeside] = useState(() => typeof window === 'undefined' || typeof window.matchMedia !== 'function' || window.matchMedia(query).matches);
  useEffect(() => {
    if (typeof window.matchMedia !== 'function') return undefined;
    const media = window.matchMedia(query);
    const update = () => setBeside(media.matches);
    media.addEventListener?.('change', update);
    return () => media.removeEventListener?.('change', update);
  }, []);
  return beside;
}

function BlockCue({ subject, saved, onSave }: { subject: string; saved?: PlanCue; onSave: (cue: PlanCue) => void }) {
  const [trigger, setTrigger] = useState(saved?.trigger ?? PLAN_TRIGGERS[0]);
  const [then, setThen] = useState(saved?.then ?? defaultThen(subject));
  const [savedOk, setSavedOk] = useState(!!saved);
  const field = useRef<HTMLTextAreaElement>(null);
  return <details className="pl7-cue"><summary className="pl7-cue-head"><span>Your if-then for this block</span><ChevronDown className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" /></summary>
    <div className="pl7-cue-triggers">{PLAN_TRIGGERS.map(item => <ChoiceTile key={item} compact kind="toggle" chosen={trigger === item} label={item} onClick={() => { setTrigger(item); setSavedOk(false); }} />)}</div>
    <AreaField ref={field} label="Then I’ll…" value={then} onChange={event => { setThen(event.target.value); setSavedOk(false); }} />
    <Button size="sm" missing={then.trim() ? undefined : { sentence: 'Write what you will do first.', goTo: field }} onClick={() => { onSave({ trigger, then: then.trim() }); setSavedOk(true); }}>{savedOk ? 'Saved' : 'Save my if-then'}</Button>
    <p className="pl7-cue-why">{PLAN_WHY.text}<br />{PLAN_WHY.source}</p>
  </details>;
}

export default function PlannerWorkbench({ uid, timetable, subjects, weekStart, weekOffset, onWeekChange, restDays, duration, onSettings, onPlanSettingsChange, isComplete, isSkipped, isDeferred, onComplete, onSkip, onStudy, schoolEvents, hints, cues, onCueSave, explanation }: {
  uid: string; timetable: WeeklyTimetable; subjects: string[]; weekStart: Date; weekOffset: number; onWeekChange: (offset: number) => void;
  restDays: string[]; duration: number; onSettings: () => void; onPlanSettingsChange: (days: string[], minutes: number) => void;
  isComplete: (entry: PlannerEntry) => boolean; isSkipped: (entry: PlannerEntry) => boolean; isDeferred?: (entry: PlannerEntry) => boolean;
  onComplete?: (entry: PlannerEntry, done: boolean) => void; onSkip?: (entry: PlannerEntry, skipped: boolean) => void; onStudy?: (entry: PlannerEntry) => void;
  schoolEvents: SchoolEvent[]; hints: Record<string, { label: string }>; cues: PlanCues; onCueSave: (id: string, cue: PlanCue) => void; explanation: ReactNode; summary?: ReactNode;
}) {
  const entries = plannerEntries(timetable, weekStart);
  const today = toDateKey(new Date());
  const beside = useBeside();
  const [selectedKey, setSelectedKey] = useState<string>();
  const selected = entries.find(entry => entry.key === selectedKey) ?? entries.find(entry => entry.dateKey === today && !isComplete(entry) && !isSkipped(entry)) ?? entries.find(entry => !isComplete(entry) && !isSkipped(entry)) ?? entries[0];
  const [view, setView] = useState('Week');
  const [selectedDay, setSelectedDay] = useState((new Date().getDay() + 6) % 7);
  const [settings, setSettings] = useState(false);
  const [draftRest, setDraftRest] = useState(restDays);
  const [draftDuration, setDraftDuration] = useState(duration);
  const [editing, setEditing] = useState(false);
  const [todos, setTodos] = useState<Record<string, PlanStep[]>>({});
  const [saveError, setSaveError] = useState('');
  const [explain, setExplain] = useState(false);
  // On a phone a tapped block's next small step rises over the week, where you are.
  const [stepOpen, setStepOpen] = useState(false);
  const [moreSteps, setMoreSteps] = useState(false);
  const totalMinutes = entries.reduce((sum, entry) => sum + entry.block.durationMinutes, 0);
  const completed = entries.filter(isComplete).length;
  const ledger = workloadLedger(timetable, subjects);
  const maximum = Math.max(1, ...ledger.map(row => row.minutes));
  const dateFor = (day: number) => { const date = new Date(weekStart); date.setDate(date.getDate() + day); return date; };
  const steps = selected ? todos[selected.key] ?? readPlannerTodos(uid, selected.dateKey, selected.id) ?? defaultSteps(selected.block) : [];
  const openSettings = () => { setDraftRest([...restDays]); setDraftDuration(duration); setSettings(true); };
  const chooseBlock = (entry: PlannerEntry) => { setSelectedKey(entry.key); setSelectedDay(entry.day); setMoreSteps(false); if (!beside) setStepOpen(true); };
  const studyBlocked = !onStudy || (selected ? isSkipped(selected) : true) || editing || settings || explain;
  const study = () => { if (selected && !studyBlocked) onStudy?.(selected); };
  // ⌘↵ (Ctrl+Enter) studies the chosen block, as the plan card's shortcut did; not while
  // something is open over it.
  const studyRef = useRef(study);
  studyRef.current = study;
  useEffect(() => {
    if (!beside && !stepOpen) return undefined;
    const onKey = (event: KeyboardEvent) => {
      if (event.key !== 'Enter' || !(event.metaKey || event.ctrlKey)) return;
      event.preventDefault();
      studyRef.current();
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [beside, stepOpen]);

  const renderBlock = (entry: PlannerEntry) => <PressBox key={entry.key} className="pl7-block" pressed={beside ? selected?.key === entry.key : undefined}
    label={`${entry.block.subjectName} ${method[entry.block.sessionType]} · ${entry.block.durationMinutes} minutes`} onPress={() => chooseBlock(entry)}>
    <StudySubjectArtwork subject={entry.block.subjectName} size={52} />
    <span className="pl7-block-copy"><span className="pl7-block-name">{entry.block.subjectName}</span><span className="pl7-block-meta">{method[entry.block.sessionType]} · {entry.block.durationMinutes} min</span></span>
    {isComplete(entry) ? <span className="pl7-block-state" aria-label="Completed"><AnswerTick /></span>
      : isSkipped(entry) ? <SkipForward aria-label="Skipped" className="pl7-block-state ui-icon" width={20} height={20} strokeWidth={1.75} />
        : <ChevronRight className="pl7-block-chev ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" />}
  </PressBox>;
  const dayEvents = (day: number) => schoolEvents.filter(event => event.date === toDateKey(dateFor(day))).map(event => <p className="pl7-event" key={event.id}>{event.title}</p>);
  const shownSteps = moreSteps ? steps : steps.slice(0, VISIBLE_STEPS);

  // The chosen block's next small step: beside the week on a laptop, in a sheet on a phone.
  const step = selected ? <aside className="pl7-step" aria-label="Selected study block">
    <AnimatePresence mode="wait"><motion.div key={selected.key} className="pl7-step-inner" initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} transition={{ duration: .2 }}>
      {beside ? <p className="t-label pl7-step-label">{days[selected.day]} · Your next small step</p> : null}
      <div className="pl7-step-head">
        <StudySubjectArtwork subject={selected.block.subjectName} size={beside ? 112 : 120} />
        <h2 className="t-name">{selected.block.subjectName}</h2>
        <p className="t-sub">{method[selected.block.sessionType]} · {selected.block.durationMinutes} minutes</p>
        <p className="t-meta pl7-prompt">{hints[selected.block.subjectName]?.label ?? (selected.block.suggestedTopics?.join(', ') || 'Choose a manageable piece of work. Give it your attention.')}</p>
      </div>
      <div className="pl7-todo-head"><span className="t-label">To-dos · {steps.length}</span><TextButton onClick={() => setEditing(true)}>Edit to-dos</TextButton></div>
      <ul className="pl7-todos">{shownSteps.map((item, index) => <li key={`${index}-${item.label}`} data-done={item.done || undefined}><span className="pl7-todo-mark" aria-hidden="true" />{item.label}</li>)}</ul>
      {steps.length > VISIBLE_STEPS ? <TextButton tone="quiet" aria-expanded={moreSteps} onClick={() => setMoreSteps(value => !value)}>{moreSteps ? 'Show fewer' : `Show ${steps.length - VISIBLE_STEPS} more`}</TextButton> : null}
      <div className="pl7-state">
        <span className="pl7-ready">{isComplete(selected) ? <><AnswerTick />Completed</> : isSkipped(selected) ? <><Glyph icon={SkipForward} size={16} />Skipped this time</> : <><Glyph icon={Clock3} size={16} />Ready when you are</>}</span>
        {isComplete(selected) ? onComplete && <Button size="sm" onClick={() => onComplete(selected, false)}><span className="pl7-inline"><Glyph icon={RotateCcw} size={16} />Undo</span></Button>
          : isSkipped(selected) ? isDeferred?.(selected) && onSkip && <Button size="sm" onClick={() => onSkip(selected, false)}><span className="pl7-inline"><Glyph icon={RotateCcw} size={16} />Undo</span></Button>
            : <>{onComplete && <Button size="sm" onClick={() => onComplete(selected, true)}>Already studied</Button>}{onSkip && <Button size="sm" aria-label="Skip this block" onClick={() => onSkip(selected, true)}>Skip</Button>}</>}
      </div>
      <BlockCue key={selected.id} subject={selected.block.subjectName} saved={cues[selected.id]} onSave={cue => onCueSave(selected.id, cue)} />
      {beside ? <Button kind="main" size="lg" block arrow="forward" className="pl7-study" aria-label="Study this block"
        unavailable={onStudy && isSkipped(selected) ? 'You skipped this block. Undo to study it.' : undefined} onClick={study}>
        <span className="pl7-study-label">Study this block<span className="pl7-keys t-readout" aria-hidden="true">⌘ ↵</span></span>
      </Button> : null}
    </motion.div></AnimatePresence>
  </aside> : <p className="t-sub pl7-rest">There’s room to rest. Your next blocks will appear here.</p>;

  return <div className="pl7-planner"><div className="pl7-main">
    <div className="pl7-cols">
      <div className="pl7-week-col">
        <div className="pl7-intro"><h1 className="t-title">A little room for what’s next.</h1><p className="t-sub">Your week, in manageable blocks.</p></div>
        <div className="pl7-weekbar">
          <div className="pl7-weeknav">
            <IconButton className="pl7-arrow" label="Previous timetable week" icon={<Glyph icon={ChevronLeft} size={20} />} aria-disabled={weekOffset <= 0 || undefined} onClick={() => { if (weekOffset > 0) onWeekChange(weekOffset - 1); }} />
            <div className="pl7-weekname" aria-live="polite"><span className="t-meta">{weekOffset === 0 ? 'The week ahead' : 'Looking ahead'} · {completed} of {entries.length} done</span><h2 className="pl7-weekdates">{dateLabel(weekStart)} to {dateLabel(dateFor(6))}</h2></div>
            <IconButton className="pl7-arrow" label="Next timetable week" icon={<Glyph icon={ChevronRight} size={20} />} onClick={() => onWeekChange(weekOffset + 1)} />
          </div>
          <a className="pl7-jump t-readout" href="#workload">{entries.length} blocks · {time(totalMinutes)}</a>
        </div>
        {weekOffset !== 0 && <TextButton className="pl7-thisweek" onClick={() => onWeekChange(0)}>This week</TextButton>}
        <div className="pl7-viewbar">
          <SelectionBar label="Planner view" size="md" className="pl7-seg" value={view} onChange={next => setView(next)} options={[{ value: 'Week', label: 'Week' }, { value: 'Day', label: 'Day' }]} />
          <Button size="sm" onClick={openSettings}><span className="pl7-inline"><Glyph icon={SlidersHorizontal} size={16} />Plan settings</span></Button>
        </div>
        <section className="pl7-agenda" aria-label="Your study schedule">
          {view === 'Week' ? <>
            <motion.div className="pl7-days" key={weekOffset} initial={{ opacity: 0, y: 7 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: .3 }}>{days.map((day, index) => {
              const dayEntries = entries.filter(entry => entry.day === index);
              const events = dayEvents(index);
              if (!dayEntries.length && !events.length) return null;
              const isToday = toDateKey(dateFor(index)) === today;
              return <section className="pl7-day" key={day} aria-label={`${day} ${dateFor(index).getDate()}`}>
                <header className="pl7-day-head"><button type="button" className="pl7-day-name" onClick={() => { setSelectedDay(index); setView('Day'); }}>{day} {dateFor(index).getDate()}</button>{isToday ? <span className="pl7-today">Today</span> : null}<span className="pl7-day-time t-readout">{dayEntries.length ? time(dayEntries.reduce((sum, entry) => sum + entry.block.durationMinutes, 0)) : 'School calendar'}</span></header>
                {events}
                <div className="pl7-blocks">{dayEntries.map(renderBlock)}</div>
              </section>;
            })}</motion.div>
            {!entries.length && !days.some((_, index) => dayEvents(index).length) && <div className="pl7-empty"><h2 className="t-heading">No study blocks planned this week.</h2><p className="t-sub">Adjust your plan when you’re ready to make some time.</p><Button onClick={openSettings}>Plan settings</Button></div>}
          </> : <>
            <div className="pl7-dayrail" role="group" aria-label="Choose a day">{days.map((day, index) => <button type="button" key={day} aria-pressed={selectedDay === index} onClick={() => { setSelectedDay(index); const first = entries.find(entry => entry.day === index); if (first) setSelectedKey(first.key); }}><span>{day.slice(0, 3)}</span><strong>{dateFor(index).getDate()}</strong><i data-rest={restDays.includes(day) || undefined} /></button>)}</div>
            <div className="pl7-daytitle"><p className="t-label">{days[selectedDay]} · {dateLabel(dateFor(selectedDay))}</p><h2 className="t-heading">{entries.some(entry => entry.day === selectedDay) ? 'One thing at a time.' : 'Today has a little more space.'}</h2><p className="t-sub">{restDays.includes(days[selectedDay]) ? 'Rest is part of the plan.' : 'Take the blocks in your own time.'}</p></div>{dayEvents(selectedDay)}
            {entries.some(entry => entry.day === selectedDay) ? <div className="pl7-blocks">{entries.filter(entry => entry.day === selectedDay).map(renderBlock)}</div> : <div className="pl7-restday"><Artwork src="/assets/star-crew/companions/thinker.png" size={160} transparentBackground /><Button onClick={openSettings}>Adjust rest days</Button></div>}
          </>}
        </section>
      </div>
      {beside ? step : null}
    </div>
    <section className="pl7-workload" id="workload" aria-label="The balance of your week">
      <div className="pl7-ledger-head"><h3 className="t-heading">The balance of your week</h3><span className="t-meta">Planned time</span></div>
      <ul className="pl7-ledger">{ledger.map(row => <li className="pl7-ledger-row" key={row.subject}><StudySubjectArtwork subject={row.subject} size={40} /><span className="pl7-ledger-name">{row.subject}</span><span className="pl7-ledger-track" aria-hidden="true"><motion.i initial={false} animate={{ width: `${row.minutes / maximum * 100}%` }} transition={{ duration: .5 }} /></span><span className="pl7-ledger-time t-readout">{time(row.minutes)}</span></li>)}</ul>
      <TextButton className="pl7-explain-toggle" aria-expanded={explain} onClick={() => setExplain(value => !value)}><span className="pl7-inline">Behind your plan<ChevronDown className="ui-icon pl7-chev" data-open={explain || undefined} width={16} height={16} strokeWidth={2} aria-hidden="true" /></span></TextButton>
      {explain && <div className="pl7-explanation">{explanation}</div>}
    </section>
    {!beside && selected ? <Sheet open={stepOpen} onClose={() => setStepOpen(false)} title={`${days[selected.day]} · Your next small step`} titleSize="small" className="pl7-step-sheet"
      footer={<Button kind="main" size="lg" block arrow="forward" aria-label="Study this block" unavailable={onStudy && isSkipped(selected) ? 'You skipped this block. Undo to study it.' : undefined} onClick={study}>Study this block</Button>}>
      {step}
    </Sheet> : null}
    <Sheet open={settings} onClose={() => setSettings(false)} title="Make room for your week." titleSize="small" save={{ label: 'Save', onPress: () => { onPlanSettingsChange(draftRest, draftDuration); setSettings(false); } }} className="pl7-settings">
      <p className="t-sub">Choose the days that work for you and a manageable block length.</p>
      <fieldset className="pl7-rest"><legend className="t-label">Rest days</legend>
        <div className="pl7-rest-days">{days.map(day => <ChoiceTile key={day} kind="several" compact chosen={draftRest.includes(day)} label={day} onClick={() => setDraftRest(previous => previous.includes(day) ? previous.filter(item => item !== day) : [...previous, day])} />)}</div>
      </fieldset>
      <label className="pl7-duration"><span className="t-body">Minutes per block</span><select className="ui-field-input pl7-select" value={draftDuration} onChange={event => setDraftDuration(Number(event.target.value))}>{[...new Set([25, 30, 45, 60, 90, duration])].sort((a, b) => a - b).map(minutes => <option key={minutes} value={minutes}>{minutes} minutes</option>)}</select></label>
      <TextButton arrow="forward" onClick={() => { setSettings(false); onSettings(); }}>Edit subjects and grades</TextButton>
    </Sheet>
    {editing && selected && <SessionTodos key={selected.key} steps={steps} onClose={() => setEditing(false)} onSave={next => { setTodos(previous => ({ ...previous, [selected.key]: next })); const ok = savePlannerTodos(uid, selected.dateKey, selected.id, next); setSaveError(ok ? '' : 'Your to-dos are available for this visit, but could not be saved on this device.'); setEditing(false); }} />}
    {saveError && <p role="alert" className="t-sub">{saveError}</p>}
  </div></div>;
}
