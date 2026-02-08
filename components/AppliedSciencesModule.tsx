/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Key, Cpu, Droplet, Code, HardHat, Wrench } from 'lucide-react';
import { ModuleProgress } from '../types';
import { emeraldTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = emeraldTheme;

// --- INTERACTIVE COMPONENTS ---
const DopingSimulator = () => {
    const [doping, setDoping] = useState<'n'|'p'|null>(null);
    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-semibold text-stone-800 text-center italic">Semiconductor Doping</h4>
            <div className="flex justify-center gap-4 my-4">
                <button onClick={()=>setDoping('n')} className="px-4 py-2 bg-blue-100 text-blue-800 rounded-lg">N-Type Doping</button>
                <button onClick={()=>setDoping('p')} className="px-4 py-2 bg-rose-100 text-rose-800 rounded-lg">P-Type Doping</button>
            </div>
            {doping && <p className="text-center text-sm">{doping === 'n' ? 'Introducing Phosphorus (Group V) creates a free electron.' : 'Introducing Boron (Group III) creates a "hole".'}</p>}
        </div>
    );
}

// --- MODULE COMPONENT ---
const AppliedSciencesModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'convergence', title: 'The Convergence', eyebrow: '01 // The Core Idea', icon: Key },
    { id: 'engineering', title: 'Engineering', eyebrow: '02 // Semiconductor Focus', icon: Cpu },
    { id: 'dcg', title: 'DCG', eyebrow: '03 // Soap Dispensers & CAD', icon: Droplet },
    { id: 'cs', title: 'Computer Science', eyebrow: '04 // Forests & Climate', icon: Code },
    { id: 'construction-tech', title: 'Construction & Tech', eyebrow: '05 // The Artefact', icon: HardHat },
    { id: 'synergies', title: 'Cross-Curricular Synergies', eyebrow: '06 // The Action Plan', icon: Wrench },
  ];

  return (
    <ModuleLayout
      moduleNumber="06"
      moduleTitle="Mastering Applied Sciences"
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Convergence." eyebrow="Step 1" icon={Key} theme={theme}>
              <p>The "practical" subjects are no longer just about workshop skills. They represent the cutting edge of STEM education, demanding a synthesis of theoretical knowledge, digital fluency, and design innovation. The key to a H1 is demonstrating this <Highlight description="The ability to synthesize theoretical knowledge, manual/digital dexterity, and design innovation into a coherent whole." theme={theme}>technological capability</Highlight>.</p>
              <p>Across all these subjects, the single biggest cause of lost marks is a disconnect between the <Highlight description="The physical project or artefact you create." theme={theme}>"made artefact"</Highlight> and the <Highlight description="The design folio or report that documents the process." theme={theme}>"written account."</Highlight> A brilliant project with a poor folio that looks "retro-fitted" will not achieve a high grade. The narrative of your design process is as important as the final product.</p>
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="Engineering: 2026." eyebrow="Step 2" icon={Cpu} theme={theme}>
              <p>For 2026, the prescribed Special Topic is **Semiconductor Technology**. This is a high-stakes question that demands deep theoretical knowledge. You must be able to explain the atomic-level mechanics of <Highlight description="The process of adding impurities to a pure semiconductor to change its electrical properties." theme={theme}>doping</Highlight> to create N-type (free electrons) and P-type ("holes") materials, and how this forms a <Highlight description="The fundamental building block of most semiconductor devices, like diodes and transistors." theme={theme}>PN Junction</Highlight>.</p>
              <p>For the project (25%) and practical (25%), precision is everything. The folio must demonstrate a genuine design process, not be "retro-fitted" to the finished artefact. CAD skills (SolidWorks) are now essential. For the practical exam, the first 45 minutes on **Marking Out** are the most critical; an error here makes the entire piece impossible to assemble correctly.</p>
              <DopingSimulator/>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="DCG: 2026." eyebrow="Step 3" icon={Droplet} theme={theme}>
                <p>The Student Assignment is 40% of your grade. For 2026, the Higher Level theme is **Refillable Soap Dispensers**, and Ordinary Level is **Fidget Toys**. For HL, this means a focus on ergonomics and complex CAD surfacing. You'll need to master SolidWorks features like <Highlight description="A CAD tool for creating complex, organic shapes by connecting a series of profiles." theme={theme}>Loft</Highlight> and <Highlight description="A CAD feature that restricts the movement of components in an assembly, allowing for realistic simulation of mechanisms." theme={theme}>Limit Mates</Highlight> to model the pump mechanism.</p>
                <p>A H1 folio requires more than just good CAD. It needs rich <Highlight description="Explaining how the form of an object relates to its function (e.g., 'the truncated cone shape lowers the centre of gravity, making it more stable')." theme={theme}>Geometric Analysis</Highlight> and photorealistic renders using PhotoView 360 that show an understanding of materials and lighting.</p>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="Computer Science: 2026." eyebrow="Step 4" icon={Code} theme={theme}>
              <p>The 2026 coursework (30%) is themed **"Forests, Climate Change, and Biodiversity."** This requires an ambitious integration of hardware and software. You must build an embedded system using a <Highlight description="The standard microcontroller for the course, featuring integrated sensors and radio capability." theme={theme}>BBC micro:bit</Highlight> with external sensors (e.g., soil moisture, temperature) that sends data to a Python program.</p>
              <p>The Python program must then run a <Highlight description="A 'what-if' model of a forest-related system, like a forest fire simulation, where the probability of ignition is influenced by the real-time data from your micro:bit." theme={theme}>Modelling and Simulation</Highlight>. The crucial element is the feedback loop: the physical data must influence the virtual model, and the model should ideally send a signal back to the hardware. Your final report is a website (HTML/CSS), and a video demo is mandatory.</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Construction & Tech." eyebrow="Step 5" icon={HardHat} theme={theme}>
              <p>In **Construction Studies**, the 2026 exam remains rooted in the existing syllabus but with a heavy emphasis on sustainability. Question 1 (Scale Drawing) is compulsory and requires mastery of detailing rules like <Highlight description="Insulation must be continuous, especially at junctions, to prevent heat loss." theme={theme}>Thermal Continuity</Highlight> and the unbroken <Highlight description="A line on a drawing showing the air barrier, which must be continuous. Taping at joints is essential." theme={theme}>Airtightness Line</Highlight>. For the project (25%) and practical (25%), the focus is on precision joinery and finish.</p>
              <p>In **Technology**, the project is a massive 50% of your grade. A H1 project requires an iterative design loop documented in a folio and the use of <Highlight description="Computer-Aided Design and Computer-Aided Manufacturing, such as using a laser cutter or 3D printer to create parts designed in CAD." theme={theme}>CAD/CAM</Highlight>. The artefact must integrate electronics (PIC/PICAXE microcontrollers) and mechanisms, with a focus on gear ratios and mechanical advantage.</p>
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="Cross-Curricular Synergies." eyebrow="Step 6" icon={Wrench} theme={theme}>
              <p>These subjects share a common DNA. Mastering a concept in one area gives you a massive advantage in another. The **"Control Systems"** thread is the most powerful. The semiconductor physics in Engineering underpins the electronics in Technology and the embedded systems in Computer Science. The <Highlight description="A fundamental electronic circuit used to read a sensor's changing resistance. It is a 'master key' that unlocks sensor integration in all three subjects." theme={theme}>Potential Divider</Highlight> circuit is a universal tool.</p>
              <p>To maximize your learning, you must use <Highlight description="The cognitive science technique of mixing related topics from different subjects in one study session. This strengthens retention and builds flexible knowledge." theme={theme}>Interleaved Practice</Highlight>. When you study logic gates for CS, immediately review digital electronics in Engineering. When you learn about NZEB in Construction, review climate monitoring in CS. This builds the web of interconnected knowledge that the new curriculum demands.</p>
              <MicroCommitment theme={theme}>
                <p>Pick one cross-curricular link mentioned here. Spend 10 minutes creating a quick mind map showing how the concepts connect across the different subjects. You're starting to think like an integrated engineer.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default AppliedSciencesModule;
