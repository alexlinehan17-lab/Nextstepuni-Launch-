/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — Topic Vault question card. One past-paper question as it was
 * actually printed: the real paper crop (diagrams, tables, source material
 * included), synthesised from the answer-map anchors, with the verified
 * marking-scheme crop behind a show/hide toggle.
 *
 * Everything degrades honestly: no sidecar / no confident region / render
 * failure → a compact row that still opens the question in the full paper.
 * We never show a crop we can't stand over.
 */

import React, { useEffect, useMemo, useRef, useState } from 'react';
import { BookOpenCheck, Check, ChevronDown, ExternalLink, Plus, Scale } from 'lucide-react';
import type { PDFDocumentProxy } from 'pdfjs-dist';
import { type PaperAnswerMap, type PaperAnswerQuestion } from '../../types/paperTrail';
import CropView from './CropView';
import { paperRegionFor } from './paperRegion';
import { vaultPdf } from './vaultDocs';
import { answerMapUrls, isAnswerMap, resolveSibling } from './vaultResolve';
import { type TopicSibling } from './topics';
import { lensFor } from '../../data/markingLens';

const INK = '#1a1a1a';
const ACCENT = '#F26B1F';
const LVL: Record<string, string> = { higher: 'Higher', ordinary: 'Ordinary', foundation: 'Foundation', common: 'Common' };

// Stable identity — CropView re-renders its (expensive) canvas whenever this
// callback's reference changes, so it must NOT be an inline closure per render
// (a scheme-reveal / review-star toggle would otherwise re-decode the crop).
const paperCropLabel = (p: number) => `Exam paper page ${p}, shown as an image — © State Examinations Commission`;

// Session-scoped answer-map memo (small JSON sidecars; null = miss — the card
// degrades to a plain open-in-paper row). PERMANENT misses stay memoised: a
// 404 (sidecar not published) or a shape/parse failure — the hosted fallback
// path is served by Firebase Hosting, whose SPA rewrite answers missing files
// with index.html (200), which isAnswerMap rejects — won't change this session,
// and every card in a feed re-asks as it scrolls into view. Only TRANSIENT
// failures (network throw, non-404 error status) are forgotten, so a retry
// after coming back online gets a fresh attempt.
const mapMemo = new Map<string, Promise<PaperAnswerMap | null>>();
const fetchOneMap = (url: string): Promise<PaperAnswerMap | null> => {
  let p = mapMemo.get(url);
  if (!p) {
    p = (async () => {
      try {
        const r = await fetch(url);
        if (!r.ok) {
          if (r.status !== 404) mapMemo.delete(url); // 5xx/429 may recover
          return null;
        }
        const v = await r.json().catch(() => null); // HTML from the SPA rewrite
        return isAnswerMap(v) ? v : null;
      } catch {
        mapMemo.delete(url); // offline / network blip — let a remount retry
        return null;
      }
    })();
    mapMemo.set(url, p);
  }
  return p;
};
/** First candidate map that actually CARRIES question `n` (Storage sidecar,
 *  then the hosted paper-anchors fallback) — a valid map numbered against a
 *  different question run (the split-spec Paper-2 class: printed Q11-17 vs a
 *  tag's 1-7) must not shadow a later candidate that has the question. */
const fetchAnswerMap = async (urls: string[], n: string): Promise<PaperAnswerMap | null> => {
  let withoutN: PaperAnswerMap | null = null;
  for (const url of urls) {
    const m = await fetchOneMap(url);
    if (!m) continue;
    if (m.q.some(q => q.n === n)) return m;
    withoutN = withoutN ?? m;
  }
  return withoutN;
};

type CardState =
  | { s: 'idle' } // idle = not started OR in flight — both render the skeleton
  | { s: 'ready'; pdf: PDFDocumentProxy; q: PaperAnswerQuestion; region: NonNullable<ReturnType<typeof paperRegionFor>>; schemeUrl: string | null }
  | { s: 'fallback' };

interface Props {
  sibling: TopicSibling;
  saved: boolean;
  onToggleReview: () => void;
  onOpenInPaper: () => void;
}

const VaultQuestionCard: React.FC<Props> = ({ sibling, saved, onToggleReview, onOpenInPaper }) => {
  const [visible, setVisible] = useState(false);
  const [state, setState] = useState<CardState>({ s: 'idle' });
  const [lensOpen, setLensOpen] = useState(false);
  const [schemeOpen, setSchemeOpen] = useState(false);
  const [schemePdf, setSchemePdf] = useState<PDFDocumentProxy | null>(null);
  const [schemeFailed, setSchemeFailed] = useState(false);
  const rootRef = useRef<HTMLDivElement | null>(null);

  const resolved = useMemo(() => resolveSibling(sibling), [sibling]);
  // Marking Lens — the scheme-grounded marks breakdown, where one is authored.
  // Independent of the crop state: it teaches even when no crop can render.
  const lens = useMemo(() => lensFor(sibling), [sibling]);

  // Render lazily — a topic feed can span dozens of multi-MB papers.
  useEffect(() => {
    const el = rootRef.current;
    if (!el || visible) return;
    if (!('IntersectionObserver' in window)) { setVisible(true); return; }
    const obs = new IntersectionObserver(
      entries => { if (entries.some(e => e.isIntersecting)) { setVisible(true); obs.disconnect(); } },
      { rootMargin: '400px 0px' },
    );
    obs.observe(el);
    return () => obs.disconnect();
  }, [visible]);

  useEffect(() => {
    if (!visible || state.s !== 'idle') return;
    if (!resolved) { setState({ s: 'fallback' }); return; }
    // NB: no intermediate "loading" setState here — state.s is in the deps, so
    // a self-triggered transition re-runs this effect and its cleanup would
    // cancel the in-flight load. The skeleton renders for 'idle' anyway.
    let cancelled = false;
    (async () => {
      const map = await fetchAnswerMap(answerMapUrls(resolved), sibling.n);
      if (cancelled) return;
      const q = map?.q.find(x => x.n === sibling.n);
      const region = map && q ? paperRegionFor(map.q, sibling.n) : null;
      if (!q || !region) { setState({ s: 'fallback' }); return; }
      try {
        const pdf = await vaultPdf(resolved.paperUrl);
        if (cancelled) return;
        setState({ s: 'ready', pdf, q, region, schemeUrl: resolved.schemeUrl });
      } catch {
        if (!cancelled) setState({ s: 'fallback' });
      }
    })();
    return () => { cancelled = true; };
  }, [visible, state.s, resolved, sibling.n]);

  // Scheme reveal — loads the scheme PDF on first open.
  useEffect(() => {
    if (!schemeOpen || schemePdf || state.s !== 'ready' || !state.schemeUrl) return;
    let cancelled = false;
    vaultPdf(state.schemeUrl)
      .then(pdf => { if (!cancelled) setSchemePdf(pdf); })
      .catch(() => { if (!cancelled) setSchemeFailed(true); });
    return () => { cancelled = true; };
  }, [schemeOpen, schemePdf, state]);

  const meta = [
    LVL[sibling.level] ?? sibling.level,
    sibling.paperKey === 'p1' ? 'Paper 1' : sibling.paperKey === 'p2' ? 'Paper 2' : null,
    sibling.lang === 'iv' ? 'Gaeilge' : null,
  ].filter(Boolean) as string[];

  const canReveal = state.s === 'ready' && state.schemeUrl !== null && state.q.mode === 'crop';

  return (
    <div
      ref={rootRef}
      // Card stays white in dark mode (design system: all cards white) — the
      // inline ink text depends on it.
      className="rounded-2xl bg-white overflow-hidden"
      style={{ border: '2px solid #1a1a1a' }}
    >
      {/* Header row */}
      <div className="flex items-center gap-2.5 px-4 py-2.5" style={{ borderBottom: '2px solid #f0efec' }}>
        <span className="text-[19px] font-bold tabular-nums shrink-0" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>
          {sibling.year}
        </span>
        <span className="flex items-center gap-1.5 flex-wrap min-w-0">
          {meta.map(m => (
            <span key={m} className="text-[10px] font-bold uppercase tracking-[0.06em] px-2 py-0.5 rounded-full" style={{ backgroundColor: '#FDEEDF', color: '#8C3A0E', border: '1px solid rgba(242,107,31,0.2)' }}>
              {m}
            </span>
          ))}
          <span className="text-[12.5px] font-semibold" style={{ color: '#5a5550' }}>
            {(state.s === 'ready' && state.q.label) || `Question ${sibling.n}`}
          </span>
        </span>
        <span className="flex-1" />
        <button
          onClick={onToggleReview}
          aria-pressed={saved}
          aria-label={saved ? 'Remove from daily review' : 'Add to daily review'}
          title={saved ? 'In your daily review' : 'Add to daily review'}
          className="shrink-0 w-7 h-7 rounded-lg flex items-center justify-center border-2 transition-colors"
          style={saved
            ? { backgroundColor: '#E8F2EC', borderColor: '#3A8D5F', color: '#1F5F3E' }
            : { backgroundColor: '#fff', borderColor: '#d0cdc8', color: '#9e9186' }}
        >
          {saved ? <Check size={14} /> : <Plus size={14} />}
        </button>
        <button
          onClick={onOpenInPaper}
          className="shrink-0 flex items-center gap-1 text-[11.5px] font-semibold"
          style={{ color: '#9e9186' }}
          title="Open in the full paper"
        >
          Full paper <ExternalLink size={12} />
        </button>
      </div>

      {/* Body */}
      {state.s === 'ready' ? (
        // Stays light in dark mode too — the card itself is forced white
        // (design system), so a zinc-950 strip here read as a black band.
        <div className="px-3 pt-3 pb-1 bg-[#fafafa]">
          <CropView
            pdf={state.pdf}
            region={state.region}
            ariaLabel={paperCropLabel}
            failText="Couldn’t render this question — open the full paper."
          />
        </div>
      ) : state.s === 'fallback' ? (
        <button onClick={onOpenInPaper} className="w-full text-left px-4 py-3 text-[13px]" style={{ color: '#5a5550' }}>
          This question can’t be shown as a crop yet — <span className="font-semibold" style={{ color: ACCENT }}>open it in the full paper →</span>
        </button>
      ) : (
        <div className="px-4 py-6">
          <div className="h-3 rounded-full mb-2 animate-pulse" style={{ backgroundColor: '#f0efec', width: '82%' }} />
          <div className="h-3 rounded-full mb-2 animate-pulse" style={{ backgroundColor: '#f0efec', width: '64%' }} />
          <div className="h-3 rounded-full animate-pulse" style={{ backgroundColor: '#f0efec', width: '73%' }} />
        </div>
      )}

      {/* Marking Lens — how the marks are given (scheme-grounded) */}
      {lens && (
        <div style={{ borderTop: '2px solid #f0efec' }}>
          <button
            onClick={() => setLensOpen(v => !v)}
            aria-expanded={lensOpen}
            className="w-full flex items-center justify-center gap-2 px-4 py-2.5 text-[13px] font-semibold transition-colors"
            style={lensOpen ? { color: '#8C3A0E', backgroundColor: '#FDEEDF' } : { color: ACCENT }}
          >
            <Scale size={15} />
            How the marks are given
            <ChevronDown size={14} className="transition-transform" style={lensOpen ? { transform: 'rotate(180deg)' } : undefined} />
          </button>
          {lensOpen && (
            <div className="px-3 pt-3 pb-3" style={{ backgroundColor: '#FDEEDF' }}>
              <div className="flex items-start justify-between gap-3 px-1 mb-2.5">
                <p className="text-[12.5px] italic leading-snug" style={{ color: '#8C3A0E' }}>{lens.headline}</p>
                <span
                  className="shrink-0 text-[11px] font-bold px-2.5 py-1 rounded-full bg-white tabular-nums"
                  style={{ color: '#8C3A0E', border: '1px solid rgba(242,107,31,0.35)' }}
                >
                  {lens.totalMarks} marks
                </span>
              </div>
              <div className="space-y-1.5">
                {lens.parts.map((p, i) => (
                  <div
                    key={i}
                    className="flex items-start gap-3 rounded-xl bg-white px-3 py-2.5"
                    style={{ border: '1px solid rgba(242,107,31,0.25)' }}
                  >
                    <span className="flex-1 min-w-0">
                      <span className="flex items-baseline gap-2 flex-wrap">
                        {p.part && (
                          <span className="text-[10px] font-bold uppercase tracking-[0.06em]" style={{ color: '#8C3A0E' }}>{p.part}</span>
                        )}
                        <span className="text-[12.5px] font-semibold" style={{ color: INK }}>{p.task}</span>
                      </span>
                      <span className="block text-[11.5px] font-bold mt-0.5 tabular-nums" style={{ color: '#8C3A0E' }}>{p.notation}</span>
                      <span className="block text-[12px] mt-0.5 leading-snug" style={{ color: '#5a5550' }}>{p.decoded}</span>
                    </span>
                    <span className="shrink-0 text-right" aria-label={`${p.marks} marks`}>
                      <span className="text-[18px] font-bold tabular-nums" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>{p.marks}</span>
                      <span className="text-[10px] font-semibold ml-0.5" style={{ color: '#9e9186' }}>m</span>
                    </span>
                  </div>
                ))}
              </div>
              {lens.pitfall && (
                <div className="mt-2 rounded-r-xl bg-white px-3 py-2.5" style={{ borderLeft: '3px solid #F26B1F' }}>
                  <p className="text-[12px] italic leading-snug" style={{ color: '#8C3A0E' }}>Where marks are lost: {lens.pitfall.text}</p>
                  <p className="text-[10px] mt-1" style={{ color: '#9e9186' }}>{lens.pitfall.cite}</p>
                </div>
              )}
              <p className="text-[10px] font-bold uppercase tracking-[0.12em] mt-2.5 px-1" style={{ color: '#8C3A0E' }}>
                {lens.cite} — © State Examinations Commission
              </p>
            </div>
          )}
        </div>
      )}

      {/* Answer toggle */}
      {state.s === 'ready' && (
        canReveal ? (
          <div style={{ borderTop: '2px solid #f0efec' }}>
            <button
              onClick={() => setSchemeOpen(v => !v)}
              aria-expanded={schemeOpen}
              className="w-full flex items-center justify-center gap-2 px-4 py-2.5 text-[13px] font-semibold transition-colors"
              style={schemeOpen ? { color: '#1F5F3E', backgroundColor: '#E8F2EC' } : { color: ACCENT }}
            >
              <BookOpenCheck size={15} />
              {schemeOpen ? 'Hide the marking scheme' : 'Show the marking scheme'}
              <ChevronDown size={14} className="transition-transform" style={schemeOpen ? { transform: 'rotate(180deg)' } : undefined} />
            </button>
            {schemeOpen && (
              <div className="px-3 pt-3 pb-2" style={{ backgroundColor: '#E8F2EC' }}>
                <p className="text-[10px] font-bold uppercase tracking-[0.12em] mb-2 px-1" style={{ color: '#1F5F3E' }}>
                  Marking scheme — © State Examinations Commission
                </p>
                {schemePdf && state.s === 'ready' ? (
                  <CropView pdf={schemePdf} region={state.q.region} />
                ) : schemeFailed ? (
                  <p className="text-[12px] py-3 text-center" style={{ color: '#1F5F3E' }}>
                    Couldn’t load the scheme — open the question in the full paper instead.
                  </p>
                ) : (
                  <div className="h-3 rounded-full my-4 animate-pulse mx-1" style={{ backgroundColor: 'rgba(58,141,95,0.25)', width: '70%' }} />
                )}
              </div>
            )}
          </div>
        ) : (
          <button
            onClick={onOpenInPaper}
            className="w-full flex items-center justify-center gap-2 px-4 py-2.5 text-[13px] font-semibold"
            style={{ color: ACCENT, borderTop: '2px solid #f0efec' }}
          >
            <BookOpenCheck size={15} /> Open beside its marking scheme
          </button>
        )
      )}

    </div>
  );
};

export default VaultQuestionCard;
