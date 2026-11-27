import { useEffect, useMemo, useRef, useState, type KeyboardEvent as ReactKeyboardEvent } from 'react';
import { Bookmark, Check, ChevronRight as ChevronRightIcon, CircleHelp, Plus, RotateCcw } from 'lucide-react';
import { useFutureFinderRevamped } from '../hooks/useFutureFinderRevamped';
import type { StudentSubjectProfile } from './subjectData';
import { LoadingState } from './ui/SystemState';
import { computeAnalysis, type CourseResult } from './futureFinderAnalysis';
import { computeTargetCAOPoints, RECOMMENDATION_RANKING_VERSION } from './futureFinderRecommendation';
import { riasecItems, RIASEC_ITEMS, VALUE_ITEMS } from './futureFinderRiasecItems';
import { RIASEC_LETTERS, RIASEC_LABELS, WORK_VALUE_LABELS } from './futureFinderRiasec';
import { INSTITUTIONS, REGIONS } from './futureFinderData';
import { REACH_META, riasecToRecommendation } from './futureFinderRevampedAdapter';
import { CollegeLink, CourseFacts, CoursePoints, pointsDifference, typicalEntry } from './FutureCourseFacts';
import { Button, Glyph, TextButton } from './ui/Button';
import { ChoiceTile, SelectionBar, useRovingRadios } from './ui/Choice';
import { Menu } from './ui/Menu';
import { PaperSheet } from './ui/List';
import { Confirm, Sheet } from './ui/Sheet';
import { PinnedFooter } from './ui/Bars';
import { useFrameTask } from './ui/Frame';
import { useBackStep } from '../contexts/NavigationContext';
import './future-finder-paper.css';
import './future-finder-details.css';
import './future-finder-7.css';

const interestScale = ['Strongly dislike', 'Dislike', 'Neutral', 'Like', 'Strongly like'];
const valueScale = ['Not important', 'A little', 'Neutral', 'Important', 'Very important'];
type Question = { id: string; kind: 'interest' | 'value'; text: string };
const ROUTES = [
  { id: 'quick', meta: 'Around 5 minutes · 42 taps', name: 'Quick discovery', line: 'A first look at the things you enjoy.', count: '30 activities' },
  { id: 'full', meta: 'Around 9 minutes · 72 taps', name: 'The fuller picture', line: 'More room to explore your interests.', count: '60 activities' },
] as const;
/** The menus over the course list: the choice shows in the button under its small name. */
function Picker({ label, options, value, onChange }: { label: string; options: string[]; value: string; onChange: (value: string) => void }) {
  return <Menu label={label} block className="ff7-picker" value={value} onChange={onChange}
    face={<span className="ff7-picker-face"><small>{label}</small><span>{value}</span></span>} options={options.map(item => ({ value: item, label: item }))} />;
}

export default function FutureFinderPaper({uid, profile, resultsOnly = false, onOpenCareerPaths}: {uid?: string; profile: StudentSubjectProfile; studentSubjects?: string[]; resultsOnly?: boolean; onOpenCareerPaths?: (paths: string[])=>void}) {
  const {saved: stored, isLoaded, persist, reset: resetStored} = useFutureFinderRevamped(uid);
  const points = useMemo(()=>computeTargetCAOPoints(profile),[profile]);
  const subjectNames = useMemo(()=>profile.subjects.map(subject=>subject.subjectName),[profile]);
  const [phase, setPhase] = useState<'intro' | 'quiz' | 'results'>('intro');
  const [length, setLength] = useState<'quick' | 'full'>('full');
  const [at, setAt] = useState(0);
  const [responses, setResponses] = useState<Record<string, number>>({});
  const [values, setValues] = useState<Record<string, number>>({});
  const questionHeading = useRef<HTMLHeadingElement>(null);
  const answersRef = useRef<HTMLDivElement>(null);
  const main = useRef<HTMLElement>(null);
  const [saved, setSaved] = useState<string[]>([]);
  const [compares, setCompares] = useState<string[]>([]);
  const [detail, setDetail] = useState<CourseResult | null>(null);
  const [compareOpen, setCompareOpen] = useState(false);
  const [restartOpen, setRestartOpen] = useState(false);
  const [explainerOpen, setExplainerOpen] = useState(false);
  const [resultTab, setResultTab] = useState('All suggestions');
  const [sort, setSort] = useState('Recommended');
  const [region, setRegion] = useState('All regions');
  const questions: Question[] = useMemo(() => [
    ...riasecItems(length === 'quick').map(item => ({ id: item.id, text: item.text, kind: 'interest' as const })),
    ...VALUE_ITEMS.map(item => ({ id: item.id, text: item.text, kind: 'value' as const })),
  ], [length]);
  const interestCount = questions.length - VALUE_ITEMS.length;
  const q = questions[at];
  const answered = Object.keys(responses).length + Object.keys(values).length;
  const current = q.kind === 'interest' ? responses[q.id] : values[q.id];
  const a = useMemo(() => computeAnalysis(responses, values, points, subjectNames), [responses, values, points, subjectNames]);
  const top = [...RIASEC_LETTERS].sort((x, y) => a.studentProfile[y] - a.studentProfile[x]).slice(0, 3);
  const profileRatings = Object.fromEntries(RIASEC_LETTERS.map(letter => {
    const count = RIASEC_ITEMS.filter(item => item.scale === letter && responses[item.id] !== undefined).length;
    return [letter, count ? a.studentProfile[letter] / count : 0];
  }));
  const shown = a.shown.filter(result => (region === 'All regions' || REGIONS[result.course.region] === region) && (resultTab !== 'Saved picks' || saved.includes(result.course.code)));
  if (sort !== 'Recommended') shown.sort((x, y) => sort === 'Points: low to high' ? x.course.typicalPoints - y.course.typicalPoints : y.course.typicalPoints - x.course.typicalPoints);
  const displayed = shown.slice(0, 10);
  const compared = compares.map(code => a.shown.find(result => result.course.code === code)).filter((result): result is CourseResult => !!result);
  useEffect(() => {
    if (!isLoaded || !stored?.completedAt) return;
    setResponses(stored.responses ?? {}); setValues(stored.valueResponses ?? {}); setLength(stored.length ?? 'full');
    setSaved(stored.picks ?? []); setCompares(stored.compareCodes ?? []); setPhase('results');
  }, [isLoaded, stored]);
  useEffect(() => {
    if (!stored?.completedAt || stored.rankingVersion === RECOMMENDATION_RANKING_VERSION || !Object.keys(responses).length) return;
    persist({...stored, topMatches:a.shown.slice(0,10).map(item=>item.course.code), rankingVersion:RECOMMENDATION_RANKING_VERSION, updatedAt:new Date().toISOString()});
  }, [stored, responses, a, persist]);
  const savePicks = (picks: string[], compareCodes: string[]) => persist({
    length, responses, valueResponses:values, picks, compareCodes,
    topMatches:a.shown.slice(0,10).map(item=>item.course.code), rankingVersion:RECOMMENDATION_RANKING_VERSION,
    completedAt:stored?.completedAt ?? new Date().toISOString(), updatedAt:new Date().toISOString(),
  });
  useEffect(() => { if (phase === 'quiz') questionHeading.current?.focus({ preventScroll: true }); }, [at, phase]);
  const changePhase = (next: typeof phase) => {
    setPhase(next);
    requestAnimationFrame(() => main.current?.scrollIntoView?.({ block: 'start', behavior: 'instant' }));
  };
  // Choosing marks the answer; Continue moves on (the agreed question screen: the choice no
  // longer vanishes after a quarter of a second). The scoring and what is saved are unchanged.
  const choose = (rating: number) => (q.kind === 'interest' ? setResponses : setValues)(previous => ({ ...previous, [q.id]: rating }));
  const proceed = () => {
    if (current === undefined) return;
    if (at === questions.length - 1) {
      const ranked = computeAnalysis(responses,values,points,subjectNames).shown.slice(0,10).map(item=>item.course.code);
      persist({length,responses,valueResponses:values,picks:saved,compareCodes:compares,topMatches:ranked,rankingVersion:RECOMMENDATION_RANKING_VERSION,completedAt:new Date().toISOString(),updatedAt:new Date().toISOString()});
      changePhase('results');
    } else setAt(index => index + 1);
  };
  // The bar's one Back steps back a question, and from the first back to the opening (today's
  // "Previous question" and "Back to introduction"; answers stay for this visit).
  useBackStep(phase === 'quiz', () => { if (at) setAt(index => index - 1); else changePhase('intro'); });
  // The questions are a task: the tab bar steps aside for the pinned Continue on a phone.
  useFrameTask(phase === 'quiz');
  const scale = q.kind === 'interest' ? interestScale : valueScale;
  const roving = useRovingRadios(scale.length, current === undefined ? -1 : current - 1, index => choose(index + 1));
  const onQuestionKey = (event: ReactKeyboardEvent) => {
    if (event.metaKey || event.ctrlKey || event.altKey) return;
    if (/^[1-5]$/.test(event.key)) { event.preventDefault(); choose(Number(event.key)); }
    else if (event.key === 'Enter' && current !== undefined && !(event.target as HTMLElement).closest('button')) { event.preventDefault(); proceed(); }
  };
  const reset = () => {
    resetStored(); setResponses({}); setValues({}); setAt(0); setSaved([]); setCompares([]); setResultTab('All suggestions'); setSort('Recommended'); setRegion('All regions'); setRestartOpen(false); changePhase('intro');
  };
  const toggleSaved = (code: string) => { const next=saved.includes(code)?saved.filter(item=>item!==code):[...saved,code]; setSaved(next); savePicks(next,compares); };
  const toggleCompare = (code: string) => { if(compares.length>=3&&!compares.includes(code))return; const next=compares.includes(code)?compares.filter(item=>item!==code):[...compares,code]; setCompares(next); savePicks(saved,next); };
  const detailRecommendation = detail ? riasecToRecommendation(detail.course, detail.fit, top, a.studentValues, detail.recommendation) : null;
  const resultActions = (result: CourseResult) => <div className="ff7-actions">
    <CollegeLink course={result.course}/>
    <div className="ff7-action-pair">
      <Button size="sm" aria-pressed={saved.includes(result.course.code)} onClick={() => toggleSaved(result.course.code)}><span className="ff7-inline"><Bookmark size={16} fill={saved.includes(result.course.code) ? 'currentColor' : 'none'} aria-hidden="true" />{saved.includes(result.course.code) ? 'Saved' : 'Save'}</span></Button>
      <Button size="sm" aria-pressed={compares.includes(result.course.code)} unavailable={compares.length >= 3 && !compares.includes(result.course.code) ? 'Three courses are queued to compare.' : undefined} onClick={() => toggleCompare(result.course.code)}><span className="ff7-inline">{compares.includes(result.course.code) ? <Check size={16} aria-hidden="true" /> : <Plus size={16} aria-hidden="true" />}Compare</span></Button>
    </div>
  </div>;
  const stage = q.kind === 'interest' ? 0 : 1;
  const stageAt = q.kind === 'interest' ? at : at - interestCount;
  const stageTotal = q.kind === 'interest' ? interestCount : VALUE_ITEMS.length;

  if (!isLoaded) return <LoadingState label="Loading your future finder"/>;
  if (resultsOnly && !stored?.completedAt) return <p className="t-sub">Your course suggestions will appear after you complete Future Finder.</p>;
  return <div className="nsu-future-finder ff7"><main ref={main} className="ff7-main">

    {phase === 'intro' && <div className="ff7-intro">
      <section className="ff7-invite">
        <h2 className="t-display ff7-headline">Your interests are<br/>a starting point.</h2>
        <p className="t-sub ff7-lead">Rate activities and what matters to you. Find courses and routes worth a closer look.</p>
        <ol className="ff7-steps" aria-label="Your discovery">{['Find your interests', 'Explore the routes', 'Compare your options'].map((step, index) => <li key={step}><span className="t-readout">0{index + 1}</span>{step}</li>)}</ol>
      </section>
      <section className="ff7-routes-section">
        <div className="ff7-section-head"><p className="t-label">Choose your route</p><span className="t-meta">No right or wrong answers.</span></div>
        <div className="ff7-routes" role="radiogroup" aria-label="Discovery route">
          {ROUTES.map((route, index) => <ChoiceTile key={route.id} className="ff7-route" chosen={length === route.id} disabled={answered > 0} aria-label={route.name}
            onClick={() => setLength(route.id)}
            label={<span className="ff7-route-in"><span className="ff7-route-num">0{index + 1}</span><span className="ff7-route-copy"><span className="t-meta">{route.meta}</span><span className="ff7-route-name">{route.name}</span><span className="ff7-route-line">{route.line}</span><span className="t-meta">{route.count} + 12 work values</span></span></span>} />)}
        </div>
        <div className="ff7-go"><p className="t-meta">{answered ? `${answered} ${answered === 1 ? 'answer' : 'answers'} ready to continue.` : 'Take it at your own pace.'}</p><Button kind="main" size="lg" block arrow="forward" onClick={() => { changePhase('quiz'); }}>{answered ? 'Continue discovery' : 'Let’s explore'}</Button></div>
        {answered > 0 && <TextButton tone="quiet" onClick={() => setRestartOpen(true)}>Start again or change route</TextButton>}
        <p className="t-meta ff7-foot">A snapshot, not a verdict. Explore it with your guidance counsellor.</p>
      </section>
    </div>}

    {phase === 'quiz' && <div className="ff7-discovery">
      <aside className="ff7-journey"><p className="t-label">{length === 'quick' ? 'Quick discovery' : 'The fuller picture'}</p><h2 className="t-heading">A little more about you.</h2>
        <ol>{[['Your interests', interestCount + ' activities'], ['What matters', '12 work values'], ['Your possibilities', 'Courses to explore']].map(([title, description], index) => <li key={title} data-active={index === stage || undefined} data-complete={index < stage || undefined}><span className="t-readout">{index < stage ? <Check size={15} aria-label="Done" /> : `0${index + 1}`}</span><span><strong>{title}</strong><small>{description}</small></span></li>)}</ol>
        <p className="t-meta">Go with what appeals to you, even if you haven’t tried it yet.</p></aside>
      <section className="ff7-question-area" onKeyDown={onQuestionKey}>
        <div className="ff7-progress">
          <div className="ff7-count"><span className="t-label"><b className="ff7-live t-readout">{stage + 1} / 3</b> · {stage === 0 ? 'Your interests' : 'What matters'}</span><span className="t-label">{stageAt + 1} of {stageTotal}</span></div>
          <div className="ff7-steps-bar" role="progressbar" aria-label={`Question ${at + 1} of ${questions.length}`} aria-valuemin={0} aria-valuemax={questions.length} aria-valuenow={at}>
            {[0, 1, 2].map(index => <i key={index}><b style={{ transform: `scaleX(${index < stage ? 1 : index === stage ? stageAt / stageTotal : 0})` }} /></i>)}
          </div>
        </div>
        <PaperSheet className="ff7-card" label="Question">
          <p className="t-label ff7-ask">{q.kind === 'interest' ? 'How much would you enjoy this?' : 'How important is this to you?'}</p>
          <h2 className="ff7-q" ref={questionHeading} tabIndex={-1} key={q.id}>{q.text}.</h2>
          <div className="ff7-answers" ref={answersRef} role="radiogroup" aria-label={q.kind === 'interest' ? 'Rate this activity' : 'Rate this work value'}>
            {scale.map((label, index) => <ChoiceTile key={`${q.id}-${label}`} ref={element => { roving.refs.current[index] = element; }} className="ff7-answer" chosen={current === index + 1}
              tabIndex={roving.tabIndexOf(index)} onKeyDown={event => roving.onKeyDown(event, index)} onClick={() => choose(index + 1)} aria-label={label}
              label={<span className="ff7-answer-in"><span className="ff7-answer-num" aria-hidden="true">0{index + 1}</span><span>{label}</span></span>} />)}
          </div>
          <p className="t-meta ff7-keys">You can also use keys 1–5</p>
        </PaperSheet>
        <TextButton tone="quiet" className="ff7-pause" onClick={() => changePhase('intro')}>Pause</TextButton>
        <PinnedFooter className="ff7-foot-bar frame-float frame-float-bottom" lead={current === undefined ? undefined : `Your answer: ${scale[current - 1]}.`}>
          <Button kind="main" size="lg" block arrow="forward" missing={current === undefined ? { sentence: 'Choose one to continue.', goTo: answersRef } : undefined} onClick={proceed}>Continue</Button>
        </PinnedFooter>
      </section>
    </div>}

    {phase === 'results' && <>
      <div className="ff7-results-head"><p className="t-label">Your possibilities</p><h2 className="t-title ff7-results-title">A few directions<br/>worth exploring.</h2><p className="t-sub">Your interests, values and target grades, brought together.</p>
        <div className="ff7-results-tools"><Button onClick={() => setExplainerOpen(true)}><span className="ff7-inline"><Glyph icon={CircleHelp} size={20} />How this works</span></Button>{!resultsOnly && <Button onClick={() => setRestartOpen(true)}><span className="ff7-inline"><Glyph icon={RotateCcw} size={20} />Start again</span></Button>}</div></div>
      <div className="ff7-results">
        <aside className="ff7-profile"><p className="t-label">Your interest profile</p><h3 className="t-heading ff7-profile-title">{top.filter(letter => a.studentProfile[letter] > 0).map(letter => RIASEC_LABELS[letter]).join(', ')}.</h3>
          <div className="ff7-bars">{RIASEC_LETTERS.map(letter => <div key={letter} className="ff7-bar" data-leading={top.includes(letter) || undefined}><div><span>{RIASEC_LABELS[letter]}</span><span className="t-readout">{profileRatings[letter].toFixed(1)} / 5</span></div><span className="ff7-track"><i style={{ width: `${profileRatings[letter] / 5 * 100}%` }}/></span></div>)}</div>
          <div className="ff7-values"><p className="t-label">What matters to you</p><p className="ff7-values-list">{a.studentValues.map(value => WORK_VALUE_LABELS[value]).join(' · ')}</p></div>
          <div className="ff7-points"><span className="ff7-points-name">Target-grade points<small className="t-meta">From your subject targets.</small></span><strong className="t-number">{points}</strong></div>
          <p className="t-meta">{length === 'quick' ? 'A first indication. Try the fuller picture for a more detailed profile.' : 'A snapshot of your interests today. There is room for them to change.'}</p></aside>
        <section className="ff7-courses" aria-label="Course suggestions">
          <SelectionBar label="Course results" size="md" className="ff7-tabs" value={resultTab} onChange={value => setResultTab(value)} options={[{ value: 'All suggestions', label: 'All suggestions' }, { value: 'Saved picks', label: `Saved picks (${saved.length})` }]} />
          <div className="ff7-filters"><Picker label="Region" options={['All regions', ...Object.values(REGIONS)]} value={region} onChange={setRegion}/><Picker label="Order" options={['Recommended', 'Points: low to high', 'Points: high to low']} value={sort} onChange={setSort}/></div>
          <p className="t-meta">{displayed.length} {resultTab === 'Saved picks' ? 'saved possibilities' : 'possibilities to explore'}</p>
          {displayed.map((result, index) => <article className="ff7-course ff-course" key={result.course.code}><div className="ff7-course-num">{String(index + 1).padStart(2, '0')}</div><div className="ff7-course-main"><div className="t-meta">{result.course.code} · {result.course.institution} · Level {result.course.level}</div>
            <h3 className="ff7-course-title"><button type="button" onClick={() => setDetail(result)} aria-label={`Explore ${result.course.title}`}><span>{result.course.title}</span><Glyph icon={ChevronRightIcon} size={20} /></button></h3>
            <p className="t-sub">{result.course.description}</p>
            <div className="ff7-course-facts"><span><strong className={index === 0 ? 'ff7-live' : undefined}>{result.fit.matchPct}%</strong> interest match</span><span>{REACH_META[result.fit.reach].label}</span></div>
            <p className="t-meta">{pointsDifference(result.course, points).summary}</p>
            <CourseFacts course={result.course}/>{result.fit.eligibility.missing.length > 0 && <p className="t-meta">Check requirements: {result.fit.eligibility.missing.join(', ')}.</p>}{resultActions(result)}</div></article>)}
          {!displayed.length && <div className="ff7-empty"><h3 className="t-heading">{resultTab === 'Saved picks' ? 'A little room for possibilities.' : 'No courses in this view.'}</h3><p className="t-sub">{resultTab === 'Saved picks' ? 'Save courses as you explore to find them here.' : 'Try all regions or revisit your answers.'}</p><TextButton arrow="forward" onClick={() => { setRegion('All regions'); setResultTab('All suggestions'); }}>Show all suggestions</TextButton></div>}
          <p className="t-meta">Catalogue uses 2025 points. Points change each year; check current course requirements. Interest match stays separate from points reach.</p>
        </section></div>
      {compares.length > 0 && <div className="ff7-compare-bar frame-float frame-float-bottom"><div><strong>{compares.length} of 3 courses</strong><span className="t-meta">Make a little room to compare.</span></div><div className="ff7-compare-actions"><TextButton tone="quiet" onClick={() => {setCompares([]); savePicks(saved,[]);}}>Clear</TextButton><Button kind="main" arrow="forward" onClick={() => setCompareOpen(true)}>Compare courses</Button></div></div>}
    </>}

    <Sheet open={!!detail} onClose={() => setDetail(null)} title={detail?.course.title ?? 'Course'} titleAlign="start" className="ff7-sheet ff7-detail">
      {detail && detailRecommendation && <>
        <p className="t-label">{detail.course.code} · {INSTITUTIONS[detail.course.institution] || detail.course.institution}</p>
        <p className="t-sub">{detail.course.description}</p>
        <div className="ff7-figures"><div><span className="t-meta">Interest match</span><strong>{detail.fit.matchPct}%</strong></div><div><span className="t-meta">Points reach</span><strong>{REACH_META[detail.fit.reach].label}</strong></div><div><span className="t-meta">Qualification</span><strong>Level {detail.course.level}</strong></div></div>
        <CourseFacts course={detail.course}/>
        <CoursePoints course={detail.course} targetPoints={points}/>
        <section><h3 className="t-heading">Why it appears here</h3><ul className="ff7-reasons" role="list">{detailRecommendation.reasons.map(reason => <li key={reason}>{reason}</li>)}</ul></section>
        <section><h3 className="t-heading">Possible paths</h3><p className="t-sub">{detail.course.careerPaths.join(' · ')}</p>{onOpenCareerPaths && <Button arrow="forward" onClick={() => onOpenCareerPaths(detail.course.careerPaths)}>Explore career paths</Button>}</section>
        <dl className="ff7-extra"><div><dt className="t-meta">Employability</dt><dd>{detail.course.employability} / 5</dd></div><div><dt className="t-meta">Subjects that help</dt><dd>{detail.course.subjectBonus.length ? detail.course.subjectBonus.join(' · ') : 'No specific subjects listed'}</dd></div></dl>
        <section className="ff7-score"><h3 className="t-heading">A closer look at your fit.</h3>{([
          ['Interests', detailRecommendation.scoreBreakdown.interestScore],
          ['Work values', detailRecommendation.scoreBreakdown.valuesScore],
          ['Points reach', detailRecommendation.scoreBreakdown.feasibilityScore],
        ] as [string, number][]).map(([label, score]) => <div key={label}><span>{label}</span><span className="ff7-track"><i style={{ width: `${Math.round(score * 100)}%` }}/></span><span className="t-readout">{Math.round(score * 100)}%</span></div>)}</section>
        <p className="t-meta">{detail.fit.eligibility.missing.length ? `Subject requirements to check: ${detail.fit.eligibility.missing.join(', ')}. ` : ''}Catalogue figures use 2025 entry points. Check the provider’s current subjects, grades and entry requirements before applying.</p>
        {resultActions(detail)}
      </>}
    </Sheet>
    <Sheet open={compareOpen} onClose={() => setCompareOpen(false)} title="Keep your options open." titleAlign="start" className="ff7-sheet ff7-compare">
      <p className="t-label">Side by side</p>
      <p className="t-sub">Compare the course, entry route and work each possibility could lead to.</p>
      <div className="ff7-compare-grid" style={{ gridTemplateColumns: `repeat(${Math.max(1, compared.length)},minmax(0,1fr))` }}>{compared.map(result => <article key={result.course.code}>
        <p className="t-label">{result.course.code} · {result.course.institution}</p><h3 className="t-heading">{result.course.title}</h3>
        <dl><dt>Institution</dt><dd>{INSTITUTIONS[result.course.institution] || result.course.institution}</dd>
          <dt>Qualification</dt><dd>Level {result.course.level}</dd>
          <dt>Region</dt><dd>{REGIONS[result.course.region]}</dd>
          <dt>Duration</dt><dd>{result.course.duration} {result.course.duration === 1 ? 'year' : 'years'}</dd>
          <dt>Salary band</dt><dd>{result.course.salaryBand.charAt(0).toUpperCase() + result.course.salaryBand.slice(1)}</dd>
          <dt>Interest match</dt><dd>{result.fit.matchPct}%</dd>
          <dt>Points reach</dt><dd>{REACH_META[result.fit.reach].label}</dd>
          <dt>Your target points</dt><dd>{points}</dd>
          <dt>Typical entry · 2025</dt><dd>{typicalEntry(result.course)}</dd>
          <dt>{pointsDifference(result.course, points).label}</dt><dd>{pointsDifference(result.course, points).value}</dd>
          <dt>Employability</dt><dd>{result.course.employability} / 5</dd>
          <dt>Possible paths</dt><dd>{result.course.careerPaths.join(', ')}</dd>
          <dt>Subjects that help</dt><dd>{result.course.subjectBonus.join(', ') || 'No specific subjects listed'}</dd>
          <dt>Entry requirements</dt><dd>{result.fit.eligibility.missing.length ? `Check ${result.fit.eligibility.missing.join(', ')}` : 'Check current provider requirements'}</dd>
        </dl><CollegeLink course={result.course}/>
        <TextButton tone="quiet" aria-label={`Remove ${result.course.title} from comparison`} onClick={() => toggleCompare(result.course.code)}>Remove</TextButton>
      </article>)}</div>
      {!compared.length && <p className="t-sub">Add courses from your suggestions to compare them here.</p>}
    </Sheet>
    <Confirm open={restartOpen} sentence="Make a fresh start?" detail="This clears your saved answers and picks so you can choose either discovery route." keepLabel="Keep my answers" onKeep={() => setRestartOpen(false)} dangerLabel="Start again" onDanger={reset} />
    <Sheet open={explainerOpen} onClose={() => setExplainerOpen(false)} title="Three different things." titleAlign="start" className="ff7-sheet">
      <p className="t-label">Behind your possibilities</p>
      <p className="t-sub">Each helps you explore a course from a different angle.</p>
      <div className="ff7-explainer"><section><h3 className="t-row">01 / Your interests</h3><p className="t-sub">Activity ratings build a six-part RIASEC interest profile. Interest match compares your interests with each course, independently of points.</p></section><section><h3 className="t-row">02 / What you value</h3><p className="t-sub">Your answers highlight the things you want from work, such as independence, relationships or achievement.</p></section><section><h3 className="t-row">03 / Your routes</h3><p className="t-sub">The recommendation order also considers target-grade points, work values, route level and known subject requirements. A high interest match can still be a points stretch.</p></section><p className="t-sub">A snapshot, not a verdict. Use it alongside your guidance counsellor.</p></div>
    </Sheet>
  </main></div>;
}
