/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect, useCallback, useRef } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionButton, MotionDiv, MotionPolygon, MotionSpan } from './Motion';
import { ArrowRight, Lock } from 'lucide-react';
import { doc, setDoc, getDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { saveInBackground } from '../utils/firestoreWrite';
import {
    type GameState, type Choice, type HistoryItem, type StatKey, type Phase,
    type Location,
    STORY_DATA, ROUTE_RESOLVERS, INITIAL_GAME_STATE, PHASE_METADATA,
    ARCHETYPES, STAT_TO_MODULES, STAT_LABELS,
    WEAKEST_STAT_INSIGHTS,
    getStatGrade, getKeyTurningPoints, getWeakestStat,
} from './journeySimulatorData';
import { EvidenceDisclosure, OutcomeSection, OutcomeShell } from './ui/OutcomePatterns';
import { OutlinedSurface } from './ui/ProductPatterns';

export interface JourneyResult {
  endingId: string;
  finalStats?: GameState;
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

// Results artwork follows the same painted-blob + hand-drawn PNG language as
// the Launchpad. Turning points choose an icon from their largest stat effect,
// so every existing (and future) outcome has a deterministic visual.
const RESULT_STAT_ART: Record<StatKey, { icon: string; blob: string; path: string }> = {
    energy: {
        icon: '/icons/modules/09-hourglass.png', blob: '#F1D6A3',
        path: 'M 6 24 Q -2 52 8 78 Q 24 98 52 94 Q 86 90 94 62 Q 100 30 84 10 Q 60 -4 32 4 Q 12 12 6 24 Z',
    },
    academicCap: {
        icon: '/icons/modules/02-brain.png', blob: '#BCCCE3',
        path: 'M 4 28 Q 0 56 12 82 Q 28 100 56 96 Q 90 92 96 60 Q 100 28 82 8 Q 56 -6 30 6 Q 10 16 4 28 Z',
    },
    socialSupport: {
        icon: '/icons/modules/11-heart.png', blob: '#E8C7C1',
        path: 'M 8 22 Q 0 48 6 76 Q 20 96 50 96 Q 84 96 94 70 Q 100 40 84 14 Q 64 -2 36 4 Q 14 12 8 22 Z',
    },
    systemSavvy: {
        icon: '/icons/modules/13-checklist.png', blob: '#B5D4CC',
        path: 'M 6 22 Q -2 50 10 78 Q 26 98 56 94 Q 90 88 96 56 Q 100 24 80 6 Q 56 -6 28 6 Q 10 14 6 22 Z',
    },
    resilience: {
        icon: '/icons/modules/03-shield.png', blob: '#D8CBE5',
        path: 'M 4 26 Q 2 56 12 82 Q 26 98 52 96 Q 88 94 96 64 Q 100 34 84 10 Q 60 -4 30 6 Q 10 18 4 26 Z',
    },
};

function dominantEffectStat(effects: Partial<GameState>, fallback: StatKey = 'resilience'): StatKey {
    const entries = (Object.entries(effects) as [StatKey, number][]).filter(([, value]) => Number.isFinite(value));
    if (!entries.length) return fallback;
    return entries.reduce((best, entry) => Math.abs(entry[1]) > Math.abs(best[1]) ? entry : best)[0];
}

const ResultIconBlob: React.FC<{ stat: StatKey; size?: number; className?: string }> = ({ stat, size = 64, className }) => {
    const art = RESULT_STAT_ART[stat];
    return (
        <div className={`relative shrink-0 ${className ?? ''}`} style={{ width: size, height: size }} aria-hidden>
            <svg className="absolute inset-0 h-full w-full" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid meet">
                <path d={art.path} fill={art.blob} opacity="0.82" />
            </svg>
            <img src={art.icon} alt="" className="absolute left-1/2 top-1/2 object-contain" style={{ width: '102%', height: '102%', transform: 'translate(-50%, -50%)' }} />
        </div>
    );
};

const ArchetypeMountainBlob: React.FC = () => (
    <div className="relative hidden shrink-0 sm:block" style={{ width: 116, height: 106 }} aria-hidden>
        <svg className="absolute inset-0 h-full w-full" viewBox="0 0 100 100" preserveAspectRatio="none">
            <path d="M 6 24 Q -2 52 8 78 Q 24 98 52 94 Q 86 90 94 62 Q 100 30 84 10 Q 60 -4 32 4 Q 12 12 6 24 Z" fill="#EFD9CD" opacity="0.82" />
        </svg>
        <img src="/assets/level-up/header-mountain.png" alt="" className="absolute object-contain" style={{ width: '118%', height: '118%', left: '-9%', top: '-9%' }} />
    </div>
);

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
    const [visibleCount, setVisibleCount] = useState(0);
    const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

    useEffect(() => {
        setVisibleCount(0);
        intervalRef.current = setInterval(() => {
            setVisibleCount(prev => {
                if (prev >= words.length) { if (intervalRef.current) clearInterval(intervalRef.current); return prev; }
                return prev + 1;
            });
        }, 35);
        return () => { if (intervalRef.current) clearInterval(intervalRef.current); };
    }, [sceneId, words.length]);

    return (
        <p className="font-serif text-[16px] sm:text-[17px] leading-[1.5] italic" style={{ color: INK }}>
            {words.map((word, i) => (
                <MotionSpan key={`${sceneId}-${i}`} initial={false} animate={{ opacity: i < visibleCount ? 1 : 0 }} transition={{ duration: 0.15 }} className="inline">
                    {word}{' '}
                </MotionSpan>
            ))}
        </p>
    );
};

// ════════════════════════════════════════════════════════════════════════════
// CHOICE BUTTON — paper card, sketched A/B/C pill, phase-tint hover
// ════════════════════════════════════════════════════════════════════════════

const ChoiceButton: React.FC<{
    choice: Choice; gameState: GameState; visitedScenes: string[];
    onChoose: (choice: Choice) => void; disabled?: boolean; chosen?: boolean;
    index?: number; phase: Phase;
}> = ({ choice, gameState, visitedScenes, onChoose, disabled, chosen, index = 0, phase }) => {
    const statRequirementsMet = !choice.requires || choice.requires.every(r => (r.min === undefined || gameState[r.stat] >= r.min) && (r.max === undefined || gameState[r.stat] <= r.max));
    const visitRequirementsMet = !choice.requiresVisited || choice.requiresVisited.every(id => visitedScenes.includes(id));
    const isLocked = !statRequirementsMet || !visitRequirementsMet;
    const letter = String.fromCharCode(65 + index);
    const t = PHASE_TOKENS[phase];

    if (isLocked) {
        return (
            <div className="px-4 py-3 mb-3" style={{ background: 'transparent', border: `1.5px dashed ${INK_MUTE}66`, borderRadius: 12 }}>
                <div className="flex items-start gap-3">
                    <span className="flex items-center justify-center shrink-0 mt-0.5" style={{
                        width: 26, height: 26, borderRadius: '50%',
                        border: `1.4px dashed ${INK_MUTE}aa`, color: INK_MUTE,
                    }}>
                        <Lock size={12} />
                    </span>
                    <div className="flex-1 min-w-0">
                        <p className="text-[14px] italic" style={{ color: INK_MUTE }}>{choice.text}</p>
                        {choice.requires && (
                            <p className="text-[10px] mt-1 uppercase tracking-[0.15em] font-semibold" style={{ color: INK_MUTE }}>
                                Requires: {choice.requires.map(r => `${STAT_LABELS[r.stat]} ${r.max !== undefined ? `≤${r.max}` : `${r.min}+`}`).join(', ')}
                            </p>
                        )}
                    </div>
                </div>
            </div>
        );
    }

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
                <div className="flex-1 min-w-0">
                    <p className="text-[15px] leading-snug" style={{ color: INK }}>{choice.text}</p>
                    {choice.flavor && <p className="text-[12px] mt-1 italic" style={{ color: INK_MUTE }}>{choice.flavor}</p>}
                </div>
            </div>
        </MotionButton>
    );
};

// ════════════════════════════════════════════════════════════════════════════
// PENTAGON RADAR — sketchy hand-drawn version
// ════════════════════════════════════════════════════════════════════════════

const pentagonPoints = (cx: number, cy: number, r: number): string =>
    Array.from({ length: 5 }, (_, i) => {
        const angle = (Math.PI * 2 * i) / 5 - Math.PI / 2;
        return `${cx + r * Math.cos(angle)},${cy + r * Math.sin(angle)}`;
    }).join(' ');

const statPentagonPoints = (stats: GameState, cx: number, cy: number, maxR: number): string => {
    const keys = Object.keys(stats) as StatKey[];
    return keys.map((stat, i) => {
        const angle = (Math.PI * 2 * i) / 5 - Math.PI / 2;
        const r = (stats[stat] / 100) * maxR;
        return `${cx + r * Math.cos(angle)},${cy + r * Math.sin(angle)}`;
    }).join(' ');
};

const SketchedRadar: React.FC<{ stats: GameState }> = ({ stats }) => {
    const cx = 200, cy = 200, maxR = 130;
    const sage = PHASE_TOKENS.Foundation.deep;
    return (
        <svg viewBox="0 0 400 400" className="w-full max-w-md h-auto">
            {/* Concentric pentagons — sketched, slightly varied stroke */}
            {[0.25, 0.5, 0.75, 1].map((scale, idx) => (
                <polygon
                    key={scale}
                    points={pentagonPoints(cx, cy, maxR * scale)}
                    fill="none"
                    stroke={INK}
                    strokeWidth={idx === 3 ? 1.2 : 0.7}
                    strokeOpacity={idx === 3 ? 0.55 : 0.28}
                    strokeLinejoin="round"
                />
            ))}
            {/* Spokes */}
            {Array.from({ length: 5 }).map((_, i) => {
                const a = (Math.PI * 2 * i) / 5 - Math.PI / 2;
                return <line key={i} x1={cx} y1={cy} x2={cx + maxR * Math.cos(a)} y2={cy + maxR * Math.sin(a)} stroke={INK} strokeWidth={0.6} strokeOpacity={0.22} />;
            })}
            {/* Stat polygon */}
            <MotionPolygon
                initial={{ opacity: 0 }}
                animate={{ opacity: 1, points: statPentagonPoints(stats, cx, cy, maxR) }}
                transition={{ duration: 1, ease: 'easeOut' }}
                fill={`${sage}33`}
                stroke={sage}
                strokeWidth={2}
                strokeLinejoin="round"
            />
            {/* Vertex dots in accent */}
            {(Object.keys(stats) as StatKey[]).map((stat, i) => {
                const angle = (Math.PI * 2 * i) / 5 - Math.PI / 2;
                const px = cx + (stats[stat] / 100) * maxR * Math.cos(angle);
                const py = cy + (stats[stat] / 100) * maxR * Math.sin(angle);
                return <circle key={stat} cx={px} cy={py} r={3} fill={ACCENT} stroke={INK} strokeWidth={0.8} />;
            })}
            {/* Labels */}
            {(Object.keys(stats) as StatKey[]).map((stat, i) => {
                const angle = (Math.PI * 2 * i) / 5 - Math.PI / 2;
                const lx = cx + (maxR + 28) * Math.cos(angle);
                const ly = cy + (maxR + 28) * Math.sin(angle);
                return (
                    <g key={stat}>
                        <text x={lx} y={ly - 6} textAnchor="middle" dominantBaseline="middle"
                              fill={INK} className="font-serif" style={{ fontSize: 18, fontWeight: 700 }}>
                            {getStatGrade(stats[stat]).letter}
                        </text>
                        <text x={lx} y={ly + 12} textAnchor="middle" dominantBaseline="middle"
                              fill={INK_MUTE} style={{ fontSize: 10, letterSpacing: 0.5 }}>
                            {STAT_LABELS[stat]}
                        </text>
                    </g>
                );
            })}
        </svg>
    );
};

// ════════════════════════════════════════════════════════════════════════════
// REPORT CARD — editorial reveal
// ════════════════════════════════════════════════════════════════════════════

// ── Product-native outcome ──────────────────────────────────────────────

export const JourneyOutcomeReport: React.FC<{
    endingId: string;
    gameState: GameState;
    history: HistoryItem[];
    onRestart: () => void;
    onSelectModule?: (moduleId: string) => void;
}> = ({ endingId, gameState, history, onRestart, onSelectModule }) => {
    const archetype = ARCHETYPES[endingId];
    const endScene = STORY_DATA[endingId];
    const strongest = strongestStat(gameState);
    const weakest = getWeakestStat(gameState);
    const turningPoints = getKeyTurningPoints(history);
    const recommendedModules = STAT_TO_MODULES[weakest];
    const defining = history.find(item => item.scene.mood === 'crisis') || history[Math.floor(history.length / 2)];

    const pathsNotTaken: { sceneTitle: string; choiceText: string; requirement: string }[] = [];
    for (const item of history) {
        for (const alternative of item.scene.choices || []) {
            if (alternative.text === item.choiceText || !alternative.requires) continue;
            const meetsRequirements = alternative.requires.every(requirement =>
                (requirement.min === undefined || gameState[requirement.stat] >= requirement.min)
                && (requirement.max === undefined || gameState[requirement.stat] <= requirement.max));
            if (!meetsRequirements) {
                pathsNotTaken.push({
                    sceneTitle: item.scene.title,
                    choiceText: alternative.text,
                    requirement: alternative.requires
                        .map(requirement => `${STAT_LABELS[requirement.stat]} ${requirement.max !== undefined ? `≤${requirement.max}` : `${requirement.min}+`}`)
                        .join(', '),
                });
            }
        }
    }

    const primaryModule = recommendedModules[0];
    const outcomeTitle = archetype?.title || endScene?.title || 'Results Day';
    const summary = archetype?.description || endScene?.text;
    const pathGroups = (['Foundation', 'Pressure Cooker', 'Final Stretch'] as Phase[])
        .map(phase => ({ phase, items: history.filter(item => item.scene.phase === phase) }))
        .filter(group => group.items.length > 0);

    return (
        <MotionDiv initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.32 }}>
            <OutcomeShell
                eyebrow="Your journey outcome"
                title={outcomeTitle}
                summary={summary}
                illustration={<ArchetypeMountainBlob />}
                metrics={[
                    { label: `Strongest · ${STAT_LABELS[strongest]}`, value: getStatGrade(gameState[strongest]).letter, tone: 'success' },
                    { label: `Growth · ${STAT_LABELS[weakest]}`, value: getStatGrade(gameState[weakest]).letter },
                    { label: 'Decisions made', value: history.length || 'Saved' },
                    { label: 'Turning points', value: turningPoints.length || '—', tone: turningPoints.length ? 'accent' : 'default' },
                ]}
                primaryAction={primaryModule && onSelectModule ? {
                    label: `Open ${primaryModule.moduleTitle}`,
                    onClick: () => onSelectModule(primaryModule.moduleId),
                } : undefined}
                secondaryAction={{ label: 'Try another path', onClick: onRestart }}
            >
                <OutcomeSection eyebrow="The central insight" title="What this journey says about you">
                    <OutlinedSurface strong className="grid gap-5 p-5 sm:p-6 md:grid-cols-[1fr_240px] md:items-start">
                        <div>
                            <h4 className="font-serif text-[22px] font-semibold leading-snug text-[var(--ink-primary)]">
                                Your {STAT_LABELS[strongest].toLowerCase()} is your strongest lever.
                            </h4>
                            <p className="mt-3 text-sm leading-relaxed text-[var(--ink-secondary)]">
                                It carried you through pressure and protected your options. The next gain comes from pairing it with more deliberate work on {STAT_LABELS[weakest].toLowerCase()}.
                            </p>
                            {defining && (
                                <div className="mt-5 border-t border-[var(--outline-soft)] pt-4">
                                    <p className="text-[10px] font-bold uppercase tracking-[.16em] text-[var(--ink-muted)]">Defining decision · {defining.scene.month}</p>
                                    <p className="mt-1.5 font-serif text-[16px] font-semibold text-[var(--ink-primary)]">{defining.scene.title}</p>
                                    <p className="mt-1 text-sm text-[var(--ink-secondary)]">{defining.choiceText}</p>
                                </div>
                            )}
                        </div>
                        <div className="border-t border-[var(--outline-soft)] pt-5 md:border-l md:border-t-0 md:pl-5 md:pt-0">
                            <p className="text-[10px] font-bold uppercase tracking-[.16em] text-[#A43F08]">Growth edge</p>
                            <p className="mt-2 font-serif text-[19px] font-semibold text-[var(--ink-primary)]">{STAT_LABELS[weakest]}</p>
                            <p className="mt-2 text-xs leading-relaxed text-[var(--ink-secondary)]">{WEAKEST_STAT_INSIGHTS[weakest]}</p>
                        </div>
                    </OutlinedSurface>
                </OutcomeSection>

                <OutcomeSection eyebrow="Recommended next" title="Turn the result into action">
                    <div className="grid gap-3 sm:grid-cols-2">
                        {recommendedModules.map((module, index) => (
                            <button
                                key={module.moduleId}
                                type="button"
                                onClick={() => onSelectModule?.(module.moduleId)}
                                disabled={!onSelectModule}
                                className="group flex min-h-[92px] items-center justify-between gap-5 rounded-2xl border border-[var(--outline-soft)] bg-[var(--surface-paper)] p-5 text-left transition-all hover:-translate-y-0.5 hover:border-[var(--outline-strong)] disabled:cursor-default disabled:hover:translate-y-0"
                            >
                                <span>
                                    <span className="block text-[10px] font-bold uppercase tracking-[.16em] text-[var(--ink-muted)]">{index === 0 ? 'Start here' : 'Then build'}</span>
                                    <span className="mt-1.5 block font-serif text-[17px] font-semibold text-[var(--ink-primary)]">{module.moduleTitle}</span>
                                </span>
                                <ArrowRight size={18} className="shrink-0 text-[#F26B1F] transition-transform group-hover:translate-x-1" aria-hidden="true" />
                            </button>
                        ))}
                    </div>
                </OutcomeSection>

                <OutcomeSection eyebrow="Supporting evidence" title="Understand the result">
                    <OutlinedSurface className="overflow-hidden px-5 sm:px-6">
                        <EvidenceDisclosure summary="Your five scores" description="The full profile behind your archetype." defaultOpen>
                            <div className="grid gap-6 md:grid-cols-[.9fr_1.1fr] md:items-center">
                                <div className="mx-auto w-full max-w-[290px]"><SketchedRadar stats={gameState} /></div>
                                <div className="space-y-1">
                                    {(Object.keys(gameState) as StatKey[]).map(stat => (
                                        <div key={stat} className="grid grid-cols-[1fr_auto] items-center gap-4 border-b border-[var(--outline-soft)] py-3 last:border-b-0">
                                            <span className="text-sm text-[var(--ink-secondary)]">{STAT_LABELS[stat]}</span>
                                            <span className="font-mono text-xs font-bold text-[var(--ink-primary)]">{getStatGrade(gameState[stat]).letter} · {gameState[stat]}</span>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </EvidenceDisclosure>

                        <EvidenceDisclosure
                            summary="How you got here"
                            description={history.length ? `${history.length} decisions across your final-year journey.` : 'Decision history is available after a new playthrough.'}
                        >
                            {pathGroups.length ? (
                                <div className="space-y-6">
                                    {pathGroups.map(group => (
                                        <div key={group.phase}>
                                            <p className="text-[10px] font-bold uppercase tracking-[.16em]" style={{ color: PHASE_TOKENS[group.phase].deep }}>{PHASE_DISPLAY[group.phase]}</p>
                                            <div className="mt-2 divide-y divide-[var(--outline-soft)]">
                                                {group.items.map((item, index) => (
                                                    <div key={`${item.scene.title}-${index}`} className="grid gap-1 py-3 sm:grid-cols-[170px_1fr] sm:gap-5">
                                                        <span className="font-serif text-sm font-semibold text-[var(--ink-primary)]">{item.scene.title}</span>
                                                        <span className="text-xs leading-relaxed text-[var(--ink-secondary)]">{item.choiceText}</span>
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            ) : <p className="text-sm text-[var(--ink-muted)]">Play the journey again to create a complete decision record.</p>}
                        </EvidenceDisclosure>

                        {turningPoints.length > 0 && (
                            <EvidenceDisclosure summary="Key turning points" description="The moments that changed your direction most.">
                                <div className="space-y-3">
                                    {turningPoints.map((item, index) => (
                                        <div key={`${item.scene.title}-${index}`} className="flex items-start gap-4 rounded-xl bg-[var(--surface-soft)] p-4">
                                            <ResultIconBlob stat={dominantEffectStat(item.effects)} size={46} />
                                            <div>
                                                <p className="text-[10px] font-bold uppercase tracking-[.14em] text-[var(--ink-muted)]">{item.scene.month}</p>
                                                <p className="mt-1 font-serif text-[16px] font-semibold text-[var(--ink-primary)]">{item.scene.title}</p>
                                                <p className="mt-1 text-xs leading-relaxed text-[var(--ink-secondary)]">{item.choiceText}</p>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </EvidenceDisclosure>
                        )}

                        {pathsNotTaken.length > 0 && (
                            <EvidenceDisclosure summary="Paths not taken" description="Alternatives your final profile left out of reach.">
                                <div className="space-y-3">
                                    {pathsNotTaken.slice(0, 3).map((path, index) => (
                                        <div key={`${path.sceneTitle}-${index}`} className="flex items-start gap-3 border-b border-[var(--outline-soft)] pb-3 last:border-0">
                                            <Lock size={15} className="mt-0.5 shrink-0 text-[var(--ink-muted)]" aria-hidden="true" />
                                            <div>
                                                <p className="text-xs font-semibold text-[var(--ink-primary)]">{path.sceneTitle}</p>
                                                <p className="mt-1 font-serif text-sm italic text-[var(--ink-secondary)]">{path.choiceText}</p>
                                                <p className="mt-1 text-[10px] uppercase tracking-[.12em] text-[var(--ink-muted)]">Required: {path.requirement}</p>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </EvidenceDisclosure>
                        )}
                    </OutlinedSurface>
                </OutcomeSection>
            </OutcomeShell>
        </MotionDiv>
    );
};

const ReportCard = JourneyOutcomeReport;

// Helper: pick the strongest stat (mirrors getWeakestStat)
function strongestStat(state: GameState): StatKey {
    const keys: StatKey[] = ['energy', 'academicCap', 'socialSupport', 'systemSavvy', 'resilience'];
    return keys.reduce((best, k) => state[k] > state[best] ? k : best, keys[0]);
}

// ════════════════════════════════════════════════════════════════════════════
// MAIN COMPONENT
// ════════════════════════════════════════════════════════════════════════════

const AcademicJourneyGame: React.FC<{ onSelectModule?: (moduleId: string) => void; user?: { uid: string } | null; savedJourneyResult?: JourneyResult | null; onJourneyComplete?: (result: JourneyResult) => void }> = ({ onSelectModule, user, savedJourneyResult, onJourneyComplete }) => {
    const [gameState, setGameState] = useState<GameState>({ ...INITIAL_GAME_STATE });
    const [_prevState, setPrevState] = useState<GameState>({ ...INITIAL_GAME_STATE });
    const [currentSceneId, setCurrentSceneId] = useState('START');
    const [history, setHistory] = useState<HistoryItem[]>([]);
    const [visitedScenes, setVisitedScenes] = useState<string[]>(['START']);
    const [currentPhase, setCurrentPhase] = useState<Phase>('Foundation');
    const [showPhaseTransition, setShowPhaseTransition] = useState(false);
    const [pendingSceneId, setPendingSceneId] = useState<string | null>(null);
    const [chosenText, setChosenText] = useState<string | null>(null);
    const [lastModuleLink, setLastModuleLink] = useState<Choice['moduleLink'] | null>(null);
    const [previousResult, setPreviousResult] = useState<{ endingId: string; completedAt?: string; finalStats?: GameState } | null>(savedJourneyResult || null);
    const [showingSavedResult, setShowingSavedResult] = useState(!!savedJourneyResult);
    const hasSavedRef = useRef(false);
    const overlayTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

    const currentScene = STORY_DATA[currentSceneId];
    const isEndScene = currentSceneId.startsWith('END_');

    useEffect(() => {
        if (!user?.uid) return;
        let cancelled = false;
        const loadPrevious = async () => {
            try {
                const progressDoc = await getDoc(doc(db, 'progress', user.uid));
                if (cancelled) return;
                if (progressDoc.exists()) {
                    const data = progressDoc.data();
                    if (data['journey-simulator']?.endingId) {
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
        const result = { endingId: currentSceneId, finalStats: gameState };
        setPreviousResult(result);
        onJourneyComplete?.(result);
        if (user?.uid) {
            const progressDocRef = doc(db, 'progress', user.uid);
            saveInBackground(
                setDoc(progressDocRef, {
                    'journey-simulator': {
                        completedAt: new Date().toISOString(),
                        endingId: currentSceneId,
                        finalStats: gameState,
                        decisionsCount: history.length,
                    }
                }, { merge: true }),
                'AcademicJourneyGame.saveResult',
            );
        }
    }, [isEndScene, user?.uid, currentSceneId, gameState, history.length]);

    const handleChoice = useCallback((choice: Choice) => {
        const currentChoiceScene = STORY_DATA[currentSceneId];
        const newGameState = { ...gameState };
        for (const [key, value] of Object.entries(choice.effects)) {
            newGameState[key as StatKey] = Math.max(0, Math.min(100, newGameState[key as StatKey] + value));
        }
        const newHistoryItem: HistoryItem = {
            scene: currentChoiceScene, choiceText: choice.text, effects: choice.effects, moduleLink: choice.moduleLink,
        };
        const newHistory = [...history, newHistoryItem];
        setHistory(newHistory);
        setPrevState(gameState);
        setGameState(newGameState);

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
    }, [currentSceneId, gameState, history]);

    const handlePhaseTransitionComplete = useCallback(() => {
        setShowPhaseTransition(false);
        if (pendingSceneId) { setCurrentSceneId(pendingSceneId); setPendingSceneId(null); }
    }, [pendingSceneId]);

    const restartGame = useCallback(() => {
        setGameState({ ...INITIAL_GAME_STATE });
        setPrevState({ ...INITIAL_GAME_STATE });
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
        return (
            <ReportCard
                endingId={previousResult.endingId}
                gameState={savedStats}
                history={[]}
                onRestart={() => { setShowingSavedResult(false); restartGame(); }}
                onSelectModule={onSelectModule}
            />
        );
    }

    if (isEndScene) {
        return <ReportCard endingId={currentSceneId} gameState={gameState} history={history} onRestart={restartGame} onSelectModule={onSelectModule} />;
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
                                        gameState={gameState}
                                        visitedScenes={visitedScenes}
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
