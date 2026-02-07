
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, Eye, Workflow, Box, Film, AlertTriangle, Pyramid
} from 'lucide-react';

interface MentalModellingModuleProps {
  onBack: () => void;
}

const Highlight = ({ children, description, color = "bg-cyan-100/40", textColor = "text-cyan-900", decorColor = "decoration-cyan-400/40", hoverColor="hover:bg-cyan-200/60" }: { children?: React.ReactNode, description: string, color?: string, textColor?: string, decorColor?: string, hoverColor?: string }) => {
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
              <p className="font-sans font-bold text-cyan-400 mb-2 uppercase tracking-[0.2em] text-[9px]">The Academic Insight</p>
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
        <div className="w-12 h-12 rounded-2xl bg-stone-900 flex items-center justify-center text-cyan-400 shadow-xl border border-white/10">
          <Icon size={24} />
        </div>
      </div>
      <span className="inline-flex items-center gap-2 px-3 py-1 bg-cyan-50 text-cyan-600 text-[10px] font-black tracking-[0.4em] uppercase rounded-full mb-4">
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
  <div className="my-12 p-8 bg-cyan-50/50 border-2 border-dashed border-cyan-200 rounded-3xl">
    <div className="flex items-start gap-5">
      <div className="w-11 h-11 rounded-xl bg-cyan-500 text-white flex items-center justify-center shrink-0 mt-1 shadow-lg shadow-cyan-500/20">
        <Flag size={20} />
      </div>
      <div>
        <h4 className="font-bold text-cyan-800 text-sm uppercase tracking-widest">Your Mission (Under 5 Mins)</h4>
        <div className="text-stone-600 mt-2 font-medium leading-relaxed">
          {children}
        </div>
      </div>
    </div>
  </div>
);

const ActivityRing = ({ progress, color = "#06b6d4" }: { progress: number, color?: string }) => {
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

const GlassBoxUnfolder = () => {
    const [isUnfolded, setIsUnfolded] = useState(false);
    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl flex flex-col items-center">
             <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">The "Glass Box" Model</h4>
             <p className="text-center text-sm text-stone-500 mb-8">This is the fundamental mental model for orthographic projection.</p>
             <div className="w-48 h-48 [perspective:1000px] mb-8">
                <motion.div className="relative w-full h-full" style={{ transformStyle: 'preserve-3d', transform: 'rotateX(-20deg) rotateY(-30deg)' }} animate={{scale: isUnfolded ? 0.8 : 1}}>
                    {/* Front */}
                    <motion.div className="absolute w-48 h-48 border-2 border-cyan-500 bg-cyan-500/10 flex items-center justify-center" style={{transformOrigin: 'bottom'}} animate={{rotateX: isUnfolded ? -90 : 0, y: isUnfolded ? 96 : 0 }}><span className="font-bold">ELEVATION</span></motion.div>
                    {/* Top */}
                    <motion.div className="absolute w-48 h-48 border-2 border-cyan-500 bg-cyan-500/10 flex items-center justify-center" style={{transformOrigin: 'top'}} animate={{transform: `rotateX(90deg) translateZ(96px)`, rotateX: isUnfolded ? -90 : 90, y: isUnfolded ? -96 : 0}}><span className="font-bold">PLAN</span></motion.div>
                     {/* Side */}
                    <motion.div className="absolute w-48 h-48 border-2 border-cyan-500 bg-cyan-500/10 flex items-center justify-center" style={{transformOrigin: 'left'}} animate={{transform: `rotateY(-90deg) translateZ(96px)`, rotateY: isUnfolded ? 90 : -90, x: isUnfolded ? -96 : 0}}><span className="font-bold">END VIEW</span></motion.div>
                </motion.div>
             </div>
             <button onClick={() => setIsUnfolded(!isUnfolded)} className="px-4 py-2 bg-cyan-500 text-white font-bold rounded-lg">{isUnfolded ? 'Fold Box' : 'Unfold Box'}</button>
        </div>
    );
};

const CycleOfModelling = () => {
    const steps = ["Decomposition", "Internalization", "Simulation", "Externalization", "Re-Internalization"];
    const [activeStep, setActiveStep] = useState(0);
    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">The Cycle of Modelling</h4>
             <p className="text-center text-sm text-stone-500 mb-8">This is the active hypothesis-testing process your brain runs.</p>
             <div className="flex justify-between mb-2">
                {steps.map((step, i) => <div key={step} className={`w-1/5 text-center text-xs font-bold ${i <= activeStep ? 'text-cyan-600' : 'text-stone-300'}`}>{step}</div>)}
             </div>
             <div className="w-full h-2 bg-stone-100 rounded-full"><motion.div className="h-full bg-cyan-500 rounded-full" animate={{width: `${(activeStep / (steps.length - 1)) * 100}%`}} /></div>
             <div className="flex justify-center gap-2 mt-4">
                <button onClick={() => setActiveStep(s => Math.max(0, s-1))} className="px-3 py-1 text-xs bg-stone-200 rounded-md">Prev</button>
                <button onClick={() => setActiveStep(s => Math.min(steps.length-1, s+1))} className="px-3 py-1 text-xs bg-stone-200 rounded-md">Next</button>
             </div>
        </div>
    );
};

// --- MODULE COMPONENT ---
export const MentalModellingModule: React.FC<MentalModellingModuleProps> = ({ onBack }) => {
  const [activeSection, setActiveSection] = useState(0);
  const [unlockedSection, setUnlockedSection] = useState(0);
  
  const sections = [
    { id: 'minds-eye', title: 'The Mind\'s Eye', eyebrow: '01 // The Hidden Curriculum', icon: Eye },
    { id: 'modelling-cycle', title: 'The Modelling Cycle', eyebrow: '02 // The Process', icon: Workflow },
    { id: 'glass-box', title: 'The "Glass Box" (DCG)', eyebrow: '03 // Geometric Models', icon: Box },
    { id: 'mental-movie', title: 'The "Mental Movie" (Eng)', eyebrow: '04 // Kinematic Models', icon: Film },
    { id: 'procedural-trap', title: 'The Procedural Trap', eyebrow: '05 // The Failure Mode', icon: AlertTriangle },
    { id: 'training-plan', title: 'The Training Plan', eyebrow: '06 // The Action Plan', icon: Pyramid },
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
            <p className="text-[9px] font-black text-cyan-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 08</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">Mental Modelling</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <motion.div
                  className="w-full bg-cyan-500 shadow-[0_0_10px_rgba(6,182,212,0.5)]"
                  initial={{ height: 0 }}
                  animate={{ height: sections.length > 1 ? `${(unlockedSection / (sections.length - 1)) * 100}%` : '0%' }}
              />
          </div>
          {sections.map((section, idx) => {
            const isUnlocked = idx <= unlockedSection;
            const isActive = idx === activeSection;
            const isCompleted = idx < unlockedSection;
            return (
              <button key={section.id} disabled={!isUnlocked} onClick={() => handleJumpToSection(idx)} className={`relative z-10 w-full flex items-center gap-4 p-3 rounded-xl transition-all duration-500 text-left group ${isActive ? 'bg-cyan-50 shadow-sm translate-x-2' : ''} ${!isUnlocked ? 'opacity-40 grayscale cursor-not-allowed' : 'hover:bg-stone-50'}`}>
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border-2 transition-all duration-500 ${isCompleted ? 'bg-cyan-600 border-cyan-600 text-white shadow-lg' : isActive ? 'bg-white border-cyan-500 text-cyan-600 shadow-xl rotate-12' : 'bg-white border-stone-200 text-stone-300'}`}>
                   {isCompleted ? <CheckCircle2 size={18} /> : isActive ? <section.icon size={18} /> : <Lock size={16} />}
                </div>
                <div className="flex-grow"><p className={`text-[8px] font-black uppercase tracking-widest ${isActive ? 'text-cyan-500' : 'text-stone-400'}`}>{section.eyebrow.split('// ')[1]}</p><h4 className={`text-xs font-bold leading-tight ${isActive ? 'text-stone-900' : 'text-stone-500'}`}>{section.title}</h4></div>
              </button>
            );
          })}
        </div>

        <div className="mt-8 border-t border-stone-100 pt-8 flex flex-col items-center">
           <ActivityRing progress={progress} color="#06b6d4" /><p className="text-[11px] font-black text-stone-900 uppercase tracking-widest text-center">Progress</p>
        </div>
      </aside>

      <main className="flex-grow flex flex-col items-center py-10 md:py-24 px-6 md:px-16 overflow-y-auto h-screen relative">
        <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:32px_32px] opacity-40 pointer-events-none" />
        <div className="w-full max-w-4xl relative z-10">
          <AnimatePresence mode="wait">
            <motion.div key={activeSection} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}>
              {activeSection === 0 && (
                <ReadingSection title="The Mind's Eye." eyebrow="Step 1" icon={Eye}>
                  <p>In subjects like DCG and Engineering, there's a "hidden curriculum." It's not about what you draw; it's about what you *see* in your head before you draw it. This is <Highlight description="A dynamic, internal simulation of an external system. It's the cognitive workspace where you rotate objects, simulate mechanisms, and visualize unseen structures.">Mental Modelling</Highlight>. It's the difference between blindly following steps and truly understanding the geometry.</p>
                  <p>"Spatial ability" isn't one thing. It's a cluster of skills. The big three for the Leaving Cert are: 1) <Highlight description="The 'heavy lifting' skill of imagining a multi-step transformation, like slicing an object or finding where two shapes intersect.">Spatial Visualisation (Vz)</Highlight>, 2) <Highlight description="The ability to rapidly and accurately rotate a rigid object in your mind. This is key for drawing different views of an object.">Mental Rotation</Highlight>, and 3) <Highlight description="Understanding how objects are arranged from a first-person perspective, critical for things like Perspective Drawing.">Spatial Orientation</Highlight>.</p>
                </ReadingSection>
              )}
               {activeSection === 1 && (
                <ReadingSection title="The Modelling Cycle." eyebrow="Step 2" icon={Workflow}>
                  <p>How does your brain build a mental model? It runs a 5-step cycle. 1) **Decomposition**: You break the 2D drawing on the exam paper into basic shapes (prisms, cones). 2) **Internalization**: You build a 3D model in your head based on these shapes. 3) **Simulation**: You mentally manipulate this model ("If I look from the side, what will it look like?"). 4) **Externalization**: You draw the line. 5) **Re-internalization**: You check if your drawing matches your mental simulation.</p>
                  <p>Here's the key: novice students almost always skip Step 3. They rely on "procedural recipes" ("always draw this line at 45 degrees") instead of running the mental simulation. This works for standard questions, but collapses the moment a novel problem appears.</p>
                  <CycleOfModelling />
                </ReadingSection>
              )}
              {activeSection === 2 && (
                <ReadingSection title="The 'Glass Box' (DCG)." eyebrow="Step 3" icon={Box}>
                  <p>For DCG, the fundamental mental model is the "Glass Box"—imagining an object suspended in a clear cube, with the Elevation, Plan, and End Views projected onto its faces. The challenge is that you have to mentally construct this 3D reality while working on a 2D page. This becomes incredibly difficult with abstract ideas like the <Highlight description="The line where an imaginary plane (like a cutting plane) intersects one of the reference planes (the floor or wall). It's an abstraction of an abstraction.">Traces of a Plane</Highlight>.</p>
                  <p>To solve complex Interpenetration questions, expert modellers use a mental shortcut called the <Highlight description="A mental strategy where you imagine taking thin 2D slices through a complex 3D problem. By solving a series of simpler 2D problems, you can reconstruct the 3D solution.">"Slicing" Heuristic</Highlight>. This reduces the cognitive load by breaking one massive 3D problem into many small, manageable 2D problems.</p>
                  <GlassBoxUnfolder/>
                </ReadingSection>
              )}
               {activeSection === 3 && (
                <ReadingSection title="The 'Mental Movie' (Eng)." eyebrow="Step 4" icon={Film}>
                    <p>In Engineering, mental models are less about static form and more about dynamic function. For Mechanisms, you need to create a <Highlight description="The kinematic mental model required for Engineering, where you mentally animate a static 2D diagram to understand its movement and function.">"Mental Movie."</Highlight> You see a static drawing of a windscreen wiper and you must be able to press 'play' in your mind to see how it moves.</p>
                    <p>For Materials Science, the models are even more abstract. You have to visualize things you can never see, like the difference between a <Highlight description="A way atoms are arranged in a metal. The ability of atoms to slide along 'slip planes' in an FCC lattice is what makes metals like copper ductile.">Face-Centred Cubic (FCC)</Highlight> and Body-Centred Cubic (BCC) crystal lattice. Without this micro-structural model, definitions of properties like ductility are just meaningless words to be memorized.</p>
                </ReadingSection>
              )}
               {activeSection === 4 && (
                <ReadingSection title="The Procedural Trap." eyebrow="Step 5" icon={AlertTriangle}>
                  <p>The single biggest reason students fail in DCG and Engineering is the <Highlight description="The common teaching and learning failure where students memorize a sequence of steps ('how' to draw something) without understanding the underlying geometric principle ('why' it works).">"Procedural Trap."</Highlight> They learn to treat geometry as a set of rules for drawing lines on paper, rather than a representation of objects in 3D space.</p>
                  <p>This creates a brittle, inflexible knowledge base. A student can perfectly reproduce a standard drawing from the textbook, but when the examiner presents a slightly non-standard problem, they have no mental model to fall back on. Their procedural "recipe" doesn't work, and they are left completely lost. The examiner reports are filled with comments about "conceptual errors"—this is what they mean.</p>
                   <MicroCommitment>
                    <p>Look back at your last DCG or Engineering drawing. Can you explain *why* you drew each line, in terms of the 3D object? Or did you just follow a memorized sequence of steps?</p>
                  </MicroCommitment>
                </ReadingSection>
              )}
               {activeSection === 5 && (
                <ReadingSection title="The Training Plan." eyebrow="Step 6" icon={Pyramid}>
                  <p>Mental modelling is a teachable skill, not a gift. Like any skill, it must be trained with "progressive overload," moving from simple to complex. The <Highlight description="A curriculum design that revisits spatial skills with increasing levels of abstraction, moving from physical objects to abstract verbal problems.">Spiral of Visualisation</Highlight> is a framework for this training.</p>
                  <p>**Phase 1: Concrete Manipulation.** Start with physical objects (LEGO, cardboard models). Hold them, rotate them, and sketch them. This is "Touch-See-Draw." **Phase 2: Guided Visualisation.** Use CAD. Before you create a feature, sketch what you *predict* it will look like. Then, compare your sketch to the result. This is "Predict-Verify-Reflect." **Phase 3: Abstract Visualisation.** Solve "Dark Room" problems, where the geometry is described only in words. This is the ultimate test of your mind's eye, and the final preparation for the exam.</p>
                </ReadingSection>
              )}
              <footer className="mt-24 flex items-center justify-between pt-12 border-t border-stone-200/60 px-4">
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handlePrev} disabled={activeSection === 0} className={`flex items-center gap-4 bg-stone-100 text-stone-800 px-8 py-4 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all shadow-sm ${activeSection === 0 ? 'opacity-0 pointer-events-none' : ''}`}>
                  <ArrowLeft size={16} /> Prev
                </motion.button>
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handleCompleteSection} className="group relative flex items-center gap-4 bg-stone-900 text-white px-12 py-6 rounded-2xl font-black text-[12px] uppercase tracking-widest hover:bg-cyan-600 transition-all shadow-[0_20px_50px_rgba(0,0,0,0.2)] overflow-hidden">
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
