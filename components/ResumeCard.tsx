/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * "Pick up where you left off" — one card at the top of the home page that
 * deep-links straight back into the last module or tool this account
 * opened (fed by components/lastVisited.ts). Styled in the home page's
 * white/cream register, not the module design system.
 */

import React, { useMemo } from 'react';
import { ArrowRight, BookOpen, RotateCcw } from 'lucide-react';
import { getLastVisit } from './lastVisited';
import { type CourseData } from './Library';
import { COLORS } from '../design/tokens';

interface Props {
  uid?: string;
  allCourses: CourseData[];
  userProgress: { [moduleId: string]: { unlockedSection: number } };
  onSelectModule: (moduleId: string) => void;
  onOpenTool?: (toolId: string) => void;
}

const ResumeCard: React.FC<Props> = ({ uid, allCourses, userProgress, onSelectModule, onOpenTool }) => {
  const visit = useMemo(() => getLastVisit(uid), [uid]);
  const fallbackCourse = allCourses.find(course => {
    const progress = userProgress[course.id];
    return !progress || progress.unlockedSection < course.sectionsCount;
  });

  let title = '';
  let sub = '';
  let go: (() => void) | null = null;
  let isResume = false;

  // Older than three weeks reads as nagging, so a stale visit becomes a calm
  // first-step suggestion instead of making this useful home slot disappear.
  if (visit && Date.now() - visit.at <= 21 * 86400000) {
    if (visit.kind === 'module') {
      const course = allCourses.find(candidate => candidate.id === visit.id);
      const progress = course ? userProgress[course.id] : undefined;
      const done = course && progress ? Math.min(progress.unlockedSection, course.sectionsCount) : 0;
      if (course && done < course.sectionsCount) {
        title = course.title;
        sub = done > 0 ? `Section ${done + 1} of ${course.sectionsCount}` : `${course.sectionsCount} short sections`;
        go = () => onSelectModule(course.id);
        isResume = done > 0;
      }
    } else if (onOpenTool) {
      title = visit.label;
      sub = visit.sub || 'Return to this tool';
      go = () => onOpenTool(visit.id);
      isResume = true;
    }
  }

  if (!go && fallbackCourse) {
    title = fallbackCourse.title;
    sub = `${fallbackCourse.sectionsCount} short sections`;
    go = () => onSelectModule(fallbackCourse.id);
  }
  if (!go) return null;

  const Icon = isResume ? RotateCcw : BookOpen;

  return (
    <button
      onClick={go}
      className="group mb-4 flex w-full flex-col items-stretch justify-between gap-4 rounded-2xl border-[1.5px] border-[#383838] bg-white px-5 py-4 text-left transition-transform hover:-translate-y-0.5 dark:border-zinc-700 dark:bg-zinc-900 sm:flex-row sm:items-center"
    >
      <div className="flex items-center gap-3 min-w-0">
        <div
          className="w-9 h-9 rounded-xl flex items-center justify-center shrink-0"
          style={{ backgroundColor: 'rgba(242,107,31,0.1)' }}
        >
          <Icon size={16} style={{ color: COLORS.accent }} />
        </div>
        <div className="min-w-0">
          <p className="text-[10px] font-bold uppercase tracking-widest text-[#A8A29E] dark:text-zinc-500">
            {isResume ? 'Pick up where you left off' : 'Start here'}
          </p>
          <p className="line-clamp-2 text-sm font-semibold leading-snug text-[#1A1A1A] dark:text-white">{title}</p>
          {sub && <p className="mt-0.5 text-xs text-[#78716C] dark:text-zinc-400">{sub}</p>}
        </div>
      </div>
      <span
        className="flex items-center gap-1.5 text-xs font-bold px-4 py-2.5 rounded-lg text-white shrink-0 border-2 border-[#1A1A1A] bg-[#F26B1F] shadow-[3px_3px_0_0_#1A1A1A] transition-transform group-active:translate-x-[3px] group-active:translate-y-[3px] group-active:shadow-none"
      >
        {isResume ? 'Continue' : 'Start'} <ArrowRight size={12} />
      </span>
    </button>
  );
};

export default ResumeCard;
