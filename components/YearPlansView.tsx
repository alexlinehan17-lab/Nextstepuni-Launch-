/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * YearPlansView — the year-by-year curriculum, 1st through 6th.
 *
 * The look (r5-year-plans, agreed 26 Nov 2026): each year lies on the page
 * between thin rules with its drawn year number; the bars are ink; your
 * current year is the screen's one sheet with the one charcoal Continue.
 * The same language as LearningPathsView (plans-paths.css).
 */

import React, { useState } from 'react';
import { Check } from 'lucide-react';
import PageHeader from './ui/PageHeader';
import { Button, TextButton } from './ui/Button';
import { List, PaperSheet, Row } from './ui/List';
import './plans-paths.css';
import { type CourseData } from './Library';
import { YEAR_PLANS, type YearPlan } from '../yearPlans';
import { type YearGroup } from './subjectData';

type UserProgress = {
  [moduleId: string]: { unlockedSection: number };
};

interface YearPlansViewProps {
  allCourses: CourseData[];
  userProgress: UserProgress;
  onSelectModule: (moduleId: string) => void;
  onBack: () => void;
  /** LCA students see the two LCA year plans instead of the six LC/JC years. */
  isLca?: boolean;
  currentYearGroup?: YearGroup;
}

const CYCLE_EYEBROW: Record<YearPlan['cycle'], string> = {
  junior: 'Junior Cycle',
  ty: 'Transition Year',
  senior: 'Senior Cycle',
  lca: 'Leaving Cert Applied',
};

const YearPlansView: React.FC<YearPlansViewProps> = ({
  allCourses,
  userProgress,
  onSelectModule,
  onBack,
  isLca = false,
  currentYearGroup,
}) => {
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const plans = YEAR_PLANS.filter(p => (isLca ? p.cycle === 'lca' : p.cycle !== 'lca'));
  const currentPlanId = currentYearGroup === 'LCA1' ? 'lca-year-1'
    : currentYearGroup === 'LCA2' ? 'lca-year-2'
      : currentYearGroup === 'TY' ? 'year-4'
        : currentYearGroup && currentYearGroup !== 'graduated'
          ? `year-${Number.parseInt(currentYearGroup, 10)}`
          : null;

  const isModuleComplete = (moduleId: string) => {
    const course = allCourses.find(c => c.id === moduleId);
    if (!course) return false;
    const p = userProgress[moduleId];
    return p && p.unlockedSection >= course.sectionsCount;
  };

  const getFirstIncomplete = (plan: YearPlan): string | null => {
    for (const id of plan.moduleIds) {
      if (!isModuleComplete(id)) return id;
    }
    return null;
  };

  const getModuleTitle = (moduleId: string): string => {
    const course = allCourses.find(c => c.id === moduleId);
    return course?.title ?? moduleId;
  };

  return (
    <div className="pp-page min-h-screen">
      <div className="pp-bar"><div className="pp-width"><PageHeader onBack={onBack} eyebrow="Plan ahead" title="Year Plans" /></div></div>
      <div className="pp-width pp-body">
        <p className="t-sub pp-intro">
          A curated set of modules for every year of secondary school — in the order they teach best. Pick your
          year and work through it; subject-specific modules live in Decoding the Subjects.
        </p>

        <div className="pp-grid">
          {plans.map(plan => {
            const eyebrow = CYCLE_EYEBROW[plan.cycle];
            const completed = plan.moduleIds.filter(id => isModuleComplete(id)).length;
            const total = plan.moduleIds.length;
            const pct = total > 0 ? Math.round((completed / total) * 100) : 0;
            const isExpanded = expandedId === plan.id;
            const firstIncomplete = getFirstIncomplete(plan);
            const isComplete = total > 0 && !firstIncomplete;
            const isCurrent = plan.id === currentPlanId;
            const body = (
              <>
                <div className="pp-top">
                  <div className="pp-names">
                    <p className="t-label pp-label">{eyebrow}</p>
                    {isCurrent && <p className="t-label pp-live">Your current plan</p>}
                    <h2 className="pp-title">{plan.title}</h2>
                    <p className="t-sub">{plan.subtitle}</p>
                  </div>
                  <img src={`/assets/year-plans/${plan.year}.png`} alt="" aria-hidden draggable={false} className="pp-number" />
                </div>
                <p className="pp-desc">{plan.description}</p>
                <div className="pp-prog">
                  <span className="pp-bar-track" aria-hidden="true"><i style={{ width: `${pct}%` }} /></span>
                  <span className="t-meta">{completed} / {total} complete</span>
                </div>
                <div className="pp-acts">
                  {isComplete ? (
                    <span className="pp-done"><Check size={16} strokeWidth={2} aria-hidden="true" />Year complete</span>
                  ) : (
                    <Button kind={isCurrent ? 'main' : 'second'} arrow="forward" className="pp-go"
                      aria-label={`${completed > 0 ? 'Continue' : 'Start'} ${plan.title}`}
                      onClick={() => firstIncomplete && onSelectModule(firstIncomplete)}>
                      {completed > 0 ? 'Continue' : 'Start'}
                    </Button>
                  )}
                  <TextButton tone="quiet" arrow="menu" className="pp-toggle" aria-expanded={isExpanded}
                    aria-label={`${isExpanded ? 'Hide' : 'View'} modules in ${plan.title}`}
                    onClick={() => setExpandedId(isExpanded ? null : plan.id)}>
                    {isExpanded ? 'Hide modules' : `View modules (${total})`}
                  </TextButton>
                </div>
                {isExpanded && (
                  <List className="pp-modules" label={`Modules in ${plan.title}`}>
                    {plan.moduleIds.map((moduleId, idx) => {
                      const done = isModuleComplete(moduleId);
                      return <Row key={moduleId} className={done ? 'pp-module pp-module--done' : 'pp-module'}
                        icon={done ? <Check size={18} strokeWidth={2} /> : <span className="pp-module-n">{idx + 1}</span>}
                        title={getModuleTitle(moduleId)} meta={done ? 'Read' : undefined} onPress={() => onSelectModule(moduleId)} />;
                    })}
                  </List>
                )}
              </>
            );
            return isCurrent
              ? <PaperSheet key={plan.id} className="pp-item pp-item--current" label={plan.title}>{body}</PaperSheet>
              : <section key={plan.id} className="pp-item" aria-label={plan.title}>{body}</section>;
          })}
        </div>
      </div>
    </div>
  );
};

export default YearPlansView;
