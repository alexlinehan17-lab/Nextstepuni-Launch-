/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Cpu, Zap, Shield, Moon, Utensils, ClipboardList, Flag, Brain } from 'lucide-react';
import { ModuleProgress } from '../types';
import { skyTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = skyTheme;

// --- INTERACTIVE COMPONENTS ---
const CognitionShiftVisualizer = () => {
    const [isHot, setIsHot] = useState(false);
    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-semibold text-stone-800 text-center italic">Hot vs. Cold Cognition</h4>
             <p className="text-center text-sm text-stone-500 mb-8">Click the button to simulate what happens to your brain under exam stress.</p>
             <div className="flex justify-center items-center gap-4">
                <div className="text-center">
                    <motion.div animate={{opacity: isHot ? 0.3 : 1}}><Brain size={48} className="text-blue-500 mx-auto"/></motion.div>
                    <p className="font-bold text-sm mt-2">PFC (Cold)</p>
                </div>
                <div className="w-24 text-center">&harr;</div>
                <div className="text-center">
                     <motion.div animate={{opacity: isHot ? 1 : 0.3}}><Zap size={48} className="text-rose-500 mx-auto"/></motion.div>
                     <p className="font-bold text-sm mt-2">Amygdala (Hot)</p>
                </div>
             </div>
             <div className="text-center mt-6">
                <button onClick={() => setIsHot(!isHot)} className="px-4 py-2 bg-rose-500 text-white font-bold text-sm rounded-lg">{isHot ? 'De-escalate Threat' : 'Trigger Threat'}</button>
             </div>
        </div>
    );
};

const PhysiologicalSighGuide = () => (
    <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl text-center">
         <h4 className="font-serif text-2xl font-semibold text-stone-800 text-center italic">The Physiological Sigh</h4>
         <p className="text-sm text-stone-500 mb-6">Your emergency brake for acute panic. Repeat 3 times.</p>
         <div className="flex justify-center items-center gap-8">
            <motion.div initial={{scale:0.5}} animate={{scale:[1, 1, 0.5, 0.5]}} transition={{duration:6, repeat: Infinity, times:[0, 0.4, 0.5, 1]}} className="w-20 h-20 rounded-full bg-sky-300 flex items-center justify-center font-bold">Inhale 1</motion.div>
            <motion.div initial={{scale:0.5}} animate={{scale:[0.5, 1, 0.5, 0.5]}} transition={{duration:6, repeat: Infinity, times:[0, 0.4, 0.5, 1]}} className="w-16 h-16 rounded-full bg-sky-300 flex items-center justify-center font-bold">Inhale 2</motion.div>
            <motion.div initial={{scale:1}} animate={{scale:[1, 1, 0.5, 1]}} transition={{duration:6, repeat: Infinity, times:[0, 0.5, 0.9, 1]}} className="w-24 h-24 rounded-full bg-sky-500 text-white flex items-center justify-center font-bold">Exhale</motion.div>
         </div>
    </div>
);

// --- MODULE COMPONENT ---
const ExamCrisisManagementModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'anatomy-of-blank', title: 'The Anatomy of "Going Blank"', eyebrow: '01 // Hot vs. Cold Cognition', icon: Cpu },
    { id: 'blank-mind-protocol', title: 'The "Blank Mind" Protocol', eyebrow: '02 // Physiological Interventions', icon: Zap },
    { id: 'social-containment', title: 'Social Containment', eyebrow: '03 // The Post-Mortem Ban', icon: Shield },
    { id: 'cognitive-athlete-sleep', title: 'The Cognitive Athlete: Sleep', eyebrow: '04 // Sleep Architecture', icon: Moon },
    { id: 'cognitive-athlete-nutrition', title: 'The Cognitive Athlete: Nutrition', eyebrow: '05 // Bio-Optimization', icon: Utensils },
    { id: 'crisis-planning', title: 'Crisis Planning: The WRAP', eyebrow: '06 // The Pre-Planned Protocol', icon: ClipboardList },
    { id: 'implementation', title: 'The 7-Day Taper', eyebrow: '07 // The Implementation Guide', icon: Flag },
  ];

  return (
    <ModuleLayout
      moduleNumber="04"
      moduleTitle="Exam Crisis Management"
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="Anatomy of 'Going Blank'." eyebrow="Step 1" icon={Cpu} theme={theme}>
              <p>Going "blank" in an exam isn't you being stupid or unprepared. It's a physiological crisis. It's a neurochemical event where your brain's alarm system hijacks its command centre. To beat it, you need to understand the two states your brain operates in: <Highlight description="Your calm, logical state. Your Prefrontal Cortex (PFC) is in charge, allowing for clear thinking and easy memory retrieval." theme={theme}>Cold Cognition</Highlight> and <Highlight description="Your stressed, survival state. Your Amygdala (threat detector) takes over, shutting down the PFC and blocking access to memory." theme={theme}>Hot Cognition</Highlight>.</p>
              <p>When you see a question you don't know, your brain can perceive it as a threat. This triggers an <Highlight description="The moment your emotional Amygdala hijacks your rational Prefrontal Cortex, flooding your system with stress hormones like cortisol and cutting the 'phone lines' to your memory." theme={theme}>Amygdala Hijack</Highlight>, switching you from "cold" to "hot" cognition. Your memory isn't gone; the connection is just temporarily offline. This isn't a knowledge problem; it's a hardware problem.</p>
              <CognitionShiftVisualizer />
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The 'Blank Mind' Protocol." eyebrow="Step 2" icon={Zap} theme={theme}>
                <p>Since the problem is physiological, the solution must be physiological. You can't "think" your way out of a panic because the thinking part of your brain is offline. You need to use your body to send a "safety" signal to your brain. This is called <Highlight description="Using bodily sensations and actions (like breathing) to influence your mental and emotional state, rather than trying to think your way calm." theme={theme}>bottom-up processing</Highlight>.</p>
                <p>The fastest way to do this is the <Highlight description="An emergency breathing technique (two inhales, one long exhale) that re-inflates collapsed air sacs in your lungs, rapidly offloading CO2 and forcing your nervous system to calm down." theme={theme}>Physiological Sigh</Highlight>. It's your "hard reset" button. Once the initial chemical flood is stopped, you re-engage your PFC with a <Highlight description="The 5-4-3-2-1 technique of naming things you can see, feel, hear, smell, and taste. It forces your brain to process external sensory data, pulling it out of the internal panic loop." theme={theme}>Sensory Grounding</Highlight> exercise. Finally, you restart your cognitive engine with an <Highlight description="Deliberately finding the easiest possible question on the paper to answer. This micro-success triggers a small release of dopamine, which helps clear the cortisol 'fog' from your PFC." theme={theme}>'Easy Win'</Highlight>.</p>
                <PhysiologicalSighGuide/>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="Social Containment." eyebrow="Step 3" icon={Shield} theme={theme}>
              <p>The crisis doesn't end when you put your pen down. The minutes after an exam are a minefield of <Highlight description="The contagious spread of anxiety through a peer group, often triggered by post-exam 'post-mortems.'" theme={theme}>Anxiety Contagion</Highlight>. Discussing answers with stressed-out friends is one of the worst things you can do. It elevates your cortisol levels, preventing the physiological recovery you need for the next exam.</p>
              <p>This urge to compare answers is driven by a powerful psychological force called the <Highlight description="A psychological desire for a firm answer to a question and an aversion to ambiguity. The uncertainty of an exam result creates a cognitive 'open loop' that the brain desperately wants to close." theme={theme}>Need for Cognitive Closure (NFC)</Highlight>. You have to train the discipline to leave that loop open. This requires a strict <Highlight description="A personal rule to immediately exit the exam hall and avoid all discussion of the exam until the entire exam period is over." theme={theme}>"Post-Mortem Ban"</Highlight>. This isn't anti-social; it's a professional strategy to manage your mental stamina.</p>
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="The Cognitive Athlete: Sleep." eyebrow="Step 4" icon={Moon} theme={theme}>
              <p>You must treat the weeks before the Leaving Cert like a championship season. You are a <Highlight description="A model that treats academic performance like an athletic event, focusing on physiological optimization (sleep, nutrition) to maximize cognitive output." theme={theme}>Cognitive Athlete</Highlight>, and your brain is your primary muscle. Sleep is your most important training tool.</p>
              <p>In the week before exams, you should engage in <Highlight description="The strategy of extending sleep duration in the days leading up to a period of sleep restriction to build a 'cognitive reserve' and mitigate the negative effects." theme={theme}>Sleep Banking</Highlight>--getting an extra hour of sleep per night. This builds a cognitive reserve that has been proven to protect against the effects of later sleep loss. During sleep, your brain also activates the <Highlight description="The brain's unique cleaning system, where cerebrospinal fluid flushes out metabolic waste products like adenosine that accumulate during waking hours and cause 'brain fog.'" theme={theme}>Glymphatic System</Highlight>, clearing out the toxins that impair focus.</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="The Cognitive Athlete: Nutrition." eyebrow="Step 5" icon={Utensils} theme={theme}>
              <p>Your brain runs on glucose, but it needs a steady supply, not a sugar rush. High <Highlight description="Foods that are rapidly digested, causing a quick spike and then a crash in blood sugar levels (e.g., sugary snacks, white bread)." theme={theme}>Glycemic Index (GI)</Highlight> foods cause a "crash" that coincides with the middle of an exam. Your pre-exam meal should be low-GI complex carbs and protein 3 hours before.</p>
              <p>To maximize your alertness on the day, you can use caffeine strategically. <Highlight description="The process of gradually reducing caffeine intake in the 7-10 days before an exam to re-sensitize your brain's adenosine receptors." theme={theme}>Caffeine Tapering</Highlight> means a normal cup of coffee on exam day will have a much more powerful effect. Pairing it with L-Theanine (found in tea) can create "calm focus" without the jitters.</p>
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="Crisis Planning: The WRAP." eyebrow="Step 6" icon={ClipboardList} theme={theme}>
              <p>Elite performers don't just react to crises; they plan for them. The <Highlight description="The Wellness Recovery Action Plan is a structured system for identifying your personal triggers and creating a pre-planned response to a crisis." theme={theme}>WRAP Framework</Highlight> is a tool for doing just that. It moves you from a state of panic to executing a pre-planned protocol.</p>
              <p>Your Academic WRAP has four parts. **1. Daily Maintenance:** What do you need to do every day to stay well? **2. Triggers:** What external events throw you off? **3. Early Warning Signs:** What are your internal signals of rising stress? **4. Crisis Plan:** Your "Break Glass" protocol for a full-blown panic attack. By writing this down *before* the crisis, you outsource the decision-making to your calm, rational self.</p>
            </ReadingSection>
          )}
          {activeSection === 6 && (
            <ReadingSection title="The 7-Day Taper." eyebrow="Step 7" icon={Flag} theme={theme}>
              <p>This is where it all comes together. The final week before the exams is your "Taper." Just like an athlete, you reduce the training load to allow your body and mind to recover and peak at the right moment. This is not the time for cramming.</p>
              <p>Your 7-day taper should include: **Caffeine Resensitization** (T-7 days), **Circadian Entrainment** (T-5 days, waking up at exam time), and **Nutritional Priming** (T-3 days, shifting to low-GI foods and hyper-hydrating). The day before the exam, you stop all heavy study. You are no longer building knowledge; you are preparing the machine that will deploy it.</p>
              <MicroCommitment theme={theme}>
                <p>Take out your calendar. Find the date one week before your first exam. Create an event called "Begin 7-Day Taper." You've just taken the first step to becoming a Cognitive Athlete.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default ExamCrisisManagementModule;
