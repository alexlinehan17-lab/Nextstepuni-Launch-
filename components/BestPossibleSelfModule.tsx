/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import {
  MapPin, BatteryWarning, Filter, Zap, ClipboardCheck
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { blueTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = blueTheme;

// --- INTERACTIVE COMPONENTS ---

const WOOPPlanner = () => {
    const [woop, setWoop] = useState({ wish: '', outcome: '', obstacle: '', plan: '' });
    const update = (field: keyof typeof woop, value: string) => setWoop(prev => ({...prev, [field]: value}));
    const isComplete = Object.values(woop).every(v => v.trim() !== '');

    return(
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Your WOOP Blueprint</h4>
            <div className="space-y-4 mt-8">
                <input value={woop.wish} onChange={e => update('wish', e.target.value)} placeholder="WISH: Your most important wish..." className="w-full p-4 bg-zinc-50 dark:bg-zinc-800/50 rounded-lg border border-zinc-100 focus:border-blue-500 outline-none"/>
                <input value={woop.outcome} onChange={e => update('outcome', e.target.value)} placeholder="OUTCOME: The best result from that..." className="w-full p-4 bg-zinc-50 dark:bg-zinc-800/50 rounded-lg border border-zinc-100 focus:border-blue-500 outline-none"/>
                <input value={woop.obstacle} onChange={e => update('obstacle', e.target.value)} placeholder="OBSTACLE: The main inner barrier..." className="w-full p-4 bg-zinc-50 dark:bg-zinc-800/50 rounded-lg border border-zinc-100 focus:border-blue-500 outline-none"/>
                <input value={woop.plan} onChange={e => update('plan', e.target.value)} placeholder="PLAN: If [obstacle], then I will..." className="w-full p-4 bg-zinc-50 dark:bg-zinc-800/50 rounded-lg border border-zinc-100 focus:border-blue-500 outline-none"/>
            </div>
            {isComplete && (
                <motion.div initial={{opacity:0}} animate={{opacity:1}} className="text-center mt-6">
                    <p className="text-sm font-bold text-emerald-600">Blueprint complete! You've turned a wish into an actionable plan.</p>
                </motion.div>
            )}
        </div>
    );
};

// --- MODULE COMPONENT ---
const BestPossibleSelfModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'daydream-problem', title: 'The Daydream Problem', eyebrow: '01 // The Trap', icon: BatteryWarning },
    { id: 'bps-protocol', title: 'The "Best Possible Self" Protocol', eyebrow: '02 // The Vision', icon: MapPin },
    { id: 'mental-contrasting', title: 'The Reality Check', eyebrow: '03 // Mental Contrasting', icon: Filter },
    { id: 'woop-method', title: 'The WOOP Method', eyebrow: '04 // The System', icon: Zap },
    { id: 'implementation', title: 'Implementation & Habit', eyebrow: '05 // The Action Plan', icon: ClipboardCheck },
  ];

  return (
    <ModuleLayout
      moduleNumber="04"
      moduleTitle="Best Possible Self"
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Daydream Problem." eyebrow="Step 1" icon={BatteryWarning} theme={theme}>
              <p>We're often told to "think positive" and visualize our dreams. But research by Gabriele Oettingen reveals a paradox: pure <Highlight description="Indulging in idealized fantasies of the future. Counter-intuitively, this can relax you so much that it actually lowers your energy and motivation to take action." theme={theme}>positive fantasizing</Highlight> can be demotivating. It tricks your brain into feeling like you've already achieved the goal, reducing the energy you commit to the hard work needed to get there.</p>
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="The 'Best Possible Self' Protocol." eyebrow="Step 2" icon={MapPin} theme={theme}>
              <p>The solution isn't to stop dreaming, but to dream with purpose. The <Highlight description="A positive psychology intervention where you write in detail about an optimal future version of yourself. This has been shown to increase positive mood and build a sense of purpose." theme={theme}>'Best Possible Self' (BPS)</Highlight> exercise is a scientifically-validated tool for this. By writing a vivid, detailed description of your future life where you've achieved all your goals, you create a clear, emotionally-resonant target for your brain to aim for.</p>
              <MicroCommitment theme={theme}><p>Take 5 minutes. In your phone's notes app, write one paragraph describing what your life would look like in 5 years if everything went as well as it possibly could. Be specific.</p></MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="The Reality Check." eyebrow="Step 3" icon={Filter} theme={theme}>
              <p>A vivid dream is not enough. The crucial next step is to ground that dream in reality. This is <Highlight description="The process of contrasting your desired future with the real-world obstacles that stand in your way. This contrast is what generates the energy for action." theme={theme}>Mental Contrasting</Highlight>. After vividly imagining your 'Best Possible Self', you must immediately and just as vividly imagine the primary obstacle *within you* that holds you back. It's not about external problems; it's about your own habits and beliefs.</p>
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="The WOOP Method." eyebrow="Step 4" icon={Zap} theme={theme}>
                <p>This process of combining a positive vision with a realistic obstacle is the core of the <Highlight description="A powerful, four-step goal-setting strategy: Wish, Outcome, Obstacle, Plan. It combines positive thinking with a realistic assessment of barriers." theme={theme}>WOOP Method</Highlight>. It's a simple but profound algorithm for turning wishes into action.</p>
                <p>1. <strong>Wish:</strong> What is your most important goal? 2. <strong>Outcome:</strong> What is the best feeling or result if you achieve it? 3. <strong>Obstacle:</strong> What is the main thing *inside you* that stands in the way? 4. <strong>Plan:</strong> Create an "If [Obstacle], then I will [Action]" plan.</p>
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="Implementation & Habit." eyebrow="Step 5" icon={ClipboardCheck} theme={theme}>
              <p>You now have the full WOOP protocol. It's a portable, 5-minute tool you can use every day to align your daily actions with your long-term vision. By repeatedly running this mental simulation, you train your brain to automatically link your biggest dreams to your smallest daily habits. Use the blueprint below to run your first WOOP.</p>
              <WOOPPlanner />
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default BestPossibleSelfModule;
