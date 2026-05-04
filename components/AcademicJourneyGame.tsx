/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect, useCallback, useRef } from 'react';
import { useToast } from './Toast';
import { AnimatePresence } from 'framer-motion';
import { MotionButton, MotionDiv, MotionPolygon, MotionSpan } from './Motion';
import { Zap, Shield, TrendingUp, Users, BookOpen, Lock } from 'lucide-react';
import { doc, setDoc, getDoc } from 'firebase/firestore';
import { db } from '../firebase';
import {
    type GameState, type Choice, type HistoryItem, type StatKey, type Phase,
    type Location,
    STORY_DATA, ROUTE_RESOLVERS, INITIAL_GAME_STATE, PHASE_METADATA,
    ARCHETYPES, STAT_TO_MODULES, STAT_LABELS,
    WEAKEST_STAT_INSIGHTS,
    getStatGrade, getKeyTurningPoints, getWeakestStat,
} from './journeySimulatorData';

export interface JourneyResult {
  endingId: string;
  finalStats?: GameState;
}

// ════════════════════════════════════════════════════════════════════════════
// DESIGN TOKENS — editorial / hand-drawn world
// ════════════════════════════════════════════════════════════════════════════

const PAPER = '#F6F1E6';        // warm cream, slightly toastier than the global cream so the simulator feels like a separate journal
const PAPER_DEEP = '#EFE7D5';   // for nested paper cards within the simulator
const INK = '#1F1B17';          // near-black charcoal — never use #000
const INK_SOFT = '#5C544A';     // body copy
const INK_MUTE = '#8E8378';     // overlines, muted descriptors
const ACCENT = '#CC785C';       // brand orange — focal accent only
const ACCENT_DARK = '#B56A50';

// Softened phase palette — muted, paper-friendly, never neon
const PHASE_TOKENS: Record<Phase, { ink: string; wash: string; tint: string; deep: string }> = {
  'Foundation':      { ink: '#5E8B7E', wash: '#E8EDE6', tint: '#D8E4DA', deep: '#3F6A5E' },
  'Pressure Cooker': { ink: '#B8843D', wash: '#EFE0BF', tint: '#E6CE94', deep: '#8C6022' },
  'Final Stretch':   { ink: '#B86F5A', wash: '#EFD9CD', tint: '#E0B8A2', deep: '#8C4D3B' },
};

const STAT_ICONS: Record<StatKey, React.ElementType> = {
    energy: Zap,
    academicCap: TrendingUp,
    socialSupport: Users,
    systemSavvy: BookOpen,
    resilience: Shield,
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

// ════════════════════════════════════════════════════════════════════════════
// HAND-DRAWN SVG PRIMITIVES
// All strokes use slightly varied widths and "rough" pathing to feel sketched.
// Each motif keeps its own viewBox so callers control size via width/height.
// ════════════════════════════════════════════════════════════════════════════

const SketchedSun: React.FC<{ size?: number; color?: string; className?: string }> = ({ size = 48, color = INK, className }) => (
    <svg width={size} height={size} viewBox="0 0 64 64" fill="none" className={className} aria-hidden>
        {/* Half-sun on horizon — uneven rays, slightly off-circle */}
        <path d="M14 42 Q 32 22, 50 42" stroke={color} strokeWidth={1.4} strokeLinecap="round" fill="rgba(204,120,92,0.16)" />
        <path d="M11 42 L 53 42" stroke={color} strokeWidth={1.2} strokeLinecap="round" />
        {/* Rays — irregular lengths, not symmetric */}
        <path d="M32 18 L 32 8"  stroke={color} strokeWidth={1.2} strokeLinecap="round" />
        <path d="M22 22 L 17 14" stroke={color} strokeWidth={1.2} strokeLinecap="round" />
        <path d="M42 22 L 48 13" stroke={color} strokeWidth={1.2} strokeLinecap="round" />
        <path d="M14 32 L 6 30"  stroke={color} strokeWidth={1.2} strokeLinecap="round" />
        <path d="M50 32 L 58 31" stroke={color} strokeWidth={1.2} strokeLinecap="round" />
    </svg>
);

const SketchedMountain: React.FC<{ size?: number; color?: string; flag?: boolean; className?: string }> = ({ size = 64, color = INK, flag = true, className }) => (
    <svg width={size} height={size} viewBox="0 0 80 80" fill="none" className={className} aria-hidden>
        {/* Two overlapping peaks, slightly imperfect */}
        <path d="M6 64 L 30 22 L 48 50 L 56 38 L 74 64 Z" stroke={color} strokeWidth={1.3} strokeLinejoin="round" fill="none" />
        {/* Hatching for shading on the right face */}
        <path d="M30 28 L 33 38" stroke={color} strokeWidth={0.9} strokeLinecap="round" />
        <path d="M33 32 L 36 44" stroke={color} strokeWidth={0.8} strokeLinecap="round" />
        <path d="M36 38 L 39 50" stroke={color} strokeWidth={0.8} strokeLinecap="round" />
        <path d="M56 42 L 59 52" stroke={color} strokeWidth={0.8} strokeLinecap="round" />
        <path d="M59 46 L 62 56" stroke={color} strokeWidth={0.8} strokeLinecap="round" />
        {flag && (
            <>
                <path d="M30 22 L 30 10" stroke={color} strokeWidth={1.2} strokeLinecap="round" />
                <path d="M30 10 L 38 12 L 30 16 Z" fill={ACCENT} stroke={color} strokeWidth={1} />
            </>
        )}
    </svg>
);

const SketchedSapling: React.FC<{ size?: number; color?: string; className?: string }> = ({ size = 48, color = INK, className }) => (
    <svg width={size} height={size} viewBox="0 0 64 64" fill="none" className={className} aria-hidden>
        {/* Soil mound */}
        <path d="M14 50 Q 32 44, 50 50" stroke={color} strokeWidth={1.2} strokeLinecap="round" />
        <path d="M16 53 Q 32 49, 48 53" stroke={color} strokeWidth={0.9} strokeLinecap="round" />
        {/* Stem + two leaves */}
        <path d="M32 50 L 32 26" stroke={color} strokeWidth={1.3} strokeLinecap="round" />
        <path d="M32 34 Q 22 30, 18 36 Q 24 40, 32 36" stroke={color} strokeWidth={1.2} fill="rgba(94,139,126,0.18)" />
        <path d="M32 28 Q 42 22, 46 28 Q 40 34, 32 30" stroke={color} strokeWidth={1.2} fill="rgba(94,139,126,0.18)" />
        {/* Tiny scatter — pebbles */}
        <circle cx="11" cy="55" r="1.2" fill={color} />
        <circle cx="56" cy="55" r="1" fill={color} />
    </svg>
);

const SketchedDroplet: React.FC<{ size?: number; color?: string; className?: string }> = ({ size = 48, color = INK, className }) => (
    <svg width={size} height={size} viewBox="0 0 64 64" fill="none" className={className} aria-hidden>
        <path d="M32 14 Q 22 32, 26 42 Q 32 50, 38 42 Q 42 32, 32 14 Z" stroke={color} strokeWidth={1.3} fill="rgba(94,139,126,0.12)" />
        {/* Ripples — slightly uneven ellipses */}
        <ellipse cx="32" cy="52" rx="14" ry="2.5" stroke={color} strokeWidth={1} fill="none" />
        <ellipse cx="32" cy="52" rx="22" ry="3.5" stroke={color} strokeWidth={0.7} fill="none" opacity="0.7" />
    </svg>
);

const SketchedFlame: React.FC<{ size?: number; color?: string; className?: string }> = ({ size = 48, color = INK, className }) => (
    <svg width={size} height={size} viewBox="0 0 64 64" fill="none" className={className} aria-hidden>
        <path d="M32 12 Q 22 26, 26 36 Q 28 42, 24 46 Q 22 38, 18 40 Q 16 50, 24 54 Q 32 58, 40 54 Q 48 50, 46 40 Q 42 38, 40 46 Q 36 42, 38 36 Q 42 26, 32 12 Z"
              stroke={color} strokeWidth={1.3} fill="rgba(184,132,61,0.18)" strokeLinejoin="round" />
        {/* Inner flicker */}
        <path d="M30 30 Q 28 38, 32 44 Q 36 38, 32 30 Z" stroke={color} strokeWidth={0.9} fill="none" />
    </svg>
);

const SketchedLeaf: React.FC<{ size?: number; color?: string; className?: string }> = ({ size = 48, color = INK, className }) => (
    <svg width={size} height={size} viewBox="0 0 64 64" fill="none" className={className} aria-hidden>
        <path d="M16 48 Q 18 18, 48 16 Q 46 46, 16 48 Z" stroke={color} strokeWidth={1.3} fill="rgba(94,139,126,0.16)" strokeLinejoin="round" />
        <path d="M18 46 L 46 18" stroke={color} strokeWidth={0.9} strokeLinecap="round" />
        <path d="M26 38 L 30 32" stroke={color} strokeWidth={0.7} strokeLinecap="round" />
        <path d="M32 36 L 36 30" stroke={color} strokeWidth={0.7} strokeLinecap="round" />
    </svg>
);

const SketchedFlag: React.FC<{ size?: number; color?: string; className?: string }> = ({ size = 32, color = INK, className }) => (
    <svg width={size} height={size} viewBox="0 0 32 32" fill="none" className={className} aria-hidden>
        <path d="M8 28 L 8 4" stroke={color} strokeWidth={1.3} strokeLinecap="round" />
        <path d="M8 4 Q 18 6, 24 4 Q 22 10, 24 14 Q 16 12, 8 14 Z" fill={ACCENT} stroke={color} strokeWidth={1.1} strokeLinejoin="round" />
    </svg>
);

const SketchedStar: React.FC<{ size?: number; color?: string; className?: string }> = ({ size = 24, color = ACCENT, className }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" className={className} aria-hidden>
        <path d="M12 3 L 14.3 9.4 L 21 9.7 L 15.7 13.8 L 17.6 20.3 L 12 16.6 L 6.4 20.3 L 8.3 13.8 L 3 9.7 L 9.7 9.4 Z"
              stroke={color} strokeWidth={1.3} strokeLinejoin="round" strokeLinecap="round" />
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

// Hand-drawn loop — used on "Walk the path again"
const LoopArrow: React.FC<{ size?: number; color?: string }> = ({ size = 28, color = INK }) => (
    <svg width={size} height={size} viewBox="0 0 32 32" fill="none" aria-hidden>
        <path d="M26 14 Q 28 4, 16 4 Q 4 4, 4 16 Q 4 28, 16 28 Q 22 28, 26 24" stroke={color} strokeWidth={1.4} strokeLinecap="round" fill="none" />
        <path d="M22 22 L 26 24 L 24 28" stroke={color} strokeWidth={1.4} strokeLinecap="round" strokeLinejoin="round" fill="none" />
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
                                    <span
                                        className="mt-2 text-[10px] font-semibold uppercase tracking-[0.18em] whitespace-nowrap text-center"
                                        style={{ color: labelColor }}
                                    >
                                        {PHASE_DISPLAY[node.phase]}
                                    </span>
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

// Sticky-note callout used in the scenario hero illustration
const StickyNote: React.FC<{ children: React.ReactNode; rotate?: number; className?: string }> = ({ children, rotate = -3, className = '' }) => (
    <div
        className={`relative inline-block px-3 py-2 font-serif text-[12px] leading-snug ${className}`}
        style={{
            background: '#FBF6E5',
            color: INK,
            transform: `rotate(${rotate}deg)`,
            boxShadow: '0 2px 0 rgba(31,27,23,0.06), 0 6px 14px rgba(31,27,23,0.08)',
            border: `1px solid rgba(31,27,23,0.08)`,
            // Faintly torn edges via clip-path-ish: just rounded with slight skew
            borderRadius: '2px 6px 3px 7px',
        }}
    >
        {children}
    </div>
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
            style={{ background: PAPER }}
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
    const statRequirementsMet = !choice.requires || choice.requires.every(r => gameState[r.stat] >= r.min);
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
                                Requires: {choice.requires.map(r => `${STAT_LABELS[r.stat]} ${r.min}+`).join(', ')}
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

// Pick a sketched motif for a phase — used in turning-points trail
const phaseMotif = (phase: Phase, idx: number): React.ReactNode => {
    if (phase === 'Final Stretch') return <SketchedFlag size={36} />;
    if (phase === 'Pressure Cooker') return idx % 2 === 0 ? <SketchedFlame size={36} /> : <SketchedSun size={36} />;
    return idx % 2 === 0 ? <SketchedLeaf size={36} /> : <SketchedSapling size={36} />;
};

const InsightCard: React.FC<{ overline: string; title: string; body: string; motif: React.ReactNode; tilt?: number }> = ({ overline, title, body, motif, tilt = -0.6 }) => (
    <div className="relative p-5" style={{
        background: '#FFFFFF',
        borderRadius: 14,
        border: `1px solid ${INK}12`,
        boxShadow: '0 1px 0 rgba(31,27,23,0.03), 0 6px 18px rgba(31,27,23,0.06)',
        transform: `rotate(${tilt}deg)`,
    }}>
        {/* Hand-drawn header flourish: star + extending line */}
        <div className="flex items-center gap-1.5 mb-3">
            <img src="/assets/journey/insight-star.png" alt="" aria-hidden style={{ width: 22, height: 22, objectFit: 'contain' }} />
            <svg width="120" height="5" viewBox="0 0 120 5" fill="none" aria-hidden className="flex-shrink-0">
                <path d="M1 2.5 Q 40 0.8, 119 2.5" stroke={INK} strokeWidth={1} strokeLinecap="round" fill="none" />
            </svg>
        </div>
        <Overline className="text-[9px]">{overline}</Overline>
        <h5 className="font-serif text-[18px] sm:text-[19px] font-bold mt-2 leading-[1.2]" style={{ color: INK }}>{title}</h5>
        <p className="font-sans text-[13px] mt-2 leading-snug max-w-[30ch]" style={{ color: INK_SOFT }}>{body}</p>
        <div className="mt-3 flex justify-end" style={{ opacity: 0.7 }}>{motif}</div>
    </div>
);

const ReportCard: React.FC<{ endingId: string; gameState: GameState; history: HistoryItem[]; onRestart: () => void; onSelectModule?: (moduleId: string) => void }> = ({ endingId, gameState, history, onRestart, onSelectModule }) => {
    const archetype = ARCHETYPES[endingId];
    const endScene = STORY_DATA[endingId];
    const turningPoints = getKeyTurningPoints(history);
    const weakestStat = getWeakestStat(gameState);
    const recommendedModules = STAT_TO_MODULES[weakestStat];

    const pathNodes = history.map((item) => ({ title: item.scene.title, phase: item.scene.phase, month: item.scene.month, choiceText: item.choiceText }));

    const pathsNotTaken: { sceneTitle: string; choiceText: string; requirement: string }[] = [];
    for (const item of history) {
        const choices = item.scene.choices || [];
        for (const alt of choices) {
            if (alt.text !== item.choiceText && alt.requires) {
                const reqText = alt.requires.map(r => `${STAT_LABELS[r.stat]} ${r.min}+`).join(', ');
                const meetsReqs = alt.requires.every(r => gameState[r.stat] >= r.min);
                if (!meetsReqs) pathsNotTaken.push({ sceneTitle: item.scene.title, choiceText: alt.text, requirement: reqText });
            }
        }
    }

    // Identify a "defining" scene — first crisis or biggest stat-shift moment
    const defining = history.find(h => h.scene.mood === 'crisis') || history[Math.floor(history.length / 2)];

    const phases: Phase[] = ['Foundation', 'Pressure Cooker', 'Final Stretch'];
    const groupedPath = phases
        .map(phase => ({ phase, nodes: pathNodes.filter(n => n.phase === phase) }))
        .filter(g => g.nodes.length > 0);

    return (
        <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-10 pt-6 md:pt-8 pb-10">
            {/* ── HERO archetype block ── */}
            <section>
                <Overline>Your archetype</Overline>
                <div className="flex items-start gap-6 mt-3">
                    <h3 className="font-serif text-5xl sm:text-6xl font-bold leading-[1.02]" style={{ color: INK }}>
                        {archetype?.title || endScene?.title || 'Results Day'}
                    </h3>
                    {/* Hand-drawn circular emblem — archetype mountain logo */}
                    <img
                        src="/assets/journey/archetype-mountain.png"
                        alt=""
                        aria-hidden
                        className="hidden sm:block shrink-0"
                        style={{ width: 96, height: 96, objectFit: 'contain' }}
                    />
                </div>
                <p className="font-serif text-[17px] mt-5 leading-relaxed max-w-2xl" style={{ color: INK_SOFT }}>
                    {archetype?.description || endScene?.text}
                </p>

                {/* Supporting insight cards — sit beneath the archetype as a triptych */}
                <div className="mt-8 grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
                    <InsightCard
                        overline="Your insight"
                        title={`Your ${STAT_LABELS[strongestStat(gameState)].toLowerCase()} is your superpower.`}
                        body={`This carried you through the year — lean into it next.`}
                        motif={<SketchedSapling size={32} />}
                    />
                    {defining && (
                        <InsightCard
                            overline="Defined by"
                            title={defining.scene.title}
                            body={defining.choiceText}
                            motif={<SketchedDroplet size={30} />}
                            tilt={0.6}
                        />
                    )}
                    {turningPoints[0] && (
                        <InsightCard
                            overline="Turning point"
                            title={turningPoints[0].scene.title}
                            body={turningPoints[0].choiceText}
                            motif={<SketchedSun size={32} />}
                        />
                    )}
                </div>
            </section>

            {/* ── Sketched radar ── */}
            <section>
                <div className="flex items-center gap-3 mb-2">
                    <Overline>Your grades</Overline>
                    <SunburstRule width={70} color={ACCENT} />
                </div>
                <div className="flex justify-center mt-4">
                    <SketchedRadar stats={gameState} />
                </div>
            </section>

            {/* ── Vulnerability ── */}
            <section className="max-w-2xl">
                <div className="flex items-center gap-3 mb-3">
                    <Overline color={ACCENT}>Your biggest vulnerability</Overline>
                    <SunburstRule width={50} color={ACCENT} />
                </div>
                <h4 className="font-serif text-[28px] font-semibold mb-3" style={{ color: INK }}>{STAT_LABELS[weakestStat]}</h4>
                <p className="font-serif text-[16px] leading-relaxed" style={{ color: INK_SOFT }}>
                    {WEAKEST_STAT_INSIGHTS[weakestStat]}
                </p>
            </section>

            {/* ── Key turning points — vertical dashed trail ── */}
            {turningPoints.length > 0 && (
                <section>
                    <h4 className="font-serif text-[26px] font-semibold mb-6" style={{ color: INK }}>Key Turning Points</h4>
                    <div className="relative pl-20">
                        {/* Hand-drawn vertical dashed trail */}
                        <div aria-hidden className="absolute left-[28px] top-2 bottom-2"
                            style={{
                                width: 2,
                                backgroundImage: `radial-gradient(circle, ${INK}88 1.2px, transparent 1.4px)`,
                                backgroundSize: '2px 8px',
                                backgroundRepeat: 'repeat-y',
                            }}
                        />
                        <div className="space-y-7">
                            {turningPoints.map((item, index) => (
                                <div key={index} className="relative">
                                    {/* Motif sits over the trail */}
                                    <div className="absolute -left-20 top-0 flex items-center justify-center"
                                        style={{ width: 56, height: 56, background: PAPER, borderRadius: '50%' }}>
                                        {phaseMotif(item.scene.phase, index)}
                                    </div>
                                    <Overline>{item.scene.month}</Overline>
                                    <h5 className="font-serif text-[20px] font-semibold mt-1 leading-snug" style={{ color: INK }}>{item.scene.title}</h5>
                                    <p className="font-sans text-[14px] mt-1 leading-relaxed" style={{ color: INK_SOFT }}>{item.choiceText}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                </section>
            )}

            {/* ── Paths not taken — dashed alternate routes ── */}
            {pathsNotTaken.length > 0 && (
                <section>
                    <div className="flex items-center gap-3 mb-4">
                        <Overline>Paths not taken</Overline>
                        <SunburstRule width={60} color={INK_MUTE} />
                    </div>
                    <div className="space-y-3">
                        {pathsNotTaken.slice(0, 3).map((path, index) => (
                            <div key={index} className="px-4 py-3" style={{ background: 'transparent', border: `1.4px dashed ${INK_MUTE}66`, borderRadius: 12 }}>
                                <div className="flex items-start gap-3">
                                    <span className="flex items-center justify-center shrink-0 mt-0.5" style={{
                                        width: 26, height: 26, borderRadius: '50%', border: `1.3px dashed ${INK_MUTE}aa`, color: INK_MUTE,
                                    }}>
                                        <Lock size={12} />
                                    </span>
                                    <div className="flex-1">
                                        <Overline>{path.sceneTitle}</Overline>
                                        <p className="font-serif italic text-[15px] mt-1" style={{ color: INK_SOFT }}>{path.choiceText}</p>
                                        <p className="text-[10px] uppercase tracking-[0.15em] font-semibold mt-1" style={{ color: INK_MUTE }}>Required: {path.requirement}</p>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </section>
            )}

            {/* ── Recommended modules ── */}
            <section>
                <div className="flex items-center gap-3 mb-1">
                    <Overline>Recommended for you</Overline>
                    <SunburstRule width={50} color={ACCENT} />
                </div>
                <p className="text-[12px] mb-4" style={{ color: INK_MUTE }}>Based on your weakest area: {STAT_LABELS[weakestStat]}</p>
                <div className="grid sm:grid-cols-2 gap-3">
                    {recommendedModules.map(mod => (
                        <button
                            key={mod.moduleId}
                            onClick={() => onSelectModule?.(mod.moduleId)}
                            className="text-left p-4 transition-all group"
                            style={{
                                background: '#FFFFFF', border: `1px solid ${INK}18`, borderRadius: 14,
                                boxShadow: '0 1px 0 rgba(31,27,23,0.04), 0 6px 18px rgba(31,27,23,0.04)',
                            }}
                            onMouseEnter={(e: any) => { e.currentTarget.style.borderColor = ACCENT; e.currentTarget.style.boxShadow = `0 2px 0 ${ACCENT}22, 0 8px 22px rgba(31,27,23,0.08)`; }}
                            onMouseLeave={(e: any) => { e.currentTarget.style.borderColor = `${INK}18`; e.currentTarget.style.boxShadow = '0 1px 0 rgba(31,27,23,0.04), 0 6px 18px rgba(31,27,23,0.04)'; }}
                        >
                            <div className="flex items-start justify-between gap-3">
                                <p className="font-serif text-[17px] font-semibold leading-snug" style={{ color: INK }}>{mod.moduleTitle}</p>
                                <svg width="22" height="14" viewBox="0 0 22 14" fill="none" aria-hidden className="shrink-0 mt-1">
                                    <path d="M2 7 Q 10 4, 20 7" stroke={ACCENT} strokeWidth={1.3} strokeLinecap="round" fill="none" />
                                    <path d="M16 3 L 21 7 L 16 11" stroke={ACCENT} strokeWidth={1.3} strokeLinecap="round" strokeLinejoin="round" fill="none" />
                                </svg>
                            </div>
                        </button>
                    ))}
                </div>
            </section>

            {/* ── Your Path — meandering trail ── */}
            <section>
                <h4 className="font-serif text-[26px] font-semibold mb-6" style={{ color: INK }}>Your Path</h4>
                <div className="relative pl-12">
                    <div aria-hidden className="absolute left-[14px] top-2 bottom-6"
                        style={{
                            width: 2,
                            backgroundImage: `radial-gradient(circle, ${INK}66 1.1px, transparent 1.3px)`,
                            backgroundSize: '2px 7px', backgroundRepeat: 'repeat-y',
                        }}
                    />
                    {groupedPath.map(({ phase, nodes }) => (
                        <div key={phase} className="mb-7">
                            <div className="flex items-center gap-2 mb-3 -ml-12">
                                <div className="flex items-center justify-center" style={{
                                    width: 30, height: 30, borderRadius: '50%',
                                    background: PHASE_TOKENS[phase].wash, border: `1.4px solid ${PHASE_TOKENS[phase].ink}`,
                                }}>
                                    <div style={{ width: 8, height: 8, borderRadius: '50%', background: PHASE_TOKENS[phase].deep }} />
                                </div>
                                <Overline color={PHASE_TOKENS[phase].deep}>{PHASE_DISPLAY[phase]}</Overline>
                            </div>
                            {nodes.map((node, ni) => (
                                <div key={ni} className="relative mb-3 ml-2">
                                    <div className="absolute -left-[39px] top-2" style={{
                                        width: 10, height: 10, borderRadius: '50%',
                                        background: PAPER, border: `1.4px solid ${INK}`,
                                    }} />
                                    <Overline>{node.title}</Overline>
                                    <p className="font-serif text-[15px] mt-0.5 leading-relaxed" style={{ color: INK }}>{node.choiceText}</p>
                                </div>
                            ))}
                        </div>
                    ))}
                    {/* Endpoint flag */}
                    <div className="-ml-12 flex items-center gap-2">
                        <div className="flex items-center justify-center" style={{ width: 30, height: 30 }}>
                            <SketchedFlag size={26} />
                        </div>
                        <Overline color={ACCENT}>{archetype?.title || 'End'}</Overline>
                    </div>
                </div>
            </section>

            {/* ── Play again — closing gesture ── */}
            <section className="text-center py-10" style={{ borderTop: `1px dashed ${INK_MUTE}66` }}>
                <p className="font-serif italic text-[15px] mb-4" style={{ color: INK_MUTE }}>
                    The year is yours to write again.
                </p>
                <button
                    onClick={onRestart}
                    className="inline-flex items-center gap-3 px-6 py-3 transition-all group"
                    style={{
                        background: '#FFFFFF', border: `1.5px solid ${INK}`, borderRadius: 100,
                        boxShadow: `0 2px 0 ${INK}, 0 4px 12px rgba(31,27,23,0.08)`,
                    }}
                    onMouseEnter={(e: any) => { e.currentTarget.style.background = PHASE_TOKENS.Foundation.wash; e.currentTarget.style.transform = 'translateY(-1px)'; }}
                    onMouseLeave={(e: any) => { e.currentTarget.style.background = '#FFFFFF'; e.currentTarget.style.transform = 'translateY(0)'; }}
                >
                    <LoopArrow size={22} />
                    <span className="font-serif text-[15px] font-semibold" style={{ color: INK }}>Walk the path again</span>
                </button>
            </section>
        </MotionDiv>
    );
};

// Helper: pick the strongest stat (mirrors getWeakestStat)
function strongestStat(state: GameState): StatKey {
    const keys: StatKey[] = ['energy', 'academicCap', 'socialSupport', 'systemSavvy', 'resilience'];
    return keys.reduce((best, k) => state[k] > state[best] ? k : best, keys[0]);
}

// ════════════════════════════════════════════════════════════════════════════
// MAIN COMPONENT
// ════════════════════════════════════════════════════════════════════════════

const AcademicJourneyGame: React.FC<{ onSelectModule?: (moduleId: string) => void; user?: { uid: string } | null; savedJourneyResult?: JourneyResult | null; onJourneyComplete?: (result: JourneyResult) => void }> = ({ onSelectModule, user, savedJourneyResult, onJourneyComplete }) => {
    const { showToast } = useToast();
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
        let cancelled = false;
        const result = { endingId: currentSceneId, finalStats: gameState };
        setPreviousResult(result);
        onJourneyComplete?.(result);
        if (user?.uid) {
            const saveResult = async () => {
                try {
                    const progressDocRef = doc(db, 'progress', user.uid);
                    await setDoc(progressDocRef, {
                        'journey-simulator': {
                            completedAt: new Date().toISOString(),
                            endingId: currentSceneId,
                            finalStats: gameState,
                            decisionsCount: history.length,
                        }
                    }, { merge: true });
                } catch (err) {
                    if (cancelled) return;
                    console.error('Failed to save journey result:', err);
                    showToast('Couldn\'t save — check your connection', 'error');
                }
            };
            saveResult();
        }
        return () => { cancelled = true; };
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
