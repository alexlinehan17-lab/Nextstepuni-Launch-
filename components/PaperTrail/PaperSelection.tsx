import React, { useEffect, useRef, useState } from 'react';
import { ArrowLeft, ArrowRight, Bookmark, ChevronDown, ArrowUpRight } from 'lucide-react';
import type { PaperEntry, PaperItem, PaperLang, PaperLevel, PaperTrailSubject } from '../../types/paperTrail';
import { recentKey } from '../../types/paperTrail';
import { isPinned, type PaperRef } from './recentsStore';
import { prettyBytes } from './storage';
import PaperCover from './PaperCover';
import { PaperDocuments, documentUrl, type DocumentSide } from './PaperDocuments';
import { PaperSubjectArtwork } from './PaperSubjects';
import { Button } from '../approved-ui-runtime';
import { ToggleGroup, ToggleGroupItem } from '../approved-ui-runtime';
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from '../approved-ui-runtime';

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
  /** Page-level alert (the archive-outage notice), shown under the heading. */
  banner?: React.ReactNode;
  onLevel: (level: PaperLevel) => void;
  onLang: (lang: PaperLang) => void;
  onYear: (year: number) => void;
  onOpen: (entry: PaperEntry, item: PaperItem, side: 'paper' | 'scheme') => void;
  onSave: (ref: Omit<PaperRef, 'at'>) => void;
  onBack: () => void;
  onTopics: () => void;
}

export default function PaperSelection(props: Props) {
  const { uid, subject, label, level, lang, langs, year, years, entry, notice, banner, onLevel, onLang, onYear, onOpen, onSave, onBack, onTopics } = props;
  const [allYears, setAllYears] = useState(false);
  const [preview, setPreview] = useState<{ entry: PaperEntry; item: PaperItem; mode: DocumentSide | 'files' } | null>(null);
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
      {!allYears && <PaperSubjectArtwork label={label} />}
      <p className="pt-eyebrow">{allYears ? label : 'Your exam archive'}{subject.cycle === 'lca' ? ' · LCA' : ''}</p>
      <h1 ref={heading} tabIndex={-1} className="pt-title">{allYears ? 'Choose a year' : label}</h1>
    </header>
    {banner}
    <div className="pt-approved-filters">
      <div className="pt-level-field"><span className="pt-control-label">Level</span>
        <ToggleGroup aria-label="Level" variant="outline" value={[level]} onValueChange={values => { if (values.length) { setGap(null); onLevel(values[0] as PaperLevel); } }}>
          {subject.levels.map(lv => <ToggleGroupItem key={lv} value={lv}>{LEVEL_LABEL[lv]} level</ToggleGroupItem>)}
        </ToggleGroup>
      </div>
      <div className="pt-two-fields">
        <div><span className="pt-control-label">Paper language</span>
          <Select value={lang} onValueChange={value => { if (value) { setGap(null); onLang(value as PaperLang); } }}>
            <SelectTrigger aria-label="Paper language"><SelectValue>{lang === 'ev' ? 'English' : 'Gaeilge'}</SelectValue></SelectTrigger>
            <SelectContent>{(langs.length ? langs : [lang]).map(lg => <SelectItem key={lg} value={lg}>{lg === 'ev' ? 'English' : 'Gaeilge'}</SelectItem>)}</SelectContent>
          </Select>
        </div>
        <div><span className="pt-control-label">Choose a year</span>
          <Select value={allYears ? 'all' : String(year ?? '')} onValueChange={value => { if (value === 'all') setAllYears(true); else if (value) { onYear(Number(value)); setAllYears(false); setGap(null); } }}>
            <SelectTrigger aria-label="Choose a year"><SelectValue>{allYears ? 'All years' : year ?? 'No published years'}</SelectValue></SelectTrigger>
            <SelectContent>{[...new Set([...recentYears.map(y => y.year), ...(year ? [year] : [])])].map(y => <SelectItem key={y} value={String(y)}>{y}</SelectItem>)}<SelectItem value="all">All years</SelectItem></SelectContent>
          </Select>
        </div>
      </div>
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
      <div className="pt-paper-selection-heading"><h2>{year ? `${year} papers` : 'Your papers'}</h2><Button ref={allYearsButton} variant="ghost" onClick={() => setAllYears(true)}>All years<ChevronDown size={14} /></Button></div>
      {notice && <p role="status" className="pt-notice">{notice}</p>}
      {entry?.note && <p className="pt-notice">{entry.note}</p>}
      {entry ? <div className="pt-paper-list" aria-label={`${year} papers`}>
        {papers.map(item => {
          const name = paperLabel(item.label);
          const ref: Omit<PaperRef, 'at'> = { key: recentKey(subject.id, entry.year, entry.level, entry.lang, item.doc.f), subjectId: subject.id, year: entry.year, level: entry.level, lang: entry.lang, fileid: item.doc.f, label: name, kind: 'paper' };
          const saved = isPinned(uid, ref.key);
          const image = /\.(jpg|jpeg|png)$/i.test(item.doc.f);
          return <article key={item.doc.f} className="pt-paper-card" aria-label={name}>
            <div className="pt-paper-pair-heading">
              <h3>{name}</h3>
              <Button variant="ghost" size="icon" className="pt-save" aria-label={`${saved ? 'Remove saved' : 'Save'} ${name}`} aria-pressed={saved} onClick={() => onSave(ref)}>
                <Bookmark size={20} fill={saved ? 'currentColor' : 'none'} aria-hidden />
              </Button>
            </div>
            <div className="pt-paper-cover-grid">
              {(['paper', ...(item.scheme ? ['scheme'] : [])] as DocumentSide[]).map(side => {
                const document = side === 'paper' ? item.doc : item.scheme!;
                const title = side === 'paper' ? name : 'Marking scheme';
                return <div className="pt-paper-cover-card" key={side}>
                  <button className="pt-large-cover-button" aria-label={`Preview ${title}`} onClick={() => setPreview({ entry, item, mode: side })}>
                    <PaperCover url={documentUrl(subject, entry, item, side)} image={side === 'paper' && image} renderWidth={600} />
                  </button>
                  <div className="pt-paper-cover-details"><h4>{title}</h4><p>{side === 'paper' && image ? 'Image' : 'PDF'}{document.b > 0 ? ` · ${prettyBytes(document.b)}` : ''}</p>
                    <Button variant="outline" className="nsu-ink-outline" aria-label={side === 'scheme' ? `Open marking scheme for ${name}` : undefined} onClick={() => onOpen(entry, item, side)}>{side === 'scheme' ? 'Open scheme' : image ? 'Open image' : 'Open paper'}<ArrowUpRight /></Button>
                  </div>
                </div>;
              })}
            </div>
            {!item.scheme && !image && <p className="pt-scheme-unavailable">Marking scheme not published</p>}
            <Button variant="ghost" className="pt-paper-files-button" onClick={() => setPreview({ entry, item, mode: 'files' })}>{item.scheme ? 'Paper & marking scheme' : 'File details'}<ArrowUpRight /></Button>
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
    {preview && preview.entry === entry && <PaperDocuments key={`${preview.item.doc.f}-${preview.mode}`} subject={subject} label={label} entry={preview.entry} item={preview.item} initial={preview.mode} onClose={() => setPreview(null)} onRead={side => { const selected = preview; setPreview(null); onOpen(selected.entry, selected.item, side); }} />}
  </section>;
}
