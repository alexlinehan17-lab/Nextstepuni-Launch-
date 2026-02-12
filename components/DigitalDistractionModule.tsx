/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  BrainCircuit, Shield, Laptop, Home, Repeat, Users, Map
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { slateTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = slateTheme;

// --- INTERACTIVE COMPONENTS ---
const AttentionDeficitCalculator = () => {
    const [checks, setChecks] = useState(3);
    const recoveryMins = 23.25;
    const timeLost = Math.min(60, checks * recoveryMins);
    const deepWorkTime = Math.max(0, 60 - timeLost);
    const deepPct = Math.round((deepWorkTime / 60) * 100);

    return (
        <div className="my-10 p-6 md:p-10 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Attention Deficit Calculator</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">Every phone check triggers a ~23 minute attention recovery. How much of your study hour survives?</p>

            {/* Big number */}
            <div className="text-center mb-6">
                <motion.div
                    key={checks}
                    initial={{ scale: 0.9, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    className="inline-block"
                >
                    <span className={`text-6xl font-bold tabular-nums ${deepPct >= 60 ? 'text-emerald-500' : deepPct >= 30 ? 'text-amber-500' : deepPct > 0 ? 'text-orange-500' : 'text-rose-500'}`}>{deepWorkTime.toFixed(0)}</span>
                    <span className="text-2xl font-bold text-zinc-400 ml-1">/ 60 min</span>
                </motion.div>
                <p className="text-sm font-semibold text-zinc-500 dark:text-zinc-400 mt-1">of actual deep work</p>
            </div>

            {/* Hour bar — simple stacked bar */}
            <div className="w-full h-6 rounded-full bg-zinc-100 dark:bg-zinc-700 overflow-hidden flex mb-2">
                <motion.div
                    className="h-full bg-emerald-500 flex items-center justify-center"
                    animate={{ width: `${deepPct}%` }}
                    transition={{ type: 'spring', stiffness: 120, damping: 20 }}
                >
                    {deepPct > 18 && <span className="text-xs font-bold text-white">{deepPct}%</span>}
                </motion.div>
                <motion.div
                    className="h-full bg-rose-400 flex items-center justify-center"
                    animate={{ width: `${100 - deepPct}%` }}
                    transition={{ type: 'spring', stiffness: 120, damping: 20 }}
                >
                    {(100 - deepPct) > 18 && <span className="text-xs font-bold text-white">{100 - deepPct}%</span>}
                </motion.div>
            </div>
            <div className="flex justify-between text-xs mb-6">
                <span className="font-semibold text-emerald-600 dark:text-emerald-400">Deep Work</span>
                <span className="font-semibold text-rose-500 dark:text-rose-400">Recovery Time</span>
            </div>

            {/* Phone check selector */}
            <div className="mb-5">
                <p className="text-sm font-bold text-zinc-700 dark:text-zinc-200 mb-2.5">Phone checks per study hour</p>
                <div className="flex gap-1.5">
                    {Array.from({ length: 11 }).map((_, i) => {
                        const isActive = i === checks;
                        const bg = i === 0 ? 'bg-emerald-500' : i <= 2 ? 'bg-amber-500' : 'bg-rose-500';
                        const bgMuted = i === 0 ? 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400' : i <= 2 ? 'bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-400' : 'bg-zinc-100 dark:bg-zinc-700 text-zinc-500 dark:text-zinc-400';
                        return (
                            <button key={i} onClick={() => setChecks(i)}
                                className={`flex-1 py-2 rounded-lg text-sm font-bold transition-all ${isActive ? `${bg} text-white shadow-sm scale-105` : `${bgMuted} hover:opacity-80`}`}>
                                {i}
                            </button>
                        );
                    })}
                </div>
                <div className="flex justify-between text-xs text-zinc-400 mt-1.5">
                    <span>Phone away</span>
                    <span>Constant</span>
                </div>
            </div>

            {/* Insight */}
            <div className={`p-3.5 rounded-xl text-sm text-center ${
                checks === 0 ? 'bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800 text-emerald-700 dark:text-emerald-300' :
                checks <= 2 ? 'bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 text-amber-700 dark:text-amber-300' :
                'bg-rose-50 dark:bg-rose-900/20 border border-rose-200 dark:border-rose-800 text-rose-700 dark:text-rose-300'
            }`}>
                {checks === 0 && <span className="font-semibold">Phone away = full hour of deep work. This is the goal.</span>}
                {checks === 1 && <span>Even <strong>one check</strong> costs 23 minutes of recovery. You lose over a third of your hour.</span>}
                {checks === 2 && <span><strong>Two checks</strong> and you&apos;ve lost 46 minutes. Only 14 minutes of real studying.</span>}
                {checks === 3 && <span>At <strong>3 checks</strong>, you&apos;re losing over an hour of focus time. Your brain never reaches deep processing.</span>}
                {checks >= 4 && checks <= 6 && <span>At <strong>{checks} checks per hour</strong>, virtually none of your study time is productive. You&apos;re just sitting with a book open.</span>}
                {checks > 6 && <span><strong>{checks} checks per hour</strong> means you&apos;re checking your phone every {(60 / checks).toFixed(0)} minutes. This isn&apos;t studying — it&apos;s scrolling with extra steps.</span>}
            </div>
        </div>
    );
};

// --- MODULE COMPONENT ---
const DigitalDistractionModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'adversary', title: 'The Adversary', eyebrow: '01 // Neuroscience of Distraction', icon: BrainCircuit },
    { id: 'hardware-barrier', title: 'Hardware Architecture', eyebrow: '02 // The Physical Barrier', icon: Shield },
    { id: 'software-fortification', title: 'Software Fortification', eyebrow: '03 // The Laptop Sanctuary', icon: Laptop },
    { id: 'environmental-engineering', title: 'Environmental Engineering', eyebrow: '04 // The Study Sanctuary', icon: Home },
    { id: 'behavioral-engineering', title: 'Behavioral Engineering', eyebrow: '05 // Atomic Habits', icon: Repeat },
    { id: 'social-dynamics', title: 'Social Dynamics', eyebrow: '06 // The FOMO Barrier', icon: Users },
    { id: 'roadmap', title: 'The Roadmap', eyebrow: '07 // Strategic Implementation', icon: Map },
  ];

  return (
    <ModuleLayout
      moduleNumber="08"
      moduleTitle="Digital Distractions"
      moduleSubtitle="The Cognitive Sovereignty Protocol"
      moduleDescription="A blueprint for reclaiming your focus from the attention economy, using neuroscience-backed hardware, software, and behavioral barriers."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Adversary." eyebrow="Step 1" icon={BrainCircuit} theme={theme}>
              <p>Your inability to focus is not a character flaw. It's a predictable conflict between your brain's biology and a digital environment engineered to exploit it. The adolescent brain has an underdeveloped <Highlight description="The 'CEO' of your brain, responsible for impulse control and long-term planning." theme={theme}>Prefrontal Cortex (PFC)</Highlight> and a hyperactive <Highlight description="The brain's reward and emotion centre." theme={theme}>Limbic System</Highlight>. Social media is designed as a <Highlight description="Like a slot machine, it provides unpredictable rewards (likes, messages) that trigger a dopamine hit, creating a compulsive loop." theme={theme}>Variable Ratio Reinforcement Schedule</Highlight> that hijacks this system.</p>
              <p>Every time you switch tasks (from study to Snapchat), you suffer from <Highlight description="The 'cognitive residue' left from the previous task. It takes an average of 23 minutes to regain deep focus after an interruption." theme={theme}>Attention Residue</Highlight>. This module is a blueprint for reclaiming your <Highlight description="Your ability to direct your own attention and consciousness, free from external manipulation." theme={theme}>Cognitive Sovereignty</Highlight>.</p>
              <AttentionDeficitCalculator />
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="Hardware Architecture." eyebrow="Step 2" icon={Shield} theme={theme}>
              <p>Since your internal "software" (willpower) is compromised by adolescent biology, the most effective strategy is to alter the "hardware" of your environment. The most radical and effective barrier is the "Dumb Phone" revolution. By switching to a device without an algorithmic feed, you eliminate the possibility of distraction.</p>
              <p>This involves a trade-off between <Highlight description="Making a behavior more difficult to perform. The 'friction' of using a T9 keypad for texting is a powerful deterrent." theme={theme}>Friction</Highlight> and function. There's a hierarchy of devices, from the "Purist" Nokia with zero features, to the "Hybrid" CAT S22 Flip which has WhatsApp but is physically unpleasant to scroll on. The goal is to make the cost of the distraction (frustration) outweigh the reward.</p>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="Software Fortification." eyebrow="Step 3" icon={Laptop} theme={theme}>
              <p>Your laptop is a "Trojan Horse"--a study tool that is also the main portal for distraction. Browser extensions are easily disabled. You need system-level blocking architecture. Applications like <Highlight description="Software that can block websites, apps, or the entire internet on your computer. 'Locked Mode' makes it impossible to bypass the block." theme={theme}>Freedom or Cold Turkey</Highlight> are essential.</p>
              <p>The best strategy is an "Allowlist" that creates a <Highlight description="Blocking the entire internet except for a few pre-approved educational sites like Studyclix or Examinations.ie." theme={theme}>"Walled Garden."</Highlight> To counter the "I need it for research" excuse, you can build an <Highlight description="Using tools like Kiwix to download entire websites (like Wikipedia) for offline use, satisfying the need for information without the temptation of the live internet." theme={theme}>"Offline Internet"</Highlight>. This separates "Hunting" for information from "Gathering" it.</p>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="Environmental Engineering." eyebrow="Step 4" icon={Home} theme={theme}>
              <p>Your physical environment is a silent architect of your behavior. The principle of <Highlight description="The neurobiological fact that the mere presence of a tempting object (like a phone) in your visual field consumes cognitive resources as your brain actively works to inhibit the impulse to use it." theme={theme}>Visual Field Management</Highlight> is crucial. "Out of sight, out of mind" is not a cliche; it's a neurological reality. The mere presence of your phone, even face down, causes "Brain Drain."</p>
              <p>The protocol is simple: the phone must be physically removed from the study room. It should be charged in a communal area like the kitchen. To counter the "I use it to check the time" excuse, place a simple analog clock on your desk.</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Behavioral Engineering." eyebrow="Step 5" icon={Repeat} theme={theme}>
              <p>You can automate the creation of these barriers using principles from behavioral psychology. The first tool is <Highlight description="A technique from James Clear's 'Atomic Habits' where you pair a new, desired behavior with an established one." theme={theme}>Habit Stacking</Highlight>. The formula is: "After [Current Habit], I will [New Habit]." For example: "After I walk in the door from school, I will immediately put my phone in the kitchen charger."</p>
              <p>The second tool is <Highlight description="An 'If-Then' plan that pre-programs your response to an inevitable distraction, removing the need for in-the-moment willpower." theme={theme}>Implementation Intentions</Highlight>. The formula: "If [Trigger occurs], then I will [Action]." For example: "If I feel the urge to check Instagram, then I will stand up and do 5 star jumps." This removes the need to negotiate with your tired brain.</p>
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="Social Dynamics." eyebrow="Step 6" icon={Users} theme={theme}>
              <p>The biggest barrier to disconnecting is not the technology; it's the social anxiety it alleviates--the Fear Of Missing Out (FOMO). Disconnecting without explanation can lead to social friction. The <Highlight description="The strategy of explicitly communicating your new boundaries to your friends (e.g., 'I'm off my phone from 5-9 PM for the LC, I'll reply after')." theme={theme}>"Social Contract"</Highlight> strategy manages expectations.</p>
              <p>Instead of constant, low-quality connection, you should <Highlight description="The practice of condensing your social media use into specific, pre-scheduled 'Online Windows' (e.g., 8:30-9:30 PM)." theme={theme}>"Batch" your socialization</Highlight>. This makes the interactions more focused and turns them into a reward for a day of deep work, rather than a constant background noise that fragments your attention.</p>
            </ReadingSection>
          )}
          {activeSection === 6 && (
            <ReadingSection title="The Roadmap." eyebrow="Step 7" icon={Map} theme={theme}>
              <p>Implementing these barriers is a phased process over the Leaving Cert cycle. <strong>Phase 1: The Audit (Sept - Dec).</strong> Install RescueTime, identify your time sinks, and start with a Level 1 detox (phone out of the room at night). <strong>Phase 2: The Hardening (Jan - Mar).</strong> Introduce software blockers, an "Offline Internet," and "batch" your social communication. <strong>Phase 3: The Sprint (Apr - June).</strong> This is "Monk Mode." Switch to a "dumb phone," use "Locked Mode" on laptops, and consider deactivating social media accounts.</p>
              <MicroCommitment theme={theme}>
                <p>Tonight, take your phone charger out of your bedroom and move it to the kitchen. This is your first, most important step in building a wall of friction.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default DigitalDistractionModule;
