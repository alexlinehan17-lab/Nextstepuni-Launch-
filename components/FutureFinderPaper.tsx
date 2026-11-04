import { useEffect, useMemo, useRef, useState } from 'react';
import { ArrowLeft, ArrowRight, Bookmark, Check, Pause, RotateCcw, X } from 'lucide-react';
import { Button } from './approved-ui-runtime';
import { RadioGroup, RadioGroupItem } from './approved-ui-runtime';
import { Progress, ProgressLabel } from './approved-ui-runtime';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from './approved-ui-runtime';
import { Tabs, TabsList, TabsTrigger } from './approved-ui-runtime';
import { Artwork, Eyebrow } from './learning/shared';
import KobraScope from './approved-ui-runtime';
import { useFutureFinderRevamped } from '../hooks/useFutureFinderRevamped';
import type { StudentSubjectProfile } from './subjectData';
import { LoadingState } from './ui/SystemState';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './approved-ui-runtime';
import { computeAnalysis, type CourseResult } from './futureFinderAnalysis';
import { computeTargetCAOPoints, RECOMMENDATION_RANKING_VERSION } from './futureFinderRecommendation';
import { riasecItems, RIASEC_ITEMS, VALUE_ITEMS } from './futureFinderRiasecItems';
import { RIASEC_LETTERS, RIASEC_LABELS, WORK_VALUE_LABELS } from './futureFinderRiasec';
import { INSTITUTIONS, REGIONS } from './futureFinderData';
import { REACH_META, riasecToRecommendation } from './futureFinderRevampedAdapter';
import { CollegeLink, CourseFacts, CoursePoints, pointsDifference, typicalEntry } from './FutureCourseFacts';
import './future-finder-paper.css';
import './future-finder-details.css';

const interestScale = ['Strongly dislike', 'Dislike', 'Neutral', 'Like', 'Strongly like'];
const valueScale = ['Not important', 'A little', 'Neutral', 'Important', 'Very important'];
type Question = { id: string; kind: 'interest' | 'value'; text: string };
function Picker({label, options, value, onChange}: {label: string; options: string[]; value: string; onChange: (value: string) => void}) {
  return <label className="rs-field"><span>{label}</span><Select value={value} items={options.map(item=>({value:item,label:item}))} onValueChange={next=>next && onChange(next)}><SelectTrigger aria-label={label}><SelectValue/></SelectTrigger><SelectContent alignItemWithTrigger={false}>{options.map(item=><SelectItem value={item} key={item}>{item}</SelectItem>)}</SelectContent></Select></label>;
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
  const [busy, setBusy] = useState(false);
  const lock = useRef(false);
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const questionHeading = useRef<HTMLHeadingElement>(null);
  const detailTitle = useRef<HTMLHeadingElement>(null);
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
  useEffect(() => () => { if (timer.current) clearTimeout(timer.current); }, []);
  useEffect(() => { if (phase === 'quiz') questionHeading.current?.focus({ preventScroll: true }); }, [at, phase]);
  const changePhase = (next: typeof phase) => {
    setPhase(next);
    requestAnimationFrame(() => main.current?.scrollIntoView({ block: 'start', behavior: 'instant' }));
  };
  const advance = () => {
    if (at === questions.length - 1) changePhase('results');
    else setAt(index => index + 1);
  };
  const answer = (rating: number) => {
    if (lock.current) return;
    lock.current = true;
    setBusy(true);
    (q.kind === 'interest' ? setResponses : setValues)(previous => ({ ...previous, [q.id]: rating }));
    timer.current = setTimeout(() => {
      lock.current = false; setBusy(false);
      if (at === questions.length - 1) {
        const finalResponses = q.kind === 'interest' ? {...responses,[q.id]:rating} : responses;
        const finalValues = q.kind === 'value' ? {...values,[q.id]:rating} : values;
        const ranked = computeAnalysis(finalResponses,finalValues,points,subjectNames).shown.slice(0,10).map(item=>item.course.code);
        persist({length,responses:finalResponses,valueResponses:finalValues,picks:saved,compareCodes:compares,topMatches:ranked,rankingVersion:RECOMMENDATION_RANKING_VERSION,completedAt:new Date().toISOString(),updatedAt:new Date().toISOString()});
      }
      advance();
    }, 280);
  };
  const reset = () => {
    resetStored(); setResponses({}); setValues({}); setAt(0); setSaved([]); setCompares([]); setResultTab('All suggestions'); setSort('Recommended'); setRegion('All regions'); setRestartOpen(false); changePhase('intro');
  };
  const toggleSaved = (code: string) => { const next=saved.includes(code)?saved.filter(item=>item!==code):[...saved,code]; setSaved(next); savePicks(next,compares); };
  const toggleCompare = (code: string) => { if(compares.length>=3&&!compares.includes(code))return; const next=compares.includes(code)?compares.filter(item=>item!==code):[...compares,code]; setCompares(next); savePicks(saved,next); };
  const detailRecommendation = detail ? riasecToRecommendation(detail.course, detail.fit, top, a.studentValues, detail.recommendation) : null;
  const resultActions = (result: CourseResult, includeExplore = true) => <div className="ff-course-actions">
    <CollegeLink course={result.course}/>
    <Button variant="ghost" aria-pressed={saved.includes(result.course.code)} onClick={() => toggleSaved(result.course.code)}><Bookmark size={16} fill={saved.includes(result.course.code) ? 'currentColor' : 'none'} />{saved.includes(result.course.code) ? 'Saved' : 'Save'}</Button>
    <Button variant="ghost" aria-pressed={compares.includes(result.course.code)} disabled={compares.length >= 3 && !compares.includes(result.course.code)} onClick={() => toggleCompare(result.course.code)}>{compares.includes(result.course.code) && <Check size={16}/>}Compare</Button>
    {includeExplore && <Button variant="outline" onClick={() => setDetail(result)}>Explore <ArrowRight size={16}/></Button>}
  </div>;

  if (!isLoaded) return <LoadingState label="Loading your future finder"/>;
  if (resultsOnly && !stored?.completedAt) return <p>Your course suggestions will appear after you complete Future Finder.</p>;
  return <KobraScope className="nsu-future-finder"><main ref={main} className="ff-main">
    <header className="ff-masthead"><div><Eyebrow>Your next chapter</Eyebrow><h1>Future <em>Finder.</em></h1></div><Artwork src="/assets/tools/future-finder-revamped.png" size={78}/></header>

    {phase === 'intro' && <>
      <div className="ff-intro-grid">
        <section className="ff-invitation"><Eyebrow>Start with you</Eyebrow><h2>Your interests are<br/>a starting point.</h2><p>Rate activities and what matters to you. Find courses and routes worth a closer look.</p>
          <ol className="ff-steps" aria-label="Your discovery"><li><span>01</span>Find your interests</li><li><span>02</span>Explore the routes</li><li><span>03</span>Compare your options</li></ol>
        </section>
        <section className="ff-route-section"><div className="ff-section-heading"><Eyebrow>Choose your route</Eyebrow><span>No right or wrong answers.</span></div>
          <RadioGroup className="ff-routes" value={length} onValueChange={value => setLength(value as typeof length)} disabled={answered > 0} aria-label="Discovery route">
            {(['quick', 'full'] as const).map((route, index) => <label key={route} className="ff-route" data-selected={length === route}><span className="ff-route-number">0{index + 1}</span><span className="ff-route-copy"><span className="ff-route-meta">{route === 'quick' ? 'Around 5 minutes · 42 taps' : 'Around 9 minutes · 72 taps'}</span><strong>{route === 'quick' ? 'Quick discovery' : 'The fuller picture'}</strong><span>{route === 'quick' ? 'A first look at the things you enjoy.' : 'More room to explore your interests.'}</span><small>{route === 'quick' ? '30 activities' : '60 activities'} + 12 work values</small></span><RadioGroupItem value={route} aria-label={route === 'quick' ? 'Quick discovery' : 'The fuller picture'}/></label>)}
          </RadioGroup>
          <div className="ff-route-action"><p>{answered ? `${answered} ${answered === 1 ? 'answer' : 'answers'} ready to continue.` : 'Take it at your own pace.'}</p><Button className="ff-primary" variant="outline" onClick={() => { changePhase('quiz'); }}>{answered ? 'Continue discovery' : 'Let’s explore'}<ArrowRight size={18}/></Button></div>
          {answered > 0 && <Button variant="ghost" className="ff-restart" onClick={() => setRestartOpen(true)}>Start again or change route</Button>}
        </section>
      </div>
      <div className="ff-intro-foot"><p>A snapshot, not a verdict. Explore it with your guidance counsellor.</p></div>
    </>}

    {phase === 'quiz' && <>
      <div className="ff-discovery">
      <aside className="ff-journey"><Eyebrow>{length === 'quick' ? 'Quick discovery' : 'The fuller picture'}</Eyebrow><h2>A little more<br/>about you.</h2><ol>{[['Your interests', interestCount + ' activities'], ['What matters', '12 work values'], ['Your possibilities', 'Courses to explore']].map(([title, description], index) => <li key={title} data-active={index === (q.kind === 'interest' ? 0 : 1)} data-complete={index === 0 && q.kind === 'value'}><span>{index === 0 && q.kind === 'value' ? <Check size={15}/> : `0${index + 1}`}</span><div><strong>{title}</strong><small>{description}</small></div></li>)}</ol><p>Go with what appeals to you, even if you haven’t tried it yet.</p></aside>
      <section className="ff-question-area" data-direction="focus" onKeyDown={event => { if (/^[1-5]$/.test(event.key) && !event.metaKey && !event.ctrlKey && !event.altKey) { event.preventDefault(); answer(Number(event.key)); } }}>
        <div className="ff-question-toolbar"><Progress className="ff-progress" value={at} max={questions.length}><ProgressLabel>Question {at + 1} <span>of {questions.length}</span></ProgressLabel></Progress><Button variant="ghost" disabled={busy} onClick={() => changePhase('intro')}><Pause size={15}/>Pause</Button></div>
        <div className="ff-question-paper"><div className="ff-question-copy"><Eyebrow>{q.kind === 'interest' ? 'How much would you enjoy this?' : 'How important is this to you?'}</Eyebrow><h2 ref={questionHeading} tabIndex={-1} key={q.id}>{q.text}<span>.</span></h2></div>
          <div className="ff-answer-content"><div className="ff-answer-scale" role="group" aria-label={q.kind === 'interest' ? 'Rate this activity' : 'Rate this work value'}>{(q.kind === 'interest' ? interestScale : valueScale).map((label, index) => <Button key={label} variant="outline" disabled={busy} aria-pressed={current === index + 1} onClick={() => answer(index + 1)}><span className="ff-answer-number" aria-hidden="true">{`0${index + 1}`}</span><span className="ff-answer-label">{label}</span><span className="ff-answer-mark" aria-hidden="true">{current === index + 1 && <Check size={12}/>}</span></Button>)}</div>
          <div className="ff-answer-note"><span>Choose one to continue.</span><span className="ff-keyboard-note">You can also use keys 1–5</span></div></div>
        </div>
        <div className="ff-question-nav"><Button variant="ghost" disabled={busy} onClick={() => at ? setAt(index => index - 1) : changePhase('intro')}><ArrowLeft size={16}/>{at ? 'Previous question' : 'Back to introduction'}</Button></div>
      </section>
    </div></>}

    {phase === 'results' && <>
      <div className="ff-results-heading"><div><Eyebrow>Your possibilities</Eyebrow><h2>A few directions<br/>worth exploring.</h2><p>Your interests, values and target grades, brought together.</p></div><div className="ff-results-tools"><Button variant="outline" onClick={() => setExplainerOpen(true)}>How this works</Button>{!resultsOnly && <Button variant="ghost" onClick={() => setRestartOpen(true)}><RotateCcw size={16}/>Start again</Button>}</div></div>
      <div className="ff-results-grid"><aside className="ff-profile"><Eyebrow>Your interest profile</Eyebrow><h3>{top.filter(letter => a.studentProfile[letter] > 0).map(letter => RIASEC_LABELS[letter]).join(', ')}.</h3><div className="ff-profile-bars">{RIASEC_LETTERS.map(letter => <div key={letter}><div><span>{RIASEC_LABELS[letter]}</span><span>{profileRatings[letter].toFixed(1)} / 5</span></div><span className="ff-profile-track"><i style={{ width: `${profileRatings[letter] / 5 * 100}%` }} data-leading={top.includes(letter)}/></span></div>)}</div><div className="ff-profile-values"><Eyebrow>What matters to you</Eyebrow>{a.studentValues.map(value => <p key={value}>{WORK_VALUE_LABELS[value]}</p>)}</div><div className="ff-points"><span>Target-grade points</span><strong>{points}</strong><small>From your subject targets.</small></div><p className="ff-profile-note">{length === 'quick' ? 'A first indication. Try the fuller picture for a more detailed profile.' : 'A snapshot of your interests today. There is room for them to change.'}</p></aside>
        <section className="ff-courses"><div className="ff-results-filter"><Tabs value={resultTab} onValueChange={value => setResultTab(String(value))}><TabsList aria-label="Course results"><TabsTrigger value="All suggestions">All suggestions</TabsTrigger><TabsTrigger value="Saved picks">Saved picks ({saved.length})</TabsTrigger></TabsList></Tabs><div><Picker label="Region" options={['All regions', ...Object.values(REGIONS)]} value={region} onChange={setRegion}/><Picker label="Order" options={['Recommended', 'Points: low to high', 'Points: high to low']} value={sort} onChange={setSort}/></div></div>
          <p className="ff-result-count">{displayed.length} {resultTab === 'Saved picks' ? 'saved possibilities' : 'possibilities to explore'}</p>
          {displayed.map((result, index) => <article className="ff-course" key={result.course.code}><div className="ff-course-number">{String(index + 1).padStart(2, '0')}</div><div className="ff-course-main"><div className="ff-course-meta">{result.course.code} <span>·</span> {result.course.institution} <span>·</span> Level {result.course.level}</div><h3><button onClick={() => setDetail(result)}>{result.course.title}<ArrowRight size={20}/></button></h3><p>{result.course.description}</p><div className="ff-course-facts"><span><strong>{result.fit.matchPct}%</strong> interest match</span><span>{REACH_META[result.fit.reach].label}</span><span className="ff-points-gap">{pointsDifference(result.course, points).summary}</span></div><CourseFacts course={result.course}/>{result.fit.eligibility.missing.length > 0 && <p className="ff-requirement">Check requirements: {result.fit.eligibility.missing.join(', ')}.</p>}{resultActions(result)}</div></article>)}
          {!displayed.length && <div className="ff-empty"><h3>{resultTab === 'Saved picks' ? 'A little room for possibilities.' : 'No courses in this view.'}</h3><p>{resultTab === 'Saved picks' ? 'Save courses as you explore to find them here.' : 'Try all regions or revisit your answers.'}</p><Button variant="outline" onClick={() => { setRegion('All regions'); setResultTab('All suggestions'); }}>Show all suggestions <ArrowRight size={16}/></Button></div>}
          <p className="ff-catalogue-note">Catalogue uses 2025 points. Points change each year; check current course requirements. Interest match stays separate from points reach.</p>
        </section></div>
      {compares.length > 0 && <div className="ff-compare-bar"><div><strong>{compares.length} of 3 courses</strong><span>Make a little room to compare.</span></div><div><Button variant="ghost" onClick={() => {setCompares([]); savePicks(saved,[]);}}>Clear</Button><Button variant="outline" onClick={() => setCompareOpen(true)}>Compare courses <ArrowRight size={17}/></Button></div></div>}
    </>}

    <Dialog open={!!detail} onOpenChange={open => !open && setDetail(null)}>
      <DialogContent className="ff-dialog" size="lg" initialFocus={detailTitle}>
        <DialogHeader><Eyebrow>{detail?.course.code} / {detail ? INSTITUTIONS[detail.course.institution] || detail.course.institution : ''}</Eyebrow><DialogTitle ref={detailTitle} tabIndex={-1}>{detail?.course.title}</DialogTitle><DialogDescription>{detail?.course.description}</DialogDescription></DialogHeader>
        {detail && detailRecommendation && <>
          <div className="ff-detail-facts"><div><span>Interest match</span><strong>{detail.fit.matchPct}%</strong></div><div><span>Points reach</span><strong>{REACH_META[detail.fit.reach].label}</strong></div><div><span>Qualification</span><strong>Level {detail.course.level}</strong></div></div>
          <CourseFacts course={detail.course}/>
          <CoursePoints course={detail.course} targetPoints={points}/>
          <section><h3>Why it appears here</h3><ul className="ff-reasons" role="list">{detailRecommendation.reasons.map(reason => <li key={reason}>{reason}</li>)}</ul></section>
          <section><h3>Possible paths</h3><p>{detail.course.careerPaths.join(' · ')}</p>{onOpenCareerPaths && <Button variant="outline" onClick={() => onOpenCareerPaths(detail.course.careerPaths)}>Explore career paths <ArrowRight size={16}/></Button>}</section>
          <dl className="ff-extra-facts"><div><dt>Employability</dt><dd>{detail.course.employability} / 5</dd></div><div><dt>Subjects that help</dt><dd>{detail.course.subjectBonus.length ? detail.course.subjectBonus.join(' · ') : 'No specific subjects listed'}</dd></div></dl>
          <section className="ff-score-breakdown"><h3>A closer look at your fit.</h3>{([
            ['Interests', detailRecommendation.scoreBreakdown.interestScore],
            ['Work values', detailRecommendation.scoreBreakdown.valuesScore],
            ['Points reach', detailRecommendation.scoreBreakdown.feasibilityScore],
          ] as [string, number][]).map(([label, score]) => <div key={label}><span>{label}</span><span className="ff-score-track"><i style={{ width: `${Math.round(score * 100)}%` }}/></span><span>{Math.round(score * 100)}%</span></div>)}</section>
          <p className="ff-catalogue-note">{detail.fit.eligibility.missing.length ? `Subject requirements to check: ${detail.fit.eligibility.missing.join(', ')}. ` : ''}Catalogue figures use 2025 entry points. Check the provider’s current subjects, grades and entry requirements before applying.</p>
          {resultActions(detail, false)}
        </>}
      </DialogContent>
    </Dialog>
    <Dialog open={compareOpen} onOpenChange={setCompareOpen}>
      <DialogContent className="ff-dialog ff-compare-dialog" size="xl">
        <DialogHeader><Eyebrow>Side by side</Eyebrow><DialogTitle>Keep your options open.</DialogTitle><DialogDescription>Compare the course, entry route and work each possibility could lead to.</DialogDescription></DialogHeader>
        <div className="ff-compare-grid" style={{ gridTemplateColumns: `repeat(${Math.max(1, compared.length)},minmax(0,1fr))` }}>{compared.map(result => <article key={result.course.code}>
          <Button className="ff-remove" variant="ghost" size="icon" aria-label={`Remove ${result.course.title} from comparison`} onClick={() => toggleCompare(result.course.code)}><X size={16}/></Button>
          <Eyebrow>{result.course.code} / {result.course.institution}</Eyebrow><h3>{result.course.title}</h3>
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
        </article>)}</div>
        {!compared.length && <p>Add courses from your suggestions to compare them here.</p>}
      </DialogContent>
    </Dialog>
    <Dialog open={restartOpen} onOpenChange={setRestartOpen}><DialogContent className="ff-dialog" size="sm"><DialogHeader><DialogTitle>Make a fresh start?</DialogTitle><DialogDescription>This clears your saved answers and picks so you can choose either discovery route.</DialogDescription></DialogHeader><DialogFooter><Button variant="ghost" onClick={() => setRestartOpen(false)}>Keep my answers</Button><Button variant="outline" onClick={reset}>Start again <RotateCcw size={16}/></Button></DialogFooter></DialogContent></Dialog>
    <Dialog open={explainerOpen} onOpenChange={setExplainerOpen}><DialogContent className="ff-dialog" size="md"><DialogHeader><Eyebrow>Behind your possibilities</Eyebrow><DialogTitle>Three different things.</DialogTitle><DialogDescription>Each helps you explore a course from a different angle.</DialogDescription></DialogHeader><div className="ff-explainer"><section><h3>01 / Your interests</h3><p>Activity ratings build a six-part RIASEC interest profile. Interest match compares your interests with each course, independently of points.</p></section><section><h3>02 / What you value</h3><p>Your answers highlight the things you want from work, such as independence, relationships or achievement.</p></section><section><h3>03 / Your routes</h3><p>The recommendation order also considers target-grade points, work values, route level and known subject requirements. A high interest match can still be a points stretch.</p></section><p>A snapshot, not a verdict. Use it alongside your guidance counsellor.</p></div></DialogContent></Dialog>
  </main></KobraScope>;
}
