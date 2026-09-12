/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Search sixteen years of Higher Level papers by printed words or Paper
 * Trail's topic tags. Separate indexes preserve each source's question
 * identities; topic hits never depend on the word appearing in the PDF.
 */

import React, { Suspense, useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Body, Container, Eyebrow, SectionRule } from '../primitives';
import { FONT, L, SPACE } from '../theme';
import { type AskData, type AskIndexFile, type AskMode, type AskQuestion, byPaperOrder, highlight, loadAsk, loadAskIndex, matches, matchingTopics, queryTerms, sentenceFor } from '../fx-e/ask';
import HorizontalTabs from '../../ui/HorizontalTabs';
import Guesswork from './Guesswork';
import '../fx-e/fx-e.css';

const AskPaperViewer = React.lazy(() => import('../glass/AskPaperViewer'));

const TEXT = {
  eyebrow: 'Ask the papers',
  lead: 'See where your topic appears in real exam questions.',
  body: 'Sixteen years of Higher Level papers. Eight subjects, 2010–2025. Search by topic or by the words on the paper, then choose a year to explore.',
  label: 'Search the papers',
  loading: 'Opening sixteen years of papers…',
  failed: 'The papers could not be loaded.',
  none: 'no matches in these papers',
  more: 'more in this year',
} as const;

/** Row labels on a phone; the full name shows from 640px. */
const SHORT: Record<string, string> = { biology: 'Bio', chemistry: 'Chem', physics: 'Phys', mathematics: 'Maths', english: 'Eng', geography: 'Geog', economics: 'Econ', business: 'Bus' };
const LEVEL = { H: 'Higher Level', O: 'Ordinary Level' } as const;
const MAX_LIST = 20;

const meta: React.CSSProperties = { fontFamily: FONT.mono, fontSize: 11, letterSpacing: '0.14em', textTransform: 'uppercase', color: L.faint, margin: 0 };
const fine: React.CSSProperties = { fontFamily: FONT.mono, fontSize: 11, lineHeight: 1.6, color: L.faint, margin: 0 };

const plural = (n: number, one: string, many = `${one}s`): string => `${n} ${n === 1 ? one : many}`;

const AskThePapers: React.FC = () => {
  const [index, setIndex] = useState<AskIndexFile | null>(null);
  const [data, setData] = useState<AskData | null>(null);
  const [state, setState] = useState<'idle' | 'loading' | 'ready' | 'failed'>('idle');
  const [query, setQuery] = useState('');
  const [mode, setMode] = useState<AskMode>('topics');
  const [opened, setOpened] = useState<AskQuestion | null>(null);
  const [selected, setSelected] = useState<string | null>(null);
  const loading = useRef(false);

  // The grid's shape on mount, so the section has its form before anyone types.
  useEffect(() => {
    let live = true;
    loadAskIndex().then(i => { if (live) setIndex(i); }).catch(() => { if (live && !loading.current) setState('failed'); });
    return () => { live = false; };
  }, []);

  const load = useCallback(() => {
    if (loading.current || data) return;
    loading.current = true;
    setState('loading');
    (async () => {
      const i = index ?? await loadAskIndex();
      setIndex(i);
      const d = await loadAsk(i);
      setData(d);
      setState('ready');
    })().catch(() => { setState('failed'); loading.current = false; });
  }, [index, data]);

  const terms = useMemo(() => queryTerms(query), [query]);

  const { cells, total, yearCount, max } = useMemo(() => {
    const cells = new Map<string, AskQuestion[]>();
    const years = new Set<number>();
    let total = 0, max = 0;
    if (data && terms.length) {
      for (const q of mode === 'topics' ? data.topicQuestions : data.questions) {
        if (!(mode === 'topics' ? matchingTopics(q, terms).length > 0 : matches(q, terms))) continue;
        const key = `${q.subject.id}|${q.paper.y}`;
        const list = cells.get(key) ?? [];
        list.push(q);
        cells.set(key, list);
        total++;
        years.add(q.paper.y);
        if (list.length > max) max = list.length;
      }
    }
    return { cells, total, yearCount: years.size, max };
  }, [data, terms, mode]);

  useEffect(() => { if (selected && !cells.has(selected)) setSelected(null); }, [cells, selected]);

  const term = query.trim();
  const status = state === 'failed' ? TEXT.failed
    : !term ? 'The grid lights as you type.'
    : state !== 'ready' ? TEXT.loading
    : total === 0 ? <><b>{term}</b> — {TEXT.none}</>
    : <><b>{term}</b> — {mode === 'topics' ? plural(total, 'tagged question') : plural(total, 'text match', 'text matches')} across {plural(yearCount, 'year')}</>;

  const years = index?.years ?? [];
  const subjects = index?.subjects ?? [];
  const list = selected ? [...(cells.get(selected) ?? [])].sort(byPaperOrder) : [];
  const [selSubject, selYear] = selected ? selected.split('|') : ['', ''];
  const selName = subjects.find(s => s.id === selSubject)?.name ?? '';

  return (
    <section id="ask" aria-labelledby="ask-heading" className={SPACE.sectionTight} style={{ position: 'relative', scrollMarginTop: 70 }}>
      <SectionRule />
      <Container>
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-start">
          <div className="lg:col-span-4 lg:pt-2 min-w-0">
            <Eyebrow>{TEXT.eyebrow}</Eyebrow>
            <div className="mt-5"><Guesswork /></div>
            <Body className="mt-6" style={{ maxWidth: '32ch', fontSize: 18, fontWeight: 500, lineHeight: 1.45, color: L.ink }}>{TEXT.lead}</Body>
            <Body className="mt-3" style={{ maxWidth: '40ch' }}>{TEXT.body}</Body>
          </div>

          <div className="lg:col-span-8 min-w-0">
            <div className="fxe-modes">
              <HorizontalTabs<AskMode>
                label="Search by"
                variant="pill"
                value={mode}
                options={[{ value: 'topics', label: 'Topics' }, { value: 'words', label: 'Words' }]}
                onChange={value => { setMode(value); setSelected(null); }}
              />
            </div>
            <label htmlFor="fxe-search" style={meta}>{TEXT.label}</label>
            <input
              id="fxe-search"
              className="fxe-field mt-2"
              type="search"
              value={query}
              onChange={e => { setQuery(e.target.value); if (state === 'idle') load(); }}
              onFocus={() => { if (state === 'idle') load(); }}
              placeholder={mode === 'topics' ? 'Try Trigonometry, photosynthesis, poetry…' : 'A word or phrase from a question…'}
              autoComplete="off"
              autoCorrect="off"
              autoCapitalize="off"
              spellCheck={false}
              aria-describedby="fxe-search-help fxe-count"
            />
            <p id="fxe-search-help" className="fxe-help">{mode === 'topics'
              ? 'Find tagged topics, even when the topic’s name isn’t printed in the question.'
              : 'Find words in the question text, including word endings as you type.'}</p>
            <p id="fxe-count" className="fxe-count" role="status" aria-live="polite">{status}</p>
            {state === 'failed' && <button className="fxe-open" type="button" onClick={load}>Try again</button>}

            {index && (
              <div className="fxe-grid-scroll" data-lenis-prevent>
              <div className="fxe-grid" style={{ '--fxe-years': years.length } as React.CSSProperties} role="group" aria-label="Years by subject">
                <span aria-hidden="true" />
                {years.map(y => (
                  <span key={y} className="fxe-grid__year" aria-hidden="true"><span className="fxe-grid__century">{String(y).slice(0, 2)}</span>{String(y).slice(2)}</span>
                ))}
                {subjects.map(s => (
                  <React.Fragment key={s.id}>
                    <span className="fxe-grid__label"><span className="fxe-grid__long">{s.name}</span><span className="fxe-grid__short">{SHORT[s.id] ?? s.name}</span></span>
                    {years.map(y => {
                      const key = `${s.id}|${y}`;
                      const count = cells.get(key)?.length ?? 0;
                      const lit = count > 0;
                      const untagged = mode === 'topics' && data && !data.topicCoverage.has(key);
                      return (
                        <button
                          key={key}
                          type="button"
                          className={`fxe-cell${lit ? ' fxe-cell--lit' : ''}${untagged ? ' fxe-cell--untagged' : ''}`}
                          style={{ '--lit': lit ? 0.28 + 0.72 * (count / max) : 0 } as React.CSSProperties}
                          aria-label={`${s.name} ${y}: ${lit ? plural(count, 'question') : untagged ? 'topic tags not available' : 'no matches'}`}
                          title={untagged ? 'Topic tags not available for this subject and year' : undefined}
                          aria-pressed={selected === key}
                          tabIndex={lit ? 0 : -1}
                          onClick={() => { if (lit) setSelected(key); }}
                          onFocus={() => { if (lit) setSelected(key); }}
                        />
                      );
                    })}
                  </React.Fragment>
                ))}
              </div>
              </div>
            )}
            <p className="fxe-help fxe-swipe">Swipe across the grid to see all years.</p>
            {mode === 'topics' && <p className="fxe-help">Based on available Paper Trail tags. An unlit year doesn’t prove a topic was absent; a dash means tags aren’t available yet.</p>}

            {selected && list.length > 0 && (
              <div className="mt-8">
                <p style={meta}>{selName} · {selYear} — {plural(list.length, 'question')}</p>
                <ol className="fxe-results" style={{ marginTop: 12 }}>
                  {list.slice(0, MAX_LIST).map(q => (
                    <li key={`${q.paper.y}-${q.paper.f}-${q.n}-${q.page}`} className="fxe-result">
                      <p style={meta}>{LEVEL[q.paper.l]}{q.paper.p ? ` · ${q.paper.p}` : ''} · {q.n}{q.page > 0 ? ` · p.${q.page}` : ''}</p>
                      {mode === 'topics' ? <p className="fxe-result__text">{matchingTopics(q, terms).map(t => t.label).join(' · ')}</p> : <p className="fxe-result__text">
                        {highlight(sentenceFor(q, terms), terms).map((r, j) => r.hit ? <mark key={j} className="fxe-mark">{r.text}</mark> : <React.Fragment key={j}>{r.text}</React.Fragment>)}
                      </p>}
                      <button type="button" className="fxe-open" onClick={() => setOpened(q)} aria-label={`Open ${q.subject.name} ${q.paper.y} ${q.paper.p} ${q.n}`}>Open question <span aria-hidden="true">→</span></button>
                      <p style={fine}>SEC Leaving Certificate {q.subject.attributionName} {q.paper.y} {LEVEL[q.paper.l]} — © State Examinations Commission</p>
                    </li>
                  ))}
                </ol>
                {list.length > MAX_LIST && <p style={{ ...meta, marginTop: 12 }}>+ {list.length - MAX_LIST} {TEXT.more}</p>}
              </div>
            )}
          </div>
        </div>
      </Container>
      {opened && <Suspense fallback={<div className="fixed inset-0 z-[100] bg-white p-8" role="status">Opening the question… <button type="button" className="fxe-open" onClick={() => setOpened(null)}>Cancel</button></div>}>
        <AskPaperViewer question={opened} onClose={() => setOpened(null)} />
      </Suspense>}
    </section>
  );
};

export default AskThePapers;
