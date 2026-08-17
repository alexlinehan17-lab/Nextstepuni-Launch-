import { COMMAND_WORDS } from '../../data/knowledge/commandWords';
import type {
  CommandDemand,
  QuestionHighlight,
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

const commandDemands: CommandDemand[] = [
  ...COMMAND_WORDS.flatMap(entry => [entry.word, ...(entry.aliases ?? [])].map(surface => ({
    surface,
    requiredAction: entry.requiredAction,
    answerShape: entry.structuralTemplate,
    commonTrap: entry.commonError,
  }))),
  ...EXTRA_COMMANDS,
].sort((a, b) => b.surface.length - a.surface.length);

const STOP_WORDS = new Set([
  'about', 'after', 'again', 'against', 'along', 'also', 'answer', 'before',
  'being', 'between', 'could', 'describe', 'determine', 'discuss', 'during',
  'each', 'explain', 'following', 'given', 'identify', 'including', 'into',
  'itself', 'marks', 'other', 'question', 'should', 'state', 'their', 'there',
  'these', 'they', 'those', 'through', 'using', 'which', 'while', 'with', 'would',
]);

const clean = (value: string) => value.replace(/\s+/g, ' ').trim();

export function splitQuestionLines(text: string): string[] {
  const exact = text.trim();
  if (!exact) return [];
  const physical = exact.split(/\n+/).map(clean).filter(Boolean);
  const out: string[] = [];
  for (const line of physical) {
    const parts = line.split(/(?<=[?!.;:])\s+(?=(?:\(?[a-z0-9ivx]+\)?[.)]?\s+)?[A-Z])/);
    for (const part of parts) {
      const value = clean(part);
      if (value) out.push(value);
    }
  }
  return out.slice(0, 12);
}

export function findCommandDemand(text: string): CommandDemand | null {
  let earliest: { demand: CommandDemand; index: number; match: string } | null = null;
  for (const demand of commandDemands) {
    const re = new RegExp(`\\b${escapeRe(demand.surface)}\\b`, 'i');
    const match = re.exec(text);
    if (!match) continue;
    if (
      earliest === null
      || match.index < earliest.index
      || (match.index === earliest.index && match[0].length > earliest.match.length)
    ) {
      earliest = { demand, index: match.index, match: match[0] };
    }
  }
  return earliest ? { ...earliest.demand, surface: earliest.match } : null;
}

function findConstraints(text: string, source: WaysInQuestionSource): string[] {
  const found: string[] = [];
  const patterns = [
    /\b(?:any|the)\s+(?:one|two|three|four|five|six|\d+)\b[^.;?]*/gi,
    /\b(?:one|two|three|four|five|six|\d+)\s+(?:features?|reasons?|examples?|advantages?|disadvantages?|differences?|similarities?|points?|factors?|ways?|items?|uses?)\b[^.;?]*/gi,
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
  if (source.stem) found.push(clean(source.stem));
  const text = `${source.stem ?? ''} ${source.questionText}`;
  const quoted = text.match(/[“"][^”"]{2,80}[”"]/g) ?? [];
  for (const value of quoted) found.push(clean(value));
  const data = text.match(/\b\d+(?:\.\d+)?\s*(?:%|°C|kg|g|mg|km|m|cm|mm|s|min|hours?|mol|dm³|cm³|V|A|N|J|W|Pa)?\b/g) ?? [];
  for (const value of data) {
    if (!found.includes(value) && !/^20\d{2}$/.test(value)) found.push(value);
  }
  return found.slice(0, 6);
}

function findKeywords(text: string, command: CommandDemand | null): string[] {
  const words = Array.from(
    text.matchAll(/[A-Za-zÀ-ÖØ-öø-ÿ][A-Za-zÀ-ÖØ-öø-ÿ'-]{3,}/g),
    match => match[0],
  );
  const counts = new Map<string, { label: string; count: number; first: number }>();
  words.forEach((word, index) => {
    const key = word.toLowerCase();
    if (STOP_WORDS.has(key) || key === command?.surface.toLowerCase()) return;
    const current = counts.get(key);
    counts.set(key, current ? { ...current, count: current.count + 1 } : { label: word, count: 1, first: index });
  });
  return [...counts.values()]
    .sort((a, b) => b.count - a.count || a.first - b.first)
    .slice(0, 7)
    .map(item => item.label);
}

function buildHighlights(text: string, command: CommandDemand | null, constraints: string[]): QuestionHighlight[] {
  const ranges: QuestionHighlight[] = [];
  const add = (start: number, end: number, kind: QuestionHighlight['kind'], label: string) => {
    if (start < 0 || end <= start || ranges.some(r => start < r.end && end > r.start)) return;
    ranges.push({ start, end, kind, label });
  };
  if (command) {
    const index = text.toLowerCase().indexOf(command.surface.toLowerCase());
    add(index, index + command.surface.length, 'action', 'The job');
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

function expectedPoints(source: WaysInQuestionSource, command: CommandDemand | null): number {
  if (source.answerShape?.points) return Math.max(1, Math.min(8, source.answerShape.points));
  if (!command) return 3;
  const key = command.surface.toLowerCase();
  if (['state', 'name', 'identify', 'define', 'label'].includes(key)) return 1;
  if (['compare', 'contrast', 'distinguish'].includes(key)) return 2;
  if (source.answerShape?.totalMarks) return Math.max(1, Math.min(6, Math.ceil(source.answerShape.totalMarks / 3)));
  return 3;
}

export function buildQuestionModel(source: WaysInQuestionSource): WaysInQuestionModel {
  const exactText = source.questionText.trim();
  const command = findCommandDemand(exactText);
  const constraints = findConstraints(exactText, source);
  const lines = splitQuestionLines(exactText);
  return {
    exactText,
    lines,
    command,
    givens: findGivens(source),
    constraints,
    keywords: findKeywords(exactText, command),
    expectedPoints: expectedPoints(source, command),
    highlights: buildHighlights(exactText, command, constraints),
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
