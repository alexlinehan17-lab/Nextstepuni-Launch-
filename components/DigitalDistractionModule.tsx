/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import {
  BrainCircuit, Shield, Laptop, Home, Repeat, Users, Map
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { slateTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment, PersonalStory } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = slateTheme;

// --- INTERACTIVE COMPONENTS ---
const AttentionDeficitCalculator = () => {
    const [checks, setChecks] = useState(3);
    const recoveryMins = 23.25;
    const timeLost = Math.min(60, checks * recoveryMins);
    const deepWorkTime = Math.max(0, 60 - timeLost);
    const deepPct = Math.round((deepWorkTime / 60) * 100);

    return (
        <div className="my-10 p-6 md:p-10 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Attention Deficit Calculator</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">Every phone check triggers a ~23 minute attention recovery. How much of your study hour survives?</p>

            {/* Big number */}
            <div className="text-center mb-6">
                <motion.div
                    key={checks}
                    initial={{ scale: 0.9, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    className="inline-block"
                >
                    <span className={`text-6xl font-bold tabular-nums ${deepPct >= 60 ? 'text-emerald-500' : deepPct >= 30 ? 'text-amber-500' : deepPct > 0 ? 'text-orange-500' : 'text-rose-500'}`}>{deepWorkTime.toFixed(0)}</span>
                    <span className="text-2xl font-bold text-zinc-400 ml-1">/ 60 min</span>
                </motion.div>
                <p className="text-sm font-semibold text-zinc-500 dark:text-zinc-400 mt-1">of actual deep work</p>
            </div>

            {/* Hour bar — simple stacked bar */}
            <div className="w-full h-6 rounded-full bg-zinc-100 dark:bg-zinc-700 overflow-hidden flex mb-2">
                <motion.div
                    className="h-full bg-emerald-500 flex items-center justify-center"
                    animate={{ width: `${deepPct}%` }}
                    transition={{ type: 'spring', stiffness: 120, damping: 20 }}
                >
                    {deepPct > 18 && <span className="text-xs font-bold text-white">{deepPct}%</span>}
                </motion.div>
                <motion.div
                    className="h-full bg-rose-400 flex items-center justify-center"
                    animate={{ width: `${100 - deepPct}%` }}
                    transition={{ type: 'spring', stiffness: 120, damping: 20 }}
                >
                    {(100 - deepPct) > 18 && <span className="text-xs font-bold text-white">{100 - deepPct}%</span>}
                </motion.div>
            </div>
            <div className="flex justify-between text-xs mb-6">
                <span className="font-semibold text-emerald-600 dark:text-emerald-400">Deep Work</span>
                <span className="font-semibold text-rose-500 dark:text-rose-400">Recovery Time</span>
            </div>

            {/* Phone check selector */}
            <div className="mb-5">
                <p className="text-sm font-bold text-zinc-700 dark:text-zinc-200 mb-2.5">Phone checks per study hour</p>
                <div className="flex gap-1.5">
                    {Array.from({ length: 11 }).map((_, i) => {
                        const isActive = i === checks;
                        const bg = i === 0 ? 'bg-emerald-500' : i <= 2 ? 'bg-amber-500' : 'bg-rose-500';
                        const bgMuted = i === 0 ? 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400' : i <= 2 ? 'bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-400' : 'bg-zinc-100 dark:bg-zinc-700 text-zinc-500 dark:text-zinc-400';
                        return (
                            <button key={i} onClick={() => setChecks(i)}
                                className={`flex-1 py-2 rounded-lg text-sm font-bold transition-all ${isActive ? `${bg} text-white shadow-sm scale-105` : `${bgMuted} hover:opacity-80`}`}>
                                {i}
                            </button>
                        );
                    })}
                </div>
                <div className="flex justify-between text-xs text-zinc-400 mt-1.5">
                    <span>Phone away</span>
                    <span>Constant</span>
                </div>
            </div>

            {/* Insight */}
            <div className={`p-3.5 rounded-xl text-sm text-center ${
                checks === 0 ? 'bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800 text-emerald-700 dark:text-emerald-300' :
                checks <= 2 ? 'bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 text-amber-700 dark:text-amber-300' :
                'bg-rose-50 dark:bg-rose-900/20 border border-rose-200 dark:border-rose-800 text-rose-700 dark:text-rose-300'
            }`}>
                {checks === 0 && <span className="font-semibold">Phone away = full hour of deep work. This is the goal.</span>}
                {checks === 1 && <span>Even <strong>one check</strong> costs 23 minutes of recovery. You lose over a third of your hour.</span>}
                {checks === 2 && <span><strong>Two checks</strong> and you&apos;ve lost 46 minutes. Only 14 minutes of real studying.</span>}
                {checks === 3 && <span>At <strong>3 checks</strong>, you&apos;re losing over an hour of focus time. Your brain never reaches deep processing.</span>}
                {checks >= 4 && checks <= 6 && <span>At <strong>{checks} checks per hour</strong>, virtually none of your study time is productive. You&apos;re just sitting with a book open.</span>}
                {checks > 6 && <span><strong>{checks} checks per hour</strong> means you&apos;re checking your phone every {(60 / checks).toFixed(0)} minutes. This isn&apos;t studying — it&apos;s scrolling with extra steps.</span>}
            </div>
        </div>
    );
};

// --- PHASED DETOX ROADMAP ---
const PHASES = [
  {
    number: 1,
    title: 'Foundation',
    range: 'Sept — Dec',
    color: 'blue',
    items: [
      'Turn off all non-essential notifications',
      'Set up a phone charging station outside bedroom',
      'Install a website blocker (Cold Turkey / Freedom)',
      "Create a 'study mode' shortcut on your phone",
      'Tell one friend about your digital boundaries',
    ],
  },
  {
    number: 2,
    title: 'Fortification',
    range: 'Jan — Mar',
    color: 'amber',
    items: [
      'Switch to greyscale mode during study hours',
      'Delete social media apps (use browser only)',
      "Set up scheduled 'online windows' (e.g. 6-7pm)",
      'Create a distraction log — note every urge for one week',
      'Establish a phone-free morning routine (first 30 min)',
    ],
  },
  {
    number: 3,
    title: 'Monk Mode',
    range: 'Apr — Jun',
    color: 'rose',
    items: [
      'Remove all social media from phone completely',
      'Use a basic phone or leave smartphone at home during study',
      'Block all non-essential websites 24/7',
      "Implement 'airplane mode' during all study blocks",
      'Complete a full weekend digital detox',
    ],
  },
] as const;

const phaseStyles: Record<string, { accent: string; accentBg: string; checkBg: string; checkBorder: string; completedBorder: string; completedGlow: string; badge: string; text: string }> = {
  blue: {
    accent: 'border-l-blue-500',
    accentBg: 'bg-blue-500',
    checkBg: 'bg-blue-500',
    checkBorder: 'border-blue-300 dark:border-blue-600',
    completedBorder: 'border-blue-400 dark:border-blue-500',
    completedGlow: 'shadow-blue-200/50 dark:shadow-blue-900/30',
    badge: 'bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-300',
    text: 'text-blue-600 dark:text-blue-400',
  },
  amber: {
    accent: 'border-l-amber-500',
    accentBg: 'bg-amber-500',
    checkBg: 'bg-amber-500',
    checkBorder: 'border-amber-300 dark:border-amber-600',
    completedBorder: 'border-amber-400 dark:border-amber-500',
    completedGlow: 'shadow-amber-200/50 dark:shadow-amber-900/30',
    badge: 'bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300',
    text: 'text-amber-600 dark:text-amber-400',
  },
  rose: {
    accent: 'border-l-rose-500',
    accentBg: 'bg-rose-500',
    checkBg: 'bg-rose-500',
    checkBorder: 'border-rose-300 dark:border-rose-600',
    completedBorder: 'border-rose-400 dark:border-rose-500',
    completedGlow: 'shadow-rose-200/50 dark:shadow-rose-900/30',
    badge: 'bg-rose-100 text-rose-700 dark:bg-rose-900/40 dark:text-rose-300',
    text: 'text-rose-600 dark:text-rose-400',
  },
};

const PhasedDetoxRoadmap = () => {
  const [checked, setChecked] = useState<Set<string>>(new Set());

  const toggle = (key: string) => {
    setChecked((prev) => {
      const next = new Set(prev);
      if (next.has(key)) next.delete(key);
      else next.add(key);
      return next;
    });
  };

  const totalChecked = checked.size;
  const totalItems = PHASES.reduce((s, p) => s + p.items.length, 0);
  const allDone = totalChecked === totalItems;

  /* Progress line: fraction of phases completed (by items) */
  let cumulativeChecked = 0;
  const phaseCompletions = PHASES.map((phase) => {
    const phaseChecked = phase.items.filter((_, i) => checked.has(`${phase.number}-${i}`)).length;
    cumulativeChecked += phaseChecked;
    return { phaseChecked, phaseTotal: phase.items.length, done: phaseChecked === phase.items.length };
  });
  const progressPct = Math.round((totalChecked / totalItems) * 100);

  return (
    <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      {/* Header */}
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">
        Phased Detox Roadmap
      </h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mt-1 mb-2">
        Progressively build your digital fortress across the school year.
      </p>

      {/* Overall progress */}
      <div className="text-center mb-8">
        <MotionDiv
          key={totalChecked}
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          className="inline-block"
        >
          <span className={`text-4xl font-bold tabular-nums ${allDone ? 'text-emerald-500' : 'text-zinc-700 dark:text-zinc-200'}`}>
            {totalChecked}
          </span>
          <span className="text-lg font-bold text-zinc-400 ml-1">/ {totalItems}</span>
        </MotionDiv>
        <p className="text-sm font-semibold text-zinc-500 dark:text-zinc-400 mt-0.5">barriers activated</p>
      </div>

      {/* Timeline */}
      <div className="relative pl-8 md:pl-10">
        {/* Vertical progress line */}
        <div className="absolute left-3 md:left-4 top-0 bottom-0 w-1 rounded-full bg-zinc-200 dark:bg-zinc-700">
          <motion.div
            className="w-full rounded-full bg-emerald-500"
            animate={{ height: `${progressPct}%` }}
            transition={{ type: 'spring', stiffness: 80, damping: 18 }}
          />
        </div>

        <div className="space-y-8">
          {PHASES.map((phase, pi) => {
            const style = phaseStyles[phase.color];
            const pc = phaseCompletions[pi];
            const phaseDone = pc.done;

            return (
              <MotionDiv
                key={phase.number}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: pi * 0.12 }}
                className={`relative rounded-xl border-l-4 ${style.accent} border border-zinc-200 dark:border-zinc-700 p-5 md:p-6 transition-shadow duration-500 ${phaseDone ? `${style.completedBorder} shadow-lg ${style.completedGlow}` : ''}`}
              >
                {/* Dot on timeline */}
                <div className={`absolute -left-[calc(2rem+10px)] md:-left-[calc(2.5rem+10px)] top-6 w-5 h-5 rounded-full border-4 border-white dark:border-zinc-800 ${phaseDone ? 'bg-emerald-500' : style.accentBg}`} />

                {/* Phase header */}
                <div className="flex flex-wrap items-center gap-2 mb-3">
                  <span className={`text-xs font-bold px-2.5 py-0.5 rounded-full ${style.badge}`}>
                    Phase {phase.number}
                  </span>
                  <h5 className="font-serif text-lg font-semibold text-zinc-800 dark:text-white">
                    {phase.title}
                  </h5>
                  <span className="text-xs text-zinc-400 dark:text-zinc-500 ml-auto">{phase.range}</span>
                </div>

                {/* Progress count */}
                <p className={`text-xs font-semibold mb-3 ${style.text}`}>
                  {pc.phaseChecked}/{pc.phaseTotal} complete
                </p>

                {/* Checklist */}
                <ul className="space-y-2.5">
                  {phase.items.map((item, ii) => {
                    const key = `${phase.number}-${ii}`;
                    const isChecked = checked.has(key);
                    return (
                      <li key={key}>
                        <button
                          onClick={() => toggle(key)}
                          className="flex items-start gap-3 w-full text-left group"
                        >
                          {/* Custom checkbox */}
                          <MotionDiv
                            className={`mt-0.5 flex-shrink-0 w-5 h-5 rounded-md border-2 flex items-center justify-center transition-colors ${isChecked ? `${style.checkBg} border-transparent` : `${style.checkBorder} bg-white dark:bg-zinc-900`}`}
                            animate={isChecked ? { scale: [1, 1.25, 1] } : { scale: 1 }}
                            transition={{ duration: 0.25 }}
                          >
                            {isChecked && (
                              <svg width="12" height="12" viewBox="0 0 12 12" fill="none" className="text-white">
                                <path d="M2.5 6L5 8.5L9.5 3.5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                              </svg>
                            )}
                          </MotionDiv>
                          <span className={`text-sm leading-snug transition-colors ${isChecked ? 'line-through text-zinc-400 dark:text-zinc-500' : 'text-zinc-700 dark:text-zinc-300 group-hover:text-zinc-900 dark:group-hover:text-white'}`}>
                            {item}
                          </span>
                        </button>
                      </li>
                    );
                  })}
                </ul>

                {/* Phase completion badge */}
                <AnimatePresence>
                  {phaseDone && (
                    <MotionDiv
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      exit={{ opacity: 0, height: 0 }}
                      className="mt-4 p-3 rounded-lg bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800 text-center text-sm font-semibold text-emerald-700 dark:text-emerald-300"
                    >
                      Phase {phase.number} complete
                    </MotionDiv>
                  )}
                </AnimatePresence>
              </MotionDiv>
            );
          })}
        </div>
      </div>

      {/* Celebration message */}
      <AnimatePresence>
        {allDone && (
          <MotionDiv
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 10 }}
            className="mt-8 p-5 rounded-xl bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-300 dark:border-emerald-700 text-center"
          >
            <p className="font-serif text-lg font-semibold text-emerald-700 dark:text-emerald-300">
              Full digital fortress activated.
            </p>
            <p className="text-sm text-emerald-600 dark:text-emerald-400 mt-1">
              You&apos;ve removed every barrier between you and deep focus.
            </p>
          </MotionDiv>
        )}
      </AnimatePresence>
    </div>
  );
};

// --- MODULE COMPONENT ---
const DigitalDistractionModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'adversary', title: 'Why Your Phone Wins', eyebrow: '01 // Your Brain vs Your Phone', icon: BrainCircuit },
    { id: 'hardware-barrier', title: 'The Phone Swap', eyebrow: '02 // The Physical Barrier', icon: Shield },
    { id: 'software-fortification', title: 'Locking Down Your Laptop', eyebrow: '03 // Blocking Distractions', icon: Laptop },
    { id: 'environmental-engineering', title: 'Setting Up Your Space', eyebrow: '04 // Your Study Zone', icon: Home },
    { id: 'behavioral-engineering', title: 'Building Better Habits', eyebrow: '05 // Making It Automatic', icon: Repeat },
    { id: 'social-dynamics', title: 'Dealing with FOMO', eyebrow: '06 // Your Friends Will Survive', icon: Users },
    { id: 'roadmap', title: 'Your Step-by-Step Plan', eyebrow: '07 // Putting It All Together', icon: Map },
  ];

  return (
    <ModuleLayout
      moduleNumber="08"
      moduleTitle="Digital Distractions"
      moduleSubtitle="Take Back Your Focus"
      moduleDescription="Your phone is designed to steal your attention. This module gives you a step-by-step plan to block distractions and actually get your study hours to count."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Take Back Your Focus"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="Why Your Phone Wins." eyebrow="Step 1" icon={BrainCircuit} theme={theme}>
              <p>If you can't stop reaching for your phone, that's not because you're lazy or weak. It's because your brain is literally wired to lose this fight right now. The part of your brain that handles <Highlight description="This is the part right behind your forehead that helps you plan ahead, resist impulses, and make good decisions. In your teens, it's still developing -- which is why it's harder to say no to distractions." theme={theme}>self-control and planning</Highlight> isn't fully developed yet, while the part that craves <Highlight description="This is the emotional, reward-seeking part of your brain. It's the bit that lights up when you get a notification or a like. In your teens, it's running the show." theme={theme}>rewards and excitement</Highlight> is running on overdrive.</p>
              <p>Apps like TikTok, Instagram, and Snapchat are built to exploit exactly this. They work like <Highlight description="Think of a slot machine -- you never know when you'll hit the jackpot, so you keep pulling the lever. Social media does the same thing with likes and messages. You keep checking because sometimes there's something exciting, and that unpredictability is addictive." theme={theme}>digital slot machines</Highlight>, giving you random hits of likes and messages that keep you coming back.</p>
              <p>Here's the real kicker: every time you switch from studying to checking your phone, your brain doesn't just snap back. There's a kind of <Highlight description="When you switch from studying to your phone, your brain doesn't reset instantly. Part of it is still thinking about what you just saw. Research shows it takes about 23 minutes to get properly focused again." theme={theme}>mental hangover</Highlight> that takes about 23 minutes to clear. This module is about taking back control of your own attention -- so your study time actually counts.</p>
              <PersonalStory name="Ciara" role="5th Year, Cork">
                <p>"I used to think I was just bad at concentrating. Turns out I was checking my phone about 8 times an hour during study. Once I worked out how much focus time I was actually losing, it proper shocked me. I wasn't studying -- I was just sitting at a desk."</p>
              </PersonalStory>
              <AttentionDeficitCalculator />
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="The Phone Swap." eyebrow="Step 2" icon={Shield} theme={theme}>
              <p>Willpower alone won't cut it -- your brain is working against you (remember that underdeveloped self-control from Step 1?). So instead of relying on discipline, the smartest move is to change the actual device you're using during study time.</p>
              <p>The nuclear option? A "dumb phone" -- one of those basic Nokias with no apps, no feed, no TikTok. If a notification can't reach you, it can't distract you. But there's a middle ground too. The key idea is <Highlight description="Basically, making it annoying to do the thing you want to avoid. If checking social media requires typing on tiny buttons or loading a slow browser, you'll naturally do it less. The harder something is, the less likely you are to bother." theme={theme}>friction</Highlight> -- the harder you make it to access distractions, the less likely you are to reach for them. Even something as simple as logging out of apps, or leaving your phone in another room, adds enough friction to break the habit.</p>
              <p>You don't need to buy a new phone. You could borrow an old one from a parent or sibling during study blocks, or just use your phone's built-in Focus Mode or Do Not Disturb. The goal is the same: make distractions harder to reach than your books.</p>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="Locking Down Your Laptop." eyebrow="Step 3" icon={Laptop} theme={theme}>
              <p>Your laptop is both your best study tool and your biggest trap. You open it to study, and twenty minutes later you're watching YouTube. Browser extensions that "block" sites are easy to turn off when you're tempted. What you need are proper <Highlight description="Free apps like Cold Turkey or Freedom that block distracting websites and apps on your laptop. The best ones have a 'locked mode' that makes it literally impossible to undo the block until the timer runs out -- even if you restart your computer." theme={theme}>website blockers</Highlight> that you genuinely can't get around.</p>
              <p>The best approach is an <Highlight description="Instead of blocking individual bad sites (you'll always miss one), you block everything and then only allow the specific sites you need -- like Studyclix, Examinations.ie, or your school portal. This way, only useful stuff gets through." theme={theme}>allowlist</Highlight> -- block everything except the handful of sites you actually need for study, like Studyclix or Examinations.ie. And if you're worried about needing to look something up, try downloading what you need beforehand. You can save Wikipedia articles, past papers, or notes for <Highlight description="You can use tools like Kiwix to save entire websites (like Wikipedia) onto your laptop so you can access them without the internet. That way you get the information without the temptation of going online." theme={theme}>offline use</Highlight> so you have the information without the temptation of a live internet connection.</p>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="Setting Up Your Space." eyebrow="Step 4" icon={Home} theme={theme}>
              <p>Where you study matters more than you think. Here's a wild fact: just having your phone on the desk -- even face down, even on silent -- <Highlight description="Research from the University of Texas found that just having your phone visible drains your brainpower. Your brain is constantly spending energy resisting the urge to check it, even if you don't realise it. Moving it to another room completely removes that drain." theme={theme}>makes you worse at concentrating</Highlight>. Your brain is quietly fighting the urge to pick it up, and that uses up energy you could be putting into study.</p>
              <p>"Out of sight, out of mind" isn't just a saying -- it's how your brain actually works. The fix is dead simple: move your phone out of the room while you study. Charge it in the kitchen or the hall. If you use it to check the time, stick a cheap clock on your desk instead (or use a watch). The less you can see your phone, the less it pulls at your attention.</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Building Better Habits." eyebrow="Step 5" icon={Repeat} theme={theme}>
              <p>The best way to beat distractions isn't willpower -- it's making good habits automatic so you don't even have to think about it. The first trick is <Highlight description="You attach a new habit to something you already do every day. The formula: 'After I [thing I always do], I will [new thing].' Because the first habit is automatic, the second one gets pulled along with it." theme={theme}>habit stacking</Highlight>. You pair your new habit with something you already do without thinking. For example: "After I walk in the door from school, I'll put my phone straight on the kitchen charger." You don't have to decide each day -- it just becomes what you do.</p>
              <p>The second trick is making <Highlight description="You decide in advance what you'll do when a specific situation happens. The formula: 'If [this happens], then I will [do this].' For example: 'If I feel the urge to check Instagram, I'll stand up and do 5 star jumps.' It takes the decision-making out of the moment when you're tired and your willpower is low." theme={theme}>if-then plans</Highlight>. You decide in advance what you'll do when temptation hits. For example: "If I feel the urge to check Instagram, I'll stand up and do 5 star jumps." The point is that you've already made the decision, so when the moment comes, you don't have to negotiate with your tired brain.</p>
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="Dealing with FOMO." eyebrow="Step 6" icon={Users} theme={theme}>
              <p>Let's be real -- the hardest part of putting your phone away isn't the phone. It's the fear that you're missing out on something. What if someone messages and you don't reply? What if something kicks off in the group chat? The trick is to <Highlight description="Just give your mates a heads up. A quick message like 'I'm off my phone from 5 to 9 for study, I'll reply after' takes the pressure off. People are way more understanding than you expect, and once they know, they stop expecting instant replies." theme={theme}>tell your friends what you're doing</Highlight>. Send a quick message to your group chat: "I'm off my phone from 5 to 9 for study, I'll reply after." Once people know, the pressure disappears.</p>
              <p>The other move is to <Highlight description="Instead of scrolling on and off all day (which means you're never fully studying and never fully relaxing), you pick a specific time for social media -- like 8:30 to 9:30pm. You'll actually enjoy it more because you're not feeling guilty, and the rest of your day stays focused." theme={theme}>batch your screen time</Highlight>. Instead of dipping in and out of social media all day (which means you're never fully studying and never fully chilling), pick one window -- say 8:30 to 9:30pm -- and save it all for then. You'll actually enjoy it more because you're not feeling guilty about it.</p>
            </ReadingSection>
          )}
          {activeSection === 6 && (
            <ReadingSection title="Your Step-by-Step Plan." eyebrow="Step 7" icon={Map} theme={theme}>
              <p>You don't have to do everything at once. This is a gradual plan that builds up across the Leaving Cert year. <strong>Phase 1: Getting Started (Sept - Dec).</strong> Turn off unnecessary notifications, start charging your phone outside your bedroom, and figure out where your time actually goes. <strong>Phase 2: Locking It Down (Jan - Mar).</strong> Set up website blockers on your laptop, start batching your social media into one window each evening, and delete the worst time-wasting apps. <strong>Phase 3: Full Focus (Apr - June).</strong> This is where you go all-in for the exams. Minimal phone use, locked blockers on your laptop, and maybe even deactivating social media until the Leaving Cert is over.</p>
              <PhasedDetoxRoadmap />
              <MicroCommitment theme={theme}>
                <p>Tonight, move your phone charger out of your bedroom and into the kitchen. That's it. One small change, but it's the single most effective thing you can do right now.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default DigitalDistractionModule;
