
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, Feather, BookOpen, Scale, Award, FileText
} from 'lucide-react';

interface StrategicAdvantageModuleProps {
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
const NarrativeSwitcher = () => {
    const [script, setScript] = useState<'idle' | 'contamination' | 'redemption'>('idle');

    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">The Narrative Switcher</h4>
            <p className="text-center text-sm text-stone-500 mb-8">Pivotal Moment: You fail an important mock exam. Which story do you tell?</p>
            <div className="flex justify-center gap-4">
                <button onClick={() => setScript('contamination')} className={`px-4 py-2 text-xs font-bold rounded-lg transition-all ${script === 'contamination' ? 'bg-rose-500 text-white shadow-md' : 'bg-rose-100 text-rose-800'}`}>Contamination Script</button>
                <button onClick={() => setScript('redemption')} className={`px-4 py-2 text-xs font-bold rounded-lg transition-all ${script === 'redemption' ? 'bg-emerald-500 text-white shadow-md' : 'bg-emerald-100 text-emerald-800'}`}>Redemption Script</button>
            </div>
            <div className="mt-8 h-24 flex items-center justify-center">
                <svg viewBox="0 0 300 100" className="w-full h-auto overflow-visible">
                    {/* Static elements */}
                    <circle cx="50" cy="50" r="10" fill="#6366f1" />
                    <path d="M 60 50 L 125 50" stroke="#d1d5db" strokeWidth="2" strokeDasharray="4"/>
                    
                    {/* Animated Path Drawing */}
                    <AnimatePresence>
                        {script === 'redemption' && (
                            <motion.path
                                key="redemption-path"
                                d="M 125 50 Q 175 25 250 25"
                                stroke="#10b981"
                                strokeWidth="3"
                                fill="none"
                                initial={{ pathLength: 0 }}
                                animate={{ pathLength: 1 }}
                                exit={{ pathLength: 0 }}
                                transition={{ duration: 1, ease: "easeInOut" }}
                            />
                        )}
                        {script === 'contamination' && (
                            <motion.path
                                key="contamination-path"
                                d="M 125 50 Q 175 75 250 75"
                                stroke="#f43f5e"
                                strokeWidth="3"
                                fill="none"
                                initial={{ pathLength: 0 }}
                                animate={{ pathLength: 1 }}
                                exit={{ pathLength: 0 }}
                                transition={{ duration: 1, ease: "easeInOut" }}
                            />
                        )}
                    </AnimatePresence>
                </svg>
            </div>
        </div>
    );
};


const AgencyCommunionBalancer = () => {
    const [balance, setBalance] = useState(0); // -1 for Agency, 1 for Communion, 0 for balanced
    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">The Agency & Communion Balancer</h4>
             <p className="text-center text-sm text-stone-500 mb-12">Click the narrative statement that builds the most robust identity.</p>
             <div className="h-40 flex justify-center items-center">
                <motion.div animate={{rotate: balance * 15}} className="w-56 h-20 relative">
                    <div className="w-full h-2 bg-stone-300 absolute bottom-0 left-0" />
                    <div className="w-2 h-4 bg-stone-300 absolute bottom-0 left-1/2 -translate-x-1/2" />
                    <div className="w-12 h-12 bg-blue-100 rounded-md absolute -left-6 -bottom-1" />
                    <div className="w-12 h-12 bg-emerald-100 rounded-md absolute -right-6 -bottom-1" />
                </motion.div>
             </div>
             <div className="grid grid-cols-3 gap-2 mt-6">
                <button 
                    onClick={() => setBalance(-1)} 
                    className={`p-2 text-xs border-2 rounded-lg transition-all ${balance === -1 ? 'border-blue-500 bg-blue-50' : 'border-stone-200'}`}
                >
                    "I did it all myself." (Pure Agency)
                </button>
                <button 
                    onClick={() => setBalance(0)} 
                    className={`p-2 text-xs border-2 rounded-lg transition-all ${balance === 0 ? 'border-indigo-500 bg-indigo-50' : 'border-stone-200'}`}
                >
                    "I worked hard to honor my family's sacrifices." (Balanced)
                </button>
                <button 
                    onClick={() => setBalance(1)} 
                    className={`p-2 text-xs border-2 rounded-lg transition-all ${balance === 1 ? 'border-emerald-500 bg-emerald-50' : 'border-stone-200'}`}
                >
                    "I only survived because of others." (Pure Communion)
                </button>
             </div>
        </div>
    )
};

const DesirableDifficultyChart = () => (
    <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
         <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Chart: The Illusion of Fluency</h4>
         <p className="text-center text-sm text-stone-500 mb-8">"Easy" learning feels good, but "hard" learning builds lasting knowledge.</p>
         <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="text-left">
                <h5 className="font-bold mb-4 text-center">Easy Learning (Re-reading)</h5>
                <div className="space-y-4">
                    <div>
                        <span className="text-xs font-bold text-stone-500">Feeling of Learning:</span>
                        <div className="w-full bg-stone-100 rounded-full h-5 mt-1 overflow-hidden">
                            <motion.div initial={{width: 0}} animate={{width: '90%'}} className="h-full bg-fuchsia-400 rounded-full" />
                        </div>
                    </div>
                    <div>
                        <span className="text-xs font-bold text-stone-500">Long-term Retention:</span>
                        <div className="w-full bg-stone-100 rounded-full h-5 mt-1 overflow-hidden">
                            <motion.div initial={{width: 0}} animate={{width: '20%'}} className="h-full bg-indigo-400 rounded-full" />
                        </div>
                    </div>
                </div>
            </div>
             <div className="text-left">
                <h5 className="font-bold mb-4 text-center">Hard Learning (Practice Qs)</h5>
                <div className="space-y-4">
                     <div>
                        <span className="text-xs font-bold text-stone-500">Feeling of Learning:</span>
                        <div className="w-full bg-stone-100 rounded-full h-5 mt-1 overflow-hidden">
                            <motion.div initial={{width: 0}} animate={{width: '30%'}} className="h-full bg-fuchsia-400 rounded-full" />
                        </div>
                    </div>
                    <div>
                        <span className="text-xs font-bold text-stone-500">Long-term Retention:</span>
                        <div className="w-full bg-stone-100 rounded-full h-5 mt-1 overflow-hidden">
                            <motion.div initial={{width: 0}} animate={{width: '85%'}} className="h-full bg-indigo-400 rounded-full" />
                        </div>
                    </div>
                </div>
            </div>
         </div>
    </div>
);

// --- MODULE COMPONENT ---
export const StrategicAdvantageModule: React.FC<StrategicAdvantageModuleProps> = ({ onBack }) => {
  const [activeSection, setActiveSection] = useState(0);
  const [unlockedSection, setUnlockedSection] = useState(0);
  
  const sections = [
    { id: 'narrative-identity', title: 'The Story of You', eyebrow: '01 // Your Internal Script', icon: Feather },
    { id: 'agency-communion', title: 'The Two Pillars', eyebrow: '02 // Agency & Communion', icon: Scale },
    { id: 'pivotal-moments', title: 'The Power of Failure', eyebrow: '03 // Pivotal Moments', icon: BookOpen },
    { id: 'desirable-difficulties', title: 'The Advantage of Disadvantage', eyebrow: '04 // Desirable Difficulties', icon: Award },
    { id: 'redemption-script', title: 'Your Redemption Script', eyebrow: '05 // The Blueprint', icon: FileText },
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
            <p className="text-[9px] font-black text-indigo-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 08</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">Your Strategic Advantage</h1>
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
                <ReadingSection title="The Story of You." eyebrow="Step 1" icon={Feather}>
                  <p>You are a storyteller. The most important story you will ever tell is the one you tell yourself about your own life. This is your <Highlight description="Pioneered by psychologist Dan McAdams, this is the internalized, evolving story of the self that each person crafts to provide their life with a sense of meaning and purpose.">Narrative Identity</Highlight>. It's how you make sense of your past, present, and future.</p>
                  <p>Society often hands students from tough backgrounds a ready-made story: a tale of deficit and struggle. This is a <Highlight description="A life story in which a positive event is ruined or spoiled by a subsequent negative event, leading to feelings of hopelessness and despair.">Contamination Script</Highlight>. Resilience is the act of radical authorship: rejecting that story and writing your own, a <Highlight description="A life story in which a negative event is 'redeemed' or transformed by a positive outcome, leading to growth, learning, and a sense of agency.">Redemption Script</Highlight> where adversity becomes the source of your strength.</p>
                  <NarrativeSwitcher />
                </ReadingSection>
              )}
               {activeSection === 1 && (
                <ReadingSection title="The Two Pillars." eyebrow="Step 2" icon={Scale}>
                    <p>Every great story is built on two core themes. The first is <Highlight description="A narrative theme focused on the protagonist's autonomy, power, and ability to control their own destiny. It's about self-mastery and achievement.">Agency</Highlight>—the story of the self-reliant hero who overcomes obstacles through their own power. The second is <Highlight description="A narrative theme focused on connection, intimacy, and belonging. It's about love, friendship, and being part of a community.">Communion</Highlight>—the story of connection, of being supported by family, friends, and community.</p>
                    <p>A story of pure Agency leads to the "Isolated Hero" who burns out. A story of pure Communion leads to passivity. The most resilient narrative identities skillfully weave both: "I worked hard (Agency) to honor the sacrifices of my family (Communion)." Finding this balance is key to a sustainable story of success.</p>
                    <AgencyCommunionBalancer />
                </ReadingSection>
              )}
              {activeSection === 2 && (
                <ReadingSection title="The Power of Failure." eyebrow="Step 3" icon={BookOpen}>
                  <p>Your life story is not a continuous film; it’s a collection of key scenes. These are your <Highlight description="Significant life experiences—high points, low points, and turning points—that are heavily interpreted and serve as anchors for your narrative identity.">Pivotal Moments</Highlight>. For resilient individuals, the most important pivotal moments are often failures. They are the moments where suffering is transformed into insight.</p>
                  <p>The key is to learn the art of <Highlight description="The cognitive skill of changing the context or interpretation of an event to alter its meaning. It is the primary mechanism by which we assert agency over circumstance.">Reframing</Highlight>. A technique like the "Failure Resume" helps you de-shame failure and see it not as a verdict on your worth, but as valuable data for future success. It's about learning to say, "I didn't suffer for nothing; I suffered to become stronger."</p>
                  <MicroCommitment>
                    <p>Think of one failure from the last year. Now, name one thing you learned from it that you couldn't have learned otherwise. You've just taken the first step in writing a redemption script.</p>
                  </MicroCommitment>
                </ReadingSection>
              )}
               {activeSection === 3 && (
                <ReadingSection title="The Advantage of Disadvantage." eyebrow="Step 4" icon={Award}>
                  <p>What if the things that make your academic journey harder are the very things that are making your learning deeper and more durable? This is the principle of <Highlight description="Coined by Robert Bjork, these are learning conditions that are effortful and slow down immediate performance but lead to much better long-term retention and transfer of knowledge.">Desirable Difficulties</Highlight>. Learning that is "easy" (like re-reading notes) is shallow. Learning that is "hard" (like struggling to solve a problem without help) forces deeper processing and builds stronger neural pathways.</p>
                  <p>Students from disadvantaged backgrounds often face *involuntary* desirable difficulties. Lack of tutors forces self-explanation (generative learning). Time scarcity forces spaced practice instead of cramming. Resource scarcity builds resourcefulness (self-directed learning). These are not liabilities; they are hidden training programs that build a cognitive toolkit that privileged peers may lack.</p>
                  <DesirableDifficultyChart />
                </ReadingSection>
              )}
              {activeSection === 4 && (
                <ReadingSection title="Your Redemption Script." eyebrow="Step 5" icon={FileText}>
                  <p>You have the power to be the author of your own story. This module has given you the tools of narrative construction: the ability to turn contamination into redemption, to balance agency with communion, and to reframe difficulty as a desirable advantage. Now it's time to put it into practice.</p>
                  <p>The final step is to build your own mini-"Failure Resume." By taking a past failure and actively converting it into an asset, you are practicing the core skill of resilient identity construction. You are forging your own redemption script, turning the lead of your past into the gold of your future.</p>
                  <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
                    <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">My Redemption Story</h4>
                     <div className="mt-6 space-y-4">
                        <div>
                            <label className="block text-xs font-black text-stone-600 uppercase ml-4 mb-2">The Failure (Pivotal Moment):</label>
                            <select className="w-full p-4 bg-stone-50 border-2 border-stone-100 rounded-xl focus:outline-none focus:border-indigo-500"><option>Failed a mock exam</option><option>Missed an assignment deadline</option><option>Didn't understand a topic in class</option></select>
                        </div>
                         <div>
                            <label className="block text-xs font-black text-stone-600 uppercase ml-4 mb-2">The Lesson (Your Asset):</label>
                            <textarea placeholder="What is the single most valuable lesson, skill, or piece of wisdom you gained from this experience?" className="w-full h-24 p-4 bg-stone-50 border-2 border-stone-100 rounded-xl focus:outline-none focus:border-indigo-500"></textarea>
                        </div>
                    </div>
                  </div>
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
