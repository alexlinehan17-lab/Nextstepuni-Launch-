/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { SubjectModuleContent } from './subjectModuleData';

export const STEM_CONTENT: Record<string, SubjectModuleContent> = {
  // ────────────────────────────────────────────────────────────────
  //  MATHEMATICS (Higher Level)
  // ────────────────────────────────────────────────────────────────
  'mathematics': {
    subjectId: 'mathematics',
    subjectName: 'Mathematics',
    moduleNumber: '08',
    moduleTitle: 'Mastering Mathematics',
    moduleSubtitle: 'Your Complete Maths Exam Guide',
    moduleDescription: 'Understand how Paper 1 and Paper 2 work, where the marks are hiding, and exactly how to show your work to pick up every attempt mark.',
    themeName: 'indigo',
    sections: [
      // Section 1: Exam Structure
      {
        title: 'How Mathematics Actually Works',
        eyebrow: '01 // Exam Structure',
        paragraphs: [
          'Higher Level Maths is split across **two papers**, each worth **150 marks** and lasting **2 hours and 30 minutes**. That gives you a total of **300 marks** across five hours of exam time. Both papers have the same format: [[six questions]], and you must answer all of them. There is no choice -- every question counts.',
          'Paper 1 covers [[Algebra]], [[Functions and Graphs]], [[Complex Numbers]], [[Calculus]] (differentiation and integration), and [[Financial Maths]]. Paper 2 covers [[Geometry]], [[Trigonometry]], and [[Probability and Statistics]]. The split is clean, so you can focus your revision on one paper at a time without overlap.',
          'Each question is worth **25 marks** at minimum, but some carry up to **50 marks** depending on the part structure. Questions are broken into parts (a), (b), and often (c), with part (a) designed to be more accessible. The examiner expects to see your working clearly laid out -- not just final answers.',
          'Here is the big bonus: if you score a **H6 or above** (that is 40% or higher at Higher Level), you receive an extra **25 CAO points** on top of your grade points. This makes Maths one of the most strategically valuable subjects on your entire Leaving Cert. Even students who find Maths challenging can benefit enormously from sitting Higher Level and targeting that bonus.'
        ],
        highlights: [
          { term: 'six questions', description: 'Both Paper 1 and Paper 2 contain exactly 6 questions each. You must answer all 6 on each paper -- there is no choice.' },
          { term: 'Algebra', description: 'Covers expressions, equations, inequalities, indices, logs, and sequences & series. A huge chunk of Paper 1.' },
          { term: 'Functions and Graphs', description: 'Function notation, transformations, graph sketching, and interpreting graphs. Frequently combined with Calculus questions.' },
          { term: 'Complex Numbers', description: 'Operations with complex numbers, Argand diagrams, De Moivre\'s theorem, and roots of unity.' },
          { term: 'Calculus', description: 'Differentiation (from first principles, rules, applications) and Integration (indefinite, definite, area). The highest-value topic on Paper 1.' },
          { term: 'Financial Maths', description: 'Present value, future value, amortisation, and depreciation. Typically appears as part of one question on Paper 1.' },
          { term: 'Geometry', description: 'Coordinate geometry of the line, circle, and theorems/proofs. Proofs are examined directly and are worth learning off.' },
          { term: 'Trigonometry', description: 'Trig ratios, identities, equations, and solving triangles. Often combined with Geometry or 3D problems.' },
          { term: 'Probability and Statistics', description: 'Counting principles, probability rules, distributions (Normal, Bernoulli, Binomial), hypothesis testing, and inferential statistics.' }
        ],
        bullets: [
          'Paper 1: Algebra, Complex Numbers, Functions, Calculus, Financial Maths -- 150 marks, 2.5 hours',
          'Paper 2: Geometry, Trigonometry, Probability & Statistics -- 150 marks, 2.5 hours',
          'All 6 questions compulsory on each paper -- no choice',
          '+25 CAO bonus points for H6 (40%) or above at Higher Level'
        ]
      },
      // Section 2: Marking Criteria
      {
        title: 'What the Examiner Rewards',
        eyebrow: '02 // Marking Criteria',
        paragraphs: [
          'The Maths marking scheme is one of the most transparent in the entire Leaving Cert. Each part of each question is broken into specific **marking checkpoints** -- and crucially, the scheme awards [[attempt marks]] for any correct, relevant step even if you do not reach the final answer. This means that showing your work is not optional. It is where the marks live.',
          'When the examiner looks at your answer, they are checking: did you identify the right approach? Did you set up the problem correctly? Did you apply the relevant formula or technique? Did you carry out the algebra accurately? Each of these steps can earn marks independently. A student who sets up a Calculus problem correctly but makes an arithmetic slip in the final line can still earn **most of the marks** for that question.',
          'The marking scheme uses a system of [[scale marks]] -- typically on a scale of 0 to 5 or 0 to 10 for each part. A "5A" or "5B" scale means 5 marks are available, and partial credit is given for partially correct work. The key insight is that the examiner cannot give marks for work they cannot see. If you do steps in your head and skip to the answer, you are gambling everything on getting it perfectly right.',
          'For [[proofs and constructions]], the examiner follows a strict checklist. Each logical step or construction mark must appear on the page. Memorising the sequence of steps for the key geometry proofs and presenting them clearly is one of the easiest ways to guarantee full marks in an otherwise tricky area.'
        ],
        highlights: [
          { term: 'attempt marks', description: 'Marks awarded for correct initial steps or relevant work even when the final answer is incorrect. The Maths scheme is generous with these.' },
          { term: 'scale marks', description: 'The marking scheme grades each part on a numbered scale (e.g. 5A, 10C). Partial credit is built into the scale at each level.' },
          { term: 'proofs and constructions', description: 'Geometry proofs and ruler-and-compass constructions are marked against a strict step-by-step checklist. Learn the steps and present them clearly.' }
        ]
      },
      // Section 3: High-Value Zones
      {
        title: 'Where Your Marks Are',
        eyebrow: '03 // High-Value Zones',
        paragraphs: [
          'The single most valuable topic across both papers is [[Calculus]]. Differentiation and integration questions appear on Paper 1 every single year, typically accounting for **50 marks or more** -- that is one-third of the entire paper. If you can differentiate confidently, apply max/min problems, and integrate with reasonable accuracy, you are sitting on a huge chunk of marks.',
          'On Paper 2, [[Probability and Statistics]] is a goldmine for well-prepared students. The questions follow predictable patterns: Normal distribution calculations, hypothesis testing at the 5% significance level, and expected value problems. Once you learn the standard steps, these questions become almost mechanical. They regularly account for **40-50 marks** on Paper 2.',
          'The [[part (a) questions]] across both papers are designed to be accessible. They test foundational skills -- basic differentiation, solving a simple equation, plotting a point, or stating a definition. Across 12 questions, these opening parts can add up to **60+ marks** if you answer them all correctly. That alone could be worth close to a H5.',
          'Do not overlook [[Financial Maths]] on Paper 1. It typically appears as one part of a question and uses a small number of formulas (present value, amortisation). Students who learn these formulas and practise 3-4 past paper examples can often score full marks on this section with minimal revision time. It has one of the best marks-to-effort ratios on the entire exam.'
        ],
        highlights: [
          { term: 'Calculus', description: 'Differentiation and integration dominate Paper 1, worth 50+ marks annually. Master the rules and applications for the biggest single payoff.' },
          { term: 'Probability and Statistics', description: 'Predictable question patterns on Paper 2. Normal distribution, hypothesis testing, and counting principles are high-yield revision targets.' },
          { term: 'part (a) questions', description: 'The opening part of each question is designed to be the most accessible. Across both papers, these can add up to 60+ marks.' },
          { term: 'Financial Maths', description: 'A small number of formulas with high return. Learn present value, future value, and amortisation for reliable marks on Paper 1.' }
        ]
      },
      // Section 4: Common Pitfalls
      {
        title: 'What Costs You Marks',
        eyebrow: '04 // Common Pitfalls',
        paragraphs: [
          'The number one mark-killer in Maths is **skipping steps**. Students who do working in their heads and write only the final answer lose marks every single year. The marking scheme explicitly awards marks for setting up equations, substituting values, and simplifying -- even when the final answer is wrong. If the examiner cannot see your logic, they cannot award [[attempt marks]].',
          'The second major pitfall is [[poor time management]]. With 6 compulsory questions in 150 minutes, you have roughly 25 minutes per question. Students who spend 40 minutes on a difficult question and then rush the remaining five are throwing away easy marks. If you are stuck, write down everything you know about the problem, move on, and come back later.',
          'Many students lose marks through [[sign errors and arithmetic slips]] rather than conceptual misunderstanding. A minus sign dropped during differentiation or a factor of 2 forgotten in an integration can cascade through an entire solution. The fix is simple: write each step on a separate line, and double-check your algebra before moving to the next step.',
          'Finally, students consistently underperform on [[Geometry proofs]] because they try to wing them. The proofs on the syllabus are finite and examinable -- there are only a handful of them. Students who learn these proofs step-by-step and practise writing them out in full will pick up marks that most of their classmates leave behind.'
        ],
        highlights: [
          { term: 'attempt marks', description: 'Marks given for correct initial steps. You lose these when you skip working and jump to a final answer.' },
          { term: 'poor time management', description: 'Spending too long on one question means rushing others. Aim for roughly 25 minutes per question and move on if stuck.' },
          { term: 'sign errors and arithmetic slips', description: 'Small calculation errors that cascade through multi-step solutions. Writing one step per line helps catch them.' },
          { term: 'Geometry proofs', description: 'A finite set of proofs that appear regularly. Learning them by rote is one of the most reliable mark-earners on Paper 2.' }
        ]
      },
      // Section 5: Study Techniques
      {
        title: 'How to Study Mathematics',
        eyebrow: '05 // Study Techniques',
        paragraphs: [
          'Maths is not a spectator sport. Reading through solutions teaches you almost nothing. The only way to learn Maths is to **do Maths** -- pen in hand, working through problems from start to finish. Your primary study tool should be [[past paper practice]]. Work through every available Higher Level paper from the last 10 years, timed where possible.',
          'When you get a question wrong, do not just read the solution and move on. Take out a fresh page and [[rework the problem]] from scratch without looking at the answer. This is the step most students skip, and it is the step that actually builds the skill. If you cannot do it independently, you have not learned it yet.',
          'Build a [[formula reference sheet]] for each paper. Paper 1 formulas include differentiation rules, integration rules, the factor theorem, and financial maths formulas. Paper 2 formulas include coordinate geometry formulas, trig identities, and the Normal distribution z-score formula. Many of these are on the Formulae and Tables booklet, but knowing where to find them quickly saves critical time.',
          'Use [[topic rotation]] in your study sessions rather than spending an entire evening on one topic. Do 30 minutes of Calculus, then 30 minutes of Probability, then 30 minutes of Algebra. This interleaving forces your brain to practise switching between methods, which is exactly what the exam demands.'
        ],
        highlights: [
          { term: 'past paper practice', description: 'The single most effective study technique for Maths. Work through complete papers under timed conditions.' },
          { term: 'rework the problem', description: 'After checking a solution, redo the problem independently on a clean page. If you cannot, you have not truly learned it.' },
          { term: 'formula reference sheet', description: 'A personal summary of key formulas for each paper. Know where they are in the Tables booklet and which ones you need to memorise.' },
          { term: 'topic rotation', description: 'Interleave different Maths topics within a single study session to build the flexible problem-solving the exam requires.' }
        ]
      },
      // Section 6: Action Plan
      {
        title: 'Your Mathematics Action Plan',
        eyebrow: '06 // Action Plan',
        paragraphs: [
          'Start by printing or downloading the last **five years** of Higher Level Maths papers from examinations.ie. Work through Paper 1 and Paper 2 separately, focusing on one topic at a time. For each question you get wrong, rework it independently the next day. Track which topics you are weakest on and prioritise those in your next study session.',
          'Build your revision around three priorities: **Calculus** on Paper 1 (your biggest single marks target), **Probability and Statistics** on Paper 2 (the most predictable questions), and **part (a) answers** across every question on both papers (your safety net for base marks). If you are aiming for the H6 bonus, focus on nailing these three areas first before broadening out.',
          'In the final two weeks before the exam, do at least two full timed papers -- one Paper 1 and one Paper 2 -- under exam conditions. Use the Formulae and Tables booklet, time yourself strictly, and mark your own paper against the published marking scheme. This builds the time pressure stamina that separates students who know the content from students who can actually perform on the day.'
        ],
        highlights: [],
        commitmentText: 'This week, I will complete one full past Paper 1 under timed conditions (2.5 hours), mark it against the marking scheme, and rework every question I scored below 50% on.'
      }
    ]
  },

  // ────────────────────────────────────────────────────────────────
  //  APPLIED MATHS
  // ────────────────────────────────────────────────────────────────
  'applied-maths': {
    subjectId: 'applied-maths',
    subjectName: 'Applied Maths',
    moduleNumber: '09',
    moduleTitle: 'Mastering Applied Maths',
    moduleSubtitle: 'Your Complete Applied Maths Guide',
    moduleDescription: 'Decode the Applied Maths exam -- understand the topic weighting, how to set up problems correctly, and where students leave the most marks on the table.',
    themeName: 'violet',
    sections: [
      // Section 1: Exam Structure
      {
        title: 'How Applied Maths Actually Works',
        eyebrow: '01 // Exam Structure',
        paragraphs: [
          'Applied Maths consists of a **single exam paper** lasting **2 hours and 30 minutes**. The paper contains **10 questions**, and you must answer **6 of them**. Each question is worth **50 marks**, giving a total of **300 marks**. The beauty of this exam is the choice -- you pick the 6 topics you are strongest in and ignore the rest.',
          'The 10 questions map directly onto 10 topics from the syllabus: [[Linear Motion]], [[Projectiles]], [[Newton\'s Laws]], [[Connected Particles]], [[Moments and Equilibrium]], [[Statics]] (including inclined planes), [[Collisions]] (including oblique impacts), [[Circular Motion]], [[Simple Harmonic Motion]] (SHM), and [[Differential Equations]]. Each topic gets exactly one question every year, so the paper is highly predictable.',
          'Most students focus on **6 to 8 topics** during their revision and aim to be confident in at least 7, giving themselves one spare topic as insurance. The questions follow recognisable patterns -- once you have seen the types of problems that appear in each topic, you can practise them systematically.',
          'There is no coursework, no practical component, and no oral or aural. It is purely an exam-based subject. This means your entire grade is determined by what you produce in those 150 minutes. The upside is that revision is straightforward: learn the methods, practise the problems, and execute on the day.'
        ],
        highlights: [
          { term: 'Linear Motion', description: 'Equations of motion (suvat), velocity-time graphs, and multi-stage journeys. Usually one of the more accessible questions.' },
          { term: 'Projectiles', description: 'Objects launched at angles -- finding range, max height, time of flight. A very popular choice among students.' },
          { term: 'Newton\'s Laws', description: 'F=ma applied to particles on surfaces, in lifts, or on inclines. Core topic that connects to several others.' },
          { term: 'Connected Particles', description: 'Pulleys, tow-ropes, and systems of particles. Requires careful free-body diagrams and simultaneous equations.' },
          { term: 'Moments and Equilibrium', description: 'Turning effects of forces, balancing beams, and ladders against walls. Setting up the moment equation correctly is key.' },
          { term: 'Statics', description: 'Resolving forces on inclined planes, friction, and equilibrium problems. Requires clean force diagrams.' },
          { term: 'Collisions', description: 'Conservation of momentum and coefficient of restitution. Direct and oblique impacts between particles and walls.' },
          { term: 'Circular Motion', description: 'Objects moving in circles -- conical pendulums, cars on banked tracks, vertical circles.' },
          { term: 'Simple Harmonic Motion', description: 'Oscillating systems -- springs, pendulums. Requires knowledge of SHM equations and period formulas.' },
          { term: 'Differential Equations', description: 'First and second order differential equations modelling physical situations. Often the most challenging question.' }
        ],
        bullets: [
          'Single paper: 2.5 hours, 10 questions, answer any 6',
          'Each question: 50 marks. Total: 300 marks',
          'One question per topic -- highly predictable structure',
          'No coursework or practical -- 100% exam-based'
        ]
      },
      // Section 2: Marking Criteria
      {
        title: 'What the Examiner Rewards',
        eyebrow: '02 // Marking Criteria',
        paragraphs: [
          'Applied Maths questions follow a consistent internal structure. Each 50-mark question is typically split into **two or three parts**, and the marking scheme awards marks at each stage of the solution. The examiner is looking for three things: a correct [[problem setup]], accurate [[mathematical execution]], and a clear final answer with appropriate units.',
          'The most important marks in Applied Maths are earned in the **setup phase**. Drawing a correct [[free-body diagram]], identifying the right equations of motion, or establishing the correct coordinate system can be worth **10-15 marks** before you even start solving. Students who skip the diagram and dive straight into algebra are gambling with a huge portion of the marks.',
          'The marking scheme uses a **cumulative approach** -- if you make an error early in a solution but then solve correctly from that point, you can still earn [[follow-through marks]] for all subsequent correct work. This means you should never abandon a question just because you think you made a mistake halfway through. Keep going -- the examiner will credit your method.',
          'Presentation matters more in Applied Maths than in pure Maths. Because problems involve physical scenarios, the examiner expects to see: a clear diagram, forces labelled with their correct directions, variables defined (e.g., "Let a = acceleration"), and the final answer clearly stated with units. Answers without units can lose marks even if the numerical value is correct.'
        ],
        highlights: [
          { term: 'problem setup', description: 'The initial stage where you define variables, draw diagrams, and identify which equations apply. Worth a significant portion of marks on every question.' },
          { term: 'mathematical execution', description: 'The algebra and arithmetic you perform after setting up. Clean, step-by-step working is essential.' },
          { term: 'free-body diagram', description: 'A diagram showing all forces acting on a particle or body. This is your single most important tool for earning setup marks.' },
          { term: 'follow-through marks', description: 'If you make an early error but solve correctly from that point, the examiner still awards marks for your correct method.' }
        ]
      },
      // Section 3: High-Value Zones
      {
        title: 'Where Your Marks Are',
        eyebrow: '03 // High-Value Zones',
        paragraphs: [
          'The highest-value topics in terms of marks-to-effort ratio are [[Linear Motion]] and [[Projectiles]]. Both follow predictable patterns, use the same small set of suvat equations, and appear in recognisable formats year after year. Most students can master both topics with 4-5 hours of focused practice. Together they represent **100 marks** -- one-third of your total.',
          '[[Newton\'s Laws]] and [[Connected Particles]] are the next tier. They require slightly more setup work (free-body diagrams, simultaneous equations), but the question types are finite and learnable. If you add these to Linear Motion and Projectiles, you now have 4 confident topics worth **200 marks**. You only need 2 more.',
          '[[Collisions]] is often underestimated by students but is one of the most reliable scoring topics. The questions almost always involve conservation of momentum and the coefficient of restitution formula. Once you learn the two-step method (momentum equation + restitution equation), you can solve nearly every collision problem that has appeared in the last 15 years.',
          'For your sixth topic, [[Moments and Equilibrium]] or [[Circular Motion]] tend to be the most popular choices. Moments questions involve balancing forces around a pivot -- if you can set up the moment equation correctly, the rest is straightforward algebra. Circular Motion questions follow a small number of standard setups (conical pendulum, banked track, vertical circle).'
        ],
        highlights: [
          { term: 'Linear Motion', description: 'Uses suvat equations in predictable formats. One of the easiest topics to score 50/50 on with focused practice.' },
          { term: 'Projectiles', description: 'Launches at angles using suvat + trig. Highly patterned questions that reward systematic practice.' },
          { term: 'Newton\'s Laws', description: 'F=ma applied to standard setups. Requires good diagrams but the algebra is manageable.' },
          { term: 'Connected Particles', description: 'Pulley systems and tow-ropes. Once you master the free-body diagram technique, these become very scorable.' },
          { term: 'Collisions', description: 'Conservation of momentum + restitution formula. A reliable 50 marks once you learn the two-step method.' },
          { term: 'Moments and Equilibrium', description: 'Balancing forces around a pivot. Clean setup leads to straightforward algebra.' },
          { term: 'Circular Motion', description: 'Standard setups like conical pendulums and banked tracks. Learn the key formula and apply to each scenario.' }
        ]
      },
      // Section 4: Common Pitfalls
      {
        title: 'What Costs You Marks',
        eyebrow: '04 // Common Pitfalls',
        paragraphs: [
          'The single biggest mark-killer in Applied Maths is a **missing or incorrect diagram**. Every year, students lose setup marks because they did not draw a free-body diagram, or they drew one with forces pointing in the wrong direction. The diagram is not decoration -- it is where the examiner looks first to see if you understand the problem. A wrong diagram means wrong equations, which means a wrong answer and [[lost setup marks]].',
          'The second critical error is [[sign convention mistakes]]. In Applied Maths, positive and negative directions matter enormously. If you define "up" as positive for one equation but accidentally treat "down" as positive in the next, your entire solution collapses. Always write your sign convention at the top of your answer (e.g., "Taking right and up as positive") and stick to it.',
          'Students also lose marks by [[not defining variables]]. The examiner needs to know what your letters represent. Writing "Let T = tension in the string, a = acceleration of the system" takes five seconds but makes your solution readable and earns you marks. Jumping into algebra with undefined variables makes the examiner guess at your reasoning.',
          'Finally, many students attempt too many questions. You only need 6, but some students start 7 or 8 and finish none of them properly. A half-finished question is worth far less than a complete one. Pick your 6 best topics, commit to them, and [[finish each question fully]] before moving on.'
        ],
        highlights: [
          { term: 'lost setup marks', description: 'Marks allocated for the initial diagram, variable definition, and equation setup. These are lost when diagrams are missing or incorrect.' },
          { term: 'sign convention mistakes', description: 'Using inconsistent positive/negative directions across equations. Always state your convention and stick to it throughout.' },
          { term: 'not defining variables', description: 'Jumping into algebra without stating what each letter represents. This costs marks and makes your work harder to follow.' },
          { term: 'finish each question fully', description: 'A complete answer to 6 questions beats partial answers to 8. Commit to your chosen 6 and see each one through to the end.' }
        ]
      },
      // Section 5: Study Techniques
      {
        title: 'How to Study Applied Maths',
        eyebrow: '05 // Study Techniques',
        paragraphs: [
          'Applied Maths is the most pattern-based subject on the Leaving Cert. The same question types repeat year after year with different numbers. Your study strategy should centre on [[topic-by-topic past papers]]: take one topic (e.g., Projectiles), pull out that question from every available past paper, and work through them all in sequence. You will quickly see the 3-4 standard problem types that appear.',
          'For each topic, build a [[method sheet]] -- a single page that lists the key formulas, the standard setup steps, and the common variations. For Projectiles, this might be: "Step 1: Resolve initial velocity into horizontal and vertical components. Step 2: Use suvat equations for vertical motion. Step 3: Use constant velocity for horizontal motion." These sheets become your revision backbone.',
          'Practice under [[time pressure]] is essential. In the exam, you have approximately 25 minutes per question. Time yourself when doing past papers and build up to completing questions within this window. If a question consistently takes you more than 30 minutes, you either need more practice on that topic or should consider swapping it for a different one.',
          'Finally, use the [[marking scheme as a study tool]]. After attempting a question, mark it yourself using the official scheme. This teaches you exactly what the examiner is looking for, where the marks are allocated, and what level of working is expected. You will learn to write solutions that hit every marking checkpoint.'
        ],
        highlights: [
          { term: 'topic-by-topic past papers', description: 'Group past paper questions by topic and work through all available examples for each. This reveals the repeating patterns.' },
          { term: 'method sheet', description: 'A single-page summary of the key steps, formulas, and common variations for each topic. Your core revision tool.' },
          { term: 'time pressure', description: 'Practise completing questions in 25 minutes or less. If a topic consistently takes too long, consider swapping it out.' },
          { term: 'marking scheme as a study tool', description: 'Mark your own practice answers using the official scheme. This teaches you exactly what the examiner rewards.' }
        ]
      },
      // Section 6: Action Plan
      {
        title: 'Your Applied Maths Action Plan',
        eyebrow: '06 // Action Plan',
        paragraphs: [
          'Choose your **6 core topics** and 1-2 backup topics. For most students, a strong starting six is: Linear Motion, Projectiles, Newton\'s Laws, Connected Particles, Collisions, and either Moments or Circular Motion. Print out the past paper questions for each of these topics (examinations.ie has papers going back decades) and organise them by topic.',
          'Work through each topic in order, spending 2-3 study sessions per topic. On the first session, learn the method and do 2-3 questions with the textbook open. On the second session, do 3-4 questions without help. On the third session, do them under timed conditions. After completing all 6 topics, do at least two full mock exams under exam conditions -- picking your 6 questions and finishing within 2.5 hours.',
          'In the final week, review your method sheets, redo any questions you previously got wrong, and do one final timed paper. On exam day, read all 10 questions before committing to your 6. Start with the topic you are most confident in to settle your nerves and build momentum.'
        ],
        highlights: [],
        commitmentText: 'This week, I will choose my 6 core topics and complete 3 past paper questions from my strongest topic under timed conditions (25 minutes each).'
      }
    ]
  },

  // ────────────────────────────────────────────────────────────────
  //  PHYSICS
  // ────────────────────────────────────────────────────────────────
  'physics': {
    subjectId: 'physics',
    subjectName: 'Physics',
    moduleNumber: '10',
    moduleTitle: 'Mastering Physics',
    moduleSubtitle: 'Your Complete Physics Exam Guide',
    moduleDescription: 'Master the Physics exam from experiments to problem-solving -- understand how marks are allocated and what the examiner actually wants to see.',
    themeName: 'cyan',
    sections: [
      // Section 1: Exam Structure
      {
        title: 'How Physics Actually Works',
        eyebrow: '01 // Exam Structure',
        paragraphs: [
          'The Physics Leaving Cert consists of a **single exam paper** lasting **3 hours** and worth a total of **400 marks**. The paper is divided into two sections: [[Section A]] (experiments) and [[Section B]] (theory and problem-solving). Understanding how marks are split between these two sections is the first step to maximising your grade.',
          '[[Section A]] is worth **120 marks** and contains **4 experiment questions** -- you must answer **3 of them**. Each experiment question is worth **40 marks**. These questions are based on the [[mandatory experiments]] you performed (or should have performed) during the course. They ask you to describe the procedure, draw the setup, list precautions, and explain how you obtained and used your results.',
          '[[Section B]] is worth **280 marks** and contains **8 questions** -- you must answer **5 of them**. Each question is worth **56 marks**. These cover the full theory syllabus: Mechanics, Heat, Waves, Electricity, Modern Physics (atomic physics, nuclear physics, and particle physics), and the optional topics. Questions typically mix definitions, explanations, calculations, and diagram work.',
          'The total demand is 8 questions (3 from Section A + 5 from Section B) in 180 minutes. That gives you roughly **22 minutes per question** on average -- though you should spend less time on the shorter experiment questions and more on the longer theory questions.'
        ],
        highlights: [
          { term: 'Section A', description: 'Experiments section: 4 questions, answer 3. Worth 120 marks (40 marks each). Based on mandatory experiments from the course.' },
          { term: 'Section B', description: 'Theory and problem-solving: 8 questions, answer 5. Worth 280 marks (56 marks each). Covers the full Physics syllabus.' },
          { term: 'mandatory experiments', description: 'A set of prescribed experiments you must know. They form the basis of all Section A questions and can also appear in Section B.' }
        ],
        bullets: [
          'Single paper: 3 hours, 400 marks total',
          'Section A: 3 from 4 experiment questions (120 marks)',
          'Section B: 5 from 8 theory questions (280 marks)',
          'Roughly 22 minutes per question'
        ]
      },
      // Section 2: Marking Criteria
      {
        title: 'What the Examiner Rewards',
        eyebrow: '02 // Marking Criteria',
        paragraphs: [
          'In Section A, the examiner rewards **specificity and precision**. When describing an experiment, you need to give [[exact procedural details]] -- not vague summaries. For example, "I measured the diameter of the wire using a micrometer screw gauge, taking readings at several points along the wire" earns more marks than "I measured the wire." Name the instruments, describe what you did with them, and mention how you ensured accuracy.',
          'For Section B, the marking scheme values **definitions, laws, and derivations**. Many questions open with "Define..." or "State the law of..." and these carry [[definition marks]] that are essentially free if you have learned them. The examiner expects the exact, precise wording from the syllabus. A vague or incomplete definition loses marks even if you understand the concept.',
          'In calculation questions, the examiner awards marks for [[method and substitution]] as well as the final answer. Writing the relevant formula, substituting the values with correct units, and showing each algebraic step earns marks at every stage. A correct final answer with no working might get full marks, but a wrong final answer with correct method still earns most of the marks.',
          'Diagrams are [[essential in Physics]]. When you are asked to describe an experiment or explain a concept, a clear, labelled diagram can earn 6-9 marks on its own. Always draw diagrams large enough to label clearly, use a ruler for straight lines, and label every component. The examiner cannot give marks for a diagram they cannot read.'
        ],
        highlights: [
          { term: 'exact procedural details', description: 'Name the equipment, describe each step precisely, and explain how you ensured accuracy. Vague descriptions lose marks.' },
          { term: 'definition marks', description: 'Marks awarded for stating precise definitions and laws. These are near-free marks if you learn the exact wording.' },
          { term: 'method and substitution', description: 'Marks for showing the formula, substituting correctly, and working through the algebra step by step.' },
          { term: 'essential in Physics', description: 'Diagrams can be worth 6-9 marks per question. Draw them large, use a ruler, and label every component.' }
        ]
      },
      // Section 3: High-Value Zones
      {
        title: 'Where Your Marks Are',
        eyebrow: '03 // High-Value Zones',
        paragraphs: [
          '[[Section A]] is the highest-value zone on the entire Physics paper. The experiment questions are **highly predictable** -- the same experiments come up in rotation, and the format is always the same: describe, diagram, procedure, precautions, results. A student who thoroughly learns all the mandatory experiments can walk into Section A and confidently score **100-120 marks** out of 120. That is 30% of the entire exam secured before you even open Section B.',
          'In Section B, [[Electricity]] is the single most valuable topic. It appears every year, often as two separate questions (one on circuits/Ohm\'s Law and one on electromagnetism or electromagnetic induction). Electricity questions carry a high proportion of calculation marks, which tend to be more straightforward to earn than explanation marks. If you are strong on V=IR, series/parallel circuits, and electromagnetic induction, this topic alone can be worth **80-100 marks**.',
          '[[Mechanics]] is the other heavyweight topic in Section B, covering forces, motion, momentum, and energy. Like Electricity, it appears every year and often spans more than one question. The calculations use familiar equations (F=ma, s=ut+1/2at^2, momentum conservation) that you may already know from Applied Maths or from Paper 2 of regular Maths.',
          '[[Definitions and laws]] scattered throughout Section B are easy marks that students often leave behind. There are approximately 40-50 definitions on the Physics syllabus. Questions that start with "Define..." or "State..." are testing recall, not understanding. Learning these by rote takes a few hours of flashcard work and can be worth 30-40 marks across the paper.'
        ],
        highlights: [
          { term: 'Section A', description: 'Experiment questions are highly predictable and follow the same format every year. Learn all mandatory experiments for reliable marks.' },
          { term: 'Electricity', description: 'Appears every year in Section B, often as two questions. Circuit calculations and electromagnetic induction are high-yield revision targets.' },
          { term: 'Mechanics', description: 'Forces, motion, momentum, and energy. Uses familiar equations and appears as at least one question annually.' },
          { term: 'Definitions and laws', description: 'Around 40-50 definitions on the syllabus. Learning them by rote is worth 30-40 marks across the paper.' }
        ]
      },
      // Section 4: Common Pitfalls
      {
        title: 'What Costs You Marks',
        eyebrow: '04 // Common Pitfalls',
        paragraphs: [
          'The most common mistake in Physics is writing **vague experiment descriptions**. Students write things like "We set up the apparatus and took measurements." This earns almost nothing. The examiner needs to see: what apparatus you used (by name), how you set it up, what you measured, what instrument you used to measure it, and what [[precautions]] you took. Specificity is everything in Section A.',
          'In Section B, students consistently lose marks by giving [[incomplete definitions]]. "Velocity is speed with direction" is not precise enough. The correct definition is "Velocity is the rate of change of displacement with respect to time." Every word matters. Learn definitions from the textbook or syllabus, not from memory or paraphrase.',
          'Calculation errors caused by [[unit confusion]] are another major mark-killer. Physics uses a mix of units (km, m, cm, mm; kg, g; hours, seconds) and students who do not convert everything to SI units before substituting into formulas regularly get wrong answers. Always convert to metres, kilograms, and seconds before you start calculating.',
          'Finally, students waste time and marks by [[attempting too many questions]]. You need 3 from Section A and 5 from Section B. Some students attempt extra questions "just in case" but this eats into time for their other answers. The examiner marks only your best attempts up to the required number, so spreading yourself thin is counterproductive.'
        ],
        highlights: [
          { term: 'precautions', description: 'Specific steps taken to ensure accuracy in experiments. Examples: repeat measurements, use a spirit level, allow time for thermal equilibrium.' },
          { term: 'incomplete definitions', description: 'Vague or paraphrased definitions lose marks. The examiner expects precise, syllabus-standard wording.' },
          { term: 'unit confusion', description: 'Mixing units (e.g., km with m, grams with kg) leads to wrong answers. Convert everything to SI units before calculating.' },
          { term: 'attempting too many questions', description: 'Only the required number of answers are marked. Attempting extras wastes time better spent completing your chosen questions.' }
        ]
      },
      // Section 5: Study Techniques
      {
        title: 'How to Study Physics',
        eyebrow: '05 // Study Techniques',
        paragraphs: [
          'Your Physics revision should be split into two distinct tracks: [[experiment revision]] and [[theory revision]]. For experiments, create a one-page summary for each mandatory experiment including: diagram, equipment list, procedure (step by step), precautions, and how results are processed. Practise writing out these summaries from memory until you can reproduce them cleanly.',
          'For theory, use a combination of [[definition flashcards]] and [[problem practice]]. Make flashcards for every definition, law, and principle on the syllabus. Test yourself daily using active recall -- cover the answer, state it aloud, then check. For calculations, work through past paper questions topic by topic, starting with Electricity and Mechanics as your highest-priority areas.',
          'When studying a theory topic, always start with the **definitions and laws**, then move to **explanations and applications**, and finally to **calculations**. This mirrors the structure of exam questions, which typically open with a definition, then ask for an explanation, then pose a calculation. Studying in this order means you build understanding from the ground up.',
          'Use [[past marking schemes]] as your revision guide. After attempting a question, check the marking scheme to see exactly where marks are allocated. You will quickly notice that the scheme rewards very specific phrases, diagram labels, and calculation steps. Learning to write answers that match the scheme\'s expectations is the fastest route to higher marks.'
        ],
        highlights: [
          { term: 'experiment revision', description: 'A separate revision track focused on mastering all mandatory experiments. Create one-page summaries and practise reproducing them.' },
          { term: 'theory revision', description: 'Covers definitions, explanations, and calculations. Use flashcards for definitions and past papers for calculation practice.' },
          { term: 'definition flashcards', description: 'Physical flashcards or a digital app (like Anki) with one definition per card. Test yourself daily using active recall.' },
          { term: 'problem practice', description: 'Work through past paper calculations topic by topic. Start with Electricity and Mechanics for the highest mark payoff.' },
          { term: 'past marking schemes', description: 'The examiner\'s own guide to what earns marks. Study them to learn which phrases, labels, and steps are rewarded.' }
        ]
      },
      // Section 6: Action Plan
      {
        title: 'Your Physics Action Plan',
        eyebrow: '06 // Action Plan',
        paragraphs: [
          'Start with Section A. List all the mandatory experiments, then write out a one-page summary for each one from memory. Check against your textbook and fill any gaps. Aim to be able to reproduce all experiment write-ups cleanly within two weeks. This secures up to **120 marks** -- nearly a third of the paper.',
          'For Section B, prioritise **Electricity** and **Mechanics** first (they appear every year), then add **Waves**, **Heat**, and your strongest remaining topic. Make definition flashcards for each topic as you study it. Work through at least 5 past paper questions per topic, marking your own answers against the official scheme.',
          'In the final fortnight, do two full timed papers (3 hours each) under exam conditions. After each, identify your weakest area and spend one focused session on it. On exam day, read every question in Section A before choosing your 3, and every question in Section B before choosing your 5. Start with the questions you are most confident in.'
        ],
        highlights: [],
        commitmentText: 'This week, I will write out one-page summaries for 5 mandatory experiments from memory and check them against my textbook for accuracy.'
      }
    ]
  },

  // ────────────────────────────────────────────────────────────────
  //  CHEMISTRY
  // ────────────────────────────────────────────────────────────────
  'chemistry': {
    subjectId: 'chemistry',
    subjectName: 'Chemistry',
    moduleNumber: '11',
    moduleTitle: 'Mastering Chemistry',
    moduleSubtitle: 'Your Complete Chemistry Exam Guide',
    moduleDescription: 'Break down the Chemistry exam by section -- mandatory experiments, theory questions, and calculations -- and learn where the high-value marks are.',
    themeName: 'teal',
    sections: [
      // Section 1: Exam Structure
      {
        title: 'How Chemistry Actually Works',
        eyebrow: '01 // Exam Structure',
        paragraphs: [
          'The Chemistry Leaving Cert is a **single exam paper** lasting **3 hours** with a total of **400 marks**. Like Physics, it is divided into two main sections: [[Section A]] (experiments) and [[Section B]] (theory, calculations, and applied chemistry). The structure rewards students who prepare both their experimental knowledge and their theory comprehensively.',
          '[[Section A]] is worth **120 marks** and typically contains around **5 experiment-based questions** -- you must answer **3 of them**. Each is worth **40 marks**. These are drawn from the [[mandatory experiments]] on the syllabus, covering areas like titrations, organic preparations, tests for ions and gases, and calorimetry. The format is predictable: describe, draw, explain results, and state precautions.',
          '[[Section B]] is worth **280 marks** and contains **8 questions** -- you must answer **5 of them**. Each question is worth **56 marks**. These questions span the major syllabus areas: Atomic Theory and the Periodic Table, Chemical Bonding, Stoichiometry and the Mole, Organic Chemistry, Rates of Reaction, Equilibrium, Acids and Bases, Oxidation-Reduction, and Industrial Chemistry/Environmental Chemistry.',
          'The exam demands 8 answers in 180 minutes, giving roughly **22 minutes per question**. However, the experiment questions in Section A tend to be shorter and more formulaic, so experienced students often allocate about 15 minutes each for Section A and 24-25 minutes each for Section B.'
        ],
        highlights: [
          { term: 'Section A', description: 'Experiment questions: typically 5 available, answer 3. Worth 120 marks total (40 each). Based on mandatory practical work.' },
          { term: 'Section B', description: 'Theory and calculations: 8 questions, answer 5. Worth 280 marks total (56 each). Covers the full Chemistry syllabus.' },
          { term: 'mandatory experiments', description: 'Prescribed experiments including titrations, preparations, tests, and measurements. These form the basis of Section A and can appear in Section B.' }
        ],
        bullets: [
          'Single paper: 3 hours, 400 marks total',
          'Section A: 3 from ~5 experiment questions (120 marks)',
          'Section B: 5 from 8 theory questions (280 marks)',
          'Roughly 15 min per Section A question, 24 min per Section B question'
        ]
      },
      // Section 2: Marking Criteria
      {
        title: 'What the Examiner Rewards',
        eyebrow: '02 // Marking Criteria',
        paragraphs: [
          'Chemistry has one of the highest [[definition densities]] of any Leaving Cert subject. Questions routinely open with "Define...", "What is meant by...", or "State the meaning of..." -- and these carry significant marks. The examiner expects precise, textbook definitions. "An acid is a proton donor" (Bronsted-Lowry definition) is correct; "An acid is something that makes things acidic" is not.',
          'In experiment questions, the examiner rewards [[procedural precision]] just as in Physics. You must name specific chemicals and their concentrations, describe exact steps in the correct order, state what indicator you used and the colour change observed, and list relevant precautions. Generic answers score poorly. For a titration, for example, you need to mention the burette, pipette, conical flask, indicator, endpoint colour change, and the use of a white tile.',
          'For calculation questions in Section B, the marking scheme awards marks for [[correctly balanced equations]], correct mole calculations, and appropriate use of units. Writing the balanced equation at the start of a stoichiometry problem is worth marks in itself. Then showing moles = mass/molar mass, or using the appropriate gas/solution calculations, earns marks at each step.',
          'The examiner also looks for [[chemical accuracy]] in explanations. When explaining why a reaction occurs, you need to reference specific chemical principles -- electronegativity, bond polarity, Le Chatelier\'s principle, or oxidation states. Vague explanations like "it reacts because it wants to be stable" do not earn marks. Specific, technical language does.'
        ],
        highlights: [
          { term: 'definition densities', description: 'Chemistry has an unusually high number of examinable definitions. Learning them precisely is one of the best mark-earning strategies.' },
          { term: 'procedural precision', description: 'Naming exact chemicals, concentrations, equipment, and steps in experiment answers. Generic descriptions score poorly.' },
          { term: 'correctly balanced equations', description: 'Writing and balancing the chemical equation is worth marks before you even begin a calculation. Always include state symbols.' },
          { term: 'chemical accuracy', description: 'Using precise scientific language and referencing specific principles (e.g., electronegativity, Le Chatelier\'s). Vague answers lose marks.' }
        ]
      },
      // Section 3: High-Value Zones
      {
        title: 'Where Your Marks Are',
        eyebrow: '03 // High-Value Zones',
        paragraphs: [
          'Just like Physics, [[Section A]] is your most reliable mark-earner. The mandatory experiments repeat in predictable patterns, and the format is always the same. A student who thoroughly prepares all the experiments can realistically score **100-120 marks** in Section A. That is 30% of the exam from a section that rewards rote preparation rather than deep problem-solving.',
          '[[Organic Chemistry]] is the single most valuable topic in Section B. It appears every year, often across two questions -- one on reactions and mechanisms, another on analysis or structure determination. Organic Chemistry questions follow learnable patterns: functional group tests, preparation methods, and reaction mechanisms (especially the addition, substitution, and elimination reactions). This topic alone can be worth **80-100 marks**.',
          '[[Acids and Bases]] is another high-yield area. Questions on pH calculations, buffer solutions, and acid-base titrations appear frequently. The calculations follow a small number of standard types, and the definitions (pH, acid, base, buffer, conjugate pair) come up repeatedly. Mastering this topic is excellent value for revision time.',
          '[[Definitions across the syllabus]] represent the easiest marks on the entire paper. Chemistry has roughly 50-60 examinable definitions, and they appear throughout Section B. A student who learns all of them by heart using flashcards can pick up **40-50 marks** scattered across the paper with minimal effort. This is the single best return on a few hours of revision.'
        ],
        highlights: [
          { term: 'Section A', description: 'The most predictable and learnable section. Master all mandatory experiments for up to 120 reliable marks.' },
          { term: 'Organic Chemistry', description: 'The highest-value topic in Section B. Learn functional groups, reactions, mechanisms, and tests for a huge mark payoff.' },
          { term: 'Acids and Bases', description: 'pH calculations, buffers, and titrations. A small number of calculation types with high predictability.' },
          { term: 'Definitions across the syllabus', description: 'Roughly 50-60 definitions worth 40-50 marks total. Flashcard revision gives the best return per hour of study.' }
        ]
      },
      // Section 4: Common Pitfalls
      {
        title: 'What Costs You Marks',
        eyebrow: '04 // Common Pitfalls',
        paragraphs: [
          'The most damaging mistake in Chemistry is writing [[unbalanced equations]]. Every time you write a chemical equation, check that the atoms balance on both sides. Unbalanced equations can lose you marks not only on the equation itself but on any subsequent calculation that depends on it. Always include state symbols (s, l, g, aq) -- the examiner checks for these and they are often worth a mark.',
          'In experiment answers, students frequently lose marks by being [[too vague about observations]]. "The solution changed colour" is not enough. You need to say what colour it changed from and to. "The solution changed from colourless to a faint permanent pink" earns full marks for a titration endpoint. The specific colour change is what the examiner is looking for.',
          'Many students struggle with [[mole calculations]] not because the Maths is hard but because they skip steps. The examiner awards marks for: writing the balanced equation, identifying the mole ratio, calculating moles of the known substance, using the ratio to find moles of the unknown, and converting to the required quantity (mass, volume, concentration). Skipping any of these steps costs marks.',
          'Finally, students who have not revised [[Organic Chemistry mechanisms]] often try to bluff their way through. Mechanism questions require you to show the movement of electron pairs using curly arrows, identify intermediates, and explain each step. You cannot improvise this -- either you know the mechanism or you do not. Learn the 4-5 key mechanisms on the syllabus and practise drawing them.'
        ],
        highlights: [
          { term: 'unbalanced equations', description: 'Equations with atoms that do not balance on both sides. Always check balancing and include state symbols (s, l, g, aq).' },
          { term: 'too vague about observations', description: 'Not specifying exact colour changes, precipitate colours, or gas tests. The examiner needs precise observations.' },
          { term: 'mole calculations', description: 'Students skip steps in stoichiometry. Show: balanced equation, mole ratio, moles of known, moles of unknown, final conversion.' },
          { term: 'Organic Chemistry mechanisms', description: 'Curly arrow mechanisms cannot be improvised. Learn the key mechanisms on the syllabus and practise drawing them from memory.' }
        ]
      },
      // Section 5: Study Techniques
      {
        title: 'How to Study Chemistry',
        eyebrow: '05 // Study Techniques',
        paragraphs: [
          'Split your Chemistry revision into three streams: [[experiments]], [[definitions]], and [[theory and calculations]]. Each requires a different study approach, and you should work on all three in every study session rather than spending an entire evening on just one.',
          'For experiments, create a [[standard write-up template]] for each mandatory experiment. Include: diagram, chemicals and equipment, step-by-step procedure, observations, precautions, and how results are calculated. Write these out from memory repeatedly until you can reproduce them cleanly. Section A is pure recall -- the more you practise writing, the more marks you earn.',
          'For definitions, use [[active recall flashcards]]. Write the term on one side and the precise definition on the other. Test yourself daily, removing cards from the deck only when you can state the definition perfectly three times in a row. Aim to have all 50-60 definitions memorised at least two weeks before the exam.',
          'For theory and calculations, work through past paper questions [[topic by topic]]. Start with Organic Chemistry and Acids & Bases (your highest-value topics), then cover Stoichiometry, Equilibrium, Rates of Reaction, and Electrochemistry. For each calculation type, learn the standard method and practise until you can execute it without reference to notes. Mark your answers using the official marking scheme.'
        ],
        highlights: [
          { term: 'experiments', description: 'One of three revision streams. Create write-up templates and practise reproducing them from memory.' },
          { term: 'definitions', description: 'The second revision stream. Use flashcards with active recall to memorise all 50-60 syllabus definitions.' },
          { term: 'theory and calculations', description: 'The third stream. Work through past papers topic by topic, starting with the highest-value areas.' },
          { term: 'standard write-up template', description: 'A structured format for each experiment: diagram, chemicals, procedure, observations, precautions, results.' },
          { term: 'active recall flashcards', description: 'Flashcards tested daily using the cover-and-recall method. Remove cards only when you can state the definition perfectly.' },
          { term: 'topic by topic', description: 'Group past paper questions by topic and work through them sequentially to identify patterns and build fluency.' }
        ]
      },
      // Section 6: Action Plan
      {
        title: 'Your Chemistry Action Plan',
        eyebrow: '06 // Action Plan',
        paragraphs: [
          'In week one, focus on Section A. List every mandatory experiment, write out a one-page summary for each, and practise reproducing them from memory. In parallel, begin making definition flashcards -- aim to cover all definitions within the first two weeks of revision. Test yourself on definitions for 10 minutes at the start of every study session.',
          'In weeks two and three, tackle Section B topic by topic. Spend one session on Organic Chemistry reactions and mechanisms, one on Acids & Bases calculations, one on Stoichiometry, and so on. For each topic, do at least 4-5 past paper questions and mark them against the official scheme. Keep a running list of your weakest areas and revisit them.',
          'In the final week, do two full timed practice papers (3 hours each) and mark them. Review your experiment write-ups one more time, run through your flashcards, and rework any questions you scored below 60% on. On exam day, allocate roughly 45 minutes for Section A and 2 hours 15 minutes for Section B.'
        ],
        highlights: [],
        commitmentText: 'This week, I will create definition flashcards for one complete Chemistry topic (e.g., Acids and Bases) and test myself on them every day for 10 minutes using active recall.'
      }
    ]
  },

  // ────────────────────────────────────────────────────────────────
  //  BIOLOGY
  // ────────────────────────────────────────────────────────────────
  'biology': {
    subjectId: 'biology',
    subjectName: 'Biology',
    moduleNumber: '12',
    moduleTitle: 'Mastering Biology',
    moduleSubtitle: 'Your Complete Biology Exam Guide',
    moduleDescription: 'Understand how the Biology exam really works, why some topics are worth far more than others, and how to write answers the examiner can actually give marks to.',
    themeName: 'lime',
    sections: [
      // Section 1: Exam Structure
      {
        title: 'How Biology Actually Works',
        eyebrow: '01 // Exam Structure',
        paragraphs: [
          'The Biology Leaving Cert is a **single exam paper** lasting **3 hours** and worth **400 marks**. It is divided into three sections: [[Section A]] (short questions), [[Section B]] (short answer and experiment questions), and [[Section C]] (long questions). Each section has a distinct format and tests different skills, so your preparation needs to cover all three.',
          '[[Section A]] is worth **100 marks** and contains **6 short questions** -- you must answer **5 of them**. Each question is worth **20 marks**. These are typically based on diagrams, experiments, data interpretation, and basic recall. They are shorter and more accessible than the other sections, but they still demand precise knowledge.',
          '[[Section B]] is worth **100 marks** and contains **3 questions** -- you must answer **2 of them**. Each question is worth **50 marks**. This section focuses on [[mandatory experiments]] and practical biology. Questions ask you to describe experimental procedures, interpret results, draw diagrams of apparatus, and explain scientific reasoning. Section B is where your experiment knowledge is tested most directly.',
          '[[Section C]] is worth **200 marks** and contains **6 long questions** -- you must answer **4 of them**. Each question is worth **50 marks**. These are the big essay-style questions covering major syllabus topics: Ecology, Cell Biology, Genetics, Plant Biology, Human Biology (including the digestive, circulatory, respiratory, excretory, and reproductive systems), and Microbiology. Section C is where most of your marks will come from -- and where the best-prepared students pull ahead.'
        ],
        highlights: [
          { term: 'Section A', description: 'Short questions: 6 available, answer 5. Worth 100 marks (20 each). Tests diagrams, data, experiments, and quick recall.' },
          { term: 'Section B', description: 'Experiment and short-answer questions: 3 available, answer 2. Worth 100 marks (50 each). Focuses on mandatory experiments.' },
          { term: 'Section C', description: 'Long essay questions: 6 available, answer 4. Worth 200 marks (50 each). Major topics from the full syllabus.' },
          { term: 'mandatory experiments', description: 'A set of prescribed experiments covering food tests, enzyme activity, osmosis, photosynthesis, ecology fieldwork, and more.' }
        ],
        bullets: [
          'Single paper: 3 hours, 400 marks total',
          'Section A: 5 from 6 short questions (100 marks)',
          'Section B: 2 from 3 experiment questions (100 marks)',
          'Section C: 4 from 6 long questions (200 marks)'
        ]
      },
      // Section 2: Marking Criteria
      {
        title: 'What the Examiner Rewards',
        eyebrow: '02 // Marking Criteria',
        paragraphs: [
          'Biology is a [[detail-driven subject]]. The marking scheme awards marks for specific facts, named examples, and precise terminology. Vague answers that demonstrate general understanding but lack specific terms will consistently underperform. The examiner is literally counting correct points -- each distinct, valid point you make earns a mark or set of marks.',
          'In Section C long questions, answers are marked using a [[points-based system]]. Each question lists a set of marking points (specific facts, terms, or explanations) and the student earns marks for each correct point they include. This means longer, more detailed answers tend to score higher -- but only if the details are correct and relevant. Padding your answer with irrelevant information earns nothing.',
          'The examiner places high value on [[correct biological terminology]]. Writing "mitosis" instead of "cell division," "alveoli" instead of "air sacs," or "transpiration" instead of "water loss from leaves" is the difference between full marks and partial marks. Using the correct scientific terms shows the examiner you truly understand the content rather than just having a vague awareness.',
          'For experiment questions, the same rules apply as in Physics and Chemistry: [[name your equipment]], describe each step precisely, state your results, and explain what they demonstrate. But Biology experiments also often require you to include a [[control experiment]] -- describing what you kept the same and what you changed. Forgetting the control is one of the most common ways students lose marks in Section B.'
        ],
        highlights: [
          { term: 'detail-driven subject', description: 'Marks are awarded for specific facts and precise terms, not general understanding. The examiner counts correct points.' },
          { term: 'points-based system', description: 'Section C answers are marked by counting distinct valid biological points. More correct detail means more marks.' },
          { term: 'correct biological terminology', description: 'Using precise scientific terms (e.g., "alveoli" not "air sacs") earns more marks and demonstrates real understanding.' },
          { term: 'name your equipment', description: 'In experiment answers, specify exact equipment and materials used. "Beaker," "water bath at 37 degrees C," not "container."' },
          { term: 'control experiment', description: 'Describing what was kept constant and what was changed. Essential for earning full marks on experiment questions.' }
        ]
      },
      // Section 3: High-Value Zones
      {
        title: 'Where Your Marks Are',
        eyebrow: '03 // High-Value Zones',
        paragraphs: [
          '[[Section C]] is where 50% of your marks are. Four questions at 50 marks each means Section C alone determines whether you get a H3 or a H5. The topics that appear most frequently and carry the most weight are: **Human Biology** (the digestive, circulatory, respiratory, and excretory systems), **Genetics** (Mendelian genetics, DNA, and gene expression), and **Ecology** (food webs, nutrient recycling, and ecological fieldwork). These three areas should be your top revision priorities.',
          '[[Mandatory experiments]] are your next highest-value zone. They are tested directly in Section B and frequently appear in Section A as well. There are approximately 20 mandatory experiments on the syllabus, covering food tests (Benedict\'s, iodine, biuret), enzyme experiments, osmosis demonstrations, photosynthesis and respiration investigations, and ecological fieldwork techniques. A student who knows all of them can expect to score well across both Sections A and B.',
          '[[Section A]] short questions are often undervalued by students, but they add up fast. Five questions at 20 marks each is **100 marks** -- a quarter of the entire paper. These questions tend to test diagrams (e.g., label a cell, identify parts of the heart), experiment knowledge, and data interpretation. They reward broad knowledge rather than deep expertise, making them ideal for students who have covered the full syllabus.',
          'Within Section C, the [[Ecology question]] has been one of the most predictable and accessible questions in recent years. It frequently asks about food webs, nutrient recycling (carbon or nitrogen cycle), ecological terms and definitions, and the biotic/abiotic factors in an ecosystem. Students who know their ecology vocabulary and can describe a fieldwork technique can reliably score 40-50 marks here.'
        ],
        highlights: [
          { term: 'Section C', description: 'Worth 200 marks (50% of the exam). Four long questions on major syllabus topics. Your biggest marks opportunity.' },
          { term: 'Mandatory experiments', description: 'Approximately 20 experiments tested in Sections A and B. Thorough preparation here secures up to 200 marks across the paper.' },
          { term: 'Section A', description: 'Short questions worth 100 marks total. Tests diagrams, data, and broad recall. Good coverage of the syllabus pays off here.' },
          { term: 'Ecology question', description: 'One of the most predictable questions in Section C. Learn ecology vocabulary, nutrient cycles, and fieldwork techniques.' }
        ]
      },
      // Section 4: Common Pitfalls
      {
        title: 'What Costs You Marks',
        eyebrow: '04 // Common Pitfalls',
        paragraphs: [
          'The biggest mark-killer in Biology is writing [[vague, general answers]] instead of specific, detailed ones. "The heart pumps blood around the body" is not worth marks in Section C. "The left ventricle contracts, forcing oxygenated blood through the aorta to the body\'s tissues via the systemic circulation" is. The examiner is counting distinct, correct points. Every specific term you include is potentially another mark.',
          'Students consistently lose marks by [[not answering the question asked]]. Biology questions often use specific command words: "Describe" means give a detailed account; "Explain" means give reasons why; "State" means give a brief, precise answer. Writing a long description when the question asks you to "explain" means you may earn no marks at all for that part, because you have not addressed the actual question.',
          'In experiment questions, the most common error is [[forgetting the control]]. If you are describing how you tested for starch in a leaf, you need to mention that you also tested a leaf that was kept in the dark (the control). Without describing the control and why it matters, you cannot earn full marks on most experiment questions.',
          'Finally, poor [[time allocation in Section C]] costs students dearly. Some students write 3 pages for their favourite topic and then have only 10 minutes left for their fourth question. Each Section C question is worth the same 50 marks, so spending 40 minutes on one and 10 minutes on another is poor strategy. Aim for roughly **20-22 minutes per long question** and move on.'
        ],
        highlights: [
          { term: 'vague, general answers', description: 'Answers that show general awareness but lack specific terms and detail. The examiner counts precise, named points.' },
          { term: 'not answering the question asked', description: 'Ignoring the command word (Describe, Explain, State) and writing the wrong type of answer. Read the question carefully.' },
          { term: 'forgetting the control', description: 'Experiment answers that do not describe the control setup lose significant marks. Always state what you kept constant.' },
          { term: 'time allocation in Section C', description: 'Spending too long on one question and rushing others. Each question is 50 marks -- allocate time equally.' }
        ]
      },
      // Section 5: Study Techniques
      {
        title: 'How to Study Biology',
        eyebrow: '05 // Study Techniques',
        paragraphs: [
          'Biology is primarily a **recall-based subject**. The exam rewards students who can reproduce specific facts, definitions, diagrams, and experiment procedures. This means your study strategy should centre on [[active recall]] -- testing yourself on what you know rather than passively re-reading notes. Flashcards, blank diagrams to label, and practice questions are far more effective than highlighting textbooks.',
          'Create [[topic summary sheets]] for each major area: one page per system in Human Biology, one page for Genetics, one for Ecology, one for Cell Biology, one for Plant Biology, and one for Microbiology. Each sheet should include: key definitions, labelled diagrams, named examples, and important processes described step by step. These sheets become your revision backbone.',
          'For experiments, use the same approach as the science subjects above: write a [[structured experiment summary]] for each mandatory experiment (diagram, equipment, procedure, observations, control, conclusion). Practise writing these out from memory. The experiment knowledge tested in Sections A and B is pure recall -- if you have practised writing them, you will score well.',
          'Use [[past paper practice]] as your primary assessment tool. Work through Section C questions by writing full answers under timed conditions (20-22 minutes each). Then mark your answers against the marking scheme, counting how many distinct points you made. This tells you exactly where your knowledge gaps are. Any topic where you score below 35/50 needs more focused revision.'
        ],
        highlights: [
          { term: 'active recall', description: 'Testing yourself on material rather than re-reading it. Use flashcards, blank diagrams, and practice questions.' },
          { term: 'topic summary sheets', description: 'One-page summaries per topic with definitions, diagrams, examples, and key processes. Your core revision resource.' },
          { term: 'structured experiment summary', description: 'A standard write-up for each mandatory experiment: diagram, equipment, procedure, observations, control, conclusion.' },
          { term: 'past paper practice', description: 'Write full Section C answers under timed conditions and mark them against the scheme to identify knowledge gaps.' }
        ]
      },
      // Section 6: Action Plan
      {
        title: 'Your Biology Action Plan',
        eyebrow: '06 // Action Plan',
        paragraphs: [
          'Start by making a checklist of all mandatory experiments and all Section C topics. Tick off each one as you create a summary sheet and can reproduce it from memory. Prioritise **Human Biology**, **Genetics**, and **Ecology** first -- these cover the most Section C marks. In parallel, start your definition flashcards and test yourself for 10 minutes at the beginning of every study session.',
          'Once you have covered the major topics, practise writing full Section C answers under timed conditions. Do at least 2-3 past paper long questions per study session, mark them yourself, and count the points. Where you are losing marks, go back to your summary sheet and fill in the missing details. Repeat this cycle until you can consistently score 40+ on Section C questions.',
          'In the final two weeks, do two complete timed papers (3 hours each) and mark them fully. Review your experiment summaries, run through all your flashcards, and focus your final sessions on your weakest topics. On exam day, read all questions before choosing -- especially in Section C, where picking the right 4 questions can make or break your grade.'
        ],
        highlights: [],
        commitmentText: 'This week, I will create topic summary sheets for 3 major Biology topics (Human Biology systems, Genetics, and Ecology) and test myself on their key definitions using active recall.'
      }
    ]
  },

  // ────────────────────────────────────────────────────────────────
  //  COMPUTER SCIENCE
  // ────────────────────────────────────────────────────────────────
  'computer-science': {
    subjectId: 'computer-science',
    subjectName: 'Computer Science',
    moduleNumber: '13',
    moduleTitle: 'Mastering Computer Science',
    moduleSubtitle: 'Your Complete CS Exam Guide',
    moduleDescription: 'Navigate the Computer Science exam and coursework -- understand the ALT project, the written paper structure, and how to maximise marks across both.',
    themeName: 'sky',
    sections: [
      // Section 1: Exam Structure
      {
        title: 'How Computer Science Actually Works',
        eyebrow: '01 // Exam Structure',
        paragraphs: [
          'Computer Science is unique among Leaving Cert subjects because it has a significant **coursework component**. Your final grade is made up of two parts: the [[Applied Learning Task]] (ALT), worth **30%** of your overall mark, and the [[written exam]], worth **70%**. Both components must be taken seriously, but the ALT is completed before the exam and represents a major opportunity to bank marks early.',
          'The [[Applied Learning Task]] is a substantial project completed during 5th or 6th year. You are given a brief by the SEC and must design, develop, and document a computational solution. The ALT assesses your ability to apply programming, computational thinking, and problem-solving to a real-world scenario. It is submitted as a portfolio including your code, documentation, and a reflective journal. The marking criteria emphasise [[process and documentation]] as much as the final product.',
          'The [[written exam]] is a **2-hour paper** worth **70%** of your grade. It tests your understanding of computational thinking, programming concepts, algorithms, data structures, computer systems, and the societal impact of computing. The paper typically contains a mix of short-answer questions, code-reading questions, code-writing questions, and longer structured questions.',
          'Because the ALT is worth 30%, a strong project can significantly boost your overall grade. A student who scores very well on the ALT effectively needs a lower exam mark to reach each grade boundary. This makes the ALT one of the most strategically important components in your entire Leaving Cert.'
        ],
        highlights: [
          { term: 'Applied Learning Task', description: 'A coursework project worth 30% of your grade. Involves designing and coding a computational solution to a given brief.' },
          { term: 'written exam', description: 'A 2-hour exam paper worth 70% of your grade. Covers computational thinking, programming, algorithms, data structures, and more.' },
          { term: 'process and documentation', description: 'The ALT is marked on your development process and documentation as much as the final code. Keep a detailed journal.' }
        ],
        bullets: [
          'ALT coursework: 30% of final grade (completed during the year)',
          'Written exam: 2 hours, 70% of final grade',
          'Exam covers: computational thinking, programming, algorithms, data structures, computer systems',
          'Strong ALT performance can significantly offset a weaker exam result'
        ]
      },
      // Section 2: Marking Criteria
      {
        title: 'What the Examiner Rewards',
        eyebrow: '02 // Marking Criteria',
        paragraphs: [
          'For the ALT, the examiner rewards a clear [[development process]]. This means showing that you planned your solution before coding it, tested it systematically, iterated on your design, and reflected on your decisions. Students who jump straight into coding and submit a working program but no documentation or planning evidence will score poorly. The journal and portfolio are as important as the code itself.',
          'In the ALT, [[code quality]] matters but it is not just about whether the program works. The examiner looks for: clear variable naming, use of functions and modularity, comments explaining your logic, appropriate use of data structures, and evidence that you tested edge cases. A simple, well-structured program with clear documentation often scores higher than a complex program with messy code and no explanation.',
          'On the written exam, the examiner rewards [[precise technical vocabulary]]. Questions about algorithms expect you to use terms like "time complexity," "iteration," "recursion," "sorting," and "searching" correctly. Questions about data structures expect you to distinguish between arrays, lists, stacks, queues, and dictionaries with specific examples.',
          'For code-writing questions on the exam, the examiner values [[logical correctness]] over syntactic perfection. If your pseudocode or code demonstrates the correct logic and approach but has a minor syntax error, you will typically still earn most of the marks. However, if your logic is fundamentally wrong -- even if the syntax looks right -- you will score poorly. Focus on getting the algorithm right first.'
        ],
        highlights: [
          { term: 'development process', description: 'Planning, iterating, testing, and reflecting. The ALT rewards the journey as much as the destination.' },
          { term: 'code quality', description: 'Clear naming, modularity, comments, appropriate data structures, and edge-case testing. Well-structured beats complex.' },
          { term: 'precise technical vocabulary', description: 'Using correct CS terminology (time complexity, recursion, iteration, etc.) in exam answers.' },
          { term: 'logical correctness', description: 'Getting the algorithm and logic right matters more than perfect syntax in code-writing questions.' }
        ]
      },
      // Section 3: High-Value Zones
      {
        title: 'Where Your Marks Are',
        eyebrow: '03 // High-Value Zones',
        paragraphs: [
          'The [[ALT project]] at 30% of your total grade is the single biggest marks opportunity you have control over before exam day. Unlike the exam, you have weeks to work on it, can get feedback from your teacher, and can iterate until it is right. Investing serious time in the ALT is one of the smartest strategic moves in the entire Leaving Cert. Aim for an ALT score that puts you ahead before you even sit the exam.',
          'On the written exam, [[programming and algorithms]] questions are the highest-value section. These test your ability to read code, trace through algorithms, write pseudocode, and solve problems computationally. Students who have practised coding regularly throughout the year find these questions significantly easier than those who relied on theory alone. Practising actual coding -- writing programs, debugging, and solving problems -- is the best preparation.',
          '[[Computational thinking]] questions test your ability to decompose problems, recognise patterns, abstract away unnecessary detail, and design algorithmic solutions. These questions are often more accessible than they look because they test a way of thinking rather than specific knowledge. If you practise breaking down problems step by step, you can score well even on unfamiliar problem types.',
          'Questions on [[computer systems and societal impact]] tend to be the most accessible for students who have not been strong coders. These cover topics like hardware vs software, networks, data representation, cybersecurity, and the ethical/social implications of technology. They reward clear, structured writing with specific examples rather than coding ability.'
        ],
        highlights: [
          { term: 'ALT project', description: 'Worth 30% of your final grade and completed before the exam. The biggest controllable marks opportunity in CS.' },
          { term: 'programming and algorithms', description: 'The highest-value section on the written exam. Regular coding practice is the best preparation.' },
          { term: 'Computational thinking', description: 'Problem decomposition, pattern recognition, and abstraction. Tests thinking skills rather than memorisation.' },
          { term: 'computer systems and societal impact', description: 'Hardware, networks, data, ethics. More accessible for students who are stronger in theory than coding.' }
        ]
      },
      // Section 4: Common Pitfalls
      {
        title: 'What Costs You Marks',
        eyebrow: '04 // Common Pitfalls',
        paragraphs: [
          'The biggest mark-killer in CS is [[neglecting the ALT documentation]]. Many students build a working program but submit thin documentation -- no planning diagrams, no testing evidence, no reflective journal entries. The ALT is not just marked on the final product. The SEC marking criteria explicitly allocate significant marks to the development process, and students who skip this documentation are throwing away easy marks.',
          'On the written exam, students lose marks by [[writing vague explanations]] when precise technical language is expected. "The program goes through the list and finds the biggest number" is not as strong as "The algorithm iterates through the array, comparing each element to a running maximum, and returns the largest value." Using correct terminology demonstrates genuine understanding.',
          'In code-writing questions, the most common error is [[not planning before coding]]. Students who start writing code immediately often produce tangled, incorrect logic. Taking 60 seconds to sketch out the steps (in plain English or pseudocode) before writing the actual code dramatically improves the quality and correctness of your answer.',
          'Finally, students who [[do not practise coding regularly]] throughout the year find the exam extremely difficult. CS is a skills-based subject -- you cannot cram programming ability in the last few weeks. The students who score best on the code-reading and code-writing questions are those who have been writing and debugging code consistently all year. Start early and code often.'
        ],
        highlights: [
          { term: 'neglecting the ALT documentation', description: 'Submitting code without planning, testing evidence, or reflective journal. Documentation marks are significant and easy to earn.' },
          { term: 'writing vague explanations', description: 'Using imprecise language instead of correct CS terminology. Be specific: "iterates," "time complexity," "data structure."' },
          { term: 'not planning before coding', description: 'Jumping into code-writing without sketching the algorithm first. A 60-second plan prevents logic errors.' },
          { term: 'do not practise coding regularly', description: 'Programming ability cannot be crammed. Regular coding practice throughout the year is essential.' }
        ]
      },
      // Section 5: Study Techniques
      {
        title: 'How to Study Computer Science',
        eyebrow: '05 // Study Techniques',
        paragraphs: [
          'CS study should be split between [[active coding practice]] and [[theory revision]]. For coding, spend at least 2-3 sessions per week actually writing programs. Use platforms like repl.it, CodeHS, or just a simple text editor and terminal. Solve small problems: sort a list, search for an item, build a simple calculator, parse a string. The more problems you solve, the more fluent you become.',
          'For theory, make [[concept summary cards]] for each topic: algorithms (searching, sorting, time complexity), data structures (arrays, lists, stacks, queues, trees), computer systems (CPU, memory, storage, networking), and societal issues (privacy, security, AI ethics). Each card should include a definition, a diagram or example, and a past paper question that tests it.',
          'Practise [[code tracing]] regularly. The exam will give you a block of code and ask what it outputs, or ask you to identify an error. The only way to get good at this is practice: take a piece of code, trace through it line by line (writing down variable values at each step), and predict the output. Then run the code to check. This skill transfers directly to the exam.',
          'For the ALT, keep a [[project journal]] from day one. Every time you work on your project, write a short entry: what you did, what decisions you made and why, what problems you encountered, and how you solved them. This journal becomes the core of your documentation and is much easier to write as you go than to reconstruct at the end.'
        ],
        highlights: [
          { term: 'active coding practice', description: 'Writing actual programs 2-3 times per week. Solve small problems to build fluency in programming logic.' },
          { term: 'theory revision', description: 'Concept cards covering algorithms, data structures, computer systems, and societal impact.' },
          { term: 'concept summary cards', description: 'One card per concept with definition, diagram/example, and a linked past paper question.' },
          { term: 'code tracing', description: 'Stepping through code line by line, tracking variable values, and predicting output. A key exam skill.' },
          { term: 'project journal', description: 'A running log of your ALT development process. Write entries as you work, not at the end.' }
        ]
      },
      // Section 6: Action Plan
      {
        title: 'Your Computer Science Action Plan',
        eyebrow: '06 // Action Plan',
        paragraphs: [
          'If you have not started your ALT, start now. Create a project plan, begin your reflective journal, and aim to have a working prototype at least 4 weeks before the submission deadline. Document every step as you go -- screenshots, code snippets, design decisions, and test results. The documentation is worth as much as the code itself.',
          'For the written exam, build a revision schedule that alternates between **coding practice** (solving problems, tracing code) and **theory review** (concept cards, past paper questions). Aim for at least 3 coding sessions and 2 theory sessions per week in the lead-up to the exam. Work through every available past paper, as the question styles and topics are still settling into predictable patterns.',
          'In the final two weeks, focus on timed practice: do a full 2-hour paper under exam conditions, mark it, and identify gaps. Spend your remaining sessions filling those gaps. On exam day, read every question before starting, answer the ones you are most confident in first, and remember that clear, well-explained logic earns more marks than clever but unclear code.'
        ],
        highlights: [],
        commitmentText: 'This week, I will complete one coding challenge per day (e.g., sort a list, search for an element, reverse a string) and write a 200-word reflective journal entry for my ALT project.'
      }
    ]
  },

  // ────────────────────────────────────────────────────────────────
  //  AGRICULTURAL SCIENCE
  // ────────────────────────────────────────────────────────────────
  'ag-science': {
    subjectId: 'ag-science',
    subjectName: 'Agricultural Science',
    moduleNumber: '14',
    moduleTitle: 'Mastering Ag Science',
    moduleSubtitle: 'Your Complete Ag Science Guide',
    moduleDescription: 'Crack the Agricultural Science exam -- from the CBAs and mandatory experiments to the written paper -- and learn what the examiner rewards.',
    themeName: 'yellow',
    sections: [
      // Section 1: Exam Structure
      {
        title: 'How Agricultural Science Actually Works',
        eyebrow: '01 // Exam Structure',
        paragraphs: [
          'Agricultural Science has undergone significant syllabus changes in recent years, reflecting its move to the new specification. The assessment consists of a **written exam paper** lasting **2 hours and 30 minutes** and [[Classroom-Based Assessments]] (CBAs) completed during the course. The written exam is the primary determinant of your Leaving Cert grade, but the CBAs build essential practical knowledge that feeds directly into the exam.',
          'The written paper is divided into three sections. [[Section A]] contains **short questions** testing broad recall across the syllabus -- definitions, diagrams, and quick calculations. [[Section B]] focuses on **experiments and investigations**, testing your knowledge of the [[mandatory experiments]] and practical procedures. [[Section C]] contains **long answer questions** that require detailed, structured responses on major syllabus topics.',
          'The syllabus covers four main strands: [[Soils, Crops and the Environment]], [[Animal Science and Production]], [[Food Science and Human Health]], and [[Sustainability and the Agri-Food Industry]]. Questions can draw from any of these strands, and the best-performing students are those who have covered all four comprehensively rather than betting on a few topics appearing.',
          'The CBAs include practical investigations and research activities completed during 5th and 6th year. While the CBAs themselves do not carry a direct percentage of the final exam mark in the same way as the CS ALT, the [[practical knowledge and skills]] developed through the CBAs are directly examinable on the written paper. Students who engaged seriously with their CBAs have a significant advantage in Sections A and B of the exam.'
        ],
        highlights: [
          { term: 'Classroom-Based Assessments', description: 'Practical investigations and research activities completed during the course. The skills developed are directly tested on the written exam.' },
          { term: 'Section A', description: 'Short questions testing broad recall: definitions, diagrams, and quick calculations across all syllabus strands.' },
          { term: 'Section B', description: 'Experiment and investigation questions. Tests your knowledge of mandatory experiments and practical procedures.' },
          { term: 'Section C', description: 'Long answer questions requiring detailed, structured responses on major agricultural science topics.' },
          { term: 'mandatory experiments', description: 'Prescribed experiments on soils, plant growth, food testing, and animal science that form the basis of Section B questions.' },
          { term: 'Soils, Crops and the Environment', description: 'Soil types, nutrients, crop growth, pest management, and environmental impact. A major syllabus strand.' },
          { term: 'Animal Science and Production', description: 'Animal nutrition, reproduction, genetics, breeding, and livestock management systems.' },
          { term: 'Food Science and Human Health', description: 'Food composition, food processing, nutrition, food safety, and the link between diet and health.' },
          { term: 'Sustainability and the Agri-Food Industry', description: 'Sustainable farming practices, the food chain, agricultural economics, and environmental stewardship.' },
          { term: 'practical knowledge and skills', description: 'Hands-on experience from CBAs feeds directly into exam questions, especially in Sections A and B.' }
        ],
        bullets: [
          'Written paper: 2.5 hours with three sections',
          'Section A: Short questions (broad recall)',
          'Section B: Experiments and investigations',
          'Section C: Long structured questions',
          'CBAs completed during the course build exam-relevant skills'
        ]
      },
      // Section 2: Marking Criteria
      {
        title: 'What the Examiner Rewards',
        eyebrow: '02 // Marking Criteria',
        paragraphs: [
          'Agricultural Science rewards students who combine **scientific precision** with **practical agricultural knowledge**. The examiner is looking for answers that demonstrate both theoretical understanding and awareness of real-world farming and food production. Writing "nitrogen is important for plant growth" is too vague. Writing "nitrogen promotes vegetative growth and is a key component of chlorophyll and amino acids" shows the depth the examiner expects.',
          'In Section B experiment questions, the examiner applies the same standards as in the other sciences: [[specific procedural detail]]. You must name the chemicals, describe the steps in order, state your results and observations precisely, and explain what your results demonstrate. For Ag Science experiments specifically, you also need to show awareness of [[agricultural context]] -- how the experiment relates to farming practice.',
          'Section C long answers are marked on a [[points-based system]] similar to Biology. The examiner has a list of valid marking points, and you earn marks for each correct, distinct point you make. This means that well-structured answers with clear, separate points score better than long, rambling paragraphs. Use numbered points or separate paragraphs for each distinct piece of information.',
          'The examiner values [[real-world examples]] highly. When discussing crop management, name specific crops (e.g., barley, potatoes, grass silage). When discussing animal production, name specific breeds and systems (e.g., Friesian dairy cattle, spring calving system). Specific examples demonstrate genuine knowledge and earn marks that generic answers miss.'
        ],
        highlights: [
          { term: 'specific procedural detail', description: 'Name chemicals, describe steps precisely, state observations clearly. Vague experiment descriptions score poorly.' },
          { term: 'agricultural context', description: 'Relating experiments and theory to real farming practice. Shows the examiner you understand the practical relevance.' },
          { term: 'points-based system', description: 'Section C answers are marked by counting valid points. Structure your answer clearly with distinct, separate points.' },
          { term: 'real-world examples', description: 'Naming specific crops, breeds, farming systems, and practices. Specific examples earn marks that generic answers miss.' }
        ]
      },
      // Section 3: High-Value Zones
      {
        title: 'Where Your Marks Are',
        eyebrow: '03 // High-Value Zones',
        paragraphs: [
          '[[Section B experiments]] are the most predictable and learnable part of the paper. The mandatory experiments cover a finite set of procedures -- soil testing (pH, organic matter, water content), plant growth experiments, food tests (starch, protein, fat, vitamin C), and animal science investigations. Learning these experiments thoroughly is the fastest way to secure reliable marks. The format is always the same: describe, diagram, results, conclusion.',
          '[[Section A short questions]] are a goldmine for well-prepared students. They test breadth rather than depth -- a little knowledge about every topic goes a long way. Definitions, labelled diagrams, and simple calculations make up most of Section A. Students who have covered the full syllabus (even superficially) consistently outperform those who know three topics inside out but have gaps elsewhere.',
          'In Section C, [[Animal Science]] and [[Soils and Crops]] are the highest-value topics. Animal Science covers nutrition, reproduction, genetics, and production systems -- it is a rich area with many examinable points. Soils and Crops covers soil types, nutrient management, crop establishment, and pest/disease control. Together, these two strands typically account for the majority of Section C marks.',
          '[[Food Science]] questions have become increasingly important under the new specification. Questions on food composition, processing, preservation, and the relationship between diet and health appear regularly. Students who understand the science behind food production (not just farming) have access to a whole set of questions that others may struggle with.'
        ],
        highlights: [
          { term: 'Section B experiments', description: 'A finite set of mandatory experiments with predictable exam formats. Learn them all for reliable, scorable marks.' },
          { term: 'Section A short questions', description: 'Tests breadth of knowledge. Covering the full syllabus -- even lightly -- pays dividends in this section.' },
          { term: 'Animal Science', description: 'Nutrition, reproduction, genetics, and production systems. A rich topic with many examinable marking points.' },
          { term: 'Soils and Crops', description: 'Soil types, nutrients, crop management, and pest control. Frequently the highest-weighted area in Section C.' },
          { term: 'Food Science', description: 'Food composition, processing, preservation, and diet-health links. Increasingly important under the new specification.' }
        ]
      },
      // Section 4: Common Pitfalls
      {
        title: 'What Costs You Marks',
        eyebrow: '04 // Common Pitfalls',
        paragraphs: [
          'The biggest mistake in Ag Science is assuming that **common sense and farm knowledge** are enough. Students from farming backgrounds sometimes think they can answer questions based on practical experience alone. But the examiner wants [[scientific terminology]], not colloquial descriptions. "The soil was wet and sticky" is not the same as "the soil had a high clay content and poor drainage." Always use the scientific language from the syllabus.',
          'In experiment questions, students lose marks by [[not quantifying their results]]. "The plant grew taller in the light" is weaker than "the plant in the light grew to 15cm over 10 days, while the plant in the dark grew to only 3cm." Including actual numbers (even approximate ones from your experiment) demonstrates rigour and earns extra marks.',
          'Section C answers often suffer from [[poor structure]]. Students write one long paragraph and expect the examiner to find the marking points buried in it. Instead, separate your answer into clear, distinct points or short paragraphs. Each new point should be clearly identifiable. This makes the examiner\'s job easier and ensures you get credit for every valid point.',
          'Finally, students often [[neglect the newer syllabus strands]] -- particularly Food Science and Sustainability. These strands are fully examinable and questions on them appear regularly. Students who only revise the traditional topics (soils, crops, animals) are limiting their options on the exam paper and missing marks in Section A.'
        ],
        highlights: [
          { term: 'scientific terminology', description: 'Using precise scientific language from the syllabus, not everyday farming terms. "Clay content" not "sticky soil."' },
          { term: 'not quantifying their results', description: 'Experiment answers without numbers or measurements. Include actual data wherever possible to earn full marks.' },
          { term: 'poor structure', description: 'Long, unstructured paragraphs where marking points are hard to find. Use clear, separated points instead.' },
          { term: 'neglect the newer syllabus strands', description: 'Food Science and Sustainability are fully examinable. Ignoring them limits your question choices on the paper.' }
        ]
      },
      // Section 5: Study Techniques
      {
        title: 'How to Study Agricultural Science',
        eyebrow: '05 // Study Techniques',
        paragraphs: [
          'Ag Science revision should be organised around the **four syllabus strands**: Soils/Crops/Environment, Animal Science, Food Science, and Sustainability. Create a [[revision checklist]] for each strand listing every topic, and tick each one off as you study it. This ensures you cover the full syllabus and do not leave gaps that cost you marks in Section A.',
          'For experiments, use the same [[structured write-up approach]] as the other sciences. For each mandatory experiment, prepare: a labelled diagram, equipment and materials list, step-by-step procedure, results (with numbers where possible), conclusion, and agricultural relevance. Practise writing these from memory until they are automatic. This preparation pays off directly in Section B.',
          'For Section C long questions, use [[past paper practice with self-marking]]. Write full answers to past questions under timed conditions, then mark them against the marking scheme (where available) or your textbook. Count the number of distinct, valid points in your answer. If you are consistently making fewer than 8-10 points per question, you need to add more specific detail to your answers.',
          'Make [[agricultural vocabulary flashcards]] covering definitions from every strand. Ag Science has a large number of specific terms (e.g., leaching, nitrification, colostrum, pasteurisation, silage, photosynthesis, sustainability). The examiner expects these terms to appear in your answers. Flashcard revision for 10 minutes at the start of each study session builds your vocabulary steadily over time.'
        ],
        highlights: [
          { term: 'revision checklist', description: 'A strand-by-strand list of every topic on the syllabus. Tick each off as you study it to avoid gaps.' },
          { term: 'structured write-up approach', description: 'A standard template for experiment revision: diagram, equipment, procedure, results, conclusion, agricultural context.' },
          { term: 'past paper practice with self-marking', description: 'Write full answers under timed conditions and count your marking points. Aim for 8-10 distinct points per long question.' },
          { term: 'agricultural vocabulary flashcards', description: 'Flashcards for key terms across all strands. Test daily using active recall to build precise scientific vocabulary.' }
        ]
      },
      // Section 6: Action Plan
      {
        title: 'Your Agricultural Science Action Plan',
        eyebrow: '06 // Action Plan',
        paragraphs: [
          'Create a **four-strand revision plan**. In week one, focus on Soils, Crops and the Environment -- create your topic summaries, experiment write-ups, and flashcards for this strand. In week two, do the same for Animal Science. Week three covers Food Science, and week four covers Sustainability. By the end of four weeks, you will have the full syllabus covered with revision materials you can return to.',
          'In parallel with your strand revision, practise Section B experiment questions from past papers. Aim to complete all available experiment questions for each mandatory experiment. After covering all four strands, move to Section C past paper practice -- write at least 3-4 long answers per week under timed conditions and mark them yourself.',
          'In the final two weeks, do two full timed practice papers (2.5 hours each). Identify your weakest strand and spend extra time there. On exam day, answer Section A first (it is the quickest and builds confidence), then Section B (experiments -- your most predictable marks), and finally Section C (where you choose your strongest topics). Read all Section C questions before committing to your choices.'
        ],
        highlights: [],
        commitmentText: 'This week, I will create a complete revision checklist covering all four syllabus strands and write structured experiment summaries for 3 mandatory experiments from memory.'
      }
    ]
  }
};
