
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    ArrowLeft, Lightbulb, Zap, Clock, Shield, Wrench, RotateCcw,
    TrendingUp, Users, BookOpen, GitBranch, ChevronDown, ChevronUp, BookMarked
} from 'lucide-react';
import {
    type GameState, type Choice, type Scene, type HistoryItem, type StatKey, type Phase,
    STORY_DATA, ROUTE_RESOLVERS, INITIAL_GAME_STATE, PHASE_METADATA,
    ARCHETYPES, STAT_TO_MODULES, STAT_LABELS, STAT_COLORS, STAT_BG_COLORS,
    getStatGrade, getKeyTurningPoints, getWeakestStat,
} from './journeySimulatorData';

const MotionDiv = motion.div as any;
const MotionButton = motion.button as any;

interface InnovationZoneProps {
  onBack: () => void;
}

const STAT_ICONS: Record<StatKey, React.ElementType> = {
    energy: Zap,
    academicCap: TrendingUp,
    socialSupport: Users,
    systemSavvy: BookOpen,
    resilience: Shield,
};

// ─── StatBar ─────────────────────────────────────────────────────────────────

const StatBar = ({ icon: Icon, label, value, color }: { icon: React.ElementType; label: string; value: number; color: string }) => (
    <div>
        <div className="flex items-center gap-2">
            <Icon size={16} className={color}/>
            <p className="text-xs font-bold uppercase tracking-wider text-zinc-500 dark:text-zinc-400">{label}</p>
        </div>
        <div className="w-full bg-zinc-200 dark:bg-white/10 rounded-full h-2.5 mt-1">
            <MotionDiv
                className={`h-2.5 rounded-full ${color.replace('text-', 'bg-')}`}
                initial={{ width: '0%' }}
                animate={{ width: `${value}%` }}
            />
        </div>
    </div>
);

// ─── ChoiceFeedback ──────────────────────────────────────────────────────────

type FeedbackState = {
    effects: Partial<GameState>;
    moduleLink?: Choice['moduleLink'];
};

const ChoiceFeedback: React.FC<{ feedback: FeedbackState; onComplete: () => void }> = ({ feedback, onComplete }) => {
    return (
        <MotionDiv
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.3 }}
            onClick={onComplete}
            className="fixed inset-0 z-[100] flex items-center justify-center bg-black/40 backdrop-blur-sm cursor-pointer"
        >
            <MotionDiv
                initial={{ opacity: 0, scale: 0.9, y: 20 }}
                animate={{ opacity: 1, scale: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.9, y: -20 }}
                transition={{ duration: 0.3, ease: 'easeOut' }}
                className="bg-white dark:bg-zinc-900 rounded-2xl p-6 max-w-sm w-full mx-4 shadow-2xl border border-zinc-200 dark:border-white/10"
            >
                <div className="flex flex-wrap items-center justify-center gap-4 mb-4">
                    {Object.entries(feedback.effects).map(([stat, value], index) => {
                        const Icon = STAT_ICONS[stat as StatKey];
                        const isPositive = (value as number) >= 0;
                        return (
                            <MotionDiv
                                key={stat}
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: index * 0.1 }}
                                className="flex items-center gap-1.5"
                            >
                                <Icon size={16} className={isPositive ? 'text-emerald-500' : 'text-rose-500'} />
                                <span className={`font-mono text-sm font-bold ${isPositive ? 'text-emerald-500' : 'text-rose-500'}`}>
                                    {isPositive ? '+' : ''}{value}
                                </span>
                            </MotionDiv>
                        );
                    })}
                </div>

                {feedback.moduleLink && (
                    <MotionDiv
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.3 }}
                        className="bg-purple-50 dark:bg-purple-900/20 border border-purple-200 dark:border-purple-700/30 rounded-xl p-4"
                    >
                        <div className="flex items-center gap-2 mb-2">
                            <BookMarked size={14} className="text-purple-600 dark:text-purple-400" />
                            <p className="text-xs font-bold text-purple-600 dark:text-purple-400">{feedback.moduleLink.moduleTitle}</p>
                        </div>
                        <p className="text-xs text-purple-700 dark:text-purple-300 leading-relaxed">{feedback.moduleLink.insight}</p>
                    </MotionDiv>
                )}

                <p className="text-center text-[10px] text-zinc-400 dark:text-zinc-500 mt-3">Click anywhere to continue</p>
            </MotionDiv>
        </MotionDiv>
    );
};

// ─── PhaseTransition ─────────────────────────────────────────────────────────

const PhaseTransition: React.FC<{ phase: Phase; gameState: GameState; onComplete: () => void }> = ({ phase, gameState, onComplete }) => {
    useEffect(() => {
        const timer = setTimeout(onComplete, 4000);
        return () => clearTimeout(timer);
    }, [onComplete]);

    const meta = PHASE_METADATA.find(p => p.name === phase);

    return (
        <MotionDiv
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.5 }}
            onClick={onComplete}
            className="cursor-pointer"
        >
            <div className="bg-white/50 dark:bg-white/5 backdrop-blur-2xl border border-zinc-200/50 dark:border-white/10 rounded-xl p-10 text-center">
                <MotionDiv
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                >
                    <p className="text-xs font-bold uppercase tracking-[0.3em] text-purple-600 dark:text-purple-400 mb-2">
                        {meta?.months}
                    </p>
                    <h2 className="font-serif text-4xl font-semibold text-zinc-900 dark:text-white mb-3">
                        {phase}
                    </h2>
                    <p className="text-zinc-500 dark:text-zinc-400 max-w-md mx-auto mb-8">
                        {meta?.subtitle}
                    </p>
                </MotionDiv>

                <MotionDiv
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.5 }}
                    className="grid grid-cols-5 gap-3 max-w-lg mx-auto"
                >
                    {(Object.keys(gameState) as StatKey[]).map(stat => {
                        const Icon = STAT_ICONS[stat];
                        return (
                            <div key={stat} className="text-center">
                                <Icon size={16} className={`${STAT_COLORS[stat]} mx-auto mb-1`} />
                                <div className="w-full bg-zinc-200 dark:bg-white/10 rounded-full h-1.5">
                                    <div className={`h-1.5 rounded-full ${STAT_BG_COLORS[stat]}`} style={{ width: `${gameState[stat]}%` }} />
                                </div>
                                <p className="text-[10px] font-bold text-zinc-400 dark:text-zinc-500 mt-1">{gameState[stat]}</p>
                            </div>
                        );
                    })}
                </MotionDiv>

                <MotionDiv
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 1 }}
                    className="mt-6"
                >
                    <p className="text-[10px] text-zinc-400 dark:text-zinc-500">Click to continue</p>
                </MotionDiv>
            </div>
        </MotionDiv>
    );
};

// ─── Phase Colors (literal strings for Tailwind CDN) ─────────────────────────

const PHASE_TREE_COLORS: Record<Phase, { dot: string; line: string; label: string; labelBg: string }> = {
    'Foundation': { dot: 'bg-blue-500', line: 'bg-blue-200 dark:bg-blue-800', label: 'text-blue-700 dark:text-blue-300', labelBg: 'bg-blue-100 dark:bg-blue-900/30' },
    'Pressure Cooker': { dot: 'bg-amber-500', line: 'bg-amber-200 dark:bg-amber-800', label: 'text-amber-700 dark:text-amber-300', labelBg: 'bg-amber-100 dark:bg-amber-900/30' },
    'Final Stretch': { dot: 'bg-rose-500', line: 'bg-rose-200 dark:bg-rose-800', label: 'text-rose-700 dark:text-rose-300', labelBg: 'bg-rose-100 dark:bg-rose-900/30' },
};

// ─── ReportCard ──────────────────────────────────────────────────────────────

const ReportCard: React.FC<{ endingId: string; gameState: GameState; history: HistoryItem[]; onRestart: () => void }> = ({ endingId, gameState, history, onRestart }) => {
    const [showLog, setShowLog] = useState(false);
    const archetype = ARCHETYPES[endingId];
    const endScene = STORY_DATA[endingId];
    const turningPoints = getKeyTurningPoints(history);
    const weakestStat = getWeakestStat(gameState);
    const recommendedModules = STAT_TO_MODULES[weakestStat];

    // Compute branching path tree data
    const pathNodes = history.map((item) => {
        const choices = item.scene.choices || [];
        const chosenChoice = choices.find(c => c.text === item.choiceText);
        const chosenNext = chosenChoice?.nextSceneId;
        const branches: string[] = [];
        for (const alt of choices) {
            if (alt.text !== item.choiceText && alt.nextSceneId !== chosenNext) {
                if (alt.nextSceneId.startsWith('__')) continue;
                const altScene = STORY_DATA[alt.nextSceneId];
                if (altScene) branches.push(altScene.title);
            }
        }
        return { title: item.scene.title, phase: item.scene.phase, branches };
    });

    const phases: Phase[] = ['Foundation', 'Pressure Cooker', 'Final Stretch'];
    const groupedPath = phases
        .map(phase => ({ phase, nodes: pathNodes.filter(n => n.phase === phase) }))
        .filter(g => g.nodes.length > 0);

    return (
        <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
            {/* A. Archetype Badge */}
            <div className={`${archetype?.accentBg || 'bg-zinc-100 dark:bg-white/5'} rounded-2xl p-8 text-center border border-zinc-200/50 dark:border-white/10`}>
                <div className="text-5xl mb-4">{archetype?.icon || '🎓'}</div>
                <h3 className={`font-serif text-3xl font-semibold mb-3 ${archetype?.accentColor || 'text-zinc-900 dark:text-white'}`}>
                    {endScene?.title || 'Results Day'}
                </h3>
                <p className="text-zinc-600 dark:text-zinc-300 leading-relaxed max-w-lg mx-auto">
                    {archetype?.description || endScene?.text}
                </p>
            </div>

            {/* B. Stat Letter Grades */}
            <div>
                <h4 className="font-bold text-sm uppercase tracking-widest text-zinc-500 dark:text-zinc-400 mb-3 text-center">Your Grades</h4>
                <div className="grid grid-cols-5 gap-3">
                    {(Object.keys(gameState) as StatKey[]).map(stat => {
                        const grade = getStatGrade(gameState[stat]);
                        const Icon = STAT_ICONS[stat];
                        return (
                            <div key={stat} className="bg-white/50 dark:bg-white/5 border border-zinc-200 dark:border-white/10 rounded-xl p-3 text-center">
                                <Icon size={16} className={`${STAT_COLORS[stat]} mx-auto mb-1`} />
                                <p className={`font-serif text-2xl font-bold ${grade.color}`}>{grade.letter}</p>
                                <p className="text-[10px] font-bold text-zinc-400 dark:text-zinc-500 mt-0.5">{STAT_LABELS[stat]}</p>
                            </div>
                        );
                    })}
                </div>
            </div>

            {/* C. Key Turning Points */}
            {turningPoints.length > 0 && (
                <div>
                    <h4 className="font-bold text-sm uppercase tracking-widest text-zinc-500 dark:text-zinc-400 mb-3 text-center">Key Turning Points</h4>
                    <div className="space-y-2">
                        {turningPoints.map((item, index) => (
                            <div key={index} className="bg-white/50 dark:bg-white/5 border border-zinc-200 dark:border-white/10 rounded-xl p-4">
                                <div className="flex items-center gap-2 mb-1">
                                    <p className="text-xs font-bold text-purple-600 dark:text-purple-400">{item.scene.month}</p>
                                    <span className="text-zinc-300 dark:text-zinc-600">|</span>
                                    <p className="text-xs font-bold text-zinc-700 dark:text-zinc-300">{item.scene.title}</p>
                                </div>
                                <p className="text-sm text-zinc-600 dark:text-zinc-400">{item.choiceText}</p>
                                <div className="flex items-center gap-3 mt-2">
                                    {Object.entries(item.effects).map(([stat, value]) => {
                                        const Icon = STAT_ICONS[stat as StatKey];
                                        const isPositive = (value as number) >= 0;
                                        return (
                                            <div key={stat} className="flex items-center gap-1">
                                                <Icon size={12} className={isPositive ? 'text-emerald-500' : 'text-rose-500'} />
                                                <span className={`font-mono text-xs font-bold ${isPositive ? 'text-emerald-500' : 'text-rose-500'}`}>
                                                    {isPositive ? '+' : ''}{value}
                                                </span>
                                            </div>
                                        );
                                    })}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* D. Recommended Modules */}
            <div>
                <h4 className="font-bold text-sm uppercase tracking-widest text-zinc-500 dark:text-zinc-400 mb-1 text-center">Recommended For You</h4>
                <p className="text-xs text-zinc-400 dark:text-zinc-500 text-center mb-3">Based on your weakest area: {STAT_LABELS[weakestStat]}</p>
                <div className="space-y-2">
                    {recommendedModules.map(mod => (
                        <div key={mod.moduleId} className="flex items-center gap-3 bg-purple-50 dark:bg-purple-900/20 border border-purple-200 dark:border-purple-700/30 rounded-xl p-3">
                            <BookMarked size={16} className="text-purple-600 dark:text-purple-400 flex-shrink-0" />
                            <p className="text-sm font-semibold text-purple-700 dark:text-purple-300">{mod.moduleTitle}</p>
                        </div>
                    ))}
                </div>
            </div>

            {/* E. Branching Path Tree */}
            <div>
                <h4 className="font-bold text-sm uppercase tracking-widest text-zinc-500 dark:text-zinc-400 mb-3 text-center">Your Path</h4>
                <div className="bg-white/50 dark:bg-white/5 border border-zinc-200 dark:border-white/10 rounded-xl p-5 overflow-x-auto">
                    {groupedPath.map((group, gi) => {
                        const colors = PHASE_TREE_COLORS[group.phase];
                        return (
                            <div key={group.phase} className={gi > 0 ? 'mt-4' : ''}>
                                <div className={`inline-block px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider mb-3 ${colors.label} ${colors.labelBg}`}>
                                    {group.phase}
                                </div>
                                {group.nodes.map((node, ni) => {
                                    const isLastInGroup = ni === group.nodes.length - 1;
                                    const isLastOverall = gi === groupedPath.length - 1 && isLastInGroup;
                                    return (
                                        <div key={ni} className="flex items-stretch">
                                            {/* Dot + line */}
                                            <div className="flex flex-col items-center mr-3 flex-shrink-0" style={{ width: 12 }}>
                                                <div className={`w-2.5 h-2.5 rounded-full flex-shrink-0 ${colors.dot}`} />
                                                {!isLastOverall && <div className={`w-px flex-grow ${isLastInGroup ? 'bg-zinc-200 dark:bg-zinc-700' : colors.line}`} />}
                                            </div>
                                            {/* Label + branches */}
                                            <div className={`${isLastOverall ? '' : 'pb-2'} min-w-0`}>
                                                <p className="text-xs font-semibold text-zinc-700 dark:text-zinc-300 leading-tight">{node.title}</p>
                                                {node.branches.map((branch, bi) => (
                                                    <div key={bi} className="flex items-center gap-1.5 mt-1 ml-1">
                                                        <div className="w-4 border-t border-dashed border-zinc-300 dark:border-zinc-600 flex-shrink-0" />
                                                        <div className="w-1.5 h-1.5 rounded-full bg-zinc-300 dark:bg-zinc-600 flex-shrink-0" />
                                                        <p className="text-[10px] text-zinc-400 dark:text-zinc-500 italic truncate">{branch}</p>
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    );
                                })}
                            </div>
                        );
                    })}
                    {/* End node */}
                    <div className="flex items-center mt-3 pt-3 border-t border-zinc-200 dark:border-white/10">
                        <div className="flex-shrink-0 mr-3 text-center" style={{ width: 12 }}>
                            <span className="text-sm">{archetype?.icon || '🎓'}</span>
                        </div>
                        <p className={`text-xs font-bold ${archetype?.accentColor || 'text-zinc-700 dark:text-zinc-300'}`}>
                            {endScene?.title || 'Results Day'}
                        </p>
                    </div>
                </div>
            </div>

            {/* F. Collapsible Journey Log */}
            <div>
                <button
                    onClick={() => setShowLog(!showLog)}
                    className="w-full flex items-center justify-center gap-2 text-sm font-bold text-zinc-500 dark:text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-200 transition-colors py-2"
                >
                    {showLog ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    {showLog ? 'Hide' : 'Show'} Full Journey Log ({history.length} decisions)
                </button>
                {showLog && (
                    <MotionDiv
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        className="overflow-hidden"
                    >
                        <div className="text-left space-y-4 max-h-96 overflow-y-auto p-4 bg-zinc-100 dark:bg-white/5 rounded-xl border border-zinc-200 dark:border-white/10 mt-2">
                            {history.map((item, index) => (
                                <div key={index} className="relative pl-8">
                                    <div className="absolute top-1 left-0 flex flex-col items-center">
                                        <div className="w-6 h-6 rounded-full bg-purple-200 dark:bg-purple-800 flex items-center justify-center ring-4 ring-zinc-100 dark:ring-white/5">
                                            <GitBranch size={14} className="text-purple-600 dark:text-purple-300"/>
                                        </div>
                                        {index < history.length - 1 && <div className="w-px h-full bg-zinc-300 dark:bg-zinc-700 mt-1" style={{height: 'calc(100% + 1rem)'}} />}
                                    </div>
                                    <p className="font-bold text-sm text-zinc-800 dark:text-zinc-200">{item.scene.month}: {item.scene.title}</p>
                                    <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-1">{item.choiceText}</p>
                                    <div className="flex items-center gap-2 mt-1">
                                        {Object.entries(item.effects).map(([stat, value]) => {
                                            const Icon = STAT_ICONS[stat as StatKey];
                                            const isPositive = (value as number) >= 0;
                                            return (
                                                <div key={stat} className="flex items-center gap-0.5">
                                                    <Icon size={10} className={isPositive ? 'text-emerald-500' : 'text-rose-500'} />
                                                    <span className={`font-mono text-[10px] font-bold ${isPositive ? 'text-emerald-500' : 'text-rose-500'}`}>
                                                        {isPositive ? '+' : ''}{value}
                                                    </span>
                                                </div>
                                            );
                                        })}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </MotionDiv>
                )}
            </div>

            {/* Play Again */}
            <div className="text-center">
                <MotionButton
                    onClick={onRestart}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="inline-flex items-center gap-2 px-6 py-3 bg-zinc-800 dark:bg-white text-white dark:text-zinc-900 font-bold text-sm rounded-full shadow-lg hover:bg-purple-600 dark:hover:bg-purple-400 transition-colors"
                >
                    Play Again <RotateCcw size={16} />
                </MotionButton>
            </div>
        </MotionDiv>
    );
};

// ─── AcademicJourneyGame ─────────────────────────────────────────────────────

const AcademicJourneyGame: React.FC = () => {
    const [gameState, setGameState] = useState<GameState>({ ...INITIAL_GAME_STATE });
    const [currentSceneId, setCurrentSceneId] = useState('START');
    const [history, setHistory] = useState<HistoryItem[]>([]);
    const [currentPhase, setCurrentPhase] = useState<Phase>('Foundation');
    const [showPhaseTransition, setShowPhaseTransition] = useState(false);
    const [pendingSceneId, setPendingSceneId] = useState<string | null>(null);
    const [feedbackState, setFeedbackState] = useState<FeedbackState | null>(null);

    const currentScene = STORY_DATA[currentSceneId];
    const isEndScene = currentSceneId.startsWith('END_');

    const advanceToScene = useCallback((sceneId: string, newState: GameState) => {
        const targetScene = STORY_DATA[sceneId];
        if (targetScene && targetScene.phase !== currentPhase) {
            setShowPhaseTransition(true);
            setCurrentPhase(targetScene.phase);
            setPendingSceneId(sceneId);
        } else {
            setCurrentSceneId(sceneId);
        }
    }, [currentPhase]);

    const handleChoice = useCallback((choice: Choice) => {
        const currentChoiceScene = STORY_DATA[currentSceneId];
        const newGameState = { ...gameState };

        for (const [key, value] of Object.entries(choice.effects)) {
            newGameState[key as StatKey] = Math.max(0, Math.min(100, newGameState[key as StatKey] + value));
        }

        setHistory(prev => [...prev, {
            scene: currentChoiceScene,
            choiceText: choice.text,
            effects: choice.effects,
            moduleLink: choice.moduleLink,
        }]);
        setGameState(newGameState);

        // Resolve route if it's an invisible logic gate
        let targetSceneId = choice.nextSceneId;
        if (targetSceneId.startsWith('__') && ROUTE_RESOLVERS[targetSceneId]) {
            targetSceneId = ROUTE_RESOLVERS[targetSceneId](newGameState);
        }

        // Show feedback overlay, then advance
        setFeedbackState({ effects: choice.effects, moduleLink: choice.moduleLink });
        setPendingSceneId(targetSceneId);
    }, [currentSceneId, gameState]);

    const handleFeedbackComplete = useCallback(() => {
        setFeedbackState(null);
        if (pendingSceneId) {
            const targetScene = STORY_DATA[pendingSceneId];
            if (targetScene && targetScene.phase !== currentPhase) {
                setShowPhaseTransition(true);
                setCurrentPhase(targetScene.phase);
                // pendingSceneId stays set for after phase transition
            } else {
                setCurrentSceneId(pendingSceneId);
                setPendingSceneId(null);
            }
        }
    }, [pendingSceneId, currentPhase]);

    const handlePhaseTransitionComplete = useCallback(() => {
        setShowPhaseTransition(false);
        if (pendingSceneId) {
            setCurrentSceneId(pendingSceneId);
            setPendingSceneId(null);
        }
    }, [pendingSceneId]);

    const restartGame = useCallback(() => {
        setGameState({ ...INITIAL_GAME_STATE });
        setCurrentSceneId('START');
        setHistory([]);
        setCurrentPhase('Foundation');
        setShowPhaseTransition(false);
        setPendingSceneId(null);
        setFeedbackState(null);
    }, []);

    // End screen
    if (isEndScene) {
        return (
            <div className="bg-white/50 dark:bg-white/5 backdrop-blur-2xl border border-zinc-200/50 dark:border-white/10 rounded-xl p-8">
                <ReportCard endingId={currentSceneId} gameState={gameState} history={history} onRestart={restartGame} />
            </div>
        );
    }

    // Phase transition interstitial
    if (showPhaseTransition) {
        return (
            <AnimatePresence mode="wait">
                <PhaseTransition key={currentPhase} phase={currentPhase} gameState={gameState} onComplete={handlePhaseTransitionComplete} />
            </AnimatePresence>
        );
    }

    if (!currentScene || !currentScene.choices) {
        return null;
    }

    return (
        <>
            <div className="bg-white/50 dark:bg-white/5 backdrop-blur-2xl border border-zinc-200/50 dark:border-white/10 rounded-xl p-8">
                <AnimatePresence mode="wait">
                    <MotionDiv
                        key={currentSceneId}
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: -20 }}
                        transition={{ duration: 0.4, ease: 'easeInOut' }}
                    >
                        <div className="border-b border-zinc-200 dark:border-white/10 pb-4 mb-6">
                            <p className="text-xs font-bold uppercase tracking-widest text-purple-600 dark:text-purple-400">{currentScene.phase} - {currentScene.month}</p>
                            <h3 className="font-serif text-3xl font-semibold text-zinc-900 dark:text-white">{currentScene.title}</h3>
                        </div>

                        <p className="text-zinc-600 dark:text-zinc-300 leading-relaxed mb-8">{currentScene.text}</p>

                        <div className="space-y-3 mb-8">
                            {currentScene.choices.map((choice, index) => (
                                <MotionButton
                                    key={index}
                                    onClick={() => handleChoice(choice)}
                                    whileHover={{ scale: 1.02 }}
                                    whileTap={{ scale: 0.98 }}
                                    className="w-full text-left p-4 rounded-xl bg-zinc-100 dark:bg-white/5 border border-zinc-200 dark:border-white/10 hover:bg-zinc-200 dark:hover:bg-white/10 transition-colors font-semibold text-zinc-700 dark:text-zinc-200"
                                >
                                    {choice.text}
                                </MotionButton>
                            ))}
                        </div>

                        <div>
                            <h4 className="font-bold text-sm uppercase tracking-widest text-zinc-500 dark:text-zinc-400 mb-4 text-center">Life Dashboard</h4>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <StatBar icon={Zap} label="Energy" value={gameState.energy} color="text-amber-500" />
                                <StatBar icon={TrendingUp} label="Academic Mastery" value={gameState.academicCap} color="text-blue-500" />
                                <StatBar icon={Users} label="Social Support" value={gameState.socialSupport} color="text-emerald-500" />
                                <StatBar icon={BookOpen} label="System Savvy" value={gameState.systemSavvy} color="text-purple-500" />
                                <StatBar icon={Shield} label="Resilience" value={gameState.resilience} color="text-rose-500" />
                            </div>
                        </div>
                    </MotionDiv>
                </AnimatePresence>
            </div>

            {/* Choice Feedback Overlay */}
            <AnimatePresence>
                {feedbackState && (
                    <ChoiceFeedback feedback={feedbackState} onComplete={handleFeedbackComplete} />
                )}
            </AnimatePresence>
        </>
    );
};

// ─── ToolCard ────────────────────────────────────────────────────────────────

const ToolCard: React.FC<{title: string, description: string, icon: React.ElementType, onClick: () => void, disabled?: boolean, accentColor?: string}> =
({ title, description, icon: Icon, onClick, disabled = false, accentColor = 'text-purple-500' }) => (
    <MotionButton
        onClick={onClick}
        disabled={disabled}
        whileHover={{ scale: disabled ? 1 : 1.03 }}
        className={`w-full text-left p-6 rounded-2xl border-2 transition-all ${disabled ? 'bg-zinc-50 dark:bg-white/5 border-zinc-200 dark:border-white/10 opacity-50 cursor-not-allowed' : 'bg-white/50 dark:bg-white/10 border-zinc-200/80 dark:border-white/15 hover:border-purple-300 dark:hover:border-purple-500/50 cursor-pointer'}`}
    >
        <div className="flex items-center gap-4">
            <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${disabled ? 'bg-zinc-200 dark:bg-white/10' : 'bg-purple-100 dark:bg-purple-900/50'}`}>
                <Icon size={24} className={disabled ? 'text-zinc-400 dark:text-zinc-600' : accentColor} />
            </div>
            <div>
                <h3 className="font-bold text-zinc-800 dark:text-white">{title}</h3>
                <p className="text-xs text-zinc-500 dark:text-zinc-400">{disabled ? "Coming Soon..." : description}</p>
            </div>
        </div>
    </MotionButton>
);

// ─── InnovationZone ──────────────────────────────────────────────────────────

const InnovationZone: React.FC<InnovationZoneProps> = ({ onBack }) => {
    const [activeTool, setActiveTool] = useState<string | null>(null);

    const tools = [
        { id: 'journey', title: 'Academic Journey Simulator', description: 'Navigate the choices of your final school year.', icon: GitBranch, component: <AcademicJourneyGame /> },
        { id: 'focus', title: 'Deep Focus Timer', description: 'A customizable timer based on the Pomodoro technique.', icon: Clock, disabled: true },
        { id: 'planner', title: 'Retrospective Timetable', description: 'A data-driven study planner based on your confidence.', icon: Wrench, disabled: true }
    ];

    const currentTool = tools.find(t => t.id === activeTool);

  return (
    <div className="min-h-screen bg-white dark:bg-zinc-950 transition-colors duration-500 overflow-x-hidden relative flex flex-col items-center pt-32 pb-24">

      <header className="fixed top-0 left-0 right-0 z-[60] bg-white/60 dark:bg-zinc-950/60 backdrop-blur-2xl border-b border-zinc-200/50 dark:border-white/5 px-10 py-6">
        <div className="container mx-auto flex items-center justify-between">
          <div className="flex items-center gap-8">
            <MotionButton whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={onBack} className="tactile-button p-3 rounded-full bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 transition-all">
              <ArrowLeft size={18} className="text-zinc-900 dark:text-white" />
            </MotionButton>
            <div className="h-10 w-px bg-zinc-200/50 dark:bg-zinc-700" />
            <div>
              <p className="font-mono text-[9px] font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-[0.25em] mb-1">Explore</p>
              <h1 className="font-serif font-semibold text-2xl tracking-tight text-zinc-900 dark:text-white">The Innovation Zone</h1>
            </div>
          </div>
          <div className="w-14 h-14 bg-purple-500 dark:bg-purple-400 rounded-2xl flex items-center justify-center text-white shadow-2xl rotate-3">
            <Lightbulb size={24} strokeWidth={1.5} />
          </div>
        </div>
      </header>

      <main className="flex-grow w-full max-w-4xl px-6 pt-16 relative z-10">
         <AnimatePresence mode="wait">
            {!activeTool ? (
                <MotionDiv
                    key="tool-grid"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                >
                    <div className="text-center mb-12">
                        <h2 className="font-serif text-5xl font-semibold text-zinc-900 dark:text-white">Experimental Tools</h2>
                        <p className="max-w-xl mx-auto mt-4 text-zinc-500 dark:text-zinc-400">A collection of interactive simulations and utilities designed to help you master the key concepts from the Learning Lab.</p>
                    </div>
                    <div className="space-y-4">
                        {tools.map(tool => (
                            <ToolCard
                                key={tool.id}
                                title={tool.title}
                                description={tool.description}
                                icon={tool.icon}
                                onClick={() => !tool.disabled && setActiveTool(tool.id)}
                                disabled={tool.disabled}
                            />
                        ))}
                    </div>
                </MotionDiv>
            ) : (
                <MotionDiv
                    key="active-tool"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                >
                    <MotionButton onClick={() => setActiveTool(null)} className="flex items-center gap-2 text-sm font-bold text-zinc-500 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-white mb-8">
                        <ArrowLeft size={16} /> Back to Tools
                    </MotionButton>
                    {currentTool?.component}
                </MotionDiv>
            )}
        </AnimatePresence>
      </main>
    </div>
  );
};
export default InnovationZone;
