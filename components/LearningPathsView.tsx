/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * LearningPathsView — editorial library of curated module paths.
 *
 * The look (r5-learning-paths, agreed 26 Nov 2026): each path keeps its
 * drawing and lies on the page between thin rules; one colour (ink) for every
 * bar; Continue is a real button, and the path recommended next is the
 * screen's one sheet with the one charcoal Continue (plans-paths.css).
 */

import React, { useMemo, useState } from 'react';
import { Check } from 'lucide-react';
import PageHeader from './ui/PageHeader';
import { Button, TextButton } from './ui/Button';
import { List, PaperSheet, Row } from './ui/List';
import './plans-paths.css';
import { type CourseData } from './Library';
import { LEARNING_PATHS, type LearningPath } from '../learningPaths';
import { availableLearningPaths } from '../utils/courseVisibility';
import type { CurriculumLevel } from '../utils/authUtils';

type UserProgress = {
  [moduleId: string]: { unlockedSection: number };
};

interface LearningPathsViewProps {
  allCourses: CourseData[];
  userProgress: UserProgress;
  onSelectModule: (moduleId: string) => void;
  onBack: () => void;
  curriculumLevel?: CurriculumLevel;
}

// Editorial metadata layered on top of LEARNING_PATHS — eyebrow label and
// hand-drawn icon path. Every bar is ink; the bright accentHex from
// learningPaths.ts is intentionally not used on this surface.
//
// `iconScale` compensates for per-PNG internal padding so all four icons
// read at roughly equal visual weight. exam-prep's content sits in a
// shorter portion of its canvas (wide horizontal layout), so it gets
// scaled up; the others fill their canvas already.
const PATH_META: Record<string, { eyebrow: string; iconPath: string; iconScale: number }> = {
  'getting-started':      { eyebrow: 'Foundation Path', iconPath: '/assets/learning-paths/getting-started.png', iconScale: 1.0 },
  'exam-prep-sprint':     { eyebrow: 'Exam Path',       iconPath: '/assets/learning-paths/exam-prep.png',     iconScale: 1.35 },
  'build-your-mindset':   { eyebrow: 'Mindset Path',    iconPath: '/assets/learning-paths/mindset.png',       iconScale: 1.0 },
  'master-your-learning': { eyebrow: 'Learning Path',   iconPath: '/assets/learning-paths/master-learning.png', iconScale: 1.0 },
};

const LearningPathsView: React.FC<LearningPathsViewProps> = ({
  allCourses,
  userProgress,
  onSelectModule,
  onBack,
  curriculumLevel,
}) => {
  const [expandedPathId, setExpandedPathId] = useState<string | null>(null);
  const paths = useMemo(() => availableLearningPaths(LEARNING_PATHS, allCourses, curriculumLevel), [allCourses, curriculumLevel]);

  const isModuleComplete = (moduleId: string) => {
    const course = allCourses.find(c => c.id === moduleId);
    if (!course) return false;
    const p = userProgress[moduleId];
    return p && p.unlockedSection >= course.sectionsCount;
  };

  const getFirstIncomplete = (path: LearningPath): string | null => {
    for (const id of path.moduleIds) {
      if (!isModuleComplete(id)) return id;
    }
    return null;
  };

  const getModuleTitle = (moduleId: string): string => {
    const course = allCourses.find(c => c.id === moduleId);
    return course?.title ?? moduleId;
  };

  const recommendedPathId = useMemo(() => {
    const unfinished = paths.filter(path => getFirstIncomplete(path));
    if (unfinished.length === 0) return null;
    return unfinished
      .map(path => {
        const completed = path.moduleIds.filter(id => isModuleComplete(id)).length;
        const hasActiveModule = path.moduleIds.some(id => {
          const course = allCourses.find(candidate => candidate.id === id);
          const progress = userProgress[id];
          return Boolean(course && progress && progress.unlockedSection > 0 && progress.unlockedSection < course.sectionsCount);
        });
        return { id: path.id, score: (hasActiveModule ? 100 : 0) + (completed / Math.max(1, path.moduleIds.length)) };
      })
      .sort((a, b) => b.score - a.score)[0]?.id ?? null;
  }, [allCourses, userProgress, paths]);

  return (
    <div className="product-shell learning-paths-shell pp-page min-h-screen">
      <div className="pp-bar"><div className="pp-width"><PageHeader onBack={onBack} eyebrow="Guided learning" title="Learning Paths" /></div></div>
      <div className="pp-width pp-body">
        <div className="pp-grid pp-grid--paths">
          {paths.map(path => {
            const meta = PATH_META[path.id] ?? { eyebrow: 'Path', iconPath: '/assets/worlds/learn-book.png', iconScale: 1.0 };
            const completed = path.moduleIds.filter(id => isModuleComplete(id)).length;
            const total = path.moduleIds.length;
            const pct = total > 0 ? Math.round((completed / total) * 100) : 0;
            const isExpanded = expandedPathId === path.id;
            const firstIncomplete = getFirstIncomplete(path);
            const isComplete = !firstIncomplete;
            const isRecommended = recommendedPathId === path.id;
            const body = (
              <>
                <span className="pp-art" aria-hidden="true">
                  <img src={meta.iconPath} alt="" draggable={false} className="pp-art-inv" style={{ transform: `scale(${meta.iconScale})` }} />
                </span>
                <div className="pp-names">
                  <p className="t-label pp-label">{meta.eyebrow}{isRecommended ? <> · <span className="pp-live">Recommended next</span></> : ''}</p>
                  <h2 className="pp-title">{path.title}</h2>
                  <p className="t-sub">{total} modules available to you</p>
                </div>
                <p className="pp-desc">{path.description}</p>
                <div className="pp-prog">
                  <span className="pp-bar-track" aria-hidden="true"><i style={{ width: `${pct}%` }} /></span>
                  <span className="t-meta">{completed} / {total} complete</span>
                </div>
                <div className="pp-acts">
                  {isComplete ? (
                    <span className="pp-done"><Check size={16} strokeWidth={2} aria-hidden="true" />Path complete</span>
                  ) : (
                    <Button kind={isRecommended ? 'main' : 'second'} arrow="forward" className="pp-go"
                      aria-label={`${completed > 0 ? 'Continue' : 'Start'} ${path.title}`}
                      onClick={() => firstIncomplete && onSelectModule(firstIncomplete)}>
                      {completed > 0 ? 'Continue' : 'Start'}
                    </Button>
                  )}
                  <TextButton tone="quiet" arrow="menu" className="pp-toggle" aria-expanded={isExpanded}
                    aria-label={`${isExpanded ? 'Hide' : 'View'} modules in ${path.title}`}
                    onClick={() => setExpandedPathId(isExpanded ? null : path.id)}>
                    {isExpanded ? 'Hide modules' : 'View modules'}
                  </TextButton>
                </div>
                {isExpanded && (
                  <List className="pp-modules" label={`Modules in ${path.title}`}>
                    {path.moduleIds.map((moduleId, idx) => {
                      const done = isModuleComplete(moduleId);
                      return <Row key={moduleId} className={done ? 'pp-module pp-module--done' : 'pp-module'}
                        icon={done ? <Check size={18} strokeWidth={2} /> : <span className="pp-module-n">{idx + 1}</span>}
                        title={getModuleTitle(moduleId)} meta={done ? 'Read' : undefined} onPress={() => onSelectModule(moduleId)} />;
                    })}
                  </List>
                )}
              </>
            );
            return isRecommended
              ? <PaperSheet key={path.id} className="pp-item pp-item--current" label={path.title}>{body}</PaperSheet>
              : <section key={path.id} className="pp-item" aria-label={path.title}>{body}</section>;
          })}
        </div>
      </div>
    </div>
  );
};

export default LearningPathsView;
