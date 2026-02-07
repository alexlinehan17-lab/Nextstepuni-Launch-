/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, Calculator, Shield, Target, BookOpen, Timer, Brain, PenSquare, Briefcase, Eye, HeartPulse, PieChart, Info, ChevronsUpDown,
} from 'lucide-react';

type ModuleProgress = {
  unlockedSection: number;
};

interface LeavingCertStrategyModuleProps {
  onBack: () => void;
  progress: ModuleProgress;
  onProgressUpdate: (progress: ModuleProgress) => void;
}

const Highlight = ({ children, description, color = "bg-red-100/40", textColor = "text-red-900", decorColor = "decoration-red-400/40", hoverColor="hover:bg-red-200/60" }: { children?: React.ReactNode, description: string, color?: string, textColor?: string, decorColor?: string, hoverColor?: string }) => {
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
              <p className="font-sans font-bold text-red-400 mb-2 uppercase tracking-[0.2em] text-[9px]">The Academic Insight</p>
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
        <div className="w-12 h-12 rounded-2xl bg-stone-900 flex items-center justify-center text-red-400 shadow-xl border border-white/10">
          <Icon size={24} />
        </div>
      </div>
      <span className="inline-flex items-center gap-2 px-3 py-1 bg-red-50 text-red-600 text-[10px] font-black tracking-[0.4em] uppercase rounded-full mb-4">
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
  <div className="my-12 p-8 bg-red-50/50 border-2 border-dashed border-red-200 rounded-3xl">
    <div className="flex items-start gap-5">
      <div className="w-11 h-11 rounded-xl bg-red-500 text-white flex items-center justify-center shrink-0 mt-1 shadow-lg shadow-red-500/20">
        <Flag size={20} />
      </div>
      <div>
        <h4 className="font-bold text-red-800 text-sm uppercase tracking-widest">Your Mission (Under 5 Mins)</h4>
        <div className="text-stone-600 mt-2 font-medium leading-relaxed">
          {children}
        </div>
      </div>
    </div>
  </div>
);

const ActivityRing = ({ progress, color = "#ef4444" }: { progress: number, color?: string }) => {
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

const PointsCalculator = () => {
    const grades = [
        { grade: 'H1', hl: 100, ol: 56 }, { grade: 'H2', hl: 88, ol: 46 }, { grade: 'H3', hl: 77, ol: 37 },
        { grade: 'H4', hl: 66, ol: 28 }, { grade: 'H5', hl: 56, ol: 20 }, { grade: 'H6', hl: 46, ol: 12 },
        { grade: 'H7', hl: 37, ol: 0 }, { grade: 'H8', hl: 0, ol: 0 }
    ];
    const getPoints = (grade: string, level: 'hl' | 'ol', isMaths: boolean) => {
        const g = grades.find(g => g.grade === grade);
        if (!g) return 0;
        let points = g[level];
        if (isMaths && level === 'hl' && ['H1','H2','H3','H4','H5','H6'].includes(grade)) {
            points += 25;
        }
        return points;
    }

    const [subjects, setSubjects] = useState(Array(7).fill({grade: 'H4', level: 'hl'}));

    const updateSubject = (index: number, field: string, value: string) => {
        const newSubjects = [...subjects];
        newSubjects[index] = {...newSubjects[index], [field]: value};
        setSubjects(newSubjects);
    };
    
    const subjectPoints = subjects.map((s, i) => getPoints(s.grade, s.level, i === 0));
    const totalPoints = subjectPoints.sort((a, b) => b - a).slice(0, 6).reduce((sum, p) => sum + p, 0);

    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">CAO Points Calculator</h4>
            <p className="text-center text-sm text-stone-500 mb-8">See how the "Best Six" and Maths Bonus work in practice.</p>
            <div className="space-y-3">
                {subjects.map((s, i) => (
                    <div key={i} className={`p-3 rounded-lg flex items-center gap-4 ${i === 0 ? 'bg-amber-50' : 'bg-stone-50'}`}>
                        <span className="font-bold text-sm w-24">{i === 0 ? 'Maths' : `Subject ${i+1}`}</span>
                        <select value={s.level} onChange={e => updateSubject(i, 'level', e.target.value)} className="p-1 rounded-md bg-white border border-stone-200">
                            <option value="hl">Higher</option>
                            <option value="ol">Ordinary</option>
                        </select>
                        <select value={s.grade} onChange={e => updateSubject(i, 'grade', e.target.value)} className="p-1 rounded-md bg-white border border-stone-200">
                            {grades.map(g => <option key={g.grade} value={g.grade}>{g.grade}</option>)}
                        </select>
                        <span className="ml-auto font-bold text-lg">{subjectPoints[i]}</span>
                    </div>
                ))}
            </div>
            <div className="mt-8 p-6 bg-stone-900 rounded-2xl text-center">
                <p className="text-sm font-bold text-stone-400">Total "Best Six" Points:</p>
                <p className="text-5xl font-black text-white">{totalPoints}</p>
            </div>
        </div>
    );
};

const SubjectClusterExplorer = () => {
    const [activeCluster, setActiveCluster] = useState<string | null>(null);
    const clusters = {
        'Lab Science': ['Biology', 'Ag Science', 'Home Ec', 'Physics', 'Applied Maths'],
        'Business': ['Business', 'Accounting', 'Economics'],
    };

    const isHighlighted = (subject: string) => activeCluster && clusters[activeCluster as keyof typeof clusters].includes(subject);

    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Syllabus Overlap Explorer</h4>
            <p className="text-center text-sm text-stone-500 mb-6">Click a cluster to see how subjects connect and reduce your workload.</p>
            <div className="flex justify-center gap-3 mb-6">
                <button onClick={() => setActiveCluster('Lab Science')} className={`px-4 py-2 text-sm font-bold rounded-lg border-2 ${activeCluster === 'Lab Science' ? 'bg-emerald-500 text-white border-emerald-500' : 'bg-emerald-50 text-emerald-800 border-emerald-200'}`}>Lab Science</button>
                <button onClick={() => setActiveCluster('Business')} className={`px-4 py-2 text-sm font-bold rounded-lg border-2 ${activeCluster === 'Business' ? 'bg-sky-500 text-white border-sky-500' : 'bg-sky-50 text-sky-800 border-sky-200'}`}>Business</button>
                <button onClick={() => setActiveCluster(null)} className="text-xs">Reset</button>
            </div>
            <div className="grid grid-cols-3 gap-3 text-center">
                <div className={`p-3 rounded-lg border-2 ${isHighlighted('Biology') ? 'border-emerald-400 bg-emerald-50' : 'border-stone-200'}`}>Biology</div>
                <div className={`p-3 rounded-lg border-2 ${isHighlighted('Ag Science') ? 'border-emerald-400 bg-emerald-50' : 'border-stone-200'}`}>Ag Science</div>
                <div className={`p-3 rounded-lg border-2 ${isHighlighted('Home Ec') ? 'border-emerald-400 bg-emerald-50' : 'border-stone-200'}`}>Home Ec</div>
                <div className={`p-3 rounded-lg border-2 ${isHighlighted('Physics') ? 'border-emerald-400 bg-emerald-50' : 'border-stone-200'}`}>Physics</div>
                <div className={`p-3 rounded-lg border-2 ${isHighlighted('Applied Maths') ? 'border-emerald-400 bg-emerald-50' : 'border-stone-200'}`}>Applied Maths</div>
                <div className={`p-3 rounded-lg border-2 ${isHighlighted('Business') ? 'border-sky-400 bg-sky-50' : 'border-stone-200'}`}>Business</div>
                <div className={`p-3 rounded-lg border-2 ${isHighlighted('Accounting') ? 'border-sky-400 bg-sky-50' : 'border-stone-200'}`}>Accounting</div>
                <div className={`p-3 rounded-lg border-2 ${isHighlighted('Economics') ? 'border-sky-400 bg-sky-50' : 'border-stone-200'}`}>Economics</div>
            </div>
        </div>
    );
};

const CommandWordDecoder = () => {
    const words = [
        { word: "Describe", expectation: '"Paint a picture" with facts.', pitfall: "Just a list of words." },
        { word: "Explain", expectation: 'Give the reason WHY (Cause & Effect).', pitfall: "Just describing what happens." },
        { word: "Compare", expectation: 'Identify similarities AND differences.', pitfall: "Writing two separate descriptions." },
        { word: "Evaluate", expectation: 'Make a judgement based on evidence. Weigh pros/cons.', pitfall: "Giving an opinion without evidence." },
    ];
    const [selected, setSelected] = useState(words[0]);

    return (
         <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Command Word Decoder</h4>
            <p className="text-center text-sm text-stone-500 mb-8">Misinterpreting this word is the #1 cause of losing marks.</p>
            <div className="flex justify-center flex-wrap gap-2 mb-6">
                {words.map(w => <button key={w.word} onClick={() => setSelected(w)} className={`px-4 py-2 font-mono text-sm rounded-lg border-2 ${selected.word === w.word ? 'bg-red-500 text-white border-red-500' : 'bg-stone-100 border-stone-200'}`}>{w.word}</button>)}
            </div>
             <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                 <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-lg">
                    <p className="text-xs font-bold text-emerald-700">EXPECTATION</p>
                    <p className="mt-2 text-sm">{selected.expectation}</p>
                 </div>
                 <div className="p-4 bg-rose-50 border border-rose-200 rounded-lg">
                    <p className="text-xs font-bold text-rose-700">COMMON PITFALL</p>
                    <p className="mt-2 text-sm">{selected.pitfall}</p>
                 </div>
             </div>
        </div>
    );
}

// --- MODULE COMPONENT ---
export const LeavingCertStrategyModule: React.FC<LeavingCertStrategyModuleProps> = ({ onBack, progress, onProgressUpdate }) => {
  const [activeSection, setActiveSection] = useState(progress.unlockedSection);
  const unlockedSection = progress.unlockedSection;
  
  const sections = [
    { id: 'points-marketplace', title: 'The Points Marketplace', eyebrow: '01 // The Rules of the Game', icon: Calculator },
    { id: 'portfolio-construction', title: 'Portfolio Construction', eyebrow: '02 // Strategic Subject Selection', icon: Briefcase },
    { id: 'core-tactics', title: 'Tactics: Core Subjects', eyebrow: '03 // The Big Three', icon: Target },
    { id: 'elective-tactics', title: 'Tactics: Elective Subjects', eyebrow: '04 // Exploiting the System', icon: PenSquare },
    { id: 'hidden-curriculum', title: 'The Hidden Curriculum', eyebrow: '05 // Examiner Psychology', icon: Eye },
    { id: 'exam-day-protocol', title: 'Exam Day Protocol', eyebrow: '06 // Execution in the Arena', icon: HeartPulse },
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
            <p className="text-[9px] font-black text-red-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 01</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">The Points Protocol</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <motion.div
                  className="w-full bg-red-500 shadow-[0_0_10px_rgba(220,38,38,0.5)]"
                  style={{ height: `${progressPercentage}%` }}
              />
          </div>
          {sections.map((section, idx) => {
            const isUnlocked = idx <= unlockedSection;
            const isActive = idx === activeSection;
            const isCompleted = idx < unlockedSection;
            return (
              <button key={section.id} disabled={!isUnlocked} onClick={() => handleJumpToSection(idx)} className={`relative z-10 w-full flex items-center gap-4 p-3 rounded-xl transition-all duration-500 text-left group ${isActive ? 'bg-red-50 shadow-sm translate-x-2' : ''} ${!isUnlocked ? 'opacity-40 grayscale cursor-not-allowed' : 'hover:bg-stone-50'}`}>
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border-2 transition-all duration-500 ${isCompleted ? 'bg-red-600 border-red-600 text-white shadow-lg' : isActive ? 'bg-white border-red-500 text-red-600 shadow-xl rotate-12' : 'bg-white border-stone-200 text-stone-300'}`}>
                   {isCompleted ? <CheckCircle2 size={18} /> : isActive ? <section.icon size={18} /> : <Lock size={16} />}
                </div>
                <div className="flex-grow"><p className={`text-[8px] font-black uppercase tracking-widest ${isActive ? 'text-red-500' : 'text-stone-400'}`}>{section.eyebrow.split('// ')[1]}</p><h4 className={`text-xs font-bold leading-tight ${isActive ? 'text-stone-900' : 'text-stone-500'}`}>{section.title}</h4></div>
              </button>
            );
          })}
        </div>
        <div className="mt-8 border-t border-stone-100 pt-8 flex flex-col items-center">
           <ActivityRing progress={progressPercentage} color="#ef4444" /><p className="text-[11px] font-black text-stone-900 uppercase tracking-widest text-center">Progress</p>
        </div>
      </aside>

      <main className="flex-grow flex flex-col items-center py-10 md:py-24 px-6 md:px-16 overflow-y-auto h-screen relative">
        <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:32px_32px] opacity-40 pointer-events-none" />
        <div className="w-full max-w-4xl relative z-10">
          <AnimatePresence mode="wait">
            <motion.div key={activeSection} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}>
              {activeSection === 0 && (
                <ReadingSection title="The Points Marketplace." eyebrow="Step 1" icon={Calculator}>
                  <p>The Leaving Cert is not just an exam; it's a points accumulation game. To win, you must shift your mindset from a passive student to an active tactician. This means moving beyond "hard work" and focusing on <Highlight description="The true differentiator in the points race; applying effort to the areas with the highest potential return on investment.">efficiency</Highlight>. The points system is a rigid algorithm with exploitable inefficiencies.</p>
                  <p>The three key rules of the game are: 1) The <Highlight description="Your total score is based on your six highest results. Your seventh subject is an insurance policy, allowing one catastrophic failure to be discarded.">"Best Six" Rule</Highlight>, 2) The 25 <Highlight description="Awarded for a H6 or higher in Higher Level Maths, this radically transforms the value of the subject, making a low pass more valuable than a high distinction in other subjects.">Bonus Points</Highlight> for Maths, and 3) The <Highlight description="The 37 points awarded for a H7 (30-39%) de-risks taking Higher Level, creating a 'Reach Strategy' where aiming high has a limited downside.">H7 Safety Net</Highlight>. Understanding these rules is the first step to mastering the system.</p>
                  <PointsCalculator />
                </ReadingSection>
              )}
               {activeSection === 1 && (
                <ReadingSection title="Portfolio Construction." eyebrow="Step 2" icon={Briefcase}>
                  <p>If the points system is a market, your subject choice is your investment portfolio. The goal is to maximize your points yield while minimizing cognitive load. This means debunking the <Highlight description="The idea that some subjects are inherently 'easy'. H1 rates are often misleading due to self-selecting groups of students (e.g., native speakers in language subjects).">'Easy Subject' Myth</Highlight> and instead focusing on structural advantages.</p>
                  <p>The two most powerful strategies are the <Highlight description="Grouping subjects that share content (e.g., Biology and Ag Science) to reduce the total volume of unique information you need to learn.">"Cluster Strategy"</Highlight> and the <Highlight description="Choosing subjects with substantial coursework or oral components (e.g., Irish, DCG, Geography) to secure a large percentage of your grade before the written exams.">"Banking Marks" Strategy</Highlight>. This reduces the pressure and variance of a "bad day" in June.</p>
                  <SubjectClusterExplorer />
                </ReadingSection>
              )}
              {activeSection === 2 && (
                <ReadingSection title="Tactics: Core Subjects." eyebrow="Step 3" icon={Target}>
                  <p>General study habits are not enough. You must study the exam itself. For English, this means mastering the rigid, algorithmic <Highlight description="The marking criteria for English: Purpose (30%), Coherence (30%), Language (30%), and Mechanics (10%). Writing to these criteria is non-negotiable.">PCLM Engine</Highlight> and implementing a ruthless timing strategy for Paper 2.</p>
                  <p>For Maths, it's about exploiting the <Highlight description="The system of 'Partial Credit' where marks are awarded for any correct step, even if the final answer is wrong. Never leave a blank space.">Step-Mark Economy</Highlight>. For Irish, it's about maximizing the <Highlight description="The Oral exam accounts for 40% of the total grade. The strategy is 'fluency trumps accuracy'—it's better to keep talking with minor errors than to freeze in silence.">Oral Dividend</Highlight>.</p>
                </ReadingSection>
              )}
               {activeSection === 3 && (
                <ReadingSection title="Tactics: Elective Subjects." eyebrow="Step 4" icon={PenSquare}>
                  <p>Elective subjects have their own unique algorithms. Biology is a <Highlight description="The marking scheme is binary: specific keywords earn marks, synonyms often do not. 'Semi-permeable membrane' is a non-negotiable keyword for Osmosis.">Semantic Precision Game</Highlight> where specific keywords are everything. Geography is an <Highlight description="Significant Relevant Points (SRPs) are the currency of Geography. An essay is a collection of these distinct factual points, typically worth 2 marks each.">SRP Algorithm</Highlight> where you must deliver short, punchy, fact-laden paragraphs.</p>
                  <p>Business requires <Highlight description="The expected format for long questions: State the point, Explain the concept, provide a relevant Example.">Structure as Content</Highlight>, following the "State, Explain, Example" format. These are not suggestions; they are the rules of the game you must play to win.</p>
                </ReadingSection>
              )}
               {activeSection === 4 && (
                <ReadingSection title="The Hidden Curriculum." eyebrow="Step 5" icon={Eye}>
                  <p>Beyond the syllabus lies the "Hidden Curriculum"—the specific language and expectations of the State Examinations Commission. Every question contains a <Highlight description="The verb in the question (e.g., Describe, Explain, Evaluate) that dictates the required style of answer. Misinterpreting this is a leading cause of losing marks.">Command Word</Highlight> that dictates the required output. 'Describe' asks for a picture in words; 'Explain' asks for a cause-and-effect reason. They are not the same.</p>
                  <p>The most valuable strategic document is the <Highlight description="Published every few years, this document details common student errors. It is a goldmine of 'negative data'—telling you exactly what not to do.">Chief Examiner's Report (CER)</Highlight>. This is the official "cheat sheet" for the exam, outlining the most common pitfalls that you must learn to avoid.</p>
                  <CommandWordDecoder />
                  <MicroCommitment><p>Go to the SEC website, find the most recent Chief Examiner's Report for your favourite subject, and read only the "Recommendations to Candidates" section. You've just accessed the official cheat sheet.</p></MicroCommitment>
                </ReadingSection>
              )}
               {activeSection === 5 && (
                <ReadingSection title="Exam Day Protocol." eyebrow="Step 6" icon={HeartPulse}>
                  <p>All your preparation is useless without effective execution in the arena. The exam hall is a high-pressure environment where physiological regulation is as important as academic knowledge.</p>
                  <p>Master the <Highlight description="A protocol for the start of an exam: 30 seconds of tactical breathing to calm the nervous system, followed by a 'brain dump' of key formulas and quotes onto rough work paper to free up working memory.">"First 5 Minutes" Protocol</Highlight> to manage panic. Adhere to a <Highlight description="A strict timing plan where you move on when the allocated time for a question is up, no matter what. The 'first marks' of the next question are always easier than the 'last marks' of the current one.">Non-Negotiable Contract</Highlight> for time management. And finally, use the Post-Exam Script Review in September as a final strategic lever for appeals and, more importantly, for learning.</p>
                </ReadingSection>
              )}
              <footer className="mt-24 flex items-center justify-between pt-12 border-t border-stone-200/60 px-4">
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handlePrev} disabled={activeSection === 0} className={`flex items-center gap-4 bg-stone-100 text-stone-800 px-8 py-4 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all shadow-sm ${activeSection === 0 ? 'opacity-0 pointer-events-none' : ''}`}>
                  <ArrowLeft size={16} /> Prev
                </motion.button>
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handleCompleteSection} className="group relative flex items-center gap-4 bg-stone-900 text-white px-12 py-6 rounded-2xl font-black text-[12px] uppercase tracking-widest hover:bg-red-600 transition-all shadow-[0_20px_50px_rgba(0,0,0,0.2)] overflow-hidden">
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
