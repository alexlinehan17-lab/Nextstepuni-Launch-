/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  BookOpen, PenSquare, MessageSquare, BarChart, BrainCircuit, Mic, Settings
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { blueTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = blueTheme;

// --- INTERACTIVE COMPONENTS ---
const PCLMGrader = () => {
    const [pclm, setPclm] = useState({ p: 50, c: 50, l: 50, m: 50 });

    // P caps C and L
    const cappedC = Math.min(pclm.c, pclm.p);
    const cappedL = Math.min(pclm.l, pclm.p);

    const total = (pclm.p * 0.3) + (cappedC * 0.3) + (cappedL * 0.3) + (pclm.m * 0.1);
    const grade = total >= 90 ? 'H1' : total >= 80 ? 'H2' : total >= 70 ? 'H3' : 'H4';

    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">PCLM Grader</h4>
            <div className="grid grid-cols-2 gap-6 items-center">
                <div className="space-y-2">
                    <input type="range" value={pclm.p} onChange={e => setPclm({...pclm, p: parseInt(e.target.value)})} className="w-full"/>
                    <input type="range" value={pclm.c} onChange={e => setPclm({...pclm, c: parseInt(e.target.value)})} className="w-full"/>
                    <input type="range" value={pclm.l} onChange={e => setPclm({...pclm, l: parseInt(e.target.value)})} className="w-full"/>
                    <input type="range" value={pclm.m} onChange={e => setPclm({...pclm, m: parseInt(e.target.value)})} className="w-full"/>
                </div>
                <div className="text-center">
                    <p className="text-6xl font-semibold text-blue-500">{grade}</p>
                </div>
            </div>
        </div>
    );
};

// --- MODULE COMPONENT ---
const MasteringEnglishModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'pclm-blueprint', title: 'The PCLM Blueprint', eyebrow: '01 // The Marking Scheme', icon: Settings },
    { id: 'paper1-engine', title: 'Paper 1: The Engine of Grades', eyebrow: '02 // Language & Comprehension', icon: BookOpen },
    { id: 'composing', title: 'Paper 1: The 100-Mark Essay', eyebrow: '03 // Composing', icon: PenSquare },
    { id: 'single-text', title: 'Paper 2: The Single Text', eyebrow: '04 // Macbeth 2026', icon: MessageSquare },
    { id: 'comparative-study', title: 'Paper 2: The Comparative Study', eyebrow: '05 // The Modes', icon: BarChart },
    { id: 'poetry', title: 'Paper 2: Prescribed Poetry', eyebrow: '06 // The "Big 4" Rule', icon: Mic },
    { id: 'toolkit', title: 'The Strategic Toolkit', eyebrow: '07 // High-Yield Strategies', icon: BrainCircuit },
  ];

  return (
    <ModuleLayout
      moduleNumber="04"
      moduleTitle="Mastering English"
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The PCLM Blueprint." eyebrow="Step 1" icon={Settings} theme={theme}>
              <p>The Leaving Cert English exam is not subjective. It is governed by a strict, unified marking scheme: <Highlight description="The four criteria for marking English: Purpose (30%), Coherence (30%), Language (30%), and Mechanics (10%)." theme={theme}>PCLM</Highlight>. Understanding this blueprint is the single most significant differentiator between a H3 and a H1.</p>
              <p><Highlight description="Did you answer the specific question asked? This is the most important criterion." theme={theme}>Purpose</Highlight> is king. A brilliant essay that is irrelevant is worthless. Crucially, your marks for Coherence and Language are *capped* by your Purpose mark. You must prioritize relevance above all else.</p>
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="Paper 1: Engine of Grades." eyebrow="Step 2" icon={BookOpen} theme={theme}>
              <p>Paper 1 is 50% of your total grade and the most reliable place to secure marks. Question A tests comprehension and analysis. The 20-mark "Style/Technique" question is where the H1 is won or lost. You must go beyond listing techniques and explain their *effect* on the reader.</p>
              <p>Question B, the Functional Writing task, is a "hidden trap." You must adhere strictly to the conventions of the requested genre (e.g., letter, blog post). Writing a personal essay in the wrong format is a fatal error for your 'P' mark.</p>
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="The 100-Mark Essay." eyebrow="Step 3" icon={PenSquare} theme={theme}>
              <p>The Composing section is worth 25% of your total grade. The Personal Essay is the most popular but most poorly executed. It is not just a story; it must be a <Highlight description="An exploration of how an event felt, what was learned, and how the writer changed as a result." theme={theme}>reflective piece</Highlight>. "Show, don't tell" is the golden rule.</p>
              <p>The Short Story is high-risk, high-reward. Focus on a single incident and a short timeframe. The Discursive Essay requires a balanced exploration of an issue, while the Persuasive Essay demands a firm stance and the use of rhetorical devices.</p>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="Paper 2: Single Text (Macbeth)." eyebrow="Step 4" icon={MessageSquare} theme={theme}>
               <p>For 2026, the prescribed Shakespearean text is Macbeth. A H1 analysis requires you to discuss the interconnectedness of themes, character, and imagery. The core themes are: <Highlight description="It's not just about wanting power; it's about the moral cost of that want." theme={theme}>Ambition and its Corrupting Influence</Highlight>, Kingship vs. Tyranny, The Supernatural and Fate, and Appearance vs. Reality.</p>
               <p>Character analysis should focus on trajectories. Macbeth devolves from "brave Macbeth" to a nihilistic "butcher." Lady Macbeth follows a reverse trajectory, from ruthless resolve to collapse under the weight of repressed guilt.</p>
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="The Comparative Study." eyebrow="Step 5" icon={BarChart} theme={theme}>
                <p>For Higher Level 2026, the three comparative modes are <strong>Cultural Context</strong>, <strong>General Vision and Viewpoint (GVV)</strong>, and <strong>Literary Genre</strong>. Crucially, "Theme or Issue" is NOT a mode for Higher Level. Preparing it is a catastrophic waste of time.</p>
                <p>The key to a H1 is a link-heavy structure. Avoid discussing your texts sequentially. Instead, weave them together in each paragraph, comparing and contrasting them based on the mode. The <Highlight description="A study technique where you identify 4-5 key moments in each text that can be flexibly applied to any of the comparative modes." theme={theme}>"Key Moment" Matrix</Highlight> is the most effective way to prepare for this.</p>
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="Prescribed Poetry." eyebrow="Step 6" icon={Mic} theme={theme}>
              <p>The <Highlight description="The mathematical reality that to guarantee one of your studied poets appears on the paper (where 4 out of 8 are examined), you must study 5 poets thoroughly." theme={theme}>"Big 4+1" Rule</Highlight> is non-negotiable. To guarantee a poet you've studied appears, you must master five poets. H1 answers must balance a discussion of the poet's themes (substance) with an analysis of their style (how they say it).</p>
            </ReadingSection>
          )}
           {activeSection === 6 && (
            <ReadingSection title="The Strategic Toolkit." eyebrow="Step 7" icon={BrainCircuit} theme={theme}>
              <p>High-yield strategies can transform your performance. Use the <Highlight description="A time-saving technique where you read the questions first, assign a color to each, and then highlight relevant quotes as you read the text." theme={theme}>'Index Margining'</Highlight> technique for Paper 1 Comprehension. Prioritize <Highlight description="Short phrases (3-5 words) that fit grammatically into your own sentences, which are far superior to long, clunky block quotes." theme={theme}>Embedded Quotes</Highlight> over long block quotes. And above all, adhere to a strict time management protocol for both papers.</p>
               <MicroCommitment theme={theme}>
                <p>For your next practice essay, perform a PCLM audit. Go through with four different highlighters and mark where you have demonstrated Purpose, Coherence, Language, and good Mechanics. This will reveal your weaknesses.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default MasteringEnglishModule;
