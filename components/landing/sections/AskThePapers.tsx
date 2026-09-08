/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Ask the papers — a search box over sixteen years of real Leaving Cert
 * papers. The first keystroke lights a grid of years by subjects: a cell
 * goes orange, deeper with the count, when the typed term appears in that
 * year's question text. Clicking or focusing a lit cell lists the questions
 * — year, level, paper, printed number, and the sentence carrying the term,
 * verbatim, with the SEC attribution. The index is built by
 * scripts/landing/ask-index.mjs from the local corpus of SEC PDFs (Higher
 * Level, 2010–2025, eight subjects) and loaded on the input's first focus;
 * searching is client-side on the marker's tokens.
 */

import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Body, Container, Display, Eyebrow, SectionRule } from '../primitives';
import { FONT, L, SPACE } from '../theme';
import { type AskData, type AskIndexFile, type AskQuestion, byPaperOrder, highlight, loadAsk, loadAskIndex, matches, queryTerms, sentenceFor } from '../fx-e/ask';
import '../fx-e/fx-e.css';

const TEXT = {
  eyebrow: 'Ask the papers',
  line: 'Sixteen years of exam papers. Type a word.',
  body: 'Every Higher Level paper in eight subjects since 2010, split into its questions. Type a term and the years that asked about it light up. Open a year to read what the SEC set.',
  label: 'Search the papers',
  placeholder: 'A topic, a name, a formula',
  idle: 'The grid lights as you type.',
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

const plural = (n: number, one: string): string => `${n} ${one}${n === 1 ? '' : 's'}`;

const AskThePapers: React.FC = () => {
  const [index, setIndex] = useState<AskIndexFile | null>(null);
  const [data, setData] = useState<AskData | null>(null);
  const [state, setState] = useState<'idle' | 'loading' | 'ready' | 'failed'>('idle');
  const [query, setQuery] = useState('');
  const [selected, setSelected] = useState<string | null>(null);
  const loading = useRef(false);

  // The grid's shape on mount, so the section has its form before anyone types.
  useEffect(() => {
    let live = true;
    loadAskIndex().then(i => { if (live) setIndex(i); }).catch(() => { if (live) setState('failed'); });
    return () => { live = false; };
  }, []);

  const load = useCallback(() => {
    if (loading.current || !index) return;
    loading.current = true;
    setState('loading');
    loadAsk(index).then(d => { setData(d); setState('ready'); }).catch(() => { setState('failed'); loading.current = false; });
  }, [index]);

  const terms = useMemo(() => queryTerms(query), [query]);

  const { cells, total, yearCount, max } = useMemo(() => {
    const cells = new Map<string, AskQuestion[]>();
    const years = new Set<number>();
    let total = 0, max = 0;
    if (data && terms.length) {
      for (const q of data.questions) {
        if (!matches(q, terms)) continue;
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
  }, [data, terms]);

  useEffect(() => { if (selected && !cells.has(selected)) setSelected(null); }, [cells, selected]);

  const term = query.trim();
  const status = state === 'failed' ? TEXT.failed
    : !term ? TEXT.idle
    : state !== 'ready' ? TEXT.loading
    : total === 0 ? <><b>{term}</b> — {TEXT.none}</>
    : <><b>{term}</b> — {plural(total, 'question')} across {plural(yearCount, 'year')}</>;

  const years = index?.years ?? [];
  const subjects = index?.subjects ?? [];
  const list = selected ? [...(cells.get(selected) ?? [])].sort(byPaperOrder) : [];
  const [selSubject, selYear] = selected ? selected.split('|') : ['', ''];
  const selName = subjects.find(s => s.id === selSubject)?.name ?? '';

  return (
    <section id="ask" className={SPACE.sectionTight} style={{ position: 'relative', scrollMarginTop: 70 }}>
      <SectionRule />
      <Container>
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-start">
          <div className="lg:col-span-4 lg:pt-2">
            <Eyebrow>{TEXT.eyebrow}</Eyebrow>
            <Display size="sub" as="h2" className="mt-4" style={{ maxWidth: '18ch' }}>{TEXT.line}</Display>
            <Body className="mt-5" style={{ maxWidth: '40ch' }}>{TEXT.body}</Body>
          </div>

          <div className="lg:col-span-8 min-w-0">
            <label htmlFor="fxe-search" style={meta}>{TEXT.label}</label>
            <input
              id="fxe-search"
              className="fxe-field mt-2"
              type="search"
              value={query}
              onChange={e => { setQuery(e.target.value); if (state === 'idle') load(); }}
              onFocus={() => { if (state === 'idle') load(); }}
              placeholder={TEXT.placeholder}
              autoComplete="off"
              autoCorrect="off"
              autoCapitalize="off"
              spellCheck={false}
              aria-describedby="fxe-count"
            />
            <p id="fxe-count" className="fxe-count" role="status" aria-live="polite">{status}</p>

            {index && (
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
                      return (
                        <button
                          key={key}
                          type="button"
                          className={`fxe-cell${lit ? ' fxe-cell--lit' : ''}`}
                          style={{ '--lit': lit ? 0.28 + 0.72 * (count / max) : 0 } as React.CSSProperties}
                          aria-label={`${s.name} ${y}: ${lit ? plural(count, 'question') : 'no matches'}`}
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
            )}

            {selected && list.length > 0 && (
              <div className="mt-8">
                <p style={meta}>{selName} · {selYear} — {plural(list.length, 'question')}</p>
                <ol className="fxe-results" style={{ marginTop: 12 }}>
                  {list.slice(0, MAX_LIST).map(q => (
                    <li key={`${q.paper.f}-${q.n}-${q.page}`} className="fxe-result">
                      <p style={meta}>{LEVEL[q.paper.l]}{q.paper.p ? ` · ${q.paper.p}` : ''} · {q.n} · p.{q.page}</p>
                      <p className="fxe-result__text">
                        {highlight(sentenceFor(q, terms), terms).map((r, j) => r.hit ? <mark key={j} className="fxe-mark">{r.text}</mark> : <React.Fragment key={j}>{r.text}</React.Fragment>)}
                      </p>
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
    </section>
  );
};

export default AskThePapers;
