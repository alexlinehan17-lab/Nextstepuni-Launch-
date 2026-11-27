import { BrandedHopeDiagnostic } from './learning/BrandedFeatures';
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
import React,{ useId,useState } from 'react';
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
import { AnswerGroup,AnswerLine,ExerciseLabel,ExerciseSheet } from './learning/Exercise';
import { Button,TextButton } from './ui/Button';
import { ChoiceTile } from './ui/Choice';
import { Field } from './ui/Field';

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
    <ExerciseSheet title="Interactive: The Dopamine Dial" sub="Scenario: You need to study for a history exam. Choose your thought process." name="DopamineDial">
      {/* The dial: a hairline track, the student's own motivation in orange */}
      <div className="w-full flex justify-center items-end h-24">
        <svg width="160" height="80" viewBox="0 0 160 80" className="overflow-visible" aria-hidden="true">
          <path d="M 20 80 A 60 60 0 0 1 140 80" fill="none" stroke="var(--hairline)" strokeWidth="15" strokeLinecap="round" />
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
              <stop offset="0%" style={{stopColor: "var(--nsu-orange)", stopOpacity:1}} />
              <stop offset="100%" style={{stopColor: "var(--nsu-orange)", stopOpacity:1}} />
            </linearGradient>
          </defs>
        </svg>
      </div>

      <AnswerGroup kind="one">
        <ChoiceTile chosen={choice === 'cold'} onClick={() => handleChoice('cold')} label={<><strong>"Cold" Cognition:</strong> "I need to study history."</>} />
        <ChoiceTile chosen={choice === 'hot'} onClick={() => handleChoice('hot')} label={<><strong>"Hot" Cognition (EFT):</strong> "Imagine acing that exam..."</>} />
      </AnswerGroup>

      <AnimatePresence>
        {choice !== 'none' && (
          <motion.div
            initial={{opacity:0, y:10}}
            animate={{opacity:1, y:0}}
          >
            <AnswerLine tone={choice === 'hot' ? 'ok' : 'note'}>
              {choice === 'cold' && <span><strong>Result:</strong> A small motivational increase. The task is abstract and lacks an immediate reward signal for your brain.</span>}
              {choice === 'hot' && <span><strong>Result:</strong> Major dopamine boost! Vividly simulating future success makes the reward feel real <em>now</em>, flooding your brain with the motivation to start.</span>}
            </AnswerLine>
          </motion.div>
        )}
      </AnimatePresence>
    </ExerciseSheet>
  );
};

const HopeMap = () => {
  const [step, setStep] = useState(0);
  const [goal, setGoal] = useState('');
  const [pathway, setPathway] = useState('');
  const [obstacle, setObstacle] = useState('');
  const [solution, setSolution] = useState('');
  const promptId = useId();

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
    <ExerciseSheet title="My Hope Circuit Blueprint" sub="Build your circuit one component at a time." name="HopeMap">
      {/* Progress: step marks (the current one ink, done ones ticked, the rest a hairline ring) */}
      <ol className="ex-steps">
        {steps.map((s, i) => (
          <li key={i} className="flex items-center gap-2">
            <span className={`ex-badge${i < step || isComplete ? ' ex-badge--done' : i === step && !isComplete ? ' ex-badge--on' : ''}`}>
              {i < step || isComplete ? '✓' : i + 1}
            </span>
            {i < steps.length - 1 && (
              <span className={`block w-8 h-px ${i < step || isComplete ? 'bg-outline-strong' : 'bg-hairline'}`} aria-hidden="true" />
            )}
          </li>
        ))}
      </ol>

      <AnimatePresence mode="wait">
        {!isComplete ? (
          <motion.div
            key={step}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.3 }}
            className="ex-stack"
          >
            <div className="ex-head">
              <ExerciseLabel>{steps[step].label}</ExerciseLabel>
              <p id={promptId} className="t-heading text-ink-primary">{steps[step].prompt}</p>
              <p className="ex-sub">{steps[step].hint}</p>
            </div>
            <Field
              aria-labelledby={promptId}
              value={values[step]}
              onChange={(e) => setters[step](e.target.value)}
              placeholder="Type your answer here..."
              autoFocus
            />
            <div className="flex justify-between items-center">
              <TextButton
                tone="quiet"
                onClick={() => setStep(step - 1)}
                className={step === 0 ? 'invisible' : ''}
              >
                Back
              </TextButton>
              <Button
                onClick={() => setStep(step + 1)}
                {...{ disabled: !canAdvance }}
              >
                {step === 3 ? 'Complete Blueprint' : 'Next'}
              </Button>
            </div>
          </motion.div>
        ) : (
          <motion.div
            key="complete"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.4 }}
            className="ex-stack"
          >
            {/* The finished circuit: words you read, on the sheet with its wires, not in a box */}
            <div className="flex flex-col pt-3 border-t border-hairline">
              {/* Step 1: Power Source */}
              <div className="flex items-start gap-3">
                <span className="ex-icon w-6 justify-center pt-0.5"><Zap size={18} aria-hidden="true" /></span>
                <div className="flex flex-col gap-1">
                  <p className="ex-label">The Power Source</p>
                  <p className="t-row text-ink-primary">{goal}</p>
                </div>
              </div>
              <div className="h-5 flex items-center" style={{ marginLeft: 11.5 }}><div className="w-px h-full bg-outline-soft" /></div>

              {/* Step 2: Wiring */}
              <div className="flex items-start gap-3">
                <span className="ex-icon w-6 justify-center pt-0.5"><Waypoints size={18} aria-hidden="true" /></span>
                <div className="flex flex-col gap-1">
                  <p className="ex-label">The Wiring</p>
                  <p className="t-row text-ink-primary">{pathway}</p>
                </div>
              </div>
              <div className="h-5 flex items-center" style={{ marginLeft: 11.5 }}><div className="w-px h-full bg-outline-soft" /></div>

              {/* Step 3: Short Circuit */}
              <div className="flex items-start gap-3">
                <span className="ex-icon w-6 justify-center pt-0.5"><Shield size={18} aria-hidden="true" /></span>
                <div className="flex flex-col gap-1">
                  <p className="ex-label">Short Circuit</p>
                  <p className="t-row text-ink-primary">{obstacle}</p>
                </div>
              </div>
              <div className="h-5 flex items-center" style={{ marginLeft: 11.5 }}><div className="w-px h-full bg-outline-soft" /></div>

              {/* Step 4: The Fix */}
              <div className="flex items-start gap-3">
                <span className="ex-icon w-6 justify-center pt-0.5"><Activity size={18} aria-hidden="true" /></span>
                <div className="flex flex-col gap-1">
                  <p className="ex-label">The Fix</p>
                  <p className="t-row text-ink-primary">{solution}</p>
                </div>
              </div>
            </div>
            <div className="ex-actions">
              <TextButton
                tone="quiet"
                onClick={() => { setStep(0); setGoal(''); setPathway(''); setObstacle(''); setSolution(''); }}
              >
                Start a new blueprint
              </TextButton>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </ExerciseSheet>
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
