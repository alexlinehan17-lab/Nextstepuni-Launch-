/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Link2, Brain, Wand2, Gamepad2, Briefcase, Wind
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { fuchsiaTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = fuchsiaTheme;

// --- INTERACTIVE COMPONENTS ---

const WOOPPlanner = () => {
    const [data, setData] = useState({wish: '', outcome: '', obstacle: '', plan: ''});
    const update = (field: string, value: string) => setData(prev => ({...prev, [field]: value}));

    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-2xl border border-zinc-200 dark:border-zinc-700 shadow-xl">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center italic">My WOOP Blueprint</h4>
            <div className="space-y-4 mt-6">
                <input value={data.wish} onChange={e => update('wish', e.target.value)} placeholder="WISH: What do you want to achieve?" className="w-full p-3 bg-zinc-50 dark:bg-zinc-800/50 rounded-lg"/>
                <input value={data.outcome} onChange={e => update('outcome', e.target.value)} placeholder="OUTCOME: What's the best feeling if you do?" className="w-full p-3 bg-zinc-50 dark:bg-zinc-800/50 rounded-lg"/>
                <input value={data.obstacle} onChange={e => update('obstacle', e.target.value)} placeholder="OBSTACLE: What *inside you* holds you back?" className="w-full p-3 bg-zinc-50 dark:bg-zinc-800/50 rounded-lg"/>
                <input value={data.plan} onChange={e => update('plan', e.target.value)} placeholder="PLAN: If [obstacle], then I will..." className="w-full p-3 bg-zinc-50 dark:bg-zinc-800/50 rounded-lg"/>
            </div>
        </div>
    );
};

// --- MODULE COMPONENT ---
const ConnectingEducationToGoalsModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'time-horizon', title: 'The Time Horizon Problem', eyebrow: '01 // The Why', icon: Wind },
    { id: 'motivation-engine', title: 'The Engine of Motivation', eyebrow: '02 // The Fuel', icon: Brain },
    { id: 'impossibility-heuristic', title: 'The "Impossibility" Heuristic', eyebrow: '03 // The Reframe', icon: Wand2 },
    { id: 'structural-levers', title: 'Hacking the System', eyebrow: '04 // The Levers', icon: Briefcase },
    { id: 'playbook-motivation', title: 'Playbook: The "Why"', eyebrow: '05 // Motivation & Identity', icon: Gamepad2 },
    { id: 'playbook-action', title: 'Playbook: The "How" & "What"', eyebrow: '06 // The Action Plan', icon: Link2 },
  ];

  return (
    <ModuleLayout
      moduleNumber="14"
      moduleTitle="Connecting to Goals"
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Time Horizon Problem." eyebrow="Step 1" icon={Wind} theme={theme}>
              <p>Why is it so hard to study for a future that feels a million miles away? The science shows that psychological time isn't constant. Your <Highlight description="The extent to which you integrate the future into your present planning. It's a key cognitive resource for long-term goals." theme={theme}>Future Time Perspective (FTP)</Highlight> is a cognitive resource, and it's unequally distributed. Students from unstable environments often develop a rational, short-term "present-fatalistic" focus. This is a survival skill, but it's "maladaptive" for the long-game of education.</p>
              <p>This isn't a character flaw. It's about bridging the gap. The goal is to make the future feel closer and more connected to today's actions. This is a psychological intervention that recruits neural circuitry to override the immediate pressures of disadvantage.</p>
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="The Engine of Motivation." eyebrow="Step 2" icon={Brain} theme={theme}>
              <p><Highlight description="A major theory of human motivation that focuses on the degree to which an individual's behavior is self-motivated and self-determined." theme={theme}>Self-Determination Theory (SDT)</Highlight> explains the fuel for this journey. Motivation runs on a spectrum from "controlled" (doing it to avoid getting in trouble) to "autonomous" (doing it because you value it). The most potent form for academic success is <Highlight description="A type of autonomous motivation where you engage in a task because you personally value its outcome, even if the task itself isn't enjoyable." theme={theme}>Identified Regulation</Highlight>--you've accepted the goal as your own.</p>
              <p>Crucially, research shows that for students from low-income backgrounds, the feeling of connection to the future ONLY works if it triggers these self-regulation strategies. "Dreaming big" is not enough. The dream must be converted into daily habits.</p>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The 'Impossibility' Heuristic." eyebrow="Step 3" icon={Wand2} theme={theme}>
              <p>When does a task feel "worth doing," and when does it feel "impossible"? <Highlight description="A theory stating that we are motivated to act in ways that are congruent with our identities." theme={theme}>Identity-Based Motivation (IBM)</Highlight> theory has the answer. It's about how you interpret difficulty. When a task feels "like me," difficulty is seen as **importance**. ("This is hard, so it must be worth it.") When a task feels alien, difficulty is seen as **impossibility**. ("This is hard, so it's not for people like me.")</p>
              <p>This "impossibility heuristic" is a major barrier for students from disadvantaged backgrounds. The key is to reframe your identity--to see academic struggle not as a sign you don't belong, but as a challenge you are uniquely equipped to handle due to your resilience.</p>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="Hacking the System." eyebrow="Step 4" icon={Briefcase} theme={theme}>
              <p>The Irish education system has real structural barriers, like the "grinds" industry. But it also has powerful structural levers designed to help you. These are not handouts; they are tools to level the playing field. Understanding them is a critical part of your strategy.</p>
              <p>The main levers are the <Highlight description="Higher Education Access Route: A scheme that offers reduced points places to students from socio-economically disadvantaged backgrounds." theme={theme}>HEAR</Highlight> and <Highlight description="Disability Access Route to Education: A scheme that supports students whose education has been impacted by a disability." theme={theme}>DARE</Highlight> schemes, which offer reduced points for college entry, and the <Highlight description="Student Universal Support Ireland: The main financial grant for third-level education in Ireland." theme={theme}>SUSI</Highlight> grant, which provides financial support. Knowing the deadlines and eligibility criteria is not optional; it's part of the curriculum.</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Playbook: The 'Why'." eyebrow="Step 5" icon={Gamepad2} theme={theme}>
              <p>This is where theory becomes action. The first phase is to build your "why"--a Future Time Perspective strong enough to withstand the stress of the exam year. There are two core exercises.</p>
              <p>The first is the <Highlight description="A powerful, four-step goal-setting strategy: Wish, Outcome, Obstacle, Plan. It combines positive thinking with a realistic assessment of barriers." theme={theme}>WOOP Method</Highlight>. It's a scientifically-validated way to connect a long-term goal to your immediate actions. The second is <Highlight description="A brief writing exercise about your core personal values (e.g., family, creativity). It has been proven to buffer the brain against stress and raise grades in low-SES students." theme={theme}>Self-Affirmation Journaling</Highlight>, which acts as a psychological shield against "Stereotype Threat" (the fear that 'people like me' don't succeed).</p>
              <WOOPPlanner />
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="Playbook: The 'How' & 'What'." eyebrow="Step 6" icon={Link2} theme={theme}>
              <p>Once your "Why" is established, you need the "How" and the "What." The "How" is about using high-impact learning techniques that are free and outperform expensive grinds. This means prioritizing <Highlight description="The 'Testing Effect.' Forcing your brain to retrieve information is the single most effective way to build durable memory." theme={theme}>Retrieval Practice</Highlight> ("Brain Dumps") over passive re-reading, and using a <Highlight description="A simple schedule of reviewing material on Day 1, Day 2, Day 7, and Day 30 to move information into long-term memory." theme={theme}>Spaced Repetition</Highlight> schedule.</p>
              <p>The "What" is about using every structural advantage available. You must conduct a **HEAR & DARE Audit** early in 6th year. You must become a **SUSI Maximizer**, checking your distance from college for the "Non-Adjacent" rate. And you must find **Free "Grinds"** through university access programs and high-quality YouTube channels. This is not just studying; it's system hacking.</p>
              <MicroCommitment theme={theme}>
                <p>Go to Google Maps right now. Check the distance from your house to your dream college course. Is it over 30km? You may have just found thousands of euro in extra SUSI funding.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default ConnectingEducationToGoalsModule;
