import { BrandedHopeDiagnostic } from './learning/BrandedFeatures';
import { moduleFill,moduleText } from './learning/brandTokens';
import { BrandedBrainMismatch,BrandedCortisol } from './learning/WideFeatures';
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import { AnimatePresence,motion } from 'framer-motion';
import {
Activity,
BookOpen,
Cpu,
Shield,
Waypoints,
Zap
} from 'lucide-react';
import React,{ useState } from 'react';
import { HOPE_PROTOCOL_REFERENCE_LIST } from '../data/references/hopeProtocol';
import { useEssentialsMode } from '../hooks/useEssentialsMode';
import { useNorthStar } from '../hooks/useNorthStar';
import { emeraldTheme } from '../moduleThemes';
import { COMPACT_CALLOUT_PLACEMENTS } from '../northStarData';
import { type ModuleProgress } from '../types';
import { ModuleLayout } from './ModuleLayout';
import { Cite } from './ModuleReferences';
import { ConceptCardGrid,Highlight,MicroCommitment,ReadingSection } from './ModuleShared';
import NorthStarCallout from './NorthStarCallout';

const theme = emeraldTheme;

// --- INTERACTIVE COMPONENTS ---

const HopeDiagnostic = BrandedHopeDiagnostic

const BrainMismatchDiagram = BrandedBrainMismatch;

const DopamineDial = () => {
  const [motivation, setMotivation] = useState(10);
  const [choice, setChoice] = useState<'none' | 'cold' | 'hot'>('none');

  const handleChoice = (type: 'cold' | 'hot') => {
    setChoice(type);
    setMotivation(type === 'cold' ? 30 : 90);
  };

  const radius = 60;
  const circumference = Math.PI * radius; // Semicircle
  const offset = circumference - (motivation / 100) * circumference;

  return (
    <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: "var(--module-surface)", borderRadius: 18 }}>
      <h4 className="font-serif text-2xl font-semibold text-[var(--module-ink)] dark:text-[var(--module-ink)] text-center">Interactive: The Dopamine Dial</h4>
      <p className="text-center text-sm text-[var(--module-muted)] dark:text-[var(--module-muted)] mb-8">Scenario: You need to study for a history exam. Choose your thought process.</p>

      <div className="w-full flex justify-center items-end h-24">
        <svg width="160" height="80" viewBox="0 0 160 80" className="overflow-visible">
          <path d="M 20 80 A 60 60 0 0 1 140 80" fill="none" stroke="var(--module-on-fill)" strokeWidth="15" strokeLinecap="round" />
          <motion.path
            d="M 20 80 A 60 60 0 0 1 140 80"
            fill="none"
            stroke="url(#grad)"
            strokeWidth="15"
            strokeLinecap="round"
            strokeDasharray={circumference}
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset: offset }}
            transition={{ type: "spring", damping: 15, stiffness: 100 }}
          />
          <defs>
            <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" style={{stopColor: "var(--module-success)", stopOpacity:1}} />
              <stop offset="100%" style={{stopColor: "var(--module-success)", stopOpacity:1}} />
            </linearGradient>
          </defs>
        </svg>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-8">
        <button onClick={() => handleChoice('cold')} className="p-4 rounded-xl text-left text-sm font-medium" style={{ backgroundColor: moduleFill(choice === 'cold' ? "var(--module-surface)" : "var(--module-surface)"), border: `2.5px solid ${choice === 'cold' ? "var(--module-line)" : "var(--module-line)"}`, borderRadius: 14, boxShadow: 'none', color: moduleText(choice === 'cold' ? "var(--module-danger-text)" : "var(--module-ink)") }} data-wide-button="true" data-selected={!!(choice === 'cold')} data-tone="coral" aria-pressed={!!(choice === 'cold')}><strong>"Cold" Cognition:</strong> "I need to study history."</button>
        <button onClick={() => handleChoice('hot')} className="p-4 rounded-xl text-left text-sm font-medium" style={{ backgroundColor: moduleFill(choice === 'hot' ? "var(--module-success-soft)" : "var(--module-surface)"), border: `2.5px solid ${choice === 'hot' ? "var(--module-line)" : "var(--module-line)"}`, borderRadius: 14, boxShadow: 'none', color: moduleText(choice === 'hot' ? "var(--module-success-text)" : "var(--module-ink)") }} data-wide-button="true" data-selected={!!(choice === 'hot')} data-tone="mint" aria-pressed={!!(choice === 'hot')}><strong>"Hot" Cognition (EFT):</strong> "Imagine acing that exam..."</button>
      </div>

      <AnimatePresence>
        {choice !== 'none' && (
          <motion.div
            initial={{opacity:0, y:10}}
            animate={{opacity:1, y:0}}
            className="mt-8 p-6 rounded-xl"
            style={{
              backgroundColor: moduleFill(choice === 'cold' ? "var(--module-surface)" : "var(--module-success-soft)"),
              border: `2.5px solid ${choice === 'cold' ? "var(--module-line)" : "var(--module-line)"}`,
              boxShadow: 'none',
            }}
          >
            {choice === 'cold' && <p style={{ color: "var(--module-danger-text)" }}><strong>Result:</strong> A small motivational increase. The task is abstract and lacks an immediate reward signal for your brain.</p>}
            {choice === 'hot' && <p style={{ color: "var(--module-success-text)" }}><strong>Result:</strong> Major dopamine boost! Vividly simulating future success makes the reward feel real <em>now</em>, flooding your brain with the motivation to start.</p>}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

const HopeMap = () => {
  const [step, setStep] = useState(0);
  const [goal, setGoal] = useState('');
  const [pathway, setPathway] = useState('');
  const [obstacle, setObstacle] = useState('');
  const [solution, setSolution] = useState('');

  const steps = [
    { label: 'Goal', prompt: 'What is your goal?', hint: 'Be specific. Not "do well in Maths" but "Get a top grade in Maths by June."' },
    { label: 'Pathway', prompt: 'What is your first route to get there?', hint: 'The first concrete step or strategy. e.g., "Complete 3 past papers per week starting in January."' },
    { label: 'Obstacle', prompt: 'What could block this pathway?', hint: 'Be honest. What is the most likely thing to derail you? e.g., "I lose motivation after a bad result."' },
    { label: 'Solution', prompt: 'How will you get around it?', hint: 'Pre-load the fix. e.g., "If I get a bad result, I will review my mistakes and adjust my plan, not quit."' },
  ];

  const values = [goal, pathway, obstacle, solution];
  const setters = [setGoal, setPathway, setObstacle, setSolution];
  const canAdvance = values[step]?.trim().length > 0;
  const isComplete = step === 4;

  return (
    <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: "var(--module-surface)", borderRadius: 18 }}>
      <h4 className="font-serif text-2xl font-semibold text-[var(--module-ink)] dark:text-[var(--module-ink)] text-center">My Hope Circuit Blueprint</h4>
      <p className="text-center text-sm text-[var(--module-muted)] dark:text-[var(--module-muted)] mb-8">Build your circuit one component at a time.</p>

      {/* Progress dots */}
      <div className="flex justify-center gap-2 mb-8">
        {steps.map((s, i) => (
          <div key={i} className="flex items-center gap-2">
            <div
              className="w-8 h-8 flex items-center justify-center text-xs font-bold transition-all duration-300"
              style={{
                borderRadius: 10,
                backgroundColor: moduleFill(i < step || isComplete ? "var(--module-success)" : i === step && !isComplete ? "var(--module-success-soft)" : "var(--module-surface)"),
                border: `2px solid ${i < step || isComplete ? "var(--module-line)" : i === step && !isComplete ? "var(--module-line)" : "var(--module-line)"}`,
                boxShadow: 'none',
                color: moduleText(i < step || isComplete ? "var(--module-on-fill)" : i === step && !isComplete ? "var(--module-success-text)" : "var(--module-muted)"),
              }}
            >
              {i < step || isComplete ? '✓' : i + 1}
            </div>
            {i < steps.length - 1 && (
              <div className="w-8 h-0.5 transition-all duration-300" style={{ backgroundColor: moduleFill(i < step || isComplete ? "var(--module-success)" : "var(--module-surface)") }} />
            )}
          </div>
        ))}
      </div>

      <AnimatePresence mode="wait">
        {!isComplete ? (
          <motion.div
            key={step}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.3 }}
            className="space-y-4"
          >
            <p className="text-xs font-semibold text-[var(--module-success-text)] uppercase tracking-wider">{steps[step].label}</p>
            <p className="font-serif text-xl font-semibold text-[var(--module-ink)] dark:text-[var(--module-ink)]">{steps[step].prompt}</p>
            <p className="text-sm text-[var(--module-muted)] dark:text-[var(--module-muted)]">{steps[step].hint}</p>
            <input
              value={values[step]}
              onChange={(e) => setters[step](e.target.value)}
              placeholder="Type your answer here..."
              className="w-full bg-[var(--module-surface)] dark:bg-[var(--module-surface)] rounded-xl px-5 py-3.5 text-sm font-medium text-[var(--module-ink)] dark:text-[var(--module-ink)] placeholder-zinc-400 outline-none"
              style={{ border: "1.5px solid var(--module-line)" }}
              autoFocus
            />
            <div className="flex justify-between items-center pt-2">
              <button
                onClick={() => setStep(step - 1)}
                className={`text-sm font-medium text-zinc-400 hover:text-zinc-600 transition-colors ${step === 0 ? 'invisible' : ''}`} data-wide-button="true"
              >
                Back
              </button>
              <button
                onClick={() => setStep(step + 1)}
                disabled={!canAdvance}
                className={`px-6 py-2.5 rounded-xl text-sm font-bold transition-all ${
                  canAdvance
                    ? "bg-[var(--module-success)] text-[var(--module-ink)] hover:bg-[var(--module-success)] shadow-none shadow-none"
                    : "bg-[var(--module-surface)] dark:bg-[var(--module-surface)] text-[var(--module-muted)] cursor-not-allowed"
                }`} data-wide-button="true" data-selected={!!(canAdvance)} data-tone="mint" aria-pressed={!!(canAdvance)}
              >
                {step === 3 ? 'Complete Blueprint' : 'Next'}
              </button>
            </div>
          </motion.div>
        ) : (
          <motion.div
            key="complete"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.4 }}
            className="space-y-4"
          >
            <div className="bg-[var(--module-surface)] dark:bg-[var(--module-surface)] rounded-2xl" style={{ border: "2.5px solid var(--module-line)", boxShadow: 'none', padding: '24px 28px' }}>
              {/* Step 1: Power Source */}
              <div className="flex items-start gap-4">
                <div className="w-11 h-11 shrink-0 flex items-center justify-center" style={{ backgroundColor: "var(--module-surface)", border: "2px solid var(--module-line)", borderRadius: 12, boxShadow: 'none' }}>
                  <Zap size={18} style={{ color: "var(--module-danger-text)" }} />
                </div>
                <div className="pt-0.5">
                  <p className="text-[10px] uppercase tracking-wider font-semibold" style={{ color: "var(--module-muted)" }}>The Power Source</p>
                  <p className="font-serif font-semibold text-[var(--module-ink)] dark:text-[var(--module-ink)] mt-0.5">{goal}</p>
                </div>
              </div>
              <div className="h-5 flex items-center" style={{ marginLeft: 21 }}><div className="w-0.5 h-full bg-[var(--module-surface)] dark:bg-[var(--module-surface)]" /></div>

              {/* Step 2: Wiring */}
              <div className="flex items-start gap-4">
                <div className="w-11 h-11 shrink-0 flex items-center justify-center" style={{ backgroundColor: "var(--module-surface)", border: "2px solid var(--module-line)", borderRadius: 12, boxShadow: 'none' }}>
                  <Waypoints size={18} style={{ color: "var(--module-ink)" }} />
                </div>
                <div className="pt-0.5">
                  <p className="text-[10px] uppercase tracking-wider font-semibold" style={{ color: "var(--module-muted)" }}>The Wiring</p>
                  <p className="font-serif font-semibold text-[var(--module-ink)] dark:text-[var(--module-ink)] mt-0.5">{pathway}</p>
                </div>
              </div>
              <div className="h-5 flex items-center" style={{ marginLeft: 21 }}><div className="w-0.5 h-full bg-[var(--module-surface)] dark:bg-[var(--module-surface)]" /></div>

              {/* Step 3: Short Circuit */}
              <div className="flex items-start gap-4">
                <div className="w-11 h-11 shrink-0 flex items-center justify-center" style={{ backgroundColor: "var(--module-surface)", border: "2px solid var(--module-line)", borderRadius: 12, boxShadow: 'none' }}>
                  <Shield size={18} style={{ color: "var(--module-danger-text)" }} />
                </div>
                <div className="pt-0.5">
                  <p className="text-[10px] uppercase tracking-wider font-semibold" style={{ color: "var(--module-muted)" }}>Short Circuit</p>
                  <p className="font-serif font-semibold text-[var(--module-ink)] dark:text-[var(--module-ink)] mt-0.5">{obstacle}</p>
                </div>
              </div>
              <div className="h-5 flex items-center" style={{ marginLeft: 21 }}><div className="w-0.5 h-full bg-[var(--module-surface)] dark:bg-[var(--module-surface)]" /></div>

              {/* Step 4: The Fix */}
              <div className="flex items-start gap-4">
                <div className="w-11 h-11 shrink-0 flex items-center justify-center" style={{ backgroundColor: "var(--module-success-soft)", border: "2px solid var(--module-line)", borderRadius: 12, boxShadow: 'none' }}>
                  <Activity size={18} style={{ color: "var(--module-success-text)" }} />
                </div>
                <div className="pt-0.5">
                  <p className="text-[10px] uppercase tracking-wider font-semibold" style={{ color: "var(--module-muted)" }}>The Fix</p>
                  <p className="font-serif font-semibold text-[var(--module-ink)] dark:text-[var(--module-ink)] mt-0.5">{solution}</p>
                </div>
              </div>
            </div>
            <button
              onClick={() => { setStep(0); setGoal(''); setPathway(''); setObstacle(''); setSolution(''); }}
              className="w-full text-center text-sm font-medium text-[var(--module-muted)] hover:text-[var(--module-ink)] hover:underline transition-colors pt-2" data-wide-button="true"
            >
              Start a new blueprint
            </button>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

const CortisolSimulator = BrandedCortisol

// --- MODULE COMPONENT ---
const HopeProtocolModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const essentials = useEssentialsMode();
  const { northStar } = useNorthStar();
  const sections = [
    { id: 'schematic', title: 'The Schematic: De-Coding Hope', eyebrow: '01 // The Blueprint', icon: BookOpen },
    { id: 'circuit-board', title: "Your Brain's Circuit Board", eyebrow: '02 // The Hardware', icon: Cpu },
    { id: 'willpower', title: "Powering Up: The Science of 'Willpower'", eyebrow: '03 // The Voltage', icon: Zap },
    { id: 'waypower', title: "Designing the Wires: The Art of 'Waypower'", eyebrow: '04 // The Wiring', icon: Waypoints },
    { id: 'stress-shield', title: 'Stress Shield: Your Surge Protector', eyebrow: '05 // System Protection', icon: Shield },
    { id: 'upgrade', title: 'Upgrading the Hardware', eyebrow: '06 // System Upgrade', icon: Activity },
  ];

  return (
    <ModuleLayout
      moduleNumber="02"
      moduleTitle="The Science of Hope"
      moduleSubtitle="Your Brain's Engineering Manual"
      moduleDescription="Hope isn't wishful thinking — it's a skill you can train. Learn how your brain creates motivation and how to get it working for you."
      theme={theme}
      sections={sections}
      references={HOPE_PROTOCOL_REFERENCE_LIST}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Ignite Your Hope"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Schematic: De-Coding Hope." eyebrow="Step 1" icon={BookOpen} theme={theme}>
              {essentials ? (<>
              <p>Hope is a skill you can train. It has a simple formula: Hope = Goals + <Highlight description="Your willpower — the raw 'I can do this' energy that gets you off the couch and started. It's the spark that fires up your engine." theme={theme}>Agency</Highlight> (your drive to start) + <Highlight description="Your waypower — the ability to come up with a plan, think of backup routes, and adapt when things go sideways. It's the sat-nav that keeps you on course." theme={theme}>Pathways</Highlight> (your plan to get there).<Cite n={1} /> You can practise and improve each part. Try the diagnostic below to see where you are strong.</p>
              </>) : (<>
              <p>Forget everything you think you know about hope. It's not a fluffy feeling or wishful thinking. Hope is actually a skill — a way of thinking that you can learn, practise, and get seriously good at. Think of it as the engineering manual for your brain's motivation system.</p>
              <p>The formula is simple: Hope = Goals + <Highlight description="Your willpower — the raw 'I can do this' energy that gets you off the couch and started. It's the spark that fires up your engine." theme={theme}>Agency</Highlight> + <Highlight description="Your waypower — the ability to come up with a plan, think of backup routes, and adapt when things go sideways. It's the sat-nav that keeps you on course." theme={theme}>Pathways</Highlight>.<Cite n={1} /> A quick diagnostic can help you see where your own circuit is strong and where it might need work.</p>
              </>)}
              <HopeDiagnostic />
              <MicroCommitment theme={theme}>
                <p>Think of one vague goal you have (e.g., 'do better in French'). Open the notes app on your phone and re-write it as a clear, specific goal (e.g., 'Learn 10 new French vocabulary words by tomorrow evening').</p>
              </MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="Your Brain's Circuit Board." eyebrow="Step 2" icon={Cpu} theme={theme}>
              {essentials ? (<>
              <p>Your brain has a <Highlight description="Your emotional brain (the accelerator) is already at full power, but your planning brain (the brakes) is still being built. That's why you can desperately want something but struggle to plan how to get it. It's not a flaw — it's just where your brain is at right now." theme={theme}>Developmental Mismatch</Highlight> right now. Your <Highlight description="The emotional engine room of your brain. It's what drives your desire for rewards, your excitement, and your impulses. In your teens, it's turned up to maximum — which gives you massive energy and motivation." theme={theme}>Limbic System</Highlight> (emotions, drive) is at full power. Your <Highlight description="The planning department of your brain, right behind your forehead. It handles long-term thinking, impulse control, and problem-solving. It's still under construction until your mid-20s — which is why planning feels harder than wanting." theme={theme}>Prefrontal Cortex</Highlight> (planning, brakes) is still being built.<Cite n={2} /> That is why wanting something feels easy but planning feels hard. It is not a character flaw. It is biology. Your job is to train the planning side.</p>
              </>) : (<>
              <p>Your brain right now is a high-tech circuit board undergoing a massive upgrade. But here's the catch: not all parts get upgraded at the same speed. This creates a <Highlight description="Your emotional brain (the accelerator) is already at full power, but your planning brain (the brakes) is still being built. That's why you can desperately want something but struggle to plan how to get it. It's not a flaw — it's just where your brain is at right now." theme={theme}>Developmental Mismatch</Highlight>.</p>
              <p>Your <Highlight description="The emotional engine room of your brain. It's what drives your desire for rewards, your excitement, and your impulses. In your teens, it's turned up to maximum — which gives you massive energy and motivation." theme={theme}>Limbic System</Highlight> (your 'accelerator') is already at full power, giving you huge amounts of energy and drive. But your <Highlight description="The planning department of your brain, right behind your forehead. It handles long-term thinking, impulse control, and problem-solving. It's still under construction until your mid-20s — which is why planning feels harder than wanting." theme={theme}>Prefrontal Cortex (PFC)</Highlight> (your 'brakes' and 'Sat-Nav') is still being built.<Cite n={2} /> This means your desire to succeed often outstrips your brain's ability to plan the route, leading to frustration. This isn't a character flaw — it's biology. Your job is to become a conscious engineer of this system.</p>
              </>)}
              <BrainMismatchDiagram />
               <MicroCommitment theme={theme}>
                <p>Next time you feel a strong impulse to procrastinate, just notice it. Say to yourself, "That's my limbic system." Don't judge it, just label it. This simple act of noticing engages your PFC.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="Powering Up: The Science of 'Willpower'." eyebrow="Step 3" icon={Zap} theme={theme}>
                {essentials ? (<>
                <p>Your brain's reward system drives motivation — and you can switch it on deliberately. Use <Highlight description="Imagining your future so vividly that it feels real. Picture yourself walking out of the exam hall, relieved and proud. That vivid image makes the future reward feel close, giving you the motivation to start now." theme={theme}>Episodic Future Thinking</Highlight>: vividly picture yourself succeeding. "I can see myself walking out of the exam, relieved and proud." Vividly imagining future success makes that reward feel real now, which boosts your motivation to start.<Cite n={3} /> Vague thoughts like "I should study" do not work. Make the picture specific and emotional.</p>
                </>) : (<>
                <p>Agency — your willpower — is the electrical current in your Hope Circuit. It's the force that gets you to actually start. And it's not just about 'trying hard'; your brain has a specific chemical for this called <Highlight description="Your brain's motivation chemical. It's what makes you feel driven and excited about goals. The trick is: you can learn to trigger it on demand by vividly imagining your future success." theme={theme}>Dopamine</Highlight>.</p>
                <p>Here's the key: there's a huge difference between "cold" and "hot" thinking. "Cold" thinking is vague and abstract ("I should study"). "Hot" thinking — or <Highlight description="Imagining your future so vividly that it feels real. Picture yourself walking out of the exam hall, relieved and proud. That vivid image fires up your brain's reward system right now, giving you the motivation to start." theme={theme}>Episodic Future Thinking</Highlight> — is vivid and emotional ("I can see myself walking out of that exam hall, relieved and proud"). That vivid image makes a future reward feel close and pulls your motivation forward to right now.<Cite n={3} /> You can literally learn to generate your own voltage.</p>
                </>)}
                <DopamineDial />
                <MicroCommitment theme={theme}>
                    <p>Before you start studying tonight, take 60 seconds. Close your eyes and vividly imagine the feeling of relief and pride after you finish. You're practicing Episodic Future Thinking and giving your motivation a small, upfront boost.</p>
                </MicroCommitment>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="Designing the Wires: The Art of 'Waypower'." eyebrow="Step 4" icon={Waypoints} theme={theme}>
              {northStar && (() => { const p = COMPACT_CALLOUT_PLACEMENTS.find(p => p.moduleId === 'hope-protocol'); return p ? <NorthStarCallout northStar={northStar} variant="compact" message={p.message} /> : null; })()}
              {essentials ? (<>
              <p>Pathways thinking means planning your route and having backup plans.<Cite n={1} /> It comes down to three skills: planning (break big goals into steps), flexibility (have a Plan B), and problem-solving (spot obstacles before they hit). The Hope Map below trains exactly this.</p>
              </>) : (<>
              <p>If Agency is the raw power, Pathways thinking is the wiring that directs it.<Cite n={1} /> It's the most important — and for teens, the hardest — part of the Hope Circuit, because it relies on the part of your brain that's still being built.</p>
              <p>Good waypower comes down to three skills.</p>
              </>)}
              <ConceptCardGrid
                cards={[
                  { number: 1, term: "Planning", description: "Breaking a big goal into small steps." },
                  { number: 2, term: "Flexibility", description: "Having backup routes when the first path doesn't work out." },
                  { number: 3, term: "Problem-Solving", description: "Seeing obstacles before they hit you and pre-loading solutions." },
                ]}
              />
              {!essentials && <p>The Hope Map below trains exactly this. It forces you to design your circuit before you turn on the power — and pre-loads solutions so failure doesn't knock you off course.</p>}
              <HopeMap />
              <MicroCommitment theme={theme}>
                <p>Map out one tiny goal for tomorrow using the Goal-Pathway-Obstacle format. E.g., Goal: Get homework done by 8 pm. Pathway: Start at 6 pm in the kitchen. Obstacle: My brother will be noisy. Solution: Put on headphones.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="Stress Shield: Your Surge Protector." eyebrow="Step 5" icon={Shield} theme={theme}>
              {essentials ? (<>
              <p>Stress floods your body with <Highlight description="Your body's stress chemical. A short burst helps you focus, but when it stays high for too long, it messes with your memory, your sleep, and your ability to think clearly. Basically, it shuts down the exact brain functions you need for exams." theme={theme}>Cortisol</Highlight>, which can impair clear thinking.<Cite n={4} /> Hope is your shield. When you have a goal and a plan, your brain treats exams as problems to solve, not disasters. Your stress drops. Your thinking stays sharp. See the simulator below.</p>
              </>) : (<>
              <p>Hopelessness isn't just a feeling — it has a physical effect on your body. When you face a threat (like a looming exam), your brain's alarm system — your <Highlight description="Your body's built-in stress alarm. When danger is detected, it fires off a chain reaction of hormones that flood you with stress chemicals. Useful if you're running from a bear. Less useful the night before your Maths paper." theme={theme}>Stress Response System</Highlight> — goes off, flooding you with the stress hormone <Highlight description="Your body's stress chemical. A short burst helps you focus, but when it stays high for too long, it messes with your memory, your sleep, and your ability to think clearly. Basically, it shuts down the exact brain functions you need for exams." theme={theme}>Cortisol</Highlight>. Chronically high cortisol impairs the memory and thinking you rely on for exams.<Cite n={4} /></p>
              <p>Here's the good news: hope acts as a built-in surge protector. When you have a clear goal and a plan, your brain sees a tough exam as a problem to solve — not a disaster. That lowers your stress levels and keeps your thinking brain online when you need it most. See for yourself how a hopeful response can physically change the stress in your body.</p>
              </>)}
              <CortisolSimulator/>
              <MicroCommitment theme={theme}>
                <p>The next time you feel exam stress, consciously name the feeling ('I am feeling stressed about Maths'). Acknowledging the signal is the first step any engineer takes to regulate a system.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="Upgrading the Hardware." eyebrow="Step 6" icon={Activity} theme={theme}>
              {essentials ? (<>
              <p>Your brain rewires itself based on what you practise. This is <Highlight description="Your brain's ability to rewire itself based on what you practise. Like a path through a field — the more you walk it, the clearer it gets. Every time you plan, set goals, or solve problems, you're literally building a stronger brain." theme={theme}>Neuroplasticity</Highlight>.<Cite n={5} /> Every time you plan, set goals, or solve problems, you build stronger <Highlight description="The major highway inside your brain that connects your planning centre to the rest of your thinking systems. The more you use it, the faster and stronger it gets — like upgrading from a country road to a motorway." theme={theme}>Planning Highways</Highlight> in your brain. Making a Hope Map is not just homework. You are physically upgrading your brain. Use the "Stop-Think" trick: set a reminder mid-study to ask "Is this the best use of my time right now?"</p>
              </>) : (<>
              <p>Here's the most powerful idea in this entire module: your brain's wiring isn't fixed. Every time you practise planning, goal-setting, or problem-solving, you physically strengthen the connections in your brain. This is called <Highlight description="Your brain's ability to rewire itself based on what you practise. Like a path through a field — the more you walk it, the clearer it gets. Every time you plan, set goals, or solve problems, you're literally building a stronger brain." theme={theme}>Neuroplasticity</Highlight>.<Cite n={5} /> The <Highlight description="The major highway inside your brain that connects your planning centre to the rest of your thinking systems. The more you use it, the faster and stronger it gets — like upgrading from a country road to a motorway." theme={theme}>Planning Highways</Highlight> in your brain work like muscles: the more you use them, the stronger they get.</p>
              <p>This means every time you make a Hope Map or break down a big task, you're not just getting work done — you're physically upgrading your brain. One of the best ways to train this is the 'Stop-Think' Protocol: a manual override for your brain's autopilot that forces you to engage the Hope Circuit.</p>
              </>)}
               <MicroCommitment theme={theme}>
                <p>Put a reminder on your phone for halfway through your study time tonight that just says 'STOP-THINK'. When it goes off, take 60 seconds to ask: "Is what I'm doing now the most effective way to reach my goal?"</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default HopeProtocolModule;
