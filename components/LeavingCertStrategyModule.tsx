/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Calculator, Briefcase, Target, PenSquare, Eye, HeartPulse } from 'lucide-react';
import { ModuleProgress } from '../types';
import { redTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = redTheme;

// --- INTERACTIVE COMPONENTS ---

const PointsCalculator = () => {
    const grades = [
        { grade: 'H1', hl: 100, ol: 56 }, { grade: 'H2', hl: 88, ol: 46 }, { grade: 'H3', hl: 77, ol: 37 },
        { grade: 'H4', hl: 66, ol: 28 }, { grade: 'H5', hl: 56, ol: 20 }, { grade: 'H6', hl: 46, ol: 12 },
        { grade: 'H7', hl: 37, ol: 0 }, { grade: 'H8', hl: 0, ol: 0 }
    ];
    const getPoints = (grade: string, level: 'hl' | 'ol', isMaths: boolean) => {
        const g = grades.find(g => g.grade === grade);
        if (!g) return 0;
        let points = g[level];
        if (isMaths && level === 'hl' && ['H1','H2','H3','H4','H5','H6'].includes(grade)) {
            points += 25;
        }
        return points;
    }

    const [subjects, setSubjects] = useState(Array(7).fill({grade: 'H4', level: 'hl'}));

    const updateSubject = (index: number, field: string, value: string) => {
        const newSubjects = [...subjects];
        newSubjects[index] = {...newSubjects[index], [field]: value};
        setSubjects(newSubjects);
    };

    const subjectPoints = subjects.map((s, i) => getPoints(s.grade, s.level, i === 0));
    const totalPoints = subjectPoints.sort((a, b) => b - a).slice(0, 6).reduce((sum, p) => sum + p, 0);

    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">CAO Points Calculator</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">See how the "Best Six" and Maths Bonus work in practice.</p>
            <div className="space-y-3">
                {subjects.map((s, i) => (
                    <div key={i} className={`p-3 rounded-lg flex items-center gap-4 ${i === 0 ? 'bg-amber-50' : 'bg-zinc-50'}`}>
                        <span className="font-bold text-sm w-24">{i === 0 ? 'Maths' : `Subject ${i+1}`}</span>
                        <select value={s.level} onChange={e => updateSubject(i, 'level', e.target.value)} className="p-1 rounded-md bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700">
                            <option value="hl">Higher</option>
                            <option value="ol">Ordinary</option>
                        </select>
                        <select value={s.grade} onChange={e => updateSubject(i, 'grade', e.target.value)} className="p-1 rounded-md bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700">
                            {grades.map(g => <option key={g.grade} value={g.grade}>{g.grade}</option>)}
                        </select>
                        <span className="ml-auto font-bold text-lg">{subjectPoints[i]}</span>
                    </div>
                ))}
            </div>
            <div className="mt-8 p-6 bg-zinc-900 rounded-xl text-center">
                <p className="text-sm font-bold text-zinc-400">Total "Best Six" Points:</p>
                <p className="text-5xl font-semibold text-white">{totalPoints}</p>
            </div>
        </div>
    );
};

const SubjectClusterExplorer = () => {
    const [activeCluster, setActiveCluster] = useState<string | null>(null);
    const clusters = {
        'Lab Science': ['Biology', 'Ag Science', 'Home Ec', 'Physics', 'Applied Maths'],
        'Business': ['Business', 'Accounting', 'Economics'],
    };

    const isHighlighted = (subject: string) => activeCluster && clusters[activeCluster as keyof typeof clusters].includes(subject);

    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Syllabus Overlap Explorer</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">Click a cluster to see how subjects connect and reduce your workload.</p>
            <div className="flex justify-center gap-3 mb-6">
                <button onClick={() => setActiveCluster('Lab Science')} className={`px-4 py-2 text-sm font-bold rounded-lg border ${activeCluster === 'Lab Science' ? 'bg-emerald-500 text-white border-emerald-500' : 'bg-emerald-50 text-emerald-800 border-emerald-200'}`}>Lab Science</button>
                <button onClick={() => setActiveCluster('Business')} className={`px-4 py-2 text-sm font-bold rounded-lg border ${activeCluster === 'Business' ? 'bg-sky-500 text-white border-sky-500' : 'bg-sky-50 text-sky-800 border-sky-200'}`}>Business</button>
                <button onClick={() => setActiveCluster(null)} className="text-xs">Reset</button>
            </div>
            <div className="grid grid-cols-3 gap-3 text-center">
                <div className={`p-3 rounded-lg border ${isHighlighted('Biology') ? 'border-emerald-400 bg-emerald-50' : 'border-zinc-200 dark:border-zinc-700'}`}>Biology</div>
                <div className={`p-3 rounded-lg border ${isHighlighted('Ag Science') ? 'border-emerald-400 bg-emerald-50' : 'border-zinc-200 dark:border-zinc-700'}`}>Ag Science</div>
                <div className={`p-3 rounded-lg border ${isHighlighted('Home Ec') ? 'border-emerald-400 bg-emerald-50' : 'border-zinc-200 dark:border-zinc-700'}`}>Home Ec</div>
                <div className={`p-3 rounded-lg border ${isHighlighted('Physics') ? 'border-emerald-400 bg-emerald-50' : 'border-zinc-200 dark:border-zinc-700'}`}>Physics</div>
                <div className={`p-3 rounded-lg border ${isHighlighted('Applied Maths') ? 'border-emerald-400 bg-emerald-50' : 'border-zinc-200 dark:border-zinc-700'}`}>Applied Maths</div>
                <div className={`p-3 rounded-lg border ${isHighlighted('Business') ? 'border-sky-400 bg-sky-50' : 'border-zinc-200 dark:border-zinc-700'}`}>Business</div>
                <div className={`p-3 rounded-lg border ${isHighlighted('Accounting') ? 'border-sky-400 bg-sky-50' : 'border-zinc-200 dark:border-zinc-700'}`}>Accounting</div>
                <div className={`p-3 rounded-lg border ${isHighlighted('Economics') ? 'border-sky-400 bg-sky-50' : 'border-zinc-200 dark:border-zinc-700'}`}>Economics</div>
            </div>
        </div>
    );
};

const CommandWordDecoder = () => {
    const words = [
        { word: "Describe", expectation: '"Paint a picture" with facts.', pitfall: "Just a list of words." },
        { word: "Explain", expectation: 'Give the reason WHY (Cause & Effect).', pitfall: "Just describing what happens." },
        { word: "Compare", expectation: 'Identify similarities AND differences.', pitfall: "Writing two separate descriptions." },
        { word: "Evaluate", expectation: 'Make a judgement based on evidence. Weigh pros/cons.', pitfall: "Giving an opinion without evidence." },
    ];
    const [selected, setSelected] = useState(words[0]);

    return (
         <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Command Word Decoder</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Misinterpreting this word is the #1 cause of losing marks.</p>
            <div className="flex justify-center flex-wrap gap-2 mb-6">
                {words.map(w => <button key={w.word} onClick={() => setSelected(w)} className={`px-4 py-2 font-mono text-sm rounded-lg border ${selected.word === w.word ? 'bg-red-500 text-white border-red-500' : 'bg-zinc-100 border-zinc-200 dark:border-zinc-700'}`}>{w.word}</button>)}
            </div>
             <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                 <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-lg">
                    <p className="text-xs font-bold text-emerald-700">EXPECTATION</p>
                    <p className="mt-2 text-sm">{selected.expectation}</p>
                 </div>
                 <div className="p-4 bg-rose-50 border border-rose-200 rounded-lg">
                    <p className="text-xs font-bold text-rose-700">COMMON PITFALL</p>
                    <p className="mt-2 text-sm">{selected.pitfall}</p>
                 </div>
             </div>
        </div>
    );
}

// --- EXAM DAY TIMELINE BUILDER ---

interface TimelineActivity {
    id: number;
    label: string;
    time: number;
    isBad: boolean;
    warning: string;
    optimalOrder: number;
}

const TIMELINE_ACTIVITIES: TimelineActivity[] = [
    { id: 1, label: 'Wake up & hydrate', time: 5, isBad: false, warning: '', optimalOrder: 1 },
    { id: 2, label: '10 minutes of sunlight or bright light', time: 10, isBad: false, warning: '', optimalOrder: 2 },
    { id: 3, label: 'Low-GI breakfast (porridge, eggs, toast)', time: 15, isBad: false, warning: '', optimalOrder: 3 },
    { id: 4, label: 'Review dump sheet notes (not new material)', time: 15, isBad: false, warning: '', optimalOrder: 4 },
    { id: 5, label: 'Pack exam bag (pens, calculator, ID)', time: 5, isBad: false, warning: '', optimalOrder: 5 },
    { id: 6, label: 'Physiological sigh (2 inhales + 1 exhale)', time: 2, isBad: false, warning: '', optimalOrder: 6 },
    { id: 7, label: 'Travel to exam centre', time: 20, isBad: false, warning: '', optimalOrder: 7 },
    { id: 8, label: 'Arrive 15 minutes early', time: 15, isBad: false, warning: '', optimalOrder: 8 },
    { id: 9, label: 'Cram new material frantically', time: 10, isBad: true, warning: 'Cramming new material before an exam triggers anxiety and interferes with consolidated knowledge.' , optimalOrder: -1 },
    { id: 10, label: 'Check social media and messages', time: 10, isBad: true, warning: 'Social media activates your stress response and scatters your focus.', optimalOrder: -1 },
];

const formatTime = (totalMinutes: number): string => {
    const hours = Math.floor(totalMinutes / 60);
    const mins = totalMinutes % 60;
    const h = 7 + hours;
    return `${h}:${mins.toString().padStart(2, '0')}`;
};

const MotionDiv = motion.div as any;

const ExamDayTimelineBuilder = () => {
    const [sequence, setSequence] = useState<TimelineActivity[]>([]);
    const [flashWarning, setFlashWarning] = useState<string | null>(null);
    const [showFeedback, setShowFeedback] = useState(false);

    const selectedIds = new Set(sequence.map(a => a.id));

    const handleAddActivity = (activity: TimelineActivity) => {
        if (selectedIds.has(activity.id)) return;
        if (showFeedback) return;

        if (activity.isBad) {
            setFlashWarning(activity.warning);
            setTimeout(() => setFlashWarning(null), 3000);
        }

        setSequence(prev => [...prev, activity]);
    };

    const handleReset = () => {
        setSequence([]);
        setFlashWarning(null);
        setShowFeedback(false);
    };

    const handleCheckPlan = () => {
        setShowFeedback(true);
    };

    const getRunningTime = (index: number): number => {
        let total = 0;
        for (let i = 0; i < index; i++) {
            total += sequence[i].time;
        }
        return total;
    };

    const goodActivities = TIMELINE_ACTIVITIES.filter(a => !a.isBad);
    const optimalSequence = goodActivities.sort((a, b) => a.optimalOrder - b.optimalOrder);

    const hasBadChoices = sequence.some(a => a.isBad);
    const totalMinutes = sequence.reduce((sum, a) => sum + a.time, 0);

    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Exam Morning Planner</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Build your optimal exam morning routine. Order matters.</p>

            {/* Warning flash */}
            <AnimatePresence>
                {flashWarning && (
                    <MotionDiv
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -10 }}
                        className="mb-6 p-4 bg-rose-50 dark:bg-rose-900/30 border border-rose-300 dark:border-rose-700 rounded-lg text-rose-700 dark:text-rose-300 text-sm font-medium text-center"
                    >
                        {flashWarning}
                    </MotionDiv>
                )}
            </AnimatePresence>

            {/* Activity cards */}
            <div className="mb-8">
                <p className="text-xs font-bold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider mb-3">Click to add to your timeline:</p>
                <div className="flex flex-wrap gap-2">
                    {TIMELINE_ACTIVITIES.map(activity => {
                        const isSelected = selectedIds.has(activity.id);
                        return (
                            <button
                                key={activity.id}
                                onClick={() => handleAddActivity(activity)}
                                disabled={isSelected || showFeedback}
                                className={`px-3 py-2 text-xs font-medium rounded-lg border transition-all ${
                                    isSelected
                                        ? 'bg-zinc-100 dark:bg-zinc-700 text-zinc-400 dark:text-zinc-500 border-zinc-200 dark:border-zinc-600 cursor-default opacity-50'
                                        : activity.isBad
                                            ? 'bg-rose-50 dark:bg-rose-900/20 text-rose-700 dark:text-rose-300 border-rose-200 dark:border-rose-700 hover:bg-rose-100 dark:hover:bg-rose-900/40 cursor-pointer'
                                            : 'bg-emerald-50 dark:bg-emerald-900/20 text-emerald-700 dark:text-emerald-300 border-emerald-200 dark:border-emerald-700 hover:bg-emerald-100 dark:hover:bg-emerald-900/40 cursor-pointer'
                                }`}
                            >
                                {activity.label}
                                <span className="ml-2 text-zinc-400 dark:text-zinc-500">{activity.time}m</span>
                            </button>
                        );
                    })}
                </div>
            </div>

            {/* Timeline */}
            {sequence.length > 0 && (
                <div className="mb-6">
                    <p className="text-xs font-bold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider mb-3">Your Morning Timeline:</p>
                    <div className="relative pl-16 space-y-0">
                        {sequence.map((activity, index) => {
                            const startMin = getRunningTime(index);
                            const timeLabel = formatTime(startMin);
                            return (
                                <MotionDiv
                                    key={activity.id}
                                    initial={{ opacity: 0, x: -20 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{ duration: 0.3 }}
                                    className="relative flex items-stretch"
                                >
                                    {/* Time label */}
                                    <span className="absolute left-[-64px] top-3 text-xs font-mono font-bold text-zinc-500 dark:text-zinc-400 w-12 text-right">
                                        {timeLabel}
                                    </span>
                                    {/* Vertical line */}
                                    {index < sequence.length - 1 && (
                                        <div className="absolute left-0 top-6 bottom-0 w-px bg-zinc-300 dark:bg-zinc-600" style={{ left: '-1px' }} />
                                    )}
                                    {/* Dot */}
                                    <div className={`absolute w-2 h-2 rounded-full top-4 ${activity.isBad ? 'bg-rose-500' : 'bg-emerald-500'}`} style={{ left: '-5px' }} />
                                    {/* Activity card */}
                                    <div className={`ml-4 mb-3 p-3 rounded-lg border-l-4 flex-1 ${
                                        activity.isBad
                                            ? 'border-l-rose-500 bg-rose-50 dark:bg-rose-900/20'
                                            : 'border-l-emerald-500 bg-emerald-50 dark:bg-emerald-900/20'
                                    }`}>
                                        <div className="flex items-center gap-2">
                                            {activity.isBad && <span className="text-rose-500 text-sm">&#9888;</span>}
                                            <span className={`text-sm font-medium ${activity.isBad ? 'text-rose-700 dark:text-rose-300' : 'text-emerald-700 dark:text-emerald-300'}`}>
                                                {activity.label}
                                            </span>
                                            <span className="ml-auto text-xs text-zinc-400 dark:text-zinc-500">{activity.time} min</span>
                                        </div>
                                    </div>
                                </MotionDiv>
                            );
                        })}
                        {/* End time */}
                        <div className="relative">
                            <span className="absolute left-[-64px] top-0 text-xs font-mono font-bold text-zinc-500 dark:text-zinc-400 w-12 text-right">
                                {formatTime(totalMinutes)}
                            </span>
                            <div className={`absolute w-2 h-2 rounded-full top-1 ${totalMinutes > 140 ? 'bg-rose-500' : 'bg-zinc-400'}`} style={{ left: '-5px' }} />
                            <p className="ml-4 text-xs text-zinc-400 dark:text-zinc-500">
                                {totalMinutes > 140
                                    ? `Total: ${totalMinutes} min \u2014 You may be cutting it close!`
                                    : `Total: ${totalMinutes} min`
                                }
                            </p>
                        </div>
                    </div>
                </div>
            )}

            {/* Action buttons */}
            {sequence.length > 0 && !showFeedback && (
                <div className="flex justify-center gap-3 mt-6">
                    <button onClick={handleCheckPlan} className="px-5 py-2 text-sm font-bold rounded-lg bg-red-500 text-white hover:bg-red-600 transition-colors">
                        Check My Plan
                    </button>
                    <button onClick={handleReset} className="px-5 py-2 text-sm font-bold rounded-lg border border-zinc-300 dark:border-zinc-600 text-zinc-600 dark:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-700 transition-colors">
                        Start Over
                    </button>
                </div>
            )}

            {/* Feedback */}
            <AnimatePresence>
                {showFeedback && (
                    <MotionDiv
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.4 }}
                        className="mt-8 space-y-4"
                    >
                        {hasBadChoices && (
                            <div className="p-4 bg-rose-50 dark:bg-rose-900/20 border border-rose-200 dark:border-rose-700 rounded-lg">
                                <p className="text-sm font-bold text-rose-700 dark:text-rose-300 mb-2">Bad Choices Detected:</p>
                                {sequence.filter(a => a.isBad).map(a => (
                                    <p key={a.id} className="text-sm text-rose-600 dark:text-rose-400 ml-2">&#9888; <strong>{a.label}</strong> &mdash; {a.warning}</p>
                                ))}
                            </div>
                        )}

                        <div className="p-4 bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-700 rounded-lg">
                            <p className="text-sm font-bold text-emerald-700 dark:text-emerald-300 mb-2">Optimal Morning Sequence:</p>
                            <ol className="list-decimal list-inside space-y-1">
                                {optimalSequence.map(a => (
                                    <li key={a.id} className="text-sm text-emerald-600 dark:text-emerald-400">{a.label} <span className="text-zinc-400">({a.time} min)</span></li>
                                ))}
                            </ol>
                        </div>

                        <div className="p-5 bg-zinc-900 dark:bg-zinc-950 rounded-xl text-center">
                            <p className="text-sm text-zinc-200 leading-relaxed italic">
                                &ldquo;A calm, structured morning routine primes your prefrontal cortex for peak performance. Chaos primes your amygdala for panic.&rdquo;
                            </p>
                        </div>

                        <div className="flex justify-center mt-4">
                            <button onClick={handleReset} className="px-5 py-2 text-sm font-bold rounded-lg border border-zinc-300 dark:border-zinc-600 text-zinc-600 dark:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-700 transition-colors">
                                Start Over
                            </button>
                        </div>
                    </MotionDiv>
                )}
            </AnimatePresence>
        </div>
    );
};

// --- MODULE COMPONENT ---
const LeavingCertStrategyModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'points-marketplace', title: 'The Points Marketplace', eyebrow: '01 // The Rules of the Game', icon: Calculator },
    { id: 'portfolio-construction', title: 'Portfolio Construction', eyebrow: '02 // Strategic Subject Selection', icon: Briefcase },
    { id: 'core-tactics', title: 'Tactics: Core Subjects', eyebrow: '03 // The Big Three', icon: Target },
    { id: 'elective-tactics', title: 'Tactics: Elective Subjects', eyebrow: '04 // Exploiting the System', icon: PenSquare },
    { id: 'hidden-curriculum', title: 'The Hidden Curriculum', eyebrow: '05 // Examiner Psychology', icon: Eye },
    { id: 'exam-day-protocol', title: 'Exam Day Protocol', eyebrow: '06 // Execution in the Arena', icon: HeartPulse },
  ];

  return (
    <ModuleLayout
      moduleNumber="01"
      moduleTitle="The Points Protocol"
      moduleSubtitle="The Economics of Academic Assessment"
      moduleDescription="Deconstruct the Leaving Cert as a points-based marketplace and learn the tactical framework for maximizing your score."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Points Marketplace." eyebrow="Step 1" icon={Calculator} theme={theme}>
              <p>The Leaving Cert is not just an exam; it's a points accumulation game. To win, you must shift your mindset from a passive student to an active tactician. This means moving beyond "hard work" and focusing on <Highlight description="The true differentiator in the points race; applying effort to the areas with the highest potential return on investment." theme={theme}>efficiency</Highlight>. The points system is a rigid algorithm with exploitable inefficiencies.</p>
              <p>The three key rules of the game are: 1) The <Highlight description="Your total score is based on your six highest results. Your seventh subject is an insurance policy, allowing one catastrophic failure to be discarded." theme={theme}>"Best Six" Rule</Highlight>, 2) The 25 <Highlight description="Awarded for a H6 or higher in Higher Level Maths, this radically transforms the value of the subject, making a low pass more valuable than a high distinction in other subjects." theme={theme}>Bonus Points</Highlight> for Maths, and 3) The <Highlight description="The 37 points awarded for a H7 (30-39%) de-risks taking Higher Level, creating a 'Reach Strategy' where aiming high has a limited downside." theme={theme}>H7 Safety Net</Highlight>. Understanding these rules is the first step to mastering the system.</p>
              <PointsCalculator />
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="Portfolio Construction." eyebrow="Step 2" icon={Briefcase} theme={theme}>
              <p>If the points system is a market, your subject choice is your investment portfolio. The goal is to maximize your points yield while minimizing cognitive load. This means debunking the <Highlight description="The idea that some subjects are inherently 'easy'. H1 rates are often misleading due to self-selecting groups of students (e.g., native speakers in language subjects)." theme={theme}>'Easy Subject' Myth</Highlight> and instead focusing on structural advantages.</p>
              <p>The two most powerful strategies are the <Highlight description="Grouping subjects that share content (e.g., Biology and Ag Science) to reduce the total volume of unique information you need to learn." theme={theme}>"Cluster Strategy"</Highlight> and the <Highlight description="Choosing subjects with substantial coursework or oral components (e.g., Irish, DCG, Geography) to secure a large percentage of your grade before the written exams." theme={theme}>"Banking Marks" Strategy</Highlight>. This reduces the pressure and variance of a "bad day" in June.</p>
              <SubjectClusterExplorer />
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="Tactics: Core Subjects." eyebrow="Step 3" icon={Target} theme={theme}>
              <p>General study habits are not enough. You must study the exam itself. For English, this means mastering the rigid, algorithmic <Highlight description="The marking criteria for English: Purpose (30%), Coherence (30%), Language (30%), and Mechanics (10%). Writing to these criteria is non-negotiable." theme={theme}>PCLM Engine</Highlight> and implementing a ruthless timing strategy for Paper 2.</p>
              <p>For Maths, it's about exploiting the <Highlight description="The system of 'Partial Credit' where marks are awarded for any correct step, even if the final answer is wrong. Never leave a blank space." theme={theme}>Step-Mark Economy</Highlight>. For Irish, it's about maximizing the <Highlight description="The Oral exam accounts for 40% of the total grade. The strategy is 'fluency trumps accuracy'--it's better to keep talking with minor errors than to freeze in silence." theme={theme}>Oral Dividend</Highlight>.</p>
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="Tactics: Elective Subjects." eyebrow="Step 4" icon={PenSquare} theme={theme}>
              <p>Elective subjects have their own unique algorithms. Biology is a <Highlight description="The marking scheme is binary: specific keywords earn marks, synonyms often do not. 'Semi-permeable membrane' is a non-negotiable keyword for Osmosis." theme={theme}>Semantic Precision Game</Highlight> where specific keywords are everything. Geography is an <Highlight description="Significant Relevant Points (SRPs) are the currency of Geography. An essay is a collection of these distinct factual points, typically worth 2 marks each." theme={theme}>SRP Algorithm</Highlight> where you must deliver short, punchy, fact-laden paragraphs.</p>
              <p>Business requires <Highlight description="The expected format for long questions: State the point, Explain the concept, provide a relevant Example." theme={theme}>Structure as Content</Highlight>, following the "State, Explain, Example" format. These are not suggestions; they are the rules of the game you must play to win.</p>
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="The Hidden Curriculum." eyebrow="Step 5" icon={Eye} theme={theme}>
              <p>Beyond the syllabus lies the "Hidden Curriculum"--the specific language and expectations of the State Examinations Commission. Every question contains a <Highlight description="The verb in the question (e.g., Describe, Explain, Evaluate) that dictates the required style of answer. Misinterpreting this is a leading cause of losing marks." theme={theme}>Command Word</Highlight> that dictates the required output. 'Describe' asks for a picture in words; 'Explain' asks for a cause-and-effect reason. They are not the same.</p>
              <p>The most valuable strategic document is the <Highlight description="Published every few years, this document details common student errors. It is a goldmine of 'negative data'--telling you exactly what not to do." theme={theme}>Chief Examiner's Report (CER)</Highlight>. This is the official "cheat sheet" for the exam, outlining the most common pitfalls that you must learn to avoid.</p>
              <CommandWordDecoder />
              <MicroCommitment theme={theme}><p>Go to the SEC website, find the most recent Chief Examiner's Report for your favourite subject, and read only the "Recommendations to Candidates" section. You've just accessed the official cheat sheet.</p></MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="Exam Day Protocol." eyebrow="Step 6" icon={HeartPulse} theme={theme}>
              <p>All your preparation is useless without effective execution in the arena. The exam hall is a high-pressure environment where physiological regulation is as important as academic knowledge.</p>
              <p>Master the <Highlight description="A protocol for the start of an exam: 30 seconds of tactical breathing to calm the nervous system, followed by a 'brain dump' of key formulas and quotes onto rough work paper to free up working memory." theme={theme}>"First 5 Minutes" Protocol</Highlight> to manage panic. Adhere to a <Highlight description="A strict timing plan where you move on when the allocated time for a question is up, no matter what. The 'first marks' of the next question are always easier than the 'last marks' of the current one." theme={theme}>Non-Negotiable Contract</Highlight> for time management. And finally, use the Post-Exam Script Review in September as a final strategic lever for appeals and, more importantly, for learning.</p>
              <ExamDayTimelineBuilder />
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default LeavingCertStrategyModule;
