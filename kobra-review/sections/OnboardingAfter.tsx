/**
 * Onboarding, rebuilt on Kobra (AFTER for the wave 1 / 2 review, 27 Oct 2026).
 *
 * The behaviour is the app's own: this view runs the REAL hook,
 * components/onboarding/useSetupFlow.tsx, so every step, title, eyebrow,
 * validation line, stage count and button label below comes from the same
 * code SetupFlow.tsx renders today. Only the view is new:
 *  - the step count is a Kobra Progress (was 7 hand-drawn segments);
 *  - "Explore ideas" and "Subject group" are the house pill Tabs (were native selects);
 *  - subjects are square Kobra Checkbox rows (were Add / Added buttons with an orange border);
 *  - year, motivation, level, grade and day choices are Kobra ToggleGroups;
 *  - the grade pickers are ToggleGroups of every grade (were a Select each; the
 *    desktop sheet's range slider in GradeOptions.tsx goes the same way);
 *  - the exam date is a Kobra Input type=date: Kobra's Calendar is purchased but
 *    NOT compiled into the runtime, so it needs compiling before a calendar can replace it;
 *  - "This is the right date for me." is a square Kobra Checkbox (was a native checkbox);
 *  - the programme-change warning is the Kobra Dialog (was a hand-built alertdialog).
 * One selected treatment: on paper, a chosen card is the orange face with dark
 * text and a chosen list row takes the ink ring; on the orange steps (where an
 * orange face cannot show) the chosen card is the ink face, as today.
 *
 * OPEN DECISION FOR ALEX: the full-orange welcome, North Star and schedule
 * steps are kept exactly as they are. Whether they stay is his call; nothing
 * here decides it.
 *
 * The appearance cards on the summary are the real AppearanceChoice (the two
 * app miniatures with the ink border and check, kept by standing decision),
 * and "How do points work?" is the real PointsGuide, already on Kobra.
 * Sample answers only; nothing is saved to an account.
 */
import { useId, useState, type ReactNode } from 'react';
import { ArrowLeft, ArrowUpRight, Check, Volume2, VolumeX, X } from 'lucide-react';
import KobraScope, {
  Button, Checkbox, Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, Input, Progress,
  Select, SelectContent, SelectItem, SelectTrigger, SelectValue, Tabs, TabsList, TabsTrigger,
  ToggleGroup, ToggleGroupItem, setSoundMuted, toast, useSoundMuted,
} from '../../components/approved-ui-runtime';
import { useSetupFlow, PointsCount } from '../../components/onboarding/useSetupFlow';
import { daysUntil, gradeBarHeight, needsDate, type GradeChoice, type SetupStep } from '../../components/onboarding/model';
import AppearanceChoice from '../../components/onboarding/AppearanceChoice';
import PointsGuide from '../../components/onboarding/PointsGuide';
import SubjectAvatar from '../../components/SubjectAvatar';
import { DAYS_OF_WEEK, LEVEL_LABELS, SUBJECT_GROUP_LABELS, subjectMatchesQuery, type YearGroup } from '../../components/subjectData';
import { VISION_CARD_ART } from '../../northStarData';
import { NORTH_STAR_CATEGORY_BLOBS } from '../../components/NorthStarCategoryIcon';
import { SAMPLE_NAME, SAMPLE_STEPS, seedSampleDraft, silenceFunnel } from './onboarding-sample';
import './onboarding.css';

silenceFunnel();

const USER_ID = 'kobra-review-kobra';
const pageParams = new URLSearchParams(window.location.search);
const FIRST_STEP = (SAMPLE_STEPS.find(item => item.step === pageParams.get('ob'))?.step ?? 'welcome') as SetupStep;
seedSampleDraft(USER_ID, FIRST_STEP);

const YEAR_GROUPS = [
  { label: 'Junior Cycle', years: ['1st', '2nd', '3rd'] },
  { label: 'Senior Cycle', years: ['TY', '5th', '6th'] },
  { label: 'Leaving Cert Applied', years: ['LCA1', 'LCA2'] },
] as const;

const yearAria = (year: string) => year === 'TY'
  ? 'Transition Year'
  : year.startsWith('LCA') ? `Leaving Cert Applied ${year === 'LCA1' ? 'Year 1' : 'Year 2'}` : `${year} Year`;

/** The house pill: Kobra Tabs as a grey tray; it wraps on a phone. */
function PillTabs({ label, value, options, onChange }: {
  label: string; value: string; options: { value: string; label: string }[]; onChange: (value: string) => void;
}) {
  return (
    <Tabs value={value} onValueChange={next => onChange(String(next))} className="kr-ob-tabs">
      <TabsList aria-label={label}>
        {options.map(option => <TabsTrigger key={option.value} value={option.value}>{option.label}</TabsTrigger>)}
      </TabsList>
    </Tabs>
  );
}

function SoundToggle() {
  const muted = useSoundMuted();
  if (typeof globalThis.AudioContext !== 'function') return null;
  return (
    <Button
      variant="outline"
      className="nsu-ink-outline kr-ob-sound"
      aria-label={muted ? 'Turn interface sound on' : 'Turn interface sound off'}
      aria-pressed={!muted}
      title={muted ? 'Sound off' : 'Sound on'}
      data-sound="swoosh"
      onClick={() => setSoundMuted(!muted)}
    >
      {muted ? <VolumeX aria-hidden="true" /> : <Volume2 aria-hidden="true" />}
      <span>Sound {muted ? 'off' : 'on'}</span>
    </Button>
  );
}

function Flow({ onRestart }: { onRestart: (step: SetupStep) => void }) {
  const ids = useId();
  const {
    draft, setDraft, patch, query, setQuery, subjectGroup, setSubjectGroup, visionGroup, setVisionGroup,
    editSnapshot, pendingYear, setPendingYear, saving, saveError, scroller, heading, yearDialog, junior, lca,
    categories, category, visions, maxVision, subjectList, nextSubject, config, gradeChoices, targetChoices,
    levelChoices, levelNote, points, studyDays, stage, stages, surface, edit, updateGrade, saveGrade, changeYear,
    selectYear, toggleSubject, problem, next, back, title, intro, gradeLabel, transition, guest,
  } = useSetupFlow({
    userId: USER_ID,
    userName: SAMPLE_NAME,
    onComplete: async () => {
      toast({ message: 'Start Learning saves this plan and opens the app. The review starts again.' });
      onRestart('welcome');
    },
    onSkip: () => {
      toast({ message: 'Skip for now opens the app without a plan. The review starts again.' });
      onRestart('welcome');
    },
  });

  const exploreValue = visionGroup || draft.category || categories[0].id;
  const groups = Object.entries(SUBJECT_GROUP_LABELS).filter(([key]) => subjectList.some(s => s.group === key));
  const shownSubjects = subjectList.filter(item => (query.trim() ? subjectMatchesQuery(item, query) : item.group === subjectGroup));

  const continueLabel = saving
    ? 'Saving your plan…'
    : draft.step === 'welcome'
      ? 'Get Started'
      : draft.step === 'summary'
        ? guest ? 'Dive in' : 'Start Learning'
        : editSnapshot
          ? 'Save and review'
          : draft.step === 'grades'
            ? nextSubject ? 'Next subject' : transition ? 'Continue' : 'Continue to schedule'
            : 'Continue';

  let body: ReactNode = null;
  if (draft.step === 'welcome') {
    body = (
      <>
        <p className="kr-ob-lead">A little more direction.<br />A lot more possibility.</p>
        <img className="kr-ob-art kr-ob-welcome-art" src="/icons/onboarding/north-star.png" alt="" />
        <p className="kr-ob-description">Choose what matters to you, add your subjects, and make a plan that fits your week.</p>
      </>
    );
  } else if (draft.step === 'year') {
    body = (
      <>
        <p className="kr-ob-description">We’ll match your subjects and tools to your school year.</p>
        {YEAR_GROUPS.map(group => (
          <fieldset key={group.label} className="kr-ob-fieldset">
            <legend className="kr-ob-label">{group.label}</legend>
            <ToggleGroup
              className="kr-ob-cards kr-ob-years"
              data-count={group.years.length}
              value={draft.year && (group.years as readonly string[]).includes(draft.year) ? [draft.year] : []}
              onValueChange={values => { if (values[0]) selectYear(values[0] as YearGroup); }}
            >
              {group.years.map(year => (
                <ToggleGroupItem key={year} value={year} aria-label={yearAria(year)} className="kr-ob-card kr-ob-year">
                  <strong>{year.startsWith('LCA') ? (year === 'LCA1' ? 'Year 1' : 'Year 2') : year}</strong>
                  <span>{year === 'TY' ? 'Transition Year' : year.startsWith('LCA') ? 'Leaving Cert Applied' : 'Year'}</span>
                </ToggleGroupItem>
              ))}
            </ToggleGroup>
          </fieldset>
        ))}
      </>
    );
  } else if (draft.step === 'north') {
    body = (
      <>
        <div className="kr-ob-motivation-art" key={category?.id ?? 'direction'}>
          <img
            className="kr-ob-art"
            src={category ? NORTH_STAR_CATEGORY_BLOBS[category.id].iconPath : '/icons/onboarding/north-star.png'}
            alt={category ? `${category.label} illustration` : 'Find your direction illustration'}
          />
          <span className="kr-ob-art-label">{category?.label ?? 'Find your direction'}</span>
        </div>
        <p className="kr-ob-description">
          {junior
            ? 'Everyone has a reason for putting in the work. What’s yours?'
            : lca
              ? 'Everyone has a reason for putting in the work. Pick the one that feels most like yours.'
              : 'Everyone has a reason for doing the Leaving Cert. Pick the one that feels most like yours.'}
        </p>
        <ToggleGroup
          className="kr-ob-cards kr-ob-motivations"
          aria-label={title}
          value={draft.category ? [draft.category] : []}
          onValueChange={values => {
            const id = values[0];
            if (!id) return;
            patch({ category: id as typeof draft.category });
            setVisionGroup(id);
          }}
        >
          {categories.map((item, index) => (
            <ToggleGroupItem key={item.id} value={item.id} className="kr-ob-card kr-ob-motivation">
              <span className="kr-ob-card-number" aria-hidden="true">{String(index + 1).padStart(2, '0')}</span>
              <span>{item.label}</span>
            </ToggleGroupItem>
          ))}
        </ToggleGroup>
        <p className="kr-ob-description kr-ob-selected-description" aria-live="polite">
          {category?.description || 'Choose the one that feels like you.'}
        </p>
      </>
    );
  } else if (draft.step === 'vision') {
    body = (
      <>
        <p className="kr-ob-description">Choose 1–{maxVision} things you’d love to make happen. One is enough to start.</p>
        <div className="kr-ob-field">
          <span className="kr-ob-label" aria-hidden="true">Explore ideas</span>
          <PillTabs
            label="Explore ideas"
            value={exploreValue}
            onChange={setVisionGroup}
            options={categories.map(item => ({ value: item.id, label: item.label }))}
          />
        </div>
        {draft.vision.length > 0 && (
          <div className="kr-ob-tray">
            {visions.filter(item => draft.vision.includes(item.id)).map(item => (
              <Button key={item.id} variant="outline" size="sm" className="nsu-ink-outline kr-ob-chip" aria-label={`Remove ${item.label}`}
                onClick={() => patch({ vision: draft.vision.filter(id => id !== item.id) })}>
                {item.label}<X aria-hidden="true" />
              </Button>
            ))}
          </div>
        )}
        <div className="kr-ob-list">
          {visions.filter(item => item.category === exploreValue).map(item => {
            const selected = draft.vision.includes(item.id);
            return (
              <button
                type="button"
                key={item.id}
                className="kr-ob-row kr-ob-vision"
                aria-pressed={selected}
                disabled={!selected && draft.vision.length >= maxVision}
                onClick={() => patch({ vision: selected ? draft.vision.filter(id => id !== item.id) : [...draft.vision, item.id] })}
              >
                <img src={VISION_CARD_ART[item.id]} alt="" />
                <span className="kr-ob-row-name">{item.label}</span>
                <span className="kr-ob-tick" aria-hidden="true">{selected && <Check />}</span>
              </button>
            );
          })}
        </div>
        <p className="kr-ob-description kr-ob-count" aria-live="polite">{draft.vision.length} of {maxVision} selected</p>
      </>
    );
  } else if (draft.step === 'subjects') {
    body = (
      <>
        <p className="kr-ob-description">The subjects you take now. You can change these later.</p>
        <div className="kr-ob-subject-hero" data-compact={draft.subjects.length > 0}>
          <img className="kr-ob-art" src="/icons/onboarding/subjects.png" alt="" />
          <div><strong>{draft.subjects.length}</strong><p>subjects selected</p></div>
        </div>
        <label className="kr-ob-field">
          <span className="kr-ob-label">Find a subject</span>
          <Input type="search" placeholder="Search subjects" value={query} onChange={event => setQuery(event.target.value)} className="kr-ob-input" />
        </label>
        {!query.trim() && (
          <div className="kr-ob-field">
            <span className="kr-ob-label" aria-hidden="true">Subject group</span>
            <PillTabs label="Subject group" value={subjectGroup} onChange={setSubjectGroup}
              options={groups.map(([key, label]) => ({ value: key, label }))} />
          </div>
        )}
        {draft.subjects.length > 0 && (
          <div className="kr-ob-tray">
            {draft.subjects.map(name => (
              <Button key={name} variant="outline" size="sm" className="nsu-ink-outline kr-ob-chip" aria-label={`Remove ${name}`} onClick={() => toggleSubject(name)}>
                {name}<X aria-hidden="true" />
              </Button>
            ))}
          </div>
        )}
        <div className="kr-ob-list">
          {shownSubjects.map(item => {
            const added = draft.subjects.includes(item.name);
            return (
              <label key={item.name} className="kr-ob-row kr-ob-subject" data-checked={added || undefined}>
                <SubjectAvatar subject={item.name} />
                <span className="kr-ob-row-name">{item.name}</span>
                <span className="kr-ob-subject-state" aria-hidden="true">{added ? 'Added' : 'Add'}</span>
                <Checkbox checked={added} onCheckedChange={() => toggleSubject(item.name)} />
              </label>
            );
          })}
        </div>
        {query.trim() && !subjectList.some(s => subjectMatchesQuery(s, query)) && (
          <p className="kr-ob-description">
            No subjects found. Try another name or{' '}
            <Button variant="link" className="kr-ob-link" onClick={() => setQuery('')}>clear the search</Button>.
          </p>
        )}
      </>
    );
  } else if (draft.step === 'grades') {
    const noun = junior ? 'band' : 'grade';
    body = (
      <>
        <p className="kr-ob-description">Where you are now, and where you’d like to be. It’s okay if you don’t know yet.</p>
        {levelChoices.length > 1 && (
          <fieldset className="kr-ob-fieldset">
            <legend className="kr-ob-label">Your level</legend>
            <ToggleGroup
              className="kr-ob-cards kr-ob-levels"
              value={config.level ? [config.level] : []}
              onValueChange={values => {
                const level = values[0] as typeof config.level;
                if (level) updateGrade({ level, ...(junior ? {} : { current: '', target: '' }) });
              }}
            >
              {levelChoices.map(level => <ToggleGroupItem key={level} value={level} className="kr-ob-card kr-ob-level">{LEVEL_LABELS[level]}</ToggleGroupItem>)}
            </ToggleGroup>
          </fieldset>
        )}
        {levelNote && <p className="kr-ob-description">{levelNote}</p>}
        {!junior && !lca && <PointsGuide draft={draft} />}
        <div className="kr-ob-grade-graphic" aria-hidden="true">
          {(['current', 'target'] as const).map(field => (
            <div className="kr-ob-grade-column" key={field}>
              <div className="kr-ob-grade-rail">
                <span data-target={field === 'target'} style={{ height: `${gradeBarHeight(draft.year, config[field], field === 'target' ? targetChoices : gradeChoices)}%` }} />
              </div>
              <strong>{config[field] && config[field] !== 'later' ? config[field] : '—'}</strong>
            </div>
          ))}
        </div>
        {(['current', 'target'] as const).map(field => {
          const label = `${field === 'current' ? 'Current' : 'Target'} ${noun}`;
          const choices = field === 'target' ? targetChoices : gradeChoices;
          return (
            <div className="kr-ob-field kr-ob-grade-field" key={field}>
              <span className="kr-ob-label" id={`${ids}-${field}`}>{label}</span>
              <ToggleGroup
                className="kr-ob-grades"
                aria-labelledby={`${ids}-${field}`}
                disabled={!config.level}
                value={config[field] ? [config[field]] : []}
                onValueChange={values => { if (values[0]) updateGrade({ [field]: values[0] as GradeChoice }); }}
              >
                {choices.map(grade => <ToggleGroupItem key={grade} value={grade} className="kr-ob-grade">{grade}</ToggleGroupItem>)}
                <ToggleGroupItem value="later" className="kr-ob-grade kr-ob-grade-later">I don’t know yet</ToggleGroupItem>
              </ToggleGroup>
              {!config.level && <p className="kr-ob-hint">Choose {noun}</p>}
            </div>
          );
        })}
        <Button variant="link" className="kr-ob-link kr-ob-defer" disabled={!config.level} onClick={() => saveGrade(true)}>
          Set these grades later
        </Button>
        <p className="kr-ob-description">
          {config.level
            ? 'Your level is saved even if you leave grades for later.'
            : 'We need your level to show the right papers. No grades are filled in for you.'}
        </p>
      </>
    );
  } else if (draft.step === 'schedule') {
    const days = daysUntil(draft.date);
    body = (
      <>
        {needsDate(draft.year) && (
          <>
            <p className="kr-ob-description">A date to work towards. Check that this is the right one for you.</p>
            <label className="kr-ob-field">
              <span className="kr-ob-label">Your exam date</span>
              {/* Kobra's Calendar is purchased but not compiled into the runtime
                  (needs compiling); until it is, the date is a Kobra Input. */}
              <Input type="date" value={draft.date} className="kr-ob-input kr-ob-date"
                onChange={event => patch({ date: event.target.value, dateConfirmed: false })} />
            </label>
            {days > 0 && (
              <div className="kr-ob-countdown">
                <strong>{days}</strong>
                <span>days<br />to go</span>
              </div>
            )}
            <label className="kr-ob-confirm">
              <Checkbox checked={draft.dateConfirmed} onCheckedChange={checked => patch({ dateConfirmed: Boolean(checked) })} />
              <span>This is the right date for me.</span>
            </label>
          </>
        )}
        <fieldset className="kr-ob-fieldset kr-ob-week-field">
          <legend className="kr-ob-label">Which days can you study?</legend>
          <p className="kr-ob-description">Tap the days that work for you. Keep the others free.</p>
          <ToggleGroup
            multiple
            className="kr-ob-week"
            value={DAYS_OF_WEEK.filter(day => !draft.rest.includes(day))}
            onValueChange={values => setDraft(prev => ({ ...prev, rest: DAYS_OF_WEEK.filter(day => !values.includes(day)) }))}
          >
            {DAYS_OF_WEEK.map(day => {
              const selected = !draft.rest.includes(day);
              return (
                <ToggleGroupItem key={day} value={day} className="kr-ob-day" aria-label={`${day}, ${selected ? 'study' : 'rest'} day`}>
                  <span>{day.slice(0, 3)}</span>
                  <span className="kr-ob-day-state">{selected ? 'Study' : 'Rest'}</span>
                </ToggleGroupItem>
              );
            })}
          </ToggleGroup>
        </fieldset>
        <p className="kr-ob-description kr-ob-count" aria-live="polite">
          {studyDays.length
            ? `${studyDays.map(d => d.slice(0, 3)).join(', ')} · ${studyDays.length} study ${studyDays.length === 1 ? 'day' : 'days'} a week`
            : 'Choose your study days.'}
        </p>
      </>
    );
  } else if (draft.step === 'summary') {
    body = (
      <>
        <p className="kr-ob-lead">Review your plan, then start learning.</p>
        {!junior && !lca && (
          <section className="kr-ob-points" aria-label="Your points target">
            {points.count ? (
              <>
                <p className="kr-ob-eyebrow">{points.count < draft.subjects.length ? 'Your points target so far' : 'Your points target'}</p>
                <PointsCount from={points.current} to={points.target} />
                <p className="kr-ob-description">
                  {points.count < draft.subjects.length
                    ? `Based on ${points.count} of your ${draft.subjects.length} subjects. Remaining grades can be added later.`
                    : points.count > 6
                      ? `Best six of your ${points.count} subjects.`
                      : `Based on your ${points.count} ${points.count === 1 ? 'subject' : 'subjects'}.`}
                </p>
              </>
            ) : <p className="kr-ob-description">Your points will appear as you add grades.</p>}
          </section>
        )}
        <section className="kr-ob-review">
          <div className="kr-ob-review-heading">
            <h2>Your subjects{lca ? '' : ' & goals'}</h2>
            <Button variant="link" className="kr-ob-link" onClick={() => edit('subjects')}>Edit subjects</Button>
          </div>
          {draft.subjects.map(name => (
            <div className="kr-ob-review-subject" key={name}>
              <span>{name}{!lca && <small>{gradeLabel(name)}</small>}</span>
              {!lca && <Button variant="link" className="kr-ob-link" aria-label={`Edit ${name} grades`} onClick={() => edit('grades', name)}>Edit</Button>}
            </div>
          ))}
        </section>
        <section className="kr-ob-review">
          <div className="kr-ob-review-heading">
            <h2>Your week</h2>
            <Button variant="link" className="kr-ob-link" onClick={() => edit('schedule')}>Edit schedule</Button>
          </div>
          <dl className="kr-ob-review-details">
            <div><dt>Study days</dt><dd>{studyDays.map(d => d.slice(0, 3)).join(', ') || 'None selected'}</dd></div>
            <div><dt>Rest days</dt><dd>{DAYS_OF_WEEK.filter(d => draft.rest.includes(d)).map(d => d.slice(0, 3)).join(', ') || 'None selected'}</dd></div>
            {needsDate(draft.year) && (
              <div>
                <dt>Exam date</dt>
                <dd>
                  {Number.isFinite(daysUntil(draft.date))
                    ? new Date(`${draft.date}T12:00:00`).toLocaleDateString('en-IE', { day: 'numeric', month: 'long', year: 'numeric' })
                    : 'Choose a date'}
                  {!draft.dateConfirmed && ' · Not confirmed'}
                </dd>
              </div>
            )}
          </dl>
        </section>
        <section className="kr-ob-review">
          <div className="kr-ob-review-heading">
            <h2>Your North Star</h2>
            <Button variant="link" className="kr-ob-link" onClick={() => edit('north')}>Edit motivation</Button>
          </div>
          <p className="kr-ob-statement">{category?.label || 'Choose your motivation'}</p>
          <p className="kr-ob-description">{category?.description}</p>
          <div className="kr-ob-review-heading">
            <h2>Your vision board</h2>
            <Button variant="link" className="kr-ob-link" onClick={() => edit('vision')}>Edit ideas</Button>
          </div>
          <p className="kr-ob-description">{visions.filter(v => draft.vision.includes(v.id)).map(v => v.label).join(' · ') || 'Choose at least one idea.'}</p>
        </section>
        <div className="kr-ob-appearance">
          <AppearanceChoice darkMode={draft.appearance === 'dark'} onChange={dark => patch({ appearance: dark ? 'dark' : 'light' })} disabled={saving} />
        </div>
      </>
    );
  }

  return (
    <div className="kr-ob-device" data-step={draft.step} data-surface={surface}>
      <div ref={scroller} className="kr-ob-scroller">
        <div className="kr-ob-shell">
          <header className="kr-ob-brand">
            <span>nextstepuni</span>
            <div className="kr-ob-tools">
              <SoundToggle />
              <span className="kr-ob-stage">{String(stage).padStart(2, '0')} / {String(stages).padStart(2, '0')}</span>
            </div>
          </header>
          {/* Kobra Progress for the step count (was seven drawn segments). */}
          <Progress className="kr-ob-progress" value={stage} max={stages} aria-label="Onboarding progress" />
          <main className="kr-ob-content" key={`${draft.step}-${draft.step === 'grades' ? draft.gradeSubject : ''}`}>
            <p className="kr-ob-eyebrow">{intro}</p>
            <h1 ref={heading} tabIndex={-1} className={draft.step === 'welcome' ? 'kr-ob-title kr-ob-welcome-title' : 'kr-ob-title'}>{title}</h1>
            {body}
          </main>
        </div>
      </div>
      <footer className="kr-ob-footer">
        <p className="kr-ob-validation" id={`${ids}-validation`} aria-live="polite">{saveError || problem}</p>
        <Button className="kr-ob-continue" disabled={Boolean(problem) || saving} aria-describedby={`${ids}-validation`} onClick={() => void next()}>
          <span>{continueLabel}</span>
          <ArrowUpRight aria-hidden="true" />
        </Button>
        <div className="kr-ob-footer-links">
          {(!transition || draft.step !== 'subjects' || editSnapshot) && (
            <Button variant="ghost" className="kr-ob-back" disabled={saving} onClick={back}>
              {draft.step !== 'welcome' && <ArrowLeft aria-hidden="true" />}
              {editSnapshot ? 'Cancel edits' : draft.step === 'welcome' ? 'Skip for now' : 'Back'}
            </Button>
          )}
          <span>{draft.step === 'welcome' ? 'Grades can wait' : 'Your answers stay as you go back'}</span>
        </div>
      </footer>

      {/* The programme-change warning as the Kobra Dialog (was a hand-built alertdialog). */}
      <Dialog open={Boolean(pendingYear)} onOpenChange={open => { if (!open) setPendingYear(null); }}>
        <DialogContent ref={yearDialog} role="alertdialog" size="sm" showCloseButton={false} className="kr-ob-dialog">
          <KobraScope className="kr-ob-portal">
            <DialogHeader>
              <DialogTitle className="kr-ob-dialog-title">Change your school programme?</DialogTitle>
              <DialogDescription className="kr-ob-dialog-text">
                Your subjects, grades and vision choices belong to a different programme. Changing will clear those choices from this draft.
              </DialogDescription>
            </DialogHeader>
            <div className="kr-ob-dialog-actions">
              <Button autoFocus className="kr-ob-dialog-keep" onClick={() => setPendingYear(null)}>Keep my choices</Button>
              <Button variant="outline" className="nsu-ink-outline kr-ob-dialog-change" onClick={() => { if (pendingYear) changeYear(pendingYear); }}>
                Change programme and clear choices
              </Button>
            </div>
          </KobraScope>
        </DialogContent>
      </Dialog>
    </div>
  );
}

export default function OnboardingAfter() {
  const [run, setRun] = useState(0);
  const [step, setStep] = useState<SetupStep>(FIRST_STEP);
  const restart = (next: SetupStep) => {
    seedSampleDraft(USER_ID, next);
    setStep(next);
    setRun(value => value + 1);
  };
  return (
    <section className="kr-section kr-ob" aria-label="Onboarding on Kobra">
      <div className="kr-ob-preview">
        <span className="kr-ob-preview-label">Review: open at a step, with sample answers</span>
        <Select value={step} items={SAMPLE_STEPS.map(item => ({ value: item.step, label: item.label }))}
          onValueChange={value => { if (typeof value === 'string') restart(value as SetupStep); }}>
          <SelectTrigger aria-label="Open the rebuild at a step" className="kr-ob-preview-select"><SelectValue /></SelectTrigger>
          <SelectContent align="start" alignItemWithTrigger={false}>
            {SAMPLE_STEPS.map(item => <SelectItem key={item.step} value={item.step}>{item.label}</SelectItem>)}
          </SelectContent>
        </Select>
      </div>
      <Flow key={run} onRestart={restart} />
    </section>
  );
}
