/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, Users, Share2, Anchor, Link, VenetianMask, Map
} from 'lucide-react';

type ModuleProgress = {
  unlockedSection: number;
};

interface SocialCapitalModuleProps {
  onBack: () => void;
  progress: ModuleProgress;
  onProgressUpdate: (progress: ModuleProgress) => void;
}

const Highlight = ({ children, description, color = "bg-violet-100/40", textColor = "text-violet-900", decorColor = "decoration-violet-400/40", hoverColor="hover:bg-violet-200/60" }: { children?: React.ReactNode, description: string, color?: string, textColor?: string, decorColor?: string, hoverColor?: string }) => {
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
              <p className="font-sans font-bold text-violet-400 mb-2 uppercase tracking-[0.2em] text-[9px]">The Academic Insight</p>
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
        <div className="w-12 h-12 rounded-2xl bg-stone-900 flex items-center justify-center text-violet-400 shadow-xl border border-white/10">
          <Icon size={24} />
        </div>
      </div>
      <span className="inline-flex items-center gap-2 px-3 py-1 bg-violet-50 text-violet-600 text-[10px] font-black tracking-[0.4em] uppercase rounded-full mb-4">
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
  <div className="my-12 p-8 bg-violet-50/50 border-2 border-dashed border-violet-200 rounded-3xl">
    <div className="flex items-start gap-5">
      <div className="w-11 h-11 rounded-xl bg-violet-500 text-white flex items-center justify-center shrink-0 mt-1 shadow-lg shadow-violet-500/20">
        <Flag size={20} />
      </div>
      <div>
        <h4 className="font-bold text-violet-800 text-sm uppercase tracking-widest">Your Mission (Under 5 Mins)</h4>
        <div className="text-stone-600 mt-2 font-medium leading-relaxed">
          {children}
        </div>
      </div>
    </div>
  </div>
);

const ActivityRing = ({ progress, color = "#8b5cf6" }: { progress: number, color?: string }) => {
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
const SocialCapitalSorter = () => {
    const initialItems = [
        {id: 1, text: "My best mate", type: "bonding"},
        {id: 2, text: "My mam", type: "bonding"},
        {id: 3, text: "A cousin in college", type: "bridging"},
        {id: 4, text: "My GAA coach", type: "bridging"},
        {id: 5, text: "The local shopkeeper", type: "bonding"},
    ];
    const [items, setItems] = useState(initialItems);
    const [bonding, setBonding] = useState<typeof initialItems>([]);
    const [bridging, setBridging] = useState<typeof initialItems>([]);

    const handleSort = (item: typeof initialItems[0], target: 'bonding' | 'bridging') => {
        setItems(items.filter(i => i.id !== item.id));
        if (target === 'bonding') setBonding([...bonding, item]);
        else setBridging([...bridging, item]);
    };
    
    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Social Capital Sorter</h4>
             <p className="text-center text-sm text-stone-500 mb-8">Sort these connections into the correct network.</p>
             <div className="grid grid-cols-2 gap-4">
                <div className="p-4 bg-emerald-50 border-2 border-dashed border-emerald-200 rounded-2xl min-h-[150px]">
                    <h5 className="font-bold text-emerald-700 text-center mb-2">Bonding (Safety Net)</h5>
                    {bonding.map(b => <motion.div layoutId={`item-${b.id}`} key={b.id} className="text-xs p-2 bg-white rounded-md text-center font-bold mb-2 shadow-sm">{b.text}</motion.div>)}
                </div>
                <div className="p-4 bg-blue-50 border-2 border-dashed border-blue-200 rounded-2xl min-h-[150px]">
                    <h5 className="font-bold text-blue-700 text-center mb-2">Bridging (Ladder)</h5>
                    {bridging.map(b => <motion.div layoutId={`item-${b.id}`} key={b.id} className="text-xs p-2 bg-white rounded-md text-center font-bold mb-2 shadow-sm">{b.text}</motion.div>)}
                </div>
             </div>
             <div className="mt-6 flex flex-wrap justify-center gap-3">
                {items.map(item => (
                    <motion.div layoutId={`item-${item.id}`} key={item.id} className="p-3 bg-stone-100 rounded-lg shadow-sm">
                        <span className="font-bold text-sm">{item.text}</span>
                        <div className="mt-2 text-xs flex gap-1">
                            <button onClick={() => handleSort(item, 'bonding')} className="bg-emerald-200 text-emerald-800 px-2 py-0.5 rounded">Bonding</button>
                            <button onClick={() => handleSort(item, 'bridging')} className="bg-blue-200 text-blue-800 px-2 py-0.5 rounded">Bridging</button>
                        </div>
                    </motion.div>
                ))}
             </div>
        </div>
    );
};

const NotionsDecoder = () => {
    const phrases = [
        { insult: "Lick-arse", reframe: "Someone building a strategic relationship with a teacher." },
        { insult: "Try-hard", reframe: "Someone who understands that effort is the engine of success." },
        { insult: "Swot", reframe: "Someone investing time in their future." },
        { insult: "Notions", reframe: "Having aspirations beyond what's expected." },
    ];
    const [selected, setSelected] = useState(0);
    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">The "Notions" Decoder</h4>
            <p className="text-center text-sm text-stone-500 mb-8">Translate the language of 'smart shaming' into the language of success.</p>
            <div className="flex flex-wrap justify-center gap-2 mb-6">
                {phrases.map((p, i) => (
                    <button key={p.insult} onClick={() => setSelected(i)} className={`px-4 py-2 text-sm font-bold rounded-lg border-2 ${selected === i ? 'bg-violet-500 text-white border-violet-500' : 'bg-stone-100 border-stone-200'}`}>{p.insult}</button>
                ))}
            </div>
             <div className="p-6 bg-stone-900 rounded-2xl text-center text-white font-mono">
                {phrases[selected].reframe}
             </div>
        </div>
    );
}

const NetworkAudit = () => {
    const [nodes, setNodes] = useState([
        { id: 'You', x: 200, y: 150, type: 'self' },
        { id: 'Friend 1', x: 100, y: 100, type: 'bonding' },
        { id: 'Family', x: 150, y: 200, type: 'bonding' },
        { id: 'Teacher', x: 300, y: 100, type: 'bridging' },
        { id: 'Coach', x: 250, y: 200, type: 'bridging' },
    ]);

    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">My Network Map</h4>
             <p className="text-center text-sm text-stone-500 mb-8">Who is in your network? Who could you add?</p>
             <div className="h-80 w-full bg-stone-50 rounded-lg relative">
                {nodes.map(node => (
                    <motion.div 
                        key={node.id} 
                        drag 
                        dragConstraints={{left:0, right: 350, top:0, bottom:250}}
                        className={`absolute p-2 rounded-full text-xs font-bold text-white ${node.type === 'self' ? 'bg-violet-600' : node.type === 'bonding' ? 'bg-emerald-500' : 'bg-blue-500'}`}
                        style={{left: node.x, top: node.y}}
                    >{node.id}</motion.div>
                ))}
             </div>
        </div>
    );
};


// --- MODULE COMPONENT ---
export const SocialCapitalModule: React.FC<SocialCapitalModuleProps> = ({ onBack, progress, onProgressUpdate }) => {
  const [activeSection, setActiveSection] = useState(progress.unlockedSection);
  const unlockedSection = progress.unlockedSection;
  
  const sections = [
    { id: 'hidden-currency', title: 'The Hidden Currency', eyebrow: '01 // The Network Effect', icon: Users },
    { id: 'bonding-vs-bridging', title: 'Bonding vs. Bridging', eyebrow: '02 // Safety Net vs. Ladder', icon: Share2 },
    { id: 'accessing-tacit-knowledge', title: 'Tacit Knowledge', eyebrow: '03 // The Unwritten Rules', icon: Anchor },
    { id: 'cultural-capital', title: 'The Language of Power', eyebrow: '04 // Cultural Capital', icon: VenetianMask },
    { id: 'engineering-your-network', title: 'Engineering Your Network', eyebrow: '05 // The Action Plan', icon: Map },
  ];
  
  useEffect(() => {
    setActiveSection(progress.unlockedSection);
  }, [progress.unlockedSection]);

  const handleCompleteSection = () => {
    if (activeSection === unlockedSection && unlockedSection < sections.length - 1) {
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

  const progressPercentage = sections.length > 1 ? (unlockedSection / (sections.length - 1)) * 100 : 0;

  return (
    <div className="min-h-screen bg-[#FBFBF9] text-stone-900 font-sans flex flex-col md:flex-row overflow-x-hidden">
      <aside className="w-full md:w-80 bg-white border-r border-stone-200 sticky top-0 md:h-screen z-40 p-8 flex flex-col">
        <div className="flex items-center gap-4 mb-12">
          <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={onBack} className="p-2 rounded-full transition-all border border-stone-200/50 shadow-sm bg-white">
            <ArrowLeft size={16} className="text-stone-700" />
          </motion.button>
          <div>
            <p className="text-[9px] font-black text-violet-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 06</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">The Social Capital Protocol</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <motion.div
                  className="w-full bg-violet-500 shadow-[0_0_10px_rgba(139,92,246,0.5)]"
                  style={{ height: `${progressPercentage}%` }}
              />
          </div>
          {sections.map((section, idx) => {
            const isUnlocked = idx <= unlockedSection;
            const isActive = idx === activeSection;
            const isCompleted = idx < unlockedSection;
            return (
              <button key={section.id} disabled={!isUnlocked} onClick={() => handleJumpToSection(idx)} className={`relative z-10 w-full flex items-center gap-4 p-3 rounded-xl transition-all duration-500 text-left group ${isActive ? 'bg-violet-50 shadow-sm translate-x-2' : ''} ${!isUnlocked ? 'opacity-40 grayscale cursor-not-allowed' : 'hover:bg-stone-50'}`}>
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border-2 transition-all duration-500 ${isCompleted ? 'bg-violet-600 border-violet-600 text-white shadow-lg' : isActive ? 'bg-white border-violet-500 text-violet-600 shadow-xl rotate-12' : 'bg-white border-stone-200 text-stone-300'}`}>
                   {isCompleted ? <CheckCircle2 size={18} /> : isActive ? <section.icon size={18} /> : <Lock size={16} />}
                </div>
                <div className="flex-grow"><p className={`text-[8px] font-black uppercase tracking-widest ${isActive ? 'text-violet-500' : 'text-stone-400'}`}>{section.eyebrow.split('// ')[1]}</p><h4 className={`text-xs font-bold leading-tight ${isActive ? 'text-stone-900' : 'text-stone-500'}`}>{section.title}</h4></div>
              </button>
            );
          })}
        </div>
        <div className="mt-8 border-t border-stone-100 pt-8 flex flex-col items-center">
           <ActivityRing progress={progressPercentage} color="#8b5cf6" /><p className="text-[11px] font-black text-stone-900 uppercase tracking-widest text-center">Progress</p>
        </div>
      </aside>

      <main className="flex-grow flex flex-col items-center py-10 md:py-24 px-6 md:px-16 overflow-y-auto h-screen relative">
        <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:32px_32px] opacity-40 pointer-events-none" />
        <div className="w-full max-w-4xl relative z-10">
          <AnimatePresence mode="wait">
            <motion.div key={activeSection} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}>
              {activeSection === 0 && <ReadingSection title="The Hidden Currency." eyebrow="Step 1" icon={Users} />}
              {activeSection === 1 && <ReadingSection title="Bonding vs. Bridging Capital." eyebrow="Step 2" icon={Share2} />}
              {activeSection === 2 && <ReadingSection title="Accessing Tacit Knowledge." eyebrow="Step 3" icon={Anchor} />}
              {activeSection === 3 && <ReadingSection title="The Language of Power." eyebrow="Step 4" icon={VenetianMask} />}
              {activeSection === 4 && <ReadingSection title="Engineering Your Network." eyebrow="Step 5" icon={Map} />}
              <footer className="mt-24 flex items-center justify-between pt-12 border-t border-stone-200/60 px-4">
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handlePrev} disabled={activeSection === 0} className={`flex items-center gap-4 bg-stone-100 text-stone-800 px-8 py-4 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all shadow-sm ${activeSection === 0 ? 'opacity-0 pointer-events-none' : ''}`}>
                  <ArrowLeft size={16} /> Prev
                </motion.button>
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handleCompleteSection} className="group relative flex items-center gap-4 bg-stone-900 text-white px-12 py-6 rounded-2xl font-black text-[12px] uppercase tracking-widest hover:bg-violet-600 transition-all shadow-[0_20px_50px_rgba(0,0,0,0.2)] overflow-hidden">
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
