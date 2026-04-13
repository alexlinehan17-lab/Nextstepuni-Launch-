
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect, useCallback, useRef } from 'react';
import { useToast } from './Toast';
import { createPortal } from 'react-dom';
import { AnimatePresence } from 'framer-motion';
import { MotionButton, MotionDiv, MotionPolygon, MotionSpan } from './Motion';
import {
    ArrowRight, Zap, Shield, RotateCcw,
    TrendingUp, Users, BookOpen,
    Lock, Compass, Brain, HandHelping, Target, ArrowUpRight, Award, Megaphone,
    Flame, Scale,
} from 'lucide-react';
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

const STAT_ICONS: Record<StatKey, React.ElementType> = {
    energy: Zap,
    academicCap: TrendingUp,
    socialSupport: Users,
    systemSavvy: BookOpen,
    resilience: Shield,
};

// ─── Location Config (label only) ───────────────────────────────────────────

// Phase colour config — Headspace-style environmental colour
const PHASE_COLORS: Record<Phase, { bg: string; darkText: boolean }> = {
  'Foundation': { bg: '#2A7D6F', darkText: false },
  'Pressure Cooker': { bg: '#D4891C', darkText: false },
  'Final Stretch': { bg: '#D4564E', darkText: false },
};

const LOCATION_CONFIG: Record<Location, { label: string }> = {
    school: { label: 'School' },
    home: { label: 'Home' },
    'exam-hall': { label: 'Exam Hall' },
    library: { label: 'Library' },
    social: { label: 'Social' },
    work: { label: 'Work' },
    online: { label: 'Online' },
};

// ─── Archetype Icon Map ─────────────────────────────────────────────────────

const _ARCHETYPE_ICONS: Record<string, React.ElementType> = {
    'compass': Compass,
    'brain': Brain,
    'hand-helping': HandHelping,
    'target': Target,
    'arrow-up-right': ArrowUpRight,
    'rotate-ccw': RotateCcw,
    'award': Award,
    'megaphone': Megaphone,
    'flame': Flame,
    'scale': Scale,
};

// ─── Pentagon Radar Helpers ─────────────────────────────────────────────────

const pentagonPoints = (cx: number, cy: number, r: number): string => {
    return Array.from({ length: 5 }, (_, i) => {
        const angle = (Math.PI * 2 * i) / 5 - Math.PI / 2;
        return `${cx + r * Math.cos(angle)},${cy + r * Math.sin(angle)}`;
    }).join(' ');
};

const statPentagonPoints = (stats: GameState, cx: number, cy: number, maxR: number): string => {
    const keys: StatKey[] = ['energy', 'academicCap', 'socialSupport', 'systemSavvy', 'resilience'];
    return keys.map((stat, i) => {
        const angle = (Math.PI * 2 * i) / 5 - Math.PI / 2;
        const r = (stats[stat] / 100) * maxR;
        return `${cx + r * Math.cos(angle)},${cy + r * Math.sin(angle)}`;
    }).join(' ');
};

// ─── Scene transition easing ────────────────────────────────────────────────

const editorialEase = [0.22, 1, 0.36, 1];

// ─── EphemeralStatOverlay ────────────────────────────────────────────────────

const EphemeralStatOverlay: React.FC<{ effects: Partial<GameState>; gameState: GameState }> = ({ effects, gameState }) => (
    <MotionDiv
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        exit={{ opacity: 0, x: 20 }}
        className="fixed top-32 right-4 z-[90] flex items-center gap-5
                   bg-white/90 dark:bg-zinc-900/90 backdrop-blur-sm
                   border border-zinc-200 dark:border-white/10 rounded-full px-5 py-2.5 shadow-sm"
    >
        {(Object.keys(effects) as StatKey[]).map(stat => {
            const delta = effects[stat] as number;
            const Icon = STAT_ICONS[stat];
            return (
                <div key={stat} className="flex items-center gap-2">
                    <Icon size={14} className="text-zinc-400 dark:text-zinc-500" />
                    <span className="text-xs font-bold text-zinc-500 dark:text-zinc-400">{gameState[stat]}</span>
                    <span className={`font-mono text-xs font-black ${delta >= 0 ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400'}`}>
                        {delta >= 0 ? '+' : ''}{delta}
                    </span>
                </div>
            );
        })}
    </MotionDiv>
);

// ─── PhaseTransition (editorial) ────────────────────────────────────────────

const PhaseTransition: React.FC<{ phase: Phase; onComplete: () => void }> = ({ phase, onComplete }) => {
    useEffect(() => {
        const timer = setTimeout(onComplete, 5000);
        return () => clearTimeout(timer);
    }, [onComplete]);

    const meta = PHASE_METADATA.find(p => p.name === phase);
    const pc = (PHASE_COLORS[phase] || PHASE_COLORS['Foundation']).bg;

    return (
        <MotionDiv
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.6 }}
            onClick={onComplete}
            className="cursor-pointer fixed inset-0 z-[70] flex flex-col items-center justify-center overflow-hidden"
            style={{ backgroundColor: pc }}
        >
            {/* Decorative blobs */}
            <div className="absolute pointer-events-none" style={{ top: -80, right: -60, width: 300, height: 300, borderRadius: '50%', background: 'rgba(255,255,255,0.08)' }} />
            <div className="absolute pointer-events-none" style={{ bottom: -60, left: -80, width: 250, height: 250, borderRadius: '50%', background: 'rgba(0,0,0,0.06)' }} />
            <div className="absolute pointer-events-none" style={{ top: '40%', left: -30, width: 120, height: 120, borderRadius: '50%', background: 'rgba(255,255,255,0.05)' }} />
            <div className="absolute pointer-events-none" style={{ bottom: '30%', right: 20, width: 70, height: 70, borderRadius: '50%', background: 'rgba(255,255,255,0.06)' }} />

            <div className="relative z-10 text-center px-6">
                <MotionDiv
                    initial={{ opacity: 0, y: 15 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3, duration: 0.6 }}
                >
                    <p className="text-[11px] font-bold uppercase tracking-[0.25em] mb-4" style={{ color: 'rgba(255,255,255,0.5)' }}>
                        {meta?.months}
                    </p>
                    <h2 className="font-serif text-5xl sm:text-7xl font-bold text-white mb-4">
                        {phase}
                    </h2>
                    <p className="text-lg max-w-md mx-auto leading-relaxed" style={{ color: 'rgba(255,255,255,0.6)' }}>
                        {meta?.subtitle}
                    </p>
                </MotionDiv>

                <MotionDiv
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 1.2 }}
                    className="mt-14"
                >
                    <p className="text-[10px] font-semibold uppercase tracking-[0.2em]" style={{ color: 'rgba(255,255,255,0.35)' }}>Tap to continue</p>
                </MotionDiv>
            </div>
        </MotionDiv>
    );
};

// ─── Typing Text ────────────────────────────────────────────────────────────

const TypingText: React.FC<{ text: string; sceneId: string }> = ({ text, sceneId }) => {
    const words = text.split(' ');
    const [visibleCount, setVisibleCount] = useState(0);
    const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

    useEffect(() => {
        setVisibleCount(0);
        intervalRef.current = setInterval(() => {
            setVisibleCount(prev => {
                if (prev >= words.length) {
                    if (intervalRef.current) clearInterval(intervalRef.current);
                    return prev;
                }
                return prev + 1;
            });
        }, 40);
        return () => { if (intervalRef.current) clearInterval(intervalRef.current); };
    }, [sceneId, words.length]);

    return (
        <div className="relative max-w-2xl mb-8">
            <p className="font-serif text-xl text-zinc-700 dark:text-zinc-200 leading-relaxed italic">
                {words.map((word, i) => (
                    <MotionSpan
                        key={`${sceneId}-${i}`}
                        initial={false}
                        animate={{ opacity: i < visibleCount ? 1 : 0 }}
                        transition={{ duration: 0.15 }}
                        className="inline"
                    >
                        {word}{' '}
                    </MotionSpan>
                ))}
            </p>
        </div>
    );
};

// ─── Choice Button (editorial) ──────────────────────────────────────────────

const ChoiceButton: React.FC<{ choice: Choice; gameState: GameState; visitedScenes: string[]; onChoose: (choice: Choice) => void; disabled?: boolean; chosen?: boolean; index?: number; phaseColor?: string }> = ({ choice, gameState, visitedScenes, onChoose, disabled, chosen, index = 0, phaseColor = '#2A7D6F' }) => {
    const statRequirementsMet = !choice.requires || choice.requires.every(r => gameState[r.stat] >= r.min);
    const visitRequirementsMet = !choice.requiresVisited || choice.requiresVisited.every(id => visitedScenes.includes(id));
    const isLocked = !statRequirementsMet || !visitRequirementsMet;
    const letter = String.fromCharCode(65 + index); // A, B, C

    if (isLocked) {
        return (
            <div className="rounded-xl px-4 py-3 mb-2 opacity-40" style={{ backgroundColor: 'rgba(0,0,0,0.03)', borderRadius: 12 }}>
                <div className="flex items-center gap-3">
                    <Lock size={14} className="text-zinc-400 flex-shrink-0" />
                    <p className="text-[15px] text-zinc-400">{choice.text}</p>
                </div>
                {choice.requires && (
                    <p className="text-[10px] text-zinc-400 mt-1 ml-7 uppercase tracking-wider">
                        Requires: {choice.requires.map(r => `${STAT_LABELS[r.stat]} ${r.min}+`).join(', ')}
                    </p>
                )}
            </div>
        );
    }

    if (disabled && !chosen) {
        return (
            <div className="rounded-xl px-4 py-3 mb-2 opacity-25 bg-[#FEFDFB] dark:bg-zinc-900 border border-[#EDEBE8] dark:border-zinc-800" style={{ borderRadius: 12 }}>
                <div className="flex items-center gap-3">
                    <span className="text-[11px] font-bold w-5 h-5 rounded-md flex items-center justify-center shrink-0" style={{ backgroundColor: 'rgba(0,0,0,0.04)', color: '#C4C0BC' }}>{letter}</span>
                    <p className="text-[15px] text-zinc-400">{choice.text}</p>
                </div>
            </div>
        );
    }

    if (chosen) {
        return (
            <div className="rounded-xl px-4 py-3 mb-2" style={{ backgroundColor: phaseColor, borderRadius: 12 }}>
                <div className="flex items-center gap-3">
                    <span className="text-[11px] font-bold w-5 h-5 rounded-md flex items-center justify-center shrink-0" style={{ backgroundColor: 'rgba(255,255,255,0.2)', color: '#fff' }}>{letter}</span>
                    <p className="text-[15px] font-semibold text-white">{choice.text}</p>
                </div>
            </div>
        );
    }

    return (
        <MotionButton
            onClick={() => onChoose(choice)}
            whileTap={{ scale: 0.98 }}
            className="w-full text-left rounded-xl px-4 py-3.5 mb-2.5 transition-all bg-[#FEFDFB] dark:bg-zinc-900"
            style={{ border: '1px solid rgba(0,0,0,0.06)', borderRadius: 14, boxShadow: '0 2px 8px rgba(0,0,0,0.04)' }}
            onMouseEnter={(e: any) => { e.currentTarget.style.borderColor = phaseColor; e.currentTarget.style.boxShadow = `0 4px 16px ${phaseColor}20`; e.currentTarget.style.transform = 'translateY(-1px)'; }}
            onMouseLeave={(e: any) => { e.currentTarget.style.borderColor = 'rgba(0,0,0,0.06)'; e.currentTarget.style.boxShadow = '0 2px 8px rgba(0,0,0,0.04)'; e.currentTarget.style.transform = 'translateY(0)'; }}
        >
            <div className="flex items-center gap-3">
                <span className="text-[11px] font-bold w-5 h-5 rounded-md flex items-center justify-center shrink-0" style={{ backgroundColor: `${phaseColor}12`, color: phaseColor }}>{letter}</span>
                <div className="flex-1 min-w-0">
                    <p className="text-[15px] font-medium text-[#1C1917] dark:text-white">{choice.text}</p>
                    {choice.flavor && <p className="text-[11px] mt-0.5 italic text-[#A8A29E] dark:text-zinc-500">{choice.flavor}</p>}
                </div>
            </div>
        </MotionButton>
    );
};

// ─── ReportCard (magazine editorial) ────────────────────────────────────────

const ReportCard: React.FC<{ endingId: string; gameState: GameState; history: HistoryItem[]; onRestart: () => void; onSelectModule?: (moduleId: string) => void }> = ({ endingId, gameState, history, onRestart, onSelectModule }) => {
    const archetype = ARCHETYPES[endingId];
    const endScene = STORY_DATA[endingId];
    const turningPoints = getKeyTurningPoints(history);
    const weakestStat = getWeakestStat(gameState);
    const recommendedModules = STAT_TO_MODULES[weakestStat];

    // Compute branching path tree data
    const pathNodes = history.map((item) => {
        return { title: item.scene.title, phase: item.scene.phase, month: item.scene.month, choiceText: item.choiceText };
    });

    // Paths not taken — locked choices the player missed
    const pathsNotTaken: { sceneTitle: string; choiceText: string; requirement: string }[] = [];
    for (const item of history) {
        const choices = item.scene.choices || [];
        for (const alt of choices) {
            if (alt.text !== item.choiceText && alt.requires) {
                const reqText = alt.requires.map(r => `${STAT_LABELS[r.stat]} ${r.min}+`).join(', ');
                const meetsReqs = alt.requires.every(r => gameState[r.stat] >= r.min);
                if (!meetsReqs) {
                    pathsNotTaken.push({ sceneTitle: item.scene.title, choiceText: alt.text, requirement: reqText });
                }
            }
        }
    }

    const phases: Phase[] = ['Foundation', 'Pressure Cooker', 'Final Stretch'];
    const groupedPath = phases
        .map(phase => ({ phase, nodes: pathNodes.filter(n => n.phase === phase) }))
        .filter(g => g.nodes.length > 0);

    return (
        <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-16">
            {/* A. Archetype Reveal — editorial hero */}
            <MotionDiv
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, ease: 'easeOut' }}
                className="min-h-[50vh] flex flex-col items-center justify-center text-center py-16"
            >
                <p className="font-mono text-[10px] font-bold uppercase tracking-[0.3em] text-[var(--accent-hex)] mb-4">Your Archetype</p>
                <h3 className="font-serif text-5xl sm:text-6xl font-semibold text-zinc-900 dark:text-white mb-6">
                    {archetype?.title || endScene?.title || 'Results Day'}
                </h3>
                <p className="text-lg text-zinc-600 dark:text-zinc-300 leading-relaxed max-w-lg mx-auto">
                    {archetype?.description || endScene?.text}
                </p>
            </MotionDiv>

            {/* B. Animated Pentagon Radar — monochrome */}
            <div className="-mt-4">
                <p className="font-mono text-[11px] font-bold uppercase tracking-[0.25em] text-zinc-400 dark:text-zinc-500 mb-2 text-center">Your Grades</p>
                <div className="flex justify-center">
                    <svg viewBox="0 0 400 330" className="w-full max-w-lg h-auto">
                        {[0.25, 0.5, 0.75, 1].map(scale => (
                            <polygon
                                key={scale}
                                points={pentagonPoints(200, 170, 110 * scale)}
                                fill="none"
                                stroke="currentColor"
                                strokeWidth="0.5"
                                className="text-zinc-200 dark:text-white/10"
                            />
                        ))}
                        <MotionPolygon
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1, points: statPentagonPoints(gameState, 200, 170, 110) }}
                            transition={{ duration: 1, ease: 'easeOut' }}
                            style={{ fill: 'rgba(var(--accent), 0.15)', stroke: 'var(--accent-hex)' }}
                            strokeWidth="2"
                        />
                        {(Object.keys(gameState) as StatKey[]).map((stat, i) => {
                            const angle = (Math.PI * 2 * i) / 5 - Math.PI / 2;
                            const lx = 200 + 140 * Math.cos(angle);
                            const ly = 170 + 140 * Math.sin(angle);
                            return (
                                <g key={stat}>
                                    <text x={lx} y={ly - 6} textAnchor="middle" dominantBaseline="middle"
                                        className="text-[15px] font-bold fill-current font-mono text-zinc-700 dark:text-zinc-200">
                                        {getStatGrade(gameState[stat]).letter}
                                    </text>
                                    <text x={lx} y={ly + 8} textAnchor="middle" dominantBaseline="middle"
                                        className="text-[9px] fill-current font-mono text-zinc-400 dark:text-zinc-500">
                                        {STAT_LABELS[stat]}
                                    </text>
                                </g>
                            );
                        })}
                    </svg>
                </div>
            </div>

            {/* B2. Weakest Stat Insight — editorial callout */}
            <div>
                <div className="w-12 h-px bg-[var(--accent-hex)] mb-6" />
                <p className="font-mono text-[11px] font-bold uppercase tracking-[0.25em] text-[var(--accent-hex)] mb-2">Your Biggest Vulnerability</p>
                <h4 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white mb-3">{STAT_LABELS[weakestStat]}</h4>
                <p className="text-zinc-600 dark:text-zinc-300 leading-relaxed max-w-2xl">
                    {WEAKEST_STAT_INSIGHTS[weakestStat]}
                </p>
            </div>

            {/* C. Key Turning Points — editorial */}
            {turningPoints.length > 0 && (
                <div>
                    <p className="font-mono text-[11px] font-bold uppercase tracking-[0.25em] text-zinc-400 dark:text-zinc-500 mb-6 text-center">Key Turning Points</p>
                    <div className="space-y-8">
                        {turningPoints.map((item, index) => (
                            <div key={index}>
                                <p className="font-mono text-[11px] font-bold uppercase tracking-[0.2em] text-[var(--accent-hex)] mb-1">{item.scene.month}</p>
                                <h5 className="font-serif text-xl font-semibold text-zinc-900 dark:text-white mb-1">{item.scene.title}</h5>
                                <p className="text-zinc-600 dark:text-zinc-400">{item.choiceText}</p>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* D. Paths Not Taken */}
            {pathsNotTaken.length > 0 && (
                <div>
                    <p className="font-mono text-[11px] font-bold uppercase tracking-[0.25em] text-zinc-400 dark:text-zinc-500 mb-6 text-center">Paths Not Taken</p>
                    <div className="space-y-4">
                        {pathsNotTaken.slice(0, 3).map((path, index) => (
                            <div key={index} className="border-t border-zinc-200 dark:border-white/10 pt-4">
                                <div className="flex items-center gap-2 mb-1">
                                    <Lock size={12} className="text-zinc-400 dark:text-zinc-500" />
                                    <p className="font-mono text-[11px] font-bold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">{path.sceneTitle}</p>
                                </div>
                                <p className="text-zinc-500 dark:text-zinc-400 italic">{path.choiceText}</p>
                                <p className="font-mono text-[10px] text-zinc-400 dark:text-zinc-500 mt-1 uppercase tracking-wider">Required: {path.requirement}</p>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* E. Recommended Modules */}
            <div>
                <p className="font-mono text-[11px] font-bold uppercase tracking-[0.25em] text-zinc-400 dark:text-zinc-500 mb-1 text-center">Recommended For You</p>
                <p className="text-xs text-zinc-400 dark:text-zinc-500 text-center mb-6">Based on your weakest area: {STAT_LABELS[weakestStat]}</p>
                <div className="space-y-0">
                    {recommendedModules.map(mod => (
                        <button
                            key={mod.moduleId}
                            onClick={() => onSelectModule?.(mod.moduleId)}
                            className="w-full text-left py-4 border-t border-zinc-200 dark:border-white/10 group transition-colors"
                        >
                            <div className="flex items-center justify-between">
                                <p className="font-serif text-lg text-zinc-700 dark:text-zinc-200 group-hover:text-[var(--accent-hex)] transition-colors">{mod.moduleTitle}</p>
                                <ArrowRight size={14} className="text-zinc-300 dark:text-zinc-600 group-hover:text-[var(--accent-hex)] transition-colors flex-shrink-0" />
                            </div>
                        </button>
                    ))}
                </div>
            </div>

            {/* F. Decision Path — monochrome vertical line */}
            <div>
                <p className="font-mono text-[11px] font-bold uppercase tracking-[0.25em] text-zinc-400 dark:text-zinc-500 mb-6 text-center">Your Path</p>
                <div className="relative pl-8">
                    <div className="absolute left-3 top-0 bottom-0 w-px bg-zinc-200 dark:bg-white/10" />

                    {groupedPath.map(({ phase, nodes }) => (
                        <div key={phase} className="mb-8">
                            <div className="flex items-center gap-2 mb-4 -ml-8">
                                <div className="w-6 h-6 rounded-full bg-[var(--accent-hex)] flex items-center justify-center ring-4 ring-white dark:ring-zinc-950">
                                    <div className="w-2 h-2 rounded-full bg-white" />
                                </div>
                                <span className="font-mono text-[10px] font-bold uppercase tracking-[0.2em] text-[var(--accent-hex)]">{phase}</span>
                            </div>

                            {nodes.map((node, ni) => (
                                <div key={ni} className="relative mb-4">
                                    <div className="absolute -left-8 top-1.5 w-6 h-6 flex items-center justify-center">
                                        <div className="w-2 h-2 rounded-full bg-zinc-300 dark:bg-zinc-600" />
                                    </div>
                                    <p className="font-mono text-[10px] text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">{node.title}</p>
                                    <p className="text-sm text-[var(--accent-hex)] dark:text-[var(--accent-hex)] mt-0.5">{node.choiceText.length > 80 ? node.choiceText.slice(0, 78) + '...' : node.choiceText}</p>
                                </div>
                            ))}
                        </div>
                    ))}

                    <div className="relative -ml-8 flex items-center gap-2">
                        <div className="w-6 h-6 rounded-full bg-[var(--accent-hex)] flex items-center justify-center ring-4 ring-white dark:ring-zinc-950">
                            <div className="w-2 h-2 rounded-full bg-white" />
                        </div>
                        <span className="font-mono text-[10px] font-bold text-[var(--accent-hex)] uppercase tracking-wider">{archetype?.title || 'End'}</span>
                    </div>
                </div>
            </div>

            {/* Play Again */}
            <div className="text-center py-8">
                <button
                    onClick={onRestart}
                    className="font-mono text-[11px] font-bold uppercase tracking-[0.25em] text-[var(--accent-hex)] hover:text-[var(--accent-dark-hex)] dark:hover:text-[var(--accent-hex)] transition-colors"
                >
                    Play Again
                </button>
            </div>
        </MotionDiv>
    );
};

// ─── AcademicJourneyGame ─────────────────────────────────────────────────────

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
    const [showStatOverlay, setShowStatOverlay] = useState(false);
    const [lastEffects, setLastEffects] = useState<Partial<GameState> | null>(null);
    const [lastModuleLink, setLastModuleLink] = useState<Choice['moduleLink'] | null>(null);
    const [previousResult, setPreviousResult] = useState<{ endingId: string; completedAt?: string; finalStats?: GameState } | null>(savedJourneyResult || null);
    const [showingSavedResult, setShowingSavedResult] = useState(!!savedJourneyResult);
    const hasSavedRef = useRef(false);
    const overlayTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

    const currentScene = STORY_DATA[currentSceneId];
    const isEndScene = currentSceneId.startsWith('END_');

    // Load previous journey result from Firestore
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
            } catch (err) {
                if (!cancelled) console.error('Failed to load journey result:', err);
            }
        };
        loadPrevious();
        return () => { cancelled = true; };
    }, [user?.uid]);

    // Save journey result when game ends
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
            scene: currentChoiceScene,
            choiceText: choice.text,
            effects: choice.effects,
            moduleLink: choice.moduleLink,
        };
        const newHistory = [...history, newHistoryItem];
        setHistory(newHistory);
        setPrevState(gameState);
        setGameState(newGameState);
        // Resolve route
        let targetSceneId = choice.nextSceneId;
        while (targetSceneId.startsWith('__') && ROUTE_RESOLVERS[targetSceneId]) {
            targetSceneId = ROUTE_RESOLVERS[targetSceneId](newGameState, newHistory);
        }

        setVisitedScenes(prev => [...prev, targetSceneId]);

        // Show ephemeral overlay, then advance
        setChosenText(choice.text);
        setLastEffects(choice.effects);
        setLastModuleLink(choice.moduleLink || null);
        setShowStatOverlay(true);
        setPendingSceneId(targetSceneId);

        // Clear overlay timer if one exists
        if (overlayTimerRef.current) clearTimeout(overlayTimerRef.current);

        overlayTimerRef.current = setTimeout(() => {
            setShowStatOverlay(false);
            setChosenText(null);
            setLastEffects(null);
            setLastModuleLink(null);

            const targetScene = STORY_DATA[targetSceneId];
            if (targetScene && targetScene.phase !== currentChoiceScene.phase) {
                setCurrentPhase(targetScene.phase);
                setShowPhaseTransition(true);
                // Keep pendingSceneId so handlePhaseTransitionComplete can advance
            } else {
                setCurrentSceneId(targetSceneId);
                setPendingSceneId(null);
            }
        }, 2500);
    }, [currentSceneId, gameState, history]);

    const handlePhaseTransitionComplete = useCallback(() => {
        setShowPhaseTransition(false);
        if (pendingSceneId) {
            setCurrentSceneId(pendingSceneId);
            setPendingSceneId(null);
        }
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
        setShowStatOverlay(false);
        setLastEffects(null);
        setLastModuleLink(null);
        hasSavedRef.current = false;
        if (overlayTimerRef.current) clearTimeout(overlayTimerRef.current);
    }, []);

    // Saved result screen (editorial treatment)
    if (showingSavedResult && previousResult?.endingId && ARCHETYPES[previousResult.endingId]) {
        const savedArch = ARCHETYPES[previousResult.endingId];
        const savedStats = previousResult.finalStats || { ...INITIAL_GAME_STATE };
        const savedWeakestStat = getWeakestStat(savedStats);
        return (
            <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-16">
                {/* Archetype — editorial hero */}
                <div className="min-h-[40vh] flex flex-col items-center justify-center text-center py-16">
                    <p className="font-mono text-[10px] font-bold uppercase tracking-[0.3em] text-[var(--accent-hex)] mb-4">Your Previous Result</p>
                    <h3 className="font-serif text-5xl sm:text-6xl font-semibold text-zinc-900 dark:text-white mb-6">{savedArch.title}</h3>
                    <p className="text-lg text-zinc-600 dark:text-zinc-300 leading-relaxed max-w-lg mx-auto">{savedArch.description}</p>
                </div>

                {/* Pentagon Radar — monochrome */}
                <div>
                    <p className="font-mono text-[11px] font-bold uppercase tracking-[0.25em] text-zinc-400 dark:text-zinc-500 mb-4 text-center">Your Grades</p>
                    <div className="flex justify-center">
                        <svg viewBox="0 0 400 330" className="w-full max-w-lg h-auto">
                            {[0.25, 0.5, 0.75, 1].map(scale => (
                                <polygon
                                    key={scale}
                                    points={pentagonPoints(200, 170, 110 * scale)}
                                    fill="none"
                                    stroke="currentColor"
                                    strokeWidth="0.5"
                                    className="text-zinc-200 dark:text-white/10"
                                />
                            ))}
                            <MotionPolygon
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1, points: statPentagonPoints(savedStats, 200, 170, 110) }}
                                transition={{ duration: 1, ease: 'easeOut' }}
                                style={{ fill: 'rgba(var(--accent), 0.15)', stroke: 'var(--accent-hex)' }}
                                strokeWidth="2"
                            />
                            {(Object.keys(savedStats) as StatKey[]).map((stat, i) => {
                                const angle = (Math.PI * 2 * i) / 5 - Math.PI / 2;
                                const lx = 200 + 140 * Math.cos(angle);
                                const ly = 170 + 140 * Math.sin(angle);
                                return (
                                    <g key={stat}>
                                        <text x={lx} y={ly - 6} textAnchor="middle" dominantBaseline="middle"
                                            className="text-[15px] font-bold fill-current font-mono text-zinc-700 dark:text-zinc-200">
                                            {getStatGrade(savedStats[stat]).letter}
                                        </text>
                                        <text x={lx} y={ly + 8} textAnchor="middle" dominantBaseline="middle"
                                            className="text-[9px] fill-current font-mono text-zinc-400 dark:text-zinc-500">
                                            {STAT_LABELS[stat]}
                                        </text>
                                    </g>
                                );
                            })}
                        </svg>
                    </div>
                </div>

                {/* Vulnerability — editorial callout */}
                <div>
                    <div className="w-12 h-px bg-[var(--accent-hex)] mb-6" />
                    <p className="font-mono text-[11px] font-bold uppercase tracking-[0.25em] text-[var(--accent-hex)] mb-2">Your Biggest Vulnerability</p>
                    <h4 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white mb-3">{STAT_LABELS[savedWeakestStat]}</h4>
                    <p className="text-zinc-600 dark:text-zinc-300 leading-relaxed max-w-2xl">
                        {WEAKEST_STAT_INSIGHTS[savedWeakestStat]}
                    </p>
                </div>

                {/* Recommended Modules */}
                <div>
                    <p className="font-mono text-[11px] font-bold uppercase tracking-[0.25em] text-zinc-400 dark:text-zinc-500 mb-1 text-center">Recommended For You</p>
                    <p className="text-xs text-zinc-400 dark:text-zinc-500 text-center mb-6">Based on your weakest area: {STAT_LABELS[savedWeakestStat]}</p>
                    <div className="space-y-0">
                        {STAT_TO_MODULES[savedWeakestStat].map(mod => (
                            <button
                                key={mod.moduleId}
                                onClick={() => onSelectModule?.(mod.moduleId)}
                                className="w-full text-left py-4 border-t border-zinc-200 dark:border-white/10 group transition-colors"
                            >
                                <div className="flex items-center justify-between">
                                    <p className="font-serif text-lg text-zinc-700 dark:text-zinc-200 group-hover:text-[var(--accent-hex)] transition-colors">{mod.moduleTitle}</p>
                                    <ArrowRight size={14} className="text-zinc-300 dark:text-zinc-600 group-hover:text-[var(--accent-hex)] transition-colors flex-shrink-0" />
                                </div>
                            </button>
                        ))}
                    </div>
                </div>

                {/* Play Again */}
                <div className="text-center py-8">
                    <button
                        onClick={() => { setShowingSavedResult(false); restartGame(); }}
                        className="font-mono text-[11px] font-bold uppercase tracking-[0.25em] text-[var(--accent-hex)] hover:text-[var(--accent-dark-hex)] dark:hover:text-[var(--accent-hex)] transition-colors"
                    >
                        Play Again
                    </button>
                </div>
            </MotionDiv>
        );
    }

    // End screen
    if (isEndScene) {
        return <ReportCard endingId={currentSceneId} gameState={gameState} history={history} onRestart={restartGame} onSelectModule={onSelectModule} />;
    }

    // Phase transition interstitial
    if (showPhaseTransition) {
        return (
            <AnimatePresence mode="wait">
                <PhaseTransition key={currentPhase} phase={currentPhase} onComplete={handlePhaseTransitionComplete} />
            </AnimatePresence>
        );
    }

    if (!currentScene || !currentScene.choices) {
        return null;
    }

    const locationConfig = LOCATION_CONFIG[currentScene.location];

    return (
        <>
            {/* Ephemeral Stat Overlay — portaled to body to escape Framer transform context */}
            {createPortal(
                <AnimatePresence>
                    {showStatOverlay && lastEffects && (
                        <EphemeralStatOverlay effects={lastEffects} gameState={gameState} />
                    )}
                </AnimatePresence>,
                document.body
            )}

            {/* Scene — Headspace editorial layout */}
            {(() => {
                const phaseConfig = PHASE_COLORS[currentScene.phase] || PHASE_COLORS['Foundation'];
                const phaseMeta = PHASE_METADATA.find(p => p.name === currentScene.phase);
                const pc = phaseConfig.bg;

                return (
                    <AnimatePresence mode="wait">
                        <MotionDiv
                            key={currentSceneId}
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            transition={{ duration: 0.4, ease: editorialEase }}
                        >
                            {/* ── Full-bleed colour hero ── */}
                            <div
                                className="relative overflow-hidden"
                                style={{
                                    backgroundColor: pc,
                                    position: 'relative',
                                    left: '50%',
                                    right: '50%',
                                    marginLeft: '-50vw',
                                    marginRight: '-50vw',
                                    width: '100vw',
                                }}
                            >
                                {/* Decorative blobs — layered system */}
                                <div className="absolute pointer-events-none" style={{ top: -60, right: -40, width: 280, height: 280, borderRadius: '50%', background: 'rgba(255,255,255,0.1)' }} />
                                <div className="absolute pointer-events-none" style={{ top: 20, right: 30, width: 100, height: 100, borderRadius: '50%', background: 'rgba(255,255,255,0.06)' }} />
                                <div className="absolute pointer-events-none" style={{ bottom: 40, left: -50, width: 200, height: 200, borderRadius: '50%', background: 'rgba(0,0,0,0.06)' }} />

                                {/* Centered content within the full-bleed field */}
                                <div className="relative z-10 max-w-2xl mx-auto px-6 pt-10 pb-16">
                                    <MotionDiv initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1, duration: 0.4 }}>
                                        <div className="flex items-center gap-3 mb-2">
                                            <span className="text-[10px] font-bold uppercase tracking-[0.2em]" style={{ color: 'rgba(255,255,255,0.5)' }}>{currentScene.phase}</span>
                                            <span className="text-[10px]" style={{ color: 'rgba(255,255,255,0.25)' }}>|</span>
                                            <span className="text-[10px] uppercase tracking-[0.15em]" style={{ color: 'rgba(255,255,255,0.5)' }}>{phaseMeta?.months}</span>
                                        </div>
                                        <p className="text-[11px] font-semibold uppercase tracking-[0.12em] mb-6" style={{ color: 'rgba(255,255,255,0.55)' }}>
                                            {currentScene.month} — {locationConfig.label}
                                        </p>
                                    </MotionDiv>

                                    <MotionDiv initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2, duration: 0.5 }}>
                                        <h2 className="font-serif text-3xl sm:text-5xl font-bold text-white leading-tight">{currentScene.title}</h2>
                                    </MotionDiv>
                                </div>

                                {/* Wavy edge to cream */}
                                <div className="absolute bottom-0 left-0 right-0" style={{ transform: 'translateY(1px)' }}>
                                    <svg viewBox="0 0 1440 48" preserveAspectRatio="none" className="block w-full" style={{ height: 40 }}>
                                        <path d="M0,24 C240,48 480,8 720,32 C960,56 1200,16 1440,28 L1440,48 L0,48 Z" className="fill-[#FDF8F0] dark:fill-zinc-900" />
                                    </svg>
                                </div>
                            </div>

                            {/* ── Content on cream ── */}
                            <div className="max-w-2xl mx-auto px-6 pt-5 pb-8">
                                <MotionDiv initial={{ opacity: 0, y: 4 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3, duration: 0.4 }}>
                                    <p className="text-xs mb-6 leading-relaxed text-[#A8A29E] dark:text-zinc-500">{phaseMeta?.subtitle}</p>
                                </MotionDiv>

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
                                                if ('visited' in v.condition && visitedScenes.includes(v.condition.visited)) {
                                                    return v.text;
                                                }
                                            }
                                        }
                                        return currentScene.text;
                                    })()}
                                    sceneId={currentSceneId}
                                />

                                <p className="text-[10px] font-bold uppercase tracking-[0.15em] mb-3 text-[#A8A29E] dark:text-zinc-500">What do you do?</p>

                                <div>
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
                                            phaseColor={pc}
                                        />
                                    ))}
                                </div>

                                {lastModuleLink && chosenText && (
                                    <p className="text-xs italic mt-4 text-[#A8A29E] dark:text-zinc-500">
                                        Related: <span className="font-semibold" style={{ color: pc }}>{lastModuleLink.moduleTitle}</span>
                                    </p>
                                )}

                                {currentSceneId === 'START' && previousResult && ARCHETYPES[previousResult.endingId] && (
                                    <div className="mt-6 px-4 py-3 rounded-xl" style={{ backgroundColor: `${pc}10`, border: `1px solid ${pc}20`, borderRadius: 12 }}>
                                        <p className="text-[11px] text-[#78716C] dark:text-zinc-400">
                                            Previous result: <span className="font-bold" style={{ color: pc }}>{ARCHETYPES[previousResult.endingId].title}</span>
                                        </p>
                                    </div>
                                )}
                            </div>
                        </MotionDiv>
                    </AnimatePresence>
                );
            })()}
        </>
    );
};

export default AcademicJourneyGame;
