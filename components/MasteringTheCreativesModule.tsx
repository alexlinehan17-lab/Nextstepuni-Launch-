/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React from 'react';
import { Key, PenTool, SlidersHorizontal, Film, Shield, Wrench } from 'lucide-react';
import { ModuleProgress } from '../types';
import { slateTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = slateTheme;

// --- MODULE COMPONENT ---
const MasteringTheCreativesModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'shift-from-talent', title: 'The Talent Myth', eyebrow: '01 // The Paradigm Shift', icon: Key },
    { id: 'art-protocol', title: 'Art: The Visual Journal', eyebrow: '02 // The Art Protocol', icon: PenTool },
    { id: 'music-protocol', title: 'Music: The Algorithm of Melody', eyebrow: '03 // The Music Protocol', icon: SlidersHorizontal },
    { id: 'film-protocol', title: 'Film: The Grammar of Vision', eyebrow: '04 // The Film Protocol', icon: Film },
    { id: 'pressure-protocol', title: 'Mastering Exam Pressure', eyebrow: '05 // The Pressure Protocol', icon: Shield },
    { id: 'action-plan', title: 'Your Creative Blueprint', eyebrow: '06 // The Action Plan', icon: Wrench },
  ];

  return (
    <ModuleLayout
      moduleNumber="07"
      moduleTitle="Mastering the Creatives"
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Talent Myth." eyebrow="Step 1" icon={Key} theme={theme}>
              <p>For years, you've probably heard the same old story: you're either "good at art" or you're not. You're born with "talent," or you're not. That's a myth. The Leaving Cert creative subjects--Art, Music, and Film--are not a lottery of natural ability. They're a game of skill.</p>
              <p>A deep dive into the marking schemes and examiner reports reveals the truth: top grades aren't awarded for some magical spark of genius. They're awarded for mastering a process. High performance is the result of <Highlight description="Focused, strategic practice that pushes you just beyond your current comfort zone. It's about working on your weaknesses, not just repeating what you're good at." theme={theme}>deliberate practice</Highlight>, understanding the technical rules of the game, and mastering <Highlight description="Working in cycles of creating, getting feedback, and refining. It's about treating your work as a draft that can always be improved, not a one-shot masterpiece." theme={theme}>iterative processes</Highlight>. This module is your playbook for learning these skills.</p>
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="Art: The Visual Journal." eyebrow="Step 2" icon={PenTool} theme={theme}>
              <p>The new Art course has one core message: your process is as important as your final product. The <Highlight description="Formerly the sketchbook, this is now the 50% coursework component. It's the documented 'thinking process' behind your final piece." theme={theme}>Visual Journal</Highlight> is not a gallery of finished drawings; it's a messy laboratory of thought. A high-scoring journal shows your journey from an initial idea to a final piece.</p>
              <p>Kickstart your project with mind maps that go beyond words, using textures and sensory details. Master observational drawing not by "copying," but by tricking your brain with techniques like drawing upside down (<Highlight description="An observational drawing exercise where you draw from an upside-down reference photo, forcing your brain to see shapes and lines instead of recognizable objects." theme={theme}>Inversion</Highlight>) or drawing the space *around* an object (<Highlight description="An exercise where you focus on drawing the empty shapes between and around objects, which dramatically improves your sense of proportion." theme={theme}>Negative Space</Highlight>).</p>
               <MicroCommitment theme={theme}><p>Take any object on your desk. For just two minutes, try to draw it without looking at the paper, keeping your eyes locked on the object. This is 'Blind Contour' drawing. It feels weird, but it's a powerful way to train your eyes to truly see.</p></MicroCommitment>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="Music: The Algorithm of Melody." eyebrow="Step 3" icon={SlidersHorizontal} theme={theme}>
              <p>The 16-bar melody question is not a test of your inner Mozart; it's a structural engineering problem. You can get full marks by treating it like a puzzle with clear rules. Before you write a single note, run your "pre-flight check": What's the Key Signature? The Time Signature? What's the instrument's range?</p>
              <p>The most reliable structure is the A-A1-B-A2 formula. **A** is given. **A1** is a response that starts the same but ends differently, usually with a <Highlight description="The process of changing from one key to another. A mandatory part of the melody composition question." theme={theme}>modulation</Highlight> to a new key. **B** is the contrast--go higher, change the rhythm. **A2** is the return home, resolving firmly back in the original key. It's an algorithm, not a whim.</p>
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="Film: The Grammar of Vision." eyebrow="Step 4" icon={Film} theme={theme}>
              <p>Film is not just a recorded story; it's a language constructed through technical choices. A H1 student doesn't just describe the plot; they analyze the *form*. How did the director use a <Highlight description="A camera shot where the camera looks up at the subject, making them seem powerful or threatening." theme={theme}>Low Angle Shot</Highlight> to make the villain seem powerful? How did they use <Highlight description="High-contrast lighting with deep shadows, often used in horror and noir to create mystery and danger." theme={theme}>Low-Key Lighting (Chiaroscuro)</Highlight> to create a sense of mystery?</p>
              <p>For the Comparative Study, you must analyze these technical choices as part of the General Vision & Viewpoint or Cultural Context. In *Blade Runner*, the constant rain and "Venetian blind" shadows aren't just for atmosphere; they're direct quotes from 1940s <Highlight description="A cinematic style known for its dark themes, cynical characters, and high-contrast, black-and-white visuals." theme={theme}>Film Noir</Highlight>, creating a feeling of paranoia and fractured identity.</p>
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="Mastering Exam Pressure." eyebrow="Step 5" icon={Shield} theme={theme}>
              <p>Performance anxiety is the primary enemy in all creative subjects, from the Music practical to the Art deadline. It's a physiological response to perceived social judgment. Your brain releases adrenaline, causing trembling and shallow breathing. The key is to manage the biology, not just the thoughts.</p>
              <p>Use <Highlight description="A breathing technique (Inhale 4s, Hold 4s, Exhale 4s, Hold 4s) that activates the body's 'rest and digest' system to counteract the adrenaline rush." theme={theme}>Box Breathing</Highlight> to calm your nervous system. Reframe the exam from a test of "correctness" to a "communication of emotion." And most importantly, use <Highlight description="Practicing under exam-like conditions (e.g., performing for a mock examiner) to desensitize your brain to the context triggers of the real event." theme={theme}>Simulation Training</Highlight>. The more you expose your brain to the pressure in a safe environment, the less it will panic on the day.</p>
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="Your Creative Blueprint." eyebrow="Step 6" icon={Wrench} theme={theme}>
              <p>You now have the master key. "Talent" is a myth. Success in creative subjects is a skill built through deliberate practice and strategic thinking. By mastering the process of the Visual Journal, the algorithm of melody, the grammar of film, and the psychology of performance, you can engineer your own success.</p>
              <MicroCommitment theme={theme}>
                <p>Pick ONE technique from this module. Just one. Whether it's a 'Blind Contour' drawing, analyzing one movie scene for lighting, or trying Box Breathing for one minute. Commit to trying it this week. You've just taken your first step to becoming a creative master.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default MasteringTheCreativesModule;
