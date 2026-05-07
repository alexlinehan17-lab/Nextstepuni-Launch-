/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Oral Exam Authenticity Coach — language patterns and prompts (Stage 3.4).
 *
 * Four diagnostic categories:
 *   1. Rote phrases — generic constructions examiners flag (per dossier
 *      § B3 / § B8: "every student spoke about liking the same TV
 *      programme", "every candidate expressed a liking for the same TV
 *      programme, the same school subject, or the same film or book").
 *   2. Tense signals — verb-form patterns whose presence marks a
 *      sentence as a particular tense. Used to render a tense strip and
 *      flag monotony.
 *   3. Generic-noun patterns — family / person / place references
 *      without specific details, surfaced as personalisation prompts.
 *   4. Sample prompts and polished exemplars — for the comparison view.
 *
 * Coverage:
 *   - French (most dossier-detailed in § B8)
 *   - Irish (§ B3, including authenticity culture)
 *   - German (§ B8)
 *   - Spanish (§ B8)
 */

import {
  type RotePattern,
  type TenseSignal,
  type GenericNounSignal,
  type OralPromptSeed,
  type LanguageId,
} from '../../types/knowledge';

export const LANGUAGE_LABELS: Record<LanguageId, string> = {
  french: 'French',
  irish: 'Irish (Gaeilge)',
  german: 'German',
  spanish: 'Spanish',
};

// ─── Sample prompts ────────────────────────────────────────────────────

export const ORAL_PROMPTS: OralPromptSeed[] = [
  // French
  {
    id: 'fr-typical-day-past',
    language: 'french',
    question: 'Décris ta journée typique l\'année dernière.',
    topic: 'school',
    personalisationPrompts: [
      'Add the name of your school: "à [nom de l\'école]".',
      'Add a specific subject and a real teacher\'s habit: "Mme [nom] commençait toujours par...".',
      'Anchor with one specific event from last year: "le jour où nous avons fait...".',
    ],
  },
  {
    id: 'fr-hobbies',
    language: 'french',
    question: 'Quels sont tes loisirs?',
    topic: 'hobbies',
    personalisationPrompts: [
      'Replace "j\'aime regarder la télé" with a specific show + your reason for watching.',
      'Add a recent occasion: "la semaine dernière, j\'ai joué...".',
      'Express an opinion with reasoning: "X parce que Y".',
    ],
  },
  {
    id: 'fr-family',
    language: 'french',
    question: 'Parle-moi de ta famille.',
    topic: 'family',
    personalisationPrompts: [
      'Name each family member.',
      'Add a job or interest for each: "ma sœur Aoife est étudiante en sciences à Galway".',
      'Mention a recent shared activity: "le week-end dernier, nous avons...".',
    ],
  },
  {
    id: 'fr-future-plans',
    language: 'french',
    question: 'Quels sont tes projets pour l\'avenir?',
    topic: 'future-plans',
    personalisationPrompts: [
      'Use the conditional or future: "j\'aimerais étudier..." / "je ferai...".',
      'Name a specific course and a specific university.',
      'Add a reason rooted in your experience: "parce que mon professeur de... m\'a montré...".',
    ],
  },
  // Irish
  {
    id: 'ga-school',
    language: 'irish',
    question: 'Inis dom faoi do scoil.',
    topic: 'school',
    personalisationPrompts: [
      'Ainmnigh do scoil agus do chathair.',
      'Cuir múinteoir ar leith san áireamh: "is é/í [Bean/An tUasal Mac—] mo mhúinteoir is fearr liom...".',
      'Cuir samplaí faoi rud a tharla i mbliana: "an seachtain seo caite, rinneamar...".',
    ],
  },
  {
    id: 'ga-hobbies',
    language: 'irish',
    question: 'Cad iad na caitheamh aimsire atá agat?',
    topic: 'hobbies',
    personalisationPrompts: [
      'In ionad "is breá liom peil", luaigh club / foireann ar leith.',
      'Cuir tarlú gairid san áireamh: "an Domhnach seo caite, d\'imir mé...".',
      'Tabhair tuairim le réasún: "X mar Y".',
    ],
  },
  {
    id: 'ga-family',
    language: 'irish',
    question: 'Inis dom faoi do theaghlach.',
    topic: 'family',
    personalisationPrompts: [
      'Ainmnigh gach duine de do theaghlach.',
      'Cuir post nó suim ar leith san áireamh: "tá mo dheirfiúr Aoife ag staidéar in Ollscoil na Gaillimhe".',
      'Mínigh rud a rinne sibh le déanaí.',
    ],
  },
  // German
  {
    id: 'de-typical-day',
    language: 'german',
    question: 'Beschreibe deinen typischen Schultag.',
    topic: 'school',
    personalisationPrompts: [
      'Nenne deine Schule und deinen Heimatort.',
      'Schreibe einen konkreten Lehrer und sein Fach: "Frau / Herr [Name], die / der [Fach] unterrichtet, …".',
      'Erwähne ein konkretes Ereignis aus dieser Woche.',
    ],
  },
  {
    id: 'de-hobbies',
    language: 'german',
    question: 'Was sind deine Hobbys?',
    topic: 'hobbies',
    personalisationPrompts: [
      'Statt "ich mag Fußball spielen" nenne den Verein oder die Mannschaft.',
      'Schließe eine kürzliche Aktivität ein: "letzte Woche habe ich gespielt...".',
      'Äußere eine begründete Meinung: "X, weil Y".',
    ],
  },
  // Spanish
  {
    id: 'es-typical-day',
    language: 'spanish',
    question: 'Describe tu día típico el año pasado.',
    topic: 'school',
    personalisationPrompts: [
      'Nombra tu colegio y tu ciudad.',
      'Incluye un profesor específico y su asignatura: "El Señor / La Señora [nombre] me enseñó...".',
      'Ancla con un evento específico del año pasado.',
    ],
  },
  {
    id: 'es-hobbies',
    language: 'spanish',
    question: '¿Cuáles son tus aficiones?',
    topic: 'hobbies',
    personalisationPrompts: [
      'En vez de "me gusta jugar al fútbol", nombra el equipo o club.',
      'Añade una actividad reciente: "la semana pasada jugué...".',
      'Expresa una opinión con razón: "X porque Y".',
    ],
  },
];

// ─── Sample rote answers (the "before" canvas — students start from these
//      so the diagnostics light up immediately, and they can rewrite). ─

export const SAMPLE_ROTE_ANSWERS: Record<string, string> = {
  // French — composite of the dossier's flagged phrases
  'fr-typical-day-past': 'Je me lève à sept heures. Je prends mon petit-déjeuner. Je vais à l\'école. À l\'école, j\'étudie beaucoup. Je rentre à la maison. Je fais mes devoirs. Je regarde la télé. Mon programme préféré est très intéressant. Je me couche à dix heures.',
  'fr-hobbies': 'J\'aime regarder la télé. Je joue au foot. Mon programme préféré est Friends. C\'est très intéressant. J\'aime aussi écouter de la musique. Je joue au foot avec mes amis. Mes amis sont très importants pour moi.',
  'fr-family': 'Ma famille est très importante pour moi. J\'ai un frère et une sœur. Mon père est gentil. Ma mère est gentille. Nous mangeons ensemble. Ma famille est très importante.',
  'fr-future-plans': 'Je veux aller à l\'université. Je veux étudier. C\'est très important. Je veux avoir un bon travail. Je veux gagner de l\'argent.',

  // Irish
  'ga-school': 'Téim ar scoil gach lá. Is breá liom mo scoil. Tá mo chairde sa scoil. Déanaim mo chuid obair bhaile. Téim abhaile ar a ceathair. Bím tuirseach. Téim a chodladh.',
  'ga-hobbies': 'Is breá liom peil. Imrím peil le mo chairde. Is breá liom ceol freisin. Éistim le ceol. Mo theaghlach an-tábhachtach dom. Imrím cluichí ríomhaire.',
  'ga-family': 'Tá mo theaghlach an-tábhachtach dom. Tá deartháir agus deirfiúr agam. Tá mo mháthair go deas. Tá m\'athair go deas. Itheann muid le chéile.',

  // German
  'de-typical-day': 'Ich stehe um sieben Uhr auf. Ich frühstücke. Ich gehe in die Schule. In der Schule lerne ich viel. Ich gehe nach Hause. Ich mache meine Hausaufgaben. Ich sehe fern. Meine Lieblingssendung ist sehr interessant.',
  'de-hobbies': 'Ich mag Fußball spielen. Mein Lieblingsfilm ist sehr interessant. Ich höre gern Musik. Meine Hobbys sind wichtig.',

  // Spanish
  'es-typical-day': 'Me levanto a las siete. Desayuno. Voy al colegio. En el colegio estudio mucho. Vuelvo a casa. Hago mis deberes. Veo la televisión. Mi programa favorito es muy interesante.',
  'es-hobbies': 'Me gusta jugar al fútbol. Me gusta ver la televisión. Mi programa favorito es muy interesante. Mis amigos son muy importantes para mí.',
};

/** Polished exemplars — what the same prompt sounds like with
 *  personalisation and tense variety applied. */
export const POLISHED_EXEMPLARS: Record<string, string> = {
  'fr-typical-day-past': 'L\'année dernière, en cinquième année à St Joseph\'s, je me levais à sept heures et quart. Mon premier cours était souvent maths avec Madame Walsh, qui commençait toujours par dix minutes de calcul mental — je trouvais ça utile, parce que ça nous réveillait. Le mardi, après les cours, j\'allais à l\'entraînement de hurling au club; on a gagné le championnat du comté en mars, ce qui m\'a vraiment marqué. Le soir, je faisais mes devoirs avant de regarder un épisode de Lupin sur Netflix, parce que j\'aime les séries où il y a un mystère à résoudre.',
  'fr-hobbies': 'Mes loisirs ont changé l\'année dernière. Avant, je jouais au foot tous les samedis avec l\'équipe locale, mais je me suis blessé au genou en novembre, donc j\'ai dû arrêter pendant trois mois. Pendant ma convalescence, j\'ai commencé à regarder des séries en français — surtout Lupin et Le Bureau des Légendes — parce que mon professeur, Monsieur Ó Flatharta, nous avait recommandé de pratiquer notre compréhension orale. Maintenant, je suis revenu au foot, mais j\'écoute aussi un podcast en français pendant mes trajets.',
  'fr-family': 'Nous sommes une famille de cinq. Mon père Liam est plombier, et ma mère Síle est infirmière à l\'hôpital de Limerick. J\'ai une sœur aînée, Aoife, qui étudie l\'ingénierie chimique à Galway, et un petit frère, Conor, qui a douze ans et joue au hurling. Le week-end dernier, on est tous allés voir la finale du county de Conor — il a marqué deux points et on était très fiers de lui. Ma famille m\'est importante parce qu\'on rit beaucoup ensemble.',
  'fr-future-plans': 'L\'année prochaine, j\'aimerais étudier la médecine à University College Cork, parce que mon expérience à l\'hôpital de Limerick avec ma mère m\'a montré ce que c\'est. Si je n\'obtiens pas les points, j\'envisagerais la pharmacie à Trinity comme deuxième choix. Avant l\'université, je ferais une année à l\'étranger — peut-être en France — pour améliorer mon français, parce que je sais qu\'il y a beaucoup de patients francophones à Cork.',
  'ga-school': 'Téim ar scoil i St Mary\'s i nGaillimh. An rud is fearr liom faoin scoil ná na múinteoirí, go háirithe Mr Ó Tuathail, atá ag múineadh stair. An tseachtain seo caite, thug sé léacht dúinn ar 1916 nár dhearmadfaidh mé go deo. Tá mo chairde, Niamh agus Eimear, sa rang céanna, agus déanaimid an obair bhaile le chéile uaireanta. Bíonn an mata deacair domsa, ach tá mé ag feabhsú.',
  'ga-hobbies': 'Imrím camógaíocht don chlub áitiúil, Eyrecourt CLG, agus chuamar chuig craobh an chontae anuraidh. Bhuamar! Bhí mé ag imirt sa lár-pháirc agus chuir mé scór amháin agus pas chun comhghleacaí mo, Aoife, ar an scór a bhuaigh an cluiche. Lasmuigh den spórt, is maith liom léitheoireacht, go háirithe leabhair faoi stair na hÉireann — léigh mé "Mise Éire" anuraidh agus chuir sé brón mór orm.',
  'ga-family': 'Tá ceathrar sa teaghlach: m\'athair Brendan, mo mháthair Caitríona, mo dheirfiúr Sadhbh agus mé. Tá m\'athair ina mhúinteoir bunscoile i mBaile na nGall, agus oibríonn mo mháthair mar dhochtúir ginearálta. Tá Sadhbh dhá bhliain níos óige ná mé, agus seinneann sí an fheadóg stáin go han-mhaith — bhuaigh sí Slógadh i Lios na Sé an mhí seo caite.',
  'de-typical-day': 'Letztes Jahr stand ich normalerweise um Viertel nach sieben auf, weil mein Schulbus um zehn vor acht abfuhr. In St Joseph\'s war meine erste Stunde meistens Deutsch mit Frau O\'Brien — sie begann jede Stunde mit fünf Minuten Diktat, was mir wirklich geholfen hat. Am Mittwoch hatten wir kein Sport, also bin ich nach Hause gegangen und habe mit meinem Bruder Conor Schach gespielt; er ist zwölf, aber er gewinnt jedes zweite Spiel.',
  'de-hobbies': 'Mein Haupt-Hobby ist Hurling — ich spiele für den lokalen Verein in Loughrea, und wir haben letzten März das County-Championship gewonnen. Außerdem höre ich gern deutsche Podcasts, besonders "Easy German", weil mein Lehrer Herr Ó Cearra uns beigebracht hat, dass man eine Sprache am besten durch Hören lernt.',
  'es-typical-day': 'El año pasado, me levantaba a las siete y cuarto porque el autobús salía a las ocho menos diez. Mi primera clase en el colegio St Joseph\'s era español con la Señora Walsh — empezaba siempre con cinco minutos de conversación libre, lo cual me ayudó mucho con la fluidez. Los miércoles, después del colegio, iba al entrenamiento de hurling. Ganamos el campeonato del condado en marzo y fue uno de los mejores momentos del año.',
  'es-hobbies': 'Mi afición principal es el hurling — juego para el club local en Loughrea, y ganamos el campeonato del condado en marzo. Además, veo series en español, sobre todo La Casa de Papel y Élite, porque mi profesor, el Señor Ó Conaire, nos enseñó que ver televisión en la lengua extranjera mejora la comprensión.',
};

// ─── Rote patterns ────────────────────────────────────────────────────

export const ROTE_PATTERNS: RotePattern[] = [
  // French — drawn from 2016 SEC CER complaints
  {
    id: 'fr-tele',
    language: 'french',
    pattern: 'j\'aime regarder la t[ée]l[ée]',
    flag: 'The 2016 French Chief Examiner Report flagged this as a near-universal opening — "every candidate expressed a liking for the same TV programme."',
    prescription: 'Replace with: "Je regarde [specific show] sur [Netflix / RTÉ Player] le [day], parce que [specific reason]." Specifics break the rote signal.',
  },
  {
    id: 'fr-foot',
    language: 'french',
    pattern: 'je joue au foot(ball)?',
    flag: 'The most-flagged hobby phrase. Without club / team / context, the marker reads it as memorised.',
    prescription: 'Add specifics: "Je joue au foot pour [club name] tous les samedis depuis [year]." Or, better, name a specific recent match.',
  },
  {
    id: 'fr-prog-prefere',
    language: 'french',
    pattern: 'mon programme pr[ée]f[ée]r[ée] est',
    flag: 'Stock construction. Examiners hear it many times per session.',
    prescription: 'Replace with a personal hook: "En ce moment, je suis accro à...". Or describe a specific scene: "j\'ai pleuré quand...".',
  },
  {
    id: 'fr-tres-important',
    language: 'french',
    pattern: '(est|sont) tr[ée]s important[es]? pour moi',
    flag: 'Filler intensifier without justification.',
    prescription: 'Replace with a specific reason: "parce que [specific moment / shared experience]". The marker rewards reasons, not adjectives.',
  },
  {
    id: 'fr-tres-interessant',
    language: 'french',
    pattern: '(c\'est|il est|elle est) tr[ée]s int[ée]ressant',
    flag: 'Empty adjective. The 2016 CER explicitly criticised "generic statements".',
    prescription: 'Cut. Replace with a specific detail: "Le moment que je préfère est quand...".',
  },
  {
    id: 'fr-jaime-ecouter',
    language: 'french',
    pattern: 'j\'aime [eé]couter de la musique',
    flag: 'Generic musical preference.',
    prescription: 'Name an artist, an album, a specific song or genre and a reason: "j\'écoute Stromae, surtout l\'album Multitude, parce que les paroles sont très politiques".',
  },

  // Irish
  {
    id: 'ga-is-brea',
    language: 'irish',
    pattern: 'is br[ée]a liom peil',
    flag: 'Stock GAA opener. Per dossier § B3, this is on the rote-detection list.',
    prescription: 'Cuir club, foireann, agus eachtra ar leith san áireamh: "Imrím peil don [club name] agus bhuamar [event] anuraidh — chuir mé scór sa chluiche."',
  },
  {
    id: 'ga-tabhachtach',
    language: 'irish',
    pattern: '(an[-\\s]?t[áa]bhachtach do(m)?|tábhachtach domsa)',
    flag: '"Importance" claim without justification.',
    prescription: 'In ionad "an-tábhachtach", tabhair fáth le sampla: "is iad mo theaghlach an chéad daoine ar a smaoiním nuair a bhíonn fadhb agam, mar shampla nuair a thosaigh mé ag staidéar do na scrúduithe..."',
  },
  {
    id: 'ga-ricomh',
    language: 'irish',
    pattern: 'imr[ií]m cluich[íi] r[íi]omhaire',
    flag: 'Generic computer-games claim.',
    prescription: 'Luaigh ainm cluiche, fad ama, agus duine eile: "Imrím Football Manager le mo dheartháir Conor gach Domhnach — d\'éirigh linn sraith Liverpool a bhuachan an samhradh seo caite."',
  },
  {
    id: 'ga-eist-ceol',
    language: 'irish',
    pattern: '[eé]istim le ceol',
    flag: 'Generic music claim.',
    prescription: 'Luaigh banna, leabhar, nó coirm cheoil ar leith: "Éistim le The Murder Capital, go háirithe an t-amhrán \'Don\'t Cling to Life\'."',
  },

  // German
  {
    id: 'de-fussball',
    language: 'german',
    pattern: 'ich (mag|spiele) (gern )?fu(ß|ss)ball',
    flag: 'Stock hobby phrase. The 2016 CER flagged identical hobby answers across cohorts.',
    prescription: 'Konkret: "Ich spiele Fußball für [Vereinsname] und wir haben am [Datum] gegen [Gegner] gespielt."',
  },
  {
    id: 'de-lieblingssendung',
    language: 'german',
    pattern: 'meine lieblingssendung',
    flag: 'Stock television-preference opener.',
    prescription: 'Konkrete Folge / Szene erwähnen: "Letzte Woche habe ich die Folge gesehen, in der..."',
  },
  {
    id: 'de-sehr-interessant',
    language: 'german',
    pattern: '(ist|sind) sehr interessant',
    flag: 'Leere Beschreibung.',
    prescription: 'Streichen oder konkretisieren: "...weil [spezifischer Grund]".',
  },

  // Spanish
  {
    id: 'es-jugar-futbol',
    language: 'spanish',
    pattern: 'me gusta jugar al f[uú]tbol',
    flag: 'Stock hobby phrase per the 2016 CER.',
    prescription: 'Concreta: "Juego al fútbol para [nombre del equipo] y ganamos el campeonato local en [fecha]."',
  },
  {
    id: 'es-programa-favorito',
    language: 'spanish',
    pattern: 'mi programa favorito',
    flag: 'Stock TV opener.',
    prescription: 'Habla de un episodio o escena específica: "En el último episodio que vi, [acción concreta]."',
  },
  {
    id: 'es-muy-importante',
    language: 'spanish',
    pattern: '(son|es) muy importante[s]?( para mí)?',
    flag: 'Filler intensifier.',
    prescription: 'Sustitúyelo por una razón concreta con un ejemplo.',
  },
];

// ─── Tense signals — language-keyed verb-form patterns ────────────────

export const TENSE_SIGNALS: TenseSignal[] = [
  // French — present, passé composé, imparfait, conditional, subjunctive, future
  {
    id: 'fr-passe-compose',
    language: 'french',
    tenseLabel: 'Past',
    patterns: ['\\b(j\'ai|tu as|il a|elle a|on a|nous avons|vous avez|ils ont|elles ont)\\s+\\w+(é|i|u|s|t)', '\\b(je suis|tu es|il est|elle est|nous sommes|vous êtes|ils sont|elles sont)\\s+\\w+(é|ée|és|ées)\\b'],
  },
  {
    id: 'fr-imparfait',
    language: 'french',
    tenseLabel: 'Imp',
    patterns: ['\\b\\w+(ais|ait|aient|ions|iez)\\b'],
  },
  {
    id: 'fr-conditional',
    language: 'french',
    tenseLabel: 'Cond',
    patterns: ['\\b\\w+(rais|rait|raient|rions|riez)\\b'],
  },
  {
    id: 'fr-future',
    language: 'french',
    tenseLabel: 'Fut',
    patterns: ['\\b\\w+(rai|ras|ra|rons|rez|ront)\\b(?! to)', '\\b(je vais|tu vas|il va|elle va|nous allons|vous allez|ils vont)\\s+\\w+er'],
  },
  {
    id: 'fr-subjunctive',
    language: 'french',
    tenseLabel: 'Subj',
    patterns: ['\\b(que|qu\')\\s+(je|tu|il|elle|on|nous|vous|ils|elles)\\s+\\w+(e|es|ions|iez|ent)\\b', '\\b(sois|soit|soyons|soyez|soient|aille|aies|ait|ayons|ayez|aient)\\b'],
  },

  // Irish
  {
    id: 'ga-past',
    language: 'irish',
    tenseLabel: 'Past',
    patterns: ['\\b(bh[íi]|dúirt|rinne|chuaigh|chonaic|chuala|fuair|tháinig|d\'imir|d\'ól|d\'ith|chaith|cheap)\\b', '\\bd\'\\w+', '\\bch\\w+ mé\\b'],
  },
  {
    id: 'ga-future',
    language: 'irish',
    tenseLabel: 'Fut',
    patterns: ['\\b\\w+(faidh|fidh|óchaidh|eoidh)\\b', '\\bbeidh\\b'],
  },
  {
    id: 'ga-cond',
    language: 'irish',
    tenseLabel: 'Cond',
    patterns: ['\\b\\w+(fadh|feadh|óchadh|eodh)\\b', '\\bbheinn\\b', '\\bbheadh\\b'],
  },

  // German
  {
    id: 'de-perfekt',
    language: 'german',
    tenseLabel: 'Past',
    patterns: ['\\b(habe|hast|hat|haben|habt)\\s+\\w+(t|en)\\b', '\\b(bin|bist|ist|sind|seid)\\s+ge\\w+(t|en)\\b'],
  },
  {
    id: 'de-praeteritum',
    language: 'german',
    tenseLabel: 'Past',
    patterns: ['\\b(war|warst|waren|wart|hatte|hattest|hatten|hattet|ging|kam|sah|machte|spielte|lernte)\\b'],
  },
  {
    id: 'de-konjunktiv',
    language: 'german',
    tenseLabel: 'Cond',
    patterns: ['\\b(würde|würdest|würden|würdet|wäre|wärst|wären|wärt|hätte|hättest|hätten|hättet)\\b'],
  },
  {
    id: 'de-future',
    language: 'german',
    tenseLabel: 'Fut',
    patterns: ['\\b(werde|wirst|wird|werden|werdet)\\s+\\w+en?\\b'],
  },

  // Spanish
  {
    id: 'es-preterito',
    language: 'spanish',
    tenseLabel: 'Past',
    patterns: ['\\b\\w+(é|aste|ó|amos|aron|í|iste|imos|isteis|ieron)\\b', '\\b(fui|fue|fuimos|fueron|hice|hizo|tuve|tuvo|estuve|estuvo)\\b'],
  },
  {
    id: 'es-imperfecto',
    language: 'spanish',
    tenseLabel: 'Imp',
    patterns: ['\\b\\w+(aba|abas|ábamos|aban|ía|ías|íamos|ían)\\b', '\\b(era|eras|éramos|eran|iba|ibas|íbamos|iban)\\b'],
  },
  {
    id: 'es-condicional',
    language: 'spanish',
    tenseLabel: 'Cond',
    patterns: ['\\b\\w+(ría|rías|ríamos|rían)\\b'],
  },
  {
    id: 'es-future',
    language: 'spanish',
    tenseLabel: 'Fut',
    patterns: ['\\b\\w+(ré|rás|rá|remos|rán)\\b'],
  },
];

// ─── Generic noun signals ─────────────────────────────────────────────

export const GENERIC_NOUN_SIGNALS: GenericNounSignal[] = [
  // French
  {
    id: 'fr-soeur',
    language: 'french',
    pattern: '\\bma s[œo]ur\\b(?!\\s+[A-ZÀ-Ÿ])',
    prescription: 'Add her name + a specific detail: "ma sœur Aoife, qui étudie à Galway".',
  },
  {
    id: 'fr-frere',
    language: 'french',
    pattern: '\\bmon fr[èe]re\\b(?!\\s+[A-ZÀ-Ÿ])',
    prescription: 'Add his name + a specific detail: "mon frère Conor, qui joue au hurling".',
  },
  {
    id: 'fr-pere',
    language: 'french',
    pattern: '\\bmon p[èe]re\\b(?!\\s+[A-ZÀ-Ÿ])',
    prescription: 'Add his job or a habit: "mon père, plombier dans le quartier".',
  },
  {
    id: 'fr-mere',
    language: 'french',
    pattern: '\\bma m[èe]re\\b(?!\\s+[A-ZÀ-Ÿ])',
    prescription: 'Add her job or a habit: "ma mère, qui travaille à l\'hôpital de Limerick".',
  },
  {
    id: 'fr-amis',
    language: 'french',
    pattern: '\\b(mes amis|mon ami(e)?)\\b(?!\\s+[A-ZÀ-Ÿ])',
    prescription: 'Name them. "Mes amis Niamh et Eimear" beats "mes amis".',
  },
  {
    id: 'fr-ecole',
    language: 'french',
    pattern: '\\b(à |de )l\'?[ée]cole\\b(?!\\s+[A-Z])',
    prescription: 'Name the school: "à St Joseph\'s à Limerick".',
  },

  // Irish
  {
    id: 'ga-deirfiur',
    language: 'irish',
    pattern: '\\bmo dheirfi[úu]r\\b(?!\\s+[A-Z])',
    prescription: 'Cuir a hainm agus rud sonrach: "mo dheirfiúr Aoife, atá ag staidéar in Ollscoil na Gaillimhe".',
  },
  {
    id: 'ga-deartair',
    language: 'irish',
    pattern: '\\bmo dheart[áa]ir\\b(?!\\s+[A-Z])',
    prescription: 'Cuir a ainm agus rud sonrach.',
  },
  {
    id: 'ga-mathair',
    language: 'irish',
    pattern: '\\bmo mh[áa]thair\\b(?!\\s+[A-Z])',
    prescription: 'Cuir a hainm nó a post: "mo mháthair Caitríona, atá ina dochtúir".',
  },
  {
    id: 'ga-athair',
    language: 'irish',
    pattern: '\\bm\'athair\\b(?!\\s+[A-Z])',
    prescription: 'Cuir a ainm nó a phost.',
  },
  {
    id: 'ga-cara',
    language: 'irish',
    pattern: '\\b(mo chara|mo chairde)\\b(?!\\s+[A-Z])',
    prescription: 'Ainmnigh do chara: "mo chara Niamh".',
  },
  {
    id: 'ga-scoil',
    language: 'irish',
    pattern: '\\b(ar |i d?t?\\s?)scoil\\b(?!\\s+[A-Z])',
    prescription: 'Ainmnigh an scoil agus an ceantar: "i St Mary\'s i nGaillimh".',
  },

  // German
  {
    id: 'de-schwester',
    language: 'german',
    pattern: '\\bmeine schwester\\b(?!\\s+[A-ZÄÖÜ])',
    prescription: 'Nenne ihren Namen und ein Detail.',
  },
  {
    id: 'de-bruder',
    language: 'german',
    pattern: '\\bmein bruder\\b(?!\\s+[A-ZÄÖÜ])',
    prescription: 'Nenne seinen Namen und ein Detail.',
  },
  {
    id: 'de-mutter',
    language: 'german',
    pattern: '\\bmeine mutter\\b(?!\\s+[A-ZÄÖÜ])',
    prescription: 'Nenne ihren Beruf oder ein Detail.',
  },
  {
    id: 'de-vater',
    language: 'german',
    pattern: '\\bmein vater\\b(?!\\s+[A-ZÄÖÜ])',
    prescription: 'Nenne seinen Beruf oder ein Detail.',
  },
  {
    id: 'de-schule',
    language: 'german',
    pattern: '\\b(in die |zur )?schule\\b(?!\\s+[A-Z])',
    prescription: 'Nenne den Schulnamen: "St Joseph\'s in Limerick".',
  },

  // Spanish
  {
    id: 'es-hermana',
    language: 'spanish',
    pattern: '\\bmi hermana\\b(?!\\s+[A-ZÁ-Ú])',
    prescription: 'Añade su nombre y un detalle.',
  },
  {
    id: 'es-hermano',
    language: 'spanish',
    pattern: '\\bmi hermano\\b(?!\\s+[A-ZÁ-Ú])',
    prescription: 'Añade su nombre y un detalle.',
  },
  {
    id: 'es-madre',
    language: 'spanish',
    pattern: '\\bmi madre\\b(?!\\s+[A-ZÁ-Ú])',
    prescription: 'Añade su profesión o un detalle.',
  },
  {
    id: 'es-padre',
    language: 'spanish',
    pattern: '\\bmi padre\\b(?!\\s+[A-ZÁ-Ú])',
    prescription: 'Añade su profesión o un detalle.',
  },
  {
    id: 'es-colegio',
    language: 'spanish',
    pattern: '\\b(al |en el |del )colegio\\b(?!\\s+[A-Z])',
    prescription: 'Nombra el colegio.',
  },
];
