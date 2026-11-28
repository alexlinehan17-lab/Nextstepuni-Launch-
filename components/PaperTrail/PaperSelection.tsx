import React, { useEffect, useRef, useState } from 'react';
import { useBackStep } from '../../contexts/NavigationContext';
import { Bookmark } from 'lucide-react';
import type { PaperEntry, PaperItem, PaperLang, PaperLevel, PaperTrailSubject } from '../../types/paperTrail';
import { recentKey } from '../../types/paperTrail';
import { isPinned, type PaperRef } from './recentsStore';
import { prettyBytes } from './storage';
import PaperCover from './PaperCover';
import { documentUrl, type DocumentSide } from './PaperDocuments';
import { PaperSubjectArtwork } from './PaperSubjects';
import { Button, TextButton } from '../ui/Button';
import { SelectionBar } from '../ui/Choice';
import { Menu } from '../ui/Menu';
import { List, PressBox, Row } from '../ui/List';

export const LEVEL_LABEL: Record<PaperLevel, string> = {
  higher: 'Higher', ordinary: 'Ordinary', foundation: 'Foundation', common: 'Common',
};
export const paperLabel = (label: string) => label.replace(/\s*\([A-Z]{2}\)\s*$/, '').trim();

/** One tile of the year grid. A year can hold the June sitting, the SEC's
 *  deferred sitting (2022+, same entry, labelled "Deferred · …") or, for a
 *  specification not yet examined, only official sample papers. */
export interface YearCell {
  year: number;
  gap?: string;
  /** The entry also lists deferred-sitting papers. */
  deferred?: boolean;
  /** Every paper in the entry is an official sample paper. */
  sample?: boolean;
  /** Set on an earlier syllabus, beside current-syllabus years. */
  earlier?: boolean;
}

export const yearCellLabel = (cell: Pick<YearCell, 'year' | 'sample'>) =>
  cell.sample ? `${cell.year} · Sample` : String(cell.year);

const DEFERRED_INTRO = 'A separate set of papers the SEC set for candidates who could not sit the June exams. Each opens beside its own deferred marking scheme where the SEC published one.';

interface Props {
  uid?: string;
  subject: PaperTrailSubject;
  label: string;
  level: PaperLevel;
  lang: PaperLang;
  langs: PaperLang[];
  year?: number;
  years: YearCell[];
  entry?: PaperEntry;
  /** Every year's papers at this level and language, newest first (All years). */
  everyYear?: PaperEntry[];
  notice?: string;
  /** Earlier-syllabus sentence for the selected year (syllabusChanges.ts). */
  syllabusNote?: string;
  /** One line above the year grid explaining the subject's syllabus history. */
  gridNote?: string;
  /** Short tag for earlier-syllabus year tiles ("Earlier syllabus"). */
  earlierTag?: string;
  /** Page-level alert (the archive-outage notice), shown under the heading. */
  banner?: React.ReactNode;
  /** All years is showing (held by the parent so it survives a trip to the reader). */
  allYears?: boolean;
  onAllYears?: (on: boolean) => void;
  onLevel: (level: PaperLevel) => void;
  onLang: (lang: PaperLang) => void;
  onYear: (year: number) => void;
  onOpen: (entry: PaperEntry, item: PaperItem, side: 'paper' | 'scheme') => void;
  onSave: (ref: Omit<PaperRef, 'at'>) => void;
  onBack: () => void;
  onTopics: () => void;
}

const isImage = (f: string) => /\.(jpg|jpeg|png)$/i.test(f);
/** The main papers of a year (accessible-format copies are offered beside them). */
const mainPapers = (entry?: PaperEntry) => {
  const mains = entry?.papers.filter(p => !p.modified) ?? [];
  return mains.length ? mains : entry?.papers ?? [];
};

export default function PaperSelection(props: Props) {
  const { uid, subject, label, level, lang, langs, year, years, entry, everyYear = [], notice, syllabusNote, gridNote, earlierTag = 'Earlier syllabus', banner, onLevel, onLang, onYear, onOpen, onSave, onBack: _onBack, onTopics } = props;
  const [ownAllYears, setOwnAllYears] = useState(false);
  const allYears = props.allYears ?? ownAllYears;
  const setAllYears = (on: boolean) => { if (props.onAllYears) props.onAllYears(on); else setOwnAllYears(on); };
  // Every year is a step of the subject: Back returns to the year first.
  useBackStep(allYears, () => setAllYears(false));
  const heading = useRef<HTMLHeadingElement>(null);
  const papersHeading = useRef<HTMLHeadingElement>(null);
  const previous = useRef(allYears);
  useEffect(() => {
    if (previous.current !== allYears) papersHeading.current?.focus();
    previous.current = allYears;
  }, [allYears]);

  const published = years.filter(y => !y.gap);
  // The year bar: All years and the three newest years. A year chosen from
  // further back (search, a saved paper) takes the place of the oldest of them.
  const recent = published.slice(0, 3).map(y => y.year);
  const barYears = year && !recent.includes(year) && published.some(y => y.year === year) ? [...recent.slice(0, 2), year] : recent;
  const papers = mainPapers(entry);
  const juneItems = papers.filter(p => p.sitting !== 'deferred');
  const deferredItems = papers.filter(p => p.sitting === 'deferred');
  const sampleOnly = papers.length > 0 && papers.every(p => p.sitting === 'sample');
  const single = papers.length === 1;

  const saveRef = (item: PaperItem, e: PaperEntry): Omit<PaperRef, 'at'> => ({
    key: recentKey(subject.id, e.year, e.level, e.lang, item.doc.f), subjectId: subject.id, year: e.year, level: e.level, lang: e.lang,
    fileid: item.doc.f, label: paperLabel(item.label), kind: 'paper',
  });
  const saveButton = (item: PaperItem, e: PaperEntry) => {
    const ref = saveRef(item, e);
    const saved = isPinned(uid, ref.key);
    return <Button size="sm" className="pt-icon-btn pt-save-btn" aria-label={`${saved ? 'Remove saved' : 'Save'} ${ref.label}`} aria-pressed={saved} onClick={() => onSave(ref)}>
      <Bookmark width={18} height={18} strokeWidth={1.75} fill={saved ? 'currentColor' : 'none'} aria-hidden="true" />{saved ? 'Saved' : 'Save'}
    </Button>;
  };

  const yearPapers = entry ? <>
    <div className="pt-sec-head">
      <h2 ref={papersHeading} tabIndex={-1} className="t-heading">{sampleOnly ? 'Sample papers' : year ? `${year} papers` : 'Your papers'}</h2>
      {single && saveButton(papers[0], entry)}
    </div>
    {notice && <p role="status" className="t-meta">{notice}</p>}
    {entry.note && <p className="t-meta">{entry.note}</p>}
    {syllabusNote && <p className="t-meta pt-syllabus-note">{syllabusNote}</p>}
    <div className="pt-paper-stack" aria-label={sampleOnly ? 'Sample papers' : `${year} papers`}>
      {[...juneItems, ...deferredItems].map(item => {
        const name = paperLabel(item.label);
        const image = isImage(item.doc.f);
        const card = <article key={item.doc.f} className="pt-paper" aria-label={name}>
          {!single && <div className="pt-sec-head pt-paper-head"><h3 className="t-row">{name}</h3>{saveButton(item, entry)}</div>}
          <div className="pt-pair">
            {(['paper', ...(item.scheme ? ['scheme'] : [])] as DocumentSide[]).map(side => {
              const document = side === 'paper' ? item.doc : item.scheme!;
              const title = side === 'paper' ? name : 'Marking scheme';
              return <div className="pt-doc" key={side}>
                <PressBox className="pt-cover-btn" label={side === 'scheme' ? `Open the ${entry.year} marking scheme for ${name}` : `Open the ${entry.year} ${name}`} onPress={() => onOpen(entry, item, side)}>
                  <PaperCover url={documentUrl(subject, entry, item, side)} image={side === 'paper' && image} renderWidth={600} />
                </PressBox>
                <span className="pt-doc-title">{title}</span>
                <span className="t-meta">{side === 'paper' && image ? 'Image' : 'PDF'}{document.b > 0 ? ` · ${prettyBytes(document.b)}` : ''}</span>
                <Button block className="pt-open" aria-label={side === 'scheme' ? `Open marking scheme for ${name}` : undefined} onClick={() => onOpen(entry, item, side)}>{side === 'scheme' ? 'Open scheme' : image ? 'Open image' : 'Open paper'}</Button>
              </div>;
            })}
          </div>
          {!item.scheme && !image && <p className="t-meta">Marking scheme not published</p>}
          {item.modified && <p className="t-meta">Accessible format</p>}
          {papers.some(p => !p.modified) && entry.papers.filter(p => p.modified && paperLabel(p.label).startsWith(name)).map(mod =>
            <TextButton key={mod.doc.f} className="pt-accessible-link" onClick={() => onOpen(entry, mod, 'paper')}>{paperLabel(mod.label)} · accessible format</TextButton>)}
        </article>;
        // The deferred sitting follows the June papers under its own heading.
        return item === deferredItems[0]
          ? <React.Fragment key={item.doc.f}>
              <div className="pt-sitting"><h3 className="t-heading">{entry.year} · Deferred sitting</h3><p className="t-meta">{DEFERRED_INTRO}</p></div>
              {card}
            </React.Fragment>
          : card;
      })}
      {!papers.length && <p className="t-meta">Nothing published for this year and level.</p>}
    </div>
  </> : <p className="t-meta">Nothing is published at {LEVEL_LABEL[level]} level for this subject{subject.levels.length > 1 ? ' — try another level above.' : ' yet.'}</p>;

  // Every paper, newest first, each beside its cover and its scheme's. A year
  // the SEC did not publish says why, in place.
  const everyEntry = new Map(everyYear.map(e => [e.year, e]));
  const allPapers = <>
    <div className="pt-sec-head">
      <h2 ref={papersHeading} tabIndex={-1} className="t-heading">Every paper</h2>
      <span className="t-meta">Newest first</span>
    </div>
    {gridNote && <p className="t-meta pt-syllabus-note">{gridNote}</p>}
    {years.length ? <List className="pt-shelf" label="Every paper">
      {years.flatMap(cell => {
        if (cell.gap) return [<Row key={`gap-${cell.year}`} title={`${cell.year} · Unavailable`} meta={cell.gap} />];
        const e = everyEntry.get(cell.year);
        if (!e) return [];
        return mainPapers(e).map(item => {
          const name = paperLabel(item.label);
          const tags = [cell.earlier && earlierTag].filter((tag): tag is string => Boolean(tag));
          return <Row key={`${cell.year}-${item.doc.f}`} title={`${cell.year} · ${name}`}
            meta={[item.scheme ? 'Paper and marking scheme' : isImage(item.doc.f) ? 'Image' : 'No marking scheme published', ...tags].join(' · ')}
            label={`Open the ${cell.year} ${name}`}
            art={<span className="pt-minis">
              <PaperCover url={documentUrl(subject, e, item, 'paper')} image={isImage(item.doc.f)} renderWidth={120} />
              {item.scheme && <PaperCover url={documentUrl(subject, e, item, 'scheme')} renderWidth={120} />}
            </span>}
            onPress={() => onOpen(e, item, 'paper')} />;
        });
      })}
    </List> : <p className="t-meta">No papers have been published at this level yet.</p>}
  </>;

  return <section className="pt-archive pt-selection" aria-label={`${label} exam papers`}>
    {/* No "← Paper Trail" here: the top bar's one Back returns to the year,
        then to the archive's front page (useBackStep above and in index.tsx). */}
    <div className="pt-cols">
      <div className="pt-lead">
        <header className="pt-top">
          <div className="pt-top-copy">
            <h1 ref={heading} tabIndex={-1} className="t-display">{label}{subject.cycle === 'lca' ? <span className="t-meta"> · LCA</span> : null}</h1>
            <p className="t-sub">Which paper today?</p>
          </div>
          <PaperSubjectArtwork label={label} className="pt-top-art" />
        </header>
        {banner}
        <div className="pt-pickers">
          <div className="pt-filter-row">
            <SelectionBar label="Level" size="md" className="pt-level" value={level}
              onChange={lv => onLevel(lv)} options={subject.levels.map(lv => ({ value: lv, label: LEVEL_LABEL[lv] }))} />
            <Menu label="Paper language" className="pt-lang" value={lang} onChange={value => onLang(value)}
              options={(langs.length ? langs : [lang]).map(lg => ({ value: lg, label: lg === 'ev' ? 'English' : 'Gaeilge' }))} />
          </div>
          <SelectionBar label="Year" size="md" className="pt-years" value={allYears ? 'all' : year ? String(year) : ''}
            onChange={value => { if (value === 'all') setAllYears(true); else { onYear(Number(value)); setAllYears(false); } }}
            options={[{ value: 'all', label: 'All years' }, ...barYears.map(y => ({ value: String(y), label: String(y) }))]} />
        </div>
      </div>
      <div className="pt-side">
        <section className="pt-papers">{allYears ? allPapers : yearPapers}</section>
        <section className="pt-end">
          <h2 className="t-heading">Prefer to practise by topic?</h2>
          <TextButton arrow="forward" onClick={onTopics}>Open Topic Atlas</TextButton>
          <p className="t-meta">Examination material © State Examinations Commission.</p>
        </section>
      </div>
    </div>
  </section>;
}
