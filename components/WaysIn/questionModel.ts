import { COMMAND_WORDS } from '../../data/knowledge/commandWords';
import type {
  CommandDemand,
  QuestionHighlight,
  WaysInPlanKind,
  WaysInPlanPrompt,
  WaysInQuestionModel,
  WaysInQuestionSource,
} from './types';

const escapeRe = (value: string) => value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

const EXTRA_COMMANDS: CommandDemand[] = [
  {
    surface: 'what is meant by',
    requiredAction: 'Give the precise meaning of the term or idea named.',
    answerShape: 'The named term is … followed by the essential defining feature or features.',
    commonTrap: 'Giving an example of the term without stating what it means.',
  },
  {
    surface: 'what does',
    requiredAction: 'Supply the direct meaning, expansion or effect requested.',
    answerShape: 'A short direct response that completes the exact “what does …?” prompt.',
    commonTrap: 'Writing around the topic without supplying the requested meaning or expansion.',
  },
  {
    surface: 'what term',
    requiredAction: 'Name the precise term that matches the description in the question.',
    answerShape: 'One exact term for each description supplied.',
    commonTrap: 'Explaining the idea without naming the term itself.',
  },
  {
    surface: 'how does',
    requiredAction: 'Trace the change, effect or mechanism asked about.',
    answerShape: 'Starting condition → relevant change or mechanism → resulting condition.',
    commonTrap: 'Stating only the final effect without showing how it happens.',
  },
  {
    surface: 'how can',
    requiredAction: 'State a valid method or route by which the requested result can happen.',
    answerShape: 'Method or action → short link to the requested result, where needed.',
    commonTrap: 'Saying that it can happen without naming the method.',
  },
  {
    surface: 'where does',
    requiredAction: 'Name the location in which the process or event occurs.',
    answerShape: 'One precise location, with further detail only if the question asks for it.',
    commonTrap: 'Naming a broad system when the question expects a specific structure or place.',
  },
  {
    surface: 'where would',
    requiredAction: 'Place or rank the item in the location, category or scale requested.',
    answerShape: 'A clear position or rank using the labels supplied by the question.',
    commonTrap: 'Discussing the item without committing to its requested position.',
  },
  {
    surface: 'to which',
    requiredAction: 'Identify the category, group or destination that the named item belongs to.',
    answerShape: 'The precise category or group name.',
    commonTrap: 'Describing the item without naming the category requested.',
  },
  {
    surface: 'what is',
    requiredAction: 'Give the direct definition, identity, value or function requested.',
    answerShape: 'A precise response to the noun phrase that follows “what is”.',
    commonTrap: 'Giving related information without answering the exact noun phrase.',
  },
  {
    surface: 'what could',
    requiredAction: 'Name a plausible item or action that satisfies the condition given.',
    answerShape: 'One clear possibility, supported only if the question asks why.',
    commonTrap: 'Giving a broad topic rather than a usable example or action.',
  },
  {
    surface: 'what distinguishes',
    requiredAction: 'State the feature or features that make the named things different.',
    answerShape: 'A is … whereas the other type is …',
    commonTrap: 'Describing the topic without making the requested difference explicit.',
  },
  {
    surface: 'which',
    requiredAction: 'Choose the item or items that satisfy the condition in the question.',
    answerShape: 'A clear selection using the names, numbers or labels supplied.',
    commonTrap: 'Listing several possibilities when the wording asks for a definite choice.',
  },
  {
    surface: 'where',
    requiredAction: 'Name the location, source or position requested.',
    answerShape: 'One precise place or position.',
    commonTrap: 'Giving a process when the question asks for a location.',
  },
  {
    surface: 'what',
    requiredAction: 'Supply the exact thing, meaning, value or feature requested.',
    answerShape: 'A direct response to the wording after “what”.',
    commonTrap: 'Writing relevant background without supplying the requested item.',
  },
  {
    surface: 'write',
    requiredAction: 'Record the requested word, formula, value or expression in the required form.',
    answerShape: 'The requested item itself, with working or units only where the question requires them.',
    commonTrap: 'Explaining the item while failing to write it in the requested notation or form.',
  },
  {
    surface: 'choose',
    requiredAction: 'Select the option or options that meet the condition in the question.',
    answerShape: 'A clear choice using the labels or boxes supplied.',
    commonTrap: 'Leaving more than the permitted number of options selected.',
  },
  {
    surface: 'account for',
    requiredAction: 'Explain the reason for the result, pattern or difference named in the question.',
    answerShape: 'Observed result or difference → relevant cause → link showing how the cause produces it.',
    commonTrap: 'Repeating the difference without explaining why it occurs.',
  },
  {
    surface: 'how would',
    requiredAction: 'Set out the method, change or effect requested by the question.',
    answerShape: 'Direct response → the steps or causal link that make it happen.',
    commonTrap: 'Naming the topic without answering the specific “how” in the question.',
  },
  {
    surface: 'advise',
    requiredAction: 'Recommend an appropriate course of action for the person or situation given.',
    answerShape: 'Clear recommendation → relevant reason or consequence, when the question asks for support.',
    commonTrap: 'Giving general information without making a usable recommendation for this situation.',
  },
  {
    surface: 'construct',
    requiredAction: 'Build the requested argument, plan or response from the evidence and knowledge named.',
    answerShape: 'Required position or goal → distinct supporting steps or reasons → clear finish.',
    commonTrap: 'Listing facts without organising them into the argument or plan requested.',
  },
  {
    surface: 'comment',
    requiredAction: 'Make a concise evidence-based observation or judgement about what is shown.',
    answerShape: 'Observation or judgement → evidence from the supplied material.',
    commonTrap: 'Describing every detail without stating what the evidence means overall.',
  },
  {
    surface: 'provide',
    requiredAction: 'Supply the exact items, examples or recommendations requested.',
    answerShape: 'One distinct requested item per line, with support only where asked.',
    commonTrap: 'Giving relevant background but not the requested items themselves.',
  },
  {
    surface: 'complete',
    requiredAction: 'Fill the missing parts of the table, graph, sentence or sequence supplied.',
    answerShape: 'Work through each blank or unfinished part in its printed order.',
    commonTrap: 'Answering only the first blank or overlooking labels, units or headings already supplied.',
  },
  {
    surface: 'estimate',
    requiredAction: 'Work out a reasonable approximate value from the information supplied.',
    answerShape: 'Relevant values → sensible approximation method → result with units.',
    commonTrap: 'Giving an unjustified guess or presenting false precision.',
  },
  {
    surface: 'predict',
    requiredAction: 'State the outcome you expect from the pattern, evidence or knowledge given.',
    answerShape: 'Expected outcome → reason, when requested.',
    commonTrap: 'Describing the present data without stating what is expected next.',
  },
  {
    surface: 'assist',
    requiredAction: 'Carry out the ordering, matching or decision described for the named person.',
    answerShape: 'Follow the supplied format and give one unambiguous placement or choice for each item.',
    commonTrap: 'Explaining the topic while leaving the requested ordering or matching unfinished.',
  },
  {
    surface: 'plot',
    requiredAction: 'Place the supplied data accurately on the requested graph.',
    answerShape: 'Suitable axes and scale → plotted data → labels, units and joining convention where required.',
    commonTrap: 'Plotting the values but omitting an axis label, unit or workable scale.',
  },
  {
    surface: 'indicate',
    requiredAction: 'Show the required choice, status or position in the format supplied.',
    answerShape: 'One clear tick, term, label or selection for each item.',
    commonTrap: 'Adding an explanation while leaving the required selection ambiguous.',
  },
  {
    surface: 'place',
    requiredAction: 'Put each item, label or step into the correct position or order.',
    answerShape: 'Follow the printed layout and make one clear placement for each item.',
    commonTrap: 'Knowing the items but not recording their order or location unambiguously.',
  },
  {
    surface: 'match',
    requiredAction: 'Pair each item with the corresponding option supplied.',
    answerShape: 'One unambiguous pair for each item, using the paper’s labels or letters.',
    commonTrap: 'Using an option twice when the paper expects one-to-one matching.',
  },
  {
    surface: 'select',
    requiredAction: 'Choose the option or options that satisfy the condition in the question.',
    answerShape: 'A clear selection using the paper’s own labels, followed by support only if requested.',
    commonTrap: 'Listing every plausible option instead of committing to the number requested.',
  },
  {
    surface: 'calculate',
    requiredAction: 'Use the supplied information and show a route to a numerical result.',
    answerShape: 'Formula or rule → substitution → working → answer with units.',
    commonTrap: 'Writing only the final number makes it impossible to recover method marks.',
  },
  {
    surface: 'determine',
    requiredAction: 'Work out the requested result from the information given.',
    answerShape: 'Choose a method → show the working → state the result clearly.',
    commonTrap: 'Giving a result without showing how the supplied information led to it.',
  },
  {
    surface: 'distinguish',
    requiredAction: 'State a clear difference between the named things.',
    answerShape: 'A is … whereas B is …',
    commonTrap: 'Defining each item separately without making the difference explicit.',
  },
  {
    surface: 'suggest',
    requiredAction: 'Offer a plausible answer that fits the evidence or context supplied.',
    answerShape: 'Suggestion + a short link to the evidence, when the question asks for one.',
    commonTrap: 'Giving a memorised fact that does not fit the situation in the question.',
  },
  {
    surface: 'list',
    requiredAction: 'Give the requested items briefly, without adding an explanation unless asked.',
    answerShape: 'One distinct item per line.',
    commonTrap: 'Repeating the same idea in different words and counting it twice.',
  },
  {
    surface: 'give',
    requiredAction: 'Supply exactly the information requested.',
    answerShape: 'A direct answer in the shortest form that fully answers the prompt.',
    commonTrap: 'Adding unrelated detail while missing one of the requested pieces.',
  },
  {
    surface: 'label',
    requiredAction: 'Attach the correct term to each indicated part of the figure.',
    answerShape: 'One precise label for each letter, arrow or numbered part.',
    commonTrap: 'Using a broad structure name when the arrow points to a specific part.',
  },
  {
    surface: 'draw',
    requiredAction: 'Produce the requested diagram, graph or construction with its required conventions.',
    answerShape: 'Shape or axes → accurate features → labels, units or scale where requested.',
    commonTrap: 'Producing a recognisable picture but omitting the labels or conventions that carry marks.',
  },
  {
    surface: 'sketch',
    requiredAction: 'Show the important shape, trend or structure without unnecessary fine detail.',
    answerShape: 'Essential form → key features → labels or axes where relevant.',
    commonTrap: 'Adding detail while missing the overall trend or defining feature.',
  },
];

const ADDITIONAL_COMMAND_GROUPS: Array<{
  surfaces: string[];
  requiredAction: string;
  answerShape: string;
  commonTrap: string;
}> = [
  {
    surfaces: ['how'],
    requiredAction: 'Answer the exact method, amount, change, difference or sequence asked for.',
    answerShape: 'Direct response to the “how” prompt → working, steps or a link where the wording calls for it.',
    commonTrap: 'Writing generally about the topic without answering the particular “how” relationship.',
  },
  {
    surfaces: ['why'],
    requiredAction: 'Give the cause or reason that produces the result named in the question.',
    answerShape: 'Relevant cause or reason → clear link to the result in the question.',
    commonTrap: 'Repeating what happened without giving the reason it happened.',
  },
  {
    surfaces: ['in which', 'through which', 'to which', 'under what'],
    requiredAction: 'Select the precise place, category, route or condition requested.',
    answerShape: 'One direct selection using the paper’s names, labels or conditions.',
    commonTrap: 'Describing the topic without making the requested selection.',
  },
  {
    surfaces: ['illustrate'],
    requiredAction: 'Make the idea clear with the example, diagram or application requested.',
    answerShape: 'Named idea → relevant example or diagram → short link showing how it illustrates the idea.',
    commonTrap: 'Giving an example without showing how it connects to the named idea.',
  },
  {
    surfaces: ['use'],
    requiredAction: 'Apply the source, relationship, equation or method named in the question.',
    answerShape: 'Relevant supplied material → application or working → requested result.',
    commonTrap: 'Giving a result without visibly using the material the question specifies.',
  },
  {
    surfaces: ['set out'],
    requiredAction: 'Present the requested details clearly and in a logical order.',
    answerShape: 'Distinct details or stages in the order that makes the task easiest to follow.',
    commonTrap: 'Leaving the requested structure implicit or mixing separate stages together.',
  },
  {
    surfaces: ['circle'],
    requiredAction: 'Mark the permitted option clearly for every statement or item supplied.',
    answerShape: 'One unambiguous selection for each printed item.',
    commonTrap: 'Leaving two options marked for one item or overlooking a later item.',
  },
  {
    surfaces: ['find'],
    requiredAction: 'Work out or identify the exact result requested.',
    answerShape: 'Relevant information or method → working where needed → clear result with units or label.',
    commonTrap: 'Stating a result without the working or identification the wording requires.',
  },
  {
    surfaces: ['draft'],
    requiredAction: 'Produce the requested document, diagram or communication in its expected form.',
    answerShape: 'Required format and audience → essential content → appropriate close or labels.',
    commonTrap: 'Supplying the content but omitting a required feature of the requested format.',
  },
  {
    surfaces: ['differentiate'],
    requiredAction: 'State the defining difference between the named things.',
    answerShape: 'A is … whereas B is …',
    commonTrap: 'Writing two separate descriptions without making the difference explicit.',
  },
  {
    surfaces: ['show'],
    requiredAction: 'Demonstrate the requested result using working, evidence, an equation or a diagram.',
    answerShape: 'Starting information → visible steps or evidence → requested result.',
    commonTrap: 'Writing only the final result when the question asks you to show it.',
  },
  {
    surfaces: ['derive'],
    requiredAction: 'Develop the requested expression step by step from known relationships.',
    answerShape: 'Starting relationship → justified algebraic steps → requested expression.',
    commonTrap: 'Quoting the final expression without the steps that derive it.',
  },
  {
    surfaces: ['convert'],
    requiredAction: 'Change the supplied value or expression into the requested unit or form.',
    answerShape: 'Original value → conversion factor or rule → converted value with the new unit.',
    commonTrap: 'Changing the number but leaving the original unit or form attached.',
  },
  {
    surfaces: ['insert'],
    requiredAction: 'Place each requested label, value or item in the correct printed position.',
    answerShape: 'One clear entry in every relevant position supplied by the paper.',
    commonTrap: 'Knowing the entries but not tying each one unambiguously to its position.',
  },
  {
    surfaces: ['devise'],
    requiredAction: 'Create a workable plan, method or set of strategies for the situation given.',
    answerShape: 'Goal → distinct practical actions → link showing how each action serves the goal.',
    commonTrap: 'Listing broad aims instead of actions that could be carried out.',
  },
  {
    surfaces: ['classify'],
    requiredAction: 'Place each named item into the category that matches its defining features.',
    answerShape: 'Item → precise category, repeated for every item requested.',
    commonTrap: 'Describing an item without assigning it to a category.',
  },
  {
    surfaces: ['recommend'],
    requiredAction: 'Propose a suitable action for the situation and support it where requested.',
    answerShape: 'Clear action → reason or expected consequence.',
    commonTrap: 'Giving background information without making a usable recommendation.',
  },
];

const ADDITIONAL_COMMANDS: CommandDemand[] = ADDITIONAL_COMMAND_GROUPS.flatMap(group => (
  group.surfaces.map(surface => ({
    surface,
    requiredAction: group.requiredAction,
    answerShape: group.answerShape,
    commonTrap: group.commonTrap,
  }))
));

const commandDemands: CommandDemand[] = [
  ...COMMAND_WORDS.flatMap(entry => [entry.word, ...(entry.aliases ?? [])].map(surface => ({
    surface,
    requiredAction: entry.requiredAction,
    answerShape: entry.structuralTemplate,
    commonTrap: entry.commonError,
  }))),
  ...EXTRA_COMMANDS,
  ...ADDITIONAL_COMMANDS,
].sort((a, b) => b.surface.length - a.surface.length);

const STOP_WORDS = new Set([
  'about', 'after', 'again', 'against', 'along', 'also', 'answer', 'before',
  'being', 'between', 'could', 'describe', 'determine', 'discuss', 'during',
  'each', 'explain', 'following', 'given', 'identify', 'including', 'into',
  'itself', 'marks', 'other', 'question', 'should', 'state', 'their', 'there',
  'these', 'they', 'those', 'through', 'using', 'which', 'while', 'with', 'would',
]);

const clean = (value: string) => value.replace(/\s+/g, ' ').trim();
const STANDALONE_PART_LABEL = /^(?:\((?:[a-h]|[ivx]+)\)|(?:[a-h]|[ivx]+)[.)]|\d+[.)])$/i;
const PRINTED_PART_LABEL = /(?<!\S)(?:\((?:[a-h]|[ivx]+)\)|(?:\d+|[a-h])[.)])(?=\s+\S)/gi;
const PRINTED_PART_REFERENCE = /\b(?:part|question|section)s?\s+(?:(?:\((?:[a-h]|[ivx]+)\)|(?:\d+|[a-h])[.)])\s*(?:(?:,|and|or)\s*)?)*$/i;
const LEADING_PART_LABEL_TOKEN = /^(\((?:[a-h]|[ivx]+)\)|(?:\d+|[a-h])[.)])\s+/i;

const DATA_TOKEN = /(?:€|£|\$)?\b\d+(?:[.,]\d+)?(?:\s*(?:m\s*s[−–-]?[1¹]?|km\s*h[−–-]?[1¹]?|m\/s|km\/h|seconds?|minutes?|hours?|mins?|mol|dm[³3]|cm[³3]|°(?:C|F)?|%|kg|mg|km|cm|mm|Pa|[gsmVAJWN]))?/gi;
const MEANINGFUL_DATA_UNIT = /(?:€|£|\$|m\s*s[−–-]?[1¹]?|km\s*h[−–-]?[1¹]?|m\/s|km\/h|seconds?|minutes?|hours?|mins?|mol|dm[³3]|cm[³3]|°(?:C|F)?|%|kg|mg|km|cm|mm|Pa|\b[VAJWN]\b)/i;

type PrintedPartStyle = 'parenthesised' | 'numbered' | 'bare-letter';

const printedPartStyle = (label: string): PrintedPartStyle => {
  if (label.startsWith('(')) return 'parenthesised';
  return /^\d/.test(label) ? 'numbered' : 'bare-letter';
};

const coherentBareLetterRun = (labels: RegExpMatchArray[]): RegExpMatchArray[] => {
  const run: RegExpMatchArray[] = [];
  for (const label of labels) {
    const letter = label[0][0]?.toLowerCase();
    if (!letter) break;
    if (run.length > 0) {
      const previous = run[run.length - 1][0][0].toLowerCase();
      if (letter.charCodeAt(0) !== previous.charCodeAt(0) + 1) break;
    }
    run.push(label);
  }
  return run;
};

interface PrintedPartLine {
  label: string;
  labels: string[];
  text: string;
}

const leadingPrintedPart = (line: string): PrintedPartLine | null => {
  const labels: string[] = [];
  let rest = line;
  let match = LEADING_PART_LABEL_TOKEN.exec(rest);
  while (match) {
    labels.push(match[1]);
    rest = rest.slice(match[0].length);
    match = LEADING_PART_LABEL_TOKEN.exec(rest);
  }
  return labels.length > 0 && rest.trim()
    ? { label: labels.join(' '), labels, text: line }
    : null;
};

const printedPlanParts = (lines: string[]): PrintedPartLine[] => {
  const parsed = lines.map(leadingPrintedPart);
  return parsed.flatMap((part, index) => {
    if (!part) return [];
    const firstChild = parsed[index + 1];
    const secondChild = parsed[index + 2];
    if (!part.text.trimEnd().endsWith(':') || !firstChild || !secondChild) return [part];

    const wrapperStyle = printedPartStyle(part.labels[part.labels.length - 1]);
    const firstChildStyle = printedPartStyle(firstChild.labels[firstChild.labels.length - 1]);
    const secondChildStyle = printedPartStyle(secondChild.labels[secondChild.labels.length - 1]);
    // A colon-terminated labelled line can be a wrapper rather than an answer
    // place: “(ii) Define the following: 1. Biosphere 2. Niche”. Keep the
    // wrapper in Read, but let its repeated child labels own the plan fields.
    return firstChildStyle !== wrapperStyle && secondChildStyle === firstChildStyle ? [] : [part];
  });
};

const splitAtPrintedPartLabels = (line: string): string[] => {
  const labels = [...line.matchAll(PRINTED_PART_LABEL)].filter(match => {
    const index = match.index ?? 0;
    return !PRINTED_PART_REFERENCE.test(line.slice(0, index));
  });
  if (labels.length < 2) return [line];

  // A repeated label sequence is a list only when its first label begins the
  // line or follows printed punctuation. This keeps references such as
  // “part 1. above” inside their sentence while recognising SEC layouts such
  // as “Describe each: 1. Cornea 2. Retina”.
  const boundaries: RegExpMatchArray[] = [];
  const resolvedStyles = new Set<PrintedPartStyle>();
  for (let firstLabel = 0; firstLabel < labels.length; firstLabel += 1) {
    const first = labels[firstLabel];
    const index = first.index ?? 0;
    const before = line.slice(0, index).trimEnd();
    const followsOuterPart = /(?:^|[.!?;:]\s+)(?:\((?:[a-h]|[ivx]+)\)\s*)+$/i.test(before);
    if (index !== 0 && !/[.!?;:]$/.test(before) && !followsOuterPart) continue;

    const style = printedPartStyle(first[0]);
    if (resolvedStyles.has(style)) continue;
    const sameStyle = labels.slice(firstLabel).filter(label => printedPartStyle(label[0]) === style);
    const candidate = style === 'bare-letter' ? coherentBareLetterRun(sameStyle) : sameStyle;
    if (candidate.length >= 2) {
      boundaries.push(...candidate);
      resolvedStyles.add(style);
    }
  }
  if (boundaries.length < 2) return [line];
  boundaries.sort((a, b) => (a.index ?? 0) - (b.index ?? 0));

  const parts: string[] = [];
  const firstIndex = boundaries[0].index ?? 0;
  if (firstIndex > 0) parts.push(line.slice(0, firstIndex));
  boundaries.forEach((match, index) => {
    const start = match.index ?? 0;
    const end = boundaries[index + 1]?.index ?? line.length;
    parts.push(line.slice(start, end));
  });
  return parts.map(clean).filter(Boolean);
};

export function splitQuestionLines(text: string): string[] {
  const exact = text.trim();
  if (!exact) return [];
  const physical = exact.split(/\n+/).map(clean).filter(Boolean);
  const out: string[] = [];
  for (const line of physical) {
    const parts = splitAtPrintedPartLabels(line).flatMap(part => part.split(
      /(?<=[?!.;:])\s+(?=(?:(?:\((?:[a-hA-H]|[ivxIVX]+|[1-8])\)|(?:[a-hA-H]|[ivxIVX]+|[1-8])[.)])\s+)?[A-Z])/,
    )).map(clean).filter(Boolean);
    for (let index = 0; index < parts.length; index += 1) {
      const value = parts[index];
      const following = parts[index + 1];
      // A numbered/lettered label belongs to the wording that follows it.
      // Treating “1.” as a line of its own gives the student less context than
      // the paper and makes text-to-speech announce a meaningless number.
      if (STANDALONE_PART_LABEL.test(value) && following) {
        const labels = [value];
        let wordingIndex = index + 1;
        while (wordingIndex < parts.length && STANDALONE_PART_LABEL.test(parts[wordingIndex])) {
          labels.push(parts[wordingIndex]);
          wordingIndex += 1;
        }
        if (wordingIndex < parts.length) {
          out.push(`${labels.join(' ')} ${parts[wordingIndex]}`);
          index = wordingIndex;
        } else {
          out.push(labels.join(' '));
          index = wordingIndex - 1;
        }
      } else {
        out.push(value);
      }
    }
  }
  // Do not cap this list. The line-focus control describes itself as the exact
  // question, so dropping later sentences or sub-parts would be materially
  // worse than asking the student to move through a longer set of lines.
  return out;
}

interface CommandMatch {
  demand: CommandDemand;
  index: number;
  end: number;
  match: string;
}

const NOUN_LIKE_COMMANDS = new Set(['label', 'list', 'name', 'outline', 'state']);
const QUESTION_COMMANDS = new Set([
  'how', 'how can', 'how does', 'how far', 'how would', 'in which', 'through which', 'to what extent',
  'to which', 'under what', 'what', 'what could', 'what does', 'what distinguishes', 'what is', 'what is meant by', 'what term',
  'where', 'where does', 'where would', 'which',
  'why',
]);

const stripPartLabel = (value: string): string => value.replace(
  /^\s*(?:(?:\((?:[a-h]|[ivx]+)\)|(?:[a-h]|[ivx]+)[.)]|\d+[.)])\s*)+/i,
  '',
);

const clausePrefixBefore = (text: string, index: number): string => {
  const before = text.slice(0, index);
  const boundary = Math.max(
    before.lastIndexOf('.'),
    before.lastIndexOf('?'),
    before.lastIndexOf('!'),
    before.lastIndexOf(';'),
    before.lastIndexOf('\n'),
  );
  return stripPartLabel(before.slice(boundary + 1));
};

const endsAsQuestion = (text: string, start: number): boolean => {
  const tail = text.slice(start);
  const terminal = tail.search(/[.?!;]/);
  return terminal >= 0 && tail[terminal] === '?';
};

/** Words that can be either an instruction or ordinary question content. */
function isLikelyCommandUse(text: string, index: number, match: string): boolean {
  const key = match.toLowerCase();
  const before = text.slice(0, index);
  const after = text.slice(index + match.length);
  const clausePrefix = clausePrefixBefore(text, index);
  const prefix = clausePrefix.trim();

  // “the outline diagram”, “a list of terms” and “the label on the bottle”
  // are nouns. Treating them as imperatives hid the real Identify/Match/State
  // later in the same printed question.
  if (
    NOUN_LIKE_COMMANDS.has(key)
    && /\b(?:a|an|the|this|that|each|its|their)\s+$/i.test(before)
  ) return false;
  if (key === 'list' && /^\s+(?:of\b|provided\b|above\b|below\b)/i.test(after)) return false;
  if (key === 'outline' && /^\s+(?:diagram|drawing|map)\b/i.test(after)) return false;
  if (key === 'name' && /^\s+of\b/i.test(after)) return false;
  if (key === 'use' && /^\s*\)?\s+of\b/i.test(after)) return false;
  if (key === 'set out' && /^\s+(?:above|below)\b/i.test(after)) return false;
  if (key === 'complete' && /^\s+decomposition\b/i.test(after)) return false;
  if (
    key === 'state'
    && /^\s+(?:agency|body|broadcaster|company|enterprise|examinations?|ownership|pension|sector|services?)\b/i.test(after)
  ) return false;
  if (NOUN_LIKE_COMMANDS.has(key) && /^\s*:/.test(after)) return false;

  // A word boundary also exists inside a hyphenated compound. “solid-state”
  // is question content, not a new instruction beginning after a dash.
  if (/[\p{L}\p{N}]-$/u.test(before)) return false;

  // Infinitives and modal constructions describe context rather than telling
  // the student what to do: “a trial to distinguish …”, “which could explain
  // …”. The actual paper command normally follows later.
  if (/\bto\s+$/i.test(before) && key !== 'to what extent') return false;
  if (/\b(?:can|could|may|might|must|should|will|would)\s+$/i.test(before)) return false;

  // “which” is interrogative after a question preposition (“in which”, “at
  // which”, “of which”). After an ordinary noun—“hydrogen gas which could…”—
  // it is a relative pronoun, not the task.
  if (QUESTION_COMMANDS.has(key)) {
    if (!endsAsQuestion(text, index)) return false;
    if (!prefix) return true;
    if (/^(?:at|by|for|from|in|of|to|with)\s+$/i.test(prefix)) return true;
    if (/^(?:according to|based on|from|given|in relation to|in the context of|using|with reference to)\b[^,]{0,220},\s*$/i.test(prefix)) {
      return true;
    }
    if (/^(?:as|if|when)\b[^,]{0,220},\s*$/i.test(prefix)) return true;
    return false;
  }

  // Imperatives are accepted at the start of a printed sentence/part, after a
  // lead-in comma, or as an explicitly joined second instruction. Dictionary
  // words elsewhere in prose are content, not commands.
  if (!prefix) return true;
  if (/(?:,|[—–]|(?:^|\s)-)\s*$/.test(clausePrefix)) return true;
  if (/\b(?:and|then)\s+$/i.test(clausePrefix)) return true;
  if (/^briefly$/i.test(prefix)) return true;
  if (/^(?:part|question|section)\s+[a-z0-9()]+:\s*$/i.test(prefix)) return true;
  if (/^(?:according to|based on|from|given|in relation to|referring to|using|with reference to)\b.{0,220}$/i.test(prefix)) {
    // SEC lead-ins do not consistently include a comma (“Using the data
    // below explain …”). Accept the command when it follows a completed
    // source phrase, but not when it sits inside that phrase (“on complete
    // decomposition”).
    const lastLeadInWord = prefix.match(/([A-Za-z]+)[^A-Za-z]*$/)?.[1] ?? '';
    if (!/^(?:a|an|and|as|at|by|for|from|in|into|of|on|or|the|to|under|with)$/i.test(lastLeadInWord)) {
      return true;
    }
  }
  return false;
}

function commandMatches(text: string): CommandMatch[] {
  const candidates: CommandMatch[] = [];
  for (const demand of commandDemands) {
    const re = new RegExp(`\\b${escapeRe(demand.surface)}\\b`, 'gi');
    for (const match of text.matchAll(re)) {
      if (match.index === undefined || !isLikelyCommandUse(text, match.index, match[0])) continue;
      candidates.push({
        demand,
        index: match.index,
        end: match.index + match[0].length,
        match: match[0],
      });
    }
  }
  candidates.sort((a, b) => a.index - b.index || b.match.length - a.match.length);

  // Longest wins where surfaces overlap (“what is meant by” over “what is”
  // and “what”). Then keep one command per clause unless another is explicitly
  // joined (“state and explain”) or starts a new printed sentence/part.
  const nonOverlapping: CommandMatch[] = [];
  for (const candidate of candidates) {
    if (nonOverlapping.some(item => candidate.index < item.end && candidate.end > item.index)) continue;
    nonOverlapping.push(candidate);
  }

  const selected: CommandMatch[] = [];
  for (const candidate of nonOverlapping) {
    const previous = selected[selected.length - 1];
    if (previous) {
      const between = text.slice(previous.end, candidate.index);
      const newClause = /[.?!;:]|\((?:[ivx]+|[a-h])\)/i.test(between);
      const joinedInstruction = /\b(?:and|then)\s+$/i.test(text.slice(0, candidate.index));
      if (!newClause && !joinedInstruction) continue;
    }
    selected.push(candidate);
  }
  return selected;
}

export function findCommandDemands(text: string): CommandDemand[] {
  return commandMatches(text).map(item => ({ ...item.demand, surface: item.match }));
}

export function findCommandDemand(text: string): CommandDemand | null {
  return findCommandDemands(text)[0] ?? null;
}

function findConstraints(text: string, source: WaysInQuestionSource): string[] {
  const found: string[] = [];
  const patterns = [
    /\b(?:any\s+)?(?:one|two|three|four|five|six|seven|eight|[1-8])\s+(?:distinct\s+|different\s+)?(?:features?|reasons?|examples?|advantages?|disadvantages?|differences?|similarities?|points?|factors?|ways?|items?|uses?|steps?|terms?|methods?|properties?|functions?)\b[^.;?]*/gi,
    /\b(?:both|each|respectively)\b[^.;?]*/gi,
    /\b(?:with reference to|using|based on|according to|from the (?:diagram|graph|table|passage))\b[^.;?]*/gi,
  ];
  for (const pattern of patterns) {
    for (const match of text.matchAll(pattern)) {
      const value = clean(match[0]);
      if (value.length > 3 && value.length < 150 && !found.some(x => x.toLowerCase() === value.toLowerCase())) {
        found.push(value);
      }
    }
  }
  if (source.answerShape?.choice) {
    found.unshift(`Answer ${source.answerShape.choice.answer} of ${source.answerShape.choice.available} available parts.`);
  }
  if (source.answerShape?.totalMarks) {
    found.push(`${source.answerShape.totalMarks} marks are available in total.`);
  }
  if (source.figure) found.push('The printed figure is part of the question.');
  return found.slice(0, 5);
}

function findGivens(source: WaysInQuestionSource): string[] {
  const found: string[] = [];
  const add = (value: string) => {
    const exact = clean(value);
    if (!exact || found.some(item => item === exact || item.includes(exact))) return;
    found.push(exact);
  };
  if (source.stem) {
    splitQuestionLines(source.stem)
      .flatMap(line => line.split(/(?<=;)\s+/).map(clean).filter(Boolean))
      .forEach(line => {
        if (findCommandDemands(line).length === 0) {
          add(line);
          return;
        }
        (line.match(DATA_TOKEN) ?? [])
          .filter(token => MEANINGFUL_DATA_UNIT.test(token))
          .forEach(add);
      });
  }

  // Preserve data as complete printed clauses where possible. When a command
  // sentence also contains a value ("Calculate ... in 1.2 seconds"), keep the
  // exact value and unit rather than duplicating the whole task under
  // "Information supplied". Every returned fragment is still verbatim paper
  // text; nothing is inferred from the marking scheme.
  for (const line of splitQuestionLines(source.questionText)) {
    const withoutPartLabels = line.replace(
      /(?:^|\s)(?:\((?:[a-h]|[ivx]+)\)|[1-8][.)])(?=\s)/gi,
      ' ',
    );
    const numericTokens = withoutPartLabels.match(DATA_TOKEN) ?? [];
    const hasExplicitUnit = numericTokens.some(token => MEANINGFUL_DATA_UNIT.test(token));
    const hasDataContext = /\b(?:average|data|graph|mass|mean|number|price|rate|table|temperature|time|trial|value|volume)\b/i.test(withoutPartLabels);
    const startsWithInstruction = findCommandDemands(withoutPartLabels).length > 0;
    if (!startsWithInstruction && (
      numericTokens.length >= 2
      || ((hasExplicitUnit || hasDataContext) && numericTokens.length >= 1)
    )) {
      add(line);
      continue;
    }

    if (startsWithInstruction) {
      numericTokens
        .filter(token => MEANINGFUL_DATA_UNIT.test(token))
        .filter(token => !found.some(item => item.toLowerCase().includes(clean(token).toLowerCase())))
        .forEach(add);
    }
  }

  const quoted = source.questionText.match(/[“"][^”"]{2,120}[”"]/g) ?? [];
  quoted.forEach(add);
  return found;
}

function findKeywords(text: string, commands: CommandDemand[]): string[] {
  const words = Array.from(
    text.matchAll(/[A-Za-zÀ-ÖØ-öø-ÿ][A-Za-zÀ-ÖØ-öø-ÿ'-]{3,}/g),
    match => match[0],
  );
  const counts = new Map<string, { label: string; count: number; first: number }>();
  words.forEach((word, index) => {
    const key = word.toLowerCase();
    if (STOP_WORDS.has(key) || commands.some(command => key === command.surface.toLowerCase())) return;
    const current = counts.get(key);
    counts.set(key, current ? { ...current, count: current.count + 1 } : { label: word, count: 1, first: index });
  });
  return [...counts.values()]
    .sort((a, b) => b.count - a.count || a.first - b.first)
    .slice(0, 7)
    .map(item => item.label);
}

function buildHighlights(text: string, commands: CommandDemand[], constraints: string[]): QuestionHighlight[] {
  const ranges: QuestionHighlight[] = [];
  const add = (start: number, end: number, kind: QuestionHighlight['kind'], label: string) => {
    if (start < 0 || end <= start || ranges.some(r => start < r.end && end > r.start)) return;
    ranges.push({ start, end, kind, label });
  };
  let commandCursor = 0;
  for (const command of commands) {
    const index = text.toLowerCase().indexOf(command.surface.toLowerCase(), commandCursor);
    add(index, index + command.surface.length, 'action', 'The job');
    if (index >= 0) commandCursor = index + command.surface.length;
  }
  for (const constraint of constraints) {
    const printed = constraint.replace(/\.$/, '');
    const index = text.toLowerCase().indexOf(printed.toLowerCase());
    if (index >= 0) add(index, index + printed.length, 'constraint', 'Boundary');
  }
  for (const match of text.matchAll(/\b\d+(?:\.\d+)?(?:\s*(?:%|°C|kg|g|mg|km|m|cm|mm|s|min|mol|dm³|cm³|V|A|N|J|W|Pa))?\b/g)) {
    if (match.index !== undefined) add(match.index, match.index + match[0].length, 'data', 'Given data');
  }
  return ranges.sort((a, b) => a.start - b.start);
}

const NUMBER_WORDS: Record<string, number> = {
  one: 1, two: 2, three: 3, four: 4, five: 5, six: 6, seven: 7, eight: 8,
};

const COUNTED_ANSWER_NOUNS = [
  'advantages?', 'arguments?', 'benefits?', 'causes?', 'characteristics?', 'consequences?',
  'details?', 'differences?', 'disadvantages?', 'effects?', 'elements?',
  'examples?', 'factors?', 'features?', 'functions?', 'ideas?', 'items?',
  'measures?', 'methods?', 'observations?', 'points?', 'problems?', 'properties?',
  'reasons?', 'recommendations?', 'results?', 'roles?', 'similarities?',
  'solutions?', 'steps?', 'terms?', 'treatments?', 'uses?', 'ways?',
].join('|');

const countValue = (token: string): number | null => {
  const value = NUMBER_WORDS[token.toLowerCase()] ?? Number(token);
  return Number.isInteger(value) && value >= 1 && value <= 8 ? value : null;
};

/**
 * Find an answer count only when the question itself prints one.
 *
 * Marks and marking rows are intentionally ignored: six marks might mean one
 * developed explanation, six labels, or several tariff-dependent points. A
 * planning tool that turns the tariff into six boxes is not simplifying the
 * question; it is inventing a different one.
 */
export function findPrintedPlanShape(text: string): WaysInQuestionModel['planShape'] {
  // A printed choice overrides the number of options that follows. “Three of
  // the following” means three plan lines even when four labelled options are
  // printed beneath it.
  const explicitChoice = new RegExp(
    '\\b((?:any\\s+)?(one|two|three|four|five|six|seven|eight|[1-8])\\s+of\\s+(?:the\\s+)?(?:following|these))\\b',
    'i',
  ).exec(text);
  if (explicitChoice) {
    const count = countValue(explicitChoice[2]);
    if (count) {
      return {
        count,
        basis: 'printed',
        evidence: explicitChoice[1],
        structure: 'choice',
      };
    }
  }

  const blanks = text.match(/_{3,}/g) ?? [];
  if (blanks.length >= 1 && blanks.length <= 8) {
    return {
      count: blanks.length,
      basis: 'printed',
      evidence: blanks.join(' '),
      structure: 'blanks',
    };
  }

  // Repeated sub-part labels are an explicit structure even when the paper
  // does not state a number in prose: “(i) … (ii) …” safely means two places
  // to plan, without consulting the marking scheme.
  const partLabels = printedPlanParts(splitQuestionLines(text)).map(part => part.label);
  const uniqueParts = [...new Set(partLabels.map(label => label.toLowerCase()))];
  if (uniqueParts.length >= 2 && uniqueParts.length <= 8) {
    return {
      count: uniqueParts.length,
      basis: 'printed',
      evidence: partLabels.filter((label, index) => (
        partLabels.findIndex(item => item.toLowerCase() === label.toLowerCase()) === index
      )).join(', '),
      structure: 'parts',
    };
  }

  // Figure questions often express the structure as labels rather than a
  // number: “Name the parts labelled A and B.” Keep those exact labels ahead
  // of command/count heuristics so one role “for each” cannot collapse them.
  const labels = /\b(?:labelled|labeled|marked)\s+([A-Z](?:\s*,\s*[A-Z])*(?:\s*,?\s+(?:and|or)\s+[A-Z])?)\b/.exec(text);
  if (labels) {
    const count = new Set(labels[1].match(/\b[A-Z]\b/g) ?? []).size;
    if (count >= 1 && count <= 8) {
      return {
        count,
        basis: 'printed',
        evidence: labels[0],
        structure: 'labels',
      };
    }
  }

  const number = '(one|two|three|four|five|six|seven|eight|[1-8])';
  const countedPattern = new RegExp(
    `\\b(any\\s+)?${number}\\s+(?:distinct\\s+|different\\s+)?(?:${COUNTED_ANSWER_NOUNS})\\b`,
    'gi',
  );
  const commands = commandMatches(text);
  const counted = (commands.length === 1 ? [...text.matchAll(countedPattern)] : []).filter(match => {
    if (match.index === undefined) return false;
    const before = text.slice(0, match.index);
    const after = text.slice(match.index + match[0].length);
    if (/\b(?:these|those|the|following|listed|supplied)\s+$/i.test(before)) return false;
    if (/^\s+(?:do|does|is|are|was|were|has|have|had|can|could|will|would|may|might)\b/i.test(after)) {
      return false;
    }
    if (/^\s+(?:for|of)\s+(?:both|each)\b/i.test(after)) return false;
    return commands.some(command => (
      command.end <= match.index!
      && !/[.?!;]/.test(text.slice(command.end, match.index))
    ));
  });

  // “Suggest one reason for any three treatments” is a common, unambiguous
  // nested construction: the selectable items set the number of plan lines.
  // Other competing count phrases are left flexible rather than guessed.
  const preferred = counted.length === 1
    ? counted[0]
    : counted.length === 2 && counted.filter(match => Boolean(match[1])).length === 1
      ? counted.find(match => Boolean(match[1]))
      : undefined;
  if (preferred) {
    const count = countValue(preferred[2]);
    if (count) {
      return {
        count,
        basis: 'printed',
        evidence: preferred[0],
        structure: 'count-phrase',
      };
    }
  }

  // With several separately printed instructions, one starting line per task
  // is a safe decomposition. It is deliberately not presented as the number
  // of marking points; the student can add lines within any task that needs it.
  if (commands.length >= 2 && commands.length <= 8) {
    return {
      count: commands.length,
      basis: 'printed',
      evidence: commands.map(command => command.match).join(', '),
      structure: 'instructions',
    };
  }

  return { count: 1, basis: 'flexible' };
}

const CALCULATION_COMMANDS = new Set(['calculate', 'convert', 'derive', 'estimate']);
const COMPARISON_COMMANDS = new Set(['compare', 'contrast', 'differentiate', 'distinguish', 'what distinguishes']);
const EXPLANATION_COMMANDS = new Set([
  'account for', 'comment', 'discuss', 'evaluate', 'explain', 'justify', 'predict', 'suggest', 'why',
]);
const PROCEDURE_COMMANDS = new Set(['construct', 'describe', 'devise', 'draft', 'how can', 'how does', 'how would', 'outline', 'set out']);

const prompt = (
  id: string,
  label: string,
  placeholder: string,
  sourceText?: string,
): WaysInPlanPrompt => ({ id, label, placeholder, ...(sourceText ? { sourceText } : {}) });

function buildPlanPrompts(
  source: WaysInQuestionSource,
  commands: CommandDemand[],
  planShape: WaysInQuestionModel['planShape'],
  givens: string[],
): { kind: WaysInPlanKind; prompts: WaysInPlanPrompt[] } {
  const sourceLines = [
    ...splitQuestionLines(source.stem ?? ''),
    ...splitQuestionLines(source.questionText),
  ];
  const questionLines = splitQuestionLines(source.questionText);

  if (planShape.structure === 'parts') {
    const partLines = printedPlanParts(questionLines).slice(0, planShape.count);
    if (partLines.length === planShape.count) {
      return {
        kind: 'printed-parts',
        prompts: partLines.map((part, index) => {
          const displayLabel = part.label.replace(/([a-h]|\d+)[.)]$/i, '$1');
          return prompt(
            `part-${index + 1}`,
            `Part ${displayLabel}`,
            'Your response idea for this exact part',
            part.text,
          );
        }),
      };
    }
  }

  if (planShape.structure === 'instructions') {
    // The stem can contain a contextual instruction (for example “Analyse the
    // graph”), but a printed multi-task plan must mirror the tasks on this card.
    // Otherwise that stem command can displace the final question instruction.
    // Consume the printed lines in order as well: repeated verbs in separate
    // sentences are separate tasks, while joined verbs on one sentence still
    // intentionally share that sentence as their context.
    const instructionTasks = questionLines.flatMap(line => (
      findCommandDemands(line).map(command => ({ command, sourceText: line }))
    ));
    const instructionPrompts = instructionTasks.slice(0, planShape.count).map((task, index) => {
      return prompt(
        `instruction-${index + 1}`,
        `Task ${index + 1}: ${task.command.surface}`,
        'Your response idea for this exact task',
        task.sourceText,
      );
    });
    if (instructionPrompts.length === planShape.count) {
      return {
        kind: 'printed-parts',
        prompts: instructionPrompts,
      };
    }
  }

  if (planShape.structure === 'labels' && planShape.evidence) {
    const labels = planShape.evidence.match(/\b[A-Z]\b/g) ?? [];
    if (labels.length === planShape.count) {
      return {
        kind: 'printed-parts',
        prompts: labels.map((label, index) => prompt(
          `label-${label.toLowerCase()}-${index + 1}`,
          `Label ${label}`,
          `Your response for label ${label}`,
          source.questionText,
        )),
      };
    }
  }

  if (planShape.basis === 'printed' && planShape.count > 1) {
    const paperText = [source.stem, source.questionText].filter(Boolean).join('\n');
    const sourceText = planShape.evidence && paperText.includes(planShape.evidence)
      ? planShape.evidence
      : undefined;
    return {
      kind: 'printed-parts',
      prompts: Array.from({ length: planShape.count }, (_, index) => prompt(
        `printed-${index + 1}`,
        planShape.structure === 'choice' ? `Chosen response ${index + 1}` : `Response ${index + 1}`,
        'Keep this as one distinct response',
        sourceText,
      )),
    };
  }

  const surfaces = commands.map(command => command.surface.toLowerCase());
  const taskLine = sourceLines.find(line => findCommandDemands(line).length > 0) ?? source.questionText;
  const hasNumericalData = givens.some(item => (item.match(DATA_TOKEN) ?? []).some(token => MEANINGFUL_DATA_UNIT.test(token)));
  const isCalculation = surfaces.some(surface => CALCULATION_COMMANDS.has(surface))
    || (hasNumericalData && surfaces.some(surface => ['determine', 'find', 'show'].includes(surface)));

  if (isCalculation) {
    return {
      kind: 'calculation',
      prompts: [
        prompt('values', 'Values supplied', 'Copy the values and units you need'),
        prompt('target', 'Quantity to find', 'Name what the question asks you to find', taskLine),
        prompt('relationship', 'Relationship', 'Write the formula or rule you plan to use'),
        prompt('substitution', 'Substitution', 'Place the supplied values into that relationship'),
        prompt('result', 'Result and unit', 'Record the result and its unit'),
      ],
    };
  }

  if (surfaces.some(surface => COMPARISON_COMMANDS.has(surface))) {
    return {
      kind: 'comparison',
      prompts: [
        prompt('first-side', 'First item', 'Note the relevant feature of the first item', taskLine),
        prompt('second-side', 'Second item', 'Note the corresponding feature of the second item'),
        prompt('difference', 'Difference or connection', 'Make the comparison explicit'),
      ],
    };
  }

  if (surfaces.some(surface => PROCEDURE_COMMANDS.has(surface))
    && /\b(?:how|method|procedure|steps?|prepare|carry out|dilut|experiment|investigat)\b/i.test(`${source.stem ?? ''} ${source.questionText}`)) {
    return {
      kind: 'procedure',
      prompts: [
        prompt('start', 'Starting action', 'Write the first action', taskLine),
        prompt('middle', 'Next action or actions', 'Keep the sequence in order'),
        prompt('finish', 'Finish or check', 'Write how the procedure is completed or checked'),
      ],
    };
  }

  if (surfaces.some(surface => EXPLANATION_COMMANDS.has(surface))) {
    return {
      kind: 'explanation',
      prompts: [
        prompt('reason', 'Main reason or claim', 'State the point you intend to make', taskLine),
        prompt('evidence', 'Relevant information', 'Copy the exact fact or context you will use'),
        prompt('link', 'Link to the question', 'Connect your point back to what was asked'),
      ],
    };
  }

  return {
    kind: 'direct',
    prompts: [prompt('direct', 'Direct response', 'Write the exact response you intend to give', taskLine)],
  };
}

export function buildQuestionModel(source: WaysInQuestionSource): WaysInQuestionModel {
  const exactText = source.questionText.trim();
  const paperText = [source.stem?.trim(), exactText].filter(Boolean).join('\n');
  const commands = findCommandDemands(paperText);
  const command = commands[0] ?? null;
  // The lead-in is consulted for its instruction and supplied information, but
  // not for an answer count: SEC section-level stems such as “answer eight of
  // the following” describe the paper, not eight responses to this card.
  const constraints = findConstraints(exactText, source);
  const lines = splitQuestionLines(exactText);
  const printedPlan = findPrintedPlanShape(exactText);
  const planShape = printedPlan.basis === 'printed' || !source.answerShape?.points
    ? printedPlan
    : {
        count: Math.max(1, Math.min(8, source.answerShape.points)),
        basis: 'printed' as const,
      };
  const givens = findGivens(source);
  const plan = buildPlanPrompts(source, commands, planShape, givens);
  return {
    exactText,
    lines,
    commands,
    command,
    givens,
    constraints,
    keywords: findKeywords(exactText, commands),
    planShape,
    expectedPoints: planShape.count,
    planKind: plan.kind,
    planPrompts: plan.prompts,
    highlights: buildHighlights(exactText, commands, constraints),
    steps: [
      {
        id: 'meet', eyebrow: 'First, only read', title: 'Meet the exact question',
        prompt: 'Take it one line at a time. Nothing needs to be answered yet.',
      },
      {
        id: 'job', eyebrow: 'Find the verb', title: 'Name the job',
        prompt: 'The command word decides what kind of answer the examiner is asking you to build.',
      },
      {
        id: 'boundaries', eyebrow: 'Keep hold of', title: 'Collect the givens and boundaries',
        prompt: 'Separate what the question supplies from the limits it places on your answer.',
      },
      {
        id: 'shape', eyebrow: 'Before writing', title: 'Build an empty answer shape',
        prompt: 'Plan distinct spaces for distinct ideas. The spaces are not answers; they stop one idea swallowing the whole response.',
      },
      {
        id: 'attempt', eyebrow: 'Your turn', title: 'Make the attempt',
        prompt: 'Write in your own words. Your draft stays on this device and the marking scheme remains closed.',
      },
      {
        id: 'return', eyebrow: 'Remove the scaffold', title: 'Return to the original',
        prompt: 'Check that your answer still meets the exact wording before going back to the exam question.',
      },
    ],
  };
}
