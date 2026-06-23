
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  BarChart3, BrainCircuit, XCircle, Share2, HeartPulse, Wrench, Check, X
} from 'lucide-react';
import { type ModuleProgress } from '../types';
import { indigoTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment, ToolJumpCard } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';
import { useEssentialsMode } from '../hooks/useEssentialsMode';
import { Cite } from './ModuleReferences';
import { ACTIVE_RECALL_REFERENCE_LIST } from '../data/references/activeRecall';

const theme = indigoTheme;

// --- INTERACTIVE COMPONENTS ---
const StrengthMeter = () => {
    const [method, setMethod] = useState<'passive'|'active'|null>(null);
    let retrieval = 10, storage = 10;
    if (method === 'passive') { retrieval = 90; storage = 15; }
    if (method === 'active') { retrieval = 40; storage = 85; }

    return(
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
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
        { id: 1, name: "Re-reading your notes", type: "passive", explanation: "This feels productive because it all looks familiar, but familiarity isn't the same as actually knowing it. You're basically just fooling yourself into feeling prepared." },
        { id: 2, name: "Doing a past paper", type: "active", explanation: "This is one of the best things you can do. The struggle of trying to pull answers out of your head is exactly what makes them stick." },
        { id: 3, name: "Highlighting a textbook", type: "passive", explanation: "You're picking out information, but you're not actually testing whether you know it. Your brain isn't doing the heavy lifting here, so very little sticks." },
        { id: 4, name: "Explaining it to a friend", type: "active", explanation: "This is brilliant. To explain something, you have to pull it from memory and organise it clearly. That's a seriously powerful way to learn." },
        { id: 5, name: "Watching a YouTube video", type: "passive", explanation: "It's handy for understanding something the first time, but just watching doesn't build memory. You need to quiz yourself on it afterwards to make it stick." },
        { id: 6, name: "Creating flashcards", type: "active", explanation: "This counts as active recall IF you make them from memory. If you're just copying from the book, it's passive. The real benefit comes from testing yourself with them later." },
    ];
    const [selectedId, setSelectedId] = useState<number | null>(null);
    const selectedMethod = methods.find(m => m.id === selectedId);

    return (
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Study Method Auditor</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Click a study method to get your Active Recall rating.</p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {methods.map(method => (
                    <motion.button
                        key={method.id}
                        onClick={() => setSelectedId(method.id)}
                        whileHover={selectedId !== method.id ? { x: -2, y: -2 } : {}}
                        whileTap={selectedId !== method.id ? { x: 2, y: 2 } : {}}
                        className="p-4 rounded-xl text-sm font-bold text-left transition-all"
                        style={{
                            backgroundColor: selectedId === method.id ? (methods.find(m => m.id === method.id)?.type === 'active' ? '#6EE7B7' : '#FCA5A5') : '#FFFFFF',
                            border: `2.5px solid ${selectedId === method.id ? (methods.find(m => m.id === method.id)?.type === 'active' ? '#059669' : '#DC2626') : '#1C1917'}`,
                            borderRadius: 14,
                            boxShadow: selectedId === method.id ? 'none' : '3px 3px 0px 0px #1C1917',
                            color: selectedId === method.id ? (methods.find(m => m.id === method.id)?.type === 'active' ? '#064E3B' : '#7F1D1D') : '#1C1917',
                        }}
                    >
                        {method.name}
                    </motion.button>
                ))}
            </div>
            <AnimatePresence>
                {selectedMethod && (
                    <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: 10 }}
                        className="mt-6 p-4 rounded-xl"
                        style={{
                            backgroundColor: selectedMethod.type === 'active' ? '#6EE7B7' : '#FCA5A5',
                            border: `2.5px solid ${selectedMethod.type === 'active' ? '#059669' : '#DC2626'}`,
                            boxShadow: `3px 3px 0px 0px ${selectedMethod.type === 'active' ? '#059669' : '#DC2626'}`,
                        }}
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
  const essentials = useEssentialsMode();
  const sections = [
    { id: 'great-forgetting', title: 'The Great Forgetting', eyebrow: '01 // The Problem', icon: BarChart3 },
    { id: 'test-effect', title: 'Why Testing Yourself Works', eyebrow: '02 // How It Works', icon: BrainCircuit },
    { id: 'dropout-fallacy', title: 'The "I Know This" Trap', eyebrow: '03 // The Common Mistake', icon: XCircle },
    { id: 'transfer-effect', title: 'Beyond Just Memorising Facts', eyebrow: '04 // Real Understanding', icon: Share2 },
    { id: 'anxiety-myth', title: 'The Anxiety Myth', eyebrow: '05 // The Surprising Truth', icon: HeartPulse },
    { id: 'recall-toolkit', title: 'Your Recall Toolkit', eyebrow: '06 // The Action Plan', icon: Wrench },
  ];

  return (
    <ModuleLayout moduleNumber="01" moduleTitle="Mastering Active Recall" moduleSubtitle="Why Testing Yourself Is a Superpower" moduleDescription={`Testing yourself isn't just for checking what you know — it's actually the single best way to make things stick in your memory for good.`} theme={theme} sections={sections} onBack={onBack} progress={progress} onProgressUpdate={onProgressUpdate} finishButtonText="Activate Recall" references={ACTIVE_RECALL_REFERENCE_LIST}>
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Great Forgetting." eyebrow="Step 1" icon={BarChart3} theme={theme}>
              {essentials ? (<>
              <p>Re-reading feels good but your memory collapses within a week. Testing yourself keeps far more in your head. This is the <Highlight description="Your memory naturally fades over time unless you do something about it. Just re-reading your notes barely slows this down at all." theme={theme}>Forgetting Curve</Highlight>. Re-reading is a trap. Self-testing slows down forgetting and changes how much you hold onto.</p>
              </>) : (<>
              <p>In the last module, we saw that passive review (like re-reading) feels good but leads to poor memory over time. This isn't a small effect — it's a massive one. When you compare students who just re-read their notes to students who tested themselves, the re-readers did slightly better after a few minutes, but a week later the re-readers had forgotten far more than the students who had tested themselves.<Cite n={1} /></p>
              <p>This is the harsh reality of the <Highlight description="Your memory naturally fades over time unless you do something about it. Just re-reading your notes barely slows this down at all." theme={theme}>Forgetting Curve</Highlight>. The comfort of re-reading is a trap. Testing yourself, on the other hand, does something powerful: it slows down how fast you forget, completely changing how much you actually hold onto.</p>
              </>)}
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="Why Testing Yourself Works." eyebrow="Step 2" icon={BrainCircuit} theme={theme}>
              {essentials ? (<>
              <p>Testing builds stronger memories. This is the <Highlight description="The simple idea that pulling information out of your head makes that memory stronger and longer-lasting than just reading over it again." theme={theme}>Testing Effect</Highlight>. Your memory has two parts: <Highlight description="How deeply something is actually locked into your brain. This is real learning — it's fairly permanent and only gets stronger when you make an effort to remember things." theme={theme}>Storage Strength</Highlight> (how deeply you know it) and <Highlight description="How easily something comes to mind right now. This changes all the time based on what you've looked at recently." theme={theme}>Retrieval Strength</Highlight> (how easily it comes to mind). Re-reading only boosts retrieval. Active recall builds storage. That is real learning.</p>
              </>) : (<>
              <p>So why is testing yourself so powerful? It's not about checking what you know — it's actually a way of building stronger memories. This is the <Highlight description="The simple idea that pulling information out of your head makes that memory stronger and longer-lasting than just reading over it again." theme={theme}>Testing Effect</Highlight><Cite n={1} />. To understand why, it helps to think of memory as having two separate parts.</p>
              <p><Highlight description="How deeply something is actually locked into your brain. This is real learning — it's fairly permanent and only gets stronger when you make an effort to remember things." theme={theme}>Storage Strength</Highlight> is how well you've actually learned something. <Highlight description="How easily something comes to mind right now. This changes all the time based on what you've looked at recently." theme={theme}>Retrieval Strength</Highlight> is how easily you can access it right now. Re-reading makes retrieval strength shoot up (everything looks familiar and easy) but barely touches storage strength. Active recall — especially when it feels hard — is the only thing that seriously builds storage strength.<Cite n={2} /></p>
              </>)}
              <StrengthMeter />
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The 'I Know This' Trap." eyebrow="Step 3" icon={XCircle} theme={theme}>
              {essentials ? (<>
              <p>Do not stop testing yourself after getting it right once. Students who keep testing themselves remember far more a week later than students who stop as soon as they get it right.<Cite n={3} /> The act of pulling information from your head IS the learning. When you stop testing, you stop learning. Keep going even after you get it right.</p>
              </>) : (<>
              <p>One of the most common and damaging student habits is this: "I got it right once, so I'll stop quizzing myself on it and just look over my notes." It feels efficient, but it's actually a trap.</p>
              <p>Here's what actually happens: continuing to test yourself on a topic, even after you've already gotten it right once, is the most important part of the whole process. In a well-known study, students who kept testing themselves on material remembered far more a week later than students who stopped as soon as they got it right once — even though, at the time, both groups felt just as sure they knew it.<Cite n={3} /> The real work of locking things into your memory is done by the act of pulling it from your head. When you stop testing yourself, you stop learning.</p>
              </>)}
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="Beyond Just Memorising Facts." eyebrow="Step 4" icon={Share2} theme={theme}>
              {essentials ? (<>
              <p>Active recall does not just help you parrot facts. It improves your ability to <Highlight description="Being able to take what you learned in one situation and use it in a completely different one. This is the real test of whether you actually understand something." theme={theme}>apply knowledge to new situations</Highlight>. When you pull information from memory, you rebuild it in your own words. Your brain focuses on the key ideas. Your knowledge becomes flexible and works on problems you have never seen before.</p>
              </>) : (<>
              <p>A common worry about active recall is that it only helps you parrot back facts without really understanding them. Not true. Testing yourself actually improves your ability to <Highlight description="Being able to take what you learned in one situation and use it in a completely different one. This is the real test of whether you actually understand something." theme={theme}>apply your knowledge to new situations</Highlight>. Here's why.</p>
              <p>When you re-read, your brain stores the information exactly as it appears on the page. But when you're forced to pull it from memory, you have to rebuild it in your own words. This makes your brain focus on the key ideas underneath the specific examples. The result? Your knowledge becomes more flexible and easier to use on problems you haven't seen before<Cite n={4} /> — like the ones that show up on your exam paper.<Cite n={5} /></p>
              </>)}
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="The Anxiety Myth." eyebrow="Step 5" icon={HeartPulse} theme={theme}>
              {essentials ? (<>
              <p>Self-testing feels scary, but when surveyed, the large majority of students say it helps them learn — and most say it actually makes them less nervous for big exams.<Cite n={6} /> It works by <Highlight description="When you test yourself regularly in a low-pressure way, the format starts to feel normal. By the time the real exam comes around, it's not scary — it's just familiar." theme={theme}>getting you used to the format</Highlight> and by <Highlight description="When you test yourself, you get an honest picture of what you know and what you don't. That removes the uncertainty, which is a huge source of exam anxiety." theme={theme}>showing you where you stand</Highlight>. The exam stops being a scary unknown.</p>
              </>) : (<>
              <p>The biggest barrier to using active recall is fear. It feels like a test, it exposes what you don't know, and that can be stressful. But when large groups of students were asked about frequent, low-stakes quizzing, the results told the opposite story.</p>
              <p>When those students were surveyed, the large majority said it helped them learn, and most said it actually made them <em>less</em> nervous for big exams.<Cite n={6} /> It works in two ways: <Highlight description="When you test yourself regularly in a low-pressure way, the format starts to feel normal. By the time the real exam comes around, it's not scary — it's just familiar." theme={theme}>Getting Used to It</Highlight> and <Highlight description="When you test yourself, you get an honest picture of what you know and what you don't. That removes the uncertainty, which is a huge source of exam anxiety." theme={theme}>Knowing Where You Stand</Highlight>. By testing yourself regularly, you take away the surprise. The final exam is no longer a scary unknown — it's just another Tuesday.</p>
              </>)}
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="Your Recall Toolkit." eyebrow="Step 6" icon={Wrench} theme={theme}>
              {essentials ? (<>
              <p>Three rules: a bit of effortful struggle you can still succeed at is what builds memory. Never judge your knowledge with the book open. Keep testing even after getting it right. Check how your current methods stack up below.</p>
              </>) : (<>
              <p>You now get why this works. Active recall is the single most powerful tool you have for studying. To make the most of it, follow three simple rules — and take a look at how your current methods stack up.</p>
              </>)}
              <div className="my-10 rounded-2xl p-5 md:p-6 space-y-3" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
                {/* Card 1 — Sky */}
                <div className="p-4 flex items-start gap-4" style={{ backgroundColor: '#93C5FD', border: '2.5px solid #2563EB', borderRadius: 16, boxShadow: '4px 4px 0px 0px #2563EB' }}>
                  <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-white" style={{ backgroundColor: '#2563EB' }}>1</div>
                  <div>
                    <p className="text-sm font-bold" style={{ color: '#1E3A8A' }}>A Bit of Struggle Is the Point</p>
                    <p className="text-[13px] mt-0.5" style={{ color: '#1E3A8A', opacity: 0.8 }}>When recalling something takes real effort — but you can still manage it — that effort is what builds lasting memory (researchers call these &ldquo;desirable difficulties&rdquo;).<Cite n={2} /> If it feels completely effortless, it&apos;s probably not doing much.</p>
                  </div>
                </div>
                {/* Card 2 — Sunshine */}
                <div className="p-4 flex items-start gap-4" style={{ backgroundColor: '#FCD34D', border: '2.5px solid #D97706', borderRadius: 16, boxShadow: '4px 4px 0px 0px #D97706' }}>
                  <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-white" style={{ backgroundColor: '#D97706' }}>2</div>
                  <div>
                    <p className="text-sm font-bold" style={{ color: '#78350F' }}>The "Book Closed" Rule</p>
                    <p className="text-[13px] mt-0.5" style={{ color: '#78350F', opacity: 0.8 }}>Never judge how well you know something with the book open. That's just familiarity, not real knowledge.</p>
                  </div>
                </div>
                {/* Card 3 — Peach */}
                <div className="p-4 flex items-start gap-4" style={{ backgroundColor: '#FDBA74', border: '2.5px solid #EA580C', borderRadius: 16, boxShadow: '4px 4px 0px 0px #EA580C' }}>
                  <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-white" style={{ backgroundColor: '#EA580C' }}>3</div>
                  <div>
                    <p className="text-sm font-bold" style={{ color: '#7C2D12' }}>Don't Stop After Getting It Right</p>
                    <p className="text-[13px] mt-0.5" style={{ color: '#7C2D12', opacity: 0.8 }}>Keep testing yourself on material even after you get it right once. That's what stops you from forgetting it.</p>
                  </div>
                </div>
              </div>
              <StudyMethodAuditor />
              <MicroCommitment theme={theme}>
                <p>For your next study session, flip the balance: spend most of your time actively recalling (self-quizzing, explaining out loud) rather than re-reading or watching. The more of your study time goes into pulling information out of your own head, the more of it sticks.</p>
              </MicroCommitment>
              <ToolJumpCard
                toolId="syllabus-xray"
                title="See where to test yourself first"
                description="Syllabus X-Ray shows the exact topics most likely to come up. Pick a shaky one and run an active recall session against it now."
                ctaLabel="Open Syllabus X-Ray"
              />
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default MasteringActiveRecallModule;
