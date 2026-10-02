
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React from 'react';
import { PinballExercise, IncubationExercise } from './learning/ReaderExercises';
import {
  Brain, SlidersHorizontal, Lightbulb, PauseCircle, Zap, Clock
} from 'lucide-react';
import { type ModuleProgress } from '../types';
import { purpleTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';
import { useEssentialsMode } from '../hooks/useEssentialsMode';
import { Cite } from './ModuleReferences';
import { BIMODAL_BRAIN_REFERENCE_LIST } from '../data/references/bimodalBrain';

const theme = purpleTheme;

const BimodalBrainModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const essentials = useEssentialsMode();

  const sections = essentials ? [
    { id: 'two-modes', title: 'Your Brain Has Two Gears', eyebrow: '01 // The Big Idea', icon: Brain },
    { id: 'focused-engine', title: 'Focus & Diffuse', eyebrow: '02 // The Two Modes', icon: Zap },
    { id: 'toggling', title: 'Switching Gears', eyebrow: '03 // The Art of the Break', icon: PauseCircle },
    { id: 'blueprint', title: 'Your Game Plan', eyebrow: '04 // Your Action Plan', icon: SlidersHorizontal },
  ] : [
    { id: 'two-modes', title: 'Your Brain Has Two Gears', eyebrow: '01 // The Big Idea', icon: Brain },
    { id: 'focused-engine', title: 'Gear One: Laser Focus', eyebrow: '02 // Locking In', icon: Zap },
    { id: 'diffuse-network', title: 'Gear Two: The Wandering Mind', eyebrow: '03 // Letting Go', icon: Lightbulb },
    { id: 'toggling', title: 'Switching Between Gears', eyebrow: '04 // The Art of the Break', icon: PauseCircle },
    { id: 'procrastination-link', title: 'Why We Put Things Off', eyebrow: '05 // Why We Delay', icon: Clock },
    { id: 'blueprint', title: 'Your Two-Gear Game Plan', eyebrow: '06 // Your Action Plan', icon: SlidersHorizontal },
  ];

  return (
    <ModuleLayout
      moduleNumber="08"
      moduleTitle="The Bimodal Brain"
      moduleSubtitle="The Bimodal Brain"
      moduleDescription="Your brain has two modes — one for grinding through problems, one for creative breakthroughs. Learning when to switch between them is a game-changer for your study."
      theme={theme}
      sections={sections}
      fullSectionsCount={6}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Switch Your Mode"
      references={BIMODAL_BRAIN_REFERENCE_LIST}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="Your Brain Has Two Gears." eyebrow="Step 1" icon={Brain} theme={theme}>
              {essentials ? (
                <p>Your brain has two modes. <Highlight description="When you're fully locked in on something — like working through a maths problem step by step. Your brain is zoomed in and focused on the details." theme={theme}>Focused Mode</Highlight> is your "head down" gear for problems you know how to solve. <Highlight description="When your mind is relaxed and wandering — like daydreaming in the shower. Your brain is making connections in the background that you'd never spot while concentrating hard." theme={theme}>Diffuse Mode</Highlight> is your relaxed gear where your brain connects dots in the background.<Cite n={1} /> You need both.</p>
              ) : (
                <p>Here's something most people never get told: your brain doesn't just think one way — it has two completely different modes. <Highlight description="When you're fully locked in on something — like working through a maths problem step by step. Your brain is zoomed in and focused on the details." theme={theme}>Focused Mode</Highlight> is your "head down, get it done" gear. It's what kicks in when you're working through a maths problem you know how to solve. Then there's <Highlight description="When your mind is relaxed and wandering — like daydreaming in the shower. Your brain is making connections in the background that you'd never spot while concentrating hard." theme={theme}>Diffuse Mode</Highlight> — your "chill out and let ideas come to you" gear. It's that relaxed, mind-wandering state where your brain quietly connects dots you didn't even know were there.<Cite n={1} /></p>
              )}
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title={essentials ? "Focus & Diffuse." : "Gear One: Laser Focus."} eyebrow="Step 2" icon={Zap} theme={theme}>
                {essentials ? (
                  <>
                    <p>Focused Mode is for step-by-step work. You're practising equations or following methods. But if you hit a wall, this mode works against you. Your thoughts keep bouncing off the same spots.</p>
                    <p>Diffuse Mode is where "Aha!" moments happen. Your brain links ideas from different places.<Cite n={2} /> You can't force it. Go for a walk or stare out the window. When you stop trying, your brain does its best work.</p>
                  </>
                ) : (
                  <p>Think of Focused Mode like a pinball machine with tightly packed bumpers. Your thoughts bounce around in a small area, working through something familiar step by step. This is the gear you need for practising equations in Maths or balancing reactions in Chemistry — anything where you're following a method you've already learned. It's the mode you're in during a focused study sprint. But here's the catch: if you hit a wall on something new or tricky, this mode can actually work against you. Your thoughts just keep bouncing off the same spots, and you end up more frustrated than when you started.</p>
                )}
                <PinballExercise />
            </ReadingSection>
          )}
          {!essentials && activeSection === 2 && (
             <ReadingSection title="Gear Two: The Wandering Mind." eyebrow="Step 3" icon={Lightbulb} theme={theme}>
                <p>Now picture the pinball machine with the bumpers spread way apart. Your thoughts can travel across your whole brain, linking up ideas from completely different places — maybe something from History clicks with a Biology concept, or a song lyric helps you remember a formula. This is where those "Aha!" moments come from.<Cite n={2} /> The thing is, you can't force it. You just have to create the right conditions — go for a walk, have a shower, stare out the window for a bit. When you stop trying so hard, your brain does some of its best work.</p>
            </ReadingSection>
          )}
          {(essentials ? activeSection === 2 : activeSection === 3) && (
             <ReadingSection title="Switching Between Gears." eyebrow={essentials ? "Step 3" : "Step 4"} icon={PauseCircle} theme={theme}>
                {essentials ? (
                  <p>When you're stuck, step away on purpose. Your brain keeps working in the background. This is the <Highlight description="That thing where the answer just 'pops' into your head after you've walked away from a problem for a while. Your brain was quietly working on it the whole time." theme={theme}>Incubation Effect</Highlight>.<Cite n={3} /> Come back and the answer often clicks.</p>
                ) : (
                  <p>This is the real skill: knowing when to switch gears. Grind away in Focused Mode on a tough problem. When you hit a wall, step away on purpose — take a break, go for a walk, do something completely different. Here's what's cool: your brain keeps working on the problem in the background even when you're not thinking about it (this is called the <Highlight description="That thing where the answer just 'pops' into your head after you've walked away from a problem for a while. Your brain was quietly working on it the whole time." theme={theme}>Incubation Effect</Highlight>).<Cite n={3} /> When you come back to the problem, the answer often just clicks.</p>
                )}
                <IncubationExercise />
                <MicroCommitment theme={theme}><p>The next time you're stuck on a homework problem, don't just push harder. Get up and walk around for 5 minutes. You're not giving up — you're using a different part of your brain.</p></MicroCommitment>
            </ReadingSection>
          )}
          {!essentials && activeSection === 4 && (
            <ReadingSection title="Why We Put Things Off." eyebrow="Step 5" icon={Clock} theme={theme}>
                <p>Ever notice how the hardest part of studying is just... starting? That's because your brain doesn't like the discomfort of switching into Focused Mode for something hard. For a task you find aversive, just anticipating it can register as genuine discomfort, so you scroll your phone instead.<Cite n={4} /> The trick? Don't tell yourself you need to study for an hour. Just commit to 5 minutes. That's it. Once you're actually going, the pain fades and it's way easier to keep at it. Starting is always the worst bit — once you're in, you're in.</p>
            </ReadingSection>
          )}
          {(essentials ? activeSection === 3 : activeSection === 5) && (
             <ReadingSection title={essentials ? "Your Game Plan." : "Your Two-Gear Game Plan."} eyebrow={essentials ? "Step 4" : "Step 6"} icon={SlidersHorizontal} theme={theme}>
                {essentials ? (
                  <p>Your study needs both gears. Focused work blocks AND real breaks. Not phone breaks. A walk, music, or staring at the ceiling. Build both into your routine. You'll get more done in less time.</p>
                ) : (
                  <p>So here's the bottom line: your study sessions need both gears. Blocks of proper, focused work AND real breaks where you actually switch off. Not "I'll check Instagram for a sec" breaks — proper ones. A walk. Some music. Staring at the ceiling. This isn't being lazy; it's how your brain actually learns. Build both into your study routine and you'll get more done in less time than if you just tried to grind for hours straight.</p>
                )}
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default BimodalBrainModule;
