import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import SessionScreen, { marksClaimed, showsRowMarks } from '../components/MarkBank/SessionScreen';
import LanguageRubricPanel from '../components/MarkBank/LanguageRubricPanel';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import { languageMarks, languageScoreId, languageGroupId, languageRowId, languageFlagId, languageLengthId, languageOtherLanguageId } from '../components/MarkBank/languageScoring';
import { isRubricCard, tariffReconciles } from '../types/markBank';

const sitting = REVIEWED_CARDS.filter(card => card.year === 2021 && card.level === 'higher');
function get(suffix: string) {
  const card = sitting.find(item => item.id === `ru-2021-hl-${suffix}`);
  if (!card) throw new Error(suffix);
  return card;
}
function points(suffix: string) {
  const card = get(suffix);
  if (!isRubricCard(card) || card.rubric.system !== 'language-points') throw new Error(suffix);
  return { ...card, rubric: card.rubric };
}
function writing() {
  const card = get('gw');
  if (!isRubricCard(card) || card.rubric.system !== 'language-writing') throw new Error('gw');
  return { ...card, rubric: card.rubric };
}
function confidence() {
  const card = get('se');
  if (isRubricCard(card)) throw new Error('se');
  return card;
}
const row = (group: string, id = 'full') => ({ [languageGroupId(group)]: 1, [languageRowId(group, id)]: 1 });
const detail = (n: number, mark: number) => ({ [languageGroupId(`detail-${n}`)]: 1, [languageScoreId(`detail-${n}-credit`)]: mark });
afterEach(cleanup);

describe('Russian 2021 Higher original tasks and source-specific scoring', () => {
  it('represents all 41 source asks, retaining 290 priced practice marks and one complete confidence task', () => {
    expect(sitting).toHaveLength(41);
    expect(sitting.every(tariffReconciles)).toBe(true);
    expect(sitting.filter(isRubricCard).reduce((sum, card) => sum + card.totalMarks, 0)).toBe(290);
    expect(sitting.filter(card => card.audioMaterial)).toHaveLength(20);
    expect(sitting.filter(card => card.answerLanguageRule)).toHaveLength(16);
    expect(confidence().totalMarks).toBe(30);
  });

  it('counts the two published school-year wordings as one fact, with separate age and city details', () => {
    const card = points('c1-1-ii');
    const both = { ...row('school-year', 'final-year'), ...row('school-year', 'second-last-year') };
    expect(languageMarks(card, both)).toBe(2);
    for (const alternative of ['final-year', 'second-last-year']) {
      expect(languageMarks(card, { ...row('answer-1'), ...row('school-year', alternative) })).toBe(4);
    }
    expect(languageMarks(card, { ...both, ...row('answer-1'), ...row('answer-3') })).toBe(4);
    render(<LanguageRubricPanel card={card} scores={both} onScore={vi.fn()} />);
    expect(screen.getByText(/Both published school-year wordings remain available/)).toBeVisible();
    expect(screen.getByText(/Second last year in school/)).toBeVisible();
    expect(screen.getByText(/11th grade\/form\/year/)).toBeVisible();
  });

  it('requires one advantage and one disadvantage, keeping both alternative advantages', () => {
    const card = points('c1-3-iii');
    const advantages = { ...row('advantage', 'option-1'), ...row('advantage', 'option-2') };
    expect(languageMarks(card, advantages)).toBe(2);
    expect(languageMarks(card, { ...advantages, ...row('disadvantage') })).toBe(4);
    expect(card.rubric.groups.map(group => group.rows.length)).toEqual([2, 1]);
  });

  it('retains the comprehension quota and source cross-question duplicate-credit instruction', () => {
    for (const suffix of ['c1-1-i', 'c1-2-i', 'c1-2-ii', 'c1-3-i', 'c1-3-ii', 'c1-4-i', 'c1-4-ii']) {
      const card = points(suffix);
      expect(languageMarks(card, Object.assign({}, ...card.rubric.groups.map(group => row(group.id))))).toBe(card.totalMarks);
      expect(card.rubric.groups.every(group => group.rows[0].marks === 2 && !group.rows[0].steps)).toBe(true);
      expect(card.rubric.taskRequirements.join(' ')).toContain('accept the one which gives the candidate the most marks');
    }
  });

  it('keeps 22 literal music entries but only 21 distinct claims under the ten-word limit', () => {
    const card = points('ca1');
    expect(card.rubric.groups).toHaveLength(21);
    expect(card.rubric.groups.filter(group => group.rows[0].text === 'синтезатор')).toHaveLength(1);
    expect(languageMarks(card, Object.assign({}, ...card.rubric.groups.map(group => row(group.id))))).toBe(10);
    expect(card.topicId).toBe('russian-2-0');
    expect(card.additionalTopicIds).toEqual(['russian-1-1', 'russian-0-5']);
    render(<LanguageRubricPanel card={card} scores={{}} onScore={vi.fn()} />);
    expect(screen.getByText(/No mark for YouTube \(In English or Russian\)/)).toBeVisible();
    expect(screen.getByText(/The printed list repeats синтезатор/)).toBeVisible();
  });

  it('caps only summary discretion when a required certain or uncertain aspect is omitted', () => {
    const card = points('c2-1');
    const saved = { ...detail(1, 2), ...detail(2, 2), ...detail(3, 2), ...detail(4, 2), [languageScoreId('summary-skills')]: 2 };
    expect(languageMarks(card, saved)).toBe(10);
    const flagged = { ...saved, [languageFlagId('missing-certain-or-uncertain')]: 1 };
    expect(languageMarks(card, flagged)).toBe(9);
    expect(languageMarks(card, { ...flagged, [languageFlagId('missing-certain-or-uncertain')]: 0 })).toBe(10);
    expect(languageMarks(card, { ...detail(1, 1), [languageFlagId('missing-certain-or-uncertain')]: 1 })).toBe(1);
    render(<LanguageRubricPanel card={card} scores={flagged} onScore={vi.fn()} />);
    expect(screen.getAllByText(/at least one uncertain and one certain aspect/)[0]).toBeVisible();
  });

  it.each([1, 2, 3, 4])('keeps summary %i manual discretion available under the literal Russian-word exception and its cap', number => {
    const card = points(`c2-${number}`);
    const saved = { ...detail(1, 1), ...detail(2, 2), ...detail(3, 2), ...detail(4, 2), [languageScoreId('summary-skills')]: 2 };
    expect(languageMarks(card, saved)).toBe(9);
    const other = { ...saved, [languageOtherLanguageId('response')]: 1 };
    expect(languageMarks(card, other)).toBe(2);
    expect(languageMarks(card, { ...other, [languageFlagId('incomplete-response')]: 1 })).toBe(1);
    expect(languageMarks(card, { ...other, [languageOtherLanguageId('response')]: 0 })).toBe(9);
    render(<LanguageRubricPanel card={card} scores={other} onScore={vi.fn()} />);
    expect(screen.getAllByText(/Discretionary marks \(as opposed to content marks\) may be awarded/)[0]).toBeVisible();
    expect(screen.getAllByText(/intelligible to a monolingual speaker of English/)[0]).toBeVisible();
    expect(screen.getByText(/The original Q2.1 heading prints 50 marks/)).toBeVisible();
    expect(screen.getByText(/Irish is not a disallowed answer language/)).toBeVisible();
  });

  it('retains the five original case answers and both literal infinitive language clauses', () => {
    for (const suffix of ['la1', 'la2-i', 'la2-ii']) {
      const card = points(suffix);
      expect(card.rubric.groups).toHaveLength(5);
      expect(card.answerLanguageRule).toBeUndefined();
      expect(languageMarks(card, Object.assign({}, ...card.rubric.groups.map(group => row(group.id))))).toBe(10);
    }
    const infinitives = points('la2-i');
    expect(infinitives.rubric.groups.map(group => group.rows[0].text)).toEqual(['понял — понять', 'хочу — хотеть', 'повлияли — повлиять', 'перешёл — перейти', 'сомневаюсь — сомневаться']);
    render(<LanguageRubricPanel card={infinitives} scores={{}} onScore={vi.fn()} />);
    expect(screen.getByText(/You may write your answer in Irish, English or Russian/)).toBeVisible();
    expect(screen.getByText(/Do not assign any marks where candidates translate the phrases into English/)).toBeVisible();
    expect(points('la2-ii').rubric.markingGuideNote).toContain('repeating the first Irish label');
  });

  it('keeps ten matches and fifteen native grammar forms without a second claim for the first slash alternative', () => {
    const matching = points('sd');
    expect(matching.rubric.groups.map(group => group.rows[0].text.split(' — ')[0])).toEqual(['8', '10', '4', '7', '9', '2', '6', '5', '3', '1']);
    expect(languageMarks(matching, Object.assign({}, ...matching.rubric.groups.map(group => row(group.id))))).toBe(20);
    const grammar = points('gr');
    expect(grammar.rubric.groups.map(group => group.rows[0].text)).toEqual(['увлекалась/увлекается', 'искусством', 'получила', 'её', 'новым', 'учебном', 'заведении', 'могла', 'соревнованиях', 'международной', 'арене', 'кулинарией', 'любимому', 'друзьями', 'своей']);
    expect(languageMarks(grammar, row('answer-1'))).toBe(2);
    expect(languageMarks(grammar, Object.assign({}, ...grammar.rubric.groups.map(group => row(group.id))))).toBe(30);
  });

  it('retains the original writing range and overlap with no automatic minimum or invented one-mark deduction', () => {
    const card = writing();
    const saved = { [languageScoreId('content')]: 15, [languageScoreId('expression')]: 15, [languageScoreId('coherence')]: 10, [languageLengthId('words')]: 140 };
    expect(languageMarks(card, saved)).toBe(40);
    expect(languageMarks(card, { ...saved, [languageFlagId('lower-a')]: 1 })).toBe(37);
    expect(languageMarks(card, { ...saved, [languageFlagId('lower-a')]: 1, [languageScoreId('expression')]: 6 })).toBe(25);
    expect(languageMarks(card, { ...saved, [languageScoreId('soft-sign-penalty')]: 2 })).toBe(38);
    expect(languageMarks(card, { ...saved, [languageScoreId('soft-sign-penalty')]: 1 })).toBe(40);
    expect(languageMarks(card, { ...saved, [languageScoreId('content')]: 7 })).toBe(27);
    render(<LanguageRubricPanel card={card} scores={{ ...saved, [languageFlagId('lower-a')]: 1 }} onScore={vi.fn()} />);
    expect(screen.getAllByText(/Lower A Expression 11-12/)[0]).toHaveTextContent('9-11');
    expect(card.rubric.criteria[1].limits?.find(limit => limit.id === 'lower-a')?.bands).toBeUndefined();
  });

  it('keeps listening Boat as the named one-mark option and Channels as zero guidance', () => {
    const card = points('l3-1-i');
    expect(languageMarks(card, row('answer-3'))).toBe(1);
    expect(languageMarks(card, { ...row('answer-1'), ...row('answer-2'), ...row('answer-3') })).toBe(2);
    expect(card.rubric.taskRequirements.join(' ')).toContain('No marks for Channels');
    expect(card.answerLanguageRule).toBeUndefined();
  });

  it('uses the explicit four-mark English-language crew answer despite the two-detail prompt', () => {
    const card = points('l3-2');
    expect(card.rubric.groups).toHaveLength(1);
    expect(languageMarks(card, row('answer-1'))).toBe(4);
    expect(card.rubric.markingGuideNote).toContain('1 x 4 marks');
    expect(card.rubric.markingGuideNote).toContain('original prompt asks for two details');
  });

  it('keeps Economics alone exclusive to its full education detail and permits a distinct second fact', () => {
    const card = points('l4-1-i');
    const partial = row('answer-3', 'economics-only');
    expect(languageMarks(card, partial)).toBe(1);
    expect(languageMarks(card, { ...partial, ...row('answer-3') })).toBe(2);
    expect(languageMarks(card, { ...partial, ...row('answer-1') })).toBe(3);
    expect(languageMarks(card, { ...partial, ...row('answer-3'), ...row('answer-1') })).toBe(4);
  });

  it('preserves each plus-linked listening answer as one complete two-mark response', () => {
    const training = points('l2-2-i').rubric.groups.flatMap(group => group.rows).find(item => item.text.includes('training twice a week + on Tuesdays and Thursdays'));
    expect(training?.marks).toBe(2); expect(training?.steps).toBeUndefined();
    const advice = points('l4-3').rubric.groups.flatMap(group => group.rows);
    for (const phrase of ['Don’t focus on one topic only + try different things', 'Try to improve the picture + photo and video content']) {
      const item = advice.find(answer => answer.text.includes(phrase));
      expect(item?.marks).toBe(2); expect(item?.steps).toBeUndefined();
    }
    for (const card of sitting.filter(item => item.audioMaterial)) {
      expect(card.answerLanguageRule).toBeUndefined();
      if (!isRubricCard(card) || card.rubric.system !== 'language-points') throw new Error('Listening source tariff must remain language-points');
      expect(card.rubric.taskRequirements.join(' ')).toContain('Accept answers written in Russian');
    }
  });

  it('keeps the complete five-choice essay unpriced with the literal ambiguous deduction', () => {
    const card = confidence();
    expect(card.tariffModel).toEqual({ kind: 'questionTotal' });
    expect(card.rows.every(item => item.marks === null)).toBe(true);
    expect(card.questionText.match(/•/g)).toHaveLength(5);
    expect(card.rows.map(item => item.verbatim).join(' ')).toContain('Deduct 1/2 marks');
    expect(showsRowMarks(card)).toBe(false);
    expect(marksClaimed(card, Object.fromEntries(card.rows.map(item => [item.id, 'yes'])), {})).toBe(0);
  });

  it.each([false, true])('saves complete essay confidence 0/0 with paper layout=%s', async paperLayout => {
    const card = confidence(), onGrade = vi.fn();
    render(<SessionScreen paperLayout={paperLayout} cards={[card]} subjectLabel="Russian" onGrade={onGrade} onFinish={vi.fn()} onExit={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: 'Reveal the marking scheme' }));
    await waitFor(() => expect(screen.getByText(/Neither interpretation is selected/)).toBeVisible());
    expect(screen.queryByRole('button', { name: /^Claim \d+ marks/ })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Got it' }));
    expect(onGrade).toHaveBeenCalledWith(expect.objectContaining({ cardId: card.id, grade: 'got', marksClaimed: 0, marksAvailable: 0 }));
  });
});
// Current-root confidence headings and numeric-quiz exclusion are integration gates.
