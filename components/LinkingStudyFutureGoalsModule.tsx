
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Link2, Brain, Wand2, Gamepad2, Briefcase, DraftingCompass, Wind
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { roseTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = roseTheme;

// --- INTERACTIVE COMPONENTS ---

const MotivationCalculator = () => {
    const [vars, setVars] = useState({ E: 50, V: 50, C: 50 });
    const motivation = (vars.E * vars.V) / (vars.C + 1);

    const Slider = ({ label, value, setter }: { label: string, value: number, setter: (val: number) => void}) => (
        <div>
            <label className="text-xs font-bold">{label} ({value})</label>
            <input type="range" min="1" max="100" value={value} onChange={e => setter(parseInt(e.target.value))} className="w-full accent-rose-500" />
        </div>
    );

    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Motivation Calculator</h4>
            <div className="grid grid-cols-2 gap-6 items-center">
                <div className="space-y-4">
                    <Slider label="Expectancy (Belief I can do it)" value={vars.E} setter={v => setVars({...vars, E:v})}/>
                    <Slider label="Value (How useful/enjoyable is it?)" value={vars.V} setter={v => setVars({...vars, V:v})}/>
                    <Slider label="Cost (Stress, boredom, time)" value={vars.C} setter={v => setVars({...vars, C:v})}/>
                </div>
                <div className="text-center">
                     <p className="text-sm text-zinc-500 dark:text-zinc-400">Your Motivation Score:</p>
                     <p className="text-6xl font-semibold text-rose-500 tracking-tighter">{Math.round(motivation)}</p>
                </div>
            </div>
        </div>
    )
};

const WOOPPlanner = () => {
    const [data, setData] = useState({wish: '', outcome: '', obstacle: '', plan: ''});
    const update = (field: string, value: string) => setData(prev => ({...prev, [field]: value}));

    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">My WOOP Blueprint</h4>
            <div className="space-y-4 mt-6">
                <input value={data.wish} onChange={e => update('wish', e.target.value)} placeholder="WISH: What do you want to achieve?" className="w-full p-3 bg-zinc-50 dark:bg-zinc-800/50 rounded-lg"/>
                <input value={data.outcome} onChange={e => update('outcome', e.target.value)} placeholder="OUTCOME: What's the best feeling if you do?" className="w-full p-3 bg-zinc-50 dark:bg-zinc-800/50 rounded-lg"/>
                <input value={data.obstacle} onChange={e => update('obstacle', e.target.value)} placeholder="OBSTACLE: What *inside you* holds you back?" className="w-full p-3 bg-zinc-50 dark:bg-zinc-800/50 rounded-lg"/>
                <input value={data.plan} onChange={e => update('plan', e.target.value)} placeholder="PLAN: If [obstacle], then I will..." className="w-full p-3 bg-zinc-50 dark:bg-zinc-800/50 rounded-lg"/>
            </div>
        </div>
    );
};

const TransferableSkillsMatrix = () => {
    const [activeRow, setActiveRow] = useState<string | null>(null);
    const skills = [
        { activity: "History RSR", skill: "Information Synthesis", application: "Legal Research, Journalism" },
        { activity: "English Comparative", skill: "Pattern Recognition", application: "UX Design, HR Management" },
        { activity: "Maths Probability", skill: "Risk Assessment", application: "Insurance, Business Strategy" },
        { activity: "Geography Field Study", skill: "Systems Thinking", application: "Urban Planning, Logistics" },
        { activity: "LCVP/Business", skill: "Project Management", application: "Event Management, Operations" },
    ];

    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Transferable Skills Matrix</h4>
            <div className="mt-6 flow-root">
                <div className="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
                    <div className="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
                        <table className="min-w-full divide-y divide-zinc-200">
                            <thead>
                                <tr>
                                    <th className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-zinc-900">LC Activity</th>
                                    <th className="px-3 py-3.5 text-left text-sm font-semibold text-zinc-900">Corporate/Life Skill</th>
                                    <th className="px-3 py-3.5 text-left text-sm font-semibold text-zinc-900">Career Application</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-zinc-100">
                                {skills.map(item => (
                                    <tr key={item.activity} onMouseEnter={() => setActiveRow(item.activity)} onMouseLeave={() => setActiveRow(null)} className="hover:bg-rose-50 cursor-pointer">
                                        <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium">{item.activity}</td>
                                        <td className="whitespace-nowrap px-3 py-4 text-sm font-medium">{item.skill}</td>
                                        <td className="whitespace-nowrap px-3 py-4 text-sm font-medium">{item.application}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    );
};


// --- MODULE COMPONENT ---
const LinkingStudyFutureGoalsModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'friction-point', title: 'The "Why Bother?" Problem', eyebrow: '01 // The Anatomy of Friction', icon: Wind },
    { id: 'horizon-of-purpose', title: 'The Horizon of Purpose', eyebrow: '02 // Future Time Perspective', icon: DraftingCompass },
    { id: 'writing-cure', title: 'The "Writing Cure"', eyebrow: '03 // Utility Value Interventions', icon: Wand2 },
    { id: 'woop-protocol', title: 'From Dream to Plan', eyebrow: '04 // The WOOP Protocol', icon: Gamepad2 },
    { id: 'becoming-the-author', title: 'Becoming the Author', eyebrow: '05 // Narrative & Autonomy', icon: Brain },
    { id: 'career-training', title: 'Curriculum as Career Training', eyebrow: '06 // Reframing the Work', icon: Briefcase },
    { id: 'purpose-protocol', title: 'The Purpose Protocol', eyebrow: '07 // The Action Plan', icon: Link2 },
  ];

  return (
    <ModuleLayout moduleNumber="11" moduleTitle="Linking Study to Goals" theme={theme} sections={sections} onBack={onBack} progress={progress} onProgressUpdate={onProgressUpdate}>
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The 'Why Bother?' Problem." eyebrow="Step 1" icon={Wind} theme={theme}>
              <p>The feeling of "why bother?" isn't laziness. It's a rational calculation your brain makes when the cost of a task outweighs its value. The science for this is called <Highlight description="A theory of motivation that posits that your level of motivation is a product of your expectation of success (Expectancy) and the value you place on the task (Value)." theme={theme}>Expectancy-Value Theory (EVT)</Highlight>. Motivation collapses when the <Highlight description="The perceived negative aspects of a task, like stress, boredom, or the time it takes away from other activities." theme={theme}>Cost</Highlight> feels higher than the <Highlight description="The usefulness of a task for achieving your future goals. It's the most stable and powerful form of motivation for schoolwork." theme={theme}>Utility Value</Highlight>.</p>
              <p>In the Leaving Cert, the "points race" often disconnects the work you're doing from any real-world purpose, reducing its Utility Value to zero. This makes the work feel like "drudgery," which massively increases its psychological Cost. This module is about flipping that equation back in your favour.</p>
              <MotivationCalculator />
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="The Horizon of Purpose." eyebrow="Step 2" icon={DraftingCompass} theme={theme}>
              <p>The single biggest factor in overcoming the "why bother?" friction is your <Highlight description="A cognitive construct that describes the extent to which you anticipate and integrate the future into your present actions. A long, deep FTP is a powerful buffer against burnout." theme={theme}>Future Time Perspective (FTP)</Highlight>. It's the mental timeline you use to frame your current actions. A short FTP (just getting to June) makes every task feel like a painful cost. A long FTP (seeing how this connects to your career in 5 years) reframes the same task as a valuable investment.</p>
              <p>Crucially, your FTP needs to be <Highlight description="The motivational power of FTP is strongest when it's specific. A general desire for a 'good life' is weak compared to knowing exactly how the Krebs cycle is relevant to becoming a doctor." theme={theme}>domain-specific</Highlight>. It's not enough to want a good job; you need to see the direct, concrete link between the paragraph you're writing today and the person you want to become tomorrow.</p>
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="The 'Writing Cure'." eyebrow="Step 3" icon={Wand2} theme={theme}>
              <p>How do you forge that link? One of the most robust interventions in psychology is the <Highlight description="A simple, evidence-based exercise where students write briefly about how their schoolwork is relevant to their own lives. It is proven to boost interest and grades, especially for struggling students." theme={theme}>Utility Value Intervention</Highlight>. The act of articulating the connection yourself forces your brain to "internalize" the value. You move from "the teacher says this is important" to "I see how this helps me."</p>
              <MicroCommitment theme={theme}>
                <p>Pick one subject you're studying this week. Now, think of one specific way it could be useful to (a) you in the future, (b) a family member, or (c) solving a problem you care about. You've just run your first Utility Value Intervention.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="From Dream to Plan." eyebrow="Step 4" icon={Gamepad2} theme={theme}>
              <p>Just having a goal isn't enough. Research shows that pure positive fantasizing can actually lower your energy. To turn a dream into a plan, you need a tool called <Highlight description="A powerful, four-step goal-setting strategy developed by Gabriele Oettingen, based on the science of Mental Contrasting with Implementation Intentions." theme={theme}>WOOP</Highlight>: Wish, Outcome, Obstacle, Plan.</p>
              <p>The magic is in the <strong>Obstacle</strong> step. By vividly imagining the internal barrier that stops you (e.g., "I get distracted by my phone"), you can create an "If-Then" plan to deal with it automatically. This transforms the obstacle from a motivation-killer into a trigger for a pre-planned, positive response.</p>
              <WOOPPlanner />
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="Becoming the Author." eyebrow="Step 5" icon={Brain} theme={theme}>
                <p>Feeling a lack of purpose often comes from a lack of control. <Highlight description="A psychological theory that states we have three core needs: Autonomy (control), Competence (capability), and Relatedness (connection)." theme={theme}>Self-Determination Theory (SDT)</Highlight> shows that we are most motivated when we feel we have <Highlight description="The feeling of being in control of your own actions and life. It's about acting from a sense of choice, not coercion." theme={theme}>Autonomy</Highlight>. The Leaving Cert can feel like it strips this away.</p>
                <p>You can reclaim your autonomy through <Highlight description="A technique where you slightly modify how you approach your schoolwork to better align it with your personal strengths and interests." theme={theme}>Course Crafting</Highlight>. This isn't about changing the assignment, but about changing your *approach* to it. If you have to write a History essay but you love art, write about the history of art. This act of choice transforms the motivation from "controlled" (have to) to "autonomous" (want to).</p>
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="Curriculum as Career Training." eyebrow="Step 6" icon={Briefcase} theme={theme}>
              <p>The biggest lie of the "points race" is that subjects are just abstract hurdles. The truth is that every subject on the curriculum is a training ground for high-demand, 21st-century skills. To beat the "why bother?" friction, you must reframe the curriculum as direct career training.</p>
              <p>Maths isn't just Maths; it's the science of risk assessment and decision-making. English isn't just reading books; it's a laboratory for social intelligence and empathy. The History RSR isn't just an essay; it's training in information synthesis and due diligence—the core skills of a lawyer or a journalist. By making this matrix visible, the "drudgery" of schoolwork is reframed as building a portfolio of real-world skills.</p>
              <TransferableSkillsMatrix />
            </ReadingSection>
          )}
          {activeSection === 6 && (
            <ReadingSection title="The Purpose Protocol." eyebrow="Step 7" icon={Link2} theme={theme}>
              <p>You now have the scientific toolkit to re-wire the connection between your present effort and your future self. This is the <strong>Purpose Protocol</strong>, a 5-phase plan for building sustainable motivation.</p>
              <p><strong>Phase 1: The Audit.</strong> For each subject, ask "Why am I doing this?" If the only answer is "points," that's a friction point. Apply the Utility Value Writing exercise. <strong>Phase 2: The Vision.</strong> Spend 15 minutes writing a detailed description of your "Best Possible Self" 5 years from now. Then, use WOOP to plan your next study session. <strong>Phase 3: The Craft.</strong> Find one assignment this week and "course craft" it to make it your own. <strong>Phase 4: The Habit.</strong> Use "Tiny Habits" to make starting the work so small it's impossible to fail. <strong>Phase 5: Re-Authoring.</strong> If you feel stuck, externalize the problem ("The stress is visiting me") and map your skills from other areas (like gaming) to your schoolwork.</p>
              <MicroCommitment theme={theme}>
                <p>Pick one phase, one protocol. Just one. Commit to trying it for one week. You're not just studying; you're becoming the architect of your own purpose.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default LinkingStudyFutureGoalsModule;
