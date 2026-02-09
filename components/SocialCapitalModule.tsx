/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import {
  Users, Share2, Anchor, VenetianMask, Map
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { violetTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = violetTheme;

// --- INTERACTIVE COMPONENTS ---
const SocialCapitalSorter = () => {
    const initialItems = [
        {id: 1, text: "My best mate", type: "bonding"},
        {id: 2, text: "My mam", type: "bonding"},
        {id: 3, text: "A cousin in college", type: "bridging"},
        {id: 4, text: "My GAA coach", type: "bridging"},
        {id: 5, text: "The local shopkeeper", type: "bonding"},
    ];
    const [items, setItems] = useState(initialItems);
    const [bonding, setBonding] = useState<typeof initialItems>([]);
    const [bridging, setBridging] = useState<typeof initialItems>([]);

    const handleSort = (item: typeof initialItems[0], target: 'bonding' | 'bridging') => {
        setItems(items.filter(i => i.id !== item.id));
        if (target === 'bonding') setBonding([...bonding, item]);
        else setBridging([...bridging, item]);
    };

    return(
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-2xl border border-zinc-200 dark:border-zinc-700 shadow-xl">
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center italic">Social Capital Sorter</h4>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Sort these connections into the correct network.</p>
             <div className="grid grid-cols-2 gap-4">
                <div className="p-4 bg-emerald-50 border-2 border-dashed border-emerald-200 rounded-2xl min-h-[150px]">
                    <h5 className="font-bold text-emerald-700 text-center mb-2">Bonding (Safety Net)</h5>
                    {bonding.map(b => <motion.div layoutId={`item-${b.id}`} key={b.id} className="text-xs p-2 bg-white dark:bg-zinc-800 rounded-md text-center font-bold mb-2 shadow-sm">{b.text}</motion.div>)}
                </div>
                <div className="p-4 bg-blue-50 border-2 border-dashed border-blue-200 rounded-2xl min-h-[150px]">
                    <h5 className="font-bold text-blue-700 text-center mb-2">Bridging (Ladder)</h5>
                    {bridging.map(b => <motion.div layoutId={`item-${b.id}`} key={b.id} className="text-xs p-2 bg-white dark:bg-zinc-800 rounded-md text-center font-bold mb-2 shadow-sm">{b.text}</motion.div>)}
                </div>
             </div>
             <div className="mt-6 flex flex-wrap justify-center gap-3">
                {items.map(item => (
                    <motion.div layoutId={`item-${item.id}`} key={item.id} className="p-3 bg-zinc-100 dark:bg-zinc-800 rounded-lg shadow-sm">
                        <span className="font-bold text-sm">{item.text}</span>
                        <div className="mt-2 text-xs flex gap-1">
                            <button onClick={() => handleSort(item, 'bonding')} className="bg-emerald-200 text-emerald-800 px-2 py-0.5 rounded">Bonding</button>
                            <button onClick={() => handleSort(item, 'bridging')} className="bg-blue-200 text-blue-800 px-2 py-0.5 rounded">Bridging</button>
                        </div>
                    </motion.div>
                ))}
             </div>
        </div>
    );
};

const NotionsDecoder = () => {
    const phrases = [
        { insult: "Lick-arse", reframe: "Someone building a strategic relationship with a teacher." },
        { insult: "Try-hard", reframe: "Someone who understands that effort is the engine of success." },
        { insult: "Swot", reframe: "Someone investing time in their future." },
        { insult: "Notions", reframe: "Having aspirations beyond what's expected." },
    ];
    const [selected, setSelected] = useState(0);
    return(
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-2xl border border-zinc-200 dark:border-zinc-700 shadow-xl">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center italic">The "Notions" Decoder</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Translate the language of 'smart shaming' into the language of success.</p>
            <div className="flex flex-wrap justify-center gap-2 mb-6">
                {phrases.map((p, i) => (
                    <button key={p.insult} onClick={() => setSelected(i)} className={`px-4 py-2 text-sm font-bold rounded-lg border-2 ${selected === i ? 'bg-violet-500 text-white border-violet-500' : 'bg-zinc-100 border-zinc-200 dark:border-zinc-700'}`}>{p.insult}</button>
                ))}
            </div>
             <div className="p-6 bg-zinc-900 rounded-2xl text-center text-white font-mono">
                {phrases[selected].reframe}
             </div>
        </div>
    );
}

const NetworkAudit = () => {
    const [nodes] = useState([
        { id: 'You', x: 200, y: 150, type: 'self' },
        { id: 'Friend 1', x: 100, y: 100, type: 'bonding' },
        { id: 'Family', x: 150, y: 200, type: 'bonding' },
        { id: 'Teacher', x: 300, y: 100, type: 'bridging' },
        { id: 'Coach', x: 250, y: 200, type: 'bridging' },
    ]);

    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-2xl border border-zinc-200 dark:border-zinc-700 shadow-xl">
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center italic">My Network Map</h4>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Who is in your network? Who could you add?</p>
             <div className="h-80 w-full bg-zinc-50 dark:bg-zinc-800/50 rounded-lg relative">
                {nodes.map(node => (
                    <motion.div
                        key={node.id}
                        drag
                        dragConstraints={{left:0, right: 350, top:0, bottom:250}}
                        className={`absolute p-2 rounded-full text-xs font-bold text-white ${node.type === 'self' ? 'bg-violet-600' : node.type === 'bonding' ? 'bg-emerald-500' : 'bg-blue-500'}`}
                        style={{left: node.x, top: node.y}}
                    >{node.id}</motion.div>
                ))}
             </div>
        </div>
    );
};


// --- MODULE COMPONENT ---
const SocialCapitalModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'hidden-currency', title: 'The Hidden Currency', eyebrow: '01 // The Network Effect', icon: Users },
    { id: 'bonding-vs-bridging', title: 'Bonding vs. Bridging', eyebrow: '02 // Safety Net vs. Ladder', icon: Share2 },
    { id: 'accessing-tacit-knowledge', title: 'Tacit Knowledge', eyebrow: '03 // The Unwritten Rules', icon: Anchor },
    { id: 'cultural-capital', title: 'The Language of Power', eyebrow: '04 // Cultural Capital', icon: VenetianMask },
    { id: 'engineering-your-network', title: 'Engineering Your Network', eyebrow: '05 // The Action Plan', icon: Map },
  ];

  return (
    <ModuleLayout
      moduleNumber="06"
      moduleTitle="The Social Capital Protocol"
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && <ReadingSection title="The Hidden Currency." eyebrow="Step 1" icon={Users} theme={theme} />}
          {activeSection === 1 && <ReadingSection title="Bonding vs. Bridging Capital." eyebrow="Step 2" icon={Share2} theme={theme} />}
          {activeSection === 2 && <ReadingSection title="Accessing Tacit Knowledge." eyebrow="Step 3" icon={Anchor} theme={theme} />}
          {activeSection === 3 && <ReadingSection title="The Language of Power." eyebrow="Step 4" icon={VenetianMask} theme={theme} />}
          {activeSection === 4 && <ReadingSection title="Engineering Your Network." eyebrow="Step 5" icon={Map} theme={theme} />}
        </>
      )}
    </ModuleLayout>
  );
};
export default SocialCapitalModule;
