/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Comparative Texts Linker — questions and curated point banks (Stage 3.1).
 *
 * Six sample comparative questions across the four LC English Comparative
 * modes (Theme/Issue, Cultural Context, General Vision and Viewpoint,
 * Literary Genre). Each question references three widely-studied LC
 * English texts; descriptors are paraphrased and never reproduce text
 * content from any source.
 *
 * Per /CLAUDE.md content rule: question prompts paraphrased, never more
 * than 15 words verbatim from any SEC paper.
 *
 * Source: dossier § B1 (English Comparative — "best answers were
 * written in an analytical fashion" — 2013 CER), § A5 (three-text rule).
 */

import { type ComparativeQuestion, type ComparativeText } from '../../types/knowledge';

// Reusable text references. Titles are not copyrighted; descriptors are
// paraphrased framings, never quoted content.
const HAMLET: ComparativeText = {
  id: 'hamlet',
  label: 'Hamlet',
  formLabel: 'Play',
  descriptor: 'A young prince processes grief, suspicion, and the demands of vengeance after his father\'s death.',
};
const GATSBY: ComparativeText = {
  id: 'gatsby',
  label: 'The Great Gatsby',
  formLabel: 'Novel',
  descriptor: 'A self-made man pursues a vanished romance against the surface of 1920s American wealth.',
};
const BROOKLYN: ComparativeText = {
  id: 'brooklyn',
  label: 'Brooklyn',
  formLabel: 'Novel / Film',
  descriptor: 'A young Irish woman emigrates to mid-century New York and finds herself divided between two homes.',
};
const TRANSLATIONS: ComparativeText = {
  id: 'translations',
  label: 'Translations',
  formLabel: 'Play',
  descriptor: 'A nineteenth-century Donegal hedge-school confronts British cartographers renaming the local landscape.',
};
const FOSTER: ComparativeText = {
  id: 'foster',
  label: 'Foster',
  formLabel: 'Novella',
  descriptor: 'An Irish girl is sent for a summer to relatives whose careful kindness reveals what her own family lacks.',
};
const WH: ComparativeText = {
  id: 'wh',
  label: 'Wuthering Heights',
  formLabel: 'Novel',
  descriptor: 'Two families on the Yorkshire moors are bound and ruined across a generation by an obsessive love.',
};

export const COMPARATIVE_QUESTIONS: ComparativeQuestion[] = [
  // ─── 1. Theme — Identity ──────────────────────────────────────────
  {
    id: 'theme-identity',
    mode: 'theme',
    questionPrompt: 'Compare the ways in which identity is shaped by external pressure in three of the texts on your comparative course.',
    texts: [HAMLET, BROOKLYN, TRANSLATIONS],
    pointBank: [
      {
        id: 'p1-1',
        text: 'All three protagonists experience identity as fracture: Hamlet\'s by the demand of vengeance, Eilis\'s by the Atlantic crossing, Maire\'s by the renaming of her village.',
        textsTouched: ['hamlet', 'brooklyn', 'translations'],
        rationale: 'Integrated. A single comparative claim ("identity as fracture") threaded through all three texts with a specific external pressure named for each.',
        connectingVerbs: ['all three', 'and'],
      },
      {
        id: 'p1-2',
        text: 'Whereas Hamlet\'s identity-crisis is private and philosophical, Eilis\'s is geographic and embodied, and Maire\'s is collective and linguistic — three different keys turning the same lock.',
        textsTouched: ['hamlet', 'brooklyn', 'translations'],
        rationale: 'Integrated with explicit contrast. The "whereas / and / and" structure carries the comparative work.',
        connectingVerbs: ['whereas', 'and'],
      },
      {
        id: 'p1-3',
        text: 'In Hamlet, the protagonist is paralysed by the question of who he is now after his father\'s death.',
        textsTouched: ['hamlet'],
        rationale: 'Serial. The point is true but only engages Hamlet — the marker cannot credit it as comparative work.',
        integratedRewrite: 'Hamlet, Eilis, and Maire are each paralysed by the question of who they are now — Hamlet after the ghost, Eilis after the boat, Maire after the surveyors. The pressure is different; the structural shock is the same.',
      },
      {
        id: 'p1-4',
        text: 'Eilis Lacey\'s homesickness in Brooklyn reveals a divided identity.',
        textsTouched: ['brooklyn'],
        rationale: 'Serial. Engages Brooklyn alone. A descriptive single-text observation.',
        integratedRewrite: 'Eilis\'s homesickness — like Hamlet\'s mourning and Maire\'s bewilderment at the renamed village — reveals an identity divided between what was and what is being made.',
      },
      {
        id: 'p1-5',
        text: 'Both Eilis and Hamlet face external pressures that fragment their sense of self.',
        textsTouched: ['brooklyn', 'hamlet'],
        rationale: 'Partial. Two texts brought into dialogue; Translations is absent. Two-text answers cap below the band on three-text rubrics.',
        integratedRewrite: 'Eilis, Hamlet, and Maire all face external pressures that fragment their sense of self — Hamlet\'s the spectral father, Eilis\'s the Atlantic crossing, Maire\'s the soldier\'s redrawing of her language.',
      },
      {
        id: 'p1-6',
        text: 'In Translations, the colonial cartographers reshape the landscape of Maire\'s identity.',
        textsTouched: ['translations'],
        rationale: 'Serial. Concentrates on Translations.',
        integratedRewrite: 'In Translations, the cartographers reshape Maire\'s landscape; in Hamlet, the ghost reshapes the prince\'s court; in Brooklyn, the Atlantic reshapes Eilis\'s family — three reshapings, one structural pattern.',
      },
    ],
    source: { section: 'B1', page: 8, cite: 'English CER 2013 — "best answers were written in an analytical fashion"' },
  },

  // ─── 2. Theme — Conflict ──────────────────────────────────────────
  {
    id: 'theme-conflict',
    mode: 'theme',
    questionPrompt: 'Discuss how conflict drives the action in three of the texts on your comparative course.',
    texts: [HAMLET, WH, GATSBY],
    pointBank: [
      {
        id: 'p2-1',
        text: 'Conflict in all three texts is internal before it becomes external: Hamlet\'s with himself, Heathcliff\'s with the world that rejects him, Gatsby\'s with the past he cannot revise.',
        textsTouched: ['hamlet', 'wh', 'gatsby'],
        rationale: 'Integrated. A unifying claim ("internal before external") threaded across each text with a specific conflict named.',
        connectingVerbs: ['in all three', 'with'],
      },
      {
        id: 'p2-2',
        text: 'Similarly, none of the three protagonists wins his conflict — each is undone by the very thing that defined him.',
        textsTouched: ['hamlet', 'wh', 'gatsby'],
        rationale: 'Integrated. A second-order observation that links the three endings under one structural rule.',
        connectingVerbs: ['similarly', 'each'],
      },
      {
        id: 'p2-3',
        text: 'Hamlet\'s conflict with Claudius is the central axis of the play.',
        textsTouched: ['hamlet'],
        rationale: 'Serial. Single-text observation; no comparative framework.',
        integratedRewrite: 'The enemy who is also family — Claudius for Hamlet, Hindley for Heathcliff, Tom for Gatsby — is the axis around which the conflict in each text turns.',
      },
      {
        id: 'p2-4',
        text: 'In Wuthering Heights, the conflict between the Earnshaws and the Lintons drives the second generation\'s grief.',
        textsTouched: ['wh'],
        rationale: 'Serial.',
        integratedRewrite: 'Inter-family conflict shapes a second generation in Wuthering Heights, just as Hamlet\'s death warps Fortinbras\'s arrival and Gatsby\'s death seeds Nick\'s disillusion. Conflict is heritable in all three.',
      },
      {
        id: 'p2-5',
        text: 'Both Hamlet and Heathcliff are defined by an inability to let go of the past.',
        textsTouched: ['hamlet', 'wh'],
        rationale: 'Partial. Two-text. Gatsby is the obvious third leg of this comparison and is missing.',
        integratedRewrite: 'Hamlet, Heathcliff, and Gatsby are each defined by an inability to let go of the past — and each is destroyed by it. The form differs; the structural defeat is shared.',
      },
    ],
    source: { section: 'B1', page: 8 },
  },

  // ─── 3. Cultural Context — Power and Class ───────────────────────
  {
    id: 'culture-power',
    mode: 'cultural-context',
    questionPrompt: 'Examine how power and class shape the choices available to characters in three of the texts on your comparative course.',
    texts: [GATSBY, BROOKLYN, TRANSLATIONS],
    pointBank: [
      {
        id: 'p3-1',
        text: 'In each text, power belongs to people who possess what the protagonist lacks: old money for Gatsby, citizenship for Eilis, English for Maire.',
        textsTouched: ['gatsby', 'brooklyn', 'translations'],
        rationale: 'Integrated. A precise definition of what "power" means in each cultural context, with each gap named.',
        connectingVerbs: ['in each text', 'lacks'],
      },
      {
        id: 'p3-2',
        text: 'The cultural cost is paid in the same currency in all three: the protagonist must perform someone else\'s standards in order to be heard at all.',
        textsTouched: ['gatsby', 'brooklyn', 'translations'],
        rationale: 'Integrated. The "performance" frame works across the three contexts at once.',
        connectingVerbs: ['in all three', 'must'],
      },
      {
        id: 'p3-3',
        text: 'Tom Buchanan\'s old-money confidence wins every confrontation in The Great Gatsby.',
        textsTouched: ['gatsby'],
        rationale: 'Serial.',
        integratedRewrite: 'Tom\'s old-money confidence in Gatsby, Mrs Kehoe\'s Brooklyn boarding-house pecking order in Brooklyn, and Lancey\'s English-speaking authority in Translations all work the same way: power that doesn\'t need to argue.',
      },
      {
        id: 'p3-4',
        text: 'Eilis is shaped by the expectations of her Brooklyn boarding-house community.',
        textsTouched: ['brooklyn'],
        rationale: 'Serial.',
        integratedRewrite: 'Eilis is shaped by Brooklyn\'s boarding-house expectations the way Gatsby is shaped by Long Island\'s old money and Maire by Donegal\'s shifting linguistic order — each protagonist living inside a culture they didn\'t make.',
      },
      {
        id: 'p3-5',
        text: 'Both Gatsby and Eilis are outsiders trying to break into a class that won\'t admit them.',
        textsTouched: ['gatsby', 'brooklyn'],
        rationale: 'Partial. Translations missing.',
        integratedRewrite: 'Gatsby tries to break into old money; Eilis tries to break into Brooklyn\'s middle class; Maire tries to break into English. Three outsider trajectories, three closed gates, three different costs of admission.',
      },
    ],
    source: { section: 'B1', page: 8, cite: 'English CER — Cultural Context analytical fashion' },
  },

  // ─── 4. Cultural Context — Family ─────────────────────────────────
  {
    id: 'culture-family',
    mode: 'cultural-context',
    questionPrompt: 'Compare the ways in which family shapes the protagonist\'s sense of belonging in three of the texts on your comparative course.',
    texts: [FOSTER, BROOKLYN, HAMLET],
    pointBank: [
      {
        id: 'p4-1',
        text: 'Each protagonist is forced to choose between blood family and a found family — Hamlet between Gertrude and Horatio, Eilis between her mother and Tony, the unnamed girl in Foster between her parents and the Kinsellas.',
        textsTouched: ['foster', 'brooklyn', 'hamlet'],
        rationale: 'Integrated. The "blood vs found family" frame applied to each text with specifics.',
        connectingVerbs: ['each', 'between'],
      },
      {
        id: 'p4-2',
        text: 'In all three texts, the family that protects is not always the family the protagonist was born into — and that recognition is the wound that defines them.',
        textsTouched: ['foster', 'brooklyn', 'hamlet'],
        rationale: 'Integrated. A unifying second-order observation.',
        connectingVerbs: ['in all three', 'and'],
      },
      {
        id: 'p4-3',
        text: 'In Foster, the Kinsellas\' kindness is what shows the girl what her own family fails to give her.',
        textsTouched: ['foster'],
        rationale: 'Serial.',
        integratedRewrite: 'The Kinsellas\' kindness in Foster, Mrs Kehoe\'s no-nonsense pragmatism in Brooklyn, and Horatio\'s steadiness in Hamlet each show the protagonist what blood family is failing to provide.',
      },
      {
        id: 'p4-4',
        text: 'Brooklyn shows Eilis caught between her mother\'s expectations and Tony\'s love.',
        textsTouched: ['brooklyn'],
        rationale: 'Serial.',
        integratedRewrite: 'Eilis caught between her mother and Tony, Hamlet caught between his father\'s ghost and Horatio, the girl in Foster caught between Cluna and the Kinsellas — each must decide which family\'s pull to follow.',
      },
    ],
    source: { section: 'B1', page: 8 },
  },

  // ─── 5. General Vision and Viewpoint ─────────────────────────────
  {
    id: 'gvv-hopeful-bleak',
    mode: 'general-vision',
    questionPrompt: 'Discuss how a sense of hope sits alongside a sense of bleakness in three of the texts on your comparative course.',
    texts: [BROOKLYN, FOSTER, TRANSLATIONS],
    pointBank: [
      {
        id: 'p5-1',
        text: 'In each text, hope is small, specific, and easily missed — a stamp licked, a hand held, a story told in Latin — while bleakness is structural and inherited.',
        textsTouched: ['brooklyn', 'foster', 'translations'],
        rationale: 'Integrated. The "small hope vs structural bleakness" frame with named instances per text.',
        connectingVerbs: ['in each', 'while'],
      },
      {
        id: 'p5-2',
        text: 'The general vision in all three is therefore neither despairing nor optimistic but watchful — hope and grief share the same room.',
        textsTouched: ['brooklyn', 'foster', 'translations'],
        rationale: 'Integrated.',
        connectingVerbs: ['in all three', 'and'],
      },
      {
        id: 'p5-3',
        text: 'In Brooklyn, Eilis\'s decision to return to Tony at the end is a quietly hopeful one.',
        textsTouched: ['brooklyn'],
        rationale: 'Serial.',
        integratedRewrite: 'Brooklyn\'s closing moment of hope — Eilis returning to Tony — is the same kind of small, contingent hope that Foster offers in the closing embrace and that Translations offers in Hugh\'s decision to teach English. None of the three is bleak; none is unguarded.',
      },
      {
        id: 'p5-4',
        text: 'Translations ends with a sense of imminent loss — the language is going.',
        textsTouched: ['translations'],
        rationale: 'Serial.',
        integratedRewrite: 'Translations\' linguistic loss, Brooklyn\'s emigrant homesickness, and Foster\'s closing return all render bleakness as something inherited — a structural condition the protagonist has not chosen and cannot fully escape.',
      },
    ],
    source: { section: 'B1', page: 8 },
  },

  // ─── 6. Literary Genre ────────────────────────────────────────────
  {
    id: 'genre-form',
    mode: 'literary-genre',
    questionPrompt: 'Examine how three different literary forms shape the comparative experience for the reader / viewer.',
    texts: [HAMLET, GATSBY, BROOKLYN],
    pointBank: [
      {
        id: 'p6-1',
        text: 'The play, the novel, and the film each foreground a different layer of the experience: Hamlet stages what we feel, Gatsby narrates what we infer, Brooklyn films what we see.',
        textsTouched: ['hamlet', 'gatsby', 'brooklyn'],
        rationale: 'Integrated. Each form\'s defining device named — staging vs narration vs camera — under one comparative rule.',
        connectingVerbs: ['each', 'vs'],
      },
      {
        id: 'p6-2',
        text: 'In all three, the form\'s dominant device — soliloquy, narrator, close-up — is the route through which the protagonist\'s interior reaches us.',
        textsTouched: ['hamlet', 'gatsby', 'brooklyn'],
        rationale: 'Integrated.',
        connectingVerbs: ['in all three'],
      },
      {
        id: 'p6-3',
        text: 'Hamlet\'s soliloquies give us his interior thought directly.',
        textsTouched: ['hamlet'],
        rationale: 'Serial.',
        integratedRewrite: 'Hamlet\'s soliloquies, Nick Carraway\'s narration in Gatsby, and the camera\'s close-ups on Eilis\'s face in Brooklyn each function as the form\'s preferred route into the protagonist\'s interior.',
      },
      {
        id: 'p6-4',
        text: 'Brooklyn the film uses light and music to convey what novels would say in a sentence.',
        textsTouched: ['brooklyn'],
        rationale: 'Serial.',
        integratedRewrite: 'Brooklyn the film uses light and music; Gatsby the novel uses Nick\'s qualified narration; Hamlet the play uses soliloquy. Each form encodes interior life through the device its medium most trusts.',
      },
      {
        id: 'p6-5',
        text: 'Both the play and the novel rely on language; the film relies more on image.',
        textsTouched: ['hamlet', 'gatsby', 'brooklyn'],
        rationale: 'Integrated, though shallow. The point names all three but offers a thin generalisation; a stronger answer specifies each medium\'s tools.',
        connectingVerbs: ['both', 'the'],
      },
    ],
    source: { section: 'B1', page: 8 },
  },
];
