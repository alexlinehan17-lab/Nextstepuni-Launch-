
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  Link2, Brain, Wand2, Gamepad2, Briefcase, DraftingCompass, Wind, GraduationCap
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { roseTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment, PersonalStory } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';
import { useModuleResponses } from '../hooks/useModuleResponses';
import { useNorthStar } from '../hooks/useNorthStar';
import NorthStarCallout from './NorthStarCallout';
import { COMPACT_CALLOUT_PLACEMENTS } from '../northStarData';

const theme = roseTheme;

// --- INTERACTIVE COMPONENTS ---

const WhyBotherAudit = ({ savedSubjects, savedRatings, onSave }: { savedSubjects?: string[]; savedRatings?: { [key: string]: number }; onSave?: (subjects: string[], ratings: { [key: string]: number }) => void }) => {
    const subjects = [
      'English', 'Irish', 'Maths', 'History', 'Geography', 'Biology',
      'Chemistry', 'Physics', 'Business', 'Economics', 'French', 'Art',
    ];

    const [selected, setSelected] = useState<Set<string>>(new Set(savedSubjects || []));
    const [ratings, setRatings] = useState<{ [key: string]: number }>(savedRatings || {});

    useEffect(() => {
      if (savedSubjects) setSelected(new Set(savedSubjects));
      if (savedRatings) setRatings(savedRatings);
    }, [savedSubjects, savedRatings]);

    const toggleSubject = (s: string) => {
      setSelected(prev => {
        const next = new Set(prev);
        if (next.has(s)) { next.delete(s); } else if (next.size < 7) { next.add(s); }
        onSave?.(Array.from(next), ratings);
        return next;
      });
    };

    const setRating = (subject: string, value: number) => {
      setRatings(prev => {
        const next = { ...prev, [subject]: value };
        onSave?.(Array.from(selected), next);
        return next;
      });
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
            <p className="text-[10px] font-bold uppercase tracking-wider text-zinc-400 dark:text-zinc-500">Rate each subject — how useful does it feel for your future?</p>
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
                  These are the subjects where "why bother?" hits hardest. They feel pointless right now, which makes the effort feel unbearable. The rest of this module will help you change that.
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
  const { responses, saveResponse, isLoaded } = useModuleResponses('linking-study-future-goals');
  const { northStar } = useNorthStar();

  const sections = [
    { id: 'friction-point', title: 'The "Why Bother?" Problem', eyebrow: '01 // When Motivation Drops', icon: Wind },
    { id: 'horizon-of-purpose', title: 'The Horizon of Purpose', eyebrow: '02 // Seeing Your Future', icon: DraftingCompass },
    { id: 'writing-cure', title: 'The "Writing Cure"', eyebrow: '03 // Making It Personal', icon: Wand2 },
    { id: 'dream-to-plan', title: 'From Dream to Plan', eyebrow: '04 // Getting Real About Goals', icon: Gamepad2 },
    { id: 'becoming-the-author', title: 'Becoming the Author', eyebrow: '05 // Taking Ownership', icon: Brain },
    { id: 'career-training', title: 'Curriculum as Career Training', eyebrow: '06 // Reframing the Work', icon: Briefcase },
    { id: 'structural-levers', title: 'Hacking the System', eyebrow: '07 // Using Every Advantage', icon: GraduationCap },
    { id: 'purpose-protocol', title: 'The Purpose Protocol', eyebrow: '08 // Putting It Together', icon: Link2 },
  ];

  return (
    <ModuleLayout moduleNumber="11" moduleTitle="Linking Study to Goals" moduleSubtitle="Finding Your Why" moduleDescription={`Ever sat down to study and thought "what's the point?" This module helps you figure out why your subjects actually matter to you — and how to stay motivated when the work feels pointless.`} theme={theme} sections={sections} onBack={onBack} progress={progress} onProgressUpdate={onProgressUpdate} finishButtonText="Find Your Why">
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The 'Why Bother?' Problem." eyebrow="Step 1" icon={Wind} theme={theme}>
              {northStar && (() => { const p = COMPACT_CALLOUT_PLACEMENTS.find(p => p.moduleId === 'linking-study-future-goals-protocol'); return p ? <NorthStarCallout northStar={northStar} variant="compact" message={p.message} /> : null; })()}
              <p>The feeling of "why bother?" isn't laziness. It's your brain doing a quick calculation: does the effort of this task feel worth it? This idea is called <Highlight description="Basically, your motivation depends on two things: whether you think you can actually do the task, and whether you think it's worth doing. If either one drops, your motivation tanks." theme={theme}>Expectancy-Value Theory (EVT)</Highlight>. Motivation collapses when the <Highlight description="All the stuff that makes a task feel painful -- the boredom, the stress, the time it takes away from things you'd rather be doing." theme={theme}>Cost</Highlight> feels higher than the <Highlight description="How useful a subject or task feels for what you actually want to do with your life. This is the strongest type of motivation for schoolwork because it doesn't fade as fast as other kinds." theme={theme}>Utility Value</Highlight>.</p>
              <p>In the Leaving Cert, the "points race" often disconnects the work you're doing from any real-world purpose, which makes its Utility Value feel like zero. When that happens, everything feels like pointless drudgery, and the Cost becomes unbearable. This module is about flipping that equation back in your favour.</p>
              <PersonalStory name="Alex" role="Founder, NextStepUni">
                <p>I had the "why bother?" problem worse than most. Growing up in Togher, I couldn't see a single connection between what was happening in a classroom and anything that mattered in my life. School felt like it was designed for other people. It wasn't until I started reading the science of learning for myself that I realised the problem wasn't me — it was that nobody had ever shown me why any of it was worth the effort.</p>
              </PersonalStory>
              <WhyBotherAudit savedSubjects={responses['audit-subjects']} savedRatings={responses['audit-ratings']} onSave={(subjects, ratings) => { saveResponse('audit-subjects', subjects); saveResponse('audit-ratings', ratings); }} />
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="The Horizon of Purpose." eyebrow="Step 2" icon={DraftingCompass} theme={theme}>
              <p>The single biggest factor in beating the "why bother?" feeling is your <Highlight description="How far into the future you think when deciding what to do right now. If you're only thinking about getting to June, everything feels painful. But if you can see how today's work connects to where you want to be in 5 years, the same task starts to feel like an investment." theme={theme}>Future Time Perspective (FTP)</Highlight>. It's basically the mental timeline you use to frame what you're doing right now. A short FTP (just surviving until June) makes every task feel like a painful cost. A long FTP (seeing how this connects to your career in 5 years) reframes the exact same task as something worth doing.</p>
              <p>The key thing is that your FTP needs to be <Highlight description="A vague idea like 'I want a good life' doesn't really motivate you. What works is being specific -- like knowing exactly how learning about cell biology connects to becoming a doctor. The more concrete the link, the stronger the motivation." theme={theme}>specific to what you're studying</Highlight>. It's not enough to want a good job someday. You need to see a direct, concrete link between what you're working on today and the person you want to become.</p>
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="The 'Writing Cure'." eyebrow="Step 3" icon={Wand2} theme={theme}>
              <p>So how do you actually build that connection? One of the most effective exercises is the <Highlight description="A quick writing exercise where you spend a few minutes writing about how what you're studying is actually relevant to your own life. When you put it in your own words, it stops being something a teacher told you and becomes something you actually believe." theme={theme}>Utility Value Intervention</Highlight>. When you write down in your own words why something matters to you, your brain takes it seriously. You go from "the teacher says this is important" to "I can actually see how this helps me."</p>
              <p>There's another writing trick that works like a mental shield: <Highlight description="Spending a few minutes writing about what matters most to you -- like family, creativity, or independence. It sounds simple, but it takes the pressure off by reminding you that you're more than just your grades." theme={theme}>Self-Affirmation Journaling</Highlight>. By spending a few minutes writing about what matters most to you -- family, creativity, helping others -- you build a defence against <Highlight description="That nagging feeling of 'people like me don't do well here.' It's the worry that you'll confirm some negative stereotype about where you're from or who you are, and it can quietly drain your performance without you even realising." theme={theme}>Stereotype Threat</Highlight>, that nagging voice that says "people like me don't succeed here." This simple exercise helps close achievement gaps by reminding you that who you are is so much bigger than any single exam or grade.</p>
              <MicroCommitment theme={theme}>
                <p>Pick one subject you're studying this week. Now, think of one specific way it could be useful to (a) you in the future, (b) a family member, or (c) solving a problem you care about. That's it -- you've just done the exercise. Seriously, it's that simple.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="From Dream to Plan." eyebrow="Step 4" icon={Gamepad2} theme={theme}>
              <p>Just having a goal isn't enough. In fact, pure positive daydreaming can actually <strong>lower</strong> your energy because it tricks your brain into feeling like you've already achieved it. The fix is <Highlight description="Instead of just daydreaming about your ideal future, you also think honestly about the real obstacles in your way. This combo -- dream plus obstacle -- lights a fire under you because your brain goes 'oh wait, I actually need to do something about this.'" theme={theme}>Mental Contrasting</Highlight> -- deliberately pairing your dream with the internal barriers that could derail it.</p>
              <p>Here's why it works: when you think about the obstacle <strong>before</strong> it happens, your brain pre-loads a solution. "If I get distracted by my phone, then I will put it in the kitchen." This turns barriers from motivation-killers into automatic triggers for action. The obstacle becomes the cue, not the excuse.</p>
              <MicroCommitment theme={theme}>
                <p>Think of your biggest study goal this week. Now name the single biggest internal obstacle (not "time" — something inside you, like "I'll get bored" or "I'll feel overwhelmed"). Finally, write one "If [obstacle], then I will [action]" sentence. You've just turned your barrier into a plan.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="Becoming the Author." eyebrow="Step 5" icon={Brain} theme={theme}>
                <p>Feeling a lack of purpose often comes from a lack of control. <Highlight description="The idea is simple: people have three core needs to feel motivated -- feeling in control (Autonomy), feeling capable (Competence), and feeling connected to others (Relatedness). When these are met, motivation comes naturally." theme={theme}>Self-Determination Theory</Highlight> tells us we're most motivated when we feel we have <Highlight description="The feeling of being in the driver's seat. It's about doing things because you chose to, not because someone forced you." theme={theme}>Autonomy</Highlight>. The Leaving Cert can feel like it strips that away completely.</p>
                <p>You can take back control through <Highlight description="Tweaking how you approach your schoolwork so it lines up with what you're actually interested in. You're not changing the assignment -- you're changing your angle on it." theme={theme}>Course Crafting</Highlight>. This isn't about changing the assignment, but about changing your <em>approach</em> to it. If you have to write a History essay but you love art, write about the history of art. That small act of choice transforms the motivation from "I have to do this" to "I want to do this."</p>
                <p>There's something even deeper going on here. <Highlight description="Your sense of who you are shapes how you react to hard tasks. When something feels 'like you,' difficulty feels worthwhile. When it feels totally alien, the same difficulty makes you want to give up because your brain goes 'this isn't for someone like me.'" theme={theme}>Identity-Based Motivation</Highlight> explains how your sense of self determines whether struggle feels validating or crushing. When a task feels like it fits who you are -- "I'm the kind of person who does this" -- difficulty feels like a signal of <strong>importance</strong>. ("This is hard, so it must be worth it.") But when a task feels alien, the same difficulty triggers what's called the <Highlight description="When something feels hard and it also doesn't feel 'like you,' your brain takes a shortcut and decides it must be impossible -- rather than just difficult. It's your brain being lazy, not you being incapable." theme={theme}>"Impossibility Shortcut"</Highlight>. ("This is hard, so it's not for people like me.")</p>
                <p>This is why Course Crafting matters so much: it shifts how you see yourself in relation to the work. When you shape your own approach, the task starts to feel "like you," and the struggle that once felt like a wall becomes proof that you're on a path worth walking.</p>
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="Curriculum as Career Training." eyebrow="Step 6" icon={Briefcase} theme={theme}>
              <p>The biggest lie of the "points race" is that subjects are just abstract hurdles you need to jump over. The truth is that every subject on the curriculum is training you in skills that employers and colleges actually value. To beat the "why bother?" feeling, you need to start seeing the curriculum as direct career training.</p>
              <p>Maths isn't just Maths -- it's training you in risk assessment and decision-making. English isn't just reading books -- it's building your ability to understand people and communicate clearly. The History RSR isn't just an essay -- it's practice in pulling together information and making a case, which is exactly what lawyers and journalists do every day. Once you see this connection, the "drudgery" starts to look a lot more like building a portfolio of real-world skills.</p>
              <TransferableSkillsMatrix />
            </ReadingSection>
          )}
          {activeSection === 6 && (
            <ReadingSection title="Hacking the System." eyebrow="Step 7" icon={GraduationCap} theme={theme}>
              <p>The Irish education system has real barriers -- the "grinds" industry, hidden costs, and the fact that some families just know more about how the system works than others. But there are also powerful tools designed specifically to level the playing field. Knowing about these isn't optional -- it's a critical part of your strategy. These are not handouts. They are tools, and knowing how to use them is a skill in itself.</p>
              <p>The <Highlight description="A scheme that gives you reduced CAO points for college entry if you come from a disadvantaged background. They look at things like family income, whether your school is DEIS, and your parents' education. It can knock 30-50 points off the score you need -- that's huge." theme={theme}>HEAR (Higher Education Access Route)</Highlight> scheme offers reduced CAO points for college entry to students from disadvantaged backgrounds. They look at things like family income, whether your school is DEIS, and parental education levels. If you qualify, this can mean 30-50 fewer points on your required score -- that's a game-changer. Applications open in the autumn of 6th year through the CAO, and missing the deadline means missing the opportunity entirely.</p>
              <p>The <Highlight description="A scheme for students whose education has been affected by a disability -- whether that's physical, sensory, learning (like dyslexia or ADHD), or mental health related. You get reduced points AND extra supports in college like assistive tech and exam accommodations." theme={theme}>DARE (Disability Access Route to Education)</Highlight> scheme is for students whose education has been affected by a disability -- whether physical, sensory, learning (like dyslexia or ADHD), or psychological. DARE doesn't just offer reduced points; it also connects you with in-college supports like assistive technology, exam accommodations, and dedicated advisors.</p>
              <p>Finally, the <Highlight description="The main money support for going to college in Ireland. It covers your fees and gives you a grant for living costs. Big tip: if you live more than 30km from your college, you get a higher rate -- and that distance is measured to your actual course building, not just the main campus." theme={theme}>SUSI (Student Universal Support Ireland)</Highlight> grant is the main financial support for college. It covers tuition fees and gives you a maintenance grant for living costs. Here's a key detail: the maintenance grant has distance tiers. If you live more than 30km from your college, you qualify for the higher "non-adjacent" rate, which can mean thousands of euro in extra support. Check the distance from your home to your course -- not the college campus generally, but the specific building where your course is based.</p>
              <MicroCommitment theme={theme}>
                <p>Do a quick audit right now. (1) Does your family income fall under the HEAR thresholds? Is your school a DEIS school? (2) Do you have a diagnosed disability that has impacted your education? (3) How far is your home from your target college? If any answer is "yes" or "over 30km," you have a structural lever to pull. Write down which schemes to research this week.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
          {activeSection === 7 && (
            <ReadingSection title="The Purpose Protocol." eyebrow="Step 8" icon={Link2} theme={theme}>
              <p>You now have the tools to rebuild the connection between what you're doing today and where you want to be. This is the <strong>Purpose Protocol</strong> -- a 5-phase plan for building motivation that actually lasts.</p>
              <p><strong>Phase 1: The Audit.</strong> For each subject, ask "Why am I doing this?" If the only answer is "points," that's a friction point. Do the Utility Value Writing exercise on it. <strong>Phase 2: The Vision.</strong> Spend 15 minutes writing a detailed picture of your "Best Possible Self" 5 years from now. Then pair that vision with your biggest real obstacle. <strong>Phase 3: The Craft.</strong> Find one assignment this week and "course craft" it -- put your own spin on it so it feels like yours. <strong>Phase 4: The Habit.</strong> Make starting so small it's impossible to fail. One page. One question. Just begin. <strong>Phase 5: Re-Authoring.</strong> If you feel stuck, step back from the problem ("The stress is visiting me, it's not who I am") and think about skills you use in other areas of your life -- gaming, sports, whatever -- and how they apply to your schoolwork.</p>
              <MicroCommitment theme={theme}>
                <p>Pick one phase. Just one. Commit to trying it for one week. You're not just studying -- you're building something that matters to you.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default LinkingStudyFutureGoalsModule;
