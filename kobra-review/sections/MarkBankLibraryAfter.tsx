/**
 * Mark Bank library, rebuilt on Kobra for the before/after review.
 *
 * The words are the live page's. The counts and years per unit are the
 * Politics and Society corpus at each level (components/MarkBank/cards/
 * politics-and-society/authored.json, units only: the syllabus's "Topic N"
 * groupings are left out), and every question shown is lifted from the paper.
 *
 * What changed against the before: the level segmented control is Kobra Tabs,
 * the search is a Kobra Input, "Available only" is a Kobra Checkbox, the
 * practice size is a Kobra ToggleGroup and every action is a Kobra Button. The
 * index and the unit list are the study room's hairline rows: a round ink
 * marker fills for the chosen strand and the chosen unit takes the ink ring.
 */

import { useEffect, useId, useRef, useState } from 'react';
import { ArrowRight, ArrowUpRight, RotateCcw, Search, X } from 'lucide-react';
import {
  Button,
  Checkbox,
  Input,
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
  Tabs,
  TabsList,
  TabsTrigger,
  ToggleGroup,
  ToggleGroupItem,
  toast,
} from '../../components/approved-ui-runtime';
import ThemeArtwork from '../../components/ThemeArtwork';
import './mark-bank-library-after.css';

type Level = 'higher' | 'ordinary';
type LoadState = 'loaded' | 'loading' | 'error';

interface Unit {
  id: string;
  code: string;
  title: string;
  count: Record<Level, number>;
  years: Record<Level, readonly number[]>;
}
interface Strand { id: string; title: string; units: Unit[] }
interface Sample { ref: string; marks: number; text: string }

const LEVEL_LABEL: Record<Level, string> = { higher: 'Higher', ordinary: 'Ordinary' };
const SIZES = [2, 5, 10] as const;
const SUBJECT = 'Politics and Society';
/** A student's own subjects. Only Politics and Society carries data in this review. */
const SUBJECTS = ['Biology', 'Business', 'English', 'Geography', 'Irish', 'Mathematics', SUBJECT];
const SUBJECT_ITEMS = SUBJECTS.map(title => ({ value: title, label: title }));

const span = (first: number, last: number) => Array.from({ length: last - first + 1 }, (_, i) => first + i);
const unit = (code: string, title: string, higher: number, higherYears: number[], ordinary: number, ordinaryYears: number[]): Unit => ({
  id: code, code, title, count: { higher, ordinary }, years: { higher: higherYears, ordinary: ordinaryYears },
});

const STRANDS: Strand[] = [
  {
    id: 'strand-1', title: 'Strand 1: Power and decision-making', units: [
      unit('1.1', 'Power in the School', 2, [2019, 2025], 7, [2018, 2019, 2022, 2023, 2024, 2025, 2026]),
      unit('1.2', 'The Need for Rules', 0, [], 2, [2025, 2026]),
      unit('1.3', 'Dimensions of Power', 0, [], 0, []),
      unit('1.4', 'Effects of Rules', 0, [], 0, []),
      unit('2.1', 'Making National Policy', 6, [2020, 2022, 2026], 9, [2019, 2021, 2022, 2023, 2024, 2026]),
      unit('2.2', 'Selecting the Executive', 18, span(2018, 2026), 16, [2018, 2019, 2021, 2022, 2024, 2025, 2026]),
      unit('2.3', 'Social Class and Gender', 21, span(2018, 2026), 23, [2018, 2019, ...span(2021, 2026)]),
      unit('2.4', 'Arguments on Representation', 5, [2019, 2021, 2022, 2023, 2026], 6, [2018, 2021, 2022, 2023, 2026]),
      unit('2.5', 'Effectiveness of Representation', 8, [2021, 2022, 2024, 2025], 3, [2022, 2023, 2025]),
      unit('2.6', 'Media, Public Opinion and Democracy', 19, span(2018, 2026), 17, [2018, 2019, ...span(2021, 2026)]),
      unit('2.7', 'Key Thinkers', 2, [2018], 2, [2021]),
    ],
  },
  {
    id: 'strand-2', title: 'Strand 2: Active citizenship', units: [
      unit('3.1', 'Positive Contributions', 0, [], 6, [2018, 2019, 2022, 2026]),
      unit('3.2', 'Starting an Initiative', 0, [], 7, [2019, ...span(2021, 2026)]),
      unit('3.3', 'Means of Taking Action', 5, [2019, 2022, 2023, 2025, 2026], 6, [2018, 2019, 2023, 2024, 2026]),
      unit('3.4', 'Setting and Achieving Goals', 0, [], 0, []),
      unit('3.5', 'Developing Personal Qualities', 0, [], 0, []),
      unit('3.6', 'Self-Appraisal and Feedback', 0, [], 0, []),
      unit('4.1', 'Freedom of Expression', 0, [], 0, []),
      unit('4.2', 'Listening and Communicating', 0, [], 0, []),
      unit('4.3', 'Resolving Conflicts', 0, [], 1, [2021]),
      unit('4.4', 'Evaluating Information', 35, span(2018, 2026), 66, [2018, 2019, ...span(2021, 2026)]),
      unit('4.5', 'Democracy in Wider Society', 0, [], 3, [2022, 2023, 2025]),
    ],
  },
  {
    id: 'strand-3', title: 'Strand 3: Human rights and responsibilities', units: [
      unit('5.1', 'Rights of Young People', 5, [2019, 2020, 2022, 2024, 2026], 21, [2018, ...span(2021, 2026)]),
      unit('5.2', 'Human Rights Principles', 10, [2018, 2019, 2020, 2023, 2024, 2026], 8, [2018, 2019, 2025, 2026]),
      unit('5.3', 'Equality and Rights', 13, [...span(2019, 2023), 2025, 2026], 14, [2018, ...span(2021, 2026)]),
      unit('5.4', 'Arguments About Rights', 1, [2021], 1, [2024]),
      unit('5.5', 'State Bodies for Rights', 0, [], 3, [2021, 2023, 2025]),
      unit('5.6', 'The Right to Education', 10, [2018, 2019, ...span(2021, 2025)], 8, [2018, 2021, 2024, 2025, 2026]),
      unit('5.7', 'Key Thinkers', 2, [2025], 1, [2022]),
      unit('6.1', 'Rights in the Wider World', 9, span(2019, 2024), 17, [2018, 2019, 2022, 2023, 2025, 2026]),
      unit('6.2', 'Arguments on Global Rights', 2, [2022, 2023], 4, [2022, 2024, 2025]),
      unit('6.3', 'International Cooperation', 7, [2018, 2019, 2022, 2024, 2026], 8, [2018, 2019, 2021, 2024, 2025]),
    ],
  },
  {
    id: 'strand-4', title: 'Strand 4: Globalisation and localisation', units: [
      unit('7.1', 'National Identity', 4, [2018, 2022, 2023, 2024], 2, [2024, 2025]),
      unit('7.2', 'Diversity and Cultural Change', 5, [2018, 2019, 2020, 2022, 2026], 5, [2018, 2019, 2021, 2026]),
      unit('7.3', 'Diversity in the EU', 1, [2025], 1, [2023]),
      unit('7.4', 'Understanding Identity', 6, [...span(2018, 2021), 2024, 2025], 6, [2018, 2019, 2023, 2025]),
      unit('7.5', 'West and Non-West Culture', 10, [2018, ...span(2023, 2026)], 4, [2021, 2022, 2024]),
      unit('7.6', 'Globalisation and Power', 5, [2018, 2021, 2022], 6, [2019, 2021, 2023, 2024, 2025, 2026]),
      unit('7.7', 'Key Thinkers', 0, [], 0, []),
      unit('8.1', 'Acting for Sustainable Development', 9, [2019, 2020, 2021, 2023, 2025, 2026], 17, [2018, 2019, ...span(2021, 2026)]),
      unit('8.2', 'Arguments on Sustainability', 16, [2018, 2019, ...span(2021, 2026)], 18, [2018, ...span(2022, 2026)]),
      unit('8.3', 'Key Thinkers', 2, [2023, 2024], 1, [2023]),
    ],
  },
];

/** Lifted from the SEC papers, as the bank holds them. */
const SAMPLES: Record<string, Record<Level, Sample[]>> = {
  '1.1': {
    higher: [
      { ref: '2019 HL Q1(d)', marks: 5, text: 'Are school uniforms socially divisive or a powerful tool for social equality? Justify your answer.' },
      { ref: '2025 HL Q1(a)', marks: 5, text: 'Identify a group that may be under-represented in the decision-making processes in schools and suggest one way to increase their representation.' },
    ],
    ordinary: [
      { ref: '2018 OL Q1(a)', marks: 5, text: 'Name two groups who are under‐represented in decision‐making processes in schools.\nExplain your answer.' },
      { ref: '2026 OL Q1(b)', marks: 10, text: 'Name a group that may be under-represented in the decision-making processes in schools.\nExplain your answer.' },
    ],
  },
};

const serial = (n: number) => String(n).padStart(2, '0');
const plural = (n: number, one: string, many: string) => `${n} ${n === 1 ? one : many}`;

/** Year runs, as the live library prints them: "2019, 2025" or "2018–2026". */
function yearsLabel(years: readonly number[]): string {
  const sorted = [...new Set(years)].sort((a, b) => a - b);
  const runs: string[] = [];
  for (let index = 0; index < sorted.length; index++) {
    const first = sorted[index];
    let last = first;
    while (sorted[index + 1] === last + 1) last = sorted[++index];
    runs.push(first === last ? String(first) : `${first}–${last}`);
  }
  return runs.join(', ');
}

/** A size is offered only when it would add questions over the size before it. */
const sizeEnabled = (index: number, count: number) => index === 0 || SIZES[index - 1] < count;
const defaultSize = (count: number) => (count > SIZES[0] ? SIZES[1] : SIZES[0]);

function Mark() {
  return <span className="kr-mb-mark" aria-hidden="true"><span /></span>;
}

function Skeleton({ className = '' }: { className?: string }) {
  return <span className={`kr-mb-skeleton ${className}`} aria-hidden="true" />;
}

export default function MarkBankLibraryAfter() {
  const ids = useId();
  const [loadState, setLoadState] = useState<LoadState>('loaded');
  const [subject, setSubject] = useState(SUBJECT);
  const [level, setLevel] = useState<Level>('higher');
  const [strandId, setStrandId] = useState(STRANDS[0].id);
  const [unitId, setUnitId] = useState('1.1');
  const [query, setQuery] = useState('');
  const [availableOnly, setAvailableOnly] = useState(false);
  const [amount, setAmount] = useState<number>(SIZES[0]);
  const searchRef = useRef<HTMLInputElement>(null);
  const libraryRef = useRef<HTMLDivElement>(null);
  const titleRef = useRef<HTMLHeadingElement>(null);
  const retryTimer = useRef<number | undefined>(undefined);

  const strandIndex = Math.max(0, STRANDS.findIndex(item => item.id === strandId));
  const strand = STRANDS[strandIndex];
  const allUnits = STRANDS.flatMap(item => item.units.map(entry => ({ ...entry, strand: item })));
  const selected = allUnits.find(item => item.id === unitId) ?? allUnits[0];
  const count = selected.count[level];
  const years = selected.years[level];
  const size = Math.min(amount, count);
  const samples = SAMPLES[selected.id]?.[level] ?? [];
  const needle = query.trim().toLowerCase();
  const visible = (needle ? allUnits : allUnits.filter(item => item.strand.id === strand.id))
    .filter(item => !availableOnly || item.count[level] > 0)
    .filter(item => `${item.code} ${item.title} ${item.strand.title}`.toLowerCase().includes(needle));
  const strandQuestions = strand.units.reduce((sum, item) => sum + item.count[level], 0);
  const bankQuestions = allUnits.reduce((sum, item) => sum + item.count[level], 0);
  const activeTopics = allUnits.filter(item => item.count[level] > 0).length;

  useEffect(() => {
    const handler = (event: KeyboardEvent) => {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
        event.preventDefault();
        searchRef.current?.focus();
      }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, []);
  useEffect(() => () => window.clearTimeout(retryTimer.current), []);

  function showState(next: LoadState) {
    window.clearTimeout(retryTimer.current);
    setLoadState(next);
  }
  function retry() {
    showState('loading');
    retryTimer.current = window.setTimeout(() => setLoadState('loaded'), 900);
  }
  function chooseLevel(next: Level) {
    setLevel(next);
    setAmount(defaultSize(selected.count[next]));
  }
  function chooseStrand(id: string) {
    const next = STRANDS.find(item => item.id === id) ?? STRANDS[0];
    const first = next.units.find(item => item.count[level] > 0) ?? next.units[0];
    setStrandId(next.id);
    setQuery('');
    setUnitId(first.id);
    setAmount(defaultSize(first.count[level]));
  }
  function chooseUnit(id: string) {
    const next = allUnits.find(item => item.id === id);
    if (!next) return;
    setUnitId(id);
    setAmount(defaultSize(next.count[level]));
  }
  function start(from?: string) {
    toast({ message: from ? `Practice opens at ${from}` : `Practice opens with ${plural(size, 'question', 'questions')} from ${selected.code} ${selected.title}` });
  }
  function backToLibrary() {
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    libraryRef.current?.scrollIntoView({ block: 'start', behavior: reduce ? 'auto' : 'smooth' });
    titleRef.current?.focus({ preventScroll: true });
  }

  const loading = loadState === 'loading';
  const failed = loadState === 'error';

  return (
    <section className="kr-section kr-mb" aria-labelledby={`${ids}-title`}>
      <div className="kr-mb-preview">
        <span className="kr-mb-preview-label" id={`${ids}-state`}>Preview state</span>
        <Tabs value={loadState} onValueChange={value => showState(value as LoadState)}>
          <TabsList aria-labelledby={`${ids}-state`}>
            <TabsTrigger value="loaded">Loaded</TabsTrigger>
            <TabsTrigger value="loading">Loading</TabsTrigger>
            <TabsTrigger value="error">Error</TabsTrigger>
          </TabsList>
        </Tabs>
      </div>

      <div className="kr-mb-library" ref={libraryRef}>
        <header className="kr-mb-masthead">
          <div>
            <p className="kr-mb-kicker">The practice library</p>
            <h2 className="kr-mb-title" id={`${ids}-title`} ref={titleRef} tabIndex={-1}>The Mark <em>Bank.</em></h2>
            <p className="kr-mb-lede">Flashcards made from real exam questions. Answer, check the marks, and each one comes back just before you’d forget it.</p>
          </div>
          <div className="kr-mb-masthead-aside">
            <ThemeArtwork src="/assets/tools/mark-bank.png" alt="" width={94} height={94} className="kr-mb-art" />
            <span>One question<br />at a time.</span>
          </div>
        </header>

        <div className="kr-mb-toolbar">
          <div className="kr-mb-field">
            <span className="kr-mb-field-label">Your subject</span>
            <Select value={subject} items={SUBJECT_ITEMS} onValueChange={value => { if (typeof value === 'string') setSubject(value); }}>
              <SelectTrigger aria-label="Choose subject"><SelectValue /></SelectTrigger>
              <SelectContent align="start" alignItemWithTrigger={false}>
                {SUBJECTS.map(title => <SelectItem key={title} value={title} disabled={title !== SUBJECT}>{title}</SelectItem>)}
              </SelectContent>
            </Select>
          </div>
          <div className="kr-mb-field kr-mb-level">
            <span className="kr-mb-field-label" id={`${ids}-level`}>Paper level</span>
            <Tabs value={level} onValueChange={value => chooseLevel(value as Level)}>
              <TabsList aria-labelledby={`${ids}-level`}>
                <TabsTrigger value="higher">{LEVEL_LABEL.higher}</TabsTrigger>
                <TabsTrigger value="ordinary">{LEVEL_LABEL.ordinary}</TabsTrigger>
              </TabsList>
            </Tabs>
          </div>
          <div className="kr-mb-search">
            <Search className="kr-mb-search-icon" aria-hidden="true" />
            <Input
              ref={searchRef}
              type="search"
              placeholder={`Search ${subject.toLowerCase()} topics…`}
              aria-label="Search topics"
              value={query}
              onChange={event => setQuery(event.target.value)}
            />
            {query
              ? <Button variant="ghost" size="icon-sm" className="kr-mb-search-clear" aria-label="Clear search" onClick={() => { setQuery(''); searchRef.current?.focus(); }}><X aria-hidden="true" /></Button>
              : <kbd className="kr-mb-kbd" aria-hidden="true">⌘ K</kbd>}
          </div>
        </div>
        <p className="kr-mb-fine">Your syllabus: Leaving Certificate Politics and Society specification. Questions retain their original paper year. Archived topics are labelled in the index.</p>

        <div className="kr-mb-layout" data-state={loadState} aria-busy={loading || undefined}>
          {loading && <p className="kr-mb-sr" role="status">Loading this question bank…</p>}

          <aside className="kr-mb-index" aria-label="The subject index">
            <div className="kr-mb-index-head">
              <p className="kr-mb-eyebrow">The subject index</p>
              <span>{serial(STRANDS.length)}</span>
            </div>
            {loading ? (
              <div className="kr-mb-index-list">
                {STRANDS.map(item => (
                  <div className="kr-mb-index-row kr-mb-index-row-skeleton" key={item.id}>
                    <Skeleton className="kr-mb-skeleton-mark" />
                    <Skeleton className="kr-mb-skeleton-serial" />
                    <Skeleton className="kr-mb-skeleton-line" />
                  </div>
                ))}
              </div>
            ) : (
              <nav className="kr-mb-index-list" aria-label="Subject units">
                {STRANDS.map((item, index) => {
                  const current = !needle && item.id === strand.id;
                  return (
                    <button type="button" key={item.id} className="kr-mb-index-row" aria-current={current ? 'true' : undefined} onClick={() => chooseStrand(item.id)}>
                      <Mark />
                      <span className="kr-mb-serial">{serial(index + 1)}</span>
                      <span className="kr-mb-index-title">{item.title}</span>
                    </button>
                  );
                })}
              </nav>
            )}
            {!loading && !failed && (
              <p className="kr-mb-index-note"><strong>{plural(bankQuestions, 'question', 'questions')}</strong><span>Across {activeTopics} topics</span></p>
            )}
          </aside>

          <section className="kr-mb-units" aria-labelledby={`${ids}-units`}>
            <div className="kr-mb-units-head">
              <p className="kr-mb-eyebrow">{needle ? 'Search the bank' : `${serial(strandIndex + 1)} / Subject unit`}</p>
              <h3 className="kr-mb-units-title" id={`${ids}-units`}>{needle ? `Results for “${query.trim()}”` : strand.title}</h3>
              <div className="kr-mb-units-meta">
                <span>{needle ? plural(visible.length, 'matching topic', 'matching topics') : `${strand.units.length} topics · ${plural(strandQuestions, 'question', 'questions')}`}</span>
                <label className="kr-mb-check">
                  <Checkbox checked={availableOnly} disabled={loading || failed} onCheckedChange={checked => setAvailableOnly(Boolean(checked))} />
                  Available only
                </label>
              </div>
            </div>

            {loading && (
              <ul className="kr-mb-unit-list" aria-hidden="true">
                {[0, 1, 2].map(row => (
                  <li key={row}>
                    <div className="kr-mb-unit kr-mb-unit-skeleton">
                      <Skeleton className="kr-mb-skeleton-code" />
                      <span className="kr-mb-unit-copy"><Skeleton className="kr-mb-skeleton-line" /><Skeleton className="kr-mb-skeleton-short" /></span>
                    </div>
                  </li>
                ))}
              </ul>
            )}

            {failed && (
              <div className="kr-mb-error" role="alert">
                <p>The questions could not be loaded.</p>
                <Button variant="outline" className="nsu-ink-outline" onClick={retry}><RotateCcw aria-hidden="true" />Try again</Button>
              </div>
            )}

            {loadState === 'loaded' && (
              <>
                <ul className="kr-mb-unit-list">
                  {visible.map(item => {
                    const n = item.count[level];
                    return (
                      <li key={item.id}>
                        <button type="button" className="kr-mb-unit" aria-pressed={item.id === selected.id} onClick={() => chooseUnit(item.id)}>
                          <span className="kr-mb-unit-code">{item.code}</span>
                          <span className="kr-mb-unit-copy">
                            <strong>{item.title}</strong>
                            <small>{n > 0 ? `${plural(n, 'question', 'questions')} · ${yearsLabel(item.years[level])}` : 'No questions in this corpus'}</small>
                          </span>
                          <ArrowUpRight className="kr-mb-unit-arrow" aria-hidden="true" />
                        </button>
                      </li>
                    );
                  })}
                </ul>
                {!visible.length && (
                  <div className="kr-mb-empty">
                    <h4>No topics found.</h4>
                    <p>Try a different phrase or show every topic.</p>
                    <Button variant="outline" className="nsu-ink-outline" onClick={() => { setQuery(''); setAvailableOnly(false); }}>Reset filters</Button>
                  </div>
                )}
              </>
            )}
            <p className="kr-mb-fine">Question counts include distinct answer routes. Examination material © State Examinations Commission.</p>
          </section>

          {!failed && (
            <aside className="kr-mb-practice nsu-paper-card" aria-label="Selected topic">
              {loading ? (
                <div className="kr-mb-practice-skeleton" aria-hidden="true">
                  <Skeleton className="kr-mb-skeleton-short" />
                  <Skeleton className="kr-mb-skeleton-title" />
                  <Skeleton className="kr-mb-skeleton-title kr-mb-skeleton-title-end" />
                  <span className="kr-mb-practice-skeleton-facts"><Skeleton className="kr-mb-skeleton-figure" /><Skeleton className="kr-mb-skeleton-figure" /></span>
                  <Skeleton className="kr-mb-skeleton-button" />
                </div>
              ) : (
                <>
                  <p className="kr-mb-eyebrow">{subject} / {LEVEL_LABEL[level]}</p>
                  <h3 className="kr-mb-practice-title">{selected.code} {selected.title}</h3>
                  <dl className="kr-mb-facts">
                    <div><dt>{count === 1 ? 'question to explore' : 'questions to explore'}</dt><dd>{count}</dd></div>
                    <div><dt>{years.length === 1 ? 'exam year' : 'exam years'}</dt><dd>{years.length || '—'}</dd></div>
                  </dl>
                  {count > 0 ? (
                    <>
                      <p className="kr-mb-label" id={`${ids}-size`}>A little practice</p>
                      <ToggleGroup
                        className="kr-mb-size"
                        variant="outline"
                        aria-labelledby={`${ids}-size`}
                        value={[String(amount)]}
                        onValueChange={values => { if (values[0]) setAmount(Number(values[0])); }}
                      >
                        {SIZES.map((n, index) => (
                          <ToggleGroupItem key={n} value={String(n)} disabled={!sizeEnabled(index, count)} aria-label={`${n} questions`}>{n}</ToggleGroupItem>
                        ))}
                      </ToggleGroup>
                      <Button className="kr-mb-start" onClick={() => start()}>
                        Start {plural(size, 'question', 'questions')}<ArrowRight aria-hidden="true" />
                      </Button>
                      <p className="kr-mb-start-note">Write an answer. Then open the scheme.</p>
                      {samples.length > 0 && (
                        <div className="kr-mb-inside">
                          <p className="kr-mb-eyebrow">Inside this topic</p>
                          <ul>
                            {samples.map(sample => (
                              <li key={sample.ref}>
                                <button type="button" className="kr-mb-sample" onClick={() => start(sample.ref)}>
                                  <span className="kr-mb-sample-copy"><strong>{sample.text}</strong><small>{sample.ref}</small></span>
                                  <span className="kr-mb-sample-marks">{sample.marks}<small>marks</small></span>
                                </button>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </>
                  ) : (
                    <div className="kr-mb-empty-topic">
                      <p>No questions are available for this topic in the current corpus.</p>
                      <p>You can still explore the rest of the subject index.</p>
                    </div>
                  )}
                </>
              )}
            </aside>
          )}
        </div>
      </div>

      <div className="kr-mb-after">
        <header className="kr-mb-after-head">
          <p className="kr-mb-eyebrow">After a session</p>
          <span>Sample results, not a real account</span>
        </header>
        <section className="kr-mb-close nsu-paper-card" aria-labelledby={`${ids}-close`}>
          <p className="kr-mb-kicker">Session complete</p>
          <h3 className="kr-mb-close-title" id={`${ids}-close`}>Good work. Keep building.</h3>
          <p className="kr-mb-close-meta">2 questions reviewed · Politics and Society · Higher level</p>
          <dl className="kr-mb-stats">
            <div><dt>Marks banked</dt><dd>7</dd></div>
            <div><dt>Available</dt><dd>10</dd></div>
            <div><dt>To revisit</dt><dd>3</dd></div>
          </dl>
          <div className="kr-mb-next">
            <p className="kr-mb-eyebrow">Best next review</p>
            <p className="kr-mb-next-ref">2025 HL Q1(a) · 3 marks to recover</p>
            <p className="kr-mb-next-text">Identify a group that may be under-represented in the decision-making processes in schools and suggest one way to increase their representation.</p>
          </div>
          <div className="kr-mb-close-actions">
            <Button className="kr-mb-close-primary" onClick={backToLibrary}>Back to Mark Bank<ArrowUpRight aria-hidden="true" /></Button>
            <Button variant="outline" className="nsu-ink-outline" onClick={() => toast({ message: 'Practice opens with 2 cards from 1.1 Power in the School' })}>Review 2 cards from this topic</Button>
          </div>
        </section>
      </div>
    </section>
  );
}
