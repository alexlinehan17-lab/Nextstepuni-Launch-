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
import React, { useState, useRef, useMemo } from 'react';
import { createPortal } from 'react-dom';
import {
  Eye, X, Check, ChevronDown, MapPin, ArrowDown, Building2, CircleHelp, Sparkles, ExternalLink,
} from 'lucide-react';
import { MotionDiv } from './Motion';
import { COLORS } from '../design/tokens';
import { type YearGroup } from './subjectData';
import { useModal } from '../hooks/useModal';
import { useCollegeCompass } from '../hooks/useCollegeCompass';
import PrimaryActionButton from './ui/PrimaryActionButton';
import { ToolJumpCard } from './ModuleShared';
import ToolIconBlob from './ToolIconBlob';
import { INSTITUTIONS } from './futureFinderData';
import HearMeter from './collegeCompass/HearMeter';
import DareGate from './collegeCompass/DareGate';
import MoneySorter from './collegeCompass/MoneySorter';
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

// ─── Rail dot ────────────────────────────────────────────────────────────────

const RailDot: React.FC<{ status: StopStatus; preview: boolean }> = ({ status, preview }) => {
  if (preview) {
    return <span className="block w-4 h-4 rounded-full border-2" style={{ borderColor: '#A8D5C9', backgroundColor: '#FFFFFF' }} />;
  }
  if (status === 'past') {
    return (
      <span className="inline-flex items-center justify-center w-4 h-4 rounded-full" style={{ backgroundColor: COLORS.success }}>
        <Check size={10} className="text-white" />
      </span>
    );
  }
  if (status === 'now') {
    return (
      <span className="relative block w-4 h-4">
        <span className="absolute inset-0 rounded-full animate-ping opacity-60" style={{ backgroundColor: COLORS.accent }} />
        <span className="absolute inset-0 rounded-full" style={{ backgroundColor: COLORS.accent }} />
      </span>
    );
  }
  return <span className="block w-4 h-4 rounded-full border-2" style={{ borderColor: '#d0cdc8', backgroundColor: '#FFFFFF' }} />;
};

// ─── Myth flip card ──────────────────────────────────────────────────────────

const MythFlip: React.FC<{ claim: string; verdict: 'true' | 'false'; explainer: string }> = ({ claim, verdict, explainer }) => {
  const [revealed, setRevealed] = useState(false);
  const isMyth = verdict === 'false';
  return (
    <button
      type="button"
      onClick={() => setRevealed(r => !r)}
      className="w-full text-left rounded-xl border-2 p-3.5 transition-colors"
      style={{
        borderColor: revealed ? COLORS.accent : COLORS.border,
        backgroundColor: revealed ? COLORS.accentTint : '#FFFFFF',
      }}
    >
      <div className="flex items-start gap-2.5">
        <span
          className="text-[9px] font-bold uppercase tracking-wide px-2 py-0.5 rounded-full shrink-0 mt-0.5"
          style={
            revealed
              ? (isMyth ? { backgroundColor: COLORS.accent, color: '#FFFFFF' } : { backgroundColor: COLORS.success, color: '#FFFFFF' })
              : { backgroundColor: '#F0EEEB', color: '#9e9186' }
          }
        >
          {revealed ? (isMyth ? 'Myth' : 'True') : 'Myth?'}
        </span>
        <div className="min-w-0">
          <p className="text-sm font-semibold text-[#1A1A1A]">“{claim}”</p>
          {revealed ? (
            <p className="text-xs leading-relaxed mt-1.5" style={{ color: COLORS.accentDarkText }}>{explainer}</p>
          ) : (
            <p className="text-[11px] font-medium text-zinc-400 mt-1">Tap to reveal</p>
          )}
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
              className="rounded-full border-2 px-3 py-1.5 text-xs font-semibold transition-colors"
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
          <button onClick={onClose} className="w-8 h-8 rounded-lg flex items-center justify-center hover:bg-black/5 dark:hover:bg-white/10 transition-colors shrink-0" aria-label="Close">
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

// ─── Journey stop card ───────────────────────────────────────────────────────

interface StopCardProps {
  stop: JourneyStop;
  state: StopState;
  mode: CompassMode;
  isOpen: boolean;
  onToggle: () => void;
  checklist: Record<string, 'in-progress' | 'done'>;
  onCycleItem: (key: string) => void;
  embedded?: React.ReactNode;
  cardRef: (el: HTMLDivElement | null) => void;
}

const STATUS_LABEL: Record<StopStatus, string> = { past: 'Done', now: 'Now', future: 'Ahead' };

const JourneyStopCard: React.FC<StopCardProps> = ({ stop, state, mode, isOpen, onToggle, checklist, onCycleItem, embedded, cardRef }) => {
  const preview = mode === 'orientation';
  const dateLabel = stop.end ? `${stop.start.label} → ${stop.end.label}` : stop.start.label;

  // Countdown chip (live mode, upcoming stops only)
  let countdown: string | null = null;
  if (!preview) {
    if (state.status === 'now') countdown = 'Happening now';
    else if (state.status === 'future' && state.daysUntilStart >= 0) {
      countdown = state.daysUntilStart === 0 ? 'Today' : `in ${state.daysUntilStart} day${state.daysUntilStart === 1 ? '' : 's'}`;
    }
  }

  return (
    <div className="relative pl-10" ref={cardRef} style={{ scrollMarginTop: '110px' }}>
      {/* rail dot */}
      <div className="absolute left-0 top-4">
        <RailDot status={state.status} preview={preview} />
      </div>

      <div
        className="rounded-2xl border-2 overflow-hidden transition-colors"
        style={{
          borderColor: COLORS.border,
          backgroundColor: '#FFFFFF',
          boxShadow: isOpen ? `4px 4px 0 0 ${COLORS.border}` : 'none',
          opacity: preview ? 0.92 : 1,
        }}
      >
        <button type="button" onClick={onToggle} className="w-full text-left px-4 py-3.5 flex items-center gap-3">
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 flex-wrap">
              <span className="font-mono text-[10px] font-bold tracking-wide px-2 py-0.5 rounded-md" style={{ backgroundColor: '#F0EEEB', color: '#7a7068' }}>{dateLabel}</span>
              {countdown && (
                <span className="text-[10px] font-bold uppercase tracking-wide px-2 py-0.5 rounded-full" style={{ backgroundColor: state.status === 'now' ? COLORS.accentTint : '#F0EEEB', color: state.status === 'now' ? COLORS.accentDarkText : '#7a7068' }}>
                  {countdown}
                </span>
              )}
              {!preview && state.status === 'past' && (
                <span className="text-[10px] font-bold uppercase tracking-wide px-2 py-0.5 rounded-full" style={{ backgroundColor: COLORS.successTint, color: COLORS.successDarkText }}>{STATUS_LABEL.past}</span>
              )}
            </div>
            <h3 className="font-serif text-lg font-bold text-[#1A1A1A] mt-1">{stop.title}</h3>
            <p className="text-xs text-[#7a7068] mt-0.5">{stop.tagline}</p>
          </div>
          <ChevronDown size={18} className="text-zinc-400 shrink-0 transition-transform" style={{ transform: isOpen ? 'rotate(180deg)' : 'rotate(0deg)' }} />
        </button>

        {isOpen && (
          <div className="px-4 pb-4 space-y-4">
            {/* why it matters — sanctioned left-border callout */}
            <div className="pl-3 py-1" style={{ borderLeft: `3px solid ${COLORS.accent}` }}>
              <p className="text-sm leading-relaxed" style={{ color: COLORS.accentDarkText }}>{stop.whyItMatters}</p>
            </div>

            {/* myths */}
            {stop.myths.length > 0 && (
              <div className="space-y-2">
                {stop.myths.map((m, i) => (
                  <MythFlip key={i} claim={m.claim} verdict={m.verdict} explainer={m.explainer} />
                ))}
              </div>
            )}

            {/* embedded mini-tool */}
            {embedded}

            {/* checklist (live mode only) */}
            {!preview && stop.checklistItems.length > 0 && (
              <div>
                <p className="text-[10px] font-bold uppercase tracking-[0.15em] text-zinc-400 mb-2">Your checklist</p>
                <div className="space-y-1.5">
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
                        className="w-full text-left rounded-xl border-2 px-3 py-2.5 flex items-start gap-2.5 transition-colors"
                        style={{ borderColor: done ? COLORS.success : inProg ? COLORS.accent : COLORS.border, backgroundColor: done ? COLORS.successTint : inProg ? COLORS.accentTint : '#FFFFFF' }}
                      >
                        <span className="inline-flex items-center justify-center w-5 h-5 rounded-md shrink-0 mt-0.5" style={{ backgroundColor: done ? COLORS.success : inProg ? COLORS.accent : '#F0EEEB' }}>
                          {done ? <Check size={13} className="text-white" /> : inProg ? <span className="block w-2.5 h-[2px] rounded-full bg-white" /> : null}
                        </span>
                        <span className="min-w-0 flex-1">
                          <span className={`block text-sm font-semibold ${done ? 'text-[#7a7068] line-through' : 'text-[#1A1A1A]'}`}>{item.label}</span>
                          {item.detail && <span className="block text-xs text-[#7a7068] mt-0.5">{item.detail}</span>}
                        </span>
                        {inProg && <span className="text-[10px] font-bold uppercase tracking-[0.1em] shrink-0 mt-1" style={{ color: COLORS.accentDarkText }}>In progress</span>}
                      </button>
                    );
                  })}
                </div>
              </div>
            )}

            {/* cross-links */}
            {stop.crossLinks.map(link => (
              <div key={link.toolId} className="-my-10">
                <ToolJumpCard toolId={link.toolId} title={link.title} description={link.description} ctaLabel="Open tool" />
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

// ─── Main component ──────────────────────────────────────────────────────────

interface CollegeCompassProps {
  uid?: string;
  yearGroup?: YearGroup;
}

const CollegeCompass: React.FC<CollegeCompassProps> = ({ uid, yearGroup }) => {
  const mode: CompassMode = yearGroup === '6th' ? 'live' : 'orientation';
  const preview = mode === 'orientation';

  const { state, cycleItemStatus, setHearIndicators, setDareCategory, setTargetInstitutions } = useCollegeCompass(uid);

  // Resolve dates/statuses once. `new Date()` is the project "today".
  const { entryYear, states, currentIndex } = useMemo(() => computeStopStates(new Date(), mode), [mode]);

  const initialOpen = preview ? JOURNEY_STOPS[0].id : JOURNEY_STOPS[currentIndex]?.id ?? JOURNEY_STOPS[0].id;
  const [openId, setOpenId] = useState<string>(initialOpen);
  const [showVerify, setShowVerify] = useState(false);
  const [showColleges, setShowColleges] = useState(false);

  const trailRef = useRef<HTMLDivElement | null>(null);
  const stopRefs = useRef<Record<string, HTMLDivElement | null>>({});

  const scrollToStop = (id: string) => {
    setOpenId(id);
    // allow the panel to open before scrolling
    window.requestAnimationFrame(() => stopRefs.current[id]?.scrollIntoView({ behavior: 'smooth', block: 'start' }));
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
    if (stopId === 'money-stops') return <MoneySorter />;
    return null;
  };

  return (
    <div className="w-full max-w-2xl mx-auto pb-12">
      {/* ── Hero ── */}
      <section
        className="rounded-3xl border-2 border-[#1A1A1A] dark:border-zinc-700 shadow-[5px_5px_0_0_#1A1A1A] dark:shadow-[5px_5px_0_0_#3f3f46] p-6 md:p-8 mt-4"
        style={{ backgroundColor: '#F0FAF8' }}
      >
        <div className="flex items-start gap-4">
          <ToolIconBlob toolId="college-compass" size={72} className="hidden sm:block" />
          <div className="min-w-0 flex-1">
            <p className="font-mono text-[10px] font-bold uppercase tracking-[0.2em] mb-1" style={{ color: '#2A7D6F' }}>{hero.eyebrow}</p>
            <h1 className="font-serif text-3xl md:text-4xl font-bold text-[#1A1A1A] leading-tight">{hero.title}</h1>
            <p className="text-sm text-[#5a544e] leading-relaxed mt-2 max-w-md">{hero.tagline}</p>
            <span className="inline-flex items-center gap-1.5 mt-3 px-3 py-1 rounded-full text-[11px] font-bold" style={{ backgroundColor: '#FFFFFF', border: `2px solid ${COLORS.border}`, color: '#1A1A1A' }}>
              <Sparkles size={12} style={{ color: '#2A7D6F' }} /> {entryYear} entry cycle
            </span>
          </div>
        </div>

        {preview && (
          <div className="mt-5 rounded-xl px-4 py-3" style={{ backgroundColor: '#FFFFFF', border: `2px solid ${COLORS.border}` }}>
            <p className="text-sm font-semibold text-[#1A1A1A]">You’re previewing the year ahead.</p>
            <p className="text-xs text-[#7a7068] mt-0.5">No deadlines to act on yet — explore each stop so none of it surprises you in 6th year.</p>
          </div>
        )}

        {/* mini-map */}
        <div className="mt-6 flex items-center gap-1.5">
          {JOURNEY_STOPS.map((stop, i) => {
            const st = states[i];
            return (
              <button
                key={stop.id}
                type="button"
                onClick={() => scrollToStop(stop.id)}
                className="group flex-1 flex flex-col items-center gap-1.5"
                title={stop.title}
              >
                <div className="w-full h-1 rounded-full" style={{ backgroundColor: preview ? '#A8D5C9' : st.status === 'past' ? COLORS.success : st.status === 'now' ? COLORS.accent : '#d0cdc8' }} />
                <span className="text-[9px] font-semibold text-zinc-400 group-hover:text-[#1A1A1A] truncate w-full text-center hidden sm:block">{stop.title}</span>
              </button>
            );
          })}
        </div>

        {/* CTA row */}
        <div className="mt-6 flex flex-wrap items-center gap-3">
          <PrimaryActionButton
            label={preview ? 'Explore the year' : 'Walk the trail'}
            icon={ArrowDown}
            variant="dark"
            onClick={() => trailRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' })}
          />
          <button
            type="button"
            onClick={() => setShowColleges(s => !s)}
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-full text-sm font-semibold transition-colors"
            style={{ backgroundColor: '#FFFFFF', border: `2px solid ${COLORS.border}`, color: '#1A1A1A' }}
          >
            <Building2 size={15} />
            {targetCodes.length > 0 ? `${targetCodes.length} target college${targetCodes.length === 1 ? '' : 's'}` : 'Set my target colleges'}
          </button>
          <button
            type="button"
            onClick={() => setShowVerify(true)}
            aria-label="How these dates work"
            className="inline-flex items-center gap-1.5 px-3 py-2.5 rounded-full text-xs font-semibold text-zinc-500 hover:text-[#1A1A1A] transition-colors"
          >
            <CircleHelp size={15} /> How dates work
          </button>
        </div>

        {/* target college picker */}
        {showColleges && (
          <div className="mt-4 rounded-xl p-4" style={{ backgroundColor: '#FFFFFF', border: `2px solid ${COLORS.border}` }}>
            <p className="text-xs text-[#7a7068] mb-2.5">Tap the colleges you’re aiming at — we’ll keep them in mind for the money stop.</p>
            <div className="flex flex-wrap gap-1.5">
              {TARGET_COLLEGE_CODES.map(code => {
                const on = targetCodes.includes(code);
                return (
                  <button
                    key={code}
                    type="button"
                    onClick={() => toggleCollege(code)}
                    className="rounded-full border-2 px-3 py-1.5 text-xs font-semibold transition-colors"
                    style={{ borderColor: on ? '#2A7D6F' : COLORS.border, backgroundColor: on ? '#E3F2EE' : '#FFFFFF', color: '#1A1A1A' }}
                    title={INSTITUTIONS[code]}
                  >
                    {code}
                  </button>
                );
              })}
            </div>
          </div>
        )}
      </section>

      {/* ── Sticky "Your Next Step" (live mode) ── */}
      {!preview && (
        <div className="sticky z-40 mt-4" style={{ top: 'calc(96px + var(--sat, 0px))' }}>
          {nextStep ? (
            <button
              type="button"
              onClick={() => scrollToStop(nextStep.stop.id)}
              className="w-full text-left rounded-2xl border-2 px-4 py-3 flex items-center gap-3 shadow-[3px_3px_0_0_#1A1A1A]"
              style={{ borderColor: COLORS.border, backgroundColor: COLORS.accentTint }}
            >
              <MapPin size={18} style={{ color: COLORS.accent }} className="shrink-0" />
              <div className="flex-1 min-w-0">
                <p className="text-[10px] font-bold uppercase tracking-[0.15em]" style={{ color: COLORS.accentDarkText }}>Your next step · {nextStep.stop.title}</p>
                <p className="text-sm font-semibold text-[#1A1A1A] truncate">{nextStep.item.label}</p>
              </div>
              {nextStep.st.status === 'future' && nextStep.st.daysUntilStart >= 0 && (
                <span className="text-[11px] font-bold shrink-0" style={{ color: COLORS.accentDarkText }}>
                  {nextStep.st.daysUntilStart === 0 ? 'today' : `${nextStep.st.daysUntilStart}d`}
                </span>
              )}
            </button>
          ) : (
            <div className="w-full rounded-2xl border-2 px-4 py-3 flex items-center gap-3 shadow-[3px_3px_0_0_#1A1A1A]" style={{ borderColor: COLORS.border, backgroundColor: COLORS.successTint }}>
              <Check size={18} style={{ color: COLORS.success }} className="shrink-0" />
              <p className="text-sm font-bold" style={{ color: COLORS.successDarkText }}>You’re all caught up — nice work.</p>
            </div>
          )}
        </div>
      )}

      {/* ── The trail ── */}
      <div ref={trailRef} className="mt-8 relative" style={{ scrollMarginTop: '110px' }}>
        {/* vertical rail */}
        <div className="absolute left-[7px] top-2 bottom-2 w-px" style={{ backgroundColor: '#d0cdc8' }} />
        <div className="space-y-3">
          {JOURNEY_STOPS.map((stop, i) => (
            <JourneyStopCard
              key={stop.id}
              stop={stop}
              state={states[i]}
              mode={mode}
              isOpen={openId === stop.id}
              onToggle={() => setOpenId(openId === stop.id ? '' : stop.id)}
              checklist={state.checklist}
              onCycleItem={cycleItemStatus}
              embedded={embeddedFor(stop.id)}
              cardRef={el => { stopRefs.current[stop.id] = el; }}
            />
          ))}
        </div>
      </div>

      {showVerify && <VerifyModal entryYear={entryYear} onClose={() => setShowVerify(false)} />}
    </div>
  );
};

export default CollegeCompass;
