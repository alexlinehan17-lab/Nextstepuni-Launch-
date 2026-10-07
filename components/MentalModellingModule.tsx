import { ConceptSequence } from './learning/WideFeatures';
import { moduleBorder,moduleFill,moduleText } from './learning/brandTokens';

/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import { AnimatePresence,motion } from 'framer-motion';
import {
AlertTriangle,
Box,
Eye,
Film,
Pyramid,
Workflow
} from 'lucide-react';
import React,{ useState } from 'react';
import { MENTAL_MODELLING_REFERENCE_LIST } from '../data/references/mentalModelling';
import { useEssentialsMode } from '../hooks/useEssentialsMode';
import { cyanTheme } from '../moduleThemes';
import { type ModuleProgress } from '../types';
import { ModuleLayout } from './ModuleLayout';
import { Cite } from './ModuleReferences';
import { ConceptCardGrid,Highlight,MicroCommitment,ReadingSection } from './ModuleShared';

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
        { v: [[0,0,3],[1,0,3],[1,2,3],[0,2,3]], fill: "var(--module-surface)" },
        { v: [[1,0,1],[3,0,1],[3,2,1],[1,2,1]], fill: "var(--module-surface)" },
        { v: [[1,0,1],[1,2,1],[1,2,3],[1,0,3]], fill: "var(--module-solid)" },
        { v: [[3,0,0],[3,2,0],[3,2,1],[3,0,1]], fill: "var(--module-solid)" },
        { v: [[0,0,0],[3,0,0],[3,0,1],[1,0,1],[1,0,3],[0,0,3]], fill: "var(--module-surface)" },
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
        front: { label: 'Front', sub: 'Elevation', color: "var(--module-ink)" },
        top:   { label: 'Top', sub: 'Plan', color: "var(--module-success-text)" },
        side:  { label: 'Side', sub: 'End View', color: "var(--module-ink)" },
    };

    const allRevealed = revealed.size === 3;

    return (
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: "var(--module-surface)", borderRadius: 18 }}>
            <h4 className="font-serif text-2xl font-semibold text-[var(--module-ink)] dark:text-[var(--module-ink)] text-center">The "Glass Box" Model</h4>
            <p className="text-center text-sm text-[var(--module-muted)] dark:text-[var(--module-muted)] mb-2">Click each view to see how the 3D object projects onto the glass faces.</p>
            <p className="text-center text-xs text-[var(--module-muted)] dark:text-[var(--module-muted)] mb-6">Reveal all three, then flatten the box into a drawing layout.</p>

            {/* View buttons */}
            <div className="flex justify-center gap-2 mb-6 flex-wrap">
                {(['front', 'top', 'side'] as const).map(v => {
                    const isActive = activeView === v;
                    const isSeen = revealed.has(v);
                    return (
                        <button key={v} onClick={() => handleView(v)}
                            className={`px-3 py-2 text-xs font-bold rounded-lg transition-all`}
                            style={
                                isActive ? { backgroundColor: moduleFill(vc[v].color), color: "var(--module-on-fill)", border: '2.5px solid ' + vc[v].color, borderRadius: 10, boxShadow: 'none' }
                                : isSeen ? { backgroundColor: moduleFill(vc[v].color + '18'), color: moduleText(vc[v].color), border: '2.5px solid ' + vc[v].color + '60', borderRadius: 10 }
                                : { backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", borderRadius: 10, boxShadow: 'none' }
                            } data-wide-button="true" data-selected={!!(isActive)} data-tone="orange" aria-pressed={!!(isActive)}
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
                            <div className="rounded-xl p-3" style={{ backgroundColor: "var(--module-surface)", border: "1.5px solid var(--module-line)" }}>
                                <svg viewBox="0 0 310 220" className="w-full" style={{ maxWidth: 320 }}>
                                    {/* Glass box wireframe */}
                                    {boxEdges.map(([a, b], i) => {
                                        const [x1, y1] = iso(a[0], a[1], a[2]);
                                        const [x2, y2] = iso(b[0], b[1], b[2]);
                                        return <line key={i} x1={x1} y1={y1} x2={x2} y2={y2} stroke="var(--module-muted)" strokeWidth="0.7" strokeDasharray="4 2" opacity="0.4" />;
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
                                        <polygon key={i} points={pts(f.v)} fill={f.fill} stroke="var(--module-ink)" strokeWidth="0.8" strokeLinejoin="round" />
                                    ))}

                                    {/* Face labels */}
                                    {(() => {
                                        const [fx, fy] = iso(1.5, -0.4, 1.5);
                                        const [tx, ty] = iso(1.5, 1, 3.5);
                                        const [sx, sy] = iso(3.5, 1, 1.5);
                                        return <>
                                            <text x={fx} y={fy} textAnchor="middle" className="text-[6px] font-bold" fill={activeView === 'front' ? vc.front.color : "var(--module-surface)"}>ELEVATION</text>
                                            <text x={tx} y={ty} textAnchor="middle" className="text-[6px] font-bold" fill={activeView === 'top' ? vc.top.color : "var(--module-surface)"}>PLAN</text>
                                            <text x={sx} y={sy} textAnchor="middle" className="text-[6px] font-bold" fill={activeView === 'side' ? vc.side.color : "var(--module-surface)"}>END VIEW</text>
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
                                        <p className="text-[10px] font-bold uppercase tracking-wider mb-3" style={{ color: moduleText(vc[activeView].color) }}>
                                            2D Projection: {vc[activeView].sub}
                                        </p>
                                        <div className="p-4 rounded-xl border" style={{ backgroundColor: moduleFill(vc[activeView].color + '08'), borderColor: moduleBorder(vc[activeView].color + '30') }}>
                                            {activeView === 'front' && (
                                                <svg viewBox="0 0 106 106" width="120" height="120">
                                                    <path d="M 8 98 L 98 98 L 98 68 L 38 68 L 38 8 L 8 8 Z"
                                                        fill="var(--module-solid)" stroke="var(--module-ink)" strokeWidth="2" strokeLinejoin="round" />
                                                </svg>
                                            )}
                                            {activeView === 'top' && (
                                                <svg viewBox="0 0 106 76" width="120" height="86">
                                                    <rect x="8" y="8" width="90" height="60" rx="1"
                                                        fill="var(--module-success)" stroke="var(--module-success-text)" strokeWidth="2" />
                                                    <line x1="38" y1="8" x2="38" y2="68" stroke="var(--module-success-text)" strokeWidth="1" strokeDasharray="4 3" />
                                                </svg>
                                            )}
                                            {activeView === 'side' && (
                                                <svg viewBox="0 0 76 106" width="86" height="120">
                                                    <rect x="8" y="8" width="60" height="90" rx="1"
                                                        fill="var(--module-surface)" stroke="var(--module-ink)" strokeWidth="2" />
                                                    <line x1="8" y1="68" x2="68" y2="68" stroke="var(--module-ink)" strokeWidth="1" strokeDasharray="4 3" />
                                                </svg>
                                            )}
                                        </div>
                                        <p className="text-xs text-[var(--module-muted)] dark:text-[var(--module-muted)] mt-3 max-w-[220px] text-center">
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
                        <div className="rounded-xl p-4" style={{ backgroundColor: "var(--module-surface)", border: "1.5px solid var(--module-line)" }}>
                            <svg viewBox="0 0 260 260" className="w-full mx-auto" style={{ maxWidth: 380, display: 'block' }}>
                                {/* Plan (top, green) */}
                                <rect x="30" y="10" width="90" height="60" fill="var(--module-success)" stroke="var(--module-success-text)" strokeWidth="1.5" rx="2" />
                                <line x1="60" y1="10" x2="60" y2="70" stroke="var(--module-success-text)" strokeWidth="0.8" strokeDasharray="3 2" />
                                <text x="75" y="44" textAnchor="middle" className="text-[8px] font-bold" fill="var(--module-success)">PLAN</text>

                                {/* Elevation (bottom-left, cyan) — L-profile */}
                                <path d="M 30 90 L 60 90 L 60 150 L 120 150 L 120 180 L 30 180 Z"
                                    fill="var(--module-solid)" stroke="var(--module-ink)" strokeWidth="1.5" strokeLinejoin="round" />
                                <text x="45" y="170" textAnchor="middle" className="text-[7px] font-bold" fill="var(--module-solid)">ELEVATION</text>

                                {/* End View (bottom-right, purple) */}
                                <rect x="140" y="90" width="60" height="90" fill="var(--module-surface)" stroke="var(--module-ink)" strokeWidth="1.5" rx="2" />
                                <line x1="140" y1="150" x2="200" y2="150" stroke="var(--module-ink)" strokeWidth="0.8" strokeDasharray="3 2" />
                                <text x="170" y="135" textAnchor="middle" className="text-[7px] font-bold" fill="var(--module-surface)">END VIEW</text>

                                {/* Projection lines: plan to elevation (vertical) */}
                                <line x1="30" y1="70" x2="30" y2="90" stroke="var(--module-muted)" strokeWidth="0.6" strokeDasharray="2 2" />
                                <line x1="60" y1="70" x2="60" y2="90" stroke="var(--module-muted)" strokeWidth="0.6" strokeDasharray="2 2" />
                                <line x1="120" y1="70" x2="120" y2="90" stroke="var(--module-muted)" strokeWidth="0.6" strokeDasharray="2 2" />

                                {/* Projection lines: elevation to end view (horizontal) */}
                                <line x1="120" y1="90" x2="140" y2="90" stroke="var(--module-muted)" strokeWidth="0.6" strokeDasharray="2 2" />
                                <line x1="120" y1="150" x2="140" y2="150" stroke="var(--module-muted)" strokeWidth="0.6" strokeDasharray="2 2" />
                                <line x1="120" y1="180" x2="140" y2="180" stroke="var(--module-muted)" strokeWidth="0.6" strokeDasharray="2 2" />

                                {/* 45 degree transfer line */}
                                <line x1="120" y1="70" x2="140" y2="90" stroke="var(--module-muted)" strokeWidth="0.5" strokeDasharray="2 2" opacity="0.6" />
                            </svg>
                            <p className="text-center text-xs text-[var(--module-muted)] dark:text-[var(--module-muted)] mt-3">
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
                        className="px-4 py-2.5 text-sm font-bold rounded-lg bg-[var(--module-solid)] hover:bg-[var(--module-solid)] text-[var(--module-ink)] transition-colors" data-wide-button="true"
                    >
                        {showLayout ? 'Back to 3D Box' : 'Flatten to Drawing Layout'}
                    </button>
                </motion.div>
            )}

            {/* Progress hint */}
            {revealed.size > 0 && revealed.size < 3 && !showLayout && (
                <p className="text-center text-xs text-[var(--module-muted)] dark:text-[var(--module-muted)] mt-4">
                    {3 - revealed.size} view{3 - revealed.size > 1 ? 's' : ''} remaining...
                </p>
            )}
        </div>
    );
};

const CycleOfModelling = () => {
    const steps = [
        { name: "Read the Problem", description: "Understand what the question is asking. Identify the object, the view, and what needs to be drawn." },
        { name: "Build the Mental Model", description: "Picture the 3D object in your mind. Rotate it, zoom in, examine it from different angles." },
        { name: "Plan Your Drawing", description: "Decide which views are needed, what scale to use, and where each view goes on the page." },
        { name: "Execute", description: "Draw with precision. Use construction lines, apply projection rules, and maintain consistent proportions." },
        { name: "Check & Verify", description: "Compare your drawing against the original. Does each view match? Are dimensions consistent?" },
    ];
    const [activeStep, setActiveStep] = useState(0);
    return (
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: "var(--module-surface)", borderRadius: 18 }}>
             <h4 className="font-serif text-2xl font-semibold text-[var(--module-ink)] dark:text-[var(--module-ink)] text-center">The Cycle of Modelling</h4>
             <p className="text-center text-sm text-[var(--module-muted)] dark:text-[var(--module-muted)] mb-8">This is the step-by-step process your brain goes through when you picture something in 3D.</p>
             <div className="flex justify-between mb-2">
                {steps.map((step, i) => <div key={step.name} className={`w-1/5 text-center text-xs font-bold ${i <= activeStep ? "text-[var(--module-ink)]" : "text-[var(--module-muted)]"}`}>{step.name}</div>)}
             </div>
             <div className="w-full h-2 bg-[var(--module-surface)] dark:bg-[var(--module-surface)] rounded-full"><motion.div className="h-full bg-[var(--module-solid)] rounded-full" animate={{width: `${(activeStep / (steps.length - 1)) * 100}%`}} /></div>
             <AnimatePresence mode="wait">
                <motion.p
                    key={activeStep}
                    initial={{ opacity: 0, y: 6 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -6 }}
                    transition={{ duration: 0.25 }}
                    className="text-center text-sm text-[var(--module-ink)] dark:text-[var(--module-muted)] mt-4 px-4"
                >
                    {steps[activeStep].description}
                </motion.p>
             </AnimatePresence>
             <div className="flex justify-center gap-2 mt-4">
                <button onClick={() => setActiveStep(s => Math.max(0, s-1))} className="px-3 py-1 text-xs bg-[var(--module-surface)] dark:bg-[var(--module-surface)] dark:text-[var(--module-ink)] rounded-md" data-wide-button="true">Prev</button>
                <button onClick={() => setActiveStep(s => Math.min(steps.length-1, s+1))} className="px-3 py-1 text-xs bg-[var(--module-surface)] dark:bg-[var(--module-surface)] dark:text-[var(--module-ink)] rounded-md" data-wide-button="true">Next</button>
             </div>
        </div>
    );
};

// --- MODULE COMPONENT ---
const MentalModellingModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const essentials = useEssentialsMode();
  const sections = [
    { id: 'minds-eye', title: 'The Mind\'s Eye', eyebrow: '01 // The Skill Nobody Teaches', icon: Eye },
    { id: 'modelling-cycle', title: 'The Modelling Cycle', eyebrow: '02 // The Process', icon: Workflow },
    { id: 'glass-box', title: 'The "Glass Box" (DCG)', eyebrow: '03 // Picturing Shapes', icon: Box },
    { id: 'mental-movie', title: 'The "Mental Movie" (Eng)', eyebrow: '04 // Picturing Movement', icon: Film },
    { id: 'procedural-trap', title: 'The Procedural Trap', eyebrow: '05 // Where Students Get Stuck', icon: AlertTriangle },
    { id: 'training-plan', title: 'The Training Plan', eyebrow: '06 // The Action Plan', icon: Pyramid },
  ];

  return (
    <ModuleLayout
      moduleNumber="09"
      moduleTitle="Mental Modelling"
      moduleSubtitle="The Mind's Eye Method"
      moduleDescription="Learn to see the answer in your head before you put pen to paper. In subjects like DCG and Engineering, the real skill isn't drawing — it's picturing 3D objects in your mind. This module shows you how."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="See It Clearly"
      references={MENTAL_MODELLING_REFERENCE_LIST}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Mind's Eye." eyebrow="Step 1" icon={Eye} theme={theme}>
              {essentials ? (
                <>
                  <p>In DCG and Engineering, the real skill is seeing shapes in your head before you draw them. This is <Highlight description="Building a 3D picture in your head that you can spin and test." theme={theme}>Mental Modelling</Highlight>. It is actually three skills bundled together:<Cite n={1} /><Cite n={2} /></p>
                  <ConceptCardGrid
                    cards={[
                      { number: 1, term: "Spatial Visualisation", description: "The ability to imagine something changing shape step by step — like picturing what happens when you slice through a 3D object, or where two shapes overlap." },
                      { number: 2, term: "Mental Rotation", description: "Being able to spin an object around in your head quickly and accurately. This is what you need when you're drawing different views of the same object." },
                      { number: 3, term: "Spatial Orientation", description: "Understanding how things look from different positions — like imagining you're standing somewhere else in the room. This is key for things like Perspective Drawing." },
                    ]}
                  />
                </>
              ) : (
                <>
                  <p>In subjects like DCG and Engineering, there's a skill nobody actually teaches you — but everyone expects you to have. It's not about what you draw; it's about what you can <em>see</em> in your head before you draw it. This is <Highlight description="Your ability to build a picture in your head — like a 3D model you can spin around, take apart, and test — all without touching a pencil." theme={theme}>Mental Modelling</Highlight>. It's the difference between blindly following steps and truly understanding the shape or mechanism you're working with.</p>
                  <p>This "seeing in your head" skill isn't just one thing. It's actually a few different skills bundled together. The big three for these subjects are:<Cite n={1} /><Cite n={2} /></p>
                  <ConceptCardGrid
                    cards={[
                      { number: 1, term: "Spatial Visualisation", description: "The ability to imagine something changing shape step by step — like picturing what happens when you slice through a 3D object, or where two shapes overlap." },
                      { number: 2, term: "Mental Rotation", description: "Being able to spin an object around in your head quickly and accurately. This is what you need when you're drawing different views of the same object." },
                      { number: 3, term: "Spatial Orientation", description: "Understanding how things look from different positions — like imagining you're standing somewhere else in the room. This is key for things like Perspective Drawing." },
                    ]}
                  />
                </>
              )}
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The Modelling Cycle." eyebrow="Step 2" icon={Workflow} theme={theme}>
              <p>So how does your brain actually build a picture of something? It follows a 5-step loop.</p>
              <ConceptSequence kind="spatial">
                <div className="p-4 flex items-start gap-4" style={{ backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", borderRadius: 16, boxShadow: 'none' }}>
                  <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-[var(--module-ink)]" style={{ backgroundColor: "var(--module-solid)" }}>1</div>
                  <div>
                    <p className="text-sm font-bold" style={{ color: "var(--module-ink)" }}>Break it down</p>
                    <p className="text-[13px] mt-0.5" style={{ color: "var(--module-ink)", opacity: 0.8 }}>You look at the flat drawing on the exam paper and split it into simple shapes (boxes, cylinders, cones).</p>
                  </div>
                </div>
                <div className="p-4 flex items-start gap-4" style={{ backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", borderRadius: 16, boxShadow: 'none' }}>
                  <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-[var(--module-ink)]" style={{ backgroundColor: "var(--module-danger)" }}>2</div>
                  <div>
                    <p className="text-sm font-bold" style={{ color: "var(--module-danger-text)" }}>Build it in your head</p>
                    <p className="text-[13px] mt-0.5" style={{ color: "var(--module-danger-text)", opacity: 0.8 }}>You piece those shapes together into a 3D picture in your mind.</p>
                  </div>
                </div>
                <div className="p-4 flex items-start gap-4" style={{ backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", borderRadius: 16, boxShadow: 'none' }}>
                  <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-[var(--module-ink)]" style={{ backgroundColor: "var(--module-danger)" }}>3</div>
                  <div>
                    <p className="text-sm font-bold" style={{ color: "var(--module-danger-text)" }}>Test it mentally</p>
                    <p className="text-[13px] mt-0.5" style={{ color: "var(--module-danger-text)", opacity: 0.8 }}>You spin it around, zoom in, ask yourself "what would this look like from the side?"</p>
                  </div>
                </div>
                <div className="p-4 flex items-start gap-4" style={{ backgroundColor: "var(--module-success-soft)", border: "2.5px solid var(--module-line)", borderRadius: 16, boxShadow: 'none' }}>
                  <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-[var(--module-ink)]" style={{ backgroundColor: "var(--module-success)" }}>4</div>
                  <div>
                    <p className="text-sm font-bold" style={{ color: "var(--module-success-text)" }}>Draw it out</p>
                    <p className="text-[13px] mt-0.5" style={{ color: "var(--module-success-text)", opacity: 0.8 }}>You put your pencil on the page and draw what you see.</p>
                  </div>
                </div>
                <div className="p-4 flex items-start gap-4" style={{ backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", borderRadius: 16, boxShadow: 'none' }}>
                  <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-[var(--module-ink)]" style={{ backgroundColor: "var(--module-solid)" }}>5</div>
                  <div>
                    <p className="text-sm font-bold" style={{ color: "var(--module-ink)" }}>Check your work</p>
                    <p className="text-[13px] mt-0.5" style={{ color: "var(--module-ink)", opacity: 0.8 }}>You compare what you drew with what you pictured — do they match?</p>
                  </div>
                </div>
              </ConceptSequence>
              {essentials ? (
                <p>Most students skip the "test it mentally" step. They memorise drawing rules instead of picturing the object. This works for standard questions but breaks on anything new.</p>
              ) : (
                <p>Here's the important part: most students skip Step 3 entirely. They fall back on memorised rules ("always draw this line at 45 degrees") instead of actually picturing the object. This gets you through standard questions, but the moment the exam throws you something slightly different, you're stuck — because you never really understood the shape in the first place.</p>
              )}
              <CycleOfModelling />
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The 'Glass Box' (DCG)." eyebrow="Step 3" icon={Box} theme={theme}>
              {essentials ? (
                <p>Imagine an object inside a see-through cube. Front, Top, and Side views project onto the glass faces. For tough Interpenetration questions, use <Highlight description="Take thin flat slices through a 3D shape to simplify the problem." theme={theme}>"Slicing"</Highlight>. Break one big 3D problem into many simpler flat problems. Try the interactive tool below.</p>
              ) : (
                <>
                  <p>For DCG, the key mental picture is the "Glass Box" — imagine an object floating inside a see-through cube, with the Front View, Top View, and Side View projected onto the glass faces. The tricky part is that you have to build this 3D picture in your head while working on a flat 2D page. This gets really hard with abstract ideas like the <Highlight description="The line you get where an imaginary flat surface (like a cutting plane) meets one of the main reference surfaces (like the floor or wall in your drawing). It's a tricky concept because you're imagining something invisible meeting something else invisible." theme={theme}>Traces of a Plane</Highlight>.</p>
                  <p>To tackle those tough Interpenetration questions, strong students use a mental shortcut called <Highlight description="A trick where you imagine taking thin flat slices through a complicated 3D shape. Instead of trying to solve one huge 3D problem all at once, you solve a bunch of simpler flat problems one at a time, then piece the answer together." theme={theme}>"Slicing"</Highlight>. Instead of trying to solve one huge 3D problem in your head all at once, you break it into lots of smaller, simpler flat problems — much easier to handle.</p>
                </>
              )}
              <GlassBoxUnfolder/>
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="The 'Mental Movie' (Eng)." eyebrow="Step 4" icon={Film} theme={theme}>
                {essentials ? (
                  <p>In Engineering, you picture how things move. Create a <Highlight description="Press play in your head to see how a mechanism moves." theme={theme}>"Mental Movie"</Highlight> from flat diagrams. For Materials Science, you picture invisible things like <Highlight description="How atoms are stacked inside a metal — this determines if it bends or snaps." theme={theme}>crystal structures</Highlight>. If you cannot picture atom arrangements, words like "ductility" stay meaningless.</p>
                ) : (
                  <>
                    <p>In Engineering, it's less about picturing still shapes and more about picturing how things <em>move</em>. For Mechanisms, you need to create a <Highlight description="The ability to look at a flat diagram of a mechanism and 'press play' in your head �� imagining how all the parts move together, like watching a short video in your mind." theme={theme}>"Mental Movie."</Highlight> You see a flat drawing of a windscreen wiper on the page, and you need to be able to press 'play' in your head to see how it actually moves.</p>
                    <p>For Materials Science, it gets even trickier. You have to picture things you can never actually see with your eyes, like the difference between a <Highlight description="A pattern for how atoms are stacked inside a metal. The way atoms are arranged determines whether a metal bends easily (like copper) or snaps. Picturing this arrangement helps you understand why different metals behave differently." theme={theme}>Face-Centred Cubic (FCC)</Highlight> and Body-Centred Cubic (BCC) crystal structure. If you can't picture how atoms are stacked, then definitions like "ductility" are just empty words you're trying to memorise without understanding.</p>
                  </>
                )}
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="The Procedural Trap." eyebrow="Step 5" icon={AlertTriangle} theme={theme}>
              {essentials ? (
                <p>The biggest mistake is the <Highlight description="Memorising drawing steps without understanding the 3D shape they represent." theme={theme}>"Procedural Trap."</Highlight> You memorise steps instead of understanding the shape.<Cite n={3} /> This works for textbook drawings but breaks on anything new. Examiners call these "conceptual errors."</p>
              ) : (
                <>
                  <p>The single biggest reason students struggle in DCG and Engineering is the <Highlight description="When you memorise the steps to draw something ('first draw this line, then this arc') without actually understanding why those steps work. You know the recipe but you don't understand the cooking." theme={theme}>"Procedural Trap."</Highlight> You end up treating geometry as a set of rules for drawing lines on paper, instead of understanding that those lines represent real 3D objects in space.<Cite n={3} /></p>
                  <p>The problem is that this kind of knowledge is fragile. You can perfectly copy a standard drawing from the textbook, but the moment the exam gives you something slightly different, you're lost — because you never actually understood the shape, you just memorised the steps. The examiner reports come back every year saying students make "conceptual errors" — and this is exactly what they're talking about.</p>
                </>
              )}
               <MicroCommitment theme={theme}>
                <p>Look back at your last DCG or Engineering drawing. Can you explain <em>why</em> you drew each line, in terms of the 3D object? Or did you just follow a memorized sequence of steps?</p>
              </MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="The Training Plan." eyebrow="Step 6" icon={Pyramid} theme={theme}>
              {essentials ? (
                <p>You can train this skill. It is not a talent you either have or do not have.<Cite n={4} /> The <Highlight description="Start with physical objects, move to predicting on screen, finish picturing shapes from words alone." theme={theme}>Spiral of Visualisation</Highlight> gives you a roadmap.<Cite n={5} /> Three phases:</p>
              ) : (
                <p>Here's the good news: this "seeing in your head" skill is something you can actually train — it's not a talent you either have or don't.<Cite n={4} /> Like any skill, you build it up gradually, starting easy and working your way to the hard stuff. The <Highlight description="A step-by-step training approach where you start by handling real objects, move on to predicting what things look like on screen, and finish by picturing shapes described only in words — each stage stretching your mind's eye a bit further." theme={theme}>Spiral of Visualisation</Highlight> gives you a roadmap for doing exactly that.<Cite n={5} /></p>
              )}
              <ConceptSequence kind="spatial">
                <div className="p-4 flex items-start gap-4" style={{ backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", borderRadius: 16, boxShadow: 'none' }}>
                  <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-[var(--module-ink)]" style={{ backgroundColor: "var(--module-solid)" }}>1</div>
                  <div>
                    <p className="text-sm font-bold" style={{ color: "var(--module-ink)" }}>Phase 1: Get Hands-On</p>
                    <p className="text-[13px] mt-0.5" style={{ color: "var(--module-ink)", opacity: 0.8 }}>Start with physical objects — LEGO, cardboard models, anything you can hold. Pick them up, turn them around, and sketch what you see. Touch it, see it, draw it.</p>
                  </div>
                </div>
                <div className="p-4 flex items-start gap-4" style={{ backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", borderRadius: 16, boxShadow: 'none' }}>
                  <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-[var(--module-ink)]" style={{ backgroundColor: "var(--module-danger)" }}>2</div>
                  <div>
                    <p className="text-sm font-bold" style={{ color: "var(--module-danger-text)" }}>Phase 2: Predict and Check</p>
                    <p className="text-[13px] mt-0.5" style={{ color: "var(--module-danger-text)", opacity: 0.8 }}>Use CAD software. Before you click to create a shape, sketch what you think it will look like. Then compare your sketch to what actually appears on screen. Predict it, check it, learn from the difference.</p>
                  </div>
                </div>
                <div className="p-4 flex items-start gap-4" style={{ backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", borderRadius: 16, boxShadow: 'none' }}>
                  <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-[var(--module-ink)]" style={{ backgroundColor: "var(--module-danger)" }}>3</div>
                  <div>
                    <p className="text-sm font-bold" style={{ color: "var(--module-danger-text)" }}>Phase 3: Pure Imagination</p>
                    <p className="text-[13px] mt-0.5" style={{ color: "var(--module-danger-text)", opacity: 0.8 }}>Try "Dark Room" problems, where a shape is described only in words and you have to picture it entirely in your head. This is the ultimate test of your mind's eye — and the best prep for exam day.</p>
                  </div>
                </div>
              </ConceptSequence>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default MentalModellingModule;
