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
import { ArrowRight, RotateCcw } from 'lucide-react';
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

  if (!visit) return null;
  // Older than three weeks reads as nagging, not helping.
  if (Date.now() - visit.at > 21 * 86400000) return null;

  let title = visit.label;
  let sub = visit.sub || '';
  let go: () => void;

  if (visit.kind === 'module') {
    const course = allCourses.find(c => c.id === visit.id);
    if (!course) return null; // e.g. subject dropped since
    const p = userProgress[course.id];
    const done = p ? Math.min(p.unlockedSection, course.sectionsCount) : 0;
    if (done >= course.sectionsCount) return null; // finished — nothing to resume
    title = course.title;
    sub = done > 0 ? `Section ${done + 1} of ${course.sectionsCount}` : 'Not started yet';
    go = () => onSelectModule(course.id);
  } else {
    if (!onOpenTool) return null;
    go = () => onOpenTool(visit.id);
  }

  return (
    <button
      onClick={go}
      className="w-full text-left rounded-2xl px-5 py-3.5 mb-4 flex items-center justify-between gap-3 bg-white dark:bg-zinc-900 border border-[#EDEBE8] dark:border-zinc-800 transition-all hover:shadow-md group"
      style={{ boxShadow: '0 1px 3px rgba(28,25,23,0.04)' }}
    >
      <div className="flex items-center gap-3 min-w-0">
        <div
          className="w-9 h-9 rounded-xl flex items-center justify-center shrink-0"
          style={{ backgroundColor: 'rgba(242,107,31,0.1)' }}
        >
          <RotateCcw size={16} style={{ color: COLORS.accent }} />
        </div>
        <div className="min-w-0">
          <p className="text-[10px] font-bold uppercase tracking-widest text-[#A8A29E] dark:text-zinc-500">
            Pick up where you left off
          </p>
          <p className="text-sm font-semibold text-[#1A1A1A] dark:text-white truncate">
            {title}
            {sub && <span className="font-normal text-[#78716C] dark:text-zinc-400"> · {sub}</span>}
          </p>
        </div>
      </div>
      <span
        className="flex items-center gap-1 text-xs font-bold px-4 py-2 rounded-lg text-white shrink-0 transition-transform duration-300 group-hover:translate-x-0.5"
        style={{ backgroundColor: COLORS.accent }}
      >
        Continue <ArrowRight size={12} />
      </span>
    </button>
  );
};

export default ResumeCard;
