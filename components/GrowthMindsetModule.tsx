/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import { AnimatePresence,motion } from 'framer-motion';
import {
Activity,
BrainCircuit,
Cpu,
MessageSquareQuote,
RotateCcw,Zap
} from 'lucide-react';
import React,{ useEffect,useId,useState } from 'react';
import { GROWTH_MINDSET_REFERENCE_LIST } from '../data/references/growthMindset';
import { COLORS } from '../design/tokens';
import { useEssentialsMode } from '../hooks/useEssentialsMode';
import { useModuleResponses } from '../hooks/useModuleResponses';
import { amberTheme } from '../moduleThemes';
import { type ModuleProgress } from '../types';
import { ModuleLayout } from './ModuleLayout';
import { Cite } from './ModuleReferences';
import { Highlight,MicroCommitment,PersonalStory,ReadingSection } from './ModuleShared';
import { MotionDiv } from './Motion';
import { AnswerGroup,AnswerLine,ExerciseLabel,ExercisePart,ExerciseSheet,RevealCard } from './learning/Exercise';
import { Button,TextButton } from './ui/Button';
import { ChoiceTile } from './ui/Choice';
import { AreaField,Field } from './ui/Field';

const theme = amberTheme;

// --- INTERACTIVE COMPONENTS ---

const MindsetDiagnostic = ({ savedAnswers, onSaveAnswers }: { savedAnswers?: ('fixed' | 'growth' | null)[]; onSaveAnswers?: (answers: ('fixed' | 'growth' | null)[]) => void }) => {
  const [answers, setAnswers] = useState<( 'fixed' | 'growth' | null)[]>(savedAnswers || [null, null, null]);
  const score = answers.filter(a => a === 'growth').length;

  useEffect(() => {
    if (savedAnswers) setAnswers(savedAnswers);
  }, [savedAnswers]);

  const handleAnswer = (index: number, type: 'fixed' | 'growth') => {
    const newAnswers = [...answers];
    newAnswers[index] = type;
    setAnswers(newAnswers);
    onSaveAnswers?.(newAnswers);
  };

  const isComplete = answers.every(a => a !== null);

  return <ExerciseSheet title="Mindset Diagnostic" sub="Which thought sounds more like you in a tough situation?" name="MindsetDiagnostic">
      <div className="ex-questions">
        {/* Question 1 */}
        <AnswerGroup kind="one" legend="When I fail at something..." columns={2}>
            <ChoiceTile tile chosen={answers[0] === 'fixed'} onClick={() => handleAnswer(0, 'fixed')} label="A) I feel like I'm a failure." />
            <ChoiceTile tile chosen={answers[0] === 'growth'} onClick={() => handleAnswer(0, 'growth')} label="B) I feel like I need to try a new strategy." />
        </AnswerGroup>
        {/* Question 2 */}
        <AnswerGroup kind="one" legend="If a subject is hard for me..." columns={2}>
            <ChoiceTile tile chosen={answers[1] === 'fixed'} onClick={() => handleAnswer(1, 'fixed')} label="A) It means I'm probably not smart enough for it." />
            <ChoiceTile tile chosen={answers[1] === 'growth'} onClick={() => handleAnswer(1, 'growth')} label="B) It means I have a great opportunity to learn." />
        </AnswerGroup>
        {/* Question 3 */}
        <AnswerGroup kind="one" legend="I believe my intelligence is something..." columns={2}>
            <ChoiceTile tile chosen={answers[2] === 'fixed'} onClick={() => handleAnswer(2, 'fixed')} label="A) That I can't change very much." />
            <ChoiceTile tile chosen={answers[2] === 'growth'} onClick={() => handleAnswer(2, 'growth')} label="B) That I can grow with effort." />
        </AnswerGroup>
      </div>
      <AnimatePresence>
      {isComplete && (
        <motion.div initial={{opacity:0, y:10}} animate={{opacity:1, y:0}}>
          <AnswerLine tone={score === 3 ? 'ok' : 'note'}>
            {score === 3 && <span>Result: You're operating with a strong Growth Mindset OS!</span>}
            {score === 2 && <span>Result: You're leaning towards Growth, with some Fixed-Mindset code still running.</span>}
            {score < 2 && <span>Result: Your system is currently running a Fixed-Mindset OS. Time for an upgrade!</span>}
          </AnswerLine>
        </motion.div>
      )}
      </AnimatePresence>
    </ExerciseSheet>;
};

const NeuroplasticityVisualizer = () => {
  const [connections, setConnections] = useState(0);
  const milestone = connections === 1 ? 'First connection forming.' : connections === 3 ? 'Pathway strengthening — repetition is working.' : connections === 5 ? 'Strong neural pathway established.' : null;

  return (
    <ExerciseSheet label="Neuroscience Simulation" title="The Brain Rewiring Simulator" sub="Every time you practice, you strengthen the physical connections in your brain." name="NeuroplasticityVisualizer">
      {/* The drawing, on the sheet under its label (no box of its own) */}
      <div className="ex-figure">
        <ExerciseLabel>Neural Pathway</ExerciseLabel>

        <svg width="250" height="100" viewBox="0 0 250 100" className="ex-figure-art">
          {/* Base placeholder connection */}
          <path d="M 70 50 Q 125 50 180 50" fill="none" stroke="var(--ink-muted)" strokeWidth="1" opacity="0.5" />

          {/* Connection arcs */}
          <AnimatePresence>
            {connections > 0 && Array.from({length: connections}).map((_, i) => {
              const age = connections - 1 - i;
              const opacity = Math.max(0.12, 0.9 - age * 0.12);
              const sw = Math.max(1.0, 2.5 - age * 0.3);
              return (
                <motion.path
                  key={i}
                  d={`M 70 50 Q 125 ${50 + (i - (connections-1)/2) * 15} 180 50`}
                  fill="none"
                  stroke={COLORS.accent}
                  initial={{ pathLength: 0, opacity: 0, strokeWidth: sw }}
                  animate={{ pathLength: 1, opacity, strokeWidth: sw }}
                  transition={{ duration: 0.5 }}
                />
              );
            })}
          </AnimatePresence>

          {/* Neuron A */}
          <circle cx="50" cy="50" r="20" fill={COLORS.accent} stroke={COLORS.accentDark} strokeWidth="2" />
          <circle cx="50" cy="50" r="8" fill="rgba(255,255,255,0.25)" />
          {/* Neuron B */}
          <circle cx="200" cy="50" r="20" fill={COLORS.accent} stroke={COLORS.accentDark} strokeWidth="2" />
          <circle cx="200" cy="50" r="8" fill="rgba(255,255,255,0.25)" />

          {/* Node labels */}
          <text x="50" y="82" textAnchor="middle" fontSize="11" fill="var(--ink-muted)" style={{ fontFamily: 'var(--font-ui)' }}>Neuron A</text>
          <text x="200" y="82" textAnchor="middle" fontSize="11" fill="var(--ink-muted)" style={{ fontFamily: 'var(--font-ui)' }}>Neuron B</text>
        </svg>

        {/* Connection count */}
        <p className="ex-figure-count">{connections} connection{connections !== 1 ? 's' : ''} formed</p>
      </div>

      {/* Milestone: a line in ink (the tick once the pathway is established) */}
      {milestone && (
        <motion.div
          key={milestone}
          initial={{ opacity: 0, y: 6 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <AnswerLine tone={connections === 5 ? 'ok' : 'note'}>{milestone}</AnswerLine>
        </motion.div>
      )}

      {/* Buttons */}
      <div className="ex-actions">
        <Button onClick={() => setConnections(c => Math.min(c + 1, 5))}>
          Practice a Skill
        </Button>
        <TextButton tone="quiet" onClick={() => setConnections(0)}>
          Reset
        </TextButton>
      </div>
    </ExerciseSheet>
  );
}

const ReframeChallenge = ({ savedText, onSave }: { savedText?: string; onSave?: (text: string) => void }) => {
    const [reframe, setReframe] = useState(savedText || '');
    const containsYet = reframe.toLowerCase().includes('yet');

    useEffect(() => {
      if (savedText !== undefined && savedText !== reframe) setReframe(savedText);
    }, [savedText]);

    return(
        <ExerciseSheet label="Growth Mindset Activity" title={'The "Yet" Reframe Challenge'} sub={'Upgrade this fixed thought into a growth mindset statement using the power of "yet".'} name="ReframeChallenge">
            {/* The fixed thought: words you read, so on the sheet under their label, not in a box */}
            <div className="ex-thought">
                <ExerciseLabel>Fixed Mindset Thought</ExerciseLabel>
                <p className="ex-thought-words">I'm just not a maths person.</p>
            </div>

            {/* Transformation connector */}
            <div className="ex-connector">
                <i aria-hidden="true" />
                <span className="ex-label">ADD "YET"</span>
                <i aria-hidden="true" />
                <svg width="16" height="10" viewBox="0 0 16 10" fill="none" aria-hidden="true">
                    <path d="M1 1L8 8L15 1" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
            </div>

            {/* Rewrite area: the field and the line that answers it */}
            <AreaField
                label="Your Reframe"
                value={reframe}
                onChange={(e) => setReframe(e.target.value)}
                onBlur={() => onSave?.(reframe)}
                placeholder="Rewrite this using the word 'yet'..."
            />

            <AnimatePresence>
                {containsYet && (
                    <motion.div initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }}>
                        <AnswerLine><b>Reframe complete.</b> You've opened up the possibility of future growth.</AnswerLine>
                    </motion.div>
                )}
            </AnimatePresence>
        </ExerciseSheet>
    );
};

const feedbackPairs = [
  {
    verdict: "This essay is poorly written.",
    data: "Your argument structure needs clearer topic sentences and supporting evidence in each paragraph.",
    shift: "Shift: vague verdict \u2192 specific, actionable data",
  },
  {
    verdict: "You're just not a maths person.",
    data: "Your current approach to maths isn't working yet. Let's identify which specific steps are causing confusion.",
    shift: "Shift: identity label \u2192 strategy problem",
  },
  {
    verdict: "This is careless work.",
    data: "There are 4 calculation errors here. A final check-through step would catch these.",
    shift: "Shift: character judgment \u2192 countable, fixable issue",
  },
  {
    verdict: "You should know this by now.",
    data: "This concept hasn't stuck yet. Try explaining it to someone else to find where your understanding breaks down.",
    shift: "Shift: time-based shame \u2192 retrieval practice suggestion",
  },
  {
    verdict: "Disappointing result.",
    data: "You scored 52%. The areas to focus on are Q3 and Q5 \u2014 those are the highest-value gaps to close.",
    shift: "Shift: emotional verdict \u2192 strategic data",
  },
  {
    verdict: "You need to try harder.",
    data: "Your effort needs to be more targeted. Spend 20 minutes on active recall instead of 40 minutes re-reading.",
    shift: "Shift: vague effort demand \u2192 specific method change",
  },
];

const writeYourOwnTranslations = [
  "That feedback is pointing to a specific skill gap I can work on \u2014 it\u2019s data, not a label.",
  "This tells me my current strategy isn\u2019t working yet. Time to try a different approach.",
  "The feedback is about my method, not my ability. I can adjust and improve.",
];

const FeedbackTranslator = () => {
  const [flipped, setFlipped] = useState<boolean[]>(Array(6).fill(false));
  const [customFeedback, setCustomFeedback] = useState('');
  const [selectedTranslation, setSelectedTranslation] = useState<number | null>(null);
  const writeOwnId = useId();

  const translatedCount = flipped.filter(Boolean).length;
  const allTranslated = translatedCount === 6;

  const handleFlip = (index: number) => {
    if (flipped[index]) return;
    const next = [...flipped];
    next[index] = true;
    setFlipped(next);
  };

  return (
    <ExerciseSheet label="Interactive Activity" title="Feedback Translator" sub={'Tap each card to translate harsh "verdict language" into constructive "data language."'} name="FeedbackTranslator">
      {/* Progress: a count in the readout, not a tinted chip */}
      <p className="ex-count ui-readout" aria-live="polite">
        {allTranslated ? `All ${feedbackPairs.length} translated ✓` : `${translatedCount} / ${feedbackPairs.length} translated`}
      </p>

      <div className="ex-cards">
        {feedbackPairs.map((pair, i) => (
          <RevealCard
            key={i}
            revealed={flipped[i]}
            onPress={() => handleFlip(i)}
            keepBefore={false}
            toggles={false}
            before={<>
              <span className="ex-label">Verdict Language</span>
              <span className="ex-reveal-words">{pair.verdict}</span>
            </>}
            hint={<>
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" aria-hidden="true"><path d="M7 16V4m0 0L3 8m4-4l4 4M17 8v12m0 0l4-4m-4 4l-4-4"/></svg>
                    Tap to translate
            </>}
            after={<>
              <span className="ex-reveal-tickrow"><span className="ex-reveal-check">✓</span><span className="ex-label">Data Language</span></span>
              <span className="ex-reveal-words">{pair.data}</span>
              <span className="ex-reveal-note">{pair.shift}</span>
            </>}
          />
        ))}
      </div>

      {/* Completion */}
      <AnimatePresence>
        {allTranslated && (
          <MotionDiv initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}>
            <AnswerLine><b>Translation complete.</b> You can now hear feedback as information, not judgment.</AnswerLine>
          </MotionDiv>
        )}
      </AnimatePresence>

      {/* Write Your Own */}
      <ExercisePart title="Write Your Own" level={5} id={writeOwnId} sub="Type a piece of feedback you've received, then pick the translation that fits best.">
        <Field
          type="text"
          aria-labelledby={writeOwnId}
          value={customFeedback}
          onChange={(e) => { setCustomFeedback(e.target.value); setSelectedTranslation(null); }}
          placeholder="e.g. You always make silly mistakes..."
        />
        <AnimatePresence>
          {customFeedback.trim().length > 0 && (
            <MotionDiv initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -8 }} className="ex-stack">
              <AnswerGroup kind="one" legend="Pick your growth translation:">
                {writeYourOwnTranslations.map((t, i) => (
                  <ChoiceTile
                    key={i}
                    chosen={selectedTranslation === i}
                    onClick={() => setSelectedTranslation(i)}
                    label={t}
                  />
                ))}
              </AnswerGroup>
              <AnimatePresence>
                {selectedTranslation !== null && (
                  <MotionDiv initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }}>
                    <AnswerLine><b>You just turned a verdict into data.</b> That's the growth mindset in action.</AnswerLine>
                  </MotionDiv>
                )}
              </AnimatePresence>
            </MotionDiv>
          )}
        </AnimatePresence>
      </ExercisePart>
    </ExerciseSheet>
  );
};

// --- MODULE COMPONENT ---
const GrowthMindsetModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const essentials = useEssentialsMode();
  const { responses, saveResponse, isLoaded: _isLoaded } = useModuleResponses('growth-mindset-protocol');

  const sections = [
    { id: 'two-brains', title: 'The Two Brains: Fixed vs. Growth', eyebrow: '01 // The Operating System', icon: Cpu },
    { id: 'brain-muscle', title: 'Your Brain is Plastic', eyebrow: '02 // The Hardware Upgrade', icon: BrainCircuit },
    { id: 'power-of-yet', title: 'The Most Powerful Word', eyebrow: '03 // The Software Patch', icon: RotateCcw },
    { id: 'effort-is-key', title: 'Effort is the Real Talent', eyebrow: '04 // The Engine', icon: Zap },
    { id: 'feedback-fuel', title: 'Feedback is Fuel, Not a Verdict', eyebrow: '05 // The Navigation Data', icon: MessageSquareQuote },
    { id: 'install-os', title: 'Installing Your Growth OS', eyebrow: '06 // System Integration', icon: Activity },
  ];

  return (
    <ModuleLayout
      moduleNumber="14"
      moduleTitle="The Growth Playbook"
      moduleSubtitle="The Mind's Operating System"
      moduleDescription={`Your brain can actually change and get better at things — that's not just a nice idea, it's how your brain works. This module shows you how to stop thinking "I'm just not smart enough" and start seeing every challenge as a chance to grow.`}
      theme={theme}
      sections={sections}
      references={GROWTH_MINDSET_REFERENCE_LIST}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Unlock Growth Mode"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Two Brains: Fixed vs. Growth." eyebrow="Step 1" icon={Cpu} theme={theme}>
              {essentials ? (
                <>
                  <p>Fixed mindset: you believe you are either smart or not. Effort feels pointless. Failing feels permanent. Growth mindset: you believe you can get better with effort. Challenges become opportunities.<Cite n={1} /></p>
                  <p>Which one are you running? Take the diagnostic below to find out.</p>
                </>
              ) : (
                <>
                  <p>Think of your brain like a phone. Some people believe it shipped with whatever apps it's going to have, and that's it. You're born with a certain amount of intelligence, and you're stuck with it. This is the <Highlight description="Basically thinking you're either smart or you're not, and there's nothing you can do about it. If you have this, you'll dodge hard stuff because failing feels like proof you're just not good enough." theme={theme}>Fixed Mindset</Highlight>. When you're running this, effort feels pointless and failing feels like a permanent label on who you are.</p>
                  <p>But your brain is actually more like a phone you can keep upgrading. Every time you learn something new, you're adding new capabilities. This is the <Highlight description="Thinking that you can actually get smarter and better at things by putting in effort and trying new approaches. When you believe this, you stop being scared of hard stuff and start seeing it as a way to level up." theme={theme}>Growth Mindset</Highlight>.<Cite n={1} /> With this one, challenges are chances to get better and failing is just useful information about what to try next. So which one are you running right now?</p>
                  <PersonalStory name="Alex" role="Founder, NextStepUni" junior={{ children: (
                    <p>Growing up in Togher in Cork, I never saw school as something that mattered. I spent my time playing soccer and messing around — I genuinely believed the classroom wasn't for people like me. I fell in with the wrong crowds and was heading nowhere. I failed my Junior Cert, but honestly, I was on that path long before the results came out. The fixed mindset wasn't some concept in a textbook — it was my entire operating system, and I didn't even know it was running.</p>
                  ) }}>
                    <p>Growing up in Togher in Cork, I never saw school as something that mattered. I spent my time playing soccer and messing around — I genuinely believed the classroom wasn't for people like me. I fell in with the wrong crowds, started drinking, and was heading nowhere. I failed my Junior Cert, but honestly, I was on that path long before the results came out. The fixed mindset wasn't some concept in a textbook — it was my entire operating system, and I didn't even know it was running.</p>
                  </PersonalStory>
                </>
              )}
              <MindsetDiagnostic savedAnswers={responses['mindset-diagnostic']} onSaveAnswers={(a) => saveResponse('mindset-diagnostic', a)} />
              <MicroCommitment theme={theme}>
                <p>Listen to how you talk about school today. Catch one "fixed" thought (e.g., "I'm bad at Irish") and just notice it. You don't have to change it yet, just acknowledge you're running that piece of code.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="Your Brain is Plastic." eyebrow="Step 2" icon={BrainCircuit} theme={theme}>
              {essentials ? (
                <p>Your brain physically changes when you practise.<Cite n={2} /> Every time you study, you build stronger connections between brain cells. It is like wearing a path through a forest. More practice means a clearer, faster path. Try the simulator below.</p>
              ) : (
                <>
                  <p>Here's the thing most people don't realise: your brain is not set in stone. It physically changes based on what you do with it. This is called <Highlight description="Your brain's ability to physically rewire itself whenever you learn something new. Every time you practise, your brain builds stronger connections — it's literally how learning works under the hood." theme={theme}>Neuroplasticity</Highlight>. Think of learning a new maths formula like walking through a forest. The first time, it's hard going because there's no clear path.</p>
                  <p>But if you walk that same route every day (i.e., you practise the formula), you wear down a clear trail. In your brain, this is literally what happens: the connections between your brain cells get stronger, faster, and more efficient.<Cite n={2} /> You're actually building roads in your head every time you study. Every bit of effort you put in is real construction work happening inside your brain.</p>
                </>
              )}
              <NeuroplasticityVisualizer />
               <MicroCommitment theme={theme}>
                <p>Pick the one school subject you find hardest. Spend just five minutes tonight reviewing a topic from it. You just sent a work crew to start clearing a new path in your brain's forest.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="The Most Powerful Word." eyebrow="Step 3" icon={RotateCcw} theme={theme}>
                {essentials ? (
                  <p>Add the word "yet" to any fixed statement. "I cannot do this" becomes "I cannot do this yet." It keeps the door open. It tells your brain the story is not over. Try the reframe challenge below.</p>
                ) : (
                  <>
                    <p>A fixed mindset talks in absolutes: "I can't do this." "I'm not good at this." These are dead ends. They shut down effort and kill motivation. But there's a ridiculously simple fix: the word "yet."</p>
                    <p>Adding "yet" to the end of a fixed statement instantly changes it from a full stop into a work in progress. "I can't do this" becomes "I can't do this... yet." "I'm not good at this" becomes "I'm not good at this... yet." It sounds small, but it tells your brain the story isn't over. It keeps the door open for new approaches and more effort, and that's what keeps you going.</p>
                    <PersonalStory name="Alex" role="Founder, NextStepUni" junior={{ children: (
                      <p>After I lost one of my best friends during my Junior Cert years, my whole world shattered. But at some point, something shifted. I started reading about how people actually learn, and I realised the voice that had been telling me "you can't do this" was just a habit, not a fact. I built my own study system, and "I can't" slowly became "I can't yet." It felt fake at first — but bit by bit, it started to prove itself true.</p>
                    ) }}>
                      <p>After I lost one of my best friends during Junior Cert, my whole world shattered. In 4th year, something shifted. I started reading about how people actually learn, and I realised the voice that had been telling me "you can't do this" was just a habit, not a fact. I built my own study system, and "I can't" slowly became "I can't yet." It felt fake at first. But I went from failing my Junior Cert to nearly 600 points in the Leaving Cert and a UCC Scholarship. The "yet" was real — I just had to give it time to prove itself.</p>
                    </PersonalStory>
                  </>
                )}
                <ReframeChallenge savedText={responses['reframe-text']} onSave={(t) => saveResponse('reframe-text', t)} />
                <MicroCommitment theme={theme}>
                    <p>The next time you hear a friend (or yourself) say a "fixed" statement like "I don't get this," add a gentle "...yet?" at the end. You're installing the software patch for them.</p>
                </MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="Effort is the Real Talent." eyebrow="Step 4" icon={Zap} theme={theme}>
                {essentials ? (
                  <p>Talent gives you a head start. Effort is what actually makes you better. Focused practice on the hard bits builds real brain connections.<Cite n={3} /> If something feels hard, that is not a sign you are not smart enough. That is the process of getting smarter.</p>
                ) : (
                  <>
                    <p>Everyone loves the idea of "natural talent." We see someone who's brilliant at something and assume they were just born that way. This is one of the most unhelpful ideas out there. It teaches us that if something doesn't come easily, we must not be cut out for it.</p>
                    <p>But that's just not true. Talent might give you a head start, but effort is what actually makes you better. It's <Highlight description="Practising with focus on the bits you actually find hard, not just repeating the easy stuff. It's the kind of effort that stretches you just enough to make your brain build new connections and get better." theme={theme}>Deliberate Practice</Highlight><Cite n={3} /> — the focused, targeted kind — that builds those strong brain connections we talked about earlier. A growth mindset gets this: effort isn't a sign you're not smart enough. It's literally the process of getting smarter.</p>
                  </>
                )}
                <MicroCommitment theme={theme}>
                    <p>Identify one area where you rely on "talent". Now, identify one tiny, effortful action you can take to actually improve it. (e.g., If you're 'naturally good' at English, spend 10 minutes learning one new sophisticated word).</p>
                </MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="Feedback is Fuel, Not a Verdict." eyebrow="Step 5" icon={MessageSquareQuote} theme={theme}>
              {essentials ? (
                <p>Fixed mindset hears feedback as "you are stupid." Growth mindset hears "here is what to do differently." A bad grade is a signpost, not a label.<Cite n={4} /> Separate how you did from who you are. Try the translator below.</p>
              ) : (
                <>
                  <p>A fixed mindset hears criticism and thinks: "They're telling me I'm stupid." It treats feedback like a final judgement on who you are. This is why people with a fixed mindset get defensive or just give up when they get a bad grade or a harsh correction from a teacher.</p>
                  <p>A growth mindset hears the exact same criticism and thinks: "OK, so what can I do differently next time?" It treats feedback as useful information, not a personal attack. It's not about you as a person — it's about what you did this time. A bad grade isn't a label. It's a signpost showing you where to focus.<Cite n={4} /> Learning to separate how you did from who you are is one of the most useful things you can do.</p>
                </>
              )}
              <FeedbackTranslator />
              <MicroCommitment theme={theme}>
                <p>Go back to a piece of work where you got a lower grade than you wanted. Find one comment from the teacher and write down what strategy it's telling you to try next time.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="Installing Your Growth OS." eyebrow="Step 6" icon={Activity} theme={theme}>
              {essentials ? (
                <p>Growth mindset is a daily practice, not a one-time switch. Change how you talk to yourself. React to mistakes with curiosity, not shame. You become "the person working on getting better" instead of "the person who is bad at it."</p>
              ) : (
                <>
                  <p>A growth mindset isn't a magic switch you flip once. It's something you choose to practise every day through small, consistent habits: the way you talk to yourself, the way you react to mistakes, and the way you approach something difficult.</p>
                  <p>Once you start thinking this way, something cool happens. You stop being "the person who's bad at Maths" and become "the person who's working on getting better at Maths." That might sound like a small change, but it's massive. It's the difference between giving up and keeping going. And that's what this whole module has been building towards.</p>
                </>
              )}
               <MicroCommitment theme={theme}>
                <p>Write down your favourite "Growth Mindset Mantra" from this module. Stick it on your bedroom wall, your mirror, or the inside of your school journal. Make it visible.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default GrowthMindsetModule;
