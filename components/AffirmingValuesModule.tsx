/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import {
  BrainCircuit, Shield, AlertTriangle, UserCheck
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { blueTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = blueTheme;

// --- INTERACTIVE COMPONENTS ---

const ValuesSelector = () => {
    const values = ["Family", "Friendship", "Creativity", "Kindness", "Humour", "Ambition", "Community", "Independence", "Learning"];
    const [selected, setSelected] = useState<string[]>([]);

    const handleSelect = (value: string) => {
        if (selected.includes(value)) {
            setSelected(selected.filter(v => v !== value));
        } else if (selected.length < 3) {
            setSelected([...selected, value]);
        }
    };

    return(
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Core Values Audit</h4>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Select your top 3 most important personal values.</p>
             <div className="flex flex-wrap justify-center gap-3">
                {values.map(value => (
                    <motion.button
                        key={value}
                        onClick={() => handleSelect(value)}
                        className={`px-4 py-2 text-sm font-bold rounded-full border transition-all ${selected.includes(value) ? 'bg-blue-500 text-white border-blue-500' : 'bg-zinc-50 border-zinc-200 dark:border-zinc-700'}`}
                        whileHover={{y: -2}}
                    >
                        {value}
                    </motion.button>
                ))}
             </div>
             {selected.length === 3 && (
                <div className="mt-8">
                    <h5 className="font-bold text-center">Your 15-Minute Writing Prompt:</h5>
                    <p className="p-4 bg-zinc-100 dark:bg-zinc-800 rounded-xl mt-2 text-center text-sm">Choose ONE of these values: <span className="font-bold">{selected.join(', ')}</span>. Write for 15 minutes about why this value is important to you and describe a time when you lived up to it.</p>
                </div>
             )}
        </div>
    );
};

// --- MODULE COMPONENT ---
const AffirmingValuesModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'invisible-threat', title: 'The Invisible Threat', eyebrow: '01 // The Problem', icon: AlertTriangle },
    { id: 'psychological-shield', title: 'The Psychological Shield', eyebrow: '02 // The Solution', icon: Shield },
    { id: 'broaden-build', title: 'How It Works: "Broaden-and-Build"', eyebrow: '03 // The Mechanism', icon: BrainCircuit },
    { id: 'real-world-data', title: 'The Real World Data', eyebrow: '04 // The Evidence', icon: UserCheck },
    { id: 'your-protocol', title: 'Your Pre-Exam Protocol', eyebrow: '05 // The Action Plan', icon: UserCheck },
  ];

  return (
    <ModuleLayout
      moduleNumber="03"
      moduleTitle="Affirming Values"
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Invisible Threat." eyebrow="Step 1" icon={AlertTriangle} theme={theme}>
              <p>In a high-stakes situation like the Leaving Cert, your brain is on high alert for threats. For students from disadvantaged backgrounds, there's an extra, invisible threat in the room: the fear that a poor performance will confirm a negative stereotype about your group. This is called <Highlight description="A situational predicament in which individuals are at risk of confirming negative stereotypes about their social group. This adds extra cognitive load, which can impair performance." theme={theme}>Stereotype Threat</Highlight>.</p>
              <p>It's a cognitive tax. Part of your precious working memory gets hijacked by this background anxiety, leaving less capacity for the actual exam questions. This isn't just "in your head"--it's a measurable physiological stress response that can sabotage your performance, even if you know the material perfectly.</p>
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The Psychological Shield." eyebrow="Step 2" icon={Shield} theme={theme}>
              <p>For decades, psychologists have been searching for a "vaccine" against this threat. The most powerful and replicable intervention is astonishingly simple: a 15-minute writing exercise called <Highlight description="A brief psychological intervention where individuals write about their core personal values. This has been shown to buffer against stress and improve performance in high-pressure situations." theme={theme}>Self-Affirmation</Highlight>.</p>
              <p>It sounds too good to be true, but the data is overwhelming. By taking a few moments before a stressful event to write about what's truly important to you (like family, creativity, or friendship), you create a psychological "shield." You remind your brain that your self-worth is not solely defined by the exam you're about to take. This frees up the cognitive resources that stereotype threat would otherwise steal.</p>
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="How It Works: 'Broaden-and-Build'." eyebrow="Step 3" icon={BrainCircuit} theme={theme}>
              <p>How can a simple writing exercise have such a powerful effect? It's not magic; it's neuroscience. According to Barbara Fredrickson's <Highlight description="A theory in positive psychology that suggests positive emotions (like the feeling of self-worth from an affirmation) broaden a person's mindset and help build their psychological, social, and intellectual resources." theme={theme}>Broaden-and-Build Theory</Highlight>, negative emotions (like fear) narrow your focus to a single threat. Positive emotions, on the other hand, do the opposite: they broaden your perspective.</p>
              <p>When you affirm your core values, you activate brain regions associated with self-processing and reward (like the ventromedial prefrontal cortex). This creates a moment of positive emotion that "zooms out" your perspective. The exam is no longer a life-or-death verdict on your entire identity; it's just one part of a much larger, more meaningful life. This cognitive 'broadening' is what reduces the threat and frees up your working memory.</p>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="The Real World Data." eyebrow="Step 4" icon={UserCheck} theme={theme}>
              <p>In a landmark study by Cohen et al. (2006), they gave a values affirmation exercise to a group of African American middle-school students. The results were staggering. This simple, 15-minute exercise, done just a few times a year, boosted the grades of the students by an average of 0.3 grade points.</p>
              <p>Even more remarkably, two years later, the students who had done the exercise were still outperforming their peers. The intervention had set off a "virtuous cycle"--better grades led to more confidence, which led to even better grades. The effect was most powerful for the students who were most at risk of underperforming. This is one of the most effective psychological interventions ever discovered.</p>
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="Your Pre-Exam Protocol." eyebrow="Step 5" icon={UserCheck} theme={theme}>
              <p>You now have a scientifically-proven tool to protect your brain under pressure. The final step is to turn it into a concrete, pre-exam ritual. Before every major exam (especially the Mocks and the Leaving Cert itself), you will run the Self-Affirmation Protocol.</p>
              <p>The steps are simple: **1. Identify your core values.** **2. Choose the one that feels most important to you right now.** **3. Write for 15 minutes.** This isn't an essay; it's a private reflection. Write about why the value is important and describe a specific time you lived up to it. This isn't a "nice to have"; it's a cognitive warm-up as important as checking your pens.</p>
              <ValuesSelector />
              <MicroCommitment theme={theme}>
                <p>Take the values you selected above. Create a recurring event in your phone's calendar for the morning of every exam you have this year, with the title: "15 Min Values Affirmation." You've just weaponized positive psychology.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default AffirmingValuesModule;
