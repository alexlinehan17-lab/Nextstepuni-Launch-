/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { SubjectModuleContent } from './subjectModuleData';

export const CREATIVE_CONTENT: Record<string, SubjectModuleContent> = {
  art: {
    subjectId: 'art',
    subjectName: 'Art',
    moduleNumber: '28',
    moduleTitle: 'Mastering Art',
    moduleSubtitle: 'Your Complete Art Exam Guide',
    moduleDescription:
      'Understand the Art exam from the practical to the History of Art paper — learn what the examiner rewards and how to present your work for top marks.',
    themeName: 'fuchsia',
    finishButtonText: 'Create Your Masterpiece',
    sections: [
      // ---------------------------------------------------------------
      // Section 1 — Exam Structure
      // ---------------------------------------------------------------
      {
        title: 'How Art Actually Works',
        eyebrow: '01 // Exam Structure',
        paragraphs: [
          'Leaving Cert Art at Higher Level is worth **400 marks** in total and it is split across two very different skill sets: making art and writing about art. The balance between the two catches a lot of students off guard, so understanding the structure early gives you a genuine edge. There are three assessed components and each one rewards a different kind of preparation.',
          'The first component is the [[Practical Exam]], which takes place on a single exam day. You sit a **five-hour Craftwork or Imaginative Composition session** where you respond to one of the set questions in your chosen medium — painting, design, printmaking, sculpture, fabric work, calligraphy, graphics, or any other approved area. Later the same day (or on a separate scheduled sitting), you complete a [[Life Drawing]] session, typically lasting one and a half hours, working from a live model. Together the practical exam accounts for roughly **62.5%** of your total mark — that is **250 out of 400 marks**.',
          'The second component is the [[Art History and Appreciation]] written paper, which is sat in the normal June exam period. This paper is worth **150 marks — 37.5% of your total**. It covers Irish art, European art from the Renaissance to the present, and appreciation of art and design. You answer a combination of short-answer, paragraph, and essay questions drawn from set topics and gallery-based appreciation.',
          'What makes Art unusual is that you build your practical skills throughout the year and then demonstrate them under timed conditions on exam day, while the written paper tests your ability to discuss and analyse art. Both components matter, and ignoring either one will cap your grade.'
        ],
        highlights: [
          {
            term: 'Practical Exam',
            description:
              'The hands-on exam day where you produce a Craftwork or Imaginative Composition piece (5 hours) plus a Life Drawing (approx. 1.5 hours). Worth roughly 250 out of 400 marks.'
          },
          {
            term: 'Life Drawing',
            description:
              'A timed drawing session from a live model, assessed on observation, proportion, tone, and line quality. It is part of the practical exam component.'
          },
          {
            term: 'Art History and Appreciation',
            description:
              'A written exam paper worth 150 marks (37.5%) covering Irish art, European art movements, and gallery/design appreciation.'
          }
        ]
      },
      // ---------------------------------------------------------------
      // Section 2 — Marking Criteria
      // ---------------------------------------------------------------
      {
        title: 'What the Examiner Rewards',
        eyebrow: '02 // Marking Criteria',
        paragraphs: [
          'In the practical exam the examiner is looking for three things above all: [[Composition]], technical skill, and personal response. A strong composition means you have thought about how elements are arranged on the page or in space — balance, focal point, contrast, and use of the picture plane. Technical skill means you can actually control your chosen medium: clean colour mixing, confident line work, appropriate tonal range, and finish. Personal response is what separates the top grades from the rest — the examiner wants to see that you interpreted the question in your own way rather than producing a generic answer.',
          'Life Drawing is marked on your ability to observe and record the figure accurately. [[Proportion and anatomy]] matter, but so does the quality of your mark-making. Using a range of tones, showing an understanding of light and shadow, and capturing the pose with energy rather than stiffness will push you into the higher mark bands. Even a slightly inaccurate drawing can score well if it shows real observation.',
          'On the Art History paper the examiner rewards **specific knowledge**: names, dates, titles of works, correct art-historical terminology, and evidence that you have actually looked at the art rather than just memorised notes. For the [[Appreciation question]], you are expected to give a personal but informed response to an unseen image. Examiners look for structured answers — an introduction, discussion of formal elements, context, and a clear personal judgement. Vague answers like "I like the colours" will not score.',
          'Across both components, the pattern is the same: the examiner rewards students who combine skill with thoughtfulness. Showing that you made deliberate choices — in your medium, your composition, your essay structure — is how you access the top marks.'
        ],
        highlights: [
          {
            term: 'Composition',
            description:
              'How you arrange elements within your artwork — balance, focal point, use of space, contrast. A well-composed piece immediately signals a strong student to the examiner.'
          },
          {
            term: 'Proportion and anatomy',
            description:
              'In Life Drawing, the examiner assesses how accurately you observe and record the human figure, including correct proportions, gesture, and tonal modelling.'
          },
          {
            term: 'Appreciation question',
            description:
              'A section of the Art History paper where you respond to an unseen artwork. You must discuss formal qualities, context, and your personal reaction in a structured way.'
          }
        ]
      },
      // ---------------------------------------------------------------
      // Section 3 — High-Value Zones
      // ---------------------------------------------------------------
      {
        title: 'Where Your Marks Are',
        eyebrow: '03 // High-Value Zones',
        paragraphs: [
          'The single biggest mark zone in Leaving Cert Art is your [[Craftwork or Imaginative Composition]] — the five-hour practical. It carries the heaviest weighting within the 250-mark practical component and it is the piece where your personal style, medium choice, and preparation all come together. If you want to maximise your grade, this is the piece that deserves the most practice time across the year. Think of every class and homework piece as a rehearsal for that five-hour session.',
          'Life Drawing is a smaller slice of the practical marks but it is also the area where students can improve the most in a short time. Dedicated practice — even 20 minutes a week sketching from reference — builds the observational skills that the examiner is looking for. Many students neglect life drawing because it feels less "creative," but that is exactly why it is a high-value zone: a little effort goes a long way.',
          'On the written side, the [[Art History paper]] (150 marks) is often under-prepared. Students pour energy into their practical work and then scramble to learn art history in the final weeks. The reality is that **37.5% of your total mark** comes from this paper. Within it, the essay questions on Irish art and European art carry the most marks per question, so knowing your set topics inside out — with specific references to named artworks — is a direct route to high marks.',
          'The Appreciation section rewards students who can think on their feet. Because the image is unseen, you cannot memorise your way through it. But you can practise the skill of visual analysis throughout the year by writing short appreciation responses to artworks you encounter in galleries, textbooks, or online. The more you practise structured visual analysis, the more natural it becomes under exam conditions.'
        ],
        highlights: [
          {
            term: 'Craftwork or Imaginative Composition',
            description:
              'The main practical exam piece produced in a 5-hour timed session. It carries the largest single mark weighting in the entire Art exam.'
          },
          {
            term: 'Art History paper',
            description:
              'Worth 150 marks (37.5%). Covers Irish art, European art movements, and an appreciation section. Essay questions on set topics carry the highest marks per question.'
          }
        ]
      },
      // ---------------------------------------------------------------
      // Section 4 — Common Pitfalls
      // ---------------------------------------------------------------
      {
        title: 'What Costs You Marks',
        eyebrow: '04 // Common Pitfalls',
        paragraphs: [
          'The number one mark-killer in the practical exam is **poor time management** during the five-hour session. Students get absorbed in detail on one part of the piece and leave large areas unfinished. An incomplete composition always scores lower than a resolved one, even if the finished parts are excellent. You need to plan your time before you start: rough in the full composition in the first hour, then develop and refine systematically.',
          'In Life Drawing, the most common mistake is [[timid mark-making]]. Students draw lightly and tentatively because they are afraid of getting it wrong. The result is a faint, lifeless sketch that lacks tonal range. Examiners want to see confident, expressive lines and a full range from light to dark. It is better to commit to a bold line and adjust than to hedge with pale, scratchy marks.',
          'On the Art History paper, the biggest pitfall is **vagueness**. Writing "the artist uses colour effectively" without naming the specific colours, techniques, or artworks tells the examiner nothing. Every point should be anchored to a named work, a specific visual detail, or a recognised art term. Another common error is [[answering the wrong question]] — students see a familiar topic keyword and launch into a prepared essay without actually reading what the question asks. Always underline the key instruction words (discuss, compare, analyse) before you start writing.',
          'Finally, many students underestimate how much the Art History paper contributes to their overall grade. Treating it as an afterthought and cramming in the last two weeks is a strategy that consistently costs a full grade band or more. The written paper is worth almost two-fifths of your total — give it the time it deserves.'
        ],
        highlights: [
          {
            term: 'timid mark-making',
            description:
              'Drawing with faint, hesitant lines out of fear of making mistakes. It produces flat, lifeless work and signals a lack of confidence to the examiner.'
          },
          {
            term: 'answering the wrong question',
            description:
              'Seeing a familiar topic and writing a pre-prepared essay without reading the actual question. Always check the instruction words (discuss, compare, evaluate) first.'
          }
        ]
      },
      // ---------------------------------------------------------------
      // Section 5 — Study Techniques
      // ---------------------------------------------------------------
      {
        title: 'How to Study Art',
        eyebrow: '05 // Study Techniques',
        paragraphs: [
          'For the practical exam, the best study technique is [[structured timed practice]]. Set up mock five-hour sessions at home or in the art room where you work through the full process: reading the brief, sketching thumbnails, roughing in the composition, and developing to a finish. Do this at least three or four times before the real exam. Each session will teach you something about pacing, medium handling, and decision-making under pressure that no amount of casual sketching will replicate.',
          'For Life Drawing, build a habit of quick observational sketches. Use a timer: five-minute poses, then two-minute poses, then thirty-second gesture drawings. The shorter the time, the more you train your eye to capture the essential proportions and movement of the figure. Supplement live sessions with practice from photo references if access to a model is limited — the key skill is sustained, focused observation.',
          'For Art History, create [[visual flashcards]] — one side shows an image of the artwork, the other side lists the artist, date, movement, key formal qualities, and a brief personal response. Test yourself by looking at the image and recalling the details, then flip and check. This mirrors the appreciation skill the examiner tests: looking at art and articulating an informed response. Aim to cover at least 15 to 20 key works across your Irish and European topics.',
          'Finally, practise writing timed essay answers. Give yourself 30 minutes and one Art History question, and write a full answer by hand. Then compare it against the marking scheme and examiner notes. Focus on including **specific references** — title, artist, date, visual detail — in every paragraph. The habit of anchoring every point to a concrete example is the single most effective way to improve your Art History grade.'
        ],
        highlights: [
          {
            term: 'structured timed practice',
            description:
              'Running full mock practical sessions under exam-like time constraints. This builds your ability to manage pacing, medium control, and composition decisions under pressure.'
          },
          {
            term: 'visual flashcards',
            description:
              'Cards with an artwork image on one side and key details (artist, date, movement, formal analysis) on the other. They train the recall and visual analysis skills tested in the exam.'
          }
        ]
      },
      // ---------------------------------------------------------------
      // Section 6 — Action Plan
      // ---------------------------------------------------------------
      {
        title: 'Your Art Action Plan',
        eyebrow: '06 // Action Plan',
        paragraphs: [
          'Start by auditing where you stand right now. Rate your confidence from 1 to 5 in each of the three components: Craftwork/Imaginative Composition, Life Drawing, and Art History. Whichever area scores lowest is where your biggest point gains are hiding. Most students find that Art History is their weakest link — if that is you, commit to two focused study sessions per week on your set topics starting now.',
          'Build a weekly rhythm that covers all three areas. Dedicate at least one session to [[practical work]] (a timed piece or focused medium practice), one session to Life Drawing (even 20 minutes of gesture drawing counts), and one session to Art History (flashcard review, a timed essay, or reading about a set topic). Consistency across all three components is what separates H1 students from everyone else.',
          'In the final month before the exam, shift your focus to exam simulation. Do at least two full five-hour mock practicals under real conditions. Write two or three timed Art History essays per week. Review your Life Drawing folder and identify which poses and angles you find hardest — then practise those specifically. The students who walk into the Art exam feeling prepared are the ones who have already done it all before under pressure.'
        ],
        highlights: [
          {
            term: 'practical work',
            description:
              'Dedicated sessions working in your chosen medium under timed or semi-timed conditions, replicating the demands of the 5-hour practical exam.'
          }
        ],
        commitmentText:
          'I will identify my weakest Art component this week, schedule dedicated practice time for it, and complete at least one full timed mock session within the next two weeks.'
      }
    ]
  },

  music: {
    subjectId: 'music',
    subjectName: 'Music',
    moduleNumber: '29',
    moduleTitle: 'Mastering Music',
    moduleSubtitle: 'Your Complete Music Exam Guide',
    moduleDescription:
      'Decode the Music exam — from the practical performance to the listening and composing components — and understand where the high-value marks are.',
    themeName: 'purple',
    finishButtonText: 'Hit the Right Note',
    sections: [
      // ---------------------------------------------------------------
      // Section 1 — Exam Structure
      // ---------------------------------------------------------------
      {
        title: 'How Music Actually Works',
        eyebrow: '01 // Exam Structure',
        paragraphs: [
          'Leaving Cert Music at Higher Level is worth **400 marks** and it is divided into three distinct components that test completely different skills. Unlike most Leaving Cert subjects, Music is not just a written exam — a full **50% of your marks** come from practical and coursework elements that are assessed outside the exam hall. Understanding how the three components fit together is the first step to a smart strategy.',
          'The [[Listening Paper]] is the written exam, sat in June, and it is worth **200 marks — 50% of your total**. It runs for approximately **two and a half hours** and covers three areas: set works (prescribed pieces that change periodically), general listening (identifying instruments, forms, textures, and styles from unfamiliar excerpts), and music literacy including theory, harmony, and history questions. You listen to recorded excerpts and answer a mix of short-answer and extended questions.',
          'The [[Performing]] component is worth **100 marks — 25%** of your total. This is a practical exam where you perform a programme of pieces on your chosen instrument or voice, assessed by a visiting examiner. Your programme must meet specific requirements regarding duration, difficulty, and variety. This exam typically takes place in the spring of your Leaving Cert year.',
          'The [[Composing]] component is also worth **100 marks — 25%**. You submit a portfolio of compositions as coursework, usually including a melody composition and a harmony exercise or arrangement task as well as an original composition. The portfolio is prepared throughout the year and submitted before a set deadline. Between performing and composing, you have half your marks decided before you ever sit the written paper in June.'
        ],
        highlights: [
          {
            term: 'Listening Paper',
            description:
              'The written exam worth 200 marks (50%). Approximately 2.5 hours long, covering set works, general listening, and music literacy/theory questions.'
          },
          {
            term: 'Performing',
            description:
              'A practical exam worth 100 marks (25%). You perform a programme of pieces on your instrument or voice for a visiting examiner in the spring.'
          },
          {
            term: 'Composing',
            description:
              'A coursework portfolio worth 100 marks (25%). Includes melody composition, harmony/arrangement exercises, and an original composition, submitted before a set deadline.'
          }
        ]
      },
      // ---------------------------------------------------------------
      // Section 2 — Marking Criteria
      // ---------------------------------------------------------------
      {
        title: 'What the Examiner Rewards',
        eyebrow: '02 // Marking Criteria',
        paragraphs: [
          'In the Performing exam, the examiner assesses [[technical proficiency]], musicality, and programme choice. Technical proficiency means you can play or sing accurately — correct notes, rhythm, intonation, and tempo. Musicality goes beyond accuracy: it includes dynamics, phrasing, expression, and your ability to communicate the character of each piece. Programme choice matters too — selecting pieces that show a range of styles, tempos, and moods demonstrates versatility and earns higher marks than performing three similar pieces.',
          'For the Composing portfolio, the examiner rewards creativity, technical correctness, and understanding of musical structure. In [[melody composition]], they look for a well-shaped melodic line with a clear sense of phrase structure, appropriate cadences, and stylistic consistency. In harmony exercises, accuracy in part-writing, correct voice leading, and avoidance of parallel fifths and octaves are essential. Your original composition is where you can show real creative flair — but it still needs to demonstrate solid craft.',
          'On the Listening Paper, the set works questions reward **detailed knowledge** of the prescribed pieces: instrumentation, structure, harmonic language, historical context, and the ability to identify specific passages when they are played. General listening questions test your ear — can you identify an oboe from a clarinet, a rondo from a sonata form, a major key from a minor key? Music literacy questions reward students who understand [[music theory]] at a practical level: intervals, chords, keys, time signatures, and standard notation.',
          'Across all three components, the examiner is looking for the same underlying quality: a student who engages deeply with music rather than going through the motions. In performance, that means playing with feeling. In composition, it means making deliberate creative choices. In listening, it means hearing structure and detail, not just sound.'
        ],
        highlights: [
          {
            term: 'technical proficiency',
            description:
              'Accurate playing or singing — correct notes, rhythm, intonation, and tempo. The foundation of a strong performance mark, though musicality is equally important.'
          },
          {
            term: 'melody composition',
            description:
              'A task requiring you to write a melodic line with clear phrase structure, appropriate cadences, and stylistic consistency. Assessed on shape, flow, and musical logic.'
          },
          {
            term: 'music theory',
            description:
              'Knowledge of intervals, chords, keys, time signatures, scales, and standard notation. Tested directly in the Listening Paper and applied in your composing work.'
          }
        ]
      },
      // ---------------------------------------------------------------
      // Section 3 — High-Value Zones
      // ---------------------------------------------------------------
      {
        title: 'Where Your Marks Are',
        eyebrow: '03 // High-Value Zones',
        paragraphs: [
          'The [[Listening Paper]] is the single largest mark zone at **200 marks (50%)**. Within it, the set works section is the most predictable and therefore the most "studyable" part of the entire Music exam. You know exactly which pieces will be examined, so you can prepare detailed notes on every aspect — form, instrumentation, harmony, historical context — and walk in knowing that those questions are coming. Students who know their set works inside out consistently score highest on this paper.',
          'Your [[Performing]] exam (100 marks) is a high-value zone because it is assessed entirely on the day and rewards sustained practice across the year. The key insight is that programme selection can make or break your mark. Choose pieces that sit comfortably within your ability — slightly challenging but not so difficult that you risk errors under pressure. A confident, musical performance of a Grade 5 piece will outscore a shaky, anxious performance of a Grade 7 piece every time.',
          'The [[Composing]] portfolio (100 marks) is often the most overlooked area, yet it is the component where you have the most control. Unlike the listening paper (timed exam) or the performance (one-shot assessment), your composition portfolio is coursework — you can draft, revise, get feedback, and refine before you submit. Students who start their compositions early and go through multiple drafts consistently achieve higher marks than those who rush them at the last minute.',
          'Within the Listening Paper, the general listening and music literacy sections are areas where focused study pays off quickly. Learning to reliably identify instruments, forms, and basic harmonic progressions is a trainable skill. Spending 15 minutes a day on ear training — using apps, past papers, or just active listening to a range of music — can lift your general listening marks significantly within a few weeks.'
        ],
        highlights: [
          {
            term: 'Listening Paper',
            description:
              'Worth 200 marks (50%). The set works section is the most studyable part of the exam — you know exactly which pieces will be tested.'
          },
          {
            term: 'Performing',
            description:
              'Worth 100 marks (25%). Programme selection is critical — choose pieces that showcase your range while staying within comfortable technical reach.'
          },
          {
            term: 'Composing',
            description:
              'Worth 100 marks (25%). As coursework, this is the component where you have the most control. Multiple drafts and early starts lead to significantly better marks.'
          }
        ]
      },
      // ---------------------------------------------------------------
      // Section 4 — Common Pitfalls
      // ---------------------------------------------------------------
      {
        title: 'What Costs You Marks',
        eyebrow: '04 // Common Pitfalls',
        paragraphs: [
          'The most common mark-killer in the Performing exam is [[over-ambitious programme selection]]. Students pick pieces that are too difficult, hoping to impress the examiner, and then perform them with noticeable errors, poor tempo control, or visible anxiety. The examiner is not grading the difficulty of your repertoire — they are grading how well you play it. A polished, expressive performance of a moderately difficult piece will always beat a stumbling attempt at a virtuoso showpiece.',
          'In Composing, the biggest pitfall is **leaving it too late**. Because the portfolio is coursework with a deadline, many students treat it like a homework assignment and rush it in the final weeks. Compositions written under time pressure tend to be formulaic, short, and lacking in development. The melody may wander without clear phrasing, the harmony exercise may have basic voice-leading errors, and the original piece may feel unfinished. Start your portfolio early in the year and build in time for at least two rounds of revision.',
          'On the Listening Paper, the most damaging mistake is [[neglecting the set works]]. Some students assume they can rely on their general musical knowledge and skip the detailed study of prescribed pieces. But set works questions are worth a significant portion of the paper and they require very specific answers — identifying exact bars, naming precise instruments, explaining particular harmonic choices. General knowledge will not get you through these questions. You need to know the set works bar by bar.',
          'Another common pitfall across the paper is poor use of musical terminology. Writing "the music gets louder" instead of "there is a crescendo" or "the tune goes up" instead of "the melody moves by ascending stepwise motion" costs you marks. Examiners expect Higher Level students to use correct technical vocabulary. Build a glossary of key terms — [[dynamics]], articulation, texture, form, cadence — and use them consistently in your answers.'
        ],
        highlights: [
          {
            term: 'over-ambitious programme selection',
            description:
              'Choosing performance pieces that are too difficult, leading to errors, poor tempo, and anxiety. The examiner marks how well you play, not how hard the piece is.'
          },
          {
            term: 'neglecting the set works',
            description:
              'Failing to study the prescribed listening pieces in detail. Set works questions require bar-by-bar knowledge that general musical ability cannot replace.'
          },
          {
            term: 'dynamics',
            description:
              'The variation in loudness — piano, forte, crescendo, diminuendo. One of many technical terms you should use precisely in Listening Paper answers instead of everyday language.'
          }
        ]
      },
      // ---------------------------------------------------------------
      // Section 5 — Study Techniques
      // ---------------------------------------------------------------
      {
        title: 'How to Study Music',
        eyebrow: '05 // Study Techniques',
        paragraphs: [
          'For the Listening Paper, the most effective technique is [[annotated score study]]. Get a copy of each set work score and listen to it while following along, annotating structural features, instrumentation changes, harmonic shifts, and any details that the examiner might ask about. Do this repeatedly — first for the big picture (overall form, key sections), then for fine detail (specific chord progressions, rhythmic motifs, dynamic markings). After several passes, test yourself by listening without the score and seeing how much you can identify by ear alone.',
          'For general listening, train your ear systematically. Use past paper audio tracks and practise identifying instruments, textures, time signatures, and musical forms. Build an [[instrument recognition]] habit by listening to orchestral recordings and picking out individual parts. Apps and online ear-training tools that drill intervals, chords, and scales are also excellent — even 10 to 15 minutes a day makes a measurable difference over a few months. Irish traditional music and [[sean-nos]] singing are part of the syllabus, so make sure you are familiar with the sounds of traditional instruments (uilleann pipes, bodhran, tin whistle, fiddle) and the characteristics of sean-nos vocal style.',
          'For Performing, the key study technique is **spaced, focused practice** rather than marathon sessions. Practise your programme pieces in short, concentrated blocks — 20 to 30 minutes of focused work is more productive than two hours of distracted playing. Record yourself regularly and listen back critically. Perform for friends, family, or your teacher as often as possible to simulate the pressure of the exam. The more you perform under observation, the less nervous you will be on the day.',
          'For Composing, study model compositions before you write your own. Look at past high-scoring student portfolios if your teacher has examples, or analyse short works by established composers to understand how they achieve structure, contrast, and development. When drafting your own compositions, write freely first, then revise ruthlessly — cut what does not serve the musical idea, strengthen transitions, and check every harmony exercise against the voice-leading rules.'
        ],
        highlights: [
          {
            term: 'annotated score study',
            description:
              'Listening to a set work while following and marking up the score — noting form, instrumentation, harmony, and key moments. The most effective way to prepare for set works questions.'
          },
          {
            term: 'instrument recognition',
            description:
              'The ability to identify instruments by their timbre in a recording. A trainable skill tested in the general listening section of the paper.'
          },
          {
            term: 'sean-nos',
            description:
              'Traditional Irish unaccompanied singing style characterised by ornamentation, free rhythm, and a highly personal vocal delivery. Part of the Irish music content on the syllabus.'
          }
        ]
      },
      // ---------------------------------------------------------------
      // Section 6 — Action Plan
      // ---------------------------------------------------------------
      {
        title: 'Your Music Action Plan',
        eyebrow: '06 // Action Plan',
        paragraphs: [
          'Start by mapping out your current position in each component. For Performing, confirm your programme pieces and rate your readiness from 1 to 5 on each one. For Composing, check where your portfolio stands — are all pieces drafted, or do you still have blank pages? For the Listening Paper, list the set works and honestly assess how many you could answer detailed questions on right now. This audit tells you exactly where to focus your energy.',
          'Build a weekly schedule that touches all three components. Dedicate at least **three practice sessions** to your performance pieces, **two study sessions** to [[set works and ear training]], and **one working session** to your composition portfolio. The students who score highest in Music are the ones who work on all three components consistently rather than cramming one area and neglecting the others.',
          'In the final six weeks before the exams, shift into exam simulation mode. Do at least two full mock Listening Papers under timed conditions using past papers with audio. Perform your full programme in front of an audience at least three times. Finalise and polish your composition portfolio with at least one round of feedback from your teacher. Walk into each assessment knowing you have already done it under pressure — that preparation is the difference between hoping for a good result and expecting one.'
        ],
        highlights: [
          {
            term: 'set works and ear training',
            description:
              'Combining detailed study of prescribed pieces with general ear-training exercises. Together these prepare you for the full scope of the 200-mark Listening Paper.'
          }
        ],
        commitmentText:
          'I will audit my readiness across all three Music components this week, identify the one that needs the most urgent attention, and complete one focused study session for it within the next three days.'
      }
    ]
  }
};
