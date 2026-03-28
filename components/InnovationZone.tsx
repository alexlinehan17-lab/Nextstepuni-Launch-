
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect, useCallback, useRef, useMemo } from 'react';
import { useToast } from './Toast';
import { createPortal } from 'react-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
    ArrowLeft, ArrowRight, Zap, Clock, Shield, RotateCcw,
    TrendingUp, Users, BookOpen, BookMarked,
    Lock, Compass, Brain, HandHelping, Target, ArrowUpRight, Award, Megaphone,
    Flame, Scale, Settings, CalendarDays, Calculator, GitBranch, Rocket,
    Map, ScanSearch
} from 'lucide-react';
import { doc, setDoc, getDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { type StudentSubjectProfile, type TimetableCompletions, type TimetableStreak, type StudyBlock, getBlockId, toDateKey } from './subjectData';
import { type SchoolEvent } from './gc/GCKeyEvents';
import { computeStreak, computeSubjectPriorities, allocateSessions, generateWeeklyTimetable, computeWeeksUntilExam } from './timetableAlgorithm';
import { type StudyReflection, type PointsData, type CosmeticUnlocks, type EarnedRest, type UserSettings } from '../types';
import SubjectOnboarding from './SubjectOnboarding';
import SpacedRepetitionTimetable from './SpacedRepetitionTimetable';
import WarRoom from './WarRoom';
import ComebackEngine from './ComebackEngine';
import CAOPointsSimulator from './CAOPointsSimulator';

import FutureFinder from './FutureFinder';
import SyllabusXRay from './SyllabusXRay';
import PointsPassport from './PointsPassport';
import { getNotifications, type AppNotification } from './gc/gcNotifications';
// ReflectionModal import removed — "Already Studied" flow gives 2 pts, no reflection
import StudyJournalModal from './StudyJournalModal';
import RewardShopModal from './RewardShopModal';
import {
    type GameState, type Choice, type Scene, type HistoryItem, type StatKey, type Phase,
    type Mood, type Location,
    STORY_DATA, ROUTE_RESOLVERS, INITIAL_GAME_STATE, PHASE_METADATA,
    ARCHETYPES, STAT_TO_MODULES, STAT_LABELS,
    WEAKEST_STAT_INSIGHTS,
    getStatGrade, getKeyTurningPoints, getWeakestStat,
} from './journeySimulatorData';

const MotionDiv = motion.div as any;
const MotionButton = motion.button as any;
const MotionSpan = motion.span as any;
const MotionPolygon = motion.polygon as any;

interface JourneyResult {
  endingId: string;
  finalStats?: GameState;
}

interface InnovationZoneProps {
  onBack: () => void;
  onSelectModule?: (moduleId: string) => void;
  user?: { uid: string; school?: string; yearGroup?: '5th' | '6th' } | null;
  autoOpenJourney?: boolean;
  savedJourneyResult?: JourneyResult | null;
  onJourneyComplete?: (result: JourneyResult) => void;
  settings: UserSettings;
  updateSetting: <K extends keyof UserSettings>(key: K, value: UserSettings[K]) => void;
  onCosmeticUnlocksChange?: (unlocks: CosmeticUnlocks) => void;
  onStudyNow?: (block: { subject: string; sessionType: 'new-learning' | 'practice' | 'revision'; durationMinutes: number; dateKey: string; blockId: string }) => void;
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

const ARCHETYPE_ICONS: Record<string, React.ElementType> = {
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
            <div className="rounded-xl px-4 py-3 mb-2 opacity-25" style={{ backgroundColor: '#FEFDFB', border: '1px solid #EDEBE8', borderRadius: 12 }}>
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
            className="w-full text-left rounded-xl px-4 py-3.5 mb-2.5 transition-all"
            style={{ backgroundColor: '#FEFDFB', border: '1px solid rgba(0,0,0,0.06)', borderRadius: 14, boxShadow: '0 2px 8px rgba(0,0,0,0.04)' }}
            onMouseEnter={(e: any) => { e.currentTarget.style.borderColor = phaseColor; e.currentTarget.style.boxShadow = `0 4px 16px ${phaseColor}20`; e.currentTarget.style.transform = 'translateY(-1px)'; }}
            onMouseLeave={(e: any) => { e.currentTarget.style.borderColor = 'rgba(0,0,0,0.06)'; e.currentTarget.style.boxShadow = '0 2px 8px rgba(0,0,0,0.04)'; e.currentTarget.style.transform = 'translateY(0)'; }}
        >
            <div className="flex items-center gap-3">
                <span className="text-[11px] font-bold w-5 h-5 rounded-md flex items-center justify-center shrink-0" style={{ backgroundColor: `${phaseColor}12`, color: phaseColor }}>{letter}</span>
                <div className="flex-1 min-w-0">
                    <p className="text-[15px] font-medium" style={{ color: '#1C1917' }}>{choice.text}</p>
                    {choice.flavor && <p className="text-[11px] mt-0.5 italic" style={{ color: '#A8A29E' }}>{choice.flavor}</p>}
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
    const [gameState, setGameState] = useState<GameState>({ ...INITIAL_GAME_STATE });
    const [prevState, setPrevState] = useState<GameState>({ ...INITIAL_GAME_STATE });
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
            } catch (e) {
                if (!cancelled) console.error('Failed to load journey result:', e);
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
                } catch (e) {
                    if (cancelled) return;
                    console.error('Failed to save journey result:', e);
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
                                        <path d="M0,24 C240,48 480,8 720,32 C960,56 1200,16 1440,28 L1440,48 L0,48 Z" fill="#FDF8F0" />
                                    </svg>
                                </div>
                            </div>

                            {/* ── Content on cream ── */}
                            <div className="max-w-2xl mx-auto px-6 pt-5 pb-8">
                                <MotionDiv initial={{ opacity: 0, y: 4 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3, duration: 0.4 }}>
                                    <p className="text-xs mb-6 leading-relaxed" style={{ color: '#A8A29E' }}>{phaseMeta?.subtitle}</p>
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

                                <p className="text-[10px] font-bold uppercase tracking-[0.15em] mb-3" style={{ color: '#A8A29E' }}>What do you do?</p>

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
                                    <p className="text-xs italic mt-4" style={{ color: '#A8A29E' }}>
                                        Related: <span className="font-semibold" style={{ color: pc }}>{lastModuleLink.moduleTitle}</span>
                                    </p>
                                )}

                                {currentSceneId === 'START' && previousResult && ARCHETYPES[previousResult.endingId] && (
                                    <div className="mt-6 px-4 py-3 rounded-xl" style={{ backgroundColor: `${pc}10`, border: `1px solid ${pc}20`, borderRadius: 12 }}>
                                        <p className="text-[11px]" style={{ color: '#78716C' }}>
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

// ─── Data Validation Helpers ─────────────────────────────────────────────────

/** Ensures a value is a finite number, falling back to a default. */
function safeNum(val: unknown, fallback: number = 0): number {
    if (typeof val === 'number' && Number.isFinite(val)) return val;
    return fallback;
}

/** Validates PointsData from Firestore, ensuring no NaN or undefined values. */
function validatePointsData(raw: unknown): PointsData {
    if (!raw || typeof raw !== 'object') return { totalEarned: 0, totalSpent: 0 };
    const obj = raw as Record<string, unknown>;
    return {
        totalEarned: safeNum(obj.totalEarned),
        totalSpent: safeNum(obj.totalSpent),
    };
}

// ─── InnovationZone ──────────────────────────────────────────────────────────

const InnovationZone: React.FC<InnovationZoneProps> = ({ onBack, onSelectModule, user, autoOpenJourney, savedJourneyResult, onJourneyComplete, settings, updateSetting, onCosmeticUnlocksChange, onStudyNow }) => {
    const { showToast } = useToast();
    const [activeTool, setActiveTool] = useState<string | null>(autoOpenJourney ? 'journey' : null);
    const [subjectProfile, setSubjectProfile] = useState<StudentSubjectProfile | null>(null);
    const [showOnboarding, setShowOnboarding] = useState(false);
    const [profileLoaded, setProfileLoaded] = useState(false);
    const [pendingToolId, setPendingToolId] = useState<string | null>(null);
    const [timetableCompletions, setTimetableCompletions] = useState<TimetableCompletions>({});
    const [timetableStreak, setTimetableStreak] = useState<TimetableStreak>({ currentStreak: 0, lastActiveDate: '', longestStreak: 0 });
    const [reflections, setReflections] = useState<StudyReflection[]>([]);
    const [pointsData, setPointsData] = useState<PointsData>({ totalEarned: 0, totalSpent: 0 });
    const [cosmeticUnlocks, setCosmeticUnlocks] = useState<CosmeticUnlocks>({ avatarSeeds: [], themeColors: [], cardStyles: [] });
    const [earnedRest, setEarnedRest] = useState<EarnedRest>({ skippedSessions: [], restDayPasses: [] });
    const [schoolEvents, setSchoolEvents] = useState<SchoolEvent[]>([]);
    const [gcRecommendations, setGcRecommendations] = useState<Record<string, { fromName: string; message?: string }>>({});

    // Load school events for student's school + year group
    useEffect(() => {
        if (!user?.school) return;
        let cancelled = false;
        const loadEvents = async () => {
            try {
                const eventsDoc = await getDoc(doc(db, 'gcEvents', user.school!));
                if (cancelled) return;
                if (eventsDoc.exists()) {
                    const data = eventsDoc.data();
                    const allEvents: SchoolEvent[] = data.events || [];
                    const yg = user.yearGroup || '6th';
                    setSchoolEvents(allEvents.filter(e => e.yearGroup === 'both' || e.yearGroup === yg));
                }
            } catch (e) {
                if (!cancelled) console.error('Failed to load school events:', e);
            }
        };
        loadEvents();
        return () => { cancelled = true; };
    }, [user?.school, user?.yearGroup]);

    // Refs to always access latest state in callbacks (avoids stale closures)
    const pointsDataRef = useRef(pointsData);
    pointsDataRef.current = pointsData;
    const cosmeticUnlocksRef = useRef(cosmeticUnlocks);
    cosmeticUnlocksRef.current = cosmeticUnlocks;
    const earnedRestRef = useRef(earnedRest);
    earnedRestRef.current = earnedRest;
    const onCosmeticUnlocksChangeRef = useRef(onCosmeticUnlocksChange);
    onCosmeticUnlocksChangeRef.current = onCosmeticUnlocksChange;
    const [showRewardShop, setShowRewardShop] = useState(false);
    const [showJournal, setShowJournal] = useState(false);
    const [showPointsExplainer, setShowPointsExplainer] = useState(() => {
        try { return !localStorage.getItem('nextstep-points-explainer-v2'); } catch { return true; }
    });

    const dismissPointsExplainer = useCallback(() => {
        setShowPointsExplainer(false);
        try { localStorage.setItem('nextstep-points-explainer-v2', '1'); } catch {}
    }, []);

    // Load subject profile from Firebase
    useEffect(() => {
        if (!user?.uid) { setProfileLoaded(true); return; }
        let cancelled = false;
        const loadProfile = async () => {
            try {
                const progressDoc = await getDoc(doc(db, 'progress', user.uid));
                if (cancelled) return;
                if (progressDoc.exists()) {
                    const data = progressDoc.data();
                    if (data.subjectProfile) {
                        setSubjectProfile({ restDays: [], ...data.subjectProfile } as StudentSubjectProfile);
                    }
                    if (data.timetableCompletions) {
                        setTimetableCompletions(data.timetableCompletions as TimetableCompletions);
                    }
                    if (data.timetableStreak) {
                        setTimetableStreak(data.timetableStreak as TimetableStreak);
                    }
                    if (data.reflections) {
                        setReflections(data.reflections as StudyReflection[]);
                    }
                    setPointsData(validatePointsData(data.pointsData));
                    if (data.cosmeticUnlocks) {
                        setCosmeticUnlocks({
                            avatarSeeds: [],
                            themeColors: [],
                            cardStyles: [],
                            ...data.cosmeticUnlocks,
                        });
                    }
                    if (data.earnedRest) {
                        setEarnedRest(data.earnedRest as EarnedRest);
                    }
                }
            } catch (e) {
                if (!cancelled) console.error('Failed to load subject profile:', e);
            }
            if (!cancelled) setProfileLoaded(true);
        };
        loadProfile();
        return () => { cancelled = true; };
    }, [user?.uid]);

    // Load GC recommendations from notifications
    useEffect(() => {
        if (!user?.uid) return;
        let cancelled = false;
        const loadRecommendations = async () => {
            try {
                const notifications = await getNotifications(user.uid);
                const recMap: Record<string, { fromName: string; message?: string }> = {};
                for (const n of notifications) {
                    if (n.type === 'gc-recommendation' && !n.read && n.actionToolId && !recMap[n.actionToolId]) {
                        recMap[n.actionToolId] = { fromName: n.fromGCName || 'your counsellor', message: n.body };
                    }
                }
                if (!cancelled) setGcRecommendations(recMap);
            } catch {}
        };
        loadRecommendations();
        return () => { cancelled = true; };
    }, [user?.uid]);

    const handleOnboardingComplete = useCallback(async (profile: StudentSubjectProfile) => {
        setSubjectProfile(profile);
        setShowOnboarding(false);
        if (pendingToolId) {
            setActiveTool(pendingToolId);
            setPendingToolId(null);
        }
        if (user?.uid) {
            try {
                await setDoc(doc(db, 'progress', user.uid), { subjectProfile: profile }, { merge: true });
            } catch (e) {
                console.error('Failed to save subject profile:', e);
                showToast('Couldn\'t save — check your connection', 'error');
            }
        }
    }, [user?.uid, pendingToolId]);

    const getStreakMultiplier = useCallback((streak: number): number => {
        if (streak >= 14) return 2.5;
        if (streak >= 7) return 2.0;
        if (streak >= 3) return 1.5;
        return 1.0;
    }, []);

    const executeToggle = useCallback((dateKey: string, blockId: string, completed: boolean, extraFirestoreData?: Record<string, any>) => {
        setTimetableCompletions(prev => {
            const updated = { ...prev };
            const dayArr = [...(updated[dateKey] ?? [])];
            if (completed) {
                if (!dayArr.includes(blockId)) dayArr.push(blockId);
            } else {
                const idx = dayArr.indexOf(blockId);
                if (idx >= 0) dayArr.splice(idx, 1);
            }
            if (dayArr.length === 0) {
                delete updated[dateKey];
            } else {
                updated[dateKey] = dayArr;
            }

            const restDays = subjectProfile?.restDays ?? [];
            const { currentStreak, lastActiveDate } = computeStreak(updated, restDays, new Date(), earnedRest.restDayPasses);
            const newLongest = Math.max(timetableStreak.longestStreak, currentStreak);
            const newStreak: TimetableStreak = { currentStreak, lastActiveDate, longestStreak: newLongest };
            setTimetableStreak(newStreak);

            if (user?.uid) {
                setDoc(doc(db, 'progress', user.uid), {
                    timetableCompletions: updated,
                    timetableStreak: newStreak,
                    ...extraFirestoreData,
                }, { merge: true }).catch(e => { console.error('Failed to save completions:', e); showToast('Couldn\'t save — check your connection', 'error'); });
            }

            return updated;
        });
    }, [subjectProfile?.restDays, timetableStreak.longestStreak, user?.uid, earnedRest.restDayPasses]);

    const handleToggleCompletion = useCallback(async (dateKey: string, blockId: string, completed: boolean) => {
        if (completed) {
            // "Already Studied" flow: 2 pts flat, no reflection
            const ALREADY_STUDIED_POINTS = 2;
            const updatedPointsData: PointsData = {
                totalEarned: pointsData.totalEarned + ALREADY_STUDIED_POINTS,
                totalSpent: pointsData.totalSpent,
            };
            setPointsData(updatedPointsData);
            executeToggle(dateKey, blockId, true, {
                pointsData: updatedPointsData,
            });
        } else {
            executeToggle(dateKey, blockId, false);
        }
    }, [executeToggle, pointsData]);

    const handleSpendPoints = useCallback((type: 'skip-session' | 'rest-day-pass' | 'unlock-avatar' | 'unlock-theme' | 'unlock-card-style', detail?: string) => {
        const costs: Record<string, number> = {
            'skip-session': 20,
            'rest-day-pass': 60,
            'unlock-avatar': 50,
            'unlock-theme': 40,
            'unlock-card-style': 40,
        };
        const cost = costs[type];

        // Read latest state from refs to avoid stale closures
        const currentPoints = pointsDataRef.current;
        const currentCosmeticUnlocks = cosmeticUnlocksRef.current;
        const currentEarnedRest = earnedRestRef.current;

        const balance = currentPoints.totalEarned - currentPoints.totalSpent;
        if (balance < cost) return;

        const updatedPointsData: PointsData = {
            totalEarned: currentPoints.totalEarned,
            totalSpent: currentPoints.totalSpent + cost,
        };
        setPointsData(updatedPointsData);

        const todayKey = toDateKey(new Date());
        let updatedEarnedRest = currentEarnedRest;
        let updatedCosmeticUnlocks = currentCosmeticUnlocks;

        if (type === 'skip-session' && detail) {
            updatedEarnedRest = {
                ...currentEarnedRest,
                skippedSessions: [...currentEarnedRest.skippedSessions, detail],
            };
            setEarnedRest(updatedEarnedRest);
        } else if (type === 'rest-day-pass') {
            updatedEarnedRest = {
                ...currentEarnedRest,
                restDayPasses: [...currentEarnedRest.restDayPasses, todayKey],
            };
            setEarnedRest(updatedEarnedRest);
        } else if (type === 'unlock-avatar' && detail) {
            updatedCosmeticUnlocks = {
                ...currentCosmeticUnlocks,
                avatarSeeds: [...(currentCosmeticUnlocks.avatarSeeds || []), detail],
            };
            setCosmeticUnlocks(updatedCosmeticUnlocks);
        } else if (type === 'unlock-theme' && detail) {
            updatedCosmeticUnlocks = {
                ...currentCosmeticUnlocks,
                themeColors: [...(currentCosmeticUnlocks.themeColors || []), detail],
            };
            setCosmeticUnlocks(updatedCosmeticUnlocks);
        } else if (type === 'unlock-card-style' && detail) {
            updatedCosmeticUnlocks = {
                ...currentCosmeticUnlocks,
                cardStyles: [...(currentCosmeticUnlocks.cardStyles || []), detail],
            };
            setCosmeticUnlocks(updatedCosmeticUnlocks);
        }

        // Notify parent of cosmetic unlock changes so App.tsx state stays in sync
        if (updatedCosmeticUnlocks !== currentCosmeticUnlocks) {
            onCosmeticUnlocksChangeRef.current?.(updatedCosmeticUnlocks);
        }

        if (user?.uid) {
            setDoc(doc(db, 'progress', user.uid), {
                pointsData: updatedPointsData,
                earnedRest: updatedEarnedRest,
                cosmeticUnlocks: updatedCosmeticUnlocks,
            }, { merge: true }).catch(e => {
                console.error('Failed to save purchase:', e);
                showToast('Purchase couldn\'t be saved — check your connection', 'error');
                // Roll back to latest ref values (may have changed since write started)
                setPointsData(currentPoints);
                setEarnedRest(currentEarnedRest);
                setCosmeticUnlocks(currentCosmeticUnlocks);
                onCosmeticUnlocksChangeRef.current?.(currentCosmeticUnlocks);
            });
        }
    }, [user?.uid]);


    const handleToolClick = useCallback((toolId: string, needsProfile: boolean) => {
        if (needsProfile && !profileLoaded) return;
        if (needsProfile && !subjectProfile) {
            setPendingToolId(toolId);
            setShowOnboarding(true);
            return;
        }
        setActiveTool(toolId);
    }, [subjectProfile, profileLoaded]);

    const skippableBlocks = useMemo(() => {
        if (!subjectProfile) return [];
        const today = new Date();
        const todayKey = toDateKey(today);
        const jsDay = today.getDay();
        const todayDayIndex = jsDay === 0 ? 6 : jsDay - 1;

        const priorities = computeSubjectPriorities(subjectProfile.subjects);
        const weeksUntilExam = computeWeeksUntilExam(subjectProfile.examStartDate);
        const allocations = allocateSessions(priorities, weeksUntilExam);
        const restDaysArray = subjectProfile.restDays || [];
        const timetable = generateWeeklyTimetable(allocations, weeksUntilExam, 0, restDaysArray, subjectProfile.defaultBlockDuration ?? 45);
        const todayBlocks = timetable[todayDayIndex]?.blocks ?? [];

        const completedIds = timetableCompletions[todayKey] ?? [];
        const skippedSet = new Set(earnedRest.skippedSessions);

        return todayBlocks
            .map((block, bi) => {
                const blockId = getBlockId(block, bi);
                const fullId = `${todayKey}|${blockId}`;
                const isCompleted = completedIds.includes(blockId);
                const isSkipped = skippedSet.has(fullId);
                if (isCompleted || isSkipped) return null;
                return { blockId, fullId, subjectName: block.subjectName, sessionType: block.sessionType };
            })
            .filter((b): b is { blockId: string; fullId: string; subjectName: string; sessionType: string } => b !== null);
    }, [subjectProfile, timetableCompletions, earnedRest.skippedSessions]);

    const tools = [
        {
            id: 'journey', title: 'Academic Journey Simulator', description: 'Navigate the choices of your final school year.', icon: GitBranch, needsProfile: false,
            tag: 'Simulator', accentHex: '#f59e0b', gridClass: 'md:col-span-3',
            iconBg: 'bg-amber-100 dark:bg-amber-900/30', iconColor: 'text-amber-600 dark:text-amber-400',
            accentBarColor: 'bg-amber-500', tagBg: 'bg-amber-100 dark:bg-amber-900/30', tagText: 'text-amber-700 dark:text-amber-400',
            hoverBorder: 'hover:border-amber-400/50 dark:hover:border-amber-500/40',
            component: <AcademicJourneyGame onSelectModule={onSelectModule} user={user} savedJourneyResult={savedJourneyResult} onJourneyComplete={onJourneyComplete} />,
        },
        {
            id: 'cao-simulator', title: 'CAO Points Simulator', description: 'Explore how grade changes affect your CAO points.', icon: Calculator, needsProfile: true,
            tag: 'Simulator', accentHex: '#64748b', gridClass: 'md:col-span-3',
            iconBg: 'bg-slate-100 dark:bg-slate-800/40', iconColor: 'text-slate-600 dark:text-slate-300',
            accentBarColor: 'bg-slate-500', tagBg: 'bg-slate-100 dark:bg-slate-800/40', tagText: 'text-slate-600 dark:text-slate-300',
            hoverBorder: 'hover:border-slate-400/50 dark:hover:border-slate-500/40',
            component: subjectProfile ? <CAOPointsSimulator profile={subjectProfile} uid={user?.uid} onOpenSettings={() => setShowOnboarding(true)} /> : null,
        },
        {
            id: 'planner', title: 'Spaced Repetition Timetable', description: 'A data-driven study planner powered by your subject goals.', icon: CalendarDays, needsProfile: true,
            tag: 'Planner', accentHex: '#6366f1', gridClass: 'md:col-span-2',
            iconBg: 'bg-indigo-100 dark:bg-indigo-900/30', iconColor: 'text-indigo-600 dark:text-indigo-400',
            accentBarColor: 'bg-indigo-500', tagBg: 'bg-indigo-100 dark:bg-indigo-900/30', tagText: 'text-indigo-700 dark:text-indigo-400',
            hoverBorder: 'hover:border-indigo-400/50 dark:hover:border-indigo-500/40',
            component: subjectProfile ? <SpacedRepetitionTimetable profile={subjectProfile} uid={user?.uid} onOpenSettings={() => setShowOnboarding(true)} completions={timetableCompletions} streak={timetableStreak} onToggleCompletion={handleToggleCompletion} points={pointsData.totalEarned - pointsData.totalSpent} onOpenShop={() => setShowRewardShop(true)} onOpenJournal={() => setShowJournal(true)} skippedSessions={earnedRest.skippedSessions} onStudyNow={onStudyNow} schoolEvents={schoolEvents} onBlockDurationChange={async (_s, _t, newDuration) => { const updated = { ...subjectProfile, defaultBlockDuration: newDuration }; setSubjectProfile(updated); if (user?.uid) { try { await setDoc(doc(db, 'progress', user.uid), { subjectProfile: updated }, { merge: true }); } catch (e) { console.error('Failed to save block duration:', e); showToast('Couldn\'t save — check your connection', 'error'); } } }} onRestDaysChange={async (days) => { const updated = { ...subjectProfile, restDays: days }; setSubjectProfile(updated); if (user?.uid) { try { await setDoc(doc(db, 'progress', user.uid), { subjectProfile: updated }, { merge: true }); } catch (e) { console.error('Failed to save rest days:', e); showToast('Couldn\'t save — check your connection', 'error'); } } }} /> : null,
        },
        {
            id: 'war-room', title: 'War Room', description: 'Your strategic study command centre.', icon: Target, needsProfile: true,
            tag: 'Strategy', accentHex: '#dc2626', gridClass: 'md:col-span-2',
            iconBg: 'bg-red-100 dark:bg-red-900/30', iconColor: 'text-red-600 dark:text-red-400',
            accentBarColor: 'bg-red-500', tagBg: 'bg-red-100 dark:bg-red-900/30', tagText: 'text-red-700 dark:text-red-400',
            hoverBorder: 'hover:border-red-400/50 dark:hover:border-red-500/40',
            component: subjectProfile ? <WarRoom uid={user!.uid} profile={subjectProfile} timetableCompletions={timetableCompletions} /> : null,
        },
        {
            id: 'comeback', title: 'Comeback Engine', description: 'Find your quickest wins and build a comeback plan.', icon: Rocket, needsProfile: true,
            tag: 'Comeback', accentHex: '#f97316', gridClass: 'md:col-span-2',
            iconBg: 'bg-orange-100 dark:bg-orange-900/30', iconColor: 'text-orange-600 dark:text-orange-400',
            accentBarColor: 'bg-orange-500', tagBg: 'bg-orange-100 dark:bg-orange-900/30', tagText: 'text-orange-700 dark:text-orange-400',
            hoverBorder: 'hover:border-orange-400/50 dark:hover:border-orange-500/40',
            component: subjectProfile ? <ComebackEngine uid={user!.uid} profile={subjectProfile} /> : null,
        },
        {
            id: 'future-finder', title: 'Future Finder', description: 'Discover college courses that fit who you are.', icon: Compass, needsProfile: true,
            tag: 'Career Discovery', accentHex: '#6366f1', gridClass: 'md:col-span-2',
            iconBg: 'bg-indigo-100 dark:bg-indigo-900/30', iconColor: 'text-indigo-600 dark:text-indigo-400',
            accentBarColor: 'bg-indigo-500', tagBg: 'bg-indigo-100 dark:bg-indigo-900/30', tagText: 'text-indigo-700 dark:text-indigo-400',
            hoverBorder: 'hover:border-indigo-400/50 dark:hover:border-indigo-500/40',
            component: subjectProfile ? <FutureFinder uid={user!.uid} profile={subjectProfile} /> : null,
        },
        {
            id: 'syllabus-xray', title: 'Syllabus X-Ray', description: 'See where the marks are hiding in your exams.', icon: ScanSearch, needsProfile: false,
            tag: 'Exam Intel', accentHex: '#e11d48', gridClass: 'md:col-span-2',
            iconBg: 'bg-rose-100 dark:bg-rose-900/30', iconColor: 'text-rose-600 dark:text-rose-400',
            accentBarColor: 'bg-rose-500', tagBg: 'bg-rose-100 dark:bg-rose-900/30', tagText: 'text-rose-700 dark:text-rose-400',
            hoverBorder: 'hover:border-rose-400/50 dark:hover:border-rose-500/40',
            component: <SyllabusXRay studentSubjects={subjectProfile?.subjects.map(s => s.subjectName)} uid={user?.uid} />,
        },
        {
            id: 'points-passport', title: 'Points Passport', description: 'Mock trends & grade bargains at a glance.', icon: Map, needsProfile: true,
            tag: 'Tracker', accentHex: '#0ea5e9', gridClass: 'md:col-span-2',
            iconBg: 'bg-sky-100 dark:bg-sky-900/30', iconColor: 'text-sky-600 dark:text-sky-400',
            accentBarColor: 'bg-sky-500', tagBg: 'bg-sky-100 dark:bg-sky-900/30', tagText: 'text-sky-700 dark:text-sky-400',
            hoverBorder: 'hover:border-sky-400/50 dark:hover:border-sky-500/40',
            component: subjectProfile && user ? <PointsPassport uid={user.uid} profile={subjectProfile} /> : null,
        },
    ];

    const [activeFilter, setActiveFilter] = useState<'all' | 'understand' | 'plan' | 'track'>('all');

    const TOOL_CATEGORIES: Record<string, 'understand' | 'plan' | 'track'> = {
        'syllabus-xray': 'understand',
        'cao-simulator': 'understand',
        'future-finder': 'understand',
        'planner': 'plan',
        'war-room': 'plan',
        'comeback': 'plan',
        'points-passport': 'track',
        'journey': 'track',
    };

    const filteredTools = activeFilter === 'all'
        ? tools
        : tools.filter(t => TOOL_CATEGORIES[t.id] === activeFilter);

    const currentTool = tools.find(t => t.id === activeTool);

  return (
    <div className={`min-h-screen bg-zinc-50 dark:bg-zinc-950 transition-colors duration-500 overflow-x-hidden relative flex flex-col items-center pb-36 md:pb-24 ${activeTool === 'journey' || activeTool === 'war-room' ? 'pt-14 md:pt-16' : 'pt-24 md:pt-32'}`}>

      <header className={`fixed top-0 left-0 right-0 z-[60] bg-zinc-50 dark:bg-zinc-950 px-4 py-4 md:px-10 md:py-6 ${activeTool === 'journey' || activeTool === 'war-room' ? '' : 'border-b border-zinc-200 dark:border-zinc-800'}`}>
        <div className="container mx-auto flex items-center justify-between">
          <div className="flex items-center gap-4 md:gap-8">
            <MotionButton whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={activeTool ? () => setActiveTool(null) : onBack} className="p-2.5 rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 transition-colors hover:bg-zinc-100 dark:hover:bg-zinc-800 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[rgba(var(--accent),0.5)]">
              <ArrowLeft size={18} className="text-zinc-900 dark:text-white" />
            </MotionButton>
            <div className="hidden md:block h-10 w-px bg-zinc-200 dark:bg-zinc-800" />
            <div>
              <p className="font-mono text-[9px] font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-[0.25em] mb-1">Explore</p>
              <h1 className="font-serif font-semibold text-lg md:text-2xl tracking-tight text-zinc-900 dark:text-white truncate">The Innovation Zone</h1>
            </div>
          </div>
          <div className="flex items-center gap-3">
            {subjectProfile && (
              <button
                onClick={() => setShowOnboarding(true)}
                className="p-2.5 rounded-lg bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 transition-colors hover:bg-zinc-100 dark:hover:bg-zinc-800"
                title="Edit subjects"
              >
                <Settings size={16} className="text-zinc-500 dark:text-zinc-400" />
              </button>
            )}
          </div>
        </div>
      </header>

      <main className={`flex-grow w-full max-w-4xl relative z-10 ${activeTool === 'journey' || activeTool === 'war-room' ? 'px-6 pt-0' : 'px-6 pt-16'}`}>
         <AnimatePresence mode="wait">
            {!activeTool ? (
                <MotionDiv
                    key="tool-grid"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                >
                    {/* Filter pills */}
                    <div className="mb-8">
                        <div className="flex items-center gap-1 p-1 rounded-xl bg-zinc-100 dark:bg-zinc-800/50 w-fit">
                            {(['all', 'understand', 'plan', 'track'] as const).map(filter => (
                                <button
                                    key={filter}
                                    onClick={() => setActiveFilter(filter)}
                                    className={`px-4 py-2 rounded-lg text-sm transition-all ${
                                        activeFilter === filter
                                            ? 'bg-white dark:bg-zinc-800 text-zinc-900 dark:text-white font-medium shadow-sm'
                                            : 'text-zinc-500 dark:text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-300'
                                    }`}
                                >
                                    {filter === 'all' ? 'All' : filter.charAt(0).toUpperCase() + filter.slice(1)}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Bento card grid */}
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '16px' }}>
                        {filteredTools.map((tool, i) => {
                            const Icon = tool.icon;
                            const disabled = (tool.needsProfile && !profileLoaded) || (tool.needsProfile && !subjectProfile);
                            const gcRecommended = gcRecommendations[tool.id];

                            return (
                                <MotionDiv
                                    key={tool.id}
                                    initial={{ opacity: 0, y: 16 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    transition={{ duration: 0.3, delay: i * 0.04 }}
                                    onClick={disabled ? undefined : () => handleToolClick(tool.id, tool.needsProfile)}
                                    className={`flex flex-col rounded-xl border overflow-hidden transition-all ${
                                        disabled
                                            ? 'border-zinc-200/60 dark:border-zinc-800/40 cursor-not-allowed'
                                            : 'border-zinc-200/60 dark:border-zinc-800/40 hover:border-zinc-300 dark:hover:border-zinc-700 hover:shadow-md cursor-pointer'
                                    } bg-white dark:bg-zinc-900`}
                                >
                                    <div className="p-6 flex-1 flex flex-col">
                                        {/* Icon in colored circle */}
                                        <div className={`w-10 h-10 rounded-full flex items-center justify-center mb-4 ${
                                            disabled ? 'bg-zinc-100 dark:bg-zinc-800' : tool.iconBg
                                        }`}>
                                            {disabled
                                                ? <Lock size={18} className="text-zinc-400 dark:text-zinc-600" />
                                                : <Icon size={18} className={tool.iconColor} />
                                            }
                                        </div>

                                        {/* Category label */}
                                        <p className={`text-[10px] font-bold uppercase tracking-widest mb-1.5 ${
                                            disabled ? 'text-zinc-300 dark:text-zinc-600' : 'text-zinc-400 dark:text-zinc-500'
                                        }`}>
                                            {disabled ? 'Needs Profile' : tool.tag}
                                        </p>

                                        {/* Title */}
                                        <h3 className={`text-base font-semibold mb-1.5 ${
                                            disabled ? 'text-zinc-300 dark:text-zinc-600' : 'text-zinc-900 dark:text-white'
                                        }`}>
                                            {tool.title}
                                        </h3>

                                        {/* Description */}
                                        <p className={`text-xs leading-relaxed flex-1 ${
                                            disabled ? 'text-zinc-300 dark:text-zinc-600' : 'text-zinc-500 dark:text-zinc-400'
                                        }`}>
                                            {disabled ? 'Complete your Subject Profile to unlock.' : tool.description}
                                        </p>

                                        {/* GC recommendation badge if present */}
                                        {gcRecommended && !disabled && (
                                            <div className="mt-3 px-3 py-2 rounded-lg bg-indigo-50 dark:bg-indigo-900/20 border border-indigo-200/60 dark:border-indigo-800/40">
                                                <p className="text-[11px] font-semibold text-indigo-600 dark:text-indigo-400">
                                                    Recommended by {gcRecommended.fromName || 'your counsellor'}
                                                </p>
                                            </div>
                                        )}
                                    </div>

                                    {/* Bottom section with divider */}
                                    {!disabled && (
                                        <div className="px-6 py-3 border-t border-zinc-100 dark:border-zinc-800/60">
                                            <span className="text-xs font-medium text-zinc-400 dark:text-zinc-500">
                                                Launch tool
                                            </span>
                                        </div>
                                    )}
                                </MotionDiv>
                            );
                        })}
                    </div>
                </MotionDiv>
            ) : (
                <MotionDiv
                    key="active-tool"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                >
                    {currentTool?.component}
                </MotionDiv>
            )}
        </AnimatePresence>
      </main>

      {/* Subject Onboarding Modal */}
      <AnimatePresence>
        {showOnboarding && user && (
          <SubjectOnboarding
            user={user}
            existingProfile={subjectProfile || undefined}
            onComplete={handleOnboardingComplete}
            onClose={() => { setShowOnboarding(false); setPendingToolId(null); }}
          />
        )}
      </AnimatePresence>

      {/* Reflection Modal — kept for backwards compat but no longer triggered */}

      {/* Study Journal Modal */}
      <StudyJournalModal
        isOpen={showJournal}
        onClose={() => setShowJournal(false)}
        reflections={reflections}
      />

      {/* Reward Shop Modal */}
      <RewardShopModal
        isOpen={showRewardShop}
        onClose={() => setShowRewardShop(false)}
        pointsBalance={pointsData.totalEarned - pointsData.totalSpent}
        cosmeticUnlocks={cosmeticUnlocks}
        earnedRest={earnedRest}
        onSpend={handleSpendPoints}
        skippableBlocks={skippableBlocks}
        settings={settings}
        updateSetting={updateSetting}
      />

      {/* Points Explainer (first visit) */}
      <AnimatePresence>
        {showPointsExplainer && (
          <MotionDiv
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-[100] p-4"
            onClick={dismissPointsExplainer}
          >
            <MotionDiv
              initial={{ scale: 0.92, opacity: 0, y: 20 }}
              animate={{ scale: 1, opacity: 1, y: 0 }}
              exit={{ scale: 0.92, opacity: 0, y: 20 }}
              transition={{ duration: 0.35, ease: [0.16, 1, 0.3, 1] }}
              className="bg-white dark:bg-zinc-900 rounded-2xl max-w-sm w-full shadow-2xl border border-zinc-200 dark:border-zinc-800 overflow-hidden"
              onClick={(e: React.MouseEvent) => e.stopPropagation()}
            >
              <div className="h-1.5 bg-gradient-to-r from-amber-400 via-[var(--accent-hex)] to-purple-500" />

              <div className="p-6">
                <div className="flex items-center gap-3 mb-5">
                  <div className="w-10 h-10 rounded-xl bg-amber-100 dark:bg-amber-900/30 flex items-center justify-center">
                    <Zap size={20} className="text-amber-500" />
                  </div>
                  <div>
                    <h3 className="font-serif font-semibold text-lg text-zinc-900 dark:text-white">How Points Work</h3>
                    <p className="text-xs text-zinc-400 dark:text-zinc-500">Earn & spend in the Innovation Zone</p>
                  </div>
                </div>

                <div className="space-y-2.5 mb-4">
                  <div className="flex items-start gap-3 p-3 rounded-xl bg-zinc-50 dark:bg-white/[0.04]">
                    <div className="w-8 h-8 rounded-lg bg-teal-100 dark:bg-teal-900/30 flex items-center justify-center shrink-0 mt-0.5">
                      <Clock size={14} className="text-teal-600 dark:text-teal-400" />
                    </div>
                    <div>
                      <p className="text-sm font-medium text-zinc-800 dark:text-zinc-200">Study Sessions</p>
                      <p className="text-xs text-zinc-500 dark:text-zinc-400">10 pts per completed timetable session</p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3 p-3 rounded-xl bg-zinc-50 dark:bg-white/[0.04]">
                    <div className="w-8 h-8 rounded-lg bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center shrink-0 mt-0.5">
                      <BookMarked size={14} className="text-purple-600 dark:text-purple-400" />
                    </div>
                    <div>
                      <p className="text-sm font-medium text-zinc-800 dark:text-zinc-200">Reflections</p>
                      <p className="text-xs text-zinc-500 dark:text-zinc-400">Bonus points for thoughtful study reflections</p>
                    </div>
                  </div>
                </div>

                {/* Streak Explainer */}
                <div className="mb-4 p-3 rounded-xl bg-gradient-to-r from-amber-50 to-orange-50 dark:from-amber-950/20 dark:to-orange-950/20 border border-amber-200/50 dark:border-amber-800/30">
                  <div className="flex items-center gap-2 mb-2">
                    <Flame size={14} className="text-amber-500" />
                    <p className="text-sm font-semibold text-zinc-800 dark:text-zinc-200">Streak Multiplier</p>
                  </div>
                  <p className="text-xs text-zinc-500 dark:text-zinc-400 mb-2">Complete your timetable sessions on consecutive days to build a streak and multiply your points.</p>
                  <div className="grid grid-cols-3 gap-1.5">
                    <div className="text-center p-1.5 rounded-lg bg-white/60 dark:bg-white/[0.04]">
                      <p className="text-[10px] font-bold text-amber-600 dark:text-amber-400">3+ days</p>
                      <p className="text-[10px] text-zinc-500 dark:text-zinc-400">1.5x pts</p>
                    </div>
                    <div className="text-center p-1.5 rounded-lg bg-white/60 dark:bg-white/[0.04]">
                      <p className="text-[10px] font-bold text-orange-600 dark:text-orange-400">7+ days</p>
                      <p className="text-[10px] text-zinc-500 dark:text-zinc-400">2x pts</p>
                    </div>
                    <div className="text-center p-1.5 rounded-lg bg-white/60 dark:bg-white/[0.04]">
                      <p className="text-[10px] font-bold text-red-600 dark:text-red-400">14+ days</p>
                      <p className="text-[10px] text-zinc-500 dark:text-zinc-400">2.5x pts</p>
                    </div>
                  </div>
                </div>

                <p className="text-xs text-zinc-400 dark:text-zinc-500 text-center mb-4">
                  Spend points in the <span className="font-semibold text-zinc-600 dark:text-zinc-300">Reward Shop</span> on avatars, themes & card styles.
                </p>

                <button
                  onClick={dismissPointsExplainer}
                  className="w-full py-2.5 rounded-xl bg-[var(--accent-hex)] hover:bg-[var(--accent-dark-hex)] text-white font-semibold text-sm transition-colors"
                >
                  Got it!
                </button>
              </div>
            </MotionDiv>
          </MotionDiv>
        )}
      </AnimatePresence>
    </div>
  );
};
export default InnovationZone;
