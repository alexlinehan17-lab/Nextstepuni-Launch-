/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * College Compass — Innovation Zone tool for active senior cycle (TY/5th/6th).
 *
 * A year-aware roadmap of the senior-cycle-to-college path: the CAO calendar
 * with HEAR, DARE and scholarship deadlines on their separate, earlier clock,
 * plus interactive eligibility self-checks. 6th years get the live layer
 * (countdowns + a saved checklist + a sticky "next step"); TY/5th years get a
 * calm preview of the cycle ahead.
 *
 * Scope: navigator + deadline-truth + eligibility self-checks only. All points
 * maths / course matching is pushed OUT to Future Finder, the CAO Points
 * Simulator and Points Passport via cross-links.
 */
import React, { useEffect, useMemo, useRef, useState } from 'react';
import { Building2, Check, ChevronDown, CircleHelp, LocateFixed } from 'lucide-react';
import { type YearGroup } from './subjectData';
import { useBackStep } from '../contexts/NavigationContext';
import { Button, TextButton } from './ui/Button';
import { ChoiceTile } from './ui/Choice';
import { PaperSheet, Row, List } from './ui/List';
import { Sheet } from './ui/Sheet';
import './college-compass-7.css';
import { useCollegeCompass } from '../hooks/useCollegeCompass';
import { ToolJumpCard } from './ModuleShared';
import { INSTITUTIONS } from './futureFinderData';
import HearMeter from './collegeCompass/HearMeter';
import DareGate from './collegeCompass/DareGate';
import MoneySorter from './collegeCompass/MoneySorter';
import OpenDoor from './collegeCompass/OpenDoor';
import DocumentChecklist from './collegeCompass/DocumentChecklist';
import { JOURNEY_STOPS, RESTRICTED_COURSE_TYPES, COMPASS_SOURCES, CYCLE_NOTE, COMPASS_LAST_VERIFIED, computeStopStates, itemStatus, type CompassMode, type JourneyStop, type StopState, type StopStatus } from '../collegeCompassData';

// Colleges worth offering as "target" chips (exclude the FET/apprenticeship
// catch-alls that aren't single institutions).
const TARGET_COLLEGE_CODES = Object.keys(INSTITUTIONS).filter(
  c => !['PLC', 'SOLAS', 'ETB'].includes(c),
);

// ─── Myth flip card ──────────────────────────────────────────────────────────

const MythFlip: React.FC<{ claim: string; verdict: 'true' | 'false'; explainer: string }> = ({ claim, verdict, explainer }) => {
  const [revealed, setRevealed] = useState(false);
  const isMyth = verdict === 'false';
  return (
    <button
      type="button"
      onClick={() => setRevealed(r => !r)}
      aria-expanded={revealed}
      className="cc7-myth"
    >
      <div className="cc7-myth-in">
        <span className="t-label cc7-myth-label">
          {revealed ? (isMyth ? 'Myth' : 'True') : 'Reveal'}
        </span>
        <div className="min-w-0">
          <p className="cc7-myth-claim">“{claim}”</p>
          {revealed ? (
            <p className="t-sub">{explainer}</p>
          ) : null}
        </div>
      </div>
    </button>
  );
};

// ─── Restricted-course quick check (Lock-In Day) ─────────────────────────────

const RestrictedCheck: React.FC = () => {
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const selected = RESTRICTED_COURSE_TYPES.find(r => r.id === selectedId) ?? null;
  return (
    <section className="cc7-tool" aria-label="Is my course restricted?">
      <p className="t-label cc7-label">Quick check</p>
      <h3 className="t-heading">Is my course restricted?</h3>
      <div className="cc7-picks">
        {RESTRICTED_COURSE_TYPES.map(r => <ChoiceTile key={r.id} compact kind="toggle" chosen={selectedId === r.id} label={r.label} onClick={() => setSelectedId(selectedId === r.id ? null : r.id)} />)}
      </div>
      {selected && (
        <div className="cc7-answer">
          <p className="t-row">{selected.mustLockByFeb1 ? 'Lock it in by 1 February' : 'No early gate'}</p>
          <p className="t-sub">{selected.test}</p>
        </div>
      )}
    </section>
  );
};

// ─── Dates and sources (the shared sheet) ────────────────────────────────────

const VerifySheet: React.FC<{ open: boolean; entryYear: number; onClose: () => void }> = ({ open, entryYear, onClose }) => (
  <Sheet open={open} onClose={onClose} title="Before you trust these dates" titleAlign="start" className="cc7-sheet"
    footer={<Button kind="main" size="lg" block onClick={onClose}>Got it</Button>}>
    <p className="t-sub">How College Compass handles a moving target</p>
    <p className="t-body">{CYCLE_NOTE}</p>
    <div className="cc7-answer">
      <p className="t-row">You’re seeing the {entryYear} entry cycle.</p>
      <p className="t-sub">Dates are stored without a year and resolved to whichever cycle is still ahead of you, so a passed deadline is never shown as upcoming.</p>
    </div>
    <p className="t-label cc7-label">Always confirm on the source</p>
    <List label="Sources">
      {COMPASS_SOURCES.map(source => <Row key={source.url} title={source.label} href={source.url} external />)}
    </List>
    <p className="t-meta">Content last reviewed {COMPASS_LAST_VERIFIED}. Figures reflect the 2026 cycle and must be re-checked each year.</p>
  </Sheet>
);

// ─── Stage panel ─────────────────────────────────────────────────────────────

interface MilestonePanelProps {
  stop: JourneyStop;
  state: StopState;
  mode: CompassMode;
  checklist: Record<string, 'in-progress' | 'done'>;
  onCycleItem: (key: string) => void;
  embedded?: React.ReactNode;
  tabId: string;
  panelId: string;
}

const STATUS_LABEL: Record<StopStatus, string> = { past: 'Done', now: 'Now', future: 'Ahead' };

const MilestonePanel: React.FC<MilestonePanelProps> = ({ stop, state, mode, checklist, onCycleItem, embedded, tabId, panelId }) => {
  const preview = mode === 'orientation';
  const dateLabel = stop.end ? `${stop.start.label} to ${stop.end.label}` : stop.start.label;
  const firstIncompleteId = stop.checklistItems.find(item => itemStatus(checklist, `${stop.id}:${item.id}`) !== 'done')?.id;
  const doneCount = stop.checklistItems.filter(item => itemStatus(checklist, `${stop.id}:${item.id}`) === 'done').length;

  // Countdown (live mode, upcoming stops only): "Happening now" is the one orange word.
  let status: React.ReactNode;
  if (preview) status = 'Preview';
  else if (state.status === 'now') status = <><span className="cc7-live">Happening now</span>{stop.end ? ` · until ${stop.end.label}` : ''}</>;
  else if (state.status === 'future' && state.daysUntilStart >= 0) status = state.daysUntilStart === 0 ? 'Today' : `in ${state.daysUntilStart} day${state.daysUntilStart === 1 ? '' : 's'}`;
  else if (state.status === 'past') status = <span className="cc7-inline"><Check size={14} aria-hidden="true" /> {STATUS_LABEL.past}</span>;
  else status = STATUS_LABEL[state.status];

  return (
    <PaperSheet className="cc7-stage" label={stop.title} fitTilt>
      <div id={panelId} role="tabpanel" aria-labelledby={tabId} tabIndex={-1} className="cc7-stage-in">
        <div className="cc7-stage-top">
          <div className="cc7-stage-name">
            <p className="t-label cc7-label">Stage {stop.order} of {JOURNEY_STOPS.length} · {dateLabel}</p>
            <h2 className="t-title cc7-title">{stop.title}</h2>
            <p className="t-sub">{stop.tagline}</p>
          </div>
          <p className="cc7-status">{status}</p>
        </div>
        <div className="cc7-cols">
          <section aria-labelledby={`${panelId}-why`} className="cc7-why">
            <p id={`${panelId}-why`} className="t-label cc7-label">Why this matters</p>
            <p className="t-body">{stop.whyItMatters}</p>
          </section>
          {stop.checklistItems.length > 0 && (
            <section aria-labelledby={`${panelId}-checklist`} className="cc7-acts">
              <div className="cc7-acts-head">
                <p id={`${panelId}-checklist`} className="t-label cc7-label">{preview ? 'Be ready for' : 'Your actions'}</p>
                <span className="t-meta">{doneCount} of {stop.checklistItems.length} done</span>
              </div>
              <p className="t-meta">Tap an action to move it from not started, to in progress, to done.</p>
              <ul className="cc7-list">
                {stop.checklistItems.map(item => {
                  const key = `${stop.id}:${item.id}`;
                  const st = itemStatus(checklist, key);
                  const done = st === 'done';
                  const inProg = st === 'in-progress';
                  const next = st === 'not-started' ? 'mark in progress' : st === 'in-progress' ? 'mark done' : 'clear';
                  return (
                    <li key={item.id}>
                      <button type="button" className="cc7-act" data-status={st} onClick={() => onCycleItem(key)}
                        aria-label={`${item.label}. ${done ? 'Done' : inProg ? 'In progress' : 'Not started'}. Tap to ${next}.`}>
                        <span className="cc7-mark" aria-hidden="true">{done ? <Check size={13} strokeWidth={2.6} /> : null}</span>
                        <span className="cc7-act-copy"><span className="cc7-act-title">{item.label}</span>{item.detail && <span className="t-meta">{item.detail}</span>}</span>
                        <span className="t-meta cc7-act-state">{!done && item.id === firstIncompleteId && !preview ? 'Next · ' : ''}{done ? 'Done' : inProg ? 'In progress' : 'Not started'}</span>
                      </button>
                    </li>
                  );
                })}
              </ul>
            </section>
          )}
        </div>

        {embedded}

        {stop.myths.length > 0 && (
          <details className="cc7-myths">
            <summary className="cc7-myths-head"><span>Common misconceptions</span><ChevronDown size={20} strokeWidth={1.75} aria-hidden="true" /></summary>
            <div>{stop.myths.map((m, i) => <MythFlip key={i} claim={m.claim} verdict={m.verdict} explainer={m.explainer} />)}</div>
          </details>
        )}

        {stop.crossLinks.map(link => (
          <ToolJumpCard key={link.toolId} toolId={link.toolId} title={link.title} description={link.description} ctaLabel="Open tool" />
        ))}
      </div>
    </PaperSheet>
  );
};

// ─── Main component ──────────────────────────────────────────────────────────

interface CollegeCompassProps {
  uid?: string;
  yearGroup?: YearGroup;
  examStartDate?: string | null;
}

const CollegeCompass: React.FC<CollegeCompassProps> = ({ uid, yearGroup, examStartDate }) => {
  const mode: CompassMode = yearGroup === '6th' ? 'live' : 'orientation';
  const preview = mode === 'orientation';

  const { state, cycleItemStatus, setHearIndicators, setDareCategory, setTargetInstitutions } = useCollegeCompass(uid);

  // Resolve dates/statuses once. `new Date()` is the project "today".
  const profileEntryYear = examStartDate ? Number(examStartDate.slice(0, 4)) : undefined;
  const { entryYear, states, currentIndex } = useMemo(
    () => computeStopStates(new Date(), mode, profileEntryYear),
    [mode, profileEntryYear],
  );

  const initialStopId = preview ? JOURNEY_STOPS[0].id : JOURNEY_STOPS[currentIndex]?.id ?? JOURNEY_STOPS[0].id;
  const [selectedStopId, setSelectedStopId] = useState<string>(initialStopId);
  const [showVerify, setShowVerify] = useState(false);
  const [showColleges, setShowColleges] = useState(false);
  // The HEAR self-check is its own screen, reached from The Access Window; the bar's Back returns.
  const [hearOpen, setHearOpen] = useState(false);
  useBackStep(hearOpen, () => setHearOpen(false));
  useEffect(() => { if (hearOpen) window.scrollTo?.({ top: 0 }); }, [hearOpen]);

  const workspaceRef = useRef<HTMLDivElement | null>(null);
  const tabRefs = useRef<Record<string, HTMLButtonElement | null>>({});

  const selectedIndex = Math.max(0, JOURNEY_STOPS.findIndex(stop => stop.id === selectedStopId));
  const selectedStop = JOURNEY_STOPS[selectedIndex];
  const selectedState = states[selectedIndex];

  const selectStop = (id: string, moveFocus = false, showWorkspace = false) => {
    setSelectedStopId(id);
    window.requestAnimationFrame(() => {
      if (moveFocus) tabRefs.current[id]?.focus();
      if (showWorkspace) workspaceRef.current?.scrollIntoView?.({ behavior: 'smooth', block: 'start' });
    });
  };

  const handleTimelineKeyDown = (event: React.KeyboardEvent<HTMLButtonElement>, index: number) => {
    let nextIndex: number;
    if (event.key === 'ArrowRight') nextIndex = Math.min(JOURNEY_STOPS.length - 1, index + 1);
    else if (event.key === 'ArrowLeft') nextIndex = Math.max(0, index - 1);
    else if (event.key === 'Home') nextIndex = 0;
    else if (event.key === 'End') nextIndex = JOURNEY_STOPS.length - 1;
    else return;
    event.preventDefault();
    selectStop(JOURNEY_STOPS[nextIndex].id, true);
  };

  // Next uncompleted checklist item across the whole trail (live mode only).
  const nextStep = useMemo(() => {
    if (preview) return null;
    for (let i = 0; i < JOURNEY_STOPS.length; i++) {
      const stop = JOURNEY_STOPS[i];
      for (const item of stop.checklistItems) {
        if (state.checklist[`${stop.id}:${item.id}`] !== 'done') {
          return { stop, item, st: states[i] };
        }
      }
    }
    return null;
  }, [preview, state.checklist, states]);

  const targetCodes = state.targetInstitutionCodes ?? [];
  const toggleCollege = (code: string) => {
    setTargetInstitutions(targetCodes.includes(code) ? targetCodes.filter(c => c !== code) : [...targetCodes, code]);
  };

  const embeddedFor = (stopId: string): React.ReactNode => {
    if (stopId === 'lock-in') return <RestrictedCheck />;
    if (stopId === 'access-window') {
      return (
        <div className="cc7-embedded">
          <List label="Self-checks">
            <Row title="Could I qualify for HEAR?" over="Self-check" meta={(state.hearIndicators ?? []).length ? `${(state.hearIndicators ?? []).length} ticked` : 'Tick what is true for your family'} onPress={() => setHearOpen(true)} />
          </List>
          <DareGate categoryId={state.dareCategoryId} onCategoryChange={setDareCategory} />
          <DocumentChecklist hearIndicators={state.hearIndicators ?? []} dareCategoryId={state.dareCategoryId} />
        </div>
      );
    }
    if (stopId === 'money-stops') {
      return (
        <div className="cc7-embedded">
          <OpenDoor />
          <MoneySorter />
        </div>
      );
    }
    return null;
  };

  if (hearOpen) {
    return (
      <div className="cc7 cc7-hear">
        <div className="cc7-hear-head">
          <p className="t-label cc7-label">The Access Window · Self-check</p>
          <h1 className="t-title cc7-title">Could I qualify for HEAR?</h1>
          <p className="t-sub">Tick what is true for your family. The meter shows where you would land.</p>
        </div>
        <HearMeter selected={state.hearIndicators ?? []} onChange={setHearIndicators} />
      </div>
    );
  }

  return (
    <div className="cc7">

      {preview && (
        <div className="cc7-preview">
          <p className="t-row">You’re previewing the year ahead.</p>
          <p className="t-sub">Nothing is urgent yet. Explore each stage now so the application year feels familiar when it arrives.</p>
        </div>
      )}

      {/* The six stages as a runway across the top: dates above, names below; the stage you are in
          filled; the chosen one's dot breathes in its ring (Alex, 26 Nov 2026). */}
      <section aria-labelledby="compass-timeline-heading" className="cc7-runway-sec">
        <div className="cc7-headgrid">
          <div className="cc7-top">
            <Button size="sm" aria-expanded={showColleges} onClick={() => setShowColleges(true)}><span className="cc7-inline"><Building2 size={16} strokeWidth={2} aria-hidden="true" />{targetCodes.length > 0 ? `${targetCodes.length} target college${targetCodes.length === 1 ? '' : 's'}` : 'Target colleges'}</span></Button>
            <TextButton tone="quiet" onClick={() => setShowVerify(true)}><span className="cc7-inline"><CircleHelp size={20} strokeWidth={1.75} aria-hidden="true" />Dates and sources</span></TextButton>
          </div>
          <div className="cc7-runhead">
            <p id="compass-timeline-heading" className="t-label cc7-label">Your application year</p>
            <span className="t-meta">{entryYear} entry · six stages</span>
          </div>
        </div>
        <div role="tablist" aria-label="College application stages" className="cc7-runway">
          {JOURNEY_STOPS.map((stop, index) => {
            const stopState = states[index];
            const selected = selectedStopId === stop.id;
            // The runway's short date ("~1 Mar", "~Apr", "~Aug"): the label without its note or its word.
            const date = stop.start.label.replace(/ \(.+\)/, '').replace(/^[A-Z][a-z]+ (?=~)|^[A-Z]{2,} /, '');
            return (
              <button
                key={stop.id}
                ref={element => { tabRefs.current[stop.id] = element; }}
                id={`compass-tab-${stop.id}`}
                type="button"
                role="tab"
                aria-label={stop.title}
                aria-selected={selected}
                aria-controls={`compass-panel-${stop.id}`}
                tabIndex={selected ? 0 : -1}
                data-now={!preview && stopState.status === 'now' ? '' : undefined}
                data-past={!preview && stopState.status === 'past' ? '' : undefined}
                onClick={() => selectStop(stop.id)}
                onKeyDown={event => handleTimelineKeyDown(event, index)}
                className="cc7-stop"
              >
                <span className="cc7-sdate">{date}</span>
                <span className="cc7-sdot" aria-hidden="true" />
                <span className="cc7-sname">{stop.title.replace(/^The /, '')}</span>
              </button>
            );
          })}
        </div>
      </section>

      {!preview && (
        <List label="Next action" className="cc7-next">
          {nextStep
            ? <Row icon={<LocateFixed size={20} strokeWidth={1.75} />} over="Next action" title={nextStep.item.label} onPress={() => selectStop(nextStep.stop.id, false, true)} />
            : <Row icon={<Check size={20} strokeWidth={1.75} />} title="You’re all caught up." />}
        </List>
      )}

      <div ref={workspaceRef} className="cc7-workspace">
        <MilestonePanel
          key={selectedStop.id}
          stop={selectedStop}
          state={selectedState}
          mode={mode}
          checklist={state.checklist}
          onCycleItem={cycleItemStatus}
          embedded={embeddedFor(selectedStop.id)}
          tabId={`compass-tab-${selectedStop.id}`}
          panelId={`compass-panel-${selectedStop.id}`}
        />
      </div>

      <Sheet open={showColleges} onClose={() => setShowColleges(false)} title="Target colleges" titleAlign="start" className="cc7-sheet">
        <p className="t-sub">Choose the colleges you’re aiming at. We’ll keep them in mind when you reach funding and scholarships.</p>
        <div className="cc7-colleges" role="group" aria-label="Target colleges">
          {TARGET_COLLEGE_CODES.map(code => <ChoiceTile key={code} kind="several" chosen={targetCodes.includes(code)} label={INSTITUTIONS[code] ?? code} meta={INSTITUTIONS[code] ? code : undefined} onClick={() => toggleCollege(code)} />)}
        </div>
      </Sheet>
      <VerifySheet open={showVerify} entryYear={entryYear} onClose={() => setShowVerify(false)} />
    </div>
  );
};

export default CollegeCompass;
