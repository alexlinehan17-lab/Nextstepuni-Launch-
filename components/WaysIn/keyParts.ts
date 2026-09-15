/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Ways In — the key parts of a question.
 *
 * The planner used to hand a student the question back one sentence at a
 * time: on three cards in four, every planning row was a verbatim sentence of
 * the paper. That is re-reading, not breaking down. A teacher breaks a
 * question into the job (the command word), how many, what it is about, the
 * limits that decide what counts, and the material to use. This module does
 * the same, from the printed wording alone.
 *
 * Two rules make it safe to show before the marking scheme:
 *   1. Every slot is LIFTED. action, count, focus, conditions and use are
 *      character ranges of the printed stem or question — never paraphrase.
 *      Only `means` (what a command word asks for, generic to the command) is
 *      authored text.
 *   2. Nothing is inferred from the scheme, and a given whose quantity is the
 *      thing being asked for is never attached (it would be the answer).
 *
 * When a question cannot be broken down honestly — not in English, garbled,
 * no text, no recognisable instruction — the breakdown says so and the panel
 * falls back to the printed question rather than guessing.
 */
import {
  commandMatches, COUNTED_ANSWER_NOUNS, DATA_TOKEN, MEANINGFUL_DATA_UNIT,
  type CommandMatch,
} from './questionModel';
import { EXAM_LEXICONS, type ExamLexicon } from './examLexicons';
import type { WaysInQuestionSource } from './types';

export interface KPSpan {
  /** Exact printed characters. */
  text: string;
  /** Whitespace collapsed, for display. */
  display: string;
  from: 'q' | 'stem';
  start: number;
  end: number;
}

export type KPUseKind = 'material' | 'given' | 'options' | 'locator';
export interface KPUse extends KPSpan { kind: KPUseKind }

export type KPFlag =
  | 'needs-figure'          // refers to a figure the card does not carry
  | 'values-on-paper'       // a calculation whose values are not on this card
  | 'depends-on-earlier-part'
  | 'excludes-example'      // "another", "one other": the stem's own example does not count
  | 'as-printed';           // could not be broken down: the part is shown exactly as printed

export interface KPUnit {
  id: string;
  /** The printed part label, "(ii)" or "1.", never inferred. */
  ref: string;
  altGroup?: 'A' | 'B';
  /** Written in the same answer as another unit ("Describe and explain"). */
  jointWith?: string;
  action: KPSpan | null;
  actionKey: string;
  /** What the command asks for, generic to the command, never to the topic. */
  means: string;
  /** An exam-language command's plain English ("Pick out" for "Relevez"). */
  english?: string;
  count: KPSpan | null;
  countValue?: number;
  /** The noun a counted plan row is labelled with ("Reason 1"). */
  countNoun?: string;
  focus: KPSpan | null;
  /** Printed words that continue the focus after a limit interrupts it:
   *  "conditions, other than X, that are necessary for …". */
  focusMore?: KPSpan[];
  /** The printed item this unit covers, from a list the question prints. */
  item?: KPSpan;
  /** Headings the paper names for the answer ("colour, pattern"). */
  headings?: KPSpan[];
  sides?: [KPSpan, KPSpan];
  conditions: KPSpan[];
  use: KPUse[];
  marks: number | null;
  flags: KPFlag[];
}

export type KPMode = 'decomposed' | 'glossed' | 'verbatim' | 'blocked';
export type KPReason = 'non-english' | 'garbled' | 'no-text' | 'command-missing';

export interface KeyPartsBreakdown {
  mode: KPMode;
  reasons: KPReason[];
  /** Two printed alternatives: the student answers one. */
  banner?: 'answer-one-alt';
  /** Card-wide rules shown once ("Answer in English", "about 50 words"). */
  cardRules: KPSpan[];
  /** Printed statements the question sets up before it asks, that no slot
   *  shows ("You are asked to address a group of farmers …"). */
  setting?: KPSpan[];
  units: KPUnit[];
  totalMarks: number | null;
}

// ---------------------------------------------------------------------------
// Lexicon: what each command word asks for (§3.8 of the spec, from 220
// hand-written breakdowns across every kind of subject).
// ---------------------------------------------------------------------------

const MEANS: Record<string, string> = {
  state: 'A short, direct answer — no explanation needed.',
  name: 'A word or short phrase — no explanation.',
  identify: 'Pick out the right one and name it.',
  list: 'Brief points, one per line.',
  define: 'The exact meaning, in one precise sentence, in your own words.',
  explain: 'Say why or how — not just what.',
  'explain-why': 'Give the reason — the “because” behind it.',
  'explain-how': 'Say how it happens, with the reason for each point.',
  'justify-tail': 'Back up the answer you just gave.',
  describe: 'Say what it is or what happens — features or stages.',
  'describe-how': 'Set out how it works or is done, in order.',
  'describe-experiment': 'Apparatus, what you do, what you see, what it shows.',
  'brief-describe': 'A short account — key points only.',
  outline: 'Main points, briefly — a line or two each.',
  discuss: 'Several developed points, with reasons or examples.',
  examine: 'Describe it and explain it — develop each point.',
  analyse: 'Break it into its parts and show how they connect.',
  compare: 'Set the two side by side — refer to both.',
  'compare-contrast': 'How they are alike and how they differ, point against point.',
  contrast: 'The differences, point against point.',
  distinguish: 'Say what each is, then the difference — cover both.',
  evaluate: 'Weigh strengths against weaknesses, then give a verdict.',
  assess: 'Weigh it up and reach a judgement you can support.',
  suggest: 'A sensible answer from what you know — more than one may work.',
  argue: 'Build the case for the side you are given.',
  justify: 'Give the reasons that support it.',
  account: 'Give the reasons it happened.',
  give: 'Separate, brief points — one per idea.',
  calculate: 'Formula, substitute, answer with its unit.',
  solve: 'Work it through to the final result, every step shown.',
  prove: 'Every step, in order, to the result — nothing assumed.',
  derive: 'Build the result step by step from what you are given.',
  convert: 'Rewrite it in the form asked, showing each step.',
  draw: 'A clear drawing — every named part labelled.',
  sketch: 'A quick, clear drawing with the key features shown.',
  label: 'Put each name on the right part.',
  complete: 'Fill in what is missing, in the space given.',
  include: 'It must appear on the drawing or in the answer itself.',
  tick: 'Mark one box — no writing needed.',
  choose: 'Make your choice first — it decides the rest.',
  illustrate: 'Add sketches or an example that support what you write.',
  predict: 'Say what will happen, and why you expect it.',
  estimate: 'A reasonable value — show how you got it.',
  classify: 'Put each into the right group.',
  match: 'Pair each item with the one it goes with.',
  interpret: 'Say what it shows and what that means.',
  summarise: 'The main points only, in your own words.',
  write: 'Write it out in full, in the form asked.',
  translate: 'The meaning, faithfully, in the other language.',
  'wh-where': 'A place or position — as specific as you can.',
  'wh-when': 'A time — as specific as the question allows.',
  'wh-why': 'Give the reason — the “because” behind it.',
  'wh-feel': 'Name the feeling, then point to what shows it.',
  'wh-evidence': 'Point to specific details — quote or refer to them.',
  'wh-effect': 'What changes, and which way.',
  'wh-opinion': 'Take a clear position, then back it up.',
  'to-what-extent': 'Decide how far, and argue it throughout.',
  'wh-plain': 'A direct answer — say it plainly.',
  'wh-developed': 'Answer it directly, then develop it — a reason or piece of evidence for each point.',
  'account-of': 'Say what happened or what it is, in order — develop each point.',
  'give-details': 'Specific points of information — one per detail.',
  'yes-no': 'Decide yes or no.',
  'either-or': 'Pick one of the options it gives.',
  'true-false': 'Decide true or false for each — no explanation needed.',
  construct: 'Find it by construction on the drawing — leave the construction lines showing.',
  choice: 'Pick the one option that answers it.',
  'illustrate-tail': 'Add sketches or diagrams that support what you write.',
  amend: 'Change what is there so it does what is asked — keep the rest working.',
  balance: 'Make both sides match — the same number of each atom and the same charge.',
  'on-drawing': 'Mark it on the drawing itself — clearly and in the right place.',
  'brief-comment': 'A short comment — a point or two, with a reason.',
  persuade: 'Win the reader over — a clear case, with reasons they will accept.',
  step: 'A step to carry out on the computer before the parts that earn marks.',
  'brief-job': 'One of the things your piece must do — develop it in its own paragraph.',
  'show-drawing': 'Show it in a clear, labelled drawing, with notes where they help.',
  copy: 'Reproduce it accurately — the same labels, scale and features.',
  'as-printed': '',
};

const keyFor = (surface: string, following: string): string => {
  const s = surface.toLowerCase().replace(/\s+/g, ' ').trim();
  const bare = s.replace(/^(?:briefly|clearly|carefully|neatly|fully|accurately|now|next|then|also|finally|hence|therefore|thus)\s+/, '').replace(/\s+(?:briefly|clearly|in detail)(?=\s|$)/g, '');
  const next = following.trimStart().toLowerCase();
  if (/^explain (?:the (?:underlined |following )?terms?|what is meant by)|^define|^what is meant by/.test(bare)
    || /^(?:explain|state|describe|outline) what is meant by/.test(`${bare} ${next}`)) return 'define';
  if (/^give an account of/.test(bare)) return 'account-of';
  const noun = /^give an? (?:(?:brief|short|detailed|full|clear|reasoned) )?(explanation|description|assessment|evaluation|analysis|outline|summary|definition|comparison|discussion|justification|interpretation|account)\b/.exec(bare);
  if (noun) {
    const brief = /^give an? (?:brief|short) /.test(bare);
    const byNoun: Record<string, string> = {
      explanation: 'explain', description: brief ? 'brief-describe' : 'describe', assessment: 'assess', evaluation: 'evaluate',
      analysis: 'analyse', outline: 'outline', summary: 'summarise', definition: 'define', comparison: 'compare',
      discussion: 'discuss', justification: 'justify', interpretation: 'interpret', account: brief ? 'brief-describe' : 'account-of',
    };
    return byNoun[noun[1]];
  }
  if (/^(?:explain|give|state|write)(?: in (?:english|irish))? (?:the |its )?meaning\b/.test(`${bare} ${next}`.replace(/\s+/g, ' '))) return 'define';
  if (/^write (?:briefly )?about\b|^write briefly/.test(`${s} ${next}`)) return 'brief-describe';
  if (/^comment briefly|^briefly comment/.test(s)) return 'brief-comment';
  if (/^describe why/.test(bare)) return 'explain-why';
  if (/^examine whether|^consider whether|^discuss whether/.test(bare)) return 'assess';
  // "Describe how X differs from Y", "How does X differ from Y?": the
  // difference between two things.
  if (/^(?:describe|show|explain|state) how$|^how (?:does|do|did|is|are|was|were)$/.test(bare) && /^[^.?]{0,80}\b(?:differs?|different|contrasts?)\b/.test(next)) return 'contrast';
  if (/^(?:describe|show|explain|state) how$|^how (?:does|do|did|is|are|was|were)$/.test(bare) && /^[^.?]{0,80}\bcompares?\b/.test(next)) return 'compare';
  if (/^choose\b/.test(bare) && /^(?:the|one|a) (?:term|word|option|answer|letter|number|phrase|statement|structure|name)s?\b|from the (?:list|following)/.test(next)) return 'choice';
  if (/^give (?:full )?details$/.test(bare)) return 'give-details';
  if (/^illustrate your answer/.test(`${bare} ${next}`)) return 'illustrate-tail';
  if (/^(?:explain|justify) your answer|^give (?:a )?reasons? for your answer/.test(`${bare} ${next}`)) return 'justify-tail';
  if (/^how (?:did|do|would|will|should)$/.test(bare) && /^you\b/.test(next) && !/^you (?:think|feel|know|describe)\b/.test(next)) return 'describe-how';
  if (/^how (?:could|can|might)$/.test(bare) && /^you\b/.test(next)) return 'suggest';
  if (/^(?:explain|state|describe) how$/.test(bare) && /^you (?:know|can tell|could tell)\b/.test(next)) return 'wh-evidence';
  if (/^identify how$/.test(bare)) return 'explain-how';
  if (/^give$/.test(bare) && /^your (?:own )?(?:personal )?(?:response|views?|opinion|reaction|verdict|assessment)\b/.test(next)) return 'wh-opinion';
  if (/^what is your (?:opinion|view|assessment)|^what are your views/.test(`${bare} ${next}`)) return 'wh-opinion';
  if (/^what did you learn\b|^what have you learned\b/.test(`${bare} ${next}`)) return 'wh-developed';
  if (/^what similarities and differences|^what are the similarities and differences/.test(`${bare} ${next}`)) return 'compare-contrast';
  if (/^give the names? of\b/.test(`${bare} ${next}`)) return 'name';
  if (/^(?:open|save|run)\b/.test(bare)) return 'step';
  if (/^explain why/.test(bare)) return 'explain-why';
  if (/^explain how/.test(bare)) return 'explain-how';
  if (/^describe how/.test(bare)) return 'describe-how';
  if (/^describe an experiment/.test(bare)) return 'describe-experiment';
  if (/^compare and contrast/.test(bare)) return 'compare-contrast';
  if (/^(?:distinguish|differentiate)/.test(bare)) return 'distinguish';
  if (/^account for/.test(bare)) return 'account';
  if (/^to what extent/.test(bare)) return 'to-what-extent';
  if (/^(?:do you (?:think|agree)|what do you (?:think|consider))/.test(bare)) return 'wh-opinion';
  if (/^what evidence/.test(bare)) return 'wh-evidence';
  if (/^what effect/.test(bare)) return 'wh-effect';
  if (/^how does .* feel|^how did .* feel/.test(`${bare} ${next}`) && /^how/.test(bare)) return 'wh-feel';
  if (/^where\b/.test(bare)) return 'wh-where';
  if (/^when\b/.test(bare)) return 'wh-when';
  if (/^why\b/.test(bare)) return 'wh-why';
  if (/^how (?:does|did|do|will|would)$/.test(bare) && /^[^.?]{0,80}\b(?:change|vary|differ|affect)\b/.test(next)) return 'wh-effect';
  if (/^how (?:does|did|do|can|could|would|will|should|might|is|are|was|were|has|have)$/.test(bare)) return 'explain-how';
  if (/^how (?:many|much)$/.test(bare) && /^(?:moles?|grams?|kilograms?|g|kg|joules?|kj|j|litres?|cm3|cm³|dm3|dm³|atoms?|molecules?|electrons?|protons?|neutrons?|ions?|energy|heat|work|charge|current|time|mass|volume|water|metres?|seconds?|hours?|minutes?|years|days|euro|money|interest|tax|profit)\b/i.test(next)) return 'calculate';
  if (/^(?:what|which|how|who|whose|whom)\b/.test(bare)) return 'wh-plain';
  if (/^(?:to|under|in|from|on|at|by|for|with|of|during)\s+(?:what|which|whom|whose|how)\b/.test(bare)) return 'wh-plain';
  if (s.startsWith('briefly describe') || /^describe briefly/.test(s)) return 'brief-describe';
  const verb = bare.split(' ')[0];
  // "Find the value of x" is a calculation; "find ten words related to
  // 'Music'" is not.
  if (/^(?:find|determine)$/.test(verb) && !QUANTITY.test(next)) return 'identify';
  const map: Record<string, string> = {
    state: 'state', name: 'name', identify: 'identify', list: 'list', define: 'define', explain: 'explain',
    describe: 'describe', outline: 'outline', discuss: 'discuss', examine: 'examine', analyse: 'analyse', analyze: 'analyse',
    compare: 'compare', contrast: 'contrast', evaluate: 'evaluate', assess: 'assess', suggest: 'suggest', argue: 'argue',
    justify: 'justify', give: 'give', calculate: 'calculate', find: 'calculate', determine: 'calculate', work: 'calculate',
    solve: 'solve', prove: 'prove', show: 'prove', derive: 'derive', convert: 'convert', draw: 'draw', sketch: 'sketch',
    label: 'label', complete: 'complete', include: 'include', tick: 'tick', choose: 'choose', select: 'choose',
    illustrate: 'illustrate', predict: 'predict', estimate: 'estimate', classify: 'classify', interpret: 'interpret',
    summarise: 'summarise', summarize: 'summarise', write: 'write', translate: 'translate', mention: 'state',
    specify: 'state', indicate: 'state', recommend: 'suggest', propose: 'suggest', comment: 'discuss', consider: 'discuss',
    match: 'match', rank: 'classify', plot: 'draw', construct: 'draw', design: 'draw',
    measure: 'calculate', verify: 'prove', demonstrate: 'prove', investigate: 'describe', review: 'evaluate',
    simplify: 'solve', factorise: 'solve', factorize: 'solve', expand: 'solve', express: 'convert', locate: 'identify',
    scan: 'identify', project: 'draw', fill: 'complete', shade: 'draw', mark: 'label', insert: 'complete',
    underline: 'choice', circle: 'choice', rewrite: 'write', arrange: 'classify', devise: 'suggest', plan: 'write',
    trace: 'describe', set: 'write', present: 'write', prepare: 'write', put: 'tick', place: 'tick',
    amend: 'amend', update: 'amend', modify: 'amend', extend: 'amend', edit: 'amend', replace: 'write', create: 'write',
    add: 'amend', change: 'amend', redraw: 'draw', reproduce: 'draw',
    implement: 'write', apply: 'solve', balance: 'balance',
    tell: 'account-of', relate: 'account-of', recount: 'account-of', narrate: 'account-of', point: 'identify',
    copy: 'copy', multiply: 'solve', reflect: 'discuss', explore: 'discuss', introduce: 'describe', provide: 'give',
    share: 'describe', warn: 'persuade', urge: 'persuade', persuade: 'persuade', convince: 'persuade', encourage: 'persuade',
    promote: 'persuade', impress: 'persuade', appeal: 'persuade', nominate: 'choose', highlight: 'identify',
    offer: 'give', advise: 'suggest', inform: 'describe', speculate: 'predict', recall: 'describe', respond: 'discuss',
  };
  // "Place a tick" ticks; "Place X on the diagram" / "place it in Column B" labels or matches.
  if (/^(?:place|put)$/.test(verb) && !/^(?:a |your )?(?:tick|✓|x\b|cross|circle)/.test(next)) return /\bcolumn\b|\bmatch/.test(next) ? 'match' : 'label';
  // "Express your views" gives them; "Express x in terms of y" converts.
  if (verb === 'express' && /^(?:your|their|his|her|an?\s+(?:opinion|view|personal))\b/.test(next)) return 'give';
  // "construct an argument" is argued and "construct a plan" is written;
  // only a drawing or a geometric figure is constructed.
  if (verb === 'construct' && /^(?:an?\s+)?(?:[\p{L}-]+\s+)?(?:argument|case)\b/iu.test(next)) return 'argue';
  if (verb === 'construct' && /^(?:an?\s+)?(?:[\p{L}-]+\s+)?(?:plan|paragraph|sentence|response|speech|letter|report|timeline|schedule|table|questionnaire|survey|budget)\b/iu.test(next)) return 'write';
  return map[verb] ?? 'other';
};

const QUANTITY = /^(?:(?:the|an?|its|their|his|her)\s+)?(?:[\p{L}-]+\s+){0,2}(?:values?|area|volume|length|distance|displacement|speed|velocity|time|mass|weight|force|angle|coordinates?|equations?|expression|roots?|derivative|gradient|slope|range|sum|product|probability|mean|median|mode|number|cost|price|rate|percentage|ratio|height|radius|diameter|perimeter|circumference|magnitude|acceleration|energy|power|resistance|current|voltage|concentration|moles?|yield|limit|integral|point|points|intersection|inverse|period|frequency|wavelength|work|momentum|tension|pressure|density|temperature|charge|capacitance|efficiency|profit|loss|interest|tax|amount|size|measure|dimensions?|centre|center|image|solution|solutions|matrix|determinant|modulus|argument|domain|breakeven|margin|elasticity|multiplier|output|surplus)\b|^[a-zA-Zθφλμ](?:\s*[=,)]|\s*$|\s+(?:and|if|when|such|in terms)\b)|^[\d(]|^\|/iu;

const CALC_KEYS = new Set(['calculate', 'solve', 'convert', 'estimate']);
/** How much a command asks for, to pick one gloss for two joined verbs. */
const JOB_WEIGHT = (key: string) => (/^(?:state|name|label|identify|list|give|indicate|tick|choice|mark-answer|include)$/.test(key) ? 1
  : /^(?:describe|outline|brief-describe|define|write|draw|sketch|complete|suggest)$/.test(key) ? 2
    : /^(?:explain|explain-how|explain-why|discuss|analyse|evaluate|assess|compare|contrast|construct|calculate|solve|prove|derive|justify|account-of)$/.test(key) ? 3 : 2);

// Imperatives the shared command lexicon lacks. Used only at a clause start,
// so "locate" inside a sentence is never mistaken for an instruction.
const EXTRA_VERBS = /^(?:hence(?:,| or otherwise,)?\s+)?(identify|describe|explain|outline|discuss|suggest|analyse|analyze|evaluate|assess|compare|contrast|define|justify|classify|predict|interpret|summarise|summarize|examine|distinguish|illustrate|label|draw|put a tick|place a tick|amend|update|modify|extend|replace|balance|apply|create|implement|edit|solve|work out|prove|verify|show that|find|evaluate|simplify|factorise|factorize|expand|express|write down|write out|write|obtain|derive|estimate|calculate|locate|scan|project|construct|determine|mention|fill in|complete|shade|mark|plot|insert|underline|circle|match|rewrite|arrange|rank|sketch|trace|investigate|recommend|propose|devise|design|plan|prepare|set out|show|indicate|specify|select|choose|tick|give|state|name|list)(?![\p{L}])/iu;
const EXTENDED = new Set(['describe', 'explain', 'discuss', 'examine', 'analyse']);

// ---------------------------------------------------------------------------
// Small text helpers.
// ---------------------------------------------------------------------------

const collapse = (value: string) => value.replace(/\s+/g, ' ').trim();

/** A span over raw[start, end), trimmed of whitespace and clause punctuation. */
function spanOf(from: 'q' | 'stem', raw: string, start: number, end: number): KPSpan | null {
  let s = Math.max(0, start);
  let e = Math.min(raw.length, end);
  while (s < e && /[\s,;:–—-]/.test(raw[s])) s += 1;
  while (e > s && /[\s,;:.?!–—-]/.test(raw[e - 1])) e -= 1;
  // An unmatched opening bracket at the end, or closing at the start, is
  // punctuation that belongs to the neighbour.
  while (e > s && /[([“‘"]/.test(raw[e - 1])) e -= 1;
  while (s < e && /[)\]”’•·▪‣◦]/.test(raw[s])) s += 1;
  while (s < e && /\s/.test(raw[s])) s += 1;
  // A bracket the span cannot close belongs to the text around it: "(Unless
  // otherwise stated, …" / "… may be estimated.)".
  if (raw[s] === '(' && !raw.slice(s, e).includes(')')) { s += 1; while (s < e && /\s/.test(raw[s])) s += 1; }
  if (raw[e - 1] === ')' && !raw.slice(s, e).includes('(')) { e -= 1; while (e > s && /[\s.,;:]/.test(raw[e - 1])) e -= 1; }
  if (e - s < 1) return null;
  const text = raw.slice(s, e);
  const display = collapse(text);
  if (!display || !/[\p{L}\p{N}]/u.test(display)) return null;
  return { text, display, from, start: s, end: e };
}

const ENGLISH_FUNCTION = new Set([
  'the', 'a', 'an', 'of', 'to', 'in', 'and', 'or', 'with', 'for', 'on', 'by', 'is', 'are', 'be', 'which',
  'what', 'how', 'why', 'your', 'you', 'this', 'that', 'from', 'as', 'at', 'it', 'its', 'was', 'were', 'has',
  'have', 'each', 'one', 'two', 'three', 'answer', 'explain', 'describe', 'name', 'state', 'give', 'identify',
  'outline', 'discuss', 'evaluate', 'calculate', 'list', 'draw', 'compare', 'suggest', 'write', 'following',
  'above', 'below', 'text', 'question', 'refer', 'reference', 'why', 'where', 'when', 'who', 'does', 'do', 'did',
  'between', 'during', 'about', 'into', 'than', 'these', 'those', 'their', 'there', 'they', 'his', 'her', 'not', 'can',
  'will', 'would', 'should', 'could', 'may', 'must', 'been', 'all', 'some', 'other', 'another', 'within', 'after',
  'before', 'any', 'distinguish', 'define', 'difference', 'differences', 'reason', 'reasons', 'example', 'examples',
  'using', 'use', 'term', 'terms', 'effect', 'effects', 'role', 'main',
]);

function englishRatio(text: string): { words: number; ratio: number } {
  const words = text.toLowerCase().match(/[\p{L}']+/gu) ?? [];
  if (!words.length) return { words: 0, ratio: 0 };
  // Slovak, Hungarian and Irish use "a" too; with their letters present it
  // is not evidence of English.
  const foreignLetters = /[à-öø-ÿĀ-ſ]/i.test(text.replace(/[‘’“”–—]/g, ''));
  const hits = words.filter(w => ENGLISH_FUNCTION.has(w) && !(foreignLetters && w === 'a')).length;
  return { words: words.length, ratio: hits / words.length };
}

// Sentence splitting that does not break after "Fig.", "e.g.", "No.", a
// decimal or a single initial — the old splitter cut "Fig. C-5" in two.
const NO_BREAK_AFTER = /(?:\b(?:Fig|Figs|No|Nos|Par|para|e\.g|i\.e|etc|c|ca|approx|vs|cf|St|Mr|Mrs|Ms|Dr|Prof|p|pp|vol|Q|Qs|Co|Ltd|Inc|Mt|Rd|Ave)|(?<![\d]\s?)\b[A-Z](?![\p{L}]))\.$/u;

interface Piece { start: number; end: number }

// A printed line that runs on into the next one: the PDF wrapped it. "Give two
// details about\nSamantha's personality" is one sentence, not two.
const RUNS_ON = /(?:\b(?:the|a|an|and|or|of|to|in|on|for|with|about|during|which|that|by|from|at|is|are|was|were|its|their|his|her|this|these|those|your|between|into|than|as|what|how|why|where|when|who|whose|whom)|,)\s*$/iu;
const OPENS_BLOCK = /^(?:[•◆▪●\-–]|\((?:iii|ii|iv|vi{1,3}|ix|x|i|v|[a-h])\)|\d{1,2}[.)]\s|OR\b)/u;
// Words that open an instruction: a single capital before one of these ends a
// sentence ("from A to B. Give your answer …"), where "J. Smith" does not.
const OPENS_TASK = /^\s+(?:Give|Write|Find|Calculate|Explain|Describe|Name|State|What|How|Why|Which|Where|When|Who|Show|Hence|Use|Draw|Identify|Outline|Discuss|Suggest|Evaluate|Compare|List|Sketch|Determine|Work|Label|Complete|Justify|Estimate|Prove|Verify|Express|Solve)\b/;

function sentences(raw: string, start: number, end: number): Piece[] {
  const out: Piece[] = [];
  let s = start;
  const re = /[.?!][)”’"“»]*(?=\s+[\p{Lu}(“"‘„«\d•◆▪])|\n{1,}/gu;
  re.lastIndex = start;
  let m: RegExpExecArray | null;
  while ((m = re.exec(raw)) && m.index < end) {
    const cut = m[0] === '\n' || m[0].startsWith('\n') ? m.index : m.index + m[0].length;
    if (m[0][0] === '\n' && m[0].length === 1) {
      const before = raw.slice(s, m.index).trimEnd();
      const after = raw.slice(m.index + 1, end).trimStart();
      const wrapped = before && !/[.?!:;]$/.test(before) && !OPENS_BLOCK.test(after)
        && (RUNS_ON.test(before) || (/[\p{Ll},]$/u.test(before) && /^\p{Ll}/u.test(after)));
      if (wrapped) continue;
    }
    if (m[0][0] === '.') {
      const tail = raw.slice(Math.max(s, m.index - 6), m.index + 1);
      const initial = /(?<![\p{L}\d])[A-Z]\.$/u.test(tail) && OPENS_TASK.test(raw.slice(m.index + 1, m.index + 20));
      if (!initial && (NO_BREAK_AFTER.test(tail) || /\d\.$/.test(raw.slice(m.index - 1, m.index + 1)) && /^\d/.test(raw.slice(m.index + 1)))) continue;
    }
    if (cut > s && raw.slice(s, cut).trim()) out.push({ start: s, end: cut });
    s = cut;
  }
  if (end > s && raw.slice(s, end).trim()) out.push({ start: s, end });
  // "… a verbal pitch to the committee in which you: promote …, impress …":
  // the set-up before the colon and the jobs after it are separate pieces.
  const split: Piece[] = [];
  for (const p of out) {
    const lead = JOB_LIST_LEAD.exec(raw.slice(p.start, p.end));
    const at = lead ? p.start + lead.index + lead[0].length : -1;
    if (lead && at < p.end - 3 && new RegExp(`^(?:[-–•]\\s*)?(?:${JOB_VERBS})(?![\\p{L}])`, 'iu').test(raw.slice(at, p.end))) {
      split.push({ start: p.start, end: at }, { start: at, end: p.end });
    } else split.push(p);
  }
  return split;
}

// ---------------------------------------------------------------------------
// Segmentation: OR alternatives, printed parts.
// ---------------------------------------------------------------------------

interface Part { start: number; end: number; ref: string; altGroup?: 'A' | 'B' }

const PART_LABEL = /(?<![\p{L}\p{N}])\((?:iii|ii|iv|vi{1,3}|ix|x|i|v|[a-h])\)(?=\s)/gu;

function splitAlternatives(raw: string): Array<{ start: number; end: number; altGroup?: 'A' | 'B' }> {
  const re = /(?:(?<=[.?!)])\s+|\n\s*)OR(?=\s*\n|\s+[\p{Lu}(])/u;
  const m = re.exec(raw);
  if (!m) return [{ start: 0, end: raw.length }];
  const orStart = m.index + m[0].indexOf('OR');
  return [
    { start: 0, end: m.index, altGroup: 'A' },
    { start: orStart + 2, end: raw.length, altGroup: 'B' },
  ];
}

function splitParts(raw: string, start: number, end: number, altGroup?: 'A' | 'B'): Part[] {
  const labels: Array<{ index: number; label: string }> = [];
  const ROMAN = ['(i)', '(ii)', '(iii)', '(iv)', '(v)', '(vi)', '(vii)', '(viii)', '(ix)', '(x)'];
  const follows = (prev: string, next: string) => {
    const r = ROMAN.indexOf(prev);
    if (r >= 0) return ROMAN[r + 1] === next;
    return /^\([a-h]\)$/.test(prev) && next === `(${String.fromCharCode(prev.charCodeAt(1) + 1)})`;
  };
  for (const m of raw.slice(start, end).matchAll(PART_LABEL)) {
    const index = start + (m.index ?? 0);
    const before = raw.slice(start, index).trimEnd();
    // A label only opens a part at the start, after a line break or after
    // sentence punctuation — never mid-sentence ("see part (ii) above") —
    // unless it continues a run already open: "(i) Design of products (ii)
    // Manufacturing".
    const opens = !before || /[.?!:;\n)]$/.test(before) || /\n\s*$/.test(raw.slice(start, index));
    const continues = labels.length > 0 && follows(labels[labels.length - 1].label, m[0]);
    if (!opens && !continues) continue;
    labels.push({ index, label: m[0] });
  }
  // Numbered items "1. … 2. …" at the start or after a colon.
  const numbered: Array<{ index: number; label: string }> = [];
  for (const m of raw.slice(start, end).matchAll(/(?:^|(?<=[:.?\n]\s*)|\n)\s*([1-8])\.\s+(?=\S)/g)) {
    const at = start + (m.index ?? 0) + m[0].indexOf(m[1]);
    numbered.push({ index: at, label: `${m[1]}.` });
  }
  const seqOk = numbered.length >= 2 && numbered.every((n, i) => n.label === `${i + 1}.`);
  const chosen = labels.length >= 2 || (labels.length === 1 && labels[0].index === start)
    ? labels
    : seqOk ? numbered : [];
  if (!chosen.length) return [{ start, end, ref: '', altGroup }];
  const parts: Part[] = [];
  if (chosen[0].index > start && raw.slice(start, chosen[0].index).trim()) {
    parts.push({ start, end: chosen[0].index, ref: '', altGroup });
  }
  chosen.forEach((label, i) => {
    const s = label.index + label.label.length;
    const e = chosen[i + 1]?.index ?? end;
    // A numbered item with nothing after it is an answer frame ("1. 2."
    // under "Name two …"), not another task.
    if (raw.slice(s, e).trim().length <= 2) return;
    parts.push({ start: s, end: e, ref: label.label, altGroup });
  });
  return parts;
}

// ---------------------------------------------------------------------------
// Slot patterns.
// ---------------------------------------------------------------------------

const LEADING = /^(?:If\b[^,]{3,80},|Using (?:your knowledge of|notes and freehand sketches|the [^,]{2,60})[^,]{0,60},|In your preparation of [^:]{2,80}:|Under the terms of [^,]{2,80},|To a scale of [^,]{2,40},|In your view,|According to [^,]{2,80},|From your knowledge of [^,]{2,80},|With (?:the aid of|reference to) [^,]{2,80},|In the case of [^,]{2,60},)\s*/i;

const WH_FORMS = [
  'what information does this give about', 'to what extent do you agree or disagree with', 'to what extent',
  'what evidence is there', 'what evidence do you find', 'what do you consider', 'what do you think',
  'do you agree or disagree with', 'do you agree or disagree that', 'do you agree or disagree', 'do you think', 'do you agree', 'how would you best describe', 'what is the purpose of', 'what is meant by',
  'what effect', 'what caused', 'what makes', 'what is', 'what are', 'what was', 'what were', 'what does', 'what did',
  'how does', 'how did', 'how do', 'how is', 'how are', 'how can', 'how would', 'how will', 'how could', 'how should', 'how might', 'how many', 'how much',
  'what will', 'what would', 'what could', 'what should', 'why would', 'why should', 'why might',
  'why do', 'why does', 'why did', 'why is', 'why are', 'why was', 'why were', 'why',
  'to what', 'under which', 'under what', 'in which', 'from which', 'on which', 'at which', 'to which', 'by which',
  'for which', 'with which', 'of which', 'during which', 'in whose', 'to whom', 'from whom', 'by whom',
  'by how much', 'by how many', 'how long', 'how far', 'how often', 'for how long', 'what did', 'what do',
  'in what way', 'in what ways', 'in what', 'at what', 'on what', 'by what', 'for what', 'from what', 'with what', 'to whom', 'of what',
  'where are', 'where is', 'where does', 'where do', 'where', 'when did', 'when was', 'when', 'which', 'who', 'what', 'how',
];

const GENERIC_UNIT_NOUNS = /^(?:reasons?|ways?|examples?|details?|points?|differences?|similarities?|facts?|uses?|pieces? of evidence|texts?|phrases?)\b/i;

const NUMBER_WORDS: Record<string, number> = {
  one: 1, two: 2, three: 3, four: 4, five: 5, six: 6, seven: 7, eight: 8,
};

const COUNT_AFTER_CMD = /^(?:(any\s+(?:one|two|three|four|five|six)|at least\s+(?:one|two|three|four|five)|each of the following|each|all|both|one|two|three|four|five|six|seven|eight|[2-8])(?![\p{L}\p{N}.])((?:\s+(?:different|distinct|separate|possible|other|main|major|key|specific|named|important|relevant|suitable|significant|further|additional))*))/iu;

// Each trigger begins a condition that runs to the next clause boundary.
const CONDITION_TRIGGERS = [
  '(?:developing|supporting|illustrating) your (?:response|answer|discussion|points?|views?|argument) (?:with|by) (?:close |detailed )?reference to',
  'with reference to', 'with specific reference to', 'with particular reference to', 'by reference to', 'in relation to', 'referring to',
  'making (?:detailed )?reference in your answer to',
  'in the context of', 'in the light of', 'according to', 'using evidence from', 'using your knowledge of', 'using the following',
  'using the', 'using', 'from your knowledge of', 'in your view', 'with analysis of', 'making detailed reference to',
  'making reference to', 'with the aid of', 'from first principles', 'in terms of', 'with respect to(?= [a-zA-Zθφ](?![\\p{L}]))', 'prior to', 'during',
  'that you have studied', 'that you studied', 'you have studied', 'by placing', 'showing', 'correct to', 'to the nearest',
  'as a method of', 'as preparation for', 'to ensure', 'to support your answer', 'in support of', 'supported by', 'giving',
  'stating', 'including', 'other than', 'apart from', 'excluding', 'except', 'outside of', 'outside', 'not in',
  'under the following headings', 'under the headings', 'in your own words', 'in your answer', 'for each', 'in each case',
  'refer in your answer to', 'in your answer refer to', 'include discussion of', 'include reference to', 'refer to',
  'from the (?:text|passage|extract|article|poem|story|document|source|letter|interview|report)s?',
  'in Ireland', 'outside Ireland', 'in Europe', 'in the EU', 'in the European Union', 'on your drawing',
  'if', 'unless', 'assuming', 'given that', 'where(?= [a-zA-Z](?:\\s*,|\\s*[∈=<>≤≥]))', 'in English', 'in Irish',
  'in the form', 'in its simplest form', 'in simplest form', 'as a fraction', 'as a decimal', 'as a percentage',
  'by ticking', 'with a tick', 'by placing a tick', 'placing a tick', 'by putting', 'giving your answer',

  'when', 'whenever', 'available to', 'required to', 'required for', 'to a scale of', 'on your drawing', 'as part of',
  'for (?:a|an|the) (?:open |closed |irish |local |national |global )?(?:economy|business|home|workplace|farm|week|month|year|day|household|community|society|region|country|school|family|consumer|employee|employer)',
  'in (?:a|an|the) (?:workplace|business|home|farm|laboratory|region|circuit|economy|school|community)',
  'between \\d{4} and \\d{4}', 'in \\d{4}', 'since \\d{4}', 'before \\d{4}', 'after \\d{4}',
  'in (?:metres|meters|seconds|minutes|hours|kg|kilograms|grams|litres|cm|mm|km|euro|degrees|kelvin|joules|watts|newtons)(?=\\s*(?:[,.;)]|$|and\\b|correct\\b|to\\b))',
];
const TRIGGER_RE = new RegExp(`(?<![\\p{L}\\p{N}])(?:${CONDITION_TRIGGERS.join('|')})(?![\\p{L}\\p{N}])`, 'giu');
// A gerund after a preposition is the object, not a limit: "one benefit of
// using a flux" asks about using the flux.
const GERUND_TRIGGER = /^(?:using|giving|stating|including|showing|referring|making|placing|putting)/i;
const AFTER_PREPOSITION = /\b(?:of|for|by|in|on|about|from|to|at|with|without|when|while|before|after)\s+$/i;
// Time words inside a question are the question ("What took place during the
// festival?"), not a limit on the answer.
const QUESTION_TIME_TRIGGER = /^(?:during|when|whenever|prior to|in \d{4}|since|before|after|between)/i;
function triggersIn(raw: string, start: number, end: number, actionKey = ''): RegExpMatchArray[] {
  TRIGGER_RE.lastIndex = 0;
  return [...raw.slice(start, end).matchAll(TRIGGER_RE)].filter(t => {
    const at = start + (t.index ?? 0);
    if (GERUND_TRIGGER.test(t[0]) && AFTER_PREPOSITION.test(raw.slice(Math.max(0, at - 12), at))) return false;
    // "the number of people using the services …": a participle after a
    // noun describes it. A limit is set off: ", using …", "Using …".
    const agent = /\b(?:people|persons|customers|consumers|students|pupils|farmers|users|workers|employees|businesses|firms|companies|households|children|adults|patients|athletes|players|families|visitors|tourists|drivers|shoppers|individuals|those)\s+$/i;
    if (/^(?:giving|stating|showing|including)$/i.test(t[0]) && !/(?:^|[,(;:–—]\s*|\b(?:and|or|by|when|while|before|after|without)\s+)$/i.test(raw.slice(Math.max(0, at - 12), at)) && at > start) return false;
    if (/^using\b/i.test(t[0]) && agent.test(raw.slice(Math.max(0, at - 16), at))) return false;
    if (/^(?:wh-|explain-how|to-what-extent)/.test(actionKey) && QUESTION_TIME_TRIGGER.test(t[0])) return false;
    // "Describe what happens during the primary stage", "Outline two
    // challenges when starting a new business": the occasion is what the
    // answer is about. In a calculation a "when" clause with values is given.
    if (/^(?:when|whenever|during|prior to)$/i.test(t[0])) {
      const clause = raw.slice(at, Math.min(end, at + 120));
      if (!(CALC_KEYS.has(actionKey) || /^(?:prove|derive)$/.test(actionKey)) || !/\d/.test(clause.split(/[.;?]/)[0])) return false;
    }
    // "why a company would locate in Ireland": a place a verb needs.
    if (/^(?:in|outside) (?:ireland|europe|the eu|the european union)$/i.test(t[0]) && /\b(?:locate|located|locating|live|lives|living|based|set up|invest|investing|work|working|move|moved|operate|operating|trade|trading|sell|selling|grow|grown|found|made|produced|built)\s+$/i.test(raw.slice(Math.max(0, at - 14), at))) return false;
    if (/^either$/i.test(t[0]) && /\b(?:in|of|for|with|to|on|from|by|at|about|between)\s+$/i.test(raw.slice(Math.max(0, at - 10), at))) return false;
    return true;
  });
}
// A participle in front of a place/exclusion trigger belongs to it:
// "found outside of Ireland", "located in the …".
const PARTICIPLE_BEFORE = /\b(?:found|located|situated|grown|used|made|produced|seen|studied|based|built|practised|practiced)\s+$/i;

// Material nouns that name supplied material on their own ("the diagram",
// "the passage"), and nouns that only do with a pointer: "the model shown"
// is material, "the model of the atom" is an idea; "the figure" in an art
// question is a human figure.
const STRONG_MATERIAL = 'diagrams?|tables?|graphs?|pie charts?|charts?|photographs?|photos?|word bank|article|extracts?|passages?|texts?|maps?|cartoons?|(?<!(?:neural|nerve|reflex|brain|nervous) )circuits?(?: diagrams?)?|drawings?|poem|poster|advertisement|pseudo-code|flowchart|timeline|documents?|scheduling network|cashflow forecast|parts list|case study|quotation|recipe|menu|results table|bar chart|line graph|notice board';
// "the image distance v", "the source of several gases", "these images" in a
// poem: material only with a pointer ("the image below").
const WEAK_MATERIAL = 'list|models?|figures?|sketch(?:es)?|data|information|results|code|algorithm|equation|network|forecast|situation|scenario|statement|label|images?|pictures?|sources?';
const MATERIAL_POINTER = '(?:\\s+(?:below|above|shown|provided|supplied|opposite|overleaf|on the next page))';
const MATERIAL_RE = new RegExp(
  `\\b(?:the|this|these|each)\\s+(?:(?:following|above|below|accompanying|attached|given|printed)\\s+(?:labelled\\s+|unlabelled\\s+)?(?:${STRONG_MATERIAL}|${WEAK_MATERIAL})${MATERIAL_POINTER}?|(?:labelled\\s+|unlabelled\\s+)?(?:${STRONG_MATERIAL})${MATERIAL_POINTER}?|(?:${WEAK_MATERIAL})${MATERIAL_POINTER})\\b`,
  'gi',
);
// "The reaction profile diagram for the reaction X → Y … is shown below".
const MATERIAL_LONG = /\b(?:The|the|This|this)\s+(?:[\p{L}-]+\s+){1,3}(?:diagram|graph|table|chart|map|photograph|drawing)(?=[^.]{0,80}\b(?:is|are)\s+(?:shown|given|printed)\b)/gu;
const MATERIAL_ADJ = /\b(?:the|this|these)\s+(?:aerial|Ordnance Survey|OS|weather|synoptic|satellite|oblique)\s+(?:photograph|photo|map|image|chart)s?\b/gi;
// "sitting at the left of the table" is furniture, not material.
const notMaterial = (text: string, index: number, match: string) =>
  (/^\S+\s+tables?$/i.test(match) && /\b(?:at|around|of|on|under|beside|across)\s+$/i.test(text.slice(Math.max(0, index - 12), index)))
  // The grid the answers go in: "Fill out the table".
  || /\b(?:fill (?:out|in)|complete|copy)\s+$/i.test(text.slice(Math.max(0, index - 14), index))
  // "Write the text of a talk", "the text for a podcast": the student's own writing.
  || (/^the texts?$/i.test(match) && /^\s+(?:of|for)\s+(?:a|an|the|your)\s+(?:[\p{L}-]+\s+){0,2}(?:talk|speech|podcast|article|blog|letter|review|introduction|address|commentary|pitch|dialogue|report|radio|contribution|presentation|feature|editorial|diary|interview|announcement)/iu.test(text.slice(index + match.length, index + match.length + 60)));
const NAMED_RE = /\b(?:Fig\.?\s*[A-Z]?-?\d+|Figure\s+[A-Z0-9]+|(?:Document|Source|Extract|Image|Photograph|Table|Text|TEXT|Graph|Diagram|Map)\s+[A-Z0-9]+(?:\s+on Paper\s+[A-Z])?)\b/g;
const LOCATOR_RE = /\((?:para(?:graph)?|Par\.|section|lines?|Alt|Part|Abschnitt|Absatz|Zeile|párrafo|parágrafo|paragraphe|paragrafo|sezione|dalis|część|akapit|línea|ligne|riga|kappale|odsek|bekezdés)\s*[\d\s–-]+\)|\(\s*\d+\s+(?:dalis|bekezdés|odsek|kappale|rész)\s*\)|\bAlt\s+\d+\b|\b(?:paragraph|para\.?|Par\.|section)\s+\d+\b|\blines?\s+\d+\s*[–-]\s*\d+\b/gi;
const OPTIONS_RE = /\[[^\]]*\/[^\]]*\]/g;
const VISUAL = /diagram|graph|chart|photo|picture|image|map|cartoon|circuit|figure|drawing|sketch|model|Fig/i;

const TAIL_UNIT = /^(?:(?:Explain|Justify) your (?:answer|choice)|Give (?:a )?reasons? for your (?:answer|choice)|Support your answer|Illustrate your answer)/i;
// "Support your response with reference to the poem." / "Develop your
// response with reference to your chosen text.": how the answer before it
// must be backed up.
const SUPPORT_TAIL = /^(?:Support|Develop|Back up)\s+your\s+(?:answer|response|discussion|points?|views?|argument|opinion|essay|ideas?|analysis)\b/i;
// "Develop at least two points in your response." / "Make three points in
// your response.": how many points, for the job before it.
const POINTS_SENTENCE = /^(?:Develop|Make|Argue|Present|Offer|Discuss)\s+((?:at least|any)\s+)?(one|two|three|four|five|six)\s+((?:[\p{L}-]+\s+){0,2}?(?:points?|reasons?|examples?|ways?|arguments?|benefits?|recommendations?|features?|factors?|ideas?|aspects?))(?![\p{L}])/iu;
// "Your plan should include at least four specific benefits."
const YOUR_SHOULD = /^(?:Your\s+[\p{L}-]+(?:\s+[\p{L}-]+)?|The\s+[\p{L}-]+\s+you\s+(?:give|write|deliver|make|produce|present))\s+(?:should|must)\s+/iu;
const YOUR_SHOULD_COUNT = /\b((?:at least|at most|exactly|no more than|up to)\s+)?(one|two|three|four|five|six|seven|eight)\s+((?:[\p{L}-]+\s+){0,2}?[\p{L}-]+s)(?![\p{L}])/iu;
// Printed for the whole answer: drawing conventions, "work must be shown",
// a permission.
const WHOLE_SENTENCE = /^(?:\(?\s*Unless otherwise (?:stated|specified|indicated)\b|(?:Relevant |All )?(?:supporting )?(?:work(?:ings?)?|calculations) must be shown\b|You (?:may|can) (?:use|include|draw|refer)\b)/i;
// A sentence that says how the answer must be given, not what to answer. It
// limits the task before it ("Give your answer in its simplest form").
const TAIL_CONDITION = /^(?:Indicate your (?:choice|sector|option|answer|chosen)\b|(?:Put|Place) a tick\b|Tick\s*(?:\([^)]{1,4}\)\s*)?(?:the|one|a) (?:correct|appropriate|relevant)?\s*(?:box|boxes|answer|option)?\b|Show (?:all )?(?:your )?(?:workings?|work|calculations)\b|Use [^.]{0,60}\bto support your answer|Refer to the text in support of your answer|(?:Give|Write|Express|Leave|State|Show) (?:your|each|the|all|both) (?:final )?answers?\b|Write (?:your )?answers? (?:in|on)\b|(?:In your answer,? )?refer to\b|Refer in your answer to\b|Include\b(?!\s+(?:one|two|three|four|five|six|[2-6])\b)|N\.\s?B\.|You must\b|You should\b|Your answer (?:should|must)\b|Make (?:detailed )?reference to\b|Any omitted dimensions)/i;
// "Name two." / "Give four details." after a question: how many, for that question.
const COUNT_SENTENCE = /^(?:Give|Name|State|List|Mention|Identify|Write down)\s+(?:(?:any|at least)\s+)?(one|two|three|four|five|six)(?:\s+([\p{L}]+(?: of information)?))?\s*[.?!]?\s*$/iu;
const DETAILS_SENTENCE = /^Give (?:full |more )?details\s*[.?!]?\s*$/i;
const PAREN_COUNT = /^\(\s*(one|two|three|four|five|six)\s+(points?|reasons?|examples?|details?|ways?|pieces of information)\b[^)]*\)\s*\.?\s*$/i;
const CARD_RULE = /\b(?:Answer in (?:English|Irish)|about \d+ words(?: in total)?|Refer to the text in support of your answer|Indicate your (?:choice|answer) by (?:putting|writing) (?:the letter )?A, B, C or D)\b|\(\s*(?:about\s+)?\d+\s*words?(?:\s+in total)?\s*\)|\(Is leor \d+ focal\.?\)|(?<=\banswer,?\s)in English\b/gi;

const RUBRIC = /^(?:Question \d+|Q\d+\([a-z]\)|Answer (?:either|any|all)\b|Read the (?:article|information|passage|text|extract)\b[^.]*\bthen answer\b|Section [A-Z]\b|You will be shown|Study the\b|Look at the\b|Examine the\b|Read the\b)/i;

// ---------------------------------------------------------------------------
// Unit building.
// ---------------------------------------------------------------------------

interface Clause { start: number; end: number; command: CommandMatch | null }

/** Command candidates inside a sentence, as offsets into the raw string. */
function commandsIn(raw: string, start: number, end: number): CommandMatch[] {
  return commandMatches(raw.slice(start, end)).map(m => ({ ...m, index: m.index + start, end: m.end + start }));
}

// A second instruction the shared lexicon misses: "… and include one example".
const SECOND_VERB = /(?:,\s*and|\s(?:and|then))\s+(?:briefly\s+|clearly\s+|fully\s+|carefully\s+)?(include|project|label|annotate|give|state|name|list|suggest|justify|identify|draw|sketch|show|calculate|find|write|comment|discuss|explain|describe|outline)(?![\p{L}])|,\s*and\s+(what|how|why|where|when|who)(?![\p{L}])|,\s+(?:briefly\s+|clearly\s+)?(outline|explain|describe|identify|discuss|suggest|justify|evaluate|assess|analyse|state|give|name)(?=\s+(?:the|their|its|his|her|how|why|what|which|a|an|one|two|three)\b)|,\s+(?:briefly|clearly)\s+(describe|explain|outline|discuss|state|identify)(?![\p{L}])|,?\s+and,?\s+hence,?\s+(find|show|prove|calculate|verify|deduce|write|express|solve|evaluate|determine|sketch|draw)(?![\p{L}])|\s+and\s+((?:at|in|by|for|to|from|on|with|under)\s+what|how (?:many|much|long|far|fast|often))(?![\p{L}])/giu;

// The jobs a composing task lists after "you should:" / "in which you:":
// "promote your preferred theme …, impress the committee …, and nominate …".
const JOB_LIST_MARK = 'job-list';
const JOB_LIST_LEAD = /\b(?:you (?:should|must|will|need to|are asked to)|in which you|where you|in which they|which should)\s*:\s*/i;
const JOB_VERBS = 'explore|introduce|provide|warn|urge|share|promote|impress|nominate|reflect on|reflect|recommend|offer|persuade|convince|encourage|invite|advise|inform|express|highlight|consider|celebrate|thank|welcome|challenge|propose|argue|give|state|outline|discuss|describe|explain|identify|name|list|include|mention|recall|imagine|tell|compare|evaluate|assess|examine|present|set out|respond to|respond|suggest|create|design|develop|make|select|choose|convey|capture|reveal|show|demonstrate|justify|comment on|speculate|predict|acknowledge|address|defend|criticise|praise|appeal|ask|answer|summarise|analyse|interpret|review|rank|rate|detail|pay tribute|apologise|remind|announce|question|call on|seek to|attempt to|try to|aim to';

/** Split a task sentence into one clause per command ("Name … and explain …"). */
function clausesOf(raw: string, s: Piece): Clause[] {
  const cmds = commandsIn(raw, s.start, s.end);
  const lead = JOB_LIST_LEAD.exec(raw.slice(s.start, s.end));
  const leadBefore = /\b(?:you (?:should|must|will|need to|are asked to)|in which you|where you|in which they|which should)\s*:\s*$/i.test(raw.slice(Math.max(0, s.start - 60), s.start));
  if (lead || leadBefore) {
    const from = lead ? s.start + lead.index + lead[0].length : s.start;
    const verbAt = new RegExp(`(?:^(?:[-–•]\\s*)?|,\\s*(?:and\\s+)?|\\s+and\\s+|;\\s*(?:and\\s+)?|\\s[-–•]\\s+)(${JOB_VERBS})(?![\\p{L}])`, 'giu');
    for (const m of raw.slice(from, s.end).matchAll(verbAt)) {
      const index = from + (m.index ?? 0) + m[0].length - m[1].length;
      const known = cmds.findIndex(c => Math.abs(c.index - index) < 2);
      // Marked, so a short-answer gloss is not given to a job the piece develops.
      if (known >= 0) { cmds[known] = { ...cmds[known], demand: { ...cmds[known].demand, commonTrap: JOB_LIST_MARK } }; continue; }
      cmds.push({ demand: { surface: m[1], requiredAction: '', answerShape: '', commonTrap: JOB_LIST_MARK }, index, end: index + m[1].length, match: m[1] });
    }
  }
  // "The alkaline earth metals make up Group 2 and include …" is a statement:
  // its "and include" is prose, not a second instruction.
  const statement = /^\s*(?:The|A|An|This|These|Those|It|They|There|Its|Their|Some|Many|Most|All)\s/.test(raw.slice(s.start, s.end)) && !commandsIn(raw, s.start, s.end).length;
  for (const m of statement ? [] : raw.slice(s.start, s.end).matchAll(SECOND_VERB)) {
    const word = m.slice(1).find(Boolean) as string;
    const index = s.start + (m.index ?? 0) + m[0].length - word.length;
    if (cmds.some(c => Math.abs(c.index - index) < 2)) continue;
    cmds.push({ demand: { surface: word, requiredAction: '', answerShape: '', commonTrap: '' }, index, end: index + word.length, match: word });
  }
  // "you should: identify …, explain why …": a command straight after a colon
  // or semicolon opens a task even where the shared lexicon misses it.
  for (const m of raw.slice(s.start, s.end).matchAll(/[:;]\s+(identify|describe|explain|outline|discuss|state|name|list|give|suggest|evaluate|examine|analyse|compare|calculate|draw|write)(?![\p{L}])/giu)) {
    const index = s.start + (m.index ?? 0) + m[0].length - m[1].length;
    if (cmds.some(c => Math.abs(c.index - index) < 2)) continue;
    cmds.push({ demand: { surface: m[1], requiredAction: '', answerShape: '', commonTrap: '' }, index, end: index + m[1].length, match: m[1] });
  }
  cmds.sort((a, b) => a.index - b.index);
  // "In what direction is it moving and at what speed …?": the second
  // question splits off even when the first opens without a lexicon command.
  const opener = { demand: { surface: '', requiredAction: '', answerShape: '', commonTrap: '' }, index: s.start, end: s.start, match: '' };
  if (cmds.length === 1 && cmds[0].index > s.start + 3 && /^\s*\p{Lu}/u.test(raw.slice(s.start, s.end))
    && !commandsIn(raw, s.start, cmds[0].index).length && /\band\s+$/i.test(raw.slice(s.start, cmds[0].index))) cmds.unshift(opener);
  if (cmds.length <= 1) return [{ start: s.start, end: s.end, command: cmds[0] ?? null }];
  const out: Clause[] = [];
  let cursor = s.start;
  cmds.forEach((cmd, i) => {
    if (i === 0) return;
    const between = raw.slice(cmds[i - 1].end, cmd.index);
    const joined = /(?:,\s*(?:and\s+)?|\s+and\s+|\s+then\s+|[.;:]\s*|\s[-–•]\s*)(?:briefly\s+|clearly\s+)?$/i.test(between)
      || /[.?!;:]/.test(between);
    if (!joined) return;
    // Keep "briefly"/"clearly" — and "hence", which ties this task to the
    // last — with the command they belong to.
    const adverb = /(?:briefly|clearly|hence,?|hence or otherwise,?)\s+$/i.exec(raw.slice(cmds[i - 1].end, cmd.index));
    const cut = adverb ? cmd.index - adverb[0].length : cmd.index;
    const connector = /(?:,?\s*and,?\s+hence,?\s*|,?\s+hence,?\s*|,\s*(?:and\s+)?|\s+and\s+|\s+then\s+)$/i.exec(raw.slice(cursor, cut));
    out.push({ start: cursor, end: connector ? cut - connector[0].length : cut, command: null });
    cursor = cut;
  });
  out.push({ start: cursor, end: s.end, command: null });
  // Re-attach each clause's own command.
  return out.map(c => ({ ...c, command: cmds.find(m => m !== opener && m.index >= c.start && m.index < c.end) ?? null }));
}

// A limit that is only its trigger ("in relation to" before a list) says
// nothing; "that you have studied" or "in English" is a whole limit.
const emptyLimit = (sp: KPSpan, trigger: string) =>
  sp.display.length <= trigger.trim().length && /\b(?:to|of|in|on|for|with|from|by|at|as|than|between|during|using|the|following)$/i.test(trigger.trim());

const depthAt = (text: string, i: number) => {
  let d = 0;
  for (let k = 0; k < i; k += 1) {
    if (text[k] === '(') d += 1;
    else if (text[k] === ')' && d > 0) d -= 1;
  }
  return d;
};

// A limit that introduces a list runs through its commas: "Refer in your
// answer to space, function, layout and lighting".
const LIST_TRIGGER = /(?:headings?|refer(?: in your answer)? to|include (?:discussion of|reference to)|^where|^in terms of)$/i;

/**
 * Where a limit ends. Brackets belong to it — "(not in Ireland)" does not end
 * "a European region" — and a heading list after a colon runs to the end of
 * the sentence.
 */
function conditionEnd(raw: string, from: number, end: number, trigger = ''): number {
  const rest = raw.slice(from, end);
  const listy = LIST_TRIGGER.test(trigger.trim());
  let cut = end;
  let depth = 0;
  for (let i = 0; i < rest.length; i += 1) {
    const ch = rest[i];
    if (ch === '(') { depth += 1; continue; }
    if (ch === ')') {
      if (depth > 0) { depth -= 1; continue; }
      cut = from + i;
      break;
    }
    if (depth > 0) continue;
    const boundary = i + 1 >= rest.length || /\s/.test(rest[i + 1]);
    if (!boundary || !/[,;.?!:]/.test(ch)) continue;
    // "with reference to one of the following: • Mining • …": the list after
    // the colon is options, not the limit; a heading list runs on.
    if (ch === ':' && (listy || /(?:headings?|refer(?: in your answer)? to)\s*$/i.test(rest.slice(0, i)))) {
      const stop = /[.?!](?=\s|$)/.exec(rest.slice(i));
      cut = stop ? from + i + stop.index : end;
      break;
    }
    if (listy && (ch === ',' || ch === ';')) continue;
    cut = from + i;
    break;
  }
  const andCmd = /\s+(?:and|or)\s+(?=(?:state|name|explain|describe|give|identify|discuss|outline|suggest|evaluate|calculate|list|draw|include|label)\b)/i.exec(rest);
  if (andCmd && from + andCmd.index < cut) cut = from + andCmd.index;
  // "(one point)", "(10 marks)" after a limit belong to the answer, not the limit.
  const countParen = /\s*\(\s*(?:one|two|three|four|five|six|\d+)\s+(?:points?|marks?|words?|reasons?|details?)[^)]*\)/i.exec(rest);
  if (countParen && from + countParen.index < cut) cut = from + countParen.index;
  // "if all ash trees in Ireland died": a conditional clause keeps its own
  // place and time words.
  const clausal = /^(?:if|unless|assuming|given that|when|whenever|where|while)$/i.test(trigger.trim());
  if (!listy && !clausal) {
    // Stop at the next limit too, so chained limits stay separate — except
    // words that sit inside a limit ("when one character was either …").
    for (const t of triggersIn(raw, from, cut)) {
      const i = t.index ?? 0;
      if (i <= 3 || depthAt(rest, i) > 0 || /^(?:either|you think|you consider|in english|in irish|required to|required for)$/i.test(t[0])) continue;
      cut = from + i;
      break;
    }
  }
  return cut;
}

// "Use de Moivre's theorem to write …": the method is a limit; the job is the
// verb after it.
// "By using a = dv/dt solve a differential equation …": the same, without "to".
const METHOD = /^((?:Use|Using|By using)\s+[^,.;?]{2,90}?)\s+(?:to\s+)?(?=(?:write|find|show|prove|calculate|solve|express|verify|determine|work out|evaluate|estimate|draw|construct|explain|describe|identify|investigate|obtain|derive|sketch|plot|factorise|simplify|convert)\b)/i;
// A manner limit straight after the command, with no commas round it:
// "Describe with the aid of a labelled diagram the gold foil experiment".
const MANNER = /^(?:with the aid of|using|by means of|with the help of|making use of)\s+(?:a |an |the )?(?:(?:labelled|clear|neat|suitable|annotated|freehand|fully labelled|well-labelled)\s+)*(?:diagrams?|sketch(?:es)?|drawings?|examples?|graphs?|notes(?: and (?:freehand )?sketches)?)(?:\s*\(s\))?\s*,?\s*/i;
// Words that belong to the command: "Give an account of", "Write out in
// full", "Comment on", "Explain the terms".
function actionTail(raw: string, aEnd: number, end: number, verb: string): number {
  const after = raw.slice(aEnd, end);
  const v = verb.toLowerCase().trim();
  const GENERAL = /^\s+(?:what is meant by(?![\p{L}])|how(?!\s+(?:[\p{L}]+ly|long|many|much|far|often|well|soon|big|large|fast|high|old|deep|wide|strong|important|successful|effective|accurate|reliable|useful|likely|close|quickly)\b)(?![\p{L}])|(?:why|whether|where|when)(?![\p{L}])|between(?![\p{L}])|the (?:underlined |following )?terms?(?![\p{L}])|briefly(?![\p{L}])|clearly(?![\p{L}])|in detail(?![\p{L}]))/iu;
  const general = GENERAL.exec(after);
  if (general) {
    const again = GENERAL.exec(after.slice(general[0].length));
    let more = again && /^\s+(?:briefly|clearly|in detail)$/i.test(general[0]) ? again[0].length : 0;
    const about = /^(?:write|talk|comment)$/.test(v) && /^\s+about(?![\p{L}])/iu.exec(after.slice(general[0].length + more))
      || /^(?:write|comment|reflect|elaborate|report|focus)$/.test(v) && /^\s+on(?![\p{L}])/iu.exec(after.slice(general[0].length + more));
    if (about) more += about[0].length;
    return aEnd + general[0].length + more;
  }
  const particle = v === 'give'
    ? /^\s+(?:an account of|an? (?:(?:brief|short|detailed|full|clear|reasoned)\s+)?(?:explanation|description|assessment|evaluation|analysis|outline|summary|definition|comparison|discussion|justification|interpretation|account)(?:\s+(?:of|for))?(?=\s|[.?!]|$)|(?:full |more )?details(?:\s+(?:of|about|on))?(?=\s|[.?!]|$))(?![\p{L}])/iu
    : /^(?:write|set|carry|fill|work|point|find|note|jot|sum|fill)$/.test(v)
      ? /^\s+(?:out in full|out|down|in full|up)(?![\p{L}])/iu
      : /^(?:comment|reflect|elaborate|expand|report|focus)$/.test(v)
        ? /^\s+on(?![\p{L}])/iu
        : null;
  const p = particle?.exec(after);
  return p ? aEnd + p[0].length : aEnd;
}

/** "In what direction is …", "Which county has …": the noun belongs to the question word when a verb follows it. */
function whNounEnd(raw: string, whStart: number, whEnd: number, end: number): number {
  const wh = raw.slice(whStart, whEnd).trim();
  // "What is said about Talgo?", "What was done to …": the passive verb
  // belongs to the question.
  if (/\b(?:is|are|was|were|has|have|had)$/i.test(wh)) {
    const participle = /^\s+(?:said|done|known|seen|made|given|taken|shown|meant|found|told|written|thought|felt|heard|described|mentioned|suggested|revealed|learned|learnt|discovered|decided|offered|planned|proposed|reported|expected|needed|required|used|achieved)\b/i.exec(raw.slice(whEnd, end));
    if (participle) return whEnd + participle[0].length;
  }
  // "How skilfully does Homer …": the adverb belongs to the question word.
  if (/^how$/i.test(wh)) {
    const adverb = /^\s+[\p{L}]{3,}ly(?![\p{L}])/iu.exec(raw.slice(whEnd, end));
    return adverb ? whEnd + adverb[0].length : whEnd;
  }
  if (!/^(?:what|which|whose|(?:to|under|in|into|from|on|at|by|for|with|of|during|between|about)\s+(?:what|which))$/i.test(wh)) return whEnd;
  const after = raw.slice(whEnd, end);
  // "What county is …", "What type of sculpture is …", "What kind of person
  // is …": the noun phrase before the verb is part of the question word.
  // A counted noun ("What two things did …") is left for How many.
  const AUX = '(?:is|are|was|were|did|does|do|has|have|had|can|could|would|should|will|might|may|must)';
  const noun = /^\s+(?!(?:one|two|three|four|five|six|seven|eight|the|a|an|this|that|these|those|his|her|their|its)\b)((?:[\p{L}-]+\s+){0,2}?[\p{L}-]{3,}(?:\s+of\s+(?:[\p{L}-]+\s+)?[\p{L}-]{3,})?)(?=(?:\s*\([^)]{1,30}\))?\s+AUX\b|\s*[?,]|\s*$)/iu;
  const np = new RegExp(noun.source.replace('AUX', AUX), 'iu').exec(after);
  if (np && !new RegExp(`\\b${AUX}\\b`, 'i').test(np[1])) return whEnd + np[0].length;
  // "At what point in the festival did …", "For what reason …": one noun
  // after a preposition's question word.
  if (/\s/.test(wh)) {
    const one = /^\s+(?!(?:one|two|three|four|five|six|the|a|an)\b)([\p{L}-]{3,})(?=\s+(?:in|of|on|at|for|to|from|with|by|during|between)\b)/iu.exec(after);
    if (one) return whEnd + one[0].length;
  }
  return whEnd;
}

const YES_NO = /^(?:((?:At|In|On|After|Before|During|From|By|Given|Based on|According to|Having|Throughout|Towards)\b[^?]{2,60}?),?\s+)?(do|does|did|is|are|was|were|can|could|would|should|has|have|had|will)\s+(?=\S)/i;
const HEAD_STOP = /^(?:of|in|on|for|to|from|with|by|at|that|which|who|whose|where|when|between|during|used|found|made|given|shown|than|as|about|into|within|across)$/i;

/** The noun a counted plan row is named after: "three key areas …" → area. */
function headNoun(focus: KPSpan | null): string | undefined {
  if (!focus) return undefined;
  const words = focus.display.split(/[,;:(]/)[0].split(/\s+/).filter(Boolean);
  // Step over the words that open the phrase: "the following", "each of the".
  while (words.length && /^(?:the|a|an|this|these|those|following|each|any|one|two|three|four|five|six|of|your|its|their)$/i.test(words[0])) words.shift();
  const window: string[] = [];
  for (const w of words) {
    if (HEAD_STOP.test(w) || /^(?:a|an|the|this|that|these|those|each|every|some|may|might|can|could|will|would|should|must|is|are|was|were|has|have|had|do|does|did)$/i.test(w)) break;
    window.push(w);
    if (window.length >= 5) break;
  }
  // "sport related scalar quantities mentioned …" → quantity; "one safety
  // benefit" → benefit.
  const plural = [...window].reverse().find(w => /[^s]s$|ies$|sses$/i.test(w) && !/^(?:is|was|has|this|its|as|us|thus|always|perhaps)$/i.test(w));
  const head = plural ?? [...window].reverse().find(w => !/(?:ed|ing)$/i.test(w));
  if (!head || !/^[\p{Ll}-]{3,18}$/u.test(head)) return undefined;
  return singular(head);
}

function buildUnit(
  raw: string, clause: Clause, ctx: { ref: string; altGroup?: 'A' | 'B'; id: string; from: 'q' | 'stem' },
): KPUnit | null {
  const { from } = ctx;
  let cur = clause.start;
  const end = clause.end;
  const conditions: KPSpan[] = [];
  const skipSpace = () => { while (cur < end && /\s/.test(raw[cur])) cur += 1; };
  skipSpace();
  // A printed bullet opens the clause; it is not part of the command.
  const bullet = /^[-–•◆▪●]\s+/.exec(raw.slice(cur, end));
  if (bullet) cur += bullet[0].length;

  // A1: a leading clause is a condition, and the command follows it.
  const lead = LEADING.exec(raw.slice(cur, end));
  let leadCount: KPSpan | null = null;
  if (lead) {
    const caseOf = /^In the case of\s+(.+?),\s*$/i.exec(lead[0]);
    if (caseOf) {
      const s0 = cur + lead[0].indexOf(caseOf[1]);
      leadCount = spanOf(from, raw, s0, s0 + caseOf[1].length);
    } else {
      const sp = spanOf(from, raw, cur, cur + lead[0].length);
      if (sp) conditions.push(sp);
    }
    cur += lead[0].length;
    skipSpace();
  }
  // A quotation printed before the question is what the question is about:
  // "“As an interior the Pantheon is unsurpassed.” Do you agree with …?"
  const quote = /^([‘“'"][^’”'"]{3,400}[’”'"])(?:\s*\([^)]{2,60}\))?\s+(?=\p{Lu})/u.exec(raw.slice(cur, end));
  let quoted: KPSpan | null = null;
  if (quote) {
    quoted = spanOf(from, raw, cur, cur + quote[1].length);
    cur += quote[0].length;
  }
  // "From the list above identify two alkanes": an opener with no comma.
  const yourOpener = /^((?:On|In) your (?:drawing|diagram|sketch|graph|answer ?book|answer sheet|sketch map))\s*,?\s+(?=\p{Ll})/u.exec(raw.slice(cur, end));
  if (yourOpener && EXTRA_VERBS.test(raw.slice(cur + yourOpener[0].length, end).replace(/^(?:clearly|carefully|neatly|also|now)\s+/i, ''))) {
    const sp = spanOf(from, raw, cur, cur + yourOpener[1].length);
    if (sp) conditions.push(sp);
    cur += yourOpener[0].length;
  }
  const bareOpener = /^((?:From|Using|In|On|Based on|According to) (?:the|this|these) (?:[^,.?]{2,40}?(?:above|below|provided|given|shown)|(?:text|passage|extract|article|poem|story|document|diagram|table|graph|source|letter|advertisement)))\s+(?=\p{Ll})/u.exec(raw.slice(cur, end));
  const openerUse: KPUse[] = [];
  if (bareOpener && EXTRA_VERBS.test(raw.slice(cur + bareOpener[0].length, end))) {
    const sp = spanOf(from, raw, cur, cur + bareOpener[1].length);
    if (sp) openerUse.push({ ...sp, kind: 'material' });
    cur += bareOpener[0].length;
  }
  // "In your talk, which can be serious or humorous, you should: identify …"
  const colonLead = /^([^:?]{0,200}?)(?:,\s*)?(?:you (?:should|must|may|might|could|will need to)|your [\p{L}]+ (?:should|must))\s*:\s*/iu.exec(raw.slice(cur, end));
  if (colonLead) {
    const sp = colonLead[1].trim().length > 3 ? spanOf(from, raw, cur, cur + colonLead[1].length) : null;
    if (sp) conditions.push(sp);
    cur += colonLead[0].length;
  }
  let command = clause.command;
  if (colonLead) command = commandsIn(raw, cur, end).find(m => m.index >= cur) ?? null;
  // "Using notes and a freehand sketch, describe …": the method runs to its
  // comma; "a freehand sketch" is a drawing named, not the command.
  const methodComma = /^((?:Use|Using|By using)\s+[^.;?]{2,120}?),\s+(?=\p{Ll})/u.exec(raw.slice(cur, end));
  const methodBare = METHOD.exec(raw.slice(cur, end));
  const method = methodComma && commandsIn(raw, cur + methodComma[0].length, end).some(m => m.index === cur + methodComma[0].length)
    ? methodComma
    : methodBare && !/\b(?:a|an|the|freehand|large|neat|labelled|annotated|simple|clear|rough|detailed)$/i.test(methodBare[1]) ? methodBare : null;
  if (method) {
    const sp = spanOf(from, raw, cur, cur + method[1].length);
    if (sp) conditions.push(sp);
    cur += method[0].length;
    command = commandsIn(raw, cur, end)[0] ?? null;
  }
  if (command && command.index < cur) command = commandsIn(raw, cur, end).find(m => m.index >= cur) ?? null;

  // Action: a lexicon command at the clause start (after an adverb), or a
  // question form.
  let action: KPSpan | null = null;
  let actionKey = 'other';
  let means = '';
  let henceStart = -1;
  const adverb = /^(?:briefly|clearly|carefully)\s+/i.exec(raw.slice(cur, end));
  let cmd = command && command.index <= cur + (adverb?.[0].length ?? 0) + 2 ? command : null;
  if (!cmd && command && /^\p{Lu}/u.test(command.match) && command.index - cur < 160
    && !/[.?!]\s*$/.test(raw.slice(cur, command.index)) && /[)\p{Lu}\p{Ll}]\s+$/u.test(raw.slice(cur, command.index))) {
    // A printed heading runs straight into a capitalised command:
    // "Irish Art and Modernism (c.1880 – 1960s) Analyse how …".
    cur = command.index;
    cmd = command;
  }
  if (!cmd && command && command.index - cur < 160) {
    // "In your opinion, …, argue that …": the command follows an opening
    // clause. The clause is kept as a condition when it is a qualifier, and as
    // material when it names what is supplied ("Given the following …,").
    const prefix = raw.slice(cur, command.index);
    if (/,\s*$/.test(prefix) || /^(?:and|then)\s+$/i.test(prefix.trim() + ' ')) {
      if (/^hence(?:,| or otherwise,)?\s*$/i.test(prefix)) {
        // "hence, find …": "hence" ties the job to the last and stays with it.
        henceStart = cur;
      } else if (/,\s*$/.test(prefix)) {
        const sp = spanOf(from, raw, cur, command.index);
        if (sp && /^(?:Given|From)\s+(?:the|this|these)\s/i.test(sp.display)) openerUse.push({ ...sp, kind: 'material' });
        else if (sp) conditions.push(sp);
      }
      cur = command.index;
      cmd = command;
    }
  }
  if (cmd) {
    if (henceStart >= 0) cur = henceStart;
    let aEnd = actionTail(raw, cmd.end, end, cmd.match.replace(/^(?:briefly|clearly|carefully)\s+/i, '').split(/\s+/)[0]);
    // A question word from the lexicon takes its full printed form:
    // "How many", "What did", "Which".
    if (/^(?:(?:at|in|by|for|to|from|on|with|under)\s+)?(?:what|which|how|why|where|when|who)(?:\s|$)/i.test(cmd.match.trim())) {
      const head = raw.slice(cur, end).toLowerCase();
      const wh = WH_FORMS.find(f => head.startsWith(f) && !/[\p{L}]/u.test(head[f.length] ?? ' '));
      if (wh && cur + wh.length > aEnd) aEnd = cur + wh.length;
      aEnd = whNounEnd(raw, cur, aEnd, end);
    }
    action = spanOf(from, raw, cur, aEnd);
    actionKey = keyFor(raw.slice(henceStart >= 0 ? cmd.index : cur, aEnd), raw.slice(aEnd, end));
    // A verb the lexicon has no reading for gets no gloss rather than a wrong one.
    means = MEANS[actionKey] ?? (firstSentence(cmd.demand.requiredAction) || (actionKey === 'other' ? '' : MEANS.state));
    // A job in a composing brief ("In your talk you should: give …") is
    // developed in the piece, not answered in a line.
    if (cmd.demand.commonTrap === JOB_LIST_MARK && /^(?:state|name|give|list|identify|other|tick|label)$/.test(actionKey)) means = MEANS['brief-job'];
    cur = aEnd;
  } else {
    // "By 1715, what was …?" / "Apart from ditches, what did …?": an opening
    // phrase before a question. The phrase is a condition.
    const opener = /^([^,?]{3,70}),\s+(?=(?:(?:to|in|for|from|on|at|by|with|under|during|into|between)\s+)?(?:what|which|whom|whose|how|why|where|when|who)\b[^?]*\?\s*$)/i.exec(raw.slice(cur, end))
      ?? /^(According to [^,?]{3,80}?)\s+(?=(?:what|which|how|why|where|when|who)\b[^?]*\?\s*$)/i.exec(raw.slice(cur, end));
    if (opener) {
      const sp = spanOf(from, raw, cur, cur + opener[1].length);
      if (sp) conditions.push(sp);
      cur += opener[0].length;
    }
    // "Baroque (c.1600 – 1700s) What influence did …?" — a printed heading
    // before the question is the area the answer must stay in. "However
    // what did they not do?" — a connective is neither.
    const beforeQuestion = /^(.{2,120}?)\s+(?=(?:What|How|Why|Which|Where|When|Who|To what|In what|Under which)\b[^?]*\?\s*$)/u.exec(raw.slice(cur, end));
    if (beforeQuestion && !/[.?!:]\s*$/.test(beforeQuestion[1]) && !commandMatches(beforeQuestion[1]).length
      && (/\)$/.test(beforeQuestion[1]) || /^(?:however|so|then|also|and|but|now|finally)$/i.test(beforeQuestion[1]))) {
      if (!/^(?:however|so|then|also|and|but|now|finally)$/i.test(beforeQuestion[1])) {
        const sp = spanOf(from, raw, cur, cur + beforeQuestion[1].length);
        if (sp) conditions.push(sp);
      }
      cur += beforeQuestion[0].length;
    }
    let verb = EXTRA_VERBS.exec(raw.slice(cur, end));
    if (!verb) {
      const commaVerb = /^([^.?!;]{3,120}?),\s+(?=\p{Ll})/u.exec(raw.slice(cur, end));
      if (commaVerb && EXTRA_VERBS.test(raw.slice(cur + commaVerb[0].length, end))) {
        const sp = spanOf(from, raw, cur, cur + commaVerb[1].length);
        if (sp) conditions.push(sp);
        cur += commaVerb[0].length;
        verb = EXTRA_VERBS.exec(raw.slice(cur, end));
      }
    }
    if (!verb) {
      const mid = /\s(?=(?:Solve|Work out|Prove|Verify|Show that|Find|Evaluate|Simplify|Factorise|Expand|Express|Write|Calculate|Hence|Draw|Sketch|Construct|Determine|State|Name|Give|Explain|Describe|Identify|Complete|Fill in)(?![\p{L}]))/u.exec(raw.slice(cur, end));
      if (mid && mid.index > 0 && !/[.?!]\s*$/.test(raw.slice(cur, cur + mid.index + 1))) {
        // What comes before a mid-sentence command is the set-up: for a
        // calculation it is where the values are, so it is kept as a given.
        const setup = spanOf(from, raw, cur, cur + mid.index);
        if (setup && /=/.test(setup.display)) openerUse.push({ ...setup, kind: 'given' });
        else if (setup && /\)$/.test(setup.display)) conditions.push(setup);
        else if (setup) openerUse.push({ ...setup, kind: /\d/.test(setup.display) ? 'given' : 'material' });
        cur += mid.index + 1;
        verb = EXTRA_VERBS.exec(raw.slice(cur, end));
      }
    }
    if (verb) {
      const vStart = cur + verb[0].length - verb[1].length;
      // "hence, find …" — "hence" ties the job to the last one and stays with it.
      const hence = /^hence(?:,| or otherwise,)?\s*$/i.test(raw.slice(cur, vStart));
      if (vStart > cur && !hence) { const hs = spanOf(from, raw, cur, vStart); if (hs) conditions.push(hs); }
      const aEnd = actionTail(raw, vStart + verb[1].length, end, verb[1].split(/\s+/)[0]);
      action = spanOf(from, raw, hence ? cur : vStart, aEnd);
      actionKey = keyFor(raw.slice(vStart, aEnd), raw.slice(aEnd, end));
      means = MEANS[actionKey] ?? MEANS.state;
      cur = aEnd;
    }
    const head = raw.slice(cur, end).toLowerCase();
    const prepWh = /^(?:to|under|in|into|from|on|at|by|for|with|of|during|between|about|against|through|towards|within|across|after|before|since|until)\s+(?:what|which|whom|whose|where|when|how (?:many|much|long|far|often))(?![\p{L}])/iu.exec(raw.slice(cur, end));
    const wh = prepWh ? prepWh[0].toLowerCase() : WH_FORMS.find(f => head.startsWith(f) && !/[\p{L}]/u.test(head[f.length] ?? ' '));
    // Without a question mark, only a question-shaped sentence is a question:
    // "When a computer is carrying out lots of tasks, it …" is a statement.
    const asked = /[?？]\s*$/.test(raw.slice(cur, end))
      || (wh && !/^(?:when|where|how|why)$/.test(wh))
      || (wh && /^\s*(?:is|are|was|were|do|does|did|has|have|had|can|could|would|should|will|might|may|must)\b/i.test(raw.slice(cur + wh.length, end)));
    if (!action && wh && asked) {
      const aEnd = whNounEnd(raw, cur, cur + wh!.length, end);
      action = spanOf(from, raw, cur, aEnd);
      actionKey = keyFor(raw.slice(cur, aEnd), raw.slice(aEnd, end));
      means = MEANS[actionKey] ?? MEANS['wh-plain'];
      cur = aEnd;
    }
    // "Hammer throwers mainly move in which plane of movement?": a quiz
    // question whose question word sits mid-sentence. The question is the job.
    if (!action && /\?\s*$/.test(raw.slice(cur, end)) && /\s(?:which|what|whom|whose|how many|how much)\s/i.test(raw.slice(cur, end))
      && !YES_NO.test(raw.slice(cur, end))) {
      const qEnd = cur + raw.slice(cur, end).lastIndexOf('?');
      action = spanOf(from, raw, cur, qEnd);
      actionKey = 'wh-plain';
      means = MEANS['wh-plain'];
      cur = qEnd;
    }
    // A yes/no or either/or question: the question itself is the job.
    // "Do both documents give similar descriptions of …?" / "At the end of
    // the play did you feel any sympathy for Jason?"
    const yn = !action && /\?\s*$/.test(raw.slice(cur, end)) ? YES_NO.exec(raw.slice(cur, end)) : null;
    // A prefix that holds a question word is not a yes/no question's opener.
    if (yn && yn[1] && /\b(?:what|which|whom|whose|how|why|where|when|who)\b/i.test(yn[1])) yn.splice(0, yn.length);
    if (yn && yn.length) {
      if (yn[1]) {
        const sp = spanOf(from, raw, cur, cur + yn[1].length);
        if (sp) conditions.push(sp);
      }
      const aStart = cur + yn[0].length - yn[2].length - (yn[0].length - yn[0].trimEnd().length);
      const qEnd = cur + raw.slice(cur, end).lastIndexOf('?');
      action = spanOf(from, raw, aStart, qEnd);
      actionKey = /\s(?:or)\s/i.test(raw.slice(aStart, qEnd)) ? 'either-or' : 'yes-no';
      means = MEANS[actionKey];
      cur = qEnd;
    }
  }
  if (!action) return null;
  // Answer-box labels ("Name of Myth 1: Location on temple:") are not
  // instructions; "For this cross, state:" is.
  if (/^\s+of\s+[^.?!:]{1,30}:/.test(raw.slice(cur, end)) || /^\s*:\s*\p{Lu}[\p{L} ]{0,30}:/u.test(raw.slice(cur, end))) return null;
  // "Use or attempted use by an athlete …": a word the lexicon knows as a
  // command, used as a noun.
  if (/^\p{L}+$/u.test(action.display) && /^\s+or\s+(?:attempted|the|a|an|its|their|any)\b/i.test(raw.slice(cur, end))) return null;
  // A single command word followed by "of" is a noun: "Design of products".
  if (/^\p{L}+$/u.test(action.display) && !/^(?:account|details)/i.test(action.display) && !/^(?:wh-|explain-how|to-what-extent)/.test(actionKey)
    && !/^(?:which|what|who|whose|whom|how)$/i.test(action.display) && /^\s+of\s/i.test(raw.slice(cur, end))) return null;
  skipSpace();

  // "Discuss in detail, using notes and freehand sketches, three …": a
  // bracketed limit between the command and its object.
  const bracket = /^,\s*([^,.;:?]{2,100}?)\s*,\s*(?=\S)/.exec(raw.slice(cur, end));
  if (bracket && !/^(?:and|or|then)\b/i.test(bracket[1]) && !commandMatches(bracket[1]).some(m => m.index === 0)) {
    const s0 = cur + bracket[0].indexOf(bracket[1]);
    const sp = spanOf(from, raw, s0, s0 + bracket[1].length);
    if (sp) conditions.push(sp);
    cur += bracket[0].length;
  }
  // "Explain in ENGLISH the meaning of …": the language is a limit.
  const language = /^in (?:English|ENGLISH|Irish|IRISH)\b,?\s*/.exec(raw.slice(cur, end));
  if (language) {
    const sp = spanOf(from, raw, cur, cur + language[0].trimEnd().length);
    if (sp) conditions.push(sp);
    cur += language[0].length;
  }
  // "at what speed (in mm/year) is it moving": the bracketed unit is a limit.
  const unitParen = /^\((?:in|to|correct to|as)\s[^)]{1,30}\)\s*/i.exec(raw.slice(cur, end));
  if (unitParen) {
    const sp = spanOf(from, raw, cur, cur + unitParen[0].trimEnd().length);
    if (sp) conditions.push(sp);
    cur += unitParen[0].length;
  }
  if (!bracket) { const lone = /^,\s*/.exec(raw.slice(cur, end)); if (lone) cur += lone[0].length; }
  const manner = MANNER.exec(raw.slice(cur, end));
  if (manner && cur + manner[0].length < end - 3) {
    const sp = spanOf(from, raw, cur, cur + manner[0].length);
    if (sp) conditions.push(sp);
    cur += manner[0].length;
  }
  skipSpace();

  // COUNT directly after the action.
  let count: KPSpan | null = null;
  let countValue: number | undefined;
  let countNoun: string | undefined;
  let pairHeadings: KPSpan[] | undefined;
  const afterAction = raw.slice(cur, end);
  // "How does one remain safe?": after a question form, "one" is a pronoun.
  const pronounOne = /^(?:wh-|explain-how|to-what-extent|yes-no)/.test(actionKey) && /^one\s/i.test(afterAction);
  const pairCount = /^one\s+([\p{L}-]+)\s+and\s+one\s+([\p{L}-]+)/iu.exec(afterAction)
    ?? /^one\s+([\p{L}-]+(?:\s+(?:of|for|to|in|on|from|about)\s+[^,;.?]{1,60}?))\s+and\s+one\s+([\p{L}-]+(?:\s+(?:of|for|to|in|on|from|about)\s+[^,;.?]{1,60}?)?)(?=\s*(?:[,;.?]|$|\s+(?:that|which|who|when|where|if|in (?:the|your)|using|with)\b))/iu.exec(afterAction);
  const c0 = pronounOne || pairCount ? null : COUNT_AFTER_CMD.exec(afterAction);
  // "Clearly show all points of contact": "all" is not a number to plan for.
  const c = c0 && /^all$/i.test(c0[1].trim()) && !/^\s+(?:two|three|four|five|six|seven|eight|[2-8])\b/i.test(afterAction.slice(c0[0].length)) ? null : c0;
  if (c) {
    const phraseEnd = cur + c[0].length;
    const nounMatch = /^\s+([\p{L}-]+(?:\s+of evidence)?)/u.exec(raw.slice(phraseEnd, end));
    const noun = nounMatch?.[1] ?? '';
    const word = c[1].toLowerCase().replace(/^(?:any|at least)\s+/, '');
    const unitAhead = new RegExp(`^\\s*(?:${MEANINGFUL_DATA_UNIT.source})(?![\\p{L}])`, 'iu').test(raw.slice(phraseEnd, end));
    const ofFollowing = /^\s+of\s+(?=the following\b)/i.exec(raw.slice(phraseEnd, end));
    // "Name any two of the plastic manufacturing processes shown at A, B and
    // C": the number is counted out of the pool the phrase after "of" names.
    const ofPool = !ofFollowing && !/^(?:each|all|both)$/.test(c[1].toLowerCase().replace(/^(?:any|at least)\s+/, ''))
      ? /^\s+of\s+(?=(?:the|these|those|your|his|her|their|its)\s+((?:[\p{L}-]+\s+){0,3}?[\p{L}-]+s)(?![\p{L}]))/iu.exec(raw.slice(phraseEnd, end))
      : null;
    if (ofPool && !unitAhead && !/^(?:of|that|which|who)$/i.test(ofPool[1])) {
      count = spanOf(from, raw, cur, phraseEnd);
      cur = phraseEnd + ofPool[0].length;
      const value = NUMBER_WORDS[word] ?? (/^[2-8]$/.test(word) ? Number(word) : undefined);
      if (value) countValue = value;
      countNoun = singular(ofPool[1].trim().split(/\s+/).pop()!.toLowerCase());
    } else if (ofFollowing && !unitAhead) {
      count = spanOf(from, raw, cur, phraseEnd);
      cur = phraseEnd + ofFollowing[0].length;
      const value = NUMBER_WORDS[word] ?? (/^[2-8]$/.test(word) ? Number(word) : undefined);
      if (value) countValue = value;
      // "any two of the following terms" → Term 1; bare "the following" → Choice 1.
      const listNoun = /^the following\s+([\p{L}-]+s)\b/iu.exec(raw.slice(cur, end));
      countNoun = listNoun ? singular(listNoun[1]) : 'choice';
    } else if (!unitAhead && !/^(?:of)\b/i.test(noun) || /^each of the following|^each|^all|^both/.test(word)) {
      if (noun && GENERIC_UNIT_NOUNS.test(noun) && word !== 'all') {
        const cEnd = phraseEnd + nounMatch![0].length;
        count = spanOf(from, raw, cur, cEnd);
        countNoun = singular(noun);
        cur = cEnd;
        // "one way in which …": "in which" opens what it is about.
        const connector = /^\s+(?:of|for|in(?!\s+(?:which|whom|whose)\b)|on(?!\s+which\b)|as|about)(?![\p{L}])/iu.exec(raw.slice(cur, end));
        if (connector) cur += connector[0].length;
      } else if (/^(?:each|all|both)$/.test(word) && /^\s+of\s+(?!the following\b)(?:the|these|those|your)\s/i.test(raw.slice(phraseEnd, end))) {
        // "each of the letters A, B, C and D with the term …" — the counted
        // set is the whole "each of …" phrase; the focus follows its preposition.
        const tail = raw.slice(phraseEnd, end);
        // A comma before a single letter or number is inside a list ("A, B, C and D").
        const stop = /\s+(?:with|to|into|in|on|from|for|by|that|which)\s+|,(?=\s)(?!\s*[A-Z0-9](?![\p{L}]))|[;:?.](?=\s|$)/iu.exec(tail.replace(/^\s+of\s+/, m => ' '.repeat(m.length)));
        const cEnd = stop ? phraseEnd + stop.index : end;
        count = spanOf(from, raw, cur, cEnd);
        const inner = /\b(two|three|four|five|six|seven|eight)\s+([\p{L}-]+s)\b/iu.exec(raw.slice(phraseEnd, cEnd));
        if (inner) { countValue = NUMBER_WORDS[inner[1].toLowerCase()]; countNoun = singular(inner[2]); }
        cur = cEnd;
        const prep = /^\s+(?:with|to|into|in|on|from|for|by)\s+/i.exec(raw.slice(cur, end));
        if (prep) cur += prep[0].length;
      } else {
        // "three key areas, other than …": How many is the number with its
        // noun phrase, and About starts at the noun phrase too, so neither
        // slot tears an adjective from its noun.
        const np = /^(?:each|all|both)$/.test(word) ? null : /^((?:\s+[\p{L}-]+){1,4}?)(?=\s+(?:of|in|on|for|to|from|with|by|at|that|which|who|whose|where|when|between|during|used|found|made|given|shown|than|as|about|into|within|across|you|your|and|or|a|an|the|this|that|these|those|each|every|some|may|might|can|could|will|would|should|must|is|are|was|were|has|have|had|do|does|did)\b|\s*[,.;:?!(]|\s*$)/iu.exec(raw.slice(cur + c[1].length, end));
        if (np && !unitAhead) {
          let npWords = np[1].trim().split(/\s+/);
          const isPlural = (w: string) => /[^s]s$|ies$|sses$/i.test(w);
          // "two things farmers would check": the second plural starts a
          // clause about the first, so it is not the counted noun.
          const clauseAfter = /^\s+(?:would|could|can|should|might|may|must|will|do|did|use|need|have|has|had|are|were)\b/i.test(raw.slice(cur + c[1].length + np[1].length, end));
          if (clauseAfter && npWords.length >= 2 && isPlural(npWords[npWords.length - 1]) && npWords.slice(0, -1).some(isPlural)) npWords = npWords.slice(0, -1);
          const npText = ' ' + npWords.join(' ');
          const plural = [...npWords].reverse().find(isPlural);
          const head = plural ?? [...npWords].reverse().find(w => !/(?:ed|ing)$/i.test(w)) ?? npWords[npWords.length - 1];
          const headEnd = cur + c[1].length + np[1].indexOf(head, npText.length - npWords.slice(npWords.indexOf(head)).join(' ').length - 1) + head.length;
          count = spanOf(from, raw, cur, Math.max(cur + c[1].length + 1, headEnd));
          countNoun = singular(head);
          // "What two things did the herald ask …?": the question goes on
          // after its counted noun.
          cur = /^wh-/.test(actionKey) ? headEnd : cur + c[1].length;
        } else {
          count = spanOf(from, raw, cur, phraseEnd);
          cur = phraseEnd;
        }
      }
      const value = NUMBER_WORDS[word] ?? (/^[2-8]$/.test(word) ? Number(word) : undefined);
      if (value) countValue = value;
    }
  } else if (pairCount) {
    // "one advantage and one disadvantage": two answers, one of each.
    const pair = pairCount;
    count = spanOf(from, raw, cur, cur + pair[0].length);
    const aAt = cur + pair[0].indexOf(pair[1]);
    const bAt = cur + pair[0].lastIndexOf(pair[2]);
    const a = spanOf(from, raw, aAt, aAt + pair[1].length);
    const b = spanOf(from, raw, bAt, bAt + pair[2].length);
    if (a && b) pairHeadings = [a, b];
    cur += pair[0].length;
    const connector = /^\s+(?:of|for|in|on|about)(?![\p{L}])/iu.exec(raw.slice(cur, end));
    if (connector) cur += connector[0].length;
  } else {
    const an = pronounOne ? null : /^(?:an?|one)\s+(example|reason|way|point|detail|use|fact|feature|advantage|disadvantage|benefit|effect|cause|method|function)(?![\p{L}])(?!\s+(?:article|film|story|writer|length|page|programme|documentary|piece|film|film-maker|report|magazine|book|poem)\b)/iu.exec(afterAction);
    if (an) {
      count = spanOf(from, raw, cur, cur + an[0].length);
      countNoun = an[1];
      cur += an[0].length;
      const connector = /^\s+(?:of|for|in(?!\s+(?:which|whom|whose)\b)|on(?!\s+which\b)|as|from|about)(?![\p{L}])/iu.exec(raw.slice(cur, end));
      if (connector) cur += connector[0].length;
      countValue = 1;
    }
  }
  skipSpace();

  if (!count && leadCount) {
    count = leadCount;
    const v = /\b(one|two|three|four|five|six)\b/i.exec(leadCount.display);
    if (v) countValue = NUMBER_WORDS[v[1].toLowerCase()];
  }
  // A printed "(three points)" closes the clause it counts.
  if (!count) {
    const paren = /\(\s*(one|two|three|four|five|six)\s+(points?|reasons?|examples?|details?)\b[^)]*\)/i.exec(raw.slice(clause.start, end));
    if (paren) {
      const s0 = clause.start + paren.index + 1;
      count = spanOf(from, raw, s0, s0 + paren[1].length + 1 + paren[2].length);
      countValue = NUMBER_WORDS[paren[1].toLowerCase()];
      countNoun = singular(paren[2]);
    }
  }

  // FOCUS runs to the first condition trigger, relative clause after it, a
  // following command, or the clause's end.
  let focusEnd = end;
  const rest = raw.slice(cur, end);
  const firstTrigger = triggersIn(raw, cur, end, actionKey).find(t => (t.index ?? 0) > 0 && depthAt(rest, t.index ?? 0) === 0);
  if (firstTrigger) {
    let at = cur + (firstTrigger.index ?? 0);
    const participle = PARTICIPLE_BEFORE.exec(raw.slice(cur, at));
    if (participle && /outside|other than|apart from|excluding|except|not in/i.test(firstTrigger[0])) at -= participle[0].length;
    // "in any named plant you have studied": the studied thing is the limit.
    if (/^(?:that |which )?you (?:have )?studied|^you studied/i.test(firstTrigger[0])) {
      const back = /(?:,\s*)?\b(?:in|from|for|on)\s+(?:an?|any|one|the|two|three)\s+(?:[\p{L}-]+\s+){0,3}$/iu.exec(raw.slice(cur, at));
      if (back && back.index > 0) at = cur + back.index;
    }
    focusEnd = Math.min(focusEnd, at);
  }
  const pointer = /\s+(?:illustrated|shown|given|labelled|marked|represented|described|pictured|listed|printed|named|outlined)\s+(?:in|on|by|at|below|above)\b/i.exec(rest);
  MATERIAL_RE.lastIndex = 0;
  if (pointer && pointer.index > 3 && MATERIAL_RE.test(rest.slice(pointer.index))) focusEnd = Math.min(focusEnd, cur + pointer.index);
  MATERIAL_RE.lastIndex = 0;
  const hardStop = [...rest.matchAll(/[?:;]|\.(?=\s|$)|\s[•◆▪●]\s/g)]
    .find(m => m[0] !== '.' || !/(?:\b(?:e\.g|i\.e|etc|approx|Fig|No|c)|\b[A-Z])$/.test(rest.slice(0, m.index)));
  if (hardStop) focusEnd = Math.min(focusEnd, cur + (hardStop.index ?? 0));
  // A restrictive relative clause after the focus head is a condition.
  // Only a clause that narrows what counts ("that does not …", "which is
  // deemed …"); "the advice you would give", "the world in which you live"
  // and "one conclusion you can make" are what the answer is about.
  const rel = /,?\s+(?:that|which|who)\s+(?=(?:does|do|did|is|are|was|were|can|cannot|could|may|might|would|will|should|has|have)\s+not\b|are deemed\b|is deemed\b)/i.exec(raw.slice(cur, focusEnd));
  let relStart = -1;
  if (rel && rel.index > 2 && !/the following$/i.test(raw.slice(cur, cur + rel.index)) && !/\b(?:in|by|of|for|to|from|on|at|with|through|under)$/i.test(raw.slice(cur, cur + rel.index))) {
    relStart = cur + rel.index;
    focusEnd = relStart;
  }
  // "two reasons (other than corporation tax) why …": a bracketed exclusion
  // before the topic is a limit.
  const bracketLimit = /^\s*\((other than|apart from|except|excluding|not)\b[^()]{1,80}\)\s*/i.exec(raw.slice(cur, focusEnd));
  if (bracketLimit) {
    const sp = spanOf(from, raw, cur + bracketLimit[0].indexOf('(') + 1, cur + bracketLimit[0].lastIndexOf(')'));
    if (sp) conditions.push(sp);
    cur += bracketLimit[0].length;
  }
  let focus = spanOf(from, raw, cur, focusEnd);
  const dangling = focus && (/,?\s+(?:in which (?:you|they)|where you|in which)$/i.exec(focus.text) ?? /\s+(?:and|or|but|that|which|who)$/i.exec(focus.text));
  if (focus && dangling) focus = spanOf(from, raw, focus.start, focus.end - dangling[0].length) ?? focus;
  // "Give two examples from the text": where to look, not what about.
  if (focus && /^from the (?:text|passage|extract|article|poem|story|document|source|letter|interview|report)s?$/i.test(focus.display)) {
    conditions.push(focus);
    focus = null;
  }
  // "…, and the line l, where:" — the "where" introduces the givens.
  if (focus && /,?\s+where$/i.test(focus.text)) focus = spanOf(from, raw, focus.start, focus.end - (/,?\s+where$/i.exec(focus.text)![0].length)) ?? focus;
  // Where/When/Why … "located" style questions: a trailing participle is
  // part of the question form, not the thing asked about.
  // (A trailing participle stays: "Where were the families rehoused?" asks
  // about the rehousing, not the families.)

  // CONDITIONS from the relative clause and every trigger in the remainder.
  if (relStart >= 0) {
    const relEnd = conditionEnd(raw, relStart + 1, end);
    const sp = spanOf(from, raw, relStart, relEnd);
    if (sp) conditions.push(sp);
  }
  for (const t of triggersIn(raw, focusEnd, end, actionKey)) {
    let at = focusEnd + (t.index ?? 0);
    const tEnd = at + t[0].length;
    if (conditions.some(x => at >= x.start && at < x.end)) continue;
    // "… that you think are the most important": the relative word is the limit's.
    const rel = /^you\b/i.test(t[0]) ? /\b(?:that|which|who)\s+$/i.exec(raw.slice(Math.max(clause.start, at - 8), at)) : null;
    if (rel) at -= rel[0].length;
    const participle = PARTICIPLE_BEFORE.exec(raw.slice(Math.max(focusEnd, at - 20), at));
    if (participle && /outside|other than|apart from|excluding|except|not in/i.test(t[0])) at -= participle[0].length;
    if (/^(?:that |which )?you (?:have )?studied|^you studied/i.test(t[0]) && at === focusEnd + (t.index ?? 0)) {
      const back = /(?:,\s*)?\b(?:in|from|for|on)\s+(?:an?|any|one|the|two|three)\s+(?:[\p{L}-]+\s+){0,3}$/iu.exec(raw.slice(focusEnd, at));
      if (back) at = focusEnd + back.index;
    }
    const sp = spanOf(from, raw, at, conditionEnd(raw, tEnd, end, t[0]));
    if (sp && !emptyLimit(sp, t[0]) && !conditions.some(x => x.display === sp.display)) conditions.push(sp);
  }
  // "if R1 = 10 kΩ, R2 = 60 kΩ and C = 10 µF": in a calculation, a clause
  // that states values is what you are given, not a limit.
  const valueClause = (t: string) => /[\p{L}\p{N}₀-₉)\]]\s*=\s*[-−]?[\d(]/u.test(t);
  if (CALC_KEYS.has(actionKey) || /^(?:prove|derive)$/.test(actionKey)) {
    for (let i = conditions.length - 1; i >= 0; i -= 1) {
      if (!valueClause(conditions[i].text)) continue;
      const [c0] = conditions.splice(i, 1);
      openerUse.push({ ...c0, kind: 'given' });
    }
  }
  // Keep a limit whole when the paper runs it on: "a European region (not in
  // Ireland) that you have studied".
  conditions.sort((a, b) => (a.from === b.from ? a.start - b.start : a.from === 'stem' ? -1 : 1));
  for (let i = conditions.length - 1; i > 0; i -= 1) {
    const a = conditions[i - 1];
    const b = conditions[i];
    if (a.from === b.from && b.start >= a.end && /^[\s,]*$/.test(raw.slice(a.end, b.start)) && /^(?:that|which|who|you)\b/i.test(b.display)) {
      const merged = spanOf(from, raw, a.start, b.end);
      if (merged) conditions.splice(i - 1, 2, merged);
    }
  }

  // COUNT elsewhere in the clause.
  const clauseText = raw.slice(clause.start, end);
  if (!count) {
    // "any two of the following stages": a choice from a printed list.
    const ofList = /(?<![\p{L}])((?:any\s+)?(one|two|three|four|five|six))\s+of\s+the\s+following(?=(?:\s+([\p{L}-]+))?)/iu.exec(clauseText);
    const numbered = /\b(?:items?|parts?|statements?|questions?|sentences?|lines?|boxes|terms?|events?|stages?)\s+(?:numbered\s+|labelled\s+)?\(?(\d)\)?\s*(?:to|–|-)\s*\(?(\d)\)?(?![\d])/.exec(clauseText);
    const eachOfN = /\beach of the (two|three|four|five|six|seven|eight) ([\p{L}-]+s)\b/iu.exec(clauseText);
    if (eachOfN) {
      count = spanOf(from, raw, clause.start + eachOfN.index, clause.start + eachOfN.index + eachOfN[0].length);
      countValue = NUMBER_WORDS[eachOfN[1].toLowerCase()];
      countNoun = singular(eachOfN[2]);
    } else if (ofList) {
      count = spanOf(from, raw, clause.start + ofList.index, clause.start + ofList.index + ofList[0].length);
      countValue = NUMBER_WORDS[ofList[2].toLowerCase()];
      countNoun = ofList[3] && /s$/.test(ofList[3]) ? singular(ofList[3]) : 'choice';
    } else if (numbered && Number(numbered[2]) > Number(numbered[1]) && Number(numbered[2]) - Number(numbered[1]) < 8) {
      count = spanOf(from, raw, clause.start + numbered.index, clause.start + numbered.index + numbered[0].length);
      countValue = Number(numbered[2]) - Number(numbered[1]) + 1;
      countNoun = singular(/^\S+/.exec(numbered[0])![0]);
    }
  }
  if (!count) {
    const nouns = COUNTED_ANSWER_NOUNS;
    // "the probability that at most 2 teams drop …" describes the event; it is
    // not how many answers to give.
    // "Name the two parts" is the object of the command, so it counts; a
    // number in a description ("where two neurons come into contact") does not.
    const objectStart = focus && focus.from === from ? focus.start : cur;
    const pool = (at: number) => {
      const before = raw.slice(Math.max(clause.start, at - 13), at);
      if (/\bthe\s+$/i.test(before) && /^\s*the\s+$/i.test(raw.slice(objectStart, at))) return false;
      if (/\b(?:where|that|which|who|whom|whose|when|while|if|because|between|connect|connects)\b[^,.;:]*$/i.test(raw.slice(Math.max(objectStart, at - 40), at))) return true;
      return /\b(?:the|these|those|all|of|between|at most|at least|exactly|more than|fewer than|less than|up to)\s+$/i.test(before);
    };
    const c2 = new RegExp(`(?<![\\p{L}\\p{N}])(one|two|three|four|five|six|[2-6])\\s+(?:(?:different|distinct|separate|possible|other|main|major|key)\\s+)?(?:${nouns})(?![\\p{L}])`, 'iu')
      .exec(clauseText);
    // Any plural noun counted in the clause: "Give an account of any two myths".
    const c3 = /(?<![\p{L}\p{N}])(?:any\s+|at least\s+)?(two|three|four|five|six|[2-6])\s+(?:(?:most|least)\s+[\p{L}-]+\s+)?(?:(?:different|distinct|separate|possible|other|main|major|key|named|specific|important|contrasting|european|irish|non-european|developing|developed|urban|rural|physical|human)\s+){0,2}([\p{L}-]{3,}s)(?![\p{L}])/iu.exec(clauseText);
    const hit = c2 && !pool(clause.start + c2.index) ? c2
      : c3 && !pool(clause.start + c3.index) && !/^(?:years|hours|minutes|seconds|marks|words|times|days|weeks|months|metres|pages|lines|sides|decimal|places)$/i.test(c3[2])
        && !new RegExp(`^(?:${MEANINGFUL_DATA_UNIT.source})$`, 'iu').test(c3[2]) ? c3 : null;
    const inLimit = hit && conditions.some(x => x.from === from && clause.start + hit.index >= x.start && clause.start + hit.index < x.end);
    if (hit && !inLimit) {
      count = spanOf(from, raw, clause.start + hit.index, clause.start + hit.index + hit[0].length);
      countValue = NUMBER_WORDS[hit[1].toLowerCase()] ?? Number(hit[1]);
      if (hit === c3) countNoun = singular(c3[2]);
    }
  }

  // USE: supplied material named in the clause.
  const use: KPUse[] = openerUse;
  const addUse = (s: number, e: number, kind: KPUseKind) => {
    const sp = spanOf(from, raw, s, e);
    if (!sp || use.some(u => (s < u.end && e > u.start))) return;
    use.push({ ...sp, kind });
  };
  for (const m of clauseText.matchAll(NAMED_RE)) addUse(clause.start + (m.index ?? 0), clause.start + (m.index ?? 0) + m[0].length, 'material');
  for (const m of clauseText.matchAll(MATERIAL_RE)) {
    if (notMaterial(clauseText, m.index ?? 0, m[0])) continue;
    addUse(clause.start + (m.index ?? 0), clause.start + (m.index ?? 0) + m[0].length, 'material');
  }
  for (const m of clauseText.matchAll(MATERIAL_ADJ)) addUse(clause.start + (m.index ?? 0), clause.start + (m.index ?? 0) + m[0].length, 'material');
  for (const m of clauseText.matchAll(LOCATOR_RE)) addUse(clause.start + (m.index ?? 0), clause.start + (m.index ?? 0) + m[0].length, 'locator');
  for (const m of clauseText.matchAll(OPTIONS_RE)) addUse(clause.start + (m.index ?? 0), clause.start + (m.index ?? 0) + m[0].length, 'options');

  // Printed words the focus is interrupted by a limit and then resumes:
  // "two conditions, other than X, that are necessary for …". They are the
  // rest of the focus, not a limit, and never dropped.
  const focusMore: KPSpan[] = [];
  if (focus) {
    const colon = raw.slice(focus.end, end).search(/:(?=\s|$)/);
    const sentenceEnd = raw.slice(focus.end, end).search(/[.?!](?=\s|$)/);
    const stopAt = Math.min(colon >= 0 ? focus.end + colon : end, sentenceEnd >= 0 ? focus.end + sentenceEnd : end);
    const covered = [...conditions, ...use, ...(count ? [count] : [])]
      .filter(x => x.from === from && x.end > focus!.end && x.start < stopAt)
      .map(x => [x.start, x.end] as [number, number])
      .sort((a, b) => a[0] - b[0]);
    let p = focus.end;
    for (const [s, e] of [...covered, [stopAt, stopAt] as [number, number]]) {
      if (s > p) {
        let gap = spanOf(from, raw, p, Math.min(s, stopAt));
        const dangling = gap && /\s+(?:in|on|of|to|from|at|by|with|for|and|or)$/i.exec(gap.text);
        if (gap && dangling) gap = spanOf(from, raw, gap.start, gap.end - dangling[0].length);
        if (gap && gap.display.split(/\s+/).length >= 2 && /\p{L}{2,}/u.test(gap.display)
          && !/^(?:and|or|then|in your answer|your answer|in|of|on|to|the|a|an)$/i.test(gap.display)
          && !TAIL_UNIT.test(gap.display) && !commandMatches(gap.display).some(m => m.index === 0)
          && !/^(?:in relation|with reference|in terms|referring|in the context|regarding|concerning)(?: to| of)?$/i.test(gap.display)) {
          if (valueClause(gap.text) && (CALC_KEYS.has(actionKey) || /^(?:prove|derive)$/.test(actionKey))) use.push({ ...gap, kind: 'given' });
          else focusMore.push(gap);
        }
      }
      p = Math.max(p, e);
      if (p >= stopAt) break;
    }
    // "… by the differential equation: v dv/ds = −29.4 −v²" — what is to be
    // shown is printed after the colon.
    if (colon >= 0 && /^(?:prove|derive|calculate|solve|balance)$/.test(actionKey)) {
      const eq = spanOf(from, raw, focus.end + colon + 1, end);
      if (eq && /[=→]/.test(eq.display) && eq.display.length < 120) {
        if (/^(?:prove|derive|balance)$/.test(actionKey)) focusMore.push(eq);
        else if (!use.some(x => x.start === eq.start)) use.push({ ...eq, kind: 'given' });
      }
    }
  }

  // A comparison's two sides.
  let sides: [KPSpan, KPSpan] | undefined;

  const both = focus && /^(?:compare|contrast|compare-contrast|distinguish)$/.test(actionKey) ? /\bboth\s+(.+?)\s+and\s+(.+)$/i.exec(focus.text) : null;
  if (focus && both) {
    const aStart = focus.start + both.index + both[0].indexOf(both[1]);
    const bStart = focus.start + both.index + both[0].lastIndexOf(both[2]);
    const a = spanOf(from, raw, aStart, aStart + both[1].length);
    const b = spanOf(from, raw, bStart, bStart + both[2].length);
    if (a && b) sides = [a, b];
  } else if (focus && /^(?:compare|contrast|compare-contrast|distinguish)$/.test(actionKey)) {
    const verbSplit = /\s+(?:differs?|is different|are different|compares?|contrasts?)\s+(?:from|with|to)\s+/i.exec(focus.text);
    // "the extent to which" joins no sides; the replacement keeps offsets.
    const ftext = focus.text.replace(/\bthe extent to which\b/gi, m => m.replace(/ /g, '_'));
    const split = verbSplit ?? /\s+(?:and|with|from|to)\s+(?!the same\b|which\b|whom\b|what\b|how\b|each\b|every\b|at least\b|both\b|one of\b)/i.exec(ftext);
    const last = verbSplit ? verbSplit.index : split ? ftext.lastIndexOf(split[0]) : -1;
    // Two sides are two short things ("artisan produce and a niche market"),
    // not the last "and" of a long clause ("social position and status").
    const words = (t: string) => t.trim().split(/\s+/).length;
    const sidesFit = last > 0 && (verbSplit || (words(ftext.slice(0, last)) <= 8 && words(ftext.slice(last + split![0].length)) <= 8 && !/_/.test(ftext)));
    if (last > 0 && sidesFit) {
      const a = spanOf(from, raw, focus.start, focus.start + last);
      const b = spanOf(from, raw, focus.start + last + split![0].length, focus.end);
      if (a && b) sides = [a, b];
    }
  }

  // The kind of job, where the clause makes it plain.
  if (/\btrue or false\b/i.test(clauseText) && /^(?:state|identify|tick|other|wh-plain|write)$/.test(actionKey)) {
    actionKey = 'true-false';
    means = MEANS['true-false'];
  } else if (/whether$/i.test(action.display) && !/^(?:explain|discuss|examine|consider|assess|evaluate|justify|comment)/i.test(action.display) && focus && /\s(?:or)\s/i.test(focus.display)) {
    actionKey = 'either-or';
    means = MEANS['either-or'];
  } else if (/^indicate/i.test(action.display) && /\btick|✓|\uF050|\bbox\b/i.test(clauseText)) {
    actionKey = 'tick';
    means = MEANS.tick;
  } else if (actionKey === 'explain' && /^(?:each of )?(?:the )?(?:following\s+)?(?:[\p{L}-]+\s+){0,3}terms?\b/iu.test(`${count?.display ?? ''} ${focus?.display ?? ''}`.trim())) {
    actionKey = 'define';
    means = MEANS.define;
  }
  if (/^(?:state|tick|prove|include|other|identify|label)$/.test(actionKey) && /^(?:(?:clearly|carefully|neatly|also)\s+)?(?:indicate|show|include|mark|identify|label)\b/i.test(action.display)
    && conditions.some(c => /^(?:on|in) (?:your|the) (?:drawing|diagram|sketch|graph)/i.test(c.display))) {
    actionKey = 'on-drawing';
    means = MEANS['on-drawing'];
  }
  if (!countNoun && countValue && countValue > 1) countNoun = headNoun(focus);
  if (!pairHeadings && !count && focus && !sides) {
    const pair = /^(?:an?|one)\s+((?:[\p{L}-]+\s+){0,2}[\p{L}-]+)\s+and\s+(?:an?|one)\s+((?:[\p{L}-]+\s+){0,2}[\p{L}-]+?)(?=\s+(?:between|of|in|for|that|which|to|on|with)\b|$)/iu.exec(focus.text);
    if (pair) {
      const aAt = focus.start + pair[0].indexOf(pair[1]);
      const bAt = focus.start + pair[0].lastIndexOf(pair[2]);
      const a = spanOf(from, raw, aAt, aAt + pair[1].length);
      const b = spanOf(from, raw, bAt, bAt + pair[2].length);
      if (a && b) pairHeadings = [a, b];
    }
  }
  if (quoted) {
    if (!focus) focus = quoted;
    else use.unshift({ ...quoted, kind: 'material' });
  }

  const flags: KPFlag[] = [];
  if (focus && /(?<!\bone\s)\banother\s+(?:example|reason|way|method|advantage|disadvantage|benefit|use|feature|type|factor|cause|effect|source|point|difference|similarity|named|suitable|possible|different|one)\b|\b(?:one|two|three)\s+other\b|\bany\s+other\s+(?:example|reason|way|method|named|type|advantage|disadvantage|use|feature)\b|\bother than\b/i.test(`${count?.display ?? ''} ${focus.display} ${conditions.map(c => c.display).join(' ')}`)) flags.push('excludes-example');
  if (/\b(?:in|from|at) part \(?[a-z]{1,4}\)?|\babove\b.*\b(?:part|answer)\b|\byour answer (?:to|in|at) (?:part|question|\()/i.test(clauseText)) flags.push('depends-on-earlier-part');

  return {
    id: ctx.id, ref: ctx.ref, altGroup: ctx.altGroup,
    action, actionKey, means,
    count, countValue, countNoun,
    focus, ...(focusMore.length ? { focusMore } : {}), ...(pairHeadings ? { headings: pairHeadings } : {}), sides, conditions, use,
    marks: null, flags,
  };
}

function materialIn(raw: string, ranges: Array<[number, number]>, from: 'q' | 'stem'): KPUse[] {
  const out: KPUse[] = [];
  for (const [s0, e0] of ranges) {
    const text = raw.slice(s0, e0);
    const add = (m: RegExpMatchArray, kind: KPUseKind) => {
      const sp = spanOf(from, raw, s0 + (m.index ?? 0), s0 + (m.index ?? 0) + m[0].length);
      if (sp && !out.some(u => u.display.toLowerCase() === sp.display.toLowerCase())) out.push({ ...sp, kind });
    };
    for (const m of text.matchAll(NAMED_RE)) add(m, 'material');
    for (const m of text.matchAll(MATERIAL_RE)) if (!notMaterial(text, m.index ?? 0, m[0])) add(m, 'material');
    for (const m of text.matchAll(MATERIAL_LONG)) add(m, 'material');
    for (const m of text.matchAll(MATERIAL_ADJ)) add(m, 'material');
    for (const m of text.matchAll(LOCATOR_RE)) add(m, 'locator');
  }
  return out;
}

// Stem text that is not this question's material: acknowledgements, the
// copyright notice, cover pages and rubric furniture the reader swept in.
const BOILERPLATE = /Acknowledgements|Copyright|Section 53|State Examinations Commission|Coimisiún na Scrúduithe|examination paper|This document|Space for extra work|Indicate clearly the number|Rough work|This question continues|previous page|www\.|https?:\/\/|Leaving Certificate|Junior Cycle|superintendent|Do not write|Page \d+ of \d+/i;
const PART_START = /^\s*(?:\((?:iii|ii|iv|vi{1,3}|ix|x|i|v|[a-h])\)|\d{1,2}\.\s)/;

/**
 * The stem sentences that can supply this question's material or givens.
 * Another part's instruction ("(iv) Calculate the distance …", "Discuss this
 * statement …" from a sibling task) is not material for this one.
 */
function stemContextPieces(stem: string, pieces: Piece[]): { material: Piece[]; givens: Piece[] } {
  const material: Piece[] = [];
  const givens: Piece[] = [];
  for (const p of pieces) {
    const text = stem.slice(p.start, p.end).trim();
    if (BOILERPLATE.test(text)) continue;
    const rubric = RUBRIC.test(text);
    const task = PART_START.test(text) || commandMatches(text).some(m => m.index <= 2) || EXTRA_VERBS.test(text);
    if (task && !rubric) continue;
    material.push(p);
    if (!rubric) givens.push(p);
  }
  return { material, givens };
}

const singular = (noun: string) => {
  const w = noun.toLowerCase().replace(/\s+of (?:evidence|information)$/, '');
  if (/ies$/.test(w)) return w.replace(/ies$/, 'y');
  if (/sses$/.test(w)) return w.replace(/es$/, '');
  // viruses, stimuli, nuclei, analyses, hypotheses, crises, bases (of a
  // triangle stay "base").
  const irregular: Record<string, string> = { viruses: 'virus', statuses: 'status', bonuses: 'bonus', campuses: 'campus', stimuli: 'stimulus', nuclei: 'nucleus', fungi: 'fungus', bacteria: 'bacterium', analyses: 'analysis', hypotheses: 'hypothesis', crises: 'crisis', theses: 'thesis', axes: 'axis', criteria: 'criterion', phenomena: 'phenomenon', data: 'data', media: 'medium', species: 'species', series: 'series', apparatus: 'apparatus', processes: 'process', leaves: 'leaf', lives: 'life', halves: 'half', shelves: 'shelf', wolves: 'wolf', knives: 'knife', people: 'person', children: 'child', women: 'woman', men: 'man', teeth: 'tooth', feet: 'foot', mice: 'mouse' };
  if (irregular[w]) return irregular[w];
  if (/(?:ss|us|is)$/.test(w)) return w;
  if (/(?:ch|sh|x)es$/.test(w)) return w.replace(/es$/, '');
  return w.replace(/s$/, '');
};

const firstSentence = (value: string) => {
  const s = value.split(/(?<=[.!?])\s/)[0] ?? value;
  return s.length > 90 ? `${s.slice(0, 87)}…` : s;
};

// ---------------------------------------------------------------------------
// Givens for calculation units (G1–G5).
// ---------------------------------------------------------------------------

// Units the shared data list lacks: "a half-life of 8 days", "5.4 g", "10 kΩ".
const GIVEN_TOKEN = /(?:€|£|\$)?\b\d+(?:[.,]\d+)?(?:\s*(?:days?|years?|weeks?|g|Hz|kHz|MHz|kΩ|MΩ|Ω|µF|μF|nF|pF|nm|µm|μm|kPa|kJ|kW|MW|mL|ml|L|dB|rpm|M|K|m|s))\b|(?:€|£|\$)\s?\d[\d,]*(?:\.\d+)?/g;
const hasGivenValue = (text: string) => [...text.matchAll(DATA_TOKEN)].some(t => MEANINGFUL_DATA_UNIT.test(t[0]))
  || new RegExp(GIVEN_TOKEN.source).test(text) || /[\p{L}₀-₉)\]]\s*=\s*[-−]?\d/u.test(text)
  || /\bis equal to\b|\bwas found to be\b|\b(?:value|rate|price|cost|mass|length|number|total|amount|base|concentration|temperature)\s+(?:is|was|of)\s+[-−€£$]?\d/i.test(text);

function givensFor(unit: KPUnit, raws: Array<{ from: 'q' | 'stem'; raw: string; pieces: Piece[] }>): KPUse[] {
  const out: KPUse[] = [];
  // The quantity asked for is the noun before the first preposition:
  // "the astronaut's weight on Earth" asks for weight, not Earth.
  const beforePrep = unit.focus?.display.toLowerCase().split(/\s+(?:of|on|in|at|for|to|from|with|by|during|when|if|that|which)\s+/)[0] ?? '';
  const head = beforePrep.match(/[\p{L}]+/gu)?.filter(w => w.length > 3 && !/^(?:that|this|with|from|total|value|amount|number|maximum|minimum|average|final|initial)$/.test(w)).pop();
  const ofWhat = head ? new RegExp(`\\b${head}(?:\\s+of\\s+(?:the\\s+)?[\\p{L}-]+)?`, 'iu').exec(unit.focus?.display.toLowerCase() ?? '') : null;
  const askedPhrase = ofWhat?.[0];
  for (const { from, raw, pieces } of raws) {
    for (const p of pieces) {
      const text = raw.slice(p.start, p.end);
      if (unit.action && p.start <= unit.action.start && p.end >= unit.action.end && from === unit.action.from) {
        // The task sentence itself: only a value stated inside it counts.
      }
      GIVEN_TOKEN.lastIndex = 0;
      const tokens = [...text.matchAll(DATA_TOKEN)].filter(t => MEANINGFUL_DATA_UNIT.test(t[0])).concat([...text.matchAll(GIVEN_TOKEN)]);
      GIVEN_TOKEN.lastIndex = 0;
      if (!tokens.length && !hasGivenValue(text)) continue;
      // G4: never attach a given about the very quantity being asked for.
      // "the heat of reaction" is asked; "the heat of formation of B is …" is given.
      if (askedPhrase && text.toLowerCase().includes(askedPhrase) && tokens.length <= 1) continue;
      const clauses = text.split(/(?<=[,;])\s+(?=\S)/);
      let offset = p.start;
      for (const cl of clauses) {
        const s = raw.indexOf(cl, offset);
        offset = s + cl.length;
        GIVEN_TOKEN.lastIndex = 0;
        const hasValue = hasGivenValue(cl);
        GIVEN_TOKEN.lastIndex = 0;
        if (!hasValue) continue;
        if (commandMatches(cl).some(m => m.index < 3)) {
          // A value inside the command sentence: take only "<value> <unit>" tokens.
          for (const t of cl.matchAll(DATA_TOKEN)) {
            if (!MEANINGFUL_DATA_UNIT.test(t[0])) continue;
            const ts = s + (t.index ?? 0);
            const sp = spanOf(from, raw, ts, ts + t[0].length);
            if (sp && !out.some(u => u.display === sp.display)) out.push({ ...sp, kind: 'given' });
          }
          continue;
        }
        // The whole printed sentence, not the clause after its first comma:
        // "A particle, of mass 2 kg, is projected …" keeps its subject.
        const whole = clauses.length > 1 && text.length <= 240 && !commandMatches(text).some(m => m.index < 3)
          ? spanOf(from, raw, p.start, p.end) : null;
        const sp = whole ?? spanOf(from, raw, s, s + cl.length);
        if (sp && !out.some(u => u.display === sp.display || (u.from === sp.from && u.start <= sp.start && u.end >= sp.end))) out.push({ ...sp, kind: 'given' });
        if (whole) break;
      }
    }
  }
  return out.slice(0, 6);
}

// ---------------------------------------------------------------------------
// Printed lists: "the following X: A; B", bullets, one per line.
// ---------------------------------------------------------------------------

const LOCATOR_ONLY = /^\(?(?:(?:para(?:graph)?|Par\.|section|lines?|Alt|Part|Abschnitt|Absatz|Zeile|párrafo|parágrafo|paragraphe|paragrafo|dalis|część|akapit|línea|ligne|riga)\s*[\d\s–-]+|\s*\d+\s+(?:dalis|bekezdés|odsek|kappale|rész)\s*)\)?$/i;

/** The items of a printed list, each lifted. An instruction ends the list. */
function listItems(raw: string, from: 'q' | 'stem', start: number, end: number, bySentence = false): KPSpan[] {
  const body = raw.slice(start, end);
  if (!body.trim()) return [];
  const strong = /[;\n•◆▪●\uF0A7\uF0B7\uF0D8\uF076\uF0FC\uF06E]|(?:^|\s)(?:\d{1,2}\.|\([a-h]\)|\(\d{1,2}\))\s+\S/.test(body);
  const sep = strong ? /\s*(?:[;\n•◆▪●\uF0A7\uF0B7\uF0D8\uF076\uF0FC\uF06E]+|(?:^|\s)(?:\d{1,2}\.|\([a-h]\)|\(\d{1,2}\))(?=\s))\s*/g
    : bySentence ? /(?<=[.?!])\s+/g
      : /\s*(?:,\s*(?:and\s+|or\s+)?|\s+and\s+)\s*/g;
  let ranges: Array<[number, number]> = [];
  let p = 0;
  for (const m of body.matchAll(sep)) {
    ranges.push([p, m.index ?? 0]);
    p = (m.index ?? 0) + m[0].length;
  }
  ranges.push([p, body.length]);
  if (!strong && !bySentence && /,/.test(body)) {
    // "Animal Welfare, Health and Safety, Traceability": with commas, only the
    // last item's "and" separates ("A, B and C").
    ranges = [];
    p = 0;
    for (const m of body.matchAll(/\s*,\s*(?:and\s+|or\s+)?/g)) {
      ranges.push([p, m.index ?? 0]);
      p = (m.index ?? 0) + m[0].length;
    }
    const last = body.slice(p);
    const and = /\s+and\s+/.exec(last);
    if (and && ranges.length) {
      ranges.push([p, p + and.index]);
      ranges.push([p + and.index + and[0].length, body.length]);
    } else ranges.push([p, body.length]);
  }
  const items: KPSpan[] = [];
  for (const [s, e] of ranges) {
    let sp = spanOf(from, raw, start + s, start + e);
    if (!sp) continue;
    // A table header printed before the first statement: "True False …".
    const header = /^(?:True\s+False|Yes\s+No)\s+/i.exec(sp.text);
    if (header) sp = spanOf(from, raw, sp.start + header[0].length, sp.end);
    // A trailing "OR" is the paper's either/or, not part of the item.
    const or = sp && /[.?!]?\s+OR$/.exec(sp.text);
    if (sp && or) sp = spanOf(from, raw, sp.start, sp.end - or[0].length);
    if (!sp || LOCATOR_ONLY.test(sp.display) || /^(?:True|False|True\s+False|Yes|No|Yes\s+No)$/i.test(sp.display)) continue;
    if (sp.display.split(/\s+/).length > 6 && commandMatches(sp.display).some(m => m.index === 0)) break;
    items.push(sp);
  }
  if (!strong && !bySentence && items.length === 1 && /[.?!]\s+\p{Lu}/u.test(body)) {
    const bits = listItems(raw, from, start, end, true);
    if (bits.length >= 2 && bits.every(b => b.display.split(/\s+/).length <= 5)) return bits;
  }
  if (!strong && !bySentence && items.some(it => it.display.split(/\s+/).length > 6)) return [];
  return items.filter(it => it.display.length >= 2 && it.display.length <= 400);
}

/** A span over a run of items, for a list shown whole as options. */
const spanOver = (raw: string, items: KPSpan[]) => {
  const marker = /(?:\d{1,2}\.|\([a-h]\)|[•◆▪●])\s*$/.exec(raw.slice(Math.max(0, items[0].start - 6), items[0].start));
  return spanOf(items[0].from, raw, items[0].start - (marker?.[0].length ?? 0), items[items.length - 1].end);
};

/**
 * A unit that introduces a printed list becomes one unit per item — "Explain
 * the following types of reward: Commission, …" is three explanations. When
 * the question asks for fewer than the list offers ("any two of the
 * following"), or asks to match, the list is the options instead.
 */
function spreadOver(unit: KPUnit, items: KPSpan[], raws: { q: string; stem: string }, nextId: () => string, choice = false): KPUnit[] {
  // Every span is cut from its own printed source.
  const raw = raws[items[0].from];
  const pick = choice || (unit.countValue && unit.countValue < items.length
    && unit.count && /\bof the following\b|^any\b|\bof these\b/i.test(unit.count.display));
  if (pick || unit.actionKey === 'match') {
    const whole = spanOver(raw, items);
    if (whole && !unit.use.some(u => u.start === whole.start && u.from === whole.from)) unit.use.push({ ...whole, kind: 'options' });
    return [unit];
  }
  if (/^(?:compare|contrast|compare-contrast|distinguish)$/.test(unit.actionKey) && items.length === 1) {
    const pair = /^(.+?)\s*\/\s*(.+)$/.exec(items[0].text);
    if (pair) {
      const a = spanOf(items[0].from, raw, items[0].start, items[0].start + pair[1].length);
      const bStart = items[0].start + items[0].text.lastIndexOf(pair[2]);
      const b = spanOf(items[0].from, raw, bStart, bStart + pair[2].length);
      if (a && b) return [{ ...unit, sides: [a, b] }];
    }
  }
  if (/^(?:true-false|tick)$/.test(unit.actionKey) && unit.focus) {
    // "Indicate with a tick (✓) whether each of the following statements is
    // true or false": the statement is the item; how to mark it is the limit.
    const how = /^(?:with a tick|by ticking)\s*(?:\([^)]*\))?/i.exec(unit.focus.text);
    const sp = how ? spanOf(unit.focus.from, raws[unit.focus.from], unit.focus.start, unit.focus.start + how[0].length) : null;
    unit = { ...unit, focus: null, conditions: sp ? [sp, ...unit.conditions] : unit.conditions };
  }
  // A card split per option prints fewer items than the choice count: the
  // item is what this card answers, and "any two" does not multiply it.
  if (isChoice(unit, raws) && (unit.countValue ?? 0) > items.length) {
    unit = { ...unit, count: null, countValue: undefined, countNoun: undefined };
  }
  if (items.length === 1) return [{ ...unit, item: items[0] }];
  const perList = unit.count && (/\beach\b|\bthe following\b|^all\b|^both\b/i.test(unit.count.display)
    // "the following two factors: • Transport • Labour": the count is the list's.
    || unit.countValue === items.length
    || /\b(?:the following|these|those)\s+$/i.test(raws[unit.count.from].slice(Math.max(0, unit.count.start - 16), unit.count.start)));
  return items.map(item => ({
    ...unit, id: nextId(), item,
    count: perList ? null : unit.count, countValue: perList ? undefined : unit.countValue, countNoun: perList ? undefined : unit.countNoun,
    conditions: [...unit.conditions], use: [...unit.use], flags: [...unit.flags],
  }));
}

/** "any two of the following", "one of the following religions": the student picks. */
const isChoice = (unit: KPUnit, raw: { q: string; stem: string }) => Boolean(unit.count && unit.countValue && (
  /\bof the following\b|^any\b|\bof these\b/i.test(unit.count.display)
  || /^\s*of\s+(?:the following|these|those)\b/i.test(raw[unit.count.from].slice(unit.count.end, unit.count.end + 30))
));

const HEADINGS_LEAD = /^(?:refer(?: in your answer)? to|in your answer,? refer to|using the following headings|under the (?:following )?headings|with reference to the following|include (?:discussion of|reference to))\s*:?\s*/i;

/** "Refer in your answer to space, function, layout and lighting" → the headings. */
function headingsFrom(unit: KPUnit, raw: { q: string; stem: string }): KPSpan[] | undefined {
  for (const c of unit.conditions) {
    const lead = HEADINGS_LEAD.exec(c.text);
    if (!lead) continue;
    const items = listItems(raw[c.from], c.from, c.start + lead[0].length, c.end);
    if (items.length >= 2 && items.length <= 6 && items.every(i => i.display.split(/\s+/).length <= 4)) return items;
  }
  return undefined;
}

const BLANK = /[…_]{3,}|\.{4,}|…{2,}/;
const asPrinted = (id: string, ref: string, altGroup: 'A' | 'B' | undefined, focus: KPSpan): KPUnit => ({
  id, ref, altGroup, action: null, actionKey: 'as-printed', means: BLANK.test(focus.text) ? 'Fill in the missing word or words.' : '', count: null, focus,
  conditions: [], use: [], marks: null, flags: ['as-printed'],
});

// Irish-medium questions read as English to a function-word count ("an",
// "is", "do" are Irish words too). These are not.
const IRISH_FUNCTION = new Set([
  'agus', 'na', 'sa', 'san', 'den', 'don', 'ar', 'le', 'leis', 'ag', 'go', 'nó', 'dhá', 'dá', 'seo', 'sin', 'faoi',
  'féin', 'bhfuil', 'atá', 'ón', 'chun', 'iad', 'mar', 'conas', 'cad', 'cén', 'tabhair', 'scríobh', 'aimsigh',
  'luaigh', 'mínigh', 'déan', 'cuir', 'focal', 'sliocht', 'alt', 'léiríonn', 'dar', 'leat', 'uatha',
]);
const irishShare = (text: string) => {
  const words = text.toLowerCase().match(/[\p{L}’']+/gu) ?? [];
  return words.length ? words.filter(w => IRISH_FUNCTION.has(w)).length / words.length : 0;
};

const ENGLISH_MEDIUM = new Set([
  'accounting', 'agricultural-science', 'applied-maths', 'art', 'biology', 'business', 'chemistry', 'classical-studies',
  'computer-science', 'construction-studies', 'dcg', 'design-and-communication-graphics', 'economics', 'engineering', 'english',
  'geography', 'history', 'home-economics', 'lcvp', 'link-modules', 'maths', 'mathematics', 'music', 'physical-education', 'physics',
  'physics-and-chemistry', 'politics-and-society', 'religious-education', 'technology',
]);

const STATEMENT_FOCUS = /^(?:this|the|these) (?:statement|view|claim|quotation|quote|opinion|assertion|idea|comment|remark)s?$/i;
const PICTURE = /photo|image|picture/i;
const PICTURE_REFERENCE = /photo|image|picture|poster|cartoon|advert|painting|sculpture|shown|above|below|illustrated|this work|the work|opposite/i;
const headOf = (display: string) => singular(display.toLowerCase().split(/\s+/).pop() ?? '');

// ---------------------------------------------------------------------------
// Entry point.
// ---------------------------------------------------------------------------

export function buildKeyParts(source: WaysInQuestionSource): KeyPartsBreakdown {
  const q = source.questionText ?? '';
  const stem = source.stem ?? '';
  const totalMarks = source.answerShape?.totalMarks ?? null;
  const base: KeyPartsBreakdown = { mode: 'verbatim', reasons: [], cardRules: [], units: [], totalMarks };
  if (!q.trim()) return { ...base, reasons: ['no-text'] };

  // Garbled or leak-prone text is never broken down: private-use glyphs, a
  // "headword= definition" line, or a column-interleaved paper where another
  // question's number lands mid-sentence ("length 2ℓabout an 8. its plane").
  // Symbol-font bullets (U+F0B7 and kin) are list marks, not garble.
  const privateUse = /[\uE000-\uF04F\uF051-\uF8FF]/.test(q.replace(/[\uF0A7\uF0B7\uF0D8\uF076\uF0FC\uF06E\uF0A8\uF0AE]/g, ''));
  if (privateUse || /^\s*\S+\s*=\s*\S/.test(q) && !/[\d(]/.test(q.split('=')[0]) || /\p{Ll}\s+\d{1,2}\.\s+\p{Ll}/u.test(q)) {
    return { ...base, mode: 'blocked', reasons: ['garbled'] };
  }

  // The question's own language decides: an English introduction in the
  // stem does not make "Pourquoi Marie a-t-elle besoin de vacances ?" English.
  const qLang = englishRatio(q);
  // …unless the question is only the printed item an English instruction in
  // the stem works on ("Explain in English the meaning of: … (line 9)").
  const stemLang = englishRatio(stem);
  const itemOfEnglishStem = stemLang.words >= 4 && stemLang.ratio >= 0.2 && commandMatches(stem).length > 0 && !/[?？]\s*(?:\([^)]*\))?\s*$/.test(q.trim());
  const lang = qLang.words >= 5 && !itemOfEnglishStem ? qLang : englishRatio(`${stem} ${q}`);
  const cardRules: KPSpan[] = [];
  for (const [from, raw] of [['stem', stem], ['q', q]] as const) {
    for (const m of raw.matchAll(CARD_RULE)) {
      const sp = spanOf(from, raw, m.index ?? 0, (m.index ?? 0) + m[0].length);
      if (sp && !cardRules.some(r => r.display.toLowerCase() === sp.display.toLowerCase())) cardRules.push(sp);
    }
  }
  // "Answer in English, giving TWO points and referring to the text.": the
  // whole printed sentence is the rule, not just its language.
  for (const [from, raw] of [['stem', stem], ['q', q]] as const) {
    for (const m of raw.matchAll(/(?:^|(?<=[.?!]\s))Answer\b[^.?!\n]{0,40}?\bin (?:English|ENGLISH|Irish|IRISH)\b[^.?!\n]*/g)) {
      const sp = spanOf(from, raw, m.index ?? 0, (m.index ?? 0) + m[0].length);
      if (!sp) continue;
      for (let i = cardRules.length - 1; i >= 0; i -= 1) if (cardRules[i].from === from && cardRules[i].start >= sp.start && cardRules[i].end <= sp.end) cardRules.splice(i, 1);
      if (!cardRules.some(r => r.display.toLowerCase() === sp.display.toLowerCase())) cardRules.push(sp);
    }
  }
  // "Answer the following questions in ENGLISH." — words between "answer"
  // and the language.
  for (const [from, raw] of [['stem', stem], ['q', q]] as const) {
    for (const m of raw.matchAll(/\b[Aa]nswer\b[^.?!:]{0,60}?\b(in (?:English|ENGLISH|Irish|IRISH))\b/g)) {
      const at = (m.index ?? 0) + m[0].length - m[1].length;
      const sp = spanOf(from, raw, at, at + m[1].length);
      if (sp && !cardRules.some(r => r.display.toLowerCase() === sp.display.toLowerCase() || (r.from === sp.from && r.start <= sp.start && r.end >= sp.end))) cardRules.push(sp);
    }
  }
  const latin = (q.match(/[A-Za-zÀ-ÿ]/g) ?? []).length;
  const letters = (q.match(/\p{L}/gu) ?? []).length;
  const irish = irishShare(q) >= 0.12 && /[áéíóú]/i.test(q);
  // A subject examined in English is never "in the exam language": its
  // formulas and flattened tables only look foreign to a word count.
  const englishMedium = ENGLISH_MEDIUM.has(source.subjectLabel.toLowerCase().trim().replace(/\s+/g, '-'));
  if (!englishMedium && ((lang.words >= 5 && lang.ratio < 0.14) || (letters > 8 && latin / letters < 0.5) || irish)) {
    // An exam-language question: its printed instruction words, glossed, and
    // the rest of it as printed, part by part.
    const lex = EXAM_LEXICONS[source.subjectLabel.toLowerCase().trim().replace(/\s+/g, '-')];
    const exam = lex ? buildExamLanguage(source, lex, base, cardRules) : null;
    if (exam) return exam;
    // Not English: name the instructions the lexicon recognises (with their
    // meaning) and leave the wording itself to the printed question.
    const units: KPUnit[] = commandMatches(q).map((m, i) => ({
      id: `${source.id}#${i + 1}`, ref: '', action: spanOf('q', q, m.index, m.end), actionKey: 'other',
      means: firstSentence(m.demand.requiredAction), count: null, focus: null, conditions: [], use: [], marks: null, flags: [],
    })).filter(u => u.action) as KPUnit[];
    return units.length && !irish
      ? { ...base, mode: 'glossed', reasons: ['non-english'], units, cardRules }
      : { ...base, reasons: ['non-english'], cardRules };
  }

  const units: KPUnit[] = [];
  const contexts: Array<{ from: 'q' | 'stem'; raw: string; pieces: Piece[] }> = [];
  const stemPieces = sentences(stem, 0, stem.length);
  const stemCtx = stemContextPieces(stem, stemPieces);
  if (stemCtx.givens.length) contexts.push({ from: 'stem', raw: stem, pieces: stemCtx.givens });
  const refersToPicture = PICTURE_REFERENCE.test(q);
  // How many labelled sources the stem names ("Text A", "Text B").
  const stemNamedCount = new Set([...stem.matchAll(NAMED_RE)].map(m => m[0].toLowerCase())).size;

  const alts = splitAlternatives(q);
  const banner = alts.length > 1 ? 'answer-one-alt' as const : undefined;
  let n = 0;
  const nextId = () => `${source.id}#${++n}`;
  const partMarks = new Map<string, number>();
  let leadIn: KPUnit | null = null;
  // A labelled part that introduces a list ("(ii) … each of the following
  // statements") serves the sub-parts after it until a part of its own kind.
  let leadInFamily: string | null = null;
  const usedLeadIns = new Set<string>();
  const keptLeadIns = new Set<string>();
  const familyOf = (ref: string) => /^\d+\.$/.test(ref) ? 'number' : /^\((?:i|ii|iii|iv|v|vi|vii|viii|ix|x)\)$/.test(ref) ? 'roman' : /^\([a-h]\)$/.test(ref) ? 'letter' : '';

  for (const alt of alts) {
    // Limits printed once before the labelled parts apply to every part:
    // "Answer each of the following with reference to a European region (not
    // in Ireland) that you have studied. (i) … (ii) …".
    let sharedConditions: KPSpan[] = [];
    const parts = splitParts(q, alt.start, alt.end, alt.altGroup);
    for (const [partIndex, part] of parts.entries()) {
      if (leadIn && leadInFamily && familyOf(part.ref) === leadInFamily) { leadIn = null; leadInFamily = null; }
      const tariffHit = /\(\s*(\d{1,3})\s*(?:marks?|mharc|marc)?\s*\)\s*$/i.exec(q.slice(part.start, part.end));
      // "(25)" printed for the whole of part (b) is not this sub-part's tariff.
      const tariff = tariffHit && !(totalMarks != null && Number(tariffHit[1]) > totalMarks) ? tariffHit : null;
      const partEnd = tariff ? part.start + tariff.index : part.end;
      const pieces = sentences(q, part.start, partEnd);
      const ctxPieces: Piece[] = [];
      const partUnits: KPUnit[] = [];
      const unitPiece = new Map<string, Piece>();
      let lastStatement: Piece | null = null;
      // Under "Circle the correct option in each of the following statements"
      // or "True or false:", each labelled part is a statement to judge, not
      // an instruction ("State broadcaster RTE …" is not the command State).
      const statementList = Boolean(part.ref && leadIn && /^(?:true-false|tick|choice)$/.test(leadIn.actionKey));
      for (const piece of statementList ? [] : pieces) {
        const text = q.slice(piece.start, piece.end).trim();
        if (!text) continue;
        const lastUnit = partUnits[partUnits.length - 1];
        if ((/\b(?:may|can) be (?:estimated|assumed|omitted|ignored|used|drawn|shown)|\bneed not\b|\bare not (?:required|needed)\b/i.test(text) && /^\(?\s*(?:Note|Any|All|You|The|Hidden|Construction|Dimensions|Fillets|Chamfers)\b/.test(text))
          || /^\(?\s*Note\s*:/i.test(text) || /^\(?\s*Scale\s+\d+\s*:\s*\d+\b/i.test(text)) {
          const sp = spanOf('q', q, piece.start, piece.end);
          if (sp && !cardRules.some(r => r.display === sp.display)) cardRules.push(sp);
          continue;
        }
        // A printed bullet does not change what the sentence is.
        const tt = text.replace(/^[•·▪‣◦]\s*/, '');
        if (WHOLE_SENTENCE.test(tt)) {
          const sp = spanOf('q', q, piece.start, piece.end);
          if (sp && !cardRules.some(r => r.display === sp.display)) cardRules.push(sp);
          continue;
        }
        const points = POINTS_SENTENCE.exec(tt);
        if (points && lastUnit && lastUnit.action && !lastUnit.flags.includes('as-printed')) {
          // Offsets from the untrimmed printed piece.
          const counted = new RegExp(`${points[1] ?? ''}${points[2]}\\s+${points[3].replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}`, 'i').exec(q.slice(piece.start, piece.end));
          const at = counted ? piece.start + counted.index : -1;
          const sp = counted ? spanOf('q', q, at, at + counted[0].length) : null;
          if (!lastUnit.count && sp) {
            lastUnit.count = sp;
            lastUnit.countValue = NUMBER_WORDS[points[2].toLowerCase()];
            lastUnit.countNoun = singular(points[3].trim().split(/\s+/).pop()!.toLowerCase());
            // "Make two points in your response, supporting them with …".
            const rest = /,\s*((?:supporting|referring|using|drawing|developing|illustrating)\b[^.?!]*)/i.exec(q.slice(at, piece.end));
            if (rest) {
              const rs = at + rest.index + rest[0].length - rest[1].length;
              const lim = spanOf('q', q, rs, rs + rest[1].length);
              if (lim) lastUnit.conditions.push(lim);
            }
          } else {
            const whole = spanOf('q', q, piece.start, piece.end);
            if (whole) lastUnit.conditions.push(whole);
          }
          continue;
        }
        if (YOUR_SHOULD.test(tt) && lastUnit && !lastUnit.flags.includes('as-printed')) {
          const c = YOUR_SHOULD_COUNT.exec(q.slice(piece.start, piece.end));
          const whole = spanOf('q', q, piece.start, piece.end);
          if (c && !lastUnit.count && /\binclude\b/i.test(q.slice(piece.start, piece.start + c.index))) {
            const at = piece.start + c.index;
            const sp = spanOf('q', q, at, at + c[0].length);
            if (sp) {
              lastUnit.count = sp;
              lastUnit.countValue = NUMBER_WORDS[c[2].toLowerCase()];
              lastUnit.countNoun = singular(c[3].trim().split(/\s+/).pop()!.toLowerCase());
            }
          } else if (whole) lastUnit.conditions.push(whole);
          continue;
        }
        if (SUPPORT_TAIL.test(tt) && lastUnit && !lastUnit.flags.includes('as-printed')) {
          const sp = spanOf('q', q, piece.start, piece.end);
          if (sp) lastUnit.conditions.push(sp);
          continue;
        }
        if (TAIL_CONDITION.test(tt) && lastUnit) {
          const sp = spanOf('q', q, piece.start, piece.end);
          if (sp) lastUnit.conditions.push(sp);
          continue;
        }
        // "What events took place? Name two." — the count belongs to the question.
        const countSentence = COUNT_SENTENCE.exec(text);
        if (countSentence && lastUnit && !lastUnit.count && lastUnit.action) {
          const word = countSentence[1];
          const at = q.slice(piece.start, piece.end).search(new RegExp(`\\b${word}\\b`, 'i')) + piece.start;
          const noun = countSentence[2];
          const cEnd = noun ? q.indexOf(noun, at + word.length) + noun.length : at + word.length;
          lastUnit.count = spanOf('q', q, at, cEnd);
          lastUnit.countValue = NUMBER_WORDS[word.toLowerCase()];
          const firstNoun = lastUnit.focus && /^([\p{Ll}-]{3,}s)\b/u.exec(lastUnit.focus.display);
          lastUnit.countNoun = noun ? singular(noun) : firstNoun ? singular(firstNoun[1]) : 'point';
          continue;
        }
        if (DETAILS_SENTENCE.test(text) && lastUnit && /^(?:wh-|explain-how)/.test(lastUnit.actionKey)) {
          const sp = spanOf('q', q, piece.start, piece.end);
          if (sp) lastUnit.conditions.push(sp);
          continue;
        }
        if (/^\([^()]{3,120}\)\.?$/.test(text) && lastUnit && !PAREN_COUNT.test(text) && !LOCATOR_ONLY.test(text.replace(/\.$/, ''))
          && !CARD_RULE.test(text)) {
          CARD_RULE.lastIndex = 0;
          const sp = spanOf('q', q, piece.start, piece.end);
          if (sp) lastUnit.conditions.push(sp);
          continue;
        }
        CARD_RULE.lastIndex = 0;
        // "(Two points, about 50 words in total.)"
        const paren = PAREN_COUNT.exec(text);
        if (paren && lastUnit) {
          if (!lastUnit.count) {
            const at = q.indexOf(paren[1], piece.start);
            lastUnit.count = spanOf('q', q, at, at + paren[1].length + 1 + paren[2].length);
            lastUnit.countValue = NUMBER_WORDS[paren[1].toLowerCase()];
            lastUnit.countNoun = singular(paren[2]);
          }
          continue;
        }
        if (TAIL_UNIT.test(text)) {
          const m = /^(\s*)((?:Explain|Justify|Give (?:a )?reasons? for|Support|Illustrate))\s+(your (?:answers?|choices?))/i.exec(q.slice(piece.start, piece.end));
          if (m) {
            const aStart = piece.start + m[1].length;
            const fStart = aStart + m[2].length + 1;
            const key = /^illustrate/i.test(m[2]) ? 'illustrate-tail' : 'justify-tail';
            const unit: KPUnit = {
              id: nextId(), ref: part.ref, altGroup: part.altGroup,
              action: spanOf('q', q, aStart, aStart + m[2].length), actionKey: key, means: MEANS[key],
              count: null, focus: spanOf('q', q, fStart, fStart + m[3].length), conditions: [], use: [], marks: null, flags: [],
            };
            const restStart = fStart + m[3].length;
            for (const t of triggersIn(q, restStart, piece.end)) {
              const at = restStart + (t.index ?? 0);
              const sp = spanOf('q', q, at, conditionEnd(q, at + t[0].length, piece.end, t[0]));
              if (sp) unit.conditions.push(sp);
            }
            partUnits.push(unit);
            unitPiece.set(unit.id, piece);
            continue;
          }
        }
        // "Examine the aerial photograph of Dundalk accompanying this paper."
        // says where to look; it is material, not a task.
        if (/^(?:Examine|Study|Look (?:closely )?at|Read) (?:the|this|these)\b[^.?!]*$/i.test(text.replace(/[.!]\s*$/, ''))
          && (MATERIAL_RE.test(text) || /^\S+(?:\s+\S+)?\s+(?:the|this|these)\s+(?:[\p{L}-]+\s+){0,3}(?:photograph|photo|map|diagram|graph|table|chart|image|extract|passage|text|article|document|source|cartoon|poster|picture|figure)s?\b/iu.test(text))
          && !/\b(?:and|then)\s+(?:explain|describe|answer|discuss|identify|name)\b/i.test(text)) {
          MATERIAL_RE.lastIndex = 0;
          ctxPieces.push(piece);
          continue;
        }
        MATERIAL_RE.lastIndex = 0;
        const made: KPUnit[] = [];
        const clauses = clausesOf(q, piece);
        for (const clause of clauses) {
          const unit = buildUnit(q, clause, { ref: part.ref, altGroup: part.altGroup, id: `${source.id}#${n + 1}`, from: 'q' });
          if (unit) { n += 1; made.push(unit); unitPiece.set(unit.id, piece); continue; }
          // A clause of a task sentence that holds an instruction the parser
          // cannot read is shown as printed rather than dropped.
          const sp = clauses.length > 1 ? spanOf('q', q, clause.start, clause.end) : null;
          if (sp && sp.display.split(/\s+/).length >= 3 && /\b(?:find|list|name|identify|describe|explain|give|state|write|calculate|draw|label|outline|discuss|suggest|compare|show|complete|choose|select)\b/i.test(sp.display)) {
            const u = asPrinted(nextId(), part.ref, part.altGroup, sp);
            made.push(u);
            unitPiece.set(u.id, piece);
          }
        }
        // The statement a question is about: "Linda is well suited to the
        // work. Do you agree?" / "The narrator describes his colleague's
        // face. Give details." / "… Discuss this statement …".
        for (const unit of made) {
          if (!lastStatement) break;
          const statement = spanOf('q', q, lastStatement.start, lastStatement.end);
          if (!statement) break;
          // "draw and label: the fixed costs … and the variable costs …": a
          // command opening a list is about the list, not the statement.
          const opensList = unit.action && /^\s*:/.test(q.slice(unit.action.end, unit.action.end + 3));
          if (!unit.focus && !opensList && !/^(?:yes-no|either-or|true-false|justify-tail|illustrate-tail|as-printed)$/.test(unit.actionKey)) unit.focus = statement;
          else if (unit.focus && (STATEMENT_FOCUS.test(unit.focus.display) || /^(?:it|they|this|these|he|she|its|their)\b|\beach(?: of them)?$/i.test(unit.focus.display))) {
            unit.use.unshift({ ...statement, kind: 'material' });
          }
        }
        partUnits.push(...made);
        if (!made.length) {
          if (/\?\s*$/.test(text)) {
            // A question the breakdown cannot read is shown as printed, never dropped.
            const sp = spanOf('q', q, piece.start, piece.end);
            if (sp) { const u = asPrinted(nextId(), part.ref, part.altGroup, sp); partUnits.push(u); unitPiece.set(u.id, piece); }
          } else if (lastUnit && !lastUnit.flags.includes('as-printed') && (text.match(/\b(?:is|are|was|were|has|have|had|will|would|can|could|the|a|an|to|of|in|on|for|with|by|and|that|this|you|your)\b/gi) ?? []).length < 2
            && text.split(/\s+/).length >= 2 && !/^[•·▪‣◦\-–\uF0B7]/.test(text) && !/:\s*$/.test(q.slice(Math.max(0, piece.start - 3), piece.start))
            && /\b(?:table|tick|box)\b/i.test(q.slice(lastUnit.action?.start ?? piece.start, piece.start))) {
            // "… in the table below. Oil/Gas exploitation Quarrying Mining": a
            // flattened table after the ask is what it chooses or matches from.
            const sp = spanOf('q', q, piece.start, piece.end);
            if (sp && !lastUnit.use.some(u => u.start === sp.start)) lastUnit.use.push({ ...sp, kind: 'options' });
          } else {
            ctxPieces.push(piece);
            lastStatement = piece;
          }
        }
      }

      // Units that must not borrow a neighbour's focus: a question that is
      // its own job, or an "Explain your answer" tail.
      const selfContained = (u: KPUnit) => /^(?:yes-no|either-or|true-false|justify-tail|illustrate-tail|as-printed)$/.test(u.actionKey) || u.actionKey.startsWith('wh-');
      // Right to left, so a chain ("Name, briefly describe and discuss X")
      // passes the focus all the way back.
      for (let i = partUnits.length - 2; i >= 0; i -= 1) {
        const a = partUnits[i];
        const b = partUnits[i + 1];
        if (!b || a.focus || !a.action || !b.action || selfContained(a) || selfContained(b)) continue;
        if (b.action.start - a.action.end >= 40 || a.action.from !== b.action.from) continue;
        // "draw and label: …" is one job.
        if ((/^label$/.test(b.actionKey) || a.actionKey === 'choose') && /^\s+and\s+$/i.test(q.slice(a.action.end, b.action.start))) {
          const joined = spanOf('q', q, a.action.start, b.action.end);
          if (joined) {
            const lead = a.actionKey === 'choose' || /^(?:state|other|tick)$/.test(a.actionKey) ? b : a;
            partUnits.splice(i, 2, { ...a, actionKey: lead.actionKey, means: lead.means, action: joined, focus: b.focus, focusMore: b.focusMore, count: a.count ?? b.count, countValue: a.countValue ?? b.countValue, conditions: [...a.conditions, ...b.conditions], use: [...a.use, ...b.use.filter(x => !a.use.some(y => y.display === x.display))] });
            const piece = unitPiece.get(a.id) ?? unitPiece.get(b.id);
            if (piece) unitPiece.set(a.id, piece);
            continue;
          }
        }
        if (!b.focus) continue;
        // "Name and explain X": a command left without a focus shares the next
        // one's. "Identify and describe two paintings": the count is shared
        // too, and the two jobs are done together, one space per painting.
        a.focus = b.focus;
        if (!a.conditions.length) a.conditions = [...b.conditions];
        if (!a.count && b.count) { a.count = b.count; a.countValue = b.countValue; a.countNoun = b.countNoun; }
        // Two commands on one object ("Identify and explain the benefits",
        // "Name and explain one method") are answered together.
        if (/^\s+and\s+$/i.test(q.slice(a.action.end, b.action.start)) || (EXTENDED.has(a.actionKey.replace(/-.*/, '')) && EXTENDED.has(b.actionKey.replace(/-.*/, ''))) || (b.countValue ?? 0) > 1) {
          a.jointWith = b.id;
          // "Determine and indicate the true length": the shown gloss is the
          // bigger of the two jobs, not the smaller.
          if (JOB_WEIGHT(a.actionKey) > JOB_WEIGHT(b.actionKey)) { b.actionKey = a.actionKey; b.means = a.means; }
          // "With reference to a region you have studied, describe and
          // explain …": a limit on the first verb is on the joint job.
          for (const c of a.conditions) if (!b.conditions.some(x => x.from === c.from && x.start === c.start)) b.conditions.unshift(c);
        }
      }
      // "Identify three principles … and describe how each principle
      // identified …": the second job is done for each of the first's items.
      for (let i = 1; i < partUnits.length; i += 1) {
        const a = partUnits[i - 1];
        const b = partUnits[i];
        if (!a.action || !b.action || !(a.countValue && a.countValue > 1) || a.jointWith) continue;
        // "… and, for each named method, give one example": the limit that
        // ties the second job to each of the first's items.
        const perItem = a.countNoun
          ? [...a.conditions, ...b.conditions].find(c => new RegExp(`\\beach\\s+(?:[\\p{L}-]+\\s+)?${a.countNoun}`, 'iu').test(c.display))
          : undefined;
        if (b.count && !/^each$/i.test(b.count.display) && !perItem) continue;
        const eachRef = perItem || /\beach\b/i.test(`${b.focus?.display ?? ''} ${b.action.display} ${b.count?.display ?? ''}`);
        if (!eachRef || !/\band\b[^.?!]*$/i.test(q.slice(a.action.end, b.action.start))) continue;
        // One space per counted item holds both jobs. The second job's own
        // count ("one example") is then a limit on each item, and the "for
        // each" limit moves to the job it governs.
        if (b.count && !/^each$/i.test(b.count.display)) b.conditions.unshift(b.count);
        if (perItem && a.conditions.includes(perItem)) {
          a.conditions = a.conditions.filter(c => c !== perItem);
          b.conditions.splice(b.count && !/^each$/i.test(b.count.display) ? 1 : 0, 0, perItem);
        }
        b.count = a.count;
        b.countValue = a.countValue;
        b.countNoun = a.countNoun;
        a.jointWith = b.id;
      }
      for (const u of partUnits) if (u.action && !unitPiece.has(u.id)) unitPiece.set(u.id, pieces[0]);

      // "Define (i) isotopes, (ii) relative atomic mass." / "What colour is
      // observed in a flame test on a salt of (i) lithium, (ii) copper?": an
      // enumeration inside the sentence gives one part per printed item.
      for (let i = 0; i < partUnits.length; i += 1) {
        const u = partUnits[i];
        if (!u.focus || u.focus.from !== 'q' || u.flags.includes('as-printed') || u.item) continue;
        const text = q.slice(u.focus.start, u.focus.end);
        const labels = [...text.matchAll(/(?<![\p{L}\p{N}])\((i{1,3}|iv|v|vi|[a-f])\)\s+/gu)];
        const roman = ['i', 'ii', 'iii', 'iv', 'v', 'vi'];
        const inOrder = labels.length >= 2 && labels.every((m, k) => m[1] === (/^[a-f]$/.test(labels[0][1]) ? 'abcdef'[k] : roman[k]));
        if (!inOrder) continue;
        const items: Array<{ ref: string; span: KPSpan }> = [];
        labels.forEach((m, k) => {
          const s0 = u.focus!.start + m.index! + m[0].length;
          const e0 = k + 1 < labels.length ? u.focus!.start + labels[k + 1].index! : u.focus!.end;
          const tail = /(?:[,;]\s*(?:and|or)?|\s+(?:and|or))\s*$/i.exec(q.slice(s0, e0));
          const sp = spanOf('q', q, s0, tail ? e0 - tail[0].length : e0);
          if (sp) items.push({ ref: `(${m[1]})`, span: sp });
        });
        if (items.length !== labels.length) continue;
        // "for each part (i) and (ii) below" names parts; it lists nothing.
        if (items.some(x => x.span.display.length < 3 || /^(?:and|or|below|above|the)\b/i.test(x.span.display))) continue;
        // "how (i) health and (ii) responsible living might influence food
        // choices": the last item runs on into the question they share.
        const verbIn = (t: string) => /\b(?:might|may|can|could|will|would|should|is|are|was|were|has|have|do|does|did)\b/i.test(t);
        if (verbIn(items[items.length - 1].span.display) && !items.slice(0, -1).some(x => verbIn(x.span.display))) continue;
        const head = spanOf('q', q, u.focus.start, u.focus.start + labels[0].index!);
        const spread = items.map(({ ref, span }) => ({
          ...u, id: nextId(), ref: `${u.ref ?? ''}${ref}`, focus: head, focusMore: undefined, item: span,
          conditions: [...u.conditions], use: [...u.use], flags: [...u.flags],
        }));
        partUnits.splice(i, 1, ...spread);
        for (const x of spread) unitPiece.set(x.id, unitPiece.get(u.id) ?? pieces[0]);
        i += spread.length - 1;
      }

      // A unit that introduces a printed list takes one unit per item.
      const consumed: Array<[number, number]> = [];
      for (let i = 0; i < partUnits.length; i += 1) {
        const u = partUnits[i];
        if (!u.action || u.action.from !== 'q' || u.flags.includes('as-printed')) continue;
        const piece = unitPiece.get(u.id)!;
        const next = partUnits.slice(i + 1).find(x => x.action && x.action.from === 'q' && x.action.start > u.action!.end);
        const regionEnd = next ? (unitPiece.get(next.id)?.start ?? next.action!.start) : partEnd;
        const colonAt = q.slice(u.action.end, piece.end).search(/:(?=\s|$)/);
        const colon = colonAt >= 0 ? u.action.end + colonAt : -1;
        const listLead = /\bthe following\b/i.test(`${u.count?.display ?? ''} ${u.focus?.display ?? ''}`) || u.actionKey === 'true-false';
        let regionStart = -1;
        if (colon >= 0 && !u.conditions.some(c => c.from === 'q' && colon >= c.start && colon < c.end)) regionStart = colon + 1;
        else if (listLead) {
          // "… in the following lines. sit qui me raptum …": the list can
          // start inside the same printed sentence, after the lead's stop.
          const from = u.focus?.end ?? u.action.end;
          const stop = q.slice(from, piece.end).search(/[.](?=\s+\S)/);
          regionStart = stop >= 0 ? from + stop + 1 : piece.end;
        }
        let items: KPSpan[] = [];
        // A limit sentence printed straight after the instruction ("Put a
        // tick (✓) in the appropriate boxes.") is stepped over, not a stop.
        for (let moved = true; moved && regionStart >= 0;) {
          moved = false;
          const lead = u.conditions.find(c => c.from === 'q' && c.start >= regionStart && /^\s*$/.test(q.slice(regionStart, c.start)));
          if (lead) { regionStart = lead.end + (/^[.!?]/.test(q.slice(lead.end, lead.end + 1)) ? 1 : 0); moved = true; }
        }
        const limitAfter = [...u.conditions, ...cardRules].filter(c => c.from === 'q' && c.start > regionStart).map(c => c.start);
        const listEnd = Math.min(regionEnd, partEnd, ...limitAfter);
        if (regionStart >= 0 && regionStart < listEnd) items = listItems(q, 'q', regionStart, listEnd, u.actionKey === 'true-false');
        // "given the following data: • Speed 20 m/s • …": supplied values,
        // not items to answer.
        if (items.length && /\b(?:the following|these)\s+(?:data|details|information|motion|specifications?|dimensions|values|measurements|readings|costs|figures)(?=\s*(?::|below|shown|given|supplied|\(|$))/i.test(q.slice(u.action.start, regionStart))) {
          for (const it of items) if (!u.use.some(x => x.display === it.display)) u.use.push({ ...it, kind: 'given' });
          consumed.push([regionStart, listEnd]);
          continue;
        }
        if (regionStart >= 0 && items.length) {
          for (const m of q.slice(regionStart, listEnd).matchAll(LOCATOR_RE)) {
            const sp = spanOf('q', q, regionStart + (m.index ?? 0), regionStart + (m.index ?? 0) + m[0].length);
            if (sp && !u.use.some(x => x.display === sp.display)) u.use.push({ ...sp, kind: 'locator' });
          }
        }
        // The list printed in the stem: "• Multi-factor authentication • …",
        // or the rows of an answer table printed as bare lines.
        if (!items.length && listLead && /^\s*[•◆▪●]/.test(stem)) items = listItems(stem, 'stem', 0, stem.length);
        if (!items.length && listLead && stem.trim() && !BOILERPLATE.test(stem) && !RUBRIC.test(stem.trim())) {
          const lines = listItems(stem, 'stem', 0, stem.length, !/\n/.test(stem));
          if (lines.length >= 2 && lines.length <= 8 && lines.every(l => l.display.split(/\s+/).length <= 10 && !commandMatches(l.display).some(m => m.index === 0))) items = lines;
        }
        // "Examine how … one of the following: • Coastal processes" — a card
        // for one option: the option is the item and the choice is made.
        if (items.length === 1 && isChoice(u, { q, stem })) {
          u.item = items[0];
          u.count = null;
          u.countValue = undefined;
          consumed.push([regionStart, regionEnd]);
          continue;
        }
        // "Explain the terms user interface and Bluetooth."
        if (!items.length && /\bterms$/i.test(u.action.display) && u.focus) {
          items = listItems(q, 'q', u.focus.start, u.focus.end);
          if (items.length >= 2) u.focus = null;
        }
        if (u.actionKey === 'choose' && items.length <= 1 && u.focus && /^(?:one |any one )?(?:of )?the following$/i.test(u.focus.display)) {
          // The card has already made the choice ("Choose one of the following: • Tony O'Malley").
          partUnits.splice(i, 1);
          i -= 1;
          if (regionStart >= 0) consumed.push([regionStart, regionEnd]);
          continue;
        }
        // "using the following headings: • subject matter • …": the items are
        // headings for the answer, and the limit runs to the end of the list.
        const headingLimit = colon >= 0 ? u.conditions.find(c => c.from === 'q' && c.end === colon && /headings?$/i.test(c.display)) : undefined;
        if (headingLimit && items.length >= 2) {
          const whole = spanOf('q', q, headingLimit.start, items[items.length - 1].end);
          if (whole) u.conditions.splice(u.conditions.indexOf(headingLimit), 1, whole);
          u.headings = items;
          consumed.push([regionStart, regionEnd]);
          continue;
        }
        // "Choose any two of the following battles. … explain their
        // importance: Arginusae; Mantinea; …" — the list is what was chosen from.
        const chooser = partUnits.slice(0, i).reverse().find(x => x.actionKey === 'choose' && isChoice(x, { q, stem }));
        if (chooser && items.length >= 2) {
          const whole = spanOver(q, items);
          if (whole) chooser.use.push({ ...whole, kind: 'options' });
          consumed.push([regionStart, regionEnd]);
          continue;
        }
        if (!items.length && listLead && regionStart >= 0 && regionStart < listEnd) {
          const lines = listItems(q, 'q', regionStart, listEnd, true);
          if (lines.length >= 1 && lines.length <= 8 && lines.every(l => l.display.split(/\s+/).length <= 40)) items = lines;
        }
        // "… in the following lines. sit qui me raptum …": one printed item.
        if (items.length === 1 && listLead && !isChoice(u, { q, stem }) && !/^(?:true-false|tick|compare|contrast|compare-contrast|distinguish)$/.test(u.actionKey)) {
          u.item = items[0];
          for (const other of partUnits) if (other !== u && other.focus && u.focus && other.focus.start === u.focus.start && !other.item) other.item = items[0];
          consumed.push([regionStart, regionEnd]);
          continue;
        }
        if (items.length >= 2 || (items.length === 1 && /^(?:true-false|tick|compare|contrast|compare-contrast|distinguish)$/.test(u.actionKey))) {
          const aw = `${u.action.display} ${u.focus?.display ?? ''}`;
          const whichOf = /^(?:(?:identify|state|say|indicate)\s+)?(?:which|what)\b/i.test(aw) && /\bof the following\b/i.test(aw);
          const spread = spreadOver(u, items, { q, stem }, nextId, whichOf || (isChoice(u, { q, stem }) && (u.countValue ?? 0) < items.length));
          // "Describe and explain any two of the following: • …": the joined
          // first verb goes with the second into every item.
          const partnerAt = partUnits.findIndex(p => p.jointWith === u.id);
          if (partnerAt >= 0 && spread.length > 1 && spread[0].id !== u.id) {
            const partner = partUnits[partnerAt];
            const withPartners = spread.flatMap(x => [{ ...partner, id: nextId(), jointWith: x.id, item: x.item, conditions: [...partner.conditions], use: [...partner.use], flags: [...partner.flags] }, x]);
            partUnits.splice(i, 1, ...withPartners);
            partUnits.splice(partnerAt, 1);
            i += withPartners.length - 2;
          } else {
            partUnits.splice(i, 1, ...spread);
            i += spread.length - 1;
          }
          if (regionStart >= 0) consumed.push([regionStart, regionEnd]);
        }
      }
      const liveCtx = ctxPieces.filter(p => !consumed.some(([s, e]) => p.start >= s && p.end <= e + 1));

      // A lead-in ending in ":" gives its command to the bare items after it.
      if (!partUnits.length && leadIn) {
        const item = spanOf('q', q, part.start, partEnd);
        const labelled = parts.filter(p => p.ref).length;
        if (item && (leadIn.actionKey === 'match' || (isChoice(leadIn, { q, stem }) && (leadIn.countValue ?? 0) < labelled))) {
          if (!leadIn.countNoun && (leadIn.countValue ?? 0) > 1) leadIn.countNoun = 'choice';
          leadIn.use.push({ ...item, kind: 'options' });
          keptLeadIns.add(leadIn.id);
        } else if (item) {
          const ref = leadInFamily && leadIn.ref ? `${leadIn.ref}${part.ref}` : part.ref;
          const header = /\s+(?:True\s+False|Yes\s+No)$/i.exec(item.text);
          const clean = header ? spanOf('q', q, item.start, item.end - header[0].length) ?? item : item;
          const judged = /^(?:true-false|tick)$/.test(leadIn.actionKey);
          const keepCount = leadIn.count && !/\beach\b|\bthe following\b|^all\b|^both\b/i.test(leadIn.count.display) && !isChoice(leadIn, { q, stem });
          partUnits.push({ ...leadIn, id: nextId(), ref, altGroup: part.altGroup, item: clean, focus: judged ? null : leadIn.focus, count: keepCount ? leadIn.count : null, countValue: keepCount ? leadIn.countValue : undefined, countNoun: keepCount ? leadIn.countNoun : undefined, conditions: [...leadIn.conditions], use: [...leadIn.use], flags: [...leadIn.flags] });
        }
        usedLeadIns.add(leadIn.id);
      }
      // A preamble with limits but no task of its own ("Answer each of the
      // following with reference to …") lends its limits to every part.
      if (!part.ref && parts.slice(partIndex + 1).some(p => p.ref) && partUnits.every(u => /^answer\b/i.test(u.action?.display ?? ''))) {
        const pre: KPSpan[] = [];
        for (const t of triggersIn(q, part.start, partEnd)) {
          const at = part.start + (t.index ?? 0);
          if (pre.some(x => at >= x.start && at < x.end)) continue;
          const sp = spanOf('q', q, at, conditionEnd(q, at + t[0].length, partEnd, t[0]));
          if (sp && !emptyLimit(sp, t[0])) pre.push(sp);
        }
        for (let i = pre.length - 1; i > 0; i -= 1) {
          if (/^[\s,]*$/.test(q.slice(pre[i - 1].end, pre[i].start)) && /^(?:that|which|who|you)\b/i.test(pre[i].display)) {
            const merged = spanOf('q', q, pre[i - 1].start, pre[i].end);
            if (merged) pre.splice(i - 1, 2, merged);
          }
        }
        sharedConditions = pre;
        partUnits.splice(0, partUnits.length);
      } else if (part.ref && sharedConditions.length) {
        for (const u of partUnits) u.conditions.unshift(...sharedConditions.filter(c => !u.conditions.some(x => x.start === c.start)));
      }
      // A question part the breakdown cannot read is shown as printed.
      if (!partUnits.length && part.ref && !(leadIn && usedLeadIns.has(leadIn.id))) {
        const sp = spanOf('q', q, part.start, partEnd);
        if (sp && sp.display.split(/\s+/).length >= 3) partUnits.push(asPrinted(nextId(), part.ref, part.altGroup, sp));
      }
      // "True or false:" before the statements is the instruction itself.
      if (!part.ref && !partUnits.length && parts.slice(partIndex + 1).some(p => p.ref)) {
        const tf = /^\s*(True or false|True\/False)\s*[:.]?\s*$/i.exec(q.slice(part.start, partEnd));
        if (tf) {
          const s0 = part.start + tf[0].indexOf(tf[1]);
          const action = spanOf('q', q, s0, s0 + tf[1].length);
          if (action) partUnits.push({ id: nextId(), ref: '', action, actionKey: 'true-false', means: MEANS['true-false'], count: null, focus: null, conditions: [], use: [], marks: null, flags: [] });
        }
      }
      // An instruction printed once before labelled parts ("Circle the
      // correct option in each of the following statements.") serves every
      // part that has no instruction of its own.
      const last = partUnits[partUnits.length - 1];
      if (last && !part.ref && last.action && parts.slice(partIndex + 1).some(p => p.ref)) { leadIn = last; leadInFamily = null; }
      const nextPart = parts[partIndex + 1];
      if (last && part.ref && last.action && !last.item && nextPart?.ref && familyOf(nextPart.ref) !== familyOf(part.ref)
        && (/\bthe following\b/i.test(`${last.count?.display ?? ''} ${last.focus?.display ?? ''}`) || /[:]\s*$/.test(q.slice(part.start, partEnd)))) {
        leadIn = last;
        leadInFamily = familyOf(part.ref);
      }
      // Material named anywhere in the part (or the stem) serves every unit
      // in it — a scene-setting photograph in the stem only when the question
      // itself points at a picture.
      const shared = materialIn(q, liveCtx.map(p => [p.start, p.end]), 'q')
        .concat(materialIn(stem, stemCtx.material.map(p => [p.start, p.end]), 'stem'))
        .filter(u => !(u.from === 'stem' && PICTURE.test(u.display) && !refersToPicture));
      for (const unit of partUnits) {
        if (unit.flags.includes('as-printed')) continue;
        const ownNamed = unit.use.filter(u => u.kind === 'material' && new RegExp(NAMED_RE.source).test(u.display));
        for (const u of shared) {
          // "Text B" in the part: "Text A" in the stem belongs to another part.
          if (ownNamed.length && new RegExp(NAMED_RE.source).test(u.display) && !ownNamed.some(o => o.display.toLowerCase() === u.display.toLowerCase())) continue;
          // A part that never points at a text, image or document ("Explain two
          // arguments that Socrates makes in the Crito") does not borrow the
          // stem's labelled ones.
          if (u.from === 'stem' && stemNamedCount >= 2 && new RegExp(NAMED_RE.source).test(u.display) && !/\b(?:texts?|extracts?|documents?|sources?|images?|photographs?|pictures?|figures?|fig|tables?|graphs?|maps?|diagrams?|passages?|poems?|cartoons?)\b/i.test(q)) continue;
          if (unit.use.some(x => x.display.toLowerCase() === u.display.toLowerCase() || (x.kind === 'material' && headOf(x.display) === headOf(u.display)))) continue;
          unit.use.push(u);
        }
        const headings = headingsFrom(unit, { q, stem });
        if (headings) unit.headings = headings;
      }
      if (tariff && partUnits.length === 1) partMarks.set(partUnits[0].id, Number(tariff[1]));
      contexts.push({ from: 'q', raw: q, pieces: liveCtx });
      units.push(...partUnits);
    }
  }

  // A lead-in that handed its instruction to its items is shown through them.
  for (const id of usedLeadIns) {
    if (keptLeadIns.has(id)) continue;
    const at = units.findIndex(u => u.id === id);
    if (at >= 0) units.splice(at, 1);
  }

  // A lead-in in the stem ("Give the collective name for:", "Write the
  // meaning of any five of the following Kanji in English") supplies the
  // command; each printed item in the question is what it applies to.
  if (!units.some(u => u.action) && stem.trim()) {
    let lead: KPUnit | null = null;
    for (const p of stemPieces) {
      if (BOILERPLATE.test(stem.slice(p.start, p.end))) continue;
      const clauses = clausesOf(stem, { start: p.start, end: stem.length > p.end && /:\s*$/.test(stem.slice(p.start, p.end)) ? stem.length : p.end });
      // The instruction the printed items complete is the one that ends at the
      // colon: "Choose one woman … and describe her life story using each of
      // the following headings:" lends "describe", not "Choose".
      const byColon = [...clauses].reverse().find(c => /:\s*$/.test(stem.slice(c.start, c.end)));
      for (const clause of byColon ? [byColon, ...clauses.filter(c => c !== byColon)] : clauses) {
        lead = buildUnit(stem, clause, { ref: '', id: `${source.id}#lead`, from: 'stem' });
        // "Scríobh … Write …": an Irish instruction on a bilingual stem is
        // passed over for the English one.
        if (lead?.action && IRISH_FUNCTION.has(lead.action.display.toLowerCase().split(/\s+/)[0])) { lead = null; continue; }
        if (lead) break;
      }
      if (lead) break;
    }
    if (lead && lead.action) {
      units.splice(0, units.length);
      const colon = stem.indexOf(':', lead.action.start);
      const stemItems = colon > 0 ? listItems(stem, 'stem', colon + 1, stem.length) : [];
      const perList = (lead.count && /\beach\b|\bthe following\b/i.test(lead.count.display)) || isChoice(lead, { q, stem });
      if (stemItems.length >= 2) {
        for (const item of stemItems) {
          units.push({ ...lead, id: nextId(), item, count: perList ? null : lead.count, countValue: perList ? undefined : lead.countValue, conditions: [...lead.conditions], use: [...lead.use] });
        }
      } else {
        const parts = splitParts(q, 0, q.length);
        for (const part of parts) {
          const item = spanOf('q', q, part.start, part.end);
          if (!item) continue;
          const keep = parts.length === 1 && !perList;
          const judged = /^(?:true-false|tick)$/.test(lead.actionKey);
          units.push({ ...lead, id: nextId(), ref: part.ref, item, focus: judged ? null : lead.focus, count: keep ? lead.count : null, countValue: keep ? lead.countValue : undefined, countNoun: keep ? lead.countNoun : undefined, conditions: [...lead.conditions], use: [...lead.use] });
        }
      }
    }
  }

  if (!units.length) return { ...base, reasons: ['command-missing'], cardRules };

  // Subject and card-wide readings of the command, givens, marks.
  const dcg = /^dcg-/.test(source.id) || /^dcg$|design (?:&|and) communication graphics/i.test(source.subjectLabel);
  const mathsSubject = /^(?:maths|mathematics|applied[- ]maths|physics|chemistry|engineering|construction[- ]studies|technology)$/i.test(source.subjectLabel.trim());
  // Where "Show …" is a proof; elsewhere it is drawn or set out.
  const proofSubject = /^(?:maths|mathematics|applied[- ]maths|physics|chemistry)$/i.test(source.subjectLabel.trim());
  const multipleChoice = cardRules.some(r => /A, B, C or D/.test(r.display));
  const underlined = /the underlined (?:term|word|phrase)s?\s+(?:is|are)\s+['‘"“]([^'’"”]{1,60})['’"”]/i.exec(stem);
  for (const unit of units) {
    // "Show" proves only in a mathematical subject. In a drawing subject it
    // puts the thing on the drawing; elsewhere it sets it out.
    if (!proofSubject && !dcg && unit.actionKey === 'prove' && /^(?:(?:clearly|also|now)\s+)?show\b/i.test(unit.action?.display ?? '') && !/^that\b/i.test(unit.focus?.display ?? '')) {
      const drawn = /\b(?:sketch|sketches|drawing|drawings|draw|diagram|diagrams|map|maps|graph|grid|axes)\b/i.test(`${stem} ${q}`);
      // "Show and label the following on the map": marked on the figure itself.
      const onFigure = /\bon (?:the|your|this) (?:map|diagram|drawing|sketch|graph|grid|axes|figure|photograph)\b/i.test(`${unit.focus?.display ?? ''} ${unit.conditions.map(c => c.display).join(' ')}`);
      unit.actionKey = onFigure ? 'on-drawing' : drawn ? 'show-drawing' : 'describe';
      unit.means = MEANS[unit.actionKey];
    }
    // In a mathematical subject "Find …" and "Determine …" ask for a value or
    // an expression, whatever the noun: "Find ∫ g(x) dx", "Find where …".
    if (mathsSubject && unit.actionKey === 'identify' && /^(?:hence,?\s+)?(?:find|determine)\b/i.test(unit.action?.display ?? '')
      && !/^(?:the\s+)?(?:name|word|term|type|kind|letter|colour|label)s?\b/i.test(unit.focus?.display ?? '')) {
      unit.actionKey = 'calculate';
      unit.means = MEANS.calculate;
    }
    const dcgVerb = (unit.action?.display ?? '').replace(/^(?:clearly|carefully|neatly|also|now|then|hence)\s+/i, '');
    if (dcg && /^plot\s*$/i.test(dcgVerb)) {
      unit.actionKey = 'construct';
      unit.means = MEANS.construct;
    } else if (dcg && /^show\s*$/i.test(dcgVerb) && unit.focus && !/^(?:that|how|why)\b/i.test(unit.focus.display)) {
      // "Clearly show all points of contact": put it on the drawing.
      unit.actionKey = 'on-drawing';
      unit.means = MEANS['on-drawing'];
    } else if (dcg && /^(?:calculate|prove|identify|draw)$/.test(unit.actionKey) && /^(?:determine|show|find|locate|project|construct|establish)/i.test(dcgVerb)) {
      // In DCG, "Determine" and "Show" mean find it by construction.
      unit.actionKey = 'construct';
      unit.means = MEANS.construct;
    }
    if (underlined && /underlined/i.test(`${unit.action?.display ?? ''} ${unit.focus?.display ?? ''}`)) {
      const at = underlined.index + underlined[0].indexOf(underlined[1]);
      unit.focus = spanOf('stem', stem, at, at + underlined[1].length) ?? unit.focus;
    }
    if (CALC_KEYS.has(unit.actionKey) && !dcg) {
      // "…, where: l : 5x−y−13 = 0 …" / "defined as follows: f(x) = …" — the
      // values printed after the colon are the givens.
      const own = unit.focus ? /:\s*(.+)$/s.exec(q.slice(unit.focus.end, unitEndIn(q, unit))) : null;
      if (own && /=/.test(own[1]) && unit.focus?.from === 'q') {
        const s0 = unit.focus.end + own.index + own[0].length - own[1].length;
        const sp = spanOf('q', q, s0, s0 + own[1].length);
        if (sp && !unit.use.some(u => u.start === sp.start)) unit.use.push({ ...sp, kind: 'given' });
        if (unit.focusMore) {
          unit.focusMore = unit.focusMore.filter(f => !(sp && f.start >= sp.start - 1));
          if (!unit.focusMore.length) delete unit.focusMore;
        }
      }
      const givens = givensFor(unit, contexts);
      for (const g of givens) if (!unit.use.some(u => u.display === g.display)) unit.use.push(g);
      if (!unit.use.some(u => u.kind === 'given')) unit.flags.push('values-on-paper');
    }
    if (unit.use.some(u => u.kind === 'material' && VISUAL.test(u.display)) && !source.figure) unit.flags.push('needs-figure');
    unit.marks = partMarks.get(unit.id) ?? (units.filter(u => !u.jointWith).length === 1 && !unit.jointWith ? totalMarks : null);
    if (unit.actionKey === 'explain-how' && /^how (?:did|does|do|was|were|is|are)\b/i.test(unit.action?.display ?? '') && (unit.marks ?? 99) <= 4) {
      unit.actionKey = 'wh-plain';
      unit.means = MEANS['wh-plain'];
    }
    if (unit.actionKey === 'wh-plain') {
      // A high tariff alone does not make "What do the following letters
      // stand for?" a developed answer; a question about a role, an impact or
      // the evidence does.
      const developed = /^(?:what|which|in what)\s+(?:role|roles|impact|impacts|effect|effects|evidence|contribution|influence|importance|significance|problems|challenges|changes|factors|reasons|methods|arguments|lessons|message|messages|view|views|attitude|attitudes|techniques|ways|features|qualities|themes?)\b/i
        .test(`${unit.action?.display ?? ''} ${unit.focus?.display ?? ''}`)
        // "What do the other immortals think of …?" asks for views, developed.
        || /\b(?:think|believe|feel|consider)\b/i.test(unit.focus?.display ?? '');
      if (multipleChoice) unit.means = MEANS.choice;
      else if ((unit.marks ?? 0) >= 10 && developed) unit.means = MEANS['wh-developed'];
    }
  }

  for (const unit of units) {
    // "for each of the following" is the head of a list, and "Hence or
    // otherwise" is a permission; neither is a limit.
    unit.conditions = unit.conditions.filter(c => !/^(?:for|in) each(?: of the following| case)?$|^hence(?:,)? or otherwise,?$/i.test(c.display));
  }
  // Nothing could be read: the printed question is the honest view.
  if (units.every(u => u.flags.includes('as-printed'))) return { ...base, reasons: ['command-missing'], cardRules };
  const setting = settingOf(q, contexts, units, cardRules);
  return { mode: 'decomposed', reasons: [], banner, cardRules, ...(setting.length ? { setting } : {}), units, totalMarks };
}

// ---------------------------------------------------------------------------
// Exam-language questions.
// ---------------------------------------------------------------------------

const escapeRe = (text: string) => text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
const examMatchers = new Map<ExamLexicon, { commands: RegExp; count: RegExp; conditions: RegExp | null; details: RegExp | null; bySurface: Map<string, ExamLexicon['commands'][number]> }>();
function examMatcher(lex: ExamLexicon) {
  const cached = examMatchers.get(lex);
  if (cached) return cached;
  const alt = (surfaces: string[]) => surfaces.filter(Boolean).sort((a, b) => b.length - a.length).map(x => escapeRe(x).replace(/['’]/g, '[\'’]').replace(/\s+/g, '\\s+')).join('|');
  const edge = (body: string) => new RegExp(`(?<![\\p{L}\\p{N}])(?:${body})(?![\\p{L}\\p{N}])`, 'giu');
  const made = {
    commands: edge(alt(lex.commands.map(c => c.surface))),
    // A number word or digit within the first words after the command, then its noun.
    count: new RegExp(`^\\s*(?:[\\p{L}’']+\\s+){0,2}?(${[alt(Object.keys(lex.counts)), '\\d{1,2}'].filter(Boolean).join('|')})(?![\\p{L}\\p{N}])\\s+([\\p{L}’'-]{3,})`, 'iu'),
    conditions: lex.conditions.length ? edge(alt(lex.conditions.map(c => c.surface))) : null,
    details: lex.details.length ? edge(alt(lex.details.map(d => d.surface))) : null,
    bySurface: new Map(lex.commands.map(c => [c.surface.toLowerCase().replace(/’/g, "'").replace(/\s+/g, ' '), c])),
  };
  examMatchers.set(lex, made);
  return made;
}
const norm = (t: string) => t.toLowerCase().replace(/’/g, "'").replace(/\s+/g, ' ');

/** A locator printed at the end of a sentence: "(Section 1)", "(3 dalis)", "(párrafo 6)". */
function trailingLocator(raw: string, start: number, end: number, lex: ExamLexicon): { at: number; span: KPSpan | null } {
  const text = raw.slice(start, end);
  const m = /\(([^()]{1,40})\)\s*[.?!;:]?\s*$/u.exec(text);
  if (!m) return { at: end, span: null };
  const inner = m[1];
  const words = lex.locatorWords.map(w => escapeRe(w)).join('|');
  const isLocator = /\d/.test(inner) && (!words || new RegExp(`(?:${words})|^\\s*[\\d\\s,–-]+\\s*$|§|lines?|par`, 'iu').test(inner) || /^\s*[\d\s,–-]+\s*$/.test(inner));
  if (!isLocator) return { at: end, span: null };
  const at = start + m.index;
  return { at, span: spanOf('q', raw, at + 1, at + 1 + inner.length) };
}

function examUnitsIn(raw: string, start: number, end: number, lex: ExamLexicon, part: Part, nextId: () => string): { units: KPUnit[]; setting: KPSpan[] } {
  const mx = examMatcher(lex);
  const units: KPUnit[] = [];
  const setting: KPSpan[] = [];
  // Printed options after the question: "A. Od dawna B. Od miesiąca …".
  const opts = /(?:^|\s)(?:A[.)]|\(A\)|a\)|\(a\))\s+\S[^]*?(?:\s)(?:B[.)]|\(B\)|b\)|\(b\))\s+\S/u.exec(raw.slice(start, end));
  const bodyEnd = opts && opts.index > 3 ? start + opts.index : end;
  // "…? (Section 4)": a locator printed after the question mark ends that
  // question, not a sentence of its own.
  const pieces: Piece[] = [];
  for (const p of sentences(raw, start, bodyEnd)) {
    const prev = pieces[pieces.length - 1];
    if (prev && /^\s*\([^()]{1,40}\)\s*[.:;]?\s*$/.test(raw.slice(p.start, p.end)) && /\d/.test(raw.slice(p.start, p.end))) prev.end = p.end;
    else pieces.push({ ...p });
  }
  const limitLead = (before: string) => lex.conditions.some(c => norm(before).replace(/[,:]$/, '').trim() === norm(c.surface));
  const MARKS_TAIL = /\s*[([]\s*\d+\s*(?:marc|mharc|marks?|pts?|points?|punkt\w*|puntos?|pontos?|bod\w*|pisteet?|poäng|point)\s*[)\]]\s*[.]?\s*$/iu;
  for (const piece of pieces) {
    // "Setzen Sie die fehlenden Konjunktionen … ein. Lena setzt sich …": once a
    // gap-fill or rewrite instruction is given, what follows is its passage.
    const filler = units.find(u => /^(?:fill-gap|complete|rewrite|translate|match)$/.test(u.actionKey));
    if (filler) {
      const sp = spanOf('q', raw, piece.start, end);
      if (sp && !filler.item) filler.item = sp;
      break;
    }
    let s0 = piece.start;
    const marks = MARKS_TAIL.exec(raw.slice(s0, piece.end));
    if (marks) piece.end = s0 + marks.index;
    if (piece.end <= s0) continue;
    const label = /^\s*(?:\((?:[a-h]|i{1,3}|iv|vi{0,3}|ix|x)\)|\d{1,2}[.)])\s+/u.exec(raw.slice(s0, piece.end));
    if (label) s0 += label[0].length;
    const text = raw.slice(s0, piece.end);
    if (!text.trim()) continue;
    // "Geben Sie Details." after a question: how the answer must be given.
    if (mx.details) mx.details.lastIndex = 0;
    const det = mx.details ? mx.details.exec(text) : null;
    if (det && units.length && !text.slice(0, det.index).trim() && text.slice(det.index + det[0].length).replace(/\([^)]*\)/g, '').replace(/[.!?\s]/g, '').length === 0) {
      const loc = trailingLocator(raw, s0, piece.end, lex);
      const sp = spanOf('q', raw, s0 + det.index, s0 + det.index + det[0].length);
      const last = units[units.length - 1];
      if (sp) last.conditions.push(sp);
      if (loc.span && !last.use.some(u => u.display === loc.span!.display)) last.use.push({ ...loc.span, kind: 'locator' });
      continue;
    }
    mx.commands.lastIndex = 0;
    let hit: { index: number; length: number; cmd: ExamLexicon['commands'][number] } | null = null;
    const asks = /[?？]\s*(?:\([^)]*\))?\s*[.]?\s*$/.test(text);
    for (const m of text.matchAll(mx.commands)) {
      const cmd = mx.bySurface.get(norm(m[0]));
      if (!cmd) continue;
      const before = text.slice(0, m.index).trim();
      const leadOk = !before || /[,:;»”"’)]$/.test(before) || (before.split(/\s+/).length <= 1 && /^[\p{Lu}¿¡]/u.test(before)) || limitLead(before);
      if (cmd.position === 'start' ? leadOk : (leadOk || asks)) { hit = { index: m.index!, length: m[0].length, cmd }; break; }
    }
    if (!hit) {
      const sp = spanOf('q', raw, s0, piece.end);
      const last = units[units.length - 1];
      // A line after an instruction that has no instruction of its own is
      // what the instruction is applied to: "املأ كل فراغ …: (ه) لن… إلى أمريكا."
      if (sp && last && !last.item && !last.focus?.display.includes(sp.display) && /[:：]\s*$/.test(raw.slice(last.action!.end, s0))) {
        last.item = sp;
        continue;
      }
      if (sp && sp.display.split(/\s+/).length >= 3 && !/^\(?[^()]{0,30}\)?$/.test(sp.display.replace(/\(\s*\d+\s*\w*\s*\)/g, '').trim() || '()')) setting.push(sp);
      continue;
    }
    const aStart = s0 + hit.index;
    const aEnd = aStart + hit.length;
    const unit: KPUnit = {
      id: nextId(), ref: part.ref, altGroup: part.altGroup,
      action: spanOf('q', raw, aStart, aEnd), actionKey: hit.cmd.key, means: MEANS[hit.cmd.key] ?? '', english: hit.cmd.english,
      count: null, focus: null, conditions: [], use: [], marks: null, flags: [],
    };
    // A lead phrase before the command ("Riferendovi alla seconda sezione,")
    // says where or how: a limit. A quotation is what the question is about;
    // a lone preposition belongs to the question word ("За каква …").
    const lead = spanOf('q', raw, s0, aStart);
    if (lead && /^[„“"«‘'‚].*[”"»’'“]\.?$/u.test(lead.display)) unit.use.push({ ...lead, kind: 'material' });
    else if (lead && lead.display.length <= 4 && !/\s/.test(lead.display)) unit.action = spanOf('q', raw, s0, aEnd);
    else if (lead) unit.conditions.push(lead);
    const loc = trailingLocator(raw, aEnd, piece.end, lex);
    if (loc.span) unit.use.push({ ...loc.span, kind: 'locator' });
    let cur = aEnd;
    // How many: a printed number word or digit straight after the command.
    const cm = mx.count.exec(raw.slice(cur, loc.at));
    if (cm) {
      const cStart = cur + cm[0].lastIndexOf(cm[1], cm[0].length - cm[2].length);
      const cEnd = cur + cm[0].length;
      const sp = spanOf('q', raw, cStart, cEnd);
      const value = lex.counts[norm(cm[1])] ?? (Number(cm[1]) || undefined);
      if (sp && value) {
        unit.count = sp;
        unit.countValue = value;
        unit.countNoun = cm[2].toLowerCase();
        cur = cStart;
      }
    }
    // Limits the lexicon knows: "in your own words", "according to the text".
    if (mx.conditions) mx.conditions.lastIndex = 0;
    const limits = mx.conditions ? [...raw.slice(cur, loc.at).matchAll(mx.conditions)] : [];
    let focusEnd = loc.at;
    for (const m of limits) {
      const at = cur + m.index!;
      const sp = spanOf('q', raw, at, at + m[0].length);
      if (!sp) continue;
      unit.conditions.push(sp);
      // A limit at the end of the sentence ends what it is about.
      if (!raw.slice(at + m[0].length, loc.at).replace(/[\s.?!,;:]/g, '')) focusEnd = Math.min(focusEnd, at);
    }
    // "Opišite, na temelju teksta, ali svojim riječima, kako …": limits that
    // open the object are shown as limits, and what it is about starts after.
    for (let moved = true; moved;) {
      moved = false;
      const lead = /^[\s,]*/.exec(raw.slice(cur, focusEnd))![0].length;
      const hitLimit = unit.conditions.find(c => c.from === 'q' && c.start === cur + lead);
      if (hitLimit) { cur = hitLimit.end; moved = true; while (cur < focusEnd && /[\s,;:]/.test(raw[cur])) cur += 1; if (/^(?:ali|mais|aber|pero|ma|men|maar|ale|bet|de|a)\s/i.test(raw.slice(cur, cur + 6))) cur = cur + raw.slice(cur).indexOf(' ') + 1; }
    }
    // "… w tekście? przepisanie" — a word printed after the question mark is
    // the item it asks about; the question ends at its own full stop.
    const qmark = /[?？]\s*(?=\S)/u.exec(raw.slice(cur, focusEnd));
    if (qmark) {
      const item = spanOf('q', raw, cur + qmark.index + qmark[0].length, focusEnd);
      if (item && item.display.split(/\s+/).length <= 6) { unit.item = item; focusEnd = cur + qmark.index; }
    }
    const stop = /[.!](?=\s+[„“"«‘\p{Lu}])/u.exec(raw.slice(cur, focusEnd));
    if (stop && stop.index > 0) focusEnd = cur + stop.index;
    // "Förklara dessa ord såsom de används i texten. ansåg (anse)": the
    // printed word after the instruction's full stop is its item.
    const tailItem = /\.\s+([^.?!]{1,60})$/u.exec(raw.slice(cur, focusEnd));
    if (tailItem && !unit.item && tailItem[1].trim().split(/\s+/).length <= 6) {
      const item = spanOf('q', raw, focusEnd - tailItem[1].length, focusEnd);
      if (item) { unit.item = item; focusEnd = cur + tailItem.index; }
    }
    // "…: kolidować z czymś" — the printed item after a colon.
    const colon = raw.slice(cur, focusEnd).indexOf(':');
    if (colon >= 0 && raw.slice(cur + colon + 1, focusEnd).trim()) {
      const item = spanOf('q', raw, cur + colon + 1, focusEnd);
      if (item) unit.item = item;
      focusEnd = cur + colon;
    }
    // About starts at the counted noun: "2 informacje dotyczące …" → "informacje dotyczące …".
    const nounAt = unit.count ? unit.count.end - (unit.countNoun?.length ?? 0) : cur;
    const focus = spanOf('q', raw, unit.count ? Math.max(cur, nounAt) : cur, focusEnd);
    if (focus) unit.focus = focus;
    units.push(unit);
  }
  if (opts && units.length) {
    const sp = spanOf('q', raw, bodyEnd, end);
    if (sp) units[units.length - 1].use.push({ ...sp, kind: 'options' });
  }
  return { units, setting };
}

function buildExamLanguage(source: WaysInQuestionSource, lex: ExamLexicon, base: KeyPartsBreakdown, cardRules: KPSpan[]): KeyPartsBreakdown | null {
  const q = source.questionText ?? '';
  const stem = source.stem ?? '';
  let n = 0;
  const nextId = () => `${source.id}#${++n}`;
  const units: KPUnit[] = [];
  const setting: KPSpan[] = [];
  for (const alt of splitAlternatives(q)) {
    for (const part of splitParts(q, alt.start, alt.end, alt.altGroup)) {
      const r = examUnitsIn(q, part.start, part.end, lex, part, nextId);
      units.push(...r.units);
      setting.push(...r.setting);
    }
  }
  if (!units.length && stem.trim()) {
    // The instruction is in the stem ("Busca en el texto una palabra … que:")
    // and the question is the printed item ("dejar (para 3)").
    const r = examUnitsIn(stem, 0, stem.length, lex, { start: 0, end: stem.length, ref: '' }, nextId);
    const lead = r.units[r.units.length - 1];
    if (lead) {
      lead.action = lead.action && { ...lead.action, from: 'stem' };
      if (lead.count) lead.count = { ...lead.count, from: 'stem' };
      if (lead.focus) lead.focus = { ...lead.focus, from: 'stem' };
      lead.conditions = lead.conditions.map(c => ({ ...c, from: 'stem' as const }));
      lead.use = lead.use.map(u => ({ ...u, from: 'stem' as const }));
      const loc = trailingLocator(q, 0, q.length, lex);
      const item = spanOf('q', q, 0, loc.at);
      if (item) lead.item = item;
      if (loc.span) lead.use.push({ ...loc.span, kind: 'locator' });
      units.push(lead);
      setting.splice(0, setting.length);
    }
  }
  if (!units.length) return null;
  for (const u of units) u.marks = units.length === 1 ? base.totalMarks : null;
  return { ...base, mode: 'glossed', reasons: ['non-english'], cardRules, ...(setting.length ? { setting } : {}), units };
}

/**
 * What the question tells the student before it asks: its printed statements
 * that no slot shows. A role ("Imagine you are the historian Thucydides."), an
 * audience ("You are asked to address a group of farmers …") or the fact a
 * question builds on is part of the task, so it is shown, never dropped.
 */
function settingOf(q: string, contexts: Array<{ from: 'q' | 'stem'; raw: string; pieces: Piece[] }>, units: KPUnit[], cardRules: KPSpan[]): KPSpan[] {
  const covered: Array<[number, number]> = [];
  const cover = (sp: KPSpan | null | undefined) => { if (sp && sp.from === 'q') covered.push([sp.start, sp.end]); };
  for (const u of units) {
    cover(u.action); cover(u.count); cover(u.focus); cover(u.item);
    for (const x of [...(u.focusMore ?? []), ...u.conditions, ...u.use, ...(u.headings ?? []), ...(u.sides ?? [])]) cover(x);
  }
  for (const r of cardRules) cover(r);
  const out: KPSpan[] = [];
  for (const ctx of contexts) {
    if (ctx.from !== 'q') continue;
    for (const piece of ctx.pieces) {
      // Shown already when a slot holds most of it; "In TEXT 2, the writer
      // suggests …" is still set-up when only "TEXT 2" is in USE.
      let inSlots = 0;
      for (let i = piece.start; i < piece.end; i += 1) if (covered.some(([s, e]) => i >= s && i < e)) inSlots += 1;
      if (inSlots > (piece.end - piece.start) * 0.4) continue;
      const sp = spanOf('q', q, piece.start, piece.end);
      if (!sp || out.some(o => o.start === sp.start)) continue;
      const words = sp.display.split(/\s+/);
      const letters = (sp.display.match(/\p{L}/gu) ?? []).length;
      // A sentence, not a flattened table, an axis label or a rubric line.
      if (words.length < 4 || letters < sp.display.length * 0.6 || !/^[\p{Lu}“‘"'(]/u.test(sp.display)) continue;
      if (!/[.?!:)”’"']\s*$/.test(q.slice(piece.start, piece.end).trim()) && words.length < 8) continue;
      if (RUBRIC.test(sp.display) || /^(?:Page \d|Question \d|\[?\d+ marks?\]?$|Answer\b)/i.test(sp.display)) continue;
      // A flattened table ("Oil/Gas exploitation Quarrying Mining …") is not a
      // sentence the question tells you; a sentence has its small words.
      if ((sp.display.match(/\b(?:is|are|was|were|has|have|had|will|would|can|could|the|a|an|to|of|in|on|for|with|by|and|that|this|you|your)\b/gi) ?? []).length < 2) continue;
      out.push(sp);
    }
  }
  return out.sort((a, b) => a.start - b.start);
}

/** Where a unit's own printed text ends: the end of the sentence it is in. */
function unitEndIn(q: string, unit: KPUnit): number {
  const from = unit.focus?.end ?? unit.action?.end ?? 0;
  const stop = /[.?!](?=\s+\p{Lu}|\s*$)/u.exec(q.slice(from));
  return stop ? from + stop.index : q.length;
}

// ---------------------------------------------------------------------------
// Plan rows derived from the breakdown.
// ---------------------------------------------------------------------------

export interface KeyPartPlanRow {
  id: string;
  unitId: string;
  /** Short neutral label: "Reason 2", "(ii) Name", "Side A". */
  label: string;
  /** The unit's key parts in one line, all lifted from the question. */
  summary: string;
  placeholder: string;
}

const cap = (s: string) => s.charAt(0).toUpperCase() + s.slice(1);

export function keyPartSummary(unit: KPUnit): string {
  if (unit.flags.includes('as-printed')) return '';
  const aboutRaw = unit.focus ? [unit.focus.display, ...(unit.focusMore ?? []).map(f => f.display)].join(' … ') : '';
  // "the following" says nothing once the options are listed.
  const about = /^the following(?:\s+[\p{L}-]+)?$/iu.test(aboutRaw) && unit.use.some(u => u.kind === 'options') ? '' : aboutRaw;
  // "two pyroclastic materials" · "pyroclastic materials that are …": the
  // noun is said once in a one-line summary.
  const countNoun = unit.count?.display.replace(/^(?:any|at least)?\s*\S+\s*/i, '') ?? '';
  const repeats = countNoun && about.toLowerCase().startsWith(countNoun.toLowerCase());
  const bits = [
    repeats ? undefined : unit.count?.display,
    about,
    ...unit.conditions.map(c => c.display),
  ].filter(Boolean) as string[];
  return bits.join(' · ');
}

/** A label short enough for a planning row, cut at a word. */
const clip = (s: string, n = 60) => {
  if (s.length <= n) return s;
  const cut = s.lastIndexOf(' ', n - 1);
  return `${s.slice(0, cut > 20 ? cut : n - 1)}…`;
};

export function planRowsFromKeyParts(kp: KeyPartsBreakdown): KeyPartPlanRow[] {
  if (kp.mode !== 'decomposed' && !(kp.mode === 'glossed' && kp.units.some(u => u.focus || u.item || u.count))) return [];
  const rows: KeyPartPlanRow[] = [];
  for (const unit of kp.units) {
    if (unit.jointWith) continue; // drawn together with its partner
    // "Illustrate your answer" is drawn into the answer before it. "Justify
    // your answer" is a marked job of its own, so it keeps its own space.
    if (unit.actionKey === 'illustrate-tail' && rows.length) {
      rows[rows.length - 1].placeholder = 'Your answer, with sketches';
      continue;
    }
    const partner = kp.units.find(u => u.id !== unit.id && u.jointWith === unit.id);
    const verb = [partner?.action?.display, unit.action?.display].filter(Boolean).join(' and ');
    const ref = unit.ref ? `${unit.ref} ` : '';
    // "Name … methods … and give one example of a plant …": one space holds
    // both jobs, so it names both objects.
    const partnerFocus = partner?.focus && unit.focus && partner.focus.display !== unit.focus.display ? partner.focus.display : '';
    const summary = [partnerFocus, keyPartSummary(unit)].filter(Boolean).join(' · ');
    if (unit.flags.includes('as-printed')) {
      rows.push({ id: `${unit.id}-1`, unitId: unit.id, label: `${ref}${clip(unit.focus?.display ?? 'This part', 50)}`, summary, placeholder: 'Your response to this part' });
      continue;
    }
    if (unit.sides) {
      rows.push({ id: `${unit.id}-a`, unitId: unit.id, label: cap(unit.sides[0].display), summary, placeholder: 'This side' });
      rows.push({ id: `${unit.id}-b`, unitId: unit.id, label: cap(unit.sides[1].display), summary, placeholder: 'The other side' });
      continue;
    }
    const n = unit.countValue && unit.countValue > 1 ? Math.min(unit.countValue, 6) : 1;
    const noun = unit.countNoun ?? 'point';
    if (unit.item) {
      // One row per printed item: "Commission", "(i) Design of products".
      const itemLabel = `${ref}${cap(clip(unit.item.display))}`;
      for (let i = 1; i <= n; i += 1) {
        rows.push({
          id: `${unit.id}-${i}`, unitId: unit.id,
          label: n > 1 ? `${itemLabel} · ${cap(noun)} ${i}` : itemLabel,
          summary, placeholder: n > 1 ? `Your ${ordinal(i)} ${noun}` : 'Your response to this item',
        });
      }
      continue;
    }
    if (n === 1 && unit.headings && unit.headings.length >= 2) {
      // "Refer in your answer to space, function, layout and lighting".
      // The heading list is the rows; each row's summary leaves it out.
      // A paired count ("one advantage and one disadvantage") is the headings
      // themselves, so the rows leave it out too.
      const pairCounted = unit.count && unit.headings.every(h => unit.count!.display.includes(h.display));
      const headingSummary = keyPartSummary({ ...unit, count: pairCounted ? null : unit.count, conditions: unit.conditions.filter(c => !unit.headings!.every(h => c.display.includes(h.display))) });
      for (const [i, h] of unit.headings.entries()) {
        rows.push({ id: `${unit.id}-h${i + 1}`, unitId: unit.id, label: `${ref}${cap(h.display)}`, summary: headingSummary, placeholder: `Your point on ${h.display}` });
      }
      continue;
    }
    // "Detail 1", "Detail 2": the label already says how many.
    const countedSummary = n > 1 ? [partnerFocus, keyPartSummary({ ...unit, count: null })].filter(Boolean).join(' · ') : summary;
    for (let i = 1; i <= n; i += 1) {
      rows.push({
        id: `${unit.id}-${i}`, unitId: unit.id,
        label: n > 1 ? `${ref}${cap(noun)} ${i}` : `${ref}${cap(clip(verb || 'Answer'))}`,
        summary: countedSummary,
        placeholder: n > 1 ? `Your ${ordinal(i)} ${noun}` : 'Your response to this part',
      });
    }
  }
  return rows.slice(0, 8);
}

const ordinal = (i: number) => ['first', 'second', 'third', 'fourth', 'fifth', 'sixth'][i - 1] ?? `${i}th`;

/**
 * The Plan stage's rows. The breakdown decides the rows, with one exception:
 * a single-part question whose printed wording already fixes a count the
 * breakdown does not see ("Name the parts labelled A and B") keeps the
 * printed-count rows, now captioned with the key parts instead of the
 * sentence. Losing a printed count would take a space away from the student.
 */
export function planRowsFor(
  kp: KeyPartsBreakdown,
  printed: { basis: 'printed' | 'flexible'; prompts: Array<{ id: string; label: string; placeholder: string }> },
): KeyPartPlanRow[] {
  const rows = planRowsFromKeyParts(kp);
  if (
    kp.mode === 'decomposed' && kp.units.length === 1 && printed.basis === 'printed'
    && printed.prompts.length > rows.length
    // The breakdown already knows how many: a count, printed items or headings.
    && !kp.units[0].countValue && !kp.units[0].item && !kp.units[0].headings
    // Rows the old planner made by splitting sentences ("Task 2: Give") are
    // what the breakdown replaces; only a printed count is kept.
    && !printed.prompts.some(p => /^Task \d+:/.test(p.label))
    // "the synapse, where two neurons come into close contact": a number in
    // a description is not a count of answers.
    && !/\b(?:where|that|which|who|whom|when|while|if|between|connects?)\b[^.?!]*\b(?:two|three|four|five|six|[2-6])\b/i.test([kp.units[0].focus?.display, ...kp.units[0].conditions.map(c => c.display)].join(' '))
  ) {
    const unit = kp.units[0];
    const summary = keyPartSummary(unit);
    return printed.prompts.slice(0, 8).map(p => ({
      id: p.id, unitId: unit.id, label: p.label, summary, placeholder: p.placeholder,
    }));
  }
  return rows;
}
