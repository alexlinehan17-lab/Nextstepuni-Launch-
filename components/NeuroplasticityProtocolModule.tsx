/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useRef, useEffect, useCallback } from 'react';
import { motion } from 'framer-motion';
import {
  BrainCircuit, Wrench, BookOpen, BarChart3, ClipboardCheck, ShieldCheck
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { orangeTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = orangeTheme;

// --- INTERACTIVE COMPONENTS ---
const JugglingStudyVisualizer = () => {
    const [scan, setScan] = useState(1);
    const data = [
        { scan: 1, value: 50, label: "Baseline" },
        { scan: 2, value: 80, label: "After 3 Months Practice" },
        { scan: 3, value: 60, label: "After 3 Months No Practice" },
    ];
    const currentData = data[scan-1];

    return (
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Juggling Study</h4>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Proof that learning physically changes the structure of your brain.</p>
             <div className="w-full max-w-xs mx-auto h-48 flex justify-center items-end">
                <motion.div
                    className="w-24 rounded-t-lg"
                    style={{ backgroundColor: '#2A7D6F' }}
                    initial={{height: '50%'}}
                    animate={{height: `${currentData.value}%`}}
                    transition={{type: 'spring', damping: 15, stiffness: 100}}
                />
             </div>
             <p className="text-center font-bold mt-2 dark:text-zinc-300">{currentData.label}</p>
             <div className="flex justify-center gap-2 mt-4">
                {[1, 2, 3].map(n => (
                  <button
                    key={n}
                    onClick={() => setScan(n)}
                    style={{
                      backgroundColor: scan === n ? '#2A7D6F' : '#FFFFFF',
                      border: scan === n ? '2px solid #2A7D6F' : '2px solid #d0cdc8',
                      borderRadius: 100,
                      padding: '8px 20px',
                      fontSize: 13,
                      fontWeight: 600,
                      color: scan === n ? '#FFFFFF' : '#7a7068',
                    }}
                  >
                    Scan {n}
                  </button>
                ))}
             </div>
        </div>
    );
};

const StudyMethodGrader = () => {
    const [method, setMethod] = useState<'passive' | 'active' | null>(null);
    return(
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Study Method Grader</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">Which study method sends a stronger signal to build your brain?</p>
             <div className="grid grid-cols-2 gap-4">
                <button onClick={() => setMethod('passive')} className="p-4 rounded-xl text-center font-medium transition-all" style={method === 'passive' ? { backgroundColor: '#FCA5A5', border: '2.5px solid #DC2626', borderRadius: 14, boxShadow: '3px 3px 0px 0px #DC2626', color: '#7F1D1D' } : { backgroundColor: '#FFFFFF', border: '2.5px solid #1C1917', borderRadius: 14, boxShadow: '3px 3px 0px 0px #1C1917' }}><strong>Passive Re-reading:</strong> "I'll just read my notes again."</button>
                <button onClick={() => setMethod('active')} className="p-4 rounded-xl text-center font-medium transition-all" style={method === 'active' ? { backgroundColor: '#6EE7B7', border: '2.5px solid #059669', borderRadius: 14, boxShadow: '3px 3px 0px 0px #059669', color: '#064E3B' } : { backgroundColor: '#FFFFFF', border: '2.5px solid #1C1917', borderRadius: 14, boxShadow: '3px 3px 0px 0px #1C1917' }}><strong>Active Recall:</strong> "I'll try to explain this from memory."</button>
             </div>
             {method &&
             <motion.div initial={{opacity:0}} animate={{opacity:1}} className="mt-6">
                <h5 className="font-bold text-center">Brain-Building Score:</h5>
                <div className="w-full h-8 bg-zinc-100 dark:bg-zinc-800 rounded-full mt-2 overflow-hidden">
                    <motion.div
                        className={`h-full rounded-full ${method === 'active' ? 'bg-emerald-500' : 'bg-rose-500'}`}
                        initial={{width: '0%'}}
                        animate={{width: method === 'active' ? '95%' : '20%'}}
                        transition={{duration: 1}}
                    />
                </div>
                <p className="text-xs text-center mt-2 text-zinc-500 dark:text-zinc-400">{method === 'active' ? 'Strong signal sent. Your brain is actually changing.' : 'Weak signal. Not much is changing up there.'}</p>
             </motion.div>}
        </div>
    );
}

const GRID_COLS = 12;
const GRID_ROWS = 8;
const TOTAL_CELLS = GRID_COLS * GRID_ROWS;

const getPathStyle = (walked: number): { bg: string; border: string } => {
  if (walked <= 0) return { bg: '#f0ece6', border: '#ddd8d0' };
  if (walked === 1) return { bg: '#c8e8e0', border: '#a0d4c8' };
  if (walked === 2) return { bg: '#8ecfbf', border: '#6ab8a4' };
  if (walked >= 3) return { bg: '#2A7D6F', border: '#1a5a4e' };
  return { bg: '#f0ece6', border: '#ddd8d0' };
};

const DesirePathMaker = () => {
  const [grid, setGrid] = useState<number[]>(() => new Array(TOTAL_CELLS).fill(0));
  const [isAnimating, setIsAnimating] = useState(false);
  const [resultMessage, setResultMessage] = useState<string | null>(null);
  const animationRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Clean up any running animation on unmount
  useEffect(() => {
    return () => {
      if (animationRef.current) clearTimeout(animationRef.current);
    };
  }, []);

  const strongPathCount = useCallback((g: number[]) => g.filter(v => v >= 3).length, []);

  const handleCellClick = (index: number) => {
    if (isAnimating) return;
    setResultMessage(null);
    setGrid(prev => {
      const next = [...prev];
      next[index] = Math.min(next[index] + 1, 5);
      return next;
    });
  };

  const handleDaysPass = () => {
    if (isAnimating) return;
    setResultMessage(null);
    setGrid(prev => prev.map(v => Math.max(v - 1, 0)));
  };

  const handleReset = () => {
    if (isAnimating) return;
    setGrid(new Array(TOTAL_CELLS).fill(0));
    setResultMessage(null);
  };

  // Animate a sequence of cell walks, then call onDone with the final grid
  const animateWalks = (steps: number[][], onDone: (finalGrid: number[]) => void) => {
    setIsAnimating(true);
    setResultMessage(null);
    const freshGrid = new Array(TOTAL_CELLS).fill(0);
    setGrid(freshGrid);

    let currentGrid = [...freshGrid];
    let stepIndex = 0;

    const tick = () => {
      if (stepIndex >= steps.length) {
        setIsAnimating(false);
        onDone(currentGrid);
        return;
      }
      const batch = steps[stepIndex];
      currentGrid = [...currentGrid];
      batch.forEach(cellIdx => {
        currentGrid[cellIdx] = Math.min(currentGrid[cellIdx] + 1, 5);
      });
      setGrid([...currentGrid]);
      stepIndex++;
      animationRef.current = setTimeout(tick, 180);
    };
    animationRef.current = setTimeout(tick, 300);
  };

  // Cramming: scatter walks across many random cells, each visited ~1 time
  const handleCramming = () => {
    if (isAnimating) return;
    const steps: number[][] = [];
    const allCells = Array.from({ length: TOTAL_CELLS }, (_, i) => i);
    // Shuffle and pick 40 random cells, each walked once across 10 batches
    const shuffled = [...allCells].sort(() => Math.random() - 0.5);
    const picked = shuffled.slice(0, 40);
    for (let i = 0; i < 10; i++) {
      const batch = picked.slice(i * 4, (i + 1) * 4);
      steps.push(batch);
    }
    animateWalks(steps, (finalGrid) => {
      const strong = strongPathCount(finalGrid);
      setResultMessage(`Cramming result: ${strong} strong pathway${strong !== 1 ? 's' : ''} formed. Scattered effort, weak connections.`);
    });
  };

  // Spaced Repetition: walk the same narrow path repeatedly
  const handleSpacedRepetition = () => {
    if (isAnimating) return;
    // Create a clear diagonal-ish path through the grid
    const pathCells: number[] = [];
    for (let row = 1; row <= 6; row++) {
      const col = Math.min(2 + row, GRID_COLS - 1);
      pathCells.push(row * GRID_COLS + col);
      if (col + 1 < GRID_COLS) pathCells.push(row * GRID_COLS + col + 1);
    }
    // Walk the same path 5 times (10 steps)
    const steps: number[][] = [];
    for (let rep = 0; rep < 5; rep++) {
      // Split path into two batches per repetition
      steps.push(pathCells.slice(0, Math.ceil(pathCells.length / 2)));
      steps.push(pathCells.slice(Math.ceil(pathCells.length / 2)));
    }
    animateWalks(steps, (finalGrid) => {
      const strong = strongPathCount(finalGrid);
      setResultMessage(`Spaced repetition result: ${strong} strong pathway${strong !== 1 ? 's' : ''} formed! Focused repetition builds lasting connections.`);
    });
  };

  return (
    <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
      {/* Section chip + title */}
      <div className="text-center mb-8">
        <span className="inline-block px-3 py-1 rounded-full text-[10px] font-bold tracking-wider uppercase mb-3" style={{ backgroundColor: '#e8f5f2', color: '#1a6358', border: '1px solid rgba(42,125,111,0.2)' }}>Interactive Simulation</span>
        <h4 className="font-serif text-2xl font-bold" style={{ color: '#1a1a1a' }}>Desire Path Maker</h4>
        <p className="text-sm mt-1" style={{ color: '#7a7068' }}>
          Click cells to walk on them. Repeat the same path to build strong connections — or scatter your effort and watch them fade.
        </p>
      </div>

      {/* Grid in bordered card */}
      <div className="bg-white dark:bg-zinc-900" style={{ border: '2px solid #1a1a1a', borderRadius: 16, padding: 20, maxWidth: 520, margin: '0 auto' }}>
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: `repeat(${GRID_COLS}, 1fr)`,
            gap: '4px',
          }}
        >
          {grid.map((walked, idx) => {
            const cs = getPathStyle(walked);
            return (
              <motion.div
                key={idx}
                onClick={() => handleCellClick(idx)}
                style={{
                  backgroundColor: cs.bg,
                  border: `1.5px solid ${cs.border}`,
                  aspectRatio: '1',
                  borderRadius: 8,
                  cursor: isAnimating ? 'default' : 'pointer',
                  transition: 'background-color 0.3s ease, border-color 0.3s ease',
                }}
                whileHover={!isAnimating ? { scale: 1.05 } : undefined}
                whileTap={!isAnimating ? { scale: 0.9 } : undefined}
              />
            );
          })}
        </div>
      </div>

      {/* Stat card */}
      <div className="flex justify-center mt-4">
        <div className="inline-flex items-center gap-3" style={{ backgroundColor: '#e8f5f2', border: '1.5px solid rgba(42,125,111,0.25)', borderRadius: 12, padding: '10px 20px' }}>
          <span className="font-serif font-bold" style={{ fontSize: 28, color: '#2A7D6F' }}>{strongPathCount(grid)}</span>
          <span className="text-[10px] font-semibold uppercase tracking-wider" style={{ color: '#9e9186', letterSpacing: '0.08em' }}>Strong paths<br/>built</span>
        </div>
      </div>

      {/* Controls */}
      <div className="flex flex-wrap justify-center gap-2 mt-6">
        <button onClick={handleDaysPass} disabled={isAnimating} className="inline-flex items-center gap-1.5 disabled:opacity-40 transition-colors" style={{ backgroundColor: '#FFFFFF', border: '2px solid #1a1a1a', borderRadius: 20, padding: '10px 20px', fontSize: 13, fontWeight: 600, color: '#1a1a1a' }}>
          Days Pass (Decay)
        </button>
        <button onClick={handleCramming} disabled={isAnimating} className="inline-flex items-center gap-1.5 disabled:opacity-40 transition-colors" style={{ backgroundColor: '#FFFFFF', border: '2px solid #d0cdc8', borderRadius: 20, padding: '10px 20px', fontSize: 13, fontWeight: 600, color: '#7a7068' }}>
          <span style={{ width: 6, height: 6, borderRadius: '50%', backgroundColor: '#E85D75', display: 'inline-block' }} />
          Cramming Pattern
        </button>
        <button onClick={handleSpacedRepetition} disabled={isAnimating} className="inline-flex items-center gap-1.5 disabled:opacity-40 transition-colors" style={{ backgroundColor: '#e8f5f2', border: '2px solid #2A7D6F', borderRadius: 20, padding: '10px 20px', fontSize: 13, fontWeight: 600, color: '#1a6358' }}>
          <span style={{ width: 6, height: 6, borderRadius: '50%', backgroundColor: '#2A7D6F', display: 'inline-block' }} />
          Spaced Repetition
        </button>
        <button onClick={handleReset} disabled={isAnimating} className="inline-flex items-center gap-1.5 disabled:opacity-40 transition-colors" style={{ backgroundColor: '#FFFFFF', border: '2px solid #d0cdc8', borderRadius: 20, padding: '10px 20px', fontSize: 13, fontWeight: 600, color: '#b0a898' }}>
          Reset
        </button>
      </div>

      {/* Result message */}
      {resultMessage && (
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-4 max-w-lg mx-auto"
          style={{ borderLeft: '3px solid #2A7D6F', backgroundColor: '#f0faf8', borderRadius: '0 10px 10px 0', padding: '12px 16px' }}
        >
          <p className="text-sm italic" style={{ color: '#1a6358' }}>{resultMessage}</p>
        </motion.div>
      )}
    </div>
  );
};

// --- MODULE COMPONENT ---
const NeuroplasticityProtocolModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'paradigm-shift', title: 'The Plastic Brain', eyebrow: '01 // The Paradigm Shift', icon: BrainCircuit },
    { id: 'brain-renovation', title: "The Brain's Renovation", eyebrow: '02 // Sculpt & Upgrade', icon: Wrench },
    { id: 'rulebook-of-learning', title: 'The Rulebook of Learning', eyebrow: '03 // Fire Together, Wire Together', icon: BookOpen },
    { id: 'physical-evidence', title: 'The Physical Evidence', eyebrow: '04 // The Juggling Study', icon: BarChart3 },
    { id: 'learning-blueprint', title: 'The Learning Blueprint', eyebrow: '05 // Why Some Methods Work', icon: ClipboardCheck },
    { id: 'system-maintenance', title: 'System Maintenance', eyebrow: '06 // Sleep & Stress', icon: ShieldCheck },
  ];

  return (
    <ModuleLayout
      moduleNumber="01"
      moduleTitle="Neuroplasticity"
      moduleSubtitle="Your Brain's User Manual"
      moduleDescription="Your brain isn't stuck the way it is -- it physically changes shape when you learn new things. This module shows you how that works and how to make it work for you."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Rewire Your Brain"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Plastic Brain." eyebrow="Step 1" icon={BrainCircuit} theme={theme}>
              <p>People used to think your brain was basically set in stone by the time you were a kid. You were either "smart" or you weren't, and that was that. Turns out, that's completely wrong. Your brain is more like plasticine -- it's constantly being reshaped by what you do, what you think about, and what you practise.</p>
              <p>This ability to change is called <Highlight description="Your brain's ability to physically reshape itself based on what you do and learn. It's basically why practice actually works -- your brain literally builds new wiring for the things you repeat." theme={theme}>Neuroplasticity</Highlight>. And here's the thing: during your teenage years, your brain is more changeable than at almost any other point in your life. It's going through a massive rebuild. Understanding how this works is basically having a cheat code for your own brain.</p>
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The Brain's Renovation." eyebrow="Step 2" icon={Wrench} theme={theme}>
              <p>Your brain is doing two big renovation jobs at once right now. The first is <Highlight description="Your brain cutting away connections you don't use anymore. Think of it like a gardener trimming dead branches so the healthy ones get more energy. It makes your brain faster and more efficient." theme={theme}>Synaptic Pruning</Highlight>. Basically, your brain is like a gardener, trimming away the connections you don't use to free up energy for the ones you do. This is "use it or lose it" in action. If you stop practising something, your brain actually takes apart the wiring for it.</p>
              <p>The second job is <Highlight description="Your brain wrapping insulation around the pathways you use a lot, like upgrading a country lane to a motorway. It makes signals travel way faster, so you can think and react quicker." theme={theme}>Myelination</Highlight>. Think of this as upgrading a bumpy country road to a motorway. Your brain wraps insulation around the pathways you use often, making them super-fast and efficient. Practice doesn't just make perfect -- it makes things <em>faster</em>.</p>
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="The Rulebook of Learning." eyebrow="Step 3" icon={BookOpen} theme={theme}>
              <p>So how does your brain know which connections to keep and which to get rid of? It follows one simple rule: <Highlight description="The basic idea is 'cells that fire together, wire together.' When you practise something and the same brain cells keep activating together, the connection between them gets physically stronger. That's literally how you learn." theme={theme}>"Cells that fire together, wire together"</Highlight>. Every time you think about something or practise a skill, you're sending an electrical signal through a chain of brain cells. The more you fire that same chain, the stronger the physical connections between those cells become.</p>
              <p>Here are two ways to picture it. For strengthening connections, imagine a field of tall grass. The first time you walk across it (studying a topic once), you bend the grass, but it springs back. If you walk the same path over and over, you wear a permanent trail. For speed, think of an orchestra. To make music, different sections need their signals to arrive at the same time. Your brain's insulation works like a conductor, adjusting the speed of different pathways so your thoughts are perfectly timed.</p>
              <DesirePathMaker />
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="The Physical Evidence." eyebrow="Step 4" icon={BarChart3} theme={theme}>
              <p>This isn't just a nice idea -- you can actually see it happening on brain scans. In one well-known experiment, scientists scanned the brains of people who had never juggled. Then they taught them to juggle and scanned them again after three months of practice. The result? The parts of the brain used for tracking moving objects had physically grown.</p>
              <p>But here's the key part: they then told the jugglers to stop practising for three months. The final brain scan showed those same areas had shrunk back down again. Use it or lose it. Your brain is efficient -- it won't waste energy keeping up a skill you've stopped using. The takeaway? Your brain isn't fixed. It's changing shape based on what you do every single day.</p>
              <JugglingStudyVisualizer />
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="The Learning Blueprint." eyebrow="Step 5" icon={ClipboardCheck} theme={theme}>
                <p>All of this tells us <em>why</em> certain study techniques actually work and others are a waste of time. For example, <Highlight description="Going back over material at spaced-out intervals -- like reviewing something after 1 day, then 3 days, then a week. It works because you're reminding your brain 'hey, keep this connection' just before it starts to fade." theme={theme}>Spaced Repetition</Highlight> works because it tells your brain "this is important, keep this pathway." Cramming, on the other hand, is like one intense stampede across the grass -- it doesn't create a trail that lasts.</p>
                <p>Same idea with <Highlight description="Instead of just re-reading your notes, you close the book and try to remember the material from scratch -- using flashcards, practice questions, or just explaining it to yourself. It's harder, but that effort is what forces your brain to actually strengthen the connection." theme={theme}>Active Recall</Highlight>. It's way more effective than just reading over your notes again. Why? Because re-reading is easy, so it sends a weak signal to your brain. Active recall forces your brain to rebuild the whole connection from scratch, and that effort is what makes it stick.</p>
                <StudyMethodGrader />
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="System Maintenance." eyebrow="Step 6" icon={ShieldCheck} theme={theme}>
                <p>Your brain's ability to change depends on how well you look after it. Sleep isn't a luxury -- it's when your brain does its filing and cleaning. While you're asleep, your brain sorts through the connections you made during the day, keeps the important ones, and clears out the junk. Without enough sleep, your brain gets overloaded and can't take in new stuff properly.</p>
                <p>Stress is the other thing that gets in the way. When you're constantly stressed, your body releases a hormone called cortisol that actually blocks your brain from building new connections -- and can even speed up the loss of existing ones, especially around memory. Looking after your stress levels isn't just about feeling better; it directly affects how well you can learn. Once you understand these basics, you can stop accidentally working against your brain and start working with it.</p>
                <MicroCommitment theme={theme}>
                    <p>Tonight, put your phone away 30 minutes before you go to sleep. It's a small change, but it makes a real difference to how well your brain locks in everything you learned today.</p>
                </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default NeuroplasticityProtocolModule;
