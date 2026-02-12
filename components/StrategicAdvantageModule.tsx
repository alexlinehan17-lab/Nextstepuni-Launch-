/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Feather, BookOpen, Scale, Award, FileText
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { indigoTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = indigoTheme;

// --- INTERACTIVE COMPONENTS ---
const NarrativeSwitcher = () => {
    const [script, setScript] = useState<'idle' | 'contamination' | 'redemption'>('idle');
    const [animKey, setAnimKey] = useState(0);

    const contamination = [
      { text: '"I failed the mock."', tone: 'neutral' as const },
      { text: '"I\'m just not smart enough."', tone: 'bad' as const },
      { text: '"Everyone else got it. What\'s wrong with me?"', tone: 'bad' as const },
      { text: '"There\'s no point trying harder."', tone: 'bad' as const },
      { text: '"I give up."', tone: 'bad' as const },
    ];

    const redemption = [
      { text: '"I failed the mock."', tone: 'neutral' as const },
      { text: '"That stings. But now I know exactly where the gaps are."', tone: 'good' as const },
      { text: '"I\'m going to target those weak areas this week."', tone: 'good' as const },
      { text: '"I\'ll do 3 past papers focused on the topics I got wrong."', tone: 'good' as const },
      { text: '"This failure just became my study plan."', tone: 'good' as const },
    ];

    const handleSelect = (type: 'contamination' | 'redemption') => {
      setScript(type);
      setAnimKey(k => k + 1);
    };

    const toneStyles = {
      neutral: 'bg-zinc-100 dark:bg-zinc-700/50 text-zinc-700 dark:text-zinc-300 border-zinc-200 dark:border-zinc-600',
      bad: 'bg-rose-50 dark:bg-rose-950/30 text-rose-700 dark:text-rose-300 border-rose-200 dark:border-rose-800/50',
      good: 'bg-emerald-50 dark:bg-emerald-950/30 text-emerald-700 dark:text-emerald-300 border-emerald-200 dark:border-emerald-800/50',
    };

    const renderSequence = (steps: typeof contamination, active: boolean) => (
      <div className="space-y-3">
        {steps.map((step, i) => (
          <motion.div
            key={`${animKey}-${i}`}
            initial={active ? { opacity: 0, y: 10 } : { opacity: 0.3 }}
            animate={active ? { opacity: 1, y: 0 } : { opacity: 0.3 }}
            transition={active ? { delay: i * 0.4, duration: 0.4 } : { duration: 0.3 }}
            className={`p-3 rounded-lg border text-sm font-medium ${active ? toneStyles[step.tone] : 'bg-zinc-50 dark:bg-zinc-800/30 text-zinc-300 dark:text-zinc-600 border-zinc-100 dark:border-zinc-800'}`}
          >
            {i > 0 && active && (
              <motion.span
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: i * 0.4 + 0.1 }}
                className="mr-1.5"
              >
                →
              </motion.span>
            )}
            {step.text}
          </motion.div>
        ))}
      </div>
    );

    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Narrative Switcher</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Pivotal Moment: You fail an important mock exam. Which story do you tell?</p>
            <div className="flex justify-center gap-4 mb-8">
                <button onClick={() => handleSelect('contamination')} className={`px-5 py-2.5 text-xs font-bold rounded-lg transition-all ${script === 'contamination' ? 'bg-rose-500 text-white shadow-lg shadow-rose-500/20' : 'bg-rose-100 text-rose-800 hover:bg-rose-200'}`}>Contamination Script</button>
                <button onClick={() => handleSelect('redemption')} className={`px-5 py-2.5 text-xs font-bold rounded-lg transition-all ${script === 'redemption' ? 'bg-emerald-500 text-white shadow-lg shadow-emerald-500/20' : 'bg-emerald-100 text-emerald-800 hover:bg-emerald-200'}`}>Redemption Script</button>
            </div>
            {script !== 'idle' && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <p className={`text-xs font-bold uppercase tracking-wider mb-3 ${script === 'contamination' ? 'text-rose-500' : 'text-zinc-300 dark:text-zinc-600'}`}>Contamination Script</p>
                  {renderSequence(contamination, script === 'contamination')}
                </div>
                <div>
                  <p className={`text-xs font-bold uppercase tracking-wider mb-3 ${script === 'redemption' ? 'text-emerald-500' : 'text-zinc-300 dark:text-zinc-600'}`}>Redemption Script</p>
                  {renderSequence(redemption, script === 'redemption')}
                </div>
              </div>
            )}
        </div>
    );
};


const AgencyCommunionBalancer = () => {
    const [balance, setBalance] = useState(0); // -1 for Agency, 1 for Communion, 0 for balanced
    return(
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Agency & Communion Balancer</h4>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-12">Click the narrative statement that builds the most robust identity.</p>
             <div className="h-40 flex justify-center items-center">
                <motion.div animate={{rotate: balance * 15}} className="w-56 h-20 relative">
                    <div className="w-full h-2 bg-zinc-300 absolute bottom-0 left-0" />
                    <div className="w-2 h-4 bg-zinc-300 absolute bottom-0 left-1/2 -translate-x-1/2" />
                    <div className="w-12 h-12 bg-blue-100 rounded-md absolute -left-6 -bottom-1" />
                    <div className="w-12 h-12 bg-emerald-100 rounded-md absolute -right-6 -bottom-1" />
                </motion.div>
             </div>
             <div className="grid grid-cols-3 gap-2 mt-6">
                <button
                    onClick={() => setBalance(-1)}
                    className={`p-2 text-xs border rounded-lg transition-all ${balance === -1 ? 'border-blue-500 bg-blue-50' : 'border-zinc-200 dark:border-zinc-700'}`}
                >
                    "I did it all myself." (Pure Agency)
                </button>
                <button
                    onClick={() => setBalance(0)}
                    className={`p-2 text-xs border rounded-lg transition-all ${balance === 0 ? 'border-indigo-500 bg-indigo-50' : 'border-zinc-200 dark:border-zinc-700'}`}
                >
                    "I worked hard to honor my family's sacrifices." (Balanced)
                </button>
                <button
                    onClick={() => setBalance(1)}
                    className={`p-2 text-xs border rounded-lg transition-all ${balance === 1 ? 'border-emerald-500 bg-emerald-50' : 'border-zinc-200 dark:border-zinc-700'}`}
                >
                    "I only survived because of others." (Pure Communion)
                </button>
             </div>
        </div>
    )
};

const DesirableDifficultyChart = () => (
    <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
         <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Chart: The Illusion of Fluency</h4>
         <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">"Easy" learning feels good, but "hard" learning builds lasting knowledge.</p>
         <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="text-left">
                <h5 className="font-bold mb-4 text-center">Easy Learning (Re-reading)</h5>
                <div className="space-y-4">
                    <div>
                        <span className="text-xs font-bold text-zinc-500 dark:text-zinc-400">Feeling of Learning:</span>
                        <div className="w-full bg-zinc-100 dark:bg-zinc-800 rounded-full h-5 mt-1 overflow-hidden">
                            <motion.div initial={{width: 0}} animate={{width: '90%'}} className="h-full bg-fuchsia-400 rounded-full" />
                        </div>
                    </div>
                    <div>
                        <span className="text-xs font-bold text-zinc-500 dark:text-zinc-400">Long-term Retention:</span>
                        <div className="w-full bg-zinc-100 dark:bg-zinc-800 rounded-full h-5 mt-1 overflow-hidden">
                            <motion.div initial={{width: 0}} animate={{width: '20%'}} className="h-full bg-indigo-400 rounded-full" />
                        </div>
                    </div>
                </div>
            </div>
             <div className="text-left">
                <h5 className="font-bold mb-4 text-center">Hard Learning (Practice Qs)</h5>
                <div className="space-y-4">
                     <div>
                        <span className="text-xs font-bold text-zinc-500 dark:text-zinc-400">Feeling of Learning:</span>
                        <div className="w-full bg-zinc-100 dark:bg-zinc-800 rounded-full h-5 mt-1 overflow-hidden">
                            <motion.div initial={{width: 0}} animate={{width: '30%'}} className="h-full bg-fuchsia-400 rounded-full" />
                        </div>
                    </div>
                    <div>
                        <span className="text-xs font-bold text-zinc-500 dark:text-zinc-400">Long-term Retention:</span>
                        <div className="w-full bg-zinc-100 dark:bg-zinc-800 rounded-full h-5 mt-1 overflow-hidden">
                            <motion.div initial={{width: 0}} animate={{width: '85%'}} className="h-full bg-indigo-400 rounded-full" />
                        </div>
                    </div>
                </div>
            </div>
         </div>
    </div>
);

// --- MODULE COMPONENT ---
const StrategicAdvantageModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'narrative-identity', title: 'The Story of You', eyebrow: '01 // Your Internal Script', icon: Feather },
    { id: 'agency-communion', title: 'The Two Pillars', eyebrow: '02 // Agency & Communion', icon: Scale },
    { id: 'pivotal-moments', title: 'The Power of Failure', eyebrow: '03 // Pivotal Moments', icon: BookOpen },
    { id: 'desirable-difficulties', title: 'The Advantage of Disadvantage', eyebrow: '04 // Desirable Difficulties', icon: Award },
    { id: 'redemption-script', title: 'Your Redemption Script', eyebrow: '05 // The Blueprint', icon: FileText },
  ];

  return (
    <ModuleLayout
      moduleNumber="08"
      moduleTitle="Your Strategic Advantage"
      moduleSubtitle="The Narrative Identity Protocol"
      moduleDescription="Discover how to turn your personal story of adversity into your greatest competitive advantage in academia and beyond."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Story of You." eyebrow="Step 1" icon={Feather} theme={theme}>
              <p>You are a storyteller. The most important story you will ever tell is the one you tell yourself about your own life. This is your <Highlight description="Pioneered by psychologist Dan McAdams, this is the internalized, evolving story of the self that each person crafts to provide their life with a sense of meaning and purpose." theme={theme}>Narrative Identity</Highlight>. It's how you make sense of your past, present, and future.</p>
              <p>Society often hands students from tough backgrounds a ready-made story: a tale of deficit and struggle. This is a <Highlight description="A life story in which a positive event is ruined or spoiled by a subsequent negative event, leading to feelings of hopelessness and despair." theme={theme}>Contamination Script</Highlight>. Resilience is the act of radical authorship: rejecting that story and writing your own, a <Highlight description="A life story in which a negative event is 'redeemed' or transformed by a positive outcome, leading to growth, learning, and a sense of agency." theme={theme}>Redemption Script</Highlight> where adversity becomes the source of your strength.</p>
              <NarrativeSwitcher />
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The Two Pillars." eyebrow="Step 2" icon={Scale} theme={theme}>
                <p>Every great story is built on two core themes. The first is <Highlight description="A narrative theme focused on the protagonist's autonomy, power, and ability to control their own destiny. It's about self-mastery and achievement." theme={theme}>Agency</Highlight>--the story of the self-reliant hero who overcomes obstacles through their own power. The second is <Highlight description="A narrative theme focused on connection, intimacy, and belonging. It's about love, friendship, and being part of a community." theme={theme}>Communion</Highlight>--the story of connection, of being supported by family, friends, and community.</p>
                <p>A story of pure Agency leads to the "Isolated Hero" who burns out. A story of pure Communion leads to passivity. The most resilient narrative identities skillfully weave both: "I worked hard (Agency) to honor the sacrifices of my family (Communion)." Finding this balance is key to a sustainable story of success.</p>
                <AgencyCommunionBalancer />
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The Power of Failure." eyebrow="Step 3" icon={BookOpen} theme={theme}>
              <p>Your life story is not a continuous film; it's a collection of key scenes. These are your <Highlight description="Significant life experiences--high points, low points, and turning points--that are heavily interpreted and serve as anchors for your narrative identity." theme={theme}>Pivotal Moments</Highlight>. For resilient individuals, the most important pivotal moments are often failures. They are the moments where suffering is transformed into insight.</p>
              <p>The key is to learn the art of <Highlight description="The cognitive skill of changing the context or interpretation of an event to alter its meaning. It is the primary mechanism by which we assert agency over circumstance." theme={theme}>Reframing</Highlight>. A technique like the "Failure Resume" helps you de-shame failure and see it not as a verdict on your worth, but as valuable data for future success. It's about learning to say, "I didn't suffer for nothing; I suffered to become stronger."</p>
              <MicroCommitment theme={theme}>
                <p>Think of one failure from the last year. Now, name one thing you learned from it that you couldn't have learned otherwise. You've just taken the first step in writing a redemption script.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="The Advantage of Disadvantage." eyebrow="Step 4" icon={Award} theme={theme}>
              <p>What if the things that make your academic journey harder are the very things that are making your learning deeper and more durable? This is the principle of <Highlight description="Coined by Robert Bjork, these are learning conditions that are effortful and slow down immediate performance but lead to much better long-term retention and transfer of knowledge." theme={theme}>Desirable Difficulties</Highlight>. Learning that is "easy" (like re-reading notes) is shallow. Learning that is "hard" (like struggling to solve a problem without help) forces deeper processing and builds stronger neural pathways.</p>
              <p>Students from disadvantaged backgrounds often face *involuntary* desirable difficulties. Lack of tutors forces self-explanation (generative learning). Time scarcity forces spaced practice instead of cramming. Resource scarcity builds resourcefulness (self-directed learning). These are not liabilities; they are hidden training programs that build a cognitive toolkit that privileged peers may lack.</p>
              <DesirableDifficultyChart />
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Your Redemption Script." eyebrow="Step 5" icon={FileText} theme={theme}>
              <p>You have the power to be the author of your own story. This module has given you the tools of narrative construction: the ability to turn contamination into redemption, to balance agency with communion, and to reframe difficulty as a desirable advantage. Now it's time to put it into practice.</p>
              <p>The final step is to build your own mini-"Failure Resume." By taking a past failure and actively converting it into an asset, you are practicing the core skill of resilient identity construction. You are forging your own redemption script, turning the lead of your past into the gold of your future.</p>
              <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
                <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">My Redemption Story</h4>
                 <div className="mt-6 space-y-4">
                    <div>
                        <label className="block text-xs font-semibold text-zinc-600 dark:text-zinc-300 uppercase ml-4 mb-2">The Failure (Pivotal Moment):</label>
                        <select className="w-full p-4 bg-zinc-50 dark:bg-zinc-800/50 border border-zinc-100 rounded-xl focus:outline-none focus:border-indigo-500"><option>Failed a mock exam</option><option>Missed an assignment deadline</option><option>Didn't understand a topic in class</option></select>
                    </div>
                     <div>
                        <label className="block text-xs font-semibold text-zinc-600 dark:text-zinc-300 uppercase ml-4 mb-2">The Lesson (Your Asset):</label>
                        <textarea placeholder="What is the single most valuable lesson, skill, or piece of wisdom you gained from this experience?" className="w-full h-24 p-4 bg-zinc-50 dark:bg-zinc-800/50 border border-zinc-100 rounded-xl focus:outline-none focus:border-indigo-500"></textarea>
                    </div>
                </div>
              </div>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default StrategicAdvantageModule;
