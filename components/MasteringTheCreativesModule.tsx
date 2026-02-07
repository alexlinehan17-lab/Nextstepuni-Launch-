

/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, Key, PenTool, SlidersHorizontal, Film, Shield, Wrench
} from 'lucide-react';

interface MasteringTheCreativesModuleProps {
  onBack: () => void;
}

const Highlight = ({ children, description, color = "bg-slate-100/40", textColor = "text-slate-900", decorColor = "decoration-slate-400/40", hoverColor="hover:bg-slate-200/60" }: { children?: React.ReactNode, description: string, color?: string, textColor?: string, decorColor?: string, hoverColor?: string }) => {
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
              <p className="font-sans font-bold text-slate-400 mb-2 uppercase tracking-[0.2em] text-[9px]">The Academic Insight</p>
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
        <div className="w-12 h-12 rounded-2xl bg-stone-900 flex items-center justify-center text-slate-400 shadow-xl border border-white/10">
          <Icon size={24} />
        </div>
      </div>
      <span className="inline-flex items-center gap-2 px-3 py-1 bg-slate-50 text-slate-600 text-[10px] font-black tracking-[0.4em] uppercase rounded-full mb-4">
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
  <div className="my-12 p-8 bg-slate-50/50 border-2 border-dashed border-slate-200 rounded-3xl">
    <div className="flex items-start gap-5">
      <div className="w-11 h-11 rounded-xl bg-slate-500 text-white flex items-center justify-center shrink-0 mt-1 shadow-lg shadow-slate-500/20">
        <Flag size={20} />
      </div>
      <div>
        <h4 className="font-bold text-slate-800 text-sm uppercase tracking-widest">Your Mission (Under 5 Mins)</h4>
        <div className="text-stone-600 mt-2 font-medium leading-relaxed">
          {children}
        </div>
      </div>
    </div>
  </div>
);

const ActivityRing = ({ progress, color = "#64748b" }: { progress: number, color?: string }) => {
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


export const MasteringTheCreativesModule: React.FC<{onBack: () => void}> = ({ onBack }) => {
  const [activeSection, setActiveSection] = useState(0);
  const [unlockedSection, setUnlockedSection] = useState(0);
  
  const sections = [
    { id: 'shift-from-talent', title: 'The Talent Myth', eyebrow: '01 // The Paradigm Shift', icon: Key },
    { id: 'art-protocol', title: 'Art: The Visual Journal', eyebrow: '02 // The Art Protocol', icon: PenTool },
    { id: 'music-protocol', title: 'Music: The Algorithm of Melody', eyebrow: '03 // The Music Protocol', icon: SlidersHorizontal },
    { id: 'film-protocol', title: 'Film: The Grammar of Vision', eyebrow: '04 // The Film Protocol', icon: Film },
    { id: 'pressure-protocol', title: 'Mastering Exam Pressure', eyebrow: '05 // The Pressure Protocol', icon: Shield },
    { id: 'action-plan', title: 'Your Creative Blueprint', eyebrow: '06 // The Action Plan', icon: Wrench },
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
            <p className="text-[9px] font-black text-slate-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 07</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">Mastering the Creatives</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <motion.div
                  className="w-full bg-slate-500 shadow-[0_0_10px_rgba(71,85,105,0.5)]"
                  initial={{ height: 0 }}
                  animate={{ height: sections.length > 1 ? `${(unlockedSection / (sections.length - 1)) * 100}%` : '0%' }}
              />
          </div>
          {sections.map((section, idx) => {
            const isUnlocked = idx <= unlockedSection;
            const isActive = idx === activeSection;
            const isCompleted = idx < unlockedSection;
            return (
              <button key={section.id} disabled={!isUnlocked} onClick={() => handleJumpToSection(idx)} className={`relative z-10 w-full flex items-center gap-4 p-3 rounded-xl transition-all duration-500 text-left group ${isActive ? 'bg-slate-50 shadow-sm translate-x-2' : ''} ${!isUnlocked ? 'opacity-40 grayscale cursor-not-allowed' : 'hover:bg-stone-50'}`}>
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border-2 transition-all duration-500 ${isCompleted ? 'bg-slate-600 border-slate-600 text-white shadow-lg' : isActive ? 'bg-white border-slate-500 text-slate-600 shadow-xl rotate-12' : 'bg-white border-stone-200 text-stone-300'}`}>
                   {isCompleted ? <CheckCircle2 size={18} /> : isActive ? <section.icon size={18} /> : <Lock size={16} />}
                </div>
                <div className="flex-grow"><p className={`text-[8px] font-black uppercase tracking-widest ${isActive ? 'text-slate-500' : 'text-stone-400'}`}>{section.eyebrow.split('// ')[1]}</p><h4 className={`text-xs font-bold leading-tight ${isActive ? 'text-stone-900' : 'text-stone-500'}`}>{section.title}</h4></div>
              </button>
            );
          })}
        </div>
        <div className="mt-8 border-t border-stone-100 pt-8 flex flex-col items-center">
           <ActivityRing progress={progress} color="#64748b" /><p className="text-[11px] font-black text-stone-900 uppercase tracking-widest text-center">Progress</p>
        </div>
      </aside>

      <main className="flex-grow flex flex-col items-center py-10 md:py-24 px-6 md:px-16 overflow-y-auto h-screen relative">
        <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:32px_32px] opacity-40 pointer-events-none" />
        <div className="w-full max-w-4xl relative z-10">
          <AnimatePresence mode="wait">
            <motion.div key={activeSection} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}>
              {activeSection === 0 && (
                <ReadingSection title="The Talent Myth." eyebrow="Step 1" icon={Key}>
                  <p>For years, you've probably heard the same old story: you're either "good at art" or you're not. You're born with "talent," or you're not. That's a myth. The Leaving Cert creative subjects—Art, Music, and Film—are not a lottery of natural ability. They're a game of skill.</p>
                  <p>A deep dive into the marking schemes and examiner reports reveals the truth: top grades aren't awarded for some magical spark of genius. They're awarded for mastering a process. High performance is the result of <Highlight description="Focused, strategic practice that pushes you just beyond your current comfort zone. It's about working on your weaknesses, not just repeating what you're good at.">deliberate practice</Highlight>, understanding the technical rules of the game, and mastering <Highlight description="Working in cycles of creating, getting feedback, and refining. It's about treating your work as a draft that can always be improved, not a one-shot masterpiece.">iterative processes</Highlight>. This module is your playbook for learning these skills.</p>
                </ReadingSection>
              )}
               {activeSection === 1 && (
                <ReadingSection title="Art: The Visual Journal." eyebrow="Step 2" icon={PenTool}>
                  <p>The new Art course has one core message: your process is as important as your final product. The <Highlight description="Formerly the sketchbook, this is now the 50% coursework component. It's the documented 'thinking process' behind your final piece.">Visual Journal</Highlight> is not a gallery of finished drawings; it's a messy laboratory of thought. A high-scoring journal shows your journey from an initial idea to a final piece.</p>
                  <p>Kickstart your project with mind maps that go beyond words, using textures and sensory details. Master observational drawing not by "copying," but by tricking your brain with techniques like drawing upside down (<Highlight description="An observational drawing exercise where you draw from an upside-down reference photo, forcing your brain to see shapes and lines instead of recognizable objects.">Inversion</Highlight>) or drawing the space *around* an object (<Highlight description="An exercise where you focus on drawing the empty shapes between and around objects, which dramatically improves your sense of proportion.">Negative Space</Highlight>).</p>
                   <MicroCommitment><p>Take any object on your desk. For just two minutes, try to draw it without looking at the paper, keeping your eyes locked on the object. This is 'Blind Contour' drawing. It feels weird, but it's a powerful way to train your eyes to truly see.</p></MicroCommitment>
                </ReadingSection>
              )}
              {activeSection === 2 && (
                <ReadingSection title="Music: The Algorithm of Melody." eyebrow="Step 3" icon={SlidersHorizontal}>
                  <p>The 16-bar melody question is not a test of your inner Mozart; it's a structural engineering problem. You can get full marks by treating it like a puzzle with clear rules. Before you write a single note, run your "pre-flight check": What's the Key Signature? The Time Signature? What's the instrument's range?</p>
                  <p>The most reliable structure is the A-A1-B-A2 formula. **A** is given. **A1** is a response that starts the same but ends differently, usually with a <Highlight description="The process of changing from one key to another. A mandatory part of the melody composition question.">modulation</Highlight> to a new key. **B** is the contrast—go higher, change the rhythm. **A2** is the return home, resolving firmly back in the original key. It's an algorithm, not a whim.</p>
                </ReadingSection>
              )}
               {activeSection === 3 && (
                <ReadingSection title="Film: The Grammar of Vision." eyebrow="Step 4" icon={Film}>
                  <p>Film is not just a recorded story; it's a language constructed through technical choices. A H1 student doesn't just describe the plot; they analyze the *form*. How did the director use a <Highlight description="A camera shot where the camera looks up at the subject, making them seem powerful or threatening.">Low Angle Shot</Highlight> to make the villain seem powerful? How did they use <Highlight description="High-contrast lighting with deep shadows, often used in horror and noir to create mystery and danger.">Low-Key Lighting (Chiaroscuro)</Highlight> to create a sense of mystery?</p>
                  <p>For the Comparative Study, you must analyze these technical choices as part of the General Vision & Viewpoint or Cultural Context. In *Blade Runner*, the constant rain and "Venetian blind" shadows aren't just for atmosphere; they're direct quotes from 1940s <Highlight description="A cinematic style known for its dark themes, cynical characters, and high-contrast, black-and-white visuals.">Film Noir</Highlight>, creating a feeling of paranoia and fractured identity.</p>
                </ReadingSection>
              )}
               {activeSection === 4 && (
                <ReadingSection title="Mastering Exam Pressure." eyebrow="Step 5" icon={Shield}>
                  <p>Performance anxiety is the primary enemy in all creative subjects, from the Music practical to the Art deadline. It's a physiological response to perceived social judgment. Your brain releases adrenaline, causing trembling and shallow breathing. The key is to manage the biology, not just the thoughts.</p>
                  <p>Use <Highlight description="A breathing technique (Inhale 4s, Hold 4s, Exhale 4s, Hold 4s) that activates the body's 'rest and digest' system to counteract the adrenaline rush.">Box Breathing</Highlight> to calm your nervous system. Reframe the exam from a test of "correctness" to a "communication of emotion." And most importantly, use <Highlight description="Practicing under exam-like conditions (e.g., performing for a mock examiner) to desensitize your brain to the context triggers of the real event.">Simulation Training</Highlight>. The more you expose your brain to the pressure in a safe environment, the less it will panic on the day.</p>
                </ReadingSection>
              )}
               {activeSection === 5 && (
                <ReadingSection title="Your Creative Blueprint." eyebrow="Step 6" icon={Wrench}>
                  <p>You now have the master key. "Talent" is a myth. Success in creative subjects is a skill built through deliberate practice and strategic thinking. By mastering the process of the Visual Journal, the algorithm of melody, the grammar of film, and the psychology of performance, you can engineer your own success.</p>
                  <MicroCommitment>
                    <p>Pick ONE technique from this module. Just one. Whether it's a 'Blind Contour' drawing, analyzing one movie scene for lighting, or trying Box Breathing for one minute. Commit to trying it this week. You've just taken your first step to becoming a creative master.</p>
                  </MicroCommitment>
                </ReadingSection>
              )}
              <footer className="mt-24 flex items-center justify-between pt-12 border-t border-stone-200/60 px-4">
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handlePrev} disabled={activeSection === 0} className={`flex items-center gap-4 bg-stone-100 text-stone-800 px-8 py-4 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all shadow-sm ${activeSection === 0 ? 'opacity-0 pointer-events-none' : ''}`}>
                  <ArrowLeft size={16} /> Prev
                </motion.button>
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handleCompleteSection} className="group relative flex items-center gap-4 bg-stone-900 text-white px-12 py-6 rounded-2xl font-black text-[12px] uppercase tracking-widest hover:bg-slate-600 transition-all shadow-[0_20px_50px_rgba(0,0,0,0.2)] overflow-hidden">
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
