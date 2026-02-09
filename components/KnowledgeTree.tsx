/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, useMotionValue, useMotionTemplate, AnimatePresence } from 'framer-motion';
import { 
  Sprout, Zap, Rocket, Target, FlaskConical, 
  Layout, ArrowRight, Sparkles, Beaker
} from 'lucide-react';
import { CourseData, BentoModuleTile } from './Library';

// FIX: Cast motion components to any to bypass broken type definitions
const MotionDiv = motion.div as any;
const MotionCircle = motion.circle as any;

export type CategoryType = 
  | 'architecture-mindset' 
  | 'science-growth' 
  | 'learning-cheat-codes' 
  | 'the-shield' 
  | 'the-launchpad' 
  | 'exam-zone'
  | 'subject-specific-science';

type UserProgress = {
  [moduleId: string]: { unlockedSection: number };
};

interface KnowledgeTreeProps {
  onSelectCategory: (category: CategoryType) => void;
  onGoToInnovationZone: () => void;
  onSelectModule: (moduleId: string) => void;
  allCourses: CourseData[];
  categoryTitles: Record<CategoryType, string>;
  userProgress: UserProgress;
}

const ActivityRing = ({ 
  progress, 
  size = 52, 
  strokeWidth = 4, 
  color = "#3b82f6" 
}: { 
  progress: number, 
  size?: number, 
  strokeWidth?: number, 
  color?: string 
}) => {
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (progress / 100) * circumference;

  return (
    <div className="relative flex items-center justify-center shrink-0" style={{ width: size, height: size }}>
      <svg className="w-full h-full -rotate-90 overflow-visible" viewBox={`0 0 ${size} ${size}`}>
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="currentColor"
          strokeWidth={strokeWidth}
          fill="transparent"
          className="text-zinc-100 dark:text-white/5"
        />
        <MotionCircle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={color}
          strokeWidth={strokeWidth}
          fill="transparent"
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          whileInView={{ strokeDashoffset: offset }}
          viewport={{ once: true }}
          transition={{ duration: 1.5, delay: 0.5, ease: "easeOut" }}
          strokeLinecap="round"
        />
      </svg>
      <div className="absolute flex flex-col items-center justify-center leading-none">
        <span className="text-[14px] font-semibold text-zinc-900 dark:text-white tracking-tighter">
          {Math.round(progress)}
        </span>
        <span className="text-[6px] font-semibold uppercase text-zinc-400 dark:text-white/30 -mt-0.5">%</span>
      </div>
    </div>
  );
};

interface BentoTileProps {
  icon: any, 
  title: string, 
  subtitle: string, 
  onClick: () => void,
  accentHex: string,
  progress?: number,
  className?: string,
  delay?: number
}

const BentoTile: React.FC<BentoTileProps> = ({ 
  icon: Icon, 
  title, 
  subtitle, 
  onClick, 
  accentHex,
  progress = 0,
  className = "",
  delay = 0
}) => {
  const mouseX = useMotionValue(0);
  const mouseY = useMotionValue(0);

  function handleMouseMove({ currentTarget, clientX, clientY }: React.MouseEvent) {
    const { left, top } = currentTarget.getBoundingClientRect();
    mouseX.set(clientX - left);
    mouseY.set(clientY - top);
  }

  return (
    <MotionDiv
      initial={{ opacity: 0, scale: 0.95, y: 20 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      transition={{ duration: 0.8, delay, ease: [0.16, 1, 0.3, 1] }}
      onClick={onClick}
      onMouseMove={handleMouseMove}
      className={`group relative overflow-hidden rounded-2xl bg-white/80 dark:bg-white/5 backdrop-blur-2xl border border-zinc-200/50 dark:border-white/10 cursor-pointer transition-all duration-500 hover:border-[#CC785C]/30 dark:hover:border-white/20 shadow-xl hover:shadow-2xl dark:shadow-[0_20px_50px_rgba(0,0,0,0.3)] ${className}`}
    >
      {/* Localized Glow Effect */}
      <MotionDiv
        className="pointer-events-none absolute -inset-px rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"
        style={{
          background: useMotionTemplate`
            radial-gradient(
              600px circle at ${mouseX}px ${mouseY}px,
              ${accentHex}15,
              transparent 80%
            )
          `,
        }}
      />

      <div className="relative z-10 p-8 h-full flex flex-col justify-between">
        <div>
          <div className="flex items-center justify-between mb-8">
            <div 
              className="w-14 h-14 rounded-2xl bg-white dark:bg-white/5 flex items-center justify-center border border-zinc-100 dark:border-white/10 shadow-sm"
              style={{ color: accentHex }}
            >
              <Icon size={28} strokeWidth={1.5} />
            </div>
            
            <div className="opacity-0 group-hover:opacity-100 transition-all duration-500 transform translate-x-4 group-hover:translate-x-0">
               <ArrowRight size={20} className="text-zinc-400 dark:text-white/40" />
            </div>
          </div>
          
          <div className="flex items-center gap-2 mb-2">
            <p className="font-mono text-[10px] font-semibold uppercase tracking-wider text-zinc-400 dark:text-white/40">
              {subtitle}
            </p>
          </div>
          <h3 className="font-serif text-2xl md:text-3xl text-zinc-900 dark:text-white leading-tight font-semibold tracking-tight">
            {title}
          </h3>
        </div>

        <div className="mt-8 flex items-center justify-between gap-6 pt-6 border-t border-zinc-100 dark:border-white/5">
            <div className="flex flex-col">
              <span className="text-[10px] font-mono font-bold uppercase tracking-widest text-zinc-400 dark:text-white/40 mb-1">Progress</span>
              <span className="text-[9px] font-semibold uppercase tracking-wider text-zinc-300 dark:text-white/10 group-hover:text-zinc-900 dark:group-hover:text-white transition-colors duration-500">Active</span>
            </div>
            
            <div className="transition-all duration-500 transform group-hover:scale-110">
               <ActivityRing progress={progress} color={accentHex} />
            </div>
        </div>
      </div>
      
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        <div className="absolute top-[-30%] right-[-20%] w-[60%] h-[60%] rounded-full opacity-30 dark:opacity-20 blur-[60px]" style={{ backgroundColor: accentHex + '10' }} />
      </div>
    </MotionDiv>
  );
};

export const KnowledgeTree: React.FC<KnowledgeTreeProps> = ({ onSelectCategory, onGoToInnovationZone, allCourses, onSelectModule, categoryTitles, userProgress }) => {
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  
  const getCategoryProgress = (category: CategoryType) => {
    const categoryCourses = allCourses.filter(c => c.category === category);
    if (categoryCourses.length === 0) return 0;

    const totalCourses = categoryCourses.length;
    const completedCourses = categoryCourses.reduce((count, course) => {
      const progress = userProgress[course.id];
      const isComplete = progress && progress.unlockedSection >= course.sectionsCount - 1;
      return count + (isComplete ? 1 : 0);
    }, 0);

    return (completedCourses / totalCourses) * 100;
  };

  const modules = [
    { 
      id: 'architecture-mindset', 
      title: "The Architecture of your Mindset", 
      subtitle: "Pillar 01",
      icon: Layout, 
      hex: "#3b82f6", 
      className: "md:col-span-4" 
    },
    { 
      id: 'science-growth', 
      title: "The Science of Growth", 
      subtitle: "Pillar 02",
      icon: Sprout, 
      hex: "#f59e0b",
      className: "md:col-span-2" 
    },
    { 
      id: 'learning-cheat-codes', 
      title: "The Science of Learning Effectively", 
      subtitle: "Pillar 03",
      icon: Zap, 
      hex: "#14b8a6", // Teal
      className: "md:col-span-2" 
    },
     { 
      id: 'subject-specific-science', 
      title: "Subject Specific Science", 
      subtitle: "Specialist",
      icon: Beaker, 
      hex: "#6b7280", // Gray
      className: "md:col-span-2" 
    },
    { 
      id: 'exam-zone', 
      title: "Exam Strategy and Points Maximisation", 
      subtitle: "Pillar 04",
      icon: Target, 
      hex: "#ef4444", // Red
      className: "md:col-span-2" 
    },
  ];

  const allTags = [...new Set(allCourses.flatMap(course => course.tags))].sort();

  const handleTagClick = (tag: string) => {
    const isSelected = selectedTags.includes(tag);
    if (isSelected) {
      setSelectedTags(selectedTags.filter(t => t !== tag));
    } else {
      if (selectedTags.length < 2) {
        setSelectedTags([...selectedTags, tag]);
      } else {
        setSelectedTags([selectedTags[1], tag]); // Replace the first tag
      }
    }
  };

  const filteredCourses = selectedTags.length > 0
    ? allCourses.filter(course => selectedTags.every(tag => course.tags.includes(tag as string)))
    : [];

  return (
    <div className="min-h-screen bg-zinc-50 dark:bg-zinc-950 overflow-x-hidden relative flex flex-col items-center pt-16 md:pt-32 pb-32 transition-colors duration-500 selection:bg-[#CC785C]/10 dark:selection:bg-[#CC785C]/20">

       {/* Ambient mesh background */}
      <div className="fixed inset-0 z-0 pointer-events-none overflow-hidden">
        <div className="absolute top-[-20%] left-[-10%] w-[60vw] h-[60vw] rounded-full bg-[#CC785C]/[0.05] dark:bg-[#CC785C]/[0.03] blur-[120px]" />
        <div className="absolute bottom-[-15%] right-[-10%] w-[50vw] h-[50vw] rounded-full bg-[#D4A27F]/[0.04] dark:bg-[#D4A27F]/[0.02] blur-[120px]" />
        <div className="absolute top-[30%] left-[60%] w-[30vw] h-[30vw] rounded-full bg-amber-500/[0.03] dark:bg-amber-500/[0.015] blur-[100px]" />
      </div>

      <div className="relative z-10 w-full max-w-7xl px-6">
        <header className="text-center mb-16">
          <h1 className="font-serif text-5xl md:text-7xl text-black dark:text-white tracking-tighter leading-none font-semibold dark:drop-shadow-[0_0_15px_rgba(255,255,255,0.1)]">
            Learning Lab
          </h1>
          <p className="max-w-2xl mx-auto mt-4 text-zinc-500 dark:text-zinc-400">
            A dynamic, science-backed curriculum designed to give you an unfair advantage in your final school exams. Select a pillar to begin.
          </p>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-6 gap-6">
          {modules.map((mod, i) => (
            <BentoTile 
              key={mod.id}
              title={mod.title}
              subtitle={mod.subtitle}
              icon={mod.icon}
              accentHex={mod.hex}
              onClick={() => onSelectCategory(mod.id as CategoryType)}
              progress={getCategoryProgress(mod.id as CategoryType)}
              className={mod.className}
              delay={i * 0.1}
            />
          ))}
           <BentoTile 
              title="The Innovation Zone"
              subtitle="Explore"
              icon={Rocket}
              accentHex="#8b5cf6" // Purple
              onClick={onGoToInnovationZone}
              className="md:col-span-6"
              delay={modules.length * 0.1}
            />
        </div>
        
        {/* Module Search */}
        <div className="mt-24">
            <h2 className="text-center font-serif text-3xl font-semibold mb-2 text-zinc-800 dark:text-white">Find Modules by Topic</h2>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8 max-w-md mx-auto">Filter modules by up to two tags to find connections and build a deeper web of knowledge.</p>
            <div className="flex flex-wrap justify-center gap-2 max-w-3xl mx-auto mb-12">
                {allTags.map(tag => (
                    <button 
                        key={tag}
                        onClick={() => handleTagClick(tag)}
                        className={`px-3 py-1.5 text-xs font-bold rounded-full border-2 transition-all duration-300 ${selectedTags.includes(tag) ? 'bg-[#CC785C] text-white border-[#CC785C]' : 'bg-white dark:bg-white/5 border-zinc-200 dark:border-white/10 hover:border-[#CC785C]/40 dark:hover:border-[#CC785C]/50'}`}
                    >
                        {tag}
                    </button>
                ))}
            </div>
            <AnimatePresence>
                {filteredCourses.length > 0 && (
                    <MotionDiv 
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-6"
                    >
                        {filteredCourses.map((course, index) => {
                            const progress = userProgress[course.id];
                            const isCompleted = progress && progress.unlockedSection >= course.sectionsCount - 1;
                            return (
                                <BentoModuleTile 
                                    key={course.id} 
                                    course={course}
                                    index={index}
                                    isUnlocked={true}
                                    isCompleted={isCompleted}
                                    onClick={() => onSelectModule(course.id)}
                                    categoryTitle={categoryTitles[course.category]}
                                />
                            )
                        })}
                    </MotionDiv>
                )}
            </AnimatePresence>
        </div>

      </div>
    </div>
  );
};
