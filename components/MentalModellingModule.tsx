
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Eye, Workflow, Box, Film, AlertTriangle, Pyramid
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { cyanTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = cyanTheme;

// --- INTERACTIVE COMPONENTS ---

const GlassBoxUnfolder = () => {
    const [activeView, setActiveView] = useState<'front' | 'top' | 'side' | null>(null);
    const [revealed, setRevealed] = useState(new Set<string>());
    const [showLayout, setShowLayout] = useState(false);

    const handleView = (v: 'front' | 'top' | 'side') => {
        setActiveView(v);
        setRevealed(prev => new Set(prev).add(v));
        if (showLayout) setShowLayout(false);
    };

    /* Isometric projection */
    const S = 22, CX = 155, CY = 120;
    const iso = (x: number, y: number, z: number): [number, number] => [
        CX + (x - y) * 0.866 * S,
        CY + (x + y) * 0.5 * S - z * S,
    ];
    const pts = (verts: number[][]): string =>
        verts.map(([x, y, z]) => iso(x, y, z).join(',')).join(' ');

    /* L-shape: base 3x2x1, tower 1x2x3. Visible faces back-to-front */
    const shapeFaces = [
        { v: [[0,0,3],[1,0,3],[1,2,3],[0,2,3]], fill: '#a5f3fc' },
        { v: [[1,0,1],[3,0,1],[3,2,1],[1,2,1]], fill: '#a5f3fc' },
        { v: [[1,0,1],[1,2,1],[1,2,3],[1,0,3]], fill: '#0891b2' },
        { v: [[3,0,0],[3,2,0],[3,2,1],[3,0,1]], fill: '#0891b2' },
        { v: [[0,0,0],[3,0,0],[3,0,1],[1,0,1],[1,0,3],[0,0,3]], fill: '#22d3ee' },
    ];

    /* Glass box 3x2x3 */
    const boxEdges: number[][][] = [
        [[0,0,0],[3,0,0]], [[3,0,0],[3,2,0]], [[3,2,0],[0,2,0]], [[0,2,0],[0,0,0]],
        [[0,0,3],[3,0,3]], [[3,0,3],[3,2,3]], [[3,2,3],[0,2,3]], [[0,2,3],[0,0,3]],
        [[0,0,0],[0,0,3]], [[3,0,0],[3,0,3]], [[3,2,0],[3,2,3]], [[0,2,0],[0,2,3]],
    ];
    const boxFaces: Record<string, number[][]> = {
        front: [[0,0,0],[3,0,0],[3,0,3],[0,0,3]],
        top:   [[0,0,3],[3,0,3],[3,2,3],[0,2,3]],
        side:  [[3,0,0],[3,2,0],[3,2,3],[3,0,3]],
    };

    const vc = {
        front: { label: 'Front', sub: 'Elevation', color: '#06b6d4' },
        top:   { label: 'Top', sub: 'Plan', color: '#10b981' },
        side:  { label: 'Side', sub: 'End View', color: '#a855f7' },
    };

    const allRevealed = revealed.size === 3;

    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The "Glass Box" Model</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-2">Click each view to see how the 3D object projects onto the glass faces.</p>
            <p className="text-center text-xs text-zinc-400 dark:text-zinc-500 mb-6">Reveal all three, then flatten the box into a drawing layout.</p>

            {/* View buttons */}
            <div className="flex justify-center gap-2 mb-6 flex-wrap">
                {(['front', 'top', 'side'] as const).map(v => {
                    const isActive = activeView === v;
                    const isSeen = revealed.has(v);
                    return (
                        <button key={v} onClick={() => handleView(v)}
                            className={`px-3 py-2 text-xs font-bold rounded-lg border transition-all ${
                                isActive ? 'text-white border-transparent'
                                : isSeen ? 'border-transparent'
                                : 'bg-zinc-50 dark:bg-zinc-900/30 text-zinc-500 dark:text-zinc-400 border-zinc-200 dark:border-zinc-700 hover:border-zinc-400 cursor-pointer'
                            }`}
                            style={
                                isActive ? { backgroundColor: vc[v].color }
                                : isSeen ? { backgroundColor: vc[v].color + '18', color: vc[v].color }
                                : undefined
                            }
                        >
                            {vc[v].label} ({vc[v].sub})
                        </button>
                    );
                })}
            </div>

            <AnimatePresence mode="wait">
                {!showLayout ? (
                    <motion.div key="explorer" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
                        <div className="flex flex-col md:flex-row gap-6 items-center justify-center">
                            {/* Isometric 3D view */}
                            <div className="bg-zinc-50 dark:bg-zinc-900/30 rounded-xl border border-zinc-200 dark:border-zinc-700 p-3">
                                <svg viewBox="0 0 310 220" className="w-full" style={{ maxWidth: 320 }}>
                                    {/* Glass box wireframe */}
                                    {boxEdges.map(([a, b], i) => {
                                        const [x1, y1] = iso(a[0], a[1], a[2]);
                                        const [x2, y2] = iso(b[0], b[1], b[2]);
                                        return <line key={i} x1={x1} y1={y1} x2={x2} y2={y2} stroke="#a1a1aa" strokeWidth="0.7" strokeDasharray="4 2" opacity="0.4" />;
                                    })}

                                    {/* Highlighted glass face */}
                                    {activeView && (
                                        <motion.polygon key={activeView} points={pts(boxFaces[activeView])}
                                            fill={vc[activeView].color} fillOpacity={0.15}
                                            stroke={vc[activeView].color} strokeWidth="1.5" strokeDasharray="6 3"
                                            initial={{ opacity: 0 }} animate={{ opacity: 1 }} />
                                    )}

                                    {/* L-shape solid faces */}
                                    {shapeFaces.map((f, i) => (
                                        <polygon key={i} points={pts(f.v)} fill={f.fill} stroke="#0e7490" strokeWidth="0.8" strokeLinejoin="round" />
                                    ))}

                                    {/* Face labels */}
                                    {(() => {
                                        const [fx, fy] = iso(1.5, -0.4, 1.5);
                                        const [tx, ty] = iso(1.5, 1, 3.5);
                                        const [sx, sy] = iso(3.5, 1, 1.5);
                                        return <>
                                            <text x={fx} y={fy} textAnchor="middle" className="text-[6px] font-bold" fill={activeView === 'front' ? vc.front.color : '#a1a1aa'}>ELEVATION</text>
                                            <text x={tx} y={ty} textAnchor="middle" className="text-[6px] font-bold" fill={activeView === 'top' ? vc.top.color : '#a1a1aa'}>PLAN</text>
                                            <text x={sx} y={sy} textAnchor="middle" className="text-[6px] font-bold" fill={activeView === 'side' ? vc.side.color : '#a1a1aa'}>END VIEW</text>
                                        </>;
                                    })()}
                                </svg>
                            </div>

                            {/* 2D projection panel */}
                            <AnimatePresence mode="wait">
                                {activeView && (
                                    <motion.div key={activeView}
                                        initial={{ opacity: 0, x: 16 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -16 }}
                                        className="flex flex-col items-center min-w-[160px]"
                                    >
                                        <p className="text-[10px] font-bold uppercase tracking-wider mb-3" style={{ color: vc[activeView].color }}>
                                            2D Projection: {vc[activeView].sub}
                                        </p>
                                        <div className="p-4 rounded-xl border" style={{ backgroundColor: vc[activeView].color + '08', borderColor: vc[activeView].color + '30' }}>
                                            {activeView === 'front' && (
                                                <svg viewBox="0 0 106 106" width="120" height="120">
                                                    <path d="M 8 98 L 98 98 L 98 68 L 38 68 L 38 8 L 8 8 Z"
                                                        fill="#06b6d415" stroke="#06b6d4" strokeWidth="2" strokeLinejoin="round" />
                                                </svg>
                                            )}
                                            {activeView === 'top' && (
                                                <svg viewBox="0 0 106 76" width="120" height="86">
                                                    <rect x="8" y="8" width="90" height="60" rx="1"
                                                        fill="#10b98115" stroke="#10b981" strokeWidth="2" />
                                                    <line x1="38" y1="8" x2="38" y2="68" stroke="#10b981" strokeWidth="1" strokeDasharray="4 3" />
                                                </svg>
                                            )}
                                            {activeView === 'side' && (
                                                <svg viewBox="0 0 76 106" width="86" height="120">
                                                    <rect x="8" y="8" width="60" height="90" rx="1"
                                                        fill="#a855f715" stroke="#a855f7" strokeWidth="2" />
                                                    <line x1="8" y1="68" x2="68" y2="68" stroke="#a855f7" strokeWidth="1" strokeDasharray="4 3" />
                                                </svg>
                                            )}
                                        </div>
                                        <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-3 max-w-[220px] text-center">
                                            {activeView === 'front' && 'Looking straight at the front face — you see the distinctive L-profile.'}
                                            {activeView === 'top' && 'Looking straight down — the full footprint. The dashed line shows the hidden step.'}
                                            {activeView === 'side' && 'Looking from the side — base and tower overlap into a rectangle. The dashed line marks the base top.'}
                                        </p>
                                    </motion.div>
                                )}
                            </AnimatePresence>
                        </div>
                    </motion.div>
                ) : (
                    <motion.div key="layout" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
                        <div className="bg-zinc-50 dark:bg-zinc-900/30 rounded-xl border border-zinc-200 dark:border-zinc-700 p-4">
                            <svg viewBox="0 0 260 260" className="w-full mx-auto" style={{ maxWidth: 380, display: 'block' }}>
                                {/* Plan (top, green) */}
                                <rect x="30" y="10" width="90" height="60" fill="#10b98112" stroke="#10b981" strokeWidth="1.5" rx="2" />
                                <line x1="60" y1="10" x2="60" y2="70" stroke="#10b981" strokeWidth="0.8" strokeDasharray="3 2" />
                                <text x="75" y="44" textAnchor="middle" className="text-[8px] font-bold" fill="#10b981">PLAN</text>

                                {/* Elevation (bottom-left, cyan) — L-profile */}
                                <path d="M 30 90 L 60 90 L 60 150 L 120 150 L 120 180 L 30 180 Z"
                                    fill="#06b6d412" stroke="#06b6d4" strokeWidth="1.5" strokeLinejoin="round" />
                                <text x="45" y="170" textAnchor="middle" className="text-[7px] font-bold" fill="#06b6d4">ELEVATION</text>

                                {/* End View (bottom-right, purple) */}
                                <rect x="140" y="90" width="60" height="90" fill="#a855f712" stroke="#a855f7" strokeWidth="1.5" rx="2" />
                                <line x1="140" y1="150" x2="200" y2="150" stroke="#a855f7" strokeWidth="0.8" strokeDasharray="3 2" />
                                <text x="170" y="135" textAnchor="middle" className="text-[7px] font-bold" fill="#a855f7">END VIEW</text>

                                {/* Projection lines: plan to elevation (vertical) */}
                                <line x1="30" y1="70" x2="30" y2="90" stroke="#a1a1aa" strokeWidth="0.6" strokeDasharray="2 2" />
                                <line x1="60" y1="70" x2="60" y2="90" stroke="#a1a1aa" strokeWidth="0.6" strokeDasharray="2 2" />
                                <line x1="120" y1="70" x2="120" y2="90" stroke="#a1a1aa" strokeWidth="0.6" strokeDasharray="2 2" />

                                {/* Projection lines: elevation to end view (horizontal) */}
                                <line x1="120" y1="90" x2="140" y2="90" stroke="#a1a1aa" strokeWidth="0.6" strokeDasharray="2 2" />
                                <line x1="120" y1="150" x2="140" y2="150" stroke="#a1a1aa" strokeWidth="0.6" strokeDasharray="2 2" />
                                <line x1="120" y1="180" x2="140" y2="180" stroke="#a1a1aa" strokeWidth="0.6" strokeDasharray="2 2" />

                                {/* 45 degree transfer line */}
                                <line x1="120" y1="70" x2="140" y2="90" stroke="#a1a1aa" strokeWidth="0.5" strokeDasharray="2 2" opacity="0.6" />
                            </svg>
                            <p className="text-center text-xs text-zinc-500 dark:text-zinc-400 mt-3">
                                The glass box unfolded flat — this is your standard drawing layout. Projection lines connect corresponding edges across views.
                            </p>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>

            {/* Flatten button */}
            {allRevealed && (
                <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="text-center mt-6">
                    <button onClick={() => { setShowLayout(!showLayout); setActiveView(null); }}
                        className="px-4 py-2.5 text-sm font-bold rounded-lg bg-cyan-500 hover:bg-cyan-600 text-white transition-colors"
                    >
                        {showLayout ? 'Back to 3D Box' : 'Flatten to Drawing Layout'}
                    </button>
                </motion.div>
            )}

            {/* Progress hint */}
            {revealed.size > 0 && revealed.size < 3 && !showLayout && (
                <p className="text-center text-xs text-zinc-400 dark:text-zinc-500 mt-4">
                    {3 - revealed.size} view{3 - revealed.size > 1 ? 's' : ''} remaining...
                </p>
            )}
        </div>
    );
};

const CycleOfModelling = () => {
    const steps = ["Decomposition", "Internalization", "Simulation", "Externalization", "Re-Internalization"];
    const [activeStep, setActiveStep] = useState(0);
    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Cycle of Modelling</h4>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">This is the active hypothesis-testing process your brain runs.</p>
             <div className="flex justify-between mb-2">
                {steps.map((step, i) => <div key={step} className={`w-1/5 text-center text-xs font-bold ${i <= activeStep ? 'text-cyan-600' : 'text-zinc-300'}`}>{step}</div>)}
             </div>
             <div className="w-full h-2 bg-zinc-100 dark:bg-zinc-800 rounded-full"><motion.div className="h-full bg-cyan-500 rounded-full" animate={{width: `${(activeStep / (steps.length - 1)) * 100}%`}} /></div>
             <div className="flex justify-center gap-2 mt-4">
                <button onClick={() => setActiveStep(s => Math.max(0, s-1))} className="px-3 py-1 text-xs bg-zinc-200 rounded-md">Prev</button>
                <button onClick={() => setActiveStep(s => Math.min(steps.length-1, s+1))} className="px-3 py-1 text-xs bg-zinc-200 rounded-md">Next</button>
             </div>
        </div>
    );
};

// --- MODULE COMPONENT ---
const MentalModellingModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'minds-eye', title: 'The Mind\'s Eye', eyebrow: '01 // The Hidden Curriculum', icon: Eye },
    { id: 'modelling-cycle', title: 'The Modelling Cycle', eyebrow: '02 // The Process', icon: Workflow },
    { id: 'glass-box', title: 'The "Glass Box" (DCG)', eyebrow: '03 // Geometric Models', icon: Box },
    { id: 'mental-movie', title: 'The "Mental Movie" (Eng)', eyebrow: '04 // Kinematic Models', icon: Film },
    { id: 'procedural-trap', title: 'The Procedural Trap', eyebrow: '05 // The Failure Mode', icon: AlertTriangle },
    { id: 'training-plan', title: 'The Training Plan', eyebrow: '06 // The Action Plan', icon: Pyramid },
  ];

  return (
    <ModuleLayout
      moduleNumber="07"
      moduleTitle="Mental Modelling"
      moduleSubtitle="The Mind's Eye Protocol"
      moduleDescription="Learn to see the answer in your mind's eye. This module deconstructs the 'hidden curriculum' of subjects like DCG and Engineering, teaching you how to build robust mental simulations."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Mind's Eye." eyebrow="Step 1" icon={Eye} theme={theme}>
              <p>In subjects like DCG and Engineering, there's a "hidden curriculum." It's not about what you draw; it's about what you *see* in your head before you draw it. This is <Highlight description="A dynamic, internal simulation of an external system. It's the cognitive workspace where you rotate objects, simulate mechanisms, and visualize unseen structures." theme={theme}>Mental Modelling</Highlight>. It's the difference between blindly following steps and truly understanding the geometry.</p>
              <p>"Spatial ability" isn't one thing. It's a cluster of skills. The big three for the Leaving Cert are: 1) <Highlight description="The 'heavy lifting' skill of imagining a multi-step transformation, like slicing an object or finding where two shapes intersect." theme={theme}>Spatial Visualisation (Vz)</Highlight>, 2) <Highlight description="The ability to rapidly and accurately rotate a rigid object in your mind. This is key for drawing different views of an object." theme={theme}>Mental Rotation</Highlight>, and 3) <Highlight description="Understanding how objects are arranged from a first-person perspective, critical for things like Perspective Drawing." theme={theme}>Spatial Orientation</Highlight>.</p>
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The Modelling Cycle." eyebrow="Step 2" icon={Workflow} theme={theme}>
              <p>How does your brain build a mental model? It runs a 5-step cycle. 1) <strong>Decomposition</strong>: You break the 2D drawing on the exam paper into basic shapes (prisms, cones). 2) <strong>Internalization</strong>: You build a 3D model in your head based on these shapes. 3) <strong>Simulation</strong>: You mentally manipulate this model ("If I look from the side, what will it look like?"). 4) <strong>Externalization</strong>: You draw the line. 5) <strong>Re-internalization</strong>: You check if your drawing matches your mental simulation.</p>
              <p>Here's the key: novice students almost always skip Step 3. They rely on "procedural recipes" ("always draw this line at 45 degrees") instead of running the mental simulation. This works for standard questions, but collapses the moment a novel problem appears.</p>
              <CycleOfModelling />
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The 'Glass Box' (DCG)." eyebrow="Step 3" icon={Box} theme={theme}>
              <p>For DCG, the fundamental mental model is the "Glass Box"—imagining an object suspended in a clear cube, with the Elevation, Plan, and End Views projected onto its faces. The challenge is that you have to mentally construct this 3D reality while working on a 2D page. This becomes incredibly difficult with abstract ideas like the <Highlight description="The line where an imaginary plane (like a cutting plane) intersects one of the reference planes (the floor or wall). It's an abstraction of an abstraction." theme={theme}>Traces of a Plane</Highlight>.</p>
              <p>To solve complex Interpenetration questions, expert modellers use a mental shortcut called the <Highlight description="A mental strategy where you imagine taking thin 2D slices through a complex 3D problem. By solving a series of simpler 2D problems, you can reconstruct the 3D solution." theme={theme}>"Slicing" Heuristic</Highlight>. This reduces the cognitive load by breaking one massive 3D problem into many small, manageable 2D problems.</p>
              <GlassBoxUnfolder/>
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="The 'Mental Movie' (Eng)." eyebrow="Step 4" icon={Film} theme={theme}>
                <p>In Engineering, mental models are less about static form and more about dynamic function. For Mechanisms, you need to create a <Highlight description="The kinematic mental model required for Engineering, where you mentally animate a static 2D diagram to understand its movement and function." theme={theme}>"Mental Movie."</Highlight> You see a static drawing of a windscreen wiper and you must be able to press 'play' in your mind to see how it moves.</p>
                <p>For Materials Science, the models are even more abstract. You have to visualize things you can never see, like the difference between a <Highlight description="A way atoms are arranged in a metal. The ability of atoms to slide along 'slip planes' in an FCC lattice is what makes metals like copper ductile." theme={theme}>Face-Centred Cubic (FCC)</Highlight> and Body-Centred Cubic (BCC) crystal lattice. Without this micro-structural model, definitions of properties like ductility are just meaningless words to be memorized.</p>
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="The Procedural Trap." eyebrow="Step 5" icon={AlertTriangle} theme={theme}>
              <p>The single biggest reason students fail in DCG and Engineering is the <Highlight description="The common teaching and learning failure where students memorize a sequence of steps ('how' to draw something) without understanding the underlying geometric principle ('why' it works)." theme={theme}>"Procedural Trap."</Highlight> They learn to treat geometry as a set of rules for drawing lines on paper, rather than a representation of objects in 3D space.</p>
              <p>This creates a brittle, inflexible knowledge base. A student can perfectly reproduce a standard drawing from the textbook, but when the examiner presents a slightly non-standard problem, they have no mental model to fall back on. Their procedural "recipe" doesn't work, and they are left completely lost. The examiner reports are filled with comments about "conceptual errors"—this is what they mean.</p>
               <MicroCommitment theme={theme}>
                <p>Look back at your last DCG or Engineering drawing. Can you explain *why* you drew each line, in terms of the 3D object? Or did you just follow a memorized sequence of steps?</p>
              </MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="The Training Plan." eyebrow="Step 6" icon={Pyramid} theme={theme}>
              <p>Mental modelling is a teachable skill, not a gift. Like any skill, it must be trained with "progressive overload," moving from simple to complex. The <Highlight description="A curriculum design that revisits spatial skills with increasing levels of abstraction, moving from physical objects to abstract verbal problems." theme={theme}>Spiral of Visualisation</Highlight> is a framework for this training.</p>
              <p><strong>Phase 1: Concrete Manipulation.</strong> Start with physical objects (LEGO, cardboard models). Hold them, rotate them, and sketch them. This is "Touch-See-Draw." <strong>Phase 2: Guided Visualisation.</strong> Use CAD. Before you create a feature, sketch what you *predict* it will look like. Then, compare your sketch to the result. This is "Predict-Verify-Reflect." <strong>Phase 3: Abstract Visualisation.</strong> Solve "Dark Room" problems, where the geometry is described only in words. This is the ultimate test of your mind's eye, and the final preparation for the exam.</p>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default MentalModellingModule;
