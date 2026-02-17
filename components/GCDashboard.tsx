/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { CourseData } from './Library';
import { SessionUser, getAvatarUrl } from './Auth';
import { GraduationCap, LogOut, ArrowUpDown, Search } from 'lucide-react';
import { CategoryType } from './KnowledgeTree';
import { db } from '../firebase';
import { collection, query, where, getDocs, doc, getDoc } from 'firebase/firestore';
import { getSchoolName } from '../schoolData';

// FIX: Cast motion components to any to bypass broken type definitions
const MotionDiv = motion.div as any;

type ModuleProgress = {
  unlockedSection: number;
};

type UserProgress = {
  [moduleId: string]: ModuleProgress;
};

interface GCDashboardProps {
  school: string;
  onLogout: () => void;
  allCourses: CourseData[];
}

const CATEGORIES: { id: CategoryType; title: string }[] = [
  { id: 'architecture-mindset', title: 'The Architecture of your Mindset' },
  { id: 'science-growth', title: 'The Science of Growth' },
  { id: 'learning-cheat-codes', title: 'The Science of Learning Effectively' },
  { id: 'subject-specific-science', title: 'Decoding the Subjects' },
  { id: 'exam-zone', title: 'Exam Strategy and Points Maximisation' },
];

type SortOption = 'name-asc' | 'name-desc' | 'progress-high' | 'progress-low';

const GCStudentCard: React.FC<{ user: SessionUser; userProgress: UserProgress; allCourses: CourseData[] }> = ({ user, userProgress, allCourses }) => {
  const calculateCategoryProgress = (category: CategoryType) => {
    const categoryCourses = allCourses.filter(c => c.category === category);
    if (categoryCourses.length === 0) return 0;

    const totalProgress = categoryCourses.reduce((sum, course) => {
      const progress = userProgress[course.id];
      if (progress && typeof progress.unlockedSection === 'number' && course.sectionsCount > 0) {
        const coursePercentage = Math.min(100, (progress.unlockedSection / course.sectionsCount) * 100);
        return sum + coursePercentage;
      }
      return sum;
    }, 0);

    return totalProgress / categoryCourses.length;
  };

  const totalProgressSum = allCourses.reduce((sum, course) => {
    const progress = userProgress[course.id];
    if (progress && typeof progress.unlockedSection === 'number' && course.sectionsCount > 0) {
      const coursePercentage = Math.min(100, (progress.unlockedSection / course.sectionsCount) * 100);
      return sum + coursePercentage;
    }
    return sum;
  }, 0);

  const overallProgress = allCourses.length > 0 ? totalProgressSum / allCourses.length : 0;

  return (
    <div className="bg-white dark:bg-zinc-900/50 border border-zinc-200/50 dark:border-white/10 rounded-2xl p-6 shadow-sm">
      <div className="flex items-center gap-4 border-b border-zinc-200/50 dark:border-white/10 pb-4 mb-4">
        <img src={getAvatarUrl(user.avatar)} alt="User Avatar" className="w-12 h-12 rounded-full bg-zinc-200" />
        <div>
          <p className="font-bold text-zinc-800 dark:text-white">{user.name}</p>
          <p className="text-xs text-zinc-500">Overall Progress: {overallProgress.toFixed(0)}%</p>
        </div>
      </div>
      <div className="space-y-3 max-h-64 overflow-y-auto pr-2">
        {CATEGORIES.map(category => {
          const categoryProgress = calculateCategoryProgress(category.id);
          return (
            <div key={category.id}>
              <div className="flex justify-between items-center">
                <p className="text-xs font-medium text-zinc-600 dark:text-zinc-400 truncate">{category.title}</p>
                <p className="text-xs font-bold text-zinc-500 dark:text-zinc-300">{categoryProgress.toFixed(0)}%</p>
              </div>
              <div className="w-full bg-zinc-200 dark:bg-zinc-700 rounded-full h-2 mt-1">
                <MotionDiv
                  className={`h-2 rounded-full ${categoryProgress >= 100 ? 'bg-emerald-500' : 'bg-blue-500'}`}
                  initial={{ width: 0 }}
                  animate={{ width: `${categoryProgress}%` }}
                  transition={{ duration: 0.5, ease: 'easeOut' }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export const GCDashboard: React.FC<GCDashboardProps> = ({ school, onLogout, allCourses }) => {
  const [studentData, setStudentData] = useState<{ user: SessionUser; progress: UserProgress }[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [sortBy, setSortBy] = useState<SortOption>('name-asc');
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      try {
        // Query only users from this school
        const usersCol = collection(db, 'users');
        const schoolQuery = query(usersCol, where('school', '==', school));
        const userSnapshot = await getDocs(schoolQuery);
        const users = userSnapshot.docs.map(d => ({ uid: d.id, ...d.data() })) as SessionUser[];

        // Filter out GC accounts — only show students
        const students = users.filter(u => u.role !== 'gc' && u.role !== 'admin');

        // Fetch progress for each student individually (GC rules only allow per-doc reads)
        const progressEntries = await Promise.all(
          students.map(async (user) => {
            try {
              const progressDoc = await getDoc(doc(db, 'progress', user.uid));
              return { uid: user.uid, progress: progressDoc.exists() ? (progressDoc.data() as UserProgress) : {} };
            } catch {
              return { uid: user.uid, progress: {} };
            }
          })
        );
        const allProgress = Object.fromEntries(progressEntries.map(e => [e.uid, e.progress]));

        const combinedData = students.map(user => ({
          user,
          progress: allProgress[user.uid] || {},
        }));

        setStudentData(combinedData);
      } catch (error) {
        console.error('Error fetching GC data:', error);
      }
      setIsLoading(false);
    };

    fetchData();
  }, [school]);

  const getOverallProgress = (userProgress: UserProgress) => {
    const totalProgressSum = allCourses.reduce((sum, course) => {
      const progress = userProgress[course.id];
      if (progress && typeof progress.unlockedSection === 'number' && course.sectionsCount > 0) {
        const coursePercentage = Math.min(100, (progress.unlockedSection / course.sectionsCount) * 100);
        return sum + coursePercentage;
      }
      return sum;
    }, 0);
    return allCourses.length > 0 ? totalProgressSum / allCourses.length : 0;
  };

  const filteredAndSorted = studentData
    .filter(d => d.user.name.toLowerCase().includes(searchQuery.toLowerCase()))
    .sort((a, b) => {
      switch (sortBy) {
        case 'name-asc': return a.user.name.localeCompare(b.user.name);
        case 'name-desc': return b.user.name.localeCompare(a.user.name);
        case 'progress-high': return getOverallProgress(b.progress) - getOverallProgress(a.progress);
        case 'progress-low': return getOverallProgress(a.progress) - getOverallProgress(b.progress);
        default: return 0;
      }
    });

  return (
    <div className="min-h-screen w-full p-8 pt-24">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-xl bg-[#CC785C]/10 flex items-center justify-center">
              <GraduationCap size={28} className="text-[#CC785C]" />
            </div>
            <div>
              <h1 className="font-serif text-3xl font-semibold text-zinc-900 dark:text-white">{getSchoolName(school)}</h1>
              <p className="text-zinc-500 dark:text-zinc-400">Guidance Counsellor Dashboard</p>
            </div>
          </div>
          <button
            onClick={onLogout}
            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-300 hover:bg-zinc-200 dark:hover:bg-zinc-700 transition-colors text-sm font-medium"
          >
            <LogOut size={16} />
            Log Out
          </button>
        </div>

        {/* Stats bar */}
        <div className="flex items-center gap-6 mb-6 pb-6 border-b border-zinc-200/50 dark:border-white/10">
          <div className="flex items-center gap-2">
            <span className="text-2xl font-bold text-zinc-900 dark:text-white">{studentData.length}</span>
            <span className="text-sm text-zinc-500 dark:text-zinc-400">students</span>
          </div>
        </div>

        {/* Controls */}
        <div className="flex flex-col sm:flex-row gap-3 mb-6">
          <div className="relative flex-1">
            <Search size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-zinc-400 dark:text-zinc-500" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search students..."
              className="w-full bg-white dark:bg-zinc-900/50 border border-zinc-200/50 dark:border-white/10 rounded-xl py-2.5 pl-10 pr-4 text-zinc-900 dark:text-white text-sm placeholder:text-zinc-400 dark:placeholder:text-zinc-500 focus:outline-none focus:border-[#CC785C]/60 focus:ring-1 focus:ring-[#CC785C]/30 transition-colors"
            />
          </div>
          <div className="relative">
            <ArrowUpDown size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-zinc-400 dark:text-zinc-500 pointer-events-none" />
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as SortOption)}
              className="appearance-none bg-white dark:bg-zinc-900/50 border border-zinc-200/50 dark:border-white/10 rounded-xl py-2.5 pl-10 pr-8 text-zinc-900 dark:text-white text-sm cursor-pointer focus:outline-none focus:border-[#CC785C]/60 focus:ring-1 focus:ring-[#CC785C]/30 transition-colors"
            >
              <option value="name-asc">Name A-Z</option>
              <option value="name-desc">Name Z-A</option>
              <option value="progress-high">Progress (Highest)</option>
              <option value="progress-low">Progress (Lowest)</option>
            </select>
          </div>
        </div>

        {isLoading ? (
          <div className="text-center py-16"><p className="text-zinc-500 dark:text-zinc-400">Loading student data...</p></div>
        ) : filteredAndSorted.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredAndSorted.map(data => (
              <GCStudentCard
                key={data.user.uid}
                user={data.user}
                userProgress={data.progress}
                allCourses={allCourses}
              />
            ))}
          </div>
        ) : studentData.length > 0 ? (
          <div className="text-center py-16 border border-dashed border-zinc-300 dark:border-zinc-700 rounded-2xl">
            <p className="text-zinc-500">No students match your search.</p>
          </div>
        ) : (
          <div className="text-center py-16 border border-dashed border-zinc-300 dark:border-zinc-700 rounded-2xl">
            <p className="text-zinc-500">No students have signed up for {getSchoolName(school)} yet.</p>
          </div>
        )}
      </div>
    </div>
  );
};
