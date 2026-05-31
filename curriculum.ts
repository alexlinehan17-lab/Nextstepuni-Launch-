/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Leaving Cert curriculum taxonomy — every examined subject → levels →
 * strands → detailed sub-topics, from the official syllabi. Drives the Exam
 * Reps subject/level/topic picker. Subjects with a redeveloped spec use the
 * CURRENTLY-EXAMINED (established) syllabus. ⚠️ Re-verify periodically.
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
            "name": "Fáiltiú / Beannú (Welcome & introduction — name, age, address, exam number)"
          },
          {
            "id": "irish-0-1",
            "name": "Aithris Filíochta (Recitation/reading of a prescribed poem nominated by examiner)"
          },
          {
            "id": "irish-0-2",
            "name": "Sraith Pictiúr (Picture sequence — narrate the story + answer questions; 20 prescribed series, prepare ~10)"
          },
          {
            "id": "irish-0-3",
            "name": "Comhrá / Agallamh (Conversation — self, family, school, subjects, hobbies, area, current affairs)"
          },
          {
            "id": "irish-0-4",
            "name": "Saibhreas, cruinneas agus líofacht (Vocabulary, accuracy and fluency of speech)"
          },
          {
            "id": "irish-0-5",
            "name": "Foghraíocht agus blas (Pronunciation and accent)"
          }
        ]
      },
      {
        "id": "irish-1",
        "name": "An Chluastuiscint (Aural / Listening Comprehension — Paper 1, 60 marks)",
        "subtopics": [
          {
            "id": "irish-1-0",
            "name": "Cuid A — Fógraí (Announcements: Fógra a hAon, Fógra a Dó)"
          },
          {
            "id": "irish-1-1",
            "name": "Cuid B — Comhráite (Conversations: Comhrá a hAon, Comhrá a Dó)"
          },
          {
            "id": "irish-1-2",
            "name": "Cuid C — Píosaí Nuachta (News pieces / reports: Píosa a hAon, Píosa a Dó)"
          },
          {
            "id": "irish-1-3",
            "name": "Tuiscint éisteachta (Listening skills — gist, detail, numbers, dates, places)"
          }
        ]
      },
      {
        "id": "irish-2",
        "name": "An Cheapadóireacht (Composition / Written Production — Paper 1, 100 marks)",
        "subtopics": [
          {
            "id": "irish-2-0",
            "name": "Aiste (Essay — current affairs / discursive topics, ~500–600 words)"
          },
          {
            "id": "irish-2-1",
            "name": "Alt Nuachtáin / Irise (Newspaper or magazine article)"
          },
          {
            "id": "irish-2-2",
            "name": "Blag (Blog post)"
          },
          {
            "id": "irish-2-3",
            "name": "Scéal (Story / creative narrative — based on a prompt or seanfhocal)"
          },
          {
            "id": "irish-2-4",
            "name": "Díospóireacht (Debate speech — for/against a motion)"
          },
          {
            "id": "irish-2-5",
            "name": "Óráid (Speech / address)"
          },
          {
            "id": "irish-2-6",
            "name": "Giota leanúnach (Continuous piece — Ordinary level)"
          },
          {
            "id": "irish-2-7",
            "name": "Saibhreas na Gaeilge (Richness, accuracy and structure of written Irish)"
          }
        ]
      },
      {
        "id": "irish-3",
        "name": "An Léamhthuiscint (Reading Comprehension — Paper 2, ~100 marks)",
        "subtopics": [
          {
            "id": "irish-3-0",
            "name": "Léamhthuiscint A (Reading comprehension text 1 + questions)"
          },
          {
            "id": "irish-3-1",
            "name": "Léamhthuiscint B (Reading comprehension text 2 + questions)"
          },
          {
            "id": "irish-3-2",
            "name": "Ceisteanna tuisceana (Comprehension questions — detail, inference, vocabulary)"
          },
          {
            "id": "irish-3-3",
            "name": "Ceist ghramadaí / teanga (Grammar & language point on the text)"
          }
        ]
      },
      {
        "id": "irish-4",
        "name": "An Prós (Prose — Paper 2; named & optional, Higher & Ordinary)",
        "subtopics": [
          {
            "id": "irish-4-0",
            "name": "Prós Comónta Ainmnithe (Prescribed common prose)"
          },
          {
            "id": "irish-4-1",
            "name": "Oisín i dTír na nÓg (scéal béaloidis, Niall Ó Dónaill eag.)"
          },
          {
            "id": "irish-4-2",
            "name": "An Gnáthrud (Déirdre Ní Ghrianna)"
          },
          {
            "id": "irish-4-3",
            "name": "Seal i Neipeal (Cathal Ó Searcaigh)"
          },
          {
            "id": "irish-4-4",
            "name": "Dís (Siobhán Ní Shúilleabháin)"
          },
          {
            "id": "irish-4-5",
            "name": "Hurlamaboc (Éilís Ní Dhuibhne)"
          },
          {
            "id": "irish-4-6",
            "name": "Cáca Milis (gearrscannán) nó An Lasair Choille (gearrdhráma, Caitlín Maude & Mícheál Ó hAirtnéide)"
          },
          {
            "id": "irish-4-7",
            "name": "Prós: Ábhar Roghnach (Optional/unprescribed prose — sliocht béaloidis, dírbheathaisnéis, gearrscéal, úrscéal, dráma/scannán)"
          }
        ]
      },
      {
        "id": "irish-5",
        "name": "An Fhilíocht (Poetry — Paper 2; named & optional, Higher & Ordinary)",
        "subtopics": [
          {
            "id": "irish-5-0",
            "name": "Filíocht Chomónta Ainmnithe (Prescribed common poetry)"
          },
          {
            "id": "irish-5-1",
            "name": "An Spailpín Fánach (véarsaí 1–3, anaithnid)"
          },
          {
            "id": "irish-5-2",
            "name": "Géibheann (Caitlín Maude)"
          },
          {
            "id": "irish-5-3",
            "name": "An tEarrach Thiar (Máirtín Ó Direáin)"
          },
          {
            "id": "irish-5-4",
            "name": "Mo Ghrá-sa (idir lúibíní) (Nuala Ní Dhomhnaill)"
          },
          {
            "id": "irish-5-5",
            "name": "Colscaradh (Pádraig Mac Suibhne)"
          },
          {
            "id": "irish-5-6",
            "name": "Filíocht: Ábhar Roghnach (Optional/unprescribed poetry — 5 poems, 1 pre-1850)"
          }
        ]
      },
      {
        "id": "irish-6",
        "name": "Litríocht Bhreise — Ardleibhéal (Additional Literature — Higher Level only)",
        "subtopics": [
          {
            "id": "irish-6-0",
            "name": "Prós Breise — An Triail (Mairéad Ní Ghráda) [go huile]"
          },
          {
            "id": "irish-6-1",
            "name": "Prós Breise — A Thig Ná Tit Orm (Maidhc Dainín Ó Sé)"
          },
          {
            "id": "irish-6-2",
            "name": "Prós Breise — Tóraíocht Dhiarmada agus Ghráinne (Nessa Ní Shé eag.)"
          },
          {
            "id": "irish-6-3",
            "name": "Prós Breise — Gafa (Ré Ó Laighléis)"
          },
          {
            "id": "irish-6-4",
            "name": "Prós Breise — Canary Wharf (Orna Ní Choileáin — 5 named short stories)"
          },
          {
            "id": "irish-6-5",
            "name": "Dánta Breise (Additional poems — all five of the following)"
          },
          {
            "id": "irish-6-6",
            "name": "Caoineadh Airt Uí Laoghaire (Eibhlín Dhubh Ní Chonaill)"
          },
          {
            "id": "irish-6-7",
            "name": "Fill Arís (Seán Ó Ríordáin)"
          },
          {
            "id": "irish-6-8",
            "name": "A Chlann (Máire Áine Nic Gearailt)"
          },
          {
            "id": "irish-6-9",
            "name": "Colmáin (Cathal Ó Searcaigh)"
          },
          {
            "id": "irish-6-10",
            "name": "Éiceolaí (Biddy Jenkinson)"
          }
        ]
      },
      {
        "id": "irish-7",
        "name": "Stair Litríocht na Gaeilge / Ábhar Cúlra (Background — Higher Level)",
        "subtopics": [
          {
            "id": "irish-7-0",
            "name": "Stair Litríocht na Gaeilge (History of Irish literature — context, recommended study)"
          },
          {
            "id": "irish-7-1",
            "name": "Comhthéacs agus téamaí na dtéacsanna (Context & themes of prescribed texts)"
          }
        ]
      },
      {
        "id": "irish-8",
        "name": "Scileanna Teanga / Gramadach (Underlying Language Skills)",
        "subtopics": [
          {
            "id": "irish-8-0",
            "name": "An Tuiscint (Comprehension — listening & reading)"
          },
          {
            "id": "irish-8-1",
            "name": "An Labhairt (Speaking / oral production)"
          },
          {
            "id": "irish-8-2",
            "name": "An Scríobh (Writing / written production)"
          },
          {
            "id": "irish-8-3",
            "name": "An Léitheoireacht (Reading)"
          },
          {
            "id": "irish-8-4",
            "name": "Gramadach (Grammar — an aimsir/verb tenses, an tuiseal ginideach, séimhiú & urú, na réamhfhocail)"
          },
          {
            "id": "irish-8-5",
            "name": "Stór focal agus nathanna (Vocabulary, idioms and phrases — saibhreas teanga)"
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
            "name": "Comprehending (analyse, infer, synthesise, evaluate)"
          },
          {
            "id": "english-0-1",
            "name": "Composing (research, plan, draft, re-draft, edit)"
          },
          {
            "id": "english-0-2",
            "name": "Shaping experience through style, genre and context"
          },
          {
            "id": "english-0-3",
            "name": "Texts and genres (every language product as a text to be studied)"
          },
          {
            "id": "english-0-4",
            "name": "Oracy: dialogue, group discussion, oral presentations, performance"
          }
        ]
      },
      {
        "id": "english-1",
        "name": "The Language of Information",
        "subtopics": [
          {
            "id": "english-1-0",
            "name": "Information texts: reports, records, memos, bulletins, abstracts, media accounts, documentary films"
          },
          {
            "id": "english-1-1",
            "name": "Comprehending: give the gist of a text; specify appropriate details"
          },
          {
            "id": "english-1-2",
            "name": "Comprehending: summarise information; evaluate adequacy and indicate omissions"
          },
          {
            "id": "english-1-3",
            "name": "Comprehending: identify the author's point of view and values assumed"
          },
          {
            "id": "english-1-4",
            "name": "Comprehending: indicate genre; comment on language use, structure and lay-out"
          },
          {
            "id": "english-1-5",
            "name": "Composing: records - memos, minutes, notices, precis"
          },
          {
            "id": "english-1-6",
            "name": "Composing: letters of all kinds"
          },
          {
            "id": "english-1-7",
            "name": "Composing: reports and research projects"
          },
          {
            "id": "english-1-8",
            "name": "Composing: media scripts and newspaper reports"
          }
        ]
      },
      {
        "id": "english-2",
        "name": "The Language of Argument",
        "subtopics": [
          {
            "id": "english-2-0",
            "name": "Argumentative texts: deductive and inductive reasoning (journalistic, philosophical, scientific, legal)"
          },
          {
            "id": "english-2-1",
            "name": "Comprehending: outline the stages of an argument and identify the conclusion"
          },
          {
            "id": "english-2-2",
            "name": "Comprehending: identify reasoning structure (key words - therefore, because, nevertheless)"
          },
          {
            "id": "english-2-3",
            "name": "Comprehending: distinguish statements/propositions vs examples; opinion, anecdote vs evidence"
          },
          {
            "id": "english-2-4",
            "name": "Comprehending: evaluate validity; identify assumptions; outline values asserted"
          },
          {
            "id": "english-2-5",
            "name": "Composing: put forward a theory or hypothesis"
          },
          {
            "id": "english-2-6",
            "name": "Composing: justify a decision; attempt an overview"
          }
        ]
      },
      {
        "id": "english-3",
        "name": "The Language of Persuasion",
        "subtopics": [
          {
            "id": "english-3-0",
            "name": "Persuasive texts: political speeches, advertising in all media, satiric texts, journalism"
          },
          {
            "id": "english-3-1",
            "name": "Comprehending: identify persuasive techniques (tone, image, rhythm, choice of words, selection of detail)"
          },
          {
            "id": "english-3-2",
            "name": "Comprehending: evaluate impact in achieving desired effect; indicate audience"
          },
          {
            "id": "english-3-3",
            "name": "Comprehending: analyse value-system advocated/implied; outline whose interests it serves"
          },
          {
            "id": "english-3-4",
            "name": "Composing: newspaper articles"
          },
          {
            "id": "english-3-5",
            "name": "Composing: advertising copy"
          },
          {
            "id": "english-3-6",
            "name": "Composing: public relations / propaganda / political statements"
          }
        ]
      },
      {
        "id": "english-4",
        "name": "The Language of Narration",
        "subtopics": [
          {
            "id": "english-4-0",
            "name": "Narrative texts: short stories, novels, drama texts, autobiographies, biographies, travel-books, films"
          },
          {
            "id": "english-4-1",
            "name": "Comprehending: awareness of own response to texts; analyse and justify that response"
          },
          {
            "id": "english-4-2",
            "name": "Comprehending: indicate significant aspects of narrative and explain meaning generated"
          },
          {
            "id": "english-4-3",
            "name": "Comprehending: outline narrative structure and how it achieves coherence within its genre"
          },
          {
            "id": "english-4-4",
            "name": "Comprehending: narrative characteristics of different genres and how language is shaped for effect"
          },
          {
            "id": "english-4-5",
            "name": "Comprehending: critical viewpoints (gender, power, class) across periods and cultures"
          },
          {
            "id": "english-4-6",
            "name": "Comprehending: compare texts in different genres on the same theme"
          },
          {
            "id": "english-4-7",
            "name": "Composing: anecdote"
          },
          {
            "id": "english-4-8",
            "name": "Composing: parable, fable"
          },
          {
            "id": "english-4-9",
            "name": "Composing: short story"
          },
          {
            "id": "english-4-10",
            "name": "Composing: autobiographical sketch"
          },
          {
            "id": "english-4-11",
            "name": "Composing: scripts and dialogues"
          }
        ]
      },
      {
        "id": "english-5",
        "name": "The Aesthetic Use of Language",
        "subtopics": [
          {
            "id": "english-5-0",
            "name": "Literary genres: fiction, drama, essay, poetry and film"
          },
          {
            "id": "english-5-1",
            "name": "Comprehending: appropriate stances for reading/viewing each literary genre"
          },
          {
            "id": "english-5-2",
            "name": "Comprehending: interpretative performance of texts"
          },
          {
            "id": "english-5-3",
            "name": "Comprehending: awareness of affective, imaginative and intellectual responses; build coherent interpretations"
          },
          {
            "id": "english-5-4",
            "name": "Comprehending: re-read for suggestion, inference and levels of meaning"
          },
          {
            "id": "english-5-5",
            "name": "Comprehending: compare and evaluate texts for the quality of the imaginative experience"
          },
          {
            "id": "english-5-6",
            "name": "Composing: compose within the aesthetic forms encountered"
          },
          {
            "id": "english-5-7",
            "name": "Composing: interventions (alternative scenarios based on texts studied)"
          },
          {
            "id": "english-5-8",
            "name": "Composing: response journals"
          },
          {
            "id": "english-5-9",
            "name": "Composing: analytical and coherent essays relative to a text"
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
            "name": "Shakespearean drama (compulsory at Higher Level; optional at Ordinary Level)"
          },
          {
            "id": "english-6-2",
            "name": "Attitudes, values, structures and styles within the text"
          },
          {
            "id": "english-6-3",
            "name": "Form, structure and style and how they constitute genre"
          }
        ]
      },
      {
        "id": "english-7",
        "name": "Comparative Study (three or more texts)",
        "subtopics": [
          {
            "id": "english-7-0",
            "name": "Higher Level mode: a theme or issue"
          },
          {
            "id": "english-7-1",
            "name": "Higher Level mode: a historical or literary period"
          },
          {
            "id": "english-7-2",
            "name": "Higher Level mode: a literary genre"
          },
          {
            "id": "english-7-3",
            "name": "Higher Level mode: the cultural context"
          },
          {
            "id": "english-7-4",
            "name": "Higher Level mode: the general vision and viewpoint"
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
            "name": "Ordinary Level mode: Specific Themes (e.g. love, race, prejudice, violence)"
          },
          {
            "id": "english-7-10",
            "name": "Ordinary Level mode: Aspects of story (tension, climax, resolution, ending)"
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
            "name": "Higher Level: representative selection from eight prescribed poets (at least six poems each)"
          },
          {
            "id": "english-8-1",
            "name": "Ordinary Level: selection of prescribed poetry (about forty poems)"
          },
          {
            "id": "english-8-2",
            "name": "Unseen poem (both levels)"
          },
          {
            "id": "english-8-3",
            "name": "Reading widely in poetry: themes, style, viewpoint and mode of using language"
          }
        ]
      },
      {
        "id": "english-9",
        "name": "Examination Structure",
        "subtopics": [
          {
            "id": "english-9-0",
            "name": "Paper I, Section: Comprehending (comprehension questions on texts)"
          },
          {
            "id": "english-9-1",
            "name": "Paper I, Section: Composing (functional writing task and extended composition in a specific genre)"
          },
          {
            "id": "english-9-2",
            "name": "Paper II, Section A: In-depth study of the Single Text"
          },
          {
            "id": "english-9-3",
            "name": "Paper II, Section B: Comparative Study (questions on two prescribed modes)"
          },
          {
            "id": "english-9-4",
            "name": "Paper II, Section C: Poetry (unseen poem and prescribed poetry)"
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
            "name": "Meeting and getting to know people and maintaining social relations"
          },
          {
            "id": "french-0-1",
            "name": "Making plans and discussing future action"
          },
          {
            "id": "french-0-2",
            "name": "Understanding, seeking and giving information about climate and weather"
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
            "name": "Facilitating, encouraging or impeding a course of action"
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
            "name": "Talking and writing about your experience of the target language"
          },
          {
            "id": "french-1-4",
            "name": "Consulting reference materials (e.g. dictionaries and grammars) relating to the vocabulary and grammar of the target language"
          }
        ]
      },
      {
        "id": "french-2",
        "name": "Cultural Awareness",
        "subtopics": [
          {
            "id": "french-2-0",
            "name": "Learning in the target language about the present-day culture associated with the target language"
          },
          {
            "id": "french-2-1",
            "name": "Reading modern literary texts (notably novels, short stories, poems and plays, or extracts from these) in the target language"
          },
          {
            "id": "french-2-2",
            "name": "Describing and discussing everyday life in the target language community"
          },
          {
            "id": "french-2-3",
            "name": "Understanding, describing and discussing aspects of the relations between the target language community and Ireland"
          },
          {
            "id": "french-2-4",
            "name": "Understanding, describing and discussing in general terms issues that transcend cultural divisions (e.g. teenager culture, the generation gap, environment and ecology, sexual and racial equality, ethnic minorities, health and lifestyle, human relationships, the European dimension, the Third World)"
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
            "name": "Meeting and getting to know people and maintaining social relations"
          },
          {
            "id": "german-0-1",
            "name": "Making plans and discussing future action"
          },
          {
            "id": "german-0-2",
            "name": "Understanding, seeking and giving information about climate and weather"
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
            "name": "Facilitating, encouraging or impeding a course of action"
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
            "name": "Talking and writing about your experience of the target language"
          },
          {
            "id": "german-1-4",
            "name": "Consulting reference materials (e.g. dictionaries and grammars) relating to the vocabulary and grammar of the target language"
          }
        ]
      },
      {
        "id": "german-2",
        "name": "Cultural Awareness",
        "subtopics": [
          {
            "id": "german-2-0",
            "name": "Learning in the target language about the present-day culture associated with the language (everyday activities; customs and traditions; the arts and entertainment; the range and role of the mass media)"
          },
          {
            "id": "german-2-1",
            "name": "Reading modern literary texts (novels, short stories, poems and plays, or extracts) in the target language"
          },
          {
            "id": "german-2-2",
            "name": "Describing and discussing everyday life in the target language community"
          },
          {
            "id": "german-2-3",
            "name": "Understanding, describing and discussing aspects of the relations between the target language community and Ireland"
          },
          {
            "id": "german-2-4",
            "name": "Understanding, describing and discussing in general terms issues that transcend cultural divisions (e.g. teenager culture; the generation gap; entertainment; environment and ecology; sexual and racial equality; ethnic minorities; health and lifestyle; human relationships/marriage/family; the European dimension; the Third World)"
          }
        ]
      },
      {
        "id": "german-3",
        "name": "Assessment (Four Skills)",
        "subtopics": [
          {
            "id": "german-3-0",
            "name": "Oral Assessment (general conversation; project OR picture sequence; role-play) - Higher 25% / Ordinary 20%"
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
            "name": "Meeting and getting to know people and maintaining social relations"
          },
          {
            "id": "spanish-0-1",
            "name": "Making plans and discussing future action"
          },
          {
            "id": "spanish-0-2",
            "name": "Seeking and giving information about climate and weather"
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
            "name": "Facilitating, encouraging or impeding a course of action"
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
            "name": "Talking and writing about your experience of the target language"
          },
          {
            "id": "spanish-1-4",
            "name": "Consulting reference materials (e.g. dictionaries and grammars) relating to the vocabulary and grammar of the target language"
          }
        ]
      },
      {
        "id": "spanish-2",
        "name": "Cultural Awareness",
        "subtopics": [
          {
            "id": "spanish-2-0",
            "name": "Learning in the target language about the present-day culture associated with the target language"
          },
          {
            "id": "spanish-2-1",
            "name": "Reading modern literary texts (notably novels, short stories, poems and plays, or extracts from these) in the target language"
          },
          {
            "id": "spanish-2-2",
            "name": "Describing and discussing everyday life in target language community"
          },
          {
            "id": "spanish-2-3",
            "name": "Understanding, describing and discussing aspects of the relations between the target language community and Ireland"
          },
          {
            "id": "spanish-2-4",
            "name": "Understanding, describing and discussing in general terms issues that transcend cultural divisions (e.g. teenager culture, the generation gap, environment and ecology, sexual and racial equality, ethnic minorities, health and lifestyle, human relationships, the European dimension, the Third World)"
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
            "name": "Meeting and getting to know people and maintaining social relations"
          },
          {
            "id": "italian-0-1",
            "name": "Making plans and discussing future action"
          },
          {
            "id": "italian-0-2",
            "name": "Understanding, seeking and giving information about climate and weather"
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
            "name": "Facilitating, encouraging or impeding a course of action"
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
            "name": "Talking and writing about your experience of the target language"
          },
          {
            "id": "italian-1-4",
            "name": "Consulting reference materials (e.g. dictionaries and grammars), relating to the vocabulary and grammar of the target language"
          }
        ]
      },
      {
        "id": "italian-2",
        "name": "Cultural Awareness",
        "subtopics": [
          {
            "id": "italian-2-0",
            "name": "Learning in the target language about the present-day culture associated with the target language (everyday activities; customs and traditions; the popular arts and entertainment; the range and role of the mass media)"
          },
          {
            "id": "italian-2-1",
            "name": "Reading modern literary texts (notably novels, short stories, poems and plays, or extracts from these) in the target language"
          },
          {
            "id": "italian-2-2",
            "name": "Describing and discussing everyday life in the target language community"
          },
          {
            "id": "italian-2-3",
            "name": "Understanding, describing and discussing aspects of the relations between the target language community and Ireland"
          },
          {
            "id": "italian-2-4",
            "name": "Understanding, describing and discussing in general terms issues that transcend cultural divisions (e.g. teenager culture; the generation gap; entertainment; environment and ecology; sexual and racial equality; ethnic minorities; health and lifestyle; human relationships such as marriage and the family; the European dimension; the Third World)"
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
            "name": "Meeting and getting to know people and maintaining social relations"
          },
          {
            "id": "russian-0-1",
            "name": "Discussing family and home"
          },
          {
            "id": "russian-0-2",
            "name": "Asking about and describing the general nature of the region or locality in which someone lives"
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
            "name": "Facilitating, encouraging or impeding a course of action"
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
            "name": "Talking and writing about your experience of the target language"
          },
          {
            "id": "russian-1-4",
            "name": "Consulting reference materials (e.g. dictionaries and grammars) relating to the vocabulary and grammar of the target language"
          }
        ]
      },
      {
        "id": "russian-2",
        "name": "Cultural Awareness",
        "subtopics": [
          {
            "id": "russian-2-0",
            "name": "Learning in the target language about the present-day culture associated with the target language (everyday activities; customs and traditions; the arts and entertainment; the range and role of the mass media)"
          },
          {
            "id": "russian-2-1",
            "name": "Reading extracts from modern literary texts (notably novels, short stories, poems and plays) in the target language"
          },
          {
            "id": "russian-2-2",
            "name": "Describing and discussing everyday life in the target language community (comparisons with Ireland; national stereotypes)"
          },
          {
            "id": "russian-2-3",
            "name": "Understanding, describing and discussing aspects of the relations between the target language community and Ireland (e.g. tourism, sport)"
          },
          {
            "id": "russian-2-4",
            "name": "Understanding, describing and discussing in general terms issues that transcend cultural divisions"
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
            "name": "A society in transition (from centralised state to civil society)"
          },
          {
            "id": "russian-2-8",
            "name": "The place of Russia on the world stage (Russia and Europe, Russia and the West, Russia and the Far East, Russia and Central Asia)"
          },
          {
            "id": "russian-2-9",
            "name": "The challenges facing a multi-cultural state (racial equality, ethnic minorities)"
          },
          {
            "id": "russian-2-10",
            "name": "The Russian landscape (environment and ecology)"
          },
          {
            "id": "russian-2-11",
            "name": "Aspects of contemporary Russian life (the generation gap, sexual equality, health and lifestyle, changing perspectives regarding human relationships such as marriage and the family)"
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
            "name": "Meeting and getting to know people and maintaining social relations"
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
            "name": "Understanding, seeking and giving information about climate and weather"
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
            "name": "Requesting, facilitating or impeding a course of action"
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
            "name": "Talking and writing about your experience of the target language"
          },
          {
            "id": "japanese-1-4",
            "name": "Consulting reference materials (e.g. dictionaries and grammars) relating to the vocabulary and grammar of the target language"
          }
        ]
      },
      {
        "id": "japanese-2",
        "name": "Cultural Awareness",
        "subtopics": [
          {
            "id": "japanese-2-0",
            "name": "Learning in the target language about the present-day culture associated with Japan and the Japanese"
          },
          {
            "id": "japanese-2-1",
            "name": "Reading extracts from modern texts of various kinds in the target language"
          },
          {
            "id": "japanese-2-2",
            "name": "Describing and discussing everyday life in the target language community"
          },
          {
            "id": "japanese-2-3",
            "name": "Understanding, describing and discussing aspects of the relations between the target language community and Ireland"
          },
          {
            "id": "japanese-2-4",
            "name": "Understanding, describing and discussing issues that transcend cultural divisions"
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
            "name": "Kanji (the prescribed List of Required Kanji in the syllabus Appendix)"
          }
        ]
      },
      {
        "id": "japanese-4",
        "name": "Assessment — The Four Skills",
        "subtopics": [
          {
            "id": "japanese-4-0",
            "name": "Speaking / Oral examination (general conversation, role-play, development of theme through discussion, picture description and related discussion)"
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
            "name": "Reception (mode of communication)"
          },
          {
            "id": "mandarin-chinese-0-1",
            "name": "Reception: Follow classroom interactions including pair and group work, very simple presentations on familiar topics and basic instructions (CLC1)"
          },
          {
            "id": "mandarin-chinese-0-2",
            "name": "Reception: Explore a range of short, simple authentic oral, written and multi-modal texts in a variety of genres and formats e.g. advertisements, announcements, narratives (CLC2)"
          },
          {
            "id": "mandarin-chinese-0-3",
            "name": "Reception: Identify and gather specific information from short, simple oral, written and multi-modal texts for a particular purpose, especially with visual support (CLC3)"
          },
          {
            "id": "mandarin-chinese-0-4",
            "name": "Reception: Understand a lexical range comprised of individual words and simple expressions (CLC4)"
          },
          {
            "id": "mandarin-chinese-0-5",
            "name": "Reception: Identify simple information consisting of everyday language in oral, written and multi-modal texts, especially with visual support (CLC5)"
          },
          {
            "id": "mandarin-chinese-0-6",
            "name": "Reception: Understand short, simple descriptions of places, events, personal experiences, feelings and perspectives in very simple everyday language (CLC6)"
          },
          {
            "id": "mandarin-chinese-0-7",
            "name": "Interaction (mode of communication)"
          },
          {
            "id": "mandarin-chinese-0-8",
            "name": "Interaction: Deal with simple transactions likely to arise while obtaining goods and services (CLC7)"
          },
          {
            "id": "mandarin-chinese-0-9",
            "name": "Interaction: Give short, very simple accounts of social and personal events, experiences and activities, and respond in face-to-face and online interactions (CLC8)"
          },
          {
            "id": "mandarin-chinese-0-10",
            "name": "Interaction: Use short, very simple expressions and phrases to initiate and close simple conversations, asking for clarifications (CLC9)"
          },
          {
            "id": "mandarin-chinese-0-11",
            "name": "Interaction: Ask and answer simple questions, exchange ideas, express emotions and information on familiar topics in everyday situations (CLC10)"
          },
          {
            "id": "mandarin-chinese-0-12",
            "name": "Production (mode of communication)"
          },
          {
            "id": "mandarin-chinese-0-13",
            "name": "Production: Convey message clearly with generally clear pronunciation (e.g. tones), intonation, stress and rhythm (CLC11)"
          },
          {
            "id": "mandarin-chinese-0-14",
            "name": "Production: Use characters to write short, coherent texts that are clear enough to be understood (CLC12)"
          },
          {
            "id": "mandarin-chinese-0-15",
            "name": "Production: Use basic linguistic patterns, structures and strategies to communicate in familiar contexts (CLC13)"
          },
          {
            "id": "mandarin-chinese-0-16",
            "name": "Production: Describe, in simple language, past, present or future events, activities or experiences (CLC14)"
          },
          {
            "id": "mandarin-chinese-0-17",
            "name": "Production: Express feelings in a simple way, in writing and orally, on subjects relating to everyday life (CLC15)"
          },
          {
            "id": "mandarin-chinese-0-18",
            "name": "Production: Develop a range of creative texts on subjects of personal interest in oral, written and multi-modal formats, e.g. songs, poems, drama, stories (CLC16)"
          },
          {
            "id": "mandarin-chinese-0-19",
            "name": "Mediation (mode of communication)"
          },
          {
            "id": "mandarin-chinese-0-20",
            "name": "Mediation: Convey, in writing or orally, the main points in clear, simple texts on familiar subjects of personal interest (CLC17)"
          },
          {
            "id": "mandarin-chinese-0-21",
            "name": "Mediation: Collaborate in simple practical tasks, asking what others think and understanding responses; ask for repetition or reformulation (CLC18)"
          },
          {
            "id": "mandarin-chinese-0-22",
            "name": "Mediation: Convey simple, predictable information in familiar contexts given in short, simple signs, notices, posters and programmes (CLC19)"
          },
          {
            "id": "mandarin-chinese-0-23",
            "name": "Mediation: Use simple words to ask someone to explain or clarify something (CLC20)"
          },
          {
            "id": "mandarin-chinese-0-24",
            "name": "Mediation: Recognise when speakers disagree or have a problem and use simple words/phrases to indicate empathy and interest (CLC21)"
          },
          {
            "id": "mandarin-chinese-0-25",
            "name": "Mediation: Respond, in writing and orally, to short, simple creative texts about everyday topics, explaining how it made them feel (CLC22)"
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
            "name": "Plurilingual: Make sense of unfamiliar characters by considering constituent parts, such as radicals, word roots and lexical elements (PPC1)"
          },
          {
            "id": "mandarin-chinese-1-2",
            "name": "Plurilingual: Recognise a range of linguistic patterns and structures (such as verbal system, syntax) and understand their meaning in context (PPC2)"
          },
          {
            "id": "mandarin-chinese-1-3",
            "name": "Plurilingual: Apply communication and compensation strategies when communication is impaired (synonyms, gestures, translanguaging) (PPC3)"
          },
          {
            "id": "mandarin-chinese-1-4",
            "name": "Plurilingual: Further develop learning strategies to recall, understand and use the target language for basic oral and written communication (PPC4)"
          },
          {
            "id": "mandarin-chinese-1-5",
            "name": "Plurilingual: Creatively exploit their plurilingual repertoire to communicate in unexpected situations or make sense of short, very simple texts (PPC5)"
          },
          {
            "id": "mandarin-chinese-1-6",
            "name": "Plurilingual: Recognise similarities and differences in the way concepts are expressed and understood across different languages (PPC6)"
          },
          {
            "id": "mandarin-chinese-1-7",
            "name": "Plurilingual: Compare and contrast target languages already known, accounting for features such as tonality or logographic writing system (PPC7)"
          },
          {
            "id": "mandarin-chinese-1-8",
            "name": "Plurilingual: Reflect on the language-learning process, using feedback to improve (PPC8)"
          },
          {
            "id": "mandarin-chinese-1-9",
            "name": "Pluricultural competence: Awareness and understanding of the target language communities and cultures (element)"
          },
          {
            "id": "mandarin-chinese-1-10",
            "name": "Pluricultural: Explore and appreciate popular culture through a range of media (PPC9)"
          },
          {
            "id": "mandarin-chinese-1-11",
            "name": "Pluricultural: Research and discuss aspects of the target language society/societies, such as geographical features, significant historical events, facts, famous people and places (PPC10)"
          },
          {
            "id": "mandarin-chinese-1-12",
            "name": "Pluricultural: Research aspects of the diverse cultural heritage in areas such as cuisine, folklore, music, traditions, the arts, and religions (PPC11)"
          },
          {
            "id": "mandarin-chinese-1-13",
            "name": "Pluricultural: Interpret aspects of cultures and communities in everyday living, social conventions, interpersonal relations, evolving values and beliefs (PPC12)"
          },
          {
            "id": "mandarin-chinese-1-14",
            "name": "Pluricultural: Develop and demonstrate awareness of customs, beliefs and attitudes of people in the target language cultures and communities (PPC13)"
          },
          {
            "id": "mandarin-chinese-1-15",
            "name": "Pluricultural: Explain features of the target language cultures and communities to people with different cultural backgrounds (PPC14)"
          },
          {
            "id": "mandarin-chinese-1-16",
            "name": "Pluricultural: Demonstrate awareness of and use appropriate verbal and non-verbal social conventions when interacting with others (PPC15)"
          },
          {
            "id": "mandarin-chinese-1-17",
            "name": "Pluricultural: Consider similarities and differences between target language culture(s) and other culture(s), recognising the feelings and world views of others (PPC16)"
          },
          {
            "id": "mandarin-chinese-1-18",
            "name": "Pluricultural: Support communication and interaction across cultures by showing interest, empathy, agreement and understanding (PPC17)"
          },
          {
            "id": "mandarin-chinese-1-19",
            "name": "Pluricultural: Explore their own cultural identity and consider common stereotypes of their own and other cultures (PPC18)"
          }
        ]
      },
      {
        "id": "mandarin-chinese-2",
        "name": "Assessment for Certification (exam components)",
        "subtopics": [
          {
            "id": "mandarin-chinese-2-0",
            "name": "Oral examination (Ordinary 30% / Higher 35%) - includes discussion of the Language Portfolio"
          },
          {
            "id": "mandarin-chinese-2-1",
            "name": "Aural examination (Ordinary 30% / Higher 25%) - assesses listening reception and mediation"
          },
          {
            "id": "mandarin-chinese-2-2",
            "name": "Written examination - Reading (Ordinary 25% / Higher 20%) and Writing (Ordinary 15% / Higher 20%); assesses written reception, production and mediation"
          },
          {
            "id": "mandarin-chinese-2-3",
            "name": "Language Portfolio (stimulus for oral discussion; not assessed for certification)"
          },
          {
            "id": "mandarin-chinese-2-4",
            "name": "Pin Yin and simplified characters (Pin Yin used as a building block but not formally assessed; texts in simplified characters)"
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
            "name": "Different text formats: narratives, plays, speeches, types of poetry, inscriptions, graffiti, mottos"
          },
          {
            "id": "latin-0-2",
            "name": "Different ways of reading: for pleasure, linguistic practice, research, interpretation, comparison"
          },
          {
            "id": "latin-0-3",
            "name": "Learning words and expressions, and strategies to do this"
          },
          {
            "id": "latin-0-4",
            "name": "Lexical phenomena: idiomatic, poetic and colloquial expressions, metaphors"
          },
          {
            "id": "latin-0-5",
            "name": "Pronunciation: how Latin may have sounded as a living language; tone, stress, rhythm, metre"
          },
          {
            "id": "latin-0-6",
            "name": "Composition into Latin"
          },
          {
            "id": "latin-0-7",
            "name": "Distinguishing stem and ending; how parts of words change to convey meaning"
          },
          {
            "id": "latin-0-8",
            "name": "Translation: creating accurate and idiomatic translations of sentences and passages"
          },
          {
            "id": "latin-0-9",
            "name": "How source and target language convey meaning differently; the role of the translator as interpreter, mediator and creator"
          },
          {
            "id": "latin-0-10",
            "name": "Evaluating information in texts: style, register, tone, mood, purpose; questions, premises and claims; viewpoints; arguments and conclusions"
          },
          {
            "id": "latin-0-11",
            "name": "Distinctive literary techniques, formal features and figures of style"
          },
          {
            "id": "latin-0-12",
            "name": "Developing language awareness and analytical skills (core element)"
          },
          {
            "id": "latin-0-13",
            "name": "Morphology and syntax; word types, inflection, grammatical functions, word order"
          },
          {
            "id": "latin-0-14",
            "name": "Constituent parts of words: roots, stems, prefixes, suffixes, endings"
          },
          {
            "id": "latin-0-15",
            "name": "Word types: nouns, adjectives, pronouns, adverbs, finite verbs, infinitives, participles"
          },
          {
            "id": "latin-0-16",
            "name": "Inflection patterns: nominal declensions and verbal conjugations"
          },
          {
            "id": "latin-0-17",
            "name": "Main clauses and main verbs, participial and infinitive constructions, subordinate clauses and conditionals"
          },
          {
            "id": "latin-0-18",
            "name": "Spelling and punctuation conventions"
          },
          {
            "id": "latin-0-19",
            "name": "Logical reasoning from syntactical construction, word-order, cases and their grammatical functions"
          },
          {
            "id": "latin-0-20",
            "name": "Using dictionaries, vocabulary lists, grammars, parsing tools and commentaries (traditional and electronic)"
          },
          {
            "id": "latin-0-21",
            "name": "Comparing languages: similarities and differences in linguistic patterns and lexical expressions across languages"
          },
          {
            "id": "latin-0-22",
            "name": "Etymology of words derived from Latin in English, Irish and Romance languages; derivatives and cognates"
          },
          {
            "id": "latin-0-23",
            "name": "Culture-specific abstract concepts with no direct equivalent: e.g. virtus, otium, officium"
          },
          {
            "id": "latin-0-24",
            "name": "How word choice, syntax, grammar and text structure vary with genre, purpose, context and period (e.g. classical vs medieval, epic vs graffiti)"
          },
          {
            "id": "latin-0-25",
            "name": "Monitoring language confidence, learning strategies and use of resources; creating flashcards and graphic organisers"
          },
          {
            "id": "latin-0-26",
            "name": "Prescribed grammatical forms and constructions for examination (Higher and Ordinary level, per annual circular)"
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
            "name": "Responding to texts: relating events to personal values; significance of events and settings; connections between text and context"
          },
          {
            "id": "latin-1-2",
            "name": "Investigating characters and their relationships, attitudes, dilemmas and decisions"
          },
          {
            "id": "latin-1-3",
            "name": "Researching the context of Latin texts and their authors; reliability and relevance of sources"
          },
          {
            "id": "latin-1-4",
            "name": "Contexts relevant to understanding texts: history, politics, ideology, philosophy, social norms, visual art, architecture, material culture"
          },
          {
            "id": "latin-1-5",
            "name": "Close reading: attention to word choice, grammar, syntax and text structure for in-depth study"
          },
          {
            "id": "latin-1-6",
            "name": "Significance of a literary text for its original audience versus its relevance to audiences today"
          },
          {
            "id": "latin-1-7",
            "name": "Reception of Latin literature: portrayal of Romans in modern media such as film, games and historical fiction"
          },
          {
            "id": "latin-1-8",
            "name": "Continued importance and survival of Latin as a language of literature, learning, science and religion over time, across the world and in Ireland"
          },
          {
            "id": "latin-1-9",
            "name": "Roman culture explored through Latin texts (core element)"
          },
          {
            "id": "latin-1-10",
            "name": "Regions, communities and cultures who have used Latin; places, significant historical events and people encountered in texts"
          },
          {
            "id": "latin-1-11",
            "name": "Cultural heritage and daily life of ancient Rome: myths and legends, the arts, traditions, religion, housing, cuisine"
          },
          {
            "id": "latin-1-12",
            "name": "Roman values and attitudes; social hierarchy, status, social conventions, interpersonal relations, beliefs and customs"
          },
          {
            "id": "latin-1-13",
            "name": "Critically discussing Roman society, history, politics and culture"
          },
          {
            "id": "latin-1-14",
            "name": "Roman cultural identity and self-representation; representation of 'others' and ideas of what it means to be a Roman (elite male) citizen; reflecting on one's own perceptions, biases and assumptions"
          }
        ]
      },
      {
        "id": "latin-2",
        "name": "Capstone Text and Assessment Components",
        "subtopics": [
          {
            "id": "latin-2-0",
            "name": "Capstone text: prescribed author, title and specified passages (per annual Department of Education circular)"
          },
          {
            "id": "latin-2-1",
            "name": "Capstone text general context: literary, cultural and historical aspects"
          },
          {
            "id": "latin-2-2",
            "name": "Written examination (60%) - Higher and Ordinary level"
          },
          {
            "id": "latin-2-3",
            "name": "Additional assessment component: Research study - 'text in context' (40%), based on an SEC brief, ~20 hours"
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
            "name": "1.1 Explore a range of authentic, adapted and confected Ancient Greek texts in a variety of genres and formats (narratives, plays, speeches, types of poetry, inscriptions, graffiti, mottos)"
          },
          {
            "id": "ancient-greek-0-2",
            "name": "1.2 Recognise lexical items at the level of words, expressions and collocations in context (learning words/expressions and strategies)"
          },
          {
            "id": "ancient-greek-0-3",
            "name": "1.3 Pronounce Ancient Greek words, phrases and sentences accurately, with appropriate intonation and rhythm (how Ancient Greek may have sounded; tone, stress, rhythm, metre)"
          },
          {
            "id": "ancient-greek-0-4",
            "name": "1.4 Collaborate with others to understand Ancient Greek"
          },
          {
            "id": "ancient-greek-0-5",
            "name": "1.5 Explore vocabulary and grammatical rules by completing and transforming phrases and sentences (composition into Ancient Greek; stem and ending)"
          },
          {
            "id": "ancient-greek-0-6",
            "name": "1.6 Create accurate and idiomatic translations of Ancient Greek sentences and passages (applying vocabulary, grammar and context; how languages convey meaning differently)"
          },
          {
            "id": "ancient-greek-0-7",
            "name": "1.7 Evaluate information contained in Ancient Greek texts for a particular purpose (style, register, tone, mood, purpose; questions, premises, claims; viewpoints; arguments and conclusions)"
          },
          {
            "id": "ancient-greek-0-8",
            "name": "1.8 Describe the content and structure of Ancient Greek texts (summarising, listing, classifying; creative ways of presenting understanding)"
          },
          {
            "id": "ancient-greek-0-9",
            "name": "1.9 Evaluate different translations of an Ancient Greek text (the translator as interpreter, mediator and creator)"
          },
          {
            "id": "ancient-greek-0-10",
            "name": "1.10 Appreciate distinctive features and aims of Ancient Greek texts (distinctive literary techniques, formal features and figures of style)"
          },
          {
            "id": "ancient-greek-0-11",
            "name": "Element: Developing language awareness and analytical skills"
          },
          {
            "id": "ancient-greek-0-12",
            "name": "1.11 Make sense of unfamiliar Ancient Greek words and word forms by considering constituent parts and context (comparative reasoning; word families)"
          },
          {
            "id": "ancient-greek-0-13",
            "name": "1.12 Recognise linguistic patterns and structures and explain their use (morphology and syntax; word types, inflection, grammatical functions, word order; spelling and punctuation; roots, stems, prefixes, suffixes, endings)"
          },
          {
            "id": "ancient-greek-0-14",
            "name": "1.13 Explain the reasoning that led to a specific interpretation of a phrase or sentence (logical reasoning from syntax, word-order, cases and grammatical functions)"
          },
          {
            "id": "ancient-greek-0-15",
            "name": "1.14 Effectively use Ancient Greek language resources (dictionaries, vocabulary lists, grammars, commentaries, traditional and electronic)"
          },
          {
            "id": "ancient-greek-0-16",
            "name": "1.15 Monitor and assess own language confidence, learning strategies and use of resources (taking ownership; graphic organisers and flashcards)"
          },
          {
            "id": "ancient-greek-0-17",
            "name": "1.16 Recognise similarities and differences in how concepts are expressed across languages (culture-specific concepts such as dikē, philia, logos)"
          },
          {
            "id": "ancient-greek-0-18",
            "name": "1.17 Compare and contrast known languages to support comprehension of Ancient Greek texts"
          },
          {
            "id": "ancient-greek-0-19",
            "name": "1.18 Investigate the etymology of words derived from Ancient Greek (in English, Irish, French, etc.)"
          },
          {
            "id": "ancient-greek-0-20",
            "name": "1.19 Assess how word choice, syntax, grammar and text structure vary with genre, purpose, context and period (e.g. Attic vs koine, epic poetry vs fables)"
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
            "name": "2.1 Give a response to Ancient Greek texts (relating events to personal values; significance of events/settings; connecting text and context; investigating characters, relationships, attitudes, dilemmas, decisions)"
          },
          {
            "id": "ancient-greek-1-2",
            "name": "2.2 Research the context of Ancient Greek texts and their authors (using a text to gain information about its time period; evaluating reliability and relevance of information)"
          },
          {
            "id": "ancient-greek-1-3",
            "name": "2.3 Explain specific aspects of a text with reference to its various contexts (history, politics, ideology, philosophy, social norms, visual art, architecture, material culture)"
          },
          {
            "id": "ancient-greek-1-4",
            "name": "2.4 Employ close reading to support interpretation with reference to the words of the text (attention to word choice, grammar, syntax, text structure)"
          },
          {
            "id": "ancient-greek-1-5",
            "name": "2.5 Consider the significance a literary text has for its audience (significance for original audience vs relevance to audiences today)"
          },
          {
            "id": "ancient-greek-1-6",
            "name": "2.6 Examine examples of reception of an Ancient Greek literary text (reception over time; portrayal of ancient Greeks in modern media such as film, games, historical fiction)"
          },
          {
            "id": "ancient-greek-1-7",
            "name": "2.7 Appreciate the continued importance of Ancient Greek as a language of literature, learning, science and religion over time, across the world and in Ireland (survival and ongoing relevance of the Greek language since antiquity)"
          },
          {
            "id": "ancient-greek-1-8",
            "name": "Element: Hellenic culture explored through Ancient Greek texts"
          },
          {
            "id": "ancient-greek-1-9",
            "name": "2.8 Research and discuss the regions, communities and cultures who have used Ancient Greek (places, significant historical events and people encountered in texts)"
          },
          {
            "id": "ancient-greek-1-10",
            "name": "2.9 Examine the diverse cultural heritage and daily life of ancient Greece and the Hellenic world (myths and legends, the arts, traditions, religion, housing, cuisine)"
          },
          {
            "id": "ancient-greek-1-11",
            "name": "2.10 Examine what Ancient Greek texts reveal about Greek values and attitudes (texts as evidence for social hierarchy, status, conventions, interpersonal relations, values, beliefs, customs, attitudes)"
          },
          {
            "id": "ancient-greek-1-12",
            "name": "2.11 Critically discuss aspects of ancient Greek society, history, politics and culture (representation of 'others'; literary and historical representations including stereotypes, biases and propaganda)"
          },
          {
            "id": "ancient-greek-1-13",
            "name": "2.12 Use Ancient Greek texts to examine Greek cultural identity and self-representation, reflecting on own perceptions, biases and assumptions ('otherness' in the Hellenic world; representation of women, foreigners and slaves)"
          }
        ]
      },
      {
        "id": "ancient-greek-2",
        "name": "Capstone Text & Prescribed Material (cross-strand examination focus)",
        "subtopics": [
          {
            "id": "ancient-greek-2-0",
            "name": "The Capstone text: prescribed title and author with specified passages in Ancient Greek (issued by Department of Education circular each examination year)"
          },
          {
            "id": "ancient-greek-2-1",
            "name": "Guidance on general context of the Capstone text (literary, cultural, historical aspects)"
          },
          {
            "id": "ancient-greek-2-2",
            "name": "Prescribed grammatical forms and constructions for examination (separate lists for Higher and Ordinary level)"
          }
        ]
      },
      {
        "id": "ancient-greek-3",
        "name": "Additional Assessment Component: Research Study – Text in Context (40%)",
        "subtopics": [
          {
            "id": "ancient-greek-3-0",
            "name": "Investigate a significant but manageable aspect of language or a short Ancient Greek text/extract, anchored in the specification, chosen under a common SEC brief"
          },
          {
            "id": "ancient-greek-3-1",
            "name": "Research Ancient Greek texts and process linguistic and contextual information"
          },
          {
            "id": "ancient-greek-3-2",
            "name": "Synthesise and evaluate information and make an informed judgement; language-based analysis central"
          },
          {
            "id": "ancient-greek-3-3",
            "name": "Explore the broader context (literary, linguistic, artistic, historical, cultural, social, political, philosophical or religious significance) of the classical world"
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
            "name": "Family (structure, roles, values and purpose of the family as perceived by the Hebrews in Biblical and early post-Biblical development)"
          },
          {
            "id": "hebrew-studies-0-1",
            "name": "Family — Old Testament texts: Gen 2.18; 15.1-5; 21.1-8; 24.1-27, 61-67; Ex 20.1-17; Deut 24.1-4; 25.5-10; Ruth 4; Ps 128; Prov 31.10-31"
          },
          {
            "id": "hebrew-studies-0-2",
            "name": "Family — Mishnah texts: Ta'Anit 4m.8; Av 5m.21 (first half); Peah 1m.1"
          },
          {
            "id": "hebrew-studies-0-3",
            "name": "Government and Monarchy (the place of Monarchy in Israelite society and its tensions/conflicts; the religious understanding of the monarchic institution)"
          },
          {
            "id": "hebrew-studies-0-4",
            "name": "Government and Monarchy — Old Testament texts: Gen 42.12-27; Deut 17.14-20; Judg 9.1-21; 1 Sam 8; 24; 2 Sam 15.1-16; 1 Kings 1.15-53"
          },
          {
            "id": "hebrew-studies-0-5",
            "name": "Government and Monarchy — Mishnah texts: Av 3m.2 (first part); Sot 7m.8; Sanh 2m.3"
          }
        ]
      },
      {
        "id": "hebrew-studies-1",
        "name": "Section B",
        "subtopics": [
          {
            "id": "hebrew-studies-1-0",
            "name": "Prophetic Protest (the role and position of the prophet in relation to leadership and the masses; the nature and substance of prophetic protest into early post-Biblical times)"
          },
          {
            "id": "hebrew-studies-1-1",
            "name": "Prophetic Protest — Old Testament texts: 2 Sam 12.1-25; 1 Kings 18.17-39; 21; Amos 5.4-24; Is 58; Jer 1; 22.11-19"
          },
          {
            "id": "hebrew-studies-1-2",
            "name": "Prophetic Protest — Mishnah texts: Av 1m.2, 10, 18; 2m.3; 5m.17; 6m.5"
          },
          {
            "id": "hebrew-studies-1-3",
            "name": "Wisdom (the context and background of wisdom teaching; the values and ideas in wisdom literature and their early post-Biblical expression and development)"
          },
          {
            "id": "hebrew-studies-1-4",
            "name": "Wisdom — Old Testament texts: Prov 2.1-8; 24.13-34; Eccles 3.1-15; 12"
          },
          {
            "id": "hebrew-studies-1-5",
            "name": "Wisdom — Mishnah texts: Av 1m.12, 14; 2m.5, 12; 3m.18; 4m.1, 2; 6m.5"
          },
          {
            "id": "hebrew-studies-1-6",
            "name": "Wisdom — Additional reading (recommended, not prescribed): Job; 1 Kings 3.5-14; 4.29-34 (English version); 5.9-14; Mishnah Ber 9m.5"
          }
        ]
      },
      {
        "id": "hebrew-studies-2",
        "name": "Section C",
        "subtopics": [
          {
            "id": "hebrew-studies-2-0",
            "name": "Worship (Sacrifice and Prayer) — the role and development of worship; the place of sacrifice and liturgy; the position of the Temple; the role of the Priesthood and the Levites"
          },
          {
            "id": "hebrew-studies-2-1",
            "name": "Worship — Old Testament texts: Num 6.22-27; Deut 6.4-9; 12.11-19; 1 Kings 8.1-21; Ps 20; 24; 122; 134"
          },
          {
            "id": "hebrew-studies-2-2",
            "name": "Worship — Mishnah texts: Sot 7m.6; Ber 1m.3; 4m.1, 2, 3, 4, 5, 6; 5m.1, 2, 3, 5; Av 2m.13; Tamid 6m.4"
          },
          {
            "id": "hebrew-studies-2-3",
            "name": "Festivals and Symbols (the form and substance of the Festivals in Hebrew life, Biblical and early post-Biblical; the form, substance and significance of religious symbols in Jewish life within calendar and daily contexts)"
          },
          {
            "id": "hebrew-studies-2-4",
            "name": "Festivals and Symbols — Old Testament texts: Ex 12; 13.1-16; Lev 23; Josh 5.4-12 (Passover); 1 Sam 20.18-42 (New Moon); 1 Kings 8.55-66 (Tabernacles); 2 Kings 23.21-25 (Passover); Neh 8.3-18 (Tabernacles); 1 Mac 4.52-59; Num 15.37-41; Deut 6.4-9; 11.13-31"
          },
          {
            "id": "hebrew-studies-2-5",
            "name": "Festivals and Symbols — Mishnah texts: Sukkah 1m.1; 3m.4; Pesachim 10m.1, 5; Bikkurim 3m.3, 6; Yoma 6m.2; 8m.1, 9; Rosh Hashanah 4m.8, 9; Megillah 1m.8; 3m.6 (Purim and Chanukah)"
          }
        ]
      },
      {
        "id": "hebrew-studies-3",
        "name": "Section D",
        "subtopics": [
          {
            "id": "hebrew-studies-3-0",
            "name": "Election and Covenant (how the idea of covenant is used to define the relationship between the people and God)"
          },
          {
            "id": "hebrew-studies-3-1",
            "name": "Election and Covenant — Old Testament texts: Gen 15.7-21; Ex 19.1-8; Deut 26.5-9, 16-19; 29.9-28; 30.19-20; Josh 24.1-28; 1 Sam 12.7-25; 2 Sam 7; 2 Kings 23.1-8; Jer 31.31-34; Neh 9-10.1 (= 9 in English version)"
          },
          {
            "id": "hebrew-studies-3-2",
            "name": "Election and Covenant — Mishnah texts: Av 1m.1; 3m.15; Ta'Anit 2m.4"
          },
          {
            "id": "hebrew-studies-3-3",
            "name": "Messianism (the nature of Messianism across Biblical and early post-Biblical literature; the idea in relation to the historical circumstances that nurtured it)"
          },
          {
            "id": "hebrew-studies-3-4",
            "name": "Messianism — Old Testament texts: Deut 30.1-10; Is 11.1-10; 40.1-11; 54; Jer 31.1-20; 32.6-15; 36-44; Ezek 37; Micah 4.1-5; Mal 3.19-24; Zach 9.9-17; Ps 20"
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
            "name": "Reception (understanding/processing spoken, written and multimodal Arabic: following classroom interactions; engaging with authentic literary and non-literary texts; gathering specific information; wide lexical range, idioms and collocations; identifying main argument, viewpoints and conclusions; understanding news bulletins, advertisements, announcements, narratives; understanding descriptions of people, places, events, experiences, feelings)"
          },
          {
            "id": "arabic-0-1",
            "name": "Interaction (oral and written exchanges: asking/answering questions, making plans, solving problems; discussion and debate on familiar/current topics; transactions for goods and services; expressions, phrases and idioms to initiate, maintain and close conversations; strategies to focus a discussion)"
          },
          {
            "id": "arabic-0-2",
            "name": "Production (speaking and writing in a range of genres: composing and responding to written communications; giving accounts of social and personal events; clear pronunciation, intonation, stress and rhythm; coherent text using spelling, punctuation and linguistic devices; expressing opinions, feelings and experiences; creating songs, poems, drama, stories)"
          },
          {
            "id": "arabic-0-3",
            "name": "Mediation (conveying main points of texts; collaborating in practical tasks; communicating what is heard/read; supporting a shared communication culture; responding to creative texts; explaining ideas and problems, summarising data, weighing advantages and disadvantages)"
          }
        ]
      },
      {
        "id": "arabic-1",
        "name": "Strand 2: Plurilingual and Pluricultural Competence Strand",
        "subtopics": [
          {
            "id": "arabic-1-0",
            "name": "Plurilingual Competence (word roots and lexical elements; using language resources/dictionaries independently; linguistic patterns and structures; communication and compensation strategies; language-learning strategies; exploiting a plurilingual repertoire across dialects; comparing/contrasting linguistic patterns across languages; reflecting on the language-learning process)"
          },
          {
            "id": "arabic-1-1",
            "name": "Pluricultural Competence (popular culture through media; geography, history, famous people and places of Arabic-speaking countries; cultural heritage - cuisine, folklore, music, traditions, arts, religions; social conventions, interpersonal relations, values and beliefs; customs, beliefs and attitudes; verbal and non-verbal social conventions; comparing cultures respectfully; supporting intercultural communication)"
          }
        ]
      },
      {
        "id": "arabic-2",
        "name": "Assessment for Certification (new specification, 2025 intake onward)",
        "subtopics": [
          {
            "id": "arabic-2-0",
            "name": "Oral examination - additional assessment component (HL 30% / OL 25%; common tasks at both levels; discussion of texts from the Language Portfolio)"
          },
          {
            "id": "arabic-2-1",
            "name": "Aural examination - additional assessment component (HL 25% / OL 30%; at Higher and Ordinary level)"
          },
          {
            "id": "arabic-2-2",
            "name": "Written examination - Reading (HL 25% / OL 30%)"
          },
          {
            "id": "arabic-2-3",
            "name": "Written examination - Writing (HL 20% / OL 15%)"
          },
          {
            "id": "arabic-2-4",
            "name": "Language Portfolio (developed over two years; stimulus for the oral examination; content not itself certified)"
          }
        ]
      },
      {
        "id": "arabic-3",
        "name": "Interim Syllabus: Reading and Directed Writing",
        "subtopics": [
          {
            "id": "arabic-3-0",
            "name": "Understanding and conveying information; ordering and presenting facts, ideas and opinions"
          },
          {
            "id": "arabic-3-1",
            "name": "Evaluating information and selecting what is relevant to specific purposes"
          },
          {
            "id": "arabic-3-2",
            "name": "Scanning for and extracting specific information; organising and presenting material in a given format"
          },
          {
            "id": "arabic-3-3",
            "name": "Identifying main and subordinate topics; summarising, paraphrasing, re-expressing"
          },
          {
            "id": "arabic-3-4",
            "name": "Recognising and responding to linguistic devices including figurative language; recognising implicit meaning and attitudes"
          },
          {
            "id": "arabic-3-5",
            "name": "Higher level: precise understanding of extended texts; drawing inferences, evaluating, comparing, analysing, synthesising; editing or elaborating the work of others"
          }
        ]
      },
      {
        "id": "arabic-4",
        "name": "Interim Syllabus: Continuous Writing",
        "subtopics": [
          {
            "id": "arabic-4-0",
            "name": "Articulating experience and expressing what is felt and imagined; ordering and presenting facts, ideas and opinions"
          },
          {
            "id": "arabic-4-1",
            "name": "Demonstrating adequate control of vocabulary, syntax, grammar and punctuation"
          },
          {
            "id": "arabic-4-2",
            "name": "Expressing thoughts, feelings and opinions to interest, inform or convince"
          },
          {
            "id": "arabic-4-3",
            "name": "Higher level: wider sense of audience and context; paragraphing; sophisticated use of vocabulary and structures (imaginative, narrative or argumentative composition, 300-400 words)"
          }
        ]
      },
      {
        "id": "arabic-5",
        "name": "Interim Syllabus: Use of Language",
        "subtopics": [
          {
            "id": "arabic-5-0",
            "name": "Exercising control of appropriate grammatical structures"
          },
          {
            "id": "arabic-5-1",
            "name": "Conventions of paragraphing, sentence structure and punctuation"
          },
          {
            "id": "arabic-5-2",
            "name": "Understanding and employing a range of apt vocabulary"
          },
          {
            "id": "arabic-5-3",
            "name": "Sense of audience and awareness of register and style in formal and informal situations"
          },
          {
            "id": "arabic-5-4",
            "name": "Writing accurate simple/complex sentences; varied sentence structure; well-constructed paragraphs"
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
            "name": "Understanding and commenting on set texts (textual and contextual questions)"
          }
        ]
      },
      {
        "id": "arabic-7",
        "name": "Interim Syllabus: Reading Comprehension (unseen texts)",
        "subtopics": [
          {
            "id": "arabic-7-0",
            "name": "Letters, newspaper or magazine articles, and works of literature (prose extract with multiple-choice and open-ended questions)"
          },
          {
            "id": "arabic-7-1",
            "name": "Exploring levels of meaning within a text; awareness of stylistic aspects; author's attitude and use of language"
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
            "name": "Characteristics and types of heroes and leaders (qualities, abilities, decision-making, relevance to modern leaders)"
          },
          {
            "id": "classical-studies-0-1",
            "name": "Heroic society (myths and legends underpinning the epics; gods and divine intervention; impact of war; portrayal of women; Virgil's Aeneid as Augustan propaganda; values in daily life)"
          },
          {
            "id": "classical-studies-0-2",
            "name": "Heroic narratives (key events, plot and locations; poetic devices such as epithets and similes; storytelling techniques; visual representation of heroes and ecphrasis)"
          },
          {
            "id": "classical-studies-0-3",
            "name": "Homer's Odyssey (prescribed epic text)"
          },
          {
            "id": "classical-studies-0-4",
            "name": "Virgil's Aeneid, with emphasis on Books 1-6 (prescribed epic text)"
          }
        ]
      },
      {
        "id": "classical-studies-1",
        "name": "Strand 2: Drama and spectacle",
        "subtopics": [
          {
            "id": "classical-studies-1-0",
            "name": "Greek tragedy (plot and structure; core themes; social and democratic political norms; dramatic devices such as dramatic irony, catharsis, recognition, reversal, divine prologues and deus ex machina)"
          },
          {
            "id": "classical-studies-1-1",
            "name": "The context of Greek tragedy (audience experience, theatre design, costumes, masks, props, actors and chorus; the Dionysia festival; theatres as focal points of civic life)"
          },
          {
            "id": "classical-studies-1-2",
            "name": "Prescribed tragedy (one play studied from a rotating pairing: Euripides' Medea / Sophocles' Philoctetes; Sophocles' Oedipus the King / Euripides' Trojan Women; Aeschylus' Prometheus Bound / Sophocles' Antigone)"
          },
          {
            "id": "classical-studies-1-3",
            "name": "The Colosseum, the Circus Maximus and Roman spectacle (architecture; audience experience and seating; types of entertainment; funding, building and organisation; written sources; comparison with Athenian tragedy and modern entertainment)"
          }
        ]
      },
      {
        "id": "classical-studies-2",
        "name": "Strand 3: Power and identity",
        "subtopics": [
          {
            "id": "classical-studies-2-0",
            "name": "The time of Alexander or Caesar (key historical events; political and social tensions; changing political geography before and after the conquests)"
          },
          {
            "id": "classical-studies-2-1",
            "name": "The political and military exploits of Alexander or Caesar (outline of life; Alexander's Persian campaign or Caesar's Gallic campaign; army composition and tactics in a major military event)"
          },
          {
            "id": "classical-studies-2-2",
            "name": "The characterisation of Alexander or Caesar (depiction in the literary texts; relevance of text type such as biography, autobiography, history; how texts select, present and assess actions and decisions)"
          },
          {
            "id": "classical-studies-2-3",
            "name": "The attitudes of Alexander and Caesar towards foreign peoples (Alexander and the Persians vs. Caesar and the Gauls; cultural ambitions and conceptions of 'civilised' and 'barbarian')"
          },
          {
            "id": "classical-studies-2-4",
            "name": "Prescribed literary sources: Plutarch's Lives of Alexander and Caesar, Arrian's Anabasis, and Caesar's Gallic War"
          }
        ]
      },
      {
        "id": "classical-studies-3",
        "name": "Strand 4: Gods and humans",
        "subtopics": [
          {
            "id": "classical-studies-3-0",
            "name": "The Greek and Roman gods (identifying gods by physical characteristics and attributes; matching Greek and Roman names; domains and relationships within the pantheon; ancient explanations of the gods' origins, nature and purpose)"
          },
          {
            "id": "classical-studies-3-1",
            "name": "The Athenian Parthenon and Erechtheion and the Roman Pantheon and Temple of Vesta (architectural terminology; structure, design and sculptures; attendees and officials; political and civic importance of temples and rituals)"
          },
          {
            "id": "classical-studies-3-2",
            "name": "Greek and Roman funerary practices and the afterlife (material and textual evidence; key elements of funerals; perceptions of the afterlife; comparison with modern practices)"
          },
          {
            "id": "classical-studies-3-3",
            "name": "Philosophical ideas about mortality and living well (Socrates as depicted in Plato's Crito and Horace in the Odes and Epodes; human decision and responsibility vs. divine will and fate; relating ancient ideas to one's own views on living well)"
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
            "name": "Reception (listening and reading): following classroom interactions, instructions and presentations; exploring authentic oral, written and multi-modal texts for pleasure, research or comparison; identifying and gathering specific information; understanding a wide lexical range including idioms and collocations; identifying factual information, main argument, viewpoints and conclusions; understanding news bulletins, advertisements, announcements and narratives; understanding descriptions of places, events, experiences, feelings and perspectives (CLC1-CLC7)"
          },
          {
            "id": "lithuanian-0-1",
            "name": "Interaction (spoken interaction): discussing topics of interest, exchanging information, comparing viewpoints and suggesting solutions; dealing with transactions to obtain goods and services; giving accounts of social and personal events in real time; initiating, maintaining and closing conversations; using strategies to focus a discussion (summarising, reporting back, inviting others to contribute) (CLC8-CLC12)"
          },
          {
            "id": "lithuanian-0-2",
            "name": "Production (speaking and writing): conveying messages with clear pronunciation, intonation, stress and rhythm; using linguistic patterns and structures with reasonable precision; producing continuous, coherent text with appropriate spelling, punctuation and linking devices; expressing opinions, feelings and experiences and justifying viewpoints; developing creative texts (songs, poems, drama, stories) in oral, written and multi-modal formats (CLC13-CLC17)"
          },
          {
            "id": "lithuanian-0-3",
            "name": "Mediation: conveying main points of clear, well-structured texts; collaborating in simple practical tasks; communicating the main point of what is heard or read; supporting a shared communication culture and seeking compromise; responding to creative texts; explaining ideas and problems, summarising factual information including data, and giving a personal response (CLC18-CLC23)"
          }
        ]
      },
      {
        "id": "lithuanian-1",
        "name": "Plurilingual and Pluricultural Competence",
        "subtopics": [
          {
            "id": "lithuanian-1-0",
            "name": "Plurilingual competence: making sense of unfamiliar words via word roots and context; recognising linguistic patterns and structures (verbal system, syntax); applying communication and compensation strategies (synonyms, gestures, translanguaging); developing learning strategies; exploiting the plurilingual repertoire; recognising similarities and differences in how concepts are expressed across languages; comparing and contrasting linguistic patterns and lexical expressions; reflecting on the language-learning process using feedback (PPC1-PPC8)"
          },
          {
            "id": "lithuanian-1-1",
            "name": "Pluricultural competence: exploring popular culture through media; researching the target-language country/countries, communities and cultures (geographical features, significant historical events, famous people and places); researching cultural heritage (cuisine, folklore, music, traditions, the arts, religions); interpreting everyday living, social conventions, interpersonal relations and evolving values and beliefs; awareness of customs, beliefs and attitudes; explaining cultural features to others; using verbal and non-verbal social conventions; comparing target-language and other cultures; exploring one's own cultural identity and stereotypes (PPC9-PPC18)"
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
            "name": "Reception (listening, reading and viewing oral, written and multi-modal texts; following classroom interactions; gathering specific information; understanding lexical range, idioms and collocations; identifying main argument, viewpoints and conclusions; understanding descriptions of places, events, experiences and feelings)"
          },
          {
            "id": "polish-0-1",
            "name": "Interaction (discussing topics of interest; exchanging information; comparing viewpoints; handling transactions for goods and services; giving accounts of social/personal events in real time; initiating, maintaining and closing conversations; using strategies to focus a discussion)"
          },
          {
            "id": "polish-0-2",
            "name": "Production (clear pronunciation, intonation, stress and rhythm; using linguistic patterns and structures with precision; producing continuous coherent text with spelling and punctuation; expressing opinions, feelings and experiences; creating creative texts such as songs, poems, drama and stories)"
          },
          {
            "id": "polish-0-3",
            "name": "Mediation (conveying main points of well-structured texts; collaborating in practical tasks; communicating the main point of what is heard/read; supporting a shared communication culture; responding to creative texts; explaining ideas and problems and summarising factual information)"
          }
        ]
      },
      {
        "id": "polish-1",
        "name": "Plurilingual and Pluricultural Competence",
        "subtopics": [
          {
            "id": "polish-1-0",
            "name": "Plurilingual competence (deducing meaning of unfamiliar words from word roots and context; recognising linguistic patterns and structures such as the verbal system and syntax; applying communication and compensation strategies including translanguaging; developing learning strategies; exploiting the plurilingual repertoire; comparing linguistic patterns and lexical expressions across languages; reflecting on the language-learning process)"
          },
          {
            "id": "polish-1-1",
            "name": "Pluricultural competence (exploring popular culture through media; researching geographical features, historical events, famous people and places of the target-language country/countries; researching cultural heritage such as cuisine, folklore, music, traditions, the arts and religions; interpreting social conventions, interpersonal relations, values and beliefs; awareness of customs, beliefs and attitudes; explaining cultural features to others; using verbal and non-verbal social conventions; comparing cultures respectfully; exploring own cultural identity and stereotypes)"
          }
        ]
      },
      {
        "id": "polish-2",
        "name": "Assessment Components and Language Portfolio",
        "subtopics": [
          {
            "id": "polish-2-0",
            "name": "Oral examination (Higher Level 30%) - spoken reception, interaction, production and mediation; awareness of target-language communities and cultures; discussion of texts from the Language Portfolio"
          },
          {
            "id": "polish-2-1",
            "name": "Aural examination (Higher Level 25%) - listening reception and mediation"
          },
          {
            "id": "polish-2-2",
            "name": "Written examination - Reading (Higher Level 25%) - written reception across a range of texts"
          },
          {
            "id": "polish-2-3",
            "name": "Written examination - Writing (Higher Level 20%) - written production and mediation"
          },
          {
            "id": "polish-2-4",
            "name": "Language Portfolio - record and reflect on language journey across the four modes of communication; stimulus for the oral examination (not assessed directly for certification)"
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
            "name": "Reception (understanding oral, written and multi-modal texts)"
          },
          {
            "id": "portuguese-0-1",
            "name": "Interaction (discussing, exchanging information, transactions, conversations)"
          },
          {
            "id": "portuguese-0-2",
            "name": "Production (speaking and writing: opinions, descriptions, creative texts)"
          },
          {
            "id": "portuguese-0-3",
            "name": "Mediation (conveying/summarising main points, collaborating, cross-cultural communication)"
          }
        ]
      },
      {
        "id": "portuguese-1",
        "name": "Plurilingual and Pluricultural Competence",
        "subtopics": [
          {
            "id": "portuguese-1-0",
            "name": "Plurilingual competence (word roots/lexical elements, linguistic patterns and structures, compensation strategies, learning strategies, comparing languages)"
          },
          {
            "id": "portuguese-1-1",
            "name": "Pluricultural competence (popular culture; geography, history, famous people and places; cultural heritage – cuisine, folklore, music, traditions, arts, religions; social conventions; customs, beliefs and attitudes; cultural identity and stereotypes)"
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
            "name": "Statistical reasoning with an aim to becoming a statistically aware consumer"
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
            "name": "Analysing, interpreting and drawing inferences from data"
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
            "name": "Statistical reasoning with an aim to becoming a statistically aware consumer"
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
            "name": "Analysing, interpreting and drawing inferences from data"
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
            "name": "Linear motion (displacement, velocity, acceleration, equations of motion)"
          },
          {
            "id": "physics-0-1",
            "name": "Vectors and scalars"
          },
          {
            "id": "physics-0-2",
            "name": "Newton's laws of motion (force and momentum, F = ma)"
          },
          {
            "id": "physics-0-3",
            "name": "Conservation of momentum"
          },
          {
            "id": "physics-0-4",
            "name": "Gravity (acceleration due to gravity, gravitational force, Newton's law of universal gravitation)"
          },
          {
            "id": "physics-0-5",
            "name": "Density and pressure"
          },
          {
            "id": "physics-0-6",
            "name": "Moments (turning effect of a force)"
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
            "name": "Energy (kinetic and potential energy, conservation of energy)"
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
            "name": "Heat transfer: conduction"
          },
          {
            "id": "physics-2-4",
            "name": "Heat transfer: convection"
          },
          {
            "id": "physics-2-5",
            "name": "Heat transfer: radiation (including the Sun, solar constant, U-values)"
          }
        ]
      },
      {
        "id": "physics-3",
        "name": "Waves",
        "subtopics": [
          {
            "id": "physics-3-0",
            "name": "Properties of waves (longitudinal and transverse, frequency, amplitude, wavelength, velocity, c = fλ)"
          },
          {
            "id": "physics-3-1",
            "name": "Wave phenomena (reflection, refraction, diffraction, interference, polarisation, stationary waves)"
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
            "name": "Characteristics of notes (frequency/pitch, amplitude/loudness, quality/overtones)"
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
            "name": "Mirrors (images formed by plane and spherical mirrors)"
          },
          {
            "id": "physics-5-2",
            "name": "Laws of refraction (refractive index)"
          },
          {
            "id": "physics-5-3",
            "name": "Total internal reflection (critical angle, optical fibres)"
          },
          {
            "id": "physics-5-4",
            "name": "Lenses"
          },
          {
            "id": "physics-5-5",
            "name": "Diffraction and interference (diffraction grating)"
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
            "name": "Colours (primary, secondary, complementary; addition of colours)"
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
            "name": "Force between charges (Coulomb's law)"
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
            "name": "Conduction in materials (solids, liquids, gases, semiconductors, vacuum)"
          },
          {
            "id": "physics-6-11",
            "name": "Resistance (Ohm's law, resistivity, resistors in series and parallel, LDR, thermistor, potential divider)"
          },
          {
            "id": "physics-6-12",
            "name": "Effects of an electric current (heating, chemical, magnetic)"
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
            "name": "Current in a magnetic field (force on a current-carrying conductor)"
          },
          {
            "id": "physics-6-16",
            "name": "Electromagnetic induction (Faraday's law, Lenz's law)"
          },
          {
            "id": "physics-6-17",
            "name": "Alternating current (peak and rms values, generator, motor)"
          },
          {
            "id": "physics-6-18",
            "name": "Mutual and self-induction (transformers, induction)"
          }
        ]
      },
      {
        "id": "physics-7",
        "name": "Modern Physics",
        "subtopics": [
          {
            "id": "physics-7-0",
            "name": "The electron (charge, Millikan's experiment, cathode rays)"
          },
          {
            "id": "physics-7-1",
            "name": "Thermionic emission (cathode ray tube, CRO)"
          },
          {
            "id": "physics-7-2",
            "name": "Photoelectric emission (photoelectric effect, photocell)"
          },
          {
            "id": "physics-7-3",
            "name": "X-rays (production, uses, hazards)"
          },
          {
            "id": "physics-7-4",
            "name": "Structure of the atom (energy levels, spectra, the photon E = hf)"
          },
          {
            "id": "physics-7-5",
            "name": "Structure of the nucleus (protons, neutrons, isotopes)"
          },
          {
            "id": "physics-7-6",
            "name": "Radioactivity (alpha, beta, gamma; nuclear reactions; half-life)"
          },
          {
            "id": "physics-7-7",
            "name": "Nuclear energy (fission, fusion, E = mc², reactors)"
          },
          {
            "id": "physics-7-8",
            "name": "Ionising radiation, its hazards and uses (radioisotopes)"
          },
          {
            "id": "physics-7-9",
            "name": "Particle Physics (option, Higher Level): fundamental forces, quarks, leptons, antimatter, accelerators"
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
            "name": "Linear motion (displacement, velocity, acceleration, equations of motion)"
          },
          {
            "id": "physics-and-chemistry-0-1",
            "name": "Vectors and scalars"
          },
          {
            "id": "physics-and-chemistry-0-2",
            "name": "Newton's laws of motion (force and momentum, F = ma)"
          },
          {
            "id": "physics-and-chemistry-0-3",
            "name": "Conservation of momentum"
          },
          {
            "id": "physics-and-chemistry-0-4",
            "name": "Gravity (acceleration due to gravity, gravitational force, Newton's law of universal gravitation)"
          },
          {
            "id": "physics-and-chemistry-0-5",
            "name": "Density and pressure"
          },
          {
            "id": "physics-and-chemistry-0-6",
            "name": "Moments (turning effect of a force)"
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
            "name": "Energy (kinetic and potential energy, conservation of energy)"
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
            "name": "Heat transfer: conduction"
          },
          {
            "id": "physics-and-chemistry-2-4",
            "name": "Heat transfer: convection"
          },
          {
            "id": "physics-and-chemistry-2-5",
            "name": "Heat transfer: radiation (including the Sun, solar constant, U-values)"
          }
        ]
      },
      {
        "id": "physics-and-chemistry-3",
        "name": "Waves",
        "subtopics": [
          {
            "id": "physics-and-chemistry-3-0",
            "name": "Properties of waves (longitudinal and transverse, frequency, amplitude, wavelength, velocity, c = fλ)"
          },
          {
            "id": "physics-and-chemistry-3-1",
            "name": "Wave phenomena (reflection, refraction, diffraction, interference, polarisation, stationary waves)"
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
            "name": "Characteristics of notes (frequency/pitch, amplitude/loudness, quality/overtones)"
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
            "name": "Mirrors (images formed by plane and spherical mirrors)"
          },
          {
            "id": "physics-and-chemistry-5-2",
            "name": "Laws of refraction (refractive index)"
          },
          {
            "id": "physics-and-chemistry-5-3",
            "name": "Total internal reflection (critical angle, optical fibres)"
          },
          {
            "id": "physics-and-chemistry-5-4",
            "name": "Lenses"
          },
          {
            "id": "physics-and-chemistry-5-5",
            "name": "Diffraction and interference (diffraction grating)"
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
            "name": "Colours (primary, secondary, complementary; addition of colours)"
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
            "name": "Force between charges (Coulomb's law)"
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
            "name": "Conduction in materials (solids, liquids, gases, semiconductors, vacuum)"
          },
          {
            "id": "physics-and-chemistry-6-11",
            "name": "Resistance (Ohm's law, resistivity, resistors in series and parallel, LDR, thermistor, potential divider)"
          },
          {
            "id": "physics-and-chemistry-6-12",
            "name": "Effects of an electric current (heating, chemical, magnetic)"
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
            "name": "Current in a magnetic field (force on a current-carrying conductor)"
          },
          {
            "id": "physics-and-chemistry-6-16",
            "name": "Electromagnetic induction (Faraday's law, Lenz's law)"
          },
          {
            "id": "physics-and-chemistry-6-17",
            "name": "Alternating current (peak and rms values, generator, motor)"
          },
          {
            "id": "physics-and-chemistry-6-18",
            "name": "Mutual and self-induction (transformers, induction)"
          }
        ]
      },
      {
        "id": "physics-and-chemistry-7",
        "name": "Modern Physics",
        "subtopics": [
          {
            "id": "physics-and-chemistry-7-0",
            "name": "The electron (charge, Millikan's experiment, cathode rays)"
          },
          {
            "id": "physics-and-chemistry-7-1",
            "name": "Thermionic emission (cathode ray tube, CRO)"
          },
          {
            "id": "physics-and-chemistry-7-2",
            "name": "Photoelectric emission (photoelectric effect, photocell)"
          },
          {
            "id": "physics-and-chemistry-7-3",
            "name": "X-rays (production, uses, hazards)"
          },
          {
            "id": "physics-and-chemistry-7-4",
            "name": "Structure of the atom (energy levels, spectra, the photon E = hf)"
          },
          {
            "id": "physics-and-chemistry-7-5",
            "name": "Structure of the nucleus (protons, neutrons, isotopes)"
          },
          {
            "id": "physics-and-chemistry-7-6",
            "name": "Radioactivity (alpha, beta, gamma; nuclear reactions; half-life)"
          },
          {
            "id": "physics-and-chemistry-7-7",
            "name": "Nuclear energy (fission, fusion, E = mc², reactors)"
          },
          {
            "id": "physics-and-chemistry-7-8",
            "name": "Ionising radiation, its hazards and uses (radioisotopes)"
          },
          {
            "id": "physics-and-chemistry-7-9",
            "name": "Particle Physics (option, Higher Level): fundamental forces, quarks, leptons, antimatter, accelerators"
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
            "name": "The Scientific Method (Biology; Scientific Method; Experimentation)"
          },
          {
            "id": "biology-0-1",
            "name": "The Characteristics of Life (A Search for a Definition of Life; Definition of Life; Characteristics of Life)"
          },
          {
            "id": "biology-0-2",
            "name": "Nutrition (Function of Food; Chemical Elements; Biomolecular Structures; Biomolecular Sources and Components of Food; Energy Transfer Reactions; Structural Role of Biomolecules; Metabolic Role of Biomolecules; Minerals; Water)"
          },
          {
            "id": "biology-0-3",
            "name": "General Principles of Ecology (Ecology; Ecosystem; Biosphere; Habitat; Environmental Factors; Energy Flow; Niche; Nutrient Recycling; Human Impact on an Ecosystem; HL: Pyramid of Numbers; Ecological Relationships; Population Dynamics)"
          },
          {
            "id": "biology-0-4",
            "name": "A Study of an Ecosystem (Broad Overview; Observation and Scientific Study; Organism Distribution; Choice of Habitat; Organism Adaptations; Organism Role in Energy Transfer; Analysis)"
          }
        ]
      },
      {
        "id": "biology-1",
        "name": "Unit Two: The Cell",
        "subtopics": [
          {
            "id": "biology-1-0",
            "name": "Cell Structure (Microscopy; Cell Structure and Function; Cell Ultrastructure; HL: Prokaryotic and Eukaryotic Cells)"
          },
          {
            "id": "biology-1-1",
            "name": "Cell Metabolism (Cell Metabolism; Sources of Energy; Enzymes; Photosynthesis; Respiration; Movement through Cell Membranes - diffusion, osmosis; HL: Enzymes; Role of ATP and NAD; Photosynthesis Extended; Respiration Extended)"
          },
          {
            "id": "biology-1-2",
            "name": "Cell Continuity (Cell Continuity and Chromosome; Haploid, Diploid; The Cell Cycle; Mitosis; Function of Mitosis; Meiosis; Functions of Meiosis; HL: Stages of Mitosis)"
          },
          {
            "id": "biology-1-3",
            "name": "Cell Diversity (Tissues; Organs; Organ System)"
          },
          {
            "id": "biology-1-4",
            "name": "Genetics (Variation of Species; Heredity and Gene Expression; Genetic Code; DNA Structure, Replication and Profiling; Protein Synthesis; Genetic Inheritance; Causes of Variation; Evolution; Genetic Engineering; HL: Origin of the Science of Genetics; Law of Segregation; Law of Independent Assortment; Dihybrid Cross; Nucleic Acid Structure and Function; Protein Synthesis Extended)"
          }
        ]
      },
      {
        "id": "biology-2",
        "name": "Unit Three: The Organism",
        "subtopics": [
          {
            "id": "biology-2-0",
            "name": "Diversity of Organisms (Diversity of Organisms; Micro-organisms; Monera e.g. Bacteria; Fungi; Laboratory Procedures with Micro-organisms; Protista e.g. Amoeba; Plant e.g. the Flowering Plant; Animal e.g. the Human; HL: Nature of Bacteria and Fungi; Growth Curves)"
          },
          {
            "id": "biology-2-1",
            "name": "Organisation and the Vascular Structures (Organisational Complexity of the Flowering Plant; Organisational Complexity of the Human - the Circulatory System and Heart; HL: Blood Cells; Heartbeat Control)"
          },
          {
            "id": "biology-2-2",
            "name": "Transport and Nutrition (Nutrition in the Flowering Plant; Modified Plant Food Storage Organs; Nutrition in the Human; Human Digestive System; Blood Transport of Nutrients; Balanced Human Diet; HL: Cohesion-Tension Model of Xylem Transport)"
          },
          {
            "id": "biology-2-3",
            "name": "Breathing System and Excretion (Homeostasis; Necessity for Homeostasis; Exchange System in Flowering Plants; The Breathing System in the Human; Plant Excretion; The Excretory System in the Human; HL: Carbon Dioxide as a Controlling Factor in Gaseous Exchange; The Nephron as a Unit of Kidney Function)"
          },
          {
            "id": "biology-2-4",
            "name": "Responses to Stimuli (Structures for Response; Responses in the Flowering Plant - tropisms; Responses in the Human - nervous system, senses/eye/ear, endocrine system, musculoskeletal system, defence/immune system; Viruses; HL: Auxins; Plant Growth Regulators and Animal Hormones; Human Immune System; Growth and Development in Bones)"
          },
          {
            "id": "biology-2-5",
            "name": "Reproduction and Growth (Reproduction of the Flowering Plant; Sexual Reproduction in the Human; germination, vegetative propagation, menstrual cycle, contraception, infertility; HL: Sexual Reproduction in the Flowering Plant; Human Embryo Development; Sexual Reproduction in the Human)"
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
            "name": "Social and ethical considerations of computing technologies"
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
            "name": "Diverse roles and careers that use computing technologies"
          },
          {
            "id": "computer-science-0-15",
            "name": "Designing and developing"
          },
          {
            "id": "computer-science-0-16",
            "name": "Design process (staged and iterative)"
          },
          {
            "id": "computer-science-0-17",
            "name": "Working in a team, assigning roles and responsibilities"
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
            "name": "Abstraction: modular design and abstract models"
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
            "name": "Sorting: Simple sort, Insert sort, Bubble sort, Quicksort"
          },
          {
            "id": "computer-science-1-6",
            "name": "Search: Linear search, Binary search"
          },
          {
            "id": "computer-science-1-7",
            "name": "Functions (including recursive), procedures and modules"
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
            "name": "Basic electronics: voltage, current, resistors, capacitors, transistors"
          },
          {
            "id": "computer-science-1-12",
            "name": "Logic gates"
          },
          {
            "id": "computer-science-1-13",
            "name": "Operating system layers: Hardware, OS, Application, User"
          },
          {
            "id": "computer-science-1-14",
            "name": "Binary, hexadecimal and decimal number systems and conversion"
          },
          {
            "id": "computer-science-1-15",
            "name": "Digital and analogue input"
          },
          {
            "id": "computer-science-1-16",
            "name": "Web infrastructure - Computer Network Protocols: HTTP, TCP, IP, VOIP"
          },
          {
            "id": "computer-science-1-17",
            "name": "World Wide Web and the Internet: client-server model, hardware, protocols"
          },
          {
            "id": "computer-science-1-18",
            "name": "Data"
          },
          {
            "id": "computer-science-1-19",
            "name": "Data types: Boolean, integer, real, char, string, date, array"
          },
          {
            "id": "computer-science-1-20",
            "name": "Character encoding: 8-bit ASCII, Non-Roman character sets, Unicode (UTF-8, Emojis)"
          },
          {
            "id": "computer-science-1-21",
            "name": "Information systems: collecting, storing and sorting continuous and discrete data"
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
            "name": "Testing: Unit test, Function test, System test"
          }
        ]
      },
      {
        "id": "computer-science-2",
        "name": "Strand 3: Computer science in practice",
        "subtopics": [
          {
            "id": "computer-science-2-0",
            "name": "Applied Learning Task 1 - Interactive information systems"
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
            "name": "ALT2: Data collection, analysis and interpretation"
          },
          {
            "id": "computer-science-2-5",
            "name": "ALT2: Frequency, mean, median and mode; data representation"
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
            "name": "ALT4: Computing inputs and outputs (digital and analogue, sensors)"
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
            "name": "The nature and purpose of the conceptual framework in accounting"
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
            "name": "Desirable qualitative characteristics of accounting information (relevance, reliability, understandability, comparability)"
          },
          {
            "id": "accounting-0-4",
            "name": "Accounting concepts, bases and policies"
          },
          {
            "id": "accounting-0-5",
            "name": "Fundamental accounting concepts in SSAP 2 (going concern, accruals, consistency, prudence)"
          },
          {
            "id": "accounting-0-6",
            "name": "Other concepts, conventions and principles (entity, money measurement, materiality, realisation, double-entry, period of account)"
          }
        ]
      },
      {
        "id": "accounting-1",
        "name": "The Regulatory Framework of Accounting (HL)",
        "subtopics": [
          {
            "id": "accounting-1-0",
            "name": "The nature and objectives of the regulation of financial reporting"
          },
          {
            "id": "accounting-1-1",
            "name": "The predominant regulatory bodies (Government, European Union, accountancy profession, Stock Exchange)"
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
            "name": "The procedures for monitoring the regulation of financial reporting"
          }
        ]
      },
      {
        "id": "accounting-2",
        "name": "Accounting Records",
        "subtopics": [
          {
            "id": "accounting-2-0",
            "name": "Double-Entry Bookkeeping (source documents, day books and journal, trial balance, capital v revenue, VAT and statutory deductions, accruals, prepayments and provisions, depreciation and appreciation)"
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
            "name": "Suspense Accounts (correction of errors, effects on net profit and balance sheet; statement of corrected net profit HL)"
          }
        ]
      },
      {
        "id": "accounting-3",
        "name": "Sole Traders",
        "subtopics": [
          {
            "id": "accounting-3-0",
            "name": "The nature and extent of the sole trader form of business"
          },
          {
            "id": "accounting-3-1",
            "name": "Preparation and presentation of trading, profit and loss account and balance sheet"
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
            "name": "Share Capital, Reserves and Loan Capital (types of companies, classes of shares, authorised/issued/called-up/paid-up capital, reserves v provisions, debentures)"
          },
          {
            "id": "accounting-4-1",
            "name": "Financial Statements of Limited Companies (revaluation of assets, dividends and taxation, preparation of internal financial statements)"
          },
          {
            "id": "accounting-4-2",
            "name": "Appreciation of Annual Reports of Public Limited Companies (HL) — directors' report, auditor's report, statutory requirements, analysis of published reports"
          }
        ]
      },
      {
        "id": "accounting-5",
        "name": "Specialised Accounts",
        "subtopics": [
          {
            "id": "accounting-5-0",
            "name": "Manufacturing Accounts (classification of costs, work-in-progress, transfer at current market value, unit cost of production)"
          },
          {
            "id": "accounting-5-1",
            "name": "Stock (valuation of stock, effect on profit, mark-up and margin, stock turnover)"
          },
          {
            "id": "accounting-5-2",
            "name": "Club Accounts and Accounts of Service Firms (receipts and payments account, income and expenditure account, accumulated fund, balance sheet)"
          },
          {
            "id": "accounting-5-3",
            "name": "Departmental Accounts (allocation of expenses and gains, departmental trading and profit and loss account, inter-departmental transfers)"
          },
          {
            "id": "accounting-5-4",
            "name": "Farm Accounts (stock valuation, analysed receipts and payments account, enterprise analysis account)"
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
            "name": "Profit statements using net worth method (effects of drawings and introduction of capital)"
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
            "name": "Distinction between items that do and do not involve the movement of cash"
          },
          {
            "id": "accounting-7-3",
            "name": "The different sources of cash inflows and outflows"
          },
          {
            "id": "accounting-7-4",
            "name": "The impact of the movement in working capital on cash flows"
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
            "name": "Objective of analysis and interpretation of financial statements"
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
            "name": "The nature and scope of management accounting and its relationship to financial accounting"
          },
          {
            "id": "accounting-9-1",
            "name": "Cost classifications (manufacturing/non-manufacturing, direct/indirect, product/period, fixed/variable; mixed, step-fixed and step-variable HL; controllable and uncontrollable HL)"
          },
          {
            "id": "accounting-9-2",
            "name": "Product costing"
          },
          {
            "id": "accounting-9-3",
            "name": "Cost-Volume-Profit Analysis (contribution, break-even point, margin of safety, break-even charts, limitations; sensitivity analysis HL)"
          },
          {
            "id": "accounting-9-4",
            "name": "Budgetary Planning and Control (master budget and subsidiary budgets — sales, production, raw materials, purchases, direct labour, factory overhead, non-factory expense, closing stock; cash budgeting; budgeted profit and loss account and balance sheet; comparison of actual with budget)"
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
            "name": "The importance of information technology in the accounting environment"
          },
          {
            "id": "accounting-10-1",
            "name": "Spreadsheet application in dealing with specific areas of the accounting syllabus"
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
            "name": "Methods of resolving conflicts in relationships (non-legislative and legislative)"
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
            "name": "Introduction and definition of enterprise (relevance to personal, business and public life and to business start-up)"
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
            "name": "Application of enterprise skills to different situations"
          }
        ]
      },
      {
        "id": "business-2",
        "name": "Unit 3: Managing 1",
        "subtopics": [
          {
            "id": "business-2-0",
            "name": "Introduction and definition of management (achieving results through people)"
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
            "name": "Management skill: Leading - direction, delegation"
          },
          {
            "id": "business-2-5",
            "name": "Management skill: Motivating - classic motivation theories"
          },
          {
            "id": "business-2-6",
            "name": "Management skill: Communication - importance, communication skills, methods and their application"
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
            "name": "Organising - structure of organisation (formal and informal); staffing, span of control and project teams"
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
            "name": "Household and business manager (comparison of roles re finance, insurance and taxation)"
          },
          {
            "id": "business-3-1",
            "name": "Aspects of finance: basic cash flow, main sources of finance, cost of finance, current account, applying for a loan"
          },
          {
            "id": "business-3-2",
            "name": "Aspects of insurance: principles, risks and costs, and types of insurance"
          },
          {
            "id": "business-3-3",
            "name": "Aspects of taxation: main types, basic tax computations, principal tax forms"
          },
          {
            "id": "business-3-4",
            "name": "Human resource management"
          },
          {
            "id": "business-3-5",
            "name": "HRM function: recruitment and selection"
          },
          {
            "id": "business-3-6",
            "name": "HRM function: employer and employee relationships"
          },
          {
            "id": "business-3-7",
            "name": "HRM function: Teamwork"
          },
          {
            "id": "business-3-8",
            "name": "HRM function: people development, performance appraisal and reward"
          },
          {
            "id": "business-3-9",
            "name": "Changing role of management"
          },
          {
            "id": "business-3-10",
            "name": "Managing new relationships: empowerment of workers and total quality management"
          },
          {
            "id": "business-3-11",
            "name": "Managing new technologies: impact of technology on personnel, business costs and business opportunities"
          },
          {
            "id": "business-3-12",
            "name": "Monitoring the business: use, understanding and interpretation of accountancy and business data"
          },
          {
            "id": "business-3-13",
            "name": "Basic final accounts and balance sheets"
          },
          {
            "id": "business-3-14",
            "name": "Main profitability and liquidity ratios; debt/equity ratio"
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
            "name": "Sources of opportunities: internal and external"
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
            "name": "The marketing concept (consumer orientation)"
          },
          {
            "id": "business-4-5",
            "name": "The marketing strategy"
          },
          {
            "id": "business-4-6",
            "name": "Developing the marketing mix - product, price, promotion and place"
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
            "name": "Categories of industry: agriculture, manufacturing, services and natural resources"
          },
          {
            "id": "business-5-1",
            "name": "Changing trends in business"
          },
          {
            "id": "business-5-2",
            "name": "Types of business organisation: sole trader, partnership, alliances, franchising, private limited companies, transnationals, public limited companies, co-operatives, state-owned enterprises and indigenous firms"
          },
          {
            "id": "business-5-3",
            "name": "Changing trends in ownership and structure"
          },
          {
            "id": "business-5-4",
            "name": "Community development: local community and business; community development incorporating local community initiatives"
          },
          {
            "id": "business-5-5",
            "name": "Business and the economy: impact of the economy on business (state of economy, inflation, interest rates, tax, grants)"
          },
          {
            "id": "business-5-6",
            "name": "Impact of business on the economy at local and national level (employment, tax revenues, environmental issues)"
          },
          {
            "id": "business-5-7",
            "name": "The interaction between business and the wider economy"
          },
          {
            "id": "business-5-8",
            "name": "Government and business: encouraging and regulating business"
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
            "name": "Socially responsible business at local and national level"
          }
        ]
      },
      {
        "id": "business-6",
        "name": "Unit 7: International Environment",
        "subtopics": [
          {
            "id": "business-6-0",
            "name": "Introduction to the international trading environment"
          },
          {
            "id": "business-6-1",
            "name": "The significance of international trade for the Irish economy"
          },
          {
            "id": "business-6-2",
            "name": "The changing nature of the international economy and its effects on Irish business"
          },
          {
            "id": "business-6-3",
            "name": "Opportunities and challenges for Irish business in international trade"
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
            "name": "Purpose of the main European Union policies and directives and their impact on Irish business"
          },
          {
            "id": "business-6-8",
            "name": "Decision-making process in the main European Union institutions"
          },
          {
            "id": "business-6-9",
            "name": "The role of the special interest groups in this process"
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
            "name": "The Tectonic Cycle (internal structure of the earth, the plate tectonics model, plate boundaries, geography of volcanoes and earthquakes)"
          },
          {
            "id": "geography-0-1",
            "name": "The Rock Cycle (formation of igneous, metamorphic and sedimentary rocks; weathering, mass wasting and erosion; human interaction with the rock cycle)"
          },
          {
            "id": "geography-0-2",
            "name": "Landform Development (i): the influence of geological structures (volcanic/plutonic structures, lava flows, folding, doming, faulting)"
          },
          {
            "id": "geography-0-3",
            "name": "Landform Development (ii): the influence of rock characteristics (landforms associated with particular rock types; spatial variations in rock type)"
          },
          {
            "id": "geography-0-4",
            "name": "Landform Development (iii): surface (exogenetic) processes - mass movement, fluvial, coastal and glacial processes, patterns and associated landforms"
          },
          {
            "id": "geography-0-5",
            "name": "Landform Development (iv): the balance of endogenetic and exogenetic forces (isostasy, fluvial adjustment to base level, cyclic landscape development and peneplains)"
          },
          {
            "id": "geography-0-6",
            "name": "Human Interaction (impact of human activities on surface processes - mass movement, river processes, coastal processes)"
          }
        ]
      },
      {
        "id": "geography-1",
        "name": "Core Unit 2: Regional Geography",
        "subtopics": [
          {
            "id": "geography-1-0",
            "name": "The Concept of a Region (physical/climatic/geomorphological regions, administrative regions, cultural regions, socio-economic regions, nodal/city/urban regions)"
          },
          {
            "id": "geography-1-1",
            "name": "The Dynamics of Regions (physical, economic and human processes in two contrasting Irish regions, two contrasting European regions, and one continental/subcontinental region)"
          },
          {
            "id": "geography-1-2",
            "name": "The Complexity of Regions (i): interaction of economic, cultural and physical processes; the future of Europe and the EU"
          },
          {
            "id": "geography-1-3",
            "name": "The Complexity of Regions (ii): how the boundaries and extent of regions change over time (language regions, city regions, EU expansion, political boundaries)"
          }
        ]
      },
      {
        "id": "geography-2",
        "name": "Core Unit 3: The Geographical Investigation and Skills Unit",
        "subtopics": [
          {
            "id": "geography-2-0",
            "name": "Geographical Skills (map interpretation, photograph analysis, statistical analysis, ICT, geographical information systems)"
          },
          {
            "id": "geography-2-1",
            "name": "Introduction: posing the problem and devising a strategy (selection of topic, hypothesis/aim, objectives, information required)"
          },
          {
            "id": "geography-2-2",
            "name": "Planning: preparation of the work (methods of data collection, questionnaire/recording sheet design, locations, instruments)"
          },
          {
            "id": "geography-2-3",
            "name": "Collection of Data (field observations, questionnaires and surveys, secondary/documentary sources)"
          },
          {
            "id": "geography-2-4",
            "name": "Preparation of the Report (organisation of data; illustrations, graphs, maps and tables; use of ICT to present results)"
          },
          {
            "id": "geography-2-5",
            "name": "Conclusion and Evaluation (analysis and interpretation of results, valid conclusions, comparison with theory, evaluation of hypotheses)"
          }
        ]
      },
      {
        "id": "geography-3",
        "name": "Elective Unit 4: Patterns and Processes in Economic Activities",
        "subtopics": [
          {
            "id": "geography-3-0",
            "name": "Economic Development (GNP as a measure of development; the Human Development Index)"
          },
          {
            "id": "geography-3-1",
            "name": "Spatial variations in economic development (case study of a developed economy; case study of a developing economy; global justice perspective)"
          },
          {
            "id": "geography-3-2",
            "name": "The Global Economy (multi-national companies, world trade patterns, the international division of labour, globalisation)"
          },
          {
            "id": "geography-3-3",
            "name": "Ireland and the European Union (EU and Irish trading patterns; CAP, Common Fisheries Policy, regional development funds, social funding)"
          },
          {
            "id": "geography-3-4",
            "name": "Environmental Impact (renewable/non-renewable resources, fossil fuels and alternative energy, pollution, sustainable economic development, economic vs environmental conflicts)"
          }
        ]
      },
      {
        "id": "geography-4",
        "name": "Elective Unit 5: Patterns and Processes in the Human Environment",
        "subtopics": [
          {
            "id": "geography-4-0",
            "name": "The Dynamics of Population: population characteristics change over time and space (distribution, density, growth patterns, population structure, fertility and mortality rates)"
          },
          {
            "id": "geography-4-1",
            "name": "The Dynamics of Population: impact on levels of human development (causes and effects of over-population; resources, society/culture, income, technology)"
          },
          {
            "id": "geography-4-2",
            "name": "The Dynamics of Population: population movements and their impact on donor and receiver regions (migration patterns and policy, ethnic/racial/religious issues, rural-urban migration)"
          },
          {
            "id": "geography-4-3",
            "name": "The Dynamics of Settlement: site, situation and function (pre-historic/historic settlement, rural settlement patterns, ribbon development, urban hierarchy, hinterland and central place theory)"
          },
          {
            "id": "geography-4-4",
            "name": "The Dynamics of Settlement: the changing landuse pattern of urban settlements (landuse zones, planning issues, land values and social stratification, expansion of cities)"
          },
          {
            "id": "geography-4-5",
            "name": "The Dynamics of Settlement: problems from the growth of urban centres (traffic congestion, urban decay and sprawl, heritage and environmental quality, urban renewal, developing-world cities, the future of urbanism)"
          }
        ]
      },
      {
        "id": "geography-5",
        "name": "Optional Unit 6: Global Interdependence (Higher Level Only)",
        "subtopics": [
          {
            "id": "geography-5-0",
            "name": "Views of development and underdevelopment (determinist and modernisation approaches, images and language of developing societies, 'first world/third world', north-south, eurocentric thinking)"
          },
          {
            "id": "geography-5-1",
            "name": "The interdependent global economy (multinational case study, global environmental issues - deforestation, desertification, global warming; social and political decisions - refugees, migration, human rights)"
          },
          {
            "id": "geography-5-2",
            "name": "Empowering people - linking economic growth with human development (national debt and the cycle of poverty, the 'aid' debate, role of NGOs, land ownership, participation, exploitation, gender roles)"
          },
          {
            "id": "geography-5-3",
            "name": "Sustainable development as a model for the future (sustainable use of resources, fair trade, justice issues for minority groups, self-reliance and self-help)"
          }
        ]
      },
      {
        "id": "geography-6",
        "name": "Optional Unit 7: Geoecology (Higher Level Only)",
        "subtopics": [
          {
            "id": "geography-6-0",
            "name": "Soil composition and characteristics (mineral matter, organic matter, water and air; texture, colour, structure, water content, water retention)"
          },
          {
            "id": "geography-6-1",
            "name": "Soil processes and human interference (global pattern of soils; weathering, soil erosion, leaching, humification, podzolisation, laterisation, calcification; over-cropping, over-grazing, desertification and conservation)"
          },
          {
            "id": "geography-6-2",
            "name": "Biomes (a detailed study of one major biome - climatic and soil characteristics and related animal and vegetation distribution)"
          },
          {
            "id": "geography-6-3",
            "name": "Human alteration of biomes (early settlement and forest clearing, felling of tropical rainforests, intensive agriculture, industrial development)"
          }
        ]
      },
      {
        "id": "geography-7",
        "name": "Optional Unit 8: Culture and Identity (Higher Level Only)",
        "subtopics": [
          {
            "id": "geography-7-0",
            "name": "Physical and cultural indicators of population (racial groupings, impact of colonialism and migration, language as a cultural indicator, religion as a cultural indicator, everyday expressions of culture)"
          },
          {
            "id": "geography-7-1",
            "name": "Nationality and the nation state (physical and political boundaries, cultural groups within nation states, cultural groups without nationality, conflicts between political structures and cultural groups)"
          },
          {
            "id": "geography-7-2",
            "name": "Identity as a concept (case study of a European region drawing together race, nationality and identity - historical/political boundaries, ethnicity, religion, culture, migration, new boundaries)"
          }
        ]
      },
      {
        "id": "geography-8",
        "name": "Optional Unit 9: The Atmosphere-Ocean Environment (Higher Level Only)",
        "subtopics": [
          {
            "id": "geography-8-0",
            "name": "Composition and structure of the atmosphere and oceans (measurement of pressure, temperature, wind, humidity)"
          },
          {
            "id": "geography-8-1",
            "name": "Solar energy distribution (energy flows in the atmospheric/ocean environment, the heat budget of the earth, geographical distribution of temperature)"
          },
          {
            "id": "geography-8-2",
            "name": "Exchanges of water between oceans and atmosphere (the hydrological cycle; humidity, evaporation and condensation; cloud formation and classification; precipitation and its distribution)"
          },
          {
            "id": "geography-8-3",
            "name": "Circulation in the atmosphere and oceans (forces governing movement of air and water, general circulation, mid-latitude depressions and anticyclones, land/sea breezes, mountain/valley winds, thunderstorms)"
          },
          {
            "id": "geography-8-4",
            "name": "Distinctive climatic environments (one distinctive global climate - equatorial, monsoon, mid-latitude west coast, mediterranean or continental; examples of climate change)"
          },
          {
            "id": "geography-8-5",
            "name": "Influence of climate on economic development (rainfall and agriculture/water supply, drought and desertification, climate and tourism)"
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
            "name": "Reform and Reformation in Tudor Ireland - Case study: The Plantation of Laois/Offaly"
          },
          {
            "id": "history-0-2",
            "name": "Reform and Reformation in Tudor Ireland - Case study: Women and marriage under Gaelic law"
          },
          {
            "id": "history-0-3",
            "name": "Reform and Reformation in Tudor Ireland - Case study: The Bardic Schools"
          },
          {
            "id": "history-0-4",
            "name": "Rebellion and conquest in Elizabethan Ireland, 1558-1603"
          },
          {
            "id": "history-0-5",
            "name": "Rebellion and conquest in Elizabethan Ireland - Case study: The Lordship of Tir Eoghain"
          },
          {
            "id": "history-0-6",
            "name": "Rebellion and conquest in Elizabethan Ireland - Case study: Elizabethan Dublin"
          },
          {
            "id": "history-0-7",
            "name": "Rebellion and conquest in Elizabethan Ireland - Case study: Meiler Magrath's clerical career"
          },
          {
            "id": "history-0-8",
            "name": "Kingdom versus colony - the struggle for mastery in Ireland, 1603-1660"
          },
          {
            "id": "history-0-9",
            "name": "Kingdom versus colony - Case study: The trial of Strafford"
          },
          {
            "id": "history-0-10",
            "name": "Kingdom versus colony - Case study: The Scots migration to Ulster"
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
            "name": "Establishing a colonial ascendancy - Case study: The Parliament of 1689"
          },
          {
            "id": "history-0-14",
            "name": "Establishing a colonial ascendancy - Case study: Restoration Dublin"
          },
          {
            "id": "history-0-15",
            "name": "Establishing a colonial ascendancy - Case study: The Jacobite poets"
          },
          {
            "id": "history-0-16",
            "name": "Colony versus kingdom - tensions in mid-18th century Ireland, 1715-1770"
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
            "name": "Colony versus kingdom - Case study: The trial of Fr. Sheehy"
          },
          {
            "id": "history-0-20",
            "name": "The end of the Irish kingdom and the establishment of the Union, 1770-1815"
          },
          {
            "id": "history-0-21",
            "name": "End of the Irish kingdom - Case study: The Wexford Rebellion"
          },
          {
            "id": "history-0-22",
            "name": "End of the Irish kingdom - Case study: The rise of Belfast"
          },
          {
            "id": "history-0-23",
            "name": "End of the Irish kingdom - Case study: Maynooth College"
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
            "name": "Renaissance to Reformation - Case study: The divorce of Henry VIII and Catherine of Aragon"
          },
          {
            "id": "history-1-2",
            "name": "Renaissance to Reformation - Case study: Seville, the port of the New World"
          },
          {
            "id": "history-1-3",
            "name": "Renaissance to Reformation - Case study: Calvin's Geneva"
          },
          {
            "id": "history-1-4",
            "name": "Religion and power - politics in the later sixteenth century, 1567-1609"
          },
          {
            "id": "history-1-5",
            "name": "Religion and power - Case study: The Spanish Armada"
          },
          {
            "id": "history-1-6",
            "name": "Religion and power - Case study: The decline of the port of Antwerp"
          },
          {
            "id": "history-1-7",
            "name": "Religion and power - Case study: The Jesuit mission in China"
          },
          {
            "id": "history-1-8",
            "name": "The eclipse of Old Europe, 1609-1660"
          },
          {
            "id": "history-1-9",
            "name": "The eclipse of Old Europe - Case study: The revolt of the Catalans"
          },
          {
            "id": "history-1-10",
            "name": "The eclipse of Old Europe - Case study: The Dutch empire in Asia"
          },
          {
            "id": "history-1-11",
            "name": "The eclipse of Old Europe - Case study: Galileo and the Inquisition"
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
            "name": "Age of Louis XIV - Case study: The (English) East India Company"
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
            "name": "Establishing empires - Case study: The Boston Tea Party, 1773"
          },
          {
            "id": "history-1-18",
            "name": "Establishing empires - Case study: The West Indies slave plantations"
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
            "name": "Empires in revolution - Case study: The Committee of Public Safety"
          },
          {
            "id": "history-1-22",
            "name": "Empires in revolution - Case study: The growth of Manchester"
          },
          {
            "id": "history-1-23",
            "name": "Empires in revolution - Case study: The Civil Constitution of the Clergy"
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
            "name": "Ireland and the Union - Case study: Private responses to Famine, 1845-1849"
          },
          {
            "id": "history-2-2",
            "name": "Ireland and the Union - Case study: The campaign for Catholic Emancipation, 1823-1829"
          },
          {
            "id": "history-2-3",
            "name": "Ireland and the Union - Case study: The Synod of Thurles, 1850, and the Romanisation of the Catholic Church"
          },
          {
            "id": "history-2-4",
            "name": "Movements for political and social reform, 1870-1914"
          },
          {
            "id": "history-2-5",
            "name": "Movements for political and social reform - Case study: The elections of 1885 and 1886: issues and outcomes"
          },
          {
            "id": "history-2-6",
            "name": "Movements for political and social reform - Case study: Dublin 1913 - strike and lockout"
          },
          {
            "id": "history-2-7",
            "name": "Movements for political and social reform - Case study: The GAA to 1891"
          },
          {
            "id": "history-2-8",
            "name": "The pursuit of sovereignty and the impact of partition, 1912-1949"
          },
          {
            "id": "history-2-9",
            "name": "Pursuit of sovereignty and partition - Case study: The Treaty negotiations, October-December 1921"
          },
          {
            "id": "history-2-10",
            "name": "Pursuit of sovereignty and partition - Case study: Belfast during World War II"
          },
          {
            "id": "history-2-11",
            "name": "Pursuit of sovereignty and partition - Case study: The Eucharistic Congress, 1932"
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
            "name": "The Irish diaspora - Case study: De Valera in America, June 1919-December 1920"
          },
          {
            "id": "history-2-15",
            "name": "The Irish diaspora - Case study: The Holy Ghost mission to Nigeria, 1945-1966"
          },
          {
            "id": "history-2-16",
            "name": "Politics and society in Northern Ireland, 1949-1993"
          },
          {
            "id": "history-2-17",
            "name": "Politics and society in Northern Ireland - Case study: The Sunningdale Agreement and the power-sharing executive, 1973-1974"
          },
          {
            "id": "history-2-18",
            "name": "Politics and society in Northern Ireland - Case study: The Coleraine University controversy"
          },
          {
            "id": "history-2-19",
            "name": "Politics and society in Northern Ireland - Case study: The Apprentice Boys of Derry"
          },
          {
            "id": "history-2-20",
            "name": "Government, economy and society in the Republic of Ireland, 1949-1989"
          },
          {
            "id": "history-2-21",
            "name": "Government, economy and society in the Republic - Case study: The First Programme for Economic Expansion, 1958-1963"
          },
          {
            "id": "history-2-22",
            "name": "Government, economy and society in the Republic - Case study: Impact of the EEC on fisheries"
          },
          {
            "id": "history-2-23",
            "name": "Government, economy and society in the Republic - Case study: The impact of RTE, 1962-1972"
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
            "name": "Nationalism and state formation - Case study: The 1848 Revolution in Germany"
          },
          {
            "id": "history-3-2",
            "name": "Nationalism and state formation - Case study: Robert Owen's model village at New Lanark"
          },
          {
            "id": "history-3-3",
            "name": "Nationalism and state formation - Case study: Haussmann's Paris"
          },
          {
            "id": "history-3-4",
            "name": "Nation states and international tensions, 1871-1920"
          },
          {
            "id": "history-3-5",
            "name": "Nation states and international tensions - Case study: The naval policy of Wilhelm II"
          },
          {
            "id": "history-3-6",
            "name": "Nation states and international tensions - Case study: Women in the workforce during World War I"
          },
          {
            "id": "history-3-7",
            "name": "Nation states and international tensions - Case study: The invention and early history of the motor car"
          },
          {
            "id": "history-3-8",
            "name": "Dictatorship and democracy in Europe, 1920-1945"
          },
          {
            "id": "history-3-9",
            "name": "Dictatorship and democracy in Europe - Case study: Stalin's show trials"
          },
          {
            "id": "history-3-10",
            "name": "Dictatorship and democracy in Europe - Case study: The Jarrow March, October 1936"
          },
          {
            "id": "history-3-11",
            "name": "Dictatorship and democracy in Europe - Case study: The Nuremberg Rallies"
          },
          {
            "id": "history-3-12",
            "name": "Division and realignment in Europe, 1945-1992"
          },
          {
            "id": "history-3-13",
            "name": "Division and realignment in Europe - Case study: The Hungarian Uprising, 1956"
          },
          {
            "id": "history-3-14",
            "name": "Division and realignment in Europe - Case study: The Oil Crisis, 1973"
          },
          {
            "id": "history-3-15",
            "name": "Division and realignment in Europe - Case study: The Second Vatican Council"
          },
          {
            "id": "history-3-16",
            "name": "European retreat from empire and the aftermath, 1945-1990"
          },
          {
            "id": "history-3-17",
            "name": "European retreat from empire - Case study: British withdrawal from India, 1945-1947"
          },
          {
            "id": "history-3-18",
            "name": "European retreat from empire - Case study: The secession of Katanga, 1960-1965"
          },
          {
            "id": "history-3-19",
            "name": "European retreat from empire - Case study: Race relations in France in the 1980s"
          },
          {
            "id": "history-3-20",
            "name": "The United States and the world, 1945-1989"
          },
          {
            "id": "history-3-21",
            "name": "The United States and the world - Case study: The Montgomery bus boycott, 1956"
          },
          {
            "id": "history-3-22",
            "name": "The United States and the world - Case study: Lyndon Johnson and Vietnam, 1963-1968"
          },
          {
            "id": "history-3-23",
            "name": "The United States and the world - Case study: The Moon landing, 1969"
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
            "name": "Topic 1: Power and decision-making in the school — 1.1 Processes of power and decision-making in their school"
          },
          {
            "id": "politics-and-society-0-1",
            "name": "Topic 1 — 1.2 Arguments concerning the need for rules"
          },
          {
            "id": "politics-and-society-0-2",
            "name": "Topic 1 — 1.3 Ideas underpinning these arguments (dimensions of the concept of power)"
          },
          {
            "id": "politics-and-society-0-3",
            "name": "Topic 1 — 1.4 Evidence concerning the effects of rules and rule-making processes"
          },
          {
            "id": "politics-and-society-0-4",
            "name": "Topic 2: Power and decision-making at national and European level — 2.1 The making of national policy"
          },
          {
            "id": "politics-and-society-0-5",
            "name": "Topic 2 — 2.2 How the executive branch of government is selected (Oireachtas, Northern Ireland Executive, EU institutions, non-democratic example)"
          },
          {
            "id": "politics-and-society-0-6",
            "name": "Topic 2 — 2.3 Social class and gender as important social categories (capitalism, patriarchy)"
          },
          {
            "id": "politics-and-society-0-7",
            "name": "Topic 2 — 2.4 Arguments concerning representation"
          },
          {
            "id": "politics-and-society-0-8",
            "name": "Topic 2 — 2.5 Evidence about the effectiveness of representation"
          },
          {
            "id": "politics-and-society-0-9",
            "name": "Topic 2 — 2.6 Traditional and new media in a democracy"
          },
          {
            "id": "politics-and-society-0-10",
            "name": "Topic 2 — 2.7 Participants in these debates (Hobbes, Locke, Nozick, Walby, Marx, Lynch)"
          }
        ]
      },
      {
        "id": "politics-and-society-1",
        "name": "Strand 2: Active citizenship",
        "subtopics": [
          {
            "id": "politics-and-society-1-0",
            "name": "Topic 3: Effectively contributing to communities — 3.1 People who have made positive contributions to their social context"
          },
          {
            "id": "politics-and-society-1-1",
            "name": "Topic 3 — 3.2 Becoming involved in, or starting an initiative, group or organisation"
          },
          {
            "id": "politics-and-society-1-2",
            "name": "Topic 3 — 3.3 The range of means of taking action at local, national or international level"
          },
          {
            "id": "politics-and-society-1-3",
            "name": "Topic 3 — 3.4 Identifying, evaluating and achieving personal and collective goals, including developing and evaluating action plans"
          },
          {
            "id": "politics-and-society-1-4",
            "name": "Topic 3 — 3.5 Developing personal qualities that help in new and difficult situations (initiative, flexibility, reliability, perseverance)"
          },
          {
            "id": "politics-and-society-1-5",
            "name": "Topic 3 — 3.6 Appraising oneself, evaluating one's own performance, receiving and responding to feedback"
          },
          {
            "id": "politics-and-society-1-6",
            "name": "Topic 4: Rights and responsibilities in communication with others — 4.1 Rights to freedom of expression in small-group contexts"
          },
          {
            "id": "politics-and-society-1-7",
            "name": "Topic 4 — 4.2 Developing skills in listening and communicating"
          },
          {
            "id": "politics-and-society-1-8",
            "name": "Topic 4 — 4.3 Acknowledging differences and negotiating and resolving conflicts"
          },
          {
            "id": "politics-and-society-1-9",
            "name": "Topic 4 — 4.4 Seeking and evaluating information and ideas"
          },
          {
            "id": "politics-and-society-1-10",
            "name": "Topic 4 — 4.5 Relating democratic practices in small groups to practices appropriate for citizens in wider society"
          }
        ]
      },
      {
        "id": "politics-and-society-2",
        "name": "Strand 3: Human rights and responsibilities",
        "subtopics": [
          {
            "id": "politics-and-society-2-0",
            "name": "Topic 5: Human rights and responsibilities in Ireland — 5.1 Some of the rights of young people"
          },
          {
            "id": "politics-and-society-2-1",
            "name": "Topic 5 — 5.2 Human rights principles (universal, inalienable, indivisible; civil/political vs economic/social/cultural; absolute/limited/qualified; negative/positive)"
          },
          {
            "id": "politics-and-society-2-2",
            "name": "Topic 5 — 5.3 The idea of equality in relation to rights (nine grounds, direct/indirect discrimination, patterns of diversity on the island of Ireland)"
          },
          {
            "id": "politics-and-society-2-3",
            "name": "Topic 5 — 5.4 Arguments about rights"
          },
          {
            "id": "politics-and-society-2-4",
            "name": "Topic 5 — 5.5 State bodies for human rights (IHREC, NIHRC, Ombudsman for Children, NICCY)"
          },
          {
            "id": "politics-and-society-2-5",
            "name": "Topic 5 — 5.6 Evidence on the right to education"
          },
          {
            "id": "politics-and-society-2-6",
            "name": "Topic 5 — 5.7 Participants in these debates (Locke, Nozick, Freire, Nussbaum, Lynch)"
          },
          {
            "id": "politics-and-society-2-7",
            "name": "Topic 6: Human rights and responsibilities in Europe and the wider world — 6.1 Rights in the wider world (UNCRC articles 6, 14, 19, 31; European Convention on Human Rights)"
          },
          {
            "id": "politics-and-society-2-8",
            "name": "Topic 6 — 6.2 Arguments about rights in the wider world (cultural imperialism, development)"
          },
          {
            "id": "politics-and-society-2-9",
            "name": "Topic 6 — 6.3 International cooperation and human rights (UN Declaration on the Right to Development)"
          }
        ]
      },
      {
        "id": "politics-and-society-3",
        "name": "Strand 4: Globalisation and localisation",
        "subtopics": [
          {
            "id": "politics-and-society-3-0",
            "name": "Topic 7: Globalisation and identity — 7.1 Representations of national identity made available to young people"
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
            "name": "Topic 7 — 7.4 Understanding identity (national/ethnic groups, imagined communities, effects of ethnic identity)"
          },
          {
            "id": "politics-and-society-3-4",
            "name": "Topic 7 — 7.5 Understanding interaction between western and non-western culture"
          },
          {
            "id": "politics-and-society-3-5",
            "name": "Topic 7 — 7.6 Globalisation and political power (IMF, WTO, World Bank, UNDP, supranational bodies)"
          },
          {
            "id": "politics-and-society-3-6",
            "name": "Topic 7 — 7.7 Participants in these debates (Eriksen, Appiah, Anderson, Said, Huntington)"
          },
          {
            "id": "politics-and-society-3-7",
            "name": "Topic 8: Sustainable development — 8.1 Actions that address sustainable development"
          },
          {
            "id": "politics-and-society-3-8",
            "name": "Topic 8 — 8.2 Arguments concerning sustainable development"
          },
          {
            "id": "politics-and-society-3-9",
            "name": "Topic 8 — 8.3 Participants in these debates (André Gunder Frank, Vandana Shiva, Seán McDonagh)"
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
            "name": "Part 1: The return to origins — 1.1 The pattern of return"
          },
          {
            "id": "religious-education-1-1",
            "name": "1.2 Jesus and his message in contemporary culture"
          },
          {
            "id": "religious-education-1-2",
            "name": "Part 2: The vision of Jesus in context — 2.1 The impact of Rome"
          },
          {
            "id": "religious-education-1-3",
            "name": "2.2 Evidence for Jesus of Nazareth"
          },
          {
            "id": "religious-education-1-4",
            "name": "2.3 The teachings of Jesus and their impact on the community"
          },
          {
            "id": "religious-education-1-5",
            "name": "2.4 Jesus as Messiah"
          },
          {
            "id": "religious-education-1-6",
            "name": "Part 3: The message in conflict — 3.1 Conflict with establishment"
          },
          {
            "id": "religious-education-1-7",
            "name": "3.2 The death and resurrection of Jesus"
          },
          {
            "id": "religious-education-1-8",
            "name": "Part 4: The formation of Christian communities — 4.1 The first Christian communities as seen through the writing of Paul"
          },
          {
            "id": "religious-education-1-9",
            "name": "Part 5: The Christian message today — 5.1 Interpreting the message today"
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
            "name": "Part 1: The phenomenon of religion — 1.1 Religion as a world-wide phenomenon"
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
            "name": "Part 2: A closer look at the major living traditions — 2.1 A vision of salvation"
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
            "name": "Part 4: Other living traditions — 4.1 A living tradition"
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
            "name": "Part 1: Thinking about morality — 1.1 What is morality?"
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
            "name": "Part 2: Morality and religion — 2.1 The relationship between morality and religion"
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
            "name": "Part 3: Moral principles and decision-making — morality in a pluralist society"
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
            "name": "Part 1: Gender, society and religion — 1.1 Gender and society"
          },
          {
            "id": "religious-education-4-1",
            "name": "1.2 The place of women and men in the major religious traditions"
          },
          {
            "id": "religious-education-4-2",
            "name": "Part 2: Gender and Christianity — 2.1 Women and men in the Hebrew scriptures"
          },
          {
            "id": "religious-education-4-3",
            "name": "2.2 Women and men in the Christian scriptures / tradition"
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
            "name": "Part 3: Women's stories — 3.1 Feminist theologies and spiritualities / the contributions of women"
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
            "name": "Part 2: The concept of justice and peace — 2.1 Visions of justice"
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
            "name": "Part 3: The religious imperative to act for justice and peace — 3.1 The religious imperative"
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
            "name": "Part 1: Symbol, ritual and sacrament — 1.1 Symbols"
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
            "name": "Part 1: The Bible as living classic and sacred text — 1.1 The Bible as living classic"
          },
          {
            "id": "religious-education-7-1",
            "name": "1.2 The Bible as sacred text"
          },
          {
            "id": "religious-education-7-2",
            "name": "Part 2: Text and community — 2.1 The formation of the Hebrew scriptures"
          },
          {
            "id": "religious-education-7-3",
            "name": "2.2 The Gospels"
          },
          {
            "id": "religious-education-7-4",
            "name": "Part 3: The literature of the Bible — 3.1 The language of story"
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
            "name": "Part 3: Christianity in Ireland — 3.1 The coming of Patrick"
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
            "name": "3.5 Religion and the ideas of the Enlightenment / modern period"
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
            "name": "Part 2: The relationship between religion and science — 2.1 Science and religion go their separate ways (Galileo)"
          },
          {
            "id": "religious-education-9-2",
            "name": "2.2 Science and religion in tension (Darwin)"
          },
          {
            "id": "religious-education-9-3",
            "name": "2.3 Science and religion in dialogue (the ecological crisis)"
          },
          {
            "id": "religious-education-9-4",
            "name": "2.4 Science and religion in dialogue (understanding of creation)"
          },
          {
            "id": "religious-education-9-5",
            "name": "Part 3: Current issues for religion and science: origins — 3.1 The debate about origins"
          },
          {
            "id": "religious-education-9-6",
            "name": "3.2 The new physics and religion (Higher level)"
          },
          {
            "id": "religious-education-9-7",
            "name": "Part 4: Current issues for religion and science: life and death — 4.1 Fundamental issues"
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
            "name": "Romanesque and Gothic (c. 1000 - 1500s)"
          },
          {
            "id": "art-4-1",
            "name": "The Renaissance - Proto, Early, High Renaissance & Mannerism (c. 1300 - 1600s)"
          },
          {
            "id": "art-4-2",
            "name": "Baroque (c. 1600 - 1700s)"
          },
          {
            "id": "art-4-3",
            "name": "Realism, Impressionism and Post-Impressionism (c. 1850 - 1900s)"
          },
          {
            "id": "art-4-4",
            "name": "Modernism (c. 1900 - 1960s)"
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
            "name": "Pre-Christian (c. 4,000 BCE - 500 CE)"
          },
          {
            "id": "art-5-1",
            "name": "Insular Art (c. 500 - 1100s)"
          },
          {
            "id": "art-5-2",
            "name": "Late Medieval Architecture and Art (c. 1100 - 1550s)"
          },
          {
            "id": "art-5-3",
            "name": "Georgian period (c. 1720 - 1800s)"
          },
          {
            "id": "art-5-4",
            "name": "Irish Art and Modernism (c. 1880 - c. 1960s)"
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
            "name": "Singing or playing individually (Appendix A) - includes singing individually, performing individually, and traditional/popular/classical art repertoires"
          },
          {
            "id": "music-0-1",
            "name": "Singing or playing as a member of a musical group (Appendix B) - e.g. traditional Irish groups, folk groups, recorder groups, madrigal groups, choral groups, orchestral groups, bands, mixed vocal/instrumental ensembles, stage musical/operetta extracts"
          },
          {
            "id": "music-0-2",
            "name": "Rehearsing and conducting a musical group (Appendix C)"
          },
          {
            "id": "music-0-3",
            "name": "Prepared songs or pieces (two at Ordinary level, three at Higher level)"
          },
          {
            "id": "music-0-4",
            "name": "Sight reading test (unprepared test option)"
          },
          {
            "id": "music-0-5",
            "name": "Aural memory test (unprepared test option)"
          },
          {
            "id": "music-0-6",
            "name": "Unprepared improvisation (unprepared test option) - melodic, rhythmic, harmonic, free improvisation to a given mood/visual/text stimulus, or any combination"
          },
          {
            "id": "music-0-7",
            "name": "Accompaniments in individual performing (where appropriate)"
          },
          {
            "id": "music-0-8",
            "name": "Ornamentation in traditional Irish music performance"
          },
          {
            "id": "music-0-9",
            "name": "Microtechnology / music technology music-making systems (MIDI input, save/retrieve/edit a score, taped/printed final version)"
          },
          {
            "id": "music-0-10",
            "name": "Musical and technical fluency, holding own musical line in group performing"
          },
          {
            "id": "music-0-11",
            "name": "Choosing suitable repertoire (Appendix E) - classical art, traditional Irish, ethnic, folk, rock, jazz, stage musical and other modern popular repertoires"
          },
          {
            "id": "music-0-12",
            "name": "Higher level elective in performing - a programme of approximately 12 minutes' duration expanding the essential performing activity"
          }
        ]
      },
      {
        "id": "music-1",
        "name": "Composing",
        "subtopics": [
          {
            "id": "music-1-0",
            "name": "Rudiments of music and notation - treble and bass staves, diatonic intervals (unison to octave), rhythmic values (semibreve to quaver incl. dotted minims/crotchets) and equivalent rests"
          },
          {
            "id": "music-1-1",
            "name": "Time signatures (2/4, 3/4, 4/4; compound duple 6/8 at Higher level) and major/minor keys (up to two sharps/flats Ordinary; up to four sharps/flats Higher)"
          },
          {
            "id": "music-1-2",
            "name": "Chord progressions in root position - major keys I, V, IV, ii, vi; minor keys i, V, iv, VI"
          },
          {
            "id": "music-1-3",
            "name": "First inversion chords (Higher level) - major keys Ib, Vb, IVb, iib; minor keys ib, Vb, ivb, iiob"
          },
          {
            "id": "music-1-4",
            "name": "The dominant seventh (V7) and the cadential 6/4 chord in stock phrases (Higher level)"
          },
          {
            "id": "music-1-5",
            "name": "Modulation to the dominant and non-chord notes in a melodic context (Higher level)"
          },
          {
            "id": "music-1-6",
            "name": "Melody writing (eight bars Ordinary, sixteen bars Higher) - continuation of a given opening, setting of a given text, or using a given dance rhythm/metre and/or form"
          },
          {
            "id": "music-1-7",
            "name": "Harmony exercises (Ordinary level) - providing cadential melody/bass notes; adding bass notes and chord indications at cadence points; adding descant notes and chord indications at cadence points"
          },
          {
            "id": "music-1-8",
            "name": "Harmony exercises (Higher level) - composing melody and bass from a given set of chords; composing supportive bass and backing chords to a given tune; adding a countermelody/descant and chordal support to a given tune"
          },
          {
            "id": "music-1-9",
            "name": "Higher level elective in composing (portfolio) - original compositions/arrangements/orchestrations using conventional, traditional, popular, ethnic, avant-garde or electro-acoustic approaches; full notation and written description; control of motivic, structural, tonal and expressive features"
          }
        ]
      },
      {
        "id": "music-2",
        "name": "Listening",
        "subtopics": [
          {
            "id": "music-2-0",
            "name": "Prescribed works (Appendix F) - study four set works in detail: musical features, musical style and historical context, patterns of repetition and change (rotating Group A / Group B)"
          },
          {
            "id": "music-2-1",
            "name": "Comparative judgements and evaluation of interpretation and performance (Higher level prescribed-works requirement)"
          },
          {
            "id": "music-2-2",
            "name": "Irish music - range and variety of Irish music heard today; Irish musical idioms and influences; traditional and modern-day performing styles and contribution to folk music abroad (Higher level)"
          },
          {
            "id": "music-2-3",
            "name": "Aural skills - working knowledge of musical notation"
          },
          {
            "id": "music-2-4",
            "name": "Aural perception of melody and rhythm within a musical context; vocal and instrumental timbres"
          },
          {
            "id": "music-2-5",
            "name": "Simple musical structures (binary, ternary, variation, rondo) and idiomatic melodic/rhythmic features"
          },
          {
            "id": "music-2-6",
            "name": "Higher level aural skills - semiquaver movement and compound time; stylistic features affecting musical textures; identifying perfect, imperfect, plagal and interrupted cadences"
          },
          {
            "id": "music-2-7",
            "name": "General listening - listening to a wide variety of musical styles and genres, past and present, from our own and other environments"
          },
          {
            "id": "music-2-8",
            "name": "Higher level elective in listening - special study topic (Appendix G): art music from a specific period (e.g. Medieval, Romantic, Impressionist), contemporary popular or art genres, or traditional/ethnic music; e.g. plainchant, English Renaissance madrigals, the concerto grosso, the Classical symphony, German lieder, Italian opera, Russian ballet music, Impressionist piano music, American popular song, film music, early jazz, popular Irish music, contemporary Irish composers, string quartets, ethnic music from Asia"
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
            "name": "Orthographic Projection (principal planes of reference, projection of right and oblique solids, auxiliary views incl. second and subsequent auxiliary views, sectional views, true shapes and true lengths, right solids in contact, projection of cube and tetrahedron with inscribed and circumscribed spheres)"
          },
          {
            "id": "design-and-communication-graphics-0-2",
            "name": "Pictorial Projection: Isometric Drawing and Axonometric Projection (isometric drawing of solids, derivation/construction/application of the isometric scale, the axonometric plane and axes, orthogonal axonometric projection)"
          },
          {
            "id": "design-and-communication-graphics-0-3",
            "name": "Pictorial Projection: Perspective Drawing/Projection (parallel and angular perspective, vanishing points, picture plane, ground line and horizon lines, vanishing points for inclined lines)"
          },
          {
            "id": "design-and-communication-graphics-0-4",
            "name": "Plane Geometry (construction of plane figures, construction of loci, circles in contact with points, lines and curves)"
          },
          {
            "id": "design-and-communication-graphics-0-5",
            "name": "Conic Sections (terminology for conics, ellipse/parabola/hyperbola as sections of a right cone, focal points, focal sphere, directrix and eccentricity, conic curves as geometric loci, tangents to conics, double hyperbola, centre of curvature and evolute)"
          },
          {
            "id": "design-and-communication-graphics-0-6",
            "name": "Descriptive Geometry of Lines and Planes (simply inclined and oblique planes, oblique and tangent planes, true shape and inclinations of planes, intersection of oblique planes/lines and dihedral angle, sectioning of right solids by oblique planes, laminar surfaces from co-ordinates, skew lines, spatial relationships between lines and planes)"
          },
          {
            "id": "design-and-communication-graphics-0-7",
            "name": "Intersection and Development of Surfaces (surface development and envelopment of right and oblique solids; intersection of surfaces of prisms, pyramids, cones, cylinders and spheres, their frustra and composite solids, and development of same)"
          }
        ]
      },
      {
        "id": "design-and-communication-graphics-1",
        "name": "Communication of Design and Computer Graphics (Core)",
        "subtopics": [
          {
            "id": "design-and-communication-graphics-1-0",
            "name": "Graphics in Design and Communication (drawing from a historical perspective, design strategies, reflection on processes of design, design appraisal, generation and interpretation of design briefs, ideas sketching, design problem solving, design communication)"
          },
          {
            "id": "design-and-communication-graphics-1-1",
            "name": "Communication of Design (drawing conventions/symbols/standards, presentation methods and layout, design drawings and associated processes, pictorial and orthographic working and assembly drawings, balloon extraction detailing, exploded pictorial views, dimensioning and notation, schematic diagrams)"
          },
          {
            "id": "design-and-communication-graphics-1-2",
            "name": "Freehand Drawing (materials for freehand drawing, observation techniques, representing shape/form/texture/material, light and shade, design sketching, freehand detailing, use of colour)"
          },
          {
            "id": "design-and-communication-graphics-1-3",
            "name": "Information and Communication Technologies: CAD Applications (file management, graphics and CAD terminology and software, working drawings from part and assembly models, CAD sketching principles, creating 3D assemblies, presentation drawings from parametric models, exploded views and animated sequences, modelling and editing, templates and libraries, data exchange, graphic output)"
          },
          {
            "id": "design-and-communication-graphics-1-4",
            "name": "Information and Communication Technologies: ICT and Graphics (file management and organisation, file formats and filename extensions, image transfer, image processing and manipulation, web research, presentation techniques using ICT and CAD software)"
          },
          {
            "id": "design-and-communication-graphics-1-5",
            "name": "Student Assignment (design investigation and modification, or design investigation and concept design; CAD modelling, presentation, inclusive and user-centred design, reflective evaluation)"
          }
        ]
      },
      {
        "id": "design-and-communication-graphics-2",
        "name": "Applied Graphics (Optional Areas of Study – two to be chosen)",
        "subtopics": [
          {
            "id": "design-and-communication-graphics-2-0",
            "name": "Dynamic Mechanisms (common geometric loci: involutes, helices, conical spirals, Archimedean spirals, logarithmic spirals; cycloids, epicycloids, hypocycloids, trochoids; tangents to these curves; loci from linkage mechanisms; cam profiles and displacement diagrams for knife-edge, roller and flat followers; involute and epicycloidal gear profiles)"
          },
          {
            "id": "design-and-communication-graphics-2-1",
            "name": "Structural Forms (natural and manufactured structural forms; arches, domes, vaults, frames and surface structures; singly and doubly ruled surfaces; the hyperbolic paraboloid as a ruled surface and as a surface of translation; plane directors; the hyperboloid of revolution, projections and sections; sections through ruled surfaces; the geodesic dome of not more than four points of frequency)"
          },
          {
            "id": "design-and-communication-graphics-2-2",
            "name": "Geologic Geometry (symbols and notation; bearings, grid layout, true north; interpolation and plotting of contours; slopes and gradients; profiles from contours; skew boreholes in mining problems; true and apparent dip of ore strata; strike and thickness of strata; determination of outcrop; cutting and embankment sections for level and inclined constructions)"
          },
          {
            "id": "design-and-communication-graphics-2-3",
            "name": "Surface Geometry (dihedral angles between surfaces; surface developments of containers and structures – plane intersecting roof surfaces, sheet metal containers, hoppers, transition pieces; projections and developments of intersecting prismatic, right and oblique cylindrical, oblique conical, transition and ducting details; transition pieces connecting rectilinear-to-rectilinear, circular-to-circular and circular-to-rectilinear cross-sections)"
          },
          {
            "id": "design-and-communication-graphics-2-4",
            "name": "Assemblies (interpretation of exploded and assembled drawings; drawing layout and conventions; system of projection; sectional views; hatching; dimensioning; joining methods; machine surface and texture symbols; modelling assemblies in 3D CAD)"
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
            "name": "General (historical development of buildings; aesthetic principles; elements of and controls over the built environment; planning permission; choosing a site; house purchase, mortgages, insurance; role of the construction industry; drawings/documents, scales, symbols and notation; dimensioned drawings and freehand sketches; site investigation; conservation orders; structural principles; exposure to the elements; site safety; B.S. fire tests; building regulations)"
          },
          {
            "id": "construction-studies-0-1",
            "name": "Substructure (excavation; removal of vegetable soil; water in excavations; functions of and factors in choice of foundations; subsoil movement; strip, slab, short bored pile and pad foundations; steel reinforcement; concrete materials, storage, batching by volume/weight; water/cement ratio; site-mixed v ready-mixed concrete)"
          },
          {
            "id": "construction-studies-0-2",
            "name": "Superstructure (relationship of super- to substructure; structural forms; external envelope and its functions; choice of materials for external walls; bonding and attached piers; parapet walls; damp proof courses and membranes; lintels and arches; windows, glass and glazing; doors, door schedules, sizes, door sets and openings; roofs - timber pitched roofs to 7,500mm span, trusses and trussed rafters, single/double lap coverings, sarking and thermal insulation, timber flat roofs to 4,000mm span, mastic asphalt and built-up finishes, eaves, verges and abutments)"
          },
          {
            "id": "construction-studies-0-3",
            "name": "Internal Construction (internal walls - brick and block, openings, finishes; ground floors - solid and suspended timber; suspended timber upper floors, trimmings, strutting; stairs - rise, going, handrail, headroom; stud partitions and internal doors; dry lining and plasterboard ceilings; plasters and plaster finishes; oil- and water-bound paints, application and defects in painted finishes)"
          },
          {
            "id": "construction-studies-0-4",
            "name": "Services and External Works (entry/outlet of services; service installation materials and protection; direct and indirect hot and cold water systems; storage cisterns and hot water cylinders; small bore heating systems and heat conservation; rainwater collection - gutters and downpipes; underground drainage, sanitary fitments, single stack system, separate and combined systems, septic tanks, rigid and flexible drains; domestic fireplaces and flues; domestic electrical installation - power and lighting circuits, cables, circuit protection, ESB consumer control gear)"
          },
          {
            "id": "construction-studies-0-5",
            "name": "Heat and Thermal Effects in Buildings (thermal resistance, resistivity and conductivity; thermal transmittance of surfaces and composite barriers; thermal bridges; insulating materials; steady state heat loss and costs-in-use calculations; statutory U-values; solar and other heat gain; radiant/dry bulb/wet bulb temperature; humidity and the psychrometric chart; ventilation rates; human comfort; surface condensation and vapour barriers)"
          },
          {
            "id": "construction-studies-0-6",
            "name": "Illumination in Buildings (the way we see - nature of light, reflection, refraction, concept of illumination; units of illumination, C.I.E. standard overcast sky, daylight factor; calculation of average illumination by the degree of efficiency method; glare and the glare index; acuity and vision; conditions for good illumination)"
          },
          {
            "id": "construction-studies-0-7",
            "name": "Sound in Buildings (the way we hear - nature and propagation of sound waves, sound power/intensity/pressure, response of the ear, threshold of audibility; the decibel, inverse square law; reverberation and reverberation time; airborne and impact noise insulation; loss of hearing, threshold shift, recommended noise levels; attenuation of noise and protection devices)"
          }
        ]
      },
      {
        "id": "construction-studies-1",
        "name": "Part 2 - Practical Skills",
        "subtopics": [
          {
            "id": "construction-studies-1-0",
            "name": "Tools (maintenance and care in use of tools; common woodworking tools - uses, construction and mechanical principles; grinding, sharpening and maintenance of workshop equipment; safety precautions with edged tools and electricity)"
          },
          {
            "id": "construction-studies-1-1",
            "name": "Processes (construction of joints used in partitions, floors, stairs, roofs, structural timbers, doors, windows, frames, box and carcase construction and simple fitments; jointing and use of manufactured boards; storage; principles of joint choice; measuring/testing for accuracy; surface preparation and finishing; cutting lists and the setting-out rod; glues and adhesives; holding and supporting work; design and use of jigs)"
          }
        ]
      },
      {
        "id": "construction-studies-2",
        "name": "Part 3 - Course Work and Projects",
        "subtopics": [
          {
            "id": "construction-studies-2-0",
            "name": "Project options (a Building Detail incorporating a minimum of three craft practices; a Building Science Project relating to craft practice; or a Written/Drawn Project relating to the craft heritage of the architectural heritage or built environment)"
          },
          {
            "id": "construction-studies-2-1",
            "name": "Workshop/laboratory course work (assigned, supervised experiments and pupil-led projects; assessment of manipulative skills, equipment care, plan of procedure, experimentation, conclusions and presentation)"
          },
          {
            "id": "construction-studies-2-2",
            "name": "Building Science - Timber and Adhesives (characteristics of soft and hard woods; seasoning and storing; characteristics and grading of manufactured boards/timber; types, properties and selection of glues and adhesives)"
          },
          {
            "id": "construction-studies-2-3",
            "name": "Building Science - Porosity and Durability of Materials (pore structure; porosity, water absorption, surface tension, capillarity, permeability, saturation coefficient; crystallisation, efflorescence, sulphate attack on stone mortars, bricks and concrete; sources of sulphates)"
          },
          {
            "id": "construction-studies-2-4",
            "name": "Building Science - Aggregates and Concrete (voids in granular materials; grading of sands and aggregates and its effect on mortar/concrete mixes; reduction in volume on mixing; strength v density and strength v water-cement ratio)"
          },
          {
            "id": "construction-studies-2-5",
            "name": "Building Science - Binders, Setting and Hydration (setting of gypsum and Portland cement as hydration; retarders and accelerators, heat of hydration, strength-time relation, strength tests; setting of lime, insoluble/soluble matter, fineness, soundness and hydraulic strength tests)"
          },
          {
            "id": "construction-studies-2-6",
            "name": "Building Science - Paints, Pigments and Solvents (pigments - tinting strength, light fastness, bleeding, particle size/shape, thermal stability; solvents - abrasion resistance, drying time, opacity)"
          },
          {
            "id": "construction-studies-2-7",
            "name": "Building Science - Water and Comfort Conditions (water hardness, alkaline/temporary v permanent, water-softening; electro-chemical series; vapour pressure; comfort conditions; humidity and condensation)"
          },
          {
            "id": "construction-studies-2-8",
            "name": "Building Science - Heat (nature and effects of heat; transmission of heat; thermometry; calorimetry; coefficient of thermal conductivity; temperature gradients through composite constructions)"
          },
          {
            "id": "construction-studies-2-9",
            "name": "Building Science - Light (nature of light; reflection, refraction; photometry; daylighting; illumination; light source; measurement of light)"
          },
          {
            "id": "construction-studies-2-10",
            "name": "Building Science - Electricity (electrical circuits; measurement of electricity; generators; motors; earthing considerations)"
          },
          {
            "id": "construction-studies-2-11",
            "name": "Building Science - Acoustics (attenuation of noise at source; reverberation)"
          }
        ]
      },
      {
        "id": "construction-studies-3",
        "name": "Appendix 1 (Leaving Certificate Vocational Programme - optional, examined by optional questions)",
        "subtopics": [
          {
            "id": "construction-studies-3-0",
            "name": "Design (components of design problems and the design process; measurement criteria and judgement in design; simple aesthetic principles; functions of models in design and modelmaking materials/finishes; designing with computers - working drawings on screen and plotter, hardware, software)"
          },
          {
            "id": "construction-studies-3-1",
            "name": "Structures (structural forms - space frames, wide-span structures, air-supported and curved/doubly-curved membranes, cable nets, cable-supported roofs, domes, bridges and forms occurring in nature; structural functions - resisting dead and dynamic loads, tests/analyses using models and test rigs)"
          },
          {
            "id": "construction-studies-3-2",
            "name": "New Technology Applications (principles of electronic control circuits and devices applied to models and mechanisms; operation, control and management of computer-aided machine; role of block models in computer-aided manufacture)"
          },
          {
            "id": "construction-studies-3-3",
            "name": "Marketing (school-based enterprise activities; market research, cost analyses and quality control; sales techniques including presentation and exhibition of goods)"
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
            "name": "Personal Protection (clothing, eye, ear, respiratory, skin)"
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
            "name": "Marking out and measurement (rule, squares, surface gauge, protractor, Vernier caliper, micrometer)"
          },
          {
            "id": "engineering-1-1",
            "name": "Shaping"
          },
          {
            "id": "engineering-1-2",
            "name": "Bending & folding (metal and plastics)"
          },
          {
            "id": "engineering-1-3",
            "name": "Surface finish (filing, emery, steel wool, painting & dip coating)"
          },
          {
            "id": "engineering-1-4",
            "name": "Lathe (parts, accessories, work holding, operations, taper turning)"
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
            "name": "Welding (resistance welding)"
          },
          {
            "id": "engineering-1-9",
            "name": "Adhesive"
          },
          {
            "id": "engineering-1-10",
            "name": "Fasteners (rivets, screws, pins, threading)"
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
            "name": "Materials Testing (hardness, conductivity, toughness, elasticity, malleability, magnetism; plastics ID tests)"
          },
          {
            "id": "engineering-2-1",
            "name": "Properties of Materials (ferrous, non-ferrous, pure, precious metals, alloys & composites)"
          },
          {
            "id": "engineering-2-2",
            "name": "Origin and production of materials (mining, iron ore extraction, carbon steel production, plastics & polymerisation)"
          },
          {
            "id": "engineering-2-3",
            "name": "Recycling"
          },
          {
            "id": "engineering-2-4",
            "name": "Structure of Materials (states of matter, heat treatment, steel equilibrium diagram)"
          },
          {
            "id": "engineering-2-5",
            "name": "Heat Treatment (hardening & tempering, annealing, normalising)"
          },
          {
            "id": "engineering-2-6",
            "name": "Corrosion (chemical and electrochemical corrosion, prevention, protection)"
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
            "name": "Framework for designing (research, briefs & specifications, planning, prototype, evaluation)"
          },
          {
            "id": "engineering-3-6",
            "name": "Product design (product, case study, the designer in action, evaluation)"
          }
        ]
      },
      {
        "id": "engineering-4",
        "name": "Core: Computer Aided Processes (CAD/CAM)",
        "subtopics": [
          {
            "id": "engineering-4-0",
            "name": "Drawing functions (3-D CAD drawing)"
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
            "name": "CAM Principles (two-axes programming, Z and X axes)"
          },
          {
            "id": "engineering-4-6",
            "name": "CAM Co-ordinates (absolute co-ordinates)"
          }
        ]
      },
      {
        "id": "engineering-5",
        "name": "Core: Power and Energy",
        "subtopics": [
          {
            "id": "engineering-5-0",
            "name": "Engines (four-stroke engine cycle)"
          },
          {
            "id": "engineering-5-1",
            "name": "Electric Motors (principle of the electric motor, electro-magnet)"
          },
          {
            "id": "engineering-5-2",
            "name": "Cells and Batteries (simple cell)"
          },
          {
            "id": "engineering-5-3",
            "name": "Energy (concept, conservation, conversion, renewable sources)"
          }
        ]
      },
      {
        "id": "engineering-6",
        "name": "Core: Electronics",
        "subtopics": [
          {
            "id": "engineering-6-0",
            "name": "Electronic circuits (resistors, diodes, LEDs, NPN transistors, LDRs, thermistors)"
          },
          {
            "id": "engineering-6-1",
            "name": "Transistor Circuits (transistor as a switch)"
          },
          {
            "id": "engineering-6-2",
            "name": "Measurement (multi-meter: voltage, resistance)"
          },
          {
            "id": "engineering-6-3",
            "name": "Electronic Units (Volts, Amps, Ohms; Ohm's law)"
          },
          {
            "id": "engineering-6-4",
            "name": "Sensitive circuits (LDRs, thermistors, variable resistors as sensors)"
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
            "name": "Levers (three classes of levers, mechanical advantage)"
          },
          {
            "id": "engineering-7-2",
            "name": "Pulleys & belt drives (flat, vee and toothed)"
          },
          {
            "id": "engineering-7-3",
            "name": "Gears and gearing (simple and compound gear trains, gear ratios)"
          }
        ]
      },
      {
        "id": "engineering-8",
        "name": "Core: Pneumatics",
        "subtopics": [
          {
            "id": "engineering-8-0",
            "name": "Pneumatic Circuit (single/double-acting cylinder)"
          },
          {
            "id": "engineering-8-1",
            "name": "Valves (three-port valve)"
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
            "name": "Cylinders (single and double acting)"
          }
        ]
      },
      {
        "id": "engineering-9",
        "name": "Option: Computer Aided Processes (CAD/CAM)",
        "subtopics": [
          {
            "id": "engineering-9-0",
            "name": "Design (use of CAD in design)"
          },
          {
            "id": "engineering-9-1",
            "name": "Drawing functions (additional commands, solid models from profile)"
          },
          {
            "id": "engineering-9-2",
            "name": "Dimensioning (modifying a 3-D model)"
          },
          {
            "id": "engineering-9-3",
            "name": "Drawing Generation (parts and assemblies, basic animation)"
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
            "name": "Drive system for CAM (stepper motors, photo-electric encoders)"
          },
          {
            "id": "engineering-9-7",
            "name": "Applications of CAM (industry, advantages/disadvantages of CNC)"
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
            "name": "Geometric Drawing (prisms, pyramids, polygons, ellipse, parabola)"
          },
          {
            "id": "engineering-10-2",
            "name": "Beaten metalwork (hollowing, raising, planishing, sinking, repoussé, chasing)"
          },
          {
            "id": "engineering-10-3",
            "name": "Jewellery work / techniques (piercing, chains, rings, stone setting)"
          },
          {
            "id": "engineering-10-4",
            "name": "Enamelling (firing, champlevé, free dusting, stencilling, paste)"
          },
          {
            "id": "engineering-10-5",
            "name": "Etching (acids and resists for brass, copper, aluminium)"
          },
          {
            "id": "engineering-10-6",
            "name": "Surface Treatment / Decorative Finishes (oxidation, anodising, polishing, mottling, lacquers)"
          },
          {
            "id": "engineering-10-7",
            "name": "Edge finishing (beaded edge, wired edge, folded seam)"
          },
          {
            "id": "engineering-10-8",
            "name": "Hot and cold forming (drawing down, turning an eye, twisting, scrollwork, riveting)"
          },
          {
            "id": "engineering-10-9",
            "name": "Joining Processes (silver soldering, brazing, manual arc & inert gas welding)"
          },
          {
            "id": "engineering-10-10",
            "name": "Casting (low melting point alloy, polymers, investment & silicone casting)"
          },
          {
            "id": "engineering-10-11",
            "name": "Celtic Metalwork (Ardagh Chalice, Thistle brooch, bronze age spear head)"
          }
        ]
      },
      {
        "id": "engineering-11",
        "name": "Option: Power, Energy and Control (Energy Power & Control)",
        "subtopics": [
          {
            "id": "engineering-11-0",
            "name": "Design (control devices in design problems)"
          },
          {
            "id": "engineering-11-1",
            "name": "Energy (storing energy, fossil fuels, the Joule, energy conversion, calorific value)"
          },
          {
            "id": "engineering-11-2",
            "name": "Control device (model unit incorporating a control device)"
          },
          {
            "id": "engineering-11-3",
            "name": "Computer Interfacing"
          },
          {
            "id": "engineering-11-4",
            "name": "Work (Work = Force x Distance)"
          },
          {
            "id": "engineering-11-5",
            "name": "Power (mechanical power, electrical power, engines, electrical generator)"
          },
          {
            "id": "engineering-11-6",
            "name": "Efficiency of systems"
          },
          {
            "id": "engineering-11-7",
            "name": "Control (control system elements, transducers/sensors/actuators, feedback, mechanical/electronic/computer/pneumatic control)"
          }
        ]
      },
      {
        "id": "engineering-12",
        "name": "Option: Manufacturing Techniques and Technology",
        "subtopics": [
          {
            "id": "engineering-12-0",
            "name": "Design (framework for design)"
          },
          {
            "id": "engineering-12-1",
            "name": "Manufacture (components from a variety of materials)"
          },
          {
            "id": "engineering-12-2",
            "name": "Lathe Turning (reaming, knurling, parting off, 4-jaw chuck/eccentric turning, turning between centres)"
          },
          {
            "id": "engineering-12-3",
            "name": "Grinding (grind-wheel dressing, loading, glazing, structure of grind-wheels)"
          },
          {
            "id": "engineering-12-4",
            "name": "Soldering (silver soldering, brazing)"
          },
          {
            "id": "engineering-12-5",
            "name": "Welding (oxy/acetylene, manual arc, inert gas, MAG/TAG, thermal welding of plastics)"
          },
          {
            "id": "engineering-12-6",
            "name": "Heat Treatment (normalising, case hardening, annealing, pack carburising)"
          },
          {
            "id": "engineering-12-7",
            "name": "Hot forming of metal (drop forging, extrusion, hot rolling)"
          },
          {
            "id": "engineering-12-8",
            "name": "Shaping of Plastics (vacuum forming, blow moulding, extrusion, compression, injection moulding, calendaring)"
          },
          {
            "id": "engineering-12-9",
            "name": "Metrology (limits and fits; clearance, transition, interference fit)"
          }
        ]
      },
      {
        "id": "engineering-13",
        "name": "Option: Materials Science",
        "subtopics": [
          {
            "id": "engineering-13-0",
            "name": "Design (materials to fulfil design criteria)"
          },
          {
            "id": "engineering-13-1",
            "name": "Classification of Materials (ferrous, non-ferrous, polymer, composite, ceramic)"
          },
          {
            "id": "engineering-13-2",
            "name": "Structure of Materials (crystalline structure BCC/FCC/CPH, ionic/covalent/metallic bonds, solid solutions, iron/carbon equilibrium diagram, ferrite/pearlite/cementite/martensite/austenite, plastics classification)"
          },
          {
            "id": "engineering-13-3",
            "name": "Corrosion (electrochemical series, sacrificial protection, effects on environment, design)"
          },
          {
            "id": "engineering-13-4",
            "name": "Materials testing (destructive: Brinell, Vickers, Rockwell, Izod, extensometer, cyclic; non-destructive: X-ray, ultrasound, dye)"
          },
          {
            "id": "engineering-13-5",
            "name": "Origin and production of materials (ore concentration, production of aluminium and copper, recovery and recycling)"
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
            "name": "1.2 Analysing skill and technique (biomechanical: planes and axes, levers; movement: vectors and scalars, Newton's laws of motion; quality/effectiveness)"
          },
          {
            "id": "physical-education-0-3",
            "name": "1.3 Skill acquisition (stages of learning, effective practice, practice schedules and methods)"
          },
          {
            "id": "physical-education-0-4",
            "name": "Topic 2: Physical and psychological demands of performance"
          },
          {
            "id": "physical-education-0-5",
            "name": "2.1 Physical fitness (health- vs performance-related fitness)"
          },
          {
            "id": "physical-education-0-6",
            "name": "2.2 Health-related fitness (cardio-respiratory endurance, muscular endurance, strength, flexibility, body composition)"
          },
          {
            "id": "physical-education-0-7",
            "name": "2.3 Performance-related fitness (agility, balance, co-ordination, power, speed, reaction time)"
          },
          {
            "id": "physical-education-0-8",
            "name": "2.4 Application of health- and performance-related components of fitness"
          },
          {
            "id": "physical-education-0-9",
            "name": "2.5 Assessment of health- and performance-related components of physical fitness (fitness test battery, principles of training, FITT formula)"
          },
          {
            "id": "physical-education-0-10",
            "name": "2.6 Designing a fitness plan (training methods, periodisation, recovery and adaptation)"
          },
          {
            "id": "physical-education-0-11",
            "name": "2.7 Psychological preparation (confidence, anxiety, motivation, concentration, feedback)"
          },
          {
            "id": "physical-education-0-12",
            "name": "2.8 Diet and nutrition (hydration, sports supplements, energy systems)"
          },
          {
            "id": "physical-education-0-13",
            "name": "Topic 3: Structures, strategies, roles and conventions"
          },
          {
            "id": "physical-education-0-14",
            "name": "3.1 Structures, strategies and/or compositional elements"
          },
          {
            "id": "physical-education-0-15",
            "name": "3.2 Roles and relationships"
          },
          {
            "id": "physical-education-0-16",
            "name": "3.3 Safe practice (warm-up/cool-down, attire, equipment, facilities, injuries and first aid, overtraining)"
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
            "name": "4.2 Methods of analysis (skill and technique, structures and strategies, choreography, performance-related fitness, psychological preparedness)"
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
            "name": "5.1 Benefits of physical activity participation (play, leisure and recreation, physical education, mass-participation sports, outdoor and adventure activities, sport)"
          },
          {
            "id": "physical-education-1-2",
            "name": "5.2 Physical activity participation (supports and barriers, data collection, participation patterns)"
          },
          {
            "id": "physical-education-1-3",
            "name": "5.3 Physical activity promotion (national/local policies, national governing bodies)"
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
            "name": "6.1 Principles of ethical practice (integrity, respect, fairness, equity)"
          },
          {
            "id": "physical-education-1-7",
            "name": "6.2 Codes of ethics (sportsmanship and gamesmanship)"
          },
          {
            "id": "physical-education-1-8",
            "name": "6.3 Drugs and sport (performance-enhancing drugs)"
          },
          {
            "id": "physical-education-1-9",
            "name": "6.4 Anti-doping rules (Irish anti-doping rules, therapeutic use exemption)"
          },
          {
            "id": "physical-education-1-10",
            "name": "6.5 Best practice for the use of supplements"
          },
          {
            "id": "physical-education-1-11",
            "name": "Topic 7: Physical activity and inclusion (optional/prescribed topic)"
          },
          {
            "id": "physical-education-1-12",
            "name": "7.1 Supports and barriers to physical activity participation for selected groups (women, older adults, physical disability, intellectual disability, ethnic groups, socio-economic groups)"
          },
          {
            "id": "physical-education-1-13",
            "name": "7.2 Addressing barriers to physical activity"
          },
          {
            "id": "physical-education-1-14",
            "name": "7.3 Developments in physical activity and sporting opportunities over the past twenty years"
          },
          {
            "id": "physical-education-1-15",
            "name": "7.4 Adapted physical activity"
          },
          {
            "id": "physical-education-1-16",
            "name": "Topic 8: Technology, media and sport (optional/prescribed topic)"
          },
          {
            "id": "physical-education-1-17",
            "name": "8.1 The impact of technology on sport and physical activity"
          },
          {
            "id": "physical-education-1-18",
            "name": "8.2 Media in sport"
          },
          {
            "id": "physical-education-1-19",
            "name": "Topic 9: Gender and physical activity (optional/prescribed topic)"
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
            "name": "9.3 Gender socialisation and its impact on physical activity participation (hegemonic masculinity and femininity)"
          },
          {
            "id": "physical-education-1-23",
            "name": "Topic 10: Business and enterprise in physical activity and sport (optional/prescribed topic)"
          },
          {
            "id": "physical-education-1-24",
            "name": "10.1 Sponsorship and advertising in physical activity and sport"
          },
          {
            "id": "physical-education-1-25",
            "name": "10.2 Physical activity and sport – the business dimension"
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
            "name": "Adventure activities (Orienteering, Canoeing/Kayaking, Rock-climbing, Sailing, Rowing/Sculling)"
          },
          {
            "id": "physical-education-2-1",
            "name": "Artistic and aesthetic activities (Gymnastics: Artistic, Rhythmic; Dance: contemporary, folk, modern, ballet, jazz, tap, ethnic, traditional)"
          },
          {
            "id": "physical-education-2-2",
            "name": "Athletics (Running, Throwing, Jumping)"
          },
          {
            "id": "physical-education-2-3",
            "name": "Aquatics (Lifesaving, Survival swim, Two swimming strokes, Water-polo, Synchronised swimming)"
          },
          {
            "id": "physical-education-2-4",
            "name": "Games (Invasion, Striking/Fielding, Net/Wall)"
          },
          {
            "id": "physical-education-2-5",
            "name": "Personal exercise and fitness activities (aerobic training method plus a conditioning and resistance activity)"
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
            "name": "Unit 1 - Introduction to Working Life (local sources of employment, social services & job-creation agencies, transport, financial institutions, industrial relations agencies, principal economic activities, tourism potential, school vs work, intrinsic value of work / self-employment / voluntary work, employment of young workers legislation, workplace Health & Safety, workplace disputes, diversity in the workplace, assistance for unemployed people, training schemes)"
          },
          {
            "id": "lcvp-link-modules-0-1",
            "name": "Unit 2 - Job Seeking Skills (how job vacancies are advertised, applying by letter/telephone/e-mail, completing an application form, compiling a curriculum vitae in word-processed format, preparing for a job interview, simulated job interview)"
          },
          {
            "id": "lcvp-link-modules-0-2",
            "name": "Unit 3 - Career Investigation (personal aptitudes and interests, investigating careers, aptitudes & skills for a specific career, qualifications & training for entry, opportunities locally/nationally/internationally, interview and/or work shadowing, preparing the final Career Investigation report, reflection and evaluation)"
          },
          {
            "id": "lcvp-link-modules-0-3",
            "name": "Unit 4 - Work Placement (personal goals for placement, planning & organising the placement, punctuality, appropriate dress, following procedures & instructions, communicating with co-workers, Health & Safety instructions, reviewing personal experience, employer/adult reports on performance, evaluation against career aspirations, transfer of learning to home/school/community, diary/written/verbal placement report)"
          }
        ]
      },
      {
        "id": "lcvp-link-modules-1",
        "name": "Link Module 2: Enterprise Education",
        "subtopics": [
          {
            "id": "lcvp-link-modules-1-0",
            "name": "Unit 1 - Enterprise Skills (qualities & skills of enterprising people, personal/community/entrepreneurial enterprise, personal strengths & weaknesses, improving personal enterprise skills, working co-operatively in a team, value of teamwork, leadership of a group, planning & organising a meeting, making presentations to peers and adults, evaluation of successes & problems)"
          },
          {
            "id": "lcvp-link-modules-1-1",
            "name": "Unit 2 - Local Business Enterprises (identifying local enterprises, how an enterprise starts up & available support/training, planning an investigation of a local enterprise, organising visits & guest speakers, SWOT analysis of a business, reporting on entrepreneur visits & enterprise visits, products/services/markets/workforce, roles of adults in business, the Single European Market, ICT in business, education & training in business development, evaluation of successes & problems)"
          },
          {
            "id": "lcvp-link-modules-1-2",
            "name": "Unit 3 - Local Voluntary Organisations / Community Enterprises (identifying local voluntary bodies, work of voluntary groups, roles of adults in voluntary community organisations, organising community-enterprise visits & speakers, formulating questions on a community enterprise, preparing a report/plan/presentation on community development, evaluation of successes & problems)"
          },
          {
            "id": "lcvp-link-modules-1-3",
            "name": "Unit 4 - An Enterprise Activity (generating ideas co-operatively, preparing the enterprise plan, identifying resources, integrating information sources, assessing personal & group skills and training needs, recruiting consultants/advisers, market research & marketing mix, publicity & promotion, group roles - owner/worker/team leader, meeting targets, reviewing group & personal performance, written or verbal Enterprise Activity report, evaluation of successes & problems)"
          }
        ]
      }
    ]
  }
];
