import './module-cards.css';
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * ModuleShowcase: one module world (area 5 of the design build; boards
 * c-modules-world on a phone, r5-module-world on a laptop).
 *
 * A world opens on the module to read next, with one Continue, under the
 * world's drawing and its own words. The rest are short boxes you press, and
 * the finished modules fold into one row. On a laptop the drawing and the
 * world's words stay at the left; the module to read next keeps its topics and
 * "What's in this module" (ROUND5-RESULTS, "c1").
 *
 * ModuleWorldScreen is the whole page (its bar included): the router shows it,
 * and Modules draws it into a door as the door opens.
 */
import React, { useState } from 'react';
import { Search } from 'lucide-react';
import { type CourseData } from './Library';
import type { UserProgress } from '../types';
import { useCompactLayout } from '../hooks/useCompactLayout';
import { useSettingsContext } from '../contexts/SettingsContext';
import { TopBar } from './ui/Bars';
import { Button, IconButton, Glyph, Arrow } from './ui/Button';
import { List, Row, PaperSheet, PressBox } from './ui/List';
import { SearchField } from './ui/Field';
import { CompletionMark } from './learning/CompletionMark';
import { sectionsFor } from './learning/data';
import { requestModuleResume } from './learning/intents';
import { moduleOutcome, moduleReadingTime } from '../utils/moduleDiscovery';
import { MODULE_WORLDS, Marks, Readout, WorldArt, isModuleDone, isModuleStarted, moduleResumePoint, worldProgress, worldStyle, type ModuleWorld } from './moduleWorlds';

interface ModuleShowcaseProps {
  courses: CourseData[];
  categoryTitle: string;
  categoryId: string;
  userProgress: UserProgress | Record<string, { unlockedSection: number }>;
  onSelectCourse: (courseId: string) => void;
  /** On a phone: the world's own search ("Find a module") is open from the bar's search button. */
  searchOpen?: boolean;
}

const pad = (n: number) => String(n).padStart(2, '0');

/** The world's page under its bar. */
export default function ModuleShowcase({ courses, categoryId, userProgress, onSelectCourse, searchOpen = false }: ModuleShowcaseProps) {
  const phone = useCompactLayout();
  const dark = useSettingsContext()?.settings.darkMode ?? false;
  const essentials = useSettingsContext()?.settings.essentialsMode;
  const progress = userProgress as UserProgress;
  const world: ModuleWorld = MODULE_WORLDS.find(item => item.id === categoryId) ?? MODULE_WORLDS[0];
  const [query, setQuery] = useState('');
  const [whatsIn, setWhatsIn] = useState(false);
  const [finishedOpen, setFinishedOpen] = useState(false);
  if (courses.length === 0) return null;

  const numberOf = (course: CourseData) => courses.findIndex(item => item.id === course.id) + 1;
  const next = courses.find(course => isModuleStarted(course, progress)) ?? courses.find(course => !isModuleDone(course, progress)) ?? courses[0];
  const nextDone = isModuleDone(next, progress);
  const nextStarted = isModuleStarted(next, progress);
  const at = moduleResumePoint(next, progress);
  const matches = (course: CourseData) => !query.trim() || `${course.title} ${course.description}`.toLowerCase().includes(query.toLowerCase().trim());
  const rest = courses.filter(course => course.id !== next.id && !isModuleDone(course, progress) && matches(course));
  const finished = courses.filter(course => course.id !== next.id && isModuleDone(course, progress) && matches(course));
  const p = worldProgress(world.id, courses, progress);
  const label = nextDone ? 'Review module' : nextStarted ? 'Continue' : 'Start module';
  const go = () => { if (nextStarted) requestModuleResume(next.id); onSelectCourse(next.id); };

  const head = (
    <div className={phone ? 'mw-whead' : 'mw-wlead'} style={worldStyle(world, dark)}>
      {phone ? (
        <div className="mw-whead-row" data-in="1">
          <div className="mw-whead-copy">
            <p className="t-label mw-w-ink mw-whead-place">{world.place}</p>
            <h1 className="t-title mw-whead-title">{world.blurb}</h1>
          </div>
          <WorldArt world={world} size={112} className="mw-whead-art" />
        </div>
      ) : (
        <>
          <WorldArt world={world} size={168} className="mw-wlead-art" />
          <p className="t-label mw-w-ink mw-whead-place" data-in="1">{world.place}</p>
          <h1 className="t-display mw-wlead-title" data-in="1">{world.blurb}</h1>
        </>
      )}
      <p className="t-sub mw-whead-sub" data-in="1">{world.description}</p>
      <div className="mw-prog mw-whead-prog" data-in="1">
        <Marks total={p.total} on={p.done} part={p.part} />
        <Readout>{p.done} of {p.total} done</Readout>
      </div>
    </div>
  );

  const sections = sectionsFor(next);
  const upNext = (
    <section className="mw-wsec mw-wsec--next" data-in="2">
      <PaperSheet className={`mw-upnext${phone ? '' : ' mw-upnext--wide'}`} label={`Up next: ${next.title}`}>
        <p className="t-label mw-upnext-label">Up next · Module {pad(numberOf(next))}</p>
        <h2 className={phone ? 't-heading mw-upnext-title' : 't-title mw-upnext-title'}>{next.title}</h2>
        <p className="t-sub mw-upnext-sub">{moduleOutcome(next)}</p>
        <hr className="mw-rule" />
        <p className="t-meta mw-upnext-meta">{nextStarted ? 'Section' : 'Begins with · Section'} {nextStarted ? at.step : 1} of {next.sectionsCount} · <b>{nextStarted ? at.title : sections[0]?.title ?? 'Section 1'}</b></p>
        <Marks total={next.sectionsCount} on={Math.min(at.read, next.sectionsCount)} className="mw-upnext-marks" />
        {!phone && next.tags.length ? <p className="t-meta mw-upnext-topics">Topics · {next.tags.slice(0, 3).join(', ')}</p> : null}
        {phone ? (
          <Button kind="main" size="lg" block arrow="forward" className="mw-upnext-go" onClick={go}>{label}</Button>
        ) : (
          <div className="mw-upnext-acts">
            <Button kind="main" size="lg" block arrow="forward" onClick={go}>{label}</Button>
            <Button size="lg" block arrow="menu" aria-expanded={whatsIn} className="mw-whatsin-btn" onClick={() => setWhatsIn(value => !value)}>What’s in this module</Button>
          </div>
        )}
        {!phone && whatsIn ? (
          <List className="mw-whatsin" label={`What’s in ${next.title}`}>
            {sections.map((section, index) => (
              <Row key={`${index}-${section.title}`} icon={<CompletionMark number={index + 1} complete={(progress[next.id]?.unlockedSection ?? 0) > index} />}
                title={section.title} meta={section.eyebrow?.includes(' // ') ? section.eyebrow.split(' // ').slice(1).join(' // ') : undefined} />
            ))}
          </List>
        ) : null}
      </PaperSheet>
    </section>
  );

  const box = (course: CourseData, done: boolean) => (
    <PressBox key={course.id} className={`mw-mod${phone ? '' : ' mw-mod--wide'}`} onPress={() => onSelectCourse(course.id)}>
      <span className="mw-mod-in">
        <Readout className="mw-mod-no">{pad(numberOf(course))}</Readout>{' '}
        <span className="mw-mod-copy">
          <span className="mw-mod-title">{course.title}</span>{' '}
          {!phone && !done ? <><span className="t-sub mw-mod-sub">{moduleOutcome(course)}</span>{' '}</> : null}
          {done
            ? <span className="t-meta mw-mod-done"><svg viewBox="0 0 12 12" aria-hidden="true" focusable="false"><path d="M2.5 6.2l2.4 2.4 4.6-5" /></svg>Finished</span>
            : <span className="t-meta">{moduleReadingTime(course, essentials).replace(/ reading$/, '')} · {course.sectionsCount} sections</span>}
        </span>
        <Arrow meaning="opens" size={20} className="mw-chev" />
      </span>
    </PressBox>
  );

  const names = finished.length > 2 ? `${finished[0].title}, ${finished[1].title} and ${finished.length - 2} more` : finished.map(course => course.title).join(' and ');
  const lists = (
    <>
      {rest.length ? (
        <section className="mw-wsec" data-in="3" aria-labelledby="mw-rest-head">
          <div className="mw-sec-head"><h2 id="mw-rest-head" className="t-heading">Still to read</h2><Readout className="mw-ink3">{rest.length}</Readout></div>
          <div className="mw-mods">{rest.map(course => box(course, false))}</div>
        </section>
      ) : null}
      {finished.length ? (
        <section className="mw-wsec" data-in="4" aria-labelledby="mw-done-head">
          <div className="mw-sec-head"><h2 id="mw-done-head" className="t-heading">Finished</h2><Readout className="mw-ink3">{finished.length}</Readout></div>
          <div className="mw-mods">
            <PressBox className="mw-mod mw-fold" expanded={finishedOpen} onPress={() => setFinishedOpen(value => !value)}>
              <span className="mw-mod-in">
                <span className="mw-tick" aria-hidden="true"><svg viewBox="0 0 12 12" focusable="false"><path d="M2.5 6.2l2.4 2.4 4.6-5" /></svg></span>
                <span className="mw-mod-copy">
                  <span className="mw-mod-title">{finished.length} {finished.length === 1 ? 'module' : 'modules'} finished</span>{' '}
                  <span className="t-meta">{names}</span>
                </span>
                <Arrow meaning="menu" size={20} className="mw-chev mw-turn" />
              </span>
            </PressBox>
            {finishedOpen ? <div className="mw-mods mw-finished">{finished.map(course => box(course, true))}</div> : null}
          </div>
        </section>
      ) : null}
      {query.trim() && !rest.length && !finished.length ? (
        <p className="t-body mw-wsec">No matching modules. <Button size="sm" onClick={() => setQuery('')}>Clear search</Button></p>
      ) : null}
    </>
  );

  const search = (
    <SearchField className="mw-wsearch" label="Find a module" placeholder="Search modules" value={query} onChange={event => setQuery(event.target.value)} autoComplete="off" />
  );

  return phone ? (
    <div className="mw-world mw-world--phone">
      {searchOpen || query.trim() ? <div className="mw-wsec mw-wsearch-slot">{search}</div> : null}
      {head}
      {upNext}
      {lists}
    </div>
  ) : (
    <div className="mw-world mw-world--desk">
      <div className="mw-wcols">
        {head}
        <div className="mw-wmain">
          {upNext}
          {lists}
        </div>
      </div>
    </div>
  );
}

/** The whole world page: its one bar (one Back, the world's number over its name) and the page. */
export function ModuleWorldScreen({ onBack, ...props }: ModuleShowcaseProps & { onBack: () => void }) {
  const phone = useCompactLayout();
  const [searching, setSearching] = useState(false);
  const world = MODULE_WORLDS.find(item => item.id === props.categoryId) ?? MODULE_WORLDS[0];
  const bar = (
    <TopBar data-student-page-header tool={!phone} ruled={!phone} className="mw-wbar"
      leave={{ kind: 'back', onPress: onBack, label: 'Back to Modules' }} over={`Modules · ${world.number}`}
      title={<span data-world-name>{world.name}</span>}
      action={phone ? <IconButton label="Find a module" aria-expanded={searching} icon={<Glyph icon={Search} />} onClick={() => setSearching(!searching)} /> : undefined} />
  );
  return (
    <div className={`mw-page ${phone ? 'mw-page--phone' : 'mw-page--desk'} mw-worldpage`}>
      {phone ? bar : null}
      <div className="mw-col">
        {phone ? null : bar}
        <ModuleShowcase {...props} searchOpen={searching} />
      </div>
    </div>
  );
}
