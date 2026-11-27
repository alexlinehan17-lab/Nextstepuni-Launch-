/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Key, Cpu, Droplet, Code, HardHat, Wrench } from 'lucide-react';
import { type ModuleProgress } from '../types';
import { emeraldTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment, PersonalStory } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';
import { useEssentialsMode } from '../hooks/useEssentialsMode';
import { AnswerLine, ExerciseSheet } from './learning/Exercise';
import { SelectionBar } from './ui/Choice';

const theme = emeraldTheme;

/** The exercise's title: on the sheet, and the name of its selection bar. */
const DOPING_TITLE = 'Semiconductor Doping';

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
    // The drawing's own colours, in tokens: pure silicon in the quieter ink, a doped atom in full ink
    const color = mode === 'pure' ? 'var(--ink-secondary)' : 'var(--ink-primary)';
    const svgText = { fontFamily: 'var(--font-ui)' };

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
        <ExerciseSheet title={DOPING_TITLE} sub="See how adding impurities creates free charge carriers in silicon." name="DopingSimulator">
            <p className="t-meta">Toggle between states to understand N-type and P-type doping.</p>

            {/* Toggle: the system's selection bar (three short choices), named by the sheet's own title */}
            <SelectionBar
                label={DOPING_TITLE}
                value={mode}
                onChange={handleMode}
                options={([['pure', 'Pure Si'], ['n', 'N-Type'], ['p', 'P-Type']] as const).map(([key, lbl]) => ({ value: key, label: lbl }))}
            />

            {/* Lattice SVG: the drawing on the sheet (no grey box of its own) */}
            <div className="ex-figure">
                <svg viewBox="0 0 300 210" className="ex-figure-art w-full" style={{ maxWidth: 340 }}>
                    {/* Bonds */}
                    {neighbors.map((n, i) => {
                        const isHole = mode === 'p' && i === 0;
                        return (
                            <line key={`b-${i}`}
                                x1={cx} y1={cy} x2={n.x} y2={n.y}
                                stroke={isHole ? 'var(--ink-primary)' : 'var(--outline-soft)'}
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
                                    fill={isHole ? 'none' : 'var(--ink-muted)'}
                                    stroke={isHole ? 'var(--ink-primary)' : 'none'}
                                    strokeWidth="1" strokeDasharray={isHole ? '2 1.5' : ''} />
                                <circle cx={mx - px} cy={my - py} r="2.5" fill="var(--ink-muted)" />
                            </g>
                        );
                    })}

                    {/* Neighbor Si atoms */}
                    {neighbors.map((n, i) => (
                        <g key={`a-${i}`}>
                            <circle cx={n.x} cy={n.y} r={ar} fill="var(--surface-paper)" stroke="var(--outline-soft)" strokeWidth="1.5" />
                            <text x={n.x} y={n.y + 4} textAnchor="middle" fontSize="11" style={svgText} fill="var(--ink-secondary)">Si</text>
                        </g>
                    ))}

                    {/* Center atom */}
                    <motion.g key={mode} initial={{ scale: 0.85 }} animate={{ scale: 1 }} transition={{ type: 'spring', stiffness: 200 }}>
                        <circle cx={cx} cy={cy} r={ar + 2} fill="var(--surface-paper)" stroke={color} strokeWidth="2" />
                        <text x={cx} y={cy + 5} textAnchor="middle" fontSize="13" style={svgText} fill={color}>{label}</text>
                    </motion.g>
                    {/* the group line sits on the bond, so a paper-coloured edge keeps it readable */}
                    <text x={cx} y={cy + ar + 16} textAnchor="middle" fontSize="11" style={{ ...svgText, paintOrder: 'stroke' }} stroke="var(--surface-paper)" strokeWidth="4" fill={color}>Group {group} \u00b7 {valence}e\u207b</text>

                    {/* Free electron (N-type) */}
                    {mode === 'n' && (
                        <>
                            <motion.g
                                animate={{ x: [0, 14, -6, 12, 0], y: [0, -10, 8, -14, 0] }}
                                transition={{ repeat: Infinity, duration: 4, ease: 'easeInOut' }}
                            >
                                <circle cx={cx + 36} cy={cy - 36} r="9" fill="var(--ink-primary)" />
                                <text x={cx + 36} y={cy - 32} textAnchor="middle" fontSize="11" style={svgText} fill="var(--surface-paper)">e\u207b</text>
                            </motion.g>
                            <text x={cx + 58} y={cy - 52} textAnchor="start" fontSize="11" style={svgText} fill="var(--ink-primary)" letterSpacing="0.1em">FREE</text>
                            <text x={cx + 58} y={cy - 39} textAnchor="start" fontSize="11" style={svgText} fill="var(--ink-primary)" letterSpacing="0.1em">ELECTRON</text>
                        </>
                    )}

                    {/* Hole (P-type) */}
                    {mode === 'p' && (
                        <>
                            <motion.circle
                                cx={cx} cy={cy - dist * 0.5}
                                r="8" fill="none" stroke="var(--ink-primary)" strokeWidth="2" strokeDasharray="3 2"
                                animate={{ scale: [1, 1.2, 1], opacity: [0.8, 1, 0.8] }}
                                transition={{ repeat: Infinity, duration: 1.5 }}
                            />
                            <text x={cx + 14} y={cy - dist * 0.5 + 4} textAnchor="start" fontSize="11" style={svgText} fill="var(--ink-primary)" letterSpacing="0.1em">HOLE</text>
                        </>
                    )}

                    {/* Conductivity label */}
                    <text x={285} y={200} textAnchor="end" fontSize="11" style={svgText} letterSpacing="0.1em"
                        fill={mode === 'pure' ? 'var(--ink-muted)' : color}>
                        {mode === 'pure' ? 'INSULATOR' : 'CONDUCTOR'}
                    </text>
                </svg>
            </div>

            {/* Info panel: words you read, under the state's label and a hairline (no tinted box) */}
            <AnimatePresence mode="wait">
                <motion.div key={mode} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
                    className="ex-block"
                >
                    <p className="ex-label">{info[mode].title}</p>
                    <p className="ex-block-text">{info[mode].desc}</p>
                    <p className="t-body text-ink-primary">{info[mode].result}</p>
                </motion.div>
            </AnimatePresence>

            {/* PN Junction insight: once all three states are seen, a line in ink with the tick */}
            {allViewed && (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                    <AnswerLine>
                    When N-type and P-type meet, electrons fill holes at the boundary \u2014 forming the <b>PN Junction</b>, the foundation of every diode and transistor.
                    </AnswerLine>
                </motion.div>
            )}
        </ExerciseSheet>
    );
};

// --- MODULE COMPONENT ---
const AppliedSciencesModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const essentials = useEssentialsMode();
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
              {essentials ? (
                <>
                  <p>These subjects test more than workshop skills. You need to show <Highlight description="Combining knowledge, hands-on skills, and design ideas into one piece of work." theme={theme}>technological capability</Highlight>. The biggest reason students lose marks is a gap between the <Highlight description="The thing you build." theme={theme}>"made artefact"</Highlight> and the <Highlight description="The report documenting your design process." theme={theme}>"written account"</Highlight>. Your folio matters just as much as your finished project. Start documenting from day one.</p>
                  <PersonalStory name="Oisin" role="6th Year, Waterford">
                    <p>I did Engineering and Construction Studies for my LC. In 5th year, I spent ages on my Engineering project but barely touched the folio -- I thought the project would speak for itself. It didn’t go well. In 6th year, I started the folio from day one, documenting every decision and sketch. Same skill level, way better grade. The folio is where the marks actually are.</p>
                  </PersonalStory>
                </>
              ) : (
                <>
                  <p>The "practical" subjects are way more than just workshop skills now. You need to show that you can think through a problem, use digital tools, and come up with creative design solutions. The key to a H1 is showing your <Highlight description="Being able to combine your knowledge, your hands-on skills, and your design ideas into one solid piece of work." theme={theme}>technological capability</Highlight> -- that you can bring it all together.</p>
                  <p>Across all these subjects, the single biggest reason students lose marks is a gap between the <Highlight description="The actual physical thing you build or make." theme={theme}>"made artefact"</Highlight> (the thing you build) and the <Highlight description="The folder or report where you document your whole design process." theme={theme}>"written account"</Highlight> (the folio where you show your process). A brilliant project with a sloppy folio that looks like you wrote it after the fact will not get a high grade. Telling the story of how you designed it matters just as much as the finished product.</p>
                  <PersonalStory name="Oisin" role="6th Year, Waterford">
                    <p>I did Engineering and Construction Studies for my LC. In 5th year, I spent ages on my Engineering project but barely touched the folio -- I thought the project would speak for itself. I got a B2. In 6th year, I started the folio from day one, documenting every decision and sketch. Same skill level, way better grade. The folio is where the marks actually are.</p>
                  </PersonalStory>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="Engineering: 2026." eyebrow="Step 2" icon={Cpu} theme={theme}>
              {essentials ? (
                <>
                  <p>The 2026 Special Topic is <strong>Semiconductor Technology</strong>. Learn how <Highlight description="Adding impurities to silicon to change conductivity." theme={theme}>doping</Highlight> creates N-type and P-type materials and how they form a <Highlight description="Where N-type and P-type meet — the building block of diodes and transistors." theme={theme}>PN Junction</Highlight>. For the project and practical, show a real design process in your folio. Master CAD (SolidWorks). In the practical, <strong>Marking Out</strong> in the first 45 minutes is the most important step.</p>
                </>
              ) : (
                <>
                  <p>This year's Special Topic is <strong>Semiconductor Technology</strong>. It's a big-mark question, so you really need to understand this stuff. You need to be able to explain how <Highlight description="Adding tiny amounts of other elements to silicon to change how it conducts electricity." theme={theme}>doping</Highlight> works -- how you add impurities to silicon to create N-type (extra electrons floating around) and P-type (gaps where electrons are missing, called 'holes') materials, and what happens when you put them together to form a <Highlight description="Where N-type and P-type materials meet. It's the basic building block inside every diode and transistor." theme={theme}>PN Junction</Highlight>.</p>
                  <p>For the project (25%) and practical exam (25%), precision is everything. Your folio needs to show a real design process -- not one you wrote after the fact to match what you already built. CAD skills (SolidWorks, which you'll have access to in school) are essential now. In the practical exam, the first 45 minutes on <strong>Marking Out</strong> are the most important part; if you get this wrong, the whole piece won't fit together properly.</p>
                </>
              )}
              <DopingSimulator/>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="DCG: 2026." eyebrow="Step 3" icon={Droplet} theme={theme}>
                {essentials ? (
                  <p>The Student Assignment is 40% of your grade. HL theme: <strong>Refillable Soap Dispensers</strong>. OL: <strong>Fidget Toys</strong>. Master SolidWorks features like <Highlight description="A tool for creating smooth curved shapes." theme={theme}>Loft</Highlight> and <Highlight description="Controls how far parts can move in assemblies." theme={theme}>Limit Mates</Highlight>. For a H1, include <Highlight description="Explaining why your shapes work." theme={theme}>Geometric Analysis</Highlight> and photorealistic renders using PhotoView 360.</p>
                ) : (
                  <>
                    <p>The Student Assignment is a massive 40% of your grade. For 2026, the Higher Level theme is <strong>Refillable Soap Dispensers</strong>, and Ordinary Level is <strong>Fidget Toys</strong>. For HL, you'll be designing something ergonomic with moving parts, so you'll need to get comfortable with SolidWorks features like <Highlight description="A tool in SolidWorks that lets you create smooth, curved shapes by blending between different cross-sections -- think of the shape of a soap bottle." theme={theme}>Loft</Highlight> and <Highlight description="A setting in SolidWorks assemblies that controls how far parts can move, so you can show your pump mechanism actually working." theme={theme}>Limit Mates</Highlight> to model the pump mechanism.</p>
                    <p>A H1 folio needs more than just good 3D models. You should include <Highlight description="Explaining why your design is shaped the way it is -- for example, 'making the base wider stops it tipping over.' It shows you thought about the shape, not just drew it." theme={theme}>Geometric Analysis</Highlight> (explaining why your shapes work the way they do) and photorealistic renders using PhotoView 360 that show you understand materials and lighting. You can access all these tools through SolidWorks in school.</p>
                  </>
                )}
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="Computer Science: 2026." eyebrow="Step 4" icon={Code} theme={theme}>
              {essentials ? (
                <p>The 2026 coursework (30%) is themed <strong>"Forests, Climate Change, and Biodiversity."</strong> Combine a <Highlight description="A small credit-card-sized computer with sensors." theme={theme}>BBC micro:bit</Highlight> with sensors to send real data to a Python <Highlight description="A what-if program driven by real sensor data." theme={theme}>simulation</Highlight>. Examiners want a feedback loop: sensor data changes the simulation and the simulation signals the hardware. Submit a website report and video demo.</p>
              ) : (
                <>
                  <p>The 2026 coursework (worth 30%) is themed <strong>"Forests, Climate Change, and Biodiversity."</strong> You need to combine hardware and software into one project. That means building something with a <Highlight description="A small, cheap computer the size of a credit card that your school provides. It has built-in sensors and can talk wirelessly to other devices." theme={theme}>BBC micro:bit</Highlight> plus some external sensors (like soil moisture or temperature sensors, which your school should have) that sends real data to a Python program.</p>
                  <p>Your Python program then needs to run a <Highlight description="A 'what-if' program -- like a forest fire simulation where real sensor data (say, temperature) changes what happens in the model." theme={theme}>simulation</Highlight>. The key thing examiners want to see is a feedback loop: your physical sensor data should change what happens in the simulation, and ideally the simulation sends a signal back to the hardware too. Your final report is a website (HTML/CSS), and you also need a video demo showing it all working.</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Construction & Tech." eyebrow="Step 5" icon={HardHat} theme={theme}>
              {essentials ? (
                <p><strong>Construction Studies:</strong> Sustainability is a huge focus. Nail <Highlight description="No gaps in insulation." theme={theme}>Thermal Continuity</Highlight> and the <Highlight description="An unbroken line showing where the building is sealed against air." theme={theme}>Airtightness Line</Highlight> in your Scale Drawing. Clean joinery matters most. <strong>Technology:</strong> The project is 50% of your grade. Show a real design process. Use <Highlight description="Design on computer, make parts with laser cutter or 3D printer." theme={theme}>CAD/CAM</Highlight>. Include electronics and mechanisms.</p>
              ) : (
                <>
                  <p>In <strong>Construction Studies</strong>, the 2026 exam sticks to the existing syllabus but sustainability is a huge focus. Question 1 (Scale Drawing) is compulsory, and you need to nail details like <Highlight description="Insulation can't have gaps -- especially where walls meet roofs or floors. Any break means heat escapes." theme={theme}>Thermal Continuity</Highlight> (no gaps in insulation) and the <Highlight description="A line on your drawing showing where the building is sealed against air leaks. It has to be unbroken -- tape every joint." theme={theme}>Airtightness Line</Highlight> (showing an unbroken air seal). For the project (25%) and practical (25%), clean joinery and a good finish are what matter most.</p>
                  <p>In <strong>Technology</strong>, the project is worth a huge 50% of your grade. For a H1, you need to show that you went through a real design process -- trying things, improving them, and documenting it all in your folio. You should use <Highlight description="Designing on a computer (CAD) and then making parts with machines like your school's laser cutter or 3D printer (CAM)." theme={theme}>CAD/CAM</Highlight> (design on the computer, cut or print with the school's laser cutter or 3D printer). Your project also needs to include electronics (PIC/PICAXE microcontrollers) and mechanisms like gears.</p>
                </>
              )}
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="How These Subjects Connect." eyebrow="Step 6" icon={Wrench} theme={theme}>
              {essentials ? (
                <p>These subjects overlap heavily. The biggest connection is "Control Systems." The <Highlight description="A circuit for reading sensor values. Appears in Engineering, Technology, and CS." theme={theme}>Potential Divider</Highlight> circuit shows up in Engineering, Technology, and CS. <Highlight description="Mixing topics from different subjects in one session." theme={theme}>Mix your study across subjects</Highlight>. Study logic gates for CS, then do digital electronics in Engineering. Same idea, different angle, better memory.</p>
              ) : (
                <>
                  <p>These subjects share a lot of the same ideas. If you learn something well in one, it gives you a head start in another. The biggest overlap is <strong>"Control Systems"</strong> -- the semiconductor stuff in Engineering is the same physics behind the electronics in Technology and the sensor projects in Computer Science. The <Highlight description="A simple circuit that lets you read sensor values. Once you understand it, you can use sensors in Engineering, Technology, and CS." theme={theme}>Potential Divider</Highlight> circuit comes up in all three subjects.</p>
                  <p>A really effective study trick is to <Highlight description="Instead of studying one subject for hours, mix topics from different subjects in the same session. It feels harder but you remember more." theme={theme}>mix your study across subjects</Highlight>. When you study logic gates for CS, flip to digital electronics in Engineering straight after. When you learn about energy-efficient buildings (NZEB) in Construction, look at the climate monitoring project in CS. Seeing the same ideas from different angles makes everything stick better.</p>
                </>
              )}
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
