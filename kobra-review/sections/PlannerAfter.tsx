/**
 * The Planner and the native-select sweep, rebuilt on Kobra (AFTER for review section 07).
 *
 * The words, order and accessible names are components/launchpad/PlannerWorkbench.tsx's,
 * on the same sample week as the "Now" pane (planner-demo.ts: the real planner
 * algorithm on a demo Leaving Cert student). Every value is local review state.
 *
 * What changed against the before:
 *  - the day rail (PlannerWorkbench.tsx:90) is Kobra Tabs, drawn as the house pill;
 *  - the if-then cue triggers (45) are one Kobra ToggleGroup, the chosen one on the orange face;
 *  - "Minutes per block" inside the Plan settings Dialog (103) is a Kobra Select;
 *  - a finished block carries a square ink check, never the orange circle (planner-preview.css:206-215);
 *  - the selected block takes the ink ring, day cards and the plan card are hairlines with no shadow,
 *    and the quiet text actions are outline Buttons so they look clickable before hover.
 * Beneath it, the same three controls as the Now pane: the Launchpad subject picker as a
 * searchable Kobra Combobox, LaunchpadSelect and the Kanban "Move task" menus as Kobra Select.
 *
 * Drawn by hand: the planned-time bars (a hairline track with the subject's fill; Kobra Progress
 * is a progress role, and these are shares of a week, not progress) and the square done mark.
 * "See the allocation in detail" opens the live PlannerExplanation unchanged: it sits on
 * ModalFrame, which the wave 0 "One Dialog" item rebuilds, and its phone-only select is part of
 * the same sweep.
 */
import { useId, useMemo, useState } from 'react';
import { ArrowDown, ArrowUpRight, Check, ChevronDown, ChevronLeft, ChevronRight, Clock3, RotateCcw, Settings2, SkipForward } from 'lucide-react';
import {
  Button, Checkbox, Combobox, ComboboxContent, ComboboxEmpty, ComboboxInput, ComboboxItem, ComboboxList,
  Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, PlanCard,
  Select, SelectContent, SelectItem, SelectTrigger, SelectValue, Tabs, TabsContent, TabsList, TabsTrigger,
  Textarea, ToggleGroup, ToggleGroupItem, type PlanStep,
} from '../../components/approved-ui-runtime';
import ThemeArtwork from '../../components/ThemeArtwork';
import { BrandBook } from '../../components/learning/BrandBook';
import { SessionTodos } from '../../components/study/SessionTodos';
import { StudySubjectArtwork } from '../../components/study/StudySubjectPicker';
import PlannerExplanation from '../../components/launchpad/PlannerExplanation';
import { plannerEntries, workloadLedger, type PlannerEntry } from '../../components/launchpad/PlannerWorkbench';
import { DAYS_OF_WEEK as days, toDateKey, type StudyBlock } from '../../components/subjectData';
import type { PlanCue, PlanCues } from '../../hooks/usePlanCues';
import { PLAN_TRIGGERS, PLAN_WHY, defaultThen } from '../../planIntentionData';
import { getSubjectFill } from '../../utils/subjectColors';
import {
  CATCH_UP_LEVELS, DEMO_DURATION, DEMO_REST_DAYS, DEMO_SUBJECT_NAMES, EXPLAIN_DETAIL, EXPLAIN_SENIOR, EXPLAIN_SPREAD,
  catchUpOptions, demoCompletions, demoPlan, type CatchUpLevel, type PickerOption,
} from './planner-demo';
import './planner.css';

const method = { 'new-learning': 'New learning', practice: 'Practice', revision: 'Revision' };
const time = (minutes: number) => minutes < 60 ? `${minutes}m` : `${Math.floor(minutes / 60)}h${minutes % 60 ? ` ${minutes % 60}m` : ''}`;
const dateLabel = (date: Date) => date.toLocaleDateString('en-IE', { day: 'numeric', month: 'short' });
const defaultSteps = (block: StudyBlock): PlanStep[] => block.sessionType === 'practice' ? [
  { label: block.suggestedTopics?.[0] ? `Practise ${block.suggestedTopics[0]}` : 'Choose one question to work through' },
  { label: 'Have a go before checking the answer' }, { label: 'Note one thing to revisit' },
] : [{ label: block.suggestedTopics?.[0] ? `Work through ${block.suggestedTopics[0]}` : 'Choose a manageable piece of work' }, { label: 'Recall it in your own words' }, { label: 'Note what needs another look' }];

/** The if-then for a block: the triggers are one ToggleGroup, the line a Kobra Textarea. */
function BlockCue({ subject, saved, onSave }: { subject: string; saved?: PlanCue; onSave: (cue: PlanCue) => void }) {
  const [trigger, setTrigger] = useState(saved?.trigger ?? PLAN_TRIGGERS[0]);
  const [then, setThen] = useState(saved?.then ?? defaultThen(subject));
  const [savedOk, setSavedOk] = useState(!!saved);
  return (
    <details className="kr-pl-cue">
      <summary><span>Your if-then for this block</span><ChevronDown aria-hidden="true" /></summary>
      <ToggleGroup className="kr-pl-triggers" variant="outline" value={[trigger]}
        onValueChange={value => { const next = value[value.length - 1]; if (next) { setTrigger(String(next)); setSavedOk(false); } }}>
        {PLAN_TRIGGERS.map(item => <ToggleGroupItem key={item} value={item}>{item}</ToggleGroupItem>)}
      </ToggleGroup>
      <label className="kr-pl-then">Then I’ll…<Textarea value={then} onChange={event => { setThen(event.target.value); setSavedOk(false); }} /></label>
      <Button className="nsu-ink-outline kr-pl-save-cue" variant="outline" disabled={!then.trim()} onClick={() => { onSave({ trigger, then: then.trim() }); setSavedOk(true); }}>
        {savedOk && <Check aria-hidden="true" />}{savedOk ? 'Saved' : 'Save my if-then'}
      </Button>
      <p className="kr-pl-why">{PLAN_WHY.text}<br />{PLAN_WHY.source}</p>
    </details>
  );
}

/** The square ink check that replaces the orange done-circle. */
const DoneMark = ({ label }: { label?: string }) => <span className="kr-pl-done" aria-label={label}><Check aria-hidden="true" /></span>;

function Planner() {
  const ids = useId();
  const [weekOffset, setWeekOffset] = useState(0);
  const [restDays, setRestDays] = useState(DEMO_REST_DAYS);
  const [duration, setDuration] = useState(DEMO_DURATION);
  const [completions, setCompletions] = useState(demoCompletions);
  const [deferred, setDeferred] = useState<string[]>([]);
  const [cues, setCues] = useState<PlanCues>({});
  const [showExplainer, setShowExplainer] = useState(false);
  const plan = useMemo(() => demoPlan(weekOffset, restDays, duration), [weekOffset, restDays, duration]);
  const { timetable, weekStart } = plan;

  const isComplete = (entry: PlannerEntry) => completions[entry.dateKey]?.includes(entry.id) ?? false;
  const isSkipped = (entry: PlannerEntry) => deferred.includes(entry.key);
  const isDeferred = isSkipped;
  const onComplete = (entry: PlannerEntry, done: boolean) => setCompletions(current => {
    const day = current[entry.dateKey] ?? [];
    return { ...current, [entry.dateKey]: done ? [...day, entry.id] : day.filter(id => id !== entry.id) };
  });
  const onSkip = (entry: PlannerEntry, skipped: boolean) => setDeferred(current => skipped ? [...current, entry.key] : current.filter(key => key !== entry.key));

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
  const [explain, setExplain] = useState(false);
  const totalMinutes = entries.reduce((sum, entry) => sum + entry.block.durationMinutes, 0);
  const completed = entries.filter(isComplete).length;
  const ledger = workloadLedger(timetable, DEMO_SUBJECT_NAMES);
  const maximum = Math.max(1, ...ledger.map(row => row.minutes));
  const dateFor = (day: number) => { const date = new Date(weekStart); date.setDate(date.getDate() + day); return date; };
  const steps = selected ? todos[selected.key] ?? defaultSteps(selected.block) : [];
  const openSettings = () => { setDraftRest([...restDays]); setDraftDuration(duration); setSettings(true); };
  const chooseBlock = (entry: PlannerEntry) => { setSelectedKey(entry.key); setSelectedDay(entry.day); };
  const minuteChoices = [...new Set([25, 30, 45, 60, 90, duration])].sort((a, b) => a - b);
  const minuteItems = minuteChoices.map(minutes => ({ value: String(minutes), label: `${minutes} minutes` }));
  const workloadId = `${ids}-workload`.replace(/:/g, '');

  const renderBlock = (entry: PlannerEntry) => (
    <button type="button" key={entry.key} className="kr-pl-block" data-selected={selected?.key === entry.key}
      data-status={isComplete(entry) ? 'done' : isSkipped(entry) ? 'skipped' : undefined}
      aria-label={`${entry.block.subjectName} ${method[entry.block.sessionType]} · ${entry.block.durationMinutes} minutes`}
      aria-pressed={selected?.key === entry.key} onClick={() => chooseBlock(entry)}>
      <StudySubjectArtwork subject={entry.block.subjectName} size={48} />
      <span className="kr-pl-block-copy"><strong>{entry.block.subjectName}</strong><span>{method[entry.block.sessionType]} <i>·</i> {entry.block.durationMinutes} min</span></span>
      {isComplete(entry) ? <DoneMark label="Completed" /> : isSkipped(entry) ? <SkipForward aria-label="Skipped" className="kr-pl-status-icon" /> : <ArrowUpRight className="kr-pl-block-arrow" />}
    </button>
  );

  return (
    <section className="kr-pl-planner" aria-label="The Planner">
      <div className="kr-pl-intro">
        <div><p className="kr-pl-eyebrow">Your Launchpad / The Planner</p><h1>A little room for what’s next.</h1><p>Your week, in manageable blocks.</p></div>
        <ThemeArtwork src="/assets/tools/planner.png" alt="" width={132} height={132} className="kr-pl-art" />
      </div>

      <div className="kr-pl-toolbar">
        <div className="kr-pl-week-nav">
          <Button variant="outline" size="icon" aria-label="Previous timetable week" disabled={weekOffset <= 0} onClick={() => setWeekOffset(weekOffset - 1)}><ChevronLeft /></Button>
          <div aria-live="polite"><span>{weekOffset === 0 ? 'The week ahead' : 'Looking ahead'}</span><h2>{dateLabel(weekStart)} — {dateLabel(dateFor(6))}</h2></div>
          <Button variant="outline" size="icon" aria-label="Next timetable week" onClick={() => setWeekOffset(weekOffset + 1)}><ChevronRight /></Button>
          {weekOffset !== 0 && <Button variant="outline" onClick={() => setWeekOffset(0)}>This week</Button>}
        </div>
        <div className="kr-pl-toolbar-actions">
          <a href={`#${workloadId}`}>{entries.length} blocks · {time(totalMinutes)}<ArrowDown aria-hidden="true" /></a>
          <Button variant="outline" className="nsu-ink-outline" onClick={openSettings}><Settings2 />Plan settings</Button>
        </div>
      </div>

      <div className="kr-pl-layout">
        <section className="kr-pl-agenda" aria-label="Your study schedule">
          <Tabs className="kr-pl-view" value={view} onValueChange={value => setView(String(value))}>
            <div className="kr-pl-agenda-heading">
              <TabsList aria-label="Planner view"><TabsTrigger value="Week">Week</TabsTrigger><TabsTrigger value="Day">Day</TabsTrigger></TabsList>
              <span>{completed} of {entries.length} blocks complete</span>
            </div>
            <TabsContent value="Week">
              <div className="kr-pl-week">
                {days.map((day, index) => {
                  const dayEntries = entries.filter(entry => entry.day === index);
                  if (!dayEntries.length) return null;
                  return (
                    <section className="kr-pl-day" key={day}>
                      <header>
                        <button type="button" className="kr-pl-day-open" onClick={() => { setSelectedDay(index); setView('Day'); }}>{day}<span>{dateFor(index).getDate()}</span></button>
                        <small>{time(dayEntries.reduce((sum, entry) => sum + entry.block.durationMinutes, 0))}</small>
                      </header>
                      <div className="kr-pl-day-blocks">{dayEntries.map(renderBlock)}</div>
                    </section>
                  );
                })}
              </div>
              {!entries.length && (
                <div className="kr-pl-empty-week"><h2>No study blocks planned this week.</h2><p>Adjust your plan when you’re ready to make some time.</p><Button variant="outline" className="nsu-ink-outline" onClick={openSettings}>Plan settings</Button></div>
              )}
            </TabsContent>
            <TabsContent value="Day">
              <Tabs className="kr-pl-rail" value={String(selectedDay)}
                onValueChange={value => { const index = Number(value); setSelectedDay(index); const first = entries.find(entry => entry.day === index); if (first) setSelectedKey(first.key); }}>
                <TabsList aria-label="Choose a day">
                  {days.map((day, index) => (
                    <TabsTrigger key={day} value={String(index)}>
                      <span>{day.slice(0, 3)}</span><strong>{dateFor(index).getDate()}</strong><i aria-hidden="true" data-rest={restDays.includes(day)} />
                    </TabsTrigger>
                  ))}
                </TabsList>
              </Tabs>
              <div className="kr-pl-day-title">
                <p className="kr-pl-eyebrow">{days[selectedDay]} / {dateLabel(dateFor(selectedDay))}</p>
                <h2>{entries.some(entry => entry.day === selectedDay) ? 'One thing at a time.' : 'Today has a little more space.'}</h2>
                <p>{restDays.includes(days[selectedDay]) ? 'Rest is part of the plan.' : 'Take the blocks in your own time.'}</p>
              </div>
              {entries.some(entry => entry.day === selectedDay)
                ? <div className="kr-pl-day-detail">{entries.filter(entry => entry.day === selectedDay).map(renderBlock)}</div>
                : <div className="kr-pl-rest"><ThemeArtwork src="/assets/star-crew/companions/thinker.png" alt="" width={190} height={190} className="kr-pl-art" /><Button variant="outline" className="nsu-ink-outline" onClick={openSettings}>Adjust rest days</Button></div>}
            </TabsContent>
          </Tabs>
        </section>

        <aside className="kr-pl-detail" aria-label="Selected study block">
          {selected ? (
            <div key={selected.key}>
              <div className="kr-pl-detail-heading"><p className="kr-pl-eyebrow">{days[selected.day]} / Your next small step</p><StudySubjectArtwork subject={selected.block.subjectName} size={148} /></div>
              <PlanCard className="nsu-plan-card kr-pl-plan-card" icon={<BrandBook size={27} />} title={selected.block.subjectName}
                description={`${method[selected.block.sessionType]} · ${selected.block.durationMinutes} minutes`} steps={steps}
                approveLabel="Study this block" approveDisabled={isSkipped(selected) || editing || settings || explain} viewLabel="Edit to-dos"
                onApprove={() => {}} onView={() => setEditing(true)} />
              <p className="kr-pl-prompt">{selected.block.suggestedTopics?.join(', ') || 'Choose a manageable piece of work. Give it your attention.'}</p>
              <div className="kr-pl-state">
                <span>{isComplete(selected) ? <><DoneMark />Completed</> : isSkipped(selected) ? <><SkipForward aria-hidden="true" />Skipped this time</> : <><Clock3 aria-hidden="true" />Ready when you are</>}</span>
                {isComplete(selected)
                  ? <Button variant="outline" onClick={() => onComplete(selected, false)}><RotateCcw />Undo</Button>
                  : isSkipped(selected)
                    ? isDeferred(selected) && <Button variant="outline" onClick={() => onSkip(selected, false)}><RotateCcw />Undo</Button>
                    : <><Button variant="outline" onClick={() => onComplete(selected, true)}><Check />Already studied</Button><Button variant="outline" size="icon" aria-label="Skip this block" onClick={() => onSkip(selected, true)}><SkipForward /></Button></>}
              </div>
              <BlockCue key={selected.id} subject={selected.block.subjectName} saved={cues[selected.id]} onSave={cue => setCues(current => ({ ...current, [selected.id]: cue }))} />
            </div>
          ) : <p className="kr-pl-empty">There’s room to rest. Your next blocks will appear here.</p>}
        </aside>
      </div>

      <section className="kr-pl-workload" id={workloadId}>
        <div className="kr-pl-ledger-heading"><h3>The balance of your week</h3><span>Planned time</span></div>
        {ledger.map(row => (
          <div className="kr-pl-ledger-row" key={row.subject}>
            <StudySubjectArtwork subject={row.subject} size={43} />
            <span>{row.subject}</span>
            <span className="kr-pl-track" aria-hidden="true"><i style={{ width: `${row.minutes / maximum * 100}%`, background: getSubjectFill(row.subject) }} /></span>
            <strong>{time(row.minutes)}</strong>
          </div>
        ))}
        <button type="button" className="kr-pl-explain-toggle" aria-expanded={explain} onClick={() => setExplain(value => !value)}>Behind your plan<ChevronDown aria-hidden="true" /></button>
        {explain && (
          <div className="kr-pl-explanation">
            <p>{plan.weeklyTarget.explanation}</p><p>{EXPLAIN_SPREAD}</p><p>{EXPLAIN_SENIOR}</p>
            <Button variant="outline" className="nsu-ink-outline" onClick={() => setShowExplainer(true)}>{EXPLAIN_DETAIL}</Button>
            <PlannerExplanation open={showExplainer} onClose={() => setShowExplainer(false)} priorities={plan.priorities} allocations={plan.allocations} totalSessions={plan.totalSessions} totalMinutes={plan.totalMinutes} workloadExplanation={plan.weeklyTarget.explanation} />
          </div>
        )}
      </section>

      <Dialog open={settings} onOpenChange={setSettings}>
        <DialogContent className="kr-pl-dialog">
          <DialogHeader><DialogTitle>Make room for your week.</DialogTitle><DialogDescription>Choose up to three rest days and a manageable block length.</DialogDescription></DialogHeader>
          <fieldset className="kr-pl-rest-days">
            <legend>Rest days</legend>
            {days.map(day => (
              <label key={day} className="kr-pl-rest-day">
                <Checkbox checked={draftRest.includes(day)} disabled={!draftRest.includes(day) && draftRest.length >= 3}
                  onCheckedChange={checked => setDraftRest(previous => checked ? [...previous, day] : previous.filter(item => item !== day))} />{day}
              </label>
            ))}
          </fieldset>
          <div className="kr-pl-duration">
            <span id={`${ids}-minutes`}>Minutes per block</span>
            <Select value={String(draftDuration)} items={minuteItems} onValueChange={value => { if (value) setDraftDuration(Number(value)); }}>
              <SelectTrigger aria-labelledby={`${ids}-minutes`} className="kr-pl-select"><SelectValue /></SelectTrigger>
              <SelectContent className="kr-pl-menu" alignItemWithTrigger={false} align="end">
                {minuteItems.map(item => <SelectItem key={item.value} value={item.value}>{item.label}</SelectItem>)}
              </SelectContent>
            </Select>
          </div>
          <Button variant="outline" className="kr-pl-edit-subjects" onClick={() => setSettings(false)}>Edit subjects and grades<ArrowUpRight /></Button>
          <DialogFooter>
            <Button variant="outline" onClick={() => setSettings(false)}>Cancel</Button>
            <Button variant="outline" className="nsu-ink-outline" onClick={() => { setRestDays(draftRest); setDuration(draftDuration); setSettings(false); }}>Save plan settings</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
      {editing && selected && <SessionTodos key={selected.key} steps={steps} onClose={() => setEditing(false)} onSave={next => { setTodos(previous => ({ ...previous, [selected.key]: next })); setEditing(false); }} />}
    </section>
  );
}

/** launchpad/SubjectPicker.tsx as a searchable Combobox: same label, placeholder, options and empty line. */
function SubjectCombobox({ value, options, onChange, label = 'Choose a subject' }: { value: string; options: PickerOption[]; onChange: (value: string) => void; label?: string }) {
  const id = useId();
  const selected = options.find(option => option.value === value) ?? null;
  return (
    <div className="kr-pl-field">
      <label className="kr-pl-sr" htmlFor={id}>{label}</label>
      <Combobox items={options} value={selected} itemToStringLabel={(option: PickerOption) => option.label}
        isItemEqualToValue={(a: PickerOption, b: PickerOption) => a.value === b.value}
        onValueChange={(option: PickerOption | null) => { if (option) onChange(option.value); }}>
        <ComboboxInput id={id} className="kr-pl-combo" placeholder="Search subjects" aria-label={label} />
        <ComboboxContent className="kr-pl-menu kr-pl-combo-menu">
          <ComboboxEmpty>No matching subjects. Try a shorter name.</ComboboxEmpty>
          <ComboboxList>
            {(option: PickerOption) => (
              <ComboboxItem key={option.value} value={option}>
                <span className="kr-pl-option"><strong>{option.label}</strong>{option.detail && <small>{option.detail}</small>}</span>
              </ComboboxItem>
            )}
          </ComboboxList>
        </ComboboxContent>
      </Combobox>
    </div>
  );
}

/** activities/KanbanBoard.tsx with a Kobra Select per task. Same stages, tasks and words. */
const STAGES = [{ id: 'todo', label: 'To do' }, { id: 'doing', label: 'In progress' }, { id: 'done', label: 'Done' }] as const;
type Stage = typeof STAGES[number]['id'];
interface Task { id: number; text: string; column: Stage }
const STAGE_ITEMS = STAGES.map(stage => ({ value: stage.id, label: stage.label }));

function Kanban() {
  const ids = useId();
  const [tasks, setTasks] = useState<Task[]>([
    { id: 1, text: 'Write Macbeth Quote Bank', column: 'todo' },
    { id: 2, text: 'Do 2023 Paper 1 Algebra Q', column: 'todo' },
    { id: 3, text: 'Practice Irish Oral Poem', column: 'doing' },
  ]);
  const [announcement, setAnnouncement] = useState('');
  const moveTask = (task: Task, column: Stage) => {
    if (column === task.column) return;
    setTasks(previous => previous.map(item => item.id === task.id ? { ...item, column } : item));
    setAnnouncement(`${task.text} moved to ${STAGES.find(stage => stage.id === column)?.label}.`);
  };
  return (
    <section className="kr-pl-kanban" aria-labelledby={`${ids}-kanban`}>
      <div className="kr-pl-kanban-head">
        <p className="kr-pl-eyebrow">Try it · Make progress visible</p>
        <h4 id={`${ids}-kanban`}>Kanban Flow</h4>
        <p>Move a task through the stages using its menu. Each task in Done is a win.</p>
      </div>
      <div className="kr-pl-columns">
        {STAGES.map((stage, index) => {
          const inStage = tasks.filter(task => task.column === stage.id);
          return (
            <section key={stage.id} data-stage={stage.id} aria-label={stage.label} className="kr-pl-column">
              <h5><span><span className="kr-pl-serial">0{index + 1}</span>{stage.label}</span><span aria-label={`${inStage.length} ${inStage.length === 1 ? 'task' : 'tasks'}`} className="kr-pl-count">{inStage.length}</span></h5>
              <div className="kr-pl-tasks">
                {inStage.map(task => (
                  <div key={task.id} className="kr-pl-task">
                    <p>{task.text}</p>
                    <label htmlFor={`${ids}-kanban-task-${task.id}`}>Move task</label>
                    <Select value={task.column} items={STAGE_ITEMS} onValueChange={value => { if (value) moveTask(task, value as Stage); }}>
                      <SelectTrigger id={`${ids}-kanban-task-${task.id}`} aria-label={`Move ${task.text}`} className="kr-pl-select"><SelectValue /></SelectTrigger>
                      <SelectContent className="kr-pl-menu" alignItemWithTrigger={false} align="start">
                        {STAGE_ITEMS.map(option => <SelectItem key={option.value} value={option.value}>{option.label}</SelectItem>)}
                      </SelectContent>
                    </Select>
                  </div>
                ))}
                {!inStage.length && <p className="kr-pl-column-empty">{stage.id === 'done' ? 'Your finished tasks land here.' : 'No tasks here yet.'}</p>}
              </div>
            </section>
          );
        })}
      </div>
      <p role="status" className="kr-pl-kanban-status">{announcement || `${tasks.filter(task => task.column === 'done').length} of ${tasks.length} tasks done.`}</p>
    </section>
  );
}

function NativeSelects() {
  const ids = useId();
  const [level, setLevel] = useState<CatchUpLevel>('higher');
  const options = useMemo(() => catchUpOptions(level), [level]);
  const [subjectId, setSubjectId] = useState('biology');
  return (
    <section className="kr-pl-sweep" aria-labelledby={`${ids}-sweep`}>
      <h2 id={`${ids}-sweep`}>Native selects around the app</h2>
      <p className="kr-pl-caption">The Launchpad subject picker and two components that render the browser’s own select, mounted on their own with sample options.</p>
      <div className="kr-pl-sweep-item">
        <p className="kr-pl-caption"><code>components/launchpad/SubjectPicker.tsx</code> as a Combobox and <code>components/launchpad/LaunchpadSelect.tsx</code> as a Select, as the Catch-Up Lane uses them</p>
        <div className="kr-pl-aside">
          <SubjectCombobox value={subjectId} options={options} onChange={setSubjectId} />
          <Select value={level} items={CATCH_UP_LEVELS} onValueChange={value => { if (value) setLevel(value as CatchUpLevel); }}>
            <SelectTrigger aria-label="Catch-Up level" className="kr-pl-select"><SelectValue /></SelectTrigger>
            <SelectContent className="kr-pl-menu" alignItemWithTrigger={false} align="start">
              {CATCH_UP_LEVELS.map(item => <SelectItem key={item.value} value={item.value}>{item.label}</SelectItem>)}
            </SelectContent>
          </Select>
        </div>
      </div>
      <div className="kr-pl-sweep-item">
        <p className="kr-pl-caption"><code>components/activities/KanbanBoard.tsx</code>, in the Reframing Progress module</p>
        <Kanban />
      </div>
    </section>
  );
}

export default function PlannerAfter() {
  return (
    <div className="kr-pl">
      <p className="kr-pl-caption kr-pl-sample">Sample week for a demo Leaving Cert student. No account is connected.</p>
      <Planner />
      <NativeSelects />
    </div>
  );
}
