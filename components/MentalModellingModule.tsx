
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
    const [isUnfolded, setIsUnfolded] = useState(false);
    return(
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700 flex flex-col items-center">
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The "Glass Box" Model</h4>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">This is the fundamental mental model for orthographic projection.</p>
             <div className="w-48 h-48 [perspective:1000px] mb-8">
                <motion.div className="relative w-full h-full" style={{ transformStyle: 'preserve-3d', transform: 'rotateX(-20deg) rotateY(-30deg)' }} animate={{scale: isUnfolded ? 0.8 : 1}}>
                    {/* Front */}
                    <motion.div className="absolute w-48 h-48 border border-cyan-500 bg-cyan-500/10 flex items-center justify-center" style={{transformOrigin: 'bottom'}} animate={{rotateX: isUnfolded ? -90 : 0, y: isUnfolded ? 96 : 0 }}><span className="font-bold">ELEVATION</span></motion.div>
                    {/* Top */}
                    <motion.div className="absolute w-48 h-48 border border-cyan-500 bg-cyan-500/10 flex items-center justify-center" style={{transformOrigin: 'top'}} animate={{transform: `rotateX(90deg) translateZ(96px)`, rotateX: isUnfolded ? -90 : 90, y: isUnfolded ? -96 : 0}}><span className="font-bold">PLAN</span></motion.div>
                     {/* Side */}
                    <motion.div className="absolute w-48 h-48 border border-cyan-500 bg-cyan-500/10 flex items-center justify-center" style={{transformOrigin: 'left'}} animate={{transform: `rotateY(-90deg) translateZ(96px)`, rotateY: isUnfolded ? 90 : -90, x: isUnfolded ? -96 : 0}}><span className="font-bold">END VIEW</span></motion.div>
                </motion.div>
             </div>
             <button onClick={() => setIsUnfolded(!isUnfolded)} className="px-4 py-2 bg-cyan-500 text-white font-bold rounded-lg">{isUnfolded ? 'Fold Box' : 'Unfold Box'}</button>
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
