/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * "Your setup": everything a student told us in onboarding, read back from
 * their saved profile and North Star, each with the editor that already owns
 * it. No new store and no new editing logic.
 *
 * The look (r5-your-setup, agreed 26 Nov 2026): the walking character, the big
 * headline and the seven numbered parts stay; the parts lie on the page between
 * thin rules (a box you cannot press has no line round it), each subject carries
 * its character, the week is drawn as seven marks, and the choices are the
 * shared selection bar. On a laptop the parts sit in two columns and "Change
 * exam date" sits beside "Change year" at the top of School year.
 */

import { useState } from 'react';
import KobraScope from '../approved-ui-runtime';
import PageHeader from '../ui/PageHeader';
import { Button } from '../ui/Button';
import { SelectionBar } from '../ui/Choice';
import { Field } from '../ui/Field';
import ThemeArtwork from '../ThemeArtwork';
import SubjectAvatar from '../SubjectAvatar';
import { useMobileAppDesign } from '../../hooks/useMobileAppDesign';
import { useStudyNotifications } from '../../hooks/useStudyNotifications';
import { useSettingsContext } from '../../contexts/SettingsContext';
import type { StudentSubjectProfile, YearGroup } from '../subjectData';
import type { NorthStar } from '../../types';
import { canEditExamDate, examDateBounds, examDateProblem, summariseSetup } from './yourSetupModel';
import { getDefaultExamDateForYear } from '../../utils/examDates';
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

/** One numbered part of the page: its number and label, an action at the right, then its content, under a thin rule. */
function Section({ index, title, action, className = '', children }: {
  index: string; title: string; action?: React.ReactNode; className?: string; children: React.ReactNode;
}) {
  return (
    <section className={`ys-sec ${className}`} aria-labelledby={`ys-${index}`}>
      <header className="ys-sec-head">
        <p className="ys-eyebrow"><span>{index}</span>{title}</p>
        {action ? <div className="ys-sec-actions">{action}</div> : null}
      </header>
      {children}
    </section>
  );
}

function ExamDateForm({ current, year, onSave, onClose }: { current: string | null; year?: YearGroup; onSave: (examStartDate: string) => void; onClose: () => void }) {
  const [value, setValue] = useState(() => current ?? getDefaultExamDateForYear(year));
  const [problem, setProblem] = useState<string | null>(null);
  const { min, max } = examDateBounds();
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
        onClose();
      }}
    >
      <Field
        label="When do your exams start?"
        type="date"
        value={value}
        min={min}
        max={max}
        required
        help="Choose the date you’re working towards. You can change it again whenever you need to."
        error={problem ?? undefined}
        onChange={event => { setValue(event.target.value); setProblem(null); }}
      />
      <div className="ys-date-actions">
        <Button kind="main" type="submit">Save date</Button>
        <Button onClick={onClose}>Cancel</Button>
      </div>
    </form>
  );
}

export default function YourSetupView({
  profile, northStar, yearGroup, darkMode, onBack, onFinishSetup, onEditSubjects, onSaveExamDate,
  onEditNorthStar, onOpenSettings, onOpenPlanner, onSetDarkMode,
}: Props) {
  const mobileAppDesign = useMobileAppDesign();
  const setup = summariseSetup(profile, northStar, yearGroup);
  const notify = useStudyNotifications();
  // Settings are optional here (tests render the page without a provider).
  const settingsContext = useSettingsContext();
  const quizOn = settingsContext?.settings.studyQuiz !== false;
  const [editingDate, setEditingDate] = useState(false);
  const examYear = yearGroup ?? profile?.yearGroup;
  const canChangeDate = Boolean(profile && onSaveExamDate && canEditExamDate(examYear));
  const dateButton = canChangeDate && !editingDate
    ? <Button className="ys-date-edit" onClick={() => setEditingDate(true)}>{profile?.examStartDate ? 'Change exam date' : 'Set exam date'}</Button>
    : null;

  return (
    <KobraScope className="nsu-your-setup">
      <div className="product-shell min-h-screen bg-[var(--surface-canvas)] text-[var(--ink-primary)]">
        <div className="ys-topbar">
          <div className="ys-width">
            <PageHeader onBack={onBack} eyebrow="Your profile" title="Your setup" compact />
          </div>
        </div>

        <main className="ys-width ys-main">
          <div className="ys-hero">
            <div className="ys-hero-words">
              <p className="t-label ys-kicker">What you told us</p>
              <h1 className="t-display ys-title">Everything you set up, in one place.</h1>
              <p className="t-sub ys-lede">Your year, your goal, your subjects and your week shape your plan, your points and what we recommend. Change any of them when things change.</p>
            </div>
            <ThemeArtwork src="/assets/star-crew/companions/wayfinder.png" transparentBackground alt="" width={168} height={168} className="ys-art" />
          </div>

          {!profile && (
            <section className="ys-sec ys-empty" aria-labelledby="ys-empty-title">
              <h2 id="ys-empty-title" className="ys-value">You haven&apos;t finished setting up yet.</h2>
              <p className="ys-meta">Tell us your year, your subjects and the grades you&apos;re aiming for, and your plan builds around them.</p>
              <Button kind="main" arrow="forward" className="ys-finish" onClick={onFinishSetup}>Finish setting up</Button>
            </section>
          )}

          <div className="ys-grid">
            <Section index="01" title="School year" action={<>
              {!mobileAppDesign ? dateButton : null}
              <Button onClick={onOpenSettings}>Change year</Button>
            </>}>
              <h2 id="ys-01" className="ys-value">{setup.year?.label || 'Not set'}</h2>
              {setup.year && <p className="ys-meta">{setup.year.cycle}</p>}
              {setup.exam && (
                <dl className="ys-facts">
                  <div><dt>Exams start</dt><dd>{setup.exam.label}</dd></div>
                  <div><dt>Time to go</dt><dd>{setup.exam.daysAway > 0 ? <>{setup.exam.daysAway} <small>days</small></> : 'Underway'}</dd></div>
                </dl>
              )}
              {mobileAppDesign && dateButton ? <div className="ys-date">{dateButton}</div> : null}
              {canChangeDate && editingDate && profile && onSaveExamDate && (
                <div className="ys-date"><ExamDateForm current={profile.examStartDate} year={examYear} onSave={onSaveExamDate} onClose={() => setEditingDate(false)} /></div>
              )}
            </Section>

            <Section index="02" title="Your North Star" action={<Button onClick={onEditNorthStar}>{setup.northStar ? 'Edit North Star' : 'Set North Star'}</Button>}>
              {setup.northStar ? (
                <>
                  <h2 id="ys-02" className="ys-value">{setup.northStar.title}</h2>
                  <p className="ys-statement">{setup.northStar.statement}</p>
                  {setup.northStar.vision.length > 0 && (
                    <ul className="ys-vision" aria-label="Your vision board">
                      {setup.northStar.vision.map(card => (
                        <li key={card.id}>
                          {card.art && <ThemeArtwork src={card.art} transparentBackground alt="" width={44} height={44} />}
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

            <Section index="03" title="Subjects and goals" className="ys-wide" action={profile && <Button onClick={onEditSubjects}>Change subjects</Button>}>
              <h2 id="ys-03" className="ys-sr">Subjects and goals</h2>
              {setup.subjects.length ? (
                <>
                  <table className="ys-subjects">
                    <thead><tr><th scope="col">Subject</th><th scope="col">Level</th><th scope="col">Now</th><th scope="col">Aiming for</th></tr></thead>
                    <tbody>
                      {setup.subjects.map(subject => (
                        <tr key={subject.name}>
                          <th scope="row"><span className="ys-subject"><SubjectAvatar subject={subject.name} bare className="ys-subject-art" />{subject.name}</span></th>
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

            <Section index="04" title="Your study week" action={profile && <Button arrow="forward" onClick={onOpenPlanner}>Open Planner</Button>}>
              <h2 id="ys-04" className="ys-value">{setup.studyDays} study {setup.studyDays === 1 ? 'day' : 'days'}</h2>
              <ol className="ys-week" aria-label="Study and rest days">
                {setup.week.map(day => (
                  <li key={day.day} data-study={day.study || undefined} aria-label={`${day.day}: ${day.study ? 'study' : 'rest'}`}>
                    <i aria-hidden="true" /><span>{day.short}</span>
                  </li>
                ))}
              </ol>
              {setup.blockMinutes && <p className="ys-meta">{setup.blockMinutes}-minute study blocks</p>}
            </Section>

            <Section index="05" title="Appearance">
              <h2 id="ys-05" className="ys-value">{darkMode ? 'Dark' : 'Light'}</h2>
              <SelectionBar label="Appearance" size="md" className="ys-seg" value={darkMode ? 'dark' : 'light'} onChange={value => onSetDarkMode(value === 'dark')}
                options={[{ value: 'light', label: 'Light' }, { value: 'dark', label: 'Dark' }]} />
            </Section>

            {settingsContext && (
              <Section index="06" title="After each session">
                <h2 id="ys-06" className="ys-value">{quizOn ? 'Quiz on' : 'Quiz off'}</h2>
                <p className="ys-meta">We’ll ask whether you want to try questions from the topics you studied. You choose whether to start.</p>
                <SelectionBar label="End-of-session quiz" size="md" className="ys-seg" value={quizOn ? 'on' : 'off'} onChange={value => settingsContext.updateSetting('studyQuiz', value === 'on')}
                  options={[{ value: 'off', label: 'Off' }, { value: 'on', label: 'On' }]} />
              </Section>
            )}

            {/* Only where this device can show one (not iPhone or iPad Safari). */}
            {notify.available && (
              <Section index="07" title="Notifications">
                <h2 id="ys-07" className="ys-value">{notify.enabled ? 'On' : 'Off'}</h2>
                <p className="ys-meta">One notification when your study time is up, so you can work in another app while the timer runs.</p>
                <SelectionBar label="Study timer notifications" size="md" className="ys-seg" value={notify.enabled ? 'on' : 'off'} onChange={value => { if (value === 'on') void notify.turnOn(); else notify.turnOff(); }}
                  options={[{ value: 'off', label: 'Off' }, { value: 'on', label: 'On' }]} />
                {notify.blocked && <p className="ys-meta ys-notify-hint" role="status">{notify.hint}</p>}
              </Section>
            )}
          </div>
        </main>
      </div>
    </KobraScope>
  );
}
