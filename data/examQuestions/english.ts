/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Leaving Cert English exam questions for the Exam Strategiser.
 * 2025 Paper 1 (Higher Level), theme: Perspectives.
 * 2024 Paper 1 (Higher Level), theme: Connections.
 */

import { type ExamQuestion } from '../../types/examStrategiser';

export const englishQuestions: ExamQuestion[] = [
  {
    id: 'english-2025-p1-text1-qa-iii',
    taskType: 'english-style-elements',
    subject: 'english',
    year: 2025,
    paper: 'Paper 1',
    section: 'Section I — Comprehending — Text 1 (The Underdog Effect) Question A',
    questionNumber: '(iii)',
    level: 'higher',
    marks: 20,
    totalPaperMarks: 200,
    totalPaperMinutes: 170,
    commandWords: ['to what extent do you agree', 'support'],
    questionText: [
      {
        type: 'paragraph',
        content: [
          { text: '"In TEXT 1, David Robson uses elements of language that are effective in making this article both ' },
          { text: 'informative and thought-provoking', annotation: { note: 'Both qualities must be addressed across your answer — not necessarily equally, but ignoring one is penalised.', type: 'keyword' } },
          { text: '." ' },
          { text: 'To what extent do you agree', annotation: { note: 'Not yes/no. Take a position on the DEGREE (fully / largely / partly / disagree) and justify it. Bald agreement scores poorly.', type: 'command' } },
          { text: ' with this statement? Support your answer with reference to ' },
          { text: 'four elements of Robson\'s style', annotation: { note: 'Four is the explicit minimum. Style = HOW the writer writes (tone, statistics, anecdote, rhetorical questions, sentence structure, allusion) — NOT what they say.', type: 'keyword' } },
          { text: ' from the text. ' },
          { text: '(20)', annotation: { note: '20 marks → roughly 17 minutes. About 4 minutes per element plus 1 minute planning.', type: 'marks-allocation' } },
        ],
      },
    ],
    predictPrompts: [
      {
        id: 'p1',
        type: 'multiple-choice',
        prompt: "What's the command instruction in this question?",
        options: ['Describe', 'To what extent do you agree', 'Compare', 'Discuss'],
        correctAnswer: 'To what extent do you agree',
        debrief: {
          strategicPrinciple: '"To what extent do you agree" is a degree-of-agreement command — not yes/no. Take a position on the degree (fully / largely / partly / disagree) and justify it. Bald agreement caps Purpose because the command itself asks for a graded response.',
          commonWrongAnswer: {
            answer: 'Discuss',
            reason: 'Misreading the command word changes the shape of the answer. "Discuss" demands balanced two-sided exploration; "To what extent do you agree" demands you stake a position on degree first. The 2025 marking scheme rewards a clear stance with reasoning — neutral discussion misses Purpose.',
            source: { year: 2025, type: 'marking-scheme' },
          },
        },
      },
      {
        id: 'p2',
        type: 'number',
        prompt: 'How many style elements must you discuss (minimum)?',
        correctAnswer: 4,
        debrief: {
          strategicPrinciple: 'Four style elements is the explicit minimum. Two or three caps below H1; five-plus dilutes (no extra credit, more chance to slip). Four discrete elements, each developed properly, lands the band.',
          commonWrongAnswer: {
            answer: '2',
            reason: 'Two elements falls below the floor the question explicitly sets. The 2025 marking scheme rewards quality over volume, but volume below the stated minimum caps regardless of quality on the two you did write.',
            source: { year: 2025, type: 'marking-scheme' },
          },
        },
      },
      {
        id: 'p3',
        type: 'multiple-choice',
        prompt: 'Which counts as a "style element" rather than a "content point"?',
        options: ['The writer mentions Donald Trump', 'The writer uses statistics from a study', 'The underdog effect is real', 'Trump won in 2016'],
        correctAnswer: 'The writer uses statistics from a study',
        debrief: {
          strategicPrinciple: 'Style = HOW the writer writes (statistics, anecdote, tone, rhetorical questions, sentence structure, allusion). Content = WHAT they say (Trump, the underdog effect, the study findings). The 2025 indicative material distinguishes the two — only style elements score on this question.',
          commonWrongAnswer: {
            answer: 'The writer mentions Donald Trump',
            reason: 'Content point disguised as style. The student names something the writer talks about, not how the writer talks. The 2025 indicative material lists "factual information / statistics / real-life examples" as the style — Trump is the example, the use of real-life examples is the style.',
            source: { year: 2025, type: 'marking-scheme' },
          },
        },
      },
      {
        id: 'p4',
        type: 'short-text',
        prompt: 'The article must be shown to be both ___ and ___ (the two qualities in the statement).',
        hint: 'Informative and thought-provoking.',
        debrief: {
          strategicPrinciple: 'Both qualities — informative AND thought-provoking — must be addressed across the answer. Not necessarily equally, but ignoring one halves your engagement with the question\'s statement and is penalised under Purpose.',
          commonWrongAnswer: {
            answer: 'Informative only',
            reason: 'Engaging with only one of the two qualities misses half the question\'s framing. Even if the four elements are strong, ignoring "thought-provoking" (or "informative") caps the Purpose band because the question requires engagement with both qualities of Robson\'s style.',
            source: { year: 2025, type: 'marking-scheme' },
          },
        },
      },
    ],
    biggestMistake: {
      title: 'Listing content points instead of style elements',
      body: 'The question wants four STYLE elements — HOW Robson writes — not four content points (WHAT he says). The most common failure pattern is "he mentions Trump / he talks about the underdog effect / he gives examples / he wraps up by saying it matters" — four content points, zero style elements. Style = statistics, anecdote, tone, rhetorical questions, allusion, sentence structure. For each: identify, quote, explain effect. Both "informative" and "thought-provoking" need engagement across the answer.',
      source: { year: 2025, type: 'marking-scheme' },
    },
  },

  {
    id: 'english-2025-p1-text2-qb',
    taskType: 'english-composition-genre-task',
    subject: 'english',
    year: 2025,
    paper: 'Paper 1',
    section: 'Section I — Comprehending — Text 2 (Margaret Atwood) Question B',
    questionNumber: 'B',
    level: 'higher',
    marks: 50,
    totalPaperMarks: 200,
    totalPaperMinutes: 170,
    commandWords: ['outline', 'challenge', 'encourage'],
    questionText: [
      {
        type: 'paragraph',
        content: [
          { text: 'You are a hotel manager', annotation: { note: 'Adopt this register throughout — professional, confident, polished. Slipping into student voice loses Purpose marks.', type: 'keyword' } },
          { text: '. A recent, disgruntled guest has left a highly critical review of your hotel and its facilities on a travel-review website. You decide to challenge this person\'s views with an ' },
          { text: 'online response', annotation: { note: 'Genre = public-facing review reply (Tripadvisor / Google reviews vibe). Not a private letter. Other readers will see it.', type: 'keyword' } },
          { text: ' on the same website. In your response you should: ' },
        ],
      },
      {
        type: 'list-item',
        content: [
          { text: 'outline the proud tradition and history', annotation: { note: 'Task component 1 of 3. You MUST address this. Invent specific history details — founding year, family ownership, awards.', type: 'command' } },
          { text: ' of your establishment, ' },
        ],
      },
      {
        type: 'list-item',
        content: [
          { text: 'challenge the specific criticisms', annotation: { note: 'Task component 2 of 3. "Specific" is doing work — you need to invent plausible criticisms (cleanliness, service, food) and rebut each.', type: 'command' } },
          { text: ' of the guest reviewer, and ' },
        ],
      },
      {
        type: 'list-item',
        content: [
          { text: 'encourage the reviewer to return', annotation: { note: 'Task component 3 of 3. Forward-looking. Tone shifts from defence to invitation.', type: 'command' } },
          { text: ' by highlighting some of the ' },
          { text: 'exciting upcoming events', annotation: { note: 'Specific concrete events required — food festival, jazz weekend, local heritage week. Vague "we have lots of events" loses freshness marks.', type: 'keyword' } },
          { text: ' in your hotel and its locality. ' },
          { text: '(50)', annotation: { note: '50 marks → ~42 mins. P 15 / C 15 / L 15 / M 5. Plan structure before writing.', type: 'marks-allocation' } },
        ],
      },
    ],
    predictPrompts: [
      {
        id: 'p1',
        type: 'multiple-choice',
        prompt: 'What genre is required?',
        options: ['Personal letter', 'Online review response', 'Newspaper article', 'Speech'],
        correctAnswer: 'Online review response',
        debrief: {
          strategicPrinciple: 'Genre = online review response — public-facing, professional, Tripadvisor/Google-reviews vibe. Wrong genre (private letter, complaint letter, speech) caps Purpose because the genre is the frame for everything else.',
          commonWrongAnswer: {
            answer: 'Personal letter',
            reason: 'Personal letter implies one private recipient. The question specifies an online response on the same review website — public-facing, addressed to the reviewer but visible to potential guests reading the thread. Slipping into letter register strips the public dimension and caps Purpose.',
            source: { year: 2025, type: 'marking-scheme' },
          },
        },
      },
      {
        id: 'p2',
        type: 'number',
        prompt: 'How many distinct task components must your answer address?',
        correctAnswer: 3,
        debrief: {
          strategicPrinciple: 'Three task components required: (1) outline proud tradition, (2) challenge criticisms, (3) encourage return. The 2025 marking scheme P descriptor reflects all three. Missing one caps Purpose at the proportion you addressed.',
          commonWrongAnswer: {
            answer: '2',
            reason: 'Addressing only two components is the most common 50-mark error on Question B tasks — usually the third (encourage return) is skipped because students get into the rebuttal flow. Missing component = Purpose cap = ceiling on Coherence and Language too.',
            source: { year: 2025, type: 'marking-scheme' },
          },
        },
      },
      {
        id: 'p3',
        type: 'multiple-choice',
        prompt: 'Which voice/register should dominate?',
        options: ['Casual student voice', 'Aggressive defensive', 'Professional hotel manager', 'Detached journalist'],
        correctAnswer: 'Professional hotel manager',
        debrief: {
          strategicPrinciple: 'Register = professional hotel manager. Confident, courteous, never grovelling or aggressive. The 2025 marking scheme P descriptor requires "register of hotel manager" explicitly — slipping into student voice (or revenge-rant) caps Purpose because the register IS the Purpose for this task.',
          commonWrongAnswer: {
            answer: 'Casual student voice',
            reason: 'Student voice is the default register most candidates write in. The question requires the hotel-manager register — confident professional voice managing a public relationship. Slipping out of it is a Purpose cap because the register is what the marker is testing.',
            source: { year: 2025, type: 'marking-scheme' },
          },
        },
      },
      {
        id: 'p4',
        type: 'number',
        prompt: 'Roughly how many minutes should you spend on this?',
        correctAnswer: 42,
        debrief: {
          strategicPrinciple: 'English Paper 1 runs at 0.85 minutes per mark (170 min / 200 marks). 50 marks → 42 minutes — a quarter of the paper. Plan three components (5 min) before writing the body.',
          commonWrongAnswer: {
            answer: '30',
            reason: 'Under-budgets the question. The per-mark rate gives 42 minutes for a 50-mark Question B. 30 minutes leaves no room for planning the three components or polishing the close, and reads as rushed under the marker\'s eye.',
          },
        },
      },
    ],
    biggestMistake: {
      title: 'Skipping the third task component (encourage return)',
      body: 'The 2025 marking scheme requires all three components — outline tradition, challenge criticisms, encourage return. The third is most commonly skipped because students get into the rebuttal flow and forget to pivot to invitation. Missing it caps Purpose, which caps Coherence and Language under the P-caps-C-L rule. Plan in three blocks before writing: opening + tradition / point-by-point rebuttal / upcoming events + invitation.',
      source: { year: 2025, type: 'marking-scheme' },
    },
  },

  {
    id: 'english-2025-p1-composing-2',
    taskType: 'english-composition-speech',
    subject: 'english',
    year: 2025,
    paper: 'Paper 1',
    section: 'Section II — Composing',
    questionNumber: '2',
    level: 'higher',
    marks: 100,
    totalPaperMarks: 200,
    totalPaperMinutes: 170,
    commandWords: ['write a speech', 'for or against'],
    questionText: [
      {
        type: 'paragraph',
        content: [
          { text: "The theme of this examination, 'Perspectives', explores how we see things in different ways." },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'Write a speech', annotation: { note: 'Genre is FIXED. Must read like a SPOKEN speech — direct address, rhetorical devices, oral rhythm. Not an essay with quotes around it.', type: 'command' } },
          { text: ' ' },
          { text: 'for or against', annotation: { note: 'Pick ONE side. Hedging or arguing both sides equally is penalised under Purpose. Commit and defend.', type: 'keyword' } },
          { text: ' the motion that: "' },
          { text: 'Truth has become a valueless currency', annotation: { note: 'Engage with the metaphor — truth as something traded, devalued, debased. Don\'t just argue "is truth important?" — argue the specific currency framing.', type: 'keyword' } },
          { text: ' ' },
          { text: 'in today\'s world', annotation: { note: 'Contemporary references expected — fake news, AI deepfakes, social media, post-truth politics, recent named scandals or figures.', type: 'keyword' } },
          { text: '."  ' },
          { text: '(100)', annotation: { note: '100 marks → ~85 mins. The biggest single piece on Paper 1. P 30 / C 30 / L 30 / M 10.', type: 'marks-allocation' } },
        ],
      },
    ],
    predictPrompts: [
      {
        id: 'p1',
        type: 'multiple-choice',
        prompt: 'What is the required genre?',
        options: ['Personal essay', 'Speech', 'Discursive essay', 'Short story'],
        correctAnswer: 'Speech',
        debrief: {
          strategicPrinciple: 'Genre = speech. Must read as SPOKEN — direct address, rhetorical devices, oral rhythm. An essay with quotes around it caps Purpose because the genre is the frame for everything else.',
          commonWrongAnswer: {
            answer: 'Personal essay',
            reason: 'Personal essay sits with the reader silently. Speech projects to an audience — direct address, rhetorical questions, building rhythm. Wrong genre on a 100-mark Composition caps Purpose, which caps Coherence and Language under the P-caps-C-L rule.',
            source: { year: 2025, type: 'marking-scheme' },
          },
        },
      },
      {
        id: 'p2',
        type: 'multiple-choice',
        prompt: 'Which approach scores highest?',
        options: ['Argue both sides equally', 'Argue ONE side only and commit', 'Stay neutral', 'Mostly one side, slightly the other'],
        correctAnswer: 'Argue ONE side only and commit',
        debrief: {
          strategicPrinciple: '"For or against" = pick ONE. The 2025 indicative material rewards "focus on a speech for or against the motion" — hedging or arguing both sides equally is the discursive register, wrong for a debate motion. Commit and defend.',
          commonWrongAnswer: {
            answer: 'Argue both sides equally',
            reason: 'Hedging on a "for or against" motion is the discursive essay\'s job, not a speech for/against. Sitting on the fence caps Purpose because the genre demands a position — the speech is the act of persuasion, not a balanced survey.',
            source: { year: 2025, type: 'marking-scheme' },
          },
        },
      },
      {
        id: 'p3',
        type: 'short-text',
        prompt: 'Name two rhetorical devices a speech should use.',
        hint: 'Common ones: rhetorical question, anaphora (repetition), direct address, tricolon, anecdote, pathos, contrast.',
        debrief: {
          strategicPrinciple: 'Speech-genre features: rhetorical question, anaphora (repetition), direct address, tricolon (three-part lists), anecdote, contrast. The 2025 indicative material lists "rhetorical devices, anecdotes, imagery, emotive/inclusive language, audience awareness" — these are the load-bearing techniques.',
          commonWrongAnswer: {
            answer: 'Long sub-claused sentences',
            reason: 'Reads beautifully on the page but wouldn\'t survive a podium delivery. Speech needs oral rhythm — short punchy units, repetition, pauses for emphasis. Long sub-claused sentences are an essay technique, not a speech technique; the marker reading it will hear the absence of oral rhythm.',
            source: { year: 2025, type: 'marking-scheme' },
          },
        },
      },
      {
        id: 'p4',
        type: 'number',
        prompt: 'Roughly how many minutes should you spend on this?',
        correctAnswer: 85,
        debrief: {
          strategicPrinciple: '100 marks at 0.85 min/mark = 85 minutes — the largest single piece on Paper 1. Plan structure (8-10 mins) before the body. Three blocks: opening hook + stance / 3-4 developed arguments with contemporary evidence / memorable close.',
          commonWrongAnswer: {
            answer: '60',
            reason: 'Under-budgets the Composition. 100 marks deserves the time to plan structure, build the argument with named contemporary evidence, and close strong. 60 minutes leaves no room for the rhetorical scaffolding a speech needs and reads as rushed.',
          },
        },
      },
    ],
    biggestMistake: {
      title: 'Writing an essay rather than a speech',
      body: 'The 2025 marking scheme P descriptor rewards "a speech for or against the motion, effective use of speech-writing elements (rhetorical devices, anecdotes, imagery, emotive/inclusive language, audience awareness)". The most common 100-mark error is writing a discursive essay — beautiful prose with no audience, no oral rhythm, no direct address. Wrong genre caps Purpose, which caps Coherence and Language under the P-caps-C-L rule. Open with a hook addressed to the audience; use rhetorical questions and repetition; commit to one side; close memorably with the "currency" metaphor.',
      source: { year: 2025, type: 'marking-scheme' },
    },
  },

  {
    id: 'english-2025-p1-composing-3',
    taskType: 'english-composition-short-story',
    subject: 'english',
    year: 2025,
    paper: 'Paper 1',
    section: 'Section II — Composing',
    questionNumber: '3',
    level: 'higher',
    marks: 100,
    totalPaperMarks: 200,
    totalPaperMinutes: 170,
    commandWords: ['write a short story'],
    questionText: [
      {
        type: 'paragraph',
        content: [
          { text: "TEXT 1 analyses how the 'Underdog Effect' influences people's attitudes and behaviour." },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'Write a short story', annotation: { note: 'Genre is FIXED. Narrative — plot, character, setting, conflict, resolution. Not an essay reflecting on underdogs.', type: 'command' } },
          { text: ' in which a "' },
          { text: 'plucky chancer', annotation: { note: 'Your protagonist must be unmistakably this — scrappy underdog with nerve. SHOW it through action and dialogue, don\'t TELL it ("she was very plucky").', type: 'keyword' } },
          { text: '" ' },
          { text: 'challenges', annotation: { note: 'Conflict is REQUIRED. Needs an actual confrontation, contest, or pursuit — not just internal musing.', type: 'keyword' } },
          { text: ' a more ' },
          { text: 'privileged or established opponent', annotation: { note: 'Antagonist with structural advantages. Their power must be visible — name, position, social capital. Avoid mustache-twirling caricature.', type: 'keyword' } },
          { text: '. ' },
          { text: '(100)', annotation: { note: '100 marks → ~85 mins. P 30 / C 30 / L 30 / M 10. Plan structure (5 mins) before writing.', type: 'marks-allocation' } },
        ],
      },
    ],
    predictPrompts: [
      {
        id: 'p1',
        type: 'multiple-choice',
        prompt: 'What genre is required?',
        options: ['Personal essay', 'Short story', 'Speech', 'Feature article'],
        correctAnswer: 'Short story',
        debrief: {
          strategicPrinciple: 'Genre = short story — narrative with plot, character, setting, conflict, resolution. Not an essay reflecting on underdogs. The 2025 marking scheme P descriptor rewards "short story with plucky chancer challenging privileged opponent, effective use of narrative shape".',
          commonWrongAnswer: {
            answer: 'Personal essay',
            reason: 'Personal essay reflects on a theme; short story shows characters acting out the theme. Wrong genre on a 100-mark Composition caps Purpose, which caps Coherence and Language. The marker is looking for narrative craft, not reflection.',
            source: { year: 2025, type: 'marking-scheme' },
          },
        },
      },
      {
        id: 'p2',
        type: 'multiple-choice',
        prompt: 'Which structural element is required?',
        options: ['Bibliography', 'Conflict between protagonist and opponent', 'Statistics', 'Counter-argument'],
        correctAnswer: 'Conflict between protagonist and opponent',
        debrief: {
          strategicPrinciple: 'Conflict between protagonist and opponent is required — the question specifies "challenges a more privileged or established opponent". The story needs a real confrontation, contest, or pursuit; internal musing alone doesn\'t satisfy "challenges".',
          commonWrongAnswer: {
            answer: 'Bibliography',
            reason: 'Confuses creative writing with academic writing. Short stories don\'t take bibliographies — they take characters, settings, scenes. Picking this option shows the prompt hasn\'t been parsed at all.',
            source: { year: 2025, type: 'marking-scheme' },
          },
        },
      },
      {
        id: 'p3',
        type: 'short-text',
        prompt: 'Name two short-story craft elements you would use.',
        hint: 'Setting, dialogue, tension, characterisation, atmosphere, narrative voice, resolution, sensory detail.',
        debrief: {
          strategicPrinciple: 'Short-story craft = setting, dialogue, tension, characterisation, atmosphere, narrative voice, sensory detail, resolution. The 2025 indicative material lists these explicitly — they\'re the load-bearing techniques the marker scans for.',
          commonWrongAnswer: {
            answer: 'Statistics',
            reason: 'Article technique, not story technique. Short stories use sensory detail, dialogue, atmosphere — not citations or statistics. Using essay/article techniques in a story task is genre confusion that caps Purpose.',
            source: { year: 2025, type: 'marking-scheme' },
          },
        },
      },
      {
        id: 'p4',
        type: 'multiple-choice',
        prompt: 'The opponent should be...',
        options: ['Equally matched', 'Younger and weaker', 'Privileged or established', 'Off-page entirely'],
        correctAnswer: 'Privileged or established',
        debrief: {
          strategicPrinciple: 'Opponent must be privileged or established — the question specifies this directly. The contrast between the underdog protagonist and the structurally advantaged opponent IS the engine of the story. Equally-matched or weaker opponents don\'t fit the prompt.',
          commonWrongAnswer: {
            answer: 'Equally matched',
            reason: 'Loses the underdog dynamic the question is built around. "A plucky chancer challenges a more privileged or established opponent" requires structural inequality — name, position, social capital on the antagonist\'s side. Equally-matched opponents make the protagonist a competitor, not an underdog.',
            source: { year: 2025, type: 'marking-scheme' },
          },
        },
      },
    ],
    biggestMistake: {
      title: 'Writing an essay about underdogs instead of a story featuring one',
      body: 'The 2025 marking scheme P descriptor explicitly rewards "short story with plucky chancer challenging privileged opponent, effective use of narrative shape, setting, plot, characterisation, dialogue, tension, narrative voice, resolution". Discursive essays about why underdogs matter (or about Text 1\'s argument) are wrong genre — Purpose cap, with C and L capped behind it. Show the chancer in action through scenes, dialogue, sensory detail; show the opponent\'s structural advantages through specifics (name, position, social capital); resolve through a contest or confrontation — the chancer doesn\'t have to win.',
      source: { year: 2025, type: 'marking-scheme' },
    },
  },

  // ────────────────────────────────────────────────────────────────────
  // 2024 Paper 1 (Higher Level) — theme: Connections
  // Source: SEC paper + marking scheme.
  // ────────────────────────────────────────────────────────────────────

  {
    id: 'english-2024-p1-text1-qa-i',
    taskType: 'english-comprehension-insight',
    subject: 'english',
    year: 2024,
    paper: 'Paper 1',
    section: "Section I — Comprehending — Text 1 (Family Connections and the Natural World — Fintan O'Toole) Question A",
    questionNumber: '(i)',
    level: 'higher',
    marks: 15,
    totalPaperMarks: 200,
    totalPaperMinutes: 170,
    commandWords: ['What does the writer reveal'],
    questionText: [
      {
        type: 'paragraph',
        content: [
          { text: 'What, in your opinion, ' },
          { text: 'does the writer reveal', annotation: { type: 'command', note: '"Reveal" = the question is comprehension-of-text plus inference. Not asking for your views on family — asking what the writer SHOWS US through the article. Anchor every point in something specific in the passage.' } },
          { text: ' about ' },
          { text: 'the nature of family relationships', annotation: { type: 'keyword', note: 'Anchor concept. Each of your three points should be a different facet of "family relationships" the writer reveals — not three variations on "family is important".' } },
          { text: ' in TEXT 1? ' },
          { text: 'Make three points', annotation: { type: 'keyword', note: "THREE is enforced. Two points won't hit the mark band. Four points dilute. Make three discrete, well-developed points — not overlapping rephrasings." } },
          { text: ', ' },
          { text: 'supporting your response with reference to the text', annotation: { type: 'trap', note: 'Marking scheme: "Responses should be supported with reference to Text 1." Pure personal views with no textual anchor caps you in the lower bands. Quote or paraphrase a specific moment for each of your three points.' } },
          { text: '. ' },
          { text: '(15)', annotation: { type: 'marks-allocation', note: 'Marked ex 15 against the criteria (P/C/L/M). H1 band: 15-14. H4 (mid-band): 11. Indicative material: generational differences; genetic/environmental/historical connections; values/beliefs/interests shaping relationships; memories and bonds; the power of memory.' } },
        ],
      },
    ],
    predictPrompts: [
      {
        id: 'q1ai-three',
        type: 'multiple-choice',
        prompt: 'How many points does this question want?',
        options: ['Two', 'Three', 'Four', 'As many as you can think of'],
        correctAnswer: 'Three',
        debrief: {
          strategicPrinciple: 'Three is the enforced count — two falls short of the band, four-plus dilutes. Three discrete points, each from a different facet of family relationships the writer reveals, lands the H1 band.',
          commonWrongAnswer: {
            answer: 'As many as you can think of',
            reason: 'More is not better. The 2024 marking scheme rewards quality of points over volume. Listing five thin points reads as scatter-gun and ends up below H1; three well-developed points (one anchored moment each, one inferred insight each) lands the band.',
            source: { year: 2024, type: 'marking-scheme' },
          },
        },
      },
      {
        id: 'q1ai-where',
        type: 'multiple-choice',
        prompt: 'Where must your evidence come from?',
        options: ['Your own family experience', 'The text only', 'Other texts on the paper', 'A mix is fine but each point needs textual reference'],
        correctAnswer: 'A mix is fine but each point needs textual reference',
        debrief: {
          strategicPrinciple: 'A(i) is "what the writer reveals" — anchored in the text. The 2024 marking scheme states: "Responses should be supported with reference to Text 1." Personal experience can supplement, but each point needs a specific textual moment as its anchor.',
          commonWrongAnswer: {
            answer: 'Your own family experience',
            reason: 'Confuses A(i) (what the writer reveals — text-anchored comprehension/inference) with A(ii) (your own views — broader scope). Personal experience alone on A(i) misses the comprehension dimension and caps the answer in the lower bands per the marking scheme.',
            source: { year: 2024, type: 'marking-scheme' },
          },
        },
      },
      {
        id: 'q1ai-moment',
        type: 'short-text',
        prompt: 'Name one specific moment in the text that reveals something about family relationships.',
        hint: 'The waxwing tattoo, the bus trip to Ballsbridge, the pallid swift in the museum, the four-year-old grandson…',
        debrief: {
          strategicPrinciple: 'Each of the three points needs a specific textual moment as its anchor — the waxwing tattoo, the bus trip to Ballsbridge, the pallid swift, the four-year-old grandson. Generic "family is important" without naming what the writer reveals reads as paraphrase, not insight.',
          commonWrongAnswer: {
            answer: 'Family is mentioned several times in the text',
            reason: 'Vague reference without naming the specific moment or quoting the writer\'s framing. The 2024 marking scheme requires "support with reference to Text 1" — each point needs a moment (the waxwing tattoo, the bus trip, the grandson\'s indifference) quoted or paraphrased with enough specificity for the marker to recognise it.',
            source: { year: 2024, type: 'marking-scheme' },
          },
        },
      },
    ],
    biggestMistake: {
      title: "Personal opinions about family instead of what the writer reveals",
      body: 'The 2024 marking scheme states: "Responses should be supported with reference to Text 1." A(i) is comprehension-plus-inference, not personal reflection. Three points, each anchored in a specific textual moment (the waxwing tattoo, the bus trip, the grandson, the writer\'s own self-aware "ego thing"), each surfacing a different facet of family relationships (generational transmission, shared experience, inherited values). Three variations on "family is important" reads as one point repeated.',
      source: { year: 2024, type: 'marking-scheme' },
    },
  },

  {
    id: 'english-2024-p1-text1-qa-ii',
    taskType: 'english-personal-views',
    subject: 'english',
    year: 2024,
    paper: 'Paper 1',
    section: "Section I — Comprehending — Text 1 (Family Connections and the Natural World — Fintan O'Toole) Question A",
    questionNumber: '(ii)',
    level: 'higher',
    marks: 15,
    totalPaperMarks: 200,
    totalPaperMinutes: 170,
    commandWords: ['Why do you think', 'Develop three points'],
    questionText: [
      {
        type: 'paragraph',
        content: [
          { text: "The writer in TEXT 1 tells us that some parents don't like the idea of their children getting tattoos. " },
          { text: 'Why do you think', annotation: { type: 'command', note: 'PERSONAL VIEWS task — not comprehension. Marking scheme: "Candidates may draw deductions from the text and/or from their own views and experience." This is the structural opposite of A(i). A(i) wants what the writer reveals; A(ii) wants what YOU think.' } },
          { text: " that some parents don't like the idea of their children getting tattoos? " },
          { text: 'Develop three points', annotation: { type: 'keyword', note: "\"Develop\" is the load-bearing word. Listing three reasons in single sentences won't cut it — each point needs to be EXTENDED. Reasoning, example, consequence, contrast. A developed point is a paragraph, not a sentence." } },
          { text: ' in your response. ' },
          { text: '(15)', annotation: { type: 'marks-allocation', note: 'Marked ex 15 against the criteria. H1 band: 15-14. Pay attention to the QUALITY of the points (marking scheme) — quality > quantity. A well-developed three is worth more than a thin five.' } },
        ],
      },
    ],
    predictPrompts: [
      {
        id: 'q1aii-vs-i',
        type: 'multiple-choice',
        prompt: 'How is A(ii) different from A(i)?',
        options: [
          'No difference — both want textual reference',
          'A(i) = what the writer reveals; A(ii) = your own views (text and/or experience)',
          'A(ii) is shorter',
          'A(ii) wants a counter-argument',
        ],
        correctAnswer: 'A(i) = what the writer reveals; A(ii) = your own views (text and/or experience)',
        debrief: {
          strategicPrinciple: 'A(i) and A(ii) are structurally opposite. A(i) = comprehension-anchored ("what the writer reveals" — text-only). A(ii) = personal-reasoning-anchored ("your own views" — text and/or experience). The 2024 marking scheme states A(ii) candidates "may draw deductions from the text and/or from their own views and experience".',
          commonWrongAnswer: {
            answer: 'No difference — both want textual reference',
            reason: 'Conflating the two tasks means either over-anchoring A(ii) in the text (missing the personal-views dimension) or under-anchoring A(i) in the text (failing the comprehension dimension). The 2024 marking scheme treats them as distinct tasks with different evidence demands.',
            source: { year: 2024, type: 'marking-scheme' },
          },
        },
      },
      {
        id: 'q1aii-develop',
        type: 'multiple-choice',
        prompt: 'What does "develop" mean in this question?',
        options: [
          'List three short reasons',
          'Extend each reason — reasoning, example, consequence — paragraph not sentence',
          'Develop one reason in great detail',
          'Build it gradually like a story',
        ],
        correctAnswer: 'Extend each reason — reasoning, example, consequence — paragraph not sentence',
        debrief: {
          strategicPrinciple: '"Develop" = extend each reason with reasoning + example + consequence. Paragraph, not sentence. The 2024 marking scheme rewards quality of points; a single sentence reads as listing, not developing, and caps you below H1.',
          commonWrongAnswer: {
            answer: 'List three short reasons',
            reason: 'Listing three short reasons is exactly what "develop" rules out. The marking scheme\'s quality criterion rewards extension — each point needs reasoning, example or illustration, and an implication or consequence. Single sentences read as listing.',
            source: { year: 2024, type: 'marking-scheme' },
          },
        },
      },
      {
        id: 'q1aii-reasons',
        type: 'short-text',
        prompt: "Name two reasons parents might dislike tattoos that you'd actually develop in the answer.",
        hint: 'The writer hints at one ("the flesh of our flesh should remain spotless" — ego/possessiveness). Others: permanence, judgement of others, religious/cultural views, employment concerns, parental control.',
        debrief: {
          strategicPrinciple: 'Three DIFFERENT reasons (not three rephrasings). The writer\'s own "ego thing" is one angle. Permanence and regret is a second. Social/professional consequences is a third. Each different reason opens a different developed paragraph.',
          commonWrongAnswer: {
            answer: 'Parents are old-fashioned / parents don\'t understand / parents are stuck in their ways',
            reason: 'Three variations on the same core idea collapse to one developed point. The 2024 marking scheme rewards distinct angles — generational ego, permanence and regret, professional consequences, religious/cultural objection — not rephrasings of the same thought.',
            source: { year: 2024, type: 'marking-scheme' },
          },
        },
      },
    ],
    biggestMistake: {
      title: 'Listing five short reasons instead of developing three',
      body: 'The 2024 marking scheme rewards quality of points over volume. The instruction "Develop three points" is doing real work — each point should be a paragraph: reasoning, example or illustration, consequence. Listing five thin reasons or three single-sentence reasons reads as quantity-over-quality and caps below H1. Pick three different angles (ego, permanence, consequences) and extend each one with the texture a paragraph needs.',
      source: { year: 2024, type: 'marking-scheme' },
    },
  },

  {
    id: 'english-2024-p1-text2-qb',
    taskType: 'english-composition-genre-task',
    subject: 'english',
    year: 2024,
    paper: 'Paper 1',
    section: 'Section I — Comprehending — Text 2 (Friendship — The Bee Sting, Paul Murray) Question B',
    questionNumber: 'B',
    level: 'higher',
    marks: 50,
    totalPaperMarks: 200,
    totalPaperMinutes: 170,
    commandWords: ['Write a proposal', 'outline', 'propose', 'suggest'],
    questionText: [
      {
        type: 'paragraph',
        content: [
          { text: 'Certain aspects of the area where you live have become run down and neglected. ' },
          { text: 'Write a proposal', annotation: { type: 'command', note: "GENRE PRESCRIBED — proposal, not letter, not article, not essay. Distinct features: structured headings or clearly-marked sections; formal civic register; addressed to a body, not an individual; combines analysis (what's wrong) with action (what to do)." } },
          { text: ' to your local ' },
          { text: 'Tidy Towns Committee', annotation: { type: 'keyword', note: 'AUDIENCE — a formal civic committee of mostly older volunteers. Register: respectful, evidence-based, constructive. NOT teen voice, NOT casual, NOT ranty. The audience matters as much as the genre — a brilliant proposal in the wrong register caps Purpose.' } },
          { text: ' in which you: ' },
          { text: 'outline your key concerns', annotation: { type: 'command', note: 'TASK COMPONENT 1 of 3. You MUST address this. Be specific — name actual problems (litter on a named road, dilapidated playground, derelict shop fronts). Vague "the area is run-down" caps Purpose.' } },
          { text: ' in relation to the problems you have identified, ' },
          { text: 'propose a project', annotation: { type: 'command', note: 'TASK COMPONENT 2 of 3. A specific, actionable project — not three competing ideas. Name it, scope it, say roughly what it costs in time/money/volunteers. Concrete > vague.' } },
          { text: ' that you believe would improve the situation, and ' },
          { text: 'suggest how the committee could encourage', annotation: { type: 'trap', note: 'TASK COMPONENT 3 of 3 — most commonly skipped. Marking scheme P descriptor: "outline their key concerns... propose a project... suggest how the committee could encourage more members of the local community". Skip this and your Purpose mark is capped, which CAPS your Coherence and Language marks too (P caps C and L).' } },
          { text: ' more members of the local community to become active in improving the local area. ' },
          { text: '(50)', annotation: { type: 'marks-allocation', note: 'P 15 / C 15 / L 15 / M 5. CRUCIAL RULE: P caps C and L — your Coherence and Language marks cannot exceed your Purpose mark. Brilliant prose on the wrong genre or missing a sub-task is capped at the level of Purpose. ~43 mins.' } },
        ],
      },
    ],
    predictPrompts: [
      {
        id: 'q2b-genre',
        type: 'multiple-choice',
        prompt: 'What genre is required?',
        options: ['Personal letter', 'Newspaper article', 'Formal proposal to a committee', 'Speech'],
        correctAnswer: 'Formal proposal to a committee',
        debrief: {
          strategicPrinciple: 'Genre = formal proposal to a committee. Headed sections OK, formal civic register, evidence-based, constructive. NOT personal letter (private), NOT newspaper article (broadcast), NOT speech (oral). The 2024 marking scheme P descriptor specifies "proposal".',
          commonWrongAnswer: {
            answer: 'Personal letter',
            reason: 'Personal letter is one-to-one and private; the question requires a proposal addressed to a civic body — a document the committee will read and discuss together. Wrong genre on a 50-mark Question B caps Purpose, which caps Coherence and Language.',
            source: { year: 2024, type: 'marking-scheme' },
          },
        },
      },
      {
        id: 'q2b-three',
        type: 'multiple-choice',
        prompt: 'How many distinct task components must your proposal address?',
        options: ['One', 'Two', 'Three', 'As many as you have ideas for'],
        correctAnswer: 'Three',
        debrief: {
          strategicPrinciple: 'Three components required: (1) outline key concerns, (2) propose a project, (3) suggest how the committee could encourage more community involvement. The 2024 marking scheme P descriptor names all three explicitly. Missing one caps Purpose.',
          commonWrongAnswer: {
            answer: 'Two',
            reason: 'Addressing only two components — almost always the third (community engagement) is the one skipped because students get into the project-pitch flow. Missing component caps Purpose, which caps Coherence and Language under the P-caps-C-L rule.',
            source: { year: 2024, type: 'marking-scheme' },
          },
        },
      },
      {
        id: 'q2b-pcaps',
        type: 'multiple-choice',
        prompt: "Your prose is brilliant but you skip the third sub-task. What's the ceiling on your Coherence and Language marks?",
        options: [
          "No effect — they're marked separately",
          'Capped at the level of your Purpose mark (P caps C and L)',
          'Capped at half',
          'Only Purpose suffers',
        ],
        correctAnswer: 'Capped at the level of your Purpose mark (P caps C and L)',
        debrief: {
          strategicPrinciple: 'P caps C and L in English marking. Brilliant prose on the wrong genre or missing a sub-task is capped at the level of your Purpose mark. The 2024 marking scheme makes Purpose load-bearing — every other dimension ceilings at it.',
          commonWrongAnswer: {
            answer: "No effect — they're marked separately",
            reason: 'Misunderstands the P-caps-C-L rule. P, C, L are NOT independent — your Coherence and Language marks cannot exceed your Purpose mark. Skipping the third sub-task drops Purpose, which then ceilings the other two regardless of how well the prose is written.',
            source: { year: 2024, type: 'marking-scheme' },
          },
        },
      },
      {
        id: 'q2b-time',
        type: 'number',
        prompt: 'Roughly how many minutes should you spend?',
        correctAnswer: 43,
        debrief: {
          strategicPrinciple: '50 marks at 0.85 min/mark (170 min / 200 marks) = ~43 minutes — a quarter of the paper. Plan three components (5 min) before writing the body.',
          commonWrongAnswer: {
            answer: '30',
            reason: 'Under-budgets the question. 30 minutes for a 50-mark Question B leaves no room for planning the three components or for the proposal-specific structural moves (headed sections, civic register, evidence). Reads as rushed under the marker\'s eye.',
          },
        },
      },
    ],
    biggestMistake: {
      title: 'Skipping the third task component — community engagement',
      body: 'The 2024 marking scheme requires all three components: outline key concerns, propose a project, suggest how the committee could encourage more community involvement. The third is most commonly skipped because students get into the project-pitch flow. Missing it caps Purpose, which caps Coherence and Language under the P-caps-C-L rule. Plan in three blocks before writing: opening + concerns / one named project (who, what, when, rough cost) / community engagement mechanisms (schools, social media, TY hours, GAA tie-ups, business sponsorship).',
      source: { year: 2024, type: 'marking-scheme' },
    },
  },

  {
    id: 'english-2024-p1-composing-5',
    taskType: 'english-composition-discursive',
    subject: 'english',
    year: 2024,
    paper: 'Paper 1',
    section: 'Section II — Composing',
    questionNumber: '5',
    level: 'higher',
    marks: 100,
    totalPaperMarks: 200,
    totalPaperMinutes: 170,
    commandWords: ['Write a discursive essay', 'consider'],
    questionText: [
      {
        type: 'paragraph',
        content: [
          { text: 'The writer in TEXT 3 regrets losing her anonymity by engaging with social media.' },
        ],
      },
      {
        type: 'paragraph',
        content: [
          { text: 'Write a discursive essay', annotation: { type: 'command', note: 'GENRE PRESCRIBED — discursive, NOT argumentative or persuasive. A discursive essay considers MULTIPLE views, weighs evidence, and arrives at a considered position. It is not a speech for one side. Picking one side and arguing it is the most common genre error and caps Purpose.' } },
          { text: ' in which you ' },
          { text: 'consider', annotation: { type: 'keyword', note: '"Consider" reinforces discursive register. Weighing, balancing, examining from multiple angles — not advocating. Marking scheme indicative material includes "arguments and counter-arguments, consideration of a variety of views".' } },
          { text: ' ' },
          { text: 'whether or not it is possible, or even desirable, to maintain privacy', annotation: { type: 'trap', note: 'TWO QUESTIONS in one — possible AND desirable. They are NOT the same. (a) Is it technically possible to be private in 2024? (b) Even if it were, would we want to be? Engaging with only one half caps Purpose. Strong essays interrogate both and may conclude the two halves diverge.' } },
          { text: ' ' },
          { text: "in today's world", annotation: { type: 'keyword', note: 'CONTEMPORARY references expected — not abstract philosophy. Named platforms (Meta, TikTok, X), named technologies (AI, facial recognition, location data), named scandals (Cambridge Analytica, Pegasus, data breaches), named figures or cases. "Today\'s world" is doing work in the prompt.' } },
          { text: '. ' },
          { text: '(100)', annotation: { type: 'marks-allocation', note: 'P 30 / C 30 / L 30 / M 10. ~85 mins — the largest single piece on Paper 1. P CAPS C AND L: brilliant writing in the wrong genre (e.g. an argumentative essay, a personal essay) is capped at the level of your Purpose mark. Get the genre right first, then dazzle.' } },
        ],
      },
    ],
    predictPrompts: [
      {
        id: 'comp5-genre',
        type: 'multiple-choice',
        prompt: 'A "discursive" essay differs from "argumentative" how?',
        options: [
          'No difference — both argue a side',
          'Discursive considers multiple views and weighs them; argumentative picks one and defends it',
          'Discursive is shorter',
          'Discursive avoids personal opinion',
        ],
        correctAnswer: 'Discursive considers multiple views and weighs them; argumentative picks one and defends it',
        debrief: {
          strategicPrinciple: 'Discursive = considers multiple views and weighs them. Argumentative = picks one and defends it. The 2024 marking scheme indicative material requires "arguments and counter-arguments, consideration of a variety of views" — picking one side is wrong genre and caps Purpose.',
          commonWrongAnswer: {
            answer: 'No difference — both argue a side',
            reason: 'Conflates the two genres. Discursive essays weigh perspectives; argumentative essays advocate. The 2024 marking scheme rewards "consideration of a variety of views" on discursive prompts — picking one side and defending it is the argumentative shape and caps Purpose on this question.',
            source: { year: 2024, type: 'marking-scheme' },
          },
        },
      },
      {
        id: 'comp5-twohalves',
        type: 'multiple-choice',
        prompt: "Which of the prompt's halves do you have to engage with?",
        options: [
          'Just whether privacy is possible',
          'Just whether privacy is desirable',
          'Both — "possible" AND "desirable" are separate questions',
          'Either one is fine',
        ],
        correctAnswer: 'Both — "possible" AND "desirable" are separate questions',
        debrief: {
          strategicPrinciple: 'The prompt asks "whether or not it is possible, OR even desirable" — TWO questions. (a) Can privacy be maintained technically? (b) Even if it could, would we want to? Strong essays interrogate both and may conclude they diverge. Engaging with only one half caps Purpose.',
          commonWrongAnswer: {
            answer: 'Just whether privacy is possible',
            reason: 'Misses half the prompt. The "or even desirable" phrasing makes these distinct questions — possible (technical) is not the same as desirable (normative). Engaging with only one half caps Purpose because the answer addresses only half the prompt.',
            source: { year: 2024, type: 'marking-scheme' },
          },
        },
      },
      {
        id: 'comp5-pcaps',
        type: 'multiple-choice',
        prompt: 'You write a beautiful argumentative essay (one side, well-defended). Genre is wrong. What happens to your max C and L marks?',
        options: [
          'Unaffected — only Purpose drops',
          "They're capped at your Purpose mark (P caps C and L)",
          'You lose 10%',
          'Examiner reclassifies it',
        ],
        correctAnswer: "They're capped at your Purpose mark (P caps C and L)",
        debrief: {
          strategicPrinciple: 'Wrong genre caps Purpose, which caps Coherence and Language. A beautifully argued argumentative essay on a discursive prompt has its C and L marks ceilinged at its (low) Purpose mark. Get the genre right first, then dazzle.',
          commonWrongAnswer: {
            answer: 'Unaffected — only Purpose drops',
            reason: 'Misunderstands the P-caps-C-L rule. Wrong genre is a Purpose failure; Purpose then ceilings Coherence and Language regardless of how well written the wrong-genre essay is. The cap is structural, not punitive.',
            source: { year: 2024, type: 'marking-scheme' },
          },
        },
      },
      {
        id: 'comp5-references',
        type: 'short-text',
        prompt: 'Name three contemporary references (platforms, scandals, technologies, figures) you\'d use to ground "today\'s world".',
        hint: "Cambridge Analytica, GDPR, Edward Snowden, TikTok minor-data investigations, AI deepfakes, Apple's privacy-vs-FBI cases, Clearview AI, Pegasus spyware, Meta Pixel litigation, the right-to-be-forgotten EU rulings…",
        debrief: {
          strategicPrinciple: 'Contemporary, specific references ground "today\'s world" — Cambridge Analytica, GDPR, Snowden, AI deepfakes, the Apple-FBI case, the right-to-be-forgotten rulings, smart-home device data flows, Pegasus spyware. Generic "the modern world is bad for privacy" without named platforms or scandals reads as abstract and weakens Purpose.',
          commonWrongAnswer: {
            answer: 'The internet has changed things',
            reason: 'Generic abstraction without specifics. The prompt says "in today\'s world" — markers expect named platforms, named scandals, named technologies, named cases. Vague references don\'t trigger the "contemporary" weight the prompt asks for.',
            source: { year: 2024, type: 'marking-scheme' },
          },
        },
      },
      {
        id: 'comp5-time',
        type: 'number',
        prompt: 'Roughly how many minutes should you spend?',
        correctAnswer: 85,
        debrief: {
          strategicPrinciple: '100 marks at 0.85 min/mark = 85 minutes — the largest single piece on Paper 1. Plan structure (8-10 mins) before the body to balance the two halves and weave in contemporary references.',
          commonWrongAnswer: {
            answer: '60',
            reason: 'Under-budgets the Composition. 100 marks deserves the time to plan the two-halves structure, build counter-arguments, weave in named contemporary evidence, and resolve thoughtfully. 60 minutes reads as rushed under the marker\'s eye.',
          },
        },
      },
    ],
    biggestMistake: {
      title: 'Writing an argumentative essay on a discursive prompt',
      body: 'The most common 100-mark error on this kind of question is genre confusion — students pick one side (privacy is dead / privacy still matters) and defend it brilliantly. The 2024 marking scheme indicative material requires "arguments and counter-arguments, consideration of a variety of views, opinions and personal experiences, illustrations, allusions, analysis" — discursive register, not argumentative. Wrong genre caps Purpose, which caps Coherence and Language under P-caps-C-L. Author with weighing language ("on one hand", "however", "yet it could equally be argued"); steel-man the opposite of your emerging view at least once; close with a qualified conclusion that distils where the weighing has led.',
      source: { year: 2024, type: 'marking-scheme' },
    },
  },
];
