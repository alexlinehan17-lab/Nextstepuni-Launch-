
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, Link2, Brain, Wand2, Gamepad2, Briefcase, DraftingCompass, Wind
} from 'lucide-react';

interface LinkingStudyFutureGoalsModuleProps {
  onBack: () => void;
}

const Highlight = ({ children, description, color = "bg-rose-100/40", textColor = "text-rose-900", decorColor = "decoration-rose-400/40", hoverColor="hover:bg-rose-200/60" }: { children?: React.ReactNode, description: string, color?: string, textColor?: string, decorColor?: string, hoverColor?: string }) => {
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
              <p className="font-sans font-bold text-rose-400 mb-2 uppercase tracking-[0.2em] text-[9px]">The Academic Insight</p>
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
        <div className="w-12 h-12 rounded-2xl bg-stone-900 flex items-center justify-center text-rose-400 shadow-xl border border-white/10">
          <Icon size={24} />
        </div>
      </div>
      <span className="inline-flex items-center gap-2 px-3 py-1 bg-rose-50 text-rose-600 text-[10px] font-black tracking-[0.4em] uppercase rounded-full mb-4">
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
  <div className="my-12 p-8 bg-rose-50/50 border-2 border-dashed border-rose-200 rounded-3xl">
    <div className="flex items-start gap-5">
      <div className="w-11 h-11 rounded-xl bg-rose-500 text-white flex items-center justify-center shrink-0 mt-1 shadow-lg shadow-rose-500/20">
        <Flag size={20} />
      </div>
      <div>
        <h4 className="font-bold text-rose-800 text-sm uppercase tracking-widest">Your Mission (Under 5 Mins)</h4>
        <div className="text-stone-600 mt-2 font-medium leading-relaxed">
          {children}
        </div>
      </div>
    </div>
  </div>
);

const ActivityRing = ({ progress, color = "#e11d48" }: { progress: number, color?: string }) => {
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

const MotivationCalculator = () => {
    const [vars, setVars] = useState({ E: 50, V: 50, C: 50 });
    const motivation = (vars.E * vars.V) / (vars.C + 1);

    const Slider = ({ label, value, setter }: { label: string, value: number, setter: (val: number) => void}) => (
        <div>
            <label className="text-xs font-bold">{label} ({value})</label>
            <input type="range" min="1" max="100" value={value} onChange={e => setter(parseInt(e.target.value))} className="w-full accent-rose-500" />
        </div>
    );

    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Motivation Calculator</h4>
            <div className="grid grid-cols-2 gap-6 items-center">
                <div className="space-y-4">
                    <Slider label="Expectancy (Belief I can do it)" value={vars.E} setter={v => setVars({...vars, E:v})}/>
                    <Slider label="Value (How useful/enjoyable is it?)" value={vars.V} setter={v => setVars({...vars, V:v})}/>
                    <Slider label="Cost (Stress, boredom, time)" value={vars.C} setter={v => setVars({...vars, C:v})}/>
                </div>
                <div className="text-center">
                     <p className="text-sm text-stone-500">Your Motivation Score:</p>
                     <p className="text-6xl font-black text-rose-500 tracking-tighter">{Math.round(motivation)}</p>
                </div>
            </div>
        </div>
    )
};

const WOOPPlanner = () => {
    const [data, setData] = useState({wish: '', outcome: '', obstacle: '', plan: ''});
    const update = (field: string, value: string) => setData(prev => ({...prev, [field]: value}));

    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">My WOOP Blueprint</h4>
            <div className="space-y-4 mt-6">
                <input value={data.wish} onChange={e => update('wish', e.target.value)} placeholder="WISH: What do you want to achieve?" className="w-full p-3 bg-stone-50 rounded-lg"/>
                <input value={data.outcome} onChange={e => update('outcome', e.target.value)} placeholder="OUTCOME: What's the best feeling if you do?" className="w-full p-3 bg-stone-50 rounded-lg"/>
                <input value={data.obstacle} onChange={e => update('obstacle', e.target.value)} placeholder="OBSTACLE: What *inside you* holds you back?" className="w-full p-3 bg-stone-50 rounded-lg"/>
                <input value={data.plan} onChange={e => update('plan', e.target.value)} placeholder="PLAN: If [obstacle], then I will..." className="w-full p-3 bg-stone-50 rounded-lg"/>
            </div>
        </div>
    );
};

const TransferableSkillsMatrix = () => {
    const [activeRow, setActiveRow] = useState<string | null>(null);
    const skills = [
        { activity: "History RSR", skill: "Information Synthesis", application: "Legal Research, Journalism" },
        { activity: "English Comparative", skill: "Pattern Recognition", application: "UX Design, HR Management" },
        { activity: "Maths Probability", skill: "Risk Assessment", application: "Insurance, Business Strategy" },
        { activity: "Geography Field Study", skill: "Systems Thinking", application: "Urban Planning, Logistics" },
        { activity: "LCVP/Business", skill: "Project Management", application: "Event Management, Operations" },
    ];
    
    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Transferable Skills Matrix</h4>
            <div className="mt-6 flow-root">
                <div className="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
                    <div className="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
                        <table className="min-w-full divide-y divide-stone-200">
                            <thead>
                                <tr>
                                    <th className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-stone-900">LC Activity</th>
                                    <th className="px-3 py-3.5 text-left text-sm font-semibold text-stone-900">Corporate/Life Skill</th>
                                    <th className="px-3 py-3.5 text-left text-sm font-semibold text-stone-900">Career Application</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-stone-100">
                                {skills.map(item => (
                                    <tr key={item.activity} onMouseEnter={() => setActiveRow(item.activity)} onMouseLeave={() => setActiveRow(null)} className="hover:bg-rose-50 cursor-pointer">
                                        <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium">{item.activity}</td>
                                        <td className="whitespace-nowrap px-3 py-4 text-sm font-medium">{item.skill}</td>
                                        <td className="whitespace-nowrap px-3 py-4 text-sm font-medium">{item.application}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    );
};


// --- MODULE COMPONENT ---
export const LinkingStudyFutureGoalsModule: React.FC<{onBack: () => void}> = ({ onBack }) => {
  const [activeSection, setActiveSection] = useState(0);
  const [unlockedSection, setUnlockedSection] = useState(0);
  
  const sections = [
    { id: 'friction-point', title: 'The "Why Bother?" Problem', eyebrow: '01 // The Anatomy of Friction', icon: Wind },
    { id: 'horizon-of-purpose', title: 'The Horizon of Purpose', eyebrow: '02 // Future Time Perspective', icon: DraftingCompass },
    { id: 'writing-cure', title: 'The "Writing Cure"', eyebrow: '03 // Utility Value Interventions', icon: Wand2 },
    { id: 'woop-protocol', title: 'From Dream to Plan', eyebrow: '04 // The WOOP Protocol', icon: Gamepad2 },
    { id: 'becoming-the-author', title: 'Becoming the Author', eyebrow: '05 // Narrative & Autonomy', icon: Brain },
    { id: 'career-training', title: 'Curriculum as Career Training', eyebrow: '06 // Reframing the Work', icon: Briefcase },
    { id: 'purpose-protocol', title: 'The Purpose Protocol', eyebrow: '07 // The Action Plan', icon: Link2 },
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
            <p className="text-[9px] font-black text-rose-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 11</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">Linking Study to Goals</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <motion.div
                  className="w-full bg-rose-500 shadow-[0_0_10px_rgba(225,29,72,0.5)]"
                  initial={{ height: 0 }}
                  animate={{ height: sections.length > 1 ? `${(unlockedSection / (sections.length - 1)) * 100}%` : '0%' }}
              />
          </div>
          {sections.map((section, idx) => {
            const isUnlocked = idx <= unlockedSection;
            const isActive = idx === activeSection;
            const isCompleted = idx < unlockedSection;
            return (
              <button key={section.id} disabled={!isUnlocked} onClick={() => handleJumpToSection(idx)} className={`relative z-10 w-full flex items-center gap-4 p-3 rounded-xl transition-all duration-500 text-left group ${isActive ? 'bg-rose-50 shadow-sm translate-x-2' : ''} ${!isUnlocked ? 'opacity-40 grayscale cursor-not-allowed' : 'hover:bg-stone-50'}`}>
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border-2 transition-all duration-500 ${isCompleted ? 'bg-rose-600 border-rose-600 text-white shadow-lg' : isActive ? 'bg-white border-rose-500 text-rose-600 shadow-xl rotate-12' : 'bg-white border-stone-200 text-stone-300'}`}>
                   {isCompleted ? <CheckCircle2 size={18} /> : isActive ? <section.icon size={18} /> : <Lock size={16} />}
                </div>
                <div className="flex-grow"><p className={`text-[8px] font-black uppercase tracking-widest ${isActive ? 'text-rose-500' : 'text-stone-400'}`}>{section.eyebrow.split('// ')[1]}</p><h4 className={`text-xs font-bold leading-tight ${isActive ? 'text-stone-900' : 'text-stone-500'}`}>{section.title}</h4></div>
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
                <ReadingSection title="The 'Why Bother?' Problem." eyebrow="Step 1" icon={Wind}>
                  <p>The feeling of "why bother?" isn't laziness. It's a rational calculation your brain makes when the cost of a task outweighs its value. The science for this is called <Highlight description="A theory of motivation that posits that your level of motivation is a product of your expectation of success (Expectancy) and the value you place on the task (Value).">Expectancy-Value Theory (EVT)</Highlight>. Motivation collapses when the <Highlight description="The perceived negative aspects of a task, like stress, boredom, or the time it takes away from other activities.">Cost</Highlight> feels higher than the <Highlight description="The usefulness of a task for achieving your future goals. It's the most stable and powerful form of motivation for schoolwork.">Utility Value</Highlight>.</p>
                  <p>In the Leaving Cert, the "points race" often disconnects the work you're doing from any real-world purpose, reducing its Utility Value to zero. This makes the work feel like "drudgery," which massively increases its psychological Cost. This module is about flipping that equation back in your favour.</p>
                  <MotivationCalculator />
                </ReadingSection>
              )}
              {activeSection === 1 && (
                <ReadingSection title="The Horizon of Purpose." eyebrow="Step 2" icon={DraftingCompass}>
                  <p>The single biggest factor in overcoming the "why bother?" friction is your <Highlight description="A cognitive construct that describes the extent to which you anticipate and integrate the future into your present actions. A long, deep FTP is a powerful buffer against burnout.">Future Time Perspective (FTP)</Highlight>. It's the mental timeline you use to frame your current actions. A short FTP (just getting to June) makes every task feel like a painful cost. A long FTP (seeing how this connects to your career in 5 years) reframes the same task as a valuable investment.</p>
                  <p>Crucially, your FTP needs to be <Highlight description="The motivational power of FTP is strongest when it's specific. A general desire for a 'good life' is weak compared to knowing exactly how the Krebs cycle is relevant to becoming a doctor.">domain-specific</Highlight>. It's not enough to want a good job; you need to see the direct, concrete link between the paragraph you're writing today and the person you want to become tomorrow.</p>
                </ReadingSection>
              )}
               {activeSection === 2 && (
                <ReadingSection title="The 'Writing Cure'." eyebrow="Step 3" icon={Wand2}>
                  <p>How do you forge that link? One of the most robust interventions in psychology is the <Highlight description="A simple, evidence-based exercise where students write briefly about how their schoolwork is relevant to their own lives. It is proven to boost interest and grades, especially for struggling students.">Utility Value Intervention</Highlight>. The act of articulating the connection yourself forces your brain to "internalize" the value. You move from "the teacher says this is important" to "I see how this helps me."</p>
                  <MicroCommitment>
                    <p>Pick one subject you're studying this week. Now, think of one specific way it could be useful to (a) you in the future, (b) a family member, or (c) solving a problem you care about. You've just run your first Utility Value Intervention.</p>
                  </MicroCommitment>
                </ReadingSection>
              )}
               {activeSection === 3 && (
                <ReadingSection title="From Dream to Plan." eyebrow="Step 4" icon={Gamepad2}>
                  <p>Just having a goal isn't enough. Research shows that pure positive fantasizing can actually lower your energy. To turn a dream into a plan, you need a tool called <Highlight description="A powerful, four-step goal-setting strategy developed by Gabriele Oettingen, based on the science of Mental Contrasting with Implementation Intentions.">WOOP</Highlight>: Wish, Outcome, Obstacle, Plan.</p>
                  <p>The magic is in the **Obstacle** step. By vividly imagining the internal barrier that stops you (e.g., "I get distracted by my phone"), you can create an "If-Then" plan to deal with it automatically. This transforms the obstacle from a motivation-killer into a trigger for a pre-planned, positive response.</p>
                  <WOOPPlanner />
                </ReadingSection>
              )}
               {activeSection === 4 && (
                <ReadingSection title="Becoming the Author." eyebrow="Step 5" icon={Brain}>
                    <p>Feeling a lack of purpose often comes from a lack of control. <Highlight description="A psychological theory that states we have three core needs: Autonomy (control), Competence (capability), and Relatedness (connection).">Self-Determination Theory (SDT)</Highlight> shows that we are most motivated when we feel we have <Highlight description="The feeling of being in control of your own actions and life. It's about acting from a sense of choice, not coercion.">Autonomy</Highlight>. The Leaving Cert can feel like it strips this away.</p>
                    <p>You can reclaim your autonomy through <Highlight description="A technique where you slightly modify how you approach your schoolwork to better align it with your personal strengths and interests.">Course Crafting</Highlight>. This isn't about changing the assignment, but about changing your *approach* to it. If you have to write a History essay but you love art, write about the history of art. This act of choice transforms the motivation from "controlled" (have to) to "autonomous" (want to).</p>
                </ReadingSection>
              )}
               {activeSection === 5 && (
                <ReadingSection title="Curriculum as Career Training." eyebrow="Step 6" icon={Briefcase}>
                  <p>The biggest lie of the "points race" is that subjects are just abstract hurdles. The truth is that every subject on the curriculum is a training ground for high-demand, 21st-century skills. To beat the "why bother?" friction, you must reframe the curriculum as direct career training.</p>
                  <p>Maths isn't just Maths; it's the science of risk assessment and decision-making. English isn't just reading books; it's a laboratory for social intelligence and empathy. The History RSR isn't just an essay; it's training in information synthesis and due diligence—the core skills of a lawyer or a journalist. By making this matrix visible, the "drudgery" of schoolwork is reframed as building a portfolio of real-world skills.</p>
                  <TransferableSkillsMatrix />
                </ReadingSection>
              )}
              {activeSection === 6 && (
                <ReadingSection title="The Purpose Protocol." eyebrow="Step 7" icon={Link2}>
                  <p>You now have the scientific toolkit to re-wire the connection between your present effort and your future self. This is the **Purpose Protocol**, a 5-phase plan for building sustainable motivation.</p>
                  <p><strong>Phase 1: The Audit.</strong> For each subject, ask "Why am I doing this?" If the only answer is "points," that's a friction point. Apply the Utility Value Writing exercise. <strong>Phase 2: The Vision.</strong> Spend 15 minutes writing a detailed description of your "Best Possible Self" 5 years from now. Then, use WOOP to plan your next study session. <strong>Phase 3: The Craft.</strong> Find one assignment this week and "course craft" it to make it your own. <strong>Phase 4: The Habit.</strong> Use "Tiny Habits" to make starting the work so small it's impossible to fail. <strong>Phase 5: Re-Authoring.</strong> If you feel stuck, externalize the problem ("The stress is visiting me") and map your skills from other areas (like gaming) to your schoolwork.</p>
                  <MicroCommitment>
                    <p>Pick one phase, one protocol. Just one. Commit to trying it for one week. You're not just studying; you're becoming the architect of your own purpose.</p>
                  </MicroCommitment>
                </ReadingSection>
              )}
              <footer className="mt-24 flex items-center justify-between pt-12 border-t border-stone-200/60 px-4">
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handlePrev} disabled={activeSection === 0} className={`flex items-center gap-4 bg-stone-100 text-stone-800 px-8 py-4 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all shadow-sm ${activeSection === 0 ? 'opacity-0 pointer-events-none' : ''}`}>
                  <ArrowLeft size={16} /> Prev
                </motion.button>
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handleCompleteSection} className="group relative flex items-center gap-4 bg-stone-900 text-white px-12 py-6 rounded-2xl font-black text-[12px] uppercase tracking-widest hover:bg-rose-600 transition-all shadow-[0_20px_50px_rgba(0,0,0,0.2)] overflow-hidden">
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
