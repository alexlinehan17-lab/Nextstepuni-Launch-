import React, { useEffect, useRef, useState } from 'react';
import { ArrowLeft, ArrowRight, Bookmark, ChevronDown } from 'lucide-react';
import type { PaperEntry, PaperItem, PaperLang, PaperLevel, PaperTrailSubject } from '../../types/paperTrail';
import { recentKey } from '../../types/paperTrail';
import { isPinned, type PaperRef } from './recentsStore';
import { paperStoragePath, paperUrl, prettyBytes } from './storage';
import PaperCover from './PaperCover';

export const LEVEL_LABEL: Record<PaperLevel, string> = {
  higher: 'Higher', ordinary: 'Ordinary', foundation: 'Foundation', common: 'Common',
};
export const paperLabel = (label: string) => label.replace(/\s*\([A-Z]{2}\)\s*$/, '').trim();

interface Props {
  uid?: string;
  subject: PaperTrailSubject;
  label: string;
  level: PaperLevel;
  lang: PaperLang;
  langs: PaperLang[];
  year?: number;
  years: { year: number; gap?: string }[];
  entry?: PaperEntry;
  notice?: string;
  onLevel: (level: PaperLevel) => void;
  onLang: (lang: PaperLang) => void;
  onYear: (year: number) => void;
  onOpen: (entry: PaperEntry, item: PaperItem, side: 'paper' | 'scheme') => void;
  onSave: (ref: Omit<PaperRef, 'at'>) => void;
  onBack: () => void;
  onTopics: () => void;
}

export default function PaperSelection(props: Props) {
  const { uid, subject, label, level, lang, langs, year, years, entry, notice, onLevel, onLang, onYear, onOpen, onSave, onBack, onTopics } = props;
  const [allYears, setAllYears] = useState(false);
  const [gap, setGap] = useState<string | null>(null);
  const heading = useRef<HTMLHeadingElement>(null);
  const allYearsButton = useRef<HTMLButtonElement>(null);
  const previous = useRef(false);
  useEffect(() => {
    if (allYears) heading.current?.focus();
    else if (previous.current) allYearsButton.current?.focus();
    previous.current = allYears;
  }, [allYears]);
  const recentYears = years.filter(y => !y.gap).slice(0, 3);
  const olderSelected = year != null && !recentYears.some(y => y.year === year);
  const decades = [...new Set(years.map(y => Math.floor(y.year / 10) * 10))];
  const mains = entry?.papers.filter(p => !p.modified) ?? [];
  const papers = mains.length ? mains : entry?.papers ?? [];

  return <section className="pt-archive pt-selection" aria-label={`${label} exam papers`}>
    <nav className="pt-toolbar" aria-label="Paper Trail">
      <button className="pt-text-button" onClick={allYears ? () => setAllYears(false) : onBack}>
        <ArrowLeft size={20} aria-hidden /> {allYears ? label : 'Paper Trail'}
      </button>
    </nav>
    <header className="pt-subject-heading">
      <p className="pt-eyebrow">{allYears ? label : 'Your exam archive'}{subject.cycle === 'lca' ? ' · LCA' : ''}</p>
      <h1 ref={heading} tabIndex={-1} className="pt-title">{allYears ? 'Choose a year' : label}</h1>
    </header>
    <div className="pt-filters">
      <label><span className="sr-only">Level</span>
        <select aria-label="Level" value={level} onChange={e => { setGap(null); onLevel(e.target.value as PaperLevel); }}>
          {subject.levels.map(lv => <option key={lv} value={lv}>{LEVEL_LABEL[lv]} level</option>)}
        </select><ChevronDown size={16} aria-hidden />
      </label>
      <label><span className="sr-only">Paper language</span>
        <select aria-label="Paper language" value={lang} onChange={e => { setGap(null); onLang(e.target.value as PaperLang); }}>
          {(langs.length ? langs : [lang]).map(lg => <option key={lg} value={lg}>{lg === 'ev' ? 'English' : 'Gaeilge'}</option>)}
        </select><ChevronDown size={16} aria-hidden />
      </label>
    </div>
    {allYears ? <>
      <p className="pt-year-intro">Every available paper, newest first.</p>
      {gap && <p role="status" className="pt-notice">{gap}</p>}
      {decades.map(decade => <section className="pt-decade" key={decade}>
        <h2 className="pt-eyebrow">{decade}–{Math.min(decade + 9, years[0].year)}</h2>
        <div className="pt-year-grid">{years.filter(y => Math.floor(y.year / 10) * 10 === decade).map(y =>
          <button key={y.year} className={y.gap ? 'pt-year-gap' : ''} aria-pressed={!y.gap && y.year === year}
            aria-label={y.gap ? `${y.year} unavailable — ${y.gap}` : String(y.year)}
            onClick={() => { if (y.gap) setGap(`${y.year}: ${y.gap}`); else { onYear(y.year); setGap(null); setAllYears(false); } }}>
            {y.year}{y.gap && <span>Unavailable</span>}
          </button>)}</div>
      </section>)}
      {!years.length && <p className="pt-notice">No papers have been published at this level yet.</p>}
    </> : <>
      <h2 className="pt-eyebrow pt-choose-year">Choose a year</h2>
      <div className="pt-year-tabs" role="group" aria-label="Exam year">
        {recentYears.map(y => <button key={y.year} aria-pressed={y.year === year} onClick={() => onYear(y.year)}>{y.year}</button>)}
        <button ref={allYearsButton} aria-pressed={olderSelected} onClick={() => setAllYears(true)}>{olderSelected ? `${year} · All years` : 'All years'}<ChevronDown size={14} aria-hidden /></button>
      </div>
      {notice && <p role="status" className="pt-notice">{notice}</p>}
      {entry?.note && <p className="pt-notice">{entry.note}</p>}
      {entry ? <div className="pt-paper-list" aria-label={`${year} papers`}>
        {papers.map(item => {
          const name = paperLabel(item.label);
          const ref: Omit<PaperRef, 'at'> = { key: recentKey(subject.id, entry.year, entry.level, entry.lang, item.doc.f), subjectId: subject.id, year: entry.year, level: entry.level, lang: entry.lang, fileid: item.doc.f, label: name, kind: 'paper' };
          const saved = isPinned(uid, ref.key);
          const image = /\.(jpg|jpeg|png)$/i.test(item.doc.f);
          return <article key={item.doc.f} className="pt-paper-card" aria-label={name}>
            <div className="pt-paper-identity">
              <button className="pt-cover-button" aria-label={`Open ${name} preview`} onClick={() => onOpen(entry, item, 'paper')}>
                <PaperCover url={paperUrl(paperStoragePath(subject.cycle, subject.id, entry.year, 'paper', item.doc.f))} image={image} />
              </button>
              <div className="pt-paper-name"><h3>{name}</h3><p>{image ? 'Image' : 'PDF'}{item.doc.b > 0 ? ` · ${prettyBytes(item.doc.b)}` : ''}</p></div>
              <button className="pt-save" aria-label={`${saved ? 'Remove saved' : 'Save'} ${name}`} aria-pressed={saved} onClick={() => onSave(ref)}>
                <Bookmark size={20} fill={saved ? 'currentColor' : 'none'} aria-hidden />
              </button>
            </div>
            <button className="pt-open-paper" onClick={() => onOpen(entry, item, 'paper')}>{image ? 'Open image' : 'Open paper'}</button>
            {item.scheme ? <button className="pt-scheme" onClick={() => onOpen(entry, item, 'scheme')}>
              <span>Marking scheme</span><span className="pt-file-size">{prettyBytes(item.scheme.b)}</span><ArrowRight size={18} aria-hidden />
            </button> : !image && <p className="pt-scheme-unavailable">Marking scheme not published</p>}
            {item.modified && <p className="pt-format-note">Accessible format</p>}
            {mains.length > 0 && entry.papers.filter(p => p.modified && paperLabel(p.label).startsWith(name)).map(mod =>
              <button key={mod.doc.f} className="pt-accessible" onClick={() => onOpen(entry, mod, 'paper')}>{paperLabel(mod.label)} · accessible format</button>)}
          </article>;
        })}
        {!papers.length && <p className="pt-notice">Nothing published for this year and level.</p>}
      </div> : <p className="pt-notice">Nothing is published at {LEVEL_LABEL[level]} level for this subject{subject.levels.length > 1 ? ' — try another level above.' : ' yet.'}</p>}
      <button className="pt-topic-link" onClick={onTopics}><span>Prefer to practise by topic?</span><ArrowRight size={18} aria-hidden /></button>
      <p className="pt-source-note">Examination material © State Examinations Commission.</p>
    </>}
  </section>;
}
