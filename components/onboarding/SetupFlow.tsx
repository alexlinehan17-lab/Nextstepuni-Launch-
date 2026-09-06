import React, { useEffect, useLayoutEffect, useRef, useState } from 'react';
import { ArrowLeft, ArrowUpRight, X } from 'lucide-react';
import { useReducedMotion } from '../Motion';
import { useModal } from '../../hooks/useModal';
import { DAYS_OF_WEEK, SUBJECT_GROUP_LABELS, type Level, type StudentSubjectProfile, type YearGroup } from '../subjectData';
import { getActiveCategories, getVisionCardsForLevel, VISION_CARD_ART } from '../../northStarData';
import { NORTH_STAR_CATEGORY_BLOBS } from '../NorthStarCategoryIcon';
import { isLcaYear } from '../../utils/authUtils';
import { trackFunnel } from '../../utils/funnel';
import type { NorthStar } from '../../types';
import { buildNorthStar, buildProfile, choiceReady, choicesFor, cycleFor, daysUntil, draftKey, emptyChoice, hasGrades, legacyDraftKey, needsDate, pointsFor, readDraft, subjectsFor, type GradeChoice, type SetupDraft, type SetupStep, type SubjectChoice } from './model';
import './onboarding.css';

export interface OnboardingProps {
  userId: string;
  userName: string;
  onComplete: (profile: StudentSubjectProfile, northStar?: NorthStar, essentialsMode?: boolean) => void | Promise<void>;
  onSkip: () => void;
  mode?: 'fresh' | 'transition-to-senior';
  transitionTargetYear?: 'TY' | '5th';
}

function PointsCount({ from, to }: { from: number; to: number }) {
  const reduced = useReducedMotion();
  const [value, setValue] = useState(from);
  useEffect(() => {
    if (reduced || from === to) { setValue(to); return; }
    setValue(from);
    const start = performance.now();
    let frame = 0;
    const tick = (now: number) => {
      const amount = Math.min(1, Math.max(0, (now - start) / 1450));
      setValue(Math.round(from + (to - from) * (1 - (1 - amount) ** 3)));
      if (amount < 1) frame = requestAnimationFrame(tick);
    };
    frame = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frame);
  }, [from, to, reduced]);
  return <><span className="setup-points-number" aria-hidden="true">{value}</span><span className="sr-only">{to} target points, from {from} current points</span></>;
}

export default function SetupFlow({ userId, userName, onComplete, onSkip, mode = 'fresh', transitionTargetYear }: OnboardingProps) {
  const transition = mode === 'transition-to-senior';
  const [draft, setDraft] = useState(() => readDraft(userId, mode, transition ? transitionTargetYear ?? '5th' : undefined));
  const [query, setQuery] = useState('');
  const [subjectGroup, setSubjectGroup] = useState('languages');
  const [visionGroup, setVisionGroup] = useState<string>('');
  const [editSnapshot, setEditSnapshot] = useState<SetupDraft | null>(null);
  const [pendingYear, setPendingYear] = useState<YearGroup | null>(null);
  const [saving, setSaving] = useState(false);
  const [saveError, setSaveError] = useState('');
  const scroller = useRef<HTMLDivElement>(null);
  const yearDialog = useRef<HTMLElement>(null);
  useModal(Boolean(pendingYear), () => setPendingYear(null), yearDialog);
  const heading = useRef<HTMLHeadingElement>(null);
  const savingRef = useRef(false);
  const latest = useRef(draft);
  const reduced = useReducedMotion();
  const junior = cycleFor(draft.year) === 'junior';
  const lca = isLcaYear(draft.year ?? undefined);
  const categories = getActiveCategories(cycleFor(draft.year));
  const category = categories.find(c => c.id === draft.category);
  const visions = getVisionCardsForLevel(cycleFor(draft.year));
  const maxVision = junior ? 3 : 5;
  const subjectList = subjectsFor(draft.year);
  const currentSubject = draft.gradeSubject && draft.subjects.includes(draft.gradeSubject) ? draft.gradeSubject : draft.subjects[0];
  const subjectIndex = draft.subjects.indexOf(currentSubject);
  const nextSubject = draft.subjects[subjectIndex + 1];
  const gradeStepSubject = draft.step === 'grades' ? currentSubject : null;
  const config = draft.configs[currentSubject] ?? emptyChoice(draft.year, currentSubject);
  const gradeChoices = choicesFor(draft.year, config.level);
  const unreviewed = draft.subjects.filter(name => !draft.configs[name]?.reviewed);
  const points = pointsFor(draft);
  const studyDays = DAYS_OF_WEEK.filter(day => !draft.rest.includes(day));
  const route: SetupStep[] = transition ? ['subjects', 'grades', 'north', 'vision', 'schedule', 'summary'] : ['welcome', 'year', 'north', 'vision', 'subjects', ...(lca ? [] : ['grades' as const]), 'schedule', 'summary'];
  const stage = transition ? Math.max(1, route.indexOf(draft.step) + 1) : ({ welcome: 1, year: 2, north: 3, vision: 3, subjects: 4, grades: 5, schedule: lca ? 5 : 6, summary: lca ? 6 : 7 })[draft.step];
  const stages = transition ? route.length : lca ? 6 : 7;
  const surface = draft.step === 'summary' ? 'ink' : ['welcome', 'north', 'schedule'].includes(draft.step) ? 'orange' : 'paper';
  const patch = (value: Partial<SetupDraft>) => setDraft(prev => ({ ...prev, ...value }));

  // Persist before painting. While editing a review section, reload restores the
  // last committed review, not a half-finished edit with no Cancel route.
  useLayoutEffect(() => {
    latest.current = editSnapshot ?? draft;
    try { localStorage.setItem(draftKey(userId, mode), JSON.stringify(latest.current)); } catch { /* Private browsing may block storage. */ }
  }, [draft, editSnapshot, userId, mode]);
  useEffect(() => {
    const persist = () => { try { localStorage.setItem(draftKey(userId, mode), JSON.stringify(latest.current)); } catch { /* Keep the in-memory draft. */ } };
    window.addEventListener('pagehide', persist);
    document.addEventListener('visibilitychange', persist);
    return () => { window.removeEventListener('pagehide', persist); document.removeEventListener('visibilitychange', persist); };
  }, [userId, mode]);
  useLayoutEffect(() => {
    if (scroller.current) scroller.current.scrollTop = 0;
    heading.current?.focus({ preventScroll: true });
  }, [draft.step, gradeStepSubject]);
  useEffect(() => {
    const region = scroller.current;
    if (!region) return;
    let x = 0, y = 0;
    const start = (event: TouchEvent) => { const touch = event.touches[0]; if (touch) { x = touch.clientX; y = touch.clientY; } };
    const move = (event: TouchEvent) => {
      const touch = event.touches[0];
      if (!touch || Math.abs(touch.clientY - y) <= Math.abs(touch.clientX - x)) return;
      if ((region.scrollTop <= 0 && touch.clientY > y) || (Math.ceil(region.scrollTop + region.clientHeight) >= region.scrollHeight && touch.clientY < y)) event.preventDefault();
    };
    region.addEventListener('touchstart', start, { passive: true });
    region.addEventListener('touchmove', move, { passive: false });
    return () => { region.removeEventListener('touchstart', start); region.removeEventListener('touchmove', move); };
  }, []);
  useEffect(() => { trackFunnel('onboarding_started'); }, []);
  useEffect(() => {
    if (draft.step === 'subjects') trackFunnel('onboarding_reached_subjects');
    if (draft.step === 'schedule') trackFunnel('onboarding_reached_exam_date');
  }, [draft.step]);

  const edit = (step: SetupStep, subject?: string) => {
    setEditSnapshot(draft);
    setSaveError('');
    patch({ step, ...(subject ? { gradeSubject: subject } : {}) });
  };
  const cancelEdit = () => { if (editSnapshot) setDraft(editSnapshot); setEditSnapshot(null); setSaveError(''); };
  const changeYear = (year: YearGroup) => {
    const different = cycleFor(year) !== cycleFor(draft.year) || isLcaYear(year) !== lca;
    if (different) {
      patch({ year, subjects: [], configs: {}, category: null, vision: [], gradeSubject: null, dateConfirmed: false });
      setSubjectGroup('languages'); setVisionGroup('');
    } else patch({ year, dateConfirmed: false });
    setPendingYear(null);
  };
  const selectYear = (year: YearGroup) => {
    if (draft.year && (draft.subjects.length || draft.category) && (cycleFor(year) !== cycleFor(draft.year) || isLcaYear(year) !== lca)) setPendingYear(year);
    else changeYear(year);
  };
  const toggleSubject = (name: string) => setDraft(prev => ({ ...prev, subjects: prev.subjects.includes(name) ? prev.subjects.filter(s => s !== name) : [...prev.subjects, name], configs: { ...prev.configs, [name]: prev.configs[name] ?? emptyChoice(prev.year, name) } }));
  const updateGrade = (value: Partial<SubjectChoice>) => setDraft(prev => ({ ...prev, configs: { ...prev.configs, [currentSubject]: { ...config, ...value, reviewed: false } } }));
  const saveGrade = (later = false) => {
    const nextConfig = { ...config, ...(later ? { current: 'later' as const, target: 'later' as const } : {}), reviewed: true };
    if (!choiceReady(draft.year, nextConfig)) return;
    const nextName = nextSubject;
    patch({ configs: { ...draft.configs, [currentSubject]: nextConfig }, gradeSubject: editSnapshot ? currentSubject : nextName ?? currentSubject, step: editSnapshot ? 'summary' : nextName ? 'grades' : transition ? 'north' : 'schedule' });
    setEditSnapshot(null);
  };
  const validation = () => {
    if (draft.step === 'year' && !draft.year) return 'Choose your school year to continue.';
    if (draft.step === 'north' && !category) return 'Choose the reason that matters most to you.';
    if (draft.step === 'vision' && !draft.vision.length) return 'Choose at least one idea. You can change it later.';
    if (draft.step === 'subjects' && !draft.subjects.length) return 'Choose at least one subject.';
    if (draft.step === 'grades' && !config.level) return 'Choose your level. Grades can be added later.';
    if (draft.step === 'grades' && !choiceReady(draft.year, config)) return 'Choose your grades, or set them later.';
    if (draft.step === 'schedule' && !studyDays.length) return 'Choose at least one study day.';
    if (draft.step === 'schedule' && needsDate(draft.year) && !(daysUntil(draft.date) > 0)) return 'Choose a future exam date.';
    if (draft.step === 'schedule' && needsDate(draft.year) && !draft.dateConfirmed) return 'Confirm your exam date to continue.';
    if (draft.step === 'summary') {
      if (!draft.year || !draft.subjects.length || !category || !draft.vision.length) return 'Finish your year, subjects and motivation before starting.';
      if (!lca && unreviewed.length) return `Review ${unreviewed.length === 1 ? 'the remaining subject' : `${unreviewed.length} remaining subjects`}. Grades can be set later.`;
      if (!studyDays.length || (needsDate(draft.year) && (!draft.dateConfirmed || !(daysUntil(draft.date) > 0)))) return 'Review your study days and exam date.';
    }
    return '';
  };
  const problem = validation();
  const next = async () => {
    if (problem || savingRef.current) return;
    if (draft.step === 'grades') { saveGrade(); return; }
    if (editSnapshot) { patch({ step: 'summary' }); setEditSnapshot(null); return; }
    if (draft.step === 'summary') {
      savingRef.current = true; setSaving(true); setSaveError('');
      try {
        await onComplete(buildProfile(draft), buildNorthStar(draft), false);
        trackFunnel('onboarding_completed');
        // Keep this account-scoped draft for a delayed offline-write rollback.
        // The app's completed-onboarding gate, not local storage, owns success.
      } catch { setSaveError('We couldn’t save your setup. Your answers are still here. Please try again.'); }
      finally { savingRef.current = false; setSaving(false); }
      return;
    }
    const step = route[route.indexOf(draft.step) + 1];
    patch({ step, ...(step === 'grades' ? { gradeSubject: unreviewed[0] ?? draft.subjects[0] } : {}) });
  };
  const back = () => {
    if (editSnapshot) { cancelEdit(); return; }
    if (draft.step === 'grades' && subjectIndex > 0) {
      patch({ gradeSubject: draft.subjects[subjectIndex - 1] });
      return;
    }
    if (draft.step === 'welcome') {
      trackFunnel('onboarding_skipped');
      try { localStorage.removeItem(draftKey(userId, mode)); localStorage.removeItem(legacyDraftKey(userId, mode)); } catch { /* Optional storage. */ }
      onSkip(); return;
    }
    patch({ step: route[Math.max(0, route.indexOf(draft.step) - 1)] });
  };
  const title = ({ welcome: 'Make your mark.', year: 'Where are you now?', north: 'What’s driving you?', vision: 'Picture your future.', subjects: 'Make it yours.', grades: currentSubject || 'Your grades.', schedule: 'Make room for progress.', summary: `You’re ready, ${userName.trim().split(/\s+/)[0] || 'let’s go'}.` })[draft.step];
  const intro = ({ welcome: 'Your future. Your next step.', year: 'Your starting point', north: 'Your North Star · 1 of 2', vision: 'Your North Star · 2 of 2', subjects: 'Your subjects', grades: `Subject ${Math.max(1, draft.subjects.indexOf(currentSubject) + 1)} of ${draft.subjects.length}`, schedule: 'A rhythm that works for you', summary: 'This is your starting line' })[draft.step];
  const gradeLabel = (name: string) => {
    const value = draft.configs[name];
    if (!value?.reviewed) return 'Not reviewed';
    const format = (grade: string) => grade === 'later' ? 'Set later' : grade;
    return hasGrades(draft.year, value) ? `${value.current} → ${value.target}` : `${format(value.current)} → ${format(value.target)}`;
  };

  return <div className="setup-flow" data-step={draft.step} data-surface={surface} data-prevent-pull-to-refresh="true" data-reduced-motion={Boolean(reduced)}>
    <div ref={scroller} className="setup-scroller" data-testid="onboarding-scroll-region">
      <div className="setup-shell">
        <header className="setup-brand"><span>nextstepuni</span><span>{String(stage).padStart(2, '0')} / {String(stages).padStart(2, '0')}</span></header>
        <div className="setup-progress" role="progressbar" aria-label="Onboarding progress" aria-valuemin={0} aria-valuemax={stages} aria-valuenow={stage}>{Array.from({ length: stages }, (_, i) => <span key={i} data-complete={i < stage} />)}</div>
        <main className="setup-content" key={`${draft.step}-${draft.step === 'grades' ? currentSubject : ''}`}>
          <p className="setup-eyebrow">{intro}</p>
          <h1 ref={heading} tabIndex={-1} className={draft.step === 'welcome' ? 'setup-welcome-title' : ''}>{title}</h1>
          {draft.step === 'welcome' && <><p className="setup-lead">A little more direction.<br />A lot more possibility.</p><img className="setup-art setup-welcome-art" src="/icons/onboarding/north-star.png" alt="" /><p className="setup-description">Choose what matters to you, add your subjects, and make a plan that fits your week.</p></>}
          {draft.step === 'year' && <><p className="setup-description">We’ll match your subjects and tools to your school year.</p>{([{ label: 'Junior Cycle', years: ['1st', '2nd', '3rd'] }, { label: 'Senior Cycle', years: ['TY', '5th', '6th'] }, { label: 'Leaving Cert Applied', years: ['LCA1', 'LCA2'] }] as const).map(group => <fieldset key={group.label}><legend className="setup-label">{group.label}</legend><div className={`setup-years ${group.years.length === 2 ? 'setup-two' : ''}`}>{group.years.map(year => <button type="button" className="setup-choice setup-year" key={year} aria-label={year === 'TY' ? 'Transition Year' : year.startsWith('LCA') ? `Leaving Cert Applied ${year === 'LCA1' ? 'Year 1' : 'Year 2'}` : `${year} Year`} aria-pressed={draft.year === year} onClick={() => selectYear(year)}><strong>{year.startsWith('LCA') ? year === 'LCA1' ? 'Year 1' : 'Year 2' : year}</strong><span>{year === 'TY' ? 'Transition Year' : year.startsWith('LCA') ? 'Leaving Cert Applied' : 'Year'}</span></button>)}</div></fieldset>)}</>}
          {draft.step === 'north' && <>
            <div className="setup-motivation-art" key={category?.id ?? 'direction'}>
              <img className="setup-art" src={category ? NORTH_STAR_CATEGORY_BLOBS[category.id].iconPath : '/icons/onboarding/north-star.png'} alt={category ? `${category.label} illustration` : 'Find your direction illustration'} />
              <span className="setup-art-label">{category?.label ?? 'Find your direction'}</span>
            </div>
            <p className="setup-description">{junior ? 'Everyone has a reason for putting in the work. What’s yours?' : lca ? 'Everyone has a reason for putting in the work. Pick the one that feels most like yours.' : 'Everyone has a reason for doing the Leaving Cert. Pick the one that feels most like yours.'}</p>
            <div className="setup-grid">{categories.map((item, index) => <button type="button" className="setup-choice setup-motivation" key={item.id} aria-pressed={draft.category === item.id} onClick={() => { patch({ category: item.id }); setVisionGroup(item.id); }}><span className="setup-choice-number" aria-hidden="true">{String(index + 1).padStart(2, '0')}</span><span>{item.label}</span></button>)}</div>
            <p className="setup-description setup-selected-description" aria-live="polite">{category?.description || 'Choose the one that feels like you.'}</p>
          </>}
          {draft.step === 'vision' && <><p className="setup-description">Choose 1–{maxVision} things you’d love to make happen. One is enough to start.</p><label className="setup-field"><span>Explore ideas</span><select value={visionGroup || draft.category || categories[0].id} onChange={event => setVisionGroup(event.target.value)}>{categories.map(item => <option key={item.id} value={item.id}>{item.label}</option>)}</select></label><div className="setup-tray">{visions.filter(item => draft.vision.includes(item.id)).map(item => <button type="button" key={item.id} className="setup-chip" onClick={() => patch({ vision: draft.vision.filter(id => id !== item.id) })} aria-label={`Remove ${item.label}`}>{item.label}<X size={13} aria-hidden="true" /></button>)}</div><div className="setup-list">{visions.filter(item => item.category === (visionGroup || draft.category || categories[0].id)).map(item => { const selected = draft.vision.includes(item.id); return <button type="button" key={item.id} className="setup-choice setup-vision" aria-pressed={selected} disabled={!selected && draft.vision.length >= maxVision} onClick={() => patch({ vision: selected ? draft.vision.filter(id => id !== item.id) : [...draft.vision, item.id] })}><img src={VISION_CARD_ART[item.id]} alt="" /><span>{item.label}</span></button>; })}</div><p className="setup-description setup-selection-count" aria-live="polite">{draft.vision.length} of {maxVision} selected</p></>}
          {draft.step === 'subjects' && <><p className="setup-description">The subjects you take now. You can change these later.</p><div className="setup-subject-hero" data-compact={draft.subjects.length > 0}><img className="setup-art" src="/icons/onboarding/subjects.png" alt="" /><div><strong>{draft.subjects.length}</strong><p>subjects selected</p></div></div><label className="setup-field"><span>Find a subject</span><input type="search" placeholder="Search subjects" value={query} onChange={event => setQuery(event.target.value)} /></label>{!query.trim() && <label className="setup-field"><span>Subject group</span><select value={subjectGroup} onChange={event => setSubjectGroup(event.target.value)}>{Object.entries(SUBJECT_GROUP_LABELS).filter(([key]) => subjectList.some(s => s.group === key)).map(([key, label]) => <option value={key} key={key}>{label}</option>)}</select></label>}<div className="setup-tray">{draft.subjects.map(name => <button type="button" className="setup-chip" key={name} aria-label={`Remove ${name}`} onClick={() => toggleSubject(name)}>{name}<X size={13} aria-hidden="true" /></button>)}</div><div className="setup-list">{subjectList.filter(item => query.trim() ? item.name.toLocaleLowerCase().includes(query.trim().toLocaleLowerCase()) : item.group === subjectGroup).map(item => <button type="button" className="setup-choice setup-subject" key={item.name} aria-pressed={draft.subjects.includes(item.name)} onClick={() => toggleSubject(item.name)}><span>{item.name}</span><span aria-hidden="true">{draft.subjects.includes(item.name) ? '−' : '+'}</span></button>)}</div>{query.trim() && !subjectList.some(s => s.name.toLocaleLowerCase().includes(query.trim().toLocaleLowerCase())) && <p className="setup-description">No subjects found. Try another name or <button type="button" className="setup-text" onClick={() => setQuery('')}>clear the search</button>.</p>}</>}
          {draft.step === 'grades' && <><p className="setup-description">Where you are now, and where you’d like to be. It’s okay if you don’t know yet.</p>{config.level !== 'common' && <fieldset><legend className="setup-label">Your level</legend><div className="setup-levels">{(['higher', 'ordinary'] as Level[]).map(level => <button type="button" key={level} className="setup-chip" aria-pressed={config.level === level} onClick={() => updateGrade({ level, ...(junior ? {} : { current: '', target: '' }) })}>{level === 'higher' ? 'Higher' : 'Ordinary'}</button>)}</div></fieldset>}<div className="setup-grade-graphic" aria-hidden="true">{(['current', 'target'] as const).map(field => { const index = gradeChoices.indexOf(config[field]); const height = index < 0 ? 0 : Math.max(10, ((gradeChoices.length - index) / gradeChoices.length) * 100); return <div className="setup-grade-column" key={field}><div className="setup-grade-rail"><span data-target={field === 'target'} style={{ height: `${height}%` }} /></div><strong>{config[field] && config[field] !== 'later' ? config[field] : '—'}</strong></div>; })}</div><div className={`setup-grade-pickers ${junior ? 'setup-stack' : ''}`}>{(['current', 'target'] as const).map(field => <label className="setup-field" key={field}><span>{field === 'current' ? 'Current' : 'Target'} {junior ? 'band' : 'grade'}</span><select disabled={!config.level} value={config[field]} onChange={event => updateGrade({ [field]: event.target.value as GradeChoice })}><option value="" disabled>Choose {junior ? 'band' : 'grade'}</option>{gradeChoices.map(grade => <option key={grade} value={grade}>{grade}</option>)}<option value="later">I don’t know yet</option></select></label>)}</div><button type="button" className="setup-text setup-defer" disabled={!config.level} onClick={() => saveGrade(true)}>Set these grades later</button><p className="setup-description">{config.level ? 'Your level is saved even if you leave grades for later.' : 'We need your level to show the right papers. No grades are filled in for you.'}</p></>}
          {draft.step === 'schedule' && <>{needsDate(draft.year) && <><p className="setup-description">A date to work towards. Check that this is the right one for you.</p><label className="setup-field"><span>Your exam date</span><input type="date" value={draft.date} onChange={event => patch({ date: event.target.value, dateConfirmed: false })} /></label>{daysUntil(draft.date) > 0 && <div className="setup-countdown"><strong>{daysUntil(draft.date)}</strong><span>days<br />to go</span></div>}<label className="setup-confirm"><input type="checkbox" checked={draft.dateConfirmed} onChange={event => patch({ dateConfirmed: event.target.checked })} /><span>This is the right date for me.</span></label></>}<fieldset className="setup-week-field"><legend className="setup-label">Which days can you study?</legend><p className="setup-description">Tap the days that work for you. Keep the others free.</p><div className="setup-week">{DAYS_OF_WEEK.map(day => { const selected = !draft.rest.includes(day); return <button type="button" className="setup-day" key={day} aria-pressed={selected} aria-label={`${day}, ${selected ? 'study' : 'rest'} day`} onClick={() => setDraft(prev => ({ ...prev, rest: prev.rest.includes(day) ? prev.rest.filter(d => d !== day) : [...prev.rest, day] }))}><span>{day.slice(0, 3)}</span><span className="setup-day-state">{selected ? 'Study' : 'Rest'}</span></button>; })}</div></fieldset><p className="setup-description setup-selection-count" aria-live="polite">{studyDays.length ? `${studyDays.map(d => d.slice(0, 3)).join(', ')} · ${studyDays.length} study ${studyDays.length === 1 ? 'day' : 'days'} a week` : 'Choose your study days.'}</p></>}
          {draft.step === 'summary' && <><p className="setup-lead">Review your plan, then start learning.</p>{!junior && !lca && <section className="setup-points" aria-label="Your points target">{points.count ? <><p className="setup-eyebrow">{points.count < draft.subjects.length ? 'Your points target so far' : 'Your points target'}</p><PointsCount from={points.current} to={points.target} /><p className="setup-description">{points.count < draft.subjects.length ? `Based on ${points.count} of your ${draft.subjects.length} subjects. Remaining grades can be added later.` : points.count > 6 ? `Best six of your ${points.count} subjects.` : `Based on your ${points.count} ${points.count === 1 ? 'subject' : 'subjects'}.`}</p></> : <p className="setup-description">Your points will appear as you add grades.</p>}</section>}<section className="setup-review-section"><div className="setup-review-heading"><h2>Your subjects{lca ? '' : ' & goals'}</h2><button type="button" className="setup-text" onClick={() => edit('subjects')}>Edit subjects</button></div>{draft.subjects.map(name => <div className="setup-review-subject" key={name}><span>{name}{!lca && <small>{gradeLabel(name)}</small>}</span>{!lca && <button type="button" className="setup-text" aria-label={`Edit ${name} grades`} onClick={() => edit('grades', name)}>Edit</button>}</div>)}</section><section className="setup-review-section"><div className="setup-review-heading"><h2>Your week</h2><button type="button" className="setup-text" onClick={() => edit('schedule')}>Edit schedule</button></div><dl className="setup-review-details"><div><dt>Study days</dt><dd>{studyDays.map(d => d.slice(0, 3)).join(', ') || 'None selected'}</dd></div><div><dt>Rest days</dt><dd>{DAYS_OF_WEEK.filter(d => draft.rest.includes(d)).map(d => d.slice(0, 3)).join(', ') || 'None selected'}</dd></div>{needsDate(draft.year) && <div><dt>Exam date</dt><dd>{Number.isFinite(daysUntil(draft.date)) ? new Date(`${draft.date}T12:00:00`).toLocaleDateString('en-IE', { day: 'numeric', month: 'long', year: 'numeric' }) : 'Choose a date'}{!draft.dateConfirmed && ' · Not confirmed'}</dd></div>}</dl></section><section className="setup-review-section"><div className="setup-review-heading"><h2>Your North Star</h2><button type="button" className="setup-text" onClick={() => edit('north')}>Edit motivation</button></div><p className="setup-statement">{category?.label || 'Choose your motivation'}</p><p className="setup-description">{category?.description}</p><div className="setup-review-heading"><h2>Your vision board</h2><button type="button" className="setup-text" onClick={() => edit('vision')}>Edit ideas</button></div><p className="setup-description">{visions.filter(v => draft.vision.includes(v.id)).map(v => v.label).join(' · ') || 'Choose at least one idea.'}</p></section></>}
        </main>
      </div>
    </div>
    <footer className="setup-footer">
      <p className="setup-validation" id="setup-validation" aria-live="polite">{saveError || problem}</p>
      <button type="button" className="setup-continue" disabled={Boolean(problem) || saving} aria-describedby="setup-validation" onClick={() => void next()}><span>{saving ? 'Saving your plan…' : draft.step === 'welcome' ? 'Get Started' : draft.step === 'summary' ? 'Start Learning' : editSnapshot ? 'Save and review' : draft.step === 'grades' ? nextSubject ? 'Next subject' : transition ? 'Continue' : 'Continue to schedule' : 'Continue'}</span><ArrowUpRight size={24} aria-hidden="true" /></button>
      <div className="setup-footer-links">{(!transition || draft.step !== 'subjects' || editSnapshot) && <button type="button" className="setup-back" disabled={saving} onClick={back}>{draft.step !== 'welcome' && <ArrowLeft size={15} aria-hidden="true" />}{editSnapshot ? 'Cancel edits' : draft.step === 'welcome' ? 'Skip for now' : 'Back'}</button>}<span>{draft.step === 'welcome' ? 'Grades can wait' : 'Your answers stay as you go back'}</span></div>
    </footer>
    {pendingYear && <div className="setup-dialog-backdrop"><section ref={yearDialog} role="alertdialog" aria-modal="true" aria-labelledby="setup-year-warning" className="setup-dialog"><h2 id="setup-year-warning">Change your school programme?</h2><p>Your subjects, grades and vision choices belong to a different programme. Changing will clear those choices from this draft.</p><button type="button" autoFocus className="setup-continue" onClick={() => setPendingYear(null)}>Keep my choices</button><button type="button" className="setup-text" onClick={() => changeYear(pendingYear)}>Change programme and clear choices</button></section></div>}
  </div>;
}
