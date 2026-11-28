/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useMemo, useRef } from 'react';
import { ChevronLeft, ChevronRight, MoreHorizontal, Plus } from 'lucide-react';
import { db } from '../../firebase';
import { saveInBackground } from '../../utils/firestoreWrite';
import { doc, getDoc, setDoc } from 'firebase/firestore';
import { Button, IconButton, TextButton } from '../ui/Button';
import { SelectionBar } from '../ui/Choice';
import { Field } from '../ui/Field';
import { List, Row } from '../ui/List';
import { Menu, MenuAction, MenuPanel } from '../ui/Menu';
import { Sheet } from '../ui/Sheet';
import { LoadingShape } from '../ui/States';
import { getDaysUntilLC } from './gcUtils';
import { useWide } from './gcView';

// ─── Types ──────────────────────────────────────────────────────────────────

// Year-group targeting (Phase 1 was '5th' | '6th' | 'both'; Phase 6 extends
// to the JC years + TY). 'both' = both senior years (legacy semantics);
// 'all' = everyone regardless of year. Keep 'both' as-is to avoid migrating
// existing Firestore docs.
export type EventYearGroup =
  | '1st' | '2nd' | '3rd'
  | 'TY'
  | '5th' | '6th'
  | 'both'         // legacy: senior cycle (5th + 6th)
  | 'all';         // everyone

export interface SchoolEvent {
  id: string;
  title: string;
  date: string;        // ISO "YYYY-MM-DD"
  yearGroup: EventYearGroup;
  category: EventCategory;
  createdAt: string;
}

type EventCategory = 'exams' | 'deadlines' | 'school' | 'other';

// Curriculum tag on a preset — drives context-aware filtering in the
// "Add Event" dropdown. 'both' means the preset is relevant to both
// curricula (e.g. Christmas Tests, Parent-Teacher Meeting).
export type EventCurriculum = 'junior' | 'senior' | 'both';

interface PresetEvent {
  title: string;
  category: EventCategory;
  curriculum: EventCurriculum;
  // Default yearGroup to pre-fill when the GC picks this preset. Helps
  // them avoid having to re-pick year manually for events that only apply
  // to one specific year (Junior Cert → 3rd, LC Starts → 6th).
  defaultYearGroup: EventYearGroup;
}

const EVENT_CATEGORIES: { id: EventCategory; label: string; color: string; dotColor: string }[] = [
  { id: 'exams', label: 'Exams', color: 'text-red-600 dark:text-red-400', dotColor: 'bg-red-500' },
  { id: 'deadlines', label: 'Deadlines', color: 'text-amber-600 dark:text-amber-400', dotColor: 'bg-amber-500' },
  { id: 'school', label: 'School', color: 'text-blue-600 dark:text-blue-400', dotColor: 'bg-blue-500' },
  { id: 'other', label: 'Other', color: 'text-zinc-600 dark:text-zinc-400', dotColor: 'bg-zinc-500' },
];

// Preset events — Phase 6 splits Mocks into JC/LC variants, retags existing
// senior events explicitly, and adds JC-relevant presets. Universal
// in-school events (Christmas Tests, Summer Tests, Parent-Teacher Meeting)
// are tagged 'both'.
const PRESET_EVENTS: PresetEvent[] = [
  // Mocks (split per Phase 6 spec — dates differ between JC and LC)
  { title: 'LC Mocks Start',                  category: 'exams',     curriculum: 'senior', defaultYearGroup: '6th' },
  { title: 'LC Mocks End',                    category: 'exams',     curriculum: 'senior', defaultYearGroup: '6th' },
  { title: 'JC Mocks Start',                  category: 'exams',     curriculum: 'junior', defaultYearGroup: '3rd' },
  { title: 'JC Mocks End',                    category: 'exams',     curriculum: 'junior', defaultYearGroup: '3rd' },
  // Senior-only — CAO / SUSI / LC
  { title: 'CAO Application Deadline',        category: 'deadlines', curriculum: 'senior', defaultYearGroup: '6th' },
  { title: 'CAO Change of Mind Deadline',     category: 'deadlines', curriculum: 'senior', defaultYearGroup: '6th' },
  { title: 'SUSI Grant Deadline',             category: 'deadlines', curriculum: 'senior', defaultYearGroup: '6th' },
  { title: 'Leaving Cert Starts',             category: 'exams',     curriculum: 'senior', defaultYearGroup: '6th' },
  { title: 'Leaving Cert Ends',               category: 'exams',     curriculum: 'senior', defaultYearGroup: '6th' },
  // JC-only
  { title: 'Junior Cert Starts',              category: 'exams',     curriculum: 'junior', defaultYearGroup: '3rd' },
  { title: 'Junior Cert Ends',                category: 'exams',     curriculum: 'junior', defaultYearGroup: '3rd' },
  { title: 'Junior Cert Results Day',         category: 'school',    curriculum: 'junior', defaultYearGroup: '3rd' },
  { title: 'LC Subject Choice Deadline',      category: 'deadlines', curriculum: 'junior', defaultYearGroup: '3rd' },
  // TY-specific (lives under senior since TY rides senior content per Phase 1)
  { title: 'TY Mini-Company Final',           category: 'school',    curriculum: 'senior', defaultYearGroup: 'TY' },
  { title: 'TY Work Experience',              category: 'school',    curriculum: 'senior', defaultYearGroup: 'TY' },
  // Universal — applies to both curricula
  { title: 'Christmas Tests',                 category: 'exams',     curriculum: 'both',   defaultYearGroup: 'all' },
  { title: 'Summer Tests',                    category: 'exams',     curriculum: 'both',   defaultYearGroup: 'all' },
  { title: 'Parent-Teacher Meeting',          category: 'school',    curriculum: 'both',   defaultYearGroup: 'all' },
  { title: 'Career Talks',                    category: 'school',    curriculum: 'both',   defaultYearGroup: 'all' },
  { title: 'College Open Day',                category: 'school',    curriculum: 'senior', defaultYearGroup: '6th' },
  { title: 'Study Week',                      category: 'school',    curriculum: 'both',   defaultYearGroup: 'all' },
];

// ─── Firestore path: gcEvents/{school} → { events: SchoolEvent[] } ──────────

interface GCKeyEventsProps {
  school: string;
  /** Per-student context for preset filtering. When the GC opens this
   *  component from within a student detail view, pass the student's
   *  curriculum + year so the "Quick Add" presets only show those
   *  relevant to that student. From the school-wide GC dashboard, omit
   *  this prop — all presets show. */
  studentContext?: {
    curriculumLevel?: 'junior' | 'senior';
    yearGroup?: EventYearGroup;
  };
  /** page: the Key dates place (a title, the list and the calendar); panel (default): a part of the Overview. */
  layout?: 'panel' | 'page';
}

export const GCKeyEvents: React.FC<GCKeyEventsProps> = ({ school, studentContext, layout = 'panel' }) => {
  const wide = useWide();
  const titleRef = useRef<HTMLInputElement>(null);
  const dateRef = useRef<HTMLInputElement>(null);
  const [events, setEvents] = useState<SchoolEvent[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);
  // Year-group filter widened to include JC years + TY so a school running
  // a mixed cohort can scope the events list by any actual year group.
  const [yearFilter, setYearFilter] = useState<'all' | EventYearGroup>('all');

  // Add form state
  const [newTitle, setNewTitle] = useState('');
  const [newDate, setNewDate] = useState('');
  const [newYearGroup, setNewYearGroup] = useState<EventYearGroup>('both');
  const [newCategory, setNewCategory] = useState<EventCategory>('school');
  const [showPresets, setShowPresets] = useState(false);

  // Filter presets by context: per-student context → only presets matching
  // that student's curriculum + (loosely) their year group. School-wide
  // context (studentContext undefined) → all presets.
  const visiblePresets = useMemo(() => {
    if (!studentContext) return PRESET_EVENTS;
    return PRESET_EVENTS.filter(p => {
      // Curriculum gate: 'both' presets always show; otherwise must match.
      if (p.curriculum !== 'both' && p.curriculum !== studentContext.curriculumLevel) {
        return false;
      }
      // Year-group gate (loose): if the student has a known yearGroup and
      // the preset defaults to a specific year that doesn't match, hide it.
      // Presets defaulting to 'all' or 'both' always pass.
      if (studentContext.yearGroup && p.defaultYearGroup !== 'all' && p.defaultYearGroup !== 'both') {
        if (p.defaultYearGroup !== studentContext.yearGroup) return false;
      }
      return true;
    });
  }, [studentContext]);

  // Load events
  useEffect(() => {
    let cancelled = false;
    const load = async () => {
      try {
        const snap = await getDoc(doc(db, 'gcEvents', school));
        if (cancelled) return;
        if (snap.exists()) {
          setEvents(snap.data().events ?? []);
        }
      } catch (err) {
        console.error('[GCKeyEvents] Failed to load:', err);
      }
      if (!cancelled) setIsLoading(false);
    };
    load();
    return () => { cancelled = true; };
  }, [school]);

  // Save events
  const saveEvents = (updated: SchoolEvent[]) => {
    const previous = events;
    setEvents(updated);
    saveInBackground(
      setDoc(doc(db, 'gcEvents', school), { events: updated }, { merge: true }),
      'GCKeyEvents.saveEvents',
      () => setEvents(previous),
    );
  };

  const handleAdd = () => {
    if (!newTitle.trim() || !newDate) return;
    const event: SchoolEvent = {
      id: `${Date.now()}-${Math.random().toString(36).substr(2, 6)}`,
      title: newTitle.trim(),
      date: newDate,
      yearGroup: newYearGroup,
      category: newCategory,
      createdAt: new Date().toISOString(),
    };
    saveEvents([...events, event].sort((a, b) => a.date.localeCompare(b.date)));
    setNewTitle('');
    setNewDate('');
    setNewYearGroup('both');
    setNewCategory('school');
    setShowAddForm(false);
  };

  const handleDelete = (id: string) => {
    saveEvents(events.filter(e => e.id !== id));
  };

  const handlePresetClick = (preset: PresetEvent) => {
    setNewTitle(preset.title);
    setNewCategory(preset.category);
    setNewYearGroup(preset.defaultYearGroup);
    setShowPresets(false);
  };

  // Filter events. Match logic:
  //   - filter 'all' → show everything
  //   - filter equal to event.yearGroup → match
  //   - event tagged 'all' → matches any year filter
  //   - event tagged 'both' (legacy = senior 5th+6th) → matches 5th, 6th, or 'both' filter
  const filteredEvents = useMemo(() => {
    return events.filter(e => {
      if (yearFilter === 'all') return true;
      if (e.yearGroup === yearFilter) return true;
      if (e.yearGroup === 'all') return true;
      if (e.yearGroup === 'both' && (yearFilter === '5th' || yearFilter === '6th')) return true;
      return false;
    });
  }, [events, yearFilter]);

  // Group by upcoming vs past
  const today = new Date().toISOString().split('T')[0];
  const upcomingEvents = filteredEvents.filter(e => e.date >= today);
  const pastEvents = filteredEvents.filter(e => e.date < today);

  const getDaysUntil = (dateStr: string) => {
    const d = new Date(dateStr + 'T00:00:00');
    const now = new Date();
    now.setHours(0, 0, 0, 0);
    return Math.ceil((d.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));
  };

  const categoryWords: Record<EventCategory, string> = { exams: 'Exam', deadlines: 'Deadline', school: 'School', other: 'Other' };
  const yearWords = (yg: EventYearGroup) => (yg === 'all' ? 'All years' : yg === 'both' ? 'Both senior years' : yg === 'TY' ? 'TY' : `${yg} Year`);
  const shortDate = (dateStr: string) => new Date(dateStr + 'T00:00:00').toLocaleDateString('en-IE', { weekday: 'short', day: 'numeric', month: 'short' }).replace(/,/g, '');
  const toGo = (days: number) => (days === 0 ? 'Today' : days === 1 ? 'Tomorrow' : `${days} days`);
  const page = layout === 'page';

  const eventRow = (event: SchoolEvent, past: boolean) => (
    <Row
      key={event.id}
      icon={<i className={`gc8-mk gc8-mk--${event.category}`} />}
      title={event.title}
      meta={`${shortDate(event.date)} · ${categoryWords[event.category]} · ${yearWords(event.yearGroup)}`}
      value={past ? undefined : toGo(getDaysUntil(event.date))}
      end={
        <MenuPanel
          label={event.title}
          buttonLabel={`Actions for ${event.title}`}
          buttonClassName="gc8-acts"
          className="gc8-rowmenu"
          chevron={false}
          face={<MoreHorizontal className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" />}
        >
          <MenuAction plain tone="danger" title="Delete" onPress={() => handleDelete(event.id)} />
        </MenuPanel>
      }
    />
  );

  const tools = (
    <div className="gc8-date-tools">
      <Menu
        label="Year"
        value={yearFilter}
        onChange={value => setYearFilter(value as 'all' | EventYearGroup)}
        options={[
          { value: 'all', label: 'All years' },
          ...(['1st', '2nd', '3rd', 'TY', '5th', '6th'] as const).map(yg => ({ value: yg, label: yearWords(yg) })),
        ]}
      />
      <Button className="gc8-ib" onClick={() => setShowAddForm(true)}><Plus className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" />Add event</Button>
    </div>
  );

  const lists = filteredEvents.length === 0 ? (
    <p className="gc8-empty">No events yet. Add key dates for your students.</p>
  ) : (
    <>
      {upcomingEvents.length > 0 && (
        <div className="gc8-sec">
          {page && <p className="gc8-label">Upcoming</p>}
          <List className="gc8-list gc8-dates">{upcomingEvents.map(e => eventRow(e, false))}</List>
        </div>
      )}
      {pastEvents.length > 0 && (
        <div className="gc8-sec">
          <p className="gc8-label">Past</p>
          <List className="gc8-list gc8-dates gc8-dates--past">{pastEvents.map(e => eventRow(e, true))}</List>
        </div>
      )}
    </>
  );

  const addSheet = (
    <Sheet
      open={showAddForm}
      title="Add event"
      onClose={() => setShowAddForm(false)}
      footer={
        <Button
          kind="main"
          size="lg"
          block
          missing={!newTitle.trim() || !newDate ? { sentence: 'Add an event name and a date.', goTo: !newTitle.trim() ? titleRef : dateRef } : undefined}
          onClick={handleAdd}
        >
          Add event
        </Button>
      }
    >
      <div className="gc8-sheet-body">
        <div className="gc8-sheet-group">
          <TextButton tone="quiet" arrow="menu" aria-expanded={showPresets} onClick={() => setShowPresets(!showPresets)}>Quick add</TextButton>
          {showPresets && (
            <div className="gc8-presets">
              {visiblePresets.length === 0 && (
                <p className="gc8-meta">No quick-add presets match this student's curriculum / year.</p>
              )}
              {visiblePresets.map(preset => (
                <Button key={preset.title} size="sm" className="gc8-ib" onClick={() => handlePresetClick(preset)}>
                  <i className={`gc8-mk gc8-mk--${preset.category}`} aria-hidden="true" />{preset.title}
                </Button>
              ))}
            </div>
          )}
        </div>
        <Field ref={titleRef} label="Event name" placeholder="Event name" value={newTitle} onChange={e => setNewTitle(e.target.value)} enterKeyHint="done" />
        <Field ref={dateRef} label="Date" type="date" value={newDate} onChange={e => setNewDate(e.target.value)} />
        <label className="ui-part ui-field">
          <span className="ui-field-label">Year group</span>
          {/* A long form's own picker (components.md: native select is acceptable inside a form). */}
          <select className="ui-field-input" value={newYearGroup} onChange={e => setNewYearGroup(e.target.value as EventYearGroup)}>
            <option value="all">Everyone</option>
            <option value="1st">1st Year</option>
            <option value="2nd">2nd Year</option>
            <option value="3rd">3rd Year</option>
            <option value="TY">TY</option>
            <option value="5th">5th Year</option>
            <option value="6th">6th Year</option>
            <option value="both">Both senior years</option>
          </select>
        </label>
        <div className="gc8-sheet-group">
          <p className="ui-field-label">Category</p>
          <SelectionBar
            label="Category"
            size="md"
            value={newCategory}
            onChange={value => setNewCategory(value as EventCategory)}
            options={EVENT_CATEGORIES.map(cat => ({ value: cat.id, label: cat.label }))}
          />
        </div>
      </div>
    </Sheet>
  );

  if (isLoading) {
    return <LoadingShape rows={3} label="Loading key dates" />;
  }

  const comingUp = `${upcomingEvents.length} coming up`;

  if (page) {
    const daysUntilLC = getDaysUntilLC();
    return (
      <div id="gc-events" className="gc8-dates-page">
        <section className="gc8-hero" aria-labelledby="gc8-dates-title">
          <div className="gc8-head">
            <h1 id="gc8-dates-title" className={wide ? 'gc8-title' : 'gc8-name'}>Key dates and events</h1>
            <p className="gc8-sub">{comingUp}</p>
          </div>
          {tools}
        </section>
        <div className="gc8-two">
          <section className="gc8-sec" aria-label="Key dates">{lists}</section>
          <section className="gc8-sec" aria-labelledby="gc8-dates-cal">
            {wide ? (
              <p id="gc8-dates-cal" className="gc8-label">Exam calendar</p>
            ) : (
              <div className="gc8-sechead">
                <div className="gc8-sechead-col"><p className="gc8-label">Countdown</p><h2 id="gc8-dates-cal" className="gc8-h">Exam calendar</h2></div>
                <p className="gc8-countdown"><span className="gc8-num gc8-live">{daysUntilLC}</span><span className="gc8-meta">days to the<br />Leaving Cert</span></p>
              </div>
            )}
            <GCCalendar events={events} months={1} initialDate={upcomingEvents[0]?.date} />
          </section>
        </div>
        {addSheet}
      </div>
    );
  }

  return (
    <section id="gc-events" className="gc8-sec" aria-labelledby="gc8-dates-panel">
      <div className="gc8-sechead"><h2 id="gc8-dates-panel" className="gc8-h">Key dates and events</h2><span className="gc8-meta">{comingUp}</span></div>
      {tools}
      {lists}
      {addSheet}
    </section>
  );
};

// ─── The calendar (the Kobra calendar: months in one frame, today in ink, the chosen day outlined,
// a mark under each event by its kind, and what is on the chosen day under or beside it) ─────────

/** The Leaving Cert starts on the first Wednesday of June (the next one still to come). */
export function getLCExamDate(): Date {
  const now = new Date();
  const year = now.getFullYear();
  const june1 = new Date(year, 5, 1);
  let firstWed = new Date(june1);
  const dow = june1.getDay();
  const daysUntilWed = (3 - dow + 7) % 7;
  firstWed.setDate(june1.getDate() + daysUntilWed);
  if (firstWed.getTime() < now.getTime()) {
    const nextJune1 = new Date(year + 1, 5, 1);
    const nextDow = nextJune1.getDay();
    const nextDays = (3 - nextDow + 7) % 7;
    firstWed = new Date(nextJune1);
    firstWed.setDate(nextJune1.getDate() + nextDays);
  }
  return firstWed;
}

const MONTH_NAMES = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
const WEEKDAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
const keyOf = (d: Date) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;

export function GCCalendar({ events, months = 1, beside = false, countdown, initialDate }: {
  events: SchoolEvent[];
  /** One month on a phone and beside a list; two on a wide laptop. */
  months?: 1 | 2;
  /** What is on the chosen day sits beside the calendar (a laptop's Overview), not under it. */
  beside?: boolean;
  /** Shown above the chosen day when beside (the countdown to the Leaving Cert). */
  countdown?: React.ReactNode;
  /** The day chosen at first (today if not given). */
  initialDate?: string;
}) {
  const today = new Date();
  const todayKey = keyOf(today);
  const lcKey = keyOf(getLCExamDate());
  const [chosen, setChosen] = useState<string>(initialDate ?? todayKey);
  const start = new Date(`${chosen}T00:00:00`);
  const [view, setView] = useState({ year: (initialDate ? start : today).getFullYear(), month: (initialDate ? start : today).getMonth() });

  const byDay = useMemo(() => {
    const map: Record<string, SchoolEvent[]> = {};
    for (const ev of events) (map[ev.date] ??= []).push(ev);
    return map;
  }, [events]);

  const step = (by: number) => setView(v => {
    const d = new Date(v.year, v.month + by, 1);
    return { year: d.getFullYear(), month: d.getMonth() };
  });
  const daysTo = (key: string) => {
    const d = new Date(`${key}T00:00:00`);
    const now = new Date(); now.setHours(0, 0, 0, 0);
    return Math.round((d.getTime() - now.getTime()) / 86400000);
  };
  const toGo = (days: number) => (days === 0 ? 'Today' : days === 1 ? 'Tomorrow' : days > 0 ? `${days} days` : `${-days} days ago`);
  const catWords: Record<EventCategory, string> = { exams: 'Exam', deadlines: 'Deadline', school: 'School', other: 'Other' };
  const yearWords = (yg: EventYearGroup) => (yg === 'all' ? 'All years' : yg === 'both' ? 'Both senior years' : yg === 'TY' ? 'TY' : `${yg} Year`);
  const shortDate = (key: string) => new Date(`${key}T00:00:00`).toLocaleDateString('en-IE', { weekday: 'short', day: 'numeric', month: 'short' }).replace(/,/g, '');

  const chosenDate = new Date(`${chosen}T00:00:00`);
  const chosenWords = `${chosen === todayKey ? 'Today, ' : ''}${chosenDate.toLocaleDateString('en-IE', { weekday: 'long', day: 'numeric', month: 'long' }).replace(/,/g, '')}`;
  const onDay = [...(byDay[chosen] ?? [])];
  const next = onDay.length === 0 ? events.filter(e => e.date > chosen).sort((a, b) => a.date.localeCompare(b.date))[0] : undefined;

  const monthGrid = (offset: number) => {
    const first = new Date(view.year, view.month + offset, 1);
    const y = first.getFullYear();
    const m = first.getMonth();
    const lead = (first.getDay() + 6) % 7; // Monday first
    const count = new Date(y, m + 1, 0).getDate();
    return (
      <div key={`${y}-${m}`}>
        <p className="gc8-cal-title" aria-live={offset === 0 ? 'polite' : undefined}>{MONTH_NAMES[m]} {y}</p>
        <div className="gc8-cal-grid" role="group" aria-label={`${MONTH_NAMES[m]} ${y}`}>
          {WEEKDAYS.map(w => <span key={w} className="gc8-cal-wd" aria-hidden="true">{w}</span>)}
          {Array.from({ length: lead }, (_, i) => <span key={`b${i}`} aria-hidden="true" />)}
          {Array.from({ length: count }, (_, i) => {
            const key = keyOf(new Date(y, m, i + 1));
            const dayEvents = byDay[key] ?? [];
            const isLC = key === lcKey;
            const mark = isLC ? 'lc' : dayEvents[0]?.category;
            const label = `${new Date(y, m, i + 1).toLocaleDateString('en-IE', { weekday: 'long', day: 'numeric', month: 'long' }).replace(/,/g, '')}${key === todayKey ? ', today' : ''}${isLC ? ', Leaving Cert' : ''}${dayEvents.map(e => `, ${e.title}`).join('')}`;
            return (
              <button
                key={key}
                type="button"
                className={`gc8-day${key === todayKey ? ' gc8-day--today' : ''}`}
                aria-pressed={key === chosen}
                aria-label={label}
                onClick={() => setChosen(key)}
              >
                {i + 1}
                {mark ? <i className={`gc8-mk--${mark}`} aria-hidden="true" /> : null}
              </button>
            );
          })}
        </div>
      </div>
    );
  };

  const agenda = (
    <div className="gc8-agenda" aria-live="polite">
      <p className="gc8-ag-day">{chosenWords}</p>
      {onDay.length === 0 && chosen !== lcKey && <p className="gc8-meta">Nothing on this day.</p>}
      <div className="gc8-ag-list">
        {chosen === lcKey && (
          <div className="gc8-ag-ev"><i className="gc8-mk gc8-mk--lc" aria-hidden="true" /><span><span className="gc8-person">Leaving Cert</span><span className="gc8-meta">Exam</span></span><span className="gc8-readout">{toGo(daysTo(chosen))}</span></div>
        )}
        {onDay.map(ev => (
          <div key={ev.id} className="gc8-ag-ev">
            <i className={`gc8-mk gc8-mk--${ev.category}`} aria-hidden="true" />
            <span><span className="gc8-person">{ev.title}</span><span className="gc8-meta">{catWords[ev.category]} · {yearWords(ev.yearGroup)}</span></span>
            <span className="gc8-readout">{toGo(daysTo(ev.date))}</span>
          </div>
        ))}
        {next && (
          <div className="gc8-ag-ev">
            <i className={`gc8-mk gc8-mk--${next.category}`} aria-hidden="true" />
            <span><span className="gc8-person">Next: {next.title}</span><span className="gc8-meta">{shortDate(next.date)} · {yearWords(next.yearGroup)}</span></span>
            <span className="gc8-readout">{toGo(daysTo(next.date))}</span>
          </div>
        )}
      </div>
    </div>
  );
  const legend = (
    <ul className="gc8-legend" aria-label="Key">
      <li><i className="gc8-mk gc8-mk--today" />Today</li>
      <li><i className="gc8-mk gc8-mk--exams" />Exam</li>
      <li><i className="gc8-mk gc8-mk--deadlines" />Deadline</li>
      <li><i className="gc8-mk gc8-mk--school" />School</li>
      <li><i className="gc8-mk gc8-mk--other" />Other</li>
      <li><i className="gc8-mk gc8-mk--lc" />Leaving Cert</li>
    </ul>
  );

  return (
    <div className={`gc8-calwrap${beside ? ' gc8-calwrap--beside' : ''}`}>
      <div className="gc8-cal">
        <IconButton className="gc8-cal-step gc8-cal-step--prev" label="Previous month" onClick={() => step(-1)}
          icon={<ChevronLeft className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" />} />
        <IconButton className="gc8-cal-step gc8-cal-step--next" label="Next month" onClick={() => step(1)}
          icon={<ChevronRight className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" />} />
        <div className="gc8-cal-months">{Array.from({ length: months }, (_, i) => monthGrid(i))}</div>
      </div>
      {beside ? (
        <div className="gc8-cal-side">
          {countdown}
          {countdown ? <hr className="gc8-rule" /> : null}
          {agenda}
          {legend}
        </div>
      ) : (
        <>{agenda}{legend}</>
      )}
    </div>
  );
}
