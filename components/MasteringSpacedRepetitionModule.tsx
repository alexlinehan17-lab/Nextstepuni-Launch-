
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Clock, BarChart2, CalendarDays, RadioTower, Wrench, Brain, RefreshCcw, TrendingDown
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { skyTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = skyTheme;

// --- INTERACTIVE COMPONENTS ---
const ForgettingCurveVisualizer = () => {
    const [reviews, setReviews] = useState([false, false, false]);

    const reviewPoints = [ { day: 1, x: 125 }, { day: 3, x: 250 }, { day: 7, x: 375 }];
    const viewboxWidth = 500;
    const viewboxHeight = 150;

    const generatePathData = (activeReviews: boolean[]) => {
        let path = `M 0 5`;
        let lastY = 5;
        const decayFactors = [0.6, 0.4, 0.2, 0.1];

        const activeReviewXs = reviewPoints.map(p => p.x).filter((_, i) => activeReviews[i]);
        const allPoints = [0, ...activeReviewXs, viewboxWidth];

        for (let i = 0; i < allPoints.length - 1; i++) {
            const startX = allPoints[i];
            const currentY = (i > 0) ? 5 : 5;

            if (i > 0) path += ` L ${startX} 5`;

            const endX = allPoints[i];
            const duration = allPoints[i + 1] - startX;
            const endY = currentY + (viewboxHeight - 10) * decayFactors[i];

            path += ` C ${startX + duration * 0.3} ${currentY}, ${endX + duration * 0.7} ${endY}, ${allPoints[i+1]} ${endY}`;
            lastY = endY;
        }
        return { path, lastY };
    };

    const { path: activePath, lastY: activeLastY } = generatePathData(reviews);
    const baselinePath = `M 0 5 C ${viewboxWidth*0.3} 5, ${viewboxWidth*0.7} ${viewboxHeight - 20}, ${viewboxWidth} ${viewboxHeight - 20}`;
    const activeAreaPath = activePath + ` L ${viewboxWidth} ${viewboxHeight} L 0 ${viewboxHeight} Z`;
    const baselineAreaPath = baselinePath + ` L ${viewboxWidth} ${viewboxHeight} L 0 ${viewboxHeight} Z`;

    const retention = { baseline: 21, r0: 21, r1: 55, r2: 78, r3: 95 };
    const currentReviewCount = reviews.filter(Boolean).length;
    const currentRetention = retention[`r${currentReviewCount}` as keyof typeof retention];

    const handleReviewClick = (index: number) => {
        const newReviews = [...reviews];
        newReviews[index] = !newReviews[index];
        // Ensure sequential activation for a clearer story
        if (newReviews[index]) {
            for (let i = 0; i <= index; i++) newReviews[i] = true;
        } else {
             for (let i = index; i < newReviews.length; i++) newReviews[i] = false;
        }
        setReviews(newReviews);
    };

    return (
        <div className="my-10 p-6 md:p-8 bg-stone-900 rounded-[3rem] border border-white/10 shadow-2xl text-white shadow-[inset_0_2px_4px_0_rgba(255,255,255,0.05)]">
            <h4 className="font-serif text-2xl font-semibold text-center italic">The Forgetting Curve</h4>
            <p className="text-center text-sm text-stone-400 mb-8">Click review points on the timeline to fight the curve.</p>

            <div className="relative h-56">
                <svg viewBox={`0 0 ${viewboxWidth} ${viewboxHeight}`} className="w-full h-full overflow-visible">
                    <defs>
                        <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
                            <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
                            <feMerge>
                                <feMergeNode in="coloredBlur"/>
                                <feMergeNode in="SourceGraphic"/>
                            </feMerge>
                        </filter>
                        <linearGradient id="skyGradient" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#0ea5e9" stopOpacity="0.4"/><stop offset="100%" stopColor="#0ea5e9" stopOpacity="0"/></linearGradient>
                        <linearGradient id="redGradient" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#ef4444" stopOpacity="0.2"/><stop offset="100%" stopColor="#ef4444" stopOpacity="0"/></linearGradient>
                    </defs>

                    {/* Y-Axis Labels */}
                    <text x="-10" y="10" fontSize="10" fill="#6b7280" textAnchor="end">100%</text>
                    <text x="-10" y={viewboxHeight-5} fontSize="10" fill="#6b7280" textAnchor="end">0%</text>

                    {/* Baseline Curve */}
                    <path d={baselineAreaPath} fill="url(#redGradient)" />
                    <path d={baselinePath} stroke="#ef4444" strokeWidth="2" strokeDasharray="4 4" fill="none" />
                    <circle cx={viewboxWidth} cy={viewboxHeight - 20} r="4" fill="#ef4444" />

                    {/* Active Curve */}
                    <motion.path d={activeAreaPath} fill="url(#skyGradient)" initial={{opacity:0}} animate={{opacity:1}} transition={{ duration: 0.7, ease: "easeInOut" }} />
                    <motion.path d={activePath} stroke="#0ea5e9" strokeWidth="3" fill="none" style={{filter: 'drop-shadow(0 0 5px #0ea5e9)'}} transition={{ duration: 0.7, ease: "easeInOut" }} />
                    <motion.circle cx={viewboxWidth} cy={activeLastY} r="4" fill="#0ea5e9" style={{filter: 'drop-shadow(0 0 5px #0ea5e9)'}} transition={{ duration: 0.7, ease: "easeInOut" }} />

                    {/* Interactive Points */}
                    {reviewPoints.map((point, i) => (
                        <g key={`point-${i}`} onClick={() => handleReviewClick(i)} className="cursor-pointer">
                            <circle cx={point.x} cy="5" r="8" fill="#0ea5e9" fillOpacity={reviews[i] ? 1 : 0.2} style={{filter: 'drop-shadow(0 0 8px #0ea5e9aa)'}}/>
                            <circle cx={point.x} cy="5" r="4" fill="white" />
                        </g>
                    ))}
                </svg>
            </div>

             <div className="relative grid grid-cols-4 gap-2 pt-4 -mt-4">
                {reviewPoints.map((point, index) => (
                    <div key={index} className="text-center col-start-2" style={{ gridColumnStart: index + 2 }}>
                        <p className="text-xs text-stone-400 mt-2">Day {point.day}</p>
                    </div>
                ))}
            </div>

            <div className="mt-8 grid grid-cols-2 gap-4 items-center bg-white/5 p-4 rounded-xl">
                <div>
                    <p className="flex items-center gap-2 text-xs font-bold uppercase text-stone-400"><TrendingDown size={14} className="text-rose-400"/>Baseline</p>
                    <p className="text-3xl font-semibold text-rose-400 tracking-tighter">{retention.baseline}%</p>
                </div>
                 <div className="text-right">
                    <p className="flex items-center justify-end gap-2 text-xs font-bold uppercase text-stone-400"><Clock size={14} className="text-sky-400"/>Your Retention</p>
                    <p className="text-3xl font-semibold text-sky-400 tracking-tighter">{currentRetention}%</p>
                </div>
                 <div className="col-span-2 text-center">
                    <button onClick={() => setReviews([false, false, false])} className="inline-flex items-center gap-2 text-xs text-stone-500 hover:text-white transition-colors px-3 py-1 rounded-full hover:bg-white/10"><RefreshCcw size={12}/>Reset</button>
                 </div>
            </div>
        </div>
    );
};


const OptimalScheduleCalculator = () => {
    const [ri, setRi] = useState<string>('1_week');

    const schedules = {
        '1_week': { gap: '1-2 Days', ratio: '20-40%', example: 'Study Mon, Review Weds, Test next Mon.' },
        '1_month': { gap: '1 Week', ratio: '~20%', example: 'Study Week 1, Review Week 2, Test Week 5.' },
        '3_months': { gap: '2 Weeks', ratio: '~15%', example: 'Mid-term review should be 2 weeks after intro.' },
        '6_months': { gap: '3 Weeks', ratio: '~10-12%', example: 'Long-term prep requires substantial spacing.' },
    };

    return(
         <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-semibold text-stone-800 text-center italic">Optimal Schedule Calculator</h4>
             <p className="text-center text-sm text-stone-500 mb-6">Based on the landmark Cepeda et al. (2008) research.</p>
             <div className="flex items-center justify-center gap-4">
                 <label className="font-bold">My test is in:</label>
                 <select value={ri} onChange={e => setRi(e.target.value)} className="p-2 bg-stone-100 rounded-lg">
                    <option value="1_week">1 Week</option>
                    <option value="1_month">1 Month</option>
                    <option value="3_months">3 Months</option>
                    <option value="6_months">6 Months</option>
                 </select>
             </div>
             <div className="mt-6 p-6 bg-sky-50 border-2 border-dashed border-sky-200 rounded-2xl text-center">
                <p className="text-sm text-sky-800">Optimal Review Gap (ISI):</p>
                <p className="font-bold text-2xl text-sky-600">{schedules[ri as keyof typeof schedules].gap}</p>
                <p className="text-xs text-sky-500 mt-4"><strong>Actionable Advice:</strong> {schedules[ri as keyof typeof schedules].example}</p>
             </div>
        </div>
    );
};


// --- MODULE COMPONENT ---
const MasteringSpacedRepetitionModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'forgetting-curve', title: 'The Forgetting Curve', eyebrow: '01 // The Default Setting', icon: Clock },
    { id: 'cramming-paradox', title: 'The Cramming Paradox', eyebrow: '02 // The Illusion of Speed', icon: BarChart2 },
    { id: 'desirable-difficulty', title: 'Desirable Difficulty', eyebrow: '03 // The Brain\'s Trigger', icon: Brain },
    { id: 'optimal-schedule', title: 'The Optimal Schedule', eyebrow: '04 // The Ridgeline Rule', icon: CalendarDays },
    { id: 'algorithmic-tools', title: 'Algorithmic Tools', eyebrow: '05 // The Autopilot', icon: RadioTower },
    { id: 'spacing-blueprint', title: 'Your Spacing Blueprint', eyebrow: '06 // The Action Plan', icon: Wrench },
  ];

  return (
    <ModuleLayout moduleNumber="03" moduleTitle="Spaced Repetition" theme={theme} sections={sections} onBack={onBack} progress={progress} onProgressUpdate={onProgressUpdate}>
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Forgetting Curve." eyebrow="Step 1" icon={Clock} theme={theme}>
              <p>Your brain is designed to forget. This isn't a flaw; it's a feature. To survive, your brain has to constantly discard useless information. The problem is, it defaults to forgetting almost everything. This process was first mapped in 1885 by Hermann Ebbinghaus, who discovered the <Highlight description="The mathematical certainty that, without active reinforcement, your memory for new information will decay exponentially over time." theme={theme}>Forgetting Curve</Highlight>.</p>
              <p>The curve is brutal. Without reviewing, you can lose over 50% of new information within an hour, and up to 80% within a day. This is why "cramming" is a catastrophic waste of time. To build lasting knowledge, you can't just put information *in* to your brain; you have to interrupt the process of it leaking *out*.</p>
              <ForgettingCurveVisualizer />
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="The Cramming Paradox." eyebrow="Step 2" icon={BarChart2} theme={theme}>
                <p>If cramming is so bad, why does everyone do it? Because of a metacognitive trap called the <Highlight description="The common student experience where massed practice (cramming) leads to high immediate test performance but catastrophic long-term forgetting, reinforcing an ineffective study habit." theme={theme}>Cramming Paradox</Highlight>. For tests that happen immediately after studying (minutes or hours), cramming works. It keeps information active in your temporary working memory, creating a powerful "Illusion of Competence."</p>
                <p>This gives you a false sense of security. You score well on the immediate test, which "rewards" the cramming behaviour. But the information never gets consolidated into long-term memory. As the research shows, for the same amount of study time, <Highlight description="Also called Distributed Practice. The method of spreading study sessions out over time, which is proven to be vastly superior to cramming for long-term retention." theme={theme}>Spaced Practice</Highlight> can triple the durability of your memory.</p>
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="Desirable Difficulty." eyebrow="Step 3" icon={Brain} theme={theme}>
              <p>Why is spacing so much more powerful? Because it leverages the "struggle" of forgetting. This is the principle of <Highlight description="A learning task that requires a considerable but desirable amount of effort, thereby improving long-term performance. Spacing creates this by allowing some forgetting to occur between sessions." theme={theme}>Desirable Difficulty</Highlight>. When you space out your study, you allow your memory to fade slightly. When you come back to review it, your brain has to work harder to retrieve it.</p>
              <p>This effortful retrieval is a powerful biological signal. It tells your brain, "This information is important! I had to work hard to find it, so I should strengthen the pathway to make it easier next time." Cramming eliminates this difficulty; the information is always right there, so your brain sees no reason to invest the resources in building a strong, long-term memory trace.</p>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="The Optimal Schedule." eyebrow="Step 4" icon={CalendarDays} theme={theme}>
              <p>So, what is the perfect gap between study sessions? There's no single magic number. Landmark research by Cepeda and Pashler found that the <Highlight description="The Inter-Study Interval (ISI) is the time gap between your study sessions." theme={theme}>Optimal Gap</Highlight> depends entirely on when you need to remember the information—the <Highlight description="The Retention Interval (RI) is the time between your last study session and the final test." theme={theme}>Retention Interval</Highlight>.</p>
              <p>Their "Ridgeline Rule" gives us a practical ratio: to maximize recall, your review gap should be roughly **5-20%** of the time until the test. For a test in a week, you need a short gap (1-2 days). For a test in 6 months, you need a much longer gap (e.g., 3 weeks). This is because a longer gap allows for more forgetting, creating a more "desirable difficulty" and triggering a stronger memory consolidation process for the long haul.</p>
              <OptimalScheduleCalculator />
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="Algorithmic Tools." eyebrow="Step 5" icon={RadioTower} theme={theme}>
              <p>Managing the optimal schedule for thousands of facts across dozens of subjects is humanly impossible. This is where <Highlight description="Software (like Anki or SuperMemo) that uses algorithms based on the Forgetting Curve and Spacing Effect to automatically schedule reviews for individual pieces of information (like flashcards)." theme={theme}>Spaced Repetition Software (SRS)</Highlight> comes in. These tools are like a personal tutor for your memory.</p>
              <p>Using an app like Anki, you create digital flashcards. Each time you review a card, you tell the algorithm how difficult it was ("Again," "Hard," "Good," "Easy"). The algorithm then uses this feedback to predict when you'll be on the verge of forgetting that specific card and schedules it for review at that precise moment. It automates the entire process of optimal scheduling, ensuring you review the right thing at the right time.</p>
              <MicroCommitment theme={theme}>
                <p>Download Anki on your phone or computer. Don't worry about making cards yet. Just get the tool. This is the first step to building an automated, long-term memory system.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="Your Spacing Blueprint." eyebrow="Step 6" icon={Wrench} theme={theme}>
              <p>You now have the science to defeat the Forgetting Curve. The timing of your study is as important as the content. This section provides a simple, actionable heuristic to put this into practice immediately, even without software.</p>
              <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
                <h4 className="font-serif text-2xl font-semibold text-stone-800 text-center italic">Actionable Advice: The Heuristic Planner</h4>
                <p className="text-center text-sm text-stone-500 mb-8">For any test or exam, follow this simple rule-of-thumb schedule.</p>
                <div className="grid grid-cols-3 gap-4 text-center">
                    <div className="p-4 bg-stone-50 rounded-xl">
                        <p className="font-bold">Day 1: Learn</p>
                        <p className="text-xs mt-1">First exposure to the material in class.</p>
                    </div>
                     <div className="p-4 bg-stone-50 rounded-xl">
                        <p className="font-bold">Day 2-3: First Review</p>
                        <p className="text-xs mt-1">Review the material using Active Recall. This is the most critical review.</p>
                    </div>
                     <div className="p-4 bg-stone-50 rounded-xl">
                        <p className="font-bold">Day 7 (or before test): Final Review</p>
                        <p className="text-xs mt-1">A final active recall session to consolidate the memory.</p>
                    </div>
                </div>
              </div>
              <MicroCommitment theme={theme}>
                <p>Pick one subject you have a test for in the next two weeks. Open your calendar and schedule two short review sessions for it between now and then, following the "Ridgeline Rule".</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default MasteringSpacedRepetitionModule;
