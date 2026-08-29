/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect, useCallback, useRef } from 'react';
import { AnimatePresence, useReducedMotion } from 'framer-motion';
import { MotionButton, MotionDiv, MotionSpan } from './Motion';
import { ArrowRight, RotateCcw } from 'lucide-react';
import { doc, setDoc, getDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { saveInBackground } from '../utils/firestoreWrite';
import { DEMO_STUDENT_UID } from '../data/devStudent';
import {
    type GameState, type Choice, type HistoryItem, type StatKey, type CapabilityKey, type JourneyEvidence, type Phase,
    type Location,
    STORY_DATA, ROUTE_RESOLVERS, INITIAL_GAME_STATE, PHASE_METADATA,
    ARCHETYPES, STAT_TO_MODULES, STAT_LABELS, CAPABILITY_KEYS, JOURNEY_SCORING_VERSION,
    applyJourneyChoice, createJourneyEvidence, getKeyTurningPoints,
    getStrongestCapability, getWeakestCapability, normaliseCapabilityImpact, normaliseEnergyImpact,
} from './journeySimulatorData';

export interface JourneyResult {
  endingId: string;
  finalStats?: GameState;
  completedAt?: string;
  decisionsCount?: number;
  scoringVersion?: number;
  history?: Array<{
    sceneId: string;
    choiceText: string;
    effects: Partial<GameState>;
    moduleLink?: Choice['moduleLink'];
  }>;
}

// ════════════════════════════════════════════════════════════════════════════
// DESIGN TOKENS — editorial / hand-drawn world
// ════════════════════════════════════════════════════════════════════════════

const PAPER = '#F6F1E6';        // warm cream, slightly toastier than the global cream so the simulator feels like a separate journal
const INK = '#1F1B17';          // near-black charcoal — never use #000
const INK_SOFT = '#5C544A';     // body copy
const INK_MUTE = '#8E8378';     // overlines, muted descriptors
const ACCENT = '#CC785C';       // brand orange — focal accent only

// Softened phase palette — muted, paper-friendly, never neon
const PHASE_TOKENS: Record<Phase, { ink: string; wash: string; tint: string; deep: string }> = {
  'Foundation':      { ink: '#5E8B7E', wash: '#E8EDE6', tint: '#D8E4DA', deep: '#3F6A5E' },
  'Pressure Cooker': { ink: '#B8843D', wash: '#EFE0BF', tint: '#E6CE94', deep: '#8C6022' },
  'Final Stretch':   { ink: '#B86F5A', wash: '#EFD9CD', tint: '#E0B8A2', deep: '#8C4D3B' },
};

const LOCATION_CONFIG: Record<Location, { label: string }> = {
    school: { label: 'School' }, home: { label: 'Home' }, 'exam-hall': { label: 'Exam Hall' },
    library: { label: 'Library' }, social: { label: 'Social' }, work: { label: 'Work' }, online: { label: 'Online' },
};

const editorialEase = [0.22, 1, 0.36, 1] as number[];

// Display labels — the Phase type stays 'Foundation' to avoid migrating
// the simulator data file, but every user-facing surface reads through this map.
const PHASE_DISPLAY: Record<Phase, string> = {
    'Foundation': 'New Beginnings',
    'Pressure Cooker': 'Crunch Time',
    'Final Stretch': 'Final Stretch',
};

// Mobile-friendly short labels for the bottom trail stepper. Used at <sm
// widths where the full labels would extend past the screen edge and get
// clipped beside their 36px circle.
const PHASE_DISPLAY_SHORT: Record<Phase, string> = {
    'Foundation': 'Begin',
    'Pressure Cooker': 'Crunch',
    'Final Stretch': 'Final',
};

// ════════════════════════════════════════════════════════════════════════════
// HAND-DRAWN SVG PRIMITIVES
// All strokes use slightly varied widths and "rough" pathing to feel sketched.
// Each motif keeps its own viewBox so callers control size via width/height.
// ════════════════════════════════════════════════════════════════════════════

const SketchedFlag: React.FC<{ size?: number; color?: string; className?: string }> = ({ size = 32, color = INK, className }) => (
    <svg width={size} height={size} viewBox="0 0 32 32" fill="none" className={className} aria-hidden>
        <path d="M8 28 L 8 4" stroke={color} strokeWidth={1.3} strokeLinecap="round" />
        <path d="M8 4 Q 18 6, 24 4 Q 22 10, 24 14 Q 16 12, 8 14 Z" fill={ACCENT} stroke={color} strokeWidth={1.1} strokeLinejoin="round" />
    </svg>
);

const SketchedHorizon: React.FC<{ phase: Phase; className?: string }> = ({ phase, className }) => {
    // A phase-specific landscape vignette: silhouettes + sun/path. Used in scenario hero card.
    const t = PHASE_TOKENS[phase];
    if (phase === 'Foundation') {
        // Custom-painted hand illustration for "New Beginnings" — anchored bottom so the
        // sun/horizon sit naturally above the choices when the panel is taller than the art.
        return (
            <img
                src="/assets/journey/new-beginnings.png"
                alt=""
                aria-hidden
                className={className}
                style={{ objectFit: 'contain', objectPosition: 'center bottom', padding: '12px' }}
            />
        );
    }
    if (phase === 'Pressure Cooker') {
        return (
            <img
                src="/assets/journey/crunch-time.png"
                alt=""
                aria-hidden
                className={className}
                style={{ objectFit: 'contain', objectPosition: 'center bottom', padding: '12px' }}
            />
        );
    }
    if (phase === 'Final Stretch') {
        return (
            <img
                src="/assets/journey/final-stretch.png"
                alt=""
                aria-hidden
                className={className}
                style={{ objectFit: 'contain', objectPosition: 'center bottom', padding: '12px' }}
            />
        );
    }
    if (phase === 'Pressure Cooker') {
        return (
            <svg viewBox="0 0 240 200" className={className} fill="none" aria-hidden preserveAspectRatio="xMidYMid slice">
                {/* Mountain pass + sun + winding path */}
                <path d="M0 170 L 60 80 L 110 130 L 150 95 L 200 150 L 240 110 L 240 200 L 0 200 Z" fill={t.tint} stroke={INK} strokeWidth={1.3} strokeLinejoin="round" />
                {/* Hatching */}
                <path d="M70 100 L 75 116" stroke={INK} strokeWidth={0.7} />
                <path d="M80 110 L 85 126" stroke={INK} strokeWidth={0.7} />
                <path d="M155 110 L 162 126" stroke={INK} strokeWidth={0.7} />
                <path d="M165 122 L 172 138" stroke={INK} strokeWidth={0.7} />
                {/* Path */}
                <path d="M30 195 Q 80 175, 110 160 Q 140 150, 170 140 Q 200 130, 220 122" stroke={INK} strokeWidth={1.2} strokeDasharray="2 4" fill="none" />
                {/* Sun behind peak — just a half */}
                <path d="M170 80 Q 180 56, 200 60" fill={t.tint} stroke={INK} strokeWidth={1.2} />
                <path d="M188 50 L 188 38" stroke={INK} strokeWidth={1} strokeLinecap="round" />
                <path d="M205 56 L 215 50" stroke={INK} strokeWidth={1} strokeLinecap="round" />
                {/* Cloud */}
                <path d="M48 64 Q 56 56, 70 60 Q 80 56, 86 64 Q 80 70, 64 68 Q 54 70, 48 64 Z" stroke={INK} strokeWidth={1} fill="none" />
            </svg>
        );
    }
    // Final Stretch — summit + flag
    return (
        <svg viewBox="0 0 240 200" className={className} fill="none" aria-hidden preserveAspectRatio="xMidYMid slice">
            <path d="M0 180 L 80 70 L 130 130 L 160 90 L 240 180 L 240 200 L 0 200 Z" fill={t.tint} stroke={INK} strokeWidth={1.3} strokeLinejoin="round" />
            <path d="M90 90 L 95 110" stroke={INK} strokeWidth={0.7} />
            <path d="M100 100 L 105 120" stroke={INK} strokeWidth={0.7} />
            <path d="M170 110 L 176 130" stroke={INK} strokeWidth={0.7} />
            {/* Summit flag */}
            <path d="M80 70 L 80 42" stroke={INK} strokeWidth={1.3} strokeLinecap="round" />
            <path d="M80 42 Q 96 44, 104 42 Q 100 50, 104 58 Q 92 56, 80 58 Z" fill={ACCENT} stroke={INK} strokeWidth={1.1} strokeLinejoin="round" />
            <path d="M30 195 Q 60 178, 75 80" stroke={INK} strokeWidth={1.2} strokeDasharray="2 4" fill="none" />
        </svg>
    );
};

// Sun + line overline rule, used to mark sections (sunburst underline)
const SunburstRule: React.FC<{ width?: number; color?: string }> = ({ width = 80, color = ACCENT }) => (
    <svg width={width} height={14} viewBox="0 0 80 14" fill="none" aria-hidden>
        <path d="M2 9 L 78 9" stroke={color} strokeWidth={1.4} strokeLinecap="round" />
        <circle cx="14" cy="9" r="3" fill={color} />
        <path d="M14 4 L 14 1"  stroke={color} strokeWidth={1.1} strokeLinecap="round" />
        <path d="M9 6  L 7 3"   stroke={color} strokeWidth={1.1} strokeLinecap="round" />
        <path d="M19 6 L 21 3"  stroke={color} strokeWidth={1.1} strokeLinecap="round" />
    </svg>
);

// ════════════════════════════════════════════════════════════════════════════
// JOURNEY PROGRESS TRAIL — sketchy footer trail used on scenario + transition
// 8 stylized nodes split across 3 phases, dashed connectors, flag at end.
// ════════════════════════════════════════════════════════════════════════════

const TRAIL_LAYOUT: { i: number; phase: Phase }[] = [
    { i: 1, phase: 'Foundation' },
    { i: 2, phase: 'Pressure Cooker' },
    { i: 3, phase: 'Final Stretch' },
];

const PHASE_INDEX: Record<Phase, number> = {
    'Foundation': 1,
    'Pressure Cooker': 2,
    'Final Stretch': 3,
};

const JourneyTrail: React.FC<{ currentPhase: Phase; compact?: boolean }> = ({ currentPhase, compact = false }) => {
    const step = PHASE_INDEX[currentPhase];
    return (
        <div className={`w-full ${compact ? 'mt-3' : 'mt-2'}`}>
            <div className="relative flex items-start justify-between gap-1 px-2">
                {TRAIL_LAYOUT.map((node, idx) => {
                    const active = node.i === step;
                    const past = node.i < step;
                    const labelColor = active
                        ? PHASE_TOKENS[node.phase].deep
                        : INK_MUTE;
                    return (
                        <React.Fragment key={node.i}>
                            <div className="relative flex flex-col items-center shrink-0" style={{ width: 36 }}>
                                <div
                                    className="flex items-center justify-center font-serif text-[14px] font-semibold transition-colors"
                                    style={{
                                        width: 36, height: 36, borderRadius: '50%',
                                        border: `1.8px solid ${active ? ACCENT : INK}`,
                                        background: active ? PAPER : past ? PHASE_TOKENS[node.phase].tint : PAPER,
                                        color: active ? ACCENT : past ? INK : INK_MUTE,
                                        transform: `rotate(${(idx % 2 === 0 ? -1 : 1) * 0.6}deg)`,
                                        boxShadow: active ? `0 0 0 3px ${PAPER}, 0 0 0 4.5px ${ACCENT}33` : undefined,
                                    }}
                                >
                                    {node.i}
                                </div>
                                {!compact && (
                                    <>
                                        <span
                                            className="mt-2 text-[10px] font-semibold uppercase tracking-[0.18em] whitespace-nowrap text-center hidden sm:inline"
                                            style={{ color: labelColor }}
                                        >
                                            {PHASE_DISPLAY[node.phase]}
                                        </span>
                                        <span
                                            className="mt-2 text-[10px] font-semibold uppercase tracking-[0.18em] whitespace-nowrap text-center sm:hidden"
                                            style={{ color: labelColor }}
                                        >
                                            {PHASE_DISPLAY_SHORT[node.phase]}
                                        </span>
                                    </>
                                )}
                            </div>
                            {idx < TRAIL_LAYOUT.length - 1 && (
                                <div
                                    className="flex-1 h-px self-start shrink"
                                    aria-hidden
                                    style={{
                                        marginTop: 17,
                                        backgroundImage: `radial-gradient(circle, ${INK_MUTE} 1px, transparent 1.2px)`,
                                        backgroundSize: '6px 2px',
                                        backgroundRepeat: 'repeat-x',
                                        backgroundPosition: 'center',
                                    }}
                                />
                            )}
                        </React.Fragment>
                    );
                })}
                <div className="shrink-0 self-start" style={{ marginTop: 5 }}>
                    <SketchedFlag size={26} />
                </div>
            </div>
        </div>
    );
};

// ════════════════════════════════════════════════════════════════════════════
// EDITORIAL PRIMITIVES
// ════════════════════════════════════════════════════════════════════════════

const Overline: React.FC<{ children: React.ReactNode; color?: string; className?: string }> = ({ children, color = INK_MUTE, className = '' }) => (
    <p className={`text-[10px] font-semibold uppercase tracking-[0.22em] ${className}`} style={{ color }}>{children}</p>
);

// ════════════════════════════════════════════════════════════════════════════
// PHASE TRANSITION — illustrated chapter divider (not a flat splash)
// ════════════════════════════════════════════════════════════════════════════

const PhaseTransition: React.FC<{ phase: Phase; onComplete: () => void }> = ({ phase, onComplete }) => {
    useEffect(() => {
        const timer = setTimeout(onComplete, 6000);
        return () => clearTimeout(timer);
    }, [onComplete]);

    const meta = PHASE_METADATA.find(p => p.name === phase);
    const t = PHASE_TOKENS[phase];

    return (
        <MotionDiv
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.6 }}
            onClick={onComplete}
            className="cursor-pointer fixed inset-0 z-[70] flex items-center justify-center overflow-y-auto"
            // pb keeps the centered transition card above the fixed mobile bottom
            // nav (z-90 sits in front of this overlay at z-70). sat keeps the top
            // clear of the dynamic island.
            style={{
                background: PAPER,
                paddingTop: 'var(--sat, 0px)',
                paddingBottom: 'calc(96px + var(--sab, 0px))',
            }}
        >
            <div
                className="relative w-full max-w-3xl mx-4 my-8 overflow-hidden"
                style={{
                    background: t.wash,
                    border: `1.5px solid ${INK}`,
                    borderRadius: 18,
                    boxShadow: '0 10px 40px rgba(31,27,23,0.10), 0 2px 0 rgba(31,27,23,0.06)',
                }}
            >
                {/* Asymmetric two-column composition: copy left, illustration right */}
                <div className="grid md:grid-cols-2 gap-0">
                    <div className="p-8 md:p-10 flex flex-col justify-between min-h-[320px]">
                        <MotionDiv initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2, duration: 0.6 }}>
                            <Overline color={t.deep}>{meta?.months}</Overline>
                            <h2
                              className="font-serif font-bold mt-4 leading-[1.05]"
                              style={{
                                color: INK,
                                fontSize: 'clamp(36px, 6vw, 56px)',
                                letterSpacing: '-0.02em',
                              }}
                            >
                              {PHASE_DISPLAY[phase]}
                            </h2>
                            <p className="font-serif text-lg mt-5 leading-relaxed max-w-sm" style={{ color: INK_SOFT }}>
                                {meta?.subtitle}
                            </p>
                        </MotionDiv>

                        <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 1.2 }} className="mt-10 flex items-center gap-3">
                            <span className="font-sans text-[12px]" style={{ color: INK_SOFT }}>Tap anywhere to continue</span>
                            <svg width="36" height="12" viewBox="0 0 36 12" fill="none" aria-hidden>
                                <path d="M2 6 Q 16 2, 32 6" stroke={INK} strokeWidth={1.3} strokeLinecap="round" fill="none" />
                                <path d="M28 2 L 33 6 L 28 10" stroke={INK} strokeWidth={1.3} strokeLinecap="round" strokeLinejoin="round" fill="none" />
                            </svg>
                        </MotionDiv>
                    </div>

                    {/* Phase-specific illustration */}
                    <div className="relative min-h-[280px] md:min-h-full">
                        <SketchedHorizon phase={phase} className="absolute inset-0 w-full h-full" />
                    </div>
                </div>

                {/* Trail along bottom inside the card */}
                <div className="px-8 md:px-10 pb-7 pt-4">
                    <JourneyTrail currentPhase={phase} />
                </div>
            </div>
        </MotionDiv>
    );
};

// ════════════════════════════════════════════════════════════════════════════
// TYPING TEXT — italic serif narration
// ════════════════════════════════════════════════════════════════════════════

const TypingText: React.FC<{ text: string; sceneId: string }> = ({ text, sceneId }) => {
    const words = text.split(' ');
    const reducedMotion = useReducedMotion();
    const [visibleCount, setVisibleCount] = useState(reducedMotion ? words.length : 0);
    const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

    useEffect(() => {
        if (reducedMotion) {
            setVisibleCount(words.length);
            return;
        }
        setVisibleCount(0);
        intervalRef.current = setInterval(() => {
            setVisibleCount(prev => {
                if (prev >= words.length) { if (intervalRef.current) clearInterval(intervalRef.current); return prev; }
                return prev + 1;
            });
        }, 35);
        return () => { if (intervalRef.current) clearInterval(intervalRef.current); };
    }, [sceneId, words.length, reducedMotion]);

    return (
        <p className="font-serif text-[16px] sm:text-[17px] leading-[1.5] italic" style={{ color: INK }}>
            <span className="sr-only">{text}</span>
            <span aria-hidden="true">
            {words.map((word, i) => (
                <MotionSpan key={`${sceneId}-${i}`} initial={false} animate={{ opacity: i < visibleCount ? 1 : 0 }} transition={{ duration: 0.15 }} className="inline">
                    {word}{' '}
                </MotionSpan>
            ))}
            </span>
        </p>
    );
};

// ════════════════════════════════════════════════════════════════════════════
// CHOICE BUTTON — paper card, sketched A/B/C pill, phase-tint hover
// ════════════════════════════════════════════════════════════════════════════

const ChoiceButton: React.FC<{
    choice: Choice;
    onChoose: (choice: Choice) => void; disabled?: boolean; chosen?: boolean;
    index?: number; phase: Phase;
}> = ({ choice, onChoose, disabled, chosen, index = 0, phase }) => {
    const letter = String.fromCharCode(65 + index);
    const t = PHASE_TOKENS[phase];

    if (disabled && !chosen) {
        return (
            <div className="px-4 py-3 mb-3 opacity-40" style={{ background: '#ffffff', border: `1px solid ${INK}10`, borderRadius: 12 }}>
                <div className="flex items-center gap-3">
                    <span className="font-serif font-bold flex items-center justify-center shrink-0" style={{ width: 28, height: 28, borderRadius: '50%', border: `1.4px solid ${INK_MUTE}55`, color: INK_MUTE, fontSize: 12 }}>{letter}</span>
                    <p className="text-[15px]" style={{ color: INK_MUTE }}>{choice.text}</p>
                </div>
            </div>
        );
    }

    if (chosen) {
        return (
            <div className="px-4 py-3 mb-3" style={{ background: t.wash, border: `1.5px solid ${t.ink}`, borderRadius: 12, boxShadow: `0 2px 0 ${t.ink}22` }}>
                <div className="flex items-center gap-3">
                    <span className="font-serif font-bold flex items-center justify-center shrink-0" style={{
                        width: 28, height: 28, borderRadius: '50%', background: t.tint, color: t.deep, border: `1.4px solid ${t.ink}`, fontSize: 12,
                    }}>{letter}</span>
                    <p className="text-[15px] font-semibold" style={{ color: INK }}>{choice.text}</p>
                </div>
            </div>
        );
    }

    return (
        <MotionButton
            onClick={() => onChoose(choice)}
            whileTap={{ scale: 0.99 }}
            className="w-full text-left px-4 py-3.5 mb-3 transition-all"
            style={{
                // Pure white card — keeps choices crisp against the warm phase wash background.
                background: '#ffffff',
                border: `1px solid ${INK}1a`,
                borderRadius: 12,
                boxShadow: '0 1px 2px rgba(31,27,23,0.04), 0 4px 14px rgba(31,27,23,0.05)',
            }}
            onMouseEnter={(e: any) => {
                e.currentTarget.style.borderColor = `${t.ink}aa`;
                e.currentTarget.style.boxShadow = `0 2px 0 ${t.ink}22, 0 8px 18px rgba(31,27,23,0.08)`;
            }}
            onMouseLeave={(e: any) => {
                e.currentTarget.style.borderColor = `${INK}1a`;
                e.currentTarget.style.boxShadow = '0 1px 2px rgba(31,27,23,0.04), 0 4px 14px rgba(31,27,23,0.05)';
            }}
        >
            <div className="flex items-start gap-3">
                <span className="font-serif font-bold flex items-center justify-center shrink-0 mt-0.5" style={{
                    width: 28, height: 28, borderRadius: '50%',
                    background: t.tint, color: t.deep,
                    border: `1.4px solid ${t.ink}`, fontSize: 12,
                    transform: `rotate(${(index % 2 === 0 ? -1 : 1) * 1.2}deg)`,
                }}>{letter}</span>
                <p className="flex-1 min-w-0 text-[15px] leading-snug" style={{ color: INK }}>{choice.text}</p>
            </div>
        </MotionButton>
    );
};

// ════════════════════════════════════════════════════════════════════════════
// JOURNEY OUTCOME — product-native decision dashboard
// ════════════════════════════════════════════════════════════════════════════

const RESULT_STAT_ORDER: CapabilityKey[] = [...CAPABILITY_KEYS];
const RESULT_EFFECT_ORDER: StatKey[] = ['energy', ...CAPABILITY_KEYS];

const RESULT_NEXT_ACTION: Record<CapabilityKey, string> = {
    academicCap: 'Replace passive review with retrieval practice and timed application.',
    socialSupport: 'Bring one trusted person into the plan before pressure builds.',
    systemSavvy: 'Map the deadlines, points and supports that can change your options.',
    resilience: 'Pre-plan what you will do in the 24 hours after a setback.',
};

const formatSignedValue = (value: number): string => value > 0 ? `+${value}` : `${value}`;

const formatEffects = (effects: Partial<GameState>): string => {
    const entries = RESULT_EFFECT_ORDER
        .filter(stat => typeof effects[stat] === 'number' && effects[stat] !== 0)
        .map(stat => ({
            stat,
            value: stat === 'energy'
                ? normaliseEnergyImpact(effects[stat] as number)
                : normaliseCapabilityImpact(effects[stat] as number),
        }))
        .filter(({ value }) => value !== 0)
        .sort((a, b) => Number(b.value > 0) - Number(a.value > 0))
        .map(({ stat, value }) => `${formatSignedValue(value)} ${STAT_LABELS[stat]}`);
    return entries.join(' · ') || 'No score change';
};

export const JourneyOutcomeReport: React.FC<{
    endingId: string;
    gameState: GameState;
    history: HistoryItem[];
    decisionsCount?: number;
    onRestart: () => void;
    onSelectModule?: (moduleId: string) => void;
}> = ({ endingId, gameState, history, decisionsCount, onRestart, onSelectModule }) => {
    const archetype = ARCHETYPES[endingId];
    const endScene = STORY_DATA[endingId];
    const strongestCapabilities = getStrongestCapability(gameState);
    const weakestCapabilities = getWeakestCapability(gameState);
    const strongest = strongestCapabilities[0];
    const weakest = weakestCapabilities[0];
    const strongestLabel = strongestCapabilities.map(stat => STAT_LABELS[stat]).join(' + ');
    const weakestLabel = weakestCapabilities.map(stat => STAT_LABELS[stat]).join(' + ');
    const turningPoints = getKeyTurningPoints(history);
    const recommendedModules = STAT_TO_MODULES[weakest];
    const primaryModule = recommendedModules[0];
    const outcomeTitle = archetype?.title || endScene?.title || 'Your journey result';
    const summary = endScene?.text || archetype?.description || 'Your choices created a distinct decision profile.';
    const finalDecisionCount = decisionsCount ?? history.length;

    return (
        <MotionDiv
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.34, ease: editorialEase }}
            className="pb-16 pt-3 text-[var(--ink-primary)]"
        >
            <header className="border-b border-[var(--outline-soft)] pb-7 sm:pb-9">
                <div className="grid gap-7 lg:grid-cols-[minmax(0,1fr)_250px] lg:items-end lg:gap-12">
                    <div className="max-w-[780px]">
                        <p className="text-[10px] font-bold uppercase tracking-[.2em] text-[var(--ink-muted)]">Academic journey · outcome</p>
                        <h1 className="mt-4 max-w-[720px] font-serif text-[clamp(2.5rem,6vw,5.4rem)] font-medium leading-[.94] tracking-[-.045em] text-[var(--ink-primary)]">
                            {outcomeTitle}
                        </h1>
                        <p className="mt-5 max-w-[690px] text-[15px] leading-7 text-[var(--ink-secondary)] sm:text-base">
                            {summary}
                        </p>
                    </div>
                    <div className="border-l-2 border-[#F26B1F] pl-4 lg:mb-1">
                        <p className="text-[10px] font-bold uppercase tracking-[.18em] text-[var(--ink-muted)]">Your clearest signal</p>
                        <p className="mt-2 font-serif text-[26px] font-semibold leading-tight text-[var(--ink-primary)]">{strongestLabel}</p>
                        <p className="mt-1 text-sm text-[var(--ink-secondary)]">The quality your choices relied on most.</p>
                    </div>
                </div>

                <dl className="mt-8 grid border-y border-[var(--outline-soft)] sm:grid-cols-2 lg:grid-cols-4 lg:divide-x lg:divide-[var(--outline-soft)]">
                    <div className="flex items-baseline justify-between gap-5 border-b border-[var(--outline-soft)] py-4 sm:block sm:border-b-0 sm:px-5 sm:first:pl-0">
                        <dt className="text-[10px] font-bold uppercase tracking-[.16em] text-[var(--ink-muted)]">Strongest signal</dt>
                        <dd className="sm:mt-2">
                            <span className="font-serif text-xl font-semibold text-[var(--ink-primary)]">{strongestLabel}</span>
                            <span className="ml-2 font-mono text-xs text-[var(--ink-muted)]">{gameState[strongest]}/100</span>
                        </dd>
                    </div>
                    <div className="flex items-baseline justify-between gap-5 border-b border-[var(--outline-soft)] py-4 sm:block sm:border-b-0 sm:px-5">
                        <dt className="text-[10px] font-bold uppercase tracking-[.16em] text-[var(--ink-muted)]">Build next</dt>
                        <dd className="sm:mt-2">
                            <span className="font-serif text-xl font-semibold text-[var(--ink-primary)]">{weakestLabel}</span>
                            <span className="ml-2 font-mono text-xs text-[var(--ink-muted)]">{gameState[weakest]}/100</span>
                        </dd>
                    </div>
                    <div className="flex items-baseline justify-between gap-5 border-b border-[var(--outline-soft)] py-4 sm:block sm:border-b-0 sm:px-5">
                        <dt className="text-[10px] font-bold uppercase tracking-[.16em] text-[var(--ink-muted)]">Energy reserve</dt>
                        <dd className="font-serif text-xl font-semibold text-[var(--ink-primary)] sm:mt-2">{gameState.energy}<span className="ml-1 font-mono text-xs font-normal text-[var(--ink-muted)]">/100</span></dd>
                    </div>
                    <div className="flex items-baseline justify-between gap-5 py-4 sm:block sm:px-5">
                        <dt className="text-[10px] font-bold uppercase tracking-[.16em] text-[var(--ink-muted)]">Choices made</dt>
                        <dd className="font-serif text-xl font-semibold text-[var(--ink-primary)] sm:mt-2">{finalDecisionCount || '—'}</dd>
                    </div>
                </dl>
            </header>

            <div className="mt-6 grid gap-6 lg:grid-cols-12">
                <section aria-labelledby="journey-profile-title" className="overflow-hidden rounded-[18px] border border-[var(--outline-soft)] bg-[var(--surface-paper)] lg:col-span-7">
                    <div className="border-b border-[var(--outline-soft)] px-5 py-5 sm:px-6">
                        <p className="text-[10px] font-bold uppercase tracking-[.18em] text-[var(--ink-muted)]">Four capability readout</p>
                        <div className="mt-2 flex flex-wrap items-end justify-between gap-3">
                            <h2 id="journey-profile-title" className="font-serif text-[26px] font-semibold leading-tight text-[var(--ink-primary)]">Your decision profile</h2>
                            <p className="text-xs text-[var(--ink-muted)]">Final score · change from start</p>
                        </div>
                    </div>

                    <div role="img" aria-label="Academic journey decision profile" className="px-5 py-4 sm:px-6 sm:py-5">
                        {RESULT_STAT_ORDER.map((stat, index) => {
                            const value = gameState[stat];
                            const delta = value - INITIAL_GAME_STATE[stat];
                            const isStrongest = strongestCapabilities.includes(stat);
                            const isWeakest = weakestCapabilities.includes(stat);
                            return (
                                <div key={stat} className={`py-4 ${index ? 'border-t border-[var(--outline-soft)]' : ''}`}>
                                    <div className="flex items-center justify-between gap-4">
                                        <div className="flex min-w-0 items-baseline gap-2">
                                            <span className="truncate text-sm font-semibold text-[var(--ink-primary)]">{STAT_LABELS[stat]}</span>
                                            {isStrongest && <span className="hidden text-[9px] font-bold uppercase tracking-[.12em] text-[#C55212] sm:inline">Strongest</span>}
                                            {isWeakest && !isStrongest && <span className="hidden text-[9px] font-bold uppercase tracking-[.12em] text-[var(--ink-muted)] sm:inline">Build next</span>}
                                        </div>
                                        <div className="shrink-0 font-mono text-xs">
                                            <span className="font-bold text-[var(--ink-primary)]">{value}</span>
                                            <span className="ml-2 text-[var(--ink-muted)]">{formatSignedValue(delta)}</span>
                                        </div>
                                    </div>
                                    <div className="mt-2.5 h-2 overflow-hidden rounded-full bg-[var(--surface-soft)]">
                                        <MotionDiv
                                            initial={{ width: 0 }}
                                            animate={{ width: `${Math.max(2, Math.min(100, value))}%` }}
                                            transition={{ duration: 0.7, delay: 0.06 * index, ease: editorialEase }}
                                            className="h-full rounded-full"
                                            style={{ background: isStrongest ? '#F26B1F' : isWeakest ? 'var(--ink-primary)' : 'var(--ink-muted)' }}
                                        />
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                    <div className="border-t border-[var(--outline-soft)] bg-[var(--surface-soft)] px-5 py-3 sm:px-6">
                        <p className="text-[11px] leading-relaxed text-[var(--ink-muted)]">Capability scores compare the evidence available on your route, so longer paths do not automatically score higher. They are reflective signals, not grades or predictions.</p>
                    </div>
                </section>

                <section aria-labelledby="journey-next-title" className="flex flex-col rounded-[18px] border-[1.5px] border-[var(--outline-strong)] bg-[var(--surface-paper)] lg:col-span-5">
                    <div className="px-5 py-5 sm:px-6 sm:py-6">
                        <p className="text-[10px] font-bold uppercase tracking-[.18em] text-[#C55212]">Recommended next</p>
                        <h2 id="journey-next-title" className="mt-2 font-serif text-[30px] font-semibold leading-tight text-[var(--ink-primary)]">Build {weakestLabel}</h2>
                        <p className="mt-3 text-sm leading-6 text-[var(--ink-secondary)]">{RESULT_NEXT_ACTION[weakest]}</p>
                        <div className="mt-5 border-t border-[var(--outline-soft)] pt-4">
                            <div className="flex items-center justify-between gap-4">
                                <p className="text-[10px] font-bold uppercase tracking-[.16em] text-[var(--ink-muted)]">Energy reserve</p>
                                <p className="font-mono text-xs font-bold text-[var(--ink-primary)]">{gameState.energy}/100</p>
                            </div>
                            <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-[var(--surface-soft)]">
                                <div className="h-full rounded-full bg-[#F26B1F]" style={{ width: `${Math.max(2, Math.min(100, gameState.energy))}%` }} />
                            </div>
                            <p className="mt-2 text-[11px] leading-relaxed text-[var(--ink-muted)]">Energy is a changing resource, shown separately from your capabilities. Protect sleep and recovery before adding more study hours.</p>
                        </div>
                    </div>

                    <div className="mt-auto border-t border-[var(--outline-soft)] px-5 py-5 sm:px-6">
                        <p className="text-[10px] font-bold uppercase tracking-[.16em] text-[var(--ink-muted)]">Start with</p>
                        {primaryModule && (
                            <button
                                type="button"
                                onClick={() => onSelectModule?.(primaryModule.moduleId)}
                                disabled={!onSelectModule}
                                className="group mt-3 flex min-h-12 w-full items-center justify-between gap-4 rounded-xl bg-[#F26B1F] px-4 py-3 text-left text-sm font-bold text-white transition-transform hover:-translate-y-0.5 disabled:cursor-default disabled:hover:translate-y-0"
                            >
                                <span>Start with {primaryModule.moduleTitle}</span>
                                <ArrowRight size={17} className="shrink-0 transition-transform group-hover:translate-x-1" aria-hidden="true" />
                            </button>
                        )}
                        {recommendedModules.slice(1).map(module => (
                            <button
                                key={module.moduleId}
                                type="button"
                                onClick={() => onSelectModule?.(module.moduleId)}
                                disabled={!onSelectModule}
                                className="group mt-2 flex min-h-11 w-full items-center justify-between gap-4 rounded-xl border border-[var(--outline-soft)] px-4 py-3 text-left text-xs font-semibold text-[var(--ink-secondary)] transition-colors hover:border-[var(--outline-strong)] hover:text-[var(--ink-primary)] disabled:cursor-default"
                            >
                                <span>{module.moduleTitle}</span>
                                <ArrowRight size={15} className="shrink-0 transition-transform group-hover:translate-x-1" aria-hidden="true" />
                            </button>
                        ))}
                    </div>
                </section>
            </div>

            {turningPoints.length > 0 && (
                <section aria-labelledby="journey-decisions-title" className="mt-6 overflow-hidden rounded-[18px] border border-[var(--outline-soft)] bg-[var(--surface-paper)]">
                    <div className="border-b border-[var(--outline-soft)] px-5 py-5 sm:px-6">
                        <p className="text-[10px] font-bold uppercase tracking-[.18em] text-[var(--ink-muted)]">What moved the result</p>
                        <h2 id="journey-decisions-title" className="mt-2 font-serif text-[26px] font-semibold leading-tight text-[var(--ink-primary)]">Decisions that shaped the result</h2>
                    </div>
                    <div className="hidden grid-cols-[minmax(150px,.8fr)_minmax(240px,1.5fr)_minmax(170px,1fr)] gap-6 border-b border-[var(--outline-soft)] bg-[var(--surface-soft)] px-6 py-3 text-[9px] font-bold uppercase tracking-[.16em] text-[var(--ink-muted)] sm:grid" aria-hidden="true">
                        <span>Moment</span><span>Your decision</span><span>Profile shift</span>
                    </div>
                    <ol className="divide-y divide-[var(--outline-soft)] px-5 sm:px-6">
                        {turningPoints.map((item, index) => (
                            <li key={`${item.scene.id}-${index}`} className="grid gap-3 py-5 sm:grid-cols-[minmax(150px,.8fr)_minmax(240px,1.5fr)_minmax(170px,1fr)] sm:gap-6">
                                <div>
                                    <p className="text-[9px] font-bold uppercase tracking-[.14em] text-[var(--ink-muted)]">{item.scene.month}</p>
                                    <p className="mt-1 font-serif text-[16px] font-semibold leading-snug text-[var(--ink-primary)]">{item.scene.title}</p>
                                </div>
                                <p className="text-sm leading-6 text-[var(--ink-secondary)]">{item.choiceText}</p>
                                <p className="font-mono text-[11px] leading-5 text-[var(--ink-secondary)]">{formatEffects(item.effects)}</p>
                            </li>
                        ))}
                    </ol>
                </section>
            )}

            <footer className="mt-6 flex flex-col gap-5 border-y border-[var(--outline-soft)] py-5 sm:flex-row sm:items-center sm:justify-between">
                <div className="max-w-[650px]">
                    <p className="font-serif text-lg font-semibold text-[var(--ink-primary)]">A reflection, not a forecast.</p>
                    <p className="mt-1 text-xs leading-relaxed text-[var(--ink-muted)]">This result reflects the choices made in one simulation. A different route can produce a different profile.</p>
                </div>
                <button
                    type="button"
                    onClick={onRestart}
                    className="inline-flex min-h-11 shrink-0 items-center justify-center gap-2 rounded-xl border-[1.5px] border-[var(--outline-strong)] bg-[var(--surface-paper)] px-4 text-xs font-bold text-[var(--ink-primary)] transition-transform hover:-translate-y-0.5"
                >
                    <RotateCcw size={15} aria-hidden="true" />
                    Explore another route
                </button>
            </footer>
        </MotionDiv>
    );
};

const ReportCard = JourneyOutcomeReport;

// ════════════════════════════════════════════════════════════════════════════
// MAIN COMPONENT
// ════════════════════════════════════════════════════════════════════════════

const AcademicJourneyGame: React.FC<{ onSelectModule?: (moduleId: string) => void; user?: { uid: string } | null; savedJourneyResult?: JourneyResult | null; onJourneyComplete?: (result: JourneyResult) => void }> = ({ onSelectModule, user, savedJourneyResult, onJourneyComplete }) => {
    const currentSavedResult = savedJourneyResult?.scoringVersion === JOURNEY_SCORING_VERSION ? savedJourneyResult : null;
    const [gameState, setGameState] = useState<GameState>({ ...INITIAL_GAME_STATE });
    const [journeyEvidence, setJourneyEvidence] = useState<JourneyEvidence>(() => createJourneyEvidence());
    const [currentSceneId, setCurrentSceneId] = useState('START');
    const [history, setHistory] = useState<HistoryItem[]>([]);
    const [visitedScenes, setVisitedScenes] = useState<string[]>(['START']);
    const [currentPhase, setCurrentPhase] = useState<Phase>('Foundation');
    const [showPhaseTransition, setShowPhaseTransition] = useState(false);
    const [pendingSceneId, setPendingSceneId] = useState<string | null>(null);
    const [chosenText, setChosenText] = useState<string | null>(null);
    const [lastModuleLink, setLastModuleLink] = useState<Choice['moduleLink'] | null>(null);
    const [previousResult, setPreviousResult] = useState<JourneyResult | null>(currentSavedResult);
    const [showingSavedResult, setShowingSavedResult] = useState(!!currentSavedResult);
    const hasSavedRef = useRef(false);
    const overlayTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

    const currentScene = STORY_DATA[currentSceneId];
    const isEndScene = currentSceneId.startsWith('END_');

    useEffect(() => {
        if (!user?.uid || user.uid === DEMO_STUDENT_UID) return;
        let cancelled = false;
        const loadPrevious = async () => {
            try {
                const progressDoc = await getDoc(doc(db, 'progress', user.uid));
                if (cancelled) return;
                if (progressDoc.exists()) {
                    const data = progressDoc.data();
                    if (data['journey-simulator']?.endingId && data['journey-simulator']?.scoringVersion === JOURNEY_SCORING_VERSION) {
                        setPreviousResult(data['journey-simulator']);
                        setShowingSavedResult(true);
                    }
                }
            } catch (err) { if (!cancelled) console.error('Failed to load journey result:', err); }
        };
        loadPrevious();
        return () => { cancelled = true; };
    }, [user?.uid]);

    useEffect(() => {
        if (!isEndScene || hasSavedRef.current) return;
        hasSavedRef.current = true;
        const completedAt = new Date().toISOString();
        const result: JourneyResult = {
            endingId: currentSceneId,
            finalStats: gameState,
            completedAt,
            decisionsCount: history.length,
            scoringVersion: JOURNEY_SCORING_VERSION,
            history: history.map(item => ({
                sceneId: item.scene.id,
                choiceText: item.choiceText,
                effects: item.effects,
                ...(item.moduleLink ? { moduleLink: item.moduleLink } : {}),
            })),
        };
        setPreviousResult(result);
        onJourneyComplete?.(result);
        if (user?.uid && user.uid !== DEMO_STUDENT_UID) {
            const progressDocRef = doc(db, 'progress', user.uid);
            saveInBackground(
                setDoc(progressDocRef, {
                    'journey-simulator': {
                        completedAt,
                        endingId: currentSceneId,
                        finalStats: gameState,
                        decisionsCount: history.length,
                        scoringVersion: JOURNEY_SCORING_VERSION,
                        history: history.map(item => ({
                            sceneId: item.scene.id,
                            choiceText: item.choiceText,
                            effects: item.effects,
                            ...(item.moduleLink ? { moduleLink: item.moduleLink } : {}),
                        })),
                    }
                }, { merge: true }),
                'AcademicJourneyGame.saveResult',
            );
        }
    }, [isEndScene, user?.uid, currentSceneId, gameState, history, onJourneyComplete]);

    const handleChoice = useCallback((choice: Choice) => {
        const currentChoiceScene = STORY_DATA[currentSceneId];
        const scoringUpdate = applyJourneyChoice(
            gameState,
            journeyEvidence,
            choice,
            currentChoiceScene.choices || [choice],
        );
        const newGameState = scoringUpdate.state;
        const newHistoryItem: HistoryItem = {
            scene: currentChoiceScene, choiceText: choice.text, effects: choice.effects, moduleLink: choice.moduleLink,
        };
        const newHistory = [...history, newHistoryItem];
        setHistory(newHistory);
        setGameState(newGameState);
        setJourneyEvidence(scoringUpdate.evidence);

        let targetSceneId = choice.nextSceneId;
        while (targetSceneId.startsWith('__') && ROUTE_RESOLVERS[targetSceneId]) {
            targetSceneId = ROUTE_RESOLVERS[targetSceneId](newGameState, newHistory);
        }
        setVisitedScenes(prev => [...prev, targetSceneId]);

        setChosenText(choice.text);
        setLastModuleLink(choice.moduleLink || null);
        setPendingSceneId(targetSceneId);

        if (overlayTimerRef.current) clearTimeout(overlayTimerRef.current);
        overlayTimerRef.current = setTimeout(() => {
            setChosenText(null);
            setLastModuleLink(null);

            const targetScene = STORY_DATA[targetSceneId];
            if (targetScene && targetScene.phase !== currentChoiceScene.phase) {
                setCurrentPhase(targetScene.phase);
                setShowPhaseTransition(true);
            } else {
                setCurrentSceneId(targetSceneId);
                setPendingSceneId(null);
            }
        }, 2500);
    }, [currentSceneId, gameState, history, journeyEvidence]);

    const handlePhaseTransitionComplete = useCallback(() => {
        setShowPhaseTransition(false);
        if (pendingSceneId) { setCurrentSceneId(pendingSceneId); setPendingSceneId(null); }
    }, [pendingSceneId]);

    const restartGame = useCallback(() => {
        setGameState({ ...INITIAL_GAME_STATE });
        setJourneyEvidence(createJourneyEvidence());
        setCurrentSceneId('START');
        setHistory([]);
        setVisitedScenes(['START']);
        setCurrentPhase('Foundation');
        setShowPhaseTransition(false);
        setPendingSceneId(null);
        setChosenText(null);
        setLastModuleLink(null);
        hasSavedRef.current = false;
        if (overlayTimerRef.current) clearTimeout(overlayTimerRef.current);
    }, []);

    // ── Saved result screen ─────────────────────────────────────────────────
    if (showingSavedResult && previousResult?.endingId && ARCHETYPES[previousResult.endingId]) {
        const savedStats = previousResult.finalStats || { ...INITIAL_GAME_STATE };
        const savedHistory: HistoryItem[] = (previousResult.history ?? [])
            .filter(item => Boolean(STORY_DATA[item.sceneId]))
            .map(item => ({
                scene: STORY_DATA[item.sceneId],
                choiceText: item.choiceText,
                effects: item.effects,
                moduleLink: item.moduleLink,
            }));
        return (
            <ReportCard
                endingId={previousResult.endingId}
                gameState={savedStats}
                history={savedHistory}
                decisionsCount={previousResult.decisionsCount}
                onRestart={() => { setShowingSavedResult(false); restartGame(); }}
                onSelectModule={onSelectModule}
            />
        );
    }

    if (isEndScene) {
        return <ReportCard endingId={currentSceneId} gameState={gameState} history={history} decisionsCount={history.length} onRestart={restartGame} onSelectModule={onSelectModule} />;
    }

    if (showPhaseTransition) {
        return (
            <AnimatePresence mode="wait">
                <PhaseTransition key={currentPhase} phase={currentPhase} onComplete={handlePhaseTransitionComplete} />
            </AnimatePresence>
        );
    }

    if (!currentScene || !currentScene.choices) return null;

    const locationConfig = LOCATION_CONFIG[currentScene.location];
    const phaseMeta = PHASE_METADATA.find(p => p.name === currentScene.phase);
    const t = PHASE_TOKENS[currentScene.phase];

    return (
        <>
            <AnimatePresence mode="wait">
                <MotionDiv
                    key={currentSceneId}
                    initial={{ opacity: 0, y: 6 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0 }}
                    transition={{ duration: 0.45, ease: editorialEase }}
                    // Break out of the parent <main>'s max-w-4xl so the editorial spread can use full viewport width.
                    style={{ position: 'relative', left: '50%', right: '50%', marginLeft: '-50vw', marginRight: '-50vw', width: '100vw' }}
                    className="pt-4 md:pt-6 pb-10"
                >
                  <div className="max-w-[1280px] mx-auto px-4 md:px-8">
                    {/*
                      Single unified canvas — one phase-tinted background covers both halves.
                      The illustration is layered into the lower-right of the same container,
                      so the scene reads as one composition rather than a split.
                    */}
                    <div
                        className="relative overflow-hidden"
                        style={{
                            background: t.wash,
                            // Slightly hand-touched border: lighter weight, warmer ink tone.
                            border: `1px solid ${INK}aa`,
                            borderRadius: 20,
                            boxShadow: '0 1px 0 rgba(31,27,23,0.04), 0 14px 36px rgba(31,27,23,0.07)',
                        }}
                    >
                        {/* Layered illustration — anchored bottom-right, sized so its ground line sits roughly at answers' baseline. */}
                        <div
                            className="hidden md:block absolute pointer-events-none select-none"
                            aria-hidden
                            style={{
                                right: 0,
                                bottom: 0,
                                width: '58%',
                                height: '78%',
                                maxWidth: 740,
                            }}
                        >
                            <SketchedHorizon phase={currentScene.phase} className="absolute inset-0 w-full h-full" />
                        </div>

                        {/* Content column — constrained so it doesn't overlap the illustration on wide screens. */}
                        <div className="relative px-6 md:px-10 pt-7 md:pt-9 pb-6 md:pb-8" style={{ maxWidth: 640 }}>
                            <Overline color={t.deep}>{currentScene.month} — {locationConfig.label}</Overline>

                            <h2 className="font-serif text-[28px] sm:text-[38px] font-bold leading-[1.04] mt-2" style={{ color: INK }}>
                                {currentScene.title}
                            </h2>
                            <p className="font-serif italic text-[13px] mt-1.5 max-w-md" style={{ color: t.deep }}>
                                {phaseMeta?.subtitle}
                            </p>

                            <div className="mt-4">
                                <TypingText
                                    text={(() => {
                                        if (currentScene.textVariants) {
                                            for (const v of currentScene.textVariants) {
                                                if ('stat' in v.condition) {
                                                    const val = gameState[v.condition.stat];
                                                    if (v.condition.min !== undefined && val < v.condition.min) continue;
                                                    if (v.condition.max !== undefined && val > v.condition.max) continue;
                                                    return v.text;
                                                }
                                                if ('visited' in v.condition && visitedScenes.includes(v.condition.visited)) return v.text;
                                            }
                                        }
                                        return currentScene.text;
                                    })()}
                                    sceneId={currentSceneId}
                                />
                            </div>

                            <div className="mt-4 flex items-center gap-3">
                                <Overline color={INK_MUTE}>What do you do?</Overline>
                                <SunburstRule width={42} color={t.ink} />
                            </div>

                            <div className="mt-2">
                                {currentScene.choices.map((choice, index) => (
                                    <ChoiceButton
                                        key={index}
                                        choice={choice}
                                        onChoose={handleChoice}
                                        disabled={!!chosenText}
                                        chosen={chosenText === choice.text}
                                        index={index}
                                        phase={currentScene.phase}
                                    />
                                ))}
                            </div>

                            {lastModuleLink && chosenText && (
                                <p className="font-serif italic text-[13px] mt-3" style={{ color: INK_SOFT }}>
                                    Related: <span className="font-semibold not-italic" style={{ color: t.deep }}>{lastModuleLink.moduleTitle}</span>
                                </p>
                            )}

                            {currentSceneId === 'START' && previousResult && ARCHETYPES[previousResult.endingId] && (
                                <div className="mt-5 px-4 py-3 inline-block" style={{
                                    background: '#ffffff', border: `1px dashed ${INK_MUTE}66`, borderRadius: 12,
                                }}>
                                    <p className="text-[12px]" style={{ color: INK_SOFT }}>
                                        Previous result: <span className="font-bold" style={{ color: t.deep }}>{ARCHETYPES[previousResult.endingId].title}</span>
                                    </p>
                                </div>
                            )}
                        </div>

                        {/* Trail — sits on the same canvas; only a hairline dashed rule above to ground it. */}
                        <div className="relative px-6 md:px-10 py-4" style={{ borderTop: `1px dashed ${INK}1f` }}>
                            <JourneyTrail currentPhase={currentScene.phase} />
                        </div>
                    </div>
                  </div>
                </MotionDiv>
            </AnimatePresence>
        </>
    );
};

export default AcademicJourneyGame;
