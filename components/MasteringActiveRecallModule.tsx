

/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, BarChart3, BrainCircuit, XCircle, Share2, HeartPulse, Wrench, Check, X
} from 'lucide-react';

interface MasteringActiveRecallModuleProps {
  onBack: () => void;
}

const Highlight = ({ children, description, color = "bg-indigo-100/40", textColor = "text-indigo-900", decorColor = "decoration-indigo-400/40", hoverColor="hover:bg-indigo-200/60" }: { children?: React.ReactNode, description: string, color?: string, textColor?: string, decorColor?: string, hoverColor?: string }) => {
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
              <p className="font-sans font-bold text-indigo-400 mb-2 uppercase tracking-[0.2em] text-[9px]">The Academic Insight</p>
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
        <div className="w-12 h-12 rounded-2xl bg-stone-900 flex items-center justify-center text-indigo-400 shadow-xl border border-white/10">
          <Icon size={24} />
        </div>
      </div>
      <span className="inline-flex items-center gap-2 px-3 py-1 bg-indigo-50 text-indigo-600 text-[10px] font-black tracking-[0.4em] uppercase rounded-full mb-4">
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
  <div className="my-12 p-8 bg-indigo-50/50 border-2 border-dashed border-indigo-200 rounded-3xl">
    <div className="flex items-start gap-5">
      <div className="w-11 h-11 rounded-xl bg-indigo-500 text-white flex items-center justify-center shrink-0 mt-1 shadow-lg shadow-indigo-500/20">
        <Flag size={20} />
      </div>
      <div>
        <h4 className="font-bold text-indigo-800 text-sm uppercase tracking-widest">Your Mission (Under 5 Mins)</h4>
        <div className="text-stone-600 mt-2 font-medium leading-relaxed">
          {children}
        </div>
      </div>
    </div>
  </div>
);

const ActivityRing = ({ progress, color = "#4f46e5" }: { progress: number, color?: string }) => {
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
const StrengthMeter = () => {
    const [method, setMethod] = useState<'passive'|'active'|null>(null);
    let retrieval = 10, storage = 10;
    if (method === 'passive') { retrieval = 90; storage = 15; }
    if (method === 'active') { retrieval = 40; storage = 85; }
    
    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Storage vs. Retrieval Strength</h4>
             <p className="text-center text-sm text-stone-500 mb-8">Choose a study method to see its effect on your memory.</p>
             <div className="grid grid-cols-2 gap-4 mb-8">
                <div className="text-center">
                    <p className="font-bold text-sm text-fuchsia-600 mb-2">Retrieval Strength (Feeling)</p>
                    <div className="w-full h-6 bg-stone-100 rounded-full"><motion.div className="h-full bg-fuchsia-500 rounded-full" initial={{width: "10%"}} animate={{width: `${retrieval}%`}} /></div>
                </div>
                <div className="text-center">
                    <p className="font-bold text-sm text-indigo-600 mb-2">Storage Strength (Learning)</p>
                    <div className="w-full h-6 bg-stone-100 rounded-full"><motion.div className="h-full bg-indigo-500 rounded-full" initial={{width: "10%"}} animate={{width: `${storage}%`}} /></div>
                </div>
            </div>
             <div className="flex justify-center gap-4">
                <button onClick={() => setMethod('passive')} className="px-4 py-2 bg-fuchsia-100 text-fuchsia-800 text-xs font-bold rounded-lg">Passive Review</button>
                <button onClick={() => setMethod('active')} className="px-4 py-2 bg-indigo-100 text-indigo-800 text-xs font-bold rounded-lg">Active Recall</button>
             </div>
        </div>
    );
};

const StudyMethodAuditor = () => {
    const methods = [
        { id: 1, name: "Re-reading your notes", type: "passive", explanation: "This feels productive because it increases fluency, but it's a weak signal for long-term memory. It's the classic 'Illusion of Competence'." },
        { id: 2, name: "Doing a past paper", type: "active", explanation: "This is a gold-standard active recall method. The struggle to retrieve information is exactly what builds strong, durable memory." },
        { id: 3, name: "Highlighting a textbook", type: "passive", explanation: "This is a form of passive review. It involves selecting information but doesn't require you to retrieve it from memory, so learning is minimal." },
        { id: 4, name: "Explaining it to a friend", type: "active", explanation: "Excellent! To teach something, you must first retrieve it and organize it coherently. This is a very powerful form of active recall." },
        { id: 5, name: "Watching a YouTube video", type: "passive", explanation: "Like re-reading, this is passive consumption. While useful for first-pass understanding, it doesn't build memory unless you actively test yourself on it afterwards." },
        { id: 6, name: "Creating flashcards", type: "active", explanation: "This is active recall IF you make them from memory. If you just copy from the book, it's passive. The real power comes from testing yourself with them later." },
    ];
    const [selectedId, setSelectedId] = useState<number | null>(null);
    const selectedMethod = methods.find(m => m.id === selectedId);

    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Study Method Auditor</h4>
            <p className="text-center text-sm text-stone-500 mb-8">Click a study method to get your Active Recall rating.</p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {methods.map(method => (
                    <button 
                        key={method.id} 
                        onClick={() => setSelectedId(method.id)}
                        className={`p-4 rounded-xl text-sm font-bold border-2 transition-all ${selectedId === method.id ? 'bg-stone-200 border-stone-300' : 'bg-stone-50 hover:bg-stone-100 border-stone-200'}`}
                    >
                        {method.name}
                    </button>
                ))}
            </div>
            <AnimatePresence>
                {selectedMethod && (
                    <motion.div 
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: 10 }}
                        className={`mt-6 p-4 rounded-2xl border-2 ${selectedMethod.type === 'active' ? 'bg-emerald-50 border-emerald-200' : 'bg-rose-50 border-rose-200'}`}
                    >
                        <div className="flex items-center gap-3">
                            <div className={`w-10 h-10 rounded-full flex items-center justify-center text-white ${selectedMethod.type === 'active' ? 'bg-emerald-500' : 'bg-rose-500'}`}>
                                {selectedMethod.type === 'active' ? <Check size={20}/> : <X size={20}/>}
                            </div>
                            <div>
                                <h5 className={`font-bold ${selectedMethod.type === 'active' ? 'text-emerald-800' : 'text-rose-800'}`}>
                                    {selectedMethod.type === 'active' ? 'Active Recall' : 'Passive Review'}
                                </h5>
                                <p className="text-xs mt-1">{selectedMethod.explanation}</p>
                            </div>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};


// --- MODULE COMPONENT ---
export const MasteringActiveRecallModule: React.FC<{onBack: () => void}> = ({ onBack }) => {
  const [activeSection, setActiveSection] = useState(0);
  const [unlockedSection, setUnlockedSection] = useState(0);
  
  const sections = [
    { id: 'great-forgetting', title: 'The Great Forgetting', eyebrow: '01 // The Problem', icon: BarChart3 },
    { id: 'test-effect', title: 'The "Test Effect"', eyebrow: '02 // The Mechanism', icon: BrainCircuit },
    { id: 'dropout-fallacy', title: 'The "Dropout" Fallacy', eyebrow: '03 // The Common Mistake', icon: XCircle },
    { id: 'transfer-effect', title: 'Beyond Rote Memory', eyebrow: '04 // The Transfer Effect', icon: Share2 },
    { id: 'anxiety-myth', title: 'The Anxiety Myth', eyebrow: '05 // The Surprising Truth', icon: HeartPulse },
    { id: 'recall-toolkit', title: 'Your Recall Toolkit', eyebrow: '06 // The Action Plan', icon: Wrench },
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
            <p className="text-[9px] font-black text-indigo-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 02</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">Mastering Active Recall</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <motion.div
                  className="w-full bg-indigo-500 shadow-[0_0_10px_rgba(79,70,229,0.5)]"
                  initial={{ height: 0 }}
                  animate={{ height: sections.length > 1 ? `${(unlockedSection / (sections.length - 1)) * 100}%` : '0%' }}
              />
          </div>
          {sections.map((section, idx) => {
            const isUnlocked = idx <= unlockedSection;
            const isActive = idx === activeSection;
            const isCompleted = idx < unlockedSection;
            return (
              <button key={section.id} disabled={!isUnlocked} onClick={() => handleJumpToSection(idx)} className={`relative z-10 w-full flex items-center gap-4 p-3 rounded-xl transition-all duration-500 text-left group ${isActive ? 'bg-indigo-50 shadow-sm translate-x-2' : ''} ${!isUnlocked ? 'opacity-40 grayscale cursor-not-allowed' : 'hover:bg-stone-50'}`}>
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border-2 transition-all duration-500 ${isCompleted ? 'bg-indigo-600 border-indigo-600 text-white shadow-lg' : isActive ? 'bg-white border-indigo-500 text-indigo-600 shadow-xl rotate-12' : 'bg-white border-stone-200 text-stone-300'}`}>
                   {isCompleted ? <CheckCircle2 size={18} /> : isActive ? <section.icon size={18} /> : <Lock size={16} />}
                </div>
                <div className="flex-grow"><p className={`text-[8px] font-black uppercase tracking-widest ${isActive ? 'text-indigo-500' : 'text-stone-400'}`}>{section.eyebrow.split('// ')[1]}</p><h4 className={`text-xs font-bold leading-tight ${isActive ? 'text-stone-900' : 'text-stone-500'}`}>{section.title}</h4></div>
              </button>
            );
          })}
        </div>

        <div className="mt-8 border-t border-stone-100 pt-8 flex flex-col items-center">
           <ActivityRing progress={progress} color="#4f46e5" /><p className="text-[11px] font-black text-stone-900 uppercase tracking-widest text-center">Progress</p>
        </div>
      </aside>

      <main className="flex-grow flex flex-col items-center py-10 md:py-24 px-6 md:px-16 overflow-y-auto h-screen relative">
        <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:32px_32px] opacity-40 pointer-events-none" />
        <div className="w-full max-w-4xl relative z-10">
          <AnimatePresence mode="wait">
            <motion.div key={activeSection} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}>
              {activeSection === 0 && (
                <ReadingSection title="The Great Forgetting." eyebrow="Step 1" icon={BarChart3}>
                  <p>In the last module, we saw that passive review (like re-reading) feels good but leads to poor long-term memory. This isn't a small effect; it's a catastrophic failure. The data from Roediger & Karpicke (2006) showed a classic "crossover interaction": while re-reading was slightly better after 5 minutes, it led to a near-total memory collapse after one week compared to active testing.</p>
                  <p>This is the harsh reality of the <Highlight description="The natural, exponential decay of memory over time. Passive review does almost nothing to slow this curve down.">Forgetting Curve</Highlight>. The comfort of re-reading is a trap. The act of testing, however, does something remarkable: it slows the rate of forgetting, fundamentally changing the trajectory of your learning.</p>
                </ReadingSection>
              )}
              {activeSection === 1 && (
                <ReadingSection title="The 'Test Effect'." eyebrow="Step 2" icon={BrainCircuit}>
                  <p>So why is testing so powerful? It's not about assessment; it's a mechanism for building memory. This is the <Highlight description="The finding that the act of retrieving information from memory makes that memory more durable and long-lasting than simply re-studying it.">Testing Effect</Highlight>. The psychologist Robert Bjork gives us the vocabulary to understand why: he splits memory into two types.</p>
                  <p><Highlight description="How deeply a memory is embedded. This is 'true' learning and is relatively permanent. It only increases through effortful retrieval.">Storage Strength</Highlight> is how well you've actually learned something. <Highlight description="How easily a memory comes to mind right now. This is a temporary state, influenced by recent exposure.">Retrieval Strength</Highlight> is how easily you can access it. Re-reading massively boosts retrieval strength (it feels easy and fluent) but does almost nothing for storage strength. Active recall, especially when it's difficult, is the only thing that significantly boosts storage strength.</p>
                  <StrengthMeter />
                </ReadingSection>
              )}
              {activeSection === 2 && (
                <ReadingSection title="The 'Dropout' Fallacy." eyebrow="Step 3" icon={XCircle}>
                  <p>One of the most common and damaging student habits is the "dropout" method: "I know this now, so I'll stop quizzing myself and just look over my notes." This feels efficient, but a devastating 2008 study by Karpicke and Roediger proved it's a fallacy.</p>
                  <p>They found that continuing to test yourself on a topic, even after you've gotten it right once, is the most crucial part of learning. Students who dropped items from testing after one correct answer had a final recall of only ~35% a week later. Students who continued testing themselves on everything retained ~80%—more than double! The heavy lifting of memory consolidation is done entirely by the retrieval process. Stopping the testing stops the learning.</p>
                </ReadingSection>
              )}
               {activeSection === 3 && (
                <ReadingSection title="Beyond Rote Memory." eyebrow="Step 4" icon={Share2}>
                  <p>A common criticism of active recall is that it only teaches you to parrot back facts without real understanding. This is a myth. Research shows that retrieval practice enhances <Highlight description="The ability to apply knowledge learned in one context to new, different contexts. It is a key measure of deep understanding.">Transfer of Knowledge</Highlight>. Why?</p>
                  <p>When you re-read, you're encoding the information exactly as it appears on the page. But when you are forced to retrieve it, you must reconstruct the memory in your own words. This process forces your brain to focus on the underlying principles and abstract them from the specific examples. This makes the knowledge more flexible and easier to apply to new problems you haven't seen before—like the ones that show up on your Leaving Cert paper.</p>
                </ReadingSection>
              )}
              {activeSection === 4 && (
                <ReadingSection title="The Anxiety Myth." eyebrow="Step 5" icon={HeartPulse}>
                  <p>The biggest barrier to using active recall is fear. It feels like a high-stakes judgment, and it exposes your gaps in knowledge, which can be stressful. But a large-scale study by Agarwal et al. (2014) on students using frequent, low-stakes quizzing found the exact opposite was true.</p>
                  <p>An incredible 92% of students said it helped them learn, and 72% said it made them *less* nervous for big exams. It works through two mechanisms: <Highlight description="Repeated, low-stakes exposure to the testing format makes it feel normal and routine, reducing the fear associated with high-stakes exams.">Exposure & Desensitization</Highlight> and <Highlight description="The process of getting an accurate understanding of what you know and don't know. Active recall eliminates the uncertainty that is a major source of anxiety.">Metacognitive Calibration</Highlight>. By testing yourself constantly, you eliminate the surprise. The final exam is no longer a scary unknown; it's just another Tuesday.</p>
                </ReadingSection>
              )}
              {activeSection === 5 && (
                <ReadingSection title="Your Recall Toolkit." eyebrow="Step 6" icon={Wrench}>
                  <p>You now understand the science. Active recall is the single most powerful tool in your academic arsenal. To master it, you need to follow three core rules derived from the research, and audit your own current methods.</p>
                  <p>1. **Embrace Disfluency:** Understand that the feeling of "struggle" is the feeling of learning. If it feels easy, it's probably ineffective. 2. **The "Book Closed" Rule:** Never judge how well you know something with the book open. That's just fluency, not learning. 3. **Stop Dropping Items:** Continue to test yourself on material even after you get it right. Continued retrieval is what arrests the forgetting curve. </p>
                  <StudyMethodAuditor />
                  <MicroCommitment>
                    <p>For your next study session, try the 20/80 rule. Spend 20% of your time consuming information (reading, watching) and 80% of your time actively recalling it (self-quizzing, explaining it out loud).</p>
                  </MicroCommitment>
                </ReadingSection>
              )}
              <footer className="mt-24 flex items-center justify-between pt-12 border-t border-stone-200/60 px-4">
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handlePrev} disabled={activeSection === 0} className={`flex items-center gap-4 bg-stone-100 text-stone-800 px-8 py-4 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all shadow-sm ${activeSection === 0 ? 'opacity-0 pointer-events-none' : ''}`}>
                  <ArrowLeft size={16} /> Prev
                </motion.button>
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handleCompleteSection} className="group relative flex items-center gap-4 bg-stone-900 text-white px-12 py-6 rounded-2xl font-black text-[12px] uppercase tracking-widest hover:bg-indigo-600 transition-all shadow-[0_20px_50px_rgba(0,0,0,0.2)] overflow-hidden">
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
