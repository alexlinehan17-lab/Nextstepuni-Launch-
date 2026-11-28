/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import {
Code,
Flag,
Recycle,
SlidersHorizontal,UserX
} from 'lucide-react';
import React,{ useEffect,useState } from 'react';
import { AGENCY_ARCHITECTURE_REFERENCE_LIST } from '../data/references/agencyArchitecture';
import { useEssentialsMode } from '../hooks/useEssentialsMode';
import { useModuleResponses } from '../hooks/useModuleResponses';
import { amberTheme } from '../moduleThemes';
import { type ModuleProgress } from '../types';
import { ModuleLayout } from './ModuleLayout';
import { Cite } from './ModuleReferences';
import { Highlight,MicroCommitment,PersonalStory,ReadingSection } from './ModuleShared';
import { MotionDiv } from './Motion';
import { AnswerGroup,ExercisePart,ExerciseRange,ExerciseSheet,RevealCard } from './learning/Exercise';
import { ChoiceTile } from './ui/Choice';

const theme = amberTheme;

// --- INTERACTIVE COMPONENTS ---

const AttributionMapper = ({ savedValues, onSave }: { savedValues?: { locus: number; stability: number; controllability: number }; onSave?: (values: { locus: number; stability: number; controllability: number }) => void }) => {
  const [locus, setLocus] = useState(savedValues?.locus ?? 50);
  const [stability, setStability] = useState(savedValues?.stability ?? 50);
  const [controllability, setControllability] = useState(savedValues?.controllability ?? 50);

  useEffect(() => {
    if (savedValues) {
      setLocus(savedValues.locus);
      setStability(savedValues.stability);
      setControllability(savedValues.controllability);
    }
  }, [savedValues]);

  // Internal (high locus) + Unstable (low stability) + Controllable (low controllability) = growth
  // Optimism score: locus contributes positively when high, stability when low, controllability when low
  const optimismScore = (locus / 100) + (1 - stability / 100) + (1 - controllability / 100); // 0–3

  const getLabel = (): { text: string; color: string } => {
    if (optimismScore >= 2.2) return { text: 'Growth Attribution', color: 'emerald' };
    if (optimismScore <= 1.0) return { text: 'Helplessness Risk', color: 'rose' };
    return { text: 'Mixed', color: 'amber' };
  };

  const getExplanation = (): string => {
    const isInternal = locus >= 55;
    const isStable = stability >= 55;
    const isControllable = controllability <= 45;

    if (isInternal && !isStable && isControllable) {
      return "This is the ideal growth attribution. You take ownership, see it as temporary, and believe you can change it. This pattern fuels motivation and resilience.";
    }
    if (!isInternal && isStable && !isControllable) {
      return "You see this as someone else's fault, permanent, and out of your control. This is the classic pattern behind learned helplessness — it kills motivation because effort feels pointless.";
    }
    if (isInternal && isStable && !isControllable) {
      return "You see this as permanent and out of your control — this is the pattern that leads to learned helplessness. Try reframing: what specific strategy could you change?";
    }
    if (!isInternal && !isStable && isControllable) {
      return "You see this as external and temporary, but believe you can act on it. That's a resilient stance, though taking more ownership could help you grow even faster.";
    }
    if (isInternal && isStable && isControllable) {
      return "You take ownership and feel you can act, but seeing it as permanent may weigh you down. Try reframing: is this really forever, or just this situation?";
    }
    if (!isInternal && isStable && isControllable) {
      return "You see the cause as external and permanent but feel you can still act. Consider whether more ownership of the cause would give you a clearer path forward.";
    }
    if (!isInternal && !isStable && !isControllable) {
      return "You see this as external, temporary, and beyond your control. That can feel comforting, but look for the part you can influence — even small actions build agency.";
    }
    if (isInternal && !isStable && !isControllable) {
      return "You own the cause and see it as temporary, but feel powerless to change it. The missing piece is controllability — what one small lever could you pull?";
    }
    // Neutral / middle ground
    return "Your attribution sits in the middle ground. Try pushing the sliders to the extremes to see how different stories about failure lead to very different emotional outcomes.";
  };

  const label = getLabel();

  const handleSliderChange = (dimension: 'locus' | 'stability' | 'controllability', value: number) => {
    const setters = { locus: setLocus, stability: setStability, controllability: setControllability };
    setters[dimension](value);
    const next = { locus, stability, controllability, [dimension]: value };
    onSave?.(next);
  };

  const sliders: { label: string; leftLabel: string; rightLabel: string; leftExample: string; rightExample: string; value: number; dimension: 'locus' | 'stability' | 'controllability' }[] = [
    {
      label: 'Locus',
      leftLabel: 'External',
      rightLabel: 'Internal',
      leftExample: '"The teacher marked unfairly"',
      rightExample: '"I didn\'t prepare well"',
      value: locus,
      dimension: 'locus',
    },
    {
      label: 'Stability',
      leftLabel: 'Unstable',
      rightLabel: 'Stable',
      leftExample: '"I had an off day"',
      rightExample: '"I\'m always like this"',
      value: stability,
      dimension: 'stability',
    },
    {
      label: 'Controllability',
      leftLabel: 'Controllable',
      rightLabel: 'Uncontrollable',
      leftExample: '"I can change my approach"',
      rightExample: '"There\'s nothing I can do"',
      value: controllability,
      dimension: 'controllability',
    },
  ];

  return (
    <ExercisePart title="Attribution Mapper" sub="Think of a recent setback or bad result. Map how you interpreted it:">
      <div className="ex-sliders">
        {sliders.map((s) => (
          <div key={s.label} className="ex-slider">
            <p className="ex-slider-name">{s.label}</p>
            <ExerciseRange
              min={0}
              max={100}
              value={s.value}
              onChange={(e) => handleSliderChange(s.dimension, Number(e.target.value))}
              aria-label={s.label}
            />
            <div className="ex-slider-ends">
              <span>{s.leftLabel}<small>{s.leftExample}</small></span>
              <span>{s.rightLabel}<small>{s.rightExample}</small></span>
            </div>
          </div>
        ))}
      </div>

      <MotionDiv
        key={label.text}
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.35 }}
        className="ex-result"
      >
        <p className="ex-result-name">{label.text}</p>
        <p className="ex-sub">{getExplanation()}</p>
      </MotionDiv>
    </ExercisePart>
  );
};

const AttributionSorter = ({ savedChoices, onSave }: { savedChoices?: { [key: string]: boolean }; onSave?: (choices: { [key: string]: boolean }) => void }) => {
    const reasons = [
        { text: "I didn't use the right study method.", type: 'internal', control: true },
        { text: "I'm just naturally bad at this subject.", type: 'internal', control: false },
        { text: "The test was unfairly hard.", type: 'external', control: false },
        { text: "I didn't put in enough focused effort.", type: 'internal', control: true },
    ];
    const [choice, setChoice] = useState<{ [key: string]: boolean }>(savedChoices || {});

    useEffect(() => {
      if (savedChoices) setChoice(savedChoices);
    }, [savedChoices]);

    return <ExercisePart title="Control Panel" sub="Scenario: You fail a test. Which of these reasons are actually within your control?">
            <AnswerGroup kind="several" count>
                {reasons.map(reason => (
                    <ChoiceTile
                        key={reason.text}
                        kind="several"
                        chosen={!!choice[reason.text]}
                        label={reason.text}
                        note={choice[reason.text] ? (reason.control ? '(CONTROLLABLE)' : '(UNCONTROLLABLE)') : undefined}
                        noteTone={reason.control ? 'ok' : 'plain'}
                        onClick={() => { const next = {...choice, [reason.text]: !choice[reason.text]}; setChoice(next); onSave?.(next); }}
                    />
                ))}
            </AnswerGroup>
        </ExercisePart>;
};

/** A thought in its quotation marks, as the drill has always shown it. */
const quoted = (thought: string) => <>"{thought}"</>;

const AttributionReframeDrill = () => {
  const examples = [
    { id: 1, maladaptive: "I failed the test because I am stupid.", adaptive: "I failed the test because my study strategy for this topic was ineffective." },
    { id: 2, maladaptive: "I'm just naturally bad at Maths.", adaptive: "I haven't found an effective way to learn Maths yet." },
    { id: 3, maladaptive: "I'll never be good enough to get a top grade.", adaptive: "Getting a top grade is a difficult goal, so I will need to break it down into smaller, manageable steps." },
  ];

  const [flipped, setFlipped] = useState<number[]>([]);

  const handleFlip = (id: number) => {
    setFlipped(
      flipped.includes(id)
        ? flipped.filter(fId => fId !== id)
        : [...flipped, id]
    );
  };

  return (
    <ExerciseSheet title="Attribution Reframe Drill" sub="Click on a self-defeating thought to transform it into an empowering one." name="AttributionReframeDrill">
      <div className="ex-cards">
        {examples.map((ex) => (
          <RevealCard
            key={ex.id}
            revealed={flipped.includes(ex.id)}
            onPress={() => handleFlip(ex.id)}
            before={quoted(ex.maladaptive)}
            after={quoted(ex.adaptive)}
            hint="Tap to reframe"
            done="Reframed"
          />
        ))}
      </div>
    </ExerciseSheet>
  );
};

// --- MODULE COMPONENT ---
const AgencyArchitectureModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const essentials = useEssentialsMode();
  const { responses, saveResponse, isLoaded: _isLoaded } = useModuleResponses('controlling-the-controllables');

  const sections = [
    { id: 'attribution-theory', title: 'The Story of Failure', eyebrow: '01 // The Source Code', icon: Code },
    { id: 'three-dimensions', title: 'The Three Dimensions', eyebrow: '02 // The Control Panel', icon: SlidersHorizontal },
    { id: 'pessimistic-script', title: 'The Pessimist\'s Script', eyebrow: '03 // Learned Helplessness', icon: UserX },
    { id: 'agency-rewrite', title: 'The Agency Re-Write', eyebrow: '04 // Retraining', icon: Recycle },
    { id: 'blueprint', title: 'Your New OS', eyebrow: '05 // The Blueprint', icon: Flag },
  ];

  return (
    <ModuleLayout
      moduleNumber="07"
      moduleTitle="Controlling the Controllables"
      moduleSubtitle="The Attribution Retraining Guide"
      moduleDescription="Learn to distinguish between what you can and cannot control, and rewire your brain to see failure as feedback, not a final verdict."
      theme={theme}
      sections={sections}
      references={AGENCY_ARCHITECTURE_REFERENCE_LIST}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Take the Controls"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Story of Failure." eyebrow="Step 1" icon={Code} theme={theme}>
              {essentials ? (
                <>
                  <p>When something goes wrong, your brain writes a story to explain it. That story is called an <Highlight description="The story your brain tells you about why something happened. The kind of story you default to has a huge effect on how motivated and resilient you feel." theme={theme}>attribution</Highlight>.<Cite n={1} /> It controls your motivation.</p>
                  <p>Here's what to do: focus on what you can control. Split everything into two buckets. Things you control (your effort, your strategy). Things you don't (other people, luck). Pour your energy into the first bucket. This is the <Highlight description="A simple but powerful idea: split everything in your life into two buckets — stuff you can actually control (your effort, your attitude) and stuff you can't (other people, external events). Then pour your energy into the first bucket." theme={theme}>Dichotomy of Control</Highlight>.</p>
                </>
              ) : (
                <>
                  <p>When something bad happens, your brain instantly writes a story to explain why. This story is called an <Highlight description="The story your brain tells you about why something happened. The kind of story you default to has a huge effect on how motivated and resilient you feel." theme={theme}>attribution</Highlight>. It's the "source code" for your motivation. A resilient mindset isn't about being positive; it's about telling yourself the right kind of story after a failure.</p>
                  <p>The core principle is to focus on what you can control. This idea is called the <Highlight description="A simple but powerful idea: split everything in your life into two buckets — stuff you can actually control (your effort, your attitude) and stuff you can't (other people, external events). Then pour your energy into the first bucket." theme={theme}>Dichotomy of Control</Highlight>. Research on how students explain their results points the same way: those who attribute outcomes to causes they can act on tend to be more resilient and motivated.<Cite n={1} /></p>
                  <PersonalStory name="Alex" role="Founder, NextStepUni" junior={{ children: (
                    <p>After I failed my Junior Cert, I had a long list of things I couldn't control. Where I grew up, the crowds I'd been in, the things that had happened. Then I made a decision to stop looking at that list. I focused on the one thing I could control: how I studied. I read up on how learning actually works, I built a system, and I worked it every day. That was the only thing I changed — and it changed everything.</p>
                  ) }}>
                    <p>After I failed my Junior Cert, I had a long list of things I couldn't control. Where I grew up, the crowds I'd been in, the things that had happened. In 4th year I made a decision to stop looking at that list. I focused on the one thing I could control: how I studied. I read the academic papers, I built a system, and I worked it every day. That was the only variable I changed — and it changed everything.</p>
                  </PersonalStory>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="The Three Dimensions." eyebrow="Step 2" icon={SlidersHorizontal} theme={theme}>
              <p>{essentials ? 'Your failure story has three parts. Each one changes how you feel.' : 'Every story you tell yourself about a failure can be broken down along three dimensions.'}<Cite n={1} /></p>
              <ol className="ex-nums">
                <li>
                  <span className="ex-num">1</span>
                  <div className="ex-num-copy">
                    <p className="ex-num-title">Locus of Control</p>
                    <p className="ex-num-sub">Is the cause <Highlight description="You're saying the cause is something about you — like how much effort you put in or how you prepared." theme={theme}>Internal</Highlight> (about you) or <Highlight description="You're saying the cause is something outside of you — like the teacher, the exam, or bad luck." theme={theme}>External</Highlight> (about the world)?</p>
                  </div>
                </li>
                <li>
                  <span className="ex-num">2</span>
                  <div className="ex-num-copy">
                    <p className="ex-num-title">Stability</p>
                    <p className="ex-num-sub">Is the cause <Highlight description="You're saying this is permanent — it's always been this way and always will be. Like thinking 'I'm just not a maths person.'" theme={theme}>Stable</Highlight> (permanent) or <Highlight description="You're saying this is temporary — it happened this time but it's not a forever thing. Like thinking 'I didn't study enough for this specific test.'" theme={theme}>Unstable</Highlight> (temporary)?</p>
                  </div>
                </li>
                <li>
                  <span className="ex-num">3</span>
                  <div className="ex-num-copy">
                    <p className="ex-num-title">Controllability</p>
                    <p className="ex-num-sub">Is the cause something you can change, or not?</p>
                  </div>
                </li>
              </ol>
              <ExerciseSheet name="AttributionMapper">
                <AttributionMapper savedValues={responses['attribution-mapper']} onSave={(v) => saveResponse('attribution-mapper', v)} />
                <AttributionSorter savedChoices={responses['attribution-sorter']} onSave={(c) => saveResponse('attribution-sorter', c)} />
              </ExerciseSheet>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The Pessimist's Script." eyebrow="Step 3" icon={UserX} theme={theme}>
              {essentials ? (
                <>
                  <p>The most dangerous story says failure is <strong>Internal, Stable, and Uncontrollable</strong>. "I failed because I'm stupid." That leads to <Highlight description="When you've told yourself 'there's no point' so many times that you actually start to believe it. You stop trying — not because you're lazy, but because your brain has convinced itself that nothing you do will make a difference." theme={theme}>Learned Helplessness</Highlight>.<Cite n={2} /></p>
                  <p>You stop trying. Not because you're lazy. Your brain concluded that effort is pointless. This pattern kills motivation fast.</p>
                </>
              ) : (
                <>
                  <p>The most dangerous story your brain can write is the "pessimistic explanatory style." It attributes failure to causes that are <strong>Internal, Stable, and Uncontrollable</strong>. For example: "I failed the test (bad event) because I am stupid (Internal, Stable, Uncontrollable)."</p>
                  <p>This kind of thinking is toxic. It leads straight to <Highlight description="When you've told yourself 'there's no point' so many times that you actually start to believe it. You stop trying — not because you're lazy, but because your brain has convinced itself that nothing you do will make a difference." theme={theme}>Learned Helplessness</Highlight>.<Cite n={2} /> If you believe the cause of your failure is a permanent, unchangeable part of who you are, then there's no point in trying again. Your motivation collapses, not because you're lazy, but because your brain has logically concluded that effort is futile.</p>
                </>
              )}
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="The Agency Re-Write." eyebrow="Step 4" icon={Recycle} theme={theme}>
              {essentials ? (
                <>
                  <p>You can rewrite this script. This is <Highlight description="Basically, training yourself to change the story you tell about why things went wrong. Instead of jumping to 'I'm useless,' you learn to say 'my approach didn't work — what can I try differently?'" theme={theme}>Attributional Retraining</Highlight>.<Cite n={3} /> Shift your explanations to <strong>Internal, Unstable, and Controllable</strong>.</p>
                  <p>"I'm stupid" becomes "my strategy didn't work." You still own it. But now you can change it. That turns a dead end into a next step.</p>
                </>
              ) : (
                <>
                  <p>The good news is that you can consciously re-write this script. This is called <Highlight description="Basically, training yourself to change the story you tell about why things went wrong. Instead of jumping to 'I'm useless,' you learn to say 'my approach didn't work — what can I try differently?'" theme={theme}>Attributional Retraining</Highlight>. It genuinely works — in studies, students taught to re-attribute setbacks to changeable causes improved their grades.<Cite n={3} /></p>
                  <p>The goal is to shift your explanations towards causes that are <strong>Internal, Unstable, and Controllable</strong>. "I failed the test because I am stupid" becomes "I failed the test because my <em>strategy</em> was ineffective." The cause is still internal (giving you agency), but it's unstable (you can change your strategy) and controllable. This isn't just wordplay; it's a fundamental shift in your brain's operating system that turns a dead end into a learning opportunity.</p>
                </>
              )}
              <AttributionReframeDrill />
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="Your New OS." eyebrow="Step 5" icon={Flag} theme={theme}>
              <p>{essentials ? 'Each time you rewrite, you install a new default. You start seeing setbacks as data, not verdicts. That is agency.' : 'By practicing this "re-write," you are installing a new default operating system in your brain. You are training yourself to see setbacks not as verdicts, but as data points. This is the foundation of a Growth Mindset and the core of what it means to have agency over your own academic life.'}</p>
              <MicroCommitment theme={theme}>
                <p>The next time you face a small failure—any small failure—consciously run the 3D analysis. Ask yourself: "What story am I telling myself about why this happened?" Is it Internal/External? Stable/Unstable? Controllable/Uncontrollable? This act of noticing is the first step to rewriting the script.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default AgencyArchitectureModule;
