/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Calculator, Briefcase, Target, PenSquare, Eye, HeartPulse } from 'lucide-react';
import { ModuleProgress } from '../types';
import { redTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment, PersonalStory } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';
import { useNorthStar } from '../hooks/useNorthStar';
import NorthStarCallout from './NorthStarCallout';
import { COMPACT_CALLOUT_PLACEMENTS } from '../northStarData';

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
                                &ldquo;A calm, structured morning sets your brain up to perform at its best. A chaotic one sets it up for panic.&rdquo;
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
    { id: 'points-game', title: 'How the Points Game Works', eyebrow: '01 // The Rules', icon: Calculator },
    { id: 'picking-subjects', title: 'Picking Your Subjects Smartly', eyebrow: '02 // Subject Choice', icon: Briefcase },
    { id: 'core-subjects', title: 'English, Maths & Irish', eyebrow: '03 // The Big Three', icon: Target },
    { id: 'elective-subjects', title: 'Your Other Subjects', eyebrow: '04 // Working the System', icon: PenSquare },
    { id: 'what-examiners-want', title: 'What Examiners Actually Want', eyebrow: '05 // Reading the Exam', icon: Eye },
    { id: 'exam-day', title: 'Exam Day: Your Game Plan', eyebrow: '06 // On the Day', icon: HeartPulse },
  ];

  const { northStar } = useNorthStar();

  return (
    <ModuleLayout
      moduleNumber="01"
      moduleTitle="The Points Playbook"
      moduleSubtitle="Your Game Plan for the Leaving Cert"
      moduleDescription="The Leaving Cert is a points game -- and like any game, once you know the rules, you can play it a whole lot smarter. Here's your game plan for getting the most points you can."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="How the Points Game Works." eyebrow="Step 1" icon={Calculator} theme={theme}>
              {northStar && (() => { const p = COMPACT_CALLOUT_PLACEMENTS.find(p => p.moduleId === 'leaving-cert-strategy-protocol'); return p ? <NorthStarCallout northStar={northStar} variant="compact" message={p.message} /> : null; })()}
              <p>Here's the thing nobody spells out clearly enough: the Leaving Cert is a points game. Working hard matters, but working <Highlight description="It's not just about hours at the desk -- it's about putting your energy into the things that will actually move your points the most." theme={theme}>smart</Highlight> matters more. Once you know how the scoring actually works, you can make way better decisions about where to focus.</p>
              <p>There are three rules you absolutely need to know: 1) The <Highlight description="Only your six best results count. Your seventh subject is basically a safety net -- if one exam goes badly, it gets dropped." theme={theme}>"Best Six" Rule</Highlight>, 2) The 25 <Highlight description="If you get a H6 or higher in Higher Level Maths, you get 25 extra points on top. That makes even a low pass in HL Maths worth more than top marks in many other subjects." theme={theme}>Bonus Points</Highlight> for Maths, and 3) The <Highlight description="You get 37 points just for scraping a H7 (30-39%) at Higher Level. That means trying Higher Level is way less risky than most people think." theme={theme}>H7 Safety Net</Highlight>. Get your head around these three things and you're already ahead of most students.</p>
              <PointsCalculator />
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="Picking Your Subjects Smartly." eyebrow="Step 2" icon={Briefcase} theme={theme}>
              <p>Your subject choice is one of the biggest decisions you'll make for the Leaving Cert. The goal is simple: pick subjects where you can get the most points without burning yourself out. That means ignoring the <Highlight description="People love to say some subjects are 'easy picks'. But H1 rates can be misleading -- sometimes a subject looks easy because only the strongest students take it (like native speakers in languages)." theme={theme}>'Easy Subject' Myth</Highlight> and thinking about what actually gives you an edge.</p>
              <p>Two approaches that really work: the <Highlight description="Some subjects share a lot of content -- like Biology and Ag Science. If you pick subjects that overlap, you're learning the same material for two exams instead of one." theme={theme}>"Cluster" Approach</Highlight> (picking subjects with overlapping content) and the <Highlight description="Subjects like Irish, DCG, and Geography have orals, projects, or coursework that let you lock in a chunk of your grade before the written exams even start." theme={theme}>"Bank Your Marks" Approach</Highlight> (choosing subjects where you can lock in marks through coursework or orals before June). Both take pressure off exam day.</p>
              <SubjectClusterExplorer />
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="English, Maths & Irish." eyebrow="Step 3" icon={Target} theme={theme}>
              <p>Studying hard is one thing, but studying the exam itself is what makes the real difference. For English, you need to understand <Highlight description="English is marked on four things: Purpose (30%), Coherence (30%), Language (30%), and Mechanics (10%). If you write with these in mind, you're giving the examiner exactly what they want." theme={theme}>how PCLM marking works</Highlight> and make sure you're timing Paper 2 properly so you actually finish.</p>
              <p>For Maths, the big secret is <Highlight description="You get marks for every correct step, even if your final answer is wrong. So never leave a question blank -- write down whatever you can, because every line could be worth marks." theme={theme}>partial credit</Highlight> -- every correct step earns marks, even if the final answer is wrong. For Irish, the oral is worth 40% of your total grade, so it's a massive opportunity. The key? <Highlight description="In the oral, it's much better to keep talking -- even with a few mistakes -- than to freeze up and say nothing. Fluency beats perfection." theme={theme}>Keep talking</Highlight>, even if it's not perfect.</p>
              <PersonalStory name="Aoife, Dublin" role="Leaving Cert 2024">
                <p>I used to panic in the Irish oral and go completely silent when I made a mistake. Once I realised the examiner just wanted to hear me talk, I stopped worrying about being perfect and just kept going. I ended up getting a H3 -- way higher than I expected.</p>
              </PersonalStory>
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="Your Other Subjects." eyebrow="Step 4" icon={PenSquare} theme={theme}>
              <p>Every subject has its own way of giving out marks, and knowing how each one works is a huge advantage. In Biology, it's all about <Highlight description="The examiner is looking for exact keywords. A close synonym often won't count -- you need the precise term from the syllabus, like 'semi-permeable membrane' for osmosis." theme={theme}>using the exact right words</Highlight> -- the marking scheme rewards specific keywords, not vague descriptions. In Geography, it's about <Highlight description="Geography essays are marked on how many distinct, relevant facts you include. Each one is usually worth about 2 marks, so pack in as many clear points as you can." theme={theme}>packing in clear, separate facts</Highlight> rather than writing long flowery paragraphs.</p>
              <p>For Business, <Highlight description="Long questions in Business follow a pattern: State your point, Explain what it means, then give an Example. Stick to this and you'll pick up marks consistently." theme={theme}>structure is everything</Highlight> -- follow the "State, Explain, Example" format and you'll pick up marks every time. These aren't just tips; they're how the marking schemes actually work.</p>
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="What Examiners Actually Want." eyebrow="Step 5" icon={Eye} theme={theme}>
              <p>There's a whole layer to the exams that nobody really teaches you in class. Every exam question has a <Highlight description="Words like 'Describe', 'Explain', and 'Evaluate' each tell you to answer in a completely different way. Getting this wrong is one of the most common reasons students lose marks." theme={theme}>command word</Highlight> -- a verb like "Describe" or "Explain" -- and each one is asking for a different type of answer. Mix them up and you'll lose marks even if you know the topic inside out.</p>
              <p>Here's a brilliant free resource most students never use: the <Highlight description="The SEC publishes reports that spell out exactly where students went wrong in previous years. It's basically a list of mistakes to avoid -- like having the answers in advance." theme={theme}>Chief Examiner's Report</Highlight>. It's published by the SEC and literally tells you the most common mistakes students make. It's the closest thing to a cheat sheet you'll ever get.</p>
              <CommandWordDecoder />
              <MicroCommitment theme={theme}><p>Go to the SEC website (examinations.ie), find the most recent Chief Examiner's Report for your favourite subject, and read only the "Recommendations to Candidates" section. It takes five minutes and it's genuinely eye-opening.</p></MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="Exam Day: Your Game Plan." eyebrow="Step 6" icon={HeartPulse} theme={theme}>
              <p>All the studying in the world won't help if you fall apart on the day. The exam hall is stressful, and knowing how to manage yourself physically and mentally is just as important as knowing the content.</p>
              <p>Start with the <Highlight description="When you sit down, take 30 seconds to breathe slowly and calm your nerves. Then scribble down key formulas, quotes, or facts onto your rough work page before you forget them. This frees up your brain to focus on answering." theme={theme}>"First 5 Minutes" trick</Highlight> -- breathe, then brain-dump your key facts onto rough paper. Stick to a <Highlight description="Give each question a set amount of time and move on when it's up, no matter what. The first few marks on the next question are always easier to pick up than squeezing out the last marks on the current one." theme={theme}>strict timing plan</Highlight> -- when time's up on a question, move on. The first marks on the next question are always easier to get than the last marks on the one you're stuck on.</p>
              <ExamDayTimelineBuilder />
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default LeavingCertStrategyModule;
