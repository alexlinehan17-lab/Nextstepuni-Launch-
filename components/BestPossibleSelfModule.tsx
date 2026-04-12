/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { } from 'react';
import { motion } from 'framer-motion';
import {
  MapPin, BatteryWarning, Filter, Zap, ClipboardCheck
} from 'lucide-react';
import { type ModuleProgress } from '../types';
import { blueTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment, PersonalStory } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';
import { useModuleResponses } from '../hooks/useModuleResponses';
import { useEssentialsMode } from '../hooks/useEssentialsMode';
import { useNorthStar } from '../hooks/useNorthStar';
import NorthStarCallout from './NorthStarCallout';
import { COMPACT_CALLOUT_PLACEMENTS } from '../northStarData';

const theme = blueTheme;

// --- INTERACTIVE COMPONENTS ---

const WOOPPlanner = ({ responses, saveResponse }: { responses: Record<string, any>; saveResponse: (key: string, value: any) => void }) => {
    const wish = responses['woopWish'] || '';
    const outcome = responses['woopOutcome'] || '';
    const obstacle = responses['woopObstacle'] || '';
    const plan = responses['woopPlan'] || '';
    const isComplete = wish.trim() && outcome.trim() && obstacle.trim() && plan.trim();

    return(
        <div className="my-10 max-w-xl mx-auto bg-white dark:bg-zinc-900 rounded-2xl p-8 md:p-10" style={{ border: '2.5px solid #1C1917', boxShadow: '4px 4px 0px 0px #1C1917' }}>
            <h4 className="font-serif text-2xl md:text-3xl font-medium text-zinc-900 dark:text-white text-center mb-8">Your WOOP Blueprint</h4>
            <div className="space-y-7">
                {/* Wish */}
                <div>
                    <div className="flex items-center gap-2.5 mb-2">
                        <div className="w-8 h-8 flex items-center justify-center shrink-0 font-serif font-medium text-base" style={{ backgroundColor: '#FCD34D', border: '2px solid #D97706', borderRadius: 10, boxShadow: '2px 2px 0px 0px #D97706', color: '#78350F' }}>W</div>
                        <span className="text-[13px] font-medium text-zinc-900 dark:text-white">Wish — your most important goal right now</span>
                    </div>
                    <input value={wish} onChange={e => saveResponse('woopWish', e.target.value)} placeholder="e.g., Get a H3 or higher in English" className="w-full bg-transparent py-2.5 px-0 text-[15px] text-zinc-900 dark:text-white placeholder-zinc-400 outline-none border-b-2 border-zinc-200 dark:border-zinc-700 focus:border-amber-600" />
                </div>
                {/* Outcome */}
                <div>
                    <div className="flex items-center gap-2.5 mb-2">
                        <div className="w-8 h-8 flex items-center justify-center shrink-0 font-serif font-medium text-base" style={{ backgroundColor: '#93C5FD', border: '2px solid #2563EB', borderRadius: 10, boxShadow: '2px 2px 0px 0px #2563EB', color: '#1E3A8A' }}>O</div>
                        <span className="text-[13px] font-medium text-zinc-900 dark:text-white">Outcome — the best thing that would happen</span>
                    </div>
                    <input value={outcome} onChange={e => saveResponse('woopOutcome', e.target.value)} placeholder="e.g., I'd feel proud and confident applying for college" className="w-full bg-transparent py-2.5 px-0 text-[15px] text-zinc-900 dark:text-white placeholder-zinc-400 outline-none border-b-2 border-zinc-200 dark:border-zinc-700 focus:border-blue-600" />
                </div>
                {/* Obstacle */}
                <div>
                    <div className="flex items-center gap-2.5 mb-2">
                        <div className="w-8 h-8 flex items-center justify-center shrink-0 font-serif font-medium text-base" style={{ backgroundColor: '#FCA5A5', border: '2px solid #DC2626', borderRadius: 10, boxShadow: '2px 2px 0px 0px #DC2626', color: '#7F1D1D' }}>O</div>
                        <span className="text-[13px] font-medium text-zinc-900 dark:text-white">Obstacle — the main thing inside you that gets in the way</span>
                    </div>
                    <input value={obstacle} onChange={e => saveResponse('woopObstacle', e.target.value)} placeholder="e.g., I procrastinate when the essay feels overwhelming" className="w-full bg-transparent py-2.5 px-0 text-[15px] text-zinc-900 dark:text-white placeholder-zinc-400 outline-none border-b-2 border-zinc-200 dark:border-zinc-700 focus:border-red-600" />
                </div>
                {/* Plan */}
                <div>
                    <div className="flex items-center gap-2.5 mb-2">
                        <div className="w-8 h-8 flex items-center justify-center shrink-0 font-serif font-medium text-base" style={{ backgroundColor: '#6EE7B7', border: '2px solid #059669', borderRadius: 10, boxShadow: '2px 2px 0px 0px #059669', color: '#064E3B' }}>P</div>
                        <span className="text-[13px] font-medium text-zinc-900 dark:text-white">Plan — "If [obstacle], then I will..."</span>
                    </div>
                    <input value={plan} onChange={e => saveResponse('woopPlan', e.target.value)} placeholder="e.g., If I feel overwhelmed, I'll just write the first paragraph" className="w-full bg-transparent py-2.5 px-0 text-[15px] text-zinc-900 dark:text-white placeholder-zinc-400 outline-none border-b-2 border-zinc-200 dark:border-zinc-700 focus:border-emerald-600" />
                </div>
            </div>
            {isComplete && (
                <motion.div initial={{opacity:0}} animate={{opacity:1}} className="mt-8 p-4 rounded-xl text-center" style={{ backgroundColor: '#6EE7B7', border: '2.5px solid #059669', boxShadow: '3px 3px 0px 0px #059669' }}>
                    <p className="text-sm font-bold" style={{ color: '#064E3B' }}>Blueprint complete. You've turned a wish into an actual plan.</p>
                </motion.div>
            )}
        </div>
    );
};

// --- MODULE COMPONENT ---
const BestPossibleSelfModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const essentials = useEssentialsMode();
  const { responses, saveResponse, isLoaded: _isLoaded } = useModuleResponses('best-possible-self');
  const { northStar } = useNorthStar();

  const sections = [
    { id: 'daydream-problem', title: 'The Daydream Problem', eyebrow: '01 // The Trap', icon: BatteryWarning },
    { id: 'bps-protocol', title: 'The "Best Possible Self" Protocol', eyebrow: '02 // The Vision', icon: MapPin },
    { id: 'mental-contrasting', title: 'The Reality Check', eyebrow: '03 // Mental Contrasting', icon: Filter },
    { id: 'woop-method', title: 'The WOOP Method', eyebrow: '04 // The System', icon: Zap },
    { id: 'implementation', title: 'Build Your First WOOP', eyebrow: '05 // The Action Plan', icon: ClipboardCheck },
  ];

  return (
    <ModuleLayout
      moduleNumber="04"
      moduleTitle="Best Possible Self"
      moduleSubtitle="The Future-Proofing Playbook"
      moduleDescription="Daydreaming about the future feels good — but it can actually kill your motivation. Learn how to turn vague wishes into real plans that stick."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Own Your Future"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Daydream Problem." eyebrow="Step 1" icon={BatteryWarning} theme={theme}>
              {essentials ? (
                <>
                  <p>Here's the trap: daydreaming about success without planning the work actually drains your motivation. Your brain treats the fantasy like it already happened. This is <Highlight description="When you daydream about success without thinking about the work, your brain actually relaxes — as if you've already done it. It feels great in the moment, but it drains the energy you need to actually get started." theme={theme}>positive fantasising</Highlight>.</p>
                  <p>The fix is not to stop dreaming. The fix is to dream smarter.</p>
                </>
              ) : (
                <>
                  <p>We're told to "think positive" and visualise our dreams. But here's the trap: pure <Highlight description="When you daydream about success without thinking about the work, your brain actually relaxes — as if you've already done it. It feels great in the moment, but it drains the energy you need to actually get started." theme={theme}>positive fantasising</Highlight> can backfire. When you spend time daydreaming about acing the Leaving Cert or getting that college offer without thinking about the work involved, your brain treats it like you've already made it. It feels good — but it quietly drains the energy you need to actually get started.</p>
                  <p>This is why some of the most ambitious, optimistic students still struggle to follow through. The dreaming itself is eating their motivation. The fix isn't to stop dreaming — it's to dream smarter.</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="The 'Best Possible Self' Exercise." eyebrow="Step 2" icon={MapPin} theme={theme}>
              {northStar && (() => { const p = COMPACT_CALLOUT_PLACEMENTS.find(p => p.moduleId === 'best-possible-self-protocol'); return p ? <NorthStarCallout northStar={northStar} variant="compact" message={p.message} /> : null; })()}
              {essentials ? (
                <>
                  <p>Write a detailed picture of your life in 5 years. This is the <Highlight description="You write a vivid, detailed description of your future life — the version where things have gone well because you put in the work. Not a vague wish, but a clear picture your brain can actually aim for." theme={theme}>'Best Possible Self'</Highlight> exercise. Be specific: where do you live, what do you do, how do you feel? A vivid target gives your brain something real to aim for.</p>
                </>
              ) : (
                <>
                  <p>The fix is to dream with purpose. The <Highlight description="You write a vivid, detailed description of your future life — the version where things have gone well because you put in the work. Not a vague wish, but a clear picture your brain can actually aim for." theme={theme}>'Best Possible Self'</Highlight> exercise works like this: instead of a vague "I want to do well," you write a detailed picture of your future life — the version where you've put in the work and things have gone well. The more specific and vivid you make it, the more powerful it is.</p>
                  <p>This isn't about being unrealistic. It's about giving your brain a clear target. A vague dream of "doing well" gives your brain nothing to work with. A detailed picture of who you want to become in 5 years gives it a destination to drive toward.</p>
                  <PersonalStory name="Alex" role="Founder, NextStepUni">
                    <p>I used to daydream constantly about a better life but never did anything about it. It was only when someone asked me to write it down — properly, in detail — that something clicked. Seeing the gap between where I was and where I wanted to be wasn't depressing. It was the first time I felt genuinely motivated, because I could finally see what I was working toward.</p>
                  </PersonalStory>
                </>
              )}
              <MicroCommitment theme={theme}><p>Open the notes app on your phone. Write one paragraph describing what your life looks like in 5 years if everything goes as well as it possibly could. Be specific — where do you live? What do you do? How do you feel?</p></MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="The Reality Check." eyebrow="Step 3" icon={Filter} theme={theme}>
              {essentials ? (
                <p>After your dream, do a reality check. Ask: "What's standing in my way?" Be honest about internal obstacles. This is <Highlight description="Right after imagining your best future, you immediately think about the real obstacles standing in your way — especially the ones inside you (habits, fears, procrastination). That contrast between dream and reality is what creates the energy to actually act." theme={theme}>Mental Contrasting</Highlight>. The contrast between dream and reality creates real motivation.</p>
              ) : (
                <>
                  <p>A vivid dream on its own isn't enough. The crucial next step is to ground it in reality. This is <Highlight description="Right after imagining your best future, you immediately think about the real obstacles standing in your way — especially the ones inside you (habits, fears, procrastination). That contrast between dream and reality is what creates the energy to actually act." theme={theme}>Mental Contrasting</Highlight>.</p>
                  <p>After picturing your Best Possible Self, you ask: "What's actually standing between me and that?" — and you're honest about it. Not "the system is against me" (even if it sometimes is), but the obstacles inside you: the procrastination, the self-doubt, the habit of giving up when things get hard. That contrast — dream vs. reality — is what creates genuine motivation to act.</p>
                </>
              )}
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="The WOOP Method." eyebrow="Step 4" icon={Zap} theme={theme}>
                <p>{essentials ? 'Combine dream + reality check into the' : 'Putting the dream and the reality check together gives you the'} <Highlight description="A four-step system: Wish (what you want), Outcome (why it matters), Obstacle (what's in the way), Plan (what you'll do about it). It turns vague wishes into concrete action." theme={theme}>WOOP Method</Highlight>{essentials ? ': Wish, Outcome, Obstacle, Plan.' : ' — a simple system for turning wishes into real plans:'}</p>
                <div className="my-10 rounded-2xl p-5 md:p-6 space-y-3" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
                  <div className="p-4 flex items-start gap-4" style={{ backgroundColor: '#93C5FD', border: '2.5px solid #2563EB', borderRadius: 16, boxShadow: '4px 4px 0px 0px #2563EB' }}>
                    <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-white" style={{ backgroundColor: '#2563EB' }}>W</div>
                    <div>
                      <p className="text-sm font-bold" style={{ color: '#1E3A8A' }}>Wish</p>
                      <p className="text-[13px] mt-0.5" style={{ color: '#1E3A8A', opacity: 0.8 }}>What's the goal? Be specific.</p>
                    </div>
                  </div>
                  <div className="p-4 flex items-start gap-4" style={{ backgroundColor: '#FCD34D', border: '2.5px solid #D97706', borderRadius: 16, boxShadow: '4px 4px 0px 0px #D97706' }}>
                    <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-white" style={{ backgroundColor: '#D97706' }}>O</div>
                    <div>
                      <p className="text-sm font-bold" style={{ color: '#78350F' }}>Outcome</p>
                      <p className="text-[13px] mt-0.5" style={{ color: '#78350F', opacity: 0.8 }}>What's the best thing that happens if you achieve it? Feel it.</p>
                    </div>
                  </div>
                  <div className="p-4 flex items-start gap-4" style={{ backgroundColor: '#FDBA74', border: '2.5px solid #EA580C', borderRadius: 16, boxShadow: '4px 4px 0px 0px #EA580C' }}>
                    <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-white" style={{ backgroundColor: '#EA580C' }}>O</div>
                    <div>
                      <p className="text-sm font-bold" style={{ color: '#7C2D12' }}>Obstacle</p>
                      <p className="text-[13px] mt-0.5" style={{ color: '#7C2D12', opacity: 0.8 }}>What's the main thing *inside you* that could derail it?</p>
                    </div>
                  </div>
                  <div className="p-4 flex items-start gap-4" style={{ backgroundColor: '#6EE7B7', border: '2.5px solid #059669', borderRadius: 16, boxShadow: '4px 4px 0px 0px #059669' }}>
                    <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-white" style={{ backgroundColor: '#059669' }}>P</div>
                    <div>
                      <p className="text-sm font-bold" style={{ color: '#064E3B' }}>Plan</p>
                      <p className="text-[13px] mt-0.5" style={{ color: '#064E3B', opacity: 0.8 }}>"If [obstacle happens], then I will [specific action]."</p>
                    </div>
                  </div>
                </div>
                <p>That last step is the key. It pre-loads a response so your brain doesn't have to figure it out in the moment. When the obstacle hits, you already know what to do.</p>
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="Build Your First WOOP." eyebrow="Step 5" icon={ClipboardCheck} theme={theme}>
              {essentials ? (
                <p>Use the blueprint below to build your first WOOP. Pick something real. Do this every Sunday evening for 5 minutes.</p>
              ) : (
                <>
                  <p>WOOP is a 5-minute exercise you can use before any study session, exam, or important week. The more you use it, the more automatic it becomes — your brain starts linking your daily habits to your long-term goals without you even thinking about it.</p>
                  <p>Use the blueprint below to build your first WOOP. Pick something real — maybe a subject you're struggling with, or a goal for this week.</p>
                </>
              )}
              <WOOPPlanner responses={responses} saveResponse={saveResponse} />
              <MicroCommitment theme={theme}><p>Set a reminder on your phone for Sunday evening called "Weekly WOOP." Spend 5 minutes running the exercise for the week ahead. Try it for 3 weeks and see how it changes your focus.</p></MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default BestPossibleSelfModule;
