import { useState, type ReactNode } from 'react';
import { AnimatePresence, motion } from 'motion/react';
import { ArrowDown, ArrowUpRight, Check, ChevronDown, ChevronLeft, ChevronRight, Clock3, RotateCcw, Settings2, SkipForward } from 'lucide-react';
import KobraScope from '../approved-ui-runtime';
import { Button } from '../approved-ui-runtime';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '../approved-ui-runtime';
import { PlanCard, type PlanStep } from '../approved-ui-runtime';
import { Checkbox } from '../approved-ui-runtime';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from '../approved-ui-runtime';
import { Artwork, Eyebrow } from '../learning/shared';
import { BrandBook } from '../learning/BrandBook';
import { SessionTodos } from '../study/SessionTodos';
import { StudySubjectArtwork } from '../study/StudySubjectPicker';
import { DAYS_OF_WEEK as days, getBlockId, toDateKey, type StudyBlock, type WeeklyTimetable } from '../subjectData';
import type { SchoolEvent } from '../gc/GCKeyEvents';
import type { PlanCue, PlanCues } from '../../hooks/usePlanCues';
import { PLAN_TRIGGERS, PLAN_WHY, defaultThen } from '../../planIntentionData';
import { readPlannerTodos, savePlannerTodos } from './plannerTodos';
import '../learning/planner-preview.css';
import './planner-workbench.css';

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

function BlockCue({ subject, saved, onSave }: { subject: string; saved?: PlanCue; onSave: (cue: PlanCue) => void }) {
  const [trigger, setTrigger] = useState(saved?.trigger ?? PLAN_TRIGGERS[0]);
  const [then, setThen] = useState(saved?.then ?? defaultThen(subject));
  const [savedOk, setSavedOk] = useState(!!saved);
  return <details className="pp-cue"><summary>Your if-then for this block</summary><div className="pp-cue-triggers">{PLAN_TRIGGERS.map(item => <Button key={item} variant="outline" size="sm" aria-pressed={trigger === item} onClick={() => { setTrigger(item); setSavedOk(false); }}>{item}</Button>)}</div><label>Then I’ll…<textarea value={then} onChange={event => { setThen(event.target.value); setSavedOk(false); }} /></label><Button className="nsu-ink-outline" variant="outline" disabled={!then.trim()} onClick={() => { onSave({ trigger, then: then.trim() }); setSavedOk(true); }}>{savedOk ? 'Saved' : 'Save my if-then'}</Button><p>{PLAN_WHY.text}<br />{PLAN_WHY.source}</p></details>;
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
  const totalMinutes = entries.reduce((sum, entry) => sum + entry.block.durationMinutes, 0);
  const completed = entries.filter(isComplete).length;
  const ledger = workloadLedger(timetable, subjects);
  const maximum = Math.max(1, ...ledger.map(row => row.minutes));
  const dateFor = (day: number) => { const date = new Date(weekStart); date.setDate(date.getDate() + day); return date; };
  const steps = selected ? todos[selected.key] ?? readPlannerTodos(uid, selected.dateKey, selected.id) ?? defaultSteps(selected.block) : [];
  const openSettings = () => { setDraftRest([...restDays]); setDraftDuration(duration); setSettings(true); };
  const chooseBlock = (entry: PlannerEntry) => { setSelectedKey(entry.key); setSelectedDay(entry.day); };
  const renderBlock = (entry: PlannerEntry) => <button type="button" key={entry.key} className="pp-block" data-selected={selected?.key === entry.key} data-status={isComplete(entry) ? 'done' : isSkipped(entry) ? 'skipped' : undefined} aria-label={`${entry.block.subjectName} ${method[entry.block.sessionType]} · ${entry.block.durationMinutes} minutes`} aria-pressed={selected?.key === entry.key} onClick={() => chooseBlock(entry)}>
    <StudySubjectArtwork subject={entry.block.subjectName} size={48} /><span className="pp-block-copy"><strong>{entry.block.subjectName}</strong><span>{method[entry.block.sessionType]} <i>·</i> {entry.block.durationMinutes} min</span></span>
    {isComplete(entry) ? <span className="pp-done" aria-label="Completed"><Check /></span> : isSkipped(entry) ? <SkipForward aria-label="Skipped" className="pp-status-icon" /> : <ArrowUpRight className="pp-block-arrow" />}
  </button>;
  const dayEvents = (day: number) => schoolEvents.filter(event => event.date === toDateKey(dateFor(day))).map(event => <p className="pp-school-event" key={event.id}>{event.title}</p>);
  return <KobraScope className="nsu-planner"><div className="pp-main">
    <div className="pp-intro"><div><Eyebrow>Your Launchpad / The Planner</Eyebrow><h1>A little room for what’s next.</h1><p>Your week, in manageable blocks.</p></div><Artwork src="/assets/tools/planner.png" size={132} /></div>
    <div className="pp-week-toolbar"><div className="pp-week-navigation"><Button variant="outline" size="icon" aria-label="Previous timetable week" disabled={weekOffset <= 0} onClick={() => onWeekChange(weekOffset - 1)}><ChevronLeft /></Button><div aria-live="polite"><span>{weekOffset === 0 ? 'The week ahead' : 'Looking ahead'}</span><h2>{dateLabel(weekStart)} — {dateLabel(dateFor(6))}</h2></div><Button variant="outline" size="icon" aria-label="Next timetable week" onClick={() => onWeekChange(weekOffset + 1)}><ChevronRight /></Button>{weekOffset !== 0 && <Button variant="ghost" onClick={() => onWeekChange(0)}>This week</Button>}</div><div className="pp-toolbar-actions"><a href="#workload">{entries.length} blocks · {time(totalMinutes)}<ArrowDown /></a><Button variant="outline" onClick={openSettings}><Settings2 />Plan settings</Button></div></div>
    <div className="pp-layout"><section className="pp-agenda" aria-label="Your study schedule"><Tabs className="pp-tabs" value={view} onValueChange={value => setView(String(value))}><div className="pp-agenda-heading"><TabsList aria-label="Planner view"><TabsTrigger value="Week">Week</TabsTrigger><TabsTrigger value="Day">Day</TabsTrigger></TabsList><span>{completed} of {entries.length} blocks complete</span></div>
      <TabsContent value="Week"><motion.div className="pp-week-grid" key={weekOffset} initial={{ opacity: 0, y: 7 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: .3 }}>{days.map((day, index) => {
        const dayEntries = entries.filter(entry => entry.day === index);
        const events = dayEvents(index);
        if (!dayEntries.length && !events.length) return null;
        return <section className="pp-day" key={day}><header><button onClick={() => { setSelectedDay(index); setView('Day'); }}>{day}<span>{dateFor(index).getDate()}</span></button><small>{dayEntries.length ? time(dayEntries.reduce((sum, entry) => sum + entry.block.durationMinutes, 0)) : 'School calendar'}</small></header>{events}<div className="pp-day-blocks">{dayEntries.map(renderBlock)}</div></section>;
      })}</motion.div>{!entries.length && !days.some((_, index) => dayEvents(index).length) && <div className="pp-empty-week"><h2>No study blocks planned this week.</h2><p>Adjust your plan when you’re ready to make some time.</p><Button variant="outline" onClick={openSettings}>Plan settings</Button></div>}</TabsContent>
      <TabsContent value="Day"><div className="pp-day-rail" aria-label="Choose a day">{days.map((day, index) => <button key={day} aria-pressed={selectedDay === index} onClick={() => { setSelectedDay(index); const first = entries.find(entry => entry.day === index); if (first) setSelectedKey(first.key); }}><span>{day.slice(0, 3)}</span><strong>{dateFor(index).getDate()}</strong><i data-rest={restDays.includes(day)} /></button>)}</div>
        <div className="pp-day-title"><Eyebrow>{days[selectedDay]} / {dateLabel(dateFor(selectedDay))}</Eyebrow><h2>{entries.some(entry => entry.day === selectedDay) ? 'One thing at a time.' : 'Today has a little more space.'}</h2><p>{restDays.includes(days[selectedDay]) ? 'Rest is part of the plan.' : 'Take the blocks in your own time.'}</p></div>{dayEvents(selectedDay)}
        {entries.some(entry => entry.day === selectedDay) ? <div className="pp-day-detail-blocks">{entries.filter(entry => entry.day === selectedDay).map(renderBlock)}</div> : <div className="pp-rest-large"><Artwork src="/assets/star-crew/companions/thinker.png" size={190} /><Button variant="outline" onClick={openSettings}>Adjust rest days</Button></div>}
      </TabsContent></Tabs></section>
      <aside className="pp-detail" aria-label="Selected study block">{selected ? <AnimatePresence mode="wait"><motion.div key={selected.key} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} transition={{ duration: .2 }}><div className="pp-detail-heading"><Eyebrow>{days[selected.day]} / Your next small step</Eyebrow><StudySubjectArtwork subject={selected.block.subjectName} size={148} /></div>
        <PlanCard className="nsu-plan-card rs-composed-card pp-plan-card" icon={<BrandBook size={27} />} title={selected.block.subjectName} description={`${method[selected.block.sessionType]} · ${selected.block.durationMinutes} minutes`} steps={steps} approveLabel="Study this block" approveDisabled={!onStudy || isSkipped(selected) || editing || settings || explain} viewLabel="Edit to-dos" onApprove={() => { if (!editing && !settings && !explain) onStudy?.(selected); }} onView={() => setEditing(true)} />
        <p className="pp-block-prompt">{hints[selected.block.subjectName]?.label ?? (selected.block.suggestedTopics?.join(', ') || 'Choose a manageable piece of work. Give it your attention.')}</p>
        <div className="pp-block-state"><span>{isComplete(selected) ? <><span className="pp-done"><Check /></span>Completed</> : isSkipped(selected) ? <><SkipForward />Skipped this time</> : <><Clock3 />Ready when you are</>}</span>
          {isComplete(selected) ? onComplete && <Button variant="ghost" onClick={() => onComplete(selected, false)}><RotateCcw />Undo</Button> : isSkipped(selected) ? isDeferred?.(selected) && onSkip && <Button variant="ghost" onClick={() => onSkip(selected, false)}><RotateCcw />Undo</Button> : <>{onComplete && <Button variant="ghost" onClick={() => onComplete(selected, true)}><Check />Already studied</Button>}{onSkip && <Button variant="ghost" size="icon" aria-label="Skip this block" onClick={() => onSkip(selected, true)}><SkipForward /></Button>}</>}
        </div><BlockCue key={selected.id} subject={selected.block.subjectName} saved={cues[selected.id]} onSave={cue => onCueSave(selected.id, cue)} />
      </motion.div></AnimatePresence> : <p className="kl-empty">There’s room to rest. Your next blocks will appear here.</p>}</aside>
    </div>
    <section className="pp-workload" id="workload"><div className="pp-workload-ledger"><div className="pp-ledger-heading"><h3>The balance of your week</h3><span>Planned time</span></div>{ledger.map(row => <div className="pp-ledger-row" key={row.subject}><StudySubjectArtwork subject={row.subject} size={43} /><span>{row.subject}</span><span className="pp-ledger-track"><motion.i initial={false} animate={{ width: `${row.minutes / maximum * 100}%` }} transition={{ duration: .5 }} /></span><strong>{time(row.minutes)}</strong></div>)}<button className="pp-explain-toggle" aria-expanded={explain} onClick={() => setExplain(value => !value)}>Behind your plan<ChevronDown /></button>{explain && <div className="pp-explanation">{explanation}</div>}</div></section>
    <Dialog open={settings} onOpenChange={setSettings}><DialogContent className="pp-settings-dialog"><DialogHeader><DialogTitle>Make room for your week.</DialogTitle><DialogDescription>Choose up to three rest days and a manageable block length.</DialogDescription></DialogHeader><fieldset className="pp-rest-settings"><legend>Rest days</legend>{days.map(day => <label key={day}><Checkbox checked={draftRest.includes(day)} disabled={!draftRest.includes(day) && draftRest.length >= 3} onCheckedChange={checked => setDraftRest(previous => checked ? [...previous, day] : previous.filter(item => item !== day))} />{day}</label>)}</fieldset><label className="pp-duration-setting">Minutes per block<select value={draftDuration} onChange={event => setDraftDuration(Number(event.target.value))}>{[...new Set([25, 30, 45, 60, 90, duration])].sort((a, b) => a - b).map(minutes => <option key={minutes} value={minutes}>{minutes} minutes</option>)}</select></label><Button variant="ghost" onClick={() => { setSettings(false); onSettings(); }}>Edit subjects and grades<ArrowUpRight /></Button><DialogFooter><Button variant="ghost" onClick={() => setSettings(false)}>Cancel</Button><Button variant="outline" className="nsu-ink-outline" onClick={() => { onPlanSettingsChange(draftRest, draftDuration); setSettings(false); }}>Save plan settings</Button></DialogFooter></DialogContent></Dialog>
    {editing && selected && <SessionTodos key={selected.key} steps={steps} onClose={() => setEditing(false)} onSave={next => { setTodos(previous => ({ ...previous, [selected.key]: next })); const ok = savePlannerTodos(uid, selected.dateKey, selected.id, next); setSaveError(ok ? '' : 'Your to-dos are available for this visit, but could not be saved on this device.'); setEditing(false); }} />}
    {saveError && <p role="alert">{saveError}</p>}
  </div></KobraScope>;
}
