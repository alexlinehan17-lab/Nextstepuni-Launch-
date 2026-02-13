/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence, Reorder } from 'framer-motion';
import {
  Target, Users, Settings, ShieldAlert, Zap, Map,
  Lightbulb, Activity, Brain, ChevronsUpDown
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { blueTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment, PersonalStory } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = blueTheme;

const FlipCard = ({ front, back, frontIcon: FrontIcon, backIcon: BackIcon }: { front: React.ReactNode, back: React.ReactNode, frontIcon: any, backIcon: any }) => {
  const [isFlipped, setIsFlipped] = useState(false);
  return (
    <div className="w-full h-52 [perspective:1000px] cursor-pointer" onClick={() => setIsFlipped(!isFlipped)}>
      <motion.div
        className="relative w-full h-full"
        style={{ transformStyle: 'preserve-3d' }}
        animate={{ rotateY: isFlipped ? 180 : 0 }}
        transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
      >
        <div className="absolute w-full h-full [backface-visibility:hidden] rounded-xl p-6 flex flex-col items-center justify-center text-center border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-800 group hover:border-zinc-300 dark:hover:border-zinc-600 transition-colors">
          <div className="w-10 h-10 rounded-lg bg-zinc-100 dark:bg-zinc-700 flex items-center justify-center mb-4">
            <FrontIcon size={20} className="text-zinc-500 dark:text-zinc-400"/>
          </div>
          <p className="text-sm font-semibold leading-snug text-zinc-700 dark:text-zinc-200">{front}</p>
          <p className="absolute bottom-3 right-4 text-[9px] font-medium tracking-wider text-zinc-300 dark:text-zinc-600 uppercase">Tap to reveal</p>
        </div>
        <div className="absolute w-full h-full [backface-visibility:hidden] rounded-xl p-6 flex flex-col items-center justify-center text-center bg-zinc-900 dark:bg-white text-white dark:text-zinc-900" style={{ transform: 'rotateY(180deg)' }}>
          <div className="w-10 h-10 rounded-lg bg-white/10 dark:bg-zinc-900/10 flex items-center justify-center mb-4">
            <BackIcon size={20} className="text-white/70 dark:text-zinc-900/70"/>
          </div>
          <p className="text-sm font-semibold leading-snug">{back}</p>
        </div>
      </motion.div>
    </div>
  );
};

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

  const handleSort = (thought: typeof initialThoughts[0]) => {
    setThoughts(thoughts.filter(t => t.id !== thought.id));
    if (thought.type === 'passenger') {
      setPassenger([...passenger, thought]);
    } else {
      setDriver([...driver, thought]);
    }
  };

  return (
    <div className="my-10 p-8 md:p-10 bg-white dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-800">
      <h4 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white text-center">Driver vs. Passenger Diagnostic</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">After a bad result, sort these thoughts into the correct lane.</p>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 min-h-[200px]">
        <div className="p-6 bg-rose-50/50 border border-rose-200 rounded-xl">
           <h5 className="font-semibold text-rose-700 mb-4 text-center text-sm">Passenger Lane</h5>
           <AnimatePresence>
             {passenger.map(p => (
                <motion.div layoutId={`${p.id}`} key={p.id} className="p-4 bg-white dark:bg-zinc-800 rounded-xl shadow-sm text-sm font-medium text-zinc-700 dark:text-zinc-200 text-center mb-2">
                   "{p.text}"
                </motion.div>
             ))}
           </AnimatePresence>
        </div>
         <div className="p-6 bg-blue-50/50 border border-blue-200 rounded-xl">
           <h5 className="font-semibold text-blue-700 mb-4 text-center text-sm">Driver Lane</h5>
            <AnimatePresence>
             {driver.map(d => (
                <motion.div layoutId={`${d.id}`} key={d.id} className="p-4 bg-white dark:bg-zinc-800 rounded-xl shadow-sm text-sm font-medium text-zinc-700 dark:text-zinc-200 text-center mb-2">
                   "{d.text}"
                </motion.div>
             ))}
           </AnimatePresence>
        </div>
      </div>
      <div className="mt-8 flex flex-wrap justify-center gap-3">
        <AnimatePresence>
          {thoughts.map(thought => (
             <motion.button layoutId={`${thought.id}`} key={thought.id} onClick={() => handleSort(thought)} className="p-4 bg-zinc-100 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 rounded-xl text-sm font-bold text-zinc-800 dark:text-white hover:bg-zinc-200 dark:hover:bg-zinc-600 transition-colors">
               "{thought.text}"
             </motion.button>
          ))}
        </AnimatePresence>
      </div>
    </div>
  );
};


const AgencyProtocolModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const [futureSelf, setFutureSelf] = useState('');
  const [dailyAction, setDailyAction] = useState('');
  const [reframe, setReframe] = useState(false);
  const [battlePlanItems, setBattlePlanItems] = useState([
    { id: 'goal', text: 'Program Your Destination (Goal)' },
    { id: 'advantage', text: 'Know Your Engine (Advantage)' },
    { id: 'reframe', text: 'Install Your Suspension (Reframe)' },
    { id: 'hack', text: 'Take The Wheel (Classroom Hack)' },
  ]);
  const [scenarioChoice, setScenarioChoice] = useState<string | null>(null);

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
      moduleSubtitle="The Driver's Manual"
      moduleDescription="Synthesising research on motivation and identity, this module provides the blueprint for becoming the &quot;Origin&quot; of your academic success."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Start Your Engine"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="Setting the Sat-Nav: Your Future is Calling." eyebrow="Step 1" icon={Target} theme={theme}>
              <p>Without a destination programmed into the Sat-Nav, you're just driving aimlessly. The same is true for school. You might know you want to go to college, but that's a vague spot on a map. To get there, you need a clear route, and that starts by connecting today's homework to tomorrow's destination.</p>
              <p>The science is clear: linking your daily study to a future career you want makes you far more likely to do the work. The solution is to stop seeing schoolwork as a chore and start seeing it as an <Highlight description="The scientifically-proven idea that every piece of study you do now is a direct deposit into your future self's bank account. This isn't just a nice thought; it's a powerful motivational tool." theme={theme}>Investment</Highlight> in your <Highlight description="A vivid, personal picture of who you want to become. Psychologists have shown this is a key tool for driving motivation, as it makes future rewards feel more immediate." theme={theme}>Possible Self</Highlight>. Every single action you take today builds the road to that future destination.</p>
              <PersonalStory name="Alex" role="Founder, NextStepUni">
                <p>For most of school, I had no destination programmed. Growing up in Togher, nobody in my world was talking about college courses or career paths. School was just something you showed up to — or didn't. I had no "Possible Self" because I'd never been shown one that looked like me. It wasn't until I lost my best friend and hit rock bottom that I even considered the idea that school could lead somewhere worth going.</p>
              </PersonalStory>
              <MicroCommitment theme={theme}>
                <p>Open your phone's calendar right now. Schedule a 15-minute slot for tomorrow called 'Driving Practice' and use it to do the small action you list below.</p>
              </MicroCommitment>
              <div className="my-10 p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700 space-y-6">
                <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Program Your Destination</h4>
                <div className="space-y-3"><label className="block text-[10px] font-semibold text-zinc-600 dark:text-zinc-300 uppercase ml-4 text-left">The Destination (Your Dream Course/Career):</label><input value={futureSelf} onChange={(e) => setFutureSelf(e.target.value)} placeholder="e.g., Computer Science at Trinity, Physiotherapy" className="w-full bg-zinc-50 dark:bg-zinc-800/50 border border-zinc-100 rounded-xl p-4 focus:border-blue-500 outline-none transition-colors" /></div>
                <div className="space-y-3"><label className="block text-[10px] font-semibold text-zinc-600 dark:text-zinc-300 uppercase ml-4 text-left">The First Turn (One Small Action Tomorrow):</label><input value={dailyAction} onChange={(e) => setDailyAction(e.target.value)} placeholder="e.g., Do 20 minutes of Maths revision before school" className="w-full bg-zinc-50 dark:bg-zinc-800/50 border border-zinc-100 rounded-xl p-4 focus:border-blue-500 outline-none transition-colors" /></div>
                {futureSelf && dailyAction && <motion.div initial={{opacity:0}} animate={{opacity:1}} className="text-center pt-4 text-blue-600 font-bold text-sm">Route locked in. The journey starts now.</motion.div>}
              </div>
            </ReadingSection>
          )}

          {activeSection === 1 && (
            <ReadingSection title="Driver or Passenger? Seizing the Wheel." eyebrow="Step 2" icon={Users} theme={theme}>
              <p>In the car of your education, you have two choices. You can be a 'Passenger', letting the teacher, your parents, or your friends decide the direction. You only do the work to avoid getting in trouble. This is being a <Highlight description="A term from a major psychological theory called Self-Determination Theory. A 'Pawn' feels their actions are controlled by external forces, like a piece on a chessboard." theme={theme}>Pawn</Highlight>, and it leads to shallow, rote learning that falls apart under exam pressure.</p>
              <p>Or, you can be a 'Driver'—an <Highlight description="The opposite of a Pawn. An 'Origin' feels they are the true source of their own actions. This sense of control is a powerful predictor of academic success." theme={theme}>Origin</Highlight>—who grabs the steering wheel. You take <Highlight description="The experience that your actions come from your own choice and will, not from external pressure. You do the work because YOU have chosen to." theme={theme}>Academic Ownership</Highlight>. This isn't a personality trait you're born with; it's a choice you make every single day.</p>
              <MicroCommitment theme={theme}>
                <p>Think of one class you have tomorrow where you usually act like a passenger. Decide on one small 'driver' move you can make – like asking one question or deliberately trying to connect the topic to your own interests.</p>
              </MicroCommitment>
              <MindsetSorter />
            </ReadingSection>
          )}

          {activeSection === 2 && (
            <ReadingSection title="The Driver's Controls: Hacking the Classroom." eyebrow="Step 3" icon={Settings} theme={theme}>
               <p>Being a Driver isn't about ignoring the teacher; it's about working with them. You have controls—your questions, your comments, your focus—that influence the journey. Using them is called <Highlight description="Actively and constructively contributing to your own instruction. It's about personalising the material, expressing preferences, and giving feedback to the teacher so they can help you better." theme={theme}>Agentic Engagement</Highlight>. Your teachers need your feedback to provide both the clear directions you need (<Highlight description="Clear expectations, directions, and feedback from a teacher. This is like the road signs and markings on your journey." theme={theme}>Structure</Highlight>) and support for your motivation.</p>
               <MicroCommitment theme={theme}>
                <p>Look at your notes from your hardest subject. Find one thing you don't fully understand. Write it down on a post-it note and stick it to your school journal as a reminder to ask the teacher tomorrow.</p>
              </MicroCommitment>
               <div className="my-10 p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
                  <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Branching Scenario: The Confusion</h4>
                  <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">You don't understand the teacher's explanation. What's your move?</p>
                  <div className="space-y-4 max-w-lg mx-auto">
                    <button onClick={() => setScenarioChoice('passive')} className="w-full text-left p-4 bg-zinc-50 dark:bg-zinc-800/50 hover:bg-zinc-100 dark:hover:bg-zinc-700 rounded-xl border border-zinc-200 dark:border-zinc-700 transition-all"><strong>Passenger Move:</strong> Say nothing and hope you figure it out later.</button>
                    <button onClick={() => setScenarioChoice('agentic')} className="w-full text-left p-4 bg-zinc-50 dark:bg-zinc-800/50 hover:bg-zinc-100 dark:hover:bg-zinc-700 rounded-xl border border-zinc-200 dark:border-zinc-700 transition-all"><strong>Driver Move:</strong> Ask a strategic question to clarify.</button>
                  </div>
                  <AnimatePresence>
                  {scenarioChoice && (
                    <motion.div initial={{opacity:0, y:10}} animate={{opacity:1, y:0}} className="mt-8 p-6 rounded-xl bg-zinc-900 text-white">
                      {scenarioChoice === 'passive' && <p><strong className="text-rose-400">Roadblock:</strong> You've missed a turn. The feeling of being "lost" grows, making it harder to catch up later.</p>}
                      {scenarioChoice === 'agentic' && <p><strong className="text-emerald-400">Success:</strong> You get a clear direction, help others in the car, and show the teacher you're a co-pilot, not just a passenger. This is Agentic Engagement.</p>}
                    </motion.div>
                  )}
                  </AnimatePresence>
               </div>
            </ReadingSection>
          )}

          {activeSection === 3 && (
            <ReadingSection title="Roadblocks & Potholes: When the Journey is Unfair." eyebrow="Step 4" icon={ShieldAlert} theme={theme}>
              <p>Let's be real: not all roads are perfectly paved. If you're from a disadvantaged area, you face real <Highlight description="Systemic barriers like underfunded schools or fewer resources that make academic success harder. These are the potholes and unfair tolls on your educational road." theme={theme}>Structural Conditions</Highlight>. It's easy to see these roadblocks and think the journey is impossible for you.</p>
              <p>This creates the most dangerous trap in education: interpreting <Highlight description="A common cognitive trap where academic struggle is seen as proof of personal limitation ('I'm not smart enough'), rather than a sign of a challenging and important task." theme={theme}>Difficulty as Impossibility</Highlight>. The moment the work gets hard, your brain defaults to: "See? This isn't for people like me." The key is to install a high-tech suspension system in your brain: a conscious, deliberate reframe. This is a skill, like learning to change gear.</p>
              <MicroCommitment theme={theme}>
                <p>Write this 'Reframe' on a small piece of paper: "This is hard because it's a high-level problem. Solving it is a step toward my goal." Fold it up and put it in your wallet or pencil case.</p>
              </MicroCommitment>
              <div className="my-10 p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700 flex flex-col items-center gap-6">
                <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Mental Suspension System</h4>
                <p className="text-sm text-zinc-500 dark:text-zinc-400 -mt-4">Next time you hit a mental pothole, run this script:</p>
                <div className="w-full max-w-md text-left bg-zinc-50 dark:bg-zinc-800/50 p-6 rounded-xl border border-zinc-200 dark:border-zinc-700 space-y-4">
                  <p className={`font-mono text-sm transition-opacity ${reframe ? 'text-zinc-400' : 'text-rose-600 font-bold'}`}>&gt; Initial thought: "This is too hard. I can't do it."</p>
                  <button onClick={() => setReframe(true)} className={`w-full text-left font-mono text-sm transition-opacity ${reframe ? 'text-blue-600 font-bold' : 'text-zinc-400'}`}>&gt; Reframe: "This is hard because it's a high-level problem. This is what progress feels like."</button>
                </div>
              </div>
            </ReadingSection>
          )}

          {activeSection === 4 && (
            <ReadingSection title="Your Unique Engine: The Power of Your Story." eyebrow="Step 5" icon={Zap} theme={theme}>
              <p>Society often focuses on what students from disadvantaged backgrounds lack. This is a deficit mindset. We're flipping it. Your life experiences have equipped your car with a unique, custom-tuned engine that many other students with factory-standard parts don't have. This is your <Highlight description="A core concept from sociology. It means the valuable, valid skills and knowledge you bring from your home and community (e.g., resilience, social intelligence). It is your academic superpower." theme={theme}>Funds of Knowledge</Highlight>.</p>
              <p>These aren't just 'life skills'; they are high-level cognitive and social assets that give you more horsepower for the Leaving Cert journey. Click the cards below to see how your 'street smarts' translate directly into academic power.</p>
               <MicroCommitment theme={theme}>
                <p>Tell one person today—a friend, a family member—about one of your 'Street Smarts' and how it's actually a superpower for school. Saying it out loud makes it real.</p>
              </MicroCommitment>
              <div className="my-10 grid grid-cols-1 md:grid-cols-3 gap-6">
                <FlipCard
                  front="Street Smarts: Reading different social situations."
                  back="Academic Horsepower: High-level analysis of character in English."
                  frontIcon={Users}
                  backIcon={Lightbulb}
                />
                 <FlipCard
                  front="Street Smarts: Dealing with setbacks and bouncing back."
                  back="Academic Horsepower: Resilience to keep studying after a bad mock result."
                  frontIcon={Zap}
                  backIcon={Activity}
                />
                 <FlipCard
                  front="Street Smarts: Translating for family or code-switching."
                  back="Academic Horsepower: Advanced ability to analyse language in Irish & English papers."
                  frontIcon={Brain}
                  backIcon={Brain}
                />
              </div>
            </ReadingSection>
          )}

           {activeSection === 5 && (
            <ReadingSection title="Your Route Plan: Building Your Driver Identity." eyebrow="Step 6" icon={Map} theme={theme}>
              <p>A Driver identity isn't something you find; it's something you build through deliberate, daily action. It's the route plan that guides you when motivation is low and the road is long. First, arrange your protocol components into your personal pre-drive checklist.</p>

              <div className="my-10 p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700 space-y-6">
                <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Assemble Your Pre-Drive Checklist</h4>
                <Reorder.Group axis="y" values={battlePlanItems} onReorder={setBattlePlanItems} className="space-y-3 max-w-md mx-auto">
                  {battlePlanItems.map(item => (
                    <Reorder.Item key={item.id} value={item} className="p-4 bg-zinc-50 dark:bg-zinc-800/50 rounded-xl shadow-sm flex items-center gap-4 cursor-grabbing border border-zinc-200 dark:border-zinc-700">
                      <ChevronsUpDown className="text-zinc-400" />
                      <span className="font-bold text-zinc-700 dark:text-zinc-200">{item.text}</span>
                    </Reorder.Item>
                  ))}
                </Reorder.Group>
              </div>

              <div className="my-10 p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700 space-y-6">
                <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Finalise Your Route Plan</h4>
                <div className="space-y-3"><label className="block text-[10px] font-semibold text-zinc-600 dark:text-zinc-300 uppercase ml-4 text-left">My Destination (LC Goal):</label><input placeholder="e.g., 500 points to get Engineering at UCD" className="w-full bg-zinc-50 dark:bg-zinc-800/50 border border-zinc-100 rounded-xl p-4 focus:border-blue-500 outline-none transition-colors" /></div>
                <div className="space-y-3"><label className="block text-[10px] font-semibold text-zinc-600 dark:text-zinc-300 uppercase ml-4 text-left">My Custom Engine (My Advantage):</label><input placeholder="e.g., I'm good at staying calm under pressure." className="w-full bg-zinc-50 dark:bg-zinc-800/50 border border-zinc-100 rounded-xl p-4 focus:border-blue-500 outline-none transition-colors" /></div>
                <div className="space-y-3"><label className="block text-[10px] font-semibold text-zinc-600 dark:text-zinc-300 uppercase ml-4 text-left">My First Turn (Classroom Hack):</label><input placeholder="e.g., Tomorrow in Maths, I will ask the teacher to explain the 'why' behind one formula." className="w-full bg-zinc-50 dark:bg-zinc-800/50 border border-zinc-100 rounded-xl p-4 focus:border-blue-500 outline-none transition-colors" /></div>
              </div>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default AgencyProtocolModule;
