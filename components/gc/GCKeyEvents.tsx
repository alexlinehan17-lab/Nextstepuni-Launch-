/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useMemo } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from '../Motion';
import { CalendarPlus, Trash2, Calendar, ChevronDown, Plus, X } from 'lucide-react';
import { db } from '../../firebase';
import { doc, getDoc, setDoc } from 'firebase/firestore';

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
}

export const GCKeyEvents: React.FC<GCKeyEventsProps> = ({ school, studentContext }) => {
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
  const saveEvents = async (updated: SchoolEvent[]) => {
    setEvents(updated);
    try {
      await setDoc(doc(db, 'gcEvents', school), { events: updated }, { merge: true });
    } catch (err) {
      console.error('[GCKeyEvents] Failed to save:', err);
    }
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

  const getCategoryConfig = (cat: EventCategory) =>
    EVENT_CATEGORIES.find(c => c.id === cat) ?? EVENT_CATEGORIES[3];

  const formatDate = (dateStr: string) => {
    const d = new Date(dateStr + 'T00:00:00');
    return d.toLocaleDateString('en-IE', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' });
  };

  const getDaysUntil = (dateStr: string) => {
    const d = new Date(dateStr + 'T00:00:00');
    const now = new Date();
    now.setHours(0, 0, 0, 0);
    return Math.ceil((d.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));
  };

  if (isLoading) {
    return (
      <div className="rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 p-5">
        <div className="h-4 w-32 bg-zinc-200 dark:bg-zinc-800 rounded animate-pulse mb-4" />
        <div className="space-y-3">
          {[1, 2, 3].map(i => (
            <div key={i} className="h-12 bg-zinc-100 dark:bg-zinc-800/50 rounded-lg animate-pulse" />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div id="gc-events" className="rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between px-5 pt-5 pb-3">
        <div className="flex items-center gap-2">
          <Calendar size={18} className="text-zinc-400" />
          <h3 className="text-sm font-bold text-zinc-800 dark:text-zinc-200">Key Dates & Events</h3>
          <span className="text-[10px] font-bold px-1.5 py-0.5 rounded-full bg-zinc-100 dark:bg-zinc-800 text-zinc-500 dark:text-zinc-400">
            {filteredEvents.length}
          </span>
        </div>
        <div className="flex items-center gap-2">
          {/* Year filter. JC schools see JC years + TY in the dropdown;
              the legacy 5th/6th + 'all' remain for senior. Rendered as a
              select rather than a pill row to fit 6 + 'all' cleanly. */}
          <select
            value={yearFilter}
            onChange={e => setYearFilter(e.target.value as 'all' | EventYearGroup)}
            className="px-2 py-1 rounded-md text-[10px] font-bold bg-zinc-100 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-200 border-0"
          >
            <option value="all">All years</option>
            <option value="1st">1st Year</option>
            <option value="2nd">2nd Year</option>
            <option value="3rd">3rd Year</option>
            <option value="TY">TY</option>
            <option value="5th">5th Year</option>
            <option value="6th">6th Year</option>
          </select>
          {/* Add button */}
          <button
            onClick={() => setShowAddForm(!showAddForm)}
            className="flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-indigo-50 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400 text-xs font-semibold hover:bg-indigo-100 dark:hover:bg-indigo-900/50 transition-colors"
          >
            {showAddForm ? <X size={12} /> : <Plus size={12} />}
            {showAddForm ? 'Cancel' : 'Add Event'}
          </button>
        </div>
      </div>

      {/* Add Form */}
      <AnimatePresence>
        {showAddForm && (
          <MotionDiv
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="overflow-hidden"
          >
            <div className="px-5 pb-4 space-y-3 border-b border-zinc-100 dark:border-zinc-800">
              {/* Preset quick-picks */}
              <div>
                <button
                  onClick={() => setShowPresets(!showPresets)}
                  className="flex items-center gap-1 text-[10px] font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider mb-2 hover:text-zinc-600 dark:hover:text-zinc-300"
                >
                  Quick Add <ChevronDown size={10} className={`transition-transform ${showPresets ? 'rotate-180' : ''}`} />
                </button>
                {showPresets && (
                  <div className="flex flex-wrap gap-1.5 mb-3">
                    {visiblePresets.length === 0 && (
                      <p className="text-[10px] italic text-zinc-400 dark:text-zinc-500">
                        No quick-add presets match this student's curriculum / year.
                      </p>
                    )}
                    {visiblePresets.map(preset => {
                      const cat = getCategoryConfig(preset.category);
                      return (
                        <button
                          key={preset.title}
                          onClick={() => handlePresetClick(preset)}
                          className="flex items-center gap-1 px-2 py-1 rounded-md bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-[10px] font-medium text-zinc-600 dark:text-zinc-400 hover:border-zinc-400 dark:hover:border-zinc-500 transition-colors"
                        >
                          <div className={`w-1.5 h-1.5 rounded-full ${cat.dotColor}`} />
                          {preset.title}
                        </button>
                      );
                    })}
                  </div>
                )}
              </div>

              {/* Form fields */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <input
                  type="text"
                  value={newTitle}
                  onChange={e => setNewTitle(e.target.value)}
                  placeholder="Event name"
                  className="px-3 py-2 rounded-lg border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-sm text-zinc-900 dark:text-white placeholder-zinc-400 dark:placeholder-zinc-500"
                />
                <input
                  type="date"
                  value={newDate}
                  onChange={e => setNewDate(e.target.value)}
                  className="px-3 py-2 rounded-lg border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-sm text-zinc-900 dark:text-white"
                />
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                {/* Year group — widened to JC years + TY + 'all' for mixed
                    cohorts. Rendered as a select to fit 8 options cleanly. */}
                <div>
                  <p className="text-[10px] font-bold text-zinc-400 dark:text-zinc-500 uppercase mb-1">Year Group</p>
                  <select
                    value={newYearGroup}
                    onChange={e => setNewYearGroup(e.target.value as EventYearGroup)}
                    className="w-full py-1.5 px-2 rounded-md text-[11px] font-bold bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-zinc-700 dark:text-zinc-200"
                  >
                    <option value="all">Everyone</option>
                    <option value="1st">1st Year</option>
                    <option value="2nd">2nd Year</option>
                    <option value="3rd">3rd Year</option>
                    <option value="TY">TY</option>
                    <option value="5th">5th Year</option>
                    <option value="6th">6th Year</option>
                    <option value="both">Both senior years</option>
                  </select>
                </div>
                {/* Category */}
                <div>
                  <p className="text-[10px] font-bold text-zinc-400 dark:text-zinc-500 uppercase mb-1">Category</p>
                  <div className="flex gap-1">
                    {EVENT_CATEGORIES.map(cat => (
                      <button
                        key={cat.id}
                        onClick={() => setNewCategory(cat.id)}
                        className={`flex-1 py-1.5 rounded-md text-[10px] font-bold border transition-all ${
                          newCategory === cat.id
                            ? `bg-zinc-50 dark:bg-zinc-800 border-zinc-400 dark:border-zinc-500 ${cat.color}`
                            : 'bg-white dark:bg-zinc-800 border-zinc-200 dark:border-zinc-700 text-zinc-400 dark:text-zinc-500'
                        }`}
                      >
                        {cat.label}
                      </button>
                    ))}
                  </div>
                </div>
                {/* Save button */}
                <div className="flex items-end">
                  <button
                    onClick={handleAdd}
                    disabled={!newTitle.trim() || !newDate}
                    className="w-full py-2 rounded-lg bg-indigo-500 text-white text-xs font-bold hover:bg-indigo-600 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
                  >
                    <CalendarPlus size={12} className="inline mr-1 -mt-0.5" />
                    Add Event
                  </button>
                </div>
              </div>
            </div>
          </MotionDiv>
        )}
      </AnimatePresence>

      {/* Events List */}
      <div className="px-5 py-4">
        {filteredEvents.length === 0 ? (
          <p className="text-sm text-zinc-400 dark:text-zinc-500 text-center py-6">
            No events yet. Add key dates for your students.
          </p>
        ) : (
          <div className="space-y-4">
            {/* Upcoming */}
            {upcomingEvents.length > 0 && (
              <div>
                <p className="text-[10px] font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider mb-2">Upcoming</p>
                <div className="space-y-1.5">
                  {upcomingEvents.map(event => {
                    const cat = getCategoryConfig(event.category);
                    const daysUntil = getDaysUntil(event.date);
                    return (
                      <div key={event.id} className="flex items-center gap-3 px-3 py-2.5 rounded-lg bg-zinc-50 dark:bg-zinc-800/50 group">
                        <div className={`w-2 h-2 rounded-full flex-shrink-0 ${cat.dotColor}`} />
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-semibold text-zinc-800 dark:text-zinc-200 truncate">{event.title}</p>
                          <p className="text-[10px] text-zinc-400 dark:text-zinc-500">
                            {formatDate(event.date)}
                            {event.yearGroup !== 'both' && event.yearGroup !== 'all' && (
                              <span className="ml-2 px-1.5 py-0.5 rounded bg-indigo-50 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400 font-bold">
                                {event.yearGroup === 'TY' ? 'TY' : `${event.yearGroup} Year`}
                              </span>
                            )}
                          </p>
                        </div>
                        <div className="flex items-center gap-2">
                          <span className={`text-xs font-bold ${daysUntil <= 7 ? 'text-red-500' : daysUntil <= 30 ? 'text-amber-500' : 'text-zinc-400 dark:text-zinc-500'}`}>
                            {daysUntil === 0 ? 'Today' : daysUntil === 1 ? 'Tomorrow' : `${daysUntil}d`}
                          </span>
                          <button
                            onClick={() => handleDelete(event.id)}
                            className="opacity-0 group-hover:opacity-100 p-1 rounded hover:bg-red-50 dark:hover:bg-red-900/20 text-zinc-300 hover:text-red-500 transition-all"
                          >
                            <Trash2 size={12} />
                          </button>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Past */}
            {pastEvents.length > 0 && (
              <div>
                <p className="text-[10px] font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider mb-2">Past</p>
                <div className="space-y-1.5">
                  {pastEvents.map(event => {
                    const cat = getCategoryConfig(event.category);
                    return (
                      <div key={event.id} className="flex items-center gap-3 px-3 py-2 rounded-lg opacity-50 group">
                        <div className={`w-2 h-2 rounded-full flex-shrink-0 ${cat.dotColor}`} />
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium text-zinc-500 dark:text-zinc-400 truncate line-through">{event.title}</p>
                          <p className="text-[10px] text-zinc-400 dark:text-zinc-500">
                            {formatDate(event.date)}
                            {event.yearGroup !== 'both' && event.yearGroup !== 'all' && (
                              <span className="ml-2 font-bold">{event.yearGroup === 'TY' ? 'TY' : `${event.yearGroup} Year`}</span>
                            )}
                          </p>
                        </div>
                        <button
                          onClick={() => handleDelete(event.id)}
                          className="opacity-0 group-hover:opacity-100 p-1 rounded hover:bg-red-50 dark:hover:bg-red-900/20 text-zinc-300 hover:text-red-500 transition-all"
                        >
                          <Trash2 size={12} />
                        </button>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
