/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, BrainCircuit, Wrench, BookOpen, BarChart3, ClipboardCheck, ShieldCheck
} from 'lucide-react';

interface NeuroplasticityProtocolModuleProps {
  onBack: () => void;
}

const Highlight = ({ children, description, color = "bg-orange-100/40", textColor = "text-orange-900", decorColor = "decoration-orange-400/40", hoverColor="hover:bg-orange-200/60" }: { children?: React.ReactNode, description: string, color?: string, textColor?: string, decorColor?: string, hoverColor?: string }) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <span className="relative inline-block mx-0.5">
      <button 
        onClick={(e) => {
          e.stopPropagation();
          setIsOpen(!isOpen);
        }}
        className={`relative inline-flex items-center px-2 py-0.5 font-bold ${color} ${textColor} rounded-md cursor-help ${hoverColor} transition-all duration-300 ${decorColor} underline decoration-2 underline-offset-4`}
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
              <p className="font-sans font-bold text-orange-400 mb-2 uppercase tracking-[0.2em] text-[9px]">The Academic Insight</p>
              <p className="text-stone-200 font-medium">{description}</p>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </span>
  );
};

const ReadingSection = ({ title, eyebrow, icon: Icon, children }: { title: string, eyebrow: string, icon: any, children: React.ReactNode }) => (
  <article className="animate-fade-in">
    <header className="mb-12 text-left relative">
      <div className="absolute -left-16 top-0 hidden xl:block">
        <div className="w-12 h-12 rounded-2xl bg-stone-900 flex items-center justify-center text-orange-400 shadow-xl border border-white/10">
          <Icon size={24} />
        </div>
      </div>
      <span className="inline-flex items-center gap-2 px-3 py-1 bg-orange-50 text-orange-600 text-[10px] font-black tracking-[0.4em] uppercase rounded-full mb-4">
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

const MicroCommitment = ({ children }: { children: React.ReactNode }) => (
  <div className="my-12 p-8 bg-orange-50/50 border-2 border-dashed border-orange-200 rounded-3xl">
    <div className="flex items-start gap-5">
      <div className="w-11 h-11 rounded-xl bg-orange-500 text-white flex items-center justify-center shrink-0 mt-1 shadow-lg shadow-orange-500/20">
        <Flag size={20} />
      </div>
      <div>
        <h4 className="font-bold text-orange-800 text-sm uppercase tracking-widest">Your Mission (Under 5 Mins)</h4>
        <div className="text-stone-600 mt-2 font-medium leading-relaxed">
          {children}
        </div>
      </div>
    </div>
  </div>
);

const ActivityRing = ({ progress, color = "#f97316" }: { progress: number, color?: string }) => {
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
const JugglingStudyVisualizer = () => {
    const [scan, setScan] = useState(1);
    const data = [
        { scan: 1, value: 50, label: "Baseline" },
        { scan: 2, value: 80, label: "After 3 Months Practice" },
        { scan: 3, value: 60, label: "After 3 Months No Practice" },
    ];
    const currentData = data[scan-1];

    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">The Juggling Study (2004)</h4>
             <p className="text-center text-sm text-stone-500 mb-8">Proof that learning physically changes your brain's grey matter.</p>
             <div className="w-full max-w-xs mx-auto h-48 flex justify-center items-end">
                <motion.div 
                    className="w-24 bg-orange-400 rounded-t-lg"
                    initial={{height: '50%'}}
                    animate={{height: `${currentData.value}%`}}
                    transition={{type: 'spring', damping: 15, stiffness: 100}}
                />
             </div>
             <p className="text-center font-bold mt-2">{currentData.label}</p>
             <div className="flex justify-center gap-2 mt-4">
                <button onClick={() => setScan(1)} className={`px-3 py-1 text-xs font-bold rounded-full ${scan===1 ? 'bg-orange-500 text-white' : 'bg-stone-100'}`}>Scan 1</button>
                <button onClick={() => setScan(2)} className={`px-3 py-1 text-xs font-bold rounded-full ${scan===2 ? 'bg-orange-500 text-white' : 'bg-stone-100'}`}>Scan 2</button>
                <button onClick={() => setScan(3)} className={`px-3 py-1 text-xs font-bold rounded-full ${scan===3 ? 'bg-orange-500 text-white' : 'bg-stone-100'}`}>Scan 3</button>
             </div>
        </div>
    );
};

const StudyMethodGrader = () => {
    const [method, setMethod] = useState<'passive' | 'active' | null>(null);
    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Study Method Grader</h4>
            <p className="text-center text-sm text-stone-500 mb-6">Which study method sends a stronger signal to build your brain?</p>
             <div className="grid grid-cols-2 gap-4">
                <button onClick={() => setMethod('passive')} className="p-4 bg-rose-50 border-2 border-rose-200 rounded-xl text-center"><strong>Passive Re-reading:</strong> "I'll just read my notes again."</button>
                <button onClick={() => setMethod('active')} className="p-4 bg-emerald-50 border-2 border-emerald-200 rounded-xl text-center"><strong>Active Recall:</strong> "I'll try to explain this from memory."</button>
             </div>
             {method && 
             <motion.div initial={{opacity:0}} animate={{opacity:1}} className="mt-6">
                <h5 className="font-bold text-center">Neuroplasticity Score:</h5>
                <div className="w-full h-8 bg-stone-100 rounded-full mt-2 overflow-hidden">
                    <motion.div 
                        className={`h-full rounded-full ${method === 'active' ? 'bg-emerald-500' : 'bg-rose-500'}`}
                        initial={{width: '0%'}}
                        animate={{width: method === 'active' ? '95%' : '20%'}}
                        transition={{duration: 1}}
                    />
                </div>
                <p className="text-xs text-center mt-2 text-stone-500">{method === 'active' ? 'High-fidelity signal sent. Brain rewiring initiated.' : 'Low-level signal. Minimal rewiring.'}</p>
             </motion.div>}
        </div>
    );
}

// --- MODULE COMPONENT ---
export const NeuroplasticityProtocolModule: React.FC<NeuroplasticityProtocolModuleProps> = ({ onBack }) => {
  const [activeSection, setActiveSection] = useState(0);
  const [unlockedSection, setUnlockedSection] = useState(0);
  
  const sections = [
    { id: 'paradigm-shift', title: 'The Plastic Brain', eyebrow: '01 // The Paradigm Shift', icon: BrainCircuit },
    { id: 'brain-renovation', title: "The Brain's Renovation", eyebrow: '02 // Sculpt & Upgrade', icon: Wrench },
    { id: 'rulebook-of-learning', title: 'The Rulebook of Learning', eyebrow: '03 // Fire Together, Wire Together', icon: BookOpen },
    { id: 'physical-evidence', title: 'The Physical Evidence', eyebrow: '04 // The Juggling Study', icon: BarChart3 },
    { id: 'learning-blueprint', title: 'The Learning Blueprint', eyebrow: '05 // Neuro-Pedagogy', icon: ClipboardCheck },
    { id: 'system-maintenance', title: 'System Maintenance', eyebrow: '06 // Sleep & Stress', icon: ShieldCheck },
  ];

  const handleCompleteSection = () => {
    if (activeSection === unlockedSection && activeSection < sections.length - 1) {
      setUnlockedSection(activeSection + 1);
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

  const progress = ((unlockedSection + 1) / sections.length) * 100;

  return (
    <div className="min-h-screen bg-[#FBFBF9] text-stone-900 font-sans flex flex-col md:flex-row overflow-x-hidden">
      <aside className="w-full md:w-80 bg-white border-r border-stone-200 sticky top-0 md:h-screen z-40 p-8 flex flex-col">
        <div className="flex items-center gap-4 mb-12">
          <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={onBack} className="p-2 rounded-full transition-all border border-stone-200/50 shadow-sm bg-white">
            <ArrowLeft size={16} className="text-stone-700" />
          </motion.button>
          <div>
            <p className="text-[9px] font-black text-orange-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 01</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">Neuroplasticity Protocol</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <motion.div
                  className="w-full bg-orange-500 shadow-[0_0_10px_rgba(249,115,22,0.5)]"
                  initial={{ height: 0 }}
                  animate={{ height: sections.length > 1 ? `${(unlockedSection / (sections.length - 1)) * 100}%` : '0%' }}
              />
          </div>
          {sections.map((section, idx) => {
            const isUnlocked = idx <= unlockedSection;
            const isActive = idx === activeSection;
            const isCompleted = idx < unlockedSection;
            return (
              <button key={section.id} disabled={!isUnlocked} onClick={() => handleJumpToSection(idx)} className={`relative z-10 w-full flex items-center gap-4 p-3 rounded-xl transition-all duration-500 text-left group ${isActive ? 'bg-orange-50 shadow-sm translate-x-2' : ''} ${!isUnlocked ? 'opacity-40 grayscale cursor-not-allowed' : 'hover:bg-stone-50'}`}>
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border-2 transition-all duration-500 ${isCompleted ? 'bg-orange-600 border-orange-600 text-white shadow-lg' : isActive ? 'bg-white border-orange-500 text-orange-600 shadow-xl rotate-12' : 'bg-white border-stone-200 text-stone-300'}`}>
                   {isCompleted ? <CheckCircle2 size={18} /> : isActive ? <section.icon size={18} /> : <Lock size={16} />}
                </div>
                <div className="flex-grow"><p className={`text-[8px] font-black uppercase tracking-widest ${isActive ? 'text-orange-500' : 'text-stone-400'}`}>{section.eyebrow.split('// ')[1]}</p><h4 className={`text-xs font-bold leading-tight ${isActive ? 'text-stone-900' : 'text-stone-500'}`}>{section.title}</h4></div>
              </button>
            );
          })}
        </div>

        <div className="mt-8 border-t border-stone-100 pt-8 flex flex-col items-center">
           <ActivityRing progress={progress} color="#f97316" /><p className="text-[11px] font-black text-stone-900 uppercase tracking-widest text-center">Progress</p>
        </div>
      </aside>

      <main className="flex-grow flex flex-col items-center py-10 md:py-24 px-6 md:px-16 overflow-y-auto h-screen relative">
        <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:32px_32px] opacity-40 pointer-events-none" />
        <div className="w-full max-w-4xl relative z-10">
          <AnimatePresence mode="wait">
            <motion.div key={activeSection} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}>
              {activeSection === 0 && (
                <ReadingSection title="The Plastic Brain." eyebrow="Step 1" icon={BrainCircuit}>
                  <p>For decades, scientists believed your brain was like concrete: it set early in life and couldn't be changed. You were born with a certain level of "smartness," and that was it. We now know this is completely wrong. Your brain is more like plasticine: it is constantly being reshaped by your experiences, thoughts, and actions.</p>
                  <p>This ability to change is called <Highlight description="The brain's ability to modify its own structure and function in response to experience. It's the biological process that underpins all learning and skill acquisition.">Neuroplasticity</Highlight>. During your teenage years, your brain is more 'plastic' than at almost any other time in your life. It's a period of massive reorganization. Understanding how this process works isn't just interesting science; it's the user manual for your own brain.</p>
                </ReadingSection>
              )}
               {activeSection === 1 && (
                <ReadingSection title="The Brain's Renovation." eyebrow="Step 2" icon={Wrench}>
                  <p>Your brain is undergoing two massive renovation projects at once. The first is <Highlight description="The process where the brain eliminates weak or unused synaptic connections. It's like a sculptor chipping away unnecessary stone to reveal the statue underneath. It makes the brain more efficient.">Synaptic Pruning</Highlight>. Your brain is like a gardener, trimming away the connections you don't use to free up resources for the ones you do. This is the "use it or lose it" principle in action. If you don't practice something, your brain physically dismantles the wiring for it.</p>
                  <p>The second project is <Highlight description="The process of coating axons in a fatty sheath called myelin. This insulation makes nerve signals travel up to 100 times faster, allowing for quicker and more synchronized thinking.">Myelination</Highlight>. Think of this as upgrading a bumpy country road to a motorway. Your brain wraps insulation (myelin) around the neural pathways you use often, making them super-fast and efficient. Practice doesn't just make perfect; it makes *faster*.</p>
                </ReadingSection>
              )}
               {activeSection === 2 && (
                <ReadingSection title="The Rulebook of Learning." eyebrow="Step 3" icon={BookOpen}>
                  <p>How does your brain know which connections to prune and which to myelinate? It follows a simple, powerful rule from 1949 known as <Highlight description="The foundational principle of neuroplasticity, often summarized as 'Cells that fire together, wire together.' It means that when two neurons are active at the same time, the connection between them gets stronger.">Hebbian Theory</Highlight>: "Cells that fire together, wire together." Every time you have a thought or practice a skill, you're sending an electrical signal through a chain of neurons. The more you fire that chain, the stronger the physical connections between those neurons become.</p>
                  <p>We can think of this with two analogies. For strengthening connections, imagine a field of tall grass. The first time you walk across (study a topic once), you bend the grass, but it springs back. If you walk the same "Desire Path" repeatedly, you wear a permanent trail. For speed, think of an "Orchestra." To make music, different sections need their signals to arrive at the same time. Myelination is your brain's conductor, adjusting the speed of different pathways so your thoughts are perfectly timed and synchronized.</p>
                </ReadingSection>
              )}
              {activeSection === 3 && (
                <ReadingSection title="The Physical Evidence." eyebrow="Step 4" icon={BarChart3}>
                  <p>This isn't just a theory; we can see it happen. In a landmark 2004 study, scientists took brain scans of people who had never juggled before. Then, they taught them to juggle and scanned their brains again after three months of practice. The result? A measurable, physical increase in the amount of grey matter in the parts of the brain responsible for tracking moving objects.</p>
                  <p>But here's the crucial part: they then told the jugglers to stop practicing for three months. The final brain scan showed that those same areas of the brain had shrunk back down again. This is the "use it or lose it" principle in action. Your brain is an efficient machine; it will not waste energy maintaining a skill you aren't using. Your intelligence is not fixed; it is a dynamic landscape that you are actively shaping every day.</p>
                  <JugglingStudyVisualizer />
                </ReadingSection>
              )}
              {activeSection === 4 && (
                <ReadingSection title="The Learning Blueprint." eyebrow="Step 5" icon={ClipboardCheck}>
                    <p>This science gives us a blueprint for effective learning. It tells us *why* certain study techniques work and others don't. For example, <Highlight description="Reviewing material at increasing intervals (e.g., 1 day, 3 days, 1 week). This strategy works by reactivating neural pathways just as they begin to weaken, signaling to the brain that they are important and should be kept.">Spaced Repetition</Highlight> is powerful because it's the biological signal to "keep this connection" and "myelinate this pathway." Cramming, on the other hand, is like a single, intense stampede across the grass—it doesn't create a lasting path.</p>
                    <p>Similarly, <Highlight description="Forcing your brain to retrieve information from scratch (e.g., using flashcards or practice tests) instead of passively re-reading it. This high-effort activity generates a much stronger 'fire together, wire together' signal.">Active Recall</Highlight> is far more effective than passive re-reading. Why? Because re-reading is a low-effort task that sends a weak signal. Active recall forces your brain to reconstruct the entire neural pathway from scratch, generating an intense "coincidence detection" signal that triggers powerful synaptic strengthening.</p>
                    <StudyMethodGrader />
                </ReadingSection>
              )}
               {activeSection === 5 && (
                <ReadingSection title="System Maintenance." eyebrow="Step 6" icon={ShieldCheck}>
                    <p>Finally, your brain's ability to change depends on how well you maintain it. Sleep isn't a luxury; it's the brain's cleaning and filing cycle. During deep sleep, your brain scales down the synaptic connections you made during the day, keeping the important ones and getting rid of the noise. Without enough sleep, your brain becomes saturated and "noisy," making it impossible to learn new things.</p>
                    <p>Stress is the other enemy of plasticity. Chronic stress floods your brain with cortisol, a hormone that actively inhibits the growth of new connections and can even accelerate pruning in important areas like your memory centres. Managing stress isn't just for your mental health; it's a prerequisite for effective learning. By understanding these biological rules, you can stop working against your brain and start working with it.</p>
                    <MicroCommitment>
                        <p>Tonight, put your phone away 30 minutes before you plan to sleep. This small act of "sleep hygiene" can have a huge impact on your brain's ability to consolidate what you learned today.</p>
                    </MicroCommitment>
                </ReadingSection>
              )}
              <footer className="mt-24 flex items-center justify-between pt-12 border-t border-stone-200/60 px-4">
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handlePrev} disabled={activeSection === 0} className={`flex items-center gap-4 bg-stone-100 text-stone-800 px-8 py-4 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all shadow-sm ${activeSection === 0 ? 'opacity-0 pointer-events-none' : ''}`}>
                  <ArrowLeft size={16} /> Prev
                </motion.button>
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handleCompleteSection} className="group relative flex items-center gap-4 bg-stone-900 text-white px-12 py-6 rounded-2xl font-black text-[12px] uppercase tracking-widest hover:bg-orange-600 transition-all shadow-[0_20px_50px_rgba(0,0,0,0.2)] overflow-hidden">
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