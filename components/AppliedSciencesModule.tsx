/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, Key, Cpu, Droplet, Code, HardHat, ToyBrick, Wrench
} from 'lucide-react';

interface AppliedSciencesModuleProps {
  onBack: () => void;
}

const Highlight = ({ children, description, color = "bg-teal-100/40", textColor = "text-teal-900", decorColor = "decoration-teal-400/40", hoverColor="hover:bg-teal-200/60" }: { children?: React.ReactNode, description: string, color?: string, textColor?: string, decorColor?: string, hoverColor?: string }) => {
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
              <p className="font-sans font-bold text-teal-400 mb-2 uppercase tracking-[0.2em] text-[9px]">The Academic Insight</p>
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
        <div className="w-12 h-12 rounded-2xl bg-stone-900 flex items-center justify-center text-teal-400 shadow-xl border border-white/10">
          <Icon size={24} />
        </div>
      </div>
      <span className="inline-flex items-center gap-2 px-3 py-1 bg-teal-50 text-teal-600 text-[10px] font-black tracking-[0.4em] uppercase rounded-full mb-4">
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
  <div className="my-12 p-8 bg-teal-50/50 border-2 border-dashed border-teal-200 rounded-3xl">
    <div className="flex items-start gap-5">
      <div className="w-11 h-11 rounded-xl bg-teal-500 text-white flex items-center justify-center shrink-0 mt-1 shadow-lg shadow-teal-500/20">
        <Flag size={20} />
      </div>
      <div>
        <h4 className="font-bold text-teal-800 text-sm uppercase tracking-widest">Your Mission (Under 5 Mins)</h4>
        <div className="text-stone-600 mt-2 font-medium leading-relaxed">
          {children}
        </div>
      </div>
    </div>
  </div>
);

const ActivityRing = ({ progress, color = "#14b8a6" }: { progress: number, color?: string }) => {
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
const DopingSimulator = () => {
    const [doping, setDoping] = useState<'n'|'p'|null>(null);
    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Semiconductor Doping</h4>
            <div className="flex justify-center gap-4 my-4">
                <button onClick={()=>setDoping('n')} className="px-4 py-2 bg-blue-100 text-blue-800 rounded-lg">N-Type Doping</button>
                <button onClick={()=>setDoping('p')} className="px-4 py-2 bg-rose-100 text-rose-800 rounded-lg">P-Type Doping</button>
            </div>
            {doping && <p className="text-center text-sm">{doping === 'n' ? 'Introducing Phosphorus (Group V) creates a free electron.' : 'Introducing Boron (Group III) creates a "hole".'}</p>}
        </div>
    );
}

// --- MODULE COMPONENT ---
export const AppliedSciencesModule: React.FC<{onBack: () => void}> = ({ onBack }) => {
  const [activeSection, setActiveSection] = useState(0);
  const [unlockedSection, setUnlockedSection] = useState(0);
  
  const sections = [
    { id: 'convergence', title: 'The Convergence', eyebrow: '01 // The Core Idea', icon: Key },
    { id: 'engineering', title: 'Engineering', eyebrow: '02 // Semiconductor Focus', icon: Cpu },
    { id: 'dcg', title: 'DCG', eyebrow: '03 // Soap Dispensers & CAD', icon: Droplet },
    { id: 'cs', title: 'Computer Science', eyebrow: '04 // Forests & Climate', icon: Code },
    { id: 'construction-tech', title: 'Construction & Tech', eyebrow: '05 // The Artefact', icon: HardHat },
    { id: 'synergies', title: 'Cross-Curricular Synergies', eyebrow: '06 // The Action Plan', icon: Wrench },
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
            <p className="text-[9px] font-black text-teal-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 06</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">Mastering Applied Sciences</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <motion.div
                  className="w-full bg-teal-500 shadow-[0_0_10px_rgba(20,184,166,0.5)]"
                  initial={{ height: 0 }}
                  animate={{ height: sections.length > 1 ? `${(unlockedSection / (sections.length - 1)) * 100}%` : '0%' }}
              />
          </div>
          {sections.map((section, idx) => {
            const isUnlocked = idx <= unlockedSection;
            const isActive = idx === activeSection;
            const isCompleted = idx < unlockedSection;
            return (
              <button key={section.id} disabled={!isUnlocked} onClick={() => handleJumpToSection(idx)} className={`relative z-10 w-full flex items-center gap-4 p-3 rounded-xl transition-all duration-500 text-left group ${isActive ? 'bg-teal-50 shadow-sm translate-x-2' : ''} ${!isUnlocked ? 'opacity-40 grayscale cursor-not-allowed' : 'hover:bg-stone-50'}`}>
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border-2 transition-all duration-500 ${isCompleted ? 'bg-teal-600 border-teal-600 text-white shadow-lg' : isActive ? 'bg-white border-teal-500 text-teal-600 shadow-xl rotate-12' : 'bg-white border-stone-200 text-stone-300'}`}>
                   {isCompleted ? <CheckCircle2 size={18} /> : isActive ? <section.icon size={18} /> : <Lock size={16} />}
                </div>
                <div className="flex-grow"><p className={`text-[8px] font-black uppercase tracking-widest ${isActive ? 'text-teal-500' : 'text-stone-400'}`}>{section.eyebrow.split('// ')[1]}</p><h4 className={`text-xs font-bold leading-tight ${isActive ? 'text-stone-900' : 'text-stone-500'}`}>{section.title}</h4></div>
              </button>
            );
          })}
        </div>
        <div className="mt-8 border-t border-stone-100 pt-8 flex flex-col items-center">
           <ActivityRing progress={progress} /><p className="text-[11px] font-black text-stone-900 uppercase tracking-widest text-center">Progress</p>
        </div>
      </aside>

      <main className="flex-grow flex flex-col items-center py-10 md:py-24 px-6 md:px-16 overflow-y-auto h-screen relative">
        <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:32px_32px] opacity-40 pointer-events-none" />
        <div className="w-full max-w-4xl relative z-10">
          <AnimatePresence mode="wait">
            <motion.div key={activeSection} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}>
              {activeSection === 0 && (
                <ReadingSection title="The Convergence." eyebrow="Step 1" icon={Key}>
                  <p>The "practical" subjects are no longer just about workshop skills. They represent the cutting edge of STEM education, demanding a synthesis of theoretical knowledge, digital fluency, and design innovation. The key to a H1 is demonstrating this <Highlight description="The ability to synthesize theoretical knowledge, manual/digital dexterity, and design innovation into a coherent whole.">technological capability</Highlight>.</p>
                  <p>Across all these subjects, the single biggest cause of lost marks is a disconnect between the <Highlight description="The physical project or artefact you create.">"made artefact"</Highlight> and the <Highlight description="The design folio or report that documents the process.">"written account."</Highlight> A brilliant project with a poor folio that looks "retro-fitted" will not achieve a high grade. The narrative of your design process is as important as the final product.</p>
                </ReadingSection>
              )}
              {activeSection === 1 && (
                <ReadingSection title="Engineering: 2026." eyebrow="Step 2" icon={Cpu}>
                  <p>For 2026, the prescribed Special Topic is **Semiconductor Technology**. This is a high-stakes question that demands deep theoretical knowledge. You must be able to explain the atomic-level mechanics of <Highlight description="The process of adding impurities to a pure semiconductor to change its electrical properties.">doping</Highlight> to create N-type (free electrons) and P-type ("holes") materials, and how this forms a <Highlight description="The fundamental building block of most semiconductor devices, like diodes and transistors.">PN Junction</Highlight>.</p>
                  <p>For the project (25%) and practical (25%), precision is everything. The folio must demonstrate a genuine design process, not be "retro-fitted" to the finished artefact. CAD skills (SolidWorks) are now essential. For the practical exam, the first 45 minutes on **Marking Out** are the most critical; an error here makes the entire piece impossible to assemble correctly.</p>
                  <DopingSimulator/>
                </ReadingSection>
              )}
              {activeSection === 2 && (
                <ReadingSection title="DCG: 2026." eyebrow="Step 3" icon={Droplet}>
                    <p>The Student Assignment is 40% of your grade. For 2026, the Higher Level theme is **Refillable Soap Dispensers**, and Ordinary Level is **Fidget Toys**. For HL, this means a focus on ergonomics and complex CAD surfacing. You'll need to master SolidWorks features like <Highlight description="A CAD tool for creating complex, organic shapes by connecting a series of profiles.">Loft</Highlight> and <Highlight description="A CAD feature that restricts the movement of components in an assembly, allowing for realistic simulation of mechanisms.">Limit Mates</Highlight> to model the pump mechanism.</p>
                    <p>A H1 folio requires more than just good CAD. It needs rich <Highlight description="Explaining how the form of an object relates to its function (e.g., 'the truncated cone shape lowers the centre of gravity, making it more stable').">Geometric Analysis</Highlight> and photorealistic renders using PhotoView 360 that show an understanding of materials and lighting.</p>
                </ReadingSection>
              )}
              {activeSection === 3 && (
                <ReadingSection title="Computer Science: 2026." eyebrow="Step 4" icon={Code}>
                  <p>The 2026 coursework (30%) is themed **"Forests, Climate Change, and Biodiversity."** This requires an ambitious integration of hardware and software. You must build an embedded system using a <Highlight description="The standard microcontroller for the course, featuring integrated sensors and radio capability.">BBC micro:bit</Highlight> with external sensors (e.g., soil moisture, temperature) that sends data to a Python program.</p>
                  <p>The Python program must then run a <Highlight description="A 'what-if' model of a forest-related system, like a forest fire simulation, where the probability of ignition is influenced by the real-time data from your micro:bit.">Modelling and Simulation</Highlight>. The crucial element is the feedback loop: the physical data must influence the virtual model, and the model should ideally send a signal back to the hardware. Your final report is a website (HTML/CSS), and a video demo is mandatory.</p>
                </ReadingSection>
              )}
              {activeSection === 4 && (
                <ReadingSection title="Construction & Tech." eyebrow="Step 5" icon={HardHat}>
                  <p>In **Construction Studies**, the 2026 exam remains rooted in the existing syllabus but with a heavy emphasis on sustainability. Question 1 (Scale Drawing) is compulsory and requires mastery of detailing rules like <Highlight description="Insulation must be continuous, especially at junctions, to prevent heat loss.">Thermal Continuity</Highlight> and the unbroken <Highlight description="A line on a drawing showing the air barrier, which must be continuous. Taping at joints is essential.">Airtightness Line</Highlight>. For the project (25%) and practical (25%), the focus is on precision joinery and finish.</p>
                  <p>In **Technology**, the project is a massive 50% of your grade. A H1 project requires an iterative design loop documented in a folio and the use of <Highlight description="Computer-Aided Design and Computer-Aided Manufacturing, such as using a laser cutter or 3D printer to create parts designed in CAD.">CAD/CAM</Highlight>. The artefact must integrate electronics (PIC/PICAXE microcontrollers) and mechanisms, with a focus on gear ratios and mechanical advantage.</p>
                </ReadingSection>
              )}
               {activeSection === 5 && (
                <ReadingSection title="Cross-Curricular Synergies." eyebrow="Step 6" icon={Wrench}>
                  <p>These subjects share a common DNA. Mastering a concept in one area gives you a massive advantage in another. The **"Control Systems"** thread is the most powerful. The semiconductor physics in Engineering underpins the electronics in Technology and the embedded systems in Computer Science. The <Highlight description="A fundamental electronic circuit used to read a sensor's changing resistance. It is a 'master key' that unlocks sensor integration in all three subjects.">Potential Divider</Highlight> circuit is a universal tool.</p>
                  <p>To maximize your learning, you must use <Highlight description="The cognitive science technique of mixing related topics from different subjects in one study session. This strengthens retention and builds flexible knowledge.">Interleaved Practice</Highlight>. When you study logic gates for CS, immediately review digital electronics in Engineering. When you learn about NZEB in Construction, review climate monitoring in CS. This builds the web of interconnected knowledge that the new curriculum demands.</p>
                  <MicroCommitment>
                    <p>Pick one cross-curricular link mentioned here. Spend 10 minutes creating a quick mind map showing how the concepts connect across the different subjects. You're starting to think like an integrated engineer.</p>
                  </MicroCommitment>
                </ReadingSection>
              )}
              <footer className="mt-24 flex items-center justify-between pt-12 border-t border-stone-200/60 px-4">
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handlePrev} disabled={activeSection === 0} className={`flex items-center gap-4 bg-stone-100 text-stone-800 px-8 py-4 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all shadow-sm ${activeSection === 0 ? 'opacity-0 pointer-events-none' : ''}`}>
                  <ArrowLeft size={16} /> Prev
                </motion.button>
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handleCompleteSection} className="group relative flex items-center gap-4 bg-stone-900 text-white px-12 py-6 rounded-2xl font-black text-[12px] uppercase tracking-widest hover:bg-teal-600 transition-all shadow-[0_20px_50px_rgba(0,0,0,0.2)] overflow-hidden">
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
