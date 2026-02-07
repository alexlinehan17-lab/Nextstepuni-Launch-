

/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React from 'react';
import { motion } from 'framer-motion';
import { 
  ArrowLeft, FlaskConical, CheckCircle2, 
  ChevronRight, Lock, Sparkles, BookOpen,
  Zap, Brain, Target, Shield, Compass, Star, Hash
} from 'lucide-react';
import { CategoryType } from './KnowledgeTree';

// FIX: Cast motion components to any to bypass broken type definitions
const MotionDiv = motion.div as any;

export interface CourseData {
  id: string;
  category: CategoryType;
  title: string;
  subtitle: string;
  description: string;
  sectionsCount: number;
  tags: readonly string[];
  gradient: string;
  accentColor: string;
  auraColor?: string;
}

type UserProgress = {
  [moduleId: string]: { unlockedSection: number };
};

interface LibraryProps {
  title: string;
  courses: CourseData[];
  onSelectCourse: (courseId: string) => void;
  onBack: () => void;
  userProgress: UserProgress;
}

export interface BentoModuleTileProps {
  course: CourseData;
  index: number;
  isUnlocked: boolean;
  isCompleted: boolean;
  onClick: () => void;
  categoryTitle: string;
}

export const BentoModuleTile: React.FC<BentoModuleTileProps> = ({ 
  course, 
  index, 
  isUnlocked, 
  isCompleted, 
  onClick,
  categoryTitle
}) => {
  const icons = [BookOpen, Zap, Brain, Target, Shield, Compass, Star];
  const Icon = icons[index % icons.length];

  const getSpanClass = (idx: number) => {
    if (idx === 0) return "md:col-span-3 lg:col-span-4 lg:row-span-2 min-h-[400px]";
    if (idx === 1) return "md:col-span-3 lg:col-span-2 lg:row-span-1";
    if (idx === 2) return "md:col-span-3 lg:col-span-2 lg:row-span-1";
    if (idx % 5 === 0) return "md:col-span-6 lg:col-span-4";
    return "md:col-span-3 lg:col-span-2";
  };
  
  const pillBgColor = course.accentColor.replace('text-', 'bg-');


  return (
    <MotionDiv
      initial={{ opacity: 0, scale: 0.9, y: 20 }}
      whileInView={{ opacity: 1, scale: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.6, delay: index * 0.05, ease: [0.16, 1, 0.3, 1] }}
      whileHover={isUnlocked ? { scale: 1.03 } : {}}
      className={`group relative overflow-hidden rounded-[2rem] transition-all duration-500 ${getSpanClass(index)} 
        ${isUnlocked ? 'cursor-pointer hover:shadow-2xl' : 'cursor-not-allowed'}
      `}
      onClick={isUnlocked ? onClick : undefined}
    >
      {/* Category Pill */}
      <div className={`absolute top-6 left-6 z-20 px-3 py-1 rounded-full ${pillBgColor} border border-black/10 dark:border-white/10`}>
        <p className={`text-[9px] font-black uppercase tracking-wider text-white`}>{categoryTitle}</p>
      </div>

      {/* Background Aura Glow */}
      <div className={`absolute -inset-20 opacity-0 group-hover:opacity-20 transition-opacity duration-700 blur-[100px] pointer-events-none -z-10 ${course.accentColor.replace('text-', 'bg-')}`}></div>

      {/* Glass Surface */}
      <div className="h-full w-full bg-white/40 dark:bg-white/5 backdrop-blur-3xl border border-stone-200/50 dark:border-white/10 p-8 pt-16 flex flex-col justify-between relative z-10 overflow-hidden">
        
        {/* Subtle Noise/Grain texture for depth */}
        <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-[0.03] pointer-events-none"></div>

        <div>
          <div className="flex items-center justify-between mb-8">
            <MotionDiv 
              className={`w-14 h-14 rounded-2xl flex items-center justify-center transition-all duration-500 shadow-sm 
                ${isCompleted ? 'bg-emerald-500 text-white' : isUnlocked ? 'bg-stone-900 dark:bg-white text-white dark:text-stone-900' : 'bg-stone-200 dark:bg-stone-800 text-stone-400'}`}
              whileHover={isUnlocked ? { x: 5, y: -2 } : {}}
            >
              {isCompleted ? <CheckCircle2 size={28} /> : !isUnlocked ? <Lock size={24} /> : <Icon size={28} strokeWidth={1.5} />}
            </MotionDiv>
            
            <div className="flex flex-col items-end">
              <span className="font-mono text-[9px] font-black uppercase tracking-[0.4em] text-stone-400 dark:text-stone-500">Unit // 0{index + 1}</span>
              {isCompleted && <span className="text-[8px] font-bold text-emerald-500 uppercase tracking-widest mt-1">Validated</span>}
            </div>
          </div>

          <h3 className="font-serif text-2xl md:text-3xl text-stone-900 dark:text-white mb-4 leading-tight font-bold italic tracking-tight">
            {course.title}
          </h3>
          
          <p className="text-stone-500 dark:text-stone-400 text-sm leading-relaxed font-medium line-clamp-3 mb-8">
            {course.description}
          </p>
        </div>

        <div className="flex items-center justify-between mt-auto pt-6 border-t border-stone-200/30 dark:border-white/5">
          <div className="flex gap-2">
            {course.tags.slice(0, 2).map(tag => (
              <span key={tag} className="px-2.5 py-1 rounded-full bg-stone-100 dark:bg-white/5 text-stone-400 dark:text-stone-500 text-[9px] font-bold uppercase tracking-wider">
                {tag}
              </span>
            ))}
          </div>
          {isUnlocked && (
            <MotionDiv 
              className="text-stone-900 dark:text-white"
              whileHover={{ x: 5 }}
            >
              <ChevronRight size={20} />
            </MotionDiv>
          )}
        </div>

        {!isUnlocked && (
          <div className="absolute inset-0 bg-stone-100/40 dark:bg-black/40 backdrop-blur-[2px] flex items-center justify-center z-20">
            <div className="bg-white/80 dark:bg-stone-900/80 px-4 py-2 rounded-full border border-white/20 shadow-xl flex items-center gap-2">
               <Lock size={12} className="text-stone-400" />
               <span className="text-[10px] font-black uppercase tracking-widest text-stone-400">Locked</span>
            </div>
          </div>
        )}
      </div>
    </MotionDiv>
  );
};

export const Library: React.FC<LibraryProps> = ({ title, courses, onSelectCourse, onBack, userProgress }) => {
  const calculateCategoryProgress = () => {
    if (courses.length === 0) return 0;
    const totalCourses = courses.length;
    const completedCourses = courses.reduce((count, course) => {
      const progress = userProgress[course.id];
      const isComplete = progress && progress.unlockedSection >= course.sectionsCount - 1;
      return count + (isComplete ? 1 : 0);
    }, 0);
    return Math.round((completedCourses / totalCourses) * 100);
  };

  const overallProgress = calculateCategoryProgress();
  const unlockedIndex = courses.length; // For now, all modules in a category are unlocked by default

  return (
    <div className="min-h-screen bg-[#FDFCFB] dark:bg-[#0A0A0B] transition-colors duration-500 overflow-x-hidden relative flex flex-col items-center pt-32 pb-48">
      
      {/* Texture & Atmospheric Lighting */}
      <div className="fixed inset-0 z-0 pointer-events-none overflow-hidden">
        <div className="absolute top-[-20%] left-[-10%] w-[70vw] h-[70vw] bg-blue-500/5 blur-[150px] rounded-full" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[50vw] h-[50vw] bg-emerald-500/5 blur-[120px] rounded-full" />
        <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] dark:bg-[radial-gradient(#1e293b_1px,transparent_1px)] [background-size:48px_48px] opacity-10"></div>
      </div>

      <header className="fixed top-0 left-0 right-0 z-[60] bg-white/60 dark:bg-[#0A0A0B]/60 backdrop-blur-2xl border-b border-stone-200/50 dark:border-white/5 px-10 py-6">
        <div className="container mx-auto flex items-center justify-between">
          <div className="flex items-center gap-8">
            <button onClick={onBack} className="tactile-button p-3 rounded-full bg-white dark:bg-stone-800 border border-stone-200 dark:border-stone-700 transition-all hover:scale-105 active:scale-95">
              <ArrowLeft size={18} className="text-stone-900 dark:text-white" />
            </button>
            <div className="h-10 w-px bg-stone-200/50 dark:bg-stone-700" />
            <div>
              <p className="font-mono text-[9px] font-bold text-stone-400 dark:text-stone-500 uppercase tracking-[0.5em] mb-1">Navigation Hub</p>
              <h1 className="font-serif font-bold text-2xl tracking-tight text-stone-900 dark:text-white italic">{title}</h1>
            </div>
          </div>
          <div className="w-14 h-14 bg-stone-900 dark:bg-white rounded-2xl flex items-center justify-center text-white dark:text-black shadow-2xl rotate-3">
            <FlaskConical size={24} strokeWidth={1.5} />
          </div>
        </div>
      </header>

      <main className="flex-grow w-full max-w-7xl px-6 pt-24 relative z-10">
        
        {/* Bento Grid Command Center */}
        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-6 auto-rows-fr">
          
          {/* Bento Header Strip */}
          <MotionDiv 
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="md:col-span-6 flex flex-col md:flex-row items-center justify-between p-8 rounded-[2rem] bg-stone-900 dark:bg-white/5 border border-white/10 mb-2 relative overflow-hidden"
          >
            <div className="relative z-10">
              <h2 className="text-white font-serif text-3xl md:text-4xl font-bold italic tracking-tight">Mission Briefing</h2>
              <p className="text-stone-400 dark:text-stone-500 font-mono text-[10px] uppercase tracking-[0.4em] mt-2">Select a unit to initialize protocol sequence</p>
            </div>
            <div className="mt-6 md:mt-0 flex items-center gap-6 relative z-10">
               <div className="flex flex-col items-end">
                  <span className="text-white text-xl font-bold">{overallProgress}%</span>
                  <span className="text-stone-500 text-[9px] font-black uppercase tracking-widest">Category Progress</span>
               </div>
               <div className="w-12 h-12 rounded-full bg-blue-500/20 border border-blue-500/30 flex items-center justify-center text-blue-500">
                  <Sparkles size={24} className="animate-pulse" />
               </div>
            </div>
            <div className="absolute right-0 top-0 w-64 h-64 bg-blue-500/10 blur-[80px] -mr-32 -mt-32"></div>
          </MotionDiv>

          {courses.map((course, idx) => {
            const progress = userProgress[course.id];
            const isCompleted = progress && progress.unlockedSection >= course.sectionsCount - 1;
            return (
              <BentoModuleTile 
                key={course.id}
                course={course}
                index={idx}
                isUnlocked={idx <= unlockedIndex}
                isCompleted={isCompleted}
                onClick={() => onSelectCourse(course.id)}
                categoryTitle={title}
              />
            )
          })}

          {/* Sequence Terminated Bento Tile */}
          <MotionDiv 
             initial={{ opacity: 0 }}
             whileInView={{ opacity: 1 }}
             className="md:col-span-6 flex flex-col items-center justify-center py-20 mt-12 rounded-[2.5rem] border border-dashed border-stone-200 dark:border-white/10"
          >
             <div className="w-20 h-20 bg-stone-50 dark:bg-white/5 rounded-full flex items-center justify-center text-stone-300 dark:text-stone-700 mb-6">
                <Hash size={32} strokeWidth={1} />
             </div>
             <p className="font-mono text-[10px] font-bold uppercase tracking-[0.8em] text-stone-400 dark:text-stone-600 translate-x-[0.4em]">End of Transmission</p>
          </MotionDiv>
        </div>
      </main>

      <footer className="mt-24 py-16 border-t border-stone-200/50 dark:border-white/5 w-full text-center relative z-10">
        <div className="inline-flex items-center gap-6 px-12 py-5 bg-white dark:bg-stone-900 border border-stone-200 dark:border-stone-800 rounded-full shadow-sm">
          <Hash size={16} className="text-blue-500" />
          <p className="font-mono text-[10px] font-bold text-stone-400 dark:text-stone-500 uppercase tracking-[0.4em]">Protocol // V.4.2.0-Alpha</p>
        </div>
      </footer>
    </div>
  );
};
