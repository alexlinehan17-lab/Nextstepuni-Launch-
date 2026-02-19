

/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React from 'react';
import { motion } from 'framer-motion';
import {
  ArrowLeft, CheckCircle2,
  ChevronRight, Lock, Sparkles, BookOpen,
  Zap, Brain, Target, Shield, Compass, Star, Hash
} from 'lucide-react';
import { CategoryType } from './KnowledgeTree';
import { NorthStar } from '../types';
import { type StudentSubjectProfile } from './subjectData';
import NorthStarCallout from './NorthStarCallout';

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
  pillBgColor: string;
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
  northStar?: NorthStar | null;
  studentProfile?: StudentSubjectProfile | null;
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
  
  const pillBgColor = course.pillBgColor;


  return (
    <MotionDiv
      initial={{ opacity: 0, scale: 0.9, y: 20 }}
      whileInView={{ opacity: 1, scale: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.6, delay: index * 0.05, ease: [0.16, 1, 0.3, 1] }}
      whileHover={isUnlocked ? { scale: 1.01 } : {}}
      className={`group relative overflow-hidden rounded-xl transition-all duration-300 ${getSpanClass(index)}
        ${isUnlocked ? 'cursor-pointer hover:shadow-md' : 'cursor-not-allowed'}
      `}
      onClick={isUnlocked ? onClick : undefined}
    >
      {/* Category Pill */}
      <div className={`absolute top-6 left-6 z-20 px-3 py-1 rounded-full ${pillBgColor} border border-black/10 dark:border-white/10`}>
        <p className={`text-[9px] font-semibold uppercase tracking-wider text-white`}>{categoryTitle}</p>
      </div>

      {/* Clean Surface */}
      <div className="h-full w-full bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 p-8 pt-16 flex flex-col justify-between relative z-10 overflow-hidden">
        <div>
          <div className="flex items-center justify-between mb-8">
            <MotionDiv 
              className={`w-14 h-14 rounded-2xl flex items-center justify-center transition-all duration-500 shadow-sm 
                ${isCompleted ? 'bg-emerald-500 text-white' : isUnlocked ? 'bg-zinc-900 dark:bg-white text-white dark:text-zinc-900' : 'bg-zinc-200 dark:bg-zinc-800 text-zinc-400'}`}
              whileHover={isUnlocked ? { x: 5, y: -2 } : {}}
            >
              {isCompleted ? <CheckCircle2 size={28} /> : !isUnlocked ? <Lock size={24} /> : <Icon size={28} strokeWidth={1.5} />}
            </MotionDiv>
            
            <div className="flex flex-col items-end">
              <span className="font-mono text-[9px] font-semibold uppercase tracking-wider text-zinc-400 dark:text-zinc-500">Unit {index + 1}</span>
              {isCompleted && <span className="text-[8px] font-bold text-emerald-500 uppercase tracking-widest mt-1">Complete</span>}
            </div>
          </div>

          <h3 className="font-serif text-2xl md:text-3xl text-zinc-900 dark:text-white mb-4 leading-tight font-semibold tracking-tight">
            {course.title}
          </h3>
          
          <p className="text-zinc-500 dark:text-zinc-400 text-sm leading-relaxed font-medium line-clamp-3 mb-8">
            {course.description}
          </p>
        </div>

        <div className="flex items-center justify-between mt-auto pt-6 border-t border-zinc-200/30 dark:border-white/5">
          <div className="flex gap-2">
            {course.tags.slice(0, 2).map(tag => (
              <span key={tag} className="px-2.5 py-1 rounded-full bg-zinc-100 dark:bg-white/5 text-zinc-400 dark:text-zinc-500 text-[9px] font-bold uppercase tracking-wider">
                {tag}
              </span>
            ))}
          </div>
          {isUnlocked && (
            <MotionDiv 
              className="text-zinc-900 dark:text-white"
              whileHover={{ x: 5 }}
            >
              <ChevronRight size={20} />
            </MotionDiv>
          )}
        </div>

        {!isUnlocked && (
          <div className="absolute inset-0 bg-zinc-50/80 dark:bg-zinc-950/80 flex items-center justify-center z-20">
            <div className="bg-white dark:bg-zinc-900 px-4 py-2 rounded-lg border border-zinc-200 dark:border-zinc-800 flex items-center gap-2">
               <Lock size={12} className="text-zinc-400" />
               <span className="text-[10px] font-semibold uppercase tracking-wider text-zinc-400">Locked</span>
            </div>
          </div>
        )}
      </div>
    </MotionDiv>
  );
};

export const Library: React.FC<LibraryProps> = ({ title, courses, onSelectCourse, onBack, userProgress, northStar, studentProfile }) => {
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
    <div className="min-h-screen bg-zinc-50 dark:bg-zinc-950 transition-colors duration-500 overflow-x-hidden relative flex flex-col items-center pt-24 md:pt-32 pb-48">

      <header className="fixed top-0 left-0 right-0 z-[60] bg-zinc-50 dark:bg-zinc-950 border-b border-zinc-200 dark:border-zinc-800 px-4 py-4 md:px-10 md:py-6">
        <div className="container mx-auto flex items-center justify-between">
          <div className="flex items-center gap-4 md:gap-8">
            <button onClick={onBack} className="p-2.5 rounded-lg bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 transition-colors hover:bg-zinc-100 dark:hover:bg-zinc-800">
              <ArrowLeft size={18} className="text-zinc-900 dark:text-white" />
            </button>
            <div className="hidden md:block h-10 w-px bg-zinc-200 dark:bg-zinc-800" />
            <div>
              <p className="font-mono text-[9px] font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-[0.25em] mb-1">Module</p>
              <h1 className="font-serif font-semibold text-lg md:text-2xl tracking-tight text-zinc-900 dark:text-white truncate">{title}</h1>
            </div>
          </div>
        </div>
      </header>

      <main className="flex-grow w-full max-w-7xl px-6 pt-4 md:pt-24 relative z-10">

        {/* North Star Callout */}
        {northStar && (
          <div className="mb-4">
            <NorthStarCallout northStar={northStar} variant="full" />
          </div>
        )}

        {/* Bento Grid Command Center */}
        {/* Bento Header Strip — outside grid so auto-rows-fr doesn't stretch it */}
        <MotionDiv
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex flex-row items-center justify-between px-5 py-4 md:p-8 rounded-xl bg-zinc-900 dark:bg-zinc-900 border border-zinc-800 mb-4 md:mb-6"
        >
            <div>
              <h2 className="text-white font-serif text-lg md:text-4xl font-semibold tracking-tight">Overview</h2>
              <p className="hidden md:block text-zinc-400 text-[11px] uppercase tracking-[0.15em] mt-2">Choose a unit to get started</p>
            </div>
            <div className="flex items-center gap-3 md:gap-6">
               <div className="flex flex-col items-end">
                  <span className="text-white text-lg md:text-xl font-bold">{overallProgress}%</span>
                  <span className="text-zinc-500 text-[10px] font-semibold uppercase tracking-wider">Progress</span>
               </div>
               <div className="w-8 h-8 md:w-10 md:h-10 rounded-lg bg-[#CC785C]/15 flex items-center justify-center text-[#CC785C]">
                  <Sparkles size={16} className="md:hidden" /><Sparkles size={20} className="hidden md:block" />
               </div>
            </div>
        </MotionDiv>

        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-6 auto-rows-fr">
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
          <div className="md:col-span-6 flex flex-col items-center justify-center py-16 mt-8 border-t border-zinc-200 dark:border-zinc-800">
             <p className="text-[11px] font-semibold uppercase tracking-[0.2em] text-zinc-400 dark:text-zinc-600">End of Module</p>
          </div>
        </div>
      </main>

      <footer className="mt-16 py-12 border-t border-zinc-200 dark:border-zinc-800 w-full text-center">
        <div className="inline-flex items-center gap-3">
          <div className="w-4 h-1 bg-[#CC785C] rounded-full" />
          <p className="text-[11px] font-semibold text-zinc-400 dark:text-zinc-500 uppercase tracking-[0.15em]">NextStepUni Learning Lab</p>
        </div>
      </footer>
    </div>
  );
};
