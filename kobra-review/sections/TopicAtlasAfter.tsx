/**
 * Topic Atlas, rebuilt on Kobra (AFTER for the wave 1 / 2 review, 27 Oct 2026).
 *
 * The same two levels, words and order as components/PaperTrail/ReviseByTopic.tsx
 * (the topic map, then one topic's question feed), on the real data: the
 * Paper Trail topic index loads lazily here, as the Viewer does, and the
 * question cards load the real paper crops and marking schemes from the
 * world-readable corpus. The whole surface sits inside the Kobra scope (the
 * review page's KobraScope here; in the app, wrapping studySurface in
 * PaperTrail/index.tsx does it, along with the saved and practice views).
 *
 * What changes against the current screen:
 *  - the subject picker is a Kobra Select (was a button opening a modal list);
 *  - "Search topics" is a Kobra Input on the hairline (was a grey hand-styled field);
 *  - sort, level and language bars are the house pill Tabs (were HorizontalTabs);
 *  - the year filter is a Kobra Select (was a native select);
 *  - Share confirms "Copied" with the runtime toast (was an inline green label);
 *  - "How the marks are given" is a hairline disclosure that opens and closes:
 *    Kobra's Accordion is purchased but NOT compiled into the runtime, so it is
 *    drawn here and needs compiling before it can replace this (was a peach panel);
 *  - placeholders while the index and each crop load are hairline skeleton rows:
 *    Kobra's Skeleton is not compiled either (needs compiling), so they are drawn;
 *  - every colour is a theme token, so the topic names that vanish in dark mode
 *    today (hex ink on dark:bg-zinc-900 rows) read in both themes.
 * Not rebuilt here: the Politics and Society task feed, the Accounting source
 * reader, PE task cards and French audio, which keep their own bodies.
 * Nothing is saved to an account: the review deck is this browser's local
 * storage under a review-only id, as in the "Now" pane.
 */
import { lazy, Suspense, useEffect, useId, useMemo, useRef, useState, type ReactNode } from 'react';
import { ArrowLeft, ArrowRight, BookOpenCheck, Check, ChevronDown, Download, ExternalLink, Link2, Plus, Scale, Search, X } from 'lucide-react';
import type { PDFDocumentProxy } from 'pdfjs-dist';
import {
  Button, Input, Select, SelectContent, SelectItem, SelectTrigger, SelectValue, Tabs, TabsList, TabsTrigger, toast,
} from '../../components/approved-ui-runtime';
import ThemeArtwork from '../../components/ThemeArtwork';
import type { PaperAnswerMap, PaperAnswerQuestion, PaperAnswerSeg } from '../../types/paperTrail';
import type { SubjectTopic, TopicSibling } from '../../components/PaperTrail/topics';
import './topic-atlas.css';

const CropView = lazy(() => import('../../components/PaperTrail/CropView'));

const UID = 'kobra-review-kobra';
const FIRST_SUBJECT = 'physics';
/** Review affordance: ?ta-topic=<id> opens the rebuild at one Physics topic (e.g. physics-higher-new-course-21-the-transfer-of-heat-energy-and-temperature-change). */
const FIRST_TOPIC = new URLSearchParams(window.location.search).get('ta-topic');
const LVL: Record<string, string> = { higher: 'HL', ordinary: 'OL', foundation: 'FL', common: 'CL' };
const LEVEL_NAME: Record<string, string> = { higher: 'Higher', ordinary: 'Ordinary', foundation: 'Foundation', common: 'Common' };
const CATEGORY_LABEL: Record<string, string> = {
  stem: 'Sciences & Maths', language: 'Languages', business: 'Business', 'social-environmental': 'Social & Environmental',
  'practical-applied': 'Practical & Applied', arts: 'Arts', other: 'Other subjects',
};

/** Everything the Atlas needs from the 1.2 MB Paper Trail index, loaded on demand. */
async function loadAtlas() {
  const [topics, registry, review, deepLink, pack, lens, data, names, resolve, region, docs] = await Promise.all([
    import('../../components/PaperTrail/topics'),
    import('../../data/examTopics/registry'),
    import('../../components/PaperTrail/reviewStore'),
    import('../../components/PaperTrail/vaultDeepLink'),
    import('../../components/PaperTrail/revisionPack'),
    import('../../data/markingLens'),
    import('../../paperTrailData'),
    import('../../components/shared/subjectNames'),
    import('../../components/PaperTrail/vaultResolve'),
    import('../../components/PaperTrail/paperRegion'),
    import('../../components/PaperTrail/vaultDocs'),
  ]);
  // Paper Trail's own label rule (paperTrailSubjectLabel): the short name unless two syllabuses share it.
  const counts = new Map<string, number>();
  for (const s of data.PAPER_TRAIL_SUBJECTS) counts.set(`${s.cycle}:${names.displayName(s.name)}`, (counts.get(`${s.cycle}:${names.displayName(s.name)}`) ?? 0) + 1);
  const byId = new Map(data.PAPER_TRAIL_SUBJECTS.map(s => [s.id, s]));
  const label = (id: string) => {
    const s = byId.get(id);
    if (!s) return names.displayName(id);
    return (counts.get(`${s.cycle}:${names.displayName(s.name)}`) ?? 0) > 1 ? s.name : names.displayName(s.name);
  };
  const subjects = topics.taggedSubjects()
    .filter(id => byId.get(id)?.cycle === 'lc')
    .map(id => ({ id, label: label(id) }))
    .sort((a, b) => a.label.localeCompare(b.label));
  return { topics, registry, review, deepLink, pack, lens, resolve, region, docs, label, subjects };
}
type Atlas = Awaited<ReturnType<typeof loadAtlas>>;

let atlasPromise: Promise<Atlas> | null = null;
const getAtlas = () => (atlasPromise ??= loadAtlas());

/** Skeleton: purchased but not compiled into the runtime (needs compiling), drawn as a hairline block. */
function Bone({ className = '' }: { className?: string }) {
  return <span className={`kr-ta-bone ${className}`} aria-hidden="true" />;
}

function PillTabs<T extends string>({ label, value, options, onChange }: {
  label: string; value: T; options: { value: T; label: string }[]; onChange: (value: T) => void;
}) {
  return (
    <Tabs value={value} onValueChange={next => onChange(String(next) as T)} className="kr-ta-tabs">
      <TabsList aria-label={label}>
        {options.map(option => <TabsTrigger key={option.value} value={option.value}>{option.label}</TabsTrigger>)}
      </TabsList>
    </Tabs>
  );
}

// ── One question card: the same loading rules as VaultQuestionCard ──────────
type CardState =
  | { s: 'idle' }
  | { s: 'ready'; pdf: PDFDocumentProxy; q: PaperAnswerQuestion; region: PaperAnswerSeg[]; schemeUrl: string | null }
  | { s: 'fallback' };

const mapMemo = new Map<string, Promise<PaperAnswerMap | null>>();

function QuestionCard({ atlas, sibling, saved, onToggleReview, onOpenInPaper }: {
  atlas: Atlas; sibling: TopicSibling; saved: boolean; onToggleReview: () => void; onOpenInPaper: () => void;
}) {
  const ids = useId();
  const rootRef = useRef<HTMLElement | null>(null);
  const [visible, setVisible] = useState(false);
  const [state, setState] = useState<CardState>({ s: 'idle' });
  const [lensOpen, setLensOpen] = useState(false);
  const [schemeOpen, setSchemeOpen] = useState(false);
  const [schemePdf, setSchemePdf] = useState<PDFDocumentProxy | null>(null);
  const [schemeFailed, setSchemeFailed] = useState(false);
  const resolved = useMemo(() => atlas.resolve.resolveSibling(sibling), [atlas, sibling]);
  const lens = useMemo(() => atlas.lens.lensFor(sibling), [atlas, sibling]);

  useEffect(() => {
    const el = rootRef.current;
    if (!el || visible) return;
    if (!('IntersectionObserver' in window)) { setVisible(true); return; }
    const obs = new IntersectionObserver(entries => {
      if (entries.some(e => e.isIntersecting)) { setVisible(true); obs.disconnect(); }
    }, { rootMargin: '400px 0px' });
    obs.observe(el);
    return () => obs.disconnect();
  }, [visible]);

  useEffect(() => {
    if (!visible || state.s !== 'idle') return;
    if (!resolved) { setState({ s: 'fallback' }); return; }
    let cancelled = false;
    const fetchOne = (url: string) => {
      let p = mapMemo.get(url);
      if (!p) {
        p = fetch(url).then(async r => {
          if (!r.ok) return null;
          const v = await r.json().catch(() => null);
          return atlas.resolve.isAnswerMap(v) ? v : null;
        }).catch(() => null);
        mapMemo.set(url, p);
      }
      return p;
    };
    (async () => {
      // As VaultQuestionCard: the map that carries this question, with the
      // verified scheme map and a hosted paper-only map merged when both do.
      let matched: PaperAnswerMap | null = null;
      for (const url of atlas.resolve.answerMapUrls(resolved)) {
        const m = await fetchOne(url);
        if (!m || !m.q.some(x => x.n === sibling.n)) continue;
        if (!matched) matched = m;
        else if (m.paperOnly === 1 && matched.paperOnly !== 1) matched = atlas.resolve.mergePaperAnchorMetadata(matched, m, sibling.n);
        else if (matched.paperOnly === 1 && m.paperOnly !== 1) matched = atlas.resolve.mergePaperAnchorMetadata(m, matched, sibling.n);
      }
      if (cancelled) return;
      const q = matched?.q.find(x => x.n === sibling.n);
      const limit = Math.max(sibling.subjectId === 'applied-mathematics' ? 4 : sibling.subjectId === 'politics-and-society' ? 10 : 3, matched?.maxCropPages ?? 0);
      const region = matched && q ? atlas.region.paperRegionFor(matched.q, sibling.n, limit) : null;
      if (!q || !region) { setState({ s: 'fallback' }); return; }
      try {
        const pdf = await atlas.docs.vaultPdf(resolved.paperUrl);
        if (!cancelled) setState({ s: 'ready', pdf, q, region, schemeUrl: resolved.schemeUrl });
      } catch {
        if (!cancelled) setState({ s: 'fallback' });
      }
    })();
    return () => { cancelled = true; };
  }, [atlas, visible, state.s, resolved, sibling.n, sibling.subjectId]);

  useEffect(() => {
    if (!schemeOpen || schemePdf || state.s !== 'ready' || !state.schemeUrl) return;
    let cancelled = false;
    atlas.docs.vaultPdf(state.schemeUrl)
      .then(pdf => { if (!cancelled) setSchemePdf(pdf); })
      .catch(() => { if (!cancelled) setSchemeFailed(true); });
    return () => { cancelled = true; };
  }, [atlas, schemeOpen, schemePdf, state]);

  const meta = [
    LEVEL_NAME[sibling.level] ?? sibling.level,
    sibling.paperKey === 'p1' ? 'Paper 1' : sibling.paperKey === 'p2' ? 'Paper 2' : null,
    sibling.lang === 'iv' ? 'Gaeilge' : null,
  ].filter(Boolean) as string[];
  const canReveal = state.s === 'ready' && state.schemeUrl !== null && state.q.mode === 'crop';

  return (
    <article ref={rootRef} className="kr-ta-card">
      <header className="kr-ta-card-head">
        <span className="kr-ta-card-year">{sibling.year}</span>
        <span className="kr-ta-card-meta">{[...meta, (state.s === 'ready' && state.q.label) || atlas.topics.questionLabel(sibling)].join(' · ')}</span>
        <Button variant="outline" size="icon" className="nsu-ink-outline kr-ta-icon" onClick={onToggleReview} aria-pressed={saved}
          aria-label={saved ? 'Remove from daily review' : 'Add to daily review'} title={saved ? 'In your daily review' : 'Add to daily review'}>
          {saved ? <Check aria-hidden="true" /> : <Plus aria-hidden="true" />}
        </Button>
        <Button variant="outline" size="sm" className="nsu-ink-outline kr-ta-small" onClick={onOpenInPaper} title="Open in the full paper">
          Full paper <ExternalLink aria-hidden="true" />
        </Button>
      </header>

      {state.s === 'ready' ? (
        <div className="kr-ta-crop">
          <Suspense fallback={<div className="kr-ta-card-skeleton"><Bone /><Bone className="kr-ta-bone-mid" /><Bone className="kr-ta-bone-short" /></div>}>
            <CropView pdf={state.pdf} region={state.region}
              ariaLabel={p => `Exam paper page ${p}, shown as an image — © State Examinations Commission`}
              failText="Couldn’t render this question — open the full paper." />
          </Suspense>
        </div>
      ) : state.s === 'fallback' ? (
        <Button variant="ghost" className="kr-ta-fallback" onClick={onOpenInPaper}>
          This question can’t be shown as a crop yet — <span>open it in the full paper →</span>
        </Button>
      ) : (
        <div className="kr-ta-card-skeleton" role="status" aria-label="Loading question">
          <Bone /><Bone className="kr-ta-bone-mid" /><Bone className="kr-ta-bone-short" />
        </div>
      )}

      {/* Marking Lens: a hairline disclosure. Kobra's Accordion is not compiled
          into the runtime (needs compiling); this is drawn to its shape. */}
      {lens && (
        <section className="kr-ta-lens" data-open={lensOpen || undefined}>
          <button type="button" className="kr-ta-disclosure" aria-expanded={lensOpen} aria-controls={`${ids}-lens`} onClick={() => setLensOpen(v => !v)}>
            <Scale aria-hidden="true" />
            <span>How the marks are given</span>
            <ChevronDown aria-hidden="true" className="kr-ta-chevron" />
          </button>
          <div className="kr-ta-lens-body" id={`${ids}-lens`} inert={!lensOpen} aria-hidden={!lensOpen}>
            <div className="kr-ta-lens-inner">
              <div className="kr-ta-lens-head">
                <p className="kr-ta-lens-headline">{lens.headline}</p>
                <span className="kr-ta-lens-total">{lens.totalMarks} marks</span>
              </div>
              <ol className="kr-ta-lens-parts">
                {lens.parts.map((part, index) => (
                  <li key={index} className="kr-ta-lens-part">
                    <span className="kr-ta-lens-copy">
                      <span className="kr-ta-lens-task">{part.part && <b>{part.part}</b>}{part.task}</span>
                      <span className="kr-ta-lens-notation">{part.notation}</span>
                      <span className="kr-ta-lens-decoded">{part.decoded}</span>
                    </span>
                    <span className="kr-ta-lens-marks" aria-label={`${part.marks} marks`}>{part.marks}<small>m</small></span>
                  </li>
                ))}
              </ol>
              {lens.pitfall && (
                <div className="kr-ta-lens-pitfall">
                  <p>Where marks are lost: {lens.pitfall.text}</p>
                  <p className="kr-ta-lens-cite">{lens.pitfall.cite}</p>
                </div>
              )}
              <p className="kr-ta-lens-source">{lens.cite} — © State Examinations Commission</p>
            </div>
          </div>
        </section>
      )}

      {state.s === 'ready' && (canReveal ? (
        <section className="kr-ta-lens" data-open={schemeOpen || undefined}>
          <button type="button" className="kr-ta-disclosure" aria-expanded={schemeOpen} onClick={() => setSchemeOpen(v => !v)}>
            <BookOpenCheck aria-hidden="true" />
            <span>{schemeOpen ? 'Hide the marking scheme' : 'Show the marking scheme'}</span>
            <ChevronDown aria-hidden="true" className="kr-ta-chevron" />
          </button>
          {schemeOpen && (
            <div className="kr-ta-scheme">
              <p className="kr-ta-lens-source">Marking scheme — © State Examinations Commission</p>
              {state.q.schemeNote && <p className="kr-ta-scheme-note">{state.q.schemeNote}</p>}
              {schemePdf ? (
                <div className="kr-ta-crop kr-ta-crop-scheme">
                  <Suspense fallback={<Bone />}>
                    <CropView pdf={schemePdf} region={atlas.region.schemeRegionFor(state.q)} trim responsive />
                  </Suspense>
                </div>
              ) : schemeFailed ? (
                <p className="kr-ta-muted">Couldn’t load the scheme — open the question in the full paper instead.</p>
              ) : <div className="kr-ta-card-skeleton"><Bone className="kr-ta-bone-mid" /></div>}
            </div>
          )}
        </section>
      ) : (
        <Button variant="ghost" className="kr-ta-disclosure kr-ta-open-beside" onClick={onOpenInPaper}>
          <BookOpenCheck aria-hidden="true" /> Open beside its marking scheme
        </Button>
      ))}
    </article>
  );
}

// ── The Atlas ────────────────────────────────────────────────────────────
function Atlas({ atlas }: { atlas: Atlas }) {
  const { topics: T, registry, review } = atlas;
  const [subjectId, setSubjectId] = useState(FIRST_SUBJECT);
  const [subtopicId, setSubtopicId] = useState<string | null>(() => (FIRST_TOPIC && atlas.topics.topicsForSubject(FIRST_SUBJECT).some(t => t.subtopicId === FIRST_TOPIC) ? FIRST_TOPIC : null));
  const [previewId, setPreviewId] = useState<string | null>(null);
  const [sort, setSort] = useState<'reference' | 'busiest' | 'frequent'>(() => (registry.examTopicTaxonomyFor(FIRST_SUBJECT) ? 'reference' : 'busiest'));
  const [levelFilter, setLevelFilter] = useState<string>('all');
  const [yearFilter, setYearFilter] = useState<'all' | number>('all');
  const [topicQuery, setTopicQuery] = useState('');
  const [langPref, setLangPref] = useState<'ev' | 'iv'>('ev');
  const [revVer, setRevVer] = useState(0);
  const headingRef = useRef<HTMLHeadingElement | null>(null);
  const level = subtopicId ? 2 : 1;
  const prevLevel = useRef(level);
  useEffect(() => {
    if (prevLevel.current !== level) headingRef.current?.focus();
    prevLevel.current = level;
  }, [level]);
  useEffect(() => () => atlas.docs.releaseVaultPdfs(), [atlas]);

  const chooseSubject = (id: string) => {
    setSubjectId(id);
    setSubtopicId(null);
    setPreviewId(null);
    setTopicQuery('');
    setSort(registry.examTopicTaxonomyFor(id) ? 'reference' : 'busiest');
  };
  const openTopic = (id: string | null) => {
    setSubtopicId(id);
    setLevelFilter('all');
    setYearFilter('all');
  };

  const label = atlas.label(subjectId);
  const taxonomy = registry.examTopicTaxonomyFor(subjectId);
  const baseTopics = useMemo(() => T.topicsForSubject(subjectId), [T, subjectId]);
  const totalYears = useMemo(() => T.taggedYearsForSubject(subjectId), [T, subjectId]);
  const referenceOrder = useMemo(() => new Map(taxonomy?.groups.flatMap(group => group.topicIds).map((id, index) => [id, index]) ?? []), [taxonomy]);
  const sortedTopics = useMemo(() => {
    if (sort === 'busiest') return baseTopics;
    if (sort === 'reference') return [...baseTopics].sort((a, b) => (referenceOrder.get(a.subtopicId) ?? 1e9) - (referenceOrder.get(b.subtopicId) ?? 1e9));
    return [...baseTopics].sort((a, b) => b.years - a.years || b.count - a.count || a.label.localeCompare(b.label));
  }, [baseTopics, sort, referenceOrder]);
  const topics = useMemo(() => {
    const q = topicQuery.trim().toLowerCase();
    return q ? sortedTopics.filter(t => t.label.toLowerCase().includes(q)) : sortedTopics;
  }, [sortedTopics, topicQuery]);

  const allEditions = useMemo(() => (subtopicId ? T.siblingsFor(subjectId, subtopicId) : []), [T, subjectId, subtopicId]);
  const hasIrish = allEditions.some(q => q.lang === 'iv');
  const questions = useMemo(() => {
    const byQ = new Map<string, TopicSibling>();
    for (const q of allEditions) {
      const key = T.logicalQuestionIdentity(q);
      const cur = byQ.get(key);
      if (!cur || (cur.lang !== langPref && q.lang === langPref)) byQ.set(key, q);
    }
    return [...byQ.values()].sort((a, b) => b.year - a.year || a.level.localeCompare(b.level) || a.n.localeCompare(b.n, undefined, { numeric: true }));
  }, [T, allEditions, langPref]);

  const subjectSelect = (
    <Select value={subjectId} items={atlas.subjects.map(s => ({ value: s.id, label: s.label }))}
      onValueChange={value => { if (typeof value === 'string') chooseSubject(value); }}>
      <SelectTrigger aria-label="Choose a subject" className="kr-ta-select kr-ta-subject"><SelectValue /></SelectTrigger>
      <SelectContent align="start" alignItemWithTrigger={false}>
        {atlas.subjects.map(s => <SelectItem key={s.id} value={s.id}>{s.label}</SelectItem>)}
      </SelectContent>
    </Select>
  );

  // ── Level 2: one topic's feed ──
  if (subtopicId) {
    const topicName = T.topicLabel(subtopicId);
    const years = new Set(questions.map(q => q.year));
    const referenceEntries = taxonomy?.topics.find(topic => topic.id === subtopicId)?.officialQuestionKeys.length ?? 0;
    const referenceOnly = questions.length === 0 && referenceEntries > 0;
    const levels = [...new Set(questions.map(q => q.level))];
    const yearList = [...years].sort((a, b) => b - a);
    const inYear = yearFilter === 'all' ? questions : questions.filter(q => q.year === yearFilter);
    const shown = levelFilter === 'all' ? inYear : inYear.filter(q => q.level === levelFilter);
    const levelCount = (l: string) => (l === 'all' ? inYear.length : inYear.filter(q => q.level === l).length);
    const copyTopicLink = async () => {
      const url = atlas.deepLink.buildVaultLink(subjectId, subtopicId);
      try {
        await navigator.clipboard.writeText(url);
        toast({ message: 'Copied' });
      } catch {
        window.prompt('Copy this link to share the topic:', url);
      }
    };
    const toggleReview = (q: TopicSibling) => {
      const id = { subjectId: q.subjectId, year: q.year, level: q.level, lang: q.lang, fileid: q.fileid, n: q.n };
      if (review.hasCard(UID, id)) review.removeCard(UID, id);
      else review.addCard(UID, id, subtopicId, Date.now());
      setRevVer(v => v + 1);
    };
    void revVer;
    return (
      <div className="kr-ta-feed">
        <Button variant="ghost" className="kr-ta-back" onClick={() => openTopic(null)}><ArrowLeft aria-hidden="true" />{label}</Button>
        <p className="kr-ta-eyebrow">{label} · {CATEGORY_LABEL[T.categoryOf(subjectId)] ?? 'Topic Atlas'}</p>
        <h2 ref={headingRef} tabIndex={-1} className="kr-ta-topic-title">{topicName}</h2>
        {referenceOnly ? (
          <p aria-live="polite" className="kr-ta-muted">{referenceEntries} reference entr{referenceEntries === 1 ? 'y' : 'ies'} · official source files pending</p>
        ) : shown.length === questions.length ? (
          <dl className="kr-ta-stats" aria-label={`${questions.length} questions across ${years.size} years, marking scheme beneath each`}>
            {[
              { v: String(questions.length), l: questions.length === 1 ? 'Question' : 'Questions' },
              { v: String(years.size), l: years.size === 1 ? 'Year' : 'Years' },
              { v: levels.map(l => LVL[l] ?? l).join(' · ') || 'All levels', l: 'Levels' },
            ].map(cell => <div key={cell.l}><dt>{cell.l}</dt><dd>{cell.v}</dd></div>)}
          </dl>
        ) : (
          <p aria-live="polite" className="kr-ta-muted kr-ta-filtered">
            {shown.length} of {questions.length} questions{yearFilter !== 'all' ? ` · ${yearFilter}` : ''}{levelFilter !== 'all' ? ` · ${LVL[levelFilter] ?? levelFilter}` : ''}
          </p>
        )}

        <div className="kr-ta-toolbar">
          {levels.length > 1 && (
            <PillTabs label="Level" value={levelFilter} onChange={setLevelFilter}
              options={['all', ...levels].map(l => ({ value: l, label: `${l === 'all' ? 'All levels' : LVL[l] ?? l} ${levelCount(l)}` }))} />
          )}
          {hasIrish && (
            <PillTabs label="Language" value={langPref} onChange={setLangPref}
              options={[{ value: 'ev', label: 'English' }, { value: 'iv', label: 'Gaeilge' }]} />
          )}
          {yearList.length > 3 && (
            <Select value={yearFilter === 'all' ? 'all' : String(yearFilter)}
              items={[{ value: 'all', label: 'All years' }, ...yearList.map(y => ({ value: String(y), label: String(y) }))]}
              onValueChange={value => { if (typeof value === 'string') setYearFilter(value === 'all' ? 'all' : Number(value)); }}>
              <SelectTrigger aria-label="Year" className="kr-ta-select kr-ta-year" data-chosen={yearFilter !== 'all' || undefined}><SelectValue /></SelectTrigger>
              <SelectContent align="start" alignItemWithTrigger={false}>
                <SelectItem value="all">All years</SelectItem>
                {yearList.map(y => <SelectItem key={y} value={String(y)}>{y}</SelectItem>)}
              </SelectContent>
            </Select>
          )}
          <span className="kr-ta-spacer" />
          {questions.length > 0 && (
            <Button variant="outline" size="sm" className="nsu-ink-outline kr-ta-small" onClick={() => atlas.pack.downloadPack({
              subjectLabel: label, topicLabel: topicName, questions: shown.length ? shown : questions, dateIso: new Date(Date.now()).toISOString().slice(0, 10),
            })}>
              <Download aria-hidden="true" /> Export
            </Button>
          )}
          <Button variant="outline" size="sm" className="nsu-ink-outline kr-ta-small" onClick={() => void copyTopicLink()} aria-label="Copy a shareable link to this topic">
            <Link2 aria-hidden="true" /> Share
          </Button>
        </div>

        <div className="kr-ta-cards">
          {referenceOnly ? (
            <p className="kr-ta-muted">This reference topic is retained, but its official question material is not available in the local SEC corpus yet.</p>
          ) : shown.length === 0 ? (
            <p className="kr-ta-muted">
              No questions match that filter.{' '}
              <Button variant="link" className="kr-ta-link" onClick={() => { setLevelFilter('all'); setYearFilter('all'); }}>Show all</Button>
            </p>
          ) : shown.map(q => (
            <QuestionCard key={`${q.year}-${q.level}-${q.lang}-${q.fileid}-${q.n}`} atlas={atlas} sibling={q}
              saved={review.hasCard(UID, { subjectId: q.subjectId, year: q.year, level: q.level, lang: q.lang, fileid: q.fileid, n: q.n })}
              onToggleReview={() => toggleReview(q)}
              onOpenInPaper={() => toast({ message: `Opens ${label} ${q.year} at ${T.questionLabel(q)} in the paper viewer` })} />
          ))}
        </div>
      </div>
    );
  }

  // ── Level 1: the topic map ──
  const stats = T.subjectAtlasStats(subjectId);
  const yearSets = T.topicYearSets(subjectId);
  const strands = T.strandsFor(subjectId, topics.map(t => t.subtopicId));
  const topicById = new Map(topics.map(t => [t.subtopicId, t]));
  const orderedByStrand = strands
    .map(strand => {
      const strandTopics = strand.subtopicIds.map(id => topicById.get(id)).filter((t): t is SubjectTopic => !!t);
      const ordered = [...strandTopics].sort((a, b) => sort === 'reference'
        ? (referenceOrder.get(a.subtopicId) ?? 1e9) - (referenceOrder.get(b.subtopicId) ?? 1e9)
        : sort === 'busiest'
          ? b.count - a.count || b.years - a.years || a.label.localeCompare(b.label)
          : b.years - a.years || b.count - a.count || a.label.localeCompare(b.label));
      return { strand, ordered };
    })
    .filter(entry => entry.ordered.length > 0);
  const contentsNo = new Map<string, number>();
  let running = 0;
  for (const entry of orderedByStrand) for (const t of entry.ordered) contentsNo.set(t.subtopicId, ++running);
  const selected = topics.find(t => t.subtopicId === previewId) ?? topics[0];

  return (
    <div className="kr-ta-map">
      <Masthead />
      <div className="kr-ta-controls">
        {subjectSelect}
        <p className="kr-ta-muted">{stats.questions.toLocaleString()} questions · {stats.yearMin}–{stats.yearMax}</p>
      </div>
      <div className="kr-ta-workspace">
        <section>
          <div className="kr-ta-toolbar kr-ta-map-toolbar">
            <PillTabs label="Sort topics" value={sort} onChange={setSort}
              options={([...(taxonomy ? ['reference'] as const : []), 'busiest', 'frequent'] as const).map(s => ({
                value: s, label: s === 'reference' ? 'A–Z' : s === 'busiest' ? 'Most asked' : 'Most recurrent',
              }))} />
            <span className="kr-ta-spacer" />
            {sortedTopics.length > 8 && (
              <div className="kr-ta-search">
                <Search aria-hidden="true" className="kr-ta-search-icon" />
                <Input type="text" value={topicQuery} onChange={e => setTopicQuery(e.target.value)} placeholder="Search topics" aria-label="Search topics" />
                {topicQuery && (
                  <Button variant="ghost" size="icon-sm" className="kr-ta-search-clear" onClick={() => setTopicQuery('')} aria-label="Clear search"><X aria-hidden="true" /></Button>
                )}
              </div>
            )}
          </div>
          {topics.length === 0 ? (
            <p className="kr-ta-muted kr-ta-empty">
              No topics match “{topicQuery.trim()}”.{' '}
              <Button variant="link" className="kr-ta-link" onClick={() => setTopicQuery('')}>Clear</Button>
            </p>
          ) : orderedByStrand.map(({ strand, ordered }) => (
            <section key={strand.id} className="kr-ta-strand">
              <div className="kr-ta-strand-head">
                <h3>{strand.name}</h3>
                <span className="kr-ta-rule" />
                <span>{ordered.reduce((a, t) => a + t.count, 0).toLocaleString()} q</span>
              </div>
              <div className="kr-ta-rows">
                {ordered.map(t => {
                  const asked = yearSets.get(t.subtopicId) ?? new Set<number>();
                  return (
                    <button key={t.subtopicId} type="button" className="kr-ta-row" aria-current={previewId === t.subtopicId || undefined}
                      onClick={() => openTopic(t.subtopicId)} onFocus={() => setPreviewId(t.subtopicId)} onMouseEnter={() => setPreviewId(t.subtopicId)}>
                      <span aria-hidden="true" className="kr-ta-serial">{String(contentsNo.get(t.subtopicId) ?? 0).padStart(2, '0')}</span>
                      <span className="kr-ta-row-copy">
                        <span className="kr-ta-row-title">{t.label}</span>
                        <span className="kr-ta-row-meta">{t.count} questions · {t.years} of {totalYears} years</span>
                      </span>
                      <span className="kr-ta-row-count">{t.count}</span>
                      <span className="kr-ta-strip" aria-label={`Asked in ${t.years} of ${totalYears} years`}>
                        {stats.years.map(y => <span key={y} title={String(y)} data-asked={asked.has(y) || undefined} />)}
                      </span>
                    </button>
                  );
                })}
              </div>
            </section>
          ))}
          <p className="kr-ta-muted kr-ta-note">Frequency describes past papers, not what will appear next.</p>
        </section>
        <aside className="kr-ta-preview">
          {selected ? (
            <>
              <p className="kr-ta-eyebrow">Selected topic</p>
              <h2 className="kr-ta-preview-title">{selected.label}</h2>
              <p className="kr-ta-muted">{selected.count} questions · {selected.years} of {totalYears} years</p>
              <p className="kr-ta-muted kr-ta-preview-body">Browse the original questions and open each with its linked marking scheme.</p>
              <Button className="kr-ta-explore" onClick={() => openTopic(selected.subtopicId)}>Explore this topic <ArrowRight aria-hidden="true" /></Button>
            </>
          ) : <p className="kr-ta-muted">Choose a topic from the map.</p>}
        </aside>
      </div>
    </div>
  );
}

function Masthead({ children }: { children?: ReactNode }) {
  return (
    <header className="kr-ta-masthead">
      <div>
        <p className="kr-ta-kicker">Follow the topic</p>
        <h1 className="kr-ta-title">Topic Atlas.</h1>
        <p className="kr-ta-lede">Past questions, connected by what they ask.</p>
        {children}
      </div>
      <ThemeArtwork src="/assets/tools/paper-trail.png" alt="" width={92} height={92} className="kr-ta-art" />
    </header>
  );
}

/** Placeholder rows while the Paper Trail index loads. */
function Loading() {
  return (
    <div className="kr-ta-map" role="status" aria-label="Loading the Topic Atlas">
      <Masthead />
      <div className="kr-ta-controls"><Bone className="kr-ta-bone-select" /><Bone className="kr-ta-bone-short" /></div>
      <div className="kr-ta-toolbar kr-ta-map-toolbar"><Bone className="kr-ta-bone-tabs" /></div>
      <div className="kr-ta-strand">
        <div className="kr-ta-strand-head"><Bone className="kr-ta-bone-short" /></div>
        <div className="kr-ta-rows">
          {Array.from({ length: 6 }, (_, i) => (
            <div key={i} className="kr-ta-row kr-ta-row-bone">
              <Bone className="kr-ta-bone-serial" />
              <span className="kr-ta-row-copy"><Bone className={i % 2 ? 'kr-ta-bone-mid' : ''} /></span>
              <Bone className="kr-ta-bone-count" />
              <Bone className="kr-ta-bone-strip" />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default function TopicAtlasAfter() {
  const [atlas, setAtlas] = useState<Atlas | null>(null);
  const [failed, setFailed] = useState(false);
  const [preview, setPreview] = useState<'loaded' | 'loading'>('loaded');
  useEffect(() => {
    let cancelled = false;
    getAtlas().then(a => { if (!cancelled) setAtlas(a); }).catch(() => { if (!cancelled) setFailed(true); });
    return () => { cancelled = true; };
  }, []);
  return (
    <section className="kr-section kr-ta" aria-label="Topic Atlas on Kobra">
      <div className="kr-ta-preview-bar">
        <span>Review: show the page</span>
        <PillTabs label="Review state" value={preview} onChange={setPreview}
          options={[{ value: 'loaded', label: 'Loaded' }, { value: 'loading', label: 'While the index loads' }]} />
      </div>
      {failed
        ? <p className="kr-ta-muted">The Paper Trail index did not load. Reload the page.</p>
        : atlas && preview === 'loaded' ? <Atlas atlas={atlas} /> : <Loading />}
    </section>
  );
}
