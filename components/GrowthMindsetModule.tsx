
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, Zap, ArrowRight, 
  BrainCircuit, Cpu,
  Activity, Lock, Flag, RotateCcw, MessageSquareQuote
} from 'lucide-react';

type ModuleProgress = {
  unlockedSection: number;
};

interface GrowthMindsetModuleProps {
  onBack: () => void;
  progress: ModuleProgress;
  onProgressUpdate: (progress: ModuleProgress) => void;
}

const Highlight = ({ children, description, color = "bg-amber-100/40" }: { children?: React.ReactNode, description: string, color?: string }) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <span className="relative inline-block mx-0.5">
      <button 
        onClick={(e) => {
          e.stopPropagation();
          setIsOpen(!isOpen);
        }}
        className={`relative inline-flex items-center px-2 py-0.5 font-bold ${color} rounded-md cursor-help hover:bg-amber-200/60 transition-all duration-300 decoration-amber-400/40 underline decoration-2 underline-offset-4 text-amber-900`}
      >
        <span className="not-italic">{children}</span>
      </button>
      <AnimatePresence>
        {isOpen && (
          <>
            <div className="fixed inset-0 z-[60]" onClick={() => setIsOpen(false)} />
            <motion.div 
              initial={{ opacity: 0, scale: 0.9, y: 10, x: "-50%" }}
              animate={{ opacity: 1, scale: 1, y: 0, x: "-50%" }}
              exit={{ opacity: 0, scale: 0.9, y: 10, x: "-50%" }}
              className="absolute z-[70] bottom-full left-1/2 mb-6 w-72 p-6 bg-stone-900/95 text-white text-xs rounded-2xl shadow-2xl pointer-events-auto leading-relaxed border border-white/10 backdrop-blur-xl whitespace-normal text-left"
              style={{ transformOrigin: 'bottom center' }}
            >
              <div className="absolute bottom-0 left-1/2 -translate-x-1/2 translate-y-full w-0 h-0 border-l-[10px] border-l-transparent border-r-[10px] border-r-transparent border-t-[10px] border-t-stone-900/95"></div>
              <p className="font-sans font-bold text-amber-400 mb-2 uppercase tracking-[0.2em] text-[9px]">The Academic Insight</p>
              <p className="text-stone-200 font-medium">{description}</p>
            </motion.div>
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
        <div className="w-12 h-12 rounded-2xl bg-stone-900 flex items-center justify-center text-amber-400 shadow-xl border border-white/10">
          <Icon size={24} />
        </div>
      </div>
      <span className="inline-flex items-center gap-2 px-3 py-1 bg-amber-50 text-amber-600 text-[10px] font-black tracking-[0.4em] uppercase rounded-full mb-4">
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
  <div className="my-12 p-8 bg-amber-50/50 border-2 border-dashed border-amber-200 rounded-3xl">
    <div className="flex items-start gap-5">
      <div className="w-11 h-11 rounded-xl bg-amber-500 text-white flex items-center justify-center shrink-0 mt-1 shadow-lg shadow-amber-500/20">
        <Flag size={20} />
      </div>
      <div>
        <h4 className="font-bold text-amber-800 text-sm uppercase tracking-widest">Your Mission (Under 5 Mins)</h4>
        <div className="text-stone-600 mt-2 font-medium leading-relaxed">
          {children}
        </div>
      </div>
    </div>
  </div>
);

const ActivityRing = ({ progress, color = "#f59e0b" }: { progress: number, color?: string }) => {
  const radius = 35;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (progress / 100) * circumference;

  return (
    <div className="relative flex items-center justify-center w-24 h-24 mx-auto mb-4">
      <svg className="w-full h-full -rotate-90 overflow-visible" viewBox="0 0 96 96">
        <circle cx="48" cy="48" r={radius} stroke={color} strokeWidth="10" fill="transparent" className="opacity-10"/>
        <motion.circle cx="48" cy="48" r={radius} stroke={color} strokeWidth="10" fill="transparent" strokeDasharray={circumference} initial={{ strokeDashoffset: circumference }} animate={{ strokeDashoffset: offset }} transition={{ duration: 1.5, ease: "easeOut" }} strokeLinecap="round" style={{ filter: `drop-shadow(0 0 8px ${color}55)` }}/>
      </svg>
    </div>
  );
};

// --- INTERACTIVE COMPONENTS ---

const MindsetDiagnostic = () => {
  const [answers, setAnswers] = useState<( 'fixed' | 'growth' | null)[]>([null, null, null]);
  const score = answers.filter(a => a === 'growth').length;
  
  const handleAnswer = (index: number, type: 'fixed' | 'growth') => {
    const newAnswers = [...answers];
    newAnswers[index] = type;
    setAnswers(newAnswers);
  };
  
  const isComplete = answers.every(a => a !== null);

  return (
    <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
      <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Mindset Diagnostic</h4>
      <p className="text-center text-sm text-stone-500 mb-8">Which thought sounds more like you in a tough situation?</p>
      <div className="space-y-6">
        {/* Question 1 */}
        <div>
          <p className="text-sm font-bold text-center text-stone-600 mb-3">When I fail at something...</p>
          <div className="grid grid-cols-2 gap-3">
            <button onClick={() => handleAnswer(0, 'fixed')} className={`p-4 rounded-xl text-xs text-center border-2 ${answers[0] === 'fixed' ? 'bg-rose-500 text-white border-rose-500' : 'bg-stone-50 border-stone-200 hover:bg-stone-100'}`}>A) I feel like I'm a failure.</button>
            <button onClick={() => handleAnswer(0, 'growth')} className={`p-4 rounded-xl text-xs text-center border-2 ${answers[0] === 'growth' ? 'bg-emerald-500 text-white border-emerald-500' : 'bg-stone-50 border-stone-200 hover:bg-stone-100'}`}>B) I feel like I need to try a new strategy.</button>
          </div>
        </div>
        {/* Question 2 */}
         <div>
          <p className="text-sm font-bold text-center text-stone-600 mb-3">If a subject is hard for me...</p>
          <div className="grid grid-cols-2 gap-3">
            <button onClick={() => handleAnswer(1, 'fixed')} className={`p-4 rounded-xl text-xs text-center border-2 ${answers[1] === 'fixed' ? 'bg-rose-500 text-white border-rose-500' : 'bg-stone-50 border-stone-200 hover:bg-stone-100'}`}>A) It means I'm probably not smart enough for it.</button>
            <button onClick={() => handleAnswer(1, 'growth')} className={`p-4 rounded-xl text-xs text-center border-2 ${answers[1] === 'growth' ? 'bg-emerald-500 text-white border-emerald-500' : 'bg-stone-50 border-stone-200 hover:bg-stone-100'}`}>B) It means I have a great opportunity to learn.</button>
          </div>
        </div>
        {/* Question 3 */}
         <div>
          <p className="text-sm font-bold text-center text-stone-600 mb-3">I believe my intelligence is something...</p>
          <div className="grid grid-cols-2 gap-3">
            <button onClick={() => handleAnswer(2, 'fixed')} className={`p-4 rounded-xl text-xs text-center border-2 ${answers[2] === 'fixed' ? 'bg-rose-500 text-white border-rose-500' : 'bg-stone-50 border-stone-200 hover:bg-stone-100'}`}>A) That I can't change very much.</button>
            <button onClick={() => handleAnswer(2, 'growth')} className={`p-4 rounded-xl text-xs text-center border-2 ${answers[2] === 'growth' ? 'bg-emerald-500 text-white border-emerald-500' : 'bg-stone-50 border-stone-200 hover:bg-stone-100'}`}>B) That I can grow with effort.</button>
          </div>
        </div>
      </div>
      <AnimatePresence>
      {isComplete && (
        <motion.div initial={{opacity:0, y:10}} animate={{opacity:1, y:0}} className="mt-8 p-6 rounded-2xl bg-stone-900 text-white">
          <p className="text-center font-bold">
            {score === 3 && <span className="text-emerald-400">Result: You're operating with a strong Growth Mindset OS!</span>}
            {score === 2 && <span className="text-amber-400">Result: You're leaning towards Growth, with some Fixed-Mindset code still running.</span>}
            {score < 2 && <span className="text-rose-400">Result: Your system is currently running a Fixed-Mindset OS. Time for an upgrade!</span>}
          </p>
        </motion.div>
      )}
      </AnimatePresence>
    </div>
  );
};

const NeuroplasticityVisualizer = () => {
  const [connections, setConnections] = useState(0);

  return (
    <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
      <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">The Brain Rewiring Simulator</h4>
      <p className="text-center text-sm text-stone-500 mb-8">Every time you practice, you strengthen the physical connections in your brain.</p>
      
      <div className="h-40 flex justify-center items-center">
        <svg width="250" height="100" viewBox="0 0 250 100">
          {/* Neurons */}
          <circle cx="50" cy="50" r="20" fill="#f59e0b" />
          <circle cx="200" cy="50" r="20" fill="#f59e0b" />
          <AnimatePresence>
            {connections > 0 && Array.from({length: connections}).map((_, i) => (
              <motion.path 
                key={i}
                d={`M 70 50 Q 125 ${50 + (i - (connections-1)/2) * 15} 180 50`}
                fill="none"
                stroke="#f59e0b"
                initial={{ pathLength: 0, opacity: 0, strokeWidth: 1 }}
                animate={{ pathLength: 1, opacity: Math.max(0.1, i / connections), strokeWidth: 1 + i*0.5 }}
                transition={{ duration: 0.5 }}
              />
            ))}
          </AnimatePresence>
        </svg>
      </div>
      <div className="text-center">
        <button onClick={() => setConnections(c => Math.min(c + 1, 5))} className="px-6 py-3 bg-amber-500 text-white font-bold rounded-lg shadow-lg hover:bg-amber-600 transition-colors">
          Practice a Skill
        </button>
        <button onClick={() => setConnections(0)} className="ml-4 text-xs text-stone-400">Reset</button>
      </div>
    </div>
  );
}

const ReframeChallenge = () => {
    const [thought, setThought] = useState("I'm just not a maths person.");
    const [reframe, setReframe] = useState('');
    const containsYet = reframe.toLowerCase().includes('yet');

    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">The "Yet" Reframe Challenge</h4>
            <p className="text-center text-sm text-stone-500 mb-8">Upgrade this fixed thought into a growth mindset statement using the power of "yet".</p>
            <div className="p-6 bg-rose-50 border border-rose-200 rounded-2xl mb-4">
                <p className="text-rose-800 text-center font-mono"><strong>Fixed Thought:</strong> "{thought}"</p>
            </div>
            <textarea 
                value={reframe}
                onChange={(e) => setReframe(e.target.value)}
                placeholder="Your growth reframe..."
                className="w-full h-24 bg-stone-50 border-2 border-stone-100 rounded-2xl p-4 focus:border-amber-500 outline-none transition-colors"
            />
             <AnimatePresence>
                {containsYet && (
                <motion.div initial={{opacity:0, y:10}} animate={{opacity:1, y:0}} className="mt-4 p-4 rounded-xl bg-emerald-50 text-emerald-700 text-center text-sm font-bold">
                    Excellent! You've opened up the possibility of future growth.
                </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};


// --- MODULE COMPONENT ---
export const GrowthMindsetModule: React.FC<GrowthMindsetModuleProps> = ({ onBack, progress, onProgressUpdate }) => {
  const [activeSection, setActiveSection] = useState(progress.unlockedSection);
  const unlockedSection = progress.unlockedSection;
  
  const sections = [
    { id: 'two-brains', title: 'The Two Brains: Fixed vs. Growth', eyebrow: '01 // The Operating System', icon: Cpu },
    { id: 'brain-muscle', title: 'Your Brain is Plastic', eyebrow: '02 // The Hardware Upgrade', icon: BrainCircuit },
    { id: 'power-of-yet', title: 'The Most Powerful Word', eyebrow: '03 // The Software Patch', icon: RotateCcw },
    { id: 'effort-is-key', title: 'Effort is the Real Talent', eyebrow: '04 // The Engine', icon: Zap },
    { id: 'feedback-fuel', title: 'Feedback is Fuel, Not a Verdict', eyebrow: '05 // The Navigation Data', icon: MessageSquareQuote },
    { id: 'install-os', title: 'Installing Your Growth OS', eyebrow: '06 // System Integration', icon: Activity },
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
          <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={onBack} className="p-2 rounded-full transition-all border border-stone-200/50 shadow-sm bg-white">
            <ArrowLeft size={16} className="text-stone-700" />
          </motion.button>
          <div>
            <p className="text-[9px] font-black text-amber-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 01</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">The Growth Protocol</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <motion.div
                  className="w-full bg-amber-500 shadow-[0_0_10px_rgba(245,158,11,0.5)]"
                  style={{ height: `${progressPercentage}%` }}
              />
          </div>
          {sections.map((section, idx) => {
            const isUnlocked = idx <= unlockedSection;
            const isActive = idx === activeSection;
            const isCompleted = idx < unlockedSection;
            return (
              <button key={section.id} disabled={!isUnlocked} onClick={() => handleJumpToSection(idx)} className={`relative z-10 w-full flex items-center gap-4 p-3 rounded-xl transition-all duration-500 text-left group ${isActive ? 'bg-amber-50 shadow-sm translate-x-2' : ''} ${!isUnlocked ? 'opacity-40 grayscale cursor-not-allowed' : 'hover:bg-stone-50'}`}>
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border-2 transition-all duration-500 ${isCompleted ? 'bg-amber-600 border-amber-600 text-white shadow-lg' : isActive ? 'bg-white border-amber-500 text-amber-600 shadow-xl rotate-12' : 'bg-white border-stone-200 text-stone-300'}`}>
                   {isCompleted ? <CheckCircle2 size={18} /> : isActive ? <section.icon size={18} /> : <Lock size={16} />}
                </div>
                <div className="flex-grow"><p className={`text-[8px] font-black uppercase tracking-widest ${isActive ? 'text-amber-500' : 'text-stone-400'}`}>{section.eyebrow.split('// ')[1]}</p><h4 className={`text-xs font-bold leading-tight ${isActive ? 'text-stone-900' : 'text-stone-500'}`}>{section.title}</h4></div>
              </button>
            );
          })}
        </div>

        <div className="mt-8 border-t border-stone-100 pt-8 flex flex-col items-center">
           <ActivityRing progress={progressPercentage} color="#f59e0b" /><p className="text-[11px] font-black text-stone-900 uppercase tracking-widest text-center">Progress</p>
        </div>
      </aside>

      <main className="flex-grow flex flex-col items-center py-10 md:py-24 px-6 md:px-16 overflow-y-auto h-screen relative">
        <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:32px_32px] opacity-40 pointer-events-none" />
        <div className="w-full max-w-4xl relative z-10">
          <AnimatePresence mode="wait">
            <motion.div key={activeSection} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}>
              {activeSection === 0 && (
                <ReadingSection title="The Two Brains: Fixed vs. Growth." eyebrow="Step 1" icon={Cpu}>
                  <p>Imagine your brain is a computer. Some people believe it comes with "read-only" memory. You're born with a certain amount of intelligence, and that's that. This is the <Highlight description="The belief that your intelligence and abilities are static, unchangeable traits. People with this mindset avoid challenges to avoid 'proving' their limitations.">Fixed Mindset</Highlight>. It's an operating system that sees effort as pointless and failure as a permanent judgement.</p>
                  <p>But the science shows your brain is more like a rewritable drive. Every time you learn something new, you're installing new software. This is the <Highlight description="The belief that intelligence can be developed through dedication and hard work. This view creates a love of learning and a resilience that is essential for great accomplishment.">Growth Mindset</Highlight>. It's an operating system that sees challenges as opportunities and failure as feedback. Which OS is your brain running right now?</p>
                  <MindsetDiagnostic />
                  <MicroCommitment>
                    <p>Listen to how you talk about school today. Catch one "fixed" thought (e.g., "I'm bad at Irish") and just notice it. You don't have to change it yet, just acknowledge you're running that piece of code.</p>
                  </MicroCommitment>
                </ReadingSection>
              )}
               {activeSection === 1 && (
                <ReadingSection title="Your Brain is Plastic." eyebrow="Step 2" icon={BrainCircuit}>
                  <p>The single most important discovery in neuroscience is that your brain is not fixed. It physically changes based on what you do. This is called <Highlight description="The brain's ability to reorganize itself by forming new neural connections throughout life. It's the biological basis of learning and memory.">Neuroplasticity</Highlight>. Think of learning a new maths formula like walking through a forest. The first time, it's hard work, and there's no clear path.</p>
                  <p>But if you walk that same path every day (i.e., you practice the formula), you wear down a clear trail. In your brain, this is real: the connections between your brain cells (neurons) get stronger, faster, and more efficient. You are literally building the road to knowledge in your head. Every bit of effort you put in is a construction project in your own brain.</p>
                  <NeuroplasticityVisualizer />
                   <MicroCommitment>
                    <p>Pick the one school subject you find hardest. Spend just five minutes tonight reviewing a topic from it. You just sent a work crew to start clearing a new path in your brain's forest.</p>
                  </MicroCommitment>
                </ReadingSection>
              )}
               {activeSection === 2 && (
                <ReadingSection title="The Most Powerful Word." eyebrow="Step 3" icon={RotateCcw}>
                    <p>A fixed mindset speaks in absolutes: "I can't do this." "I'm not good at this." These are dead ends. They shut down effort and kill motivation. The growth mindset has a simple but incredibly powerful software patch for this bug: the word "yet."</p>
                    <p>Adding "yet" to the end of a fixed statement instantly changes it from a verdict into a journey. "I can't do this" becomes "I can't do this... yet." "I'm not good at this" becomes "I'm not good at this... yet." It's a linguistic trick that tells your brain the story isn't over. It opens the door to new strategies and further effort, keeping your motivation circuit online.</p>
                    <ReframeChallenge />
                    <MicroCommitment>
                        <p>The next time you hear a friend (or yourself) say a "fixed" statement like "I don't get this," add a gentle "...yet?" at the end. You're installing the software patch for them.</p>
                    </MicroCommitment>
                </ReadingSection>
              )}
               {activeSection === 3 && (
                <ReadingSection title="Effort is the Real Talent." eyebrow="Step 4" icon={Zap}>
                    <p>Our culture loves the myth of "natural talent." We see someone brilliant at something and assume they were just born that way. This is one of the most damaging ideas in education. It teaches us that if something doesn't come easily, we must not be "talented" at it.</p>
                    <p>The science of expertise shows this is a lie. Talent is a starting point, but effort is the engine of growth. It is the <Highlight description="Focused, strategic practice that pushes you slightly beyond your current comfort zone. This is the specific type of effort that triggers neuroplasticity and builds skill.">Deliberate Practice</Highlight> that forges the strong neural pathways we saw earlier. A growth mindset understands that effort isn't a sign of weakness; it's the process of getting smarter.</p>
                    <MicroCommitment>
                        <p>Identify one area where you rely on "talent". Now, identify one tiny, effortful action you can take to actually improve it. (e.g., If you're 'naturally good' at English, spend 10 minutes learning one new sophisticated word).</p>
                    </MicroCommitment>
                </ReadingSection>
              )}
               {activeSection === 4 && (
                <ReadingSection title="Feedback is Fuel, Not a Verdict." eyebrow="Step 5" icon={MessageSquareQuote}>
                  <p>A fixed mindset hears criticism and thinks: "They're telling me I'm stupid." It treats feedback as a final verdict on your ability. This is why people with a fixed mindset get defensive or give up when they get a bad grade or tough correction from a teacher.</p>
                  <p>A growth mindset hears the exact same criticism and thinks: "They're giving me data I can use to improve." It sees feedback as fuel for the engine. It's not about you, it's about your current strategy. A bad grade isn't a label, it's a diagnostic telling you where the path needs more work. Learning to separate your performance from your identity is a critical upgrade.</p>
                  <MicroCommitment>
                    <p>Go back to a piece of work where you got a lower grade than you wanted. Find one comment from the teacher and write down what strategy it's telling you to try next time.</p>
                  </MicroCommitment>
                </ReadingSection>
              )}
               {activeSection === 5 && (
                <ReadingSection title="Installing Your Growth OS." eyebrow="Step 6" icon={Activity}>
                  <p>A growth mindset isn't a magical incantation. It's a new operating system that you have to consciously choose to run every day. It's built through small, consistent habits: the way you talk to yourself, the way you react to mistakes, and the way you approach a challenge.</p>
                  <p>By internalising these ideas, you can start to build an identity based on growth. You stop being "the person who is bad at Maths" and become "the person who is working to get better at Maths." This shift is the foundation of resilience and the key to unlocking your academic potential. It's time to finalise the installation.</p>
                   <MicroCommitment>
                    <p>Write down your favourite "Growth Mindset Mantra" from this module. Stick it on your bedroom wall, your mirror, or the inside of your school journal. Make it visible.</p>
                  </MicroCommitment>
                </ReadingSection>
              )}
              <footer className="mt-24 flex items-center justify-between pt-12 border-t border-stone-200/60 px-4">
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handlePrev} disabled={activeSection === 0} className={`flex items-center gap-4 bg-stone-100 text-stone-800 px-8 py-4 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all shadow-sm ${activeSection === 0 ? 'opacity-0 pointer-events-none' : ''}`}>
                  <ArrowLeft size={16} /> Prev
                </motion.button>
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handleCompleteSection} className="group relative flex items-center gap-4 bg-stone-900 text-white px-12 py-6 rounded-2xl font-black text-[12px] uppercase tracking-widest hover:bg-amber-600 transition-all shadow-[0_20px_50px_rgba(0,0,0,0.2)] overflow-hidden">
                  <span className="relative z-10">{activeSection === sections.length - 1 ? 'Finish Protocol' : 'Deploy Next Phase'}</span>
                  <ArrowRight size={18} className="relative z-10 group-hover:translate-x-2 transition-transform" />
                </motion.button>
              </footer>
            </motion.div>
          </AnimatePresence>
        </div>
      </main>
    </div>
  );
};
