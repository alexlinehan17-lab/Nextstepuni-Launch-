/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Leaving Cert curriculum taxonomy — every examined subject → levels →
 * strands → sub-topics, from the official syllabi (currently-examined spec).
 * Sub-topic names are shortened for the picker; the full syllabus detail lives
 * in the source specs. ⚠️ Re-verify periodically.
 */
export type CurriculumLevel = 'higher' | 'ordinary' | 'foundation' | 'common';
export type CurriculumCategory = 'language' | 'stem' | 'business' | 'social-environmental' | 'practical-applied' | 'arts' | 'other';
export interface CurriculumSubtopic { id: string; name: string }
export interface CurriculumStrand { id: string; name: string; subtopics: CurriculumSubtopic[] }
export interface CurriculumSubject { id: string; name: string; category: CurriculumCategory; levels: CurriculumLevel[]; strands: CurriculumStrand[] }

export const CURRICULUM: CurriculumSubject[] = [
  {
    "id": "irish",
    "name": "Irish (Gaeilge)",
    "category": "language",
    "levels": [
      "higher",
      "ordinary",
      "foundation"
    ],
    "strands": [
      {
        "id": "irish-0",
        "name": "An Bhéaltriail (Oral Examination — 40%)",
        "subtopics": [
          {
            "id": "irish-0-0",
            "name": "Fáiltiú / Beannú"
          },
          {
            "id": "irish-0-1",
            "name": "Aithris Filíochta"
          },
          {
            "id": "irish-0-2",
            "name": "Sraith Pictiúr"
          },
          {
            "id": "irish-0-3",
            "name": "Comhrá / Agallamh"
          },
          {
            "id": "irish-0-4",
            "name": "Saibhreas, cruinneas agus líofacht"
          },
          {
            "id": "irish-0-5",
            "name": "Foghraíocht agus blas"
          }
        ]
      },
      {
        "id": "irish-1",
        "name": "An Chluastuiscint (Aural / Listening Comprehension — Paper 1, 60 marks)",
        "subtopics": [
          {
            "id": "irish-1-0",
            "name": "Cuid A — Fógraí"
          },
          {
            "id": "irish-1-1",
            "name": "Cuid B — Comhráite"
          },
          {
            "id": "irish-1-2",
            "name": "Cuid C — Píosaí Nuachta"
          },
          {
            "id": "irish-1-3",
            "name": "Tuiscint éisteachta"
          }
        ]
      },
      {
        "id": "irish-2",
        "name": "An Cheapadóireacht (Composition / Written Production — Paper 1, 100 marks)",
        "subtopics": [
          {
            "id": "irish-2-0",
            "name": "Aiste"
          },
          {
            "id": "irish-2-1",
            "name": "Alt Nuachtáin / Irise"
          },
          {
            "id": "irish-2-2",
            "name": "Blag (Blog post)"
          },
          {
            "id": "irish-2-3",
            "name": "Scéal"
          },
          {
            "id": "irish-2-4",
            "name": "Díospóireacht"
          },
          {
            "id": "irish-2-5",
            "name": "Óráid"
          },
          {
            "id": "irish-2-6",
            "name": "Giota leanúnach"
          },
          {
            "id": "irish-2-7",
            "name": "Saibhreas na Gaeilge"
          }
        ]
      },
      {
        "id": "irish-3",
        "name": "An Léamhthuiscint (Reading Comprehension — Paper 2, ~100 marks)",
        "subtopics": [
          {
            "id": "irish-3-0",
            "name": "Léamhthuiscint A"
          },
          {
            "id": "irish-3-1",
            "name": "Léamhthuiscint B"
          },
          {
            "id": "irish-3-2",
            "name": "Ceisteanna tuisceana"
          },
          {
            "id": "irish-3-3",
            "name": "Ceist ghramadaí / teanga"
          }
        ]
      },
      {
        "id": "irish-4",
        "name": "An Prós (Prose — Paper 2; named & optional, Higher & Ordinary)",
        "subtopics": [
          {
            "id": "irish-4-0",
            "name": "Prós Comónta Ainmnithe"
          },
          {
            "id": "irish-4-1",
            "name": "Oisín i dTír na nÓg"
          },
          {
            "id": "irish-4-2",
            "name": "An Gnáthrud"
          },
          {
            "id": "irish-4-3",
            "name": "Seal i Neipeal"
          },
          {
            "id": "irish-4-4",
            "name": "Dís"
          },
          {
            "id": "irish-4-5",
            "name": "Hurlamaboc"
          },
          {
            "id": "irish-4-6",
            "name": "Cáca Milis (gearrscannán) nó An Lasair Choille"
          },
          {
            "id": "irish-4-7",
            "name": "Prós: Ábhar Roghnach"
          }
        ]
      },
      {
        "id": "irish-5",
        "name": "An Fhilíocht (Poetry — Paper 2; named & optional, Higher & Ordinary)",
        "subtopics": [
          {
            "id": "irish-5-0",
            "name": "Filíocht Chomónta Ainmnithe"
          },
          {
            "id": "irish-5-1",
            "name": "An Spailpín Fánach"
          },
          {
            "id": "irish-5-2",
            "name": "Géibheann"
          },
          {
            "id": "irish-5-3",
            "name": "An tEarrach Thiar"
          },
          {
            "id": "irish-5-4",
            "name": "Mo Ghrá-sa (idir lúibíní)"
          },
          {
            "id": "irish-5-5",
            "name": "Colscaradh"
          },
          {
            "id": "irish-5-6",
            "name": "Filíocht: Ábhar Roghnach"
          }
        ]
      },
      {
        "id": "irish-6",
        "name": "Litríocht Bhreise — Ardleibhéal (Additional Literature — Higher Level only)",
        "subtopics": [
          {
            "id": "irish-6-0",
            "name": "Prós Breise — An Triail [go huile]"
          },
          {
            "id": "irish-6-1",
            "name": "Prós Breise — A Thig Ná Tit Orm"
          },
          {
            "id": "irish-6-2",
            "name": "Prós Breise — Tóraíocht Dhiarmada agus Ghráinne"
          },
          {
            "id": "irish-6-3",
            "name": "Prós Breise — Gafa"
          },
          {
            "id": "irish-6-4",
            "name": "Prós Breise — Canary Wharf"
          },
          {
            "id": "irish-6-5",
            "name": "Dánta Breise"
          },
          {
            "id": "irish-6-6",
            "name": "Caoineadh Airt Uí Laoghaire"
          },
          {
            "id": "irish-6-7",
            "name": "Fill Arís"
          },
          {
            "id": "irish-6-8",
            "name": "A Chlann"
          },
          {
            "id": "irish-6-9",
            "name": "Colmáin"
          },
          {
            "id": "irish-6-10",
            "name": "Éiceolaí"
          }
        ]
      },
      {
        "id": "irish-7",
        "name": "Stair Litríocht na Gaeilge / Ábhar Cúlra (Background — Higher Level)",
        "subtopics": [
          {
            "id": "irish-7-0",
            "name": "Stair Litríocht na Gaeilge"
          },
          {
            "id": "irish-7-1",
            "name": "Comhthéacs agus téamaí na dtéacsanna"
          }
        ]
      },
      {
        "id": "irish-8",
        "name": "Scileanna Teanga / Gramadach (Underlying Language Skills)",
        "subtopics": [
          {
            "id": "irish-8-0",
            "name": "An Tuiscint"
          },
          {
            "id": "irish-8-1",
            "name": "An Labhairt"
          },
          {
            "id": "irish-8-2",
            "name": "An Scríobh"
          },
          {
            "id": "irish-8-3",
            "name": "An Léitheoireacht (Reading)"
          },
          {
            "id": "irish-8-4",
            "name": "Gramadach"
          },
          {
            "id": "irish-8-5",
            "name": "Stór focal agus nathanna"
          }
        ]
      }
    ]
  },
  {
    "id": "english",
    "name": "English",
    "category": "language",
    "levels": [
      "higher",
      "ordinary"
    ],
    "strands": [
      {
        "id": "english-0",
        "name": "Domains: Comprehending and Composing",
        "subtopics": [
          {
            "id": "english-0-0",
            "name": "Comprehending"
          },
          {
            "id": "english-0-1",
            "name": "Composing"
          },
          {
            "id": "english-0-2",
            "name": "Shaping experience through style, genre and context"
          },
          {
            "id": "english-0-3",
            "name": "Texts and genres"
          },
          {
            "id": "english-0-4",
            "name": "Oracy"
          }
        ]
      },
      {
        "id": "english-1",
        "name": "The Language of Information",
        "subtopics": [
          {
            "id": "english-1-0",
            "name": "Information texts"
          },
          {
            "id": "english-1-1",
            "name": "Comprehending: Give the gist of a text; specify…"
          },
          {
            "id": "english-1-2",
            "name": "Comprehending: Summarise information; evaluate…"
          },
          {
            "id": "english-1-3",
            "name": "Comprehending: Identify the author's point of view…"
          },
          {
            "id": "english-1-4",
            "name": "Comprehending"
          },
          {
            "id": "english-1-5",
            "name": "Composing"
          },
          {
            "id": "english-1-6",
            "name": "Composing: Letters of all kinds"
          },
          {
            "id": "english-1-7",
            "name": "Composing: Reports and research projects"
          },
          {
            "id": "english-1-8",
            "name": "Composing: Media scripts and newspaper reports"
          }
        ]
      },
      {
        "id": "english-2",
        "name": "The Language of Argument",
        "subtopics": [
          {
            "id": "english-2-0",
            "name": "Argumentative texts: Deductive and inductive reasoning"
          },
          {
            "id": "english-2-1",
            "name": "Comprehending: Outline the stages of an argument and…"
          },
          {
            "id": "english-2-2",
            "name": "Comprehending: Identify reasoning structure"
          },
          {
            "id": "english-2-3",
            "name": "Comprehending"
          },
          {
            "id": "english-2-4",
            "name": "Comprehending: Evaluate validity; identify…"
          },
          {
            "id": "english-2-5",
            "name": "Composing: Put forward a theory or hypothesis"
          },
          {
            "id": "english-2-6",
            "name": "Composing: Justify a decision; attempt an overview"
          }
        ]
      },
      {
        "id": "english-3",
        "name": "The Language of Persuasion",
        "subtopics": [
          {
            "id": "english-3-0",
            "name": "Persuasive texts"
          },
          {
            "id": "english-3-1",
            "name": "Comprehending: Identify persuasive techniques"
          },
          {
            "id": "english-3-2",
            "name": "Comprehending: Evaluate impact in achieving desired…"
          },
          {
            "id": "english-3-3",
            "name": "Comprehending: Analyse value-system…"
          },
          {
            "id": "english-3-4",
            "name": "Composing: Newspaper articles"
          },
          {
            "id": "english-3-5",
            "name": "Composing: Advertising copy"
          },
          {
            "id": "english-3-6",
            "name": "Composing: Public relations / propaganda / political…"
          }
        ]
      },
      {
        "id": "english-4",
        "name": "The Language of Narration",
        "subtopics": [
          {
            "id": "english-4-0",
            "name": "Narrative texts"
          },
          {
            "id": "english-4-1",
            "name": "Comprehending: Awareness of own response to texts…"
          },
          {
            "id": "english-4-2",
            "name": "Comprehending: Indicate significant aspects of…"
          },
          {
            "id": "english-4-3",
            "name": "Comprehending: Outline narrative structure and how it…"
          },
          {
            "id": "english-4-4",
            "name": "Comprehending: Narrative characteristics of different…"
          },
          {
            "id": "english-4-5",
            "name": "Comprehending: Critical viewpoints across periods and…"
          },
          {
            "id": "english-4-6",
            "name": "Comprehending: Compare texts in different genres on…"
          },
          {
            "id": "english-4-7",
            "name": "Composing: Anecdote"
          },
          {
            "id": "english-4-8",
            "name": "Composing"
          },
          {
            "id": "english-4-9",
            "name": "Composing: Short story"
          },
          {
            "id": "english-4-10",
            "name": "Composing: Autobiographical sketch"
          },
          {
            "id": "english-4-11",
            "name": "Composing: Scripts and dialogues"
          }
        ]
      },
      {
        "id": "english-5",
        "name": "The Aesthetic Use of Language",
        "subtopics": [
          {
            "id": "english-5-0",
            "name": "Literary genres"
          },
          {
            "id": "english-5-1",
            "name": "Comprehending: Appropriate stances for…"
          },
          {
            "id": "english-5-2",
            "name": "Comprehending: Interpretative performance of texts"
          },
          {
            "id": "english-5-3",
            "name": "Comprehending"
          },
          {
            "id": "english-5-4",
            "name": "Comprehending"
          },
          {
            "id": "english-5-5",
            "name": "Comprehending: Compare and evaluate texts for the…"
          },
          {
            "id": "english-5-6",
            "name": "Composing: Compose within the aesthetic forms…"
          },
          {
            "id": "english-5-7",
            "name": "Composing: Interventions"
          },
          {
            "id": "english-5-8",
            "name": "Composing: Response journals"
          },
          {
            "id": "english-5-9",
            "name": "Composing: Analytical and coherent essays relative to…"
          }
        ]
      },
      {
        "id": "english-6",
        "name": "Single Text (Text studied on its own)",
        "subtopics": [
          {
            "id": "english-6-0",
            "name": "In-depth study of one prescribed text"
          },
          {
            "id": "english-6-1",
            "name": "Shakespearean drama"
          },
          {
            "id": "english-6-2",
            "name": "Attitudes, values, structures and styles within the…"
          },
          {
            "id": "english-6-3",
            "name": "Form, structure and style and how they constitute…"
          }
        ]
      },
      {
        "id": "english-7",
        "name": "Comparative Study (three or more texts)",
        "subtopics": [
          {
            "id": "english-7-0",
            "name": "Higher Level mode: A theme or issue"
          },
          {
            "id": "english-7-1",
            "name": "Higher Level mode: A historical or literary period"
          },
          {
            "id": "english-7-2",
            "name": "Higher Level mode: A literary genre"
          },
          {
            "id": "english-7-3",
            "name": "Higher Level mode: The cultural context"
          },
          {
            "id": "english-7-4",
            "name": "Higher Level mode: The general vision and viewpoint"
          },
          {
            "id": "english-7-5",
            "name": "Ordinary Level mode: Hero/Heroine/Villain"
          },
          {
            "id": "english-7-6",
            "name": "Ordinary Level mode: Relationships"
          },
          {
            "id": "english-7-7",
            "name": "Ordinary Level mode: Social Setting"
          },
          {
            "id": "english-7-8",
            "name": "Ordinary Level mode: Change and Development"
          },
          {
            "id": "english-7-9",
            "name": "Ordinary Level mode: Specific Themes"
          },
          {
            "id": "english-7-10",
            "name": "Ordinary Level mode: Aspects of story"
          },
          {
            "id": "english-7-11",
            "name": "Film as an element within the comparative study"
          }
        ]
      },
      {
        "id": "english-8",
        "name": "Poetry",
        "subtopics": [
          {
            "id": "english-8-0",
            "name": "Higher Level: Representative selection from eight…"
          },
          {
            "id": "english-8-1",
            "name": "Ordinary Level: Selection of prescribed poetry"
          },
          {
            "id": "english-8-2",
            "name": "Unseen poem (both levels)"
          },
          {
            "id": "english-8-3",
            "name": "Reading widely in poetry"
          }
        ]
      },
      {
        "id": "english-9",
        "name": "Examination Structure",
        "subtopics": [
          {
            "id": "english-9-0",
            "name": "Paper I, Section: Comprehending"
          },
          {
            "id": "english-9-1",
            "name": "Paper I, Section: Composing"
          },
          {
            "id": "english-9-2",
            "name": "Paper II, Section A: In-depth study of the Single Text"
          },
          {
            "id": "english-9-3",
            "name": "Paper II, Section B: Comparative Study"
          },
          {
            "id": "english-9-4",
            "name": "Paper II, Section C: Poetry"
          }
        ]
      }
    ]
  },
  {
    "id": "french",
    "name": "French",
    "category": "language",
    "levels": [
      "higher",
      "ordinary"
    ],
    "strands": [
      {
        "id": "french-0",
        "name": "Basic Communicative Proficiency",
        "subtopics": [
          {
            "id": "french-0-0",
            "name": "Meeting and getting to know people and maintaining…"
          },
          {
            "id": "french-0-1",
            "name": "Making plans and discussing future action"
          },
          {
            "id": "french-0-2",
            "name": "Understanding, seeking and giving information about…"
          },
          {
            "id": "french-0-3",
            "name": "Coping with travel and transport"
          },
          {
            "id": "french-0-4",
            "name": "Buying goods and services"
          },
          {
            "id": "french-0-5",
            "name": "Dealing with emergencies"
          },
          {
            "id": "french-0-6",
            "name": "Facilitating, encouraging or impeding a course of…"
          },
          {
            "id": "french-0-7",
            "name": "Understanding, expressing feelings and attitudes"
          },
          {
            "id": "french-0-8",
            "name": "Managing a conversation"
          },
          {
            "id": "french-0-9",
            "name": "Engaging in discussion"
          },
          {
            "id": "french-0-10",
            "name": "Passing on messages"
          }
        ]
      },
      {
        "id": "french-1",
        "name": "Language Awareness",
        "subtopics": [
          {
            "id": "french-1-0",
            "name": "Learning about language from target language material"
          },
          {
            "id": "french-1-1",
            "name": "Exploring meaning"
          },
          {
            "id": "french-1-2",
            "name": "Relating language to attitude"
          },
          {
            "id": "french-1-3",
            "name": "Talking and writing about your experience of the…"
          },
          {
            "id": "french-1-4",
            "name": "Consulting reference materials relating to the…"
          }
        ]
      },
      {
        "id": "french-2",
        "name": "Cultural Awareness",
        "subtopics": [
          {
            "id": "french-2-0",
            "name": "Learning in the target language about the present-day…"
          },
          {
            "id": "french-2-1",
            "name": "Reading modern literary texts in the target language"
          },
          {
            "id": "french-2-2",
            "name": "Describing and discussing everyday life in the target…"
          },
          {
            "id": "french-2-3",
            "name": "Understanding, describing and discussing aspects of…"
          },
          {
            "id": "french-2-4",
            "name": "Understanding, describing and discussing in general…"
          }
        ]
      }
    ]
  },
  {
    "id": "german",
    "name": "German",
    "category": "language",
    "levels": [
      "higher",
      "ordinary"
    ],
    "strands": [
      {
        "id": "german-0",
        "name": "Basic Communicative Proficiency",
        "subtopics": [
          {
            "id": "german-0-0",
            "name": "Meeting and getting to know people and maintaining…"
          },
          {
            "id": "german-0-1",
            "name": "Making plans and discussing future action"
          },
          {
            "id": "german-0-2",
            "name": "Understanding, seeking and giving information about…"
          },
          {
            "id": "german-0-3",
            "name": "Coping with travel and transport"
          },
          {
            "id": "german-0-4",
            "name": "Buying goods and services"
          },
          {
            "id": "german-0-5",
            "name": "Dealing with emergencies"
          },
          {
            "id": "german-0-6",
            "name": "Facilitating, encouraging or impeding a course of…"
          },
          {
            "id": "german-0-7",
            "name": "Understanding and expressing feelings and attitudes"
          },
          {
            "id": "german-0-8",
            "name": "Managing a conversation"
          },
          {
            "id": "german-0-9",
            "name": "Engaging in discussion"
          },
          {
            "id": "german-0-10",
            "name": "Passing on messages"
          }
        ]
      },
      {
        "id": "german-1",
        "name": "Language Awareness",
        "subtopics": [
          {
            "id": "german-1-0",
            "name": "Learning about language from target language material"
          },
          {
            "id": "german-1-1",
            "name": "Exploring meaning"
          },
          {
            "id": "german-1-2",
            "name": "Relating language to attitude"
          },
          {
            "id": "german-1-3",
            "name": "Talking and writing about your experience of the…"
          },
          {
            "id": "german-1-4",
            "name": "Consulting reference materials relating to the…"
          }
        ]
      },
      {
        "id": "german-2",
        "name": "Cultural Awareness",
        "subtopics": [
          {
            "id": "german-2-0",
            "name": "Learning in the target language about the present-day…"
          },
          {
            "id": "german-2-1",
            "name": "Reading modern literary texts in the target language"
          },
          {
            "id": "german-2-2",
            "name": "Describing and discussing everyday life in the target…"
          },
          {
            "id": "german-2-3",
            "name": "Understanding, describing and discussing aspects of…"
          },
          {
            "id": "german-2-4",
            "name": "Understanding, describing and discussing in general…"
          }
        ]
      },
      {
        "id": "german-3",
        "name": "Assessment (Four Skills)",
        "subtopics": [
          {
            "id": "german-3-0",
            "name": "Oral Assessment - Higher 25% / Ordinary 20%"
          },
          {
            "id": "german-3-1",
            "name": "Listening Comprehension - Higher 20% / Ordinary 25%"
          },
          {
            "id": "german-3-2",
            "name": "Reading Comprehension - Higher 30% / Ordinary 40%"
          },
          {
            "id": "german-3-3",
            "name": "Written Production - Higher 25% / Ordinary 15%"
          }
        ]
      }
    ]
  },
  {
    "id": "spanish",
    "name": "Spanish",
    "category": "language",
    "levels": [
      "higher",
      "ordinary"
    ],
    "strands": [
      {
        "id": "spanish-0",
        "name": "Basic Communicative Proficiency",
        "subtopics": [
          {
            "id": "spanish-0-0",
            "name": "Meeting and getting to know people and maintaining…"
          },
          {
            "id": "spanish-0-1",
            "name": "Making plans and discussing future action"
          },
          {
            "id": "spanish-0-2",
            "name": "Seeking and giving information about climate and…"
          },
          {
            "id": "spanish-0-3",
            "name": "Coping with travel and transport"
          },
          {
            "id": "spanish-0-4",
            "name": "Buying goods and services"
          },
          {
            "id": "spanish-0-5",
            "name": "Dealing with emergencies"
          },
          {
            "id": "spanish-0-6",
            "name": "Facilitating, encouraging or impeding a course of…"
          },
          {
            "id": "spanish-0-7",
            "name": "Expressing feelings and attitudes"
          },
          {
            "id": "spanish-0-8",
            "name": "Managing a conversation"
          },
          {
            "id": "spanish-0-9",
            "name": "Engaging in discussion"
          },
          {
            "id": "spanish-0-10",
            "name": "Passing on messages"
          }
        ]
      },
      {
        "id": "spanish-1",
        "name": "Language Awareness",
        "subtopics": [
          {
            "id": "spanish-1-0",
            "name": "Learning about language from target language material"
          },
          {
            "id": "spanish-1-1",
            "name": "Exploring meaning"
          },
          {
            "id": "spanish-1-2",
            "name": "Relating language to attitude"
          },
          {
            "id": "spanish-1-3",
            "name": "Talking and writing about your experience of the…"
          },
          {
            "id": "spanish-1-4",
            "name": "Consulting reference materials relating to the…"
          }
        ]
      },
      {
        "id": "spanish-2",
        "name": "Cultural Awareness",
        "subtopics": [
          {
            "id": "spanish-2-0",
            "name": "Learning in the target language about the present-day…"
          },
          {
            "id": "spanish-2-1",
            "name": "Reading modern literary texts in the target language"
          },
          {
            "id": "spanish-2-2",
            "name": "Describing and discussing everyday life in target…"
          },
          {
            "id": "spanish-2-3",
            "name": "Understanding, describing and discussing aspects of…"
          },
          {
            "id": "spanish-2-4",
            "name": "Understanding, describing and discussing in general…"
          }
        ]
      }
    ]
  },
  {
    "id": "italian",
    "name": "Italian",
    "category": "language",
    "levels": [
      "higher",
      "ordinary"
    ],
    "strands": [
      {
        "id": "italian-0",
        "name": "Basic Communicative Proficiency",
        "subtopics": [
          {
            "id": "italian-0-0",
            "name": "Meeting and getting to know people and maintaining…"
          },
          {
            "id": "italian-0-1",
            "name": "Making plans and discussing future action"
          },
          {
            "id": "italian-0-2",
            "name": "Understanding, seeking and giving information about…"
          },
          {
            "id": "italian-0-3",
            "name": "Coping with travel and transport"
          },
          {
            "id": "italian-0-4",
            "name": "Buying goods and services"
          },
          {
            "id": "italian-0-5",
            "name": "Dealing with emergencies"
          },
          {
            "id": "italian-0-6",
            "name": "Facilitating, encouraging or impeding a course of…"
          },
          {
            "id": "italian-0-7",
            "name": "Understanding and expressing feelings and attitudes"
          },
          {
            "id": "italian-0-8",
            "name": "Managing a conversation"
          },
          {
            "id": "italian-0-9",
            "name": "Engaging in discussion"
          },
          {
            "id": "italian-0-10",
            "name": "Passing on messages"
          }
        ]
      },
      {
        "id": "italian-1",
        "name": "Language Awareness",
        "subtopics": [
          {
            "id": "italian-1-0",
            "name": "Learning about language from target language material"
          },
          {
            "id": "italian-1-1",
            "name": "Exploring meaning"
          },
          {
            "id": "italian-1-2",
            "name": "Relating language to attitude"
          },
          {
            "id": "italian-1-3",
            "name": "Talking and writing about your experience of the…"
          },
          {
            "id": "italian-1-4",
            "name": "Consulting reference materials, relating to the…"
          }
        ]
      },
      {
        "id": "italian-2",
        "name": "Cultural Awareness",
        "subtopics": [
          {
            "id": "italian-2-0",
            "name": "Learning in the target language about the present-day…"
          },
          {
            "id": "italian-2-1",
            "name": "Reading modern literary texts in the target language"
          },
          {
            "id": "italian-2-2",
            "name": "Describing and discussing everyday life in the target…"
          },
          {
            "id": "italian-2-3",
            "name": "Understanding, describing and discussing aspects of…"
          },
          {
            "id": "italian-2-4",
            "name": "Understanding, describing and discussing in general…"
          }
        ]
      }
    ]
  },
  {
    "id": "russian",
    "name": "Russian",
    "category": "language",
    "levels": [
      "higher",
      "ordinary"
    ],
    "strands": [
      {
        "id": "russian-0",
        "name": "Basic Communicative Proficiency",
        "subtopics": [
          {
            "id": "russian-0-0",
            "name": "Meeting and getting to know people and maintaining…"
          },
          {
            "id": "russian-0-1",
            "name": "Discussing family and home"
          },
          {
            "id": "russian-0-2",
            "name": "Asking about and describing the general nature of the…"
          },
          {
            "id": "russian-0-3",
            "name": "Talking about learning"
          },
          {
            "id": "russian-0-4",
            "name": "Enquiring about and describing work"
          },
          {
            "id": "russian-0-5",
            "name": "Enquiring about and discussing leisure pursuits"
          },
          {
            "id": "russian-0-6",
            "name": "Making plans and discussing future action"
          },
          {
            "id": "russian-0-7",
            "name": "Talking about events in people's lives"
          },
          {
            "id": "russian-0-8",
            "name": "Coping with travel and transport"
          },
          {
            "id": "russian-0-9",
            "name": "Buying goods and services"
          },
          {
            "id": "russian-0-10",
            "name": "Facilitating, encouraging or impeding a course of…"
          },
          {
            "id": "russian-0-11",
            "name": "Understanding, expressing feelings and attitudes"
          },
          {
            "id": "russian-0-12",
            "name": "Managing a conversation"
          },
          {
            "id": "russian-0-13",
            "name": "Engaging in discussion"
          },
          {
            "id": "russian-0-14",
            "name": "Passing on messages"
          }
        ]
      },
      {
        "id": "russian-1",
        "name": "Language Awareness",
        "subtopics": [
          {
            "id": "russian-1-0",
            "name": "Learning about language from target language material"
          },
          {
            "id": "russian-1-1",
            "name": "Exploring meaning"
          },
          {
            "id": "russian-1-2",
            "name": "Relating language to attitude"
          },
          {
            "id": "russian-1-3",
            "name": "Talking and writing about your experience of the…"
          },
          {
            "id": "russian-1-4",
            "name": "Consulting reference materials relating to the…"
          }
        ]
      },
      {
        "id": "russian-2",
        "name": "Cultural Awareness",
        "subtopics": [
          {
            "id": "russian-2-0",
            "name": "Learning in the target language about the present-day…"
          },
          {
            "id": "russian-2-1",
            "name": "Reading extracts from modern literary texts in the…"
          },
          {
            "id": "russian-2-2",
            "name": "Describing and discussing everyday life in the target…"
          },
          {
            "id": "russian-2-3",
            "name": "Understanding, describing and discussing aspects of…"
          },
          {
            "id": "russian-2-4",
            "name": "Understanding, describing and discussing in general…"
          },
          {
            "id": "russian-2-5",
            "name": "Aspects of Russian culture"
          },
          {
            "id": "russian-2-6",
            "name": "Aspects of Russian history"
          },
          {
            "id": "russian-2-7",
            "name": "A society in transition"
          },
          {
            "id": "russian-2-8",
            "name": "The place of Russia on the world stage"
          },
          {
            "id": "russian-2-9",
            "name": "The challenges facing a multi-cultural state"
          },
          {
            "id": "russian-2-10",
            "name": "The Russian landscape"
          },
          {
            "id": "russian-2-11",
            "name": "Aspects of contemporary Russian life"
          },
          {
            "id": "russian-2-12",
            "name": "Russian traditions, customs and practices"
          }
        ]
      }
    ]
  },
  {
    "id": "japanese",
    "name": "Japanese",
    "category": "language",
    "levels": [
      "higher",
      "ordinary"
    ],
    "strands": [
      {
        "id": "japanese-0",
        "name": "Basic Communicative Proficiency",
        "subtopics": [
          {
            "id": "japanese-0-0",
            "name": "Meeting and getting to know people and maintaining…"
          },
          {
            "id": "japanese-0-1",
            "name": "Managing a conversation"
          },
          {
            "id": "japanese-0-2",
            "name": "Making plans and discussing future action"
          },
          {
            "id": "japanese-0-3",
            "name": "Understanding, seeking and giving information about…"
          },
          {
            "id": "japanese-0-4",
            "name": "Coping with travel and transport"
          },
          {
            "id": "japanese-0-5",
            "name": "Buying goods and services"
          },
          {
            "id": "japanese-0-6",
            "name": "Dealing with emergencies"
          },
          {
            "id": "japanese-0-7",
            "name": "Requesting, facilitating or impeding a course of…"
          },
          {
            "id": "japanese-0-8",
            "name": "Understanding and expressing feelings and attitudes"
          },
          {
            "id": "japanese-0-9",
            "name": "Engaging in discussion"
          },
          {
            "id": "japanese-0-10",
            "name": "Passing on messages"
          }
        ]
      },
      {
        "id": "japanese-1",
        "name": "Language Awareness",
        "subtopics": [
          {
            "id": "japanese-1-0",
            "name": "Learning about language from target language material"
          },
          {
            "id": "japanese-1-1",
            "name": "Exploring meaning"
          },
          {
            "id": "japanese-1-2",
            "name": "Relating language to attitude"
          },
          {
            "id": "japanese-1-3",
            "name": "Talking and writing about your experience of the…"
          },
          {
            "id": "japanese-1-4",
            "name": "Consulting reference materials relating to the…"
          }
        ]
      },
      {
        "id": "japanese-2",
        "name": "Cultural Awareness",
        "subtopics": [
          {
            "id": "japanese-2-0",
            "name": "Learning in the target language about the present-day…"
          },
          {
            "id": "japanese-2-1",
            "name": "Reading extracts from modern texts of various kinds…"
          },
          {
            "id": "japanese-2-2",
            "name": "Describing and discussing everyday life in the target…"
          },
          {
            "id": "japanese-2-3",
            "name": "Understanding, describing and discussing aspects of…"
          },
          {
            "id": "japanese-2-4",
            "name": "Understanding, describing and discussing issues that…"
          }
        ]
      },
      {
        "id": "japanese-3",
        "name": "Writing Systems (Kana and Kanji)",
        "subtopics": [
          {
            "id": "japanese-3-0",
            "name": "Hiragana"
          },
          {
            "id": "japanese-3-1",
            "name": "Katakana"
          },
          {
            "id": "japanese-3-2",
            "name": "Kanji"
          }
        ]
      },
      {
        "id": "japanese-4",
        "name": "Assessment — The Four Skills",
        "subtopics": [
          {
            "id": "japanese-4-0",
            "name": "Speaking / Oral examination"
          },
          {
            "id": "japanese-4-1",
            "name": "Listening comprehension (aural)"
          },
          {
            "id": "japanese-4-2",
            "name": "Reading comprehension"
          },
          {
            "id": "japanese-4-3",
            "name": "Written production"
          }
        ]
      }
    ]
  },
  {
    "id": "mandarin-chinese",
    "name": "Mandarin Chinese",
    "category": "language",
    "levels": [
      "higher",
      "ordinary"
    ],
    "strands": [
      {
        "id": "mandarin-chinese-0",
        "name": "Communicative Language Competence",
        "subtopics": [
          {
            "id": "mandarin-chinese-0-0",
            "name": "Reception"
          },
          {
            "id": "mandarin-chinese-0-1",
            "name": "Reception"
          },
          {
            "id": "mandarin-chinese-0-2",
            "name": "Reception"
          },
          {
            "id": "mandarin-chinese-0-3",
            "name": "Reception"
          },
          {
            "id": "mandarin-chinese-0-4",
            "name": "Reception: Understand a lexical range comprised of…"
          },
          {
            "id": "mandarin-chinese-0-5",
            "name": "Reception"
          },
          {
            "id": "mandarin-chinese-0-6",
            "name": "Reception"
          },
          {
            "id": "mandarin-chinese-0-7",
            "name": "Interaction"
          },
          {
            "id": "mandarin-chinese-0-8",
            "name": "Interaction: Deal with simple transactions likely to…"
          },
          {
            "id": "mandarin-chinese-0-9",
            "name": "Interaction"
          },
          {
            "id": "mandarin-chinese-0-10",
            "name": "Interaction"
          },
          {
            "id": "mandarin-chinese-0-11",
            "name": "Interaction"
          },
          {
            "id": "mandarin-chinese-0-12",
            "name": "Production"
          },
          {
            "id": "mandarin-chinese-0-13",
            "name": "Production"
          },
          {
            "id": "mandarin-chinese-0-14",
            "name": "Production"
          },
          {
            "id": "mandarin-chinese-0-15",
            "name": "Production"
          },
          {
            "id": "mandarin-chinese-0-16",
            "name": "Production"
          },
          {
            "id": "mandarin-chinese-0-17",
            "name": "Production"
          },
          {
            "id": "mandarin-chinese-0-18",
            "name": "Production"
          },
          {
            "id": "mandarin-chinese-0-19",
            "name": "Mediation"
          },
          {
            "id": "mandarin-chinese-0-20",
            "name": "Mediation"
          },
          {
            "id": "mandarin-chinese-0-21",
            "name": "Mediation"
          },
          {
            "id": "mandarin-chinese-0-22",
            "name": "Mediation"
          },
          {
            "id": "mandarin-chinese-0-23",
            "name": "Mediation: Use simple words to ask someone to explain…"
          },
          {
            "id": "mandarin-chinese-0-24",
            "name": "Mediation: Recognise when speakers disagree or have a…"
          },
          {
            "id": "mandarin-chinese-0-25",
            "name": "Mediation"
          }
        ]
      },
      {
        "id": "mandarin-chinese-1",
        "name": "Plurilingual and Pluricultural Competence",
        "subtopics": [
          {
            "id": "mandarin-chinese-1-0",
            "name": "Plurilingual competence (element)"
          },
          {
            "id": "mandarin-chinese-1-1",
            "name": "Plurilingual"
          },
          {
            "id": "mandarin-chinese-1-2",
            "name": "Plurilingual: Recognise a range of linguistic…"
          },
          {
            "id": "mandarin-chinese-1-3",
            "name": "Plurilingual: Apply communication and compensation…"
          },
          {
            "id": "mandarin-chinese-1-4",
            "name": "Plurilingual"
          },
          {
            "id": "mandarin-chinese-1-5",
            "name": "Plurilingual"
          },
          {
            "id": "mandarin-chinese-1-6",
            "name": "Plurilingual: Recognise similarities and differences…"
          },
          {
            "id": "mandarin-chinese-1-7",
            "name": "Plurilingual"
          },
          {
            "id": "mandarin-chinese-1-8",
            "name": "Plurilingual"
          },
          {
            "id": "mandarin-chinese-1-9",
            "name": "Pluricultural competence: Awareness and understanding…"
          },
          {
            "id": "mandarin-chinese-1-10",
            "name": "Pluricultural: Explore and appreciate popular culture…"
          },
          {
            "id": "mandarin-chinese-1-11",
            "name": "Pluricultural"
          },
          {
            "id": "mandarin-chinese-1-12",
            "name": "Pluricultural"
          },
          {
            "id": "mandarin-chinese-1-13",
            "name": "Pluricultural"
          },
          {
            "id": "mandarin-chinese-1-14",
            "name": "Pluricultural"
          },
          {
            "id": "mandarin-chinese-1-15",
            "name": "Pluricultural: Explain features of the target…"
          },
          {
            "id": "mandarin-chinese-1-16",
            "name": "Pluricultural: Demonstrate awareness of and use…"
          },
          {
            "id": "mandarin-chinese-1-17",
            "name": "Pluricultural"
          },
          {
            "id": "mandarin-chinese-1-18",
            "name": "Pluricultural"
          },
          {
            "id": "mandarin-chinese-1-19",
            "name": "Pluricultural: Explore their own cultural identity…"
          }
        ]
      },
      {
        "id": "mandarin-chinese-2",
        "name": "Assessment for Certification (exam components)",
        "subtopics": [
          {
            "id": "mandarin-chinese-2-0",
            "name": "Oral examination - includes discussion of the…"
          },
          {
            "id": "mandarin-chinese-2-1",
            "name": "Aural examination - assesses listening reception and…"
          },
          {
            "id": "mandarin-chinese-2-2",
            "name": "Written examination - Reading and Writing; assesses…"
          },
          {
            "id": "mandarin-chinese-2-3",
            "name": "Language Portfolio"
          },
          {
            "id": "mandarin-chinese-2-4",
            "name": "Pin Yin and simplified characters"
          }
        ]
      }
    ]
  },
  {
    "id": "latin",
    "name": "Latin",
    "category": "language",
    "levels": [
      "higher",
      "ordinary"
    ],
    "strands": [
      {
        "id": "latin-0",
        "name": "Strand 1: Latin Language",
        "subtopics": [
          {
            "id": "latin-0-0",
            "name": "Understanding Latin texts (core element)"
          },
          {
            "id": "latin-0-1",
            "name": "Different text formats"
          },
          {
            "id": "latin-0-2",
            "name": "Different ways of reading"
          },
          {
            "id": "latin-0-3",
            "name": "Learning words and expressions, and strategies to do…"
          },
          {
            "id": "latin-0-4",
            "name": "Lexical phenomena"
          },
          {
            "id": "latin-0-5",
            "name": "Pronunciation"
          },
          {
            "id": "latin-0-6",
            "name": "Composition into Latin"
          },
          {
            "id": "latin-0-7",
            "name": "Distinguishing stem and ending; how parts of words…"
          },
          {
            "id": "latin-0-8",
            "name": "Translation: Creating accurate and idiomatic…"
          },
          {
            "id": "latin-0-9",
            "name": "How source and target language convey meaning…"
          },
          {
            "id": "latin-0-10",
            "name": "Evaluating information in texts"
          },
          {
            "id": "latin-0-11",
            "name": "Distinctive literary techniques, formal features and…"
          },
          {
            "id": "latin-0-12",
            "name": "Developing language awareness and analytical skills…"
          },
          {
            "id": "latin-0-13",
            "name": "Morphology and syntax; word types, inflection…"
          },
          {
            "id": "latin-0-14",
            "name": "Constituent parts of words"
          },
          {
            "id": "latin-0-15",
            "name": "Word types"
          },
          {
            "id": "latin-0-16",
            "name": "Inflection patterns: Nominal declensions and verbal…"
          },
          {
            "id": "latin-0-17",
            "name": "Main clauses and main verbs, participial and…"
          },
          {
            "id": "latin-0-18",
            "name": "Spelling and punctuation conventions"
          },
          {
            "id": "latin-0-19",
            "name": "Logical reasoning from syntactical construction…"
          },
          {
            "id": "latin-0-20",
            "name": "Using dictionaries, vocabulary lists, grammars…"
          },
          {
            "id": "latin-0-21",
            "name": "Comparing languages: Similarities and differences in…"
          },
          {
            "id": "latin-0-22",
            "name": "Etymology of words derived from Latin in English…"
          },
          {
            "id": "latin-0-23",
            "name": "Culture-specific abstract concepts with no direct…"
          },
          {
            "id": "latin-0-24",
            "name": "How word choice, syntax, grammar and text structure…"
          },
          {
            "id": "latin-0-25",
            "name": "Monitoring language confidence, learning strategies…"
          },
          {
            "id": "latin-0-26",
            "name": "Prescribed grammatical forms and constructions for…"
          }
        ]
      },
      {
        "id": "latin-1",
        "name": "Strand 2: Literature in context",
        "subtopics": [
          {
            "id": "latin-1-0",
            "name": "Latin literature (core element)"
          },
          {
            "id": "latin-1-1",
            "name": "Responding to texts: Relating events to personal…"
          },
          {
            "id": "latin-1-2",
            "name": "Investigating characters and their relationships…"
          },
          {
            "id": "latin-1-3",
            "name": "Researching the context of Latin texts and their…"
          },
          {
            "id": "latin-1-4",
            "name": "Contexts relevant to understanding texts"
          },
          {
            "id": "latin-1-5",
            "name": "Close reading"
          },
          {
            "id": "latin-1-6",
            "name": "Significance of a literary text for its original…"
          },
          {
            "id": "latin-1-7",
            "name": "Reception of Latin literature"
          },
          {
            "id": "latin-1-8",
            "name": "Continued importance and survival of Latin as a…"
          },
          {
            "id": "latin-1-9",
            "name": "Roman culture explored through Latin texts (core…"
          },
          {
            "id": "latin-1-10",
            "name": "Regions, communities and cultures who have used…"
          },
          {
            "id": "latin-1-11",
            "name": "Cultural heritage and daily life of ancient Rome"
          },
          {
            "id": "latin-1-12",
            "name": "Roman values and attitudes; social hierarchy, status…"
          },
          {
            "id": "latin-1-13",
            "name": "Critically discussing Roman society, history…"
          },
          {
            "id": "latin-1-14",
            "name": "Roman cultural identity and self-representation…"
          }
        ]
      },
      {
        "id": "latin-2",
        "name": "Capstone Text and Assessment Components",
        "subtopics": [
          {
            "id": "latin-2-0",
            "name": "Capstone text"
          },
          {
            "id": "latin-2-1",
            "name": "Capstone text general context"
          },
          {
            "id": "latin-2-2",
            "name": "Written examination (60%) - Higher and Ordinary level"
          },
          {
            "id": "latin-2-3",
            "name": "Additional assessment component"
          }
        ]
      }
    ]
  },
  {
    "id": "ancient-greek",
    "name": "Ancient Greek",
    "category": "language",
    "levels": [
      "higher",
      "ordinary"
    ],
    "strands": [
      {
        "id": "ancient-greek-0",
        "name": "Strand 1: Ancient Greek Language",
        "subtopics": [
          {
            "id": "ancient-greek-0-0",
            "name": "Element: Understanding Ancient Greek texts"
          },
          {
            "id": "ancient-greek-0-1",
            "name": "1.1 Explore a range of authentic, adapted and…"
          },
          {
            "id": "ancient-greek-0-2",
            "name": "1.2 Recognise lexical items at the level of words…"
          },
          {
            "id": "ancient-greek-0-3",
            "name": "1.3 Pronounce Ancient Greek words, phrases and…"
          },
          {
            "id": "ancient-greek-0-4",
            "name": "1.4 Collaborate with others to understand Ancient…"
          },
          {
            "id": "ancient-greek-0-5",
            "name": "1.5 Explore vocabulary and grammatical rules by…"
          },
          {
            "id": "ancient-greek-0-6",
            "name": "1.6 Create accurate and idiomatic translations of…"
          },
          {
            "id": "ancient-greek-0-7",
            "name": "1.7 Evaluate information contained in Ancient Greek…"
          },
          {
            "id": "ancient-greek-0-8",
            "name": "1.8 Describe the content and structure of Ancient…"
          },
          {
            "id": "ancient-greek-0-9",
            "name": "1.9 Evaluate different translations of an Ancient…"
          },
          {
            "id": "ancient-greek-0-10",
            "name": "1.10 Appreciate distinctive features and aims of…"
          },
          {
            "id": "ancient-greek-0-11",
            "name": "Element: Developing language awareness and analytical…"
          },
          {
            "id": "ancient-greek-0-12",
            "name": "1.11 Make sense of unfamiliar Ancient Greek words and…"
          },
          {
            "id": "ancient-greek-0-13",
            "name": "1.12 Recognise linguistic patterns and structures and…"
          },
          {
            "id": "ancient-greek-0-14",
            "name": "1.13 Explain the reasoning that led to a specific…"
          },
          {
            "id": "ancient-greek-0-15",
            "name": "1.14 Effectively use Ancient Greek language resources"
          },
          {
            "id": "ancient-greek-0-16",
            "name": "1.15 Monitor and assess own language confidence…"
          },
          {
            "id": "ancient-greek-0-17",
            "name": "1.16 Recognise similarities and differences in how…"
          },
          {
            "id": "ancient-greek-0-18",
            "name": "1.17 Compare and contrast known languages to support…"
          },
          {
            "id": "ancient-greek-0-19",
            "name": "1.18 Investigate the etymology of words derived from…"
          },
          {
            "id": "ancient-greek-0-20",
            "name": "1.19 Assess how word choice, syntax, grammar and text…"
          }
        ]
      },
      {
        "id": "ancient-greek-1",
        "name": "Strand 2: Literature in context",
        "subtopics": [
          {
            "id": "ancient-greek-1-0",
            "name": "Element: Ancient Greek literature"
          },
          {
            "id": "ancient-greek-1-1",
            "name": "2.1 Give a response to Ancient Greek texts"
          },
          {
            "id": "ancient-greek-1-2",
            "name": "2.2 Research the context of Ancient Greek texts and…"
          },
          {
            "id": "ancient-greek-1-3",
            "name": "2.3 Explain specific aspects of a text with reference…"
          },
          {
            "id": "ancient-greek-1-4",
            "name": "2.4 Employ close reading to support interpretation…"
          },
          {
            "id": "ancient-greek-1-5",
            "name": "2.5 Consider the significance a literary text has for…"
          },
          {
            "id": "ancient-greek-1-6",
            "name": "2.6 Examine examples of reception of an Ancient Greek…"
          },
          {
            "id": "ancient-greek-1-7",
            "name": "2.7 Appreciate the continued importance of Ancient…"
          },
          {
            "id": "ancient-greek-1-8",
            "name": "Element: Hellenic culture explored through Ancient…"
          },
          {
            "id": "ancient-greek-1-9",
            "name": "2.8 Research and discuss the regions, communities and…"
          },
          {
            "id": "ancient-greek-1-10",
            "name": "2.9 Examine the diverse cultural heritage and daily…"
          },
          {
            "id": "ancient-greek-1-11",
            "name": "2.10 Examine what Ancient Greek texts reveal about…"
          },
          {
            "id": "ancient-greek-1-12",
            "name": "2.11 Critically discuss aspects of ancient Greek…"
          },
          {
            "id": "ancient-greek-1-13",
            "name": "2.12 Use Ancient Greek texts to examine Greek…"
          }
        ]
      },
      {
        "id": "ancient-greek-2",
        "name": "Capstone Text & Prescribed Material (cross-strand examination focus)",
        "subtopics": [
          {
            "id": "ancient-greek-2-0",
            "name": "The Capstone text: Prescribed title and author with…"
          },
          {
            "id": "ancient-greek-2-1",
            "name": "Guidance on general context of the Capstone text"
          },
          {
            "id": "ancient-greek-2-2",
            "name": "Prescribed grammatical forms and constructions for…"
          }
        ]
      },
      {
        "id": "ancient-greek-3",
        "name": "Additional Assessment Component: Research Study – Text in Context (40%)",
        "subtopics": [
          {
            "id": "ancient-greek-3-0",
            "name": "Investigate a significant but manageable aspect of…"
          },
          {
            "id": "ancient-greek-3-1",
            "name": "Research Ancient Greek texts and process linguistic…"
          },
          {
            "id": "ancient-greek-3-2",
            "name": "Synthesise and evaluate information and make an…"
          },
          {
            "id": "ancient-greek-3-3",
            "name": "Explore the broader context of the classical world"
          }
        ]
      }
    ]
  },
  {
    "id": "hebrew-studies",
    "name": "Hebrew Studies",
    "category": "language",
    "levels": [
      "higher",
      "ordinary"
    ],
    "strands": [
      {
        "id": "hebrew-studies-0",
        "name": "Section A",
        "subtopics": [
          {
            "id": "hebrew-studies-0-0",
            "name": "Family"
          },
          {
            "id": "hebrew-studies-0-1",
            "name": "Family — Old Testament texts"
          },
          {
            "id": "hebrew-studies-0-2",
            "name": "Family — Mishnah texts: Ta'Anit 4m.8; Av 5m.21 (first…"
          },
          {
            "id": "hebrew-studies-0-3",
            "name": "Government and Monarchy"
          },
          {
            "id": "hebrew-studies-0-4",
            "name": "Government and Monarchy — Old Testament texts: Gen…"
          },
          {
            "id": "hebrew-studies-0-5",
            "name": "Government and Monarchy — Mishnah texts: Av 3m.2…"
          }
        ]
      },
      {
        "id": "hebrew-studies-1",
        "name": "Section B",
        "subtopics": [
          {
            "id": "hebrew-studies-1-0",
            "name": "Prophetic Protest"
          },
          {
            "id": "hebrew-studies-1-1",
            "name": "Prophetic Protest — Old Testament texts: 2 Sam…"
          },
          {
            "id": "hebrew-studies-1-2",
            "name": "Prophetic Protest — Mishnah texts"
          },
          {
            "id": "hebrew-studies-1-3",
            "name": "Wisdom"
          },
          {
            "id": "hebrew-studies-1-4",
            "name": "Wisdom — Old Testament texts: Prov 2.1-8; 24.13-34…"
          },
          {
            "id": "hebrew-studies-1-5",
            "name": "Wisdom — Mishnah texts"
          },
          {
            "id": "hebrew-studies-1-6",
            "name": "Wisdom — Additional reading: Job; 1 Kings 3.5-14…"
          }
        ]
      },
      {
        "id": "hebrew-studies-2",
        "name": "Section C",
        "subtopics": [
          {
            "id": "hebrew-studies-2-0",
            "name": "Worship — the role and development of worship; the…"
          },
          {
            "id": "hebrew-studies-2-1",
            "name": "Worship — Old Testament texts: Num 6.22-27; Deut…"
          },
          {
            "id": "hebrew-studies-2-2",
            "name": "Worship — Mishnah texts"
          },
          {
            "id": "hebrew-studies-2-3",
            "name": "Festivals and Symbols"
          },
          {
            "id": "hebrew-studies-2-4",
            "name": "Festivals and Symbols — Old Testament texts: Ex 12…"
          },
          {
            "id": "hebrew-studies-2-5",
            "name": "Festivals and Symbols — Mishnah texts"
          }
        ]
      },
      {
        "id": "hebrew-studies-3",
        "name": "Section D",
        "subtopics": [
          {
            "id": "hebrew-studies-3-0",
            "name": "Election and Covenant"
          },
          {
            "id": "hebrew-studies-3-1",
            "name": "Election and Covenant — Old Testament texts"
          },
          {
            "id": "hebrew-studies-3-2",
            "name": "Election and Covenant — Mishnah texts: Av 1m.1…"
          },
          {
            "id": "hebrew-studies-3-3",
            "name": "Messianism"
          },
          {
            "id": "hebrew-studies-3-4",
            "name": "Messianism — Old Testament texts: Deut 30.1-10; Is…"
          },
          {
            "id": "hebrew-studies-3-5",
            "name": "Messianism — Mishnah texts: Ber 1m.5; Sot 9m.15"
          }
        ]
      }
    ]
  },
  {
    "id": "arabic",
    "name": "Arabic",
    "category": "language",
    "levels": [
      "higher",
      "ordinary"
    ],
    "strands": [
      {
        "id": "arabic-0",
        "name": "Strand 1: Communicative Language Competence",
        "subtopics": [
          {
            "id": "arabic-0-0",
            "name": "Reception"
          },
          {
            "id": "arabic-0-1",
            "name": "Interaction"
          },
          {
            "id": "arabic-0-2",
            "name": "Production"
          },
          {
            "id": "arabic-0-3",
            "name": "Mediation"
          }
        ]
      },
      {
        "id": "arabic-1",
        "name": "Strand 2: Plurilingual and Pluricultural Competence Strand",
        "subtopics": [
          {
            "id": "arabic-1-0",
            "name": "Plurilingual Competence"
          },
          {
            "id": "arabic-1-1",
            "name": "Pluricultural Competence"
          }
        ]
      },
      {
        "id": "arabic-2",
        "name": "Assessment for Certification (new specification, 2025 intake onward)",
        "subtopics": [
          {
            "id": "arabic-2-0",
            "name": "Oral examination - additional assessment component"
          },
          {
            "id": "arabic-2-1",
            "name": "Aural examination - additional assessment component"
          },
          {
            "id": "arabic-2-2",
            "name": "Written examination - Reading"
          },
          {
            "id": "arabic-2-3",
            "name": "Written examination - Writing"
          },
          {
            "id": "arabic-2-4",
            "name": "Language Portfolio"
          }
        ]
      },
      {
        "id": "arabic-3",
        "name": "Interim Syllabus: Reading and Directed Writing",
        "subtopics": [
          {
            "id": "arabic-3-0",
            "name": "Understanding and conveying information; ordering and…"
          },
          {
            "id": "arabic-3-1",
            "name": "Evaluating information and selecting what is relevant…"
          },
          {
            "id": "arabic-3-2",
            "name": "Scanning for and extracting specific information…"
          },
          {
            "id": "arabic-3-3",
            "name": "Identifying main and subordinate topics; summarising…"
          },
          {
            "id": "arabic-3-4",
            "name": "Recognising and responding to linguistic devices…"
          },
          {
            "id": "arabic-3-5",
            "name": "Higher level"
          }
        ]
      },
      {
        "id": "arabic-4",
        "name": "Interim Syllabus: Continuous Writing",
        "subtopics": [
          {
            "id": "arabic-4-0",
            "name": "Articulating experience and expressing what is felt…"
          },
          {
            "id": "arabic-4-1",
            "name": "Demonstrating adequate control of vocabulary, syntax…"
          },
          {
            "id": "arabic-4-2",
            "name": "Expressing thoughts, feelings and opinions to…"
          },
          {
            "id": "arabic-4-3",
            "name": "Higher level: Wider sense of audience and context…"
          }
        ]
      },
      {
        "id": "arabic-5",
        "name": "Interim Syllabus: Use of Language",
        "subtopics": [
          {
            "id": "arabic-5-0",
            "name": "Exercising control of appropriate grammatical…"
          },
          {
            "id": "arabic-5-1",
            "name": "Conventions of paragraphing, sentence structure and…"
          },
          {
            "id": "arabic-5-2",
            "name": "Understanding and employing a range of apt vocabulary"
          },
          {
            "id": "arabic-5-3",
            "name": "Sense of audience and awareness of register and style…"
          },
          {
            "id": "arabic-5-4",
            "name": "Writing accurate simple/complex sentences; varied…"
          }
        ]
      },
      {
        "id": "arabic-6",
        "name": "Interim Syllabus: Literature (Prescribed Texts)",
        "subtopics": [
          {
            "id": "arabic-6-0",
            "name": "Extract from the Koran (Qur'an)"
          },
          {
            "id": "arabic-6-1",
            "name": "Classical Arabic verse"
          },
          {
            "id": "arabic-6-2",
            "name": "Extract from a work of modern Arabic prose"
          },
          {
            "id": "arabic-6-3",
            "name": "Understanding and commenting on set texts"
          }
        ]
      },
      {
        "id": "arabic-7",
        "name": "Interim Syllabus: Reading Comprehension (unseen texts)",
        "subtopics": [
          {
            "id": "arabic-7-0",
            "name": "Letters, newspaper or magazine articles, and works of…"
          },
          {
            "id": "arabic-7-1",
            "name": "Exploring levels of meaning within a text; awareness…"
          }
        ]
      },
      {
        "id": "arabic-8",
        "name": "Interim Syllabus: Assessment / Mark Allocation (current June examinations)",
        "subtopics": [
          {
            "id": "arabic-8-0",
            "name": "Reading comprehension - 20%"
          },
          {
            "id": "arabic-8-1",
            "name": "Literature - 35%"
          },
          {
            "id": "arabic-8-2",
            "name": "Usage - 20%"
          },
          {
            "id": "arabic-8-3",
            "name": "Continuous writing - 25%"
          }
        ]
      }
    ]
  },
  {
    "id": "classical-studies",
    "name": "Classical Studies",
    "category": "language",
    "levels": [
      "higher",
      "ordinary"
    ],
    "strands": [
      {
        "id": "classical-studies-0",
        "name": "Strand 1: The world of heroes",
        "subtopics": [
          {
            "id": "classical-studies-0-0",
            "name": "Characteristics and types of heroes and leaders"
          },
          {
            "id": "classical-studies-0-1",
            "name": "Heroic society"
          },
          {
            "id": "classical-studies-0-2",
            "name": "Heroic narratives"
          },
          {
            "id": "classical-studies-0-3",
            "name": "Homer's Odyssey"
          },
          {
            "id": "classical-studies-0-4",
            "name": "Virgil's Aeneid, with emphasis on Books 1-6"
          }
        ]
      },
      {
        "id": "classical-studies-1",
        "name": "Strand 2: Drama and spectacle",
        "subtopics": [
          {
            "id": "classical-studies-1-0",
            "name": "Greek tragedy"
          },
          {
            "id": "classical-studies-1-1",
            "name": "The context of Greek tragedy"
          },
          {
            "id": "classical-studies-1-2",
            "name": "Prescribed tragedy"
          },
          {
            "id": "classical-studies-1-3",
            "name": "The Colosseum, the Circus Maximus and Roman spectacle"
          }
        ]
      },
      {
        "id": "classical-studies-2",
        "name": "Strand 3: Power and identity",
        "subtopics": [
          {
            "id": "classical-studies-2-0",
            "name": "The time of Alexander or Caesar"
          },
          {
            "id": "classical-studies-2-1",
            "name": "The political and military exploits of Alexander or…"
          },
          {
            "id": "classical-studies-2-2",
            "name": "The characterisation of Alexander or Caesar"
          },
          {
            "id": "classical-studies-2-3",
            "name": "The attitudes of Alexander and Caesar towards foreign…"
          },
          {
            "id": "classical-studies-2-4",
            "name": "Prescribed literary sources"
          }
        ]
      },
      {
        "id": "classical-studies-3",
        "name": "Strand 4: Gods and humans",
        "subtopics": [
          {
            "id": "classical-studies-3-0",
            "name": "The Greek and Roman gods"
          },
          {
            "id": "classical-studies-3-1",
            "name": "The Athenian Parthenon and Erechtheion and the Roman…"
          },
          {
            "id": "classical-studies-3-2",
            "name": "Greek and Roman funerary practices and the afterlife"
          },
          {
            "id": "classical-studies-3-3",
            "name": "Philosophical ideas about mortality and living well"
          }
        ]
      }
    ]
  },
  {
    "id": "lithuanian",
    "name": "Lithuanian (non-curricular EU language)",
    "category": "language",
    "levels": [
      "higher"
    ],
    "strands": [
      {
        "id": "lithuanian-0",
        "name": "Communicative Language Competence",
        "subtopics": [
          {
            "id": "lithuanian-0-0",
            "name": "Reception"
          },
          {
            "id": "lithuanian-0-1",
            "name": "Interaction"
          },
          {
            "id": "lithuanian-0-2",
            "name": "Production"
          },
          {
            "id": "lithuanian-0-3",
            "name": "Mediation"
          }
        ]
      },
      {
        "id": "lithuanian-1",
        "name": "Plurilingual and Pluricultural Competence",
        "subtopics": [
          {
            "id": "lithuanian-1-0",
            "name": "Plurilingual competence: Making sense of unfamiliar…"
          },
          {
            "id": "lithuanian-1-1",
            "name": "Pluricultural competence"
          }
        ]
      }
    ]
  },
  {
    "id": "polish",
    "name": "Polish (non-curricular EU language)",
    "category": "language",
    "levels": [
      "higher"
    ],
    "strands": [
      {
        "id": "polish-0",
        "name": "Communicative Language Competence",
        "subtopics": [
          {
            "id": "polish-0-0",
            "name": "Reception"
          },
          {
            "id": "polish-0-1",
            "name": "Interaction"
          },
          {
            "id": "polish-0-2",
            "name": "Production"
          },
          {
            "id": "polish-0-3",
            "name": "Mediation"
          }
        ]
      },
      {
        "id": "polish-1",
        "name": "Plurilingual and Pluricultural Competence",
        "subtopics": [
          {
            "id": "polish-1-0",
            "name": "Plurilingual competence"
          },
          {
            "id": "polish-1-1",
            "name": "Pluricultural competence"
          }
        ]
      },
      {
        "id": "polish-2",
        "name": "Assessment Components and Language Portfolio",
        "subtopics": [
          {
            "id": "polish-2-0",
            "name": "Oral examination - spoken reception, interaction…"
          },
          {
            "id": "polish-2-1",
            "name": "Aural examination - listening reception and mediation"
          },
          {
            "id": "polish-2-2",
            "name": "Written examination - Reading - written reception…"
          },
          {
            "id": "polish-2-3",
            "name": "Written examination - Writing - written production…"
          },
          {
            "id": "polish-2-4",
            "name": "Language Portfolio - record and reflect on language…"
          }
        ]
      }
    ]
  },
  {
    "id": "portuguese",
    "name": "Portuguese (non-curricular EU language)",
    "category": "language",
    "levels": [
      "higher"
    ],
    "strands": [
      {
        "id": "portuguese-0",
        "name": "Communicative Language Competence",
        "subtopics": [
          {
            "id": "portuguese-0-0",
            "name": "Reception"
          },
          {
            "id": "portuguese-0-1",
            "name": "Interaction"
          },
          {
            "id": "portuguese-0-2",
            "name": "Production"
          },
          {
            "id": "portuguese-0-3",
            "name": "Mediation"
          }
        ]
      },
      {
        "id": "portuguese-1",
        "name": "Plurilingual and Pluricultural Competence",
        "subtopics": [
          {
            "id": "portuguese-1-0",
            "name": "Plurilingual competence"
          },
          {
            "id": "portuguese-1-1",
            "name": "Pluricultural competence"
          }
        ]
      }
    ]
  },
  {
    "id": "mathematics",
    "name": "Mathematics",
    "category": "stem",
    "levels": [
      "higher",
      "ordinary",
      "foundation"
    ],
    "strands": [
      {
        "id": "mathematics-0",
        "name": "Strand 1: Statistics and Probability",
        "subtopics": [
          {
            "id": "mathematics-0-0",
            "name": "Counting"
          },
          {
            "id": "mathematics-0-1",
            "name": "Concepts of probability"
          },
          {
            "id": "mathematics-0-2",
            "name": "Outcomes of random processes"
          },
          {
            "id": "mathematics-0-3",
            "name": "Statistical reasoning with an aim to becoming a…"
          },
          {
            "id": "mathematics-0-4",
            "name": "Finding, collecting and organising data"
          },
          {
            "id": "mathematics-0-5",
            "name": "Representing data graphically and numerically"
          },
          {
            "id": "mathematics-0-6",
            "name": "Analysing, interpreting and drawing inferences from…"
          }
        ]
      },
      {
        "id": "mathematics-1",
        "name": "Strand 2: Geometry and Trigonometry",
        "subtopics": [
          {
            "id": "mathematics-1-0",
            "name": "Synthetic geometry"
          },
          {
            "id": "mathematics-1-1",
            "name": "Co-ordinate geometry"
          },
          {
            "id": "mathematics-1-2",
            "name": "Trigonometry"
          },
          {
            "id": "mathematics-1-3",
            "name": "Transformation geometry, enlargements"
          }
        ]
      },
      {
        "id": "mathematics-2",
        "name": "Strand 3: Number",
        "subtopics": [
          {
            "id": "mathematics-2-0",
            "name": "Number systems"
          },
          {
            "id": "mathematics-2-1",
            "name": "Indices"
          },
          {
            "id": "mathematics-2-2",
            "name": "Arithmetic"
          },
          {
            "id": "mathematics-2-3",
            "name": "Length, area and volume"
          }
        ]
      },
      {
        "id": "mathematics-3",
        "name": "Strand 4: Algebra",
        "subtopics": [
          {
            "id": "mathematics-3-0",
            "name": "Expressions"
          },
          {
            "id": "mathematics-3-1",
            "name": "Solving equations"
          },
          {
            "id": "mathematics-3-2",
            "name": "Inequalities"
          },
          {
            "id": "mathematics-3-3",
            "name": "Complex Numbers"
          }
        ]
      },
      {
        "id": "mathematics-4",
        "name": "Strand 5: Functions",
        "subtopics": [
          {
            "id": "mathematics-4-0",
            "name": "Functions"
          },
          {
            "id": "mathematics-4-1",
            "name": "Calculus"
          }
        ]
      }
    ]
  },
  {
    "id": "applied-mathematics",
    "name": "Applied Mathematics",
    "category": "stem",
    "levels": [
      "higher",
      "ordinary"
    ],
    "strands": [
      {
        "id": "applied-mathematics-0",
        "name": "Strand 1: Statistics and Probability",
        "subtopics": [
          {
            "id": "applied-mathematics-0-0",
            "name": "Counting"
          },
          {
            "id": "applied-mathematics-0-1",
            "name": "Concepts of probability"
          },
          {
            "id": "applied-mathematics-0-2",
            "name": "Outcomes of random processes"
          },
          {
            "id": "applied-mathematics-0-3",
            "name": "Statistical reasoning with an aim to becoming a…"
          },
          {
            "id": "applied-mathematics-0-4",
            "name": "Finding, collecting and organising data"
          },
          {
            "id": "applied-mathematics-0-5",
            "name": "Representing data graphically and numerically"
          },
          {
            "id": "applied-mathematics-0-6",
            "name": "Analysing, interpreting and drawing inferences from…"
          }
        ]
      },
      {
        "id": "applied-mathematics-1",
        "name": "Strand 2: Geometry and Trigonometry",
        "subtopics": [
          {
            "id": "applied-mathematics-1-0",
            "name": "Synthetic geometry"
          },
          {
            "id": "applied-mathematics-1-1",
            "name": "Co-ordinate geometry"
          },
          {
            "id": "applied-mathematics-1-2",
            "name": "Trigonometry"
          },
          {
            "id": "applied-mathematics-1-3",
            "name": "Transformation geometry, enlargements"
          }
        ]
      },
      {
        "id": "applied-mathematics-2",
        "name": "Strand 3: Number",
        "subtopics": [
          {
            "id": "applied-mathematics-2-0",
            "name": "Number systems"
          },
          {
            "id": "applied-mathematics-2-1",
            "name": "Indices"
          },
          {
            "id": "applied-mathematics-2-2",
            "name": "Arithmetic"
          },
          {
            "id": "applied-mathematics-2-3",
            "name": "Length, area and volume"
          }
        ]
      },
      {
        "id": "applied-mathematics-3",
        "name": "Strand 4: Algebra",
        "subtopics": [
          {
            "id": "applied-mathematics-3-0",
            "name": "Expressions"
          },
          {
            "id": "applied-mathematics-3-1",
            "name": "Solving equations"
          },
          {
            "id": "applied-mathematics-3-2",
            "name": "Inequalities"
          },
          {
            "id": "applied-mathematics-3-3",
            "name": "Complex Numbers"
          }
        ]
      },
      {
        "id": "applied-mathematics-4",
        "name": "Strand 5: Functions",
        "subtopics": [
          {
            "id": "applied-mathematics-4-0",
            "name": "Functions"
          },
          {
            "id": "applied-mathematics-4-1",
            "name": "Calculus"
          }
        ]
      }
    ]
  },
  {
    "id": "physics",
    "name": "Physics",
    "category": "stem",
    "levels": [
      "higher",
      "ordinary"
    ],
    "strands": [
      {
        "id": "physics-0",
        "name": "Mechanics",
        "subtopics": [
          {
            "id": "physics-0-0",
            "name": "Linear motion"
          },
          {
            "id": "physics-0-1",
            "name": "Vectors and scalars"
          },
          {
            "id": "physics-0-2",
            "name": "Newton's laws of motion"
          },
          {
            "id": "physics-0-3",
            "name": "Conservation of momentum"
          },
          {
            "id": "physics-0-4",
            "name": "Gravity"
          },
          {
            "id": "physics-0-5",
            "name": "Density and pressure"
          },
          {
            "id": "physics-0-6",
            "name": "Moments"
          },
          {
            "id": "physics-0-7",
            "name": "Conditions for equilibrium"
          },
          {
            "id": "physics-0-8",
            "name": "Work"
          },
          {
            "id": "physics-0-9",
            "name": "Energy"
          },
          {
            "id": "physics-0-10",
            "name": "Power"
          },
          {
            "id": "physics-0-11",
            "name": "Circular motion (Higher Level)"
          },
          {
            "id": "physics-0-12",
            "name": "Simple harmonic motion and Hooke's law (Higher Level)"
          }
        ]
      },
      {
        "id": "physics-1",
        "name": "Temperature",
        "subtopics": [
          {
            "id": "physics-1-0",
            "name": "Concept of temperature"
          },
          {
            "id": "physics-1-1",
            "name": "Thermometric property"
          },
          {
            "id": "physics-1-2",
            "name": "Thermometers and temperature scales"
          }
        ]
      },
      {
        "id": "physics-2",
        "name": "Heat",
        "subtopics": [
          {
            "id": "physics-2-0",
            "name": "Concept of heat"
          },
          {
            "id": "physics-2-1",
            "name": "Heat capacity and specific heat capacity"
          },
          {
            "id": "physics-2-2",
            "name": "Latent heat and specific latent heat"
          },
          {
            "id": "physics-2-3",
            "name": "Heat transfer: Conduction"
          },
          {
            "id": "physics-2-4",
            "name": "Heat transfer: Convection"
          },
          {
            "id": "physics-2-5",
            "name": "Heat transfer: Radiation"
          }
        ]
      },
      {
        "id": "physics-3",
        "name": "Waves",
        "subtopics": [
          {
            "id": "physics-3-0",
            "name": "Properties of waves"
          },
          {
            "id": "physics-3-1",
            "name": "Wave phenomena"
          },
          {
            "id": "physics-3-2",
            "name": "Doppler effect"
          }
        ]
      },
      {
        "id": "physics-4",
        "name": "Vibrations and Sound",
        "subtopics": [
          {
            "id": "physics-4-0",
            "name": "Wave nature of sound"
          },
          {
            "id": "physics-4-1",
            "name": "Characteristics of notes"
          },
          {
            "id": "physics-4-2",
            "name": "Resonance"
          },
          {
            "id": "physics-4-3",
            "name": "Vibrations in strings and pipes"
          },
          {
            "id": "physics-4-4",
            "name": "Sound intensity and sound intensity level"
          }
        ]
      },
      {
        "id": "physics-5",
        "name": "Light",
        "subtopics": [
          {
            "id": "physics-5-0",
            "name": "Laws of reflection"
          },
          {
            "id": "physics-5-1",
            "name": "Mirrors"
          },
          {
            "id": "physics-5-2",
            "name": "Laws of refraction"
          },
          {
            "id": "physics-5-3",
            "name": "Total internal reflection"
          },
          {
            "id": "physics-5-4",
            "name": "Lenses"
          },
          {
            "id": "physics-5-5",
            "name": "Diffraction and interference"
          },
          {
            "id": "physics-5-6",
            "name": "Light as a transverse wave motion (polarisation)"
          },
          {
            "id": "physics-5-7",
            "name": "Dispersion"
          },
          {
            "id": "physics-5-8",
            "name": "Colours"
          },
          {
            "id": "physics-5-9",
            "name": "Electromagnetic spectrum"
          },
          {
            "id": "physics-5-10",
            "name": "The spectrometer"
          }
        ]
      },
      {
        "id": "physics-6",
        "name": "Electricity",
        "subtopics": [
          {
            "id": "physics-6-0",
            "name": "Electrification by contact / friction"
          },
          {
            "id": "physics-6-1",
            "name": "Electrification by induction"
          },
          {
            "id": "physics-6-2",
            "name": "Distribution of charge on conductors"
          },
          {
            "id": "physics-6-3",
            "name": "The electroscope"
          },
          {
            "id": "physics-6-4",
            "name": "Force between charges"
          },
          {
            "id": "physics-6-5",
            "name": "Electric fields"
          },
          {
            "id": "physics-6-6",
            "name": "Potential difference"
          },
          {
            "id": "physics-6-7",
            "name": "Capacitors and capacitance"
          },
          {
            "id": "physics-6-8",
            "name": "Electric current"
          },
          {
            "id": "physics-6-9",
            "name": "Sources of emf and electric current"
          },
          {
            "id": "physics-6-10",
            "name": "Conduction in materials"
          },
          {
            "id": "physics-6-11",
            "name": "Resistance"
          },
          {
            "id": "physics-6-12",
            "name": "Effects of an electric current"
          },
          {
            "id": "physics-6-13",
            "name": "Domestic circuits and electrical safety"
          },
          {
            "id": "physics-6-14",
            "name": "Magnetism and magnetic fields"
          },
          {
            "id": "physics-6-15",
            "name": "Current in a magnetic field"
          },
          {
            "id": "physics-6-16",
            "name": "Electromagnetic induction"
          },
          {
            "id": "physics-6-17",
            "name": "Alternating current"
          },
          {
            "id": "physics-6-18",
            "name": "Mutual and self-induction"
          }
        ]
      },
      {
        "id": "physics-7",
        "name": "Modern Physics",
        "subtopics": [
          {
            "id": "physics-7-0",
            "name": "The electron"
          },
          {
            "id": "physics-7-1",
            "name": "Thermionic emission"
          },
          {
            "id": "physics-7-2",
            "name": "Photoelectric emission"
          },
          {
            "id": "physics-7-3",
            "name": "X-rays"
          },
          {
            "id": "physics-7-4",
            "name": "Structure of the atom"
          },
          {
            "id": "physics-7-5",
            "name": "Structure of the nucleus"
          },
          {
            "id": "physics-7-6",
            "name": "Radioactivity"
          },
          {
            "id": "physics-7-7",
            "name": "Nuclear energy"
          },
          {
            "id": "physics-7-8",
            "name": "Ionising radiation, its hazards and uses"
          },
          {
            "id": "physics-7-9",
            "name": "Particle Physics"
          }
        ]
      }
    ]
  },
  {
    "id": "chemistry",
    "name": "Chemistry",
    "category": "stem",
    "levels": [
      "higher",
      "ordinary"
    ],
    "strands": [
      {
        "id": "chemistry-0",
        "name": "1. Periodic Table and Atomic Structure",
        "subtopics": [
          {
            "id": "chemistry-0-0",
            "name": "1.1 Periodic Table"
          },
          {
            "id": "chemistry-0-1",
            "name": "1.2 Atomic Structure"
          },
          {
            "id": "chemistry-0-2",
            "name": "1.3 Radioactivity"
          },
          {
            "id": "chemistry-0-3",
            "name": "1.4 Electronic Structure of Atoms"
          },
          {
            "id": "chemistry-0-4",
            "name": "1.5 Oxidation and Reduction"
          }
        ]
      },
      {
        "id": "chemistry-1",
        "name": "2. Chemical Bonding",
        "subtopics": [
          {
            "id": "chemistry-1-0",
            "name": "2.1 Chemical Compounds"
          },
          {
            "id": "chemistry-1-1",
            "name": "2.2 Ionic Bonding"
          },
          {
            "id": "chemistry-1-2",
            "name": "2.3 Covalent Bonding"
          },
          {
            "id": "chemistry-1-3",
            "name": "2.4 Electronegativity"
          },
          {
            "id": "chemistry-1-4",
            "name": "2.5 Shapes of Molecules and Intermolecular Forces"
          },
          {
            "id": "chemistry-1-5",
            "name": "2.6 Oxidation Numbers"
          }
        ]
      },
      {
        "id": "chemistry-2",
        "name": "3. Stoichiometry, Formulas and Equations",
        "subtopics": [
          {
            "id": "chemistry-2-0",
            "name": "3.1 States of Matter"
          },
          {
            "id": "chemistry-2-1",
            "name": "3.2 Gas Laws"
          },
          {
            "id": "chemistry-2-2",
            "name": "3.3 The Mole"
          },
          {
            "id": "chemistry-2-3",
            "name": "3.4 Chemical Formulas"
          },
          {
            "id": "chemistry-2-4",
            "name": "3.5 Chemical Equations"
          }
        ]
      },
      {
        "id": "chemistry-3",
        "name": "4. Volumetric Analysis",
        "subtopics": [
          {
            "id": "chemistry-3-0",
            "name": "4.1 Concentration of Solutions"
          },
          {
            "id": "chemistry-3-1",
            "name": "4.2 Acids and Bases"
          },
          {
            "id": "chemistry-3-2",
            "name": "4.3 Volumetric Analysis"
          }
        ]
      },
      {
        "id": "chemistry-4",
        "name": "5. Fuels and Heats of Reaction",
        "subtopics": [
          {
            "id": "chemistry-4-0",
            "name": "5.1 Sources of Hydrocarbons"
          },
          {
            "id": "chemistry-4-1",
            "name": "5.2 Structure of Aliphatic Hydrocarbons"
          },
          {
            "id": "chemistry-4-2",
            "name": "5.3 Aromatic Hydrocarbons"
          },
          {
            "id": "chemistry-4-3",
            "name": "5.4 Exothermic and Endothermic Reactions"
          },
          {
            "id": "chemistry-4-4",
            "name": "5.5 Oil Refining and its Products"
          },
          {
            "id": "chemistry-4-5",
            "name": "5.6 Other Chemical Fuels"
          }
        ]
      },
      {
        "id": "chemistry-5",
        "name": "6. Rates of Reaction",
        "subtopics": [
          {
            "id": "chemistry-5-0",
            "name": "6.1 Reaction Rates"
          },
          {
            "id": "chemistry-5-1",
            "name": "6.2 Factors Affecting Rates of Reaction"
          }
        ]
      },
      {
        "id": "chemistry-6",
        "name": "7. Organic Chemistry",
        "subtopics": [
          {
            "id": "chemistry-6-0",
            "name": "7.1 Tetrahedral Carbon"
          },
          {
            "id": "chemistry-6-1",
            "name": "7.2 Planar Carbon"
          },
          {
            "id": "chemistry-6-2",
            "name": "7.3 Organic Chemical Reaction Types"
          },
          {
            "id": "chemistry-6-3",
            "name": "7.4 Organic Natural Products"
          },
          {
            "id": "chemistry-6-4",
            "name": "7.5 Chromatography"
          }
        ]
      },
      {
        "id": "chemistry-7",
        "name": "8. Chemical Equilibrium",
        "subtopics": [
          {
            "id": "chemistry-7-0",
            "name": "8.1 Chemical Equilibrium"
          },
          {
            "id": "chemistry-7-1",
            "name": "8.2 Le Chatelier's Principle"
          }
        ]
      },
      {
        "id": "chemistry-8",
        "name": "9. Environmental Chemistry: Water",
        "subtopics": [
          {
            "id": "chemistry-8-0",
            "name": "9.1 pH Scale"
          },
          {
            "id": "chemistry-8-1",
            "name": "9.2 Hardness in Water"
          },
          {
            "id": "chemistry-8-2",
            "name": "9.3 Water Treatment"
          },
          {
            "id": "chemistry-8-3",
            "name": "9.4 Water Analysis"
          }
        ]
      },
      {
        "id": "chemistry-9",
        "name": "Option 1A: Additional Industrial Chemistry",
        "subtopics": [
          {
            "id": "chemistry-9-0",
            "name": "1A.1 General Principles"
          },
          {
            "id": "chemistry-9-1",
            "name": "1A.2 Case Study"
          }
        ]
      },
      {
        "id": "chemistry-10",
        "name": "Option 1B: Atmospheric Chemistry",
        "subtopics": [
          {
            "id": "chemistry-10-0",
            "name": "1B.1 Oxygen"
          },
          {
            "id": "chemistry-10-1",
            "name": "1B.2 Nitrogen"
          },
          {
            "id": "chemistry-10-2",
            "name": "1B.3 Carbon Dioxide"
          },
          {
            "id": "chemistry-10-3",
            "name": "1B.4 Atmospheric Pollution"
          },
          {
            "id": "chemistry-10-4",
            "name": "1B.5 The Ozone Layer"
          }
        ]
      },
      {
        "id": "chemistry-11",
        "name": "Option 2A: Materials",
        "subtopics": [
          {
            "id": "chemistry-11-0",
            "name": "2A.1 Crystals"
          },
          {
            "id": "chemistry-11-1",
            "name": "2A.2 Addition Polymers"
          },
          {
            "id": "chemistry-11-2",
            "name": "2A.3 Metals"
          }
        ]
      },
      {
        "id": "chemistry-12",
        "name": "Option 2B: Additional Electrochemistry and the Extraction of Metals",
        "subtopics": [
          {
            "id": "chemistry-12-0",
            "name": "2B.1 The Electrochemical Series"
          },
          {
            "id": "chemistry-12-1",
            "name": "2B.2 Electrolysis of Molten Salts"
          },
          {
            "id": "chemistry-12-2",
            "name": "2B.3 Corrosion"
          },
          {
            "id": "chemistry-12-3",
            "name": "2B.4 Strongly Electropositive Metals (Na and Al)"
          },
          {
            "id": "chemistry-12-4",
            "name": "2B.5 d-Block Metals"
          }
        ]
      }
    ]
  },
  {
    "id": "physics-and-chemistry",
    "name": "Physics and Chemistry (combined)",
    "category": "stem",
    "levels": [
      "higher",
      "ordinary"
    ],
    "strands": [
      {
        "id": "physics-and-chemistry-0",
        "name": "Mechanics",
        "subtopics": [
          {
            "id": "physics-and-chemistry-0-0",
            "name": "Linear motion"
          },
          {
            "id": "physics-and-chemistry-0-1",
            "name": "Vectors and scalars"
          },
          {
            "id": "physics-and-chemistry-0-2",
            "name": "Newton's laws of motion"
          },
          {
            "id": "physics-and-chemistry-0-3",
            "name": "Conservation of momentum"
          },
          {
            "id": "physics-and-chemistry-0-4",
            "name": "Gravity"
          },
          {
            "id": "physics-and-chemistry-0-5",
            "name": "Density and pressure"
          },
          {
            "id": "physics-and-chemistry-0-6",
            "name": "Moments"
          },
          {
            "id": "physics-and-chemistry-0-7",
            "name": "Conditions for equilibrium"
          },
          {
            "id": "physics-and-chemistry-0-8",
            "name": "Work"
          },
          {
            "id": "physics-and-chemistry-0-9",
            "name": "Energy"
          },
          {
            "id": "physics-and-chemistry-0-10",
            "name": "Power"
          },
          {
            "id": "physics-and-chemistry-0-11",
            "name": "Circular motion (Higher Level)"
          },
          {
            "id": "physics-and-chemistry-0-12",
            "name": "Simple harmonic motion and Hooke's law (Higher Level)"
          }
        ]
      },
      {
        "id": "physics-and-chemistry-1",
        "name": "Temperature",
        "subtopics": [
          {
            "id": "physics-and-chemistry-1-0",
            "name": "Concept of temperature"
          },
          {
            "id": "physics-and-chemistry-1-1",
            "name": "Thermometric property"
          },
          {
            "id": "physics-and-chemistry-1-2",
            "name": "Thermometers and temperature scales"
          }
        ]
      },
      {
        "id": "physics-and-chemistry-2",
        "name": "Heat",
        "subtopics": [
          {
            "id": "physics-and-chemistry-2-0",
            "name": "Concept of heat"
          },
          {
            "id": "physics-and-chemistry-2-1",
            "name": "Heat capacity and specific heat capacity"
          },
          {
            "id": "physics-and-chemistry-2-2",
            "name": "Latent heat and specific latent heat"
          },
          {
            "id": "physics-and-chemistry-2-3",
            "name": "Heat transfer: Conduction"
          },
          {
            "id": "physics-and-chemistry-2-4",
            "name": "Heat transfer: Convection"
          },
          {
            "id": "physics-and-chemistry-2-5",
            "name": "Heat transfer: Radiation"
          }
        ]
      },
      {
        "id": "physics-and-chemistry-3",
        "name": "Waves",
        "subtopics": [
          {
            "id": "physics-and-chemistry-3-0",
            "name": "Properties of waves"
          },
          {
            "id": "physics-and-chemistry-3-1",
            "name": "Wave phenomena"
          },
          {
            "id": "physics-and-chemistry-3-2",
            "name": "Doppler effect"
          }
        ]
      },
      {
        "id": "physics-and-chemistry-4",
        "name": "Vibrations and Sound",
        "subtopics": [
          {
            "id": "physics-and-chemistry-4-0",
            "name": "Wave nature of sound"
          },
          {
            "id": "physics-and-chemistry-4-1",
            "name": "Characteristics of notes"
          },
          {
            "id": "physics-and-chemistry-4-2",
            "name": "Resonance"
          },
          {
            "id": "physics-and-chemistry-4-3",
            "name": "Vibrations in strings and pipes"
          },
          {
            "id": "physics-and-chemistry-4-4",
            "name": "Sound intensity and sound intensity level"
          }
        ]
      },
      {
        "id": "physics-and-chemistry-5",
        "name": "Light",
        "subtopics": [
          {
            "id": "physics-and-chemistry-5-0",
            "name": "Laws of reflection"
          },
          {
            "id": "physics-and-chemistry-5-1",
            "name": "Mirrors"
          },
          {
            "id": "physics-and-chemistry-5-2",
            "name": "Laws of refraction"
          },
          {
            "id": "physics-and-chemistry-5-3",
            "name": "Total internal reflection"
          },
          {
            "id": "physics-and-chemistry-5-4",
            "name": "Lenses"
          },
          {
            "id": "physics-and-chemistry-5-5",
            "name": "Diffraction and interference"
          },
          {
            "id": "physics-and-chemistry-5-6",
            "name": "Light as a transverse wave motion (polarisation)"
          },
          {
            "id": "physics-and-chemistry-5-7",
            "name": "Dispersion"
          },
          {
            "id": "physics-and-chemistry-5-8",
            "name": "Colours"
          },
          {
            "id": "physics-and-chemistry-5-9",
            "name": "Electromagnetic spectrum"
          },
          {
            "id": "physics-and-chemistry-5-10",
            "name": "The spectrometer"
          }
        ]
      },
      {
        "id": "physics-and-chemistry-6",
        "name": "Electricity",
        "subtopics": [
          {
            "id": "physics-and-chemistry-6-0",
            "name": "Electrification by contact / friction"
          },
          {
            "id": "physics-and-chemistry-6-1",
            "name": "Electrification by induction"
          },
          {
            "id": "physics-and-chemistry-6-2",
            "name": "Distribution of charge on conductors"
          },
          {
            "id": "physics-and-chemistry-6-3",
            "name": "The electroscope"
          },
          {
            "id": "physics-and-chemistry-6-4",
            "name": "Force between charges"
          },
          {
            "id": "physics-and-chemistry-6-5",
            "name": "Electric fields"
          },
          {
            "id": "physics-and-chemistry-6-6",
            "name": "Potential difference"
          },
          {
            "id": "physics-and-chemistry-6-7",
            "name": "Capacitors and capacitance"
          },
          {
            "id": "physics-and-chemistry-6-8",
            "name": "Electric current"
          },
          {
            "id": "physics-and-chemistry-6-9",
            "name": "Sources of emf and electric current"
          },
          {
            "id": "physics-and-chemistry-6-10",
            "name": "Conduction in materials"
          },
          {
            "id": "physics-and-chemistry-6-11",
            "name": "Resistance"
          },
          {
            "id": "physics-and-chemistry-6-12",
            "name": "Effects of an electric current"
          },
          {
            "id": "physics-and-chemistry-6-13",
            "name": "Domestic circuits and electrical safety"
          },
          {
            "id": "physics-and-chemistry-6-14",
            "name": "Magnetism and magnetic fields"
          },
          {
            "id": "physics-and-chemistry-6-15",
            "name": "Current in a magnetic field"
          },
          {
            "id": "physics-and-chemistry-6-16",
            "name": "Electromagnetic induction"
          },
          {
            "id": "physics-and-chemistry-6-17",
            "name": "Alternating current"
          },
          {
            "id": "physics-and-chemistry-6-18",
            "name": "Mutual and self-induction"
          }
        ]
      },
      {
        "id": "physics-and-chemistry-7",
        "name": "Modern Physics",
        "subtopics": [
          {
            "id": "physics-and-chemistry-7-0",
            "name": "The electron"
          },
          {
            "id": "physics-and-chemistry-7-1",
            "name": "Thermionic emission"
          },
          {
            "id": "physics-and-chemistry-7-2",
            "name": "Photoelectric emission"
          },
          {
            "id": "physics-and-chemistry-7-3",
            "name": "X-rays"
          },
          {
            "id": "physics-and-chemistry-7-4",
            "name": "Structure of the atom"
          },
          {
            "id": "physics-and-chemistry-7-5",
            "name": "Structure of the nucleus"
          },
          {
            "id": "physics-and-chemistry-7-6",
            "name": "Radioactivity"
          },
          {
            "id": "physics-and-chemistry-7-7",
            "name": "Nuclear energy"
          },
          {
            "id": "physics-and-chemistry-7-8",
            "name": "Ionising radiation, its hazards and uses"
          },
          {
            "id": "physics-and-chemistry-7-9",
            "name": "Particle Physics"
          }
        ]
      }
    ]
  },
  {
    "id": "biology",
    "name": "Biology",
    "category": "stem",
    "levels": [
      "higher",
      "ordinary"
    ],
    "strands": [
      {
        "id": "biology-0",
        "name": "Unit One: Biology - The Study of Life",
        "subtopics": [
          {
            "id": "biology-0-0",
            "name": "The Scientific Method"
          },
          {
            "id": "biology-0-1",
            "name": "The Characteristics of Life"
          },
          {
            "id": "biology-0-2",
            "name": "Nutrition"
          },
          {
            "id": "biology-0-3",
            "name": "General Principles of Ecology"
          },
          {
            "id": "biology-0-4",
            "name": "A Study of an Ecosystem"
          }
        ]
      },
      {
        "id": "biology-1",
        "name": "Unit Two: The Cell",
        "subtopics": [
          {
            "id": "biology-1-0",
            "name": "Cell Structure"
          },
          {
            "id": "biology-1-1",
            "name": "Cell Metabolism"
          },
          {
            "id": "biology-1-2",
            "name": "Cell Continuity"
          },
          {
            "id": "biology-1-3",
            "name": "Cell Diversity"
          },
          {
            "id": "biology-1-4",
            "name": "Genetics"
          }
        ]
      },
      {
        "id": "biology-2",
        "name": "Unit Three: The Organism",
        "subtopics": [
          {
            "id": "biology-2-0",
            "name": "Diversity of Organisms"
          },
          {
            "id": "biology-2-1",
            "name": "Organisation and the Vascular Structures"
          },
          {
            "id": "biology-2-2",
            "name": "Transport and Nutrition"
          },
          {
            "id": "biology-2-3",
            "name": "Breathing System and Excretion"
          },
          {
            "id": "biology-2-4",
            "name": "Responses to Stimuli"
          },
          {
            "id": "biology-2-5",
            "name": "Reproduction and Growth"
          }
        ]
      }
    ]
  },
  {
    "id": "agricultural-science",
    "name": "Agricultural Science",
    "category": "stem",
    "levels": [
      "higher",
      "ordinary"
    ],
    "strands": [
      {
        "id": "agricultural-science-0",
        "name": "Strand 1: Scientific practices",
        "subtopics": [
          {
            "id": "agricultural-science-0-0",
            "name": "Hypothesising"
          },
          {
            "id": "agricultural-science-0-1",
            "name": "Experimenting"
          },
          {
            "id": "agricultural-science-0-2",
            "name": "Evaluating evidence"
          },
          {
            "id": "agricultural-science-0-3",
            "name": "Communicating"
          },
          {
            "id": "agricultural-science-0-4",
            "name": "Working safely"
          }
        ]
      },
      {
        "id": "agricultural-science-1",
        "name": "Strand 2: Soils",
        "subtopics": [
          {
            "id": "agricultural-science-1-0",
            "name": "Formation and classification"
          },
          {
            "id": "agricultural-science-1-1",
            "name": "Properties"
          },
          {
            "id": "agricultural-science-1-2",
            "name": "Properties: Chemical"
          },
          {
            "id": "agricultural-science-1-3",
            "name": "Properties: Physical"
          },
          {
            "id": "agricultural-science-1-4",
            "name": "Properties: Biological"
          },
          {
            "id": "agricultural-science-1-5",
            "name": "Management"
          }
        ]
      },
      {
        "id": "agricultural-science-2",
        "name": "Strand 3: Crops",
        "subtopics": [
          {
            "id": "agricultural-science-2-0",
            "name": "Plant physiology"
          },
          {
            "id": "agricultural-science-2-1",
            "name": "Classification/identification"
          },
          {
            "id": "agricultural-science-2-2",
            "name": "Production"
          },
          {
            "id": "agricultural-science-2-3",
            "name": "Production: Establishment"
          },
          {
            "id": "agricultural-science-2-4",
            "name": "Production: Management"
          },
          {
            "id": "agricultural-science-2-5",
            "name": "Production: Harvesting"
          }
        ]
      },
      {
        "id": "agricultural-science-3",
        "name": "Strand 4: Animals",
        "subtopics": [
          {
            "id": "agricultural-science-3-0",
            "name": "Animal physiology"
          },
          {
            "id": "agricultural-science-3-1",
            "name": "Classification/identification"
          },
          {
            "id": "agricultural-science-3-2",
            "name": "Production"
          },
          {
            "id": "agricultural-science-3-3",
            "name": "Production: System/enterprise"
          },
          {
            "id": "agricultural-science-3-4",
            "name": "Production: Management"
          },
          {
            "id": "agricultural-science-3-5",
            "name": "Production: Animal husbandry and health"
          }
        ]
      }
    ]
  },
  {
    "id": "computer-science",
    "name": "Computer Science",
    "category": "stem",
    "levels": [
      "higher",
      "ordinary"
    ],
    "strands": [
      {
        "id": "computer-science-0",
        "name": "Strand 1: Practices and principles",
        "subtopics": [
          {
            "id": "computer-science-0-0",
            "name": "Computational thinking"
          },
          {
            "id": "computer-science-0-1",
            "name": "Problem solving"
          },
          {
            "id": "computer-science-0-2",
            "name": "Logical thinking"
          },
          {
            "id": "computer-science-0-3",
            "name": "Algorithmic thinking"
          },
          {
            "id": "computer-science-0-4",
            "name": "Modelling and simulation"
          },
          {
            "id": "computer-science-0-5",
            "name": "Heuristics"
          },
          {
            "id": "computer-science-0-6",
            "name": "Computers and society"
          },
          {
            "id": "computer-science-0-7",
            "name": "Social and ethical considerations of computing…"
          },
          {
            "id": "computer-science-0-8",
            "name": "Turing machines"
          },
          {
            "id": "computer-science-0-9",
            "name": "The Internet"
          },
          {
            "id": "computer-science-0-10",
            "name": "Machine learning"
          },
          {
            "id": "computer-science-0-11",
            "name": "Artificial intelligence"
          },
          {
            "id": "computer-science-0-12",
            "name": "User-centred design"
          },
          {
            "id": "computer-science-0-13",
            "name": "Adaptive technology and accessibility"
          },
          {
            "id": "computer-science-0-14",
            "name": "Diverse roles and careers that use computing…"
          },
          {
            "id": "computer-science-0-15",
            "name": "Designing and developing"
          },
          {
            "id": "computer-science-0-16",
            "name": "Design process"
          },
          {
            "id": "computer-science-0-17",
            "name": "Working in a team, assigning roles and…"
          },
          {
            "id": "computer-science-0-18",
            "name": "Communication and reporting"
          },
          {
            "id": "computer-science-0-19",
            "name": "Software development and management"
          }
        ]
      },
      {
        "id": "computer-science-1",
        "name": "Strand 2: Core concepts",
        "subtopics": [
          {
            "id": "computer-science-1-0",
            "name": "Abstraction"
          },
          {
            "id": "computer-science-1-1",
            "name": "Abstraction: Modular design and abstract models"
          },
          {
            "id": "computer-science-1-2",
            "name": "Algorithms"
          },
          {
            "id": "computer-science-1-3",
            "name": "Programming concepts"
          },
          {
            "id": "computer-science-1-4",
            "name": "Pseudo code"
          },
          {
            "id": "computer-science-1-5",
            "name": "Sorting"
          },
          {
            "id": "computer-science-1-6",
            "name": "Search"
          },
          {
            "id": "computer-science-1-7",
            "name": "Functions, procedures and modules"
          },
          {
            "id": "computer-science-1-8",
            "name": "Algorithmic complexity / measures of efficiency"
          },
          {
            "id": "computer-science-1-9",
            "name": "Computer systems"
          },
          {
            "id": "computer-science-1-10",
            "name": "CPU: ALU, Registers, Program counter, Memory"
          },
          {
            "id": "computer-science-1-11",
            "name": "Basic electronics"
          },
          {
            "id": "computer-science-1-12",
            "name": "Logic gates"
          },
          {
            "id": "computer-science-1-13",
            "name": "Operating system layers"
          },
          {
            "id": "computer-science-1-14",
            "name": "Binary, hexadecimal and decimal number systems and…"
          },
          {
            "id": "computer-science-1-15",
            "name": "Digital and analogue input"
          },
          {
            "id": "computer-science-1-16",
            "name": "Web infrastructure - Computer Network Protocols"
          },
          {
            "id": "computer-science-1-17",
            "name": "World Wide Web and the Internet"
          },
          {
            "id": "computer-science-1-18",
            "name": "Data"
          },
          {
            "id": "computer-science-1-19",
            "name": "Data types"
          },
          {
            "id": "computer-science-1-20",
            "name": "Character encoding"
          },
          {
            "id": "computer-science-1-21",
            "name": "Information systems"
          },
          {
            "id": "computer-science-1-22",
            "name": "Evaluation and testing"
          },
          {
            "id": "computer-science-1-23",
            "name": "Debugging"
          },
          {
            "id": "computer-science-1-24",
            "name": "Testing"
          }
        ]
      },
      {
        "id": "computer-science-2",
        "name": "Strand 3: Computer science in practice",
        "subtopics": [
          {
            "id": "computer-science-2-0",
            "name": "Applied Learning Task 1 - Interactive information…"
          },
          {
            "id": "computer-science-2-1",
            "name": "ALT1: Web design and user-centred design"
          },
          {
            "id": "computer-science-2-2",
            "name": "ALT1: File systems and relational databases"
          },
          {
            "id": "computer-science-2-3",
            "name": "Applied Learning Task 2 - Analytics"
          },
          {
            "id": "computer-science-2-4",
            "name": "ALT2"
          },
          {
            "id": "computer-science-2-5",
            "name": "ALT2"
          },
          {
            "id": "computer-science-2-6",
            "name": "Applied Learning Task 3 - Modelling and simulation"
          },
          {
            "id": "computer-science-2-7",
            "name": "ALT3: Agent-based modelling and emergent behaviours"
          },
          {
            "id": "computer-science-2-8",
            "name": "Applied Learning Task 4 - Embedded systems"
          },
          {
            "id": "computer-science-2-9",
            "name": "ALT4: Computing inputs and outputs"
          }
        ]
      }
    ]
  },
  {
    "id": "accounting",
    "name": "Accounting",
    "category": "business",
    "levels": [
      "higher",
      "ordinary"
    ],
    "strands": [
      {
        "id": "accounting-0",
        "name": "The Conceptual Framework of Accounting",
        "subtopics": [
          {
            "id": "accounting-0-0",
            "name": "The nature and purpose of the conceptual framework in…"
          },
          {
            "id": "accounting-0-1",
            "name": "The objectives of financial reporting"
          },
          {
            "id": "accounting-0-2",
            "name": "The users of financial accounting information"
          },
          {
            "id": "accounting-0-3",
            "name": "Desirable qualitative characteristics of accounting…"
          },
          {
            "id": "accounting-0-4",
            "name": "Accounting concepts, bases and policies"
          },
          {
            "id": "accounting-0-5",
            "name": "Fundamental accounting concepts in SSAP 2"
          },
          {
            "id": "accounting-0-6",
            "name": "Other concepts, conventions and principles"
          }
        ]
      },
      {
        "id": "accounting-1",
        "name": "The Regulatory Framework of Accounting (HL)",
        "subtopics": [
          {
            "id": "accounting-1-0",
            "name": "The nature and objectives of the regulation of…"
          },
          {
            "id": "accounting-1-1",
            "name": "The predominant regulatory bodies"
          },
          {
            "id": "accounting-1-2",
            "name": "The regulatory mechanism used by the regulatory bodies"
          },
          {
            "id": "accounting-1-3",
            "name": "The importance of the true and fair view"
          },
          {
            "id": "accounting-1-4",
            "name": "The role of the auditor"
          },
          {
            "id": "accounting-1-5",
            "name": "The procedures for monitoring the regulation of…"
          }
        ]
      },
      {
        "id": "accounting-2",
        "name": "Accounting Records",
        "subtopics": [
          {
            "id": "accounting-2-0",
            "name": "Double-Entry Bookkeeping"
          },
          {
            "id": "accounting-2-1",
            "name": "Bank Reconciliation Statement"
          },
          {
            "id": "accounting-2-2",
            "name": "Control Accounts"
          },
          {
            "id": "accounting-2-3",
            "name": "Suspense Accounts"
          }
        ]
      },
      {
        "id": "accounting-3",
        "name": "Sole Traders",
        "subtopics": [
          {
            "id": "accounting-3-0",
            "name": "The nature and extent of the sole trader form of…"
          },
          {
            "id": "accounting-3-1",
            "name": "Preparation and presentation of trading, profit and…"
          },
          {
            "id": "accounting-3-2",
            "name": "Gross profit, net profit and net worth"
          }
        ]
      },
      {
        "id": "accounting-4",
        "name": "Company Accounting",
        "subtopics": [
          {
            "id": "accounting-4-0",
            "name": "Share Capital, Reserves and Loan Capital"
          },
          {
            "id": "accounting-4-1",
            "name": "Financial Statements of Limited Companies"
          },
          {
            "id": "accounting-4-2",
            "name": "Appreciation of Annual Reports of Public Limited…"
          }
        ]
      },
      {
        "id": "accounting-5",
        "name": "Specialised Accounts",
        "subtopics": [
          {
            "id": "accounting-5-0",
            "name": "Manufacturing Accounts"
          },
          {
            "id": "accounting-5-1",
            "name": "Stock"
          },
          {
            "id": "accounting-5-2",
            "name": "Club Accounts and Accounts of Service Firms"
          },
          {
            "id": "accounting-5-3",
            "name": "Departmental Accounts"
          },
          {
            "id": "accounting-5-4",
            "name": "Farm Accounts"
          }
        ]
      },
      {
        "id": "accounting-6",
        "name": "Incomplete Records",
        "subtopics": [
          {
            "id": "accounting-6-0",
            "name": "Why incomplete records arise"
          },
          {
            "id": "accounting-6-1",
            "name": "Preparation of final accounts using control accounts"
          },
          {
            "id": "accounting-6-2",
            "name": "Profit statements using net worth method"
          },
          {
            "id": "accounting-6-3",
            "name": "Profit statements using mark-up and margin method (HL)"
          }
        ]
      },
      {
        "id": "accounting-7",
        "name": "Cash Flow Statements",
        "subtopics": [
          {
            "id": "accounting-7-0",
            "name": "The importance of cash flow statements"
          },
          {
            "id": "accounting-7-1",
            "name": "The distinction between profit and cash"
          },
          {
            "id": "accounting-7-2",
            "name": "Distinction between items that do and do not involve…"
          },
          {
            "id": "accounting-7-3",
            "name": "The different sources of cash inflows and outflows"
          },
          {
            "id": "accounting-7-4",
            "name": "The movement in working capital on cash flows"
          },
          {
            "id": "accounting-7-5",
            "name": "The preparation of simple cash flow statements"
          }
        ]
      },
      {
        "id": "accounting-8",
        "name": "Analysis and Interpretation of Financial Statements",
        "subtopics": [
          {
            "id": "accounting-8-0",
            "name": "Objective of analysis and interpretation of financial…"
          },
          {
            "id": "accounting-8-1",
            "name": "Definition, calculation and role of accounting ratios"
          },
          {
            "id": "accounting-8-2",
            "name": "Users and their interest in accounting ratios"
          },
          {
            "id": "accounting-8-3",
            "name": "Limitations of ratio analysis"
          },
          {
            "id": "accounting-8-4",
            "name": "Profitability and efficiency ratios"
          },
          {
            "id": "accounting-8-5",
            "name": "Working capital ratios"
          },
          {
            "id": "accounting-8-6",
            "name": "Liquidity/solvency ratios"
          },
          {
            "id": "accounting-8-7",
            "name": "Gearing ratios"
          },
          {
            "id": "accounting-8-8",
            "name": "Investment ratios"
          },
          {
            "id": "accounting-8-9",
            "name": "Interpreting the findings of ratio analysis"
          },
          {
            "id": "accounting-8-10",
            "name": "Presentation of reports (HL)"
          }
        ]
      },
      {
        "id": "accounting-9",
        "name": "Management Accounting",
        "subtopics": [
          {
            "id": "accounting-9-0",
            "name": "The nature and scope of management accounting and its…"
          },
          {
            "id": "accounting-9-1",
            "name": "Cost classifications"
          },
          {
            "id": "accounting-9-2",
            "name": "Product costing"
          },
          {
            "id": "accounting-9-3",
            "name": "Cost-Volume-Profit Analysis"
          },
          {
            "id": "accounting-9-4",
            "name": "Budgetary Planning and Control"
          },
          {
            "id": "accounting-9-5",
            "name": "Flexible budgeting (HL)"
          }
        ]
      },
      {
        "id": "accounting-10",
        "name": "Information Technology and Computer Applications in Accounting",
        "subtopics": [
          {
            "id": "accounting-10-0",
            "name": "Information technology in the accounting environment"
          },
          {
            "id": "accounting-10-1",
            "name": "Spreadsheet application in dealing with specific…"
          }
        ]
      }
    ]
  },
  {
    "id": "business",
    "name": "Business",
    "category": "business",
    "levels": [
      "higher",
      "ordinary"
    ],
    "strands": [
      {
        "id": "business-0",
        "name": "Unit 1: People in Business",
        "subtopics": [
          {
            "id": "business-0-0",
            "name": "People and their relationships in business"
          },
          {
            "id": "business-0-1",
            "name": "Consumers, entrepreneurs and investors"
          },
          {
            "id": "business-0-2",
            "name": "Producers, suppliers and services"
          },
          {
            "id": "business-0-3",
            "name": "Employer, employee and trade union relationships"
          },
          {
            "id": "business-0-4",
            "name": "Interest groups"
          },
          {
            "id": "business-0-5",
            "name": "Co-operative and competitive relationships"
          },
          {
            "id": "business-0-6",
            "name": "Elements of contract law"
          },
          {
            "id": "business-0-7",
            "name": "Conflicting interests and how they are resolved"
          },
          {
            "id": "business-0-8",
            "name": "Identifying areas of conflict in business"
          },
          {
            "id": "business-0-9",
            "name": "Methods of resolving conflicts in relationships"
          },
          {
            "id": "business-0-10",
            "name": "Consumer and industrial relations legislation"
          }
        ]
      },
      {
        "id": "business-1",
        "name": "Unit 2: Enterprise",
        "subtopics": [
          {
            "id": "business-1-0",
            "name": "Introduction and definition of enterprise"
          },
          {
            "id": "business-1-1",
            "name": "Entrepreneurs and enterprise skills"
          },
          {
            "id": "business-1-2",
            "name": "Characteristics of entrepreneurs"
          },
          {
            "id": "business-1-3",
            "name": "Enterprise skills - innate and learned"
          },
          {
            "id": "business-1-4",
            "name": "Application of enterprise skills to different…"
          }
        ]
      },
      {
        "id": "business-2",
        "name": "Unit 3: Managing 1",
        "subtopics": [
          {
            "id": "business-2-0",
            "name": "Introduction and definition of management"
          },
          {
            "id": "business-2-1",
            "name": "Managers and management skills"
          },
          {
            "id": "business-2-2",
            "name": "Characteristics of managers"
          },
          {
            "id": "business-2-3",
            "name": "Difference between enterprise and management"
          },
          {
            "id": "business-2-4",
            "name": "Management skill"
          },
          {
            "id": "business-2-5",
            "name": "Management skill: Motivating - classic motivation…"
          },
          {
            "id": "business-2-6",
            "name": "Management skill"
          },
          {
            "id": "business-2-7",
            "name": "Management activities"
          },
          {
            "id": "business-2-8",
            "name": "Planning - theory, principles and types"
          },
          {
            "id": "business-2-9",
            "name": "Organising - structure of organisation; staffing…"
          },
          {
            "id": "business-2-10",
            "name": "Controlling - theory, principles and types"
          }
        ]
      },
      {
        "id": "business-3",
        "name": "Unit 4: Managing 2",
        "subtopics": [
          {
            "id": "business-3-0",
            "name": "Household and business manager"
          },
          {
            "id": "business-3-1",
            "name": "Aspects of finance"
          },
          {
            "id": "business-3-2",
            "name": "Aspects of insurance"
          },
          {
            "id": "business-3-3",
            "name": "Aspects of taxation"
          },
          {
            "id": "business-3-4",
            "name": "Human resource management"
          },
          {
            "id": "business-3-5",
            "name": "HRM function: Recruitment and selection"
          },
          {
            "id": "business-3-6",
            "name": "HRM function: Employer and employee relationships"
          },
          {
            "id": "business-3-7",
            "name": "HRM function: Teamwork"
          },
          {
            "id": "business-3-8",
            "name": "HRM function"
          },
          {
            "id": "business-3-9",
            "name": "Changing role of management"
          },
          {
            "id": "business-3-10",
            "name": "Managing new relationships: Empowerment of workers…"
          },
          {
            "id": "business-3-11",
            "name": "Managing new technologies"
          },
          {
            "id": "business-3-12",
            "name": "Monitoring the business"
          },
          {
            "id": "business-3-13",
            "name": "Basic final accounts and balance sheets"
          },
          {
            "id": "business-3-14",
            "name": "Main profitability and liquidity ratios; debt/equity…"
          }
        ]
      },
      {
        "id": "business-4",
        "name": "Unit 5: Business in Action",
        "subtopics": [
          {
            "id": "business-4-0",
            "name": "Identifying opportunities"
          },
          {
            "id": "business-4-1",
            "name": "Sources of opportunities: Internal and external"
          },
          {
            "id": "business-4-2",
            "name": "New product and service development process"
          },
          {
            "id": "business-4-3",
            "name": "Marketing"
          },
          {
            "id": "business-4-4",
            "name": "The marketing concept"
          },
          {
            "id": "business-4-5",
            "name": "The marketing strategy"
          },
          {
            "id": "business-4-6",
            "name": "Developing the marketing mix - product, price…"
          },
          {
            "id": "business-4-7",
            "name": "Getting started"
          },
          {
            "id": "business-4-8",
            "name": "Finance, ownership and production options"
          },
          {
            "id": "business-4-9",
            "name": "Developing a business plan"
          },
          {
            "id": "business-4-10",
            "name": "Expansion"
          },
          {
            "id": "business-4-11",
            "name": "Reasons and finance for expansion"
          },
          {
            "id": "business-4-12",
            "name": "Implications and methods of expansion"
          }
        ]
      },
      {
        "id": "business-5",
        "name": "Unit 6: Domestic Environment",
        "subtopics": [
          {
            "id": "business-5-0",
            "name": "Categories of industry"
          },
          {
            "id": "business-5-1",
            "name": "Changing trends in business"
          },
          {
            "id": "business-5-2",
            "name": "Types of business organisation"
          },
          {
            "id": "business-5-3",
            "name": "Changing trends in ownership and structure"
          },
          {
            "id": "business-5-4",
            "name": "Community development: Local community and business…"
          },
          {
            "id": "business-5-5",
            "name": "Business and the economy: Impact of the economy on…"
          },
          {
            "id": "business-5-6",
            "name": "Impact of business on the economy at local and…"
          },
          {
            "id": "business-5-7",
            "name": "The interaction between business and the wider economy"
          },
          {
            "id": "business-5-8",
            "name": "Government and business: Encouraging and regulating…"
          },
          {
            "id": "business-5-9",
            "name": "Role of the Government as employer"
          },
          {
            "id": "business-5-10",
            "name": "Social responsibilities of business"
          },
          {
            "id": "business-5-11",
            "name": "Ethical business practice"
          },
          {
            "id": "business-5-12",
            "name": "Socially responsible business at local and national…"
          }
        ]
      },
      {
        "id": "business-6",
        "name": "Unit 7: International Environment",
        "subtopics": [
          {
            "id": "business-6-0",
            "name": "The international trading environment"
          },
          {
            "id": "business-6-1",
            "name": "The significance of international trade for the Irish…"
          },
          {
            "id": "business-6-2",
            "name": "The changing nature of the international economy and…"
          },
          {
            "id": "business-6-3",
            "name": "Opportunities and challenges for Irish business in…"
          },
          {
            "id": "business-6-4",
            "name": "Trading blocs and agreements"
          },
          {
            "id": "business-6-5",
            "name": "European Union"
          },
          {
            "id": "business-6-6",
            "name": "The importance of the European Union"
          },
          {
            "id": "business-6-7",
            "name": "Purpose of the main European Union policies and…"
          },
          {
            "id": "business-6-8",
            "name": "Decision-making process in the main European Union…"
          },
          {
            "id": "business-6-9",
            "name": "The special interest groups in this process"
          },
          {
            "id": "business-6-10",
            "name": "International business"
          },
          {
            "id": "business-6-11",
            "name": "The global marketing of products and services"
          },
          {
            "id": "business-6-12",
            "name": "The development and impact of transnational companies"
          }
        ]
      }
    ]
  },
  {
    "id": "economics",
    "name": "Economics",
    "category": "business",
    "levels": [
      "higher",
      "ordinary"
    ],
    "strands": [
      {
        "id": "economics-0",
        "name": "Strand 1: What is economics about?",
        "subtopics": [
          {
            "id": "economics-0-0",
            "name": "Economics as a way of thinking"
          },
          {
            "id": "economics-0-1",
            "name": "The economic concepts of scarcity and choice"
          },
          {
            "id": "economics-0-2",
            "name": "Economic, social and environmental sustainability"
          }
        ]
      },
      {
        "id": "economics-1",
        "name": "Strand 2: How are economic decisions made?",
        "subtopics": [
          {
            "id": "economics-1-0",
            "name": "The market economy"
          },
          {
            "id": "economics-1-1",
            "name": "The consumer (demand)"
          },
          {
            "id": "economics-1-2",
            "name": "The firm (supply)"
          },
          {
            "id": "economics-1-3",
            "name": "Government intervention in the market"
          }
        ]
      },
      {
        "id": "economics-2",
        "name": "Strand 3: What can markets do?",
        "subtopics": [
          {
            "id": "economics-2-0",
            "name": "Market structures"
          },
          {
            "id": "economics-2-1",
            "name": "The labour market"
          },
          {
            "id": "economics-2-2",
            "name": "Market failure"
          }
        ]
      },
      {
        "id": "economics-3",
        "name": "Strand 4: What is the relationship between policy and economic performance?",
        "subtopics": [
          {
            "id": "economics-3-0",
            "name": "National income"
          },
          {
            "id": "economics-3-1",
            "name": "Fiscal policy and the budget framework"
          },
          {
            "id": "economics-3-2",
            "name": "Employment and unemployment"
          },
          {
            "id": "economics-3-3",
            "name": "Monetary policy and the price level"
          },
          {
            "id": "economics-3-4",
            "name": "Financial sector"
          }
        ]
      },
      {
        "id": "economics-4",
        "name": "Strand 5: How is the economy influenced by international economics?",
        "subtopics": [
          {
            "id": "economics-4-0",
            "name": "Economic growth and development"
          },
          {
            "id": "economics-4-1",
            "name": "Globalisation"
          },
          {
            "id": "economics-4-2",
            "name": "International trade and competitiveness"
          }
        ]
      }
    ]
  },
  {
    "id": "geography",
    "name": "Geography",
    "category": "social-environmental",
    "levels": [
      "higher",
      "ordinary"
    ],
    "strands": [
      {
        "id": "geography-0",
        "name": "Core Unit 1: Patterns and Processes in the Physical Environment",
        "subtopics": [
          {
            "id": "geography-0-0",
            "name": "The Tectonic Cycle"
          },
          {
            "id": "geography-0-1",
            "name": "The Rock Cycle"
          },
          {
            "id": "geography-0-2",
            "name": "Landform Development (i): Geological structures"
          },
          {
            "id": "geography-0-3",
            "name": "Landform Development (ii): Rock characteristics"
          },
          {
            "id": "geography-0-4",
            "name": "Landform Development (iii)"
          },
          {
            "id": "geography-0-5",
            "name": "Landform Development (iv): The balance of endogenetic…"
          },
          {
            "id": "geography-0-6",
            "name": "Human Interaction"
          }
        ]
      },
      {
        "id": "geography-1",
        "name": "Core Unit 2: Regional Geography",
        "subtopics": [
          {
            "id": "geography-1-0",
            "name": "The Concept of a Region"
          },
          {
            "id": "geography-1-1",
            "name": "The Dynamics of Regions"
          },
          {
            "id": "geography-1-2",
            "name": "The Complexity of Regions (i)"
          },
          {
            "id": "geography-1-3",
            "name": "The Complexity of Regions (ii): How the boundaries…"
          }
        ]
      },
      {
        "id": "geography-2",
        "name": "Core Unit 3: The Geographical Investigation and Skills Unit",
        "subtopics": [
          {
            "id": "geography-2-0",
            "name": "Geographical Skills"
          },
          {
            "id": "geography-2-1",
            "name": "Introduction: Posing the problem and devising a…"
          },
          {
            "id": "geography-2-2",
            "name": "Planning: Preparation of the work"
          },
          {
            "id": "geography-2-3",
            "name": "Collection of Data"
          },
          {
            "id": "geography-2-4",
            "name": "Preparation of the Report"
          },
          {
            "id": "geography-2-5",
            "name": "Conclusion and Evaluation"
          }
        ]
      },
      {
        "id": "geography-3",
        "name": "Elective Unit 4: Patterns and Processes in Economic Activities",
        "subtopics": [
          {
            "id": "geography-3-0",
            "name": "Economic Development"
          },
          {
            "id": "geography-3-1",
            "name": "Spatial variations in economic development"
          },
          {
            "id": "geography-3-2",
            "name": "The Global Economy"
          },
          {
            "id": "geography-3-3",
            "name": "Ireland and the European Union"
          },
          {
            "id": "geography-3-4",
            "name": "Environmental Impact"
          }
        ]
      },
      {
        "id": "geography-4",
        "name": "Elective Unit 5: Patterns and Processes in the Human Environment",
        "subtopics": [
          {
            "id": "geography-4-0",
            "name": "Population: Population characteristics change over…"
          },
          {
            "id": "geography-4-1",
            "name": "Population: Impact on levels of human development"
          },
          {
            "id": "geography-4-2",
            "name": "Population: Population movements and their impact on…"
          },
          {
            "id": "geography-4-3",
            "name": "The Dynamics of Settlement"
          },
          {
            "id": "geography-4-4",
            "name": "Settlement: The changing landuse pattern of urban…"
          },
          {
            "id": "geography-4-5",
            "name": "Settlement: Problems from the growth of urban centres"
          }
        ]
      },
      {
        "id": "geography-5",
        "name": "Optional Unit 6: Global Interdependence (Higher Level Only)",
        "subtopics": [
          {
            "id": "geography-5-0",
            "name": "Views of development and underdevelopment"
          },
          {
            "id": "geography-5-1",
            "name": "The interdependent global economy"
          },
          {
            "id": "geography-5-2",
            "name": "Empowering people - linking economic growth with…"
          },
          {
            "id": "geography-5-3",
            "name": "Sustainable development as a model for the future"
          }
        ]
      },
      {
        "id": "geography-6",
        "name": "Optional Unit 7: Geoecology (Higher Level Only)",
        "subtopics": [
          {
            "id": "geography-6-0",
            "name": "Soil composition and characteristics"
          },
          {
            "id": "geography-6-1",
            "name": "Soil processes and human interference"
          },
          {
            "id": "geography-6-2",
            "name": "Biomes"
          },
          {
            "id": "geography-6-3",
            "name": "Human alteration of biomes"
          }
        ]
      },
      {
        "id": "geography-7",
        "name": "Optional Unit 8: Culture and Identity (Higher Level Only)",
        "subtopics": [
          {
            "id": "geography-7-0",
            "name": "Physical and cultural indicators of population"
          },
          {
            "id": "geography-7-1",
            "name": "Nationality and the nation state"
          },
          {
            "id": "geography-7-2",
            "name": "Identity as a concept"
          }
        ]
      },
      {
        "id": "geography-8",
        "name": "Optional Unit 9: The Atmosphere-Ocean Environment (Higher Level Only)",
        "subtopics": [
          {
            "id": "geography-8-0",
            "name": "Composition and structure of the atmosphere and oceans"
          },
          {
            "id": "geography-8-1",
            "name": "Solar energy distribution"
          },
          {
            "id": "geography-8-2",
            "name": "Exchanges of water between oceans and atmosphere"
          },
          {
            "id": "geography-8-3",
            "name": "Circulation in the atmosphere and oceans"
          },
          {
            "id": "geography-8-4",
            "name": "Distinctive climatic environments"
          },
          {
            "id": "geography-8-5",
            "name": "Influence of climate on economic development"
          }
        ]
      }
    ]
  },
  {
    "id": "history",
    "name": "History",
    "category": "social-environmental",
    "levels": [
      "higher",
      "ordinary"
    ],
    "strands": [
      {
        "id": "history-0",
        "name": "Early Modern field of study (1492-1815): Irish history, 1494-1815",
        "subtopics": [
          {
            "id": "history-0-0",
            "name": "Reform and Reformation in Tudor Ireland, 1494-1558"
          },
          {
            "id": "history-0-1",
            "name": "Reform and Reformation in Tudor Ireland - Case study…"
          },
          {
            "id": "history-0-2",
            "name": "Reform and Reformation in Tudor Ireland - Case study…"
          },
          {
            "id": "history-0-3",
            "name": "Reform and Reformation in Tudor Ireland - Case study…"
          },
          {
            "id": "history-0-4",
            "name": "Rebellion and conquest in Elizabethan Ireland…"
          },
          {
            "id": "history-0-5",
            "name": "Rebellion and conquest in Elizabethan Ireland - Case…"
          },
          {
            "id": "history-0-6",
            "name": "Rebellion and conquest in Elizabethan Ireland - Case…"
          },
          {
            "id": "history-0-7",
            "name": "Rebellion and conquest in Elizabethan Ireland - Case…"
          },
          {
            "id": "history-0-8",
            "name": "Kingdom versus colony - the struggle for mastery in…"
          },
          {
            "id": "history-0-9",
            "name": "Kingdom versus colony - Case study: The trial of…"
          },
          {
            "id": "history-0-10",
            "name": "Kingdom versus colony - Case study: The Scots…"
          },
          {
            "id": "history-0-11",
            "name": "Kingdom versus colony - Case study: Louvain"
          },
          {
            "id": "history-0-12",
            "name": "Establishing a colonial ascendancy, 1660-1715"
          },
          {
            "id": "history-0-13",
            "name": "Establishing a colonial ascendancy - Case study: The…"
          },
          {
            "id": "history-0-14",
            "name": "Establishing a colonial ascendancy - Case study…"
          },
          {
            "id": "history-0-15",
            "name": "Establishing a colonial ascendancy - Case study: The…"
          },
          {
            "id": "history-0-16",
            "name": "Colony versus kingdom - tensions in mid-18th century…"
          },
          {
            "id": "history-0-17",
            "name": "Colony versus kingdom - Case study: The Ponsonbys"
          },
          {
            "id": "history-0-18",
            "name": "Colony versus kingdom - Case study: The Whiteboys"
          },
          {
            "id": "history-0-19",
            "name": "Colony versus kingdom - Case study: The trial of Fr.…"
          },
          {
            "id": "history-0-20",
            "name": "The end of the Irish kingdom and the establishment of…"
          },
          {
            "id": "history-0-21",
            "name": "End of the Irish kingdom - Case study: The Wexford…"
          },
          {
            "id": "history-0-22",
            "name": "End of the Irish kingdom - Case study: The rise of…"
          },
          {
            "id": "history-0-23",
            "name": "End of the Irish kingdom - Case study: Maynooth…"
          }
        ]
      },
      {
        "id": "history-1",
        "name": "Early Modern field of study (1492-1815): History of Europe and the wider world, 1492-1815",
        "subtopics": [
          {
            "id": "history-1-0",
            "name": "Europe from Renaissance to Reformation, 1492-1567"
          },
          {
            "id": "history-1-1",
            "name": "Renaissance to Reformation - Case study: The divorce…"
          },
          {
            "id": "history-1-2",
            "name": "Renaissance to Reformation - Case study"
          },
          {
            "id": "history-1-3",
            "name": "Renaissance to Reformation - Case study: Calvin's…"
          },
          {
            "id": "history-1-4",
            "name": "Religion and power - politics in the later sixteenth…"
          },
          {
            "id": "history-1-5",
            "name": "Religion and power - Case study: The Spanish Armada"
          },
          {
            "id": "history-1-6",
            "name": "Religion and power - Case study: The decline of the…"
          },
          {
            "id": "history-1-7",
            "name": "Religion and power - Case study: The Jesuit mission…"
          },
          {
            "id": "history-1-8",
            "name": "The eclipse of Old Europe, 1609-1660"
          },
          {
            "id": "history-1-9",
            "name": "The eclipse of Old Europe - Case study: The revolt of…"
          },
          {
            "id": "history-1-10",
            "name": "The eclipse of Old Europe - Case study: The Dutch…"
          },
          {
            "id": "history-1-11",
            "name": "The eclipse of Old Europe - Case study: Galileo and…"
          },
          {
            "id": "history-1-12",
            "name": "Europe in the age of Louis XIV, 1660-1715"
          },
          {
            "id": "history-1-13",
            "name": "Age of Louis XIV - Case study: The Streltsy"
          },
          {
            "id": "history-1-14",
            "name": "Age of Louis XIV - Case study: The (English) East…"
          },
          {
            "id": "history-1-15",
            "name": "Age of Louis XIV - Case study: The court of Versailles"
          },
          {
            "id": "history-1-16",
            "name": "Establishing empires, 1715-1775"
          },
          {
            "id": "history-1-17",
            "name": "Establishing empires - Case study"
          },
          {
            "id": "history-1-18",
            "name": "Establishing empires - Case study: The West Indies…"
          },
          {
            "id": "history-1-19",
            "name": "Establishing empires - Case study: The Encyclopedie"
          },
          {
            "id": "history-1-20",
            "name": "Empires in revolution, 1775-1815"
          },
          {
            "id": "history-1-21",
            "name": "Empires in revolution - Case study: The Committee of…"
          },
          {
            "id": "history-1-22",
            "name": "Empires in revolution - Case study: The growth of…"
          },
          {
            "id": "history-1-23",
            "name": "Empires in revolution - Case study: The Civil…"
          }
        ]
      },
      {
        "id": "history-2",
        "name": "Later Modern field of study (1815-1993): Irish history, 1815-1993",
        "subtopics": [
          {
            "id": "history-2-0",
            "name": "Ireland and the Union, 1815-1870"
          },
          {
            "id": "history-2-1",
            "name": "Ireland and the Union - Case study"
          },
          {
            "id": "history-2-2",
            "name": "Ireland and the Union - Case study"
          },
          {
            "id": "history-2-3",
            "name": "Ireland and the Union - Case study"
          },
          {
            "id": "history-2-4",
            "name": "Movements for political and social reform, 1870-1914"
          },
          {
            "id": "history-2-5",
            "name": "Movements for political and social reform - Case…"
          },
          {
            "id": "history-2-6",
            "name": "Movements for political and social reform - Case…"
          },
          {
            "id": "history-2-7",
            "name": "Movements for political and social reform - Case…"
          },
          {
            "id": "history-2-8",
            "name": "The pursuit of sovereignty and partition, 1912-1949"
          },
          {
            "id": "history-2-9",
            "name": "Pursuit of sovereignty and partition - Case study"
          },
          {
            "id": "history-2-10",
            "name": "Pursuit of sovereignty and partition - Case study…"
          },
          {
            "id": "history-2-11",
            "name": "Pursuit of sovereignty and partition - Case study"
          },
          {
            "id": "history-2-12",
            "name": "The Irish diaspora, 1840-1966"
          },
          {
            "id": "history-2-13",
            "name": "The Irish diaspora - Case study: Grosse Isle"
          },
          {
            "id": "history-2-14",
            "name": "The Irish diaspora - Case study"
          },
          {
            "id": "history-2-15",
            "name": "The Irish diaspora - Case study"
          },
          {
            "id": "history-2-16",
            "name": "Politics and society in Northern Ireland, 1949-1993"
          },
          {
            "id": "history-2-17",
            "name": "Politics and society in Northern Ireland - Case study"
          },
          {
            "id": "history-2-18",
            "name": "Politics and society in Northern Ireland - Case…"
          },
          {
            "id": "history-2-19",
            "name": "Politics and society in Northern Ireland - Case…"
          },
          {
            "id": "history-2-20",
            "name": "Government, economy and society in the Republic of…"
          },
          {
            "id": "history-2-21",
            "name": "Government, economy and society in the Republic -…"
          },
          {
            "id": "history-2-22",
            "name": "Government, economy and society in the Republic -…"
          },
          {
            "id": "history-2-23",
            "name": "Government, economy and society in the Republic -…"
          }
        ]
      },
      {
        "id": "history-3",
        "name": "Later Modern field of study (1815-1993): History of Europe and the wider world, 1815-1992",
        "subtopics": [
          {
            "id": "history-3-0",
            "name": "Nationalism and state formation in Europe, 1815-1871"
          },
          {
            "id": "history-3-1",
            "name": "Nationalism and state formation - Case study: The…"
          },
          {
            "id": "history-3-2",
            "name": "Nationalism and state formation - Case study: Robert…"
          },
          {
            "id": "history-3-3",
            "name": "Nationalism and state formation - Case study…"
          },
          {
            "id": "history-3-4",
            "name": "Nation states and international tensions, 1871-1920"
          },
          {
            "id": "history-3-5",
            "name": "Nation states and international tensions - Case…"
          },
          {
            "id": "history-3-6",
            "name": "Nation states and international tensions - Case…"
          },
          {
            "id": "history-3-7",
            "name": "Nation states and international tensions - Case…"
          },
          {
            "id": "history-3-8",
            "name": "Dictatorship and democracy in Europe, 1920-1945"
          },
          {
            "id": "history-3-9",
            "name": "Dictatorship and democracy in Europe - Case study…"
          },
          {
            "id": "history-3-10",
            "name": "Dictatorship and democracy in Europe - Case study"
          },
          {
            "id": "history-3-11",
            "name": "Dictatorship and democracy in Europe - Case study…"
          },
          {
            "id": "history-3-12",
            "name": "Division and realignment in Europe, 1945-1992"
          },
          {
            "id": "history-3-13",
            "name": "Division and realignment in Europe - Case study"
          },
          {
            "id": "history-3-14",
            "name": "Division and realignment in Europe - Case study"
          },
          {
            "id": "history-3-15",
            "name": "Division and realignment in Europe - Case study: The…"
          },
          {
            "id": "history-3-16",
            "name": "European retreat from empire and the aftermath…"
          },
          {
            "id": "history-3-17",
            "name": "European retreat from empire - Case study"
          },
          {
            "id": "history-3-18",
            "name": "European retreat from empire - Case study"
          },
          {
            "id": "history-3-19",
            "name": "European retreat from empire - Case study: Race…"
          },
          {
            "id": "history-3-20",
            "name": "The United States and the world, 1945-1989"
          },
          {
            "id": "history-3-21",
            "name": "The United States and the world - Case study"
          },
          {
            "id": "history-3-22",
            "name": "The United States and the world - Case study"
          },
          {
            "id": "history-3-23",
            "name": "The United States and the world - Case study"
          }
        ]
      }
    ]
  },
  {
    "id": "politics-and-society",
    "name": "Politics and Society",
    "category": "social-environmental",
    "levels": [
      "higher",
      "ordinary"
    ],
    "strands": [
      {
        "id": "politics-and-society-0",
        "name": "Strand 1: Power and decision-making",
        "subtopics": [
          {
            "id": "politics-and-society-0-0",
            "name": "Topic 1: Power and decision-making in the school —…"
          },
          {
            "id": "politics-and-society-0-1",
            "name": "Topic 1 — 1.2 Arguments concerning the need for rules"
          },
          {
            "id": "politics-and-society-0-2",
            "name": "Topic 1 — 1.3 Ideas underpinning these arguments"
          },
          {
            "id": "politics-and-society-0-3",
            "name": "Topic 1 — 1.4 Evidence concerning the effects of…"
          },
          {
            "id": "politics-and-society-0-4",
            "name": "Topic 2: Power and decision-making at national and…"
          },
          {
            "id": "politics-and-society-0-5",
            "name": "Topic 2 — 2.2 How the executive branch of government…"
          },
          {
            "id": "politics-and-society-0-6",
            "name": "Topic 2 — 2.3 Social class and gender as important…"
          },
          {
            "id": "politics-and-society-0-7",
            "name": "Topic 2 — 2.4 Arguments concerning representation"
          },
          {
            "id": "politics-and-society-0-8",
            "name": "Topic 2 — 2.5 Evidence about the effectiveness of…"
          },
          {
            "id": "politics-and-society-0-9",
            "name": "Topic 2 — 2.6 Traditional and new media in a democracy"
          },
          {
            "id": "politics-and-society-0-10",
            "name": "Topic 2 — 2.7 Participants in these debates"
          }
        ]
      },
      {
        "id": "politics-and-society-1",
        "name": "Strand 2: Active citizenship",
        "subtopics": [
          {
            "id": "politics-and-society-1-0",
            "name": "Topic 3: Effectively contributing to communities —…"
          },
          {
            "id": "politics-and-society-1-1",
            "name": "Topic 3 — 3.2 Becoming involved in, or starting an…"
          },
          {
            "id": "politics-and-society-1-2",
            "name": "Topic 3 — 3.3 The range of means of taking action at…"
          },
          {
            "id": "politics-and-society-1-3",
            "name": "Topic 3 — 3.4 Identifying, evaluating and achieving…"
          },
          {
            "id": "politics-and-society-1-4",
            "name": "Topic 3 — 3.5 Developing personal qualities that help…"
          },
          {
            "id": "politics-and-society-1-5",
            "name": "Topic 3 — 3.6 Appraising oneself, evaluating one's…"
          },
          {
            "id": "politics-and-society-1-6",
            "name": "Topic 4: Rights and responsibilities in communication…"
          },
          {
            "id": "politics-and-society-1-7",
            "name": "Topic 4 — 4.2 Developing skills in listening and…"
          },
          {
            "id": "politics-and-society-1-8",
            "name": "Topic 4 — 4.3 Acknowledging differences and…"
          },
          {
            "id": "politics-and-society-1-9",
            "name": "Topic 4 — 4.4 Seeking and evaluating information and…"
          },
          {
            "id": "politics-and-society-1-10",
            "name": "Topic 4 — 4.5 Relating democratic practices in small…"
          }
        ]
      },
      {
        "id": "politics-and-society-2",
        "name": "Strand 3: Human rights and responsibilities",
        "subtopics": [
          {
            "id": "politics-and-society-2-0",
            "name": "Topic 5: Human rights and responsibilities in Ireland…"
          },
          {
            "id": "politics-and-society-2-1",
            "name": "Topic 5 — 5.2 Human rights principles"
          },
          {
            "id": "politics-and-society-2-2",
            "name": "Topic 5 — 5.3 The idea of equality in relation to…"
          },
          {
            "id": "politics-and-society-2-3",
            "name": "Topic 5 — 5.4 Arguments about rights"
          },
          {
            "id": "politics-and-society-2-4",
            "name": "Topic 5 — 5.5 State bodies for human rights"
          },
          {
            "id": "politics-and-society-2-5",
            "name": "Topic 5 — 5.6 Evidence on the right to education"
          },
          {
            "id": "politics-and-society-2-6",
            "name": "Topic 5 — 5.7 Participants in these debates"
          },
          {
            "id": "politics-and-society-2-7",
            "name": "Topic 6: Human rights and responsibilities in Europe…"
          },
          {
            "id": "politics-and-society-2-8",
            "name": "Topic 6 — 6.2 Arguments about rights in the wider…"
          },
          {
            "id": "politics-and-society-2-9",
            "name": "Topic 6 — 6.3 International cooperation and human…"
          }
        ]
      },
      {
        "id": "politics-and-society-3",
        "name": "Strand 4: Globalisation and localisation",
        "subtopics": [
          {
            "id": "politics-and-society-3-0",
            "name": "Topic 7: Globalisation and identity — 7.1…"
          },
          {
            "id": "politics-and-society-3-1",
            "name": "Topic 7 — 7.2 Diversity and cultural change"
          },
          {
            "id": "politics-and-society-3-2",
            "name": "Topic 7 — 7.3 Diversity in the European Union"
          },
          {
            "id": "politics-and-society-3-3",
            "name": "Topic 7 — 7.4 Understanding identity"
          },
          {
            "id": "politics-and-society-3-4",
            "name": "Topic 7 — 7.5 Understanding interaction between…"
          },
          {
            "id": "politics-and-society-3-5",
            "name": "Topic 7 — 7.6 Globalisation and political power"
          },
          {
            "id": "politics-and-society-3-6",
            "name": "Topic 7 — 7.7 Participants in these debates"
          },
          {
            "id": "politics-and-society-3-7",
            "name": "Topic 8: Sustainable development — 8.1 Actions that…"
          },
          {
            "id": "politics-and-society-3-8",
            "name": "Topic 8 — 8.2 Arguments concerning sustainable…"
          },
          {
            "id": "politics-and-society-3-9",
            "name": "Topic 8 — 8.3 Participants in these debates"
          }
        ]
      }
    ]
  },
  {
    "id": "religious-education",
    "name": "Religious Education",
    "category": "social-environmental",
    "levels": [
      "higher",
      "ordinary"
    ],
    "strands": [
      {
        "id": "religious-education-0",
        "name": "Section A: The Search for Meaning and Values (Unit 1 - compulsory)",
        "subtopics": [
          {
            "id": "religious-education-0-0",
            "name": "1.1 The contemporary context"
          },
          {
            "id": "religious-education-0-1",
            "name": "1.2 The tradition of search"
          },
          {
            "id": "religious-education-0-2",
            "name": "2.1 The language of symbol"
          },
          {
            "id": "religious-education-0-3",
            "name": "2.2 The tradition of response"
          },
          {
            "id": "religious-education-0-4",
            "name": "3.1 The gods of the ancients"
          },
          {
            "id": "religious-education-0-5",
            "name": "3.2 The concept of revelation"
          },
          {
            "id": "religious-education-0-6",
            "name": "3.3 Naming God, past and present"
          },
          {
            "id": "religious-education-0-7",
            "name": "4.1 Religion as a source of communal values"
          },
          {
            "id": "religious-education-0-8",
            "name": "4.2 Secular sources of communal values"
          }
        ]
      },
      {
        "id": "religious-education-1",
        "name": "Section B: Christianity: Origins and Contemporary Expressions (Unit 2 - choose 2 of B/C/D)",
        "subtopics": [
          {
            "id": "religious-education-1-0",
            "name": "Part 1: The return to origins — 1.1 The pattern of…"
          },
          {
            "id": "religious-education-1-1",
            "name": "1.2 Jesus and his message in contemporary culture"
          },
          {
            "id": "religious-education-1-2",
            "name": "Part 2: The vision of Jesus in context — 2.1 Rome"
          },
          {
            "id": "religious-education-1-3",
            "name": "2.2 Evidence for Jesus of Nazareth"
          },
          {
            "id": "religious-education-1-4",
            "name": "2.3 The teachings of Jesus and their impact on the…"
          },
          {
            "id": "religious-education-1-5",
            "name": "2.4 Jesus as Messiah"
          },
          {
            "id": "religious-education-1-6",
            "name": "Part 3: The message in conflict — 3.1 Conflict with…"
          },
          {
            "id": "religious-education-1-7",
            "name": "3.2 The death and resurrection of Jesus"
          },
          {
            "id": "religious-education-1-8",
            "name": "Part 4: The formation of Christian communities — 4.1…"
          },
          {
            "id": "religious-education-1-9",
            "name": "Part 5: The Christian message today — 5.1…"
          },
          {
            "id": "religious-education-1-10",
            "name": "5.2 Trends in Christianity (Higher level)"
          }
        ]
      },
      {
        "id": "religious-education-2",
        "name": "Section C: World Religions (Unit 2 - choose 2 of B/C/D)",
        "subtopics": [
          {
            "id": "religious-education-2-0",
            "name": "Part 1: The phenomenon of religion — 1.1 Religion as…"
          },
          {
            "id": "religious-education-2-1",
            "name": "1.2 Primal religion"
          },
          {
            "id": "religious-education-2-2",
            "name": "1.3 The holy (Higher level)"
          },
          {
            "id": "religious-education-2-3",
            "name": "Part 2: A closer look at the major living traditions…"
          },
          {
            "id": "religious-education-2-4",
            "name": "2.2 The community of believers"
          },
          {
            "id": "religious-education-2-5",
            "name": "2.3 A celebrating tradition"
          },
          {
            "id": "religious-education-2-6",
            "name": "2.4 Challenges to the tradition"
          },
          {
            "id": "religious-education-2-7",
            "name": "2.5 Inter-faith dialogue"
          },
          {
            "id": "religious-education-2-8",
            "name": "Part 3: New religious movements — 3.1 Cults and sects"
          },
          {
            "id": "religious-education-2-9",
            "name": "3.2 Some new religious movements"
          },
          {
            "id": "religious-education-2-10",
            "name": "Part 4: Other living traditions — 4.1 A living…"
          },
          {
            "id": "religious-education-2-11",
            "name": "4.2 Traditions in dialogue (Higher level)"
          }
        ]
      },
      {
        "id": "religious-education-3",
        "name": "Section D: Moral Decision-Making (Unit 2 - choose 2 of B/C/D)",
        "subtopics": [
          {
            "id": "religious-education-3-0",
            "name": "Part 1: Thinking about morality — 1.1 What is…"
          },
          {
            "id": "religious-education-3-1",
            "name": "1.2 Why be moral?"
          },
          {
            "id": "religious-education-3-2",
            "name": "1.3 The common good and individual freedom"
          },
          {
            "id": "religious-education-3-3",
            "name": "Part 2: Morality and religion — 2.1 The relationship…"
          },
          {
            "id": "religious-education-3-4",
            "name": "2.2 Morality and the Christian tradition"
          },
          {
            "id": "religious-education-3-5",
            "name": "2.3 Religious perspectives on moral issues"
          },
          {
            "id": "religious-education-3-6",
            "name": "Part 3: Moral principles and decision-making —…"
          },
          {
            "id": "religious-education-3-7",
            "name": "Part 4: Moral development"
          }
        ]
      },
      {
        "id": "religious-education-4",
        "name": "Section E: Religion and Gender (Unit 3 - elective / coursework)",
        "subtopics": [
          {
            "id": "religious-education-4-0",
            "name": "Part 1"
          },
          {
            "id": "religious-education-4-1",
            "name": "1.2 The place of women and men in the major religious…"
          },
          {
            "id": "religious-education-4-2",
            "name": "Part 2: Gender and Christianity — 2.1 Women and men…"
          },
          {
            "id": "religious-education-4-3",
            "name": "2.2 Women and men in the Christian scriptures /…"
          },
          {
            "id": "religious-education-4-4",
            "name": "2.3 Changing perspectives on Mary, the mother of Jesus"
          },
          {
            "id": "religious-education-4-5",
            "name": "2.4 Gender perspectives on empowerment"
          },
          {
            "id": "religious-education-4-6",
            "name": "Part 3: Women's stories — 3.1 Feminist theologies and…"
          }
        ]
      },
      {
        "id": "religious-education-5",
        "name": "Section F: Issues of Justice and Peace (Unit 3 - elective / coursework)",
        "subtopics": [
          {
            "id": "religious-education-5-0",
            "name": "Part 1: Reflecting on context — 1.1 Social analysis"
          },
          {
            "id": "religious-education-5-1",
            "name": "1.2 Social analysis in action"
          },
          {
            "id": "religious-education-5-2",
            "name": "Part 2: The concept of justice and peace — 2.1…"
          },
          {
            "id": "religious-education-5-3",
            "name": "2.2 Visions of peace"
          },
          {
            "id": "religious-education-5-4",
            "name": "2.3 Religious perspectives on justice and peace"
          },
          {
            "id": "religious-education-5-5",
            "name": "2.4 Violence"
          },
          {
            "id": "religious-education-5-6",
            "name": "Part 3: The religious imperative to act for justice…"
          },
          {
            "id": "religious-education-5-7",
            "name": "3.2 Religious traditions and the environment"
          }
        ]
      },
      {
        "id": "religious-education-6",
        "name": "Section G: Worship, Prayer and Ritual (Unit 3 - elective / coursework)",
        "subtopics": [
          {
            "id": "religious-education-6-0",
            "name": "Part 1"
          },
          {
            "id": "religious-education-6-1",
            "name": "1.2 Ritual"
          },
          {
            "id": "religious-education-6-2",
            "name": "1.3 Sacrament"
          },
          {
            "id": "religious-education-6-3",
            "name": "Part 2: Prayer — 2.1 The need for reflection"
          },
          {
            "id": "religious-education-6-4",
            "name": "2.2 The human being as pray-er"
          },
          {
            "id": "religious-education-6-5",
            "name": "2.3 Contexts for prayer"
          },
          {
            "id": "religious-education-6-6",
            "name": "2.4 The praying tradition"
          },
          {
            "id": "religious-education-6-7",
            "name": "Part 3: Meditation and contemplation — 3.1 Meditation"
          },
          {
            "id": "religious-education-6-8",
            "name": "3.2 The contemplative traditions"
          },
          {
            "id": "religious-education-6-9",
            "name": "3.3 The mystic tradition"
          }
        ]
      },
      {
        "id": "religious-education-7",
        "name": "Section H: The Bible: Literature and Sacred Text (Unit 3 - elective / coursework)",
        "subtopics": [
          {
            "id": "religious-education-7-0",
            "name": "Part 1: The Bible as living classic and sacred text —…"
          },
          {
            "id": "religious-education-7-1",
            "name": "1.2 The Bible as sacred text"
          },
          {
            "id": "religious-education-7-2",
            "name": "Part 2: Text and community — 2.1 The formation of the…"
          },
          {
            "id": "religious-education-7-3",
            "name": "2.2 The Gospels"
          },
          {
            "id": "religious-education-7-4",
            "name": "Part 3: The literature of the Bible — 3.1 The…"
          },
          {
            "id": "religious-education-7-5",
            "name": "3.2 The language of reflection"
          },
          {
            "id": "religious-education-7-6",
            "name": "3.3 The language of symbol (Higher level)"
          },
          {
            "id": "religious-education-7-7",
            "name": "Part 4: Biblical texts — 4.1 The Hebrew scriptures"
          },
          {
            "id": "religious-education-7-8",
            "name": "4.2 The New Testament"
          }
        ]
      },
      {
        "id": "religious-education-8",
        "name": "Section I: Religion: The Irish Experience (Unit 3 - elective / coursework)",
        "subtopics": [
          {
            "id": "religious-education-8-0",
            "name": "Part 1: Patterns of change"
          },
          {
            "id": "religious-education-8-1",
            "name": "Part 2: Pre-Christian Ireland — 2.1 Local evidence"
          },
          {
            "id": "religious-education-8-2",
            "name": "2.2 National evidence"
          },
          {
            "id": "religious-education-8-3",
            "name": "Part 3: Christianity in Ireland — 3.1 The coming of…"
          },
          {
            "id": "religious-education-8-4",
            "name": "3.2 Religion, spirituality and land"
          },
          {
            "id": "religious-education-8-5",
            "name": "3.3 Religion, spirituality and monasticism"
          },
          {
            "id": "religious-education-8-6",
            "name": "3.4 Religion, spirituality and reforms"
          },
          {
            "id": "religious-education-8-7",
            "name": "3.5 Religion and the ideas of the Enlightenment /…"
          },
          {
            "id": "religious-education-8-8",
            "name": "3.6 Religion in contemporary Ireland"
          }
        ]
      },
      {
        "id": "religious-education-9",
        "name": "Section J: Religion and Science (Unit 3 - elective / coursework)",
        "subtopics": [
          {
            "id": "religious-education-9-0",
            "name": "Part 1: The scientific and theological enterprises"
          },
          {
            "id": "religious-education-9-1",
            "name": "Part 2: The relationship between religion and science…"
          },
          {
            "id": "religious-education-9-2",
            "name": "2.2 Science and religion in tension (Darwin)"
          },
          {
            "id": "religious-education-9-3",
            "name": "2.3 Science and religion in dialogue"
          },
          {
            "id": "religious-education-9-4",
            "name": "2.4 Science and religion in dialogue"
          },
          {
            "id": "religious-education-9-5",
            "name": "Part 3: Current issues for religion and science…"
          },
          {
            "id": "religious-education-9-6",
            "name": "3.2 The new physics and religion (Higher level)"
          },
          {
            "id": "religious-education-9-7",
            "name": "Part 4: Current issues for religion and science: Life…"
          },
          {
            "id": "religious-education-9-8",
            "name": "4.2 Specific topics (Higher level)"
          }
        ]
      }
    ]
  },
  {
    "id": "home-economics",
    "name": "Home Economics",
    "category": "social-environmental",
    "levels": [
      "higher",
      "ordinary"
    ],
    "strands": [
      {
        "id": "home-economics-0",
        "name": "Strand 1: What is economics about?",
        "subtopics": [
          {
            "id": "home-economics-0-0",
            "name": "Economics as a way of thinking"
          },
          {
            "id": "home-economics-0-1",
            "name": "The economic concepts of scarcity and choice"
          },
          {
            "id": "home-economics-0-2",
            "name": "Economic, social and environmental sustainability"
          }
        ]
      },
      {
        "id": "home-economics-1",
        "name": "Strand 2: How are economic decisions made?",
        "subtopics": [
          {
            "id": "home-economics-1-0",
            "name": "The market economy"
          },
          {
            "id": "home-economics-1-1",
            "name": "The consumer (demand)"
          },
          {
            "id": "home-economics-1-2",
            "name": "The firm (supply)"
          },
          {
            "id": "home-economics-1-3",
            "name": "Government intervention in the market"
          }
        ]
      },
      {
        "id": "home-economics-2",
        "name": "Strand 3: What can markets do?",
        "subtopics": [
          {
            "id": "home-economics-2-0",
            "name": "Market structures"
          },
          {
            "id": "home-economics-2-1",
            "name": "The labour market"
          },
          {
            "id": "home-economics-2-2",
            "name": "Market failure"
          }
        ]
      },
      {
        "id": "home-economics-3",
        "name": "Strand 4: What is the relationship between policy and economic performance?",
        "subtopics": [
          {
            "id": "home-economics-3-0",
            "name": "National income"
          },
          {
            "id": "home-economics-3-1",
            "name": "Fiscal policy and the budget framework"
          },
          {
            "id": "home-economics-3-2",
            "name": "Employment and unemployment"
          },
          {
            "id": "home-economics-3-3",
            "name": "Monetary policy and the price level"
          },
          {
            "id": "home-economics-3-4",
            "name": "Financial sector"
          }
        ]
      },
      {
        "id": "home-economics-4",
        "name": "Strand 5: How is the economy influenced by international economics?",
        "subtopics": [
          {
            "id": "home-economics-4-0",
            "name": "Economic growth and development"
          },
          {
            "id": "home-economics-4-1",
            "name": "Globalisation"
          },
          {
            "id": "home-economics-4-2",
            "name": "International trade and competitiveness"
          }
        ]
      }
    ]
  },
  {
    "id": "art",
    "name": "Art (including crafts / Visual Studies)",
    "category": "arts",
    "levels": [
      "higher",
      "ordinary"
    ],
    "strands": [
      {
        "id": "art-0",
        "name": "Research strand",
        "subtopics": [
          {
            "id": "art-0-0",
            "name": "1.1 Looking"
          },
          {
            "id": "art-0-1",
            "name": "1.2 Recording and documenting"
          },
          {
            "id": "art-0-2",
            "name": "1.3 Experimenting and interpretation"
          },
          {
            "id": "art-0-3",
            "name": "1.4 Contextual enquiries"
          },
          {
            "id": "art-0-4",
            "name": "1.5 Process"
          }
        ]
      },
      {
        "id": "art-1",
        "name": "Create strand",
        "subtopics": [
          {
            "id": "art-1-0",
            "name": "2.1 Making"
          },
          {
            "id": "art-1-1",
            "name": "2.2 Contextual enquiries"
          },
          {
            "id": "art-1-2",
            "name": "2.3 Process"
          },
          {
            "id": "art-1-3",
            "name": "2.4 Realisation/Presenting"
          }
        ]
      },
      {
        "id": "art-2",
        "name": "Respond strand",
        "subtopics": [
          {
            "id": "art-2-0",
            "name": "3.1 Analysis"
          },
          {
            "id": "art-2-1",
            "name": "3.2 Contextual enquiries"
          },
          {
            "id": "art-2-2",
            "name": "3.3 Impact and value"
          },
          {
            "id": "art-2-3",
            "name": "3.4 Critical and personal reflection"
          },
          {
            "id": "art-2-4",
            "name": "3.5 Process"
          }
        ]
      },
      {
        "id": "art-3",
        "name": "Visual Studies Framework (six elements)",
        "subtopics": [
          {
            "id": "art-3-0",
            "name": "Context"
          },
          {
            "id": "art-3-1",
            "name": "Artists and Artworks"
          },
          {
            "id": "art-3-2",
            "name": "Analysis"
          },
          {
            "id": "art-3-3",
            "name": "Art Elements and Design Principles"
          },
          {
            "id": "art-3-4",
            "name": "Media and Areas of Practice"
          },
          {
            "id": "art-3-5",
            "name": "Innovation and Invention"
          }
        ]
      },
      {
        "id": "art-4",
        "name": "Visual Studies Content Area 1: Europe and the wider world",
        "subtopics": [
          {
            "id": "art-4-0",
            "name": "Romanesque and Gothic"
          },
          {
            "id": "art-4-1",
            "name": "The Renaissance - Proto, Early, High Renaissance &…"
          },
          {
            "id": "art-4-2",
            "name": "Baroque"
          },
          {
            "id": "art-4-3",
            "name": "Realism, Impressionism and Post-Impressionism"
          },
          {
            "id": "art-4-4",
            "name": "Modernism"
          },
          {
            "id": "art-4-5",
            "name": "Post 1960"
          }
        ]
      },
      {
        "id": "art-5",
        "name": "Visual Studies Content Area 2: Ireland and its place in the wider world",
        "subtopics": [
          {
            "id": "art-5-0",
            "name": "Pre-Christian"
          },
          {
            "id": "art-5-1",
            "name": "Insular Art"
          },
          {
            "id": "art-5-2",
            "name": "Late Medieval Architecture and Art"
          },
          {
            "id": "art-5-3",
            "name": "Georgian period"
          },
          {
            "id": "art-5-4",
            "name": "Irish Art and Modernism"
          },
          {
            "id": "art-5-5",
            "name": "Post 1960"
          }
        ]
      },
      {
        "id": "art-6",
        "name": "Visual Studies Content Area 3: Today's world",
        "subtopics": [
          {
            "id": "art-6-0",
            "name": "Artists: Theory and thinking"
          },
          {
            "id": "art-6-1",
            "name": "Artists: Processes and media"
          },
          {
            "id": "art-6-2",
            "name": "Art as Social Commentary or Commentator"
          },
          {
            "id": "art-6-3",
            "name": "Art and the Environment"
          }
        ]
      }
    ]
  },
  {
    "id": "music",
    "name": "Music",
    "category": "arts",
    "levels": [
      "higher",
      "ordinary"
    ],
    "strands": [
      {
        "id": "music-0",
        "name": "Performing",
        "subtopics": [
          {
            "id": "music-0-0",
            "name": "Singing or playing individually (Appendix A) -…"
          },
          {
            "id": "music-0-1",
            "name": "Singing or playing as a member of a musical group…"
          },
          {
            "id": "music-0-2",
            "name": "Rehearsing and conducting a musical group (Appendix C)"
          },
          {
            "id": "music-0-3",
            "name": "Prepared songs or pieces"
          },
          {
            "id": "music-0-4",
            "name": "Sight reading test"
          },
          {
            "id": "music-0-5",
            "name": "Aural memory test"
          },
          {
            "id": "music-0-6",
            "name": "Unprepared improvisation - melodic, rhythmic…"
          },
          {
            "id": "music-0-7",
            "name": "Accompaniments in individual performing"
          },
          {
            "id": "music-0-8",
            "name": "Ornamentation in traditional Irish music performance"
          },
          {
            "id": "music-0-9",
            "name": "Microtechnology / music technology music-making…"
          },
          {
            "id": "music-0-10",
            "name": "Musical and technical fluency, holding own musical…"
          },
          {
            "id": "music-0-11",
            "name": "Choosing suitable repertoire (Appendix E) - classical…"
          },
          {
            "id": "music-0-12",
            "name": "Higher level elective in performing - a programme of…"
          }
        ]
      },
      {
        "id": "music-1",
        "name": "Composing",
        "subtopics": [
          {
            "id": "music-1-0",
            "name": "Rudiments of music and notation - treble and bass…"
          },
          {
            "id": "music-1-1",
            "name": "Time signatures and major/minor keys"
          },
          {
            "id": "music-1-2",
            "name": "Chord progressions in root position - major keys I…"
          },
          {
            "id": "music-1-3",
            "name": "First inversion chords (Higher level) - major keys…"
          },
          {
            "id": "music-1-4",
            "name": "The dominant seventh (V7) and the cadential 6/4 chord…"
          },
          {
            "id": "music-1-5",
            "name": "Modulation to the dominant and non-chord notes in a…"
          },
          {
            "id": "music-1-6",
            "name": "Melody writing - continuation of a given opening…"
          },
          {
            "id": "music-1-7",
            "name": "Harmony exercises - providing cadential melody/bass…"
          },
          {
            "id": "music-1-8",
            "name": "Harmony exercises (Higher level) - composing melody…"
          },
          {
            "id": "music-1-9",
            "name": "Higher level elective in composing (portfolio) -…"
          }
        ]
      },
      {
        "id": "music-2",
        "name": "Listening",
        "subtopics": [
          {
            "id": "music-2-0",
            "name": "Prescribed works (Appendix F) - study four set works…"
          },
          {
            "id": "music-2-1",
            "name": "Comparative judgements and evaluation of…"
          },
          {
            "id": "music-2-2",
            "name": "Irish music - range and variety of Irish music heard…"
          },
          {
            "id": "music-2-3",
            "name": "Aural skills - working knowledge of musical notation"
          },
          {
            "id": "music-2-4",
            "name": "Aural perception of melody and rhythm within a…"
          },
          {
            "id": "music-2-5",
            "name": "Simple musical structures and idiomatic…"
          },
          {
            "id": "music-2-6",
            "name": "Higher level aural skills - semiquaver movement and…"
          },
          {
            "id": "music-2-7",
            "name": "General listening - listening to a wide variety of…"
          },
          {
            "id": "music-2-8",
            "name": "Higher level elective in listening - special study…"
          }
        ]
      }
    ]
  },
  {
    "id": "design-and-communication-graphics",
    "name": "Design and Communication Graphics (DCG)",
    "category": "practical-applied",
    "levels": [
      "higher",
      "ordinary"
    ],
    "strands": [
      {
        "id": "design-and-communication-graphics-0",
        "name": "Plane and Descriptive Geometry (Core)",
        "subtopics": [
          {
            "id": "design-and-communication-graphics-0-0",
            "name": "Projection Systems"
          },
          {
            "id": "design-and-communication-graphics-0-1",
            "name": "Orthographic Projection"
          },
          {
            "id": "design-and-communication-graphics-0-2",
            "name": "Pictorial Projection: Isometric Drawing and…"
          },
          {
            "id": "design-and-communication-graphics-0-3",
            "name": "Pictorial Projection: Perspective Drawing/Projection"
          },
          {
            "id": "design-and-communication-graphics-0-4",
            "name": "Plane Geometry"
          },
          {
            "id": "design-and-communication-graphics-0-5",
            "name": "Conic Sections"
          },
          {
            "id": "design-and-communication-graphics-0-6",
            "name": "Descriptive Geometry of Lines and Planes"
          },
          {
            "id": "design-and-communication-graphics-0-7",
            "name": "Intersection and Development of Surfaces"
          }
        ]
      },
      {
        "id": "design-and-communication-graphics-1",
        "name": "Communication of Design and Computer Graphics (Core)",
        "subtopics": [
          {
            "id": "design-and-communication-graphics-1-0",
            "name": "Graphics in Design and Communication"
          },
          {
            "id": "design-and-communication-graphics-1-1",
            "name": "Communication of Design"
          },
          {
            "id": "design-and-communication-graphics-1-2",
            "name": "Freehand Drawing"
          },
          {
            "id": "design-and-communication-graphics-1-3",
            "name": "Information and Communication Technologies: CAD…"
          },
          {
            "id": "design-and-communication-graphics-1-4",
            "name": "Information and Communication Technologies: ICT and…"
          },
          {
            "id": "design-and-communication-graphics-1-5",
            "name": "Student Assignment"
          }
        ]
      },
      {
        "id": "design-and-communication-graphics-2",
        "name": "Applied Graphics (Optional Areas of Study – two to be chosen)",
        "subtopics": [
          {
            "id": "design-and-communication-graphics-2-0",
            "name": "Dynamic Mechanisms"
          },
          {
            "id": "design-and-communication-graphics-2-1",
            "name": "Structural Forms"
          },
          {
            "id": "design-and-communication-graphics-2-2",
            "name": "Geologic Geometry"
          },
          {
            "id": "design-and-communication-graphics-2-3",
            "name": "Surface Geometry"
          },
          {
            "id": "design-and-communication-graphics-2-4",
            "name": "Assemblies"
          }
        ]
      }
    ]
  },
  {
    "id": "construction-studies",
    "name": "Construction Studies",
    "category": "practical-applied",
    "levels": [
      "higher",
      "ordinary"
    ],
    "strands": [
      {
        "id": "construction-studies-0",
        "name": "Part 1 - Construction Theory and Drawings",
        "subtopics": [
          {
            "id": "construction-studies-0-0",
            "name": "General"
          },
          {
            "id": "construction-studies-0-1",
            "name": "Substructure"
          },
          {
            "id": "construction-studies-0-2",
            "name": "Superstructure"
          },
          {
            "id": "construction-studies-0-3",
            "name": "Internal Construction"
          },
          {
            "id": "construction-studies-0-4",
            "name": "Services and External Works"
          },
          {
            "id": "construction-studies-0-5",
            "name": "Heat and Thermal Effects in Buildings"
          },
          {
            "id": "construction-studies-0-6",
            "name": "Illumination in Buildings"
          },
          {
            "id": "construction-studies-0-7",
            "name": "Sound in Buildings"
          }
        ]
      },
      {
        "id": "construction-studies-1",
        "name": "Part 2 - Practical Skills",
        "subtopics": [
          {
            "id": "construction-studies-1-0",
            "name": "Tools"
          },
          {
            "id": "construction-studies-1-1",
            "name": "Processes"
          }
        ]
      },
      {
        "id": "construction-studies-2",
        "name": "Part 3 - Course Work and Projects",
        "subtopics": [
          {
            "id": "construction-studies-2-0",
            "name": "Project options"
          },
          {
            "id": "construction-studies-2-1",
            "name": "Workshop/laboratory course work"
          },
          {
            "id": "construction-studies-2-2",
            "name": "Building Science - Timber and Adhesives"
          },
          {
            "id": "construction-studies-2-3",
            "name": "Building Science - Porosity and Durability of…"
          },
          {
            "id": "construction-studies-2-4",
            "name": "Building Science - Aggregates and Concrete"
          },
          {
            "id": "construction-studies-2-5",
            "name": "Building Science - Binders, Setting and Hydration"
          },
          {
            "id": "construction-studies-2-6",
            "name": "Building Science - Paints, Pigments and Solvents"
          },
          {
            "id": "construction-studies-2-7",
            "name": "Building Science - Water and Comfort Conditions"
          },
          {
            "id": "construction-studies-2-8",
            "name": "Building Science - Heat"
          },
          {
            "id": "construction-studies-2-9",
            "name": "Building Science - Light"
          },
          {
            "id": "construction-studies-2-10",
            "name": "Building Science - Electricity"
          },
          {
            "id": "construction-studies-2-11",
            "name": "Building Science - Acoustics"
          }
        ]
      },
      {
        "id": "construction-studies-3",
        "name": "Appendix 1 (Leaving Certificate Vocational Programme - optional, examined by optional questions)",
        "subtopics": [
          {
            "id": "construction-studies-3-0",
            "name": "Design"
          },
          {
            "id": "construction-studies-3-1",
            "name": "Structures"
          },
          {
            "id": "construction-studies-3-2",
            "name": "New Technology Applications"
          },
          {
            "id": "construction-studies-3-3",
            "name": "Marketing"
          }
        ]
      }
    ]
  },
  {
    "id": "engineering",
    "name": "Engineering",
    "category": "practical-applied",
    "levels": [
      "higher",
      "ordinary"
    ],
    "strands": [
      {
        "id": "engineering-0",
        "name": "Core: Health and Safety",
        "subtopics": [
          {
            "id": "engineering-0-0",
            "name": "Work environment"
          },
          {
            "id": "engineering-0-1",
            "name": "Personal Protection"
          },
          {
            "id": "engineering-0-2",
            "name": "Hand-tools"
          },
          {
            "id": "engineering-0-3",
            "name": "Machinery"
          },
          {
            "id": "engineering-0-4",
            "name": "Electrical"
          },
          {
            "id": "engineering-0-5",
            "name": "Gas"
          },
          {
            "id": "engineering-0-6",
            "name": "Adhesives"
          },
          {
            "id": "engineering-0-7",
            "name": "Chemicals"
          },
          {
            "id": "engineering-0-8",
            "name": "Computers"
          }
        ]
      },
      {
        "id": "engineering-1",
        "name": "Core: Manufacturing Techniques and Technology",
        "subtopics": [
          {
            "id": "engineering-1-0",
            "name": "Marking out and measurement"
          },
          {
            "id": "engineering-1-1",
            "name": "Shaping"
          },
          {
            "id": "engineering-1-2",
            "name": "Bending & folding"
          },
          {
            "id": "engineering-1-3",
            "name": "Surface finish"
          },
          {
            "id": "engineering-1-4",
            "name": "Lathe"
          },
          {
            "id": "engineering-1-5",
            "name": "Cutting tool geometry"
          },
          {
            "id": "engineering-1-6",
            "name": "Drilling machine and operations"
          },
          {
            "id": "engineering-1-7",
            "name": "Soldering"
          },
          {
            "id": "engineering-1-8",
            "name": "Welding"
          },
          {
            "id": "engineering-1-9",
            "name": "Adhesive"
          },
          {
            "id": "engineering-1-10",
            "name": "Fasteners"
          },
          {
            "id": "engineering-1-11",
            "name": "Joining"
          }
        ]
      },
      {
        "id": "engineering-2",
        "name": "Core: Materials Science",
        "subtopics": [
          {
            "id": "engineering-2-0",
            "name": "Materials Testing"
          },
          {
            "id": "engineering-2-1",
            "name": "Properties of Materials"
          },
          {
            "id": "engineering-2-2",
            "name": "Origin and production of materials"
          },
          {
            "id": "engineering-2-3",
            "name": "Recycling"
          },
          {
            "id": "engineering-2-4",
            "name": "Structure of Materials"
          },
          {
            "id": "engineering-2-5",
            "name": "Heat Treatment"
          },
          {
            "id": "engineering-2-6",
            "name": "Corrosion"
          }
        ]
      },
      {
        "id": "engineering-3",
        "name": "Core: Drawing and Design",
        "subtopics": [
          {
            "id": "engineering-3-0",
            "name": "Freehand sketching"
          },
          {
            "id": "engineering-3-1",
            "name": "Orthographic drawing"
          },
          {
            "id": "engineering-3-2",
            "name": "Pictorial drawing"
          },
          {
            "id": "engineering-3-3",
            "name": "Geometric drawing (developments)"
          },
          {
            "id": "engineering-3-4",
            "name": "Presentation and reporting"
          },
          {
            "id": "engineering-3-5",
            "name": "Framework for designing"
          },
          {
            "id": "engineering-3-6",
            "name": "Product design"
          }
        ]
      },
      {
        "id": "engineering-4",
        "name": "Core: Computer Aided Processes (CAD/CAM)",
        "subtopics": [
          {
            "id": "engineering-4-0",
            "name": "Drawing functions"
          },
          {
            "id": "engineering-4-1",
            "name": "CAM Part program"
          },
          {
            "id": "engineering-4-2",
            "name": "CAM Simulation"
          },
          {
            "id": "engineering-4-3",
            "name": "Computer terminology"
          },
          {
            "id": "engineering-4-4",
            "name": "CAD hardware"
          },
          {
            "id": "engineering-4-5",
            "name": "CAM Principles"
          },
          {
            "id": "engineering-4-6",
            "name": "CAM Co-ordinates"
          }
        ]
      },
      {
        "id": "engineering-5",
        "name": "Core: Power and Energy",
        "subtopics": [
          {
            "id": "engineering-5-0",
            "name": "Engines"
          },
          {
            "id": "engineering-5-1",
            "name": "Electric Motors"
          },
          {
            "id": "engineering-5-2",
            "name": "Cells and Batteries (simple cell)"
          },
          {
            "id": "engineering-5-3",
            "name": "Energy"
          }
        ]
      },
      {
        "id": "engineering-6",
        "name": "Core: Electronics",
        "subtopics": [
          {
            "id": "engineering-6-0",
            "name": "Electronic circuits"
          },
          {
            "id": "engineering-6-1",
            "name": "Transistor Circuits"
          },
          {
            "id": "engineering-6-2",
            "name": "Measurement"
          },
          {
            "id": "engineering-6-3",
            "name": "Electronic Units"
          },
          {
            "id": "engineering-6-4",
            "name": "Sensitive circuits"
          }
        ]
      },
      {
        "id": "engineering-7",
        "name": "Core: Mechanisms",
        "subtopics": [
          {
            "id": "engineering-7-0",
            "name": "Force"
          },
          {
            "id": "engineering-7-1",
            "name": "Levers"
          },
          {
            "id": "engineering-7-2",
            "name": "Pulleys & belt drives"
          },
          {
            "id": "engineering-7-3",
            "name": "Gears and gearing"
          }
        ]
      },
      {
        "id": "engineering-8",
        "name": "Core: Pneumatics",
        "subtopics": [
          {
            "id": "engineering-8-0",
            "name": "Pneumatic Circuit"
          },
          {
            "id": "engineering-8-1",
            "name": "Valves"
          },
          {
            "id": "engineering-8-2",
            "name": "Terminology & symbols"
          },
          {
            "id": "engineering-8-3",
            "name": "Supply & distribution"
          },
          {
            "id": "engineering-8-4",
            "name": "Cylinders"
          }
        ]
      },
      {
        "id": "engineering-9",
        "name": "Option: Computer Aided Processes (CAD/CAM)",
        "subtopics": [
          {
            "id": "engineering-9-0",
            "name": "Design"
          },
          {
            "id": "engineering-9-1",
            "name": "Drawing functions"
          },
          {
            "id": "engineering-9-2",
            "name": "Dimensioning"
          },
          {
            "id": "engineering-9-3",
            "name": "Drawing Generation"
          },
          {
            "id": "engineering-9-4",
            "name": "Printing or plotting"
          },
          {
            "id": "engineering-9-5",
            "name": "Computer Aided Machining (CAM) - CNC lathe"
          },
          {
            "id": "engineering-9-6",
            "name": "Drive system for CAM"
          },
          {
            "id": "engineering-9-7",
            "name": "Applications of CAM"
          }
        ]
      },
      {
        "id": "engineering-10",
        "name": "Option: Decorative Metal Craft",
        "subtopics": [
          {
            "id": "engineering-10-0",
            "name": "Design"
          },
          {
            "id": "engineering-10-1",
            "name": "Geometric Drawing"
          },
          {
            "id": "engineering-10-2",
            "name": "Beaten metalwork"
          },
          {
            "id": "engineering-10-3",
            "name": "Jewellery work / techniques"
          },
          {
            "id": "engineering-10-4",
            "name": "Enamelling"
          },
          {
            "id": "engineering-10-5",
            "name": "Etching"
          },
          {
            "id": "engineering-10-6",
            "name": "Surface Treatment / Decorative Finishes"
          },
          {
            "id": "engineering-10-7",
            "name": "Edge finishing"
          },
          {
            "id": "engineering-10-8",
            "name": "Hot and cold forming"
          },
          {
            "id": "engineering-10-9",
            "name": "Joining Processes"
          },
          {
            "id": "engineering-10-10",
            "name": "Casting"
          },
          {
            "id": "engineering-10-11",
            "name": "Celtic Metalwork"
          }
        ]
      },
      {
        "id": "engineering-11",
        "name": "Option: Power, Energy and Control (Energy Power & Control)",
        "subtopics": [
          {
            "id": "engineering-11-0",
            "name": "Design"
          },
          {
            "id": "engineering-11-1",
            "name": "Energy"
          },
          {
            "id": "engineering-11-2",
            "name": "Control device"
          },
          {
            "id": "engineering-11-3",
            "name": "Computer Interfacing"
          },
          {
            "id": "engineering-11-4",
            "name": "Work"
          },
          {
            "id": "engineering-11-5",
            "name": "Power"
          },
          {
            "id": "engineering-11-6",
            "name": "Efficiency of systems"
          },
          {
            "id": "engineering-11-7",
            "name": "Control"
          }
        ]
      },
      {
        "id": "engineering-12",
        "name": "Option: Manufacturing Techniques and Technology",
        "subtopics": [
          {
            "id": "engineering-12-0",
            "name": "Design"
          },
          {
            "id": "engineering-12-1",
            "name": "Manufacture"
          },
          {
            "id": "engineering-12-2",
            "name": "Lathe Turning"
          },
          {
            "id": "engineering-12-3",
            "name": "Grinding"
          },
          {
            "id": "engineering-12-4",
            "name": "Soldering"
          },
          {
            "id": "engineering-12-5",
            "name": "Welding"
          },
          {
            "id": "engineering-12-6",
            "name": "Heat Treatment"
          },
          {
            "id": "engineering-12-7",
            "name": "Hot forming of metal"
          },
          {
            "id": "engineering-12-8",
            "name": "Shaping of Plastics"
          },
          {
            "id": "engineering-12-9",
            "name": "Metrology"
          }
        ]
      },
      {
        "id": "engineering-13",
        "name": "Option: Materials Science",
        "subtopics": [
          {
            "id": "engineering-13-0",
            "name": "Design"
          },
          {
            "id": "engineering-13-1",
            "name": "Classification of Materials"
          },
          {
            "id": "engineering-13-2",
            "name": "Structure of Materials"
          },
          {
            "id": "engineering-13-3",
            "name": "Corrosion"
          },
          {
            "id": "engineering-13-4",
            "name": "Materials testing"
          },
          {
            "id": "engineering-13-5",
            "name": "Origin and production of materials"
          }
        ]
      }
    ]
  },
  {
    "id": "technology",
    "name": "Technology",
    "category": "practical-applied",
    "levels": [
      "higher",
      "ordinary"
    ],
    "strands": [
      {
        "id": "technology-0",
        "name": "Core: A Process of Design",
        "subtopics": [
          {
            "id": "technology-0-0",
            "name": "Design Brief"
          },
          {
            "id": "technology-0-1",
            "name": "Identification and Analysis of Problems"
          },
          {
            "id": "technology-0-2",
            "name": "Recognition of Constraints"
          },
          {
            "id": "technology-0-3",
            "name": "Investigation and Research"
          },
          {
            "id": "technology-0-4",
            "name": "Generation of Ideas"
          },
          {
            "id": "technology-0-5",
            "name": "Presentation of Ideas"
          },
          {
            "id": "technology-0-6",
            "name": "Selection / Development of Chosen Idea(s)"
          },
          {
            "id": "technology-0-7",
            "name": "Production Planning"
          },
          {
            "id": "technology-0-8",
            "name": "Making and Testing"
          },
          {
            "id": "technology-0-9",
            "name": "Evaluation"
          },
          {
            "id": "technology-0-10",
            "name": "Presentation of Design Folio"
          }
        ]
      },
      {
        "id": "technology-1",
        "name": "Core: Project and Quality Management",
        "subtopics": [
          {
            "id": "technology-1-0",
            "name": "Project Management"
          },
          {
            "id": "technology-1-1",
            "name": "Quality Management"
          }
        ]
      },
      {
        "id": "technology-2",
        "name": "Core: Materials and Production",
        "subtopics": [
          {
            "id": "technology-2-0",
            "name": "Manufacturing Processes and Materials"
          },
          {
            "id": "technology-2-1",
            "name": "Resource Management"
          }
        ]
      },
      {
        "id": "technology-3",
        "name": "Core: Communications and Graphic Media",
        "subtopics": [
          {
            "id": "technology-3-0",
            "name": "Projection Systems"
          },
          {
            "id": "technology-3-1",
            "name": "Measured Drawings"
          },
          {
            "id": "technology-3-2",
            "name": "Pictorial Representation"
          },
          {
            "id": "technology-3-3",
            "name": "Freehand Drawings"
          },
          {
            "id": "technology-3-4",
            "name": "Computer Graphics"
          },
          {
            "id": "technology-3-5",
            "name": "Modelling"
          },
          {
            "id": "technology-3-6",
            "name": "Presentation of Information"
          },
          {
            "id": "technology-3-7",
            "name": "Production of Report"
          }
        ]
      },
      {
        "id": "technology-4",
        "name": "Core: Information and Communications Technology",
        "subtopics": [
          {
            "id": "technology-4-0",
            "name": "Introduction to Computer Systems"
          },
          {
            "id": "technology-4-1",
            "name": "Skills Development, Applications and Software"
          }
        ]
      },
      {
        "id": "technology-5",
        "name": "Core: Structures and Mechanisms",
        "subtopics": [
          {
            "id": "technology-5-0",
            "name": "Structures"
          },
          {
            "id": "technology-5-1",
            "name": "Mechanisms"
          }
        ]
      },
      {
        "id": "technology-6",
        "name": "Core: Energy, Electricity and Electronics",
        "subtopics": [
          {
            "id": "technology-6-0",
            "name": "Energy and Energy Conservation"
          },
          {
            "id": "technology-6-1",
            "name": "Electricity"
          },
          {
            "id": "technology-6-2",
            "name": "Electronics"
          }
        ]
      },
      {
        "id": "technology-7",
        "name": "Option: Electronics and Control",
        "subtopics": [
          {
            "id": "technology-7-0",
            "name": "Electrical Measurements"
          },
          {
            "id": "technology-7-1",
            "name": "Components and Circuit Design"
          },
          {
            "id": "technology-7-2",
            "name": "Power Supplies and Safety"
          },
          {
            "id": "technology-7-3",
            "name": "Electric Motors"
          },
          {
            "id": "technology-7-4",
            "name": "Assembly of Pre-designed Circuits"
          },
          {
            "id": "technology-7-5",
            "name": "Sensors"
          },
          {
            "id": "technology-7-6",
            "name": "Logic Circuits"
          },
          {
            "id": "technology-7-7",
            "name": "Inputs and Outputs"
          },
          {
            "id": "technology-7-8",
            "name": "Counters"
          }
        ]
      },
      {
        "id": "technology-8",
        "name": "Option: Applied Control Systems",
        "subtopics": [
          {
            "id": "technology-8-0",
            "name": "Robotics"
          },
          {
            "id": "technology-8-1",
            "name": "Introduction to Robotic Control"
          },
          {
            "id": "technology-8-2",
            "name": "A/D and D/A Conversion"
          },
          {
            "id": "technology-8-3",
            "name": "Control; Programmable Devices"
          },
          {
            "id": "technology-8-4",
            "name": "Pneumatics"
          }
        ]
      },
      {
        "id": "technology-9",
        "name": "Option: Information and Communications Technology",
        "subtopics": [
          {
            "id": "technology-9-0",
            "name": "Computer Architecture"
          },
          {
            "id": "technology-9-1",
            "name": "Data Communications and Computer Networks"
          },
          {
            "id": "technology-9-2",
            "name": "The Internet"
          },
          {
            "id": "technology-9-3",
            "name": "Multimedia and Design"
          }
        ]
      },
      {
        "id": "technology-10",
        "name": "Option: Manufacturing Systems",
        "subtopics": [
          {
            "id": "technology-10-0",
            "name": "The Context of Manufacturing"
          },
          {
            "id": "technology-10-1",
            "name": "Quality Management"
          },
          {
            "id": "technology-10-2",
            "name": "Project Management"
          },
          {
            "id": "technology-10-3",
            "name": "Concurrent Engineering"
          },
          {
            "id": "technology-10-4",
            "name": "Manufacturing System Design and Control"
          }
        ]
      },
      {
        "id": "technology-11",
        "name": "Option: Materials Technology",
        "subtopics": [
          {
            "id": "technology-11-0",
            "name": "Classification of Materials"
          },
          {
            "id": "technology-11-1",
            "name": "Properties of Materials"
          },
          {
            "id": "technology-11-2",
            "name": "Structure of Materials"
          },
          {
            "id": "technology-11-3",
            "name": "Joining Processes"
          },
          {
            "id": "technology-11-4",
            "name": "Materials Processing"
          },
          {
            "id": "technology-11-5",
            "name": "Surface Treatments"
          },
          {
            "id": "technology-11-6",
            "name": "Skills Development"
          },
          {
            "id": "technology-11-7",
            "name": "Materials and the Environment"
          },
          {
            "id": "technology-11-8",
            "name": "Quality Assurance"
          },
          {
            "id": "technology-11-9",
            "name": "Production Techniques"
          }
        ]
      }
    ]
  },
  {
    "id": "physical-education",
    "name": "Physical Education (LCPE - examinable subject)",
    "category": "practical-applied",
    "levels": [
      "higher",
      "ordinary"
    ],
    "strands": [
      {
        "id": "physical-education-0",
        "name": "Strand 1: Towards optimum performance",
        "subtopics": [
          {
            "id": "physical-education-0-0",
            "name": "Topic 1: Learning and improving skill and technique"
          },
          {
            "id": "physical-education-0-1",
            "name": "1.1 Defining a skilled performance"
          },
          {
            "id": "physical-education-0-2",
            "name": "1.2 Analysing skill and technique"
          },
          {
            "id": "physical-education-0-3",
            "name": "1.3 Skill acquisition"
          },
          {
            "id": "physical-education-0-4",
            "name": "Topic 2: Physical and psychological demands of…"
          },
          {
            "id": "physical-education-0-5",
            "name": "2.1 Physical fitness"
          },
          {
            "id": "physical-education-0-6",
            "name": "2.2 Health-related fitness"
          },
          {
            "id": "physical-education-0-7",
            "name": "2.3 Performance-related fitness"
          },
          {
            "id": "physical-education-0-8",
            "name": "2.4 Application of health- and performance-related…"
          },
          {
            "id": "physical-education-0-9",
            "name": "2.5 Assessment of health- and performance-related…"
          },
          {
            "id": "physical-education-0-10",
            "name": "2.6 Designing a fitness plan"
          },
          {
            "id": "physical-education-0-11",
            "name": "2.7 Psychological preparation"
          },
          {
            "id": "physical-education-0-12",
            "name": "2.8 Diet and nutrition"
          },
          {
            "id": "physical-education-0-13",
            "name": "Topic 3"
          },
          {
            "id": "physical-education-0-14",
            "name": "3.1 Structures, strategies and/or compositional…"
          },
          {
            "id": "physical-education-0-15",
            "name": "3.2 Roles and relationships"
          },
          {
            "id": "physical-education-0-16",
            "name": "3.3 Safe practice"
          },
          {
            "id": "physical-education-0-17",
            "name": "3.4 Rules, rituals and conventions"
          },
          {
            "id": "physical-education-0-18",
            "name": "3.5 Role of coach/choreographer"
          },
          {
            "id": "physical-education-0-19",
            "name": "3.6 Role of official"
          },
          {
            "id": "physical-education-0-20",
            "name": "Topic 4: Planning for optimum performance"
          },
          {
            "id": "physical-education-0-21",
            "name": "4.1 Personal performance analysis"
          },
          {
            "id": "physical-education-0-22",
            "name": "4.2 Methods of analysis"
          },
          {
            "id": "physical-education-0-23",
            "name": "4.3 Aesthetic and artistic considerations"
          },
          {
            "id": "physical-education-0-24",
            "name": "4.4 Planning for optimum performance"
          }
        ]
      },
      {
        "id": "physical-education-1",
        "name": "Strand 2: Contemporary issues in physical activity",
        "subtopics": [
          {
            "id": "physical-education-1-0",
            "name": "Topic 5: Promoting physical activity (core topic)"
          },
          {
            "id": "physical-education-1-1",
            "name": "5.1 Benefits of physical activity participation"
          },
          {
            "id": "physical-education-1-2",
            "name": "5.2 Physical activity participation"
          },
          {
            "id": "physical-education-1-3",
            "name": "5.3 Physical activity promotion"
          },
          {
            "id": "physical-education-1-4",
            "name": "5.4 Pathways to excellence in physical activity"
          },
          {
            "id": "physical-education-1-5",
            "name": "Topic 6: Ethics and fair play (core topic)"
          },
          {
            "id": "physical-education-1-6",
            "name": "6.1 Principles of ethical practice"
          },
          {
            "id": "physical-education-1-7",
            "name": "6.2 Codes of ethics"
          },
          {
            "id": "physical-education-1-8",
            "name": "6.3 Drugs and sport"
          },
          {
            "id": "physical-education-1-9",
            "name": "6.4 Anti-doping rules"
          },
          {
            "id": "physical-education-1-10",
            "name": "6.5 Best practice for the use of supplements"
          },
          {
            "id": "physical-education-1-11",
            "name": "Topic 7: Physical activity and inclusion"
          },
          {
            "id": "physical-education-1-12",
            "name": "7.1 Supports and barriers to physical activity…"
          },
          {
            "id": "physical-education-1-13",
            "name": "7.2 Addressing barriers to physical activity"
          },
          {
            "id": "physical-education-1-14",
            "name": "7.3 Developments in physical activity and sporting…"
          },
          {
            "id": "physical-education-1-15",
            "name": "7.4 Adapted physical activity"
          },
          {
            "id": "physical-education-1-16",
            "name": "Topic 8"
          },
          {
            "id": "physical-education-1-17",
            "name": "8.1 technology on sport and physical activity"
          },
          {
            "id": "physical-education-1-18",
            "name": "8.2 Media in sport"
          },
          {
            "id": "physical-education-1-19",
            "name": "Topic 9: Gender and physical activity"
          },
          {
            "id": "physical-education-1-20",
            "name": "9.1 Gender, sport and physical activity"
          },
          {
            "id": "physical-education-1-21",
            "name": "9.2 Gender, media and body image"
          },
          {
            "id": "physical-education-1-22",
            "name": "9.3 Gender socialisation and its impact on physical…"
          },
          {
            "id": "physical-education-1-23",
            "name": "Topic 10: Business and enterprise in physical…"
          },
          {
            "id": "physical-education-1-24",
            "name": "10.1 Sponsorship and advertising in physical activity…"
          },
          {
            "id": "physical-education-1-25",
            "name": "10.2 Physical activity and sport – the business…"
          },
          {
            "id": "physical-education-1-26",
            "name": "10.3 Mass participation in sport"
          },
          {
            "id": "physical-education-1-27",
            "name": "10.4 Tourism and sport"
          }
        ]
      },
      {
        "id": "physical-education-2",
        "name": "Physical activity areas (learners study three activities, each from a different area)",
        "subtopics": [
          {
            "id": "physical-education-2-0",
            "name": "Adventure activities"
          },
          {
            "id": "physical-education-2-1",
            "name": "Artistic and aesthetic activities"
          },
          {
            "id": "physical-education-2-2",
            "name": "Athletics"
          },
          {
            "id": "physical-education-2-3",
            "name": "Aquatics"
          },
          {
            "id": "physical-education-2-4",
            "name": "Games"
          },
          {
            "id": "physical-education-2-5",
            "name": "Personal exercise and fitness activities"
          }
        ]
      }
    ]
  },
  {
    "id": "lcvp-link-modules",
    "name": "LCVP Link Modules (Vocational Programme component)",
    "category": "business",
    "levels": [
      "common"
    ],
    "strands": [
      {
        "id": "lcvp-link-modules-0",
        "name": "Link Module 1: Preparation for the World of Work",
        "subtopics": [
          {
            "id": "lcvp-link-modules-0-0",
            "name": "Unit 1 - Introduction to Working Life"
          },
          {
            "id": "lcvp-link-modules-0-1",
            "name": "Unit 2 - Job Seeking Skills"
          },
          {
            "id": "lcvp-link-modules-0-2",
            "name": "Unit 3 - Career Investigation"
          },
          {
            "id": "lcvp-link-modules-0-3",
            "name": "Unit 4 - Work Placement"
          }
        ]
      },
      {
        "id": "lcvp-link-modules-1",
        "name": "Link Module 2: Enterprise Education",
        "subtopics": [
          {
            "id": "lcvp-link-modules-1-0",
            "name": "Unit 1 - Enterprise Skills"
          },
          {
            "id": "lcvp-link-modules-1-1",
            "name": "Unit 2 - Local Business Enterprises"
          },
          {
            "id": "lcvp-link-modules-1-2",
            "name": "Unit 3 - Local Voluntary Organisations / Community…"
          },
          {
            "id": "lcvp-link-modules-1-3",
            "name": "Unit 4 - An Enterprise Activity"
          }
        ]
      }
    ]
  }
];
