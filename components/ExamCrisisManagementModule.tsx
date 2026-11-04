import { BrandedBreathingView,BrandedCognitionView } from './learning/WideFeatures';
import { moduleFill,moduleText } from './learning/brandTokens';
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import { AnimatePresence } from 'framer-motion';
import { Cpu,Flag,Moon,Shield,Utensils,Zap } from 'lucide-react';
import React,{ useState } from 'react';
import { EXAM_CRISIS_MANAGEMENT_REFERENCE_LIST } from '../data/references/examCrisisManagement';
import { COLORS } from '../design/tokens';
import { useEssentialsMode } from '../hooks/useEssentialsMode';
import { skyTheme } from '../moduleThemes';
import { type ModuleProgress } from '../types';
import { ModuleLayout } from './ModuleLayout';
import { Cite } from './ModuleReferences';
import { Highlight,MicroCommitment,PersonalStory,ReadingSection,SupportSignpost } from './ModuleShared';
import { MotionDiv } from './Motion';

const theme = skyTheme;

// --- INTERACTIVE COMPONENTS ---
const CognitionShiftVisualizer = () => {
    const [stress, setStress] = useState(20);

    // Yerkes-Dodson: performance peaks around 45, collapses after 70
    const perf = stress <= 45
        ? 0.15 + (stress / 45) * 0.85
        : Math.max(0.05, 1.0 - ((stress - 45) / 55) * 1.1);
    const pfcPct = Math.max(5, Math.round((1 - stress / 100) * 100));
    const amygPct = Math.max(5, Math.round((stress / 100) * 100));

    const stages = [
        { min: 0, max: 15, label: 'Calm', desc: 'Too relaxed. You\'re chilled out but not switched on — not enough energy to perform.', color: moduleText(COLORS.success), zone: 'low' as const },
        { min: 15, max: 35, label: 'Focused', desc: 'A bit of stress is sharpening you up. Your thinking brain is fully in charge and your memory is working well.', color: moduleText(COLORS.success), zone: 'good' as const },
        { min: 35, max: 55, label: 'Optimal', desc: 'The sweet spot. Just the right amount of adrenaline — you\'re alert, fast, and accurate.', color: moduleText(COLORS.success), zone: 'good' as const },
        { min: 55, max: 72, label: 'Anxious', desc: 'Stress is tipping over. Your focus is narrowing. You re-read questions without taking them in.', color: "var(--module-muted)", zone: 'past' as const },
        { min: 72, max: 88, label: 'Panic', desc: 'Your alarm brain is taking over. Heart racing, shallow breathing. Your thinking brain is losing control.', color: "var(--module-danger-text)", zone: 'danger' as const },
        { min: 88, max: 101, label: 'Going Blank', desc: 'Full shutdown. You stare at the page and nothing comes. Your thinking brain has gone offline.', color: "var(--module-danger-text)", zone: 'danger' as const },
    ];
    const stage = stages.find(s => stress >= s.min && stress < s.max) || stages[stages.length - 1];

    return <BrandedCognitionView {...{stress,setStress,stage,perf,pfcPct,amygPct}} />;
};

const PhysiologicalSighGuide = () => {
    const [running, setRunning] = useState(false);
    const [cycle, setCycle] = useState(0);
    const [phase, setPhase] = useState<'idle' | 'inhale1' | 'inhale2' | 'exhale' | 'done'>('idle');
    const [progress, setProgress] = useState(0);
    const totalCycles = 3;

    // Phase durations in ms
    const durations = { inhale1: 1800, inhale2: 1000, exhale: 4000 };

    React.useEffect(() => {
        if (!running || phase === 'idle' || phase === 'done') return;
        const dur = durations[phase];
        const interval = 30;
        let elapsed = 0;
        const timer = setInterval(() => {
            elapsed += interval;
            setProgress(Math.min(1, elapsed / dur));
            if (elapsed >= dur) {
                clearInterval(timer);
                setProgress(0);
                if (phase === 'inhale1') setPhase('inhale2');
                else if (phase === 'inhale2') setPhase('exhale');
                else if (phase === 'exhale') {
                    if (cycle + 1 >= totalCycles) { setPhase('done'); setRunning(false); }
                    else { setCycle(c => c + 1); setPhase('inhale1'); }
                }
            }
        }, interval);
        return () => clearInterval(timer);
    }, [running, phase, cycle]);

    const start = () => { setCycle(0); setPhase('inhale1'); setProgress(0); setRunning(true); };
    const reset = () => { setRunning(false); setPhase('idle'); setCycle(0); setProgress(0); };

    const phaseConfig = {
        idle: { label: '', instruction: '', color: "var(--module-muted)", scale: 0.45 },
        inhale1: { label: 'Inhale', instruction: 'Breathe in through your nose', color: moduleText(COLORS.success), scale: 0.45 + progress * 0.35 },
        inhale2: { label: 'Inhale', instruction: 'Quick second sip of air', color: moduleText(COLORS.success), scale: 0.8 + progress * 0.2 },
        exhale: { label: 'Exhale', instruction: 'Slow exhale through your mouth', color: moduleText(COLORS.success), scale: 1.0 - progress * 0.55 },
        done: { label: '', instruction: '', color: moduleText(COLORS.success), scale: 0.45 },
    };
    const cfg = phaseConfig[phase];

    return <BrandedBreathingView {...{phase,cfg,progress,cycle,running,start,reset}} />;
};

type CrisisResponse = {
    text: string;
    quality: 'bad' | 'ok' | 'good';
    consequence: string;
    explanation: string;
};

type CrisisScenario = {
    situation: string;
    responses: CrisisResponse[];
};

const crisisScenarios: CrisisScenario[] = [
    {
        situation: "You open the exam paper. Question 1 is on a topic you barely revised.",
        responses: [
            {
                text: "Panic \u2014 read it again and again hoping it changes",
                quality: 'bad',
                consequence: "Thinking brain shuts down. Alarm brain takes over. You spiral.",
                explanation: "Stress hormones flood your system. Your ability to think shrinks. You can\u2019t focus on Q2\u2013Q6 either.",
            },
            {
                text: "Skip it and move on immediately",
                quality: 'ok',
                consequence: "Partial recovery. Anxiety lingers.",
                explanation: "Smart tactically, but you haven\u2019t calmed your body down. The anxiety follows you to Q2.",
            },
            {
                text: "Close your eyes. Take one deep double-breath. Then skip to your strongest question.",
                quality: 'good',
                consequence: "Thinking brain stays online. You stay in control.",
                explanation: "The breathing technique calms your nervous system in seconds. Starting with a strong question builds momentum. You can return to Q1 later with a clear head.",
            },
        ],
    },
    {
        situation: "You\u2019re halfway through an essay and realise you\u2019ve been answering the wrong question.",
        responses: [
            {
                text: "Scribble it all out and start over in a frenzy",
                quality: 'bad',
                consequence: "Thinking brain shuts down. Alarm brain takes over. You spiral.",
                explanation: "Panic wastes 5+ minutes. Your handwriting deteriorates. The examiner sees chaos.",
            },
            {
                text: "Keep going with the wrong answer \u2014 at least it\u2019s something",
                quality: 'bad',
                consequence: "Thinking brain shuts down. Alarm brain takes over. You spiral.",
                explanation: "You\u2019ll score near zero for relevance. The marking scheme rewards answering the actual question, not volume.",
            },
            {
                text: "Draw a single line through it. Take a breath. Start the correct answer on the next page.",
                quality: 'good',
                consequence: "Thinking brain stays online. You stay in control.",
                explanation: "A single line is neat and acceptable. You preserve time, composure, and the examiner\u2019s goodwill. Partial marks on the correct question beat full marks on the wrong one.",
            },
        ],
    },
    {
        situation: "Your mind goes completely blank on a question you definitely know.",
        responses: [
            {
                text: "Stare at the page harder until it comes back",
                quality: 'bad',
                consequence: "Thinking brain shuts down. Alarm brain takes over. You spiral.",
                explanation: "The harder you force it, the more blocked it becomes. Your brain interprets the blank as a threat and locks up even more.",
            },
            {
                text: "Write anything vaguely related and hope for the best",
                quality: 'ok',
                consequence: "Partial recovery. Anxiety lingers.",
                explanation: "You might accidentally jog your memory, but unstructured writing rarely scores well.",
            },
            {
                text: "Write the topic title. List 3 related keywords. Sketch a quick mind map in the margin.",
                quality: 'good',
                consequence: "Thinking brain stays online. You stay in control.",
                explanation: "Writing things down gives your brain something to latch onto. Related words trigger connected memories \u2014 it\u2019s like opening one drawer that leads to another, and the answer surfaces.",
            },
        ],
    },
    {
        situation: "You look at the clock and realise you have 20 minutes left but two full questions to answer.",
        responses: [
            {
                text: "Pick one question and write a perfect answer, skip the other",
                quality: 'bad',
                consequence: "Thinking brain shuts down. Alarm brain takes over. You spiral.",
                explanation: "Leaving a full question blank means zero marks. Your 8th paragraph on Q5 is worth way less than a first paragraph on Q6.",
            },
            {
                text: "Rush through both as fast as possible",
                quality: 'ok',
                consequence: "Partial recovery. Anxiety lingers.",
                explanation: "Better than skipping one, but panic-writing produces illegible, unstructured answers.",
            },
            {
                text: "Split the time: 10 minutes each. Write a clear introduction + 3 bullet-point arguments for each.",
                quality: 'good',
                consequence: "Thinking brain stays online. You stay in control.",
                explanation: "Structured bullet points with key terms score nearly as well as full paragraphs. The examiner can award marks for every valid point. Two partial answers beat one complete plus one blank.",
            },
        ],
    },
];

const CrisisScenarioTrainer = () => {
    const [scenarioIndex, setScenarioIndex] = useState(0);
    const [chosenIndex, setChosenIndex] = useState<number | null>(null);
    const [results, setResults] = useState<('bad' | 'ok' | 'good')[]>([]);
    const [finished, setFinished] = useState(false);

    const scenario = crisisScenarios[scenarioIndex];
    const chosenResponse = chosenIndex !== null ? scenario.responses[chosenIndex] : null;

    const handleChoose = (idx: number) => {
        if (chosenIndex !== null) return;
        setChosenIndex(idx);
    };

    const handleNext = () => {
        if (chosenResponse) {
            const newResults = [...results, chosenResponse.quality];
            setResults(newResults);
            if (scenarioIndex + 1 >= crisisScenarios.length) {
                setFinished(true);
            } else {
                setScenarioIndex(s => s + 1);
                setChosenIndex(null);
            }
        }
    };

    const handlePlayAgain = () => {
        setScenarioIndex(0);
        setChosenIndex(null);
        setResults([]);
        setFinished(false);
    };

    const optimalCount = results.filter(r => r === 'good').length;

    const consequenceStyle = (quality: 'bad' | 'ok' | 'good') => {
        if (quality === 'good') return { bg: COLORS.successTint, border: COLORS.success, text: COLORS.successDarkText, label: COLORS.successDarkText };
        if (quality === 'ok') return { bg: "var(--module-on-fill)", border: "var(--module-line)", text: "var(--module-ink)", label: "var(--module-ink)" };
        return { bg: "var(--module-ink)", border: "var(--module-line)", text: "var(--module-ink)", label: "var(--module-danger-text)" };
    };

    return <div className="wr-skin" data-wide="CrisisScenarioTrainer"><div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: "var(--module-surface)", borderRadius: 18 }}>
            <div className="text-center mb-8">
                <span className="inline-block px-3 py-1 rounded-full text-[11px] font-bold tracking-wider uppercase mb-3" style={{ backgroundColor: moduleFill(COLORS.accentTint), color: moduleText(COLORS.accentDarkText), border: '1px solid rgba(242,107,31,0.2)', letterSpacing: '0.06em' }}>Exam Skills Trainer</span>
                <h4 className="font-serif font-bold" style={{ fontSize: 24, color: "var(--module-ink)" }}>Crisis Scenario Trainer</h4>
                <p className="text-sm mt-1" style={{ color: "var(--module-muted)" }}>Your brain will default to its training. Build the right instincts now.</p>
            </div>

            <AnimatePresence mode="wait">
                {!finished ? (
                    <MotionDiv key={`scenario-${scenarioIndex}`} initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -16 }} transition={{ duration: 0.3 }}>
                        {/* Progress */}
                        <div className="flex items-center justify-between mb-6">
                            <span style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.12em', color: "var(--module-muted)", textTransform: 'uppercase' as const }}>Scenario {scenarioIndex + 1}/4</span>
                            <div className="flex gap-1.5">
                                {crisisScenarios.map((_, i) => (
                                    <div key={i} style={{ width: 10, height: 10, borderRadius: '50%', backgroundColor: moduleFill(i <= scenarioIndex ? COLORS.success : "var(--module-surface)"), transition: 'background-color 0.3s' }} />
                                ))}
                            </div>
                        </div>

                        {/* Scenario card */}
                        <div className="bg-[var(--module-surface)] dark:bg-[var(--module-surface)] mb-6 flex items-start gap-3" style={{ border: "2px solid var(--module-line)", borderRadius: 14, padding: '20px 24px' }}>

                            <div>
                                <span className="inline-block mb-2" style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.1em', backgroundColor: "var(--module-surface)", color: "var(--module-danger-text)", borderRadius: 20, padding: '3px 10px', textTransform: 'uppercase' as const }}>Crisis Scenario</span>
                                <p className="font-serif" style={{ fontSize: 17, color: "var(--module-ink)", lineHeight: 1.5 }}>{scenario.situation}</p>
                            </div>
                        </div>

                        {/* Options */}
                        <div className="space-y-3 mb-4">
                            {scenario.responses.map((response, idx) => {
                                const isChosen = chosenIndex === idx;
                                const isRevealed = chosenIndex !== null;
                                const cs = consequenceStyle(response.quality);

                                return (
                                    <div key={idx}>
                                        <button onClick={() => handleChoose(idx)} disabled={isRevealed} className="w-full text-left p-4 transition-all duration-200" style={
                                            isRevealed
                                                ? isChosen
                                                    ? response.quality === 'good'
                                                        ? { backgroundColor: moduleFill(COLORS.successTint), border: `2px solid ${COLORS.success}`, borderRadius: 14 }
                                                        : response.quality === 'bad'
                                                            ? { backgroundColor: "var(--module-surface)", border: "2px solid var(--module-line)", borderRadius: 14 }
                                                            : { backgroundColor: "var(--module-surface)", border: "2px solid var(--module-line)", borderRadius: 14 }
                                                    : { backgroundColor: "var(--module-surface)", border: "2px solid var(--module-line)", borderRadius: 14, opacity: 0.4 }
                                                : { backgroundColor: "var(--module-surface)", border: "2px solid var(--module-line)", borderRadius: 14, cursor: 'pointer' }
                                        } data-wide-button="true" data-selected={chosenIndex === idx} data-tone={response.quality === 'good' ? 'mint' : response.quality === 'bad' ? 'coral' : 'orange'} aria-pressed={chosenIndex === idx}>
                                            <div className="flex items-start gap-3">
                                                <span className="wr-answer-letter flex-shrink-0" style={{
                                                    backgroundColor: moduleFill(isRevealed && isChosen
                                                        ? response.quality === 'good' ? COLORS.success : response.quality === 'bad' ? "var(--module-danger)" : "var(--module-muted)"
                                                        : "var(--module-surface)"),
                                                    color: moduleText(isRevealed && isChosen ? "var(--module-on-fill)" : "var(--module-muted)"),
                                                }}>
                                                    {String.fromCharCode(65 + idx)}
                                                </span>
                                                <span style={{ fontSize: 14, fontWeight: 500, color: moduleText(isRevealed && !isChosen ? "var(--module-muted)" : "var(--module-ink)") }}>{response.text}</span>
                                            </div>
                                        </button>

                                        <AnimatePresence>
                                            {isChosen && isRevealed && (
                                                <MotionDiv initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} exit={{ opacity: 0, height: 0 }} transition={{ duration: 0.35, ease: 'easeOut' }} className="overflow-hidden">
                                                    <div className="mt-2" style={{ borderLeft: `3px solid ${cs.border}`, backgroundColor: moduleFill(cs.bg), borderRadius: '0 10px 10px 0', padding: '16px 20px' }}>
                                                        <p className="font-semibold text-sm mb-1" style={{ color: moduleText(cs.label) }}>{response.consequence}</p>
                                                        <p className="text-sm leading-relaxed" style={{ color: moduleText(cs.text) }}>{response.explanation}</p>
                                                    </div>
                                                </MotionDiv>
                                            )}
                                        </AnimatePresence>
                                    </div>
                                );
                            })}
                        </div>

                        <AnimatePresence>
                            {chosenIndex !== null && (
                                <MotionDiv initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3, duration: 0.25 }} className="flex justify-end mt-6">
                                    <button onClick={handleNext} style={{ backgroundColor: moduleFill(COLORS.accent), borderRadius: 20, padding: '12px 24px', fontSize: 14, fontWeight: 600, color: "var(--module-on-fill)" }} data-wide-button="true">
                                        {scenarioIndex + 1 >= crisisScenarios.length ? 'See Results' : 'Next Scenario'}
                                    </button>
                                </MotionDiv>
                            )}
                        </AnimatePresence>
                    </MotionDiv>
                ) : (
                    <MotionDiv key="results" initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -16 }} transition={{ duration: 0.35 }} className="text-center">
                        <div className="mb-6">
                            <div className="inline-flex items-center justify-center w-20 h-20 rounded-full mb-4" style={{ backgroundColor: moduleFill(COLORS.successTint) }}>
                                <span className="font-serif font-bold" style={{ fontSize: 28, color: moduleText(COLORS.success) }}>{optimalCount}/4</span>
                            </div>
                            <p className="font-serif font-semibold text-lg mb-1" style={{ color: "var(--module-ink)" }}>{optimalCount}/4 optimal responses</p>
                        </div>

                        <div className="mb-6" style={
                            optimalCount === 4
                                ? { borderLeft: `3px solid ${COLORS.success}`, backgroundColor: moduleFill(COLORS.successTint), borderRadius: '0 10px 10px 0', padding: '16px 20px', textAlign: 'left' }
                                : optimalCount >= 2
                                    ? { borderLeft: "3px solid var(--module-line)", backgroundColor: "var(--module-surface)", borderRadius: '0 10px 10px 0', padding: '16px 20px', textAlign: 'left' }
                                    : { borderLeft: "3px solid var(--module-line)", backgroundColor: "var(--module-surface)", borderRadius: '0 10px 10px 0', padding: '16px 20px', textAlign: 'left' }
                        }>
                            <p className="text-sm leading-relaxed" style={{ color: moduleText(optimalCount === 4 ? COLORS.successDarkText : optimalCount >= 2 ? "var(--module-ink)" : "var(--module-danger-text)") }}>
                                {optimalCount === 4 ? "You\u2019ve built exam-crisis muscle memory. When panic hits, your training will take over." : optimalCount >= 2 ? "Good instincts, but some panic responses slipped through. Review the scenarios where you chose poorly." : "Under pressure, your brain defaulted to panic. That\u2019s exactly why we practice. Run through these again."}
                            </p>
                        </div>

                        <div className="flex justify-center gap-2 mb-6">
                            {results.map((r, i) => (
                                <div key={i} className="w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold" style={{
                                    backgroundColor: moduleFill(r === 'good' ? COLORS.success : r === 'ok' ? "var(--module-muted)" : "var(--module-danger)"),
                                    color: "var(--module-on-fill)",
                                }}>{i + 1}</div>
                            ))}
                        </div>

                        <button onClick={handlePlayAgain} style={{ backgroundColor: moduleFill(COLORS.accent), borderRadius: 20, padding: '12px 24px', fontSize: 14, fontWeight: 600, color: "var(--module-on-fill)" }} data-wide-button="true">Play Again</button>
                    </MotionDiv>
                )}
            </AnimatePresence>
        </div></div>;
};

// --- MODULE COMPONENT ---
const ExamCrisisManagementModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const essentials = useEssentialsMode();
  const sections = [
    { id: 'anatomy-of-blank', title: 'Why You "Go Blank"', eyebrow: '01 // Stress vs. Your Brain', icon: Cpu },
    { id: 'blank-mind-protocol', title: 'The "Blank Mind" Fix', eyebrow: '02 // Body-Based Fixes', icon: Zap },
    { id: 'social-containment', title: 'Protect Your Head After Exams', eyebrow: '03 // The Post-Exam Trap', icon: Shield },
    { id: 'cognitive-athlete-sleep', title: 'Sleep: Your Secret Weapon', eyebrow: '04 // Sleep for Exams', icon: Moon },
    { id: 'cognitive-athlete-nutrition', title: 'Food and Focus', eyebrow: '05 // Eating for Exam Day', icon: Utensils },
        { id: 'implementation', title: 'The 7-Day Countdown', eyebrow: '06 // Your Final Week Plan', icon: Flag },
  ];

  return (
    <ModuleLayout
      moduleNumber="05"
      moduleTitle="Exam Crisis Management"
      moduleSubtitle="Your Exam Survival Guide"
      moduleDescription={`Understand why your brain freezes under pressure and learn practical techniques to stay calm, think clearly, and bounce back when things go wrong in an exam.`}
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      references={EXAM_CRISIS_MANAGEMENT_REFERENCE_LIST}
      finishButtonText="Stay in Control"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="Why You 'Go Blank'." eyebrow="Step 1" icon={Cpu} theme={theme}>
              {essentials ? (
                <>
                  <p>Going blank is not stupidity. It is a physical stress response. Your alarm brain hijacks your thinking brain.<Cite n={1} /> Your memory is still there. The connection is just temporarily cut off.</p>
                  <p>Understanding this is the first step. Once you know what is happening, you can use the tools in this module to stay in control. Try the simulator and scenario trainer below.</p>
                </>
              ) : (
                <>
                  <p>Going "blank" in an exam isn't you being stupid or unprepared. It's a physical stress response. Your brain's alarm system hijacks its thinking centre. To beat it, you need to understand the two modes your brain works in: <Highlight description="Your calm, clear-headed mode. The thinking part of your brain is in charge, so you can reason things out and pull information from memory easily." theme={theme}>Cold Cognition</Highlight> and <Highlight description="Your stressed, panicky mode. The alarm part of your brain takes over, shutting down clear thinking and blocking your access to memories you definitely have." theme={theme}>Hot Cognition</Highlight>.</p>
                  <p>When you see a question you don't know, your brain can treat it as a threat. This triggers a <Highlight description="When your alarm brain hijacks your thinking brain. Stress hormones flood your system and cut the connection to your memory. You know the stuff -- you just can't reach it." theme={theme}>brain hijack</Highlight>, switching you from "cold" to "hot" mode. Your memory isn't gone; the connection is just temporarily cut off.<Cite n={1} /> This isn't a knowledge problem; it's a wiring problem.</p>
                  <PersonalStory name="Roisin" role="6th Year, Limerick" junior={{ name: 'Roisin', role: '3rd Year, Limerick', children: (
                    <p>In a History class test, I opened the paper and my mind just went completely white. I'd studied for weeks but I couldn't remember a single date. I sat there for ages just staring. Afterwards I was in bits -- I thought there was something wrong with me. Turns out it's just what stress does to your brain. Once I learned that, it stopped scaring me so much. In my Junior Cert, the same thing started to happen, but this time I knew what it was and I had a plan.</p>
                  ) }}>
                    <p>In my mocks, I opened the History paper and my mind just went completely white. I'd studied for weeks but I couldn't remember a single date. I sat there for about ten minutes just staring. Afterwards I was in bits -- I thought there was something wrong with me. Turns out it's just what stress does to your brain. Once I learned that, it stopped scaring me so much. In the real exam, the same thing started to happen, but this time I knew what it was and I had a plan.</p>
                  </PersonalStory>
                </>
              )}
              <CognitionShiftVisualizer />
              <CrisisScenarioTrainer />
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The 'Blank Mind' Fix." eyebrow="Step 2" icon={Zap} theme={theme}>
                {essentials ? (
                  <p>The fix is physical, not mental. Use the Physiological Sigh: two quick nose inhales, one long mouth exhale.<Cite n={2} /> Then ground yourself by noticing what you can see and hear. Then start with the easiest question on the paper. Practice below.</p>
                ) : (
                  <>
                    <p>Since the problem is physical, the fix has to be physical too. You can't "think" your way out of a panic because the thinking part of your brain is offline. You need to use your body to send a "you're safe" signal to your brain. The idea is simple: <Highlight description="Using your body (like your breathing) to calm your mind, instead of trying to think your way out of panic. Your body can reset your brain faster than your thoughts can." theme={theme}>calm the body first, and the mind follows</Highlight>.</p>
                    <p>The fastest way to do this is the <Highlight description="A quick breathing trick: two short inhales through your nose, then one long exhale through your mouth. It forces your nervous system to calm down in seconds. Think of it as a hard reset button." theme={theme}>Physiological Sigh</Highlight>.<Cite n={2} /> It's your "hard reset" button. Once the panic wave passes, you bring your thinking brain back online with a <Highlight description="The 5-4-3-2-1 trick: name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, and 1 you can taste. It pulls your brain out of the panic loop and back into the real world." theme={theme}>Sensory Grounding</Highlight> exercise. Finally, you get your brain moving again with an <Highlight description="Find the easiest question on the paper and answer it first. That small success gives your brain a confidence boost and helps clear the stress fog so you can tackle the harder stuff." theme={theme}>'Easy Win'</Highlight>.</p>
                  </>
                )}
                <PhysiologicalSighGuide/>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="Protect Your Head After Exams." eyebrow="Step 3" icon={Shield} theme={theme}>
              {essentials ? (
                <p>Do not compare answers after an exam. Other people's panic is contagious.<Cite n={3} /> Put headphones in, walk away, and protect your energy for the next paper. The exam is done. Let it go.</p>
              ) : (
                <>
                  <p>The crisis doesn't end when you put your pen down. The minutes after an exam are a minefield of <Highlight description="When other people's stress rubs off on you. Standing around after an exam while everyone panics about answers is one of the fastest ways to wreck your head before the next paper." theme={theme}>catching other people's anxiety</Highlight>.<Cite n={3} /> Discussing answers with stressed-out friends is one of the worst things you can do. It keeps your stress levels high and stops you recovering for the next exam.</p>
                  <p>That urge to compare answers? It's driven by your brain's <Highlight description="Your brain hates not knowing. After an exam, the uncertainty is torture -- so your brain desperately wants to compare answers to close the loop. But doing that almost always makes you feel worse, not better." theme={theme}>desperation for answers</Highlight>. You have to train yourself to sit with the uncertainty. This means having a strict <Highlight description="A personal rule: walk out of the exam hall and don't discuss the paper with anyone until the entire exam period is over. Put your headphones in, text a mate about something else, just get away from the chat." theme={theme}>"Post-Exam Ban"</Highlight> on discussing the paper. This isn't anti-social; it's protecting your energy for the next exam.</p>
                </>
              )}
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="Sleep: Your Secret Weapon." eyebrow="Step 4" icon={Moon} theme={theme}>
              {essentials ? (
                <p>Sleep is your brain's best recovery tool. Bank extra sleep the week before exams.<Cite n={4} /> Your brain cleans itself during sleep.<Cite n={5} /> Pulling an all-nighter skips that cleanup and leaves you foggy.</p>
              ) : (
                <>
                  <p>Think of the weeks before your big exams like a championship season. Your brain is the muscle that matters most right now. And sleep is the single best thing you can do for it.</p>
                  <p>In the week before exams, try <Highlight description="Getting an extra hour of sleep per night in the days before exams. It builds up a reserve so that if you sleep badly the night before a paper, you've got a buffer and your brain still works well." theme={theme}>sleep banking</Highlight> -- getting an extra hour of sleep per night. This builds a reserve that protects you if you sleep badly the night before a paper.<Cite n={4} /> While you sleep, your brain also runs its own <Highlight description="While you sleep, your brain literally flushes out the waste that builds up during the day -- the stuff that causes brain fog and makes it hard to concentrate. Pulling an all-nighter means skipping this clean-up." theme={theme}>cleaning cycle</Highlight>, flushing out the waste that causes brain fog.<Cite n={5} /> Pulling an all-nighter means skipping that clean-up entirely.</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Food and Focus." eyebrow="Step 5" icon={Utensils} theme={theme}>
              {essentials ? (
                <p>Eat slow-release food 3 hours before exams: porridge, wholegrain toast, eggs.<Cite n={6} /> Go easy on sugar and energy drinks -- they can leave your energy dipping partway through. Cut caffeine the week before so a normal cup on exam morning actually works.</p>
              ) : (
                <>
                  <p>Your brain runs on sugar from food, but it needs a steady supply, not a sugar rush. <Highlight description="Foods like sweets, white bread, and energy drinks that give you a quick spike of energy followed by a dip. That dip can land partway through your exam, just when you need to concentrate." theme={theme}>Quick-burn foods</Highlight> (sweets, white bread, energy drinks) can leave your energy dipping partway through, just when you need it most. A slower-release breakfast -- porridge, wholegrain toast, eggs, about 3 hours before -- is linked to steadier concentration in students through the morning.<Cite n={6} /></p>
                  <p>You can also use caffeine smartly. <Highlight description="Cutting back on coffee and energy drinks in the week before exams so that when you have a normal cup on exam morning, it actually hits properly instead of barely making a difference." theme={theme}>Caffeine tapering</Highlight> means cutting back on coffee and energy drinks in the week before exams. Then a normal cup on exam morning will actually wake you up properly. If tea is more your thing, many people find it a gentler lift than coffee.</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <></>
          )}
          {activeSection === 5 && (
            <ReadingSection title="The 7-Day Countdown." eyebrow="Step 6" icon={Flag} theme={theme}>
              {essentials ? (
                <p>7 days out: ease off energy drinks and fizzy drinks. 5 days out: fix your sleep to exam times. 3 days out: switch to steady-energy food. Day before: stop heavy study by 6pm. You are getting your brain ready to perform, not cramming more in.</p>
              ) : (
                <>
                  <p>This is where it all comes together. The final week before the exams is your countdown. Just like an athlete before a final, you ease off to let your body and mind recover and peak at the right moment. This is not the time for cramming.</p>
                  <p>Your 7-day countdown should include: <strong>Cut back on caffeine</strong> (7 days out), <strong>Fix your sleep schedule</strong> (5 days out -- start waking up at exam time), and <strong>Switch to steady-energy food</strong> (3 days out -- porridge, pasta, plenty of water). The day before the exam, stop all heavy study. You're not building knowledge any more; you're getting your brain ready to use what it already knows.</p>
                </>
              )}
              <SupportSignpost />
              <MicroCommitment theme={theme}>
                <p>Take out your phone. Find the date one week before your first exam. Set a reminder called "Start 7-Day Countdown." That's it -- you've just taken the first step.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default ExamCrisisManagementModule;
