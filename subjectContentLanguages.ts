/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type SubjectModuleContent } from './subjectModuleData';

export const LANGUAGES_CONTENT: Record<string, SubjectModuleContent> = {
  // ---------------------------------------------------------------------------
  // ENGLISH
  // ---------------------------------------------------------------------------
  english: {
    subjectId: 'english',
    subjectName: 'English',
    moduleNumber: '01',
    moduleTitle: 'Mastering English',
    moduleSubtitle: 'Break the code on the Leaving Cert\'s most popular subject',
    moduleDescription: 'A strategic deep-dive into Paper 1, Paper 2, and the PCLM marking system — so you know exactly where your marks come from and how to maximise every one of them.',
    themeName: 'blue',
    finishButtonText: 'Write Your Best',
    sections: [
      // Section 1 — Exam Structure
      {
        title: 'How English Actually Works',
        eyebrow: '01 // Exam Structure',
        paragraphs: [
          'Leaving Cert English is assessed entirely through two written papers worth a combined **400 marks**. There is no oral, no coursework, no project — just you and two exam booklets across two days. That simplicity is actually a gift: every mark is within your control on the day.',
          'Paper 1 is your [[Composing and Comprehension]] paper. It runs for **2 hours 50 minutes** and is worth **200 marks**. You face two sections: Section I — Comprehending (**100 marks**), which presents three texts on a shared theme — you answer a **Question A (50 marks, comprehension) on one text and a Question B (50 marks, a functional writing task) on a different text** (you may not answer both on the same text) — and Section II is the Composition where you choose one essay from a list of prompts (100 marks). The composition prompts relate to the same theme as the texts.',
          '[[Paper 2]] is the literature paper, also **200 marks** and **3 hours 20 minutes** long. It has three sections: the [[Single Text]] (one of your studied plays, novels, or films — 60 marks), the [[Comparative Study]] (comparing three texts across a mode such as Theme, Cultural Context, or Literary Genre — 70 marks), and [[Poetry]] (**70 marks** total, in two parts: an **Unseen Poem** you have never seen before — 20 marks — and **Prescribed Poetry**, an essay on one of your studied poets — 50 marks).',
          'The total weighting is perfectly balanced: 50% for personal writing and comprehension skills (Paper 1), and 50% for literature response (Paper 2). Understanding this split is your first strategic advantage — neglect either paper and you cap your grade.'
        ],
        highlights: [
          { term: 'Composing and Comprehension', description: 'Paper 1 tests your ability to read complex texts critically AND produce high-quality original writing. These are complementary skills — strong readers tend to be stronger writers.' },
          { term: 'Paper 2', description: 'The literature paper. You must demonstrate deep understanding of your studied texts and the ability to respond to unseen poetry under time pressure.' },
          { term: 'Single Text', description: 'One text studied in depth — a play (e.g. Hamlet, Philadelphia Here I Come!), a novel, or a film. You answer one question from a choice of options. Worth 60 marks.' },
          { term: 'Comparative Study', description: 'You compare three texts across one mode of comparison. In the exam, you typically answer one question using all three texts. Worth 70 marks and often the highest-scoring section when done well.' },
          { term: 'Poetry', description: 'Paper 2, Section III (70 marks), in two parts. A — Unseen Poem (20 marks): you answer a guided question on a poem you have never seen. B — Prescribed Poetry (50 marks): an essay on one of the studied poets from the prescribed list. Prepare both — the 50-mark prescribed essay is the larger prize.' }
        ],
      },
      // Section 2 — Marking Criteria
      {
        title: 'What the Examiner Rewards',
        eyebrow: '02 // Marking Criteria',
        paragraphs: [
          'Every answer you write in Leaving Cert English is assessed using the [[PCLM]] framework. This stands for **Purpose**, **Coherence of Delivery**, **Language**, and **Mechanics**. Understanding PCLM is not optional — it is literally the lens through which every examiner reads your work. The published split is **Purpose 30%, Coherence 30%, Language 30%, Mechanics 10%** — so the first three criteria dominate, and Purpose has primacy (the marks for Coherence or Language can never exceed the marks awarded for Purpose). Together they define the difference between an H5 and an H1.',
          '**Purpose** means you actually answer the question asked. Sounds obvious, but the most common reason students lose marks is writing a beautiful answer to a question that was not asked. The examiner checks: did the student understand the task? Did they sustain their focus throughout? In a composition, this means your essay must match the genre (if the prompt asks for a speech, it must sound like a speech). In Paper 2, it means directly engaging with the specific question, not dumping everything you know about a text.',
          '**Coherence of Delivery** is about [[structure and flow]]. Does your answer have a clear arc? Do your paragraphs connect logically? Is there a sense of development from start to finish? Top-scoring students plan before they write, and their answers feel like they are going somewhere, not just listing points.',
          'The **Language** criterion rewards a rich, varied, and precise vocabulary used in an authentic voice. The examiner is looking for writing that sounds like it belongs to you — not regurgitated teacher-notes or formulaic phrases. **Mechanics** covers spelling, grammar, and punctuation. It carries only 10% of each answer, so it will not sink a strong response on its own — but consistent errors still cost the marks that are there, and it is the easiest 10% to protect. Proofread. Every. Time.'
        ],
        highlights: [
          { term: 'PCLM', description: 'Purpose, Coherence of Delivery, Language, Mechanics. This is the assessment grid used across all Leaving Cert English answers. The weighting is Purpose 30%, Coherence 30%, Language 30%, Mechanics 10% — and Purpose has primacy (Coherence and Language marks can never exceed the Purpose mark). Master all four and you are looking at top marks.' },
          { term: 'structure and flow', description: 'Examiners reward answers that feel deliberately constructed — a clear opening, developed middle paragraphs that build on each other, and a conclusion that closes the loop. Plan before writing.' }
        ],
      },
      // Section 3 — High-Value Zones
      {
        title: 'Where Your Marks Are',
        eyebrow: '03 // High-Value Zones',
        paragraphs: [
          'The single biggest mark allocation in English is the [[Paper 1 Composition]] at **100 marks** — that is 25% of your entire grade in one answer. Nothing else in the exam comes close. If you write one exceptional essay, you have secured a quarter of your total. This is where strong students separate themselves: they practise compositions across multiple genres (personal essay, short story, speech, article, debate) and go into the exam with a flexible toolkit of ideas, not a pre-learned script.',
          'On Paper 2, the [[Comparative Study]] (70 marks) and the [[Poetry]] section (70 marks) together make up 35% of your total. Here is the strategic insight many students miss: the Comparative is highly formulaic. Once you learn the structure — linking your three texts through the mode of comparison, using clear comparative language ("Similarly", "In contrast", "While Text 1...") — you can consistently score well. It rewards preparation and technique more than inspiration.',
          'Within the Poetry section, the **Prescribed Poetry essay is the bigger prize at 50 marks** — it is an essay on one of the studied poets from the prescribed list, so it rewards deep preparation of your poets (key poems, themes, techniques, and a personal response). The **Unseen Poem (20 marks)** is where the playing field is level: you cannot study the specific poem, so a student who has practised responding to unseen poems will do well. Prepare both — do not neglect the 50-mark prescribed essay in favour of unseen practice.',
          'The Comprehending section on Paper 1 delivers **100 marks** across two of the three texts — a **Question A (comprehension, 50 marks) on one text and a Question B (a functional writing task, 50 marks) on a different text**. Many students treat this as warm-up, but it is worth the same as the composition, and Question B is a distinct skill: you produce a short functional piece (such as a speech, letter, article, diary entry, or proposal) in the required register. Read each text twice, underline key phrases, and — for Question B — match the genre and register exactly.'
        ],
        highlights: [
          { term: 'Paper 1 Composition', description: 'Worth 100 marks — the single richest question in the entire exam. Genre flexibility is key: practise personal essays, short stories, speeches, articles, and discursive pieces so you can adapt to whatever prompt suits you on the day.' },
          { term: 'Comparative Study', description: 'Worth 70 marks on Paper 2. Highly structured and very learnable. Students who master the comparative framework (linking all three texts in every paragraph) consistently score well.' },
          { term: 'Poetry', description: 'Worth 70 marks total on Paper 2: Prescribed Poetry (50 marks, an essay on a studied poet) plus the Unseen Poem (20 marks). Prepare your prescribed poets deeply for the larger 50-mark essay, and practise unseen poems weekly to build a real-time analytical reflex for the 20-mark part.' }
        ],
      },
      // Section 4 — Common Pitfalls
      {
        title: 'What Costs You Marks',
        eyebrow: '04 // Common Pitfalls',
        paragraphs: [
          'The number one mark-killer in English is [[not answering the question]]. This shows up everywhere: compositions that drift off-topic, Single Text answers that retell the plot instead of addressing the question, and Comparative answers that discuss each text separately instead of comparing. Every year, the Chief Examiner\'s Report says the same thing: the best students engage directly with the question throughout their answer. Write the question at the top of your page and refer back to it every two paragraphs.',
          'The second biggest killer is **running out of time**. Paper 2 is 3 hours and 20 minutes for three sections. If you spend 80 minutes on the Single Text, you are stealing time from the Comparative and the Poetry section — both of which are worth more marks. Stick to a strict time plan: roughly 55 minutes for the Single Text (60 marks), 70 minutes for the Comparative (70 marks), and 70 minutes for Poetry (70 marks) — split within Poetry so the 50-mark Prescribed essay gets the lion\'s share and the 20-mark Unseen Poem takes about 20 minutes.',
          'On Paper 1, students routinely [[under-develop their composition]]. A five-paragraph essay will not score in the top bracket. Examiners want to see sustained, developed writing — think seven to nine substantial paragraphs for a personal essay. Short compositions signal that you either ran out of ideas or ran out of time, and neither is forgiven.',
          'Finally, many students write in a generic, impersonal voice that sounds like it could belong to anyone. The PCLM criteria explicitly reward **authentic language** — writing that sounds like a real person with real thoughts. Ditch the clichés. Stop starting paragraphs with "Furthermore" and "Moreover". Write in your own voice and the examiner will notice.'
        ],
        highlights: [
          { term: 'not answering the question', description: 'The most common reason for mid-range marks across all of English. Always re-read the question before starting each paragraph. If your paragraph does not directly address the question, cut it or rewrite it.' },
          { term: 'under-develop their composition', description: 'Top-scoring compositions are sustained pieces of writing — 1,000+ words, rich in detail and developed thought. Thin, short essays cannot access the highest mark bands even if the writing quality is strong.' }
        ],
      },
      // Section 5 — Study Techniques
      {
        title: 'How to Study English',
        eyebrow: '05 // Study Techniques',
        paragraphs: [
          'English is a [[skills-based subject]]. You do not study it the way you study History or Biology — there is no textbook to memorise. Instead, you build skills through practice. The core activities are: reading widely, writing regularly, and engaging critically with texts. If your English study involves highlighting notes and re-reading them, you are doing it wrong.',
          'For Paper 1, the best strategy is **timed composition practice**. Once a week, pick a past paper prompt and write a full composition under timed conditions (about 65 minutes). Then, assess your own work against the PCLM criteria. Better yet, swap with a classmate and assess each other\'s work. The point is not to produce a perfect essay — it is to build fluency, speed, and the ability to generate ideas under pressure.',
          'For Paper 2, create a [[one-page summary]] for each of your studied texts: key themes, important quotes (aim for five to eight per text), and character arcs. For the Comparative, build a comparison grid — a table with your three texts across the top and key aspects of the mode down the side. Fill in each cell with a specific reference. This grid is your revision gold: it forces you to think comparatively before you walk into the exam.',
          'For the Poetry section, split your preparation. For **Prescribed Poetry (50 marks)**, know your studied poets in depth — for each poet, build a one-page sheet with three or four key poems, their main themes, standout techniques, and your personal response, plus a small bank of short quotes. For the **Unseen Poem (20 marks)**, practise the TPCASLT method (**Title, Paraphrase, Connotation, Attitude, Shifts, Literary devices, Theme**) on one past-paper poem per week. Within six weeks you will approach any unseen poem with a clear analytical framework. Past papers are your best resource — the SEC website has decades of them for free.'
        ],
        highlights: [
          { term: 'skills-based subject', description: 'English rewards the ability to read critically and write effectively. You cannot cram English the night before. Skills develop over weeks and months of deliberate practice — reading, writing, and rewriting.' },
          { term: 'one-page summary', description: 'Condensing an entire text onto a single page forces you to identify the most important themes, quotes, and ideas. This is active recall at its best — far more effective than re-reading your notes.' }
        ],
      },
      // Section 6 — Action Plan
      {
        title: 'Your English Action Plan',
        eyebrow: '06 // Action Plan',
        paragraphs: [
          'Here is your concrete plan. This week, choose **one past Paper 1 composition prompt** and write a full essay under timed conditions. Set a timer for 65 minutes, choose your genre, plan for five minutes, then write without stopping. When you finish, read it back and score yourself honestly against [[PCLM]]. Where did you lose focus? Where did your language get lazy? That self-assessment is where the learning happens.',
          'Next, build your Paper 2 Comparative grid. Take a blank page, write your three comparative texts across the top, and list the key aspects of your studied mode down the left side. Fill in every cell with at least one specific reference — a scene, a quote, a technique. If any cell is empty, that is exactly where the examiner could catch you out. Fill the gaps now, not in June.',
          'Finally, work both halves of the Poetry section. This week, build a one-page sheet for one of your prescribed poets (three or four key poems, their themes, techniques, and your response) for the 50-mark essay — and separately, find one unseen poem from a past paper (any year, any level) and spend 20 minutes responding to it: what it is about, what struck you, and what techniques the poet uses. Do the unseen practice once a week. By exam day you will have prepared your poets properly and practised with 20+ unseen poems, so both parts feel routine instead of terrifying.'
        ],
        highlights: [
          { term: 'PCLM', description: 'Use the PCLM framework to self-assess: Did I fulfil the Purpose? Was my Coherence of Delivery strong? Was my Language rich and authentic? Were my Mechanics clean?' }
        ],
        commitmentText: 'This week, I will write one full timed composition (65 minutes) from a past Paper 1 prompt and self-assess it against the PCLM criteria.',
      },
    ],
  },

  // ---------------------------------------------------------------------------
  // IRISH
  // ---------------------------------------------------------------------------
  irish: {
    subjectId: 'irish',
    subjectName: 'Irish',
    moduleNumber: '02',
    moduleTitle: 'Mastering Irish',
    moduleSubtitle: 'Turn the oral into your secret weapon and unlock marks across every component',
    moduleDescription: 'The Leaving Cert Irish exam is unique — the oral alone is worth 40% of your entire grade. This module shows you exactly how to exploit that structure and pick up marks that most students leave behind.',
    themeName: 'emerald',
    finishButtonText: 'Bain Triail As!',
    sections: [
      // Section 1 — Exam Structure
      {
        title: 'How Irish Actually Works',
        eyebrow: '01 // Exam Structure',
        paragraphs: [
          'Leaving Cert Irish is assessed across the oral (An Bhéaltriail Chomónta) and two written papers, worth a combined **600 marks** at both Higher and Ordinary Level. The breakdown is: the [[Scrúdú Béil (Oral Exam)]] worth **240 marks** (40%), Paper 1 worth **160 marks** (approximately 27%), and Paper 2 worth **200 marks** (approximately 33%). Paper 1 contains the [[Scrúdú Cluastuisceana (Aural Exam)]], An Chluastuiscint, worth **60 marks** (10% of your grade), alongside the composition. The oral is a common paper at both levels — 240 marks out of 600, 40% — which makes it the single largest component in the whole exam.',
          'The oral exam takes place in the spring, usually in March or April, before you sit your written papers. It is a conversation with an external examiner. You cover your prepared topic (Sraith Pictiúr — picture sequences), general conversation about your life, school, hobbies, and current affairs, and some poetry or prose reading. This is a conversation, not an interrogation — the examiner wants you to talk confidently.',
          '[[Paper 1 (Páipéar 1)]] combines the **Cluastuiscint** (aural, 60 marks) and the **Ceapadóireacht** (composition, 100 marks). For the Ceapadóireacht you produce one substantial piece — an essay (aiste), a story (scéal), a debate/speech (díospóireacht/óráid), or a discussion (alt) — from a choice of formats. Paper 2 (Páipéar 2) is your literature and comprehension paper: **Ceist 1 — Léamhthuiscint** (two reading comprehensions, 100 marks) and **An Litríocht** (100 marks), covering [[Prós Ainmnithe]] (prose), [[Filíocht]] (poetry), and Litríocht Bhreise.',
          'The aural exam (An Chluastuiscint) is a listening test that forms part of Paper 1, worth **60 marks**. You hear recorded passages — news reports (píosaí nuachta), conversations (comhráite), and announcements (fógraí) — and answer questions on them. It tests your ability to understand spoken Irish at natural speed.'
        ],
        highlights: [
          { term: 'Scrúdú Béil (Oral Exam)', description: 'Worth a massive 240 marks at Higher Level — 40% of your total grade. This is the single largest component of any Leaving Cert language exam. Preparing thoroughly for the oral is the highest-value activity in all of Leaving Cert Irish.' },
          { term: 'Scrúdú Cluastuisceana (Aural Exam)', description: 'The listening exam (An Chluastuiscint), worth 60 marks and forming part of Paper 1 — 10% of your overall grade. You listen to recordings in Irish and answer questions. Practise with past paper recordings — TG4 and Raidió na Gaeltachta are also brilliant free practice resources.' },
          { term: 'Paper 1 (Páipéar 1)', description: 'Worth 160 marks: the Cluastuiscint (aural, 60 marks) plus the Ceapadóireacht (composition, 100 marks). For the composition you write one substantial piece — essay, story, debate/speech, or discussion — from a choice of formats.' },
          { term: 'Prós Ainmnithe', description: 'Your studied prose texts — short stories from the prescribed list. You must answer detailed questions showing genuine understanding of characters, themes, and language.' },
          { term: 'Filíocht', description: 'Your studied poems. You need to know the themes, imagery, and language of each poem well enough to answer unpredictable questions about them.' }
        ],
      },
      // Section 2 — Marking Criteria
      {
        title: 'What the Examiner Rewards',
        eyebrow: '02 // Marking Criteria',
        paragraphs: [
          'In the oral exam, the examiner assesses your [[cumarsáid (communication)]]. Can you sustain a conversation? Do you respond naturally to questions? Do you speak with reasonable fluency, even if your Irish is not perfect? The oral marking scheme rewards students who communicate effectively and confidently. You do not need to speak like a native Gaeltacht speaker — you need to speak like someone who genuinely uses the language and can hold a real conversation.',
          'For the Sraith Pictiúr specifically, the examiner wants you to narrate the picture sequence coherently, using appropriate vocabulary and past tenses. Learn the key phrases and vocabulary for each of the 20 picture sequences, but — crucially — practise telling the story fluently rather than reciting memorised blocks. Examiners can tell the difference instantly.',
          'In the written papers, the marking scheme follows a [[quality of Irish]] scale. The top band requires "saibhreas teanga" — richness of language. This means varied vocabulary, correct grammar (especially tuiseal ginideach, briathra neamhrialta, and modh coinníollach), and an ability to express complex ideas. Mid-range answers tend to rely on simple sentence structures and basic vocabulary. The jump from a B to an A in the composition is almost always about language quality, not content.',
          'For Paper 2 literature answers, the examiner rewards genuine personal engagement with the text. Quoting directly from the poem or story (even short phrases) shows that you know the text. Answers that summarise the plot without any quotes or personal response will score in the lower bands regardless of accuracy.'
        ],
        highlights: [
          { term: 'cumarsáid (communication)', description: 'The oral exam is fundamentally about communication. Can you express yourself? Can you understand what the examiner asks? Can you keep the conversation going? Fluency and confidence matter more than perfection.' },
          { term: 'quality of Irish', description: 'Written answers are graded on language richness. Simple, repetitive Irish stays in the mid-range. Using varied sentence structures, idioms (seanfhocail), and correct advanced grammar pushes you into the top bands.' }
        ],
      },
      // Section 3 — High-Value Zones
      {
        title: 'Where Your Marks Are',
        eyebrow: '03 // High-Value Zones',
        paragraphs: [
          'The oral at **240 marks** is the most valuable single component in any Leaving Cert subject. Let that sink in: [[40% of your entire Irish grade]] is decided in one conversation months before the written exam. No other subject gives you this opportunity. If you walk into the oral well-prepared, you can effectively bank a strong grade before you even open Paper 1.',
          'Within the oral, the **Sraith Pictiúr** section is the most controllable. There are 20 sequences and you will be given one at random. Each sequence requires about 90 seconds of narration. If you prepare all 20 thoroughly (key vocabulary, past tenses, linking phrases), you guarantee yourself strong marks on the one section where you know exactly what might come up.',
          'On Paper 1, the **Ceapadóireacht (composition)** is the highest-value written section — worth **100 marks** at Higher Level. You choose one piece from a range of formats (essay, story, debate/speech, or discussion), so you can play to your strengths. Preparing a small set of formats thoroughly, with flexible vocabulary and phrasing you can adapt to the title on the day, is a reliable strategy.',
          'On Paper 2, the [[studied poetry (Filíocht)]] section rewards preparation disproportionately. If you know your poems well — key quotes, themes, and the feelings they evoke — you can score very highly. Students who treat poetry as a memorisation task often miss the point. Instead, understand three or four key moments in each poem and be able to discuss them in your own Irish.'
        ],
        highlights: [
          { term: '40% of your entire Irish grade', description: 'The oral is worth 240 out of 600 marks at Higher Level. No other Leaving Cert subject concentrates so many marks into a single, highly preparable component. This is where strategic students gain the biggest advantage.' },
          { term: 'studied poetry (Filíocht)', description: 'Studied poetry on Paper 2 is one of the most predictable sections. If you know your five or six poems deeply — a few key quotes each, the main themes, and a personal response — you can write a strong answer regardless of the specific question.' }
        ],
      },
      // Section 4 — Common Pitfalls
      {
        title: 'What Costs You Marks',
        eyebrow: '04 // Common Pitfalls',
        paragraphs: [
          'The single biggest mistake in Leaving Cert Irish is [[under-preparing the oral]]. Students spend months studying grammar and literature but only two weeks preparing for a component worth 40% of their grade. The oral happens in spring, and by then it is too late to build fluency from scratch. Start speaking Irish regularly — even 10 minutes a day — months before the exam. Talk to your teacher, record yourself, or use the Sraith Pictiúr as daily speaking practice.',
          'In the written papers, **grammar errors** cost marks across every answer. The most common mistakes are: incorrect use of the genitive case (tuiseal ginideach), wrong verb forms in the past and conditional tenses, and séimhiú/urú errors after prepositions and particles. The fix is not glamorous — it is targeted grammar practice, five minutes a day, using drills or past paper correction exercises.',
          'On Paper 2, students often [[write in English-structured Irish]] — translating English thoughts word by word into Irish. This produces clunky, unnatural sentences that examiners immediately recognise. Instead, learn phrases and sentence patterns as complete units. Think in chunks of Irish, not in translated English sentences. Reading Irish language content (even short articles on Tuairisc.ie or listening to Raidió na Gaeltachta) helps your brain absorb natural Irish structures.',
          'Another common pitfall is not using quotes in literature answers. If you answer a question on a poem and never quote a line, you are telling the examiner you do not really know the text. Even short phrase-quotes ("mar a deir an file...") show direct engagement and push your answer into higher mark bands.'
        ],
        highlights: [
          { term: 'under-preparing the oral', description: 'The oral is worth 240 marks and yet many students prepare for it as an afterthought. Start early: daily speaking practice, recorded Sraith Pictiúr narrations, and conversation practice with a partner are all high-impact strategies.' },
          { term: 'write in English-structured Irish', description: 'Translating from English produces unnatural Irish. Instead, learn useful phrases as complete units and practise thinking directly in Irish. Exposure to real Irish (podcasts, TG4, Tuairisc.ie) rewires your instinct away from English structures.' }
        ],
      },
      // Section 5 — Study Techniques
      {
        title: 'How to Study Irish',
        eyebrow: '05 // Study Techniques',
        paragraphs: [
          'Irish is a [[living language]], and the exam rewards you for treating it like one. The most effective study strategy is **daily active use** — speaking, listening, reading, and writing in Irish, even in small doses. Ten minutes of speaking practice every day is worth more than three hours of passive note-reading at the weekend.',
          'For the oral, record yourself narrating each of the 20 [[Sraith Pictiúr]] sequences. Listen back, note where you hesitate or make errors, and re-record. By the time you have done each sequence three or four times, the vocabulary and sentence structures will feel natural. Also prepare answers to common conversation topics: your family, school, hobbies, current events, and your plans for the future. Have eight to ten ready-to-go topics with key vocabulary.',
          'For the written papers, build a [[frásaí úsáideacha (useful phrases)]] bank. Organise it by topic: essay openings, opinion expressions, linking phrases, conclusion phrases, and literary response language. For example: "Is léir dom go..." (It is clear to me that...), "Tá bá agam le..." (I have sympathy for...), "Ba mhaith liom a rá go..." (I would like to say that...). Having 30 to 40 versatile phrases at your fingertips transforms your written Irish instantly.',
          'For literature, create flashcards with key quotes from your studied poems and stories. On one side, write the quote; on the other, write the theme it relates to and why it matters. Test yourself using active recall — cover the answer and try to explain the significance of each quote. Five minutes of this daily is more valuable than an hour of re-reading your literature notes.'
        ],
        highlights: [
          { term: 'living language', description: 'Irish is assessed as a living, communicative language — especially in the oral. The more you use it actively (speaking, writing, thinking), the better you will perform. Passive study alone will not build fluency.' },
          { term: 'Sraith Pictiúr', description: 'The 20 picture sequences for the oral exam. Each one tells a short story through images. You must narrate the story in Irish. Recording yourself and replaying is the most efficient way to prepare.' },
          { term: 'frásaí úsáideacha (useful phrases)', description: 'A personal bank of versatile Irish phrases that you can deploy in essays, literature answers, and even the oral. These are the building blocks of strong written and spoken Irish.' }
        ],
      },
      // Section 6 — Action Plan
      {
        title: 'Your Irish Action Plan',
        eyebrow: '06 // Action Plan',
        paragraphs: [
          'This week, pick **three Sraith Pictiúr** sequences and narrate each one aloud. Record yourself on your phone. Listen back and identify where you hesitate, where you switch to English in your head, and where your grammar breaks down. Then re-record until the narration flows. This single exercise builds oral fluency, vocabulary, and confidence simultaneously — and it only takes 15 minutes per sequence.',
          'Next, start your [[frásaí úsáideacha]] bank. Open a fresh page (or a notes app) and write down 10 useful phrases you can use in any essay. Include at least two opinion phrases, two linking phrases, and two conclusion phrases. Add to this bank every week. By exam time, you will have 40+ phrases that make your written Irish sound immediately more sophisticated.',
          'Finally, pick one studied poem and write a **paragraph response in Irish** about it — what it is about, what you like about it, and one quote that stands out. Time yourself: you have 12 minutes. This mirrors what you will do on Paper 2. One poem per week means you will have covered all your studied poems multiple times before the exam.'
        ],
        highlights: [
          { term: 'frásaí úsáideacha', description: 'Your personal phrase bank. Start with 10 versatile phrases this week. Add to it weekly. These phrases become the scaffolding that holds up every essay and literature answer you write.' }
        ],
        commitmentText: 'This week, I will record myself narrating three Sraith Pictiúr sequences aloud and build a starter bank of 10 useful Irish phrases for essay writing.',
      },
    ],
  },

  // ---------------------------------------------------------------------------
  // FRENCH
  // ---------------------------------------------------------------------------
  french: {
    subjectId: 'french',
    subjectName: 'French',
    moduleNumber: '03',
    moduleTitle: 'Mastering French',
    moduleSubtitle: 'Oral, aural, reading, writing — know exactly where to focus for maximum marks',
    moduleDescription: 'The Leaving Cert French exam tests four skills across three assessment components. This module breaks down the mark allocation, what examiners actually reward, and how to turn each component into a strength.',
    themeName: 'rose',
    finishButtonText: 'Allez-y!',
    sections: [
      // Section 1 — Exam Structure
      {
        title: 'How French Actually Works',
        eyebrow: '01 // Exam Structure',
        paragraphs: [
          'Leaving Cert French at Higher Level is assessed across **three components** with a total of **400 marks**. The breakdown is: the [[Oral Exam]] worth **100 marks** (25%), the [[Aural Exam (Listening)]] worth **80 marks** (20%), and the [[Written Exam]] worth **220 marks** (55%). This means the oral and aural together account for **45%** of your total — nearly half your grade is decided before you sit down to the reading and writing.',
          'The oral exam takes place in the spring (March/April). It is a **12 to 15-minute conversation** with an external examiner conducted entirely in French. You will discuss your prepared topic, general conversation about your life and interests, and role-play or discussion scenarios. The examiner assesses your ability to communicate, not your ability to be perfect.',
          'The aural exam is a **listening comprehension test lasting approximately 40 minutes**. You hear recorded passages — conversations, news items, announcements — and answer questions based on what you hear. Each section is played twice. The aural is sat during the written exam session. Questions are answered in French or English depending on the section.',
          'The written exam is a **2 hour 30 minute paper** worth 220 marks, divided into two main sections: [[Reading Comprehension]] (Compréhension écrite, **120 marks**) and [[Written Expression]] (Production écrite, **100 marks**). Reading Comprehension involves two passages in French with questions testing your understanding. Written Expression requires you to produce original French writing — one longer opinion piece plus shorter functional and response tasks (letter, note, message, diary entry, and similar).'
        ],
        highlights: [
          { term: 'Oral Exam', description: 'Worth 100 marks (25%). A 12-15 minute face-to-face conversation in French. You can prepare extensively for this — your topic, common questions, and key vocabulary are all within your control.' },
          { term: 'Aural Exam (Listening)', description: 'Worth 80 marks (20%). A listening test with recordings played twice, sat during the written exam session. Practising with past paper audio recordings is the single best preparation strategy.' },
          { term: 'Written Exam', description: 'Worth 220 marks (55%). Combines reading comprehension (120 marks) and written production (100 marks) across 2 hours 30 minutes.' },
          { term: 'Reading Comprehension', description: 'Compréhension écrite, 120 marks — the biggest single component of the written paper. You read French passages and answer questions. Accuracy, detail, and evidence of understanding the original text are key.' },
          { term: 'Written Expression', description: 'Production écrite, 100 marks. You produce original French writing — an opinion piece plus shorter functional tasks. Quality of language, accuracy, and relevance to the prompt are all assessed.' }
        ],
      },
      // Section 2 — Marking Criteria
      {
        title: 'What the Examiner Rewards',
        eyebrow: '02 // Marking Criteria',
        paragraphs: [
          'In the oral, the examiner rewards [[communicative competence]] above all. Can you sustain a conversation? Can you respond to unexpected questions? Can you express and justify opinions? Students who prepare 10 to 12 topics thoroughly and practise responding to follow-up questions consistently outperform students who memorise essays and recite them. The examiner notices immediately when you are reciting versus conversing.',
          'In the aural, marks are awarded for accurate identification of information from the recordings. The key skill is **recognising spoken French at natural speed** — including liaisons, contractions, and colloquial expressions. The marking is precise: you either caught the information or you did not. There are no marks for creative interpretation. Listen for numbers, names, times, reasons, and opinions — these are the most commonly tested details.',
          'For the written paper, the [[reading comprehension]] marking rewards accurate and complete answers. Partial answers receive partial marks, so always attempt every part of every question. The examiner checks whether you have understood the passage — not whether your French grammar is perfect in your answers. However, answers must be clear enough to demonstrate understanding.',
          'In the [[Written Expression]] section, marking is based on **content relevance**, **quality of language**, and **grammatical accuracy**. The top bands require varied vocabulary, complex sentence structures (using subjunctive, conditional, relative clauses), and a genuine attempt to engage with the prompt. Formulaic, repetitive language stays in the middle bands. Accuracy matters — consistent tense errors, gender agreement mistakes, and accent omissions all reduce your mark.'
        ],
        highlights: [
          { term: 'communicative competence', description: 'The oral exam is about your ability to communicate in real French. Fluency, spontaneity, and the ability to discuss topics naturally are rewarded more than perfect grammar delivered in a robotic tone.' },
          { term: 'reading comprehension', description: 'Marks are awarded for demonstrating that you understood the passage. Answer in full sentences where required, and always quote or paraphrase from the text to support your answer.' },
          { term: 'Written Expression', description: 'Top marks require relevant content, rich vocabulary, varied sentence structures, and grammatical accuracy. The jump from B to A is almost always about language quality.' }
        ],
      },
      // Section 3 — High-Value Zones
      {
        title: 'Where Your Marks Are',
        eyebrow: '03 // High-Value Zones',
        paragraphs: [
          'The [[oral exam at 100 marks]] (25%) is the most efficient place to gain marks in French. Unlike the written paper, the oral is entirely preparable. You know the format, you can predict most of the questions, and you can rehearse your answers until they flow naturally. Students who invest serious time in oral preparation routinely outscore their written performance — it is common to see students who get a B in the written paper but an A in the oral.',
          'Within the oral, your **prepared topic** (le sujet préparé) is your home ground. You choose the topic, prepare the vocabulary, and can steer the conversation toward your strengths. Choose a topic that genuinely interests you and that allows you to express opinions, tell anecdotes, and use varied vocabulary. Avoid overly narrow topics that dry up after two minutes.',
          'On the written paper, the [[Written Expression section]] is where the biggest mark swing occurs. A well-written letter or essay can score 80+ out of 100, while a weak one might score 40. The difference is preparation: students who have practised writing in multiple formats (formal letter, informal letter, article, essay, blog post) and have a bank of versatile phrases can adapt to any prompt. Students who rely on memorised essays often find the prompt does not quite fit, and their answer sounds forced.',
          'The aural exam is often under-prepared, yet at **80 marks (20%)** it is worth almost as much as the oral and more than a fifth of your grade. The good news is that aural skills improve rapidly with practice. Listening to French audio for 15 minutes daily (podcasts, past paper recordings, French radio) over two to three months will dramatically improve your score. The improvement curve for listening is steeper than for any other skill.'
        ],
        highlights: [
          { term: 'oral exam at 100 marks', description: 'The oral is the most preparable, most predictable component of French. Investing heavily here gives you a guaranteed return. Many students bank 80+ marks in the oral, giving them a cushion for the written paper.' },
          { term: 'Written Expression section', description: 'This is where the biggest variation in marks occurs. A strong written piece can compensate for a weaker reading comprehension. Build a bank of versatile phrases and practise writing in multiple formats.' }
        ],
      },
      // Section 4 — Common Pitfalls
      {
        title: 'What Costs You Marks',
        eyebrow: '04 // Common Pitfalls',
        paragraphs: [
          'The most common pitfall in French is [[neglecting the oral and aural]] because they feel less "academic" than the written paper. Together they are worth 45% of your grade. Students who spend 90% of their study time on grammar and reading comprehension are optimising for barely half the exam. Balance your preparation across all three components.',
          'In the oral, the biggest mark-killer is **freezing or giving one-word answers**. The examiner cannot give you marks for silence. If you do not understand a question, ask the examiner to repeat it ("Pourriez-vous répéter, s\'il vous plaît?"). If you do not know a word, talk around it. The examiner rewards effort and communication, even when it is imperfect.',
          'In the written paper, students routinely lose marks through [[basic grammatical errors]] that are entirely avoidable: incorrect verb endings, wrong gender for common nouns, missing accents (è, é, ê, ç), and incorrect preposition use. These errors accumulate and pull your mark down across every answer. A focused 10-minute grammar drill each day — verb conjugations, gender rules, accent placement — prevents this slow mark bleed.',
          'Finally, many students [[do not finish the written paper]]. With reading comprehension (120 marks) and written expression (100 marks) to complete in 2 hours 30 minutes, time management is critical. Allocate your time before you start: roughly 75 minutes for reading comprehension, 65 minutes for written expression, and 10 minutes for review. If you are running short, move on — an incomplete answer in one section is better than no answer in another.'
        ],
        highlights: [
          { term: 'neglecting the oral and aural', description: 'The oral (100) and aural (80) are worth 180 marks combined — 45% of your grade. Students who under-prepare these components are leaving the easiest marks on the table.' },
          { term: 'basic grammatical errors', description: 'Consistent errors in verb endings, gender, and accents slowly erode your marks across every written answer. Ten minutes of daily targeted grammar practice eliminates most of these.' },
          { term: 'do not finish the written paper', description: 'Time pressure is real. Plan your time before the exam starts and stick to it. An imperfect but complete paper always scores higher than a beautiful but unfinished one.' }
        ],
      },
      // Section 5 — Study Techniques
      {
        title: 'How to Study French',
        eyebrow: '05 // Study Techniques',
        paragraphs: [
          'French rewards [[daily immersion]] over marathon study sessions. The most effective strategy is short, frequent exposure to the language across all four skills — speaking, listening, reading, and writing. Even 20 minutes a day, split across two activities, is more effective than a two-hour block once a week.',
          'For the oral, practise with a partner or record yourself answering common questions. Prepare 10 to 12 topics: family, school, hobbies, holidays, current events, future plans, a film or book you like, technology, health, and your prepared subject. For each topic, have key vocabulary, two or three opinions with justifications, and a short anecdote or example. Practise until your answers feel natural, not memorised.',
          'For listening skills, build a [[daily listening habit]]. French podcasts like "Journal en français facile" (RFI) or "Coffee Break French" are excellent. Start at a level you can mostly understand and gradually increase difficulty. When listening, focus on grasping the main ideas first, then specific details. Past paper aural recordings (available from your teacher or the SEC) are the best exam-specific practice — do one section per week under timed conditions.',
          'For the written paper, create a **phrase bank** organised by function: expressing opinion ("À mon avis...", "Il me semble que..."), comparing ("par rapport à...", "tandis que..."), concluding ("En fin de compte...", "Pour conclure..."). Practise using these phrases in timed writing exercises. Write one full piece (letter, essay, or article) per week under exam conditions. This builds both language quality and time management skills simultaneously.'
        ],
        highlights: [
          { term: 'daily immersion', description: 'Language skills atrophy without regular use. Twenty minutes of daily French — a podcast, a written paragraph, a spoken practice — maintains and grows your ability far more effectively than weekend cramming.' },
          { term: 'daily listening habit', description: 'Aural skills improve fastest with consistent daily exposure. Even 10 minutes of French audio per day trains your ear to recognise natural speech patterns, liaisons, and common expressions.' }
        ],
      },
      // Section 6 — Action Plan
      {
        title: 'Your French Action Plan',
        eyebrow: '06 // Action Plan',
        paragraphs: [
          'This week, record yourself answering **five common oral exam questions** in French. Use these: "Parlez-moi de votre famille", "Qu\'est-ce que vous aimez faire pendant votre temps libre?", "Décrivez votre école", "Quels sont vos projets pour l\'avenir?", and "Parlez-moi d\'un film ou livre que vous avez aimé". Give yourself two minutes per answer. Listen back and note where you hesitate, switch to English thinking, or repeat the same phrases. Then re-record.',
          'Next, find one past paper [[aural exam]] recording and complete one section under timed conditions. Check your answers against the marking scheme. Note which types of details you missed — was it numbers? Opinions? Reasons? This tells you exactly what to listen for next time.',
          'Finally, start your written phrase bank. Write down 10 versatile French phrases you can use in any essay or letter. Include at least two for opening, two for expressing opinions, two for giving examples, two for comparing, and two for concluding. Pin this list above your desk and add to it weekly.'
        ],
        highlights: [
          { term: 'aural exam', description: 'Past paper aural recordings are your best practice tool. The format and question types are highly consistent year to year, so practising with real past papers directly prepares you for the exam.' }
        ],
        commitmentText: 'This week, I will record myself answering five common oral questions in French and complete one past paper aural section under timed conditions.',
      },
    ],
  },

  // ---------------------------------------------------------------------------
  // GERMAN
  // ---------------------------------------------------------------------------
  german: {
    subjectId: 'german',
    subjectName: 'German',
    moduleNumber: '04',
    moduleTitle: 'Mastering German',
    moduleSubtitle: 'Navigate cases, nail the oral, and master the written paper\'s mark structure',
    moduleDescription: 'German rewards structure and precision. This module shows you how the exam is built, where the marks are concentrated, and how to turn German grammar from a headache into a scoring tool.',
    themeName: 'slate',
    finishButtonText: "Los Geht's!",
    sections: [
      // Section 1 — Exam Structure
      {
        title: 'How German Actually Works',
        eyebrow: '01 // Exam Structure',
        paragraphs: [
          'Leaving Cert German at Higher Level follows the same three-component structure as the other modern European languages, worth a total of **400 marks**. The breakdown is: [[Oral Exam]] worth **100 marks** (25%), [[Aural Exam]] worth **80 marks** (20%), and the [[Written Exam]] worth **220 marks** (55%). The oral and aural together determine **45%** of your grade before you write a single essay.',
          'The oral takes place in spring (March/April) and lasts **12 to 15 minutes**. It is a conversation with an external examiner covering your prepared topic, general conversation (school, hobbies, family, current affairs, future plans), and responses to visual or situational prompts. The entire exam is conducted in German.',
          'The aural exam is a **listening test lasting approximately 40 minutes**, sat during the written exam session. You hear a variety of recordings — dialogues, monologues, news reports, and announcements — and answer questions. Each recording is typically played twice. The questions test your ability to extract specific information and understand the gist of spoken German.',
          'The written paper runs for **2 hours 30 minutes** and is split into [[Reading Comprehension]] (Leseverständnis, **120 marks**) and [[Written Production]] (Schriftliche Produktion, **100 marks**). Reading comprehension involves two German texts with questions. Written production requires you to write a substantial piece — usually a letter, email, essay, article, or diary entry — responding to a given prompt, plus a shorter reaction task (Äußerung zum Thema).'
        ],
        highlights: [
          { term: 'Oral Exam', description: 'Worth 100 marks (25%). A conversation in German lasting 12-15 minutes. You can control a large portion of this through thorough topic preparation and conversation practice.' },
          { term: 'Aural Exam', description: 'Worth 80 marks (20%). A listening comprehension sat during the written exam session. Consistent practice with past paper recordings is the fastest way to improve your score.' },
          { term: 'Written Exam', description: 'Worth 220 marks (55%). Combines reading (120 marks) and writing (100 marks) tasks across 2 hours 30 minutes. Time management is critical.' },
          { term: 'Reading Comprehension', description: 'Leseverständnis, 120 marks — the largest single component of the written paper. Tests your understanding of written German through questions on passages. Accuracy and completeness of answers are rewarded.' },
          { term: 'Written Production', description: 'Schriftliche Produktion, 100 marks. You produce original German writing in response to prompts. Language quality, accuracy, and relevance are assessed.' }
        ],
      },
      // Section 2 — Marking Criteria
      {
        title: 'What the Examiner Rewards',
        eyebrow: '02 // Marking Criteria',
        paragraphs: [
          'In the oral, examiners reward students who can [[communicate naturally in German]]. This means responding to questions with more than one-sentence answers, expressing opinions and justifying them, and keeping the conversation flowing. The examiner is not trying to trick you — they want to hear you speak German confidently. Students who prepare topics thoroughly and practise spontaneous responses consistently score highest.',
          'For the written paper, the marking scheme places heavy emphasis on **grammatical accuracy**. German has four cases (Nominativ, Akkusativ, Dativ, Genitiv), gendered nouns, and strict word order rules. The examiner rewards correct case usage, accurate verb conjugation (especially in past tenses and the subjunctive/Konjunktiv II), and proper word order in main and subordinate clauses. Consistent grammatical accuracy is the clearest marker of a top-band answer.',
          'Beyond accuracy, the examiner looks for [[language variety and complexity]]. Using only simple "Ich habe... Ich bin... Es ist..." structures keeps you in the mid-range. Top-band answers incorporate subordinate clauses (weil, obwohl, wenn, dass), relative clauses, and varied connectors. They use a range of tenses and demonstrate vocabulary beyond the basics.',
          'In the reading comprehension, marks are awarded for **accurate extraction of information** from the text. Answer precisely — the examiner checks whether you understood the specific detail being asked about. Vague or overly general answers lose marks even if they are partially correct. Quote from or closely paraphrase the text wherever possible.'
        ],
        highlights: [
          { term: 'communicate naturally in German', description: 'The oral rewards genuine communication. Practise having real conversations, not reciting scripts. If you can discuss your opinions, share anecdotes, and respond to follow-up questions, you will score well.' },
          { term: 'language variety and complexity', description: 'Top marks require varied sentence structures. Practise using subordinate clauses (weil, dass, obwohl), the passive voice, and Konjunktiv II. These structures signal advanced competence to the examiner.' }
        ],
      },
      // Section 3 — High-Value Zones
      {
        title: 'Where Your Marks Are',
        eyebrow: '03 // High-Value Zones',
        paragraphs: [
          'The [[oral exam]] is your highest-efficiency mark opportunity. At 100 marks (25%), it rewards direct preparation more predictably than any other component. You know the format, you can prepare your topic in advance, and you can practise the most common question types until your answers flow naturally. Because so much of the oral is within your control, students who invest in it reliably outperform what their written paper alone would predict.',
          'Within the written paper, the **Written Production section** (approximately 100 marks) is where the biggest mark variation occurs between students. A strong letter or essay — well-structured, grammatically accurate, with varied vocabulary — can score in the 80s or 90s. A weak one might score in the 40s. The preparation strategy is clear: practise writing in multiple formats (formal letter, informal letter, essay, article, diary entry) and build a [[bank of versatile phrases]] for each format.',
          'The aural exam at **80 marks (20%)** is frequently the most under-prepared component, yet it offers reliable marks for students who practise. The format is consistent year after year: similar types of recordings, similar question structures. Doing one past paper aural section per week for two months before the exam is enough to see significant improvement. The marks are there for anyone willing to put on headphones regularly.',
          'In the reading comprehension, look for [[inference questions]] — these are often worth the most marks and require you to go beyond surface understanding. Questions like "What can you infer about the author\'s attitude?" or "Why do you think the person made this decision?" are where the examiner differentiates between students who merely decode the text and those who truly understand it.'
        ],
        highlights: [
          { term: 'oral exam', description: 'The most preparable component. Your topic, common questions, and key vocabulary are all within your control. Serious oral preparation is the single highest-return investment in German.' },
          { term: 'bank of versatile phrases', description: 'Build a collection of phrases for different writing formats. For letters: "Ich schreibe Ihnen, um...", for essays: "Meiner Meinung nach...", for conclusions: "Zusammenfassend lässt sich sagen..." These phrases elevate any written piece instantly.' },
          { term: 'inference questions', description: 'Higher-value questions that test deeper understanding. Practise reading German texts and asking yourself: what is the tone? What is implied but not stated? This skill separates top students.' }
        ],
      },
      // Section 4 — Common Pitfalls
      {
        title: 'What Costs You Marks',
        eyebrow: '04 // Common Pitfalls',
        paragraphs: [
          'The number one mark-killer in German is [[case errors]]. Every noun in German takes a case depending on its role in the sentence, and prepositions demand specific cases. Mixing up Akkusativ and Dativ (e.g., writing "mit der Hund" instead of "mit dem Hund") is the most common error in Leaving Cert German. The fix is systematic: learn which prepositions take which case, drill the definite and indefinite article tables until they are automatic, and check every sentence you write for case accuracy.',
          'In the oral, the biggest pitfall is **lack of development**. When the examiner asks "Was sind deine Hobbys?", answering "Ich spiele Fußball" and stopping is a wasted opportunity. Expand: "Ich spiele Fußball seit fünf Jahren. Ich spiele in einer Mannschaft in meiner Stadt. Letztes Jahr haben wir den Pokal gewonnen." Every expanded answer gives the examiner more language to reward.',
          'On the written paper, students often [[ignore word order rules]]. In German, the verb must be in second position in main clauses, and at the end in subordinate clauses. Getting word order wrong does not just lose grammar marks — it can make your sentences incomprehensible, which means you lose content marks too. Subordinate clause word order (verb-final after weil, dass, obwohl, wenn) is tested in virtually every written answer.',
          'Finally, many students run out of time on the written paper because they spend too long on reading comprehension. The reading section often feels more straightforward, so students linger there. But the written production section is where language quality — your greatest potential differentiator — is assessed. With 2 hours 30 minutes for the paper, allocate your time deliberately: approximately 75 minutes for reading (120 marks), 65 minutes for writing (100 marks), and 10 minutes for review.'
        ],
        highlights: [
          { term: 'case errors', description: 'German cases (Nominativ, Akkusativ, Dativ, Genitiv) are the most common source of errors. Learn the article tables cold and know which prepositions demand which case. This eliminates the single biggest mark drain in the subject.' },
          { term: 'ignore word order rules', description: 'German has strict word order: verb-second in main clauses, verb-final in subordinate clauses. Incorrect word order can make your meaning unclear and costs marks across grammar and content.' }
        ],
      },
      // Section 5 — Study Techniques
      {
        title: 'How to Study German',
        eyebrow: '05 // Study Techniques',
        paragraphs: [
          'German is a [[structured language]] and it responds to structured study. The most effective approach combines daily grammar drills (10 minutes), regular listening practice (15 minutes), and weekly writing exercises (45 minutes). This spread ensures you build skills across all four assessed areas simultaneously.',
          'For grammar, focus on the areas that cost the most marks: [[case system]] (article tables and preposition-case pairings), verb conjugation (present, Perfekt, Imperfekt, Konjunktiv II), and word order rules. Use flashcards or a drill app. Test yourself daily — write five sentences and check every case, every verb ending, every word order. Accuracy is a habit, not a talent.',
          'For listening, use Deutsche Welle\'s "Langsam gesprochene Nachrichten" (slowly spoken news) — it is free, daily, and pitched perfectly for Leaving Cert level. Start by listening and reading the transcript simultaneously. After a few weeks, listen first without the transcript and check how much you caught. Also work through past paper aural recordings: one full section per week under timed conditions.',
          'For the oral, prepare your topic and 10 common conversation themes. Record yourself answering questions and listen back. Pay attention to your use of tenses — the examiner expects you to use the past (Perfekt), present, and future (werden + infinitive) naturally in conversation. Practise with a partner if possible, or use a voice recorder and treat it like a mock exam. Five minutes of daily speaking practice is worth more than an hour of reading grammar notes.'
        ],
        highlights: [
          { term: 'structured language', description: 'German has clear rules — cases, word order, verb patterns. This means it responds well to systematic study. Learn the rules, drill them daily, and accuracy becomes automatic over time.' },
          { term: 'case system', description: 'The four German cases determine article forms, adjective endings, and pronoun forms. Mastering the case system is the single most impactful grammar investment you can make.' }
        ],
      },
      // Section 6 — Action Plan
      {
        title: 'Your German Action Plan',
        eyebrow: '06 // Action Plan',
        paragraphs: [
          'This week, write out the **complete definite article table** (der, die, das across all four cases, singular and plural) from memory. If you cannot do it perfectly, practise until you can. This table underpins every sentence you write and say in German. Next, write five sentences using five different prepositions and check that you used the correct case for each one. This 15-minute exercise targets the most common error in the exam.',
          'Then, choose **one past paper aural recording** and complete one section under exam conditions. Check your answers against the marking scheme. What types of information did you miss — numbers, opinions, reasons, specific details? This diagnosis tells you exactly what to listen for in future practice sessions.',
          'Finally, record yourself answering this oral question: "Erzähl mir von deiner Schule." Give yourself 90 seconds. Use at least two tenses (present for what school is like now, Perfekt for something that happened recently). Listen back. Is your German flowing or halting? Are your cases correct? Re-record until it sounds natural.'
        ],
        highlights: [
          { term: 'complete definite article table', description: 'Der/die/das across Nominativ, Akkusativ, Dativ, and Genitiv — singular and plural. If you can write this table from memory instantly, you have the foundation for accurate German. If you cannot, this is your number one priority.' }
        ],
        commitmentText: 'This week, I will write the full German article table from memory, complete one past paper aural section, and record myself answering one oral question for 90 seconds.',
      },
    ],
  },

  // ---------------------------------------------------------------------------
  // SPANISH
  // ---------------------------------------------------------------------------
  spanish: {
    subjectId: 'spanish',
    subjectName: 'Spanish',
    moduleNumber: '05',
    moduleTitle: 'Mastering Spanish',
    moduleSubtitle: 'Exploit the oral advantage and build the writing skills that examiners reward',
    moduleDescription: 'Spanish is one of the fastest-growing Leaving Cert subjects. This module shows you how to master each component — from the high-value oral to the written paper — so you can maximise your marks with targeted preparation.',
    themeName: 'orange',
    finishButtonText: 'Vamos!',
    sections: [
      // Section 1 — Exam Structure
      {
        title: 'How Spanish Actually Works',
        eyebrow: '01 // Exam Structure',
        paragraphs: [
          'Leaving Cert Spanish at Higher Level is assessed across **three components** worth a total of **400 marks**. The [[Oral Exam]] is worth **100 marks** (25%), the [[Aural Exam]] is worth **80 marks** (20%), and the [[Written Exam]] is worth **220 marks** (55%). Like all Leaving Cert modern languages, **45%** of your grade is determined by your speaking and listening skills.',
          'The oral exam takes place in spring (March/April) and is allotted **15 minutes** per candidate. It has two parts: (a) a **general conversation** in Spanish about your life, school, interests, and current affairs — during which you may also choose to discuss a literary work you have studied — and (b) a **role-play situation**. The conversation is entirely in Spanish.',
          'The aural exam is a **listening comprehension lasting approximately 40 minutes**. You hear a variety of Spanish-language recordings — conversations, interviews, news reports, announcements — and answer questions. Each recording is typically played twice. The aural is conducted during the written exam period.',
          'The written paper runs for **2 hours 30 minutes** and is built from three sections. Across them, **reading comprehension is worth roughly 120 marks** and **written production roughly 100 marks**. Section A and Section B carry the comprehension passages (Spanish read, most answers written in English); Section B also contains the **50-mark "Linked Question" (pregunta enlazada)**, the biggest single writing task; and Section C is shorter written production (a dialogue or letter, and a diary or note). Reading passages include journalistic and literary texts.'
        ],
        highlights: [
          { term: 'Oral Exam', description: 'Worth 100 marks (25%). Fifteen minutes per candidate: a general conversation in Spanish (with the option of discussing a studied literary work) plus a role-play situation. The most preparable component — rehearse common conversation topics and the role-play format until your responses flow naturally.' },
          { term: 'Aural Exam', description: 'Worth 80 marks (20%). A listening test sat during the written exam session. Spanish pronunciation is relatively phonetic, which makes listening comprehension more accessible than in French — but speed and accents can still be challenging.' },
          { term: 'Written Exam', description: 'Worth 220 marks (55%). Three sections combining reading comprehension (~120 marks) and written production (~100 marks), including a 50-mark Linked Question. Strong time management is essential.' },
          { term: 'Reading Comprehension', description: 'Roughly 120 marks across Sections A and B — journalistic and literary passages. Spanish is read and most answers are written in English. Answer precisely; "exact transcription" items require you to copy the exact Spanish phrase from the text.' },
          { term: 'Written Expression', description: 'Roughly 100 marks, led by the 50-mark Linked Question in Section B, plus shorter Section C tasks (dialogue/letter, diary/note). Quality of language, grammatical accuracy, and relevance to the prompt determine your mark.' }
        ],
      },
      // Section 2 — Marking Criteria
      {
        title: 'What the Examiner Rewards',
        eyebrow: '02 // Marking Criteria',
        paragraphs: [
          'In the oral, the examiner assesses your [[ability to communicate in Spanish]]. This means sustaining a conversation, responding to questions with developed answers, expressing and justifying opinions, and demonstrating a range of vocabulary and tenses. A student who speaks confidently with occasional errors will outscore a student who gives grammatically perfect but minimal responses. The examiner is looking for a real conversation, not a performance.',
          'For the written paper, the marking scheme rewards three things in this order: **content and relevance** (did you answer the question and include the required elements?), **quality of language** (is your vocabulary varied, your grammar accurate, and your style appropriate?), and **organisation** (is your piece well-structured with a clear opening, body, and conclusion?). All three matter, but content relevance is the gateway — if you go off-topic, even beautiful Spanish will not save you.',
          'The examiner particularly rewards students who demonstrate control of the [[subjunctive mood]]. The subjunctive is the grammar feature that most clearly separates Higher Level from Ordinary Level Spanish. Using it correctly in expressions of opinion (es importante que...), emotion (me alegra que...), and uncertainty (no creo que...) signals to the examiner that you are operating at the top of the language range.',
          'In reading comprehension, marks are precise. The examiner has a marking scheme with specific acceptable answers. Your job is to locate the relevant information in the text, understand it accurately, and express your answer clearly. Partial answers receive partial marks, so always attempt every question — even a partially correct answer is better than a blank space.'
        ],
        highlights: [
          { term: 'ability to communicate in Spanish', description: 'Oral marks reward communicative ability: can you keep a conversation going, express opinions, and respond naturally to questions? Preparation and practice matter far more than perfect grammar.' },
          { term: 'subjunctive mood', description: 'The subjunctive (subjuntivo) is the hallmark of advanced Spanish. Using it correctly in your essays and oral answers signals top-level competence. Learn the key triggers: querer que, es necesario que, no creo que, espero que, etc.' }
        ],
      },
      // Section 3 — High-Value Zones
      {
        title: 'Where Your Marks Are',
        eyebrow: '03 // High-Value Zones',
        paragraphs: [
          'The [[oral exam (100 marks)]] is your most efficient opportunity to bank marks. You choose your topic, you know the format, and you can practise until your answers are polished. Spanish pronunciation is more phonetically consistent than French, which gives many students a confidence advantage in the oral. Prepare 10 to 12 conversation topics thoroughly, and practise with a partner or by recording yourself.',
          'Within the written paper, the [[Written Expression section]] is the highest-value zone because it is where language quality is most directly rewarded. A well-crafted essay or letter with varied vocabulary, correct subjunctive use, and a clear structure can push you into the top mark band. This is also the section where preparation pays off most: students who have a bank of versatile phrases and have practised writing in multiple formats consistently outperform those who wing it on the day.',
          'The aural exam offers **reliable marks** for students who prepare. Spanish listening comprehension benefits from the language\'s relatively consistent pronunciation rules — what you see is (mostly) what you hear. Practise with past paper recordings, and supplement with Spanish-language media: news from RTVE, podcasts like "Noticias de la Semana", or Spanish-language YouTube content. The key is regular exposure to spoken Spanish at natural speed.',
          'In reading comprehension, look for questions that ask you to **identify opinions, reasons, and attitudes** — these tend to be worth more marks than simple factual extraction. They also require you to understand the text at a deeper level, which is what the examiner is looking for at Higher Level. Practise reading Spanish articles and identifying not just what is said, but why it is said and what the author thinks.'
        ],
        highlights: [
          { term: 'oral exam (100 marks)', description: 'The most preparable component. Spanish pronunciation is more phonetically transparent than French, giving many students a natural advantage. Invest in oral preparation — the return is reliable and significant.' },
          { term: 'Written Expression section', description: 'Where language quality is most directly tested. Build a phrase bank, practise in multiple formats, and use the subjunctive. This is where top students distinguish themselves.' }
        ],
      },
      // Section 4 — Common Pitfalls
      {
        title: 'What Costs You Marks',
        eyebrow: '04 // Common Pitfalls',
        paragraphs: [
          'The most common error in Leaving Cert Spanish is [[ser/estar confusion]]. Both mean "to be", but they are used in different contexts — ser for permanent characteristics, identity, and time; estar for location, temporary states, and conditions. Getting these wrong is not a minor slip — it changes the meaning of your sentence and is immediately noticeable to the examiner. Drill the rules and exceptions until the distinction is instinctive.',
          'In the oral, many students **rely on memorised scripts** and sound robotic when delivering them. Examiners pick up on this instantly, and it limits your mark because you cannot demonstrate real communicative ability. Prepare key points and vocabulary for each topic, but practise expressing them in slightly different ways each time. Flexibility, not memorisation, is the goal.',
          'On the written paper, [[tense errors]] are a major mark drain. The most common problems are: incorrect preterite vs. imperfect usage (pretérito indefinido vs. pretérito imperfecto), wrong subjunctive triggers, and confusion between the preterite and the present perfect. Spanish has a rich tense system and the examiner expects Higher Level students to use it accurately. If you are unsure about a tense, simplify your sentence rather than guessing — a correct simple sentence beats an incorrect complex one.',
          'Finally, students often underestimate the reading comprehension section and rush through it. The texts at Higher Level contain nuanced vocabulary and idiomatic expressions. Misreading one key word can lead to a completely wrong answer. Read each text twice: once for overall meaning, once for the specific details the questions ask about. Underline relevant sections as you read.'
        ],
        highlights: [
          { term: 'ser/estar confusion', description: 'The most infamous Spanish grammar pitfall. Ser: permanent traits, identity, time, origin. Estar: location, temporary states, emotions, conditions. Learn the rules, learn the exceptions (estar muerto, ser joven), and drill until it is automatic.' },
          { term: 'tense errors', description: 'Spanish has multiple past tenses (preterite, imperfect, present perfect) plus the subjunctive. Using the wrong one changes meaning. The preterite vs. imperfect distinction is especially important and frequently tested.' }
        ],
      },
      // Section 5 — Study Techniques
      {
        title: 'How to Study Spanish',
        eyebrow: '05 // Study Techniques',
        paragraphs: [
          'Spanish responds brilliantly to [[immersive daily practice]]. The language is phonetically consistent (you pronounce what you see), it shares a huge amount of vocabulary with English through Latin roots, and its grammar, while complex, follows clear patterns. These features mean that regular, focused practice yields faster improvement than in most other languages.',
          'For the oral, prepare 10 to 12 topics with key vocabulary, useful phrases, and two to three developed opinions for each. Practise answering questions aloud — not reading from notes, but speaking from memory. Record yourself and listen back. Focus on using a variety of tenses (present, past, future, conditional) naturally in your answers. Also prepare three to four questions you can ask the examiner to show engagement and buy yourself thinking time.',
          'For listening, build a [[daily Spanish audio habit]]. Even 10 minutes a day makes a measurable difference over a few months. Use past paper aural recordings as your primary resource, and supplement with Spanish podcasts, news from RTVE.es, or Spanish-language YouTube videos. When you listen, practise writing down key words and numbers — this trains exactly the skill the aural exam tests.',
          'For writing, create a phrase bank organised by task type: formal letter openings ("Estimado/a señor/a, le escribo para..."), essay opinion phrases ("En mi opinión...", "Desde mi punto de vista..."), and conclusion phrases ("En conclusión...", "Para resumir..."). Write one full piece per week under timed conditions (approximately 40 minutes for a Higher Level composition). After writing, check every verb for correct tense and conjugation, every noun for correct gender, and every adjective for correct agreement. This review step is where accuracy becomes a habit.'
        ],
        highlights: [
          { term: 'immersive daily practice', description: 'Spanish is one of the most accessible languages for daily immersion — consistent pronunciation, Latin-root vocabulary overlap with English, and abundant free online content. Use this advantage.' },
          { term: 'daily Spanish audio habit', description: 'Listening skills improve fastest with daily exposure. RTVE news, Spanish podcasts, and past paper aural recordings are all free and directly relevant to the exam.' }
        ],
      },
      // Section 6 — Action Plan
      {
        title: 'Your Spanish Action Plan',
        eyebrow: '06 // Action Plan',
        paragraphs: [
          'This week, write out the **ser vs. estar rules** from memory, including at least three examples for each. Then write 10 sentences — five using ser and five using estar — and check every one. If you get any wrong, drill that specific rule until it is automatic. This 20-minute exercise addresses the most common error in the exam.',
          'Next, prepare for the oral. Pick one common conversation theme and write out the key vocabulary (15 to 20 words), three opinions you can express about it, and a short personal anecdote. Then practise talking about it aloud for two minutes without reading from notes. Also rehearse a **role-play** — read the situation card, work out what you need to ask and say, and practise improvising it in Spanish, since part (b) of the oral is a role-play. Record yourself and listen back. Can you hear yourself using past, present, and future tenses? If not, consciously work them in.',
          'Finally, listen to **one Spanish audio resource** today — a past paper aural section, a 10-minute podcast, or a news clip from RTVE. While listening, jot down any numbers, names, and key facts you hear. Check how much you captured. Make this a daily habit and your aural score will climb steadily over the coming weeks.'
        ],
        highlights: [
          { term: 'ser vs. estar rules', description: 'Writing out the rules from memory is active recall — the most effective study technique. If you can explain when to use ser and when to use estar without checking your notes, you have genuinely learned it.' }
        ],
        commitmentText: 'This week, I will write out the ser/estar rules from memory, prepare an oral conversation theme and rehearse a role-play, and listen to one Spanish audio resource.',
      },
    ],
  },

  // ---------------------------------------------------------------------------
  // ITALIAN
  // ---------------------------------------------------------------------------
  italian: {
    subjectId: 'italian',
    subjectName: 'Italian',
    moduleNumber: '06',
    moduleTitle: 'Mastering Italian',
    moduleSubtitle: 'A smaller cohort, but the same strategic approach applies — know your exam inside out',
    moduleDescription: 'Italian is one of the smaller Leaving Cert language subjects. Its exam follows the same broad three-component shape as the other European languages, with one twist — a prescribed-literature strand in the written paper. This module shows you how to prepare efficiently across all three components and pick up every available mark.',
    themeName: 'amber',
    finishButtonText: 'Andiamo!',
    sections: [
      // Section 1 — Exam Structure
      {
        title: 'How Italian Actually Works',
        eyebrow: '01 // Exam Structure',
        paragraphs: [
          'Leaving Cert Italian at Higher Level follows the same broad assessment framework as the other modern European languages, worth a total of **400 marks**. The breakdown is: [[Oral Exam]] worth **100 marks** (25%), [[Aural Exam]] worth **80 marks** (20%), and the [[Written Exam]] worth **220 marks** (55%). Italian shares the same overall shape as French, German, and Spanish — but it has one distinctive feature: the written paper includes a **prescribed-literature strand** (a studied novel, plus an unseen literary passage), which the others do not, so do not assume the papers are interchangeable.',
          'The oral exam takes place in spring (March/April) and lasts approximately **12 to 15 minutes**. You have a conversation with an external examiner covering your prepared topic, general conversation about your life and interests, and discussion of prompts or scenarios. The entire conversation is in Italian. Because Italian is a smaller subject, you may have fewer classmates to practise with — which makes deliberate oral preparation even more important.',
          'The aural exam is a [[listening comprehension test]] lasting approximately **40 minutes**. You hear recordings in Italian — conversations, monologues, news items, announcements — and answer questions. Recordings are typically played twice. Italian pronunciation is highly phonetic, which is an advantage: what you hear closely matches what you would see written down.',
          'The written paper runs for **2 hours 30 minutes** and covers [[Reading Comprehension]] (**120 marks**) and [[Written Production]] (Section C, **100 marks**). Reading is in two parts: **Section A** — a journalistic passage (60 marks) — and **Section B** — the literary strand (60 marks), which offers an unseen literary passage and a comprehension-plus-essay on a **prescribed novel** (recent set texts have included Calvino\'s *Marcovaldo* and Sciascia\'s *A ciascuno il suo*). Written production (Section C) requires you to write pieces in Italian — a composition, a guided composition, and a formal piece — in response to prompts.'
        ],
        highlights: [
          { term: 'Oral Exam', description: 'Worth 100 marks (25%). A 12-15 minute conversation in Italian. Italian pronunciation is very regular, which helps with clarity. Prepare thoroughly — the oral is the most predictable component.' },
          { term: 'Aural Exam', description: 'Worth 80 marks (20%). A listening test sat during the written exam session. Italian\'s phonetic consistency is an advantage here — what you hear maps closely to spelling, making it easier to identify key words.' },
          { term: 'listening comprehension test', description: 'The aural tests your ability to understand spoken Italian at natural speed. Recordings include dialogues, announcements, and news-style reports. Practise with past papers and Italian-language media.' },
          { term: 'Reading Comprehension', description: '120 marks, in two sections: Section A (journalistic, 60 marks) and Section B (the literary strand, 60 marks — an unseen literary passage and a prescribed-novel comprehension with an essay).' },
          { term: 'Written Production', description: 'Section C, 100 marks. Tests your ability to produce accurate, relevant, and well-structured Italian across a composition, a guided composition, and a formal piece.' }
        ],
      },
      // Section 2 — Marking Criteria
      {
        title: 'What the Examiner Rewards',
        eyebrow: '02 // Marking Criteria',
        paragraphs: [
          'In the oral, the examiner rewards [[fluency and communicative ability]]. Can you maintain a conversation, respond to unexpected questions, and express your thoughts in Italian? A student who speaks confidently with occasional grammatical slips will outscore a student who gives hesitant, minimal answers with perfect grammar. The examiner wants to hear you using Italian as a living language.',
          'For your prepared topic, choose something you are genuinely interested in and can discuss in depth. The examiner will ask follow-up questions, so you need to be able to go beyond your prepared material. If your topic is Italian cinema, for example, be ready to discuss specific films, directors, what you liked, and how Italian cinema compares to other cinema. Depth and genuine engagement are rewarded.',
          'In the written paper, the marking criteria assess **content relevance**, **grammatical accuracy**, **vocabulary range**, and **organisation**. The top bands require more than correct Italian — they require [[sophisticated language use]]: the congiuntivo (subjunctive), conditional sentences, varied connectors (tuttavia, nonostante, infatti, quindi), and a range of tenses used accurately. Mid-range answers tend to rely on the present tense and basic vocabulary.',
          'In reading comprehension, the examiner awards marks for accurate, specific answers. If the question asks why something happened, your answer must explain the reason — not merely state what happened. Reference or quote the text to support your answers. Precision matters more than length.'
        ],
        highlights: [
          { term: 'fluency and communicative ability', description: 'The oral exam is about communication, not perfection. Confidence, developed answers, and the ability to sustain a conversation are the key markers the examiner looks for.' },
          { term: 'sophisticated language use', description: 'Top-band written Italian uses the congiuntivo, conditional tenses, relative clauses, and varied connectors. These features signal advanced competence and push your mark into the highest bands.' }
        ],
      },
      // Section 3 — High-Value Zones
      {
        title: 'Where Your Marks Are',
        eyebrow: '03 // High-Value Zones',
        paragraphs: [
          'As with all Leaving Cert languages, the [[oral at 100 marks]] is the single most efficient place to pick up marks. It is highly preparable, relatively short (12-15 minutes), and rewards thorough preparation disproportionately. Because Italian is a smaller subject with fewer students, examiners often note that well-prepared students stand out even more clearly. Invest in your oral and you bank a strong mark early.',
          'The [[Written Production section]] (approximately 100 marks) is where top students separate themselves on the written paper. A well-crafted letter or essay in Italian — with correct congiuntivo use, varied vocabulary, and a clear structure — demonstrates the kind of language competence that the marking scheme rewards at the highest level. Prepare templates for common written formats (lettera formale, lettera informale, articolo, saggio) and practise adapting them to different prompts.',
          'The aural exam at 80 marks (20%) benefits from Italian\'s phonetic regularity. Italian pronunciation is almost perfectly consistent — once you know the rules (c before e/i, gli, gn, double consonants), you can decode almost any spoken word. This makes the aural more accessible than in some other languages, but you still need to practise listening at natural speed. Past paper recordings and Italian-language podcasts or news (RAI News, for example) are your best tools.',
          'In reading comprehension, prioritise questions that ask about **opinions, reasons, and implications** — these typically carry more marks than pure factual recall. They also allow you to demonstrate a deeper level of understanding, which is what Higher Level assessment is designed to reward.',
          'Do not neglect the [[prescribed-literature strand]] in Section B (60 marks). It offers an unseen literary passage and a comprehension-and-essay on a studied novel. The essay rewards genuine knowledge of the text — three relevant, well-argued points supported from the text are enough, and quality matters more than quantity. Note the marking rule that translating the title or characters\' names into English is penalised. This is examined content the other European languages do not have, so a student who skips it walks into a section blind.'
        ],
        highlights: [
          { term: 'oral at 100 marks', description: 'The oral is the most predictable and preparable component. In a smaller subject like Italian, well-prepared students gain an even larger advantage. Prepare your topic thoroughly and practise general conversation until it flows.' },
          { term: 'Written Production section', description: 'Where language quality is directly tested. Build a phrase bank, practise multiple formats, and use the congiuntivo. This is the section with the highest mark variance between students.' },
          { term: 'prescribed-literature strand', description: 'Section B of the reading paper (60 marks) includes a comprehension-and-essay on a prescribed novel (recent set texts: Calvino\'s Marcovaldo, Sciascia\'s A ciascuno il suo) plus an unseen literary passage. The essay rewards knowledge of the text; translating the title or character names is penalised.' }
        ],
      },
      // Section 4 — Common Pitfalls
      {
        title: 'What Costs You Marks',
        eyebrow: '04 // Common Pitfalls',
        paragraphs: [
          'The most common grammatical error in Leaving Cert Italian is [[incorrect verb conjugation]], especially in the passato prossimo and imperfetto. Students mix up which auxiliary to use (essere vs. avere), forget past participle agreement with essere verbs, or confuse the two past tenses. The passato prossimo describes completed actions (Ieri sono andato al cinema), while the imperfetto describes ongoing or habitual past actions (Quando ero giovane, andavo al cinema ogni settimana). Drill the distinction until it is automatic.',
          'In the oral, the biggest mistake is giving **short, undeveloped answers**. "Mi piace il calcio" is worth almost nothing. "Mi piace il calcio perché è uno sport di squadra. Gioco nella mia squadra locale da tre anni e l\'anno scorso abbiamo vinto il campionato" is worth significantly more. Every answer should include at least two or three sentences with a justification, an example, or an additional detail.',
          'On the written paper, many students [[avoid the congiuntivo]] because they find it difficult, and instead write around it using only indicative constructions. This caps their language quality mark. The congiuntivo is not optional at Higher Level — it is one of the key features that distinguishes top-band from mid-band answers. Learn the most common triggers (penso che, credo che, è importante che, voglio che, spero che) and practise using them in every essay you write.',
          'Finally, students sometimes [[mismanage their time]] on the written paper. With reading comprehension (120 marks) and written production (100 marks) to complete in 2 hours 30 minutes, lingering too long on the reading section leaves insufficient time for writing — which is where your language quality is most directly assessed. Plan your time before you start: approximately 75 minutes for reading, 65 minutes for writing, and 10 minutes for review.'
        ],
        highlights: [
          { term: 'incorrect verb conjugation', description: 'Essere vs. avere in the passato prossimo, past participle agreement, and the passato prossimo vs. imperfetto distinction are the most common error areas. Systematic drilling eliminates these.' },
          { term: 'avoid the congiuntivo', description: 'The subjunctive (congiuntivo) is essential for Higher Level Italian. Avoiding it limits your mark. Learn the triggers, practise the forms, and include it in every essay.' },
          { term: 'mismanage their time', description: 'Time pressure on the written paper is real. Plan your time allocation before the exam starts: with 2 hours 30 minutes for the paper, roughly 75 minutes reading, 65 minutes writing, 10 minutes review.' }
        ],
      },
      // Section 5 — Study Techniques
      {
        title: 'How to Study Italian',
        eyebrow: '05 // Study Techniques',
        paragraphs: [
          'Italian is one of the most [[phonetically consistent]] European languages — pronunciation rules are clear and almost exceptionless. This is a significant advantage for both speaking and listening. Lean into it: read Italian aloud daily, even if just a paragraph from your textbook. Hearing yourself pronounce Italian correctly builds both oral confidence and aural comprehension simultaneously.',
          'For the oral, prepare 10 to 12 conversation topics with key vocabulary and developed opinions for each. Record yourself answering common questions: "Parlami della tua famiglia", "Cosa fai nel tempo libero?", "Parlami della tua scuola", "Quali sono i tuoi progetti per il futuro?", "Parlami di un film o libro che ti è piaciuto". Listen back and check: are you using different tenses? Are your answers developed (three to four sentences minimum)? Are you expressing opinions with justifications?',
          'For writing, build a [[phrase bank by function]]: opening a letter (Egregio/a Signore/a, Le scrivo per...), expressing opinion (A mio parere..., Secondo me..., Ritengo che...), comparing (d\'altra parte..., invece..., rispetto a...), and concluding (In conclusione..., Per riassumere..., In definitiva...). Practise writing one full piece per week — formal letter, informal letter, essay, or article — under timed conditions. After each piece, check every verb tense, every article-noun agreement, and every preposition.',
          'For listening, Italian-language media is your friend. RAI News, Italian podcasts, and Italian music are all freely available. Start with slower, clearer content and gradually increase difficulty. Even 10 minutes a day of Italian audio trains your ear to recognise natural speech patterns, contractions, and colloquial expressions. Supplement with past paper aural recordings for exam-specific practice.'
        ],
        highlights: [
          { term: 'phonetically consistent', description: 'Italian pronunciation follows clear, reliable rules. This makes it easier to decode spoken Italian and easier to produce clear spoken Italian yourself. Use this advantage by reading aloud and listening actively.' },
          { term: 'phrase bank by function', description: 'Organise your phrases by what they do (opening, opining, comparing, concluding) rather than by topic. This makes them versatile — you can deploy them in any essay regardless of the specific prompt.' }
        ],
      },
      // Section 6 — Action Plan
      {
        title: 'Your Italian Action Plan',
        eyebrow: '06 // Action Plan',
        paragraphs: [
          'This week, write out the **passato prossimo conjugation** of five common Italian verbs — three that use avere (mangiare, vedere, scrivere) and two that use essere (andare, partire). Include the full conjugation (io, tu, lui/lei, noi, voi, loro) and check every past participle agreement. If you make errors, drill until you get them right. This targets the most common grammar error in the exam.',
          'Next, prepare your oral topic. Write down 15 key vocabulary words, three opinions with justifications, and one personal anecdote. Then practise explaining your topic aloud for two minutes without notes. Record yourself and listen back — are you speaking in full sentences? Using more than one tense? Sounding natural rather than reciting?',
          'Finally, start your phrase bank. Write down **10 versatile Italian phrases** you can use in any essay: two for opening, two for expressing opinion, two for giving examples, two for contrasting, and two for concluding. Keep this list visible when you study and add to it every week.'
        ],
        highlights: [
          { term: 'passato prossimo conjugation', description: 'The passato prossimo is the most-used past tense in Italian and the one most frequently tested. Knowing which verbs use essere vs. avere, and getting the past participle agreement right, is foundational.' }
        ],
        commitmentText: 'This week, I will write out passato prossimo conjugations for five verbs from memory, prepare my oral topic with key vocabulary and opinions, and start a phrase bank with 10 versatile Italian phrases.',
      },
    ],
  },

  // ---------------------------------------------------------------------------
  // JAPANESE
  // ---------------------------------------------------------------------------
  japanese: {
    subjectId: 'japanese',
    subjectName: 'Japanese',
    moduleNumber: '07',
    moduleTitle: 'Mastering Japanese',
    moduleSubtitle: 'Navigate three scripts, the oral, and a unique exam structure with confidence',
    moduleDescription: 'Japanese is one of the most distinctive Leaving Cert language subjects — three writing systems, a unique cultural context, and an exam that rewards both linguistic accuracy and cultural understanding. This module breaks it all down.',
    themeName: 'red',
    finishButtonText: 'Ganbare!',
    sections: [
      // Section 1 — Exam Structure
      {
        title: 'How Japanese Actually Works',
        eyebrow: '01 // Exam Structure',
        paragraphs: [
          'Leaving Cert Japanese assesses the same core skills as the other language subjects — speaking, listening, reading, and writing — through an [[Oral Exam]], an [[Aural Exam]], and a [[Written Exam]]. Confirm the exact mark allocation and weighting for your year from the SEC exam paper and your teacher, as Japanese is examined under its own arrangements rather than the curricular-language pattern. Whatever the precise split, the principle holds: spread your preparation across all four skills, because each one carries marks.',
          'The oral exam takes place in spring (March/April) and is a **conversation** with an external examiner. It covers your prepared topic, general conversation about your life and interests, and responses to prompts or scenarios. The conversation is conducted in Japanese. You may also be asked to read a short passage aloud, which tests your pronunciation and reading fluency.',
          'The aural exam is a [[listening comprehension test]]. You hear recordings in Japanese — dialogues, announcements, short passages — and answer questions. Japanese aural comprehension requires tuning your ear to features like particles (は, が, を, に), levels of formality (desu/masu vs. plain form), and the SOV (Subject-Object-Verb) sentence structure that differs fundamentally from English.',
          'The written paper comprises [[Reading Comprehension]] and [[Written Production]]. A defining feature of Japanese is that reading tests your ability to read across three scripts: [[Hiragana]], [[Katakana]], and [[Kanji]]. Written production requires you to write in Japanese — which means demonstrating command of these scripts in your answers.'
        ],
        highlights: [
          { term: 'Oral Exam', description: 'A conversation in Japanese with an external examiner. Politeness levels (desu/masu form) and natural conversational flow are key markers the examiner listens for. Check the exact mark value for your year with your teacher or the SEC paper.' },
          { term: 'Aural Exam', description: 'A listening test in Japanese. Tuning your ear to particles, verb endings, and the SOV sentence structure is essential preparation.' },
          { term: 'listening comprehension test', description: 'Japanese listening requires attention to sentence-final verbs (which carry the meaning), particles (which mark grammatical role), and formality levels. Regular listening practice is essential.' },
          { term: 'Reading Comprehension', description: 'Tests your ability to read and understand Japanese texts written in Hiragana, Katakana, and Kanji.' },
          { term: 'Written Production', description: 'You produce original Japanese text. Script accuracy, grammar, and content relevance are all assessed.' },
          { term: 'Hiragana', description: 'The basic phonetic script for native Japanese words. 46 characters. You must be able to read and write Hiragana fluently — it is the foundation of all Japanese literacy.' },
          { term: 'Katakana', description: 'The phonetic script used for foreign loanwords, onomatopoeia, and emphasis. 46 characters. Many exam texts include Katakana words, and you must recognise them instantly.' },
          { term: 'Kanji', description: 'Chinese characters used in Japanese. The Leaving Cert requires knowledge of a prescribed set of Kanji. Each Kanji has at least one meaning and often multiple readings (on-yomi and kun-yomi).' }
        ],
      },
      // Section 2 — Marking Criteria
      {
        title: 'What the Examiner Rewards',
        eyebrow: '02 // Marking Criteria',
        paragraphs: [
          'In the oral, the examiner rewards your ability to [[communicate naturally in Japanese]]. This includes appropriate use of politeness levels (using desu/masu form with the examiner, which is a formal setting), natural sentence structure, and the ability to sustain a conversation. Responding with developed answers — not just one-word or one-sentence replies — is essential. Express opinions, give reasons, and include personal examples.',
          'Japanese culture places enormous emphasis on politeness and social context, and the oral exam reflects this. Using the correct level of formality, appropriate greetings (はじめまして, よろしくお願いします), and conversational fillers (ええと, そうですね) shows the examiner that you understand Japanese as a communicative system, not just a set of grammar rules.',
          'In the written paper, the marking rewards **script accuracy**, **grammatical correctness**, and **content relevance**. For script accuracy, your Hiragana and Katakana must be clearly legible and correctly formed. Kanji should be written clearly and correctly — a Kanji the examiner cannot read clearly cannot earn its marks. Practising correct stroke order is the reliable route to clean, legible characters. Grammar marking focuses on correct particle usage, verb conjugation (て-form, ない-form, past tense, potential form), and sentence structure.',
          'For [[written expression]], top marks require you to write coherently on a topic using varied grammar patterns. Using only basic desu/masu sentences (～です, ～ます) keeps you in the mid-range. Incorporating te-form connections, reasons with から/ので, contrast with が/けど, and expressing desire or intention with たい/つもり pushes you toward the top bands. The examiner wants to see range and control.'
        ],
        highlights: [
          { term: 'communicate naturally in Japanese', description: 'The oral rewards genuine communication in Japanese. Use polite form (desu/masu), develop your answers, and show understanding of conversational norms. Confidence and flow matter more than perfection.' },
          { term: 'written expression', description: 'Top-band writing uses varied grammar patterns beyond basic desu/masu. Incorporate te-form, から/ので for reasons, が/けど for contrast, and たい/つもり for intentions to show range.' }
        ],
      },
      // Section 3 — High-Value Zones
      {
        title: 'Where Your Marks Are',
        eyebrow: '03 // High-Value Zones',
        paragraphs: [
          'The [[oral exam]] is, as with all Leaving Cert languages, one of the most efficient places to bank marks — it is highly preparable. Japanese is a smaller Leaving Cert subject, and well-prepared students have an opportunity to stand out clearly in the oral. Prepare your topic thoroughly, practise common conversation questions, and ensure you are comfortable discussing your life, interests, and opinions in natural Japanese using appropriate politeness levels.',
          'Within the written paper, the [[Written Production section]] offers the highest mark variation between students. Your ability to write accurately in Japanese — using correct scripts, grammar, and a range of sentence patterns — is directly tested here. The key differentiator is grammar variety. Students who only use basic patterns score in the mid-range; students who confidently use conditional forms (たら, ば), giving reasons (ので, から), and expressing opinions (と思います) access the top bands.',
          'The aural exam rewards consistent listening practice. Japanese word order (SOV) means the verb — which often carries the key meaning — comes at the end of the sentence. Training yourself to hold the whole sentence in your mind until the verb appears is a crucial listening skill. Past paper recordings and Japanese-language content (NHK World, Nihongo con Teppei podcast) are excellent preparation tools.',
          '[[Script mastery]] is a high-value skill that underlies everything in the exam. A student who reads Hiragana and Katakana fluently and has strong Kanji knowledge will be faster and more accurate across every section — reading comprehension, aural (where scripts may appear in questions), and written production. Investing in script fluency has a multiplier effect on your entire exam performance.'
        ],
        highlights: [
          { term: 'oral exam', description: 'The most preparable component. Japanese is a smaller subject, so well-prepared students stand out. Invest in oral preparation for a reliable, high-value return.' },
          { term: 'Written Production section', description: 'Where grammar variety and script accuracy are directly tested. Use a range of grammar patterns beyond basic desu/masu to access the top mark bands.' },
          { term: 'Script mastery', description: 'Fluency in Hiragana, Katakana, and prescribed Kanji speeds up every part of the exam. Script practice has a multiplier effect — it improves reading, listening, and writing simultaneously.' }
        ],
      },
      // Section 4 — Common Pitfalls
      {
        title: 'What Costs You Marks',
        eyebrow: '04 // Common Pitfalls',
        paragraphs: [
          'The most common error in Leaving Cert Japanese is [[particle mistakes]]. Particles are the small words (は, が, を, に, で, へ, の, と) that mark the grammatical role of each word in a sentence. Using the wrong particle changes the meaning entirely — は marks the topic, が marks the subject, を marks the direct object. Confusing these is the Japanese equivalent of confusing "he" and "him" in English, except it happens in nearly every sentence. Systematic particle drilling is essential.',
          'In the oral, students often default to **plain form** when they should use **polite form** (desu/masu). The oral exam is a formal interaction with an examiner — you should use desu/masu form throughout, just as you would when speaking to a teacher or a stranger in Japan. Dropping into plain form signals either carelessness or incomplete language control, and it costs marks.',
          'On the written paper, [[script errors]] are a significant mark drain. Sloppy Hiragana, incorrect Katakana, or wrong Kanji can make your answer illegible or change its meaning. The fix is practice: write each Hiragana and Katakana character until your handwriting is clean and recognisable. For Kanji, focus on stroke order — it is the reliable route to characters that come out clean and legible rather than cramped or misshapen.',
          'Finally, many students [[struggle with reading speed]]. The written paper covers both reading and writing, so if you read Japanese slowly, you will spend too long on comprehension and not leave enough time for written production. Confirm the paper duration for your year from the SEC timetable and plan your split accordingly. Building reading speed requires daily practice — read a short Japanese text every day, even just a few sentences. Speed comes from familiarity with common vocabulary, grammar patterns, and Kanji recognition.'
        ],
        highlights: [
          { term: 'particle mistakes', description: 'Particles (は, が, を, に, で) are the most common source of errors in Japanese. Each one has a specific grammatical function. Learn them systematically and drill until correct usage is automatic.' },
          { term: 'script errors', description: 'Sloppy or incorrect script reduces legibility and costs marks. Clean, correctly-formed Hiragana, Katakana, and Kanji are non-negotiable. Practise writing daily.' },
          { term: 'struggle with reading speed', description: 'Japanese reading is slow if you have to decode each character individually. Build speed through daily reading practice — familiarity with common words and Kanji compounds dramatically increases your pace.' }
        ],
      },
      // Section 5 — Study Techniques
      {
        title: 'How to Study Japanese',
        eyebrow: '05 // Study Techniques',
        paragraphs: [
          'Japanese is a [[script-based language]], and your study approach must reflect this. Unlike European languages where the alphabet is shared, Japanese requires you to maintain fluency in three writing systems simultaneously. Dedicate 10 minutes every day to script practice: write five Hiragana characters, five Katakana characters, and review five Kanji from your prescribed list. This daily maintenance prevents script knowledge from decaying.',
          'For the oral, prepare 10 to 12 conversation topics in polite (desu/masu) Japanese. Key topics: self-introduction (自己紹介), family (家族), school (学校), hobbies (趣味), daily routine (日課), future plans (将来の計画), a trip or experience (旅行), and your prepared topic. For each, have key vocabulary, two or three opinions with reasons (～と思います, ～からです), and a personal anecdote. Practise speaking aloud — record yourself and listen back for fluency, politeness level, and variety of grammar.',
          'For listening, use [[Japanese-language audio resources]] daily. NHK World News (which offers simplified Japanese news), the Nihongo con Teppei podcast, and past paper aural recordings are all excellent. When listening, focus on catching the verb at the end of each sentence — in Japanese, the verb carries the essential meaning and appears last. Also listen for particles, which signal how words relate to each other.',
          'For the written paper, build vocabulary using flashcards (physical or apps like Anki). Organise vocabulary by topic to match common exam themes. For grammar, work through patterns systematically: te-form, ない-form, past tense, たい (want to), ことがある (have experienced), つもり (plan to), ほうがいい (should). Practise writing short paragraphs (100-150 characters) using a target grammar pattern each day. This builds both writing accuracy and grammar range simultaneously.'
        ],
        highlights: [
          { term: 'script-based language', description: 'Japanese requires fluency in three scripts: Hiragana (46 characters), Katakana (46 characters), and a prescribed set of Kanji. Daily script practice prevents decay and maintains reading speed.' },
          { term: 'Japanese-language audio resources', description: 'NHK World (simplified news), podcasts like Nihongo con Teppei, and past paper aural recordings are all free and highly effective. Even 10 minutes of daily listening builds comprehension rapidly.' }
        ],
      },
      // Section 6 — Action Plan
      {
        title: 'Your Japanese Action Plan',
        eyebrow: '06 // Action Plan',
        paragraphs: [
          'This week, test yourself on all **46 Hiragana and 46 Katakana** characters. Write them all out from memory. Circle any you get wrong or hesitate on, and drill those specific characters daily until they are instant. If your scripts are not fluent, nothing else in the exam will go smoothly — this is your foundation and your highest priority.',
          'Next, choose **five Kanji** from your prescribed list that you find difficult. Write each one five times, paying attention to stroke order. Then write a short sentence using each Kanji in context. This combines script practice with vocabulary reinforcement. Do this with five new Kanji every week and you will steadily build your Kanji confidence.',
          'Finally, prepare your [[oral self-introduction (自己紹介)]] in polite Japanese. Include your name, age, school, hobbies, and one interesting fact about yourself. Practise saying it aloud until it flows naturally — no reading from notes. Record yourself and check: are you using desu/masu form? Are your particles correct? Does it sound like a natural introduction? This is your opening in the oral exam, and a confident start sets the tone for the whole conversation.'
        ],
        highlights: [
          { term: 'oral self-introduction (自己紹介)', description: 'Your jikoshoukai is how the oral exam begins. A confident, fluent self-introduction sets a positive tone. Prepare it thoroughly and practise until it feels natural.' }
        ],
        commitmentText: 'This week, I will test myself on all Hiragana and Katakana from memory, practise five difficult Kanji with sentences, and prepare my oral self-introduction in polite Japanese.',
      },
    ],
  },
};
