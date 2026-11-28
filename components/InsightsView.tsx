import React from 'react';
import type { StreakData } from '../hooks/useStreak';
import type { StrategyMasteryMap } from '../types';
import { useInsights, type Insight } from '../hooks/useInsights';
import { useMobileAppDesign } from '../hooks/useMobileAppDesign';
import PageHeader from './ui/PageHeader';
import { TopBar } from './ui/Bars';
import { Button, TextButton } from './ui/Button';
import { PaperSheet } from './ui/List';
import { useScreenLeave } from './navigation/useScreenLeave';
import StarGuide from './ui/StarGuide';
import './insights.css';

export type InsightAction = 'study' | 'planner' | 'progress';
interface InsightsViewProps {
  uid: string;
  streak: StreakData;
  strategyMastery: StrategyMasteryMap;
  onBack: () => void;
  onAction: (action: InsightAction) => void;
}
const CATEGORY_LABELS = { momentum: 'Your study record', pattern: 'A pattern to consider', strategy: 'Your approach', streak: 'Showing up' };
function nextAction(insight: Insight): { action: InsightAction; label: string } {
  if (insight.category === 'strategy' || insight.category === 'streak' || insight.id.startsWith('subject-gap-')) return { action: 'study', label: 'Plan a study session' };
  if (insight.category === 'pattern') return { action: 'planner', label: 'Review your timetable' };
  return { action: 'progress', label: 'See your study record' };
}

/** Insights (r5-insights, agreed "for now" 26 Nov 2026): the frame's bar with
 *  one Back; the first insight is the screen's one sheet with the one charcoal
 *  button; the others lie on the page between thin rules, each next step in
 *  ink words with an arrow. Each device keeps its own opening words. */
export default function InsightsView({ uid, streak, strategyMastery, onBack, onAction }: InsightsViewProps) {
  const mobileAppDesign = useMobileAppDesign();
  const leave = useScreenLeave(onBack);
  const { insights, isLoaded } = useInsights(uid, streak, strategyMastery);
  return <main className="ins-page min-h-screen">
    {mobileAppDesign
      ? <div className="ins-bar"><PageHeader onBack={onBack} title="Your Insights" eyebrow="What your record says" compact /></div>
      : <div className="ins-bar"><div className="ins-width"><TopBar ruled leave={leave} /></div></div>}
    <div className="ins-width ins-body">
      {mobileAppDesign ? <p className="t-sub ins-intro">A pattern. A possibility. A next step.</p> : (
        <header className="ins-open">
          <div className="ins-open-words">
            <p className="t-label ins-label">Your next step</p>
            <h1 className="t-title">Your Insights</h1>
            <p className="t-sub">What your study record is telling you.</p>
          </div>
          <StarGuide size={80} className="ins-guide" />
        </header>
      )}
      {!isLoaded ? <p role="status" className="ins-status">Reading your study record…</p> : insights.length === 0 ? <section className="ins-empty" aria-labelledby="ins-empty-title">
        <h2 id="ins-empty-title" className="t-heading">Start with one session.</h2>
        <p className="t-sub">As you record study sessions and reflections, this page will show patterns in your timing, subjects and confidence.</p>
        <Button kind="main" block={mobileAppDesign} arrow="forward" className="ins-go" onClick={() => onAction('study')}>Plan a study session</Button>
      </section> : <div className="ins-list">
        {insights.map((insight, index) => {
          const next = nextAction(insight);
          if (index === 0) {
            return <PaperSheet key={insight.id} className="ins-lead" label={insight.title}>
              <p className="t-label ins-live">{CATEGORY_LABELS[insight.category]}</p>
              <h2 className="t-title">{insight.title}</h2>
              <p className="t-sub">{insight.description}</p>
              <Button kind="main" block={mobileAppDesign} arrow="forward" className="ins-go" onClick={() => onAction(next.action)}>{next.label}</Button>
            </PaperSheet>;
          }
          return <article key={insight.id} className="ins-item">
            <p className="t-label ins-label">{CATEGORY_LABELS[insight.category]}</p>
            <h2 className="t-heading">{insight.title}</h2>
            <p className="t-sub">{insight.description}</p>
            <TextButton arrow="forward" onClick={() => onAction(next.action)}>{next.label}</TextButton>
          </article>;
        })}
        <p className="t-meta ins-source">Based on what you’ve recorded in NextStepUni. Study outside the app won’t appear here.</p>
      </div>}
    </div>
  </main>;
}
