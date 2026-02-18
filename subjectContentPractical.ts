/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Practical subjects content for the data-driven subject modules.
 * Covers: Home Economics, Construction Studies, Engineering, DCG, Technology.
 *
 * All mark allocations and exam structures are based on the current
 * SEC (State Examinations Commission) Leaving Certificate specifications.
 */

import { SubjectModuleContent } from './subjectModuleData';

export const PRACTICAL_CONTENT: Record<string, SubjectModuleContent> = {

  /* ================================================================
   * HOME ECONOMICS — Higher Level
   * ================================================================ */
  'home-economics': {
    subjectId: 'home-economics',
    subjectName: 'Home Economics',
    moduleNumber: '23',
    moduleTitle: 'Mastering Home Economics',
    moduleSubtitle: 'Your Complete Home Ec Exam Guide',
    moduleDescription:
      'Master the Home Economics exam and practical components — from the food practical to the journal and written paper — and learn where the marks really are.',
    themeName: 'pink',
    sections: [
      /* ---- Section 1: Exam Structure ---- */
      {
        title: 'How Home Economics Actually Works',
        eyebrow: '01 // Exam Structure',
        paragraphs: [
          'Home Economics is one of the most unique subjects on the Leaving Cert because it is assessed across **three separate components** — a written exam, a food practical, and a coursework journal. Understanding how each piece fits together is the first step to maximising your grade. Too many students pour all their energy into the written paper and neglect the practical and journal, which is a strategic mistake because those components collectively account for roughly **half of your total mark**.',
          'The **written paper** is sat in June, lasts **2 hours 30 minutes**, and is worth approximately **250 marks** (around 50% of the total). You choose one of two electives: [[Elective 1 — Food Studies]] or [[Elective 2 — Social Studies]]. Most students take Elective 1. Section A is a compulsory short-answer section, and Section B contains longer structured and essay-style questions from your chosen elective.',
          'The [[Food Practical Exam]] is the timed cooking test, typically held in April or early May in your school\'s home ec room. It is worth roughly **35% of your total mark**. You receive a brief with a set of dishes to prepare, and you are assessed on planning, execution, presentation, and hygiene. This is the single biggest block of marks outside the written paper.',
          'The [[Coursework Journal]] — sometimes called the food studies assignment — is worth approximately **80 marks (around 15%)**. It documents your research, practical experiments, and evaluations throughout the year. If done properly, these are among the most reliable marks in the entire subject because they are completed under your own control with time to polish your work.'
        ],
        highlights: [
          { term: 'Elective 1 — Food Studies', description: 'The most popular elective, covering food science, nutrition, food technology, and cookery. Taken by the vast majority of HL students.' },
          { term: 'Elective 2 — Social Studies', description: 'Covers family resource management, consumer studies, and social aspects of home economics. Chosen less frequently at HL.' },
          { term: 'Food Practical Exam', description: 'A timed cooking examination, usually 2.5–3 hours, where you prepare a number of dishes under exam conditions. Marked on planning, skill, presentation, and food safety.' },
          { term: 'Coursework Journal', description: 'A structured written assignment completed during the year. Covers research, practical investigations, and evaluations. Marked by the SEC.' }
        ],
      },
      /* ---- Section 2: Marking Criteria ---- */
      {
        title: 'What the Examiner Rewards',
        eyebrow: '02 // Marking Criteria',
        paragraphs: [
          'On the **written paper**, examiners reward depth and precision. In Elective 1, they want you to demonstrate real understanding of food science — not just list facts, but **explain the why**. If a question asks about protein denaturation, they want the process explained, the factors that cause it, and ideally a practical example. Using correct terminology like [[denaturation]], [[gelatinisation]], and [[caramelisation]] signals that you genuinely understand the material.',
          'For the **Food Practical**, the marking scheme is broken into clear categories: the quality of your [[planning sheet]], your practical skills during cooking (technique, timing, multi-tasking), the final [[presentation and garnish]] of your dishes, and your hygiene and safety throughout. The planning sheet alone can earn you significant marks — it must show a realistic time plan, a clear sequence of tasks, and evidence that you have thought through every step.',
          'In the **Coursework Journal**, examiners look for clear structure, genuine investigation (not just copied notes), and honest evaluation. The best journals include well-photographed practical work, nutritional analysis, sensory evaluation charts, and thoughtful conclusions. A journal that reads like a textbook will score lower than one that shows [[genuine experimentation]] — where you tried something, assessed the result, and drew your own conclusions.',
          'Across all three components, the consistent theme is **application over recall**. Examiners do not want you to simply repeat what the textbook says. They want you to apply knowledge to real scenarios — whether that is explaining why a sauce split, adapting a recipe for a dietary requirement, or evaluating a food product against nutritional guidelines.'
        ],
        highlights: [
          { term: 'denaturation', description: 'The process by which proteins lose their structure due to heat, acid, or mechanical action. A frequently examined concept in food science.' },
          { term: 'gelatinisation', description: 'The process where starch granules absorb water and swell when heated, thickening liquids. Key to understanding sauces and soups.' },
          { term: 'caramelisation', description: 'The browning of sugar when heated above its melting point. Important in understanding flavour development and cooking techniques.' },
          { term: 'planning sheet', description: 'A detailed written plan for the food practical, including time plan, order of work, equipment needed, and recipe adaptations. Worth significant marks.' },
          { term: 'presentation and garnish', description: 'How the finished dishes look on the plate. Examiners mark for colour, arrangement, appropriate garnishing, and overall visual appeal.' },
          { term: 'genuine experimentation', description: 'The journal should show real trial and error — testing variables, recording results honestly, and drawing conclusions based on evidence.' }
        ],
      },
      /* ---- Section 3: High-Value Zones ---- */
      {
        title: 'Where Your Marks Are',
        eyebrow: '03 // High-Value Zones',
        paragraphs: [
          'The biggest strategic insight in Home Economics is that **the practical and journal together are worth roughly half your total grade**. That is enormous. In most subjects you sit a single written exam and that determines everything. Here, you walk into the June written paper with potentially 50% of your marks already banked. If you have scored well in the food practical and journal, you only need a solid — not spectacular — written paper to achieve a high grade.',
          'Within the written paper, the [[compulsory short-answer section]] (Section A) is a gift if you have been studying consistently. These are quick, factual questions that test breadth of knowledge. They are worth a significant chunk of the paper, and most well-prepared students can score very highly here. Do not rush through them — read each question carefully and give complete answers.',
          'The Food Practical is the single highest-value event in the subject. The marks for **execution and presentation** are substantial, but do not overlook the marks for your [[planning sheet]] and [[hygiene practices]]. Students who walk in without a thorough, realistic time plan leave marks on the table. Similarly, consistent hand-washing, clean-as-you-go habits, and correct food storage are all observed and marked.',
          'In the journal, the [[sensory analysis]] section and the [[nutritional analysis]] are high-mark areas that many students underperform in. A sensory analysis with a proper hedonic scale, tasting panel data, and a star diagram will outscore a vague paragraph saying "it tasted nice." The nutritional analysis should use actual data — reference values, RDAs, and percentage breakdowns — not just generic statements.'
        ],
        highlights: [
          { term: 'compulsory short-answer section', description: 'Section A of the written paper — a series of short, factual questions covering the core syllabus. High marks are achievable with consistent study.' },
          { term: 'planning sheet', description: 'Your written plan for the practical exam. A detailed, realistic time plan with clear sequencing can earn you 15–20+ marks before you even start cooking.' },
          { term: 'hygiene practices', description: 'Observed throughout the practical — hand-washing, apron use, clean work surfaces, correct storage temperatures. Marked as a distinct category.' },
          { term: 'sensory analysis', description: 'Structured evaluation of food using appearance, aroma, taste, texture, and overall acceptability. Best done with hedonic scales and tasting panel data.' },
          { term: 'nutritional analysis', description: 'Detailed breakdown of the nutritional content of dishes prepared, compared against recommended daily allowances (RDAs). Strengthened by using actual data tables.' }
        ],
      },
      /* ---- Section 4: Common Pitfalls ---- */
      {
        title: 'What Costs You Marks',
        eyebrow: '04 // Common Pitfalls',
        paragraphs: [
          'The number one mistake in Home Economics is **neglecting the practical components**. Students who spend all their time on the written paper and treat the food practical as something that will "just happen" are throwing away the easiest marks in the subject. The practical and journal reward preparation and practice — skills you build over time, not the night before.',
          'In the written paper, a common error is [[vague answering]]. If a question asks you to explain the role of vitamin C in the diet, writing "vitamin C is good for your health" will earn almost nothing. The examiner wants specific functions (antioxidant, aids iron absorption, collagen formation), specific sources, and the consequences of deficiency. Every answer should aim for precision.',
          'During the Food Practical, the biggest mark-killer is **poor time management**. Students who attempt overly ambitious dishes and cannot finish them will score lower than students who execute simpler dishes perfectly and on time. The other critical error is ignoring [[cross-contamination]] rules — using the same chopping board for raw meat and salad, or not washing hands after handling raw poultry. Examiners watch for this.',
          'In the journal, the pitfall is [[superficial evaluation]]. Concluding every experiment with "this went well" does not earn marks. Strong evaluation identifies what worked, what did not, what you would change, and why. It connects back to the food science principles you studied. The difference between a good journal and a great one is the depth of your critical reflection.'
        ],
        highlights: [
          { term: 'vague answering', description: 'Giving general, non-specific responses that could apply to anything. Examiners reward precise terminology, specific examples, and clear explanations.' },
          { term: 'cross-contamination', description: 'The transfer of harmful bacteria from one food to another, typically from raw to cooked foods. A serious food safety issue marked in the practical.' },
          { term: 'superficial evaluation', description: 'Conclusions that lack depth or critical analysis. The best evaluations identify specific successes, failures, and improvements with scientific reasoning.' }
        ],
        bullets: [
          'Skipping the planning sheet or writing it vaguely — this is **free marks** you are giving up',
          'Attempting dishes in the practical that you have never practised at home',
          'Leaving the journal until the last week — it takes time to build genuine content',
          'Ignoring dietary modifications — questions often ask you to adapt recipes for specific needs',
          'Writing essays without using correct food science terminology'
        ],
      },
      /* ---- Section 5: Study Techniques ---- */
      {
        title: 'How to Study Home Economics',
        eyebrow: '05 // Study Techniques',
        paragraphs: [
          'The best Home Economics students study with a **dual approach**: theory and practice. For the written paper, build a set of concise notes organised by topic — nutrition, food science, food technology, consumer studies. Use [[active recall]] by covering your notes and writing out key processes from memory. Flashcards are excellent for terminology-heavy topics like vitamins, minerals, and food additives.',
          'For the Food Practical, there is no substitute for **cooking practice at home**. Aim to practise your core dishes at least 3–4 times each before the exam. Time yourself. Get feedback from family. Practise your planning sheet alongside the cooking — write it out as if it were the real exam. The goal is that by the day of the practical, every dish feels automatic and your time plan is second nature.',
          'For the journal, work on it **steadily throughout the year**. Do not try to produce it all in a sprint. Each practical class is an opportunity to photograph your work, record observations, and write up evaluations while the experience is fresh. A journal built gradually over months will always outperform one assembled in a panic, because the depth and authenticity are visible to the examiner.',
          'When revising the written paper, work through [[past exam papers]] methodically. The SEC publishes papers and marking schemes going back years. Study the marking scheme closely — it reveals exactly what language and level of detail earns full marks. You will also notice that certain topics recur frequently. Nutrition, food safety, and consumer protection are perennial favourites.'
        ],
        highlights: [
          { term: 'active recall', description: 'A study technique where you actively retrieve information from memory rather than passively re-reading notes. Proven to be one of the most effective learning methods.' },
          { term: 'past exam papers', description: 'Previous years\' Leaving Cert papers and marking schemes published by the SEC. Essential for understanding question patterns and examiner expectations.' }
        ],
      },
      /* ---- Section 6: Action Plan ---- */
      {
        title: 'Your Home Economics Action Plan',
        eyebrow: '06 // Action Plan',
        paragraphs: [
          'Start by auditing where your marks are right now. Have you been building your journal consistently? Have you practised your practical dishes? If the answer to either is no, **those are your immediate priorities** — they represent roughly half your total grade and they reward effort directly. Every hour spent practising a dish or improving a journal section translates into tangible marks.',
          'For the written paper, create a focused revision plan that covers the core topics: nutrition (macronutrients, micronutrients, dietary guidelines), food science (protein, carbohydrate, and fat cookery), food safety (HACCP, food spoilage, preservation), and consumer studies. Use past papers to identify your weak areas, then target those topics specifically.',
          'Set a concrete goal: complete your journal to a standard you are proud of at least **two weeks before the deadline**. Practise each practical dish until you can execute it confidently within the time limit. And commit to working through at least **five full past papers** under timed conditions before the written exam. If you follow this plan, you will walk into each component feeling prepared rather than panicked.'
        ],
        highlights: [
          { term: 'HACCP', description: 'Hazard Analysis and Critical Control Points — a systematic food safety framework. A high-frequency topic on the written paper.' }
        ],
        commitmentText:
          'I will practise my food practical dishes this week and spend 30 minutes improving one section of my journal.',
      },
    ],
  },

  /* ================================================================
   * CONSTRUCTION STUDIES — Higher Level
   * ================================================================ */
  'construction-studies': {
    subjectId: 'construction-studies',
    subjectName: 'Construction Studies',
    moduleNumber: '24',
    moduleTitle: 'Mastering Construction Studies',
    moduleSubtitle: 'Your Complete Construction Guide',
    moduleDescription:
      'Understand the Construction Studies exam and project — how marks are split between practical and written, and what the examiner rewards in each.',
    themeName: 'slate',
    sections: [
      /* ---- Section 1: Exam Structure ---- */
      {
        title: 'How Construction Studies Actually Works',
        eyebrow: '01 // Exam Structure',
        paragraphs: [
          'Construction Studies is split almost perfectly down the middle: **roughly 50% for the written exam and 50% for the practical project**. This means the project you build in the school workshop is worth just as much as the three-hour paper you sit in June. Students who treat the project as a side task and focus only on theory are leaving half their grade to chance.',
          'The [[written paper]] is a **3-hour exam worth 400 marks**. It is divided into sections covering building construction, building services, and materials science. Section A typically contains short-answer questions, while Section B has longer, more detailed questions requiring sketches, diagrams, and extended written answers. You do not have to answer every question — there is usually a choice, so you can lean into your strongest topics.',
          'The [[practical project]] is completed in your school workshop over the course of fifth and sixth year. You select a project brief from the options provided by the SEC, and you build a piece that demonstrates your skills in woodwork, or a combination of materials. The project is assessed by a visiting examiner who evaluates the quality of construction, accuracy of dimensions, finish, and adherence to the brief.',
          'The key insight is that both components reward the same underlying quality: **attention to detail**. On the written paper, detailed sketches and precise terminology score highest. On the project, accuracy of joints, quality of finish, and closeness to specified dimensions are what separate the top grades from the rest.'
        ],
        highlights: [
          { term: 'written paper', description: 'A 3-hour exam worth 400 marks, covering building construction, services (plumbing, heating, electrics), and materials. Requires both written answers and technical sketches.' },
          { term: 'practical project', description: 'A substantial piece of work built in the school workshop over the senior cycle. Worth approximately 50% of your total grade. Assessed by a visiting SEC examiner.' }
        ],
      },
      /* ---- Section 2: Marking Criteria ---- */
      {
        title: 'What the Examiner Rewards',
        eyebrow: '02 // Marking Criteria',
        paragraphs: [
          'On the written paper, examiners reward **technical accuracy and clarity of communication**. When a question asks you to describe how a cavity wall is constructed, they want a clear, labelled diagram accompanied by a written explanation that uses correct terminology — [[DPC]], [[wall ties]], [[insulation type and placement]]. A good sketch with proper labels can earn almost as many marks as the written explanation itself.',
          'For diagram-based questions, the examiner looks for proportion, correct labelling, and evidence that you understand the real-world construction process. Drawing a roof truss is not just about getting the shape right — it is about showing the [[rafter]], [[purlin]], [[wall plate]], and connections accurately. Neat, proportional diagrams with clear annotations consistently outscore messy freehand sketches.',
          'On the **practical project**, the visiting examiner uses a structured marking scheme that covers: [[quality of joints]], accuracy of dimensions (measured against the original brief), quality of surface finish, and overall design and construction. The examiner will literally measure your project. If the brief specifies a component should be 300mm and yours is 295mm, you will lose marks. Precision matters enormously.',
          'The finish is the last thing the examiner sees and it creates a strong impression. A well-sanded, cleanly finished project with no visible glue marks, consistent staining or varnishing, and crisp edges signals craftsmanship. Conversely, rough surfaces, visible tool marks, and uneven finishes will cost you marks even if the underlying construction is sound.'
        ],
        highlights: [
          { term: 'DPC', description: 'Damp Proof Course — a horizontal barrier in a wall designed to prevent moisture rising through the structure. A core concept in building construction questions.' },
          { term: 'wall ties', description: 'Metal or plastic connectors that tie the inner and outer leaves of a cavity wall together. Frequently examined in construction detail questions.' },
          { term: 'insulation type and placement', description: 'Knowledge of where and what type of insulation is used in walls, roofs, and floors — partial fill, full fill, and pumped cavity insulation are commonly examined.' },
          { term: 'rafter', description: 'A structural member in a roof that runs from the ridge to the wall plate, supporting the roof covering. Key component in roof construction questions.' },
          { term: 'purlin', description: 'A horizontal beam in a roof structure that supports the rafters, typically running perpendicular to them.' },
          { term: 'wall plate', description: 'A timber member placed on top of a wall to distribute the load from the roof structure evenly.' },
          { term: 'quality of joints', description: 'The precision and strength of joints (mortise and tenon, dovetail, housing, etc.) in the practical project. Poorly fitting joints are the single biggest mark loser.' }
        ],
      },
      /* ---- Section 3: High-Value Zones ---- */
      {
        title: 'Where Your Marks Are',
        eyebrow: '03 // High-Value Zones',
        paragraphs: [
          'Your **practical project is the single largest block of marks** in Construction Studies. At roughly 50% of your total, this is where your grade is won or lost. The project is assessed before the written exam, so you walk into June with half your marks already determined. A well-executed project gives you a massive cushion — you can afford a mediocre written paper and still achieve a high grade. A rushed project does the opposite.',
          'Within the written paper, the [[building construction section]] is the highest-value area. Questions on wall construction, roof construction, foundations, and floor construction appear every year and carry heavy marks. These are the bread-and-butter topics — if you can draw and explain a cavity wall, a cut roof, a strip foundation, and a suspended timber floor with confidence, you have the core of the paper covered.',
          'The [[building services]] section — covering plumbing, heating systems, and electrical installations — is another reliable source of marks. Students often underestimate these topics, but they appear consistently and the questions tend to be structured and predictable. A solid understanding of a [[central heating system]], a domestic water supply layout, or a ring main circuit can earn you full marks on questions that many students leave half-answered.',
          'On the project side, the marks for [[joint quality and accuracy]] are disproportionately important. A project with four perfectly executed joints and a clean finish will outscore a more ambitious project with sloppy joints and a rushed finish every time. The examiner knows what good craftsmanship looks like — there are no shortcuts.'
        ],
        highlights: [
          { term: 'building construction section', description: 'The core section of the written paper covering walls, roofs, floors, foundations, doors, windows, and stairs. Appears every year with high mark allocations.' },
          { term: 'building services', description: 'Covers plumbing (water supply, drainage), heating (central heating systems, heat pumps), and electrical installations. A consistently examined and high-value area.' },
          { term: 'central heating system', description: 'A domestic heating system with boiler, radiators, pipework, and controls. A frequent exam question — draw the system layout and explain each component.' },
          { term: 'joint quality and accuracy', description: 'The precision of woodworking joints in your project. Tight-fitting, clean joints with no gaps are the hallmark of a high-scoring project.' }
        ],
      },
      /* ---- Section 4: Common Pitfalls ---- */
      {
        title: 'What Costs You Marks',
        eyebrow: '04 // Common Pitfalls',
        paragraphs: [
          'The most damaging mistake in Construction Studies is **leaving the project too late**. The project takes significant workshop time, and rushing it in the final weeks always shows in the quality. Joints that are not properly fitted, surfaces that are not properly sanded, and finishes that are not properly applied are all signs of a rushed project — and the examiner spots them instantly.',
          'On the written paper, the biggest mark-killer is [[poor sketching]]. Many students write decent explanations but produce diagrams that are unclear, unlabelled, or out of proportion. In Construction Studies, the sketch is not decoration — it is a core part of your answer. An unlabelled diagram earns almost nothing. A well-labelled, proportional sketch can earn full marks on its own for certain questions.',
          'Another common error is **topic avoidance**. Students who skip building services because they find plumbing or electrics confusing are giving up easy marks. These questions follow predictable patterns, and a methodical student who learns the key diagrams (hot water system, central heating layout, ring main circuit) can score very well without needing deep technical expertise.',
          'On the project, a subtle but costly mistake is [[ignoring the brief]]. The project brief specifies dimensions, materials, and design constraints. Students who deviate from the brief — making a component larger because it looks better, or substituting a material because it is easier to work with — will lose marks for non-compliance, even if the craftsmanship is good.'
        ],
        highlights: [
          { term: 'poor sketching', description: 'Diagrams that lack labels, are out of proportion, or are difficult to read. In Construction Studies, sketches carry significant marks and must be clear and annotated.' },
          { term: 'ignoring the brief', description: 'Deviating from the SEC project brief in terms of dimensions, materials, or design. The examiner marks against the brief, so non-compliance costs marks.' }
        ],
        bullets: [
          'Rushing the project in the final weeks — the quality always suffers visibly',
          'Drawing diagrams without labels — an unlabelled sketch earns close to zero',
          'Avoiding building services questions because the content seems unfamiliar',
          'Neglecting the surface finish — sanding, staining, and varnishing are all marked',
          'Not measuring your project against the brief dimensions before submission'
        ],
      },
      /* ---- Section 5: Study Techniques ---- */
      {
        title: 'How to Study Construction Studies',
        eyebrow: '05 // Study Techniques',
        paragraphs: [
          'Construction Studies rewards **visual learning**. The most effective study technique is to practise drawing construction details from memory. Take a blank page, pick a topic — say, cavity wall construction — and draw the full detail with labels. Then check against your notes. Repeat until you can produce a clear, accurate, fully-labelled diagram without reference material. This is [[sketch-based recall]] and it is the single most effective method for this subject.',
          'Build a personal library of [[key construction details]]. There are roughly 15–20 standard construction details that cover the most commonly examined topics: cavity wall, strip and raft foundations, cut and truss roofs, suspended and solid floors, domestic water supply, central heating, ring main circuit, and staircase construction. If you can draw and explain each of these from memory, you are prepared for the vast majority of questions.',
          'For the written explanations, practise answering in a structured format: name the components, describe their function, explain how they connect to each other, and state any building regulation requirements. Using [[correct terminology]] consistently is essential. Do not write "the bottom bit of the wall" — write "the substructure below DPC level." The examiner is looking for evidence that you speak the language of construction.',
          'For the project, treat your workshop time with the same seriousness as exam revision. Set milestones: joints cut by a certain date, assembly complete by another, finishing by a third. Practise your joints on scrap timber before committing to your project piece. A mortise and tenon joint practised five times on scrap will be dramatically better than one attempted for the first time on your actual project.'
        ],
        highlights: [
          { term: 'sketch-based recall', description: 'Drawing construction details from memory as a revision technique. Forces you to truly understand the components and their relationships, not just recognise them.' },
          { term: 'key construction details', description: 'The 15–20 standard construction drawings that cover the most frequently examined topics. Mastering these is the foundation of exam preparation.' },
          { term: 'correct terminology', description: 'Using proper construction terms (DPC, wall plate, flashing, soaker, noggin, etc.) rather than informal descriptions. Signals competence to the examiner.' }
        ],
      },
      /* ---- Section 6: Action Plan ---- */
      {
        title: 'Your Construction Studies Action Plan',
        eyebrow: '06 // Action Plan',
        paragraphs: [
          'First, assess your project status honestly. If you are behind on your practical project, that is your **top priority** — it is worth half your grade and cannot be crammed. Set a realistic completion timeline with your teacher and commit to using every available workshop session productively. Focus on joint quality and finish rather than adding unnecessary complexity.',
          'For the written paper, identify the 15–20 key construction details and begin practising them as sketches from memory. Aim to draw and label **two details per study session**. Work through past papers to identify which topics appear most frequently, and focus your revision there. Building construction and building services should be your primary targets.',
          'Set a target: be able to draw and fully explain at least **15 construction details from memory** before the exam. Complete at least **four full past papers** under timed conditions. And ensure your project is finished, measured against the brief, and properly finished at least **two weeks before the submission deadline**. With your project marks banked high and your construction details memorised, you will be in a strong position for a top grade.'
        ],
        highlights: [
          { term: 'construction details', description: 'Standard annotated drawings of building elements — walls, roofs, floors, foundations, services. The backbone of the written exam.' }
        ],
        commitmentText:
          'I will practise drawing two construction details from memory this week and set a project completion milestone with my teacher.',
      },
    ],
  },

  /* ================================================================
   * ENGINEERING — Higher Level
   * ================================================================ */
  'engineering': {
    subjectId: 'engineering',
    subjectName: 'Engineering',
    moduleNumber: '25',
    moduleTitle: 'Mastering Engineering',
    moduleSubtitle: 'Your Complete Engineering Guide',
    moduleDescription:
      'Break down the Engineering exam and project — understand the practical marks, the written paper structure, and how to maximise your overall grade.',
    themeName: 'gray',
    sections: [
      /* ---- Section 1: Exam Structure ---- */
      {
        title: 'How Engineering Actually Works',
        eyebrow: '01 // Exam Structure',
        paragraphs: [
          'Leaving Certificate Engineering is a subject where you **build something real** and that project counts for half your final grade. The assessment is split roughly **50/50 between the written exam and the practical project**. This dual structure means that your workshop skills matter just as much as your ability to answer questions on paper — and it means you have two separate opportunities to earn marks.',
          'The [[written exam]] is a **3-hour paper** covering the core theory of engineering: materials and their properties, manufacturing processes, mechanisms and motion, and electronics and electricity. The paper typically has a Section A with shorter, more structured questions and a Section B with longer questions that require deeper analysis, calculations, and diagrams. There is usually a choice of questions, so you can play to your strengths.',
          'The [[practical project]] is a piece of engineered work that you design, plan, and manufacture in the school workshop over the course of your senior cycle. The SEC provides a set of project briefs, and you choose one to execute. The project is assessed by a visiting examiner who evaluates the quality of your machining, fitting, assembly, finish, and adherence to the design brief.',
          'The relationship between the two components is important to understand: strong project marks give you a **safety net** for the written paper. If you score well on the project, you need fewer marks on the written paper to hit your target grade. Conversely, a weak project means you need an exceptional written paper just to compensate — and that is much harder to guarantee.'
        ],
        highlights: [
          { term: 'written exam', description: 'A 3-hour paper covering engineering materials, processes, mechanisms, electronics, and design. Worth approximately 50% of the total mark.' },
          { term: 'practical project', description: 'A manufactured piece completed in the school workshop over the senior cycle. Worth approximately 50% of the total mark. Assessed by a visiting SEC examiner.' }
        ],
      },
      /* ---- Section 2: Marking Criteria ---- */
      {
        title: 'What the Examiner Rewards',
        eyebrow: '02 // Marking Criteria',
        paragraphs: [
          'On the written paper, the examiner rewards **technical understanding demonstrated through clear explanations and accurate calculations**. In materials questions, they want you to name the material, describe its properties, explain why it is suitable for a given application, and contrast it with alternatives. Using terms like [[tensile strength]], [[hardness]], [[malleability]], and [[ductility]] correctly shows you understand the material rather than just memorising names.',
          'For questions on [[manufacturing processes]], the examiner looks for step-by-step descriptions that show you understand the sequence — not just the end result. If asked about turning on a lathe, they want to know about workpiece mounting, tool selection, speed calculation, feed rate, and finishing. Diagrams of setups and tool geometry earn significant marks.',
          'On the practical project, the examiner assesses four main areas: [[quality of machining]] (how accurately and cleanly metal has been cut, drilled, turned, and filed), quality of fitting and assembly (how well components fit together), quality of finish (surface finish, deburring, paint or coating), and compliance with the brief. The examiner will measure dimensions, check tolerances, test moving parts, and inspect surface quality closely.',
          'The project marks are heavily weighted toward **precision**. A simpler project executed with tight tolerances, clean machining marks, and a professional finish will consistently outscore a more complex project with sloppy fits and rough surfaces. The examiner is looking for evidence of skill and care, not ambition for its own sake.'
        ],
        highlights: [
          { term: 'tensile strength', description: 'The maximum stress a material can withstand while being pulled before breaking. A key property in materials science questions.' },
          { term: 'hardness', description: 'A material\'s resistance to indentation or scratching. Measured by tests like Brinell, Vickers, or Rockwell. Frequently examined in materials questions.' },
          { term: 'malleability', description: 'The ability of a material to be deformed under compression without cracking — e.g., hammered or rolled into sheets.' },
          { term: 'ductility', description: 'The ability of a material to be drawn into a wire without breaking. Copper and gold are highly ductile metals.' },
          { term: 'manufacturing processes', description: 'The methods used to shape, join, and finish materials — turning, milling, drilling, welding, brazing, soldering, casting, forging, etc.' },
          { term: 'quality of machining', description: 'The precision and cleanliness of machine work — straight cuts, accurate holes, smooth turned surfaces, correct dimensions.' }
        ],
      },
      /* ---- Section 3: High-Value Zones ---- */
      {
        title: 'Where Your Marks Are',
        eyebrow: '03 // High-Value Zones',
        paragraphs: [
          'As with all practical subjects, your **project is the single biggest mark opportunity**. At roughly 50% of your total, a well-executed project is the most reliable way to secure a high grade. The marks are awarded for tangible, measurable qualities — how accurate are your dimensions, how clean is your machining, how well do the parts fit together. There is no ambiguity. Good work gets good marks.',
          'Within the written paper, the [[materials and processes]] section is the highest-value area because it appears every year and the questions follow predictable patterns. You will be asked to identify materials, describe their properties, explain heat treatment processes (like [[hardening and tempering]]), and describe manufacturing operations. These topics are highly learnable — there is a finite body of knowledge and the exam draws from it consistently.',
          'The [[mechanisms section]] is another area where well-prepared students score heavily. Questions on gear trains, linkages, cams, and belt drives involve calculations and diagrams. If you know the formulas (gear ratio, velocity ratio, mechanical advantage) and can draw the mechanisms clearly, these are some of the most predictable marks on the paper.',
          'The [[electronics section]] covers basic circuit theory, components (resistors, capacitors, transistors, logic gates), and simple circuit analysis. Many students find this section intimidating, but the questions are often straightforward if you have practised the calculations. Ohm\'s Law, series and parallel circuits, and truth tables for logic gates are high-frequency topics that reward focused revision.'
        ],
        highlights: [
          { term: 'materials and processes', description: 'The core section covering ferrous and non-ferrous metals, plastics, composites, heat treatments, and manufacturing operations. Examined every year.' },
          { term: 'hardening and tempering', description: 'Heat treatment processes for steel — hardening involves heating and quenching, tempering involves reheating to a lower temperature to reduce brittleness.' },
          { term: 'mechanisms section', description: 'Covers gear trains, linkages, cams, belt drives, and other mechanical systems. Questions often involve calculations of gear ratios and velocity ratios.' },
          { term: 'electronics section', description: 'Covers basic circuit theory, components, and logic circuits. Ohm\'s Law calculations, transistor switching circuits, and truth tables are common questions.' }
        ],
      },
      /* ---- Section 4: Common Pitfalls ---- */
      {
        title: 'What Costs You Marks',
        eyebrow: '04 // Common Pitfalls',
        paragraphs: [
          'The most common mistake in Engineering is **underinvesting in the project**. Half your total marks depend on workshop output, but many students spend disproportionately more time on written revision and treat workshop sessions casually. Every workshop session is an opportunity to improve your project — sanding a surface smoother, filing a fit tighter, checking a dimension against the brief. These small improvements accumulate into significant marks.',
          'On the written paper, the biggest pitfall is [[incomplete answers]]. Engineering questions often have multiple parts, and students who answer only the first part and move on are leaving marks behind. If a question asks you to name a material, state two properties, and explain a suitable application, each element carries marks. Skipping the application paragraph because you are unsure costs you marks you could have earned with a reasonable attempt.',
          'Another common error is **neglecting diagrams**. Engineering questions frequently ask for sketches of mechanisms, manufacturing setups, or circuit diagrams. Students who write paragraphs of text but skip the diagram are missing the point — the diagram often carries as many marks as the written explanation. A clear, labelled diagram of a [[lathe setup]] or a gear train is worth significant marks.',
          'On the project, the most costly mistake is [[poor planning]]. Students who start machining without a clear plan of operations — what to cut first, what to drill, what tolerances to hold — end up with parts that do not fit together properly. The order of operations matters in engineering. A part that is drilled before being turned may end up with the hole off-centre. Think before you cut.'
        ],
        highlights: [
          { term: 'incomplete answers', description: 'Answering only part of a multi-part question. Each sub-part typically carries separate marks, so skipping any part wastes potential marks.' },
          { term: 'lathe setup', description: 'The arrangement of the workpiece, tool, and lathe components for a turning operation. Commonly asked to be drawn and explained in exam questions.' },
          { term: 'poor planning', description: 'Starting workshop work without a clear sequence of operations. Leads to parts that do not fit together and dimensions that are off-specification.' }
        ],
        bullets: [
          'Treating workshop time as less important than classroom study — both are worth 50%',
          'Writing answers without diagrams — sketches carry heavy marks in Engineering',
          'Skipping the electronics section because it feels difficult — the questions are often formulaic',
          'Rushing the project finish — surface preparation, deburring, and coating all carry marks',
          'Not practising calculations — gear ratios, Ohm\'s Law, and velocity ratios need practice'
        ],
      },
      /* ---- Section 5: Study Techniques ---- */
      {
        title: 'How to Study Engineering',
        eyebrow: '05 // Study Techniques',
        paragraphs: [
          'Engineering study is most effective when it combines **theory revision with practical understanding**. When you study a manufacturing process like milling, do not just read about it — think about how you have used the milling machine in the workshop. Connecting theory to your hands-on experience makes the knowledge stick and makes your exam answers more detailed and authentic.',
          'Build a [[process revision bank]]: create a one-page summary for each major manufacturing process (turning, milling, drilling, welding, brazing, casting, forging) that includes a labelled diagram, the steps involved, the materials it applies to, and any safety considerations. Do the same for heat treatment processes. These summaries become your core revision resource.',
          'For the mechanisms and electronics sections, **practice calculations repeatedly**. These are mark-rich questions with definitive right answers. Work through past paper questions until you can solve gear ratio, velocity ratio, and Ohm\'s Law problems quickly and accurately. Use [[formula sheets]] that you create yourself — the act of writing them helps you memorise the formulas.',
          'For the project, apply the same study mindset to your workshop practice. Before each session, plan what you will achieve. After each session, assess what went well and what needs improvement. If a surface is not smooth enough, spend the next session improving it rather than moving on. Treat workshop time as [[deliberate practice]] — focused, purposeful, and always aimed at improving the weakest element of your project.'
        ],
        highlights: [
          { term: 'process revision bank', description: 'A personal collection of one-page summaries for each manufacturing process — diagram, steps, materials, and safety. An efficient revision tool.' },
          { term: 'formula sheets', description: 'Self-created reference sheets with key formulas for mechanisms (gear ratio, MA, VR) and electronics (Ohm\'s Law, power, series/parallel). Writing them aids memorisation.' },
          { term: 'deliberate practice', description: 'Focused workshop practice aimed at improving specific skills rather than just "working on the project." Each session should target a measurable improvement.' }
        ],
      },
      /* ---- Section 6: Action Plan ---- */
      {
        title: 'Your Engineering Action Plan',
        eyebrow: '06 // Action Plan',
        paragraphs: [
          'Assess your project right now. What is its current state? What still needs to be done? Set a **completion deadline at least two weeks before submission** so you have time for finishing and quality checks. If specific machining operations are not going well, ask your teacher for guidance or practice on scrap material. The project is half your grade — it deserves your best effort.',
          'For the written paper, start with the materials and processes section — it is the highest-value, most predictable area. Build your process revision bank and practise sketching manufacturing setups from memory. Then tackle mechanisms and electronics through calculation practice. Aim to complete at least **four past papers** under timed conditions.',
          'Your final push should integrate both components. As your project nears completion, shift more time to written revision. But do not abandon the project — use every remaining workshop session to refine the finish. A well-finished project combined with solid written exam preparation is the formula for a top grade in Engineering.'
        ],
        highlights: [
          { term: 'process revision bank', description: 'One-page summaries per manufacturing process — your most efficient revision tool for the materials and processes section.' }
        ],
        commitmentText:
          'I will assess my project status this week, set a completion milestone, and create process summaries for three manufacturing operations.',
      },
    ],
  },

  /* ================================================================
   * DCG (Design & Communication Graphics) — Higher Level
   * ================================================================ */
  'dcg': {
    subjectId: 'dcg',
    subjectName: 'DCG',
    moduleNumber: '26',
    moduleTitle: 'Mastering DCG',
    moduleSubtitle: 'Your Complete DCG Exam Guide',
    moduleDescription:
      'Master Design & Communication Graphics — from the student assignment to the written exam — and learn how to present your work for maximum marks.',
    themeName: 'cyan',
    sections: [
      /* ---- Section 1: Exam Structure ---- */
      {
        title: 'How DCG Actually Works',
        eyebrow: '01 // Exam Structure',
        paragraphs: [
          'Design & Communication Graphics (DCG) is the modern evolution of Technical Drawing, and it tests your ability to solve spatial and geometric problems — both on paper and using CAD software. The assessment is split into two major components: the [[written exam]] worth approximately **60% of your total mark**, and the [[student assignment]] worth approximately **40%**. That assignment is a significant piece of work completed during the year, making DCG one of the subjects where you can build a substantial portion of your grade before sitting the written paper.',
          'The **written exam** is a **3-hour paper** that covers the full range of the DCG syllabus. It includes questions on [[plane and descriptive geometry]] (the traditional technical drawing problems), solid geometry, surface developments, and applied graphics. The questions require you to construct precise geometric solutions using instruments — your compass, set squares, and drawing equipment are as important as your pen.',
          'The [[student assignment]] is a design-based project, typically involving CAD modelling using software like **SolidWorks**. You receive a brief from the SEC that outlines the design challenge, and you produce a portfolio that includes research, sketches, CAD models, rendered images, and technical drawings. This assignment is assessed by the SEC and requires both creative design thinking and technical CAD proficiency.',
          'What makes DCG distinctive is the combination of **traditional drawing skills and modern CAD competence**. The written exam tests your ability to solve geometric problems by hand with precision instruments, while the student assignment tests your ability to use 3D modelling software to design, model, and present a solution. You need both skill sets to achieve a top grade.'
        ],
        highlights: [
          { term: 'written exam', description: 'A 3-hour instrument-based exam worth approximately 60% of the total mark. Covers plane geometry, descriptive geometry, solid geometry, and applied graphics.' },
          { term: 'student assignment', description: 'A CAD-based design project worth approximately 40% of the total mark. Involves 3D modelling, rendering, and technical drawing using software like SolidWorks.' },
          { term: 'plane and descriptive geometry', description: 'Core geometric problem-solving: projections, sections, developments, intersections of solids, and the representation of 3D objects on 2D planes.' }
        ],
      },
      /* ---- Section 2: Marking Criteria ---- */
      {
        title: 'What the Examiner Rewards',
        eyebrow: '02 // Marking Criteria',
        paragraphs: [
          'On the written exam, the examiner rewards **accuracy and precision above all else**. Every line you draw must be in the correct position, at the correct angle, and to the correct scale. The examiner checks your construction method — they can see from your construction lines whether you used the correct geometric technique or guessed. A correct answer arrived at through the wrong method may not receive full marks. Clean, visible [[construction lines]] that show your working are essential.',
          'The [[quality of line work]] is a distinct marking criterion. Lines should be sharp and consistent — thick for outlines, thin for construction. Intersections should be precise, not vaguely overlapping. Hidden detail should use correct dashed line conventions. A drawing that is geometrically correct but poorly presented will score lower than the same solution drawn with crisp, professional line quality.',
          'For the student assignment, the examiner assesses your [[design process]] as much as the final product. They want to see evidence of research, ideation (sketches and brainstorming), development (iterative improvement), and evaluation. The CAD models should demonstrate proficiency with features like extrusions, revolves, fillets, chamfers, and assemblies. The rendered presentations should be professional — good lighting, appropriate materials, and clear views.',
          'The technical drawing component of the assignment — orthographic views, sectional views, exploded views — must comply with [[drawing standards]]. Correct use of first-angle or third-angle projection, proper dimensioning, and appropriate scale are all marked. A beautifully rendered 3D model accompanied by sloppy technical drawings will not earn full marks.'
        ],
        highlights: [
          { term: 'construction lines', description: 'Light lines drawn as part of your geometric construction method. They show the examiner your working and must be visible but clearly lighter than the final solution lines.' },
          { term: 'quality of line work', description: 'The sharpness, consistency, and correctness of your drawn lines. Distinct line weights for outlines, hidden detail, and construction are expected.' },
          { term: 'design process', description: 'The documented journey from brief to solution — research, sketching, ideation, development, modelling, and evaluation. Marks are given for the process, not just the outcome.' },
          { term: 'drawing standards', description: 'Conventions for technical drawings — projection type, dimensioning rules, line types, title blocks, and scale. Non-compliance loses marks.' }
        ],
      },
      /* ---- Section 3: High-Value Zones ---- */
      {
        title: 'Where Your Marks Are',
        eyebrow: '03 // High-Value Zones',
        paragraphs: [
          'The **student assignment is worth 40% of your total grade** and is completed before the June exam. This is your biggest opportunity to bank marks early. A polished, well-presented assignment with strong CAD work, clear technical drawings, and a documented design process can set you up with a substantial mark before you even open the written paper. Students who invest serious time in the assignment consistently outperform those who treat it as secondary.',
          'Within the written exam, [[descriptive geometry]] questions are typically the highest-value individual questions. These involve the projection of points, lines, and planes in space — finding true lengths, true shapes, angles of inclination, and intersections. They are challenging but highly learnable. The techniques follow specific, repeatable methods, and once you master them, you can approach these questions with confidence.',
          'The [[solid geometry and surface development]] questions are another reliable source of marks. These involve the intersection of solids (cylinder penetrating a prism, cone intersecting a cylinder, etc.) and the development of surfaces for sheet metal work. Again, these follow set construction methods. A student who has practised the standard intersection types will find these questions very manageable.',
          'Applied graphics questions — covering topics like [[axonometric projection]], perspective drawing, and graphic design applications — appear regularly and are often more accessible than the pure geometry questions. Students who are comfortable with these topics can use them strategically to ensure they answer enough questions for a strong overall mark.'
        ],
        highlights: [
          { term: 'descriptive geometry', description: 'The core of DCG — representing 3D geometry on 2D planes using projection methods. Includes true lengths, true shapes, traces, and angles. High-value exam territory.' },
          { term: 'solid geometry and surface development', description: 'Questions on intersections of solids and unfolding 3D surfaces into flat patterns. Follow systematic construction methods that are highly learnable.' },
          { term: 'axonometric projection', description: 'A method of drawing 3D objects on a 2D surface (isometric, dimetric, trimetric). More visual and accessible than descriptive geometry for many students.' }
        ],
      },
      /* ---- Section 4: Common Pitfalls ---- */
      {
        title: 'What Costs You Marks',
        eyebrow: '04 // Common Pitfalls',
        paragraphs: [
          'The most common mistake in DCG is **inaccuracy**. A line that is 1mm off in a descriptive geometry problem can cascade into a completely wrong solution. Students who work carelessly with their instruments — using a blunt compass point, not anchoring the set square properly, or estimating rather than measuring — lose marks not because they do not understand the method but because the execution is imprecise. In DCG, precision is not optional; it is the subject.',
          'On the student assignment, the biggest pitfall is [[weak documentation of the design process]]. Many students jump straight to the CAD model without showing research, sketching, or development work. The examiner wants to see how you arrived at your design — the alternatives you considered, the iterations you went through, and the reasons for your final decisions. A flashy render without process documentation will score lower than a simpler design with a well-documented journey.',
          'In the written exam, students often [[misread the question setup]]. DCG questions typically provide given data — points, planes, angles — in specific positions. If you plot the given data incorrectly at the start, every subsequent construction step will be wrong. Always double-check your initial setup before proceeding with the construction. A few extra seconds verifying the given data can save an entire question.',
          'Another costly error is **poor time management** during the written paper. Students who spend too long on a difficult geometry problem and leave easier questions unanswered are making a strategic mistake. If a problem is taking significantly longer than expected, move on to a question you can complete, then return to the difficult one if time permits.'
        ],
        highlights: [
          { term: 'weak documentation of the design process', description: 'Skipping or rushing the research, sketching, and development stages of the assignment. The examiner marks the process, not just the final model.' },
          { term: 'misread the question setup', description: 'Plotting the given data (points, lines, planes) incorrectly at the start of a question. This causes the entire solution to be wrong, even if the method is correct.' }
        ],
        bullets: [
          'Using blunt instruments — a dull compass or worn pencil destroys accuracy',
          'Skipping the design process documentation in the assignment',
          'Plotting given data incorrectly and building an entire solution on a wrong foundation',
          'Spending too long on one difficult question and leaving easier ones unanswered',
          'Producing CAD models without proper technical drawings (orthographic, sectional views)'
        ],
      },
      /* ---- Section 5: Study Techniques ---- */
      {
        title: 'How to Study DCG',
        eyebrow: '05 // Study Techniques',
        paragraphs: [
          'DCG is a subject you **study by doing, not by reading**. The most effective revision method is to work through past paper questions with your drawing instruments. Set up each problem, execute the construction, and check your solution against the marking scheme. There is no shortcut — spatial reasoning and drawing precision are skills that develop through repetition. Aim to complete at least **two full construction problems per study session**.',
          'Create a [[method bank]] for the standard construction types. For each type of problem — finding a true length, determining the angle between two planes, developing a surface, constructing an intersection of solids — write out the step-by-step method and practise it until it becomes automatic. The written exam draws from a finite set of problem types, and knowing the method for each one gives you a systematic approach to every question.',
          'For the student assignment, develop your [[CAD skills]] systematically. If you are using SolidWorks, make sure you are confident with sketches, extrusions, revolves, fillets, chamfers, patterns, assemblies, and drawing views. Practise creating a simple object from scratch — sketch, extrude, add features, create an assembly, and produce a drawing sheet with proper dimensions. The faster and more confident you are with the software, the more time you can spend on design quality.',
          'Study the [[marking scheme]] for past exams carefully. In DCG, the marking scheme reveals exactly which construction steps earn marks. Sometimes a partial construction — correctly identifying a true length or plotting a key point — earns significant marks even if you do not complete the full solution. Understanding this means you know exactly where to focus your effort during the exam.'
        ],
        highlights: [
          { term: 'method bank', description: 'A personal reference of step-by-step construction methods for each standard problem type. Your most valuable revision resource for the written exam.' },
          { term: 'CAD skills', description: 'Proficiency with 3D modelling software (typically SolidWorks). Essential for the student assignment — sketches, features, assemblies, and drawing views.' },
          { term: 'marking scheme', description: 'The SEC\'s official guide to how marks are awarded for each question. In DCG, it reveals which construction steps earn marks, even in incomplete solutions.' }
        ],
      },
      /* ---- Section 6: Action Plan ---- */
      {
        title: 'Your DCG Action Plan',
        eyebrow: '06 // Action Plan',
        paragraphs: [
          'If your student assignment is not yet complete, **prioritise it immediately** — it is 40% of your grade. Ensure you have documented your design process (research, sketches, development), produced quality CAD models with proper rendering, and included compliant technical drawings. A polished assignment is the single most impactful thing you can do for your DCG grade.',
          'For the written exam, build your method bank for the core problem types: true lengths, true shapes, angles between planes, surface developments, and solid intersections. Practise each type until the construction method is automatic. Then work through **at least four full past papers** with instruments, under timed conditions, to build both speed and accuracy.',
          'Set a concrete target: finish your assignment to a high standard at least **two weeks before the deadline**, complete your method bank covering all standard construction types, and work through enough past paper questions that you can identify and execute any standard problem within the allotted time. DCG rewards preparation — the more constructions you have practised, the more confident and accurate you will be in the exam hall.'
        ],
        highlights: [
          { term: 'method bank', description: 'Step-by-step construction procedures for each problem type — your systematic preparation tool for the written exam.' }
        ],
        commitmentText:
          'I will work through one full past paper DCG question this week and identify any gaps in my method bank.',
      },
    ],
  },

  /* ================================================================
   * TECHNOLOGY — Higher Level
   * ================================================================ */
  'technology': {
    subjectId: 'technology',
    subjectName: 'Technology',
    moduleNumber: '27',
    moduleTitle: 'Mastering Technology',
    moduleSubtitle: 'Your Complete Technology Guide',
    moduleDescription:
      'Navigate the Technology exam and project — understand the design brief, the written paper, and how marks are allocated across both components.',
    themeName: 'indigo',
    sections: [
      /* ---- Section 1: Exam Structure ---- */
      {
        title: 'How Technology Actually Works',
        eyebrow: '01 // Exam Structure',
        paragraphs: [
          'Leaving Certificate Technology is a subject that combines **theoretical knowledge with a major design-and-build project**. The assessment is split approximately **50/50 between the written exam and the Design & Make Project**. This balance means that what you create in the workshop and document in your design folio is worth just as much as the paper you sit in June.',
          'The [[written exam]] covers the theoretical foundations of the subject: materials and their properties, technology systems (mechanisms, electronics, pneumatics), design theory, and the impact of technology on society. The paper is structured with short-answer questions and longer questions requiring detailed explanations, diagrams, and analysis. There is typically a choice of questions, allowing you to focus on your stronger topics.',
          'The [[Design & Make Project]] is a substantial piece of work that includes two equally important elements: the [[design folio]] (your documented design process) and the [[artefact]] (the physical product you build). The folio is not a secondary document — it carries significant marks and must demonstrate a genuine design process, from identifying the problem through research, ideation, development, and evaluation.',
          'What distinguishes Technology from subjects like Construction Studies or Engineering is the emphasis on the **design process itself**. While those subjects focus heavily on craftsmanship and manufacturing quality, Technology places significant weight on your ability to identify a need, research solutions, develop ideas, iterate on designs, and evaluate outcomes. The artefact demonstrates that you can build; the folio demonstrates that you can think like a designer.'
        ],
        highlights: [
          { term: 'written exam', description: 'Covers materials science, technology systems (mechanisms, electronics, pneumatics), design theory, and technology\'s impact on society. Worth approximately 50% of the total mark.' },
          { term: 'Design & Make Project', description: 'A substantial design-and-build project worth approximately 50% of the total mark. Includes both the design folio (documentation) and the artefact (built product).' },
          { term: 'design folio', description: 'The documented portfolio of your design process — research, ideation, development, working drawings, and evaluation. Carries a significant portion of the project marks.' },
          { term: 'artefact', description: 'The physical product you build for your project. Assessed on quality of construction, finish, functionality, and adherence to your design specification.' }
        ],
      },
      /* ---- Section 2: Marking Criteria ---- */
      {
        title: 'What the Examiner Rewards',
        eyebrow: '02 // Marking Criteria',
        paragraphs: [
          'On the written paper, examiners reward **applied understanding**. They do not want you to simply list properties of materials — they want you to explain why a specific material is appropriate for a specific application. If asked about the properties of acrylic, the top answers will mention transparency, ease of machining, and thermoforming capability, then link those properties to real applications. Using terminology like [[thermoplastic]], [[thermoset]], [[ferrous]], and [[non-ferrous]] correctly signals genuine understanding.',
          'For the technology systems questions, the examiner looks for clear explanations supported by [[circuit diagrams]] or [[mechanism diagrams]]. Whether the question involves a 555 timer circuit, a gear train, or a pneumatic actuator, the answer should include a labelled diagram showing how the system works, followed by a written explanation of the function of each component. Diagrams are not optional — they carry substantial marks.',
          'On the Design & Make Project, the folio is assessed for [[quality of the design process]]. Examiners want to see genuine investigation (not just Google screenshots), creative ideation (multiple concepts, not just the one you built), iterative development (showing how your design evolved), detailed working drawings, and honest evaluation. The best folios tell a story of how the designer solved a real problem.',
          'The artefact is assessed on construction quality, functionality, and finish — but it is also assessed on **how well it matches the design specification in your folio**. If your folio says the product will perform a certain function or meet a certain dimension, and the artefact does not deliver, you lose marks on both the artefact and the folio. Consistency between documentation and product is essential.'
        ],
        highlights: [
          { term: 'thermoplastic', description: 'A plastic that softens when heated and hardens when cooled, and can be reheated repeatedly (e.g., acrylic, polypropylene, ABS). Commonly examined in materials questions.' },
          { term: 'thermoset', description: 'A plastic that undergoes a chemical change when heated and cannot be reshaped (e.g., epoxy resin, melamine). Contrasted with thermoplastics in exam questions.' },
          { term: 'ferrous', description: 'Metals that contain iron (e.g., mild steel, cast iron, stainless steel). A key classification in materials science questions.' },
          { term: 'non-ferrous', description: 'Metals that do not contain iron (e.g., aluminium, copper, brass). Often compared with ferrous metals in exam questions.' },
          { term: 'circuit diagrams', description: 'Schematic representations of electronic circuits using standard symbols. Must be clear, correctly labelled, and include component values where relevant.' },
          { term: 'mechanism diagrams', description: 'Drawings showing how mechanical systems (gears, linkages, cams) are arranged and function. Should include labels and arrows showing motion direction.' },
          { term: 'quality of the design process', description: 'The depth and authenticity of research, ideation, development, and evaluation documented in the folio. Marks reward the journey, not just the destination.' }
        ],
      },
      /* ---- Section 3: High-Value Zones ---- */
      {
        title: 'Where Your Marks Are',
        eyebrow: '03 // High-Value Zones',
        paragraphs: [
          'The **Design & Make Project accounts for roughly 50% of your grade**, and within that, the [[design folio]] is where many students leave the most marks on the table. The folio is not an afterthought — it is a major component of the project mark. A well-structured folio with genuine research, creative ideation, clear development, and thoughtful evaluation can earn you marks that are entirely within your control. You do not need to be a gifted craftsperson to produce an excellent folio.',
          'Within the written exam, the [[materials section]] is the most consistently examined and highest-value area. Questions about material properties, selection, and processing appear every year. Understanding the properties of common materials (mild steel, aluminium, acrylic, MDF, plywood), knowing how to process them (cutting, shaping, joining, finishing), and being able to justify material choices for given applications covers a huge portion of the paper.',
          'The [[technology systems]] questions — covering electronics, mechanisms, and pneumatics — are another high-value zone. These questions often involve drawing and explaining a system that performs a specific function. If you can draw a basic transistor switching circuit, explain a gear train, or describe a pneumatic system with valves and actuators, you have access to reliable marks that many students avoid because the content seems technical.',
          'The [[design theory]] section covers the design process, product analysis, and the impact of technology on society and the environment. These questions are more discursive and accessible — they ask you to analyse, evaluate, and reflect rather than recall technical facts. Well-prepared students who can discuss sustainability, planned obsolescence, ergonomics, and the iterative design process can score highly here with good written expression.'
        ],
        highlights: [
          { term: 'design folio', description: 'The documented design process for your project. Carries substantial marks — a strong folio can significantly boost your project score even if the artefact is modest.' },
          { term: 'materials section', description: 'Covers properties, classification, selection, and processing of metals, plastics, timber, and composites. The most consistently examined area of the written paper.' },
          { term: 'technology systems', description: 'Electronics (circuits, components), mechanisms (gears, linkages, cams), and pneumatics (actuators, valves, circuits). Diagram-heavy questions with reliable mark allocations.' },
          { term: 'design theory', description: 'Covers the design process, product analysis, sustainability, ergonomics, and technology\'s societal impact. More discursive, rewarding thoughtful analysis.' }
        ],
      },
      /* ---- Section 4: Common Pitfalls ---- */
      {
        title: 'What Costs You Marks',
        eyebrow: '04 // Common Pitfalls',
        paragraphs: [
          'The single biggest mistake in Technology is producing a [[thin design folio]]. Too many students treat the folio as an annoying box-ticking exercise and rush through it to spend more time on the artefact. This is a strategic disaster. The folio carries significant marks, and a thin folio with minimal research, a single design concept, and a one-paragraph evaluation will cap your project score regardless of how well-built your artefact is.',
          'On the written paper, the most common error is [[material confusion]] — mixing up properties of different materials or failing to distinguish between categories. Calling mild steel "non-ferrous" or describing acrylic as a thermoset immediately tells the examiner you do not understand the fundamentals. These classification errors are easy to avoid with basic revision but costly if they occur.',
          'Another written paper pitfall is **avoiding technology systems questions**. Students who skip electronics or pneumatics because the content feels intimidating are giving up accessible marks. The questions often follow standard patterns — draw a circuit, explain how it works, identify the function of each component. A student who learns three or four standard circuits and their functions can score well without needing to be an electronics expert.',
          'On the artefact, the most damaging error is [[poor finish quality]]. A product that functions well but has rough edges, visible tool marks, inconsistent paint, or sloppy joints will lose marks. Finish is one of the first things the examiner notices, and it strongly influences the overall impression of your work. Budget time specifically for finishing — sanding, filling, painting, and quality checking.'
        ],
        highlights: [
          { term: 'thin design folio', description: 'A folio that lacks depth — minimal research, few design alternatives, rushed development, and superficial evaluation. Caps your project score regardless of artefact quality.' },
          { term: 'material confusion', description: 'Mixing up material properties or classifications (e.g., calling a thermoplastic a thermoset, or confusing ferrous and non-ferrous). Basic errors that cost marks.' },
          { term: 'poor finish quality', description: 'Rough surfaces, visible tool marks, uneven paint, or sloppy joins on the artefact. Finish carries distinct marks and creates the examiner\'s first impression.' }
        ],
        bullets: [
          'Rushing the design folio — it carries substantial marks and rewards effort directly',
          'Confusing material classifications — know your ferrous vs non-ferrous, thermoplastic vs thermoset',
          'Avoiding technology systems questions on the written paper out of intimidation',
          'Building an artefact that does not match the specification in your folio',
          'Neglecting the finish — sanding, painting, and quality checking are all marked'
        ],
      },
      /* ---- Section 5: Study Techniques ---- */
      {
        title: 'How to Study Technology',
        eyebrow: '05 // Study Techniques',
        paragraphs: [
          'Technology study works best when you integrate **theory and practice**. For materials, create a [[comparison table]] that lists each material with its properties, advantages, disadvantages, and typical applications. Then test yourself: if given a design scenario (e.g., "a lightweight, transparent safety guard"), can you select the appropriate material and justify your choice? This application-based approach is exactly how the exam tests you.',
          'For technology systems, the key is to **learn by drawing**. Create clear, labelled diagrams of standard electronic circuits (555 timer, transistor switch, potential divider), mechanical systems (gear trains, four-bar linkages, cam and follower), and pneumatic circuits (single and double-acting cylinders with 3/2 and 5/2 valves). Practise drawing each from memory until you can reproduce them accurately and explain how they work.',
          'For the Design & Make Project, treat your folio as an **ongoing document**. Add to it after every workshop session and every design decision. Photograph your work at each stage. Write reflections while the experience is fresh. The best folios are built gradually over months, not assembled in a sprint at the end. Use [[design process templates]] to structure each section: problem identification, research, specification, ideation, development, realisation, testing, and evaluation.',
          'When preparing for the written exam, work through [[past papers with marking schemes]]. Pay close attention to how marks are allocated — you will notice that diagrams often carry as many marks as written explanations, and that specific terminology earns more than vague descriptions. Use the marking scheme to calibrate the level of detail your answers need. Then practise writing answers that match that standard.'
        ],
        highlights: [
          { term: 'comparison table', description: 'A structured reference listing each material with its properties, pros, cons, and applications. Enables quick revision and supports material-selection questions.' },
          { term: 'design process templates', description: 'Structured frameworks for each stage of the design folio — ensuring you cover research, ideation, development, and evaluation with appropriate depth.' },
          { term: 'past papers with marking schemes', description: 'Previous exam papers and their official marking guides. Reveal how marks are allocated, what level of detail is expected, and which topics recur.' }
        ],
      },
      /* ---- Section 6: Action Plan ---- */
      {
        title: 'Your Technology Action Plan',
        eyebrow: '06 // Action Plan',
        paragraphs: [
          'Start with your Design & Make Project — specifically your folio. Audit its current state against the full design process: do you have genuine research, multiple design concepts, evidence of development, working drawings, and an honest evaluation? If any section is thin, **that is your immediate priority**. The folio is the area where effort translates most directly into marks, and you have full control over its quality.',
          'For the written paper, build your materials knowledge first (it is the most reliable area), then develop your technology systems diagrams, and finally prepare your design theory responses. Create your comparison table and diagram bank, then test yourself by working through past paper questions under timed conditions. Aim for at least **four complete past papers** before the exam.',
          'Set your milestones: design folio complete and polished at least **two weeks before the deadline**, artefact finished with quality surface finish, and written exam revision covering materials, systems, and design theory. If you invest properly in the folio and artefact, you walk into the written exam with half your grade already earned — and that changes the entire pressure dynamic.'
        ],
        highlights: [
          { term: 'design process', description: 'The full cycle of design work — research, ideation, development, realisation, and evaluation. The backbone of your folio marks.' }
        ],
        commitmentText:
          'I will audit my design folio this week, identify the weakest section, and dedicate two focused sessions to strengthening it.',
      },
    ],
  },
};
