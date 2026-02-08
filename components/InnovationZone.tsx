
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
    ArrowLeft, Lightbulb, Zap, Clock, Brain, SlidersHorizontal, Shield, User, Repeat, Wrench, RotateCcw,
    Heart, TrendingUp, Users, BookOpen, Sun, ArrowDown, GitBranch
} from 'lucide-react';

const MotionDiv = motion.div as any;
const MotionButton = motion.button as any;

interface InnovationZoneProps {
  onBack: () => void;
}

type GameState = {
    energy: number;
    academicCap: number;
    socialSupport: number;
    systemSavvy: number;
    resilience: number;
};

type Choice = {
    text: string;
    effects: Partial<GameState>;
    nextSceneId: string;
};

type LogicGate = {
    condition: (state: GameState) => boolean;
    nextSceneId: string;
}

type Scene = {
    id: string;
    phase: 'Foundation' | 'Pressure Cooker' | 'Final Stretch';
    month: string;
    title: string;
    text: string;
    choices?: Choice[];
    logicGates?: LogicGate[];
    defaultNextSceneId?: string;
};

type HistoryItem = {
    scene: Scene;
    choiceText: string;
    effects: Partial<GameState>;
};


const STORY_DATA: { [key: string]: Scene } = {
    'START': {
        id: 'START',
        phase: 'Foundation',
        month: 'September',
        title: "The First Week Back",
        text: "It's the first week of 6th year. The air is thick with talk of points and the CAO. A friend who got into college last year tells you, 'You should definitely apply for the HEAR scheme, it's a game-changer for getting in.'",
        choices: [
            { text: "Look into it. Sounds like a priority.", effects: { systemSavvy: 15, energy: -5 }, nextSceneId: 'MATHS_CLASS' },
            { text: "Maybe later. I need to focus on just studying for now.", effects: { systemSavvy: -10, academicCap: 5 }, nextSceneId: 'MATHS_CLASS' },
        ],
    },
    'MATHS_CLASS': {
        id: 'MATHS_CLASS',
        phase: 'Foundation',
        month: 'October',
        title: "The Pace of Higher Maths",
        text: "Your Higher Level Maths teacher is moving at lightning speed through Complex Numbers. You're starting to feel lost, but you don't want to look stupid by asking a question.",
        choices: [
            { text: "Stay quiet and try to figure it out yourself later.", effects: { academicCap: -10, resilience: -5 }, nextSceneId: 'FIRST_BAD_GRADE' },
            { text: "Ask the teacher to explain it again after class.", effects: { academicCap: 10, socialSupport: 5, energy: -5 }, nextSceneId: 'FIRST_BAD_GRADE' },
        ],
    },
    'FIRST_BAD_GRADE': {
        id: 'FIRST_BAD_GRADE',
        phase: 'Foundation',
        month: 'October',
        title: "The First Bad Grade",
        text: "You get back your first big test in English. It's a H4. Your heart sinks. What's your immediate internal story?",
        choices: [
            { text: "'This proves I'm not a H1 student.' Spend the evening feeling demotivated.", effects: { resilience: -15, energy: -10 }, nextSceneId: 'STUDY_METHOD_CHOICE' },
            { text: "'This is data. I haven't mastered this *yet*. I'll review the feedback tomorrow.'", effects: { resilience: 10, academicCap: 5 }, nextSceneId: 'STUDY_METHOD_CHOICE' },
        ]
    },
    'STUDY_METHOD_CHOICE': {
        id: 'STUDY_METHOD_CHOICE',
        phase: 'Foundation',
        month: 'November',
        title: "Sunday Night Study",
        text: "It's a Sunday night and you have a big Biology test on Friday. You have a 2-hour study block. What's the plan?",
        choices: [
            { text: "Passive Power-through: Re-read and highlight the key chapters. It feels productive.", effects: { energy: -5, academicCap: 5 }, nextSceneId: 'FORGETTING_CURVE_CRISIS' },
            { text: "Active Recall Assault: Close the book and 'blurt' everything you know onto a page. It feels hard.", effects: { energy: -15, academicCap: 15, resilience: 5 }, nextSceneId: 'STUDY_TECHNIQUE_UPGRADE' },
        ]
    },
    'FORGETTING_CURVE_CRISIS': {
        id: 'FORGETTING_CURVE_CRISIS',
        phase: 'Foundation',
        month: 'November',
        title: "The 'I Forgot Everything' Moment",
        text: "You spent all weekend highlighting Biology chapters. Today, your teacher gives a pop quiz and your mind is a total blank. The 'Illusion of Competence' has struck. How do you react?",
        choices: [
            { text: "Mindset Shift: 'I haven't mastered this YET.' Switch to Active Recall tonight.", effects: { resilience: 15, academicCap: 10, energy: -10 }, nextSceneId: 'PART_TIME_JOB' },
            { text: "Fixed Frustration: 'I'm just not a Science person.' Go back to re-reading.", effects: { resilience: -10, academicCap: -5, energy: -5 }, nextSceneId: 'PART_TIME_JOB' },
        ],
    },
    'STUDY_TECHNIQUE_UPGRADE': {
        id: 'STUDY_TECHNIQUE_UPGRADE',
        phase: 'Foundation',
        month: 'November',
        title: "Technique Upgrade",
        text: "Because you chose Active Recall, your brain flagged the information as important. The pop quiz felt challenging, but you could retrieve most of the key facts. You feel a surge of confidence.",
        choices: [
            { text: "Double down: 'This works. I'll build Spaced Repetition into my routine.'", effects: { academicCap: 10, systemSavvy: 10 }, nextSceneId: 'PART_TIME_JOB' },
            { text: "Get complacent: 'Great, I can ease off a bit now.'", effects: { academicCap: -5, energy: 5 }, nextSceneId: 'PART_TIME_JOB' },
        ],
    },
    'PART_TIME_JOB': {
        id: 'PART_TIME_JOB',
        phase: 'Foundation',
        month: 'December',
        title: "Work-Life Balance",
        text: "Your boss at your weekend job asks if you can cover an extra shift on Thursday night. It's good money, but it's a big study night for you.",
        choices: [
            { text: "Take the shift. The money is too important right now.", effects: { energy: -20, academicCap: -10 }, nextSceneId: 'MOCKS_LOOM' },
            { text: "Politely decline. 'The Leaving' has to come first.", effects: { resilience: 5, academicCap: 5, energy: -5 }, nextSceneId: 'MOCKS_LOOM' },
        ],
    },
     'MOCKS_LOOM': {
        id: 'MOCKS_LOOM',
        phase: 'Pressure Cooker',
        month: 'January',
        title: "The Mocks Are Looming",
        text: "It's the week before the Mocks. You feel completely overwhelmed by the amount of material you need to cover. The panic is starting to set in.",
        choices: [
            { text: "Panic-cram: Pull two all-nighters for your weakest subjects.", effects: { academicCap: 10, energy: -40, resilience: -15 }, nextSceneId: 'BURNOUT_CHECK' },
            { text: "Strategic Triage: Use Interleaving on high-yield topics and protect your sleep schedule.", effects: { academicCap: 15, energy: -10, resilience: 10, systemSavvy: 5 }, nextSceneId: 'BURNOUT_CHECK' },
        ],
    },
    'BURNOUT_CHECK': {
        id: 'BURNOUT_CHECK',
        phase: 'Pressure Cooker',
        month: 'February',
        title: "Energy Check",
        text: "Checking your energy levels...",
        logicGates: [
            { condition: (state) => state.energy < 30, nextSceneId: 'BURNOUT_RECOVERY' }
        ],
        defaultNextSceneId: 'CAO_DEADLINE'
    },
    'BURNOUT_RECOVERY': {
        id: 'BURNOUT_RECOVERY',
        phase: 'Pressure Cooker',
        month: 'March',
        title: "Strategic Reset",
        text: "You've hit a wall. You're exhausted and the Mocks were brutal. You feel like quitting the Higher Level paper.",
        choices: [
            { text: "The 'Grit' Protocol: Take 2 days off entirely to recharge energy, then simplify the goal.", effects: { energy: 40, resilience: 20, academicCap: -5 }, nextSceneId: 'ADVANCED_STRATEGY_CHECK' },
            { text: "Push Through: Force yourself to study 4 hours tonight with caffeine.", effects: { energy: -20, academicCap: 5, resilience: -15 }, nextSceneId: 'ACUTE_EXHAUSTION' },
        ],
    },
    'ACUTE_EXHAUSTION': {
        id: 'ACUTE_EXHAUSTION',
        phase: 'Pressure Cooker',
        month: 'March',
        title: "Acute Exhaustion",
        text: "You pushed through the exhaustion. You walk into class feeling wired on caffeine and no sleep. You read a question and... nothing. Your mind is a total blank.",
        choices: [
            { text: "Breathe. Use the Physiological Sigh to reset. Ask for help after class.", effects: { resilience: 20, energy: -10, socialSupport: 5 }, nextSceneId: 'ADVANCED_STRATEGY_CHECK' },
            { text: "Panic. The catastrophic thoughts take over. Say nothing.", effects: { resilience: -20, academicCap: -10, energy: -10 }, nextSceneId: 'ADVANCED_STRATEGY_CHECK' },
        ],
    },
    'CAO_DEADLINE': {
        id: 'CAO_DEADLINE',
        phase: 'Pressure Cooker',
        month: 'February',
        title: "The CAO Deadline",
        text: "The CAO deadline is this week. You're torn between a 'dream' course that feels like a reach and a 'safe' PLC or lower-points course that feels more realistic.",
        choices: [
            { text: "Be realistic. Put the safer options down first.", effects: { systemSavvy: 5, resilience: -5 }, nextSceneId: 'ADVANCED_STRATEGY_CHECK' },
            { text: "Shoot for the stars. Put the dream course as #1.", effects: { resilience: 10, systemSavvy: 5 }, nextSceneId: 'ADVANCED_STRATEGY_CHECK' },
        ],
    },
    'ADVANCED_STRATEGY_CHECK': {
        id: 'ADVANCED_STRATEGY_CHECK',
        phase: 'Pressure Cooker',
        month: 'March',
        title: "Competence Check",
        text: "Checking your academic progress...",
        logicGates: [
            { condition: (state) => state.academicCap > 70, nextSceneId: 'INTERLEAVING_CHOICE' }
        ],
        defaultNextSceneId: 'FINAL_STRETCH_START'
    },
    'INTERLEAVING_CHOICE': {
        id: 'INTERLEAVING_CHOICE',
        phase: 'Pressure Cooker',
        month: 'April',
        title: "Advanced Strategy: Interleaving",
        text: "You're feeling confident with your subjects. A teacher mentions a study technique called 'Interleaving'. It sounds harder than just focusing on one topic at a time.",
        choices: [
            { text: "Stick with what works: Blocked practice. Master one topic before moving on.", effects: { academicCap: 5, energy: -5 }, nextSceneId: 'FINAL_STRETCH_START' },
            { text: "Try Interleaving: Mix up different topics in one study session. It feels messy but effective.", effects: { academicCap: 15, energy: -10, resilience: 5 }, nextSceneId: 'FINAL_STRETCH_START' },
        ],
    },
    'FINAL_STRETCH_START': {
        id: 'FINAL_STRETCH_START',
        phase: 'Final Stretch',
        month: 'April',
        title: "The Final Push",
        text: "It's April. The final push. Your teacher gives you a heavy-duty revision plan.",
        choices: [
            { text: "Follow their plan blindly.", effects: { systemSavvy: 5 }, nextSceneId: 'PEER_SUPPORT_CHOICE' },
            { text: "Adapt the plan to my own weak areas using a Retrospective Log.", effects: { systemSavvy: 10, resilience: 5, academicCap: 5 }, nextSceneId: 'PEER_SUPPORT_CHOICE' },
        ]
    },
     'PEER_SUPPORT_CHOICE': {
        id: 'PEER_SUPPORT_CHOICE',
        phase: 'Final Stretch',
        month: 'May',
        title: "The Protégé Effect",
        text: "A classmate you're friendly with is panicking about a key topic in Maths that you've mastered. They ask if you could spend a couple of hours explaining it to them. It would eat into your own revision time.",
        choices: [
            { text: "Help them out. Explaining it will probably strengthen my own understanding anyway.", effects: { socialSupport: 15, academicCap: 5, energy: -10, resilience: 5 }, nextSceneId: 'GAME_DAY_PREP' },
            { text: "Sorry, I need to focus on my own weak areas. It's too close to the exams.", effects: { socialSupport: -10, academicCap: 10, energy: -5 }, nextSceneId: 'GAME_DAY_PREP' },
        ],
    },
    'GAME_DAY_PREP': {
        id: 'GAME_DAY_PREP',
        phase: 'Final Stretch',
        month: 'June',
        title: "Game Day Prep",
        text: "It's the night before your first exam. What's the final move?",
        choices: [
            { text: "Last-minute cramming session until 2 AM.", effects: { energy: -30, academicCap: 5 }, nextSceneId: 'END_LOGIC' },
            { text: "Pack my bag, do a 10-minute review, and get a full night's sleep.", effects: { energy: 20, resilience: 10 }, nextSceneId: 'END_LOGIC' },
        ],
    },
    'END_LOGIC': {
        id: 'END_LOGIC',
        phase: 'Final Stretch',
        month: 'June',
        title: "Results Day",
        text: "Calculating your outcome...",
        logicGates: [
            { condition: (state) => state.resilience > 70 && state.socialSupport > 60, nextSceneId: 'END_PATHFINDER' },
            { condition: (state) => state.academicCap > 80 && state.energy > 50, nextSceneId: 'END_EXPERT' },
            { condition: (state) => state.socialSupport > 70 && state.systemSavvy > 60, nextSceneId: 'END_MENTOR' },
            { condition: (state) => state.academicCap > 65 && state.systemSavvy > 50, nextSceneId: 'END_GOOD' },
            { condition: (state) => state.resilience > 50, nextSceneId: 'END_PLC' },
        ],
        defaultNextSceneId: 'END_REPEAT'
    },
    'END_GOOD': {
        id: 'END_GOOD',
        phase: 'Final Stretch',
        month: 'August',
        title: "Offer Received!",
        text: "Congratulations! Your hard work and strategic planning paid off. You received an offer for one of your top choices. Your ability to manage your resources, seek help when needed, and stay resilient under pressure was the key to your success. The next chapter begins now.",
    },
    'END_PLC': {
        id: 'END_PLC',
        phase: 'Final Stretch',
        month: 'August',
        title: "A Different Path",
        text: "The points didn't line up for your first choice this time, but your journey isn't over. You've secured a place in a brilliant PLC course that acts as a direct pathway to your dream degree next year. Your resilience means you see this not as a setback, but as a strategic stepping stone.",
    },
    'END_REPEAT': {
        id: 'END_REPEAT',
        phase: 'Final Stretch',
        month: 'August',
        title: "Another Lap",
        text: "It was a tough year, and the results weren't what you hoped for. But your journey has given you immense resilience and social support. You've decided to repeat, armed with a year's worth of wisdom and a much clearer strategy. This isn't failure; it's the start of your comeback story.",
    },
    'END_PATHFINDER': {
        id: 'END_PATHFINDER',
        phase: 'Final Stretch',
        month: 'August',
        title: "The Resilient Pathfinder",
        text: "The points came in, and you got your course. But more than that, you navigated the year with incredible resilience. You're known as the person who never gives up and always has time to help a friend. You've already started mentoring younger students, showing them the ropes.",
    },
    'END_EXPERT': {
        id: 'END_EXPERT',
        phase: 'Final Stretch',
        month: 'August',
        title: "The Efficiency Expert",
        text: "You crushed it. Your disciplined, science-backed approach to study paid off with a stellar points total. You didn't just learn the material; you learned how to learn. Your energy management was flawless, and you enter college with a powerful cognitive toolkit that will serve you for life.",
    },
    'END_MENTOR': {
        id: 'END_MENTOR',
        phase: 'Final Stretch',
        month: 'August',
        title: "The Community Mentor",
        text: "You not only got your course but you became a master of the system. You understood every grant, scheme, and deadline, and shared that knowledge freely. Your friends and family see you as the go-to person for advice, and you've built a powerful support network that will be your foundation for success in college and beyond.",
    },
};


const StatBar = ({ icon: Icon, label, value, color }: { icon: any, label: string, value: number, color: string }) => (
    <div>
        <div className="flex items-center gap-2">
            <Icon size={16} className={color}/>
            <p className="text-xs font-bold uppercase tracking-wider text-stone-500 dark:text-stone-400">{label}</p>
        </div>
        <div className="w-full bg-stone-200 dark:bg-white/10 rounded-full h-2.5 mt-1">
            <MotionDiv 
                className={`h-2.5 rounded-full ${color.replace('text-', 'bg-')}`}
                initial={{ width: '0%' }}
                animate={{ width: `${value}%` }}
            />
        </div>
    </div>
);


const AcademicJourneyGame: React.FC = () => {
    const [gameState, setGameState] = useState<GameState>({
        energy: 60,
        academicCap: 30,
        socialSupport: 50,
        systemSavvy: 20,
        resilience: 40,
    });
    const [currentSceneId, setCurrentSceneId] = useState('START');
    const [history, setHistory] = useState<HistoryItem[]>([]);

    let currentScene = STORY_DATA[currentSceneId];
    
    if (currentScene && currentScene.logicGates) {
        let nextScene = currentScene.defaultNextSceneId;
        for (const gate of currentScene.logicGates) {
            if (gate.condition(gameState)) {
                nextScene = gate.nextSceneId;
                break;
            }
        }
        if(nextScene) {
            currentScene = STORY_DATA[nextScene];
            setCurrentSceneId(nextScene);
        }
    }

    const handleChoice = (choice: Choice) => {
        const currentChoiceScene = STORY_DATA[currentSceneId];
        const newGameState = { ...gameState };
        
        for (const [key, value] of Object.entries(choice.effects)) {
            newGameState[key as keyof GameState] = Math.max(0, Math.min(100, newGameState[key as keyof GameState] + value));
        }

        setHistory([...history, { scene: currentChoiceScene, choiceText: choice.text, effects: choice.effects }]);
        setGameState(newGameState);
        setCurrentSceneId(choice.nextSceneId);
    };
    
    const restartGame = () => {
        setGameState({ energy: 60, academicCap: 30, socialSupport: 50, systemSavvy: 20, resilience: 40 });
        setCurrentSceneId('START');
        setHistory([]);
    };

    const renderEndScreen = () => {
        const endScene = STORY_DATA[currentSceneId];
        const statIcons: { [key: string]: React.ElementType } = {
            energy: Zap,
            academicCap: TrendingUp,
            socialSupport: Users,
            systemSavvy: BookOpen,
            resilience: Shield
        };

        return (
             <MotionDiv initial={{opacity: 0}} animate={{opacity: 1}} className="text-center">
                <h3 className="font-serif text-3xl font-semibold text-purple-600 dark:text-purple-400 mb-4">{endScene.title}</h3>
                <p className="text-stone-600 dark:text-stone-300 mb-8">{endScene.text}</p>
                <h4 className="font-bold mb-4 text-stone-800 dark:text-white">Your Journey Log:</h4>
                <div className="text-left space-y-4 max-h-96 overflow-y-auto p-4 bg-stone-100 dark:bg-white/5 rounded-xl border border-stone-200 dark:border-white/10 relative">
                    {history.map((item, index) => (
                        <div key={index} className="relative pl-8">
                            <div className="absolute top-1 left-0 flex flex-col items-center">
                                <div className="w-6 h-6 rounded-full bg-purple-200 dark:bg-purple-800 flex items-center justify-center ring-4 ring-stone-100 dark:ring-white/5">
                                    <GitBranch size={14} className="text-purple-600 dark:text-purple-300"/>
                                </div>
                                 {index < history.length - 1 && <div className="w-px h-full bg-stone-300 dark:bg-stone-700 mt-1" style={{height: 'calc(100% + 1rem)'}} />}
                            </div>

                            <p className="font-bold text-sm text-stone-800 dark:text-stone-200">{item.scene.month}: {item.scene.title}</p>
                            
                            <div className="mt-2 space-y-2">
                                {item.scene.choices?.map(choice => {
                                    const isChosen = choice.text === item.choiceText;
                                    return (
                                        <div key={choice.text} className={`p-3 rounded-lg border-2 text-xs transition-all ${isChosen ? 'bg-white dark:bg-white/10 border-purple-400/50' : 'bg-transparent border-transparent opacity-40'}`}>
                                            <p className={`${isChosen ? 'font-bold' : ''}`}>{choice.text}</p>
                                            {isChosen && (
                                                <div className="flex items-center gap-3 mt-2 border-t border-stone-200 dark:border-white/10 pt-2">
                                                    {Object.entries(item.effects).map(([stat, value]) => {
                                                        const Icon = statIcons[stat];
                                                        const isPositive = value >= 0;
                                                        return (
                                                            <div key={stat} className="flex items-center gap-1">
                                                                <Icon size={12} className={isPositive ? 'text-emerald-500' : 'text-rose-500'} />
                                                                <span className={`font-mono text-xs font-bold ${isPositive ? 'text-emerald-500' : 'text-rose-500'}`}>{isPositive ? '+' : ''}{value}</span>
                                                            </div>
                                                        );
                                                    })}
                                                </div>
                                            )}
                                        </div>
                                    );
                                })}
                            </div>
                        </div>
                    ))}
                     <div className="text-center pt-4">
                        <ArrowDown size={16} className="text-stone-400 dark:text-stone-600 mx-auto animate-bounce"/>
                     </div>
                </div>

                <MotionButton onClick={restartGame} className="mt-8 group flex items-center justify-center gap-2 mx-auto px-6 py-3 bg-stone-800 text-white font-bold text-sm rounded-full shadow-lg hover:bg-purple-600 transition-colors">
                  Play Again <RotateCcw size={16} />
                </MotionButton>
            </MotionDiv>
        );
    }

    if (!currentScene || !currentScene.choices) {
        return renderEndScreen();
    }
    
    return (
        <div className="bg-white/50 dark:bg-white/5 backdrop-blur-2xl border border-stone-200/50 dark:border-white/10 rounded-[2rem] p-8">
            <AnimatePresence mode="wait">
            <MotionDiv 
                key={currentSceneId}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                transition={{ duration: 0.4, ease: 'easeInOut' }}
            >
                <div className="border-b border-stone-200 dark:border-white/10 pb-4 mb-6">
                    <p className="text-xs font-bold uppercase tracking-widest text-purple-600 dark:text-purple-400">{currentScene.phase} - {currentScene.month}</p>
                    <h3 className="font-serif text-3xl font-semibold text-stone-900 dark:text-white">{currentScene.title}</h3>
                </div>

                <p className="text-stone-600 dark:text-stone-300 leading-relaxed mb-8">{currentScene.text}</p>

                <div className="space-y-3 mb-8">
                    {currentScene.choices.map((choice, index) => (
                        <MotionButton
                            key={index}
                            onClick={() => handleChoice(choice)}
                            whileHover={{ scale: 1.02 }}
                            whileTap={{ scale: 0.98 }}
                            className="w-full text-left p-4 rounded-xl bg-stone-100 dark:bg-white/5 border border-stone-200 dark:border-white/10 hover:bg-stone-200 dark:hover:bg-white/10 transition-colors font-semibold text-stone-700 dark:text-stone-200"
                        >
                            {choice.text}
                        </MotionButton>
                    ))}
                </div>
                
                <div>
                    <h4 className="font-bold text-sm uppercase tracking-widest text-stone-500 dark:text-stone-400 mb-4 text-center">Life Dashboard</h4>
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
    );
};

const ToolCard: React.FC<{title: string, description: string, icon: React.ElementType, onClick: () => void, disabled?: boolean, accentColor?: string}> = 
({ title, description, icon: Icon, onClick, disabled = false, accentColor = 'text-purple-500' }) => (
    <MotionButton
        onClick={onClick}
        disabled={disabled}
        whileHover={{ scale: disabled ? 1 : 1.03 }}
        className={`w-full text-left p-6 rounded-2xl border-2 transition-all ${disabled ? 'bg-stone-50 dark:bg-white/5 border-stone-200 dark:border-white/10 opacity-50 cursor-not-allowed' : 'bg-white/50 dark:bg-white/10 border-stone-200/80 dark:border-white/15 hover:border-purple-300 dark:hover:border-purple-500/50 cursor-pointer'}`}
    >
        <div className="flex items-center gap-4">
            <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${disabled ? 'bg-stone-200 dark:bg-white/10' : 'bg-purple-100 dark:bg-purple-900/50'}`}>
                <Icon size={24} className={disabled ? 'text-stone-400 dark:text-stone-600' : accentColor} />
            </div>
            <div>
                <h3 className="font-bold text-stone-800 dark:text-white">{title}</h3>
                <p className="text-xs text-stone-500 dark:text-stone-400">{disabled ? "Coming Soon..." : description}</p>
            </div>
        </div>
    </MotionButton>
);


const InnovationZone: React.FC<InnovationZoneProps> = ({ onBack }) => {
    const [activeTool, setActiveTool] = useState<string | null>(null);

    const tools = [
        { id: 'journey', title: 'Academic Journey Simulator', description: 'Navigate the choices of your final school year.', icon: GitBranch, component: <AcademicJourneyGame /> },
        { id: 'focus', title: 'Deep Focus Timer', description: 'A customizable timer based on the Pomodoro technique.', icon: Clock, disabled: true },
        { id: 'planner', title: 'Retrospective Timetable', description: 'A data-driven study planner based on your confidence.', icon: Wrench, disabled: true }
    ];

    const currentTool = tools.find(t => t.id === activeTool);
    
  return (
    <div className="min-h-screen bg-[#FDFCFB] dark:bg-stone-950 transition-colors duration-500 overflow-x-hidden relative flex flex-col items-center pt-32 pb-24">
      
      <header className="fixed top-0 left-0 right-0 z-[60] bg-white/60 dark:bg-stone-950/60 backdrop-blur-2xl border-b border-stone-200/50 dark:border-white/5 px-10 py-6">
        <div className="container mx-auto flex items-center justify-between">
          <div className="flex items-center gap-8">
            <MotionButton whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={onBack} className="tactile-button p-3 rounded-full bg-white dark:bg-stone-800 border border-stone-200 dark:border-stone-700 transition-all">
              <ArrowLeft size={18} className="text-stone-900 dark:text-white" />
            </MotionButton>
            <div className="h-10 w-px bg-stone-200/50 dark:bg-stone-700" />
            <div>
              <p className="font-mono text-[9px] font-bold text-stone-400 dark:text-stone-500 uppercase tracking-[0.5em] mb-1">Experimental Division</p>
              <h1 className="font-serif font-semibold text-2xl tracking-tight text-stone-900 dark:text-white">The Innovation Zone</h1>
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
                        <h2 className="font-serif text-5xl font-semibold text-stone-900 dark:text-white">Experimental Tools</h2>
                        <p className="max-w-xl mx-auto mt-4 text-stone-500 dark:text-stone-400">A collection of interactive simulations and utilities designed to help you master the key concepts from the Learning Lab.</p>
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
                    <MotionButton onClick={() => setActiveTool(null)} className="flex items-center gap-2 text-sm font-bold text-stone-500 dark:text-stone-400 hover:text-stone-900 dark:hover:text-white mb-8">
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
