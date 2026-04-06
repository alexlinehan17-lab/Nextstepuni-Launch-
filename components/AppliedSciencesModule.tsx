/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Key, Cpu, Droplet, Code, HardHat, Wrench } from 'lucide-react';
import { ModuleProgress } from '../types';
import { emeraldTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment, PersonalStory } from './ModuleShared';
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
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Semiconductor Doping</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-2">See how adding impurities creates free charge carriers in silicon.</p>
            <p className="text-center text-xs text-zinc-400 dark:text-zinc-500 mb-6">Toggle between states to understand N-type and P-type doping.</p>

            {/* Toggle */}
            <div className="flex justify-center gap-1 p-1 bg-zinc-100 dark:bg-zinc-900/50 rounded-full mb-6 max-w-xs mx-auto">
                {([['pure', 'Pure Si'], ['n', 'N-Type'], ['p', 'P-Type']] as const).map(([key, lbl]) => (
                    <button key={key} onClick={() => handleMode(key)}
                        className={`flex-1 px-3 py-2 text-xs font-bold rounded-full transition-all ${
                            mode === key
                                ? 'bg-white text-zinc-800 dark:text-white'
                                : 'text-zinc-500 dark:text-zinc-400'
                        }`}
                        style={mode === key ? { boxShadow: '2px 2px 0px 0px #1C1917' } : {}}
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
    { id: 'convergence', title: 'The Big Picture', eyebrow: '01 // What Ties It All Together', icon: Key },
    { id: 'engineering', title: 'Engineering', eyebrow: '02 // Semiconductors & Your Project', icon: Cpu },
    { id: 'dcg', title: 'DCG', eyebrow: '03 // Soap Dispensers & CAD', icon: Droplet },
    { id: 'cs', title: 'Computer Science', eyebrow: '04 // Forests & Climate', icon: Code },
    { id: 'construction-tech', title: 'Construction & Tech', eyebrow: '05 // Your Project Counts', icon: HardHat },
    { id: 'synergies', title: 'How These Subjects Connect', eyebrow: '06 // Your Action Plan', icon: Wrench },
  ];

  return (
    <ModuleLayout
      moduleNumber="06"
      moduleTitle="Mastering Applied Sciences"
      moduleSubtitle="Your 2026 Project & Exam Guide"
      moduleDescription="Everything you need to know about this year's Engineering, DCG, Computer Science, and Construction projects -- plus how to nail the exams."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Build Your Blueprint"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Big Picture." eyebrow="Step 1" icon={Key} theme={theme}>
              <p>The "practical" subjects are way more than just workshop skills now. You need to show that you can think through a problem, use digital tools, and come up with creative design solutions. The key to a H1 is showing your <Highlight description="Being able to combine your knowledge, your hands-on skills, and your design ideas into one solid piece of work." theme={theme}>technological capability</Highlight> -- that you can bring it all together.</p>
              <p>Across all these subjects, the single biggest reason students lose marks is a gap between the <Highlight description="The actual physical thing you build or make." theme={theme}>"made artefact"</Highlight> (the thing you build) and the <Highlight description="The folder or report where you document your whole design process." theme={theme}>"written account"</Highlight> (the folio where you show your process). A brilliant project with a sloppy folio that looks like you wrote it after the fact will not get a high grade. Telling the story of how you designed it matters just as much as the finished product.</p>
              <PersonalStory name="Oisin" role="6th Year, Waterford">
                <p>I did Engineering and Construction Studies for my LC. In 5th year, I spent ages on my Engineering project but barely touched the folio -- I thought the project would speak for itself. I got a B2. In 6th year, I started the folio from day one, documenting every decision and sketch. Same skill level, way better grade. The folio is where the marks actually are.</p>
              </PersonalStory>
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="Engineering: 2026." eyebrow="Step 2" icon={Cpu} theme={theme}>
              <p>This year's Special Topic is <strong>Semiconductor Technology</strong>. It's a big-mark question, so you really need to understand this stuff. You need to be able to explain how <Highlight description="Adding tiny amounts of other elements to silicon to change how it conducts electricity." theme={theme}>doping</Highlight> works -- how you add impurities to silicon to create N-type (extra electrons floating around) and P-type (gaps where electrons are missing, called 'holes') materials, and what happens when you put them together to form a <Highlight description="Where N-type and P-type materials meet. It's the basic building block inside every diode and transistor." theme={theme}>PN Junction</Highlight>.</p>
              <p>For the project (25%) and practical exam (25%), precision is everything. Your folio needs to show a real design process -- not one you wrote after the fact to match what you already built. CAD skills (SolidWorks, which you'll have access to in school) are essential now. In the practical exam, the first 45 minutes on <strong>Marking Out</strong> are the most important part; if you get this wrong, the whole piece won't fit together properly.</p>
              <DopingSimulator/>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="DCG: 2026." eyebrow="Step 3" icon={Droplet} theme={theme}>
                <p>The Student Assignment is a massive 40% of your grade. For 2026, the Higher Level theme is <strong>Refillable Soap Dispensers</strong>, and Ordinary Level is <strong>Fidget Toys</strong>. For HL, you'll be designing something ergonomic with moving parts, so you'll need to get comfortable with SolidWorks features like <Highlight description="A tool in SolidWorks that lets you create smooth, curved shapes by blending between different cross-sections -- think of the shape of a soap bottle." theme={theme}>Loft</Highlight> and <Highlight description="A setting in SolidWorks assemblies that controls how far parts can move, so you can show your pump mechanism actually working." theme={theme}>Limit Mates</Highlight> to model the pump mechanism.</p>
                <p>A H1 folio needs more than just good 3D models. You should include <Highlight description="Explaining why your design is shaped the way it is -- for example, 'making the base wider stops it tipping over.' It shows you thought about the shape, not just drew it." theme={theme}>Geometric Analysis</Highlight> (explaining why your shapes work the way they do) and photorealistic renders using PhotoView 360 that show you understand materials and lighting. You can access all these tools through SolidWorks in school.</p>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="Computer Science: 2026." eyebrow="Step 4" icon={Code} theme={theme}>
              <p>The 2026 coursework (worth 30%) is themed <strong>"Forests, Climate Change, and Biodiversity."</strong> You need to combine hardware and software into one project. That means building something with a <Highlight description="A small, cheap computer the size of a credit card that your school provides. It has built-in sensors and can talk wirelessly to other devices." theme={theme}>BBC micro:bit</Highlight> plus some external sensors (like soil moisture or temperature sensors, which your school should have) that sends real data to a Python program.</p>
              <p>Your Python program then needs to run a <Highlight description="A 'what-if' program -- like a forest fire simulation where real sensor data (say, temperature) changes what happens in the model." theme={theme}>simulation</Highlight>. The key thing examiners want to see is a feedback loop: your physical sensor data should change what happens in the simulation, and ideally the simulation sends a signal back to the hardware too. Your final report is a website (HTML/CSS), and you also need a video demo showing it all working.</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Construction & Tech." eyebrow="Step 5" icon={HardHat} theme={theme}>
              <p>In <strong>Construction Studies</strong>, the 2026 exam sticks to the existing syllabus but sustainability is a huge focus. Question 1 (Scale Drawing) is compulsory, and you need to nail details like <Highlight description="Insulation can't have gaps -- especially where walls meet roofs or floors. Any break means heat escapes." theme={theme}>Thermal Continuity</Highlight> (no gaps in insulation) and the <Highlight description="A line on your drawing showing where the building is sealed against air leaks. It has to be unbroken -- tape every joint." theme={theme}>Airtightness Line</Highlight> (showing an unbroken air seal). For the project (25%) and practical (25%), clean joinery and a good finish are what matter most.</p>
              <p>In <strong>Technology</strong>, the project is worth a huge 50% of your grade. For a H1, you need to show that you went through a real design process -- trying things, improving them, and documenting it all in your folio. You should use <Highlight description="Designing on a computer (CAD) and then making parts with machines like your school's laser cutter or 3D printer (CAM)." theme={theme}>CAD/CAM</Highlight> (design on the computer, cut or print with the school's laser cutter or 3D printer). Your project also needs to include electronics (PIC/PICAXE microcontrollers) and mechanisms like gears.</p>
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="How These Subjects Connect." eyebrow="Step 6" icon={Wrench} theme={theme}>
              <p>These subjects share a lot of the same ideas. If you learn something well in one, it gives you a head start in another. The biggest overlap is <strong>"Control Systems"</strong> -- the semiconductor stuff in Engineering is the same physics behind the electronics in Technology and the sensor projects in Computer Science. The <Highlight description="A simple circuit that lets you read sensor values. Once you understand it, you can use sensors in Engineering, Technology, and CS." theme={theme}>Potential Divider</Highlight> circuit comes up in all three subjects.</p>
              <p>A really effective study trick is to <Highlight description="Instead of studying one subject for hours, mix topics from different subjects in the same session. It feels harder but you remember more." theme={theme}>mix your study across subjects</Highlight>. When you study logic gates for CS, flip to digital electronics in Engineering straight after. When you learn about energy-efficient buildings (NZEB) in Construction, look at the climate monitoring project in CS. Seeing the same ideas from different angles makes everything stick better.</p>
              <MicroCommitment theme={theme}>
                <p>Pick one connection between two of your subjects mentioned here. Spend 10 minutes drawing a quick mind map showing how the ideas link up. This is how you start seeing the bigger picture.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default AppliedSciencesModule;
