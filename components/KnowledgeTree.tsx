/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Sprout, Zap, Rocket, Target, FlaskConical,
  Layout, ArrowRight, Sparkles, Beaker
} from 'lucide-react';
import { useTranslation } from 'react-i18next';
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
      <div className="absolute flex items-baseline justify-center leading-none">
        <span className="text-[13px] font-semibold text-zinc-900 dark:text-white">
          {Math.round(progress)}
        </span>
        <span className="text-[8px] font-semibold text-zinc-400 dark:text-white/30 ml-px">%</span>
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
  const { t } = useTranslation();
  return (
    <MotionDiv
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay, ease: [0.16, 1, 0.3, 1] }}
      onClick={onClick}
      className={`group relative overflow-hidden rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 cursor-pointer transition-all duration-300 hover:border-zinc-300 dark:hover:border-zinc-700 hover:shadow-md ${className}`}
    >
      <div className="p-8 h-full flex flex-col justify-between">
        <div>
          <div className="flex items-center justify-between mb-8">
            <div
              className="w-12 h-12 rounded-xl flex items-center justify-center"
              style={{ color: accentHex, backgroundColor: accentHex + '12' }}
            >
              <Icon size={24} strokeWidth={1.5} />
            </div>

            <div className="opacity-0 group-hover:opacity-100 transition-opacity duration-300">
               <ArrowRight size={18} className="text-zinc-400 dark:text-zinc-500" />
            </div>
          </div>

          <p className="text-[11px] font-semibold uppercase tracking-[0.15em] text-zinc-400 dark:text-zinc-500 mb-2">
            {subtitle}</p>
          <h3 className="font-serif text-2xl md:text-3xl text-zinc-900 dark:text-white leading-tight font-semibold tracking-tight">
            {title}
          </h3>
        </div>

        <div className="mt-8 flex items-center justify-between gap-6 pt-6 border-t border-zinc-100 dark:border-zinc-800">
            <div className="flex flex-col">
              <span className="text-[10px] font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">{t('tree.progress')}</span>
            </div>
            <ActivityRing progress={progress} color={accentHex} />
        </div>
      </div>
    </MotionDiv>
  );
};

export const KnowledgeTree: React.FC<KnowledgeTreeProps> = ({ onSelectCategory, onGoToInnovationZone, allCourses, onSelectModule, categoryTitles, userProgress }) => {
  const { t } = useTranslation();
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
    <div className="min-h-screen bg-zinc-50 dark:bg-zinc-950 overflow-x-hidden relative flex flex-col items-center pt-16 md:pt-32 pb-32 transition-colors duration-500 selection:bg-[#CC785C]/20">

      <div className="w-full max-w-7xl px-6">
        <header className="text-center mb-20">
          <div className="w-12 h-1 bg-[#CC785C] rounded-full mx-auto mb-6" />
          <h1 className="font-serif text-5xl md:text-7xl text-zinc-900 dark:text-white tracking-tight leading-none font-semibold">
            {t('tree.learningLab')}
          </h1>
          <p className="max-w-xl mx-auto mt-5 text-zinc-500 dark:text-zinc-400 leading-relaxed">
            {t('tree.subtitle')}
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
            <h2 className="text-center font-serif text-3xl font-semibold mb-2 text-zinc-800 dark:text-white">{t('tree.findModules')}</h2>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8 max-w-md mx-auto">{t('tree.findModulesDesc')}</p>
            <div className="flex flex-wrap justify-center gap-2 max-w-3xl mx-auto mb-12">
                {allTags.map(tag => (
                    <button 
                        key={tag}
                        onClick={() => handleTagClick(tag)}
                        className={`px-3.5 py-1.5 text-xs font-medium rounded-lg border transition-all duration-200 ${selectedTags.includes(tag) ? 'bg-[#CC785C] text-white border-[#CC785C]' : 'bg-white dark:bg-zinc-900 border-zinc-200 dark:border-zinc-800 text-zinc-600 dark:text-zinc-400 hover:border-zinc-300 dark:hover:border-zinc-700'}`}
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
