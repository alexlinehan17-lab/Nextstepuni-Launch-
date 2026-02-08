/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence, Reorder } from 'framer-motion';
import {
  MessageSquare, BrainCircuit, BookOpen, Wrench, Layers, Shield, Zap, Flag, Bus
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { slateTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = slateTheme;

// --- INTERACTIVE COMPONENTS ---

const ThoughtRecord = () => {
    const [step, setStep] = useState(0);
    const [record, setRecord] = useState({ situation: '', emotion: '', intensity: 90, nat: '', evidenceFor: '', evidenceAgainst: '', alternative: '', reRate: 50});
    const update = (field: string, value: any) => setRecord(prev => ({...prev, [field]: value}));

    const steps = ['Situation', 'Emotion', 'Negative Thought', 'Evidence For', 'Evidence Against', 'Alternative', 'Re-Rate'];

    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-semibold text-stone-800 text-center italic">The Thought Record</h4>
             <div className="flex justify-between my-4"><div className="w-full h-1 bg-stone-100 rounded-full"><motion.div className="h-1 bg-slate-500 rounded-full" animate={{width: `${(step / (steps.length - 1)) * 100}%`}}/></div></div>
             <AnimatePresence mode="wait">
             <motion.div key={step} initial={{opacity:0, x:20}} animate={{opacity:1, x:0}} exit={{opacity:0, x:-20}} >
                {step === 0 && <div><label className="font-bold">1. Situation:</label><input value={record.situation} onChange={e => update('situation', e.target.value)} placeholder="e.g., Sitting down to study History" className="w-full p-2 mt-2 bg-stone-50 rounded-lg"/></div>}
                {step === 1 && <div><label className="font-bold">2. Emotion:</label><input value={record.emotion} onChange={e => update('emotion', e.target.value)} placeholder="e.g., Panic" className="w-full p-2 mt-2 bg-stone-50 rounded-lg"/><label>Intensity: {record.intensity}%</label><input type="range" value={record.intensity} onChange={e => update('intensity', e.target.value)} className="w-full"/></div>}
                {step === 2 && <div><label className="font-bold">3. Negative Automatic Thought (NAT):</label><textarea value={record.nat} onChange={e => update('nat', e.target.value)} placeholder="e.g., I'll never remember all these dates." className="w-full p-2 mt-2 bg-stone-50 rounded-lg h-24"/></div>}
                {step === 3 && <div><label className="font-bold">4. Evidence For:</label><textarea value={record.evidenceFor} onChange={e => update('evidenceFor', e.target.value)} placeholder="e.g., I forgot the date of Clontarf yesterday." className="w-full p-2 mt-2 bg-stone-50 rounded-lg h-24"/></div>}
                {step === 4 && <div><label className="font-bold">5. Evidence Against:</label><textarea value={record.evidenceAgainst} onChange={e => update('evidenceAgainst', e.target.value)} placeholder="e.g., I passed my last test. I have 3 months to study." className="w-full p-2 mt-2 bg-stone-50 rounded-lg h-24"/></div>}
                {step === 5 && <div><label className="font-bold">6. Alternative Thought:</label><textarea value={record.alternative} onChange={e => update('alternative', e.target.value)} placeholder="e.g., History is hard, but if I use flashcards I can pass." className="w-full p-2 mt-2 bg-stone-50 rounded-lg h-24"/></div>}
                {step === 6 && <div><label className="font-bold">7. Re-Rate Emotion:</label><p>Initial Panic: {record.intensity}%</p><label>New Panic Level: {record.reRate}%</label><input type="range" value={record.reRate} onChange={e => update('reRate', e.target.value)} className="w-full"/></div>}
             </motion.div>
             </AnimatePresence>
             <div className="flex justify-between mt-4">
                <button onClick={() => setStep(s=>Math.max(0,s-1))} disabled={step===0} className="px-3 py-1 text-xs bg-stone-200 rounded-md disabled:opacity-50">Prev</button>
                <button onClick={() => setStep(s=>Math.min(steps.length-1,s+1))} disabled={step===steps.length-1} className="px-3 py-1 text-xs bg-stone-200 rounded-md disabled:opacity-50">Next</button>
             </div>
        </div>
    );
};

const GradedExposureHierarchy = () => {
    const [items, setItems] = useState([
        { id: 1, text: "Open Maths book (10 mins)", suds: 20 },
        { id: 2, text: "Read one past question", suds: 50 },
        { id: 3, text: "Attempt one question (timed)", suds: 80 },
    ]);
    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-semibold text-stone-800 text-center italic">Exposure Hierarchy Builder</h4>
             <Reorder.Group axis="y" values={items} onReorder={setItems} className="space-y-2 mt-6">
                {items.map(item => (
                    <Reorder.Item key={item.id} value={item} className="p-3 bg-stone-100 rounded-lg flex justify-between items-center cursor-grab active:cursor-grabbing">
                        <span>{item.text}</span>
                        <span className="font-bold text-sm text-rose-500">{item.suds} SUDS</span>
                    </Reorder.Item>
                ))}
             </Reorder.Group>
        </div>
    );
};

const PassengersOnBus = () => {
    const [busState, setBusState] = useState<'driving'|'stopped'>('driving');
    const [thought, setThought] = useState('');

    const thoughts = ["You're going to fail.", "You're not smart enough.", "Turn back now."];

    React.useEffect(() => {
        let interval: any;
        if(busState === 'driving') {
             interval = setInterval(() => {
                setThought(thoughts[Math.floor(Math.random() * thoughts.length)]);
                setTimeout(() => setThought(''), 1500);
            }, 3000);
        }
        return () => clearInterval(interval);
    }, [busState, thoughts]);

    return (
         <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-semibold text-stone-800 text-center italic">Passengers on the Bus</h4>
             <div className="h-32 bg-stone-100 rounded-lg p-4 relative overflow-hidden">
                <motion.div className="absolute" animate={{x: busState === 'driving' ? '150%' : '50%'}} transition={{duration: busState === 'driving' ? 5 : 0.5}}><Bus size={48} className="text-slate-700"/></motion.div>
                {thought && <div className="absolute top-4 left-1/2 p-2 bg-white rounded-lg text-xs shadow-lg">{thought}</div>}
             </div>
             <div className="grid grid-cols-2 gap-4 mt-4">
                <button onClick={() => setBusState('stopped')} className="p-4 bg-rose-100 text-rose-800 rounded-xl">Argue with Passenger (Bus Stops)</button>
                <button onClick={() => setBusState('driving')} className="p-4 bg-emerald-100 text-emerald-800 rounded-xl">Acknowledge & Drive (Bus Moves)</button>
             </div>
        </div>
    );
}

// --- MODULE COMPONENT ---
const CatastrophicThinkingModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'catastrophe-machine', title: 'The Catastrophe Machine', eyebrow: '01 // The Problem', icon: MessageSquare },
    { id: 'blank-mind', title: 'The Biology of "Blank Mind"', eyebrow: '02 // The Hardware', icon: BrainCircuit },
    { id: 'cbt-standard', title: 'The Gold Standard (CBT)', eyebrow: '03 // The Software', icon: BookOpen },
    { id: 'thought-record', title: 'The Thought Record', eyebrow: '04 // The Core Tool', icon: Wrench },
    { id: 'decatastrophize', title: 'Decatastrophizing', eyebrow: '05 // The "So What?" Drill', icon: Layers },
    { id: 'face-fear', title: 'Facing the Fear', eyebrow: '06 // Exposure', icon: Shield },
    { id: 'observer-self', title: 'The Observer Self (ACT)', eyebrow: '07 // The Alternative', icon: Zap },
    { id: 'action-plan', title: 'The Action Plan', eyebrow: '08 // The Blueprint', icon: Flag },
  ];

  return (
    <ModuleLayout
      moduleNumber="12"
      moduleTitle="Reframing Thoughts"
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Catastrophe Machine." eyebrow="Step 1" icon={MessageSquare} theme={theme}>
              <p><Highlight description="An exaggerated negative thought process about a potential threat. It's a cognitive distortion where you magnify the consequences and underestimate your ability to cope." theme={theme}>Catastrophizing</Highlight> is the engine of exam anxiety. It's a 3-part machine: 1) <Highlight description="Repetitive, intrusive thoughts about failure." theme={theme}>Rumination</Highlight> (the thought you can't switch off), 2) <Highlight description="Blowing the consequences out of proportion (e.g., 'If I get a H4, my life is over')." theme={theme}>Magnification</Highlight> (making a mountain out of a molehill), and 3) <Highlight description="The belief that the negative outcome is inevitable and you are powerless to stop it." theme={theme}>Helplessness</Highlight> (the feeling you're powerless).</p>
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="The Biology of 'Blank Mind'." eyebrow="Step 2" icon={BrainCircuit} theme={theme}>
              <p>Going "blank" is not a metaphor; it's a neurobiological event. When your brain perceives a threat (the exam paper), your <Highlight description="The brain's threat detection centre." theme={theme}>amygdala</Highlight> activates the stress response, flooding your system with adrenaline and cortisol. High levels of cortisol physically inhibit your <Highlight description="The brain region essential for memory retrieval." theme={theme}>hippocampus</Highlight>, blocking access to stored information. Your logical <Highlight description="The 'CEO' of the brain, responsible for planning and logic." theme={theme}>Prefrontal Cortex</Highlight> is taken offline. You haven't forgotten the information; you've just temporarily lost the password.</p>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The Gold Standard (CBT)." eyebrow="Step 3" icon={BookOpen} theme={theme}>
              <p><Highlight description="Cognitive Behavioral Therapy (CBT) is a form of psychological treatment that has been demonstrated to be effective for a range of problems including anxiety and depression." theme={theme}>Cognitive Behavioral Therapy (CBT)</Highlight> is the gold standard for dismantling this machine. Its central idea is simple but revolutionary: events don't cause your feelings; your *interpretation* of events causes your feelings. The exam paper is neutral. The thought "I can't do this" is the interpretation that triggers panic. CBT teaches you to challenge that interpretation.</p>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="The Thought Record." eyebrow="Step 4" icon={Wrench} theme={theme}>
              <p>The core tool of CBT is the <Highlight description="A structured exercise to identify, challenge, and reframe Negative Automatic Thoughts (NATs)." theme={theme}>Thought Record</Highlight>. It forces you to move from vague, emotional thinking to specific, evidence-based reasoning. By systematically examining the evidence for and against your catastrophic thought, you can generate a more balanced, realistic alternative. Run this protocol every time you feel a spike of panic.</p>
              <ThoughtRecord />
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Decatastrophizing." eyebrow="Step 5" icon={Layers} theme={theme}>
              <p>This technique doesn't promise "it will all be fine." Instead, it confronts the worst-case scenario head-on to strip it of its terror. It's called the <Highlight description="A CBT technique where you follow a catastrophic thought to its conclusion by repeatedly asking 'And then what?' to reveal that the ultimate outcome is manageable." theme={theme}>Downward Arrow</Highlight> technique. By following the "what if" chain to its end, you realize the ultimate outcome is survivable, and you create a "Plan B."</p>
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="Facing the Fear." eyebrow="Step 6" icon={Shield} theme={theme}>
              <p>Anxiety creates a vicious cycle of avoidance. You fear a subject, so you avoid it, which makes you unprepared, which justifies the original fear. The only way to break this cycle is <Highlight description="A behavioral technique where you face a feared stimulus in small, incremental steps, allowing your brain to 'habituate' and learn that it is not a threat." theme={theme}>Graded Exposure</Highlight>. You build a "ladder" of feared tasks, from least scary to most scary, and slowly work your way up, retraining your brain's alarm system.</p>
              <GradedExposureHierarchy/>
            </ReadingSection>
          )}
          {activeSection === 6 && (
            <ReadingSection title="The Observer Self (ACT)." eyebrow="Step 7" icon={Zap} theme={theme}>
              <p>For some, challenging thoughts feels like an endless argument. <Highlight description="Acceptance and Commitment Therapy (ACT) is a 'third-wave' CBT approach that focuses on changing your relationship to your thoughts, rather than the content of the thoughts themselves." theme={theme}>Acceptance and Commitment Therapy (ACT)</Highlight> offers an alternative: don't argue with the thought, just notice it and act anyway. This is called <Highlight description="The process of 'unhooking' from your thoughts, seeing them as just words passing through your mind, rather than objective truths or commands." theme={theme}>Cognitive Defusion</Highlight>.</p>
              <PassengersOnBus/>
            </ReadingSection>
          )}
          {activeSection === 7 && (
            <ReadingSection title="The Action Plan." eyebrow="Step 8" icon={Flag} theme={theme}>
              <p>You now have a complete toolkit of evidence-based psychological strategies to manage exam anxiety. You have the "software" (CBT & ACT) to go with the "hardware" optimization (sleep, nutrition) from other modules. Now it's about practice.</p>
              <MicroCommitment theme={theme}><p>Choose ONE tool from this module--the Thought Record, Downward Arrow, or an Exposure task. Commit to using it just once this week. You're not just studying; you're becoming your own therapist.</p></MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default CatastrophicThinkingModule;
