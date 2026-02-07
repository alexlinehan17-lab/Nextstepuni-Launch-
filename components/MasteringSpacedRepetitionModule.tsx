
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, Clock, BarChart2, CalendarDays, RadioTower, Wrench, Brain, RefreshCcw, TrendingDown
} from 'lucide-react';

interface MasteringSpacedRepetitionModuleProps {
  onBack: () => void;
}

const Highlight = ({ children, description, color = "bg-sky-100/40", textColor = "text-sky-900", decorColor = "decoration-sky-400/40", hoverColor="hover:bg-sky-200/60" }: { children?: React.ReactNode, description: string, color?: string, textColor?: string, decorColor?: string, hoverColor?: string }) => {
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
              <p className="font-sans font-bold text-sky-400 mb-2 uppercase tracking-[0.2em] text-[9px]">The Academic Insight</p>
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
        <div className="w-12 h-12 rounded-2xl bg-stone-900 flex items-center justify-center text-sky-400 shadow-xl border border-white/10">
          <Icon size={24} />
        </div>
      </div>
      <span className="inline-flex items-center gap-2 px-3 py-1 bg-sky-50 text-sky-600 text-[10px] font-black tracking-[0.4em] uppercase rounded-full mb-4">
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
  <div className="my-12 p-8 bg-sky-50/50 border-2 border-dashed border-sky-200 rounded-3xl">
    <div className="flex items-start gap-5">
      <div className="w-11 h-11 rounded-xl bg-sky-500 text-white flex items-center justify-center shrink-0 mt-1 shadow-lg shadow-sky-500/20">
        <Flag size={20} />
      </div>
      <div>
        <h4 className="font-bold text-sky-800 text-sm uppercase tracking-widest">Your Mission (Under 5 Mins)</h4>
        <div className="text-stone-600 mt-2 font-medium leading-relaxed">
          {children}
        </div>
      </div>
    </div>
  </div>
);

const ActivityRing = ({ progress, color = "#0ea5e9" }: { progress: number, color?: string }) => {
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
const ForgettingCurveVisualizer = () => {
    const [reviews, setReviews] = useState([false, false, false]);

    const reviewPoints = [ { day: 1, x: 125 }, { day: 3, x: 250 }, { day: 7, x: 375 }];
    const viewboxWidth = 500;
    const viewboxHeight = 150;

    const generatePathData = (activeReviews: boolean[]) => {
        let path = `M 0 5`;
        let lastY = 5;
        const decayFactors = [0.6, 0.4, 0.2, 0.1];

        const activeReviewXs = reviewPoints.map(p => p.x).filter((_, i) => activeReviews[i]);
        const allPoints = [0, ...activeReviewXs, viewboxWidth];

        for (let i = 0; i < allPoints.length - 1; i++) {
            const startX = allPoints[i];
            const currentY = (i > 0) ? 5 : 5;

            if (i > 0) path += ` L ${startX} 5`;

            const endX = allPoints[i];
            const duration = allPoints[i + 1] - startX;
            const endY = currentY + (viewboxHeight - 10) * decayFactors[i];
            
            path += ` C ${startX + duration * 0.3} ${currentY}, ${endX + duration * 0.7} ${endY}, ${allPoints[i+1]} ${endY}`;
            lastY = endY;
        }
        return { path, lastY };
    };
    
    const { path: activePath, lastY: activeLastY } = generatePathData(reviews);
    const baselinePath = `M 0 5 C ${viewboxWidth*0.3} 5, ${viewboxWidth*0.7} ${viewboxHeight - 20}, ${viewboxWidth} ${viewboxHeight - 20}`;
    const activeAreaPath = activePath + ` L ${viewboxWidth} ${viewboxHeight} L 0 ${viewboxHeight} Z`;
    const baselineAreaPath = baselinePath + ` L ${viewboxWidth} ${viewboxHeight} L 0 ${viewboxHeight} Z`;

    const retention = { baseline: 21, r0: 21, r1: 55, r2: 78, r3: 95 };
    const currentReviewCount = reviews.filter(Boolean).length;
    const currentRetention = retention[`r${currentReviewCount}` as keyof typeof retention];

    const handleReviewClick = (index: number) => {
        const newReviews = [...reviews];
        newReviews[index] = !newReviews[index];
        // Ensure sequential activation for a clearer story
        if (newReviews[index]) {
            for (let i = 0; i <= index; i++) newReviews[i] = true;
        } else {
             for (let i = index; i < newReviews.length; i++) newReviews[i] = false;
        }
        setReviews(newReviews);
    };

    return (
        <div className="my-10 p-6 md:p-8 bg-stone-900 rounded-[3rem] border border-white/10 shadow-2xl text-white shadow-[inset_0_2px_4px_0_rgba(255,255,255,0.05)]">
            <h4 className="font-serif text-2xl font-bold text-center italic">The Forgetting Curve</h4>
            <p className="text-center text-sm text-stone-400 mb-8">Click review points on the timeline to fight the curve.</p>
            
            <div className="relative h-56">
                <svg viewBox={`0 0 ${viewboxWidth} ${viewboxHeight}`} className="w-full h-full overflow-visible">
                    <defs>
                        <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
                            <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
                            <feMerge>
                                <feMergeNode in="coloredBlur"/>
                                <feMergeNode in="SourceGraphic"/>
                            </feMerge>
                        </filter>
                        <linearGradient id="skyGradient" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#0ea5e9" stopOpacity="0.4"/><stop offset="100%" stopColor="#0ea5e9" stopOpacity="0"/></linearGradient>
                        <linearGradient id="redGradient" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#ef4444" stopOpacity="0.2"/><stop offset="100%" stopColor="#ef4444" stopOpacity="0"/></linearGradient>
                    </defs>

                    {/* Y-Axis Labels */}
                    <text x="-10" y="10" fontSize="10" fill="#6b7280" textAnchor="end">100%</text>
                    <text x="-10" y={viewboxHeight-5} fontSize="10" fill="#6b7280" textAnchor="end">0%</text>

                    {/* Baseline Curve */}
                    <path d={baselineAreaPath} fill="url(#redGradient)" />
                    <path d={baselinePath} stroke="#ef4444" strokeWidth="2" strokeDasharray="4 4" fill="none" />
                    <circle cx={viewboxWidth} cy={viewboxHeight - 20} r="4" fill="#ef4444" />
                    
                    {/* Active Curve */}
                    <motion.path d={activeAreaPath} fill="url(#skyGradient)" initial={{opacity:0}} animate={{opacity:1}} transition={{ duration: 0.7, ease: "easeInOut" }} />
                    <motion.path d={activePath} stroke="#0ea5e9" strokeWidth="3" fill="none" style={{filter: 'drop-shadow(0 0 5px #0ea5e9)'}} transition={{ duration: 0.7, ease: "easeInOut" }} />
                    <motion.circle cx={viewboxWidth} cy={activeLastY} r="4" fill="#0ea5e9" style={{filter: 'drop-shadow(0 0 5px #0ea5e9)'}} transition={{ duration: 0.7, ease: "easeInOut" }} />

                    {/* Interactive Points */}
                    {reviewPoints.map((point, i) => (
                        <g key={`point-${i}`} onClick={() => handleReviewClick(i)} className="cursor-pointer">
                            <circle cx={point.x} cy="5" r="8" fill="#0ea5e9" fillOpacity={reviews[i] ? 1 : 0.2} style={{filter: 'drop-shadow(0 0 8px #0ea5e9aa)'}}/>
                            <circle cx={point.x} cy="5" r="4" fill="white" />
                        </g>
                    ))}
                </svg>
            </div>
            
             <div className="relative grid grid-cols-4 gap-2 pt-4 -mt-4">
                {reviewPoints.map((point, index) => (
                    <div key={index} className="text-center col-start-2" style={{ gridColumnStart: index + 2 }}>
                        <p className="text-xs text-stone-400 mt-2">Day {point.day}</p>
                    </div>
                ))}
            </div>

            <div className="mt-8 grid grid-cols-2 gap-4 items-center bg-white/5 p-4 rounded-xl">
                <div>
                    <p className="flex items-center gap-2 text-xs font-bold uppercase text-stone-400"><TrendingDown size={14} className="text-rose-400"/>Baseline</p>
                    <p className="text-3xl font-black text-rose-400 tracking-tighter">{retention.baseline}%</p>
                </div>
                 <div className="text-right">
                    <p className="flex items-center justify-end gap-2 text-xs font-bold uppercase text-stone-400"><Clock size={14} className="text-sky-400"/>Your Retention</p>
                    <p className="text-3xl font-black text-sky-400 tracking-tighter">{currentRetention}%</p>
                </div>
                 <div className="col-span-2 text-center">
                    <button onClick={() => setReviews([false, false, false])} className="inline-flex items-center gap-2 text-xs text-stone-500 hover:text-white transition-colors px-3 py-1 rounded-full hover:bg-white/10"><RefreshCcw size={12}/>Reset</button>
                 </div>
            </div>
        </div>
    );
};


const OptimalScheduleCalculator = () => {
    const [ri, setRi] = useState<string>('1_week');
    
    const schedules = {
        '1_week': { gap: '1-2 Days', ratio: '20-40%', example: 'Study Mon, Review Weds, Test next Mon.' },
        '1_month': { gap: '1 Week', ratio: '~20%', example: 'Study Week 1, Review Week 2, Test Week 5.' },
        '3_months': { gap: '2 Weeks', ratio: '~15%', example: 'Mid-term review should be 2 weeks after intro.' },
        '6_months': { gap: '3 Weeks', ratio: '~10-12%', example: 'Long-term prep requires substantial spacing.' },
    };
    
    return(
         <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Optimal Schedule Calculator</h4>
             <p className="text-center text-sm text-stone-500 mb-6">Based on the landmark Cepeda et al. (2008) research.</p>
             <div className="flex items-center justify-center gap-4">
                 <label className="font-bold">My test is in:</label>
                 <select value={ri} onChange={e => setRi(e.target.value)} className="p-2 bg-stone-100 rounded-lg">
                    <option value="1_week">1 Week</option>
                    <option value="1_month">1 Month</option>
                    <option value="3_months">3 Months</option>
                    <option value="6_months">6 Months</option>
                 </select>
             </div>
             <div className="mt-6 p-6 bg-sky-50 border-2 border-dashed border-sky-200 rounded-2xl text-center">
                <p className="text-sm text-sky-800">Optimal Review Gap (ISI):</p>
                <p className="font-bold text-2xl text-sky-600">{schedules[ri as keyof typeof schedules].gap}</p>
                <p className="text-xs text-sky-500 mt-4"><strong>Actionable Advice:</strong> {schedules[ri as keyof typeof schedules].example}</p>
             </div>
        </div>
    );
};


// --- MODULE COMPONENT ---
export const MasteringSpacedRepetitionModule: React.FC<MasteringSpacedRepetitionModuleProps> = ({ onBack }) => {
  const [activeSection, setActiveSection] = useState(0);
  const [unlockedSection, setUnlockedSection] = useState(0);
  
  const sections = [
    { id: 'forgetting-curve', title: 'The Forgetting Curve', eyebrow: '01 // The Default Setting', icon: Clock },
    { id: 'cramming-paradox', title: 'The Cramming Paradox', eyebrow: '02 // The Illusion of Speed', icon: BarChart2 },
    { id: 'desirable-difficulty', title: 'Desirable Difficulty', eyebrow: '03 // The Brain\'s Trigger', icon: Brain },
    { id: 'optimal-schedule', title: 'The Optimal Schedule', eyebrow: '04 // The Ridgeline Rule', icon: CalendarDays },
    { id: 'algorithmic-tools', title: 'Algorithmic Tools', eyebrow: '05 // The Autopilot', icon: RadioTower },
    { id: 'spacing-blueprint', title: 'Your Spacing Blueprint', eyebrow: '06 // The Action Plan', icon: Wrench },
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
            <p className="text-[9px] font-black text-sky-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 03</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">Spaced Repetition</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <motion.div
                  className="w-full bg-sky-500 shadow-[0_0_10px_rgba(14,165,233,0.5)]"
                  initial={{ height: 0 }}
                  animate={{ height: sections.length > 1 ? `${(unlockedSection / (sections.length - 1)) * 100}%` : '0%' }}
              />
          </div>
          {sections.map((section, idx) => {
            const isUnlocked = idx <= unlockedSection;
            const isActive = idx === activeSection;
            const isCompleted = idx < unlockedSection;
            return (
              <button key={section.id} disabled={!isUnlocked} onClick={() => handleJumpToSection(idx)} className={`relative z-10 w-full flex items-center gap-4 p-3 rounded-xl transition-all duration-500 text-left group ${isActive ? 'bg-sky-50 shadow-sm translate-x-2' : ''} ${!isUnlocked ? 'opacity-40 grayscale cursor-not-allowed' : 'hover:bg-stone-50'}`}>
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border-2 transition-all duration-500 ${isCompleted ? 'bg-sky-600 border-sky-600 text-white shadow-lg' : isActive ? 'bg-white border-sky-500 text-sky-600 shadow-xl rotate-12' : 'bg-white border-stone-200 text-stone-300'}`}>
                   {isCompleted ? <CheckCircle2 size={18} /> : isActive ? <section.icon size={18} /> : <Lock size={16} />}
                </div>
                <div className="flex-grow"><p className={`text-[8px] font-black uppercase tracking-widest ${isActive ? 'text-sky-500' : 'text-stone-400'}`}>{section.eyebrow.split('// ')[1]}</p><h4 className={`text-xs font-bold leading-tight ${isActive ? 'text-stone-900' : 'text-stone-500'}`}>{section.title}</h4></div>
              </button>
            );
          })}
        </div>

        <div className="mt-8 border-t border-stone-100 pt-8 flex flex-col items-center">
           <ActivityRing progress={progress} color="#0ea5e9" /><p className="text-[11px] font-black text-stone-900 uppercase tracking-widest text-center">Progress</p>
        </div>
      </aside>

      <main className="flex-grow flex flex-col items-center py-10 md:py-24 px-6 md:px-16 overflow-y-auto h-screen relative">
        <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:32px_32px] opacity-40 pointer-events-none" />
        <div className="w-full max-w-4xl relative z-10">
          <AnimatePresence mode="wait">
            <motion.div key={activeSection} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}>
              {activeSection === 0 && (
                <ReadingSection title="The Forgetting Curve." eyebrow="Step 1" icon={Clock}>
                  <p>Your brain is designed to forget. This isn't a flaw; it's a feature. To survive, your brain has to constantly discard useless information. The problem is, it defaults to forgetting almost everything. This process was first mapped in 1885 by Hermann Ebbinghaus, who discovered the <Highlight description="The mathematical certainty that, without active reinforcement, your memory for new information will decay exponentially over time.">Forgetting Curve</Highlight>.</p>
                  <p>The curve is brutal. Without reviewing, you can lose over 50% of new information within an hour, and up to 80% within a day. This is why "cramming" is a catastrophic waste of time. To build lasting knowledge, you can't just put information *in* to your brain; you have to interrupt the process of it leaking *out*.</p>
                  <ForgettingCurveVisualizer />
                </ReadingSection>
              )}
              {activeSection === 1 && (
                <ReadingSection title="The Cramming Paradox." eyebrow="Step 2" icon={BarChart2}>
                    <p>If cramming is so bad, why does everyone do it? Because of a metacognitive trap called the <Highlight description="The common student experience where massed practice (cramming) leads to high immediate test performance but catastrophic long-term forgetting, reinforcing an ineffective study habit.">Cramming Paradox</Highlight>. For tests that happen immediately after studying (minutes or hours), cramming works. It keeps information active in your temporary working memory, creating a powerful "Illusion of Competence."</p>
                    <p>This gives you a false sense of security. You score well on the immediate test, which "rewards" the cramming behaviour. But the information never gets consolidated into long-term memory. As the research shows, for the same amount of study time, <Highlight description="Also called Distributed Practice. The method of spreading study sessions out over time, which is proven to be vastly superior to cramming for long-term retention.">Spaced Practice</Highlight> can triple the durability of your memory.</p>
                </ReadingSection>
              )}
               {activeSection === 2 && (
                <ReadingSection title="Desirable Difficulty." eyebrow="Step 3" icon={Brain}>
                  <p>Why is spacing so much more powerful? Because it leverages the "struggle" of forgetting. This is the principle of <Highlight description="A learning task that requires a considerable but desirable amount of effort, thereby improving long-term performance. Spacing creates this by allowing some forgetting to occur between sessions.">Desirable Difficulty</Highlight>. When you space out your study, you allow your memory to fade slightly. When you come back to review it, your brain has to work harder to retrieve it.</p>
                  <p>This effortful retrieval is a powerful biological signal. It tells your brain, "This information is important! I had to work hard to find it, so I should strengthen the pathway to make it easier next time." Cramming eliminates this difficulty; the information is always right there, so your brain sees no reason to invest the resources in building a strong, long-term memory trace.</p>
                </ReadingSection>
              )}
              {activeSection === 3 && (
                <ReadingSection title="The Optimal Schedule." eyebrow="Step 4" icon={CalendarDays}>
                  <p>So, what is the perfect gap between study sessions? There's no single magic number. Landmark research by Cepeda and Pashler found that the <Highlight description="The Inter-Study Interval (ISI) is the time gap between your study sessions.">Optimal Gap</Highlight> depends entirely on when you need to remember the information—the <Highlight description="The Retention Interval (RI) is the time between your last study session and the final test.">Retention Interval</Highlight>.</p>
                  <p>Their "Ridgeline Rule" gives us a practical ratio: to maximize recall, your review gap should be roughly **5-20%** of the time until the test. For a test in a week, you need a short gap (1-2 days). For a test in 6 months, you need a much longer gap (e.g., 3 weeks). This is because a longer gap allows for more forgetting, creating a more "desirable difficulty" and triggering a stronger memory consolidation process for the long haul.</p>
                  <OptimalScheduleCalculator />
                </ReadingSection>
              )}
               {activeSection === 4 && (
                <ReadingSection title="Algorithmic Tools." eyebrow="Step 5" icon={RadioTower}>
                  <p>Managing the optimal schedule for thousands of facts across dozens of subjects is humanly impossible. This is where <Highlight description="Software (like Anki or SuperMemo) that uses algorithms based on the Forgetting Curve and Spacing Effect to automatically schedule reviews for individual pieces of information (like flashcards).">Spaced Repetition Software (SRS)</Highlight> comes in. These tools are like a personal tutor for your memory.</p>
                  <p>Using an app like Anki, you create digital flashcards. Each time you review a card, you tell the algorithm how difficult it was ("Again," "Hard," "Good," "Easy"). The algorithm then uses this feedback to predict when you'll be on the verge of forgetting that specific card and schedules it for review at that precise moment. It automates the entire process of optimal scheduling, ensuring you review the right thing at the right time.</p>
                  <MicroCommitment>
                    <p>Download Anki on your phone or computer. Don't worry about making cards yet. Just get the tool. This is the first step to building an automated, long-term memory system.</p>
                  </MicroCommitment>
                </ReadingSection>
              )}
               {activeSection === 5 && (
                <ReadingSection title="Your Spacing Blueprint." eyebrow="Step 6" icon={Wrench}>
                  <p>You now have the science to defeat the Forgetting Curve. The timing of your study is as important as the content. This section provides a simple, actionable heuristic to put this into practice immediately, even without software.</p>
                  <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
                    <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Actionable Advice: The Heuristic Planner</h4>
                    <p className="text-center text-sm text-stone-500 mb-8">For any test or exam, follow this simple rule-of-thumb schedule.</p>
                    <div className="grid grid-cols-3 gap-4 text-center">
                        <div className="p-4 bg-stone-50 rounded-xl">
                            <p className="font-bold">Day 1: Learn</p>
                            <p className="text-xs mt-1">First exposure to the material in class.</p>
                        </div>
                         <div className="p-4 bg-stone-50 rounded-xl">
                            <p className="font-bold">Day 2-3: First Review</p>
                            <p className="text-xs mt-1">Review the material using Active Recall. This is the most critical review.</p>
                        </div>
                         <div className="p-4 bg-stone-50 rounded-xl">
                            <p className="font-bold">Day 7 (or before test): Final Review</p>
                            <p className="text-xs mt-1">A final active recall session to consolidate the memory.</p>
                        </div>
                    </div>
                  </div>
                  <MicroCommitment>
                    <p>Pick one subject you have a test for in the next two weeks. Open your calendar and schedule two short review sessions for it between now and then, following the "Ridgeline Rule".</p>
                  </MicroCommitment>
                </ReadingSection>
              )}
              <footer className="mt-24 flex items-center justify-between pt-12 border-t border-stone-200/60 px-4">
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handlePrev} disabled={activeSection === 0} className={`flex items-center gap-4 bg-stone-100 text-stone-800 px-8 py-4 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all shadow-sm ${activeSection === 0 ? 'opacity-0 pointer-events-none' : ''}`}>
                  <ArrowLeft size={16} /> Prev
                </motion.button>
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handleCompleteSection} className="group relative flex items-center gap-4 bg-stone-900 text-white px-12 py-6 rounded-2xl font-black text-[12px] uppercase tracking-widest hover:bg-sky-600 transition-all shadow-[0_20px_50px_rgba(0,0,0,0.2)] overflow-hidden">
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