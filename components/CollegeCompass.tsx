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
import { createPortal } from 'react-dom';
import {
  Eye, X, Check, ChevronDown, MapPin, Building2, CircleHelp, ExternalLink,
  ChevronLeft, ChevronRight,
} from 'lucide-react';
import { MotionDiv } from './Motion';
import { COLORS } from '../design/tokens';
import { type YearGroup } from './subjectData';
import { useModal } from '../hooks/useModal';
import { useCollegeCompass } from '../hooks/useCollegeCompass';
import { ToolJumpCard } from './ModuleShared';
import { INSTITUTIONS } from './futureFinderData';
import HearMeter from './collegeCompass/HearMeter';
import DareGate from './collegeCompass/DareGate';
import MoneySorter from './collegeCompass/MoneySorter';
import OpenDoor from './collegeCompass/OpenDoor';
import DocumentChecklist from './collegeCompass/DocumentChecklist';
import {
  JOURNEY_STOPS,
  HERO_COPY,
  RESTRICTED_COURSE_TYPES,
  COMPASS_SOURCES,
  CYCLE_NOTE,
  COMPASS_LAST_VERIFIED,
  computeStopStates,
  itemStatus,
  type CompassMode,
  type JourneyStop,
  type StopState,
  type StopStatus,
} from '../collegeCompassData';

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
      className="w-full text-left py-3.5 border-t border-[var(--border-soft)] first:border-t-0"
    >
      <div className="flex items-start gap-2.5">
        <span
          className="text-[9px] font-bold uppercase tracking-[0.12em] shrink-0 mt-0.5 text-[var(--ink-secondary)]"
        >
          {revealed ? (isMyth ? 'Myth' : 'True') : 'Reveal'}
        </span>
        <div className="min-w-0">
          <p className="text-sm font-semibold text-[var(--ink-primary)]">“{claim}”</p>
          {revealed ? (
            <p className="text-xs leading-relaxed mt-1.5 text-[var(--ink-secondary)]">{explainer}</p>
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
    <div className="rounded-2xl border-2 border-[#1A1A1A] dark:border-zinc-700 bg-white dark:bg-zinc-900 shadow-[4px_4px_0_0_#1A1A1A] dark:shadow-[4px_4px_0_0_#3f3f46] p-5">
      <p className="text-[10px] font-bold uppercase tracking-[0.15em] text-zinc-400 dark:text-zinc-500 mb-1">Quick check</p>
      <h4 className="font-serif text-lg font-bold text-[#1A1A1A] dark:text-white mb-3">Is my course restricted?</h4>
      <div className="flex flex-wrap gap-1.5 mb-3">
        {RESTRICTED_COURSE_TYPES.map(r => {
          const on = selectedId === r.id;
          return (
            <button
              key={r.id}
              type="button"
              onClick={() => setSelectedId(on ? null : r.id)}
              className="min-h-11 rounded-full border-2 px-3 text-xs font-semibold transition-colors"
              style={{ borderColor: on ? COLORS.accent : COLORS.border, backgroundColor: on ? COLORS.accentTint : '#FFFFFF', color: '#1A1A1A' }}
            >
              {r.label}
            </button>
          );
        })}
      </div>
      {selected && (
        <div
          className="rounded-xl px-4 py-3"
          style={{ backgroundColor: selected.mustLockByFeb1 ? COLORS.accentTint : COLORS.successTint }}
        >
          <p className="text-sm font-bold" style={{ color: selected.mustLockByFeb1 ? COLORS.accentDarkText : COLORS.successDarkText }}>
            {selected.mustLockByFeb1 ? 'Lock it in by 1 February' : 'No early gate'}
          </p>
          <p className="text-xs text-[#1A1A1A] mt-1 leading-relaxed">{selected.test}</p>
        </div>
      )}
    </div>
  );
};

// ─── Verify modal ────────────────────────────────────────────────────────────

const VerifyModal: React.FC<{ entryYear: number; onClose: () => void }> = ({ entryYear, onClose }) => {
  useModal(true, onClose);
  return createPortal(
    <MotionDiv
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-[200] flex items-center justify-center bg-black/55 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <MotionDiv
        initial={{ opacity: 0, scale: 0.96, y: 12 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        exit={{ opacity: 0, scale: 0.96, y: 12 }}
        transition={{ duration: 0.25, ease: [0.16, 1, 0.3, 1] as number[] }}
        className="bg-[#FAFBF6] dark:bg-zinc-900 rounded-2xl border-2 border-[#1A1A1A] dark:border-zinc-700 shadow-[6px_6px_0_0_#1A1A1A] dark:shadow-[6px_6px_0_0_#3f3f46] max-w-lg w-full max-h-[90vh] flex flex-col overflow-hidden"
        onClick={(e: React.MouseEvent) => e.stopPropagation()}
      >
        <div className="flex items-start justify-between p-6 pb-4 shrink-0">
          <div className="flex items-start gap-3 min-w-0">
            <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0" style={{ backgroundColor: 'rgba(242,107,31,0.12)' }}>
              <Eye size={20} style={{ color: COLORS.accent }} />
            </div>
            <div className="min-w-0">
              <h2 className="font-serif text-xl font-bold text-[#1A1A1A] dark:text-white">Before you trust these dates</h2>
              <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">How College Compass handles a moving target</p>
            </div>
          </div>
          <button onClick={onClose} className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl transition-colors hover:bg-black/5 dark:hover:bg-white/10" aria-label="Close">
            <X size={18} className="text-zinc-500" />
          </button>
        </div>

        <div className="px-6 pb-6 space-y-4 overflow-y-auto flex-1 min-h-0">
          <p className="text-sm text-zinc-700 dark:text-zinc-300 leading-relaxed">{CYCLE_NOTE}</p>
          <div className="rounded-xl p-3" style={{ backgroundColor: COLORS.successTint }}>
            <p className="text-sm font-bold" style={{ color: COLORS.successDarkText }}>You’re seeing the {entryYear} entry cycle.</p>
            <p className="text-xs mt-1 leading-relaxed" style={{ color: COLORS.successDarkText }}>
              Dates are stored without a year and resolved to whichever cycle is still ahead of you, so a passed deadline is never shown as upcoming.
            </p>
          </div>
          <div>
            <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 mb-2">Always confirm on the source</p>
            <div className="space-y-1.5">
              {COMPASS_SOURCES.map(s => (
                <a key={s.url} href={s.url} target="_blank" rel="noreferrer" className="flex items-center gap-1.5 text-sm font-semibold underline" style={{ color: COLORS.accentDarkText }}>
                  {s.label} <ExternalLink size={12} />
                </a>
              ))}
            </div>
          </div>
          <p className="text-[11px] text-zinc-400">Content last reviewed {COMPASS_LAST_VERIFIED}. Figures reflect the 2026 cycle and must be re-checked each year.</p>
        </div>

        <div className="px-6 pb-6 pt-2 shrink-0 border-t border-black/[0.04] dark:border-white/[0.06]">
          <button
            onClick={onClose}
            className="w-full flex items-center justify-center gap-2 px-5 py-3 rounded-2xl border-2 border-[#1A1A1A] text-[#FDF8F0] font-sans font-bold text-sm shadow-[4px_4px_0_0_#1A1A1A] hover:shadow-[6px_6px_0_0_#1A1A1A] hover:-translate-y-0.5 active:translate-x-1 active:translate-y-1 active:shadow-[0px_0px_0_0_#1A1A1A] transition-all duration-150"
            style={{ backgroundColor: COLORS.accent }}
          >
            Got it
          </button>
        </div>
      </MotionDiv>
    </MotionDiv>,
    document.body,
  );
};

// ─── Focused milestone workspace ─────────────────────────────────────────────

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
  const dateLabel = stop.end ? `${stop.start.label} → ${stop.end.label}` : stop.start.label;
  const firstIncompleteId = stop.checklistItems.find(item => itemStatus(checklist, `${stop.id}:${item.id}`) !== 'done')?.id;

  // Countdown chip (live mode, upcoming stops only)
  let countdown: string | null = null;
  if (!preview) {
    if (state.status === 'now') countdown = 'Happening now';
    else if (state.status === 'future' && state.daysUntilStart >= 0) {
      countdown = state.daysUntilStart === 0 ? 'Today' : `in ${state.daysUntilStart} day${state.daysUntilStart === 1 ? '' : 's'}`;
    }
  }

  return (
    <section
      id={panelId}
      role="tabpanel"
      aria-labelledby={tabId}
      tabIndex={-1}
      className="rounded-[24px] border-[1.5px] border-[#1A1A1A] dark:border-zinc-600 bg-[var(--surface-paper)] overflow-hidden"
    >
      <header className="grid gap-5 px-5 py-6 sm:px-7 sm:py-7 md:grid-cols-[minmax(0,1fr)_auto] md:items-start">
        <div>
          <div className="flex items-center gap-2 flex-wrap text-[10px] font-bold uppercase tracking-[0.16em] text-[var(--ink-secondary)]">
            <span>Stage {stop.order} of {JOURNEY_STOPS.length}</span>
            <span aria-hidden="true">·</span>
            <span>{dateLabel}</span>
          </div>
          <h2 className="mt-2 text-2xl sm:text-[28px] font-semibold tracking-[-0.025em] text-[var(--ink-primary)]">{stop.title}</h2>
          <p className="mt-2 max-w-2xl text-sm leading-relaxed text-[var(--ink-secondary)]">{stop.tagline}</p>
        </div>
        <div className="flex md:justify-end">
          {countdown ? (
            <span className="inline-flex border border-[var(--border-soft)] rounded-full px-3 py-1.5 text-[11px] font-semibold text-[var(--ink-primary)]">{countdown}</span>
          ) : !preview && state.status === 'past' ? (
            <span className="inline-flex items-center gap-1.5 text-[11px] font-semibold text-[var(--ink-secondary)]"><Check size={13} aria-hidden="true" /> {STATUS_LABEL.past}</span>
          ) : (
            <span className="inline-flex text-[11px] font-semibold text-[var(--ink-secondary)]">{preview ? 'Preview' : STATUS_LABEL[state.status]}</span>
          )}
        </div>
      </header>

      <div className="border-t border-[var(--border-soft)] px-5 py-6 sm:px-7 sm:py-7 space-y-7">
        <section aria-labelledby={`${panelId}-why`}>
          <p id={`${panelId}-why`} className="text-[10px] font-bold uppercase tracking-[0.16em] text-[var(--ink-secondary)]">Why this matters</p>
          <p className="mt-2 max-w-3xl text-sm leading-7 text-[var(--ink-primary)]">{stop.whyItMatters}</p>
        </section>

        {stop.checklistItems.length > 0 && (
          <section aria-labelledby={`${panelId}-checklist`}>
            <div className="flex items-end justify-between gap-4">
              <div>
                <p id={`${panelId}-checklist`} className="text-[10px] font-bold uppercase tracking-[0.16em] text-[var(--ink-secondary)]">{preview ? 'Be ready for' : 'Your actions'}</p>
                <p className="mt-1 text-xs text-[var(--ink-secondary)]">Tap an action to move it from not started, to in progress, to done.</p>
              </div>
              <span className="text-xs tabular-nums text-[var(--ink-secondary)]">
                {stop.checklistItems.filter(item => itemStatus(checklist, `${stop.id}:${item.id}`) === 'done').length}/{stop.checklistItems.length} done
              </span>
            </div>
            <div className="mt-3 border-y border-[var(--border-soft)]">
              {stop.checklistItems.map(item => {
                const key = `${stop.id}:${item.id}`;
                const status = itemStatus(checklist, key);
                const done = status === 'done';
                const inProg = status === 'in-progress';
                const next = status === 'not-started' ? 'mark in progress' : status === 'in-progress' ? 'mark done' : 'clear';
                return (
                  <button
                    key={item.id}
                    type="button"
                    onClick={() => onCycleItem(key)}
                    aria-label={`${item.label}. ${done ? 'Done' : inProg ? 'In progress' : 'Not started'}. Tap to ${next}.`}
                    className="w-full text-left py-3.5 border-t border-[var(--border-soft)] first:border-t-0 flex items-start gap-3 group"
                  >
                    <span
                      className="inline-flex items-center justify-center w-5 h-5 rounded-full border shrink-0 mt-0.5"
                      style={{ borderColor: done ? COLORS.success : inProg ? COLORS.accent : 'var(--border-soft)', backgroundColor: done ? COLORS.success : inProg ? COLORS.accent : 'transparent' }}
                    >
                      {done ? <Check size={12} className="text-white" aria-hidden="true" /> : inProg ? <span className="block w-2 h-[2px] rounded-full bg-white" /> : null}
                    </span>
                    <span className="min-w-0 flex-1">
                      <span className={`block text-sm font-medium ${done ? 'text-[var(--ink-secondary)] line-through' : 'text-[var(--ink-primary)]'}`}>{item.label}</span>
                      {item.detail && <span className="block text-xs leading-relaxed text-[var(--ink-secondary)] mt-1">{item.detail}</span>}
                    </span>
                    <span className="flex items-center gap-2 shrink-0 mt-0.5">
                      {!done && item.id === firstIncompleteId && <span className="hidden sm:inline text-[9px] font-bold uppercase tracking-[0.12em] text-[var(--ink-secondary)]">Next</span>}
                      <span className="text-[10px] font-semibold text-[var(--ink-secondary)]">{done ? 'Done' : inProg ? 'In progress' : 'Not started'}</span>
                    </span>
                  </button>
                );
              })}
            </div>
          </section>
        )}

        {embedded}

        {stop.myths.length > 0 && (
          <details className="border-y border-[var(--border-soft)] group">
            <summary className="list-none cursor-pointer py-4 flex items-center justify-between gap-3 text-sm font-semibold text-[var(--ink-primary)]">
              Common misconceptions
              <ChevronDown size={17} className="text-[var(--ink-secondary)] transition-transform group-open:rotate-180" aria-hidden="true" />
            </summary>
            <div className="pb-1">
              {stop.myths.map((m, i) => (
                <MythFlip key={i} claim={m.claim} verdict={m.verdict} explainer={m.explainer} />
              ))}
            </div>
          </details>
        )}

        {stop.crossLinks.map(link => (
          <div key={link.toolId} className="-my-10">
            <ToolJumpCard toolId={link.toolId} title={link.title} description={link.description} ctaLabel="Open tool" />
          </div>
        ))}
      </div>
    </section>
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

  const timelineRef = useRef<HTMLDivElement | null>(null);
  const workspaceRef = useRef<HTMLDivElement | null>(null);
  const tabRefs = useRef<Record<string, HTMLButtonElement | null>>({});

  const selectedIndex = Math.max(0, JOURNEY_STOPS.findIndex(stop => stop.id === selectedStopId));
  const selectedStop = JOURNEY_STOPS[selectedIndex];
  const selectedState = states[selectedIndex];

  const selectStop = (id: string, moveFocus = false, showWorkspace = false) => {
    setSelectedStopId(id);
    window.requestAnimationFrame(() => {
      tabRefs.current[id]?.scrollIntoView?.({ behavior: 'smooth', block: 'nearest', inline: 'center' });
      if (moveFocus) tabRefs.current[id]?.focus();
      if (showWorkspace) workspaceRef.current?.scrollIntoView?.({ behavior: 'smooth', block: 'start' });
    });
  };

  useEffect(() => {
    tabRefs.current[selectedStopId]?.scrollIntoView?.({ block: 'nearest', inline: 'center' });
  }, [selectedStopId]);

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

  const hero = HERO_COPY[mode];

  const embeddedFor = (stopId: string): React.ReactNode => {
    if (stopId === 'lock-in') return <RestrictedCheck />;
    if (stopId === 'access-window') {
      return (
        <div className="space-y-3">
          <HearMeter selected={state.hearIndicators ?? []} onChange={setHearIndicators} />
          <DareGate categoryId={state.dareCategoryId} onCategoryChange={setDareCategory} />
          <DocumentChecklist hearIndicators={state.hearIndicators ?? []} dareCategoryId={state.dareCategoryId} />
        </div>
      );
    }
    if (stopId === 'money-stops') {
      return (
        <div className="space-y-3">
          <OpenDoor />
          <MoneySorter />
        </div>
      );
    }
    return null;
  };

  return (
    <div className="w-full max-w-6xl mx-auto pb-12">
      {/* ── Hero ── */}
      <header className="pt-5 sm:pt-8 pb-6 sm:pb-8 border-b border-[var(--border-soft)]">
        <div className="flex flex-col gap-5 md:flex-row md:items-end md:justify-between">
          <div className="max-w-2xl">
            <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-[var(--ink-secondary)]">{hero.eyebrow}</p>
            <h1 className="mt-2 font-serif text-4xl sm:text-5xl font-bold tracking-[-0.035em] text-[var(--ink-primary)] leading-[0.95]">{hero.title}</h1>
            <p className="mt-3 text-sm sm:text-base text-[var(--ink-secondary)] leading-relaxed max-w-xl">{hero.tagline}</p>
          </div>
          <div className="flex flex-wrap items-center gap-2 md:justify-end">
            <span className="inline-flex items-center rounded-full border border-[var(--border-soft)] px-3 py-2 text-xs font-semibold text-[var(--ink-primary)]">
              {entryYear} entry
            </span>
            <button
              type="button"
              onClick={() => setShowColleges(s => !s)}
              aria-expanded={showColleges}
              className="inline-flex min-h-11 items-center gap-2 rounded-full border border-[var(--border-soft)] px-3 text-xs font-semibold text-[var(--ink-primary)] transition-colors hover:border-[#1A1A1A] dark:hover:border-zinc-400"
            >
              <Building2 size={14} aria-hidden="true" />
              {targetCodes.length > 0 ? `${targetCodes.length} target college${targetCodes.length === 1 ? '' : 's'}` : 'Target colleges'}
            </button>
            <button
              type="button"
              onClick={() => setShowVerify(true)}
              className="inline-flex min-h-11 items-center gap-1.5 rounded-full px-3 text-xs font-semibold text-[var(--ink-secondary)] transition-colors hover:text-[var(--ink-primary)]"
            >
              <CircleHelp size={14} aria-hidden="true" /> Dates and sources
            </button>
          </div>
        </div>

        {preview && (
          <div className="mt-6 max-w-2xl border-t border-[var(--border-soft)] pt-4">
            <p className="text-sm font-semibold text-[var(--ink-primary)]">You’re previewing the year ahead.</p>
            <p className="text-xs text-[var(--ink-secondary)] mt-1">Nothing is urgent yet. Explore each stage now so the application year feels familiar when it arrives.</p>
          </div>
        )}

        {/* target college picker */}
        {showColleges && (
          <section aria-label="Target colleges" className="mt-6 rounded-2xl border-[1.5px] border-[#1A1A1A] dark:border-zinc-600 p-4 sm:p-5 bg-[var(--surface-paper)]">
            <p className="text-xs text-[var(--ink-secondary)] mb-3">Choose the colleges you’re aiming at. We’ll keep them in mind when you reach funding and scholarships.</p>
            <div className="flex flex-wrap gap-1.5">
              {TARGET_COLLEGE_CODES.map(code => {
                const on = targetCodes.includes(code);
                return (
                  <button
                    key={code}
                    type="button"
                    onClick={() => toggleCollege(code)}
                    aria-pressed={on}
                    className="min-h-11 rounded-full border px-3 text-xs font-semibold text-[var(--ink-primary)] transition-colors"
                    style={{ borderColor: on ? COLORS.border : 'var(--border-soft)', backgroundColor: on ? 'var(--ink-primary)' : 'transparent', color: on ? 'var(--surface-paper)' : 'var(--ink-primary)' }}
                    title={INSTITUTIONS[code]}
                  >
                    {code}
                  </button>
                );
              })}
            </div>
          </section>
        )}
      </header>

      {/* ── One year, at a glance ── */}
      <section aria-labelledby="compass-timeline-heading" className="pt-6 sm:pt-8">
        <div className="flex items-end justify-between gap-4 px-1">
          <div>
            <p className="text-[10px] font-bold uppercase tracking-[0.18em] text-[var(--ink-secondary)]">Your application year</p>
            <h2 id="compass-timeline-heading" className="mt-1 text-lg font-semibold tracking-[-0.015em] text-[var(--ink-primary)]">Six stages, in order</h2>
          </div>
          <p className="hidden sm:block text-xs text-[var(--ink-secondary)]">Choose a stage to see what matters.</p>
        </div>

        <div ref={timelineRef} className="mt-5 overflow-x-auto overscroll-x-contain scroll-smooth snap-x snap-mandatory [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
          <div role="tablist" aria-label="College application stages" className="relative flex min-w-max gap-3 px-[13vw] md:grid md:min-w-0 md:grid-cols-6 md:gap-0 md:px-1">
            <div aria-hidden="true" className="absolute left-[76px] right-[76px] top-[17px] hidden h-px bg-[var(--border-soft)] md:block" />
            {JOURNEY_STOPS.map((stop, index) => {
              const stopState = states[index];
              const selected = selectedStopId === stop.id;
              const doneCount = stop.checklistItems.filter(item => itemStatus(state.checklist, `${stop.id}:${item.id}`) === 'done').length;
              const date = stop.start.label.replace(/ \(.+\)/, '');
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
                  onClick={() => selectStop(stop.id)}
                  onKeyDown={event => handleTimelineKeyDown(event, index)}
                  className={`group relative z-10 w-[74vw] max-w-[270px] snap-center rounded-2xl border px-4 py-4 text-center md:w-auto md:max-w-none md:rounded-none md:border-0 md:bg-transparent md:px-2 md:pb-4 md:pt-0 ${selected ? 'border-[var(--ink-primary)] bg-[var(--surface-paper)]' : 'border-[var(--border-soft)] bg-[var(--surface-soft)]'}`}
                >
                  <span
                    className="mx-auto flex h-9 w-9 items-center justify-center rounded-full border-[1.5px] bg-[var(--surface-paper)] transition-colors"
                    style={{ borderColor: selected ? 'var(--ink-primary)' : stopState.status === 'past' && !preview ? COLORS.success : 'var(--border-soft)' }}
                  >
                    {stopState.status === 'past' && !preview ? (
                      <Check size={14} style={{ color: selected ? 'var(--ink-primary)' : COLORS.success }} aria-hidden="true" />
                    ) : (
                      <span
                        className="block h-2.5 w-2.5 rounded-full"
                        style={{ backgroundColor: stopState.status === 'now' && !preview ? COLORS.accent : selected ? 'var(--ink-primary)' : 'var(--border-soft)' }}
                      />
                    )}
                  </span>
                  <span className="mt-2.5 block text-[10px] font-bold uppercase tracking-[0.12em] text-[var(--ink-secondary)]">{date}</span>
                  <span className={`mt-1 block text-xs leading-tight ${selected ? 'font-bold text-[var(--ink-primary)]' : 'font-medium text-[var(--ink-secondary)]'}`}>{stop.title}</span>
                  <span className="mt-1 block text-[9px] tabular-nums text-[var(--ink-secondary)]">
                    {doneCount > 0 ? `${doneCount}/${stop.checklistItems.length} done` : stopState.status === 'now' && !preview ? 'Now' : selected ? 'Selected' : '\u00a0'}
                  </span>
                </button>
              );
            })}
          </div>
        </div>

        <div className="flex items-center justify-between border-t border-[var(--border-soft)] py-3 md:hidden">
          <button
            type="button"
            onClick={() => selectStop(JOURNEY_STOPS[Math.max(0, selectedIndex - 1)].id, true)}
            disabled={selectedIndex === 0}
            className="inline-flex min-h-11 items-center gap-1.5 text-xs font-semibold text-[var(--ink-secondary)] disabled:opacity-30"
          >
            <ChevronLeft size={15} aria-hidden="true" /> Previous
          </button>
          <span className="text-[10px] font-semibold tabular-nums text-[var(--ink-secondary)]">{selectedIndex + 1} / {JOURNEY_STOPS.length}</span>
          <button
            type="button"
            onClick={() => selectStop(JOURNEY_STOPS[Math.min(JOURNEY_STOPS.length - 1, selectedIndex + 1)].id, true)}
            disabled={selectedIndex === JOURNEY_STOPS.length - 1}
            className="inline-flex min-h-11 items-center gap-1.5 text-xs font-semibold text-[var(--ink-secondary)] disabled:opacity-30"
          >
            Next <ChevronRight size={15} aria-hidden="true" />
          </button>
        </div>
      </section>

      {!preview && (
        <div className="border-y border-[var(--border-soft)] py-3.5">
          {nextStep ? (
            <button type="button" onClick={() => selectStop(nextStep.stop.id, false, true)} className="w-full flex items-center gap-3 text-left">
              <MapPin size={16} style={{ color: COLORS.accent }} className="shrink-0" aria-hidden="true" />
              <span className="min-w-0 flex-1 text-xs text-[var(--ink-secondary)]">
                <strong className="font-semibold text-[var(--ink-primary)]">Next action:</strong> {nextStep.item.label}
              </span>
              <span className="hidden sm:block text-[10px] font-bold uppercase tracking-[0.12em] text-[var(--ink-secondary)]">{nextStep.stop.title}</span>
              <ChevronRight size={15} className="shrink-0 text-[var(--ink-secondary)]" aria-hidden="true" />
            </button>
          ) : (
            <div className="flex items-center gap-2.5 text-sm font-semibold text-[var(--ink-primary)]">
              <Check size={16} style={{ color: COLORS.success }} aria-hidden="true" /> You’re all caught up.
            </div>
          )}
        </div>
      )}

      {/* ── One focused workspace ── */}
      <div ref={workspaceRef} className="mt-6 sm:mt-8" style={{ scrollMarginTop: '110px' }}>
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

      {showVerify && <VerifyModal entryYear={entryYear} onClose={() => setShowVerify(false)} />}
    </div>
  );
};

export default CollegeCompass;
