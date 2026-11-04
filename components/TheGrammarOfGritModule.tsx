import { BrandedThoughtReframer } from './learning/BrandedFeatures';
import { moduleFill,moduleText } from './learning/brandTokens';
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import {
HeartCrack,
Mic,
Recycle,
Shield,
Wrench
} from 'lucide-react';
import React,{ useState } from 'react';
import { GRAMMAR_OF_GRIT_REFERENCE_LIST } from '../data/references/grammarOfGrit';
import { useEssentialsMode } from '../hooks/useEssentialsMode';
import { blueTheme } from '../moduleThemes';
import { type ModuleProgress } from '../types';
import { ModuleLayout } from './ModuleLayout';
import { Cite } from './ModuleReferences';
import { ConceptCardGrid,Highlight,MicroCommitment,ReadingSection } from './ModuleShared';

const theme = blueTheme;

// --- INTERACTIVE COMPONENTS ---

const ThoughtReframer = BrandedThoughtReframer;

const ExplanatoryStyleQuiz = () => {
    const [answers, setAnswers] = useState<( 'pessimistic' | 'optimistic' | null)[]>([null, null, null]);
    const score = answers.filter(a => a === 'optimistic').length;

    const handleAnswer = (index: number, type: 'pessimistic' | 'optimistic') => {
      const newAnswers = [...answers];
      newAnswers[index] = type;
      setAnswers(newAnswers);
    };

    const isComplete = answers.every(a => a !== null);

    return <div className="wr-skin" data-wide="ExplanatoryStyleQuiz"><div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: "var(--module-surface)", borderRadius: 18 }}>
        <h4 className="font-serif text-2xl font-semibold text-[var(--module-ink)] dark:text-[var(--module-ink)] text-center">Self-Talk Diagnostic</h4>
        <p className="text-center text-sm text-[var(--module-muted)] dark:text-[var(--module-muted)] mb-8">You fail a test. Which voice is louder in your head?</p>
        <div className="space-y-6">
            <div>
                <p className="text-center font-bold mb-2">"This means I'm stupid." vs "This means my strategy was wrong."</p>
                <div className="grid grid-cols-2 gap-3">
                  <button onClick={() => handleAnswer(0, 'pessimistic')} className="p-4 rounded-xl font-bold text-sm" style={{ backgroundColor: moduleFill(answers[0] === 'pessimistic' ? "var(--module-surface)" : "var(--module-surface)"), border: `2.5px solid ${answers[0] === 'pessimistic' ? "var(--module-line)" : "var(--module-line)"}`, borderRadius: 14, boxShadow: 'none', color: moduleText(answers[0] === 'pessimistic' ? "var(--module-danger-text)" : "var(--module-ink)") }} data-wide-button="true" data-selected={!!(answers[0] === 'pessimistic')} data-tone="coral" aria-pressed={!!(answers[0] === 'pessimistic')}>A</button>
                  <button onClick={() => handleAnswer(0, 'optimistic')} className="p-4 rounded-xl font-bold text-sm" style={{ backgroundColor: moduleFill(answers[0] === 'optimistic' ? "var(--module-success-soft)" : "var(--module-surface)"), border: `2.5px solid ${answers[0] === 'optimistic' ? "var(--module-line)" : "var(--module-line)"}`, borderRadius: 14, boxShadow: 'none', color: moduleText(answers[0] === 'optimistic' ? "var(--module-success-text)" : "var(--module-ink)") }} data-wide-button="true" data-selected={!!(answers[0] === 'optimistic')} data-tone="mint" aria-pressed={!!(answers[0] === 'optimistic')}>B</button>
                </div>
            </div>
             <div>
                <p className="text-center font-bold mb-2">"I'll never get this." vs "I'll try again tomorrow."</p>
                <div className="grid grid-cols-2 gap-3">
                  <button onClick={() => handleAnswer(1, 'pessimistic')} className="p-4 rounded-xl font-bold text-sm" style={{ backgroundColor: moduleFill(answers[1] === 'pessimistic' ? "var(--module-surface)" : "var(--module-surface)"), border: `2.5px solid ${answers[1] === 'pessimistic' ? "var(--module-line)" : "var(--module-line)"}`, borderRadius: 14, boxShadow: 'none', color: moduleText(answers[1] === 'pessimistic' ? "var(--module-danger-text)" : "var(--module-ink)") }} data-wide-button="true" data-selected={!!(answers[1] === 'pessimistic')} data-tone="coral" aria-pressed={!!(answers[1] === 'pessimistic')}>A</button>
                  <button onClick={() => handleAnswer(1, 'optimistic')} className="p-4 rounded-xl font-bold text-sm" style={{ backgroundColor: moduleFill(answers[1] === 'optimistic' ? "var(--module-success-soft)" : "var(--module-surface)"), border: `2.5px solid ${answers[1] === 'optimistic' ? "var(--module-line)" : "var(--module-line)"}`, borderRadius: 14, boxShadow: 'none', color: moduleText(answers[1] === 'optimistic' ? "var(--module-success-text)" : "var(--module-ink)") }} data-wide-button="true" data-selected={!!(answers[1] === 'optimistic')} data-tone="mint" aria-pressed={!!(answers[1] === 'optimistic')}>B</button>
                </div>
            </div>
             <div>
                <p className="text-center font-bold mb-2">"This ruins everything." vs "This is just one subject."</p>
                <div className="grid grid-cols-2 gap-3">
                  <button onClick={() => handleAnswer(2, 'pessimistic')} className="p-4 rounded-xl font-bold text-sm" style={{ backgroundColor: moduleFill(answers[2] === 'pessimistic' ? "var(--module-surface)" : "var(--module-surface)"), border: `2.5px solid ${answers[2] === 'pessimistic' ? "var(--module-line)" : "var(--module-line)"}`, borderRadius: 14, boxShadow: 'none', color: moduleText(answers[2] === 'pessimistic' ? "var(--module-danger-text)" : "var(--module-ink)") }} data-wide-button="true" data-selected={!!(answers[2] === 'pessimistic')} data-tone="coral" aria-pressed={!!(answers[2] === 'pessimistic')}>A</button>
                  <button onClick={() => handleAnswer(2, 'optimistic')} className="p-4 rounded-xl font-bold text-sm" style={{ backgroundColor: moduleFill(answers[2] === 'optimistic' ? "var(--module-success-soft)" : "var(--module-surface)"), border: `2.5px solid ${answers[2] === 'optimistic' ? "var(--module-line)" : "var(--module-line)"}`, borderRadius: 14, boxShadow: 'none', color: moduleText(answers[2] === 'optimistic' ? "var(--module-success-text)" : "var(--module-ink)") }} data-wide-button="true" data-selected={!!(answers[2] === 'optimistic')} data-tone="mint" aria-pressed={!!(answers[2] === 'optimistic')}>B</button>
                </div>
            </div>
        </div>
         {isComplete && <p className="text-center mt-4 text-sm font-bold">{score > 1 ? <span className="text-[var(--module-success-text)]">Your explanatory style is optimistic and builds resilience.</span> : <span className="text-[var(--module-danger-text)]">Your explanatory style is pessimistic and may be eroding your resilience.</span>}</p>}
      </div></div>;
};

// --- MODULE COMPONENT ---
const TheGrammarOfGritModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const essentials = useEssentialsMode();
  const sections = [
    { id: 'internal-narrator', title: 'Your Internal Narrator', eyebrow: '01 // The Source Code', icon: Mic },
    { id: 'three-ps', title: 'The 3 Ps of Failure', eyebrow: '02 // Personal, Pervasive, Permanent', icon: HeartCrack },
    { id: 'rewrite-protocol', title: 'The Re-Write Protocol', eyebrow: '03 // From Fragile to Agile', icon: Recycle },
    { id: 'self-compassion', title: 'The Role of Self-Compassion', eyebrow: '04 // The Antidote to Shame', icon: Shield },
    { id: 'blueprint', title: 'Your Resilience Blueprint', eyebrow: '05 // The Action Plan', icon: Wrench },
  ];

  return (
    <ModuleLayout
      moduleNumber="05"
      moduleTitle="The Grammar of Grit"
      moduleSubtitle="The Language of Resilience"
      moduleDescription="The way you talk to yourself after a setback matters more than you think. This module shows you how to spot the patterns and change them."
      theme={theme}
      sections={sections}
      references={GRAMMAR_OF_GRIT_REFERENCE_LIST}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Rewrite Your Script"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="Your Internal Narrator." eyebrow="Step 1" icon={Mic} theme={theme}>
              {essentials ? (
                <p>When something goes wrong, the way you talk to yourself matters. Your <strong>explanatory style</strong> -- how you explain setbacks to yourself -- shapes whether you bounce back or shut down.<Cite n={1} /> You can learn to change it.</p>
              ) : (
                <p>When you face a setback, who is the narrator in your head? The language they use is not just commentary; it's the source code for your resilience. Your <Highlight description="The way you automatically explain things to yourself when something goes wrong. It shapes how you handle setbacks, how motivated you feel, and even how you feel physically." theme={theme}>Explanatory Style</Highlight> — basically, the 'grammar' of your self-talk — shapes whether you bounce back or break down.<Cite n={1} /></p>
              )}
              <ExplanatoryStyleQuiz />
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="The 3 Ps of Failure." eyebrow="Step 2" icon={HeartCrack} theme={theme}>
              {essentials ? (
                <>
                  <p>Pessimistic self-talk has three patterns. <strong>Personal:</strong> "I am stupid." <strong>Pervasive:</strong> "I ruin everything." <strong>Permanent:</strong> "It will always be this way."<Cite n={1} /> These train your brain to give up.</p>
                  <p>Resilient self-talk flips all three. "The strategy was wrong." "Just this one area." "I will do better next time." You focus on what you can control.</p>
                </>
              ) : (
                <>
                  <p>A pessimistic explanatory style kills your grit because it filters every failure through three destructive lenses: <strong>Personal</strong> ("It's my fault; I'm stupid"), <strong>Pervasive</strong> ("I ruin everything I touch"), and <strong>Permanent</strong> ("It's always going to be this way").<Cite n={1} /> This isn't just negative thinking — it's a pattern that trains your brain to give up before you even try.</p>
                  <p>An optimistic, resilient style does the opposite. It sees failure as <strong>External/Specific</strong> ("The strategy was wrong"), <strong>Specific</strong> ("I messed up this one thing"), and <strong>Temporary</strong> ("I'll do better next time"). This isn't about lying to yourself; it's about a disciplined, strategic choice to focus on what you can control.</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The Re-Write Protocol." eyebrow="Step 3" icon={Recycle} theme={theme}>
              {essentials ? (
                <p>You can train a more optimistic style. Catch yourself using one of the 3 Ps, then rewrite it. "I am useless at Maths" becomes "My study method for trigonometry is not working yet." You are making it specific and temporary instead of personal and permanent.</p>
              ) : (
                <p>You can train your brain to adopt a more optimistic style. This is called <Highlight description="A technique where you catch your negative automatic thoughts, question whether they're actually true, and replace them with something more realistic." theme={theme}>Cognitive Restructuring</Highlight> — a core, well-evidenced technique from cognitive behavioural therapy.<Cite n={2} /> When you catch yourself using one of the 3 Ps, you consciously "re-write" the script. For example, "I'm useless at Maths" (Personal, Permanent) becomes "My study method for trigonometry isn't working yet" (Specific, Temporary).</p>
              )}
              <ThoughtReframer />
              <MicroCommitment theme={theme}><p>Take one negative thought you had about school this week. Write it down. Now, try to rewrite it, changing one of the '3 Ps'. Turn a 'Personal' blame into a 'Specific' strategy problem.</p></MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="The Role of Self-Compassion." eyebrow="Step 4" icon={Shield} theme={theme}>
                {essentials ? (
                  <p>A harsh inner critic creates shame, which kills motivation. <strong>Self-compassion</strong> is the fix.<Cite n={3} /> Treat yourself like a friend. Remember everyone messes up. Notice the feeling without letting it consume you. "I failed" is not "I am a failure."</p>
                ) : (
                  <>
                    <p>A harsh inner critic doesn't build resilience; it creates shame, which kills your motivation. <Highlight description="Treating yourself the way you'd treat a friend who's going through a tough time. It's the opposite of the shame spiral that can follow failure." theme={theme}>Self-compassion</Highlight> is the antidote.<Cite n={3} /> It lets you acknowledge a failure without letting it define you. It's the difference between "I failed" and "I am a failure."</p>
                    <p>It has three parts:</p>
                  </>
                )}
                <ConceptCardGrid
                  cards={[
                    { number: 1, term: "Self-Kindness", description: "Treat yourself like you'd treat a mate." },
                    { number: 2, term: "Common Humanity", description: "Remember that everyone messes up." },
                    { number: 3, term: "Mindfulness", description: "Acknowledge the feeling without letting it consume you." },
                  ]}
                />
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="Your Resilience Blueprint." eyebrow="Step 5" icon={Wrench} theme={theme}>
              {essentials ? (
                <p>You now have the tools. Catch the 3 Ps in your self-talk. Rewrite with self-compassion. Build resilience one sentence at a time. Start by noticing your first thought after a mistake.</p>
              ) : (
                <p>You now have the tools to edit your own internal monologue. By catching the 3 Ps in your self-talk and rewriting the script with a bit of self-compassion, you can build a more resilient mindset — one sentence at a time.</p>
              )}
              <MicroCommitment theme={theme}>
                <p>The next time you make a small mistake, just notice your first thought. Don't judge it, just label it. Was it Personal? Pervasive? Permanent? This act of noticing is the first step to taking control.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default TheGrammarOfGritModule;
