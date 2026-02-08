
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Cpu, Moon, Coffee, Droplet, ListChecks, FlaskConical, CheckCircle2
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { slateTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = slateTheme;

// --- INTERACTIVE COMPONENTS ---
const CognitiveBaselineChecklist = () => {
    const [checks, setChecks] = useState<{ [key: string]: boolean }>({});
    const toggleCheck = (key: string) => setChecks(prev => ({ ...prev, [key]: !prev[key] }));

    const items = [
        { key: 'sleep', label: '9h 15m Time in Bed', details: 'The minimum to get ~8.5h of actual sleep.' },
        { key: 'consistency', label: '<60 min sleep variation', details: 'Avoid "Social Jetlag" between weekdays and weekends.' },
        { key: 'hydration', label: '~8-11 Cups of Water', details: 'Approx. 2-2.5 litres daily. Sip consistently, as thirst is a delayed signal.' },
        { key: 'breakfast', label: 'Low-GI Breakfast', details: 'Avoid sugary cereals/toast. Choose oats, eggs, or protein.' },
        { key: 'detox', label: '1 hour digital detox pre-bed', details: 'Blue light delays sleep and reduces sleep quality.' },
    ];

    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-semibold text-stone-800 text-center italic">My Cognitive Baseline Checklist</h4>
             <p className="text-center text-sm text-stone-500 mb-8">This isn't a "nice to have" list. This is the biological minimum for high performance.</p>
             <div className="space-y-4">
                {items.map(item => (
                    <div key={item.key} onClick={() => toggleCheck(item.key)} className={`p-4 rounded-2xl border-2 flex items-center gap-4 cursor-pointer transition-all ${checks[item.key] ? 'bg-emerald-50 border-emerald-300' : 'bg-stone-50 border-stone-200'}`}>
                        <div className={`w-8 h-8 rounded-full flex items-center justify-center text-white ${checks[item.key] ? 'bg-emerald-500' : 'bg-stone-300'}`}>
                            {checks[item.key] && <CheckCircle2 size={16} />}
                        </div>
                        <div>
                            <p className="font-bold">{item.label}</p>
                            <p className="text-xs text-stone-500">{item.details}</p>
                        </div>
                    </div>
                ))}
             </div>
        </div>
    );
};

// --- MODULE COMPONENT ---
const TheCognitiveBaselineModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'command-centre', title: 'The Command Centre', eyebrow: '01 // The Fragile PFC', icon: Cpu },
    { id: 'sleep-debt-crisis', title: 'The Sleep Debt Crisis', eyebrow: '02 // Intoxication Equivalence', icon: Moon },
    { id: 'sugar-crash', title: 'The Sugar Crash', eyebrow: '03 // Reactive Hypoglycemia', icon: Coffee },
    { id: 'vicious-cycle', title: 'The Vicious Cycle', eyebrow: '04 // Sleep & Sugar', icon: Droplet },
    { id: 'cognitive-baseline', title: 'The Cognitive Baseline', eyebrow: '05 // The Checklist', icon: ListChecks },
    { id: 'self-experiment', title: 'The Self-Experiment', eyebrow: '06 // Feel The Data', icon: FlaskConical },
  ];

  return (
    <ModuleLayout
      moduleNumber="08"
      moduleTitle="The Cognitive Baseline"
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Command Centre." eyebrow="Step 1" icon={Cpu} theme={theme}>
              <p>Your brain's <Highlight description="The 'CEO' of your brain, located behind your forehead. It's responsible for working memory, inhibitory control, and complex decision-making. It's the last part of the brain to fully mature." theme={theme}>Prefrontal Cortex (PFC)</Highlight> is your academic command centre. It's what allows you to hold a complex Maths problem in your head or structure an English essay. During your teenage years, this area is undergoing a massive renovation, making it incredibly powerful but also uniquely vulnerable.</p>
              <p>When deprived of sleep or stable energy, your brain doesn't just get 'tired'. It performs a ruthless triage, functionally decoupling your 'rational' PFC from your 'emotional' <Highlight description="The brain's primitive fear and emotion centre. Without the PFC's inhibitory control, the amygdala can become hyperactive, leading to emotional volatility and anxiety." theme={theme}>amygdala</Highlight>. You're not just sleepy; you're neurologically predisposed to anxiety and poor decision-making. Your hardware is compromised.</p>
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The Sleep Debt Crisis." eyebrow="Step 2" icon={Moon} theme={theme}>
              <p>The biggest myth in student culture is that you can "get used to" less sleep. The data is clear: you can't. While you might stop *feeling* sleepy, your cognitive performance continues to plummet. A landmark study found that after a week of just 5 hours' sleep, students' working memory accuracy dropped by a catastrophic 17%--enough to turn an A into a C.</p>
              <p>Worse, "weekend catch-up" is a myth. Two nights of recovery sleep are not enough to restore your executive functions. This creates a compounding "sleep debt." The most shocking finding is the <Highlight description="The scientifically established fact that after 17-19 hours of wakefulness, your cognitive impairment is equivalent to having a Blood Alcohol Concentration (BAC) of 0.05%." theme={theme}>Intoxication Equivalence</Highlight>: if you wake up at 6 AM, by 11 PM you are functionally as impaired as someone who is legally drunk.</p>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The Sugar Crash." eyebrow="Step 3" icon={Coffee} theme={theme}>
              <p>If sleep is your brain's maintenance crew, glucose is its fuel. Your adolescent brain consumes glucose at a much higher rate than an adult's, making it extremely sensitive to fuel shortages. A high-sugar breakfast (sugary cereal, white toast) causes a rapid spike in blood glucose, followed by an aggressive insulin response that leads to a "crash" 90-120 minutes later.</p>
              <p>This crash, known as <Highlight description="A state of low blood sugar that occurs after a high-glycemic meal. In adolescents, it coincides with late morning classes and causes significant drops in attention and processing speed." theme={theme}>Reactive Hypoglycemia</Highlight>, is a cognitive disaster. It hits right in the middle of your 3rd or 4th class, resulting in slower processing speeds and higher error rates. You are literally "running on fumes" during critical learning hours.</p>
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="The Vicious Cycle." eyebrow="Step 4" icon={Droplet} theme={theme}>
                <p>Sleep and nutrition are not separate issues. They are locked in a vicious feedback loop. Sleep loss disrupts the hormones that regulate hunger, making you biologically crave high-calorie, high-carbohydrate foods. You wake up tired, so you're primed to choose the sugary cereal over the eggs.</p>
                <p>That high-sugar food then disrupts your sleep. The blood glucose fluctuations can interfere with Slow Wave Sleep (SWS), the deep sleep stage crucial for memory consolidation. So, poor sleep leads to poor diet, which leads to even poorer sleep. Over a semester, this cycle cumulatively erodes your brain's executive function.</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="The Cognitive Baseline." eyebrow="Step 5" icon={ListChecks} theme={theme}>
                <p>High academic performance is not just about effort; it's about ensuring your biological hardware is running correctly. The "Minimum Effective Doses" for sleep, hydration, and nutrition are not suggestions; they are biological requirements. Below is the evidence-based checklist for your cognitive baseline. Your mission is to treat this not as an ideal, but as the absolute, non-negotiable foundation for your work.</p>
                <CognitiveBaselineChecklist />
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="The Self-Experiment." eyebrow="Step 6" icon={FlaskConical} theme={theme}>
              <p>To truly understand the impact of nutrition, you need to feel the data yourself. The "Sugar Crash" self-experiment is a simple way to demonstrate the cognitive cost of a high-sugar breakfast compared to a low-sugar, high-protein alternative.</p>
              <p>The protocol is simple. For two consecutive days, you will eat a different breakfast and record how you feel during your 10:30 AM class. This allows you to experience the reality of reactive hypoglycemia and makes the abstract data of the research tangible. This isn't just an experiment; it's you taking control of your own biology.</p>
              <MicroCommitment theme={theme}>
                <p><strong>Day 1:</strong> Eat a high-sugar breakfast (sugary cereal, fruit juice, white toast). At 10:30 AM, rate your energy and focus from 1-10.</p>
                <p><strong>Day 2:</strong> Eat a low-sugar, high-protein breakfast (eggs, oatmeal, yogurt). At 10:30 AM, rate your energy and focus from 1-10. Compare the results.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default TheCognitiveBaselineModule;
