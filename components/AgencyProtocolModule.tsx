/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence, Reorder } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, Zap, ArrowRight, 
  Activity, Target, Settings, Lock, Users, ShieldAlert, ChevronsUpDown, Lightbulb,
  RotateCcw, Flag, Map, Brain
} from 'lucide-react';

// FIX: Cast motion components to any to bypass broken type definitions
const MotionDiv = motion.div as any;
const MotionButton = motion.button as any;
const MotionCircle = motion.circle as any;

type ModuleProgress = {
  unlockedSection: number;
};

interface AgencyProtocolModuleProps {
  onBack: () => void;
  progress: ModuleProgress;
  onProgressUpdate: (progress: ModuleProgress) => void;
}

const Highlight = ({ children, description, color = "bg-blue-100/40" }: { children?: React.ReactNode, description: string, color?: string }) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <span className="relative inline-block mx-0.5">
      <button 
        onClick={(e) => {
          e.stopPropagation();
          setIsOpen(!isOpen);
        }}
        className={`relative inline-flex items-center px-2 py-0.5 font-bold ${color} rounded-md cursor-help hover:bg-blue-200/60 transition-all duration-300 decoration-blue-400/40 underline decoration-2 underline-offset-4 text-blue-900`}
      >
        <span className="not-italic">{children}</span>
      </button>
      <AnimatePresence>
        {isOpen && (
          <>
            <div className="fixed inset-0 z-[60]" onClick={() => setIsOpen(false)} />
            <MotionDiv 
              initial={{ opacity: 0, scale: 0.9, y: 10, x: "-50%" }}
              animate={{ opacity: 1, scale: 1, y: 0, x: "-50%" }}
              exit={{ opacity: 0, scale: 0.9, y: 10, x: "-50%" }}
              className="absolute z-[70] bottom-full left-1/2 mb-6 w-72 p-6 bg-stone-900/95 text-white text-xs rounded-2xl shadow-2xl pointer-events-auto leading-relaxed border border-white/10 backdrop-blur-xl whitespace-normal text-left"
              style={{ transformOrigin: 'bottom center' }}
            >
              <div className="absolute bottom-0 left-1/2 -translate-x-1/2 translate-y-full w-0 h-0 border-l-[10px] border-l-transparent border-r-[10px] border-r-transparent border-t-[10px] border-t-stone-900/95"></div>
              <p className="font-sans font-bold text-blue-400 mb-2 uppercase tracking-[0.2em] text-[9px]">The Academic Insight</p>
              <p className="text-stone-200 font-medium">{description}</p>
            </MotionDiv>
          </>
        )}
      </AnimatePresence>
    </span>
  );
};

const ReadingSection = ({ title, eyebrow, icon: Icon, children }: { title: string, eyebrow: string, icon: any, children?: React.ReactNode }) => (
  <article className="animate-fade-in">
    <header className="mb-12 text-left relative">
      <div className="absolute -left-16 top-0 hidden xl:block">
        <div className="w-12 h-12 rounded-2xl bg-stone-900 flex items-center justify-center text-blue-400 shadow-xl border border-white/10">
          <Icon size={24} />
        </div>
      </div>
      <span className="inline-flex items-center gap-2 px-3 py-1 bg-blue-50 text-blue-600 text-[10px] font-black tracking-[0.4em] uppercase rounded-full mb-4">
        {eyebrow}
      </span>
      <h2 className="font-serif text-4xl md:text-6xl leading-tight tracking-tighter text-stone-900 font-bold italic">
        {title}
      </h2>
    </header>
    <div className="prose prose-stone prose-lg max-w-none space-y-8 text-stone-600 leading-relaxed font-sans text-justify overflow-visible">
      {children}
    </div>
  </article>
);

const MicroCommitment = ({ children }: { children?: React.ReactNode }) => (
  <div className="my-12 p-8 bg-blue-50/50 border-2 border-dashed border-blue-200 rounded-3xl">
    <div className="flex items-start gap-5">
      <div className="w-11 h-11 rounded-xl bg-blue-500 text-white flex items-center justify-center shrink-0 mt-1 shadow-lg shadow-blue-500/20">
        <Flag size={20} />
      </div>
      <div>
        <h4 className="font-bold text-blue-800 text-sm uppercase tracking-widest">Your Mission (Under 5 Mins)</h4>
        <div className="text-stone-600 mt-2 font-medium leading-relaxed">
          {children}
        </div>
      </div>
    </div>
  </div>
);

const ActivityRing = ({ progress, color = "#3b82f6" }: { progress: number, color?: string }) => {
  const radius = 35;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (progress / 100) * circumference;

  return (
    <div className="relative flex items-center justify-center w-24 h-24 mx-auto mb-4">
      <svg className="w-full h-full -rotate-90 overflow-visible" viewBox="0 0 96 96">
        <circle cx="48" cy="48" r={radius} stroke={color} strokeWidth="10" fill="transparent" className="opacity-10"/>
        <MotionCircle cx="48" cy="48" r={radius} stroke={color} strokeWidth="10" fill="transparent" strokeDasharray={circumference} initial={{ strokeDashoffset: circumference }} animate={{ strokeDashoffset: offset }} transition={{ duration: 1.5, ease: "easeOut" }} strokeLinecap="round" style={{ filter: `drop-shadow(0 0 8px ${color}55)` }}/>
      </svg>
    </div>
  );
};

const FlipCard = ({ front, back, frontIcon: FrontIcon, backIcon: BackIcon }: { front: React.ReactNode, back: React.ReactNode, frontIcon: any, backIcon: any }) => {
  const [isFlipped, setIsFlipped] = useState(false);
  return (
    <div className="w-full h-48 [perspective:1000px]" onClick={() => setIsFlipped(!isFlipped)}>
      <MotionDiv
        className="relative w-full h-full transition-transform duration-700"
        style={{ transformStyle: 'preserve-3d' }}
        animate={{ rotateY: isFlipped ? 180 : 0 }}
        transition={{ duration: 0.6, ease: 'easeInOut' }}
      >
        {/* Front */}
        <div className="absolute w-full h-full [backface-visibility:hidden] rounded-3xl p-6 flex flex-col items-center justify-center text-center border border-stone-200 bg-white shadow-lg cursor-pointer group">
          <FrontIcon size={32} className="mb-4 text-stone-400 group-hover:text-blue-500 transition-colors"/>
          <p className="text-sm font-bold leading-snug text-stone-700">{front}</p>
          <div className="absolute bottom-4 right-4 flex items-center gap-1 text-stone-300 group-hover:text-blue-500 transition-colors">
            <RotateCcw size={10} />
            <span className="text-[9px] font-bold">FLIP</span>
          </div>
        </div>
        {/* Back */}
        <div className="absolute w-full h-full [backface-visibility:hidden] rounded-3xl p-6 flex flex-col items-center justify-center text-center border border-blue-700 bg-blue-600 text-white shadow-2xl shadow-blue-500/20" style={{ transform: 'rotateY(180deg)' }}>
          <BackIcon size={32} className="mb-4 text-blue-200"/>
          <p className="text-sm font-bold leading-snug">{back}</p>
        </div>
      </MotionDiv>
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
    <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
      <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Driver vs. Passenger Diagnostic</h4>
      <p className="text-center text-sm text-stone-500 mb-8">After a bad result, sort these thoughts into the correct lane.</p>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 min-h-[200px]">
        <div className="p-6 bg-rose-50 border-2 border-dashed border-rose-200 rounded-3xl">
           <h5 className="font-bold text-rose-700 mb-4 text-center">Passenger Lane</h5>
           <AnimatePresence>
             {passenger.map(p => (
                <MotionDiv layoutId={`${p.id}`} key={p.id} className="p-4 bg-white rounded-xl shadow-sm text-sm font-medium text-stone-700 text-center mb-2">
                   "{p.text}"
                </MotionDiv>
             ))}
           </AnimatePresence>
        </div>
         <div className="p-6 bg-blue-50 border-2 border-dashed border-blue-200 rounded-3xl">
           <h5 className="font-bold text-blue-700 mb-4 text-center">Driver Lane</h5>
            <AnimatePresence>
             {driver.map(d => (
                <MotionDiv layoutId={`${d.id}`} key={d.id} className="p-4 bg-white rounded-xl shadow-sm text-sm font-medium text-stone-700 text-center mb-2">
                   "{d.text}"
                </MotionDiv>
             ))}
           </AnimatePresence>
        </div>
      </div>
      <div className="mt-8 flex flex-wrap justify-center gap-3">
        <AnimatePresence>
          {thoughts.map(thought => (
             <MotionButton layoutId={`${thought.id}`} key={thought.id} onClick={() => handleSort(thought)} className="p-4 bg-stone-100 border border-stone-200 rounded-xl text-sm font-bold text-stone-800 hover:bg-stone-200 transition-colors">
               "{thought.text}"
             </MotionButton>
          ))}
        </AnimatePresence>
      </div>
    </div>
  );
};


export const AgencyProtocolModule: React.FC<AgencyProtocolModuleProps> = ({ onBack, progress, onProgressUpdate }) => {
  const [activeSection, setActiveSection] = useState(progress.unlockedSection);
  const unlockedSection = progress.unlockedSection;
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
  
  useEffect(() => {
    setActiveSection(progress.unlockedSection);
  }, [progress.unlockedSection]);

  const handleCompleteSection = () => {
    if (activeSection === unlockedSection && unlockedSection < sections.length) {
      onProgressUpdate({ unlockedSection: unlockedSection + 1 });
    }

    if (activeSection < sections.length - 1) {
      setActiveSection(activeSection + 1);
    } else {
      onBack();
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleJumpToSection = (index: number) => {
    if (index <= unlockedSection) {
      setActiveSection(index);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  const handlePrev = () => {
    if (activeSection > 0) {
      setActiveSection(activeSection - 1);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  const progressPercentage = sections.length > 0 ? (unlockedSection / sections.length) * 100 : 0;

  return (
    <div className="min-h-screen bg-[#FBFBF9] text-stone-900 font-sans flex flex-col md:flex-row overflow-x-hidden">
      <aside className="w-full md:w-80 bg-white border-r border-stone-200 sticky top-0 md:h-screen z-40 p-8 flex flex-col">
        <div className="flex items-center gap-4 mb-12">
          <MotionButton whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={onBack} className="p-2 rounded-full transition-all border border-stone-200/50 shadow-sm bg-white">
            <ArrowLeft size={16} className="text-stone-700" />
          </MotionButton>
          <div>
            <p className="text-[9px] font-black text-blue-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 01</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">The Driver's Manual</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <MotionDiv
                  className="w-full bg-blue-500 shadow-[0_0_10px_rgba(59,130,246,0.5)]"
                  style={{ height: `${progressPercentage}%` }}
              />
          </div>
          {sections.map((section, idx) => {
            const isUnlocked = idx <= unlockedSection;
            const isActive = idx === activeSection;
            const isCompleted = idx < unlockedSection;
            return (
              <button key={section.id} disabled={!isUnlocked} onClick={() => handleJumpToSection(idx)} className={`relative z-10 w-full flex items-center gap-4 p-3 rounded-xl transition-all duration-500 text-left group ${isActive ? 'bg-blue-50 shadow-sm translate-x-2' : ''} ${!isUnlocked ? 'opacity-40 grayscale cursor-not-allowed' : 'hover:bg-stone-50'}`}>
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border-2 transition-all duration-500 ${isCompleted ? 'bg-blue-600 border-blue-600 text-white shadow-lg' : isActive ? 'bg-white border-blue-500 text-blue-600 shadow-xl rotate-12' : 'bg-white border-stone-200 text-stone-300'}`}>
                   {isCompleted ? <CheckCircle2 size={18} /> : isActive ? <section.icon size={18} /> : <Lock size={16} />}
                </div>
                <div className="flex-grow"><p className={`text-[8px] font-black uppercase tracking-widest ${isActive ? 'text-blue-500' : 'text-stone-400'}`}>{section.eyebrow.split('// ')[1]}</p><h4 className={`text-xs font-bold leading-tight ${isActive ? 'text-stone-900' : 'text-stone-500'}`}>{section.title}</h4></div>
              </button>
            );
          })}
        </div>

        <div className="mt-8 border-t border-stone-100 pt-8 flex flex-col items-center">
           <ActivityRing progress={progressPercentage} color="#3b82f6" /><p className="text-[11px] font-black text-stone-900 uppercase tracking-widest text-center">Progress</p>
        </div>
      </aside>

      <main className="flex-grow flex flex-col items-center py-10 md:py-24 px-6 md:px-16 overflow-y-auto h-screen relative">
        <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:32px_32px] opacity-40 pointer-events-none" />
        <div className="w-full max-w-4xl relative z-10">
          <AnimatePresence mode="wait">
            <MotionDiv key={activeSection} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}>
              {activeSection === 0 && (
                <ReadingSection title="Setting the Sat-Nav: Your Future is Calling." eyebrow="Step 1" icon={Target}>
                  <p>Without a destination programmed into the Sat-Nav, you're just driving aimlessly. The same is true for school. You might know you want to go to college, but that's a vague spot on a map. To get there, you need a clear route, and that starts by connecting today's homework to tomorrow's destination.</p>
                  <p>The science is clear: linking your daily study to a future career you want makes you far more likely to do the work. The solution is to stop seeing schoolwork as a chore and start seeing it as an <Highlight description="The scientifically-proven idea that every piece of study you do now is a direct deposit into your future self's bank account. This isn't just a nice thought; it's a powerful motivational tool.">Investment</Highlight> in your <Highlight description="A vivid, personal picture of who you want to become. Psychologists have shown this is a key tool for driving motivation, as it makes future rewards feel more immediate.">Possible Self</Highlight>. Every single action you take today builds the road to that future destination.</p>
                  <MicroCommitment>
                    <p>Open your phone's calendar right now. Schedule a 15-minute slot for tomorrow called 'Driving Practice' and use it to do the small action you list below.</p>
                  </MicroCommitment>
                  <div className="my-10 p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl space-y-6">
                    <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Program Your Destination</h4>
                    <div className="space-y-3"><label className="block text-[10px] font-black text-stone-600 uppercase ml-4 text-left">The Destination (Your Dream Course/Career):</label><input value={futureSelf} onChange={(e) => setFutureSelf(e.target.value)} placeholder="e.g., Computer Science at Trinity, Physiotherapy" className="w-full bg-stone-50 border-2 border-stone-100 rounded-xl p-4 focus:border-blue-500 outline-none transition-colors" /></div>
                    <div className="space-y-3"><label className="block text-[10px] font-black text-stone-600 uppercase ml-4 text-left">The First Turn (One Small Action Tomorrow):</label><input value={dailyAction} onChange={(e) => setDailyAction(e.target.value)} placeholder="e.g., Do 20 minutes of Maths revision before school" className="w-full bg-stone-50 border-2 border-stone-100 rounded-xl p-4 focus:border-blue-500 outline-none transition-colors" /></div>
                    {futureSelf && dailyAction && <MotionDiv initial={{opacity:0}} animate={{opacity:1}} className="text-center pt-4 text-blue-600 font-bold text-sm">Route locked in. The journey starts now.</MotionDiv>}
                  </div>
                </ReadingSection>
              )}

              {activeSection === 1 && (
                <ReadingSection title="Driver or Passenger? Seizing the Wheel." eyebrow="Step 2" icon={Users}>
                  <p>In the car of your education, you have two choices. You can be a 'Passenger', letting the teacher, your parents, or your friends decide the direction. You only do the work to avoid getting in trouble. This is being a <Highlight description="A term from a major psychological theory called Self-Determination Theory. A 'Pawn' feels their actions are controlled by external forces, like a piece on a chessboard.">Pawn</Highlight>, and it leads to shallow, rote learning that falls apart under exam pressure.</p>
                  <p>Or, you can be a 'Driver'—an <Highlight description="The opposite of a Pawn. An 'Origin' feels they are the true source of their own actions. This sense of control is a powerful predictor of academic success.">Origin</Highlight>—who grabs the steering wheel. You take <Highlight description="The experience that your actions come from your own choice and will, not from external pressure. You do the work because YOU have chosen to.">Academic Ownership</Highlight>. This isn't a personality trait you're born with; it's a choice you make every single day.</p>
                  <MicroCommitment>
                    <p>Think of one class you have tomorrow where you usually act like a passenger. Decide on one small 'driver' move you can make – like asking one question or deliberately trying to connect the topic to your own interests.</p>
                  </MicroCommitment>
                  <MindsetSorter />
                </ReadingSection>
              )}
               
              {activeSection === 2 && (
                <ReadingSection title="The Driver's Controls: Hacking the Classroom." eyebrow="Step 3" icon={Settings}>
                   <p>Being a Driver isn't about ignoring the teacher; it's about working with them. You have controls—your questions, your comments, your focus—that influence the journey. Using them is called <Highlight description="Actively and constructively contributing to your own instruction. It's about personalising the material, expressing preferences, and giving feedback to the teacher so they can help you better.">Agentic Engagement</Highlight>. Your teachers need your feedback to provide both the clear directions you need (<Highlight description="Clear expectations, directions, and feedback from a teacher. This is like the road signs and markings on your journey.">Structure</Highlight>) and support for your motivation.</p>
                   <MicroCommitment>
                    <p>Look at your notes from your hardest subject. Find one thing you don't fully understand. Write it down on a post-it note and stick it to your school journal as a reminder to ask the teacher tomorrow.</p>
                  </MicroCommitment>
                   <div className="my-10 p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
                      <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Branching Scenario: The Confusion</h4>
                      <p className="text-center text-sm text-stone-500 mb-8">You don't understand the teacher's explanation. What's your move?</p>
                      <div className="space-y-4 max-w-lg mx-auto">
                        <button onClick={() => setScenarioChoice('passive')} className="w-full text-left p-4 bg-stone-50 hover:bg-stone-100 rounded-xl border border-stone-200 transition-all"><strong>Passenger Move:</strong> Say nothing and hope you figure it out later.</button>
                        <button onClick={() => setScenarioChoice('agentic')} className="w-full text-left p-4 bg-stone-50 hover:bg-stone-100 rounded-xl border border-stone-200 transition-all"><strong>Driver Move:</strong> Ask a strategic question to clarify.</button>
                      </div>
                      <AnimatePresence>
                      {scenarioChoice && (
                        <MotionDiv initial={{opacity:0, y:10}} animate={{opacity:1, y:0}} className="mt-8 p-6 rounded-2xl bg-stone-900 text-white">
                          {scenarioChoice === 'passive' && <p><strong className="text-rose-400">Roadblock:</strong> You've missed a turn. The feeling of being "lost" grows, making it harder to catch up later.</p>}
                          {scenarioChoice === 'agentic' && <p><strong className="text-emerald-400">Success:</strong> You get a clear direction, help others in the car, and show the teacher you're a co-pilot, not just a passenger. This is Agentic Engagement.</p>}
                        </MotionDiv>
                      )}
                      </AnimatePresence>
                   </div>
                </ReadingSection>
              )}

              {activeSection === 3 && (
                <ReadingSection title="Roadblocks & Potholes: When the Journey is Unfair." eyebrow="Step 4" icon={ShieldAlert}>
                  <p>Let's be real: not all roads are perfectly paved. If you're from a disadvantaged area, you face real <Highlight description="Systemic barriers like underfunded schools or fewer resources that make academic success harder. These are the potholes and unfair tolls on your educational road.">Structural Conditions</Highlight>. It’s easy to see these roadblocks and think the journey is impossible for you.</p>
                  <p>This creates the most dangerous trap in education: interpreting <Highlight description="A common cognitive trap where academic struggle is seen as proof of personal limitation ('I'm not smart enough'), rather than a sign of a challenging and important task.">Difficulty as Impossibility</Highlight>. The moment the work gets hard, your brain defaults to: "See? This isn't for people like me." The key is to install a high-tech suspension system in your brain: a conscious, deliberate reframe. This is a skill, like learning to change gear.</p>
                  <MicroCommitment>
                    <p>Write this 'Reframe' on a small piece of paper: "This is hard because it's a high-level problem. Solving it is a step toward my goal." Fold it up and put it in your wallet or pencil case.</p>
                  </MicroCommitment>
                  <div className="my-10 p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl flex flex-col items-center gap-6">
                    <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">The Mental Suspension System</h4>
                    <p className="text-sm text-stone-500 -mt-4">Next time you hit a mental pothole, run this script:</p>
                    <div className="w-full max-w-md text-left bg-stone-50 p-6 rounded-2xl border border-stone-200 space-y-4">
                      <p className={`font-mono text-sm transition-opacity ${reframe ? 'text-stone-400' : 'text-rose-600 font-bold'}`}>&gt; Initial thought: "This is too hard. I can't do it."</p>
                      <button onClick={() => setReframe(true)} className={`w-full text-left font-mono text-sm transition-opacity ${reframe ? 'text-blue-600 font-bold' : 'text-stone-400'}`}>&gt; Reframe: "This is hard because it's a high-level problem. This is what progress feels like."</button>
                    </div>
                  </div>
                </ReadingSection>
              )}

              {activeSection === 4 && (
                <ReadingSection title="Your Unique Engine: The Power of Your Story." eyebrow="Step 5" icon={Zap}>
                  <p>Society often focuses on what students from disadvantaged backgrounds lack. This is a deficit mindset. We're flipping it. Your life experiences have equipped your car with a unique, custom-tuned engine that many other students with factory-standard parts don't have. This is your <Highlight description="A core concept from sociology. It means the valuable, valid skills and knowledge you bring from your home and community (e.g., resilience, social intelligence). It is your academic superpower.">Funds of Knowledge</Highlight>.</p>
                  <p>These aren't just 'life skills'; they are high-level cognitive and social assets that give you more horsepower for the Leaving Cert journey. Click the cards below to see how your 'street smarts' translate directly into academic power.</p>
                   <MicroCommitment>
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
                <ReadingSection title="Your Route Plan: Building Your Driver Identity." eyebrow="Step 6" icon={Map}>
                  <p>A Driver identity isn't something you find; it's something you build through deliberate, daily action. It's the route plan that guides you when motivation is low and the road is long. First, arrange your protocol components into your personal pre-drive checklist.</p>
                  
                  <div className="my-10 p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl space-y-6">
                    <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Assemble Your Pre-Drive Checklist</h4>
                    <Reorder.Group axis="y" values={battlePlanItems} onReorder={setBattlePlanItems} className="space-y-3 max-w-md mx-auto">
                      {battlePlanItems.map(item => (
                        <Reorder.Item key={item.id} value={item} className="p-4 bg-stone-50 rounded-xl shadow-sm flex items-center gap-4 cursor-grabbing border border-stone-200">
                          <ChevronsUpDown className="text-stone-400" />
                          <span className="font-bold text-stone-700">{item.text}</span>
                        </Reorder.Item>
                      ))}
                    </Reorder.Group>
                  </div>

                  <div className="my-10 p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl space-y-6">
                    <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Finalise Your Route Plan</h4>
                    <div className="space-y-3"><label className="block text-[10px] font-black text-stone-600 uppercase ml-4 text-left">My Destination (LC Goal):</label><input placeholder="e.g., 500 points to get Engineering at UCD" className="w-full bg-stone-50 border-2 border-stone-100 rounded-xl p-4 focus:border-blue-500 outline-none transition-colors" /></div>
                    <div className="space-y-3"><label className="block text-[10px] font-black text-stone-600 uppercase ml-4 text-left">My Custom Engine (My Advantage):</label><input placeholder="e.g., I'm good at staying calm under pressure." className="w-full bg-stone-50 border-2 border-stone-100 rounded-xl p-4 focus:border-blue-500 outline-none transition-colors" /></div>
                    <div className="space-y-3"><label className="block text-[10px] font-black text-stone-600 uppercase ml-4 text-left">My First Turn (Classroom Hack):</label><input placeholder="e.g., Tomorrow in Maths, I will ask the teacher to explain the 'why' behind one formula." className="w-full bg-stone-50 border-2 border-stone-100 rounded-xl p-4 focus:border-blue-500 outline-none transition-colors" /></div>
                  </div>
                </ReadingSection>
              )}

              <footer className="mt-24 flex items-center justify-between pt-12 border-t border-stone-200/60 px-4">
                <MotionButton whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handlePrev} disabled={activeSection === 0} className={`flex items-center gap-4 bg-stone-100 text-stone-800 px-8 py-4 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all shadow-sm ${activeSection === 0 ? 'opacity-0 pointer-events-none' : ''}`}>
                  <ArrowLeft size={16} /> Prev
                </MotionButton>
                <MotionButton whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handleCompleteSection} className="group relative flex items-center gap-4 bg-stone-900 text-white px-12 py-6 rounded-2xl font-black text-[12px] uppercase tracking-widest hover:bg-blue-600 transition-all shadow-[0_20px_50px_rgba(0,0,0,0.2)] overflow-hidden">
                  <span className="relative z-10">{activeSection === sections.length - 1 ? 'Start Your Engine' : 'Deploy Next Phase'}</span>
                  <ArrowRight size={18} className="relative z-10 group-hover:translate-x-2 transition-transform" />
                </MotionButton>
              </footer>
            </MotionDiv>
          </AnimatePresence>
        </div>
      </main>
    </div>
  );
};
