
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  BarChart3, BrainCircuit, XCircle, Share2, HeartPulse, Wrench, Check, X
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { indigoTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = indigoTheme;

// --- INTERACTIVE COMPONENTS ---
const StrengthMeter = () => {
    const [method, setMethod] = useState<'passive'|'active'|null>(null);
    let retrieval = 10, storage = 10;
    if (method === 'passive') { retrieval = 90; storage = 15; }
    if (method === 'active') { retrieval = 40; storage = 85; }

    return(
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Storage vs. Retrieval Strength</h4>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Choose a study method to see its effect on your memory.</p>
             <div className="grid grid-cols-2 gap-4 mb-8">
                <div className="text-center">
                    <p className="font-bold text-sm text-fuchsia-600 mb-2">Retrieval Strength (Feeling)</p>
                    <div className="w-full h-6 bg-zinc-100 dark:bg-zinc-800 rounded-full"><motion.div className="h-full bg-fuchsia-500 rounded-full" initial={{width: "10%"}} animate={{width: `${retrieval}%`}} /></div>
                </div>
                <div className="text-center">
                    <p className="font-bold text-sm text-indigo-600 mb-2">Storage Strength (Learning)</p>
                    <div className="w-full h-6 bg-zinc-100 dark:bg-zinc-800 rounded-full"><motion.div className="h-full bg-indigo-500 rounded-full" initial={{width: "10%"}} animate={{width: `${storage}%`}} /></div>
                </div>
            </div>
             <div className="flex justify-center gap-4">
                <button onClick={() => setMethod('passive')} className="px-4 py-2 bg-fuchsia-100 text-fuchsia-800 text-xs font-bold rounded-lg">Passive Review</button>
                <button onClick={() => setMethod('active')} className="px-4 py-2 bg-indigo-100 text-indigo-800 text-xs font-bold rounded-lg">Active Recall</button>
             </div>
        </div>
    );
};

const StudyMethodAuditor = () => {
    const methods = [
        { id: 1, name: "Re-reading your notes", type: "passive", explanation: "This feels productive because it increases fluency, but it's a weak signal for long-term memory. It's the classic 'Illusion of Competence'." },
        { id: 2, name: "Doing a past paper", type: "active", explanation: "This is a gold-standard active recall method. The struggle to retrieve information is exactly what builds strong, durable memory." },
        { id: 3, name: "Highlighting a textbook", type: "passive", explanation: "This is a form of passive review. It involves selecting information but doesn't require you to retrieve it from memory, so learning is minimal." },
        { id: 4, name: "Explaining it to a friend", type: "active", explanation: "Excellent! To teach something, you must first retrieve it and organize it coherently. This is a very powerful form of active recall." },
        { id: 5, name: "Watching a YouTube video", type: "passive", explanation: "Like re-reading, this is passive consumption. While useful for first-pass understanding, it doesn't build memory unless you actively test yourself on it afterwards." },
        { id: 6, name: "Creating flashcards", type: "active", explanation: "This is active recall IF you make them from memory. If you just copy from the book, it's passive. The real power comes from testing yourself with them later." },
    ];
    const [selectedId, setSelectedId] = useState<number | null>(null);
    const selectedMethod = methods.find(m => m.id === selectedId);

    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Study Method Auditor</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Click a study method to get your Active Recall rating.</p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {methods.map(method => (
                    <button
                        key={method.id}
                        onClick={() => setSelectedId(method.id)}
                        className={`p-4 rounded-xl text-sm font-bold border transition-all ${selectedId === method.id ? 'bg-zinc-200 border-zinc-300' : 'bg-zinc-50 hover:bg-zinc-100 dark:hover:bg-zinc-700 border-zinc-200 dark:border-zinc-700'}`}
                    >
                        {method.name}
                    </button>
                ))}
            </div>
            <AnimatePresence>
                {selectedMethod && (
                    <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: 10 }}
                        className={`mt-6 p-4 rounded-xl border ${selectedMethod.type === 'active' ? 'bg-emerald-50 border-emerald-200' : 'bg-rose-50 border-rose-200'}`}
                    >
                        <div className="flex items-center gap-3">
                            <div className={`w-10 h-10 rounded-full flex items-center justify-center text-white ${selectedMethod.type === 'active' ? 'bg-emerald-500' : 'bg-rose-500'}`}>
                                {selectedMethod.type === 'active' ? <Check size={20}/> : <X size={20}/>}
                            </div>
                            <div>
                                <h5 className={`font-bold ${selectedMethod.type === 'active' ? 'text-emerald-800' : 'text-rose-800'}`}>
                                    {selectedMethod.type === 'active' ? 'Active Recall' : 'Passive Review'}
                                </h5>
                                <p className="text-xs mt-1">{selectedMethod.explanation}</p>
                            </div>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};


// --- MODULE COMPONENT ---
const MasteringActiveRecallModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'great-forgetting', title: 'The Great Forgetting', eyebrow: '01 // The Problem', icon: BarChart3 },
    { id: 'test-effect', title: 'The "Test Effect"', eyebrow: '02 // The Mechanism', icon: BrainCircuit },
    { id: 'dropout-fallacy', title: 'The "Dropout" Fallacy', eyebrow: '03 // The Common Mistake', icon: XCircle },
    { id: 'transfer-effect', title: 'Beyond Rote Memory', eyebrow: '04 // The Transfer Effect', icon: Share2 },
    { id: 'anxiety-myth', title: 'The Anxiety Myth', eyebrow: '05 // The Surprising Truth', icon: HeartPulse },
    { id: 'recall-toolkit', title: 'Your Recall Toolkit', eyebrow: '06 // The Action Plan', icon: Wrench },
  ];

  return (
    <ModuleLayout moduleNumber="01" moduleTitle="Mastering Active Recall" moduleSubtitle="The Test Effect Protocol" moduleDescription={`Go beyond "practice testing" and learn the science of why active retrieval is the single most effective way to build durable, long-term memory.`} theme={theme} sections={sections} onBack={onBack} progress={progress} onProgressUpdate={onProgressUpdate}>
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Great Forgetting." eyebrow="Step 1" icon={BarChart3} theme={theme}>
              <p>In the last module, we saw that passive review (like re-reading) feels good but leads to poor long-term memory. This isn't a small effect; it's a catastrophic failure. The data from Roediger & Karpicke (2006) showed a classic "crossover interaction": while re-reading was slightly better after 5 minutes, it led to a near-total memory collapse after one week compared to active testing.</p>
              <p>This is the harsh reality of the <Highlight description="The natural, exponential decay of memory over time. Passive review does almost nothing to slow this curve down." theme={theme}>Forgetting Curve</Highlight>. The comfort of re-reading is a trap. The act of testing, however, does something remarkable: it slows the rate of forgetting, fundamentally changing the trajectory of your learning.</p>
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="The 'Test Effect'." eyebrow="Step 2" icon={BrainCircuit} theme={theme}>
              <p>So why is testing so powerful? It's not about assessment; it's a mechanism for building memory. This is the <Highlight description="The finding that the act of retrieving information from memory makes that memory more durable and long-lasting than simply re-studying it." theme={theme}>Testing Effect</Highlight>. The psychologist Robert Bjork gives us the vocabulary to understand why: he splits memory into two types.</p>
              <p><Highlight description="How deeply a memory is embedded. This is 'true' learning and is relatively permanent. It only increases through effortful retrieval." theme={theme}>Storage Strength</Highlight> is how well you've actually learned something. <Highlight description="How easily a memory comes to mind right now. This is a temporary state, influenced by recent exposure." theme={theme}>Retrieval Strength</Highlight> is how easily you can access it. Re-reading massively boosts retrieval strength (it feels easy and fluent) but does almost nothing for storage strength. Active recall, especially when it's difficult, is the only thing that significantly boosts storage strength.</p>
              <StrengthMeter />
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The 'Dropout' Fallacy." eyebrow="Step 3" icon={XCircle} theme={theme}>
              <p>One of the most common and damaging student habits is the "dropout" method: "I know this now, so I'll stop quizzing myself and just look over my notes." This feels efficient, but a devastating 2008 study by Karpicke and Roediger proved it's a fallacy.</p>
              <p>They found that continuing to test yourself on a topic, even after you've gotten it right once, is the most crucial part of learning. Students who dropped items from testing after one correct answer had a final recall of only ~35% a week later. Students who continued testing themselves on everything retained ~80%—more than double! The heavy lifting of memory consolidation is done entirely by the retrieval process. Stopping the testing stops the learning.</p>
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="Beyond Rote Memory." eyebrow="Step 4" icon={Share2} theme={theme}>
              <p>A common criticism of active recall is that it only teaches you to parrot back facts without real understanding. This is a myth. Research shows that retrieval practice enhances <Highlight description="The ability to apply knowledge learned in one context to new, different contexts. It is a key measure of deep understanding." theme={theme}>Transfer of Knowledge</Highlight>. Why?</p>
              <p>When you re-read, you're encoding the information exactly as it appears on the page. But when you are forced to retrieve it, you must reconstruct the memory in your own words. This process forces your brain to focus on the underlying principles and abstract them from the specific examples. This makes the knowledge more flexible and easier to apply to new problems you haven't seen before—like the ones that show up on your Leaving Cert paper.</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="The Anxiety Myth." eyebrow="Step 5" icon={HeartPulse} theme={theme}>
              <p>The biggest barrier to using active recall is fear. It feels like a high-stakes judgment, and it exposes your gaps in knowledge, which can be stressful. But a large-scale study by Agarwal et al. (2014) on students using frequent, low-stakes quizzing found the exact opposite was true.</p>
              <p>An incredible 92% of students said it helped them learn, and 72% said it made them *less* nervous for big exams. It works through two mechanisms: <Highlight description="Repeated, low-stakes exposure to the testing format makes it feel normal and routine, reducing the fear associated with high-stakes exams." theme={theme}>Exposure & Desensitization</Highlight> and <Highlight description="The process of getting an accurate understanding of what you know and don't know. Active recall eliminates the uncertainty that is a major source of anxiety." theme={theme}>Metacognitive Calibration</Highlight>. By testing yourself constantly, you eliminate the surprise. The final exam is no longer a scary unknown; it's just another Tuesday.</p>
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="Your Recall Toolkit." eyebrow="Step 6" icon={Wrench} theme={theme}>
              <p>You now understand the science. Active recall is the single most powerful tool in your academic arsenal. To master it, you need to follow three core rules derived from the research, and audit your own current methods.</p>
              <p>1. <strong>Embrace Disfluency:</strong> Understand that the feeling of "struggle" is the feeling of learning. If it feels easy, it's probably ineffective. 2. <strong>The "Book Closed" Rule:</strong> Never judge how well you know something with the book open. That's just fluency, not learning. 3. <strong>Stop Dropping Items:</strong> Continue to test yourself on material even after you get it right. Continued retrieval is what arrests the forgetting curve. </p>
              <StudyMethodAuditor />
              <MicroCommitment theme={theme}>
                <p>For your next study session, try the 20/80 rule. Spend 20% of your time consuming information (reading, watching) and 80% of your time actively recalling it (self-quizzing, explaining it out loud).</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default MasteringActiveRecallModule;
