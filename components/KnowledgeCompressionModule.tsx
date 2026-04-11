/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Target, Brain, SlidersHorizontal, Wrench, Compass, BarChart
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { tealTheme } from '../moduleThemes';
import { Highlight, ReadingSection } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = tealTheme;

// --- INTERACTIVE COMPONENT: SyllabusDeconstructor ---
const mathsSyllabus = {
  subject: "Mathematics (Higher Level)",
  strands: [
    {
      name: "Statistics & Probability",
      topics: [
        { name: "Inferential Statistics", frequency: 5, details: "Focus on hypothesis testing. Often a full long question." },
        { name: "Probability", frequency: 5, details: "High-value topic, frequently combined with other areas." },
        { name: "Descriptive Statistics", frequency: 3, details: "Core skills, but usually part of a larger question." },
      ]
    },
    {
      name: "Geometry & Trigonometry",
      topics: [
        { name: "Trigonometry", frequency: 5, details: "Guaranteed long question. Master 3D problems and proofs." },
        { name: "The Line & Circle", frequency: 4, details: "Essential coordinate geometry skills. Very frequent questions." },
        { name: "Enlargements/Constructions", frequency: 2, details: "Lower frequency, but can be easy marks if prepared." },
      ]
    },
    {
      name: "Functions & Calculus",
      topics: [
        { name: "Differentiation", frequency: 5, details: "The absolute core of Paper 1. Master rules and applications." },
        { name: "Integration", frequency: 5, details: "The other core of Paper 1. Focus on finding areas." },
        { name: "Functions", frequency: 3, details: "Often appears as a context for calculus questions." },
      ]
    },
    {
      name: "Algebra",
      topics: [
        { name: "Core Algebra", frequency: 5, details: "The language of the entire course. Essential for everything." },
        { name: "Sequences & Series", frequency: 4, details: "Predictable question style. Excellent for banking marks." },
      ]
    },
     {
      name: "Number",
      topics: [
        { name: "Complex Numbers", frequency: 4, details: "Very common long question. De Moivre's Theorem is key." },
        { name: "Financial Maths", frequency: 3, details: "Often a full question. Master the formula." },
      ]
    },
  ]
};

const SyllabusDeconstructor = () => {
    const [selectedTopic, setSelectedTopic] = useState<any>(null);

    const totalFrequency = mathsSyllabus.strands.reduce((sum, strand) =>
        sum + strand.topics.reduce((topicSum, topic) => topicSum + topic.frequency, 0), 0);

    const colors = ["#e0f2f1", "#b2dfdb", "#80cbc4", "#4db6ac", "#26a69a"];

    return (
        <div className="my-10 rounded-2xl p-4 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Syllabus Deconstructor</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">{mathsSyllabus.subject}</p>

            <div className="w-full h-[500px] bg-zinc-50 dark:bg-zinc-800/50 rounded-lg p-2 flex flex-col gap-2">
                {mathsSyllabus.strands.map(strand => {
                    const strandTotalFreq = strand.topics.reduce((sum, topic) => sum + topic.frequency, 0);
                    const strandFlex = (strandTotalFreq / totalFrequency) * 100;
                    return (
                        <div key={strand.name} style={{flexGrow: strandFlex}} className="flex gap-2">
                            {strand.topics.map(topic => {
                                const topicFlex = (topic.frequency / strandTotalFreq) * 100;
                                return (
                                    <motion.div
                                        key={topic.name}
                                        style={{flexGrow: topicFlex, backgroundColor: colors[topic.frequency-1]}}
                                        className="rounded-md p-2 text-xs font-bold text-zinc-800 dark:text-white cursor-pointer flex items-center justify-center text-center"
                                        whileHover={{scale: 1.05, zIndex: 10}}
                                        onClick={() => setSelectedTopic(topic)}
                                    >
                                        {topic.name}
                                    </motion.div>
                                );
                            })}
                        </div>
                    );
                })}
            </div>
            <AnimatePresence>
                {selectedTopic && (
                    <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: 10 }}
                        className="mt-4 p-4 rounded-xl" style={{ backgroundColor: '#6EE7B7', border: '2.5px solid #059669', boxShadow: '3px 3px 0px 0px #059669' }}
                    >
                        <h5 className="font-bold" style={{ color: '#064E3B' }}>{selectedTopic.name}</h5>
                        <p className="text-sm mt-1" style={{ color: '#065F46' }}>{selectedTopic.details}</p>
                        <button onClick={() => setSelectedTopic(null)} className="text-xs mt-2" style={{ color: '#047857' }}>Close</button>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};

// --- MODULE COMPONENT ---
const KnowledgeCompressionModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'information-overload', title: 'Information Overload', eyebrow: '01 // The Problem', icon: Target },
    { id: 'pareto-principle', title: 'The 80/20 Rule', eyebrow: '02 // The Principle', icon: SlidersHorizontal },
    { id: 'syllabus-deconstructor', title: 'The Syllabus Deconstructor', eyebrow: '03 // The Tool', icon: Compass },
    { id: 'distillation-techniques', title: 'Distillation Techniques', eyebrow: '04 // The Methods', icon: Brain },
    { id: 'high-yield-assets', title: 'High-Yield Assets', eyebrow: '05 // The Output', icon: BarChart },
    { id: 'implementation', title: 'Your Triage Plan', eyebrow: '06 // The Action Plan', icon: Wrench },
  ];

  return (
    <ModuleLayout
      moduleNumber="06"
      moduleTitle="Knowledge Compression"
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Information Overload." eyebrow="Step 1" icon={Target} theme={theme}>
              <p>You have the best study techniques in the world. But now you face a new problem: there's too much stuff to study. A typical Leaving Cert subject has hundreds of potential topics. Trying to learn everything equally is a recipe for burnout and shallow knowledge. It's like trying to drink from a firehose.</p>
              <p>The goal is not to cover everything; it's to cover the <em>right</em> things. To do this, you need to stop thinking like a student and start thinking like a strategic analyst. You need a system for <Highlight description="The process of sorting information based on its importance and urgency to prioritize your attention and effort." theme={theme}>Information Triage</Highlight>.</p>
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="The 80/20 Rule." eyebrow="Step 2" icon={SlidersHorizontal} theme={theme}>
              <p>The core principle of information triage is the <Highlight description="Also known as the Pareto Principle. It states that for many events, roughly 80% of the effects come from 20% of the causes. In studying, this means 80% of your marks will come from 20% of the syllabus." theme={theme}>80/20 Rule</Highlight>. Not all topics are created equal. A small number of "high-yield" topics consistently deliver the vast majority of the marks on the exam papers year after year.</p>
              <p>Your job is to identify this "vital few" and ruthlessly prioritize them. This isn't about ignoring the rest of the syllabus. It's about allocating your most precious resource--your focused attention--where it will have the biggest impact. This is the difference between being busy and being effective.</p>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The Syllabus Deconstructor." eyebrow="Step 3" icon={Compass} theme={theme}>
              <p>To find the 20%, you need data. The <Highlight description="A visual tool that breaks down a syllabus into its core topics and uses historical exam data to assign a 'frequency score' to each, revealing the high-yield areas." theme={theme}>Syllabus Deconstructor</Highlight> is an interactive tool that does this for you. By analyzing years of past papers, we can map out the "hot zones" of the curriculum.</p>
              <p>This tool transforms the syllabus from a long, intimidating list into a strategic map. It shows you where the 'big game' is, allowing you to plan your 'hunt' accordingly. We'll start with Maths, one of the most predictable exams on the schedule.</p>
              <SyllabusDeconstructor />
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="Distillation Techniques" eyebrow="Step 4" icon={Brain} theme={theme}>
              <p>This section is under construction. Future content will explore techniques like concept mapping, the Feynman technique, and creating one-page summaries to distill complex information into memorable, high-yield assets.</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="High-Yield Assets" eyebrow="Step 5" icon={BarChart} theme={theme}>
              <p>This section is under construction. Future content will guide you on how to turn your distilled knowledge into powerful revision tools like summary sheets, flashcards, and mind maps that are optimized for active recall.</p>
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="Your Triage Plan" eyebrow="Step 6" icon={Wrench} theme={theme}>
              <p>This section is under construction. Future content will provide a framework for creating a personalized study plan based on your own syllabus deconstruction, helping you allocate your time and energy for maximum point-scoring efficiency.</p>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default KnowledgeCompressionModule;
