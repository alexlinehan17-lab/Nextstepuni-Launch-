import { BrandedEngineCard,BrandedMindsetSorter } from './learning/WideFeatures';
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import { AnimatePresence,motion,Reorder } from 'framer-motion';
import {
Activity,
AlertTriangle,
Brain,
CheckCircle2,
GripVertical,
Lightbulb,
Map,
Settings,ShieldAlert,
Target,Users,
X,
Zap
} from 'lucide-react';
import React,{ useEffect,useState } from 'react';
import { AGENCY_PROTOCOL_REFERENCE_LIST } from '../data/references/agencyProtocol';
import { useEssentialsMode } from '../hooks/useEssentialsMode';
import { useModuleResponses } from '../hooks/useModuleResponses';
import { useNorthStar } from '../hooks/useNorthStar';
import { blueTheme } from '../moduleThemes';
import { COMPACT_CALLOUT_PLACEMENTS } from '../northStarData';
import { type ModuleProgress } from '../types';
import { ModuleLayout } from './ModuleLayout';
import { Cite } from './ModuleReferences';
import { Highlight,MicroCommitment,PersonalStory,ReadingSection } from './ModuleShared';
import NorthStarCallout from './NorthStarCallout';
import { AnswerGroup,AnswerLine,ExercisePart,ExerciseSheet } from './learning/Exercise';
import { ChoiceTile } from './ui/Choice';
import { Field } from './ui/Field';

const theme = blueTheme;

/* ═══ Shared press-down spring config ═══ */
const press = { type: 'spring' as const, stiffness: 400, damping: 25 };

const FlipCard = BrandedEngineCard;

/* ═══════════════════════════════════════════════════════
   MindsetSorter — chunky chips into coloured lanes
   ═══════════════════════════════════════════════════════ */
const MindsetSorter = BrandedMindsetSorter;


const AgencyProtocolModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const essentials = useEssentialsMode();
  const { responses, saveResponse, isLoaded } = useModuleResponses('agency-protocol');
  const { northStar } = useNorthStar();
  const [futureSelf, setFutureSelf] = useState('');
  const [dailyAction, setDailyAction] = useState('');
  const [battlePlanItems, setBattlePlanItems] = useState([
    { id: 'goal', text: 'Program Your Destination (Goal)' },
    { id: 'advantage', text: 'Know Your Engine (Advantage)' },
    { id: 'reframe', text: 'Install Your Suspension (Reframe)' },
    { id: 'hack', text: 'Take The Wheel (Classroom Hack)' },
  ]);
  const [scenarioChoice, setScenarioChoice] = useState<string | null>(null);

  useEffect(() => {
    if (isLoaded) {
      if (responses['futureSelf']) setFutureSelf(responses['futureSelf']);
      if (responses['dailyAction']) setDailyAction(responses['dailyAction']);
      if (responses['scenarioChoice']) setScenarioChoice(responses['scenarioChoice']);
    }
  }, [isLoaded]);

  const sections = essentials ? [
    { id: 'destination-path', title: 'Setting the Sat-Nav', eyebrow: '01 // Your Destination', icon: Target },
    { id: 'driver-passenger', title: 'Driver or Passenger?', eyebrow: '02 // Seizing the Wheel', icon: Users },
    { id: 'glitch', title: 'Roadblocks & Your Engine', eyebrow: '03 // Reframing Difficulty', icon: ShieldAlert },
    { id: 'blueprint', title: 'Your Route Plan', eyebrow: '04 // Building Your Driver Identity', icon: Map },
  ] : [
    { id: 'destination-path', title: 'Setting the Sat-Nav', eyebrow: '01 // Your Destination', icon: Target },
    { id: 'driver-passenger', title: 'Driver or Passenger?', eyebrow: '02 // Seizing the Wheel', icon: Users },
    { id: 'hacking', title: 'The Driver\'s Controls', eyebrow: '03 // Hacking Your Classroom', icon: Settings },
    { id: 'glitch', title: 'Roadblocks & Potholes', eyebrow: '04 // When the Journey is Unfair', icon: ShieldAlert },
    { id: 'advantage', title: 'Your Unique Engine', eyebrow: '05 // The Power of Your Story', icon: Zap },
    { id: 'blueprint', title: 'Your Route Plan', eyebrow: '06 // Building Your Driver Identity', icon: Map },
  ];

  return (
    <ModuleLayout
      moduleNumber="01"
      moduleTitle="The Driver's Manual"
      moduleSubtitle="Taking the Wheel of Your Education"
      moduleDescription="Learn how to stop being a passenger in your own school life and start driving toward the future you actually want."
      theme={theme}
      sections={sections}
      fullSectionsCount={6}
      references={AGENCY_PROTOCOL_REFERENCE_LIST}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Start Your Engine"
    >
      {(activeSection) => (
        <>
          {/* ══════════ Section 1: Setting the Sat-Nav ══════════ */}
          {activeSection === 0 && (
            <ReadingSection title="Setting the Sat-Nav: Your Future is Calling." eyebrow="Step 1" icon={Target} theme={theme}>
              {essentials ? (
                <>
                  <p>Without a destination, you're driving aimlessly. Connect today's homework to your future. See schoolwork as an <Highlight description="Every piece of study you do now is a direct deposit into your future self's bank account. It's not just homework — it's building the life you want." theme={theme}>Investment</Highlight> in your <Highlight description="A vivid picture of who you want to become. When you can actually see your future self clearly, today's effort feels worth it because you know exactly what you're working toward." theme={theme}>Possible Self</Highlight>.<Cite n={1} /></p>
                  <p>Students who link daily study to a real goal are more likely to do the work.<Cite n={2} /> Every action you take today builds the road.</p>
                </>
              ) : (
                <>
                  <p>Without a destination programmed into the Sat-Nav, you're just driving aimlessly. The same is true for school. You might know you want to go to college, but that's a vague spot on a map. To get there, you need a clear route, and that starts by connecting today's homework to tomorrow's destination.</p>
                  <p>The research points one way: linking your daily study to a future career you want makes you more likely to do the work.<Cite n={2} /> The solution is to stop seeing schoolwork as a chore and start seeing it as an <Highlight description="Every piece of study you do now is a direct deposit into your future self's bank account. It's not just homework — it's building the life you want." theme={theme}>Investment</Highlight> in your <Highlight description="A vivid picture of who you want to become. When you can actually see your future self clearly, today's effort feels worth it because you know exactly what you're working toward." theme={theme}>Possible Self</Highlight>.<Cite n={1} /> Every single action you take today builds the road to that future destination.</p>
                  <PersonalStory name="Alex" role="Founder, NextStepUni">
                    <p>For most of school, I had no destination programmed. Growing up in Togher, nobody in my world was talking about college courses or career paths. School was just something you showed up to — or didn't. I had no "Possible Self" because I'd never been shown one that looked like me. It wasn't until I lost my best friend and hit rock bottom that I even considered the idea that school could lead somewhere worth going.</p>
                  </PersonalStory>
                </>
              )}
              <MicroCommitment theme={theme}>
                <p>Open your phone's calendar right now. Schedule a 15-minute slot for tomorrow called 'Driving Practice' and use it to do the small action you list below.</p>
              </MicroCommitment>

              {/* Input form */}
              <ExerciseSheet title="Program Your Destination" name="ProgramDestination">
                <Field label="The Destination (Your Dream Course/Career)" value={futureSelf} onChange={(e) => setFutureSelf(e.target.value)} onBlur={() => saveResponse('futureSelf', futureSelf)} placeholder="e.g., Computer Science at Trinity" />
                <Field label="The First Turn (One Small Action Tomorrow)" value={dailyAction} onChange={(e) => setDailyAction(e.target.value)} onBlur={() => saveResponse('dailyAction', dailyAction)} placeholder="e.g., 20 minutes of Maths revision" />
                {futureSelf && dailyAction && (
                  <motion.div initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }}>
                    <AnswerLine>Route locked in. The journey starts now.</AnswerLine>
                  </motion.div>
                )}
              </ExerciseSheet>
            </ReadingSection>
          )}

          {/* ══════════ Section 2: Driver or Passenger? ══════════ */}
          {activeSection === 1 && (
            <ReadingSection title="Driver or Passenger? Seizing the Wheel." eyebrow="Step 2" icon={Users} theme={theme}>
              {essentials ? (
                <>
                  <p>You can be a Passenger, letting others decide for you. That makes you a <Highlight description="Someone who feels like their actions are controlled by other people — like a piece being moved around a chessboard. You do the work because someone told you to, not because you chose to." theme={theme}>Pawn</Highlight>. Or you can be a Driver, an <Highlight description="The opposite of a Pawn. You feel like the true source of your own actions. You're not being pushed — you're choosing to move. People who feel this way tend to do better in school." theme={theme}>Origin</Highlight>, who takes <Highlight description="You do the work because YOU have chosen to, not because someone is making you. It's your education, your choice, your future." theme={theme}>Academic Ownership</Highlight>.<Cite n={3} /></p>
                  <p>Being a Driver is a daily choice, not a personality trait. Choose it tomorrow in one class.</p>
                </>
              ) : (
                <>
                  <p>In the car of your education, you have two choices. You can be a 'Passenger', letting the teacher, your parents, or your friends decide the direction. You only do the work to avoid getting in trouble. This is being a <Highlight description="Someone who feels like their actions are controlled by other people — like a piece being moved around a chessboard. You do the work because someone told you to, not because you chose to." theme={theme}>Pawn</Highlight>, and it leads to shallow, rote learning that falls apart under exam pressure.</p>
                  <p>Or, you can be a 'Driver'—an <Highlight description="The opposite of a Pawn. You feel like the true source of your own actions. You're not being pushed — you're choosing to move. People who feel this way tend to do better in school." theme={theme}>Origin</Highlight>—who grabs the steering wheel. You take <Highlight description="You do the work because YOU have chosen to, not because someone is making you. It's your education, your choice, your future." theme={theme}>Academic Ownership</Highlight>.<Cite n={3} /> This isn't a personality trait you're born with; it's a choice you make every single day.</p>
                </>
              )}
              <MicroCommitment theme={theme}>
                <p>Think of one class you have tomorrow where you usually act like a passenger. Decide on one small 'driver' move you can make – like asking one question or deliberately trying to connect the topic to your own interests.</p>
              </MicroCommitment>
              <MindsetSorter />
            </ReadingSection>
          )}

          {/* ══════════ Section 3: Branching Scenario ══════════ */}
          {!essentials && activeSection === 2 && (
            <ReadingSection title="The Driver's Controls: Hacking the Classroom." eyebrow="Step 3" icon={Settings} theme={theme}>
               <p>Being a Driver isn't about ignoring the teacher; it's about working with them. You have controls — your questions, your comments, your focus — that influence the journey. Using them is called <Highlight description="Instead of sitting quietly and hoping things make sense, you actively shape how you learn. You ask questions, tell the teacher what's clicking and what's not, and make the material relevant to you." theme={theme}>Agentic Engagement</Highlight>.<Cite n={4} /></p>
               <p>Think of it like this: if you're lost while driving and you don't tell the sat-nav, it can't reroute you. Your teachers are the same — they need your feedback to give you the clear directions (<Highlight description="The road signs of your education — clear instructions, expectations, and feedback from your teacher. Without them you're guessing. With them, you know exactly where you stand." theme={theme}>Structure</Highlight>) and support you actually need.</p>
               <MicroCommitment theme={theme}>
                <p>Look at your notes from your hardest subject. Find one thing you don't fully understand. Write it down on a post-it note and stick it to your school journal as a reminder to ask the teacher tomorrow.</p>
              </MicroCommitment>

              {/* Branching Scenario */}
              <ExerciseSheet label="Scenario" title="The Confusion" sub="You don't understand the teacher's explanation. What's your move?" name="BranchingScenario">
                {/* Choosing locks the move in, so the arrow keys only move between the two */}
                <AnswerGroup kind="one" chooseOnArrow={false}>
                  <AnimatePresence>
                    {/* Passenger option — hide after choosing driver */}
                    {(!scenarioChoice || scenarioChoice === 'passive') && (
                      <motion.div
                        layout
                        exit={{ opacity: 0, scale: 0.9, transition: { duration: 0.2 } }}
                        transition={press}
                      >
                        <ChoiceTile
                          chosen={scenarioChoice === 'passive'}
                          onClick={() => { if (!scenarioChoice) { setScenarioChoice('passive'); saveResponse('scenarioChoice', 'passive'); } }}
                          label={
                            <span className="flex items-start gap-3">
                              <span className="ex-icon mt-0.5"><X size={18} aria-hidden="true" /></span>
                              <span className="flex flex-col gap-1">
                                <span className="ex-label">Passenger Move</span>{' '}
                                <span>Say nothing and hope you figure it out later.</span>
                              </span>
                            </span>
                          }
                        />
                      </motion.div>
                    )}

                    {/* Driver option — hide after choosing passenger */}
                    {(!scenarioChoice || scenarioChoice === 'agentic') && (
                      <motion.div
                        layout
                        exit={{ opacity: 0, scale: 0.9, transition: { duration: 0.2 } }}
                        transition={press}
                      >
                        <ChoiceTile
                          chosen={scenarioChoice === 'agentic'}
                          onClick={() => { if (!scenarioChoice) { setScenarioChoice('agentic'); saveResponse('scenarioChoice', 'agentic'); } }}
                          label={
                            <span className="flex items-start gap-3">
                              <span className="ex-icon mt-0.5"><CheckCircle2 size={18} aria-hidden="true" /></span>
                              <span className="flex flex-col gap-1">
                                <span className="ex-label">Driver Move</span>{' '}
                                <span>Ask a strategic question to clarify.</span>
                              </span>
                            </span>
                          }
                        />
                      </motion.div>
                    )}
                  </AnimatePresence>
                </AnswerGroup>

                <AnimatePresence>
                  {scenarioChoice && (
                    <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }} className="ex-block">
                      {/* The result's label, then its words (no coloured header band) */}
                      <p className="ex-label">
                        {scenarioChoice === 'passive' ? 'Roadblock ahead!' : 'Route recalculated!'}
                      </p>
                      <AnswerLine tone={scenarioChoice === 'passive' ? 'note' : 'ok'}>
                        {scenarioChoice === 'passive'
                          ? "You've missed a turn. The feeling of being \"lost\" grows, making it harder to catch up later."
                          : "You get a clear direction, help others in the car, and show the teacher you're a co-pilot. This is Agentic Engagement."
                        }
                      </AnswerLine>
                    </motion.div>
                  )}
                </AnimatePresence>
              </ExerciseSheet>
            </ReadingSection>
          )}

          {/* ══════════ Section 4: Reframe ══════════ */}
          {(essentials ? activeSection === 2 : activeSection === 3) && (
            <ReadingSection title={essentials ? "Roadblocks & Your Engine." : "Roadblocks & Potholes: When the Journey is Unfair."} eyebrow={essentials ? "Step 3" : "Step 4"} icon={ShieldAlert} theme={theme}>
              {northStar && (() => { const p = COMPACT_CALLOUT_PLACEMENTS.find(p => p.moduleId === 'agency-protocol'); return p ? <NorthStarCallout northStar={northStar} variant="compact" message={p.message} /> : null; })()}
              {essentials ? (
                <>
                  <p>Not all roads are equal. You may face real <Highlight description="The real-world stuff that makes school harder for some people — things like fewer resources, less support at home, or schools that are stretched thin. None of it is your fault, but it is part of your road." theme={theme}>Structural Conditions</Highlight>. The danger is interpreting <Highlight description="A mental trap where your brain confuses 'this is hard' with 'this isn't for me.' The work is supposed to be hard — that's what makes it worth something. Hard doesn't mean impossible." theme={theme}>Difficulty as Impossibility</Highlight>.<Cite n={5} /> Hard does not mean impossible.</p>
                  <p>Your life experience gave you a unique engine. Street smarts are academic superpowers. Reading people helps you analyse characters. Bouncing back from setbacks builds exam resilience.</p>
                </>
              ) : (
                <>
                  <p>Let's be real: not all roads are perfectly paved. If you're from a disadvantaged area, you face real <Highlight description="The real-world stuff that makes school harder for some people — things like fewer resources, less support at home, or schools that are stretched thin. None of it is your fault, but it is part of your road." theme={theme}>Structural Conditions</Highlight>. It's easy to see these roadblocks and think the journey is impossible for you.</p>
                  <p>This creates the most dangerous trap in education: interpreting <Highlight description="A mental trap where your brain confuses 'this is hard' with 'this isn't for me.' The work is supposed to be hard — that's what makes it worth something. Hard doesn't mean impossible." theme={theme}>Difficulty as Impossibility</Highlight>.<Cite n={5} /> The moment the work gets hard, your brain defaults to: "See? This isn't for people like me." The key is to install a high-tech suspension system in your brain: a conscious, deliberate reframe.</p>
                </>
              )}
              <MicroCommitment theme={theme}>
                <p>Write this 'Reframe' on a small piece of paper: "This is hard because it's a high-level problem. Solving it is a step toward my goal." Fold it up and put it in your wallet or pencil case.</p>
              </MicroCommitment>

              <ExerciseSheet title="The Mental Suspension System" name="MentalSuspensionSystem">
                {/* Negative thought: words you read, on the sheet, not in a box */}
                <p className="ex-quote flex items-start gap-2">
                  <span className="ex-icon mt-1"><AlertTriangle size={14} aria-hidden="true" /></span>
                  <span>&ldquo;I'll never be able for Higher Level Maths.&rdquo;</span>
                </p>
                {/* Reframe input */}
                <Field
                  label="Your reframe"
                  value={responses['reframeText'] || ''}
                  onChange={(e) => saveResponse('reframeText', e.target.value)}
                  placeholder="e.g., Maths is hard right now, but I haven't tried every approach yet."
                />
                {responses['reframeText'] && (
                  <motion.div initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }}>
                    <AnswerLine>Suspension installed. Pothole → speed bump.</AnswerLine>
                  </motion.div>
                )}
              </ExerciseSheet>
            </ReadingSection>
          )}

          {/* ══════════ Section 5: Flip Cards ══════════ */}
          {!essentials && activeSection === 4 && (
            <ReadingSection title="Your Unique Engine: The Power of Your Story." eyebrow="Step 5" icon={Zap} theme={theme}>
              <p>Society loves to focus on what students from disadvantaged backgrounds don't have. We're flipping that. Your life experiences have equipped your car with a unique, custom-tuned engine that many students with factory-standard parts simply don't have. This is your <Highlight description="The skills, street smarts, and real-world knowledge you've picked up from your life, your community, and your family. School doesn't always recognise them — but they're genuine advantages." theme={theme}>Funds of Knowledge</Highlight>.<Cite n={6} /></p>
              <p>These aren't just 'life skills' — they're genuine advantages that give you more horsepower for the Leaving Cert journey. Flip the cards below to see how your real-world experience translates directly into academic power.</p>
               <MicroCommitment theme={theme}>
                <p>Tell one person today—a friend, a family member—about one of your 'Street Smarts' and how it's actually a superpower for school. Saying it out loud makes it real.</p>
              </MicroCommitment>
              <div className="my-14 grid grid-cols-1 md:grid-cols-3 gap-5">
                <FlipCard front="Street Smarts: Reading different social situations." back="Academic Horsepower: High-level analysis of character in English." frontIcon={Users} backIcon={Lightbulb} colorIndex={0} />
                <FlipCard front="Street Smarts: Dealing with setbacks and bouncing back." back="Academic Horsepower: Resilience to keep studying after a bad mock result." frontIcon={Zap} backIcon={Activity} colorIndex={1} />
                <FlipCard front="Street Smarts: Translating for family or code-switching." back="Academic Horsepower: Advanced ability to analyse language in Irish & English papers." frontIcon={Brain} backIcon={Brain} colorIndex={2} />
              </div>
            </ReadingSection>
          )}

          {/* ══════════ Section 6: Reorder + Route Plan ══════════ */}
          {(essentials ? activeSection === 3 : activeSection === 5) && (
            <ReadingSection title="Your Route Plan: Building Your Driver Identity." eyebrow={essentials ? "Step 4" : "Step 6"} icon={Map} theme={theme}>
              <p>{essentials ? 'Build your Driver identity through daily action. Arrange your protocol below, then fill in your route plan.' : "A Driver identity isn't something you find; it's something you build through deliberate, daily action. It's the route plan that guides you when motivation is low and the road is long. First, arrange your protocol components into your personal pre-drive checklist."}</p>

              {/* The step's two exercises share one sheet (board c-read-flow: two exercises in a step, one sheet) */}
              <ExerciseSheet name="PreDriveChecklist">
              {/* Reorder checklist */}
              <ExercisePart title="Pre-Drive Checklist" sub="Drag to reorder by priority">
                {/* Rows you drag: each a box with a line, its number a neutral ring */}
                <Reorder.Group axis="y" values={battlePlanItems} onReorder={setBattlePlanItems} className="ex-cards">
                  {battlePlanItems.map((item, i) => {
                    return (
                      <Reorder.Item
                        key={item.id}
                        value={item}
                        className="flex items-center gap-3 cursor-grab active:cursor-grabbing border border-outline-soft bg-surface-paper text-ink-primary"
                        style={{
                          borderRadius: 'var(--r-box)',
                          padding: '14px 16px',
                          minHeight: 56,
                        }}
                        whileDrag={{ scale: 1.03, y: -2 }}
                      >
                        <GripVertical size={18} className="text-ink-muted shrink-0" aria-hidden="true" />
                        <span className="ex-badge">{i + 1}</span>
                        <span className="t-row">{item.text}</span>
                      </Reorder.Item>
                    );
                  })}
                </Reorder.Group>
              </ExercisePart>

              {/* Final route plan inputs */}
              <ExercisePart title="Finalise Your Route Plan">
                <Field label="My Destination (LC Goal)" value={responses['routeDestination'] || ''} onChange={(e) => saveResponse('routeDestination', e.target.value)} placeholder="e.g., 500 points for Engineering at UCD" />
                <Field label="My Custom Engine (My Advantage)" value={responses['routeEngine'] || ''} onChange={(e) => saveResponse('routeEngine', e.target.value)} placeholder="e.g., I'm good at staying calm under pressure." />
                <Field label="My First Turn (Classroom Hack)" value={responses['routeHack'] || ''} onChange={(e) => saveResponse('routeHack', e.target.value)} placeholder="e.g., Tomorrow in Maths, ask the teacher to explain the 'why'." />
              </ExercisePart>
              </ExerciseSheet>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default AgencyProtocolModule;
