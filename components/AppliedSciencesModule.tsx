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
    const [mode, setMode] = useState<'pure' | 'n' | 'p'>('pure');
    const [viewed, setViewed] = useState(new Set<string>(['pure']));

    const handleMode = (m: 'pure' | 'n' | 'p') => {
        setMode(m);
        setViewed(prev => new Set(prev).add(m));
    };

    const cx = 150, cy = 105, dist = 58, ar = 20;
    const neighbors = [
        { x: cx, y: cy - dist },
        { x: cx + dist, y: cy },
        { x: cx, y: cy + dist },
        { x: cx - dist, y: cy },
    ];

    const label = mode === 'pure' ? 'Si' : mode === 'n' ? 'P' : 'B';
    const group = mode === 'pure' ? 'IV' : mode === 'n' ? 'V' : 'III';
    const valence = mode === 'pure' ? 4 : mode === 'n' ? 5 : 3;
    const color = mode === 'pure' ? '#71717a' : mode === 'n' ? '#3b82f6' : '#f43f5e';
    const bgColor = mode === 'pure' ? '#e4e4e7' : mode === 'n' ? '#dbeafe' : '#ffe4e6';

    const info = {
        pure: {
            title: 'Pure Silicon (Intrinsic)',
            desc: 'All 4 valence electrons are locked in covalent bonds with neighbours.',
            result: 'No free charge carriers \u2192 poor conductor.',
        },
        n: {
            title: 'N-Type Doping (Phosphorus)',
            desc: 'Phosphorus has 5 valence electrons. Four bond with Si, but the 5th is free to move.',
            result: 'Free electron = mobile negative charge carrier \u2192 conducts.',
        },
        p: {
            title: 'P-Type Doping (Boron)',
            desc: 'Boron has only 3 valence electrons. It can\u2019t complete all 4 bonds, leaving a gap.',
            result: 'Missing electron = \u201chole\u201d = mobile positive charge carrier \u2192 conducts.',
        },
    };

    const allViewed = viewed.size === 3;

    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Semiconductor Doping</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-2">See how adding impurities creates free charge carriers in silicon.</p>
            <p className="text-center text-xs text-zinc-400 dark:text-zinc-500 mb-6">Toggle between states to understand N-type and P-type doping.</p>

            {/* Toggle */}
            <div className="flex justify-center gap-1 p-1 bg-zinc-100 dark:bg-zinc-900/50 rounded-full mb-6 max-w-xs mx-auto">
                {([['pure', 'Pure Si'], ['n', 'N-Type'], ['p', 'P-Type']] as const).map(([key, lbl]) => (
                    <button key={key} onClick={() => handleMode(key)}
                        className={`flex-1 px-3 py-2 text-xs font-bold rounded-full transition-all ${
                            mode === key
                                ? 'bg-white dark:bg-zinc-700 shadow-sm text-zinc-800 dark:text-white'
                                : 'text-zinc-500 dark:text-zinc-400'
                        }`}
                    >
                        {lbl}
                    </button>
                ))}
            </div>

            {/* Lattice SVG */}
            <div className="bg-zinc-50 dark:bg-zinc-900/30 rounded-xl border border-zinc-200 dark:border-zinc-700 p-3 mb-4">
                <svg viewBox="0 0 300 210" className="w-full mx-auto" style={{ maxWidth: 340 }}>
                    {/* Bonds */}
                    {neighbors.map((n, i) => {
                        const isHole = mode === 'p' && i === 0;
                        return (
                            <line key={`b-${i}`}
                                x1={cx} y1={cy} x2={n.x} y2={n.y}
                                stroke={isHole ? '#f43f5e' : '#d4d4d8'}
                                strokeWidth={isHole ? '1.5' : '2'}
                                strokeDasharray={isHole ? '4 3' : 'none'}
                                opacity={isHole ? 0.5 : 0.8}
                            />
                        );
                    })}

                    {/* Shared electron pairs on bonds */}
                    {neighbors.map((n, i) => {
                        const isHole = mode === 'p' && i === 0;
                        const dx = n.x - cx, dy = n.y - cy;
                        const len = Math.sqrt(dx * dx + dy * dy);
                        const px = (-dy / len) * 3.5, py = (dx / len) * 3.5;
                        const mx = cx + dx * 0.5, my = cy + dy * 0.5;
                        return (
                            <g key={`dots-${i}`}>
                                <circle cx={mx + px} cy={my + py} r="2.5"
                                    fill={isHole ? 'none' : '#a1a1aa'}
                                    stroke={isHole ? '#f43f5e' : 'none'}
                                    strokeWidth="1" strokeDasharray={isHole ? '2 1.5' : ''} />
                                <circle cx={mx - px} cy={my - py} r="2.5" fill="#a1a1aa" />
                            </g>
                        );
                    })}

                    {/* Neighbor Si atoms */}
                    {neighbors.map((n, i) => (
                        <g key={`a-${i}`}>
                            <circle cx={n.x} cy={n.y} r={ar} fill="#fafafa" stroke="#d4d4d8" strokeWidth="1.5" className="dark:fill-zinc-800 dark:stroke-zinc-600" />
                            <text x={n.x} y={n.y + 4} textAnchor="middle" className="text-[10px] font-bold" fill="#71717a">Si</text>
                        </g>
                    ))}

                    {/* Center atom */}
                    <motion.g key={mode} initial={{ scale: 0.85 }} animate={{ scale: 1 }} transition={{ type: 'spring', stiffness: 200 }}>
                        <circle cx={cx} cy={cy} r={ar + 2} fill={bgColor} stroke={color} strokeWidth="2" />
                        <text x={cx} y={cy + 5} textAnchor="middle" className="text-[11px] font-bold" fill={color}>{label}</text>
                    </motion.g>
                    <text x={cx} y={cy + ar + 16} textAnchor="middle" className="text-[6px]" fill={color}>Group {group} \u00b7 {valence}e\u207b</text>

                    {/* Free electron (N-type) */}
                    {mode === 'n' && (
                        <>
                            <motion.g
                                animate={{ x: [0, 14, -6, 12, 0], y: [0, -10, 8, -14, 0] }}
                                transition={{ repeat: Infinity, duration: 4, ease: 'easeInOut' }}
                            >
                                <circle cx={cx + 36} cy={cy - 36} r="7" fill="#3b82f6" />
                                <text x={cx + 36} y={cy - 33.5} textAnchor="middle" className="text-[5px] font-bold" fill="white">e\u207b</text>
                            </motion.g>
                            <text x={cx + 58} y={cy - 48} textAnchor="start" className="text-[7px] font-bold" fill="#3b82f6">FREE</text>
                            <text x={cx + 58} y={cy - 39} textAnchor="start" className="text-[7px] font-bold" fill="#3b82f6">ELECTRON</text>
                        </>
                    )}

                    {/* Hole (P-type) */}
                    {mode === 'p' && (
                        <>
                            <motion.circle
                                cx={cx} cy={cy - dist * 0.5}
                                r="8" fill="none" stroke="#f43f5e" strokeWidth="2" strokeDasharray="3 2"
                                animate={{ scale: [1, 1.2, 1], opacity: [0.8, 1, 0.8] }}
                                transition={{ repeat: Infinity, duration: 1.5 }}
                            />
                            <text x={cx + 14} y={cy - dist * 0.5 + 3} textAnchor="start" className="text-[7px] font-bold" fill="#f43f5e">HOLE</text>
                        </>
                    )}

                    {/* Conductivity label */}
                    <text x={285} y={200} textAnchor="end" className="text-[7px] font-bold"
                        fill={mode === 'pure' ? '#a1a1aa' : color}>
                        {mode === 'pure' ? 'INSULATOR' : 'CONDUCTOR'}
                    </text>
                </svg>
            </div>

            {/* Info panel */}
            <AnimatePresence mode="wait">
                <motion.div key={mode} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
                    className="p-4 rounded-xl border text-center"
                    style={{ backgroundColor: color + '08', borderColor: color + '25' }}
                >
                    <p className="text-[10px] font-bold uppercase tracking-wider mb-1.5" style={{ color }}>{info[mode].title}</p>
                    <p className="text-sm text-zinc-700 dark:text-zinc-300 mb-1">{info[mode].desc}</p>
                    <p className="text-xs font-semibold" style={{ color }}>{info[mode].result}</p>
                </motion.div>
            </AnimatePresence>

            {/* PN Junction insight */}
            {allViewed && (
                <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                    className="text-center text-xs text-zinc-500 dark:text-zinc-400 mt-4">
                    When N-type and P-type meet, electrons fill holes at the boundary \u2014 forming the <span className="font-semibold text-emerald-600 dark:text-emerald-400">PN Junction</span>, the foundation of every diode and transistor.
                </motion.p>
            )}
        </div>
    );
};

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
              <p>For 2026, the prescribed Special Topic is <strong>Semiconductor Technology</strong>. This is a high-stakes question that demands deep theoretical knowledge. You must be able to explain the atomic-level mechanics of <Highlight description="The process of adding impurities to a pure semiconductor to change its electrical properties." theme={theme}>doping</Highlight> to create N-type (free electrons) and P-type ("holes") materials, and how this forms a <Highlight description="The fundamental building block of most semiconductor devices, like diodes and transistors." theme={theme}>PN Junction</Highlight>.</p>
              <p>For the project (25%) and practical (25%), precision is everything. The folio must demonstrate a genuine design process, not be "retro-fitted" to the finished artefact. CAD skills (SolidWorks) are now essential. For the practical exam, the first 45 minutes on <strong>Marking Out</strong> are the most critical; an error here makes the entire piece impossible to assemble correctly.</p>
              <DopingSimulator/>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="DCG: 2026." eyebrow="Step 3" icon={Droplet} theme={theme}>
                <p>The Student Assignment is 40% of your grade. For 2026, the Higher Level theme is <strong>Refillable Soap Dispensers</strong>, and Ordinary Level is <strong>Fidget Toys</strong>. For HL, this means a focus on ergonomics and complex CAD surfacing. You'll need to master SolidWorks features like <Highlight description="A CAD tool for creating complex, organic shapes by connecting a series of profiles." theme={theme}>Loft</Highlight> and <Highlight description="A CAD feature that restricts the movement of components in an assembly, allowing for realistic simulation of mechanisms." theme={theme}>Limit Mates</Highlight> to model the pump mechanism.</p>
                <p>A H1 folio requires more than just good CAD. It needs rich <Highlight description="Explaining how the form of an object relates to its function (e.g., 'the truncated cone shape lowers the centre of gravity, making it more stable')." theme={theme}>Geometric Analysis</Highlight> and photorealistic renders using PhotoView 360 that show an understanding of materials and lighting.</p>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="Computer Science: 2026." eyebrow="Step 4" icon={Code} theme={theme}>
              <p>The 2026 coursework (30%) is themed <strong>"Forests, Climate Change, and Biodiversity."</strong> This requires an ambitious integration of hardware and software. You must build an embedded system using a <Highlight description="The standard microcontroller for the course, featuring integrated sensors and radio capability." theme={theme}>BBC micro:bit</Highlight> with external sensors (e.g., soil moisture, temperature) that sends data to a Python program.</p>
              <p>The Python program must then run a <Highlight description="A 'what-if' model of a forest-related system, like a forest fire simulation, where the probability of ignition is influenced by the real-time data from your micro:bit." theme={theme}>Modelling and Simulation</Highlight>. The crucial element is the feedback loop: the physical data must influence the virtual model, and the model should ideally send a signal back to the hardware. Your final report is a website (HTML/CSS), and a video demo is mandatory.</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Construction & Tech." eyebrow="Step 5" icon={HardHat} theme={theme}>
              <p>In <strong>Construction Studies</strong>, the 2026 exam remains rooted in the existing syllabus but with a heavy emphasis on sustainability. Question 1 (Scale Drawing) is compulsory and requires mastery of detailing rules like <Highlight description="Insulation must be continuous, especially at junctions, to prevent heat loss." theme={theme}>Thermal Continuity</Highlight> and the unbroken <Highlight description="A line on a drawing showing the air barrier, which must be continuous. Taping at joints is essential." theme={theme}>Airtightness Line</Highlight>. For the project (25%) and practical (25%), the focus is on precision joinery and finish.</p>
              <p>In <strong>Technology</strong>, the project is a massive 50% of your grade. A H1 project requires an iterative design loop documented in a folio and the use of <Highlight description="Computer-Aided Design and Computer-Aided Manufacturing, such as using a laser cutter or 3D printer to create parts designed in CAD." theme={theme}>CAD/CAM</Highlight>. The artefact must integrate electronics (PIC/PICAXE microcontrollers) and mechanisms, with a focus on gear ratios and mechanical advantage.</p>
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="Cross-Curricular Synergies." eyebrow="Step 6" icon={Wrench} theme={theme}>
              <p>These subjects share a common DNA. Mastering a concept in one area gives you a massive advantage in another. The <strong>"Control Systems"</strong> thread is the most powerful. The semiconductor physics in Engineering underpins the electronics in Technology and the embedded systems in Computer Science. The <Highlight description="A fundamental electronic circuit used to read a sensor's changing resistance. It is a 'master key' that unlocks sensor integration in all three subjects." theme={theme}>Potential Divider</Highlight> circuit is a universal tool.</p>
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
