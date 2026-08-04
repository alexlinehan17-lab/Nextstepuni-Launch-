/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Which words of an exam question carry the emphasis mark.
 *
 * An SEC question is a command clause wrapped in method and scope: "Using the
 * data in the table below | briefly explain the effect of harvest date on the
 * DMD %", or "Identify the part of the plant where respiration takes place | by
 * placing a tick in the correct box". The command clause is what decides
 * whether an answer earns full marks; the rest says where to look and how to
 * write it down.
 *
 * So the mark is anchored on the examiner's command word rather than on the
 * start of the sentence — the method can come first or last, and both shapes
 * are common. Marking the whole sentence was the alternative; on a two-line
 * question a filled highlight becomes a slab, which is the opposite of what an
 * emphasis is for.
 *
 * Anchoring alone is not enough, because plenty of questions carry their scope
 * with no method marker at all — "Calculate the amount of concentrate feed
 * required | for his beef calves during the six-week weaning period" has nothing
 * in it to cut on, and the whole two-line sentence came back marked. So there is
 * a second, purely typographic rule: a mark that would run past one line is cut
 * back to the last phrase boundary that still fits on one. It is a length rule
 * rather than a grammar rule on purpose — a short question is left whole, and
 * only the ones that would become slabs are trimmed.
 */

/**
 * The SEC command words, longest first so "briefly explain" wins over
 * "explain" and the adverb is marked with its verb.
 */
const COMMANDS = [
  'briefly explain', 'briefly describe', 'briefly outline', 'briefly discuss',
  'distinguish between', 'account for', 'comment on', 'refer to',
  'identify', 'describe', 'distinguish', 'calculate', 'evaluate', 'illustrate',
  'summarise', 'summarize', 'complete', 'consider', 'contrast', 'discuss',
  'explain', 'justify', 'outline', 'analyse', 'analyze', 'compare', 'suggest',
  'define', 'derive', 'assess', 'sketch', 'state', 'name', 'list', 'give',
  'draw', 'show', 'find', 'plot', 'label', 'write',
];

const COMMAND_RE = new RegExp(`\\b(?:${COMMANDS.join('|')})\\b`, 'i');

/** Where the command clause ends and method or scope resumes. */
const TAIL = new RegExp(
  [
    '\\sby\\s', '\\susing\\s', '\\swith reference to\\s', '\\swith the aid of\\s',
    '\\sfrom the (?:data|table|graph|diagram)\\b',
    '\\sin the (?:correct|table|graph|diagram|space)\\b',
    '\\saccording to\\s', '\\sbased on\\s', ':',
  ].join('|'),
  'i',
);

/**
 * Below this a clause is a fragment, and marking three words of a long question
 * reads as an accident rather than emphasis — so the tail is left attached.
 */
const MIN_CLAUSE = 20;

/**
 * About one line of the question column (620px at 20px Source Serif). Past this
 * the mark wraps, and a wrapped emphasis is the slab we are avoiding.
 */
const MAX_CLAUSE = 62;

/**
 * Words that open a trailing phrase — scope, place, time, condition — and so are
 * safe places to stop marking.
 *
 * Deliberately NOT in the list: "of", which ties an object to the noun it
 * belongs to ("the structure | of the leaf"), and "and"/"or", which join two
 * halves of one instruction ("distinguish between X | and Y"). Cutting at either
 * ends the mark mid-thought, which is worse than a mark that runs long.
 */
const SCOPE = new RegExp(
  `\\s(?:${[
    'for', 'during', 'over', 'throughout', 'within', 'across', 'between',
    'from', 'into', 'onto', 'under', 'about', 'after', 'before', 'since',
    'until', 'per', 'in', 'on', 'at', 'to', 'with', 'by', 'using',
    'when', 'where', 'which', 'who', 'whose', 'that', 'as', 'if',
  ].join('|')})\\b`,
  'gi',
);

/**
 * Cut a clause back to one line.
 *
 * Returns `[head, tail]` where `head + tail` is the input, unchanged. The cut is
 * the LAST phrase boundary that still fits — so the mark is as long as one line
 * allows rather than as short as the first preposition allows. Where nothing
 * fits, the first boundary past the ceiling is taken instead: still too long,
 * but shorter than the whole sentence. Where there is no boundary at all the
 * clause is left alone, because there is no honest place to stop.
 */
const toOneLine = (clause: string): [string, string] => {
  if (clause.length <= MAX_CLAUSE) return [clause, ''];

  SCOPE.lastIndex = 0;
  let fits = -1;
  let overflows = -1;
  for (let m = SCOPE.exec(clause); m; m = SCOPE.exec(clause)) {
    if (m.index < MIN_CLAUSE) continue;
    if (m.index <= MAX_CLAUSE) fits = m.index;
    else { overflows = m.index; break; }
  }

  const cut = fits >= 0 ? fits : overflows;
  if (cut < 0) return [clause, ''];

  const head = clause.slice(0, cut);
  const tail = clause.slice(cut);
  // Never trade a clause for whitespace.
  if (!head.trim() || !tail.trim()) return [clause, ''];
  return [head, tail];
};

export interface QuestionEmphasis {
  /** Method or scope printed before the command. Often empty. */
  before: string;
  /** The command clause. Carries the mark. Never empty. */
  marked: string;
  /** Method or scope printed after the command. Often empty. */
  after: string;
}

/**
 * Split a question into the command clause and the material around it.
 *
 * `before + marked + after` always reconstructs the input exactly, so a
 * rendering built on this cannot drop or duplicate a word of the question.
 */
export const splitForEmphasis = (text: string): QuestionEmphasis => {
  const q = text ?? '';
  const cmd = COMMAND_RE.exec(q);

  // No recognised command word: start the mark at the start of the question
  // rather than guess at a verb. The one-line rule still applies — an unanchored
  // mark over a whole two-line question is the same slab either way.
  if (!cmd) {
    const [marked, scope] = toOneLine(q);
    return { before: '', marked, after: scope };
  }

  const before = q.slice(0, cmd.index);
  const body = q.slice(cmd.index);

  // First cut: the method, where the question names one.
  let clause = body;
  let after = '';
  const tail = TAIL.exec(body);
  if (tail && tail.index >= MIN_CLAUSE) {
    const cut = tail[0] === ':' ? tail.index + 1 : tail.index;
    const rest = body.slice(cut);
    if (rest.trim()) { clause = body.slice(0, cut); after = rest; }
  }

  // Second cut: whatever scope is still riding on the end of a clause that would
  // wrap. Most questions have nothing to do here.
  const [marked, scope] = toOneLine(clause);
  return { before, marked, after: scope + after };
};
