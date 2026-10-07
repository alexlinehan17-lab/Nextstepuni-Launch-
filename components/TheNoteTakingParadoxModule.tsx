import { BrandedNoteComparison } from './learning/BrandedCharts';
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import { FileText,GitBranch,Layers,SquarePen,Wrench } from 'lucide-react';
import React from 'react';
import { NOTE_TAKING_PARADOX_REFERENCE_LIST } from '../data/references/noteTakingParadox';
import { useEssentialsMode } from '../hooks/useEssentialsMode';
import { indigoTheme } from '../moduleThemes';
import { type ModuleProgress } from '../types';
import CornellNoteSimulator from './activities/CornellNoteSimulator';
import { ModuleLayout } from './ModuleLayout';
import { Cite } from './ModuleReferences';
import { ConceptCardGrid,Highlight,MicroCommitment,PersonalStory,ReadingSection } from './ModuleShared';

const theme = indigoTheme;

// --- INTERACTIVE COMPONENTS ---

// 1. NOTE-TAKING COMPARISON (Planning Paradox style dual-chart)
const NoteTakingComparison = BrandedNoteComparison;

// 2. CORNELL NOTE SIMULATOR
// --- MODULE COMPONENT ---
const TheNoteTakingParadoxModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const essentials = useEssentialsMode();
  const sections = [
    { id: 'transcription-trap', title: 'The Copy-Paste Trap', eyebrow: '01 // The Paradox', icon: FileText },
    { id: 'generative-note-taking', title: 'Notes That Actually Work', eyebrow: '02 // Think, Don\'t Copy', icon: SquarePen },
    { id: 'cornell-system', title: 'The Cornell Method', eyebrow: '03 // The System', icon: Layers },
    { id: 'mapping-vs-listing', title: 'Maps vs Lists', eyebrow: '04 // Choosing Your Layout', icon: GitBranch },
    { id: 'building-your-system', title: 'Building Your Own System', eyebrow: '05 // Putting It Together', icon: Wrench },
  ];

  return (
    <ModuleLayout
      moduleNumber="45"
      moduleTitle="The Note-Taking Paradox"
      moduleSubtitle="Why Less Is More"
      moduleDescription="More notes doesn't mean more learning. Find out why writing less — but thinking more — is the secret to notes that actually help you in the exam."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Think More, Write Less"
      references={NOTE_TAKING_PARADOX_REFERENCE_LIST}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Transcription Trap." eyebrow="Step 1" icon={FileText} theme={theme}>
              {essentials ? (
                <>
                  <p>The more you copy word for word, the less you learn. In one well-known study, students who took fewer notes in their own words understood more than those who typed the lecture almost verbatim.<Cite n={1} /> Putting ideas in your own words forces you to pick out what matters.</p>
                  <p>That thinking process IS the learning. Copying word for word lets your brain go on autopilot. The method that feels slower actually builds real understanding.</p>
                </>
              ) : (
                <>
                  <p>Here is a paradox that trips up nearly every student: the more notes you take, the less you actually learn. A well-known study compared students who typed their notes on laptops with students who wrote by hand. The laptop group wrote far more — often copying the lecture close to word for word — while the handwriters wrote less and put things in their own words. On questions that needed real understanding, <Highlight description="When you copy everything word for word, your brain switches off. You feel busy, but you're not actually thinking about what's being said." theme={theme}>the handwriters came out ahead</Highlight>.<Cite n={1} /> (Later replications suggest the handwriting-versus-laptop part is less clear-cut than first reported — what really matters is whether you copy verbatim or process ideas into your own words, not the device you use.)</p>
                  <PersonalStory name="Maeve" role="6th Year, Sligo" junior={{ name: 'Maeve', role: '3rd Year, Sligo', children: <p>I used to type every single word in class — my notes were basically a transcript. I felt so productive. Then I'd sit down to study and realise I couldn't remember any of it. When I switched to writing by hand and putting things in my own words, my notes got way shorter but I actually understood what I'd written. My History grade went up a whole grade in the next test.</p> }}><p>I used to type every single word in class — my notes were basically a transcript. I felt so productive. Then I'd sit down to study and realise I couldn't remember any of it. When I switched to writing by hand and putting things in my own words, my notes got way shorter but I actually understood what I'd written. My History grade went up a full grade in the mocks.</p></PersonalStory>
                  <p>Why? Because when you write by hand, you physically can't keep up with every word. You're forced to <Highlight description="When you have to pick out the important bits and say them your own way, your brain has to actually think about the material. That thinking is where the learning happens." theme={theme}>pick out what matters and say it your own way</Highlight>. You have to listen, understand, decide what's important, and rephrase it — all in real time. That process IS the learning. Your brain has to work hard to shrink the information down, and that effort is what makes it <Highlight description="The stronger the mental effort you put into making sense of something, the better your brain stores it and the easier it is to remember later." theme={theme}>stick in your memory</Highlight>. Copying word for word, on the other hand, skips all of that. Your hand is busy, but your brain is on autopilot.</p>
                  <p>This is the <Highlight description="It sounds backwards, but the study method that feels easiest and most productive — writing everything down — actually leads to the worst results. The method that feels harder — being selective and using your own words — leads to the best results." theme={theme}>Note-Taking Paradox</Highlight>: the strategy that feels most productive — capturing everything — is actually the one that produces the least learning. And the strategy that feels slow and incomplete — picking out the key ideas and putting them in your own words — is the one that builds real understanding. The rest of this module will show you how to make this work for you.</p>
                </>
              )}
              <NoteTakingComparison />
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="Notes That Actually Work." eyebrow="Step 2" icon={SquarePen} theme={theme}>
              {essentials ? (
                <p>Students who paraphrase and summarise tend to outperform word-for-word note-takers, especially on questions that need real understanding.<Cite n={2} /> Real learning happens when you connect new information to what you already know.<Cite n={3} /> Three moves will transform your notes: summarise, give your own example, and connect to existing knowledge.</p>
              ) : (
                <>
                  <p>This idea — that less writing leads to more learning — has been proven again and again over decades of research. Students who paraphrase, summarise, and make connections in their notes <Highlight description="When you put things in your own words instead of copying, you tend to score better — not just on basic recall questions, but on the tricky ones where you have to apply what you've learned to something new." theme={theme}>tend to outperform word-for-word note-takers</Highlight><Cite n={2} /> on the kinds of questions that actually matter. Not just "name this thing" questions, but the ones where you have to apply what you know to a brand new situation — exactly the kind of questions you see in big exams.</p>
                  <p>Here's why it works: <Highlight description="Real learning only happens when you actively make connections between new stuff and things you already know. Just receiving information passively — no matter how much of it you write down — doesn't create understanding." theme={theme}>real learning only kicks in when you actively connect new information to things you already know</Highlight>.<Cite n={3} /> When you rephrase something in your own words, your brain has to figure out how it relates to what you already understand. You can't reword something unless you actually get it. That connection-building is what turns information from something you heard into something you know.</p>
                  <p>Three simple moves will transform your note-taking:</p>
                </>
              )}
              <ConceptCardGrid
                cards={[
                  { number: 1, term: "Summarise", description: "After reading or hearing a concept, close the book and write one sentence that captures the main idea. If you can't boil it down, you probably don't understand it yet. The constraint forces you to figure out what actually matters." },
                  { number: 2, term: "Give Your Own Example", description: "If you can come up with your own example of a concept, you really get it. You're not just remembering the specific thing you were taught -- you understand the idea behind it." },
                  { number: 3, term: "Connect", description: "When you link new information to something you already know, your brain stores it in more places. That means more ways to find it again later -- like having multiple doors into the same room." },
                ]}
                accentNote="These three moves -- summarise, give an example, connect -- are what make notes actually useful."
              />
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The Cornell System." eyebrow="Step 3" icon={Layers} theme={theme}>
              {essentials ? (
                <>
                  <p>The <strong>Cornell Method</strong> splits your page into three zones. Right column: main notes in your own words. Left column: questions and key terms added within 24 hours. Bottom: a one-sentence summary.</p>
                  <p>Cover the right column and quiz yourself using the left column cues. This turns your notes into a built-in self-testing tool.<Cite n={4} /></p>
                </>
              ) : (
                <>
                  <p>Knowing that better notes exist is one thing. Having a system that makes it easy is another. The <Highlight description="A simple way to split your page into three zones — one for notes during class, one for questions after class, and one for a quick summary. It turns your notes into a built-in study tool." theme={theme}>Cornell Method</Highlight> splits your page into three zones. The main notes area (the right column, about two-thirds of the page) is where you write during class or study — using your own words, not copying. You paraphrase, summarise, and make connections as you go.</p>
                  <p>The real power comes after the session. The <Highlight description="The narrow left column of the page. After class, you go back and write questions and key terms here. Then you can cover the right side and quiz yourself using only the cues — it's a built-in self-test." theme={theme}>cue column</Highlight> (the narrow left column) is filled in within 24 hours. You look over your main notes and turn them into key questions and trigger words. "What are the three types of rock?" "Explain osmosis in your own words." "Why does temperature affect reaction rate?" These cues turn your notes into a self-testing tool. Cover the right column, read the cues, and try to recall the answers. That's <Highlight description="Testing yourself by trying to remember something from memory, instead of just re-reading it. It feels harder, but it's one of the most powerful ways to make information stick." theme={theme}>self-testing</Highlight> built right into your notes.<Cite n={4} /></p>
                  <p>The <Highlight description="The bottom strip of the page. You write the whole page's content in one to three sentences. This forces you to figure out what really matters and gives you a quick way to scan your notes later." theme={theme}>summary section</Highlight> (the bottom of the page) completes the system. Within 24 hours, you write a one-to-three-sentence summary of the entire page. This forces you to boil everything down to its core — another round of real thinking. The Cornell Method isn't just a layout for your page; it's a complete study system that builds self-testing and real thinking into the structure of your notes.</p>
                </>
              )}
              <CornellNoteSimulator />
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="Mapping vs Listing." eyebrow="Step 4" icon={GitBranch} theme={theme}>
              {essentials ? (
                <>
                  <p>Concept maps tend to beat lists when you need to understand how ideas connect.<Cite n={5} /> Put ideas in bubbles and draw arrows between them. This shows the big picture that lists hide.</p>
                  <p>But for step-by-step content like Maths or Chemistry, linear notes work better. Match the shape of your notes to what you are learning. The best note-takers switch between both.</p>
                </>
              ) : (
                <>
                  <p>Even when you're writing notes in your own words, the shape of your notes matters too. A meta-analysis across dozens of studies found that <Highlight description="When you draw out ideas as a map with arrows showing how things connect, you tend to understand the relationships between ideas better than if you just write a plain list." theme={theme}>concept maps tend to outperform plain lists and bullet points</Highlight><Cite n={5} /> when you need to understand how ideas relate to each other. When you write linear notes — numbered lists, bullet points, outlines — you capture things in order. When you draw concept maps — ideas in bubbles connected by arrows — you capture how things actually fit together.</p>
                  <p>Think about studying Biology. A linear note might read: "1. Photosynthesis occurs in chloroplasts. 2. It requires sunlight, water, and CO2. 3. It produces glucose and oxygen." That captures facts in order. A concept map of the same content would put <Highlight description="A diagram where you put ideas in bubbles and draw arrows between them to show how they connect. Unlike lists, maps show you which ideas are central, which are less important, and how they depend on each other." theme={theme}>photosynthesis in the middle</Highlight>, with arrows connecting it to its inputs (sunlight, water, CO2), its outputs (glucose, oxygen), its location (chloroplasts), and its link to cellular respiration. The map shows you the big picture — how everything connects — which the list hides.</p>
                  <p>But mapping isn't always better. For step-by-step content — Maths proofs, Chemistry calculations, historical timelines — <Highlight description="There's no single best format for notes. If the topic is about how ideas connect (like in Biology or Business), use a map. If it's about steps in order (like in Maths or Chemistry), use a list. The best note-takers switch it up depending on what they're studying." theme={theme}>linear notes are often the better choice</Highlight> because the knowledge itself follows a sequence. The key takeaway: match the shape of your notes to the shape of what you're learning. For subjects where ideas connect in webs — Biology, History, Business — mapping shows you relationships that lists miss. For subjects with step-by-step processes — Maths proofs, Chemistry calculations — linear formats keep the logic clear. The best note-takers switch between both depending on what they're studying.</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Building Your System." eyebrow="Step 5" icon={Wrench} theme={theme}>
              {essentials ? (
                <>
                  <p><strong>During study:</strong> Use Cornell format. Write in your own words. Summarise, give examples, connect to what you know.</p>
                  <p><strong>Within 24 hours:</strong> Add cue questions in the left column. Write a summary at the bottom.</p>
                  <p><strong>Before your next session:</strong> Cover the notes column. Test yourself using only the cues. The struggle you feel is your brain getting stronger.</p>
                </>
              ) : (
                <>
                  <p>The best note-taking system pulls everything together — and decades of research confirm one thing: <Highlight description="Notes that are well-organised AND actively reviewed beat everything else. Having neat notes you never look at again doesn't work. Reviewing messy notes doesn't work either. You need both: good structure and regular review." theme={theme}>organised notes plus active review beats everything else</Highlight>.<Cite n={4} /> Not just neat notes. Not just reviewing notes. The combination of good structure plus actually going back and testing yourself is what makes the difference.</p>
                  <p>Here's your three-step system. <Highlight description="Step one: while you're in class or studying, use the Cornell layout with the right column for your main notes. Always use your own words — never copy a sentence word for word. Summarise, give examples, and connect to things you already know." theme={theme}>During study</Highlight>: use the Cornell format. Write in the right column using your own words — never copy a sentence word for word. Use the three moves: summarise in one sentence, come up with your own example, connect to something you already know. For subjects where ideas connect in webs, try switching to concept maps. <Highlight description="Step two: within 24 hours of your study session, go back to your notes and add questions and key terms in the left column. Write a one-to-three-sentence summary at the bottom. This second pass forces your brain to process everything again, which makes it stick much better." theme={theme}>Within 24 hours</Highlight>: go back to your notes. Add cue questions and key terms in the left column. Write your summary at the bottom. This second pass forces your brain to process everything again, which massively strengthens your memory.</p>
                  <p><Highlight description="Step three: before your next study session on that topic, cover the right column and test yourself using only the cue questions. The struggle you feel trying to remember is not failure — it's your brain strengthening its connections. That's where the real learning happens." theme={theme}>Before your next session</Highlight>: cover the main notes column. Read only the cue questions. Try to recall the answers from memory. This is self-testing — and the struggle you feel is not a sign of failure but of your brain getting stronger. Check your answers against the main notes. Any cue you couldn't answer shows you exactly where to focus next. This three-step system — write in your own words, add questions, test yourself — turns every page of notes into a powerful study tool.</p>
                </>
              )}
              <MicroCommitment theme={theme}>
                <p>For your next study session, draw the Cornell template: a vertical line 6cm from the left edge, a horizontal line 5cm from the bottom. Take notes in the right column using only your own words — never copy a sentence verbatim. Within 24 hours, add cue questions in the left column and a one-sentence summary at the bottom. Then close your notes and test yourself using only the cues.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};

export default TheNoteTakingParadoxModule;
