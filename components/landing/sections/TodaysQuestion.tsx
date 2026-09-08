/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Today's question — one real Leaving Cert question for everyone in Ireland,
 * per day, Wordle-style. The pool (public/assets/landing/today/pool.json) is
 * written by scripts/landing/today-pool.mjs from the Mark Bank card files:
 * the question is the paper's and the points are the scheme's, verbatim,
 * with the figure where the card carries one. The day's question is
 * pool[(N − 1) mod length], where N counts days from EPOCH in Europe/Dublin,
 * so #1 fell on a real date and tomorrow's question is not reachable. The
 * visitor's answer is scored by the shared deterministic marker
 * (marking/marker.ts); the scheme's points are then revealed with their
 * marks, the earned ones in orange, and the result becomes a row of squares
 * to share. Today's answer and the streak live in localStorage, so a second
 * visit the same day shows the result rather than the box.
 */

import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Body, Button, Container, Display, Eyebrow, Frame, SectionRule } from '../primitives';
import { FONT, L, SPACE } from '../theme';
import { markAnswer, squares, type MarkPoint, type MarkResult } from '../marking/marker';
import { dayBefore, dublinDay, formatDay, questionNumber } from '../fx-e/dublin';
import '../fx-e/fx-e.css';

/** LAUNCH: replace with the public URL of the page. The share card ends with the current origin plus this. */
const SHARE_PATH = '/landing-dev.html#today';
const POOL_URL = '/assets/landing/today/pool.json';
const STORE_KEY = 'landing.today.v1';
const STREAK_KEY = 'landing.today.streak.v1';

interface PoolEntry {
  id: string;
  subject: string;
  year: number;
  level: string;
  ref: string;
  question: string;
  points: MarkPoint[];
  attribution: string;
  figure?: { src: string; alt: string; attribution: string };
}
interface Pool { built: string; count: number; entries: PoolEntry[] }
interface Stored { day: string; id: string; answer: string }
interface Streak { count: number; last: string }

const TEXT = {
  eyebrow: 'Today’s question',
  line: 'One question a day. The same one for everyone.',
  body: 'A real Leaving Cert question, marked the way the examiner marks it: against the scheme’s own points, word for word. A new one at midnight, Irish time.',
  label: 'Your answer',
  placeholder: 'Type your answer',
  check: 'Check',
  yours: 'You wrote',
  share: 'Share your squares',
  copy: 'Copy your squares',
  copied: 'Copied',
  shared: 'Shared',
  again: 'You’ve answered today’s question. Tomorrow’s arrives at midnight.',
  loading: 'Finding today’s question…',
  failed: 'Today’s question could not be loaded.',
  streak: 'Streak',
} as const;

const read = <T,>(key: string): T | null => {
  try { const v = localStorage.getItem(key); return v ? (JSON.parse(v) as T) : null; } catch { return null; }
};
const write = (key: string, value: unknown): void => {
  try { localStorage.setItem(key, JSON.stringify(value)); } catch { /* private mode: the result still shows this visit */ }
};

/** The starguy reaction contract (Traveller.tsx): fire and forget, a no-op when he is not live. */
const starguy = (kind: 'nod' | 'tilt' | 'cheer'): void => {
  try { window.dispatchEvent(new CustomEvent('starguy', { detail: { kind } })); } catch { /* no window */ }
};

const plural = (n: number, one: string): string => `${n} ${one}${n === 1 ? '' : 's'}`;

/** The share text, exactly as it goes to the share sheet or the clipboard. */
const shareText = (n: number, day: string, result: MarkResult): string =>
  `Today's Leaving Cert question #${n} · ${formatDay(day)}\n${squares(result)}\n${window.location.origin}${SHARE_PATH}`;

const meta: React.CSSProperties = { fontFamily: FONT.mono, fontSize: 11, letterSpacing: '0.14em', textTransform: 'uppercase', color: L.faint, margin: 0 };
const fine: React.CSSProperties = { fontFamily: FONT.mono, fontSize: 11, lineHeight: 1.6, color: L.faint, margin: 0 };

const TodaysQuestion: React.FC = () => {
  const today = useMemo(() => dublinDay(), []);
  const n = questionNumber(today);
  const [entry, setEntry] = useState<PoolEntry | null>(null);
  const [failed, setFailed] = useState(false);
  const [answer, setAnswer] = useState('');
  const [result, setResult] = useState<MarkResult | null>(null);
  const [streak, setStreak] = useState<Streak | null>(null);
  const [share, setShare] = useState<'idle' | 'copied' | 'shared'>('idle');
  const timer = useRef<number | null>(null);

  useEffect(() => {
    let live = true;
    fetch(POOL_URL)
      .then(r => { if (!r.ok) throw new Error(String(r.status)); return r.json() as Promise<Pool>; })
      .then(pool => {
        if (!live) return;
        if (!pool.entries?.length) throw new Error('empty pool');
        const e = pool.entries[(n - 1) % pool.entries.length];
        setEntry(e);
        const stored = read<Stored>(STORE_KEY);
        if (stored && stored.day === today && stored.id === e.id) {
          setAnswer(stored.answer);
          setResult(markAnswer(stored.answer, e.points));
        }
        setStreak(read<Streak>(STREAK_KEY));
      })
      .catch(() => { if (live) setFailed(true); });
    return () => { live = false; if (timer.current) window.clearTimeout(timer.current); };
  }, [n, today]);

  const check = useCallback(() => {
    if (!entry || !answer.trim()) return;
    const r = markAnswer(answer, entry.points);
    setResult(r);
    const stored: Stored = { day: today, id: entry.id, answer };
    write(STORE_KEY, stored);
    const prev = read<Streak>(STREAK_KEY);
    const next: Streak = prev && prev.last === today ? prev : { count: prev && prev.last === dayBefore(today) ? prev.count + 1 : 1, last: today };
    write(STREAK_KEY, next);
    setStreak(next);
    starguy(r.earned === r.total ? 'cheer' : r.earned > 0 ? 'nod' : 'tilt');
  }, [entry, answer, today]);

  const onShare = useCallback(async () => {
    if (!result) return;
    const text = shareText(n, today, result);
    const nav = navigator as Navigator & { share?: (d: { text: string }) => Promise<void>; canShare?: (d: { text: string }) => boolean };
    if (typeof nav.share === 'function' && (typeof nav.canShare !== 'function' || nav.canShare({ text }))) {
      try { await nav.share({ text }); setShare('shared'); return; }
      catch (e) { if ((e as Error).name === 'AbortError') return; /* else fall through to the clipboard */ }
    }
    try { await navigator.clipboard.writeText(text); } catch { return; }
    setShare('copied');
    if (timer.current) window.clearTimeout(timer.current);
    timer.current = window.setTimeout(() => setShare('idle'), 2400);
  }, [result, n, today]);

  const canShareSheet = typeof navigator !== 'undefined' && typeof (navigator as Navigator & { share?: unknown }).share === 'function';
  const total = entry ? entry.points.reduce((s, p) => s + p.marks, 0) : 0;

  return (
    <section id="today" className={SPACE.sectionTight} style={{ position: 'relative', scrollMarginTop: 70 }}>
      <SectionRule />
      <Container>
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-start">
          <div className="lg:col-span-4 lg:pt-2">
            <Eyebrow>{TEXT.eyebrow}</Eyebrow>
            <Display size="sub" as="h2" className="mt-4" style={{ maxWidth: '18ch' }}>{TEXT.line}</Display>
            <Body className="mt-5" style={{ maxWidth: '40ch' }}>{TEXT.body}</Body>
            {streak && streak.count > 0 && (
              <p style={{ ...meta, marginTop: 24 }}>{TEXT.streak} · <span style={{ color: L.orangeText }}>{plural(streak.count, 'day')}</span></p>
            )}
          </div>

          <div className="lg:col-span-8 min-w-0">
            <Frame title={`Today’s question #${n}`} meta={formatDay(today)} padded>
              {failed ? (
                <Body>{TEXT.failed}</Body>
              ) : !entry ? (
                <Body>{TEXT.loading}</Body>
              ) : (
                <div>
                  <p style={meta}>{entry.subject} · {entry.year} · {entry.level} · {entry.ref}</p>
                  <p className="fxe-question mt-3">{entry.question}</p>
                  {entry.figure && (
                    <figure className="fxe-figure">
                      <img src={entry.figure.src} alt={entry.figure.alt} loading="lazy" decoding="async" />
                      <figcaption style={{ ...fine, marginTop: 8 }}>{entry.figure.attribution}</figcaption>
                    </figure>
                  )}

                  {!result ? (
                    <form className="mt-5" onSubmit={e => { e.preventDefault(); check(); }}>
                      <label htmlFor="fxe-answer" style={meta}>{TEXT.label}</label>
                      <textarea
                        id="fxe-answer"
                        className="fxe-field fxe-answer mt-2"
                        value={answer}
                        onChange={e => setAnswer(e.target.value)}
                        onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); check(); } }}
                        placeholder={TEXT.placeholder}
                        rows={2}
                        autoComplete="off"
                        spellCheck={false}
                      />
                      <div className="mt-3 flex items-center gap-4">
                        <Button variant="ink" onClick={check}>{TEXT.check}</Button>
                        <span style={meta}>{plural(total, 'mark')}</span>
                      </div>
                    </form>
                  ) : (
                    <div className="mt-5">
                      <p style={meta}>{TEXT.yours}</p>
                      <p style={{ fontFamily: FONT.sans, fontSize: 16, lineHeight: 1.45, color: L.ink, margin: '6px 0 0', whiteSpace: 'pre-wrap' }}>{answer}</p>
                      <p className="fxe-score mt-5"><b>{result.earned}</b> of {plural(result.total, 'mark')}</p>
                      <ul className="fxe-points" aria-label="The marking scheme’s points">
                        {entry.points.map((p, i) => {
                          const hit = result.hits.find(h => h.id === p.id)?.matched ?? false;
                          return (
                            <li key={p.id} className={`fxe-point fxe-rise${hit ? ' fxe-point--earned' : ''}`} style={{ '--i': i } as React.CSSProperties}>
                              <span className="fxe-point__sq" aria-hidden="true" />
                              <span className="fxe-point__text">{p.verbatim}</span>
                              <span className="fxe-point__marks">{hit ? '' : '0 of '}{plural(p.marks, 'mark')}</span>
                            </li>
                          );
                        })}
                      </ul>
                      <p style={{ ...fine, marginTop: 12 }}>{entry.attribution}</p>
                      <p style={fine}>Marking points quoted from the SEC marking scheme, {entry.subject} {entry.year} {entry.level} — © State Examinations Commission.</p>

                      <pre className="fxe-card mt-5 fxe-rise" style={{ '--i': entry.points.length } as React.CSSProperties} aria-label="Your share card">
                        {`Today's Leaving Cert question #${n} · ${formatDay(today)}\n`}
                        <span className="fxe-card__squares">{squares(result)}</span>
                        {`\n${typeof window !== 'undefined' ? window.location.origin : ''}${SHARE_PATH}`}
                      </pre>
                      <div className="mt-3 flex items-center gap-4">
                        <Button variant="ink" onClick={onShare}>{canShareSheet ? TEXT.share : TEXT.copy}</Button>
                        <span className="fxe-status" role="status" aria-live="polite">{share === 'copied' ? TEXT.copied : share === 'shared' ? TEXT.shared : ''}</span>
                      </div>
                      <p style={{ ...fine, marginTop: 16 }}>{TEXT.again}</p>
                    </div>
                  )}
                </div>
              )}
            </Frame>
          </div>
        </div>
      </Container>
    </section>
  );
};

export default TodaysQuestion;
