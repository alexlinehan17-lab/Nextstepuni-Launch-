/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Mark Bank library in the agreed look (Structure A, Alex 24 Nov 2026: "A is
 * the best yeah Structure A"; boards c-markbank-flow and r5-mark-bank). One very
 * long page became short pages:
 *
 *   the subject home   the subject and level as one button, what to practise now
 *                      with one charcoal button, Jump back in, then the strands
 *   a strand           its topics, each with its number, a thin bar and a count
 *   a topic            Practise in charcoal and Browse white with a line, then
 *                      where it comes up on the paper
 *   browse             every question of the topic; one starts the practice with it
 *   search             from the bar: topics across every strand
 *
 * A subject with one unit (Mathematics, Geography, Politics and Society) has no
 * strands: its topics sit under one row, "All 27 topics". On a laptop (1024px and
 * wider) the home's strands sit at the right, and a strand's topics sit at the
 * left with the chosen topic at the right (today's laptop bones). The one Back
 * (the Launchpad's bar) steps back through these pages, to where the student was.
 *
 * Data, counts, the practice queue and how a session starts are today's:
 * MarkBank.tsx's props and session wiring are unchanged.
 */

import { useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState, type CSSProperties, type ReactNode } from 'react';
import { ChevronDown } from 'lucide-react';
import SubjectAvatar from '../SubjectAvatar';
import { Button, Glyph, TextButton } from '../ui/Button';
import { ChoiceTile, SelectionBar, Switch } from '../ui/Choice';
import { SearchField } from '../ui/Field';
import { List, PressBox, Row } from '../ui/List';
import { MenuLabel, MenuPanel, MenuRadioRows, MenuSegment } from '../ui/Menu';
import { Sheet } from '../ui/Sheet';
import { ErrorState, LoadingShape } from '../ui/States';
import { useBackStep } from '../../contexts/NavigationContext';
import { useToolBar } from '../launchpad/toolBar';
import { getSubjectStarCrew } from '../../data/subjectStarCrew';
import { markBankCurriculumMenu, menuTopicIds } from './curriculumMenu';
import { SUBJECTS, LEVEL_LABEL, levelsFor, type Level } from './deck';
import { completeListeningExercises, resolveSessionQueue, sessionExerciseCount } from './sessionPlanning';
import { planSession } from './scheduler';
import type { DeckState } from './store';
import { isConfidenceReviewCard, isUnpricedSectionCard, unpricedSectionChip, type SecCard } from '../../types/markBank';
import './mark-bank-library.css';

const serial = (n: number) => String(n).padStart(2, '0');
const unitTitle = (title: string) => title.replace(/^(Core|Elective|Optional) Unit \d+:\s*/, '');
const plural = (n: number, one: string, many = `${one}s`) => `${n.toLocaleString()} ${n === 1 ? one : many}`;
/** A topic's own number when the syllabus prints one ("2.1", "U2"); the codes made from a
 *  topic's id ("aerial.photos") broke down the left of each row, and they go. */
const printedCode = (code?: string) => (code && /^[A-Z]{0,2}\d{1,2}(\.\d{1,2}){0,2}[a-z]?$/i.test(code) ? code : null);

/** One page of the library; `y` is where the page was scrolled to when the student left it. */
export type LibraryPage =
  | { at: 'home'; y?: number }
  | { at: 'strand'; strandId: string; topicId?: string; y?: number }
  | { at: 'topic'; topicId: string; y?: number }
  | { at: 'browse'; topicId: string; y?: number }
  | { at: 'search'; y?: number };
const HOME: LibraryPage[] = [{ at: 'home' }];

/** MarkBank keys this screen by deck, so a new subject or level mounts a new
 * instance. The subject button is focused again on it, so a keyboard user is
 * not dropped back to the top of the page. */
let refocusAfterRemount: { at: number } | null = null;

/** The laptop layout: two columns beside sidebar B (1024px and wider). */
function useWide() {
  const query = '(min-width: 1024px)';
  const [wide, setWide] = useState(() => typeof window !== 'undefined' && Boolean(window.matchMedia?.(query).matches));
  useEffect(() => {
    const media = window.matchMedia?.(query);
    if (!media) return undefined;
    const update = () => setWide(media.matches);
    media.addEventListener?.('change', update);
    return () => media.removeEventListener?.('change', update);
  }, []);
  return wide;
}

/** "Yesterday", "Sunday", "Last week": when a topic was last practised. */
function whenWords(ts: number, now: number) {
  const day = (t: number) => { const d = new Date(t); d.setHours(0, 0, 0, 0); return d.getTime(); };
  const days = Math.round((day(now) - day(ts)) / 86_400_000);
  if (days <= 0) return 'Today';
  if (days === 1) return 'Yesterday';
  if (days < 7) return new Date(ts).toLocaleDateString('en-IE', { weekday: 'long' });
  if (days < 14) return 'Last week';
  return new Date(ts).toLocaleDateString('en-IE', { day: 'numeric', month: 'short' });
}

const marksValue = (card: SecCard) => isConfidenceReviewCard(card)
  ? <span>Confidence review</span>
  : isUnpricedSectionCard(card)
    ? <span>{unpricedSectionChip(card.unpricedSection)}</span>
    : <><span>{card.totalMarks}</span> <span>marks</span></>;

interface Props {
 examDate?:string|null; subjectId:string; level:Level; cards:SecCard[]; state:DeckState; now:()=>number;
 chooseSubject:(id:string)=>void; chooseLevel:(level:Level)=>void; canSelectSubject:(name:string)=>boolean;
 onStart:(topicId?:string,queue?:SecCard[])=>void; busy:boolean; ready:boolean; loading:boolean; error:boolean; onRetry:()=>void; online:boolean;
 onStartingPoint?:()=>void;
 /** Cards of this deck that carry a recording: they are sat in Listening Studio, not reviewed here. */
 listeningCount?:number; onOpenListeningStudio?:()=>void;
 /** The page the student is on, held by MarkBank so a practice run returns to it. */
 pages?:LibraryPage[]; onPagesChange?:(pages:LibraryPage[])=>void;
 /** The subjects the student takes (Your setup), as Mark Bank subject ids: the only ones the
  *  subject button offers. None set: every subject. */
 mySubjectIds?:string[];
}

export default function MarkBankLibrary({examDate,subjectId,level,cards,state,now,chooseSubject,chooseLevel,canSelectSubject,onStart,onStartingPoint,busy,ready,loading,error,onRetry,online,listeningCount=0,onOpenListeningStudio,pages:heldPages,onPagesChange,mySubjectIds}:Props){
  const base = SUBJECTS.find(item => item.id === subjectId) ?? SUBJECTS[0];
  const wide = useWide();
  const menu = useMemo(() => markBankCurriculumMenu(subjectId, level, examDate, cards), [subjectId, level, examDate, cards]);
  const strands = menu.strands;
  const cardsByTopic = useMemo(() => {
    const grouped = new Map<string, SecCard[]>();
    for (const card of cards) for (const id of menuTopicIds(card, menu)) { const list = grouped.get(id) ?? []; list.push(card); grouped.set(id, list); }
    return grouped;
  }, [cards, menu.spec]);
  const memories = state.cards;
  const allTopics = useMemo(() => strands.flatMap((strand, strandIndex) => strand.topics.map((topic, topicIndex) => ({ ...topic, strand, strandIndex, topicIndex }))), [strands]);
  const topicStats = useMemo(() => new Map(allTopics.map(topic => {
    const list = cardsByTopic.get(topic.id) ?? [];
    let tried = 0; let last = 0;
    for (const card of list) { const seen = memories[card.id]?.last ?? 0; if (seen > 0) { tried += 1; if (seen > last) last = seen; } }
    return [topic.id, { count: list.length, tried, last, years: [...new Set(list.map(card => card.year))].sort((a, b) => a - b) }];
  })), [allTopics, cardsByTopic, memories]);
  const statsOf = (id: string) => topicStats.get(id) ?? { count: 0, tried: 0, last: 0, years: [] as number[] };
  const triedTotal = useMemo(() => cards.filter(card => (memories[card.id]?.last ?? 0) > 0).length, [cards, memories]);
  const strandStats = useCallback((strand: typeof strands[number]) => {
    const ids = new Set<string>(); const tried = new Set<string>();
    for (const topic of strand.topics) for (const card of cardsByTopic.get(topic.id) ?? []) { ids.add(card.id); if ((memories[card.id]?.last ?? 0) > 0) tried.add(card.id); }
    return { count: ids.size, tried: tried.size };
  }, [cardsByTopic, memories]);
  const bankYears = useMemo(() => { const years = cards.map(card => card.year); return years.length ? { from: Math.min(...years), to: Math.max(...years) } : null; }, [cards]);

  /* ---- the pages and the one Back ---- */
  const [ownPages, setOwnPages] = useState<LibraryPage[]>(HOME);
  const pages = heldPages?.length ? heldPages : ownPages;
  const setPages = onPagesChange ?? setOwnPages;
  const page = pages[pages.length - 1];
  const restoreY = useRef<number | null>(null);
  const push = useCallback((next: LibraryPage) => {
    const left = { ...pages[pages.length - 1], y: window.scrollY };
    setPages([...pages.slice(0, -1), left, next]);
    restoreY.current = 0;
  }, [pages, setPages]);
  const replace = useCallback((next: LibraryPage) => setPages([...pages.slice(0, -1), next]), [pages, setPages]);
  const pop = useCallback(() => {
    if (pages.length < 2) return;
    restoreY.current = pages[pages.length - 2].y ?? 0;
    setPages(pages.slice(0, -1));
  }, [pages, setPages]);
  useBackStep(pages.length > 1, pop);
  useLayoutEffect(() => {
    if (restoreY.current === null) return;
    const y = restoreY.current; restoreY.current = null;
    if (typeof window.scrollTo === 'function') try { window.scrollTo(0, y); } catch { /* jsdom */ }
  }, [page]);
  // Returning from a practice run lands where the student left the library.
  useLayoutEffect(() => { if (page.y) try { window.scrollTo(0, page.y); } catch { /* jsdom */ } }, []);

  const topicById = (id: string) => allTopics.find(topic => topic.id === id);
  const firstAvailable = (topics: { id: string }[]) => topics.find(topic => statsOf(topic.id).count > 0)?.id ?? topics[0]?.id;
  const openTopic = (topicId: string) => {
    const topic = topicById(topicId);
    if (!topic) return;
    push(wide ? { at: 'strand', strandId: topic.strand.id, topicId } : { at: 'topic', topicId });
  };
  const openSearch = () => { if (page.at !== 'search') push({ at: 'search' }); };

  // The bar names the page: the library on the subject home, the subject inside it.
  useToolBar(page.at === 'home'
    ? { over: 'The practice library', title: 'Mark Bank', search: { label: 'Search topics', onPress: openSearch } }
    : { over: 'Mark Bank', title: base.title });

  useEffect(() => {
    const handler = (event: KeyboardEvent) => { if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') { event.preventDefault(); openSearch(); } };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  });
  const subjectButtonRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const pending = refocusAfterRemount; refocusAfterRemount = null;
    if (!pending || Date.now() - pending.at > 1500) return;
    subjectButtonRef.current?.querySelector<HTMLElement>('.mb-subject')?.focus();
  }, []);
  function pickSubject(id: string) { if (id === subjectId) return; refocusAfterRemount = { at: Date.now() }; chooseSubject(id); }
  function pickLevel(next: Level) { if (next === level) return; refocusAfterRemount = { at: Date.now() }; chooseLevel(next); }

  /* ---- a topic's practice: today's Start ---- */
  const [amount, setAmount] = useState(6);
  const topicCards = (id?: string) => (id ? cardsByTopic.get(id) ?? [] : []);
  const queueFor = (id: string) => resolveSessionQueue(topicCards(id), memories, now(), state.examTs, amount);
  function begin(topicId: string, index?: number) {
    if (!ready || busy) return;
    const list = topicCards(topicId);
    const queue = queueFor(topicId);
    const seed = index === undefined ? queue : completeListeningExercises([list[index], ...queue, ...list], list, amount);
    onStart(topicId, seed);
  }

  /* ---- what to practise now: the whole subject, as the session after a sitting builds it ---- */
  const home = useMemo(() => {
    const t = now();
    const queue = resolveSessionQueue(cards, memories, t, state.examTs);
    const plan = planSession(cards.map(card => card.id), memories, t, { examTs: state.examTs });
    const due = plan.queue.slice(0, plan.dueCount);
    const dueTopics = new Set(cards.filter(card => due.includes(card.id)).flatMap(card => menuTopicIds(card, menu))).size;
    return { queue, n: sessionExerciseCount(queue), due: plan.dueCount, fresh: plan.newCount, dueTopics };
  }, [cards, memories, state.examTs, menu]);
  const q = (n: number) => (n === 1 ? 'question' : 'questions');
  const homeLine = home.due > 0 && home.fresh === 0
    ? `${home.due} ${q(home.due)} ${home.due === 1 ? 'is' : 'are'} due, from the ${plural(home.dueTopics, 'topic')} you have practised.`
    : home.due > 0
      ? `${home.due} ${q(home.due)} ${home.due === 1 ? 'is' : 'are'} due, from the ${plural(home.dueTopics, 'topic')} you have practised, and ${home.fresh} ${home.fresh === 1 ? 'is' : 'are'} new.`
      : home.fresh > 0
        ? triedTotal === 0 ? `Start with ${plural(home.n, 'question')} from across ${base.title}.` : `Nothing is due. Here are ${plural(home.n, 'question')} you have not tried yet.`
        : `Nothing is due. Here are the ${plural(home.n, 'question')} you remember least.`;
  const homeAction = home.due > 0 && home.fresh === 0 ? `Practise ${home.n} ${q(home.n)} due` : `Practise ${home.n} ${q(home.n)}`;
  const recent = useMemo(() => allTopics
    .filter((topic, index, list) => statsOf(topic.id).last > 0 && list.findIndex(other => other.id === topic.id) === index)
    .sort((a, b) => statsOf(b.id).last - statsOf(a.id).last)
    .slice(0, 3),
  [allTopics, topicStats]);

  const failed = error && !loading;
  const settled = !loading && !failed;
  const levelOptions = levelsFor(subjectId).map(value => ({ value, label: LEVEL_LABEL[value] }));
  const pickerSubjects = SUBJECTS.filter(item => canSelectSubject(item.title)
    && (!mySubjectIds?.length || mySubjectIds.includes(item.id) || item.id === subjectId));

  /* ---- parts ---- */
  const subjectButton = (
    <div className="mb-subject-slot" ref={subjectButtonRef}>
      <SubjectButton wide={wide} subject={base.title} subjectId={subjectId} level={level}
        meta={`${LEVEL_LABEL[level]} level${settled ? ` · ${plural(cards.length, 'question')}` : ''}`}
        levels={levelOptions} subjects={pickerSubjects} mine={Boolean(mySubjectIds?.length)}
        onSubject={pickSubject} onLevel={pickLevel} />
    </div>
  );
  const strandRows = strands.length === 1
    ? <List label="All topics">{(() => { const s = strandStats(strands[0]); return (
        <Row title={`All ${plural(strands[0].topics.length, 'topic')}`} progress={s.count ? s.tried / s.count : 0}
          meta={s.tried ? `${s.tried.toLocaleString()} of ${s.count.toLocaleString()} tried` : `${plural(s.count, 'question')}, none tried yet`}
          onPress={() => push({ at: 'strand', strandId: strands[0].id, topicId: wide ? firstAvailable(strands[0].topics) : undefined })} />
      ); })()}</List>
    : <List label="All topics">{strands.map((strand, index) => { const s = strandStats(strand); return (
        <Row key={strand.id} lead={serial(index + 1)} title={unitTitle(strand.title)} progress={s.count ? s.tried / s.count : 0}
          meta={`${plural(strand.topics.length, 'topic')} · ${s.tried ? `${s.tried.toLocaleString()} of ${s.count.toLocaleString()} tried` : `${plural(s.count, 'question')}, none tried yet`}`}
          onPress={() => push({ at: 'strand', strandId: strand.id, topicId: wide ? firstAvailable(strand.topics) : undefined })} />
      ); })}</List>;
  const allTopicsSection = (
    <section className="mb-sec" aria-labelledby="mb-all-topics">
      <div className="mb-sec-head"><h2 id="mb-all-topics" className="t-heading">All topics</h2>{settled && <span className="t-readout mb-ink3">{triedTotal.toLocaleString()} / {cards.length.toLocaleString()} tried</span>}</div>
      {settled ? strandRows : <LoadingShape label="Loading this question bank" rows={4} immediate />}
      {listeningCount > 0 && <p className="t-meta mb-note" data-testid="mark-bank-listening-moved">
        {listeningCount} listening {listeningCount === 1 ? 'question' : 'questions'} for {base.title} {listeningCount === 1 ? 'is' : 'are'} sat with the recording in Listening Studio.
        {onOpenListeningStudio && <>{' '}<TextButton arrow="forward" onClick={onOpenListeningStudio}>Open Listening Studio</TextButton></>}
      </p>}
    </section>
  );
  const syllabusNote = <p className="t-meta mb-note">{menu.current ? `Your syllabus: ${menu.spec?.title}.` : 'Your cohort map is being verified.'}{menu.model ? ' Topics are the Topic Atlas headings, so a question sits under the same topic in both.' : ''} Questions retain their original paper year. Archived topics are labelled in the index.</p>;
  const copyrightNote = <p className="t-meta mb-note">Question counts include distinct answer routes. Examination material © State Examinations Commission.</p>;
  const offlineNote = !online ? <p className="t-meta mb-note">You’re offline. Reviews save on this device and sync when your connection returns.</p> : null;

  const [availableOnly, setAvailableOnly] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const availableFilter = (topics: { id: string }[]) => topics.some(topic => statsOf(topic.id).count === 0)
    ? <label className="mb-filter"><span>Available only</span><Switch checked={availableOnly} onChange={setAvailableOnly} label="Available only" /></label>
    : null;
  const shownTopics = <T extends { id: string }>(topics: T[]) => (availableOnly ? topics.filter(topic => statsOf(topic.id).count > 0) : topics);
  // A strand's printed numbers where every topic has one; else their places in the list, so a
  // list never mixes "4" and "09".
  const topicNumber = (topic: { code?: string; topicIndex: number; strand: { topics: { code?: string }[] } }) =>
    topic.strand.topics.every(other => printedCode(other.code)) ? printedCode(topic.code)! : serial(topic.topicIndex + 1);
  const topicRow = (topic: typeof allTopics[number], options: { meta?: ReactNode; chosen?: boolean } = {}) => {
    const s = statsOf(topic.id);
    return (
      <Row key={`${topic.strand.id}:${topic.id}`} lead={topicNumber(topic)} title={topic.title} meta={s.count === 0 ? 'No questions in this corpus' : options.meta}
        progress={s.count ? s.tried / s.count : undefined} value={s.count ? `${s.tried} / ${s.count}` : undefined}
        label={`${topic.title}, ${s.count ? `${s.tried} of ${plural(s.count, 'question')} tried` : 'no questions in this corpus'}`}
        selected={options.chosen} onPress={() => (options.chosen === undefined ? openTopic(topic.id) : replace({ at: 'strand', strandId: topic.strand.id, topicId: topic.id, y: page.y }))} />
    );
  };

  /* ---- a topic: its head, Practise and Browse, where it comes up ---- */
  const topicPanel = (topicId: string | undefined, headingLevel: 'h1' | 'h2') => {
    const topic = topicId ? topicById(topicId) : undefined;
    if (!topic) return null;
    const s = statsOf(topic.id);
    const list = topicCards(topic.id);
    const queue = list.length ? queueFor(topic.id) : [];
    const sizes = [...new Set([3, 6, 12].map(n => Math.min(n, list.length)))];
    const Heading = headingLevel;
    const label = `${strands.length > 1 ? topic.strand.label || `Strand ${topic.strandIndex + 1}` : unitTitle(topic.strand.title)} · ${topicNumber(topic)}`;
    const sections = [...list.reduce((map, card) => map.set(card.section, (map.get(card.section) ?? 0) + 1), new Map<string, number>())]
      .sort((a, b) => a[0].localeCompare(b[0], undefined, { numeric: true }));
    const span = bankYears ? bankYears.to - bankYears.from + 1 : 0;
    const askedIn = new Set(s.years);
    return (
      <div className="mb-topic">
        <div className="mb-head">
          <p className="t-label mb-ink3">{label}</p>
          <Heading className="t-name">{topic.title}</Heading>
          {s.count > 0 ? <>
            <p className="t-sub">{plural(s.count, 'question')} from {plural(s.years.length, 'exam year')}.</p>
            <span className="mb-bar" aria-hidden="true"><i style={{ width: `${s.count ? (s.tried / s.count) * 100 : 0}%` }} /></span>
            <p className="t-meta">{s.tried ? `You have tried ${s.tried} of them.` : 'You have not tried any of them yet.'}</p>
          </> : null}
        </div>
        {s.count > 0 ? <>
          <section className="mb-sec mb-acts" aria-label="Practise this topic">
            <p className="t-label mb-ink3" id={`mb-size-${topic.id}`}>How many questions</p>
            <SelectionBar label="How many questions" value={String(Math.min(amount, list.length))} onChange={value => setAmount(Number(value))}
              options={sizes.map(n => ({ value: String(n), label: String(n) }))} />
            <Button kind="main" block arrow="forward" onClick={() => begin(topic.id)} aria-busy={busy || undefined}>Practise {queue.length} {q(queue.length)}</Button>
            <Button block onClick={() => push({ at: 'browse', topicId: topic.id })}>Browse all {plural(s.count, 'question')}</Button>
          </section>
          <section className="mb-sec" aria-labelledby={`mb-where-${topic.id}`}>
            <div className="mb-sec-head"><h2 id={`mb-where-${topic.id}`} className="t-heading">Where it comes up</h2></div>
            {sections.length > 0 && <dl className="mb-figures" style={{ '--n': Math.min(4, sections.length) } as CSSProperties}>
              {sections.map(([section, n]) => <div key={section}><dt className="t-meta">Section {section}</dt><dd className="mb-figure">{n}</dd></div>)}
            </dl>}
            {bankYears && <div className="mb-years-block">
              <p className="t-sub mb-ink">Asked in <b>{s.years.length} of the {span}</b> exam years since {bankYears.from}.</p>
              <span className="mb-years" style={{ '--n': span } as CSSProperties} aria-hidden="true">
                {Array.from({ length: span }, (_, i) => <i key={i} data-on={askedIn.has(bankYears.from + i) || undefined} />)}
              </span>
              <span className="mb-years-ends t-readout mb-ink3" aria-hidden="true"><span>{bankYears.from}</span><span>{bankYears.to}</span></span>
            </div>}
          </section>
        </> : <div className="mb-sec mb-empty-topic t-sub"><p>No questions are available for this topic in the current corpus.</p><p>You can still explore the rest of the subject index.</p></div>}
      </div>
    );
  };

  /* ---- the pages ---- */
  let body: ReactNode;
  if (failed) {
    body = <div className="mb-page">{subjectButton}<div className="mb-sec"><ErrorState sentence="The questions could not be loaded." onRetry={onRetry} /></div></div>;
  } else if (page.at === 'home' || !settled) {
    const now_ = now();
    const left = (
      <>
        {subjectButton}
        {offlineNote}
        <section className="mb-sec mb-now" aria-labelledby="mb-now-title">
          <h1 id="mb-now-title" className="t-title">A little practice.</h1>
          {settled ? <>
            <p className="t-sub">{homeLine}</p>
            <Button kind="main" size="lg" block arrow="forward" onClick={() => { if (ready && !busy && home.queue.length) onStart(undefined, home.queue); }} aria-busy={busy || undefined}>{homeAction}</Button>
          </> : <LoadingShape label="Loading this question bank" rows={2} immediate />}
          {/* Today's "Where should I start?" check (not on the board): it waits for the questions, as before. */}
          {onStartingPoint && ready && <TextButton tone="quiet" className="mb-start-here" onClick={() => { if (!busy) onStartingPoint(); }}>Where should I start?</TextButton>}
        </section>
        {settled && recent.length > 0 && <section className="mb-sec" aria-labelledby="mb-recent">
          <div className="mb-sec-head"><h2 id="mb-recent" className="t-heading">Jump back in</h2></div>
          <List label="Jump back in">{recent.map(topic => { const s = statsOf(topic.id); return (
            <Row key={topic.id} title={topic.title} meta={`${whenWords(s.last, now_)} · ${s.tried} of ${s.count} tried`} onPress={() => openTopic(topic.id)} />
          ); })}</List>
        </section>}
      </>
    );
    body = wide
      ? <div className="mb-page mb-cols"><div className="mb-col">{left}{syllabusNote}</div><div className="mb-col mb-side">{allTopicsSection}</div></div>
      : <div className="mb-page">{left}{allTopicsSection}{syllabusNote}</div>;
  } else if (page.at === 'search') {
    const query = searchQuery; const setQuery = setSearchQuery;
    const needle = query.trim().toLowerCase();
    const results = needle ? shownTopics(allTopics.filter(topic => `${topic.title} ${topic.strand.title}`.toLowerCase().includes(needle))) : [];
    body = <div className="mb-page">
      <div className="mb-search">
        <SearchField label="Search topics" placeholder={`Search ${base.title.toLowerCase()} topics…`} value={query} autoFocus
          aria-keyshortcuts="Meta+K Control+K" autoComplete="off" onChange={event => setQuery(event.target.value)} />
        {availableFilter(allTopics)}
      </div>
      {needle && results.length > 0 && <section className="mb-sec" aria-label={`Results for “${query}”`}>
        <p className="t-meta">{plural(results.length, 'matching topic')}</p>
        <List label="Matching topics">{results.map(topic => topicRow(topic, { meta: strands.length > 1 ? unitTitle(topic.strand.title) : undefined }))}</List>
      </section>}
      {needle && !results.length && <div className="mb-sec mb-empty"><h2 className="t-heading">No topics found.</h2><p className="t-sub">Try a different phrase or show every topic.</p><Button onClick={() => { setQuery(''); setAvailableOnly(false); }}>Reset filters</Button></div>}
    </div>;
  } else if (page.at === 'browse') {
    const topic = topicById(page.topicId);
    const list = topicCards(page.topicId);
    body = <div className={wide ? 'mb-page mb-cols' : 'mb-page'}>
      <div className="mb-col">
        <div className="mb-head">
          <p className="t-label mb-ink3">{topic?.title}</p>
          <h1 className="t-name">Browse all {plural(list.length, 'question')}</h1>
        </div>
        <section className="mb-sec mb-browse" aria-label={`Questions in ${topic?.title ?? 'this topic'}`}>
          <List label="Questions">{list.map((card, index) => (
            <Row key={card.id} title={card.stem || card.questionText} meta={card.questionRef} value={marksValue(card)}
              label={`${card.questionRef}: practise this first`} onPress={() => begin(page.topicId, index)} />
          ))}</List>
          {copyrightNote}
        </section>
      </div>
      {wide && <div className="mb-col mb-side">{topicPanel(page.topicId, 'h2')}</div>}
    </div>;
  } else {
    const topicPage = page.at === 'topic' ? page : null;
    const strand = page.at === 'strand' ? strands.find(item => item.id === page.strandId) : topicPage ? topicById(topicPage.topicId)?.strand : undefined;
    const strandIndex = strand ? strands.indexOf(strand) : -1;
    if (!strand) {
      body = <div className="mb-page">{subjectButton}<p className="t-sub mb-sec">No topics are available for this subject.</p></div>;
    } else if (topicPage && !wide) {
      body = <div className="mb-page">{topicPanel(topicPage.topicId, 'h1')}</div>;
    } else {
      const s = strandStats(strand);
      const topics = shownTopics(allTopics.filter(topic => topic.strand.id === strand.id));
      const chosen = (page.at === 'strand' ? page.topicId : topicPage?.topicId) ?? firstAvailable(topics);
      const head = (
        <div className="mb-head">
          <p className="t-label mb-ink3">{strands.length > 1 ? `${strand.label || `Strand ${strandIndex + 1}`} · ${plural(strand.topics.length, 'topic')}` : `${unitTitle(strand.title)} · ${plural(strand.topics.length, 'topic')}`}</p>
          <h1 className="t-name">{strands.length > 1 ? unitTitle(strand.title) : 'All topics'}</h1>
          <p className="t-sub">{plural(s.count, 'question')}. {s.tried ? `You have tried ${s.tried.toLocaleString()}.` : 'You have not tried any yet.'}</p>
          {availableFilter(strand.topics)}
        </div>
      );
      const list = <List label={`Topics in ${unitTitle(strand.title)}`}>{topics.map(topic => topicRow(topic, wide ? { chosen: topic.id === chosen } : {}))}</List>;
      body = wide
        ? <div className="mb-page mb-cols"><div className="mb-col">{head}{list}{copyrightNote}</div><div className="mb-col mb-side mb-panel">{topicPanel(chosen, 'h2')}</div></div>
        : <div className="mb-page">{head}{list}{copyrightNote}</div>;
    }
  }

  return <main className="mb-library" aria-busy={busy || loading} data-page={page.at}>
    {loading && <p className="sr-only" role="status">Loading this question bank…</p>}
    {body}
  </main>;
}


/** The subject and level as one button (the agreed subject home): its character, its name and
 *  level, and a chevron. On a phone it opens a sheet from the bottom, clear of the Dynamic Island;
 *  on a laptop a menu under the button. Level first, then the subjects, the current one ticked;
 *  choosing applies at once. */
function SubjectButton({ wide, subject, subjectId, level, meta, levels, subjects, mine, onSubject, onLevel }: {
  wide: boolean; subject: string; subjectId: string; level: Level; meta: string;
  levels: { value: Level; label: string }[]; subjects: { id: string; title: string }[]; mine: boolean;
  onSubject: (id: string) => void; onLevel: (level: Level) => void;
}) {
  const [open, setOpen] = useState(false);
  const name = `Change subject or level: ${subject}, ${meta}`;
  const face = (
    <>
      <span className="mb-subject-art" aria-hidden="true"><SubjectAvatar subject={subject} bare /></span>
      <span className="mb-subject-copy"><span className="t-name-sm">{subject}</span><span className="t-meta">{meta}</span></span>
    </>
  );
  const subjectsLabel = mine ? 'Your subjects' : 'Subjects';
  if (wide) {
    return (
      <MenuPanel label="Change subject or level" buttonLabel={name} face={face} align="start" buttonClassName="mb-subject" className="mb-subject-menu"
        open={open} onOpenChange={setOpen}>
        {levels.length > 1 && <div className="mb-menu-level"><MenuLabel>Paper level</MenuLabel>
          <MenuSegment label="Paper level" value={level} onChange={value => { setOpen(false); onLevel(value); }} options={levels} /></div>}
        <MenuLabel>{subjectsLabel}</MenuLabel>
        <MenuRadioRows label={subjectsLabel} value={subjectId} onChange={value => { setOpen(false); onSubject(value); }}
          options={subjects.map(item => ({ value: item.id, label: item.title, art: <SubjectAvatar subject={item.title} bare /> }))} />
      </MenuPanel>
    );
  }
  return (
    <>
      <PressBox className="mb-subject" label={name} expanded={open} onPress={() => setOpen(true)}>
        {face}
        <Glyph icon={ChevronDown} size={20} />
      </PressBox>
      <Sheet open={open} onClose={() => setOpen(false)} title="Change subject or level" titleAlign="start" className="mb-subject-sheet">
        {levels.length > 1 && <>
          <p className="t-label mb-ink3 mb-sheet-label">Paper level</p>
          <SelectionBar size="md" label="Paper level" value={level} options={levels} onChange={value => { setOpen(false); onLevel(value); }} />
        </>}
        <p className="t-label mb-ink3 mb-sheet-label">{subjectsLabel}</p>
        <div className="mb-sheet-subjects" role="radiogroup" aria-label={subjectsLabel}>
          {subjects.map(item => (
            <ChoiceTile key={item.id} chosen={item.id === subjectId} label={item.title} art={getSubjectStarCrew(item.title)?.src}
              onClick={() => { setOpen(false); onSubject(item.id); }} />
          ))}
        </div>
      </Sheet>
    </>
  );
}
