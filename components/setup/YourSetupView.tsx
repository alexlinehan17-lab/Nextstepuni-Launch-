/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * "Your setup": everything a student told us in onboarding, read back from
 * their saved profile and North Star, each with the editor that already owns
 * it. No new store and no new editing logic.
 */

import { useId, useState } from 'react';
import { ArrowUpRight, CalendarDays, PencilLine } from 'lucide-react';
import KobraScope, { Button, Input, Tabs, TabsList, TabsTrigger } from '../approved-ui-runtime';
import PageHeader from '../ui/PageHeader';
import ThemeArtwork from '../ThemeArtwork';
import { useMobileAppDesign } from '../../hooks/useMobileAppDesign';
import { useStudyNotifications } from '../../hooks/useStudyNotifications';
import type { StudentSubjectProfile, YearGroup } from '../subjectData';
import type { NorthStar } from '../../types';
import { canEditExamDate, examDateBounds, examDateProblem, summariseSetup } from './yourSetupModel';
import { getDefaultExamDate } from '../../utils/examDates';
import './your-setup.css';

interface Props {
  profile: StudentSubjectProfile | null;
  northStar: NorthStar | null;
  yearGroup?: YearGroup;
  darkMode: boolean;
  onBack: () => void;
  onFinishSetup: () => void;
  onEditSubjects: () => void;
  /** Saves a new exam start date (YYYY-MM-DD) onto the subject profile. */
  onSaveExamDate?: (examStartDate: string) => void;
  onEditNorthStar: () => void;
  onOpenSettings: () => void;
  onOpenPlanner: () => void;
  onSetDarkMode: (dark: boolean) => void;
}

function Section({ index, title, action, className = '', children }: {
  index: string; title: string; action?: React.ReactNode; className?: string; children: React.ReactNode;
}) {
  return (
    <section className={`ys-card nsu-paper-card ${className}`} aria-labelledby={`ys-${index}`}>
      <header className="ys-card-head">
        <p className="ys-eyebrow"><span>{index}</span>{title}</p>
        {action}
      </header>
      {children}
    </section>
  );
}

function ExamDateEditor({ current, onSave }: { current: string | null; onSave: (examStartDate: string) => void }) {
  const [editing, setEditing] = useState(false);
  const [value, setValue] = useState('');
  const [problem, setProblem] = useState<string | null>(null);
  const id = useId();
  const { min, max } = examDateBounds();

  if (!editing) {
    return (
      <Button variant="outline" className="nsu-ink-outline ys-edit ys-date-edit" onClick={() => { setValue(current ?? getDefaultExamDate()); setProblem(null); setEditing(true); }}>
        {current ? 'Change exam date' : 'Set exam date'}<CalendarDays aria-hidden="true" />
      </Button>
    );
  }

  return (
    <form
      className="ys-date-form"
      aria-label="Exam start date"
      noValidate
      onSubmit={event => {
        event.preventDefault();
        const reason = examDateProblem(value);
        if (reason) { setProblem(reason); return; }
        onSave(value);
        setEditing(false);
      }}
    >
      <label htmlFor={`${id}-date`}>When do your exams start?</label>
      <Input
        id={`${id}-date`}
        type="date"
        value={value}
        min={min}
        max={max}
        required
        aria-invalid={problem ? true : undefined}
        aria-describedby={`${id}-hint${problem ? ` ${id}-problem` : ''}`}
        onChange={event => { setValue(event.target.value); setProblem(null); }}
      />
      <p id={`${id}-hint`} className="ys-meta">The Leaving Cert and Junior Cycle usually start on the first Wednesday of June.</p>
      {problem && <p id={`${id}-problem`} className="ys-date-problem" role="alert">{problem}</p>}
      <div className="ys-date-actions">
        <Button type="submit" className="ys-primary">Save date</Button>
        <Button type="button" variant="outline" className="nsu-ink-outline" onClick={() => setEditing(false)}>Cancel</Button>
      </div>
    </form>
  );
}

function EditButton({ label, onClick, external = false }: { label: string; onClick: () => void; external?: boolean }) {
  return (
    <Button variant="outline" className="nsu-ink-outline ys-edit" onClick={onClick}>
      {label}{external ? <ArrowUpRight aria-hidden="true" /> : <PencilLine aria-hidden="true" />}
    </Button>
  );
}

export default function YourSetupView({
  profile, northStar, yearGroup, darkMode, onBack, onFinishSetup, onEditSubjects, onSaveExamDate,
  onEditNorthStar, onOpenSettings, onOpenPlanner, onSetDarkMode,
}: Props) {
  const mobileAppDesign = useMobileAppDesign();
  const setup = summariseSetup(profile, northStar, yearGroup);
  const notify = useStudyNotifications();

  return (
    <KobraScope className="nsu-your-setup">
      <div className={`${mobileAppDesign ? 'mobile-editorial ' : ''}product-shell min-h-screen bg-[var(--surface-canvas)] text-[var(--ink-primary)]`}>
        <div className="ys-topbar" style={{ paddingTop: 'calc(16px + var(--sat, 0px))' }}>
          <div className="ys-width">
            <PageHeader onBack={onBack} eyebrow="Your profile" title="Your setup" compact />
          </div>
        </div>

        <main className="ys-width ys-main">
          <div className="ys-hero">
            <div>
              <p className="ys-kicker">What you told us</p>
              <h1 className="ys-title">Everything you set up, in one place.</h1>
              <p className="ys-lede">Your year, your goal, your subjects and your week shape your plan, your points and what we recommend. Change any of them when things change.</p>
            </div>
            <ThemeArtwork src="/assets/star-crew/companions/wayfinder.png" transparentBackground alt="" width={150} height={150} className="ys-art" />
          </div>

          {!profile && (
            <section className="ys-card nsu-paper-card ys-empty" aria-labelledby="ys-empty-title">
              <h2 id="ys-empty-title">You haven&apos;t finished setting up yet.</h2>
              <p>Tell us your year, your subjects and the grades you&apos;re aiming for, and your plan builds around them.</p>
              <Button className="ys-primary" onClick={onFinishSetup}>Finish setting up<ArrowUpRight aria-hidden="true" /></Button>
            </section>
          )}

          <div className="ys-grid">
            <Section index="01" title="School year" action={<EditButton label="Change year" onClick={onOpenSettings} />}>
              <h2 id="ys-01" className="ys-value">{setup.year?.label || 'Not set'}</h2>
              {setup.year && <p className="ys-meta">{setup.year.cycle}</p>}
              {setup.exam && (
                <dl className="ys-facts">
                  <div><dt>Exams start</dt><dd>{setup.exam.label}</dd></div>
                  <div><dt>Time to go</dt><dd>{setup.exam.daysAway > 0 ? `${setup.exam.daysAway} days` : 'Underway'}</dd></div>
                </dl>
              )}
              {profile && onSaveExamDate && canEditExamDate(yearGroup ?? profile.yearGroup) && (
                <div className="ys-date"><ExamDateEditor current={profile.examStartDate} onSave={onSaveExamDate} /></div>
              )}
            </Section>

            <Section index="02" title="Your North Star" action={<EditButton label={setup.northStar ? 'Edit North Star' : 'Set North Star'} onClick={onEditNorthStar} />}>
              {setup.northStar ? (
                <>
                  <h2 id="ys-02" className="ys-value">{setup.northStar.title}</h2>
                  <p className="ys-statement">{setup.northStar.statement}</p>
                  {setup.northStar.vision.length > 0 && (
                    <ul className="ys-vision" aria-label="Your vision board">
                      {setup.northStar.vision.map(card => (
                        <li key={card.id}>
                          {card.art && <ThemeArtwork src={card.art} transparentBackground alt="" width={52} height={52} />}
                          <span>{card.label}</span>
                        </li>
                      ))}
                    </ul>
                  )}
                </>
              ) : (
                <><h2 id="ys-02" className="ys-value">Not set yet</h2><p className="ys-meta">Pick what you&apos;re working towards and it will guide your recommendations.</p></>
              )}
            </Section>

            <Section index="03" title="Subjects and goals" className="ys-wide" action={profile && <EditButton label="Change subjects" onClick={onEditSubjects} />}>
              <h2 id="ys-03" className="ys-sr">Subjects and goals</h2>
              {setup.subjects.length ? (
                <>
                  <table className="ys-subjects">
                    <thead><tr><th scope="col">Subject</th><th scope="col">Level</th><th scope="col">Now</th><th scope="col">Aiming for</th></tr></thead>
                    <tbody>
                      {setup.subjects.map(subject => (
                        <tr key={subject.name}>
                          <th scope="row"><span className="ys-dot" style={{ background: subject.fill }} aria-hidden="true" />{subject.name}</th>
                          <td>{subject.level}</td>
                          <td>{subject.current ?? <span className="ys-quiet">Later</span>}</td>
                          <td className="ys-target">{subject.target ?? <span className="ys-quiet">Later</span>}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                  {setup.points && (
                    <dl className="ys-points" aria-label="CAO points from your grades">
                      <div><dt>Your grades now</dt><dd>{setup.points.current}</dd></div>
                      <div className="ys-points-goal"><dt>Your goal</dt><dd>{setup.points.target}</dd></div>
                      <p>From the grades on this page{setup.points.counted < 6 ? ` (${setup.points.counted} graded)` : ''}: best six subjects, including the maths bonus.</p>
                    </dl>
                  )}
                </>
              ) : <p className="ys-meta">No subjects yet.</p>}
            </Section>

            <Section index="04" title="Your study week" action={profile && <EditButton label="Open Planner" onClick={onOpenPlanner} external />}>
              <h2 id="ys-04" className="ys-value">{setup.studyDays} study {setup.studyDays === 1 ? 'day' : 'days'}</h2>
              <ol className="ys-week" aria-label="Study and rest days">
                {setup.week.map(day => (
                  <li key={day.day} data-study={day.study || undefined} aria-label={`${day.day}: ${day.study ? 'study' : 'rest'}`}>
                    <span>{day.short}</span><small>{day.study ? 'Study' : 'Rest'}</small>
                  </li>
                ))}
              </ol>
              {setup.blockMinutes && <p className="ys-meta">{setup.blockMinutes}-minute study blocks</p>}
            </Section>

            <Section index="05" title="Appearance">
              <h2 id="ys-05" className="ys-value">{darkMode ? 'Dark' : 'Light'}</h2>
              <Tabs value={darkMode ? 'dark' : 'light'} onValueChange={value => onSetDarkMode(value === 'dark')}>
                <TabsList aria-label="Appearance">
                  <TabsTrigger value="light">Light</TabsTrigger>
                  <TabsTrigger value="dark">Dark</TabsTrigger>
                </TabsList>
              </Tabs>
            </Section>

            {/* Only where this device can show one (not iPhone or iPad Safari). */}
            {notify.available && (
              <Section index="06" title="Notifications">
                <h2 id="ys-06" className="ys-value">{notify.enabled ? 'On' : 'Off'}</h2>
                <p className="ys-meta">One notification when your study time is up, so you can work in another app while the timer runs.</p>
                <Tabs value={notify.enabled ? 'on' : 'off'} onValueChange={value => { if (value === 'on') void notify.turnOn(); else notify.turnOff(); }}>
                  <TabsList aria-label="Study timer notifications">
                    <TabsTrigger value="off">Off</TabsTrigger>
                    <TabsTrigger value="on">On</TabsTrigger>
                  </TabsList>
                </Tabs>
                {notify.blocked && <p className="ys-meta ys-notify-hint" role="status">{notify.hint}</p>}
              </Section>
            )}
          </div>
        </main>
      </div>
    </KobraScope>
  );
}
