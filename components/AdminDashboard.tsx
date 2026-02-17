/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/
import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { CourseData } from './Library';
import { SessionUser, getAvatarUrl } from './Auth';
import { GraduationCap, LogOut } from 'lucide-react';
import { CategoryType } from './KnowledgeTree';
import { db } from '../firebase';
import { collection, getDocs } from 'firebase/firestore';

// FIX: Cast motion components to any to bypass broken type definitions
const MotionDiv = motion.div as any;

type ModuleProgress = {
  unlockedSection: number;
};

type UserProgress = {
  [moduleId: string]: ModuleProgress;
};

type AllUserProgress = {
  [uid: string]: UserProgress;
};

interface AdminDashboardProps {
  allCourses: CourseData[];
  onLogout: () => void;
}

const CATEGORIES: { id: CategoryType; title: string }[] = [
    { id: 'architecture-mindset', title: 'The Architecture of your Mindset' },
    { id: 'science-growth', title: 'The Science of Growth' },
    { id: 'learning-cheat-codes', title: 'The Science of Learning Effectively' },
    { id: 'subject-specific-science', title: 'Decoding the Subjects' },
    { id: 'exam-zone', title: 'Exam Strategy and Points Maximisation' },
];

const StudentProgressCard: React.FC<{ user: SessionUser; userProgress: UserProgress; allCourses: CourseData[] }> = ({ user, userProgress, allCourses }) => {

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

export const AdminDashboard: React.FC<AdminDashboardProps> = ({ allCourses, onLogout }) => {
    const [studentData, setStudentData] = useState<{ user: SessionUser; progress: UserProgress }[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            setIsLoading(true);
            try {
                // Fetch all user profiles
                const usersCol = collection(db, "users");
                const userSnapshot = await getDocs(usersCol);
                const users = userSnapshot.docs.map(doc => ({ uid: doc.id, ...doc.data() })) as SessionUser[];

                // Fetch all progress data
                const progressCol = collection(db, "progress");
                const progressSnapshot = await getDocs(progressCol);
                const allProgress = progressSnapshot.docs.reduce((acc, doc) => {
                    acc[doc.id] = doc.data();
                    return acc;
                }, {} as AllUserProgress);

                // Combine data for each student (exclude admin and GC accounts)
                const combinedData = users
                    .filter(u => !u.isAdmin && (u as any).role !== 'gc' && (u as any).role !== 'admin')
                    .map(user => ({
                        user,
                        progress: allProgress[user.uid] || {}
                    }));

                setStudentData(combinedData);
            } catch (error) {
                console.error("Error fetching admin data:", error);
            }
            setIsLoading(false);
        };

        fetchData();
    }, []);

  return (
    <div className="min-h-screen w-full p-8 pt-24">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-4">
            <GraduationCap size={32} className="text-zinc-700 dark:text-zinc-300"/>
            <div>
                 <h1 className="font-serif text-3xl font-semibold text-zinc-900 dark:text-white">Admin Dashboard</h1>
                 <p className="text-zinc-500 dark:text-zinc-400">Student Progress Overview</p>
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

        {isLoading ? (
            <div className="text-center py-16"><p>Loading student data...</p></div>
        ) : studentData.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {studentData.map(data => (
                <StudentProgressCard
                    key={data.user.uid}
                    user={data.user}
                    userProgress={data.progress}
                    allCourses={allCourses}
                />
            ))}
            </div>
        ) : (
            <div className="text-center py-16 border border-dashed border-zinc-300 dark:border-zinc-700 rounded-2xl">
                <p className="text-zinc-500">No student accounts found or data could not be loaded.</p>
            </div>
        )}
      </div>
    </div>
  );
};
