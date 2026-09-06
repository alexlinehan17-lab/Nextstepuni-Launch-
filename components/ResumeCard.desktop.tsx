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
import { ArrowRight } from 'lucide-react';
import { getLastVisit } from './lastVisited';
import { type CourseData } from './Library';

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
  let frac: number | null = null;

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
        frac = done > 0 ? done / course.sectionsCount : null;
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

  return (
    <button
      onClick={go}
      className="group mb-4 flex w-full items-center justify-between gap-5 rounded-2xl border-[1.5px] border-[#383838] bg-white px-5 py-4 text-left transition-transform hover:-translate-y-0.5 dark:border-zinc-700 dark:bg-zinc-900"
    >
      <div className="min-w-0 flex-1">
        <p className="text-[10px] font-bold uppercase tracking-[0.16em] text-[#A8A29E] dark:text-zinc-500">
          {isResume ? 'Jump back in' : 'Start here'}
        </p>
        <p className="mt-1 truncate font-serif text-[16px] font-bold leading-snug text-[#1A1A1A] dark:text-white">{title}</p>
        {sub && <p className="mt-0.5 text-xs text-[#78716C] dark:text-zinc-400">{sub}</p>}
        {frac !== null && (
          <div className="mt-2.5 h-[3px] max-w-[320px] overflow-hidden rounded-full bg-[#ECE8E3] dark:bg-zinc-700">
            <div className="h-full rounded-full" style={{ width: `${Math.round(frac * 100)}%`, backgroundColor: 'rgba(242,107,31,0.62)' }} />
          </div>
        )}
      </div>
      <span className="flex shrink-0 items-center gap-1 text-[13px] font-bold text-[#F26B1F] transition-transform group-hover:translate-x-0.5">
        {isResume ? 'Continue' : 'Start'} <ArrowRight size={13} strokeWidth={2.4} />
      </span>
    </button>
  );
};

export default ResumeCard;
