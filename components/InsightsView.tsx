import React from 'react';
import { ArrowLeft, ArrowRight } from 'lucide-react';
import type { StreakData } from '../hooks/useStreak';
import type { StrategyMasteryMap } from '../types';
import { useInsights, type Insight } from '../hooks/useInsights';
import StarGuide from './ui/StarGuide';

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

export default function InsightsView({ uid, streak, strategyMastery, onBack, onAction }: InsightsViewProps) {
  const { insights, isLoaded } = useInsights(uid, streak, strategyMastery);
  return <main className="min-h-screen bg-white px-5 pb-36 pt-16 text-zinc-900 dark:bg-zinc-950 dark:text-white md:pt-24">
    <div className="mx-auto max-w-2xl">
      <button onClick={onBack} className="mb-7 inline-flex min-h-11 items-center gap-2 rounded-lg pr-4 text-base font-semibold"><ArrowLeft size={20} aria-hidden="true" /> Home</button>
      <header className="mb-8 flex items-center justify-between gap-4">
        <div><p className="text-xs font-bold uppercase tracking-[0.16em] text-[#B54D14] dark:text-orange-400">Your next step</p><h1 className="mt-2 font-serif text-4xl font-bold tracking-tight">Your Insights</h1><p className="mt-3 text-base leading-relaxed text-zinc-600 dark:text-zinc-300">What your study record is telling you.</p></div>
        <StarGuide size={72} className="shrink-0" />
      </header>
      {!isLoaded ? <p role="status" className="border-t border-zinc-200 py-8 dark:border-zinc-700">Reading your study record…</p> : insights.length === 0 ? <section className="rounded-2xl border border-zinc-300 p-6 dark:border-zinc-700">
        <h2 className="font-serif text-2xl font-semibold">Start with one session.</h2>
        <p className="mt-3 text-base leading-relaxed text-zinc-600 dark:text-zinc-300">As you record study sessions and reflections, this page will show patterns in your timing, subjects and confidence.</p>
        <button onClick={() => onAction('study')} className="mt-6 flex min-h-12 w-full items-center justify-between gap-3 rounded-xl bg-[#F26B1F] px-4 py-3 font-bold text-[#1A1A1A]">Plan a study session <ArrowRight size={20} aria-hidden="true" /></button>
      </section> : <div>
        {insights.map((insight, index) => {
          const next = nextAction(insight);
          return <article key={insight.id} className={index === 0 ? 'mb-7 rounded-2xl bg-[#1A1A1A] p-6 text-white' : 'border-t border-zinc-300 py-6 dark:border-zinc-700'}>
            <p className={`mb-3 text-xs font-bold uppercase tracking-widest ${index === 0 ? 'text-[#F26B1F]' : 'text-zinc-600 dark:text-zinc-400'}`}>{CATEGORY_LABELS[insight.category]}</p>
            <h2 className={`font-serif font-semibold leading-tight ${index === 0 ? 'text-3xl' : 'text-2xl'}`}>{insight.title}</h2>
            <p className={`mt-3 text-base leading-relaxed ${index === 0 ? 'text-zinc-200' : 'text-zinc-600 dark:text-zinc-300'}`}>{insight.description}</p>
            <button onClick={() => onAction(next.action)} className={`mt-4 flex min-h-11 items-center gap-3 text-left text-base font-semibold underline underline-offset-4 ${index === 0 ? 'text-white' : 'text-[#B54D14] dark:text-orange-400'}`}>{next.label}<ArrowRight size={18} aria-hidden="true" className="shrink-0" /></button>
          </article>;
        })}
        <p className="border-t border-zinc-300 pt-5 text-sm leading-relaxed text-zinc-500 dark:border-zinc-700 dark:text-zinc-400">Based on what you’ve recorded in NextStepUni. Study outside the app won’t appear here.</p>
      </div>}
    </div>
  </main>;
}
