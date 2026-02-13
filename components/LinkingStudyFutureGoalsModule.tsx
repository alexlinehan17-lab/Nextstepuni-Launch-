
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import {
  Link2, Brain, Wand2, Gamepad2, Briefcase, DraftingCompass, Wind, GraduationCap
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { roseTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment, PersonalStory } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = roseTheme;

// --- INTERACTIVE COMPONENTS ---

const WhyBotherAudit = () => {
    const subjects = [
      'English', 'Irish', 'Maths', 'History', 'Geography', 'Biology',
      'Chemistry', 'Physics', 'Business', 'Economics', 'French', 'Art',
    ];

    const [selected, setSelected] = useState<Set<string>>(new Set());
    const [ratings, setRatings] = useState<{ [key: string]: number }>({});

    const toggleSubject = (s: string) => {
      setSelected(prev => {
        const next = new Set(prev);
        if (next.has(s)) { next.delete(s); } else if (next.size < 7) { next.add(s); }
        return next;
      });
    };

    const setRating = (subject: string, value: number) => {
      setRatings(prev => ({ ...prev, [subject]: value }));
    };

    const ratedSubjects = Array.from(selected).filter(s => ratings[s] !== undefined);
    const frictionPoints = ratedSubjects.filter(s => (ratings[s] ?? 0) <= 2);
    const allRated = ratedSubjects.length === selected.size && selected.size > 0;

    const ratingLabels = [
      { value: 1, label: 'None', desc: 'No connection to my future', color: 'bg-rose-500 text-white' },
      { value: 2, label: 'Weak', desc: 'Vague connection at best', color: 'bg-amber-500 text-white' },
      { value: 3, label: 'Some', desc: 'I can see a partial link', color: 'bg-yellow-400 text-zinc-800' },
      { value: 4, label: 'Strong', desc: 'Clear link to my goals', color: 'bg-emerald-500 text-white' },
    ];

    return (
      <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
        <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The "Why Bother?" Audit</h4>
        <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Select your subjects, then rate how connected each one feels to your future goals.</p>

        {/* Subject picker */}
        <div className="mb-6">
          <p className="text-[10px] font-bold uppercase tracking-wider text-zinc-400 dark:text-zinc-500 mb-2">Select your subjects (up to 7)</p>
          <div className="flex flex-wrap gap-2">
            {subjects.map(s => (
              <button
                key={s}
                onClick={() => toggleSubject(s)}
                className={`px-3 py-1.5 text-xs font-bold rounded-lg border transition-all ${
                  selected.has(s)
                    ? 'bg-rose-500 text-white border-rose-500'
                    : 'bg-zinc-50 dark:bg-zinc-900/30 text-zinc-600 dark:text-zinc-300 border-zinc-200 dark:border-zinc-700 hover:border-rose-300'
                }`}
              >
                {s}
              </button>
            ))}
          </div>
        </div>

        {/* Rating cards */}
        {selected.size > 0 && (
          <div className="space-y-3 mb-6">
            <p className="text-[10px] font-bold uppercase tracking-wider text-zinc-400 dark:text-zinc-500">Rate utility value — how useful does this feel for your future?</p>
            {Array.from(selected).map(s => (
              <div
                key={s}
                className={`p-4 rounded-xl border transition-all ${
                  ratings[s] !== undefined
                    ? ratings[s] <= 2
                      ? 'bg-rose-50 dark:bg-rose-950/20 border-rose-200 dark:border-rose-800/40'
                      : 'bg-emerald-50 dark:bg-emerald-950/20 border-emerald-200 dark:border-emerald-800/40'
                    : 'bg-zinc-50 dark:bg-zinc-900/30 border-zinc-200 dark:border-zinc-700'
                }`}
              >
                <div className="flex items-center justify-between mb-2.5">
                  <p className="text-sm font-bold text-zinc-800 dark:text-white">{s}</p>
                  {ratings[s] !== undefined && (
                    <motion.span
                      initial={{ opacity: 0, scale: 0.8 }}
                      animate={{ opacity: 1, scale: 1 }}
                      className={`text-[10px] font-bold ${ratings[s] <= 2 ? 'text-rose-500' : 'text-emerald-500'}`}
                    >
                      {ratings[s] <= 2 ? 'Friction Point' : 'Connected'}
                    </motion.span>
                  )}
                </div>
                <div className="flex gap-2">
                  {ratingLabels.map(r => (
                    <button
                      key={r.value}
                      onClick={() => setRating(s, r.value)}
                      className={`flex-1 py-1.5 text-[10px] font-bold rounded-lg border transition-all ${
                        ratings[s] === r.value
                          ? `${r.color} border-transparent`
                          : 'bg-white dark:bg-zinc-800 text-zinc-500 dark:text-zinc-400 border-zinc-200 dark:border-zinc-700 hover:border-zinc-400'
                      }`}
                    >
                      {r.label}
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Results */}
        {allRated && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="p-5 bg-zinc-50 dark:bg-zinc-900/30 rounded-xl border border-zinc-200 dark:border-zinc-700"
          >
            {frictionPoints.length > 0 ? (
              <>
                <p className="text-sm font-semibold text-zinc-800 dark:text-white mb-1">
                  You have {frictionPoints.length} friction point{frictionPoints.length > 1 ? 's' : ''}: {frictionPoints.join(', ')}
                </p>
                <p className="text-xs text-zinc-500 dark:text-zinc-400">
                  These are the subjects where "why bother?" is loudest. Their Utility Value feels low, which makes the Cost feel unbearable. The rest of this module will teach you how to reframe them.
                </p>
              </>
            ) : (
              <>
                <p className="text-sm font-semibold text-emerald-600 dark:text-emerald-400 mb-1">No friction points detected.</p>
                <p className="text-xs text-zinc-500 dark:text-zinc-400">You already see strong connections between your subjects and your future. This module will help you strengthen and articulate those connections even further.</p>
              </>
            )}
          </motion.div>
        )}
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
    { id: 'dream-to-plan', title: 'From Dream to Plan', eyebrow: '04 // Mental Contrasting', icon: Gamepad2 },
    { id: 'becoming-the-author', title: 'Becoming the Author', eyebrow: '05 // Narrative & Autonomy', icon: Brain },
    { id: 'career-training', title: 'Curriculum as Career Training', eyebrow: '06 // Reframing the Work', icon: Briefcase },
    { id: 'structural-levers', title: 'Hacking the System', eyebrow: '07 // The Structural Levers', icon: GraduationCap },
    { id: 'purpose-protocol', title: 'The Purpose Protocol', eyebrow: '08 // The Protocol', icon: Link2 },
  ];

  return (
    <ModuleLayout moduleNumber="11" moduleTitle="Linking Study to Goals" moduleSubtitle="The Architecture of Purpose" moduleDescription={`Deconstruct the "why bother?" problem and learn the science of linking today's effort to tomorrow's success. This is the antidote to burnout.`} theme={theme} sections={sections} onBack={onBack} progress={progress} onProgressUpdate={onProgressUpdate}>
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The 'Why Bother?' Problem." eyebrow="Step 1" icon={Wind} theme={theme}>
              <p>The feeling of "why bother?" isn't laziness. It's a rational calculation your brain makes when the cost of a task outweighs its value. The science for this is called <Highlight description="A theory of motivation that posits that your level of motivation is a product of your expectation of success (Expectancy) and the value you place on the task (Value)." theme={theme}>Expectancy-Value Theory (EVT)</Highlight>. Motivation collapses when the <Highlight description="The perceived negative aspects of a task, like stress, boredom, or the time it takes away from other activities." theme={theme}>Cost</Highlight> feels higher than the <Highlight description="The usefulness of a task for achieving your future goals. It's the most stable and powerful form of motivation for schoolwork." theme={theme}>Utility Value</Highlight>.</p>
              <p>In the Leaving Cert, the "points race" often disconnects the work you're doing from any real-world purpose, reducing its Utility Value to zero. This makes the work feel like "drudgery," which massively increases its psychological Cost. This module is about flipping that equation back in your favour.</p>
              <PersonalStory name="Alex" role="Founder, NextStepUni">
                <p>I had the "why bother?" problem worse than most. Growing up in Togher, I couldn't see a single connection between what was happening in a classroom and anything that mattered in my life. School felt like it was designed for other people. It wasn't until I started reading the science of learning for myself that I realised the problem wasn't me — it was that nobody had ever shown me why any of it was worth the effort.</p>
              </PersonalStory>
              <WhyBotherAudit />
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
              <p>There's a complementary writing technique that works as a psychological shield: <Highlight description="A brief writing exercise about your core personal values (e.g., family, creativity, independence). It has been proven to buffer the brain against stress and raise grades, particularly in students from low-SES backgrounds." theme={theme}>Self-Affirmation Journaling</Highlight>. By spending a few minutes writing about your deepest personal values--family, creativity, helping others--you create a buffer against <Highlight description="The anxiety that arises from the fear of confirming a negative stereotype about your social group, which can suppress academic performance." theme={theme}>Stereotype Threat</Highlight>, the fear that "people like me don't succeed here." Research shows this simple exercise narrows achievement gaps by reminding students that their identity is larger than any single exam or grade.</p>
              <MicroCommitment theme={theme}>
                <p>Pick one subject you're studying this week. Now, think of one specific way it could be useful to (a) you in the future, (b) a family member, or (c) solving a problem you care about. You've just run your first Utility Value Intervention.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="From Dream to Plan." eyebrow="Step 4" icon={Gamepad2} theme={theme}>
              <p>Just having a goal isn't enough. Research shows that pure positive fantasizing can actually <strong>lower</strong> your energy. The antidote is <Highlight description="A cognitive strategy where you vividly imagine your desired future, then immediately contrast it with the reality of the obstacles standing in your way. This creates a 'necessity to act' signal in the brain." theme={theme}>Mental Contrasting</Highlight>--deliberately pairing your dream with the internal barriers that could derail it.</p>
              <p>The key insight: when you confront the obstacle <strong>before</strong> it happens, your brain pre-loads a solution. "If I get distracted by my phone, then I will put it in the kitchen." This transforms barriers from motivation-killers into triggers for pre-planned responses. The obstacle becomes the cue, not the excuse.</p>
              <MicroCommitment theme={theme}>
                <p>Think of your biggest study goal this week. Now name the single biggest internal obstacle (not "time" — something inside you, like "I'll get bored" or "I'll feel overwhelmed"). Finally, write one "If [obstacle], then I will [action]" sentence. You've just turned your barrier into a plan.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="Becoming the Author." eyebrow="Step 5" icon={Brain} theme={theme}>
                <p>Feeling a lack of purpose often comes from a lack of control. <Highlight description="A psychological theory that states we have three core needs: Autonomy (control), Competence (capability), and Relatedness (connection)." theme={theme}>Self-Determination Theory (SDT)</Highlight> shows that we are most motivated when we feel we have <Highlight description="The feeling of being in control of your own actions and life. It's about acting from a sense of choice, not coercion." theme={theme}>Autonomy</Highlight>. The Leaving Cert can feel like it strips this away.</p>
                <p>You can reclaim your autonomy through <Highlight description="A technique where you slightly modify how you approach your schoolwork to better align it with your personal strengths and interests." theme={theme}>Course Crafting</Highlight>. This isn't about changing the assignment, but about changing your *approach* to it. If you have to write a History essay but you love art, write about the history of art. This act of choice transforms the motivation from "controlled" (have to) to "autonomous" (want to).</p>
                <p>There's also a deeper identity mechanism at play. <Highlight description="A theory stating that we are motivated to act in ways that are congruent with our identities. When a task feels 'like me,' difficulty is interpreted as importance; when it feels alien, difficulty signals impossibility." theme={theme}>Identity-Based Motivation (IBM)</Highlight> theory explains how your sense of self determines whether struggle feels validating or crushing. When a task feels congruent with your identity--"I'm the kind of person who does this"--difficulty is read as a signal of <strong>importance</strong>. ("This is hard, so it must be worth it.") But when a task feels alien, the same difficulty triggers the <Highlight description="A mental shortcut where the brain interprets difficulty on an identity-incongruent task as proof that it's impossible, rather than proof that it matters." theme={theme}>"Impossibility Heuristic"</Highlight>. ("This is hard, so it's not for people like me.")</p>
                <p>This is why Course Crafting and narrative autonomy matter so much: they shift the identity frame. When you author your own approach, the task starts to feel "like you," and the very struggle that once felt like a wall becomes evidence that you're on a path worth walking.</p>
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
            <ReadingSection title="Hacking the System." eyebrow="Step 7" icon={GraduationCap} theme={theme}>
              <p>The Irish education system has real structural barriers--the "grinds" industry, hidden costs, information asymmetry. But it also has powerful structural levers designed specifically to level the playing field. Understanding these is not optional; it's a critical part of your strategy. These are not handouts. They are tools, and knowing how to use them is a skill in itself.</p>
              <p>The <Highlight description="Higher Education Access Route: A scheme that offers reduced-points places at third level to students from socio-economically disadvantaged backgrounds. Eligibility is based on indicators like family income, school DEIS status, and parental education." theme={theme}>HEAR (Higher Education Access Route)</Highlight> scheme offers reduced CAO points for college entry to students from socio-economically disadvantaged backgrounds. Eligibility is assessed on indicators like family income, whether your school is DEIS, and parental education levels. If you qualify, this can mean the difference of 30-50 points on your required score--a game-changer. Applications open in the autumn of 6th year through the CAO, and missing the deadline means missing the opportunity entirely.</p>
              <p>The <Highlight description="Disability Access Route to Education: A scheme that supports students whose education has been significantly impacted by a disability. It provides both reduced points and additional college supports." theme={theme}>DARE (Disability Access Route to Education)</Highlight> scheme is the parallel route for students whose education has been impacted by a disability--whether physical, sensory, learning (like dyslexia or ADHD), or psychological. DARE doesn't just offer reduced points; it also connects you with in-college supports like assistive technology, exam accommodations, and dedicated advisors.</p>
              <p>Finally, the <Highlight description="Student Universal Support Ireland: The main financial support scheme for third-level education in Ireland. It covers fees and provides maintenance grants based on household income and distance from college." theme={theme}>SUSI (Student Universal Support Ireland)</Highlight> grant is the primary financial lifeline. It covers tuition fees and provides a maintenance grant for living costs. Crucially, the maintenance grant has distance tiers: if you live more than 30km from your college, you qualify for the higher "non-adjacent" rate, which can mean thousands of euro in additional support. Check the distance from your home to your course--not the college campus generally, but the specific building where your course is based.</p>
              <MicroCommitment theme={theme}>
                <p>Do a quick audit right now. (1) Does your family income fall under the HEAR thresholds? Is your school a DEIS school? (2) Do you have a diagnosed disability that has impacted your education? (3) How far is your home from your target college? If any answer is "yes" or "over 30km," you have a structural lever to pull. Write down which schemes to research this week.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
          {activeSection === 7 && (
            <ReadingSection title="The Purpose Protocol." eyebrow="Step 8" icon={Link2} theme={theme}>
              <p>You now have the scientific toolkit to re-wire the connection between your present effort and your future self. This is the <strong>Purpose Protocol</strong>, a 5-phase plan for building sustainable motivation.</p>
              <p><strong>Phase 1: The Audit.</strong> For each subject, ask "Why am I doing this?" If the only answer is "points," that's a friction point. Apply the Utility Value Writing exercise. <strong>Phase 2: The Vision.</strong> Spend 15 minutes writing a detailed description of your "Best Possible Self" 5 years from now. Then, use Mental Contrasting to pair your vision with your biggest obstacle. <strong>Phase 3: The Craft.</strong> Find one assignment this week and "course craft" it to make it your own. <strong>Phase 4: The Habit.</strong> Use "Tiny Habits" to make starting the work so small it's impossible to fail. <strong>Phase 5: Re-Authoring.</strong> If you feel stuck, externalize the problem ("The stress is visiting me") and map your skills from other areas (like gaming) to your schoolwork.</p>
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
