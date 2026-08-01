/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Mark Bank session screen — behaviour and design guards.
 *
 * The design tests here are not fussiness. Two of the rules they enforce exist
 * because breaking them silently destroys meaning: if the environment green ever
 * shares a surface with the success green, "you had this mark" stops reading as
 * a state; and if the suggested grade is signalled with colour rather than
 * shape, orange starts to mean "correct", which it must never do.
 */

import { describe, test, expect, vi } from 'vitest';
import { render, screen, fireEvent, within, waitFor } from '@testing-library/react';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

import SessionScreen, {
  claimableTotal,
  committedRoute,
  marksClaimed,
  rowMarks,
  showsRowMarks,
  suggestGrade,
} from '@/components/MarkBank/SessionScreen';
import { tariffReconciles, type MarkRow, type SecCard, type SecDiagramCard } from '@/types/markBank';

const row = (o: Partial<MarkRow> = {}): MarkRow => ({ id: 'r0', kind: 'point', verbatim: 'Oesophagus', marks: 2, ...o });

const card = (o: Partial<SecCard> = {}): SecCard => ({
  source: 'sec', kind: 'question',
  id: 'bio-2025-hl-q6-ab', subjectId: 'biology', level: 'higher',
  topicId: 'biology-2-3', conceptId: 'digestive-parts',
  year: 2025, paperFileid: 'LC025ALP038EV', section: 'A',
  questionRef: '2025 HL Q6(a)–(b)',
  questionText: 'Name the parts labelled A and B.',
  tariffModel: { kind: 'fixed' }, totalMarks: 4,
  rows: [row({ id: 'r0', verbatim: 'Oesophagus', marks: 2 }), row({ id: 'r1', verbatim: 'Stomach', marks: 2 })],
  schemeCitation: 'SEC marking scheme, Biology 2025 Higher Level — © State Examinations Commission',
  specVersion: 'lc-biology-2002',
  qa: { gates: [], humanReviewedBy: 'al', humanReviewedAt: '2026-07-30' },
  ...o,
} as SecCard);

const renderSession = (cards: SecCard[]) => {
  const onGrade = vi.fn();
  const onFinish = vi.fn();
  const onExit = vi.fn();
  const utils = render(
    <SessionScreen
      cards={cards} subjectLabel="Biology"
      onGrade={onGrade} onFinish={onFinish} onExit={onExit}
    />,
  );
  return { ...utils, onGrade, onFinish, onExit };
};

/* ------------------------------------------------------------ mark logic ---- */

describe('mark arithmetic follows the scheme, not a convenient default', () => {
  test('sums a fixed tariff from its rows', () => {
    expect(claimableTotal(card())).toBe(4);
  });

  test('a best-N-of-parts card counts only the claimable subset', () => {
    const rows = Array.from({ length: 6 }, (_, i) => row({ id: `r${i}`, verbatim: `p${i}`, marks: 4 }));
    const c = card({ tariffModel: { kind: 'bestNofParts', answer: 5, ofParts: 6, perPart: 4 }, totalMarks: 20, rows });
    // Six rows at 4m would read as 24 on a 20-mark question.
    expect(claimableTotal(c)).toBe(20);
    expect(showsRowMarks(c)).toBe(false);
  });

  test('an order-dependent split shows no per-row marks at all', () => {
    const c = card({ tariffModel: { kind: 'orderedSplit', notation: '2(5) + 5(2)' }, totalMarks: 20 });
    expect(showsRowMarks(c)).toBe(false);
  });

  test('an asterisked row carries its real marks', () => {
    // The SEC asterisk means the exact term is required, not that the row is
    // worth nothing: the 2025 scheme awards "A: *Sporangium 1".
    expect(rowMarks(row({ kind: 'gate', marks: 1 }))).toBe(1);
  });

  test('an anyN group is worth its claimable maximum in total', () => {
    expect(rowMarks(row({ kind: 'anyN', marks: null, group: { claimMax: 4, perOption: 3, options: ['a', 'b', 'c', 'd', 'e'] } }))).toBe(12);
  });

  test('an anyN group scores by how many options the student actually had', () => {
    // Treating "Any four 4(3)" as one tick makes a 12-mark row all-or-nothing and
    // leaves a student who had two of them no way to say so.
    const c = card({
      totalMarks: 12,
      rows: [row({ id: 'g', kind: 'anyN', marks: null, group: { claimMax: 4, perOption: 3, options: ['a', 'b', 'c', 'd', 'e'] } })],
    });
    expect(marksClaimed(c, {}, { g: [0, 1] })).toBe(6);
    expect(marksClaimed(c, {}, { g: [0, 1, 2, 3] })).toBe(12);
    // Never more than the examiner marks, however many are ticked.
    expect(marksClaimed(c, {}, { g: [0, 1, 2, 3, 4] })).toBe(12);
  });

  test('an unclaimed asterisked row costs only its own marks', () => {
    // It does not zero the rest of the question — each asterisked item stands or
    // falls alone, per the scheme's own preamble.
    const c = card({
      totalMarks: 5,
      rows: [row({ id: 'g', kind: 'gate', verbatim: 'Sporangium', marks: 1, exactTermRequired: true }), row({ id: 'r1', verbatim: 'Stomach', marks: 4 })],
    });
    expect(marksClaimed(c, { g: 'no', r1: 'yes' })).toBe(4);
    expect(marksClaimed(c, { g: 'yes', r1: 'yes' })).toBe(5);
  });

  test('mutually exclusive routes cannot be mixed', () => {
    // Chemistry's double solidus: "a partial answer from one side of the // may
    // not be taken in conjunction with a partial answer from the other side."
    const c = card({
      totalMarks: 6,
      rows: [
        row({ id: 'a1', verbatim: 'Route A first point', marks: 3, route: 'a' }),
        row({ id: 'a2', verbatim: 'Route A second point', marks: 3, route: 'a' }),
        row({ id: 'b1', verbatim: 'Route B first point', marks: 3, route: 'b' }),
        row({ id: 'b2', verbatim: 'Route B second point', marks: 3, route: 'b' }),
      ],
    });
    expect(committedRoute(c, { a1: 'yes' })).toBe('a');
    // Both of route A scores in full.
    expect(marksClaimed(c, { a1: 'yes', a2: 'yes' })).toBe(6);
    // Mixing sides earns nothing extra — the far side is not credited.
    expect(marksClaimed(c, { a1: 'yes', b1: 'yes', b2: 'yes' })).toBe(3);
  });

  test('a card with no routes is unaffected', () => {
    expect(committedRoute(card(), { r0: 'yes' })).toBe(null);
    expect(marksClaimed(card(), { r0: 'yes', r1: 'yes' })).toBe(4);
  });

  test('the reachable total counts the routes once, not both', () => {
    // Summing every row states a total no student can reach, and then tells one
    // who answered a full route perfectly that they left half the marks behind.
    const c = card({
      totalMarks: 6,
      rows: [
        row({ id: 'a1', verbatim: 'Route A first point', marks: 3, route: 'a' }),
        row({ id: 'a2', verbatim: 'Route A second point', marks: 3, route: 'a' }),
        row({ id: 'b1', verbatim: 'Route B, in one step', marks: 6, route: 'b' }),
      ],
    });
    expect(claimableTotal(c)).toBe(6);
    expect(tariffReconciles(c)).toBe(true);
    // A row outside both routes is claimable whichever route is taken.
    const withCommon = card({
      totalMarks: 8,
      rows: [
        row({ id: 'r0', verbatim: 'Claimable either way', marks: 2 }),
        row({ id: 'a1', verbatim: 'Route A', marks: 6, route: 'a' }),
        row({ id: 'b1', verbatim: 'Route B', marks: 6, route: 'b' }),
      ],
    });
    expect(claimableTotal(withCommon)).toBe(8);
    expect(tariffReconciles(withCommon)).toBe(true);
  });

  test('a route that cannot reach the tariff fails the check', () => {
    // Each route must be a complete answer on its own. One that falls short is a
    // transcription error, not a cheaper way to the same marks.
    expect(tariffReconciles(card({
      totalMarks: 6,
      rows: [
        row({ id: 'a1', verbatim: 'Route A', marks: 6, route: 'a' }),
        row({ id: 'b1', verbatim: 'Route B, short', marks: 3, route: 'b' }),
      ],
    }))).toBe(false);
  });

  test('a synonym claim earns the mark', () => {
    expect(marksClaimed(card(), { r0: 'synonym', r1: 'no' })).toBe(2);
  });
});

describe('the suggested grade', () => {
  test('says Got it when every mark was claimed, even on a first encounter', () => {
    // Regression: an override used to force Shaky on a card's first showing, so a
    // student who claimed 12 of 12 marks was told "that looks like Shaky" directly
    // beneath "ALL 12 MARKS. NOTHING LEFT BEHIND." FSRS learning steps already
    // stop a single pass buying a long interval, so the override bought nothing.
    expect(suggestGrade(card(), { r0: 'yes', r1: 'yes' })).toBe('got');
  });

  test('follows the marks', () => {
    expect(suggestGrade(card(), { r0: 'yes', r1: 'no' })).toBe('shaky');
    expect(suggestGrade(card(), { r0: 'no', r1: 'no' })).toBe('missed');
  });
});

/* -------------------------------------------------------------- the screen -- */

describe('the question comes first and stays', () => {
  test('shows the verbatim question, the tariff and the provenance before any reveal', () => {
    renderSession([card()]);
    expect(screen.getByText('Name the parts labelled A and B.')).toBeInTheDocument();
    expect(screen.getByText('4m')).toBeInTheDocument();
    expect(screen.getByText(/BIOLOGY · HIGHER LEVEL · 2025/i)).toBeInTheDocument();
  });

  test('hides the scheme until the student asks for it', () => {
    renderSession([card()]);
    expect(screen.queryByText('Oesophagus')).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    expect(screen.getByText('Oesophagus')).toBeInTheDocument();
  });

  test('keeps the question on screen after the reveal, because a flip would hide it', () => {
    // Judging yourself against an answer you can no longer see is the foresight
    // bias that inflates self-assessment.
    renderSession([card()]);
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    expect(screen.getByText('Name the parts labelled A and B.')).toBeInTheDocument();
  });

  test('always credits the marking scheme', () => {
    renderSession([card()]);
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    expect(screen.getByText(/State Examinations Commission/)).toBeInTheDocument();
  });
});

describe('claiming marks', () => {
  test('rows start unclaimed, so overconfidence takes an action rather than an omission', () => {
    renderSession([card()]);
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    expect(screen.getByRole('button', { name: /Oesophagus/ })).toHaveAttribute('aria-pressed', 'false');
    expect(screen.getByText(/Not claimed yet/i)).toBeInTheDocument();
  });

  test('one tap claims a row and the marks-left figure falls', () => {
    renderSession([card()]);
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    fireEvent.click(screen.getByRole('button', { name: /Oesophagus/ }));
    expect(screen.getByRole('button', { name: /Oesophagus/ })).toHaveAttribute('aria-pressed', 'true');
    expect(screen.getByText(/You claimed 2 of 4 marks/)).toBeInTheDocument();
  });

  test('the marks-left figure settles on the right number', async () => {
    // It counts DOWN as marks are claimed, so a stuck animation would leave a
    // wrong number on screen — the one thing this strip must never do.
    renderSession([card()]);
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    fireEvent.click(screen.getByRole('button', { name: /Oesophagus/ }));
    // The label is its own span; the count lives beside it, so read the band.
    const strip = screen.getByText(/Not claimed yet/i).parentElement!;
    await waitFor(() => expect(strip.textContent).toMatch(/\b2\b/), { timeout: 1000 });
  });

  test('the marks-left figure can never exceed the marks on the card', async () => {
    // Regression: the count-down animation seeded its clock from
    // performance.now() while receiving rAF's own timestamp. Where those epochs
    // differ, progress went negative, the easing inverted, and a 9-mark card
    // displayed "11 marks left behind" — a number the card cannot produce.
    const c = card({
      totalMarks: 9,
      rows: [
        row({ id: 'g-a', kind: 'gate', verbatim: 'A — Sporangium', marks: 0, exactTermRequired: true }),
        row({ id: 'r-fn', verbatim: 'One function of C — spreads the fungus', marks: 3 }),
        row({ id: 'r-nut', kind: 'alt', verbatim: 'Method of nutrition — saprophytic', marks: 6 }),
      ],
    });
    renderSession([c]);
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    fireEvent.click(screen.getByRole('button', { name: /A — Sporangium/ }));
    fireEvent.click(screen.getByRole('button', { name: /One function of C/ }));
    const strip = screen.getByText(/Not claimed yet/i).parentElement!;
    await waitFor(() => {
      // The count, not the named points beside it.
      const n = Number(/·\s*(\d+)\s*marks?/.exec(strip.textContent || '')?.[1]);
      expect(n).toBe(6);
    }, { timeout: 1500 });
  });

  test('shows the scheme\'s own accepted alternatives, not just the first word', () => {
    const c = card({
      totalMarks: 6,
      rows: [row({ id: 'r0', kind: 'alt', verbatim: 'saprophytic', marks: 6, accepts: ['heterotrophic'] })],
    });
    renderSession([c]);
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    expect(screen.getByText(/heterotrophic/)).toBeInTheDocument();
  });

  test('"I had them all" claims every row at once', () => {
    renderSession([card()]);
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    fireEvent.click(screen.getByRole('button', { name: /I had them all/i }));
    expect(screen.getByText(/Nothing left behind/i)).toBeInTheDocument();
  });

  test('an asterisked row offers no synonym escape, and says nothing about why', () => {
    // The asterisk is marking-scheme mechanics. It changes what the tool accepts;
    // it is not a caption for the student to read and act on.
    const c = card({
      totalMarks: 4,
      rows: [row({ id: 'g', kind: 'gate', verbatim: 'Sporangium', marks: 1, exactTermRequired: true }), row({ id: 'r1', verbatim: 'Stomach', marks: 3 })],
    });
    renderSession([c]);
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    expect(screen.queryByText(/exact term/i)).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /I had something like this/i })).not.toBeInTheDocument();
  });

  test('an open-ended list lets a correct student say so', () => {
    // The scheme's ellipsis means the list is not exhaustive; a student who
    // wrote "cartilage" was right and must not be told otherwise.
    const c = card({ rows: [row({ id: 'r0', verbatim: 'muscles or tendons or ligament', marks: 4, openList: true })], totalMarks: 4 });
    renderSession([c]);
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    fireEvent.click(screen.getByRole('button', { name: /I had something like this/i }));
    expect(screen.getByText(/accepts synonyms here/i)).toBeInTheDocument();
  });

  test('a dependent row cannot be claimed until the row it rests on is', () => {
    const c = card({
      totalMarks: 6,
      rows: [row({ id: 'r0', verbatim: 'X — the neuron', marks: 2 }), row({ id: 'r1', verbatim: 'Justify: it is connected to a muscle cell', marks: 4, dependsOn: 'r0' })],
    });
    renderSession([c]);
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    expect(screen.getByRole('button', { name: /Justify/ })).toBeDisabled();
    fireEvent.click(screen.getByRole('button', { name: /X — the neuron/ }));
    expect(screen.getByRole('button', { name: /Justify/ })).not.toBeDisabled();
  });

  test('lets a student claim options inside an "Any four" group one by one', () => {
    const c = card({
      totalMarks: 12,
      rows: [row({
        id: 'g', kind: 'anyN', verbatim: 'Any four of the following', marks: null,
        group: { claimMax: 4, perOption: 3, options: ['zygospore formed', 'diploid nuclei formed', 'gametangium formed', 'progametangia are formed', 'survives adverse conditions'] },
      })],
    });
    renderSession([c]);
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    expect(screen.getByText(/Any 4 of these — 3 marks each/)).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /zygospore formed/ }));
    fireEvent.click(screen.getByRole('button', { name: /diploid nuclei formed/ }));
    expect(screen.getByText(/You claimed 6 of 12 marks/)).toBeInTheDocument();
  });

  test('stops a student claiming more of a group than the examiner marks', () => {
    const c = card({
      totalMarks: 6,
      rows: [row({
        id: 'g', kind: 'anyN', verbatim: 'Any two', marks: null,
        group: { claimMax: 2, perOption: 3, options: ['alpha', 'beta', 'gamma'] },
      })],
    });
    renderSession([c]);
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    fireEvent.click(screen.getByRole('button', { name: /alpha/ }));
    fireEvent.click(screen.getByRole('button', { name: /beta/ }));
    expect(screen.getByRole('button', { name: /gamma/ })).toBeDisabled();
    expect(screen.getByText(/any more score nothing/i)).toBeInTheDocument();
  });

  test('locks the route not taken, and says why', () => {
    const c = card({
      totalMarks: 6,
      rows: [
        row({ id: 'a1', verbatim: 'Oxidation route', marks: 6, route: 'a' }),
        row({ id: 'b1', verbatim: 'Reduction route', marks: 6, route: 'b' }),
      ],
    });
    renderSession([c]);
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    expect(screen.getByRole('button', { name: /Reduction route/ })).not.toBeDisabled();
    fireEvent.click(screen.getByRole('button', { name: /Oxidation route/ }));
    expect(screen.getByRole('button', { name: /Reduction route/ })).toBeDisabled();
    expect(screen.getByText(/one route or the other/i)).toBeInTheDocument();
  });

  test('shows no per-row mark chips when the scheme does not define them', () => {
    const c = card({ tariffModel: { kind: 'orderedSplit', notation: '2(5) + 5(2)' }, totalMarks: 20 });
    renderSession([c]);
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    expect(screen.queryByText('−2m')).not.toBeInTheDocument();
    expect(screen.getByText(/depends on how many you got/i)).toBeInTheDocument();
  });
});

describe('a diagram card always decodes its figure', () => {
  test('shows every label, including the ones this question never asked about', () => {
    const diagram: SecDiagramCard = {
      ...card(),
      kind: 'diagram',
      figure: {
        candId: 'cand_1', src: '/exam-figures/biology/x.png', srcHash: 'h',
        alt: 'Digestive tract with lettered leader lines',
        lettersVisible: ['A', 'B', 'C'], attribution: 'SEC Biology 2025 HL Q6',
      },
      labelKey: [
        { letter: 'A', meaning: 'Oesophagus', askedInThisQuestion: true },
        { letter: 'B', meaning: 'Stomach', askedInThisQuestion: true },
        { letter: 'C', meaning: 'Small intestine', askedInThisQuestion: false },
      ],
    };
    renderSession([diagram]);
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    const key = screen.getByText(/Also on the diagram/i).parentElement!;
    // C is on the diagram but this question never asks about it, so the panel
    // explains it — that is the whole reason the panel exists.
    expect(within(key).getByText(/Small intestine/)).toBeInTheDocument();
    // A and B ARE asked, and they are the marking points the student is about to
    // self-mark. Repeating them here printed the answer twice, directly beneath
    // itself, and gave away the rows the panel sits under.
    expect(within(key).queryByText(/Oesophagus/)).toBeNull();
    expect(within(key).queryByText(/Stomach/)).toBeNull();
    // The figure carries its attribution.
    expect(screen.getByAltText(/Digestive tract/)).toBeInTheDocument();
  });

  test('the label panel disappears when it has nothing the question left alone', () => {
    const diagram: SecDiagramCard = {
      ...card(),
      kind: 'diagram',
      figure: {
        candId: 'cand_2', src: '/exam-figures/biology/y.png', srcHash: 'h2',
        alt: 'Two lettered structures',
        lettersVisible: ['A', 'B'], attribution: 'SEC Biology 2025 HL Q6',
      },
      labelKey: [
        { letter: 'A', meaning: 'Oesophagus', askedInThisQuestion: true },
        { letter: 'B', meaning: 'Stomach', askedInThisQuestion: true },
      ],
    };
    renderSession([diagram]);
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    expect(screen.queryByText(/Also on the diagram/i)).toBeNull();
  });
});

describe('grading', () => {
  test('offers all three grades and lets the student overrule the suggestion', () => {
    const { onGrade } = renderSession([card()]);
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    fireEvent.click(screen.getByRole('button', { name: /I had them all/i }));
    for (const label of ['Missed it', 'Shaky', 'Got it']) {
      expect(screen.getByRole('button', { name: label })).toBeEnabled();
    }
    fireEvent.click(screen.getByRole('button', { name: 'Missed it' }));
    expect(onGrade).toHaveBeenCalledWith(expect.objectContaining({ grade: 'missed', marksClaimed: 4, marksAvailable: 4 }));
  });

  test('says the decision is the student\'s', () => {
    renderSession([card()]);
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    expect(screen.getByText(/You decide\. Tap any of the three\./)).toBeInTheDocument();
  });

  test('marks the suggestion with shape, never with colour', () => {
    renderSession([card()]);
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    fireEvent.click(screen.getByRole('button', { name: /I had them all/i }));
    const suggestedBtn = screen.getByRole('button', { name: 'Got it' });
    expect(suggestedBtn).toHaveAttribute('data-suggested');
    // Every grade button keeps the same neutral surface — no green "right" button.
    for (const label of ['Missed it', 'Shaky', 'Got it']) {
      const style = screen.getByRole('button', { name: label }).getAttribute('style') || '';
      expect(style).toMatch(/background:\s*(rgb\(255,\s*255,\s*255\)|#FFFFFF|white)/i);
    }
  });

  test('never renders "Missed it" in red', () => {
    renderSession([card()]);
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    const style = screen.getByRole('button', { name: 'Missed it' }).getAttribute('style') || '';
    expect(style).not.toMatch(/red|#e\d|#f00|rgb\(2[0-5]\d,\s*[0-5]\d,/i);
  });

  test('never makes a success read like a punishment', () => {
    // A first encounter graded well still returns within the hour — that is the
    // FSRS learning step consolidating, not a penalty. Said plainly it would read
    // as being punished for getting it right, so the words must reframe it.
    render(
      <SessionScreen
        cards={[card(), card({ id: 'bio-q7', questionText: 'Second.' })]}
        subjectLabel="Biology"
        onGrade={() => 'before you finish today'}
        onExit={() => undefined}
        onFinish={() => undefined}
      />,
    );
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    fireEvent.click(screen.getByRole('button', { name: /I had them all/i }));
    fireEvent.click(screen.getByRole('button', { name: 'Got it' }));

    const whisper = screen.getByText(/one more look|Nice\.|No bother/).textContent || '';
    expect(whisper).not.toMatch(/No bother/);
    expect(whisper).toMatch(/one more look before you finish today, then it starts spacing out/);
  });

  test('finishes the session and reports every result', () => {
    const { onFinish } = renderSession([card()]);
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    fireEvent.click(screen.getByRole('button', { name: 'Got it' }));
    expect(onFinish).toHaveBeenCalledWith([expect.objectContaining({ cardId: 'bio-2025-hl-q6-ab', grade: 'got' })]);
  });

  test('a missed card really does come back, even when it is not the last one', () => {
    // Regression: the re-queued card was appended and then discarded by a
    // "finished" heuristic unless it happened to be last, silently killing the
    // one mechanic that brings a failed card back.
    const three = [card(), card({ id: 'bio-q7', questionText: 'Second.' }), card({ id: 'bio-q8', questionText: 'Third.' })];
    const { onFinish } = renderSession(three, {});
    // Miss the first, then answer the other two.
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    fireEvent.click(screen.getByRole('button', { name: 'Missed it' }));
    for (const q of ['Second.', 'Third.']) {
      expect(screen.getByText(q)).toBeInTheDocument();
      fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
      fireEvent.click(screen.getByRole('button', { name: 'Got it' }));
    }
    // The missed card must be served again before the session can end.
    expect(onFinish).not.toHaveBeenCalled();
    expect(screen.getByText('Name the parts labelled A and B.')).toBeInTheDocument();
  });

  test('an asterisked row shows the marks it is worth', () => {
    // Regression: gate rows were treated as worth zero, so their chip was
    // suppressed — but the scheme awards "A: *Sporangium 1".
    const c = card({
      totalMarks: 4,
      rows: [row({ id: 'g', kind: 'gate', verbatim: 'Sporangium', marks: 1, exactTermRequired: true }), row({ id: 'r1', verbatim: 'Stomach', marks: 3 })],
    });
    renderSession([c]);
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    // Shown as what the point is WORTH, not as a deduction. An unclaimed row used
    // to render "−1m" in the accent tint, so revealing a card greeted the student
    // with a column of orange minus signs before they had touched anything.
    expect(screen.getByText('1m')).toBeInTheDocument();
  });

  test('reports no total for a card whose scheme defines no per-row marks', () => {
    // Otherwise the close screen reads "0 of 20 marks" for a card the student
    // may have answered perfectly.
    const c = card({ tariffModel: { kind: 'orderedSplit', notation: '2(5) + 5(2)' }, totalMarks: 20 });
    const { onGrade } = renderSession([c]);
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    fireEvent.click(screen.getByRole('button', { name: 'Got it' }));
    expect(onGrade).toHaveBeenCalledWith(expect.objectContaining({ marksClaimed: 0, marksAvailable: 0 }));
  });

  test('a missed card comes back later in the same sitting', () => {
    const two = [card(), card({ id: 'bio-2025-hl-q7', questionText: 'Second question.' })];
    const { onFinish } = renderSession(two);
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    fireEvent.click(screen.getByRole('button', { name: 'Missed it' }));
    // Still going: the missed card was re-queued rather than the session ending.
    expect(onFinish).not.toHaveBeenCalled();
    expect(screen.getByText('Second question.')).toBeInTheDocument();
  });

  test('leaving mid-session is safe because grades commit per card', () => {
    const { onGrade, onExit } = renderSession([card(), card({ id: 'bio-q7', questionText: 'Second.' })]);
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    fireEvent.click(screen.getByRole('button', { name: 'Got it' }));
    expect(onGrade).toHaveBeenCalledTimes(1);
    fireEvent.click(screen.getByRole('button', { name: /^Leave$/i }));
    expect(onExit).toHaveBeenCalled();
  });
});

/* ------------------------------------------------------- design guardrails -- */

describe('design rules that carry meaning', () => {
  const source = readFileSync(resolve(__dirname, '..', 'components/MarkBank/SessionScreen.tsx'), 'utf8');

  test('carries no decorative colour field — surfaces stay plain until designed', () => {
    expect(source).not.toMatch(/#123B2B|environmentColor/);
  });

  test('no banned surfaces: warm cream, coloured left borders, gradients or emoji', () => {
    expect(source).not.toMatch(/#FDF8F0|#FAF7F4|#F9F9F7/i);
    expect(source).not.toMatch(/borderLeft(?!Radius)|border-l-4/);
    expect(source).not.toMatch(/linear-gradient|backdrop-filter/);
    expect(source).not.toMatch(/[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}]/u);
  });

  test('the grade bar is solid, never translucent glass over the colour field', () => {
    // Blurred or translucent white over a saturated ground goes muddy and is a
    // reliable tell of generated UI. Translucent white is fine ON the
    // environment itself — the progress rail and counter use it correctly —
    // so this checks the fixed bar's own surface rather than banning the value.
    const bar = source.slice(source.indexOf("position: 'fixed'"));
    expect(bar).toMatch(/background:\s*'#FFFFFF'/);
    expect(bar.slice(0, bar.indexOf('</div>'))).not.toMatch(/rgba\(255,\s*255,\s*255,\s*0\.\d/);
    expect(source).not.toMatch(/backdrop-filter|backdropFilter/);
  });

  test('marks are set in the mono face so a tariff can never be mistaken for a word', () => {
    expect(source).toMatch(/MONO/);
  });

  test('respects a reduced-motion preference', () => {
    expect(source).toMatch(/useReducedMotion/);
  });

  test('the safe area is honoured, so the grade bar clears the home indicator', () => {
    expect(source).toMatch(/--sab/);
  });
});
