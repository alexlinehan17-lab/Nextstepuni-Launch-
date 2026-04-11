/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type SubjectModuleContent } from './subjectModuleData';

export const HUMANITIES_CONTENT: Record<string, SubjectModuleContent> = {
  // ---------------------------------------------------------------------------
  // HISTORY  (Higher Level)
  // ---------------------------------------------------------------------------
  'history': {
    subjectId: 'history',
    subjectName: 'History',
    moduleNumber: '18',
    moduleTitle: 'Mastering History',
    moduleSubtitle: 'Your Complete History Exam Guide',
    moduleDescription:
      'Master the History exam from the Document Question to the essays — understand how marks are allocated and what the examiner is actually looking for.',
    themeName: 'rose',
    finishButtonText: 'Make History',
    sections: [
      // Section 1 — Exam Structure
      {
        title: 'How History Actually Works',
        eyebrow: '01 // Exam Structure',
        paragraphs: [
          'The Leaving Certificate History Higher Level exam is a single paper lasting **2 hours and 50 minutes**, worth a total of **400 marks**. There is no second paper and no coursework component — everything rides on this one sitting. That makes understanding the layout absolutely critical.',
          'The paper is divided into three sections. [[Section 1]] is the Document Question, which is **compulsory** and worth **100 marks**. You will be given a set of primary or secondary sources on a topic from your course and asked a series of structured questions about them. This is the only part of the exam where you work directly with sources rather than writing from memory.',
          'In [[Section 2]] you answer on Ireland topics. You must write **two essays**, each worth **100 marks**, chosen from a range of topics in early modern and modern Irish history. Then in [[Section 3]] you answer **one essay** worth **100 marks** on a Europe and the wider world topic. That gives you three full essays plus the document question — four answers in total.',
          'Time management is everything. You have roughly **40 minutes** for the Document Question and about **43 minutes** for each essay. Many students run out of time on the final essay because they spend too long on earlier answers. Plan your timing before you open the paper.'
        ],
        highlights: [
          { term: 'Section 1', description: 'The Document Question: compulsory, 100 marks, based on source analysis of primary and secondary documents.' },
          { term: 'Section 2', description: 'Ireland topics: two essays required, each worth 100 marks, covering early modern and modern Irish history.' },
          { term: 'Section 3', description: 'Europe and the wider world: one essay required, worth 100 marks, covering European or world history topics.' }
        ]
      },
      // Section 2 — Marking Criteria
      {
        title: 'What the Examiner Rewards',
        eyebrow: '02 // Marking Criteria',
        paragraphs: [
          'History examiners are looking for more than just facts dumped onto the page. The marking scheme rewards [[structured argument]] above everything else. An essay that is well-organised with a clear introduction, developed body paragraphs, and a definite conclusion will always outscore one that has more facts but no shape.',
          'For the Document Question, examiners reward your ability to **comprehend**, **compare**, and **critically evaluate** the sources provided. You need to show you can extract information from documents, identify bias or perspective, and place the sources in their historical context. Direct quotation from the documents scores well when used to support a point.',
          'In essays, the key scoring unit is the [[SIP]] — a Significant Individual Point. Each SIP is a distinct historical point that is explained and, ideally, supported with evidence. A strong essay will contain **5 to 7 well-developed SIPs** in the body paragraphs. Examiners allocate marks per SIP, so more developed points means more marks.',
          'Your [[introduction]] should define the scope of your answer and signal the argument you will make. The conclusion should draw your points together and offer a judgement. Both the introduction and conclusion carry marks — they are not optional extras. An essay without either will lose marks even if the body is excellent.'
        ],
        highlights: [
          { term: 'structured argument', description: 'Essays must follow a clear structure: introduction setting up the argument, developed body paragraphs with SIPs, and a conclusion with a judgement.' },
          { term: 'SIP', description: 'Significant Individual Point — the basic scoring unit in History essays. Each SIP is a distinct historical point, explained and supported with evidence.' },
          { term: 'introduction', description: 'Must define the topic, set the scope, and indicate your line of argument. Carries its own marks in the marking scheme.' }
        ]
      },
      // Section 3 — High-Value Zones
      {
        title: 'Where Your Marks Are',
        eyebrow: '03 // High-Value Zones',
        paragraphs: [
          'The [[Document Question]] is the single highest-value opportunity on the entire paper. It is worth **100 marks** — a full 25% of your grade — and it is the most accessible section because **the answers are in the documents in front of you**. You do not need to recall facts from memory; you need to read carefully and respond to what is on the page. Students who prepare well for the Document Question format can score 80+ marks here relatively comfortably.',
          'Within the Document Question, the **contextualisation** sub-question (typically worth 20 marks) asks you to write a short paragraph setting the documents in their historical context. This is the one part where you do need memorised knowledge, so prepare the context for each topic you study. The **comprehension** and **comparison** questions are the easiest marks on the paper — they literally ask you to find information in the sources and compare what two documents say.',
          'For the essays, [[Section 2]] gives you the most choice because you answer two from a range of Ireland topics. If you have studied three Ireland topics thoroughly, you will always find two comfortable questions. Many students only study two topics, which leaves zero margin if a question is phrased awkwardly.',
          'The final essay in [[Section 3]] is where many students drop marks — not because the question is harder, but because they are running out of time. If you protect your timing, this essay is worth the same 100 marks as the others and should be treated with the same seriousness.'
        ],
        highlights: [
          { term: 'Document Question', description: 'Worth 100 marks (25% of total). Answers come from the sources provided, making it the most accessible high-value section of the paper.' },
          { term: 'Section 2', description: 'Two Ireland essays, 100 marks each. Study at least three topics to guarantee comfortable choice on the day.' },
          { term: 'Section 3', description: 'One Europe/world essay, 100 marks. Often where students lose marks due to poor time management rather than lack of knowledge.' }
        ]
      },
      // Section 4 — Common Pitfalls
      {
        title: 'What Costs You Marks',
        eyebrow: '04 // Common Pitfalls',
        paragraphs: [
          'The number one killer in History is [[time mismanagement]]. Students spend too long on the Document Question or their first essay and then rush or fail to finish their final essay. Losing an entire essay means losing 100 marks — that is the difference between an H1 and an H4. Use a watch. Set strict time limits. Move on even if you feel you could write more.',
          'Another common mistake is [[narrative answers]] — telling the story of what happened without making analytical points. The examiner is not looking for a timeline; they want you to argue, explain significance, assess causes and consequences. "This happened, then this happened" gets far fewer marks than "This happened because... and its significance was..."',
          'In the Document Question, students lose marks by **not using the documents**. If the question says "with reference to Document A," you must quote or paraphrase from Document A. Writing a general answer from your own knowledge when the question asks about the documents will score poorly.',
          'Finally, many students make the mistake of [[topic gambling]] — studying only the bare minimum number of topics and hoping the right questions come up. If you have studied exactly two Ireland topics and one of them has an awkward question, you are trapped. Always have a backup topic prepared to at least essay-plan level.'
        ],
        highlights: [
          { term: 'time mismanagement', description: 'The most common reason for lost marks. Failing to finish the last essay costs 100 marks — protect your timing above all else.' },
          { term: 'narrative answers', description: 'Telling the story without analysis. Examiners reward argument and explanation of significance, not chronological retelling.' },
          { term: 'topic gambling', description: 'Studying the minimum number of topics. If a question is awkward, you have no fallback. Always prepare one extra topic.' }
        ]
      },
      // Section 5 — Study Techniques
      {
        title: 'How to Study History',
        eyebrow: '05 // Study Techniques',
        paragraphs: [
          'History is a subject where [[essay plans]] are worth their weight in gold. For every topic, write out a one-page plan with your introduction, 5-7 SIPs with key evidence for each, and a conclusion. Practise writing from the plan under timed conditions. On exam day, you will spend 2-3 minutes writing a quick plan before each essay, and this habit starts now.',
          'For the Document Question, practise with **past papers**. The format barely changes from year to year: comprehension, comparison, criticism, and contextualisation. Do at least five past Document Questions under timed conditions. You will quickly see the patterns in how questions are asked and learn exactly how to structure your responses.',
          'Use [[key-evidence flashcards]] for each topic. On one side, write the SIP (e.g., "Parnell used obstructionism to gain attention at Westminster"). On the other side, write the supporting evidence — dates, names, statistics, quotes. Test yourself regularly using active recall rather than just re-reading notes.',
          'Group your topics into [[themes]] rather than studying them as isolated events. For example, if you are studying the Irish independence movement, connect the themes of leadership, public opinion, British policy, and international context. This thematic understanding lets you adapt to any question wording on the day.'
        ],
        highlights: [
          { term: 'essay plans', description: 'One-page structured outlines with introduction, 5-7 SIPs with evidence, and conclusion. The single most effective study tool for History.' },
          { term: 'key-evidence flashcards', description: 'Active recall cards with a historical point on one side and supporting evidence (dates, names, quotes) on the other.' },
          { term: 'themes', description: 'Group topics by recurring themes (leadership, public opinion, policy) rather than studying events in isolation. Builds adaptable knowledge.' }
        ]
      },
      // Section 6 — Action Plan
      {
        title: 'Your History Action Plan',
        eyebrow: '06 // Action Plan',
        paragraphs: [
          'Start by listing your topics: at least **three Ireland topics** and **two Europe/world topics**. For each topic, build a complete set of [[essay plans]] with 5-7 SIPs and supporting evidence. This is your exam toolkit — everything else is supplementary.',
          'Next, commit to doing one **timed Document Question** per week from past papers. Mark it yourself using the published marking schemes from examinations.ie. Track your scores and identify which question types (comprehension, comparison, criticism) you need to sharpen.',
          'Finally, in the last four weeks before the exam, switch to full **timed essay practice**. Write one full essay (43 minutes) at least three times a week. Review against the marking scheme, count your SIPs, and check that every essay has a clear introduction and conclusion. This is the drill that turns your knowledge into exam performance.'
        ],
        highlights: [
          { term: 'essay plans', description: 'Your core study tool. Build a plan for every potential question across all your topics before you start timed practice.' }
        ],
        bullets: [
          'Build essay plans for all topics — minimum 3 Ireland, 2 Europe/world',
          'Complete one timed Document Question per week from past papers',
          'Practise timed essays (43 minutes each) at least 3 times per week in the final month',
          'Use the published marking schemes to self-assess and count your SIPs',
          'Review your contextualisation knowledge for each Document Question topic'
        ],
        commitmentText:
          'I will build my essay plan toolkit this week and complete my first timed Document Question by Sunday.'
      }
    ]
  },

  // ---------------------------------------------------------------------------
  // GEOGRAPHY  (Higher Level)
  // ---------------------------------------------------------------------------
  'geography': {
    subjectId: 'geography',
    subjectName: 'Geography',
    moduleNumber: '19',
    moduleTitle: 'Mastering Geography',
    moduleSubtitle: 'Your Complete Geography Exam Guide',
    moduleDescription:
      'Break down the Geography exam by section — short questions, long questions, and the Geographical Investigation — and learn where to pick up the best marks.',
    themeName: 'emerald',
    finishButtonText: 'Chart Your Course',
    sections: [
      // Section 1 — Exam Structure
      {
        title: 'How Geography Actually Works',
        eyebrow: '01 // Exam Structure',
        paragraphs: [
          'Leaving Certificate Geography Higher Level has two assessment components. The **written exam** is a single paper lasting **2 hours and 50 minutes**, worth **80%** of your final grade. The [[Geographical Investigation]] (GI) is a separate fieldwork-based project worth **20%** of your grade. Both matter enormously.',
          'The written paper is worth **400 marks** and is divided into sections. It opens with [[Short Questions]] worth **80 marks** — you answer questions from a selection covering the full syllabus. These are quick-fire factual and skills-based questions, typically taking about 25-30 minutes.',
          'The long questions are where the bulk of your marks sit. You answer questions across the core and elective areas: [[Physical Geography]] (including your elective — Geoecology or the Atmosphere), [[Regional Geography]] (covering an Irish region and a continental/sub-continental region), and [[Human and Economic Geography]] along with an option topic. Each long question is typically worth **80 marks**.',
          'You also need to be prepared for [[OSI map]] work, which can appear in any section. Map-reading skills — grid references, measuring distance, interpreting contour patterns — are tested regularly and are reliable marks if you practise them.'
        ],
        highlights: [
          { term: 'Geographical Investigation', description: 'The GI is a fieldwork project worth 20% of your final grade. It is submitted separately from the written exam and must follow a specific structure.' },
          { term: 'Short Questions', description: '80 marks, broad syllabus coverage. Quick factual and skills-based questions that open the paper.' },
          { term: 'Physical Geography', description: 'Core physical processes plus your chosen elective (Geoecology or the Atmosphere). Diagrams are essential here.' },
          { term: 'Regional Geography', description: 'Covers an Irish region and a continental region. Requires detailed case study knowledge.' },
          { term: 'OSI map', description: 'Ordnance Survey Ireland maps may appear in any section. Grid references, scale, contour interpretation are commonly tested.' }
        ]
      },
      // Section 2 — Marking Criteria
      {
        title: 'What the Examiner Rewards',
        eyebrow: '02 // Marking Criteria',
        paragraphs: [
          'Geography examiners reward **specificity** above all else. Vague, general answers about "the environment" or "human activity" will not score well. The marking scheme is built around [[SRPs]] — Significant Relevant Points. Each SRP is a distinct geographical point that is relevant to the question and explained clearly. More developed SRPs means more marks.',
          'For long questions, the examiner wants to see [[case studies]] used as evidence. If you are discussing urbanisation, name specific cities and cite real data. If you are explaining a physical process, describe a real-world example. Generic answers without case study detail will hit a ceiling regardless of how well-written they are.',
          'Diagrams are a major scoring opportunity in Geography. A well-labelled [[annotated diagram]] of a physical process (fold mountains, the water cycle, soil profile) can be worth **10-15 marks** on its own. The examiner is looking for clear labels, accurate representation, and annotations that explain what is happening — not just a pretty picture.',
          'In the short questions section, marks are awarded for **precision**. One-word or one-sentence answers are often sufficient. Do not write a paragraph when a sentence will do — save your time and energy for the long questions where developed answers are rewarded.'
        ],
        highlights: [
          { term: 'SRPs', description: 'Significant Relevant Points — the basic scoring unit in Geography. Each distinct geographical point that is relevant and explained earns marks.' },
          { term: 'case studies', description: 'Real-world examples with specific names, places, and data. Essential for moving beyond generic answers in long questions.' },
          { term: 'annotated diagram', description: 'A labelled diagram with explanatory annotations. Can be worth 10-15 marks and is often the easiest way to score in Physical Geography.' }
        ]
      },
      // Section 3 — High-Value Zones
      {
        title: 'Where Your Marks Are',
        eyebrow: '03 // High-Value Zones',
        paragraphs: [
          'The [[Geographical Investigation]] is the single most important strategic element in Geography. It is worth **20% of your final grade** and it is completed **before the exam** — meaning you can perfect it without time pressure. A well-structured GI with clear methodology, accurate data presentation, and thoughtful analysis can score close to full marks. Many students treat the GI as an afterthought; smart students treat it as a guaranteed grade booster.',
          'On the written paper, the [[Short Questions]] are your fastest route to marks. At **80 marks**, they represent 20% of the paper, and many of them are straightforward factual recall or skills questions. Spending 25-30 minutes here and picking up 60+ marks is very achievable with solid syllabus coverage.',
          'In the long questions, [[Physical Geography with diagrams]] is where prepared students clean up. Questions on processes like plate tectonics, river formation, or atmospheric processes lend themselves to annotated diagrams that carry significant marks. If you have practised drawing and labelling these diagrams, you can score heavily here.',
          'Regional Geography is another high-value area because the questions tend to be predictable. If you know one Irish region and one continental region in genuine detail — with statistics, place names, and economic data — you can answer almost any question that comes up on those regions.'
        ],
        highlights: [
          { term: 'Geographical Investigation', description: 'Worth 20% of your final grade, completed before the exam. Treat it as a guaranteed grade booster, not an afterthought.' },
          { term: 'Short Questions', description: '80 marks, quick to answer. A well-prepared student can pick up 60+ marks in under 30 minutes here.' },
          { term: 'Physical Geography with diagrams', description: 'Annotated diagrams on physical processes carry heavy marks and are highly predictable — perfect for preparation.' }
        ]
      },
      // Section 4 — Common Pitfalls
      {
        title: 'What Costs You Marks',
        eyebrow: '04 // Common Pitfalls',
        paragraphs: [
          'The biggest mistake in Geography is [[neglecting the GI]]. Students who rush their Geographical Investigation or submit a poorly structured project are throwing away 20% of their grade before they even sit down for the exam. The GI should be treated as seriously as any exam section — it requires a clear aim, proper methodology, well-presented data, and a reasoned conclusion.',
          'On the written paper, the most common error is [[vague generalisation]]. Writing that "climate change affects the environment" without specifying how, where, and with what evidence is the kind of answer that examiners see constantly and reward poorly. Every point you make should be tied to a specific place, process, or data point.',
          'Students also lose marks by **skipping diagrams**. If a question asks you to "describe and explain" a physical process, a labelled diagram is almost always expected. Writing a text-only answer when a diagram would illustrate the process more clearly means leaving marks on the table.',
          'Finally, [[poor map skills]] cost marks in the short questions. Reading grid references incorrectly, miscalculating distances, or failing to interpret contour patterns are avoidable errors that come down to practice. OSI map questions appear almost every year — there is no excuse for not being ready for them.'
        ],
        highlights: [
          { term: 'neglecting the GI', description: 'Rushing the Geographical Investigation is the single most costly mistake. It is 20% of your grade and can be perfected before the exam.' },
          { term: 'vague generalisation', description: 'Generic answers without specific places, data, or case studies. The marking scheme rewards precision and punishes vagueness.' },
          { term: 'poor map skills', description: 'Grid references, scale, and contour interpretation are tested regularly. Avoidable errors from lack of practice.' }
        ]
      },
      // Section 5 — Study Techniques
      {
        title: 'How to Study Geography',
        eyebrow: '05 // Study Techniques',
        paragraphs: [
          'Geography rewards a [[case study bank]] approach. For each topic area, build a set of case studies with specific names, locations, statistics, and outcomes. For example, for urbanisation you might have case studies on Dublin (Irish context), Mumbai (developing world), and Copenhagen (sustainable urban planning). Write these out on revision cards and test yourself regularly.',
          'Practise your [[diagrams]] until you can draw them from memory in under three minutes. For Physical Geography especially, you need annotated diagrams for every major process: plate boundaries, river stages, coastal erosion, atmospheric circulation, soil formation. Draw them repeatedly — the act of drawing reinforces the knowledge far more effectively than reading about it.',
          'For the Geographical Investigation, follow the [[scientific method structure]]: aim, hypothesis, methodology, data collection, data presentation (graphs, maps, photos), analysis, and conclusion. Your GI should read like a mini research project. Use your teacher\'s feedback rounds wisely — each draft should improve significantly.',
          'Use past papers strategically. Geography questions are remarkably consistent in their phrasing. The same topics come up in similar formats year after year. By doing **five years of past papers**, you will recognise the patterns and know exactly what type of answer each question demands.'
        ],
        highlights: [
          { term: 'case study bank', description: 'A collection of detailed case studies for each topic area, with specific names, places, statistics, and outcomes on revision cards.' },
          { term: 'diagrams', description: 'Practise drawing annotated diagrams from memory. Three minutes per diagram, every major physical process covered.' },
          { term: 'scientific method structure', description: 'The GI should follow: aim, hypothesis, methodology, data collection, data presentation, analysis, and conclusion.' }
        ]
      },
      // Section 6 — Action Plan
      {
        title: 'Your Geography Action Plan',
        eyebrow: '06 // Action Plan',
        paragraphs: [
          'Start with the GI if it is not yet complete. Treat it as a priority project worth 20% of your grade. Follow the [[scientific method structure]], get teacher feedback on each draft, and make sure your data presentation is clean and professional. This is your easiest route to guaranteed marks.',
          'Next, build your case study bank and diagram set. For each topic area on the syllabus, prepare at least **two detailed case studies** and all relevant annotated diagrams. Test yourself by drawing diagrams from memory and reciting case study details without notes.',
          'In the final weeks, shift to full past papers under timed conditions. Practise the short questions for speed and accuracy, and write at least two full long answers per week. Mark your work against the published schemes and count your SRPs to track improvement.'
        ],
        highlights: [
          { term: 'scientific method structure', description: 'The framework for your GI: aim, hypothesis, methodology, data collection, data presentation, analysis, conclusion.' }
        ],
        bullets: [
          'Complete and polish your Geographical Investigation before anything else',
          'Build a case study bank with 2+ case studies per topic, including specific data',
          'Practise all Physical Geography diagrams until you can draw them from memory',
          'Do short question sets for speed — aim for 60+ out of 80 marks',
          'Complete at least 5 full past papers under timed conditions'
        ],
        commitmentText:
          'I will finalise my GI draft this week and build case study cards for my first two topic areas.'
      }
    ]
  },

  // ---------------------------------------------------------------------------
  // POLITICS & SOCIETY  (Higher Level)
  // ---------------------------------------------------------------------------
  'politics-and-society': {
    subjectId: 'politics-and-society',
    subjectName: 'Politics & Society',
    moduleNumber: '20',
    moduleTitle: 'Mastering Politics & Society',
    moduleSubtitle: 'Your Complete P&S Exam Guide',
    moduleDescription:
      'Navigate the Politics & Society exam — from the citizenship project to the written paper — and understand what the examiner rewards.',
    themeName: 'blue',
    finishButtonText: 'Make Your Voice Heard',
    sections: [
      // Section 1 — Exam Structure
      {
        title: 'How Politics & Society Actually Works',
        eyebrow: '01 // Exam Structure',
        paragraphs: [
          'Politics & Society is one of the newer Leaving Certificate subjects, introduced in 2016, and it works differently from traditional humanities exams. Your final grade is split: the **written examination** is worth **80%** and a [[Citizenship Project]] is worth **20%**. This two-component structure means you can bank a significant portion of your grade before exam day.',
          'The written paper is divided into three sections. [[Section A]] consists of **short-answer questions** worth a total of **80 marks**. You answer from a selection, and these questions test your knowledge of key political concepts, thinkers, and definitions. They are quick and factual.',
          'In [[Section B]] you face **source-based questions** — you are given documents, data, or images and must analyse them. This section tests your ability to interpret information, identify perspectives, and evaluate arguments. It is similar in spirit to the History document question but focused on political and social concepts.',
          'Finally, [[Section C]] requires **extended writing** — longer essay-style responses where you develop arguments on topics such as human rights, globalisation, democracy, or inequality. This is where the heaviest marks sit and where the depth of your understanding is tested. The total paper is worth **400 marks** over approximately **2 hours and 30 minutes**.'
        ],
        highlights: [
          { term: 'Citizenship Project', description: 'Worth 20% of your final grade. A research-based project on a social or political issue, completed during the course and submitted separately.' },
          { term: 'Section A', description: 'Short-answer questions, 80 marks. Tests knowledge of key concepts, political thinkers, and definitions.' },
          { term: 'Section B', description: 'Source-based analysis questions. Requires interpretation of documents, data, or images and evaluation of perspectives.' },
          { term: 'Section C', description: 'Extended writing section. Essay-style responses on major topics like human rights, globalisation, and democracy. Carries the heaviest marks.' }
        ]
      },
      // Section 2 — Marking Criteria
      {
        title: 'What the Examiner Rewards',
        eyebrow: '02 // Marking Criteria',
        paragraphs: [
          'Politics & Society examiners are looking for [[conceptual understanding]] — your ability to demonstrate that you genuinely understand political concepts rather than just memorise definitions. Can you explain what sovereignty means in practice? Can you discuss how different theories of democracy compare? This deeper understanding is what separates top answers from average ones.',
          'In Section B, the examiner rewards your capacity for [[critical analysis]]. When presented with a source, you need to go beyond describing what it says. Identify the perspective it comes from, evaluate the strength of the argument, consider what is missing, and connect it to the broader concepts you have studied. Source analysis that merely paraphrases the document will score poorly.',
          'For the extended writing in Section C, structure and argument matter enormously. The examiner wants to see a clear [[thesis statement]] at the start, developed paragraphs that build an argument with evidence, and a conclusion that synthesises your points. Reference to political thinkers and real-world examples strengthens your answer significantly.',
          'Throughout the paper, examiners reward students who can **apply theory to the real world**. If you are discussing human rights, reference specific cases or events. If you are writing about globalisation, name real organisations, treaties, or countries. Abstract theorising without concrete application will only get you so far.'
        ],
        highlights: [
          { term: 'conceptual understanding', description: 'Demonstrating genuine comprehension of political concepts — not just memorised definitions but the ability to explain, compare, and apply them.' },
          { term: 'critical analysis', description: 'Going beyond description to evaluate perspectives, identify biases, assess argument strength, and connect sources to broader concepts.' },
          { term: 'thesis statement', description: 'A clear, arguable position stated at the beginning of your extended answer. Signals to the examiner that your response has direction and structure.' }
        ]
      },
      // Section 3 — High-Value Zones
      {
        title: 'Where Your Marks Are',
        eyebrow: '03 // High-Value Zones',
        paragraphs: [
          'The [[Citizenship Project]] is your highest-value strategic asset. Worth **20% of your final grade**, it is completed during the year with time to research, draft, and refine. A well-executed project with a clear research question, proper methodology, and thoughtful analysis can score very highly. Unlike the exam, you control the conditions — use that advantage.',
          'On the written paper, [[Section C]] carries the most marks and is where the grade differentiation happens. Students who can write structured, evidence-based essays with clear arguments will outscore those who write vaguely about broad topics. Preparing strong essay frameworks for each major topic area (democracy, human rights, globalisation, power and decision-making) gives you a significant edge.',
          'Section A short questions are your [[quick wins]]. They test definitions, knowledge of thinkers, and basic concepts. If you have revised systematically, these marks come quickly. Aim to spend no more than **25-30 minutes** on Section A and secure as many marks as possible before moving to the more demanding sections.',
          'Section B source analysis is often underestimated. Students who practise source analysis techniques — identifying perspective, evaluating evidence, spotting bias — can score strongly here. The skill set is very transferable from subject to subject, so if you also study History, you already have a head start.'
        ],
        highlights: [
          { term: 'Citizenship Project', description: 'Worth 20% of your grade, completed during the year. A well-researched project with clear methodology is a guaranteed grade booster.' },
          { term: 'Section C', description: 'The extended writing section carries the most marks and is where strong students pull ahead. Structured essays with evidence are rewarded.' },
          { term: 'quick wins', description: 'Section A short answers are fast marks for students who have revised key concepts and definitions systematically.' }
        ]
      },
      // Section 4 — Common Pitfalls
      {
        title: 'What Costs You Marks',
        eyebrow: '04 // Common Pitfalls',
        paragraphs: [
          'The biggest pitfall in Politics & Society is [[shallow description]] instead of analysis. Many students describe what democracy is or list human rights without ever analysing why they matter, how they are contested, or what challenges they face. The exam rewards critical thinking — if your answer could be a Wikipedia summary, it is not analytical enough.',
          'Another common mistake is [[ignoring the project]]. The Citizenship Project is worth 20% of your grade and some students treat it as a minor assignment. A rushed, poorly researched project can cost you the equivalent of a full grade. Invest serious time in your research question, data collection, and written analysis.',
          'In Section B, students lose marks by **not engaging with the sources**. If you are given a document or data set, your answer must reference it directly. Writing a general response about the topic while ignoring the specific source provided will score poorly, no matter how accurate your knowledge is.',
          'Finally, students often struggle with [[time allocation]] in Section C. Extended writing takes time, and if you have spent too long on Sections A and B, you will rush your essays. Since Section C carries the heaviest marks, running out of time here is catastrophic. Plan to leave at least half your exam time for Section C.'
        ],
        highlights: [
          { term: 'shallow description', description: 'Describing concepts without analysing them. The exam rewards critical evaluation, not summary.' },
          { term: 'ignoring the project', description: 'Treating the Citizenship Project as an afterthought. It is worth 20% and can be perfected before the exam.' },
          { term: 'time allocation', description: 'Spending too long on Sections A and B and rushing the high-value Section C essays. Protect your time for extended writing.' }
        ]
      },
      // Section 5 — Study Techniques
      {
        title: 'How to Study Politics & Society',
        eyebrow: '05 // Study Techniques',
        paragraphs: [
          'Build a [[concept map]] for each strand of the syllabus. Politics & Society is organised around big ideas — power, democracy, human rights, globalisation — and each concept connects to others. A visual map showing how concepts relate helps you see the bigger picture and write more connected, analytical answers.',
          'For each major concept, prepare a set of [[thinker references]]. Know who the key political thinkers are and what they argued. For democracy, you might reference John Stuart Mill, Robert Dahl, or Amartya Sen. For human rights, know the Universal Declaration, the ECHR, and key Irish constitutional cases. Being able to name-drop relevant thinkers and frameworks elevates your answers.',
          'Practise [[source analysis]] regularly using past paper materials, newspaper editorials, or political speeches. For each source, ask: What is the perspective? What evidence is used? What is missing? Is the argument convincing? This analytical habit becomes second nature with practice and is directly transferable to Section B.',
          'For the Citizenship Project, choose a topic you genuinely find interesting. Students who are engaged with their topic produce better research, better analysis, and better writing. Frame a clear research question early, gather diverse sources (primary and secondary), and write multiple drafts.'
        ],
        highlights: [
          { term: 'concept map', description: 'A visual diagram showing how key political concepts (power, democracy, rights, globalisation) connect to each other across the syllabus.' },
          { term: 'thinker references', description: 'Key political thinkers and their arguments for each concept. Being able to reference Mill, Rawls, Sen, or Dahl elevates your answers.' },
          { term: 'source analysis', description: 'Regular practice analysing perspectives, evidence, and bias in documents, editorials, and speeches. Builds the skill set for Section B.' }
        ]
      },
      // Section 6 — Action Plan
      {
        title: 'Your Politics & Society Action Plan',
        eyebrow: '06 // Action Plan',
        paragraphs: [
          'If your Citizenship Project is not yet submitted, make it your top priority. Choose a focused research question, gather at least **five diverse sources**, and write a clear analysis with a reasoned conclusion. Get teacher feedback on at least two drafts before final submission.',
          'For the written paper, build concept maps for each syllabus strand and compile your [[thinker references]]. Then practise writing Section C essays under timed conditions — one per week minimum. Mark them against past marking schemes and focus on building structured arguments rather than just recalling information.',
          'In the final weeks, do full past papers under exam conditions. Focus on time management — aim to spend no more than 30 minutes on Section A, allocate time for Section B, and protect at least half your exam time for the high-value Section C essays.'
        ],
        highlights: [
          { term: 'thinker references', description: 'Your bank of key political thinkers and their arguments, organised by concept. Build this early and reference them in every essay.' }
        ],
        bullets: [
          'Complete your Citizenship Project with at least two teacher-reviewed drafts',
          'Build concept maps linking key ideas across all syllabus strands',
          'Compile thinker references for each major concept area',
          'Write one timed Section C essay per week from past papers',
          'Practise source analysis using editorials, speeches, and past paper documents'
        ],
        commitmentText:
          'I will finish my Citizenship Project draft this week and build concept maps for two syllabus strands.'
      }
    ]
  },

  // ---------------------------------------------------------------------------
  // RELIGIOUS EDUCATION  (Higher Level)
  // ---------------------------------------------------------------------------
  'religious-education': {
    subjectId: 'religious-education',
    subjectName: 'Religious Education',
    moduleNumber: '21',
    moduleTitle: 'Mastering Religious Education',
    moduleSubtitle: 'Your Complete RE Exam Guide',
    moduleDescription:
      'Understand how the Religious Education exam works, where the marks are distributed, and how to write clear, structured answers that get top marks.',
    themeName: 'violet',
    finishButtonText: 'Find Your Answers',
    sections: [
      // Section 1 — Exam Structure
      {
        title: 'How Religious Education Actually Works',
        eyebrow: '01 // Exam Structure',
        paragraphs: [
          'The Leaving Certificate Religious Education Higher Level exam is a single paper lasting **2 hours and 30 minutes**, worth a total of **400 marks**. It is divided into three sections of increasing depth and marks, plus a separate [[Coursework Journal]] component that forms part of your overall assessment.',
          '[[Section A]] is the short-answer section, worth **80 marks**. You answer a selection of brief questions that test your knowledge of key terms, figures, beliefs, and practices across the syllabus. These are designed to be quick — factual recall and concise definitions are what is needed here.',
          '[[Section B]] is worth **120 marks** and consists of **response-to-stimulus** material. You are given passages, images, or scenarios and must respond to structured questions about them. This tests your ability to interpret material, connect it to your course knowledge, and discuss its significance. It sits between pure recall and full essay writing in terms of demand.',
          '[[Section C]] is the extended essay section, worth **200 marks** — a full **half of the exam paper**. You write longer, essay-style answers on major topics from the syllabus. This is where the most marks are available and where detailed, structured writing is essential. Topics span the major world religions, moral issues, and the relationship between religion and contemporary life.'
        ],
        highlights: [
          { term: 'Coursework Journal', description: 'A reflective journal completed during the course, covering your engagement with religious education topics. Submitted separately from the exam.' },
          { term: 'Section A', description: 'Short-answer questions worth 80 marks. Tests factual recall of key terms, figures, beliefs, and practices.' },
          { term: 'Section B', description: 'Response to stimulus, 120 marks. Structured questions based on passages, images, or scenarios requiring interpretation and connection to course material.' },
          { term: 'Section C', description: 'Extended essays worth 200 marks (half the paper). Longer responses on major topics requiring detailed, structured writing.' }
        ]
      },
      // Section 2 — Marking Criteria
      {
        title: 'What the Examiner Rewards',
        eyebrow: '02 // Marking Criteria',
        paragraphs: [
          'Religious Education examiners reward [[balanced, respectful engagement]] with religious traditions and moral questions. This does not mean you cannot have a personal perspective — you can and should — but your answers must show that you understand multiple viewpoints. Dismissive or one-sided answers that ignore the complexity of religious questions will score poorly.',
          'In Section C, the examiner is looking for **depth of knowledge** demonstrated through specific references. If you are discussing Christianity, reference specific Scripture passages, Church documents, or theological positions. If you are writing about Islam, reference the Quran, Hadith, or specific scholars. [[Textual references]] show the examiner that your knowledge goes beyond surface-level understanding.',
          'Structure matters in the extended answers. A strong Section C response will have a clear introduction that addresses the question directly, well-developed body paragraphs each making a distinct point, and a conclusion that ties your argument together. The examiner uses [[cumulative marking]] — each relevant, well-explained point adds to your total, so more developed points means more marks.',
          'For Section B, the examiner rewards your ability to **connect the stimulus to your wider knowledge**. Do not just describe what you see in the image or read in the passage — explain its significance, relate it to the beliefs and practices you have studied, and show that you understand the deeper meaning behind the surface.'
        ],
        highlights: [
          { term: 'balanced, respectful engagement', description: 'Show understanding of multiple viewpoints on religious and moral questions. Personal perspective is welcome but must demonstrate genuine engagement with different positions.' },
          { term: 'textual references', description: 'Specific references to sacred texts, Church documents, or theological positions. Demonstrates depth beyond surface-level knowledge.' },
          { term: 'cumulative marking', description: 'Each relevant, well-explained point adds to your mark total. More developed points means more marks — there is no cap on quality.' }
        ]
      },
      // Section 3 — High-Value Zones
      {
        title: 'Where Your Marks Are',
        eyebrow: '03 // High-Value Zones',
        paragraphs: [
          '[[Section C]] is the undisputed high-value zone in Religious Education. At **200 marks**, it accounts for exactly half of the entire paper. If you perform strongly in Section C, you are in a very strong position regardless of minor slips elsewhere. Conversely, a weak Section C makes it nearly impossible to reach the top grades. Your exam preparation should reflect this — the majority of your study time should go toward the extended essay topics.',
          'The [[Coursework Journal]] is your off-exam opportunity. Like the Geography GI or the Politics & Society Citizenship Project, it is completed during the year without exam pressure. A thoughtful, well-written journal that demonstrates genuine reflection on your learning can contribute meaningfully to your grade. Take it seriously from the start of the course.',
          'Within Section B, the [[response-to-stimulus questions]] are often more accessible than students expect. If the stimulus is a passage about a moral issue, for example, you can draw directly from the material provided and connect it to your studied content. Students who practise this format find it becomes a reliable scoring section.',
          'In Section A, the short questions are your fastest marks. They reward systematic revision of key terms and definitions across the syllabus. A student who has used flashcards to learn the core vocabulary of each topic area can move through Section A quickly and confidently, banking marks early in the exam.'
        ],
        highlights: [
          { term: 'Section C', description: '200 marks — half the entire paper. Your performance here largely determines your final grade. Allocate study time accordingly.' },
          { term: 'Coursework Journal', description: 'Completed during the course without exam pressure. Genuine reflection and thoughtful writing can boost your overall grade.' },
          { term: 'response-to-stimulus questions', description: 'Section B questions that provide material to work with. More accessible than many students expect with the right preparation.' }
        ]
      },
      // Section 4 — Common Pitfalls
      {
        title: 'What Costs You Marks',
        eyebrow: '04 // Common Pitfalls',
        paragraphs: [
          'The most common pitfall in Religious Education is [[superficial knowledge]]. Students who have only a surface-level understanding of religious traditions — who know the basics but cannot reference specific texts, practices, or theological positions — will hit a ceiling in Section C. Depth is what the examiner rewards, and depth requires study beyond the textbook summaries.',
          'Another significant error is [[opinion without evidence]]. On moral and ethical questions, some students write personal opinions without grounding them in the religious or philosophical frameworks they have studied. "I think euthanasia is wrong" is not a Religious Education answer. "The Catholic Church opposes euthanasia based on the principle of the sanctity of life, as expressed in Evangelium Vitae" is.',
          'Many students also [[mismanage time across sections]]. Section A and B together are worth 200 marks, and Section C alone is worth 200 marks. If you spend too long on the first two sections, you will not have enough time to develop your Section C essays properly. Aim to finish Sections A and B within the first 60-70 minutes, leaving at least 80 minutes for Section C.',
          'Finally, neglecting the Coursework Journal is a missed opportunity. Students who submit a minimal, last-minute journal are leaving marks on the table. Start your journal entries early in the year and build them up progressively as you study each topic.'
        ],
        highlights: [
          { term: 'superficial knowledge', description: 'Surface-level understanding without specific textual or theological references. Cannot score highly in Section C without depth.' },
          { term: 'opinion without evidence', description: 'Personal views on moral questions without grounding in religious or philosophical frameworks. Examiners require evidence-based reasoning.' },
          { term: 'mismanage time across sections', description: 'Spending too long on Sections A and B at the expense of Section C, which is worth half the paper.' }
        ]
      },
      // Section 5 — Study Techniques
      {
        title: 'How to Study Religious Education',
        eyebrow: '05 // Study Techniques',
        paragraphs: [
          'Build a [[key references sheet]] for each major topic. For each religion or moral issue you study, list the 5-10 most important textual references, documents, or thinkers. For Christianity, this might include Genesis, the Gospels, Vatican II documents, and key encyclicals. For Islam, the key Surahs, Hadith, and the Five Pillars. Having these references at your fingertips transforms your Section C answers.',
          'Use [[comparative tables]] to study different religious perspectives on the same issue. For example, create a table comparing Christian, Islamic, and secular perspectives on the sanctity of life, or on the purpose of suffering. This comparative approach is exactly what examiners reward — it shows balanced engagement with multiple viewpoints.',
          'For Section B, practise with past paper stimulus materials. Get comfortable with the format: read the passage or look at the image, identify the key themes, and then connect those themes to your course material. Do at least **five past Section B questions** under timed conditions to build confidence with this format.',
          'For the Coursework Journal, write reflective entries as you go through the course rather than trying to write them all at the end. A journal that shows genuine progression in your thinking and engagement with the material is far more impressive than one clearly written in a rush.'
        ],
        highlights: [
          { term: 'key references sheet', description: 'A list of the 5-10 most important textual references, documents, and thinkers for each major topic. Your toolkit for Section C depth.' },
          { term: 'comparative tables', description: 'Tables comparing different religious or philosophical perspectives on the same issue. Builds the balanced analysis examiners reward.' }
        ]
      },
      // Section 6 — Action Plan
      {
        title: 'Your Religious Education Action Plan',
        eyebrow: '06 // Action Plan',
        paragraphs: [
          'Start by identifying your Section C topics — these are the ones you will write extended essays on. For each topic, build your [[key references sheet]] with specific textual citations and theological positions. This is the foundation of everything else.',
          'Next, create comparative tables for at least three major moral or theological issues where multiple perspectives apply. Practise writing Section C essays under timed conditions — one per week — and mark them against past marking schemes to track your development.',
          'Keep your Coursework Journal up to date throughout the year. Write reflective entries after each topic, connecting what you have learned to your own thinking and to the wider world. A strong journal is marks in the bank before exam day.'
        ],
        highlights: [
          { term: 'key references sheet', description: 'Your essential study tool: specific textual citations and theological positions for each major topic, ready to deploy in Section C.' }
        ],
        bullets: [
          'Build key references sheets for each Section C topic with 5-10 specific citations',
          'Create comparative tables for at least 3 moral/theological issues',
          'Write one timed Section C essay per week from past papers',
          'Practise 5 past Section B stimulus questions under exam conditions',
          'Maintain your Coursework Journal with reflective entries after each topic'
        ],
        commitmentText:
          'I will build my key references sheets for two Section C topics this week and write my first timed essay.'
      }
    ]
  },

  // ---------------------------------------------------------------------------
  // CLASSICAL STUDIES  (Higher Level)
  // ---------------------------------------------------------------------------
  'classical-studies': {
    subjectId: 'classical-studies',
    subjectName: 'Classical Studies',
    moduleNumber: '22',
    moduleTitle: 'Mastering Classical Studies',
    moduleSubtitle: 'Your Complete Classics Exam Guide',
    moduleDescription:
      'Decode the Classical Studies exam — understand the text-based questions, the essay structure, and how to show the depth of knowledge examiners reward.',
    themeName: 'fuchsia',
    finishButtonText: 'Carpe Diem',
    sections: [
      // Section 1 — Exam Structure
      {
        title: 'How Classical Studies Actually Works',
        eyebrow: '01 // Exam Structure',
        paragraphs: [
          'The Leaving Certificate Classical Studies Higher Level exam is a single paper covering both Greek and Roman civilisation. The exam is **2 hours and 30 minutes** long, and you will answer questions across two main sections. The paper tests your knowledge of [[set texts]], art, architecture, history, and culture from the ancient Greek and Roman worlds.',
          '[[Section A]] focuses on shorter, more structured questions based on the set texts and topics you have studied. These questions may ask you to identify passages, explain their context, discuss characters or themes, or analyse specific aspects of ancient culture. They test both recall and understanding, and the marks are awarded for precise, text-based answers.',
          '[[Section B]] consists of longer **essay-style questions** that require you to develop sustained arguments about aspects of Greek or Roman civilisation. These essays demand deeper analysis — you need to draw on multiple texts, compare different aspects of the ancient world, and demonstrate that you understand the significance of what you have studied.',
          'The split between Greek and Roman content means you need to be prepared across both civilisations. The exam typically offers choice within each area, so you can focus on the topics you know best, but you cannot avoid either civilisation entirely. **Balance your preparation** across both Greek and Roman material.'
        ],
        highlights: [
          { term: 'set texts', description: 'The prescribed literary works you study in detail — e.g., Homer\'s Odyssey, Virgil\'s Aeneid, Greek tragedies, Roman histories. Your answers must show detailed knowledge of these.' },
          { term: 'Section A', description: 'Shorter, structured questions on set texts and topics. Tests recall and understanding through passage identification, context, and analysis.' },
          { term: 'Section B', description: 'Longer essay questions requiring sustained argument. Draws on multiple texts and demands deeper analysis of Greek and Roman civilisation.' }
        ]
      },
      // Section 2 — Marking Criteria
      {
        title: 'What the Examiner Rewards',
        eyebrow: '02 // Marking Criteria',
        paragraphs: [
          'Classical Studies examiners reward one thing above all else: [[detailed textual knowledge]]. Vague generalisations about "the Greeks" or "Roman society" will not score well. The examiner wants to see that you have actually read the set texts closely and can reference specific episodes, characters, speeches, and themes. The more precise your references, the higher your marks.',
          'For essay questions in Section B, the examiner is looking for [[sustained argument]] rather than a list of facts. A strong essay will have a clear thesis, develop its argument through well-chosen examples from the set texts, and reach a reasoned conclusion. Simply narrating the plot of the Odyssey or listing facts about Roman architecture is not enough.',
          'The examiner also rewards [[comparative analysis]] — your ability to compare different texts, different cultures (Greek vs Roman), or different perspectives within a civilisation. For example, comparing how Homer and Virgil portray heroism, or how Athenian democracy differed from the Roman Republic, shows a level of understanding that goes beyond basic recall.',
          'In Section A, marks are awarded for **accuracy and relevance**. When identifying a passage, be precise about the speaker, the context, and what happens before and after. When explaining a term or concept, use the correct terminology and connect it to specific examples from your studies.'
        ],
        highlights: [
          { term: 'detailed textual knowledge', description: 'Specific references to episodes, characters, speeches, and themes from the set texts. Precision is what separates top answers from average ones.' },
          { term: 'sustained argument', description: 'A clear thesis developed through well-chosen textual examples, not just a list of facts or a plot summary.' },
          { term: 'comparative analysis', description: 'Comparing texts, cultures, or perspectives — e.g., Greek vs Roman, Homer vs Virgil — demonstrates higher-order understanding.' }
        ]
      },
      // Section 3 — High-Value Zones
      {
        title: 'Where Your Marks Are',
        eyebrow: '03 // High-Value Zones',
        paragraphs: [
          'The [[Section B essays]] carry the heaviest marks and are where the grade differentiation really happens. A student who writes two well-structured, evidence-rich essays in Section B is in a strong position for a top grade. The key is that these essays reward depth over breadth — it is better to analyse three episodes from the Odyssey in detail than to mention ten episodes superficially.',
          'Within Section A, the [[passage-based questions]] are often the most accessible for well-prepared students. If you know the set texts thoroughly, identifying a passage and explaining its context, significance, and connection to broader themes is relatively straightforward. These questions reward close reading, which is a skill you build through repeated engagement with the texts.',
          'Questions about [[art and architecture]] — whether Greek temple design, Roman engineering, or the visual arts — are a reliable scoring area if you prepare visual material alongside your texts. Being able to describe and analyse specific works (the Parthenon, the Colosseum, specific vase paintings or sculptures) with accurate terminology gives you an edge.',
          'The [[overlap between topics]] is another strategic opportunity. Many themes run across both Greek and Roman material — heroism, fate, the role of the gods, civic duty, the nature of power. If you study these themes across civilisations, you can answer a wider range of questions with confidence because your knowledge is connected rather than siloed.'
        ],
        highlights: [
          { term: 'Section B essays', description: 'The highest-value part of the exam. Well-structured, evidence-rich essays here are the key to a top grade.' },
          { term: 'passage-based questions', description: 'Section A questions that ask you to identify and analyse a passage. Very accessible if you know the set texts thoroughly.' },
          { term: 'art and architecture', description: 'Questions on specific works — temples, sculptures, engineering — are reliable marks with visual preparation.' },
          { term: 'overlap between topics', description: 'Themes like heroism, fate, and power run across Greek and Roman material. Studying thematically gives you flexible, connected knowledge.' }
        ]
      },
      // Section 4 — Common Pitfalls
      {
        title: 'What Costs You Marks',
        eyebrow: '04 // Common Pitfalls',
        paragraphs: [
          'The most damaging mistake in Classical Studies is [[plot retelling]] instead of analysis. When asked about the significance of Odysseus\'s encounter with the Cyclops, for example, do not simply retell what happened. The examiner wants you to analyse why this episode matters — what it reveals about heroism, cunning versus strength, the relationship between mortals and gods, or the Greek concept of xenia (hospitality).',
          'Another costly error is [[imbalanced preparation]] — studying Greek material thoroughly but neglecting Roman, or vice versa. The exam requires answers on both civilisations. Students who have only prepared one side find themselves with limited choice and may be forced to answer questions on topics they barely know.',
          'Students also lose marks through [[vague references]]. Saying "in the Odyssey, Odysseus faces many challenges" is not a useful reference. Saying "in Book 9, Odysseus blinds Polyphemus by driving a sharpened olive-wood stake into his eye while the Cyclops sleeps, demonstrating the cunning (metis) that defines his heroic identity" is. Specificity is everything in this subject.',
          'Finally, some students [[ignore the question focus]] and write everything they know about a topic rather than addressing what is actually being asked. If the question asks about the role of the gods in the Aeneid, an answer that spends most of its time discussing Aeneas\'s human relationships is off-target and will lose marks. Read the question carefully and answer what is asked.'
        ],
        highlights: [
          { term: 'plot retelling', description: 'Narrating events instead of analysing their significance. The examiner wants analysis of themes, characters, and concepts, not a story summary.' },
          { term: 'imbalanced preparation', description: 'Preparing only Greek or only Roman material. The exam requires both, and imbalance limits your choice on the day.' },
          { term: 'vague references', description: 'Generic mentions of texts without specific detail. "Odysseus faces challenges" scores far less than a precise, detailed reference.' },
          { term: 'ignore the question focus', description: 'Writing everything you know rather than addressing the specific question. Always answer what is being asked, not what you wish was asked.' }
        ]
      },
      // Section 5 — Study Techniques
      {
        title: 'How to Study Classical Studies',
        eyebrow: '05 // Study Techniques',
        paragraphs: [
          'The most effective study technique for Classical Studies is building [[text-specific revision notes]]. For each set text, create a document that lists the key episodes, key characters, key themes, and key quotations or passages. Organise this by book or section so you can quickly locate the material you need. This becomes your go-to reference for essay planning.',
          'Practise [[thematic essay planning]] across your texts. Choose a theme — heroism, fate, loyalty, justice, the role of women, the nature of power — and map out which episodes from which texts you would use to discuss that theme. This cross-text, cross-civilisation approach prepares you for the kinds of comparative questions that appear in Section B.',
          'For art and architecture, build a [[visual reference bank]]. Collect images of the key works you study — temples, sculptures, vase paintings, mosaics — and for each one, write a short analysis covering its date, context, key features, and significance. Being able to describe and analyse specific artworks from memory is a valuable exam skill.',
          'Use [[past papers]] extensively. Classical Studies questions follow recognisable patterns, and practising with past papers helps you understand what the examiner is looking for. Write at least one timed essay per week in the months before the exam, and compare your answers against the marking scheme to identify gaps in your knowledge.'
        ],
        highlights: [
          { term: 'text-specific revision notes', description: 'Organised notes for each set text listing key episodes, characters, themes, and quotations. Your essential reference for essay planning.' },
          { term: 'thematic essay planning', description: 'Mapping themes across multiple texts and civilisations. Prepares you for comparative questions and builds flexible, connected knowledge.' },
          { term: 'visual reference bank', description: 'Images and short analyses of key artworks, buildings, and sculptures. Builds the specific detail needed for art and architecture questions.' }
        ]
      },
      // Section 6 — Action Plan
      {
        title: 'Your Classical Studies Action Plan',
        eyebrow: '06 // Action Plan',
        paragraphs: [
          'Start by creating [[text-specific revision notes]] for every set text on your course. List the key episodes, characters, themes, and quotable passages for each. This is the foundation of all your exam preparation — everything else builds on knowing your texts in detail.',
          'Next, identify the **five major themes** that run across your course material and create thematic essay plans for each. Map which texts and episodes you would use for each theme, covering both Greek and Roman material. Then build your visual reference bank for art and architecture topics.',
          'In the final month, shift to intensive past paper practice. Write one full timed essay from a past paper every two days. Mark your work, check for specificity of references, and identify any topics where your knowledge is thin. Fill those gaps with targeted revision.'
        ],
        highlights: [
          { term: 'text-specific revision notes', description: 'Your primary study tool: detailed notes on episodes, characters, themes, and passages for every set text.' }
        ],
        bullets: [
          'Create detailed revision notes for every set text — episodes, characters, themes, quotations',
          'Identify 5 major themes and create cross-text essay plans for each',
          'Build a visual reference bank for all art and architecture topics',
          'Balance your preparation across both Greek and Roman material',
          'Write one timed essay every two days in the final month from past papers'
        ],
        commitmentText:
          'I will complete my text-specific revision notes for two set texts this week and draft my first thematic essay plan.'
      }
    ]
  }
};
