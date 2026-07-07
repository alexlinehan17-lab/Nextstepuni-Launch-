/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Leaving Cert curriculum taxonomy — every examined subject -> levels ->
 * strands -> sub-topics, from the official syllabi (currently-examined spec).
 * Strand + sub-topic labels are concise picker labels (agent-polished from the
 * official names); ids are stable so Rep Card topic tags resolve against them.
 * Re-verify periodically.
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
        "name": "An Bhéaltriail (Oral Exam)",
        "subtopics": [
          {
            "id": "irish-0-0",
            "name": "Fáiltiú / Beannú"
          },
          {
            "id": "irish-0-1",
            "name": "Aithris Filíochta (Poetry Reading)"
          },
          {
            "id": "irish-0-2",
            "name": "Sraith Pictiúr (Picture Sequence)"
          },
          {
            "id": "irish-0-3",
            "name": "Comhrá Ginearálta (General Conversation)"
          },
          {
            "id": "irish-0-4",
            "name": "Saibhreas, Cruinneas, Líofacht"
          },
          {
            "id": "irish-0-5",
            "name": "Foghraíocht agus Blas"
          },
          {
            "id": "irish-0-6",
            "name": "Ullmhú don Bhéaltriail (Oral Prep Strategy)"
          }
        ]
      },
      {
        "id": "irish-1",
        "name": "An Chluastuiscint (Listening)",
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
            "name": "Cuid C — Píosaí Nuachta / Comhrá Raidió"
          },
          {
            "id": "irish-1-3",
            "name": "Tuiscint Éisteachta"
          }
        ]
      },
      {
        "id": "irish-2",
        "name": "An Cheapadóireacht (Composition)",
        "subtopics": [
          {
            "id": "irish-2-0",
            "name": "Aiste (Essay)"
          },
          {
            "id": "irish-2-1",
            "name": "Alt Nuachtáin / Irise"
          },
          {
            "id": "irish-2-2",
            "name": "Blag (Blog Post)"
          },
          {
            "id": "irish-2-3",
            "name": "Scéal (Story)"
          },
          {
            "id": "irish-2-4",
            "name": "Díospóireacht (Debate)"
          },
          {
            "id": "irish-2-5",
            "name": "Óráid (Speech)"
          },
          {
            "id": "irish-2-6",
            "name": "Giota Leanúnach (Ordinary)"
          },
          {
            "id": "irish-2-7",
            "name": "Saibhreas na Gaeilge"
          },
          {
            "id": "irish-2-8",
            "name": "Litir / Litir Fhoirmiúil (Letter)"
          },
          {
            "id": "irish-2-9",
            "name": "Comhrá (Written Conversation — OL)"
          }
        ]
      },
      {
        "id": "irish-3",
        "name": "An Léamhthuiscint (Reading)",
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
            "name": "Ceisteanna Tuisceana"
          },
          {
            "id": "irish-3-3",
            "name": "Cruinneas Teanga (Grammar within Léamhthuiscint B)"
          }
        ]
      },
      {
        "id": "irish-4",
        "name": "An Prós (Prose)",
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
            "name": "Cáca Milis (Gearrscannán)"
          },
          {
            "id": "irish-4-7",
            "name": "Prós: Ábhar Roghnach"
          },
          {
            "id": "irish-4-8",
            "name": "An Lasair Choille (Gearrdhráma)"
          },
          {
            "id": "irish-4-9",
            "name": "Clann Lir (2027+)"
          },
          {
            "id": "irish-4-10",
            "name": "Athair (2027+)"
          },
          {
            "id": "irish-4-11",
            "name": "Glantóir (2027+)"
          },
          {
            "id": "irish-4-12",
            "name": "An Bóthar go Santiago (2027+)"
          },
          {
            "id": "irish-4-13",
            "name": "Cuairteoir (2027+)"
          },
          {
            "id": "irish-4-14",
            "name": "An tIriseoir (2027+)"
          },
          {
            "id": "irish-4-15",
            "name": "Eoinín na nÉan (Gearrscannán, 2027+)"
          },
          {
            "id": "irish-4-16",
            "name": "An Féileacán agus an Crann Úll (2027+)"
          }
        ]
      },
      {
        "id": "irish-5",
        "name": "An Fhilíocht (Poetry)",
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
            "name": "Mo Ghrá-sa (idir Lúibíní)"
          },
          {
            "id": "irish-5-5",
            "name": "Colscaradh"
          },
          {
            "id": "irish-5-6",
            "name": "Filíocht: Ábhar Roghnach"
          },
          {
            "id": "irish-5-7",
            "name": "Dínit an Bhróin (2027+)"
          },
          {
            "id": "irish-5-8",
            "name": "Deireadh na Feide (2027+)"
          },
          {
            "id": "irish-5-9",
            "name": "Iníon (2027+)"
          },
          {
            "id": "irish-5-10",
            "name": "Glaoch Abhaile (2027+)"
          },
          {
            "id": "irish-5-11",
            "name": "Úirchill an Chreagáin (2027+)"
          }
        ]
      },
      {
        "id": "irish-6",
        "name": "Litríocht Bhreise (Higher Level)",
        "subtopics": [
          {
            "id": "irish-6-0",
            "name": "Prós Breise — An Triail"
          },
          {
            "id": "irish-6-1",
            "name": "Prós Breise — A Thig Ná Tit Orm"
          },
          {
            "id": "irish-6-2",
            "name": "Prós Breise — Tóraíocht D. & G."
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
          },
          {
            "id": "irish-6-11",
            "name": "Prós Breise (2027+) — Cóirín na dTonn"
          },
          {
            "id": "irish-6-12",
            "name": "Prós Breise (2027+) — An Nollaig Thiar"
          },
          {
            "id": "irish-6-13",
            "name": "Prós Breise (2027+) — Deirdre"
          },
          {
            "id": "irish-6-14",
            "name": "Prós Breise (2027+) — Dordán"
          },
          {
            "id": "irish-6-15",
            "name": "Prós Breise (2027+) — Bláth na dTulach"
          },
          {
            "id": "irish-6-16",
            "name": "Dán Breise (2027+) — Trén bhFearann Breac"
          },
          {
            "id": "irish-6-17",
            "name": "Dán Breise (2027+) — Eanáir 1991"
          },
          {
            "id": "irish-6-18",
            "name": "Dán Breise (2027+) — Ag Tiomáint Siar"
          },
          {
            "id": "irish-6-19",
            "name": "Dán Breise (2027+) — Dijeridiú"
          },
          {
            "id": "irish-6-20",
            "name": "Dán Breise (2027+) — Anthony Daly"
          }
        ]
      },
      {
        "id": "irish-7",
        "name": "Litríocht: Anailís Chomparáideach & Comhthuiscint",
        "subtopics": [
          {
            "id": "irish-7-0",
            "name": "Anailís Théamúil agus Stíle (Theme & Technique)"
          },
          {
            "id": "irish-7-1",
            "name": "Comhthéacs agus Téamaí"
          }
        ]
      },
      {
        "id": "irish-8",
        "name": "Scileanna Teanga / Gramadach",
        "subtopics": [
          {
            "id": "irish-8-0",
            "name": "An Tuiscint (Comprehension)"
          },
          {
            "id": "irish-8-1",
            "name": "An Labhairt (Speaking)"
          },
          {
            "id": "irish-8-2",
            "name": "An Scríobh (Writing)"
          },
          {
            "id": "irish-8-3",
            "name": "An Léitheoireacht (Reading)"
          },
          {
            "id": "irish-8-4",
            "name": "Gramadach (Grammar)"
          },
          {
            "id": "irish-8-5",
            "name": "Stór Focal agus Nathanna"
          }
        ]
      },
      {
        "id": "irish-9",
        "name": "An Bonnleibhéal (Foundation Level Tasks)",
        "subtopics": [
          {
            "id": "irish-9-0",
            "name": "Foirm a Líonadh (Fill in a Form)"
          },
          {
            "id": "irish-9-1",
            "name": "Pictiúir a Mheaitseáil le Téacs (Match Pictures with Text)"
          },
          {
            "id": "irish-9-2",
            "name": "Léamhthuiscintí Gearra (Bróisiúr / Litir / Sliocht / Alt / Dán)"
          },
          {
            "id": "irish-9-3",
            "name": "Scríobh — Litir / Fógra / Scéal"
          },
          {
            "id": "irish-9-4",
            "name": "Scéal ó Phictiúir (Write From Pictures)"
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
        "id": "english-6",
        "name": "Single Text",
        "subtopics": [
          {
            "id": "english-6-0",
            "name": "In-depth study of one prescribed text"
          },
          {
            "id": "english-6-1",
            "name": "Single text drama (often Shakespearean)"
          },
          {
            "id": "english-6-2",
            "name": "Attitudes, values and themes"
          },
          {
            "id": "english-6-3",
            "name": "Form, structure and style"
          }
        ]
      },
      {
        "id": "english-7",
        "name": "Comparative Study",
        "subtopics": [
          {
            "id": "english-7-0",
            "name": "Theme or Issue"
          },
          {
            "id": "english-7-1",
            "name": "Historical/Literary Period"
          },
          {
            "id": "english-7-2",
            "name": "Literary Genre"
          },
          {
            "id": "english-7-3",
            "name": "Cultural Context"
          },
          {
            "id": "english-7-4",
            "name": "General Vision and Viewpoint"
          },
          {
            "id": "english-7-5",
            "name": "Hero/Heroine/Villain"
          },
          {
            "id": "english-7-6",
            "name": "Relationships"
          },
          {
            "id": "english-7-7",
            "name": "Social Setting"
          },
          {
            "id": "english-7-8",
            "name": "Change and Development"
          },
          {
            "id": "english-7-9",
            "name": "Specific Themes"
          },
          {
            "id": "english-7-10",
            "name": "Aspects of Story"
          }
        ]
      },
      {
        "id": "english-8",
        "name": "Poetry",
        "subtopics": [
          {
            "id": "english-8-0",
            "name": "Prescribed poetry (Higher — eight poets)"
          },
          {
            "id": "english-8-1",
            "name": "Prescribed poetry (Ordinary)"
          },
          {
            "id": "english-8-2",
            "name": "Unseen poetry (Paper 2, response to a previously unseen poem)"
          }
        ]
      },
      {
        "id": "english-9",
        "name": "Composing",
        "subtopics": [
          {
            "id": "english-9-1",
            "name": "Composition — choice of formats (essay / personal essay / short story / speech / article / discursive)"
          }
        ]
      },
      {
        "id": "english-10",
        "name": "Comprehending",
        "subtopics": [
          {
            "id": "english-10-0",
            "name": "Reading & comprehension (Paper 1, Question A)"
          },
          {
            "id": "english-10-1",
            "name": "Functional writing (Paper 1, Question B)"
          }
        ]
      },
      {
        "id": "english-11",
        "name": "Prescribed Poets",
        "subtopics": [
          {
            "id": "english-11-0",
            "name": "Elizabeth Bishop"
          },
          {
            "id": "english-11-1",
            "name": "Eavan Boland"
          },
          {
            "id": "english-11-2",
            "name": "Emily Dickinson"
          },
          {
            "id": "english-11-3",
            "name": "John Donne"
          },
          {
            "id": "english-11-4",
            "name": "Paul Durcan"
          },
          {
            "id": "english-11-5",
            "name": "T.S. Eliot"
          },
          {
            "id": "english-11-6",
            "name": "Robert Frost"
          },
          {
            "id": "english-11-7",
            "name": "Thomas Hardy"
          },
          {
            "id": "english-11-8",
            "name": "Seamus Heaney"
          },
          {
            "id": "english-11-9",
            "name": "Gerard Manley Hopkins"
          },
          {
            "id": "english-11-10",
            "name": "Patrick Kavanagh"
          },
          {
            "id": "english-11-11",
            "name": "John Keats"
          },
          {
            "id": "english-11-12",
            "name": "Brendan Kennelly"
          },
          {
            "id": "english-11-13",
            "name": "Philip Larkin"
          },
          {
            "id": "english-11-14",
            "name": "D.H. Lawrence"
          },
          {
            "id": "english-11-15",
            "name": "Derek Mahon"
          },
          {
            "id": "english-11-16",
            "name": "Paula Meehan"
          },
          {
            "id": "english-11-17",
            "name": "John Montague"
          },
          {
            "id": "english-11-18",
            "name": "Eiléan Ní Chuilleanáin"
          },
          {
            "id": "english-11-19",
            "name": "Sylvia Plath"
          },
          {
            "id": "english-11-20",
            "name": "Adrienne Rich"
          },
          {
            "id": "english-11-21",
            "name": "Tracy K. Smith"
          },
          {
            "id": "english-11-22",
            "name": "William Wordsworth"
          },
          {
            "id": "english-11-23",
            "name": "W.B. Yeats"
          },
          {
            "id": "english-11-24",
            "name": "Fleur Adcock"
          },
          {
            "id": "english-11-25",
            "name": "Gwendolyn Brooks"
          },
          {
            "id": "english-11-26",
            "name": "Elizabeth Barrett Browning"
          },
          {
            "id": "english-11-27",
            "name": "Colette Bryce"
          },
          {
            "id": "english-11-28",
            "name": "Kate Clanchy"
          },
          {
            "id": "english-11-29",
            "name": "Rita Dove"
          },
          {
            "id": "english-11-30",
            "name": "Carol Ann Duffy"
          },
          {
            "id": "english-11-31",
            "name": "Linda France"
          },
          {
            "id": "english-11-32",
            "name": "Alison Joseph"
          },
          {
            "id": "english-11-33",
            "name": "Sinéad Morrissey"
          },
          {
            "id": "english-11-34",
            "name": "Paul Muldoon"
          },
          {
            "id": "english-11-35",
            "name": "Naomi Shihab Nye"
          },
          {
            "id": "english-11-36",
            "name": "Mary Oliver"
          },
          {
            "id": "english-11-37",
            "name": "Felicia Olusanya (FeliSpeaks)"
          },
          {
            "id": "english-11-38",
            "name": "Edgar Allan Poe"
          },
          {
            "id": "english-11-39",
            "name": "Edwin Arlington Robinson"
          },
          {
            "id": "english-11-40",
            "name": "Tim Seibles"
          },
          {
            "id": "english-11-41",
            "name": "William Shakespeare (Sonnets)"
          },
          {
            "id": "english-11-42",
            "name": "Percy Bysshe Shelley"
          },
          {
            "id": "english-11-43",
            "name": "Penelope Shuttle"
          },
          {
            "id": "english-11-44",
            "name": "Jessica Traynor"
          },
          {
            "id": "english-11-45",
            "name": "William Carlos Williams"
          },
          {
            "id": "english-11-46",
            "name": "James Wright"
          },
          {
            "id": "english-11-47",
            "name": "Benjamin Zephaniah"
          }
        ]
      },
      {
        "id": "english-12",
        "name": "Prescribed Texts (Single Text & Comparative)",
        "subtopics": [
          {
            "id": "english-12-0",
            "name": "Hamlet (Shakespeare)"
          },
          {
            "id": "english-12-1",
            "name": "King Lear (Shakespeare)"
          },
          {
            "id": "english-12-2",
            "name": "Macbeth (Shakespeare)"
          },
          {
            "id": "english-12-3",
            "name": "Othello (Shakespeare)"
          },
          {
            "id": "english-12-4",
            "name": "The Tempest (Shakespeare)"
          },
          {
            "id": "english-12-5",
            "name": "1984 (George Orwell)"
          },
          {
            "id": "english-12-6",
            "name": "A Doll's House (Henrik Ibsen)"
          },
          {
            "id": "english-12-7",
            "name": "A Raisin in the Sun (Lorraine Hansberry)"
          },
          {
            "id": "english-12-8",
            "name": "All the Light We Cannot See (Anthony Doerr)"
          },
          {
            "id": "english-12-9",
            "name": "By the Bog of Cats (Marina Carr)"
          },
          {
            "id": "english-12-10",
            "name": "Days Without End (Sebastian Barry)"
          },
          {
            "id": "english-12-11",
            "name": "Dracula (Bram Stoker)"
          },
          {
            "id": "english-12-12",
            "name": "Frankenstein (Mary Shelley)"
          },
          {
            "id": "english-12-13",
            "name": "Girl on an Altar (Marina Carr)"
          },
          {
            "id": "english-12-14",
            "name": "Hamnet (Maggie O'Farrell)"
          },
          {
            "id": "english-12-15",
            "name": "Persuasion (Jane Austen)"
          },
          {
            "id": "english-12-16",
            "name": "Philadelphia, Here I Come! (Brian Friel)"
          },
          {
            "id": "english-12-17",
            "name": "Pride and Prejudice (Jane Austen)"
          },
          {
            "id": "english-12-18",
            "name": "Room (Emma Donoghue)"
          },
          {
            "id": "english-12-19",
            "name": "Sive (John B. Keane)"
          },
          {
            "id": "english-12-20",
            "name": "The Cove (Ron Rash)"
          },
          {
            "id": "english-12-21",
            "name": "The Crucible (Arthur Miller)"
          },
          {
            "id": "english-12-22",
            "name": "The Great Gatsby (F. Scott Fitzgerald)"
          },
          {
            "id": "english-12-23",
            "name": "The Handmaid's Tale (Margaret Atwood)"
          },
          {
            "id": "english-12-24",
            "name": "The Lauras (Sara Taylor)"
          },
          {
            "id": "english-12-25",
            "name": "The Picture of Dorian Gray (Oscar Wilde)"
          },
          {
            "id": "english-12-26",
            "name": "The Playboy of the Western World (J.M. Synge)"
          },
          {
            "id": "english-12-27",
            "name": "The Spinning Heart (Donal Ryan)"
          },
          {
            "id": "english-12-28",
            "name": "The Tenant of Wildfell Hall (Anne Brontë)"
          },
          {
            "id": "english-12-29",
            "name": "The Underground Railroad (Colson Whitehead)"
          },
          {
            "id": "english-12-30",
            "name": "Wuthering Heights (Emily Brontë)"
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
            "name": "Meeting People & Social Relations"
          },
          {
            "id": "french-0-1",
            "name": "Making Plans & Future Action"
          },
          {
            "id": "french-0-2",
            "name": "Climate & Weather"
          },
          {
            "id": "french-0-3",
            "name": "Travel & Transport"
          },
          {
            "id": "french-0-4",
            "name": "Buying Goods & Services"
          },
          {
            "id": "french-0-5",
            "name": "Dealing With Emergencies"
          },
          {
            "id": "french-0-6",
            "name": "Persuading and Influencing Others"
          },
          {
            "id": "french-0-7",
            "name": "Expressing Feelings & Attitudes"
          },
          {
            "id": "french-0-8",
            "name": "Managing a Conversation"
          },
          {
            "id": "french-0-9",
            "name": "Engaging in Discussion"
          },
          {
            "id": "french-0-10",
            "name": "Passing On Messages"
          }
        ]
      },
      {
        "id": "french-1",
        "name": "Language Awareness",
        "subtopics": [
          {
            "id": "french-1-0",
            "name": "Learning From Target Language Material"
          },
          {
            "id": "french-1-1",
            "name": "Exploring Meaning"
          },
          {
            "id": "french-1-2",
            "name": "Relating Language to Attitude"
          },
          {
            "id": "french-1-3",
            "name": "Reflecting On Your Own Language Learning"
          },
          {
            "id": "french-1-4",
            "name": "Using Reference Materials"
          },
          {
            "id": "french-1-5",
            "name": "Grammar and Sentence Structure in Context"
          }
        ]
      },
      {
        "id": "french-2",
        "name": "Cultural Awareness",
        "subtopics": [
          {
            "id": "french-2-0",
            "name": "Present-Day Target Culture"
          },
          {
            "id": "french-2-1",
            "name": "Reading Modern Literary Texts"
          },
          {
            "id": "french-2-2",
            "name": "Everyday Life in the Community"
          },
          {
            "id": "french-2-3",
            "name": "Relations With Ireland"
          },
          {
            "id": "french-2-4",
            "name": "Issues Across Cultures"
          },
          {
            "id": "french-2-5",
            "name": "Francophone World Beyond France"
          }
        ]
      },
      {
        "id": "french-3",
        "name": "Aural (Listening Comprehension)",
        "subtopics": [
          {
            "id": "french-3-0",
            "name": "Aural — Conversation"
          },
          {
            "id": "french-3-1",
            "name": "Aural — Interview"
          },
          {
            "id": "french-3-2",
            "name": "Aural — News Pieces"
          }
        ]
      },
      {
        "id": "french-4",
        "name": "Oral Exam",
        "subtopics": [
          {
            "id": "french-4-0",
            "name": "Oral — General Conversation"
          },
          {
            "id": "french-4-1",
            "name": "Oral — Document (Optional)"
          }
        ]
      },
      {
        "id": "french-5",
        "name": "Reading Comprehension",
        "subtopics": [
          {
            "id": "french-5-0",
            "name": "Journalistic Comprehension (Newspaper / Magazine)"
          },
          {
            "id": "french-5-1",
            "name": "Literary Comprehension (Novel / Book Extract)"
          },
          {
            "id": "french-5-2",
            "name": "Interview-Format Comprehension (OL)"
          },
          {
            "id": "french-5-3",
            "name": "Website & Other Extract Comprehension (OL)"
          }
        ]
      },
      {
        "id": "french-6",
        "name": "Written Production — Tasks",
        "subtopics": [
          {
            "id": "french-6-0",
            "name": "Write a Diary Entry"
          },
          {
            "id": "french-6-1",
            "name": "Write a Letter (Formal / Informal)"
          },
          {
            "id": "french-6-2",
            "name": "Write a Note / Message"
          },
          {
            "id": "french-6-3",
            "name": "Write an Email"
          },
          {
            "id": "french-6-4",
            "name": "Write a Postcard (OL)"
          },
          {
            "id": "french-6-5",
            "name": "Fill in a Form (OL)"
          },
          {
            "id": "french-6-6",
            "name": "Cloze Test / Fill in the Gaps (OL)"
          },
          {
            "id": "french-6-7",
            "name": "Written Production — Narrative (récit)"
          }
        ]
      },
      {
        "id": "french-7",
        "name": "Opinion / Reaction Writing — Themes",
        "subtopics": [
          {
            "id": "french-7-0",
            "name": "Animals, Nature & the Environment"
          },
          {
            "id": "french-7-1",
            "name": "Education & School Life"
          },
          {
            "id": "french-7-2",
            "name": "Health & Lifestyle"
          },
          {
            "id": "french-7-3",
            "name": "Ireland, Travel, Tourism & Culture"
          },
          {
            "id": "french-7-4",
            "name": "Politics, Social Issues & Equality"
          },
          {
            "id": "french-7-5",
            "name": "Sport"
          },
          {
            "id": "french-7-6",
            "name": "Technology & Media"
          },
          {
            "id": "french-7-7",
            "name": "Youth, Teenagers & Family"
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
            "name": "Meeting People & Social Relations"
          },
          {
            "id": "german-0-1",
            "name": "Making Plans & Future Action"
          },
          {
            "id": "german-0-2",
            "name": "Climate & Weather"
          },
          {
            "id": "german-0-3",
            "name": "Travel & Transport"
          },
          {
            "id": "german-0-4",
            "name": "Buying Goods & Services"
          },
          {
            "id": "german-0-5",
            "name": "Dealing With Emergencies"
          },
          {
            "id": "german-0-6",
            "name": "Encouraging or Impeding Action"
          },
          {
            "id": "german-0-7",
            "name": "Feelings & Attitudes"
          },
          {
            "id": "german-0-8",
            "name": "Managing a Conversation"
          },
          {
            "id": "german-0-9",
            "name": "Engaging in Discussion"
          },
          {
            "id": "german-0-10",
            "name": "Passing on Messages"
          }
        ]
      },
      {
        "id": "german-1",
        "name": "Language Awareness",
        "subtopics": [
          {
            "id": "german-1-0",
            "name": "Learning From Target Language Material"
          },
          {
            "id": "german-1-1",
            "name": "Exploring Meaning"
          },
          {
            "id": "german-1-2",
            "name": "Relating Language to Attitude"
          },
          {
            "id": "german-1-3",
            "name": "Writing About Your Experience"
          },
          {
            "id": "german-1-4",
            "name": "Consulting Reference Materials"
          }
        ]
      },
      {
        "id": "german-2",
        "name": "Cultural Awareness",
        "subtopics": [
          {
            "id": "german-2-0",
            "name": "Present-Day Culture"
          },
          {
            "id": "german-2-1",
            "name": "Modern Literary Texts (Kurzgeschichten & Poems)"
          },
          {
            "id": "german-2-2",
            "name": "Everyday Life in the Community"
          },
          {
            "id": "german-2-3",
            "name": "Relations With Ireland"
          },
          {
            "id": "german-2-4",
            "name": "Issues Beyond Cultural Divisions"
          }
        ]
      },
      {
        "id": "german-3",
        "name": "Assessment (Four Skills)",
        "subtopics": [
          {
            "id": "german-3-0",
            "name": "Oral Exam (Mündliche Prüfung)"
          },
          {
            "id": "german-3-1",
            "name": "Listening Comprehension (Hörverständnis)"
          },
          {
            "id": "german-3-2",
            "name": "Reading Comprehension (Leseverständnis)"
          },
          {
            "id": "german-3-3",
            "name": "Written Production (Schriftliche Produktion & Äußerung zum Thema)"
          },
          {
            "id": "german-3-4",
            "name": "Applied Grammar (Angewandte Grammatik)"
          }
        ]
      },
      {
        "id": "german-4",
        "name": "Aural (Hörverständnis) — Task Types",
        "subtopics": [
          {
            "id": "german-4-0",
            "name": "Aural — Interview"
          },
          {
            "id": "german-4-1",
            "name": "Aural — Phone Call"
          },
          {
            "id": "german-4-2",
            "name": "Aural — Dialogue"
          },
          {
            "id": "german-4-3",
            "name": "Aural — News Pieces"
          }
        ]
      },
      {
        "id": "german-5",
        "name": "Oral Exam — Published Materials",
        "subtopics": [
          {
            "id": "german-5-0",
            "name": "Oral — General Conversation"
          },
          {
            "id": "german-5-1",
            "name": "Picture Story 1 — Handy-Mobbing"
          },
          {
            "id": "german-5-2",
            "name": "Picture Story 2 — Chancen durch Deutsch"
          },
          {
            "id": "german-5-3",
            "name": "Picture Story 3 — Die Abi-Tour"
          },
          {
            "id": "german-5-4",
            "name": "Picture Story 4 — Die Geburtstagsüberraschung"
          },
          {
            "id": "german-5-5",
            "name": "Picture Story 5 — Mehr Windkraft – ja oder nein?"
          },
          {
            "id": "german-5-6",
            "name": "Role Play 1 — Hund verloren"
          },
          {
            "id": "german-5-7",
            "name": "Role Play 2 — Anruf bei der Redaktion"
          },
          {
            "id": "german-5-8",
            "name": "Role Play 3 — Interview fürs Fernsehen"
          },
          {
            "id": "german-5-9",
            "name": "Role Play 4 — Einladung zum Festival in Irland"
          },
          {
            "id": "german-5-10",
            "name": "Role Play 5 — Problem mit Touristen"
          }
        ]
      },
      {
        "id": "german-6",
        "name": "Reading Comprehension — Task Types",
        "subtopics": [
          {
            "id": "german-6-0",
            "name": "Comprehension — Magazine / Newspaper Text"
          },
          {
            "id": "german-6-1",
            "name": "Comprehension — Novel / Short Story"
          }
        ]
      },
      {
        "id": "german-7",
        "name": "Written Production — Task Types",
        "subtopics": [
          {
            "id": "german-7-0",
            "name": "Äußerung zum Thema (Write on a Theme)"
          },
          {
            "id": "german-7-1",
            "name": "Schriftliche Produktion — Picture-Based"
          },
          {
            "id": "german-7-2",
            "name": "Schriftliche Produktion — Letter"
          },
          {
            "id": "german-7-3",
            "name": "Write a Blog (OL)"
          },
          {
            "id": "german-7-4",
            "name": "Write a Story (OL)"
          },
          {
            "id": "german-7-5",
            "name": "Write an Application (OL)"
          },
          {
            "id": "german-7-6",
            "name": "Write an Email (OL)"
          },
          {
            "id": "german-7-7",
            "name": "Finish the Dialogue (OL)"
          },
          {
            "id": "german-7-8",
            "name": "Write on a Topic / Give Your Opinion (OL)"
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
            "name": "Meeting People and Socialising"
          },
          {
            "id": "spanish-0-1",
            "name": "Making Plans and Future Action"
          },
          {
            "id": "spanish-0-2",
            "name": "Climate and Weather"
          },
          {
            "id": "spanish-0-3",
            "name": "Travel and Transport"
          },
          {
            "id": "spanish-0-4",
            "name": "Buying Goods and Services"
          },
          {
            "id": "spanish-0-5",
            "name": "Dealing With Emergencies"
          },
          {
            "id": "spanish-0-6",
            "name": "Transactional Language and Role-Plays"
          },
          {
            "id": "spanish-0-7",
            "name": "Expressing Feelings and Attitudes"
          },
          {
            "id": "spanish-0-8",
            "name": "Managing a Conversation"
          },
          {
            "id": "spanish-0-9",
            "name": "Engaging in Discussion"
          },
          {
            "id": "spanish-0-10",
            "name": "Passing On Messages"
          }
        ]
      },
      {
        "id": "spanish-1",
        "name": "Language Awareness",
        "subtopics": [
          {
            "id": "spanish-1-0",
            "name": "Comprehending Target-Language Material (Aural and Reading)"
          },
          {
            "id": "spanish-1-1",
            "name": "Exploring Meaning"
          },
          {
            "id": "spanish-1-2",
            "name": "Relating Language to Attitude"
          },
          {
            "id": "spanish-1-3",
            "name": "Writing About Your Experience"
          },
          {
            "id": "spanish-1-4",
            "name": "Consulting Reference Materials"
          }
        ]
      },
      {
        "id": "spanish-2",
        "name": "Cultural Awareness",
        "subtopics": [
          {
            "id": "spanish-2-0",
            "name": "Present-Day Target Culture"
          },
          {
            "id": "spanish-2-1",
            "name": "Reading Modern Literary Texts (Section A Literature Option)"
          },
          {
            "id": "spanish-2-2",
            "name": "Everyday Life in the Community"
          },
          {
            "id": "spanish-2-3",
            "name": "Relations With Ireland"
          },
          {
            "id": "spanish-2-4",
            "name": "Cross-Cultural Issues"
          },
          {
            "id": "spanish-2-5",
            "name": "Prescribed Literature and Film for Opinion Writing"
          }
        ]
      },
      {
        "id": "spanish-3",
        "name": "Aural (Listening) — Task Types",
        "subtopics": [
          {
            "id": "spanish-3-0",
            "name": "Aural — Anuncio (Announcement)"
          },
          {
            "id": "spanish-3-1",
            "name": "Aural — Descriptivo (Description)"
          },
          {
            "id": "spanish-3-2",
            "name": "Aural — Diálogo (Dialogue)"
          },
          {
            "id": "spanish-3-3",
            "name": "Aural — El Tiempo (Weather Forecast)"
          },
          {
            "id": "spanish-3-4",
            "name": "Aural — Una Noticia (News Item)"
          }
        ]
      },
      {
        "id": "spanish-4",
        "name": "Oral Exam — Published Materials",
        "subtopics": [
          {
            "id": "spanish-4-0",
            "name": "Oral — General Conversation"
          },
          {
            "id": "spanish-4-1",
            "name": "Role Play 1 — Alojamiento"
          },
          {
            "id": "spanish-4-2",
            "name": "Role Play 2 — El portátil roto"
          },
          {
            "id": "spanish-4-3",
            "name": "Role Play 3 — Una autocaravana / cámper"
          },
          {
            "id": "spanish-4-4",
            "name": "Role Play 4 — El medio ambiente"
          },
          {
            "id": "spanish-4-5",
            "name": "Role Play 5 — Avería de coche"
          }
        ]
      },
      {
        "id": "spanish-5",
        "name": "Reading Comprehension — Task Types",
        "subtopics": [
          {
            "id": "spanish-5-0",
            "name": "Journalistic Text Comprehension"
          },
          {
            "id": "spanish-5-1",
            "name": "Short Comprehensions"
          },
          {
            "id": "spanish-5-2",
            "name": "Comprehension (OL)"
          }
        ]
      },
      {
        "id": "spanish-6",
        "name": "Written Production — Task Types",
        "subtopics": [
          {
            "id": "spanish-6-0",
            "name": "Opinion Essay (HL)"
          },
          {
            "id": "spanish-6-1",
            "name": "Write a Dialogue (HL)"
          },
          {
            "id": "spanish-6-2",
            "name": "Write a Letter / Email"
          },
          {
            "id": "spanish-6-3",
            "name": "Write a Diary Entry"
          },
          {
            "id": "spanish-6-4",
            "name": "Write a Note (OL)"
          }
        ]
      },
      {
        "id": "spanish-7",
        "name": "Prescribed Literature",
        "subtopics": [
          {
            "id": "spanish-7-0",
            "name": "El medallón perdido (Ana Alcolea)"
          },
          {
            "id": "spanish-7-1",
            "name": "Relato de un náufrago (Gabriel García Márquez)"
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
        "name": "Communicative Proficiency (Speaking, Listening & Writing)",
        "subtopics": [
          {
            "id": "italian-0-0",
            "name": "Meeting People & Social Relations"
          },
          {
            "id": "italian-0-1",
            "name": "Making Plans, Arrangements & Future Action"
          },
          {
            "id": "italian-0-2",
            "name": "Climate & Weather"
          },
          {
            "id": "italian-0-3",
            "name": "Travel & Transport"
          },
          {
            "id": "italian-0-4",
            "name": "Buying Goods & Services"
          },
          {
            "id": "italian-0-5",
            "name": "Dealing With Emergencies"
          },
          {
            "id": "italian-0-6",
            "name": "Encouraging or Impeding Action"
          },
          {
            "id": "italian-0-7",
            "name": "Expressing Feelings & Attitudes"
          },
          {
            "id": "italian-0-8",
            "name": "Managing a Conversation"
          },
          {
            "id": "italian-0-9",
            "name": "Engaging in Discussion"
          },
          {
            "id": "italian-0-10",
            "name": "Passing On Messages"
          }
        ]
      },
      {
        "id": "italian-1",
        "name": "Language Awareness",
        "subtopics": [
          {
            "id": "italian-1-0",
            "name": "Learning From Target Language Material"
          },
          {
            "id": "italian-1-1",
            "name": "Exploring Meaning"
          },
          {
            "id": "italian-1-2",
            "name": "Relating Language to Attitude"
          },
          {
            "id": "italian-1-3",
            "name": "Writing About Your Experience"
          },
          {
            "id": "italian-1-4",
            "name": "Consulting Reference Materials"
          },
          {
            "id": "italian-1-5",
            "name": "Grammar Accuracy & Self-Correction"
          }
        ]
      },
      {
        "id": "italian-2",
        "name": "Cultural Awareness",
        "subtopics": [
          {
            "id": "italian-2-0",
            "name": "Present-Day Target Culture"
          },
          {
            "id": "italian-2-1",
            "name": "Reading Modern Literary Texts (incl. studied text e.g. Marcovaldo)"
          },
          {
            "id": "italian-2-2",
            "name": "Everyday Life in the Community"
          },
          {
            "id": "italian-2-3",
            "name": "Relations With Ireland"
          },
          {
            "id": "italian-2-4",
            "name": "Issues Beyond Cultural Divisions"
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
            "name": "Meeting People & Social Relations"
          },
          {
            "id": "russian-0-1",
            "name": "Family & Home"
          },
          {
            "id": "russian-0-2",
            "name": "Your Region & Locality"
          },
          {
            "id": "russian-0-3",
            "name": "Learning"
          },
          {
            "id": "russian-0-4",
            "name": "Work"
          },
          {
            "id": "russian-0-5",
            "name": "Leisure Pursuits"
          },
          {
            "id": "russian-0-6",
            "name": "Plans & Future Action"
          },
          {
            "id": "russian-0-7",
            "name": "Events in People's Lives"
          },
          {
            "id": "russian-0-8",
            "name": "Travel & Transport"
          },
          {
            "id": "russian-0-9",
            "name": "Buying Goods & Services"
          },
          {
            "id": "russian-0-10",
            "name": "Facilitating, Encouraging or Impeding Action"
          },
          {
            "id": "russian-0-11",
            "name": "Feelings & Attitudes"
          },
          {
            "id": "russian-0-12",
            "name": "Managing a Conversation"
          },
          {
            "id": "russian-0-13",
            "name": "Engaging in Discussion"
          },
          {
            "id": "russian-0-14",
            "name": "Passing on Messages"
          }
        ]
      },
      {
        "id": "russian-1",
        "name": "Language Awareness",
        "subtopics": [
          {
            "id": "russian-1-0",
            "name": "Learning From Target-Language Material"
          },
          {
            "id": "russian-1-1",
            "name": "Exploring Meaning"
          },
          {
            "id": "russian-1-2",
            "name": "Relating Language to Attitude"
          },
          {
            "id": "russian-1-3",
            "name": "Writing About Your Experience of the Language"
          },
          {
            "id": "russian-1-4",
            "name": "Consulting Reference Materials"
          }
        ]
      },
      {
        "id": "russian-2",
        "name": "Cultural Awareness",
        "subtopics": [
          {
            "id": "russian-2-0",
            "name": "Present-Day Target Culture"
          },
          {
            "id": "russian-2-1",
            "name": "Modern Literary Texts"
          },
          {
            "id": "russian-2-2",
            "name": "Everyday Life in the Community"
          },
          {
            "id": "russian-2-3",
            "name": "Relations With Ireland"
          },
          {
            "id": "russian-2-4",
            "name": "Issues That Transcend Cultural Divisions"
          },
          {
            "id": "russian-2-5",
            "name": "Aspects of Russian Culture"
          },
          {
            "id": "russian-2-6",
            "name": "Aspects of Russian History"
          },
          {
            "id": "russian-2-7",
            "name": "A Society in Transition"
          },
          {
            "id": "russian-2-8",
            "name": "Russia on the World Stage"
          },
          {
            "id": "russian-2-9",
            "name": "Challenges of a Multi-Cultural State"
          },
          {
            "id": "russian-2-10",
            "name": "The Russian Landscape"
          },
          {
            "id": "russian-2-11",
            "name": "Contemporary Russian Life"
          },
          {
            "id": "russian-2-12",
            "name": "Russian Traditions & Customs"
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
            "name": "Meeting People and Social Relations"
          },
          {
            "id": "japanese-0-1",
            "name": "Managing a Conversation"
          },
          {
            "id": "japanese-0-2",
            "name": "Making Plans and Future Action"
          },
          {
            "id": "japanese-0-3",
            "name": "Climate and Weather"
          },
          {
            "id": "japanese-0-4",
            "name": "Travel and Transport"
          },
          {
            "id": "japanese-0-5",
            "name": "Buying Goods and Services"
          },
          {
            "id": "japanese-0-6",
            "name": "Dealing with Emergencies"
          },
          {
            "id": "japanese-0-7",
            "name": "Requesting and Influencing Action"
          },
          {
            "id": "japanese-0-8",
            "name": "Feelings and Attitudes"
          },
          {
            "id": "japanese-0-9",
            "name": "Engaging in Discussion"
          },
          {
            "id": "japanese-0-10",
            "name": "Passing on Messages"
          }
        ]
      },
      {
        "id": "japanese-1",
        "name": "Language Awareness",
        "subtopics": [
          {
            "id": "japanese-1-0",
            "name": "Learning from Target Language Material"
          },
          {
            "id": "japanese-1-1",
            "name": "Exploring Meaning"
          },
          {
            "id": "japanese-1-2",
            "name": "Relating Language to Attitude and Register"
          },
          {
            "id": "japanese-1-3",
            "name": "Your Experience of the Language"
          },
          {
            "id": "japanese-1-4",
            "name": "Consulting Reference Materials"
          }
        ]
      },
      {
        "id": "japanese-2",
        "name": "Cultural Awareness",
        "subtopics": [
          {
            "id": "japanese-2-0",
            "name": "Present-Day Japanese Culture"
          },
          {
            "id": "japanese-2-1",
            "name": "Reading Modern Texts"
          },
          {
            "id": "japanese-2-2",
            "name": "Everyday Life in the Community"
          },
          {
            "id": "japanese-2-3",
            "name": "Relations with Ireland"
          },
          {
            "id": "japanese-2-4",
            "name": "Cross-Cultural Issues"
          }
        ]
      },
      {
        "id": "japanese-3",
        "name": "Writing Systems & Required Kanji",
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
            "name": "Kanji (Required List)"
          },
          {
            "id": "japanese-3-3",
            "name": "Linguistic Skills: Structures & Grammar"
          }
        ]
      },
      {
        "id": "japanese-4",
        "name": "Assessment: The Four Skills",
        "subtopics": [
          {
            "id": "japanese-4-0",
            "name": "Speaking / Oral Examination"
          },
          {
            "id": "japanese-4-1",
            "name": "Listening Comprehension (Aural)"
          },
          {
            "id": "japanese-4-2",
            "name": "Reading Comprehension"
          },
          {
            "id": "japanese-4-3",
            "name": "Written Production"
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
            "name": "Reception: Follow Classroom Interactions (CLC1)"
          },
          {
            "id": "mandarin-chinese-0-2",
            "name": "Reception: Explore Authentic Texts (CLC2)"
          },
          {
            "id": "mandarin-chinese-0-3",
            "name": "Reception: Gather Specific Information (CLC3)"
          },
          {
            "id": "mandarin-chinese-0-4",
            "name": "Reception: Understand Lexical Range (CLC4)"
          },
          {
            "id": "mandarin-chinese-0-5",
            "name": "Reception: Identify Everyday Information (CLC5)"
          },
          {
            "id": "mandarin-chinese-0-6",
            "name": "Reception: Understand Descriptions (CLC6)"
          },
          {
            "id": "mandarin-chinese-0-7",
            "name": "Interaction"
          },
          {
            "id": "mandarin-chinese-0-8",
            "name": "Interaction: Simple Transactions (CLC7)"
          },
          {
            "id": "mandarin-chinese-0-9",
            "name": "Interaction: Accounts of Events (CLC8)"
          },
          {
            "id": "mandarin-chinese-0-10",
            "name": "Interaction: Manage Conversations (CLC9)"
          },
          {
            "id": "mandarin-chinese-0-11",
            "name": "Interaction: Ask & Answer Questions (CLC10)"
          },
          {
            "id": "mandarin-chinese-0-12",
            "name": "Production"
          },
          {
            "id": "mandarin-chinese-0-13",
            "name": "Production: Pronunciation & Tones (CLC11)"
          },
          {
            "id": "mandarin-chinese-0-14",
            "name": "Production: Write with Characters (CLC12)"
          },
          {
            "id": "mandarin-chinese-0-15",
            "name": "Production: Use Basic Patterns (CLC13)"
          },
          {
            "id": "mandarin-chinese-0-16",
            "name": "Production: Describe Events (CLC14)"
          },
          {
            "id": "mandarin-chinese-0-17",
            "name": "Production: Express Feelings (CLC15)"
          },
          {
            "id": "mandarin-chinese-0-18",
            "name": "Production: Create Texts (CLC16)"
          },
          {
            "id": "mandarin-chinese-0-19",
            "name": "Mediation"
          },
          {
            "id": "mandarin-chinese-0-20",
            "name": "Mediation: Convey Main Points (CLC17)"
          },
          {
            "id": "mandarin-chinese-0-21",
            "name": "Mediation: Collaborate on Tasks (CLC18)"
          },
          {
            "id": "mandarin-chinese-0-22",
            "name": "Mediation: Convey Simple Information (CLC19)"
          },
          {
            "id": "mandarin-chinese-0-23",
            "name": "Mediation: Ask for Clarification (CLC20)"
          },
          {
            "id": "mandarin-chinese-0-24",
            "name": "Mediation: Show Empathy & Interest (CLC21)"
          },
          {
            "id": "mandarin-chinese-0-25",
            "name": "Mediation: Respond to Creative Texts (CLC22)"
          }
        ]
      },
      {
        "id": "mandarin-chinese-1",
        "name": "Plurilingual & Pluricultural Competence",
        "subtopics": [
          {
            "id": "mandarin-chinese-1-0",
            "name": "Plurilingual Competence"
          },
          {
            "id": "mandarin-chinese-1-1",
            "name": "Plurilingual: Decode Unfamiliar Characters (PPC1)"
          },
          {
            "id": "mandarin-chinese-1-2",
            "name": "Plurilingual: Recognise Patterns (PPC2)"
          },
          {
            "id": "mandarin-chinese-1-3",
            "name": "Plurilingual: Compensation Strategies (PPC3)"
          },
          {
            "id": "mandarin-chinese-1-4",
            "name": "Plurilingual: Develop Learning Strategies (PPC4)"
          },
          {
            "id": "mandarin-chinese-1-5",
            "name": "Plurilingual: Exploit Repertoire (PPC5)"
          },
          {
            "id": "mandarin-chinese-1-6",
            "name": "Plurilingual: Compare Across Languages (PPC6)"
          },
          {
            "id": "mandarin-chinese-1-7",
            "name": "Plurilingual: Contrast Known Languages (PPC7)"
          },
          {
            "id": "mandarin-chinese-1-8",
            "name": "Plurilingual: Reflect on Learning (PPC8)"
          },
          {
            "id": "mandarin-chinese-1-9",
            "name": "Pluricultural Competence"
          },
          {
            "id": "mandarin-chinese-1-10",
            "name": "Pluricultural: Explore Popular Culture (PPC9)"
          },
          {
            "id": "mandarin-chinese-1-11",
            "name": "Pluricultural: Research Society (PPC10)"
          },
          {
            "id": "mandarin-chinese-1-12",
            "name": "Pluricultural: Research Cultural Heritage (PPC11)"
          },
          {
            "id": "mandarin-chinese-1-13",
            "name": "Pluricultural: Interpret Everyday Living (PPC12)"
          },
          {
            "id": "mandarin-chinese-1-14",
            "name": "Pluricultural: Awareness of Customs (PPC13)"
          },
          {
            "id": "mandarin-chinese-1-15",
            "name": "Pluricultural: Explain Cultural Features (PPC14)"
          },
          {
            "id": "mandarin-chinese-1-16",
            "name": "Pluricultural: Use Social Conventions (PPC15)"
          },
          {
            "id": "mandarin-chinese-1-17",
            "name": "Pluricultural: Compare Cultures (PPC16)"
          },
          {
            "id": "mandarin-chinese-1-18",
            "name": "Pluricultural: Communicate Across Cultures (PPC17)"
          },
          {
            "id": "mandarin-chinese-1-19",
            "name": "Pluricultural: Explore Cultural Identity (PPC18)"
          }
        ]
      },
      {
        "id": "mandarin-chinese-2",
        "name": "Assessment for Certification (Oral, Aural & Written)",
        "subtopics": [
          {
            "id": "mandarin-chinese-2-0",
            "name": "Oral Examination"
          },
          {
            "id": "mandarin-chinese-2-1",
            "name": "Aural Examination"
          },
          {
            "id": "mandarin-chinese-2-2",
            "name": "Written Examination"
          },
          {
            "id": "mandarin-chinese-2-3",
            "name": "Language Portfolio (Oral Stimulus - Not Graded)"
          },
          {
            "id": "mandarin-chinese-2-4",
            "name": "Simplified Characters (Pin Yin Not Assessed)"
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
            "name": "Understanding Latin Texts"
          },
          {
            "id": "latin-0-1",
            "name": "Text Formats"
          },
          {
            "id": "latin-0-2",
            "name": "Ways of Reading"
          },
          {
            "id": "latin-0-3",
            "name": "Learning Words and Expressions"
          },
          {
            "id": "latin-0-4",
            "name": "Lexical Phenomena"
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
            "name": "Stem and Ending"
          },
          {
            "id": "latin-0-8",
            "name": "Translation"
          },
          {
            "id": "latin-0-9",
            "name": "The Translator's Role"
          },
          {
            "id": "latin-0-10",
            "name": "Evaluating Information in Texts"
          },
          {
            "id": "latin-0-11",
            "name": "Literary Techniques and Style"
          },
          {
            "id": "latin-0-12",
            "name": "Language Awareness and Analysis"
          },
          {
            "id": "latin-0-13",
            "name": "Morphology and Syntax"
          },
          {
            "id": "latin-0-14",
            "name": "Parts of Words"
          },
          {
            "id": "latin-0-15",
            "name": "Word Types"
          },
          {
            "id": "latin-0-16",
            "name": "Inflection Patterns"
          },
          {
            "id": "latin-0-17",
            "name": "Clauses and Constructions"
          },
          {
            "id": "latin-0-18",
            "name": "Spelling and Punctuation"
          },
          {
            "id": "latin-0-19",
            "name": "Logical Reasoning from Syntax"
          },
          {
            "id": "latin-0-20",
            "name": "Using Reference Tools"
          },
          {
            "id": "latin-0-21",
            "name": "Comparing Languages"
          },
          {
            "id": "latin-0-22",
            "name": "Etymology and Derivatives"
          },
          {
            "id": "latin-0-23",
            "name": "Untranslatable Concepts"
          },
          {
            "id": "latin-0-24",
            "name": "Language Variation by Genre"
          },
          {
            "id": "latin-0-25",
            "name": "Learning Strategies and Resources"
          },
          {
            "id": "latin-0-26",
            "name": "Prescribed Forms for Examination"
          },
          {
            "id": "latin-0-27",
            "name": "Unseen Comprehension and Translation (Section B technique)"
          }
        ]
      },
      {
        "id": "latin-1",
        "name": "Strand 2: Literature in Context",
        "subtopics": [
          {
            "id": "latin-1-0",
            "name": "Latin Literature"
          },
          {
            "id": "latin-1-1",
            "name": "Responding to Texts"
          },
          {
            "id": "latin-1-2",
            "name": "Characters and Relationships"
          },
          {
            "id": "latin-1-3",
            "name": "Researching Texts and Authors"
          },
          {
            "id": "latin-1-4",
            "name": "Contexts for Understanding Texts"
          },
          {
            "id": "latin-1-5",
            "name": "Close Reading"
          },
          {
            "id": "latin-1-6",
            "name": "Original vs Modern Audience"
          },
          {
            "id": "latin-1-7",
            "name": "Reception of Latin Literature"
          },
          {
            "id": "latin-1-8",
            "name": "Survival of Latin Over Time"
          },
          {
            "id": "latin-1-9",
            "name": "Roman Culture in Latin Texts"
          },
          {
            "id": "latin-1-10",
            "name": "Places, Events and People"
          },
          {
            "id": "latin-1-11",
            "name": "Roman Heritage and Daily Life"
          },
          {
            "id": "latin-1-12",
            "name": "Roman Values and Attitudes"
          },
          {
            "id": "latin-1-13",
            "name": "Discussing Roman Society"
          },
          {
            "id": "latin-1-14",
            "name": "Roman Identity and Self-Representation"
          }
        ]
      },
      {
        "id": "latin-2",
        "name": "Capstone Text and Assessment",
        "subtopics": [
          {
            "id": "latin-2-0",
            "name": "Capstone Text: Virgil's Aeneid Books 1 & 4 (Dido and Aeneas)"
          },
          {
            "id": "latin-2-1",
            "name": "Capstone Text Context"
          },
          {
            "id": "latin-2-2",
            "name": "Written Examination (60%): Section A Capstone 100m + Section B Unseen 200m"
          },
          {
            "id": "latin-2-3",
            "name": "Research Study (40%): ~20-hour written report on a common brief"
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
            "name": "Understanding Ancient Greek Texts (element)"
          },
          {
            "id": "ancient-greek-0-1",
            "name": "1.1 Explore a Range of Greek Texts & Genres"
          },
          {
            "id": "ancient-greek-0-2",
            "name": "1.2 Recognise Vocabulary in Context"
          },
          {
            "id": "ancient-greek-0-3",
            "name": "1.3 Pronounce Greek Accurately"
          },
          {
            "id": "ancient-greek-0-4",
            "name": "1.4 Collaborate to Understand Greek"
          },
          {
            "id": "ancient-greek-0-5",
            "name": "1.5 Vocabulary & Grammar Rules"
          },
          {
            "id": "ancient-greek-0-6",
            "name": "1.6 Translate Greek Passages"
          },
          {
            "id": "ancient-greek-0-7",
            "name": "1.7 Evaluate Information in Texts"
          },
          {
            "id": "ancient-greek-0-8",
            "name": "1.8 Content & Structure of Texts"
          },
          {
            "id": "ancient-greek-0-9",
            "name": "1.9 Evaluate Translations"
          },
          {
            "id": "ancient-greek-0-10",
            "name": "1.10 Distinctive Features of Texts"
          },
          {
            "id": "ancient-greek-0-11",
            "name": "Developing Language Awareness & Analytical Skills (element)"
          },
          {
            "id": "ancient-greek-0-12",
            "name": "1.11 Make Sense of Unfamiliar Words"
          },
          {
            "id": "ancient-greek-0-13",
            "name": "1.12 Linguistic Patterns & Structures"
          },
          {
            "id": "ancient-greek-0-14",
            "name": "1.13 Explain Your Interpretation"
          },
          {
            "id": "ancient-greek-0-15",
            "name": "1.14 Use Language Resources"
          },
          {
            "id": "ancient-greek-0-16",
            "name": "1.15 Assess Own Learning"
          },
          {
            "id": "ancient-greek-0-17",
            "name": "1.16 Concepts Across Languages"
          },
          {
            "id": "ancient-greek-0-18",
            "name": "1.17 Compare Known Languages"
          },
          {
            "id": "ancient-greek-0-19",
            "name": "1.18 Etymology from Greek"
          },
          {
            "id": "ancient-greek-0-20",
            "name": "1.19 Language Varies with Genre"
          }
        ]
      },
      {
        "id": "ancient-greek-1",
        "name": "Strand 2: Literature in Context",
        "subtopics": [
          {
            "id": "ancient-greek-1-0",
            "name": "Ancient Greek Literature (element)"
          },
          {
            "id": "ancient-greek-1-1",
            "name": "2.1 Respond to Greek Texts"
          },
          {
            "id": "ancient-greek-1-2",
            "name": "2.2 Research Texts & Authors"
          },
          {
            "id": "ancient-greek-1-3",
            "name": "2.3 Explain Texts in Context"
          },
          {
            "id": "ancient-greek-1-4",
            "name": "2.4 Close Reading"
          },
          {
            "id": "ancient-greek-1-5",
            "name": "2.5 Significance for the Audience"
          },
          {
            "id": "ancient-greek-1-6",
            "name": "2.6 Reception of Greek Texts"
          },
          {
            "id": "ancient-greek-1-7",
            "name": "2.7 Continued Importance of Greek (Literature, Learning, Science, Religion)"
          },
          {
            "id": "ancient-greek-1-8",
            "name": "Hellenic Culture Explored Through Ancient Greek Texts (element)"
          },
          {
            "id": "ancient-greek-1-9",
            "name": "2.8 Communities Using Greek"
          },
          {
            "id": "ancient-greek-1-10",
            "name": "2.9 Cultural Heritage & Daily Life"
          },
          {
            "id": "ancient-greek-1-11",
            "name": "2.10 Greek Values & Attitudes"
          },
          {
            "id": "ancient-greek-1-12",
            "name": "2.11 Society, History & Politics"
          },
          {
            "id": "ancient-greek-1-13",
            "name": "2.12 Greek Identity & Otherness"
          }
        ]
      },
      {
        "id": "ancient-greek-2",
        "name": "Capstone Text & Prescribed Material (examined in the Written Paper)",
        "subtopics": [
          {
            "id": "ancient-greek-2-0",
            "name": "The Capstone Text"
          },
          {
            "id": "ancient-greek-2-1",
            "name": "Context of the Capstone Text"
          },
          {
            "id": "ancient-greek-2-2",
            "name": "Prescribed Grammar for Exam"
          }
        ]
      },
      {
        "id": "ancient-greek-3",
        "name": "Research Study: Text in Context (Additional Assessment Component, 40%)",
        "subtopics": [
          {
            "id": "ancient-greek-3-0",
            "name": "Investigate a Language or Text Topic"
          },
          {
            "id": "ancient-greek-3-1",
            "name": "Research & Process Information"
          },
          {
            "id": "ancient-greek-3-2",
            "name": "Synthesise & Make a Judgement"
          },
          {
            "id": "ancient-greek-3-3",
            "name": "Explore the Broader Context"
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
            "name": "Family: Old Testament Texts"
          },
          {
            "id": "hebrew-studies-0-2",
            "name": "Family: Mishnah Texts"
          },
          {
            "id": "hebrew-studies-0-3",
            "name": "Government and Monarchy"
          },
          {
            "id": "hebrew-studies-0-4",
            "name": "Government and Monarchy: Old Testament Texts"
          },
          {
            "id": "hebrew-studies-0-5",
            "name": "Government and Monarchy: Mishnah Texts"
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
            "name": "Prophetic Protest: OT Texts"
          },
          {
            "id": "hebrew-studies-1-2",
            "name": "Prophetic Protest: Mishnah Texts"
          },
          {
            "id": "hebrew-studies-1-3",
            "name": "Wisdom"
          },
          {
            "id": "hebrew-studies-1-4",
            "name": "Wisdom: Old Testament Texts"
          },
          {
            "id": "hebrew-studies-1-5",
            "name": "Wisdom: Mishnah Texts"
          },
          {
            "id": "hebrew-studies-1-6",
            "name": "Wisdom: Additional Reading"
          }
        ]
      },
      {
        "id": "hebrew-studies-2",
        "name": "Section C",
        "subtopics": [
          {
            "id": "hebrew-studies-2-0",
            "name": "Worship: Sacrifice and Prayer"
          },
          {
            "id": "hebrew-studies-2-1",
            "name": "Worship: Old Testament Texts"
          },
          {
            "id": "hebrew-studies-2-2",
            "name": "Worship: Mishnah Texts"
          },
          {
            "id": "hebrew-studies-2-3",
            "name": "Festivals and Symbols"
          },
          {
            "id": "hebrew-studies-2-4",
            "name": "Festivals and Symbols: OT Texts"
          },
          {
            "id": "hebrew-studies-2-5",
            "name": "Festivals and Symbols: Mishnah Texts"
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
            "name": "Election and Covenant: OT Texts"
          },
          {
            "id": "hebrew-studies-3-2",
            "name": "Election and Covenant: Mishnah Texts"
          },
          {
            "id": "hebrew-studies-3-3",
            "name": "Messianism"
          },
          {
            "id": "hebrew-studies-3-4",
            "name": "Messianism: Old Testament Texts"
          },
          {
            "id": "hebrew-studies-3-5",
            "name": "Messianism: Mishnah Texts"
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
        "name": "Strand 2: Plurilingual & Pluricultural",
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
        "name": "Assessment for Certification (New Spec, exam from 2027)",
        "subtopics": [
          {
            "id": "arabic-2-0",
            "name": "Oral Examination"
          },
          {
            "id": "arabic-2-1",
            "name": "Aural Examination"
          },
          {
            "id": "arabic-2-2",
            "name": "Written Exam: Reading"
          },
          {
            "id": "arabic-2-3",
            "name": "Written Exam: Writing"
          },
          {
            "id": "arabic-2-4",
            "name": "Language Portfolio"
          },
          {
            "id": "arabic-2-5",
            "name": "Written Exam: Reading and Writing Weightings (HL/OL)"
          }
        ]
      },
      {
        "id": "arabic-3",
        "name": "Interim: Reading & Directed Writing",
        "subtopics": [
          {
            "id": "arabic-3-0",
            "name": "Understanding & Conveying Information"
          },
          {
            "id": "arabic-3-1",
            "name": "Evaluating & Selecting Information"
          },
          {
            "id": "arabic-3-2",
            "name": "Scanning and Extracting Specific Information"
          },
          {
            "id": "arabic-3-3",
            "name": "Main Topics & Summarising"
          },
          {
            "id": "arabic-3-4",
            "name": "Linguistic Devices & Implicit Meaning"
          },
          {
            "id": "arabic-3-5",
            "name": "Higher Level: Inference & Analysis"
          }
        ]
      },
      {
        "id": "arabic-4",
        "name": "Interim: Continuous Writing",
        "subtopics": [
          {
            "id": "arabic-4-0",
            "name": "Articulating Experience & Ideas"
          },
          {
            "id": "arabic-4-1",
            "name": "Vocabulary, Syntax & Grammar"
          },
          {
            "id": "arabic-4-2",
            "name": "Expressing Thoughts & Opinions"
          },
          {
            "id": "arabic-4-3",
            "name": "Higher Level: Audience & Paragraphing"
          }
        ]
      },
      {
        "id": "arabic-5",
        "name": "Interim: Use of Language",
        "subtopics": [
          {
            "id": "arabic-5-0",
            "name": "Grammatical Structures"
          },
          {
            "id": "arabic-5-1",
            "name": "Paragraphing & Punctuation"
          },
          {
            "id": "arabic-5-2",
            "name": "Range of Apt Vocabulary"
          },
          {
            "id": "arabic-5-3",
            "name": "Register & Style"
          },
          {
            "id": "arabic-5-4",
            "name": "Sentence & Paragraph Construction"
          }
        ]
      },
      {
        "id": "arabic-6",
        "name": "Interim: Literature (Prescribed Texts)",
        "subtopics": [
          {
            "id": "arabic-6-0",
            "name": "Extract from the Quran"
          },
          {
            "id": "arabic-6-1",
            "name": "Classical Arabic Verse"
          },
          {
            "id": "arabic-6-2",
            "name": "Modern Arabic Prose Extract"
          },
          {
            "id": "arabic-6-3",
            "name": "Commenting on Set Texts"
          },
          {
            "id": "arabic-6-4",
            "name": "Answering Two of Three Literature Sections"
          }
        ]
      },
      {
        "id": "arabic-7",
        "name": "Interim: Reading Comprehension",
        "subtopics": [
          {
            "id": "arabic-7-0",
            "name": "Letters, Articles & Literature"
          },
          {
            "id": "arabic-7-1",
            "name": "Levels of Meaning & Style"
          }
        ]
      },
      {
        "id": "arabic-8",
        "name": "Interim: Assessment & Mark Allocation",
        "subtopics": [
          {
            "id": "arabic-8-0",
            "name": "Reading Comprehension (20%)"
          },
          {
            "id": "arabic-8-1",
            "name": "Literature (35%)"
          },
          {
            "id": "arabic-8-2",
            "name": "Usage (20%)"
          },
          {
            "id": "arabic-8-3",
            "name": "Continuous Writing (25%)"
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
        "name": "Strand 1: The World of Heroes",
        "subtopics": [
          {
            "id": "classical-studies-0-0",
            "name": "Characteristics and Types of Heroes and Leaders"
          },
          {
            "id": "classical-studies-0-1",
            "name": "Heroic Society"
          },
          {
            "id": "classical-studies-0-2",
            "name": "Heroic Narratives"
          },
          {
            "id": "classical-studies-0-3",
            "name": "Homer's Odyssey"
          },
          {
            "id": "classical-studies-0-4",
            "name": "Virgil's Aeneid (Books 1-6)"
          }
        ]
      },
      {
        "id": "classical-studies-1",
        "name": "Strand 2: Drama and Spectacle",
        "subtopics": [
          {
            "id": "classical-studies-1-0",
            "name": "Greek Tragedy"
          },
          {
            "id": "classical-studies-1-1",
            "name": "Context of Greek Tragedy"
          },
          {
            "id": "classical-studies-1-2",
            "name": "Prescribed Tragedy (rotating pairing)"
          },
          {
            "id": "classical-studies-1-3",
            "name": "The Colosseum, the Circus Maximus and Roman Spectacle"
          }
        ]
      },
      {
        "id": "classical-studies-2",
        "name": "Strand 3: Power and Identity",
        "subtopics": [
          {
            "id": "classical-studies-2-0",
            "name": "The Time of Alexander or Caesar"
          },
          {
            "id": "classical-studies-2-1",
            "name": "Political and Military Exploits of Alexander or Caesar"
          },
          {
            "id": "classical-studies-2-2",
            "name": "Characterisation of Alexander or Caesar"
          },
          {
            "id": "classical-studies-2-3",
            "name": "Attitudes Towards Foreign Peoples"
          },
          {
            "id": "classical-studies-2-4",
            "name": "Prescribed Literary Sources (Arrian/Plutarch or Caesar/Suetonius)"
          }
        ]
      },
      {
        "id": "classical-studies-3",
        "name": "Strand 4: Gods and Humans",
        "subtopics": [
          {
            "id": "classical-studies-3-0",
            "name": "The Greek and Roman Gods"
          },
          {
            "id": "classical-studies-3-1",
            "name": "Temples: Parthenon, Erechtheion, Pantheon and Temple of Vesta"
          },
          {
            "id": "classical-studies-3-2",
            "name": "Funerary Practices and the Afterlife"
          },
          {
            "id": "classical-studies-3-3",
            "name": "Philosophy of Mortality and Living Well (Plato's Crito, Horace's Odes/Epodes)"
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
            "name": "Reception (Listening & Reading)"
          },
          {
            "id": "lithuanian-0-1",
            "name": "Interaction (Spoken & Written)"
          },
          {
            "id": "lithuanian-0-2",
            "name": "Production: Speaking & Writing"
          },
          {
            "id": "lithuanian-0-3",
            "name": "Mediation"
          },
          {
            "id": "lithuanian-0-4",
            "name": "Pronunciation, Spelling & Grammatical Accuracy"
          }
        ]
      },
      {
        "id": "lithuanian-1",
        "name": "Plurilingual & Pluricultural Competence",
        "subtopics": [
          {
            "id": "lithuanian-1-0",
            "name": "Plurilingual Competence"
          },
          {
            "id": "lithuanian-1-1",
            "name": "Pluricultural Competence"
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
            "name": "Mediation (relaying and summarising texts)"
          }
        ]
      },
      {
        "id": "polish-1",
        "name": "Plurilingual & Pluricultural Competence",
        "subtopics": [
          {
            "id": "polish-1-0",
            "name": "Plurilingual Competence"
          },
          {
            "id": "polish-1-1",
            "name": "Pluricultural Competence"
          },
          {
            "id": "polish-1-2",
            "name": "Cultural and Historical Knowledge of Poland"
          }
        ]
      },
      {
        "id": "polish-2",
        "name": "Exam Components and Language Portfolio",
        "subtopics": [
          {
            "id": "polish-2-0",
            "name": "Oral Examination (HL 30%)"
          },
          {
            "id": "polish-2-1",
            "name": "Aural Examination (HL 25%)"
          },
          {
            "id": "polish-2-2",
            "name": "Written: Reading (HL 25%)"
          },
          {
            "id": "polish-2-3",
            "name": "Written: Writing (HL 20%)"
          },
          {
            "id": "polish-2-4",
            "name": "Language Portfolio (oral stimulus, not marked)"
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
        "name": "Communicative Language Competence (Reception, Interaction, Production, Mediation)",
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
          },
          {
            "id": "portuguese-0-4",
            "name": "Language Portfolio (focus of the oral discussion)"
          }
        ]
      },
      {
        "id": "portuguese-1",
        "name": "Plurilingual & Pluricultural Competence",
        "subtopics": [
          {
            "id": "portuguese-1-0",
            "name": "Plurilingual Competence (cross-language decoding & compensation)"
          },
          {
            "id": "portuguese-1-1",
            "name": "Pluricultural Competence (Portuguese-speaking cultures & registers)"
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
        "name": "Strand 1: Statistics & Probability",
        "subtopics": [
          {
            "id": "mathematics-0-0",
            "name": "Counting"
          },
          {
            "id": "mathematics-0-1",
            "name": "Concepts of Probability"
          },
          {
            "id": "mathematics-0-2",
            "name": "Outcomes of Random Processes"
          },
          {
            "id": "mathematics-0-3",
            "name": "Statistical Reasoning"
          },
          {
            "id": "mathematics-0-4",
            "name": "Collecting & Organising Data"
          },
          {
            "id": "mathematics-0-5",
            "name": "Representing Data"
          },
          {
            "id": "mathematics-0-6",
            "name": "Analysing & Interpreting Data"
          }
        ]
      },
      {
        "id": "mathematics-1",
        "name": "Strand 2: Geometry & Trigonometry",
        "subtopics": [
          {
            "id": "mathematics-1-0",
            "name": "Synthetic Geometry"
          },
          {
            "id": "mathematics-1-1",
            "name": "Co-ordinate Geometry"
          },
          {
            "id": "mathematics-1-2",
            "name": "Trigonometry"
          },
          {
            "id": "mathematics-1-3",
            "name": "Transformation Geometry & Enlargements"
          }
        ]
      },
      {
        "id": "mathematics-2",
        "name": "Strand 3: Number",
        "subtopics": [
          {
            "id": "mathematics-2-0",
            "name": "Number Systems"
          },
          {
            "id": "mathematics-2-1",
            "name": "Indices & Logarithms"
          },
          {
            "id": "mathematics-2-2",
            "name": "Arithmetic & Applied Arithmetic"
          },
          {
            "id": "mathematics-2-3",
            "name": "Length, Area & Volume"
          },
          {
            "id": "mathematics-2-4",
            "name": "Sequences & Series"
          },
          {
            "id": "mathematics-2-5",
            "name": "Financial Maths & Applications"
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
            "name": "Solving Equations"
          },
          {
            "id": "mathematics-3-2",
            "name": "Inequalities"
          },
          {
            "id": "mathematics-3-3",
            "name": "Complex Numbers"
          },
          {
            "id": "mathematics-3-4",
            "name": "Proof by Induction"
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
        "name": "Strand 1: Mathematical Modelling",
        "subtopics": [
          {
            "id": "applied-mathematics-0-0",
            "name": "The Problem-Solving Cycle"
          },
          {
            "id": "applied-mathematics-0-1",
            "name": "Formulating Problems"
          },
          {
            "id": "applied-mathematics-0-2",
            "name": "Translating Problems into Mathematics"
          },
          {
            "id": "applied-mathematics-0-3",
            "name": "Computing Solutions"
          },
          {
            "id": "applied-mathematics-0-4",
            "name": "Evaluating Solutions"
          }
        ]
      },
      {
        "id": "applied-mathematics-1",
        "name": "Strand 2: Mathematical Modelling with Networks and Graphs",
        "subtopics": [
          {
            "id": "applied-mathematics-1-0",
            "name": "Networks and Their Associated Terminology"
          },
          {
            "id": "applied-mathematics-1-1",
            "name": "Matrices, Matrix Algebra and Adjacency"
          },
          {
            "id": "applied-mathematics-1-2",
            "name": "Minimum Spanning Trees (Kruskal and Prim)"
          },
          {
            "id": "applied-mathematics-1-3",
            "name": "Dynamic Programming and Shortest Paths (Bellman, Dijkstra)"
          },
          {
            "id": "applied-mathematics-1-4",
            "name": "Algorithms: Greedy vs Dynamic Programming"
          },
          {
            "id": "applied-mathematics-1-5",
            "name": "Project Scheduling and Critical Paths"
          }
        ]
      },
      {
        "id": "applied-mathematics-2",
        "name": "Strand 3: Mathematically Modelling the Physical World; Kinematics and Dynamics",
        "subtopics": [
          {
            "id": "applied-mathematics-2-0",
            "name": "Kinematics: Particle Motion in One Dimension"
          },
          {
            "id": "applied-mathematics-2-1",
            "name": "Describing Motion with Calculus"
          },
          {
            "id": "applied-mathematics-2-2",
            "name": "Particle Motion in 2D: Vectors and Projectile Motion"
          },
          {
            "id": "applied-mathematics-2-3",
            "name": "Forces, Newton's Laws and Free-Body Diagrams"
          },
          {
            "id": "applied-mathematics-2-4",
            "name": "Momentum, Impulse and Collisions"
          },
          {
            "id": "applied-mathematics-2-5",
            "name": "Connected Masses, Friction and Drag"
          },
          {
            "id": "applied-mathematics-2-6",
            "name": "Work, Energy and Conservation"
          },
          {
            "id": "applied-mathematics-2-7",
            "name": "Circular Motion of a Particle"
          },
          {
            "id": "applied-mathematics-2-8",
            "name": "Dimensional Analysis"
          },
          {
            "id": "applied-mathematics-2-9",
            "name": "Relative Velocity"
          },
          {
            "id": "applied-mathematics-2-10",
            "name": "Statics & Centre of Gravity"
          },
          {
            "id": "applied-mathematics-2-11",
            "name": "Hydrostatics"
          },
          {
            "id": "applied-mathematics-2-12",
            "name": "Rigid Body Motion & Moments of Inertia"
          },
          {
            "id": "applied-mathematics-2-13",
            "name": "Simple Harmonic Motion & Hooke's Law"
          }
        ]
      },
      {
        "id": "applied-mathematics-3",
        "name": "Strand 4: Mathematically Modelling a Changing World",
        "subtopics": [
          {
            "id": "applied-mathematics-3-0",
            "name": "Recurrence Relations and Differences"
          },
          {
            "id": "applied-mathematics-3-1",
            "name": "Modelling Incremental Change with Difference Equations"
          },
          {
            "id": "applied-mathematics-3-2",
            "name": "Solving Difference Equations (Homogeneous and Inhomogeneous)"
          },
          {
            "id": "applied-mathematics-3-3",
            "name": "Modelling Continuous Change with Differential Equations"
          },
          {
            "id": "applied-mathematics-3-4",
            "name": "Solving Differential Equations (Separable; Reducible Second-Order)"
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
            "name": "Linear Motion"
          },
          {
            "id": "physics-0-1",
            "name": "Vectors and Scalars"
          },
          {
            "id": "physics-0-2",
            "name": "Newton's Laws of Motion"
          },
          {
            "id": "physics-0-3",
            "name": "Conservation of Momentum"
          },
          {
            "id": "physics-0-4",
            "name": "Gravity"
          },
          {
            "id": "physics-0-5",
            "name": "Density and Pressure"
          },
          {
            "id": "physics-0-6",
            "name": "Moments"
          },
          {
            "id": "physics-0-7",
            "name": "Conditions for Equilibrium"
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
            "name": "Circular Motion (HL)"
          },
          {
            "id": "physics-0-12",
            "name": "Simple Harmonic Motion and Hooke's Law (HL)"
          },
          {
            "id": "physics-0-13",
            "name": "Equations of Motion"
          }
        ]
      },
      {
        "id": "physics-1",
        "name": "Temperature",
        "subtopics": [
          {
            "id": "physics-1-0",
            "name": "Concept of Temperature"
          },
          {
            "id": "physics-1-1",
            "name": "Thermometric Property"
          },
          {
            "id": "physics-1-2",
            "name": "Thermometers and Temperature Scales"
          }
        ]
      },
      {
        "id": "physics-2",
        "name": "Heat",
        "subtopics": [
          {
            "id": "physics-2-0",
            "name": "Concept of Heat"
          },
          {
            "id": "physics-2-1",
            "name": "Specific Heat Capacity"
          },
          {
            "id": "physics-2-2",
            "name": "Specific Latent Heat"
          },
          {
            "id": "physics-2-3",
            "name": "Heat Transfer: Conduction"
          },
          {
            "id": "physics-2-4",
            "name": "Heat Transfer: Convection"
          },
          {
            "id": "physics-2-5",
            "name": "Heat Transfer: Radiation"
          },
          {
            "id": "physics-2-6",
            "name": "Mandatory Experiments (Calorimetry)"
          }
        ]
      },
      {
        "id": "physics-3",
        "name": "Waves",
        "subtopics": [
          {
            "id": "physics-3-0",
            "name": "Properties of Waves"
          },
          {
            "id": "physics-3-1",
            "name": "Wave Phenomena"
          },
          {
            "id": "physics-3-2",
            "name": "Doppler Effect"
          }
        ]
      },
      {
        "id": "physics-4",
        "name": "Vibrations and Sound",
        "subtopics": [
          {
            "id": "physics-4-0",
            "name": "Wave Nature of Sound"
          },
          {
            "id": "physics-4-1",
            "name": "Characteristics of Notes"
          },
          {
            "id": "physics-4-2",
            "name": "Resonance"
          },
          {
            "id": "physics-4-3",
            "name": "Vibrations in Strings and Pipes"
          },
          {
            "id": "physics-4-4",
            "name": "Sound Intensity"
          }
        ]
      },
      {
        "id": "physics-5",
        "name": "Light",
        "subtopics": [
          {
            "id": "physics-5-0",
            "name": "Laws of Reflection"
          },
          {
            "id": "physics-5-1",
            "name": "Mirrors"
          },
          {
            "id": "physics-5-2",
            "name": "Laws of Refraction"
          },
          {
            "id": "physics-5-3",
            "name": "Total Internal Reflection"
          },
          {
            "id": "physics-5-4",
            "name": "Lenses"
          },
          {
            "id": "physics-5-5",
            "name": "Diffraction and Interference"
          },
          {
            "id": "physics-5-6",
            "name": "Light as a Transverse Wave"
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
            "name": "Electromagnetic Spectrum"
          },
          {
            "id": "physics-5-10",
            "name": "The Spectrometer"
          }
        ]
      },
      {
        "id": "physics-6",
        "name": "Electricity",
        "subtopics": [
          {
            "id": "physics-6-0",
            "name": "Electrification by Contact"
          },
          {
            "id": "physics-6-1",
            "name": "Electrification by Induction"
          },
          {
            "id": "physics-6-2",
            "name": "Distribution of Charge on Conductors"
          },
          {
            "id": "physics-6-3",
            "name": "The Electroscope"
          },
          {
            "id": "physics-6-4",
            "name": "Force Between Charges"
          },
          {
            "id": "physics-6-5",
            "name": "Electric Fields"
          },
          {
            "id": "physics-6-6",
            "name": "Potential Difference"
          },
          {
            "id": "physics-6-7",
            "name": "Capacitors and Capacitance"
          },
          {
            "id": "physics-6-8",
            "name": "Electric Current"
          },
          {
            "id": "physics-6-9",
            "name": "Sources of EMF and Current"
          },
          {
            "id": "physics-6-10",
            "name": "Conduction in Materials and Semiconductors"
          },
          {
            "id": "physics-6-11",
            "name": "Resistance"
          },
          {
            "id": "physics-6-12",
            "name": "Effects of an Electric Current"
          },
          {
            "id": "physics-6-13",
            "name": "Domestic Circuits and Safety"
          },
          {
            "id": "physics-6-14",
            "name": "Magnetism and Magnetic Fields"
          },
          {
            "id": "physics-6-15",
            "name": "Current in a Magnetic Field"
          },
          {
            "id": "physics-6-16",
            "name": "Electromagnetic Induction"
          },
          {
            "id": "physics-6-17",
            "name": "Alternating Current"
          },
          {
            "id": "physics-6-18",
            "name": "Mutual and Self-Induction"
          }
        ]
      },
      {
        "id": "physics-7",
        "name": "Modern Physics",
        "subtopics": [
          {
            "id": "physics-7-0",
            "name": "The Electron"
          },
          {
            "id": "physics-7-1",
            "name": "Thermionic Emission"
          },
          {
            "id": "physics-7-2",
            "name": "Photoelectric Emission"
          },
          {
            "id": "physics-7-3",
            "name": "X-Rays"
          },
          {
            "id": "physics-7-4",
            "name": "Structure of the Atom"
          },
          {
            "id": "physics-7-5",
            "name": "Structure of the Nucleus"
          },
          {
            "id": "physics-7-6",
            "name": "Radioactivity"
          },
          {
            "id": "physics-7-7",
            "name": "Nuclear Energy"
          },
          {
            "id": "physics-7-8",
            "name": "Ionising Radiation: Hazards and Uses"
          },
          {
            "id": "physics-7-9",
            "name": "Particle Physics (Option, HL) — Fundamental Forces, Quarks and Accelerators"
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
            "name": "2.5 Molecule Shapes and Forces"
          },
          {
            "id": "chemistry-1-5",
            "name": "2.6 Oxidation Numbers"
          }
        ]
      },
      {
        "id": "chemistry-2",
        "name": "3. Stoichiometry, Formulas, Equations",
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
          },
          {
            "id": "chemistry-3-3",
            "name": "Acid-Base Theories (Bronsted-Lowry, Arrhenius)"
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
            "name": "5.2 Aliphatic Hydrocarbons"
          },
          {
            "id": "chemistry-4-2",
            "name": "5.3 Aromatic Hydrocarbons"
          },
          {
            "id": "chemistry-4-3",
            "name": "5.4 Exothermic and Endothermic"
          },
          {
            "id": "chemistry-4-4",
            "name": "5.5 Oil Refining and Products"
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
            "name": "6.2 Factors Affecting Rates"
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
            "name": "7.3 Organic Reaction Types"
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
          },
          {
            "id": "chemistry-7-2",
            "name": "Equilibrium Constant (Kc) Calculations"
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
            "name": "2B.1 Electrochemical Series"
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
            "name": "2B.4 Electropositive Metals (Na, Al)"
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
            "name": "Linear Motion"
          },
          {
            "id": "physics-and-chemistry-0-1",
            "name": "Vectors and Scalars"
          },
          {
            "id": "physics-and-chemistry-0-2",
            "name": "Newton's Laws of Motion"
          },
          {
            "id": "physics-and-chemistry-0-3",
            "name": "Conservation of Momentum"
          },
          {
            "id": "physics-and-chemistry-0-4",
            "name": "Gravity"
          },
          {
            "id": "physics-and-chemistry-0-5",
            "name": "Density and Pressure"
          },
          {
            "id": "physics-and-chemistry-0-6",
            "name": "Moments"
          },
          {
            "id": "physics-and-chemistry-0-7",
            "name": "Conditions for Equilibrium"
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
            "name": "Circular Motion (HL)"
          },
          {
            "id": "physics-and-chemistry-0-12",
            "name": "SHM and Hooke's Law (HL)"
          }
        ]
      },
      {
        "id": "physics-and-chemistry-1",
        "name": "Temperature",
        "subtopics": [
          {
            "id": "physics-and-chemistry-1-0",
            "name": "Concept of Temperature"
          },
          {
            "id": "physics-and-chemistry-1-1",
            "name": "Thermometric Property"
          },
          {
            "id": "physics-and-chemistry-1-2",
            "name": "Thermometers and Temperature Scales"
          },
          {
            "id": "physics-and-chemistry-1-3",
            "name": "Gas Laws and Kinetic Theory"
          }
        ]
      },
      {
        "id": "physics-and-chemistry-2",
        "name": "Heat",
        "subtopics": [
          {
            "id": "physics-and-chemistry-2-0",
            "name": "Concept of Heat"
          },
          {
            "id": "physics-and-chemistry-2-1",
            "name": "Specific Heat Capacity"
          },
          {
            "id": "physics-and-chemistry-2-2",
            "name": "Specific Latent Heat"
          },
          {
            "id": "physics-and-chemistry-2-3",
            "name": "Heat Transfer: Conduction"
          },
          {
            "id": "physics-and-chemistry-2-4",
            "name": "Heat Transfer: Convection"
          },
          {
            "id": "physics-and-chemistry-2-5",
            "name": "Heat Transfer: Radiation"
          }
        ]
      },
      {
        "id": "physics-and-chemistry-3",
        "name": "Waves",
        "subtopics": [
          {
            "id": "physics-and-chemistry-3-0",
            "name": "Properties of Waves"
          },
          {
            "id": "physics-and-chemistry-3-1",
            "name": "Wave Phenomena"
          },
          {
            "id": "physics-and-chemistry-3-2",
            "name": "Doppler Effect"
          }
        ]
      },
      {
        "id": "physics-and-chemistry-4",
        "name": "Vibrations and Sound",
        "subtopics": [
          {
            "id": "physics-and-chemistry-4-0",
            "name": "Wave Nature of Sound"
          },
          {
            "id": "physics-and-chemistry-4-1",
            "name": "Characteristics of Notes"
          },
          {
            "id": "physics-and-chemistry-4-2",
            "name": "Resonance"
          },
          {
            "id": "physics-and-chemistry-4-3",
            "name": "Vibrations in Strings and Pipes"
          },
          {
            "id": "physics-and-chemistry-4-4",
            "name": "Sound Intensity"
          }
        ]
      },
      {
        "id": "physics-and-chemistry-5",
        "name": "Light",
        "subtopics": [
          {
            "id": "physics-and-chemistry-5-0",
            "name": "Laws of Reflection"
          },
          {
            "id": "physics-and-chemistry-5-1",
            "name": "Mirrors"
          },
          {
            "id": "physics-and-chemistry-5-2",
            "name": "Laws of Refraction"
          },
          {
            "id": "physics-and-chemistry-5-3",
            "name": "Total Internal Reflection"
          },
          {
            "id": "physics-and-chemistry-5-4",
            "name": "Lenses"
          },
          {
            "id": "physics-and-chemistry-5-5",
            "name": "Diffraction and Interference"
          },
          {
            "id": "physics-and-chemistry-5-6",
            "name": "Light as a Transverse Wave"
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
            "name": "Electromagnetic Spectrum"
          },
          {
            "id": "physics-and-chemistry-5-10",
            "name": "The Spectrometer"
          }
        ]
      },
      {
        "id": "physics-and-chemistry-6",
        "name": "Electricity",
        "subtopics": [
          {
            "id": "physics-and-chemistry-6-0",
            "name": "Electrification by Contact"
          },
          {
            "id": "physics-and-chemistry-6-1",
            "name": "Electrification by Induction"
          },
          {
            "id": "physics-and-chemistry-6-2",
            "name": "Distribution of Charge"
          },
          {
            "id": "physics-and-chemistry-6-3",
            "name": "The Electroscope"
          },
          {
            "id": "physics-and-chemistry-6-4",
            "name": "Force Between Charges"
          },
          {
            "id": "physics-and-chemistry-6-5",
            "name": "Electric Fields"
          },
          {
            "id": "physics-and-chemistry-6-6",
            "name": "Potential Difference"
          },
          {
            "id": "physics-and-chemistry-6-7",
            "name": "Capacitors and Capacitance"
          },
          {
            "id": "physics-and-chemistry-6-8",
            "name": "Electric Current"
          },
          {
            "id": "physics-and-chemistry-6-9",
            "name": "Sources of EMF and Current"
          },
          {
            "id": "physics-and-chemistry-6-10",
            "name": "Conduction in Materials"
          },
          {
            "id": "physics-and-chemistry-6-11",
            "name": "Resistance"
          },
          {
            "id": "physics-and-chemistry-6-12",
            "name": "Effects of an Electric Current"
          },
          {
            "id": "physics-and-chemistry-6-13",
            "name": "Domestic Circuits and Safety"
          },
          {
            "id": "physics-and-chemistry-6-14",
            "name": "Magnetism and Magnetic Fields"
          },
          {
            "id": "physics-and-chemistry-6-15",
            "name": "Current in a Magnetic Field"
          },
          {
            "id": "physics-and-chemistry-6-16",
            "name": "Electromagnetic Induction"
          },
          {
            "id": "physics-and-chemistry-6-17",
            "name": "Alternating Current"
          },
          {
            "id": "physics-and-chemistry-6-18",
            "name": "Mutual and Self-Induction"
          }
        ]
      },
      {
        "id": "physics-and-chemistry-7",
        "name": "Modern Physics",
        "subtopics": [
          {
            "id": "physics-and-chemistry-7-0",
            "name": "The Electron"
          },
          {
            "id": "physics-and-chemistry-7-1",
            "name": "Thermionic Emission"
          },
          {
            "id": "physics-and-chemistry-7-2",
            "name": "Photoelectric Emission"
          },
          {
            "id": "physics-and-chemistry-7-3",
            "name": "X-Rays"
          },
          {
            "id": "physics-and-chemistry-7-4",
            "name": "Structure of the Atom"
          },
          {
            "id": "physics-and-chemistry-7-5",
            "name": "Structure of the Nucleus"
          },
          {
            "id": "physics-and-chemistry-7-6",
            "name": "Radioactivity"
          },
          {
            "id": "physics-and-chemistry-7-7",
            "name": "Nuclear Energy"
          },
          {
            "id": "physics-and-chemistry-7-8",
            "name": "Ionising Radiation: Hazards and Uses"
          },
          {
            "id": "physics-and-chemistry-7-9",
            "name": "Particle Physics (Option, HL)"
          }
        ]
      },
      {
        "id": "physics-and-chemistry-8",
        "name": "Chemistry",
        "subtopics": [
          {
            "id": "physics-and-chemistry-8-0",
            "name": "Atomic Structure & the Periodic Table"
          },
          {
            "id": "physics-and-chemistry-8-1",
            "name": "Chemical Bonding"
          },
          {
            "id": "physics-and-chemistry-8-2",
            "name": "Acids, Bases, pH & Volumetric Analysis"
          },
          {
            "id": "physics-and-chemistry-8-3",
            "name": "Oxidation & Reduction"
          },
          {
            "id": "physics-and-chemistry-8-4",
            "name": "Organic Chemistry (Hydrocarbons)"
          },
          {
            "id": "physics-and-chemistry-8-5",
            "name": "General & Applied Chemistry"
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
        "name": "Unit One: The Study of Life",
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
            "name": "Food & Nutrition (Food Tests)"
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
            "name": "Cell Metabolism & Enzymes"
          },
          {
            "id": "biology-1-2",
            "name": "Cell Continuity (Cell Division)"
          },
          {
            "id": "biology-1-3",
            "name": "Cell Diversity"
          },
          {
            "id": "biology-1-4",
            "name": "Genetics, DNA & Evolution"
          },
          {
            "id": "biology-1-5",
            "name": "Photosynthesis"
          },
          {
            "id": "biology-1-6",
            "name": "Respiration"
          },
          {
            "id": "biology-1-7",
            "name": "Movement Through Cell Membranes"
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
            "name": "Plant Structure & Transport"
          },
          {
            "id": "biology-2-2",
            "name": "Digestive System & Nutrition"
          },
          {
            "id": "biology-2-3",
            "name": "Breathing System"
          },
          {
            "id": "biology-2-4",
            "name": "Nervous System & Responses to Stimuli"
          },
          {
            "id": "biology-2-5",
            "name": "Reproduction and Growth"
          },
          {
            "id": "biology-2-6",
            "name": "Blood & Circulatory System"
          },
          {
            "id": "biology-2-7",
            "name": "Excretion & Homeostasis"
          },
          {
            "id": "biology-2-8",
            "name": "Endocrine (Hormonal) System"
          },
          {
            "id": "biology-2-9",
            "name": "Sensory Organs (Eye & Ear)"
          },
          {
            "id": "biology-2-10",
            "name": "Musculoskeletal System"
          },
          {
            "id": "biology-2-11",
            "name": "Plant Responses"
          },
          {
            "id": "biology-2-12",
            "name": "Human Reproduction"
          },
          {
            "id": "biology-2-13",
            "name": "Plant Reproduction"
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
        "name": "Strand 1: Scientific Practices",
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
            "name": "Evaluating Evidence"
          },
          {
            "id": "agricultural-science-0-3",
            "name": "Communicating"
          },
          {
            "id": "agricultural-science-0-4",
            "name": "Working Safely"
          }
        ]
      },
      {
        "id": "agricultural-science-1",
        "name": "Strand 2: Soils",
        "subtopics": [
          {
            "id": "agricultural-science-1-0",
            "name": "Formation And Classification"
          },
          {
            "id": "agricultural-science-1-1",
            "name": "Properties (Overview)"
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
          },
          {
            "id": "agricultural-science-1-6",
            "name": "Fertilisers, Nutrient Cycles & the Environment"
          }
        ]
      },
      {
        "id": "agricultural-science-2",
        "name": "Strand 3: Crops",
        "subtopics": [
          {
            "id": "agricultural-science-2-0",
            "name": "Plant Physiology"
          },
          {
            "id": "agricultural-science-2-1",
            "name": "Classification / Identification"
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
          },
          {
            "id": "agricultural-science-2-6",
            "name": "Grassland Management"
          }
        ]
      },
      {
        "id": "agricultural-science-3",
        "name": "Strand 4: Animals",
        "subtopics": [
          {
            "id": "agricultural-science-3-0",
            "name": "Animal Physiology"
          },
          {
            "id": "agricultural-science-3-1",
            "name": "Classification / Identification"
          },
          {
            "id": "agricultural-science-3-2",
            "name": "Production"
          },
          {
            "id": "agricultural-science-3-3",
            "name": "Animal Production Systems (Beef, Dairy, Sheep, Pig)"
          },
          {
            "id": "agricultural-science-3-4",
            "name": "Production: Management"
          },
          {
            "id": "agricultural-science-3-5",
            "name": "Production: Animal Husbandry & Health"
          },
          {
            "id": "agricultural-science-3-6",
            "name": "Genetics & Breeding"
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
        "name": "Strand 1: Practices and Principles",
        "subtopics": [
          {
            "id": "computer-science-0-0",
            "name": "Computational Thinking"
          },
          {
            "id": "computer-science-0-1",
            "name": "Problem Solving"
          },
          {
            "id": "computer-science-0-2",
            "name": "Logical Thinking"
          },
          {
            "id": "computer-science-0-3",
            "name": "Algorithmic Thinking"
          },
          {
            "id": "computer-science-0-4",
            "name": "Modelling and Simulation"
          },
          {
            "id": "computer-science-0-5",
            "name": "Heuristics"
          },
          {
            "id": "computer-science-0-6",
            "name": "Computers and Society"
          },
          {
            "id": "computer-science-0-7",
            "name": "Social and Ethical Considerations"
          },
          {
            "id": "computer-science-0-8",
            "name": "Turing Machines"
          },
          {
            "id": "computer-science-0-9",
            "name": "The Internet"
          },
          {
            "id": "computer-science-0-10",
            "name": "Machine Learning"
          },
          {
            "id": "computer-science-0-11",
            "name": "Artificial Intelligence"
          },
          {
            "id": "computer-science-0-12",
            "name": "User-Centred Design"
          },
          {
            "id": "computer-science-0-13",
            "name": "Adaptive Tech and Accessibility"
          },
          {
            "id": "computer-science-0-14",
            "name": "Careers in Computing"
          },
          {
            "id": "computer-science-0-15",
            "name": "Designing and Developing"
          },
          {
            "id": "computer-science-0-16",
            "name": "Design Process"
          },
          {
            "id": "computer-science-0-17",
            "name": "Working in a Team"
          },
          {
            "id": "computer-science-0-18",
            "name": "Communication and Reporting"
          },
          {
            "id": "computer-science-0-19",
            "name": "Software Development and Management"
          }
        ]
      },
      {
        "id": "computer-science-1",
        "name": "Strand 2: Core Concepts",
        "subtopics": [
          {
            "id": "computer-science-1-0",
            "name": "Abstraction"
          },
          {
            "id": "computer-science-1-1",
            "name": "Abstraction: Modular Design"
          },
          {
            "id": "computer-science-1-2",
            "name": "Algorithms"
          },
          {
            "id": "computer-science-1-3",
            "name": "Programming Concepts"
          },
          {
            "id": "computer-science-1-4",
            "name": "Pseudocode"
          },
          {
            "id": "computer-science-1-5",
            "name": "Sorting Algorithms"
          },
          {
            "id": "computer-science-1-6",
            "name": "Search Algorithms"
          },
          {
            "id": "computer-science-1-7",
            "name": "Functions, Procedures and Modules"
          },
          {
            "id": "computer-science-1-8",
            "name": "Algorithmic Complexity"
          },
          {
            "id": "computer-science-1-9",
            "name": "Computer Systems"
          },
          {
            "id": "computer-science-1-10",
            "name": "CPU Architecture"
          },
          {
            "id": "computer-science-1-11",
            "name": "Basic Electronics"
          },
          {
            "id": "computer-science-1-12",
            "name": "Logic Gates"
          },
          {
            "id": "computer-science-1-13",
            "name": "Operating System Layers"
          },
          {
            "id": "computer-science-1-14",
            "name": "Number Systems and Conversion"
          },
          {
            "id": "computer-science-1-15",
            "name": "Digital and Analogue Input"
          },
          {
            "id": "computer-science-1-16",
            "name": "Network Protocols"
          },
          {
            "id": "computer-science-1-17",
            "name": "The Web and the Internet"
          },
          {
            "id": "computer-science-1-18",
            "name": "Data"
          },
          {
            "id": "computer-science-1-19",
            "name": "Data Types"
          },
          {
            "id": "computer-science-1-20",
            "name": "Character Encoding"
          },
          {
            "id": "computer-science-1-21",
            "name": "Information Systems"
          },
          {
            "id": "computer-science-1-22",
            "name": "Evaluation and Testing"
          },
          {
            "id": "computer-science-1-23",
            "name": "Debugging"
          },
          {
            "id": "computer-science-1-24",
            "name": "Testing Methods"
          },
          {
            "id": "computer-science-1-25",
            "name": "Recursion"
          },
          {
            "id": "computer-science-1-26",
            "name": "Cryptography and Encryption"
          },
          {
            "id": "computer-science-1-27",
            "name": "Python Programming"
          },
          {
            "id": "computer-science-1-28",
            "name": "JavaScript"
          },
          {
            "id": "computer-science-1-29",
            "name": "HTML & CSS"
          }
        ]
      },
      {
        "id": "computer-science-2",
        "name": "Strand 3: Computer Science in Practice",
        "subtopics": [
          {
            "id": "computer-science-2-0",
            "name": "ALT1: Interactive Information Systems"
          },
          {
            "id": "computer-science-2-1",
            "name": "ALT1: Web and User-Centred Design"
          },
          {
            "id": "computer-science-2-2",
            "name": "Databases & Files (ALT1)"
          },
          {
            "id": "computer-science-2-3",
            "name": "ALT2: Analytics"
          },
          {
            "id": "computer-science-2-4",
            "name": "ALT2: Data Analysis"
          },
          {
            "id": "computer-science-2-5",
            "name": "ALT2: Statistics and Data Representation"
          },
          {
            "id": "computer-science-2-6",
            "name": "ALT3: Modelling and Simulation"
          },
          {
            "id": "computer-science-2-7",
            "name": "ALT3: Agent-Based Modelling"
          },
          {
            "id": "computer-science-2-8",
            "name": "ALT4: Embedded Systems (micro:bit)"
          },
          {
            "id": "computer-science-2-9",
            "name": "ALT4: Inputs and Outputs"
          },
          {
            "id": "computer-science-2-10",
            "name": "Computational Thinking Coursework Project (SEC-assessed)"
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
        "name": "Conceptual Framework of Accounting",
        "subtopics": [
          {
            "id": "accounting-0-0",
            "name": "Nature and Purpose of the Framework"
          },
          {
            "id": "accounting-0-1",
            "name": "Objectives of Financial Reporting"
          },
          {
            "id": "accounting-0-2",
            "name": "Users of Accounting Information"
          },
          {
            "id": "accounting-0-3",
            "name": "Qualitative Characteristics"
          },
          {
            "id": "accounting-0-4",
            "name": "Concepts, Bases and Policies"
          },
          {
            "id": "accounting-0-5",
            "name": "Fundamental Accounting Concepts (Going Concern, Accruals, Consistency, Prudence)"
          },
          {
            "id": "accounting-0-6",
            "name": "Other Concepts and Conventions"
          }
        ]
      },
      {
        "id": "accounting-1",
        "name": "Regulatory Framework (HL)",
        "subtopics": [
          {
            "id": "accounting-1-0",
            "name": "Nature and Objectives of Regulation"
          },
          {
            "id": "accounting-1-1",
            "name": "Regulatory Bodies"
          },
          {
            "id": "accounting-1-2",
            "name": "Regulatory Mechanism"
          },
          {
            "id": "accounting-1-3",
            "name": "True and Fair View"
          },
          {
            "id": "accounting-1-4",
            "name": "Role of the Auditor"
          },
          {
            "id": "accounting-1-5",
            "name": "Monitoring of Regulation"
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
          },
          {
            "id": "accounting-2-4",
            "name": "Correction of Errors"
          },
          {
            "id": "accounting-2-5",
            "name": "Depreciation & Revaluation of Fixed Assets"
          },
          {
            "id": "accounting-2-6",
            "name": "Tabular Statements"
          }
        ]
      },
      {
        "id": "accounting-3",
        "name": "Sole Traders",
        "subtopics": [
          {
            "id": "accounting-3-0",
            "name": "Nature of Sole Traders"
          },
          {
            "id": "accounting-3-1",
            "name": "Sole Trader Final Accounts"
          },
          {
            "id": "accounting-3-2",
            "name": "Gross Profit, Net Profit and Net Worth"
          }
        ]
      },
      {
        "id": "accounting-4",
        "name": "Company Accounting",
        "subtopics": [
          {
            "id": "accounting-4-0",
            "name": "Share Capital, Reserves and Loans"
          },
          {
            "id": "accounting-4-1",
            "name": "Company Final Accounts"
          },
          {
            "id": "accounting-4-2",
            "name": "Published Accounts of PLCs (HL)"
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
            "name": "Stock Valuation (FIFO/AVCO, Lower of Cost and NRV)"
          },
          {
            "id": "accounting-5-2",
            "name": "Club Accounts"
          },
          {
            "id": "accounting-5-3",
            "name": "Departmental Accounts"
          },
          {
            "id": "accounting-5-4",
            "name": "Farm Accounts"
          },
          {
            "id": "accounting-5-5",
            "name": "Service Firm Accounts"
          }
        ]
      },
      {
        "id": "accounting-6",
        "name": "Incomplete Records",
        "subtopics": [
          {
            "id": "accounting-6-0",
            "name": "Why Incomplete Records Arise"
          },
          {
            "id": "accounting-6-1",
            "name": "Incomplete Records — Control Accounts Method"
          },
          {
            "id": "accounting-6-2",
            "name": "Incomplete Records — Net Worth Method"
          },
          {
            "id": "accounting-6-3",
            "name": "Incomplete Records — Mark-Up & Margin (HL)"
          }
        ]
      },
      {
        "id": "accounting-7",
        "name": "Cash Flow Statements",
        "subtopics": [
          {
            "id": "accounting-7-0",
            "name": "Importance of Cash Flow Statements"
          },
          {
            "id": "accounting-7-1",
            "name": "Distinction Between Profit and Cash"
          },
          {
            "id": "accounting-7-2",
            "name": "Cash v Non-Cash Items"
          },
          {
            "id": "accounting-7-3",
            "name": "Sources of Cash Inflows and Outflows"
          },
          {
            "id": "accounting-7-4",
            "name": "Working Capital and Cash Flows"
          },
          {
            "id": "accounting-7-5",
            "name": "Preparing Cash Flow Statements"
          }
        ]
      },
      {
        "id": "accounting-8",
        "name": "Analysis of Financial Statements",
        "subtopics": [
          {
            "id": "accounting-8-0",
            "name": "Objective of Analysis"
          },
          {
            "id": "accounting-8-1",
            "name": "Interpretation of Accounts (Ratios)"
          },
          {
            "id": "accounting-8-2",
            "name": "Users and Their Interests"
          },
          {
            "id": "accounting-8-3",
            "name": "Limitations of Ratio Analysis"
          },
          {
            "id": "accounting-8-4",
            "name": "Profitability and Efficiency Ratios"
          },
          {
            "id": "accounting-8-5",
            "name": "Working Capital Ratios"
          },
          {
            "id": "accounting-8-6",
            "name": "Liquidity/Solvency Ratios"
          },
          {
            "id": "accounting-8-7",
            "name": "Gearing Ratios"
          },
          {
            "id": "accounting-8-8",
            "name": "Investment Ratios"
          },
          {
            "id": "accounting-8-9",
            "name": "Interpreting Ratio Findings"
          },
          {
            "id": "accounting-8-10",
            "name": "Presentation of Reports (HL)"
          }
        ]
      },
      {
        "id": "accounting-9",
        "name": "Management Accounting",
        "subtopics": [
          {
            "id": "accounting-9-0",
            "name": "Nature and Scope of Mgmt Accounting"
          },
          {
            "id": "accounting-9-1",
            "name": "Cost Classifications"
          },
          {
            "id": "accounting-9-2",
            "name": "Product & Absorption Costing (Overheads)"
          },
          {
            "id": "accounting-9-3",
            "name": "Marginal Costing & CVP Analysis"
          },
          {
            "id": "accounting-9-4",
            "name": "Budgetary Planning and Control"
          },
          {
            "id": "accounting-9-5",
            "name": "Flexible Budgeting (HL)"
          },
          {
            "id": "accounting-9-6",
            "name": "Cash Budgeting"
          },
          {
            "id": "accounting-9-7",
            "name": "Production & Product Budgeting"
          }
        ]
      },
      {
        "id": "accounting-10",
        "name": "IT in Accounting",
        "subtopics": [
          {
            "id": "accounting-10-0",
            "name": "Importance of IT in Accounting"
          },
          {
            "id": "accounting-10-1",
            "name": "Spreadsheet Applications"
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
            "name": "People and Their Relationships"
          },
          {
            "id": "business-0-1",
            "name": "Consumers, Entrepreneurs, Investors"
          },
          {
            "id": "business-0-2",
            "name": "Producers, Suppliers, Services"
          },
          {
            "id": "business-0-3",
            "name": "Employer, Employee, Trade Unions"
          },
          {
            "id": "business-0-4",
            "name": "Interest Groups"
          },
          {
            "id": "business-0-5",
            "name": "Co-operation and Competition"
          },
          {
            "id": "business-0-6",
            "name": "Elements of Contract Law"
          },
          {
            "id": "business-0-7",
            "name": "Conflicting Interests and Resolution"
          },
          {
            "id": "business-0-8",
            "name": "Areas of Conflict in Business"
          },
          {
            "id": "business-0-9",
            "name": "Methods of Resolving Conflict"
          },
          {
            "id": "business-0-10",
            "name": "Consumer and Industrial Law"
          },
          {
            "id": "business-0-11",
            "name": "Communication and ICT in Business"
          },
          {
            "id": "business-0-12",
            "name": "1.1 People in Business & Contract Law"
          },
          {
            "id": "business-0-13",
            "name": "1.2 Conflict Resolution: The Consumer"
          },
          {
            "id": "business-0-14",
            "name": "1.3 Conflict Resolution: Industrial Relations"
          }
        ]
      },
      {
        "id": "business-1",
        "name": "Unit 2: Enterprise",
        "subtopics": [
          {
            "id": "business-1-0",
            "name": "Introduction to Enterprise"
          },
          {
            "id": "business-1-1",
            "name": "Entrepreneurs and Enterprise Skills"
          },
          {
            "id": "business-1-2",
            "name": "Characteristics of Entrepreneurs"
          },
          {
            "id": "business-1-3",
            "name": "Innate and Learned Skills"
          },
          {
            "id": "business-1-4",
            "name": "Applying Enterprise Skills"
          },
          {
            "id": "business-1-5",
            "name": "2.1 Enterprise"
          }
        ]
      },
      {
        "id": "business-2",
        "name": "Unit 3: Managing 1",
        "subtopics": [
          {
            "id": "business-2-0",
            "name": "Introduction to Management"
          },
          {
            "id": "business-2-1",
            "name": "Managers and Management Skills"
          },
          {
            "id": "business-2-2",
            "name": "Characteristics of Managers"
          },
          {
            "id": "business-2-3",
            "name": "Enterprise vs Management"
          },
          {
            "id": "business-2-4",
            "name": "Skill: Leading"
          },
          {
            "id": "business-2-5",
            "name": "Skill: Motivating"
          },
          {
            "id": "business-2-6",
            "name": "Skill: Communicating"
          },
          {
            "id": "business-2-7",
            "name": "Management Activities (Planning, Organising, Controlling)"
          },
          {
            "id": "business-2-8",
            "name": "Planning"
          },
          {
            "id": "business-2-9",
            "name": "Organising"
          },
          {
            "id": "business-2-10",
            "name": "Controlling"
          },
          {
            "id": "business-2-11",
            "name": "3.1 Management Skills: Leading & Motivating"
          },
          {
            "id": "business-2-12",
            "name": "3.2 Management Skills: Communication & ICT"
          },
          {
            "id": "business-2-13",
            "name": "3.3 Management Activities: Planning, Organising, Controlling"
          }
        ]
      },
      {
        "id": "business-3",
        "name": "Unit 4: Managing 2",
        "subtopics": [
          {
            "id": "business-3-0",
            "name": "Household and Business Manager"
          },
          {
            "id": "business-3-1",
            "name": "Aspects of Finance"
          },
          {
            "id": "business-3-2",
            "name": "Aspects of Insurance"
          },
          {
            "id": "business-3-3",
            "name": "Aspects of Taxation"
          },
          {
            "id": "business-3-4",
            "name": "Human Resource Management"
          },
          {
            "id": "business-3-5",
            "name": "HRM: Recruitment and Selection"
          },
          {
            "id": "business-3-6",
            "name": "HRM: Employer and Employee"
          },
          {
            "id": "business-3-7",
            "name": "HRM: Teamwork"
          },
          {
            "id": "business-3-8",
            "name": "HRM: Development and Reward"
          },
          {
            "id": "business-3-9",
            "name": "Changing Role of Management"
          },
          {
            "id": "business-3-10",
            "name": "Empowerment and TQM"
          },
          {
            "id": "business-3-11",
            "name": "Managing New Technologies"
          },
          {
            "id": "business-3-12",
            "name": "Monitoring the Business"
          },
          {
            "id": "business-3-13",
            "name": "Final Accounts and Balance Sheets"
          },
          {
            "id": "business-3-14",
            "name": "Profitability and Liquidity Ratios"
          },
          {
            "id": "business-3-15",
            "name": "Break-Even Analysis"
          },
          {
            "id": "business-3-16",
            "name": "4.1 Finance & Cash-Flow Management (Household & Business)"
          },
          {
            "id": "business-3-17",
            "name": "4.2 Insurance"
          },
          {
            "id": "business-3-18",
            "name": "4.3 Taxation"
          },
          {
            "id": "business-3-19",
            "name": "4.4 Ratio Analysis & Monitoring the Business"
          },
          {
            "id": "business-3-20",
            "name": "4.5 Human Resource Management"
          },
          {
            "id": "business-3-21",
            "name": "4.6 Managing Change & TQM"
          }
        ]
      },
      {
        "id": "business-4",
        "name": "Unit 5: Business in Action",
        "subtopics": [
          {
            "id": "business-4-0",
            "name": "Identifying Opportunities"
          },
          {
            "id": "business-4-1",
            "name": "Sources of Opportunities"
          },
          {
            "id": "business-4-2",
            "name": "New Product Development"
          },
          {
            "id": "business-4-3",
            "name": "Marketing"
          },
          {
            "id": "business-4-4",
            "name": "The Marketing Concept"
          },
          {
            "id": "business-4-5",
            "name": "The Marketing Strategy"
          },
          {
            "id": "business-4-6",
            "name": "The Marketing Mix"
          },
          {
            "id": "business-4-7",
            "name": "Getting Started"
          },
          {
            "id": "business-4-8",
            "name": "Finance, Ownership, Production"
          },
          {
            "id": "business-4-9",
            "name": "Developing a Business Plan"
          },
          {
            "id": "business-4-10",
            "name": "Expansion"
          },
          {
            "id": "business-4-11",
            "name": "Reasons and Finance for Expansion"
          },
          {
            "id": "business-4-12",
            "name": "Methods of Expansion"
          },
          {
            "id": "business-4-13",
            "name": "Sources of Finance (Short, Medium, Long Term)"
          },
          {
            "id": "business-4-14",
            "name": "5.1 Identifying Opportunities & New Product Development"
          },
          {
            "id": "business-4-15",
            "name": "5.2 Getting Started in Business"
          },
          {
            "id": "business-4-16",
            "name": "5.3 Marketing: Market Research & Segmentation"
          },
          {
            "id": "business-4-17",
            "name": "5.4 Marketing: The 4 Ps (Product, Price, Place, Promotion)"
          },
          {
            "id": "business-4-18",
            "name": "5.5 Business Expansion"
          },
          {
            "id": "business-4-19",
            "name": "ABQ — Applied Business Question (Units 3, 4 & 5)"
          }
        ]
      },
      {
        "id": "business-5",
        "name": "Unit 6: Domestic Environment",
        "subtopics": [
          {
            "id": "business-5-0",
            "name": "Categories of Industry"
          },
          {
            "id": "business-5-1",
            "name": "Changing Trends in Business"
          },
          {
            "id": "business-5-2",
            "name": "Types of Business Organisation"
          },
          {
            "id": "business-5-3",
            "name": "Changing Trends in Ownership"
          },
          {
            "id": "business-5-4",
            "name": "Community Development"
          },
          {
            "id": "business-5-5",
            "name": "Economy's Impact on Business"
          },
          {
            "id": "business-5-6",
            "name": "Business's Impact on Economy"
          },
          {
            "id": "business-5-7",
            "name": "Business and the Wider Economy"
          },
          {
            "id": "business-5-8",
            "name": "Government and Business"
          },
          {
            "id": "business-5-9",
            "name": "Government as Employer"
          },
          {
            "id": "business-5-10",
            "name": "Social Responsibilities"
          },
          {
            "id": "business-5-11",
            "name": "Ethical Business Practice"
          },
          {
            "id": "business-5-12",
            "name": "Socially Responsible Business"
          },
          {
            "id": "business-5-13",
            "name": "6.1 Categories of Industry"
          },
          {
            "id": "business-5-14",
            "name": "6.2 Ownership Structures"
          },
          {
            "id": "business-5-15",
            "name": "6.3 Business, Government & the Economy"
          },
          {
            "id": "business-5-16",
            "name": "6.4 Community Development"
          },
          {
            "id": "business-5-17",
            "name": "6.5 Business Ethics & Social Responsibility"
          }
        ]
      },
      {
        "id": "business-6",
        "name": "Unit 7: International Environment",
        "subtopics": [
          {
            "id": "business-6-0",
            "name": "International Trading Environment"
          },
          {
            "id": "business-6-1",
            "name": "Trade and the Irish Economy"
          },
          {
            "id": "business-6-2",
            "name": "Changing International Economy"
          },
          {
            "id": "business-6-3",
            "name": "Opportunities and Challenges"
          },
          {
            "id": "business-6-4",
            "name": "Trading Blocs and Agreements"
          },
          {
            "id": "business-6-5",
            "name": "European Union"
          },
          {
            "id": "business-6-6",
            "name": "Importance of the EU"
          },
          {
            "id": "business-6-7",
            "name": "EU Policies and Directives"
          },
          {
            "id": "business-6-8",
            "name": "EU Decision-Making Process"
          },
          {
            "id": "business-6-9",
            "name": "Role of Special Interest Groups"
          },
          {
            "id": "business-6-10",
            "name": "International Business"
          },
          {
            "id": "business-6-11",
            "name": "Global Marketing"
          },
          {
            "id": "business-6-12",
            "name": "Transnational Companies"
          },
          {
            "id": "business-6-13",
            "name": "7.1 International Trade"
          },
          {
            "id": "business-6-14",
            "name": "7.2 The European Union"
          },
          {
            "id": "business-6-15",
            "name": "7.3 Global Business"
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
        "name": "Strand 1: What Is Economics About?",
        "subtopics": [
          {
            "id": "economics-0-0",
            "name": "Economics as a Way of Thinking"
          },
          {
            "id": "economics-0-1",
            "name": "Scarcity & Choice"
          },
          {
            "id": "economics-0-2",
            "name": "Sustainability"
          }
        ]
      },
      {
        "id": "economics-1",
        "name": "Strand 2: How Are Economic Decisions Made?",
        "subtopics": [
          {
            "id": "economics-1-0",
            "name": "The Market Economy"
          },
          {
            "id": "economics-1-1",
            "name": "The Consumer (Demand)"
          },
          {
            "id": "economics-1-2",
            "name": "The Firm (Supply)"
          },
          {
            "id": "economics-1-3",
            "name": "Government Intervention"
          },
          {
            "id": "economics-1-4",
            "name": "Elasticity (PED, PES, Income & Cross)"
          },
          {
            "id": "economics-1-5",
            "name": "Costs of Production, Revenue & Profit"
          }
        ]
      },
      {
        "id": "economics-2",
        "name": "Strand 3: What Can Markets Do?",
        "subtopics": [
          {
            "id": "economics-2-0",
            "name": "Market Structures"
          },
          {
            "id": "economics-2-1",
            "name": "The Labour Market"
          },
          {
            "id": "economics-2-2",
            "name": "Market Failure"
          }
        ]
      },
      {
        "id": "economics-3",
        "name": "Strand 4: What Is the Relationship Between Policy and Economic Performance?",
        "subtopics": [
          {
            "id": "economics-3-0",
            "name": "National Income"
          },
          {
            "id": "economics-3-1",
            "name": "Fiscal Policy & the Budget"
          },
          {
            "id": "economics-3-2",
            "name": "Employment & Unemployment"
          },
          {
            "id": "economics-3-3",
            "name": "Monetary Policy & Inflation"
          },
          {
            "id": "economics-3-4",
            "name": "Financial Sector"
          },
          {
            "id": "economics-3-5",
            "name": "Economic Growth"
          }
        ]
      },
      {
        "id": "economics-4",
        "name": "Strand 5: How Is Our Economy Influenced by International Economics?",
        "subtopics": [
          {
            "id": "economics-4-0",
            "name": "Growth & Development"
          },
          {
            "id": "economics-4-1",
            "name": "Globalisation"
          },
          {
            "id": "economics-4-2",
            "name": "International Trade & Competitiveness"
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
            "name": "Plate Tectonics (The Tectonic Cycle)"
          },
          {
            "id": "geography-0-1",
            "name": "The Rock Cycle"
          },
          {
            "id": "geography-0-2",
            "name": "Folding & Faulting (Geological Structures)"
          },
          {
            "id": "geography-0-3",
            "name": "Karst Landscapes (Rock Characteristics)"
          },
          {
            "id": "geography-0-4",
            "name": "Surface Processes (General)"
          },
          {
            "id": "geography-0-5",
            "name": "Landform Development (iv): Endo and Exogenetic Forces"
          },
          {
            "id": "geography-0-6",
            "name": "Human Interaction"
          },
          {
            "id": "geography-0-7",
            "name": "Earthquakes & Volcanoes"
          },
          {
            "id": "geography-0-8",
            "name": "Weathering & Mass Movement"
          },
          {
            "id": "geography-0-9",
            "name": "Rivers (Fluvial Processes & Landforms)"
          },
          {
            "id": "geography-0-10",
            "name": "The Sea (Coastal Processes & Landforms)"
          },
          {
            "id": "geography-0-11",
            "name": "Glaciation (Glacial Processes & Landforms)"
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
            "name": "The Complexity of Regions (i): Subsistence vs Commercial Economies"
          },
          {
            "id": "geography-1-3",
            "name": "The Complexity of Regions (ii): Urban, Political and Cultural Regions"
          },
          {
            "id": "geography-1-4",
            "name": "Irish Regions"
          },
          {
            "id": "geography-1-5",
            "name": "European Regions"
          },
          {
            "id": "geography-1-6",
            "name": "Continental / Sub-Continental Regions"
          }
        ]
      },
      {
        "id": "geography-2",
        "name": "Core Unit 3: Investigation and Skills",
        "subtopics": [
          {
            "id": "geography-2-0",
            "name": "Geographical Skills (Graphs, Tables & Data)"
          },
          {
            "id": "geography-2-1",
            "name": "Introduction: Posing the Problem"
          },
          {
            "id": "geography-2-2",
            "name": "Planning the Work"
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
          },
          {
            "id": "geography-2-6",
            "name": "Ordnance Survey Maps"
          },
          {
            "id": "geography-2-7",
            "name": "Weather Maps & Synoptic Charts"
          },
          {
            "id": "geography-2-8",
            "name": "Aerial Photographs & Satellite Imagery"
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
            "name": "Developing Economies & Spatial Variations in Development"
          },
          {
            "id": "geography-3-2",
            "name": "The Global Economy (Multinationals & Globalisation)"
          },
          {
            "id": "geography-3-3",
            "name": "Ireland and the European Union"
          },
          {
            "id": "geography-3-4",
            "name": "Environmental Impact"
          },
          {
            "id": "geography-3-5",
            "name": "Energy Resources"
          }
        ]
      },
      {
        "id": "geography-4",
        "name": "Elective Unit 5: Patterns and Processes in the Human Environment",
        "subtopics": [
          {
            "id": "geography-4-0",
            "name": "Population: Change Over Time and Space"
          },
          {
            "id": "geography-4-1",
            "name": "Population: Impact on Development"
          },
          {
            "id": "geography-4-2",
            "name": "Population: Movements and Impact"
          },
          {
            "id": "geography-4-3",
            "name": "Settlement: Site, Situation and Function"
          },
          {
            "id": "geography-4-4",
            "name": "Settlement: Changing Urban Landuse"
          },
          {
            "id": "geography-4-5",
            "name": "Settlement: Urban Growth Problems"
          }
        ]
      },
      {
        "id": "geography-5",
        "name": "Optional Unit 6: Global Interdependence",
        "subtopics": [
          {
            "id": "geography-5-0",
            "name": "Views of Development"
          },
          {
            "id": "geography-5-1",
            "name": "The Interdependent Global Economy"
          },
          {
            "id": "geography-5-2",
            "name": "Empowering People"
          },
          {
            "id": "geography-5-3",
            "name": "Sustainable Development"
          }
        ]
      },
      {
        "id": "geography-6",
        "name": "Optional Unit 7: Geoecology",
        "subtopics": [
          {
            "id": "geography-6-0",
            "name": "Soil Composition and Characteristics"
          },
          {
            "id": "geography-6-1",
            "name": "Soil Processes and Human Interference"
          },
          {
            "id": "geography-6-2",
            "name": "Biomes"
          },
          {
            "id": "geography-6-3",
            "name": "Human Alteration of Biomes"
          }
        ]
      },
      {
        "id": "geography-7",
        "name": "Optional Unit 8: Culture and Identity",
        "subtopics": [
          {
            "id": "geography-7-0",
            "name": "Cultural Indicators of Population"
          },
          {
            "id": "geography-7-1",
            "name": "Nationality and the Nation State"
          },
          {
            "id": "geography-7-2",
            "name": "Identity as a Concept"
          }
        ]
      },
      {
        "id": "geography-8",
        "name": "Optional Unit 9: The Atmosphere-Ocean Environment",
        "subtopics": [
          {
            "id": "geography-8-0",
            "name": "Composition of Atmosphere and Oceans"
          },
          {
            "id": "geography-8-1",
            "name": "Solar Energy Distribution"
          },
          {
            "id": "geography-8-2",
            "name": "Water Exchanges: Oceans and Atmosphere"
          },
          {
            "id": "geography-8-3",
            "name": "Atmospheric and Ocean Circulation"
          },
          {
            "id": "geography-8-4",
            "name": "Distinctive Climatic Environments"
          },
          {
            "id": "geography-8-5",
            "name": "Climate and Economic Development"
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
        "name": "Early Modern Field - Ireland, 1494-1815",
        "subtopics": [
          {
            "id": "history-0-0",
            "name": "Reform & Reformation in Tudor Ireland"
          },
          {
            "id": "history-0-1",
            "name": "Case Study: Plantation of Laois/Offaly"
          },
          {
            "id": "history-0-2",
            "name": "Case Study: Women & Marriage (Gaelic Law)"
          },
          {
            "id": "history-0-3",
            "name": "Case Study: The Bardic Schools"
          },
          {
            "id": "history-0-4",
            "name": "Elizabethan Ireland 1558-1603"
          },
          {
            "id": "history-0-5",
            "name": "Case Study: Lordship of Tir Eoghain"
          },
          {
            "id": "history-0-6",
            "name": "Case Study: Elizabethan Dublin"
          },
          {
            "id": "history-0-7",
            "name": "Case Study: Meiler Magrath's Career"
          },
          {
            "id": "history-0-8",
            "name": "Kingdom vs Colony 1603-1660"
          },
          {
            "id": "history-0-9",
            "name": "Case Study: The Trial of Strafford"
          },
          {
            "id": "history-0-10",
            "name": "Case Study: Scots Migration to Ulster"
          },
          {
            "id": "history-0-11",
            "name": "Case Study: Louvain"
          },
          {
            "id": "history-0-12",
            "name": "Colonial Ascendancy 1660-1715"
          },
          {
            "id": "history-0-13",
            "name": "Case Study: The Parliament of 1689"
          },
          {
            "id": "history-0-14",
            "name": "Case Study: Restoration Dublin"
          },
          {
            "id": "history-0-15",
            "name": "Case Study: The Jacobite Poets"
          },
          {
            "id": "history-0-16",
            "name": "Colony vs Kingdom 1715-1770"
          },
          {
            "id": "history-0-17",
            "name": "Case Study: The Ponsonbys"
          },
          {
            "id": "history-0-18",
            "name": "Case Study: The Whiteboys"
          },
          {
            "id": "history-0-19",
            "name": "Case Study: Trial of Fr. Sheehy"
          },
          {
            "id": "history-0-20",
            "name": "End of Irish Kingdom & the Union"
          },
          {
            "id": "history-0-21",
            "name": "Case Study: The Wexford Rebellion"
          },
          {
            "id": "history-0-22",
            "name": "Case Study: The Rise of Belfast"
          },
          {
            "id": "history-0-23",
            "name": "Case Study: Maynooth College"
          }
        ]
      },
      {
        "id": "history-1",
        "name": "Early Modern Field - Europe & the Wider World, 1492-1815",
        "subtopics": [
          {
            "id": "history-1-0",
            "name": "Renaissance to Reformation 1492-1567"
          },
          {
            "id": "history-1-1",
            "name": "Case Study: Henry VIII's Divorce"
          },
          {
            "id": "history-1-2",
            "name": "Case Study: Seville, Port of New World"
          },
          {
            "id": "history-1-3",
            "name": "Case Study: Calvin's Geneva"
          },
          {
            "id": "history-1-4",
            "name": "Religion & Power 1567-1609"
          },
          {
            "id": "history-1-5",
            "name": "Case Study: The Spanish Armada"
          },
          {
            "id": "history-1-6",
            "name": "Case Study: Decline of Antwerp"
          },
          {
            "id": "history-1-7",
            "name": "Case Study: Jesuit Mission in China"
          },
          {
            "id": "history-1-8",
            "name": "The Eclipse of Old Europe 1609-1660"
          },
          {
            "id": "history-1-9",
            "name": "Case Study: Revolt of the Catalans"
          },
          {
            "id": "history-1-10",
            "name": "Case Study: Dutch Empire in Asia"
          },
          {
            "id": "history-1-11",
            "name": "Case Study: Galileo & the Inquisition"
          },
          {
            "id": "history-1-12",
            "name": "Europe in the Age of Louis XIV"
          },
          {
            "id": "history-1-13",
            "name": "Case Study: The Streltsy"
          },
          {
            "id": "history-1-14",
            "name": "Case Study: The East India Company"
          },
          {
            "id": "history-1-15",
            "name": "Case Study: The Court of Versailles"
          },
          {
            "id": "history-1-16",
            "name": "Establishing Empires 1715-1775"
          },
          {
            "id": "history-1-17",
            "name": "Case Study: The Boston Tea Party"
          },
          {
            "id": "history-1-18",
            "name": "Case Study: West Indies Slave Plantations"
          },
          {
            "id": "history-1-19",
            "name": "Case Study: The Encyclopedie"
          },
          {
            "id": "history-1-20",
            "name": "Empires in Revolution 1775-1815"
          },
          {
            "id": "history-1-21",
            "name": "Case Study: Committee of Public Safety"
          },
          {
            "id": "history-1-22",
            "name": "Case Study: Growth of Manchester"
          },
          {
            "id": "history-1-23",
            "name": "Case Study: Civil Constitution of Clergy"
          }
        ]
      },
      {
        "id": "history-2",
        "name": "Later Modern Field - Ireland, 1815-1993",
        "subtopics": [
          {
            "id": "history-2-0",
            "name": "IRL 1: Ireland and the Union, 1815-1870"
          },
          {
            "id": "history-2-1",
            "name": "Case Study: Private Responses to Famine"
          },
          {
            "id": "history-2-2",
            "name": "Case Study: Catholic Emancipation"
          },
          {
            "id": "history-2-3",
            "name": "Case Study: The Synod of Thurles 1850"
          },
          {
            "id": "history-2-4",
            "name": "IRL 2: Movements for Political & Social Reform, 1870-1914"
          },
          {
            "id": "history-2-5",
            "name": "Case Study: Elections of 1885 & 1886"
          },
          {
            "id": "history-2-6",
            "name": "Case Study: Dublin 1913 Lockout"
          },
          {
            "id": "history-2-7",
            "name": "Case Study: The GAA to 1891"
          },
          {
            "id": "history-2-8",
            "name": "IRL 3: The Pursuit of Sovereignty & the Impact of Partition, 1912-1949"
          },
          {
            "id": "history-2-9",
            "name": "Case Study: The Treaty Negotiations 1921"
          },
          {
            "id": "history-2-10",
            "name": "Case Study: Belfast During WWII"
          },
          {
            "id": "history-2-11",
            "name": "Case Study: Eucharistic Congress 1932"
          },
          {
            "id": "history-2-12",
            "name": "IRL 4: The Irish Diaspora, 1840-1966"
          },
          {
            "id": "history-2-13",
            "name": "Case Study: Grosse Isle"
          },
          {
            "id": "history-2-14",
            "name": "Case Study: De Valera in America"
          },
          {
            "id": "history-2-15",
            "name": "Case Study: Holy Ghost Mission, Nigeria"
          },
          {
            "id": "history-2-16",
            "name": "IRL 5: Politics & Society in Northern Ireland, 1949-1993"
          },
          {
            "id": "history-2-17",
            "name": "Case Study: The Sunningdale Agreement"
          },
          {
            "id": "history-2-18",
            "name": "Case Study: Coleraine University"
          },
          {
            "id": "history-2-19",
            "name": "Case Study: Apprentice Boys of Derry"
          },
          {
            "id": "history-2-20",
            "name": "IRL 6: Government, Economy & Society in the Republic of Ireland, 1949-1989"
          },
          {
            "id": "history-2-21",
            "name": "Case Study: First Economic Programme"
          },
          {
            "id": "history-2-22",
            "name": "Case Study: EEC Impact on Fisheries"
          },
          {
            "id": "history-2-23",
            "name": "Case Study: Impact of RTE 1962-1972"
          }
        ]
      },
      {
        "id": "history-3",
        "name": "Later Modern Field - Europe & the Wider World, 1815-1993",
        "subtopics": [
          {
            "id": "history-3-0",
            "name": "EUR 1: Nationalism & State Formation, 1815-1871"
          },
          {
            "id": "history-3-1",
            "name": "Case Study: 1848 Revolution in Germany"
          },
          {
            "id": "history-3-2",
            "name": "Case Study: New Lanark"
          },
          {
            "id": "history-3-3",
            "name": "Case Study: Haussmann's Paris"
          },
          {
            "id": "history-3-4",
            "name": "EUR 2: Nation States & International Tensions, 1871-1920"
          },
          {
            "id": "history-3-5",
            "name": "Case Study: Naval Policy of Wilhelm II"
          },
          {
            "id": "history-3-6",
            "name": "Case Study: Women in the WWI Workforce"
          },
          {
            "id": "history-3-7",
            "name": "Case Study: Early History of the Motor Car"
          },
          {
            "id": "history-3-8",
            "name": "EUR 3: Dictatorship & Democracy, 1920-1945"
          },
          {
            "id": "history-3-9",
            "name": "Case Study: Stalin's Show Trials"
          },
          {
            "id": "history-3-10",
            "name": "Case Study: The Jarrow March 1936"
          },
          {
            "id": "history-3-11",
            "name": "Case Study: The Nuremberg Rallies"
          },
          {
            "id": "history-3-12",
            "name": "EUR 4: Division & Realignment in Europe, 1945-1992"
          },
          {
            "id": "history-3-13",
            "name": "Case Study: Hungarian Uprising 1956"
          },
          {
            "id": "history-3-14",
            "name": "Case Study: The Oil Crisis 1973"
          },
          {
            "id": "history-3-15",
            "name": "Case Study: Second Vatican Council"
          },
          {
            "id": "history-3-16",
            "name": "EUR 5: European Retreat from Empire & the Aftermath, 1945-1990"
          },
          {
            "id": "history-3-17",
            "name": "Case Study: British Withdrawal from India"
          },
          {
            "id": "history-3-18",
            "name": "Case Study: Secession of Katanga"
          },
          {
            "id": "history-3-19",
            "name": "Case Study: Race Relations in France"
          },
          {
            "id": "history-3-20",
            "name": "EUR 6: The United States & the World, 1945-1989"
          },
          {
            "id": "history-3-21",
            "name": "Case Study: Montgomery Bus Boycott"
          },
          {
            "id": "history-3-22",
            "name": "Case Study: Johnson & Vietnam"
          },
          {
            "id": "history-3-23",
            "name": "Case Study: The Moon Landing 1969"
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
            "name": "1.1 Power in the School"
          },
          {
            "id": "politics-and-society-0-1",
            "name": "1.2 The Need for Rules"
          },
          {
            "id": "politics-and-society-0-2",
            "name": "1.3 Dimensions of Power"
          },
          {
            "id": "politics-and-society-0-3",
            "name": "1.4 Effects of Rules"
          },
          {
            "id": "politics-and-society-0-4",
            "name": "2.1 Making National Policy"
          },
          {
            "id": "politics-and-society-0-5",
            "name": "2.2 Selecting the Executive"
          },
          {
            "id": "politics-and-society-0-6",
            "name": "2.3 Social Class and Gender"
          },
          {
            "id": "politics-and-society-0-7",
            "name": "2.4 Arguments on Representation"
          },
          {
            "id": "politics-and-society-0-8",
            "name": "2.5 Effectiveness of Representation"
          },
          {
            "id": "politics-and-society-0-9",
            "name": "2.6 Media, Public Opinion and Democracy"
          },
          {
            "id": "politics-and-society-0-10",
            "name": "2.7 Key Thinkers"
          },
          {
            "id": "politics-and-society-0-11",
            "name": "Topic 1: Power & Decision-Making in the School"
          },
          {
            "id": "politics-and-society-0-12",
            "name": "Topic 2: Power & Decision-Making at National & European Level"
          }
        ]
      },
      {
        "id": "politics-and-society-1",
        "name": "Strand 2: Active citizenship",
        "subtopics": [
          {
            "id": "politics-and-society-1-0",
            "name": "3.1 Positive Contributions"
          },
          {
            "id": "politics-and-society-1-1",
            "name": "3.2 Starting an Initiative"
          },
          {
            "id": "politics-and-society-1-2",
            "name": "3.3 Means of Taking Action"
          },
          {
            "id": "politics-and-society-1-3",
            "name": "3.4 Setting and Achieving Goals"
          },
          {
            "id": "politics-and-society-1-4",
            "name": "3.5 Developing Personal Qualities"
          },
          {
            "id": "politics-and-society-1-5",
            "name": "3.6 Self-Appraisal and Feedback"
          },
          {
            "id": "politics-and-society-1-6",
            "name": "4.1 Freedom of Expression"
          },
          {
            "id": "politics-and-society-1-7",
            "name": "4.2 Listening and Communicating"
          },
          {
            "id": "politics-and-society-1-8",
            "name": "4.3 Resolving Conflicts"
          },
          {
            "id": "politics-and-society-1-9",
            "name": "4.4 Evaluating Information"
          },
          {
            "id": "politics-and-society-1-10",
            "name": "4.5 Democracy in Wider Society"
          },
          {
            "id": "politics-and-society-1-11",
            "name": "Topic 3: Effectively Contributing to Communities"
          },
          {
            "id": "politics-and-society-1-12",
            "name": "Topic 4: Rights & Responsibilities in Communication"
          }
        ]
      },
      {
        "id": "politics-and-society-2",
        "name": "Strand 3: Human rights and responsibilities",
        "subtopics": [
          {
            "id": "politics-and-society-2-0",
            "name": "5.1 Rights of Young People"
          },
          {
            "id": "politics-and-society-2-1",
            "name": "5.2 Human Rights Principles"
          },
          {
            "id": "politics-and-society-2-2",
            "name": "5.3 Equality and Rights"
          },
          {
            "id": "politics-and-society-2-3",
            "name": "5.4 Arguments About Rights"
          },
          {
            "id": "politics-and-society-2-4",
            "name": "5.5 State Bodies for Rights"
          },
          {
            "id": "politics-and-society-2-5",
            "name": "5.6 The Right to Education"
          },
          {
            "id": "politics-and-society-2-6",
            "name": "5.7 Key Thinkers"
          },
          {
            "id": "politics-and-society-2-7",
            "name": "6.1 Rights in the Wider World"
          },
          {
            "id": "politics-and-society-2-8",
            "name": "6.2 Arguments on Global Rights"
          },
          {
            "id": "politics-and-society-2-9",
            "name": "6.3 International Cooperation"
          },
          {
            "id": "politics-and-society-2-10",
            "name": "Topic 5: Human Rights & Responsibilities in Ireland"
          },
          {
            "id": "politics-and-society-2-11",
            "name": "Topic 6: Human Rights & Responsibilities in Europe & the Wider World"
          }
        ]
      },
      {
        "id": "politics-and-society-3",
        "name": "Strand 4: Globalisation and localisation",
        "subtopics": [
          {
            "id": "politics-and-society-3-0",
            "name": "7.1 National Identity"
          },
          {
            "id": "politics-and-society-3-1",
            "name": "7.2 Diversity and Cultural Change"
          },
          {
            "id": "politics-and-society-3-2",
            "name": "7.3 Diversity in the EU"
          },
          {
            "id": "politics-and-society-3-3",
            "name": "7.4 Understanding Identity"
          },
          {
            "id": "politics-and-society-3-4",
            "name": "7.5 West and Non-West Culture"
          },
          {
            "id": "politics-and-society-3-5",
            "name": "7.6 Globalisation and Power"
          },
          {
            "id": "politics-and-society-3-6",
            "name": "7.7 Key Thinkers"
          },
          {
            "id": "politics-and-society-3-7",
            "name": "8.1 Acting for Sustainable Development"
          },
          {
            "id": "politics-and-society-3-8",
            "name": "8.2 Arguments on Sustainability"
          },
          {
            "id": "politics-and-society-3-9",
            "name": "8.3 Key Thinkers"
          },
          {
            "id": "politics-and-society-3-10",
            "name": "Topic 7: Globalisation & Identity"
          },
          {
            "id": "politics-and-society-3-11",
            "name": "Topic 8: Sustainable Development"
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
        "name": "Section A: The Search for Meaning and Values",
        "subtopics": [
          {
            "id": "religious-education-0-0",
            "name": "1.1 The Contemporary Context"
          },
          {
            "id": "religious-education-0-1",
            "name": "1.2 The Tradition of Search"
          },
          {
            "id": "religious-education-0-2",
            "name": "2.1 The Language of Symbol"
          },
          {
            "id": "religious-education-0-3",
            "name": "2.2 The Tradition of Response"
          },
          {
            "id": "religious-education-0-4",
            "name": "3.1 The Gods of the Ancients"
          },
          {
            "id": "religious-education-0-5",
            "name": "3.2 The Concept of Revelation"
          },
          {
            "id": "religious-education-0-6",
            "name": "3.3 Naming God, Past and Present"
          },
          {
            "id": "religious-education-0-7",
            "name": "4.1 Religion and Communal Values"
          },
          {
            "id": "religious-education-0-8",
            "name": "4.2 Secular Communal Values"
          }
        ]
      },
      {
        "id": "religious-education-1",
        "name": "Section B: Christianity: Origins and Contemporary Expressions",
        "subtopics": [
          {
            "id": "religious-education-1-0",
            "name": "1.1 The Pattern of Return"
          },
          {
            "id": "religious-education-1-1",
            "name": "1.2 Jesus in Contemporary Culture"
          },
          {
            "id": "religious-education-1-2",
            "name": "2.1 The Impact of Rome"
          },
          {
            "id": "religious-education-1-3",
            "name": "2.2 Evidence for Jesus of Nazareth"
          },
          {
            "id": "religious-education-1-4",
            "name": "2.3 The Teachings of Jesus"
          },
          {
            "id": "religious-education-1-5",
            "name": "2.4 Jesus as Messiah"
          },
          {
            "id": "religious-education-1-6",
            "name": "3.1 Conflict with Establishment"
          },
          {
            "id": "religious-education-1-7",
            "name": "3.2 Death and Resurrection of Jesus"
          },
          {
            "id": "religious-education-1-8",
            "name": "4.1 First Christian Communities"
          },
          {
            "id": "religious-education-1-9",
            "name": "5.1 Interpreting the Message Today"
          },
          {
            "id": "religious-education-1-10",
            "name": "5.2 Trends in Christianity (HL)"
          }
        ]
      },
      {
        "id": "religious-education-2",
        "name": "Section C: World Religions",
        "subtopics": [
          {
            "id": "religious-education-2-0",
            "name": "1.1 Religion as Worldwide Phenomenon"
          },
          {
            "id": "religious-education-2-1",
            "name": "1.2 Primal Religion"
          },
          {
            "id": "religious-education-2-2",
            "name": "1.3 The Holy (HL)"
          },
          {
            "id": "religious-education-2-3",
            "name": "2.1 A Vision of Salvation"
          },
          {
            "id": "religious-education-2-4",
            "name": "2.2 The Community of Believers"
          },
          {
            "id": "religious-education-2-5",
            "name": "2.3 A Celebrating Tradition"
          },
          {
            "id": "religious-education-2-6",
            "name": "2.4 Challenges to the Tradition"
          },
          {
            "id": "religious-education-2-7",
            "name": "2.5 Inter-Faith Dialogue"
          },
          {
            "id": "religious-education-2-8",
            "name": "3.1 Cults and Sects"
          },
          {
            "id": "religious-education-2-9",
            "name": "3.2 New Religious Movements"
          },
          {
            "id": "religious-education-2-10",
            "name": "4.1 A Living Tradition"
          },
          {
            "id": "religious-education-2-11",
            "name": "4.2 Traditions in Dialogue (HL)"
          }
        ]
      },
      {
        "id": "religious-education-3",
        "name": "Section D: Moral Decision-Making",
        "subtopics": [
          {
            "id": "religious-education-3-0",
            "name": "1.1 What Is Morality?"
          },
          {
            "id": "religious-education-3-1",
            "name": "1.2 Why Be Moral?"
          },
          {
            "id": "religious-education-3-2",
            "name": "1.3 Common Good and Freedom"
          },
          {
            "id": "religious-education-3-3",
            "name": "2.1 Morality and Religion"
          },
          {
            "id": "religious-education-3-4",
            "name": "2.2 Morality and Christianity"
          },
          {
            "id": "religious-education-3-5",
            "name": "2.3 Religion on Moral Issues"
          },
          {
            "id": "religious-education-3-6",
            "name": "Part 3: Morality in a Pluralist Society"
          },
          {
            "id": "religious-education-3-7",
            "name": "Part 4: Moral Development"
          }
        ]
      },
      {
        "id": "religious-education-4",
        "name": "Section E: Religion and Gender",
        "subtopics": [
          {
            "id": "religious-education-4-0",
            "name": "1.1 Gender and Society"
          },
          {
            "id": "religious-education-4-1",
            "name": "1.2 Women and Men in Religions"
          },
          {
            "id": "religious-education-4-2",
            "name": "2.1 Gender in the Hebrew Scriptures"
          },
          {
            "id": "religious-education-4-3",
            "name": "2.2 Gender in Christian Tradition"
          },
          {
            "id": "religious-education-4-4",
            "name": "2.3 Changing Views on Mary"
          },
          {
            "id": "religious-education-4-5",
            "name": "2.4 Gender and Empowerment"
          },
          {
            "id": "religious-education-4-6",
            "name": "3.1 Women's Stories"
          }
        ]
      },
      {
        "id": "religious-education-5",
        "name": "Section F: Issues of Justice and Peace",
        "subtopics": [
          {
            "id": "religious-education-5-0",
            "name": "1.1 Social Analysis"
          },
          {
            "id": "religious-education-5-1",
            "name": "1.2 Social Analysis in Action"
          },
          {
            "id": "religious-education-5-2",
            "name": "2.1 Visions of Justice"
          },
          {
            "id": "religious-education-5-3",
            "name": "2.2 Visions of Peace"
          },
          {
            "id": "religious-education-5-4",
            "name": "2.3 Religion on Justice and Peace"
          },
          {
            "id": "religious-education-5-5",
            "name": "2.4 Violence"
          },
          {
            "id": "religious-education-5-6",
            "name": "3.1 The Religious Imperative"
          },
          {
            "id": "religious-education-5-7",
            "name": "3.2 Religion and the Environment"
          }
        ]
      },
      {
        "id": "religious-education-6",
        "name": "Section G: Worship, Prayer and Ritual",
        "subtopics": [
          {
            "id": "religious-education-6-0",
            "name": "1.1 Symbols"
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
            "name": "2.1 The Need for Reflection"
          },
          {
            "id": "religious-education-6-4",
            "name": "2.2 The Human Being as Pray-er"
          },
          {
            "id": "religious-education-6-5",
            "name": "2.3 Contexts for Prayer"
          },
          {
            "id": "religious-education-6-6",
            "name": "2.4 The Praying Tradition"
          },
          {
            "id": "religious-education-6-7",
            "name": "3.1 Meditation"
          },
          {
            "id": "religious-education-6-8",
            "name": "3.2 The Contemplative Traditions"
          },
          {
            "id": "religious-education-6-9",
            "name": "3.3 The Mystic Tradition"
          }
        ]
      },
      {
        "id": "religious-education-7",
        "name": "Section H: The Bible: Literature and Sacred Text",
        "subtopics": [
          {
            "id": "religious-education-7-0",
            "name": "1.1 The Bible as Living Classic"
          },
          {
            "id": "religious-education-7-1",
            "name": "1.2 The Bible as Sacred Text"
          },
          {
            "id": "religious-education-7-2",
            "name": "2.1 Forming the Hebrew Scriptures"
          },
          {
            "id": "religious-education-7-3",
            "name": "2.2 The Gospels"
          },
          {
            "id": "religious-education-7-4",
            "name": "3.1 The Language of Story"
          },
          {
            "id": "religious-education-7-5",
            "name": "3.2 The Language of Reflection"
          },
          {
            "id": "religious-education-7-6",
            "name": "3.3 The Language of Symbol (HL)"
          },
          {
            "id": "religious-education-7-7",
            "name": "4.1 The Hebrew Scriptures"
          },
          {
            "id": "religious-education-7-8",
            "name": "4.2 The New Testament"
          }
        ]
      },
      {
        "id": "religious-education-8",
        "name": "Section I: Religion: the Irish Experience",
        "subtopics": [
          {
            "id": "religious-education-8-0",
            "name": "Part 1: Patterns of Change"
          },
          {
            "id": "religious-education-8-1",
            "name": "2.1 Local Evidence"
          },
          {
            "id": "religious-education-8-2",
            "name": "2.2 National Evidence"
          },
          {
            "id": "religious-education-8-3",
            "name": "3.1 The Coming of Patrick"
          },
          {
            "id": "religious-education-8-4",
            "name": "3.2 Spirituality and Land"
          },
          {
            "id": "religious-education-8-5",
            "name": "3.3 Spirituality and Monasticism"
          },
          {
            "id": "religious-education-8-6",
            "name": "3.4 Spirituality and Reforms"
          },
          {
            "id": "religious-education-8-7",
            "name": "3.5 Religion and the Enlightenment"
          },
          {
            "id": "religious-education-8-8",
            "name": "3.6 Religion in Modern Ireland"
          }
        ]
      },
      {
        "id": "religious-education-9",
        "name": "Section J: Religion and Science",
        "subtopics": [
          {
            "id": "religious-education-9-0",
            "name": "Part 1: Science and Theology"
          },
          {
            "id": "religious-education-9-1",
            "name": "2.1 Separate Ways (Galileo)"
          },
          {
            "id": "religious-education-9-2",
            "name": "2.2 In Tension (Darwin)"
          },
          {
            "id": "religious-education-9-3",
            "name": "2.3 In Dialogue: Ecological Crisis"
          },
          {
            "id": "religious-education-9-4",
            "name": "2.4 In Dialogue: Creation"
          },
          {
            "id": "religious-education-9-5",
            "name": "3.1 The Debate About Origins"
          },
          {
            "id": "religious-education-9-6",
            "name": "3.2 New Physics and Religion (HL)"
          },
          {
            "id": "religious-education-9-7",
            "name": "4.1 Fundamental Issues"
          },
          {
            "id": "religious-education-9-8",
            "name": "4.2 Specific Topics (HL)"
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
        "name": "Research Strand",
        "subtopics": [
          {
            "id": "art-0-0",
            "name": "1.1 Looking"
          },
          {
            "id": "art-0-1",
            "name": "1.2 Recording and Documenting"
          },
          {
            "id": "art-0-2",
            "name": "1.3 Experimenting and Interpreting"
          },
          {
            "id": "art-0-3",
            "name": "1.4 Contextual Enquiries"
          },
          {
            "id": "art-0-4",
            "name": "1.5 Process"
          }
        ]
      },
      {
        "id": "art-1",
        "name": "Create Strand",
        "subtopics": [
          {
            "id": "art-1-0",
            "name": "2.1 Making"
          },
          {
            "id": "art-1-1",
            "name": "2.2 Contextual Enquiries"
          },
          {
            "id": "art-1-2",
            "name": "2.3 Process"
          },
          {
            "id": "art-1-3",
            "name": "2.4 Realisation and Presenting"
          }
        ]
      },
      {
        "id": "art-2",
        "name": "Respond Strand",
        "subtopics": [
          {
            "id": "art-2-0",
            "name": "3.1 Analysis"
          },
          {
            "id": "art-2-1",
            "name": "3.2 Contextual Enquiries"
          },
          {
            "id": "art-2-2",
            "name": "3.3 Impact and Value"
          },
          {
            "id": "art-2-3",
            "name": "3.4 Critical and Personal Reflection"
          },
          {
            "id": "art-2-4",
            "name": "3.5 Process"
          }
        ]
      },
      {
        "id": "art-3",
        "name": "Visual Studies Framework",
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
        "name": "Content Area 1: Europe and the World",
        "subtopics": [
          {
            "id": "art-4-0",
            "name": "Romanesque and Gothic"
          },
          {
            "id": "art-4-1",
            "name": "The Renaissance and Mannerism (Proto, Early, High)"
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
            "name": "Post 1960s Art"
          },
          {
            "id": "art-4-6",
            "name": "Europe and the World: Generic Questions"
          }
        ]
      },
      {
        "id": "art-5",
        "name": "Content Area 2: Ireland and the World",
        "subtopics": [
          {
            "id": "art-5-0",
            "name": "Pre-Christian Ireland (c. 4,000 BCE - 500 CE)"
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
            "name": "Georgian Period"
          },
          {
            "id": "art-5-4",
            "name": "Irish Art and Modernism"
          },
          {
            "id": "art-5-5",
            "name": "Post 1960s Art in Ireland"
          }
        ]
      },
      {
        "id": "art-6",
        "name": "Content Area 3: Today's World",
        "subtopics": [
          {
            "id": "art-6-0",
            "name": "Artists: Theory and Thinking"
          },
          {
            "id": "art-6-1",
            "name": "Artists: Processes and Media"
          },
          {
            "id": "art-6-2",
            "name": "Art as Social Commentary or Commentator"
          },
          {
            "id": "art-6-3",
            "name": "Art and the Environment"
          },
          {
            "id": "art-6-4",
            "name": "Today's World: Generic Questions"
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
            "name": "Solo Singing or Playing"
          },
          {
            "id": "music-0-1",
            "name": "Performing in a Group"
          },
          {
            "id": "music-0-2",
            "name": "Rehearsing and Conducting"
          },
          {
            "id": "music-0-3",
            "name": "Prepared Songs or Pieces"
          },
          {
            "id": "music-0-4",
            "name": "Sight Reading Test"
          },
          {
            "id": "music-0-5",
            "name": "Aural Memory Test"
          },
          {
            "id": "music-0-6",
            "name": "Unprepared Improvisation"
          },
          {
            "id": "music-0-7",
            "name": "Accompaniments"
          },
          {
            "id": "music-0-8",
            "name": "Traditional Irish Ornamentation"
          },
          {
            "id": "music-0-9",
            "name": "Music Technology Performance"
          },
          {
            "id": "music-0-10",
            "name": "Fluency and Group Performing"
          },
          {
            "id": "music-0-11",
            "name": "Choosing Repertoire"
          },
          {
            "id": "music-0-12",
            "name": "Higher Elective in Performing"
          }
        ]
      },
      {
        "id": "music-1",
        "name": "Composing",
        "subtopics": [
          {
            "id": "music-1-0",
            "name": "Rudiments and Notation"
          },
          {
            "id": "music-1-1",
            "name": "Time Signatures and Keys"
          },
          {
            "id": "music-1-2",
            "name": "Root Position Chord Progressions"
          },
          {
            "id": "music-1-3",
            "name": "First Inversion Chords"
          },
          {
            "id": "music-1-4",
            "name": "Dominant 7th and Cadential 6/4 Chords"
          },
          {
            "id": "music-1-5",
            "name": "Modulation and Non-Chord Notes"
          },
          {
            "id": "music-1-6",
            "name": "Melody Writing"
          },
          {
            "id": "music-1-7",
            "name": "Harmony Exercises (Ordinary)"
          },
          {
            "id": "music-1-8",
            "name": "Harmony Exercises (Higher)"
          },
          {
            "id": "music-1-9",
            "name": "Higher Elective in Composing"
          },
          {
            "id": "music-1-10",
            "name": "Melody: Continuation of a Given Opening"
          },
          {
            "id": "music-1-11",
            "name": "Melody: Setting Music to a Given Text"
          },
          {
            "id": "music-1-12",
            "name": "Melody: Composing to a Given Dance Rhythm or Metre"
          },
          {
            "id": "music-1-13",
            "name": "Harmony: Adding Bass and Chords to a Tune"
          },
          {
            "id": "music-1-14",
            "name": "Harmony: Composing Melody and Bass from Chords"
          },
          {
            "id": "music-1-15",
            "name": "Harmony: Adding a Countermelody/Descant and Chords"
          }
        ]
      },
      {
        "id": "music-2",
        "name": "Listening",
        "subtopics": [
          {
            "id": "music-2-0",
            "name": "Prescribed Works (Set Works)"
          },
          {
            "id": "music-2-1",
            "name": "Comparing Interpretations"
          },
          {
            "id": "music-2-2",
            "name": "Irish Traditional Music"
          },
          {
            "id": "music-2-3",
            "name": "Aural Skills: Notation"
          },
          {
            "id": "music-2-4",
            "name": "Aural: Melody, Rhythm and Timbre"
          },
          {
            "id": "music-2-5",
            "name": "Simple Musical Structures"
          },
          {
            "id": "music-2-6",
            "name": "Higher Aural Skills"
          },
          {
            "id": "music-2-7",
            "name": "General Listening (Unprepared)"
          },
          {
            "id": "music-2-8",
            "name": "Higher Elective in Listening"
          },
          {
            "id": "music-2-9",
            "name": "Set Work: Mozart — Piano Concerto No. 23"
          },
          {
            "id": "music-2-10",
            "name": "Set Work: Berlioz — Symphonie Fantastique"
          },
          {
            "id": "music-2-11",
            "name": "Set Work: Deane — Seachanges (with Danse Macabre)"
          },
          {
            "id": "music-2-12",
            "name": "Set Work: The Beatles — Sgt. Pepper's Lonely Hearts Club Band"
          },
          {
            "id": "music-2-13",
            "name": "Irish Music Essay"
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
            "name": "Orthographic and Auxiliary Projection"
          },
          {
            "id": "design-and-communication-graphics-0-2",
            "name": "Axonometric Projection (Isometric, Dimetric, Trimetric)"
          },
          {
            "id": "design-and-communication-graphics-0-3",
            "name": "Perspective Drawing"
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
            "name": "Descriptive Geometry: Lines and Planes"
          },
          {
            "id": "design-and-communication-graphics-0-7",
            "name": "Developments and Envelopments"
          },
          {
            "id": "design-and-communication-graphics-0-8",
            "name": "Interpenetration (Intersection of Solids)"
          },
          {
            "id": "design-and-communication-graphics-0-9",
            "name": "Skew Lines"
          },
          {
            "id": "design-and-communication-graphics-0-10",
            "name": "The Oblique Plane"
          },
          {
            "id": "design-and-communication-graphics-0-11",
            "name": "Intersecting Planes (Lamina Planes)"
          },
          {
            "id": "design-and-communication-graphics-0-12",
            "name": "Solids in Contact"
          },
          {
            "id": "design-and-communication-graphics-0-13",
            "name": "Rotation and Inclination of Solids"
          },
          {
            "id": "design-and-communication-graphics-0-14",
            "name": "Tetrahedron"
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
            "name": "ICT: CAD Modelling and Applications"
          },
          {
            "id": "design-and-communication-graphics-1-4",
            "name": "ICT and Graphics"
          },
          {
            "id": "design-and-communication-graphics-1-5",
            "name": "Student Assignment"
          }
        ]
      },
      {
        "id": "design-and-communication-graphics-2",
        "name": "Applied Graphics (Optional Areas)",
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
        "name": "Part 1: Construction Theory & Drawings",
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
            "name": "Services, External Works & Drainage"
          },
          {
            "id": "construction-studies-0-5",
            "name": "Heat & Thermal Effects"
          },
          {
            "id": "construction-studies-0-6",
            "name": "Illumination & Light in Buildings"
          },
          {
            "id": "construction-studies-0-7",
            "name": "Sound in Buildings"
          },
          {
            "id": "construction-studies-0-8",
            "name": "Sustainability, Passive House & U-Values"
          },
          {
            "id": "construction-studies-0-9",
            "name": "Foundations"
          },
          {
            "id": "construction-studies-0-10",
            "name": "Walls"
          },
          {
            "id": "construction-studies-0-11",
            "name": "Floors"
          },
          {
            "id": "construction-studies-0-12",
            "name": "Roofs"
          },
          {
            "id": "construction-studies-0-13",
            "name": "Windows and Doors"
          },
          {
            "id": "construction-studies-0-14",
            "name": "Stairs"
          },
          {
            "id": "construction-studies-0-15",
            "name": "Fireplaces and Fire Prevention"
          },
          {
            "id": "construction-studies-0-16",
            "name": "Site Safety"
          },
          {
            "id": "construction-studies-0-17",
            "name": "Condensation and Air Tightness"
          },
          {
            "id": "construction-studies-0-18",
            "name": "Hot Water and Space Heating"
          },
          {
            "id": "construction-studies-0-19",
            "name": "Wood, Rot and Ventilation"
          },
          {
            "id": "construction-studies-0-20",
            "name": "Conservation and Restoration"
          },
          {
            "id": "construction-studies-0-21",
            "name": "Question 1: Drawing Questions"
          }
        ]
      },
      {
        "id": "construction-studies-1",
        "name": "Part 2: Practical Skills",
        "subtopics": [
          {
            "id": "construction-studies-1-0",
            "name": "Tools"
          },
          {
            "id": "construction-studies-1-1",
            "name": "Processes & Craft Practices"
          }
        ]
      },
      {
        "id": "construction-studies-2",
        "name": "Part 3: Course Work & Projects",
        "subtopics": [
          {
            "id": "construction-studies-2-0",
            "name": "Project Options"
          },
          {
            "id": "construction-studies-2-1",
            "name": "Workshop/Laboratory Course Work"
          },
          {
            "id": "construction-studies-2-2",
            "name": "Building Science: Timber & Adhesives"
          },
          {
            "id": "construction-studies-2-3",
            "name": "Building Science: Porosity & Durability"
          },
          {
            "id": "construction-studies-2-4",
            "name": "Building Science: Aggregates & Concrete"
          },
          {
            "id": "construction-studies-2-5",
            "name": "Building Science: Binders & Setting"
          },
          {
            "id": "construction-studies-2-6",
            "name": "Building Science: Paints & Pigments"
          },
          {
            "id": "construction-studies-2-7",
            "name": "Building Science: Water & Comfort"
          },
          {
            "id": "construction-studies-2-8",
            "name": "Building Science: Heat"
          },
          {
            "id": "construction-studies-2-9",
            "name": "Building Science: Light"
          },
          {
            "id": "construction-studies-2-10",
            "name": "Building Science: Electricity"
          },
          {
            "id": "construction-studies-2-11",
            "name": "Building Science: Acoustics"
          },
          {
            "id": "construction-studies-2-12",
            "name": "Portfolio Design Folio & Three Building Experiments"
          }
        ]
      },
      {
        "id": "construction-studies-3",
        "name": "Appendix 1: LCVP (Optional)",
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
            "name": "Work Environment"
          },
          {
            "id": "engineering-0-1",
            "name": "Personal Protection"
          },
          {
            "id": "engineering-0-2",
            "name": "Hand-Tools"
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
            "name": "Marking Out and Measurement"
          },
          {
            "id": "engineering-1-1",
            "name": "Shaping"
          },
          {
            "id": "engineering-1-2",
            "name": "Bending and Folding"
          },
          {
            "id": "engineering-1-3",
            "name": "Surface Finish"
          },
          {
            "id": "engineering-1-4",
            "name": "Lathe"
          },
          {
            "id": "engineering-1-5",
            "name": "Cutting Tool Geometry"
          },
          {
            "id": "engineering-1-6",
            "name": "Drilling Machine and Operations"
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
          },
          {
            "id": "engineering-1-12",
            "name": "Q2 Special Topic (Announced Annually)"
          },
          {
            "id": "engineering-1-13",
            "name": "Inventors and Engineers in Society"
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
            "name": "Origin and Production of Materials"
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
          },
          {
            "id": "engineering-2-7",
            "name": "Equilibrium Diagrams"
          }
        ]
      },
      {
        "id": "engineering-3",
        "name": "Core: Drawing and Design",
        "subtopics": [
          {
            "id": "engineering-3-0",
            "name": "Freehand Sketching"
          },
          {
            "id": "engineering-3-1",
            "name": "Orthographic Drawing"
          },
          {
            "id": "engineering-3-2",
            "name": "Pictorial Drawing"
          },
          {
            "id": "engineering-3-3",
            "name": "Geometric Drawing"
          },
          {
            "id": "engineering-3-4",
            "name": "Presentation and Reporting"
          },
          {
            "id": "engineering-3-5",
            "name": "Framework for Designing"
          },
          {
            "id": "engineering-3-6",
            "name": "Product Design"
          }
        ]
      },
      {
        "id": "engineering-4",
        "name": "Core: Computer Aided Processes (CAD/CAM)",
        "subtopics": [
          {
            "id": "engineering-4-0",
            "name": "Drawing Functions"
          },
          {
            "id": "engineering-4-1",
            "name": "CAM Part Program"
          },
          {
            "id": "engineering-4-2",
            "name": "CAM Simulation"
          },
          {
            "id": "engineering-4-3",
            "name": "Computer Terminology"
          },
          {
            "id": "engineering-4-4",
            "name": "CAD Hardware"
          },
          {
            "id": "engineering-4-5",
            "name": "CAM Principles"
          },
          {
            "id": "engineering-4-6",
            "name": "CAM Co-Ordinates"
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
            "name": "Cells and Batteries"
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
            "name": "Electronic Circuits"
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
            "name": "Sensitive Circuits"
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
            "name": "Pulleys and Belt Drives"
          },
          {
            "id": "engineering-7-3",
            "name": "Gears and Gearing"
          },
          {
            "id": "engineering-7-4",
            "name": "Cams and Followers"
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
            "name": "Terminology and Symbols"
          },
          {
            "id": "engineering-8-3",
            "name": "Supply and Distribution"
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
            "name": "Drawing Functions"
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
            "name": "Printing or Plotting"
          },
          {
            "id": "engineering-9-5",
            "name": "Computer Aided Machining (CAM)"
          },
          {
            "id": "engineering-9-6",
            "name": "Drive System for CAM"
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
            "name": "Beaten Metalwork"
          },
          {
            "id": "engineering-10-3",
            "name": "Jewellery Techniques"
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
            "name": "Surface Treatment and Finishes"
          },
          {
            "id": "engineering-10-7",
            "name": "Edge Finishing"
          },
          {
            "id": "engineering-10-8",
            "name": "Hot and Cold Forming"
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
        "name": "Option: Power, Energy and Control",
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
            "name": "Control Device"
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
            "name": "Efficiency of Systems"
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
            "name": "Hot Forming of Metal"
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
            "name": "Materials Testing"
          },
          {
            "id": "engineering-13-5",
            "name": "Origin and Production of Materials"
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
            "name": "Identifying and Analysing Problems"
          },
          {
            "id": "technology-0-2",
            "name": "Recognising Constraints"
          },
          {
            "id": "technology-0-3",
            "name": "Investigation and Research"
          },
          {
            "id": "technology-0-4",
            "name": "Generating Ideas"
          },
          {
            "id": "technology-0-5",
            "name": "Presenting Ideas"
          },
          {
            "id": "technology-0-6",
            "name": "Developing the Chosen Idea"
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
            "name": "Presenting the Design Folio"
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
            "name": "Presenting Information"
          },
          {
            "id": "technology-3-7",
            "name": "Producing the Report"
          }
        ]
      },
      {
        "id": "technology-4",
        "name": "Core: ICT",
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
            "name": "Intro to Robotic Control"
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
        "name": "Option: ICT",
        "subtopics": [
          {
            "id": "technology-9-0",
            "name": "Computer Architecture"
          },
          {
            "id": "technology-9-1",
            "name": "Data Communications and Networks"
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
        "name": "Strand 1: Towards Optimum Performance",
        "subtopics": [
          {
            "id": "physical-education-0-0",
            "name": "Topic 1: Learning and Improving Skill and Technique"
          },
          {
            "id": "physical-education-0-1",
            "name": "1.1 Defining a Skilled Performance"
          },
          {
            "id": "physical-education-0-2",
            "name": "1.2 Analysing Skill and Technique"
          },
          {
            "id": "physical-education-0-3",
            "name": "1.3 Skill Acquisition"
          },
          {
            "id": "physical-education-0-4",
            "name": "Topic 2: Demands of Performance"
          },
          {
            "id": "physical-education-0-5",
            "name": "2.1 Physical Fitness"
          },
          {
            "id": "physical-education-0-6",
            "name": "2.2 Health-Related Fitness"
          },
          {
            "id": "physical-education-0-7",
            "name": "2.3 Performance-Related Fitness"
          },
          {
            "id": "physical-education-0-8",
            "name": "2.4 Applying Fitness Components"
          },
          {
            "id": "physical-education-0-9",
            "name": "2.5 Assessing Physical Fitness"
          },
          {
            "id": "physical-education-0-10",
            "name": "2.6 Designing a Fitness Plan"
          },
          {
            "id": "physical-education-0-11",
            "name": "2.7 Psychological Preparation"
          },
          {
            "id": "physical-education-0-12",
            "name": "2.8 Diet and Nutrition"
          },
          {
            "id": "physical-education-0-13",
            "name": "Topic 3: Structures, Strategies, Roles and Conventions"
          },
          {
            "id": "physical-education-0-14",
            "name": "3.1 Structures and Strategies"
          },
          {
            "id": "physical-education-0-15",
            "name": "3.2 Roles and Relationships"
          },
          {
            "id": "physical-education-0-16",
            "name": "3.3 Safe Practice"
          },
          {
            "id": "physical-education-0-17",
            "name": "3.4 Rules, Rituals and Conventions"
          },
          {
            "id": "physical-education-0-18",
            "name": "3.5 Role of Coach/Choreographer"
          },
          {
            "id": "physical-education-0-19",
            "name": "3.6 Role of Official"
          },
          {
            "id": "physical-education-0-20",
            "name": "Topic 4: Planning for Performance"
          },
          {
            "id": "physical-education-0-21",
            "name": "4.1 Personal Performance Analysis"
          },
          {
            "id": "physical-education-0-22",
            "name": "4.2 Methods of Analysis"
          },
          {
            "id": "physical-education-0-23",
            "name": "4.3 Aesthetic and Artistic Aspects"
          },
          {
            "id": "physical-education-0-24",
            "name": "4.4 Planning for Optimum Performance"
          }
        ]
      },
      {
        "id": "physical-education-1",
        "name": "Strand 2: Contemporary Issues",
        "subtopics": [
          {
            "id": "physical-education-1-0",
            "name": "Topic 5: Promoting Physical Activity (Compulsory)"
          },
          {
            "id": "physical-education-1-1",
            "name": "5.1 Benefits of Participation"
          },
          {
            "id": "physical-education-1-2",
            "name": "5.2 Activity Participation"
          },
          {
            "id": "physical-education-1-3",
            "name": "5.3 Activity Promotion"
          },
          {
            "id": "physical-education-1-4",
            "name": "5.4 Pathways to Excellence"
          },
          {
            "id": "physical-education-1-5",
            "name": "Topic 6: Ethics and Fair Play (Compulsory)"
          },
          {
            "id": "physical-education-1-6",
            "name": "6.1 Principles of Ethical Practice"
          },
          {
            "id": "physical-education-1-7",
            "name": "6.2 Codes of Ethics"
          },
          {
            "id": "physical-education-1-8",
            "name": "6.3 Drugs and Sport"
          },
          {
            "id": "physical-education-1-9",
            "name": "6.4 Anti-Doping Rules"
          },
          {
            "id": "physical-education-1-10",
            "name": "6.5 Best Practice for Supplements"
          },
          {
            "id": "physical-education-1-11",
            "name": "Topic 7: Physical Activity and Inclusion (Prescribed - 2 of 4 examined)"
          },
          {
            "id": "physical-education-1-12",
            "name": "7.1 Supports and Barriers by Group"
          },
          {
            "id": "physical-education-1-13",
            "name": "7.2 Addressing Barriers"
          },
          {
            "id": "physical-education-1-14",
            "name": "7.3 Developments Over 20 Years"
          },
          {
            "id": "physical-education-1-15",
            "name": "7.4 Adapted Physical Activity"
          },
          {
            "id": "physical-education-1-16",
            "name": "Topic 8: Technology, Media and Sport (Prescribed - 2 of 4 examined)"
          },
          {
            "id": "physical-education-1-17",
            "name": "8.1 Impact of Technology on Sport"
          },
          {
            "id": "physical-education-1-18",
            "name": "8.2 Media in Sport"
          },
          {
            "id": "physical-education-1-19",
            "name": "Topic 9: Gender and Physical Activity (Prescribed - 2 of 4 examined)"
          },
          {
            "id": "physical-education-1-20",
            "name": "9.1 Gender, Sport and Activity"
          },
          {
            "id": "physical-education-1-21",
            "name": "9.2 Gender, Media and Body Image"
          },
          {
            "id": "physical-education-1-22",
            "name": "9.3 Gender Socialisation"
          },
          {
            "id": "physical-education-1-23",
            "name": "Topic 10: Business and Enterprise in Physical Activity and Sport (Prescribed - 2 of 4 examined)"
          },
          {
            "id": "physical-education-1-24",
            "name": "10.1 Sponsorship and Advertising"
          },
          {
            "id": "physical-education-1-25",
            "name": "10.2 The Business Dimension"
          },
          {
            "id": "physical-education-1-26",
            "name": "10.3 Mass Participation in Sport"
          },
          {
            "id": "physical-education-1-27",
            "name": "10.4 Tourism and Sport"
          }
        ]
      },
      {
        "id": "physical-education-2",
        "name": "Physical Activity Areas",
        "subtopics": [
          {
            "id": "physical-education-2-0",
            "name": "Adventure Activities"
          },
          {
            "id": "physical-education-2-1",
            "name": "Artistic and Aesthetic Activities"
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
            "name": "Personal Exercise and Fitness"
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
            "name": "Unit 1: Introduction to Working Life"
          },
          {
            "id": "lcvp-link-modules-0-1",
            "name": "Unit 2: Job Seeking Skills"
          },
          {
            "id": "lcvp-link-modules-0-2",
            "name": "Unit 3: Career Investigation (core portfolio item)"
          },
          {
            "id": "lcvp-link-modules-0-3",
            "name": "Unit 4: Work Placement"
          },
          {
            "id": "lcvp-link-modules-0-4",
            "name": "Unit 5: Curriculum Vitae & Summary Report (core portfolio items)"
          }
        ]
      },
      {
        "id": "lcvp-link-modules-1",
        "name": "Link Module 2: Enterprise Education",
        "subtopics": [
          {
            "id": "lcvp-link-modules-1-0",
            "name": "Unit 1: Enterprise Skills"
          },
          {
            "id": "lcvp-link-modules-1-1",
            "name": "Unit 2: Local Business Enterprises"
          },
          {
            "id": "lcvp-link-modules-1-2",
            "name": "Unit 3: Local Voluntary Organisations"
          },
          {
            "id": "lcvp-link-modules-1-3",
            "name": "Unit 4: An Enterprise Activity (Enterprise Report / Action Plan)"
          },
          {
            "id": "lcvp-link-modules-1-4",
            "name": "Unit 5: Work Experience Diary, My Own Place & Recorded Interview (optional portfolio items)"
          }
        ]
      }
    ]
  },
  {
    "id": "home-economics",
    "name": "Home Economics",
    "category": "practical-applied",
    "levels": [
      "higher",
      "ordinary"
    ],
    "strands": [
      {
        "id": "home-economics-0",
        "name": "Food Studies",
        "subtopics": [
          {
            "id": "home-economics-0-0",
            "name": "Food & Nutrition"
          },
          {
            "id": "home-economics-0-1",
            "name": "Diet & Health"
          },
          {
            "id": "home-economics-0-2",
            "name": "Food Science & Properties of Food"
          },
          {
            "id": "home-economics-0-3",
            "name": "Culinary Skills & Food Preparation"
          },
          {
            "id": "home-economics-0-4",
            "name": "Food Spoilage, Safety & Hygiene (incl. Legislation)"
          },
          {
            "id": "home-economics-0-5",
            "name": "Nutrition: Protein"
          },
          {
            "id": "home-economics-0-6",
            "name": "Nutrition: Carbohydrates"
          },
          {
            "id": "home-economics-0-7",
            "name": "Nutrition: Lipids (Fats)"
          },
          {
            "id": "home-economics-0-8",
            "name": "Nutrition: Vitamins, Minerals & Water"
          },
          {
            "id": "home-economics-0-9",
            "name": "Food Commodities (Meat, Fish, Cereals, Fruit & Veg, Dairy, Eggs)"
          },
          {
            "id": "home-economics-0-10",
            "name": "Meal Planning & Preparation"
          },
          {
            "id": "home-economics-0-11",
            "name": "The Food Industry & Packaging"
          }
        ]
      },
      {
        "id": "home-economics-1",
        "name": "Resource Management & Consumer Studies",
        "subtopics": [
          {
            "id": "home-economics-1-0",
            "name": "Family Resource Management"
          },
          {
            "id": "home-economics-1-1",
            "name": "Household Financial Management"
          },
          {
            "id": "home-economics-1-2",
            "name": "Consumer Studies"
          },
          {
            "id": "home-economics-1-3",
            "name": "Household Technology & Energy"
          },
          {
            "id": "home-economics-1-4",
            "name": "Household Textiles (Core)"
          },
          {
            "id": "home-economics-1-5",
            "name": "The Environment & Sustainable Living"
          }
        ]
      },
      {
        "id": "home-economics-2",
        "name": "Social Studies",
        "subtopics": [
          {
            "id": "home-economics-2-0",
            "name": "The Family in Society"
          },
          {
            "id": "home-economics-2-1",
            "name": "Marriage & the Family Life Cycle"
          },
          {
            "id": "home-economics-2-2",
            "name": "Education, Work & Leisure in Society"
          },
          {
            "id": "home-economics-2-3",
            "name": "Older People & the Family (Care Provision)"
          }
        ]
      },
      {
        "id": "home-economics-3",
        "name": "Electives",
        "subtopics": [
          {
            "id": "home-economics-3-0",
            "name": "Home Design & Management"
          },
          {
            "id": "home-economics-3-1",
            "name": "Textiles, Fashion & Design"
          },
          {
            "id": "home-economics-3-2",
            "name": "Social Studies (elective)"
          },
          {
            "id": "home-economics-3-3",
            "name": "Elective 1: Housing Provision & Planning"
          },
          {
            "id": "home-economics-3-4",
            "name": "Elective 1: Interior Design"
          },
          {
            "id": "home-economics-3-5",
            "name": "Elective 1: Household Services (Heating, Water, Lighting)"
          },
          {
            "id": "home-economics-3-6",
            "name": "Elective 1: Energy & Emissions"
          },
          {
            "id": "home-economics-3-7",
            "name": "Elective 2: Fabrics & Fibres"
          },
          {
            "id": "home-economics-3-8",
            "name": "Elective 2: Patterns & Fashion"
          },
          {
            "id": "home-economics-3-9",
            "name": "Elective 3: Unemployment & Poverty"
          },
          {
            "id": "home-economics-3-10",
            "name": "Elective 3: Education in Ireland"
          },
          {
            "id": "home-economics-3-11",
            "name": "Elective 3: Family Life & Leisure"
          }
        ]
      }
    ]
  },
  {
    "id": "jc-english",
    "name": "English (Junior Cycle)",
    "category": "language",
    "levels": [
      "higher",
      "ordinary"
    ],
    "strands": [
      {
        "id": "jc-english-0",
        "name": "Oral Language",
        "subtopics": [
          {
            "id": "jc-english-0-0",
            "name": "Spoken Communication and Presentation"
          },
          {
            "id": "jc-english-0-1",
            "name": "Discussion, Debate and Persuasion"
          },
          {
            "id": "jc-english-0-2",
            "name": "Influence and Register of Spoken Language"
          }
        ]
      },
      {
        "id": "jc-english-1",
        "name": "Reading",
        "subtopics": [
          {
            "id": "jc-english-1-0",
            "name": "Reading Comprehension (Unseen Texts)"
          },
          {
            "id": "jc-english-1-1",
            "name": "Studied Fiction (Novel and Short Story)"
          },
          {
            "id": "jc-english-1-2",
            "name": "Studied Drama and Shakespeare"
          },
          {
            "id": "jc-english-1-3",
            "name": "Poetry (Studied and Unseen)"
          },
          {
            "id": "jc-english-1-4",
            "name": "Film Studies"
          },
          {
            "id": "jc-english-1-5",
            "name": "Responding to Texts (Theme, Character, Author's Craft)"
          },
          {
            "id": "jc-english-1-6",
            "name": "Visual Literacy (Posters, Advertisements & Images)"
          }
        ]
      },
      {
        "id": "jc-english-2",
        "name": "Writing",
        "subtopics": [
          {
            "id": "jc-english-2-0",
            "name": "Functional and Transactional Writing"
          },
          {
            "id": "jc-english-2-1",
            "name": "Personal and Creative Writing"
          },
          {
            "id": "jc-english-2-2",
            "name": "Writing About Studied Texts"
          },
          {
            "id": "jc-english-2-3",
            "name": "Language, Grammar and Structure"
          }
        ]
      }
    ]
  },
  {
    "id": "jc-irish",
    "name": "Irish (Junior Cycle, Gaeilge T2)",
    "category": "language",
    "levels": [
      "higher",
      "ordinary"
    ],
    "strands": [
      {
        "id": "jc-irish-0",
        "name": "Cumas Cumarsáide (Communicative Competence)",
        "subtopics": [
          {
            "id": "jc-irish-0-0",
            "name": "Éisteacht: Cluastuiscint (Listening)"
          },
          {
            "id": "jc-irish-0-1",
            "name": "Léamhthuiscint (Reading Comprehension)"
          },
          {
            "id": "jc-irish-0-2",
            "name": "Litríocht (Studied Literature)"
          },
          {
            "id": "jc-irish-0-3",
            "name": "Ceapadóireacht (Writing and Composition)"
          },
          {
            "id": "jc-irish-0-4",
            "name": "Labhairt agus Idirghníomhú Cainte (Speaking and Interaction)"
          }
        ]
      },
      {
        "id": "jc-irish-1",
        "name": "Feasacht Teanga agus Chultúrtha (Language and Cultural Awareness)",
        "subtopics": [
          {
            "id": "jc-irish-1-0",
            "name": "Cruinneas na Teanga (Language Accuracy: Séimhiú, Urú, Aimsirí)"
          },
          {
            "id": "jc-irish-1-1",
            "name": "Feasacht Chultúrtha (Cultural Awareness)"
          },
          {
            "id": "jc-irish-1-2",
            "name": "Feasacht ar an Dátheangachas (Bilingualism Awareness)"
          }
        ]
      },
      {
        "id": "jc-irish-2",
        "name": "Féinfheasacht an Fhoghlaimeora (Learner Self-Awareness)",
        "subtopics": [
          {
            "id": "jc-irish-2-0",
            "name": "Foghlaim Féinriartha (Self-Directed Learning)"
          },
          {
            "id": "jc-irish-2-1",
            "name": "Spreagadh Pearsanta i leith na Teanga (Personal Motivation)"
          }
        ]
      }
    ]
  },
  {
    "id": "jc-mathematics",
    "name": "Mathematics (Junior Cycle)",
    "category": "stem",
    "levels": [
      "higher",
      "ordinary"
    ],
    "strands": [
      {
        "id": "jc-mathematics-0",
        "name": "Unifying strand (mathematical skills)",
        "subtopics": [
          {
            "id": "jc-mathematics-0-0",
            "name": "Building blocks (core concepts & procedures)"
          },
          {
            "id": "jc-mathematics-0-1",
            "name": "Representation (showing maths different ways)"
          },
          {
            "id": "jc-mathematics-0-2",
            "name": "Connections (within maths and to the real world)"
          },
          {
            "id": "jc-mathematics-0-3",
            "name": "Problem solving"
          },
          {
            "id": "jc-mathematics-0-4",
            "name": "Generalisation and proof"
          },
          {
            "id": "jc-mathematics-0-5",
            "name": "Communication (justifying & explaining)"
          }
        ]
      },
      {
        "id": "jc-mathematics-1",
        "name": "Number",
        "subtopics": [
          {
            "id": "jc-mathematics-1-0",
            "name": "Number systems & arithmetic operations"
          },
          {
            "id": "jc-mathematics-1-1",
            "name": "Indices & scientific notation"
          },
          {
            "id": "jc-mathematics-1-2",
            "name": "Factors, multiples & primes"
          },
          {
            "id": "jc-mathematics-1-3",
            "name": "Rounding & accuracy"
          },
          {
            "id": "jc-mathematics-1-4",
            "name": "Fractions, decimals & percentages"
          },
          {
            "id": "jc-mathematics-1-5",
            "name": "Ratio & proportion"
          },
          {
            "id": "jc-mathematics-1-6",
            "name": "Financial maths (money problems)"
          },
          {
            "id": "jc-mathematics-1-7",
            "name": "Sets & Venn diagrams"
          },
          {
            "id": "jc-mathematics-1-8",
            "name": "Distance, speed & time (incl. real-life graphs)"
          }
        ]
      },
      {
        "id": "jc-mathematics-2",
        "name": "Geometry and trigonometry",
        "subtopics": [
          {
            "id": "jc-mathematics-2-0",
            "name": "Measure, units & time"
          },
          {
            "id": "jc-mathematics-2-1",
            "name": "2D shapes: perimeter & area"
          },
          {
            "id": "jc-mathematics-2-2",
            "name": "3D solids: nets, volume & surface area"
          },
          {
            "id": "jc-mathematics-2-3",
            "name": "Geometric reasoning, theorems & constructions"
          },
          {
            "id": "jc-mathematics-2-4",
            "name": "Right-angled triangles & trigonometry"
          },
          {
            "id": "jc-mathematics-2-5",
            "name": "Co-ordinate geometry of the line"
          },
          {
            "id": "jc-mathematics-2-6",
            "name": "Transformations & symmetry"
          }
        ]
      },
      {
        "id": "jc-mathematics-3",
        "name": "Algebra and functions",
        "subtopics": [
          {
            "id": "jc-mathematics-3-0",
            "name": "Patterns, sequences & the nth term"
          },
          {
            "id": "jc-mathematics-3-1",
            "name": "Expressions, variables & equality"
          },
          {
            "id": "jc-mathematics-3-2",
            "name": "Manipulating expressions & factorising"
          },
          {
            "id": "jc-mathematics-3-3",
            "name": "Solving equations"
          },
          {
            "id": "jc-mathematics-3-4",
            "name": "Inequalities"
          },
          {
            "id": "jc-mathematics-3-5",
            "name": "Rearranging formulae"
          },
          {
            "id": "jc-mathematics-3-6",
            "name": "Functions & graphs"
          }
        ]
      },
      {
        "id": "jc-mathematics-4",
        "name": "Statistics and probability",
        "subtopics": [
          {
            "id": "jc-mathematics-4-0",
            "name": "Counting & sample spaces"
          },
          {
            "id": "jc-mathematics-4-1",
            "name": "Probability of random events"
          },
          {
            "id": "jc-mathematics-4-2",
            "name": "The data-handling cycle (statistical investigation)"
          },
          {
            "id": "jc-mathematics-4-3",
            "name": "Representing data (graphs & charts)"
          },
          {
            "id": "jc-mathematics-4-4",
            "name": "Summary statistics (averages & spread)"
          }
        ]
      }
    ]
  },
  {
    "id": "jc-science",
    "name": "Science (Junior Cycle)",
    "category": "stem",
    "levels": [
      "common"
    ],
    "strands": [
      {
        "id": "jc-science-0",
        "name": "Nature of science",
        "subtopics": [
          {
            "id": "jc-science-0-0",
            "name": "How science works & how ideas change over time"
          },
          {
            "id": "jc-science-0-1",
            "name": "Asking scientific questions & writing testable hypotheses"
          },
          {
            "id": "jc-science-0-2",
            "name": "Designing fair tests: variables, controls, reliability, accuracy, precision & safety"
          },
          {
            "id": "jc-science-0-3",
            "name": "Choosing and using measuring instruments & apparatus"
          },
          {
            "id": "jc-science-0-4",
            "name": "Recording & representing data: tables, graphs and charts"
          },
          {
            "id": "jc-science-0-5",
            "name": "Analysing data, spotting patterns & anomalies, drawing & justifying conclusions"
          },
          {
            "id": "jc-science-0-6",
            "name": "Evaluating sources, reliability, bias & media claims about science"
          },
          {
            "id": "jc-science-0-7",
            "name": "Science in society: scientists' contributions, ethics & global importance"
          }
        ]
      },
      {
        "id": "jc-science-1",
        "name": "Physical world",
        "subtopics": [
          {
            "id": "jc-science-1-0",
            "name": "Measuring physical quantities: length, mass, time, temperature, area, volume, density"
          },
          {
            "id": "jc-science-1-1",
            "name": "Speed, acceleration & motion graphs"
          },
          {
            "id": "jc-science-1-2",
            "name": "Forces"
          },
          {
            "id": "jc-science-1-3",
            "name": "Electricity: current, potential difference, resistance & electrical power"
          },
          {
            "id": "jc-science-1-4",
            "name": "Electric circuits: series, parallel & simple electronic circuits"
          },
          {
            "id": "jc-science-1-5",
            "name": "Energy conservation, transfer, dissipation & efficiency (Sankey diagrams)"
          },
          {
            "id": "jc-science-1-6",
            "name": "Technological applications of physics & their impact"
          },
          {
            "id": "jc-science-1-7",
            "name": "Ethics & sustainability of generating and using electricity"
          }
        ]
      },
      {
        "id": "jc-science-2",
        "name": "Chemical world",
        "subtopics": [
          {
            "id": "jc-science-2-0",
            "name": "States of matter, the particle model & conservation of mass"
          },
          {
            "id": "jc-science-2-1",
            "name": "Atomic structure: protons, neutrons, electrons, mass & charge"
          },
          {
            "id": "jc-science-2-2",
            "name": "Classifying substances: elements, compounds, mixtures, metals & non-metals"
          },
          {
            "id": "jc-science-2-3",
            "name": "The Periodic Table & chemical formulae"
          },
          {
            "id": "jc-science-2-4",
            "name": "Properties of materials: solubility, conductivity, melting & boiling points; separation techniques"
          },
          {
            "id": "jc-science-2-5",
            "name": "Rates of reaction & the variables that affect them"
          },
          {
            "id": "jc-science-2-6",
            "name": "Acids, bases, indicators & the pH scale"
          },
          {
            "id": "jc-science-2-7",
            "name": "Energy in reactions: exothermic, endothermic, activation energy & energy profiles"
          },
          {
            "id": "jc-science-2-8",
            "name": "Sustainability of materials: extraction, use, disposal & recycling"
          }
        ]
      },
      {
        "id": "jc-science-3",
        "name": "Biological world",
        "subtopics": [
          {
            "id": "jc-science-3-0",
            "name": "Cells: plant & animal cell structure and function"
          },
          {
            "id": "jc-science-3-1",
            "name": "Reproduction, inheritance & genetics"
          },
          {
            "id": "jc-science-3-2",
            "name": "Evolution by natural selection & the diversity of life"
          },
          {
            "id": "jc-science-3-3",
            "name": "Human body systems: digestive, circulatory & respiratory"
          },
          {
            "id": "jc-science-3-4",
            "name": "Habitats, adaptation, competition & interdependence (habitat studies)"
          },
          {
            "id": "jc-science-3-5",
            "name": "Human health: nutrition, lifestyle, inherited factors & micro-organisms"
          },
          {
            "id": "jc-science-3-6",
            "name": "Respiration, photosynthesis & energy flow through ecosystems"
          },
          {
            "id": "jc-science-3-7",
            "name": "Human sexual reproduction & related ethical and societal issues"
          },
          {
            "id": "jc-science-3-8",
            "name": "Conserving biodiversity, food production & benefits from ecosystems"
          }
        ]
      },
      {
        "id": "jc-science-4",
        "name": "Earth and space",
        "subtopics": [
          {
            "id": "jc-science-4-0",
            "name": "The solar system & universe: moons, asteroids, comets, planets, stars & galaxies"
          },
          {
            "id": "jc-science-4-1",
            "name": "The origin of the universe & comparing Earth with other planets/moons"
          },
          {
            "id": "jc-science-4-2",
            "name": "The Earth-Sun-Moon system: day & night, seasons, lunar phases & eclipses"
          },
          {
            "id": "jc-science-4-3",
            "name": "Cycling of matter: the carbon and water cycles"
          },
          {
            "id": "jc-science-4-4",
            "name": "Energy sources & meeting Earth's current and future energy needs"
          },
          {
            "id": "jc-science-4-5",
            "name": "Climate, climate change & initiatives to address it"
          },
          {
            "id": "jc-science-4-6",
            "name": "Space exploration: hazards, benefits & its future role in society"
          }
        ]
      }
    ]
  },
  {
    "id": "jc-business-studies",
    "name": "Business Studies (Junior Cycle)",
    "category": "business",
    "levels": [
      "common"
    ],
    "strands": [
      {
        "id": "jc-business-studies-0",
        "name": "Personal finance",
        "subtopics": [
          {
            "id": "jc-business-studies-0-0",
            "name": "Managing money: income, expenditure, needs & wants"
          },
          {
            "id": "jc-business-studies-0-1",
            "name": "Household budgeting & your financial position"
          },
          {
            "id": "jc-business-studies-0-2",
            "name": "The financial lifecycle: needs at different life stages"
          },
          {
            "id": "jc-business-studies-0-3",
            "name": "Saving & borrowing: sources, costs, interest & risk"
          },
          {
            "id": "jc-business-studies-0-4",
            "name": "Insurance: cover for personal needs, premiums & claims"
          },
          {
            "id": "jc-business-studies-0-5",
            "name": "Personal taxes & charges (PAYE, USC, PRSI, DIRT)"
          },
          {
            "id": "jc-business-studies-0-6",
            "name": "Wage slips & calculating your take-home pay"
          },
          {
            "id": "jc-business-studies-0-7",
            "name": "Being an informed consumer: rights & responsibilities"
          },
          {
            "id": "jc-business-studies-0-8",
            "name": "Consumer agencies, banks & financial institutions"
          },
          {
            "id": "jc-business-studies-0-9",
            "name": "Ethical & sustainable consumer choices"
          },
          {
            "id": "jc-business-studies-0-10",
            "name": "How globalisation & technology shape consumer choice"
          }
        ]
      },
      {
        "id": "jc-business-studies-1",
        "name": "Enterprise",
        "subtopics": [
          {
            "id": "jc-business-studies-1-0",
            "name": "Types of enterprise: financial, cultural & social"
          },
          {
            "id": "jc-business-studies-1-1",
            "name": "Being enterprising & the role of the entrepreneur"
          },
          {
            "id": "jc-business-studies-1-2",
            "name": "Forms of business ownership & how a business is set up"
          },
          {
            "id": "jc-business-studies-1-3",
            "name": "Work, employment & volunteerism"
          },
          {
            "id": "jc-business-studies-1-4",
            "name": "Rights & responsibilities of employers and employees"
          },
          {
            "id": "jc-business-studies-1-5",
            "name": "A business and its community: impact & responsibility (CSR)"
          },
          {
            "id": "jc-business-studies-1-6",
            "name": "Digital technologies in business: rewards & costs"
          },
          {
            "id": "jc-business-studies-1-7",
            "name": "Market research: field & desk research, target market"
          },
          {
            "id": "jc-business-studies-1-8",
            "name": "The marketing mix & promoting a product"
          },
          {
            "id": "jc-business-studies-1-9",
            "name": "Writing a business plan"
          },
          {
            "id": "jc-business-studies-1-10",
            "name": "Business documents (invoice, quotation, receipt, credit note)"
          },
          {
            "id": "jc-business-studies-1-11",
            "name": "Cash flow, club/business budgets & sources of finance"
          },
          {
            "id": "jc-business-studies-1-12",
            "name": "Analysed cash book, ledgers & the trial balance"
          },
          {
            "id": "jc-business-studies-1-13",
            "name": "Final accounts: trading, profit & loss and financial position"
          },
          {
            "id": "jc-business-studies-1-14",
            "name": "Interpreting the accounts: analysing financial performance & position"
          }
        ]
      },
      {
        "id": "jc-business-studies-2",
        "name": "Our economy",
        "subtopics": [
          {
            "id": "jc-business-studies-2-0",
            "name": "Scarcity, choice & opportunity cost"
          },
          {
            "id": "jc-business-studies-2-1",
            "name": "Economic systems: how resources are distributed"
          },
          {
            "id": "jc-business-studies-2-2",
            "name": "Supply, demand & how markets set prices"
          },
          {
            "id": "jc-business-studies-2-3",
            "name": "Government finances: revenue, spending & the National Budget"
          },
          {
            "id": "jc-business-studies-2-4",
            "name": "Taxation: why we pay tax and how it works"
          },
          {
            "id": "jc-business-studies-2-5",
            "name": "Economic growth, sustainability & the environment"
          },
          {
            "id": "jc-business-studies-2-6",
            "name": "International trade & globalisation"
          },
          {
            "id": "jc-business-studies-2-7",
            "name": "Ireland in the European Union & the eurozone"
          },
          {
            "id": "jc-business-studies-2-8",
            "name": "Economic indicators: inflation, employment, interest rates"
          },
          {
            "id": "jc-business-studies-2-9",
            "name": "Current economic issues & government economic policy"
          }
        ]
      }
    ]
  },
  {
    "id": "jc-geography",
    "name": "Geography (Junior Cycle)",
    "category": "social-environmental",
    "levels": [
      "common"
    ],
    "strands": [
      {
        "id": "jc-geography-0",
        "name": "Geographical skills: maps, photos & data",
        "subtopics": [
          {
            "id": "jc-geography-0-0",
            "name": "OS maps: grid references, scale & distance"
          },
          {
            "id": "jc-geography-0-1",
            "name": "OS maps: direction, height, relief & slope"
          },
          {
            "id": "jc-geography-0-2",
            "name": "OS maps: identifying features, sketch maps & settlement patterns"
          },
          {
            "id": "jc-geography-0-3",
            "name": "Aerial & satellite photo interpretation"
          },
          {
            "id": "jc-geography-0-4",
            "name": "Climate graphs, charts & data interpretation"
          }
        ]
      },
      {
        "id": "jc-geography-1",
        "name": "Exploring the physical world",
        "subtopics": [
          {
            "id": "jc-geography-1-0",
            "name": "Plate tectonics: volcanoes, earthquakes & fold mountains"
          },
          {
            "id": "jc-geography-1-1",
            "name": "Rocks & the rock cycle"
          },
          {
            "id": "jc-geography-1-2",
            "name": "Weathering & mass movement"
          },
          {
            "id": "jc-geography-1-3",
            "name": "Soils"
          },
          {
            "id": "jc-geography-1-4",
            "name": "Rivers, the water cycle, sea & ice: erosion, deposition & landforms"
          },
          {
            "id": "jc-geography-1-5",
            "name": "Weather, climate & climate of Ireland"
          },
          {
            "id": "jc-geography-1-6",
            "name": "Energy resources from the physical world"
          },
          {
            "id": "jc-geography-1-7",
            "name": "Physical processes in a chosen location (fieldwork)"
          }
        ]
      },
      {
        "id": "jc-geography-2",
        "name": "Exploring how we interact with the physical world",
        "subtopics": [
          {
            "id": "jc-geography-2-0",
            "name": "Living with tectonic hazards & responding to natural disasters"
          },
          {
            "id": "jc-geography-2-1",
            "name": "Rock exploitation & energy resources: consequences"
          },
          {
            "id": "jc-geography-2-2",
            "name": "Primary economic activities & the physical landscape"
          },
          {
            "id": "jc-geography-2-3",
            "name": "Natural resources: water, fish stocks, forestry & soil"
          },
          {
            "id": "jc-geography-2-4",
            "name": "Secondary economic activity: function & location"
          },
          {
            "id": "jc-geography-2-5",
            "name": "Climate change: causes & implications"
          },
          {
            "id": "jc-geography-2-6",
            "name": "Managing surface processes"
          },
          {
            "id": "jc-geography-2-7",
            "name": "Tourism, transport & the physical world"
          }
        ]
      },
      {
        "id": "jc-geography-3",
        "name": "Exploring people, place and change",
        "subtopics": [
          {
            "id": "jc-geography-3-0",
            "name": "Population: structure & change (demographic transition)"
          },
          {
            "id": "jc-geography-3-1",
            "name": "Migration: causes & consequences"
          },
          {
            "id": "jc-geography-3-2",
            "name": "Settlement: rural & urban location"
          },
          {
            "id": "jc-geography-3-3",
            "name": "Urbanisation: urban change in an Irish town or city"
          },
          {
            "id": "jc-geography-3-4",
            "name": "Development & global patterns"
          },
          {
            "id": "jc-geography-3-5",
            "name": "Life chances in developed & developing countries"
          },
          {
            "id": "jc-geography-3-6",
            "name": "Development assistance (aid) & interdependence"
          },
          {
            "id": "jc-geography-3-7",
            "name": "Globalisation: people, settlement & development"
          }
        ]
      }
    ]
  },
  {
    "id": "jc-history",
    "name": "History (Junior Cycle)",
    "category": "social-environmental",
    "levels": [
      "common"
    ],
    "strands": [
      {
        "id": "jc-history-0",
        "name": "The nature of history",
        "subtopics": [
          {
            "id": "jc-history-0-0",
            "name": "Working with sources and evidence (primary vs secondary, usefulness and limitations)"
          },
          {
            "id": "jc-history-0-1",
            "name": "Detecting bias and propaganda; fact, opinion and viewpoint"
          },
          {
            "id": "jc-history-0-2",
            "name": "Reading visual sources: photos, cartoons, posters, maps and statistical tables"
          },
          {
            "id": "jc-history-0-3",
            "name": "Chronology, time and space: timelines, eras and date patterns"
          },
          {
            "id": "jc-history-0-4",
            "name": "Cause and consequence"
          },
          {
            "id": "jc-history-0-5",
            "name": "Change and continuity"
          },
          {
            "id": "jc-history-0-6",
            "name": "Historical significance: why people, events and places are remembered"
          },
          {
            "id": "jc-history-0-7",
            "name": "Historical empathy and seeing the past from more than one perspective"
          },
          {
            "id": "jc-history-0-8",
            "name": "The job of the historian, archaeology and dating the past"
          },
          {
            "id": "jc-history-0-9",
            "name": "Repositories of evidence: museums, archives, libraries and the census"
          },
          {
            "id": "jc-history-0-10",
            "name": "The big picture: connecting people, issues and events across eras"
          }
        ]
      },
      {
        "id": "jc-history-1",
        "name": "The history of Ireland",
        "subtopics": [
          {
            "id": "jc-history-1-0",
            "name": "Early Christian Ireland: monasteries, art and the influence of Christianity"
          },
          {
            "id": "jc-history-1-1",
            "name": "Settlement and plantation, and their impact on Irish identity"
          },
          {
            "id": "jc-history-1-2",
            "name": "The Great Famine and the Irish Diaspora"
          },
          {
            "id": "jc-history-1-3",
            "name": "The parliamentary tradition: Irish political leaders and Home Rule"
          },
          {
            "id": "jc-history-1-4",
            "name": "The physical force tradition and pre-twentieth-century rebellion (e.g. 1798)"
          },
          {
            "id": "jc-history-1-5",
            "name": "Nationalism, unionism and the struggle for independence, 1911-1923 (1916 Rising, War of Independence, Civil War)"
          },
          {
            "id": "jc-history-1-6",
            "name": "The impact of the World Wars on Irish people"
          },
          {
            "id": "jc-history-1-7",
            "name": "How women's lives changed in twentieth-century Ireland"
          },
          {
            "id": "jc-history-1-8",
            "name": "A sporting, cultural or social movement in Irish life (e.g. the GAA)"
          },
          {
            "id": "jc-history-1-9",
            "name": "The Northern Ireland Troubles and North-South / Anglo-Irish relations"
          },
          {
            "id": "jc-history-1-10",
            "name": "The 1960s as a decade of change in Ireland"
          },
          {
            "id": "jc-history-1-11",
            "name": "Ireland's links with Europe and the European Union"
          },
          {
            "id": "jc-history-1-12",
            "name": "Local, personal and family history and its wider connections"
          },
          {
            "id": "jc-history-1-13",
            "name": "Celtic and pre-Christian Ireland: society, homes and daily life"
          }
        ]
      },
      {
        "id": "jc-history-2",
        "name": "The history of Europe and the wider world",
        "subtopics": [
          {
            "id": "jc-history-2-0",
            "name": "Early people and an ancient or medieval civilisation (e.g. Egypt, Rome)"
          },
          {
            "id": "jc-history-2-1",
            "name": "Life and death in medieval times"
          },
          {
            "id": "jc-history-2-2",
            "name": "The Renaissance: change in the arts and science"
          },
          {
            "id": "jc-history-2-3",
            "name": "The Reformation and the actions of one Reformer"
          },
          {
            "id": "jc-history-2-4",
            "name": "Exploration, conquest and colonisation (Portuguese and Spanish)"
          },
          {
            "id": "jc-history-2-5",
            "name": "A revolution in pre-twentieth-century Europe or the wider world (e.g. American, French)"
          },
          {
            "id": "jc-history-2-6",
            "name": "Technology and innovation as drivers of historical change (incl. the Industrial Revolution)"
          },
          {
            "id": "jc-history-2-7",
            "name": "World War One or World War Two: causes, course and impact"
          },
          {
            "id": "jc-history-2-8",
            "name": "Dictatorship in the twentieth century: life in a fascist and a communist country"
          },
          {
            "id": "jc-history-2-9",
            "name": "Genocide and the Holocaust"
          },
          {
            "id": "jc-history-2-10",
            "name": "The Cold War in international relations"
          },
          {
            "id": "jc-history-2-11",
            "name": "International co-operation: the European Union and the United Nations"
          },
          {
            "id": "jc-history-2-12",
            "name": "The 1960s as a decade of change in Europe and the wider world"
          },
          {
            "id": "jc-history-2-13",
            "name": "Patterns of change over time in a chosen theme (crime and punishment, food and drink, work and leisure, fashion, health and medicine)"
          }
        ]
      }
    ]
  },
  {
    "id": "jc-french",
    "name": "French (Junior Cycle)",
    "category": "language",
    "levels": [
      "common"
    ],
    "strands": [
      {
        "id": "jc-french-0",
        "name": "Communicative Competence",
        "subtopics": [
          {
            "id": "jc-french-0-0",
            "name": "Aural: Short Conversations"
          },
          {
            "id": "jc-french-0-1",
            "name": "Aural: Long Conversations"
          },
          {
            "id": "jc-french-0-2",
            "name": "Aural: Long Piece (Monologue)"
          },
          {
            "id": "jc-french-0-3",
            "name": "Aural: News Pieces"
          },
          {
            "id": "jc-french-0-4",
            "name": "Reading: Answering Questions in English"
          },
          {
            "id": "jc-french-0-5",
            "name": "Reading: Answering Questions in French"
          },
          {
            "id": "jc-french-0-6",
            "name": "Reading: Matching Pictures with Descriptions"
          },
          {
            "id": "jc-french-0-7",
            "name": "Reading: Multiple Choice"
          },
          {
            "id": "jc-french-0-8",
            "name": "Writing: Answering Messages"
          },
          {
            "id": "jc-french-0-9",
            "name": "Writing: Completing Phrases"
          },
          {
            "id": "jc-french-0-10",
            "name": "Writing: Email / Blog"
          },
          {
            "id": "jc-french-0-11",
            "name": "Writing: Filling in a Form"
          },
          {
            "id": "jc-french-0-12",
            "name": "Spoken Production and Interaction"
          }
        ]
      },
      {
        "id": "jc-french-1",
        "name": "Language Awareness",
        "subtopics": [
          {
            "id": "jc-french-1-0",
            "name": "Grammar Awareness and Accuracy"
          }
        ]
      },
      {
        "id": "jc-french-2",
        "name": "Socio-cultural Knowledge and Intercultural Awareness",
        "subtopics": [
          {
            "id": "jc-french-2-0",
            "name": "Intercultural Awareness: France and the French-speaking World"
          }
        ]
      }
    ]
  },
  {
    "id": "jc-german",
    "name": "German (Junior Cycle)",
    "category": "language",
    "levels": [
      "common"
    ],
    "strands": [
      {
        "id": "jc-german-0",
        "name": "Communicative Competence",
        "subtopics": [
          {
            "id": "jc-german-0-0",
            "name": "Aural: Short Conversations"
          },
          {
            "id": "jc-german-0-1",
            "name": "Aural: Long Conversations"
          },
          {
            "id": "jc-german-0-2",
            "name": "Aural: Long Piece (Monologue)"
          },
          {
            "id": "jc-german-0-3",
            "name": "Aural: News Pieces"
          },
          {
            "id": "jc-german-0-4",
            "name": "Reading: Answering Questions in English"
          },
          {
            "id": "jc-german-0-5",
            "name": "Reading: Answering Questions in German"
          },
          {
            "id": "jc-german-0-6",
            "name": "Reading: Matching Pictures with Descriptions"
          },
          {
            "id": "jc-german-0-7",
            "name": "Reading: Multiple Choice"
          },
          {
            "id": "jc-german-0-8",
            "name": "Writing: Answering Messages"
          },
          {
            "id": "jc-german-0-9",
            "name": "Writing: Completing Phrases"
          },
          {
            "id": "jc-german-0-10",
            "name": "Writing: Email / Blog"
          },
          {
            "id": "jc-german-0-11",
            "name": "Writing: Filling in a Form"
          },
          {
            "id": "jc-german-0-12",
            "name": "Spoken Production and Interaction"
          }
        ]
      },
      {
        "id": "jc-german-1",
        "name": "Language Awareness",
        "subtopics": [
          {
            "id": "jc-german-1-0",
            "name": "Grammar Awareness and Accuracy"
          }
        ]
      },
      {
        "id": "jc-german-2",
        "name": "Socio-cultural Knowledge and Intercultural Awareness",
        "subtopics": [
          {
            "id": "jc-german-2-0",
            "name": "Intercultural Awareness: Germany and the German-speaking World"
          }
        ]
      }
    ]
  },
  {
    "id": "jc-spanish",
    "name": "Spanish (Junior Cycle)",
    "category": "language",
    "levels": [
      "common"
    ],
    "strands": [
      {
        "id": "jc-spanish-0",
        "name": "Communicative Competence",
        "subtopics": [
          {
            "id": "jc-spanish-0-0",
            "name": "Aural: Short Conversations"
          },
          {
            "id": "jc-spanish-0-1",
            "name": "Aural: Long Conversations"
          },
          {
            "id": "jc-spanish-0-2",
            "name": "Aural: Long Piece (Monologue)"
          },
          {
            "id": "jc-spanish-0-3",
            "name": "Aural: News Pieces"
          },
          {
            "id": "jc-spanish-0-4",
            "name": "Reading: Answering Questions in English"
          },
          {
            "id": "jc-spanish-0-5",
            "name": "Reading: Answering Questions in Spanish"
          },
          {
            "id": "jc-spanish-0-6",
            "name": "Reading: Matching Pictures with Descriptions"
          },
          {
            "id": "jc-spanish-0-7",
            "name": "Reading: Multiple Choice"
          },
          {
            "id": "jc-spanish-0-8",
            "name": "Writing: Answering Messages"
          },
          {
            "id": "jc-spanish-0-9",
            "name": "Writing: Completing Phrases"
          },
          {
            "id": "jc-spanish-0-10",
            "name": "Writing: Email / Blog"
          },
          {
            "id": "jc-spanish-0-11",
            "name": "Writing: Filling in a Form"
          },
          {
            "id": "jc-spanish-0-12",
            "name": "Spoken Production and Interaction"
          }
        ]
      },
      {
        "id": "jc-spanish-1",
        "name": "Language Awareness",
        "subtopics": [
          {
            "id": "jc-spanish-1-0",
            "name": "Grammar Awareness and Accuracy"
          }
        ]
      },
      {
        "id": "jc-spanish-2",
        "name": "Socio-cultural Knowledge and Intercultural Awareness",
        "subtopics": [
          {
            "id": "jc-spanish-2-0",
            "name": "Intercultural Awareness: Spain and the Spanish-speaking World"
          }
        ]
      }
    ]
  },
  {
    "id": "jc-italian",
    "name": "Italian (Junior Cycle)",
    "category": "language",
    "levels": [
      "common"
    ],
    "strands": [
      {
        "id": "jc-italian-0",
        "name": "Communicative Competence",
        "subtopics": [
          {
            "id": "jc-italian-0-0",
            "name": "Aural: Short Conversations"
          },
          {
            "id": "jc-italian-0-1",
            "name": "Aural: Long Conversations"
          },
          {
            "id": "jc-italian-0-2",
            "name": "Aural: Long Piece (Monologue)"
          },
          {
            "id": "jc-italian-0-3",
            "name": "Aural: News Pieces"
          },
          {
            "id": "jc-italian-0-4",
            "name": "Reading: Answering Questions in English"
          },
          {
            "id": "jc-italian-0-5",
            "name": "Reading: Answering Questions in Italian"
          },
          {
            "id": "jc-italian-0-6",
            "name": "Reading: Matching Pictures with Descriptions"
          },
          {
            "id": "jc-italian-0-7",
            "name": "Reading: Multiple Choice"
          },
          {
            "id": "jc-italian-0-8",
            "name": "Writing: Answering Messages"
          },
          {
            "id": "jc-italian-0-9",
            "name": "Writing: Completing Phrases"
          },
          {
            "id": "jc-italian-0-10",
            "name": "Writing: Email / Blog"
          },
          {
            "id": "jc-italian-0-11",
            "name": "Writing: Filling in a Form"
          },
          {
            "id": "jc-italian-0-12",
            "name": "Spoken Production and Interaction"
          }
        ]
      },
      {
        "id": "jc-italian-1",
        "name": "Language Awareness",
        "subtopics": [
          {
            "id": "jc-italian-1-0",
            "name": "Grammar Awareness and Accuracy"
          }
        ]
      },
      {
        "id": "jc-italian-2",
        "name": "Socio-cultural Knowledge and Intercultural Awareness",
        "subtopics": [
          {
            "id": "jc-italian-2-0",
            "name": "Intercultural Awareness: Italy and Italian Culture"
          }
        ]
      }
    ]
  }
];
