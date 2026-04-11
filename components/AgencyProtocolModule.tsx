/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence, Reorder } from 'framer-motion';
import {
  Target, Users, Settings, ShieldAlert, Zap, Map,
  Lightbulb, Activity, Brain, GripVertical,
  AlertTriangle, CheckCircle2, X, Star,
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { blueTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment, PersonalStory } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';
import { useModuleResponses } from '../hooks/useModuleResponses';
import { useNorthStar } from '../hooks/useNorthStar';
import NorthStarCallout from './NorthStarCallout';
import { COMPACT_CALLOUT_PLACEMENTS } from '../northStarData';

const theme = blueTheme;

/* ═══ Shared press-down spring config ═══ */
const press = { type: 'spring' as const, stiffness: 400, damping: 25 };

/* ═══════════════════════════════════════════════════════
   FlipCard — pastel front, teal back, hard offset shadow
   ═══════════════════════════════════════════════════════ */
const FLIP_COLORS = [
  { fill: '#93C5FD', border: '#2563EB', shadow: '#2563EB', text: '#1E3A8A', darkFill: '#1E3A5C' },
  { fill: '#FCD34D', border: '#D97706', shadow: '#D97706', text: '#78350F', darkFill: '#78350F' },
  { fill: '#6EE7B7', border: '#059669', shadow: '#059669', text: '#064E3B', darkFill: '#064E3B' },
];

const FlipCard = ({ front, back, frontIcon: FrontIcon, backIcon: _BackIcon, colorIndex = 0 }: { front: React.ReactNode, back: React.ReactNode, frontIcon: any, backIcon: any, colorIndex?: number }) => {
  const [isFlipped, setIsFlipped] = useState(false);
  const c = FLIP_COLORS[colorIndex % FLIP_COLORS.length];
  return (
    <motion.div
      className="w-full h-60 [perspective:1000px] cursor-pointer select-none"
      onClick={() => setIsFlipped(!isFlipped)}
      whileHover={{ x: -2, y: -2 }}
      whileTap={{ x: 2, y: 2 }}
      transition={press}
    >
      <motion.div
        className="relative w-full h-full"
        style={{ transformStyle: 'preserve-3d' }}
        animate={{ rotateY: isFlipped ? 180 : 0 }}
        transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
      >
        {/* Front */}
        <div
          className="absolute w-full h-full [backface-visibility:hidden] p-6 flex flex-col items-center justify-center text-center"
          style={{
            backgroundColor: c.fill,
            border: `2.5px solid ${c.border}`,
            borderRadius: 18,
            boxShadow: `4px 4px 0px 0px ${c.shadow}`,
          }}
        >
          <div className="w-11 h-11 rounded-xl flex items-center justify-center mb-3" style={{ backgroundColor: c.border }}>
            <FrontIcon size={20} style={{ color: '#fff' }} />
          </div>
          <p className="text-sm font-bold leading-snug" style={{ color: c.text }}>{front}</p>
          <div className="absolute bottom-3 left-0 right-0 flex justify-center">
            <span className="px-3 py-1 rounded-full text-[9px] font-bold uppercase tracking-wider text-white" style={{ backgroundColor: c.border }}>Tap to flip</span>
          </div>
        </div>
        {/* Back */}
        <div
          className="absolute w-full h-full [backface-visibility:hidden] p-6 flex flex-col items-center justify-center text-center"
          style={{
            transform: 'rotateY(180deg)',
            backgroundColor: '#2A7D6F',
            border: '2.5px solid #1F5F54',
            borderRadius: 18,
            boxShadow: '4px 4px 0px 0px #1F5F54',
          }}
        >
          <div className="w-11 h-11 rounded-xl flex items-center justify-center mb-3" style={{ backgroundColor: 'rgba(255,255,255,0.2)' }}>
            <Star size={20} style={{ color: '#fff' }} />
          </div>
          <p className="text-[9px] font-bold uppercase tracking-widest text-white/50 mb-1">Horsepower</p>
          <p className="text-sm font-bold leading-snug text-white">{back}</p>
        </div>
      </motion.div>
    </motion.div>
  );
};

/* ═══════════════════════════════════════════════════════
   MindsetSorter — chunky chips into coloured lanes
   ═══════════════════════════════════════════════════════ */
const MindsetSorter = () => {
  const initialThoughts = [
    { id: 1, text: "I'm useless at this subject.", type: 'passenger' },
    { id: 2, text: "My study method failed me.", type: 'driver' },
    { id: 3, text: "The teacher hates me.", type: 'passenger' },
    { id: 4, text: "What strategy can I try next?", type: 'driver' },
  ];

  const [thoughts, setThoughts] = useState(initialThoughts);
  const [passenger, setPassenger] = useState<typeof initialThoughts>([]);
  const [driver, setDriver] = useState<typeof initialThoughts>([]);
  const allSorted = thoughts.length === 0;

  const handleSort = (thought: typeof initialThoughts[0], lane: 'passenger' | 'driver') => {
    setThoughts(prev => prev.filter(t => t.id !== thought.id));
    if (lane === 'passenger') setPassenger(prev => [...prev, thought]);
    else setDriver(prev => [...prev, thought]);
  };

  return (
    <div className="my-14 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
      <div className="text-center mb-6">
        <h4 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white">Driver vs. Passenger</h4>
        <p className="text-sm text-zinc-500 mt-1">Sort each thought into the right lane</p>
      </div>

      {/* Drop zones */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="bg-white dark:bg-zinc-900" style={{ border: '2.5px solid #1C1917', borderRadius: 18, boxShadow: '4px 4px 0px 0px #1C1917', overflow: 'hidden' }}>
          <div style={{ backgroundColor: '#DC2626', padding: '10px 16px', borderBottom: '2.5px solid #1C1917' }}>
            <p className="text-[13px] font-medium tracking-wider uppercase text-white text-center">Passenger</p>
          </div>
          <div className="p-4 min-h-[100px]">
            <AnimatePresence>
              {passenger.map(p => (
                <motion.div key={p.id} initial={{ opacity: 0, scale: 0.8 }} animate={{ opacity: 1, scale: 1 }} className="text-center mb-2" style={{ backgroundColor: '#FFFFFF', border: '2px solid #DC2626', borderRadius: 12, boxShadow: '2px 2px 0px 0px #DC2626', padding: '8px 12px', fontSize: '13px', fontWeight: 700, color: '#7F1D1D' }}>
                  {p.text}
                </motion.div>
              ))}
            </AnimatePresence>
          </div>
        </div>
        <div className="bg-white dark:bg-zinc-900" style={{ border: '2.5px solid #1C1917', borderRadius: 18, boxShadow: '4px 4px 0px 0px #1C1917', overflow: 'hidden' }}>
          <div style={{ backgroundColor: '#059669', padding: '10px 16px', borderBottom: '2.5px solid #1C1917' }}>
            <p className="text-[13px] font-medium tracking-wider uppercase text-white text-center">Driver</p>
          </div>
          <div className="p-4 min-h-[100px]">
            <AnimatePresence>
              {driver.map(d => (
                <motion.div key={d.id} initial={{ opacity: 0, scale: 0.8 }} animate={{ opacity: 1, scale: 1 }} className="text-center mb-2" style={{ backgroundColor: '#FFFFFF', border: '2px solid #059669', borderRadius: 12, boxShadow: '2px 2px 0px 0px #059669', padding: '8px 12px', fontSize: '13px', fontWeight: 700, color: '#064E3B' }}>
                  {d.text}
                </motion.div>
              ))}
            </AnimatePresence>
          </div>
        </div>
      </div>

      {/* Thought chips */}
      <AnimatePresence>
        {thoughts.map(thought => (
          <motion.div
            key={thought.id}
            layout
            exit={{ opacity: 0, scale: 0.8, transition: { duration: 0.2 } }}
            className="mb-3 p-4 flex items-center justify-between gap-3"
            style={{
              backgroundColor: '#FFFFFF',
              border: '2.5px solid #1C1917',
              borderRadius: 14,
              boxShadow: '3px 3px 0px 0px #1C1917',
            }}
          >
            <p className="text-sm font-bold text-zinc-800 flex-1">&ldquo;{thought.text}&rdquo;</p>
            <div className="flex gap-2 shrink-0">
              <motion.button whileTap={{ scale: 0.9 }} onClick={() => handleSort(thought, 'passenger')} className="px-3 py-1.5 rounded-lg text-[10px] font-bold uppercase tracking-wider text-white" style={{ backgroundColor: '#DC2626' }}>
                <X size={12} className="inline -mt-0.5" />
              </motion.button>
              <motion.button whileTap={{ scale: 0.9 }} onClick={() => handleSort(thought, 'driver')} className="px-3 py-1.5 rounded-lg text-[10px] font-bold uppercase tracking-wider text-white" style={{ backgroundColor: '#059669' }}>
                <CheckCircle2 size={12} className="inline -mt-0.5" />
              </motion.button>
            </div>
          </motion.div>
        ))}
      </AnimatePresence>

      {allSorted && (
        <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="text-center py-3">
          <span className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full text-sm font-bold text-white" style={{ backgroundColor: '#059669', boxShadow: '3px 3px 0px 0px #047857' }}>
            <CheckCircle2 size={16} /> All sorted!
          </span>
        </motion.div>
      )}
    </div>
  );
};

/* ═══ Reorder item colours ═══ */
const REORDER_COLORS = [
  { bg: '#2A7D6F', border: '#1F5F54' },
  { bg: '#EA580C', border: '#C2410C' },
  { bg: '#2563EB', border: '#1D4ED8' },
  { bg: '#D97706', border: '#B45309' },
];


const AgencyProtocolModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const { responses, saveResponse, isLoaded } = useModuleResponses('agency-protocol');
  const { northStar } = useNorthStar();
  const [futureSelf, setFutureSelf] = useState('');
  const [dailyAction, setDailyAction] = useState('');
  const [battlePlanItems, setBattlePlanItems] = useState([
    { id: 'goal', text: 'Program Your Destination (Goal)' },
    { id: 'advantage', text: 'Know Your Engine (Advantage)' },
    { id: 'reframe', text: 'Install Your Suspension (Reframe)' },
    { id: 'hack', text: 'Take The Wheel (Classroom Hack)' },
  ]);
  const [scenarioChoice, setScenarioChoice] = useState<string | null>(null);

  useEffect(() => {
    if (isLoaded) {
      if (responses['futureSelf']) setFutureSelf(responses['futureSelf']);
      if (responses['dailyAction']) setDailyAction(responses['dailyAction']);
      if (responses['scenarioChoice']) setScenarioChoice(responses['scenarioChoice']);
    }
  }, [isLoaded]);

  const sections = [
    { id: 'destination-path', title: 'Setting the Sat-Nav', eyebrow: '01 // Your Destination', icon: Target },
    { id: 'driver-passenger', title: 'Driver or Passenger?', eyebrow: '02 // Seizing the Wheel', icon: Users },
    { id: 'hacking', title: 'The Driver\'s Controls', eyebrow: '03 // Hacking Your Classroom', icon: Settings },
    { id: 'glitch', title: 'Roadblocks & Potholes', eyebrow: '04 // When the Journey is Unfair', icon: ShieldAlert },
    { id: 'advantage', title: 'Your Unique Engine', eyebrow: '05 // The Power of Your Story', icon: Zap },
    { id: 'blueprint', title: 'Your Route Plan', eyebrow: '06 // Building Your Driver Identity', icon: Map },
  ];

  return (
    <ModuleLayout
      moduleNumber="01"
      moduleTitle="The Driver's Manual"
      moduleSubtitle="Taking the Wheel of Your Education"
      moduleDescription="Learn how to stop being a passenger in your own school life and start driving toward the future you actually want."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Start Your Engine"
    >
      {(activeSection) => (
        <>
          {/* ══════════ Section 1: Setting the Sat-Nav ══════════ */}
          {activeSection === 0 && (
            <ReadingSection title="Setting the Sat-Nav: Your Future is Calling." eyebrow="Step 1" icon={Target} theme={theme}>
              <p>Without a destination programmed into the Sat-Nav, you're just driving aimlessly. The same is true for school. You might know you want to go to college, but that's a vague spot on a map. To get there, you need a clear route, and that starts by connecting today's homework to tomorrow's destination.</p>
              <p>The science is clear: linking your daily study to a future career you want makes you far more likely to do the work. The solution is to stop seeing schoolwork as a chore and start seeing it as an <Highlight description="Every piece of study you do now is a direct deposit into your future self's bank account. It's not just homework — it's building the life you want." theme={theme}>Investment</Highlight> in your <Highlight description="A vivid picture of who you want to become. When you can actually see your future self clearly, today's effort feels worth it because you know exactly what you're working toward." theme={theme}>Possible Self</Highlight>. Every single action you take today builds the road to that future destination.</p>
              <PersonalStory name="Alex" role="Founder, NextStepUni">
                <p>For most of school, I had no destination programmed. Growing up in Togher, nobody in my world was talking about college courses or career paths. School was just something you showed up to — or didn't. I had no "Possible Self" because I'd never been shown one that looked like me. It wasn't until I lost my best friend and hit rock bottom that I even considered the idea that school could lead somewhere worth going.</p>
              </PersonalStory>
              <MicroCommitment theme={theme}>
                <p>Open your phone's calendar right now. Schedule a 15-minute slot for tomorrow called 'Driving Practice' and use it to do the small action you list below.</p>
              </MicroCommitment>

              {/* Input form */}
              <div className="my-14 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
                <h4 className="font-serif text-xl font-semibold text-zinc-900 dark:text-white text-center mb-6">Program Your Destination</h4>
                <div className="space-y-4 max-w-lg mx-auto">
                  <div>
                    <label className="block text-xs font-medium text-zinc-500 mb-1.5">The Destination (Your Dream Course/Career)</label>
                    <input value={futureSelf} onChange={(e) => setFutureSelf(e.target.value)} onBlur={() => saveResponse('futureSelf', futureSelf)} placeholder="e.g., Computer Science at Trinity" className="w-full bg-white dark:bg-zinc-800 rounded-xl px-4 py-3 text-sm text-zinc-800 dark:text-white placeholder-zinc-400 outline-none" style={{ border: '1.5px solid #E7E5E4' }} />
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-zinc-500 mb-1.5">The First Turn (One Small Action Tomorrow)</label>
                    <input value={dailyAction} onChange={(e) => setDailyAction(e.target.value)} onBlur={() => saveResponse('dailyAction', dailyAction)} placeholder="e.g., 20 minutes of Maths revision" className="w-full bg-white dark:bg-zinc-800 rounded-xl px-4 py-3 text-sm text-zinc-800 dark:text-white placeholder-zinc-400 outline-none" style={{ border: '1.5px solid #E7E5E4' }} />
                  </div>
                  {futureSelf && dailyAction && (
                    <motion.div initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} className="p-4 rounded-xl text-center" style={{ backgroundColor: '#6EE7B7', border: '2.5px solid #059669', boxShadow: '3px 3px 0px 0px #059669' }}>
                      <p className="text-sm font-bold" style={{ color: '#064E3B' }}><CheckCircle2 size={14} className="inline -mt-0.5 mr-1" /> Route locked in. The journey starts now.</p>
                    </motion.div>
                  )}
                </div>
              </div>
            </ReadingSection>
          )}

          {/* ══════════ Section 2: Driver or Passenger? ══════════ */}
          {activeSection === 1 && (
            <ReadingSection title="Driver or Passenger? Seizing the Wheel." eyebrow="Step 2" icon={Users} theme={theme}>
              <p>In the car of your education, you have two choices. You can be a 'Passenger', letting the teacher, your parents, or your friends decide the direction. You only do the work to avoid getting in trouble. This is being a <Highlight description="Someone who feels like their actions are controlled by other people — like a piece being moved around a chessboard. You do the work because someone told you to, not because you chose to." theme={theme}>Pawn</Highlight>, and it leads to shallow, rote learning that falls apart under exam pressure.</p>
              <p>Or, you can be a 'Driver'—an <Highlight description="The opposite of a Pawn. You feel like the true source of your own actions. You're not being pushed — you're choosing to move. People who feel this way do far better in school." theme={theme}>Origin</Highlight>—who grabs the steering wheel. You take <Highlight description="You do the work because YOU have chosen to, not because someone is making you. It's your education, your choice, your future." theme={theme}>Academic Ownership</Highlight>. This isn't a personality trait you're born with; it's a choice you make every single day.</p>
              <MicroCommitment theme={theme}>
                <p>Think of one class you have tomorrow where you usually act like a passenger. Decide on one small 'driver' move you can make – like asking one question or deliberately trying to connect the topic to your own interests.</p>
              </MicroCommitment>
              <MindsetSorter />
            </ReadingSection>
          )}

          {/* ══════════ Section 3: Branching Scenario ══════════ */}
          {activeSection === 2 && (
            <ReadingSection title="The Driver's Controls: Hacking the Classroom." eyebrow="Step 3" icon={Settings} theme={theme}>
               <p>Being a Driver isn't about ignoring the teacher; it's about working with them. You have controls — your questions, your comments, your focus — that influence the journey. Using them is called <Highlight description="Instead of sitting quietly and hoping things make sense, you actively shape how you learn. You ask questions, tell the teacher what's clicking and what's not, and make the material relevant to you." theme={theme}>Agentic Engagement</Highlight>.</p>
               <p>Think of it like this: if you're lost while driving and you don't tell the sat-nav, it can't reroute you. Your teachers are the same — they need your feedback to give you the clear directions (<Highlight description="The road signs of your education — clear instructions, expectations, and feedback from your teacher. Without them you're guessing. With them, you know exactly where you stand." theme={theme}>Structure</Highlight>) and support you actually need.</p>
               <MicroCommitment theme={theme}>
                <p>Look at your notes from your hardest subject. Find one thing you don't fully understand. Write it down on a post-it note and stick it to your school journal as a reminder to ask the teacher tomorrow.</p>
              </MicroCommitment>

              {/* Branching Scenario */}
              <div className="my-14 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
                <div className="flex justify-center mb-4">
                  <span className="inline-flex items-center gap-1.5 px-4 py-1.5 rounded-full text-[10px] font-bold uppercase tracking-wider" style={{ backgroundColor: '#FCD34D', border: '2px solid #D97706', color: '#78350F', boxShadow: '2px 2px 0px 0px #D97706' }}>
                    Scenario
                  </span>
                </div>
                <h4 className="font-serif text-xl font-semibold text-zinc-900 dark:text-white text-center">The Confusion</h4>
                <p className="text-sm text-zinc-500 text-center mt-1 mb-6">You don't understand the teacher's explanation. What's your move?</p>

                <div className="space-y-3 max-w-lg mx-auto">
                  <AnimatePresence>
                    {/* Passenger option — hide after choosing driver */}
                    {(!scenarioChoice || scenarioChoice === 'passive') && (
                      <motion.button
                        layout
                        exit={{ opacity: 0, scale: 0.9, transition: { duration: 0.2 } }}
                        whileHover={!scenarioChoice ? { x: -2, y: -2, boxShadow: '6px 6px 0px 0px #1C1917' } : {}}
                        whileTap={!scenarioChoice ? { x: 2, y: 2, boxShadow: '1px 1px 0px 0px #1C1917' } : {}}
                        transition={press}
                        onClick={() => { if (!scenarioChoice) { setScenarioChoice('passive'); saveResponse('scenarioChoice', 'passive'); } }}
                        className="w-full text-left p-5 flex items-center gap-4 bg-white dark:bg-zinc-800"
                        style={{
                          border: '2.5px solid #1C1917',
                          borderRadius: 16,
                          boxShadow: scenarioChoice === 'passive' ? '2px 2px 0px 0px #1C1917' : '4px 4px 0px 0px #1C1917',
                        }}
                      >
                        <div className="w-10 h-10 flex items-center justify-center shrink-0" style={{ backgroundColor: '#DC2626', borderRadius: 12 }}>
                          <X size={18} style={{ color: '#fff' }} />
                        </div>
                        <div>
                          <p className="text-[10px] font-bold uppercase tracking-wider mb-0.5 text-zinc-500">Passenger Move</p>
                          <p className="text-sm font-semibold text-zinc-800 dark:text-white">Say nothing and hope you figure it out later.</p>
                        </div>
                      </motion.button>
                    )}

                    {/* Driver option — hide after choosing passenger */}
                    {(!scenarioChoice || scenarioChoice === 'agentic') && (
                      <motion.button
                        layout
                        exit={{ opacity: 0, scale: 0.9, transition: { duration: 0.2 } }}
                        whileHover={!scenarioChoice ? { x: -2, y: -2, boxShadow: '6px 6px 0px 0px #1C1917' } : {}}
                        whileTap={!scenarioChoice ? { x: 2, y: 2, boxShadow: '1px 1px 0px 0px #1C1917' } : {}}
                        transition={press}
                        onClick={() => { if (!scenarioChoice) { setScenarioChoice('agentic'); saveResponse('scenarioChoice', 'agentic'); } }}
                        className="w-full text-left p-5 flex items-center gap-4 bg-white dark:bg-zinc-800"
                        style={{
                          border: '2.5px solid #1C1917',
                          borderRadius: 16,
                          boxShadow: scenarioChoice === 'agentic' ? '2px 2px 0px 0px #1C1917' : '4px 4px 0px 0px #1C1917',
                        }}
                      >
                        <div className="w-10 h-10 flex items-center justify-center shrink-0" style={{ backgroundColor: '#059669', borderRadius: 12 }}>
                          <CheckCircle2 size={18} style={{ color: '#fff' }} />
                        </div>
                        <div>
                          <p className="text-[10px] font-bold uppercase tracking-wider mb-0.5 text-zinc-500">Driver Move</p>
                          <p className="text-sm font-semibold text-zinc-800 dark:text-white">Ask a strategic question to clarify.</p>
                        </div>
                      </motion.button>
                    )}
                  </AnimatePresence>
                </div>

                <AnimatePresence>
                  {scenarioChoice && (
                    <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }} className="mt-5 max-w-lg mx-auto">
                      <div className="bg-white dark:bg-zinc-900 overflow-hidden" style={{ border: '2.5px solid #1C1917', borderRadius: 18, boxShadow: '4px 4px 0px 0px #1C1917' }}>
                        {/* Coloured header bar */}
                        <div style={{ backgroundColor: scenarioChoice === 'passive' ? '#DC2626' : '#059669', padding: '10px 16px', borderBottom: '2.5px solid #1C1917' }}>
                          <p className="text-[13px] font-medium tracking-wider uppercase text-white text-center">
                            {scenarioChoice === 'passive' ? 'Roadblock ahead!' : 'Route recalculated!'}
                          </p>
                        </div>
                        <div className="p-5">
                          <p className="text-sm leading-relaxed text-zinc-700 dark:text-zinc-300">
                            {scenarioChoice === 'passive'
                              ? "You've missed a turn. The feeling of being \"lost\" grows, making it harder to catch up later."
                              : "You get a clear direction, help others in the car, and show the teacher you're a co-pilot. This is Agentic Engagement."
                            }
                          </p>
                        </div>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            </ReadingSection>
          )}

          {/* ══════════ Section 4: Reframe ══════════ */}
          {activeSection === 3 && (
            <ReadingSection title="Roadblocks & Potholes: When the Journey is Unfair." eyebrow="Step 4" icon={ShieldAlert} theme={theme}>
              {northStar && (() => { const p = COMPACT_CALLOUT_PLACEMENTS.find(p => p.moduleId === 'agency-protocol'); return p ? <NorthStarCallout northStar={northStar} variant="compact" message={p.message} /> : null; })()}
              <p>Let's be real: not all roads are perfectly paved. If you're from a disadvantaged area, you face real <Highlight description="The real-world stuff that makes school harder for some people — things like fewer resources, less support at home, or schools that are stretched thin. None of it is your fault, but it is part of your road." theme={theme}>Structural Conditions</Highlight>. It's easy to see these roadblocks and think the journey is impossible for you.</p>
              <p>This creates the most dangerous trap in education: interpreting <Highlight description="A mental trap where your brain confuses 'this is hard' with 'this isn't for me.' The work is supposed to be hard — that's what makes it worth something. Hard doesn't mean impossible." theme={theme}>Difficulty as Impossibility</Highlight>. The moment the work gets hard, your brain defaults to: "See? This isn't for people like me." The key is to install a high-tech suspension system in your brain: a conscious, deliberate reframe.</p>
              <MicroCommitment theme={theme}>
                <p>Write this 'Reframe' on a small piece of paper: "This is hard because it's a high-level problem. Solving it is a step toward my goal." Fold it up and put it in your wallet or pencil case.</p>
              </MicroCommitment>

              <div className="my-14 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
                <h4 className="font-serif text-xl font-semibold text-zinc-900 dark:text-white text-center mb-6">The Mental Suspension System</h4>
                {/* Negative thought — coral card */}
                <div className="p-4 mb-4 rounded-xl" style={{ backgroundColor: '#FCA5A5', border: '2px solid #DC2626' }}>
                  <p className="text-sm font-bold flex items-center gap-2" style={{ color: '#7F1D1D' }}>
                    <AlertTriangle size={14} /> &ldquo;I'll never be able for Higher Level Maths.&rdquo;
                  </p>
                </div>
                {/* Reframe input */}
                <div>
                  <label className="block text-xs font-medium text-zinc-500 mb-2 ml-1">Your reframe</label>
                  <input
                    value={responses['reframeText'] || ''}
                    onChange={(e) => saveResponse('reframeText', e.target.value)}
                    placeholder="e.g., Maths is hard right now, but I haven't tried every approach yet."
                    className="w-full bg-white dark:bg-zinc-800 rounded-xl px-5 py-3.5 text-sm font-medium text-zinc-800 dark:text-white placeholder-zinc-400 outline-none transition-all"
                    style={{ border: '1.5px solid #E7E5E4' }}
                  />
                </div>
                {responses['reframeText'] && (
                  <motion.div initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} className="mt-4 p-4 rounded-xl" style={{ backgroundColor: '#6EE7B7', border: '2.5px solid #059669', boxShadow: '3px 3px 0px 0px #059669' }}>
                    <p className="text-sm font-bold" style={{ color: '#064E3B' }}><CheckCircle2 size={14} className="inline -mt-0.5 mr-1" /> Suspension installed. Pothole → speed bump.</p>
                  </motion.div>
                )}
              </div>
            </ReadingSection>
          )}

          {/* ══════════ Section 5: Flip Cards ══════════ */}
          {activeSection === 4 && (
            <ReadingSection title="Your Unique Engine: The Power of Your Story." eyebrow="Step 5" icon={Zap} theme={theme}>
              <p>Society loves to focus on what students from disadvantaged backgrounds don't have. We're flipping that. Your life experiences have equipped your car with a unique, custom-tuned engine that many students with factory-standard parts simply don't have. This is your <Highlight description="The skills, street smarts, and real-world knowledge you've picked up from your life, your community, and your family. School doesn't always recognise them — but they're genuine advantages." theme={theme}>Funds of Knowledge</Highlight>.</p>
              <p>These aren't just 'life skills' — they're genuine advantages that give you more horsepower for the Leaving Cert journey. Flip the cards below to see how your real-world experience translates directly into academic power.</p>
               <MicroCommitment theme={theme}>
                <p>Tell one person today—a friend, a family member—about one of your 'Street Smarts' and how it's actually a superpower for school. Saying it out loud makes it real.</p>
              </MicroCommitment>
              <div className="my-14 grid grid-cols-1 md:grid-cols-3 gap-5">
                <FlipCard front="Street Smarts: Reading different social situations." back="Academic Horsepower: High-level analysis of character in English." frontIcon={Users} backIcon={Lightbulb} colorIndex={0} />
                <FlipCard front="Street Smarts: Dealing with setbacks and bouncing back." back="Academic Horsepower: Resilience to keep studying after a bad mock result." frontIcon={Zap} backIcon={Activity} colorIndex={1} />
                <FlipCard front="Street Smarts: Translating for family or code-switching." back="Academic Horsepower: Advanced ability to analyse language in Irish & English papers." frontIcon={Brain} backIcon={Brain} colorIndex={2} />
              </div>
            </ReadingSection>
          )}

          {/* ══════════ Section 6: Reorder + Route Plan ══════════ */}
          {activeSection === 5 && (
            <ReadingSection title="Your Route Plan: Building Your Driver Identity." eyebrow="Step 6" icon={Map} theme={theme}>
              <p>A Driver identity isn't something you find; it's something you build through deliberate, daily action. It's the route plan that guides you when motivation is low and the road is long. First, arrange your protocol components into your personal pre-drive checklist.</p>

              {/* Reorder checklist */}
              <div className="my-14 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
                <h4 className="font-serif text-xl font-semibold text-zinc-900 dark:text-white text-center mb-2">Pre-Drive Checklist</h4>
                <p className="text-sm text-zinc-500 text-center mb-6">Drag to reorder by priority</p>
                <Reorder.Group axis="y" values={battlePlanItems} onReorder={setBattlePlanItems} className="space-y-3 max-w-md mx-auto">
                  {battlePlanItems.map((item, i) => {
                    const c = REORDER_COLORS[i % REORDER_COLORS.length];
                    return (
                      <Reorder.Item
                        key={item.id}
                        value={item}
                        className="flex items-center gap-3 cursor-grab active:cursor-grabbing bg-white dark:bg-zinc-800"
                        style={{
                          border: '2.5px solid #1C1917',
                          borderRadius: 16,
                          padding: '14px 16px',
                          boxShadow: '4px 4px 0px 0px #1C1917',
                        }}
                        whileDrag={{ scale: 1.03, y: -2, boxShadow: '6px 6px 0px 0px #1C1917' }}
                      >
                        <GripVertical size={18} className="text-zinc-400 shrink-0" style={{ opacity: 0.5 }} />
                        <span className="w-9 h-9 rounded-xl flex items-center justify-center text-xs font-bold text-white shrink-0" style={{ backgroundColor: c.bg, border: `2px solid ${c.border}` }}>{i + 1}</span>
                        <span className="text-sm font-bold text-zinc-800 dark:text-zinc-200">{item.text}</span>
                      </Reorder.Item>
                    );
                  })}
                </Reorder.Group>
              </div>

              {/* Final route plan inputs */}
              <div className="my-14 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
                <h4 className="font-serif text-xl font-semibold text-zinc-900 dark:text-white text-center mb-6">Finalise Your Route Plan</h4>
                <div className="space-y-4 max-w-lg mx-auto">
                  <div>
                    <label className="block text-xs font-medium text-zinc-500 mb-1.5">My Destination (LC Goal)</label>
                    <input value={responses['routeDestination'] || ''} onChange={(e) => saveResponse('routeDestination', e.target.value)} placeholder="e.g., 500 points for Engineering at UCD" className="w-full bg-white dark:bg-zinc-800 rounded-xl px-4 py-3 text-sm text-zinc-800 dark:text-white placeholder-zinc-400 outline-none" style={{ border: '1.5px solid #E7E5E4' }} />
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-zinc-500 mb-1.5">My Custom Engine (My Advantage)</label>
                    <input value={responses['routeEngine'] || ''} onChange={(e) => saveResponse('routeEngine', e.target.value)} placeholder="e.g., I'm good at staying calm under pressure." className="w-full bg-white dark:bg-zinc-800 rounded-xl px-4 py-3 text-sm text-zinc-800 dark:text-white placeholder-zinc-400 outline-none" style={{ border: '1.5px solid #E7E5E4' }} />
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-zinc-500 mb-1.5">My First Turn (Classroom Hack)</label>
                    <input value={responses['routeHack'] || ''} onChange={(e) => saveResponse('routeHack', e.target.value)} placeholder="e.g., Tomorrow in Maths, ask the teacher to explain the 'why'." className="w-full bg-white dark:bg-zinc-800 rounded-xl px-4 py-3 text-sm text-zinc-800 dark:text-white placeholder-zinc-400 outline-none" style={{ border: '1.5px solid #E7E5E4' }} />
                  </div>
                </div>
              </div>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default AgencyProtocolModule;
